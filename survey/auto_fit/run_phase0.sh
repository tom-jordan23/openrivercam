#!/bin/bash
# Phase 0 ground-truth clicker — launches the matplotlib window for you
# to click each GCP on the pinned calibration frame.
#
# Run from any directory:
#   bash /Users/tjordan/code/git/openrivercam/survey/auto_fit/run_phase0.sh
# or from the repo root:
#   bash survey/auto_fit/run_phase0.sh

set -euo pipefail

REPO_ROOT="/Users/tjordan/code/git/openrivercam"
cd "$REPO_ROOT"

# shellcheck disable=SC1091
source .venv/bin/activate

python3 survey/auto_fit/ground_truth_click.py \
    --video spring_2026_ID/survey_data/source_data/20260420T034813.mp4 \
    --gcps spring_2026_ID/survey_data/output/gcps.csv \
    --camera-position spring_2026_ID/survey_data/output/camera_position.csv \
    --site sukabumi \
    --collected-by "Tom Jordan" \
    -o survey/tests/fixtures/sukabumi_gt_clicks_v1.json \
    "$@"
