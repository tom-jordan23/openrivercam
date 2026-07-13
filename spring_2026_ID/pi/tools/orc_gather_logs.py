#!/usr/bin/env python3
"""Gather errored-video logs + the config that produced them from an ORC-OS station.

READ-ONLY. Uploads nothing, runs nothing, deletes nothing — safe to run against a
live station. Built for a short duty-cycle window: it filters server-side for the
videos you want, fetches fast with short timeouts, and writes each file to disk the
moment it arrives, so a mid-run shutdown still leaves you with a partial bundle.

For each matching video it saves:
  video_<id>.json      the video record (status, timestamp, time_series, ...)
  video_<id>.log       the pyorc log (the line that explains the failure)
And, once, the config those videos referenced (so a repro has everything):
  video_config_<id>.json  recipe_<id>.json  camera_config_<id>.json
  cross_section_<id>.json  cross_section_wl_<id>.json
  settings.json           (the station's default video_config_id lives here)

Everything lands in --out and is tarred to <out>.tgz at the end.

AUTH: on a real station DEV_MODE is off, so a login is required. Give the back-end
password via --password or the ORC_PASSWORD env var (you'll be prompted if neither
is set and a password is configured). Login is POST /auth/login/?password=... which
returns a token; we send it back as the `orc_token` cookie the API checks. If the
instance is in DEV_MODE (e.g. a local dev stack) no password is needed.

BASE: on the native Pi install the API uvicorn serves at http://localhost:5000
with routes at root (nginx only adds the /api prefix for the browser). So:
  BASE=http://localhost:5000 ./orc_gather_logs.py --password '...'
A dockerised dev stack may publish it elsewhere (e.g. http://localhost:3001).

Usage:
  BASE=http://localhost:5000 ORC_PASSWORD='...' ./orc_gather_logs.py            # errored videos
  BASE=http://localhost:5000 ./orc_gather_logs.py --password '...' --start 2026-07-10
  BASE=http://localhost:5000 ./orc_gather_logs.py --status all --count 20
  BASE=http://localhost:5000 ./orc_gather_logs.py --ids 41 42 43

ORC-OS VideoStatus: NEW=1 QUEUE=2 TASK=3 DONE=4 ERROR=5
"""
import argparse
import getpass
import json
import os
import sys
import tarfile
import urllib.parse
import urllib.request
import urllib.error

STATUS = {1: "NEW", 2: "QUEUE", 3: "TASK", 4: "DONE", 5: "ERROR"}
NAME2CODE = {v.lower(): k for k, v in STATUS.items()}
TIMEOUT = 15  # short: fail fast if the station drops mid-window
AUTH_HEADERS = {}  # populated by login(); the orc_token cookie the API checks


def req(base, path, method="GET", body=None, extra_headers=None):
    url = base.rstrip("/") + path
    headers = dict(AUTH_HEADERS)
    if extra_headers:
        headers.update(extra_headers)
    r = urllib.request.Request(url, data=body, method=method, headers=headers)
    try:
        resp = urllib.request.urlopen(r, timeout=TIMEOUT)
        return resp.status, resp.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()
    except Exception as e:
        return None, str(e).encode()


def get(base, path):
    return req(base, path)


def login(base, password):
    """POST /auth/login/?password=... -> {access_token,...}; stash as orc_token cookie.
    Returns True if auth is in place (logged in, or DEV_MODE / no password set)."""
    # Is a password even configured / is auth enforced?
    st, b = get(base, "/auth/password_available/")
    if st is None:
        sys.exit(f"cannot reach API at {base}: {b.decode(errors='replace')}\n"
                 f"On the native Pi install try BASE=http://localhost:5000")
    if b.strip() in (b"false", b'"false"'):
        # no password configured — either DEV_MODE or a fresh box; nothing to do
        return True
    if not password:
        password = os.environ.get("ORC_PASSWORD") or getpass.getpass("ORC-OS back-end password: ")
    q = urllib.parse.urlencode({"password": password})
    st, b = req(base, f"/auth/login/?{q}", method="POST")
    if st != 200:
        sys.exit(f"login failed: HTTP {st}: {b.decode(errors='replace')[:200]}")
    try:
        token = json.loads(b).get("access_token")
    except Exception:
        token = None
    if not token:
        sys.exit(f"login returned no access_token: {b[:200]!r}")
    AUTH_HEADERS["Cookie"] = f"orc_token={token}"
    return True


def save(out, name, data, decode_json_str=False):
    """Write bytes/str to out/name. If decode_json_str, the body is a JSON-encoded
    string (like /log/ returns) — unwrap it to raw text first."""
    txt = data.decode(errors="replace") if isinstance(data, bytes) else data
    if decode_json_str:
        try:
            txt = json.loads(txt)
        except Exception:
            pass
    with open(os.path.join(out, name), "w") as fh:
        fh.write(txt if isinstance(txt, str) else json.dumps(txt, indent=1))


