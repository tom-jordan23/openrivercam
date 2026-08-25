#!/bin/bash
# verify-api-access.sh — prove what a non-owner institute member can and cannot
# do over the LiveORC REST API. Runs from any workstation; no host access.
#
# WHY
#   TODO-115 establishes the account model for read-only API access: a user who
#   is an institute Member but is not the `creator` of any record gets read on
#   the whole institute's data and 403 on every write. That is enforced upstream
#   by IsOwnerOrReadOnlyAsInstitute, so it needs no LiveORC change — but it is a
#   claim from source reading, and it is load-bearing for two things: the mirror
#   pull in TODO-114, and eventually partner access for IPB. This script is how
#   the claim gets proven against the running server instead of assumed.
#
#   It is deliberately reusable. TODO-115's last step is to re-run this same
#   matrix against one real IPB account before announcing access, because
#   institute membership is set by hand and is the only thing standing between
#   read-only and nothing.
#
# WHAT IT TOUCHES
#   By default: nothing. The default run is GET-only.
#
#   --probe-writes adds two probes that attempt writes and expect to be refused:
#     * PATCH with an empty body — a no-op even in the case where it is allowed.
#     * POST /api/video/ with a deliberately invalid payload. A 400 proves the
#       permission layer let the request through without creating anything; a
#       403 would mean it did not. TODO-115 is explicit that a REAL video must
#       never be posted to production to test this — that writes to the very
#       disk the whole media-volume workstream is about.
#
#   --probe-delete adds the DELETE probes. Read the warning below before using.
#
# THE DELETE PROBE IS THE ONE THAT CAN BITE
#   `DELETE /api/site/N/video/{id}/` returning 403 is, in TODO-115's words, "the
#   finding that matters". But the test and the risk are the same request: if
#   the permission model is NOT what we read, the probe deletes a production
#   video that exists in exactly one place.
#
#   So it is staged, and the staging is the safety mechanism:
#
#     1. Run the default GET-only pass. Confirms membership resolves and data
#        is readable.
#     2. Run --probe-writes. PATCH and DELETE are the SAME branch of
#        has_object_permission — both fall through to `obj.creator ==
#        request.user`. A 403 on PATCH therefore exercises the identical
#        predicate that gates DELETE, without being able to destroy anything.
#     3. Pull the TODO-114 mirror. Now every video exists in two places.
#     4. Only then run --probe-delete, against a video id you name explicitly
#        and have confirmed is in the mirror.
#
#   Steps 2 and 3 make step 4 cheap. Running --probe-delete before the mirror
#   exists is betting production data on a source reading.
#
# USAGE
#   export LIVEORC_EMAIL='mirror@…'
#   read -rs LIVEORC_PASSWORD && export LIVEORC_PASSWORD   # keeps it out of history
#
#   ./verify-api-access.sh --institute 1 --site 4                    # GET-only
#   ./verify-api-access.sh --institute 1 --site 4 --probe-writes     # + refused writes
#   ./verify-api-access.sh --institute 1 --site 4 \
#       --probe-delete --video-id 123                                # after the mirror
#
#   --foreign-site N   also probe a site the account is NOT a member of (expect 403)
#
# Safe to re-run. Never writes credentials to disk.

set -euo pipefail

BASE="${LIVEORC_BASE:-https://openrivercam.endlessprojects.info}"
INSTITUTE=""
SITE=""
FOREIGN_SITE=""
VIDEO_ID=""
PROBE_WRITES=0
PROBE_DELETE=0

PASS=0; FAIL=0; SKIP=0
RESULTS=()

die() { echo "ERROR: $*" >&2; exit 1; }

while [[ $# -gt 0 ]]; do
  case "$1" in
    --institute)    INSTITUTE="$2"; shift 2 ;;
    --site)         SITE="$2"; shift 2 ;;
    --foreign-site) FOREIGN_SITE="$2"; shift 2 ;;
    --video-id)     VIDEO_ID="$2"; shift 2 ;;
    --probe-writes) PROBE_WRITES=1; shift ;;
    --probe-delete) PROBE_DELETE=1; shift ;;
    --base)         BASE="$2"; shift 2 ;;
    -h|--help)      sed -n '2,60p' "$0"; exit 0 ;;
    *)              die "unknown argument: $1" ;;
  esac
