#!/usr/bin/env python3
"""orc_geojson_to_kml — convert a survey GeoJSON to a KML overlay.

Reads a survey GeoJSON and produces a KML file for visual inspection
in Google Earth, Google My Maps, or any KML-capable viewer. Points are
auto-coloured by label category so misclassifications stand out:

    GCP*       — yellow pin
    XS*, CS*   — blue pin
    CP*        — red pin (usually flags potential issues)
    CAM        — pink pin
    WL*, HREF  — light-blue pin
    other      — white pin

Each placemark's name is the label; its description shows lon, lat, z,
and any non-trivial properties from the GeoJSON feature. Pins are
pinned to the ground surface by default (--absolute-altitude flips to
the absolute z value, which is usually misleading because Google Earth
terrain data is imprecise at this scale).

Usage:

    orc_geojson_to_kml.py survey.geojson -o survey.kml
"""

import argparse
import html
import json
import sys
from pathlib import Path


LABEL_PROPERTIES = (
    "name", "Name", "NAME",
    "label", "Label", "LABEL",
    "remarks", "Remarks", "REMARKS",
    "remark", "Remark", "REMARK",
    "description", "Description", "DESCRIPTION",
)


CATEGORIES = [
    # (match-fn taking UPPER, style id, pin colour name)
    (lambda s: s.startswith("GCP"),                                 "gcp",   "ylw"),
    (lambda s: s.startswith("XS") or s.startswith("CS"),            "xs",    "blu"),
    (lambda s: s.startswith("CP"),                                  "cp",    "red"),
    (lambda s: s in ("CAM", "CAMERA"),                              "cam",   "pink"),
    (lambda s: s.startswith("WL") or s == "HREF",                   "wl",    "ltblu"),
]


def classify(label: str) -> tuple:
    clean = label.strip().rstrip("*").strip().upper()
    for matcher, cat, colour in CATEGORIES:
        if matcher(clean):
            return cat, colour
    return "other", "wht"


def extract_label(props: dict) -> str:
    for key in LABEL_PROPERTIES:
        if key in props and props[key]:
            return str(props[key])
    return ""


def style_block(cat: str, colour: str) -> str:
    url = f"http://maps.google.com/mapfiles/kml/pushpin/{colour}-pushpin.png"
    return f"""  <Style id="{cat}">
    <IconStyle>
      <scale>1.1</scale>
      <Icon><href>{url}</href></Icon>
    </IconStyle>
    <LabelStyle><scale>0.9</scale></LabelStyle>
  </Style>"""


def placemark(label: str, cat: str, lon: float, lat: float, z: float,
              extra_props: dict, clamp: bool) -> str:
    rows = [
        f"<b>lon</b>: {lon:.9f}",
        f"<b>lat</b>: {lat:.9f}",
        f"<b>z</b>: {z:.4f} m",
    ]
    for k, v in sorted(extra_props.items()):
        if v is None or v == "":
            continue
        if isinstance(v, (dict, list)):
            v = json.dumps(v, separators=(",", ":"))
        rows.append(f"<b>{html.escape(str(k))}</b>: {html.escape(str(v))}")
    desc = "<br/>".join(rows)
    altmode = "clampToGround" if clamp else "absolute"
    return f"""  <Placemark>
    <name>{html.escape(label)}</name>
    <styleUrl>#{cat}</styleUrl>
    <description><![CDATA[{desc}]]></description>
    <Point>
      <altitudeMode>{altmode}</altitudeMode>
      <coordinates>{lon:.9f},{lat:.9f},{z:.4f}</coordinates>
    </Point>
  </Placemark>"""


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Convert a survey GeoJSON to a KML overlay.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument("geojson", type=Path, help="Input GeoJSON")
    ap.add_argument("-o", "--output", type=Path, required=True,
                    help="Output KML path")
    ap.add_argument("--force", action="store_true",
                    help="Overwrite output if it exists")
    ap.add_argument("--absolute-altitude", action="store_true",
                    help="Place pins at their z values (default clamps to "
                         "the ground surface, which is usually what you "
                         "want for relative-position inspection)")
    ap.add_argument("--name", default=None,
                    help="Top-level <name> for the KML document "
                         "(default: input filename stem)")
    args = ap.parse_args()

    if args.output.exists() and not args.force:
        print(f"ERROR: {args.output} exists (--force to overwrite)",
              file=sys.stderr)
        return 1

    try:
        with open(args.geojson) as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"ERROR: {args.geojson}: {e}", file=sys.stderr)
        return 1

    features = data.get("features") or []
    if not features:
        print(f"ERROR: {args.geojson} has no features", file=sys.stderr)
        return 1

    # Collect unique categories actually used so we only emit styles we need
    used_cats: dict = {}
    placemarks: list = []
    counts: dict = {}
    clamp = not args.absolute_altitude

    for feat in features:
        if (feat.get("geometry") or {}).get("type") != "Point":
            continue
        coords = feat["geometry"].get("coordinates") or []
        if len(coords) < 3:
            continue
        lon, lat, z = coords[0], coords[1], coords[2]
        props = feat.get("properties") or {}
        label = extract_label(props) or "(unlabelled)"
        cat, colour = classify(label)
        used_cats[cat] = colour
        counts[cat] = counts.get(cat, 0) + 1
        # Extra props = everything except the label field
        extras = {k: v for k, v in props.items()
                  if k not in LABEL_PROPERTIES}
        placemarks.append(
            placemark(label, cat, lon, lat, z, extras, clamp)
        )

    if not placemarks:
        print(f"ERROR: no Point features in {args.geojson}", file=sys.stderr)
        return 1

    doc_name = args.name or args.geojson.stem
    # Doc description surfaces the provenance chain if present so the
    # user can see which script stages shaped the file they're viewing.
    meta = data.get("metadata") or {}
    chain = meta.get("provenance_chain") or []
    if chain:
        chain_lines = [
            f"{i}: {e.get('operation', '?')} ({e.get('generator', '?')} "
            f"@ {e.get('generated_at', '?')})"
            for i, e in enumerate(chain)
        ]
        doc_desc = ("Provenance chain (" + str(len(chain)) + " entries):<br/>"
                    + "<br/>".join(html.escape(l) for l in chain_lines))
    else:
        doc_desc = "No provenance_chain — likely the raw source GeoJSON."

    styles = "\n".join(style_block(c, col) for c, col in used_cats.items())
    body = "\n".join(placemarks)
    kml = f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
  <name>{html.escape(doc_name)}</name>
  <description><![CDATA[{doc_desc}]]></description>
{styles}
{body}
</Document>
</kml>
"""

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w") as f:
        f.write(kml)

    print(f"wrote {args.output}")
    for cat in sorted(counts):
        print(f"  {cat:<6} {counts[cat]:>3} point(s)")
    print(f"\nOpen in Google Earth: double-click the .kml file")
    print(f"Google My Maps: Create new map → Import → upload this .kml")
    return 0


if __name__ == "__main__":
    sys.exit(main())
