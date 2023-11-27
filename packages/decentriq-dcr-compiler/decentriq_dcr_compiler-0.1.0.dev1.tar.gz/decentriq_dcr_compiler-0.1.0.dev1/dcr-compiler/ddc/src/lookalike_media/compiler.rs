use delta_attestation_api::*;
use delta_data_room_api::DataRoom;
use delta_gcg_driver_api::*;
use format_types::v0::FormatType;
use format_types::v0::HashingAlgorithm;
use schemars::JsonSchema;
use serde::Deserialize;
use serde::Serialize;

use super::v0;
use super::v1;
use super::v2;
use crate::data_lab;
use crate::feature::RequirementFlag;
use crate::feature::RequirementList;
use crate::feature::Requirements;
use crate::lookalike_media::features::ENABLE_AUDIT_LOG_RETRIEVAL;
use crate::lookalike_media::features::ENABLE_DEV_COMPUTATIONS;
use crate::lookalike_media::features::ENABLE_RATE_LIMITING_ON_PUBLISH_DATASET;
use crate::lookalike_media::v0::LookalikeMediaDataRoomV0;
use crate::lookalike_media::v0::ACTIVATED_AUDIENCES_CONFIG_ID;
use crate::lookalike_media::v0::COMPUTE_AUDIENCE_SIZES_ID;
use crate::lookalike_media::v0::CONSENTLESS_OVERLAP_INSIGHTS_ID;
use crate::lookalike_media::v0::DATASET_AUDIENCES_ID;
use crate::lookalike_media::v0::DATASET_DEMOGRAPHICS_ID;
use crate::lookalike_media::v0::DATASET_EMBEDDINGS_ID;
use crate::lookalike_media::v0::DATASET_MATCHING_ID;
use crate::lookalike_media::v0::DATASET_SEGMENTS_ID;
use crate::lookalike_media::v0::GET_LOOKALIKE_AUDIENCE_ID;
use crate::lookalike_media::v0::MODELLED_AUDIENCE_INSIGHTS_ID;
use crate::lookalike_media::v0::MODELLED_AUDIENCE_INSIGHTS_VIEW_ID;
use crate::lookalike_media::v0::OVERLAP_BASIC_ID;
use crate::lookalike_media::v0::REQUESTED_AUDIENCE_CONFIG_ID;
use crate::lookalike_media::v0::VIEW_ACTIVATED_AUDIENCES_ID;
use crate::lookalike_media::v0::VIEW_PUBLISHED_ACTIVATED_AUDIENCES_ID;
use crate::lookalike_media::v1::LookalikeMediaDataRoomV1;
use crate::lookalike_media::v2::LookalikeMediaDataRoomV2;
use crate::lookalike_media::v2::INGEST_AUDIENCES_REPORT_ID;
use crate::lookalike_media::v3;
use crate::lookalike_media::v3::compute::v0::default_enable_rate_limiting_on_publish_dataset;
use crate::lookalike_media::v3::compute::v0::default_rate_limit_publish_data_num_per_window;
use crate::lookalike_media::v3::compute::v0::default_rate_limit_publish_data_window_seconds;
use crate::lookalike_media::v3::compute::v0::LookalikeMediaDcrComputeV0;
use crate::lookalike_media::v3::compute::CreateLookalikeMediaDcrCompute;
use crate::lookalike_media::v3::compute::LookalikeMediaDcrCompute;
use crate::lookalike_media::v3::LookalikeMediaDcrComputeOrUnknown;
use crate::lookalike_media::v3::LookalikeMediaDcrWrapper;
use crate::CompileError;
use crate::CompileResult;

/// The high-level representation of an LMDCR.
/// Starting with version 4, an outer structure has been introduced that exposes the "features"
/// supported by the LMDCR via string-based flags. This way, every version of DDC can extract these
/// feature flags and inform the SDKs whether a particular function is supported by this LMDCR.
/// In a similar way, the LMDCR exposes what datasets it needs as input from a DataLab such that
/// we can check the compatibility between a DataLab and a LMDCR from any version of DDC/the SDKs.
#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub enum LookalikeMediaDataRoom {
    V0(v0::LookalikeMediaDataRoomV0),
    V1(v1::LookalikeMediaDataRoomV1),
    V2(v2::LookalikeMediaDataRoomV2),
    V3(v3::LookalikeMediaDcrWrapper),
}

/// Arguments for creating a specific version of an LMDCR.
#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub enum CreateLookalikeMediaDataRoom {
    V0(v0::LookalikeMediaDataRoomV0),
    V1(v1::LookalikeMediaDataRoomV1),
    V2(v2::LookalikeMediaDataRoomV2),
    V3(v3::compute::CreateLookalikeMediaDcrCompute),
}

