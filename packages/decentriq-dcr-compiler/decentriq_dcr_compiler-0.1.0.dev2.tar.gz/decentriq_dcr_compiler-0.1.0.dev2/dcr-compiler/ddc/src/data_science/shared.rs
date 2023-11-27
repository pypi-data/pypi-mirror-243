use std::collections::HashMap;
use std::convert::TryFrom;

use delta_attestation_api::AttestationSpecification;
use delta_container_worker_api::container_worker_configuration;
use delta_container_worker_api::prost::Message;
use delta_container_worker_api::ContainerWorkerConfiguration;
use delta_container_worker_api::MountPoint;
use delta_container_worker_api::StaticImage;
use delta_data_room_api::compute_node;
use delta_data_room_api::configuration_element::Element;
use delta_data_room_api::permission;
use delta_data_room_api::CasAuxiliaryStatePermission;
use delta_data_room_api::ComputeNode;
use delta_data_room_api::ComputeNodeBranch;
use delta_data_room_api::ComputeNodeFormat;
use delta_data_room_api::ComputeNodeLeaf;
use delta_data_room_api::ComputeNodeProtocol;
use delta_data_room_api::ConfigurationElement;
use delta_data_room_api::DryRunPermission;
use delta_data_room_api::ExecuteComputePermission;
use delta_data_room_api::ExecuteDevelopmentComputePermission;
use delta_data_room_api::GenerateMergeSignaturePermission;
use delta_data_room_api::LeafCrudPermission;
use delta_data_room_api::MergeConfigurationCommitPermission;
use delta_data_room_api::Permission;
use delta_data_room_api::ReadAuxiliaryStatePermission;
use delta_data_room_api::RetrieveAuditLogPermission;
use delta_data_room_api::RetrieveComputeResultPermission;
use delta_data_room_api::RetrieveDataRoomPermission;
use delta_data_room_api::RetrieveDataRoomStatusPermission;
use delta_data_room_api::RetrievePublishedDatasetsPermission;
use delta_data_room_api::UpdateDataRoomStatusPermission;
use delta_data_room_api::UserPermission;
use delta_gcg_driver_api::driver_task_config;
use delta_gcg_driver_api::DriverTaskConfig;
use delta_gcg_driver_api::StaticContentConfig;
use delta_s3_sink_worker_api::s3_object;
use delta_s3_sink_worker_api::zip_object;
use delta_s3_sink_worker_api::FullContent;
use delta_s3_sink_worker_api::S3Object;
use delta_s3_sink_worker_api::S3SinkWorkerConfiguration;
use delta_s3_sink_worker_api::ZipObject;
use delta_sql_worker_api::sql_worker_configuration;
use delta_sql_worker_api::ColumnType;
use delta_sql_worker_api::ComputationConfiguration;
use delta_sql_worker_api::NamedColumn;
use delta_sql_worker_api::PrimitiveType;
use delta_sql_worker_api::PrivacySettings;
use delta_sql_worker_api::SqlWorkerConfiguration;
use delta_sql_worker_api::TableDependencyMapping;
use delta_sql_worker_api::TableSchema;
use delta_sql_worker_api::ValidationConfiguration;
use delta_synth_data_worker_api::mask::MaskFormat;
use delta_synth_data_worker_api::Column as SynthColumn;
use delta_synth_data_worker_api::Mask;
use delta_synth_data_worker_api::SyntheticDataConf;
use schemars::JsonSchema;
use serde::Deserialize;
use serde::Serialize;

use super::v0;
use super::v1;
use super::v2;
use super::v3;
use super::v4;
use super::v5;
use crate::CompileError;

