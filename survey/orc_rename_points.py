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

Duplicate source labels (OLD@INDEX):

    When the same label appears more than once in a GeoJSON (e.g. a
    rover operator re-occupied a point under its original name instead
    of a suffixed name), a plain --rename OLD=NEW is ambiguous and the
    script will refuse to run. Use an inline index disambiguator to
    target a specific occurrence:

        --rename GCP3@1=GCP3.2

    The index is 0-based over the order the features appear in the
    input GeoJSON. --rename GCP3@0=... targets the first GCP3, @1 the
    second, and so on. The chosen index is recorded in the provenance
    chain so a later reader can tell which duplicate was renamed.

Fails on:

    - OLD label not found in the GeoJSON
    - OLD matches more than one feature and no @INDEX was given
    - OLD@INDEX out of range for the number of matches
    - NEW label already exists on a feature that is not being renamed
      away (would create a duplicate)
    - Two --rename flags with the same OLD[@INDEX] (conflict)
    - Two --rename flags writing to the same NEW (conflict)
    - --reason is empty

Audit trail:

    The output GeoJSON gets a new entry appended to its top-level
    `metadata.provenance_chain` array, recording the generator, input
    SHA-256, the renames applied (including each match_index when one
    was used), and the --reason string. The reason should reference
    the matching entry in the corrections.md log so a reader can trace
    why the rename happened, not just that it did.
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


GENERATOR_NAME = "orc_rename_points.py"
GENERATOR_VERSION = "1.1"


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
    """Parse 'OLD[@INDEX]=NEW' into (old, new, match_index).

    match_index is None when no @INDEX suffix was given, otherwise a
    non-negative int picking which occurrence of OLD to rename.
    """
    if "=" not in arg:
        raise argparse.ArgumentTypeError(
            f"--rename must be OLD[@INDEX]=NEW, got {arg!r}"
        )
    old_raw, new = arg.split("=", 1)
    old_raw, new = old_raw.strip(), new.strip()

    match_index = None
    if "@" in old_raw:
        old, idx_str = old_raw.rsplit("@", 1)
        old, idx_str = old.strip(), idx_str.strip()
        try:
            match_index = int(idx_str)
        except ValueError:
            raise argparse.ArgumentTypeError(
                f"--rename {arg!r}: @INDEX must be an integer, got {idx_str!r}"
            )
        if match_index < 0:
            raise argparse.ArgumentTypeError(
                f"--rename {arg!r}: @INDEX must be ≥ 0 (0-based)"
            )
    else:
        old = old_raw

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
    return old, new, match_index


