import pandas
import json
from typing import TypedDict, List, cast, Optional

import base64


class DirectActivationConfigV0(TypedDict):
    audienceTypes: List[str]


class DirectActivationConfig(TypedDict):
    v0: Optional[DirectActivationConfigV0]
    v1: Optional[DirectActivationConfigV0]


def validate_config_v0(config: DirectActivationConfigV0):
    for field in ["audienceTypes"]:
        if field not in config:
            raise Exception(f"Expected field '{field}'")
    for list_field in [config["audienceTypes"]]:
        if not isinstance(list_field, list):
            raise Exception(f"Expected a list")
        for element in list_field:
            if not isinstance(element, str):
                raise Exception(f"Expected a str")


def validate_config(config: DirectActivationConfig):
    if "v0" in config:
        validate_config_v0(config["v0"])
        return
    if "v1" in config:
        validate_config_v0(config["v1"])
        return
    raise Exception(f"Expected field 'v0' or 'v1")

with open("/input/direct_activation_config.json", "r") as file:
    config: DirectActivationConfig = cast(DirectActivationConfig, json.loads(file.read()))

validate_config(config)

audience_types = None
if "v0" in config:
    audience_types = config["v0"]["audienceTypes"]
elif "v1" in config:
    audience_types = config["v1"]["audienceTypes"]
else:
    raise Exception(f"Expected field 'v0' or 'v1")

print(f'Config: {config}"')

df = {}

df["activation_ids_all"] = pandas.read_csv("/input/direct_activation_all/activation_ids.csv",
                                           names=["audience_type", "activation_id"])

df["activation_ids_filtered"] = df["activation_ids_all"][
    df["activation_ids_all"]["audience_type"].isin(audience_types)]

for name, value in df["activation_ids_filtered"].groupby("audience_type"):
    filename = f'{base64.b64encode(name.encode("utf-8")).decode()}'
    value.reset_index(drop=True).set_index("audience_type").to_csv(f"/output/{filename}.csv", header=False, index=False)
