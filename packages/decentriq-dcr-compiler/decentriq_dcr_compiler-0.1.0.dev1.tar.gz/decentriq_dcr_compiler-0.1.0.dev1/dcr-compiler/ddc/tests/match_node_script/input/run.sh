#!/usr/bin/env bash

set -x

rm -r /output/*
cd /input
poetry install && poetry run python3 match.py
