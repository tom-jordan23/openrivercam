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

# ---------------------------------------------------------------------------
# ADDED AFTER SAMPLE 1 (2026-09-03 16:30 UTC). Sections A-F above are unchanged
# so the counter samples stay comparable across wakes.
#
# Sample 1 made the aggregate tally in E ambiguous. It counted every
# callback_url frame in the window, not the innermost frame per failure, and
# the numbers only resolve once you know what each line is:
#   line  91 = the __getattr__ retry wrapper, present in EVERY traceback (12)
#   line 171 = `self.get_set_refresh_tokens()`, the refresh CALL SITE inside post() (5)
#   line 115 = `requests.post(..., timeout=5)` inside the refresh itself (5)
#   line 172 = the data POST, which the token remedy does not touch (2)
# So 171 and 115 are the same five failures seen at two depths, not ten.
#
# What sample 1 could NOT answer: WHICH failures those were. The token was
# valid from 09:31:55 to 14:31:55 (created_at + 5 h), yet failures landed at
# 10:31 and 12:01, inside that valid window. Either the refresh is triggered
# from a path other than post()'s guard, or the frame belongs to a different
# failure than the timestamps suggest. An aggregate cannot tell them apart.
# Section G pairs each failure with its own innermost frame.
# ---------------------------------------------------------------------------

echo
echo "=== G. PER-FAILURE: timestamp, innermost callback_url frame, error ==="
printf '%s' "$L" | awk '
  /ERROR - Error syncing video to remote site/ {
    if (ts != "") print ts "  frame=" (frame == "" ? "none" : frame) "  " err
    ts = $1 " " $2
    err = $0
    sub(/.*Error syncing video to remote site: /, "", err)
    err = substr(err, 1, 90)
    frame = ""
    n = 0
    next
  }
  ts != "" {
    n++
    if (n > 80) next
    if (match($0, /callback_url\.py", line [0-9]+/)) {
      f = substr($0, RSTART, RLENGTH)
      sub(/callback_url\.py", /, "", f)
      if (f !~ /line 91$/) frame = f
    }
  }
  END { if (ts != "") print ts "  frame=" (frame == "" ? "none" : frame) "  " err }
' | sed 's/^/  /'
echo "  (frame=line 115 -> died in the token refresh: token freshness reaches it."
echo "   frame=line 172 -> died in the data POST: it does not.)"

echo
echo "=== H. when did the token actually refresh — journal evidence ==="
printf '%s' "$L" | grep -iE "token|refresh" | grep -viE "sensors\]" \
  | tail -20 | cut -c1-180 | sed 's/^/  /'
echo "  (the callback_url row only remembers the LAST successful refresh, so"
echo "   the journal is the only place the cadence survives.)"
echo "=== END G/H ==="
