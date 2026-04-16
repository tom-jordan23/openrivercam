#!/usr/bin/env bash
#
# run_profile_test.sh — Automated camera profile A/B testing
#
# Cycles through camera streaming profiles, captures test videos for each,
# runs quality analysis, and produces a comparison report.
#
# Usage:
#   ./run_profile_test.sh                    # test all profiles
#   ./run_profile_test.sh --profiles a,b     # test specific profiles
#   ./run_profile_test.sh --captures 5       # 5 captures per profile (default: 10)
#   ./run_profile_test.sh --roi 200,100,1600,900  # focus analysis on water ROI
#   ./run_profile_test.sh --dry-run          # show what would happen
#
# Prerequisites:
#   - Camera reachable and orc-capture working
#   - camtool.py configured with credentials
#   - video_quality_test.py and dependencies installed
#   - Python with opencv-python-headless and numpy
#
# Output:
#   tests/<timestamp>/
#     baseline/       — captured videos + quality report
#     profile-a/      — captured videos + quality report
#     profile-b/      — captured videos + quality report
#     ...
#     comparison.txt  — side-by-side comparison of all profiles
#
# Run this AFTER the camera is mounted and aimed at the water.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SPRING_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
CAMERA_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
DOCS_VENV="$SPRING_DIR/docs/.venv"
CAMTOOL="$CAMERA_DIR/camtool.py"
QUALITY_TOOL="$SCRIPT_DIR/video_quality_test.py"
ORC_CAPTURE="/usr/local/bin/orc-capture"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_DIR="$SPRING_DIR/tests/camera_profiles_${TIMESTAMP}"

NUM_CAPTURES=10
ROI=""
DRY_RUN=0
PROFILES_TO_TEST="baseline,a,b"
CAMERA_NAME=""  # auto-detect from hostname
SETTLE_TIME=15  # seconds to wait after profile push for camera to adjust
MIN_BITRATE=""  # override orc-capture MIN_BITRATE_KBPS (e.g., for bench testing)

# ─── Parse arguments ─────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
    case "$1" in
        --profiles)     PROFILES_TO_TEST="$2"; shift 2 ;;
        --captures)     NUM_CAPTURES="$2"; shift 2 ;;
        --roi)          ROI="$2"; shift 2 ;;
        --camera)       CAMERA_NAME="$2"; shift 2 ;;
        --min-bitrate)  MIN_BITRATE="$2"; shift 2 ;;
        --dry-run)      DRY_RUN=1; shift ;;
        --help|-h)
            sed -n '2,/^$/p' "$0" | sed 's/^# \?//'
            exit 0
            ;;
        *) echo "Unknown argument: $1"; exit 1 ;;
    esac
done

# Auto-detect camera name from hostname
if [ -z "$CAMERA_NAME" ]; then
    STATION=$(hostname | sed 's/^orc-//')
    CAMERA_NAME="${STATION}-cam1"
fi

# Python — prefer venv if available (profiles venv > docs venv > system)
PY="python3"
[ -x "$DOCS_VENV/bin/python3" ] && PY="$DOCS_VENV/bin/python3"
[ -x "$SCRIPT_DIR/.venv/bin/python3" ] && PY="$SCRIPT_DIR/.venv/bin/python3"

# ─── Helpers ─────────────────────────────────────────────────────
log()  { echo "$(date '+%H:%M:%S') [profile-test] $1"; }
err()  { echo "$(date '+%H:%M:%S') [profile-test] ERROR: $1" >&2; }

run() {
    if [ "$DRY_RUN" -eq 1 ]; then
        echo "  DRY RUN: $*"
    else
        "$@"
    fi
}

# ─── Profile definitions ────────────────────────────────────────

declare -A PROFILE_CONFIGS
PROFILE_CONFIGS=(
    [baseline]="$CAMERA_DIR/common/streaming_101.xml"
    [a]="$SCRIPT_DIR/profile-a/streaming_101.xml"
    [b]="$SCRIPT_DIR/profile-b/streaming_101.xml"
    [c]="$SCRIPT_DIR/profile-c/streaming_101.xml"
    [e]="$SCRIPT_DIR/profile-e/streaming_101.xml"
)

