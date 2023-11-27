use crate::data_science::v2::LeafNodeKindV2;
use crate::data_science::v2::LeafNodeV2;
use crate::data_science::v2::NodeKindV2;
use crate::data_science::v2::NodeV2;
use crate::data_science::v2::TableLeafNodeColumnV2;
use crate::data_science::v2::TableLeafNodeV2;
use crate::data_science::v2::ValidationNodeV2;
use crate::data_science::ColumnDataType;
use crate::data_science::ComputationNode;
use crate::data_science::ComputationNodeKind;
use crate::data_science::LeafNode;
use crate::data_science::LeafNodeKind;
use crate::data_science::Node;
use crate::data_science::NodeKind;
use std::convert::TryInto;
use validation_config::v0::TableValidationV0;

use super::ComputationNodeKindV2;
use super::ComputationNodeV2;

impl From<Node> for NodeV2 {
    /// Upgrade
    fn from(node: Node) -> Self {
        match node.kind {
            NodeKind::Leaf(leaf) => match leaf.kind {
                LeafNodeKind::Raw(raw) => NodeV2 {
                    id: node.id,
                    name: node.name,
                    kind: NodeKindV2::Leaf(LeafNodeV2 {
                        is_required: leaf.is_required,
                        kind: LeafNodeKindV2::Raw(raw),
                    }),
                },
                LeafNodeKind::Table(table) => NodeV2 {
                    id: node.id,
                    name: node.name,
                    kind: NodeKindV2::Leaf(LeafNodeV2 {
                        is_required: leaf.is_required,
                        kind: LeafNodeKindV2::Table(TableLeafNodeV2 {
                            columns: table
                                .columns
                                .into_iter()
                                .map(|column| TableLeafNodeColumnV2 {
                                    name: column.name.clone(),
                                    data_format: column.data_format.clone(),
                                    validation: validation_config::v0::ColumnValidationV0 {
                                        name: Some(column.name),
                                        allow_null: column.data_format.is_nullable,
                                        format_type: match column.data_format.data_type {
                                            ColumnDataType::Integer => {
                                                format_types::v0::FormatType::Integer
                                            }
                                            ColumnDataType::Float => {
                                                format_types::v0::FormatType::Float
                                            }
                                            ColumnDataType::String => {
                                                format_types::v0::FormatType::String
                                            }
                                        },
                                        in_range: None,
                                        hash_with: None,
                                    },
                                })
                                .collect(),
                            validation_node: ValidationNodeV2 {
                                // Since we only use the upgrade path to convert a node of an
                                // older version to a PublishedNode, we don't need to have the attestation
                                // specs in place. Whether and how to perform server-side validation is up
                                // top the client-side wrapper to decide.
                                static_content_specification_id: "NOT_SPECIFIED".to_string(),
                                python_specification_id: "NOT_SPECIFIED".to_string(),
                                validation: TableValidationV0 {
                                    allow_empty: None,
                                    num_rows: None,
                                    uniqueness: None,
                                },
                            },
                        }),
                    }),
                },
            },
            NodeKind::Computation(compute) => {
                let kind = match compute.kind {
                    ComputationNodeKind::Sql(sql_compute) => {
                        ComputationNodeKindV2::Sql(sql_compute)
                    }
                    ComputationNodeKind::Scripting(scripting_compute) => {
                        ComputationNodeKindV2::Scripting(scripting_compute)
                    }
                    ComputationNodeKind::SyntheticData(synthetic_data_compute) => {
                        ComputationNodeKindV2::SyntheticData(synthetic_data_compute)
                    }
                    ComputationNodeKind::S3Sink(s3_sink_compute) => {
                        ComputationNodeKindV2::S3Sink(s3_sink_compute)
                    }
                    ComputationNodeKind::Match(match_compute) => {
                        ComputationNodeKindV2::Match(match_compute)
                    }
                };
                NodeV2 {
                    id: node.id,
                    name: node.name,
                    kind: NodeKindV2::Computation(ComputationNodeV2 { kind }),
                }
            }
        }
    }
}

impl TryInto<Node> for NodeV2 {
    type Error = String;
    /// Downgrade
    fn try_into(self) -> Result<Node, String> {
        match self.kind {
            NodeKindV2::Leaf(leaf) => match leaf.kind {
                // Cannot convert table nodes as they are missing the sql enclave spec id
                // required for the previous SQL worker-based validation.
                // Also, validations based on format types etc. is not possible with V1.
                LeafNodeKindV2::Table(_table) => {
                    Err("Table nodes cannot be converted from V2 to V1".to_string())
                }
                LeafNodeKindV2::Raw(raw) => Ok(Node {
                    id: self.id,
                    name: self.name,
                    kind: NodeKind::Leaf(LeafNode {
                        is_required: leaf.is_required,
                        kind: LeafNodeKind::Raw(raw),
                    }),
                }),
            },
            NodeKindV2::Computation(compute) => {
                let kind = compute.kind.try_into()?;
                Ok(Node {
                    id: self.id,
                    name: self.name,
                    kind: NodeKind::Computation(ComputationNode { kind }),
                })
            }
        }
    }
}

impl TryInto<ComputationNodeKind> for ComputationNodeKindV2 {
    type Error = String;
    /// Upgrade
    fn try_into(self) -> Result<ComputationNodeKind, Self::Error> {
        match self {
            ComputationNodeKindV2::Sql(inner) => Ok(ComputationNodeKind::Sql(inner)),
            ComputationNodeKindV2::Sqlite(_) => {
                Err("Sqlite nodes cannot be converted from V2 to V1".to_string())
            }
            ComputationNodeKindV2::Scripting(inner) => Ok(ComputationNodeKind::Scripting(inner)),
            ComputationNodeKindV2::SyntheticData(inner) => {
                Ok(ComputationNodeKind::SyntheticData(inner))
            }
            ComputationNodeKindV2::S3Sink(inner) => Ok(ComputationNodeKind::S3Sink(inner)),
            ComputationNodeKindV2::Match(inner) => Ok(ComputationNodeKind::Match(inner)),
            ComputationNodeKindV2::Post(_) => {
                Err("Post nodes cannot be converted from V2 to V1".to_string())
            }
        }
    }
}
