import pandas as pd
import json
import os
import sys
import subprocess
import argparse
import shutil
import copy
from typing import List


NUM_ERRORS_RECORD_BY_KEY_TUPLE = 10


os.environ["RUST_BACKTRACE"] = "1"


parser = argparse.ArgumentParser(
    prog="Validation",
    description="Validation of input data using WASM-based validation logic"
)
parser.add_argument(
    "-i", "--input",
    help="Path to the data to be validated"
)
parser.add_argument(
    "-c", "--config",
    help="Path to the validation config in JSON format"
)
parser.add_argument(
    "-w", "--wasm",
    help="Path to the validation program in WASM format"
)
parser.add_argument(
    "-o", "--output",
    help="Path to where the validated results should be stored"
)
parser.add_argument(
    "-r", "--report",
    help="Path to where the final report should be stored"
)
parser.add_argument(
    "-t", "--types",
    help="Path to where the types info file should be stored"
)


def find_duplicates(csv_path: str, unique_keys: List[List[int]]):
    """
    Try to find duplicates in the given CSV file and report the line
    numbers of where such duplicates where found.
    """
    csv = pd.read_csv(csv_path, header=None)
    csv.columns = range(csv.shape[1])
    errors = []
    num_duplicates_total = 0
    for keys in unique_keys:
        csv.columns = list(range(csv.shape[1]))
        subset_columns = keys["columns"]
        is_duplicated = csv.duplicated(subset=subset_columns)
        num_duplicates_total += sum(is_duplicated)
        duplicated_rows_subset = list(csv.index[is_duplicated][:NUM_ERRORS_RECORD_BY_KEY_TUPLE])
        for row in duplicated_rows_subset:
            errors.append({
                "code": "DUPLICATE_KEY",
                "location": {
                    "row": row,
                    "columns": subset_columns
                }
            })
    return num_duplicates_total, errors


if __name__ == "__main__":
    try:
        args = parser.parse_args()

        # Construct the list of directories that wasmtime is allowed
        # to read from/write to.
        paths = [
            args.input,
            args.config,
            args.wasm,
            args.output,
            args.report,
            args.types,
        ]
        required_dirs = set([os.path.dirname(p) for p in paths])
        required_dirs_args = sum([["--dir", d] for d in required_dirs], [])

        # The command to run the validation WASM using wasmtime
        command = [ "wasmtime" ]
        command += required_dirs_args
        command += [
            args.wasm,
            args.config,
            args.input,
            args.report,
            args.types,
        ]

        process = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        if process.returncode != 0:
            raise Exception(f"WASM validation error: {process.stderr}")

        # Check whether we should detect duplicates and if yes, update the validation
        # report with the outcome.
        with open(args.config, "r") as f:
            config = json.load(f)["config"]
        if "uniqueness" in config.get("table", {}):
            unique_keys = config["table"]["uniqueness"]["uniqueKeys"]
            if unique_keys:
                num_duplication_errors_total , duplication_errors = find_duplicates(args.input, unique_keys)
                with open(args.report, "r") as f:
                    report = json.load(f)
                report["report"]["uniqueness"] = {
                    "recordedErrors": duplication_errors,
                    "numErrorsTotal": num_duplication_errors_total
                }
                if num_duplication_errors_total and num_duplication_errors_total > 0:
                    report["report"]["outcome"] = "FAILED"
                with open(args.report, "w") as f:
                    json.dump(report, f, indent=2)

        # Simply copy over the input data so that downstream computations
        # can read it.
        shutil.copyfile(args.input, args.output)
    except Exception as e:
        raise e
