# orc_survey_prep.py — Reference

Helper script that turns a raw SW Maps GeoJSON export into the CSV
files ORC-OS needs to author a video configuration. It replaces the
older manual QGIS workflow documented in `SURVEY_DATA_PROCESSING.md`.

The script is a small, predictable step between two larger procedures:

1. **Survey procedure** (`SURVEY_PROCESS_v3_base.md` or
   `SURVEY_PROCESS_v3_ntrip.md`) — produces the GeoJSON.
2. **Video configuration procedure**
   (`../spring_2026_ID/docs/VIDEO_CONFIG_SETUP.md`, Phase 4) — runs
   this script as one step of a longer workflow.

This document is the reference for the script in isolation: inputs,
arguments, outputs, validation rules, and common errors. For the
field workflow, follow the survey and video-config docs.

---

## What the script does

Given a SW Maps GeoJSON export, the script:

1. Reads every point feature and classifies it by the label prefix.
2. Reprojects coordinates from the source CRS (default WGS84 lat/lon)
   to the target CRS (default UTM 48S, covering Java / Bali /
   Sumatra).
3. Subtracts the rover pole length from every elevation — except
   points explicitly flagged with a `*` no-pole marker.
4. Runs a set of cross-checks (hard fails and warnings) on the data.
5. Writes the ORC-OS CSV files, a metadata sidecar, and a
   check-point drift report.

---

## Quick start

```bash
# Install dependency once per laptop
pip install pyproj

# Typical invocation
python3 survey/orc_survey_prep.py survey_20260417.geojson \
    --site sukabumi \
    --pole-length 1.80 \
    --output-dir ./calibration/
```

This produces five files in `./calibration/`:

| File | Contents |
|------|----------|
| `gcps.csv` | Ground control points with labels |
| `cross_section.csv` | Cross-section points in traversal order |
| `camera_position.csv` | Single camera position |
| `water_level.csv` | Water-level edge points (omitted if none) |
| `metadata.yaml` | Session record — `h_ref`, pole length, counts, warnings |

---

## Input: GeoJSON label convention

