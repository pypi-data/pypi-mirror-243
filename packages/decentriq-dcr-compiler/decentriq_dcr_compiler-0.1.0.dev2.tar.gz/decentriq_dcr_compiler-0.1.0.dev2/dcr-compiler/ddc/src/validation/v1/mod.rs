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
use delta_data_room_api::ConfigurationElement;
use delta_gcg_driver_api::driver_task_config;
use delta_gcg_driver_api::DriverTaskConfig;
use delta_gcg_driver_api::StaticContentConfig;

use crate::error::CompileError;

static VALIDATION_WORKER_SCRIPT_ID: &str = "__validation_script";

static VALIDATION_CHECK_SCRIPT_ID: &str = "__validation_check";

static VALIDATION_REPORT_FILENAME: &str = "validation-report.json";

pub fn get_validation_config_id(base_node_id: &str) -> String {
    format!("{}_validation_config", base_node_id)
}

pub fn get_validation_id(base_node_id: &str) -> String {
    format!("{}_validation", base_node_id)
}

pub fn get_validation_check_id(base_node_id: &str) -> String {
    format!("{}_validation_check", base_node_id)
}

pub fn get_validation_report_id(base_node_id: &str) -> String {
    format!("{}_validation_report", base_node_id)
}

pub fn add_nodes_for_validation(
    configuration_elements: &mut Vec<ConfigurationElement>,
    base_node_id: &str,
    data_node_id: &str,
    validation_config: &validation_config::ValidationConfig,
    static_content_specification_id: &str,
    driver_protocol: u32,
    python_specification_id: &str,
    python_protocol: u32,
) -> Result<(), CompileError> {
    let validation_config_id = get_validation_config_id(&base_node_id);
    let validation_id = get_validation_id(&base_node_id);
    let validation_check_id = get_validation_check_id(&base_node_id);
    let validation_report_id = get_validation_report_id(&base_node_id);

    let was_worker_script_already_added =
        configuration_elements.iter().any(|element| element.id == VALIDATION_WORKER_SCRIPT_ID);

    if !was_worker_script_already_added {
        configuration_elements.push(ConfigurationElement {
            id: VALIDATION_WORKER_SCRIPT_ID.to_string(),
            element: Some(Element::ComputeNode(ComputeNode {
                node_name: VALIDATION_WORKER_SCRIPT_ID.to_string(),
                node: Some(compute_node::Node::Branch(ComputeNodeBranch {
                    config: DriverTaskConfig {
                        driver_task_config: Some(driver_task_config::DriverTaskConfig::StaticContent(
                            StaticContentConfig { content: include_bytes!("worker.py").to_vec() },
                        )),
                    }
                    .encode_length_delimited_to_vec(),
                    dependencies: vec![],
                    output_format: ComputeNodeFormat::Raw as i32,
                    protocol: Some(ComputeNodeProtocol { version: driver_protocol }),
                    attestation_specification_id: static_content_specification_id.to_string(),
                })),
                rate_limiting: None,
            })),
        });
    }

    let was_check_script_already_added =
        configuration_elements.iter().any(|element| element.id == VALIDATION_CHECK_SCRIPT_ID);

    if !was_check_script_already_added {
        configuration_elements.push(ConfigurationElement {
            id: VALIDATION_CHECK_SCRIPT_ID.to_string(),
            element: Some(Element::ComputeNode(ComputeNode {
                node_name: VALIDATION_CHECK_SCRIPT_ID.to_string(),
                node: Some(compute_node::Node::Branch(ComputeNodeBranch {
                    config: DriverTaskConfig {
                        driver_task_config: Some(driver_task_config::DriverTaskConfig::StaticContent(
                            StaticContentConfig { content: include_bytes!("check.py").to_vec() },
                        )),
                    }
                    .encode_length_delimited_to_vec(),
                    dependencies: vec![],
                    output_format: ComputeNodeFormat::Raw as i32,
                    protocol: Some(ComputeNodeProtocol { version: driver_protocol }),
                    attestation_specification_id: static_content_specification_id.to_string(),
                })),
                rate_limiting: None,
            })),
        });
    }

    // Include validation config as JSON file
    configuration_elements.push(ConfigurationElement {
        id: validation_config_id.clone(),
        element: Some(Element::ComputeNode(ComputeNode {
            node_name: validation_config_id.clone(),
            node: Some(compute_node::Node::Branch(ComputeNodeBranch {
                config: DriverTaskConfig {
                    driver_task_config: Some(driver_task_config::DriverTaskConfig::StaticContent(
                        StaticContentConfig {
                            content: serde_json::to_vec(&validation_config.clone().with_hash_format_if_required())?,
                        },
                    )),
                }
                .encode_length_delimited_to_vec(),
                dependencies: vec![],
                output_format: ComputeNodeFormat::Raw as i32,
                protocol: Some(ComputeNodeProtocol { version: driver_protocol }),
                attestation_specification_id: static_content_specification_id.to_string(),
            })),
            rate_limiting: None,
        })),
    });

    let validation_worker_config = ContainerWorkerConfiguration {
        configuration: Some(container_worker_configuration::Configuration::Static(StaticImage {
            command: vec![
                "python".to_string(),
                "/input/run_validation.py".to_string(),
                "--input".to_string(),
                "/input/input_data".to_string(),
                "--config".to_string(),
                "/input/validation_config".to_string(),
                "--wasm".to_string(),
                "/bin/validate.wasm".to_string(), // Burnt into the worker
                "--output".to_string(),
                "/output/dataset.csv".to_string(),
                "--report".to_string(),
                format!("/output/{}", VALIDATION_REPORT_FILENAME),
                "--types".to_string(),
                "/output/types".to_string(),
            ],
            mount_points: vec![
                MountPoint {
                    dependency: VALIDATION_WORKER_SCRIPT_ID.to_string(),
                    path: "run_validation.py".to_string(),
                },
                MountPoint { dependency: validation_config_id.clone(), path: "validation_config".to_string() },
                MountPoint { dependency: data_node_id.to_string(), path: "input_data".to_string() },
            ],
            output_path: "/output".to_string(),
            include_container_logs_on_error: true,
            include_container_logs_on_success: false,
            minimum_container_memory_size: None,
            extra_chunk_cache_size_to_available_memory_ratio: None,
        })),
    };

    configuration_elements.push(ConfigurationElement {
        id: validation_id.clone(),
        element: Some(Element::ComputeNode(ComputeNode {
            node_name: validation_id.clone(),
            node: Some(compute_node::Node::Branch(ComputeNodeBranch {
                config: validation_worker_config.encode_length_delimited_to_vec(),
                dependencies: vec![
                    data_node_id.to_string(),
                    VALIDATION_WORKER_SCRIPT_ID.to_string(),
                    validation_config_id,
                ],
                output_format: ComputeNodeFormat::Zip as i32,
                protocol: Some(ComputeNodeProtocol { version: python_protocol }),
                attestation_specification_id: python_specification_id.to_string(),
            })),
            rate_limiting: None,
        })),
    });

    let report_selector_config = ContainerWorkerConfiguration {
        configuration: Some(container_worker_configuration::Configuration::Static(StaticImage {
            command: vec![
                "cp".to_string(),
                format!("/input/validation/{}", VALIDATION_REPORT_FILENAME),
                format!("/output/{}", VALIDATION_REPORT_FILENAME),
            ],
            mount_points: vec![MountPoint { dependency: validation_id.clone(), path: "validation".to_string() }],
            output_path: "/output".to_string(),
            include_container_logs_on_error: true,
            include_container_logs_on_success: false,
            minimum_container_memory_size: None,
            extra_chunk_cache_size_to_available_memory_ratio: None,
        })),
    };
    configuration_elements.push(ConfigurationElement {
        id: validation_report_id.clone(),
        element: Some(Element::ComputeNode(ComputeNode {
            node_name: validation_report_id.clone(),
            node: Some(compute_node::Node::Branch(ComputeNodeBranch {
                config: report_selector_config.encode_length_delimited_to_vec(),
                dependencies: vec![validation_id.clone()],
                output_format: ComputeNodeFormat::Zip as i32,
                protocol: Some(ComputeNodeProtocol { version: python_protocol }),
                attestation_specification_id: python_specification_id.to_string(),
            })),
            rate_limiting: None,
        })),
    });

    let validation_check_config = ContainerWorkerConfiguration {
        configuration: Some(container_worker_configuration::Configuration::Static(StaticImage {
            command: vec!["python".to_string(), "/input/check_validation.py".to_string()],
            mount_points: vec![
                MountPoint {
                    dependency: VALIDATION_CHECK_SCRIPT_ID.to_string(),
                    path: "check_validation.py".to_string(),
                },
                MountPoint { dependency: validation_id.clone(), path: "validation".to_string() },
            ],
            output_path: "/output".to_string(),
            include_container_logs_on_error: true,
            include_container_logs_on_success: false,
            minimum_container_memory_size: None,
            extra_chunk_cache_size_to_available_memory_ratio: None,
        })),
    };
    configuration_elements.push(ConfigurationElement {
        id: validation_check_id.clone(),
        element: Some(Element::ComputeNode(ComputeNode {
            node_name: validation_check_id.clone(),
            node: Some(compute_node::Node::Branch(ComputeNodeBranch {
                config: validation_check_config.encode_length_delimited_to_vec(),
                dependencies: vec![validation_id.clone(), VALIDATION_CHECK_SCRIPT_ID.to_string()],
                output_format: ComputeNodeFormat::Zip as i32,
                protocol: Some(ComputeNodeProtocol { version: python_protocol }),
                attestation_specification_id: python_specification_id.to_string(),
            })),
            rate_limiting: None,
        })),
    });

    Ok(())
}
