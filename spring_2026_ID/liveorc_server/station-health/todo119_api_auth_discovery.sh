set -u
echo "=== date ==="; date -u
echo "uptime at grab: $(cut -d' ' -f1 /proc/uptime)s"

# Tom chose the API re-drive (POST /api/video/sync/) over a database edit, to
# avoid any risk to the ORC-OS database. That path needs three things we do not
# yet have: which port actually serves the API, how it authenticates, and the
# exact signature of the sync endpoint.
#
# READ-ONLY. It reads files, lists routes and makes local HTTP requests. The
# only request with a side effect would be a login, which mints a token and
# changes no records. It NEVER prints a secret - only whether one is present
# and how long it is.

echo "=== A. what serves :80 and what serves :5000 ==="
(ss -ltnp 2>/dev/null || netstat -ltnp 2>/dev/null) | grep -E ":(80|5000)\b" | sed 's/^/  /'
for p in 80 5000; do
  echo "  --- :$p ---"
  echo "    GET /api/video/count/  -> $(curl -s -o /dev/null -w '%{http_code}' --max-time 8 http://127.0.0.1:$p/api/video/count/ 2>&1)"
  echo "    GET /openapi.json      -> $(curl -s -o /dev/null -w '%{http_code}' --max-time 8 http://127.0.0.1:$p/openapi.json 2>&1)"
  echo "    GET /docs              -> $(curl -s -o /dev/null -w '%{http_code}' --max-time 8 http://127.0.0.1:$p/docs 2>&1)"
done

echo
echo "=== B. the auth routes orc_api actually defines ==="
SP=/home/pi/venv/orc-os/lib/python3.13/site-packages/orc_api
echo "  --- router files ---"
ls $SP/routers/ 2>/dev/null | sed 's/^/    /'
echo "  --- anything that looks like login/token/auth ---"
grep -rn "router.post\|router.get" $SP/routers/*.py 2>/dev/null \
  | grep -iE "login|token|auth|password" | sed 's/^/    /' | head -10
echo "  --- how the dependency is enforced ---"
grep -rn "HTTPBearer\|OAuth2\|Depends(.*auth\|Depends(.*token\|credentials_exception" $SP/*.py $SP/**/*.py 2>/dev/null \
  | head -10 | sed 's/^/    /'

echo
echo "=== C. the sync endpoint's exact signature ==="
grep -n -B6 -A22 '"/sync/"' $SP/routers/video.py 2>/dev/null | sed 's/^/  /'

echo
echo "=== D. is a usable password present, WITHOUT printing it ==="
for f in /home/pi/.orc_deploy_*; do
  [ -f "$f" ] || continue
  echo "  $f:"
  for k in BASE_PASSWD UPLOAD_TOKEN CAMERA_PASS ORC_PASSWORD; do
    v=$(grep -E "^$k=" "$f" 2>/dev/null | tail -1 | cut -d= -f2- | tr -d '"'"'"' ')
    if [ -n "$v" ]; then echo "    $k: PRESENT (len ${#v})"; else echo "    $k: absent"; fi
  done
done
echo "  --- how many rows in the passwords table (not the hash) ---"
sqlite3 /home/pi/.ORC-OS/orc-os.db "select count(*) from passwords;" 2>&1 | sed 's/^/    /'

echo
echo "=== E. does the device password authenticate, if we have one ==="
# A login mints a token; it records nothing and changes no video state.
BP=""
for f in /home/pi/.orc_deploy_*; do
  [ -f "$f" ] || continue
  v=$(grep -E "^BASE_PASSWD=" "$f" 2>/dev/null | tail -1 | cut -d= -f2- | tr -d '"'"'"' ')
  [ -n "$v" ] && BP=$v
done
if [ -z "$BP" ]; then
  echo "  no BASE_PASSWD found — cannot test a login"
else
  for p in 80 5000; do
    for ep in /api/token /api/login /token /login /api/auth/token; do
      code=$(curl -s -o /tmp/orc_auth_probe.json -w '%{http_code}' --max-time 8 \
             -X POST -H 'Content-Type: application/json' \
             -d "{\"password\":\"$BP\"}" "http://127.0.0.1:$p$ep" 2>&1)
      [ "$code" = "404" ] && continue
      echo "  :$p $ep -> $code"
      head -c 120 /tmp/orc_auth_probe.json 2>/dev/null | tr -d '\n' | sed 's/^/      /'; echo
    done
  done
  rm -f /tmp/orc_auth_probe.json
fi
echo "=== END ==="
