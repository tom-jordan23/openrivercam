#!/usr/bin/env python3
"""orc_mirror.py — TODO-114 Phase 2: pull an independent copy of LiveORC's videos.

WHY
    Two jobs at once. TODO-114 wants a verifiable copy of the media that exists
    somewhere other than the container writable layer, so TODO-112's Phase 5
    `rsync --itemize-changes` can be checked against something external instead
    of only against the host itself. And the videos are the input to a local
    reprocess with swapped transects — `reprocess/build_staging_local.sh` needs
    real video files on disk before it can stand up a staging LiveORC.

WHERE THE BYTES ACTUALLY COME FROM
    NOT from the `file` URL in the serializer. Measured 2026-08-25 with
    probe_media_access.py: those URLs return 404 with AND without a JWT, because
    prod media lives in MinIO behind Django's storage API and was never on the
    nginx filesystem — which the reprocess runbook already said in passing
    ("on prod they live in MinIO ... or the LiveORC video-download API").

    Bytes come from the DRF action `/api/site/{site}/video/{id}/playback/`, which
    serves video/mp4 with a correct Content-Length and supports HEAD.

    The dead `file` URL is still load-bearing as an IDENTIFIER: its path gives the
    STORAGE-RELATIVE location (videos/4/20260526/…mp4). Files are written into a
    tree mirroring those paths, because the reprocessor reads videos through
    Django's storage API and they must resolve at the same relative locations
    locally as they do on prod.

WHAT IT TOUCHES
    On the server: nothing. GET and HEAD only, plus the one POST to /api/token/.
    The mirror account is an institute member that created nothing, so upstream's
    IsOwnerOrReadOnlyAsInstitute makes writes impossible; this script additionally
    issues no write verb at all.

    Locally: writes under data/liveorc-mirror/, gitignored at the repo root. This
    repo is public — no media or token is ever committed.

PACING
    TODO-114 flags the hazard: the host is a t3.large whose `/` was at 100% on
    2026-08-10, and these requests go through Django rather than nginx. Downloads
    stream to disk and are never held in memory. Default --delay 0.2 keeps this a
    background trickle rather than a load test. Raise it if the host is busy.

RESUME
    Safe to interrupt and re-run. A file already present with the expected size is
    skipped without a request. Partial downloads land in a .part file and are
    re-fetched, never treated as complete. Checksums and sizes are checkpointed
    into the manifest as each file lands.

USAGE
    export LIVEORC_EMAIL=... LIVEORC_PASSWORD=...

    ./orc_mirror.py --site 4 --check            # dry run: what would be pulled
    ./orc_mirror.py --site 4                    # the real pull
    ./orc_mirror.py --site 4 --limit 5          # smoke test on 5 files first
    ./orc_mirror.py --site 4 --verify           # re-check sizes+checksums, no downloads
"""

import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "orc_inventory", Path(__file__).with_name("orc_inventory.py")
)
_inv = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_inv)

CHUNK = 1 << 20  # 1 MiB


def storage_relative_path(file_url):
    """videos/4/20260526/20260526T040126.mp4 from the serializer's dead `file` URL.

    The URL does not serve, but its path is the storage-relative location the
    reprocessor will expect. Anything before and including /media/ is stripped.
    """
    path = urllib.parse.urlparse(file_url).path
    marker = "/media/"
    idx = path.find(marker)
    rel = path[idx + len(marker):] if idx >= 0 else path.lstrip("/")
    # Refuse anything that would escape the mirror root.
    parts = [p for p in rel.split("/") if p not in ("", ".", "..")]
    return "/".join(parts)


