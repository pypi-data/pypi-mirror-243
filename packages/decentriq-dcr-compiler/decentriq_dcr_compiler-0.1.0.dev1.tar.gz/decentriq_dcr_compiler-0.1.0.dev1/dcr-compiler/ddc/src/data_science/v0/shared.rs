use std::collections::HashMap;

use crate::data_science::shared::EnclaveSpecificationContext;
use crate::data_science::shared::Node;
use crate::data_science::shared::Participant;

#[derive(Debug, Clone)]
pub struct DataRoomCompileContextV0 {
}

#[derive(Debug, Clone)]
pub struct CommitCompileContextV0 {
    pub nodes_map: HashMap<String, Node>,
    pub enclave_specifications_map: HashMap<String, EnclaveSpecificationContext>,
    pub participants: Vec<Participant>,
    pub enable_development: bool,
    pub enable_interactivity: bool,
}