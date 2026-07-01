#!/usr/bin/env python3
"""Reprocess historical Sukabumi videos on LiveORC with the IPB Fit 6 config.

WHY THIS EXISTS (and why LiveORC's own reprocess won't do):
  LiveORC's server-side task (api/tasks.py:run_nodeorc) feeds the *stored* water
  level into pyorc as a fixed input (`h_a = video.time_series.h`) and only writes
  back discharge. For a gauge-less site that is wrong: the historical h values were
  detected on the OLD salvage datum, so pairing them with the new z_0=615.0 camera
  config gives inconsistent geometry. We must RE-DETECT the optical water level.

  This script invokes the SAME certified engine ORC-OS uses on the station
  (`pyorc.service.velocity_flow_subprocess`) but with `h_a=None` + the WL
  cross-section, which triggers fresh optical water-level detection — then writes
  BOTH the new h and the new discharge over the existing time_series row.

HOW IT RUNS:
  Inside the LiveORC `webapp` container (Django + pyorc are both present there):
    docker cp reprocess_fit6.py webapp:/tmp/
    docker exec -it webapp python /tmp/reprocess_fit6.py \
        --site-id <SUKABUMI_SITE_ID> --video-config-id <FIT6_VC_ID> [--dry-run|--commit] ...

SAFETY:
  * --dry-run is the DEFAULT. Nothing is written unless you pass --commit.
  * Replace-in-place: each Video.time_series is OneToOne, so updating that row
    overwrites the salvage result — no duplicates, no orphans.
  * A video is only written when pyorc returns 0 AND h and q_50 are finite.
    Otherwise it is recorded as failed/skipped and the OLD row is left untouched.
  * Run backup_liveorc_db.sh FIRST. Validate on staging before prod.
"""
import argparse
import copy
import datetime as dt
import glob
import json
import os
import shutil
import sys
import threading
import time
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed


def _fmt_dur(s):
    if s != s or s == float("inf"):
        return "?"
    s = int(s)
    h, m, sec = s // 3600, (s % 3600) // 60, s % 60
    return f"{h}h{m:02d}m" if h else (f"{m}m{sec:02d}s" if m else f"{sec}s")


def _progress_line(done, total, counts, t0):
    el = time.monotonic() - t0
    rate = done / el if el > 0 else 0.0
    eta = (total - done) / rate if rate > 0 else float("inf")
    pct = 100.0 * done / total if total else 0.0
    tally = " ".join(f"{k}={v}" for k, v in sorted(counts.items()))
    return (f"{done}/{total} ({pct:.1f}%) | {tally} | elapsed {_fmt_dur(el)} | "
            f"{rate * 60:.1f}/min | ETA {_fmt_dur(eta)}")

