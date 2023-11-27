use std::collections::HashMap;

use crate::data_science::CompileVersion;
use crate::data_science::shared::DataScienceDataRoomConfiguration;
use crate::data_science::shared::add_enclave_specification_configuration_elements;
use crate::data_science::shared::add_node_configuration_elements;
use crate::data_science::shared::add_participant_permission_configuration_elements;
use crate::data_science::shared::get_basic_permissions;
use crate::data_science::v1::DataScienceDataRoomV1;
use crate::data_science::v1::InteractiveDataScienceDataRoomV1;

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

use crate::error::*;
use crate::Compile;

use super::CommitCompileContextV0;
use super::DataRoomCompileContextV0;
use super::DataScienceCommitV0;

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub enum DataScienceDataRoomV0 {
    Static(DataScienceDataRoomConfiguration),
    Interactive(InteractiveDataScienceDataRoomV0),
}

impl DataScienceDataRoomV0 {
    pub fn upgrade(self) -> DataScienceDataRoomV1 {
        match self {
            DataScienceDataRoomV0::Static(static_data_room) => DataScienceDataRoomV1::Static(static_data_room),
            DataScienceDataRoomV0::Interactive(interactive_data_room) => DataScienceDataRoomV1::Interactive(
                InteractiveDataScienceDataRoomV1 {
                    initial_configuration: interactive_data_room.initial_configuration,
                    commits: interactive_data_room.commits.into_iter().map(|v0_commit| v0_commit.upgrade()).collect(),
                    enable_automerge_feature: false,
            }),
        }
    }

    pub fn version(&self) -> CompileVersion {
        CompileVersion::V0
    }
}


#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct InteractiveDataScienceDataRoomV0 {
    pub initial_configuration: DataScienceDataRoomConfiguration,
    pub commits: Vec<DataScienceCommitV0>,
}

fn compile_configuration(
    configuration: DataScienceDataRoomConfiguration,
    enable_interactivity: bool,
) -> Result<(DataRoom, CommitCompileContextV0), CompileError> {
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
    let output_context = CommitCompileContextV0 {
        nodes_map,
        enclave_specifications_map,
        participants: configuration.participants,
        enable_development: configuration.enable_development,
        enable_interactivity,
    };

    Ok((data_room, output_context))
}

impl Compile for DataScienceDataRoomV0 {
    type LowLevelOutput = (DataRoom, Vec<ConfigurationCommit>);
    type HighLevelOutput = Self;
    type CompileContext = DataRoomCompileContextV0;
    type OutputContext = CommitCompileContextV0;

    fn compile(self, _: Self::CompileContext) -> Result<Self::CompileOutput, CompileError> {
        let self_clone = self.clone();
        match self_clone {
            DataScienceDataRoomV0::Interactive(interactive_data_room) => {
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
            DataScienceDataRoomV0::Static(static_data_room) => {
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
