# Download a list of users for one of the generated audiences.
# This computation should only be executed by the publisher.
#
# Output files:
#
# - /output/audience_users.csv
# user01
# user02
# user03
# user04
import os
import json
import shutil
import tarfile
import sys

PACKAGE = "dq_media_dcr-0.1.0"
tar = tarfile.open(f"/input/{PACKAGE}.tar.gz")
tar.extractall(f"/tmp")
tar.close()
sys.path.append(f"/tmp/{PACKAGE}")

import dq_media_dcr as dq
from dq_media_dcr import MediaDcrError
from decentriq_util.error import catch_safe_error

# Config specifying which audiences are available.
INPUT_CONFIG_PATH = "/input/activated_audiences.json"
REQUESTED_AUDIENCE_PATH = "/input/requested_audience.json"

# Where to read the user list from.
AUDIENCE_USERS_DIR = "/input/create_activated_audiences"
AUDIENCE_USERS_CONFIG_PATH = os.path.join(AUDIENCE_USERS_DIR, "activated_audience_users.json")

OUTPUT_CSV_PATH = "/output/audience_users.csv"


if __name__ == '__main__':
    with catch_safe_error():
        with open(INPUT_CONFIG_PATH, "r") as f:
            config = json.load(f)
        with open(REQUESTED_AUDIENCE_PATH, "r") as f:
            requested_audience = json.load(f)
        with open(AUDIENCE_USERS_CONFIG_PATH, "r") as f:
            activated_users_config = json.load(f)
            user_list_by_audience_reach =  {
                (entry["audience_type"], entry["reach"]): os.path.join(AUDIENCE_USERS_DIR, entry["users_file"])
                for entry in activated_users_config["activated_audiences"]
            }

        activated_audiences = config["activated_audiences"]
        published_activated_audiences = set([])

        # Create a set of all published (audience, reach) tuples used
        # for checking whether the requested users list can be returned.
        for audience in activated_audiences:
            is_published = audience.get("is_published", False)
            audience_reach = (audience["audience_type"], audience["reach"])
            if is_published:
                published_activated_audiences.add(audience_reach)

        requested_audience_reach = (requested_audience["audienceType"], requested_audience["reach"])
        if requested_audience_reach in published_activated_audiences:
            users_path = user_list_by_audience_reach[requested_audience_reach]
            if os.path.exists(users_path):
                shutil.copyfile(users_path, OUTPUT_CSV_PATH)
            else:
                raise MediaDcrError.from_safe(f"No file '{users_path}' containing the requested audience users")
        else:
            raise MediaDcrError.from_safe("The requested (audience, reach) is not in the list of published audiences")
