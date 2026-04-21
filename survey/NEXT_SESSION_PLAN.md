# Next Session Plan

*Pick-up brief for the next session. Read this first if you're resuming the Sukabumi fitment work cold.*

## State as of end-of-day 2026-04-21

**Day-2 correction pipeline ran clean.** Output in `spring_2026_ID/survey_data/output/`:

| Output | Count | Notes |
|---|---|---|
| `gcps.csv` | 20 | GCP1–14, 17, 18, plus GCP1.2/2.2/3.2/4.2 re-shoots |
| `cross_section.csv` | 21 | XS1 anchor-start, 17 bed points, XS19 anchor-end + XS1.2/XS2.2 re-shoots |
| `water_level.csv` | 1 | WL1 at z = 617.065 m |
| `camera_position.csv` | 1 | CAM at z = 624.449 m (after 40 cm pole correction) |
| `metadata.yaml` | — | `counts.camera: 1` — day-1 blocker cleared |

Check-point gate still fires at 98.6 cm H / 138.8 cm V on purpose — salvage-mode signal.

**Auto-fit pipeline built and dry-run against real data.** Phases 0, 1, 2 complete:

- **Phase 0:** Ground-truth clicker at `survey/auto_fit/ground_truth_click.py`; fixture at `survey/tests/fixtures/sukabumi_gt_clicks_v1.json` (17 of 20 GCPs clicked; GCP12, GCP17, GCP18 not clicked).
- **Phase 1 MVP:** `survey/auto_fit/{bootstrap,detect_local,refine,visualize,plots,report,subset_search}.py` + `survey/orc_auto_fit.py` CLI driver. Supports `--bootstrap-from-gt`, `--use-clicks`, `--subset-search`, annotated-frame visualisation, per-run output dir with input SHAs.
- **Phase 2:** Subset search (greedy drop-one + exhaustive over all 6+ GCP subsets with quadrant coverage).

**Salvage result.** Using Tom's 17 ground-truth clicks + subset search:

- Baseline RMSE (all 17): 79 cm.
- **Best 6-GCP subset: {GCP7, GCP8, GCP10, GCP13, GCP14, GCP3.2} → 4.61 cm RMSE.** Below the 5 cm target.
- Only 3 subsets clear the 5 cm gate out of 81,102 valid 6+ subsets. All three share a hard core of **GCP7, GCP8, GCP10, GCP13**.