impl LookalikeMediaDataRoom {
    /// Create a Lookalike Media DCR.
    pub fn new(args: CreateLookalikeMediaDataRoom) -> CompileResult<LookalikeMediaDataRoom> {
        let dcr = match args {
            CreateLookalikeMediaDataRoom::V0(args) => LookalikeMediaDataRoom::V0(LookalikeMediaDataRoomV0 { ..args }),
            CreateLookalikeMediaDataRoom::V1(args) => LookalikeMediaDataRoom::V1(LookalikeMediaDataRoomV1 { ..args }),
            CreateLookalikeMediaDataRoom::V2(args) => LookalikeMediaDataRoom::V2(LookalikeMediaDataRoomV2 { ..args }),
            CreateLookalikeMediaDataRoom::V3(compute) => match compute {
                CreateLookalikeMediaDcrCompute::V0(args) => {
                    LookalikeMediaDataRoom::V3(LookalikeMediaDcrWrapper {
                        // As soon as we provide SDK support for the LMDCR, we need to provide the full set of features
                        // here (i.e. what computations can be run in the LMDCR) so that SDKs
                        // starting from that version can correctly check for these flags to see whether a particular
                        // computation can be run.
                        // The ENABLE-style flags are required as the compiler was changed s.t. it already determines
                        // what features to add to a DCR based on these flags, rather than properties of the compute
                        // structure.
                        features: vec![
                            args.enable_audit_log_retrieval.then_some(ENABLE_AUDIT_LOG_RETRIEVAL.to_string()),
                            args.enable_dev_computations.then_some(ENABLE_DEV_COMPUTATIONS.to_string()),
                            args.enable_rate_limiting_on_publish_dataset
                                .unwrap_or(default_enable_rate_limiting_on_publish_dataset())
                                .then_some(ENABLE_RATE_LIMITING_ON_PUBLISH_DATASET.to_string()),
                        ]
                        .into_iter()
                        .filter_map(|x| x)
                        .collect(),
                        consumes: Requirements {
                            optional: vec![
                                RequirementFlag::from_dataset(data_lab::provides::DEMOGRAPHICS_DATA),
                                RequirementFlag::from_dataset(data_lab::provides::EMBEDDINGS_DATA),
                            ],
                            required: vec![
                                RequirementFlag::from_dataset(data_lab::provides::MATCHING_DATA),
                                RequirementFlag::from_dataset(data_lab::provides::SEGMENTS_DATA),
                                RequirementFlag::from_matching_id_format(&args.matching_id_format)?,
                                RequirementFlag::from_matching_id_hashing_algorithm(
                                    args.hash_matching_id_with.as_ref(),
                                )?,
                            ],
                        },
                        compute: LookalikeMediaDcrComputeOrUnknown::Known(LookalikeMediaDcrCompute::V0(
                            LookalikeMediaDcrComputeV0 {
                                id: args.id,
                                name: args.name,
                                main_publisher_email: args.main_publisher_email,
                                main_advertiser_email: args.main_advertiser_email,
                                publisher_emails: args.publisher_emails,
                                advertiser_emails: args.advertiser_emails,
                                observer_emails: args.observer_emails,
                                agency_emails: args.agency_emails,
                                matching_id_format: args.matching_id_format,
                                hash_matching_id_with: args.hash_matching_id_with,
                                authentication_root_certificate_pem: args.authentication_root_certificate_pem,
                                driver_enclave_specification: args.driver_enclave_specification,
                                python_enclave_specification: args.python_enclave_specification,
                                rate_limit_publish_data_window_seconds: args
                                    .rate_limit_publish_data_window_seconds
                                    .unwrap_or(default_rate_limit_publish_data_window_seconds()),
                                rate_limit_publish_data_num_per_window: args
                                    .rate_limit_publish_data_num_per_window
                                    .unwrap_or(default_rate_limit_publish_data_num_per_window()),
                            },
                        )),
                    })
                }
            },
        };
        Ok(dcr)
    }

    /// Extract the array of feature flags from this LMDCR.
    pub fn get_features(&self) -> Vec<String> {
        match self {
            // As soon as we provide SDK support for the LMDCR, we need to provide the set of features
            // here (i.e. what computations can be run in the LMDCR) so that SDKs starting from that
            // version can correctly check for these flags to see whether a particular computation
            // can be run.
            LookalikeMediaDataRoom::V0(_) | LookalikeMediaDataRoom::V1(_) | LookalikeMediaDataRoom::V2(_) => {
                vec![]
            }
            // Starting with V3, feature flags are correctly exposed on the outer wrapper structure
            // and can simply be extracted from there.
            LookalikeMediaDataRoom::V3(dcr) => dcr.features.clone(),
        }
    }

    /// Extract the list of consumed data sets. Each of the flag returned by this
    /// function should correspond to a data node to which data can be provisioned.
    pub fn get_consumed_datasets(&self) -> CompileResult<RequirementList> {
        Ok(self.get_requirements()?.get_datasets())
    }

    /// Extract the "consumes" flags, i.e. what datasets/properties this LMDCR takes as input.
    pub fn get_requirements(&self) -> CompileResult<Requirements> {
        // DCR versions <V3 don't yet expose the datasets they consume as part of an outer
        // wrapper structure that can be understood by all DDC versions in a backwards and forwards
        // compatible way (i.e. DDC must be able to understand the exposed datasets of older and
        // newer DCR versions).
        fn legacy_consumer_list(
            matching_id_format: &FormatType,
            hashing_alg: Option<&HashingAlgorithm>,
        ) -> CompileResult<Requirements> {
            Ok(Requirements {
                optional: vec![
                    RequirementFlag::from_dataset(data_lab::provides::DEMOGRAPHICS_DATA),
                    RequirementFlag::from_dataset(data_lab::provides::EMBEDDINGS_DATA),
                ],
                required: vec![
                    RequirementFlag::from_dataset(data_lab::provides::MATCHING_DATA),
                    RequirementFlag::from_dataset(data_lab::provides::SEGMENTS_DATA),
                    RequirementFlag::from_matching_id_format(matching_id_format)?,
                    RequirementFlag::from_matching_id_hashing_algorithm(hashing_alg)?,
                ],
            })
        }
        Ok(match self {
            LookalikeMediaDataRoom::V0(dcr) => {
                legacy_consumer_list(&dcr.matching_id_format, dcr.hash_matching_id_with.as_ref())?
            }
            LookalikeMediaDataRoom::V1(dcr) => {
                legacy_consumer_list(&dcr.matching_id_format, dcr.hash_matching_id_with.as_ref())?
            }
            LookalikeMediaDataRoom::V2(dcr) => {
                legacy_consumer_list(&dcr.matching_id_format, dcr.hash_matching_id_with.as_ref())?
            }
            // Starting with V3 we can simply extract the "consumes" part from the outer structure
            LookalikeMediaDataRoom::V3(wrapper) => wrapper.consumes.clone(),
        })
    }
}

pub type LookalikeMediaDataRoomLatest = v3::compute::v0::LookalikeMediaDcrComputeV0;

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[schemars(deny_unknown_fields)]
#[serde(rename_all = "camelCase")]
pub struct RequestedAudiencePayload {
    pub audience_type: String,
    pub reach: f32,
}

