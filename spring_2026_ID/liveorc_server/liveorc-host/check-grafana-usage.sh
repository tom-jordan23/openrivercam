#!/usr/bin/env bash
# check-grafana-usage.sh — who has used the public Grafana on :9443, and how much?
#
# WHY
#   AmCross IT asked about the Grafana instance. Before deciding whether to
#   lock it down or remove it (see ISSUE_LOG, 2026-10-28 security-group entry),
#   find out whether anything other than our own tooling touches it.
#
# EVIDENCE, in order of reliability
#   A. grafana.db table anon_device (Grafana 10.2+): one row per anonymous
#      client (IP + user agent) with first-seen and last-seen times. Kept
#      across container restarts, so it reaches back further than the logs.
#      Only updated when a client is seen, and old rows may be pruned, so
#      read it as "seen between created_at and updated_at", not a hit count.
#   B. docker logs orc-grafana. Grafana logs "Request Completed" lines only
#      for errors, unless router_logging is on. So an empty or error-only log
#      does NOT mean no traffic. The script reports what the log contains so
#      you can tell. Logs start at the last container recreate.
#   C. Live TCP connections on :9443 right now (ss).
#   D. Whether the dashboard was ever edited, and whether anyone logged in.
#
# CLIENTS
#   Our own tooling (station_gaps.py etc.) and curl show up as non-browser
#   user agents. Pass your own public IPs with --exclude-ip to hide them.
#
# READ-ONLY. Copies grafana.db out of the container to a temp dir (removed on
# exit) and reads the copy. Writes nothing to Grafana, Postgres or any volume.
#
# USAGE (on the LiveORC host, in ~/code/git/openrivercam after a git pull)
#   ./spring_2026_ID/liveorc_server/liveorc-host/check-grafana-usage.sh
#   ./spring_2026_ID/liveorc_server/liveorc-host/check-grafana-usage.sh --exclude-ip 203.0.113.5 --exclude-ip 198.51.100.7
#
# Test hooks (no Docker needed): --db-file PATH --logs-file PATH
set -u

EXCLUDE=()
DB_FILE=""
LOGS_FILE=""
while [ $# -gt 0 ]; do
  case "$1" in
    --exclude-ip) EXCLUDE+=("$2"); shift 2 ;;
    --db-file)    DB_FILE="$2"; shift 2 ;;
    --logs-file)  LOGS_FILE="$2"; shift 2 ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
done

C=orc-grafana
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
h(){ printf '\n\033[1m== %s ==\033[0m\n' "$*"; }

D=docker
if [ -z "$DB_FILE$LOGS_FILE" ]; then
  docker ps >/dev/null 2>&1 || D="sudo docker"
  if ! $D ps --format '{{.Names}}' 2>/dev/null | grep -qx "$C"; then
    echo "container $C is not running (or docker is not usable)" >&2
    exit 1
  fi
fi

h "0. the container"
if [ -z "$DB_FILE$LOGS_FILE" ]; then
  $D inspect "$C" --format '  image:    {{.Config.Image}}
  created:  {{.Created}}
  started:  {{.State.StartedAt}}' 2>&1
  echo "  anonymous settings:"
  $D inspect "$C" --format '{{range .Config.Env}}{{println .}}{{end}}' \
    | grep -E '^GF_AUTH_ANONYMOUS|^GF_SERVER_ROUTER|^GF_LOG' | sed 's/^/    /'
  echo "  (GF_SERVER_ROUTER_LOGGING absent = access lines are NOT logged)"
else
  echo "  (test mode, no container)"
fi

h "1. live connections to :9443 right now"
if command -v ss >/dev/null 2>&1; then
  ss -Htn state established '( sport = :9443 )' 2>/dev/null \
    | awk '{print $4}' | sed 's/:[0-9]*$//' | sort | uniq -c | sort -rn | sed 's/^/  /'
  echo "  (blank = nothing connected at this moment; browsers close idle connections)"
else
  echo "  ss not installed"
fi

# ---- collect the two evidence files --------------------------------------
if [ -z "$DB_FILE" ]; then
  mkdir -p "$TMP/db"
  # Stream with `docker exec cat` rather than `docker cp`: the container runs
  # as root, so the read succeeds, and the copy is owned by the caller. docker
  # cp keeps the original owner (uid 472, mode 640), which the caller cannot
  # read. That made the first version fail with "unable to open database file".
  if ! $D exec "$C" cat /var/lib/grafana/grafana.db >"$TMP/db/grafana.db"; then
    echo "  could not read /var/lib/grafana/grafana.db from $C" >&2
  fi
  # A WAL file, if present, holds recent writes not yet in the main file.
  $D exec "$C" cat /var/lib/grafana/grafana.db-wal >"$TMP/db/grafana.db-wal" 2>/dev/null \
    || rm -f "$TMP/db/grafana.db-wal"
  [ -s "$TMP/db/grafana.db-wal" ] || rm -f "$TMP/db/grafana.db-wal"
  DB_FILE="$TMP/db/grafana.db"
fi
if [ -z "$LOGS_FILE" ]; then
  LOGS_FILE="$TMP/grafana.log"
  $D logs --timestamps "$C" >"$LOGS_FILE" 2>&1
fi

EX=$(IFS=,; echo "${EXCLUDE[*]:-}")
EXCLUDE_IPS="$EX" python3 -I - "$DB_FILE" "$LOGS_FILE" <<'PY'
import os, re, sqlite3, sys, collections

