#!/usr/bin/env bash
# check-ipb-api-usage.sh — has IPB ever used its LiveORC API account?
#
# The IPB service account is user_id 19 (ipb-dashboard@liveorc.local), handed
# over after the 2026-09-09 verification run. The question can't be answered
# from the workstation: the Grafana datasource is the sensor DB (orc), not
# LiveORC's Django DB.
#
# There is no per-user record of API use. The first version of this script
# counted rows in token_blacklist_outstandingtoken, assuming that
# BLACKLIST_AFTER_ROTATION meant the blacklist app was installed. On the host
# (2026-10-05) the table does not exist: the setting is on, but the app is
# not installed. auth_user.last_login is the only per-user field, and
# simplejwt only writes it when UPDATE_LAST_LOGIN is set. So an empty value
# means "not recorded", not "never logged in".
#
# The access log is therefore the main evidence, and it does not name the
# user. Section 2 tells the clients apart by user agent instead. Our partner
# client (partner-api/fetch_timeseries.py) uses urllib, which sends
# "Python-urllib/3.x". ORC-OS on the station uses python-requests. Our own
# verification runs use curl. The station has been offline since 2026-10-01,
# so any python-requests traffic after that date is not the station.
# Timestamps come from `docker logs --timestamps`, which works whatever the
# nginx log format is.
#
# READ-ONLY. SELECT queries and docker logs. Writes nothing.
#
# USAGE (on the LiveORC host, in ~/code/git/openrivercam after a git pull)
#   ./spring_2026_ID/liveorc_server/liveorc-host/check-ipb-api-usage.sh [user_id]
set -u
UID_IPB=${1:-19}
D=docker; docker ps >/dev/null 2>&1 || D="sudo docker"
W=liveorc_webapp
h(){ printf '\n\033[1m== %s ==\033[0m\n' "$*"; }
DBU=$($D exec db sh -c 'printf %s "$POSTGRES_USER"' 2>/dev/null)
DBN=$($D exec db sh -c 'printf %s "${POSTGRES_DB:-$POSTGRES_USER}"' 2>/dev/null)
Q(){ $D exec -i db psql -U "$DBU" -d "$DBN" -At -F '|' -c "$1" 2>&1; }
echo "  db: ${DBU:-<unset>}/${DBN:-<unset>}   user_id: $UID_IPB"

h "0. the account, and its last_login"
Q "select id, email, last_login from auth_user where id=$UID_IPB;" | sed 's/^/  /'
echo "  (empty last_login = not recorded, not proof of no use)"

h "1. any token or session tables at all"
Q "select table_name from information_schema.tables
   where table_schema='public' and (table_name like '%token%' or table_name like '%session%');" \
  | sed 's/^/  /'

h "2. read-side API traffic since 2026-09-10, by day, request and client"
L=$($D logs --timestamps --since 2026-09-10T00:00:00 $W 2>&1 \
  | grep -E '"(GET|POST) /api/' | grep -v -E '"POST /api/(video|timeseries)/')
echo "  matching lines: $(printf '%s\n' "$L" | grep -c .)"
echo "  --- three raw samples, so the format can be checked ---"
printf '%s\n' "$L" | head -3 | cut -c1-300 | sed 's/^/  /'
echo "  --- day | request | client ---"
printf '%s\n' "$L" | grep . | awk '
  { day=substr($1,1,10)
    match($0, /"(GET|POST) \/api\/[a-z_]+/); req=substr($0, RSTART+1, RLENGTH-1)
    ua="other"
    if ($0 ~ /Python-urllib/) ua="urllib (our partner client)"
    else if ($0 ~ /python-requests/) ua="python-requests (ORC-OS)"
    else if ($0 ~ /curl\//) ua="curl (us)"
    else if ($0 ~ /Mozilla/) ua="browser"
    print day " | " req " | " ua }' \
  | sort | uniq -c | sed 's/^/  /'
