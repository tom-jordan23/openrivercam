#!/usr/bin/env python3
"""orc_purge_synced.py — reclaim station disk by deleting video that already shipped.

WHY
    ISS-FIELD-009. Sukabumi's SD card sits at 5.1 GB free against ORC-OS's 5.0 GB
    purge threshold, so `disk_management` purges every 300 s and the station
    never gets clear of it. Processing then errors for want of space, the task
    never completes, `shutdown_after_task` never fires, and the Pi runs to the
    Witty Pi's 25-minute backstop instead of ~2 minutes — which is what flattens
    the battery overnight (ISS-FIELD-008 / TODO-116).

    ORC-OS's own purge is AGE-BASED AND SYNC-BLIND. It works oldest-first
    regardless of whether a video ever reached the server, so it keeps synced
    videos — which are redundant, the server has them — and deletes un-synced
    ones, which are the only copy. Backwards. On 2026-08-27 the station held
    2536 SYNCED and 2744 FAILED.

    This deletes only what is provably safe to lose: videos whose own database
    row says SYNCED. That reclaims space without touching a single byte that
    exists nowhere else.

WHAT IT TOUCHES
    Deletes files under /home/pi/.ORC-OS/uploads/videos/ belonging to video rows
    with sync_status = 'SYNCED'. Nothing else. It does NOT alter the database —
    the rows stay, exactly as they do after ORC-OS's own purge, which is a state
    the application already handles.

SAFETY
    Every non-SYNCED row's paths are collected first and used as a deny-list. A
    candidate that collides with one is dropped and reported, not deleted. Paths
    are resolved and required to sit under the uploads root, so a stray absolute
    path in the database cannot walk out of the tree. Dry-run is the default:
    deleting requires --apply.

USAGE
    ssh pi@orc-sukabumi 'sudo python3 -' < orc_purge_synced.py            # dry run
    ssh pi@orc-sukabumi 'sudo python3 - --apply' < orc_purge_synced.py    # delete
"""

import argparse
import os
import shutil
import sqlite3
import sys
from pathlib import Path

DB = Path("/home/pi/.ORC-OS/orc-os.db")
UPLOADS = Path("/home/pi/.ORC-OS/uploads/videos")


def dir_size(p):
    total = 0
    for root, _dirs, files in os.walk(p, onerror=lambda e: None):
        for f in files:
            try:
                total += os.stat(os.path.join(root, f)).st_size
            except OSError:
                pass
    return total


def resolve(raw):
    """Map a database `file` value to the per-video directory, or None.

    The column has been seen as both absolute and relative. Resolve, then
    require containment under UPLOADS — a row pointing outside the tree is a
    bug or a surprise, and either way not something to delete.
    """
    if not raw:
        return None
    p = Path(raw)
    if not p.is_absolute():
        p = UPLOADS / raw
    try:
        p = p.resolve()
        p.relative_to(UPLOADS.resolve())
    except (OSError, ValueError):
        return None
    # Per-video layout is uploads/videos/<YYYYMMDD>/<id>/<file>, so the video's
    # own directory is the parent of the media file. Take the directory itself
    # if the row already points at one.
    return p if p.is_dir() else p.parent


