#!/bin/bash
# lockdown-grafana.sh — close the public Grafana on :9443 and upgrade it.
#
# WHY
#   Until now Grafana allowed anonymous Viewer access, and its datasource
#   connected to Postgres as the superuser "orc". /api/ds/query is open to
#   anonymous Viewers, so anyone on the internet could run arbitrary SQL as a
#   superuser against the production sensor database (ISSUE_LOG, "Grafana
#   lock-down"). The image, grafana/grafana:11.3.0, was also past end of life.
#
# WHAT IT CHANGES
#   1. Creates a Postgres role orc_grafana_ro: no superuser, SELECT on
#      sensor_readings only. Grafana's datasource uses it instead of "orc".
#   2. Creates the Grafana Viewer login "orc-readonly" for the station-health
#      tools on the workstation.
#   3. Copies two files from this git clone into /opt/orc-additions:
#        docker-compose.yml                       (image 13.3.1, anonymous off,
#                                                  request logging on)
#        grafana/provisioning/datasources/timescale.yml   (read-only role)
#      Nothing else is copied, so unrelated undeployed changes stay undeployed.
#   4. Recreates ONLY the grafana service.
#
# WHAT IT NEVER TOUCHES
#   The "orc" role (sensor-ingest and sheets-export connect as it), the
#   sensor-upload and sensor-ingest containers, the certs (stations pin the
#   :8443 CA), Postgres itself, liveorc_webapp, and the security group.
#   The sensor path is station -> :8443 sensor-upload -> /var/orc/sensors ->
#   sensor-ingest -> Postgres. Grafana is not in it. The script still proves
#   that: every other container's start time must be unchanged afterwards,
#   :8443 must still answer, and the newest sensor row must not regress.
#
# ROLLBACK
#   Before changing anything it backs up .env, the two files, and the Grafana
#   data volume (Grafana's database migration is one-way, so going back to
#   11.3.0 needs the old data). Any failed check after the change restores all
#   of them automatically. The Postgres role and the Viewer login stay; they
#   are harmless.
#
# USAGE (on the LiveORC host, in ~/code/git/openrivercam after a git pull)
#   sudo ./spring_2026_ID/liveorc_server/lockdown-grafana.sh --check
#   sudo ./spring_2026_ID/liveorc_server/lockdown-grafana.sh
#   sudo ./spring_2026_ID/liveorc_server/lockdown-grafana.sh --rollback
#
# Test hooks: STACK_DIR, LOCKDOWN_TEST=1 (skip the root check),
#   GRAFANA_HOST_PORT (default 9443), UPLOAD_HOST_PORT (default 8443),
#   GRAFANA_C, DB_C, UPLOAD_C, INGEST_C (container names).

set -uo pipefail

STACK_DIR="${STACK_DIR:-/opt/orc-additions}"
SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GRAFANA_C="${GRAFANA_C:-orc-grafana}"
DB_C="${DB_C:-orc-timescale}"
UPLOAD_C="${UPLOAD_C:-orc-sensor-upload}"
INGEST_C="${INGEST_C:-orc-sensor-ingest}"
HOSTNAME_FQDN="openrivercam.endlessprojects.info"
GPORT="${GRAFANA_HOST_PORT:-9443}"
UPORT="${UPLOAD_HOST_PORT:-8443}"
RO_ROLE="orc_grafana_ro"
RO_USER="orc-readonly"
NEW_IMAGE="grafana/grafana:13.3.1"
FILES=("docker-compose.yml" "grafana/provisioning/datasources/timescale.yml")

MODE="apply"
[ "${1:-}" = "--check" ]    && MODE="check"
[ "${1:-}" = "--rollback" ] && MODE="rollback"

