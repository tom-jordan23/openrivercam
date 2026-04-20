#!/usr/bin/env python3
"""orc_rename_points — rename labelled points in a survey GeoJSON, preserving provenance.

Field surveys occasionally produce mislabelled points (e.g. the rover
operator selects the wrong prefix in SW Maps, so GCP2 is recorded as
CP2). This script rewrites one or more REMARKS labels in a GeoJSON,
producing a new file and appending a provenance entry so the audit
trail back to the raw source is preserved.

Usage:

    orc_rename_points.py survey.geojson \\
        --rename CP2=GCP2 \\
        --reason "CP2 was a survey typo for GCP2; see corrections.md 2026-04-20" \\
        -o survey_corrected.geojson

Multiple --rename flags may be passed. Matching is case-insensitive and
tolerates a trailing '*' no-pole marker on either side — the '*' status
of the original feature is preserved on the renamed output. All other
feature properties are left untouched.

Fails on:

    - OLD label not found in the GeoJSON
    - OLD matches more than one feature (ambiguous — GeoJSON should
      have unique labels)
    - NEW label already exists as a different feature (would create a
      duplicate)
    - Two --rename flags that share the same OLD (conflict)
    - --reason is empty

Audit trail:

    The output GeoJSON gets a new entry appended to its top-level
    `metadata.provenance_chain` array, recording the generator, input
    SHA-256, the renames applied, and the --reason string. The reason
    should reference the matching entry in the corrections.md log so a
    reader can trace why the rename happened, not just that it did.
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


GENERATOR_NAME = "orc_rename_points.py"
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
    """Split a label into (clean, had_star_marker)."""
    s = label.strip()
    if s.endswith("*"):
        return s[:-1].rstrip(), True
    return s, False


def find_label_property(properties: dict) -> tuple:
    for key in LABEL_PROPERTIES:
        if key in properties and properties[key]:
            return key, str(properties[key])
    return None, ""


def parse_rename_arg(arg: str) -> tuple:
    """Parse 'OLD=NEW' into (old, new). Whitespace is stripped."""
    if "=" not in arg:
        raise argparse.ArgumentTypeError(
            f"--rename must be OLD=NEW, got {arg!r}"
        )
    old, new = arg.split("=", 1)
    old, new = old.strip(), new.strip()
    if not old or not new:
        raise argparse.ArgumentTypeError(
            f"--rename OLD and NEW must both be non-empty, got {arg!r}"
        )
    if old.endswith("*") or new.endswith("*"):
        raise argparse.ArgumentTypeError(
            f"--rename {arg!r}: do not include the '*' no-pole marker "
            "in OLD or NEW — it is preserved automatically from the "
            "original feature"
        )
    return old, new


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Rename labelled points in a survey GeoJSON.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument("geojson", type=Path, help="Input GeoJSON")
    ap.add_argument("--rename", action="append", required=True,
                    type=parse_rename_arg, metavar="OLD=NEW",
                    help="Rename OLD label to NEW. May be repeated.")
    ap.add_argument("--reason", required=True,
                    help="Free-text justification — should reference the "
                         "corrections.md entry that documents this fix")
    ap.add_argument("-o", "--output", type=Path, required=True,
                    help="Output GeoJSON path")
    ap.add_argument("--force", action="store_true",
                    help="Overwrite output file if it exists")
    ap.add_argument("--indent", type=int, default=2,
                    help="JSON indent for output (default: 2; use 0 for compact)")
    args = ap.parse_args()

    if not args.reason.strip():
        print("ERROR: --reason must not be empty", file=sys.stderr)
        return 1

    if args.output.exists() and not args.force:
        print(f"ERROR: {args.output} exists (use --force to overwrite)",
              file=sys.stderr)
        return 1

    # Build rename map, detecting conflicting --rename args
    renames: dict = {}
    for old, new in args.rename:
        key = old.upper()
        if key in renames:
            print(f"ERROR: --rename {old!r} specified twice "
                  f"(to {renames[key]!r} and {new!r})", file=sys.stderr)
            return 1
        renames[key] = new

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

    # First pass: index every label (clean form) to detect duplicates
    # and to validate that NEW targets don't already exist.
    label_index: dict = {}
    for idx, feat in enumerate(features):
        props = feat.get("properties") or {}
        _, raw = find_label_property(props)
        if not raw:
            continue
        clean, _ = strip_marker(raw)
        label_index.setdefault(clean.upper(), []).append((idx, clean))

    # Validate: each OLD must match exactly one feature
    errors: list = []
    for old_upper, new in renames.items():
        matches = label_index.get(old_upper, [])
        if not matches:
            errors.append(f"--rename: OLD {old_upper!r} not found in {args.geojson.name}")
        elif len(matches) > 1:
            labels = [lbl for _, lbl in matches]
            errors.append(
                f"--rename: OLD {old_upper!r} matches {len(matches)} features "
                f"({labels}) — ambiguous"
            )

    # Validate: NEW must not collide with an existing label that is not
    # itself being renamed away. In other words, renaming A→B is fine if
    # either B doesn't exist, or B is being renamed away to something else.
    for old_upper, new in renames.items():
        new_upper = new.upper()
        if new_upper in label_index and new_upper not in renames:
            existing_labels = [lbl for _, lbl in label_index[new_upper]]
            errors.append(
                f"--rename: NEW {new!r} already exists in {args.geojson.name} "
                f"({existing_labels}) — would create a duplicate"
            )

    # Detect two renames writing to the same NEW
    new_targets: dict = {}
    for old_upper, new in renames.items():
        new_upper = new.upper()
        if new_upper in new_targets:
            errors.append(
                f"--rename: two renames write to NEW {new!r} "
                f"(from {new_targets[new_upper]!r} and {old_upper!r})"
            )
        new_targets[new_upper] = old_upper

    if errors:
        print("ERROR: rename validation failed:", file=sys.stderr)
        for msg in errors:
            print(f"  - {msg}", file=sys.stderr)
        return 1

    # Apply renames. Preserve the '*' marker status of the original.
    applied: list = []
    for feat in features:
        props = feat.get("properties") or {}
        key, raw = find_label_property(props)
        if not raw:
            continue
        clean, had_star = strip_marker(raw)
        new = renames.get(clean.upper())
        if new is None:
            continue
        new_label = new + ("*" if had_star else "")
        props[key] = new_label
        applied.append({
            "from": clean + ("*" if had_star else ""),
            "to": new_label,
        })

    # Build provenance entry and append to chain
    existing_meta = data.get("metadata") or {}
    prior_chain = list(existing_meta.get("provenance_chain") or [])
    provenance_entry = {
        "generator": GENERATOR_NAME,
        "generator_version": GENERATOR_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "operation": "rename_labels",
        "reason": args.reason.strip(),
        "inputs": [
            {
                "role": "source_geojson",
                "path": str(args.geojson),
                "name": args.geojson.name,
                "sha256": sha256_file(args.geojson),
            },
        ],
        "renames": applied,
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

    print(f"wrote {args.output}  ({len(applied)} label(s) renamed)")
    for rename in applied:
        print(f"  {rename['from']} → {rename['to']}")
    print(f"\nReason recorded: {args.reason.strip()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