def _format_rename_key(old: str, match_index) -> str:
    return f"{old}@{match_index}" if match_index is not None else old


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Rename labelled points in a survey GeoJSON.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument("geojson", type=Path, help="Input GeoJSON")
    ap.add_argument("--rename", action="append", required=True,
                    type=parse_rename_arg, metavar="OLD[@INDEX]=NEW",
                    help="Rename OLD label to NEW. Optional @INDEX "
                         "(0-based) disambiguates when OLD appears more "
                         "than once. May be repeated.")
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

    # Preserve order; allow multiple --rename with the same OLD if they
    # use different @INDEX values (e.g. GCP3@0=A and GCP3@1=B).
    renames_list: list = []
    seen_keys: dict = {}
    for old, new, match_index in args.rename:
        key = (old.upper(), match_index)
        if key in seen_keys:
            prev_new = seen_keys[key]
            print(f"ERROR: --rename {_format_rename_key(old, match_index)!r} "
                  f"specified twice (to {prev_new!r} and {new!r})",
                  file=sys.stderr)
            return 1
        seen_keys[key] = new
        renames_list.append((old, new, match_index))

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

    # Index every label (clean form) → list of (feature_idx, clean_label),
    # in file order. Supports duplicate labels; order of occurrence is
    # the index space the @INDEX syntax refers to.
    label_index: dict = {}
    for idx, feat in enumerate(features):
        props = feat.get("properties") or {}
        _, raw = find_label_property(props)
        if not raw:
            continue
        clean, _ = strip_marker(raw)
        label_index.setdefault(clean.upper(), []).append((idx, clean))

    errors: list = []

    # Resolve each rename to a single feature index. Record resolution so
    # the apply pass and the NEW-collision pass don't have to redo it.
    # Entries are (feat_idx, old, new, match_index) or None on error.
    resolved: list = []
    for old, new, match_index in renames_list:
        old_upper = old.upper()
        matches = label_index.get(old_upper, [])
        if not matches:
            errors.append(
                f"--rename: OLD {old_upper!r} not found in {args.geojson.name}"
            )
            resolved.append(None)
            continue
        if match_index is None:
            if len(matches) > 1:
                labels = [lbl for _, lbl in matches]
                errors.append(
                    f"--rename: OLD {old_upper!r} matches {len(matches)} "
                    f"features ({labels}) — ambiguous; add @INDEX (0-based) "
                    f"to disambiguate, e.g. --rename {old}@0={new}"
                )
                resolved.append(None)
                continue
            feat_idx = matches[0][0]
        else:
            if match_index >= len(matches):
                errors.append(
                    f"--rename: OLD {old_upper!r}@{match_index} out of range "
                    f"({len(matches)} match(es) found; valid indexes are "
                    f"0..{len(matches) - 1})"
                )
                resolved.append(None)
                continue
            feat_idx = matches[match_index][0]
        resolved.append((feat_idx, old, new, match_index))

    # Feature indexes being renamed away (keyed by OLD upper). Used to
    # decide whether a NEW collision is actually resolved by another
    # rename vacating the label.
    touched_by_old: dict = {}
    for entry in resolved:
        if entry is None:
            continue
        feat_idx, old, _, _ = entry
        touched_by_old.setdefault(old.upper(), set()).add(feat_idx)

    # NEW collision check: a NEW target collides if some feature already
    # has that label and is NOT being renamed away.
    for entry in resolved:
        if entry is None:
            continue
        _, _, new, _ = entry
        new_upper = new.upper()
        existing = label_index.get(new_upper, [])
        if not existing:
            continue
        untouched = [
            (fidx, lbl) for fidx, lbl in existing
            if fidx not in touched_by_old.get(new_upper, set())
        ]
        if untouched:
            untouched_labels = [lbl for _, lbl in untouched]
            errors.append(
                f"--rename: NEW {new!r} already exists in {args.geojson.name} "
                f"({untouched_labels}) — would create a duplicate"
            )

    # Detect two renames writing to the same NEW (regardless of OLD).
    new_targets: dict = {}
    for entry in resolved:
        if entry is None:
            continue
        _, old, new, match_index = entry
        new_upper = new.upper()
        if new_upper in new_targets:
            prev = new_targets[new_upper]
            errors.append(
                f"--rename: two renames write to NEW {new!r} "
                f"(from {prev!r} and {_format_rename_key(old, match_index)!r})"
            )
        new_targets[new_upper] = _format_rename_key(old, match_index)

    if errors:
        print("ERROR: rename validation failed:", file=sys.stderr)
        for msg in errors:
            print(f"  - {msg}", file=sys.stderr)
        return 1

    # Apply: per-feature rename map avoids any label-based collisions
    # during traversal when duplicate labels are in play.
    per_feature_rename: dict = {}
    for entry in resolved:
        feat_idx, _, new, match_index = entry
        per_feature_rename[feat_idx] = (new, match_index)

    applied: list = []
    for idx, feat in enumerate(features):
        if idx not in per_feature_rename:
            continue
        props = feat.get("properties") or {}
        key, raw = find_label_property(props)
        if not raw:
            continue
        clean, had_star = strip_marker(raw)
        new, match_index = per_feature_rename[idx]
        new_label = new + ("*" if had_star else "")
        props[key] = new_label
        rename_record = {
            "from": clean + ("*" if had_star else ""),
            "to": new_label,
        }
        if match_index is not None:
            rename_record["match_index"] = match_index
        applied.append(rename_record)

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
        suffix = f" [@{rename['match_index']}]" if "match_index" in rename else ""
        print(f"  {rename['from']}{suffix} → {rename['to']}")
    print(f"\nReason recorded: {args.reason.strip()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
