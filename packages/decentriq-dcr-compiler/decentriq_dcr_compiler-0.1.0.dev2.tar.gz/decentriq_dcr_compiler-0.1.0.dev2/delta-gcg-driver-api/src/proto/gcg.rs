#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct GcgRequest {
    #[prost(message, optional, tag = "1")]
    pub user_auth: ::core::option::Option<UserAuth>,
    #[prost(
        oneof = "gcg_request::GcgRequest",
        tags = "2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 101"
    )]
    pub gcg_request: ::core::option::Option<gcg_request::GcgRequest>,
}
/// Nested message and enum types in `GcgRequest`.
pub mod gcg_request {
    #[allow(clippy::derive_partial_eq_without_eq)]
    #[derive(Clone, PartialEq, ::prost::Oneof)]
    pub enum GcgRequest {
        #[prost(message, tag = "2")]
        CreateDataRoomRequest(super::CreateDataRoomRequest),
        #[prost(message, tag = "3")]
        RetrieveDataRoomRequest(super::RetrieveDataRoomRequest),
        #[prost(message, tag = "4")]
        RetrieveCurrentDataRoomConfigurationRequest(
            super::RetrieveCurrentDataRoomConfigurationRequest,
        ),
        #[prost(message, tag = "5")]
        RetrieveDataRoomStatusRequest(super::RetrieveDataRoomStatusRequest),
        #[prost(message, tag = "6")]
        UpdateDataRoomStatusRequest(super::UpdateDataRoomStatusRequest),
        #[prost(message, tag = "7")]
        RetrieveAuditLogRequest(super::RetrieveAuditLogRequest),
        #[prost(message, tag = "8")]
        PublishDatasetToDataRoomRequest(super::PublishDatasetToDataRoomRequest),
        #[prost(message, tag = "9")]
        RetrievePublishedDatasetsRequest(super::RetrievePublishedDatasetsRequest),
        #[prost(message, tag = "10")]
        RemovePublishedDatasetRequest(super::RemovePublishedDatasetRequest),
        #[prost(message, tag = "11")]
        ExecuteComputeRequest(super::ExecuteComputeRequest),
        #[prost(message, tag = "12")]
        JobStatusRequest(super::JobStatusRequest),
        #[prost(message, tag = "13")]
        GetResultsRequest(super::GetResultsRequest),
        #[prost(message, tag = "14")]
        CreateConfigurationCommitRequest(super::CreateConfigurationCommitRequest),
        #[prost(message, tag = "15")]
        RetrieveConfigurationCommitRequest(super::RetrieveConfigurationCommitRequest),
        #[prost(message, tag = "16")]
        ExecuteDevelopmentComputeRequest(super::ExecuteDevelopmentComputeRequest),
        #[prost(message, tag = "17")]
        GenerateMergeApprovalSignatureRequest(
            super::GenerateMergeApprovalSignatureRequest,
        ),
        #[prost(message, tag = "18")]
        MergeConfigurationCommitRequest(super::MergeConfigurationCommitRequest),
        #[prost(message, tag = "19")]
        RetrieveConfigurationCommitApproversRequest(
            super::RetrieveConfigurationCommitApproversRequest,
        ),
        #[prost(message, tag = "20")]
        CasAuxiliaryStateRequest(super::CasAuxiliaryStateRequest),
        #[prost(message, tag = "21")]
        ReadAuxiliaryStateRequest(super::ReadAuxiliaryStateRequest),
        #[prost(message, tag = "101")]
        EndorsementRequest(::delta_identity_endorsement_api::EndorsementRequest),
    }
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct GcgResponse {
    #[prost(
        oneof = "gcg_response::GcgResponse",
        tags = "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 101"
    )]
    pub gcg_response: ::core::option::Option<gcg_response::GcgResponse>,
}
/// Nested message and enum types in `GcgResponse`.
pub mod gcg_response {
    #[allow(clippy::derive_partial_eq_without_eq)]
    #[derive(Clone, PartialEq, ::prost::Oneof)]
    pub enum GcgResponse {
        #[prost(string, tag = "1")]
        Failure(::prost::alloc::string::String),
        #[prost(message, tag = "2")]
        CreateDataRoomResponse(super::CreateDataRoomResponse),
        #[prost(message, tag = "3")]
        RetrieveDataRoomResponse(super::RetrieveDataRoomResponse),
        #[prost(message, tag = "4")]
        RetrieveCurrentDataRoomConfigurationResponse(
            super::RetrieveCurrentDataRoomConfigurationResponse,
        ),
        #[prost(message, tag = "5")]
        RetrieveDataRoomStatusResponse(super::RetrieveDataRoomStatusResponse),
        #[prost(message, tag = "6")]
        UpdateDataRoomStatusResponse(super::UpdateDataRoomStatusResponse),
        #[prost(message, tag = "7")]
        RetrieveAuditLogResponse(super::RetrieveAuditLogResponse),
        #[prost(message, tag = "8")]
        PublishDatasetToDataRoomResponse(super::PublishDatasetToDataRoomResponse),
        #[prost(message, tag = "9")]
        RetrievePublishedDatasetsResponse(super::RetrievePublishedDatasetsResponse),
        #[prost(message, tag = "10")]
        RemovePublishedDatasetResponse(super::RemovePublishedDatasetResponse),
        #[prost(message, tag = "11")]
        ExecuteComputeResponse(super::ExecuteComputeResponse),
        #[prost(message, tag = "12")]
        JobStatusResponse(super::JobStatusResponse),
        #[prost(message, tag = "13")]
        GetResultsResponseChunk(super::GetResultsResponseChunk),
        #[prost(message, tag = "14")]
        GetResultsResponseFooter(super::GetResultsResponseFooter),
        #[prost(message, tag = "15")]
        CreateConfigurationCommitResponse(super::CreateConfigurationCommitResponse),
        #[prost(message, tag = "16")]
        RetrieveConfigurationCommitResponse(super::RetrieveConfigurationCommitResponse),
        #[prost(message, tag = "17")]
        GenerateMergeApprovalSignatureResponse(
            super::GenerateMergeApprovalSignatureResponse,
        ),
        #[prost(message, tag = "18")]
        MergeConfigurationCommitResponse(super::MergeConfigurationCommitResponse),
        #[prost(message, tag = "19")]
        RetrieveConfigurationCommitApproversResponse(
            super::RetrieveConfigurationCommitApproversResponse,
        ),
        #[prost(message, tag = "20")]
        CasAuxiliaryStateResponse(super::CasAuxiliaryStateResponse),
        #[prost(message, tag = "21")]
        ReadAuxiliaryStateResponse(super::ReadAuxiliaryStateResponse),
        #[prost(message, tag = "101")]
        EndorsementResponse(::delta_identity_endorsement_api::EndorsementResponse),
    }
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct UserAuth {
    #[prost(message, optional, tag = "1")]
    pub pki: ::core::option::Option<Pki>,
    #[prost(message, optional, tag = "2")]
    pub enclave_endorsements: ::core::option::Option<
        ::delta_identity_endorsement_api::EnclaveEndorsements,
    >,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct Pki {
    #[prost(bytes = "vec", tag = "1")]
    pub cert_chain_pem: ::prost::alloc::vec::Vec<u8>,
    #[prost(bytes = "vec", tag = "2")]
    pub signature: ::prost::alloc::vec::Vec<u8>,
    #[prost(bytes = "vec", tag = "3")]
    pub id_mac: ::prost::alloc::vec::Vec<u8>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct CreateDataRoomRequest {
    #[prost(message, optional, tag = "1")]
    pub data_room: ::core::option::Option<::delta_data_room_api::DataRoom>,
    #[prost(bytes = "vec", optional, tag = "2")]
    pub high_level_representation: ::core::option::Option<::prost::alloc::vec::Vec<u8>>,
    #[prost(bytes = "vec", optional, tag = "3")]
    pub data_room_metadata: ::core::option::Option<::prost::alloc::vec::Vec<u8>>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct CreateDataRoomResponse {
    #[prost(oneof = "create_data_room_response::CreateDataRoomResponse", tags = "1, 2")]
    pub create_data_room_response: ::core::option::Option<
        create_data_room_response::CreateDataRoomResponse,
    >,
}
/// Nested message and enum types in `CreateDataRoomResponse`.
pub mod create_data_room_response {
    #[allow(clippy::derive_partial_eq_without_eq)]
    #[derive(Clone, PartialEq, ::prost::Oneof)]
    pub enum CreateDataRoomResponse {
        #[prost(bytes, tag = "1")]
        DataRoomId(::prost::alloc::vec::Vec<u8>),
        #[prost(message, tag = "2")]
        DataRoomValidationError(super::DataRoomValidationError),
    }
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct DataRoomValidationError {
    #[prost(string, tag = "1")]
    pub message: ::prost::alloc::string::String,
    #[prost(uint64, optional, tag = "2")]
    pub permission_index: ::core::option::Option<u64>,
    #[prost(string, optional, tag = "3")]
    pub compute_node_id: ::core::option::Option<::prost::alloc::string::String>,
    #[prost(string, optional, tag = "4")]
    pub user_permission_id: ::core::option::Option<::prost::alloc::string::String>,
    #[prost(string, optional, tag = "5")]
    pub attestation_specification_id: ::core::option::Option<
        ::prost::alloc::string::String,
    >,
    #[prost(string, optional, tag = "6")]
    pub authentication_method_id: ::core::option::Option<::prost::alloc::string::String>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct PublishDatasetToDataRoomRequest {
    #[prost(bytes = "vec", tag = "1")]
    pub dataset_hash: ::prost::alloc::vec::Vec<u8>,
    #[prost(bytes = "vec", tag = "2")]
    pub data_room_id: ::prost::alloc::vec::Vec<u8>,
    #[prost(string, tag = "3")]
    pub leaf_id: ::prost::alloc::string::String,
    #[prost(bytes = "vec", tag = "4")]
    pub encryption_key: ::prost::alloc::vec::Vec<u8>,
    #[prost(bytes = "vec", tag = "5")]
    pub scope: ::prost::alloc::vec::Vec<u8>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct PublishDatasetToDataRoomResponse {}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct ExecuteComputeRequest {
    #[prost(bytes = "vec", tag = "1")]
    pub data_room_id: ::prost::alloc::vec::Vec<u8>,
    #[prost(string, repeated, tag = "2")]
    pub compute_node_ids: ::prost::alloc::vec::Vec<::prost::alloc::string::String>,
    #[prost(bool, tag = "3")]
    pub is_dry_run: bool,
    #[prost(bytes = "vec", tag = "4")]
    pub scope: ::prost::alloc::vec::Vec<u8>,
    #[prost(btree_map = "string, string", tag = "5")]
    pub parameters: ::prost::alloc::collections::BTreeMap<
        ::prost::alloc::string::String,
        ::prost::alloc::string::String,
    >,
    #[prost(btree_map = "string, message", tag = "6")]
    pub test_datasets: ::prost::alloc::collections::BTreeMap<
        ::prost::alloc::string::String,
        TestDataset,
    >,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct ExecuteDevelopmentComputeRequest {
    #[prost(bytes = "vec", tag = "1")]
    pub configuration_commit_id: ::prost::alloc::vec::Vec<u8>,
    #[prost(string, repeated, tag = "2")]
    pub compute_node_ids: ::prost::alloc::vec::Vec<::prost::alloc::string::String>,
    #[prost(bool, tag = "3")]
    pub is_dry_run: bool,
    #[prost(bytes = "vec", tag = "4")]
    pub scope: ::prost::alloc::vec::Vec<u8>,
    #[prost(btree_map = "string, string", tag = "5")]
    pub parameters: ::prost::alloc::collections::BTreeMap<
        ::prost::alloc::string::String,
        ::prost::alloc::string::String,
    >,
    #[prost(btree_map = "string, message", tag = "6")]
    pub test_datasets: ::prost::alloc::collections::BTreeMap<
        ::prost::alloc::string::String,
        TestDataset,
    >,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct TestDataset {
    #[prost(bytes = "vec", tag = "1")]
    pub encryption_key: ::prost::alloc::vec::Vec<u8>,
    #[prost(bytes = "vec", tag = "2")]
    pub manifest_hash: ::prost::alloc::vec::Vec<u8>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct ExecuteComputeResponse {
    #[prost(bytes = "vec", tag = "1")]
    pub job_id: ::prost::alloc::vec::Vec<u8>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct JobStatusRequest {
    #[prost(bytes = "vec", tag = "1")]
    pub job_id: ::prost::alloc::vec::Vec<u8>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct JobStatusResponse {
    #[prost(string, repeated, tag = "1")]
    pub complete_compute_node_ids: ::prost::alloc::vec::Vec<
        ::prost::alloc::string::String,
    >,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct GetResultsRequest {
    #[prost(bytes = "vec", tag = "1")]
    pub job_id: ::prost::alloc::vec::Vec<u8>,
    #[prost(string, tag = "2")]
    pub compute_node_id: ::prost::alloc::string::String,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct GetResultsResponseChunk {
    #[prost(bytes = "vec", tag = "1")]
    pub data: ::prost::alloc::vec::Vec<u8>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct GetResultsResponseFooter {}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct RetrieveDataRoomRequest {
    #[prost(bytes = "vec", tag = "1")]
    pub data_room_id: ::prost::alloc::vec::Vec<u8>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct RetrieveDataRoomResponse {
    #[prost(message, optional, tag = "1")]
    pub data_room: ::core::option::Option<::delta_data_room_api::DataRoom>,
    #[prost(message, repeated, tag = "2")]
    pub commits: ::prost::alloc::vec::Vec<::delta_data_room_api::ConfigurationCommit>,
    #[prost(bytes = "vec", optional, tag = "3")]
    pub high_level_representation: ::core::option::Option<::prost::alloc::vec::Vec<u8>>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct RetrieveAuditLogRequest {
    #[prost(bytes = "vec", tag = "1")]
    pub data_room_id: ::prost::alloc::vec::Vec<u8>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct RetrieveAuditLogResponse {
    #[prost(bytes = "vec", tag = "1")]
    pub log: ::prost::alloc::vec::Vec<u8>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct RetrieveDataRoomStatusRequest {
    #[prost(bytes = "vec", tag = "1")]
    pub data_room_id: ::prost::alloc::vec::Vec<u8>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct RetrieveDataRoomStatusResponse {
    #[prost(enumeration = "DataRoomStatus", tag = "1")]
    pub status: i32,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct UpdateDataRoomStatusRequest {
    #[prost(bytes = "vec", tag = "1")]
    pub data_room_id: ::prost::alloc::vec::Vec<u8>,
    #[prost(enumeration = "DataRoomStatus", tag = "2")]
    pub status: i32,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct UpdateDataRoomStatusResponse {}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct RetrievePublishedDatasetsRequest {
    #[prost(bytes = "vec", tag = "1")]
    pub data_room_id: ::prost::alloc::vec::Vec<u8>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct PublishedDataset {
    #[prost(string, tag = "1")]
    pub leaf_id: ::prost::alloc::string::String,
    #[prost(string, tag = "2")]
    pub user: ::prost::alloc::string::String,
    #[prost(uint64, tag = "3")]
    pub timestamp: u64,
    #[prost(bytes = "vec", tag = "4")]
    pub dataset_hash: ::prost::alloc::vec::Vec<u8>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct RetrievePublishedDatasetsResponse {
    #[prost(message, repeated, tag = "1")]
    pub published_datasets: ::prost::alloc::vec::Vec<PublishedDataset>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct RemovePublishedDatasetRequest {
    #[prost(bytes = "vec", tag = "1")]
    pub data_room_id: ::prost::alloc::vec::Vec<u8>,
    #[prost(string, tag = "2")]
    pub leaf_id: ::prost::alloc::string::String,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct RemovePublishedDatasetResponse {}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct CreateConfigurationCommitRequest {
    #[prost(message, optional, tag = "1")]
    pub commit: ::core::option::Option<::delta_data_room_api::ConfigurationCommit>,
    #[prost(bytes = "vec", optional, tag = "2")]
    pub high_level_representation: ::core::option::Option<::prost::alloc::vec::Vec<u8>>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct CreateConfigurationCommitResponse {
    #[prost(bytes = "vec", tag = "1")]
    pub commit_id: ::prost::alloc::vec::Vec<u8>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct GenerateMergeApprovalSignatureRequest {
    #[prost(bytes = "vec", tag = "1")]
    pub commit_id: ::prost::alloc::vec::Vec<u8>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct GenerateMergeApprovalSignatureResponse {
    #[prost(bytes = "vec", tag = "1")]
    pub signature: ::prost::alloc::vec::Vec<u8>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct MergeConfigurationCommitRequest {
    #[prost(bytes = "vec", tag = "1")]
    pub commit_id: ::prost::alloc::vec::Vec<u8>,
    #[prost(btree_map = "string, bytes", tag = "2")]
    pub approval_signatures: ::prost::alloc::collections::BTreeMap<
        ::prost::alloc::string::String,
        ::prost::alloc::vec::Vec<u8>,
    >,
    #[prost(bytes = "vec", optional, tag = "3")]
    pub new_data_room_high_level_representation: ::core::option::Option<
        ::prost::alloc::vec::Vec<u8>,
    >,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct RetrieveCurrentDataRoomConfigurationRequest {
    #[prost(bytes = "vec", tag = "1")]
    pub data_room_id: ::prost::alloc::vec::Vec<u8>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct RetrieveCurrentDataRoomConfigurationResponse {
    #[prost(message, optional, tag = "1")]
    pub configuration: ::core::option::Option<
        ::delta_data_room_api::DataRoomConfiguration,
    >,
    #[prost(bytes = "vec", tag = "2")]
    pub pin: ::prost::alloc::vec::Vec<u8>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct RetrieveConfigurationCommitApproversRequest {
    #[prost(bytes = "vec", tag = "1")]
    pub commit_id: ::prost::alloc::vec::Vec<u8>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct RetrieveConfigurationCommitApproversResponse {
    #[prost(string, repeated, tag = "1")]
    pub approvers: ::prost::alloc::vec::Vec<::prost::alloc::string::String>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct RetrieveConfigurationCommitRequest {
    #[prost(bytes = "vec", tag = "1")]
    pub commit_id: ::prost::alloc::vec::Vec<u8>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct RetrieveConfigurationCommitResponse {
    #[prost(message, optional, tag = "1")]
    pub commit: ::core::option::Option<::delta_data_room_api::ConfigurationCommit>,
    #[prost(bytes = "vec", optional, tag = "2")]
    pub high_level_representation: ::core::option::Option<::prost::alloc::vec::Vec<u8>>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct CasAuxiliaryStateRequest {
    #[prost(bytes = "vec", tag = "1")]
    pub data_room_id: ::prost::alloc::vec::Vec<u8>,
    /// The index indicates what the client thinks the state is. The CAS operation will only succeed if the index
    /// matches what's stored in the enclave. The index is 0 iff the value doesn't exist/was deleted.
    #[prost(uint64, tag = "2")]
    pub index: u64,
    /// If null it will try to delete value.
    #[prost(bytes = "vec", optional, tag = "3")]
    pub value: ::core::option::Option<::prost::alloc::vec::Vec<u8>>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct CasAuxiliaryStateResponse {
    #[prost(bool, tag = "1")]
    pub success: bool,
    /// The index at the end of the operation, 0 if delete was successful. If success=false, the client should use this
    /// index and retry the operation, possibly modified based on the returned value.
    /// Example: User A is racing on two clients X and Y to add numbers 1 and 2 to an initially empty list.
    ///    1. index=0 list=[]: initial state
    ///    2. index=1 list=\[1\]: User A on client X does CAS(index=0, value=\[1\])
    ///    3. index=1 list=\[1\]: User A on client Y does CAS(index=0, value=\[2\]) => success=false, index=1, value=\[1\]
    ///    4. index=2 list=\[1,2\]: User A on client Y retries with CAS(index=1, value=\[1,2\])
    #[prost(uint64, tag = "2")]
    pub index: u64,
    /// The value at the end of the operation.
    #[prost(bytes = "vec", optional, tag = "3")]
    pub value: ::core::option::Option<::prost::alloc::vec::Vec<u8>>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct ReadAuxiliaryStateRequest {
    #[prost(bytes = "vec", tag = "1")]
    pub data_room_id: ::prost::alloc::vec::Vec<u8>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct ReadAuxiliaryStateResponse {
    #[prost(message, repeated, tag = "2")]
    pub values: ::prost::alloc::vec::Vec<AuxiliaryStateValue>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct AuxiliaryStateValue {
    #[prost(string, tag = "1")]
    pub user: ::prost::alloc::string::String,
    #[prost(uint64, tag = "2")]
    pub index: u64,
    #[prost(bytes = "vec", tag = "3")]
    pub value: ::prost::alloc::vec::Vec<u8>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct MergeConfigurationCommitResponse {}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct DriverTaskConfig {
    #[prost(oneof = "driver_task_config::DriverTaskConfig", tags = "1, 2")]
    pub driver_task_config: ::core::option::Option<driver_task_config::DriverTaskConfig>,
}
/// Nested message and enum types in `DriverTaskConfig`.
pub mod driver_task_config {
    #[allow(clippy::derive_partial_eq_without_eq)]
    #[derive(Clone, PartialEq, ::prost::Oneof)]
    pub enum DriverTaskConfig {
        #[prost(message, tag = "1")]
        Noop(super::NoopConfig),
        #[prost(message, tag = "2")]
        StaticContent(super::StaticContentConfig),
    }
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct NoopConfig {}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct StaticContentConfig {
    #[prost(bytes = "vec", tag = "1")]
    pub content: ::prost::alloc::vec::Vec<u8>,
}
#[derive(::serde::Deserialize, ::serde::Serialize)]
#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash, PartialOrd, Ord, ::prost::Enumeration)]
#[repr(i32)]
pub enum DataRoomStatus {
    Active = 0,
    Stopped = 1,
}
impl DataRoomStatus {
    /// String value of the enum field names used in the ProtoBuf definition.
    ///
    /// The values are not transformed in any way and thus are considered stable
    /// (if the ProtoBuf definition does not change) and safe for programmatic use.
    pub fn as_str_name(&self) -> &'static str {
        match self {
            DataRoomStatus::Active => "Active",
            DataRoomStatus::Stopped => "Stopped",
        }
    }
    /// Creates an enum from field names used in the ProtoBuf definition.
    pub fn from_str_name(value: &str) -> ::core::option::Option<Self> {
        match value {
            "Active" => Some(Self::Active),
            "Stopped" => Some(Self::Stopped),
            _ => None,
        }
    }
}
