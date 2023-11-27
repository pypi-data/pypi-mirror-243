use delta_data_room_api::configuration_modification::Modification;
use delta_data_room_api::AddModification;
use delta_data_room_api::ChangeModification;
use delta_data_room_api::ConfigurationCommit;
use delta_data_room_api::ConfigurationModification;
use schemars::JsonSchema;
use serde::Deserialize;
use serde::Serialize;

use super::generate_history_pin;
use super::CommitCompileContextV1;
use crate::data_science::shared::add_enclave_specification_configuration_elements;
use crate::data_science::shared::add_node_configuration_elements;
use crate::data_science::shared::add_participant_permission_configuration_elements;
use crate::data_science::shared::get_basic_permissions;
use crate::data_science::shared::AddComputationCommit;
use crate::data_science::shared::AnalystPermission;
use crate::data_science::shared::DataScienceCommitKind;
use crate::data_science::shared::DataScienceCommitMergeMetadata;
use crate::data_science::shared::Participant;
use crate::data_science::shared::ParticipantPermission;
use crate::data_science::v0::DataScienceCommitV0;
use crate::data_science::v2::AddComputationCommitV2;
use crate::data_science::v2::DataScienceCommitKindV2;
use crate::data_science::v2::DataScienceCommitV2;
use crate::data_science::CompileVersion;
use crate::data_science::LeafNodeKind;
use crate::data_science::NodeKind;
use crate::error::*;
use crate::Compile;

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct DataScienceCommitV1 {
    pub id: String,
    pub name: String,
    pub enclave_data_room_id: String,
    pub history_pin: String,
    pub kind: DataScienceCommitKind,
}

impl DataScienceCommitV1 {
    pub fn upgrade(self) -> DataScienceCommitV2 {
        DataScienceCommitV2 {
            id: self.id,
            name: self.name,
            enclave_data_room_id: self.enclave_data_room_id,
            history_pin: self.history_pin,
            kind: match self.kind {
                DataScienceCommitKind::AddComputation(add) => {
                    let node = add.node.clone();
                    match add.node.kind {
                        NodeKind::Leaf(leaf) => match leaf.kind {
                            LeafNodeKind::Raw(_raw) => {
                                DataScienceCommitKindV2::AddComputation(AddComputationCommitV2 {
                                    node: node.into(),
                                    analysts: add.analysts,
                                    enclave_specifications: add.enclave_specifications,
                                })
                            }
                            LeafNodeKind::Table(_table) => {
                                DataScienceCommitKindV2::AddComputation(AddComputationCommitV2 {
                                    node: node.into(),
                                    analysts: add.analysts,
                                    enclave_specifications: add.enclave_specifications,
                                })
                            }
                        },
                        NodeKind::Computation(_compute) => {
                            DataScienceCommitKindV2::AddComputation(AddComputationCommitV2 {
                                node: node.into(),
                                analysts: add.analysts,
                                enclave_specifications: add.enclave_specifications,
                            })
                        }
                    }
                }
            },
        }
    }

    pub fn downgrade(self) -> Result<DataScienceCommitV0, CompileError> {
        Ok(DataScienceCommitV0 {
            id: self.id,
            name: self.name,
            enclave_data_room_id: self.enclave_data_room_id,
            history_pin: self.history_pin,
            kind: self.kind,
        })
    }

    pub fn version(&self) -> CompileVersion {
        CompileVersion::V1
    }
}

fn check_mergeability(context: &CommitCompileContextV1, incoming: &DataScienceCommitV1) -> Result<(), CompileError> {
    match &incoming.kind {
        DataScienceCommitKind::AddComputation(AddComputationCommit {
            node,
            analysts: _,
            enclave_specifications: _,
        }) => {
            if context.nodes_map.contains_key(&node.id) {
                return Err(CompileError("Merge conflict: Trying to add node that was added previously".to_string()));
            }
        }
    }
    Ok(())
}

impl Compile for DataScienceCommitV1 {
    type CompileContext = CommitCompileContextV1;
    type HighLevelOutput = Self;
    type LowLevelOutput = ConfigurationCommit;
    type OutputContext = CommitCompileContextV1;