done

[[ -n "$INSTITUTE" ]] || die "--institute is required (see TODO-115: GET /api/site/ returns [] without it)"
[[ -n "$SITE" ]]      || die "--site is required"
[[ -n "${LIVEORC_EMAIL:-}" ]]    || die "set LIVEORC_EMAIL"
[[ -n "${LIVEORC_PASSWORD:-}" ]] || die "set LIVEORC_PASSWORD"

if [[ $PROBE_DELETE -eq 1 && -z "$VIDEO_ID" ]]; then
  die "--probe-delete requires an explicit --video-id. Name the video you are
     willing to lose if the permission model is not what we read, and confirm
     it is present in the TODO-114 mirror first."
fi

# record_v VERDICT NAME EXPECTED ACTUAL — for rows whose pass condition is not a
# literal string match (e.g. "some sites were listed", where the ids vary).
record_v() {
  local verdict="$1" name="$2" expected="$3" actual="$4"
  if [[ "$verdict" == "PASS" ]]; then PASS=$((PASS+1)); else FAIL=$((FAIL+1)); fi
  printf '  %-4s %-46s expected %-12s got %s\n' "$verdict" "$name" "$expected" "$actual"
  RESULTS+=("$verdict|$name|$expected|$actual")
}

# record NAME EXPECTED ACTUAL  → tally and remember for the summary table
record() {
  local name="$1" expected="$2" actual="$3" verdict
  if [[ "$actual" == "$expected" ]]; then verdict="PASS"; PASS=$((PASS+1))
  else verdict="FAIL"; FAIL=$((FAIL+1)); fi
  printf '  %-4s %-46s expected %-12s got %s\n' "$verdict" "$name" "$expected" "$actual"
  RESULTS+=("$verdict|$name|$expected|$actual")
}

skip() {
  printf '  %-4s %-46s %s\n' "SKIP" "$1" "$2"
  SKIP=$((SKIP+1))
  RESULTS+=("SKIP|$1|-|$2")
}

# HTTP status only, with the bearer token
code() {
  local method="$1" url="$2"; shift 2
  curl -sS -m 45 -o /dev/null -w '%{http_code}' -X "$method" \
    -H "Authorization: Bearer $ACCESS" "$@" "$BASE$url"
}

# response body, with the bearer token
body() {
  local method="$1" url="$2"; shift 2
  curl -sS -m 45 -X "$method" -H "Authorization: Bearer $ACCESS" "$@" "$BASE$url"
}

echo
echo "LiveORC API access verification"
echo "  base      $BASE"
echo "  account   $LIVEORC_EMAIL"
echo "  institute $INSTITUTE   site $SITE"
echo

# --- version, unauthenticated -------------------------------------------------
# The permission analysis in TODO-115 was read against v0.3.0. If this has moved,
# the conclusions need re-checking against the new tag before they are trusted.
echo "Server"
VERSION_JSON="$(curl -sS -m 20 "$BASE/api/version/")"
echo "  $VERSION_JSON"
case "$VERSION_JSON" in
  *'"version":"0.3.0"'*) ;;
  *) echo "  WARNING: not v0.3.0 — TODO-115's source reading may no longer apply." ;;
esac
echo

# --- 1. token -----------------------------------------------------------------
echo "Authentication"
TOKEN_JSON="$(curl -sS -m 30 -X POST "$BASE/api/token/" \
  -H 'Content-Type: application/json' \
  -d "$(printf '{"email":%s,"password":%s}' \
        "$(printf '%s' "$LIVEORC_EMAIL"    | sed 's/\\/\\\\/g; s/"/\\"/g; s/^/"/; s/$/"/')" \
        "$(printf '%s' "$LIVEORC_PASSWORD" | sed 's/\\/\\\\/g; s/"/\\"/g; s/^/"/; s/$/"/')")" \
  || true)"