SW Maps stores the per-feature label in the **Remarks** field on the
handheld. On export, the label travels into the feature properties
as one of `name`, `label`, `remarks`, `remark`, or `description`
(case-insensitive; SW Maps' behavior depends on version). The script
reads the first property it finds and classifies the point by its
label prefix.

| Prefix | Meaning | Example labels |
|--------|---------|----------------|
| `GCP` | Ground control point | `GCP1`, `GCP2`, … |
| `XS` or `CS` | Cross-section point (traversal order matters) | `XS1`, `XS2`, …, `CS1` |
| `WL` | Water-level edge point | `WL1`, `WL2` |
| `CAM` or `CAMERA` | Camera position (exactly one expected) | `CAM` |
| `CP` | Check point (repeatability — not written to ORC CSVs) | `CP_START`, `CP_NOON`, `CP_END` |

Labels are sorted numerically where it matters — `GCP10` comes after
`GCP2`, not after `GCP1`.

### No-pole marker (`*`)

Append a trailing `*` to a label to flag a point that was measured
**without** the survey pole (the antenna was placed directly on the
target):

```
GCP5*
CAM*
```

The `*` is stripped from the output label, and pole-length
subtraction is skipped for that point. The marker applies
uniformly — no category is implicitly exempt from pole subtraction.

---

## CLI arguments

| Argument | Required | Default | Notes |
|----------|----------|---------|-------|
| `geojson` | yes | — | Input file (positional) |
| `--site` | yes | — | Site name for metadata (`sukabumi`, `jakarta`, …) |
| `--pole-length` | yes | — | Rover pole length in meters. Subtracted from every point elevation except those flagged `*`. |
| `--h-ref` | no | mean of WL points | Water-surface elevation at the time of the calibration video. Recorded in `metadata.yaml` and used by ORC-OS as the reference datum. |
| `--output-dir` | no | current directory | Where CSVs and `metadata.yaml` are written |
| `--source-crs` | no | `EPSG:4326` | CRS of the GeoJSON. Override only if your export is already projected. |
| `--target-crs` | no | `EPSG:32748` (UTM 48S) | CRS for output CSVs. Use `EPSG:32749` for UTM 49S (east Indonesia) or another code for non-Indonesia sites. |
| `--force` | no | off | Overwrite existing output files |

### Notes on `--h-ref`

- Omit it when the water-level (`WL*`) points were surveyed at — or
  very near — the time of the calibration video. The script
  averages the pole-adjusted `WL` elevations and records
  `h_ref_source: derived-from-wl-mean` in `metadata.yaml`.
- Supply it explicitly only when the calibration video was captured
  at a different stage than the WL survey. The script warns if a
  user-supplied `--h-ref` differs from the WL mean by more than
  0.5 m.
- If `--h-ref` is omitted and the GeoJSON contains no `WL` points,
  the script fails — there is no other sensible fallback.

---

## Outputs

### CSV schemas

| File | Columns |
|------|---------|
| `gcps.csv` | `id`, `x`, `y`, `z` |
| `cross_section.csv` | `x`, `y`, `z` |
| `camera_position.csv` | `x`, `y`, `z` |
| `water_level.csv` | `x`, `y`, `z` |

Coordinates are in the target CRS, in meters, to four decimal
places. Elevations are already pole-adjusted.

`water_level.csv` is omitted if no `WL` points are present — the
script does not write a headers-only file.

### metadata.yaml

```yaml
site: sukabumi
processed_at: 2026-04-20T01:23:45.678901+00:00
source_geojson: survey_20260420.geojson
h_ref: 12.345
h_ref_source: derived-from-wl-mean    # or: user-supplied
pole_length: 1.8
source_crs: EPSG:4326
target_crs: EPSG:32748
counts:
  gcps: 10
  cross_section: 14
  water_level: 2
  camera: 1
  check_points: 3
check_point_spread:                   # present only if >= 2 CP points
  horizontal_m: 0.021
  vertical_m: 0.018
  gate_status: OK                     # or: EXCEEDS GATE
warnings:                             # present only if any warnings fired
  - 'GCP elevation spread is only 0.30 m — markers should cover > 0.5 m vertically ...'
```

---

## Validation rules

### Hard fails (script exits 1, no files written)

| Check |
|-------|
| GeoJSON missing, unreadable, or not a FeatureCollection |
| GeoJSON contains no features |
| `--h-ref` not supplied AND no `WL` points to derive it from |
| Fewer than 4 GCP points |
| Zero or multiple `CAM` points (expected exactly one) |
| Zero cross-section points |
| Duplicate label within any bucket (GCP, XS, WL, CAM, CP) |
| Source CRS is WGS84 but a coordinate is not a valid lon/lat |
| An output file already exists and `--force` was not passed |

### Warnings (script continues)

| Check |
|-------|
| Fewer than 8 GCPs (recommended minimum for robust pose fit) |
| GCP bounding-box aspect ratio below 0.2 (markers look colinear) |
| GCP elevation spread below 0.5 m (poor Z constraint) |
| Gap in `GCP`/`XS` numbering |
| Two points within 10 cm of each other (likely duplicate) |
| Camera elevation at or below `h_ref` |
| Camera less than 1 m above `h_ref` |
| Supplied `--h-ref` differs from WL mean by more than 0.5 m |
| `h_ref` below the minimum XS elevation (channel appears dry) |
| `h_ref` above the maximum XS elevation (XS missed the banks) |
| Fewer than 2 WL points |
| Reprojected coord falls outside typical UTM-48S ranges |
| `--pole-length` outside [0.5, 4.0] m |
| `--h-ref` outside [-500, 6000] m |
| Check-point spread exceeds 3 cm H or 4 cm V |

---

## Check-point drift report

If the GeoJSON contains any `CP*` labels, the script prints a drift
report to stderr and records the spread in `metadata.yaml`. Check
points are repeat-occupation readings taken at the same physical
mark at different times during the survey — typically `CP_START`,
`CP_NOON`, `CP_END`, or three back-to-back readings at `CP_START`.

The report has three parts:

```
CHECK POINTS: 3 point(s) — CP_END, CP_NOON, CP_START
  Spread: 2.1 cm H, 1.8 cm V  (gate: ≤3 cm H / ≤4 cm V → OK)
  Pairwise:
    CP_END   ↔ CP_NOON : 1.2 cm H, 0.8 cm V
    CP_END   ↔ CP_START: 2.1 cm H, 1.8 cm V
    CP_NOON  ↔ CP_START: 1.5 cm H, 1.2 cm V
```

The 3 cm horizontal / 4 cm vertical gate comes from the survey
procedure's Success Criteria. If either threshold is exceeded, the
script adds a warning — something changed during the day (base
moved, NTRIP shifted, atmospheric drift) and the survey should be
treated with suspicion before use.

`CP*` points are excluded from all ORC CSVs.

---

## Common errors and fixes

| Message | Cause / fix |
|---------|-------------|
| `ERROR: pyproj not installed` | Run `pip install pyproj` in the active virtualenv |
| `ERROR: Expected FeatureCollection, got <type>` | GeoJSON is malformed or not a point export — re-export from SW Maps |
| `WARN: feature missing name/label/remarks property; skipping (...)` | A point has no Remarks field in SW Maps. Add the label in the handheld and re-export, or delete the stray feature from the GeoJSON. |
| `WARN: N feature(s) had unrecognized labels` | A label does not start with `GCP`, `XS`/`CS`, `WL`, `CAM`, or `CP`. Rename in SW Maps (or the raw GeoJSON) before re-running. |
| `need >= 4 GCPs, got N` | The export has fewer than 4 points whose label begins with `GCP`. Check spelling — `GPC1` is not `GCP1`. |
| `multiple camera positions found` | More than one feature labeled `CAM` or `CAMERA`. Exactly one is expected. |
| `<label>: coordinates (..) are not valid lon/lat — is --source-crs correct?` | The GeoJSON was exported in a projected CRS, not WGS84. Pass `--source-crs EPSG:<code>` matching the export. |
| `<label>: projected easting ... outside the typical UTM-48S range` | Either the target UTM zone is wrong (use `--target-crs` to override — e.g. `EPSG:32749` for UTM 49S) or a point was mis-surveyed in the wrong part of the world. |
| `ERROR: <file> exists (use --force to overwrite)` | A previous run already wrote into the output directory. Pass `--force` if you intend to overwrite, otherwise pick a fresh directory. |
| `check-point spread X cm H / Y cm V exceeds the gate` | The base or NTRIP solution drifted during the survey. Investigate before trusting the data — see the survey docs' "Success Criteria" section. |

---

## See also

- `SURVEY_PROCESS_v3_base.md` — base-station survey procedure
- `SURVEY_PROCESS_v3_ntrip.md` — NTRIP survey procedure
- `../spring_2026_ID/docs/VIDEO_CONFIG_SETUP.md` — Phase 4 runs
  this script as one step of the broader video-config workflow
- `PPP_TRANSLATION.md` — how to apply a PPP correction to the CSVs
  produced by this script (base-station workflow only)
