use ddc::data_science::v0;
use ddc::data_science::CommitCompileContext;
use ddc::data_science::DataRoomCompileContext;
use ddc::data_science::DataScienceCommit;
use ddc::data_science::DataScienceDataRoom;
use ddc::Compile;
use pyo3::exceptions::PyOSError;
use pyo3::prelude::*;
use pyo3::wrap_pyfunction;

pub struct CompilerPyError(pub String);

impl std::convert::From<String> for CompilerPyError {
    fn from(err: String) -> CompilerPyError {
        CompilerPyError(err)
    }
}

impl std::convert::From<CompilerPyError> for PyErr {
    fn from(err: CompilerPyError) -> PyErr {
        PyOSError::new_err(err.0)
    }
}

#[derive(Clone)]
#[pyclass]
pub struct PyCommitCompileContext(CommitCompileContext);

#[pyclass]
pub struct DataScienceDataRoomCompileOutput {
    #[pyo3(get)]
    data_room: Vec<u8>,
    #[pyo3(get)]
    commits: Vec<Vec<u8>>,
    #[pyo3(get)]
    high_level: Vec<u8>,
    #[pyo3(get)]
    commit_context: PyCommitCompileContext,
}

#[pyfunction]
pub fn compile_data_science_data_room(input: String) -> Result<DataScienceDataRoomCompileOutput, CompilerPyError> {
    let data_science_data_room: DataScienceDataRoom =
        serde_json::from_str(&input).map_err(|err| format!("Failed to decode input: {:?}", err))?;
    let ((data_room, commits), high_level, commit_context) = data_science_data_room
        .compile(DataRoomCompileContext::V0(v0::DataRoomCompileContextV0 {}))
        .map_err(|err| format!("Failed to compile: {}", err))?;
    Ok(DataScienceDataRoomCompileOutput {
        data_room,
        commits,
        high_level,
        commit_context: PyCommitCompileContext(commit_context),
    })
}

#[pyfunction]
pub fn verify_data_room(
    low_level_data_room: Vec<u8>,
    low_level_commits: Vec<Vec<u8>>,
    high_level: Vec<u8>,
) -> Result<String, CompilerPyError> {
    let data_science_data_room = DataScienceDataRoom::verify(
        (low_level_data_room, low_level_commits),
        high_level,
        DataRoomCompileContext::V0(v0::DataRoomCompileContextV0 {}),
    )
    .map_err(|err| format!("Failed to verify: {}", err))?;
    let json_data_science_data_room =
        serde_json::to_string(&data_science_data_room).map_err(|err| format!("Failed to encode result: {}", err))?;
    Ok(json_data_science_data_room)
}

#[pyclass]
pub struct DataScienceCommitCompileOutput {
    #[pyo3(get)]
    commit: Vec<u8>,
    #[pyo3(get)]
    high_level: Vec<u8>,
    #[pyo3(get)]
    commit_context: PyCommitCompileContext,
}

#[pyfunction]
pub fn compile_data_science_commit(
    input: String,
    context: PyCommitCompileContext,
) -> Result<DataScienceCommitCompileOutput, CompilerPyError> {
    let data_science_commit: DataScienceCommit =
        serde_json::from_str(&input).map_err(|err| format!("Failed to decode input: {:?}", err))?;
    let (commit, high_level, commit_context) =
        data_science_commit.compile(context.0).map_err(|err| format!("Failed to compile: {}", err))?;
    Ok(DataScienceCommitCompileOutput { commit, high_level, commit_context: PyCommitCompileContext(commit_context) })
}

#[pyfunction]
pub fn verify_configuration_commit(
    low_level: Vec<u8>,
    high_level: Vec<u8>,
    context: PyCommitCompileContext,
) -> Result<String, CompilerPyError> {
    let data_science_commit = DataScienceCommit::verify(low_level, high_level, context.0)
        .map_err(|err| format!("Failed to verify: {}", err))?;
    let json_data_science_commit =
        serde_json::to_string(&data_science_commit).map_err(|err| format!("Failed to encode result: {}", err))?;
    Ok(json_data_science_commit)
}

#[pyfunction]
pub fn compile_lookalike_media_data_room_serialized(input: String) -> Result<Vec<u8>, CompilerPyError> {
    let serialized_low_level_dcr = ddc::lookalike_media::compiler::compile_lookalike_media_data_room_serialized(&input)
        .map_err(|err| format!("Failed to compile LAL DCR: {}", err))?;
    Ok(serialized_low_level_dcr)
}

#[pyfunction]
pub fn create_lookalike_media_data_room_serialized(input: String) -> Result<String, CompilerPyError> {
    let serialized_lm_dcr = ddc::lookalike_media::compiler::create_lookalike_media_data_room_serialized(&input)
        .map_err(|err| format!("Failed to create LAL DCR: {}", err))?;
    Ok(serialized_lm_dcr)
}

#[pyfunction]
pub fn compile_data_lab_serialized(input: String) -> Result<Vec<u8>, CompilerPyError> {
    let serialized_low_level_dcr = ddc::data_lab::compiler::compile_data_lab_serialized(&input)
        .map_err(|err| format!("Failed to compile DataLab: {}", err))?;
    Ok(serialized_low_level_dcr)
}

#[pyfunction]
pub fn get_lookalike_media_data_room_consumed_datasets_serialized(
    lm_dcr_serialized: String,
) -> Result<String, CompilerPyError> {
    let serialized_datasets =
        ddc::lookalike_media::compiler::get_lookalike_media_data_room_consumed_datasets_serialized(&lm_dcr_serialized)
            .map_err(|err| format!("Failed to get consumed datasets for LMDCR: {}", err))?;
    Ok(serialized_datasets)
}