def stream_to_file(api, url, dest, delay=0.0, _retried=False):
    """Stream one asset to disk. Returns (bytes_written, sha256) or raises.

    Never buffers the whole file: TODO-114's hazard is disk and memory pressure,
    and a 9 MB video times 2630 is not something to hold in RAM.
    """
    if delay:
        time.sleep(delay)
    req = urllib.request.Request(
        url, headers={"Authorization": f"Bearer {api.access}"}, method="GET"
    )
    part = dest.with_suffix(dest.suffix + ".part")
    part.parent.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256()
    written = 0
    try:
        with urllib.request.urlopen(req, context=api.ctx, timeout=300) as r, open(part, "wb") as fh:
            while True:
                chunk = r.read(CHUNK)
                if not chunk:
                    break
                fh.write(chunk)
                digest.update(chunk)
                written += len(chunk)
    except urllib.error.HTTPError as e:
        part.unlink(missing_ok=True)
        # The access token is good for 360 minutes; a 23 GB pull outlives it.
        if e.code == 401 and not _retried:
            api._refresh_access()
            return stream_to_file(api, url, dest, delay=delay, _retried=True)
        raise
    except Exception:
        part.unlink(missing_ok=True)
        raise

    part.replace(dest)          # atomic: a .part is never mistaken for a finished file
    return written, digest.hexdigest()


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(CHUNK), b""):
            digest.update(chunk)
    return digest.hexdigest()


def human(n):
    return _inv.human(n)