ACCESS="$(printf '%s' "$TOKEN_JSON" | sed -n 's/.*"access":"\([^"]*\)".*/\1/p')"
if [[ -z "$ACCESS" ]]; then
  record "POST /api/token/" "200 + access" "no token: $TOKEN_JSON"
  echo; echo "Cannot continue without a token."; exit 1
fi
record "POST /api/token/" "200 + access" "200 + access"

# Decode the JWT payload to answer TODO-115's open question about access
# lifetime — a long mirror pull will outlive one token if it is short.
PAYLOAD="$(printf '%s' "$ACCESS" | cut -d. -f2)"
case $(( ${#PAYLOAD} % 4 )) in 2) PAYLOAD="$PAYLOAD==" ;; 3) PAYLOAD="$PAYLOAD=" ;; esac
CLAIMS="$(printf '%s' "$PAYLOAD" | tr '_-' '/+' | base64 -d 2>/dev/null || true)"
EXP="$(printf '%s' "$CLAIMS" | sed -n 's/.*"exp":\([0-9]*\).*/\1/p')"
IAT="$(printf '%s' "$CLAIMS" | sed -n 's/.*"iat":\([0-9]*\).*/\1/p')"
if [[ -n "$EXP" && -n "$IAT" ]]; then
  echo "  access token lifetime: $(( (EXP - IAT) / 60 )) minutes"
  echo "  claims: $CLAIMS"
fi
echo

# --- 2-3. site listing and the ?institute= gotcha -----------------------------
echo "Site visibility"
SITES_BARE="$(body GET /api/site/)"
if [[ "$(printf '%s' "$SITES_BARE" | tr -d '[:space:]')" == "[]" ]]; then
  record "GET /api/site/ (no ?institute)" "[]" "[]"
else
  record "GET /api/site/ (no ?institute)" "[]" "non-empty"
fi

SITES_INST="$(body GET "/api/site/?institute=$INSTITUTE")"
SITE_IDS="$(printf '%s' "$SITES_INST" | grep -oE '"id":[0-9]+' | cut -d: -f2 | tr '\n' ' ' || true)"
SITE_IDS="${SITE_IDS%"${SITE_IDS##*[![:space:]]}"}"   # trim trailing space
if [[ -n "$SITE_IDS" ]]; then
  record_v PASS "GET /api/site/?institute=$INSTITUTE" "sites listed" "sites: $SITE_IDS"
else
  record_v FAIL "GET /api/site/?institute=$INSTITUTE" "sites listed" "empty: $(printf '%s' "$SITES_INST" | head -c 120)"
fi
echo

# --- 4-6. reading the institute's data ----------------------------------------
echo "Reading site $SITE"
record "GET /api/site/$SITE/video/" "200" "$(code GET "/api/site/$SITE/video/")"

VIDEOS="$(body GET "/api/site/$SITE/video/")"
FIRST_VIDEO="$(printf '%s' "$VIDEOS" | grep -oE '"id":[0-9]+' | head -1 | cut -d: -f2 || true)"
VIDEO_COUNT="$(printf '%s' "$VIDEOS" | grep -coE '"id":[0-9]+' || true)"
VIDEO_COUNT="${VIDEO_COUNT:-0}"
echo "  ($VIDEO_COUNT video records visible)"

PROBE_VIDEO="${VIDEO_ID:-$FIRST_VIDEO}"
if [[ -n "$PROBE_VIDEO" ]]; then
  record "GET /api/site/$SITE/video/$PROBE_VIDEO/" "200" "$(code GET "/api/site/$SITE/video/$PROBE_VIDEO/")"
  record "GET .../video/$PROBE_VIDEO/playback/" "200" "$(code GET "/api/site/$SITE/video/$PROBE_VIDEO/playback/")"
  record "GET .../video/$PROBE_VIDEO/thumbnail/" "200" "$(code GET "/api/site/$SITE/video/$PROBE_VIDEO/thumbnail/")"
else
  skip "video detail probes" "no video records visible at site $SITE"
fi

record "GET /api/site/$SITE/timeseries/" "200" "$(code GET "/api/site/$SITE/timeseries/")"
record "GET /api/site/$SITE/cameraconfig/" "200" "$(code GET "/api/site/$SITE/cameraconfig/")"
record "GET /api/site/$SITE/videoconfig/" "200" "$(code GET "/api/site/$SITE/videoconfig/")"
record "GET /api/site/$SITE/crosssection/" "200" "$(code GET "/api/site/$SITE/crosssection/")"
echo

# --- 11. the queryset.none() fall-through -------------------------------------
# TODO-115: both get_queryset() methods filter on institute and then fall
# through to queryset.none(), so the filter branch is dead code upstream.
# Fail-safe, but it means recipe and device metadata are simply unavailable.
echo "Known-empty endpoints (upstream queryset.none() fall-through)"
RECIPES="$(body GET /api/recipe/)"
if [[ "$(printf '%s' "$RECIPES" | tr -d '[:space:]')" == "[]" ]]; then
  record "GET /api/recipe/" "[]" "[]"
else
  record "GET /api/recipe/" "[]" "non-empty: $(printf '%s' "$RECIPES" | head -c 80)"
fi
DEVICES="$(body GET /api/device/)"
printf '  %-4s %-46s %s\n' "INFO" "GET /api/device/" "$(printf '%s' "$DEVICES" | head -c 80)"
echo

# --- 12. the non-member wall --------------------------------------------------
if [[ -n "$FOREIGN_SITE" ]]; then
  echo "Non-member wall"
  record "GET /api/site/$FOREIGN_SITE/video/ (foreign)" "403" "$(code GET "/api/site/$FOREIGN_SITE/video/")"
  echo
fi

# --- 7, 13. writes that must be refused ---------------------------------------
if [[ $PROBE_WRITES -eq 1 ]]; then
  echo "Writes that must be refused"
  if [[ -n "$PROBE_VIDEO" ]]; then
    # Empty body: a no-op even in the failure case where it is permitted.
    # Same has_object_permission branch that gates DELETE.
    record "PATCH .../video/$PROBE_VIDEO/ (empty body)" "403" \
      "$(code PATCH "/api/site/$SITE/video/$PROBE_VIDEO/" -H 'Content-Type: application/json' -d '{}')"
  else
    skip "PATCH probe" "no video id"
  fi

  # 400 proves the permission layer let us through without creating anything.
  # 403 would mean it did not. Never post a real video here.
  record "POST /api/video/ (invalid payload)" "400" \
    "$(code POST "/api/video/" -H 'Content-Type: application/json' -d '{"not_a_field":"deliberately invalid"}')"
  echo
else
  echo "Writes that must be refused"
  skip "PATCH / POST probes" "pass --probe-writes to run them"
  echo
fi

# --- 8, 10. the destructive probes --------------------------------------------
if [[ $PROBE_DELETE -eq 1 ]]; then
  echo "DELETE probes"
  echo "  Video $VIDEO_ID — confirm this is in the TODO-114 mirror before trusting this."
  record "DELETE .../video/$VIDEO_ID/" "403" "$(code DELETE "/api/site/$SITE/video/$VIDEO_ID/")"

  TS_ID="$(body GET "/api/site/$SITE/timeseries/" | grep -oE '"id":[0-9]+' | head -1 | cut -d: -f2 || true)"
  if [[ -n "$TS_ID" ]]; then
    record "DELETE .../timeseries/$TS_ID/" "403" "$(code DELETE "/api/site/$SITE/timeseries/$TS_ID/")"
  else
    skip "DELETE timeseries probe" "no timeseries rows visible"
  fi
  echo
else
  echo "DELETE probes"
  skip "DELETE probes" "staged — see the header; run only after the TODO-114 mirror exists"
  echo
fi

# --- summary ------------------------------------------------------------------
echo "─────────────────────────────────────────────────────────────────────────"
printf 'PASS %d   FAIL %d   SKIP %d\n' "$PASS" "$FAIL" "$SKIP"
echo
echo "Markdown row form, for the README's API access section:"
echo
echo "| Request | Expected | Actual | |"
echo "|---|---|---|---|"
for r in "${RESULTS[@]}"; do
  IFS='|' read -r v n e a <<< "$r"
  echo "| \`$n\` | $e | $a | $v |"
done
echo

[[ $FAIL -eq 0 ]] || exit 1
