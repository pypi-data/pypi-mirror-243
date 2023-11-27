#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

(
cd "$SCRIPT_DIR"

rm -rf output
mkdir -p output

MEMORY=${MEMORY:-256M}
INPUT=${INPUT:-./input_sqlite}
PY=${PY:-v3/direct_activation.py}

for input in $INPUT
do
  echo "Running test $input"
  docker run --rm -it \
    --memory="${MEMORY}" \
    --memory-swap="${MEMORY}" \
    -v "$PWD/$input":/input \
    -v "$PWD/../../src/media/$PY":/direct_activation.py \
    -v "$PWD/output":/output \
    -e INCLUDE_CONTAINER_LOGS_ON_ERROR=true\
    base-image \
    python3 /direct_activation.py
done

)
