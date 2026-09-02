#!/usr/bin/env python3
"""TODO-119 Track 2: size the newest-first re-drive, and check it can succeed.

THE DECISION THIS SERVES
    Tom, 2026-09-02: the un-synced clips are unprocessed video and we want them
    for a more complete record. Upload them, NEWEST FIRST, backfilling the
    historic tail as we are able. That turns Track 2 from a question into a job,
    and this grab is what sizes the job.

WHAT IT MUST ESTABLISH, IN ORDER OF WHAT IT WOULD CHANGE

    Q19  Is sync working RIGHT NOW? Baseline 2026-09-01 22:00 UTC was
         SYNCED 2546 / FAILED 2978 / LOCAL 126. If SYNCED has climbed and
         recent captures carry a remote_id, the link currently works and a
         re-drive has a real chance. If it has not, a bulk re-drive spends
         metered bytes on 201-failures-in-five-days odds. This is the Track 1
         first item and it now gates Track 2 as well.

    Q20  The work plan itself: un-synced rows that STILL HAVE THEIR FILE,
         bucketed by day, newest first, with megabytes. This is the ordered
         list the re-drive walks, and the per-day sizes set the window size.
         Aggregated on the station so the answer costs ~60 lines, not 1,190.

    Q21  The deletion clock, which now matters far more than it did. Tom wants
         the historic record, and the disk manager eats the OLDEST end first —
         1,911 rows have already lost their files that way. So newest-first
         upload and the purge work on opposite ends of the same backlog. Read
         min_free_space's units OUT OF THE SOURCE that consumes it rather than
         inferring them from one purge, and read free space alongside.

    Q22  The cost gate. 10.69 GB on the prepaid SIM whose exhaustion caused
         ISS-FIELD-011, and nothing watches the balance. Modem/interface byte
         counters will not give the balance, but they give consumption to date,
         which is the closest thing on the station to a budget.

READ-ONLY. sqlite selects, stat/df, source greps, and interface counters. It
writes nothing on the station, starts nothing there, and fires no re-drive.
"""
import subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import station_watch as sw  # noqa: E402

HOST, USER = "orc-sukabumi", "pi"
OUT = HERE.parents[2] / "data" / "station-forensics"

CMD = r"""
DB=$(ls /home/pi/.ORC-OS/orc-os.db 2>/dev/null | head -1)
echo '=== date (station is UTC; +7 for WIB) ==='; date -u

echo '=== Q19: sync tally now vs 2546/2978/126 at 09-01 22:00 UTC ==='
sqlite3 -header -column "$DB" "select sync_status, count(*) n from video group by 1 order by 2 desc;" 2>&1
echo '--- newest 12 rows: is what we capture now reaching the server? ---'
sqlite3 -header -column "$DB" \
  "select datetime(timestamp) ts, sync_status, remote_id, (file is not null) has_file
     from video order by timestamp desc limit 12;" 2>&1
echo '--- SYNCED count by day, last 10 days (climbing = link works now) ---'
sqlite3 -column "$DB" \
  "select date(timestamp), sync_status, count(*) from video
    where timestamp > datetime('now','-10 days') group by 1,2 order by 1 desc,3 desc;" 2>&1

echo '=== Q20: the newest-first work plan — unsynced rows that still have a file ==='
echo '--- shape of the file column (3 samples) ---'
sqlite3 "$DB" "select file from video where file is not null limit 3;" 2>&1
echo '--- video tree(s) on disk ---'
find /home/pi -maxdepth 5 -type d -name videos 2>/dev/null | head -5
echo '--- per-day: count and MB of EXTANT unsynced files, newest first ---'
sqlite3 "$DB" "select date(timestamp)||'|'||file from video
                where sync_status is not null and sync_status<>'SYNCED'
                  and file is not null order by timestamp desc;" 2>/dev/null |
while IFS='|' read -r d f; do
  p=""
  for cand in "$f" "/home/pi/$f" "/home/pi/.ORC-OS/$f"; do
    [ -f "$cand" ] && { p="$cand"; break; }
  done
  [ -n "$p" ] && echo "$d $(stat -c%s "$p" 2>/dev/null || echo 0)"
done | awk '{n[$1]++; b[$1]+=$2}
            END {for (k in n) printf "%s  %5d files  %9.1f MB\n", k, n[k], b[k]/1048576}' |
sort -r
echo '--- totals ---'
sqlite3 "$DB" "select count(*) from video where sync_status is not null and sync_status<>'SYNCED' and file is not null;" 2>&1

echo '=== Q21: the deletion clock — units of min_free_space, from the source ==='
sqlite3 -header -column "$DB" "select * from disk_management;" 2>&1
echo '--- what actually reads min_free_space ---'
grep -rn "min_free_space\|critical_space" \
  /home/pi/.venv/lib/python3*/site-packages/orc_api/ \
  /home/pi/.local/lib/python3*/site-packages/orc_api/ 2>/dev/null | grep -v '\.pyc' | head -20
echo '--- free space ---'
df -h / /home 2>&1 | head -5
du -sh /home/pi/.ORC-OS 2>/dev/null

echo '=== Q22: the cost gate — data consumed to date ==='
for i in wwan0 usb0 eth1 ppp0; do
  [ -d "/sys/class/net/$i" ] && echo "$i rx=$(cat /sys/class/net/$i/statistics/rx_bytes) tx=$(cat /sys/class/net/$i/statistics/tx_bytes)"
done
vnstat --oneline 2>/dev/null | head -3
mmcli -L 2>/dev/null | head -3
echo '=== END ==='
"""


def log(m):
    print(f"[{datetime.now(timezone.utc).strftime('%H:%M:%SZ')}] {m}", flush=True)


def main():
    log("waiting for tcp/22 on the next wake (TODO-119 Track 2 sizing)")
    deadline = time.time() + 3300
    while time.time() < deadline:
        if sw.port_open(HOST, 22, timeout_s=2):
            log("tcp/22 OPEN — sizing the newest-first re-drive")
            pw = sw.load_password()
            env = sw.askpass_env(pw) if pw else None
            argv = ["ssh", "-o", f"BatchMode={'no' if pw else 'yes'}",
                    "-o", "StrictHostKeyChecking=accept-new",
                    "-o", "ConnectTimeout=5", "-o", "NumberOfPasswordPrompts=1",
                    f"{USER}@{HOST}", CMD]
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            dest = OUT / f"{HOST}-redriveplan119f-{stamp}.txt"
            with open(dest, "wb") as fh:
                try:
                    subprocess.run(argv, stdout=fh, stderr=subprocess.STDOUT,
                                   timeout=220, env=env)
                except subprocess.TimeoutExpired:
                    log("ssh timed out — keeping whatever streamed")
            size = dest.stat().st_size if dest.exists() else 0
            log(f"*** GRABBED redriveplan119f: {size} bytes -> {dest.name} ***")
            return 0 if size > 200 else 1
        time.sleep(1.0)
    log("no wake seen within the window")
    return 1


sys.exit(main())
