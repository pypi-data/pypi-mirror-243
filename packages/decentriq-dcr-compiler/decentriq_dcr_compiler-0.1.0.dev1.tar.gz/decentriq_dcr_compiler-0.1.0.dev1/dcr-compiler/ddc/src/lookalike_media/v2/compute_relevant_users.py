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

EMBEDDINGS_DATASET_PATH = "/input/ingest_embeddings/embeddings.db"

if __name__ == '__main__':
    use_embeddings = os.path.exists(EMBEDDINGS_DATASET_PATH)

    with catch_safe_error():
        dq.compute_relevant_users(
            db_path="/output/relevant_users.db",
            output_dir="/output",
            segments_path="/input/ingest_segments/segments.db",
            embeddings_path=EMBEDDINGS_DATASET_PATH if use_embeddings else None,
        )