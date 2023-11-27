#[derive(::serde::Deserialize, ::serde::Serialize)]
#[derive(Eq, Hash)]
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct DataRoom {
    #[prost(string, tag = "1")]
    pub id: ::prost::alloc::string::String,
    #[prost(string, tag = "2")]
    pub name: ::prost::alloc::string::String,
    #[prost(string, tag = "3")]
    pub description: ::prost::alloc::string::String,
    #[prost(message, optional, tag = "4")]
    pub governance_protocol: ::core::option::Option<GovernanceProtocol>,
    #[prost(message, optional, tag = "5")]
    pub initial_configuration: ::core::option::Option<DataRoomConfiguration>,
}
#[derive(::serde::Deserialize, ::serde::Serialize)]
#[derive(Eq, Hash)]
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct GovernanceProtocol {
    #[prost(oneof = "governance_protocol::Policy", tags = "1, 2")]
    pub policy: ::core::option::Option<governance_protocol::Policy>,
}
/// Nested message and enum types in `GovernanceProtocol`.
pub mod governance_protocol {
    #[derive(::serde::Deserialize, ::serde::Serialize)]
    #[derive(Eq, Hash)]
    #[allow(clippy::derive_partial_eq_without_eq)]
    #[derive(Clone, PartialEq, ::prost::Oneof)]
    pub enum Policy {
        #[prost(message, tag = "1")]
        StaticDataRoomPolicy(super::StaticDataRoomPolicy),
        #[prost(message, tag = "2")]
        AffectedDataOwnersApprovePolicy(super::AffectedDataOwnersApprovePolicy),
    }
}
#[derive(::serde::Deserialize, ::serde::Serialize)]
#[derive(Eq, Hash)]
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct StaticDataRoomPolicy {}
#[derive(::serde::Deserialize, ::serde::Serialize)]
#[derive(Eq, Hash)]
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct AffectedDataOwnersApprovePolicy {}
#[derive(::serde::Deserialize, ::serde::Serialize)]
#[derive(Eq, Hash)]
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct DataRoomConfiguration {
    #[prost(message, repeated, tag = "1")]
    pub elements: ::prost::alloc::vec::Vec<ConfigurationElement>,
}
#[derive(::serde::Deserialize, ::serde::Serialize)]
#[derive(Eq, Hash)]
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct ConfigurationElement {
    #[prost(string, tag = "1")]
    pub id: ::prost::alloc::string::String,
    #[prost(oneof = "configuration_element::Element", tags = "2, 3, 4, 5")]
    pub element: ::core::option::Option<configuration_element::Element>,
}
/// Nested message and enum types in `ConfigurationElement`.
pub mod configuration_element {
    #[derive(::serde::Deserialize, ::serde::Serialize)]
    #[derive(Eq, Hash)]
    #[allow(clippy::derive_partial_eq_without_eq)]
    #[derive(Clone, PartialEq, ::prost::Oneof)]
    pub enum Element {
        #[prost(message, tag = "2")]
        ComputeNode(super::ComputeNode),
        #[prost(message, tag = "3")]
        AttestationSpecification(::delta_attestation_api::AttestationSpecification),
        #[prost(message, tag = "4")]
        UserPermission(super::UserPermission),
        #[prost(message, tag = "5")]
        AuthenticationMethod(super::AuthenticationMethod),
    }
}
#[derive(::serde::Deserialize, ::serde::Serialize)]
#[derive(Eq, Hash)]
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct ConfigurationModification {
    #[prost(oneof = "configuration_modification::Modification", tags = "1, 2, 3")]
    pub modification: ::core::option::Option<configuration_modification::Modification>,
}
/// Nested message and enum types in `ConfigurationModification`.
pub mod configuration_modification {
    #[derive(::serde::Deserialize, ::serde::Serialize)]
    #[derive(Eq, Hash)]
    #[allow(clippy::derive_partial_eq_without_eq)]
    #[derive(Clone, PartialEq, ::prost::Oneof)]
    pub enum Modification {
        #[prost(message, tag = "1")]
        Add(super::AddModification),
        #[prost(message, tag = "2")]
        Change(super::ChangeModification),
        #[prost(message, tag = "3")]
        Delete(super::DeleteModification),
    }
}
#[derive(::serde::Deserialize, ::serde::Serialize)]
#[derive(Eq, Hash)]
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct AddModification {
    #[prost(message, optional, tag = "1")]
    pub element: ::core::option::Option<ConfigurationElement>,
}
#[derive(::serde::Deserialize, ::serde::Serialize)]
#[derive(Eq, Hash)]
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct ChangeModification {
    #[prost(message, optional, tag = "1")]
    pub element: ::core::option::Option<ConfigurationElement>,
}
#[derive(::serde::Deserialize, ::serde::Serialize)]
#[derive(Eq, Hash)]
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct DeleteModification {
    #[prost(string, tag = "1")]
    pub id: ::prost::alloc::string::String,
}
#[derive(::serde::Deserialize, ::serde::Serialize)]
#[derive(Eq, Hash)]
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct ConfigurationCommit {
    #[prost(string, tag = "1")]
    pub id: ::prost::alloc::string::String,
    #[prost(string, tag = "2")]
    pub name: ::prost::alloc::string::String,
    #[prost(bytes = "vec", tag = "3")]
    pub data_room_id: ::prost::alloc::vec::Vec<u8>,
    #[prost(bytes = "vec", tag = "4")]
    pub data_room_history_pin: ::prost::alloc::vec::Vec<u8>,
    #[prost(message, repeated, tag = "5")]
    pub modifications: ::prost::alloc::vec::Vec<ConfigurationModification>,
}
#[derive(::serde::Deserialize, ::serde::Serialize)]
#[derive(Eq, Hash)]
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct WindowRateLimitingConfig {
    #[prost(uint32, tag = "1")]
    pub time_window_seconds: u32,
    #[prost(uint32, tag = "2")]
    pub num_max_executions: u32,
}
#[derive(::serde::Deserialize, ::serde::Serialize)]
#[derive(Eq, Hash)]
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct RateLimitingConfig {
    #[prost(oneof = "rate_limiting_config::Method", tags = "1")]
    pub method: ::core::option::Option<rate_limiting_config::Method>,
}
/// Nested message and enum types in `RateLimitingConfig`.
pub mod rate_limiting_config {
    #[derive(::serde::Deserialize, ::serde::Serialize)]
    #[derive(Eq, Hash)]
    #[allow(clippy::derive_partial_eq_without_eq)]
    #[derive(Clone, PartialEq, ::prost::Oneof)]
    pub enum Method {
        #[prost(message, tag = "1")]
        Window(super::WindowRateLimitingConfig),
    }
}
#[derive(::serde::Deserialize, ::serde::Serialize)]
#[derive(Eq, Hash)]
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct ComputeNode {
    #[prost(string, tag = "1")]
    pub node_name: ::prost::alloc::string::String,
    /// / Control how often this node can be interacted with
    /// / in the defined time interval.
    /// / Imporatant: this is currently checked in the metering extension
    /// / as implementing it in the driver would not give us additional
    /// / security due to replay/reset attacks.
    /// / In this implementation, it only checks direct interactions wit a
    /// / node, it won't check indirect executions (if the node was a dependency
    /// / of another node). This issue is even bigger in DCRs with interactivity
    /// / where someone could simply add a new node on top that doesn't have
    /// / the rate limit applied.
    #[prost(message, optional, tag = "5")]
    pub rate_limiting: ::core::option::Option<RateLimitingConfig>,
    #[prost(oneof = "compute_node::Node", tags = "2, 4, 3")]
    pub node: ::core::option::Option<compute_node::Node>,
}
/// Nested message and enum types in `ComputeNode`.
pub mod compute_node {
    #[derive(::serde::Deserialize, ::serde::Serialize)]
    #[derive(Eq, Hash)]
    #[allow(clippy::derive_partial_eq_without_eq)]
    #[derive(Clone, PartialEq, ::prost::Oneof)]
    pub enum Node {
        #[prost(message, tag = "2")]
        Leaf(super::ComputeNodeLeaf),
        #[prost(message, tag = "4")]
        Parameter(super::ComputeNodeParameter),
        #[prost(message, tag = "3")]
        Branch(super::ComputeNodeBranch),
    }
}
#[derive(::serde::Deserialize, ::serde::Serialize)]
#[derive(Eq, Hash)]
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct ComputeNodeLeaf {
    #[prost(bool, tag = "1")]
    pub is_required: bool,
}
#[derive(::serde::Deserialize, ::serde::Serialize)]
#[derive(Eq, Hash)]
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct ComputeNodeParameter {
    #[prost(bool, tag = "1")]
    pub is_required: bool,
}
#[derive(::serde::Deserialize, ::serde::Serialize)]
#[derive(Eq, Hash)]
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct ComputeNodeProtocol {
    #[prost(uint32, tag = "1")]
    pub version: u32,
}
#[derive(::serde::Deserialize, ::serde::Serialize)]
#[derive(Eq, Hash)]
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct ComputeNodeBranch {
    #[prost(bytes = "vec", tag = "1")]
    pub config: ::prost::alloc::vec::Vec<u8>,
    #[prost(string, repeated, tag = "2")]
    pub dependencies: ::prost::alloc::vec::Vec<::prost::alloc::string::String>,
    #[prost(enumeration = "ComputeNodeFormat", tag = "3")]
    pub output_format: i32,
    #[prost(message, optional, tag = "4")]
    pub protocol: ::core::option::Option<ComputeNodeProtocol>,
    #[prost(string, tag = "5")]
    pub attestation_specification_id: ::prost::alloc::string::String,
}
#[derive(::serde::Deserialize, ::serde::Serialize)]
#[derive(Eq, Hash)]
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct UserPermission {
    #[prost(string, tag = "1")]
    pub email: ::prost::alloc::string::String,
    #[prost(message, repeated, tag = "2")]
    pub permissions: ::prost::alloc::vec::Vec<Permission>,
    #[prost(string, tag = "3")]
    pub authentication_method_id: ::prost::alloc::string::String,
}
#[derive(::serde::Deserialize, ::serde::Serialize)]
#[derive(Eq, Hash)]
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct AuthenticationMethod {
    #[prost(message, optional, tag = "1")]
    pub personal_pki: ::core::option::Option<PkiPolicy>,
    #[prost(message, optional, tag = "2")]
    pub dq_pki: ::core::option::Option<PkiPolicy>,
    /// the policies below could be implemented later on
    /// EmailVerificationPolicy emailVerificationPolicy = 3;
    /// OpenIdConnectPolicy openIdConnectPolicy = 4;
    /// DcrSecretPolicy
    #[prost(message, optional, tag = "3")]
    pub dcr_secret: ::core::option::Option<DcrSecretPolicy>,
}
#[derive(::serde::Deserialize, ::serde::Serialize)]
#[derive(Eq, Hash)]
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct PkiPolicy {
    #[prost(bytes = "vec", tag = "1")]
    pub root_certificate_pem: ::prost::alloc::vec::Vec<u8>,
}
#[derive(::serde::Deserialize, ::serde::Serialize)]
#[derive(Eq, Hash)]
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct DcrSecretPolicy {
    #[prost(bytes = "vec", tag = "1")]
    pub dcr_secret_id: ::prost::alloc::vec::Vec<u8>,
}
#[derive(::serde::Deserialize, ::serde::Serialize)]
#[derive(Eq, Hash)]
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct Permission {
    #[prost(
        oneof = "permission::Permission",
        tags = "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14"
    )]
    pub permission: ::core::option::Option<permission::Permission>,
}
/// Nested message and enum types in `Permission`.
pub mod permission {
    #[derive(::serde::Deserialize, ::serde::Serialize)]
    #[derive(Eq, Hash)]
    #[allow(clippy::derive_partial_eq_without_eq)]
    #[derive(Clone, PartialEq, ::prost::Oneof)]
    pub enum Permission {
        #[prost(message, tag = "1")]
        ExecuteComputePermission(super::ExecuteComputePermission),
        #[prost(message, tag = "2")]
        LeafCrudPermission(super::LeafCrudPermission),
        #[prost(message, tag = "3")]
        RetrieveDataRoomPermission(super::RetrieveDataRoomPermission),
        #[prost(message, tag = "4")]
        RetrieveAuditLogPermission(super::RetrieveAuditLogPermission),
        #[prost(message, tag = "5")]
        RetrieveDataRoomStatusPermission(super::RetrieveDataRoomStatusPermission),
        #[prost(message, tag = "6")]
        UpdateDataRoomStatusPermission(super::UpdateDataRoomStatusPermission),
        #[prost(message, tag = "7")]
        RetrievePublishedDatasetsPermission(super::RetrievePublishedDatasetsPermission),
        #[prost(message, tag = "8")]
        DryRunPermission(super::DryRunPermission),
        #[prost(message, tag = "9")]
        GenerateMergeSignaturePermission(super::GenerateMergeSignaturePermission),
        #[prost(message, tag = "10")]
        ExecuteDevelopmentComputePermission(super::ExecuteDevelopmentComputePermission),
        #[prost(message, tag = "11")]
        MergeConfigurationCommitPermission(super::MergeConfigurationCommitPermission),
        #[prost(message, tag = "12")]
        RetrieveComputeResultPermission(super::RetrieveComputeResultPermission),
        #[prost(message, tag = "13")]
        CasAuxiliaryStatePermission(super::CasAuxiliaryStatePermission),
        #[prost(message, tag = "14")]
        ReadAuxiliaryStatePermission(super::ReadAuxiliaryStatePermission),
    }
}
#[derive(::serde::Deserialize, ::serde::Serialize)]
#[derive(Eq, Hash)]
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct ExecuteComputePermission {
    #[prost(string, tag = "1")]
    pub compute_node_id: ::prost::alloc::string::String,
}
#[derive(::serde::Deserialize, ::serde::Serialize)]
#[derive(Eq, Hash)]
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct LeafCrudPermission {
    #[prost(string, tag = "1")]
    pub leaf_node_id: ::prost::alloc::string::String,
}
#[derive(::serde::Deserialize, ::serde::Serialize)]
#[derive(Eq, Hash)]
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct RetrieveDataRoomPermission {}
#[derive(::serde::Deserialize, ::serde::Serialize)]
#[derive(Eq, Hash)]
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct RetrieveAuditLogPermission {}
#[derive(::serde::Deserialize, ::serde::Serialize)]
#[derive(Eq, Hash)]
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct RetrieveDataRoomStatusPermission {}
#[derive(::serde::Deserialize, ::serde::Serialize)]
#[derive(Eq, Hash)]
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct UpdateDataRoomStatusPermission {}
#[derive(::serde::Deserialize, ::serde::Serialize)]
#[derive(Eq, Hash)]
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct RetrievePublishedDatasetsPermission {}
#[derive(::serde::Deserialize, ::serde::Serialize)]
#[derive(Eq, Hash)]
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct DryRunPermission {}
#[derive(::serde::Deserialize, ::serde::Serialize)]
#[derive(Eq, Hash)]
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct GenerateMergeSignaturePermission {}
#[derive(::serde::Deserialize, ::serde::Serialize)]
#[derive(Eq, Hash)]
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct ExecuteDevelopmentComputePermission {}
#[derive(::serde::Deserialize, ::serde::Serialize)]
#[derive(Eq, Hash)]
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct MergeConfigurationCommitPermission {}
#[derive(::serde::Deserialize, ::serde::Serialize)]
#[derive(Eq, Hash)]
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct RetrieveComputeResultPermission {
    #[prost(string, tag = "1")]
    pub compute_node_id: ::prost::alloc::string::String,
}
#[derive(::serde::Deserialize, ::serde::Serialize)]
#[derive(Eq, Hash)]
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct CasAuxiliaryStatePermission {}
#[derive(::serde::Deserialize, ::serde::Serialize)]
#[derive(Eq, Hash)]
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct ReadAuxiliaryStatePermission {}
#[derive(::serde::Deserialize, ::serde::Serialize)]
#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash, PartialOrd, Ord, ::prost::Enumeration)]
#[repr(i32)]
pub enum ComputeNodeFormat {
    Raw = 0,
    Zip = 1,
}
impl ComputeNodeFormat {
    /// String value of the enum field names used in the ProtoBuf definition.
    ///
    /// The values are not transformed in any way and thus are considered stable
    /// (if the ProtoBuf definition does not change) and safe for programmatic use.
    pub fn as_str_name(&self) -> &'static str {
        match self {
            ComputeNodeFormat::Raw => "RAW",
            ComputeNodeFormat::Zip => "ZIP",
        }
    }
    /// Creates an enum from field names used in the ProtoBuf definition.
    pub fn from_str_name(value: &str) -> ::core::option::Option<Self> {
        match value {
            "RAW" => Some(Self::Raw),
            "ZIP" => Some(Self::Zip),
            _ => None,
        }
    }
}
