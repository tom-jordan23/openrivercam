# Shared functions for preflight.sh and bringup.sh — sourced, not executed.
# Conventions:
#   - All functions return 0 on success, non-zero on failure.
#   - Output going to stdout is informational; errors go to stderr.
#   - Counters PASS / WARN / FAIL are global.

# ---------- color / output helpers ----------

if [[ -t 1 ]]; then
    C_GREEN=$'\033[32m'; C_YELLOW=$'\033[33m'; C_RED=$'\033[31m'
    C_BOLD=$'\033[1m'; C_DIM=$'\033[2m'; C_RESET=$'\033[0m'
else
    C_GREEN=""; C_YELLOW=""; C_RED=""; C_BOLD=""; C_DIM=""; C_RESET=""
fi

PASS=0
WARN=0
FAIL=0

ok()   { echo "  ${C_GREEN}✓${C_RESET} $*"; PASS=$((PASS+1)); }
warn() { echo "  ${C_YELLOW}⚠${C_RESET} $*"; WARN=$((WARN+1)); }
bad()  { echo "  ${C_RED}✗${C_RESET} $*"; FAIL=$((FAIL+1)); }
note() { echo "  ${C_DIM}·${C_RESET} $*"; }

section() { echo; echo "${C_BOLD}[$*]${C_RESET}"; }

die() { echo "${C_RED}ERROR:${C_RESET} $*" >&2; exit 1; }

# ---------- defaults / paths ----------

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA_DIR="${DATA_DIR:-$SCRIPT_DIR/data}"
STATE_DIR="${STATE_DIR:-$SCRIPT_DIR/state}"
ENV_FILE="${ENV_FILE:-$SCRIPT_DIR/.env}"
CC_FILE="${CC_FILE:-$DATA_DIR/camera_config.json}"
XS_FILE="${XS_FILE:-$DATA_DIR/cross_section.geojson}"
API_BASE="${API_BASE:-http://localhost:3001/api}"
ORC_DB="${ORC_DB:-$HOME/.ORC-OS/orc-os.db}"
EXPECTED_H_REF="${EXPECTED_H_REF:-617.065}"
EXPECTED_CRS="${EXPECTED_CRS:-EPSG:32748}"

# ---------- core helpers ----------

require_cmd() {
    local cmd="$1"
    if command -v "$cmd" >/dev/null 2>&1; then
        ok "$cmd: $(command -v "$cmd")"
    else
        bad "$cmd: NOT FOUND in PATH"
        return 1
    fi
}

api_login() {
    # Sets COOKIE_JAR (caller should mktemp + trap rm).
    # Uses the password in $ENV_FILE (one-line file, not KEY=VALUE).
    [[ -f "$ENV_FILE" ]] || { bad ".env not found: $ENV_FILE"; return 1; }
    local pw status body
    pw="$(head -n1 "$ENV_FILE" | tr -d '[:space:]')"
    [[ -n "$pw" ]] || { bad ".env empty or whitespace-only"; return 1; }
    body=$(mktemp)
    status=$(curl -sS --max-time 10 -c "$COOKIE_JAR" \
        -X POST "$API_BASE/auth/login/?password=$pw" \
        -o "$body" -w "%{http_code}" || echo "000")
    if [[ "$status" != "200" ]]; then
        bad "auth login failed (HTTP $status)"
        cat "$body" >&2
        rm -f "$body"
        return 1
    fi
    rm -f "$body"
    return 0
}

api_get() {
    # api_get PATH -> stdout = response body, return = 0 on 2xx
    local path="$1" body status
    body=$(mktemp)
    status=$(curl -sS --max-time 15 -b "$COOKIE_JAR" \
        "$API_BASE${path}" \
        -o "$body" -w "%{http_code}" || echo "000")
    cat "$body"
    rm -f "$body"
    [[ "$status" =~ ^2 ]]
}

# ---------- input file validation ----------

validate_camera_config_json() {
    [[ -f "$CC_FILE" ]] || { bad "camera_config.json missing: $CC_FILE"; return 1; }
    local report
    report=$(python3 - "$CC_FILE" "$EXPECTED_H_REF" <<'PY' 2>&1
import json, sys
path, expected_h_ref = sys.argv[1], float(sys.argv[2])
try:
    d = json.load(open(path))
except Exception as e:
    print(f"FAIL: not parseable JSON: {e}"); sys.exit(2)
problems = []
for k in ("height", "width", "gcps", "camera_matrix"):
    if k not in d: problems.append(f"missing top-level key '{k}'")
gcps = d.get("gcps") or {}
if "h_ref" not in gcps:
    problems.append("missing gcps.h_ref")
else:
    h = gcps["h_ref"]
    if abs(float(h) - expected_h_ref) > 0.001:
        problems.append(f"gcps.h_ref={h} (expected ~{expected_h_ref})")
n_src = len((gcps.get("src") or []))
n_dst = len((gcps.get("dst") or []))
if n_src != n_dst or n_src == 0:
    problems.append(f"gcps src/dst length mismatch or empty: src={n_src} dst={n_dst}")
elif n_src < 4:
    problems.append(f"only {n_src} GCPs (PnP needs >=4)")
if problems:
    print("FAIL: " + "; ".join(problems)); sys.exit(2)
print(f"OK: {d['width']}x{d['height']}, {n_src} GCPs, h_ref={gcps['h_ref']}")
PY
    )
    if [[ "$report" == OK:* ]]; then ok "camera_config.json: ${report#OK: }"; return 0
    else bad "camera_config.json: ${report#FAIL: }"; return 1
    fi
}

