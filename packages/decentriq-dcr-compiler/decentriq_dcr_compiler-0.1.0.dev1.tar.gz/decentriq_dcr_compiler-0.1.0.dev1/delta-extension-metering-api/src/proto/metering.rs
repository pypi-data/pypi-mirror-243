#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct EnclaveInfo {
    #[prost(string, tag = "1")]
    pub attestation_spec_hash_hex: ::prost::alloc::string::String,
    #[prost(string, optional, tag = "2")]
    pub task_queue_name: ::core::option::Option<::prost::alloc::string::String>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct MeteringRequest {
    #[prost(
        oneof = "metering_request::Request",
        tags = "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11"
    )]
    pub request: ::core::option::Option<metering_request::Request>,
}
/// Nested message and enum types in `MeteringRequest`.
pub mod metering_request {
    #[allow(clippy::derive_partial_eq_without_eq)]
    #[derive(Clone, PartialEq, ::prost::Oneof)]
    pub enum Request {
        #[prost(message, tag = "1")]
        CreateDcr(super::CreateDcrRequest),
        #[prost(message, tag = "2")]
        CreateDcrCommit(super::CreateDcrCommitRequest),
        #[prost(message, tag = "3")]
        StopDcr(super::StopDcrRequest),
        #[prost(message, tag = "4")]
        PublishDataset(super::PublishDatasetRequest),
        #[prost(message, tag = "5")]
        UnpublishDataset(super::UnpublishDatasetRequest),
        #[prost(message, tag = "6")]
        WorkerMetadata(super::WorkerMetadataRequest),
        #[prost(message, tag = "7")]
        SubmitWorkerExecutionTime(super::SubmitWorkerExecutionTimeRequest),
        #[prost(message, tag = "8")]
        DcrInteraction(super::DcrInteractionRequest),
        #[prost(message, tag = "9")]
        CreateDataset(super::CreateDatasetRequest),
        #[prost(message, tag = "10")]
        GetOrCreateDatasetScope(super::GetOrCreateDatasetScopeRequest),
        #[prost(message, tag = "11")]
        MergeDcrCommit(super::MergeDcrCommitRequest),
    }
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct MeteringSuccessResponse {
    #[prost(
        oneof = "metering_success_response::Response",
        tags = "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11"
    )]
    pub response: ::core::option::Option<metering_success_response::Response>,
}
/// Nested message and enum types in `MeteringSuccessResponse`.
pub mod metering_success_response {
    #[allow(clippy::derive_partial_eq_without_eq)]
    #[derive(Clone, PartialEq, ::prost::Oneof)]
    pub enum Response {
        #[prost(message, tag = "1")]
        CreateDcr(super::CreateDcrResponse),
        #[prost(message, tag = "2")]
        CreateDcrCommit(super::CreateDcrCommitResponse),
        #[prost(message, tag = "3")]
        StopDcr(super::StopDcrResponse),
        #[prost(message, tag = "4")]
        PublishDataset(super::PublishDatasetResponse),
        #[prost(message, tag = "5")]
        UnpublishDataset(super::UnpublishDatasetResponse),
        #[prost(message, tag = "6")]
        WorkerMetadata(super::WorkerMetadataResponse),
        #[prost(message, tag = "7")]
        SubmitWorkerExecutionTime(super::SubmitWorkerExecutionTimeResponse),
        #[prost(message, tag = "8")]
        DcrInteraction(super::DcrInteractionResponse),
        #[prost(message, tag = "9")]
        CreateDataset(super::CreateDatasetResponse),
        #[prost(message, tag = "10")]
        GetOrCreateDatasetScope(super::GetOrCreateDatasetScopeResponse),
        #[prost(message, tag = "11")]
        MergeDcrCommit(super::MergeDcrCommitResponse),
    }
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct MeteringResponse {
    #[prost(oneof = "metering_response::Response", tags = "1, 2")]
    pub response: ::core::option::Option<metering_response::Response>,
}
/// Nested message and enum types in `MeteringResponse`.
pub mod metering_response {
    #[allow(clippy::derive_partial_eq_without_eq)]
    #[derive(Clone, PartialEq, ::prost::Oneof)]
    pub enum Response {
        #[prost(message, tag = "1")]
        Success(super::MeteringSuccessResponse),
        #[prost(string, tag = "2")]
        Failure(::prost::alloc::string::String),
    }
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct DcrMetadata {
    /// / Why this data room is being created (allows for purpose-based filtering of data rooms)
    #[prost(enumeration = "CreateDcrPurpose", tag = "1")]
    pub purpose: i32,
    /// / Whether to show the organization logo
    #[prost(bool, tag = "2")]
    pub show_organization_logo: bool,
    /// / Whether the DCR requires a password
    #[prost(bool, tag = "3")]
    pub require_password: bool,
    /// / The dcr type
    #[prost(enumeration = "CreateDcrKind", tag = "4")]
    pub kind: i32,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct CreateDcrRequest {
    /// / The DCR hash to be used for the published data room
    #[prost(string, tag = "1")]
    pub id_hex: ::prost::alloc::string::String,
    #[prost(string, tag = "2")]
    pub name: ::prost::alloc::string::String,
    /// / The driver attestation hash
    #[prost(string, tag = "3")]
    pub driver_attestation_hash: ::prost::alloc::string::String,
    #[prost(string, repeated, tag = "4")]
    pub participant_emails: ::prost::alloc::vec::Vec<::prost::alloc::string::String>,
    /// / Optional metadata that will be persisted to the database
    #[prost(bytes = "vec", optional, tag = "5")]
    pub metadata: ::core::option::Option<::prost::alloc::vec::Vec<u8>>,
    /// / Information about the enclaves used in this DCR
    #[prost(message, repeated, tag = "6")]
    pub enclave_info: ::prost::alloc::vec::Vec<EnclaveInfo>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct ExecuteComputationNodeInteraction {
    #[prost(string, tag = "1")]
    pub node_id: ::prost::alloc::string::String,
    /// The rate limiting config that was defined within the DCR for this node (if any)
    #[prost(message, optional, tag = "2")]
    pub rate_limiting: ::core::option::Option<::delta_data_room_api::RateLimitingConfig>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct ExecuteComputationInteraction {
    #[prost(message, repeated, tag = "1")]
    pub nodes: ::prost::alloc::vec::Vec<ExecuteComputationNodeInteraction>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct PublishDatasetInteraction {
    #[prost(string, tag = "1")]
    pub node_id: ::prost::alloc::string::String,
    /// The rate limiting config that was defined within the DCR for this node (if any)
    #[prost(message, optional, tag = "2")]
    pub rate_limiting: ::core::option::Option<::delta_data_room_api::RateLimitingConfig>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct DcrInteractionKind {
    #[prost(oneof = "dcr_interaction_kind::Kind", tags = "1, 2")]
    pub kind: ::core::option::Option<dcr_interaction_kind::Kind>,
}
/// Nested message and enum types in `DcrInteractionKind`.
pub mod dcr_interaction_kind {
    #[allow(clippy::derive_partial_eq_without_eq)]
    #[derive(Clone, PartialEq, ::prost::Oneof)]
    pub enum Kind {
        #[prost(message, tag = "1")]
        ExecuteComputation(super::ExecuteComputationInteraction),
        #[prost(message, tag = "2")]
        PublishDataset(super::PublishDatasetInteraction),
    }
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct DcrInteractionRequest {
    /// / The hex-encoded hash of the data room
    #[prost(string, tag = "1")]
    pub data_room_hash: ::prost::alloc::string::String,
    /// / The driver attestation hash
    #[prost(string, tag = "2")]
    pub driver_attestation_hash: ::prost::alloc::string::String,
    /// Id of the scope to check
    #[prost(string, tag = "3")]
    pub scope_id: ::prost::alloc::string::String,
    /// The type of interactions the user wants to perform
    #[prost(message, optional, tag = "4")]
    pub interaction: ::core::option::Option<DcrInteractionKind>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct PublishDatasetRequest {
    /// / The UUID of the compute node to which this dataset is being published
    #[prost(string, tag = "1")]
    pub compute_node_id: ::prost::alloc::string::String,
    /// / The hex-encoded manifest hash of the dataset
    #[prost(string, tag = "2")]
    pub manifest_hash: ::prost::alloc::string::String,
    /// / The hex-encoded hash of the data room
    #[prost(string, tag = "3")]
    pub data_room_hash: ::prost::alloc::string::String,
    /// / The driver attestation hash
    #[prost(string, tag = "4")]
    pub driver_attestation_hash: ::prost::alloc::string::String,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct CreateDatasetRequest {
    /// / The hex-encoded manifest hash of the dataset
    #[prost(string, tag = "1")]
    pub manifest_hash: ::prost::alloc::string::String,
    /// / The hex-encoded manifest of the dataset
    #[prost(string, optional, tag = "2")]
    pub manifest: ::core::option::Option<::prost::alloc::string::String>,
    /// / The id scope of the scope to which this dataset should be linked
    #[prost(string, tag = "3")]
    pub scope_id: ::prost::alloc::string::String,
    /// / A human-readable name of the dataset that helps to identify it
    #[prost(string, tag = "4")]
    pub name: ::prost::alloc::string::String,
    /// / A human-readable description of the dataset that helps to identify it
    #[prost(string, optional, tag = "5")]
    pub description: ::core::option::Option<::prost::alloc::string::String>,
    /// / The size of this dataset in bytes
    #[prost(uint64, optional, tag = "6")]
    pub size_bytes: ::core::option::Option<u64>,
    /// / Statistics associated with this dataset as a serialized JSON object
    #[prost(string, optional, tag = "7")]
    pub statistics: ::core::option::Option<::prost::alloc::string::String>,
    /// / An id identifying the dataset import as part of which this dataset was created
    #[prost(string, optional, tag = "8")]
    pub dataset_import_id: ::core::option::Option<::prost::alloc::string::String>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct GetOrCreateDatasetScopeRequest {
    #[prost(string, optional, tag = "1")]
    pub manifest_hash: ::core::option::Option<::prost::alloc::string::String>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct UnpublishDatasetRequest {
    /// / The UUID of the compute node to which this dataset is being published
    #[prost(string, tag = "1")]
    pub compute_node_id: ::prost::alloc::string::String,
    /// / The hex-encoded hash of the data room
    #[prost(string, tag = "2")]
    pub data_room_hash: ::prost::alloc::string::String,
    /// / The driver attestation hash
    #[prost(string, tag = "3")]
    pub driver_attestation_hash: ::prost::alloc::string::String,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct StopDcrRequest {
    /// / The hex-encoded data room hash
    #[prost(string, tag = "1")]
    pub data_room_hash: ::prost::alloc::string::String,
    /// / The driver attestation hash
    #[prost(string, tag = "2")]
    pub driver_attestation_hash: ::prost::alloc::string::String,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct CreateDcrCommitRequest {
    /// / The commit id
    #[prost(string, tag = "1")]
    pub id: ::prost::alloc::string::String,
    /// / The DCR hash the commit refers to
    #[prost(string, tag = "2")]
    pub dcr_id_hex: ::prost::alloc::string::String,
    /// / The driver attestation hash
    #[prost(string, tag = "3")]
    pub driver_attestation_hash: ::prost::alloc::string::String,
    /// / Information about the enclaves used in this commit
    #[prost(message, repeated, tag = "6")]
    pub enclave_info: ::prost::alloc::vec::Vec<EnclaveInfo>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct MergeDcrCommitRequest {
    /// / The commit id
    #[prost(string, tag = "1")]
    pub id: ::prost::alloc::string::String,
    /// / The DCR hash the commit refers to
    #[prost(string, tag = "2")]
    pub dcr_id_hex: ::prost::alloc::string::String,
    /// / The driver attestation hash
    #[prost(string, tag = "3")]
    pub driver_attestation_hash: ::prost::alloc::string::String,
    /// / Information about the enclaves that were added to the DCR
    #[prost(message, repeated, tag = "6")]
    pub enclave_info: ::prost::alloc::vec::Vec<EnclaveInfo>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct CreateDcrResponse {}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct GetOrCreateDatasetScopeResponse {
    #[prost(string, tag = "1")]
    pub id: ::prost::alloc::string::String,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct DcrInteractionResponse {}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct CreateDcrCommitResponse {}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct MergeDcrCommitResponse {}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct StopDcrResponse {}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct PublishDatasetResponse {}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct CreateDatasetResponse {
    #[prost(string, tag = "1")]
    pub id: ::prost::alloc::string::String,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct UnpublishDatasetResponse {}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct WorkerMetadataRequest {
    /// / Attestation spec of the worker for which to perform the metadata lookup
    #[prost(message, optional, tag = "1")]
    pub attestation_spec: ::core::option::Option<
        ::delta_attestation_api::AttestationSpecification,
    >,
    /// / Id of the scope in the context of which a computation is performed
    #[prost(string, tag = "2")]
    pub scope_id: ::prost::alloc::string::String,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct WorkerMetadataResponse {
    #[prost(uint64, tag = "1")]
    pub max_execution_seconds: u64,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct SubmitWorkerExecutionTimeRequest {
    #[prost(uint32, tag = "1")]
    pub execution_time_seconds: u32,
    #[prost(message, optional, tag = "2")]
    pub attestation_spec: ::core::option::Option<
        ::delta_attestation_api::AttestationSpecification,
    >,
    /// / Id of the scope in the context of which a computation is performed
    #[prost(string, tag = "3")]
    pub scope_id: ::prost::alloc::string::String,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct SubmitWorkerExecutionTimeResponse {}
#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash, PartialOrd, Ord, ::prost::Enumeration)]
#[repr(i32)]
pub enum CreateDcrPurpose {
    Standard = 0,
    Validation = 1,
    DataImport = 2,
    DataExport = 3,
    DataLab = 4,
}
impl CreateDcrPurpose {
    /// String value of the enum field names used in the ProtoBuf definition.
    ///
    /// The values are not transformed in any way and thus are considered stable
    /// (if the ProtoBuf definition does not change) and safe for programmatic use.
    pub fn as_str_name(&self) -> &'static str {
        match self {
            CreateDcrPurpose::Standard => "STANDARD",
            CreateDcrPurpose::Validation => "VALIDATION",
            CreateDcrPurpose::DataImport => "DATA_IMPORT",
            CreateDcrPurpose::DataExport => "DATA_EXPORT",
            CreateDcrPurpose::DataLab => "DATA_LAB",
        }
    }
    /// Creates an enum from field names used in the ProtoBuf definition.
    pub fn from_str_name(value: &str) -> ::core::option::Option<Self> {
        match value {
            "STANDARD" => Some(Self::Standard),
            "VALIDATION" => Some(Self::Validation),
            "DATA_IMPORT" => Some(Self::DataImport),
            "DATA_EXPORT" => Some(Self::DataExport),
            "DATA_LAB" => Some(Self::DataLab),
            _ => None,
        }
    }
}
#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash, PartialOrd, Ord, ::prost::Enumeration)]
#[repr(i32)]
pub enum CreateDcrKind {
    Expert = 0,
    Datascience = 1,
    Media = 2,
    LookalikeMedia = 3,
}
impl CreateDcrKind {
    /// String value of the enum field names used in the ProtoBuf definition.
    ///
    /// The values are not transformed in any way and thus are considered stable
    /// (if the ProtoBuf definition does not change) and safe for programmatic use.
    pub fn as_str_name(&self) -> &'static str {
        match self {
            CreateDcrKind::Expert => "EXPERT",
            CreateDcrKind::Datascience => "DATASCIENCE",
            CreateDcrKind::Media => "MEDIA",
            CreateDcrKind::LookalikeMedia => "LOOKALIKE_MEDIA",
        }
    }
    /// Creates an enum from field names used in the ProtoBuf definition.
    pub fn from_str_name(value: &str) -> ::core::option::Option<Self> {
        match value {
            "EXPERT" => Some(Self::Expert),
            "DATASCIENCE" => Some(Self::Datascience),
            "MEDIA" => Some(Self::Media),
            "LOOKALIKE_MEDIA" => Some(Self::LookalikeMedia),
            _ => None,
        }
    }
}
