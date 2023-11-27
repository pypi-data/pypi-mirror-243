import os
import tarfile
import sys

PACKAGE = "dq_media_dcr-0.1.0"
tar = tarfile.open(f"/input/{PACKAGE}.tar.gz")
tar.extractall(f"/tmp")
tar.close()
sys.path.append(f"/tmp/{PACKAGE}")

import dq_media_dcr as dq
from decentriq_util.error import catch_safe_error

EMBEDDINGS_PATH = "/input/embeddings"

if __name__ == '__main__':
    with catch_safe_error():
        has_embeddings = os.path.exists(EMBEDDINGS_PATH) and os.path.getsize(EMBEDDINGS_PATH) > 0
        if has_embeddings:
            dq.ingest_embeddings(
                output_dir="/output",
                # Note that the embeddings file is not validated in the LAL DCR as we don't
                # know how many embeddings columns there are and it has already been validated as
                # part of the DataLab.
                csv_path=EMBEDDINGS_PATH
            )
