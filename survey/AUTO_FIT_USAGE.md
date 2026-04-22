# Auto-fit Usage Guide

How to run the Sukabumi salvage pipeline end-to-end. For the design rationale see `AUTO_FIT_DESIGN.md`; for the plain-language narrative see `Sukabumi_survey_salvage_methodology.md`.

**Scope:** this tool is a one-shot salvage pipeline for the Sukabumi 2026 survey. It is not supported infrastructure for other sites (see `Sukabumi_survey_salvage_methodology.md` Decision 5).

---

## 1. One-time setup — Phase 0 (ground-truth clicks)

The pipeline needs a fixture with an operator's manual pixel clicks for each GCP. This is a ≈30 min, one-time task per dataset.

```bash
bash /Users/tjordan/code/git/openrivercam/survey/auto_fit/run_phase0.sh
```

That opens a matplotlib window showing frame 0 of the calibration video with each surveyed GCP's ID prompted one at a time. Controls:

| Key / mouse | Action |
|---|---|
| left-click | record pixel for current GCP |
| scroll-wheel | zoom in/out at cursor (use liberally for sub-pixel accuracy) |
| `n` or space | advance to next GCP |
| `b` | go back |
| `u` | undo current GCP's click |
| `s` | mark current GCP as not visible / skip |
| `q` | save and exit |

Output lands at `survey/tests/fixtures/sukabumi_gt_clicks_v1.json`. Versioned filename by convention: if the GCP set changes, save as `_v2`; never overwrite `_v1`.

---

## 2. Running the fit — the common case

Normal salvage run (gate passes, emits a certified CameraConfig):

```bash
cd /Users/tjordan/code/git/openrivercam
source .venv/bin/activate

python3 survey/orc_auto_fit.py \
    --video spring_2026_ID/survey_data/source_data/20260420T034813.mp4 \
    --gcps spring_2026_ID/survey_data/output/gcps.csv \
    --camera-position spring_2026_ID/survey_data/output/camera_position.csv \
    --water-level spring_2026_ID/survey_data/output/water_level.csv \
    --gt-clicks survey/tests/fixtures/sukabumi_gt_clicks_v1.json \
    --use-clicks survey/tests/fixtures/sukabumi_gt_clicks_v1.json \
    --subset-search \
    --site sukabumi \
    --tag <short_tag_for_this_run>
```

Key flags:

- `--use-clicks`: bypass auto-detection, use the operator's manual clicks (from Phase 0) verbatim. This is the path that has proven to pass the 5 cm gate on the Sukabumi data. The auto-detector remains in the codebase but snaps to cobbles on this scene (see `AUTO_FIT_DESIGN.md` §4.1 and the 2026-04-21 dry-run findings).
- `--subset-search`: run Stage 3 — enumerates all 6+ GCP subsets with image-quadrant coverage and picks the lowest-RMSE winner.
- `--water-level`: required to emit the CameraConfig. Without it, the driver stops at the report and labels file.
- `--tag`: short label for this run; appears in the output directory name so multiple iterations never collide.

**Outputs land under:**

```
spring_2026_ID/survey_data/auto_fit_runs/<timestamp>_<site>_<tag>/
    frame.png                    # the pinned video frame used for the fit
    frame.sha256                 # provenance hash
    annotated.png                # frame annotated with GT clicks, detections, residual vectors
    gcp_support.png              # per-GCP diagnostic bar chart
    report.md                    # human-readable summary with all plots embedded
    clicks.json                  # manual-path compatible click file
    labels.json                  # per-GCP pixel + residual record
    detections_by_pass.json      # stage 2 windowed detection trace
    audit.json                   # full decision log
    sukabumi_autofit_camera_calibration.json       # ← pyorc CameraConfig, ORC-OS-loadable
    sukabumi_autofit_camera_calibration_cert.json  # sidecar: certification_status, override metadata
```

The two JSONs at the bottom are the operational handoff: drop them into ORC-OS or keep them next to the deployed station.

---

## 3. When the gate fails — demo-override

