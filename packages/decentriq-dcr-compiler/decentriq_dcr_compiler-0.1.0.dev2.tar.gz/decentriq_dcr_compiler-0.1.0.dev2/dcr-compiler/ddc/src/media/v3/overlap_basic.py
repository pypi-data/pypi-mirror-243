import sqlite3
import json
from typing import TypedDict, List, cast, Optional
import sys
import subprocess
import os
import re
import csv
from decentriq_util.error import catch_safe_error

# @profile
def run():
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

    db_file = "/output/database.db"

    if os.path.isfile("/sys/fs/cgroup/memory.max"):
        with open("/sys/fs/cgroup/memory.max", "r") as file:
            max_memory = int(file.read())
    elif os.path.isfile("/sys/fs/cgroup/memory/memory.limit_in_bytes"):
        with open("/sys/fs/cgroup/memory/memory.limit_in_bytes", "r") as file:
            max_memory = int(file.read())
    else:
        raise Exception("Cannot determine cgroup memory bound")

    sqlite_available_memory = (max_memory - 200 * 1024 * 1024)
    print(f"Available memory for SQLite: {sqlite_available_memory}")
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    cur.execute("PRAGMA synchronous = OFF")
    cur.execute("PRAGMA journal_mode = OFF")
    cur.execute("PRAGMA temp_store_directory = '/output'")

    if len(config["matching_columns"]) > 1:
        raise Exception("Only one matching column is supported")
    if len(config["matching_columns"]) == 0:
        raise Exception("At least one matching column must be specified")
    matching_column = config["matching_columns"][0]
    advertiser_matching_id_index = config["advertiser_column_names"].index(matching_column)
    publisher_matching_id_index = config["publisher_column_names"].index(matching_column)

    audience_type = config["audience_type_column_name"]
    audience_type_index = config["advertiser_column_names"].index(audience_type)

    segment = config["segment_column_name"]
    segment_index = config["publisher_column_names"].index(segment)

    cur.execute(f"CREATE TABLE matching_ids(matching_id TEXT NOT NULL, UNIQUE(matching_id))")
    cur.execute(f"CREATE TABLE audience_types(audience_type TEXT NOT NULL, UNIQUE(audience_type))")
    cur.execute(f"CREATE INDEX audience_types_index ON audience_types(audience_type)")
    cur.execute(f"CREATE TABLE segments(segment TEXT NOT NULL, UNIQUE(segment))")
    cur.execute(f"CREATE INDEX segments_index ON segments(segment)")

    cur.execute(f"CREATE TABLE advertiser(matching_id INTEGER NOT NULL, audience_type INTEGER NOT NULL, PRIMARY KEY(matching_id, audience_type)) WITHOUT ROWID")
    cur.execute(f"CREATE TABLE publisher(matching_id INTEGER NOT NULL, segment INTEGER NOT NULL, PRIMARY KEY(matching_id, segment)) WITHOUT ROWID")

    batch_size = 10000
    audience_type_map = dict()
    segment_map = dict()

    def process_advertiser_batch(batch):
        matching_ids = list(map(lambda row: [row[advertiser_matching_id_index]], batch))
        cur.executemany("INSERT OR IGNORE INTO matching_ids VALUES (?)", matching_ids)

        audience_types = list(map(lambda row: row[audience_type_index], batch))
        for audience_type in audience_types:
            if audience_type not in audience_type_map:
                cur.execute("INSERT INTO audience_types VALUES (?)", [audience_type])
                audience_type_map[audience_type] = cur.lastrowid
        pairs = list(map(lambda row: (audience_type_map[row[audience_type_index]], row[advertiser_matching_id_index]), batch))
        cur.executemany("INSERT OR IGNORE INTO advertiser (matching_id, audience_type) SELECT rowid, ? FROM matching_ids m WHERE m.matching_id = ?", pairs)

    def process_publisher_batch(batch):
        matching_ids = list(map(lambda row: [row[publisher_matching_id_index]], batch))
        cur.executemany("INSERT OR IGNORE INTO matching_ids VALUES (?)", matching_ids)

        segments = list(map(lambda row: row[segment_index], batch))
        for segment in segments:
            if segment not in segment_map:
                cur.execute("INSERT INTO segments VALUES (?)", [segment])
                segment_map[segment] = cur.lastrowid
        pairs = list(map(lambda row: (segment_map[row[segment_index]], row[publisher_matching_id_index]), batch))
        cur.executemany("INSERT OR IGNORE INTO publisher (matching_id, segment) SELECT rowid, ? FROM matching_ids m WHERE m.matching_id = ?", pairs)

    def process_csv_batch(csv_file_path, process_fn):
        with open(csv_file_path, newline='') as file:
            reader = csv.reader(file)
            batch = []
            for row in reader:
                batch.append(row)
                if len(batch) >= batch_size:
                    process_fn(batch)
                    batch = []
            if len(batch) > 0:
                process_fn(batch)

    print("Loading advertiser...")
    process_csv_batch("/input/dataset_advertiser/dataset.csv", process_advertiser_batch)
    print("Loading publisher...")
    process_csv_batch("/input/dataset_publisher/dataset.csv", process_publisher_batch)

    print("Calculating merged")
    cur.execute(
        f"CREATE TABLE merged AS SELECT * FROM advertiser a INNER JOIN publisher p ON a.matching_id = p.matching_id")
    print("Calculating merged done")

    all_audiences = -1

    cur.execute(
        f"CREATE TABLE overlap_all_advertiser AS SELECT {all_audiences} AS audience_type, COUNT(DISTINCT matching_id) AS advertiser_size FROM advertiser")
    cur.execute(
        f"CREATE TABLE overlap_all_overlap AS SELECT {all_audiences} AS audience_type, COUNT(DISTINCT matching_id) AS overlap_size FROM merged")
    cur.execute(
        f"CREATE TABLE overlap_all AS SELECT a.audience_type, advertiser_size, overlap_size FROM overlap_all_advertiser a INNER JOIN overlap_all_overlap o ON a.audience_type = o.audience_type")

    if audience_type is None:
        cur.execute(f"CREATE VIEW overlap AS SELECT * FROM overlap_all")
    else:
        cur.execute(
            f"CREATE TABLE advertiser_audience_type_count AS SELECT audience_type, COUNT(*) as advertiser_size FROM advertiser GROUP BY audience_type")
        cur.execute(
            f"CREATE VIEW merged_grouped AS SELECT audience_type, COUNT(*) as overlap_size FROM merged GROUP BY audience_type")
        cur.execute(
            f"CREATE TABLE overlap_by_audience AS SELECT a.audience_type, advertiser_size, overlap_size FROM advertiser_audience_type_count a LEFT JOIN merged_grouped m ON a.audience_type = m.audience_type")
        cur.execute(f"CREATE VIEW overlap AS SELECT * FROM overlap_all UNION ALL SELECT * FROM overlap_by_audience")

    def round(decimals, column, cast_type):
        if decimals < 0:
            mult = 10 ** (decimals * -1)
            return f"CAST((ROUND(CAST({column} AS FLOAT) / {mult}, 0) * {mult}) AS {cast_type})"
        else:
            return f"CAST(ROUND({column}, {decimals}) AS {cast_type})"

    advertiser_size_rounded = round(config["rounding_decimals_count"], "advertiser_size", "INTEGER")
    overlap_size_rounded = round(config["rounding_decimals_count"], "overlap_size", "INTEGER")
    cur.execute(
        f"CREATE VIEW overlap_rounded AS SELECT CASE WHEN o.audience_type = -1 THEN 'All audiences combined' ELSE a.audience_type END, {advertiser_size_rounded} as advertiser_size, {overlap_size_rounded} as overlap_size FROM overlap o LEFT JOIN audience_types a ON o.audience_type = a.rowid")

    con.commit()

    result = subprocess.run([
        'sqlite3',
        db_file,
        '-cmd',
        '.mode csv',
        '.separator ,',
        '.output /output/overlap.csv',
        'SELECT * FROM overlap_rounded',
        '.quit',
    ])
    if result.returncode != 0:
        raise Exception(f"sqlite3 export failed with exit code {result.returncode}")

    advertiser_number_of_audience_types = len(audience_type_map)
    publisher_number_of_segments = len(segment_map)
    advertiser_size_rounded = cur.execute(f"SELECT {advertiser_size_rounded} FROM overlap_all_advertiser").fetchone()[0]

    statistics = CalculateOverlapBasicStatistics(
        advertiser_size=advertiser_size_rounded,
        advertiser_number_of_audience_types=advertiser_number_of_audience_types,
        publisher_number_of_segments=publisher_number_of_segments
    )

    with open("/output/statistics.json", "w") as file:
        file.write(json.dumps(statistics))

    os.remove(db_file)

if __name__ == '__main__':
    with catch_safe_error():
        run()
