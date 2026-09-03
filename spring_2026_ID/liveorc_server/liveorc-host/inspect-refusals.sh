#!/usr/bin/env bash
# inspect-refusals.sh — what did WE answer when the station's upload was refused?
#
# TODO-119. On 2026-09-03 two of Sukabumi's nine post-outage sync failures were
# not timeouts. The station logged only:
#
#   Error syncing video to remote site: Expecting value: line 2 column 1 (char 1)
#
# That text is a JSONDecodeError, and it is a red herring produced by ORC-OS
# itself. schemas/base.py:47 formats its own error message with
# r.json()['detail']; when the response is a non-2xx whose body is NOT JSON,
# r.json() raises, the JSONDecodeError replaces the ValueError, and the status
# code is destroyed before it is ever logged. So the station knows it was
# refused and cannot know how.
#
# The server still knows. This finds out, and costs zero metered bytes on the
# station's SIM.
#
# WHAT WOULD PRODUCE A NON-JSON BODY
#   413 from nginx     - the clip exceeded client_max_body_size (HTML page)
#   502 / 504           - upstream died or timed out (HTML page)
#   500 from Django    - an HTML traceback page, not a DRF JSON error
#   a redirect to HTML - anything terminating in a login page
# Sections 5 and 6 check the config and the app log for each of those, because
# the access log alone gives the code but not the cause.
#
# READ-ONLY. Reads logs and prints config values. Starts nothing, restarts
# nothing, writes nothing. Safe on production at any time.
#
# USAGE (on the LiveORC host, in ~/code/git/openrivercam after a git pull)
#   ./spring_2026_ID/liveorc_server/liveorc-host/inspect-refusals.sh
#   ./inspect-refusals.sh '2026-09-03 07:31:58' '2026-09-03 10:31:56'
#   ./inspect-refusals.sh --window 15 '2026-09-03 07:31:58'
#
# Timestamps are UTC, which is what the station logs. The script converts them
# into whatever offset nginx is writing.
set -u