validate_cross_section_geojson() {
    [[ -f "$XS_FILE" ]] || { bad "cross_section.geojson missing: $XS_FILE"; return 1; }
    local report
    # Match "EPSG:32748" or "EPSG::32748" or "32748" anywhere in the CRS string
    # (different OGC URN / OGC URL / shorthand forms all serialize the same EPSG code).
    report=$(python3 - "$XS_FILE" "$EXPECTED_CRS" <<'PY' 2>&1
import json, sys, re
path, expected_crs = sys.argv[1], sys.argv[2]
try:
    d = json.load(open(path))
except Exception as e:
    print(f"FAIL: not parseable JSON: {e}"); sys.exit(2)
problems = []
if d.get("type") != "FeatureCollection":
    problems.append(f"top-level type is {d.get('type')!r}, expected 'FeatureCollection'")
n = len(d.get("features", []))
if n < 4:
    problems.append(f"only {n} features (cross-section needs many points)")
crs = (d.get("crs") or {}).get("properties", {}).get("name", "")
m = re.search(r'EPSG[:/]+(\d+)', crs) or re.search(r'(\b\d{4,5}\b)', crs)
expected_code = re.search(r'(\d{4,5})', expected_crs)
if not expected_code:
    problems.append(f"could not parse EXPECTED_CRS={expected_crs!r}")
elif not m or m.group(1) != expected_code.group(1):
    problems.append(f"CRS {crs!r} does not match expected EPSG:{expected_code.group(1)}")
if problems:
    print("FAIL: " + "; ".join(problems)); sys.exit(2)
print(f"OK: {n} features, CRS={crs}")
PY
    )
    if [[ "$report" == OK:* ]]; then ok "cross_section.geojson: ${report#OK: }"; return 0
    else bad "cross_section.geojson: ${report#FAIL: }"; return 1
    fi
}

# ---------- station state inspection ----------

show_existing_camera_configs() {
    local body
    body=$(api_get "/camera_config/") || { bad "GET /camera_config/ failed"; return 1; }
    echo "$body" | python3 - <<'PY'
import sys, json
ds = json.load(sys.stdin)
if not isinstance(ds, list):
    print(f"  (unexpected response: {ds})"); sys.exit(0)
print(f"  count: {len(ds)}")
for d in ds:
    h_ref = (d.get("data") or {}).get("gcps", {}).get("h_ref", "?")
    print(f"  id={d.get('id')}  name={d.get('name')!r}  h_ref={h_ref}  created={d.get('created_at')}")
PY
}

show_existing_cross_sections() {
    local body
    body=$(api_get "/cross_section/") || { bad "GET /cross_section/ failed"; return 1; }
    echo "$body" | python3 - <<'PY'
import sys, json
ds = json.load(sys.stdin)
if not isinstance(ds, list):
    print(f"  (unexpected response: {ds})"); sys.exit(0)
print(f"  count: {len(ds)}")
for d in ds:
    fc = d.get("features") or {}
    n = len(fc.get("features") or [])
    crs = (fc.get("crs") or {}).get("properties", {}).get("name", "—")
    print(f"  id={d.get('id')}  name={d.get('name')!r}  features={n}  crs={crs}")
PY
}

show_video_config() {
    local id="${1:-1}"
    local body
    body=$(api_get "/video_config/$id/") || { bad "GET /video_config/$id/ failed"; return 1; }
    echo "$body" | python3 - <<'PY'
import sys, json
d = json.load(sys.stdin)
keys = ("id", "name", "camera_config_id", "cross_section_id",
        "cross_section_wl_id", "ready_to_run")
for k in keys:
    print(f"  {k}: {d.get(k, '—')}")
PY
}

# ---------- DB-side verifiers (read-only sqlite reads) ----------

db_camera_config_h_ref() {
    local id="$1"
    [[ -f "$ORC_DB" ]] || { echo "(db missing)"; return 1; }
    sqlite3 "$ORC_DB" \
        "SELECT json_extract(data, '\$.gcps.h_ref') FROM camera_config WHERE id=$id;"
}
