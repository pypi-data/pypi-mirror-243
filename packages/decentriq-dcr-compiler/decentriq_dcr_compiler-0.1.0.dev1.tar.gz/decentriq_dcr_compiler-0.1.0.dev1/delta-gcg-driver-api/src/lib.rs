mod proto;

use delta_identity_endorsement_api::endorsement_response;
use delta_identity_endorsement_api::EndorsementResponse;
pub use prost;
pub use proto::*;

impl From<endorsement_response::EndorsementResponse> for gcg_response::GcgResponse {
    fn from(endorsement_response: endorsement_response::EndorsementResponse) -> Self {
        gcg_response::GcgResponse::EndorsementResponse(EndorsementResponse {
            endorsement_response: Some(endorsement_response),
        })
    }
}
