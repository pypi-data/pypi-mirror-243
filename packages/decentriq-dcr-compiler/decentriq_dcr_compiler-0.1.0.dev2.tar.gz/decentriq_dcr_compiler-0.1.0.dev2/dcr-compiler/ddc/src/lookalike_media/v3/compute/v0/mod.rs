use std::iter::FromIterator;

use delta_attestation_api::*;
use delta_container_worker_api::*;
use delta_data_room_api::WindowRateLimitingConfig;
use delta_data_room_api::*;
use delta_gcg_driver_api::*;
use format_types::v0::FormatType;
use format_types::v0::HashingAlgorithm;
use schemars::JsonSchema;
use serde::Deserialize;
use serde::Serialize;
use validation_config::v0::ColumnValidationV0;
use validation_config::v0::TableValidationV0;
use validation_config::v0::ValidationConfigV0;
use validation_config::ValidationConfig;

use crate::data_lab::provides::apply_hashing_algorithm_type_to_format;
use crate::feature::Requirements;
use crate::lookalike_media::features::ENABLE_AUDIT_LOG_RETRIEVAL;
use crate::lookalike_media::features::ENABLE_DEV_COMPUTATIONS;
use crate::lookalike_media::features::ENABLE_RATE_LIMITING_ON_PUBLISH_DATASET;
use crate::lookalike_media::v0::EnclaveSpecificationV0;
use crate::*;

pub const DEBUG: bool = false;

pub fn default_enable_rate_limiting_on_publish_dataset() -> bool {
    true
}
pub fn default_rate_limit_publish_data_window_seconds() -> u32 {
    24 * 3600 * 7 // one week in seconds
}
pub fn default_rate_limit_publish_data_num_per_window() -> u32 {
    10
}

