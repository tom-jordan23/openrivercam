# Automated GCP Detection and Minimum-RMSE Fit — Design Doc

**Status:** Design v0.2 — spike-informed and review-informed. Ready to build Phase 1.
**Author:** co-authored Tom Jordan + Claude, 2026-04-21.
**Context:** Salvage-mode camera-fit work on the Sukabumi Spring 2026 deployment. See `ORC_FIT_STRATEGY.md` and `spring_2026_ID/survey_data/20260421_rerun_plan.md` for the manual-click pipeline this is meant to replace.

**v0.2 changes** (after four independent agent reviews — test-engineer, Explore on pyorc internals, comprehensive-researcher on SOTA, Plan architecture critique):

- Restructured from three stages to three-with-conditional. Global marker detection dropped in favour of **project-then-detect-locally** (Plan critique).
- Photo-based labelling demoted from co-primary channel to **conditional Phase 1.5 pose-prior** (MVP first; photos layered in only if Phase 1 misses the 5 cm accuracy bar).
- Hard constraints replace soft spread/count penalties — a tuneable λ nobody will tune is worse than a one-line floor.
- Stage-3 PnP switched to `cv2.solvePnPRansac(..., flags=cv2.USAC_MAGSAC)` (MAGSAC++ soft-weighting; better fit for Gaussian survey noise; no new dependency).
- Error-metric units clarified: pyorc reports **metres** (world-ground units), not pixels. All references reconciled.
- Test plan rewritten per test-engineer review: versioned ground-truth fixture, synthetic 10-GCP scene, explicit negative tests for the "re-survey required" signalling path.
- ArUco/AprilTag noted as the right answer for Jakarta and future sites.

---

## 1. Problem statement

We have:
- A surveyed set of 20 GCPs in UTM 48S (`spring_2026_ID/survey_data/output/gcps.csv`), known to carry ~90 cm position noise.
- A calibration video from the final camera mount (`spring_2026_ID/survey_data/source_data/20260420T034813.mp4`, 1920×1080, 5 s, 64 frames).
- A PDF of field-crew photos, one per GCP, showing the survey rod on each point (`spring_2026_ID/survey_data/source_data/gcp_photos.pdf`).
- A surveyed camera position (`camera_position.csv`, post-pole-correction).

We want to:
1. **Locate each GCP's pixel coordinate in the calibration video** automatically, replacing the manual-click step in `orc_build_camera_config.py` and the ORC-OS dashboard.
2. **Find the GCP subset that minimises reprojection RMSE** under physically-defensible constraints (≥ 6 GCPs, ≥ 1 GCP per image quadrant), so salvage judgement is data-driven rather than by-hand.
3. **Report** the optimal subset, its RMSE (in metres), per-GCP residuals, and how those compare to the physical floor for the known survey noise.

Output feeds `pyorc.CameraConfig` and drops into ORC-OS as a saved camera config.

## 2. Why automate this

**Scope note: one-shot salvage tool for Sukabumi 2026 only.** This pipeline exists *only* because the Sukabumi markers are already placed and the survey is already noisier than the RTK gate allows, and we cannot retroactively swap inputs. The design is judged against that scope: **cover the Sukabumi dataset well; do not invest in maintainability past the Sukabumi salvage decision.** Methodology for other sites is explicitly out of scope and handled separately.

Manual clicking is not today's bottleneck — the noisy GCP survey is. But a salvage decision requires iterating the GCP subset many times (to find the lowest-RMSE subset and prove that no subset meets the quality bar). Each iteration would require re-clicking by hand. Automating the clicking is what makes an exhaustive subset search feasible, which is what makes the re-survey decision defensible.

Epistemic win: a deterministic detector + MAGSAC PnP + scored subset search is *easier to audit* than a human click log. Provenance and reproducibility are project-wide principles (see `corrections.md`); a fit regenerable byte-identically from source files + one config is the right match to those principles for a one-shot calibration that has to defend a potentially high-cost re-survey decision.

