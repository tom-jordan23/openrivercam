#!/usr/bin/env python3
"""orc_apply_pole_lengths — apply per-point pole-length corrections to a survey GeoJSON.

When a single survey mixes multiple pole lengths (e.g. the standard rover
pole for most points and a bamboo pole extension for points in deep
water), passing a single --pole-length to orc_survey_prep.py is not
sufficient. This script reads a CSV that maps each point's REMARKS
label to its individual pole length, subtracts that length from the
GeoJSON elevations, and emits a new GeoJSON.

Every REMARKS label in the output gets a trailing '*' appended — the
no-pole marker recognised by orc_survey_prep.py. This tells the
downstream script that pole-length subtraction has already been applied
and it should not subtract again. Run orc_survey_prep.py on the output
with any --pole-length value; the '*' markers will skip subtraction
universally.

CSV format (header row required):

    Station,Pole_Len_Cm,Comment
    CP_start,129
    HREF,93,Water level was at 27cm on the pole
    GCP1,120
    GCP2,242,bamboo pole
    ...

    - Station:     label matching the GeoJSON REMARKS (case-insensitive)
    - Pole_Len_Cm: pole length in centimeters (float or int)
    - Comment:     optional free-text column (ignored)

Matching is case-insensitive and tolerant of a trailing '*' on either
side — so GCP5 in the CSV matches GCP5* in the GeoJSON, and vice versa.
Whitespace around cells is stripped.

Usage:

    orc_apply_pole_lengths.py survey.geojson pole_lengths.csv \\
        -o survey_adjusted.geojson

    # Then feed the adjusted file to orc_survey_prep.py. --pole-length
    # is required by that script but is ignored here because every label
    # carries the '*' no-pole marker:
    orc_survey_prep.py survey_adjusted.geojson \\
        --site sukabumi --pole-length 0
"""

import argparse
import csv
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


GENERATOR_NAME = "orc_apply_pole_lengths.py"
GENERATOR_VERSION = "1.0"


