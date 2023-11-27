use delta_data_room_api::prost::Message;
use delta_data_room_api::ConfigurationCommit;
use delta_data_room_api::DataRoom;
use schemars::JsonSchema;
use serde::Deserialize;
use serde::Serialize;

use super::shared::CommitCompileContext;
use super::shared::DataRoomCompileContext;
use super::v0::DataScienceDataRoomV0;
use super::v1::DataScienceDataRoomV1;
use super::v2::DataScienceDataRoomV2;
use super::v3::DataScienceDataRoomV3;
use super::v4::DataScienceDataRoomV4;
use super::v5::DataScienceDataRoomV5;
use super::CompileVersion;
use crate::error::*;
use crate::Compile;

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub enum DataScienceDataRoom {
    V0(DataScienceDataRoomV0),
    V1(DataScienceDataRoomV1),
    V2(DataScienceDataRoomV2),
    V3(DataScienceDataRoomV3),
    V4(DataScienceDataRoomV4),
    V5(DataScienceDataRoomV5),
}

impl DataScienceDataRoom {
    pub fn upgrade_to_latest(self) -> Self {
        match self {
            Self::V0(v0) => Self::upgrade_to_latest(Self::V1(v0.upgrade())),
            Self::V1(v1) => Self::upgrade_to_latest(Self::V2(v1.upgrade())),
            Self::V2(v2) => Self::upgrade_to_latest(Self::V3(v2.upgrade())),
            Self::V3(v3) => Self::upgrade_to_latest(Self::V4(v3.upgrade())),
            Self::V4(v4) => Self::upgrade_to_latest(Self::V5(v4.upgrade())),
            Self::V5(v5) => Self::V5(v5),
        }
    }

    pub fn version(&self) -> CompileVersion {
        match self {
            DataScienceDataRoom::V0(inner) => inner.version(),
            DataScienceDataRoom::V1(inner) => inner.version(),
            DataScienceDataRoom::V2(inner) => inner.version(),
            DataScienceDataRoom::V3(inner) => inner.version(),
            DataScienceDataRoom::V4(inner) => inner.version(),
            DataScienceDataRoom::V5(inner) => inner.version(),
        }
    }
}

type LowLevelDataRoom = Vec<u8>;
type LowLevelCommit = Vec<u8>;

impl Compile for DataScienceDataRoom {
    type CompileContext = DataRoomCompileContext;
    type HighLevelOutput = Vec<u8>;
    type LowLevelOutput = (LowLevelDataRoom, Vec<LowLevelCommit>);
    type OutputContext = CommitCompileContext;

