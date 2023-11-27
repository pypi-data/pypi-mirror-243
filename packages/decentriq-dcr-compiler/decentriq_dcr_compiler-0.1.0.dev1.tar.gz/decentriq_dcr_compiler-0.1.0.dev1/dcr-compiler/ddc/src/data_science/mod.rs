pub mod commit;
pub mod data_room;
pub mod shared;
pub mod v0;
pub mod v1;
pub mod v2;
pub mod v3;
pub mod v4;
pub mod v5;

pub use commit::DataScienceCommit;
pub use data_room::DataScienceDataRoom;
pub use shared::*;

#[cfg(test)]
mod tests {
    use crate::data_science::commit::DataScienceCommit;
    use crate::data_science::data_room::DataScienceDataRoom;
    use crate::data_science::shared::DataRoomCompileContext;
    use crate::data_science::shared::DataScienceDataRoomConfiguration;
    use crate::data_science::v0;
    use crate::data_science::v0::InteractiveDataScienceDataRoomV0;
    use crate::Compile;

    #[test]
    fn commit_test() {
        let datascience_data_room =
            DataScienceDataRoom::V0(v0::DataScienceDataRoomV0::Interactive(InteractiveDataScienceDataRoomV0 {
                initial_configuration: DataScienceDataRoomConfiguration {
                    id: "68656c6c6f".to_string(),
                    title: "title_data_room".to_string(),
                    description: "description_data_room".to_string(),
                    participants: vec![],
                    nodes: vec![],
                    enable_development: true,
                    enclave_root_certificate_pem: "".to_string(),
                    enclave_specifications: vec![],
                    dcr_secret_id_base64: None,
                },
                commits: vec![],
            }));
        println!("{}", serde_json::to_string_pretty(&datascience_data_room).unwrap());
        let input = r#"
        {
          "v0": {
            "id": "input",
            "name": "test",
            "enclaveDataRoomId": "68656c6c6f",
            "historyPin": "68656c6c6f",
            "kind": {
              "addComputation": {
                "node": {
                  "id": "s3_upload",
                  "name": "name",
                  "kind": {
                    "computation": {
                      "kind": {
                        "s3Sink": {
                          "specificationId": "s3_spec",
                          "endpoint": "endpoint",
                          "region": "region",
                          "credentialsDependencyId": "some_dataset",
                          "uploadDependencyId": "some_computation"
                        }
                      }
                    }
                  }
                },
                "analysts": [
                  "user3",
                  "user4"
                ],
                "enclaveSpecifications": [
                  {
                    "id": "s3_spec",
                    "attestationProtoBase64": "AhIA",
                    "workerProtocol": 0
                  }
                ]
              }
            }
          }
        }
        "#;

        let input_data_room = r#"
            {
              "v0": {
                "interactive": {
                  "initialConfiguration": {
                    "id": "68656c6c6f",
                    "title": "title_dataroom",
                    "description": "description",
                    "participants": [
                      {
                        "user": "owner",
                        "permissions": [
                          {
                            "manager": {}
                          }
                        ]
                      },
                      {
                        "user": "user1",
                        "permissions": []
                      },
                      {
                        "user": "user2",
                        "permissions": [
                          {
                            "analyst": {
                              "nodeId": "some_computation"
                            }
                          }
                        ]
                      },
                      {
                        "user": "user3",
                        "permissions": [
                          {
                            "dataOwner": {
                              "nodeId": "some_dataset"
                            }
                          }
                        ]
                      }
                    ],
                    "nodes": [
                      {
                        "id": "some_dataset",
                        "name": "my table",
                        "kind": {
                          "leaf": {
                            "isRequired": true,
                            "kind": {
                              "table": {
                                "noopSpecificationId": "driver_spec",
                                "sqlSpecificationId": "sql_spec",
                                "columns": [
                                  {
                                    "name": "column",
                                    "dataFormat": {
                                      "isNullable": false,
                                      "dataType": "string"
                                    }
                                  }
                                ]
                              }
                            }
                          }
                        }
                      },
                      {
                        "id": "some_computation",
                        "name": "python script",
                        "kind": {
                          "computation": {
                            "kind": {
                              "scripting": {
                                "staticContentSpecificationId": "driver_spec",
                                "scriptingSpecificationId": "python_spec",
                                "scriptingLanguage": "python",
                                "output": "/my/output",
                                "mainScript": {
                                  "name": "main.py",
                                  "content": "print('hello world')"
                                },
                                "additionalScripts": [
                                  {
                                    "name": "second.py",
                                    "content": "print('hello world')"
                                  }
                                ],
                                "dependencies": [
                                  "some_dataset"
                                ],
                                "enableLogsOnError": true,
                                "enableLogsOnSuccess": false
                              }
                            }
                          }
                        }
                      }
                    ],
                    "enableInteractivity": true,
                    "enableDevelopment": true,
                    "enclaveRootCertificatePem": "enclave_root_certificate_pem",
                    "enclaveSpecifications": [
                      {
                        "id": "driver_spec",
                        "attestationProtoBase64": "AhIA",
                        "workerProtocol": 0
                      },
                      {
                        "id": "sql_spec",
                        "attestationProtoBase64": "AhIA",
                        "workerProtocol": 0
                      },
                      {
                        "id": "python_spec",
                        "attestationProtoBase64": "AhIA",
                        "workerProtocol": 0
                      }
                    ]
                  },
                  "commits": []
                }
              }
            }
        "#;
        let commit: DataScienceCommit = serde_json::from_str(input).unwrap();
        let data_room: DataScienceDataRoom = serde_json::from_str(input_data_room).unwrap();
        let dcr_context = DataRoomCompileContext::V0(v0::DataRoomCompileContextV0 {});
        let ((dcr_compiled, commits_compiled), data_room, context) = data_room.compile(dcr_context.clone()).unwrap();
        println!("Compiled: {:?}", dcr_compiled);
        let output_dcr_high_level =
            DataScienceDataRoom::verify((dcr_compiled, commits_compiled), data_room, dcr_context).unwrap();
        println!("Verified: {:?}", output_dcr_high_level);
        let (commit_compiled, commit, _) = commit.compile(context.clone()).unwrap();
        println!("\nCompiled: {:?}", commit_compiled);
        let output_commit_high_level = DataScienceCommit::verify(commit_compiled, commit, context).unwrap();
        println!("Verified: {:?}", output_commit_high_level);
    }
}
