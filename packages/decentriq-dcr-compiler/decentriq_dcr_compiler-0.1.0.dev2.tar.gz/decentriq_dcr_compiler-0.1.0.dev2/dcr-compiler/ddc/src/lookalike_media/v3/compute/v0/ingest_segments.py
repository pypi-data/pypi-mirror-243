import tarfile
import sys

PACKAGE = "dq_media_dcr-0.3.0"
tar = tarfile.open(f"/input/{PACKAGE}.tar.gz")
tar.extractall(f"/tmp")
tar.close()
sys.path.append(f"/tmp/{PACKAGE}")

import dq_media_dcr as dq
from decentriq_util.error import catch_safe_error

if __name__ == '__main__':
    with catch_safe_error():
        dq.ingest_segments(
            output_dir="/output",
            csv_path="/input/segments",
        )