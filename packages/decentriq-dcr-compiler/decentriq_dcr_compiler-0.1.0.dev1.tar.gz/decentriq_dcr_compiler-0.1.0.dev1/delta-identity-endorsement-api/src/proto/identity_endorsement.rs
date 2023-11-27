#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct EndorsementRequest {
    #[prost(oneof = "endorsement_request::EndorsementRequest", tags = "2, 3")]
    pub endorsement_request: ::core::option::Option<
        endorsement_request::EndorsementRequest,
    >,
}
/// Nested message and enum types in `EndorsementRequest`.
pub mod endorsement_request {
    #[allow(clippy::derive_partial_eq_without_eq)]
    #[derive(Clone, PartialEq, ::prost::Oneof)]
    pub enum EndorsementRequest {
        #[prost(message, tag = "2")]
        PkiEndorsementRequest(super::PkiEndorsementRequest),
        #[prost(message, tag = "3")]
        DcrSecretEndorsementRequest(super::DcrSecretEndorsementRequest),
    }
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct EndorsementResponse {
    #[prost(oneof = "endorsement_response::EndorsementResponse", tags = "2, 3")]
    pub endorsement_response: ::core::option::Option<
        endorsement_response::EndorsementResponse,
    >,
}
/// Nested message and enum types in `EndorsementResponse`.
pub mod endorsement_response {
    #[allow(clippy::derive_partial_eq_without_eq)]
    #[derive(Clone, PartialEq, ::prost::Oneof)]
    pub enum EndorsementResponse {
        #[prost(message, tag = "2")]
        PkiEndorsementResponse(super::PkiEndorsementResponse),
        #[prost(message, tag = "3")]
        DcrSecretEndorsementResponse(super::DcrSecretEndorsementResponse),
    }
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct PkiEndorsementRequest {
    #[prost(bytes = "vec", tag = "1")]
    pub certificate_chain_pem: ::prost::alloc::vec::Vec<u8>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct PkiEndorsementResponse {
    #[prost(message, optional, tag = "1")]
    pub pki_endorsement: ::core::option::Option<EnclaveEndorsement>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct DcrSecretEndorsementRequest {
    #[prost(string, tag = "1")]
    pub dcr_secret: ::prost::alloc::string::String,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct DcrSecretEndorsementResponse {
    #[prost(message, optional, tag = "1")]
    pub dcr_secret_endorsement: ::core::option::Option<EnclaveEndorsement>,
    #[prost(bytes = "vec", tag = "2")]
    pub dcr_secret_id: ::prost::alloc::vec::Vec<u8>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct EnclaveEndorsements {
    #[prost(message, optional, tag = "1")]
    pub personal_pki: ::core::option::Option<EnclaveEndorsement>,
    #[prost(message, optional, tag = "2")]
    pub dq_pki: ::core::option::Option<EnclaveEndorsement>,
    #[prost(message, optional, tag = "3")]
    pub dcr_secret: ::core::option::Option<EnclaveEndorsement>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct EnclaveEndorsement {
    #[prost(bytes = "vec", tag = "1")]
    pub endorsement_certificate_der: ::prost::alloc::vec::Vec<u8>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct PkiClaim {
    #[prost(bytes = "vec", tag = "1")]
    pub root_certificate_der: ::prost::alloc::vec::Vec<u8>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct DcrSecretClaim {
    #[prost(bytes = "vec", tag = "1")]
    pub dcr_secret_id: ::prost::alloc::vec::Vec<u8>,
}
