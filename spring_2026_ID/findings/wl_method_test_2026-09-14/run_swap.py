"""Transect-swap test B: process mirrored Sukabumi clips under both transect
arrangements with the station's own software (ORC-OS 0.6.0 image, pyorc 0.9.9).

Runs INSIDE the orc-os-v060-orcapi container. Touches nothing but /work.

Inputs, all from the 2026-06-29 prod dump (VideoConfig 3, "Sukabumi IPB"):
  /work/prod/api_recipe_4.json         recipe 4
  /work/prod/api_cameraconfig_3.json   camera config 3
  /work/prod/xs_4_ipb_discharge.geojson   upstream transect, 13 pts (live: discharge)
  /work/prod/xs_5_ipb_wl_optical.geojson  downstream transect, 14 pts (live: water level)

Arrangements:
  live  cross = xs4 (upstream),   cross_wl = xs5 (downstream)   — what is deployed
  swap  cross = xs5 (downstream), cross_wl = xs4 (upstream)

The pyorc call mirrors orc_api/schemas/video.py:277 on 0.6.0: h_a=None (optical
water level), recipe transect_1 filled with the discharge cross-section as
recipe_transect_filled does, rvec/tvec of VideoConfig 3 are zero so the
cross-section rotate/translate is the identity.

Usage: python3 run_swap.py /work/jobs.json /work/out [workers]
"""
import copy
import glob
import json
import logging
import os
import sys
import time
import traceback
import threading
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import xarray as xr
from pyorc.service import velocity_flow_subprocess

W = "/work/prod"
RECIPE = json.load(open(f"{W}/api_recipe_4.json"))
CAM = json.load(open(f"{W}/api_cameraconfig_3.json"))
XS_UP = json.load(open(f"{W}/xs_4_ipb_discharge.geojson"))
XS_DOWN = json.load(open(f"{W}/xs_5_ipb_wl_optical.geojson"))
_HDF5 = threading.Lock()  # libhdf5 is not thread-safe; serialize netCDF reads
ARR = {"live": (XS_UP, XS_DOWN), "swap": (XS_DOWN, XS_UP), "up_both": (XS_UP, XS_UP)}


def fill_recipe(recipe, cross, method="grayscale"):
    """Same as ORC-OS 0.6.0 VideoConfigResponse.recipe_transect_filled.

    `method` replaces the colour method of every water-level pass (pyorc 0.9.9
    accepts grayscale, hue, sat, val); the passes' other options are kept.
    """
    recipe = copy.deepcopy(recipe)
    if "transect" in recipe and "transect_1" in recipe["transect"]:
        recipe["transect"]["transect_1"].pop("shapefile", None)
        recipe["transect"]["transect_1"]["geojson"] = cross
    wl = recipe.get("water_level", {})
    base = wl.get("frames_options", [])
    if method.endswith("_then_gray"):
        # the deployed passes with <first>, then the deployed passes with grayscale;
        # pyorc accepts the first pass that clears s2n_thres
        first = method[: -len("_then_gray")]
        wl["frames_options"] = [dict(o, method=first) for o in base] + [dict(o, method="grayscale") for o in base]
    else:
        for opt in base:
            opt["method"] = method
    return recipe


def extract(nc):
    """Same mapping as reprocess_fit6.extract_results (ORC-OS update_timeseries)."""
    with xr.open_dataset(nc) as ds:
        h = float(ds.h_a)
        Q = np.abs(ds.river_flow.values)
        q = 2 if ("quantile" in ds.dims and len(ds["quantile"]) == 5) else 0
        v_av = float(np.abs(ds.isel(quantile=q).transect.get_v_surf().values)) if "v_eff" in ds else float("nan")
        frac = float("nan")
        if "q_nofill" in ds:
            ds.transect.get_river_flow(q_name="q_nofill")
            Qn = np.abs(ds.river_flow.values)
            frac = float(Qn[2] / Q[2] * 100) if np.isfinite(Q[2]) and Q[2] else float("nan")
    fin = lambda x: round(float(x), 4) if np.isfinite(x) else None  # noqa: E731
    return {"h": fin(h), "q_50": fin(Q[2]), "v_av": fin(v_av), "fraction_velocimetry": fin(frac)}


def run(job, out_root):
    vid, arr, clip = job["id"], job["arr"], job["clip"]
    method = job.get("method", "grayscale")
    out = os.path.join(out_root, f"{vid}_{arr}" if method == "grayscale" and "method" not in job else f"{vid}_{arr}_{method}")
    os.makedirs(out, exist_ok=True)
    log_path = os.path.join(out, "run.log")
    lg = logging.getLogger(f"swap.{vid}.{arr}")
    lg.setLevel(logging.DEBUG)
    lg.propagate = False
    fh = logging.FileHandler(log_path, mode="w")
    fh.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    lg.addHandler(fh)
    cross, cross_wl = ARR[arr]
    rec = {"id": vid, "arr": arr, "cls": job["cls"], "clip": clip, "method": job.get("method")}
    t0 = time.time()
    try:
        res = velocity_flow_subprocess(
            videofile=clip, recipe=fill_recipe(RECIPE, cross, method), cameraconfig=CAM,
            output=os.path.join(out, "output"), prefix="", h_a=None,
            cross=cross, cross_wl=cross_wl, logger=lg,
        )
        rec["returncode"] = getattr(res, "returncode", None)
        for name in ("stdout", "stderr"):
            val = getattr(res, name, None)
            if val:
                val = val.decode(errors="replace") if isinstance(val, bytes) else str(val)
                open(os.path.join(out, f"{name}.txt"), "w").write(val)
    except Exception as e:  # noqa: BLE001
        rec["returncode"] = "exception"
        rec["error"] = repr(e)[:300]
        open(os.path.join(out, "exception.txt"), "w").write(traceback.format_exc())
    rec["seconds"] = round(time.time() - t0, 1)
    ncs = [f for f in sorted(glob.glob(os.path.join(out, "output", "**", "*.nc"), recursive=True))]
    for f in ncs:
        try:
            with _HDF5:
                with xr.open_dataset(f) as ds:
                    ok = "river_flow" in ds or "h_a" in ds
                if ok:
                    rec.update(extract(f))
            if ok:
                break
        except Exception as e:  # noqa: BLE001
            rec["extract_error"] = repr(e)[:200]
    # every line anywhere in this run's text output that mentions water level or S/N
    wl = []
    for f in glob.glob(os.path.join(out, "*.txt")) + glob.glob(os.path.join(out, "*.log")) + \
            glob.glob(os.path.join(out, "output", "**", "*.log"), recursive=True):
        for line in open(f, errors="replace"):
            if "water level" in line.lower() or "signal-to-noise" in line.lower() or "signal to noise" in line.lower():
                wl.append(line.strip()[-220:])
    rec["wl_lines"] = wl[-4:]
    lg.removeHandler(fh)
    fh.close()
    print(json.dumps(rec), flush=True)
    return rec


def main():
    jobs = json.load(open(sys.argv[1]))
    out_root = sys.argv[2]
    workers = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    os.makedirs(out_root, exist_ok=True)
    with open(os.path.join(out_root, "results.jsonl"), "a") as fo, ThreadPoolExecutor(workers) as ex:
        for rec in ex.map(lambda j: run(j, out_root), jobs):
            fo.write(json.dumps(rec) + "\n")
            fo.flush()


if __name__ == "__main__":
    main()
