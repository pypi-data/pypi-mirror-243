use std::collections::HashMap;
use std::convert::TryFrom;

use delta_container_worker_api::container_worker_configuration;
use delta_container_worker_api::prost::Message;
use delta_container_worker_api::ContainerWorkerConfiguration;
use delta_container_worker_api::MountPoint;
use delta_container_worker_api::StaticImage;
use delta_data_room_api::compute_node;
use delta_data_room_api::configuration_element::Element;
use delta_data_room_api::ComputeNode;
use delta_data_room_api::ComputeNodeBranch;
use delta_data_room_api::ComputeNodeFormat;
use delta_data_room_api::ComputeNodeProtocol;
use delta_data_room_api::ConfigurationCommit;
use delta_data_room_api::ConfigurationElement;
use delta_gcg_driver_api::driver_task_config;
use delta_gcg_driver_api::DriverTaskConfig;
use delta_gcg_driver_api::StaticContentConfig;

use crate::data_science::v2;
use crate::data_science::v2::ComputationNodeKindV2;
use crate::data_science::v2::NodeKindV2;
use crate::data_science::v2::NodeV2;
use crate::data_science::v3::DataScienceCommitV3;
use crate::data_science::DataScienceCommitMergeMetadata;
use crate::data_science::EnclaveSpecificationContext;
use crate::data_science::MatchingComputeNodeConfig;
use crate::data_science::Participant;
use crate::data_science::ScriptingLanguage;
use crate::error::CompileError;