def main():
    ap = argparse.ArgumentParser(description="Read-only: gather errored-video logs+config from ORC-OS.")
    ap.add_argument("--base", default=os.environ.get("BASE", "http://localhost:5000"),
                    help="ORC-OS API base URL (or set BASE env). Native Pi: http://localhost:5000")
    ap.add_argument("--password", default=None,
                    help="back-end password (or ORC_PASSWORD env; prompted if needed)")
    ap.add_argument("--status", default="error",
                    help="error|done|task|queue|new|all  (default: error)")
    ap.add_argument("--count", type=int, default=100, help="max videos to pull")
    ap.add_argument("--start", default=None, help="only videos on/after this date (YYYY-MM-DD)")
    ap.add_argument("--stop", default=None, help="only videos on/before this date (YYYY-MM-DD)")
    ap.add_argument("--ids", type=int, nargs="*", help="explicit video ids (overrides status filter)")
    ap.add_argument("--out", default=None, help="output dir (default: ./orc_logs_<host>)")
    args = ap.parse_args()

    host = urllib.parse.urlparse(args.base).hostname or "orc"
    out = args.out or f"./orc_logs_{host}"
    os.makedirs(out, exist_ok=True)
    print(f"target {args.base}  ->  {out}")

    login(args.base, args.password)

    # --- pick the video list ---
    if args.ids:
        videos = []
        for vid in args.ids:
            st, b = get(args.base, f"/video/{vid}/")
            if st == 200:
                videos.append(json.loads(b))
            else:
                print(f"  video {vid}: HTTP {st}")
    else:
        q = {"count": args.count}
        if args.status.lower() != "all":
            code = NAME2CODE.get(args.status.lower())
            if code is None:
                sys.exit(f"bad --status {args.status!r}; use one of {list(NAME2CODE)+['all']}")
            q["status"] = code
        if args.start:
            q["start"] = args.start
        if args.stop:
            q["stop"] = args.stop
        st, b = get(args.base, "/video/?" + urllib.parse.urlencode(q))
        if st == 401:
            sys.exit("401 Unauthorized — wrong/absent password (set --password or ORC_PASSWORD).")
        if st != 200:
            sys.exit(f"video list failed: HTTP {st}: {b[:200]!r}")
        videos = json.loads(b)

    print(f"videos matched: {len(videos)}")

    # --- per-video record + log (save as we go) ---
    config_ids = set()
    for v in videos:
        vid = v.get("id")
        label = STATUS.get(v.get("status"), v.get("status"))
        save(out, f"video_{vid}.json", json.dumps(v, indent=1))
        st, b = get(args.base, f"/video/{vid}/log/")
        save(out, f"video_{vid}.log", b if st == 200 else f"<no log: HTTP {st}>",
             decode_json_str=(st == 200))
        cfg = v.get("video_config_id") or (v.get("video_config") or {}).get("id")
        if cfg:
            config_ids.add(cfg)
        print(f"  video {vid}: {label}  ({v.get('timestamp','')})  cfg={cfg}")

    # --- the config those videos used (video_config carries the nested ids) ---
    save(out, "settings.json", get(args.base, "/settings/")[1])
    seen = {"recipe": set(), "camera_config": set(), "cross_section": set()}
    for cfg in sorted(config_ids):
        st, b = get(args.base, f"/video_config/{cfg}/")
        if st != 200:
            print(f"  video_config {cfg}: HTTP {st}"); continue
        vc = json.loads(b)
        save(out, f"video_config_{cfg}.json", json.dumps(vc, indent=1))
        rid = vc.get("recipe_id") or (vc.get("recipe") or {}).get("id")
        cid = vc.get("camera_config_id") or (vc.get("camera_config") or {}).get("id")
        xs = vc.get("cross_section_id") or (vc.get("cross_section") or {}).get("id")
        xswl = vc.get("cross_section_wl_id") or (vc.get("cross_section_wl") or {}).get("id")
        if rid and rid not in seen["recipe"]:
            seen["recipe"].add(rid)
            save(out, f"recipe_{rid}.json", get(args.base, f"/recipe/{rid}/download/")[1])
        if cid and cid not in seen["camera_config"]:
            seen["camera_config"].add(cid)
            save(out, f"camera_config_{cid}.json", get(args.base, f"/camera_config/{cid}")[1])
        for x in (xs, xswl):
            if x and x not in seen["cross_section"]:
                seen["cross_section"].add(x)
                save(out, f"cross_section_{x}.json", get(args.base, f"/cross_section/{x}/download/")[1])

    # --- tar it up for handoff ---
    tgz = out.rstrip("/") + ".tgz"
    with tarfile.open(tgz, "w:gz") as tf:
        tf.add(out, arcname=os.path.basename(out))
    n_err = sum(1 for v in videos if v.get("status") == 5)
    print(f"\nsaved {len(videos)} videos ({n_err} ERROR) + config to {out}")
    print(f"bundle: {tgz}")


if __name__ == "__main__":
    main()
