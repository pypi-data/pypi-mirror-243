use delta_data_room_api::prost::Message;
use delta_data_room_api::ConfigurationCommit;
use schemars::JsonSchema;
use serde::Deserialize;
use serde::Serialize;

use super::shared::CommitCompileContext;
use super::v0::DataScienceCommitV0;
use super::v1::DataScienceCommitV1;
use super::v2::DataScienceCommitV2;
use super::v3::DataScienceCommitV3;
use super::v4::DataScienceCommitV4;
use super::v5::DataScienceCommitV5;
use super::CompileVersion;
use super::DataScienceDataRoom;
use crate::error::*;
use crate::Compile;

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[schemars(deny_unknown_fields)]
#[serde(rename_all = "camelCase")]
pub enum DataScienceCommit {
    V0(DataScienceCommitV0),
    V1(DataScienceCommitV1),
    V2(DataScienceCommitV2),
    V3(DataScienceCommitV3),
    V4(DataScienceCommitV4),
    V5(DataScienceCommitV5),
}

impl From<DataScienceCommitV0> for DataScienceCommit {
    fn from(v0: DataScienceCommitV0) -> Self {
        DataScienceCommit::V0(v0)
    }
}

impl From<DataScienceCommitV1> for DataScienceCommit {
    fn from(v1: DataScienceCommitV1) -> Self {
        DataScienceCommit::V1(v1)
    }
}

impl From<DataScienceCommitV2> for DataScienceCommit {
    fn from(v2: DataScienceCommitV2) -> Self {
        DataScienceCommit::V2(v2)
    }
}

impl From<DataScienceCommitV3> for DataScienceCommit {
    fn from(v3: DataScienceCommitV3) -> Self {
        DataScienceCommit::V3(v3)
    }
}

impl From<DataScienceCommitV4> for DataScienceCommit {
    fn from(v4: DataScienceCommitV4) -> Self {
        DataScienceCommit::V4(v4)
    }
}

impl From<DataScienceCommitV5> for DataScienceCommit {
    fn from(v5: DataScienceCommitV5) -> Self {
        DataScienceCommit::V5(v5)
    }
}

impl DataScienceCommit {
    pub fn version(&self) -> CompileVersion {
        match self {
            DataScienceCommit::V0(inner) => inner.version(),
            DataScienceCommit::V1(inner) => inner.version(),
            DataScienceCommit::V2(inner) => inner.version(),
            DataScienceCommit::V3(inner) => inner.version(),
            DataScienceCommit::V4(inner) => inner.version(),
            DataScienceCommit::V5(inner) => inner.version(),
        }
    }

    pub fn downgrade(self) -> Result<Self, CompileError> {
        match self {
            DataScienceCommit::V0(_) => Err(CompileError("Cannot downgrade V0 commit".into())),
            DataScienceCommit::V1(inner) => Ok(inner.downgrade()?.into()),
            DataScienceCommit::V2(inner) => Ok(inner.downgrade()?.into()),
            DataScienceCommit::V3(inner) => Ok(inner.downgrade()?.into()),
            DataScienceCommit::V4(inner) => Ok(inner.downgrade()?.into()),
            DataScienceCommit::V5(inner) => Ok(inner.downgrade()?.into()),
        }
    }

    pub fn upgrade(self) -> Result<Self, CompileError> {
        match self {
            DataScienceCommit::V0(inner) => Ok(inner.upgrade().into()),
            DataScienceCommit::V1(inner) => Ok(inner.upgrade().into()),
            DataScienceCommit::V2(inner) => Ok(inner.upgrade().into()),
            DataScienceCommit::V3(inner) => Ok(inner.upgrade().into()),
            DataScienceCommit::V4(inner) => Ok(inner.upgrade().into()),
            DataScienceCommit::V5(_inner) => Err(CompileError("Cannot upgrade V5 commit".into())),
        }
    }

    pub fn convert(self, target_data_room: &DataScienceDataRoom) -> Result<Self, CompileError> {
        match self.version().cmp(&target_data_room.version()) {
            std::cmp::Ordering::Equal => Ok(self),
            std::cmp::Ordering::Less => Self::convert(self.upgrade()?, target_data_room),
            std::cmp::Ordering::Greater => Self::convert(self.downgrade()?, target_data_room),
        }
    }

