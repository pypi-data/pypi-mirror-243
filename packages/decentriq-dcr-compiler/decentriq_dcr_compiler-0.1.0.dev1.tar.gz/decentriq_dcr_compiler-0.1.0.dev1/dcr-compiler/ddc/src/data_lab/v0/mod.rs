use delta_attestation_api::*;
use delta_container_worker_api::*;
use delta_data_room_api::*;
use delta_gcg_driver_api::*;
use format_types::v0::FormatType;
use format_types::v0::HashingAlgorithm;
use schemars::JsonSchema;
use serde::Deserialize;
use serde::Serialize;
use validation_config::v0::ColumnTuple;
use validation_config::v0::ColumnValidationV0;
use validation_config::v0::TableValidationV0;
use validation_config::v0::UniquenessValidationRule;
use validation_config::v0::ValidationConfigV0;
use validation_config::ValidationConfig;

use crate::data_lab::provides::DEMOGRAPHICS_DATA;
use crate::data_lab::provides::EMBEDDINGS_DATA;
use crate::data_lab::DATASET_DEMOGRAPHICS_ID;
use crate::data_lab::DATASET_EMBEDDINGS_ID;
use crate::data_lab::DATASET_SEGMENTS_ID;
use crate::data_lab::DATASET_USERS_ID;
use crate::data_lab::PUBLISHER_DATA_STATISTICS_ID;
use crate::feature::RequirementFlag;
use crate::feature::Requirements;
use crate::media::v1::EnclaveSpecificationV1;
use crate::*;

