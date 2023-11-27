use std::collections::HashMap;
use std::collections::HashSet;
use std::convert::TryFrom;

use delta_container_worker_api::container_worker_configuration;
use delta_container_worker_api::prost::Message;
use delta_container_worker_api::ContainerWorkerConfiguration;
use delta_container_worker_api::MountPoint;
use delta_container_worker_api::StaticImage;
use delta_data_room_api::compute_node;
use delta_data_room_api::configuration_element::Element;
use delta_data_room_api::permission;
use delta_data_room_api::ComputeNode;
use delta_data_room_api::ComputeNodeBranch;
use delta_data_room_api::ComputeNodeFormat;
use delta_data_room_api::ComputeNodeLeaf;
use delta_data_room_api::ComputeNodeProtocol;
use delta_data_room_api::ConfigurationCommit;
use delta_data_room_api::ConfigurationElement;
use delta_data_room_api::ExecuteComputePermission;
use delta_data_room_api::LeafCrudPermission;
use delta_data_room_api::Permission;
use delta_data_room_api::RetrieveComputeResultPermission;
use delta_data_room_api::UpdateDataRoomStatusPermission;
use delta_data_room_api::UserPermission;
use delta_gcg_driver_api::driver_task_config;
use delta_gcg_driver_api::DriverTaskConfig;
use delta_gcg_driver_api::StaticContentConfig;
use delta_post_worker_api::PostWorkerConfiguration;
use delta_s3_sink_worker_api::s3_object;
use delta_s3_sink_worker_api::zip_object;
use delta_s3_sink_worker_api::FullContent;
use delta_s3_sink_worker_api::S3Object;
use delta_s3_sink_worker_api::S3SinkWorkerConfiguration;
use delta_s3_sink_worker_api::ZipObject;
use delta_sql_worker_api::sql_worker_configuration;
use delta_sql_worker_api::ColumnType;
use delta_sql_worker_api::ComputationConfiguration;
use delta_sql_worker_api::PrimitiveType;
use delta_sql_worker_api::PrivacySettings;
use delta_sql_worker_api::SqlWorkerConfiguration;
use delta_sql_worker_api::TableDependencyMapping;
use delta_synth_data_worker_api::mask::MaskFormat;
use delta_synth_data_worker_api::Column as SynthColumn;
use delta_synth_data_worker_api::Mask;
use delta_synth_data_worker_api::SyntheticDataConf;
use schemars::JsonSchema;
use serde::Deserialize;
use serde::Serialize;
use validation_config::v0::TableValidationV0;

