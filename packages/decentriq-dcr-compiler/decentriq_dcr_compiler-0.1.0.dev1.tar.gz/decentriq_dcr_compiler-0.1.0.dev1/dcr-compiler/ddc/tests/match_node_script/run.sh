#!/usr/bin/env bash
INPUT_DIR="$PWD/input"
INTERNAL_DIR="$PWD/internal"
OUTPUT_DIR="$PWD/output"

# Copy the matching script to the input folder
cp ../../src/data_science/scripts/match.py $INPUT_DIR

# Copy 'decentriq_utils' to the input folder
cp -r ../../../../trusted/python-libs/decentriq_util/ $INPUT_DIR

docker run --rm -v $INPUT_DIR:/input -v $INTERNAL_DIR:/internal -v $OUTPUT_DIR:/output matching_script:latest
