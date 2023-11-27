use format_types::v0::FormatType;
use format_types::v0::HashingAlgorithm;
use schemars::JsonSchema;
use serde::Deserialize;
use serde::Deserializer;
use serde::Serialize;
use serde_json::Value;

use crate::data_lab::provides::MATCHING_DATA_USER_ID_FORMAT;
use crate::data_lab::provides::MATCHING_DATA_USER_ID_HASHING_ALGORITHM;
use crate::data_lab::provides::MATCHING_DATA_USER_ID_HASHING_ALGORITHM_UNHASHED;
use crate::error::CompileResult;

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema, PartialEq)]
#[serde(rename_all = "camelCase")]
pub struct RequirementFlag {
    pub(crate) name: String,
    #[serde(deserialize_with = "KnownOrUnknownRequirementFlagValue::parse_if_known")]
    pub(crate) details: KnownOrUnknownRequirementFlagValue,
}

impl RequirementFlag {
    pub fn from_matching_id_format(format_type: &FormatType) -> CompileResult<Self> {
        match serde_json::to_value(format_type)? {
            Value::String(value) => Ok(RequirementFlag {
                name: MATCHING_DATA_USER_ID_FORMAT.to_string(),
                details: KnownOrUnknownRequirementFlagValue::Known(RequirementFlagValue::Property(value)),
            }),
            _ => Err(format!("Cannot convert format type '{}' to a string value", format_type).into()),
        }
    }

    pub fn from_matching_id_hashing_algorithm(algorithm: Option<&HashingAlgorithm>) -> CompileResult<Self> {
        let value = if let Some(algorithm) = algorithm {
            match serde_json::to_value(algorithm)? {
                Value::String(value) => value,
                _ => {
                    return Err(format!("Cannot convert algorithm '{}' to a string value", algorithm).into());
                }
            }
        } else {
            MATCHING_DATA_USER_ID_HASHING_ALGORITHM_UNHASHED.to_string()
        };
        Ok(RequirementFlag::from_property(MATCHING_DATA_USER_ID_HASHING_ALGORITHM, &value))
    }

    pub fn from_dataset(name: &str) -> Self {
        Self {
            name: name.to_string(),
            details: KnownOrUnknownRequirementFlagValue::Known(RequirementFlagValue::Dataset),
        }
    }

    pub fn from_property(name: &str, value: &str) -> Self {
        Self {
            name: name.to_string(),
            details: KnownOrUnknownRequirementFlagValue::Known(RequirementFlagValue::Property(value.to_string())),
        }
    }

    pub fn from_supported(name: &str) -> Self {
        Self {
            name: name.to_string(),
            details: KnownOrUnknownRequirementFlagValue::Known(RequirementFlagValue::Supported),
        }
    }

    pub fn does_match(&self, query_flag: &RequirementFlag) -> bool {
        use KnownOrUnknownRequirementFlagValue::*;
        if self.name == query_flag.name {
            match (&self.details, &query_flag.details) {
                (Known(a), Known(b)) => match (&a, &b) {
                    (RequirementFlagValue::Property(a), RequirementFlagValue::Property(b)) => a == b,
                    (RequirementFlagValue::Supported, RequirementFlagValue::Supported) => true,
                    (RequirementFlagValue::Dataset, RequirementFlagValue::Dataset) => true,
                    _ => false,
                },
                _ => false,
            }
        } else {
            false
        }
    }

    pub fn get_dataset_name(&self) -> Option<&String> {
        match &self.details {
            KnownOrUnknownRequirementFlagValue::Known(known) => match &known {
                RequirementFlagValue::Dataset => Some(&self.name),
                _ => None,
            },
            _ => None,
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema, PartialEq)]
#[serde(untagged)]
#[serde(rename_all = "camelCase")]
pub enum KnownOrUnknownRequirementFlagValue {
    Known(RequirementFlagValue),
    Unknown,
}

impl KnownOrUnknownRequirementFlagValue {
    pub fn as_option(&self) -> Option<&RequirementFlagValue> {
        match self {
            KnownOrUnknownRequirementFlagValue::Known(known) => Some(&known),
            KnownOrUnknownRequirementFlagValue::Unknown => None,
        }
    }

