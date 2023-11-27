# Output files:
#
# - /output/activated_audiences.json
# {
#     "advertiser_manifest_hash": "4d4bb3b62340e97b41e92de177f4f6c8a2ac4b595677df75891e60a449c00cfc",
#     "activated_audiences": [
#         {
#             "audience_type": "credit_card",
#             "reach": 22,
#             "is_published": true
#         },
#         {
#             "audience_type": "mortgage",
#             "reach": 25,
#             "is_published": false
#         }
#     ]
# }
import json
import os

INPUT_CONFIG_PATH = "/input/activated_audiences.json"


if __name__ == '__main__':
    with open("/output/activated_audiences.json", "w") as output_file:
        if os.path.exists(INPUT_CONFIG_PATH) and os.path.getsize(INPUT_CONFIG_PATH) > 0:
            with open(INPUT_CONFIG_PATH, "r") as input_file:
                config = json.load(input_file)
                output_file.write(json.dumps({
                    "advertiser_manifest_hash": config.get("advertiser_manifest_hash"),
                    "activated_audiences": config.get("activated_audiences", []),
                }))
        else:
            output_file.write(json.dumps({
                "advertiser_manifest_hash": None,
                "activated_audiences": []
            }))