RED=$'\033[31m'; GRN=$'\033[32m'; YEL=$'\033[33m'; BLD=$'\033[1m'; RST=$'\033[0m'
say()  { printf '%s\n' "$*"; }
ok()   { printf '%s  ok%s  %s\n'   "$GRN" "$RST" "$*"; }
warn() { printf '%s warn%s  %s\n'  "$YEL" "$RST" "$*"; }
die()  { printf '%sFAIL%s  %s\n'   "$RED" "$RST" "$*" >&2; exit 1; }
hdr()  { printf '\n%s== %s ==%s\n' "$BLD" "$*" "$RST"; }

[ "$(id -u)" -eq 0 ] || [ -n "${LOCKDOWN_TEST:-}" ] || die "run with sudo"
[ -d "$STACK_DIR" ] || die "$STACK_DIR not found — is this the LiveORC host?"
for f in "${FILES[@]}"; do [ -f "$SRC_DIR/$f" ] || die "$SRC_DIR/$f missing — git pull first"; done

if docker compose version >/dev/null 2>&1; then DC=(docker compose)
elif command -v docker-compose >/dev/null 2>&1; then DC=(docker-compose)
else die "no docker compose found"; fi
command -v python3 >/dev/null || die "python3 not found"
command -v openssl >/dev/null || die "openssl not found"

cd "$STACK_DIR" || die "cannot cd to $STACK_DIR"
COMPOSE=("${DC[@]}" --env-file .env)
ENVF="$STACK_DIR/.env"
[ -f "$ENVF" ] || die "$ENVF not found"

envget() { grep -E "^$1=" "$ENVF" | tail -1 | cut -d= -f2-; }
# Treat the .env.example placeholder as unset.
envget_real() { local v; v=$(envget "$1"); [ "$v" = "REPLACE_ME" ] && v=""; printf '%s' "$v"; }

# No -i: docker exec -i would read this script's stdin, and swallow whatever the
# operator types at the passphrase prompt. Only psql_stdin (the role heredoc)
# needs stdin.
psql_orc()   { docker exec "$DB_C" psql -U orc -d orc -v ON_ERROR_STOP=1 -X -q "$@"; }
psql_stdin() { docker exec -i "$DB_C" psql -U orc -d orc -v ON_ERROR_STOP=1 -X -q; }
gcurl()    { curl -sk --max-time 15 "$@"; }

