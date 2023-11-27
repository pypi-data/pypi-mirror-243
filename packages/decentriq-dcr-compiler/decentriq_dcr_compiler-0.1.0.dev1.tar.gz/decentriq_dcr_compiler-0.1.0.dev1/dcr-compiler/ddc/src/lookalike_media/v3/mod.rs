use schemars::JsonSchema;
use serde::Deserialize;
use serde::Deserializer;
use serde::Serialize;

use crate::feature::Requirements;
use crate::lookalike_media::v3::compute::LookalikeMediaDcrCompute;

pub mod compute;

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(untagged)]
pub enum LookalikeMediaDcrComputeOrUnknown {
    Known(LookalikeMediaDcrCompute),
    Unknown,
}

impl LookalikeMediaDcrComputeOrUnknown {
    pub fn parse_if_known<'de, D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: Deserializer<'de>,
    {
        match LookalikeMediaDcrComputeOrUnknown::deserialize(deserializer) {
            Ok(known) => Ok(known),
            Err(_) => Ok(Self::Unknown),
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct LookalikeMediaDcrWrapper {
    pub features: Vec<String>,
    pub consumes: Requirements,
    #[serde(deserialize_with = "LookalikeMediaDcrComputeOrUnknown::parse_if_known")]
    pub compute: LookalikeMediaDcrComputeOrUnknown,
}
