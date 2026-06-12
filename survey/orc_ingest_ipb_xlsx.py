#!/usr/bin/env python3
"""orc_ingest_ipb_xlsx — turn the IPB total-station deliverable into
provenance-stamped GeoJSON for ORC-OS.

The IPB Bogor re-survey of Sukabumi was delivered as an Excel workbook
(`RIVER CROSS SECTION - OPEN RIVER CAM - SUKABUMI (1).xlsx`) whose single
`data` sheet already carries coordinates in UTM Zone 48S (EPSG:32748).
This is a different shape from the SW Maps GeoJSON that
``orc_survey_prep.py`` consumes:

  * coordinates are ALREADY projected (no reprojection step),
  * there are TWO cross-sections (Upstream + Downstream) rather than one,
  * the control points are a separate block of rows.

The sheet layout (1-based rows):

    row 1            banner "Zone UTM 48 S"
    row 2            header: No | X-UTM | Y-UTM | Elevation | Code |
                     Description | Segment (m) | Distance From River
                     Left Bank (m) | Elevation (m, rel. to XS thalweg)
    rows 3..15       Upstream cross-section   (Code "Upstream-1..13")
    rows 16..29      Downstream cross-section (Code "Downstream-1..14")
    rows 30..48      Ground control points    (Code "1..19")

Outputs (all EPSG:32748, all with a provenance_chain that pins the
SHA-256 of the source workbook):

    ipb_upstream_xs.geojson      Upstream transect, ordered LB->RB by chainage
    ipb_downstream_xs.geojson    Downstream transect, ordered LB->RB by chainage
    ipb_gcp_candidates.geojson   All 19 control points
    ipb_survey.geojson           Everything, each feature tagged with `role`

NB on datum: IPB's absolute georeferencing is tied to a single
handheld-GPS fix at station S1 (whole-metre accuracy) plus a backsight
bearing, so the ABSOLUTE easting/northing/elevation is only good to a
metre or so. The total-station RELATIVE geometry (what drives the camera
calibration and the discharge integration) is millimetre-consistent
because a rigid transform preserves it. Do NOT mix these coordinates with
the prior RTK survey's frame, and do NOT carry over the salvage
z_0/h_ref = 617.065 — that value lives on the old datum.

Which transect becomes the ORC discharge cross_section and which becomes
the optical-water-level cross_section_wl is decided at fit time by
projecting both into the camera frame (the WL line is the one on the
white/yellow painted left-bank wall). This script stays agnostic and
emits both by their survey names.

Dependencies:  pip install openpyxl
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import openpyxl
except ImportError:
    print("ERROR: openpyxl not installed. Run: pip install openpyxl", file=sys.stderr)
    sys.exit(2)

GENERATOR = "orc_ingest_ipb_xlsx.py"
GENERATOR_VERSION = "1.0"
EPSG = 32748


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def fnum(v):
    """Coerce a cell to float, tolerating strings and blanks."""
    if v is None or v == "":
        return None
    return float(str(v).strip())


def parse_sheet(ws):
    """Return (upstream, downstream, gcps) lists of dicts.

    Each dict: {no, x, y, z, code, desc, chainage, rel_z}.
    Classification is by the Description column, which the surveyor
    filled consistently ("Upstream Cross Section", "Downstream Cross
    Section", "Ground Control Point").
    """
    upstream, downstream, gcps = [], [], []
    for r in ws.iter_rows(min_row=3, values_only=True):
        no = r[0]
        x, y, z = fnum(r[1]), fnum(r[2]), fnum(r[3])
        code = "" if r[4] is None else str(r[4]).strip()
        desc = "" if r[5] is None else str(r[5]).strip()
        chainage = fnum(r[7]) if len(r) > 7 else None
        rel_z = fnum(r[8]) if len(r) > 8 else None
        if x is None or y is None or z is None:
            continue
        rec = dict(no=no, x=x, y=y, z=z, code=code, desc=desc,
                   chainage=chainage, rel_z=rel_z)
        d = desc.lower()
        if d.startswith("upstream"):
            upstream.append(rec)
        elif d.startswith("downstream"):
            downstream.append(rec)
        elif d.startswith("ground control"):
            gcps.append(rec)
        else:
            raise ValueError(f"Unclassifiable row No={no} desc={desc!r}")
    return upstream, downstream, gcps


def provenance_entry(src_path: Path, src_sha: str, operation: str, note: str):
    return {
        "generator": GENERATOR,
        "generator_version": GENERATOR_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "operation": operation,
        "note": note,
        "inputs": [
            {"role": "ipb_workbook", "name": src_path.name, "sha256": src_sha}
        ],
    }


def feature(idx, rec, extra_props=None):
    props = {"x": rec["x"], "y": rec["y"], "z": rec["z"]}
    if extra_props:
        props.update(extra_props)
    return {
        "id": str(idx),
        "type": "Feature",
        "properties": props,
        "geometry": {"type": "Point", "coordinates": [rec["x"], rec["y"], rec["z"]]},
    }


def collection(name, prov, features):
    return {
        "type": "FeatureCollection",
        "name": name,
        "crs": {"type": "name", "properties": {"name": f"urn:ogc:def:crs:EPSG::{EPSG}"}},
        "metadata": {"provenance_chain": [prov]},
        "features": features,
    }


def write_json(path: Path, obj):
    with open(path, "w") as f:
        json.dump(obj, f, indent=2)
    print(f"  wrote {path.name} ({len(obj['features'])} features)")


def water_surface_estimate(xs):
    """Rough survey-time stage from a transect: take the two lowest
    bank/edge break points either side of the thalweg. Reported only as
    a sanity estimate — the production z_0/h_ref must be tied to the
    calibration-video stage, not assumed from the survey.
    """
    zs = sorted(r["z"] for r in xs)
    z_min = zs[0]
    # edge points cluster a little above the thalweg; report the band
    edges = [z for z in zs if z - z_min < 1.8]
    return z_min, (sum(edges) / len(edges) if edges else None)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("xlsx", type=Path, help="IPB RIVER CROSS SECTION workbook")
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--sheet", default="data")
    args = ap.parse_args()

    if not args.xlsx.exists():
        print(f"ERROR: {args.xlsx} not found", file=sys.stderr)
        return 2
    args.out_dir.mkdir(parents=True, exist_ok=True)

    src_sha = sha256(args.xlsx)
    wb = openpyxl.load_workbook(args.xlsx, data_only=True)
    ws = wb[args.sheet]
    upstream, downstream, gcps = parse_sheet(ws)

    # Order each transect LB->RB by the surveyor's chainage column.
    upstream.sort(key=lambda r: (r["chainage"] if r["chainage"] is not None else 0))
    downstream.sort(key=lambda r: (r["chainage"] if r["chainage"] is not None else 0))

    note = ("IPB total-station deliverable, already in UTM 48S. Relative "
            "geometry mm-consistent; absolute datum tied to a handheld-GPS "
            "fix at S1 (~metre). Do not merge with the prior RTK frame.")
    prov = provenance_entry(args.xlsx, src_sha, "ipb_xlsx_to_geojson", note)

    write_json(args.out_dir / "ipb_upstream_xs.geojson",
               collection("ipb_upstream_xs", prov,
                          [feature(i, r, {"code": r["code"], "chainage": r["chainage"]})
                           for i, r in enumerate(upstream)]))
    write_json(args.out_dir / "ipb_downstream_xs.geojson",
               collection("ipb_downstream_xs", prov,
                          [feature(i, r, {"code": r["code"], "chainage": r["chainage"]})
                           for i, r in enumerate(downstream)]))
    write_json(args.out_dir / "ipb_gcp_candidates.geojson",
               collection("ipb_gcp_candidates", prov,
                          [feature(i, r, {"gcp_code": r["code"]})
                           for i, r in enumerate(gcps)]))

    all_feats = []
    idx = 0
    for role, group in (("upstream_xs", upstream), ("downstream_xs", downstream),
                        ("gcp_candidate", gcps)):
        for r in group:
            all_feats.append(feature(idx, r, {"role": role, "code": r["code"],
                                              "chainage": r["chainage"]}))
            idx += 1
    write_json(args.out_dir / "ipb_survey.geojson",
               collection("ipb_survey", prov, all_feats))

    # ---- summary to stdout -------------------------------------------------
    def span(xs):
        xmin = min(r["x"] for r in xs); xmax = max(r["x"] for r in xs)
        ymin = min(r["y"] for r in xs); ymax = max(r["y"] for r in xs)
        width = ((xmax - xmin) ** 2 + (ymax - ymin) ** 2) ** 0.5
        zmin = min(r["z"] for r in xs); zmax = max(r["z"] for r in xs)
        return width, zmin, zmax

    print(f"\nSource SHA-256: {src_sha}")
    print(f"Upstream XS:   {len(upstream)} pts, "
          f"width {span(upstream)[0]:.2f} m, z {span(upstream)[1]:.3f}..{span(upstream)[2]:.3f}")
    print(f"Downstream XS: {len(downstream)} pts, "
          f"width {span(downstream)[0]:.2f} m, z {span(downstream)[1]:.3f}..{span(downstream)[2]:.3f}")
    print(f"GCP candidates: {len(gcps)} pts, "
          f"z {min(r['z'] for r in gcps):.3f}..{max(r['z'] for r in gcps):.3f}")
    for name, xs in (("upstream", upstream), ("downstream", downstream)):
        z_min, edge = water_surface_estimate(xs)
        print(f"  {name}: thalweg z_min={z_min:.3f}, edge-band mean~{edge:.3f} "
              f"(survey-time stage estimate, NOT production z_0)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
