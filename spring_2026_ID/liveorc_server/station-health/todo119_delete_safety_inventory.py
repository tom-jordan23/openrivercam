#!/usr/bin/env python3
"""TODO-119: prove which station-local clips are safely redundant, before deleting any.

THE DECISION THIS SERVES
    Tom, 2026-09-02: verify first, before deleting anything. min_free_space is
    staying where it is, so the only way to buy time against the purge is to
    reclaim the ~13-18 GB of already-SYNCED video the station is still holding.
    That is only safe for clips provably present elsewhere, at the right size.

THE TRAP THIS IS BUILT TO AVOID
    Checking the server's DATABASE is not evidence the bytes exist. That is
    precisely the check that would have passed on 2026-08-09, the day before
    26 GB of media was destroyed while every row survived (MEDIA_VOLUME_RUNBOOK).
    This system also holds live proof of the same gap: site 2 has 546 video rows
    whose `file` is null for every one. A row is a claim about a file, not a file.

    So the comparison is against BYTES ON DISK, from the verified TODO-114
    mirror at data/liveorc-mirror/4/media - 2630 mp4s, 30 GB, pulled over two
    independent transports that agreed. The mirror is also itself a second
    copy, so a clip present there survives in two places even if the station's
    copy goes.

    Sizes matter, not just presence. The link tears connections down
    mid-transfer, so a truncated server-side copy marked SYNCED is a real
    possibility. A size mismatch is the only thing that would catch it, and it
    would be a finding about the link as much as about the file.

WHAT IT COLLECTS
    One row per EXTANT local mp4 the database knows about: sync_status,
    remote_id, basename, local byte size. Everything else - which are
    redundant, which are truncated, which are the backlog - is joined offline
    against the mirror, needing no further station trips.

    ~2,600 lines, sent over `ssh -C`. The station's whole video tree, described
    once, to authorise a 13-18 GB reclaim.

READ-ONLY. sqlite selects and stat(1). It deletes nothing, and it is not the
thing that would do the deleting.
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
echo '=== date (station is UTC) ==='; date -u
echo '=== df ==='; df -h / | tail -1

# 119f returned an EMPTY inventory because the file column is relative to the
# uploads dir (videos/YYYYMMDD/N/*.mp4) and the candidate prefixes omitted
# uploads/. Derive the base from the tree itself rather than guessing again.
VTREE=$(find /home/pi -maxdepth 5 -type d -name videos 2>/dev/null | head -1)
BASE=$(dirname "$VTREE")
echo "=== resolved base: $BASE (tree $VTREE) ==="

echo '=== INVENTORY: status|remote_id|basename|bytes  (extant local mp4s only) ==='
sqlite3 "$DB" "select ifnull(sync_status,'NULL')||'|'||ifnull(remote_id,'')||'|'||file
                 from video where file is not null order by timestamp desc;" 2>/dev/null |
while IFS='|' read -r st rid f; do
  p=""
  for cand in "$BASE/$f" "$f" "/home/pi/$f" "/home/pi/.ORC-OS/$f"; do
    [ -f "$cand" ] && { p="$cand"; break; }
  done
  [ -n "$p" ] && echo "$st|$rid|$(basename "$p")|$(stat -c%s "$p" 2>/dev/null || echo 0)"
done
echo '=== END INVENTORY ==='

echo '=== rows whose file is GONE, by status (context, counts only) ==='
sqlite3 -column "$DB" "select ifnull(sync_status,'NULL'), count(*) from video where file is null group by 1;" 2>&1

echo '=== min_free_space units: locate orc_api first, THEN grep it ==='
# 119f grepped two guessed site-packages paths and matched nothing, leaving the
# GB-vs-percent question open. Ask the interpreter where the package actually is.
for PY in /home/pi/.venv/bin/python /home/pi/.venv/bin/python3 python3; do
  D=$("$PY" -c "import orc_api,os;print(os.path.dirname(orc_api.__file__))" 2>/dev/null) && [ -n "$D" ] && break
done
echo "orc_api at: ${D:-NOT FOUND}"
[ -n "$D" ] && grep -rn "min_free_space\|critical_space" "$D" --include=*.py 2>/dev/null | head -20
echo '--- and the disk-manager service that consumes it ---'
[ -n "$D" ] && grep -rln "free_space" "$D" --include=*.py 2>/dev/null | head
echo '=== END ==='
"""


def log(m):
    print(f"[{datetime.now(timezone.utc).strftime('%H:%M:%SZ')}] {m}", flush=True)


def main():
    log("waiting for tcp/22 (TODO-119 delete-safety inventory)")
    deadline = time.time() + 3300
    while time.time() < deadline:
        if sw.port_open(HOST, 22, timeout_s=2):
            log("tcp/22 OPEN — taking the full extant-file inventory")
            pw = sw.load_password()
            env = sw.askpass_env(pw) if pw else None
            argv = ["ssh", "-C", "-o", f"BatchMode={'no' if pw else 'yes'}",
                    "-o", "StrictHostKeyChecking=accept-new",
                    "-o", "ConnectTimeout=5", "-o", "NumberOfPasswordPrompts=1",
                    f"{USER}@{HOST}", CMD]
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            dest = OUT / f"{HOST}-deletesafety119g-{stamp}.txt"
            with open(dest, "wb") as fh:
                try:
                    subprocess.run(argv, stdout=fh, stderr=subprocess.STDOUT,
                                   timeout=220, env=env)
                except subprocess.TimeoutExpired:
                    log("ssh timed out — keeping whatever streamed")
            n = sum(1 for _ in dest.open('rb')) if dest.exists() else 0
            log(f"*** GRABBED deletesafety119g: {dest.stat().st_size} bytes, {n} lines -> {dest.name} ***")
            return 0 if n > 50 else 1
        time.sleep(1.0)
    log("no wake seen within the window")
    return 1


sys.exit(main())
