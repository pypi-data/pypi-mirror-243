#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct S3SinkWorkerConfiguration {
    #[prost(string, tag = "1")]
    pub endpoint: ::prost::alloc::string::String,
    /// S3 region can be left empty for a GCS sink worker
    #[prost(string, tag = "2")]
    pub region: ::prost::alloc::string::String,
    #[prost(string, tag = "3")]
    pub credentials_dependency: ::prost::alloc::string::String,
    #[prost(message, repeated, tag = "4")]
    pub objects: ::prost::alloc::vec::Vec<S3Object>,
    #[prost(enumeration = "S3Provider", tag = "5")]
    pub s3_provider: i32,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct S3Object {
    #[prost(string, tag = "1")]
    pub dependency: ::prost::alloc::string::String,
    #[prost(oneof = "s3_object::Format", tags = "2, 3")]
    pub format: ::core::option::Option<s3_object::Format>,
}
/// Nested message and enum types in `S3Object`.
pub mod s3_object {
    #[allow(clippy::derive_partial_eq_without_eq)]
    #[derive(Clone, PartialEq, ::prost::Oneof)]
    pub enum Format {
        #[prost(message, tag = "2")]
        Zip(super::ZipObject),
        #[prost(message, tag = "3")]
        Raw(super::RawObject),
    }
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct RawObject {
    #[prost(string, tag = "1")]
    pub key: ::prost::alloc::string::String,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct ZipObject {
    #[prost(oneof = "zip_object::Kind", tags = "1, 2")]
    pub kind: ::core::option::Option<zip_object::Kind>,
}
/// Nested message and enum types in `ZipObject`.
pub mod zip_object {
    #[allow(clippy::derive_partial_eq_without_eq)]
    #[derive(Clone, PartialEq, ::prost::Oneof)]
    pub enum Kind {
        #[prost(message, tag = "1")]
        SingleFile(super::SingleFile),
        #[prost(message, tag = "2")]
        FullContent(super::FullContent),
    }
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct SingleFile {
    #[prost(string, tag = "1")]
    pub key: ::prost::alloc::string::String,
    #[prost(string, tag = "2")]
    pub path: ::prost::alloc::string::String,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct FullContent {}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct S3Credentials {
    #[prost(string, tag = "1")]
    pub access_key: ::prost::alloc::string::String,
    #[prost(string, tag = "2")]
    pub secret_key: ::prost::alloc::string::String,
}
#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash, PartialOrd, Ord, ::prost::Enumeration)]
#[repr(i32)]
pub enum S3Provider {
    Aws = 0,
    Gcs = 1,
}
impl S3Provider {
    /// String value of the enum field names used in the ProtoBuf definition.
    ///
    /// The values are not transformed in any way and thus are considered stable
    /// (if the ProtoBuf definition does not change) and safe for programmatic use.
    pub fn as_str_name(&self) -> &'static str {
        match self {
            S3Provider::Aws => "AWS",
            S3Provider::Gcs => "GCS",
        }
    }
    /// Creates an enum from field names used in the ProtoBuf definition.
    pub fn from_str_name(value: &str) -> ::core::option::Option<Self> {
        match value {
            "AWS" => Some(Self::Aws),
            "GCS" => Some(Self::Gcs),
            _ => None,
        }
    }
}
