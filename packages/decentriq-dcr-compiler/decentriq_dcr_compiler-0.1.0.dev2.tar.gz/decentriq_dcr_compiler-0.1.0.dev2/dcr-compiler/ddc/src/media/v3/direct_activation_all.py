import json
from typing import TypedDict, List, cast, Optional
import re
import sqlite3
import sys
import subprocess
import os
from decentriq_util.error import catch_safe_error

def run():
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

    column_name_validator_re = re.compile("^[-_:0-9a-zA-Z]*$")
    def validate_column_names(columns: List[str]):
        for column in columns:
            if column_name_validator_re.match(column) is None:
                raise Exception(f"Column name {column} contains unsupported characters")

    validate_column_names(config["advertiser_column_names"])
    validate_column_names(config["publisher_column_names"])
    advertiser_schema_sql = ", ".join(map(lambda name: f"\"{name}\"", config["advertiser_column_names"]))
    publisher_schema_sql = ", ".join(map(lambda name: f"\"{name}\"", config["publisher_column_names"]))


    db_file = "/output/database.db"

    con = sqlite3.connect(db_file)
    cur = con.cursor()
    cur.execute("PRAGMA synchronous = OFF")
    cur.execute("PRAGMA journal_mode = OFF")
    cur.execute("PRAGMA temp_store_directory = '/output'")

    cur.execute(f"CREATE TABLE advertiser_raw({advertiser_schema_sql})")
    cur.execute(f"CREATE TABLE publisher_raw({publisher_schema_sql})")

    result = subprocess.run([
        'sqlite3',
        db_file,
        '-cmd',
        '.mode csv',
        '.separator ,',
        '.import /input/dataset_advertiser/dataset.csv advertiser_raw'
    ])
    if result.returncode != 0:
        raise Exception(f"sqlite3 import failed with exit code {result.returncode}")

    result = subprocess.run([
        'sqlite3',
        db_file,
        '-cmd',
        '.mode csv',
        '.separator ,',
        '.import /input/dataset_publisher/dataset.csv publisher_raw'
    ])
    if result.returncode != 0:
        raise Exception(f"sqlite3 import failed with exit code {result.returncode}")

    # Input and Basic ETL
    cur.execute(f"CREATE TABLE audience_types AS SELECT DISTINCT \"{audience_type}\" AS audience_type_str FROM advertiser_raw")
    cur.execute(f"CREATE VIEW advertiser AS SELECT DISTINCT r.\"{matching_column}\" AS matching_column, a.rowid AS audience_type FROM advertiser_raw r INNER JOIN audience_types a ON a.audience_type_str = r.\"{audience_type}\" WHERE matching_column != ''")
    cur.execute(f"CREATE VIEW publisher AS SELECT DISTINCT \"{matching_column}\" AS matching_column, \"{activation_id}\" AS activation_id FROM publisher_raw WHERE matching_column != ''")

    cur.execute(f"CREATE VIEW matched_individual AS SELECT audience_type, a.matching_column, activation_id FROM advertiser a INNER JOIN publisher p ON a.matching_column = p.matching_column ORDER BY audience_type")
    cur.execute(f"CREATE VIEW matched_all AS SELECT DISTINCT -1 as audience_type, a.matching_column, activation_id FROM advertiser a INNER JOIN publisher p ON a.matching_column = p.matching_column")

    cur.execute(f"CREATE VIEW matched AS SELECT * FROM matched_all UNION ALL SELECT * FROM matched_individual")

    activation_ids_db = "/output/activation_ids.db"

    result = subprocess.run([
        'sqlite3',
        db_file,
        '-cmd',
        f'ATTACH DATABASE "{activation_ids_db}" AS activation_ids',
        'CREATE TABLE activation_ids.activation_ids (audience_type INTEGER NOT NULL, matching_column TEXT NOT NULL, activation_id TEXT NOT NULL, PRIMARY KEY(audience_type, matching_column)) WITHOUT ROWID',
        'CREATE INDEX activation_ids.activation_ids_index ON activation_ids(audience_type)',
        'INSERT OR IGNORE INTO activation_ids.activation_ids SELECT * FROM matched',
        'CREATE TABLE activation_ids.audience_types (audience_type INTEGER NOT NULL, audience_type_str TEXT NOT NULL, PRIMARY KEY(audience_type)) WITHOUT ROWID',
        'INSERT OR IGNORE INTO activation_ids.audience_types SELECT rowid, audience_type_str FROM audience_types',
        'INSERT OR IGNORE INTO activation_ids.audience_types VALUES (-1, "All audiences combined")',
        '.quit',
    ])
    if result.returncode != 0:
        raise Exception(f"sqlite3 export failed with exit code {result.returncode}")

    os.remove(db_file)

if __name__ == '__main__':
    with catch_safe_error():
        run()
