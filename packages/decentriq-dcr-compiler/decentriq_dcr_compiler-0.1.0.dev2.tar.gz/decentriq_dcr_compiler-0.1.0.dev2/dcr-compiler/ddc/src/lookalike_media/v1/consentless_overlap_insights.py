import tarfile
import sys
import os

PACKAGE = "dq_media_dcr-0.2.0"
tar = tarfile.open(f"/input/{PACKAGE}.tar.gz")
tar.extractall(f"/tmp")
tar.close()
sys.path.append(f"/tmp/{PACKAGE}")

import dq_media_dcr as dq
from decentriq_util.error import catch_safe_error

OUTPUT_DIR = "/output"
DB_PATH = "/output/db.db"

ROUND_FLOATS_TO = 3
ROUND_COUNTS_TO = 100
MIN_POSTMATCH_POSTROUND_SEGMENT_SIZE = 100
MIN_OVERLAP_SIZE_IN_STATISTICS = 150


if __name__ == '__main__':
    with catch_safe_error():
        demographics_dataset_path = "/input/ingest_demographics/demographics.db"

        use_demographics = os.path.exists(demographics_dataset_path)

        dq.prepare_advertiser_data(
            db_path=DB_PATH,
            output_dir=OUTPUT_DIR,
            matching_path="/input/ingest_matching_info/matching.db",
        )

        dq.compute_data_insights(
            db_path=DB_PATH,
            output_dir=OUTPUT_DIR,
            matching_path="/input/ingest_matching_info/matching.db",
            segments_path="/input/ingest_segments/segments.db",
            relevant_users_path="/input/compute_relevant_users/relevant_users.db",
            demographics_path=demographics_dataset_path if use_demographics else None,
            round_counts_to=ROUND_COUNTS_TO,
            round_floats_to=ROUND_FLOATS_TO,
            min_postmatch_postround_segment_size=MIN_POSTMATCH_POSTROUND_SEGMENT_SIZE,
            min_overlap_size_in_statistics=MIN_OVERLAP_SIZE_IN_STATISTICS,
            drop_na_segments=True,
            store_results_as_csv=False,
        )

    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