## 3. Constraints and acceptance criteria

**Hard constraints (must).**
- Must use pyorc's `CameraConfig.set_gcps(...)` for final output. Intermediate subset search calls `cv2.solvePnP` directly, bypassing pyorc's calibration machinery for speed (see §5.3).
- Must write a `clicks.json` compatible with `orc_build_camera_config.py --clicks` so the manual path remains the fallback.
- Must respect `ORC_FIT_STRATEGY.md` §5 minimums: ≥ 6 GCPs in the final set; no empty image quadrant.
- Must not hide or suppress the check-point spread gate; salvage-mode preserves that signal.
- Every detection decision, subset evaluation, and rejection reason must be written to `auto_fit_audit.json`.
- Frame used for detection is **pinned to frame index 0** of the calibration video; frame SHA-256 recorded in all outputs.
- Must support an explicit `--demo-override` CLI flag that writes an *uncertified* CameraConfig even when normal acceptance criteria fail (see §5.4). Without the flag, the tool exits non-zero and writes no calibration when the survey noise dominates; *with* the flag, it writes a config that is indelibly marked `certification_status: "demo-only"`, named with a `_DEMO_UNCERTIFIED` filename suffix, and accompanied by a report whose first line is a disclaimer banner.

**Soft constraints (should).**
- Should finish end-to-end in under 2 minutes on this machine.
- Should degrade gracefully to human-in-the-loop per-GCP, not whole-pipeline.

**Acceptance criteria.**
- **A1.** On the 2026-04-21 dataset, the auto-located pixel coordinate for ≥ 70 % of the 20 GCPs lies within **5 cm in world-ground units** of a manually-clicked ground truth. At 20 m camera range with focal ≈ 1500 px, that is ≈ 3.75 px — about one human-click's worth of tolerance. Per-GCP world-space error is reported in the output; exceedances are flagged, not suppressed.
- **A2.** The auto-selected minimum-RMSE subset has world-space RMSE no worse than a hand-trimmed subset at the same cardinality on the same clicks.
- **A3.** A fit produced by the auto path round-trips through `pyorc.load_camera_config` byte-identically. Requires the auto path to write explicit `camera_matrix` and `dist_coeffs` into the output; if it leaves them None, pyorc re-calibrates on reload and byte-equality breaks (verified by Explore review).

## 4. Spike results (2026-04-21)

Artifacts at `/tmp/auto_fit_spike/`. Summary:

### 4.1 Marker detection (global, deprecated)

Spike ran Shi-Tomasi corners + 4-quadrant checker-ness + NMS over the whole frame. Result: **108 candidates in a frame with ~8–10 real markers**. Precision ~10 %; recall appears high but unverified.

**Conclusion.** Global detection is too noisy to use alone. Superseded by §5.2's project-then-detect-locally approach.

### 4.2 Photo→video registration (SIFT + RANSAC homography)

| GCP photo | Keypoints | Good matches | RANSAC inliers | Homography det | Condition | Verdict |
|---|---:|---:|---:|---:|---:|:---:|
| GCP1 | 8000 | 67 | 25 | 0.17 | 3.6M | **Degenerate** — close-up / different angle |
| GCP5 | 8000 | 282 | 210 | 0.91 | 21k | **Solid** |
| GCP11 | 8000 | 297 | 215 | 0.91 | 48k | **Solid** |

Overlays at `/tmp/auto_fit_spike/registration/GCP{5,11}_overlay.png`.

**Conclusion.** Photos that were captured from near the camera viewpoint register well (~200 inliers, near-identity homographies). Close-up / tight photos fail. Since a single failure breaks any pure-photo pipeline, photos are held in reserve as a Phase 1.5 pose-prior option, not as a primary channel.

### 4.3 Data-integrity note