    fn compile(self, mut context: Self::CompileContext) -> Result<Self::CompileOutput, CompileError> {
        let self_clone = self.clone();

        let data_room_id = hex::decode(&self.enclave_data_room_id)
            .map_err(|err| format!("Failed to decode enclave_data_room_id: {err}"))?;

        let all_pins = context.all_pins(&data_room_id);
        let history_pin =
            hex::decode(&self.history_pin).map_err(|err| format!("Failed to decode history_pin: {err}"))?;

        let is_linear_commit = all_pins
            .iter()
            .position(|pin| pin.as_slice() == history_pin.as_slice())
            .ok_or("History pin does not refer to an existing history")?
            == all_pins.len() - 1;

        if !is_linear_commit {
            check_mergeability(&context, &self)?;
        }

        match self.kind {
            DataScienceCommitKind::AddComputation(add_computation_commit) => {
                let mut new_configuration_elements = vec![];

                let new_node = add_computation_commit.node.clone();

                context
                    .nodes_map
                    .try_insert(new_node.id.clone(), new_node)
                    .map_err(|err| CompileError(format!("Node with id {} already exists", err.entry.key())))?;

                for enclave_specification in add_computation_commit.enclave_specifications {
                    add_enclave_specification_configuration_elements(
                        enclave_specification, &mut new_configuration_elements, &mut context.enclave_specifications_map,
                    )?;
                }
                let node_id = add_computation_commit.node.id.clone();

                add_node_configuration_elements(
                    add_computation_commit.node, &mut new_configuration_elements, &context.enclave_specifications_map,
                    &context.nodes_map,
                )?;

                let mut updated_configuration_elements = vec![];
                for analyst in add_computation_commit.analysts {
                    if let Some(participant) =
                        context.participants.iter_mut().find(|participant| participant.user == analyst)
                    {
                        participant
                            .permissions
                            .push(ParticipantPermission::Analyst(AnalystPermission { node_id: node_id.clone() }));
                        if is_linear_commit {
                            add_participant_permission_configuration_elements(
                                participant.clone(),
                                get_basic_permissions(context.enable_development, context.enable_interactivity),
                                &mut updated_configuration_elements,
                                &context.nodes_map,
                            )?;
                        } else {
                            if let Some(mut participant) =
                                context.participant_at_history_pin(&data_room_id, &history_pin, &analyst)?.cloned()
                            {
                                participant.permissions.push(ParticipantPermission::Analyst(AnalystPermission {
                                    node_id: node_id.clone(),
                                }));
                                add_participant_permission_configuration_elements(
                                    participant,
                                    get_basic_permissions(context.enable_development, context.enable_interactivity),
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
                                add_participant_permission_configuration_elements(
                                    participant,
                                    get_basic_permissions(context.enable_development, context.enable_interactivity),
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
                            get_basic_permissions(context.enable_development, context.enable_interactivity),
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
                    .chain(updated_configuration_elements.into_iter().map(|updated_configuration_element| {
                        ConfigurationModification {
                            modification: Some(Modification::Change(ChangeModification {
                                element: Some(updated_configuration_element),
                            })),
                        }
                    }))
                    .collect::<Vec<_>>();

                let data_room_history_pin =
                    hex::decode(&self.history_pin).map_err(|err| format!("Failed to decode history_pin: {err}"))?;

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
            Err(VerificationError::Other(format!("Expected: {:?} but got: {:?}", low_level_output, re_compiled)))
        }
    }
}

#[cfg(test)]
mod tests {

    use super::AddComputationCommit;
    use super::DataScienceCommitV1;
    use crate::data_science::shared::AnalystPermission;
    use crate::data_science::shared::ColumnDataFormat;
    use crate::data_science::shared::ColumnDataType;
    use crate::data_science::shared::ComputationNode;
    use crate::data_science::shared::ComputationNodeKind;
    use crate::data_science::shared::DataOwnerPermission;
    use crate::data_science::shared::DataScienceCommitKind;
    use crate::data_science::shared::DataScienceDataRoomConfiguration;
    use crate::data_science::shared::EnclaveSpecification;
    use crate::data_science::shared::LeafNode;
    use crate::data_science::shared::LeafNodeKind;
    use crate::data_science::shared::ManagerPermission;
    use crate::data_science::shared::Node;
    use crate::data_science::shared::NodeKind;
    use crate::data_science::shared::Participant;
    use crate::data_science::shared::ParticipantPermission;
    use crate::data_science::shared::S3SinkComputationNode;
    use crate::data_science::shared::Script;
    use crate::data_science::shared::ScriptingComputationNode;
    use crate::data_science::shared::ScriptingLanguage;
    use crate::data_science::shared::TableLeafNode;
    use crate::data_science::shared::TableLeafNodeColumn;
    use crate::data_science::v0;
    use crate::data_science::v1;
    use crate::data_science::v1::generate_history_pin;
    use crate::data_science::v1::InteractiveDataScienceDataRoomV1;
    use crate::data_science::DataRoomCompileContext;
    use crate::Compile;

    #[test]
    fn history_pin() {
        let data_room_id = hex::decode("f4b9e73bca1b6212d14df4fb52525684a8112bd68a7e7be1fd88a18f97f81828").unwrap();
        let history_pin = generate_history_pin(&data_room_id, std::iter::empty());
        println!("history_pin: {}", hex::encode(history_pin));
    }

    #[test]
    pub fn linear_and_diverging_merge_have_same_result() {
        let initial_data_room = InteractiveDataScienceDataRoomV1 {
            initial_configuration: DataScienceDataRoomConfiguration {
                id: "11".to_string(),
                title: "title_dataroom".to_string(),
                description: "description".to_string(),
                participants: vec![
                    Participant {
                        user: "owner".to_string(),
                        permissions: vec![ParticipantPermission::Manager(ManagerPermission {})],
                    },
                    Participant { user: "user1".to_string(), permissions: vec![] },
                    Participant {
                        user: "user2".to_string(),
                        permissions: vec![ParticipantPermission::Analyst(AnalystPermission {
                            node_id: "some_computation".to_string(),
                        })],
                    },
                    Participant {
                        user: "user3".to_string(),
                        permissions: vec![ParticipantPermission::DataOwner(DataOwnerPermission {
                            node_id: "some_dataset".to_string(),
                        })],
                    },
                ],
                nodes: vec![
                    Node {
                        id: "some_dataset".to_string(),
                        name: "my table".to_string(),
                        kind: NodeKind::Leaf(LeafNode {
                            is_required: true,
                            kind: LeafNodeKind::Table(TableLeafNode {
                                sql_specification_id: "sql_spec".to_string(),
                                columns: vec![TableLeafNodeColumn {
                                    name: "column".to_string(),
                                    data_format: ColumnDataFormat {
                                        is_nullable: false,
                                        data_type: ColumnDataType::String,
                                    },
                                }],
                            }),
                        }),
                    },
                    Node {
                        id: "some_computation".to_string(),
                        name: "python script".to_string(),
                        kind: NodeKind::Computation(ComputationNode {
                            kind: ComputationNodeKind::Scripting(ScriptingComputationNode {
                                static_content_specification_id: "driver_spec".to_string(),
                                scripting_specification_id: "python_spec".to_string(),
                                scripting_language: ScriptingLanguage::Python,
                                output: "/my/output".to_string(),
                                main_script: Script {
                                    name: "main.py".to_string(),
                                    content: "print('hello world')".to_string(),
                                },
                                additional_scripts: vec![Script {
                                    name: "second.py".to_string(),
                                    content: "print('hello world')".to_string(),
                                }],
                                dependencies: vec!["some_dataset".to_string()],
                                enable_logs_on_error: true,
                                enable_logs_on_success: false,
                                minimum_container_memory_size: None,
                                extra_chunk_cache_size_to_available_memory_ratio: None,
                            }),
                        }),
                    },
                ],
                enable_development: true,
                enclave_root_certificate_pem: "enclave_root_certificate_pem".to_string(),
                enclave_specifications: vec![
                    EnclaveSpecification {
                        id: "driver_spec".to_string(),
                        attestation_proto_base64: "AhIA".to_string(),
                        worker_protocol: 0,
                    },
                    EnclaveSpecification {
                        id: "sql_spec".to_string(),
                        attestation_proto_base64: "AhIA".to_string(),
                        worker_protocol: 0,
                    },
                    EnclaveSpecification {
                        id: "python_spec".to_string(),
                        attestation_proto_base64: "AhIA".to_string(),
                        worker_protocol: 0,
                    },
                ],
                dcr_secret_id_base64: None,
            },
            commits: vec![],
            enable_automerge_feature: true,
        };

        let initial_history_pin = [0u8; 32];
        let commit1 = DataScienceCommitV1 {
            id: "fdhsjka-hjklhjkl".to_string(),
            name: "commit1".to_string(),
            enclave_data_room_id: "0102".to_string(),
            history_pin: hex::encode(initial_history_pin),
            kind: DataScienceCommitKind::AddComputation(AddComputationCommit {
                node: Node {
                    id: "s3_upload1".to_string(),
                    name: "name".to_string(),
                    kind: NodeKind::Computation(ComputationNode {
                        kind: ComputationNodeKind::S3Sink(S3SinkComputationNode {
                            specification_id: "s3_spec".to_string(),
                            endpoint: "endpoint".to_string(),
                            region: "region".to_string(),
                            credentials_dependency_id: "some_dataset".to_string(),
                            upload_dependency_id: "some_computation".to_string(),
                            s3_provider: Default::default(),
                        }),
                    }),
                },
                analysts: vec!["user3".to_string(), "user4".to_string()],
                enclave_specifications: vec![EnclaveSpecification {
                    id: "s3_spec".to_string(),
                    attestation_proto_base64: "AhIA".to_string(),
                    worker_protocol: 0,
                }],
            }),
        };

        let mut commit2 = DataScienceCommitV1 {
            id: "fdshajklh-hjklsjafdbdsa".to_string(),
            name: "commit2".to_string(),
            enclave_data_room_id: "0102".to_string(),
            history_pin: "01".to_string(),
            kind: DataScienceCommitKind::AddComputation(AddComputationCommit {
                node: Node {
                    id: "s3_upload2".to_string(),
                    name: "name".to_string(),
                    kind: NodeKind::Computation(ComputationNode {
                        kind: ComputationNodeKind::S3Sink(S3SinkComputationNode {
                            specification_id: "s3_spec".to_string(),
                            endpoint: "endpoint".to_string(),
                            region: "region".to_string(),
                            credentials_dependency_id: "some_dataset".to_string(),
                            upload_dependency_id: "some_computation".to_string(),
                            s3_provider: Default::default(),
                        }),
                    }),
                },
                analysts: vec!["user3".to_string(), "user4".to_string()],
                enclave_specifications: vec![EnclaveSpecification {
                    id: "s3_spec".to_string(),
                    attestation_proto_base64: "AhIA".to_string(),
                    worker_protocol: 0,
                }],
            }),
        };

        let initial_data_room =
            crate::data_science::DataScienceDataRoom::V1(v1::DataScienceDataRoomV1::Interactive(initial_data_room));

        // linear

        let commit1_wrapper = crate::data_science::DataScienceCommit::V1(commit1.clone());
        let commit2_wrapper = crate::data_science::DataScienceCommit::V1(commit2.clone());

        let dcr_context = DataRoomCompileContext::V0(v0::DataRoomCompileContextV0 {});

        let ((_dcr_compiled, mut _commits_compiled), _data_room, context) =
            initial_data_room.clone().compile(dcr_context.clone()).unwrap();

        let (_commit1_compiled, _commit1_hl, context) = commit1_wrapper.compile(context).unwrap();
        let (_commit2_compiled, _commit2_hl, _context) = commit2_wrapper.compile(context).unwrap();

        // Diverging
        commit2.history_pin = hex::encode(&initial_history_pin);
        let commit1_wrapper = crate::data_science::DataScienceCommit::V1(commit1.clone());
        let commit2_wrapper = crate::data_science::DataScienceCommit::V1(commit2.clone());

        let ((_dcr_compiled, mut _commits_compiled), _data_room, context) =
            initial_data_room.compile(dcr_context.clone()).unwrap();

        let (_commit1_compiled, _commit1_hl, context) = commit1_wrapper.compile(context).unwrap();
        let (_commit2_compiled, _commit2_hl, _context) = commit2_wrapper.compile(context).unwrap();
    }
}