declare -A PROFILE_DESCRIPTIONS
PROFILE_DESCRIPTIONS=(
    [baseline]="Baseline: 1080p, 16 Mbps CBR, H.264"
    [a]="Profile A: 1080p, 20 Mbps CBR, H.264, shorter GOP"
    [b]="Profile B: 720p, 20 Mbps CBR, H.264 (max bits/pixel)"
    [c]="Profile C: 1080p, 20 Mbps CBR, H.264 (SD card recording — bypasses RTSP)"
    [e]="Profile E: 1080p, 12 Mbps CBR, H.265 (~20 Mbps H.264 equivalent)"
)

declare -A PROFILE_CAPTURE_OVERRIDES
# Profile B needs different quality gate resolution
PROFILE_CAPTURE_OVERRIDES=(
    [b]="EXPECTED_WIDTH=1280 EXPECTED_HEIGHT=720"
)

declare -A PROFILE_CAPTURE_METHOD
# Profile C records to camera SD card instead of RTSP pull
PROFILE_CAPTURE_METHOD=(
    [c]="sdcard"
)

# ─── Validation ──────────────────────────────────────────────────

log "Camera profile A/B test"
log "Camera: $CAMERA_NAME"
log "Profiles: $PROFILES_TO_TEST"
log "Captures per profile: $NUM_CAPTURES"
log "Output: $OUTPUT_DIR"
[ -n "$ROI" ] && log "ROI: $ROI"
[ -n "$MIN_BITRATE" ] && log "Min bitrate override: ${MIN_BITRATE} kbps"
echo ""

# Check dependencies
for tool in "$CAMTOOL" "$QUALITY_TOOL" "$ORC_CAPTURE"; do
    if [ ! -f "$tool" ]; then
        err "Required tool not found: $tool"
        exit 1
    fi
done

if [ "$DRY_RUN" -eq 0 ]; then
    mkdir -p "$OUTPUT_DIR"
fi

# ─── Run tests ───────────────────────────────────────────────────

IFS=',' read -ra PROFILES <<< "$PROFILES_TO_TEST"

