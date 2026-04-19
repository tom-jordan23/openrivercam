#!/usr/bin/env python3
"""orc_survey_prep — transform SW Maps GeoJSON into ORC-OS survey CSVs.

Takes a SW Maps GeoJSON point export and produces the CSV files needed
for Phase 4 of VIDEO_CONFIG_SETUP.md: GCPs, cross-section, camera
position, water level, plus a metadata.yaml summary.

Label convention (case-insensitive prefix match). The label is
pulled from the first property present out of: remarks, Remarks,
REMARKS, description, Description, name, Name, label, Label (SW
Maps stores the label in the per-point Remarks field, which is
exported into these properties depending on the SW Maps version).

    GCPn        ground control points (GCP1, GCP2, ...)
    XSn / CSn   cross-section points (XS1, XS2, ... in traversal order)
    WLn         water-level edge points
    CAM         camera position (exactly one expected)

No-pole marker:

    Append a trailing '*' to the label (e.g. GCP5*, CAM*) to flag a
    point that was measured WITHOUT the survey pole — the antenna was
    placed directly at the target. The script strips the '*' from the
    output label and skips pole-length subtraction for that point.
    The '*' marker applies uniformly to every label type — there is
    no bucket that is implicitly exempted from pole subtraction.

Transformations:

    - Reproject from --source-crs (default EPSG:4326) to --target-crs
      (default EPSG:32748 = UTM 48S for Java / Bali / Sumatra).
    - Subtract --pole-length from every point's elevation, EXCEPT for
      points flagged with the '*' no-pole marker. This applies to
      GCPs, cross-section stations, water-level points, and the camera
      position alike: the default assumption is that every point was
      measured with the rover pole, and you must explicitly mark
      no-pole points with '*'.

Validation:

    - FAIL if < 4 GCPs, 0 camera positions, 0 cross-section points.
    - WARN if < 8 GCPs, GCP bounding box aspect ratio < 0.2
      (markers look colinear), fewer than 2 water-level points.

Check points:

    - Any feature whose label starts with 'CP' (e.g. CP_START, CP_NOON,
      CP_END) is treated as a check point and excluded from the ORC
      CSVs. The script prints a spread report — horizontal and vertical
      spread across all CP points and pairwise distances between them —
      so you can verify repeatability without doing the math by hand.
      WARNs if spread exceeds 3 cm H / 4 cm V.

Usage:

    orc_survey_prep.py SURVEY.geojson \\
        --site sukabumi \\
        --pole-length 1.80 \\
        --h-ref 12.34

Dependencies:  pip install pyproj
"""

import argparse
import csv
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    from pyproj import Transformer
except ImportError:
    print("ERROR: pyproj not installed. Run: pip install pyproj", file=sys.stderr)
    sys.exit(2)


LABEL_PROPERTIES = (
    "name", "Name", "NAME",
    "label", "Label", "LABEL",
    "remarks", "Remarks", "REMARKS",
    "remark", "Remark", "REMARK",
    "description", "Description", "DESCRIPTION",
)


class Problem(Exception):
    pass


def classify(label: str) -> str:
    """Return one of: gcp, xs, wl, cam, cp, unknown."""
    up = label.strip().upper()
    if up.startswith("GCP"):
        return "gcp"
    if up.startswith("XS") or up.startswith("CS"):
        return "xs"
    if up.startswith("WL"):
        return "wl"
    if up in ("CAM", "CAMERA"):
        return "cam"
    if up.startswith("CP"):
        return "cp"
    return "unknown"


def extract_label(properties: dict) -> str:
    for key in LABEL_PROPERTIES:
        if key in properties and properties[key]:
            return str(properties[key])
    return ""


def sort_key(label: str) -> tuple:
    """Sort GCP10 after GCP2. Strip non-digit prefix, numeric-sort the rest."""
    digits = "".join(c for c in label if c.isdigit())
    return (int(digits) if digits else 0, label)


