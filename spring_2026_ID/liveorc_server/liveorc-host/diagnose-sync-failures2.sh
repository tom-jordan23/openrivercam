#!/usr/bin/env bash
# diagnose-sync-failures2.sh — follow-up after the first pass returned a null result.
#
# WHAT THE FIRST PASS SETTLED
#   fail2ban is not installed, and host iptables carries nothing but Docker's
#   own chains. Two candidate explanations eliminated for zero metered bytes.
#
# WHAT IT GOT WRONG
#   /var/log/nginx/{access,error}.log are ZERO BYTES, dated the image build.
#   The first script read that as "the station's requests never arrived". That
#   inference is invalid: the files were never written, almost certainly because
#   nginx logs to stdout like most containers do. The request history, if it
#   exists anywhere, is in `docker logs liveorc_webapp`.
#
#   Its client_max_body_size check is equally unsafe. A grep of /etc/nginx that
#   matches nothing does not mean the directive is absent from the RUNNING
#   config - and the logic cuts the other way anyway: if nginx's 1m default
#   really applied, every 9.2 MB upload would 413, yet 2,576 have succeeded.
#
# READ-ONLY. Nothing is changed, nothing restarted.
set -u
FROM="${1:-2026-08-23}"
TO="${2:-2026-08-28}"
W=liveorc_webapp
D=docker; docker ps >/dev/null 2>&1 || D="sudo docker"
h(){ printf '\n\033[1m== %s ==\033[0m\n' "$*"; }

h "A. is nginx even in the request path"
$D exec $W sh -c 'ps aux 2>/dev/null | grep -viE "grep|ps aux" | head -20' 2>&1 | sed 's/^/  /'
echo "  --- what is listening inside the container ---"
$D exec $W sh -c '(ss -ltnp 2>/dev/null || netstat -ltnp 2>/dev/null) | head -12' 2>&1 | sed 's/^/  /'
echo "  (host 443 -> container 8000, host 80 -> 8080; find out what owns each)"

h "B. where nginx actually logs, per its own config"
$D exec $W sh -c 'nginx -T 2>/dev/null | grep -nE "access_log|error_log|listen|ssl_certificate |client_max_body_size|limit_req|proxy_read_timeout|proxy_send_timeout|client_body_timeout"' 2>&1 | sed 's/^/  /' | head -40
echo "  (a bare 'access_log /dev/stdout' or /dev/null explains the empty files)"

h "C. the config files themselves, wherever they live"
$D exec $W sh -c 'find / -xdev -name "*.conf" -path "*nginx*" 2>/dev/null | head -10' 2>&1 | sed 's/^/  /'
$D exec $W sh -c 'grep -rn "client_max_body_size" / --include="*.conf" --include="*.template" 2>/dev/null | head' 2>&1 | sed 's/^/  /'
echo "  (absent everywhere = nginx default 1m, which 9.2 MB uploads would fail)"

h "D. docker's own log — how far back, and how big"
$D inspect $W --format '  log driver: {{.HostConfig.LogConfig.Type}}   opts: {{.HostConfig.LogConfig.Config}}' 2>&1
$D inspect $W --format '  container started: {{.State.StartedAt}}' 2>&1
echo "  --- first and last lines docker holds ---"
$D logs $W 2>&1 | head -2 | sed 's/^/  /'
echo "  ..."
$D logs $W 2>&1 | tail -2 | sed 's/^/  /'
echo "  --- total lines retained ---"
$D logs $W 2>&1 | wc -l | sed 's/^/  /'

h "E. THE QUESTION: did the station's uploads arrive, $FROM..$TO"
$D logs $W --since "${FROM}T00:00:00" --until "${TO}T00:00:00" 2>&1 |
  grep -E "POST /api/(video|token)" |
  awk '{for(i=1;i<=NF;i++) if ($i ~ /^"POST/) {ep=$(i+1); code=$(i+3)}
        sub(/\?.*/,"",ep); print ep, code}' |
  sort | uniq -c | sort -rn | head -20 | sed 's/^/  /'
echo "  (nothing here means docker's log does not reach that window either,"
echo "   NOT that the requests were absent - check section D before concluding)"

h "F. any refusal or cutoff we issued, same window"
$D logs $W --since "${FROM}T00:00:00" --until "${TO}T00:00:00" 2>&1 |
  grep -iE " 413 | 499 | 502 | 503 | 504 |reset by peer|client closed|body too large|timed out" |
  sed 's/, client:.*//' | sort | uniq -c | sort -rn | head -15 | sed 's/^/  /'
echo "  (413 = we refused the size; 499 = client gave up; 5xx = we failed)"

h "G. for comparison: the same counts for the last 2 days, when sync works"
$D logs $W --since "$(date -u -d '2 days ago' +%Y-%m-%dT%H:%M:%S)" 2>&1 |
  grep -E "POST /api/(video|token)" |
  awk '{for(i=1;i<=NF;i++) if ($i ~ /^"POST/) {ep=$(i+1); code=$(i+3)}
        sub(/\?.*/,"",ep); print ep, code}' |
  sort | uniq -c | sort -rn | head -12 | sed 's/^/  /'
echo "  (a working baseline makes the broken window interpretable)"

h "done — nothing was changed"
