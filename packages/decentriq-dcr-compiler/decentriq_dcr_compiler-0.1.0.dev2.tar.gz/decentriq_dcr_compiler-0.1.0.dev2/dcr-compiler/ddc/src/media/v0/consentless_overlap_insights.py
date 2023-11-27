import base64

import numpy
import pandas
import json
from typing import TypedDict, List, cast, Optional


class MediaDataRoomConfig(TypedDict):
    matching_columns: List[str]
    advertiser_column_names: List[str]
    publisher_column_names: List[str]
    audience_type_column_name: Optional[str]
    segment_column_name: Optional[str]
    activation_id_column_name: Optional[str]
    rounding_decimals_count: int
    rounding_decimals_ratio: int
    cutoff_overlap_basic_segment: int
    cutoff_consentless_overlap_insights_unmatched_audience_type: int
    cutoff_consentless_overlap_insights_unmatched_segment: int
    cutoff_consentless_overlap_insights_matched_audience_type: int
    cutoff_consentless_overlap_insights_matched_segment_audience_type: int


def validate_config(config: MediaDataRoomConfig):
    for field in [
        "matching_columns",
        "advertiser_column_names",
        "publisher_column_names",
        "audience_type_column_name",
        "segment_column_name",
        "activation_id_column_name",
        "rounding_decimals_count",
        "rounding_decimals_ratio",
        "cutoff_overlap_basic_segment",
        "cutoff_consentless_overlap_insights_unmatched_audience_type",
        "cutoff_consentless_overlap_insights_unmatched_segment",
        "cutoff_consentless_overlap_insights_matched_audience_type",
        "cutoff_consentless_overlap_insights_matched_segment_audience_type",
    ]:
        if field not in config:
            raise Exception(f"Expected field '{field}'")
    for list_field in [
        config["matching_columns"],
        config["advertiser_column_names"],
        config["publisher_column_names"],
    ]:
        if not isinstance(list_field, list):
            raise Exception(f"Expected a list")
        for element in list_field:
            if not isinstance(element, str):
                raise Exception(f"Expected a str")
    for optional_str_field in [
        config["audience_type_column_name"],
        config["segment_column_name"],
        config["activation_id_column_name"]
    ]:
        if optional_str_field is not None and not isinstance(optional_str_field, str):
            raise Exception(f"Expected a None or a str")
    for int_field in [
        config["rounding_decimals_count"],
        config["rounding_decimals_ratio"],
        config["cutoff_overlap_basic_segment"],
        config["cutoff_consentless_overlap_insights_unmatched_audience_type"],
        config["cutoff_consentless_overlap_insights_unmatched_segment"],
        config["cutoff_consentless_overlap_insights_matched_audience_type"],
        config["cutoff_consentless_overlap_insights_matched_segment_audience_type"],
    ]:
        if not isinstance(int_field, int):
            raise Exception(f"Expected an int")


with open("/input/media_data_room_config.json", "r") as file:
    config: MediaDataRoomConfig = cast(MediaDataRoomConfig, json.loads(file.read()))

validate_config(config)

print(f'Config: {config}"')

class CalculateOverlapInsightsParams(TypedDict):
    audience_types: List[str]


def validate_params(params: CalculateOverlapInsightsParams):
    if "audience_types" not in params:
        raise Exception(f"Expected field 'audience_types'")
    if not isinstance(params["audience_types"], list):
        raise Exception(f"Expected a list")
    for element in params["audience_types"]:
        if not isinstance(element, str):
            raise Exception(f"Expected a str")

with open("/input/overlap_insights_params.json", "r") as file:
    params: CalculateOverlapInsightsParams = cast(CalculateOverlapInsightsParams, json.loads(file.read()))

validate_params(params)

print(f'Params: {params}"')

if len(config["matching_columns"]) > 1:
    raise Exception("Only one matching column is supported")
if len(config["matching_columns"]) == 0:
    raise Exception("At least one matching column must be specified")
matching_column = config["matching_columns"][0]

audience_type = config["audience_type_column_name"]
if audience_type is None:
    raise Exception("Overlap insights require an audience_type_column_name")

segment = config["segment_column_name"]
if segment is None:
    raise Exception("Overlap insights require an segment_column_name")

entire_overlap = "All audiences combined"

def remove_nas(frame: pandas.DataFrame, column: str) -> pandas.DataFrame:
    # Remove rows with NAN matching ids
    return frame[frame[column].notna()]

df = {}
stats = {}

# Input and Basic ETL
df['input_advertiser'] = pandas.read_csv("/input/dataset_advertiser.csv", names=config["advertiser_column_names"])
df['input_publisher'] = pandas.read_csv("/input/dataset_publisher.csv", names=config["publisher_column_names"])
df["publisher"] = remove_nas(df["input_publisher"], matching_column)[[matching_column, segment]].drop_duplicates().astype(str)
df["publisher"] = df["publisher"].groupby(segment).filter(lambda s: len(s) >= config["cutoff_consentless_overlap_insights_unmatched_segment"])
df["advertiser"] = remove_nas(df["input_advertiser"], matching_column)[[matching_column, audience_type]].drop_duplicates().astype(str)
df["advertiser"] = df["advertiser"].groupby(audience_type).filter(lambda s: len(s) >= config["cutoff_consentless_overlap_insights_unmatched_audience_type"])

