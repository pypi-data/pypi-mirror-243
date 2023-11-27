// Feature flags
// These flags encode the capabilities of a DataLab, i.e. what computations can be run by the SDKs.
// DataLabs that support a particular computation should expose the respective flag in the
// features array. If a future DataLab does not support a particular computation anymore,
// it should be removed. SDKs need to check for these flags when the user calls a method
// that might be supported for some DataLabs, but not for others (which might include future
// DataLabs that are not known yet).
pub const COMPUTE_STATISTICS: &str = "COMPUTE_STATISTICS";
pub const VALIDATE_EMBEDDINGS: &str = "VALIDATE_EMBEDDINGS";
pub const VALIDATE_DEMOGRAPHICS: &str = "VALIDATE_DEMOGRAPHICS";
pub const VALIDATE_MATCHING: &str = "VALIDATE_MATCHING";
pub const VALIDATE_SEGMENTS: &str = "VALIDATE_SEGMENTS";
