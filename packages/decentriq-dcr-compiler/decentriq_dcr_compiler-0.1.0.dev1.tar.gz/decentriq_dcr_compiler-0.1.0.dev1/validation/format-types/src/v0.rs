use std::fmt::{Display, Formatter};
use schemars::JsonSchema;
use serde::{Deserialize, Serialize};

// TODO: Split into NumericFormatType and TextFormatType with only
// specific allowed rules? yagni?
#[derive(Serialize, Deserialize, JsonSchema, Clone, Debug)]
#[serde(rename_all = "SCREAMING_SNAKE_CASE")]
pub enum FormatType {
    String,
    Integer,
    Float,
    Email,
    DateIso8601,
    PhoneNumberE164,
    HashSha256Hex,
}

impl Display for FormatType {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        let stringified = serde_json::to_string(self).map_err(|_err| std::fmt::Error {})?;
        write!(f, "{}", stringified)
    }
}

#[derive(Serialize, Deserialize, JsonSchema, Clone, Debug)]
#[serde(rename_all = "SCREAMING_SNAKE_CASE")]
pub enum HashingAlgorithm {
    Sha256Hex,
}

impl Display for HashingAlgorithm {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        let stringified = serde_json::to_string(self).map_err(|_err| std::fmt::Error {})?;
        write!(f, "{}", stringified)
    }
}

