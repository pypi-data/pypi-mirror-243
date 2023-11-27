use delta_data_room_api::configuration_element::Element;
use delta_data_room_api::governance_protocol::Policy;
use delta_data_room_api::AffectedDataOwnersApprovePolicy;
use delta_data_room_api::AuthenticationMethod;
use delta_data_room_api::ConfigurationCommit;
use delta_data_room_api::ConfigurationElement;
use delta_data_room_api::DataRoom;
use delta_data_room_api::DataRoomConfiguration;
use delta_data_room_api::DcrSecretPolicy;
use delta_data_room_api::GovernanceProtocol;
use delta_data_room_api::PkiPolicy;
use delta_data_room_api::StaticDataRoomPolicy;
use schemars::JsonSchema;
use serde::Deserialize;
use serde::Serialize;
use std::collections::HashMap;

use crate::data_science::shared::get_basic_permissions;
use crate::data_science::v2::{
    add_node_configuration_elements, add_participant_permission_configuration_elements,
    CommitCompileContextV2, DataScienceCommitV2, NodeV2,
};
use crate::data_science::v3::{
    DataScienceDataRoomConfigurationV3, DataScienceDataRoomV3, InteractiveDataScienceDataRoomV3,
};
use crate::data_science::{
    add_enclave_specification_configuration_elements, CompileVersion, EnclaveSpecification,
    Participant,
};
use crate::error::CompileError;
use crate::error::VerificationError;
use crate::Compile;

use super::super::v0::DataRoomCompileContextV0;

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub enum DataScienceDataRoomV2 {
    Static(DataScienceDataRoomConfigurationV2),
    Interactive(InteractiveDataScienceDataRoomV2),
}

