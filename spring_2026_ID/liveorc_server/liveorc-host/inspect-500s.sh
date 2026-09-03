#!/usr/bin/env bash
# inspect-500s.sh — why is LiveORC returning 500 on POST /api/video/?
#
# TODO-119. inspect-refusals.sh established the fact on 2026-09-03:
#
#   [03/Sep/2026:07:31:58 +0000] "POST /api/video/ HTTP/1.0" 500 145 "python-requests/2.32.3"
#   [03/Sep/2026:10:31:56 +0000] "POST /api/video/ HTTP/1.0" 500 145 "python-requests/2.32.3"
#
# The station's uploads ARRIVED and LiveORC threw an unhandled server error.
# Not a size cap (client_max_body_size is 512M), not a proxy timeout
# (proxy_read_timeout 300000s), no fail2ban, no rate limiting. The 145-byte
# body is Django's minimal DEBUG=False error page, which is not JSON - which is
# why ORC-OS's base.py:47 raised JSONDecodeError and destroyed the status code
# before logging it.
#
# Two things are still unknown and both matter more than the fact itself:
#   1. WHAT the exception was. Section 3 dumps the app log unfiltered around
#      each 500, which is where a Django traceback would be.
#   2. HOW OFTEN. Two in one day is either noise or a fraction of every upload.
#      Track 2's answer is that 1,190 clips need uploading; if the server 500s
#      on a slice of them, the re-drive will hit it 1,190 times. Section 4
#      counts every /api/ status over 14 days to get the rate.
#
# WHY THIS READS docker logs AND NOT /var/log/nginx
# The first version read /var/log/nginx/access.log inside the container and
# found one blank line, so its section 3 reported "NOTHING - the requests never
# arrived", which was exactly backwards. liveorc_webapp logs to Docker's json
# driver. The answer only surfaced because a different section happened to use
# `docker logs`. Reading the wrong file looked identical to a real finding.
#
# READ-ONLY. Reads container logs. Starts nothing, restarts nothing.
#
# USAGE (on the LiveORC host, in ~/code/git/openrivercam after a git pull)
#   ./spring_2026_ID/liveorc_server/liveorc-host/inspect-500s.sh
#   ./inspect-500s.sh --days 30
#   ./inspect-500s.sh --context 300 '2026-09-03 07:31:58'
set -u

DAYS=14; CONTEXT=90
while [ $# -gt 0 ]; do
  case "$1" in
    --days) DAYS="$2"; shift 2;;
    --context) CONTEXT="$2"; shift 2;;
    *) break;;
  esac
done
if [ $# -gt 0 ]; then TARGETS=("$@")
else TARGETS=('2026-09-03 07:31:58' '2026-09-03 10:31:56'); fi

D=docker; docker ps >/dev/null 2>&1 || D="sudo docker"
C=liveorc_webapp
h(){ printf '\n\033[1m== %s ==\033[0m\n' "$*"; }

h "0. what this is reading"
echo "  container: $C   (logs via the docker json driver, NOT /var/log/nginx)"
echo "  rate window: last ${DAYS} days"
echo "  traceback context: +/- ${CONTEXT}s around each target"
$D ps --format '{{.Names}}\t{{.Status}}' 2>/dev/null | grep "^$C" | sed 's/^/  /'

for T in "${TARGETS[@]}"; do
  h "3. $T UTC — the app log, UNFILTERED, around the 500"
  FROM=$(date -u -d "$T UTC -${CONTEXT} seconds" '+%Y-%m-%dT%H:%M:%SZ' 2>/dev/null)
  TO=$(date -u -d "$T UTC +${CONTEXT} seconds" '+%Y-%m-%dT%H:%M:%SZ' 2>/dev/null)
  if [ -z "$FROM" ]; then echo "  could not parse '$T'"; continue; fi
  echo "  window: $FROM .. $TO"
  echo "  --- everything, in order. A Django traceback will be a run of"
  echo "      indented File \"...\" lines ending in an exception class. ---"
  $D logs --since "$FROM" --until "$TO" "$C" 2>&1 \
    | head -200 | cut -c1-300 | sed 's/^/    /'
  echo "  --- and the exception lines alone, if the dump above is noisy ---"
  $D logs --since "$FROM" --until "$TO" "$C" 2>&1 \
    | grep -iE "traceback|^[A-Za-z_.]+(Error|Exception|DoesNotExist)|File \"" \
    | head -40 | cut -c1-300 | sed 's/^/    /'
done

h "4. THE RATE — every /api/ response status over ${DAYS} days"
SINCE=$(date -u -d "-${DAYS} days" '+%Y-%m-%dT%H:%M:%SZ' 2>/dev/null)
LOG=$($D logs --since "$SINCE" "$C" 2>&1 | grep -E '"(GET|POST|PATCH|PUT) /api/')
echo "  /api/ request lines in window: $(printf '%s\n' "$LOG" | grep -c .)"
echo "  --- by endpoint and status ---"
printf '%s\n' "$LOG" | awk '{
    for(i=1;i<=NF;i++) if($i ~ /^"(GET|POST|PATCH|PUT)$/){ m=substr($i,2); p=$(i+1); s=$(i+3); break }
    if (p != "") { sub(/\?.*/,"",p); print s"  "m" "p }
  }' | sort | uniq -c | sort -rn | head -30 | sed 's/^/    /'

echo "  --- POST /api/video/ only: success vs failure ---"
printf '%s\n' "$LOG" | grep '"POST /api/video/' | awk '{
    for(i=1;i<=NF;i++) if($i ~ /^"POST$/){ print $(i+3); break }
  }' | sort | uniq -c | sort -rn | sed 's/^/    /'

echo "  --- every 5xx on /api/, with its timestamp ---"
printf '%s\n' "$LOG" | awk '{
    for(i=1;i<=NF;i++) if($i ~ /^"(GET|POST|PATCH|PUT)$/){ s=$(i+3); break }
    if (s ~ /^5/) print
  }' | cut -c1-220 | sed 's/^/    /'

h "5. do the 500s cluster in time, or by clip size"
printf '%s\n' "$LOG" | awk '{
    for(i=1;i<=NF;i++) if($i ~ /^"(GET|POST|PATCH|PUT)$/){ s=$(i+3); break }
    if (s ~ /^5/ && match($0,/\[[0-9]{2}\/[A-Za-z]{3}\/[0-9]{4}/)) print substr($0,RSTART+1,11)
  }' | sort | uniq -c | sed 's/^/    /'
echo "  (a flat rate across days means it is a property of the upload;"
echo "   a spike on one day means it is an incident with a start and an end.)"

h "done"
echo "  Read-only. Nothing was changed."
echo "  Paste back section 3's exception lines and section 4's POST /api/video/"
echo "  tally - those two decide whether the re-drive is safe to fire."
