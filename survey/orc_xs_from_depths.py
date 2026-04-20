#!/usr/bin/env python3
"""orc_xs_from_depths — interpolate bed points along a cross-section tape.

Wading surveys record water depths at fixed intervals along a tape
strung between two bank-anchor points. This script consumes the depth
table and anchor coordinates plus a water-surface elevation, and emits
a GeoJSON with new Point features placed along the straight line
between the anchors, each carrying a bed elevation derived from its
measured depth.

By default the anchor-end feature is also renamed so the final cross
section sorts correctly in orc_survey_prep.py: anchor-start keeps its
label, the new depth points fill consecutive numbers after it, and
the anchor-end is renumbered to the slot after the last bed point.
This yields a spatially ordered XS<n>..XS<n+m+1> sequence ready for
ORC's cross-section input. Pass --no-renumber-end to suppress the
rename if you want to do it yourself with orc_rename_points.py.

Every generated bed point gets a trailing '*' on its REMARKS label —
the no-pole marker from orc_survey_prep.py — because the elevation was
computed directly from depth and water-surface, not measured via a
rover pole. orc_apply_pole_lengths.py and orc_survey_prep.py will
therefore skip pole subtraction for these points.

CSV format (header required):

    anchor_pt,displacement_cm,depth_cm,comment
    XS1,20,10
    XS1,40,34
    ...

    - anchor_pt:       label matching --anchor-start (repeated each row)
    - displacement_cm: distance along the tape from anchor-start, in cm
    - depth_cm:        water depth at that station, in cm
    - comment:         optional free-text (preserved on the output feature)

Usage:

    orc_xs_from_depths.py survey_adjusted.geojson xs_depths.csv \\
        --anchor-start XS1 --anchor-end XS2 \\
        --water-surface-z 617.335 \\
        -o survey_with_bed.geojson

Water surface:

    --water-surface-z is required. It must be in the same datum / units
    as the GeoJSON's z values. For the Sukabumi 2026 survey, HREF was
    placed with a 0.93 m pole and the water level was 0.27 m up the
    pole, giving a water surface of (HREF_raw - 0.93 + 0.27) =
    617.335 m. Document this derivation in corrections.md if the value
    is not obvious from the inputs alone.

Dependencies:  pip install pyproj
"""

import argparse
import csv
import hashlib
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


GENERATOR_NAME = "orc_xs_from_depths.py"
GENERATOR_VERSION = "1.0"


LABEL_PROPERTIES = (
    "name", "Name", "NAME",
    "label", "Label", "LABEL",
    "remarks", "Remarks", "REMARKS",
    "remark", "Remark", "REMARK",
    "description", "Description", "DESCRIPTION",
)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def strip_marker(label: str) -> tuple:
    s = label.strip()
    if s.endswith("*"):
        return s[:-1].rstrip(), True
    return s, False


def find_label_property(properties: dict) -> tuple:
    for key in LABEL_PROPERTIES:
        if key in properties and properties[key]:
            return key, str(properties[key])
    return None, ""


def label_digits(label: str) -> int:
    """Pull the integer suffix out of a label. Returns 0 if none found."""
    d = "".join(c for c in label if c.isdigit())
    return int(d) if d else 0


