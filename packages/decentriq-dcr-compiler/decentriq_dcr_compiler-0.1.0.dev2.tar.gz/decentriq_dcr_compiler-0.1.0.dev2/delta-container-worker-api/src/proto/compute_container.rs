#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct ContainerWorkerConfiguration {
    #[prost(oneof = "container_worker_configuration::Configuration", tags = "1")]
    pub configuration: ::core::option::Option<
        container_worker_configuration::Configuration,
    >,
}
/// Nested message and enum types in `ContainerWorkerConfiguration`.
pub mod container_worker_configuration {
    #[allow(clippy::derive_partial_eq_without_eq)]
    #[derive(Clone, PartialEq, ::prost::Oneof)]
    pub enum Configuration {
        #[prost(message, tag = "1")]
        Static(super::StaticImage),
    }
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct StaticImage {
    #[prost(string, repeated, tag = "1")]
    pub command: ::prost::alloc::vec::Vec<::prost::alloc::string::String>,
    #[prost(message, repeated, tag = "2")]
    pub mount_points: ::prost::alloc::vec::Vec<MountPoint>,
    #[prost(string, tag = "3")]
    pub output_path: ::prost::alloc::string::String,
    #[prost(bool, tag = "4")]
    pub include_container_logs_on_error: bool,
    #[prost(bool, tag = "5")]
    pub include_container_logs_on_success: bool,
    /// When executing a computation, the available VM memory is split into two:
    /// 1. One part given to the in-memory chunk cache (this is backing the /input and /output filesystems, analogous to
    ///      the kernel's pagecache).
    /// 2. The second part is given to the container itself.
    /// The sizes are controlled by minimumContainerMemorySize and extraChunkCacheSizeToAvailableMemoryRatio.
    /// First minimumContainerMemorySize and a hardcoded minimum chunk cache size is subtracted from the available memory,
    /// then the rest is split according to extraChunkCacheSizeToAvailableMemoryRatio.
    /// For example, given a 64G VM with 62G available memory for compute:
    /// * minimumContainerMemorySize by default is 2G
    /// * minimum chunk cache size is 256M
    /// * extraChunkCacheSizeToAvailableMemoryRatio by default is 0.0625
    /// * therefore 0.0625 * (62G - 2G - 256M) =~ 3730M further memory is given to the chunk cache
    /// * so we end up with chunk_cache_size ~= 4G, container_memory ~=58G
    /// Generally speaking the split should be determined by the computation itself:
    /// * Example SQLite: SQLite is memory-bound generally speaking and does a lot of back-and-forth between its
    ///      in-memory cache and the db file. This means that high extraChunkCacheSizeToAvailableMemoryRatio(1.0) and low
    ///      minimumContainerMemorySize should be used because this will speed up the file backing, and SQLite doesn't use
    ///      the extra container memory efficiently.
    /// * Example CHUV pipeline: this computation accesses sparse static input genome data in a fairly random manner,
    ///      meaning that the best course of action is to read all data into memory first instead of relying on the chunk
    ///      cache backed filesystem. This means low extraChunkCacheSizeToAvailableMemoryRatio(1.0) should be used.
    ///      A setting of 1.0 means that all available extra memory (aside from the minimum chunk cache size) will be
    ///      given to the container.
    /// * Example default settings: by default most but not all of the memory is given to the container, assuming that
    ///      most applications tend to read the input files into memory as a first step instead of streaming through.
    ///
    /// default 2G
    #[prost(uint64, optional, tag = "6")]
    pub minimum_container_memory_size: ::core::option::Option<u64>,
    /// default 0.0625
    #[prost(float, optional, tag = "7")]
    pub extra_chunk_cache_size_to_available_memory_ratio: ::core::option::Option<f32>,
}
/// Dependencies are mounted under the `/input` directory
/// For example for a mount point entry { path: "/data", dependency: "dep" }
/// the worker will mount the dependency `dep` at path `/input/data`
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct MountPoint {
    #[prost(string, tag = "1")]
    pub path: ::prost::alloc::string::String,
    #[prost(string, tag = "2")]
    pub dependency: ::prost::alloc::string::String,
}
