import tarfile
import sys
import os

PACKAGE = "dq_media_dcr-0.3.0"
tar = tarfile.open(f"/input/{PACKAGE}.tar.gz")
tar.extractall(f"/tmp")
tar.close()
sys.path.append(f"/tmp/{PACKAGE}")

import dq_media_dcr as dq
from decentriq_util.error import catch_safe_error

DB_PATH = "/output/db.db"
DEMOGRAPHICS_DATASET_PATH = "/input/ingest_demographics/demographics.db"
EMBEDDINGS_DATASET_PATH = "/input/ingest_embeddings/embeddings.db"


if __name__ == '__main__':
    use_demographics = os.path.exists(DEMOGRAPHICS_DATASET_PATH)
    use_embeddings = os.path.exists(EMBEDDINGS_DATASET_PATH)

    with catch_safe_error():
        dq.score_users(
            DB_PATH,
            output_dir="/output",
            relevant_users_path="/input/compute_relevant_users/relevant_users.db",
            segments_path="/input/ingest_segments/segments.db",
            matching_db_path="/input/ingest_matching/matching.db",
            embeddings_path=EMBEDDINGS_DATASET_PATH if use_embeddings else None,
            demographics_path=DEMOGRAPHICS_DATASET_PATH if use_demographics else None,
            merged_db_path="/input/overlap_basic/overlap.db",
        )
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
