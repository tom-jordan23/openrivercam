#!/usr/bin/env python3
"""orc_inventory.py — TODO-114 Phase 1: inventory the LiveORC API, download nothing.

WHY
    TODO-112 moves 26 GB of media off the container writable layer, and its
    Phase 5 verification is `rsync --itemize-changes` — which only ever compares
    the host to itself. TODO-114 exists to produce something external to check
    that against. This script is the first half: it writes down what the API
    says exists, before any bytes move.

    The reconciliation is the point. The runbook says 26 GB of video / 1.3 GB of
    keyframes / 9.5 MB of thumbnails, and TODO-114 expects ~1165 video records.
    If the API sees materially less than that, the mirror is worth less than we
    think it is and we should know that BEFORE relying on it to gate TODO-112.
    A gap here is information, not an error.

WHAT IT TOUCHES
    Nothing on the server. It issues no HTTP verb but GET, plus the single POST
    to /api/token/ required to authenticate, and (with --sizes) HEAD.

    The mirror account is an institute member that created nothing, so upstream's
    IsOwnerOrReadOnlyAsInstitute makes it structurally incapable of writing.
    This script still restricts itself to GET by construction — belt and braces,
    and it keeps the script honest if the permission model ever changes upstream.

    Output goes to data/liveorc-mirror/, which is gitignored at the repo root.
    This repo is public: no manifest, token, or media file gets committed.

TOKEN REFRESH
    The access token lifetime is 360 minutes (measured 2026-08-25). Inventory
    fits comfortably inside that, but --sizes issues a HEAD per asset — four per
    video record — and a full pull in Phase 2 certainly will not fit. Refresh is
    built in here rather than bolted on after a mid-pull 401, which is TODO-114
    Phase 0's remaining requirement.

USAGE
    export LIVEORC_EMAIL='...'
    read -rs LIVEORC_PASSWORD && export LIVEORC_PASSWORD

    ./orc_inventory.py --institute 1                 # counts only, fast
    ./orc_inventory.py --institute 1 --sizes         # + HEAD every asset (slow)
    ./orc_inventory.py --institute 1 --site 4        # one site

Read-only. Safe to re-run; manifests are overwritten atomically.
"""

import argparse
import json
import os
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path

DEFAULT_BASE = os.environ.get("LIVEORC_BASE", "https://openrivercam.endlessprojects.info")

# From the OpenAPI schema's VideoStatusEnum.
STATUS_NAMES = {
    1: "new",
    2: "waiting",
    3: "processing",
    4: "finished",
    5: "error",
}

# Asset fields on the Video serializer. `file` and `image` are nullable; both
# stations run "time series + analysis images" with full-video upload disabled,
# so a null `file` is a legitimate record, not a failure. The count of nulls is
# itself a result worth reporting.
ASSET_FIELDS = ("file", "keyframe", "image", "thumbnail")

# How to actually FETCH each asset.
#
# Measured 2026-08-25 with probe_media_access.py: the URLs the serializer puts in
# `file`/`keyframe`/`image`/`thumbnail` return 404 both WITH and WITHOUT a JWT —
# byte-identical responses, so this is not an auth problem. nginx's media root
# holds admin-interface/ but not the video tree, and Django 404s the rest.
#
# The DRF actions on the video detail route DO serve real bytes (verified by
# magic number, with correct Content-Type, and HEAD returns Content-Length).
# So the serializer URLs are IDENTIFIERS; these routes are the fetch targets.
#
# `keyframe` has no action — the API exposes no /keyframe/ route, so keyframe
# bytes are simply unreachable over REST. That is a real limit on what the
# TODO-114 mirror can be, not a bug here, and it is reported rather than hidden.
ASSET_ACTIONS = {"file": "playback", "image": "image", "thumbnail": "thumbnail", "keyframe": None}


