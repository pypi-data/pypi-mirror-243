import json
import os

from decentriq_util.error import catch_safe_error

INPUT_DIR = "/input"
OUTPUT_DIR = "/output"

MODELLED_AUDIENCE_INSIGHTS_DIR = os.path.join(INPUT_DIR, "modelled_audience_insights")
INPUT_SEGMENTS_PATH = os.path.join(MODELLED_AUDIENCE_INSIGHTS_DIR, "segments.json")
ACTIVATED_AUDIENCES_CONFIG_PATH = os.path.join(INPUT_DIR, "activated_audiences.json")
OUTPUT_SEGMENTS_PATH = os.path.join(OUTPUT_DIR, "segments.json")


if __name__ == '__main__':
    with catch_safe_error():
        published_activated_audiences = set([])
        if os.path.exists(ACTIVATED_AUDIENCES_CONFIG_PATH) and os.path.getsize(ACTIVATED_AUDIENCES_CONFIG_PATH) > 0:
            with open(ACTIVATED_AUDIENCES_CONFIG_PATH, "r") as f:
                config = json.load(f)
                for audience in config["activated_audiences"]:
                    if audience.get("is_published", False):
                        published_activated_audiences.add(
                            (audience["audience_type"], audience["reach"])
                        )

        filtered_audiences = []
        with open(INPUT_SEGMENTS_PATH, "r") as f:
            segments_config = json.load(f)
            for audience in segments_config["audiences"]:
                audience_type = audience["audience_type"]
                reach = audience["reach"]
                audience_reach = (audience_type, reach)
                if audience_reach in published_activated_audiences:
                    filtered_audiences.append(audience)

        with open(OUTPUT_SEGMENTS_PATH, "w") as f:
            f.write(json.dumps({
                "audiences": filtered_audiences
            }))
# Output files:
# - /output/segments.json
# {
#     "audiences": [
#         {
#             "audience_type": "credit_card",
#             "reach": 22,
#             "aggregations": [
#                 {
#                     "id": "abc1",
#                     "aggregation": [
#                         {
#                             "column": "age",
#                             "possible_values": [
#                                 "20-30",
#                                 "30-40",
#                                 "50-60"
#                              ]
#                         }
#                     ],
#                     "audience_type": "credit_card",
#                     "columns": [
#                         "age",
#                         "affinity_ratio",
#                         "share_in_overlap",
#                         "share_in_addressable_audience",
#                         "addressable_audience_size",
#                         "count_users_overlap"
#                     ],
#                     "rows": [
#                       [ "20-30", 1.0, 1.0, 0.0, 1.0, 1 ]
#                     ]
#                 },
#                 ...
#             ]
#         }
#     ]
# }
