#[derive(Clone, PartialEq, ::prost::Message)]
pub struct S3SinkWorkerConfiguration {
    #[prost(string, tag="1")]
    pub endpoint: ::prost::alloc::string::String,
    #[prost(string, tag="2")]
    pub region: ::prost::alloc::string::String,
    #[prost(string, tag="3")]
    pub credentials_dependency: ::prost::alloc::string::String,
    #[prost(message, repeated, tag="4")]
    pub objects: ::prost::alloc::vec::Vec<S3Object>,
}
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct S3Object {
    #[prost(string, tag="1")]
    pub dependency: ::prost::alloc::string::String,
    #[prost(oneof="s3_object::Format", tags="2, 3")]
    pub format: ::core::option::Option<s3_object::Format>,
}
/// Nested message and enum types in `S3Object`.
pub mod s3_object {
    #[derive(Clone, PartialEq, ::prost::Oneof)]
    pub enum Format {
        #[prost(message, tag="2")]
        Zip(super::ZipObject),
        #[prost(message, tag="3")]
        Raw(super::RawObject),
    }
}
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct RawObject {
    #[prost(string, tag="1")]
    pub key: ::prost::alloc::string::String,
}
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct ZipObject {
    #[prost(oneof="zip_object::Kind", tags="1, 2")]
    pub kind: ::core::option::Option<zip_object::Kind>,
}
/// Nested message and enum types in `ZipObject`.
pub mod zip_object {
    #[derive(Clone, PartialEq, ::prost::Oneof)]
    pub enum Kind {
        #[prost(message, tag="1")]
        SingleFile(super::SingleFile),
        #[prost(message, tag="2")]
        FullContent(super::FullContent),
    }
}
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct SingleFile {
    #[prost(string, tag="1")]
    pub key: ::prost::alloc::string::String,
    #[prost(string, tag="2")]
    pub path: ::prost::alloc::string::String,
}
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct FullContent {
}
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct S3Credentials {
    #[prost(string, tag="1")]
    pub access_key: ::prost::alloc::string::String,
    #[prost(string, tag="2")]
    pub secret_key: ::prost::alloc::string::String,
}
