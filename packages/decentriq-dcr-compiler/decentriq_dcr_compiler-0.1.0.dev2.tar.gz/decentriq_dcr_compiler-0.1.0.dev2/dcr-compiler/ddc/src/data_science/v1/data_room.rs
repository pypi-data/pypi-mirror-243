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

use crate::data_science::shared::add_enclave_specification_configuration_elements;
use crate::data_science::shared::add_node_configuration_elements;
use crate::data_science::shared::add_participant_permission_configuration_elements;
use crate::data_science::shared::get_basic_permissions;
use crate::data_science::shared::DataScienceDataRoomConfiguration;
use crate::data_science::v2::{
    DataScienceDataRoomConfigurationV2, DataScienceDataRoomV2, InteractiveDataScienceDataRoomV2,
};
use crate::data_science::CompileVersion;
use crate::error::CompileError;
use crate::error::VerificationError;
use crate::Compile;

use super::super::v0::DataRoomCompileContextV0;
use super::CommitCompileContextV1;
use super::DataScienceCommitV1;

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub enum DataScienceDataRoomV1 {
    Static(DataScienceDataRoomConfiguration),
    Interactive(InteractiveDataScienceDataRoomV1),
}

impl DataScienceDataRoomV1 {
    pub fn upgrade(self) -> DataScienceDataRoomV2 {
        match self {
            DataScienceDataRoomV1::Static(static_data_room) => {
                DataScienceDataRoomV2::Static(DataScienceDataRoomConfigurationV2 {
                    id: static_data_room.id,
                    title: static_data_room.title,
                    description: static_data_room.description,
                    participants: static_data_room.participants,
                    nodes: static_data_room
                        .nodes
                        .into_iter()
                        .map(|node| node.into())
                        .collect(),
                    enable_development: static_data_room.enable_development,
                    enclave_root_certificate_pem: static_data_room.enclave_root_certificate_pem,
                    enclave_specifications: static_data_room.enclave_specifications,
                    dcr_secret_id_base64: static_data_room.dcr_secret_id_base64,
                    enable_serverside_wasm_validation: false,
                    enable_test_datasets: false,
                    enable_post_worker: false,
                    enable_sqlite_worker: false,
                })
            }
            DataScienceDataRoomV1::Interactive(interactive_data_room) => {
                DataScienceDataRoomV2::Interactive(InteractiveDataScienceDataRoomV2 {
                    initial_configuration: DataScienceDataRoomConfigurationV2 {
                        id: interactive_data_room.initial_configuration.id,
                        title: interactive_data_room.initial_configuration.title,
                        description: interactive_data_room.initial_configuration.description,
                        participants: interactive_data_room.initial_configuration.participants,
                        nodes: interactive_data_room
                            .initial_configuration
                            .nodes
                            .into_iter()
                            .map(|node| node.into())
                            .collect(),
                        enable_development: interactive_data_room
                            .initial_configuration
                            .enable_development,
                        enclave_root_certificate_pem: interactive_data_room
                            .initial_configuration
                            .enclave_root_certificate_pem,
                        enclave_specifications: interactive_data_room
                            .initial_configuration
                            .enclave_specifications,
                        dcr_secret_id_base64: interactive_data_room
                            .initial_configuration
                            .dcr_secret_id_base64,
                        enable_serverside_wasm_validation: false,
                        enable_test_datasets: false,
                        enable_post_worker: false,
                        enable_sqlite_worker: false,
                    },
                    commits: interactive_data_room
                        .commits
                        .into_iter()
                        .map(|commit| commit.upgrade())
                        .collect(),
                    enable_automerge_feature: interactive_data_room.enable_automerge_feature,
                })
            }
        }
    }

    pub fn version(&self) -> CompileVersion {
        CompileVersion::V1
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct InteractiveDataScienceDataRoomV1 {
    pub initial_configuration: DataScienceDataRoomConfiguration,
    pub commits: Vec<DataScienceCommitV1>,
    pub enable_automerge_feature: bool,
}

fn compile_configuration(
    configuration: DataScienceDataRoomConfiguration,
    enable_interactivity: bool,
) -> Result<(DataRoom, CommitCompileContextV1), CompileError> {
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

    let output_context = CommitCompileContextV1 {
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

impl Compile for DataScienceDataRoomV1 {
    type LowLevelOutput = (DataRoom, Vec<ConfigurationCommit>);
    type HighLevelOutput = Self;
    type CompileContext = DataRoomCompileContextV0;
    type OutputContext = CommitCompileContextV1;

    fn compile(self, _: Self::CompileContext) -> Result<Self::CompileOutput, CompileError> {
        let self_clone = self.clone();
        match self_clone {
            DataScienceDataRoomV1::Interactive(interactive_data_room) => {
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
            DataScienceDataRoomV1::Static(static_data_room) => {
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