/// MediaRequest -> GcgRequest
#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[schemars(deny_unknown_fields)]
#[serde(rename_all = "camelCase")]
pub enum LookalikeMediaRequest {
    #[serde(rename_all = "camelCase")]
    PublishDataRoom {
        data_room: LookalikeMediaDataRoom,
        show_organization_logo: bool,
        require_password: bool,
    },
    #[serde(rename_all = "camelCase")]
    RetrieveDataRoom {
        data_room_id_hex: String,
    },
    #[serde(rename_all = "camelCase")]
    PublishAdvertiserDataset {
        data_room_id_hex: String,
        dataset_hash_hex: String,
        encryption_key_hex: String,
        scope_id_hex: String,
    },
    #[serde(rename_all = "camelCase")]
    PublishPublisherUsersDataset {
        data_room_id_hex: String,
        dataset_hash_hex: String,
        encryption_key_hex: String,
        scope_id_hex: String,
    },
    #[serde(rename_all = "camelCase")]
    UnpublishPublisherUsersDataset {
        data_room_id_hex: String,
    },
    #[serde(rename_all = "camelCase")]
    UnpublishAdvertiserDataset {
        data_room_id_hex: String,
    },
    #[serde(rename_all = "camelCase")]
    UnpublishDemographicsDataset {
        data_room_id_hex: String,
    },
    #[serde(rename_all = "camelCase")]
    UnpublishEmbeddingsDataset {
        data_room_id_hex: String,
    },
    #[serde(rename_all = "camelCase")]
    UnpublishSegmentsDataset {
        data_room_id_hex: String,
    },
    #[serde(rename_all = "camelCase")]
    RetrievePublishedDatasets {
        data_room_id_hex: String,
    },
    #[serde(rename_all = "camelCase")]
    CalculateOverlapBasic {
        data_room_id_hex: String,
        scope_id_hex: String,
    },
    #[serde(rename_all = "camelCase")]
    CalculateOverlapInsights {
        data_room_id_hex: String,
        scope_id_hex: String,
    },
    #[serde(rename_all = "camelCase")]
    PublishDemographicsDataset {
        data_room_id_hex: String,
        dataset_hash_hex: String,
        encryption_key_hex: String,
        scope_id_hex: String,
    },
    #[serde(rename_all = "camelCase")]
    PublishSegmentsDataset {
        data_room_id_hex: String,
        dataset_hash_hex: String,
        encryption_key_hex: String,
        scope_id_hex: String,
    },
    #[serde(rename_all = "camelCase")]
    PublishEmbeddingsDataset {
        data_room_id_hex: String,
        dataset_hash_hex: String,
        encryption_key_hex: String,
        scope_id_hex: String,
    },
    #[serde(rename_all = "camelCase")]
    PublishActivatedAudiencesConfig {
        data_room_id_hex: String,
        dataset_hash_hex: String,
        encryption_key_hex: String,
        scope_id_hex: String,
    },
    #[serde(rename_all = "camelCase")]
    UnpublishActivatedAudiencesConfig {
        data_room_id_hex: String,
    },
    #[serde(rename_all = "camelCase")]
    CalculateModelledAudienceInsights {
        data_room_id_hex: String,
        scope_id_hex: String,
    },
    #[serde(rename_all = "camelCase")]
    CalculateModelledAudienceInsightsView {
        data_room_id_hex: String,
        scope_id_hex: String,
    },
    #[serde(rename_all = "camelCase")]
    ComputeAudienceSizes {
        data_room_id_hex: String,
        scope_id_hex: String,
    },
    #[serde(rename_all = "camelCase")]
    GetLookalikeAudience {
        data_room_id_hex: String,
        scope_id_hex: String,
        requested_audience: RequestedAudiencePayload,
    },
    #[serde(rename_all = "camelCase")]
    ViewPublishedActivatedAudiences {
        data_room_id_hex: String,
        scope_id_hex: String,
    },
    #[serde(rename_all = "camelCase")]
    ViewActivatedAudiences {
        data_room_id_hex: String,
        scope_id_hex: String,
    },
    #[serde(rename_all = "camelCase")]
    IngestAudiencesReport {
        data_room_id_hex: String,
        scope_id_hex: String,
    },
}