# Start time of every container except grafana. Created time is NOT used: a
# restart changes StartedAt and leaves Created alone.
others_state() {
    docker ps --format '{{.Names}}' | grep -vx "$GRAFANA_C" | sort \
      | while read -r c; do docker inspect -f '{{.Name}} {{.State.StartedAt}}' "$c"; done
}
# The containers the sensor path runs through. A change in any of these is a
# hard failure; any other container changing during the minute this takes is
# only reported, so an unrelated crash-restart cannot trigger a rollback.
critical_state() {
    local c
    for c in "$UPLOAD_C" "$INGEST_C" "$DB_C"; do
        docker inspect -f '{{.Name}} {{.State.StartedAt}}' "$c"
    done
}
newest_row() {
    psql_orc -At -c "SELECT coalesce(max(ts)::text,'none') FROM sensor_readings" 2>/dev/null
}
upload_health() {
    curl -s --max-time 10 --cacert "$STACK_DIR/certs/fullchain.pem" \
         --resolve "$HOSTNAME_FQDN:$UPORT:127.0.0.1" \
         "https://$HOSTNAME_FQDN:$UPORT/sensors/health" 2>/dev/null
}
wait_for_grafana() {
    for _ in $(seq 1 45); do
        [ "$(gcurl -o /dev/null -w '%{http_code}' "https://127.0.0.1:$GPORT/api/health")" = "200" ] && return 0
        sleep 2
    done
    return 1
}

BK_ROOT="$STACK_DIR/.lockdown-backup"

# ---- backup / restore of the Grafana data volume --------------------------
# A throwaway container sharing the grafana volumes does the work, using the
# image grafana already runs (so nothing is pulled). ./dashboards is a
# read-only bind mount nested in the volume path; it is excluded and spared.
grafana_data_backup() {  # $1 = backup dir
    local img; img=$(docker inspect -f '{{.Image}}' "$GRAFANA_C") || return 1
    docker run --rm --user 0 --entrypoint tar --volumes-from "$GRAFANA_C" \
        -v "$1:/bk" "$img" -C /var/lib/grafana --exclude=./dashboards \
        -cpf /bk/grafana-data.tar .
}
grafana_data_restore() {  # $1 = backup dir
    local img; img=$(docker inspect -f '{{.Image}}' "$GRAFANA_C") || return 1
    docker run --rm --user 0 --entrypoint sh --volumes-from "$GRAFANA_C" \
        -v "$1:/bk:ro" "$img" -c \
        'find /var/lib/grafana -mindepth 1 -maxdepth 1 ! -name dashboards -exec rm -rf {} + && tar -xpf /bk/grafana-data.tar -C /var/lib/grafana'
}

restore_from() {  # $1 = backup dir
    local bk="$1"
    [ -d "$bk" ] || { warn "no backup dir $bk"; return 1; }
    say "  restoring from $bk"
    docker stop "$GRAFANA_C" >/dev/null 2>&1 || true
    local f
    for f in "${FILES[@]}"; do
        [ -f "$bk/$f" ] && cp -p "$bk/$f" "$STACK_DIR/$f"
    done
    [ -f "$bk/.env" ] && cp -p "$bk/.env" "$ENVF"
    [ -f "$bk/grafana-data.tar" ] && grafana_data_restore "$bk"
    # The old compose file pins the old image; a named, no-deps up uses it.
    "${COMPOSE[@]}" up -d --no-deps grafana >/dev/null 2>&1
    if wait_for_grafana; then ok "grafana is back on its previous configuration"
    else warn "grafana did not come back: docker logs $GRAFANA_C"; return 1; fi
}

if [ "$MODE" = "rollback" ]; then
    hdr "Rollback"
    LAST=$(ls -1d "$BK_ROOT"/* 2>/dev/null | sort | tail -1)
    [ -n "$LAST" ] || die "no backup under $BK_ROOT"
    say "  newest backup: $LAST"
    restore_from "$LAST" || die "rollback failed; the backup is intact at $LAST"
    say "  The $RO_ROLE role and the $RO_USER login were left in place."
    exit 0
fi

# ================================================================ preflight
hdr "Preflight"

"${COMPOSE[@]}" config -q 2>/tmp/lockdown_cfg.err || {
    cat /tmp/lockdown_cfg.err >&2
    die "compose config fails on the CURRENT files; fix the stack first (see enable-grafana-tls.sh note on SHEETS_SPREADSHEET_ID)"; }
ok "compose config parses (current files)"

for c in "$GRAFANA_C" "$DB_C" "$UPLOAD_C" "$INGEST_C"; do
    [ "$(docker inspect -f '{{.State.Running}}' "$c" 2>/dev/null)" = "true" ] || die "$c is not running"
done
ok "grafana, timescale, sensor-upload and sensor-ingest are running"

ADMIN_PW=$(envget_real GRAFANA_ADMIN_PASSWORD)
[ -n "$ADMIN_PW" ] || die "GRAFANA_ADMIN_PASSWORD is not set in $ENVF"
# /api/user, and the login in the body must be orc-admin. NOT /api/org: while
# anonymous access is on, /api/org answers 200 to a WRONG password too, which
# would make this check pass on exactly the host state we are about to change.
WHO=$(gcurl -u "orc-admin:$ADMIN_PW" "https://127.0.0.1:$GPORT/api/user" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("login",""))' 2>/dev/null)
CODE=$([ "$WHO" = "orc-admin" ] && echo 200 || echo "not signed in")
[ "$CODE" = "200" ] || die "orc-admin cannot sign in with the .env password ($CODE).
      GF_SECURITY_ADMIN_PASSWORD only applies when Grafana's database is first
      created. If the password was changed in the UI, put the real one in .env."
ok "orc-admin signs in with the .env password"

[ "$(psql_orc -At -c 'select 1' 2>&1)" = "1" ] || die "cannot run SQL in $DB_C as orc"
ok "SQL works in $DB_C as orc"

BASE_OTHERS="$(others_state)"
BASE_CRIT="$(critical_state)"
BASE_ROW="$(newest_row)"
BASE_HEALTH="$(upload_health)"
say "    newest sensor_readings row : $BASE_ROW"
say "    :$UPORT /sensors/health      : ${BASE_HEALTH:-<no answer>}"
[ -n "$BASE_HEALTH" ] || warn "sensor-upload did not answer on :$UPORT before the change; the after-check will be weaker"
say "    sensor-path containers (must not restart), with start times:"
printf '%s\n' "$BASE_CRIT" | sed 's/^/      /'
say "    $(printf '%s\n' "$BASE_OTHERS" | grep -c .) running containers other than grafana in all (any change is reported)"

ANON_NOW=$(gcurl -o /dev/null -w '%{http_code}' "https://127.0.0.1:$GPORT/api/search")
say "    anonymous /api/search now  : HTTP $ANON_NOW (200 = still open)"
CUR_IMAGE=$(docker inspect -f '{{.Config.Image}}' "$GRAFANA_C")
say "    grafana image now          : $CUR_IMAGE   -> $NEW_IMAGE"

RO_PW=$(envget_real GRAFANA_RO_PASSWORD)
TOOL_PW=$(envget_real GRAFANA_TOOLING_PASSWORD)
say "    GRAFANA_RO_PASSWORD in .env      : $([ -n "$RO_PW" ] && echo present || echo 'absent (will be generated)')"
say "    GRAFANA_TOOLING_PASSWORD in .env : $([ -n "$TOOL_PW" ] && echo present || echo 'absent (will be asked for)')"

if [ "$MODE" = "check" ]; then
    hdr "Check only — nothing changed"
    say "Re-run without --check to apply."
    exit 0
fi

# Fail on a missing image BEFORE stopping anything.
hdr "Pulling $NEW_IMAGE"
docker pull "$NEW_IMAGE" >/dev/null 2>&1 || docker image inspect "$NEW_IMAGE" >/dev/null 2>&1 \
    || die "cannot pull $NEW_IMAGE (no network from the host?)"
ok "image available"

# Secrets: generate one, ask for the other. Neither is echoed.
if [ -z "$TOOL_PW" ]; then
    say "  Choose a passphrase for the Grafana login '$RO_USER' (used by the"
    say "  workstation tools; at least 12 characters; you will put the same one in"
    say "  ~/.config/orc/grafana-readonly as  $RO_USER:<passphrase>)."
    read -r -s -p "  passphrase: " P1; echo
    read -r -s -p "  again:      " P2; echo
    [ "$P1" = "$P2" ] || die "passphrases differ"
    [ "${#P1}" -ge 12 ] || die "too short"
    case "$P1" in *[\"\\\']*|*$'\n'*) die "avoid quotes and backslashes in the passphrase" ;; esac
    TOOL_PW="$P1"
fi
[ -n "$RO_PW" ] || RO_PW=$(openssl rand -hex 24)

# ================================================================== backup
hdr "Backup"
BK="$BK_ROOT/$(date -u +%Y%m%dT%H%M%SZ)"
mkdir -p "$BK/grafana/provisioning/datasources" && chmod 700 "$BK_ROOT" "$BK" || die "cannot create $BK"
cp -p "$ENVF" "$BK/.env"
for f in "${FILES[@]}"; do cp -p "$STACK_DIR/$f" "$BK/$f" || die "cannot back up $f"; done
docker stop "$GRAFANA_C" >/dev/null || die "cannot stop $GRAFANA_C"
if ! grafana_data_backup "$BK"; then
    docker start "$GRAFANA_C" >/dev/null 2>&1
    die "could not back up the grafana data volume; grafana restarted unchanged"
fi
ok "backed up .env, 2 config files and grafana data ($(du -sh "$BK/grafana-data.tar" | cut -f1)) to $BK"

fail() {  # a check failed after we started changing things
    printf '%sFAIL%s  %s\n' "$RED" "$RST" "$*" >&2
    hdr "Automatic rollback"
    restore_from "$BK" || printf '%s\n' "  ROLLBACK ALSO FAILED. Backup: $BK" >&2
    exit 1
}

# ============================================================ database role
hdr "Read-only database role $RO_ROLE"
# The password goes through stdin as a psql variable, never on a command line.
# `orc` is not altered. Only SELECT on sensor_readings is granted.
psql_stdin >/dev/null <<SQL || fail "creating the role failed"
\set pw '$RO_PW'
DO \$\$ BEGIN
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = '$RO_ROLE') THEN
    CREATE ROLE $RO_ROLE LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION;
  END IF;
END \$\$;
ALTER ROLE $RO_ROLE PASSWORD :'pw' CONNECTION LIMIT 20;
ALTER ROLE $RO_ROLE SET statement_timeout = '30s';
ALTER ROLE $RO_ROLE SET default_transaction_read_only = on;
REVOKE ALL ON ALL TABLES IN SCHEMA public FROM $RO_ROLE;
GRANT CONNECT ON DATABASE orc TO $RO_ROLE;
GRANT USAGE ON SCHEMA public TO $RO_ROLE;
GRANT SELECT ON sensor_readings TO $RO_ROLE;
SQL
ok "role created/updated"

pro() { docker exec -e PGPASSWORD="$RO_PW" "$DB_C" psql -h 127.0.0.1 -U "$RO_ROLE" -d orc -X -At "$@"; }
[ "$(pro -c 'select count(*) > 0 from sensor_readings' 2>&1)" = "t" ] || fail "$RO_ROLE cannot read sensor_readings"
ok "$RO_ROLE can read sensor_readings"
[ "$(pro -c 'select rolsuper from pg_roles where rolname=current_user' 2>&1)" = "f" ] || fail "$RO_ROLE is a superuser"
ok "$RO_ROLE is not a superuser"
# WHERE false: nothing is deleted even if the grant were wrong.
pro -c 'delete from sensor_readings where false' >/dev/null 2>&1 && fail "$RO_ROLE could DELETE"
ok "DELETE is refused"
pro -c "copy (select 1) to program 'true'" >/dev/null 2>&1 && fail "$RO_ROLE could run a program"
ok "COPY ... TO PROGRAM is refused"
pro -c 'create table lockdown_probe(i int)' >/dev/null 2>&1 && { psql_orc -c 'drop table if exists lockdown_probe' >/dev/null 2>&1; fail "$RO_ROLE could CREATE a table"; }
ok "CREATE TABLE is refused"

# ================================================== config + secrets + start
hdr "Applying"
upsert_env() {  # $1 key, $2 value
    if grep -qE "^$1=" "$ENVF"; then
        python3 - "$ENVF" "$1" "$2" <<'PY'
import sys
p, k, v = sys.argv[1:4]
lines = open(p).read().split("\n")
out, done = [], False
for l in lines:
    if l.startswith(k + "="):
        if not done: out.append(f"{k}={v}"); done = True
    else: out.append(l)
open(p, "w").write("\n".join(out))
PY
    else
        printf '\n%s=%s\n' "$1" "$2" >> "$ENVF"
    fi
}
upsert_env GRAFANA_RO_PASSWORD "$RO_PW"
upsert_env GRAFANA_TOOLING_PASSWORD "$TOOL_PW"
chmod --reference="$BK/.env" "$ENVF" 2>/dev/null || true
for f in "${FILES[@]}"; do cp "$SRC_DIR/$f" "$STACK_DIR/$f" || fail "cannot copy $f"; done
ok ".env updated; 2 config files copied from $SRC_DIR"

"${COMPOSE[@]}" config -q 2>/tmp/lockdown_cfg2.err || { cat /tmp/lockdown_cfg2.err >&2; fail "compose config fails with the new files"; }
ok "compose config parses (new files)"

"${COMPOSE[@]}" up -d --no-deps grafana >/dev/null 2>&1 || fail "docker compose up grafana failed"
wait_for_grafana || fail "grafana did not become healthy; see: docker logs $GRAFANA_C"
ok "grafana is up: $(docker inspect -f '{{.Config.Image}}' "$GRAFANA_C")"

# ===================================================== Grafana viewer login
hdr "Grafana login $RO_USER (Viewer)"
GA=(-u "orc-admin:$ADMIN_PW")
BODY=$(python3 -c 'import json,sys; print(json.dumps({"name":"orc readonly","login":sys.argv[1],"email":sys.argv[1]+"@liveorc.local","password":sys.argv[2]}))' "$RO_USER" "$TOOL_PW")
CODE=$(gcurl -o /tmp/lockdown_user.json -w '%{http_code}' "${GA[@]}" -H 'Content-Type: application/json' -X POST -d "$BODY" "https://127.0.0.1:$GPORT/api/admin/users")
UID_G=""
if [ "$CODE" = "200" ]; then
    UID_G=$(python3 -c 'import json; print(json.load(open("/tmp/lockdown_user.json"))["id"])')
    ok "created $RO_USER (id $UID_G)"
else
    UID_G=$(gcurl "${GA[@]}" "https://127.0.0.1:$GPORT/api/users/lookup?loginOrEmail=$RO_USER" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("id",""))' 2>/dev/null)
    [ -n "$UID_G" ] || fail "could not create or find $RO_USER (HTTP $CODE)"
    # Grafana answers 500 when asked to set the password a user already has, so
    # a re-run with the same passphrase must not call the reset at all.
    WHO=$(gcurl -u "$RO_USER:$TOOL_PW" "https://127.0.0.1:$GPORT/api/user" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("login",""))' 2>/dev/null)
    if [ "$WHO" = "$RO_USER" ]; then
        ok "$RO_USER already existed (id $UID_G) with this passphrase"
    else
        PWB=$(python3 -c 'import json,sys; print(json.dumps({"password":sys.argv[1]}))' "$TOOL_PW")
        [ "$(gcurl -o /dev/null -w '%{http_code}' "${GA[@]}" -H 'Content-Type: application/json' -X PUT -d "$PWB" "https://127.0.0.1:$GPORT/api/admin/users/$UID_G/password")" = "200" ] \
            || fail "could not reset the password of existing $RO_USER"
        ok "$RO_USER already existed (id $UID_G); password reset to the one in .env"
    fi
fi
gcurl -o /dev/null "${GA[@]}" -H 'Content-Type: application/json' -X PATCH -d '{"role":"Viewer"}' "https://127.0.0.1:$GPORT/api/org/users/$UID_G"
rm -f /tmp/lockdown_user.json

# ============================================================ verification
hdr "Verification"
gq() {  # $1 = user:password, $2 = SQL
    local body; body=$(python3 -c 'import json,sys; print(json.dumps({"queries":[{"refId":"A","datasource":{"uid":"timescale","type":"grafana-postgresql-datasource"},"format":"table","rawSql":sys.argv[1],"rawQuery":True}],"from":"now-1h","to":"now"}))' "$2")
    gcurl -u "$1" -H 'Content-Type: application/json' -X POST -d "$body" "https://127.0.0.1:$GPORT/api/ds/query"
}
for p in /api/search /api/datasources; do
    C=$(gcurl -o /dev/null -w '%{http_code}' "https://127.0.0.1:$GPORT$p")
    [ "$C" = "401" ] || fail "anonymous $p returned HTTP $C (expected 401)"
done
C=$(gcurl -o /dev/null -w '%{http_code}' -X POST -H 'Content-Type: application/json' -d '{}' "https://127.0.0.1:$GPORT/api/ds/query")
[ "$C" = "401" ] || fail "anonymous /api/ds/query returned HTTP $C (expected 401)"
ok "anonymous access is closed (search, datasources, ds/query -> 401)"

OUT=$(gq "$RO_USER:$TOOL_PW" "select count(*)::text as n from sensor_readings")
N=$(printf '%s' "$OUT" | python3 -c 'import json,sys; print(json.load(sys.stdin)["results"]["A"]["frames"][0]["data"]["values"][0][0])' 2>/dev/null)
[ -n "$N" ] && [ "$N" != "0" ] || fail "$RO_USER cannot query sensor_readings through Grafana: ${OUT:0:200}"
ok "$RO_USER queries sensor_readings through the datasource ($N rows)"

OUT=$(gq "$RO_USER:$TOOL_PW" "select current_user::text as u, (select rolsuper from pg_roles where rolname=current_user)::text as s")
printf '%s' "$OUT" | grep -q "$RO_ROLE" || fail "datasource is not connecting as $RO_ROLE: ${OUT:0:200}"
printf '%s' "$OUT" | grep -q '"false"' || fail "datasource role is a superuser"
ok "the datasource connects as $RO_ROLE, not a superuser"

DASH=$(gcurl -u "$RO_USER:$TOOL_PW" "https://127.0.0.1:$GPORT/api/search?type=dash-db" | python3 -c 'import json,sys; print(",".join(d["uid"] for d in json.load(sys.stdin)))' 2>/dev/null)
case "$DASH" in *station-overview*) ok "dashboard station-overview is provisioned" ;; *) fail "dashboard station-overview missing (saw: '$DASH')" ;; esac

HC=$(gcurl "${GA[@]}" "https://127.0.0.1:$GPORT/api/datasources/uid/timescale/health")
printf '%s' "$HC" | grep -qi '"status":"OK"' && ok "datasource health: OK" || warn "datasource health said: ${HC:0:160}"

# ---- the sensor path was not disturbed
hdr "Sensor path unchanged"
AFTER_CRIT="$(critical_state)"
if [ "$BASE_CRIT" = "$AFTER_CRIT" ]; then
    ok "sensor-upload, sensor-ingest and timescale were not restarted or recreated"
else
    diff <(printf '%s\n' "$BASE_CRIT") <(printf '%s\n' "$AFTER_CRIT") >&2
    fail "a sensor-path container changed state (diff above)"
fi
AFTER_OTHERS="$(others_state)"
if [ "$BASE_OTHERS" = "$AFTER_OTHERS" ]; then
    ok "no other container changed state"
else
    warn "another container changed state during the run (not a sensor-path container, so no rollback):"
    diff <(printf '%s\n' "$BASE_OTHERS") <(printf '%s\n' "$AFTER_OTHERS") | sed 's/^/      /' >&2
fi
AFTER_HEALTH="$(upload_health)"
if [ -n "$BASE_HEALTH" ]; then
    [ "$AFTER_HEALTH" = "$BASE_HEALTH" ] && ok ":$UPORT /sensors/health unchanged" || fail ":$UPORT health changed: '$AFTER_HEALTH'"
fi
AFTER_ROW="$(newest_row)"
if [ "$AFTER_ROW" \< "$BASE_ROW" ]; then fail "newest sensor row went backwards: $BASE_ROW -> $AFTER_ROW"; fi
ok "newest sensor row $BASE_ROW -> $AFTER_ROW (not regressed)"

hdr "Done"
say "  Backup kept at $BK (contains .env: root-only)."
say "  On the workstation, create ~/.config/orc/grafana-readonly (chmod 600):"
say "      $RO_USER:<the passphrase you chose>"
say "  Then re-check the whole path from there, no host needed:"
say "      ./spring_2026_ID/liveorc_server/station-health/ingest_flow_check.py --since $(date -u +%Y-%m-%dT%H:%M:%SZ)"
say "  The station sleeps between wakes and rows arrive about one wake late, so"
say "  wait for two wakes before treating a lack of new rows as a problem."
