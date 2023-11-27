use delta_attestation_api::*;
use delta_data_room_api::DataRoom;
use delta_gcg_driver_api::*;
use schemars::JsonSchema;
use serde::Deserialize;
use serde::Serialize;

use super::v0;
use super::v1;
use super::v2;
use super::v3;
use crate::CompileError;
use crate::CompileResult;

/// NB: Version compatibility
///
/// The Media translation logic has two layers:
/// 1. Actions (MediaRequests)
/// 2. Data (DataRoom definition, Auxiliary state definition)
///
/// In terms of compatibility, it is only 2. that needs to be versioned. The API of 1. is "HEAD",
/// and the action translation logic should take care of version compatibility of the underlying
/// stored data, and expose a unified interface through actions.
///
/// This means that there is no v0/v1 separation for top-level Actions (versioning of them are
/// implicit in the versioning of the translation WASM blobs), only for the DCR definition and the
/// auxiliary state defninition, which is found in the v0/v1 etc. folders.
#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub enum MediaDataRoom {
    V0(v0::MediaDataRoomV0),
    V1(v1::MediaDataRoomV1),
    V2(v2::MediaDataRoomV2),
    V3(v3::MediaDataRoomV3),
}

pub type MediaDataRoomLatest = v3::MediaDataRoomV3;

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[schemars(deny_unknown_fields)]
#[serde(rename_all = "camelCase")]
pub enum MediaAuxiliaryState {
    V0(v0::MediaAuxiliaryStateV0),
    V1(v1::MediaAuxiliaryStateV1),
    V2(v2::MediaAuxiliaryStateV2),
    V3(v3::MediaAuxiliaryStateV3),
}

pub type MediaAuxiliaryStateLatest = v2::MediaAuxiliaryStateV2;

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[schemars(deny_unknown_fields)]
#[serde(rename_all = "camelCase")]
pub enum DirectActivationConfig {
    V0(v0::DirectActivationConfigV0),
    V1(v2::DirectActivationConfigV2),
}

pub type DirectActivationConfigLatest = v1::DirectActivationConfigV1;

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[schemars(deny_unknown_fields)]
#[serde(rename_all = "camelCase")]
pub struct ActivatedAudiencePayload {
    pub audience_type: String,
    pub reach: f32,
}

/// MediaRequest -> GcgRequest
#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[schemars(deny_unknown_fields)]
#[serde(rename_all = "camelCase")]
pub enum MediaRequest {
    #[serde(rename_all = "camelCase")]
    PublishDataRoom {
        data_room: MediaDataRoom,
        show_organization_logo: bool,
        require_password: bool,
    },
    #[serde(rename_all = "camelCase")]
    RetrieveDataRoom { data_room_id_hex: String },
    #[serde(rename_all = "camelCase")]
    PublishAdvertiserDataset {
        data_room_id_hex: String,
        dataset_hash_hex: String,
        encryption_key_hex: String,
        scope_id_hex: String,
    },
    #[serde(rename_all = "camelCase")]
    PublishPublisherDataset {
        data_room_id_hex: String,
        dataset_hash_hex: String,
        encryption_key_hex: String,
        scope_id_hex: String,
    },
    #[serde(rename_all = "camelCase")]
    UnpublishAdvertiserDataset { data_room_id_hex: String },
    #[serde(rename_all = "camelCase")]
    UnpublishPublisherDataset { data_room_id_hex: String },
    #[serde(rename_all = "camelCase")]
    RetrievePublishedDatasets { data_room_id_hex: String },
    #[serde(rename_all = "camelCase")]
    CalculateOverlapBasic {
        data_room_id_hex: String,
        scope_id_hex: String,
    },
    #[serde(rename_all = "camelCase")]
    RetrieveAuxiliaryState { data_room_id_hex: String },
    #[serde(rename_all = "camelCase")]
    UpdateAuxiliaryState {
        data_room_id_hex: String,
        index: u64,
        state: Option<MediaAuxiliaryState>,
    },

    // Consentless
    #[serde(rename_all = "camelCase")]
    CalculateOverlapInsights {
        data_room_id_hex: String,
        scope_id_hex: String,
        audience_types: Vec<String>,
    },

    // Media DCR V2
    #[serde(rename_all = "camelCase")]
    PublishDemographicsDataset {
        data_room_id_hex: String,
        dataset_hash_hex: String,
        encryption_key_hex: String,
        scope_id_hex: String,
    },
    #[serde(rename_all = "camelCase")]
    UnpublishDemographicsDataset { data_room_id_hex: String },
    #[serde(rename_all = "camelCase")]
    PublishSegmentsDataset {
        data_room_id_hex: String,
        dataset_hash_hex: String,
        encryption_key_hex: String,
        scope_id_hex: String,
    },
    #[serde(rename_all = "camelCase")]
    UnpublishSegmentsDataset { data_room_id_hex: String },
    #[serde(rename_all = "camelCase")]
    PublishEmbeddingsDataset {
        data_room_id_hex: String,
        dataset_hash_hex: String,
        encryption_key_hex: String,
        scope_id_hex: String,
    },
    #[serde(rename_all = "camelCase")]
    UnpublishEmbeddingsDataset { data_room_id_hex: String },
    #[serde(rename_all = "camelCase")]
    PublishActivatedAudiencesConfig {
        data_room_id_hex: String,
        dataset_hash_hex: String,
        encryption_key_hex: String,
        scope_id_hex: String,
    },
    #[serde(rename_all = "camelCase")]
    UnpublishActivatedAudiencesConfig { data_room_id_hex: String },
    #[serde(rename_all = "camelCase")]
    CalculateModelledAudienceInsights {
        data_room_id_hex: String,
        scope_id_hex: String,
    },
    #[serde(rename_all = "camelCase")]
    CalculateModelledAudienceInsightsView {
        data_room_id_hex: String,
        scope_id_hex: String,
    },
    #[serde(rename_all = "camelCase")]
    GetLookalikeAudience {
        data_room_id_hex: String,
        scope_id_hex: String,
        activated_audience: ActivatedAudiencePayload,
    },
    #[serde(rename_all = "camelCase")]
    ViewPublishedActivatedAudiences {
        data_room_id_hex: String,
        scope_id_hex: String,
    },
    #[serde(rename_all = "camelCase")]
    ViewActivatedAudiences {
        data_room_id_hex: String,
        scope_id_hex: String,
    },