for profile in "${PROFILES[@]}"; do
    profile=$(echo "$profile" | xargs)  # trim whitespace

    config="${PROFILE_CONFIGS[$profile]:-}"
    desc="${PROFILE_DESCRIPTIONS[$profile]:-Profile $profile}"

    if [ -z "$config" ]; then
        err "Unknown profile: $profile"
        continue
    fi

    if [ ! -f "$config" ]; then
        err "Config file not found: $config"
        continue
    fi

    log "━━━ Testing: $desc ━━━"
    profile_dir="$OUTPUT_DIR/$profile"
    run mkdir -p "$profile_dir"

    # Push camera config
    log "Pushing config: $(basename "$config")"
    run "$PY" "$CAMTOOL" --profile-dir "$CAMERA_DIR" push "$CAMERA_NAME" --config "$config" 2>/dev/null || {
        err "Failed to push config for profile $profile"
        continue
    }

    # Wait for camera to adjust
    log "Waiting ${SETTLE_TIME}s for camera to settle..."
    [ "$DRY_RUN" -eq 0 ] && sleep "$SETTLE_TIME"

    # Capture videos
    overrides="${PROFILE_CAPTURE_OVERRIDES[$profile]:-}"
    capture_method="${PROFILE_CAPTURE_METHOD[$profile]:-rtsp}"
    for i in $(seq 1 "$NUM_CAPTURES"); do
        log "  Capture $i/$NUM_CAPTURES (method: $capture_method)"
        if [ "$DRY_RUN" -eq 0 ]; then
            if [ "$capture_method" = "sdcard" ]; then
                # SD card recording via camtool record
                output_file="$profile_dir/capture_$(printf '%03d' "$i").mp4"
                "$PY" "$CAMTOOL" --profile-dir "$CAMERA_DIR" \
                    record "$CAMERA_NAME" \
                    --duration 5 \
                    --output "$output_file" \
                    --timeout 60 || {
                    err "  SD card capture failed"
                }
            else
                # RTSP capture via orc-capture
                # Build a per-profile temp config that applies all overrides.
                # We can't use env vars because orc-capture.conf overwrites them.
                capture_conf="/tmp/orc-capture-test-${profile}-$$.conf"
                cp /etc/orc-capture.conf "$capture_conf"
                [ -n "$MIN_BITRATE" ] && sed -i "s/^MIN_BITRATE_KBPS=.*/MIN_BITRATE_KBPS=$MIN_BITRATE/" "$capture_conf"
                # Apply per-profile overrides (e.g., EXPECTED_WIDTH=1280)
                for kv in $overrides; do
                    key="${kv%%=*}"
                    val="${kv#*=}"
                    sed -i "s/^${key}=.*/${key}=${val}/" "$capture_conf"
                done
                ORC_CAPTURE_CONF="$capture_conf" "$ORC_CAPTURE" --skip-relay 2>&1 | tail -1

                # Move the captured file to profile directory
                latest=$(ls -t /home/pi/Videos/*.mp4 2>/dev/null | head -1)
                if [ -n "$latest" ]; then
                    mv "$latest" "$profile_dir/"
                else
                    err "  No video file produced"
                fi
            fi

            # Brief pause between captures
            sleep 2
        fi
    done

    # Run quality analysis
    log "Analyzing captures..."
    if [ "$DRY_RUN" -eq 0 ]; then
        roi_flag=""
        [ -n "$ROI" ] && roi_flag="--roi $ROI"

        "$PY" "$QUALITY_TOOL" "$profile_dir"/*.mp4 --compare $roi_flag \
            > "$profile_dir/quality_report.txt" 2>&1 || true

        log "Report: $profile_dir/quality_report.txt"
    fi

    echo ""
done

# ─── Restore baseline config ────────────────────────────────────

log "Restoring baseline camera config..."
run "$PY" "$CAMTOOL" --profile-dir "$CAMERA_DIR" push "$CAMERA_NAME" --config "${PROFILE_CONFIGS[baseline]}" 2>/dev/null || true

# ─── Cross-profile comparison ────────────────────────────────────

if [ "$DRY_RUN" -eq 0 ] && [ ${#PROFILES[@]} -gt 1 ]; then
    log "Generating cross-profile comparison..."

    # Collect one representative video from each profile (median bitrate)
    compare_files=()
    for profile in "${PROFILES[@]}"; do
        profile=$(echo "$profile" | xargs)
        profile_dir="$OUTPUT_DIR/$profile"
        # Pick the middle file alphabetically (rough median by timestamp)
        mid_file=$(ls "$profile_dir"/*.mp4 2>/dev/null | sort | awk "NR==$(( (NUM_CAPTURES + 1) / 2 ))")
        if [ -n "$mid_file" ]; then
            compare_files+=("$mid_file")
        fi
    done

    if [ ${#compare_files[@]} -gt 1 ]; then
        roi_flag=""
        [ -n "$ROI" ] && roi_flag="--roi $ROI"

        "$PY" "$QUALITY_TOOL" "${compare_files[@]}" --compare $roi_flag \
            > "$OUTPUT_DIR/comparison.txt" 2>&1

        log "Cross-profile comparison: $OUTPUT_DIR/comparison.txt"
        echo ""
        cat "$OUTPUT_DIR/comparison.txt"
    fi
fi

# ─── Summary ─────────────────────────────────────────────────────

echo ""
log "━━━ Test complete ━━━"
log "Results: $OUTPUT_DIR"
log ""
log "Next steps:"
log "  1. Review quality reports in each profile directory"
log "  2. Check cross-profile comparison: $OUTPUT_DIR/comparison.txt"
log "  3. For the best profiles, create ORC-OS video configurations"
log "     and run actual velocity processing to validate"
log "  4. Decision: keep camera, change profile, or replace camera"