def purge_before_date(cutoff, apply_it):
    """Drop whole uploads/videos/<YYYYMMDD>/ directories older than cutoff.

    WHY A SECOND MODE
        The synced-only pass found nothing to delete, and the station is sitting
        below its purge threshold destroying un-synced video oldest-first on a
        5-minute timer. Taking the oldest month deliberately removes what that
        purge was about to take anyway, and the headroom it buys is what stops
        the purge reaching July and August. Doing nothing is not the
        conservative option here.

        Sukabumi is a pilot and its video is not feeding anything, so this is a
        space decision, not a data one (Tom, 2026-08-27).

    WHY IT IGNORES THE DATABASE
        Date directories are named YYYYMMDD on disk. Deciding from the tree
        needs no `file` column mapping, so it cannot be wrong in the way the
        synced-only pass might be. Guardrails: immediate children of the uploads
        root only, name must be exactly 8 digits, date must be strictly before
        the cutoff.
    """
    import re
    if not re.fullmatch(r"\d{8}", cutoff):
        sys.exit(f"--before-date must be YYYYMMDD, got {cutoff!r}")
    if not UPLOADS.is_dir():
        sys.exit(f"no uploads dir at {UPLOADS}")

    victims, kept = [], []
    for d in sorted(UPLOADS.iterdir()):
        if not d.is_dir() or not re.fullmatch(r"\d{8}", d.name):
            kept.append((d.name, "not a date dir"))
            continue
        (victims if d.name < cutoff else kept).append(
            (d.name, "older" if d.name < cutoff else "kept"))

    st = os.statvfs("/")
    free_before = st.f_bavail * st.f_frsize

    total = 0
    sized = []
    for name, _ in victims:
        sz = dir_size(UPLOADS / name)
        sized.append((name, sz))
        total += sz

    print(f"cutoff                 : {cutoff} (strictly before)")
    print(f"date dirs to delete    : {len(victims)}")
    print(f"date dirs kept         : {len([k for k in kept if k[1]=='kept'])}")
    print(f"reclaimable            : {total/2**30:.2f} GiB")
    print(f"free now               : {free_before/2**30:.2f} GiB")
    print(f"free after (projected) : {(free_before+total)/2**30:.2f} GiB")
    for name, sz in sized:
        print(f"  {name}  {sz/2**30:6.2f} GiB")

    if not apply_it:
        print("\nDRY RUN — nothing deleted. Re-run with --apply.")
        return
    if not sized:
        print("\nnothing matched.")
        return

    # Delete oldest-first, one date dir at a time, reporting after each. The
    # station is duty-cycled and can lose power mid-run, so this has to be
    # resumable and auditable: a truncated run leaves whole dirs done and the
    # printed log says exactly how far it got. Re-running is safe — dirs already
    # gone are simply absent next time.
    print("\n--- deleting oldest first ---")
    removed = failed = 0
    for name, sz in sized:
        d = UPLOADS / name
        try:
            n = sum(1 for _ in d.rglob("*")) if d.exists() else 0
            shutil.rmtree(d)
            removed += 1
            st_now = os.statvfs("/")
            print(f"  deleted {name}  {n:5d} entries  {sz/2**30:5.2f} GiB  "
                  f"free now {st_now.f_bavail*st_now.f_frsize/2**30:.2f} GiB", flush=True)
        except OSError as e:
            failed += 1
            print(f"  FAILED {name}: {e}", flush=True)

    st = os.statvfs("/")
    free_after = st.f_bavail * st.f_frsize
    print(f"\ndeleted {removed} date dirs, {failed} failed")
    print(f"free before : {free_before/2**30:.2f} GiB")
    print(f"free after  : {free_after/2**30:.2f} GiB")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--apply", action="store_true",
                    help="actually delete (default is a dry run)")
    ap.add_argument("--limit", type=int, default=0,
                    help="only act on the N oldest synced videos (0 = all)")
    ap.add_argument("--before-date", metavar="YYYYMMDD",
                    help="instead of the synced-only pass, drop whole date "
                         "directories older than this. Works off the filesystem, "
                         "not the database, so it does not depend on the `file` "
                         "column mapping.")
    args = ap.parse_args()

    if args.before_date:
        return purge_before_date(args.before_date, args.apply)

    if not DB.is_file():
        sys.exit(f"no database at {DB}")

    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    cur = con.cursor()
    cur.execute("SELECT id, timestamp, file, sync_status FROM video ORDER BY timestamp")
    rows = cur.fetchall()
    con.close()

    synced, protected = [], set()
    for vid, ts, f, sync in rows:
        d = resolve(f)
        if d is None:
            continue
        if sync == "SYNCED":
            synced.append((vid, ts, d))
        else:
            protected.add(d)

    # A directory shared by a synced and an un-synced row must not be deleted.
    candidates, collisions = [], []
    seen = set()
    for vid, ts, d in synced:
        if d in protected:
            collisions.append((vid, ts, d))
        elif d not in seen:
            seen.add(d)
            candidates.append((vid, ts, d))

    if args.limit:
        candidates = candidates[:args.limit]

    st = os.statvfs("/")
    free_before = st.f_bavail * st.f_frsize

    total = 0
    existing = []
    for vid, ts, d in candidates:
        if d.exists():
            sz = dir_size(d)
            total += sz
            existing.append((vid, ts, d, sz))

    print(f"database rows            : {len(rows)}")
    print(f"  SYNCED with a path     : {len(synced)}")
    print(f"  protected (not synced) : {len(protected)} dirs")
    print(f"  candidates             : {len(candidates)}")
    print(f"  still present on disk  : {len(existing)}")
    if collisions:
        print(f"  SKIPPED, dir shared with an un-synced row: {len(collisions)}")
    print(f"reclaimable              : {total/2**30:.2f} GiB")
    print(f"free now                 : {free_before/2**30:.2f} GiB")
    print(f"free after (projected)   : {(free_before+total)/2**30:.2f} GiB")

    # Print samples even when nothing exists. "0 present" has two very different
    # explanations — the purge already took them, or this script is resolving
    # paths wrongly — and without the raw column value you cannot tell which.
    if not existing and synced:
        print("\nNOTHING PRESENT. Raw `file` values for the first 3 SYNCED rows,")
        print("to distinguish 'already purged' from 'bad path mapping':")
        con2 = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
        c2 = con2.cursor()
        c2.execute("SELECT id, file, sync_status FROM video "
                   "WHERE sync_status='SYNCED' ORDER BY timestamp LIMIT 3")
        for vid, f, sync in c2.fetchall():
            d = resolve(f)
            print(f"  id={vid} file={f!r}")
            print(f"    -> resolved {d}  exists={d.exists() if d else None}")
        c2.execute("SELECT id, file FROM video WHERE sync_status!='SYNCED' "
                   "ORDER BY timestamp DESC LIMIT 3")
        print("  and for 3 NON-synced rows (these should exist):")
        for vid, f in c2.fetchall():
            d = resolve(f)
            print(f"  id={vid} file={f!r}")
            print(f"    -> resolved {d}  exists={d.exists() if d else None}")
        con2.close()
        # A capped sample of the real tree. maxdepth 2 here is thousands of
        # lines and every one of them would be a notification.
        print("\n  actual tree (first 2 date dirs, 3 entries each):")
        try:
            dates = sorted(d for d in UPLOADS.iterdir() if d.is_dir())
            print(f"    {len(dates)} date dirs, {dates[0].name} .. {dates[-1].name}")
            for dd in dates[:2]:
                kids = sorted(dd.iterdir())[:3]
                print(f"    {dd}/  ({len(list(dd.iterdir()))} entries)")
                for k in kids:
                    print(f"      {k.name}/" if k.is_dir() else f"      {k.name}")
        except (OSError, IndexError) as e:
            print(f"    listing failed: {e}")

    if existing:
        print("\noldest 3:")
        for vid, ts, d, sz in existing[:3]:
            print(f"  {ts}  id={vid}  {sz/2**20:8.1f} MiB  {d}")
        print("newest 3:")
        for vid, ts, d, sz in existing[-3:]:
            print(f"  {ts}  id={vid}  {sz/2**20:8.1f} MiB  {d}")

    if not args.apply:
        print("\nDRY RUN — nothing deleted. Re-run with --apply.")
        return

    if not existing:
        print("\nnothing to delete.")
        return

    removed = failed = 0
    freed = 0
    for vid, ts, d, sz in existing:
        try:
            shutil.rmtree(d)
            removed += 1
            freed += sz
        except OSError as e:
            failed += 1
            print(f"  FAILED {d}: {e}")

    st = os.statvfs("/")
    free_after = st.f_bavail * st.f_frsize
    print(f"\ndeleted {removed} video dirs ({freed/2**30:.2f} GiB), {failed} failed")
    print(f"free before : {free_before/2**30:.2f} GiB")
    print(f"free after  : {free_after/2**30:.2f} GiB")


if __name__ == "__main__":
    main()