db_path, log_path = sys.argv[1], sys.argv[2]
exclude = {x for x in os.environ.get("EXCLUDE_IPS", "").split(",") if x}

def h(t): print(f"\n\033[1m== {t} ==\033[0m")
def ex(ip): return ip in exclude

def browser(ua):
    u = ua or ""
    if "curl/" in u: return "curl"
    if "Python-urllib" in u: return "python-urllib"
    if "python-requests" in u: return "python-requests"
    if "Mozilla" in u: return "browser"
    return "other: " + (u[:40] or "(none)")

# ---- A. anon_device -------------------------------------------------------
h("2. anonymous clients recorded in grafana.db (anon_device)")
con = None
if not os.path.exists(db_path) or os.path.getsize(db_path) == 0:
    print("  grafana.db could not be copied out of the container")
else:
    try:
        con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        tables = {r[0] for r in con.execute("select name from sqlite_master where type='table'")}
        print(f"  tables in db: {len(tables)}")
        if "anon_device" not in tables:
            print("  no anon_device table: this Grafana does not record anonymous devices")
        else:
            rows = con.execute("select client_ip, user_agent, created_at, updated_at "
                               "from anon_device order by updated_at desc").fetchall()
            print(f"  rows: {len(rows)}")
            shown = hidden = 0
            kinds = collections.Counter()
            for ip, ua, c, u in rows:
                if ex(ip):
                    hidden += 1
                    continue
                shown += 1
                kinds[browser(ua)] += 1
                print(f"  {ip:<40} {browser(ua):<16} first {c}  last {u}")
                print(f"      UA: {(ua or '')[:110]}")
            print(f"  --- {shown} not excluded, {hidden} excluded")
            for k, n in kinds.most_common():
                print(f"  {n:>4}  {k}")
            print("  (timestamps in this table are UTC)")
    except sqlite3.Error as e:
        print(f"  sqlite error: {e}")

# ---- D. users, logins, dashboards ----------------------------------------
h("3. logins and dashboard edits")
if con:
    def q(sql, label):
        try:
            return con.execute(sql).fetchall()
        except sqlite3.Error as e:
            print(f"  {label}: unavailable ({e})")
            return None
    r = q("select login, last_seen_at, created from user", "user")
    if r is not None:
        for login, seen, created in r:
            print(f"  user {login}: created {created}, last seen {seen}")
    r = q("select slug, created, updated, version from dashboard where is_folder=0", "dashboard")
    if r is not None:
        for row in r:
            print(f"  dashboard {row[0]}: created {row[1]}, last updated {row[2]}, version {row[3]}")
    r = q("select count(*) from star", "star")
    if r is not None:
        print(f"  starred dashboards: {r[0][0]}")
    r = q("select count(*) from login_attempt", "login_attempt")
    if r is not None:
        print(f"  failed-login records currently held: {r[0][0]}")
    for t in ("api_key", "team", "user_auth_token"):
        r = q(f"select count(*) from {t}", t)
        if r is not None:
            print(f"  {t}: {r[0][0]}")
    con.close()

# ---- B. logs --------------------------------------------------------------
h("4. docker logs")
lines = open(log_path, errors="replace").read().splitlines()
print(f"  lines: {len(lines)}")
if lines:
    print(f"  first: {lines[0][:30]}")
    print(f"  last:  {lines[-1][:30]}")
req = [l for l in lines if "Request Completed" in l]
print(f"  'Request Completed' lines: {len(req)}")
if not req:
    print("  none. Grafana does not log successful requests by default, so this")
    print("  proves nothing about traffic. Section 2 is the evidence that counts.")
else:
    kv = re.compile(r'(\w+)=("([^"]*)"|\S+)')
    by_ip = collections.Counter()
    by_path = collections.Counter()
    by_day = collections.Counter()
    hidden = 0
    for l in req:
        f = {m.group(1): (m.group(3) if m.group(3) is not None else m.group(2))
             for m in kv.finditer(l)}
        ip = re.sub(r":\d+$", "", f.get("remote_addr", "?"))
        if ex(ip):
            hidden += 1
            continue
        by_ip[ip] += 1
        by_path[f"{f.get('method','?')} {f.get('path','?')} -> {f.get('status','?')}"] += 1
        by_day[l[:10]] += 1
    print(f"  excluded by --exclude-ip: {hidden}")
    print("  --- by client IP ---")
    for k, n in by_ip.most_common(25):
        print(f"  {n:>6}  {k}")
    print("  --- by request ---")
    for k, n in by_path.most_common(25):
        print(f"  {n:>6}  {k}")
    print("  --- by day ---")
    for k in sorted(by_day):
        print(f"  {by_day[k]:>6}  {k}")

# queries that reached the datasource are logged only at debug; note login noise
bad = [l for l in lines if "invalid username or password" in l.lower() or "failed to authenticate" in l.lower()]
print(f"  failed-auth lines: {len(bad)}")
PY

h "how to read this"
cat <<'EOF'
  - Section 2 rows with a browser user agent from an address that is not ours
    are the evidence of a real viewer. Look up unfamiliar IPs (whois/ASN) before
    drawing conclusions; AmCross, PMI and IPB addresses are not known here.
  - Section 2 only proves a client was seen, not what it queried.
  - Section 4 being empty is expected. Do not read it as "nobody came".
  - If section 2 is empty or missing too, the only way to measure use is to turn
    on router logging (GF_SERVER_ROUTER_LOGGING=true) and wait.
EOF
