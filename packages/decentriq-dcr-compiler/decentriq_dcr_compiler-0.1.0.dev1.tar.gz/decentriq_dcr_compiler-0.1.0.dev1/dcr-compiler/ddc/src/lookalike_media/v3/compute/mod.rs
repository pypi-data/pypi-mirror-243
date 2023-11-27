use delta_data_room_api::DataRoom;
use schemars::JsonSchema;
use serde::Deserialize;
use serde::Serialize;

use crate::error::CompileError;
use crate::feature::Requirements;
use crate::lookalike_media::v3::LookalikeMediaDcrComputeOrUnknown;

pub mod v0;

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub enum LookalikeMediaDcrCompute {
    V0(v0::LookalikeMediaDcrComputeV0),
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub enum CreateLookalikeMediaDcrCompute {
    V0(v0::CreateLookalikeMediaDcrComputeV0),
}

pub fn compile_data_room_compute(
    data_room: &LookalikeMediaDcrComputeOrUnknown,
    features: &Vec<String>,
    requirements: &Requirements,
) -> Result<DataRoom, CompileError> {
    match data_room {
        LookalikeMediaDcrComputeOrUnknown::Known(compute) => match compute {
            LookalikeMediaDcrCompute::V0(compute) => v0::compile_compute(compute, features, requirements),
        },
        LookalikeMediaDcrComputeOrUnknown::Unknown => Err(CompileError::from(
            "Encountered an unknown compute version that is not known to this version of the compiler",
        )),
    }
}