WINDOW=5
if [ "${1:-}" = "--window" ]; then WINDOW="$2"; shift 2; fi
if [ $# -gt 0 ]; then TARGETS=("$@")
else TARGETS=('2026-09-03 07:31:58' '2026-09-03 10:31:56'); fi

D=docker; docker ps >/dev/null 2>&1 || D="sudo docker"
h(){ printf '\n\033[1m== %s ==\033[0m\n' "$*"; }

h "0. targets"
echo "  window: +/- ${WINDOW} min around each, timestamps given in UTC"
for t in "${TARGETS[@]}"; do echo "    $t"; done

h "1. which container terminates TLS"
$D ps --format '{{.Names}}\t{{.Image}}\t{{.Ports}}' 2>&1 | sed 's/^/  /'
NGX=$($D ps --format '{{.Names}}' 2>/dev/null | grep -iE 'nginx|proxy|web' | head -1)
echo "  -> using: ${NGX:-NONE FOUND}"
[ -z "${NGX:-}" ] && { echo "  cannot continue without an nginx container"; exit 1; }

# Pull the access log once. Low-traffic host, and re-reading it per target
# inside the container is slower than holding it here.
ALL=$($D exec "$NGX" sh -c '
  for f in /var/log/nginx/access.log /var/log/nginx/access.log.1; do
    [ -f "$f" ] && cat "$f"
  done
  for f in /var/log/nginx/access.log.*.gz; do
    [ -f "$f" ] && zcat "$f" 2>/dev/null
  done' 2>/dev/null)
ERR=$($D exec "$NGX" sh -c '
  for f in /var/log/nginx/error.log /var/log/nginx/error.log.1; do
    [ -f "$f" ] && cat "$f"
  done' 2>/dev/null)

h "2. does the log actually cover 2026-09-03, and in what offset"
echo "  access-log lines held: $(printf '%s\n' "$ALL" | wc -l)"
echo "  first: $(printf '%s\n' "$ALL" | head -1 | grep -oE '\[[^]]+\]' | head -1)"
echo "  last:  $(printf '%s\n' "$ALL" | tail -1 | grep -oE '\[[^]]+\]' | head -1)"
OFF=$(printf '%s\n' "$ALL" | tail -1 | grep -oE '\[[^]]+\]' | head -1 | grep -oE '[+-][0-9]{4}')
OFF="${OFF:-+0000}"
echo "  offset nginx is writing: $OFF"
if [ "$OFF" != "+0000" ]; then
  echo "  NOTE: not UTC. Targets are converted below; check the converted line."
fi
SIGN=$(printf '%s' "$OFF" | cut -c1)
OH=$(printf '%s' "$OFF" | cut -c2-3); OM=$(printf '%s' "$OFF" | cut -c4-5)
OSEC=$(( (10#$OH * 3600 + 10#$OM * 60) )); [ "$SIGN" = "-" ] && OSEC=$(( -OSEC ))

for T in "${TARGETS[@]}"; do
  h "3. $T UTC — every request in the window"
  LOCAL=$(date -u -d "$T UTC $OSEC seconds" '+%Y-%m-%d %H:%M:%S' 2>/dev/null)
  if [ -z "$LOCAL" ]; then echo "  could not parse '$T'"; continue; fi
  echo "  in the log's offset that is: $LOCAL"

  # Minute-prefix matching rather than epoch arithmetic: mawk has no mktime,
  # and the container's awk may be busybox. Prefixes are exact and portable.
  PATS=$(mktemp)
  i=$(( -WINDOW ))
  while [ "$i" -le "$WINDOW" ]; do
    date -u -d "$T UTC $OSEC seconds $i minutes" '+%d/%b/%Y:%H:%M' 2>/dev/null >> "$PATS"
    i=$(( i + 1 ))
  done

  HITS=$(printf '%s\n' "$ALL" | grep -F -f "$PATS" 2>/dev/null)
  N=$(printf '%s\n' "$HITS" | grep -c . )
  echo "  matching access-log lines: $N"
  if [ "$N" -gt 0 ]; then
    echo "  --- status codes in the window ---"
    printf '%s\n' "$HITS" | awk '{for(i=1;i<=NF;i++) if($i ~ /^"(GET|POST|PATCH|PUT)$/){print $(i+3); break}}' \
      | sort | uniq -c | sort -rn | sed 's/^/    /'
    echo "  --- every non-2xx, in full (this is the answer if it is here) ---"
    printf '%s\n' "$HITS" | awk '{
        for(i=1;i<=NF;i++) if($i ~ /^"(GET|POST|PATCH|PUT)$/){ s=$(i+3); break }
        if (s !~ /^2/) print
      }' | cut -c1-400 | sed 's/^/    /'
    echo "  --- every /api/ request in the window, in full ---"
    printf '%s\n' "$HITS" | grep -F '/api/' | cut -c1-400 | sed 's/^/    /'
  else
    echo "  NOTHING. If the window is empty the request never reached nginx,"
    echo "  which moves the fault back to the link and makes 413/502/504 moot."
  fi

  echo "  --- nginx error.log in the same window ---"
  EWIN=$(mktemp)
  i=$(( -WINDOW ))
  while [ "$i" -le "$WINDOW" ]; do
    date -u -d "$T UTC $OSEC seconds $i minutes" '+%Y/%m/%d %H:%M' 2>/dev/null >> "$EWIN"
    i=$(( i + 1 ))
  done
  printf '%s\n' "$ERR" | grep -F -f "$EWIN" 2>/dev/null | cut -c1-400 | sed 's/^/    /' \
    || echo "    (none)"
  rm -f "$PATS" "$EWIN"
done

h "5. config that turns a request into a NON-JSON body"
echo "  --- client_max_body_size (a 413 here is an HTML page, and the mean"
echo "      clip is 9.2 MB; nginx defaults to 1 MB if unset) ---"
$D exec "$NGX" sh -c 'grep -rn "client_max_body_size" /etc/nginx/ /liveorc/nginx/ 2>/dev/null' \
  2>&1 | sed 's/^/    /' || true
echo "    (no output above = never set = the 1 MB default applies)"
echo "  --- proxy timeouts (a 504 here is an HTML page) ---"
$D exec "$NGX" sh -c 'grep -rn "proxy_read_timeout\|proxy_send_timeout\|proxy_connect_timeout\|keepalive_timeout" /etc/nginx/ /liveorc/nginx/ 2>/dev/null' \
  2>&1 | sed 's/^/    /' || true
echo "  --- error_page / custom error bodies ---"
$D exec "$NGX" sh -c 'grep -rn "error_page" /etc/nginx/ /liveorc/nginx/ 2>/dev/null' \
  2>&1 | sed 's/^/    /' || true

h "6. the app behind nginx — a Django 500 is also an HTML body"
APP=$($D ps --format '{{.Names}}' 2>/dev/null | grep -viE 'nginx|proxy|db|postgres|redis' | head -3)
echo "  candidate app containers: ${APP:-none}"
for c in $APP; do
  echo "  --- $c, lines mentioning the target minutes ---"
  for T in "${TARGETS[@]}"; do
    STAMP=$(date -u -d "$T UTC" '+%Y-%m-%d %H:%M' 2>/dev/null)
    $D logs --since "$(date -u -d "$T UTC -${WINDOW} minutes" '+%Y-%m-%dT%H:%M:%SZ' 2>/dev/null)" \
            --until "$(date -u -d "$T UTC +${WINDOW} minutes" '+%Y-%m-%dT%H:%M:%SZ' 2>/dev/null)" \
            "$c" 2>&1 | grep -iE "error|exception|traceback|500|502|413|refused|denied" \
      | head -20 | cut -c1-300 | sed "s/^/    [$STAMP] /"
  done
done

h "7. is anything blocking the station on purpose"
$D ps --format '{{.Names}}' 2>/dev/null | grep -i fail2ban >/dev/null 2>&1 \
  && $D exec "$(${D} ps --format '{{.Names}}' | grep -i fail2ban | head -1)" fail2ban-client status 2>&1 | sed 's/^/  /' \
  || echo "  no fail2ban container"
command -v fail2ban-client >/dev/null 2>&1 && sudo fail2ban-client status 2>&1 | sed 's/^/  /' \
  || echo "  no fail2ban on the host"
echo "  --- rate limiting in nginx config ---"
$D exec "$NGX" sh -c 'grep -rn "limit_req\|limit_conn" /etc/nginx/ /liveorc/nginx/ 2>/dev/null' \
  2>&1 | sed 's/^/    /' || true

h "done"
echo "  Read-only. Nothing was changed."
echo "  The line that matters is the non-2xx in section 3. If section 3 is"
echo "  empty for both targets, the requests never arrived and the refusal"
echo "  theory is dead."
