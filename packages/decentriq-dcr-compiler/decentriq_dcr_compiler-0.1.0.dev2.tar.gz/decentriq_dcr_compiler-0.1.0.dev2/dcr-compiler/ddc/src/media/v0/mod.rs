use std::iter::FromIterator;

use delta_attestation_api::*;
use delta_container_worker_api::*;
use delta_data_room_api::*;
use delta_gcg_driver_api::*;
use schemars::JsonSchema;
use serde::Deserialize;
use serde::Serialize;

use crate::CompileError;
use crate::CompileResult;
use crate::Set;

pub const OVERLAP_BASIC_ID: &str = "overlap_basic";
pub const OVERLAP_INSIGHTS_ID: &str = "consentless_overlap_insights";

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct MediaDataRoomV0 {
    pub id: String,
    pub name: String,
    pub publisher_email: String,
    pub advertiser_email: String,
    pub observer_user: Option<String>,

    pub publisher_schema: Vec<ColumnType>,
    pub advertiser_schema: Vec<ColumnType>,

    pub activation_type: Option<ActivationType>,
    pub enable_download_by_publisher: bool,
    pub enable_download_by_advertiser: bool,
    pub enable_overlap_insights: bool,

    pub authentication_root_certificate_pem: String,
    pub driver_enclave_specification: EnclaveSpecification,
    pub python_enclave_specification: EnclaveSpecification,

    // Configuration of rounding to specified decimals for privacy

    // round(decimals=1, 12.34) = 12.3
    // round(decimals=0, 12.34) = 12.0
    // round(decimals=-1, 12.34) = 10.0
    // round(decimals=1, 98.76) = 98.8
    // round(decimals=0, 98.76) = 99.0
    // round(decimals=-1, 98.76) = 100.0
    // Applies to count-like numbers, should be negative
    rounding_decimals_count: i64,
    // Applies to ratio-like numbers (0.0-1.0), should be positive
    rounding_decimals_ratio: i64,

    // Configuration of cutoffs for groups of too small size

    // Segment will not be considered for basic statistics like segment count
    cutoff_overlap_basic_segment: u64,
    // Audience type will not be considered in the propensity calculations (skeleton)
    cutoff_consentless_overlap_insights_unmatched_audience_type: u64,
    // Segment will not be considered in the propensity calculations (base propensity)
    cutoff_consentless_overlap_insights_unmatched_segment: u64,
    // Overlapped audience type will not be considered in the propensity calculations (overlap propensity)
    cutoff_consentless_overlap_insights_matched_audience_type: u64,
    // Overlapped segment will not be considered in the propensity calculations (overlap propensity)
    cutoff_consentless_overlap_insights_matched_segment_audience_type: u64,
}

