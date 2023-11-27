# Compute all audiences sizes per reach level.
#
# Output files:
#
# - /output/audience_sizes.json
# {
#     "audience_sizes": [
#         {
#             "audience_type": str,
#             "audience_sizes": [
#                 {
#                     "reach": int,
#                     "size": int
#                 },
#                 ...
#             ]
#         }
# }
import tarfile
import sys

PACKAGE = "dq_media_dcr-0.1.0"
tar = tarfile.open(f"/input/{PACKAGE}.tar.gz")
tar.extractall(f"/tmp")
tar.close()
sys.path.append(f"/tmp/{PACKAGE}")

import dq_media_dcr as dq
from decentriq_util.error import catch_safe_error


if __name__ == '__main__':
    with catch_safe_error():
        dq.compute_audience_sizes(
            scored_users_dir="/input/score_users",
            output_dir="/output"
        )