    // Direct
    #[serde(rename_all = "camelCase")]
    PublishDirectActivationConfig {
        data_room_id_hex: String,
        dataset_hash_hex: String,
        encryption_key_hex: String,
        scope_id_hex: String,
    },
    #[serde(rename_all = "camelCase")]
    UnpublishDirectActivationConfig { data_room_id_hex: String },
    #[serde(rename_all = "camelCase")]
    SubmitRetrieveDirectActivationConfig {
        data_room_id_hex: String,
        scope_id_hex: String,
    },
    #[serde(rename_all = "camelCase")]
    CalculateDirectActivation {
        data_room_id_hex: String,
        scope_id_hex: String,
    },
}

/// GcgResponse -> MediaResponse
#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[schemars(deny_unknown_fields)]
#[serde(rename_all = "camelCase")]
pub enum MediaResponse {
    #[serde(rename_all = "camelCase")]
    PublishDataRoom { data_room_id: String },
    #[serde(rename_all = "camelCase")]
    RetrieveDataRoom { data_room: MediaDataRoom },
    #[serde(rename_all = "camelCase")]
    PublishAdvertiserDataset {},
    #[serde(rename_all = "camelCase")]
    PublishPublisherDataset {},
    #[serde(rename_all = "camelCase")]
    PublishDemographicsDataset {},
    #[serde(rename_all = "camelCase")]
    PublishSegmentsDataset {},
    #[serde(rename_all = "camelCase")]
    PublishEmbeddingsDataset {},
    #[serde(rename_all = "camelCase")]
    UnpublishAdvertiserDataset {},
    #[serde(rename_all = "camelCase")]
    UnpublishPublisherDataset {},
    #[serde(rename_all = "camelCase")]
    UnpublishDemographicsDataset {},
    #[serde(rename_all = "camelCase")]
    UnpublishSegmentsDataset {},
    #[serde(rename_all = "camelCase")]
    UnpublishEmbeddingsDataset {},
    #[serde(rename_all = "camelCase")]
    RetrievePublishedDatasets {
        advertiser_dataset_hash_hex: Option<String>,
        publisher_dataset_hash_hex: Option<String>,
        demographics_dataset_hash_hex: Option<String>,
        segments_dataset_hash_hex: Option<String>,
        embeddings_dataset_hash_hex: Option<String>,
    },
    #[serde(rename_all = "camelCase")]
    CalculateOverlapBasic {
        compute_node_name: String,
        job_id_hex: String,
    },
    #[serde(rename_all = "camelCase")]
    CalculateOverlapInsights {
        compute_node_name: String,
        job_id_hex: String,
    },
    #[serde(rename_all = "camelCase")]
    PublishActivatedAudiencesConfig {},
    #[serde(rename_all = "camelCase")]
    UnpublishActivatedAudiencesConfig {},
    #[serde(rename_all = "camelCase")]
    GetLookalikeAudience {
        compute_node_name: String,
        job_id_hex: String,
    },
    #[serde(rename_all = "camelCase")]
    CalculateModelledAudienceInsights {
        compute_node_name: String,
        job_id_hex: String,
    },
    #[serde(rename_all = "camelCase")]
    CalculateModelledAudienceInsightsView {
        compute_node_name: String,
        job_id_hex: String,
    },
    #[serde(rename_all = "camelCase")]
    PublishDirectActivationConfig {},
    #[serde(rename_all = "camelCase")]
    UnpublishDirectActivationConfig {},

    ViewPublishedActivatedAudiences {
        compute_node_name: String,
        job_id_hex: String,
    },
    ViewActivatedAudiences {
        compute_node_name: String,
        job_id_hex: String,
    },

    #[serde(rename_all = "camelCase")]
    SubmitRetrieveDirectActivationConfig {
        compute_node_name: String,
        job_id_hex: String,
    },
    #[serde(rename_all = "camelCase")]
    CalculateDirectActivation {
        compute_node_name: String,
        job_id_hex: String,
    },

    #[serde(rename_all = "camelCase")]
    RetrieveAuxiliaryState {
        state: Vec<IndexedMediaAuxiliaryState>,
    },