def load_features(path: Path) -> list:
    with open(path) as f:
        data = json.load(f)
    if data.get("type") != "FeatureCollection":
        raise Problem(f"Expected FeatureCollection, got {data.get('type')}")
    return data.get("features", [])


def bbox_aspect_ratio(points: list) -> float:
    """Return min_side / max_side of the 2D bounding box. 0 if degenerate."""
    if not points:
        return 0.0
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    w = max(xs) - min(xs)
    h = max(ys) - min(ys)
    short, long_ = sorted((w, h))
    return (short / long_) if long_ > 0 else 0.0


# Check-point drift gate, from the survey docs' Success Criteria.
# If horizontal spread > 3 cm or vertical spread > 4 cm across the CP
# readings, something changed during the day (base moved, NTRIP shift,
# atmospheric drift) and the data should be treated with suspicion.
CP_HORIZONTAL_GATE_M = 0.03
CP_VERTICAL_GATE_M = 0.04


def check_point_report(cp_items: list) -> tuple:
    """Analyse variation across CP-prefixed points.

    Returns (report_lines: list[str], warnings: list[str], spread: dict or None).
    `spread` is None when fewer than 2 CP points are present.
    """
    if not cp_items:
        return [], [], None

    labels = [label for label, _ in cp_items]
    lines = [f"CHECK POINTS: {len(cp_items)} point(s) — {', '.join(labels)}"]
    warnings: list = []

    if len(cp_items) < 2:
        lines.append("  Need at least 2 points to compute variation.")
        return lines, warnings, None

    xs = [p[0] for _, p in cp_items]
    ys = [p[1] for _, p in cp_items]
    zs = [p[2] for _, p in cp_items]
    dx = max(xs) - min(xs)
    dy = max(ys) - min(ys)
    spread_h = math.hypot(dx, dy)
    spread_v = max(zs) - min(zs)

    status = (
        "OK"
        if spread_h <= CP_HORIZONTAL_GATE_M and spread_v <= CP_VERTICAL_GATE_M
        else "EXCEEDS GATE"
    )
    lines.append(
        f"  Spread: {spread_h * 100:.1f} cm H, {spread_v * 100:.1f} cm V  "
        f"(gate: ≤{CP_HORIZONTAL_GATE_M * 100:.0f} cm H / "
        f"≤{CP_VERTICAL_GATE_M * 100:.0f} cm V → {status})"
    )

    if status == "EXCEEDS GATE":
        warnings.append(
            f"check-point spread {spread_h * 100:.1f} cm H / "
            f"{spread_v * 100:.1f} cm V exceeds the "
            f"{CP_HORIZONTAL_GATE_M * 100:.0f} cm H / "
            f"{CP_VERTICAL_GATE_M * 100:.0f} cm V gate — investigate "
            f"system stability before trusting the survey"
        )

    lines.append("  Pairwise:")
    width = max(len(label) for label in labels)
    for i in range(len(cp_items)):
        for j in range(i + 1, len(cp_items)):
            la, (xa, ya, za) = cp_items[i]
            lb, (xb, yb, zb) = cp_items[j]
            ph = math.hypot(xa - xb, ya - yb)
            pv = abs(za - zb)
            lines.append(
                f"    {la:<{width}} ↔ {lb:<{width}}: "
                f"{ph * 100:.1f} cm H, {pv * 100:.1f} cm V"
            )

    spread = {
        "horizontal_m": round(spread_h, 4),
        "vertical_m": round(spread_v, 4),
        "gate_status": status,
    }
    return lines, warnings, spread