def load_depths(csv_path: Path) -> list:
    """Parse the xs_depths CSV. Returns rows in displacement order.

    Required columns: anchor_pt, displacement_cm, depth_cm. Optional: comment.
    Fails on: missing column, blank required field, non-numeric number,
    negative value, duplicate (anchor, displacement).
    """
    required = {"anchor_pt", "displacement_cm", "depth_cm"}
    rows: list = []
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError(f"{csv_path} has no header row")
        header_map = {h.strip().lower(): h for h in reader.fieldnames if h}
        missing = required - set(header_map)
        if missing:
            raise ValueError(
                f"{csv_path} missing required column(s): "
                f"{', '.join(sorted(missing))}. Found: {reader.fieldnames}"
            )
        ap_col = header_map["anchor_pt"]
        disp_col = header_map["displacement_cm"]
        depth_col = header_map["depth_cm"]
        comment_col = header_map.get("comment")
        for row_num, row in enumerate(reader, start=2):
            anchor = (row.get(ap_col) or "").strip()
            disp_raw = (row.get(disp_col) or "").strip()
            depth_raw = (row.get(depth_col) or "").strip()
            if not any([anchor, disp_raw, depth_raw]):
                continue
            if not anchor:
                raise ValueError(f"{csv_path}:{row_num} missing anchor_pt")
            if not disp_raw:
                raise ValueError(
                    f"{csv_path}:{row_num} blank displacement_cm"
                )
            if not depth_raw:
                raise ValueError(
                    f"{csv_path}:{row_num} blank depth_cm"
                )
            try:
                disp = float(disp_raw)
            except ValueError:
                raise ValueError(
                    f"{csv_path}:{row_num} non-numeric displacement_cm "
                    f"{disp_raw!r}"
                )
            try:
                depth = float(depth_raw)
            except ValueError:
                raise ValueError(
                    f"{csv_path}:{row_num} non-numeric depth_cm {depth_raw!r}"
                )
            if disp < 0:
                raise ValueError(
                    f"{csv_path}:{row_num} negative displacement_cm {disp}"
                )
            if depth < 0:
                raise ValueError(
                    f"{csv_path}:{row_num} negative depth_cm {depth}"
                )
            comment = ""
            if comment_col:
                comment = (row.get(comment_col) or "").strip()
            rows.append({
                "row_num": row_num,
                "anchor": anchor,
                "displacement_cm": disp,
                "depth_cm": depth,
                "comment": comment,
            })
    if not rows:
        raise ValueError(f"{csv_path} has no data rows")
    # Duplicate (anchor, displacement) detection
    seen: dict = {}
    for r in rows:
        key = (r["anchor"].upper(), r["displacement_cm"])
        if key in seen:
            raise ValueError(
                f"{csv_path}:{r['row_num']} duplicate "
                f"(anchor_pt={r['anchor']}, displacement_cm={r['displacement_cm']}) "
                f"— also in row {seen[key]}"
            )
        seen[key] = r["row_num"]
    rows.sort(key=lambda r: r["displacement_cm"])
    return rows


