use std::iter::FromIterator;

use delta_attestation_api::*;
use delta_container_worker_api::*;
use delta_data_room_api::*;
use delta_gcg_driver_api::*;
use schemars::JsonSchema;
use serde::Deserialize;
use serde::Serialize;
use validation_config::ValidationConfig;

use super::v0;
use crate::media::v1;
use crate::media::v1::ActivationTypeV1;
use crate::media::v1::ColumnTypeV1;
use crate::media::v1::EnclaveSpecificationV1;
use crate::*;

pub type ActivationTypeV2 = v0::ActivationType;
pub type EnclaveSpecificationV2 = v0::EnclaveSpecification;
pub type MediaDataRoomConfigV2 = v0::MediaDataRoomConfig;
pub type MediaAuxiliaryStateV2 = v0::MediaAuxiliaryStateV0;
pub type DirectActivationConfigV2 = v0::DirectActivationConfigV0;
pub type CalculateOverlapInsightsParams = v0::CalculateOverlapInsightsParams;

pub const OVERLAP_BASIC_ID: &str = v0::OVERLAP_BASIC_ID;
pub const OVERLAP_INSIGHTS_ID: &str = v0::OVERLAP_INSIGHTS_ID;

pub const OVERLAP_BASIC_PY: &[u8] = include_bytes!("../v2/overlap_basic.py");
pub const DIRECT_ACTIVATION_ALL_PY: &[u8] = include_bytes!("../v2/direct_activation_all.py");
pub const DIRECT_ACTIVATION_PY: &[u8] = include_bytes!("../v2/direct_activation.py");
pub const CONSENTLESS_OVERLAP_INSIGHTS_PY: &[u8] = include_bytes!("../v2/consentless_overlap_insights.py");

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct MediaDataRoomV2 {
    pub id: String,
    pub name: String,
    pub main_publisher_email: String,
    pub main_advertiser_email: String,
    pub publisher_emails: Vec<String>,
    pub advertiser_emails: Vec<String>,
    pub observer_emails: Vec<String>,
    pub agency_emails: Vec<String>,

    pub publisher_schema: Vec<ColumnTypeV1>,
    pub advertiser_schema: Vec<ColumnTypeV1>,

    pub activation_type: Option<ActivationTypeV1>,
    pub enable_download_by_publisher: bool,
    pub enable_download_by_advertiser: bool,
    pub enable_download_by_agency: bool,
    pub enable_overlap_insights: bool,
    pub enable_audit_log_retrieval: bool,
    pub enable_dev_computations: bool,

    pub authentication_root_certificate_pem: String,
    pub driver_enclave_specification: EnclaveSpecificationV1,
    pub python_enclave_specification: EnclaveSpecificationV1,

    pub publisher_validation: ValidationConfig,
    pub advertiser_validation: ValidationConfig,
}

struct MediaDataRoomCompilerV2<'a> {
    data_room: &'a MediaDataRoomV2,
    driver_attestation_specification_id: String,
    python_attestation_specification_id: String,
    driver_protocol_version: u32,
    python_protocol_version: u32,
    configuration_elements: Vec<ConfigurationElement>,
    permissions_advertiser: Vec<Permission>,
    permissions_publisher: Vec<Permission>,
    permissions_observer: Vec<Permission>,
    permissions_agency: Vec<Permission>,
}

pub fn compile_media_data_room_v2(data_room: &MediaDataRoomV2) -> Result<DataRoom, CompileError> {
    MediaDataRoomCompilerV2::new(data_room).compile()
}

