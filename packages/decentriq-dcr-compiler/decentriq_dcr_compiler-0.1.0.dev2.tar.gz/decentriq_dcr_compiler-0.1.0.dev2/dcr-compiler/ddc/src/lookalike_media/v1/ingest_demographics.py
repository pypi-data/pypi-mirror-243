import os
import tarfile
import sys

PACKAGE = "dq_media_dcr-0.2.0"
tar = tarfile.open(f"/input/{PACKAGE}.tar.gz")
tar.extractall(f"/tmp")
tar.close()
sys.path.append(f"/tmp/{PACKAGE}")

import dq_media_dcr as dq
from decentriq_util.error import catch_safe_error

DEMOGRAPHICS_PATH="/input/demographics"

if __name__ == '__main__':
    with catch_safe_error():
        has_demographics = os.path.exists(DEMOGRAPHICS_PATH) and os.path.getsize(DEMOGRAPHICS_PATH) > 0
        if has_demographics:
            dq.ingest_demographics(
                output_dir="/output",
                csv_path=DEMOGRAPHICS_PATH
            )
