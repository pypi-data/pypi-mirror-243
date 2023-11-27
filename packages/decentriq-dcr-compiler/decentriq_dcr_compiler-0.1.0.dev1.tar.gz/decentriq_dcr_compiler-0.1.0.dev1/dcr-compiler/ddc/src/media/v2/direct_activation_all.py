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


def validate_config(config: MediaDataRoomConfig):
    for field in ["matching_columns", "advertiser_column_names", "publisher_column_names", "audience_type_column_name",
                  "segment_column_name", "activation_id_column_name"]:
        if field not in config:
            raise Exception(f"Expected field '{field}'")
    for list_field in [config["matching_columns"], config["advertiser_column_names"], config["publisher_column_names"]]:
        if not isinstance(list_field, list):
            raise Exception(f"Expected a list")
        for element in list_field:
            if not isinstance(element, str):
                raise Exception(f"Expected a str")
    if config["audience_type_column_name"] is not None and not isinstance(config["audience_type_column_name"], str):
        raise Exception(f"Expected a None or a str")
    if config["segment_column_name"] is not None and not isinstance(config["segment_column_name"], str):
        raise Exception(f"Expected a None or a str")
    if config["activation_id_column_name"] is not None and not isinstance(config["activation_id_column_name"], str):
        raise Exception(f"Expected a None or a str")


with open("/input/media_data_room_config.json", "r") as file:
    config: MediaDataRoomConfig = cast(MediaDataRoomConfig, json.loads(file.read()))

validate_config(config)

print(f'Config: {config}"')

if len(config["matching_columns"]) > 1:
    raise Exception("Only one matching column is supported")
if len(config["matching_columns"]) == 0:
    raise Exception("At least one matching column must be specified")
matching_column = config["matching_columns"][0]

audience_type = config["audience_type_column_name"]
if audience_type is None:
    raise Exception("Direct activation requires an audience_type_column_name")

activation_id = config["activation_id_column_name"]
if activation_id is None:
    raise Exception("Direct activation requires an activation_id_column_name")

entire_overlap = "All audiences combined"

def remove_nas(frame: pandas.DataFrame, column: str) -> pandas.DataFrame:
    # Remove rows with NAN matching ids
    return frame[frame[column].notna()]

df = {}

# Input and Basic ETL
df['input_advertiser'] = pandas.read_csv("/input/dataset_advertiser/dataset.csv", names=config["advertiser_column_names"])
df['input_publisher'] = pandas.read_csv("/input/dataset_publisher/dataset.csv", names=config["publisher_column_names"])
df["publisher"] = remove_nas(df["input_publisher"], matching_column)[[matching_column, activation_id]].drop_duplicates().astype(str)
df["advertiser"] = remove_nas(df["input_advertiser"], matching_column)[[matching_column, audience_type]].drop_duplicates().astype(str)

df["audience_types"] = df["advertiser"][[audience_type]].drop_duplicates()
df["audience_types"].loc[df["audience_types"].index.max()+1] = [entire_overlap]

# Matching to Find Overlap
df["matched_individual"] = df["advertiser"].set_index(matching_column).join(df["publisher"].set_index(matching_column), how="inner")

df["matched_all"] = df["matched_individual"].reset_index().copy(deep=True)
df["matched_all"][audience_type] = entire_overlap
df["matched_all"].drop_duplicates(inplace=True)
df["matched_all"].set_index(matching_column, inplace=True)

df["matched"] = pandas.concat([df["matched_all"], df["matched_individual"]])

df["matched_output"] = df["matched"].reset_index()[[audience_type, activation_id]].drop_duplicates().set_index(audience_type)

df["matched_output"].to_csv("/output/activation_ids.csv", header=False, index=True)
