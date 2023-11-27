use schemars::JsonSchema;
use serde::{Deserialize, Serialize};

pub mod v0;

#[derive(Serialize, Deserialize, JsonSchema, Clone, Debug)]
#[serde(tag = "version", rename_all = "camelCase", content = "config")]
pub enum ValidationConfig {
    V0(v0::ValidationConfigV0),
}

impl ValidationConfig {
    pub fn with_hash_format_if_required(self) -> Self {
        match self {
            ValidationConfig::V0(config) => {
                ValidationConfig::V0(config.with_hash_format_if_required())
            }
        }
    }
}