fn data_room_to_data_room_config(data_room: &MediaDataRoomV2) -> CompileResult<MediaDataRoomConfigV2> {
    let mut publisher_column_names = vec![];
    let mut segment_column_name = None;
    let mut activation_id_column_name = None;
    for column in &data_room.publisher_schema {
        let column_name = match column {
            ColumnTypeV1::MatchingId => "m:matching_id".to_string(),
            ColumnTypeV1::AudienceType => {
                return Err("AudienceType column not expected in publisher schema")?;
            }
            ColumnTypeV1::ActivationId => {
                if activation_id_column_name.is_some() {
                    return Err("Multiple Activation ID columns in publisher schema")?;
                }
                let column_name = "i:activation_id".to_string();
                activation_id_column_name = Some(column_name.clone());
                column_name
            }
            ColumnTypeV1::Segment => {
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
            ColumnTypeV1::MatchingId => "m:matching_id".to_string(),
            ColumnTypeV1::AudienceType => {
                if audience_type_column_name.is_some() {
                    return Err("Multiple AudienceType columns in advertiser schema")?;
                }
                let column_name = "a:audience_type".to_string();
                audience_type_column_name = Some(column_name.clone());
                column_name
            }
            ColumnTypeV1::Segment => {
                return Err("Segment column not expected in advertiser schema")?;
            }
            ColumnTypeV1::ActivationId => {
                return Err("ActivationId column not expected in advertiser schema")?;
            }
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

    Ok(MediaDataRoomConfigV2 {
        advertiser_column_names,
        publisher_column_names,
        matching_columns,
        audience_type_column_name,
        segment_column_name,
        activation_id_column_name,
        rounding_decimals_count: -2,
        rounding_decimals_ratio: 3,
        cutoff_overlap_basic_segment: 100,
        cutoff_consentless_overlap_insights_unmatched_audience_type: 100,
        cutoff_consentless_overlap_insights_unmatched_segment: 100,
        cutoff_consentless_overlap_insights_matched_audience_type: 100,
        cutoff_consentless_overlap_insights_matched_segment_audience_type: 0,
    })
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

// This is for clarity in add_permissions
#[allow(non_upper_case_globals)]
const __: bool = false;

impl<'a> MediaDataRoomCompilerV2<'a> {
    pub fn new(data_room: &'a MediaDataRoomV2) -> Self {
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
            permissions_agency: vec![],
        }
    }

    pub fn compile(mut self) -> CompileResult<DataRoom> {
        self.add_common_nodes()?;
        match &self.data_room.activation_type {
            None => {}
            Some(ActivationTypeV2::Direct) => {
                self.add_direct_activation_nodes()?;
            }
            Some(ActivationTypeV2::Consentless) => {
                self.add_consentless_activation_nodes()?;
            }
        }

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

        for (dataset_name, validation_config) in [
            ("dataset_advertiser", &self.data_room.advertiser_validation),
            ("dataset_publisher", &self.data_room.publisher_validation),
        ] {
            self.configuration_elements.push(ConfigurationElement {
                id: dataset_name.into(),
                element: Some(configuration_element::Element::ComputeNode(ComputeNode {
                    node_name: dataset_name.into(),
                    rate_limiting: None,
                    node: Some(compute_node::Node::Leaf(ComputeNodeLeaf { is_required: true })),
                })),
            });

            crate::validation::v0::add_nodes_for_validation(
                &mut self.configuration_elements, dataset_name, dataset_name, &validation_config,
                &self.driver_attestation_specification_id, self.data_room.driver_enclave_specification.worker_protocol,
                &self.python_attestation_specification_id, self.data_room.python_enclave_specification.worker_protocol,
            )?;
        }

        self.configuration_elements.push(ConfigurationElement {
            id: "overlap_basic_script".into(),
            element: Some(configuration_element::Element::ComputeNode(ComputeNode {
                node_name: "overlap_basic_script".into(),
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
        let config = data_room_to_data_room_config(self.data_room)?;
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
                                    path: "dataset_advertiser".into(),
                                    dependency: validation::v0::get_validation_check_id("dataset_advertiser"),
                                },
                                MountPoint {
                                    path: "dataset_publisher".into(),
                                    dependency: validation::v0::get_validation_check_id("dataset_publisher"),
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
                        validation::v0::get_validation_check_id("dataset_advertiser"),
                        validation::v0::get_validation_check_id("dataset_publisher"),
                    ],
                    output_format: ComputeNodeFormat::Zip as i32,
                    protocol: Some(ComputeNodeProtocol { version: self.python_protocol_version }),
                    attestation_specification_id: self.python_attestation_specification_id.clone(),
                })),
                rate_limiting: None,
            })),
        });

        self.add_permissions(vec![
            //                                             [ Adve, Publ, Obse, Agen ]
            (P::retrieve_data_room(), [true, true, true, true]),
            (P::retrieve_published_datasets(), [true, true, true, true]),
            (P::execute_compute(&validation::v0::get_validation_report_id("dataset_advertiser")), [true, __, __, __]),
            (P::retrieve_compute_result(&validation::v0::get_validation_report_id("dataset_advertiser")), [
                true, __, __, __,
            ]),
            (P::execute_compute(&validation::v0::get_validation_report_id("dataset_publisher")), [__, true, __, __]),
            (P::retrieve_compute_result(&validation::v0::get_validation_report_id("dataset_publisher")), [
                __, true, __, __,
            ]),
            (P::update_data_room_status(), [true, true, __, true]),
            (P::leaf_crud("dataset_advertiser"), [true, __, __, __]),
            (P::leaf_crud("dataset_publisher"), [__, true, __, __]),
            (P::execute_compute(OVERLAP_BASIC_ID), [true, true, true, true]),
            (P::retrieve_compute_result(OVERLAP_BASIC_ID), [true, true, true, true]),
        ]);

        if self.data_room.enable_audit_log_retrieval {
            self.add_permissions(vec![
                //                                         [ Adve, Publ, Obse, Agen ]
                (P::retrieve_audit_log(), [true, true, true, true]),
            ]);
        }

        if self.data_room.enable_dev_computations {
            self.add_permissions(vec![
                //                         [ Adve, Publ, Obse, Agen ]
                (P::execute_dev_compute(), [false, true, false, false]),
            ]);
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
                            StaticContentConfig { content: DIRECT_ACTIVATION_ALL_PY.to_vec() },
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
                                    path: "dataset_advertiser".into(),
                                    dependency: validation::v0::get_validation_check_id("dataset_advertiser"),
                                },
                                MountPoint {
                                    path: "dataset_publisher".into(),
                                    dependency: validation::v0::get_validation_check_id("dataset_publisher"),
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
                        validation::v0::get_validation_check_id("dataset_advertiser"),
                        validation::v0::get_validation_check_id("dataset_publisher"),
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
                            StaticContentConfig { content: DIRECT_ACTIVATION_PY.to_vec() },
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

        self.add_permissions(vec![
            //                                                       [ Adve, Publ, Obse, Agen ]
            (P::read_auxiliary_state(), [true, true, __, true]),
            (P::cas_auxiliary_state(), [true, true, __, true]),
            (P::leaf_crud("direct_activation_config"), [true, __, __, true]),
            (P::execute_compute("direct_activation_config"), [true, true, __, true]),
            (P::retrieve_compute_result("direct_activation_config"), [true, true, __, true]),
        ]);
        if self.data_room.enable_download_by_advertiser {
            self.add_permissions(vec![
                //                                                   [ Adve, Publ, Obse, Agen ]
                (P::execute_compute("direct_activation"), [true, __, __, __]),
                (P::retrieve_compute_result("direct_activation"), [true, __, __, __]),
            ]);
        }
        if self.data_room.enable_download_by_publisher {
            self.add_permissions(vec![
                //                                                   [ Adve, Publ, Obse, Agen ]
                (P::execute_compute("direct_activation"), [__, true, __, __]),
                (P::retrieve_compute_result("direct_activation"), [__, true, __, __]),
            ]);
        }
        if self.data_room.enable_download_by_agency {
            self.add_permissions(vec![
                //                                                   [ Adve, Publ, Obse, Agen ]
                (P::execute_compute("direct_activation"), [__, __, __, true]),
                (P::retrieve_compute_result("direct_activation"), [__, __, __, true]),
            ]);
        }

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
                                    path: "dataset_advertiser".into(),
                                    dependency: validation::v0::get_validation_check_id("dataset_advertiser"),
                                },
                                MountPoint {
                                    path: "dataset_publisher".into(),
                                    dependency: validation::v0::get_validation_check_id("dataset_publisher"),
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
                        validation::v0::get_validation_check_id("dataset_advertiser"),
                        validation::v0::get_validation_check_id("dataset_publisher"),
                    ],
                    output_format: ComputeNodeFormat::Zip as i32,
                    protocol: Some(ComputeNodeProtocol { version: self.python_protocol_version }),
                    attestation_specification_id: self.python_attestation_specification_id.clone(),
                })),
                rate_limiting: None,
            })),
        });

        self.add_permissions(vec![
            //                                                [ Adve, Publ, Obse, Agen ]
            (P::read_auxiliary_state(), [true, true, __, true]),
            (P::cas_auxiliary_state(), [true, true, __, true]),
            (P::execute_compute(OVERLAP_INSIGHTS_ID), [true, true, true, true]),
            (P::retrieve_compute_result(OVERLAP_INSIGHTS_ID), [true, true, true, true]),
        ]);

        Ok(())
    }
}

