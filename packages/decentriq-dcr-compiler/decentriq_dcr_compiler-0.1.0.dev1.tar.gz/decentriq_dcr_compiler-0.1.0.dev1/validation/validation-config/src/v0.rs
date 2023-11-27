use format_types::v0::*;
use schemars::JsonSchema;
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, JsonSchema, Clone, Debug)]
#[serde(rename_all = "camelCase")]
pub struct NumericRangeRule {
    pub greater_than_equals: Option<f64>,
    pub greater_than: Option<f64>,
    pub less_than: Option<f64>,
    pub less_than_equals: Option<f64>,
}

#[derive(Serialize, Deserialize, JsonSchema, Clone, Debug)]
#[serde(rename_all = "camelCase")]
pub struct ColumnValidationV0 {
    #[serde(skip_serializing_if = "Option::is_none")]
    pub name: Option<String>,
    pub format_type: FormatType,
    pub allow_null: bool,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub hash_with: Option<HashingAlgorithm>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub in_range: Option<NumericRangeRule>,
}

#[derive(Serialize, Deserialize, JsonSchema, Clone, Debug)]
#[serde(rename_all = "camelCase")]
pub struct ColumnTuple {
    pub columns: Vec<usize>
}

#[derive(Serialize, Deserialize, JsonSchema, Clone, Debug)]
#[serde(rename_all = "camelCase")]
pub struct UniquenessValidationRule {
    pub unique_keys: Vec<ColumnTuple>,
}

#[derive(Serialize, Deserialize, JsonSchema, Clone, Debug)]
#[serde(rename_all = "camelCase")]
pub struct NumRowsValidationRule {
    #[serde(skip_serializing_if = "Option::is_none")]
    pub at_least: Option<u64>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub at_most: Option<u64>,
}

#[derive(Serialize, Deserialize, JsonSchema, Clone, Debug)]
#[serde(rename_all = "camelCase")]
pub struct TableValidationV0 {
    #[serde(skip_serializing_if = "Option::is_none")]
    pub allow_empty: Option<bool>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub uniqueness: Option<UniquenessValidationRule>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub num_rows: Option<NumRowsValidationRule>,
}

#[derive(Serialize, Deserialize, JsonSchema, Clone, Debug)]
#[serde(rename_all = "camelCase")]
pub struct ValidationConfigV0 {
    pub columns: Vec<ColumnValidationV0>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub table: Option<TableValidationV0>,
}

impl ValidationConfigV0 {
    pub fn with_hash_format_if_required(self) -> Self {
        Self {
            columns: self.columns.into_iter().map(|column| {
                let format_type = match column.hash_with.as_ref() {
                    None => {
                        column.format_type
                    }
                    Some(hash) => {
                        match hash {
                            HashingAlgorithm::Sha256Hex => {
                                FormatType::HashSha256Hex
                            }
                        }
                    }
                };
                ColumnValidationV0 {
                    format_type,
                    hash_with: None,
                    ..column
                }
            }).collect(),
            table: self.table,
        }
    }
}