# Skeleton
df["segments"] = df["publisher"][[segment]].drop_duplicates()
df["audience_types"] = df["advertiser"][[audience_type]].drop_duplicates()
df["audience_types"].loc[df["audience_types"].index.max()+1] = [entire_overlap]
df['skeleton'] = df["audience_types"].merge(df["segments"], how='cross').set_index([audience_type, segment])

# Summary Stats (Pre-Match)
stats['total_publisher'] = df["publisher"][matching_column].unique().size
stats['total_advertiser'] = df["advertiser"][matching_column].unique().size
df["unmatched_segment_count"] = df["publisher"].groupby([segment]).count().rename(columns={matching_column: "unmatched_segment_count"})

# Matching to Find Overlap
df["matched_individual_segments"] = df["advertiser"].set_index(matching_column).join(df["publisher"].set_index(matching_column), how="inner")

# Here we create an "all segments/entire overlap" to keep ourself DRY. we do it post-match because it is more memory efficient.
df["matched_all_segments"] = df["matched_individual_segments"].reset_index().copy(deep=True)
df["matched_all_segments"][audience_type] = entire_overlap
df["matched_all_segments"].drop_duplicates(inplace=True)
df["matched_all_segments"].set_index(matching_column, inplace=True)
df["matched"] = pandas.concat([df["matched_all_segments"], df["matched_individual_segments"]])

# Summary Stats (Post-Match)
df["matched_audience_type_count"] = df["matched"].reset_index()[[audience_type, matching_column]].drop_duplicates().groupby([audience_type]).count().rename(columns={matching_column: "matched_audience_type_count"})
df["matched_audience_type_count"]["matched_audience_type_count"][
    df["matched_audience_type_count"]["matched_audience_type_count"] < config["cutoff_consentless_overlap_insights_matched_audience_type"]
] = 0
df["matched_segment_audience_type_count"] = df["matched"].reset_index().groupby([audience_type, segment]).count().rename(columns={matching_column: "matched_segment_audience_type_count"}) # Note this groupby order is supposed to match the skeleton index
df["matched_segment_audience_type_count"]["matched_segment_audience_type_count"][
    df["matched_segment_audience_type_count"]["matched_segment_audience_type_count"] < config["cutoff_consentless_overlap_insights_matched_segment_audience_type"]
] = 0

# Assemble Full Skeleton
df['full_skeleton'] = df['skeleton'].join(
    df["matched_segment_audience_type_count"],
    how="left"
).join(
    df["matched_audience_type_count"],  # this is ok because they have the same first index
    how="left"
).reset_index().set_index(segment).join(
    df["unmatched_segment_count"],
    how="left"
).reset_index().fillna(0)

print(df['full_skeleton'])

# Calculate Propensity Statistics
df['full_skeleton']["base_propensity"] = df['full_skeleton']["unmatched_segment_count"] / stats['total_publisher']
df['full_skeleton']["overlap_propensity"] = df['full_skeleton']["matched_segment_audience_type_count"] / df['full_skeleton']["matched_audience_type_count"]
df['full_skeleton']["overlap_propensity"].replace([numpy.inf, -numpy.inf], 0, inplace=True)
df['full_skeleton']["overlap_propensity"].fillna(0, inplace=True)
df['full_skeleton']["net_propensity"] = (df['full_skeleton']["overlap_propensity"] - df['full_skeleton']["base_propensity"]) / df['full_skeleton']["base_propensity"]
df["propensity"] = df['full_skeleton'][[audience_type, segment, "base_propensity", "overlap_propensity", "net_propensity"]].sort_values(by=[audience_type, 'net_propensity'], ascending=False)

df["propensity_rounded"] = df["propensity"].round({
    "base_propensity": config["rounding_decimals_ratio"],
    "overlap_propensity": config["rounding_decimals_ratio"],
    "net_propensity": config["rounding_decimals_ratio"],
})

# Create a mapping of segment->set of matching_ids
segment_to_ids = df["publisher"].groupby(segment)[matching_column].apply(set)

stats['cumulative_mapping'] = []
for (aud_type, aud_propensity) in df["propensity"].groupby(audience_type):
    aud_sorted = aud_propensity.sort_values("net_propensity", ascending=False)
    current_id_set = set()
    for (_, row) in aud_sorted.iterrows():
        current_id_set = current_id_set.union(segment_to_ids[row[segment]])
        current_size = len(current_id_set)
        stats['cumulative_mapping'].append([aud_type, row[segment], current_size / stats['total_publisher'], current_size])

df['cumulative_mapping'] = pandas.DataFrame(data=stats['cumulative_mapping'], columns=[audience_type, segment, 'cumulative_addressable', 'cumulative_size']).set_index([audience_type, segment])
df['cumulative_mapping_rounded'] = df['cumulative_mapping'].round({
    "cumulative_addressable": config["rounding_decimals_ratio"],
    "cumulative_size": config["rounding_decimals_count"],
})
df['cumulative_audiences_rounded'] = df["propensity_rounded"].set_index([audience_type, segment]).join(df['cumulative_mapping_rounded'])

for name, value in df['cumulative_audiences_rounded'].groupby(audience_type):
    filename = f'{base64.b64encode(name.encode("utf-8")).decode()}'
    value.reset_index().set_index(audience_type).to_csv(f"/output/{filename}.csv", header=False, index=False)
