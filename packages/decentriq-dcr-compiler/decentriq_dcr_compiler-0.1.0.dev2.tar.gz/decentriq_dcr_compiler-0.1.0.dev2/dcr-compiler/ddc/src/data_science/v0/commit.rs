use delta_data_room_api::configuration_modification::Modification;
use delta_data_room_api::AddModification;
use delta_data_room_api::ChangeModification;
use delta_data_room_api::ConfigurationCommit;
use delta_data_room_api::ConfigurationModification;
use schemars::JsonSchema;
use serde::Deserialize;
use serde::Serialize;

use crate::data_science::CompileVersion;
use crate::data_science::shared::AnalystPermission;
use crate::data_science::shared::DataScienceCommitKind;
use crate::data_science::shared::Participant;
use crate::data_science::shared::ParticipantPermission;
use crate::data_science::shared::add_enclave_specification_configuration_elements;
use crate::data_science::shared::add_node_configuration_elements;
use crate::data_science::shared::add_participant_permission_configuration_elements;
use crate::data_science::shared::get_basic_permissions;
use crate::data_science::v1::DataScienceCommitV1;
use crate::error::*;
use crate::Compile;

use super::CommitCompileContextV0;

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct DataScienceCommitV0 {
    pub id: String,
    pub name: String,
    pub enclave_data_room_id: String,
    pub history_pin: String,
    pub kind: DataScienceCommitKind,
}

impl DataScienceCommitV0 {
    pub fn upgrade(self) -> DataScienceCommitV1 {
        DataScienceCommitV1 { 
            id: self.id, 
            name: self.name, 
            enclave_data_room_id: self.enclave_data_room_id, 
            history_pin: self.history_pin, 
            kind: self.kind,
        }
    }

    pub fn version(&self) -> CompileVersion {
        CompileVersion::V0
    }
}

impl Compile for DataScienceCommitV0 {
    type LowLevelOutput = ConfigurationCommit;
    type HighLevelOutput = Self;
    type CompileContext = CommitCompileContextV0;
    type OutputContext = CommitCompileContextV0;

    fn compile(
        self,
        mut context: Self::CompileContext,
    ) -> Result<Self::CompileOutput, CompileError> {
        let self_clone = self.clone();
        match self.kind {
            DataScienceCommitKind::AddComputation(add_computation_commit) => {
                let mut new_configuration_elements = vec![];

                let new_node = add_computation_commit.node.clone();
                context.nodes_map.insert(new_node.id.clone(), new_node);

                for enclave_specification in add_computation_commit.enclave_specifications {
                    add_enclave_specification_configuration_elements(
                        enclave_specification,
                        &mut new_configuration_elements,
                        &mut context.enclave_specifications_map,
                    )?;
                }
                let node_id = add_computation_commit.node.id.clone();

                add_node_configuration_elements(
                    add_computation_commit.node,
                    &mut new_configuration_elements,
                    &context.enclave_specifications_map,
                    &context.nodes_map,
                )?;

                let mut updated_configuration_elements = vec![];
                for analyst in add_computation_commit.analysts {
                    if let Some(participant) = context
                        .participants
                        .iter_mut()
                        .find(|participant| participant.user == analyst)
                    {
                        participant.permissions.push(ParticipantPermission::Analyst(
                            AnalystPermission {
                                node_id: node_id.clone(),
                            },
                        ));
                        add_participant_permission_configuration_elements(
                            participant.clone(),
                            get_basic_permissions(
                                context.enable_development,
                                context.enable_interactivity,
                            ),
                            &mut updated_configuration_elements,
                            &context.nodes_map,
                        )?;
                    } else {
                        let participant = Participant {
                            user: analyst,
                            permissions: vec![ParticipantPermission::Analyst(AnalystPermission {
                                node_id: node_id.clone(),
                            })],
                        };
                        context.participants.push(participant.clone());
                        add_participant_permission_configuration_elements(
                            participant,
                            get_basic_permissions(
                                context.enable_development,
                                context.enable_interactivity,
                            ),
                            &mut new_configuration_elements,
                            &context.nodes_map,
                        )?;
                    }
                }

                let modifications = new_configuration_elements
                    .into_iter()
                    .map(|new_configuration_element| ConfigurationModification {
                        modification: Some(Modification::Add(AddModification {
                            element: Some(new_configuration_element),
                        })),
                    })
                    .chain(updated_configuration_elements.into_iter().map(
                        |updated_configuration_element| ConfigurationModification {
                            modification: Some(Modification::Change(ChangeModification {
                                element: Some(updated_configuration_element),
                            })),
                        },
                    ))
                    .collect::<Vec<_>>();

                let configuration_commit = ConfigurationCommit {
                    id: self.id,
                    name: self.name,
                    data_room_id: hex::decode(&self.enclave_data_room_id).map_err(|err| {
                        CompileError(format!("failed to decode enclave_data_room_id: {:?}", err))
                    })?,
                    data_room_history_pin: hex::decode(&self.history_pin).map_err(|err| {
                        CompileError(format!("failed to decode history pin: {:?}", err))
                    })?,
                    modifications,
                };
                Ok((configuration_commit, self_clone, context))
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