#[derive(Debug, Clone)]
pub enum DataRoomCompileContext {
    V0(v0::DataRoomCompileContextV0),
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum CompileVersion {
    V0 = 0,
    V1 = 1,
    V2 = 2,
    V3 = 3,
    V4 = 4,
    V5 = 5,
}

#[derive(Debug, Clone)]
pub enum CommitCompileContext {
    V0(v0::CommitCompileContextV0),
    V1(v1::CommitCompileContextV1),
    V2(v2::CommitCompileContextV2),
    V3(v3::CommitCompileContextV3),
    V4(v4::CommitCompileContextV4),
    V5(v5::CommitCompileContextV5),
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub enum DataScienceCommitKind {
    AddComputation(AddComputationCommit),
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct AddComputationCommit {
    pub node: Node,
    pub analysts: Vec<String>,
    pub enclave_specifications: Vec<EnclaveSpecification>,
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct EnclaveSpecification {
    pub id: String,
    pub attestation_proto_base64: String,
    pub worker_protocol: u32,
}

#[derive(Debug, Clone)]
pub struct EnclaveSpecificationContext {
    pub worker_protocol: u32,
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct Participant {
    pub user: String,
    pub permissions: Vec<ParticipantPermission>,
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub enum ParticipantPermission {
    DataOwner(DataOwnerPermission),
    Analyst(AnalystPermission),
    Manager(ManagerPermission),
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct ManagerPermission {}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct DataOwnerPermission {
    pub node_id: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct AnalystPermission {
    pub node_id: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct Node {
    pub id: String,
    pub name: String,
    pub kind: NodeKind,
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub enum NodeKind {
    Leaf(LeafNode),
    Computation(ComputationNode),
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct LeafNode {
    pub is_required: bool,
    pub kind: LeafNodeKind,
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub enum LeafNodeKind {
    Raw(RawLeafNode),
    Table(TableLeafNode),
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct ComputationNode {
    pub kind: ComputationNodeKind,
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub enum ComputationNodeKind {
    Sql(SqlComputationNode),
    Scripting(ScriptingComputationNode),
    SyntheticData(SyntheticDataComputationNode),
    S3Sink(S3SinkComputationNode),
    Match(MatchingComputationNode),
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct RawLeafNode {}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct TableLeafNode {
    pub sql_specification_id: String,
    pub columns: Vec<TableLeafNodeColumn>,
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct TableLeafNodeColumn {
    pub name: String,
    pub data_format: ColumnDataFormat,
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct ColumnDataFormat {
    pub is_nullable: bool,
    pub data_type: ColumnDataType,
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub enum ColumnDataType {
    Integer,
    Float,
    String,
}

impl From<ColumnDataType> for PrimitiveType {
    fn from(column_data_type: ColumnDataType) -> Self {
        match column_data_type {
            ColumnDataType::Integer => PrimitiveType::Int64,
            ColumnDataType::Float => PrimitiveType::Float64,
            ColumnDataType::String => PrimitiveType::String,
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct SqlComputationNode {
    pub specification_id: String,
    pub statement: String,
    pub privacy_filter: Option<SqlNodePrivacyFilter>,
    pub dependencies: Vec<TableMapping>,
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct TableMapping {
    pub table_name: String,
    pub node_id: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct SqlNodePrivacyFilter {
    pub minimum_rows_count: i64,
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct ScriptingComputationNode {
    pub static_content_specification_id: String,
    pub scripting_specification_id: String,
    pub scripting_language: ScriptingLanguage,
    pub output: String,
    pub main_script: Script,
    pub additional_scripts: Vec<Script>,
    pub dependencies: Vec<String>,
    pub enable_logs_on_error: bool,
    pub enable_logs_on_success: bool,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub minimum_container_memory_size: Option<u64>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub extra_chunk_cache_size_to_available_memory_ratio: Option<f32>,
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub enum ScriptingLanguage {
    Python,
    R,
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct Script {
    pub name: String,
    pub content: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct SyntheticDataComputationNode {
    pub static_content_specification_id: String,
    pub synth_specification_id: String,
    pub columns: Vec<SyntheticNodeColumn>,
    pub dependency: String,
    pub output_original_data_statistics: bool,
    pub epsilon: f32,
    pub enable_logs_on_error: bool,
    pub enable_logs_on_success: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct SyntheticNodeColumn {
    pub index: i32,
    pub name: Option<String>,
    pub should_mask_column: bool,
    pub data_format: ColumnDataFormat,
    pub mask_type: MaskType,
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub enum MaskType {
    GenericString,
    GenericNumber,
    Name,
    Address,
    Postcode,
    PhoneNumber,
    SocialSecurityNumber,
    Email,
    Date,
    Timestamp,
    Iban,
}

impl From<MaskType> for MaskFormat {
    fn from(mask_type: MaskType) -> Self {
        match mask_type {
            MaskType::GenericString => MaskFormat::GenericString,
            MaskType::GenericNumber => MaskFormat::GenericNumber,
            MaskType::Name => MaskFormat::Name,
            MaskType::Address => MaskFormat::Address,
            MaskType::Postcode => MaskFormat::Postcode,
            MaskType::PhoneNumber => MaskFormat::PhoneNumber,
            MaskType::SocialSecurityNumber => MaskFormat::SocialSecurityNumber,
            MaskType::Email => MaskFormat::Email,
            MaskType::Date => MaskFormat::Date,
            MaskType::Timestamp => MaskFormat::Timestamp,
            MaskType::Iban => MaskFormat::Iban,
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
pub enum S3Provider {
    Aws,
    Gcs,
}

impl Default for S3Provider {
    fn default() -> Self {
        S3Provider::Aws
    }
}

impl From<S3Provider> for delta_s3_sink_worker_api::S3Provider {
    fn from(s3_provider: S3Provider) -> Self {
        match s3_provider {
            S3Provider::Aws => delta_s3_sink_worker_api::S3Provider::Aws,
            S3Provider::Gcs => delta_s3_sink_worker_api::S3Provider::Gcs,
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct S3SinkComputationNode {
    pub specification_id: String,
    pub endpoint: String,
    #[serde(default)]
    pub region: String,
    pub credentials_dependency_id: String,
    pub upload_dependency_id: String,
    #[serde(default)]
    pub s3_provider: S3Provider,
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct MatchingComputationNode {
    pub static_content_specification_id: String,
    pub specification_id: String,
    pub output: String,
    pub dependencies: Vec<String>,
    // A JSON string representing the configuration.
    pub config: String,
    pub enable_logs_on_error: bool,
    pub enable_logs_on_success: bool,
}

fn get_dependency_node_name(dependency_id: &String, nodes_map: &HashMap<String, Node>) -> Result<String, CompileError> {
    Ok(nodes_map.get(dependency_id).ok_or_else(|| CompileError("Node not found".to_string()))?.name.clone())
}

fn get_enclave_dependency_node_id(dependency_id: &String, nodes_map: &HashMap<String, Node>) -> Option<String> {
    nodes_map.get(dependency_id).map(get_enclave_dependency_node_id_from_node)
}

pub fn get_enclave_dependency_node_id_from_node(node: &Node) -> String {
    match &node.kind {
        NodeKind::Leaf(leaf_node) => match &leaf_node.kind {
            LeafNodeKind::Raw(_) => node.id.clone(),
            LeafNodeKind::Table(_) => {
                let verification_id = format!("{}_verification", node.id);
                verification_id
            }
        },
        NodeKind::Computation(compute_node) => match &compute_node.kind {
            ComputationNodeKind::Sql(_) => node.id.clone(),
            ComputationNodeKind::Scripting(_) => {
                let container_id = format!("{}_container", node.id);
                container_id
            }
            ComputationNodeKind::SyntheticData(_) => {
                let container_id = format!("{}_container", node.id);
                container_id
            }
            ComputationNodeKind::S3Sink(_) => node.id.clone(),
            ComputationNodeKind::Match(_) => {
                let container_id = format!("{}_match_node", node.id);
                container_id
            }
        },
    }
}

fn get_enclave_dependency_node_id_permissions(
    dependency_id: &String,
    nodes_map: &HashMap<String, Node>,
) -> Option<String> {
    nodes_map.get(dependency_id).map(get_enclave_dependency_node_id_from_node_permissions)
}

pub fn get_enclave_dependency_node_id_from_node_permissions(node: &Node) -> String {
    match &node.kind {
        NodeKind::Leaf(leaf_node) => match &leaf_node.kind {
            LeafNodeKind::Raw(_) => node.id.clone(),
            LeafNodeKind::Table(_) => {
                let verification_id = format!("{}_verification", node.id);
                verification_id
            }
        },
        NodeKind::Computation(compute_node) => match &compute_node.kind {
            ComputationNodeKind::Sql(_) => node.id.clone(),
            ComputationNodeKind::Scripting(_) => {
                let container_id = format!("{}_container", node.id);
                container_id
            }
            ComputationNodeKind::SyntheticData(_) => {
                let container_id = format!("{}_container", node.id);
                container_id
            }
            ComputationNodeKind::S3Sink(_) => node.id.clone(),
            ComputationNodeKind::Match(_) => {
                let container_id = format!("{}_match_filter_node", node.id);
                container_id
            }
        },
    }
}

pub fn get_basic_permissions(enable_development: bool, enable_interactivity: bool) -> Vec<Permission> {
    let mut basic_permissions = vec![
        Permission {
            permission: Some(permission::Permission::RetrieveDataRoomStatusPermission(
                RetrieveDataRoomStatusPermission {},
            )),
        },
        Permission {
            permission: Some(permission::Permission::RetrieveAuditLogPermission(RetrieveAuditLogPermission {})),
        },
        Permission {
            permission: Some(permission::Permission::RetrieveDataRoomPermission(RetrieveDataRoomPermission {})),
        },
        Permission {
            permission: Some(permission::Permission::RetrievePublishedDatasetsPermission(
                RetrievePublishedDatasetsPermission {},
            )),
        },
        Permission { permission: Some(permission::Permission::DryRunPermission(DryRunPermission {})) },
        Permission {
            permission: Some(permission::Permission::CasAuxiliaryStatePermission(CasAuxiliaryStatePermission {})),
        },
        Permission {
            permission: Some(permission::Permission::ReadAuxiliaryStatePermission(ReadAuxiliaryStatePermission {})),
        },
    ];
    if enable_development {
        basic_permissions.push(Permission {
            permission: Some(permission::Permission::ExecuteDevelopmentComputePermission(
                ExecuteDevelopmentComputePermission {},
            )),
        });
    }
    if enable_interactivity {
        basic_permissions.push(Permission {
            permission: Some(permission::Permission::GenerateMergeSignaturePermission(
                GenerateMergeSignaturePermission {},
            )),
        });
        basic_permissions.push(Permission {
            permission: Some(permission::Permission::MergeConfigurationCommitPermission(
                MergeConfigurationCommitPermission {},
            )),
        });
    }
    basic_permissions
}

fn get_enclave_leaf_node_id(dependency_id: &String, nodes_map: &HashMap<String, Node>) -> Option<String> {
    nodes_map.get(dependency_id).and_then(|node| match &node.kind {
        NodeKind::Leaf(leaf_node) => match &leaf_node.kind {
            LeafNodeKind::Raw(_) => Some(node.id.clone()),
            LeafNodeKind::Table(_) => {
                let leaf_id = format!("{}_leaf", node.id);
                Some(leaf_id)
            }
        },
        NodeKind::Computation(_) => None,
    })
}

pub fn add_node_configuration_elements(
    node: Node,
    configuration_elements: &mut Vec<ConfigurationElement>,
    enclave_specifications_map: &HashMap<String, EnclaveSpecificationContext>,
    nodes_map: &HashMap<String, Node>,
) -> Result<(), CompileError> {
    match node.kind {
        NodeKind::Leaf(leaf_node) => match leaf_node.kind {
            LeafNodeKind::Raw(_) => {
                configuration_elements.push(ConfigurationElement {
                    id: node.id,
                    element: Some(Element::ComputeNode(ComputeNode {
                        node_name: node.name,
                        rate_limiting: None,
                        node: Some(compute_node::Node::Leaf(ComputeNodeLeaf { is_required: leaf_node.is_required })),
                    })),
                });
            }
            LeafNodeKind::Table(table_leaf_node) => {
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

                let verification_id = format!("{}_verification", node.id);
                let verification_name = format!("{}_verification", node.name);
                let verification_configuration = SqlWorkerConfiguration {
                    configuration: Some(sql_worker_configuration::Configuration::Validation(ValidationConfiguration {
                        table_schema: Some(TableSchema {
                            named_columns: table_leaf_node
                                .columns
                                .into_iter()
                                .map(|column| NamedColumn {
                                    name: Some(column.name),
                                    column_type: Some(ColumnType {
                                        primitive_type: PrimitiveType::from(column.data_format.data_type) as i32,
                                        nullable: column.data_format.is_nullable,
                                    }),
                                })
                                .collect(),
                        }),
                    })),
                };
                let sql_specification_id = table_leaf_node.sql_specification_id;
                let sql_worker_enclave_metadata =
                    enclave_specifications_map.get(&sql_specification_id).ok_or_else(|| {
                        CompileError(format!("No enclave specification found for '{}'", &sql_specification_id))
                    })?;
                configuration_elements.push(ConfigurationElement {
                    id: verification_id.clone(),
                    element: Some(Element::ComputeNode(ComputeNode {
                        node_name: verification_name,
                        rate_limiting: None,
                        node: Some(compute_node::Node::Branch(ComputeNodeBranch {
                            config: verification_configuration.encode_length_delimited_to_vec(),
                            dependencies: vec![leaf_id],
                            output_format: ComputeNodeFormat::Zip as i32,
                            protocol: Some(ComputeNodeProtocol {
                                version: sql_worker_enclave_metadata.worker_protocol,
                            }),
                            attestation_specification_id: sql_specification_id,
                        })),
                    })),
                });
            }
        },
        NodeKind::Computation(computation_node) => match computation_node.kind {
            ComputationNodeKind::Sql(sql_computation_node) => {
                let dependencies = construct_table_dependency_mappings(&sql_computation_node.dependencies, nodes_map)?;

                let sql_computation_configuration = construct_sql_worker_configuration(
                    &sql_computation_node.statement,
                    &sql_computation_node.privacy_filter,
                    dependencies.iter().map(|(_, _, table_dependency)| table_dependency.clone()),
                );

                let sql_specification_id = sql_computation_node.specification_id;
                let sql_node_metadata = enclave_specifications_map.get(&sql_specification_id).ok_or_else(|| {
                    CompileError(format!("No enclave specification found for '{}'", &sql_specification_id))
                })?;
                configuration_elements.push(ConfigurationElement {
                    id: node.id,
                    element: Some(Element::ComputeNode(ComputeNode {
                        node_name: node.name,
                        rate_limiting: None,
                        node: Some(compute_node::Node::Branch(ComputeNodeBranch {
                            config: sql_computation_configuration.encode_length_delimited_to_vec(),
                            dependencies: dependencies.into_iter().map(|(_, enclave_dep, _)| enclave_dep).collect(),
                            output_format: ComputeNodeFormat::Zip as i32,
                            protocol: Some(ComputeNodeProtocol { version: sql_node_metadata.worker_protocol }),
                            attestation_specification_id: sql_specification_id,
                        })),
                    })),
                });
            }
            ComputationNodeKind::Scripting(scripting_computation_node) => {
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
                let node_dependencies_mount_points = node_dependencies
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
                        .chain(node_dependencies_mount_points.into_iter())
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
            ComputationNodeKind::SyntheticData(synthetic_data_computation_node) => {
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
            ComputationNodeKind::S3Sink(s3_sink_computation_node) => {
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
            ComputationNodeKind::Match(match_node) => {
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
                                    StaticContentConfig { content: include_bytes!("./scripts/match.py").to_vec() },
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
                        rate_limiting: None,
                        node: Some(compute_node::Node::Branch(ComputeNodeBranch {
                            config: container_worker_cfg.encode_length_delimited_to_vec(),
                            dependencies: dependency_ids,
                            output_format: ComputeNodeFormat::Zip as i32,
                            protocol: Some(ComputeNodeProtocol {
                                version: match_node_specification_ctx.worker_protocol,
                            }),
                            attestation_specification_id: match_node.specification_id.clone(),
                        })),
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
                        rate_limiting: None,
                        node: Some(compute_node::Node::Branch(ComputeNodeBranch {
                            config: DriverTaskConfig {
                                driver_task_config: Some(driver_task_config::DriverTaskConfig::StaticContent(
                                    StaticContentConfig {
                                        content: include_bytes!("./scripts/match_filter.py").to_vec(),
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
        },
    }
    Ok(())
}

fn construct_sql_worker_configuration<T: IntoIterator<Item = TableDependencyMapping>>(
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

fn construct_table_dependency_mappings(
    table_mappings: &[TableMapping],
    nodes_map: &HashMap<String, Node>,
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

pub fn add_enclave_specification_configuration_elements(
    enclave_specification: EnclaveSpecification,
    configuration_elements: &mut Vec<ConfigurationElement>,
    enclave_specifications_map: &mut HashMap<String, EnclaveSpecificationContext>,
) -> Result<(), CompileError> {
    let id = enclave_specification.id;
    let attestation_specification_encoded = base64::decode(enclave_specification.attestation_proto_base64)
        .map_err(|err| CompileError(format!("Failed to decode base64 attestation spec '{}': {}", &id, err)))?;
    let attestation_specification: AttestationSpecification =
        Message::decode_length_delimited(attestation_specification_encoded.as_slice())
            .map_err(|err| CompileError(format!("Failed to decode attestation spec '{}': {}", &id, err)))?;
    configuration_elements.push(ConfigurationElement {
        id: id.clone(),
        element: Some(Element::AttestationSpecification(attestation_specification)),
    });
    enclave_specifications_map
        .insert(id, EnclaveSpecificationContext { worker_protocol: enclave_specification.worker_protocol });
    Ok(())
}

pub fn add_participant_permission_configuration_elements(
    participant: Participant,
    basic_permissions: Vec<Permission>,
    configuration_elements: &mut Vec<ConfigurationElement>,
    nodes_map: &HashMap<String, Node>,
) -> Result<(), CompileError> {
    let mut permissions = basic_permissions;
    for permission in participant.permissions {
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
        id: format!("participant_{}", participant.user),
        element: Some(Element::UserPermission(UserPermission {
            email: participant.user,
            permissions,
            authentication_method_id: "authentication_method".to_string(),
        })),
    });

    Ok(())
}

#[derive(Debug, Clone)]
pub struct DataScienceCommitMergeMetadata {
    pub participants: HashMap<String, Participant>,
    pub history_pin_at_commit: [u8; 32],
}

impl DataScienceCommitMergeMetadata {
    pub fn new(participants: &[Participant], history_pin_at_commit: [u8; 32]) -> Self {
        DataScienceCommitMergeMetadata {
            participants: participants
                .iter()
                .cloned()
                .map(|participant| (participant.user.clone(), participant))
                .collect(),
            history_pin_at_commit,
        }
    }
}

#[derive(Clone, Serialize, Deserialize)]
pub struct MatchingComputeNodeConfig {
    query: Expr,
    #[serde(skip_deserializing)]
    round: i16,
    #[serde(skip_deserializing)]
    epsilon: i8,
    #[serde(skip_deserializing)]
    sensitivity: i8,
    #[serde(skip_deserializing)]
    dependency_paths: Vec<String>,
}

#[derive(Clone, Serialize, Deserialize)]
enum Expr {
    #[serde(rename = "or")]
    Or(Vec<Expr>),
    #[serde(rename = "==")]
    Eq(Vec<Expr>),
    #[serde(rename = "and")]
    And(Vec<Expr>),
    #[serde(rename = "var")]
    Var(String),
}

impl MatchingComputeNodeConfig {
    fn set_rounding_and_noise_variables(&mut self, round: i16, epsilon: i8, sensitivity: i8) {
        self.round = round;
        self.epsilon = epsilon;
        self.sensitivity = sensitivity;
    }

    pub(crate) fn set_dependency_paths(&mut self, dependencies: Vec<String>) {
        self.dependency_paths = dependencies;
    }
}

impl TryFrom<&MatchingComputationNode> for MatchingComputeNodeConfig {
    type Error = CompileError;

    fn try_from(node: &MatchingComputationNode) -> Result<Self, Self::Error> {
        let mut cfg: MatchingComputeNodeConfig = serde_json::from_str(&node.config)
            .map_err(|_| CompileError("Failed to deserialise Match node config".to_string()))?;
        cfg.set_rounding_and_noise_variables(100, 1, 10);
        Ok(cfg)
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct DataScienceDataRoomConfiguration {
    pub id: String,
    pub title: String,
    pub description: String,
    pub participants: Vec<Participant>,
    pub nodes: Vec<Node>,
    pub enable_development: bool,
    pub enclave_root_certificate_pem: String,
    pub enclave_specifications: Vec<EnclaveSpecification>,
    pub dcr_secret_id_base64: Option<String>,
}