def write_csv(path: Path, header: list, rows: list) -> None:
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Transform SW Maps GeoJSON into ORC-OS survey CSVs.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument("geojson", type=Path, help="Input GeoJSON file (SW Maps export)")
    ap.add_argument("--site", required=True, help="Site name for metadata (sukabumi, jakarta)")
    ap.add_argument("--pole-length", type=float, required=True,
                    help="Rover pole length in meters (subtracted from GCP & XS z)")
    ap.add_argument("--h-ref", type=float, required=True,
                    help="Water level at calibration-video time, in meters")
    ap.add_argument("--output-dir", type=Path, default=Path.cwd(),
                    help="Where to write CSVs and metadata.yaml (default: cwd)")
    ap.add_argument("--source-crs", default="EPSG:4326",
                    help="Source CRS of GeoJSON (default: EPSG:4326)")
    ap.add_argument("--target-crs", default="EPSG:32748",
                    help="Target CRS for outputs (default: EPSG:32748 = UTM 48S)")
    ap.add_argument("--force", action="store_true",
                    help="Overwrite existing output files")
    args = ap.parse_args()

    # Input-argument sanity (don't fail, just warn on implausible values)
    arg_warnings = []
    if not (0.5 <= args.pole_length <= 4.0):
        arg_warnings.append(
            f"pole-length {args.pole_length} m is outside plausible range "
            f"[0.5, 4.0] — double-check")
    if not (-500.0 <= args.h_ref <= 6000.0):
        arg_warnings.append(
            f"h-ref {args.h_ref} m is outside plausible elevation range "
            f"[-500, 6000] — double-check datum / units")

    # Load features
    try:
        features = load_features(args.geojson)
    except (Problem, json.JSONDecodeError, FileNotFoundError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    # Sanity: feature count
    if not features:
        print("ERROR: GeoJSON contains no features", file=sys.stderr)
        return 1

    # Classify by label. Labels ending in '*' are flagged as no-pole
    # (antenna placed directly on the target — don't subtract pole length).
    # The '*' is stripped before storing; the clean label is used
    # everywhere downstream (sorting, duplicates, output).
    buckets = {"gcp": [], "xs": [], "wl": [], "cam": [], "cp": [], "unknown": []}
    no_pole_labels: set = set()
    skipped = 0
    for feat in features:
        if feat.get("geometry", {}).get("type") != "Point":
            skipped += 1
            continue
        coords = feat["geometry"]["coordinates"]
        if len(coords) < 3:
            print(f"WARN: feature missing elevation: {feat.get('properties', {})}",
                  file=sys.stderr)
            skipped += 1
            continue
        raw_label = extract_label(feat.get("properties", {})).strip()
        if not raw_label:
            print(f"WARN: feature missing name/label/remarks property; skipping {coords}",
                  file=sys.stderr)
            skipped += 1
            continue
        if raw_label.endswith("*"):
            label = raw_label[:-1].rstrip()
            no_pole_labels.add(label)
        else:
            label = raw_label
        kind = classify(label)
        buckets[kind].append((label, coords))

    if buckets["unknown"]:
        print(f"WARN: {len(buckets['unknown'])} feature(s) had unrecognized labels:",
              file=sys.stderr)
        for label, _ in buckets["unknown"]:
            print(f"      - {label}", file=sys.stderr)

    # Sort GCPs and XS by label number
    buckets["gcp"].sort(key=lambda x: sort_key(x[0]))
    buckets["xs"].sort(key=lambda x: sort_key(x[0]))
    buckets["wl"].sort(key=lambda x: sort_key(x[0]))
    buckets["cp"].sort(key=lambda x: x[0])  # alphabetical — CP_END, CP_NOON, CP_START

    # ── Cross-checks: hard fails ───────────────────────────────────
    fails = []

    # Bucket counts
    if len(buckets["gcp"]) < 4:
        fails.append(f"need >= 4 GCPs, got {len(buckets['gcp'])}")
    if len(buckets["cam"]) == 0:
        fails.append("no camera position found (expected label CAM)")
    if len(buckets["cam"]) > 1:
        fails.append(f"multiple camera positions found ({len(buckets['cam'])}); "
                     "expected exactly 1")
    if len(buckets["xs"]) == 0:
        fails.append("no cross-section points found (expected labels XS1, XS2, ...)")

    # Duplicate labels within a bucket (silent data loss if we wrote out)
    for kind in ("gcp", "xs", "wl", "cam", "cp"):
        seen = {}
        for label, coords in buckets[kind]:
            if label in seen:
                fails.append(f"duplicate label {label!r} in {kind.upper()} bucket — "
                             f"rename one before re-running")
            seen[label] = coords

    # Source-CRS bounds check — if EPSG:4326, coords should look like lon/lat.
    # SW Maps sometimes exports with swapped ordering or already-projected coords;
    # catch those before reprojection produces nonsense.
    if args.source_crs.upper() in ("EPSG:4326", "WGS84"):
        for kind in ("gcp", "xs", "wl", "cam", "cp"):
            for label, (lon, lat, _z) in buckets[kind]:
                if not (-180 <= lon <= 180) or not (-90 <= lat <= 90):
                    fails.append(f"{label}: coordinates ({lon}, {lat}) are not valid "
                                 f"lon/lat — is --source-crs correct?")
                    break
            if fails and fails[-1].startswith(kind):
                break

    if fails:
        print("VALIDATION FAILED:", file=sys.stderr)
        for msg in fails:
            print(f"  - {msg}", file=sys.stderr)
        return 1

    # Reproject
    transformer = Transformer.from_crs(args.source_crs, args.target_crs,
                                        always_xy=True)

    def project(label_coords):
        label, (lon, lat, z) = label_coords
        x, y = transformer.transform(lon, lat)
        return label, (x, y, z)

    projected = {k: [project(lc) for lc in buckets[k]]
                 for k in ("gcp", "xs", "wl", "cam", "cp")}

    # Apply pole-length correction to every point, EXCEPT those flagged
    # with the '*' no-pole marker in the source GeoJSON. Pole subtraction
    # is the default for every bucket — GCPs, cross-section stations,
    # water-level points, the camera position, and check points alike.
    # The '*' suffix is the only way to bypass it; no implicit exemptions.
    def subtract_pole(items):
        return [
            (label, (x, y, z if label in no_pole_labels else z - args.pole_length))
            for label, (x, y, z) in items
        ]

    for bucket in ("gcp", "xs", "wl", "cam", "cp"):
        projected[bucket] = subtract_pole(projected[bucket])

    if no_pole_labels:
        all_labels = {
            label
            for bucket in ("gcp", "xs", "wl", "cam", "cp")
            for label, _ in projected[bucket]
        }
        flagged_in_scope = sorted(no_pole_labels & all_labels)
        if flagged_in_scope:
            print(f"INFO: no-pole marker honored for {len(flagged_in_scope)} "
                  f"point(s): {', '.join(flagged_in_scope)}", file=sys.stderr)

    # ── Cross-checks: warnings ─────────────────────────────────────
    warnings = list(arg_warnings)

    # GCP count
    if len(projected["gcp"]) < 8:
        warnings.append(f"only {len(projected['gcp'])} GCPs "
                        f"(recommended >= 8 for a robust pose fit)")

    # GCP spatial spread (aspect ratio)
    gcp_xy = [(x, y) for _, (x, y, _) in projected["gcp"]]
    ar = bbox_aspect_ratio(gcp_xy)
    if ar < 0.2:
        warnings.append(f"GCP bounding box aspect ratio is {ar:.2f} "
                        "(< 0.2 suggests markers are colinear — pose fit may fail)")

    # GCP vertical spread (same-elevation markers give poor pose constraint)
    gcp_z = [z for _, (_, _, z) in projected["gcp"]]
    if gcp_z:
        z_spread = max(gcp_z) - min(gcp_z)
        if z_spread < 0.5:
            warnings.append(f"GCP elevation spread is only {z_spread:.2f} m — "
                            f"markers should cover > 0.5 m vertically for a "
                            f"well-conditioned pose fit")

    # Gap detection in numbered labels — e.g. GCP1, GCP2, GCP4 (missing GCP3)
    def gap_check(items, prefix):
        nums = []
        for label, _ in items:
            digits = "".join(c for c in label if c.isdigit())
            if digits:
                nums.append(int(digits))
        nums = sorted(set(nums))
        if nums and nums != list(range(nums[0], nums[-1] + 1)):
            missing = sorted(set(range(nums[0], nums[-1] + 1)) - set(nums))
            warnings.append(f"{prefix} numbering has gaps: missing {missing} "
                            f"(not fatal, but check you didn't lose a point)")

    gap_check(buckets["gcp"], "GCP")
    gap_check(buckets["xs"], "XS")

    # Coordinate duplicates across all buckets (accidentally measured the same
    # spot twice under different labels)
    all_projected = []
    for kind in ("gcp", "xs", "wl", "cam"):
        for label, (x, y, z) in projected[kind]:
            all_projected.append((label, kind, x, y, z))
    # Round to 10 cm for dup detection (survey noise)
    coord_map = {}
    for label, kind, x, y, z in all_projected:
        key = (round(x, 1), round(y, 1), round(z, 1))
        if key in coord_map:
            other_label, other_kind = coord_map[key]
            warnings.append(f"{kind.upper()}:{label} is within 10 cm of "
                            f"{other_kind.upper()}:{other_label} — "
                            f"likely a duplicate measurement")
        else:
            coord_map[key] = (label, kind)

    # Camera above water surface (sanity — camera should be above h_ref)
    if projected["cam"]:
        _, (_, _, cam_z) = projected["cam"][0]
        if cam_z <= args.h_ref:
            warnings.append(f"camera elevation {cam_z:.2f} m is at or below "
                            f"h_ref {args.h_ref:.2f} m — sign error in datum?")
        elif (cam_z - args.h_ref) < 1.0:
            warnings.append(f"camera is only {cam_z - args.h_ref:.2f} m above "
                            f"water level — check datum / pole-length subtraction")

    # h_ref vs WL points (if present, they should roughly agree)
    if projected["wl"]:
        wl_z = [z for _, (_, _, z) in projected["wl"]]
        wl_mean = sum(wl_z) / len(wl_z)
        if abs(wl_mean - args.h_ref) > 0.5:
            warnings.append(f"h_ref {args.h_ref:.2f} m differs from mean WL "
                            f"elevation {wl_mean:.2f} m by "
                            f"{abs(wl_mean - args.h_ref):.2f} m — verify "
                            f"--h-ref or the WL survey")

    # XS elevation range should bracket h_ref (bed below water, banks above)
    if projected["xs"]:
        xs_z = [z for _, (_, _, z) in projected["xs"]]
        xs_min, xs_max = min(xs_z), max(xs_z)
        if args.h_ref < xs_min:
            warnings.append(f"h_ref {args.h_ref:.2f} m is below XS minimum "
                            f"{xs_min:.2f} m — channel appears to be dry, "
                            f"check datum")
        if args.h_ref > xs_max:
            warnings.append(f"h_ref {args.h_ref:.2f} m is above XS maximum "
                            f"{xs_max:.2f} m — XS probably does not cover "
                            f"the banks; discharge integration will be truncated")

    # WL water-level point count
    if len(projected["wl"]) < 2:
        warnings.append(f"only {len(projected['wl'])} water-level point(s) "
                        "(recommend measuring both banks)")

    # Reprojected-coordinate bounds — for EPSG:32748 (UTM 48S, Indonesia),
    # easting should be ~100k-900k and northing ~9M (southern hemisphere
    # convention: northing decreases going south, so ~9.0M–10.0M is typical
    # for Java). Flag if any point falls way outside.
    if args.target_crs.upper() in ("EPSG:32748",):
        for kind in ("gcp", "xs", "wl", "cam"):
            for label, (x, y, _z) in projected[kind]:
                if not (100_000 <= x <= 900_000):
                    warnings.append(
                        f"{label}: projected easting {x:.0f} is outside the "
                        f"typical UTM-48S range [100k, 900k] — wrong zone?")
                    break
                if not (9_000_000 <= y <= 10_100_000):
                    warnings.append(
                        f"{label}: projected northing {y:.0f} is outside the "
                        f"typical Indonesia range [9.0M, 10.1M] — wrong zone?")
                    break

    # Check-point variation report (printed to stderr; warnings appended to
    # the main warnings list; spread recorded in metadata.yaml below).
    cp_report_lines, cp_warnings, cp_spread = check_point_report(projected["cp"])
    if cp_report_lines:
        print("\n" + "\n".join(cp_report_lines), file=sys.stderr)
    warnings.extend(cp_warnings)

    # Prepare output
    args.output_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "gcps.csv": ("gcp", ["id", "x", "y", "z"], True),
        "cross_section.csv": ("xs", ["x", "y", "z"], False),
        "camera_position.csv": ("cam", ["x", "y", "z"], False),
        "water_level.csv": ("wl", ["x", "y", "z"], False),
    }
    for filename, (kind, header, include_id) in outputs.items():
        path = args.output_dir / filename
        if path.exists() and not args.force:
            print(f"ERROR: {path} exists (use --force to overwrite)", file=sys.stderr)
            return 1

    for filename, (kind, header, include_id) in outputs.items():
        rows = []
        for label, (x, y, z) in projected[kind]:
            if include_id:
                rows.append([label, f"{x:.4f}", f"{y:.4f}", f"{z:.4f}"])
            else:
                rows.append([f"{x:.4f}", f"{y:.4f}", f"{z:.4f}"])
        path = args.output_dir / filename
        if not rows and kind == "wl":
            # Skip empty water-level file rather than write a headers-only file
            continue
        write_csv(path, header, rows)
        print(f"wrote {path}  ({len(rows)} row(s))")

    # Write metadata.yaml (hand-rolled — avoid adding PyYAML as a dep)
    meta_path = args.output_dir / "metadata.yaml"
    with open(meta_path, "w") as f:
        f.write(f"site: {args.site}\n")
        f.write(f"processed_at: {datetime.now(timezone.utc).isoformat()}\n")
        f.write(f"source_geojson: {args.geojson.name}\n")
        f.write(f"h_ref: {args.h_ref}\n")
        f.write(f"pole_length: {args.pole_length}\n")
        f.write(f"source_crs: {args.source_crs}\n")
        f.write(f"target_crs: {args.target_crs}\n")
        f.write("counts:\n")
        f.write(f"  gcps: {len(projected['gcp'])}\n")
        f.write(f"  cross_section: {len(projected['xs'])}\n")
        f.write(f"  water_level: {len(projected['wl'])}\n")
        f.write(f"  camera: {len(projected['cam'])}\n")
        f.write(f"  check_points: {len(projected['cp'])}\n")
        if cp_spread is not None:
            f.write("check_point_spread:\n")
            f.write(f"  horizontal_m: {cp_spread['horizontal_m']}\n")
            f.write(f"  vertical_m: {cp_spread['vertical_m']}\n")
            f.write(f"  gate_status: {cp_spread['gate_status']}\n")
        if warnings:
            f.write("warnings:\n")
            for w in warnings:
                f.write(f"  - {w!r}\n")
    print(f"wrote {meta_path}")

    # Print warnings to stderr at the end so they're visible
    if warnings:
        print("\nWARNINGS:", file=sys.stderr)
        for w in warnings:
            print(f"  - {w}", file=sys.stderr)

    print(f"\nNext: upload gcps.csv, cross_section.csv, and the calibration")
    print(f"      video to ORC-OS (Phase 4 in VIDEO_CONFIG_SETUP.md).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
