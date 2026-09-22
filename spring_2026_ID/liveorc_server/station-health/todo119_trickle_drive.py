#!/usr/bin/env python3
"""TODO-119 trickle: pick the next safe window, arm it, and catch a wake.

WHAT THIS IS FOR
    The backlog does not drain on its own because the boot scheduler asks only
    for SyncStatus.QUEUE, and the backlog is FAILED. POST /api/video/sync/ moves
    a window of rows into QUEUE through the app's own code path, and from then
    on ORC-OS's own startup check re-submits every QUEUE row on every boot. So
    the station does the uploading, on its own duty cycle, and nothing of ours
    runs between sessions.

    This script chooses the window, injects the credential, and hands the
    station-side script to todo119_wake_runner.py. It never talks to the station
    itself.

WHY THE WINDOW HAS TO BE CHOSEN CAREFULLY
    sync_videos_start_stop selects by TIME, so a window re-sends anything FAILED
    in range — including the 92 clips the server already holds but that are
    FAILED locally (the LiveORC 500). Re-sending those creates duplicate server
    rows, since nothing upstream constrains `timestamp`.

    The 2026-09-16 timestamp join gives a per-clip verdict, and the useful shape
    in it is that 968 of the 1,171 UPLOAD clips (9.33 GB) fall on 21 whole UTC
    days that contain NO ON-SERVER clips at all. A window covering one of those
    days is clean by construction and needs no per-clip filtering. This script
    will only emit those days unless --allow-mixed is given, which it warns about
    and which still needs a human to decide.

    The remaining 203 clips sit 1-3 at a time on 31 mixed days and are not worth
    the duplicate risk until the clean days are done.

ORDER
    Oldest-first by default. The disk manager purges oldest-first from
    2026-07-03, so the oldest clean day is the one closest to being destroyed.
    TODO-119's "measure before committing" gate asks for a newest-first probe
    day instead, which is --newest-first, and should be one day only.

SAFETY
    --dry-run is the default and is what this should normally be run as. It
    arms the station script with ORC_COMMIT unset, which makes the station side
    report what it would touch and stop. --commit requires both the flag and
    --i-have-approval-for, naming the exact window, so that firing is never a
    default and never a flag away from a dry run.

    READ-ONLY in dry-run mode: the station script logs in to nothing and POSTs
    nothing. A green dry run is not approval for a commit.
"""

import argparse
import collections
import csv
import os
import shlex
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
JOIN_CSV = REPO / "spring_2026_ID/findings/sukabumi_backlog_tsjoin_2026-09-16.csv"
PW_FILE = REPO / "spring_2026_ID/sukabumi_bringup/.env"
STATION_SCRIPT = HERE / "todo119_trickle_arm.sh"
RUNNER = HERE / "todo119_wake_runner.py"


def load_days():
    """Per-UTC-day verdict counts from the timestamp join."""
    if not JOIN_CSV.is_file():
        sys.exit(f"ERROR: join CSV not found: {JOIN_CSV}")
    days = collections.defaultdict(collections.Counter)
    nbytes = collections.Counter()
    with open(JOIN_CSV) as fh:
        for r in csv.DictReader(fh):
            d = r["station_ts_utc"][:10]
            days[d][r["verdict"]] += 1
            if r["verdict"] == "UPLOAD":
                nbytes[d] += int(r["station_bytes"] or 0)
    return days, nbytes


def clean_days(days):
    """Days holding UPLOAD clips and no ON-SERVER clip of any kind."""
    out = []
    for d, c in days.items():
        if c["UPLOAD"] and not c["ON-SERVER"] and not c["ON-SERVER-local-gone"]:
            out.append(d)
    return sorted(out)


def load_password():
    if not PW_FILE.is_file():
        sys.exit(f"ERROR: no password file at {PW_FILE}")
    if PW_FILE.stat().st_mode & 0o077:
        sys.exit(f"ERROR: {PW_FILE} is group/world readable. Fix to 0600 first.")
    pw = PW_FILE.read_text().strip()
    if not pw:
        sys.exit(f"ERROR: {PW_FILE} is empty")
    return pw