class Api:
    """Minimal LiveORC API client. GET and HEAD only, plus token endpoints."""

    def __init__(self, base, email, password, delay=0.0, verbose=False):
        self.base = base.rstrip("/")
        self.email = email
        self.password = password
        self.delay = delay
        self.verbose = verbose
        self.access = None
        self.refresh = None
        self.ctx = ssl.create_default_context()
        self._authenticate()

    # -- auth ----------------------------------------------------------------
    def _post_json(self, path, payload):
        req = urllib.request.Request(
            self.base + path,
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, context=self.ctx, timeout=60) as r:
            return json.loads(r.read().decode())

    def _authenticate(self):
        try:
            tok = self._post_json("/api/token/", {"email": self.email, "password": self.password})
        except urllib.error.HTTPError as e:
            sys.exit(f"ERROR: authentication failed ({e.code}): {e.read().decode()[:200]}")
        self.access = tok["access"]
        self.refresh = tok.get("refresh")

    def _refresh_access(self):
        """Renew the access token. Falls back to a full re-auth if refresh fails."""
        if self.refresh:
            try:
                tok = self._post_json("/api/token/refresh/", {"refresh": self.refresh})
                self.access = tok["access"]
                if "refresh" in tok:          # ROTATE_REFRESH_TOKENS may be on
                    self.refresh = tok["refresh"]
                if self.verbose:
                    print("    [token refreshed]", file=sys.stderr)
                return
            except urllib.error.HTTPError:
                pass
        self._authenticate()

    # -- requests ------------------------------------------------------------
    def _request(self, path, method="GET", _retried=False):
        if self.delay:
            time.sleep(self.delay)
        url = path if path.startswith("http") else self.base + path
        req = urllib.request.Request(
            url, headers={"Authorization": f"Bearer {self.access}"}, method=method
        )
        try:
            with urllib.request.urlopen(req, context=self.ctx, timeout=120) as r:
                return r.status, dict(r.headers), r.read() if method == "GET" else b""
        except urllib.error.HTTPError as e:
            # A 401 mid-run means the access token aged out. Refresh once and retry.
            if e.code == 401 and not _retried:
                self._refresh_access()
                return self._request(path, method, _retried=True)
            return e.code, dict(e.headers or {}), e.read()

    def get_json(self, path):
        status, _, raw = self._request(path)
        if status != 200:
            return status, None
        try:
            return status, json.loads(raw.decode())
        except json.JSONDecodeError:
            return status, None

    def head_size(self, url):
        """Content-Length for one asset, or None if unavailable."""
        status, headers, _ = self._request(url, method="HEAD")
        if status != 200:
            return None
        cl = headers.get("Content-Length") or headers.get("content-length")
        return int(cl) if cl and cl.isdigit() else None


def human(n):
    if n is None:
        return "?"
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if abs(n) < 1024 or unit == "TB":
            return f"{n:.1f} {unit}" if unit != "B" else f"{n} B"
        n /= 1024.0


def discover_sites(api, institute, only_site):
    """Every site id we can see.

    TODO-114 Phase 1 says record every site, not just 2/3/4 — so try the bare
    list first (superuser-visible) and fall back to the ?institute= form, which
    is what a non-superuser member actually needs. The bare call returning []
    is expected and is not an error.
    """
    if only_site:
        return [int(only_site)]

    seen = {}
    for path in ("/api/site/", f"/api/site/?institute={institute}"):
        status, data = api.get_json(path)
        if status == 200 and isinstance(data, list):
            for s in data:
                if isinstance(s, dict) and "id" in s:
                    seen[s["id"]] = s
    return sorted(seen)


def inventory_site(api, site):
    """Video + timeseries records for one site. No sizes, no downloads — one
    list call each. Fast enough that it is always rebuilt rather than resumed."""
    status, videos = api.get_json(f"/api/site/{site}/video/")
    if status != 200 or videos is None:
        return {"site": site, "error": f"video list returned HTTP {status}"}

    # The list route declares no page/limit parameters and returns a bare array,
    # so this is the whole set — but record what we got rather than assuming.
    ts_status, timeseries = api.get_json(f"/api/site/{site}/timeseries/")

    records, statuses, creators, null_counts = [], Counter(), Counter(), Counter()

    for v in videos:
        rec = {
            "id": v.get("id"),
            "timestamp": v.get("timestamp"),
            "created_at": v.get("created_at"),
            "status": v.get("status"),
            "status_name": STATUS_NAMES.get(v.get("status"), str(v.get("status"))),
            "creator": v.get("creator"),
            "video_config": v.get("video_config"),
            "time_series": v.get("time_series"),
            "assets": {},
        }
        statuses[rec["status_name"]] += 1
        if rec["creator"] is not None:
            creators[rec["creator"]] += 1

        for field in ASSET_FIELDS:
            url = v.get(field)
            if not url:
                null_counts[field] += 1
                rec["assets"][field] = None
            else:
                action = ASSET_ACTIONS.get(field)
                rec["assets"][field] = {
                    "url": url,                       # identifier; does NOT serve
                    "fetch": (f"{api.base}/api/site/{site}/video/{v.get('id')}/{action}/"
                              if action else None),   # None = unreachable over REST
                    "bytes": None,
                }
        records.append(rec)

    return {
        "site": site,
        "video_count": len(videos),
        "timeseries_count": len(timeseries) if isinstance(timeseries, list) else None,
        "timeseries_status": ts_status,
        "status_histogram": dict(statuses),
        "creators": dict(creators),
        "null_assets": dict(null_counts),
        "byte_totals": None,
        "videos": records,
    }