#[pyfunction]
pub fn update_data_lab_enclave_specifications_serialized(
    data_lab: String,
    driver_spec: String,
    python_spec: String,
    root_certificate_pem: String,
) -> Result<String, CompilerPyError> {
    let updated_serialized = ddc::data_lab::compiler::update_enclave_specifications_serialized(
        data_lab, driver_spec, python_spec, root_certificate_pem,
    )
    .map_err(|err| format!("Failed to update DataLab: {}", err))?;
    Ok(updated_serialized)
}

#[pyclass]
#[derive(Clone)]
pub enum DataLabNode {
    Users        = 1,
    Segments     = 2,
    Demographics = 3,
    Embeddings   = 4,
    Statistics   = 5,
}

#[pyfunction]
pub fn get_data_lab_node_id(input: DataLabNode) -> String {
    return match input {
        DataLabNode::Users => ddc::data_lab::DATASET_USERS_ID,
        DataLabNode::Segments => ddc::data_lab::DATASET_SEGMENTS_ID,
        DataLabNode::Demographics => ddc::data_lab::DATASET_DEMOGRAPHICS_ID,
        DataLabNode::Embeddings => ddc::data_lab::DATASET_EMBEDDINGS_ID,
        DataLabNode::Statistics => ddc::data_lab::PUBLISHER_DATA_STATISTICS_ID,
    }
    .to_string();
}

#[pyfunction]
pub fn create_data_lab_serialized(input: String) -> Result<String, CompilerPyError> {
    let data_lab_serialized = ddc::data_lab::compiler::create_data_lab_serialized(&input)
        .map_err(|err| format!("Failed to create DataLab: {}", err))?;
    Ok(data_lab_serialized)
}

#[pyfunction]
pub fn is_data_lab_compatible_with_lookalike_media_dcr_serialized(
    serialized_data_lab: String,
    serialized_lm_dcr: String,
) -> Result<bool, CompilerPyError> {
    let is_compatible = ddc::data_lab::compiler::is_data_lab_compatible_with_lookalike_media_dcr_serialized(
        &serialized_data_lab, &serialized_lm_dcr,
    )
    .map_err(|err| format!("Failed to perform compatibility check: {}", err))?;
    Ok(is_compatible)
}

#[pyfunction]
pub fn get_data_lab_features_serialized(input: String) -> Result<Vec<String>, CompilerPyError> {
    let features = ddc::data_lab::compiler::get_data_lab_features_serialized(&input)
        .map_err(|err| format!("Failed to get features for DataLab: {}", err))?;
    Ok(features)
}

#[pyfunction]
pub fn get_lookalike_media_data_room_features_serialized(input: String) -> Result<Vec<String>, CompilerPyError> {
    let features = ddc::lookalike_media::compiler::get_lookalike_media_data_room_features_serialized(&input)
        .map_err(|err| format!("Failed to get features for LMDCR: {}", err))?;
    Ok(features)
}

#[pyfunction]
pub fn get_lookalike_media_node_names_from_data_lab_data_type(input: String) -> Result<String, CompilerPyError> {
    Ok(match input.as_str() {
         ddc::data_lab::provides::MATCHING_DATA => ddc::lookalike_media::v3::compute::v0::DATASET_MATCHING_ID,
         ddc::data_lab::provides::SEGMENTS_DATA => ddc::lookalike_media::v3::compute::v0::DATASET_SEGMENTS_ID,
         ddc::data_lab::provides::DEMOGRAPHICS_DATA => ddc::lookalike_media::v3::compute::v0::DATASET_DEMOGRAPHICS_ID,
         ddc::data_lab::provides::EMBEDDINGS_DATA => ddc::lookalike_media::v3::compute::v0::DATASET_EMBEDDINGS_ID,
         _ => "Unknown",
    }.to_string())
}

#[pymodule]
#[pyo3(name="_ddc_py")]
fn decentriq_dcr_compiler(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_class::<PyCommitCompileContext>()?;
    m.add_class::<DataScienceCommitCompileOutput>()?;
    m.add_class::<DataScienceDataRoomCompileOutput>()?;
    m.add_class::<DataLabNode>()?;
    m.add_function(wrap_pyfunction!(compile_data_science_commit, m)?)?;
    m.add_function(wrap_pyfunction!(compile_data_science_data_room, m)?)?;
    m.add_function(wrap_pyfunction!(verify_configuration_commit, m)?)?;
    m.add_function(wrap_pyfunction!(verify_data_room, m)?)?;
    m.add_function(wrap_pyfunction!(compile_data_lab_serialized, m)?)?;
    m.add_function(wrap_pyfunction!(get_data_lab_node_id, m)?)?;
    m.add_function(wrap_pyfunction!(create_data_lab_serialized, m)?)?;
    m.add_function(wrap_pyfunction!(get_data_lab_features_serialized, m)?)?;
    m.add_function(wrap_pyfunction!(is_data_lab_compatible_with_lookalike_media_dcr_serialized, m)?)?;
    m.add_function(wrap_pyfunction!(compile_lookalike_media_data_room_serialized, m)?)?;
    m.add_function(wrap_pyfunction!(create_lookalike_media_data_room_serialized, m)?)?;
    m.add_function(wrap_pyfunction!(get_lookalike_media_data_room_features_serialized, m)?)?;
    m.add_function(wrap_pyfunction!(update_data_lab_enclave_specifications_serialized, m)?)?;
    m.add_function(wrap_pyfunction!(get_lookalike_media_data_room_consumed_datasets_serialized, m)?)?;
    m.add_function(wrap_pyfunction!(get_lookalike_media_node_names_from_data_lab_data_type, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {

    #[test]
    fn it_works() {
    }
}
