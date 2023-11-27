# Compute overlap between publisher and advertiser users.
#
# Output files:
# - /output/overlap.db
import tarfile
import sys

PACKAGE = "dq_media_dcr-0.2.0"
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
           relevant_users_path="/input/compute_relevant_users/relevant_users.db",
           matching_path="/input/ingest_matching_info/matching.db",
           output_dir="/output"
        )