def carry_over_sizes(inv, manifest_path):
    """Reuse byte counts from a previous run.

    TODO-114's resumability rule is client-side: write the manifest first, then
    work down it, skipping what already exists. Sizing is ~10k HEAD requests, so
    an interrupted run must not start over. Keyed on (video id, asset url) — if
    the URL changed, the old size is not about the same file and is discarded.
    """
    if not manifest_path.exists():
        return 0
    try:
        old = json.loads(manifest_path.read_text())
    except (json.JSONDecodeError, OSError):
        return 0

    known = {}
    for rec in old.get("videos", []):
        for field, a in (rec.get("assets") or {}).items():
            if a and a.get("bytes") is not None:
                known[(rec.get("id"), field, a.get("url"))] = a["bytes"]

    carried = 0
    for rec in inv["videos"]:
        for field, a in rec["assets"].items():
            if a is None:
                continue
            hit = known.get((rec["id"], field, a["url"]))
            if hit is not None:
                a["bytes"] = hit
                carried += 1
    return carried


def save_manifest(inv, manifest_path):
    """Atomic write — a half-written manifest is worse than none."""
    tmp = manifest_path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(inv, indent=2))
    tmp.replace(manifest_path)


def size_pass(api, inv, manifest_path, save_every=50):
    """HEAD every non-null asset that has no size yet.

    This is the slow part — four assets per record, thousands of records. It
    reports progress and checkpoints to disk, because the first version did
    neither and an interrupted run looked indistinguishable from a hang while
    silently discarding everything it had fetched.
    """
    todo = [
        (rec, field)
        for rec in inv["videos"]
        for field, a in rec["assets"].items()
        if a is not None and a["bytes"] is None and a.get("fetch")
    ]
    if not todo:
        recompute_totals(inv)
        return 0

    total = len(todo)
    started = time.monotonic()
    done = 0
    print(f"  sizing {total} assets (Ctrl-C is safe — progress is checkpointed)")

    try:
        for rec, field in todo:
            a = rec["assets"][field]
            a["bytes"] = api.head_size(a["fetch"])
            done += 1
            if done % save_every == 0 or done == total:
                recompute_totals(inv)
                save_manifest(inv, manifest_path)
                elapsed = time.monotonic() - started
                rate = done / elapsed if elapsed else 0
                eta = (total - done) / rate if rate else 0
                print(
                    f"\r  {done}/{total} ({done * 100 // total}%)  "
                    f"{rate:.1f}/s  eta {int(eta) // 60}m{int(eta) % 60:02d}s   ",
                    end="",
                    flush=True,
                )
        print()
    except KeyboardInterrupt:
        recompute_totals(inv)
        save_manifest(inv, manifest_path)
        print(f"\n  interrupted after {done}/{total} — saved; re-run to resume")
        raise

    recompute_totals(inv)
    return done


def recompute_totals(inv):
    totals = Counter()
    missing = 0
    unreachable = Counter()
    for rec in inv["videos"]:
        for field, a in rec["assets"].items():
            if a is None:
                continue
            if not a.get("fetch"):
                unreachable[field] += 1      # no API route exists for this asset type
            elif a["bytes"] is None:
                missing += 1
            else:
                totals[field] += a["bytes"]
    inv["byte_totals"] = dict(totals)
    inv["bytes_unmeasured"] = missing
    inv["unreachable_over_api"] = dict(unreachable)