impl DataScienceDataRoomV2 {
    pub fn version(&self) -> CompileVersion {
        CompileVersion::V2
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct DataScienceDataRoomConfigurationV2 {
    pub id: String,
    pub title: String,
    pub description: String,
    pub participants: Vec<Participant>,
    pub nodes: Vec<NodeV2>,
    pub enable_development: bool,
    pub enclave_root_certificate_pem: String,
    pub enclave_specifications: Vec<EnclaveSpecification>,
    pub dcr_secret_id_base64: Option<String>,
    pub enable_serverside_wasm_validation: bool,
    pub enable_test_datasets: bool,
    pub enable_post_worker: bool,
    pub enable_sqlite_worker: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct InteractiveDataScienceDataRoomV2 {
    pub initial_configuration: DataScienceDataRoomConfigurationV2,
    pub commits: Vec<DataScienceCommitV2>,
    pub enable_automerge_feature: bool,
}

fn compile_configuration(
    configuration: DataScienceDataRoomConfigurationV2,
    enable_interactivity: bool,
) -> Result<(DataRoom, CommitCompileContextV2), CompileError> {
    let mut configuration_elements = vec![];

    let nodes_map = configuration
        .nodes
        .iter()
        .map(|node| (node.id.clone(), node.clone()))
        .collect::<HashMap<_, _>>();

    let mut enclave_specifications_map = HashMap::new();

    for enclave_specification in configuration.enclave_specifications {
        add_enclave_specification_configuration_elements(
            enclave_specification,
            &mut configuration_elements,
            &mut enclave_specifications_map,
        )?;
    }

    for node in configuration.nodes {
        add_node_configuration_elements(
            node,
            &mut configuration_elements,
            &enclave_specifications_map,
            &nodes_map,
        )?;
    }
    let dcr_secret_id = match configuration.dcr_secret_id_base64 {
        Some(secret_id) => {
            let decoded = base64::decode(secret_id)
                .map_err(|err| CompileError(format!("Failed to decode dcr secret id: {}", err)))?;
            Some(DcrSecretPolicy {
                dcr_secret_id: decoded,
            })
        }
        None => None,
    };

    configuration_elements.push(ConfigurationElement {
        id: "authentication_method".to_string(),
        element: Some(Element::AuthenticationMethod(AuthenticationMethod {
            personal_pki: None,
            dq_pki: Some(PkiPolicy {
                root_certificate_pem: configuration.enclave_root_certificate_pem.into_bytes(),
            }),
            dcr_secret: dcr_secret_id,
        })),
    });

    for participant in configuration.participants.iter() {
        add_participant_permission_configuration_elements(
            participant.clone(),
            get_basic_permissions(configuration.enable_development, enable_interactivity),
            &mut configuration_elements,
            &nodes_map,
        )?;
    }

    let policy = if enable_interactivity {
        Policy::AffectedDataOwnersApprovePolicy(AffectedDataOwnersApprovePolicy {})
    } else {
        Policy::StaticDataRoomPolicy(StaticDataRoomPolicy {})
    };
    let data_room = DataRoom {
        id: configuration.id,
        name: configuration.title,
        description: configuration.description,
        governance_protocol: Some(GovernanceProtocol {
            policy: Some(policy),
        }),
        initial_configuration: Some(DataRoomConfiguration {
            elements: configuration_elements,
        }),
    };

    let initial_participants = configuration
        .participants
        .iter()
        .cloned()
        .map(|p| (p.user.clone(), p))
        .collect();

    let output_context = CommitCompileContextV2 {
        nodes_map,
        enclave_specifications_map,
        participants: configuration.participants,
        enable_development: configuration.enable_development,
        enable_interactivity,
        initial_participants,
        previous_commits: vec![],
    };

    Ok((data_room, output_context))
}

impl Compile for DataScienceDataRoomV2 {
    type LowLevelOutput = (DataRoom, Vec<ConfigurationCommit>);
    type HighLevelOutput = Self;
    type CompileContext = DataRoomCompileContextV0;
    type OutputContext = CommitCompileContextV2;

    fn compile(self, _: Self::CompileContext) -> Result<Self::CompileOutput, CompileError> {
        let self_clone = self.clone();
        match self_clone {
            DataScienceDataRoomV2::Interactive(interactive_data_room) => {
                let (data_room, mut output_context) =
                    compile_configuration(interactive_data_room.initial_configuration, true)?;
                let mut configuration_commits = vec![];
                for commit in interactive_data_room.commits {
                    let (configuration_commit, _, commit_context) =
                        commit.compile(output_context)?;
                    configuration_commits.push(configuration_commit);
                    output_context = commit_context;
                }
                Ok(((data_room, configuration_commits), self, output_context))
            }
            DataScienceDataRoomV2::Static(static_data_room) => {
                let (data_room, output_context) = compile_configuration(static_data_room, false)?;
                Ok(((data_room, vec![]), self, output_context))
            }
        }
    }

    fn verify(
        low_level_output: Self::LowLevelOutput,
        high_level_output: Self::HighLevelOutput,
        context: Self::CompileContext,
    ) -> Result<Self, VerificationError>
    where
        Self: Sized,
    {
        let (re_compiled, re_high_level_output, _) = high_level_output.compile(context)?;
        if re_compiled == low_level_output {
            Ok(re_high_level_output)
        } else {
            Err(VerificationError::Other(format!(
                "Expected: {:?} but got: {:?}",
                low_level_output, re_compiled
            )))
        }
    }
}

impl DataScienceDataRoomV2 {
    pub fn upgrade(self) -> DataScienceDataRoomV3 {
        match self {
            DataScienceDataRoomV2::Static(dcr) => {
                DataScienceDataRoomV3::Static(DataScienceDataRoomConfigurationV3 {
                    id: dcr.id,
                    title: dcr.title,
                    description: dcr.description,
                    participants: dcr.participants,
                    nodes: dcr.nodes,
                    enable_development: dcr.enable_development,
                    enclave_root_certificate_pem: dcr.enclave_root_certificate_pem,
                    enclave_specifications: dcr.enclave_specifications,
                    dcr_secret_id_base64: dcr.dcr_secret_id_base64,
                    enable_serverside_wasm_validation: dcr.enable_serverside_wasm_validation,
                    enable_test_datasets: dcr.enable_test_datasets,
                    enable_post_worker: dcr.enable_post_worker,
                    enable_sqlite_worker: dcr.enable_sqlite_worker,
                    enable_safe_python_worker_stacktrace: false,
                })
            }
            DataScienceDataRoomV2::Interactive(dcr) => {
                DataScienceDataRoomV3::Interactive(InteractiveDataScienceDataRoomV3 {
                    initial_configuration: DataScienceDataRoomConfigurationV3 {
                        id: dcr.initial_configuration.id,
                        title: dcr.initial_configuration.title,
                        description: dcr.initial_configuration.description,
                        participants: dcr.initial_configuration.participants,
                        nodes: dcr.initial_configuration.nodes,
                        enable_development: dcr.initial_configuration.enable_development,
                        enclave_root_certificate_pem: dcr
                            .initial_configuration
                            .enclave_root_certificate_pem,
                        enclave_specifications: dcr.initial_configuration.enclave_specifications,
                        dcr_secret_id_base64: dcr.initial_configuration.dcr_secret_id_base64,
                        enable_serverside_wasm_validation: dcr
                            .initial_configuration
                            .enable_serverside_wasm_validation,
                        enable_test_datasets: dcr.initial_configuration.enable_test_datasets,
                        enable_post_worker: dcr.initial_configuration.enable_post_worker,
                        enable_sqlite_worker: dcr.initial_configuration.enable_sqlite_worker,
                        enable_safe_python_worker_stacktrace: false,
                    },
                    commits: dcr
                        .commits
                        .into_iter()
                        .map(|commit| commit.upgrade())
                        .collect(),
                    enable_automerge_feature: dcr.enable_automerge_feature,
                })
            }
        }
    }
}
