use std::fs;

use ddc::data_lab::CreateDataLab;
use ddc::data_lab::DataLab;
use ddc::data_science::commit::DataScienceCommit;
use ddc::data_science::data_room::DataScienceDataRoom;
use ddc::feature::RequirementList;
use ddc::lookalike_media::compiler::LookalikeMediaRequest;
use ddc::lookalike_media::compiler::LookalikeMediaResponse;
use ddc::lookalike_media::CreateLookalikeMediaDataRoom;
use ddc::lookalike_media::LookalikeMediaDataRoom;
use ddc::lookalike_media::LookalikeMediaDataRoomLatest;
use schemars::schema_for;

fn main() {
    for (name, schema) in &[
        ("data_science_data_room", schema_for!(DataScienceDataRoom)),
        ("data_science_commit", schema_for!(DataScienceCommit)),
        ("data_lab", schema_for!(DataLab)),
        ("create_data_lab", schema_for!(CreateDataLab)),
        ("lookalike_media_request", schema_for!(LookalikeMediaRequest)),
        ("lookalike_media_response", schema_for!(LookalikeMediaResponse)),
        ("lookalike_media_data_room_latest", schema_for!(LookalikeMediaDataRoomLatest)),
        ("lookalike_media_data_room", schema_for!(LookalikeMediaDataRoom)),
        ("requirement_list", schema_for!(RequirementList)),
        ("create_lookalike_media_data_room", schema_for!(CreateLookalikeMediaDataRoom)),
    ] {
        fs::write(format!("schemas/{}.json", name), serde_json::to_string_pretty(schema).unwrap())
            .map_err(|_| format!("Unable to write schema {}", name))
            .unwrap();
    }
}