def find_feature(features: list, label: str) -> tuple:
    """Return (idx, feature, label_prop_key, clean_label, had_star) or all-None."""
    target = label.strip().upper().rstrip("*").rstrip()
    for idx, feat in enumerate(features):
        if (feat.get("geometry") or {}).get("type") != "Point":
            continue
        props = feat.get("properties") or {}
        key, raw = find_label_property(props)
        if not raw:
            continue
        clean, had_star = strip_marker(raw)
        if clean.upper() == target:
            return idx, feat, key, clean, had_star
    return None, None, None, None, None


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Interpolate bed points along a cross-section tape.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument("geojson", type=Path, help="Input GeoJSON (with anchor points)")
    ap.add_argument("depths_csv", type=Path, help="xs_depths CSV")
    ap.add_argument("--anchor-start", required=True,
                    help="Label of the starting anchor (displacement=0 side)")
    ap.add_argument("--anchor-end", required=True,
                    help="Label of the ending anchor (far end of the tape)")
    ap.add_argument("--water-surface-z", type=float, required=True,
                    help="Water surface elevation in meters, in the same "
                         "datum/units as the GeoJSON z values")
    ap.add_argument("-o", "--output", type=Path, required=True,
                    help="Output GeoJSON path")
    ap.add_argument("--force", action="store_true",
                    help="Overwrite output if it exists")
    ap.add_argument("--label-prefix", default="XS",
                    help="Prefix for generated bed-point labels (default: XS)")
    ap.add_argument("--no-renumber-end", action="store_true",
                    help="Do not rename the anchor-end; caller will fix the "
                         "sort order separately")
    ap.add_argument("--metric-crs", default="EPSG:32748",
                    help="Metric CRS used for distance math "
                         "(default: EPSG:32748 = UTM 48S)")
    ap.add_argument("--source-crs", default="EPSG:4326",
                    help="Source CRS of GeoJSON coordinates (default: EPSG:4326)")
    ap.add_argument("--indent", type=int, default=2,
                    help="JSON indent for output (default: 2; 0 for compact)")
    args = ap.parse_args()

    if args.output.exists() and not args.force:
        print(f"ERROR: {args.output} exists (use --force to overwrite)",
              file=sys.stderr)
        return 1

    if args.anchor_start.upper() == args.anchor_end.upper():
        print("ERROR: --anchor-start and --anchor-end must differ",
              file=sys.stderr)
        return 1

    try:
        depths = load_depths(args.depths_csv)
    except (ValueError, FileNotFoundError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    anchors_in_csv = {r["anchor"].upper() for r in depths}
    if anchors_in_csv != {args.anchor_start.upper()}:
        print(f"ERROR: CSV anchor_pt column holds {sorted(anchors_in_csv)}; "
              f"every row must reference --anchor-start "
              f"({args.anchor_start!r})", file=sys.stderr)
        return 1

    try:
        with open(args.geojson) as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"ERROR: {args.geojson}: {e}", file=sys.stderr)
        return 1

    if data.get("type") != "FeatureCollection":
        print(f"ERROR: expected FeatureCollection, got {data.get('type')!r}",
              file=sys.stderr)
        return 1

    features = data.get("features") or []
    if not features:
        print(f"ERROR: {args.geojson} has no features", file=sys.stderr)
        return 1

    _, start_feat, start_key, start_clean, start_star = find_feature(
        features, args.anchor_start)
    _, end_feat, end_key, end_clean, end_star = find_feature(
        features, args.anchor_end)

    if start_feat is None:
        print(f"ERROR: anchor-start {args.anchor_start!r} not found in "
              f"{args.geojson.name}", file=sys.stderr)
        return 1
    if end_feat is None:
        print(f"ERROR: anchor-end {args.anchor_end!r} not found in "
              f"{args.geojson.name}", file=sys.stderr)
        return 1

    start_coords = start_feat["geometry"]["coordinates"]
    end_coords = end_feat["geometry"]["coordinates"]
    if len(start_coords) < 3 or len(end_coords) < 3:
        print("ERROR: anchor features missing elevation", file=sys.stderr)
        return 1

    # Plausibility: water-surface-z shouldn't wildly disagree with the
    # anchor z values (same datum). Banks are usually 0.1-10 m above water.
    anchor_z_avg = (start_coords[2] + end_coords[2]) / 2.0
    dz = anchor_z_avg - args.water_surface_z
    ws_warnings: list = []
    if abs(dz) > 20.0:
        ws_warnings.append(
            f"water_surface_z {args.water_surface_z:.2f} m differs from "
            f"mean anchor z {anchor_z_avg:.2f} m by {dz:.2f} m — datum or "
            f"unit mismatch?"
        )
    elif dz < -0.5:
        ws_warnings.append(
            f"water_surface_z {args.water_surface_z:.2f} m is above mean "
            f"anchor z {anchor_z_avg:.2f} m — anchors should be on the "
            f"banks, above the water surface"
        )

    # Project to metric CRS for distance math
    to_metric = Transformer.from_crs(args.source_crs, args.metric_crs,
                                     always_xy=True)
    from_metric = Transformer.from_crs(args.metric_crs, args.source_crs,
                                       always_xy=True)
    sx, sy = to_metric.transform(start_coords[0], start_coords[1])
    ex, ey = to_metric.transform(end_coords[0], end_coords[1])
    dx, dy = ex - sx, ey - sy
    line_length_m = math.hypot(dx, dy)
    if line_length_m < 0.01:
        print(f"ERROR: anchor points are only {line_length_m * 100:.1f} cm "
              f"apart — pick different anchors", file=sys.stderr)
        return 1
    ux, uy = dx / line_length_m, dy / line_length_m

    disp_warnings: list = []
    max_disp_m = depths[-1]["displacement_cm"] / 100.0
    if max_disp_m > line_length_m + 0.10:
        disp_warnings.append(
            f"max displacement {max_disp_m * 100:.1f} cm exceeds "
            f"anchor-to-anchor length {line_length_m * 100:.1f} cm by "
            f"> 10 cm — bed points will extend past anchor-end"
        )

    # Plan labels and check for collisions
    existing_labels: set = set()
    for feat in features:
        props = feat.get("properties") or {}
        _, raw = find_label_property(props)
        if raw:
            clean, _ = strip_marker(raw)
            existing_labels.add(clean.upper())

    start_num = label_digits(start_clean)
    bed_labels = [
        f"{args.label_prefix}{start_num + i + 1}"
        for i in range(len(depths))
    ]
    new_end_label = None
    if not args.no_renumber_end:
        new_end_label = f"{args.label_prefix}{start_num + len(depths) + 1}"

    # The anchor-end label is "reserved" for us when we're about to rename
    # it away — treat it as free when checking for bed-point collisions.
    available_existing = set(existing_labels)
    if not args.no_renumber_end:
        available_existing.discard(end_clean.upper())

    bed_collisions = [
        l for l in bed_labels if l.upper() in available_existing
    ]
    if bed_collisions:
        print("ERROR: proposed bed-point labels collide with existing "
              "features in the GeoJSON:", file=sys.stderr)
        for l in bed_collisions:
            print(f"  - {l}", file=sys.stderr)
        print("Rename the conflicting features first with "
              "orc_rename_points.py, then re-run.", file=sys.stderr)
        return 1

    if new_end_label and new_end_label.upper() in available_existing:
        print(f"ERROR: proposed anchor-end new label {new_end_label!r} "
              f"collides with an existing feature. Rename the conflicting "
              f"feature first, or use --no-renumber-end.", file=sys.stderr)
        return 1

    # Rename anchor-end BEFORE generating bed points so the label isn't
    # briefly duplicated.
    rename_record = None
    if new_end_label is not None:
        end_new_full = new_end_label + ("*" if end_star else "")
        end_feat["properties"][end_key] = end_new_full
        rename_record = {
            "from": end_clean + ("*" if end_star else ""),
            "to": end_new_full,
        }

    # Generate bed features
    new_features: list = []
    derived_entries: list = []
    for r, label in zip(depths, bed_labels):
        disp_m = r["displacement_cm"] / 100.0
        px = sx + ux * disp_m
        py = sy + uy * disp_m
        lon, lat = from_metric.transform(px, py)
        bed_z = round(args.water_surface_z - r["depth_cm"] / 100.0, 4)
        full_label = label + "*"
        props = {
            "REMARKS": full_label,
            "source": {
                "generator": GENERATOR_NAME,
                "csv_row": r["row_num"],
                "anchor_pt": r["anchor"],
                "displacement_cm": r["displacement_cm"],
                "depth_cm": r["depth_cm"],
            },
        }
        if r["comment"]:
            props["comment"] = r["comment"]
        new_features.append({
            "type": "Feature",
            "properties": props,
            "geometry": {
                "type": "Point",
                "coordinates": [lon, lat, bed_z],
            },
        })
        derived_entries.append({
            "label": full_label,
            "source_csv_row": r["row_num"],
            "displacement_cm": r["displacement_cm"],
            "depth_cm": r["depth_cm"],
            "bed_z_m": bed_z,
            "lon": round(lon, 9),
            "lat": round(lat, 9),
            "comment": r["comment"] or None,
        })

    data["features"] = features + new_features

    # Provenance entry
    existing_meta = data.get("metadata") or {}
    prior_chain = list(existing_meta.get("provenance_chain") or [])
    entry = {
        "generator": GENERATOR_NAME,
        "generator_version": GENERATOR_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "operation": "xs_depth_extrapolation",
        "inputs": [
            {
                "role": "source_geojson",
                "path": str(args.geojson),
                "name": args.geojson.name,
                "sha256": sha256_file(args.geojson),
            },
            {
                "role": "depths_csv",
                "path": str(args.depths_csv),
                "name": args.depths_csv.name,
                "sha256": sha256_file(args.depths_csv),
            },
        ],
        "parameters": {
            "anchor_start": start_clean,
            "anchor_end": end_clean,
            "water_surface_z_m": args.water_surface_z,
            "source_crs": args.source_crs,
            "metric_crs": args.metric_crs,
            "label_prefix": args.label_prefix,
            "anchor_line_length_m": round(line_length_m, 4),
        },
        "derived_points": derived_entries,
    }
    if rename_record:
        entry["anchor_end_rename"] = rename_record
    warnings = ws_warnings + disp_warnings
    if warnings:
        entry["warnings"] = warnings
    data["metadata"] = {
        **existing_meta,
        "provenance_chain": prior_chain + [entry],
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w") as f:
        if args.indent and args.indent > 0:
            json.dump(data, f, indent=args.indent)
        else:
            json.dump(data, f, separators=(",", ":"))
        f.write("\n")

    print(f"wrote {args.output}  ({len(new_features)} bed point(s) added)")
    print(f"anchor line: {start_clean} → {end_clean}   "
          f"length {line_length_m:.3f} m")
    if rename_record:
        print(f"anchor-end renamed: {rename_record['from']} → "
              f"{rename_record['to']}")
    print()
    print(f"{'label':<10} {'disp (cm)':>9} {'depth (cm)':>10} "
          f"{'bed z (m)':>10}")
    for dp in derived_entries:
        print(f"{dp['label']:<10} {dp['displacement_cm']:>9.0f} "
              f"{dp['depth_cm']:>10.0f} {dp['bed_z_m']:>10.3f}")

    if warnings:
        print("\nWARNINGS:", file=sys.stderr)
        for w in warnings:
            print(f"  - {w}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
