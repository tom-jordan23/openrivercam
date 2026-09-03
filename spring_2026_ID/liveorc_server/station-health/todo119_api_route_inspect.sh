set -u
SP=/home/pi/venv/orc-os/lib/python3.13/site-packages/orc_api
echo "=== date ==="; date -u
echo "uptime at grab: $(cut -d' ' -f1 /proc/uptime)s"

# Goal: reach POST /api/video/sync/ so the backlog re-drive never has to touch
# the ORC-OS database, which Tom classified as high risk on 2026-09-03.
#
# STRICTLY READ-ONLY, AND CREDENTIAL-FREE. It reads installed source and makes
# UNAUTHENTICATED local GETs. It does NOT read any password file, does not send
# a credential, and does not write anything. The question it answers is "what
# does this API require", not "can I get in".

echo "=== A. what is listening, and which one is the app ==="
(ss -ltnp 2>/dev/null || netstat -ltnp 2>/dev/null) | grep -E ":(80|5000|8000)\b" | sed 's/^/  /'
echo "  --- unauthenticated probes, no credentials sent ---"
for p in 80 5000; do
  for path in /api/video/count/ /openapi.json /docs /api; do
    echo "    :$p $path -> $(curl -s -o /dev/null -w '%{http_code}' --max-time 6 http://127.0.0.1:$p$path 2>&1)"
  done
done
echo "  (if :5000 answers 200 where :80 answers 401, the auth lives in whatever"
echo "   fronts :80 and the app itself may be reachable directly on :5000)"

echo
echo "=== B. what fronts port 80 ==="
ps aux 2>/dev/null | grep -viE "grep" | grep -iE "nginx|caddy|apache|traefik|node|serve" | head -5 | sed 's/^/  /'
ls /etc/nginx/sites-enabled/ /etc/nginx/conf.d/ 2>/dev/null | sed 's/^/  /'

echo
echo "=== C. the routers orc_api actually installs ==="
ls $SP/routers/ 2>/dev/null | sed 's/^/  /'

echo
echo "=== D. every route the app declares, with its method ==="
grep -rhn "@router\.\(get\|post\|patch\|put\|delete\)" $SP/routers/*.py 2>/dev/null \
  | sed 's/^/  /' | head -40

echo
echo "=== E. is there ANY auth dependency in the app at all ==="
grep -rn "HTTPBearer\|OAuth2\|APIKeyHeader\|Security(\|credentials_exception\|verify_password\|jwt\|JWT" \
  $SP/*.py $SP/routers/*.py $SP/schemas/*.py 2>/dev/null | head -15 | sed 's/^/  /'
echo "  (empty means orc_api declares no auth of its own, and the 401 on :80"
echo "   comes from something in front of it)"

echo
echo "=== F. how main.py assembles the app ==="
grep -n "include_router\|add_middleware\|mount\|CORS" $SP/main.py 2>/dev/null | head -20 | sed 's/^/  /'

echo
echo "=== G. the sync route we want, in full ==="
grep -n -B10 -A28 '"/sync/"' $SP/routers/video.py 2>/dev/null | sed 's/^/  /'

echo "=== END ==="
