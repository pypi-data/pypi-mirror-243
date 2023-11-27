mod proto;

pub use proto::*;
pub use prost;

pub const EXTENSION_NAME: &'static str = "metering";

/// Returns whether a DCR is considered *temporary* based on its purpose.
/// A *temporary* DCR has a strictly limited lifetime, defined by the GC policy.
/// Furthermore, we enable creation of temporary DCRs regardless of whether the creating user
/// is licensed or not.
/// This function is specifically written to contain an enum exhaustiveness check.
pub fn is_temporary_dcr_purpose(purpose: &CreateDcrPurpose) -> bool {
    match purpose {
        CreateDcrPurpose::Standard => false,
        CreateDcrPurpose::Validation => true,
        CreateDcrPurpose::DataImport => true,
        CreateDcrPurpose::DataExport => true,
        CreateDcrPurpose::DataLab => true,
    }
}

// Returns the list of temporary DCR purposes.
pub fn get_temporary_dcr_purposes() -> Vec<CreateDcrPurpose> {
    let mut temporary_purposes = vec![];
    for i in 0 .. std::mem::size_of_val(&CreateDcrPurpose::Standard) {
        let purpose: CreateDcrPurpose = CreateDcrPurpose::from_i32(i as i32).unwrap();
        if is_temporary_dcr_purpose(&purpose) {
            temporary_purposes.push(purpose);
        }
    }
    temporary_purposes
}
