# Next Session Plan

*Pick-up brief for the next session. Read this first if you're resuming the Sukabumi fitment work cold.*

## End-of-day 2026-04-21 — paused for team review

Stopped today to memorialize state. Tom will walk the team through the
auto-fit approach tomorrow using `survey/Methodology.md` (team-facing
doc written today). Any changes after that review get folded into
v0.3 of `survey/AUTO_FIT_DESIGN.md` before Phase 1 starts.

**If resuming with no changes from the team review**, the next action
is for Tom to run the Phase 0 ground-truth clicker (one-time 30 min
session). Command under "Commands — ready to run" below.

**If the team requests changes**, update `AUTO_FIT_DESIGN.md` first
(bump to v0.3, add a decision-record entry for what changed and
why), then reconsider whether the Phase 0 fixture needs to be
re-done.

## Status as of 2026-04-21 end-of-day

**Day-2 rerun complete.** The correction pipeline ran end-to-end
against the day-2 export (`20260421_sukabumi_with_cam.geojson`,
SHA `8c844092…`) and produced a full `spring_2026_ID/survey_data/output/`:

| Output | Count | Notes |
|---|---|---|
| `gcps.csv` | 20 | GCP1–14, 17, 18, plus GCP1.2/2.2/3.2/4.2 re-shoots |
| `cross_section.csv` | 21 | XS1 anchor-start, 17 bed points (extrapolated from tape depths), XS19 anchor-end, plus XS1.2/XS2.2 re-shoots |
| `water_level.csv` | 1 | WL1 at z=617.065 m |
| `camera_position.csv` | 1 | CAM at z=624.449 m (after 40 cm pole correction) |
| `metadata.yaml` | — | `counts.camera: 1` — day-1 blocker cleared |

**Check-point gate still fires (98.6 cm H / 138.8 cm V).** That is
on purpose — the CP_start/CP_mid interpretation decision (see
`20260421_rerun_plan.md` → "Open questions resolved") treats these
as genuine drift-check failures, not label artifacts. We are in
**salvage mode**: running the fit to quantify how far the existing
noisy data can be pushed before escalating to the
professional-surveyor fallback (`survey/research/professional_surveyor_and_escape_hatch.md`).

**Tool changes landed this session:**
- `survey/orc_rename_points.py` → v1.1: supports `OLD@INDEX=NEW` to
  disambiguate duplicate labels (used on the day-2 duplicate `GCP3`).
  Smoke-tested; see the module docstring for syntax.

**Decisions recorded in `corrections.md` (three new entries dated 2026-04-21):**
1. Day-2 export ingest (zip → ISO-named archive; working rename).
2. `pole_lengths.csv` day-2 points added (12 rows, all 120 cm).
3. `pole_lengths.csv` CAM row added (40 cm).

Plus the full decision-by-decision rationale for the duplicate-GCP3
resolution and the CP_start/CP_mid salvage-mode call lives in
`spring_2026_ID/survey_data/20260421_rerun_plan.md`.

## Where to resume

**Fit decision is the next action.** The pickup options we left on
the table were:

- **A. `survey/orc_build_camera_config.py`** against the new outputs —
  opens the click UI on `spring_2026_ID/survey_data/source_data/20260420T034813.mp4`,
  produces per-GCP residuals sorted worst-first. Fastest salvage
  judgement path. Save clicks with `--save-clicks` for replay.
- **B. ORC-OS Docker dashboard Fit button** — paste the new CSVs,
  click pixel positions in the UI. Exercises the real operational
  path; same pyorc fit under the hood.
- **C. Both** — A first for residuals, then B to verify the
  operational path.

Default was **A** (salvage-mode residuals first).

## Auto-fit thread — design frozen, ready to build

**Design doc:** `survey/AUTO_FIT_DESIGN.md` (v0.2, spike + four-agent-review informed).

Goal: automate GCP detection in the calibration video and the
minimum-RMSE subset search, targeting ≤5 cm world-space registration
error on ≥70 % of GCPs.

**Key design decisions (v0.2):**
- Project-then-detect-locally (not global detection + separate labelling).
- Photos held in reserve as a **Phase 1.5 pose-prior** — only used
  if Phase 1 MVP misses the 5 cm bar.
- `cv2.solvePnPRansac(flags=cv2.USAC_MAGSAC)` for PnP — MAGSAC++
  soft-weighting handles Gaussian survey noise; pyorc itself does
  no outlier rejection, confirmed by Explore review of
  `pyorc/cv.py:505-546`.
- Subset search inner loop bypasses pyorc's calibration machinery —
  frozen intrinsics + direct `cv2.solvePnP` keeps each iteration at
  ~1 ms instead of seconds.
- Error metric is **metres** (world-ground units), not pixels —
  a v0.1 mistake caught by the Explore review.
- Frame index pinned to 0; SHA-256 recorded everywhere for audit.

**For Jakarta and future sites:** deploy ArUco 4×4 targets instead
of ad-hoc X-marks. One OpenCV call replaces Stages 1+2. See
`AUTO_FIT_DESIGN.md` §11 and the SOTA review at
`/tmp/auto_fit_review/sota_research.md`.

**Phase plan (2.5–3 days realistic):**