Page 11 of `gcp_photos.pdf` carries a second image labelled `GCP15`, but `gcps.csv` has no GCP15 (pipeline warned "missing [15, 16, 19, ...]"). The label parser must flag orphaned photos and refuse to silently assign them to a surviving GCP ID.

## 5. Chosen approach

**Three stages; Stage 1.5 (photo pose-prior) is conditional — only built if Phase 1 MVP misses the 5 cm accuracy bar.**

### 5.1 Stage 1 — Pose bootstrap

Inputs: `camera_position.csv` (CAM in UTM), `gcps.csv` (surveyed GCP UTM), intrinsics.

Produces an initial `(rvec, tvec)` for the camera:
- Translation: CAM UTM.
- Look-at target: centroid of the surveyed GCP cluster.
- Roll: 0.
- Up: +Z (ellipsoidal).

Intrinsics source, in priority order:
1. Charuco-derived `camera_matrix` / `dist_coeffs` if the calibration video has been processed (see `ORC_FIT_STRATEGY.md` §7; currently not wired, but a CLI flag accepts a pre-computed JSON).
2. A frozen default: `focal = 1500 px`, principal point = image centre, zero distortion — `ORC_FIT_STRATEGY.md` §4 value.
3. (Other-site path is out of scope for this design — see §2 scope note.)

Once computed, intrinsics are **frozen** — they do not change during Stages 2 and 3. This is what makes the subset search fast: without frozen intrinsics, `pyorc.CameraConfig.set_gcps` triggers `optimize_intrinsic` → `differential_evolution` → seconds per subset; with frozen intrinsics, each subset iteration is a single `cv2.solvePnP` call at ~1 ms.

### 5.2 Stage 2 — Project-detect-refine (the MVP loop)

Replaces the v0.1 design's global-detector-then-label decomposition. The bootstrap pose is strong enough to give small projection windows; doing detection locally in those windows cuts noise by two orders of magnitude.

