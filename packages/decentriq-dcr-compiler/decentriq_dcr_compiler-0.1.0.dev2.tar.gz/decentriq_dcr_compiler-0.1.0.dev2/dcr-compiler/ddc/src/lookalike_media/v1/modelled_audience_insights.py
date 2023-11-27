import tarfile
import sys
import os

PACKAGE = "dq_media_dcr-0.2.0"
tar = tarfile.open(f"/input/{PACKAGE}.tar.gz")
tar.extractall(f"/tmp")
tar.close()
sys.path.append(f"/tmp/{PACKAGE}")

import dq_media_dcr as dq
from decentriq_util.error import catch_safe_error

INPUT_DIR = "/input"
OUTPUT_DIR = "/output"
DB_PATH = "/output/db.db"

ROUND_FLOATS_TO = 3
ROUND_COUNTS_TO = 100
MIN_POSTMATCH_POSTROUND_SEGMENT_SIZE = 100
MIN_OVERLAP_SIZE_IN_STATISTICS = 150

CREATED_AUDIENCES_DIR = os.path.join(INPUT_DIR, "create_activated_audiences")


if __name__ == '__main__':
    with catch_safe_error():
        demographics_dataset_path = "/input/ingest_demographics/demographics.db"

        use_demographics = os.path.exists(demographics_dataset_path)

        dq.prepare_advertiser_data_for_created_audiences(
            db_path=DB_PATH,
            output_dir=OUTPUT_DIR,
            created_audiences_dir=CREATED_AUDIENCES_DIR,
            created_audiences_config_path=os.path.join(CREATED_AUDIENCES_DIR, "activated_audience_users.json"),
        )

        dq.compute_data_insights(
            db_path=DB_PATH,
            output_dir=OUTPUT_DIR,
            segments_path="/input/ingest_segments/segments.db",
            relevant_users_path="/input/compute_relevant_users/relevant_users.db",
            demographics_path=demographics_dataset_path if use_demographics else None,
            round_counts_to=ROUND_COUNTS_TO,
            round_floats_to=ROUND_FLOATS_TO,
            min_postmatch_postround_segment_size=MIN_POSTMATCH_POSTROUND_SEGMENT_SIZE,
            min_overlap_size_in_statistics=MIN_OVERLAP_SIZE_IN_STATISTICS,
            drop_na_segments=True,
            store_results_as_csv=False,
        )

    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
# Output files:
# - /output/segments.json
# {
#     "audiences": [
#         {
#             "audience_type": "credit_card",
#             "reach": 0.22,
#             "aggregations": [
#                 {
#                     "id": "abc1",
#                     "aggregation": [
#                         {
#                             "column": "age",
#                             "possible_values": [
#                                 "20-30",
#                                 "30-40",
#                                 "50-60"
#                              ]
#                         }
#                     ],
#                     "audience_type": "credit_card",
#                     "columns": [
#                         "age",
#                         "affinity_ratio",
#                         "share_in_overlap",
#                         "share_in_addressable_audience",
#                         "addressable_audience_size",
#                         "count_users_overlap"
#                     ],
#                     "rows": [
#                       [ "20-30", 1.0, 1.0, 0.0, 1.0, 1 ]
#                     ]
#                 },
#                 {
#                     "id": "abc2",
#                     "aggregation": [
#                         {
#                             "column": "gender",
#                             "possible_values": [
#                                 "m",
#                                 "f"
#                              ]
#                         }
#                     ],
#                     "audience_type": "credit_card",
#                     "columns": [
#                         "gender",
#                         "affinity_ratio",
#                         "share_in_overlap",
#                         "share_in_addressable_audience",
#                         "addressable_audience_size",
#                         "count_users_overlap"
#                     ],
#                     "rows": [
#                         [ "f", 1.0, 1.0, 0.0, 1.0, 1 ]
#                     ]
#                 }
#             ]
#         }
#     ]
# }