If the best-subset RMSE exceeds `--a1-target-m` (default 5 cm), the driver **refuses by default** and exits non-zero. Re-survey is the correct answer for a certified fit.

For stakeholder demos, training, or downstream-pipeline bug triage where a rough calibration is enough, use `--demo-override`:

```bash
python3 survey/orc_auto_fit.py \
    ... (same flags as above) ...
    --demo-override \
    --override-reason "PMI walkthrough of velocimetry pipeline, 2026-04-22"
```

Differences in demo mode:

- CameraConfig filename becomes `sukabumi_autofit_camera_calibration_DEMO_UNCERTIFIED.json`.
- Sibling cert file has `certification_status: "demo-only"` plus the override reason, the invoking user, a UTC timestamp, the actual RMSE, and the gate that was exceeded.
- `report.md` opens with a disclaimer banner: *"DEMO-UNCERTIFIED — do not use for certified flow, discharge, or water-level measurements."*
- `audit.json` records the override as a first-class event.

**The override is loud on purpose.** The filename, JSON field, report banner, and audit entry are four independent signals that this config is not production. The design assumes downstream consumers (velocimetry, dashboard publishing code) will learn to refuse flow-rate publication when they see `certification_status == "demo-only"`. That wiring is out of scope for this pipeline — filename suffix remains the primary safety net until it lands.

**Override does NOT bypass A1 registration failure.** `--demo-override` only relaxes the A2 (calibration-quality) gate. If the automation can't locate markers at all, a demo is not useful — fix that first.

---

## 4. Verifying a run through the manual path

`orc_build_camera_config.py --from-auto <run_dir>` replays the auto-fit's chosen subset through the original manual-click pipeline. This is useful as an independent sanity check — the manual path uses the same `pyorc.CameraConfig` API but without the subset-search and MAGSAC layers, so agreement of the two paths is evidence the fit is not an artefact of the auto-fit's scoring choices.

```bash
python3 survey/orc_build_camera_config.py \
    --video spring_2026_ID/survey_data/source_data/20260420T034813.mp4 \
    --gcps spring_2026_ID/survey_data/output/gcps.csv \
    --water-level spring_2026_ID/survey_data/output/water_level.csv \
    --from-auto spring_2026_ID/survey_data/auto_fit_runs/<RUN_DIR> \
    --dry-run
```

The `--from-auto` flag reads `<RUN_DIR>/clicks.json` and filters to the IDs listed in `<RUN_DIR>/audit.json`'s `subset_search.best.ids` (the subset-search winner). If the audit file is missing or the run didn't include `--subset-search`, it falls back to using every click in the file.

Drop `--dry-run` to emit a real CameraConfig JSON via the manual path.

## 5. Iterating — multiple runs

Every run writes to its own timestamped subdirectory. To compare two runs:

```bash
diff -u \
  spring_2026_ID/survey_data/auto_fit_runs/<run_A>/report.md \
  spring_2026_ID/survey_data/auto_fit_runs/<run_B>/report.md
```

Deterministic: same inputs + same flags → identical outputs (RNG seeds are pinned; see `--rng-seed`).

Useful knobs to twiddle between iterations:

- `--a1-target-m` — quality gate (default 0.05 = 5 cm). Tighten to see how many subsets survive at 2 cm, 3 cm, 4 cm.
- `--min-subset-size` — default 6 per `ORC_FIT_STRATEGY.md` §5. Can't be lowered below 6 without losing geometric constraint, but can be raised for conservative fits.
- `--exhaustive-below-n` — cap on when the exhaustive pass kicks in; default 15. Useful when the greedy result is still large (e.g. 17 GCPs).
- `--focal-px` — bootstrap focal length. Only used when `--bootstrap-from-gt` is not set and `--use-clicks` is not set, i.e. in pure auto-detect mode. With `--use-clicks`, pyorc computes the intrinsics from the clicks + UTM pairs directly.
- `--reprojection-px` — MAGSAC RANSAC threshold. At ~90 cm survey noise, loose thresholds (50–200 px) keep more points in; tight thresholds (5–10 px) eliminate survey-noise points.

---