    pub fn parse_if_known<'de, D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: Deserializer<'de>,
    {
        match Self::deserialize(deserializer) {
            Ok(known) => Ok(known),
            Err(_) => Ok(Self::Unknown),
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema, PartialEq)]
#[serde(rename_all = "SCREAMING_SNAKE_CASE", tag = "type", content = "value")]
pub enum RequirementFlagValue {
    Supported,
    Dataset,
    Property(String),
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct Requirements {
    pub optional: Vec<RequirementFlag>,
    pub required: Vec<RequirementFlag>,
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct RequirementList {
    pub optional: Vec<String>,
    pub required: Vec<String>,
}

impl Requirements {
    pub fn get_datasets(&self) -> RequirementList {
        RequirementList {
            optional: self.optional.iter().filter_map(|flag| flag.get_dataset_name().cloned()).collect(),
            required: self.required.iter().filter_map(|flag| flag.get_dataset_name().cloned()).collect(),
        }
    }

    pub fn contains_optional(&self, query_flag: &RequirementFlag) -> bool {
        self.optional.iter().find(|flag| flag.does_match(query_flag)).is_some()
    }

    pub fn contains_required(&self, query_flag: &RequirementFlag) -> bool {
        self.required.iter().find(|flag| flag.does_match(query_flag)).is_some()
    }

    pub fn contains_all(&self, query_flag: &RequirementFlag) -> bool {
        self.contains_optional(query_flag) || self.contains_required(query_flag)
    }

    pub fn is_compatible_with(&self, other: &Self) -> bool {
        let all_required_present_in_self = self.required.iter().all(|flag| other.contains_all(flag));
        let all_required_present_in_other = other.required.iter().all(|flag| self.contains_all(flag));
        all_required_present_in_self && all_required_present_in_other
    }

    pub fn try_get_string_value(&self, name: &str) -> Option<&String> {
        self.optional.iter().chain(self.required.iter()).find_map(|flag| {
            if flag.name == name {
                flag.details.as_option().and_then(|x| match x {
                    RequirementFlagValue::Property(value) => Some(value),
                    _ => None,
                })
            } else {
                None
            }
        })
    }
}

#[cfg(test)]
mod tests {
    use crate::feature::KnownOrUnknownRequirementFlagValue;
    use crate::feature::RequirementFlag;
    use crate::feature::RequirementFlagValue;
    use crate::feature::Requirements;

    #[test]
    fn test_deserialization() {
        let requirements: Requirements = serde_json::from_str(
            r#"
        {
            "required": [
                {
                    "name": "FEATURE_1",
                    "details": {
                        "type": "SUPPORTED"
                    }
                },
                {
                    "name": "FEATURE_2",
                    "details": {
                        "type": "PROPERTY",
                        "value": "hello"
                    }
                },
                {
                    "name": "FEATURE_3",
                    "details": {
                        "type": "SOMETHING_NEW",
                        "value": 123123
                    }
                }
            ],
            "optional": []
        }
        "#,
        )
        .unwrap();

        assert_eq!(requirements.optional, vec![]);
        assert_eq!(requirements.required, vec![
            RequirementFlag {
                name: "FEATURE_1".to_string(),
                details: KnownOrUnknownRequirementFlagValue::Known(RequirementFlagValue::Supported)
            },
            RequirementFlag {
                name: "FEATURE_2".to_string(),
                details: KnownOrUnknownRequirementFlagValue::Known(RequirementFlagValue::Property("hello".to_string()))
            },
            RequirementFlag { name: "FEATURE_3".to_string(), details: KnownOrUnknownRequirementFlagValue::Unknown }
        ]);
    }

    #[test]
    fn test_compatibility_check() {
        // Requires features match optional features
        let req1 = Requirements {
            optional: vec![RequirementFlag::from_supported("FEATURE_1"), RequirementFlag::from_supported("FEATURE_4")],
            required: vec![RequirementFlag::from_supported("FEATURE_2")],
        };
        let req2 = Requirements {
            optional: vec![RequirementFlag::from_supported("FEATURE_2"), RequirementFlag::from_supported("FEATURE_5")],
            required: vec![RequirementFlag::from_supported("FEATURE_1")],
        };

        assert!(req1.is_compatible_with(&req2));
        assert!(req2.is_compatible_with(&req1));

        // Required features must be present in the other set, otherwise it compatibility check fails
        let req1 = Requirements {
            optional: vec![RequirementFlag::from_supported("FEATURE_1"), RequirementFlag::from_supported("FEATURE_2")],
            required: vec![RequirementFlag::from_supported("FEATURE_3")],
        };
        let req2 = Requirements {
            optional: vec![],
            required: vec![RequirementFlag::from_supported("FEATURE_1"), RequirementFlag::from_supported("FEATURE_2")],
        };

        assert!(!req1.is_compatible_with(&req2));
        assert!(!req2.is_compatible_with(&req1));
    }
}