**Why the survey was hard** (from tonight's diagnostic plot, `gcp_support.png`):

- Three genuine same-marker RTK drifts: GCP2 ↔ GCP2.2 (29 cm), GCP4 ↔ GCP4.2 (75 cm), GCP3 ↔ GCP3.2 (89 cm). All far above the 3 cm RTK gate.
- One field mislabel: **GCP1 and GCP1.2 are different physical markers** (Tom's clicks are 958 px apart in the video), not a re-occupation. The 218 cm UTM "drift" is real geometry.
- Bamboo pole (2.42 m) correlates with exclusion: all three 242 cm-pole GCPs (GCP2, GCP3) are in the excluded orange group.
- GCP5, GCP1, GCP6, GCP1.2 exceed the ~90 cm physical floor and are likely individual fix-quality failures (FLOAT not FIX, or similar).

## Where to resume

The salvage question is **answered**: the survey can be calibrated at 4.6 cm RMSE on a 6-GCP subset. Ranked next steps:

1. **Emit a loadable `sukabumi_auto_fit.json` CameraConfig. ← the gap to close next.** The current driver produces `clicks.json`, `labels.json`, `report.md`, and `audit.json` but **does not yet emit a `pyorc.CameraConfig` JSON**. Closing that loop means building a `pyorc.CameraConfig` from the best subset with frozen intrinsics (so the byte-equal round-trip claim from A3 holds) and verifying it loads via `pyorc.load_camera_config`. ~30 min. This is what makes the fit actually usable in ORC-OS.
2. **`--demo-override` implementation.** Must-support per design §3, but the current salvage result passes the quality bar — override only fires when that bar is missed. Useful to implement so the path is tested before any live demo. ~45 min.
3. **Phase 3 polish.** Tests (`survey/tests/` + `pytest.ini`), `orc_build_camera_config.py --from-auto` wiring, `survey/AUTO_FIT_USAGE.md`. ~1 day.

Phase 1.5 (photo pose-prior) is explicitly **not** the critical path — the `--use-clicks` shortcut bypasses the detector entirely, so Phase 1.5 only matters for a full hands-free automation ambition we don't currently have.

## Commands — ready to run

```bash
cd /Users/tjordan/code/git/openrivercam
source .venv/bin/activate

# Re-run the full salvage path (deterministic; outputs go to a new
# timestamped run dir under spring_2026_ID/survey_data/auto_fit_runs/).
python3 survey/orc_auto_fit.py \
    --video spring_2026_ID/survey_data/source_data/20260420T034813.mp4 \
    --gcps spring_2026_ID/survey_data/output/gcps.csv \
    --camera-position spring_2026_ID/survey_data/output/camera_position.csv \
    --gt-clicks survey/tests/fixtures/sukabumi_gt_clicks_v1.json \
    --use-clicks survey/tests/fixtures/sukabumi_gt_clicks_v1.json \
    --subset-search \
    --site sukabumi \
    --tag salvage_final
```

## Correction pipeline cheat sheet — 2026-04-21 rerun

Full command block is in `spring_2026_ID/survey_data/20260421_rerun_plan.md`. In case of re-run from scratch:

```bash
python3 survey/orc_rename_points.py \
    spring_2026_ID/survey_data/sukabumi_survey_20260421.geojson \
    --rename CP2=GCP2 --rename 'GCP3@1=GCP3.2' \
    --reason "..." \
    -o spring_2026_ID/survey_data/sukabumi_survey_20260421_corrected.geojson

python3 survey/orc_apply_pole_lengths.py \
    spring_2026_ID/survey_data/sukabumi_survey_20260421_corrected.geojson \
    spring_2026_ID/survey_data/pole_lengths.csv \
    -o spring_2026_ID/survey_data/sukabumi_survey_20260421_adjusted.geojson

python3 survey/orc_rename_points.py \
    spring_2026_ID/survey_data/sukabumi_survey_20260421_adjusted.geojson \
    --rename HREF=WL1 --reason "..." \
    -o spring_2026_ID/survey_data/sukabumi_survey_20260421_adjusted_wl.geojson

python3 survey/orc_xs_from_depths.py \
    spring_2026_ID/survey_data/sukabumi_survey_20260421_adjusted_wl.geojson \
    spring_2026_ID/survey_data/xs_depths.csv \
    --anchor-start XS1 --anchor-end XS2 \
    --water-surface-z 617.065 \
    -o spring_2026_ID/survey_data/sukabumi_survey_20260421_with_bed.geojson

python3 survey/orc_survey_prep.py \
    spring_2026_ID/survey_data/sukabumi_survey_20260421_with_bed.geojson \
    --site sukabumi --pole-length 0 \
    --output-dir spring_2026_ID/survey_data/output --force
```

## Recorded decisions

Five decisions captured today (see `survey/AUTO_FIT_DESIGN.md` §10 and `survey/Methodology.md` §6):

- Start without photos; add only if needed (not needed — `--use-clicks` path works).
- Bypass pyorc's calibration machinery in the inner loop (frozen intrinsics + direct `cv2.solvePnP`).
- Hard constraints not soft penalties (|S| ≥ 6, all four image quadrants).
- Refuse by default when noise floor exceeded; `--demo-override` required for demo output.
- Scope is Sukabumi only; no investment in reusability beyond that.

## Known traps (still valid)

- **PyPI package name:** OpenRiverCam installs as `pyopenrivercam`, NOT `pyorc` (the short name is an unrelated Apache ORC reader).
- **Dockerfile patches:** `rainbow-sensing/orc-os/` has `setuptools<70` via PIP_CONSTRAINT and a deduplicated rasterio specifier.
- **Daemon filename template:** videos dropped in `uploads/incoming/` must match `{%Y%m%dT%H%M%S}.mp4`. Non-timestamped files get moved to `tmp/`.
- **Lens calibration from `calibration_a.mp4` currently fails:** pyorc's `set_lens_calibration` expects a 9×6 chessboard, not a 5×7 charuco. Re-shoot or skip lens intrinsics.
- **GCP1 vs GCP1.2 is a field mislabel, not a re-shoot pair.** The two `.2` members are different physical markers. Other `.2` pairs (GCP2, GCP3, GCP4) are genuine re-occupations.

## Cross-references

- `survey/Methodology.md` — plain-English walkthrough (background concepts in Appendix A).
- `survey/AUTO_FIT_DESIGN.md` — full technical design + decision record.
- `survey/ORC_FIT_STRATEGY.md` — manual residual reading, physical floor, drop-one rules.
- `survey/ORC_OS_DOCKER.md` — Docker station setup.
- `spring_2026_ID/survey_data/20260421_rerun_plan.md` — correction-pipeline command sequence + decisions.
- `spring_2026_ID/survey_data/corrections.md` — append-only correction log with baseline SHAs.
- `survey/orc_build_camera_config.py` — manual-click CameraConfig path (still the fallback).
- `survey/outsourced_survey_brief.md` + `survey/research/professional_surveyor_and_escape_hatch.md` — re-survey fallback options.