    fn compile(self, context: Self::CompileContext) -> Result<Self::CompileOutput, CompileError> {
        let serialized_self = serde_json::to_vec(&self)
            .map_err(|err| CompileError(format!("failed to serialize DataScienceDataRoom into JSON: {:?}", err)))?;
        match (self, context) {
            (DataScienceDataRoom::V0(data_science_data_room), DataRoomCompileContext::V0(context)) => {
                let ((data_room, commits), _, new_context) = data_science_data_room.compile(context)?;
                Ok((
                    (
                        data_room.encode_length_delimited_to_vec(),
                        commits.into_iter().map(|commit| commit.encode_length_delimited_to_vec()).collect(),
                    ),
                    serialized_self,
                    CommitCompileContext::V0(new_context),
                ))
            }
            (DataScienceDataRoom::V1(data_science_data_room), DataRoomCompileContext::V0(context)) => {
                let ((data_room, commits), _, new_context) = data_science_data_room.compile(context)?;
                Ok((
                    (
                        data_room.encode_length_delimited_to_vec(),
                        commits.into_iter().map(|commit| commit.encode_length_delimited_to_vec()).collect(),
                    ),
                    serialized_self,
                    CommitCompileContext::V1(new_context),
                ))
            }
            (DataScienceDataRoom::V2(data_science_data_room), DataRoomCompileContext::V0(context)) => {
                let ((data_room, commits), _, new_context) = data_science_data_room.compile(context)?;
                Ok((
                    (
                        data_room.encode_length_delimited_to_vec(),
                        commits.into_iter().map(|commit| commit.encode_length_delimited_to_vec()).collect(),
                    ),
                    serialized_self,
                    CommitCompileContext::V2(new_context),
                ))
            }
            (DataScienceDataRoom::V3(data_science_data_room), DataRoomCompileContext::V0(context)) => {
                let ((data_room, commits), _, new_context) = data_science_data_room.compile(context)?;
                Ok((
                    (
                        data_room.encode_length_delimited_to_vec(),
                        commits.into_iter().map(|commit| commit.encode_length_delimited_to_vec()).collect(),
                    ),
                    serialized_self,
                    CommitCompileContext::V3(new_context),
                ))
            }
            (DataScienceDataRoom::V4(data_science_data_room), DataRoomCompileContext::V0(context)) => {
                let ((data_room, commits), _, new_context) = data_science_data_room.compile(context)?;
                Ok((
                    (
                        data_room.encode_length_delimited_to_vec(),
                        commits.into_iter().map(|commit| commit.encode_length_delimited_to_vec()).collect(),
                    ),
                    serialized_self,
                    CommitCompileContext::V4(new_context),
                ))
            }
            (DataScienceDataRoom::V5(data_science_data_room), DataRoomCompileContext::V0(context)) => {
                let ((data_room, commits), _, new_context) = data_science_data_room.compile(context)?;
                Ok((
                    (
                        data_room.encode_length_delimited_to_vec(),
                        commits.into_iter().map(|commit| commit.encode_length_delimited_to_vec()).collect(),
                    ),
                    serialized_self,
                    CommitCompileContext::V5(new_context),
                ))
            }
        }
    }

    fn verify(
        (low_level_data_room, low_level_commits): Self::LowLevelOutput,
        high_level: Self::HighLevelOutput,
        context: Self::CompileContext,
    ) -> Result<Self, VerificationError> {
        match context {
            DataRoomCompileContext::V0(context) => {
                let data_room = DataRoom::decode_length_delimited(low_level_data_room.as_slice())
                    .map_err(|err| VerificationError::Other(format!("failed to decode DataRoom: {:?}", err)))?;
                let commits = low_level_commits
                    .into_iter()
                    .map(|commit| {
                        ConfigurationCommit::decode_length_delimited(commit.as_slice()).map_err(|err| {
                            VerificationError::Other(format!("failed to decode ConfigurationCommit: {:?}", err))
                        })
                    })
                    .collect::<Result<Vec<_>, VerificationError>>()?;
                let data_science_data_room: DataScienceDataRoom = serde_json::from_slice(&high_level)
                    .map_err(|err| VerificationError::Other(format!("Failed to decode input: {:?}", err)))?;
                match data_science_data_room {
                    DataScienceDataRoom::V0(data_science_data_room) => Ok(DataScienceDataRoom::V0(
                        DataScienceDataRoomV0::verify((data_room, commits), data_science_data_room, context)?,
                    )),
                    DataScienceDataRoom::V1(data_science_data_room) => Ok(DataScienceDataRoom::V1(
                        DataScienceDataRoomV1::verify((data_room, commits), data_science_data_room, context)?,
                    )),
                    DataScienceDataRoom::V2(data_science_data_room) => Ok(DataScienceDataRoom::V2(
                        DataScienceDataRoomV2::verify((data_room, commits), data_science_data_room, context)?,
                    )),
                    DataScienceDataRoom::V3(data_science_data_room) => Ok(DataScienceDataRoom::V3(
                        DataScienceDataRoomV3::verify((data_room, commits), data_science_data_room, context)?,
                    )),
                    DataScienceDataRoom::V4(data_science_data_room) => Ok(DataScienceDataRoom::V4(
                        DataScienceDataRoomV4::verify((data_room, commits), data_science_data_room, context)?,
                    )),
                    DataScienceDataRoom::V5(data_science_data_room) => Ok(DataScienceDataRoom::V5(
                        DataScienceDataRoomV5::verify((data_room, commits), data_science_data_room, context)?,
                    )),
                }
            }
        }
    }
}
