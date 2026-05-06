#!/usr/bin/env bash
# bringup.sh — apply the Sukabumi salvage CameraConfig + cross-section to the
# deployed station's ORC-OS, then wire video_config.id=1 to the new IDs.
#
# Each step verifies before continuing. On any failure, automatically rolls back.
# A state file is written to ./state/<timestamp>.json so --rollback can recover
# from a crash mid-run.
#
# Usage:
#   ./bringup.sh                          # apply (will roll back on error)
#   ./bringup.sh --no-link                # apply but skip the video_config PATCH
#   ./bringup.sh --rollback               # undo the most recent run (latest state file)
#   ./bringup.sh --rollback STATE_FILE    # undo a specific run
#   ./bringup.sh --keep-state             # don't delete state file on success
#   ./bringup.sh API_BASE                 # custom API base (positional)
#
# Notes:
#   - Run preflight.sh first. This script also re-runs the input-file checks.
#   - DO NOT open the camera_config edit form in the dashboard between this
#     script and your Process run — see ISS-FIELD-003.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib.sh"

LINK_VIDEO_CONFIG=1
VIDEO_CONFIG_ID="${VIDEO_CONFIG_ID:-1}"
KEEP_STATE=0
ROLLBACK=0
ROLLBACK_STATE_FILE=""
POSITIONAL_ARG=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --no-link)       LINK_VIDEO_CONFIG=0; shift ;;
        --keep-state)    KEEP_STATE=1; shift ;;
        --rollback)
            ROLLBACK=1
            shift
            if [[ $# -gt 0 && "$1" != --* ]]; then
                ROLLBACK_STATE_FILE="$1"; shift
            fi
            ;;
        --video-config-id) VIDEO_CONFIG_ID="$2"; shift 2 ;;
        -h|--help)
            sed -n '2,21p' "$0"; exit 0 ;;
        *)
            if [[ -z "$POSITIONAL_ARG" ]]; then POSITIONAL_ARG="$1"; shift
            else die "unknown argument: $1"; fi ;;
    esac
done
[[ -n "$POSITIONAL_ARG" ]] && API_BASE="$POSITIONAL_ARG"

mkdir -p "$STATE_DIR"

COOKIE_JAR="$(mktemp -t orc_bringup.XXXXXX)"
trap 'rm -f "$COOKIE_JAR"' EXIT

# ---------- helpers used by both apply and rollback ----------

require_login() {
    api_login || die "auth login failed — check $ENV_FILE"
}

state_set() {
    # state_set FILE KEY VALUE  (VALUE treated as JSON literal)
    local f="$1" key="$2" val="$3"
    python3 - "$f" "$key" "$val" <<'PY'
import json, sys, os
path, key, val = sys.argv[1], sys.argv[2], sys.argv[3]
d = {}
if os.path.exists(path):
    try: d = json.load(open(path))
    except Exception: d = {}
try: d[key] = json.loads(val)
except Exception: d[key] = val
json.dump(d, open(path, "w"), indent=2)
PY
}

state_get() {
    local f="$1" key="$2"
    [[ -f "$f" ]] || { echo ""; return; }
    python3 - "$f" "$key" <<'PY'
import json, sys
path, key = sys.argv[1], sys.argv[2]
try: d = json.load(open(path))
except Exception: print(""); sys.exit(0)
v = d.get(key, "")
if v is None: print(""); sys.exit(0)
if isinstance(v, (dict, list)): print(json.dumps(v))
else: print(v)
PY
}

# ---------- ROLLBACK PATH ----------