use crate::data_science::shared::ColumnDataFormat;
use crate::data_science::v2::DataScienceCommitV2;
use crate::data_science::DataScienceCommitMergeMetadata;
use crate::data_science::EnclaveSpecificationContext;
use crate::data_science::MatchingComputationNode;
use crate::data_science::MatchingComputeNodeConfig;
use crate::data_science::Participant;
use crate::data_science::ParticipantPermission;
use crate::data_science::RawLeafNode;
use crate::data_science::S3SinkComputationNode;
use crate::data_science::ScriptingComputationNode;
use crate::data_science::ScriptingLanguage;
use crate::data_science::SqlComputationNode;
use crate::data_science::SqlNodePrivacyFilter;
use crate::data_science::SyntheticDataComputationNode;
use crate::data_science::TableMapping;
use crate::validation;
use crate::validation::v0::add_nodes_for_validation;
use crate::validation::v0::get_validation_check_id;
use crate::CompileError;
#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct NodeV2 {
    pub id: String,
    pub name: String,
    pub kind: NodeKindV2,
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub enum NodeKindV2 {
    Leaf(LeafNodeV2),
    Computation(ComputationNodeV2),
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct ComputationNodeV2 {
    pub kind: ComputationNodeKindV2,
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub enum ComputationNodeKindV2 {
    Sql(SqlComputationNode),
    Sqlite(SqliteComputationNode),
    Scripting(ScriptingComputationNode),
    SyntheticData(SyntheticDataComputationNode),
    S3Sink(S3SinkComputationNode),
    Match(MatchingComputationNode),
    Post(PostComputationNode),
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct SqliteComputationNode {
    pub static_content_specification_id: String,
    pub sqlite_specification_id: String,
    pub statement: String,
    pub dependencies: Vec<TableMapping>,
    pub enable_logs_on_error: bool,
    pub enable_logs_on_success: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct LeafNodeV2 {
    pub is_required: bool,
    pub kind: LeafNodeKindV2,
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub enum LeafNodeKindV2 {
    Raw(RawLeafNode),
    Table(TableLeafNodeV2),
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct ValidationNodeV2 {
    pub static_content_specification_id: String,
    pub python_specification_id: String,
    pub validation: TableValidationV0,
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct TableLeafNodeV2 {
    pub columns: Vec<TableLeafNodeColumnV2>,
    pub validation_node: ValidationNodeV2,
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct TableLeafNodeColumnV2 {
    pub name: String,
    pub data_format: ColumnDataFormat,
    pub validation: validation_config::v0::ColumnValidationV0,
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct PostComputationNode {
    pub specification_id: String,
    pub dependency: String,
    pub use_mock_backend: bool,
}

#[derive(Debug, Clone)]
pub struct CommitCompileContextV2 {
    pub nodes_map: HashMap<String, NodeV2>,
    pub enclave_specifications_map: HashMap<String, EnclaveSpecificationContext>,
    pub participants: Vec<Participant>,
    pub enable_development: bool,
    pub enable_interactivity: bool,
    pub initial_participants: HashMap<String, Participant>,
    pub previous_commits: Vec<(DataScienceCommitV2, ConfigurationCommit, DataScienceCommitMergeMetadata)>,
}

impl CommitCompileContextV2 {
    pub(crate) fn initial_pin(&self, data_room_id: &[u8]) -> [u8; 32] {
        crate::data_science::v1::generate_history_pin(data_room_id, std::iter::empty())
    }

    pub(crate) fn all_pins(&self, data_room_id: &[u8]) -> Vec<[u8; 32]> {
        let mut pins = vec![self.initial_pin(data_room_id)];
        for (_, _, metadata) in self.previous_commits.iter() {
            pins.push(metadata.history_pin_at_commit);
        }
        pins
    }

    fn participant_history_by_pin(
        &self,
        data_room_id: &[u8],
    ) -> impl Iterator<Item = ([u8; 32], &HashMap<String, Participant>)> {
        std::iter::once((self.initial_pin(data_room_id), &self.initial_participants)).chain(
            self.previous_commits
                .iter()
                .map(|(_, _, metadata)| (metadata.history_pin_at_commit.clone(), &metadata.participants)),
        )
    }

    pub(crate) fn participant_at_history_pin(
        &self,
        data_room_id: &[u8],
        history_pin: &[u8],
        user: &str,
    ) -> Result<Option<&Participant>, CompileError> {
        let participants_at_history_pin = self
            .participant_history_by_pin(data_room_id)
            .find_map(|(pin, participants)| {
                if pin.as_slice() == history_pin {
                    Some(participants)
                } else {
                    None
                }
            })
            .ok_or("History pin does not refer to an existing history")?;
        Ok(participants_at_history_pin.get(user))
    }
}

pub fn get_dependency_node_name(
    dependency_id: &String,
    nodes_map: &HashMap<String, NodeV2>,
) -> Result<String, CompileError> {
    Ok(nodes_map.get(dependency_id).ok_or_else(|| CompileError("Node not found".to_string()))?.name.clone())
}

pub fn get_enclave_dependency_node_id(dependency_id: &String, nodes_map: &HashMap<String, NodeV2>) -> Option<String> {
    nodes_map.get(dependency_id).map(get_enclave_dependency_node_id_from_node)
}

pub fn get_enclave_dependency_node_id_from_node(node: &NodeV2) -> String {
    match &node.kind {
        NodeKindV2::Leaf(leaf_node) => match &leaf_node.kind {
            LeafNodeKindV2::Raw(_) => node.id.clone(),
            LeafNodeKindV2::Table(_) => get_validation_check_id(&node.id),
        },
        NodeKindV2::Computation(compute_node) => match &compute_node.kind {
            ComputationNodeKindV2::Sql(_) => node.id.clone(),
            ComputationNodeKindV2::Sqlite(_) => {
                let container_id = format!("{}_container", node.id);
                container_id
            }
            ComputationNodeKindV2::Scripting(_) => {
                let container_id = format!("{}_container", node.id);
                container_id
            }
            ComputationNodeKindV2::SyntheticData(_) => {
                let container_id = format!("{}_container", node.id);
                container_id
            }
            ComputationNodeKindV2::S3Sink(_) => node.id.clone(),
            ComputationNodeKindV2::Match(_) => {
                let container_id = format!("{}_match_node", node.id);
                container_id
            }
            ComputationNodeKindV2::Post(_) => node.id.clone(),
        },
    }
}

pub fn get_enclave_leaf_node_id(dependency_id: &str, nodes_map: &HashMap<String, NodeV2>) -> Option<String> {
    nodes_map.get(dependency_id).and_then(|node| match &node.kind {
        NodeKindV2::Leaf(leaf_node) => match &leaf_node.kind {
            LeafNodeKindV2::Raw(_) => Some(node.id.clone()),
            LeafNodeKindV2::Table(_) => {
                let leaf_id = format!("{}_leaf", node.id);
                Some(leaf_id)
            }
        },
        NodeKindV2::Computation(_) => None,
    })
}

fn get_enclave_dependency_node_id_permissions(
    dependency_id: &String,
    nodes_map: &HashMap<String, NodeV2>,
) -> Option<String> {
    nodes_map.get(dependency_id).map(get_enclave_dependency_node_id_from_node_permissions)
}

pub fn get_enclave_dependency_node_id_from_node_permissions(node: &NodeV2) -> String {
    match &node.kind {
        NodeKindV2::Leaf(leaf_node) => match &leaf_node.kind {
            LeafNodeKindV2::Raw(_) => node.id.clone(),
            LeafNodeKindV2::Table(_) => get_validation_check_id(&node.id),
        },
        NodeKindV2::Computation(compute_node) => match &compute_node.kind {
            ComputationNodeKindV2::Sql(_) => node.id.clone(),
            ComputationNodeKindV2::Sqlite(_) => {
                let container_id = format!("{}_container", node.id);
                container_id
            }
            ComputationNodeKindV2::Scripting(_) => {
                let container_id = format!("{}_container", node.id);
                container_id
            }
            ComputationNodeKindV2::SyntheticData(_) => {
                let container_id = format!("{}_container", node.id);
                container_id
            }
            ComputationNodeKindV2::S3Sink(_) => node.id.clone(),
            ComputationNodeKindV2::Match(_) => {
                let container_id = format!("{}_match_filter_node", node.id);
                container_id
            }
            ComputationNodeKindV2::Post(_) => node.id.clone(),
        },
    }
}

pub fn add_node_configuration_elements(
    node: NodeV2,
    configuration_elements: &mut Vec<ConfigurationElement>,
    enclave_specifications_map: &HashMap<String, EnclaveSpecificationContext>,
    nodes_map: &HashMap<String, NodeV2>,
) -> Result<(), CompileError> {
    match node.kind {
        NodeKindV2::Leaf(leaf_node) => match leaf_node.kind {
            LeafNodeKindV2::Raw(_) => {
                configuration_elements.push(ConfigurationElement {
                    id: node.id,
                    element: Some(Element::ComputeNode(ComputeNode {
                        node_name: node.name,
                        rate_limiting: None,
                        node: Some(compute_node::Node::Leaf(ComputeNodeLeaf { is_required: leaf_node.is_required })),
                    })),
                });
            }
            LeafNodeKindV2::Table(table_leaf_node) => {
                let leaf_id = format!("{}_leaf", node.id);
                let leaf_name = format!("{}_leaf", node.name);
                configuration_elements.push(ConfigurationElement {
                    id: leaf_id.clone(),
                    element: Some(Element::ComputeNode(ComputeNode {
                        node_name: leaf_name,
                        rate_limiting: None,
                        node: Some(compute_node::Node::Leaf(ComputeNodeLeaf { is_required: leaf_node.is_required })),
                    })),
                });

                let validation_node = &table_leaf_node.validation_node;
                let python_protocol = enclave_specifications_map
                    .get(&validation_node.python_specification_id)
                    .ok_or_else(|| {
                        CompileError(format!(
                            "No python enclave specification found for '{}'",
                            &validation_node.python_specification_id
                        ))
                    })?
                    .worker_protocol;
                let validation_config =
                    validation_config::ValidationConfig::V0(validation_config::v0::ValidationConfigV0 {
                        columns: table_leaf_node.columns.iter().map(|column| column.validation.clone()).collect(),
                        table: Some(validation_node.validation.clone()),
                    });
                let driver_protocol = enclave_specifications_map
                    .get(&validation_node.python_specification_id)
                    .ok_or_else(|| {
                        CompileError(format!(
                            "No driver enclave specification found for '{}'",
                            &validation_node.static_content_specification_id
                        ))
                    })?
                    .worker_protocol;
                add_nodes_for_validation(
                    configuration_elements, &node.id, &leaf_id, &validation_config,
                    &validation_node.static_content_specification_id, driver_protocol,
                    &validation_node.python_specification_id, python_protocol,
                )?;
            }
        },
        NodeKindV2::Computation(computation_node) => match computation_node.kind {
            ComputationNodeKindV2::Sql(sql_computation_node) => {
                let mut table_dependency_mappings = vec![];
                let mut dependencies = vec![];
                for dependency in sql_computation_node.dependencies {
                    let dependency_id = get_enclave_dependency_node_id(&dependency.node_id, nodes_map)
                        .ok_or_else(|| CompileError(format!("No node found for '{}'", &dependency.node_id)))?;
                    dependencies.push(dependency_id.clone());
                    table_dependency_mappings
                        .push(TableDependencyMapping { table: dependency.table_name, dependency: dependency_id });
                }

                let sql_computation_configuration = SqlWorkerConfiguration {
                    configuration: Some(sql_worker_configuration::Configuration::Computation(
                        ComputationConfiguration {
                            sql_statement: sql_computation_node.statement,
                            privacy_settings: sql_computation_node.privacy_filter.map(|privacy_filter| {
                                PrivacySettings { min_aggregation_group_size: privacy_filter.minimum_rows_count }
                            }),
                            constraints: vec![],
                            table_dependency_mappings,
                        },
                    )),
                };

                let sql_specification_id = sql_computation_node.specification_id;
                let sql_node_metadata = enclave_specifications_map.get(&sql_specification_id).ok_or_else(|| {
                    CompileError(format!("No enclave specification found for '{}'", &sql_specification_id))
                })?;
                configuration_elements.push(ConfigurationElement {
                    id: node.id,
                    element: Some(Element::ComputeNode(ComputeNode {
                        node_name: node.name,
                        node: Some(compute_node::Node::Branch(ComputeNodeBranch {
                            config: sql_computation_configuration.encode_length_delimited_to_vec(),
                            dependencies,
                            output_format: ComputeNodeFormat::Zip as i32,
                            protocol: Some(ComputeNodeProtocol { version: sql_node_metadata.worker_protocol }),
                            attestation_specification_id: sql_specification_id,
                        })),
                        rate_limiting: None,
                    })),
                });
            }
            ComputationNodeKindV2::Sqlite(sqlite_computation_node) => {
                let static_content_attestation_id = sqlite_computation_node.static_content_specification_id;
                let static_content_node_metadata =
                    enclave_specifications_map.get(&static_content_attestation_id).ok_or_else(|| {
                        CompileError(format!("No enclave specification found for '{}'", &static_content_attestation_id))
                    })?;

                let dependencies =
                    construct_table_dependency_mappings(&sqlite_computation_node.dependencies, nodes_map)?;

                let sql_computation_configuration = construct_sql_worker_configuration(
                    &sqlite_computation_node.statement,
                    &None,
                    dependencies.iter().map(|(_, _, table_dep)| table_dep.clone()),
                );

                let sqlite_configuration_node_id = format!("{}_configuration", node.id);
                let sqlite_worker_configuration = DriverTaskConfig {
                    driver_task_config: Some(driver_task_config::DriverTaskConfig::StaticContent(
                        StaticContentConfig { content: sql_computation_configuration.encode_length_delimited_to_vec() },
                    )),
                };
                let sqlite_configuration_node_name = format!("{}_configuration", node.name);
                configuration_elements.push(ConfigurationElement {
                    id: sqlite_configuration_node_id.clone(),
                    element: Some(Element::ComputeNode(ComputeNode {
                        node_name: sqlite_configuration_node_name.clone(),
                        node: Some(compute_node::Node::Branch(ComputeNodeBranch {
                            config: sqlite_worker_configuration.encode_length_delimited_to_vec(),
                            dependencies: vec![],
                            output_format: ComputeNodeFormat::Raw as i32,
                            protocol: Some(ComputeNodeProtocol {
                                version: static_content_node_metadata.worker_protocol,
                            }),
                            attestation_specification_id: static_content_attestation_id,
                        })),
                        rate_limiting: None,
                    })),
                });

                let sqlite_specification_id = sqlite_computation_node.sqlite_specification_id.clone();
                let sqlite_node_metadata =
                    enclave_specifications_map.get(&sqlite_specification_id).ok_or_else(|| {
                        CompileError(format!("No enclave specification found for '{}'", &sqlite_specification_id))
                    })?;

                let mut node_dependencies_mount_points = vec![];
                let mut command = vec!["run-sql-worker".to_string()];

                for (id, enclave_id, _) in dependencies {
                    let path = nodes_map
                        .get(&id)
                        .ok_or_else(|| CompileError(format!("Node not found for id `{id}`")))?
                        .name
                        .clone();
                    command.push("--input".into());
                    command.push(path.clone());

                    node_dependencies_mount_points.push(MountPoint { path, dependency: enclave_id });
                }

                node_dependencies_mount_points.push(MountPoint {
                    path: sqlite_configuration_node_name.clone(),
                    dependency: sqlite_configuration_node_id.clone(),
                });
                command.push("--config".into());
                command.push(sqlite_configuration_node_name);

                let container_worker_configuration = ContainerWorkerConfiguration {
                    configuration: Some(container_worker_configuration::Configuration::Static(StaticImage {
                        command,
                        mount_points: node_dependencies_mount_points.clone(),
                        output_path: "/output".to_string(),
                        include_container_logs_on_error: sqlite_computation_node.enable_logs_on_error,
                        include_container_logs_on_success: sqlite_computation_node.enable_logs_on_success,
                        minimum_container_memory_size: None,
                        extra_chunk_cache_size_to_available_memory_ratio: None,
                    })),
                };
                configuration_elements.push(ConfigurationElement {
                    id: format!("{}_container", node.id),
                    element: Some(Element::ComputeNode(ComputeNode {
                        node_name: node.name,
                        node: Some(compute_node::Node::Branch(ComputeNodeBranch {
                            config: container_worker_configuration.encode_length_delimited_to_vec(),
                            dependencies: node_dependencies_mount_points
                                .iter()
                                .map(|mount_point| mount_point.dependency.to_string())
                                .collect(),
                            output_format: ComputeNodeFormat::Zip as i32,
                            protocol: Some(ComputeNodeProtocol { version: sqlite_node_metadata.worker_protocol }),
                            attestation_specification_id: sqlite_specification_id,
                        })),
                        rate_limiting: None,
                    })),
                });
            }
            ComputationNodeKindV2::Scripting(scripting_computation_node) => {
                let static_content_attestation_id = scripting_computation_node.static_content_specification_id;
                let static_content_node_metadata =
                    enclave_specifications_map.get(&static_content_attestation_id).ok_or_else(|| {
                        CompileError(format!("No enclave specification found for '{}'", &static_content_attestation_id))
                    })?;

                let mut additional_scripts = vec![];
                for (idx, script) in scripting_computation_node.additional_scripts.into_iter().enumerate() {
                    let script_id = format!("{}_script_{}", node.id, idx);
                    additional_scripts.push((script_id.clone(), format!("code/{}", script.name)));
                    let script_configuration = DriverTaskConfig {
                        driver_task_config: Some(driver_task_config::DriverTaskConfig::StaticContent(
                            StaticContentConfig { content: script.content.into_bytes() },
                        )),
                    };
                    configuration_elements.push(ConfigurationElement {
                        id: script_id,
                        element: Some(Element::ComputeNode(ComputeNode {
                            node_name: script.name,
                            node: Some(compute_node::Node::Branch(ComputeNodeBranch {
                                config: script_configuration.encode_length_delimited_to_vec(),
                                dependencies: vec![],
                                output_format: ComputeNodeFormat::Raw as i32,
                                protocol: Some(ComputeNodeProtocol {
                                    version: static_content_node_metadata.worker_protocol,
                                }),
                                attestation_specification_id: static_content_attestation_id.clone(),
                            })),
                            rate_limiting: None,
                        })),
                    });
                }

                let main_script_id = format!("{}_main_script", node.id);
                let main_script_configuration = DriverTaskConfig {
                    driver_task_config: Some(driver_task_config::DriverTaskConfig::StaticContent(
                        StaticContentConfig { content: scripting_computation_node.main_script.content.into_bytes() },
                    )),
                };
                configuration_elements.push(ConfigurationElement {
                    id: main_script_id.clone(),
                    element: Some(Element::ComputeNode(ComputeNode {
                        node_name: scripting_computation_node.main_script.name,
                        node: Some(compute_node::Node::Branch(ComputeNodeBranch {
                            config: main_script_configuration.encode_length_delimited_to_vec(),
                            dependencies: vec![],
                            output_format: ComputeNodeFormat::Raw as i32,
                            protocol: Some(ComputeNodeProtocol {
                                version: static_content_node_metadata.worker_protocol,
                            }),
                            attestation_specification_id: static_content_attestation_id,
                        })),
                        rate_limiting: None,
                    })),
                });

                let node_dependencies = scripting_computation_node
                    .dependencies
                    .into_iter()
                    .map(|id| {
                        let enclave_id = get_enclave_dependency_node_id(&id, nodes_map)
                            .ok_or_else(|| CompileError("Node not found".to_string()))?;
                        Ok((id, enclave_id))
                    })
                    .collect::<Result<Vec<_>, CompileError>>()?;
                let dependencies = std::iter::once(main_script_id.clone())
                    .chain(additional_scripts.iter().map(|(id, _)| id.clone()))
                    .chain(node_dependencies.iter().map(|(_, enclave_node_id)| enclave_node_id.clone()))
                    .collect::<Vec<_>>();
                let (scripting_command, main_script_file_name) = match scripting_computation_node.scripting_language {
                    ScriptingLanguage::Python => ("python".to_string(), "script.py".to_string()),
                    ScriptingLanguage::R => ("Rscript".to_string(), "script.R".to_string()),
                };
                let node_dependecies_mount_points = node_dependencies
                    .into_iter()
                    .map(|(id, enclave_id)| {
                        Ok(MountPoint {
                            path: nodes_map
                                .get(&id)
                                .ok_or_else(|| CompileError("Node not found".to_string()))?
                                .name
                                .clone(),
                            dependency: enclave_id,
                        })
                    })
                    .collect::<Result<Vec<_>, CompileError>>()?;
                let container_worker_configuration = ContainerWorkerConfiguration {
                    configuration: Some(container_worker_configuration::Configuration::Static(StaticImage {
                        command: vec![scripting_command, format!("/input/{}", main_script_file_name)],
                        mount_points: std::iter::once(MountPoint {
                            dependency: main_script_id,
                            path: main_script_file_name,
                        })
                        .chain(
                            additional_scripts
                                .into_iter()
                                .map(|(id, file_name)| MountPoint { dependency: id, path: file_name }),
                        )
                        .chain(node_dependecies_mount_points.into_iter())
                        .collect(),
                        output_path: "/output".to_string(),
                        include_container_logs_on_error: scripting_computation_node.enable_logs_on_error,
                        include_container_logs_on_success: scripting_computation_node.enable_logs_on_success,
                        minimum_container_memory_size: None,
                        extra_chunk_cache_size_to_available_memory_ratio: None,
                    })),
                };
                let scripting_specification_id = scripting_computation_node.scripting_specification_id;
                let scripting_node_metadata =
                    enclave_specifications_map.get(&scripting_specification_id).ok_or_else(|| {
                        CompileError(format!("No enclave specification found for '{}'", &scripting_specification_id))
                    })?;
                configuration_elements.push(ConfigurationElement {
                    id: format!("{}_container", node.id),
                    element: Some(Element::ComputeNode(ComputeNode {
                        node_name: node.name,
                        node: Some(compute_node::Node::Branch(ComputeNodeBranch {
                            config: container_worker_configuration.encode_length_delimited_to_vec(),
                            dependencies,
                            output_format: ComputeNodeFormat::Zip as i32,
                            protocol: Some(ComputeNodeProtocol { version: scripting_node_metadata.worker_protocol }),
                            attestation_specification_id: scripting_specification_id,
                        })),
                        rate_limiting: None,
                    })),
                });
            }
            ComputationNodeKindV2::SyntheticData(synthetic_data_computation_node) => {
                let static_content_attestation_id = synthetic_data_computation_node.static_content_specification_id;
                let static_content_node_metadata =
                    enclave_specifications_map.get(&static_content_attestation_id).ok_or_else(|| {
                        CompileError(format!("No enclave specification found for '{}'", &static_content_attestation_id))
                    })?;
                let synthetic_data_configuration = SyntheticDataConf {
                    columns: synthetic_data_computation_node
                        .columns
                        .iter()
                        .filter_map(|column| {
                            if column.should_mask_column {
                                Some(SynthColumn {
                                    index: column.index,
                                    r#type: Some(ColumnType {
                                        primitive_type: PrimitiveType::from(column.data_format.data_type.clone())
                                            as i32,
                                        nullable: column.data_format.is_nullable,
                                    }),
                                    mask: Some(Mask { format: MaskFormat::from(column.mask_type.clone()) as i32 }),
                                })
                            } else {
                                None
                            }
                        })
                        .collect(),
                    output_original_data_stats: synthetic_data_computation_node.output_original_data_statistics,
                    epsilon: synthetic_data_computation_node.epsilon,
                };
                let synthetic_data_configuration_id = format!("{}_configuration", node.id);
                let synthetic_data_configuration_name = format!("{}_configuration", node.name);
                let synthetic_data_configuration_node = DriverTaskConfig {
                    driver_task_config: Some(driver_task_config::DriverTaskConfig::StaticContent(
                        StaticContentConfig { content: synthetic_data_configuration.encode_length_delimited_to_vec() },
                    )),
                };
                configuration_elements.push(ConfigurationElement {
                    id: synthetic_data_configuration_id.clone(),
                    element: Some(Element::ComputeNode(ComputeNode {
                        node_name: synthetic_data_configuration_name,
                        node: Some(compute_node::Node::Branch(ComputeNodeBranch {
                            config: synthetic_data_configuration_node.encode_length_delimited_to_vec(),
                            dependencies: vec![],
                            output_format: ComputeNodeFormat::Raw as i32,
                            protocol: Some(ComputeNodeProtocol {
                                version: static_content_node_metadata.worker_protocol,
                            }),
                            attestation_specification_id: static_content_attestation_id,
                        })),
                        rate_limiting: None,
                    })),
                });

                let synth_data_specification_id = synthetic_data_computation_node.synth_specification_id;
                let synth_data_computation_node_dependency = synthetic_data_computation_node.dependency;
                let synth_data_node_metadata =
                    enclave_specifications_map.get(&synth_data_specification_id).ok_or_else(|| {
                        CompileError(format!("No enclave specification found for '{}'", &synth_data_specification_id))
                    })?;
                let synthetic_data_dependency =
                    get_enclave_dependency_node_id(&synth_data_computation_node_dependency, nodes_map).ok_or_else(
                        || CompileError(format!("No node found for '{}'", &synth_data_computation_node_dependency,)),
                    )?;
                let container_worker_configuration = ContainerWorkerConfiguration {
                    configuration: Some(container_worker_configuration::Configuration::Static(StaticImage {
                        command: vec!["generate-synth-data".to_string()],
                        mount_points: vec![
                            MountPoint {
                                dependency: synthetic_data_configuration_id.clone(),
                                path: "config".to_string(),
                            },
                            MountPoint { dependency: synthetic_data_dependency.clone(), path: "input".to_string() },
                        ],
                        output_path: "/output".to_string(),
                        include_container_logs_on_error: synthetic_data_computation_node.enable_logs_on_error,
                        include_container_logs_on_success: synthetic_data_computation_node.enable_logs_on_success,
                        minimum_container_memory_size: None,
                        extra_chunk_cache_size_to_available_memory_ratio: None,
                    })),
                };
                configuration_elements.push(ConfigurationElement {
                    id: format!("{}_container", node.id),
                    element: Some(Element::ComputeNode(ComputeNode {
                        node_name: node.name,
                        node: Some(compute_node::Node::Branch(ComputeNodeBranch {
                            config: container_worker_configuration.encode_length_delimited_to_vec(),
                            dependencies: vec![synthetic_data_configuration_id, synthetic_data_dependency],
                            output_format: ComputeNodeFormat::Zip as i32,
                            protocol: Some(ComputeNodeProtocol { version: synth_data_node_metadata.worker_protocol }),
                            attestation_specification_id: synth_data_specification_id,
                        })),
                        rate_limiting: None,
                    })),
                });
            }
            ComputationNodeKindV2::S3Sink(s3_sink_computation_node) => {
                let credentials_dependency =
                    get_enclave_dependency_node_id(&s3_sink_computation_node.credentials_dependency_id, nodes_map)
                        .ok_or_else(|| {
                            CompileError(format!(
                                "No node found for '{}'",
                                &s3_sink_computation_node.credentials_dependency_id
                            ))
                        })?;
                let upload_dependency_id =
                    get_enclave_dependency_node_id(&s3_sink_computation_node.upload_dependency_id, nodes_map)
                        .ok_or_else(|| {
                            CompileError(format!(
                                "No node found for '{}'",
                                &s3_sink_computation_node.upload_dependency_id
                            ))
                        })?;
                match (&s3_sink_computation_node.s3_provider, s3_sink_computation_node.region.is_empty()) {
                    (crate::data_science::S3Provider::Aws, true) => {
                        return Err(CompileError::from("AWS S3Sink Computation requires region to be set"))
                    }
                    (crate::data_science::S3Provider::Aws, false) => {}
                    (crate::data_science::S3Provider::Gcs, _) => {}
                }
                let s3_sink_worker_configuration = S3SinkWorkerConfiguration {
                    endpoint: s3_sink_computation_node.endpoint,
                    region: s3_sink_computation_node.region,
                    credentials_dependency: credentials_dependency.clone(),
                    objects: vec![S3Object {
                        dependency: upload_dependency_id.clone(),
                        format: Some(s3_object::Format::Zip(ZipObject {
                            kind: Some(zip_object::Kind::FullContent(FullContent {})),
                        })),
                    }],
                    s3_provider: delta_s3_sink_worker_api::S3Provider::from(s3_sink_computation_node.s3_provider)
                        .into(),
                };

                let s3_sink_specification_id = s3_sink_computation_node.specification_id;
                let s3_sink_node_metadata =
                    enclave_specifications_map.get(&s3_sink_specification_id).ok_or_else(|| {
                        CompileError(format!("No enclave specification found for '{}'", &s3_sink_specification_id))
                    })?;
                configuration_elements.push(ConfigurationElement {
                    id: node.id,
                    element: Some(Element::ComputeNode(ComputeNode {
                        node_name: node.name,
                        node: Some(compute_node::Node::Branch(ComputeNodeBranch {
                            config: s3_sink_worker_configuration.encode_length_delimited_to_vec(),
                            dependencies: vec![credentials_dependency, upload_dependency_id],
                            output_format: ComputeNodeFormat::Raw as i32,
                            protocol: Some(ComputeNodeProtocol { version: s3_sink_node_metadata.worker_protocol }),
                            attestation_specification_id: s3_sink_specification_id,
                        })),
                        rate_limiting: None,
                    })),
                });
            }
            ComputationNodeKindV2::Match(match_node) => {
                let mut dependency_ids = vec![];
                let mut mount_points = vec![];

                // Leaf dependencies.
                let mut dependencies = vec![];
                for dependency_id in &match_node.dependencies {
                    let enclave_id = get_enclave_dependency_node_id(dependency_id, nodes_map)
                        .ok_or_else(|| CompileError(format!("No node found for '{}'", dependency_id)))?;
                    let path = get_dependency_node_name(dependency_id, nodes_map)?;
                    dependencies.push(path.clone());

                    dependency_ids.push(enclave_id.clone());
                    mount_points.push(MountPoint { path, dependency: enclave_id.clone() });
                }

                let static_content_specification_id = match_node.static_content_specification_id.clone();
                let static_content_specification_ctx =
                    enclave_specifications_map.get(&static_content_specification_id).ok_or_else(|| {
                        CompileError(format!(
                            "No enclave specification found for '{}'",
                            &static_content_specification_id
                        ))
                    })?;

                // Add match node configuration element.
                let mut config = MatchingComputeNodeConfig::try_from(&match_node)?;
                config.set_dependency_paths(dependencies);
                let config_id = format!("{}_matching_config", node.id);
                configuration_elements.push(ConfigurationElement {
                    id: config_id.clone(),
                    element: Some(Element::ComputeNode(ComputeNode {
                        node_name: config_id.clone(),
                        node: Some(compute_node::Node::Branch(ComputeNodeBranch {
                            config: prost::Message::encode_length_delimited_to_vec(&DriverTaskConfig {
                                driver_task_config: Some(driver_task_config::DriverTaskConfig::StaticContent(
                                    StaticContentConfig {
                                        content: serde_json::to_vec(&config)
                                            .map_err(|e| CompileError(e.to_string()))?,
                                    },
                                )),
                            }),
                            dependencies: vec![],
                            output_format: ComputeNodeFormat::Raw as i32,
                            protocol: Some(ComputeNodeProtocol {
                                version: static_content_specification_ctx.worker_protocol,
                            }),
                            attestation_specification_id: static_content_specification_id.clone(),
                        })),
                        rate_limiting: None,
                    })),
                });
                dependency_ids.push(config_id.clone());
                mount_points
                    .push(MountPoint { path: "matching_node_config.json".to_string(), dependency: config_id.clone() });

                // Add match script node.
                let script_id = format!("{}_script", node.id);
                let script_name = "match.py";

                configuration_elements.push(ConfigurationElement {
                    id: script_id.clone(),
                    element: Some(Element::ComputeNode(ComputeNode {
                        node_name: script_id.clone(),
                        node: Some(compute_node::Node::Branch(ComputeNodeBranch {
                            config: DriverTaskConfig {
                                driver_task_config: Some(driver_task_config::DriverTaskConfig::StaticContent(
                                    StaticContentConfig { content: include_bytes!("../scripts/match.py").to_vec() },
                                )),
                            }
                            .encode_length_delimited_to_vec(),
                            dependencies: vec![],
                            output_format: ComputeNodeFormat::Raw as i32,
                            protocol: Some(ComputeNodeProtocol {
                                version: static_content_specification_ctx.worker_protocol,
                            }),
                            attestation_specification_id: static_content_specification_id.clone(),
                        })),
                        rate_limiting: None,
                    })),
                });
                dependency_ids.push(script_id.clone());
                mount_points.push(MountPoint { path: script_name.to_string(), dependency: script_id.clone() });

                // Container worker.
                let container_worker_cfg = ContainerWorkerConfiguration {
                    configuration: Some(container_worker_configuration::Configuration::Static(StaticImage {
                        command: vec!["python3".to_string(), "/input/match.py".to_string()],
                        mount_points,
                        output_path: "/output".into(),
                        include_container_logs_on_error: match_node.enable_logs_on_error,
                        include_container_logs_on_success: match_node.enable_logs_on_success,
                        minimum_container_memory_size: None,
                        extra_chunk_cache_size_to_available_memory_ratio: None,
                    })),
                };

                // Match node for running the container worker.
                let match_node_specification_id = match_node.specification_id.clone();
                let match_node_specification_ctx =
                    enclave_specifications_map.get(&match_node_specification_id).ok_or_else(|| {
                        CompileError(format!("No enclave specification found for '{}'", &match_node_specification_id))
                    })?;
                let match_node_id = format!("{}_match_node", node.id);
                configuration_elements.push(ConfigurationElement {
                    id: match_node_id.clone(),
                    element: Some(Element::ComputeNode(ComputeNode {
                        node_name: match_node_id.clone(),
                        node: Some(compute_node::Node::Branch(ComputeNodeBranch {
                            config: container_worker_cfg.encode_length_delimited_to_vec(),
                            dependencies: dependency_ids,
                            output_format: ComputeNodeFormat::Zip as i32,
                            protocol: Some(ComputeNodeProtocol {
                                version: match_node_specification_ctx.worker_protocol,
                            }),
                            attestation_specification_id: match_node.specification_id.clone(),
                        })),
                        rate_limiting: None,
                    })),
                });

                // Configure match filter node (depends on the output of the match node)

                // Add match filter script node.
                let match_filter_script_id = format!("{}_match_filter_script", node.id);
                let match_filter_script_name = "match_filter.py";
                configuration_elements.push(ConfigurationElement {
                    id: match_filter_script_id.clone(),
                    element: Some(Element::ComputeNode(ComputeNode {
                        node_name: match_filter_script_id.clone(),
                        node: Some(compute_node::Node::Branch(ComputeNodeBranch {
                            config: DriverTaskConfig {
                                driver_task_config: Some(driver_task_config::DriverTaskConfig::StaticContent(
                                    StaticContentConfig {
                                        content: include_bytes!("./../scripts/match_filter.py").to_vec(),
                                    },
                                )),
                            }
                            .encode_length_delimited_to_vec(),
                            dependencies: vec![],
                            output_format: ComputeNodeFormat::Raw as i32,
                            protocol: Some(ComputeNodeProtocol {
                                version: static_content_specification_ctx.worker_protocol,
                            }),
                            attestation_specification_id: static_content_specification_id,
                        })),
                        rate_limiting: None,
                    })),
                });

                let match_filter_container_worker_cfg = ContainerWorkerConfiguration {
                    configuration: Some(container_worker_configuration::Configuration::Static(StaticImage {
                        command: vec!["python3".to_string(), "/input/match_filter.py".to_string()],
                        mount_points: vec![
                            MountPoint { path: "match_results".to_string(), dependency: match_node_id.clone() },
                            MountPoint {
                                path: match_filter_script_name.to_string(),
                                dependency: match_filter_script_id.clone(),
                            },
                        ],
                        output_path: "/output".into(),
                        include_container_logs_on_error: match_node.enable_logs_on_error,
                        include_container_logs_on_success: match_node.enable_logs_on_success,
                        minimum_container_memory_size: None,
                        extra_chunk_cache_size_to_available_memory_ratio: None,
                    })),
                };

                let container_id = format!("{}_match_filter_node", node.id);
                configuration_elements.push(ConfigurationElement {
                    id: container_id.clone(),
                    element: Some(Element::ComputeNode(ComputeNode {
                        node_name: node.name,
                        node: Some(compute_node::Node::Branch(ComputeNodeBranch {
                            config: match_filter_container_worker_cfg.encode_length_delimited_to_vec(),
                            dependencies: vec![match_node_id, match_filter_script_id],
                            output_format: ComputeNodeFormat::Zip as i32,
                            protocol: Some(ComputeNodeProtocol {
                                version: match_node_specification_ctx.worker_protocol,
                            }),
                            attestation_specification_id: match_node.specification_id,
                        })),
                        rate_limiting: None,
                    })),
                });
            }
            ComputationNodeKindV2::Post(post_computation_node) => {
                let input_dependency_id = get_enclave_dependency_node_id(&post_computation_node.dependency, nodes_map)
                    .ok_or_else(|| {
                        CompileError(format!("No node found for '{}'", &post_computation_node.dependency))
                    })?;
                let post_worker_configuration =
                    PostWorkerConfiguration { use_mock_backend: post_computation_node.use_mock_backend };

                let post_node_specification_id = post_computation_node.specification_id;
                let post_node_metadata =
                    enclave_specifications_map.get(&post_node_specification_id).ok_or_else(|| {
                        CompileError(format!("No enclave specification found for '{}'", &post_node_specification_id))
                    })?;
                configuration_elements.push(ConfigurationElement {
                    id: node.id,
                    element: Some(Element::ComputeNode(ComputeNode {
                        node_name: node.name,
                        node: Some(compute_node::Node::Branch(ComputeNodeBranch {
                            config: post_worker_configuration.encode_length_delimited_to_vec(),
                            dependencies: vec![input_dependency_id],
                            output_format: ComputeNodeFormat::Zip as i32,
                            protocol: Some(ComputeNodeProtocol { version: post_node_metadata.worker_protocol }),
                            attestation_specification_id: post_node_specification_id,
                        })),
                        rate_limiting: None,
                    })),
                });
            }
        },
    }
    Ok(())
}

pub fn add_participant_permission_configuration_elements(
    participant: Participant,
    basic_permissions: Vec<Permission>,
    configuration_elements: &mut Vec<ConfigurationElement>,
    nodes_map: &HashMap<String, NodeV2>,
) -> Result<(), CompileError> {
    let mut permissions = basic_permissions;
    for permission in &participant.permissions {
        match permission {
            ParticipantPermission::DataOwner(data_owner_perm) => {
                permissions.push(Permission {
                    permission: Some(permission::Permission::LeafCrudPermission(LeafCrudPermission {
                        leaf_node_id: get_enclave_leaf_node_id(&data_owner_perm.node_id, nodes_map)
                            .ok_or_else(|| CompileError(format!("No node found for '{}'", data_owner_perm.node_id)))?,
                    })),
                });
                permissions.push(Permission {
                    permission: Some(permission::Permission::ExecuteComputePermission(ExecuteComputePermission {
                        compute_node_id: get_enclave_dependency_node_id_permissions(
                            &data_owner_perm.node_id, nodes_map,
                        )
                        .ok_or_else(|| CompileError(format!("No node found for '{}'", data_owner_perm.node_id)))?,
                    })),
                });
                permissions.push(Permission {
                    permission: Some(permission::Permission::RetrieveComputeResultPermission(
                        RetrieveComputeResultPermission {
                            compute_node_id: get_enclave_dependency_node_id_permissions(
                                &data_owner_perm.node_id, nodes_map,
                            )
                            .ok_or_else(|| CompileError(format!("No node found for '{}'", data_owner_perm.node_id)))?,
                        },
                    )),
                });
            }
            ParticipantPermission::Analyst(analyst_perm) => {
                permissions.push(Permission {
                    permission: Some(permission::Permission::ExecuteComputePermission(ExecuteComputePermission {
                        compute_node_id: get_enclave_dependency_node_id_permissions(&analyst_perm.node_id, nodes_map)
                            .ok_or_else(|| {
                            CompileError(format!("No node found for '{}'", analyst_perm.node_id))
                        })?,
                    })),
                });
                permissions.push(Permission {
                    permission: Some(permission::Permission::RetrieveComputeResultPermission(
                        RetrieveComputeResultPermission {
                            compute_node_id: get_enclave_dependency_node_id_permissions(
                                &analyst_perm.node_id, nodes_map,
                            )
                            .ok_or_else(|| CompileError(format!("No node found for '{}'", analyst_perm.node_id)))?,
                        },
                    )),
                });
            }
            ParticipantPermission::Manager(_) => {
                permissions.push(Permission {
                    permission: Some(permission::Permission::UpdateDataRoomStatusPermission(
                        UpdateDataRoomStatusPermission {},
                    )),
                });
            }
        }
    }
    configuration_elements.push(ConfigurationElement {
        id: format!("participant_{}", &participant.user),
        element: Some(Element::UserPermission(UserPermission {
            email: participant.user.clone(),
            permissions,
            authentication_method_id: "authentication_method".to_string(),
        })),
    });

    add_permissions_for_validation_report(&participant, configuration_elements, &nodes_map)?;

    Ok(())
}

pub fn add_permissions_for_validation_report(
    participant: &Participant,
    configuration_elements: &mut Vec<ConfigurationElement>,
    nodes_map: &HashMap<String, NodeV2>,
) -> Result<(), CompileError> {
    // Get a list of table node ids that have a validation node configured
    let table_node_ids_with_validation: HashSet<&String> = nodes_map
        .iter()
        .filter_map(|(node_id, node)| {
            match &node.kind {
                NodeKindV2::Leaf(leaf) => match &leaf.kind {
                    LeafNodeKindV2::Raw(_) => (),
                    LeafNodeKindV2::Table(_) => {
                        return Some(node_id);
                    }
                },
                NodeKindV2::Computation(_) => (),
            };
            None
        })
        .collect();

    // Construct a map from user email to mutable list of permissions
    let mut permissions_by_user: HashMap<&String, &mut Vec<Permission>> = configuration_elements
        .iter_mut()
        .filter_map(|element| {
            if let Some(Element::UserPermission(user_permission)) = &mut element.element {
                Some((&user_permission.email, &mut user_permission.permissions))
            } else {
                None
            }
        })
        .collect();

    // Go through each participant and add permissions for computing and retrieving the validation
    // report in case the participant is a data owner for a table node with validation configured.
    for permission in &participant.permissions {
        if let ParticipantPermission::DataOwner(node) = permission {
            if table_node_ids_with_validation.contains(&node.node_id) {
                if let Some(permissions) = permissions_by_user.get_mut(&participant.user) {
                    permissions.push(Permission {
                        permission: Some(permission::Permission::RetrieveComputeResultPermission(
                            RetrieveComputeResultPermission {
                                compute_node_id: validation::v0::get_validation_report_id(&node.node_id),
                            },
                        )),
                    });
                    permissions.push(Permission {
                        permission: Some(permission::Permission::ExecuteComputePermission(ExecuteComputePermission {
                            compute_node_id: validation::v0::get_validation_report_id(&node.node_id),
                        })),
                    });
                }
            }
        }
    }

    Ok(())
}

pub fn construct_table_dependency_mappings(
    table_mappings: &[TableMapping],
    nodes_map: &HashMap<String, NodeV2>,
) -> Result<Vec<(String, String, TableDependencyMapping)>, CompileError> {
    let mut dependencies = vec![];
    for dependency in table_mappings {
        let enclave_dependency_id = get_enclave_dependency_node_id(&dependency.node_id, nodes_map)
            .ok_or_else(|| CompileError(format!("No node found for '{}'", &dependency.node_id)))?;
        dependencies.push((dependency.node_id.clone(), enclave_dependency_id.clone(), TableDependencyMapping {
            table: dependency.table_name.clone(),
            dependency: enclave_dependency_id,
        }))
    }
    Ok(dependencies)
}

pub fn construct_sql_worker_configuration<T: IntoIterator<Item = TableDependencyMapping>>(
    statement: &str,
    privacy_filter: &Option<SqlNodePrivacyFilter>,
    table_dependency_mappings: T,
) -> SqlWorkerConfiguration {
    let sql_computation_configuration = SqlWorkerConfiguration {
        configuration: Some(sql_worker_configuration::Configuration::Computation(ComputationConfiguration {
            sql_statement: statement.into(),
            privacy_settings: privacy_filter.as_ref().map(|privacy_filter| PrivacySettings {
                min_aggregation_group_size: privacy_filter.minimum_rows_count.clone(),
            }),
            constraints: vec![],
            table_dependency_mappings: table_dependency_mappings.into_iter().collect(),
        })),
    };
    sql_computation_configuration
}
