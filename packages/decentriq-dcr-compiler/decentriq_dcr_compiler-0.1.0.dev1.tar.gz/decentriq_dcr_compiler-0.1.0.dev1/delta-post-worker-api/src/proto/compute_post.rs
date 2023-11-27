#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct PostWorkerConfiguration {
    #[prost(bool, tag = "1")]
    pub use_mock_backend: bool,
}