    pub fn upgrade_to_latest(self) -> Result<Self, CompileError> {
        match self {
            Self::V0(inner) => Self::upgrade_to_latest(Self::V1(inner.upgrade())),
            Self::V1(inner) => Self::upgrade_to_latest(Self::V2(inner.upgrade())),
            Self::V2(inner) => Self::upgrade_to_latest(Self::V3(inner.upgrade())),
            Self::V3(inner) => Self::upgrade_to_latest(Self::V4(inner.upgrade())),
            Self::V4(inner) => Self::upgrade_to_latest(Self::V5(inner.upgrade())),
            Self::V5(_) => Ok(self),
        }
    }
}

impl Compile for DataScienceCommit {
    type CompileContext = CommitCompileContext;
    type HighLevelOutput = Vec<u8>;
    type LowLevelOutput = Vec<u8>;
    type OutputContext = CommitCompileContext;

    fn compile(self, context: Self::CompileContext) -> Result<Self::CompileOutput, CompileError> {
        let serialized_self = serde_json::to_vec(&self)
            .map_err(|err| CompileError(format!("failed to serialize DataScienceCommit into JSON: {:?}", err)))?;
        match (self, context) {
            (DataScienceCommit::V0(data_science_commit), CommitCompileContext::V0(context)) => {
                let (compiled, _, new_context) = data_science_commit.compile(context)?;
                Ok((compiled.encode_length_delimited_to_vec(), serialized_self, CommitCompileContext::V0(new_context)))
            }
            (DataScienceCommit::V1(data_science_commit), CommitCompileContext::V1(context)) => {
                let (compiled, _, new_context) = data_science_commit.compile(context)?;
                Ok((compiled.encode_length_delimited_to_vec(), serialized_self, CommitCompileContext::V1(new_context)))
            }
            (DataScienceCommit::V2(data_science_commit), CommitCompileContext::V2(context)) => {
                let (compiled, _, new_context) = data_science_commit.compile(context)?;
                Ok((compiled.encode_length_delimited_to_vec(), serialized_self, CommitCompileContext::V2(new_context)))
            }
            (DataScienceCommit::V3(data_science_commit), CommitCompileContext::V3(context)) => {
                let (compiled, _, new_context) = data_science_commit.compile(context)?;
                Ok((compiled.encode_length_delimited_to_vec(), serialized_self, CommitCompileContext::V3(new_context)))
            }
            (DataScienceCommit::V4(data_science_commit), CommitCompileContext::V4(context)) => {
                let (compiled, _, new_context) = data_science_commit.compile(context)?;
                Ok((compiled.encode_length_delimited_to_vec(), serialized_self, CommitCompileContext::V4(new_context)))
            }
            (DataScienceCommit::V5(data_science_commit), CommitCompileContext::V5(context)) => {
                let (compiled, _, new_context) = data_science_commit.compile(context)?;
                Ok((compiled.encode_length_delimited_to_vec(), serialized_self, CommitCompileContext::V5(new_context)))
            }
            (_, _) => Err(CompileError("Incompatible compile context".to_string())),
        }
    }

