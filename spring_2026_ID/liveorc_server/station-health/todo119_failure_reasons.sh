set -u
DB=/home/pi/.ORC-OS/orc-os.db
echo "=== SAMPLE $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "uptime at grab: $(cut -d' ' -f1 /proc/uptime)s"

# ---------------------------------------------------------------------------
# WHY
#   The 09-02 outage cleared on its own. In the ~18.5 h after it, ~37 clips were
#   captured, 20 synced and 17 failed. One window is not a rate, so this script
#   is written to be run UNCHANGED in several consecutive wakes: section A is
#   the counter sample, and the sections after it explain the failures.
#
#   The decisive question for the remedy Tom chose on 2026-09-03 (keep the token
#   fresh rather than patch the hardcoded timeout) is section B. In
#   schemas/callback_url.py, every get/patch/post refreshes first when
#   `token_expiration < datetime.now()`, and get_set_refresh_tokens POSTs with a
#   hardcoded `timeout=5`. If that POST times out, token_expiration is never
#   advanced - so the NEXT request refreshes too, and so does the one after it.
#   A single failed refresh is therefore self-perpetuating, which is the shape
#   that fits 64% of failures far better than a token genuinely expiring every
#   5 hours (get_token_expiration returns now + 5 h; the station wakes every
#   30 min, so a healthy station should pay a refresh on roughly one wake in
#   ten). Section B distinguishes those two worlds by reading one row.
#
#   Section E is the confirmation from the other end: which line the innermost
#   frame sits on. 115 is the refresh, 172 is the data POST. Token freshness
#   only reaches the 115s.
#
# READ-ONLY. sqlite SELECTs, journalctl, /proc. Nothing is written, no network
# request is made, and nothing is synced.
# ---------------------------------------------------------------------------

echo
echo "=== A. THE SAMPLE: rows by sync_status ==="
sqlite3 -column "$DB" "select ifnull(sync_status,'NULL') as status, count(*)
                       from video group by 1 order by 2 desc;" 2>&1 | sed 's/^/  /'

echo
echo "=== B. TOKEN STATE — is the refresh stuck? ==="
echo "  naive datetime.now() as the code sees it:"
python3 -c "from datetime import datetime; print('   ', datetime.now())" 2>&1
echo "  callback_url row (the app keeps exactly one; crud.add deletes then inserts):"
sqlite3 -line "$DB" "select id, created_at, token_expiration, retry_timeout,
                            length(ifnull(token_access,'')) as access_len,
                            length(ifnull(token_refresh,'')) as refresh_len, url
                     from callback_url;" 2>&1 | sed 's/^/    /'
echo "  READ IT LIKE THIS:"
echo "    token_expiration in the FUTURE -> refresh is not firing; the failures"
echo "      are not the token, and freshness will not reach them."
echo "    token_expiration in the PAST    -> every single request pays a 5 s"
echo "      refresh attempt first, and a failed attempt never advances the"
echo "      timestamp, so it stays stuck. That is the self-perpetuating state."
echo "    created_at tells you when a refresh last SUCCEEDED (the row is"
echo "      replaced wholesale on success), which dates the trap."

echo
echo "=== C. per-clip outcome since 09-03 00:00 UTC — which wakes worked ==="
sqlite3 -column "$DB" "select id, ifnull(sync_status,'NULL'), timestamp
                       from video where timestamp >= '2026-09-03 00:00:00'
                       order by id desc limit 24;" 2>&1 | sed 's/^/  /'

echo
echo "=== D. failure reasons SINCE THE OUTAGE CLEARED (09-03 01:30 UTC) ==="
L=$(journalctl --since '2026-09-03 01:30:00' --no-pager -o cat 2>/dev/null)
echo "  --- one line per failed sync, tallied by error class ---"
printf '%s' "$L" | grep 'Error syncing video to remote site' \
  | grep -oE 'read timeout=[0-9.]+|ConnectTimeout|RemoteDisconnected|ConnectionReset|SSLError|Max retries' \
  | sort | uniq -c | sort -rn | sed 's/^/    /'
echo "  --- total failed-sync lines in the window ---"
printf '%s' "$L" | grep -c 'Error syncing video to remote site' | sed 's/^/    /'
echo "  --- anything that matched none of the classes above (would be missed) ---"
printf '%s' "$L" | grep 'Error syncing video to remote site' \
  | grep -vE 'read timeout=[0-9.]+|ConnectTimeout|RemoteDisconnected|ConnectionReset|SSLError|Max retries' \
  | tail -5 | cut -c1-200 | sed 's/^/    /'

echo
echo "=== E. innermost frame: 115 (refresh) vs 172 (data POST) ==="
printf '%s' "$L" | grep -oE 'callback_url\.py", line [0-9]+' \
  | sort | uniq -c | sort -rn | sed 's/^/    /'
echo "    (line 115 = get_set_refresh_tokens, hardcoded timeout=5, what the"
echo "     token-freshness remedy removes. 172 = the data POST, which it does not.)"

echo
echo "=== F. the shutdown race, this wake and the last few ==="
journalctl --since '2026-09-03 01:30:00' --no-pager 2>/dev/null \
  | grep -iE "videos left to synchronize|Starting sync of videos|Shutting down|shutdown" \
  | tail -16 | sed 's/^/  /'

echo "=== END ==="