def main():
    ap = argparse.ArgumentParser(description="Inventory the LiveORC API (TODO-114 Phase 1)")
    ap.add_argument("--institute", required=True, help="institute id; /api/site/ is empty without it")
    ap.add_argument("--site", help="restrict to one site id")
    ap.add_argument("--base", default=DEFAULT_BASE)
    ap.add_argument("--sizes", action="store_true", help="HEAD every asset for Content-Length (slow)")
    ap.add_argument("--delay", type=float, default=0.0, help="seconds between requests")
    ap.add_argument("--out", default=None, help="output dir (default: <repo>/data/liveorc-mirror)")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()

    email = os.environ.get("LIVEORC_EMAIL")
    password = os.environ.get("LIVEORC_PASSWORD")
    if not email or not password:
        sys.exit("ERROR: set LIVEORC_EMAIL and LIVEORC_PASSWORD")

    out_dir = Path(args.out) if args.out else Path(__file__).resolve().parents[3] / "data" / "liveorc-mirror"
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"LiveORC inventory — {args.base}")
    print(f"  account   {email}")
    print(f"  output    {out_dir}")
    if args.sizes:
        print("  --sizes   HEAD per asset; this is 4 requests per video record")
    print()

    api = Api(args.base, email, password, delay=args.delay, verbose=args.verbose)

    # Phase 0's remaining item: prove refresh works before relying on it.
    before = api.access
    api._refresh_access()
    print(f"  token refresh: {'OK' if api.access and api.access != before else 'CHECK — token unchanged'}")
    print()

    sites = discover_sites(api, args.institute, args.site)
    if not sites:
        sys.exit("ERROR: no sites visible. Is the account a Member of this institute?")
    print(f"Sites visible: {', '.join(map(str, sites))}\n")

    grand_videos = 0
    grand_nulls = Counter()
    grand_bytes = Counter()
    all_creators = Counter()

    for site in sites:
        print(f"Site {site}")
        inv = inventory_site(api, site)
        if "error" in inv:
            print(f"  ERROR: {inv['error']}\n")
            continue

        site_dir = out_dir / str(site)
        site_dir.mkdir(parents=True, exist_ok=True)
        manifest = site_dir / "manifest.json"

        print(f"  videos           {inv['video_count']}")
        print(f"  timeseries       {inv['timeseries_count']} (HTTP {inv['timeseries_status']})")
        print(f"  status           {inv['status_histogram']}")
        print(f"  creator ids      {inv['creators']}")
        print(f"  null assets      {inv['null_assets']}")

        recompute_totals(inv)
        save_manifest(inv, manifest)          # manifest first, then work down it

        if args.sizes:
            carried = carry_over_sizes(inv, manifest)
            if carried:
                print(f"  resumed          {carried} sizes carried over from the previous run")
            size_pass(api, inv, manifest)
            print(f"  bytes            { {k: human(v) for k, v in inv['byte_totals'].items()} }")
            if inv.get("bytes_unmeasured"):
                print(f"  unmeasured       {inv['bytes_unmeasured']} assets returned no Content-Length")
            if inv.get("unreachable_over_api"):
                print(f"  UNREACHABLE      {inv['unreachable_over_api']} — no API route serves these")

        grand_videos += inv["video_count"]
        for k, n in inv["null_assets"].items():
            grand_nulls[k] += n
        for k, n in (inv["byte_totals"] or {}).items():
            grand_bytes[k] += n
        for k, n in inv["creators"].items():
            all_creators[k] += n

        print(f"  wrote            {manifest}\n")

    # -- reconciliation ------------------------------------------------------
    print("─" * 72)
    print(f"TOTAL video records: {grand_videos}")
    print(f"  TODO-114's doc says ~1165 — difference {grand_videos - 1165:+d}. "
          f"The API is the authority here; treat a large gap as a stale doc, not a bug.")
    print(f"  null assets across all sites: {dict(grand_nulls)}")
    print(f"  creator ids across all sites: {dict(all_creators)}")

    # The mirror account must not be the creator of anything — that is what makes
    # it read-only by construction rather than by policy.
    me = os.environ.get("LIVEORC_USER_ID")
    if me and int(me) in all_creators:
        print(f"  WARNING: the mirror account ({me}) is the creator of records — "
              "it can DELETE those. Investigate before trusting the read-only claim.")

    if args.sizes:
        print("\n  Byte totals vs the runbook's figures:")
        expectations = {"file": ("video", 26 * 1024**3), "thumbnail": ("thumb", 9.5 * 1024**2)}
        for field, (label, expected) in expectations.items():
            got = grand_bytes.get(field, 0)
            pct = (got / expected * 100) if expected else 0
            print(f"    {label:9s} {human(got):>10s}  vs ~{human(expected):>10s}  ({pct:.0f}%)")
        print(f"    {'image':9s} {human(grand_bytes.get('image', 0)):>10s}  (no runbook figure)")
        print(f"    {'keyframe':9s} {'—':>10s}  ~1.3 GB per the runbook, but NO API route "
              "serves keyframes:\n                 they cannot be mirrored over REST at all.")
        print("\n  A large gap is information, not an error: it means the API does not"
              "\n  see everything on disk, which changes what the mirror is worth.")
    else:
        print("\n  Re-run with --sizes to reconcile against the runbook's 26 GB / 1.3 GB / 9.5 MB.")
    print()


if __name__ == "__main__":
    main()