# --- Django bootstrap (we run inside the LiveORC container) -----------------
# The LiveORC project package lives at /liveorc; make sure it's importable no
# matter what cwd we're launched from (e.g. /tmp via `docker exec`).
_APP_DIR = os.environ.get("LIVEORC_APP_DIR", "/liveorc")
if os.path.isdir(_APP_DIR) and _APP_DIR not in sys.path:
    sys.path.insert(0, _APP_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LiveORC.settings")
import django  # noqa: E402

django.setup()

import numpy as np  # noqa: E402
import xarray as xr  # noqa: E402

from api.models import Video, VideoConfig, VideoStatus  # noqa: E402
from pyorc.service import velocity_flow_subprocess  # noqa: E402


def recipe_update_cross_section(recipe, cross_section):
    """Inject the chosen cross-section geojson into the recipe's transect (+ plot).

    Inlined verbatim from api.task_utils (LiveORC 0.3.0). We DON'T import it, because
    api.task_utils pulls in `nodeorc`, which is not installed in the LiveORC image.
    """
    recipe = copy.deepcopy(recipe)
    transect_template = recipe["transect"]
    transect = {}
    trans_no = 0
    for k, v in transect_template.items():
        if k != "write":
            trans_no += 1
            if "geojson" in v:
                del v["geojson"]
            if "shapefile" in v:
                del v["shapefile"]
            v["geojson"] = cross_section
            transect[f"transect_{trans_no}"] = v
            break
    transect["write"] = True
    recipe["transect"] = transect
    if "plot" in recipe:
        for k, v in recipe["plot"].items():
            if "transect" in v:
                transect = {}
                transect_template = v["transect"]
                for n, (k_, v_) in enumerate(transect_template.items()):
                    transect[f"transect_{n + 1}"] = v_
                    break
                v["transect"] = transect
            recipe["plot"][k] = v
    return recipe


_print_lock = threading.Lock()

# libhdf5 is NOT thread-safe: concurrent xr.open_dataset() calls from multiple
# ThreadPoolExecutor workers segfault inside libhdf5 (observed as SIGSEGV in
# libhdf5.so from ThreadPoolExecutor threads, which kills the whole run with no
# Python traceback). Serialize ALL in-process netCDF reads through one global lock.
# The heavy pyorc step runs in a SEPARATE subprocess, so workers still parallelize
# it — only the brief netCDF reads here are serialized.
_hdf5_lock = threading.Lock()


def log(msg):
    with _print_lock:
        print(msg, flush=True)


def features_of(xs):
    """GeoJSON features for a CrossSection model instance (or None)."""
    return None if xs is None else xs.features


def stage_video_file(video, dest_dir):
    """Stream the raw video to a local temp path.

    Storage-agnostic: uses Django's FieldFile, so it works for both
    FileSystemStorage (local copy) and S3Storage/MinIO (streams from the bucket).
    Returns the local path, or raises on failure.
    """
    if not getattr(video, "file", None) or not video.file.name:
        raise FileNotFoundError("video has no file")
    dest = os.path.join(dest_dir, os.path.basename(video.file.name))
    try:
        with video.file.open("rb") as src, open(dest, "wb") as out:
            for chunk in iter(lambda: src.read(1 << 20), b""):
                out.write(chunk)
    finally:
        try:
            video.file.close()
        except Exception:
            pass
    return dest


def find_discharge_nc(output_dir):
    """Locate the transect netCDF pyorc wrote (the one carrying river_flow/h_a)."""
    for fn in sorted(glob.glob(os.path.join(output_dir, "**", "*.nc"), recursive=True)):
        try:
            with _hdf5_lock, xr.open_dataset(fn) as ds:  # libhdf5 not thread-safe
                if "river_flow" in ds or "h_a" in ds:
                    return fn
        except Exception:
            continue
    return None


def extract_results(nc):
    """Map the pyorc transect output to time_series fields (mirrors ORC-OS update_timeseries)."""
    with _hdf5_lock, xr.open_dataset(nc) as ds:  # libhdf5 not thread-safe
        h = float(ds.h_a)
        Q = np.abs(ds.river_flow.values)
        q = 2 if ("quantile" in ds.dims and len(ds["quantile"]) == 5) else 0
        if "v_eff" in ds:
            v_av = float(np.abs(ds.isel(quantile=q).transect.get_v_surf().values))
            v_bulk = float(np.abs(ds.isel(quantile=q).transect.get_v_bulk().values))
        else:
            v_av = v_bulk = float("nan")
        if "q_nofill" in ds:
            ds.transect.get_river_flow(q_name="q_nofill")
            Q_nofill = np.abs(ds.river_flow.values)
            frac = float(Q_nofill[2] / Q[2] * 100) if np.isfinite(Q[2]) and Q[2] else float("nan")
        else:
            frac = float("nan")
    fin = lambda x: float(x) if np.isfinite(x) else None  # noqa: E731
    return {
        "h": fin(h),
        "q_05": fin(Q[0]), "q_25": fin(Q[1]), "q_50": fin(Q[2]),
        "q_75": fin(Q[3]), "q_95": fin(Q[4]),
        "v_av": fin(v_av), "v_bulk": fin(v_bulk),
        "fraction_velocimetry": fin(frac),
    }


def process_one(video, fit6, recipe_base, cross, cross_wl, out_base, commit, repoint, recover, sleep=0.0):
    """Run one video; return a result dict (and write to DB if commit)."""
    ts = video.time_series
    old = {f: getattr(ts, f, None) for f in
           ("h", "q_50", "v_av", "fraction_velocimetry")} if ts else {}
    rec = {
        "video_id": video.id,
        "timestamp": video.timestamp.isoformat() if video.timestamp else None,
        "file": str(video.file),
        "time_series_id": getattr(ts, "id", None),
        "old": old,
        "new": None,
        "status": "skipped",
        "error": None,
    }
    # A video with no time_series can only be RECOVERED (create a new row) if --recover.
    if ts is None and not recover:
        rec["status"], rec["error"] = "no_timeseries", "no time_series to overwrite (use --recover to create one)"
        return rec

    # per-video work dir (fresh, so pyorc's stale-output cache never silently skips)
    work = os.path.join(out_base, str(video.id))
    out = os.path.join(work, "output")
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(out, exist_ok=True)

    try:
        try:
            vf = stage_video_file(video, work)  # storage-agnostic (FS or S3/MinIO)
        except Exception as e:
            rec["status"], rec["error"] = "missing_file", f"cannot read file: {e}"
            return rec
        recipe = recipe_update_cross_section(recipe_base, cross)  # fill transect with discharge XS
        res = velocity_flow_subprocess(
            recipe=recipe,
            videofile=vf,
            cameraconfig=fit6["cameraconfig"],
            prefix="",
            output=out,
            h_a=None,            # <-- force fresh OPTICAL water-level detection
            cross=cross,
            cross_wl=cross_wl,   # WL cross-section for the optical detection
        )
        if getattr(res, "returncode", 1) != 0:
            rec["status"] = "pyorc_error"
            rec["error"] = (getattr(res, "stderr", "") or "")[-800:]
            return rec
        nc = find_discharge_nc(out)
        if nc is None:
            rec["status"], rec["error"] = "no_output", "no transect netCDF produced"
            return rec
        new = extract_results(nc)
        rec["new"] = new
        if new["h"] is None or new["q_50"] is None:
            rec["status"] = "incomplete"  # optical WL or PIV failed → leave old row alone
            rec["error"] = f"h={new['h']} q_50={new['q_50']}"
            return rec
        rec["status"] = "ok" if ts is not None else "recovered"
        if commit:
            from api.models import TimeSeries  # local import; api.models already set up
            vid_updates = {"status": VideoStatus.DONE}
            if repoint:
                vid_updates["video_config_id"] = fit6["id"]
            # IMPORTANT: write with .update()/bulk_create to bypass the model save()
            # overrides — Video.save() regenerates thumbnails from the file, and
            # TimeSeries.save() auto-associates the nearest video. We want neither.
            if ts is not None:
                TimeSeries.objects.filter(id=ts.id).update(**new)          # replace in place
            else:
                new_ts = TimeSeries(
                    site_id=fit6["site_id"],
                    timestamp=video.timestamp,
                    creator_id=video.creator_id,   # attribute to the video's uploader
                    **new,
                )
                TimeSeries.objects.bulk_create([new_ts])                    # no save() side effects
                vid_updates["time_series_id"] = new_ts.id                   # link the new row
            Video.objects.filter(id=video.id).update(**vid_updates)
    except Exception as e:
        rec["status"] = "exception"
        rec["error"] = f"{e}\n{traceback.format_exc()[-1200:]}"
    finally:
        shutil.rmtree(work, ignore_errors=True)  # don't let 1,297 temp dirs fill the disk
        if sleep:
            time.sleep(sleep)                     # throttle: ease load on the box
    return rec


def main():
    ap = argparse.ArgumentParser(description="Reprocess Sukabumi history with IPB Fit 6 (optical WL).")
    ap.add_argument("--site-id", type=int, required=True)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--video-config-id", type=int, help="Fit 6 VideoConfig id on LiveORC")
    g.add_argument("--video-config-name", help="Fit 6 VideoConfig name (alternative to id)")
    ap.add_argument("--commit", action="store_true", help="WRITE results (default: dry-run)")
    ap.add_argument("--repoint", action="store_true",
                    help="also set each video.video_config to Fit 6 (keeps config↔result consistent)")
    ap.add_argument("--recover", action="store_true",
                    help="for videos with NO time_series (errored/never-processed): CREATE one "
                         "if Fit 6 succeeds, instead of skipping")
    ap.add_argument("--limit", type=int, default=None, help="process at most N videos")
    ap.add_argument("--ids", default=None, help="comma-separated video ids (overrides site scan)")
    ap.add_argument("--start", default=None, help="only videos with timestamp >= ISO date")
    ap.add_argument("--stop", default=None, help="only videos with timestamp <= ISO date")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--sleep", type=float, default=0.0,
                    help="seconds each worker pauses after a video (throttle CPU/IO)")
    ap.add_argument("--progress-every", type=int, default=20,
                    help="print a PROGRESS line (with %% done + ETA) every N videos")
    ap.add_argument("--out-base", default="/tmp/reprocess_fit6")
    ap.add_argument("--log-dir", default="./reprocess-logs")
    args = ap.parse_args()

    dry = not args.commit
    os.makedirs(args.log_dir, exist_ok=True)
    os.makedirs(args.out_base, exist_ok=True)

    # resolve Fit 6 config
    if args.video_config_id:
        fit6_vc = VideoConfig.objects.get(id=args.video_config_id)
    else:
        fit6_vc = VideoConfig.objects.get(site_id=args.site_id, name=args.video_config_name)
    if fit6_vc.cross_section is None or fit6_vc.recipe is None or fit6_vc.camera_config is None:
        sys.exit(f"Fit 6 VideoConfig {fit6_vc.id} is missing camera_config/recipe/cross_section.")
    if fit6_vc.cross_section_wl is None:
        log("WARNING: Fit 6 VideoConfig has no cross_section_wl — optical WL detection needs it. "
            "Proceeding, but expect 'incomplete' unless the discharge XS doubles as WL.")

    fit6 = {"id": fit6_vc.id, "site_id": fit6_vc.site_id, "cameraconfig": fit6_vc.camera_config.data}
    recipe_base = fit6_vc.recipe.data
    cross = features_of(fit6_vc.cross_section)
    cross_wl = features_of(fit6_vc.cross_section_wl)

    # build the work list
    if args.ids:
        qs = Video.objects.filter(id__in=[int(x) for x in args.ids.split(",")])
    else:
        qs = Video.objects.filter(video_config__site_id=args.site_id)
    if args.start:
        qs = qs.filter(timestamp__gte=args.start)
    if args.stop:
        qs = qs.filter(timestamp__lte=args.stop)
    qs = qs.select_related("time_series", "video_config").order_by("timestamp")
    videos = list(qs[: args.limit] if args.limit else qs)

    log(f"{'DRY-RUN' if dry else 'COMMIT'} | Fit6 VideoConfig={fit6_vc.id} ({fit6_vc.name}) | "
        f"site={args.site_id} | videos={len(videos)} | workers={args.workers} | "
        f"repoint={args.repoint} | recover={args.recover}")
    if not videos:
        sys.exit("no videos matched.")

    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")  # local stamp for the log file name
    base = f"reprocess_{'dry' if dry else 'commit'}_{stamp}"
    jsonl = os.path.join(args.log_dir, base + ".jsonl")
    progress_path = os.path.join(args.log_dir, base + ".progress")
    total = len(videos)
    counts = {}
    done = 0
    t0 = time.monotonic()

    def emit_progress():
        line = _progress_line(done, total, counts, t0)
        try:                                   # live progress file (survives a crash)
            with open(progress_path, "w") as pf:
                pf.write(line + "\n")
        except OSError:
            pass
        return line

    with open(jsonl, "w") as fh, ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(process_one, v, fit6, recipe_base, cross, cross_wl,
                          args.out_base, args.commit, args.repoint, args.recover, args.sleep): v
                for v in videos}
        for fut in as_completed(futs):
            rec = fut.result()
            fh.write(json.dumps(rec) + "\n"); fh.flush()  # results streamed to disk as we go
            counts[rec["status"]] = counts.get(rec["status"], 0) + 1
            done += 1
            line = emit_progress()
            if args.progress_every and (done % args.progress_every == 0 or done == total):
                log(f"==> PROGRESS {line}")
            if rec["status"] in ("ok", "recovered"):
                o, n = rec["old"], rec["new"]
                if rec["status"] == "recovered":
                    log(f"[{done}/{total}] vid {rec['video_id']} RECOVERED  "
                        f"h={n['h']:.3f}  q50={n['q_50']:.3f}")
                else:
                    dh = (n["h"] - o["h"]) if (o.get("h") is not None and n["h"] is not None) else float("nan")
                    log(f"[{done}/{total}] vid {rec['video_id']} OK  "
                        f"h {o.get('h')}->{n['h']} (Δ{dh:+.3f})  q50 {o.get('q_50')}->{n['q_50']}")
            else:
                # show the last line of the error (the real exception), not the tqdm spam
                err = (rec["error"] or "").replace("\r", "\n").strip().splitlines()
                log(f"[{done}/{total}] vid {rec['video_id']} {rec['status'].upper()} "
                    f"{(err[-1][:140] if err else '')}")

    log("\n==== summary ====")
    log(f"  {_progress_line(done, total, counts, t0)}")
    for k in sorted(counts):
        log(f"  {k:14s} {counts[k]}")
    log(f"  results: {jsonl}")
    log(f"  progress: {progress_path}")
    if dry:
        log("\nDRY-RUN only — nothing written. Re-run with --commit (after backup + staging validation).")


if __name__ == "__main__":
    main()