pub fn add_node_configuration_elements(
    node: NodeV2,
    configuration_elements: &mut Vec<ConfigurationElement>,
    enclave_specifications_map: &HashMap<String, EnclaveSpecificationContext>,
    nodes_map: &HashMap<String, NodeV2>,
) -> Result<(), CompileError> {
    let node_clone = node.clone();
    match node.kind {
        NodeKindV2::Leaf(_) => v2::add_node_configuration_elements(
            node_clone, configuration_elements, enclave_specifications_map, nodes_map,
        ),
        NodeKindV2::Computation(computation_node) => match computation_node.kind {
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

                let (main_script_id, additional_mount_point) = match scripting_computation_node.scripting_language {
                    ScriptingLanguage::Python => {
                        // TODO: Change this to add the wrapper script with the ID of the main script, which
                        // will in turn exec the wrappee script.
                        let main_script_id = format!("{}_main_script", node.id);
                        let wrapped_main_script_id = format!("{}_main_script_wrapped", node.id);

                        let wrapper_script_configuration = DriverTaskConfig {
                            driver_task_config: Some(driver_task_config::DriverTaskConfig::StaticContent(
                                StaticContentConfig { content: include_bytes!("./python-wrapper.py").to_vec() },
                            )),
                        };

                        configuration_elements.push(ConfigurationElement {
                            id: main_script_id.clone(),
                            element: Some(Element::ComputeNode(ComputeNode {
                                node_name: scripting_computation_node.main_script.name.clone(),
                                node: Some(compute_node::Node::Branch(ComputeNodeBranch {
                                    config: wrapper_script_configuration.encode_length_delimited_to_vec(),
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

                        let main_script_configuration = DriverTaskConfig {
                            driver_task_config: Some(driver_task_config::DriverTaskConfig::StaticContent(
                                StaticContentConfig {
                                    content: scripting_computation_node.main_script.content.into_bytes(),
                                },
                            )),
                        };

                        configuration_elements.push(ConfigurationElement {
                            id: wrapped_main_script_id.clone(),
                            element: Some(Element::ComputeNode(ComputeNode {
                                node_name: format!("{}_wrapped", &scripting_computation_node.main_script.name),
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

                        let mount_point =
                            MountPoint { path: "__main_script.py".to_string(), dependency: wrapped_main_script_id };

                        (main_script_id, Some(mount_point))
                    }
                    _ => {
                        let main_script_id = format!("{}_main_script", node.id);
                        let main_script_configuration = DriverTaskConfig {
                            driver_task_config: Some(driver_task_config::DriverTaskConfig::StaticContent(
                                StaticContentConfig {
                                    content: scripting_computation_node.main_script.content.into_bytes(),
                                },
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

                        (main_script_id, None)
                    }
                };

                let node_dependencies = scripting_computation_node
                    .dependencies
                    .into_iter()
                    .map(|id| {
                        let enclave_id = v2::get_enclave_dependency_node_id(&id, nodes_map)
                            .ok_or_else(|| CompileError("Node not found".to_string()))?;
                        Ok((id, enclave_id))
                    })
                    .collect::<Result<Vec<_>, CompileError>>()?;
                let mut dependencies = std::iter::once(main_script_id.clone())
                    .chain(additional_scripts.iter().map(|(id, _)| id.clone()))
                    .chain(node_dependencies.iter().map(|(_, enclave_node_id)| enclave_node_id.clone()))
                    .collect::<Vec<_>>();
                if let Some(additional_mount_point) = &additional_mount_point {
                    dependencies.push(additional_mount_point.dependency.clone());
                };

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

                let mut mount_points: Vec<_> =
                    std::iter::once(MountPoint { dependency: main_script_id, path: main_script_file_name.clone() })
                        .chain(
                            additional_scripts
                                .into_iter()
                                .map(|(id, file_name)| MountPoint { dependency: id, path: file_name }),
                        )
                        .chain(node_dependecies_mount_points.into_iter())
                        .collect();
                if let Some(additional_mount_point) = additional_mount_point {
                    mount_points.push(additional_mount_point);
                }

                let container_worker_configuration = ContainerWorkerConfiguration {
                    configuration: Some(container_worker_configuration::Configuration::Static(StaticImage {
                        command: vec![scripting_command, format!("/input/{}", &main_script_file_name)],
                        mount_points,
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
                Ok(())
            }
            ComputationNodeKindV2::Match(match_node) => {
                let mut dependency_ids = vec![];
                let mut mount_points = vec![];

                // Leaf dependencies.
                let mut dependencies = vec![];
                for dependency_id in &match_node.dependencies {
                    let enclave_id = v2::get_enclave_dependency_node_id(dependency_id, nodes_map)
                        .ok_or_else(|| CompileError(format!("No node found for '{}'", dependency_id)))?;
                    let path = v2::get_dependency_node_name(dependency_id, nodes_map)?;
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
                                    StaticContentConfig { content: include_bytes!("./match.py").to_vec() },
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

                Ok(())
            }
            ComputationNodeKindV2::Sqlite(sqlite_computation_node) => {
                let static_content_attestation_id = sqlite_computation_node.static_content_specification_id;
                let static_content_node_metadata =
                    enclave_specifications_map.get(&static_content_attestation_id).ok_or_else(|| {
                        CompileError(format!("No enclave specification found for '{}'", &static_content_attestation_id))
                    })?;

                let dependencies =
                    v2::construct_table_dependency_mappings(&sqlite_computation_node.dependencies, nodes_map)?;

                let sql_computation_configuration = v2::construct_sql_worker_configuration(
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
                        minimum_container_memory_size: Some(256 * 1024 * 1024),
                        extra_chunk_cache_size_to_available_memory_ratio: Some(1.0),
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
                Ok(())
            }
            _ => v2::add_node_configuration_elements(
                node_clone, configuration_elements, enclave_specifications_map, nodes_map,
            ),
        },
    }?;
    Ok(())
}

#[derive(Debug, Clone)]
pub struct CommitCompileContextV3 {
    pub nodes_map: HashMap<String, NodeV2>,
    pub enclave_specifications_map: HashMap<String, EnclaveSpecificationContext>,
    pub participants: Vec<Participant>,
    pub enable_development: bool,
    pub enable_interactivity: bool,
    pub initial_participants: HashMap<String, Participant>,
    pub previous_commits: Vec<(DataScienceCommitV3, ConfigurationCommit, DataScienceCommitMergeMetadata)>,
}

impl CommitCompileContextV3 {
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
