#[derive(::serde::Deserialize, ::serde::Serialize)]
#[derive(Eq, Hash)]
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct Fatquote {
    #[prost(oneof = "fatquote::Fatquote", tags = "1, 2, 3, 4")]
    pub fatquote: ::core::option::Option<fatquote::Fatquote>,
}
/// Nested message and enum types in `Fatquote`.
pub mod fatquote {
    #[derive(::serde::Deserialize, ::serde::Serialize)]
    #[derive(Eq, Hash)]
    #[allow(clippy::derive_partial_eq_without_eq)]
    #[derive(Clone, PartialEq, ::prost::Oneof)]
    pub enum Fatquote {
        #[prost(message, tag = "1")]
        Epid(super::FatquoteEpid),
        #[prost(message, tag = "2")]
        Dcap(super::FatquoteDcap),
        #[prost(message, tag = "3")]
        Nitro(super::FatquoteNitro),
        #[prost(message, tag = "4")]
        Snp(super::FatquoteSnp),
    }
}
#[derive(::serde::Deserialize, ::serde::Serialize)]
#[derive(Eq, Hash)]
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct FatquoteEpid {
    #[prost(bytes = "vec", tag = "1")]
    pub ias_response_body: ::prost::alloc::vec::Vec<u8>,
    #[prost(bytes = "vec", tag = "2")]
    pub ias_certificate: ::prost::alloc::vec::Vec<u8>,
    #[prost(bytes = "vec", tag = "3")]
    pub ias_signature: ::prost::alloc::vec::Vec<u8>,
    #[prost(bytes = "vec", tag = "4")]
    pub ias_root_ca_der: ::prost::alloc::vec::Vec<u8>,
}
#[derive(::serde::Deserialize, ::serde::Serialize)]
#[derive(Eq, Hash)]
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct FatquoteDcap {
    #[prost(bytes = "vec", tag = "1")]
    pub dcap_quote: ::prost::alloc::vec::Vec<u8>,
    #[prost(bytes = "vec", tag = "2")]
    pub tcb_info: ::prost::alloc::vec::Vec<u8>,
    #[prost(bytes = "vec", tag = "3")]
    pub qe_identity: ::prost::alloc::vec::Vec<u8>,
    #[prost(bytes = "vec", tag = "4")]
    pub tcb_sign_cert: ::prost::alloc::vec::Vec<u8>,
    #[prost(bytes = "vec", tag = "5")]
    pub qe_sign_cert: ::prost::alloc::vec::Vec<u8>,
    #[prost(bytes = "vec", tag = "6")]
    pub dcap_root_ca_der: ::prost::alloc::vec::Vec<u8>,
}
#[derive(::serde::Deserialize, ::serde::Serialize)]
#[derive(Eq, Hash)]
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct FatquoteNitro {
    #[prost(bytes = "vec", tag = "1")]
    pub cose: ::prost::alloc::vec::Vec<u8>,
    #[prost(bytes = "vec", tag = "2")]
    pub nitro_root_ca_der: ::prost::alloc::vec::Vec<u8>,
}
#[derive(::serde::Deserialize, ::serde::Serialize)]
#[derive(Eq, Hash)]
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct FatquoteSnp {
    #[prost(bytes = "vec", tag = "1")]
    pub report_bin: ::prost::alloc::vec::Vec<u8>,
    #[prost(bytes = "vec", tag = "2")]
    pub amd_ark_der: ::prost::alloc::vec::Vec<u8>,
    #[prost(bytes = "vec", tag = "3")]
    pub amd_sev_der: ::prost::alloc::vec::Vec<u8>,
    #[prost(bytes = "vec", tag = "4")]
    pub vcek_crt_der: ::prost::alloc::vec::Vec<u8>,
    #[prost(bytes = "vec", tag = "5")]
    pub report_data: ::prost::alloc::vec::Vec<u8>,
    #[prost(bytes = "vec", tag = "6")]
    pub roughtime_pub_key: ::prost::alloc::vec::Vec<u8>,
    #[prost(bytes = "vec", tag = "7")]
    pub roughtime_nonce: ::prost::alloc::vec::Vec<u8>,
    #[prost(bytes = "vec", tag = "8")]
    pub signed_timestamp: ::prost::alloc::vec::Vec<u8>,
    #[prost(bytes = "vec", tag = "9")]
    pub decentriq_der: ::prost::alloc::vec::Vec<u8>,
    #[prost(bytes = "vec", tag = "10")]
    pub chip_der: ::prost::alloc::vec::Vec<u8>,
}
#[derive(::serde::Deserialize, ::serde::Serialize)]
#[derive(Eq, Hash)]
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct AttestationSpecification {
    #[prost(
        oneof = "attestation_specification::AttestationSpecification",
        tags = "1, 2, 3, 4"
    )]
    pub attestation_specification: ::core::option::Option<
        attestation_specification::AttestationSpecification,
    >,
}
/// Nested message and enum types in `AttestationSpecification`.
pub mod attestation_specification {
    #[derive(::serde::Deserialize, ::serde::Serialize)]
    #[derive(Eq, Hash)]
    #[allow(clippy::derive_partial_eq_without_eq)]
    #[derive(Clone, PartialEq, ::prost::Oneof)]
    pub enum AttestationSpecification {
        #[prost(message, tag = "1")]
        IntelEpid(super::AttestationSpecificationIntelEpid),
        #[prost(message, tag = "2")]
        IntelDcap(super::AttestationSpecificationIntelDcap),
        #[prost(message, tag = "3")]
        AwsNitro(super::AttestationSpecificationAwsNitro),
        #[prost(message, tag = "4")]
        AmdSnp(super::AttestationSpecificationAmdSnp),
    }
}
#[derive(::serde::Deserialize, ::serde::Serialize)]
#[derive(Eq, Hash)]
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct AttestationSpecificationIntelEpid {
    #[prost(bytes = "vec", tag = "1")]
    pub mrenclave: ::prost::alloc::vec::Vec<u8>,
    #[prost(bytes = "vec", tag = "2")]
    pub ias_root_ca_der: ::prost::alloc::vec::Vec<u8>,
    #[prost(bool, tag = "3")]
    pub accept_debug: bool,
    #[prost(bool, tag = "4")]
    pub accept_group_out_of_date: bool,
    #[prost(bool, tag = "5")]
    pub accept_configuration_needed: bool,
}
#[derive(::serde::Deserialize, ::serde::Serialize)]
#[derive(Eq, Hash)]
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct AttestationSpecificationIntelDcap {
    #[prost(bytes = "vec", tag = "1")]
    pub mrenclave: ::prost::alloc::vec::Vec<u8>,
    #[prost(bytes = "vec", tag = "2")]
    pub dcap_root_ca_der: ::prost::alloc::vec::Vec<u8>,
    #[prost(bool, tag = "3")]
    pub accept_debug: bool,
    #[prost(bool, tag = "4")]
    pub accept_out_of_date: bool,
    #[prost(bool, tag = "5")]
    pub accept_configuration_needed: bool,
    #[prost(bool, tag = "6")]
    pub accept_revoked: bool,
}
#[derive(::serde::Deserialize, ::serde::Serialize)]
#[derive(Eq, Hash)]
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct AttestationSpecificationAwsNitro {
    #[prost(bytes = "vec", tag = "1")]
    pub nitro_root_ca_der: ::prost::alloc::vec::Vec<u8>,
    #[prost(bytes = "vec", tag = "2")]
    pub pcr0: ::prost::alloc::vec::Vec<u8>,
    #[prost(bytes = "vec", tag = "3")]
    pub pcr1: ::prost::alloc::vec::Vec<u8>,
    #[prost(bytes = "vec", tag = "4")]
    pub pcr2: ::prost::alloc::vec::Vec<u8>,
    #[prost(bytes = "vec", tag = "5")]
    pub pcr8: ::prost::alloc::vec::Vec<u8>,
}
#[derive(::serde::Deserialize, ::serde::Serialize)]
#[derive(Eq, Hash)]
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct AttestationSpecificationAmdSnp {
    #[prost(bytes = "vec", tag = "1")]
    pub amd_ark_der: ::prost::alloc::vec::Vec<u8>,
    #[prost(bytes = "vec", tag = "2")]
    pub measurement: ::prost::alloc::vec::Vec<u8>,
    #[prost(bytes = "vec", tag = "3")]
    pub roughtime_pub_key: ::prost::alloc::vec::Vec<u8>,
    #[prost(bytes = "vec", repeated, tag = "4")]
    pub authorized_chip_ids: ::prost::alloc::vec::Vec<::prost::alloc::vec::Vec<u8>>,
    #[prost(bytes = "vec", tag = "5")]
    pub decentriq_der: ::prost::alloc::vec::Vec<u8>,
}
