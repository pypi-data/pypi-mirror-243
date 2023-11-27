import pandas
import numpy
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

class CalculateOverlapBasicStatistics(TypedDict):
    advertiser_size: int
    advertiser_number_of_audience_types: Optional[int]
    publisher_number_of_segments: Optional[int]


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

df = {}

# Read and remove duplicates
df["dataset_advertiser"] = pandas \
    .read_csv("/input/dataset_advertiser.csv", header=None) \
    .drop_duplicates()
df["dataset_publisher"] = pandas \
    .read_csv("/input/dataset_publisher.csv", header=None) \
    .drop_duplicates()

if len(df["dataset_advertiser"].dtypes) != len(config["advertiser_column_names"]):
    raise Exception(f'Column names for advertiser {config["advertiser_column_names"]} do not align with the number of '
                    f'columns in input ({len(df["dataset_advertiser"].dtypes)})')
if len(df["dataset_publisher"].dtypes) != len(config["publisher_column_names"]):
    raise Exception(f'Column names for publisher {config["publisher_column_names"]} do not align with the number of '
                    f'columns in input ({len(df["dataset_publisher"].dtypes)})')


df["dataset_advertiser"].columns = config["advertiser_column_names"]
df["dataset_publisher"].columns = config["publisher_column_names"]

if len(config["matching_columns"]) > 1:
    raise Exception("Only one matching column is supported")
if len(config["matching_columns"]) == 0:
    raise Exception("At least one matching column must be specified")
matching_column = config["matching_columns"][0]


def remove_nas(frame: pandas.DataFrame, column: str) -> pandas.DataFrame:
    return frame[frame[column].notna()]


# Remove rows with NAN matching ids
df["dataset_advertiser"] = remove_nas(df["dataset_advertiser"], matching_column)
df["dataset_publisher"] = remove_nas(df["dataset_publisher"], matching_column)

audience_type = config["audience_type_column_name"]
if audience_type is None:
    df["dataset_advertiser"] = df["dataset_advertiser"][[matching_column]].astype(str)
else:
    df["dataset_advertiser"] = df["dataset_advertiser"][[matching_column, audience_type]].astype(str)

segment = config["segment_column_name"]
if segment is None:
    df["dataset_publisher"] = df["dataset_publisher"][[matching_column]].astype(str)
else:
    df["dataset_publisher"] = df["dataset_publisher"][[matching_column, segment]].astype(str)
    df["dataset_publisher"] = df["dataset_publisher"].groupby(segment).filter(lambda s: len(s) >= config["cutoff_overlap_basic_segment"])

df["overlap"] = pandas.DataFrame(columns=["audience_type", "advertiser_size", "overlap_size"])
merged = df["dataset_advertiser"].merge(df["dataset_publisher"], on=matching_column, how="inner")
df["overlap"].loc[0] = [
    "All audiences combined",
    len(df["dataset_advertiser"][[matching_column]].drop_duplicates()),
    len(merged[[matching_column]].drop_duplicates()),
]
if audience_type is not None:
    advertiser_grouped = df["dataset_advertiser"].groupby(audience_type).size()
    merged_grouped = merged.groupby(audience_type)[matching_column].nunique()
    df["overlap_by_audience"] = advertiser_grouped.to_frame() \
        .join(merged_grouped.to_frame(), rsuffix="r", how="left") \
        .reset_index()
    df["overlap_by_audience"].columns = ["audience_type", "advertiser_size", "overlap_size"]
    df["overlap_by_audience"]["overlap_size"] = df["overlap_by_audience"]["overlap_size"].fillna(0).astype('int64')
    df["overlap"] = pandas.concat([df["overlap"], df["overlap_by_audience"]])

df["overlap_rounded"] = df["overlap"].round({
    "advertiser_size": config["rounding_decimals_count"],
    "overlap_size": config["rounding_decimals_count"],
})

df["overlap_rounded"].to_csv("/output/overlap.csv", header=False, index=False)

advertiser_size = int(len(df["dataset_advertiser"][[matching_column]].drop_duplicates()))
if audience_type is None:
    advertiser_number_of_audience_types = None
else:
    advertiser_number_of_audience_types = int(df["dataset_advertiser"][audience_type].nunique())
if segment is None:
    publisher_number_of_segments = None
else:
    publisher_number_of_segments = int(df["dataset_publisher"][segment].nunique())

advertiser_size_rounded = round(advertiser_size, config["rounding_decimals_count"])
statistics = CalculateOverlapBasicStatistics(
    advertiser_size=advertiser_size_rounded,
    advertiser_number_of_audience_types=advertiser_number_of_audience_types,
    publisher_number_of_segments=publisher_number_of_segments
)

with open("/output/statistics.json", "w") as file:
    file.write(json.dumps(statistics))
