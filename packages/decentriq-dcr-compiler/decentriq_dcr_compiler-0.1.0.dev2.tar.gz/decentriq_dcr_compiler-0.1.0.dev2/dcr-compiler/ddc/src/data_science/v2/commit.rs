use delta_data_room_api::configuration_modification::Modification;
use delta_data_room_api::AddModification;
use delta_data_room_api::ChangeModification;
use delta_data_room_api::ConfigurationCommit;
use delta_data_room_api::ConfigurationModification;
use schemars::JsonSchema;
use serde::Deserialize;
use serde::Serialize;
use std::convert::TryInto;

use crate::data_science::shared::get_basic_permissions;
use crate::data_science::shared::AddComputationCommit;
use crate::data_science::shared::AnalystPermission;
use crate::data_science::shared::DataScienceCommitMergeMetadata;
use crate::data_science::shared::Participant;
use crate::data_science::shared::ParticipantPermission;
use crate::data_science::v1::{generate_history_pin, DataScienceCommitV1};
use crate::data_science::v2::{
    add_node_configuration_elements, add_participant_permission_configuration_elements,
    CommitCompileContextV2, LeafNodeKindV2, NodeKindV2, NodeV2,
};
use crate::data_science::v3::DataScienceCommitV3;
use crate::data_science::{
    add_enclave_specification_configuration_elements, CompileVersion, DataScienceCommitKind,
    EnclaveSpecification,
};
use crate::error::*;
use crate::Compile;

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub enum DataScienceCommitKindV2 {
    AddComputation(AddComputationCommitV2),
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct AddComputationCommitV2 {
    pub node: NodeV2,
    pub analysts: Vec<String>,
    pub enclave_specifications: Vec<EnclaveSpecification>,
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct DataScienceCommitV2 {
    pub id: String,
    pub name: String,
    pub enclave_data_room_id: String,
    pub history_pin: String,
    pub kind: DataScienceCommitKindV2,
}

impl DataScienceCommitV2 {
    pub fn upgrade(self) -> DataScienceCommitV3 {
        DataScienceCommitV3 {
            id: self.id,
            name: self.name,
            enclave_data_room_id: self.enclave_data_room_id,
            history_pin: self.history_pin,
            kind: self.kind,
        }
    }
    pub fn downgrade(self) -> Result<DataScienceCommitV1, CompileError> {
        Ok(DataScienceCommitV1 {
            id: self.id,
            name: self.name,
            enclave_data_room_id: self.enclave_data_room_id,
            history_pin: self.history_pin,
            kind: match self.kind {
                DataScienceCommitKindV2::AddComputation(add) => {
                    let node = add.node.clone();
                    match add.node.kind {
                        NodeKindV2::Leaf(leaf) => match leaf.kind {
                            LeafNodeKindV2::Table(_table) => {
                                DataScienceCommitKind::AddComputation(AddComputationCommit {
                                    node: node.try_into()?,
                                    analysts: add.analysts,
                                    enclave_specifications: add.enclave_specifications,
                                })
                            }
                            LeafNodeKindV2::Raw(_raw) => {
                                DataScienceCommitKind::AddComputation(AddComputationCommit {
                                    node: node.try_into()?,
                                    analysts: add.analysts,
                                    enclave_specifications: add.enclave_specifications,
                                })
                            }
                        },
                        NodeKindV2::Computation(_compute) => {
                            DataScienceCommitKind::AddComputation(AddComputationCommit {
                                node: node.try_into()?,
                                analysts: add.analysts,
                                enclave_specifications: add.enclave_specifications,
                            })
                        }
                    }
                }
            },
        })
    }

    pub fn version(&self) -> CompileVersion {
        CompileVersion::V2
    }
}

fn check_mergeability(
    context: &CommitCompileContextV2,
    incoming: &DataScienceCommitV2,
) -> Result<(), CompileError> {
    match &incoming.kind {
        DataScienceCommitKindV2::AddComputation(AddComputationCommitV2 {
            node,
            analysts: _,
            enclave_specifications: _,
        }) => {
            if context.nodes_map.contains_key(&node.id) {
                return Err(CompileError(
                    "Merge conflict: Trying to add node that was added previously".to_string(),
                ));
            }
        }
    }
    Ok(())
}

impl Compile for DataScienceCommitV2 {
    type LowLevelOutput = ConfigurationCommit;
    type HighLevelOutput = Self;
    type CompileContext = CommitCompileContextV2;
    type OutputContext = CommitCompileContextV2;

    fn compile(
        self,
        mut context: Self::CompileContext,
    ) -> Result<Self::CompileOutput, CompileError> {
        let self_clone = self.clone();

        let data_room_id = hex::decode(&self.enclave_data_room_id)
            .map_err(|err| format!("Failed to decode enclave_data_room_id: {err}"))?;

        let all_pins = context.all_pins(&data_room_id);
        let history_pin = hex::decode(&self.history_pin)
            .map_err(|err| format!("Failed to decode history_pin: {err}"))?;

        let is_linear_commit = all_pins
            .iter()
            .position(|pin| pin.as_slice() == history_pin.as_slice())
            .ok_or("History pin does not refer to an existing history")?
            == all_pins.len() - 1;

        if !is_linear_commit {
            check_mergeability(&context, &self)?;
        }

        match self.kind {
            DataScienceCommitKindV2::AddComputation(add_computation_commit) => {
                let mut new_configuration_elements = vec![];

                let new_node = add_computation_commit.node.clone();

                context
                    .nodes_map
                    .try_insert(new_node.id.clone(), new_node)
                    .map_err(|err| {
                        CompileError(format!("Node with id {} already exists", err.entry.key()))
                    })?;

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
                        if is_linear_commit {
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
                            if let Some(mut participant) = context
                                .participant_at_history_pin(&data_room_id, &history_pin, &analyst)?
                                .cloned()
                            {
                                participant.permissions.push(ParticipantPermission::Analyst(
                                    AnalystPermission {
                                        node_id: node_id.clone(),
                                    },
                                ));
                                add_participant_permission_configuration_elements(
                                    participant,
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
                                    permissions: vec![ParticipantPermission::Analyst(
                                        AnalystPermission {
                                            node_id: node_id.clone(),
                                        },
                                    )],
                                };
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

                let data_room_history_pin = hex::decode(&self.history_pin)
                    .map_err(|err| format!("Failed to decode history_pin: {err}"))?;

                let configuration_commit = ConfigurationCommit {
                    id: self.id,
                    name: self.name,
                    data_room_id: data_room_id.clone(),
                    data_room_history_pin: data_room_history_pin.to_vec(),
                    modifications,
                };

                context.previous_commits.push((
                    self_clone.clone(),
                    configuration_commit.clone(),
                    DataScienceCommitMergeMetadata::new(
                        &context.participants,
                        generate_history_pin(
                            &data_room_id,
                            context
                                .previous_commits
                                .iter()
                                .map(|(_, commit, _)| commit)
                                .chain(std::iter::once(&configuration_commit)),
                        ),
                    ),
                ));

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