def main():
    ap = argparse.ArgumentParser(description="TODO-119 trickle driver")
    ap.add_argument("--day", help="drive this UTC day (YYYY-MM-DD) instead of picking one")
    ap.add_argument("--newest-first", action="store_true",
                    help="pick the newest clean day (the measurement probe) rather than the oldest")
    ap.add_argument("--allow-mixed", action="store_true",
                    help="permit a day that also holds ON-SERVER clips. Creates duplicates. Think first.")
    ap.add_argument("--max-clips", type=int, default=60, help="station-side ceiling (default 60)")
    ap.add_argument("--commit", action="store_true", help="actually POST /api/video/sync/")
    ap.add_argument("--i-have-approval-for", metavar="YYYY-MM-DD",
                    help="must equal the day being driven; required with --commit")
    ap.add_argument("--list", action="store_true", help="list the clean days and exit")
    ap.add_argument("--wait", type=int, default=1680, help="seconds to wait for a wake")
    a = ap.parse_args()

    days, nbytes = load_days()
    clean = clean_days(days)

    if a.list:
        print(f"{len(clean)} clean UTC days (UPLOAD only, no ON-SERVER):\n")
        tot = gb = 0
        for d in clean:
            n = days[d]["UPLOAD"]
            tot += n
            gb += nbytes[d]
            print(f"  {d}  {n:3d} clips  {nbytes[d]/1e6:6.1f} MB")
        print(f"\n  total {tot} clips, {gb/1e9:.2f} GB")
        mixed = sorted(d for d in days if days[d]["UPLOAD"] and d not in clean)
        mn = sum(days[d]["UPLOAD"] for d in mixed)
        print(f"  plus {mn} UPLOAD clips on {len(mixed)} mixed days, not offered here")
        return 0

    if a.day:
        day = a.day
        if day not in days:
            sys.exit(f"ERROR: {day} has no un-synced clips in the join")
        if day not in clean and not a.allow_mixed:
            c = days[day]
            sys.exit(f"ERROR: {day} holds {c['ON-SERVER'] + c['ON-SERVER-local-gone']} clip(s) the "
                     f"server already has.\n       Driving it would duplicate them. "
                     f"Re-run with --allow-mixed only if that is intended.")
    else:
        if not clean:
            sys.exit("ERROR: no clean days left in the join. Re-run the timestamp join.")
        day = clean[-1] if a.newest_first else clean[0]

    n = days[day]["UPLOAD"]
    mb = nbytes[day] / 1e6
    start = f"{day} 00:00:00"
    stop = (datetime.strptime(day, "%Y-%m-%d") + timedelta(days=1)
            - timedelta(seconds=1)).strftime("%Y-%m-%d %H:%M:%S")

    print(f"window : {start} -> {stop}  (UTC)")
    print(f"day    : {day}   {n} UPLOAD clips, {mb:.1f} MB")
    print(f"clean  : {'yes' if day in clean else 'NO — MIXED, will duplicate'}")
    print(f"mode   : {'COMMIT' if a.commit else 'dry run'}")

    if a.commit:
        if a.i_have_approval_for != day:
            sys.exit(f"\nERROR: --commit needs --i-have-approval-for {day}\n"
                     f"       (got {a.i_have_approval_for!r}). Refusing.\n"
                     f"       A dry run is not approval; the day must be named explicitly.")
        print("\n*** THIS WILL QUEUE CLIPS. The station will then upload them on its own,\n"
              f"*** on wakes nobody is watching, until the {n} clips are done (~{mb:.0f} MB metered).")

    # The parameters have to travel INSIDE the script body. The wake runner
    # pipes the script to `bash -s` over ssh, and ssh does not forward
    # environment variables to the remote without SendEnv/AcceptEnv, which is
    # not configured. So build prelude + script and hand the runner that.
    #
    # The combined body carries the password, so it is written to local tmpfs at
    # 0600 and removed in the finally below. It never touches a real disk here,
    # and on the station it exists only as bash's stdin.
    prelude = "\n".join([
        "# --- injected at arming time by todo119_trickle_drive.py ---",
        f"ORC_PW={shlex.quote(load_password())}",
        f"ORC_START={shlex.quote(start)}",
        f"ORC_STOP={shlex.quote(stop)}",
        f"ORC_MAX_CLIPS={shlex.quote(str(a.max_clips))}",
        f"ORC_COMMIT={shlex.quote('yes' if a.commit else 'no')}",
        "export ORC_PW ORC_START ORC_STOP ORC_MAX_CLIPS ORC_COMMIT",
        "# --- end injection ---",
        "",
    ])
    body = prelude + STATION_SCRIPT.read_text()

    shm = Path("/dev/shm") if Path("/dev/shm").is_dir() else Path(tempfile.gettempdir())
    fd, tmp = tempfile.mkstemp(prefix="orc_trickle_", suffix=".sh", dir=str(shm))
    tmp = Path(tmp)
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, "w") as fh:
            fh.write(body)
        label = f"trickle{day.replace('-', '')}{'c' if a.commit else 'd'}"
        argv = [sys.executable, "-u", str(RUNNER), str(tmp), label,
                "--timeout", "200", "--wait", str(a.wait)]
        print(f"\narming: {label}  (waiting up to {a.wait}s for a wake)\n")
        return subprocess.run(argv).returncode
    finally:
        try:
            tmp.unlink()
        except FileNotFoundError:
            pass


if __name__ == "__main__":
    sys.exit(main())
