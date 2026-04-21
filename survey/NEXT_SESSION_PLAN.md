# Next Session Plan

*Pick-up brief for the next session. Read this first if you're resuming the Sukabumi fitment work cold.*

## Current Blocker

Waiting on an **updated survey geojson that includes the camera position (CAM* point)**. The previous survey round shipped `spring_2026_ID/survey_data/output/metadata.yaml` with this warning:

> no camera position found — downgraded by --allow-missing-cam; camera_position.csv skipped, ORC calibration cannot be completed until CAM is surveyed and this script is re-run

No forward progress is possible on a real fit until that point is measured and delivered.

## Data Flow Once the Updated Geojson Arrives

1. **Drop the new geojson into `spring_2026_ID/survey_data/`** (alongside or replacing the existing `sukabumi_survey_adjusted_wl.geojson`).
2. **Run the corrections pipeline** — applies pole-length adjustments, renames points to canonical IDs, reconciles water-level shots. Scripts live in `survey/`:
   - `orc_rename_points.py`
   - `orc_apply_pole_lengths.py`
   - Reference: `spring_2026_ID/survey_data/corrections.md`
3. **Run survey prep** — converts the corrected geojson to the CSVs ORC-OS needs:
   - `python survey/orc_survey_prep.py` → regenerates `spring_2026_ID/survey_data/output/gcps.csv`, `water_level.csv`, `cross_section.csv`, and (this time) `camera_position.csv`.
   - Reference: `survey/orc_survey_prep.md`.
4. **Verify `metadata.yaml` warnings have cleared** — especially the camera-position warning and the check-point spread gate. If the gate still exceeds 3 cm H / 4 cm V, return to `survey/ORC_FIT_STRATEGY.md` Section 5.

## Docker Station Iteration Loop

The ORC-OS docker station at `rainbow-sensing/orc-os/` (see `survey/ORC_OS_DOCKER.md`) is already bootstrapped with a device, daemon settings, skeleton camera config (id=1, "Sukabumi Site H"), and the auto-ingested scene video (id=1). To try the updated survey data:

1. Re-POST the camera config with updated `height`/`width`/CRS if anything changed (usually not).
2. Use the dashboard to:
   - Add the new control points (paste from fresh `gcps.csv`) and z_0 from `water_level.csv`.
   - Click GCP pixel positions on a frame from video id=1.
   - Run `/control_points/fit_perspective/` via the UI's Fit button.
3. Read the residuals. Apply the drop-one loop from `ORC_FIT_STRATEGY.md` Section 5.
4. If residuals settle within the physical floor for the survey noise (see the floor formula in `ORC_FIT_STRATEGY.md` Section 4), the dataset is good.
5. If not, escalate per `survey/outsourced_survey_brief.md` and `survey/research/professional_surveyor_and_escape_hatch.md`.

## Exit Criterion

A "working set of data" means: a saved camera config in ORC-OS with GCPs fitted, residual RMSE within the physical floor for the known survey noise, and the video ready to run in a `video_config`. That dataset then gets copied to the live station (the real Pi in the field) as the reference configuration.

## Known Traps (from the current session)

- **PyPI package name:** OpenRiverCam installs as `pyopenrivercam`, NOT `pyorc` (the short name is an unrelated Apache ORC reader). See `memory/reference_pyorc_pypi_name.md`.
- **Dockerfile patch:** the local clone at `rainbow-sensing/orc-os/` has two patches — `setuptools<70` via PIP_CONSTRAINT, and a deduplicated rasterio specifier in `pyproject.toml`. Re-apply if re-cloning. See `survey/ORC_OS_DOCKER.md` → "Local Patches Applied to the Clone".
- **Daemon filename template:** videos dropped in `uploads/incoming/` must match `{%Y%m%dT%H%M%S}.mp4`. Anything else (e.g., `calibration_a.mp4`) gets moved to `tmp/` and can look like it "disappeared". Keep non-timestamped files under `~/.ORC-OS/calibration/` or similar, outside the scan path.
- **Camera config can't be registered with only `dst`:** pyorc's `set_gcps` requires `src` too, so skeleton configs go in with no GCPs; the UI click workflow populates both at once.
- **Lens calibration from `calibration_a.mp4` currently fails:** pyorc's `set_lens_calibration` looks for a 9×6 **chessboard**, not a 5×7 charuco. Either re-shoot with the right pattern or skip lens intrinsics for now.

## Cross-References

- `survey/ORC_FIT_STRATEGY.md` — how to read fit residuals and what to do about them
- `survey/ORC_OS_DOCKER.md` — Docker station setup, ports, patches, current state
- `survey/orc_build_camera_config.py` — Python-API fast-path for residual analysis outside the UI
- `survey/outsourced_survey_brief.md` — hire-a-surveyor fallback for the team
- `survey/research/professional_surveyor_and_escape_hatch.md` — deep research on fallback options A–G
