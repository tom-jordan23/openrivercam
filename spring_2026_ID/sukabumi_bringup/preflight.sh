#!/usr/bin/env bash
# preflight.sh — read-only validation before running bringup.sh
#
# Checks: tooling, input files, station services, current state,
# recent captures, duty-cycle / maintenance mode, disk space,
# LiveORC upload config.
#
# Exit codes:  0 = all good or warnings only ; 1 = blockers present
#
# Usage:
#   ./preflight.sh                       # default (localhost API)
#   ./preflight.sh http://other.host/api # custom API base

set -uo pipefail   # NOT -e: we want to continue past failed checks

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib.sh"

# Allow API_BASE override as positional arg
[[ $# -ge 1 ]] && API_BASE="$1"

COOKIE_JAR="$(mktemp -t orc_preflight.XXXXXX)"
trap 'rm -f "$COOKIE_JAR"' EXIT

echo "${C_BOLD}=== PREFLIGHT — Sukabumi station bringup ===${C_RESET}"
echo "  date:     $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "  host:     $(hostname)"
echo "  api_base: $API_BASE"

# --- Required tooling -------------------------------------------------------
section "Required tooling"
require_cmd curl       || true
require_cmd python3    || true
require_cmd sqlite3    || true
require_cmd jq         && true || warn "jq missing (optional — python3 used as fallback)"

# --- Input files ------------------------------------------------------------
section "Input files"
validate_camera_config_json    || true
validate_cross_section_geojson || true
if [[ -f "$ENV_FILE" ]]; then
    if [[ -s "$ENV_FILE" ]]; then ok ".env present (non-empty)"
    else bad ".env present but empty"; fi
else
    bad ".env missing: $ENV_FILE — create with one line containing the API password"
fi

# --- Station services -------------------------------------------------------
section "Station services"
if curl -sS --max-time 5 "$API_BASE/" >/dev/null 2>&1 \
   || curl -sS --max-time 5 "$API_BASE/camera_config/" >/dev/null 2>&1; then
    ok "ORC-OS API reachable at $API_BASE"
else
    bad "ORC-OS API NOT reachable at $API_BASE  (is the orc-api container up?)"
fi

if [[ -f "$ORC_DB" ]]; then
    db_size=$(stat -c%s "$ORC_DB" 2>/dev/null || stat -f%z "$ORC_DB" 2>/dev/null || echo "?")
    ok "ORC-OS DB present: $ORC_DB (${db_size} bytes)"
else
    warn "ORC-OS DB not at $ORC_DB — only the API path will be verified, not the DB"
fi

# Auth login (only if .env was OK)
if [[ -s "$ENV_FILE" ]]; then
    if api_login; then ok "auth login succeeded (cookie set)"
    else bad "auth login failed — bringup will not work"
    fi
fi

# --- Current state ----------------------------------------------------------
section "Current state on station"
echo "Existing camera_configs:"
show_existing_camera_configs || true
echo "Existing cross_sections:"
show_existing_cross_sections || true
echo "video_config.id=1:"
show_video_config 1 || true

# --- Recent captures --------------------------------------------------------
section "Recent captures"
INCOMING="$HOME/.ORC-OS/uploads/incoming"
VIDEOS="$HOME/.ORC-OS/uploads/videos"
if [[ -d "$INCOMING" ]]; then
    n_in=$(ls "$INCOMING" 2>/dev/null | wc -l)
    latest_in=$(ls -1t "$INCOMING" 2>/dev/null | head -n1 || true)
    if [[ -n "$latest_in" ]]; then
        latest_age=$(( $(date +%s) - $(stat -c%Y "$INCOMING/$latest_in" 2>/dev/null || echo 0) ))
        ok "uploads/incoming: $n_in file(s); newest = $latest_in ($((latest_age/60)) min old)"
    else
        warn "uploads/incoming: empty (no fresh captures — may need to wait for a wake)"
    fi
else
    warn "uploads/incoming dir not found: $INCOMING"
fi
if [[ -d "$VIDEOS" ]]; then
    n_done=$(find "$VIDEOS" -maxdepth 3 -name '*.nc' 2>/dev/null | wc -l)
    note "uploads/videos: $n_done .nc artifact(s) under processed videos"
fi

# --- Duty cycle / maintenance mode -----------------------------------------
section "Duty cycle / maintenance mode"
if command -v orc-maintenance-check >/dev/null 2>&1; then
    mc_out=$(sudo -n /usr/local/bin/orc-maintenance-check 2>&1 || true)
    if echo "$mc_out" | grep -qiE 'maintenance|disabled|paused'; then
        ok "orc-maintenance-check reports maintenance state in effect:"
        echo "    $mc_out" | sed 's/^/    /'
    elif echo "$mc_out" | grep -qiE 'production|active|running'; then
        warn "orc-maintenance-check reports PRODUCTION mode (duty cycle active)"
        warn "  → enable maintenance mode via orc-pmi-stations GitHub Actions before bringup,"
        warn "    OR plan to finish this session before the next Witty Pi sleep window"
    else
        warn "orc-maintenance-check returned: $mc_out"
    fi
else
    warn "orc-maintenance-check not found — duty-cycle status unknown"
fi

# Witty Pi next-sleep estimate (if wp5 present)
if command -v wp5 >/dev/null 2>&1; then
    note "Witty Pi installed — check 'wp5' menu (option 6) for current schedule before starting"
fi

# --- Disk space -------------------------------------------------------------
section "Disk space"
df_home=$(df -h "$HOME" 2>/dev/null | awk 'NR==2 {print $4 " free of " $2 " on " $6}')
if [[ -n "$df_home" ]]; then
    ok "$df_home"
else
    warn "could not query disk usage at $HOME"
fi
df_uploads=$(df -h "$HOME/.ORC-OS" 2>/dev/null | awk 'NR==2 {print $4 " free of " $2 " on " $6}')
[[ -n "$df_uploads" ]] && note ".ORC-OS volume: $df_uploads"

# --- LiveORC upload config --------------------------------------------------
section "LiveORC upload config"
if [[ -f "$ORC_DB" ]]; then
    liveorc_settings=$(sqlite3 "$ORC_DB" "
        SELECT key || '=' || COALESCE(value, '') FROM settings
        WHERE key LIKE '%liveorc%' OR key LIKE '%liveSite%' OR key LIKE '%upload%'
        ORDER BY key;
    " 2>/dev/null || true)
    if [[ -n "$liveorc_settings" ]]; then
        echo "  settings entries (key=value):"
        echo "$liveorc_settings" | sed 's/^/    /'
    fi
    # Hessel's API stores institution/project in different schema versions; try a few.
    for table in liveorc_config institution project; do
        rows=$(sqlite3 "$ORC_DB" "SELECT count(*) FROM $table;" 2>/dev/null || true)
        [[ -n "$rows" && "$rows" != "0" ]] && note "$table table has $rows row(s)"
    done
fi
note "Verify last successful upload after a Process run by tailing 'docker compose logs orcapi'"

# --- Summary ----------------------------------------------------------------
echo
echo "${C_BOLD}=== Summary ===${C_RESET}"
printf "  ${C_GREEN}✓${C_RESET} %d passed   ${C_YELLOW}⚠${C_RESET} %d warning(s)   ${C_RED}✗${C_RESET} %d blocker(s)\n" \
    "$PASS" "$WARN" "$FAIL"

if (( FAIL > 0 )); then
    echo
    echo "${C_RED}Preflight FAILED — fix blockers above before running bringup.sh${C_RESET}"
    exit 1
fi
if (( WARN > 0 )); then
    echo
    echo "${C_YELLOW}Preflight passed with warnings — review them, then:${C_RESET}"
    echo "  ./bringup.sh"
    exit 0
fi
echo
echo "${C_GREEN}Preflight clean — ready to run:${C_RESET}"
echo "  ./bringup.sh"
exit 0
