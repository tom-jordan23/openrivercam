#!/usr/bin/env python3
"""TODO-119: join the station's un-synced rows against the server, per timestamp.

WHY
    The 09-03 per-day join (joins/station_vs_server_by_day_2026-09-03.txt) was
    0.4% coarse: close enough to say the backlog is absent from the server, not
    close enough to scope an upload. Station FAILED does not mean server-absent -
    LiveORC 500s after committing the row and the file, 62 times on site 4 by
    09-03 - and nothing constrains `timestamp` on the server, so re-sending those
    clips creates duplicate rows. This decides, clip by clip, what an upload
    should and should not carry.

    A server row is a claim about a file, not a file (MEDIA_VOLUME_RUNBOOK). So a
    timestamp match is only called ON-SERVER when the playback route's
    Content-Length equals the station's local byte size.

INPUTS
    station  newest data/station-forensics/orc-sukabumi-tsjoin119ab-*.txt
    server   GET /api/site/4/video/ with the read-only API account (credentials
             as in mirror/orc_inventory.py), or --server-json from an earlier run.
             HEAD on /playback/ only for rows that match a station clip.

OUTPUTS
    findings/sukabumi_backlog_tsjoin_<date>.csv   one row per un-synced station row
    joins/station_vs_server_by_timestamp_<date>.txt  the summary
    data/liveorc-mirror/4/video-list-<date>.json  raw server list (gitignored)

READ-ONLY. GET and HEAD, plus the token POST.
"""
import argparse, bisect, collections, csv, json, sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(HERE.parent / "mirror"))

SITE = 4
NEAR_S = 60     # a server row within this many seconds, but not the same second


def parse_ts(s):
    """Both sides to naive UTC, truncated to the second. The station clock is UTC."""
    s = s.strip().replace("T", " ").rstrip("Z")
    s = s.split("+")[0].split(".")[0]
    return datetime.strptime(s, "%Y-%m-%d %H:%M:%S")


def load_station():
    art = sorted((REPO / "data/station-forensics").glob("orc-sukabumi-tsjoin119ab-*.txt"))[-1]
    lines = art.read_text().splitlines()
    i0 = next(i for i, l in enumerate(lines) if l.startswith("=== ROWS"))
    i1 = next(i for i, l in enumerate(lines) if l.startswith("=== END ROWS"))
    rows, bad = [], []
    for l in lines[i0 + 1:i1]:
        p = l.split("|")
        if len(p) != 7 or not p[0].isdigit():
            bad.append(l); continue
        rows.append({"id": int(p[0]), "ts": parse_ts(p[1]), "sync": p[2], "remote_id": p[3],
                     "status": p[4], "file": p[5], "bytes": int(p[6]) if p[6].isdigit() else None})
    return art, rows, bad


