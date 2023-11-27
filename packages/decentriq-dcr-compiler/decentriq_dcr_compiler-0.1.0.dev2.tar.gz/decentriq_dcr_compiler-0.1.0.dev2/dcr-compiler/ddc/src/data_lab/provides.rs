use format_types::v0::FormatType;
use format_types::v0::HashingAlgorithm;

// Dataset flags
// These flags correspond to a data node to which data can be provisioned.
// Using these flags the SDK can determine whether it can provision data to a particular node
// for a particular (potentially future) DataLab version.
pub const MATCHING_DATA: &str = "MATCHING_DATA";
pub const SEGMENTS_DATA: &str = "SEGMENTS_DATA";
pub const DEMOGRAPHICS_DATA: &str = "DEMOGRAPHICS_DATA";
pub const EMBEDDINGS_DATA: &str = "EMBEDDINGS_DATA";

// Metadata flags
// These flags correspond to the properties of the data and are used for checking the compatibility
// between a DataLab and an LMDCR.
pub const MATCHING_DATA_USER_ID_FORMAT: &str = "MATCHING_DATA_USER_ID_FORMAT";
pub const MATCHING_DATA_USER_ID_HASHING_ALGORITHM: &str = "MATCHING_DATA_USER_ID_HASHING_ALGORITHM";
pub const MATCHING_DATA_USER_ID_HASHING_ALGORITHM_UNHASHED: &str = "UNHASHED";

pub fn apply_hashing_algorithm_type_to_format(
    matching_id_format: &FormatType,
    hashing_algorithm: Option<&HashingAlgorithm>,
) -> FormatType {
    match hashing_algorithm {
        None => matching_id_format.clone(),
        Some(hashing) => match &hashing {
            HashingAlgorithm::Sha256Hex => FormatType::HashSha256Hex,
        },
    }
}