// We split the audience definition into two, depending on which parts are modifiable by which
// participant. Each contributes some fields, and this we combine in a uniform way through the
// corresponding MediaRequest.
#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub enum MediaAuxiliaryActivationState {
    #[serde(rename_all = "camelCase")]
    ConsentlessAdvertiser {
        audiences: Vec<ConsentlessAdvertiserAudience>,
    },
    #[serde(rename_all = "camelCase")]
    ConsentlessPublisher {
        audiences: Vec<ConsentlessPublisherAudience>,
    },
    #[serde(rename_all = "camelCase")]
    DirectAdvertiser {
        audiences: Vec<DirectAdvertiserAudience>,
    },
    DirectPublisher {
        audiences: Vec<DirectPublisherAudience>,
    },
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct MediaAuxiliaryStateV0 {
    // The pin provides a way to detect stale state in case the base datasets have been updated.
    pin: MediaDatasetPin,
    activation_state: MediaAuxiliaryActivationState,
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct MediaDatasetPin {
    dataset_publisher_hash_hex: String,
    dataset_advertiser_hash_hex: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct ConsentlessAdvertiserAudience {
    pub id: String,
    pub audience_type: String,
    pub precision: f64,
    pub activated: bool,
    pub downloaded: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct ConsentlessPublisherAudience {
    pub id: String,
    pub downloaded: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct DirectPublisherAudience {
    pub audience_type: String,
    pub downloaded: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct DirectAdvertiserAudience {
    pub audience_type: String,
    pub downloaded: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct EnclaveSpecification {
    pub id: String,
    pub attestation_proto_base64: String,
    pub worker_protocol: u32,
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub enum ColumnType {
    ActivationId,
    MatchingId(String),
    AudienceType,
    Segment,
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub enum ActivationType {
    Consentless,
    Direct,
}

// Static configuration of the data room generally used in all compute nodes.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MediaDataRoomConfig {
    pub advertiser_column_names: Vec<String>,
    pub publisher_column_names: Vec<String>,
    pub matching_columns: Vec<String>,
    pub audience_type_column_name: Option<String>,
    pub segment_column_name: Option<String>,
    pub activation_id_column_name: Option<String>,

    pub rounding_decimals_count: i64,
    pub rounding_decimals_ratio: i64,
    pub cutoff_overlap_basic_segment: u64,
    pub cutoff_consentless_overlap_insights_unmatched_audience_type: u64,
    pub cutoff_consentless_overlap_insights_unmatched_segment: u64,
    pub cutoff_consentless_overlap_insights_matched_audience_type: u64,
    pub cutoff_consentless_overlap_insights_matched_segment_audience_type: u64,
}

// Dynamic configuration of direct activation audiences, controlled by the advertiser. Note that
// controlling of this configuration does not mean having access to the resulting audiences, that's
// controlled separately by enable_download_by_advertiser.
#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct DirectActivationConfigV0 {
    pub audience_types: Vec<String>,
}

impl MediaDataRoomConfig {
    fn from_data_room(data_room: &MediaDataRoomV0) -> Result<Self, CompileError> {
        let mut publisher_column_names = vec![];
        let mut segment_column_name = None;
        let mut activation_id_column_name = None;
        for column in &data_room.publisher_schema {
            let column_name = match column {
                ColumnType::MatchingId(name) => format!("m:{}", name),
                ColumnType::AudienceType => return Err("AudienceType column not expected in publisher schema")?,
                ColumnType::ActivationId => {
                    if activation_id_column_name.is_some() {
                        return Err("Multiple Activation ID columns in publisher schema")?;
                    }
                    let column_name = "i:activation_id".to_string();
                    activation_id_column_name = Some(column_name.clone());
                    column_name
                }
                ColumnType::Segment => {
                    if segment_column_name.is_some() {
                        return Err("Multiple Segment columns in publisher schema")?;
                    }
                    let column_name = "s:segment".to_string();
                    segment_column_name = Some(column_name.clone());
                    column_name
                }
            };
            publisher_column_names.push(column_name);
        }
        let mut audience_type_column_name = None;
        let mut advertiser_column_names = vec![];
        for column in &data_room.advertiser_schema {
            let column_name = match column {
                ColumnType::MatchingId(name) => format!("m:{}", name),
                ColumnType::AudienceType => {
                    if audience_type_column_name.is_some() {
                        return Err("Multiple AudienceType columns in advertiser schema")?;
                    }
                    let column_name = "a:audience_type".to_string();
                    audience_type_column_name = Some(column_name.clone());
                    column_name
                }
                ColumnType::Segment => return Err("Segment column not expected in advertiser schema")?,
                ColumnType::ActivationId => return Err("ActivationId column not expected in advertiser schema")?,
            };
            advertiser_column_names.push(column_name);
        }
        let matching_columns = Set::from_iter(advertiser_column_names.iter())
            .intersection(&Set::from_iter(publisher_column_names.iter()))
            .map(|name| (**name).clone())
            .collect::<Vec<_>>();
        if matching_columns.len() == 0 {
            return Err(format!(
                "The advertiser schema ({:?}) does not have common matching columns with the publisher schema ({:?})",
                data_room.publisher_schema, data_room.advertiser_schema,
            ))?;
        }

        if audience_type_column_name.is_none() && !data_room.activation_type.is_none() {
            return Err(format!(
                "No AudienceType column found in advertiser schema, even though activation type is {:?}",
                data_room.activation_type
            ))?;
        }

        Ok(MediaDataRoomConfig {
            advertiser_column_names,
            publisher_column_names,
            matching_columns,
            audience_type_column_name,
            segment_column_name,
            activation_id_column_name,
            rounding_decimals_count: data_room.rounding_decimals_count,
            rounding_decimals_ratio: data_room.rounding_decimals_ratio,
            cutoff_overlap_basic_segment: data_room.cutoff_overlap_basic_segment,
            cutoff_consentless_overlap_insights_unmatched_audience_type: data_room
                .cutoff_consentless_overlap_insights_unmatched_audience_type,
            cutoff_consentless_overlap_insights_unmatched_segment: data_room
                .cutoff_consentless_overlap_insights_unmatched_segment,
            cutoff_consentless_overlap_insights_matched_audience_type: data_room
                .cutoff_consentless_overlap_insights_matched_audience_type,
            cutoff_consentless_overlap_insights_matched_segment_audience_type: data_room
                .cutoff_consentless_overlap_insights_matched_segment_audience_type,
        })
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CalculateOverlapInsightsParams {
    pub audience_types: Vec<String>,
}

/// Configuration elements:
/// * attestation_specification-XXX
/// * dataset_advertiser
/// * dataset_publisher
/// * media_data_room_config
/// * overlap_basic_script
/// * overlap_basic
/// * authentication_method
/// * permission_advertiser
/// * permission_publisher
///
/// * overlap_insights_script
/// * overlap_insights_params
/// * consentless_overlap_insights
///
/// * direct_activation_all_script
/// * direct_activation_all
/// * direct_activation_script
/// * direct_activation
/// * direct_activation_config
pub fn compile_media_data_room_v0(data_room: &MediaDataRoomV0) -> Result<DataRoom, CompileError> {
    MediaDataRoomCompiler::new(data_room).compile()
}

struct MediaDataRoomCompiler<'a> {
    data_room: &'a MediaDataRoomV0,
    driver_attestation_specification_id: String,
    python_attestation_specification_id: String,
    driver_protocol_version: u32,
    python_protocol_version: u32,
    configuration_elements: Vec<ConfigurationElement>,
    permissions_advertiser: Vec<permission::Permission>,
    permissions_publisher: Vec<permission::Permission>,
    permissions_observer: Vec<permission::Permission>,
}

impl<'a> MediaDataRoomCompiler<'a> {
    pub fn new(data_room: &'a MediaDataRoomV0) -> Self {
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
            configuration_elements: vec![],
            permissions_advertiser: vec![],
            permissions_publisher: vec![],
            permissions_observer: vec![],
        }
    }

    pub fn compile(mut self) -> CompileResult<DataRoom> {
        self.add_common_nodes()?;
        match &self.data_room.activation_type {
            None => {}
            Some(ActivationType::Direct) => {
                self.add_direct_activation_nodes()?;
            }
            Some(ActivationType::Consentless) => {
                self.add_consentless_activation_nodes()?;
            }
        }

        let permissions_advertiser: Vec<Permission> = self
            .permissions_advertiser
            .into_iter()
            .map(|permission| Permission { permission: Some(permission) })
            .collect();
        let permissions_publisher: Vec<Permission> = self
            .permissions_publisher
            .into_iter()
            .map(|permission| Permission { permission: Some(permission) })
            .collect();
        let permissions_observer: Vec<Permission> = self
            .permissions_observer
            .into_iter()
            .map(|permission| Permission { permission: Some(permission) })
            .collect();

        if self.data_room.advertiser_email == self.data_room.publisher_email {
            return Err(format!("User {} cannot be both advertiser and publisher", self.data_room.advertiser_email))?;
        } else {
            self.configuration_elements.push(ConfigurationElement {
                id: "permission_advertiser".into(),
                element: Some(configuration_element::Element::UserPermission(UserPermission {
                    email: self.data_room.advertiser_email.clone(),
                    permissions: permissions_advertiser.into_iter().collect(),
                    authentication_method_id: "authentication_method".into(),
                })),
            });
            self.configuration_elements.push(ConfigurationElement {
                id: "permission_publisher".into(),
                element: Some(configuration_element::Element::UserPermission(UserPermission {
                    email: self.data_room.publisher_email.clone(),
                    permissions: permissions_publisher.into_iter().collect(),
                    authentication_method_id: "authentication_method".into(),
                })),
            });
            if let Some(observer_user_email) = self.data_room.observer_user.as_ref() {
                self.configuration_elements.push(ConfigurationElement {
                    id: "permission_observer".into(),
                    element: Some(configuration_element::Element::UserPermission(UserPermission {
                        email: observer_user_email.clone(),
                        permissions: permissions_observer.into_iter().collect(),
                        authentication_method_id: "authentication_method".into(),
                    })),
                });
            }
        }

        let low_level_data_room = DataRoom {
            id: self.data_room.id.clone(),
            name: self.data_room.name.clone(),
            description: self.data_room.name.clone(),
            governance_protocol: Some(GovernanceProtocol {
                policy: Some(governance_protocol::Policy::AffectedDataOwnersApprovePolicy(
                    AffectedDataOwnersApprovePolicy {},
                )),
            }),
            initial_configuration: Some(DataRoomConfiguration { elements: self.configuration_elements }),
        };

        Ok(low_level_data_room)
    }

    fn add_common_nodes(&mut self) -> Result<(), CompileError> {
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

        for dataset_name in ["dataset_advertiser", "dataset_publisher"] {
            self.configuration_elements.push(ConfigurationElement {
                id: dataset_name.into(),
                element: Some(configuration_element::Element::ComputeNode(ComputeNode {
                    node_name: dataset_name.into(),
                    rate_limiting: None,
                    node: Some(compute_node::Node::Leaf(ComputeNodeLeaf { is_required: true })),
                })),
            });
        }

        self.configuration_elements.push(ConfigurationElement {
            id: "overlap_basic_script".into(),
            element: Some(configuration_element::Element::ComputeNode(ComputeNode {
                node_name: "overlap_basic_script".into(),
                node: Some(compute_node::Node::Branch(ComputeNodeBranch {
                    config: prost::Message::encode_length_delimited_to_vec(&DriverTaskConfig {
                        driver_task_config: Some(driver_task_config::DriverTaskConfig::StaticContent(
                            StaticContentConfig { content: include_bytes!("./overlap_basic.py").to_vec() },
                        )),
                    }),
                    dependencies: vec![],
                    output_format: ComputeNodeFormat::Raw as i32,
                    protocol: Some(ComputeNodeProtocol { version: self.driver_protocol_version }),
                    attestation_specification_id: self.driver_attestation_specification_id.clone(),
                })),
                rate_limiting: None,
            })),
        });
        let config = MediaDataRoomConfig::from_data_room(self.data_room)?;
        self.configuration_elements.push(ConfigurationElement {
            id: "media_data_room_config".into(),
            element: Some(configuration_element::Element::ComputeNode(ComputeNode {
                node_name: "media_data_room_config".into(),
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
                rate_limiting: None,
            })),
        });

        self.configuration_elements.push(ConfigurationElement {
            id: OVERLAP_BASIC_ID.into(),
            element: Some(configuration_element::Element::ComputeNode(ComputeNode {
                node_name: OVERLAP_BASIC_ID.into(),
                node: Some(compute_node::Node::Branch(ComputeNodeBranch {
                    config: prost::Message::encode_length_delimited_to_vec(&ContainerWorkerConfiguration {
                        configuration: Some(container_worker_configuration::Configuration::Static(StaticImage {
                            command: ["python3", "/input/overlap_basic.py"]
                                .iter()
                                .map(|s| s.to_string())
                                .collect::<Vec<_>>(),
                            mount_points: vec![
                                MountPoint {
                                    path: "overlap_basic.py".into(),
                                    dependency: "overlap_basic_script".into(),
                                },
                                MountPoint {
                                    path: "media_data_room_config.json".into(),
                                    dependency: "media_data_room_config".into(),
                                },
                                MountPoint {
                                    path: "dataset_advertiser.csv".into(),
                                    dependency: "dataset_advertiser".into(),
                                },
                                MountPoint {
                                    path: "dataset_publisher.csv".into(),
                                    dependency: "dataset_publisher".into(),
                                },
                            ],
                            output_path: "/output".into(),
                            include_container_logs_on_error: true,
                            include_container_logs_on_success: true,
                            minimum_container_memory_size: None,
                            extra_chunk_cache_size_to_available_memory_ratio: None,
                        })),
                    }),
                    dependencies: vec![
                        "overlap_basic_script".into(),
                        "media_data_room_config".into(),
                        "dataset_advertiser".into(),
                        "dataset_publisher".into(),
                    ],
                    output_format: ComputeNodeFormat::Zip as i32,
                    protocol: Some(ComputeNodeProtocol { version: self.python_protocol_version }),
                    attestation_specification_id: self.python_attestation_specification_id.clone(),
                })),
                rate_limiting: None,
            })),
        });

        self.permissions_advertiser.push(permission::Permission::ExecuteComputePermission(ExecuteComputePermission {
            compute_node_id: OVERLAP_BASIC_ID.into(),
        }));
        self.permissions_advertiser.push(permission::Permission::RetrieveComputeResultPermission(
            RetrieveComputeResultPermission { compute_node_id: OVERLAP_BASIC_ID.into() },
        ));
        self.permissions_advertiser
            .push(permission::Permission::RetrieveDataRoomPermission(RetrieveDataRoomPermission {}));
        self.permissions_advertiser
            .push(permission::Permission::RetrievePublishedDatasetsPermission(RetrievePublishedDatasetsPermission {}));
        self.permissions_advertiser.push(permission::Permission::LeafCrudPermission(LeafCrudPermission {
            leaf_node_id: "dataset_advertiser".into(),
        }));
        self.permissions_advertiser
            .push(permission::Permission::UpdateDataRoomStatusPermission(UpdateDataRoomStatusPermission {}));

        self.permissions_publisher
            .push(permission::Permission::RetrieveDataRoomPermission(RetrieveDataRoomPermission {}));
        self.permissions_publisher
            .push(permission::Permission::RetrievePublishedDatasetsPermission(RetrievePublishedDatasetsPermission {}));
        self.permissions_publisher.push(permission::Permission::LeafCrudPermission(LeafCrudPermission {
            leaf_node_id: "dataset_publisher".into(),
        }));
        self.permissions_publisher.push(permission::Permission::ExecuteComputePermission(ExecuteComputePermission {
            compute_node_id: OVERLAP_BASIC_ID.into(),
        }));
        self.permissions_publisher.push(permission::Permission::RetrieveComputeResultPermission(
            RetrieveComputeResultPermission { compute_node_id: OVERLAP_BASIC_ID.into() },
        ));
        self.permissions_publisher
            .push(permission::Permission::UpdateDataRoomStatusPermission(UpdateDataRoomStatusPermission {}));

        if self.data_room.observer_user.is_some() {
            self.permissions_observer.extend(
                vec![
                    permission::Permission::RetrieveDataRoomPermission(RetrieveDataRoomPermission {}),
                    permission::Permission::RetrieveDataRoomStatusPermission(RetrieveDataRoomStatusPermission {}),
                    permission::Permission::RetrieveAuditLogPermission(RetrieveAuditLogPermission {}),
                    permission::Permission::RetrievePublishedDatasetsPermission(RetrievePublishedDatasetsPermission {}),
                    permission::Permission::ExecuteComputePermission(ExecuteComputePermission {
                        compute_node_id: OVERLAP_BASIC_ID.into(),
                    }),
                    permission::Permission::RetrieveComputeResultPermission(RetrieveComputeResultPermission {
                        compute_node_id: OVERLAP_BASIC_ID.into(),
                    }),
                ]
                .into_iter(),
            );
        }

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

    fn add_direct_activation_nodes(&mut self) -> CompileResult<()> {
        self.configuration_elements.push(ConfigurationElement {
            id: "direct_activation_all_script".into(),
            element: Some(configuration_element::Element::ComputeNode(ComputeNode {
                node_name: "direct_activation_all_script".into(),
                node: Some(compute_node::Node::Branch(ComputeNodeBranch {
                    config: prost::Message::encode_length_delimited_to_vec(&DriverTaskConfig {
                        driver_task_config: Some(driver_task_config::DriverTaskConfig::StaticContent(
                            StaticContentConfig { content: include_bytes!("./direct_activation_all.py").to_vec() },
                        )),
                    }),
                    dependencies: vec![],
                    output_format: ComputeNodeFormat::Raw as i32,
                    protocol: Some(ComputeNodeProtocol { version: self.driver_protocol_version }),
                    attestation_specification_id: self.driver_attestation_specification_id.clone(),
                })),
                rate_limiting: None,
            })),
        });

        self.configuration_elements.push(ConfigurationElement {
            id: "direct_activation_all".into(),
            element: Some(configuration_element::Element::ComputeNode(ComputeNode {
                node_name: "direct_activation_all".into(),
                node: Some(compute_node::Node::Branch(ComputeNodeBranch {
                    config: prost::Message::encode_length_delimited_to_vec(&ContainerWorkerConfiguration {
                        configuration: Some(container_worker_configuration::Configuration::Static(StaticImage {
                            command: ["python3", "/input/direct_activation_all.py"]
                                .iter()
                                .map(|s| s.to_string())
                                .collect::<Vec<_>>(),
                            mount_points: vec![
                                MountPoint {
                                    path: "direct_activation_all.py".into(),
                                    dependency: "direct_activation_all_script".into(),
                                },
                                MountPoint {
                                    path: "media_data_room_config.json".into(),
                                    dependency: "media_data_room_config".into(),
                                },
                                MountPoint {
                                    path: "dataset_advertiser.csv".into(),
                                    dependency: "dataset_advertiser".into(),
                                },
                                MountPoint {
                                    path: "dataset_publisher.csv".into(),
                                    dependency: "dataset_publisher".into(),
                                },
                            ],
                            output_path: "/output".into(),
                            include_container_logs_on_error: true,
                            include_container_logs_on_success: true,
                            minimum_container_memory_size: None,
                            extra_chunk_cache_size_to_available_memory_ratio: None,
                        })),
                    }),
                    dependencies: vec![
                        "direct_activation_all_script".into(),
                        "media_data_room_config".into(),
                        "dataset_advertiser".into(),
                        "dataset_publisher".into(),
                    ],
                    output_format: ComputeNodeFormat::Zip as i32,
                    protocol: Some(ComputeNodeProtocol { version: self.python_protocol_version }),
                    attestation_specification_id: self.python_attestation_specification_id.clone(),
                })),
                rate_limiting: None,
            })),
        });

        self.configuration_elements.push(ConfigurationElement {
            id: "direct_activation_config".into(),
            element: Some(configuration_element::Element::ComputeNode(ComputeNode {
                node_name: "direct_activation_config".into(),
                rate_limiting: None,
                node: Some(compute_node::Node::Leaf(ComputeNodeLeaf {
                    // Making this non-required makes it easier to query its state using an
                    // execute request.
                    is_required: false,
                })),
            })),
        });

        self.configuration_elements.push(ConfigurationElement {
            id: "direct_activation_script".into(),
            element: Some(configuration_element::Element::ComputeNode(ComputeNode {
                node_name: "direct_activation_script".into(),
                node: Some(compute_node::Node::Branch(ComputeNodeBranch {
                    config: prost::Message::encode_length_delimited_to_vec(&DriverTaskConfig {
                        driver_task_config: Some(driver_task_config::DriverTaskConfig::StaticContent(
                            StaticContentConfig { content: include_bytes!("./direct_activation.py").to_vec() },
                        )),
                    }),
                    dependencies: vec![],
                    output_format: ComputeNodeFormat::Raw as i32,
                    protocol: Some(ComputeNodeProtocol { version: self.driver_protocol_version }),
                    attestation_specification_id: self.driver_attestation_specification_id.clone(),
                })),
                rate_limiting: None,
            })),
        });

        self.configuration_elements.push(ConfigurationElement {
            id: "direct_activation".into(),
            element: Some(configuration_element::Element::ComputeNode(ComputeNode {
                node_name: "direct_activation".into(),
                node: Some(compute_node::Node::Branch(ComputeNodeBranch {
                    config: prost::Message::encode_length_delimited_to_vec(&ContainerWorkerConfiguration {
                        configuration: Some(container_worker_configuration::Configuration::Static(StaticImage {
                            command: ["python3", "/input/direct_activation.py"]
                                .iter()
                                .map(|s| s.to_string())
                                .collect::<Vec<_>>(),
                            mount_points: vec![
                                MountPoint {
                                    path: "direct_activation.py".into(),
                                    dependency: "direct_activation_script".into(),
                                },
                                MountPoint {
                                    path: "direct_activation_all".into(),
                                    dependency: "direct_activation_all".into(),
                                },
                                MountPoint {
                                    path: "direct_activation_config.json".into(),
                                    dependency: "direct_activation_config".into(),
                                },
                            ],
                            output_path: "/output".into(),
                            include_container_logs_on_error: true,
                            include_container_logs_on_success: true,
                            minimum_container_memory_size: None,
                            extra_chunk_cache_size_to_available_memory_ratio: None,
                        })),
                    }),
                    dependencies: vec![
                        "direct_activation_all".into(),
                        "direct_activation_config".into(),
                        "direct_activation_script".into(),
                    ],
                    output_format: ComputeNodeFormat::Zip as i32,
                    protocol: Some(ComputeNodeProtocol { version: self.python_protocol_version }),
                    attestation_specification_id: self.python_attestation_specification_id.clone(),
                })),
                rate_limiting: None,
            })),
        });

        self.permissions_advertiser.push(permission::Permission::LeafCrudPermission(LeafCrudPermission {
            leaf_node_id: "direct_activation_config".into(),
        }));
        // We treat the leaf node as a compute node so that the users can query the associated data.
        self.permissions_advertiser.push(permission::Permission::ExecuteComputePermission(ExecuteComputePermission {
            compute_node_id: "direct_activation_config".into(),
        }));
        self.permissions_advertiser.push(permission::Permission::RetrieveComputeResultPermission(
            RetrieveComputeResultPermission { compute_node_id: "direct_activation_config".into() },
        ));
        self.permissions_publisher.push(permission::Permission::ExecuteComputePermission(ExecuteComputePermission {
            compute_node_id: "direct_activation_config".into(),
        }));
        self.permissions_publisher.push(permission::Permission::RetrieveComputeResultPermission(
            RetrieveComputeResultPermission { compute_node_id: "direct_activation_config".into() },
        ));

        if self.data_room.enable_download_by_advertiser {
            self.permissions_advertiser.push(permission::Permission::ExecuteComputePermission(
                ExecuteComputePermission { compute_node_id: "direct_activation".into() },
            ));
            self.permissions_advertiser.push(permission::Permission::RetrieveComputeResultPermission(
                RetrieveComputeResultPermission { compute_node_id: "direct_activation".into() },
            ));
        }

        if self.data_room.enable_download_by_publisher {
            self.permissions_publisher.push(permission::Permission::ExecuteComputePermission(
                ExecuteComputePermission { compute_node_id: "direct_activation".into() },
            ));
            self.permissions_publisher.push(permission::Permission::RetrieveComputeResultPermission(
                RetrieveComputeResultPermission { compute_node_id: "direct_activation".into() },
            ));
        }

        self.permissions_advertiser
            .push(permission::Permission::CasAuxiliaryStatePermission(CasAuxiliaryStatePermission {}));
        self.permissions_advertiser
            .push(permission::Permission::ReadAuxiliaryStatePermission(ReadAuxiliaryStatePermission {}));
        self.permissions_publisher
            .push(permission::Permission::CasAuxiliaryStatePermission(CasAuxiliaryStatePermission {}));
        self.permissions_publisher
            .push(permission::Permission::ReadAuxiliaryStatePermission(ReadAuxiliaryStatePermission {}));

        Ok(())
    }

    fn add_consentless_activation_nodes(&mut self) -> CompileResult<()> {
        self.configuration_elements.push(ConfigurationElement {
            id: "overlap_insights_script".into(),
            element: Some(configuration_element::Element::ComputeNode(ComputeNode {
                node_name: "overlap_insights_script".into(),
                node: Some(compute_node::Node::Branch(ComputeNodeBranch {
                    config: prost::Message::encode_length_delimited_to_vec(&DriverTaskConfig {
                        driver_task_config: Some(driver_task_config::DriverTaskConfig::StaticContent(
                            StaticContentConfig {
                                content: include_bytes!("./consentless_overlap_insights.py").to_vec(),
                            },
                        )),
                    }),
                    dependencies: vec![],
                    output_format: ComputeNodeFormat::Raw as i32,
                    protocol: Some(ComputeNodeProtocol { version: self.driver_protocol_version }),
                    attestation_specification_id: self.driver_attestation_specification_id.clone(),
                })),
                rate_limiting: None,
            })),
        });

        self.configuration_elements.push(ConfigurationElement {
            id: "overlap_insights_params".into(),
            element: Some(configuration_element::Element::ComputeNode(ComputeNode {
                node_name: "overlap_insights_params".into(),
                rate_limiting: None,
                node: Some(compute_node::Node::Parameter(ComputeNodeParameter { is_required: true })),
            })),
        });

        self.configuration_elements.push(ConfigurationElement {
            id: OVERLAP_INSIGHTS_ID.into(),
            element: Some(configuration_element::Element::ComputeNode(ComputeNode {
                node_name: OVERLAP_INSIGHTS_ID.into(),
                node: Some(compute_node::Node::Branch(ComputeNodeBranch {
                    config: prost::Message::encode_length_delimited_to_vec(&ContainerWorkerConfiguration {
                        configuration: Some(container_worker_configuration::Configuration::Static(StaticImage {
                            command: ["python3", "/input/data_insights.py"]
                                .iter()
                                .map(|s| s.to_string())
                                .collect::<Vec<_>>(),
                            mount_points: vec![
                                MountPoint {
                                    path: "data_insights.py".into(),
                                    dependency: "overlap_insights_script".into(),
                                },
                                MountPoint {
                                    path: "media_data_room_config.json".into(),
                                    dependency: "media_data_room_config".into(),
                                },
                                MountPoint {
                                    path: "overlap_insights_params.json".into(),
                                    dependency: "overlap_insights_params".into(),
                                },
                                MountPoint {
                                    path: "dataset_advertiser.csv".into(),
                                    dependency: "dataset_advertiser".into(),
                                },
                                MountPoint {
                                    path: "dataset_publisher.csv".into(),
                                    dependency: "dataset_publisher".into(),
                                },
                            ],
                            output_path: "/output".into(),
                            include_container_logs_on_error: true,
                            include_container_logs_on_success: true,
                            minimum_container_memory_size: None,
                            extra_chunk_cache_size_to_available_memory_ratio: None,
                        })),
                    }),
                    dependencies: vec![
                        "overlap_insights_script".into(),
                        "media_data_room_config".into(),
                        "overlap_insights_params".into(),
                        "dataset_advertiser".into(),
                        "dataset_publisher".into(),
                    ],
                    output_format: ComputeNodeFormat::Zip as i32,
                    protocol: Some(ComputeNodeProtocol { version: self.python_protocol_version }),
                    attestation_specification_id: self.python_attestation_specification_id.clone(),
                })),
                rate_limiting: None,
            })),
        });

        self.permissions_advertiser
            .push(permission::Permission::CasAuxiliaryStatePermission(CasAuxiliaryStatePermission {}));
        self.permissions_advertiser
            .push(permission::Permission::ReadAuxiliaryStatePermission(ReadAuxiliaryStatePermission {}));
        self.permissions_advertiser.push(permission::Permission::ExecuteComputePermission(ExecuteComputePermission {
            compute_node_id: OVERLAP_INSIGHTS_ID.into(),
        }));
        self.permissions_advertiser.push(permission::Permission::RetrieveComputeResultPermission(
            RetrieveComputeResultPermission { compute_node_id: OVERLAP_INSIGHTS_ID.into() },
        ));

        self.permissions_publisher
            .push(permission::Permission::CasAuxiliaryStatePermission(CasAuxiliaryStatePermission {}));
        self.permissions_publisher
            .push(permission::Permission::ReadAuxiliaryStatePermission(ReadAuxiliaryStatePermission {}));
        self.permissions_publisher.push(permission::Permission::ExecuteComputePermission(ExecuteComputePermission {
            compute_node_id: OVERLAP_INSIGHTS_ID.into(),
        }));
        self.permissions_publisher.push(permission::Permission::RetrieveComputeResultPermission(
            RetrieveComputeResultPermission { compute_node_id: OVERLAP_INSIGHTS_ID.into() },
        ));

        if self.data_room.observer_user.is_some() {
            self.permissions_observer.push(permission::Permission::ExecuteComputePermission(
                ExecuteComputePermission { compute_node_id: OVERLAP_INSIGHTS_ID.into() },
            ));
            self.permissions_observer.push(permission::Permission::RetrieveComputeResultPermission(
                RetrieveComputeResultPermission { compute_node_id: OVERLAP_INSIGHTS_ID.into() },
            ));
        }

        Ok(())
    }
}
