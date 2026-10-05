#!/usr/bin/env bash
# check-ipb-api-usage.sh — has IPB ever used its LiveORC API account?
#
# The IPB service account is user_id 19 (ipb-dashboard@liveorc.local), handed
# over after the 2026-09-09 verification run. The question can't be answered
# from the workstation: the Grafana datasource is the sensor DB (orc), not
# LiveORC's Django DB.
#
# Section 1 gives the definitive answer. LiveORC runs simplejwt with
# BLACKLIST_AFTER_ROTATION, so the token_blacklist app is installed. That app
# writes a token_blacklist_outstandingtoken row, with user_id and created_at,
# for every refresh token it issues. Each login (POST /api/token/) and each
# refresh (/api/token/refresh/, which rotates) adds a row. Our own 2026-09-09
# matrix run accounts for the rows that day. A row with a later date is IPB,
# unless someone on our side ran the account again since.
#
# auth last_login is shown too, but simplejwt only updates it when
# UPDATE_LAST_LOGIN is set. Treat an empty value as "not recorded", not as
# "never logged in".
#
# Section 2 is supporting evidence only. The access log records the path and
# the client IP but not the user, and docker logs only go back to the last
# container restart.
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

h "0. which user table, and is it the right account"
UT=$(Q "select table_name from information_schema.columns
        where column_name='last_login' and table_schema='public' limit 1;")
echo "  user table: ${UT:-<not found>}"
[ -n "$UT" ] && Q "select id, email, last_login, date_joined from $UT where id=$UID_IPB;" 2>&1 \
  | sed 's/^/  /' || true
echo "  (an error naming email/date_joined just means different column names; section 1 still stands)"

h "1. refresh tokens issued to this account, by day (UTC) — the answer"
Q "select date(created_at), count(*) from token_blacklist_outstandingtoken
   where user_id=$UID_IPB group by 1 order by 1;" | sed 's/^/  /'
echo "  --- first and last issue, and how many were spent by rotation ---"
Q "select min(o.created_at), max(o.created_at), count(*), count(b.id)
   from token_blacklist_outstandingtoken o
   left join token_blacklist_blacklistedtoken b on b.token_id=o.id
   where o.user_id=$UID_IPB;" | sed 's/^/  /'
echo "  (columns: first | last | issued | blacklisted)"
echo "  only 2026-09-09 rows -> nobody has logged in since our verification run"
echo "  --- the same for every account, for comparison ---"
Q "select user_id, count(*), max(created_at) from token_blacklist_outstandingtoken
   group by 1 order by 1;" | sed 's/^/  /'

h "2. API traffic in the webapp access log since 2026-09-10 (supporting only)"
echo "  log held from: $($D logs $W 2>&1 | head -1 | cut -c1-80)"
$D logs $W --since 2026-09-10T00:00:00 2>&1 \
  | grep -E '"(GET|POST) /api/(token|site|timeseries|video|cross)' \
  | grep -v -E '"POST /api/(video|timeseries)/' \
  | awk '{print $1}' | sort | uniq -c | sort -rn | head -20 | sed 's/^/  /'
echo "  (count per client IP; the station's own uploads are filtered out)"
