import pandas as pd
import json
import os
import sys
import subprocess
import argparse
import shutil
from typing import List


NUM_ERRORS_RECORD_BY_KEY_TUPLE = 10


os.environ["RUST_BACKTRACE"] = "1"


parser = argparse.ArgumentParser(
    prog="Validation",
    description="Validation of input data"
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
    "-b", "--bin",
    help="Path to the validation program"
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


# Top-level "driver script" of the parallelized validation. Uses split to split the input
# into fixed-sized chunks and fifos for communication and to apply backpressure
run_sh = '''
#!/usr/bin/env bash
set -euo pipefail

BIN="$1"
CONFIG="$2"
INPUT="$3"
REPORT="$4"
TYPES="$5"
CHUNK_SIZE="$6"
WORKER_PY="$7"

# If the size of the input is small (<64M), run the validation in non-parallel mode
if [[ $(stat --printf="%s" "$INPUT") -lt $((64 * 1024 * 1024)) ]]
then
  "$BIN" "$CONFIG" "$INPUT" "$REPORT" "$TYPES"
  exit 0
fi

# First determine the parallelism based on nproc and the cgroup memory
if [[ -f /sys/fs/cgroup/memory.max ]]
then
  AVAILABLE_MEMORY=$(cat /sys/fs/cgroup/memory.max)
elif [[ -f /sys/fs/cgroup/memory/memory.limit_in_bytes ]]
then
  AVAILABLE_MEMORY=$(cat /sys/fs/cgroup/memory/memory.limit_in_bytes)
else
  echo "Cannot determine available memory"
  exit 1
fi

PARALLELISM_MEMORY=$((($AVAILABLE_MEMORY - 64 * 1024 * 1024) / (128 * 1024 * 1024 + $CHUNK_SIZE)))
PARALLELISM_CPU=$(($(nproc) - 1))
if [[ "$PARALLELISM_MEMORY" -gt "$PARALLELISM_CPU" ]]
then
  PARALLELISM="$PARALLELISM_CPU"
else
  PARALLELISM="$PARALLELISM_MEMORY"
fi
if [[ "$PARALLELISM" -gt 12 ]]
then
  PARALLELISM=12
fi
echo Parallelism is "$PARALLELISM"

# Create fifo queues.
# The task queue is consumed by filter.sh and used to provide backpressure to split so it doesn't "run ahead".
# The result queue is consumed by the final merge.sh
mkfifo /tmp/task
mkfifo /tmp/result
function cleanup {
  rm -f /tmp/task /tmp/result
}
exec 3<>/tmp/task
exec 4<>/tmp/result

for i in $(seq 1 "$PARALLELISM")
do
  echo "$BIN" "$CONFIG" >&3
done

bash /tmp/merge.sh "$REPORT" "$TYPES" "$WORKER_PY" &
MERGE_PID=$!

split -C "$CHUNK_SIZE" --filter="bash /tmp/filter.sh" "$INPUT"
CHUNK_COUNT=$(cat /tmp/chunk_count)
echo "chunk_count $CHUNK_COUNT" >&4

wait $MERGE_PID
'''


# Passed to split. Reads a task from the task fifo, dumps stdin to an input file, runs the validation program in the background
# return early to split, and then when processing is finished writes the next task to the task queue as well as writes
# to the result queue, to be processed by merge.sh.
# FD 3: task fifo
# FD 4: result fifo
filter_sh = '''
#!/usr/bin/env bash
set -euo pipefail

read -u 3 line
read -a task <<<"$line"

if [[ "$line" = "error" ]]
then
  exit 1
fi

BIN=${task[0]}
CONFIG=${task[1]}

if [[ -f /tmp/chunk_count ]]
then
  I=$(($(cat /tmp/chunk_count) + 1))
else
  I=1
fi
echo -n "$I" > /tmp/chunk_count

INPUT=/tmp/input_"$I".csv
OUTPUT=/tmp/output_"$I".json
TYPES=/tmp/types_"$I"
ROW_COUNT=/tmp/row_count_"$I"

cp /dev/stdin "$INPUT"

(
  function cleanup {
    rm -f "$INPUT"
  }
  trap cleanup EXIT
  function error {
    echo error >&3
    echo error >&4
  }
  trap error ERR
  "$BIN" "$CONFIG" "$INPUT" "$OUTPUT" "$TYPES"
  wc -l < "$INPUT" > "$ROW_COUNT"
  echo "result $OUTPUT $TYPES $ROW_COUNT" >&4
  echo "$BIN $CONFIG" >&3
) &
'''

# Merges individual validation results
merge_sh = '''
#!/usr/bin/env bash
set -euo pipefail

REPORT="$1"
TYPES_FINAL="$2"
WORKER_PY="$3"

WORKER_MODULE_NAME="$(basename ${WORKER_PY%.*})"
DONE=0
CHUNK_COUNT=
while ! [[ "$DONE" = "$CHUNK_COUNT" ]]
do
  read -u 4 line
  read -a result <<<"$line"
  if [[ "${result[0]}" = "chunk_count" ]]
  then
    CHUNK_COUNT=${result[1]}
    continue
  fi

  if [[ "${result[0]}" = "error" ]]
  then
    echo "Error during validation"
    exit 1
  fi

  OUTPUT=${result[1]}
  TYPES=${result[2]}
  ROW_COUNT=${result[3]}

  DONE=$(($DONE + 1))
  if [[ $(($DONE % 64)) -eq 0 ]]
  then
    echo Merge high=$DONE
    cd $(dirname "$WORKER_PY") && python3 -c "from $WORKER_MODULE_NAME import merge_result; merge_result()" "$DONE"
  fi
done
cd $(dirname "$WORKER_PY") && python3 -c "from $WORKER_MODULE_NAME import merge_result; merge_result()" "$DONE"
mv /tmp/merge_current "$REPORT"
# /tmp/merge_types may not exist if validation failed
if [[ -f /tmp/merge_types ]]
then
  mv /tmp/merge_types "$TYPES_FINAL"
fi
'''


# This may be called out of order, so we need to buffer until we "fill the holes". We do this by utilizing $DONE from
# merge.sh which indicates the "high watermark" of results, namely how many chunks have been processed.
# merge_result() then keeps a "low watermark" which indicates the last successfully merged chunk.
# On each call we process the outputs from low_watermark up until we have a "hole" or we reach the high_watermark.
def merge_result():
    high_watermark = int(sys.argv[1])
    if os.path.isfile("/tmp/merge_low_watermark"):
        with open("/tmp/merge_low_watermark", "r") as file:
            low_watermark = int(file.read())
    else:
        low_watermark = 0

    if os.path.isfile("/tmp/merge_row_offset"):
        with open("/tmp/merge_row_offset", "r") as file:
            row_offset = int(file.read())
    else:
        row_offset = 0

    if os.path.isfile("/tmp/merge_current"):
        with open("/tmp/merge_current", "r") as file:
            merge_current = json.load(file)
    else:
        merge_current = {
            "version": "v0",
            "report": {
                "columns": [],
                "schema": {
                    "recordedErrors": [],
                    "numErrorsTotal": 0,
                },
                "table": {
                    "recordedErrors": [],
                    "numErrorsTotal": 0,
                },
                "outcome": "PASSED",
                "numInvalidRowsTotal": 0,
            },
        }

    i = low_watermark
    for i in range(low_watermark, high_watermark):
        report_path = f"/tmp/output_{i + 1}.json"
        if os.path.isfile(report_path):
            with open(report_path, "r") as file:
                report_json = json.load(file)
            os.remove(report_path)
            row_count_path = f"/tmp/row_count_{i + 1}"
            with open(row_count_path) as file:
                row_count = int(file.read())
            os.remove(row_count_path)
            merge_current = merge_single(merge_current, report_json, row_offset)
            types_path = f"/tmp/types_{i + 1}"
            if os.path.isfile(types_path):
                shutil.copyfile(types_path, "/tmp/merge_types")
                os.remove(types_path)
            row_offset += row_count
        else:
            i -= 1
            break
    next_low_watermark = i + 1

    with open("/tmp/merge_low_watermark", "w") as file:
        file.write(str(next_low_watermark))
    with open("/tmp/merge_row_offset", "w") as file:
        file.write(str(row_offset))
    with open("/tmp/merge_current", "w") as file:
        json.dump(merge_current, file)


def dump_report(report):
    dump = {
        "columns": list(map(lambda column: {
            "column": column["column"],
            "recordedErrors": len(column["recordedErrors"]),
            "numErrorsTotal": column["numErrorsTotal"],
        }, report["report"]["columns"])),
        "schema": {
            "recordedErrors": len(report["report"]["schema"]["recordedErrors"]),
            "numErrorsTotal": report["report"]["schema"]["numErrorsTotal"],
        },
        "table": {
            "recordedErrors": len(report["report"]["table"]["recordedErrors"]),
            "numErrorsTotal": report["report"]["table"]["numErrorsTotal"],
        },
        "outcome": report["report"]["outcome"],
        "numInvalidRowsTotal": report["report"]["numInvalidRowsTotal"],
    }
    print(json.dumps(dump, indent=2))

def merge_single(report_current, report, row_offset):
    # Cell errors
    current_cell_error_count = 0
    for column in report_current['report']['columns']:
        current_cell_error_count += len(column['recordedErrors'])
    maximum_cell_errors = 499
    for column in report['report']['columns']:
        column_number = column['column']
        existing = [col for i, col in enumerate(report_current['report']['columns']) if col['column'] == column_number]

        if len(existing) == 0:
            column_to_add_to = {
                'column': column_number,
                'recordedErrors': [],
                'numErrorsTotal': 0,
            }
            report_current['report']['columns'].append(column_to_add_to)
        else:
            column_to_add_to = existing[0]
        added_error_count = min(len(column['recordedErrors']), maximum_cell_errors - current_cell_error_count)
        column_to_add_to['numErrorsTotal'] += column['numErrorsTotal']
        added_errors = column['recordedErrors'][:added_error_count]
        for error in added_errors:
            error['location']['row'] += row_offset
        column_to_add_to['recordedErrors'].extend(added_errors)
        current_cell_error_count += added_error_count

    # Schema errors
    maximum_schema_errors = 499
    added_error_count = min(len(report['report']['schema']['recordedErrors']), maximum_schema_errors - len(report_current['report']['schema']['recordedErrors']))
    added_errors = report['report']['schema']['recordedErrors'][:added_error_count]
    for error in added_errors:
        error['row'] += row_offset
    report_current['report']['schema']['recordedErrors'].extend(added_errors)
    report_current['report']['schema']['numErrorsTotal'] += report['report']['schema']['numErrorsTotal']

    # Table errors
    maximum_table_errors = 499
    added_error_count = min(len(report['report']['table']['recordedErrors']), maximum_table_errors - len(report_current['report']['table']['recordedErrors']))
    added_errors = report['report']['table']['recordedErrors'][:added_error_count]
    report_current['report']['table']['recordedErrors'].extend(added_errors)
    report_current['report']['table']['numErrorsTotal'] += report['report']['table']['numErrorsTotal']

    report_current['report']['outcome'] = "PASSED" if report_current['report']['outcome'] == "PASSED" and report['report']['outcome'] == "PASSED" else "FAILED"
    report_current['report']['numInvalidRowsTotal'] += report['report']['numInvalidRowsTotal']
    return report_current

if __name__ == "__main__":
    try:
        args = parser.parse_args()
        worker_py = sys.argv[0]

        with open("/tmp/run.sh", "w") as file:
            file.write(run_sh)
        with open("/tmp/filter.sh", "w") as file:
            file.write(filter_sh)
        with open("/tmp/merge.sh", "w") as file:
            file.write(merge_sh)

        # The command to run the validation program
        command = [ "bash" ]
        command += [
            "/tmp/run.sh",
            args.bin,
            args.config,
            args.input,
            args.report,
            args.types,
            str(64 * 1024 * 1024),
            worker_py,
        ]

        process = subprocess.run(
            command,
        )

        if process.returncode != 0:
            raise Exception(f"Validation command error")

        # Check whether we should detect duplicates and if yes, update the validation
        # report with the outcome.
        with open(args.config, "r") as f:
            config = json.load(f)["config"]
        if "uniqueness" in config.get("table", {}):
            unique_keys = config["table"]["uniqueness"]["uniqueKeys"]
            # Do not attempt to check for uniqueness in a file that might not exist or is empty
            # (as is the case for validation runs).
            is_file_non_empty = os.path.exists(args.input) and os.path.getsize(args.input) > 0
            if is_file_non_empty and unique_keys:
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
