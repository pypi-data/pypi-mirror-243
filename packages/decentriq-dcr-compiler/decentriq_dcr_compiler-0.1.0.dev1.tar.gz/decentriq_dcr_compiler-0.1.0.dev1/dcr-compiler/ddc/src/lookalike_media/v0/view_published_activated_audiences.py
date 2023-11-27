# Output files:
#
# - /output/activated_audiences.json
#
# {
#     "advertiser_manifest_hash": "4d4bb3b62340e97b41e92de177f4f6c8a2ac4b595677df75891e60a449c00cfc",
#     "activated_audiences": [
#         {
#             "audience_type": "credit_card",
#             "reach": 22,
#             "is_published": true
#         }
#     ]
# }
import json
import os

INPUT_CONFIG_PATH = "/input/activated_audiences.json"
OUTPUT_CONFIG_PATH = "/output/activated_audiences.json"


if __name__ == '__main__':
    if os.path.exists(INPUT_CONFIG_PATH) and os.path.getsize(INPUT_CONFIG_PATH) > 0:
        with open(INPUT_CONFIG_PATH, "r") as f:
            config = json.load(f)

        filtered_audiences = []
        for entry in config.get("activated_audiences", []):
            if entry.get("is_published", False):
                filtered_audiences.append(entry)

        with open(OUTPUT_CONFIG_PATH, "w") as f:
            f.write(json.dumps({
                "advertiser_manifest_hash": config.get("advertiser_manifest_hash"),
                "activated_audiences": filtered_audiences
            }))
    else:
        with open(OUTPUT_CONFIG_PATH, "w") as f:
            f.write(json.dumps({
                "advertiser_manifest_hash": None,
                "activated_audiences": []
            }))
