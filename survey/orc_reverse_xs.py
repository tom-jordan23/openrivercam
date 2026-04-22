#!/usr/bin/env python3
"""orc_reverse_xs — reverse the point order of a cross-section GeoJSON,
preserving provenance.

ORC-OS reads a cross-section as a left-bank-to-right-bank polyline and
uses that orientation to sign the velocity component normal to the
section. If the surveyed polyline was captured right-bank-first, the
resulting velocimetry will show flow pointing the wrong way relative
to the true downstream direction, and the discharge sign will be
inverted.

This script reverses the order of the `features` array in a
cross-section GeoJSON and writes a new file with a `provenance_chain`
entry recording the operation, the input SHA-256, and the --reason.

Optionally also emits a flat `x,y,z` CSV alongside the output
(via --csv-out), so the handoff directory's CSV companion stays in
sync with the reversed GeoJSON. The CSV is derived purely from the
reversed GeoJSON's feature coordinates — no separate reversal.

Usage:

    orc_reverse_xs.py cross_section.geojson \\
        --reason "PIV quiver at 2026-04-23 showed flow vectors opposing \\
            the true downstream direction; reversing XS point order to \\
            correct bank orientation. See corrections.md 2026-04-23." \\
        -o cross_section_reversed.geojson \\
        --csv-out cross_section_reversed.csv

Fails on:
    - Input file missing, not a FeatureCollection, or has no features
    - --reason empty
    - Output file exists and --force not given
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


GENERATOR_NAME = "orc_reverse_xs.py"
GENERATOR_VERSION = "1.0"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def feature_xyz(feat: dict) -> tuple:
    """Extract (x, y, z) from a Feature, preferring properties, falling
    back to geometry.coordinates. Returns (x, y, z) or raises KeyError.
    """
    props = feat.get("properties") or {}
    if all(k in props for k in ("x", "y", "z")):
        return float(props["x"]), float(props["y"]), float(props["z"])
    geom = feat.get("geometry") or {}
    coords = geom.get("coordinates") or []
    if len(coords) >= 3:
        return float(coords[0]), float(coords[1]), float(coords[2])
    raise KeyError("feature has no x/y/z properties and no 3D geometry")


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Reverse the point order of a cross-section GeoJSON.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument("geojson", type=Path, help="Input cross-section GeoJSON")
    ap.add_argument("--reason", required=True,
                    help="Free-text justification — should reference the "
                         "corrections.md entry that documents this fix")
    ap.add_argument("-o", "--output", type=Path, required=True,
                    help="Output GeoJSON path")
    ap.add_argument("--csv-out", type=Path, default=None,
                    help="Optional: also emit a flat x,y,z CSV at this path, "
                         "derived from the reversed GeoJSON's feature coords")
    ap.add_argument("--force", action="store_true",
                    help="Overwrite output file(s) if they exist")
    ap.add_argument("--indent", type=int, default=2,
                    help="JSON indent for output (default: 2; 0 for compact)")
    args = ap.parse_args()

    if not args.reason.strip():
        print("ERROR: --reason must not be empty", file=sys.stderr)
        return 1

    for out_path in (args.output, args.csv_out):
        if out_path is not None and out_path.exists() and not args.force:
            print(f"ERROR: {out_path} exists (use --force to overwrite)",
                  file=sys.stderr)
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
        print(f"ERROR: {args.geojson} contains no features", file=sys.stderr)
        return 1

    input_sha = sha256_file(args.geojson)
    n = len(features)

    reversed_features = list(reversed(features))
    # Reassign sequential string ids to match the new order so downstream
    # readers that trust feature.id get a clean 0..n-1 sequence. The
    # original ids are recorded in the provenance entry so the mapping
    # is auditable.
    id_map = []
    for new_idx, feat in enumerate(reversed_features):
        prior_id = feat.get("id")
        id_map.append({"new_id": str(new_idx), "prior_id": prior_id})
        feat["id"] = str(new_idx)

    data["features"] = reversed_features

    existing_meta = data.get("metadata") or {}
    prior_chain = list(existing_meta.get("provenance_chain") or [])
    provenance_entry = {
        "generator": GENERATOR_NAME,
        "generator_version": GENERATOR_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "operation": "reverse_cross_section",
        "reason": args.reason.strip(),
        "inputs": [
            {
                "role": "source_geojson",
                "path": str(args.geojson),
                "name": args.geojson.name,
                "sha256": input_sha,
            },
        ],
        "feature_count": n,
        "id_reassignment": id_map,
    }
    data["metadata"] = {
        **existing_meta,
        "provenance_chain": prior_chain + [provenance_entry],
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w") as f:
        if args.indent and args.indent > 0:
            json.dump(data, f, indent=args.indent)
        else:
            json.dump(data, f, separators=(",", ":"))
        f.write("\n")

    csv_msg = ""
    if args.csv_out is not None:
        args.csv_out.parent.mkdir(parents=True, exist_ok=True)
        with open(args.csv_out, "w") as f:
            f.write("x,y,z\n")
            for feat in reversed_features:
                x, y, z = feature_xyz(feat)
                f.write(f"{x:.4f},{y:.4f},{z:.4f}\n")
        csv_msg = f"\nwrote {args.csv_out}  ({n} row(s); derived from reversed GeoJSON)"

    print(f"wrote {args.output}  ({n} feature(s) reversed)")
    print(f"  input SHA-256:  {input_sha}")
    print(f"  output SHA-256: {sha256_file(args.output)}")
    if csv_msg:
        print(csv_msg)
        print(f"  csv SHA-256:    {sha256_file(args.csv_out)}")
    print(f"\nReason recorded: {args.reason.strip()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