pub const PUBLISHER_DATA_STATISTICS_PY: &[u8] = include_bytes!("./publisher_data_statistics.py");

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct PublisherDatasetColumnV0 {
    format_type: Option<FormatType>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DataLabDatasetConfigV0 {
    pub(crate) path: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DataLabConfigV0 {
    pub dataset_users: DataLabDatasetConfigV0,
    pub dataset_segments: DataLabDatasetConfigV0,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub dataset_demographics: Option<DataLabDatasetConfigV0>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub dataset_embeddings: Option<DataLabDatasetConfigV0>,
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct DataLabComputeV0 {
    pub id: String,
    pub name: String,
    pub publisher_email: String,

    pub num_embeddings: usize,

    pub matching_id_format: FormatType,
    pub matching_id_hashing_algorithm: Option<HashingAlgorithm>,

    pub authentication_root_certificate_pem: String,
    pub driver_enclave_specification: EnclaveSpecificationV1,
    pub python_enclave_specification: EnclaveSpecificationV1,
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct CreateDataLabComputeV0 {
    pub id: String,
    pub name: String,
    pub publisher_email: String,

    pub has_demographics: bool,
    pub has_embeddings: bool,
    pub num_embeddings: usize,

    pub matching_id_format: FormatType,
    pub matching_id_hashing_algorithm: Option<HashingAlgorithm>,

    pub authentication_root_certificate_pem: String,
    pub driver_enclave_specification: EnclaveSpecificationV1,
    pub python_enclave_specification: EnclaveSpecificationV1,
}

struct DatLabComputeCompilerV0<'a> {
    data_room: &'a DataLabComputeV0,
    driver_attestation_specification_id: String,
    python_attestation_specification_id: String,
    driver_protocol_version: u32,
    python_protocol_version: u32,
    permissions_publisher: Vec<Permission>,
    configuration_elements: Vec<ConfigurationElement>,
    features: HashSet<&'a String>,
    requirements: &'a Requirements,
}

pub fn compile_compute<'a>(
    data_room: &'a DataLabComputeV0,
    features: HashSet<&'a String>,
    requirements: &'a Requirements,
) -> Result<DataRoom, CompileError> {
    DatLabComputeCompilerV0::new(data_room, features, requirements).compile()
}

fn data_room_to_data_room_config(has_demographics: bool, has_embeddings: bool) -> CompileResult<DataLabConfigV0> {
    Ok(DataLabConfigV0 {
        dataset_users: DataLabDatasetConfigV0 { path: "/input/dataset_users".to_string() },
        dataset_segments: DataLabDatasetConfigV0 { path: "/input/dataset_segments".to_string() },
        dataset_demographics: if has_demographics {
            Some(DataLabDatasetConfigV0 { path: "/input/dataset_demographics".to_string() })
        } else {
            None
        },
        dataset_embeddings: if has_embeddings {
            Some(DataLabDatasetConfigV0 { path: "/input/dataset_embeddings".to_string() })
        } else {
            None
        },
    })
}

impl<'a> DatLabComputeCompilerV0<'a> {
    pub fn has_demographics(&self) -> bool {
        self.requirements.contains_all(&RequirementFlag::from_dataset(DEMOGRAPHICS_DATA))
    }

    pub fn has_embeddings(&self) -> bool {
        self.requirements.contains_all(&RequirementFlag::from_dataset(EMBEDDINGS_DATA))
    }

    pub fn new(data_room: &'a DataLabComputeV0, features: HashSet<&'a String>, requirements: &'a Requirements) -> Self {
        let driver_attestation_specification_id =
            format!("attestation_specification-{}", data_room.driver_enclave_specification.id);
        let python_attestation_specification_id =
            format!("attestation_specification-{}", data_room.python_enclave_specification.id);
        Self {
            data_room,
            driver_attestation_specification_id,
            python_attestation_specification_id,
            driver_protocol_version: data_room.driver_enclave_specification.worker_protocol,
            python_protocol_version: data_room.python_enclave_specification.worker_protocol,
            permissions_publisher: vec![],
            configuration_elements: vec![],
            features,
            requirements,
        }
    }

    pub fn compile(mut self) -> CompileResult<DataRoom> {
        self.add_common_nodes()?;

        let publisher_email = &self.data_room.publisher_email;
        self.configuration_elements.push(ConfigurationElement {
            id: format!("permission_publisher_{}", publisher_email),
            element: Some(configuration_element::Element::UserPermission(UserPermission {
                email: publisher_email.clone(),
                permissions: self.permissions_publisher.iter().cloned().collect(),
                authentication_method_id: "authentication_method".into(),
            })),
        });

        let low_level_data_room = DataRoom {
            id: self.data_room.id.clone(),
            name: self.data_room.name.clone(),
            description: self.data_room.name.clone(),
            governance_protocol: Some(GovernanceProtocol {
                policy: Some(governance_protocol::Policy::StaticDataRoomPolicy(StaticDataRoomPolicy {})),
            }),
            initial_configuration: Some(DataRoomConfiguration { elements: self.configuration_elements }),
        };

        Ok(low_level_data_room)
    }

    fn add_permissions(&mut self, permissions: Vec<permission::Permission>) {
        for permission in permissions {
            self.permissions_publisher.push(Permission { permission: Some(permission) })
        }
    }

    fn add_common_nodes(&mut self) -> CompileResult<()> {
        for (enclave_specification, attestation_specification_id) in &[
            (&self.data_room.driver_enclave_specification, &self.driver_attestation_specification_id),
            (&self.data_room.python_enclave_specification, &self.python_attestation_specification_id),
        ] {
            let attestation_specification: AttestationSpecification = prost::Message::decode_length_delimited(
                base64::decode(&enclave_specification.attestation_proto_base64)
                    .map_err(|err| CompileError(format!("Failed to decode attestation specification: {}", err)))?
                    .as_slice(),
            )?;
            self.configuration_elements.push(ConfigurationElement {
                id: attestation_specification_id.to_string(),
                element: Some(configuration_element::Element::AttestationSpecification(attestation_specification)),
            });
        }

        let mut added_datasets = vec![];

        for dataset_info in [
            Some((
                DATASET_USERS_ID,
                users_validation_config(
                    &self.data_room.matching_id_format,
                    self.data_room.matching_id_hashing_algorithm.as_ref(),
                ),
            )),
            Some((DATASET_SEGMENTS_ID, segments_validation_config())),
            (if self.has_demographics() {
                Some((DATASET_DEMOGRAPHICS_ID, demographics_validation_config()))
            } else {
                None
            }),
            (if self.has_embeddings() {
                Some((DATASET_EMBEDDINGS_ID, embeddings_validation_config(self.data_room.num_embeddings)))
            } else {
                None
            }),
        ] {
            if let Some((dataset_name, validation_config)) = dataset_info {
                self.configuration_elements.push(ConfigurationElement {
                    id: dataset_name.into(),
                    element: Some(configuration_element::Element::ComputeNode(ComputeNode {
                        node_name: dataset_name.into(),
                        rate_limiting: None,
                        node: Some(compute_node::Node::Leaf(ComputeNodeLeaf { is_required: true })),
                    })),
                });
                crate::validation::v2::add_nodes_for_validation(
                    &mut self.configuration_elements, dataset_name, dataset_name, &validation_config?,
                    &self.driver_attestation_specification_id,
                    self.data_room.driver_enclave_specification.worker_protocol,
                    &self.python_attestation_specification_id,
                    self.data_room.python_enclave_specification.worker_protocol,
                )?;
                added_datasets.push(dataset_name);
                self.add_permissions(vec![
                    P::leaf_crud(dataset_name),
                    P::execute_compute(dataset_name),
                    P::execute_compute(&validation::v2::get_validation_check_id(dataset_name)),
                    P::retrieve_compute_result(&validation::v2::get_validation_check_id(dataset_name)),
                    P::execute_compute(&validation::v2::get_validation_report_id(dataset_name)),
                    P::retrieve_compute_result(&validation::v2::get_validation_report_id(dataset_name)),
                ])
            }
        }

        self.configuration_elements.push(ConfigurationElement {
            id: "publisher_data_statistics_script".into(),
            element: Some(configuration_element::Element::ComputeNode(ComputeNode {
                node_name: "publisher_data_statistics_script".into(),
                rate_limiting: None,
                node: Some(compute_node::Node::Branch(ComputeNodeBranch {
                    config: prost::Message::encode_length_delimited_to_vec(&DriverTaskConfig {
                        driver_task_config: Some(driver_task_config::DriverTaskConfig::StaticContent(
                            StaticContentConfig { content: PUBLISHER_DATA_STATISTICS_PY.to_vec() },
                        )),
                    }),
                    dependencies: vec![],
                    output_format: ComputeNodeFormat::Raw as i32,
                    protocol: Some(ComputeNodeProtocol { version: self.driver_protocol_version }),
                    attestation_specification_id: self.driver_attestation_specification_id.clone(),
                })),
            })),
        });
        let config = data_room_to_data_room_config(self.has_demographics(), self.has_embeddings())?;
        self.configuration_elements.push(ConfigurationElement {
            id: "data_lab_config".into(),
            element: Some(configuration_element::Element::ComputeNode(ComputeNode {
                node_name: "data_lab_config".into(),
                rate_limiting: None,
                node: Some(compute_node::Node::Branch(ComputeNodeBranch {
                    config: prost::Message::encode_length_delimited_to_vec(&DriverTaskConfig {
                        driver_task_config: Some(driver_task_config::DriverTaskConfig::StaticContent(
                            StaticContentConfig { content: serde_json::to_vec(&config)? },
                        )),
                    }),
                    dependencies: vec![],
                    output_format: ComputeNodeFormat::Raw as i32,
                    protocol: Some(ComputeNodeProtocol { version: self.driver_protocol_version }),
                    attestation_specification_id: self.driver_attestation_specification_id.clone(),
                })),
            })),
        });

        let dataset_mount_points: Vec<_> = added_datasets
            .iter()
            .map(|dataset_name| MountPoint {
                path: dataset_name.to_string(),
                dependency: validation::v2::get_validation_id(dataset_name),
            })
            .collect();
        let dataset_mount_point_dependencies: Vec<String> =
            dataset_mount_points.iter().map(|mp| mp.dependency.clone()).collect();

        self.configuration_elements.push(ConfigurationElement {
            id: PUBLISHER_DATA_STATISTICS_ID.into(),
            element: Some(configuration_element::Element::ComputeNode(ComputeNode {
                node_name: PUBLISHER_DATA_STATISTICS_ID.into(),
                rate_limiting: None,
                node: Some(compute_node::Node::Branch(ComputeNodeBranch {
                    config: prost::Message::encode_length_delimited_to_vec(&ContainerWorkerConfiguration {
                        configuration: Some(container_worker_configuration::Configuration::Static(StaticImage {
                            command: ["python3", "/input/publisher_data_statistics.py"]
                                .iter()
                                .map(|s| s.to_string())
                                .collect::<Vec<_>>(),
                            mount_points: vec![
                                MountPoint {
                                    path: "publisher_data_statistics.py".into(),
                                    dependency: "publisher_data_statistics_script".into(),
                                },
                                MountPoint { path: "datalab_config.json".into(), dependency: "data_lab_config".into() },
                            ]
                            .into_iter()
                            .chain(dataset_mount_points.into_iter())
                            .collect(),
                            output_path: "/output".into(),
                            include_container_logs_on_error: true,
                            include_container_logs_on_success: true,
                            minimum_container_memory_size: None,
                            extra_chunk_cache_size_to_available_memory_ratio: None,
                        })),
                    }),
                    dependencies: vec!["data_lab_config".into(), "publisher_data_statistics_script".into()]
                        .into_iter()
                        .chain(dataset_mount_point_dependencies.into_iter())
                        .chain(
                            added_datasets
                                .into_iter()
                                .map(|dataset_name| validation::v2::get_validation_check_id(dataset_name)),
                        )
                        .collect(),
                    output_format: ComputeNodeFormat::Zip as i32,
                    protocol: Some(ComputeNodeProtocol { version: self.python_protocol_version }),
                    attestation_specification_id: self.python_attestation_specification_id.clone(),
                })),
            })),
        });

        // Compute-specific permissions
        self.add_permissions(vec![
            P::execute_compute(PUBLISHER_DATA_STATISTICS_ID),
            P::retrieve_compute_result(PUBLISHER_DATA_STATISTICS_ID),
        ]);

        // DCR-wide permissions
        self.add_permissions(vec![P::update_data_room_status(), P::retrieve_data_room(), P::retrieve_audit_log()]);

        self.configuration_elements.push(ConfigurationElement {
            id: "authentication_method".into(),
            element: Some(configuration_element::Element::AuthenticationMethod(AuthenticationMethod {
                personal_pki: None,
                dq_pki: Some(PkiPolicy {
                    root_certificate_pem: self.data_room.authentication_root_certificate_pem.as_bytes().to_vec(),
                }),
                dcr_secret: None,
            })),
        });

        Ok(())
    }
}

/// Construct a uniqueness validation rule that enforces that the tuples (user_id, segment) are unique.
pub fn segments_validation_config() -> CompileResult<ValidationConfig> {
    let uniqueness_constraint = UniquenessValidationRule { unique_keys: vec![ColumnTuple { columns: vec![0, 1] }] };
    let validation_columns = vec![
        ColumnValidationV0 {
            name: Some("user_id".to_string()),
            format_type: FormatType::String,
            allow_null: false,
            hash_with: None,
            in_range: None,
        },
        ColumnValidationV0 {
            name: Some("segment".to_string()),
            format_type: FormatType::String,
            allow_null: false,
            hash_with: None,
            in_range: None,
        },
    ];
    let config = ValidationConfig::V0(ValidationConfigV0 {
        columns: validation_columns,
        table: Some(TableValidationV0 { uniqueness: Some(uniqueness_constraint), allow_empty: None, num_rows: None }),
    });
    Ok(config)
}

/// Construct a uniqueness validation rule that enforces that both matching_id and user_id are unique.
pub fn users_validation_config(
    matching_id_format_type: &FormatType,
    matching_id_hashing_algorithm: Option<&HashingAlgorithm>,
) -> CompileResult<ValidationConfig> {
    let matching_id_format_type = if let Some(hashing_algorithm) = matching_id_hashing_algorithm {
        match hashing_algorithm {
            HashingAlgorithm::Sha256Hex => FormatType::HashSha256Hex,
        }
    } else {
        matching_id_format_type.clone()
    };
    let uniqueness_constraint = UniquenessValidationRule {
        unique_keys: vec![ColumnTuple { columns: vec![0] }, ColumnTuple { columns: vec![1] }],
    };

    let validation_columns = vec![
        ColumnValidationV0 {
            name: Some("user_id".to_string()),
            format_type: FormatType::String,
            allow_null: false,
            hash_with: None,
            in_range: None,
        },
        ColumnValidationV0 {
            name: Some("matching_id".to_string()),
            format_type: matching_id_format_type,
            allow_null: false,
            hash_with: None,
            in_range: None,
        },
    ];
    let config = ValidationConfig::V0(ValidationConfigV0 {
        columns: validation_columns,
        table: Some(TableValidationV0 { uniqueness: Some(uniqueness_constraint), allow_empty: None, num_rows: None }),
    });
    Ok(config)
}

pub fn demographics_validation_config() -> CompileResult<ValidationConfig> {
    let uniqueness_constraint = UniquenessValidationRule { unique_keys: vec![ColumnTuple { columns: vec![0] }] };
    let validation_columns = vec![
        ColumnValidationV0 {
            name: Some("user_id".to_string()),
            format_type: FormatType::String,
            allow_null: false,
            hash_with: None,
            in_range: None,
        },
        ColumnValidationV0 {
            name: Some("age".to_string()),
            format_type: FormatType::String,
            allow_null: true,
            hash_with: None,
            in_range: None,
        },
        ColumnValidationV0 {
            name: Some("gender".to_string()),
            format_type: FormatType::String,
            allow_null: true,
            hash_with: None,
            in_range: None,
        },
    ];
    let config = ValidationConfig::V0(ValidationConfigV0 {
        columns: validation_columns,
        table: Some(TableValidationV0 { uniqueness: Some(uniqueness_constraint), allow_empty: None, num_rows: None }),
    });
    Ok(config)
}

pub fn embeddings_validation_config(num_embeddings: usize) -> CompileResult<ValidationConfig> {
    let uniqueness_constraint = UniquenessValidationRule { unique_keys: vec![ColumnTuple { columns: vec![0, 1] }] };
    let mut validation_columns = vec![
        ColumnValidationV0 {
            name: Some("user_id".to_string()),
            format_type: FormatType::String,
            allow_null: false,
            hash_with: None,
            in_range: None,
        },
        ColumnValidationV0 {
            name: Some("scope".to_string()),
            format_type: FormatType::String,
            allow_null: true,
            hash_with: None,
            in_range: None,
        },
    ];
    let mut ix = 0;
    while ix < num_embeddings {
        validation_columns.push(ColumnValidationV0 {
            name: Some(format!("e{}", ix)),
            format_type: FormatType::Float,
            allow_null: true,
            hash_with: None,
            in_range: None,
        });
        ix += 1;
    }
    let config = ValidationConfig::V0(ValidationConfigV0 {
        columns: validation_columns,
        table: Some(TableValidationV0 { uniqueness: Some(uniqueness_constraint), allow_empty: None, num_rows: None }),
    });
    Ok(config)
}

struct P;

#[allow(dead_code)]
impl P {
    fn execute_compute(node: &str) -> permission::Permission {
        permission::Permission::ExecuteComputePermission(ExecuteComputePermission { compute_node_id: node.into() })
    }

    fn retrieve_compute_result(node: &str) -> permission::Permission {
        permission::Permission::RetrieveComputeResultPermission(RetrieveComputeResultPermission {
            compute_node_id: node.into(),
        })
    }

    fn retrieve_data_room() -> permission::Permission {
        permission::Permission::RetrieveDataRoomPermission(RetrieveDataRoomPermission {})
    }

    fn retrieve_published_datasets() -> permission::Permission {
        permission::Permission::RetrievePublishedDatasetsPermission(RetrievePublishedDatasetsPermission {})
    }

    fn leaf_crud(node: &str) -> permission::Permission {
        permission::Permission::LeafCrudPermission(LeafCrudPermission { leaf_node_id: node.into() })
    }

    fn update_data_room_status() -> permission::Permission {
        permission::Permission::UpdateDataRoomStatusPermission(UpdateDataRoomStatusPermission {})
    }

    fn retrieve_audit_log() -> permission::Permission {
        permission::Permission::RetrieveAuditLogPermission(RetrieveAuditLogPermission {})
    }

    fn cas_auxiliary_state() -> permission::Permission {
        permission::Permission::CasAuxiliaryStatePermission(CasAuxiliaryStatePermission {})
    }

    fn read_auxiliary_state() -> permission::Permission {
        permission::Permission::ReadAuxiliaryStatePermission(ReadAuxiliaryStatePermission {})
    }

    fn execute_dev_compute() -> permission::Permission {
        permission::Permission::ExecuteDevelopmentComputePermission(ExecuteDevelopmentComputePermission {})
    }
}