## 6. Loading into ORC-OS

The station Docker must be running (see `survey/ORC_OS_DOCKER.md`).

```bash
# bring up the station
cd rainbow-sensing/orc-os && docker compose up -d

# wait for orc-api healthy
sleep 15

# persist our config as a named camera config in the DB
CFG=<absolute path to sukabumi_autofit_camera_calibration.json>
python3 -c "
import json
data = json.load(open('$CFG'))
data.pop('certification_status', None)
data.pop('resolvability_note', None)
print(json.dumps({
    'name': 'Sukabumi auto-fit salvage (6-GCP)',
    'height': data['height'], 'width': data['width'],
    'data': data,
}))
" | curl -sS -X POST http://localhost:3001/api/camera_config/ \
    -H 'Content-Type: application/json' -d @- -w '\nHTTP %{http_code}\n'
```

Expected response: HTTP 201, new camera config with `id` assigned in the DB. The intrinsics (`camera_matrix`, `rvec`, `tvec`) will show as `null` in the saved record — that's normal; ORC-OS computes them on demand when you hit the Fit button in the dashboard.

Verification — run the ORC-OS fit and confirm it produces a sane RMSE:

```bash
curl -sS -X POST http://localhost:3001/api/control_points/fit_perspective \
  -H 'Content-Type: application/json' \
  -d '{"gcps":{"control_points":[...from data.gcps...],"z_0":617.065,"crs":32748},"height":1080,"width":1920}' \
  | python3 -m json.tool
```

On the Sukabumi salvage subset, the ORC-OS fit produces RMSE ≈ 5.1 cm (our pipeline's number is 4.6 cm; the small gap is because ORC-OS also optimises focal length, which we froze).

---

## 7. Troubleshooting

**"CameraConfig.__init__() got an unexpected keyword argument 'certification_status'"** — you loaded the raw JSON via `pyorc.load_camera_config()`. That loader rejects unknown top-level fields. The certification metadata lives in the `*_cert.json` sibling file precisely to avoid this — the main JSON is a pure pyorc config.

**Matplotlib window doesn't appear during Phase 0** — matplotlib's macOS backend needs a desktop session. Via SSH, fall back to TkAgg (`MPLBACKEND=tkagg ...`) or run the clicker on a local machine with an X display.

**`dist_coeffs` shape error (`IndexError: list index out of range`)** from ORC-OS — the config was emitted with `dist_coeffs` as a 1×5 row vector. This pipeline emits as 5×1 column per ORC-OS's schema. If a config fails here, it was emitted by an older version of `orc_auto_fit.py`; re-run with the current code.

**`--demo-override` without `--override-reason`** — the tool exits with an explicit error. Supply a meaningful reason (stakeholder ID, test purpose, incident ticket) so the audit log is useful.

**Subset search finds no valid subset (empty greedy trajectory)** — hard constraints are likely blocking. Check whether every image quadrant has at least one clicked GCP. If not, the `require_all_quadrants` constraint rejects all subsets.

**RMSE looks impossibly low (< 1 mm) on a 4-GCP fit** — this happens when MAGSAC finds a self-consistent 4-GCP subset among many noisy GCPs. The RMSE is real arithmetically but the fit may be geometrically wrong. Run `--subset-search` to force ≥ 6 GCPs and engage the geometric-spread constraint; the honest RMSE will typically be higher but the fit is trustworthy.

---

## 8. Cross-references

- `AUTO_FIT_DESIGN.md` — technical design + decision record.
- `Sukabumi_survey_salvage_methodology.md` — plain-English walkthrough, for non-specialist readers.
- `NEXT_SESSION_PLAN.md` — state at last session, what to resume with.
- `ORC_FIT_STRATEGY.md` — manual residual analysis, physical floor formulas, drop-one rules.
- `ORC_OS_DOCKER.md` — docker station setup, ports, patches.
- `spring_2026_ID/survey_data/20260421_rerun_plan.md` — correction pipeline that produces the inputs to this tool.
- `spring_2026_ID/survey_data/corrections.md` — append-only survey-correction log.