def sha256_file(path: Path) -> str:
    """Return the hex SHA-256 of a file, read in 64 KiB chunks."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


LABEL_PROPERTIES = (
    "name", "Name", "NAME",
    "label", "Label", "LABEL",
    "remarks", "Remarks", "REMARKS",
    "remark", "Remark", "REMARK",
    "description", "Description", "DESCRIPTION",
)


def normalise(label: str) -> str:
    """Case-fold and strip a trailing '*' for lookup-key comparison."""
    s = label.strip()
    if s.endswith("*"):
        s = s[:-1].rstrip()
    return s.upper()


def find_label_property(properties: dict) -> tuple:
    """Return (key, value) of the first label property present, or (None, '')."""
    for key in LABEL_PROPERTIES:
        if key in properties and properties[key]:
            return key, str(properties[key])
    return None, ""


def load_pole_lengths(csv_path: Path) -> dict:
    """Parse the pole-length CSV into {normalised_station: pole_length_m}.

    Fails on: missing required columns, duplicate stations, blank or
    non-numeric pole length. Implausible values (outside 0.3-5.0 m) are
    warned about but not rejected.
    """
    required = {"station", "pole_len_cm"}
    mapping: dict = {}
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError(f"{csv_path} has no header row")
        header_map = {h.strip().lower(): h for h in reader.fieldnames if h}
        missing = required - set(header_map)
        if missing:
            raise ValueError(
                f"{csv_path} missing required column(s): "
                f"{', '.join(sorted(missing))}. "
                f"Found: {reader.fieldnames}"
            )
        station_col = header_map["station"]
        length_col = header_map["pole_len_cm"]
        for row_num, row in enumerate(reader, start=2):
            station_raw = (row.get(station_col) or "").strip()
            length_raw = (row.get(length_col) or "").strip()
            if not station_raw and not length_raw:
                continue  # tolerate blank rows
            if not station_raw:
                raise ValueError(
                    f"{csv_path}:{row_num} has pole length but no Station"
                )
            if not length_raw:
                raise ValueError(
                    f"{csv_path}:{row_num} station {station_raw!r} has blank "
                    f"Pole_Len_Cm"
                )
            try:
                cm = float(length_raw)
            except ValueError:
                raise ValueError(
                    f"{csv_path}:{row_num} station {station_raw!r} has "
                    f"non-numeric Pole_Len_Cm {length_raw!r}"
                )
            key = normalise(station_raw)
            if key in mapping:
                raise ValueError(
                    f"{csv_path}:{row_num} duplicate Station {station_raw!r}"
                )
            mapping[key] = (station_raw, cm / 100.0)
    if not mapping:
        raise ValueError(f"{csv_path} contains no data rows")
    return mapping


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Apply per-point pole-length corrections to a survey GeoJSON.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument("geojson", type=Path, help="Input GeoJSON (SW Maps export)")
    ap.add_argument("csv", type=Path, help="Pole-length CSV")
    ap.add_argument("-o", "--output", type=Path, required=True,
                    help="Output GeoJSON path")
    ap.add_argument("--force", action="store_true",
                    help="Overwrite output file if it exists")
    ap.add_argument("--strict", action="store_true",
                    help="Error out if any CSV station has no matching "
                         "GeoJSON feature (default: warn)")
    ap.add_argument("--indent", type=int, default=2,
                    help="JSON indent for output (default: 2; use 0 for compact)")
    args = ap.parse_args()

    if args.output.exists() and not args.force:
        print(f"ERROR: {args.output} exists (use --force to overwrite)",
              file=sys.stderr)
        return 1

    try:
        mapping = load_pole_lengths(args.csv)
    except (ValueError, FileNotFoundError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    # Plausibility check on pole lengths (warn, don't reject)
    for key, (station, pole_m) in mapping.items():
        if not (0.3 <= pole_m <= 5.0):
            print(f"WARN: {station!r} pole length {pole_m:.2f} m is outside "
                  f"the plausible range [0.3, 5.0] — check units (CSV is in cm)",
                  file=sys.stderr)

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

    features = data.get("features", [])
    if not features:
        print(f"ERROR: {args.geojson} contains no features", file=sys.stderr)
        return 1

    matched_keys: set = set()
    errors: list = []
    updates: list = []  # (label, pole_m, old_z, new_z) for the summary

    for idx, feat in enumerate(features):
        geom = feat.get("geometry") or {}
        if geom.get("type") != "Point":
            errors.append(f"feature #{idx}: not a Point geometry")
            continue
        coords = geom.get("coordinates") or []
        if len(coords) < 3:
            errors.append(f"feature #{idx}: missing elevation (need 3 coords)")
            continue
        props = feat.get("properties") or {}
        label_key, raw_label = find_label_property(props)
        if not raw_label:
            errors.append(f"feature #{idx}: no label/remarks/name property")
            continue
        clean_label = raw_label.rstrip("*").strip()
        norm = normalise(raw_label)
        if norm not in mapping:
            errors.append(
                f"feature #{idx} ({clean_label!r}): no matching Station in "
                f"{args.csv.name}"
            )
            continue
        station, pole_m = mapping[norm]
        matched_keys.add(norm)
        old_z = float(coords[2])
        # Round to 4 decimals (0.1 mm) to avoid float representation
        # artifacts like 622.6510000000001 in the output. Survey
        # precision is mm at best, so this loses no real information.
        new_z = round(old_z - pole_m, 4)
        # Update coordinates in-place (preserve lon/lat precision)
        coords[2] = new_z
        # Append '*' no-pole marker to the label so downstream
        # orc_survey_prep.py skips pole subtraction. Don't double up
        # if the input already had '*'.
        if not raw_label.rstrip().endswith("*"):
            props[label_key] = clean_label + "*"
        updates.append((clean_label, pole_m, old_z, new_z))

    if errors:
        print("ERROR: could not process all features:", file=sys.stderr)
        for msg in errors:
            print(f"  - {msg}", file=sys.stderr)
        return 1

    unused = sorted(set(mapping) - matched_keys)
    if unused:
        msg = (f"{len(unused)} CSV station(s) had no matching GeoJSON "
               f"feature: {', '.join(mapping[k][0] for k in unused)}")
        if args.strict:
            print(f"ERROR: {msg}", file=sys.stderr)
            return 1
        print(f"WARN: {msg}", file=sys.stderr)

    # Build the provenance block. RFC 7946 permits foreign members on
    # the top-level FeatureCollection object, and orc_survey_prep.py only
    # reads `type` and `features`, so this round-trips cleanly. If a
    # prior `metadata.provenance_chain` already exists (e.g. when this
    # script is run on an output from another transform script), the new
    # entry is appended so the full lineage is preserved.
    existing_meta = data.get("metadata") or {}
    prior_chain = list(existing_meta.get("provenance_chain") or [])
    provenance_entry = {
        "generator": GENERATOR_NAME,
        "generator_version": GENERATOR_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "operation": "pole_length_correction",
        "inputs": [
            {
                "role": "source_geojson",
                "path": str(args.geojson),
                "name": args.geojson.name,
                "sha256": sha256_file(args.geojson),
            },
            {
                "role": "pole_length_csv",
                "path": str(args.csv),
                "name": args.csv.name,
                "sha256": sha256_file(args.csv),
            },
        ],
        "transformations": [
            {
                "label": label,
                "pole_length_m": round(pole_m, 4),
                "z_before_m": round(old_z, 4),
                "z_after_m": round(new_z, 4),
                "delta_m": round(new_z - old_z, 4),
            }
            for label, pole_m, old_z, new_z in updates
        ],
    }
    if unused:
        provenance_entry["unused_csv_stations"] = [mapping[k][0] for k in unused]
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

    # Summary
    print(f"wrote {args.output}  ({len(updates)} point(s) adjusted)")
    width = max(len(label) for label, *_ in updates)
    for label, pole_m, old_z, new_z in updates:
        print(f"  {label:<{width}}  pole {pole_m:.2f} m   "
              f"z {old_z:.3f} → {new_z:.3f} m")
    print("\nNext: run orc_survey_prep.py on the adjusted GeoJSON. "
          "Any --pole-length\n      value will be ignored because every "
          "label now carries the '*' marker.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
