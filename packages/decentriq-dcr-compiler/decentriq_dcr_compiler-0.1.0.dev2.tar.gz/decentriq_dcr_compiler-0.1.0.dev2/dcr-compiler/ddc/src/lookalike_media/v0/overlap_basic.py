# Compute overlap between publisher and advertiser users.
#
# Output files:
#
# - /output/overlap.json
# {
#     "audience_types": [
#         {
#             "audience_type": "credit_card",
#             "advertiser_size": 2,
#             "overlap_size": 2
#         },
#         {
#             "audience_type": "holiday",
#             "advertiser_size": 1,
#             "overlap_size": 0
#         },
#         {
#             "audience_type": "investing",
#             "advertiser_size": 1,
#             "overlap_size": 0
#         }
#     ]
# }
#
# - /output/overlap.db
import tarfile
import sys
import os

PACKAGE = "dq_media_dcr-0.1.0"
tar = tarfile.open(f"/input/{PACKAGE}.tar.gz")
tar.extractall(f"/tmp")
tar.close()
sys.path.append(f"/tmp/{PACKAGE}")

import dq_media_dcr as dq
from decentriq_util.error import catch_safe_error

DB_PATH = "/output/overlap.db"

if __name__ == '__main__':
    with catch_safe_error():
        dq.overlap.compute_overlap(
           DB_PATH,
           round_counts_to=100,
           relevant_users_path="/input/compute_relevant_users/relevant_users.db",
           matching_path="/input/ingest_matching_info/matching.db",
           output_dir="/output"
        )
