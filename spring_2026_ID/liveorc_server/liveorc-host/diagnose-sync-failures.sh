#!/usr/bin/env bash
# diagnose-sync-failures.sh — did the station's uploads reach us, and did WE refuse them?
#
# TODO-119 Track 1, the zero-metered-bytes half. Sukabumi's video sync collapsed
# 2026-08-23 and has only partly recovered. Three explanations fit and none is
# excluded: carrier action on the traffic, a path-MTU blackhole, or something
# server-side. This checks the third, and it is the one that can be checked
# without spending a byte on the station's SIM.
#
# The point of asking here first: a self-inflicted block - fail2ban, a request
# size cap, a rate limit - is completely invisible from the station. It would
# look exactly like a bad link.
#
# READ-ONLY. Reads logs and config, prints counts. Changes nothing, restarts
# nothing. Safe to run on production at any time.
#
#   ./diagnose-sync-failures.sh              # default window 2026-08-23..2026-08-27
#   ./diagnose-sync-failures.sh 2026-09-01 2026-09-02
set -u
FROM="${1:-2026-08-23}"
TO="${2:-2026-08-27}"
D=docker; docker ps >/dev/null 2>&1 || D="sudo docker"
h(){ printf '\n\033[1m== %s ==\033[0m\n' "$*"; }

h "window under examination"
echo "  $FROM .. $TO   (station clock is UTC; WIB = UTC+7)"

h "1. which container terminates TLS for the station"
$D ps --format '{{.Names}}\t{{.Image}}\t{{.Ports}}' 2>&1 | sed 's/^/  /'
NGX=$($D ps --format '{{.Names}}' 2>/dev/null | grep -iE 'nginx|proxy|web' | head -1)
echo "  -> assuming: ${NGX:-NONE FOUND}"

h "2. do the logs even reach back that far"
# This is the question that decides whether the rest is meaningful. nginx rotates,
# and 08-23 is well over a week ago.
if [ -n "${NGX:-}" ]; then
  $D exec "$NGX" sh -c 'ls -la /var/log/nginx/ 2>/dev/null' 2>&1 | sed 's/^/  /' | head -20
  echo "  --- oldest and newest access-log entries actually present ---"
  $D exec "$NGX" sh -c '
    for f in /var/log/nginx/access.log*; do [ -f "$f" ] || continue
      case "$f" in *.gz) C="zcat";; *) C="cat";; esac
      echo "  $f: $($C "$f" 2>/dev/null | head -1 | grep -oE "\[[^]]+\]" | head -1) .. $($C "$f" 2>/dev/null | tail -1 | grep -oE "\[[^]]+\]" | head -1)"
    done' 2>&1 | sed 's/^/  /'
else echo "  no nginx container identified — inspect the ps output above"; fi

h "3. did the station's requests ARRIVE, and what did we answer"
# The station posts video to /api/video/ and refreshes at /api/token/refresh/.
# Its source IP is a dynamic Telkomsel address, so match on the endpoints.
if [ -n "${NGX:-}" ]; then
  $D exec "$NGX" sh -c '
    for f in /var/log/nginx/access.log*; do [ -f "$f" ] || continue
      case "$f" in *.gz) C="zcat";; *) C="cat";; esac
      $C "$f" 2>/dev/null
    done' 2>/dev/null |
    grep -E "POST /api/(video|token)" |
    awk -v a="$FROM" -v b="$TO" '
      { if (match($0,/\[[0-9]{2}\/[A-Za-z]{3}\/[0-9]{4}/)) {
          d=substr($0,RSTART+1,11); split(d,p,"/")
          m=index("JanFebMarAprMayJunJulAugSepOctNovDec",p[2]); m=(m+2)/3
          iso=sprintf("%s-%02d-%s",p[3],m,p[1])
          if (iso>=a && iso<=b) { ep=($7~/token/)?"token":"video"
            for(i=1;i<=NF;i++) if ($i ~ /^"(POST)/) { code=$(i+3) }
            print iso, ep, $9 } } }' |
    sort | uniq -c | sort -rn | head -30 | sed 's/^/  /'
  echo "  (blank above = the station's requests never reached nginx in this window)"
fi

h "4. nginx error log — resets, timeouts, clients giving up"
if [ -n "${NGX:-}" ]; then
  $D exec "$NGX" sh -c '
    for f in /var/log/nginx/error.log*; do [ -f "$f" ] || continue
      case "$f" in *.gz) C="zcat";; *) C="cat";; esac
      $C "$f" 2>/dev/null
    done' 2>/dev/null |
    grep -iE "reset by peer|timed out|client closed|too large|upstream" |
    sed 's/, client:.*//' | sort | uniq -c | sort -rn | head -20 | sed 's/^/  /'
  echo "  (499 in the access log = client gave up first; 413 = we refused the size)"
fi

h "5. is nginx configured to refuse a 9.2 MB upload, or to rate-limit"
# A client_max_body_size below ~10m would reject every video with 413, and a
# limit_req zone would throttle a burst. Either is invisible from the station.
if [ -n "${NGX:-}" ]; then
  $D exec "$NGX" sh -c 'grep -rniE "client_max_body_size|limit_req|limit_conn|client_body_timeout|send_timeout|keepalive_timeout" /etc/nginx/ 2>/dev/null' 2>&1 |
    sed 's/^/  /' | head -20
  echo "  (no client_max_body_size anywhere means the nginx default of 1m applies)"
fi

h "6. fail2ban — a ban would be entirely invisible from the station"
if command -v fail2ban-client >/dev/null 2>&1; then
  sudo fail2ban-client status 2>&1 | sed 's/^/  /'
  for j in $(sudo fail2ban-client status 2>/dev/null | sed -n 's/.*Jail list:\s*//p' | tr ',' ' '); do
    echo "  --- jail $j ---"; sudo fail2ban-client status "$j" 2>&1 | sed 's/^/    /'
  done
  echo "  --- ban/unban actions in the window ---"
  sudo grep -hE "Ban|Unban" /var/log/fail2ban.log* 2>/dev/null | tail -20 | sed 's/^/  /'
else
  echo "  fail2ban-client not installed — not the cause, and one explanation eliminated"
fi

h "7. host-level firewall"
sudo iptables -S 2>/dev/null | grep -viE "^-P|ACCEPT$" | head -15 | sed 's/^/  /'
echo "  (security-group rules are NOT visible from here — check the EC2 console separately)"

h "done — nothing was changed"
