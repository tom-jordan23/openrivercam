# ORC Camera-Fit Strategy and Continuity Brief

*Picks you up cold on the camera-config fit work. Read this before touching the script.*

## 1. Situation

Deploying OpenRiverCam (ORC) stations in Indonesia. Current site: **Sukabumi regency, West Java**. Day 5 of the in-country trip as of 2026-04-21. Concern: the survey data collected on-site may not be accurate enough for a clean pyorc scene fit.

**Known survey accuracy issue (already documented):**
- Check-point spread: **98.6 cm horizontal, 138.8 cm vertical** — `EXCEEDS GATE` per `spring_2026_ID/survey_data/output/metadata.yaml`.
- This is roughly an order of magnitude worse than the 3 cm H / 4 cm V gate set for geodetic RTK work.
- Interpretation is unresolved: *systematic* (whole GCP set shifted ~90 cm from true datum but internally consistent) vs. *per-point random* matters a lot — see Section 5.

## 2. What's Already Built

- **`survey/orc_build_camera_config.py`** — wraps pyorc to build a `CameraConfig` from the processed survey CSVs. Handles the no-staff-gauge case (`h_ref=None` → pyorc stores 0.0). Prints per-GCP residuals sorted worst-first. End-to-end tested with synthetic clicks; writes a JSON that round-trips through `pyorc.load_camera_config`.
- **`survey/outsourced_survey_brief.md`** — team-handoff doc. Professional surveyor shortlist, SOW template (Indonesian + English), evaluation checklist. Recommended vendors: Geopasi (primary), Geoindo (backup), CV Tata Bumi (price comparator).
- **`survey/research/professional_surveyor_and_escape_hatch.md`** — deep research on surveyor options and fallback paths (A through G) if existing data can't be made to work.
- **`.venv/`** (gitignored) — Python 3.12 venv with `pyopenrivercam`, `opencv-python`, `matplotlib`, `requests` installed.

## 3. Key File Locations

| Purpose | Path |
|---|---|
| Processed GCPs (UTM 48S) | `spring_2026_ID/survey_data/output/gcps.csv` |
| Water level → z_0 | `spring_2026_ID/survey_data/output/water_level.csv` |
| Survey metadata (warnings) | `spring_2026_ID/survey_data/output/metadata.yaml` |
| Scene video | `spring_2026_ID/survey_data/source_data/20260420T034813.mp4` |
| Charuco calibration video | `spring_2026_ID/survey_data/calibration_a.mp4` *(not yet wired into the script)* |
| Raw GCP geojson (lon/lat) | `spring_2026_ID/survey_data/sukabumi_survey_adjusted_wl.geojson` |
| pyorc source (reference only) | `/Users/tjordan/code/git/pyorc/` (missing deps; not the working env) |
| pyorc working env | `.venv/lib/python3.12/site-packages/pyorc/` |

## 4. What to Expect on the First Fit

- The CLI path `pyorc camera-config` prints `average x, y distance error: X.XXX m` — **metres in the destination CRS**, not pixels. At 0.1 m it emits a warning.
- With ~90 cm survey spread, the warning **will fire**. That is expected and is not by itself a reason to panic.
- Our script additionally prints **per-GCP pixel residuals**, sorted worst-first, which the CLI does not.

### Physical floor on residuals

At ~90 cm survey error, camera range ~20 m, nominal focal length ~1500 px:

```
floor_pixels ≈ (0.9 m / 20 m) × 1500 px ≈ 67 px
```

If uniform residuals land around that number, the fit is **as good as the survey allows**. Trimming won't help; the data itself is the limit.

## 5. Action Plan When RMSE Is Crazy

Apply in order. Do not skip steps — each one eliminates a class of cause.

### Step 1 — Classify the error pattern before changing anything

Look at the sorted residual table and (if useful) plot the residual vectors on the frame:

| Pattern | Cause | What to do |
|---|---|---|
| One huge outlier, rest ≲ floor | Bad pixel click *or* single bad GCP | Go to Step 3 |
| All residuals vectors point same way | Systematic datum / CRS error | Go to Step 2. **Do not trim.** |
| Residuals grow toward image corners | Lens distortion not modelled | Wire in calibration_a.mp4 — see Section 7 |
| Uniformly near the physical floor | Survey noise, not a fit bug | **Stop.** Accept the floor. |
| Scattered, no structure | Per-point survey noise | Drop-one (Step 3) |

### Step 2 — CRS / datum sanity check

Expected: `EPSG:32748` (WGS 84 / UTM Zone 48S), ellipsoidal height throughout. Metadata confirms `target_crs: EPSG:32748`. If a future session accidentally passes lat/lon or a different zone, residuals will be in kilometres, not pixels — rerun with `--crs 32748`.

### Step 3 — Drop-one loop

The script's sorted table identifies the worst offender. Procedure:

1. Note the worst GCP id.
2. Open the saved clicks JSON (`--save-clicks` output), either delete that id or re-click that one point with a fresh run. Fresh clicks are cheap.
3. Refit. Record new RMSE.
4. If RMSE dropped substantially, repeat on the new worst offender.
5. When a removal barely changes RMSE (say <10% improvement), **stop**. You're chasing noise.

### Step 4 — Respect the minimums

| Count | Status |
|---|---|
| ≥ 8 | comfortable — keep going |
| 6–7 | working minimum; stop trimming |
| 4–5 | solvePnP still runs but detecting further outliers is unreliable |
| < 4 | fit is underdetermined |

### Step 5 — Preserve geometric spread

Before dropping a point, ask: is this the only GCP providing near-bank or far-bank depth constraint? If yes, keeping an "outlier but unique" point may be better than a clean-looking set clustered on one side.

### Step 6 — Accept the physical floor

Apply the floor formula in Section 4 with your actual camera distance and focal length. If you're within ~2× of that number uniformly, further trimming will not help. Document the residual and move on.

### Step 7 — When to abandon and escalate

If after Steps 1–6 the residuals still sit at many multiples of the floor, the problem is the survey itself, not the fit. Shift to the escape hatch:

- Consult `survey/research/professional_surveyor_and_escape_hatch.md` — options A–G ranked by cost, time, and quality.
- Fastest in-country recovery: **Option B** (rent Emlid Reach RS2+ from MSDI or ADHIJASA, re-measure yourself).
- Cleanest hand-off: **Option C** (hire Geopasi for GCPs only, keep existing cross-section).

## 6. Traps to Avoid

- **`pip install pyorc` is the wrong package.** The PyPI name for OpenRiverCam is `pyopenrivercam`. The short name `pyorc` on PyPI is an unrelated Apache ORC file reader. Import name is still `pyorc`.
- **Do not commit `.venv/`.** It's gitignored at `.gitignore:25` but earlier this session it leaked — double-check `git status` stays clean before commits.
- **Do not pre-trim GCPs before seeing a fit.** The residual pattern is what tells you which points are bad. Guessing first discards information.
- **Do not chase sub-pixel residuals when survey error is ~90 cm.** It is physically impossible. Know the floor.
- **Do not edit GCPs in UTM metres when you meant to edit lat/lon, or vice versa.** A small-looking number (0.000001) in degrees is ~10 cm; a small-looking number in metres is 1 mm.
- **h_ref must stay unset (defaults to 0.0).** No staff gauge at this site. If a future session passes `h_ref=<something>`, water-level readings will be offset by that much.

## 7. Unfinished Business

These are deliberately deferred. Finish them only if the residual investigation says you need them.

- **Lens calibration from `calibration_a.mp4`** — not yet wired through `CameraConfig.set_lens_calibration`. If Step 1 shows corner-biased residuals, this becomes a priority. Add with:
  ```
  --calibration-video spring_2026_ID/survey_data/calibration_a.mp4
  ```
  (The flag already exists in the script; the pyorc call is in place. What's missing is verifying the video is actually a charuco recording.)
- **Camera position not surveyed.** Metadata warning: *"no camera position found — ORC calibration cannot be completed until CAM is surveyed and this script is re-run."* Blocks full velocimetry, not the residual check.
- **`bbox` / `corners` not set.** Needed for the velocimetry grid, not for the scene fit.
- **Only one water-level point.** Metadata warns two (both banks) is recommended.

## 8. Command Cheat Sheet

```bash
# activate env
source .venv/bin/activate

# first fit (interactive clicks, saves clicks.json for replay)
python survey/orc_build_camera_config.py \
  --video spring_2026_ID/survey_data/source_data/20260420T034813.mp4 \
  --gcps spring_2026_ID/survey_data/output/gcps.csv \
  --water-level spring_2026_ID/survey_data/output/water_level.csv \
  --output spring_2026_ID/survey_data/output/sukabumi_camera_config.json \
  --save-clicks spring_2026_ID/survey_data/output/sukabumi_clicks.json

# refit with saved clicks (no UI)
python survey/orc_build_camera_config.py \
  --video ... --gcps ... --water-level ... \
  --clicks spring_2026_ID/survey_data/output/sukabumi_clicks.json \
  --output ...

# dry-run (validate inputs, skip pyorc, skip clicks)
python survey/orc_build_camera_config.py --dry-run \
  --video ... --gcps ... --water-level ...
```

## 9. Decision Record

- Building camera config with `pyorc` Python API, not the CLI wizard, because per-GCP residual reporting is required and the CLI only prints an aggregate.
- `h_ref` left unset (→ 0.0) because no staff gauge is installed. Water level will come from a radar or pressure sensor and feed velocimetry as a direct elevation.
- Outsourced survey option documented but not yet acted on; team has the brief (Section 10 of `outsourced_survey_brief.md` names Geopasi as primary).
