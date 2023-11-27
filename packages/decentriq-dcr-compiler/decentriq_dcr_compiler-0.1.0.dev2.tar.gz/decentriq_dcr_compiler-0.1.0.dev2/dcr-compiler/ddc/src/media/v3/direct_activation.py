import sqlite3
import json
from typing import TypedDict, List, cast, Optional
import sys
import subprocess
import os
import base64
from decentriq_util.error import catch_safe_error

# @profile
def run():
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

    if "v0" in config:
        audience_types = config["v0"]["audienceTypes"]
    elif "v1" in config:
        audience_types = config["v1"]["audienceTypes"]
    else:
        raise Exception(f"Expected field 'v0' or 'v1")

    db_file = "/output/work.db"

    con = sqlite3.connect(db_file)
    cur = con.cursor()

    cur.execute("PRAGMA synchronous = OFF")
    cur.execute("PRAGMA journal_mode = OFF")
    cur.execute("PRAGMA temp_store_directory = '/output'")

    cur.execute("CREATE TABLE audience_types (audience_type_str TEXT NOT NULL, PRIMARY KEY(audience_type_str)) WITHOUT ROWID")
    cur.executemany("INSERT OR IGNORE INTO audience_types VALUES (?)", list(map(lambda a: (a,), audience_types)))

    cur.execute('ATTACH DATABASE "/input/direct_activation_all/activation_ids.db" AS activation_ids')
    audience_types_results = cur.execute("SELECT ac.audience_type, at.audience_type_str FROM audience_types at INNER JOIN activation_ids.audience_types ac ON at.audience_type_str = ac.audience_type_str").fetchall()
    con.commit()

    for audience_types_result in audience_types_results:
        audience_type = audience_types_result[0]
        audience_type_str = audience_types_result[1]
        # base64 the audience_type for the filename (it may contain any character)
        audience_type_base64 = f'{base64.b64encode(audience_type_str.encode("utf-8")).decode()}'
        result = subprocess.run([
            'sqlite3',
            db_file,
            '-cmd',
            '.mode csv',
            '.separator ,',
            f'.output /output/{audience_type_base64}.csv',
            'ATTACH DATABASE "/input/direct_activation_all/activation_ids.db" AS activation_ids',
            f'SELECT activation_id FROM activation_ids.activation_ids WHERE audience_type = {audience_type}',
            '.quit',
        ])
        if result.returncode != 0:
            raise Exception(f"sqlite3 export failed with exit code {result.returncode}")

    os.remove(db_file)

if __name__ == '__main__':
    with catch_safe_error():
        run()