| Phase | Deliverable | Checkpoint |
|---|---|---|
| **0** | `sukabumi_gt_clicks_v1.json` — manual click of all 20 GCPs in frame 0 | Fixture file committed with schema per §9.1 |
| **1** | `survey/auto_fit/{bootstrap,detect_local,refine}.py` + `orc_auto_fit.py` CLI | A1: ≥70 % of GCPs within 5 cm of ground truth |
| **1.5** | `survey/auto_fit/photo_prior.py` (conditional on A1 fail) | A1 after re-run |
| **2** | `subset_search.py` + `audit.py` + `auto_fit_audit.json` output | A2: auto RMSE ≤ hand-trimmed |
| **3** | `survey/tests/`, `pytest.ini`, `orc_build_camera_config.py --from-auto`, `AUTO_FIT_USAGE.md` | A3: pyorc round-trip byte-identical; tests green |

Phase 0 is a prerequisite — A1 cannot be evaluated without it. The
Phase 0 clicker tool has been built and smoke-tested; the operator
just needs to run it and click.

## Commands — ready to run

```bash
cd /Users/tjordan/code/git/openrivercam
source .venv/bin/activate

# Phase 0 — one-time 20-GCP click (operator needs a screen; macOS native window)
python3 survey/auto_fit/ground_truth_click.py \
    --video spring_2026_ID/survey_data/source_data/20260420T034813.mp4 \
    --gcps spring_2026_ID/survey_data/output/gcps.csv \
    --camera-position spring_2026_ID/survey_data/output/camera_position.csv \
    --site sukabumi \
    --collected-by "Tom Jordan" \
    -o survey/tests/fixtures/sukabumi_gt_clicks_v1.json
```

## Team review doc

`survey/Methodology.md` — plain-English walkthrough of the approach,
written for the PMI-plus-hydrologist team. Lists five concrete
decisions for the team to weigh in on. Any changes from that review
get folded into AUTO_FIT_DESIGN.md v0.3 before Phase 1 starts.

## Command cheat sheet — 2026-04-21 rerun

Full command block is in `spring_2026_ID/survey_data/20260421_rerun_plan.md`.
In case of re-runs from scratch:

```bash
cd /Users/tjordan/code/git/openrivercam
source .venv/bin/activate

# Step 3: pre-pole rename
python3 survey/orc_rename_points.py \
    spring_2026_ID/survey_data/sukabumi_survey_20260421.geojson \
    --rename CP2=GCP2 \
    --rename 'GCP3@1=GCP3.2' \
    --reason "..." \
    -o spring_2026_ID/survey_data/sukabumi_survey_20260421_corrected.geojson

# Step 4: pole-length correction
python3 survey/orc_apply_pole_lengths.py \
    spring_2026_ID/survey_data/sukabumi_survey_20260421_corrected.geojson \
    spring_2026_ID/survey_data/pole_lengths.csv \
    -o spring_2026_ID/survey_data/sukabumi_survey_20260421_adjusted.geojson

# Step 5: post-pole rename
python3 survey/orc_rename_points.py \
    spring_2026_ID/survey_data/sukabumi_survey_20260421_adjusted.geojson \
    --rename HREF=WL1 \
    --reason "..." \
    -o spring_2026_ID/survey_data/sukabumi_survey_20260421_adjusted_wl.geojson

# Step 6: bed-point extrapolation
python3 survey/orc_xs_from_depths.py \
    spring_2026_ID/survey_data/sukabumi_survey_20260421_adjusted_wl.geojson \
    spring_2026_ID/survey_data/xs_depths.csv \
    --anchor-start XS1 --anchor-end XS2 \
    --water-surface-z 617.065 \
    -o spring_2026_ID/survey_data/sukabumi_survey_20260421_with_bed.geojson

# Step 7: final ORC-OS inputs
python3 survey/orc_survey_prep.py \
    spring_2026_ID/survey_data/sukabumi_survey_20260421_with_bed.geojson \
    --site sukabumi --pole-length 0 \
    --output-dir spring_2026_ID/survey_data/output \
    --force
```

## Known traps (still valid)

- **PyPI package name:** OpenRiverCam installs as `pyopenrivercam`, NOT `pyorc` (the short name is an unrelated Apache ORC reader).
- **Dockerfile patches:** `rainbow-sensing/orc-os/` has `setuptools<70` via PIP_CONSTRAINT and a deduplicated rasterio specifier.
- **Daemon filename template:** videos dropped in `uploads/incoming/` must match `{%Y%m%dT%H%M%S}.mp4`. Non-timestamped files get moved to `tmp/`.
- **Lens calibration from `calibration_a.mp4` currently fails:** pyorc's `set_lens_calibration` looks for a 9×6 chessboard, not a 5×7 charuco. Re-shoot or skip lens intrinsics.

## Cross-references

- `survey/ORC_FIT_STRATEGY.md` — how to read fit residuals, physical floor calc, drop-one loop
- `survey/ORC_OS_DOCKER.md` — Docker station setup, ports, patches
- `spring_2026_ID/survey_data/20260421_rerun_plan.md` — the command sequence and decision record for today's run
- `spring_2026_ID/survey_data/corrections.md` — append-only correction log; baseline SHAs at top
- `survey/orc_build_camera_config.py` — Python-API fast-path for residual analysis
- `survey/outsourced_survey_brief.md` — hire-a-surveyor fallback
- `survey/research/professional_surveyor_and_escape_hatch.md` — deep research on fallback options A–G