For each surveyed GCP:
1. Project its UTM coordinate to pixel space using the current pose. First pass uses Stage-1 bootstrap; subsequent passes use the refined pose from step 5.
2. Crop a ±50 px window around the projection. On later refinement passes, tighten to ±20 px.
3. Run the checker-score detector (Shi-Tomasi + 4-quadrant validator at multiple scales) *inside that window only*. Keep the highest-scoring candidate above threshold.
4. If no candidate exceeds threshold, mark the GCP unresolved for this pass.
5. Collect the resolved `(UTM, pixel)` pairs and call `cv2.solvePnPRansac(...*, flags=cv2.USAC_MAGSAC)` with the frozen intrinsics. Use the returned `inlier_mask` to drop RANSAC outliers.
6. Recompute pose from the inliers (MAGSAC's refinement output).
7. Re-project all GCPs and repeat. Exit when the inlier set is stable across iterations OR after 4 iterations.

Exit state: `{gcp_id: (pixel_x, pixel_y, world_error_m, inlier_flag)}` plus the refined pose.

GCPs never detected in any pass → queued for manual click via the `orc_build_camera_config.py --clicks` path; not silently dropped.

### 5.2.1 Stage 1.5 — Photo pose-prior (conditional)

Only built if Phase 1 MVP fails A1 at the 5 cm bar.

Use 2–3 photos that spike §4.2 showed as reliable (GCP5, GCP11 class): SIFT + RANSAC homography to the pinned video frame, warp the photo's marker centroid to the video frame, treat those as extra `(pixel, UTM)` correspondences to sharpen the Stage-1 bootstrap pose. The homography doesn't have to be perfect — it only has to improve the initial pose enough that Stage 2's projection windows can tighten to ±20 px on the first pass instead of the third.

Pole-tip colour segmentation (in the v0.1 design) is dropped. The marker we care about is the ground target, not the rod above it; the SIFT homography warps the marker centroid directly.

### 5.3 Stage 3 — Subset search for minimum-RMSE fit

Your explicit directive: the pipeline must test *discarding points* to lower RMSE. This is that stage.

Input: resolved `{gcp_id: (pixel, UTM, world_error_m)}` from Stage 2.

**Scoring.** World-space RMSE only — no soft penalties, hard constraints instead:
```
hard_constraints:
  |S| >= 6                                     # minimum from ORC_FIT_STRATEGY §5
  every image quadrant contains ≥ 1 GCP in S   # prevent bank collapse
score(S) = rmse_world_metres(S)
```
Subsets violating a hard constraint are rejected upfront; no score computed.

**Search.**
1. Compute baseline RMSE on the full resolved set.
2. Greedy drop-one: at each step, remove the GCP whose removal most reduces RMSE (pyorc is not doing this for us — Explore review confirmed pyorc's PnP does no outlier rejection internally).
3. Stop when (a) next removal improves RMSE by < 10 %, (b) |S| = 6, or (c) the next removal would empty an image quadrant.
4. If the final set size n ≤ 15, run a full exhaustive search over `C(n, 6..n)` as a local-optimum check. Skip otherwise.
5. Each subset evaluation is `cv2.solvePnP` with frozen intrinsics — ~1 ms per call, well within the 2-minute budget for the exhaustive path.

Output: chosen subset S*, RMSE on S*, RMSE on S* ± each candidate point (contribution view), per-GCP residuals sorted worst-first, full audit trail in JSON.

### 5.4 Uncertified demo-override output

When the auto-fit's normal conclusion is "no subset meets the quality bar" (resolvability = `insufficient`), the default behaviour is to exit non-zero and write no CameraConfig. An explicit `--demo-override` CLI flag overrides that refusal and writes a calibration anyway, for end-to-end OpenRiverCam pipeline demonstration only. The override is engineered to be impossible to consume silently:

1. **Filename marker.** The CameraConfig is written as `*_DEMO_UNCERTIFIED.json` (and the sibling `_report.md`, `_clicks.json`, `_audit.json` follow suit — see §6). A file-system glob for the normal name returns nothing in demo-mode runs.
2. **In-config marker.** The top-level JSON of the CameraConfig carries `"certification_status": "demo-only"`. Downstream consumers (ORC-OS dashboard, velocimetry scripts, the dashboard importer) are expected to refuse to publish flow-rate numbers when this field is `demo-only` — a follow-on task to wire that check into the downstream consumers is flagged in §11 out-of-scope. In the interim, the filename suffix is the primary safety net.
3. **Report disclaimer.** The accompanying `*_report.md` has a mandatory disclaimer as its first line and again above the per-GCP residual table:
   ```
   > **DEMO-UNCERTIFIED — do not use for certified flow, discharge, or water-level measurements.**
   ```
4. **Audit entry.** The `*_audit.json` records the flag, the user (from the `--collected-by` or `$USER`), the timestamp, the reason (free-text required by the flag), and the worst per-GCP residual that would otherwise have triggered the refusal.
5. **CLI ergonomics.** `--demo-override` alone is not sufficient. It must be accompanied by `--override-reason "..."` explaining what the demo is for (stakeholder walk-through, pipeline-bug triage, training session). Both strings are recorded verbatim in the audit JSON.

The override is *not* intended to mask a registration-quality (A1) failure. A1 is about automation; A2 about the survey. The override is for the A2 case specifically — the calibration's world-metres RMSE exceeds what we would call certifiable, but the tool's per-GCP registrations were accurate enough that the downstream pipeline has something coherent to run on.

Behavioural matrix:

| A1 (registration) | A2 (RMSE vs. floor) | Normal behaviour | Behaviour with `--demo-override` |
|:---:|:---:|---|---|
| pass | pass | Write certified config (no suffix) | Irrelevant; flag ignored with warning |
| pass | fail | Refuse, exit non-zero | Write `*_DEMO_UNCERTIFIED.json` |
| fail | any | Refuse, exit non-zero | **Still refuse.** Demo-override is not for registration failures — fix Phase 1.5 or manually click instead. |

This last row is deliberate: if the automation itself can't locate markers, a demo is not useful. Demo-mode is for "the math is working, the data is just noisy" cases.

## 6. Data contracts / IO

```
Inputs (paths relative to repo root):
  - spring_2026_ID/survey_data/source_data/20260420T034813.mp4   # frame 0 pinned
  - spring_2026_ID/survey_data/source_data/gcp_photos.pdf
  - spring_2026_ID/survey_data/output/gcps.csv
  - spring_2026_ID/survey_data/output/camera_position.csv
  - spring_2026_ID/survey_data/output/water_level.csv            # z_0 for CameraConfig
  - (optional) intrinsics.json                                    # charuco output if available

Intermediate (under survey/auto_fit_work/, gitignored):
  - frame.png                          # the pinned video frame
  - frame.sha256                       # for provenance
  - photos/GCP{id}.png                 # PDF pages extracted
  - photo_manifest.json                # labels + orphan flags
  - detections_by_pass.json            # per-pass candidate windows and winners
  - labels.json                        # final {gcp_id: (x, y, world_err_m)}

Outputs — all runs (per-run timestamped subdirectory):
  # run_dir = spring_2026_ID/survey_data/auto_fit_runs/<timestamp>_<site>_<tag>/
  <run_dir>/report.md                         # human-readable summary
  <run_dir>/audit.json                        # every decision, every rejected subset reason
  <run_dir>/labels.json                       # per-GCP pixel + residual record
  <run_dir>/clicks.json                       # manual-path compatible click file
  <run_dir>/detections_by_pass.json           # stage 2 windowed detection trace
  <run_dir>/annotated.png                     # frame with clicks/detections/residual vectors
  <run_dir>/gcp_support.png                   # per-GCP diagnostic bar chart (if subset search ran)

Outputs — normal path (acceptance criteria met; requires --water-level):
  <run_dir>/sukabumi_autofit_camera_calibration.json       # pyorc CameraConfig (pure pyorc, no extras)
  <run_dir>/sukabumi_autofit_camera_calibration_cert.json  # cert sidecar: {"certification_status": "ok", ...}

Outputs — demo-override path (--demo-override set, gate failed):
  <run_dir>/sukabumi_autofit_camera_calibration_DEMO_UNCERTIFIED.json
  <run_dir>/sukabumi_autofit_camera_calibration_DEMO_UNCERTIFIED_cert.json
    # cert sidecar carries: certification_status="demo-only", override_flag,
    # override_reason, override_invoked_by ($USER), override_timestamp (UTC),
    # rmse_m and quality_gate_m, resolvability_note (human-readable explanation)
```

`orc_build_camera_config.py --from-auto <run_dir>` consumes the auto-fit's
`clicks.json` and filters to the chosen subset via the IDs recorded in
`audit.json`'s `subset_search.best.ids`, then runs the manual PnP path
for independent verification.

## 7. Phases and checkpoints

**Phase 1 — MVP end-to-end.** (≈ 1 day)
- `survey/auto_fit/bootstrap.py` — Stage 1 pose bootstrap.
- `survey/auto_fit/detect_local.py` — local detector (Shi-Tomasi + checker-score, windowed).
- `survey/auto_fit/refine.py` — Stage 2 project-detect-refine loop with MAGSAC PnP.
- `survey/orc_auto_fit.py` — CLI driver; writes `labels.json`, a per-GCP report, and a minimal `clicks.json`.
- **Checkpoint 1:** run against 20 known GCPs with a hand-authored `sukabumi_gt_clicks_v1.json`. Report per-GCP world-space errors. A1 decision point.

**Phase 1.5 — Photo pose-prior.** (+½ day, conditional on A1 failing at Checkpoint 1)
- `survey/auto_fit/photo_prior.py` — SIFT+RANSAC homography on 2–3 reliable photos, extra correspondences for the bootstrap.
- Re-run Checkpoint 1.

**Phase 2 — Subset search + audit JSON.** (≈ ½ day)
- `survey/auto_fit/subset_search.py` — greedy drop-one + conditional exhaustive.
- `survey/auto_fit/audit.py` — decision-log emitter.
- **Checkpoint 2:** report optimal subset + RMSE; compare to hand-trimmed (A2). Inspect the audit JSON for completeness.

**Phase 3 — Tests + wiring + docs.** (≈ 1 day)
- `survey/tests/` — per §9.
- `orc_build_camera_config.py --from-auto` plumbing.
- `survey/AUTO_FIT_USAGE.md` — how to run, what to check.
- **Checkpoint 3:** A3 round-trip check; ORC-OS dashboard import verification; full test suite green.

**Total: 2.5–3 days realistic**, including Phase 1.5 if it triggers.

## 8. Risks and fallbacks

| Risk | Likelihood | Impact | Fallback |
|---|:---:|:---:|---|
| Local detector misses a geometrically unique GCP (only near-bank or only far-bank) | Med | **High** | Frame averaging (frames 5..55); widen window; manual click for the missed one |
| Bootstrap pose bad enough that first-pass projections miss real markers by > 50 px | Low | Med | Phase 1.5 photo pose-prior triggers; widen first-pass window to 100 px as a CLI toggle |
| Photos don't match GCP IDs (GCPunknown / GCP15 case from §4.3) | **High — already happened** | Med (silent mis-fit) | Label parser flags orphans; pipeline refuses to assign orphaned photos; documented in the report |
| Subset search picks a 6-GCP subset clustered on one bank despite hard quadrant constraint | Low | Med | Hard constraint rejects those subsets upfront; tighten to "≥ 1 per quadrant AND ≥ 2 per bank" if needed |
| pyorc API changes between versions | Low | Med | Pin `pyopenrivercam` version in the venv lockfile; version cited in output `auto_fit_audit.json` |
| SIFT not in the installed OpenCV wheel (`opencv-python` vs `opencv-contrib-python`) | Med | High for Phase 1.5 only | Fall back to ORB features; or install `opencv-contrib-python` into the venv |
| Frame drift between manual ground-truth click and auto-fit run | Low once pinned | High if unpinned | Frame index pinned to 0; frame SHA-256 recorded and re-checked on every run; loud error if mismatch |
| Lens-distortion unmodelled; reprojection residuals grow toward image corners | Low (short focal, flat scene) | Med | Wire charuco → `camera_matrix` / `dist_coeffs`; feed into `orc_auto_fit.py --intrinsics` |
| Survey noise dominates; all subsets RMSE ≫ physical floor | **High — expected in salvage mode** | Low (this is the signal we want) | Default: report `resolvability: insufficient`, exit non-zero, point at `survey/research/professional_surveyor_and_escape_hatch.md`. With `--demo-override` + `--override-reason "..."` (§5.4): write an uncertified CameraConfig with `_DEMO_UNCERTIFIED` filename, `certification_status: demo-only` in-config, and a report whose first line is a disclaimer. Downstream consumers must refuse to publish flow-rate numbers when the config is demo-only. **Not a failure — success looks like this when the data can't support a certified fit.** |

Row 7's salvage-mode outcome is what automation can do that a human click log can't: quantify unfit-ness fast, feed the re-survey decision, not hide it.

## 9. Test strategy

Full version per the test-engineer review. Short form:

### 9.1 Ground-truth fixture

`survey/tests/fixtures/sukabumi_gt_clicks_v1.json`, versioned filename so regressions against a moving design are detectable:

```json
{
  "schema_version": 1,
  "site": "sukabumi",
  "video_source": "spring_2026_ID/survey_data/source_data/20260420T034813.mp4",
  "frame_index": 0,
  "frame_sha256": "<sha of the PNG extracted from frame 0>",
  "gcps_csv_sha256": "<sha of gcps.csv at click time>",
  "collected_by": "Tom Jordan",
  "collected_date": "2026-04-21",
  "method": "manual-click via orc_build_camera_config.py UI",
  "clicks": {
    "GCP1": [x, y], "GCP2": [x, y], ...
  },
  "bank_assignment": {"GCP1": "near", "GCP2": "near", ...}
}
```

`bank_assignment` supports the spread-constraint test. `frame_sha256` and `gcps_csv_sha256` pin the external state so a re-encoded video or revised coords don't silently invalidate the fixture.

Committed, never edited in place — subsequent truth sets become `_v2`, `_v3`.

### 9.2 Synthetic 10-GCP fixture

`survey/tests/fixtures/synthetic_10gcp_frame.png` + `synthetic_10gcp_scene.json` + `generate_synthetic_fixture.py` (committed generator).

10 binary checkerboard targets at known pixel positions, known camera pose, zero noise. Deterministic. Tests:
- Stage 1 detector recall: all 10 detected within 3 px in-window.
- Stage 2 pose: refined pose within 0.5 m translation, 0.5° rotation of ground truth.
- Stage 3 subset: full 10 selected as optimal (no noise → no point to drop).
- Round-trip: output `clicks.json` consumed by `orc_build_camera_config.py --from-auto --dry-run` exits 0.

### 9.3 Negative / failure-mode tests

- **Survey-noise-dominates:** perturb UTM coords by ~90 cm Gaussian, assert output contains `resolvability: insufficient` and exit code non-zero, assert no `clicks.json` written.
- **Bad camera position (50 m blunder):** Stage 1 bootstrap + MAGSAC PnP should flag Channel B as diverged and fall back cleanly (Phase 1.5 / manual) rather than return silent garbage.
- **< 6 GCPs resolved:** assert the script exits with a named error identifying which GCPs are missing, not a numerical failure inside pyorc.
- **Orphaned photo label (GCPunknown):** assert the parser logs a warning, skips the photo, does not assign it to any GCP.
- **GCP15 gap:** assert the gap is flagged in audit JSON, does not crash on `None` lookup.

### 9.4 Determinism

`cv2.solvePnP` with fixed initial rvec/tvec is deterministic; wrapper takes the seed from CLI to keep tests reproducible. MAGSAC RANSAC uses a `cv2.setRNGSeed` call at driver start.

Assertions are structural, not exact-set:
- `|S*| >= 6`
- `rmse(S*) <= rmse(S_full)`
- `S*` contains ≥ 1 near-bank and ≥ 1 far-bank GCP
- Running the full pipeline twice produces byte-identical outputs

### 9.5 Harness

- New `survey/tests/pytest.ini` with `testpaths = survey/tests`.
- Every UI-touching module (detector, `orc_auto_fit.py`) accepts `headless=True`; tests always pass it.
- Manual-click fallback uses an injectable `click_provider` callable; tests inject `lambda gcp_id: gt_clicks[gcp_id]` to simulate a perfect human clicker.
- Existing `orc_build_camera_config.py --dry-run` becomes a proper pytest entry via `main(["--dry-run", ...])`.

## 10. Decision record

- **2026-04-21 (v0.1):** Designed post-spike. Hybrid registration+projection chosen over photo-only or projection-only after the GCP1 failure in §4.2 showed neither channel is sufficient alone.
- **2026-04-21 (v0.2):** Applied four agent-review recommendations.
  - Dropped Stage 1 global detection in favour of project-then-detect-locally (Plan critique — bootstrap pose is strong enough that windowed detection is simpler and more robust than global).
  - Photo labelling demoted from co-primary channel to conditional Phase 1.5 pose-prior (Plan critique — photos aren't load-bearing for the MVP if the bootstrap pose already produces ±50 px windows).
  - PnP switched to `cv2.solvePnPRansac(flags=cv2.USAC_MAGSAC)` (researcher recommendation — MAGSAC++ soft-weighting handles Gaussian survey noise better than hard-threshold RANSAC, and pyorc itself does no outlier rejection per Explore review).
  - Replaced soft spread/count penalties with hard constraints (Plan — tuneable λ nobody tunes is worse than a one-line floor).
  - Fixed metric units: pyorc reports metres, not pixels (Explore — `pyorc/cv.py:1195-1206`).
  - Subset-search inner loop bypasses pyorc's calibration machinery (Explore — `set_gcps` can trigger `optimize_intrinsic` → seconds per subset; `cv2.solvePnP` directly with frozen intrinsics → ~1 ms).
  - Byte-equal round-trip requires explicit intrinsics in the output CameraConfig (Explore).
  - A1 tightened from 10 px to 5 cm in world-ground units (user directive — matches the spirit of the physical-floor framing and gives us a meaningful pass/fail before committing to Phase 1.5).
  - Test strategy re-scoped per test-engineer plan (versioned fixtures, synthetic scene generator, negative tests for re-survey signalling, `pytest.ini`).
- **2026-04-21 (scope clarification):** Explicitly one-shot. Sukabumi-only. Removed "should work on Jakarta with inputs swapped" from §3 soft constraints. Reframed §2 motivation around subset-search feasibility rather than reusability. Once Sukabumi is calibrated or declared unsalvageable, this code is legacy — no investment in maintainability beyond that.
- **2026-04-21 (scope clarification, addendum):** Removed all prescriptive content about how other sites should conduct their surveys or select markers. Methodology for other sites is being handled in separate deployment planning and is explicitly out of scope for this document.
- **2026-04-21 (demo-override):** Added `--demo-override` as a hard constraint in §3 and a dedicated subsection §5.4. Default behaviour when A2 fails is still "refuse and exit non-zero." With the flag, the tool writes an uncertified CameraConfig labelled `_DEMO_UNCERTIFIED` in filename and `certification_status: "demo-only"` in-config, accompanied by a disclaimer-banner report. Purpose: demonstrate the end-to-end OpenRiverCam pipeline (velocimetry, dashboards, training) at Sukabumi before re-survey completes. The override does not bypass A1 (registration) — only A2 (calibration quality). A follow-on (out of scope for this design) wires downstream consumers to refuse flow-rate publication when `certification_status == demo-only`.

## 11. Out of scope

- Velocimetry (the ORC pipeline past `CameraConfig`). This work ends at the `CameraConfig` object.
- Multi-frame fusion beyond Stage 1's optional frame averaging.
- **ArUco / AprilTag auto-detection for the Sukabumi 2026 dataset.** The markers were already physical X-marks and checker tiles by the time this design was written; they can't be retrofitted.

### Methodology for other sites is out of scope

Per 2026-04-21 scope clarification: this design is a one-shot for Sukabumi only. Any approach for other sites — whether ArUco fiducials, different survey methodology, or something else — is being handled in separate deployment planning and is not prescribed here. The SOTA review (`/tmp/auto_fit_review/sota_research.md`) is retained for reference only; it was used to confirm that *our Sukabumi approach* is not reinventing an off-the-shelf tool, not to recommend directions for other sites.

## 12. Cross-references

- `ORC_FIT_STRATEGY.md` — physical-floor formula, drop-one loop, geometric-spread rules. This design implements its manual prescriptions in code.
- `ORC_OS_DOCKER.md` — target environment for the output config.
- `NEXT_SESSION_PLAN.md` — resume-cold summary; will point to this file during the build.
- `spring_2026_ID/survey_data/20260421_rerun_plan.md` — the correction pipeline that produces the `output/` inputs to this system.
- Agent-review artefacts (transient): `/tmp/auto_fit_review/sota_research.md` (committed summary in §11), reviewer reports synthesised into §10 decision record.
- Spike artefacts (transient): `/tmp/auto_fit_spike/`.