def main():
    ap = argparse.ArgumentParser(description="Mirror LiveORC videos (TODO-114 Phase 2)")
    ap.add_argument("--site", required=True)
    ap.add_argument("--institute", default="1")
    ap.add_argument("--base", default=_inv.DEFAULT_BASE)
    ap.add_argument("--check", action="store_true", help="dry run — list work, download nothing")
    ap.add_argument("--verify", action="store_true", help="re-check existing files, download nothing")
    ap.add_argument("--limit", type=int, help="stop after N files (smoke test)")
    ap.add_argument("--delay", type=float, default=0.2, help="seconds between downloads")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    email, password = os.environ.get("LIVEORC_EMAIL"), os.environ.get("LIVEORC_PASSWORD")
    if not email or not password:
        sys.exit("ERROR: set LIVEORC_EMAIL and LIVEORC_PASSWORD")

    root = Path(args.out) if args.out else Path(__file__).resolve().parents[3] / "data" / "liveorc-mirror"
    site_dir = root / str(args.site)
    media_dir = site_dir / "media"
    manifest_path = site_dir / "manifest.json"
    log_path = site_dir / "mirror-log.jsonl"

    print(f"\nLiveORC video mirror — site {args.site}")
    print(f"  source    {args.base}")
    print(f"  dest      {media_dir}")
    mode = "CHECK (no downloads)" if args.check else "VERIFY (no downloads)" if args.verify else "PULL"
    print(f"  mode      {mode}\n")

    api = _inv.Api(args.base, email, password, delay=0.0)

    # Always re-list. The station came back online 2026-08-20, so a manifest from
    # an earlier run may already be stale — TODO-114 says to re-run Phase 1 and
    # diff rather than trusting an old baseline.
    print("Listing records ...")
    inv = _inv.inventory_site(api, int(args.site))
    if "error" in inv:
        sys.exit(f"ERROR: {inv['error']}")

    if manifest_path.exists():
        try:
            prev = json.loads(manifest_path.read_text())
            drift = inv["video_count"] - prev.get("video_count", inv["video_count"])
            if drift:
                print(f"  NOTE: {drift:+d} records since the stored manifest — uploads are live.")
        except (json.JSONDecodeError, OSError):
            pass

    targets = []
    for rec in inv["videos"]:
        asset = rec["assets"].get("file")
        if not asset:
            continue                                   # null file: no video to pull
        targets.append((rec, asset, media_dir / storage_relative_path(asset["url"])))

    print(f"  {inv['video_count']} records, {len(targets)} with a video file\n")
    if args.limit:
        targets = targets[: args.limit]
        print(f"  --limit {args.limit}: {len(targets)} selected\n")

    _inv.carry_over_sizes(inv, manifest_path)

    pending, present, mismatched = [], [], []
    for rec, asset, dest in targets:
        if not dest.exists():
            pending.append((rec, asset, dest))
            continue
        on_disk = dest.stat().st_size
        expected = asset.get("bytes")
        if expected is None or on_disk == expected:
            asset["bytes"] = on_disk
            present.append((rec, asset, dest))
        else:
            mismatched.append((rec, asset, dest, on_disk, expected))

    print(f"  already present  {len(present)}")
    print(f"  to download      {len(pending)}")
    if mismatched:
        print(f"  SIZE MISMATCH    {len(mismatched)} — will be re-fetched")
    print()

    if args.check:
        sample = pending[:5]
        if sample:
            print("  Sizing a sample to estimate the pull ...")
            sizes = [api.head_size(a["fetch"]) for _, a, _ in sample]
            good = [s for s in sizes if s]
            if good:
                est = sum(good) / len(good) * len(pending)
                print(f"  mean {human(sum(good) / len(good))} × {len(pending)} ≈ {human(est)}")
                free = shutil.disk_usage(root).free
                print(f"  free on this volume: {human(free)}")
                if est > free * 0.9:
                    print("  WARNING: that is more than 90% of free space.")
        print("\n  Dry run only. Re-run without --check to pull.\n")
        return

    if args.verify:
        print("Verifying files on disk ...")
        bad = 0
        for i, (rec, asset, dest) in enumerate(present, 1):
            actual = sha256_of(dest)
            recorded = asset.get("sha256")
            if recorded and actual != recorded:
                print(f"  CHECKSUM MISMATCH  video {rec['id']}  {dest}")
                bad += 1
            if i % 100 == 0:
                print(f"  {i}/{len(present)} ...")
        print(f"\n  {len(present) - bad} verified, {bad} mismatched\n")
        return

    work = [(r, a, d) for r, a, d, *_ in mismatched] + pending
    if not work:
        print("  Nothing to do — the mirror is complete.\n")
        _inv.recompute_totals(inv)
        _inv.save_manifest(inv, manifest_path)
        return

    free = shutil.disk_usage(root).free
    print(f"  free space: {human(free)}\n")

    started = time.monotonic()
    done = bytes_done = failed = 0
    log = open(log_path, "a")

    try:
        for rec, asset, dest in work:
            try:
                n, digest = stream_to_file(api, asset["fetch"], dest, delay=args.delay)
            except Exception as exc:                    # one bad file must not end the run
                failed += 1
                print(f"\n  FAILED video {rec['id']}: {exc}")
                log.write(json.dumps({"video": rec["id"], "error": str(exc)}) + "\n")
                log.flush()
                continue

            asset["bytes"] = n
            asset["sha256"] = digest
            asset["path"] = str(dest.relative_to(root))
            done += 1
            bytes_done += n
            log.write(json.dumps({
                "video": rec["id"], "timestamp": rec["timestamp"],
                "bytes": n, "sha256": digest, "path": asset["path"],
            }) + "\n")
            log.flush()

            if done % 25 == 0 or done == len(work):
                _inv.recompute_totals(inv)
                _inv.save_manifest(inv, manifest_path)
                elapsed = time.monotonic() - started
                rate = bytes_done / elapsed if elapsed else 0
                eta = (len(work) - done) * (elapsed / done) if done else 0
                print(f"\r  {done}/{len(work)}  {human(bytes_done)}  "
                      f"{human(rate)}/s  eta {int(eta)//60}m{int(eta)%60:02d}s   ",
                      end="", flush=True)
        print()
    except KeyboardInterrupt:
        print("\n  interrupted — checkpointing")
    finally:
        _inv.recompute_totals(inv)
        _inv.save_manifest(inv, manifest_path)
        log.close()

    print(f"\n  downloaded {done} files, {human(bytes_done)}, {failed} failed")
    print(f"  manifest {manifest_path}")
    print(f"  log      {log_path}")
    if failed:
        print("  Re-run to retry the failures — completed files are skipped.")
    print()


if __name__ == "__main__":
    main()
