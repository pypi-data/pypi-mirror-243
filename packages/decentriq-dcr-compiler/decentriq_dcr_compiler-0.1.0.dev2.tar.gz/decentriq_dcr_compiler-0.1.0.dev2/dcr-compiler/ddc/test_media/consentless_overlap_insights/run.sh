#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

(
cd "$SCRIPT_DIR"

rm -rf output
mkdir -p output

MEMORY=${MEMORY:-256M}
INPUT=${INPUT:-../overlap_basic/input_a_5mb}
PY=${PY:-v3/consentless_overlap_insights.py}

for input in $INPUT
do
  echo "Running test $input"
  docker run --rm -it \
    --memory="${MEMORY}" \
    --memory-swap="${MEMORY}" \
    -v "$PWD/$input":/input \
    -v "$PWD/../../src/media/$PY":/consentless_overlap_insights.py \
    -v "$PWD/output":/output \
    base-image \
    python3 /consentless_overlap_insights.py
done

)