do_rollback() {
    section "ROLLBACK"
    if [[ -z "$ROLLBACK_STATE_FILE" ]]; then
        ROLLBACK_STATE_FILE=$(ls -1t "$STATE_DIR"/*.json 2>/dev/null | head -n1 || true)
    fi
    [[ -n "$ROLLBACK_STATE_FILE" && -f "$ROLLBACK_STATE_FILE" ]] \
        || die "no state file to roll back (looked in $STATE_DIR)"
    note "Reading state: $ROLLBACK_STATE_FILE"
    cat "$ROLLBACK_STATE_FILE" | sed 's/^/    /'

    require_login

    local rb_fail=0  # track rollback-specific failures, separate from apply-side $FAIL

    # Revert video_config first (so it stops referencing soon-deleted records)
    local prev cc_new xs_new
    prev=$(state_get "$ROLLBACK_STATE_FILE" "video_config_previous")
    if [[ -n "$prev" && "$prev" != "{}" ]]; then
        local target_id
        target_id=$(state_get "$ROLLBACK_STATE_FILE" "video_config_id_modified")
        [[ -z "$target_id" ]] && target_id="$VIDEO_CONFIG_ID"
        local s
        s=$(curl -sS -b "$COOKIE_JAR" -X PATCH \
                "$API_BASE/video_config/$target_id/" \
                -H 'Content-Type: application/json' \
                -d "$prev" -o /tmp/rb_vc.json -w "%{http_code}")
        if [[ "$s" =~ ^2 ]]; then ok "reverted video_config.id=$target_id"
        else bad "PATCH revert returned HTTP $s — see /tmp/rb_vc.json"; rb_fail=$((rb_fail+1)); fi
    else
        note "no video_config change recorded — nothing to revert"
    fi

    cc_new=$(state_get "$ROLLBACK_STATE_FILE" "camera_config_id_created")
    if [[ -n "$cc_new" ]]; then
        local s
        s=$(curl -sS -b "$COOKIE_JAR" -X DELETE \
                "$API_BASE/camera_config/$cc_new/" \
                -o /tmp/rb_cc.json -w "%{http_code}")
        if [[ "$s" =~ ^2 ]]; then ok "deleted camera_config.id=$cc_new"
        else bad "DELETE camera_config.id=$cc_new returned HTTP $s"; rb_fail=$((rb_fail+1)); fi
    fi

    xs_new=$(state_get "$ROLLBACK_STATE_FILE" "cross_section_id_created")
    if [[ -n "$xs_new" ]]; then
        local s
        s=$(curl -sS -b "$COOKIE_JAR" -X DELETE \
                "$API_BASE/cross_section/$xs_new/" \
                -o /tmp/rb_xs.json -w "%{http_code}")
        if [[ "$s" =~ ^2 ]]; then ok "deleted cross_section.id=$xs_new"
        else bad "DELETE cross_section.id=$xs_new returned HTTP $s"; rb_fail=$((rb_fail+1)); fi
    fi

    if (( rb_fail == 0 )); then
        mv "$ROLLBACK_STATE_FILE" "${ROLLBACK_STATE_FILE%.json}.rolled-back.json"
        echo
        echo "${C_GREEN}Rollback complete.${C_RESET}"
        # Caller decides whether to exit 0 or propagate apply failure
        if (( ROLLBACK )); then exit 0; fi
        return 0
    else
        echo
        echo "${C_RED}Rollback completed with errors ($rb_fail) — inspect /tmp/rb_*.json${C_RESET}"
        if (( ROLLBACK )); then exit 1; fi
        return 1
    fi
}

if (( ROLLBACK )); then do_rollback; fi

# ---------- APPLY PATH ----------

# Re-validate inputs (preflight covered this but apply is the system-of-record).
section "Re-validating inputs"
validate_camera_config_json || die "camera_config.json is invalid — see preflight.sh"
validate_cross_section_geojson || die "cross_section.geojson is invalid — see preflight.sh"
[[ -s "$ENV_FILE" ]] || die "$ENV_FILE missing or empty"

section "Connecting"
require_login
ok "logged in to $API_BASE"

# Open state file BEFORE any mutation
TS=$(date -u +%Y%m%dT%H%M%SZ)
STATE_FILE="$STATE_DIR/$TS.json"
echo "{}" > "$STATE_FILE"
state_set "$STATE_FILE" "started_at" "\"$TS\""
state_set "$STATE_FILE" "api_base"   "\"$API_BASE\""
state_set "$STATE_FILE" "video_config_id_modified" "$VIDEO_CONFIG_ID"
note "state file: $STATE_FILE"

# Capture current video_config for rollback BEFORE changing anything
section "Recording prior video_config.id=$VIDEO_CONFIG_ID"
prev_vc=$(api_get "/video_config/$VIDEO_CONFIG_ID/") || die "GET video_config/$VIDEO_CONFIG_ID failed"
prev_compact=$(echo "$prev_vc" | python3 -c "
import sys, json
d = json.load(sys.stdin)
out = {k: d.get(k) for k in ('camera_config_id', 'cross_section_id', 'cross_section_wl_id')}
print(json.dumps(out))
")
state_set "$STATE_FILE" "video_config_previous" "$prev_compact"
echo "  $prev_compact"

# --- Step 1: POST camera_config -------------------------------------------
section "POST /camera_config/from_file/"
CC_RESP=/tmp/bringup_cc.json
status=$(curl -sS -b "$COOKIE_JAR" \
    -X POST "$API_BASE/camera_config/from_file/" \
    -H "Content-Type: multipart/form-data" \
    -F "file=@$CC_FILE" \
    -o "$CC_RESP" -w "%{http_code}")
if [[ ! "$status" =~ ^(200|201)$ ]]; then
    bad "POST returned HTTP $status — body in $CC_RESP"
    cat "$CC_RESP" >&2
    do_rollback || true
    exit 1
fi
CC_NEW_ID=$(python3 -c "import json; print(json.load(open('$CC_RESP'))['id'])")
state_set "$STATE_FILE" "camera_config_id_created" "$CC_NEW_ID"
ok "new camera_config id=$CC_NEW_ID  (HTTP $status)"

# --- Step 2: verify h_ref persisted ---------------------------------------
section "Verify camera_config h_ref persisted"
db_h_ref=""
if [[ -f "$ORC_DB" ]]; then
    db_h_ref=$(db_camera_config_h_ref "$CC_NEW_ID" 2>/dev/null || true)
fi
api_h_ref=$(api_get "/camera_config/$CC_NEW_ID/" \
    | python3 -c "import sys,json; print(json.load(sys.stdin).get('data',{}).get('gcps',{}).get('h_ref'))")
ok "API reports h_ref=$api_h_ref"
[[ -n "$db_h_ref" ]] && ok "DB  reports h_ref=$db_h_ref"
match=$(python3 -c "
import sys
api='$api_h_ref'; expected=$EXPECTED_H_REF
try: print('YES' if abs(float(api) - expected) < 0.001 else 'NO')
except: print('NO')")
if [[ "$match" != "YES" ]]; then
    bad "h_ref mismatch! expected $EXPECTED_H_REF, got $api_h_ref"
    note "Doing automatic rollback…"
    ROLLBACK_STATE_FILE="$STATE_FILE"; do_rollback
    exit 1
fi

# --- Step 3: POST cross_section -------------------------------------------
section "POST /cross_section/"
XS_RESP=/tmp/bringup_xs.json
XS_BODY=$(python3 -c "
import json
fc = json.load(open('$XS_FILE'))
print(json.dumps({'name': 'sukabumi_XS_main_line', 'features': fc}))
")
status=$(curl -sS -b "$COOKIE_JAR" \
    -X POST "$API_BASE/cross_section/" \
    -H "Content-Type: application/json" \
    -d "$XS_BODY" \
    -o "$XS_RESP" -w "%{http_code}")
if [[ ! "$status" =~ ^(200|201)$ ]]; then
    bad "POST returned HTTP $status — body in $XS_RESP"
    cat "$XS_RESP" >&2
    ROLLBACK_STATE_FILE="$STATE_FILE"; do_rollback
    exit 1
fi
XS_NEW_ID=$(python3 -c "import json; print(json.load(open('$XS_RESP'))['id'])")
state_set "$STATE_FILE" "cross_section_id_created" "$XS_NEW_ID"
ok "new cross_section id=$XS_NEW_ID  (HTTP $status)"

# --- Step 4: verify CRS landed --------------------------------------------
section "Verify cross_section CRS"
xs_check=$(api_get "/cross_section/$XS_NEW_ID/" | python3 -c "
import sys, json
d = json.load(sys.stdin)
fc = d.get('features') or {}
crs = (fc.get('crs') or {}).get('properties', {}).get('name', '')
n = len(fc.get('features') or [])
ok = 'YES' if '$EXPECTED_CRS' in crs and n >= 4 else 'NO'
print(f'{ok}|{n}|{crs}')")
xs_ok="${xs_check%%|*}"; xs_rest="${xs_check#*|}"
xs_n="${xs_rest%%|*}"; xs_crs="${xs_rest#*|}"
if [[ "$xs_ok" == "YES" ]]; then
    ok "$xs_n features, CRS=$xs_crs"
else
    bad "CRS mismatch or too few features ($xs_n features, CRS=$xs_crs)"
    ROLLBACK_STATE_FILE="$STATE_FILE"; do_rollback
    exit 1
fi

# --- Step 5: PATCH video_config (optional) --------------------------------
if (( LINK_VIDEO_CONFIG )); then
    section "PATCH /video_config/$VIDEO_CONFIG_ID/"
    body=$(python3 -c "
import json
print(json.dumps({
    'camera_config_id': $CC_NEW_ID,
    'cross_section_id': $XS_NEW_ID,
    'cross_section_wl_id': $XS_NEW_ID,
}))")
    status=$(curl -sS -b "$COOKIE_JAR" -X PATCH \
        "$API_BASE/video_config/$VIDEO_CONFIG_ID/" \
        -H 'Content-Type: application/json' \
        -d "$body" \
        -o /tmp/bringup_vc.json -w "%{http_code}")
    if [[ ! "$status" =~ ^2 ]]; then
        bad "PATCH returned HTTP $status — body in /tmp/bringup_vc.json"
        cat /tmp/bringup_vc.json >&2
        ROLLBACK_STATE_FILE="$STATE_FILE"; do_rollback
        exit 1
    fi
    ok "video_config.id=$VIDEO_CONFIG_ID  (HTTP $status)"

    # Verify wiring + ready_to_run
    api_get "/video_config/$VIDEO_CONFIG_ID/" | python3 - <<PY
import sys, json
d = json.load(sys.stdin)
print(f"  camera_config_id   = {d.get('camera_config_id')}  (expected $CC_NEW_ID)")
print(f"  cross_section_id   = {d.get('cross_section_id')}  (expected $XS_NEW_ID)")
print(f"  cross_section_wl_id= {d.get('cross_section_wl_id')}  (expected $XS_NEW_ID)")
print(f"  ready_to_run       = {d.get('ready_to_run')}")
PY
else
    section "Skipping video_config PATCH (--no-link given)"
fi

# --- Done ------------------------------------------------------------------
echo
echo "${C_BOLD}=== Bringup complete ===${C_RESET}"
echo "  camera_config id: $CC_NEW_ID"
echo "  cross_section id: $XS_NEW_ID"
if (( LINK_VIDEO_CONFIG )); then
    echo "  video_config.id=$VIDEO_CONFIG_ID linked to new IDs"
fi
echo "  state file:       $STATE_FILE"
echo
echo "${C_BOLD}Next steps:${C_RESET}"
echo "  1) In the dashboard, open a recent video and click Process."
echo "     ⚠ DO NOT open the camera_config edit form — it will clobber h_ref"
echo "       (see ISS-FIELD-003 in spring_2026_ID/ISSUE_LOG.md)."
echo "  2) Watch logs:"
echo "       docker compose logs orcapi -f | grep -E 'water level|Process|transect|Error'"
echo "  3) Expect log line 'Water level set to 617.065 m.' — confirms h_ref took."
echo "  4) Verify a time_series row was created:"
echo "       sqlite3 \$HOME/.ORC-OS/orc-os.db \\"
echo "         'select id, video_id, q_50, v_av, fraction_velocimetry from time_series order by id desc limit 3'"
echo "  5) Verify LiveORC upload fired:"
echo "       docker compose logs orcapi --since 10m | grep -iE 'liveorc|upload'"
echo
echo "If anything goes wrong post-bringup:"
echo "  ./bringup.sh --rollback   # undoes this run"

if (( ! KEEP_STATE )); then
    note "state file kept at $STATE_FILE — pass to --rollback if you need to undo"
fi
exit 0