pub fn rate_limiting_config(
    enable_rate_limiting_on_publish_dataset: bool,
    dcr: &LookalikeMediaDcrComputeV0,
) -> Option<RateLimitingConfig> {
    if enable_rate_limiting_on_publish_dataset {
        Some(RateLimitingConfig {
            method: Some(rate_limiting_config::Method::Window(WindowRateLimitingConfig {
                time_window_seconds: dcr.rate_limit_publish_data_window_seconds,
                num_max_executions: dcr.rate_limit_publish_data_num_per_window,
            })),
        })
    } else {
        None
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CalculateOverlapInsightsParams {
    pub audience_types: Vec<String>,
}

// Not used at the time but maybe still useful in case we still want to make
// some stuff configurable from the client.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct LookalikeMediaDataRoomConfigV0 {}

// Warning: changing any of these lines will require changes in the python
// scripts contained in the same directory.
pub const DATASET_EMBEDDINGS_ID: &str = "embeddings";
pub const DATASET_SEGMENTS_ID: &str = "segments";
pub const DATASET_AUDIENCES_ID: &str = "audiences";
pub const DATASET_MATCHING_ID: &str = "matching";
pub const DATASET_DEMOGRAPHICS_ID: &str = "demographics";
pub const ACTIVATED_AUDIENCES_CONFIG_ID: &str = "activated_audiences.json";
pub const REQUESTED_AUDIENCE_CONFIG_ID: &str = "requested_audience.json";

pub const DQ_MEDIA_DCR_FILE: &str = "dq_media_dcr-0.3.0.tar.gz";
pub const DQ_MEDIA_DCR_ID: &str = "dq_media_dcr";
pub const DQ_MEDIA_DCR_TAR_GZ: &[u8] = include_bytes!("dq_media_dcr-0.3.0.tar.gz");

pub const COMPUTE_RELEVANT_USERS_ID: &str = "compute_relevant_users";
pub const COMPUTE_RELEVANT_USERS_PY: &[u8] = include_bytes!("compute_relevant_users.py");

pub const OVERLAP_BASIC_ID: &str = "overlap_basic";
pub const OVERLAP_BASIC_PY: &[u8] = include_bytes!("overlap_basic.py");

pub const CONSENTLESS_OVERLAP_INSIGHTS_ID: &str = "consentless_overlap_insights";
pub const CONSENTLESS_OVERLAP_INSIGHTS_PY: &[u8] = include_bytes!("consentless_overlap_insights.py");

pub const SCORE_USERS_ID: &str = "score_users";
pub const SCORE_USERS_PY: &[u8] = include_bytes!("score_users.py");

pub const CREATE_ACTIVATED_AUDIENCES_ID: &str = "create_activated_audiences";
pub const CREATE_ACTIVATED_AUDIENCES_PY: &[u8] = include_bytes!("create_activated_audiences.py");

pub const COMPUTE_AUDIENCE_SIZES_ID: &str = "compute_audience_sizes";
pub const COMPUTE_AUDIENCE_SIZES_PY: &[u8] = include_bytes!("compute_audience_sizes.py");

pub const MODELLED_AUDIENCE_INSIGHTS_VIEW_ID: &str = "modelled_audience_insights_view";
pub const MODELLED_AUDIENCE_INSIGHTS_VIEW_PY: &[u8] = include_bytes!("modelled_audience_insights_view.py");

pub const MODELLED_AUDIENCE_INSIGHTS_ID: &str = "modelled_audience_insights";
pub const MODELLED_AUDIENCE_INSIGHTS_PY: &[u8] = include_bytes!("modelled_audience_insights.py");

pub const GET_LOOKALIKE_AUDIENCE_ID: &str = "get_lookalike_audience";
pub const GET_LOOKALIKE_AUDIENCES_PY: &[u8] = include_bytes!("get_lookalike_audience.py");

pub const VIEW_ACTIVATED_AUDIENCES_ID: &str = "view_activated_audiences";
pub const VIEW_ACTIVATED_AUDIENCES_PY: &[u8] = include_bytes!("view_activated_audiences.py");

pub const VIEW_PUBLISHED_ACTIVATED_AUDIENCES_ID: &str = "view_published_activated_audiences";
pub const VIEW_PUBLISHED_ACTIVATED_AUDIENCES_PY: &[u8] = include_bytes!("view_published_activated_audiences.py");

pub const INGEST_MATCHING_ID: &str = "ingest_matching";
pub const INGEST_MATCHING_PY: &[u8] = include_bytes!("ingest_matching.py");

pub const INGEST_AUDIENCES_ID: &str = "ingest_audiences";
pub const INGEST_AUDIENCES_PY: &[u8] = include_bytes!("ingest_audiences.py");

pub const INGEST_AUDIENCES_REPORT_ID: &str = "ingest_audiences_report";

pub const INGEST_SEGMENTS_ID: &str = "ingest_segments";
pub const INGEST_SEGMENTS_PY: &[u8] = include_bytes!("ingest_segments.py");

pub const INGEST_DEMOGRAPHICS_ID: &str = "ingest_demographics";
pub const INGEST_DEMOGRAPHICS_PY: &[u8] = include_bytes!("ingest_demographics.py");

pub const INGEST_EMBEDDINGS_ID: &str = "ingest_embeddings";
pub const INGEST_EMBEDDINGS_PY: &[u8] = include_bytes!("ingest_embeddings.py");

pub const DCR_CONFIG_ID: &str = "media_data_room_config.json";

/// See the following diagram for a visualization of the graph:
/// https://docs.google.com/drawings/d/13VfBcnhLmOlB_XBrekAmBtyi-zoThZdg1aKtJYVD2eA/edit?usp=sharing
#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct LookalikeMediaDcrComputeV0 {
    pub id: String,
    pub name: String,
    pub main_publisher_email: String,
    pub main_advertiser_email: String,
    pub publisher_emails: Vec<String>,
    pub advertiser_emails: Vec<String>,
    pub observer_emails: Vec<String>,
    pub agency_emails: Vec<String>,

    pub matching_id_format: FormatType,
    pub hash_matching_id_with: Option<HashingAlgorithm>,

    pub authentication_root_certificate_pem: String,
    pub driver_enclave_specification: EnclaveSpecificationV0,
    pub python_enclave_specification: EnclaveSpecificationV0,

    #[serde(default = "default_rate_limit_publish_data_window_seconds")]
    pub rate_limit_publish_data_window_seconds: u32,
    #[serde(default = "default_rate_limit_publish_data_num_per_window")]
    pub rate_limit_publish_data_num_per_window: u32,
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct CreateLookalikeMediaDcrComputeV0 {
    pub id: String,
    pub name: String,
    pub main_publisher_email: String,
    pub main_advertiser_email: String,
    pub publisher_emails: Vec<String>,
    pub advertiser_emails: Vec<String>,
    pub observer_emails: Vec<String>,
    pub agency_emails: Vec<String>,

    pub enable_audit_log_retrieval: bool,
    pub enable_dev_computations: bool,

    pub enable_rate_limiting_on_publish_dataset: Option<bool>,
    pub rate_limit_publish_data_window_seconds: Option<u32>,
    pub rate_limit_publish_data_num_per_window: Option<u32>,

    pub authentication_root_certificate_pem: String,
    pub driver_enclave_specification: EnclaveSpecificationV0,
    pub python_enclave_specification: EnclaveSpecificationV0,
    pub matching_id_format: FormatType,
    pub hash_matching_id_with: Option<HashingAlgorithm>,
}

struct LookalikeMediaDcrComputeCompilerV0<'a> {
    data_room: &'a LookalikeMediaDcrComputeV0,
    driver_attestation_specification_id: String,
    python_attestation_specification_id: String,
    driver_protocol_version: u32,
    python_protocol_version: u32,
    configuration_elements: Vec<ConfigurationElement>,
    permissions_advertiser: Vec<Permission>,
    permissions_publisher: Vec<Permission>,
    permissions_observer: Vec<Permission>,
    permissions_agency: Vec<Permission>,
    requirements: &'a Requirements,
    features: &'a Vec<String>,
}

pub fn compile_compute(
    data_room: &LookalikeMediaDcrComputeV0,
    features: &Vec<String>,
    requirements: &Requirements,
) -> Result<DataRoom, CompileError> {
    LookalikeMediaDcrComputeCompilerV0::new(data_room, features, requirements)?.compile()
}

fn data_room_to_data_room_config(
    _data_room: &LookalikeMediaDcrComputeV0,
) -> CompileResult<LookalikeMediaDataRoomConfigV0> {
    Ok(LookalikeMediaDataRoomConfigV0 {})
}

// This is for clarity in add_permissions
#[allow(non_upper_case_globals)]
const __: bool = false;

impl<'a> LookalikeMediaDcrComputeCompilerV0<'a> {
    pub fn new(
        data_room: &'a LookalikeMediaDcrComputeV0,
        features: &'a Vec<String>,
        requirements: &'a Requirements,
    ) -> CompileResult<Self> {
        let driver_attestation_specification_id =
            format!("attestation_specification-{}", data_room.driver_enclave_specification.id);
        let python_attestation_specification_id =
            format!("attestation_specification-{}", data_room.python_enclave_specification.id);
        Ok(Self {
            data_room,
            driver_attestation_specification_id,
            python_attestation_specification_id,
            driver_protocol_version: data_room.driver_enclave_specification.worker_protocol,
            python_protocol_version: data_room.python_enclave_specification.worker_protocol,
            configuration_elements: vec![],
            permissions_advertiser: vec![],
            permissions_publisher: vec![],
            permissions_observer: vec![],
            permissions_agency: vec![],
            requirements,
            features,
        })
    }

    pub fn compile(mut self) -> CompileResult<DataRoom> {
        self.add_compute_nodes()?;

        {
            // Role checks
            let advertiser_set = HashSet::from_iter(self.data_room.advertiser_emails.iter());
            let publisher_set = HashSet::from_iter(self.data_room.publisher_emails.iter());
            if !advertiser_set.contains(&self.data_room.main_advertiser_email) {
                return Err(format!(
                    "User {} is set as the main advertiser, however is not listed in the advertiser list {:?}",
                    self.data_room.main_advertiser_email, self.data_room.advertiser_emails,
                ))?;
            }
            if !publisher_set.contains(&self.data_room.main_publisher_email) {
                return Err(format!(
                    "User {} is set as the main publisher, however is not listed in the publisher list {:?}",
                    self.data_room.main_publisher_email, self.data_room.publisher_emails,
                ))?;
            }
            let non_overlapping_sets: [Set<&String>; 4] = [
                advertiser_set,
                publisher_set,
                Set::from_iter(self.data_room.observer_emails.iter()),
                Set::from_iter(self.data_room.agency_emails.iter()),
            ];
            for i in 0 .. non_overlapping_sets.len() {
                for j in i + 1 .. non_overlapping_sets.len() {
                    if let Some(overlapped) = non_overlapping_sets[i].intersection(&non_overlapping_sets[j]).next() {
                        return Err(format!("User {} cannot have multiple roles", overlapped))?;
                    }
                }
            }
        }

        for advertiser_email in &self.data_room.advertiser_emails {
            self.configuration_elements.push(ConfigurationElement {
                id: format!("permission_advertiser_{}", advertiser_email),
                element: Some(configuration_element::Element::UserPermission(UserPermission {
                    email: advertiser_email.clone(),
                    permissions: self.permissions_advertiser.iter().cloned().collect(),
                    authentication_method_id: "authentication_method".into(),
                })),
            });
        }

        for publisher_email in &self.data_room.publisher_emails {
            self.configuration_elements.push(ConfigurationElement {
                id: format!("permission_publisher_{}", publisher_email),
                element: Some(configuration_element::Element::UserPermission(UserPermission {
                    email: publisher_email.clone(),
                    permissions: self.permissions_publisher.iter().cloned().collect(),
                    authentication_method_id: "authentication_method".into(),
                })),
            });
        }

        for observer_email in &self.data_room.observer_emails {
            self.configuration_elements.push(ConfigurationElement {
                id: format!("permission_observer_{}", observer_email),
                element: Some(configuration_element::Element::UserPermission(UserPermission {
                    email: observer_email.clone(),
                    permissions: self.permissions_observer.iter().cloned().collect(),
                    authentication_method_id: "authentication_method".into(),
                })),
            });
        }

        for agency_email in &self.data_room.agency_emails {
            self.configuration_elements.push(ConfigurationElement {
                id: format!("permission_agency_{}", agency_email),
                element: Some(configuration_element::Element::UserPermission(UserPermission {
                    email: agency_email.clone(),
                    permissions: self.permissions_agency.iter().cloned().collect(),
                    authentication_method_id: "authentication_method".into(),
                })),
            });
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

    // [Advertiser, Publisher, Observer, Agency]
    fn add_permissions(&mut self, permissions: Vec<(permission::Permission, [bool; 4])>) {
        for (permission, [advertiser, publisher, observer, agency]) in permissions {
            let permission = Permission { permission: Some(permission) };
            if advertiser {
                self.permissions_advertiser.push(permission.clone())
            }
            if publisher {
                self.permissions_publisher.push(permission.clone())
            }
            if observer {
                self.permissions_observer.push(permission.clone())
            }
            if agency {
                self.permissions_agency.push(permission.clone())
            }
        }
    }

    fn add_compute_relevant_users(&mut self) -> CompileResult<()> {
        let script_id = get_script_id(COMPUTE_RELEVANT_USERS_ID);

        self.configuration_elements.push(ConfigurationElement {
            id: script_id.clone(),
            element: Some(configuration_element::Element::ComputeNode(ComputeNode {
                node_name: script_id.clone(),
                node: Some(compute_node::Node::Branch(ComputeNodeBranch {
                    config: prost::Message::encode_length_delimited_to_vec(&DriverTaskConfig {
                        driver_task_config: Some(driver_task_config::DriverTaskConfig::StaticContent(
                            StaticContentConfig { content: COMPUTE_RELEVANT_USERS_PY.to_vec() },
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

        self.configuration_elements.push(
            ContainerNode {
                id: COMPUTE_RELEVANT_USERS_ID.into(),
                main_script_path: "/input/run.py",
                mount_points: vec![
                    MountPoint { path: "run.py".into(), dependency: script_id.clone() },
                    MountPoint { path: INGEST_EMBEDDINGS_ID.into(), dependency: INGEST_EMBEDDINGS_ID.into() },
                    MountPoint { path: INGEST_SEGMENTS_ID.into(), dependency: INGEST_SEGMENTS_ID.into() },
                    MountPoint { path: DQ_MEDIA_DCR_FILE.into(), dependency: DQ_MEDIA_DCR_ID.into() },
                ],
                python_attestation_specification_id: &self.python_attestation_specification_id,
                python_protocol_version: self.python_protocol_version,
                memory_allocation_strategy: MemoryAllocationStrategy::SqlOptimized,
                additional_dependencies: vec![],
                rate_limiting: None,
            }
            .into(),
        );

        Ok(())
    }

    fn add_overlap_basic(&mut self) -> CompileResult<()> {
        let script_id = get_script_id(OVERLAP_BASIC_ID);

        self.configuration_elements.push(ConfigurationElement {
            id: script_id.clone(),
            element: Some(configuration_element::Element::ComputeNode(ComputeNode {
                node_name: script_id.clone(),
                node: Some(compute_node::Node::Branch(ComputeNodeBranch {
                    config: prost::Message::encode_length_delimited_to_vec(&DriverTaskConfig {
                        driver_task_config: Some(driver_task_config::DriverTaskConfig::StaticContent(
                            StaticContentConfig { content: OVERLAP_BASIC_PY.to_vec() },
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

        self.configuration_elements.push(
            ContainerNode {
                id: OVERLAP_BASIC_ID.into(),
                main_script_path: "/input/run.py",
                mount_points: vec![
                    MountPoint { path: "run.py".into(), dependency: script_id.clone() },
                    MountPoint { path: INGEST_MATCHING_ID.into(), dependency: INGEST_MATCHING_ID.into() },
                    MountPoint { path: INGEST_AUDIENCES_ID.into(), dependency: INGEST_AUDIENCES_ID.into() },
                    MountPoint { path: COMPUTE_RELEVANT_USERS_ID.into(), dependency: COMPUTE_RELEVANT_USERS_ID.into() },
                    MountPoint { path: DQ_MEDIA_DCR_FILE.into(), dependency: DQ_MEDIA_DCR_ID.into() },
                ],
                python_attestation_specification_id: &self.python_attestation_specification_id,
                python_protocol_version: self.python_protocol_version,
                memory_allocation_strategy: MemoryAllocationStrategy::SqlOptimized,
                additional_dependencies: vec![],
                rate_limiting: None,
            }
            .into(),
        );

        Ok(())
    }

    fn add_data_nodes(&mut self) -> CompileResult<()> {
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

        // Add validated table nodes
        for (dataset_name, is_required, validation_config, add_rate_limiting) in [
            (DATASET_AUDIENCES_ID, true, Some(advertiser_validation_config(&self.matching_id_format_type())?), true),
            (DATASET_MATCHING_ID, true, None, true),
            (DATASET_SEGMENTS_ID, true, None, true),
            (DATASET_DEMOGRAPHICS_ID, false, None, true),
        ] {
            // Add the data node itself
            self.configuration_elements.push(ConfigurationElement {
                id: dataset_name.into(),
                element: Some(configuration_element::Element::ComputeNode(ComputeNode {
                    node_name: dataset_name.into(),
                    rate_limiting: if add_rate_limiting {
                        rate_limiting_config(self.enable_rate_limiting_on_publish_dataset(), &self.data_room)
                    } else {
                        None
                    },
                    node: Some(compute_node::Node::Leaf(ComputeNodeLeaf { is_required })),
                })),
            });

            // validation on top of the data node
            if let Some(validation_config) = validation_config {
                crate::validation::v2::add_nodes_for_validation(
                    &mut self.configuration_elements, dataset_name, dataset_name, &validation_config,
                    &self.driver_attestation_specification_id,
                    self.data_room.driver_enclave_specification.worker_protocol,
                    &self.python_attestation_specification_id,
                    self.data_room.python_enclave_specification.worker_protocol,
                )?;
            }
        }

        // Add raw nodes
        for (dataset_name, is_required) in [(DATASET_EMBEDDINGS_ID, false), (ACTIVATED_AUDIENCES_CONFIG_ID, false)] {
            self.configuration_elements.push(ConfigurationElement {
                id: dataset_name.into(),
                element: Some(configuration_element::Element::ComputeNode(ComputeNode {
                    node_name: dataset_name.into(),
                    rate_limiting: rate_limiting_config(
                        self.enable_rate_limiting_on_publish_dataset(),
                        &self.data_room,
                    ),
                    node: Some(compute_node::Node::Leaf(ComputeNodeLeaf { is_required })),
                })),
            });
        }

        // Add ingestion nodes
        self.add_ingestion_node(INGEST_DEMOGRAPHICS_ID, INGEST_DEMOGRAPHICS_PY, DATASET_DEMOGRAPHICS_ID, false)?;
        self.add_ingestion_node(INGEST_SEGMENTS_ID, INGEST_SEGMENTS_PY, DATASET_SEGMENTS_ID, false)?;
        self.add_ingestion_node(INGEST_EMBEDDINGS_ID, INGEST_EMBEDDINGS_PY, DATASET_EMBEDDINGS_ID, false)?;
        self.add_ingestion_node(INGEST_AUDIENCES_ID, INGEST_AUDIENCES_PY, DATASET_AUDIENCES_ID, true)?;
        self.add_ingest_matching_node()?;
        self.add_report_node(INGEST_AUDIENCES_ID, INGEST_AUDIENCES_REPORT_ID)?;

        Ok(())
    }

    fn add_ingestion_node(
        &mut self,
        id: &str,
        content: &[u8],
        dataset_leaf_id: &str,
        is_validated: bool,
    ) -> CompileResult<()> {
        let script_id = format!("{}_script", id);
        self.configuration_elements.push(
            StaticContentNode {
                id: &script_id,
                content,
                driver_protocol_version: self.driver_protocol_version,
                driver_attestation_specification_id: &self.driver_attestation_specification_id,
            }
            .into(),
        );

        let (upstream_node, additional_dependencies) = if is_validated {
            (validation::v2::get_validation_id(dataset_leaf_id), vec![validation::v2::get_validation_check_id(
                dataset_leaf_id,
            )])
        } else {
            (dataset_leaf_id.to_string(), vec![])
        };

        self.configuration_elements.push(
            ContainerNode {
                id: id.into(),
                main_script_path: "/input/ingest.py",
                mount_points: vec![
                    MountPoint { path: "ingest.py".into(), dependency: script_id },
                    MountPoint { path: dataset_leaf_id.to_string(), dependency: upstream_node },
                    MountPoint { path: DQ_MEDIA_DCR_FILE.into(), dependency: DQ_MEDIA_DCR_ID.into() },
                ],
                python_attestation_specification_id: &self.python_attestation_specification_id,
                python_protocol_version: self.python_protocol_version,
                memory_allocation_strategy: MemoryAllocationStrategy::SqlOptimized,
                additional_dependencies,
                rate_limiting: None,
            }
            .into(),
        );

        Ok(())
    }

    fn add_ingest_matching_node(&mut self) -> CompileResult<()> {
        let script_id = format!("{}_script", INGEST_MATCHING_ID);
        self.configuration_elements.push(
            StaticContentNode {
                id: &script_id,
                content: INGEST_MATCHING_PY,
                driver_protocol_version: self.driver_protocol_version,
                driver_attestation_specification_id: &self.driver_attestation_specification_id,
            }
            .into(),
        );

        self.configuration_elements.push(
            ContainerNode {
                id: INGEST_MATCHING_ID,
                main_script_path: "/input/ingest.py",
                mount_points: vec![
                    MountPoint { path: "ingest.py".into(), dependency: script_id },
                    MountPoint { path: INGEST_AUDIENCES_ID.into(), dependency: INGEST_AUDIENCES_ID.into() },
                    MountPoint { path: DATASET_MATCHING_ID.into(), dependency: DATASET_MATCHING_ID.into() },
                    MountPoint { path: DQ_MEDIA_DCR_FILE.into(), dependency: DQ_MEDIA_DCR_ID.into() },
                ],
                python_attestation_specification_id: &self.python_attestation_specification_id,
                python_protocol_version: self.python_protocol_version,
                memory_allocation_strategy: MemoryAllocationStrategy::SqlOptimized,
                additional_dependencies: vec![],
                rate_limiting: None,
            }
            .into(),
        );

        Ok(())
    }

    fn add_python_package_node(&mut self) -> CompileResult<()> {
        self.configuration_elements.push(ConfigurationElement {
            id: DQ_MEDIA_DCR_ID.into(),
            element: Some(configuration_element::Element::ComputeNode(ComputeNode {
                node_name: DQ_MEDIA_DCR_ID.into(),
                node: Some(compute_node::Node::Branch(ComputeNodeBranch {
                    config: prost::Message::encode_length_delimited_to_vec(&DriverTaskConfig {
                        driver_task_config: Some(driver_task_config::DriverTaskConfig::StaticContent(
                            StaticContentConfig { content: DQ_MEDIA_DCR_TAR_GZ.to_vec() },
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
        Ok(())
    }

    fn add_data_room_config_node(&mut self) -> CompileResult<()> {
        let config = data_room_to_data_room_config(self.data_room)?;
        self.configuration_elements.push(ConfigurationElement {
            id: DCR_CONFIG_ID.into(),
            element: Some(configuration_element::Element::ComputeNode(ComputeNode {
                node_name: DCR_CONFIG_ID.into(),
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

        Ok(())
    }

    #[rustfmt::skip]
    fn add_compute_nodes(&mut self) -> CompileResult<()> {
        self.add_data_nodes()?;
        self.add_python_package_node()?;
        self.add_data_room_config_node()?;
        self.add_compute_relevant_users()?;
        self.add_overlap_basic()?;
        self.add_overlap_insights_node()?;
        self.add_score_users_node()?;
        self.add_create_activated_audiences_node()?;
        self.add_get_lookalike_audience_node()?;
        self.add_modelled_audience_insight_nodes()?;
        self.add_activated_audiences_nodes()?;

        if DEBUG {
            self.add_container_log_node(SCORE_USERS_ID)?;
            self.add_container_log_node(OVERLAP_BASIC_ID)?;
            self.add_container_log_node(CONSENTLESS_OVERLAP_INSIGHTS_ID)?;
            self.add_container_log_node(MODELLED_AUDIENCE_INSIGHTS_ID)?;
            self.add_container_log_node(INGEST_EMBEDDINGS_ID)?;
            self.add_container_log_node(INGEST_SEGMENTS_ID)?;
            self.add_container_log_node(INGEST_DEMOGRAPHICS_ID)?;
            self.add_container_log_node(INGEST_MATCHING_ID)?;
            self.add_container_log_node(COMPUTE_RELEVANT_USERS_ID)?;

            // [Advertiser, Publisher, Observer, Agency]
            self.add_permissions(vec![
                ( P::execute_compute(&get_container_log_node_id(COMPUTE_RELEVANT_USERS_ID))               , [true , true , true , true ] ) ,
                ( P::retrieve_compute_result(&get_container_log_node_id(COMPUTE_RELEVANT_USERS_ID))       , [true , true , true , true ] ) ,
                ( P::execute_compute(COMPUTE_RELEVANT_USERS_ID)                                           , [true , true , true , true ] ) ,
                ( P::retrieve_compute_result(COMPUTE_RELEVANT_USERS_ID)                                   , [true , true , true , true ] ) ,

                ( P::execute_compute(&get_container_log_node_id(SCORE_USERS_ID))                          , [true , true , true , true ] ) ,
                ( P::retrieve_compute_result(&get_container_log_node_id(SCORE_USERS_ID))                  , [true , true , true , true ] ) ,
                ( P::execute_compute(SCORE_USERS_ID)                                                      , [true , true , true , true ] ) ,
                ( P::retrieve_compute_result(SCORE_USERS_ID)                                              , [true , true , true , true ] ) ,

                (P::execute_compute(&get_container_log_node_id(INGEST_MATCHING_ID))                       , [true , true , true , true ] ) ,
                (P::retrieve_compute_result(&get_container_log_node_id(INGEST_MATCHING_ID))               , [true , true , true , true ] ) ,
                (P::execute_compute(INGEST_MATCHING_ID)                                                   , [true , true , true , true ] ) ,
                (P::retrieve_compute_result(INGEST_MATCHING_ID)                                           , [true , true , true , true ] ) ,
                ( P::execute_compute(INGEST_AUDIENCES_REPORT_ID)                                          , [true , true , true , true ] ) ,
                ( P::retrieve_compute_result(INGEST_AUDIENCES_REPORT_ID)                                  , [true , true , true , true ] ) ,

                ( P::execute_compute(&get_container_log_node_id(INGEST_DEMOGRAPHICS_ID))                  , [true , true , true , true ] ) ,
                ( P::retrieve_compute_result(&get_container_log_node_id(INGEST_DEMOGRAPHICS_ID))          , [true , true , true , true ] ) ,
                ( P::execute_compute(INGEST_DEMOGRAPHICS_ID)                                              , [true , true , true , true ] ) ,
                ( P::retrieve_compute_result(INGEST_DEMOGRAPHICS_ID)                                      , [true , true , true , true ] ) ,

                ( P::execute_compute(&get_container_log_node_id(INGEST_EMBEDDINGS_ID))                    , [true , true , true , true ] ) ,
                ( P::retrieve_compute_result(&get_container_log_node_id(INGEST_EMBEDDINGS_ID))            , [true , true , true , true ] ) ,
                ( P::execute_compute(INGEST_EMBEDDINGS_ID)                                                , [true , true , true , true ] ) ,
                ( P::retrieve_compute_result(INGEST_EMBEDDINGS_ID)                                        , [true , true , true , true ] ) ,

                ( P::execute_compute(&get_container_log_node_id(INGEST_SEGMENTS_ID))                      , [true , true , true , true ] ) ,
                ( P::retrieve_compute_result(&get_container_log_node_id(INGEST_SEGMENTS_ID))              , [true , true , true , true ] ) ,
                ( P::execute_compute(INGEST_SEGMENTS_ID)                                                  , [true , true , true , true ] ) ,
                ( P::retrieve_compute_result(INGEST_SEGMENTS_ID)                                          , [true , true , true , true ] ) ,

                ( P::execute_compute(&get_container_log_node_id(OVERLAP_BASIC_ID))                        , [true , true , true , true ] ) ,
                ( P::retrieve_compute_result(&get_container_log_node_id(OVERLAP_BASIC_ID))                , [true , true , true , true ] ) ,
                ( P::execute_compute(OVERLAP_BASIC_ID)                                                    , [true , true , true , true ] ) ,
                ( P::retrieve_compute_result(OVERLAP_BASIC_ID)                                            , [true , true , true , true ] ) ,

                ( P::execute_compute(&get_container_log_node_id(CONSENTLESS_OVERLAP_INSIGHTS_ID))         , [true , true , true , true ] ) ,
                ( P::retrieve_compute_result(&get_container_log_node_id(CONSENTLESS_OVERLAP_INSIGHTS_ID)) , [true , true , true , true ] ) ,
                ( P::execute_compute(&get_container_log_node_id(MODELLED_AUDIENCE_INSIGHTS_ID))           , [true , true , true , true ] ) ,
                ( P::retrieve_compute_result(&get_container_log_node_id(MODELLED_AUDIENCE_INSIGHTS_ID))   , [true , true , true , true ] ) ,
            ]);
        }

        // [Advertiser, Publisher, Observer, Agency]
        self.add_permissions(vec![
            ( P::retrieve_data_room()                                                                        , [true , true , true , true ] ) ,
            ( P::retrieve_published_datasets()                                                               , [true , true , true , true ] ) ,
            ( P::update_data_room_status()                                                                   , [true , true , __   , true ] ) ,
            ( P::execute_compute(CONSENTLESS_OVERLAP_INSIGHTS_ID)                                            , [true , true , true , true ] ) ,
            ( P::retrieve_compute_result(CONSENTLESS_OVERLAP_INSIGHTS_ID)                                    , [true , true , true , true ] ) ,
            ( P::execute_compute(COMPUTE_AUDIENCE_SIZES_ID)                                                  , [true , true , true , true ] ) ,
            ( P::retrieve_compute_result(COMPUTE_AUDIENCE_SIZES_ID)                                          , [true , __   , __   , true ] ) ,
            ( P::execute_compute(MODELLED_AUDIENCE_INSIGHTS_ID)                                              , [true , __   , __   , true ] ) ,
            ( P::retrieve_compute_result(MODELLED_AUDIENCE_INSIGHTS_ID)                                      , [true , __   , __   , true ] ) ,
            ( P::execute_compute(VIEW_ACTIVATED_AUDIENCES_ID)                                                , [true , __   , __   , true ] ) ,
            ( P::retrieve_compute_result(VIEW_ACTIVATED_AUDIENCES_ID)                                        , [true , __   , __   , true ] ) ,
            ( P::execute_compute(MODELLED_AUDIENCE_INSIGHTS_VIEW_ID)                                         , [__   , true , __   , __   ] ) ,
            ( P::retrieve_compute_result(MODELLED_AUDIENCE_INSIGHTS_VIEW_ID)                                 , [__   , true , __   , __   ] ) ,
            ( P::execute_compute(GET_LOOKALIKE_AUDIENCE_ID)                                                  , [__   , true , __   , __   ] ) ,
            ( P::retrieve_compute_result(GET_LOOKALIKE_AUDIENCE_ID)                                          , [__   , true , __   , __   ] ) ,
            ( P::execute_compute(VIEW_PUBLISHED_ACTIVATED_AUDIENCES_ID)                                      , [__   , true , __   , __   ] ) ,
            ( P::retrieve_compute_result(VIEW_PUBLISHED_ACTIVATED_AUDIENCES_ID)                              , [__   , true , __   , __   ] ) ,
            ( P::leaf_crud(ACTIVATED_AUDIENCES_CONFIG_ID)                                                    , [true , __   , __   , true ] ) ,
            ( P::leaf_crud(DATASET_AUDIENCES_ID)                                                             , [true , __   , __   , __   ] ) ,
            ( P::execute_compute(&validation::v2::get_validation_report_id(DATASET_AUDIENCES_ID))            , [true , __   , __   , __   ] ) ,
            ( P::retrieve_compute_result(&validation::v2::get_validation_report_id(DATASET_AUDIENCES_ID))    , [true , __   , __   , __   ] ) ,
            ( P::leaf_crud(DATASET_MATCHING_ID)                                                              , [__   , true , __   , __   ] ) ,
            ( P::leaf_crud(DATASET_SEGMENTS_ID)                                                              , [__   , true , __   , __   ] ) ,
            ( P::leaf_crud(DATASET_DEMOGRAPHICS_ID)                                                          , [__   , true , __   , __   ] ) ,
            ( P::leaf_crud(DATASET_EMBEDDINGS_ID)                                                            , [__   , true , __   , __   ] ) ,
            ( P::execute_compute(INGEST_AUDIENCES_REPORT_ID)                                                 , [true , __ , __ , true ] ) ,
            ( P::retrieve_compute_result(INGEST_AUDIENCES_REPORT_ID)                                         , [true , __ , __ , true ] ) ,
        ]);

        if self.enable_audit_log_retrieval() {
            self.add_permissions(vec![
                //                       , [ Adve , Publ , Obse , Agen ]
                (P::retrieve_audit_log() , [true  , true , true , true]) ,
            ]);
        }

        if self.enable_dev_computations() {
            self.add_permissions(vec![
                //                        , [ Adve , Publ , Obse  , Agen ]
                (P::execute_dev_compute() , [false , true , false , false]) ,
            ]);
        }

        self.configuration_elements.push(ConfigurationElement {
            id: "authentication_method".into(),
            element: Some(configuration_element::Element::AuthenticationMethod(
                AuthenticationMethod {
                    personal_pki: None,
                    dq_pki: Some(PkiPolicy {
                        root_certificate_pem: self
                            .data_room
                            .authentication_root_certificate_pem
                            .as_bytes()
                            .to_vec(),
                    }),
                    dcr_secret: None,
                },
            )),
        });

        Ok(())
    }

    fn add_overlap_insights_node(&mut self) -> CompileResult<()> {
        let script_id = get_script_id(CONSENTLESS_OVERLAP_INSIGHTS_ID);

        self.configuration_elements.push(ConfigurationElement {
            id: script_id.clone(),
            element: Some(configuration_element::Element::ComputeNode(ComputeNode {
                node_name: script_id.clone(),
                node: Some(compute_node::Node::Branch(ComputeNodeBranch {
                    config: prost::Message::encode_length_delimited_to_vec(&DriverTaskConfig {
                        driver_task_config: Some(driver_task_config::DriverTaskConfig::StaticContent(
                            StaticContentConfig { content: CONSENTLESS_OVERLAP_INSIGHTS_PY.to_vec() },
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

        self.configuration_elements.push(
            ContainerNode {
                id: CONSENTLESS_OVERLAP_INSIGHTS_ID.into(),
                main_script_path: "/input/run.py",
                mount_points: vec![
                    MountPoint { path: "run.py".into(), dependency: script_id.into() },
                    MountPoint { path: COMPUTE_RELEVANT_USERS_ID.into(), dependency: COMPUTE_RELEVANT_USERS_ID.into() },
                    MountPoint { path: INGEST_AUDIENCES_ID.into(), dependency: INGEST_AUDIENCES_ID.into() },
                    MountPoint { path: INGEST_MATCHING_ID.into(), dependency: INGEST_MATCHING_ID.into() },
                    MountPoint { path: INGEST_DEMOGRAPHICS_ID.into(), dependency: INGEST_DEMOGRAPHICS_ID.into() },
                    MountPoint { path: INGEST_SEGMENTS_ID.into(), dependency: INGEST_SEGMENTS_ID.into() },
                    MountPoint { path: DQ_MEDIA_DCR_FILE.into(), dependency: DQ_MEDIA_DCR_ID.into() },
                ],
                python_attestation_specification_id: &self.python_attestation_specification_id,
                python_protocol_version: self.python_protocol_version,
                memory_allocation_strategy: MemoryAllocationStrategy::SqlOptimized,
                additional_dependencies: vec![],
                rate_limiting: None,
            }
            .into(),
        );

        Ok(())
    }

    fn add_container_log_node(&mut self, id: &str) -> CompileResult<()> {
        let container_log_id = get_container_log_node_id(id);
        self.configuration_elements.push(ConfigurationElement {
            id: container_log_id.clone(),
            element: Some(configuration_element::Element::ComputeNode(ComputeNode {
                node_name: container_log_id.clone(),
                node: Some(compute_node::Node::Branch(ComputeNodeBranch {
                    config: prost::Message::encode_length_delimited_to_vec(&ContainerWorkerConfiguration {
                        configuration: Some(container_worker_configuration::Configuration::Static(StaticImage {
                            command: vec![
                                "cp".to_string(),
                                "/input/upstream/container.log".to_string(),
                                "/output/container.log".to_string(),
                            ],
                            mount_points: vec![MountPoint { path: "upstream".into(), dependency: id.into() }],
                            output_path: "/output".into(),
                            include_container_logs_on_error: true,
                            include_container_logs_on_success: true,
                            minimum_container_memory_size: None,
                            extra_chunk_cache_size_to_available_memory_ratio: None,
                        })),
                    }),
                    dependencies: vec![id.to_string()],
                    output_format: ComputeNodeFormat::Zip as i32,
                    protocol: Some(ComputeNodeProtocol { version: self.python_protocol_version }),
                    attestation_specification_id: self.python_attestation_specification_id.clone(),
                })),
                rate_limiting: None,
            })),
        });

        Ok(())
    }

    fn add_report_node(&mut self, upstream_id: &str, report_node_id: &str) -> CompileResult<()> {
        self.configuration_elements.push(ConfigurationElement {
            id: report_node_id.to_string(),
            element: Some(configuration_element::Element::ComputeNode(ComputeNode {
                node_name: report_node_id.to_string(),
                node: Some(compute_node::Node::Branch(ComputeNodeBranch {
                    config: prost::Message::encode_length_delimited_to_vec(&ContainerWorkerConfiguration {
                        configuration: Some(container_worker_configuration::Configuration::Static(StaticImage {
                            command: vec![
                                "cp".to_string(),
                                "/input/upstream/report.json".to_string(),
                                "/output/report.json".to_string(),
                            ],
                            mount_points: vec![MountPoint { path: "upstream".into(), dependency: upstream_id.into() }],
                            output_path: "/output".into(),
                            include_container_logs_on_error: true,
                            include_container_logs_on_success: true,
                            minimum_container_memory_size: None,
                            extra_chunk_cache_size_to_available_memory_ratio: None,
                        })),
                    }),
                    dependencies: vec![upstream_id.to_string()],
                    output_format: ComputeNodeFormat::Zip as i32,
                    protocol: Some(ComputeNodeProtocol { version: self.python_protocol_version }),
                    attestation_specification_id: self.python_attestation_specification_id.clone(),
                })),
                rate_limiting: None,
            })),
        });

        Ok(())
    }

    fn add_score_users_node(&mut self) -> CompileResult<()> {
        let script_id = get_script_id(SCORE_USERS_ID);
        self.configuration_elements.push(
            StaticContentNode {
                id: &script_id,
                content: SCORE_USERS_PY,
                driver_protocol_version: self.driver_protocol_version,
                driver_attestation_specification_id: &self.driver_attestation_specification_id,
            }
            .into(),
        );

        self.configuration_elements.push(
            ContainerNode {
                id: SCORE_USERS_ID,
                main_script_path: "/input/run.py",
                mount_points: vec![
                    MountPoint { path: "run.py".into(), dependency: script_id.into() },
                    MountPoint { path: INGEST_DEMOGRAPHICS_ID.into(), dependency: INGEST_DEMOGRAPHICS_ID.into() },
                    MountPoint { path: INGEST_SEGMENTS_ID.into(), dependency: INGEST_SEGMENTS_ID.into() },
                    MountPoint { path: INGEST_EMBEDDINGS_ID.into(), dependency: INGEST_EMBEDDINGS_ID.into() },
                    MountPoint { path: COMPUTE_RELEVANT_USERS_ID.into(), dependency: COMPUTE_RELEVANT_USERS_ID.into() },
                    MountPoint { path: INGEST_MATCHING_ID.into(), dependency: INGEST_MATCHING_ID.into() },
                    MountPoint { path: OVERLAP_BASIC_ID.into(), dependency: OVERLAP_BASIC_ID.to_string() },
                    MountPoint { path: DQ_MEDIA_DCR_FILE.into(), dependency: DQ_MEDIA_DCR_ID.into() },
                ],
                python_attestation_specification_id: &self.python_attestation_specification_id,
                python_protocol_version: self.python_protocol_version,
                memory_allocation_strategy: MemoryAllocationStrategy::PythonOptimized,
                additional_dependencies: vec![],
                rate_limiting: None,
            }
            .into(),
        );

        Ok(())
    }

    fn add_create_activated_audiences_node(&mut self) -> CompileResult<()> {
        let script_node_id = get_script_id(CREATE_ACTIVATED_AUDIENCES_ID);
        self.configuration_elements.push(
            StaticContentNode {
                id: &script_node_id,
                content: CREATE_ACTIVATED_AUDIENCES_PY,
                driver_protocol_version: self.driver_protocol_version,
                driver_attestation_specification_id: &self.driver_attestation_specification_id,
            }
            .into(),
        );
        self.configuration_elements.push(
            ContainerNode {
                id: CREATE_ACTIVATED_AUDIENCES_ID,
                main_script_path: "/input/run.py",
                mount_points: vec![
                    MountPoint { path: "run.py".to_string(), dependency: script_node_id.clone() },
                    MountPoint {
                        path: ACTIVATED_AUDIENCES_CONFIG_ID.into(),
                        dependency: ACTIVATED_AUDIENCES_CONFIG_ID.into(),
                    },
                    MountPoint { path: SCORE_USERS_ID.into(), dependency: SCORE_USERS_ID.into() },
                    MountPoint { path: DQ_MEDIA_DCR_FILE.into(), dependency: DQ_MEDIA_DCR_ID.into() },
                ],
                python_attestation_specification_id: &self.python_attestation_specification_id,
                python_protocol_version: self.python_protocol_version,
                memory_allocation_strategy: MemoryAllocationStrategy::PythonOptimized,
                additional_dependencies: vec![],
                rate_limiting: None,
            }
            .into(),
        );

        Ok(())
    }

    fn add_get_lookalike_audience_node(&mut self) -> CompileResult<()> {
        let script_node_id = get_script_id(GET_LOOKALIKE_AUDIENCE_ID);
        self.configuration_elements.push(
            StaticContentNode {
                id: &script_node_id,
                content: GET_LOOKALIKE_AUDIENCES_PY,
                driver_protocol_version: self.driver_protocol_version,
                driver_attestation_specification_id: &self.driver_attestation_specification_id,
            }
            .into(),
        );

        // Via this node the publisher requests which user list should be extracted.
        self.configuration_elements.push(ConfigurationElement {
            id: REQUESTED_AUDIENCE_CONFIG_ID.into(),
            element: Some(configuration_element::Element::ComputeNode(ComputeNode {
                node_name: REQUESTED_AUDIENCE_CONFIG_ID.into(),
                rate_limiting: None,
                node: Some(compute_node::Node::Parameter(ComputeNodeParameter { is_required: true })),
            })),
        });

        self.configuration_elements.push(
            ContainerNode {
                id: GET_LOOKALIKE_AUDIENCE_ID,
                main_script_path: "/input/run.py",
                mount_points: vec![
                    MountPoint { path: "run.py".to_string(), dependency: script_node_id.clone() },
                    MountPoint {
                        path: ACTIVATED_AUDIENCES_CONFIG_ID.into(),
                        dependency: ACTIVATED_AUDIENCES_CONFIG_ID.into(),
                    },
                    MountPoint {
                        path: REQUESTED_AUDIENCE_CONFIG_ID.into(),
                        dependency: REQUESTED_AUDIENCE_CONFIG_ID.into(),
                    },
                    MountPoint {
                        path: CREATE_ACTIVATED_AUDIENCES_ID.into(),
                        dependency: CREATE_ACTIVATED_AUDIENCES_ID.into(),
                    },
                    MountPoint { path: DQ_MEDIA_DCR_FILE.into(), dependency: DQ_MEDIA_DCR_ID.into() },
                ],
                python_attestation_specification_id: &self.python_attestation_specification_id,
                python_protocol_version: self.python_protocol_version,
                memory_allocation_strategy: MemoryAllocationStrategy::PythonOptimized,
                additional_dependencies: vec![],
                rate_limiting: None,
            }
            .into(),
        );

        Ok(())
    }

    fn add_modelled_audience_insight_nodes(&mut self) -> CompileResult<()> {
        let audience_insights_script_id = get_script_id(MODELLED_AUDIENCE_INSIGHTS_ID);

        self.configuration_elements.push(
            StaticContentNode {
                id: &audience_insights_script_id,
                content: MODELLED_AUDIENCE_INSIGHTS_PY,
                driver_protocol_version: self.driver_protocol_version,
                driver_attestation_specification_id: &self.driver_attestation_specification_id,
            }
            .into(),
        );

        self.configuration_elements.push(
            ContainerNode {
                id: MODELLED_AUDIENCE_INSIGHTS_ID,
                main_script_path: "/input/run.py",
                mount_points: vec![
                    MountPoint { path: "run.py".to_string(), dependency: audience_insights_script_id.clone() },
                    MountPoint {
                        path: CREATE_ACTIVATED_AUDIENCES_ID.into(),
                        dependency: CREATE_ACTIVATED_AUDIENCES_ID.into(),
                    },
                    MountPoint { path: INGEST_SEGMENTS_ID.into(), dependency: INGEST_SEGMENTS_ID.into() },
                    MountPoint { path: INGEST_DEMOGRAPHICS_ID.into(), dependency: INGEST_DEMOGRAPHICS_ID.into() },
                    MountPoint { path: COMPUTE_RELEVANT_USERS_ID.into(), dependency: COMPUTE_RELEVANT_USERS_ID.into() },
                    MountPoint { path: DQ_MEDIA_DCR_FILE.into(), dependency: DQ_MEDIA_DCR_ID.into() },
                ],
                python_attestation_specification_id: &self.python_attestation_specification_id,
                python_protocol_version: self.python_protocol_version,
                memory_allocation_strategy: MemoryAllocationStrategy::SqlOptimized,
                additional_dependencies: vec![],
                rate_limiting: None,
            }
            .into(),
        );

        let view_audience_insights_script_id = get_script_id(MODELLED_AUDIENCE_INSIGHTS_VIEW_ID);
        self.configuration_elements.push(
            StaticContentNode {
                id: &view_audience_insights_script_id,
                content: MODELLED_AUDIENCE_INSIGHTS_VIEW_PY,
                driver_protocol_version: self.driver_protocol_version,
                driver_attestation_specification_id: &self.driver_attestation_specification_id,
            }
            .into(),
        );
        self.configuration_elements.push(
            ContainerNode {
                id: MODELLED_AUDIENCE_INSIGHTS_VIEW_ID,
                main_script_path: "/input/run.py",
                mount_points: vec![
                    MountPoint { path: "run.py".to_string(), dependency: view_audience_insights_script_id.clone() },
                    MountPoint {
                        path: MODELLED_AUDIENCE_INSIGHTS_ID.into(),
                        dependency: MODELLED_AUDIENCE_INSIGHTS_ID.to_string(),
                    },
                    MountPoint {
                        path: ACTIVATED_AUDIENCES_CONFIG_ID.into(),
                        dependency: ACTIVATED_AUDIENCES_CONFIG_ID.into(),
                    },
                ],
                python_attestation_specification_id: &self.python_attestation_specification_id,
                python_protocol_version: self.python_protocol_version,
                memory_allocation_strategy: MemoryAllocationStrategy::PythonOptimized,
                additional_dependencies: vec![],
                rate_limiting: None,
            }
            .into(),
        );

        Ok(())
    }

    fn add_activated_audiences_nodes(&mut self) -> CompileResult<()> {
        let view_activated_audiences_script_id = get_script_id(VIEW_ACTIVATED_AUDIENCES_ID);

        self.configuration_elements.push(
            StaticContentNode {
                id: &view_activated_audiences_script_id,
                content: VIEW_ACTIVATED_AUDIENCES_PY,
                driver_protocol_version: self.driver_protocol_version,
                driver_attestation_specification_id: &self.driver_attestation_specification_id,
            }
            .into(),
        );
        self.configuration_elements.push(
            ContainerNode {
                id: VIEW_ACTIVATED_AUDIENCES_ID,
                main_script_path: "/input/run.py",
                mount_points: vec![
                    MountPoint { path: "run.py".into(), dependency: view_activated_audiences_script_id.into() },
                    MountPoint {
                        path: ACTIVATED_AUDIENCES_CONFIG_ID.into(),
                        dependency: ACTIVATED_AUDIENCES_CONFIG_ID.into(),
                    },
                ],
                python_attestation_specification_id: &self.python_attestation_specification_id,
                python_protocol_version: self.python_protocol_version,
                memory_allocation_strategy: MemoryAllocationStrategy::PythonOptimized,
                additional_dependencies: vec![],
                rate_limiting: None,
            }
            .into(),
        );

        let view_published_activated_audiences_script_id = get_script_id(VIEW_PUBLISHED_ACTIVATED_AUDIENCES_ID);

        self.configuration_elements.push(
            StaticContentNode {
                id: &view_published_activated_audiences_script_id,
                content: VIEW_PUBLISHED_ACTIVATED_AUDIENCES_PY,
                driver_protocol_version: self.driver_protocol_version,
                driver_attestation_specification_id: &self.driver_attestation_specification_id,
            }
            .into(),
        );
        self.configuration_elements.push(
            ContainerNode {
                id: VIEW_PUBLISHED_ACTIVATED_AUDIENCES_ID,
                main_script_path: "/input/view.py",
                mount_points: vec![
                    MountPoint {
                        path: "view.py".into(),
                        dependency: view_published_activated_audiences_script_id.to_string(),
                    },
                    MountPoint {
                        path: ACTIVATED_AUDIENCES_CONFIG_ID.into(),
                        dependency: ACTIVATED_AUDIENCES_CONFIG_ID.into(),
                    },
                ],
                python_attestation_specification_id: &self.python_attestation_specification_id,
                python_protocol_version: self.python_protocol_version,
                memory_allocation_strategy: MemoryAllocationStrategy::PythonOptimized,
                additional_dependencies: vec![],
                rate_limiting: None,
            }
            .into(),
        );

        let compute_audiences_sizes_script = get_script_id(COMPUTE_AUDIENCE_SIZES_ID);

        self.configuration_elements.push(
            StaticContentNode {
                id: &compute_audiences_sizes_script,
                content: COMPUTE_AUDIENCE_SIZES_PY,
                driver_protocol_version: self.driver_protocol_version,
                driver_attestation_specification_id: &self.driver_attestation_specification_id,
            }
            .into(),
        );
        self.configuration_elements.push(
            ContainerNode {
                id: COMPUTE_AUDIENCE_SIZES_ID,
                main_script_path: "/input/run.py",
                mount_points: vec![
                    MountPoint { path: "run.py".into(), dependency: compute_audiences_sizes_script.into() },
                    MountPoint { path: SCORE_USERS_ID.into(), dependency: SCORE_USERS_ID.into() },
                    MountPoint { path: DQ_MEDIA_DCR_FILE.into(), dependency: DQ_MEDIA_DCR_ID.into() },
                ],
                python_attestation_specification_id: &self.python_attestation_specification_id,
                python_protocol_version: self.python_protocol_version,
                memory_allocation_strategy: MemoryAllocationStrategy::PythonOptimized,
                additional_dependencies: vec![],
                rate_limiting: None,
            }
            .into(),
        );

        Ok(())
    }

    pub fn enable_audit_log_retrieval(&self) -> bool {
        self.features.contains(&ENABLE_AUDIT_LOG_RETRIEVAL.to_string())
    }

    pub fn enable_rate_limiting_on_publish_dataset(&self) -> bool {
        self.features.contains(&ENABLE_RATE_LIMITING_ON_PUBLISH_DATASET.to_string())
    }

    pub fn enable_dev_computations(&self) -> bool {
        self.features.contains(&ENABLE_DEV_COMPUTATIONS.to_string())
    }

    pub fn matching_id_format_type(&self) -> FormatType {
        apply_hashing_algorithm_type_to_format(
            &self.data_room.matching_id_format,
            self.data_room.hash_matching_id_with.as_ref(),
        )
    }
}

pub fn advertiser_validation_config(format_type: &FormatType) -> CompileResult<ValidationConfig> {
    let validation_columns = vec![
        ColumnValidationV0 {
            name: Some("matching_id".to_string()),
            format_type: format_type.clone(),
            allow_null: false,
            hash_with: None,
            in_range: None,
        },
        ColumnValidationV0 {
            name: Some("audience_type".to_string()),
            format_type: FormatType::String,
            allow_null: false,
            hash_with: None,
            in_range: None,
        },
    ];
    let config = ValidationConfig::V0(ValidationConfigV0 {
        columns: validation_columns,
        table: Some(TableValidationV0 { uniqueness: None, allow_empty: None, num_rows: None }),
    });
    Ok(config)
}

struct StaticContentNode<'a, 'b, 'c> {
    id: &'a str,
    content: &'b [u8],
    driver_protocol_version: u32,
    driver_attestation_specification_id: &'c String,
}

impl Into<ConfigurationElement> for StaticContentNode<'_, '_, '_> {
    fn into(self) -> ConfigurationElement {
        ConfigurationElement {
            id: self.id.to_string(),
            element: Some(configuration_element::Element::ComputeNode(ComputeNode {
                node_name: self.id.to_string(),
                node: Some(compute_node::Node::Branch(ComputeNodeBranch {
                    config: prost::Message::encode_length_delimited_to_vec(&DriverTaskConfig {
                        driver_task_config: Some(driver_task_config::DriverTaskConfig::StaticContent(
                            StaticContentConfig { content: self.content.to_vec() },
                        )),
                    }),
                    dependencies: vec![],
                    output_format: ComputeNodeFormat::Raw as i32,
                    protocol: Some(ComputeNodeProtocol { version: self.driver_protocol_version }),
                    attestation_specification_id: self.driver_attestation_specification_id.clone(),
                })),
                rate_limiting: None,
            })),
        }
    }
}

pub enum MemoryAllocationStrategy {
    SqlOptimized,
    PythonOptimized,
}

struct ContainerNode<'a, 'b, 'c> {
    id: &'a str,
    main_script_path: &'b str,
    mount_points: Vec<MountPoint>,
    python_attestation_specification_id: &'c String,
    python_protocol_version: u32,
    memory_allocation_strategy: MemoryAllocationStrategy,
    additional_dependencies: Vec<String>,
    rate_limiting: Option<RateLimitingConfig>,
}

impl Into<ConfigurationElement> for ContainerNode<'_, '_, '_> {
    fn into(self) -> ConfigurationElement {
        let dependencies = self
            .mount_points
            .iter()
            .map(|mp| mp.dependency.clone())
            .chain(self.additional_dependencies.into_iter())
            .collect();
        let (minimum_container_memory_size, extra_chunk_cache_size_to_available_memory_ratio) =
            match self.memory_allocation_strategy {
                MemoryAllocationStrategy::SqlOptimized => (Some(2048 * 1024 * 1024), Some(1.0)),
                MemoryAllocationStrategy::PythonOptimized => (None, None),
            };
        ConfigurationElement {
            id: self.id.to_string(),
            element: Some(configuration_element::Element::ComputeNode(ComputeNode {
                node_name: self.id.to_string(),
                node: Some(compute_node::Node::Branch(ComputeNodeBranch {
                    config: prost::Message::encode_length_delimited_to_vec(&ContainerWorkerConfiguration {
                        configuration: Some(container_worker_configuration::Configuration::Static(StaticImage {
                            command: ["python3", &self.main_script_path]
                                .iter()
                                .map(|s| s.to_string())
                                .collect::<Vec<_>>(),
                            mount_points: self.mount_points,
                            output_path: "/output".into(),
                            include_container_logs_on_error: DEBUG,
                            include_container_logs_on_success: DEBUG,
                            minimum_container_memory_size,
                            extra_chunk_cache_size_to_available_memory_ratio,
                        })),
                    }),
                    dependencies,
                    output_format: ComputeNodeFormat::Zip as i32,
                    protocol: Some(ComputeNodeProtocol { version: self.python_protocol_version }),
                    attestation_specification_id: self.python_attestation_specification_id.clone(),
                })),
                rate_limiting: self.rate_limiting,
            })),
        }
    }
}

struct P;
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

    fn execute_dev_compute() -> permission::Permission {
        permission::Permission::ExecuteDevelopmentComputePermission(ExecuteDevelopmentComputePermission {})
    }
}

fn get_script_id(id: &str) -> String {
    let script_node_id = format!("{}_script.py", id);
    script_node_id
}

fn get_container_log_node_id(id: &str) -> String {
    format!("{}_container_log", id)
}