    fn verify(
        low_level: Self::LowLevelOutput,
        high_level: Self::HighLevelOutput,
        context: Self::CompileContext,
    ) -> Result<Self, VerificationError> {
        match context {
            CommitCompileContext::V0(context) => {
                let configuration_commit =
                    ConfigurationCommit::decode_length_delimited(low_level.as_slice()).map_err(|err| {
                        VerificationError::Other(format!("failed to decode ConfigurationCommit: {:?}", err))
                    })?;
                let data_science_commit: DataScienceCommit = serde_json::from_slice(&high_level)
                    .map_err(|err| VerificationError::Other(format!("Failed to decode input header: {:?}", err)))?;
                match data_science_commit {
                    DataScienceCommit::V0(data_science_commit) => Ok(DataScienceCommit::V0(
                        DataScienceCommitV0::verify(configuration_commit, data_science_commit, context)?,
                    )),
                    _ => Err(VerificationError::Other("Incompatible commit version".to_string())),
                }
            }
            CommitCompileContext::V1(context) => {
                let configuration_commit =
                    ConfigurationCommit::decode_length_delimited(low_level.as_slice()).map_err(|err| {
                        VerificationError::Other(format!("failed to decode ConfigurationCommit: {:?}", err))
                    })?;
                let data_science_commit: DataScienceCommit = serde_json::from_slice(&high_level)
                    .map_err(|err| VerificationError::Other(format!("Failed to decode input header: {:?}", err)))?;
                match data_science_commit {
                    DataScienceCommit::V1(data_science_commit) => Ok(DataScienceCommit::V1(
                        DataScienceCommitV1::verify(configuration_commit, data_science_commit, context)?,
                    )),
                    _ => Err(VerificationError::Other("Incompatible commit version".to_string())),
                }
            }
            CommitCompileContext::V2(context) => {
                let configuration_commit =
                    ConfigurationCommit::decode_length_delimited(low_level.as_slice()).map_err(|err| {
                        VerificationError::Other(format!("failed to decode ConfigurationCommit: {:?}", err))
                    })?;
                let data_science_commit: DataScienceCommit = serde_json::from_slice(&high_level)
                    .map_err(|err| VerificationError::Other(format!("Failed to decode input header: {:?}", err)))?;
                match data_science_commit {
                    DataScienceCommit::V2(data_science_commit) => Ok(DataScienceCommit::V2(
                        DataScienceCommitV2::verify(configuration_commit, data_science_commit, context)?,
                    )),
                    _ => Err(VerificationError::Other("Incompatible commit version".to_string())),
                }
            }
            CommitCompileContext::V3(context) => {
                let configuration_commit =
                    ConfigurationCommit::decode_length_delimited(low_level.as_slice()).map_err(|err| {
                        VerificationError::Other(format!("failed to decode ConfigurationCommit: {:?}", err))
                    })?;
                let data_science_commit: DataScienceCommit = serde_json::from_slice(&high_level)
                    .map_err(|err| VerificationError::Other(format!("Failed to decode input header: {:?}", err)))?;
                match data_science_commit {
                    DataScienceCommit::V3(data_science_commit) => Ok(DataScienceCommit::V3(
                        DataScienceCommitV3::verify(configuration_commit, data_science_commit, context)?,
                    )),
                    _ => Err(VerificationError::Other("Incompatible commit version".to_string())),
                }
            }
            CommitCompileContext::V4(context) => {
                let configuration_commit =
                    ConfigurationCommit::decode_length_delimited(low_level.as_slice()).map_err(|err| {
                        VerificationError::Other(format!("failed to decode ConfigurationCommit: {:?}", err))
                    })?;
                let data_science_commit: DataScienceCommit = serde_json::from_slice(&high_level)
                    .map_err(|err| VerificationError::Other(format!("Failed to decode input header: {:?}", err)))?;
                match data_science_commit {
                    DataScienceCommit::V4(data_science_commit) => Ok(DataScienceCommit::V4(
                        DataScienceCommitV4::verify(configuration_commit, data_science_commit, context)?,
                    )),
                    _ => Err(VerificationError::Other("Incompatible commit version".to_string())),
                }
            }
            CommitCompileContext::V5(context) => {
                let configuration_commit =
                    ConfigurationCommit::decode_length_delimited(low_level.as_slice()).map_err(|err| {
                        VerificationError::Other(format!("failed to decode ConfigurationCommit: {:?}", err))
                    })?;
                let data_science_commit: DataScienceCommit = serde_json::from_slice(&high_level)
                    .map_err(|err| VerificationError::Other(format!("Failed to decode input header: {:?}", err)))?;
                match data_science_commit {
                    DataScienceCommit::V5(data_science_commit) => Ok(DataScienceCommit::V5(
                        DataScienceCommitV5::verify(configuration_commit, data_science_commit, context)?,
                    )),
                    _ => Err(VerificationError::Other("Incompatible commit version".to_string())),
                }
            }
        }
    }
}