/// GcgResponse -> MediaResponse
#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[schemars(deny_unknown_fields)]
#[serde(rename_all = "camelCase")]
pub enum LookalikeMediaResponse {
    #[serde(rename_all = "camelCase")]
    PublishDataRoom {
        data_room_id: String,
    },
    #[serde(rename_all = "camelCase")]
    RetrieveDataRoom {
        data_room: LookalikeMediaDataRoom,
    },
    #[serde(rename_all = "camelCase")]
    PublishAdvertiserDataset {},
    #[serde(rename_all = "camelCase")]
    PublishPublisherUsersDataset {},
    #[serde(rename_all = "camelCase")]
    UnpublishPublisherUsersDataset {},
    #[serde(rename_all = "camelCase")]
    PublishDemographicsDataset {},
    #[serde(rename_all = "camelCase")]
    UnpublishDemographicsDataset {},
    #[serde(rename_all = "camelCase")]
    PublishSegmentsDataset {},
    #[serde(rename_all = "camelCase")]
    UnpublishSegmentsDataset {},
    #[serde(rename_all = "camelCase")]
    PublishEmbeddingsDataset {},
    #[serde(rename_all = "camelCase")]
    UnpublishEmbeddingsDataset {},
    #[serde(rename_all = "camelCase")]
    UnpublishAdvertiserDataset {},
    #[serde(rename_all = "camelCase")]
    RetrievePublishedDatasets {
        advertiser_dataset_hash_hex: Option<String>,
        publisher_dataset_hash_hex: Option<String>,
        demographics_dataset_hash_hex: Option<String>,
        segments_dataset_hash_hex: Option<String>,
        embeddings_dataset_hash_hex: Option<String>,
    },
    #[serde(rename_all = "camelCase")]
    CalculateOverlapBasic {
        compute_node_name: String,
        job_id_hex: String,
    },
    #[serde(rename_all = "camelCase")]
    ComputeAudienceSizes {
        compute_node_name: String,
        job_id_hex: String,
    },
    #[serde(rename_all = "camelCase")]
    CalculateOverlapInsights {
        compute_node_name: String,
        job_id_hex: String,
    },
    #[serde(rename_all = "camelCase")]
    PublishActivatedAudiencesConfig {},
    #[serde(rename_all = "camelCase")]
    UnpublishActivatedAudiencesConfig {},
    #[serde(rename_all = "camelCase")]
    GetLookalikeAudience {
        compute_node_name: String,
        job_id_hex: String,
    },
    #[serde(rename_all = "camelCase")]
    CalculateModelledAudienceInsights {
        compute_node_name: String,
        job_id_hex: String,
    },
    #[serde(rename_all = "camelCase")]
    CalculateModelledAudienceInsightsView {
        compute_node_name: String,
        job_id_hex: String,
    },
    #[serde(rename_all = "camelCase")]
    ViewPublishedActivatedAudiences {
        compute_node_name: String,
        job_id_hex: String,
    },
    #[serde(rename_all = "camelCase")]
    ViewActivatedAudiences {
        compute_node_name: String,
        job_id_hex: String,
    },
    #[serde(rename_all = "camelCase")]
    IngestAudiencesReport {
        compute_node_name: String,
        job_id_hex: String,
    },
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[schemars(deny_unknown_fields)]
#[serde(rename_all = "camelCase")]
pub struct ConsentlessAudience {
    id: String,
    audience_type: String,
    precision: f64,
    activated: bool,
    downloaded: bool,
}

pub fn create_lookalike_media_data_room_serialized(args_json: &str) -> Result<String, CompileError> {
    let args: CreateLookalikeMediaDataRoom = serde_json::from_str(args_json)?;
    let dcr = LookalikeMediaDataRoom::new(args)?;
    Ok(serde_json::to_string(&dcr)?)
}

pub fn compile_lookalike_media_data_room_serialized(dcr_json: &str) -> Result<Vec<u8>, CompileError> {
    let dcr: LookalikeMediaDataRoom = serde_json::from_str(dcr_json)?;
    let low_level_dcr = compile_lookalike_media_data_room(&dcr)?;
    Ok(prost::Message::encode_length_delimited_to_vec(&low_level_dcr))
}

pub fn compile_lookalike_media_request_serialized(
    media_request: &str,
    user_auth_serialized: &[u8],
) -> Result<Vec<u8>, CompileError> {
    let media_request: LookalikeMediaRequest = serde_json::from_str(media_request)?;
    let gcg_request_enum = compile_lookalike_media_request(&media_request)?;
    let gcg_request = GcgRequest {
        user_auth: Some(prost::Message::decode_length_delimited(user_auth_serialized)?),
        gcg_request: Some(gcg_request_enum),
    };
    Ok(prost::Message::encode_length_delimited_to_vec(&gcg_request))
}

pub fn decompile_lookalike_media_response_serialized(
    media_request: &str,
    gcg_response_serialized: &[u8],
) -> Result<String, CompileError> {
    let media_request: LookalikeMediaRequest = serde_json::from_str(media_request)?;
    let gcg_response: GcgResponse = prost::Message::decode_length_delimited(gcg_response_serialized)?;
    let media_response = decompile_lookalike_media_response(&media_request, gcg_response)?;
    Ok(serde_json::to_string(&media_response)?)
}

fn compile_lookalike_media_data_room(data_room: &LookalikeMediaDataRoom) -> Result<DataRoom, CompileError> {
    match data_room {
        LookalikeMediaDataRoom::V0(data_room) => v0::compile_lookalike_media_data_room_v0(data_room),
        LookalikeMediaDataRoom::V1(data_room) => v1::compile_lookalike_media_data_room_v1(data_room),
        LookalikeMediaDataRoom::V2(data_room) => v2::compile_lookalike_media_data_room_v2(data_room),
        LookalikeMediaDataRoom::V3(wrapper) => v3::compute::compile_data_room_compute(
            &wrapper.compute,
            &data_room.get_features(),
            &data_room.get_requirements()?,
        ),
    }
}

fn compile_lookalike_media_request(
    media_request: &LookalikeMediaRequest,
) -> Result<gcg_request::GcgRequest, CompileError> {
    match media_request {
        LookalikeMediaRequest::PublishDataRoom {
            data_room: media_data_room,
            show_organization_logo,
            require_password,
        } => {
            let low_level_data_room = compile_lookalike_media_data_room(media_data_room)?;
            let high_level_data_room = serde_json::to_vec(media_data_room)?;
            let metadata = delta_extension_metering_api::DcrMetadata {
                kind: delta_extension_metering_api::CreateDcrKind::LookalikeMedia.into(),
                show_organization_logo: *show_organization_logo,
                require_password: *require_password,
                purpose: delta_extension_metering_api::CreateDcrPurpose::Standard.into(),
            };
            let metadata_serialized = prost::Message::encode_length_delimited_to_vec(&metadata);
            Ok(gcg_request::GcgRequest::CreateDataRoomRequest(CreateDataRoomRequest {
                data_room: Some(low_level_data_room),
                high_level_representation: Some(high_level_data_room),
                data_room_metadata: Some(metadata_serialized),
            }))
        }
        LookalikeMediaRequest::RetrieveDataRoom { data_room_id_hex } => {
            Ok(gcg_request::GcgRequest::RetrieveDataRoomRequest(RetrieveDataRoomRequest {
                data_room_id: hex::decode(data_room_id_hex)?,
            }))
        }
        LookalikeMediaRequest::PublishAdvertiserDataset {
            data_room_id_hex,
            dataset_hash_hex,
            encryption_key_hex,
            scope_id_hex,
        } => Ok(gcg_request::GcgRequest::PublishDatasetToDataRoomRequest(PublishDatasetToDataRoomRequest {
            dataset_hash: hex::decode(dataset_hash_hex)?,
            data_room_id: hex::decode(data_room_id_hex)?,
            leaf_id: DATASET_AUDIENCES_ID.to_string(),
            encryption_key: hex::decode(encryption_key_hex)?,
            scope: hex::decode(scope_id_hex)?,
        })),
        LookalikeMediaRequest::PublishPublisherUsersDataset {
            data_room_id_hex,
            dataset_hash_hex,
            encryption_key_hex,
            scope_id_hex,
        } => Ok(gcg_request::GcgRequest::PublishDatasetToDataRoomRequest(PublishDatasetToDataRoomRequest {
            dataset_hash: hex::decode(dataset_hash_hex)?,
            data_room_id: hex::decode(data_room_id_hex)?,
            leaf_id: DATASET_MATCHING_ID.to_string(),
            encryption_key: hex::decode(encryption_key_hex)?,
            scope: hex::decode(scope_id_hex)?,
        })),
        LookalikeMediaRequest::PublishDemographicsDataset {
            data_room_id_hex,
            dataset_hash_hex,
            encryption_key_hex,
            scope_id_hex,
        } => Ok(gcg_request::GcgRequest::PublishDatasetToDataRoomRequest(PublishDatasetToDataRoomRequest {
            dataset_hash: hex::decode(dataset_hash_hex)?,
            data_room_id: hex::decode(data_room_id_hex)?,
            leaf_id: DATASET_DEMOGRAPHICS_ID.to_string(),
            encryption_key: hex::decode(encryption_key_hex)?,
            scope: hex::decode(scope_id_hex)?,
        })),
        LookalikeMediaRequest::PublishEmbeddingsDataset {
            data_room_id_hex,
            dataset_hash_hex,
            encryption_key_hex,
            scope_id_hex,
        } => Ok(gcg_request::GcgRequest::PublishDatasetToDataRoomRequest(PublishDatasetToDataRoomRequest {
            dataset_hash: hex::decode(dataset_hash_hex)?,
            data_room_id: hex::decode(data_room_id_hex)?,
            leaf_id: DATASET_EMBEDDINGS_ID.to_string(),
            encryption_key: hex::decode(encryption_key_hex)?,
            scope: hex::decode(scope_id_hex)?,
        })),
        LookalikeMediaRequest::PublishSegmentsDataset {
            data_room_id_hex,
            dataset_hash_hex,
            encryption_key_hex,
            scope_id_hex,
        } => Ok(gcg_request::GcgRequest::PublishDatasetToDataRoomRequest(PublishDatasetToDataRoomRequest {
            dataset_hash: hex::decode(dataset_hash_hex)?,
            data_room_id: hex::decode(data_room_id_hex)?,
            leaf_id: DATASET_SEGMENTS_ID.to_string(),
            encryption_key: hex::decode(encryption_key_hex)?,
            scope: hex::decode(scope_id_hex)?,
        })),
        LookalikeMediaRequest::RetrievePublishedDatasets { data_room_id_hex } => {
            Ok(gcg_request::GcgRequest::RetrievePublishedDatasetsRequest(RetrievePublishedDatasetsRequest {
                data_room_id: hex::decode(data_room_id_hex)?,
            }))
        }
        LookalikeMediaRequest::CalculateOverlapBasic { data_room_id_hex, scope_id_hex } => {
            Ok(gcg_request::GcgRequest::ExecuteComputeRequest(ExecuteComputeRequest {
                data_room_id: hex::decode(data_room_id_hex)?,
                compute_node_ids: vec![OVERLAP_BASIC_ID.into()],
                is_dry_run: false,
                scope: hex::decode(scope_id_hex)?,
                parameters: Default::default(),
                test_datasets: Default::default(),
            }))
        }
        LookalikeMediaRequest::ComputeAudienceSizes { data_room_id_hex, scope_id_hex } => {
            Ok(gcg_request::GcgRequest::ExecuteComputeRequest(ExecuteComputeRequest {
                data_room_id: hex::decode(data_room_id_hex)?,
                compute_node_ids: vec![COMPUTE_AUDIENCE_SIZES_ID.into()],
                is_dry_run: false,
                scope: hex::decode(scope_id_hex)?,
                parameters: Default::default(),
                test_datasets: Default::default(),
            }))
        }
        LookalikeMediaRequest::CalculateOverlapInsights { data_room_id_hex, scope_id_hex } => {
            Ok(gcg_request::GcgRequest::ExecuteComputeRequest(ExecuteComputeRequest {
                data_room_id: hex::decode(data_room_id_hex)?,
                compute_node_ids: vec![CONSENTLESS_OVERLAP_INSIGHTS_ID.into()],
                is_dry_run: false,
                scope: hex::decode(scope_id_hex)?,
                parameters: Default::default(),
                test_datasets: Default::default(),
            }))
        }
        LookalikeMediaRequest::CalculateModelledAudienceInsights { data_room_id_hex, scope_id_hex } => {
            Ok(gcg_request::GcgRequest::ExecuteComputeRequest(ExecuteComputeRequest {
                data_room_id: hex::decode(data_room_id_hex)?,
                compute_node_ids: vec![MODELLED_AUDIENCE_INSIGHTS_ID.into()],
                is_dry_run: false,
                scope: hex::decode(scope_id_hex)?,
                parameters: Default::default(),
                test_datasets: Default::default(),
            }))
        }
        LookalikeMediaRequest::CalculateModelledAudienceInsightsView { data_room_id_hex, scope_id_hex } => {
            Ok(gcg_request::GcgRequest::ExecuteComputeRequest(ExecuteComputeRequest {
                data_room_id: hex::decode(data_room_id_hex)?,
                compute_node_ids: vec![MODELLED_AUDIENCE_INSIGHTS_VIEW_ID.into()],
                is_dry_run: false,
                scope: hex::decode(scope_id_hex)?,
                parameters: Default::default(),
                test_datasets: Default::default(),
            }))
        }
        LookalikeMediaRequest::ViewPublishedActivatedAudiences { data_room_id_hex, scope_id_hex } => {
            Ok(gcg_request::GcgRequest::ExecuteComputeRequest(ExecuteComputeRequest {
                data_room_id: hex::decode(data_room_id_hex)?,
                compute_node_ids: vec![VIEW_PUBLISHED_ACTIVATED_AUDIENCES_ID.into()],
                is_dry_run: false,
                scope: hex::decode(scope_id_hex)?,
                parameters: Default::default(),
                test_datasets: Default::default(),
            }))
        }
        LookalikeMediaRequest::ViewActivatedAudiences { data_room_id_hex, scope_id_hex } => {
            Ok(gcg_request::GcgRequest::ExecuteComputeRequest(ExecuteComputeRequest {
                data_room_id: hex::decode(data_room_id_hex)?,
                compute_node_ids: vec![VIEW_ACTIVATED_AUDIENCES_ID.into()],
                is_dry_run: false,
                scope: hex::decode(scope_id_hex)?,
                parameters: Default::default(),
                test_datasets: Default::default(),
            }))
        }
        LookalikeMediaRequest::PublishActivatedAudiencesConfig {
            data_room_id_hex,
            dataset_hash_hex,
            encryption_key_hex,
            scope_id_hex,
        } => Ok(gcg_request::GcgRequest::PublishDatasetToDataRoomRequest(PublishDatasetToDataRoomRequest {
            dataset_hash: hex::decode(dataset_hash_hex)?,
            data_room_id: hex::decode(data_room_id_hex)?,
            leaf_id: ACTIVATED_AUDIENCES_CONFIG_ID.to_string(),
            encryption_key: hex::decode(encryption_key_hex)?,
            scope: hex::decode(scope_id_hex)?,
        })),
        LookalikeMediaRequest::GetLookalikeAudience { data_room_id_hex, scope_id_hex, requested_audience } => {
            Ok(gcg_request::GcgRequest::ExecuteComputeRequest(ExecuteComputeRequest {
                data_room_id: hex::decode(data_room_id_hex)?,
                compute_node_ids: vec![GET_LOOKALIKE_AUDIENCE_ID.into()],
                is_dry_run: false,
                scope: hex::decode(scope_id_hex)?,
                parameters: From::from([(
                    REQUESTED_AUDIENCE_CONFIG_ID.to_string(),
                    serde_json::to_string(&requested_audience)?,
                )]),
                test_datasets: Default::default(),
            }))
        }
        LookalikeMediaRequest::UnpublishActivatedAudiencesConfig { data_room_id_hex } => {
            Ok(gcg_request::GcgRequest::RemovePublishedDatasetRequest(RemovePublishedDatasetRequest {
                data_room_id: hex::decode(data_room_id_hex)?,
                leaf_id: ACTIVATED_AUDIENCES_CONFIG_ID.into(),
            }))
        }
        LookalikeMediaRequest::UnpublishPublisherUsersDataset { data_room_id_hex } => {
            Ok(gcg_request::GcgRequest::RemovePublishedDatasetRequest(RemovePublishedDatasetRequest {
                data_room_id: hex::decode(data_room_id_hex)?,
                leaf_id: DATASET_MATCHING_ID.into(),
            }))
        }
        LookalikeMediaRequest::UnpublishDemographicsDataset { data_room_id_hex } => {
            Ok(gcg_request::GcgRequest::RemovePublishedDatasetRequest(RemovePublishedDatasetRequest {
                data_room_id: hex::decode(data_room_id_hex)?,
                leaf_id: DATASET_DEMOGRAPHICS_ID.into(),
            }))
        }
        LookalikeMediaRequest::UnpublishEmbeddingsDataset { data_room_id_hex } => {
            Ok(gcg_request::GcgRequest::RemovePublishedDatasetRequest(RemovePublishedDatasetRequest {
                data_room_id: hex::decode(data_room_id_hex)?,
                leaf_id: DATASET_EMBEDDINGS_ID.into(),
            }))
        }
        LookalikeMediaRequest::UnpublishSegmentsDataset { data_room_id_hex } => {
            Ok(gcg_request::GcgRequest::RemovePublishedDatasetRequest(RemovePublishedDatasetRequest {
                data_room_id: hex::decode(data_room_id_hex)?,
                leaf_id: DATASET_SEGMENTS_ID.into(),
            }))
        }
        LookalikeMediaRequest::UnpublishAdvertiserDataset { data_room_id_hex } => {
            Ok(gcg_request::GcgRequest::RemovePublishedDatasetRequest(RemovePublishedDatasetRequest {
                data_room_id: hex::decode(data_room_id_hex)?,
                leaf_id: DATASET_AUDIENCES_ID.into(),
            }))
        }
        LookalikeMediaRequest::IngestAudiencesReport { data_room_id_hex, scope_id_hex } => {
            Ok(gcg_request::GcgRequest::ExecuteComputeRequest(ExecuteComputeRequest {
                data_room_id: hex::decode(data_room_id_hex)?,
                compute_node_ids: vec![INGEST_AUDIENCES_REPORT_ID.into()],
                is_dry_run: false,
                scope: hex::decode(scope_id_hex)?,
                parameters: Default::default(),
                test_datasets: Default::default(),
            }))
        }
    }
}

fn decompile_lookalike_media_response(
    media_request: &LookalikeMediaRequest,
    gcg_response: GcgResponse,
) -> Result<LookalikeMediaResponse, CompileError> {
    let gcg_response = gcg_response.gcg_response.ok_or("gcg_response not set")?;
    match media_request {
        LookalikeMediaRequest::RetrieveDataRoom { .. } => {
            if let gcg_response::GcgResponse::RetrieveDataRoomResponse(response) = gcg_response {
                let low_level_data_room = response.data_room.as_ref().ok_or("data_room not set")?;
                let high_level_serialized = response
                    .high_level_representation
                    .as_ref()
                    .ok_or("High-level representation not set in DCR, cannot interpret as Media DCR")?;
                let high_level_data_room: LookalikeMediaDataRoom = serde_json::from_slice(high_level_serialized)?;
                let low_level_data_room_recompiled = compile_lookalike_media_data_room(&high_level_data_room)?;
                if low_level_data_room != &low_level_data_room_recompiled {
                    return Err(format!("The recompiled Media DCR representation did not reproduce, verification failed\nGot:\n{:#?}\nRecompiled:\n{:#?}", low_level_data_room, low_level_data_room_recompiled))?;
                }
                return Ok(LookalikeMediaResponse::RetrieveDataRoom { data_room: high_level_data_room });
            }
        }
        LookalikeMediaRequest::PublishDataRoom { .. } => {
            if let gcg_response::GcgResponse::CreateDataRoomResponse(response) = gcg_response {
                let response =
                    response.create_data_room_response.as_ref().ok_or("create_data_room_response not set")?;
                match response {
                    create_data_room_response::CreateDataRoomResponse::DataRoomId(id) => {
                        return Ok(LookalikeMediaResponse::PublishDataRoom { data_room_id: hex::encode(id) });
                    }
                    create_data_room_response::CreateDataRoomResponse::DataRoomValidationError(error) => {
                        return Err(flatten_validation_error(error))?
                    }
                }
            }
        }
        LookalikeMediaRequest::PublishAdvertiserDataset { .. } => {
            if let gcg_response::GcgResponse::PublishDatasetToDataRoomResponse(_response) = gcg_response {
                return Ok(LookalikeMediaResponse::PublishAdvertiserDataset {});
            }
        }
        LookalikeMediaRequest::PublishPublisherUsersDataset { .. } => {
            if let gcg_response::GcgResponse::PublishDatasetToDataRoomResponse(_response) = gcg_response {
                return Ok(LookalikeMediaResponse::PublishPublisherUsersDataset {});
            }
        }
        LookalikeMediaRequest::UnpublishPublisherUsersDataset { .. } => {
            if let gcg_response::GcgResponse::RemovePublishedDatasetResponse(_response) = gcg_response {
                return Ok(LookalikeMediaResponse::UnpublishPublisherUsersDataset {});
            }
        }
        LookalikeMediaRequest::UnpublishDemographicsDataset { .. } => {
            if let gcg_response::GcgResponse::RemovePublishedDatasetResponse(_response) = gcg_response {
                return Ok(LookalikeMediaResponse::UnpublishDemographicsDataset {});
            }
        }
        LookalikeMediaRequest::UnpublishEmbeddingsDataset { .. } => {
            if let gcg_response::GcgResponse::RemovePublishedDatasetResponse(_response) = gcg_response {
                return Ok(LookalikeMediaResponse::UnpublishEmbeddingsDataset {});
            }
        }
        LookalikeMediaRequest::UnpublishSegmentsDataset { .. } => {
            if let gcg_response::GcgResponse::RemovePublishedDatasetResponse(_response) = gcg_response {
                return Ok(LookalikeMediaResponse::UnpublishSegmentsDataset {});
            }
        }
        LookalikeMediaRequest::PublishDemographicsDataset { .. } => {
            if let gcg_response::GcgResponse::PublishDatasetToDataRoomResponse(_response) = gcg_response {
                return Ok(LookalikeMediaResponse::PublishDemographicsDataset {});
            }
        }
        LookalikeMediaRequest::PublishSegmentsDataset { .. } => {
            if let gcg_response::GcgResponse::PublishDatasetToDataRoomResponse(_response) = gcg_response {
                return Ok(LookalikeMediaResponse::PublishSegmentsDataset {});
            }
        }

        LookalikeMediaRequest::PublishEmbeddingsDataset { .. } => {
            if let gcg_response::GcgResponse::PublishDatasetToDataRoomResponse(_response) = gcg_response {
                return Ok(LookalikeMediaResponse::PublishEmbeddingsDataset {});
            }
        }
        LookalikeMediaRequest::CalculateModelledAudienceInsights { .. } => {
            if let gcg_response::GcgResponse::ExecuteComputeResponse(response) = gcg_response {
                return Ok(LookalikeMediaResponse::CalculateModelledAudienceInsights {
                    compute_node_name: MODELLED_AUDIENCE_INSIGHTS_ID.into(),
                    job_id_hex: hex::encode(&response.job_id),
                });
            }
        }
        LookalikeMediaRequest::PublishActivatedAudiencesConfig { .. } => {
            if let gcg_response::GcgResponse::PublishDatasetToDataRoomResponse(_response) = gcg_response {
                return Ok(LookalikeMediaResponse::PublishActivatedAudiencesConfig {});
            }
        }
        LookalikeMediaRequest::UnpublishActivatedAudiencesConfig { .. } => {
            if let gcg_response::GcgResponse::RemovePublishedDatasetResponse(_response) = gcg_response {
                return Ok(LookalikeMediaResponse::UnpublishActivatedAudiencesConfig {});
            }
        }
        LookalikeMediaRequest::GetLookalikeAudience { .. } => {
            if let gcg_response::GcgResponse::ExecuteComputeResponse(response) = gcg_response {
                return Ok(LookalikeMediaResponse::GetLookalikeAudience {
                    compute_node_name: GET_LOOKALIKE_AUDIENCE_ID.into(),
                    job_id_hex: hex::encode(&response.job_id),
                });
            }
        }
        LookalikeMediaRequest::CalculateModelledAudienceInsightsView { .. } => {
            if let gcg_response::GcgResponse::ExecuteComputeResponse(response) = gcg_response {
                return Ok(LookalikeMediaResponse::CalculateModelledAudienceInsightsView {
                    compute_node_name: MODELLED_AUDIENCE_INSIGHTS_VIEW_ID.into(),
                    job_id_hex: hex::encode(&response.job_id),
                });
            }
        }
        LookalikeMediaRequest::ViewPublishedActivatedAudiences { .. } => {
            if let gcg_response::GcgResponse::ExecuteComputeResponse(response) = gcg_response {
                return Ok(LookalikeMediaResponse::ViewPublishedActivatedAudiences {
                    compute_node_name: VIEW_PUBLISHED_ACTIVATED_AUDIENCES_ID.into(),
                    job_id_hex: hex::encode(&response.job_id),
                });
            }
        }
        LookalikeMediaRequest::ViewActivatedAudiences { .. } => {
            if let gcg_response::GcgResponse::ExecuteComputeResponse(response) = gcg_response {
                return Ok(LookalikeMediaResponse::ViewActivatedAudiences {
                    compute_node_name: VIEW_ACTIVATED_AUDIENCES_ID.into(),
                    job_id_hex: hex::encode(&response.job_id),
                });
            }
        }
        LookalikeMediaRequest::RetrievePublishedDatasets { .. } => {
            if let gcg_response::GcgResponse::RetrievePublishedDatasetsResponse(response) = gcg_response {
                let mut advertiser_dataset_hash_hex = None;
                let mut publisher_dataset_hash_hex = None;
                let mut segments_dataset_hash_hex = None;
                let mut demographics_dataset_hash_hex = None;
                let mut embeddings_dataset_hash_hex = None;
                for dataset in response.published_datasets {
                    if dataset.leaf_id.as_str() == DATASET_AUDIENCES_ID {
                        advertiser_dataset_hash_hex = Some(hex::encode(&dataset.dataset_hash));
                    } else if dataset.leaf_id.as_str() == DATASET_MATCHING_ID {
                        publisher_dataset_hash_hex = Some(hex::encode(&dataset.dataset_hash));
                    } else if dataset.leaf_id.as_str() == DATASET_SEGMENTS_ID {
                        segments_dataset_hash_hex = Some(hex::encode(&dataset.dataset_hash));
                    } else if dataset.leaf_id.as_str() == DATASET_DEMOGRAPHICS_ID {
                        demographics_dataset_hash_hex = Some(hex::encode(&dataset.dataset_hash));
                    } else if dataset.leaf_id.as_str() == DATASET_EMBEDDINGS_ID {
                        embeddings_dataset_hash_hex = Some(hex::encode(&dataset.dataset_hash));
                    }
                }
                return Ok(LookalikeMediaResponse::RetrievePublishedDatasets {
                    advertiser_dataset_hash_hex,
                    publisher_dataset_hash_hex,
                    demographics_dataset_hash_hex,
                    segments_dataset_hash_hex,
                    embeddings_dataset_hash_hex,
                });
            }
        }
        LookalikeMediaRequest::CalculateOverlapBasic { .. } => {
            if let gcg_response::GcgResponse::ExecuteComputeResponse(response) = gcg_response {
                return Ok(LookalikeMediaResponse::CalculateOverlapBasic {
                    compute_node_name: OVERLAP_BASIC_ID.into(),
                    job_id_hex: hex::encode(&response.job_id),
                });
            }
        }
        LookalikeMediaRequest::ComputeAudienceSizes { .. } => {
            if let gcg_response::GcgResponse::ExecuteComputeResponse(response) = gcg_response {
                return Ok(LookalikeMediaResponse::ComputeAudienceSizes {
                    compute_node_name: COMPUTE_AUDIENCE_SIZES_ID.into(),
                    job_id_hex: hex::encode(&response.job_id),
                });
            }
        }
        LookalikeMediaRequest::CalculateOverlapInsights { .. } => {
            if let gcg_response::GcgResponse::ExecuteComputeResponse(response) = gcg_response {
                return Ok(LookalikeMediaResponse::CalculateOverlapInsights {
                    compute_node_name: CONSENTLESS_OVERLAP_INSIGHTS_ID.into(),
                    job_id_hex: hex::encode(&response.job_id),
                });
            }
        }
        LookalikeMediaRequest::UnpublishAdvertiserDataset { .. } => {
            if let gcg_response::GcgResponse::RemovePublishedDatasetResponse(_response) = gcg_response {
                return Ok(LookalikeMediaResponse::UnpublishAdvertiserDataset {});
            }
        }
        LookalikeMediaRequest::IngestAudiencesReport { .. } => {
            if let gcg_response::GcgResponse::ExecuteComputeResponse(response) = gcg_response {
                return Ok(LookalikeMediaResponse::IngestAudiencesReport {
                    compute_node_name: INGEST_AUDIENCES_REPORT_ID.into(),
                    job_id_hex: hex::encode(&response.job_id),
                });
            }
        }
    }
    // No match, perhaps it's a failure
    if let gcg_response::GcgResponse::Failure(response) = gcg_response {
        return Err(response.as_str())?;
    }
    return Err("Unexpected GcgResponse, cannot decompile as MediaResponse")?;
}

fn flatten_validation_error(error: &DataRoomValidationError) -> String {
    let mut message = error.message.clone();
    fn add_field(message: &mut String, field_name: &str, field: &Option<impl std::fmt::Display>) {
        if let Some(value) = field {
            message.push_str(format!(", {}: {}", field_name, value).as_str());
        }
    }

    add_field(&mut message, "compute_node_id", &error.compute_node_id);
    add_field(&mut message, "user_permission_id", &error.user_permission_id);
    add_field(&mut message, "permission_index", &error.permission_index);
    add_field(&mut message, "attestation_specification_id", &error.attestation_specification_id);
    add_field(&mut message, "authentication_method_iid", &error.authentication_method_id);

    message
}

pub fn get_lookalike_media_data_room_features_serialized(json: &str) -> Result<Vec<String>, CompileError> {
    let dcr: LookalikeMediaDataRoom = serde_json::from_str(json)?;
    Ok(dcr.get_features())
}

pub fn get_lookalike_media_data_room_consumed_datasets_serialized(json: &str) -> Result<String, CompileError> {
    let dcr: LookalikeMediaDataRoom = serde_json::from_str(json)?;
    let consumed_datasets = dcr.get_consumed_datasets()?;
    Ok(serde_json::to_string(&consumed_datasets)?)
}

pub fn convert_lookalike_media_data_room_any_to_latest_serialized(
    media_data_room_versioned_serialized: &str,
) -> CompileResult<String> {
    let data_room: LookalikeMediaDataRoom = serde_json::from_str(media_data_room_versioned_serialized)?;
    Ok(serde_json::to_string(&convert_lookalike_media_data_room_any_to_latest(data_room)?)?)
}

fn convert_lookalike_media_data_room_any_to_latest(
    data_room: LookalikeMediaDataRoom,
) -> CompileResult<LookalikeMediaDataRoomLatest> {
    enum OldOrLatest {
        Old(LookalikeMediaDataRoom),
        Latest(LookalikeMediaDataRoomLatest),
    }
    fn convert_any_to_next(data_room: LookalikeMediaDataRoom) -> CompileResult<OldOrLatest> {
        match data_room {
            LookalikeMediaDataRoom::V0(data_room) => Ok(OldOrLatest::Old(data_room.upgrade())),
            LookalikeMediaDataRoom::V1(data_room) => Ok(OldOrLatest::Old(data_room.upgrade())),
            LookalikeMediaDataRoom::V2(data_room) => Ok(OldOrLatest::Old(data_room.try_upgrade()?)),
            LookalikeMediaDataRoom::V3(data_room) => match data_room.compute {
                LookalikeMediaDcrComputeOrUnknown::Known(compute) => match compute {
                    LookalikeMediaDcrCompute::V0(compute) => Ok(OldOrLatest::Latest(compute)),
                },
                LookalikeMediaDcrComputeOrUnknown::Unknown => {
                    Err("Cannot convert an unknown compute payload to a next version".into())
                }
            },
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

#[cfg(test)]
mod tests {
    use crate::lookalike_media::v3::LookalikeMediaDcrComputeOrUnknown;
    use crate::lookalike_media::LookalikeMediaDataRoom;

    #[test]
    fn check_forwards_compatibility_when_parsing_lm_dcrs() {
        let dcr: LookalikeMediaDataRoom = serde_json::from_str(
            r#"
            {
                "v4": {
                    "features": ["hello"],
                    "consumes": {
                        "optional": [
                            {
                                "name": "hello1",
                                "type": "DATASET"
                            }
                        ],
                        "required": [
                            {
                                "name": "hello2",
                                "type": "DATASET"
                            }
                        ]
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

        assert!(!dcr.get_features().is_empty());
        assert!(!dcr.get_requirements().unwrap().optional.is_empty());
        assert!(!dcr.get_requirements().unwrap().required.is_empty());
        match dcr {
            LookalikeMediaDataRoom::V3(dcr) => match dcr.compute {
                LookalikeMediaDcrComputeOrUnknown::Known(_) => {
                    panic!("Compute should be unknown");
                }
                LookalikeMediaDcrComputeOrUnknown::Unknown => {}
            },
            _ => {
                panic!("Unknown DCR version");
            }
        }
    }
}
