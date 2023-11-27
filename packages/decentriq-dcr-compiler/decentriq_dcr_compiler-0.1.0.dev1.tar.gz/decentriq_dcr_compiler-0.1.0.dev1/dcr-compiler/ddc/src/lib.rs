#![feature(associated_type_defaults)]
#![feature(map_try_insert)]
use std::collections::hash_map::DefaultHasher;
use std::collections::HashMap;
use std::collections::HashSet;
use std::hash::BuildHasherDefault;

use error::*;

pub mod data_lab;
pub mod data_science;
pub mod error;
pub mod feature;
pub mod lookalike_media;
pub mod media;
pub mod validation;

pub type Map<K, V> = HashMap<K, V, BuildHasherDefault<DefaultHasher>>;
pub type Set<K> = HashSet<K, BuildHasherDefault<DefaultHasher>>;

pub trait Compile {
    type LowLevelOutput;
    type HighLevelOutput;
    type CompileContext;
    type OutputContext;

    type CompileOutput = (Self::LowLevelOutput, Self::HighLevelOutput, Self::OutputContext);

    fn compile(self, context: Self::CompileContext) -> Result<Self::CompileOutput, CompileError>;
    fn verify(
        low_level_output: Self::LowLevelOutput,
        high_level_output: Self::HighLevelOutput,
        compile_context: Self::CompileContext,
    ) -> Result<Self, VerificationError>
    where
        Self: Sized;
}
