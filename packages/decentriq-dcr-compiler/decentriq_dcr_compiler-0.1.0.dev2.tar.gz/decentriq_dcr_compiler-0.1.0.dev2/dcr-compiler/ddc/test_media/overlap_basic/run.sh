#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

(
cd "$SCRIPT_DIR"

rm -rf output
mkdir -p output

MEMORY=${MEMORY:-1024M}
INPUT=${INPUT:-./input_matching}

for input in $INPUT
do
  echo "Running test $input"

    docker run --rm -it \
      --memory="${MEMORY}" \
      --memory-swappiness=0 \
      --memory-swap="${MEMORY}" \
      -v "$PWD/$input":/input \
      -v "$PWD/../../src/media/v3/overlap_basic.py":/overlap_basic.py \
      -v "/home/exfalso/mount/against":/output \
      -e INCLUDE_CONTAINER_LOGS_ON_ERROR=true \
      base-image \
      python3 -m cProfile -o /output/profile.prof /overlap_basic.py
done

)
