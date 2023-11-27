use std::collections::HashSet;

use delta_data_room_api::DataRoom;
use format_types::v0::FormatType;
use format_types::v0::HashingAlgorithm;
use prost::Message;
use schemars::JsonSchema;
use serde::Deserialize;
use serde::Deserializer;
use serde::Serialize;

use crate::data_lab::features::*;
use crate::data_lab::provides::*;
use crate::data_lab::v0;
use crate::data_lab::v0::DataLabComputeV0;
use crate::feature::RequirementFlag;
use crate::feature::Requirements;
use crate::lookalike_media::LookalikeMediaDataRoom;
use crate::media::v1::EnclaveSpecificationV1;
use crate::CompileError;
use crate::CompileResult;

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(untagged)]
#[serde(rename_all = "camelCase")]
pub enum DataLabComputeOrUnknown {
    Known(DataLabCompute),
    Unknown,
}

impl DataLabComputeOrUnknown {
    pub fn parse_if_known<'de, D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: Deserializer<'de>,
    {
        match DataLabComputeOrUnknown::deserialize(deserializer) {
            Ok(known) => Ok(known),
            Err(_) => Ok(Self::Unknown),
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct DataLabV0 {
    // What this DataLab is capable of, i.e. which computations can be run.
    pub features: Vec<String>,
    // Which datasets and dataset properties this DataLab provides.
    pub provides: Requirements,
    // When parsing DataLab versions not known yet by an SDK version,
    // the actual compute structure might be unknown, but the
    // features/provides fields should still be readable
    // in order to determine the compatibility between an LMDCR and a
    // DataLab.
    #[serde(deserialize_with = "DataLabComputeOrUnknown::parse_if_known")]
    pub compute: DataLabComputeOrUnknown,
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub enum DataLab {
    V0(DataLabV0),
}

#[derive(Debug, Clone, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
/// Arguments for constructing a specific DataLab version.
pub enum CreateDataLab {
    V0(v0::CreateDataLabComputeV0),
}

impl DataLab {
    pub fn id(&self) -> CompileResult<&String> {
        match self {
            DataLab::V0(lab) => {
                match &lab.compute {
                    DataLabComputeOrUnknown::Known(lab) => {
                        match &lab {
                            DataLabCompute::V0(compute) => {
                                Ok(&compute.id)
                            }
                        }
                    }
                    DataLabComputeOrUnknown::Unknown => {
                        Err("Unknown compute payload, cannot extract id".into())
                    }
                }
            }
        }
    }

    /// Construct a specific DataLab version.
    pub fn new(args: CreateDataLab) -> CompileResult<Self> {
        let lab = match args {
            CreateDataLab::V0(args) => DataLab::V0(DataLabV0 {
                features: vec![
                    Some(COMPUTE_STATISTICS.to_string()),
                    Some(VALIDATE_MATCHING.to_string()),
                    Some(VALIDATE_SEGMENTS.to_string()),
                    args.has_demographics.then_some(VALIDATE_DEMOGRAPHICS.to_string()),
                    args.has_embeddings.then_some(VALIDATE_EMBEDDINGS.to_string()),
                ]
                .into_iter()
                .filter_map(|x| x)
                .collect(),
                provides: Requirements {
                    optional: vec![
                        Some(RequirementFlag::from_dataset(MATCHING_DATA)),
                        Some(RequirementFlag::from_dataset(SEGMENTS_DATA)),
                        args.has_demographics.then_some(RequirementFlag::from_dataset(DEMOGRAPHICS_DATA)),
                        args.has_embeddings.then_some(RequirementFlag::from_dataset(EMBEDDINGS_DATA)),
                        Some(RequirementFlag::from_matching_id_format(&args.matching_id_format)?),
                        Some(RequirementFlag::from_matching_id_hashing_algorithm(
                            args.matching_id_hashing_algorithm.as_ref(),
                        )?),
                    ]
                    .into_iter()
                    .filter_map(|x| x)
                    .collect(),
                    required: vec![],
                },
                compute: DataLabComputeOrUnknown::Known(DataLabCompute::V0(DataLabComputeV0 {
                    id: args.id,
                    name: args.name,
                    publisher_email: args.publisher_email,
                    num_embeddings: args.num_embeddings,
                    matching_id_format: args.matching_id_format,
                    matching_id_hashing_algorithm: args.matching_id_hashing_algorithm,
                    authentication_root_certificate_pem: args.authentication_root_certificate_pem,
                    driver_enclave_specification: args.driver_enclave_specification,
                    python_enclave_specification: args.python_enclave_specification,
                })),
            }),
        };
        Ok(lab)
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub enum DataLabCompute {
    V0(v0::DataLabComputeV0),
}

pub fn update_enclave_specifications_serialized(
    data_lab_serialized: String,
    driver_enclave_specification_serialized: String,
    python_enclave_specification_serialized: String,
    root_certificate_pem: String,
) -> Result<String, CompileError> {
    let data_lab: DataLab = serde_json::from_str(&data_lab_serialized)?;
    let driver_spec: EnclaveSpecificationV1 = serde_json::from_str(&driver_enclave_specification_serialized)?;
    let python_spec: EnclaveSpecificationV1 = serde_json::from_str(&python_enclave_specification_serialized)?;
    let updated = update_enclave_specifications(data_lab, driver_spec, python_spec, root_certificate_pem)?;
    let updated_serialized = serde_json::to_string(&updated)?;
    Ok(updated_serialized)
}

pub fn update_enclave_specifications(
    data_room: DataLab,
    driver_enclave_specification: EnclaveSpecificationV1,
    python_enclave_specification: EnclaveSpecificationV1,
    root_certificate_pem: String,
) -> Result<DataLab, CompileError> {
    let updated = match data_room {
        DataLab::V0(data_lab) => match data_lab.compute {
            DataLabComputeOrUnknown::Known(compute) => match compute {
                DataLabCompute::V0(compute) => DataLab::V0(DataLabV0 {
                    features: data_lab.features,
                    provides: data_lab.provides,
                    compute: DataLabComputeOrUnknown::Known(DataLabCompute::V0(DataLabComputeV0 {
                        authentication_root_certificate_pem: root_certificate_pem,
                        driver_enclave_specification,
                        python_enclave_specification,
                        ..compute
                    })),
                }),
            },
            DataLabComputeOrUnknown::Unknown => {
                return Err(CompileError::from(
                    "Encountered an unknown compute version that is not known to this version of the compiler",
                ));
            }
        },
    };
    Ok(updated)
}

/// Compile a high-level DataLab into the low-level DCR that can be published via the driver.
pub fn compile_data_lab(data_room: &DataLab) -> Result<DataRoom, CompileError> {
    let features = data_room.get_features();
    let requirements = data_room.get_requirements();
    let feature_set: HashSet<&String> = features.iter().collect();
    match data_room {
        DataLab::V0(data_lab) => match &data_lab.compute {
            DataLabComputeOrUnknown::Known(compute) => match &compute {
                DataLabCompute::V0(compute) => v0::compile_compute(compute, feature_set, requirements),
            },
            DataLabComputeOrUnknown::Unknown => Err(CompileError::from(
                "Encountered an unknown compute version that is not known to this version of the compiler",
            )),
        },
    }
}

pub fn get_data_lab_features_serialized(json: &str) -> Result<Vec<String>, CompileError> {
    let lab: DataLab = serde_json::from_str(json)?;
    Ok(lab.get_features().clone())
}

pub fn create_data_lab_serialized(args_json: &str) -> Result<String, CompileError> {
    let args: CreateDataLab = serde_json::from_str(args_json)?;
    let lab = DataLab::new(args)?;
    Ok(serde_json::to_string(&lab)?)
}

pub fn compile_data_lab_serialized(json: &str) -> Result<Vec<u8>, CompileError> {
    let lab: DataLab = serde_json::from_str(json)?;
    let low_level_dcr = compile_data_lab(&lab)?;
    let serialized = low_level_dcr.encode_length_delimited_to_vec();
    Ok(serialized)
}

pub fn convert_data_lab_any_to_latest_serialized(media_data_room_versioned_serialized: &str) -> CompileResult<String> {
    let data_room: DataLab = serde_json::from_str(media_data_room_versioned_serialized)?;
    Ok(serde_json::to_string(&convert_data_lab_any_to_latest(data_room)?)?)
}

/// Check whether a JSON-serialized DataLab is compatible with a JSON-serialized LMDCR.
pub fn is_data_lab_compatible_with_lookalike_media_dcr_serialized(
    data_lab_json: &str,
    dcr_json: &str,
) -> Result<bool, CompileError> {
    let lab: DataLab = serde_json::from_str(data_lab_json)?;
    let dcr: LookalikeMediaDataRoom = serde_json::from_str(dcr_json)?;
    Ok(lab.is_compatible_with_lookalike_media_dcr(&dcr)?)
}

fn convert_data_lab_any_to_latest(data_room: DataLab) -> CompileResult<DataLab> {
    enum OldOrLatest {
        Old(DataLab),
        Latest(DataLab),
    }
    fn convert_any_to_next(data_room: DataLab) -> CompileResult<OldOrLatest> {
        match data_room {
            DataLab::V0(data_lab) => Ok(OldOrLatest::Latest(DataLab::V0(data_lab))),
        }
    }
    let mut current = data_room;
    loop {
        match convert_any_to_next(current)? {
            OldOrLatest::Old(next) => {
                current = next;
            }
            OldOrLatest::Latest(latest) => return Ok(latest),
        }
    }
}

impl DataLab {
    pub fn get_features(&self) -> &Vec<String> {
        match self {
            DataLab::V0(wrapper) => &wrapper.features,
        }
    }

    pub fn get_requirements(&self) -> &Requirements {
        match self {
            DataLab::V0(wrapper) => &wrapper.provides,
        }
    }

    pub fn does_require_demographics_dataset(&self) -> bool {
        self.get_requirements().contains_all(&RequirementFlag::from_dataset(DEMOGRAPHICS_DATA))
    }

    pub fn name(&self) -> CompileResult<&String> {
        match self {
            DataLab::V0(lab) => match &lab.compute {
                DataLabComputeOrUnknown::Known(compute) => match &compute {
                    DataLabCompute::V0(compute) => Ok(&compute.name),
                },
                DataLabComputeOrUnknown::Unknown => Err("Cannot parse DataLab, unknown compute definition".into()),
            },
        }
    }

    pub fn num_embeddings(&self) -> CompileResult<usize> {
        match self {
            DataLab::V0(lab) => match &lab.compute {
                DataLabComputeOrUnknown::Known(compute) => match &compute {
                    DataLabCompute::V0(compute) => Ok(compute.num_embeddings),
                },
                DataLabComputeOrUnknown::Unknown => Err("Cannot parse DataLab, unknown compute definition".into()),
            },
        }
    }

    pub fn matching_id_format(&self) -> CompileResult<&FormatType> {
        match &self {
            DataLab::V0(lab) => match &lab.compute {
                DataLabComputeOrUnknown::Known(compute) => match &compute {
                    DataLabCompute::V0(compute) => Ok(&compute.matching_id_format),
                },
                DataLabComputeOrUnknown::Unknown => Err("Cannot parse DataLab, unknown compute definition".into()),
            },
        }
    }

    pub fn matching_id_hashing_algorithm(&self) -> CompileResult<Option<&HashingAlgorithm>> {
        match &self {
            DataLab::V0(lab) => match &lab.compute {
                DataLabComputeOrUnknown::Known(compute) => match &compute {
                    DataLabCompute::V0(compute) => Ok(compute.matching_id_hashing_algorithm.as_ref()),
                },
                DataLabComputeOrUnknown::Unknown => Err("Cannot parse DataLab, unknown compute definition".into()),
            },
        }
    }

    pub fn does_require_embeddings_dataset(&self) -> bool {
        self.get_requirements().contains_all(&RequirementFlag::from_dataset(EMBEDDINGS_DATA.into()))
    }

    pub fn is_compatible_with_lookalike_media_dcr(&self, dcr: &LookalikeMediaDataRoom) -> CompileResult<bool> {
        let data_lab_requirements = self.get_requirements();
        let lm_dcr_requirements = dcr.get_requirements()?;
        let is_compatible = data_lab_requirements.is_compatible_with(&lm_dcr_requirements);
        Ok(is_compatible)
    }
}

#[cfg(test)]
mod tests {
    use format_types::v0::FormatType;
    use format_types::v0::HashingAlgorithm;

    use crate::data_lab::compiler::CreateDataLab;
    use crate::data_lab::compiler::DataLabComputeOrUnknown;
    use crate::data_lab::v0::CreateDataLabComputeV0;
    use crate::data_lab::DataLab;
    use crate::lookalike_media::compiler::CreateLookalikeMediaDataRoom;
    use crate::lookalike_media::v0::LookalikeMediaDataRoomV0;
    use crate::lookalike_media::LookalikeMediaDataRoom;
    use crate::media::v0::EnclaveSpecification;

    #[test]
    fn check_compatibility_of_hashing_format() {
        let lab = DataLab::new(CreateDataLab::V0(CreateDataLabComputeV0 {
            id: "xyz".to_string(),
            name: "my_datalab".to_string(),
            publisher_email: "hello@bla.com".to_string(),
            has_demographics: true,
            has_embeddings: true,
            num_embeddings: 50,
            matching_id_format: FormatType::String,
            matching_id_hashing_algorithm: Some(HashingAlgorithm::Sha256Hex),
            authentication_root_certificate_pem: "".to_string(),
            driver_enclave_specification: EnclaveSpecification {
                id: "hai".to_string(),
                attestation_proto_base64: "123".to_string(),
                worker_protocol: 0,
            },
            python_enclave_specification: EnclaveSpecification {
                id: "hai".to_string(),
                attestation_proto_base64: "123".to_string(),
                worker_protocol: 0,
            },
        }))
        .unwrap();
        println!("{}", serde_json::to_string_pretty(&lab).unwrap());

        let dcr_without_hashed_ids =
            LookalikeMediaDataRoom::new(CreateLookalikeMediaDataRoom::V0(LookalikeMediaDataRoomV0 {
                id: "xyz".to_string(),
                name: "my dcr".to_string(),
                main_publisher_email: "user@publisher.com".to_string(),
                main_advertiser_email: "user@advrtiser.com".to_string(),
                publisher_emails: vec![],
                advertiser_emails: vec![],
                observer_emails: vec![],
                agency_emails: vec![],
                enable_download_by_publisher: false,
                enable_download_by_advertiser: false,
                enable_download_by_agency: false,
                enable_overlap_insights: false,
                enable_audit_log_retrieval: false,
                enable_dev_computations: false,
                authentication_root_certificate_pem: "".to_string(),
                driver_enclave_specification: crate::lookalike_media::v0::EnclaveSpecificationV0 {
                    id: "".to_string(),
                    attestation_proto_base64: "".to_string(),
                    worker_protocol: 0,
                },
                python_enclave_specification: crate::lookalike_media::v0::EnclaveSpecificationV0 {
                    id: "".to_string(),
                    attestation_proto_base64: "".to_string(),
                    worker_protocol: 0,
                },
                matching_id_format: FormatType::String,
                hash_matching_id_with: None,
            }))
            .unwrap();

        println!("{}", serde_json::to_string_pretty(&dcr_without_hashed_ids).unwrap());
        assert!(!lab.is_compatible_with_lookalike_media_dcr(&dcr_without_hashed_ids).unwrap());

        let dcr_with_hashed_ids =
            LookalikeMediaDataRoom::new(CreateLookalikeMediaDataRoom::V0(LookalikeMediaDataRoomV0 {
                id: "xyz".to_string(),
                name: "my dcr".to_string(),
                main_publisher_email: "user@publisher.com".to_string(),
                main_advertiser_email: "user@advrtiser.com".to_string(),
                publisher_emails: vec![],
                advertiser_emails: vec![],
                observer_emails: vec![],
                agency_emails: vec![],
                enable_download_by_publisher: false,
                enable_download_by_advertiser: false,
                enable_download_by_agency: false,
                enable_overlap_insights: false,
                enable_audit_log_retrieval: false,
                enable_dev_computations: false,
                authentication_root_certificate_pem: "".to_string(),
                driver_enclave_specification: crate::lookalike_media::v0::EnclaveSpecificationV0 {
                    id: "".to_string(),
                    attestation_proto_base64: "".to_string(),
                    worker_protocol: 0,
                },
                python_enclave_specification: crate::lookalike_media::v0::EnclaveSpecificationV0 {
                    id: "".to_string(),
                    attestation_proto_base64: "".to_string(),
                    worker_protocol: 0,
                },
                matching_id_format: FormatType::String,
                hash_matching_id_with: Some(HashingAlgorithm::Sha256Hex),
            }))
            .unwrap();
        println!("{}", serde_json::to_string_pretty(&dcr_with_hashed_ids).unwrap());

        assert!(lab.is_compatible_with_lookalike_media_dcr(&dcr_with_hashed_ids).unwrap());
    }

    #[test]
    fn check_forwards_compatibility_when_parsing_data_labs() {
        let lab: DataLab = serde_json::from_str(
            r#"
            {
                "v0": {
                    "features": ["hello"],
                    "provides": {
                        "optional": [],
                        "required": []
                    },
                    "compute": {
                        "v999": {
                            "field1": {
                                "field2": 123
                            }
                        }
                    }
                }
            }
        "#,
        )
        .unwrap();

        assert!(!lab.get_features().is_empty());
        match lab {
            DataLab::V0(lab) => match lab.compute {
                DataLabComputeOrUnknown::Known(_) => {
                    panic!("Compute should be unknown");
                }
                DataLabComputeOrUnknown::Unknown => {}
            },
        }
    }
}