    #[serde(rename_all = "camelCase")]
    UpdateAuxiliaryState {
        success: bool,
        index: u64,
        state: Option<MediaAuxiliaryState>,
    },
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[schemars(deny_unknown_fields)]
#[serde(rename_all = "camelCase")]
pub struct IndexedMediaAuxiliaryState {
    user: String,
    index: u64,
    state: MediaAuxiliaryState,
}

#[derive(Debug, Clone, Serialize, Deserialize, JsonSchema)]
#[schemars(deny_unknown_fields)]
#[serde(rename_all = "camelCase")]
pub struct ConsentlessAudience {
    id: String,
    audience_type: String,
    precision: f64,
    activated: bool,
    downloaded: bool,
}

pub fn compile_media_request_serialized(
    media_request: &str,
    user_auth_serialized: &[u8],
) -> Result<Vec<u8>, CompileError> {
    let media_request: MediaRequest = serde_json::from_str(media_request)?;
    let gcg_request_enum = compile_media_request(&media_request)?;
    let gcg_request = GcgRequest {
        user_auth: Some(prost::Message::decode_length_delimited(
            user_auth_serialized,
        )?),
        gcg_request: Some(gcg_request_enum),
    };
    Ok(prost::Message::encode_length_delimited_to_vec(&gcg_request))
}

pub fn decompile_media_response_serialized(
    media_request: &str,
    gcg_response_serialized: &[u8],
) -> Result<String, CompileError> {
    let media_request: MediaRequest = serde_json::from_str(media_request)?;
    let gcg_response: GcgResponse =
        prost::Message::decode_length_delimited(gcg_response_serialized)?;
    let media_response = decompile_media_response(&media_request, gcg_response)?;
    Ok(serde_json::to_string(&media_response)?)
}

fn compile_media_data_room(data_room: &MediaDataRoom) -> Result<DataRoom, CompileError> {
    match data_room {
        MediaDataRoom::V0(data_room) => v0::compile_media_data_room_v0(data_room),
        MediaDataRoom::V1(data_room) => v1::compile_media_data_room_v1(data_room),
        MediaDataRoom::V2(data_room) => v2::compile_media_data_room_v2(data_room),
        MediaDataRoom::V3(data_room) => v3::compile_media_data_room_v3(data_room),
    }
}

fn compile_media_request(
    media_request: &MediaRequest,
) -> Result<gcg_request::GcgRequest, CompileError> {
    match media_request {
        MediaRequest::PublishDataRoom {
            data_room: media_data_room,
            show_organization_logo,
            require_password,
        } => {
            let low_level_data_room = compile_media_data_room(media_data_room)?;
            let high_level_data_room = serde_json::to_vec(media_data_room)?;
            let metadata = delta_extension_metering_api::DcrMetadata {
                kind: delta_extension_metering_api::CreateDcrKind::Media.into(),
                show_organization_logo: *show_organization_logo,
                require_password: *require_password,
                purpose: delta_extension_metering_api::CreateDcrPurpose::Standard.into(),
            };
            let metadata_serialized = prost::Message::encode_length_delimited_to_vec(&metadata);
            Ok(gcg_request::GcgRequest::CreateDataRoomRequest(
                CreateDataRoomRequest {
                    data_room: Some(low_level_data_room),
                    high_level_representation: Some(high_level_data_room),
                    data_room_metadata: Some(metadata_serialized),
                },
            ))
        }
        MediaRequest::RetrieveDataRoom { data_room_id_hex } => Ok(
            gcg_request::GcgRequest::RetrieveDataRoomRequest(RetrieveDataRoomRequest {
                data_room_id: hex::decode(data_room_id_hex)?,
            }),
        ),
        MediaRequest::PublishAdvertiserDataset {
            data_room_id_hex,
            dataset_hash_hex,
            encryption_key_hex,
            scope_id_hex,
        } => Ok(gcg_request::GcgRequest::PublishDatasetToDataRoomRequest(
            PublishDatasetToDataRoomRequest {
                dataset_hash: hex::decode(dataset_hash_hex)?,
                data_room_id: hex::decode(data_room_id_hex)?,
                leaf_id: "dataset_advertiser".to_string(),
                encryption_key: hex::decode(encryption_key_hex)?,
                scope: hex::decode(scope_id_hex)?,
            },
        )),
        MediaRequest::PublishPublisherDataset {
            data_room_id_hex,
            dataset_hash_hex,
            encryption_key_hex,
            scope_id_hex,
        } => Ok(gcg_request::GcgRequest::PublishDatasetToDataRoomRequest(
            PublishDatasetToDataRoomRequest {
                dataset_hash: hex::decode(dataset_hash_hex)?,
                data_room_id: hex::decode(data_room_id_hex)?,
                leaf_id: "dataset_publisher".to_string(),
                encryption_key: hex::decode(encryption_key_hex)?,
                scope: hex::decode(scope_id_hex)?,
            },
        )),
        MediaRequest::PublishDemographicsDataset {
            data_room_id_hex,
            dataset_hash_hex,
            encryption_key_hex,
            scope_id_hex,
        } => Ok(gcg_request::GcgRequest::PublishDatasetToDataRoomRequest(
            PublishDatasetToDataRoomRequest {
                dataset_hash: hex::decode(dataset_hash_hex)?,
                data_room_id: hex::decode(data_room_id_hex)?,
                leaf_id: "dataset_demographics".to_string(),
                encryption_key: hex::decode(encryption_key_hex)?,
                scope: hex::decode(scope_id_hex)?,
            },
        )),
        MediaRequest::PublishEmbeddingsDataset {
            data_room_id_hex,
            dataset_hash_hex,
            encryption_key_hex,
            scope_id_hex,
        } => Ok(gcg_request::GcgRequest::PublishDatasetToDataRoomRequest(
            PublishDatasetToDataRoomRequest {
                dataset_hash: hex::decode(dataset_hash_hex)?,
                data_room_id: hex::decode(data_room_id_hex)?,
                leaf_id: "dataset_embeddings".to_string(),
                encryption_key: hex::decode(encryption_key_hex)?,
                scope: hex::decode(scope_id_hex)?,
            },
        )),
        MediaRequest::PublishSegmentsDataset {
            data_room_id_hex,
            dataset_hash_hex,
            encryption_key_hex,
            scope_id_hex,
        } => Ok(gcg_request::GcgRequest::PublishDatasetToDataRoomRequest(
            PublishDatasetToDataRoomRequest {
                dataset_hash: hex::decode(dataset_hash_hex)?,
                data_room_id: hex::decode(data_room_id_hex)?,
                leaf_id: "dataset_segments".to_string(),
                encryption_key: hex::decode(encryption_key_hex)?,
                scope: hex::decode(scope_id_hex)?,
            },
        )),
        MediaRequest::RetrievePublishedDatasets { data_room_id_hex } => {
            Ok(gcg_request::GcgRequest::RetrievePublishedDatasetsRequest(
                RetrievePublishedDatasetsRequest {
                    data_room_id: hex::decode(data_room_id_hex)?,
                },
            ))
        }
        MediaRequest::CalculateOverlapBasic {
            data_room_id_hex,
            scope_id_hex,
        } => Ok(gcg_request::GcgRequest::ExecuteComputeRequest(
            ExecuteComputeRequest {
                data_room_id: hex::decode(data_room_id_hex)?,
                compute_node_ids: vec!["overlap_basic".into()],
                is_dry_run: false,
                scope: hex::decode(scope_id_hex)?,
                parameters: Default::default(),
                test_datasets: Default::default(),
            },
        )),
        MediaRequest::CalculateOverlapInsights {
            data_room_id_hex,
            scope_id_hex,
            audience_types,
        } => {
            let calculate_overlap_insights_parameters = v0::CalculateOverlapInsightsParams {
                audience_types: audience_types.clone(),
            };
            Ok(gcg_request::GcgRequest::ExecuteComputeRequest(
                ExecuteComputeRequest {
                    data_room_id: hex::decode(data_room_id_hex)?,
                    compute_node_ids: vec!["consentless_overlap_insights".into()],
                    is_dry_run: false,
                    scope: hex::decode(scope_id_hex)?,
                    parameters: From::from([(
                        "overlap_insights_params".to_string(),
                        serde_json::to_string(&calculate_overlap_insights_parameters)?,
                    )]),
                    test_datasets: Default::default(),
                },
            ))
        }
        MediaRequest::CalculateModelledAudienceInsights {
            data_room_id_hex,
            scope_id_hex,
        } => Ok(gcg_request::GcgRequest::ExecuteComputeRequest(
            ExecuteComputeRequest {
                data_room_id: hex::decode(data_room_id_hex)?,
                compute_node_ids: vec!["modelled_audience_insights".into()],
                is_dry_run: false,
                scope: hex::decode(scope_id_hex)?,
                parameters: Default::default(),
                test_datasets: Default::default(),
            },
        )),
        MediaRequest::CalculateModelledAudienceInsightsView {
            data_room_id_hex,
            scope_id_hex,
        } => Ok(gcg_request::GcgRequest::ExecuteComputeRequest(
            ExecuteComputeRequest {
                data_room_id: hex::decode(data_room_id_hex)?,
                compute_node_ids: vec!["modelled_audience_insights_view".into()],
                is_dry_run: false,
                scope: hex::decode(scope_id_hex)?,
                parameters: Default::default(),
                test_datasets: Default::default(),
            },
        )),
        MediaRequest::ViewPublishedActivatedAudiences {
            data_room_id_hex,
            scope_id_hex,
        } => Ok(gcg_request::GcgRequest::ExecuteComputeRequest(
            ExecuteComputeRequest {
                data_room_id: hex::decode(data_room_id_hex)?,
                compute_node_ids: vec!["view_published_activated_audiences".into()],
                is_dry_run: false,
                scope: hex::decode(scope_id_hex)?,
                parameters: Default::default(),
                test_datasets: Default::default(),
            },
        )),
        MediaRequest::ViewActivatedAudiences {
            data_room_id_hex,
            scope_id_hex,
        } => Ok(gcg_request::GcgRequest::ExecuteComputeRequest(
            ExecuteComputeRequest {
                data_room_id: hex::decode(data_room_id_hex)?,
                compute_node_ids: vec!["view_activated_audiences".into()],
                is_dry_run: false,
                scope: hex::decode(scope_id_hex)?,
                parameters: Default::default(),
                test_datasets: Default::default(),
            },
        )),
        MediaRequest::PublishDirectActivationConfig {
            data_room_id_hex,
            dataset_hash_hex,
            encryption_key_hex,
            scope_id_hex,
        } => Ok(gcg_request::GcgRequest::PublishDatasetToDataRoomRequest(
            PublishDatasetToDataRoomRequest {
                dataset_hash: hex::decode(dataset_hash_hex)?,
                data_room_id: hex::decode(data_room_id_hex)?,
                leaf_id: "direct_activation_config".to_string(),
                encryption_key: hex::decode(encryption_key_hex)?,
                scope: hex::decode(scope_id_hex)?,
            },
        )),
        MediaRequest::PublishActivatedAudiencesConfig {
            data_room_id_hex,
            dataset_hash_hex,
            encryption_key_hex,
            scope_id_hex,
        } => Ok(gcg_request::GcgRequest::PublishDatasetToDataRoomRequest(
            PublishDatasetToDataRoomRequest {
                dataset_hash: hex::decode(dataset_hash_hex)?,
                data_room_id: hex::decode(data_room_id_hex)?,
                leaf_id: "activated_audiences".to_string(),
                encryption_key: hex::decode(encryption_key_hex)?,
                scope: hex::decode(scope_id_hex)?,
            },
        )),
        MediaRequest::SubmitRetrieveDirectActivationConfig {
            data_room_id_hex,
            scope_id_hex,
        } => Ok(gcg_request::GcgRequest::ExecuteComputeRequest(
            ExecuteComputeRequest {
                data_room_id: hex::decode(data_room_id_hex)?,
                compute_node_ids: vec!["direct_activation_config".into()],
                is_dry_run: false,
                scope: hex::decode(scope_id_hex)?,
                parameters: Default::default(),
                test_datasets: Default::default(),
            },
        )),
        MediaRequest::GetLookalikeAudience {
            data_room_id_hex,
            scope_id_hex,
            activated_audience,
        } => Ok(gcg_request::GcgRequest::ExecuteComputeRequest(
            ExecuteComputeRequest {
                data_room_id: hex::decode(data_room_id_hex)?,
                compute_node_ids: vec!["get_lookalike_audience".into()],
                is_dry_run: false,
                scope: hex::decode(scope_id_hex)?,
                parameters: From::from([(
                    "activated_audience".to_string(),
                    serde_json::to_string(&activated_audience)?,
                )]),
                test_datasets: Default::default(),
            },
        )),
        MediaRequest::CalculateDirectActivation {
            data_room_id_hex,
            scope_id_hex,
        } => Ok(gcg_request::GcgRequest::ExecuteComputeRequest(
            ExecuteComputeRequest {
                data_room_id: hex::decode(data_room_id_hex)?,
                compute_node_ids: vec!["direct_activation".into()],
                is_dry_run: false,
                scope: hex::decode(scope_id_hex)?,
                parameters: Default::default(),
                test_datasets: Default::default(),
            },
        )),
        MediaRequest::RetrieveAuxiliaryState {
            data_room_id_hex, ..
        } => Ok(gcg_request::GcgRequest::ReadAuxiliaryStateRequest(
            ReadAuxiliaryStateRequest {
                data_room_id: hex::decode(data_room_id_hex)?,
            },
        )),
        MediaRequest::UpdateAuxiliaryState {
            data_room_id_hex,
            index,
            state,
        } => {
            let value = if let Some(state) = state {
                Some(serde_json::to_vec(state)?)
            } else {
                None
            };
            Ok(gcg_request::GcgRequest::CasAuxiliaryStateRequest(
                CasAuxiliaryStateRequest {
                    data_room_id: hex::decode(data_room_id_hex)?,
                    index: *index,
                    value,
                },
            ))
        }
        MediaRequest::UnpublishActivatedAudiencesConfig { data_room_id_hex } => Ok(
            gcg_request::GcgRequest::RemovePublishedDatasetRequest(RemovePublishedDatasetRequest {
                data_room_id: hex::decode(data_room_id_hex)?,
                leaf_id: "activated_audiences".into(),
            }),
        ),
        MediaRequest::UnpublishAdvertiserDataset { data_room_id_hex } => Ok(
            gcg_request::GcgRequest::RemovePublishedDatasetRequest(RemovePublishedDatasetRequest {
                data_room_id: hex::decode(data_room_id_hex)?,
                leaf_id: "dataset_advertiser".into(),
            }),
        ),
        MediaRequest::UnpublishPublisherDataset { data_room_id_hex } => Ok(
            gcg_request::GcgRequest::RemovePublishedDatasetRequest(RemovePublishedDatasetRequest {
                data_room_id: hex::decode(data_room_id_hex)?,
                leaf_id: "dataset_publisher".into(),
            }),
        ),
        MediaRequest::UnpublishSegmentsDataset { data_room_id_hex } => Ok(
            gcg_request::GcgRequest::RemovePublishedDatasetRequest(RemovePublishedDatasetRequest {
                data_room_id: hex::decode(data_room_id_hex)?,
                leaf_id: "dataset_segments".into(),
            }),
        ),
        MediaRequest::UnpublishDemographicsDataset { data_room_id_hex } => Ok(
            gcg_request::GcgRequest::RemovePublishedDatasetRequest(RemovePublishedDatasetRequest {
                data_room_id: hex::decode(data_room_id_hex)?,
                leaf_id: "dataset_demographics".into(),
            }),
        ),
        MediaRequest::UnpublishEmbeddingsDataset { data_room_id_hex } => Ok(
            gcg_request::GcgRequest::RemovePublishedDatasetRequest(RemovePublishedDatasetRequest {
                data_room_id: hex::decode(data_room_id_hex)?,
                leaf_id: "dataset_embeddings".into(),
            }),
        ),
        MediaRequest::UnpublishDirectActivationConfig { data_room_id_hex } => Ok(
            gcg_request::GcgRequest::RemovePublishedDatasetRequest(RemovePublishedDatasetRequest {
                data_room_id: hex::decode(data_room_id_hex)?,
                leaf_id: "direct_activation_config".into(),
            }),
        ),
    }
}

fn decompile_media_response(
    media_request: &MediaRequest,
    gcg_response: GcgResponse,
) -> Result<MediaResponse, CompileError> {
    let gcg_response = gcg_response.gcg_response.ok_or("gcg_response not set")?;
    match media_request {
        MediaRequest::RetrieveDataRoom { .. } => {
            if let gcg_response::GcgResponse::RetrieveDataRoomResponse(response) = gcg_response {
                let low_level_data_room = response.data_room.as_ref().ok_or("data_room not set")?;
                let high_level_serialized = response.high_level_representation.as_ref().ok_or(
                    "High-level representation not set in DCR, cannot interpret as Media DCR",
                )?;
                let high_level_data_room: MediaDataRoom =
                    serde_json::from_slice(high_level_serialized)?;
                let low_level_data_room_recompiled =
                    compile_media_data_room(&high_level_data_room)?;
                if low_level_data_room != &low_level_data_room_recompiled {
                    return Err(format!("The recompiled Media DCR representation did not reproduce, verification failed\nGot:\n{:#?}\nRecompiled:\n{:#?}", low_level_data_room, low_level_data_room_recompiled))?;
                }
                return Ok(MediaResponse::RetrieveDataRoom {
                    data_room: high_level_data_room,
                });
            }
        }
        MediaRequest::PublishDataRoom { .. } => {
            if let gcg_response::GcgResponse::CreateDataRoomResponse(response) = gcg_response {
                let response = response
                    .create_data_room_response
                    .as_ref()
                    .ok_or("create_data_room_response not set")?;
                match response {
                    create_data_room_response::CreateDataRoomResponse::DataRoomId(id) => {
                        return Ok(MediaResponse::PublishDataRoom {
                            data_room_id: hex::encode(id),
                        });
                    }
                    create_data_room_response::CreateDataRoomResponse::DataRoomValidationError(
                        error,
                    ) => return Err(flatten_validation_error(error))?,
                }
            }
        }
        MediaRequest::PublishAdvertiserDataset { .. } => {
            if let gcg_response::GcgResponse::PublishDatasetToDataRoomResponse(_response) =
                gcg_response
            {
                return Ok(MediaResponse::PublishAdvertiserDataset {});
            }
        }
        MediaRequest::PublishPublisherDataset { .. } => {
            if let gcg_response::GcgResponse::PublishDatasetToDataRoomResponse(_response) =
                gcg_response
            {
                return Ok(MediaResponse::PublishPublisherDataset {});
            }
        }
        MediaRequest::PublishDemographicsDataset { .. } => {
            if let gcg_response::GcgResponse::PublishDatasetToDataRoomResponse(_response) =
                gcg_response
            {
                return Ok(MediaResponse::PublishDemographicsDataset {});
            }
        }
        MediaRequest::PublishSegmentsDataset { .. } => {
            if let gcg_response::GcgResponse::PublishDatasetToDataRoomResponse(_response) =
                gcg_response
            {
                return Ok(MediaResponse::PublishSegmentsDataset {});
            }
        }
        MediaRequest::PublishEmbeddingsDataset { .. } => {
            if let gcg_response::GcgResponse::PublishDatasetToDataRoomResponse(_response) =
                gcg_response
            {
                return Ok(MediaResponse::PublishEmbeddingsDataset {});
            }
        }
        MediaRequest::UnpublishDemographicsDataset { .. } => {
            if let gcg_response::GcgResponse::RemovePublishedDatasetResponse(_response) =
                gcg_response
            {
                return Ok(MediaResponse::UnpublishDemographicsDataset {});
            }
        }
        MediaRequest::UnpublishSegmentsDataset { .. } => {
            if let gcg_response::GcgResponse::RemovePublishedDatasetResponse(_response) =
                gcg_response
            {
                return Ok(MediaResponse::UnpublishSegmentsDataset {});
            }
        }
        MediaRequest::UnpublishEmbeddingsDataset { .. } => {
            if let gcg_response::GcgResponse::RemovePublishedDatasetResponse(_response) =
                gcg_response
            {
                return Ok(MediaResponse::UnpublishEmbeddingsDataset {});
            }
        }
        MediaRequest::CalculateModelledAudienceInsights { .. } => {
            if let gcg_response::GcgResponse::ExecuteComputeResponse(response) = gcg_response {
                return Ok(MediaResponse::CalculateModelledAudienceInsights {
                    compute_node_name: "modelled_audience_insights".into(),
                    job_id_hex: hex::encode(&response.job_id),
                });
            }
        }
        MediaRequest::PublishActivatedAudiencesConfig { .. } => {
            if let gcg_response::GcgResponse::PublishDatasetToDataRoomResponse(_response) =
                gcg_response
            {
                return Ok(MediaResponse::PublishActivatedAudiencesConfig {});
            }
        }
        MediaRequest::UnpublishActivatedAudiencesConfig { .. } => {
            if let gcg_response::GcgResponse::RemovePublishedDatasetResponse(_response) =
                gcg_response
            {
                return Ok(MediaResponse::UnpublishActivatedAudiencesConfig {});
            }
        }
        MediaRequest::GetLookalikeAudience { .. } => {
            if let gcg_response::GcgResponse::ExecuteComputeResponse(response) = gcg_response {
                return Ok(MediaResponse::GetLookalikeAudience {
                    compute_node_name: "get_lookalike_audience".into(),
                    job_id_hex: hex::encode(&response.job_id),
                });
            }
        }
        MediaRequest::CalculateModelledAudienceInsightsView { .. } => {
            if let gcg_response::GcgResponse::ExecuteComputeResponse(response) = gcg_response {
                return Ok(MediaResponse::CalculateModelledAudienceInsightsView {
                    compute_node_name: "modelled_audience_insights_view".into(),
                    job_id_hex: hex::encode(&response.job_id),
                });
            }
        }
        MediaRequest::ViewPublishedActivatedAudiences { .. } => {
            if let gcg_response::GcgResponse::ExecuteComputeResponse(response) = gcg_response {
                return Ok(MediaResponse::ViewPublishedActivatedAudiences {
                    compute_node_name: "view_published_activated_audiences".into(),
                    job_id_hex: hex::encode(&response.job_id),
                });
            }
        }
        MediaRequest::ViewActivatedAudiences { .. } => {
            if let gcg_response::GcgResponse::ExecuteComputeResponse(response) = gcg_response {
                return Ok(MediaResponse::ViewActivatedAudiences {
                    compute_node_name: "view_activated_audiences".into(),
                    job_id_hex: hex::encode(&response.job_id),
                });
            }
        }
        MediaRequest::RetrievePublishedDatasets { .. } => {
            if let gcg_response::GcgResponse::RetrievePublishedDatasetsResponse(response) =
                gcg_response
            {
                let mut advertiser_dataset_hash_hex = None;
                let mut publisher_dataset_hash_hex = None;
                let mut segments_dataset_hash_hex = None;
                let mut demographics_dataset_hash_hex = None;
                let mut embeddings_dataset_hash_hex = None;
                for dataset in response.published_datasets {
                    if dataset.leaf_id.as_str() == "dataset_advertiser" {
                        advertiser_dataset_hash_hex = Some(hex::encode(&dataset.dataset_hash));
                    } else if dataset.leaf_id.as_str() == "dataset_publisher" {
                        publisher_dataset_hash_hex = Some(hex::encode(&dataset.dataset_hash));
                    } else if dataset.leaf_id.as_str() == "dataset_segments" {
                        segments_dataset_hash_hex = Some(hex::encode(&dataset.dataset_hash));
                    } else if dataset.leaf_id.as_str() == "dataset_demographics" {
                        demographics_dataset_hash_hex = Some(hex::encode(&dataset.dataset_hash));
                    } else if dataset.leaf_id.as_str() == "dataset_embeddings" {
                        embeddings_dataset_hash_hex = Some(hex::encode(&dataset.dataset_hash));
                    }
                }
                return Ok(MediaResponse::RetrievePublishedDatasets {
                    advertiser_dataset_hash_hex,
                    publisher_dataset_hash_hex,
                    demographics_dataset_hash_hex,
                    segments_dataset_hash_hex,
                    embeddings_dataset_hash_hex,
                });
            }
        }
        MediaRequest::CalculateOverlapBasic { .. } => {
            if let gcg_response::GcgResponse::ExecuteComputeResponse(response) = gcg_response {
                return Ok(MediaResponse::CalculateOverlapBasic {
                    compute_node_name: "overlap_basic".into(),
                    job_id_hex: hex::encode(&response.job_id),
                });
            }
        }
        MediaRequest::CalculateOverlapInsights { .. } => {
            if let gcg_response::GcgResponse::ExecuteComputeResponse(response) = gcg_response {
                return Ok(MediaResponse::CalculateOverlapInsights {
                    compute_node_name: "consentless_overlap_insights".into(),
                    job_id_hex: hex::encode(&response.job_id),
                });
            }
        }
        MediaRequest::PublishDirectActivationConfig { .. } => {
            if let gcg_response::GcgResponse::PublishDatasetToDataRoomResponse(_response) =
                gcg_response
            {
                return Ok(MediaResponse::PublishDirectActivationConfig {});
            }
        }
        MediaRequest::SubmitRetrieveDirectActivationConfig { .. } => {
            if let gcg_response::GcgResponse::ExecuteComputeResponse(response) = gcg_response {
                return Ok(MediaResponse::SubmitRetrieveDirectActivationConfig {
                    compute_node_name: "direct_activation_config".into(),
                    job_id_hex: hex::encode(&response.job_id),
                });
            }
        }
        MediaRequest::CalculateDirectActivation { .. } => {
            if let gcg_response::GcgResponse::ExecuteComputeResponse(response) = gcg_response {
                return Ok(MediaResponse::CalculateDirectActivation {
                    compute_node_name: "direct_activation".into(),
                    job_id_hex: hex::encode(&response.job_id),
                });
            }
        }
        MediaRequest::RetrieveAuxiliaryState { .. } => {
            if let gcg_response::GcgResponse::ReadAuxiliaryStateResponse(response) = gcg_response {
                let mut state = Vec::with_capacity(response.values.len());
                for value in response.values {
                    let indexed = IndexedMediaAuxiliaryState {
                        user: value.user,
                        index: value.index,
                        state: serde_json::from_slice(&value.value)?,
                    };
                    state.push(indexed)
                }
                return Ok(MediaResponse::RetrieveAuxiliaryState { state });
            }
        }
        MediaRequest::UpdateAuxiliaryState { .. } => {
            if let gcg_response::GcgResponse::CasAuxiliaryStateResponse(response) = gcg_response {
                let value = if let Some(value) = response.value {
                    Some(serde_json::from_slice(&value)?)
                } else {
                    None
                };
                return Ok(MediaResponse::UpdateAuxiliaryState {
                    success: response.success,
                    index: response.index,
                    state: value,
                });
            }
        }
        MediaRequest::UnpublishAdvertiserDataset { .. } => {
            if let gcg_response::GcgResponse::RemovePublishedDatasetResponse(_response) =
                gcg_response
            {
                return Ok(MediaResponse::UnpublishAdvertiserDataset {});
            }
        }
        MediaRequest::UnpublishPublisherDataset { .. } => {
            if let gcg_response::GcgResponse::RemovePublishedDatasetResponse(_response) =
                gcg_response
            {
                return Ok(MediaResponse::UnpublishPublisherDataset {});
            }
        }
        MediaRequest::UnpublishDirectActivationConfig { .. } => {
            if let gcg_response::GcgResponse::RemovePublishedDatasetResponse(_response) =
                gcg_response
            {
                return Ok(MediaResponse::UnpublishDirectActivationConfig {});
            }
        }
    }
    // No match, perhaps it's a failure
    if let gcg_response::GcgResponse::Failure(response) = gcg_response {
        return Err(response.as_str())?;
    }
    return Err("Unexpected GcgResponse, cannot decompile as MediaResponse")?;
}

fn flatten_validation_error(error: &DataRoomValidationError) -> String {
    let mut message = error.message.clone();
    fn add_field(message: &mut String, field_name: &str, field: &Option<impl std::fmt::Display>) {
        if let Some(value) = field {
            message.push_str(format!(", {}: {}", field_name, value).as_str());
        }
    }

    add_field(&mut message, "compute_node_id", &error.compute_node_id);
    add_field(
        &mut message,
        "user_permission_id",
        &error.user_permission_id,
    );
    add_field(&mut message, "permission_index", &error.permission_index);
    add_field(
        &mut message,
        "attestation_specification_id",
        &error.attestation_specification_id,
    );
    add_field(
        &mut message,
        "authentication_method_iid",
        &error.authentication_method_id,
    );

    message
}

pub fn convert_media_data_room_any_to_latest_serialized(
    media_data_room_versioned_serialized: &str,
) -> CompileResult<String> {
    let data_room: MediaDataRoom = serde_json::from_str(media_data_room_versioned_serialized)?;
    Ok(serde_json::to_string(
        &convert_media_data_room_any_to_latest(data_room)?,
    )?)
}

pub fn convert_media_auxiliary_state_any_to_latest_serialized(
    media_auxiliary_state_versioned_serialized: &str,
) -> CompileResult<String> {
    let media_auxiliary_state: MediaAuxiliaryState =
        serde_json::from_str(media_auxiliary_state_versioned_serialized)?;
    Ok(serde_json::to_string(
        &convert_media_auxiliary_state_any_to_latest(media_auxiliary_state)?,
    )?)
}

pub fn convert_direct_activation_config_any_to_latest_serialized(
    direct_activation_config_versioned_serialized: &str,
) -> CompileResult<String> {
    let direct_activation_config: DirectActivationConfig =
        serde_json::from_str(direct_activation_config_versioned_serialized)?;
    Ok(serde_json::to_string(
        &convert_direct_activation_config_any_to_latest(direct_activation_config)?,
    )?)
}

fn convert_media_auxiliary_state_any_to_latest(
    value: MediaAuxiliaryState,
) -> CompileResult<MediaAuxiliaryStateLatest> {
    enum OldOrLatest {
        Old(MediaAuxiliaryState),
        Latest(MediaAuxiliaryStateLatest),
    }
    fn convert_any_to_next(value: MediaAuxiliaryState) -> CompileResult<OldOrLatest> {
        match value {
            MediaAuxiliaryState::V0(value) => Ok(OldOrLatest::Old(MediaAuxiliaryState::V1(value))),
            MediaAuxiliaryState::V1(value) => Ok(OldOrLatest::Old(MediaAuxiliaryState::V2(value))),
            MediaAuxiliaryState::V2(value) => Ok(OldOrLatest::Old(MediaAuxiliaryState::V3(value))),
            MediaAuxiliaryState::V3(value) => Ok(OldOrLatest::Latest(value)),
        }
    }
    let mut current = value;
    loop {
        match convert_any_to_next(current)? {
            OldOrLatest::Old(next) => {
                current = next;
            }
            OldOrLatest::Latest(latest) => return Ok(latest),
        }
    }
}

fn convert_direct_activation_config_any_to_latest(
    value: DirectActivationConfig,
) -> CompileResult<DirectActivationConfigLatest> {
    enum OldOrLatest {
        Old(DirectActivationConfig),
        Latest(DirectActivationConfigLatest),
    }
    fn convert_any_to_next(value: DirectActivationConfig) -> CompileResult<OldOrLatest> {
        match value {
            DirectActivationConfig::V0(value) => {
                Ok(OldOrLatest::Old(DirectActivationConfig::V1(value)))
            }
            DirectActivationConfig::V1(value) => Ok(OldOrLatest::Latest(value)),
        }
    }
    let mut current = value;
    loop {
        match convert_any_to_next(current)? {
            OldOrLatest::Old(next) => {
                current = next;
            }
            OldOrLatest::Latest(latest) => return Ok(latest),
        }
    }
}

fn convert_media_data_room_any_to_latest(
    data_room: MediaDataRoom,
) -> CompileResult<MediaDataRoomLatest> {
    enum OldOrLatest {
        Old(MediaDataRoom),
        Latest(MediaDataRoomLatest),
    }
    fn convert_any_to_next(data_room: MediaDataRoom) -> CompileResult<OldOrLatest> {
        match data_room {
            MediaDataRoom::V0(data_room) => Ok(OldOrLatest::Old(MediaDataRoom::V1(
                v1::convert_data_room_v0_to_v1(data_room)?,
            ))),
            MediaDataRoom::V1(data_room) => Ok(OldOrLatest::Old(MediaDataRoom::V2(
                v2::convert_data_room_v1_to_v2(data_room)?,
            ))),
            MediaDataRoom::V2(data_room) => Ok(OldOrLatest::Old(MediaDataRoom::V3(
                v3::convert_data_room_v2_to_v3(data_room)?,
            ))),
            MediaDataRoom::V3(data_room) => Ok(OldOrLatest::Latest(data_room)),
        }
    }

    let mut current = data_room;
    loop {
        match convert_any_to_next(current)? {
            OldOrLatest::Old(next) => {
                current = next;
            }
            OldOrLatest::Latest(latest) => return Ok(latest),
        }
    }
}
