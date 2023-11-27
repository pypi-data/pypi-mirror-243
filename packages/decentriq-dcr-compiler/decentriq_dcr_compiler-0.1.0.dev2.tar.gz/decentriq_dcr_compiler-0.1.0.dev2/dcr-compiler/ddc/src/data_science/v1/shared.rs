use std::collections::HashMap;

use delta_data_room_api::ConfigurationCommit;
use prost::Message;
use sha2::Digest;

use crate::data_science::shared::DataScienceCommitMergeMetadata;
use crate::data_science::shared::EnclaveSpecificationContext;
use crate::data_science::shared::Node;
use crate::data_science::shared::Participant;
use crate::error::CompileError;

use super::DataScienceCommitV1;

pub fn generate_history_pin<'a>(
    data_room_id: &[u8],
    commits: impl IntoIterator<Item = &'a ConfigurationCommit>,
) -> [u8; 32] {
    let mut hasher = sha2::Sha256::new();
    hasher.update(data_room_id);
    for commit in commits.into_iter() {
        hasher.update(sha2::Sha256::digest(&commit.encode_to_vec()));
    }
    hasher.finalize().into()
}

#[derive(Debug, Clone)]
pub struct CommitCompileContextV1 {
    pub nodes_map: HashMap<String, Node>,
    pub enclave_specifications_map: HashMap<String, EnclaveSpecificationContext>,
    pub participants: Vec<Participant>,
    pub enable_development: bool,
    pub enable_interactivity: bool,
    pub initial_participants: HashMap<String, Participant>,
    pub previous_commits: Vec<(
        DataScienceCommitV1,
        ConfigurationCommit,
        DataScienceCommitMergeMetadata,
    )>,
}
impl CommitCompileContextV1 {
    pub(crate) fn initial_pin(&self, data_room_id: &[u8]) -> [u8; 32] {
        generate_history_pin(data_room_id, std::iter::empty())
    }

    pub (crate) fn all_pins(&self, data_room_id: &[u8]) -> Vec<[u8; 32]> {
        let mut pins = vec![self.initial_pin(data_room_id)];
        for (_, _, metadata) in self.previous_commits.iter() {
            pins.push(metadata.history_pin_at_commit);
        }
        pins
    }

    fn participant_history_by_pin(&self, data_room_id: &[u8]) -> impl Iterator<Item = ([u8; 32], &HashMap<String, Participant>)> {
        std::iter::once((self.initial_pin(data_room_id), &self.initial_participants))
            .chain(self
                    .previous_commits
                    .iter()
                    .map(|(_, _, metadata)|
                        (metadata.history_pin_at_commit.clone(), &metadata.participants))
            )
    }

    pub(crate) fn participant_at_history_pin(
        &self,
        data_room_id: &[u8],
        history_pin: &[u8],
        user: &str
    ) -> Result<Option<&Participant>, CompileError> {
        let participants_at_history_pin = self.participant_history_by_pin(data_room_id)
            .find_map(|(pin, participants)| if pin.as_slice() == history_pin {
                Some(participants)
            } else {
                None
            }).ok_or("History pin does not refer to an existing history")?;
        Ok(participants_at_history_pin.get(user))
    }
}