#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct SqlWorkerConfiguration {
    #[prost(oneof = "sql_worker_configuration::Configuration", tags = "1, 2")]
    pub configuration: ::core::option::Option<sql_worker_configuration::Configuration>,
}
/// Nested message and enum types in `SqlWorkerConfiguration`.
pub mod sql_worker_configuration {
    #[allow(clippy::derive_partial_eq_without_eq)]
    #[derive(Clone, PartialEq, ::prost::Oneof)]
    pub enum Configuration {
        #[prost(message, tag = "1")]
        Validation(super::ValidationConfiguration),
        #[prost(message, tag = "2")]
        Computation(super::ComputationConfiguration),
    }
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct ValidationConfiguration {
    #[prost(message, optional, tag = "1")]
    pub table_schema: ::core::option::Option<TableSchema>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct TableSchema {
    #[prost(message, repeated, tag = "1")]
    pub named_columns: ::prost::alloc::vec::Vec<NamedColumn>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct NamedColumn {
    #[prost(string, optional, tag = "1")]
    pub name: ::core::option::Option<::prost::alloc::string::String>,
    #[prost(message, optional, tag = "2")]
    pub column_type: ::core::option::Option<ColumnType>,
}
#[derive(::serde::Deserialize, ::serde::Serialize, Eq, std::hash::Hash)]
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct ColumnType {
    #[prost(enumeration = "PrimitiveType", tag = "1")]
    pub primitive_type: i32,
    #[prost(bool, tag = "2")]
    pub nullable: bool,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct TableDependencyMapping {
    /// Name of the table as it appears in the SQL query string
    #[prost(string, tag = "1")]
    pub table: ::prost::alloc::string::String,
    /// ID of the compute/data node that provides data for this table
    #[prost(string, tag = "2")]
    pub dependency: ::prost::alloc::string::String,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct ComputationConfiguration {
    #[prost(string, tag = "1")]
    pub sql_statement: ::prost::alloc::string::String,
    #[prost(message, optional, tag = "2")]
    pub privacy_settings: ::core::option::Option<PrivacySettings>,
    #[prost(message, repeated, tag = "3")]
    pub constraints: ::prost::alloc::vec::Vec<Constraint>,
    #[prost(message, repeated, tag = "4")]
    pub table_dependency_mappings: ::prost::alloc::vec::Vec<TableDependencyMapping>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct PrivacySettings {
    #[prost(int64, tag = "1")]
    pub min_aggregation_group_size: i64,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct Constraint {
    #[prost(string, tag = "1")]
    pub description: ::prost::alloc::string::String,
}
#[derive(::serde::Deserialize, ::serde::Serialize)]
#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash, PartialOrd, Ord, ::prost::Enumeration)]
#[repr(i32)]
pub enum PrimitiveType {
    Int64 = 0,
    String = 1,
    Float64 = 2,
}
impl PrimitiveType {
    /// String value of the enum field names used in the ProtoBuf definition.
    ///
    /// The values are not transformed in any way and thus are considered stable
    /// (if the ProtoBuf definition does not change) and safe for programmatic use.
    pub fn as_str_name(&self) -> &'static str {
        match self {
            PrimitiveType::Int64 => "INT64",
            PrimitiveType::String => "STRING",
            PrimitiveType::Float64 => "FLOAT64",
        }
    }
    /// Creates an enum from field names used in the ProtoBuf definition.
    pub fn from_str_name(value: &str) -> ::core::option::Option<Self> {
        match value {
            "INT64" => Some(Self::Int64),
            "STRING" => Some(Self::String),
            "FLOAT64" => Some(Self::Float64),
            _ => None,
        }
    }
}
