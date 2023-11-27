# For each defined (audience, reach)-tuple, create a separate list of users
# based on all scored users out of the publisher's dataset.
#
# Output files:
#
# - /output/activated_audience_users.json
# {
#     "activated_audiences": [
#         {
#             "audience_type": "credit_card",
#             "reach": 22,
#             "users_file": "users_001.csv",
#         },
#         {
#             "audience_type": "mortgage",
#             "reach": 30,
#             "users_file": "users_002.csv",
#         }
#     ]
# }
#
# - /output/users_001.csv
# user01
# user02
# user03
# user04
#
# - /output/users_002.csv
# user01
# user02
# user03
# user04
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
        dq.create_activated_audiences(
            output_dir="/output",
            scored_users_dir="/input/score_users",
            activated_audiences_path="/input/activated_audiences.json"
        )