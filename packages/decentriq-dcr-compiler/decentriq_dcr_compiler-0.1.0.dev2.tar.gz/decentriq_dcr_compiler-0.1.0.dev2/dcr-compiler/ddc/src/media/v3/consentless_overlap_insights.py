import sqlite3
import json
from typing import TypedDict, List, cast, Optional
import sys
import subprocess
import os
import re
import base64
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

    column_name_validator_re = re.compile("^[-_:0-9a-zA-Z]*$")
    def validate_column_names(columns: List[str]):
        for column in columns:
            if column_name_validator_re.match(column) is None:
                raise Exception(f"Column name {column} contains unsupported characters")

    with open("/input/media_data_room_config.json", "r") as file:
        config: MediaDataRoomConfig = cast(MediaDataRoomConfig, json.loads(file.read()))

    validate_config(config)

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

    entire_overlap_str = "All audiences combined"
    entire_overlap = -1

    db_file = "/output/database.db"

    con = sqlite3.connect(db_file)
    cur = con.cursor()
    cur.execute("PRAGMA synchronous = OFF")
    cur.execute("PRAGMA journal_mode = OFF")
    cur.execute("PRAGMA temp_store_directory = '/output'")

    validate_column_names(config["advertiser_column_names"])
    validate_column_names(config["publisher_column_names"])
    advertiser_schema_sql = ", ".join(map(lambda name: f"\"{name}\"", config["advertiser_column_names"]))
    publisher_schema_sql = ", ".join(map(lambda name: f"\"{name}\"", config["publisher_column_names"]))

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


    cur.execute(f"CREATE VIEW advertiser_base AS SELECT DISTINCT \"{matching_column}\" AS matching_column, \"{audience_type}\" AS audience_type_str FROM advertiser_raw WHERE matching_column != ''")
    cur.execute(f"CREATE VIEW advertiser_audience_type_count_individual AS SELECT audience_type_str, COUNT(*) AS audience_type_count FROM advertiser_base GROUP BY audience_type_str")
    cur.execute(f"CREATE VIEW advertiser_audience_type_count_all AS SELECT '{entire_overlap_str}', COUNT(*) AS audience_type_count FROM advertiser_base")
    cur.execute(f"CREATE TABLE advertiser_audience_type_count AS SELECT CASE WHEN audience_type_str = '{entire_overlap_str}' THEN {entire_overlap} ELSE ROW_NUMBER() OVER (ORDER BY audience_type_str) END AS audience_type, audience_type_str, audience_type_count FROM (SELECT * FROM advertiser_audience_type_count_individual UNION ALL SELECT * FROM advertiser_audience_type_count_all)")
    cur.execute(f"CREATE INDEX advertiser_audience_type_count_index ON advertiser_audience_type_count(audience_type)")
    advertiser_audience_type_cutoff = config["cutoff_consentless_overlap_insights_unmatched_audience_type"]
    cur.execute(f"CREATE VIEW advertiser AS SELECT matching_column, c.audience_type FROM advertiser_base a INNER JOIN advertiser_audience_type_count c ON a.audience_type_str = c.audience_type_str WHERE audience_type_count >= {advertiser_audience_type_cutoff}")


    cur.execute(f"CREATE VIEW publisher_base AS SELECT DISTINCT \"{matching_column}\" AS matching_column, \"{segment}\" AS segment_str FROM publisher_raw WHERE matching_column != ''")
    cur.execute(f"CREATE TABLE publisher_segment_count AS SELECT ROW_NUMBER() OVER (ORDER BY segment_str) as segment, segment_str, COUNT(*) AS segment_count FROM publisher_base GROUP BY segment_str")
    cur.execute(f"CREATE INDEX publisher_segment_count_index ON publisher_segment_count(segment)")
    publisher_segment_cutoff = config["cutoff_consentless_overlap_insights_unmatched_segment"]
    cur.execute(f"CREATE TABLE publisher AS SELECT matching_column, c.segment FROM publisher_base p INNER JOIN publisher_segment_count c ON p.segment_str = c.segment_str WHERE segment_count >= {publisher_segment_cutoff}")
    cur.execute(f"CREATE INDEX publisher_index_matching_column ON publisher(matching_column)")
    # Create a separate id for each matching_column, needed for the accumulation algorithm at the end. This id can only
    # be used for that calculation, not for the advertiser-publisher join.
    cur.execute(f"CREATE TABLE publisher_matching_column_map AS SELECT matching_column, ROW_NUMBER() OVER (ORDER BY matching_column) AS matching_column_id FROM (SELECT DISTINCT matching_column FROM publisher)")


    cur.execute(f"CREATE TABLE matched_individual AS SELECT a.matching_column, audience_type, segment FROM advertiser a INNER JOIN publisher p ON a.matching_column = p.matching_column")
    cur.execute(f"CREATE VIEW matched_all AS SELECT DISTINCT matching_column, {entire_overlap} as audience_type, segment FROM matched_individual")
    cur.execute(f"CREATE TABLE matched AS SELECT * FROM matched_individual UNION ALL SELECT * FROM matched_all")


    cutoff = config["cutoff_consentless_overlap_insights_matched_audience_type"]
    cur.execute(f"CREATE TABLE matched_audience_type_count AS SELECT audience_type, CASE WHEN audience_type_count < {cutoff} THEN 0 ELSE audience_type_count END as audience_type_count FROM (SELECT audience_type, COUNT(*) AS audience_type_count FROM (SELECT DISTINCT audience_type, matching_column FROM matched) GROUP BY audience_type)")
    cur.execute(f"CREATE INDEX matched_audience_type_count_index ON matched_audience_type_count(audience_type)")

    cutoff = config["cutoff_consentless_overlap_insights_matched_segment_audience_type"]
    cur.execute(f"CREATE TABLE matched_segment_audience_type_count AS SELECT audience_type, segment, CASE WHEN segment_audience_type_count < {cutoff} THEN 0 ELSE segment_audience_type_count END as segment_audience_type_count FROM (SELECT audience_type, segment, COUNT(*) AS segment_audience_type_count FROM matched GROUP BY audience_type, segment)")
    cur.execute(f"CREATE INDEX matched_segment_audience_type_count_index ON matched_segment_audience_type_count(audience_type, segment)")

    total_publisher = cur.execute("SELECT COUNT(DISTINCT matching_column_id) FROM publisher_matching_column_map").fetchone()[0]

    cur.execute(f"CREATE VIEW audience_type_segment AS SELECT audience_type, segment FROM advertiser_audience_type_count CROSS JOIN publisher_segment_count")

    cur.execute(f"CREATE TABLE base_propensity AS SELECT segment, CAST(segment_count AS FLOAT) / {total_publisher} AS base_propensity FROM publisher_segment_count")
    cur.execute(f"CREATE TABLE overlap_propensity AS SELECT ats.audience_type, ats.segment, IFNULL(CAST(segment_audience_type_count AS FLOAT) / audience_type_count, 0) as overlap_propensity FROM matched_audience_type_count mac INNER JOIN matched_segment_audience_type_count msac ON mac.audience_type = msac.audience_type RIGHT JOIN audience_type_segment ats ON ats.audience_type = msac.audience_type AND ats.segment = msac.segment")
    cur.execute(f"CREATE TABLE net_propensity AS SELECT audience_type, o.segment, (overlap_propensity - base_propensity) / base_propensity AS net_propensity FROM base_propensity b INNER JOIN overlap_propensity o ON b.segment = o.segment")
    cur.execute(f"CREATE INDEX net_propensity_index_net_propensity ON net_propensity(net_propensity)")


    def round(decimals, column, cast_type):
        if decimals < 0:
            mult = 10 ** (decimals * -1)
            return f"CAST((ROUND(CAST({column} AS FLOAT) / {mult}, 0) * {mult}) AS {cast_type})"
        else:
            return f"CAST(ROUND({column}, {decimals}) AS {cast_type})"

    # This is a mouthful. The high-level imperative algo:
    # For each audience_type:
    #   1. Rank segments based on net_propensity
    #   2. Iterate each segment from highest to lowest net_propensity and calculate the accumulating count of
    #      matching ids per segment. BUT we need to do this in a way where we don't count ids that are present in
    #      multiple segments.
    # To do the above in SQL we first do a strange-looking operation where we GROUP BY based on
    # audience_type + *matching id*, and we choose the maximum net_propensity. This way for each audience_type we end
    # up with a single matching id which will be "counted first" because it has the highest net_propensity. Essentially
    # we do the deduplication *before* the accumulation. It is imperative that we use the INTEGER matching_column_id
    # here, as using the matching_column directly seems to cause some kind of computational blowup in sqlite.
    # Then we count each segment, but because of the first step we will only count "new" ids per segment, and then we
    # calculate the accumulating sum with a PARTITION BY.
    cur.execute(f"CREATE VIEW publisher_highest_propensity AS "
        "SELECT audience_type, p.segment, matching_column_id, MAX(net_propensity) AS net_propensity FROM publisher p "
        "INNER JOIN publisher_matching_column_map pm ON p.matching_column = pm.matching_column INNER JOIN net_propensity n ON p.segment = n.segment "
        "GROUP BY audience_type, matching_column_id")
    cur.execute(f"CREATE VIEW publisher_highest_propensity_count AS "
        "SELECT audience_type, segment, net_propensity, COUNT(matching_column_id) AS count "
        "FROM publisher_highest_propensity "
        "GROUP BY audience_type, segment")
    cur.execute(f"CREATE VIEW publisher_highest_propensity_count_acc AS "
        "SELECT audience_type, segment, SUM(count) OVER (PARTITION BY audience_type ORDER BY net_propensity DESC, segment) as accumulated_count "
        "FROM publisher_highest_propensity_count")

    cur.execute(f"CREATE VIEW propensity AS "
        f"SELECT n.audience_type, n.segment, base_propensity, overlap_propensity, net_propensity, CAST(accumulated_count AS FLOAT) / {total_publisher} AS accumulated_ratio, accumulated_count "
        f"FROM base_propensity b INNER JOIN overlap_propensity o ON b.segment = o.segment "
        f"INNER JOIN net_propensity n ON o.segment = n.segment AND o.audience_type = n.audience_type "
        f"INNER JOIN publisher_highest_propensity_count_acc p ON n.audience_type = p.audience_type AND n.segment = p.segment "
        f"ORDER BY n.audience_type, net_propensity DESC")

    cur.execute(f"CREATE TABLE propensity_rounded AS SELECT audience_type, segment_str, "
                + round(config["rounding_decimals_ratio"], "base_propensity", "FLOAT") + " AS base_propensity, "
                + round(config["rounding_decimals_ratio"], "overlap_propensity", "FLOAT") + " AS overlap_propensity, "
                + round(config["rounding_decimals_ratio"], "net_propensity", "FLOAT") + " AS net_propensity, "
                + round(config["rounding_decimals_ratio"], "accumulated_ratio", "FLOAT") + " AS accumulated_ratio, "
                + round(config["rounding_decimals_count"], "accumulated_count", "INTEGER") + " AS accumulated_count "
                + "FROM propensity p INNER JOIN publisher_segment_count c WHERE p.segment = c.segment")

    # We store the result of each audience_type in separate files, as we may have thousands of audience_types.
    audience_types_results = cur.execute(f"SELECT audience_type, audience_type_str FROM advertiser_audience_type_count").fetchall()
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
            f'SELECT segment_str, base_propensity, overlap_propensity, net_propensity, accumulated_ratio, accumulated_count FROM propensity_rounded WHERE audience_type = {audience_type}',
            '.quit',
        ])
        if result.returncode != 0:
            raise Exception(f"sqlite3 export failed with exit code {result.returncode}")


    os.remove(db_file)

if __name__ == '__main__':
    with catch_safe_error():
        run()