def api_client():
    import orc_inventory as inv
    import os
    email, pw = os.environ.get("LIVEORC_EMAIL"), os.environ.get("LIVEORC_PASSWORD")
    if not (email and pw) and inv.SECRETS_FILE.is_file():
        for line in inv.SECRETS_FILE.read_text().splitlines():
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.split("=", 1)
                v = v.strip().strip("'\"")
                if k.strip() == "LIVEORC_EMAIL": email = email or v
                if k.strip() == "LIVEORC_PASSWORD": pw = pw or v
    if not (email and pw):
        sys.exit(f"ERROR: no credentials; set LIVEORC_EMAIL/LIVEORC_PASSWORD or write {inv.SECRETS_FILE}")
    return inv.Api(inv.DEFAULT_BASE, email, pw)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--server-json", help="reuse a saved server video list instead of fetching")
    ap.add_argument("--no-head", action="store_true", help="skip byte-size checks (not evidence)")
    a = ap.parse_args()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    art, st_rows, bad = load_station()
    api = None
    if a.server_json:
        server = json.loads(Path(a.server_json).read_text())
    else:
        api = api_client()
        status, server = api.get_json(f"/api/site/{SITE}/video/")
        if status != 200 or not isinstance(server, list):
            sys.exit(f"ERROR: video list returned HTTP {status}")
        dest = REPO / f"data/liveorc-mirror/{SITE}/video-list-{today}.json"
        dest.write_text(json.dumps(server))
        print(f"server list: {len(server)} rows, {dest.stat().st_size} bytes -> {dest}")

    srv = sorted(({"id": v["id"], "ts": parse_ts(v["timestamp"]), "status": v.get("status"),
                   "file": v.get("file")} for v in server), key=lambda r: r["ts"])
    keys = [r["ts"] for r in srv]
    by_ts = collections.defaultdict(list)
    for r in srv:
        by_ts[r["ts"]].append(r)
    dup_server = {t: rs for t, rs in by_ts.items() if len(rs) > 1}

    if api is None and not a.no_head:
        api = api_client()

    out_rows, verdicts, gb = [], collections.Counter(), collections.Counter()
    for r in st_rows:
        exact = by_ts.get(r["ts"], [])
        near = None
        if not exact:
            i = bisect.bisect_left(keys, r["ts"])
            cands = [srv[j] for j in (i - 1, i) if 0 <= j < len(srv)]
            cands = [c for c in cands if abs((c["ts"] - r["ts"]).total_seconds()) <= NEAR_S]
            near = min(cands, key=lambda c: abs((c["ts"] - r["ts"]).total_seconds())) if cands else None
        s = exact[0] if exact else None
        srv_bytes = None
        if s and s["file"] and api and not a.no_head:
            srv_bytes = api.head_size(f"{api.base}/api/site/{SITE}/video/{s['id']}/playback/")
        extant = r["bytes"] is not None

        if len(exact) > 1:
            v = "REVIEW-server-duplicate"
        elif s and not s["file"]:
            v = "REVIEW-server-row-no-file"
        elif s and extant and srv_bytes == r["bytes"]:
            v = "ON-SERVER"
        elif s and extant and srv_bytes is None:
            v = "REVIEW-server-size-unknown"
        elif s and extant:
            v = "REVIEW-size-mismatch"
        elif s:
            v = "ON-SERVER-local-gone"
        elif near:
            v = "REVIEW-near-match"
        elif extant:
            v = "UPLOAD"
        else:
            v = "LOST"
        verdicts[v] += 1
        gb[v] += r["bytes"] or 0
        out_rows.append([r["ts"].isoformat(sep=" "), r["id"], r["sync"], r["remote_id"], r["status"],
                         Path(r["file"]).name if r["file"] else "", r["bytes"] if extant else "",
                         s["id"] if s else "", s["status"] if s else "", srv_bytes if srv_bytes is not None else "",
                         near["id"] if near else "",
                         int((near["ts"] - r["ts"]).total_seconds()) if near else "", v])

    csv_out = REPO / f"spring_2026_ID/findings/sukabumi_backlog_tsjoin_{today}.csv"
    with csv_out.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["station_ts_utc", "station_id", "sync_status", "remote_id", "proc_status", "name",
                    "station_bytes", "server_id", "server_status", "server_bytes",
                    "near_server_id", "near_dt_s", "verdict"])
        w.writerows(sorted(out_rows, key=lambda x: x[0], reverse=True))

    sync_c = collections.Counter(r["sync"] for r in st_rows)
    lines = [
        f"# TODO-119 timestamp-level join, station vs LiveORC site {SITE} — {today}",
        f"# station: {art.name}   server: {len(srv)} video rows"
        + (f" (from {Path(a.server_json).name})" if a.server_json else " (API, fetched now)"),
        f"# station un-synced rows: {len(st_rows)}  by sync_status: {dict(sync_c)}"
        + (f"   unparsed lines: {len(bad)}" if bad else ""),
        f"# station files extant: {sum(r['bytes'] is not None for r in st_rows)}"
        f"   server timestamps held by >1 row: {len(dup_server)}",
        "#",
        "# verdict|rows|GB (station bytes)",
    ]
    for v, n in sorted(verdicts.items(), key=lambda kv: -kv[1]):
        lines.append(f"{v}|{n}|{gb[v]/1e9:.2f}")
    if dup_server:
        lines.append("#\n# server timestamps with more than one row (ts|ids)")
        for t, rs in sorted(dup_server.items()):
            lines.append(f"{t.isoformat(sep=' ')}|{','.join(str(x['id']) for x in rs)}")
    summary = "\n".join(lines) + "\n"
    (HERE / f"joins/station_vs_server_by_timestamp_{today}.txt").write_text(summary)
    print(summary)
    print(f"csv -> {csv_out}")


if __name__ == "__main__":
    main()