pub fn convert_data_room_v1_to_v2(data_room: v1::MediaDataRoomV1) -> CompileResult<MediaDataRoomV2> {
    Ok(MediaDataRoomV2 {
        id: data_room.id,
        name: data_room.name,
        main_publisher_email: data_room.main_publisher_email,
        main_advertiser_email: data_room.main_advertiser_email,
        publisher_emails: data_room.publisher_emails,
        advertiser_emails: data_room.advertiser_emails,
        observer_emails: data_room.observer_emails,
        agency_emails: data_room.agency_emails,
        publisher_schema: data_room.publisher_schema.clone(),
        advertiser_schema: data_room.advertiser_schema.clone(),
        activation_type: data_room.activation_type,
        enable_download_by_publisher: data_room.enable_download_by_publisher,
        enable_download_by_advertiser: data_room.enable_download_by_advertiser,
        enable_download_by_agency: data_room.enable_download_by_agency,
        enable_overlap_insights: data_room.enable_overlap_insights,
        enable_audit_log_retrieval: data_room.enable_audit_log_retrieval,
        authentication_root_certificate_pem: data_room.authentication_root_certificate_pem,
        driver_enclave_specification: data_room.driver_enclave_specification,
        python_enclave_specification: data_room.python_enclave_specification,
        publisher_validation: ValidationConfig::V0(validation_config::v0::ValidationConfigV0 {
            columns: data_room
                .publisher_schema
                .into_iter()
                .map(|_| validation_config::v0::ColumnValidationV0 {
                    name: None,
                    format_type: format_types::v0::FormatType::String,
                    allow_null: true,
                    hash_with: None,
                    in_range: None,
                })
                .collect(),
            table: None,
        }),
        advertiser_validation: ValidationConfig::V0(validation_config::v0::ValidationConfigV0 {
            columns: data_room
                .advertiser_schema
                .into_iter()
                .map(|_| validation_config::v0::ColumnValidationV0 {
                    name: None,
                    format_type: format_types::v0::FormatType::String,
                    allow_null: true,
                    hash_with: None,
                    in_range: None,
                })
                .collect(),
            table: None,
        }),
        enable_dev_computations: false,
    })
}
