set -u
SP=/home/pi/venv/orc-os/lib/python3.13/site-packages/orc_api
echo "=== date ==="; date -u

# Follow-up to apiroutes119w. The sync route carries NO auth dependency, yet
# :5000 returns 401 for every path including /openapi.json - so the 401 comes
# from app-wide middleware. This pins down exactly what that middleware wants,
# and whether nginx on :80 exposes any path that reaches the app unauthenticated.
#
# STRICTLY READ-ONLY AND CREDENTIAL-FREE. Reads source and config, makes
# unauthenticated GETs. Sends no password and reads no password file.

echo "=== A. the middleware that produces the 401 ==="
grep -n "@app.middleware\|async def .*middleware\|Depends(\|dependencies=" $SP/main.py 2>/dev/null | head -20 | sed 's/^/  /'
echo "  --- the middleware body, whatever it turns out to be ---"
sed -n '/@app.middleware/,/^app\.\|^@app\.\(get\|post\)/p' $SP/main.py 2>/dev/null | head -45 | sed 's/^/  /'

echo
echo "=== B. exempt paths, if the middleware has a whitelist ==="
grep -n "EXEMPT\|exempt\|skip\|allow\|public\|startswith\|path ==\|/login\|/docs\|openapi" $SP/main.py 2>/dev/null | head -20 | sed 's/^/  /'

echo
echo "=== C. the login route and the router's prefix ==="
grep -n "prefix\|APIRouter(" $SP/routers/auth.py 2>/dev/null | sed 's/^/  /'
sed -n '30,62p' $SP/routers/auth.py 2>/dev/null | sed 's/^/  /'

echo
echo "=== D. is a password even set (count only, never the hash) ==="
sqlite3 /home/pi/.ORC-OS/orc-os.db "select count(*) from passwords;" 2>&1 | sed 's/^/  rows: /'
echo "  (0 rows would mean set_password/ is reachable without a token and no"
echo "   secret exists yet; 1 row means a password is set and is required)"

echo
echo "=== E. what nginx actually proxies vs serves ==="
cat /etc/nginx/sites-enabled/orc-os 2>/dev/null | grep -vE "^\s*#|^\s*$" | head -40 | sed 's/^/  /'

echo
echo "=== F. is :80 /openapi.json really the schema, or the SPA index ==="
echo "  first 120 bytes:"
curl -s --max-time 6 http://127.0.0.1:80/openapi.json 2>&1 | head -c 120 | sed 's/^/    /'; echo
echo "  content-type: $(curl -s -o /dev/null -w '%{content_type}' --max-time 6 http://127.0.0.1:80/openapi.json 2>&1)"
echo "=== END ==="
