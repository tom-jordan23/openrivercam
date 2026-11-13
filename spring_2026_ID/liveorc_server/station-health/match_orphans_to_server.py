#!/usr/bin/env python3
"""Match the station's orphaned quiver plots against the LiveORC video listing (TODO-119). Workstation only; touches nothing.

    python3 -I match_orphans_to_server.py GRAB_OUTPUT.txt MANIFEST.json [--allowlist OUT.txt]

GRAB_OUTPUT   the capture from todo119_swap_orphan_verify_grab.sh (lines `ORPHAN|id|date|plot_bytes|sync_status|db_timestamp`)
MANIFEST      a LiveORC API listing, e.g. data/liveorc-mirror/4/video-list-2026-09-16.json (records with `timestamp` and `image`)

A plot is SAFE to remove from the station only if ALL hold: the station DB says SYNCED; the server has a record with the same
timestamp (to the second); and that record's `image` field is set. The allow-list holds exactly those orphans (`id|date|bytes`).
What this does NOT prove: that the image file on the server is readable (the listing only says the field is populated), or
anything about records newer than the listing. Orphans newer than the listing are reported separately, never allow-listed.
"""
import argparse
import collections
import json
import re
import sys
from datetime import datetime, timedelta, timezone


def parse_orphans(path):
    out = []
    for line in open(path, errors="replace"):
        if line.startswith("ORPHAN|"):
            _, i, date, nbytes, status, ts = (line.rstrip("\n").split("|") + [""] * 6)[:6]
            if i.isdigit() and nbytes.isdigit():
                out.append({"id": int(i), "date": date, "bytes": int(nbytes), "status": status, "ts": ts})
    return out


def station_ts(s):
    m = re.match(r"(\d{4}-\d{2}-\d{2})[ T](\d{2}:\d{2}:\d{2})", s or "")
    return datetime.strptime(m.group(1) + " " + m.group(2), "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc) if m else None


def load_manifest(path):
    d = json.load(open(path))
    items = d if isinstance(d, list) else next(v for v in d.values() if isinstance(v, list))
    idx = collections.defaultdict(list)
    newest = None
    for r in items:
        m = re.match(r"(\d{4}-\d{2}-\d{2})[T ](\d{2}:\d{2}:\d{2})", r.get("timestamp") or "")
        if not m:
            continue
        t = datetime.strptime(m.group(1) + " " + m.group(2), "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
        idx[t].append(r)
        newest = t if newest is None or t > newest else newest
    return idx, newest, len(items)


def classify(orphans, idx, newest, shift):
    res = []
    for o in orphans:
        t = station_ts(o["ts"])
        rec = idx.get(t + shift) if t else None
        if o["status"] != "SYNCED":
            cls = "NOT_SYNCED"
        elif t is None:
            cls = "NO_TIMESTAMP"
        elif rec:
            cls = "SAFE" if any(r.get("image") for r in rec) else "SERVER_NO_IMAGE"
        else:
            cls = "NEWER_THAN_LISTING" if newest and t + shift > newest else "NO_SERVER_RECORD"
        res.append((o, cls))
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("grab"); ap.add_argument("manifest"); ap.add_argument("--allowlist")
    a = ap.parse_args()
    orphans = parse_orphans(a.grab)
    if not orphans:
        sys.exit("no ORPHAN lines found in " + a.grab)
    idx, newest, n = load_manifest(a.manifest)
    print(f"orphans in the grab: {len(orphans)}   server records in the listing: {n}   listing newest: {newest}")

    best = None
    for h in (0, 7, -7):                                    # the station clock is UTC; try Jakarta offsets in case a zone differs
        shift = timedelta(hours=h)
        res = classify(orphans, idx, newest, shift)
        matched = sum(1 for _, c in res if c in ("SAFE", "SERVER_NO_IMAGE"))
        print(f"  timestamp offset {h:+d} h: {matched} of {sum(1 for _, c in res if c != 'NOT_SYNCED')} synced orphans match a server record")
        if best is None or matched > best[0]:
            best = (matched, h, res)
    matched, h, res = best
    if h != 0:
        print(f"WARNING: the best match needs a {h:+d} h offset; station and server timestamps may not share a zone. NOT writing an allow-list.")
    cnt = collections.Counter(c for _, c in res); sz = collections.Counter()
    for o, c in res: sz[c] += o["bytes"]
    print("\nclass                        plots      GiB")
    for c in ("SAFE", "SERVER_NO_IMAGE", "NO_SERVER_RECORD", "NEWER_THAN_LISTING", "NOT_SYNCED", "NO_TIMESTAMP"):
        if cnt[c]: print(f"  {c:24s} {cnt[c]:6d} {sz[c] / 2**30:8.3f}")
    for c in ("SERVER_NO_IMAGE", "NO_SERVER_RECORD", "NEWER_THAN_LISTING", "NOT_SYNCED"):
        ex = [o for o, k in res if k == c][:5]
        if ex: print(f"  e.g. {c}: " + ", ".join(f"{o['id']}({o['date']})" for o in ex))
    safe = [o for o, c in res if c == "SAFE"]
    if a.allowlist and h == 0:
        with open(a.allowlist, "w") as f:
            for o in sorted(safe, key=lambda o: o["id"]): f.write(f"{o['id']}|{o['date']}|{o['bytes']}\n")
        print(f"\nallow-list written: {a.allowlist}  ({len(safe)} plots, {sum(o['bytes'] for o in safe) / 2**30:.3f} GiB)")
    print("\nNOT proven: that the server's image file is readable (the listing only shows the field is set).")


if __name__ == "__main__":
    main()
