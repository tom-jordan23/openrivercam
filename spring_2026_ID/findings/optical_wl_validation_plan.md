# Validation plan: Sukabumi daytime optical water-level failure

**Companion to:** [`optical_wl_daytime_glint.md`](optical_wl_daytime_glint.md) (the finding this plan tests).
**Owner:** Tom Jordan.  **Assist:** Claude.  **Opened:** 2026-07-14.  **Status:** DRAFT — not yet started.

> Purpose: turn the current *hypothesis* (daytime optical WL fails; leading causes specular
> sun-glint in the afternoon and mist in the morning; likely seasonal) into a *validated,
> predictive* understanding with a defensible mitigation path. This is a multi-session effort;
> we work from this plan and record results inline as we go.

---

## 0. What we are trying to establish (exit definition)

The effort is "done" when we can answer all four:

1. **When** did daytime failures begin, and is the onset **seasonal** (tracks solar geometry) or a
   **discrete regression** (a datable event)?
2. **What** is the physical mechanism of each daytime failure peak (afternoon vs morning)?
3. **Can we predict** it — reproduce the observed pattern from camera geometry + sun position and
   forecast how it evolves over the coming months?
4. **What mitigation** is warranted, and is it validated to work *across seasons* (not just now)?

---

## 1. Hypotheses under test

| id | Hypothesis | Primary prediction | Would be refuted by |
|----|-----------|--------------------|---------------------|
| **H1** | Afternoon peak (15–17 WIB) = **specular sun glint** into the NW-facing camera | Failing pm frames show a saturated specular hotspot on the water where S/N collapses; fails when sun is low & in NW; absent on overcast pm | No hotspot; fails equally on overcast pm; S/N collapse uniform not localized |
| **H2** | Morning peak (08–12 WIB) = **valley mist/fog** (not glint) | Failing am frames show low-contrast whiteout/veiling across the scene, no hotspot; correlates with clear calm nights (radiation fog) | am frames show a specular hotspot (→ also glint); no veiling; uncorrelated with night conditions |
| **H3** | The pattern is **seasonal** (sun declination) | Afternoon failure rate peaks ~May–Aug, fades Nov–Feb as sun leaves the NW; onset tracks declination | Failures constant year-round, or step-change on a single date |
| **H0** | Null / alternatives | — | Threshold mis-set (refuted in finding §E1), wrong search band (refuted §E2), lens fouling / camera nudge / water-level drop (a datable step, tested in V1) |

These are **not** mutually exclusive — the expected outcome is H1+H2+H3 together. H0 alternatives are the things we must actively rule out.

---

## 2. Inputs already established (from the finding)

- **S/N statistics:** DONE median 4.0 (min 2.0) vs ERROR max 1.98 — bimodal; gate `s2n_thres 2.0`
  well-placed. Same detected h (~614.8 m) in both → right waterline, low confidence.
- **Timing:** failures bounded by daylight (station clock verified UTC); twin peaks 08–12 & 15–17
  WIB, dip at solar noon.
- **Camera geometry (derived from camera_config id 3):** faces **~313° (NW)**, depression **~54°**,
  ~4.5 m above water, ~3 m range. *(Bearings only — no coordinates recorded here.)*
- **Solar geometry (site ~6.9°S):** noon sun is NORTH of the station late-Feb→mid-Oct, peaking
  ~30° N of zenith at the Jun solstice; afternoon sun crosses the camera's 313° azimuth at low
  elevation only around May–Aug. Sun is in the southern sky (never NW) Nov–Feb.

---

## 3. Prerequisites / tooling gaps (build before the phase that needs them)

| id | Need | For | Status |
|----|------|-----|--------|
| **P1** | `orc_gather_logs.py`: bulk **list-only** mode — page ALL videos, record id/timestamp/status (no per-video log fetch) | V1 timeline | ☐ to build |
| **P2** | `orc_gather_logs.py`: **frame/video fetch** mode for a given id list (first-frame JPEG is enough) | V2 pixel test | ☐ to build |
| **P3** | Retrieve the **PROD reprocess commit log** `reprocess_commit_<stamp>.jsonl` from the LiveORC AWS box (`docker cp liveorc_webapp:/tmp/orc-reprocess-logs/. …`, or per `prod_reprocess.sh`). The prod reprocess (done on LiveORC) re-detected optical WL with `h_a=None` on the ~1,297 historical videos → each record carries timestamp + status (`ok` = WL succeeded / `pyorc_error` = WL failed). **Local dry-run logs are insufficient** (28 videos, 2026-05-16 only, no re-detection: `new.h==old.h`). | V1 baseline | ☐ pull from AWS |
| **P4** | Sky-state proxy: on-station rain gauge log, and/or in-frame hard-shadow detector | V4 | ☐ decide source |

All station-side tools stay **read-only**. Derived datasets committed must remain **coordinate-free**
(raw bundles carry private UTM survey coords — never commit them).

---

## 4. Phases

Ordered by information-value ÷ cost. Each phase has a **decision gate**; we stop and talk at each.

### V0 — Verify the camera pose (gate for everything geometric) ✅ RESOLVED 2026-07-14
- **Question:** is the derived orientation (313° NW / 54° depression) correct, and was it the
  **same** on the pre-Fit 6 unit (or re-aimed at the swap)?
- **Result:** camera faces **~313° (NW)**, depression **~54°**, derived from *surveyed* coords —
  the camera sits at surveyed point C and the GCPs are physical points it imaged (they carry
  row/col), so it must look C→GCPs; this is convention-free and authoritative. UTM grid→true-north
  convergence at the site is −0.23° (negligible), so 313° is a true-north bearing. **Stakeholder
  confirms the camera did not move during or since the Fit 6 swap** → no re-aim confound for V1.
- **Caveat (parked for V3):** interpreting `camera_rotation` (rvec) as the cv2 world→camera vector
  gives azimuth ~188°, disagreeing with the geometry's 313° (depressions agree, ~49° vs ~54°). The
  geometry wins for *facing direction*; the rvec **rotation convention must be pinned down before
  V3** projects the glint point into the image.

### V1 — Onset & baseline: did it work before? (answers Q1) ☐
- **Question:** reconstruct daytime optical-WL failure rate over time; is onset seasonal or a step?
- **Primary data source (best):** the **PROD reprocess commit log** (P3) — the pre-Fit 6 history
  re-scored with the *current* recipe (`h_a=None`, same optical-WL detection the station runs), so
  `status` per record = WL succeeded (`ok`) / failed (`pyorc_error`). This is a **same-algorithm**
  seasonal baseline — it controls for "did the pipeline change" (it didn't; the same code scored
  both eras).
- **Method:**
  - ☐ P3: parse the prod commit log → per-video timestamp + WL success/fail; confirm the failures
    carry the "Could not estimate water level" signature (vs unrelated velocimetry errors).
  - ☐ Combine with the current live-station ERROR/DONE sets (already pulled) for the Fit-6 era.
  - ☐ Per-day failure rate, split **morning (06–12)** and **afternoon (12–18)** WIB; overlay solar
    declination and the sunset-azimuth-vs-313° track.
  - ☐ (Optional P1) station-DB full history to extend/confirm the Fit-6-era tail.
- **Output:** a failure-rate-vs-date chart (am/pm split) spanning the reprocessed history → now.
- **Gate:**
  - Onset **tracks the sun going north / sunset entering the NW** → seasonal (H3 supported); proceed.
  - **Step change on a single date** → a discrete regression (H0); pivot to find that event
    (lens, camera nudge, water-level drop, recipe/capture-config change) before seasonal modelling.
  - **Persistent failures across the whole reprocessed span** (if it only covers ~May–Jun, all near
    the solstice, i.e. all "bad-glint" months) → consistent with a seasonal May–Aug problem but with
    little transition *leverage*; lean on V3 (model) + V5 (forward monitoring) for the seasonal
    swing, and say so. **First check the history's actual date span** (open question §9).

### V2 — Split frame-level proof (answers Q2; tests H1 & H2) ☐
- **Question:** does each peak show its own predicted signature?
- **Method:**
  - ☐ P2: fetch frames for a matched set — failing **~09:00** (H2), failing **~16:00** (H1),
    passing **~13:00** (control), passing **night** (control). A few of each for robustness.
  - ☐ In the water-surface band, measure: saturated/near-white pixel fraction (glint marker) and a
    global contrast/veiling metric (mist marker). Compare across the four groups.
  - ☐ Where possible, overlay where pyorc's S/N collapses and check it coincides (afternoon) with
    the bright patch.
- **Output:** annotated frames + a small metrics table.
- **Gate:** afternoon hotspot present & morning veiling present → H1+H2 confirmed. If afternoon has
  no hotspot → H1 refuted, rethink. If morning also shows a hotspot → mornings are glint too.

### V3 — Physical glint model (answers Q3; predictive) ☐
- **Question:** can we reproduce the afternoon peak from first principles and forecast it?
- **Method:** from the verified pose (V0) + FOV + a water-roughness/Fresnel glitter model, compute
  per (day-of-year, time) whether the specular glitter patch enters the FOV and its image location.
  - ☐ Validate: does it reproduce the observed 15–17 WIB afternoon peak for the July data window?
  - ☐ Forecast: run it forward to Dec — does it predict the afternoon rate fading by ~Oct–Nov?
  - ☐ Byproduct: predicted **image location** of the glint patch per time (enables masking).
- **Output:** a glint calendar + per-capture glint-in-FOV flag; validation against V1/V2.
- **Gate:** model reproduces observed afternoon timing → trust its forecast & drive V5 expectations
  and the masking mitigation. Poor fit → water-roughness assumptions wrong; revisit.

### V4 — Overcast natural experiment (fast causal check for H1) ☐
- **Question:** does the afternoon failure need direct sun (glint) vs happen regardless (mist/other)?
- **Method:** ☐ P4 sky-state proxy → compare afternoon failure rate on **clear** vs **overcast**
  days. Glint (H1) requires direct sun; mist (H2) and geometry do not.
- **Output:** afternoon failure rate stratified by sky state.
- **Gate:** overcast afternoons **pass** → strong causal support for H1. Fail equally → afternoon
  cause is not (only) glint.

### V5 — Forward seasonal monitoring (the decisive experiment; answers Q3) ☐
- **Question:** do the two peaks follow the predicted, *different* seasonal curves?
- **Method:** ☐ weekly am/pm daytime failure-rate tracking from now → past the Sep equinox into
  Nov, plotted against the V3 forecast and fog climatology.
- **Output:** running seasonal curves, am vs pm, vs model.
- **Gate:** afternoon rate declines as sun leaves the NW **and** morning rate follows fog season
  (not sun azimuth) → H1+H2+H3 confirmed. This also tells us if/when a durable fix is needed before
  next May.

---

## 5. Decision flow (how the phases branch)

```
V0 pose ok? ──no──> fix model/interpretation first
   │yes
V1 onset seasonal? ──step-change──> hunt discrete regression (lens/nudge/water-level) ──> re-enter
   │seasonal (or insufficient history)
V2 signatures match? ──afternoon:no hotspot──> H1 refuted, rethink afternoon
   │afternoon hotspot + morning veiling
V3 model reproduces pm peak? ──no──> revisit roughness/FOV assumptions
   │yes → forecast + glint-region prediction
V4 overcast pm passes? (fast causal confirm of H1, can run parallel to V3)
   │
V5 seasonal curves diverge as predicted → CONFIRMED → choose & validate mitigation
```

## 6. Mitigation options (evaluate only after mechanism is confirmed; must validate across seasons)

- Glint-robust WL preprocessing (both recipe passes are plain `grayscale` = glint-sensitive).
- Predictive glint-region **masking** using V3's per-time image-location output.
- **Fallback h** for captures flagged glint-in-FOV (river is stable; good reads bracket the window)
  to preserve daytime *discharge*.
- Scheduling / down-weighting of known-bad windows.
- Physical (sunshade/polarizer) — impractical on the sealed C1200; note and park.
- **Note:** if seasonal, the problem partly self-resolves by Nov but returns each May — a durable
  fix is still warranted, and any fix must be re-validated in a *different* season.

## 7. Confounders to control

- ~~Camera re-aimed at the Fit 6 swap~~ — **cleared** (V0: stakeholder confirms no movement).
- **Pre/post-Fit 6 capture-config comparability** — the reprocess scores *old imagery* with the new
  recipe, but if the pre-Fit 6 camera model / exposure / resolution / IR settings differed, imagery
  characteristics (hence S/N) could differ independently of season. Confirm the camera and capture
  settings were unchanged across the swap.
- Reprocess `status` semantics — confirm `pyorc_error` on a historical video means the *WL* step
  failed (our signature), not a downstream velocimetry error; the runbook's "recovered/errored"
  wording refers to discharge salvage, which is not the same thing.
- LiveORC data gaps may reflect upload/comms outages, not WL failures — cross-check against known
  outage windows (see sensor-upload memories) before reading a gap as a failure.
- Dry-season clear skies raise *both* glint (direct sun) and radiation fog — don't attribute both
  peaks to one cause.
- Water level itself changes seasonally (dry season) — a lower/rougher surface could shift S/N
  independently of sun; V3/V2 should watch for it.
- Sampling caps in the gather tool (100-most-recent) — use P1 full-history paging for rates.

## 8. Results log (fill inline as phases complete)

- V0 — ✅ **done (2026-07-14):** camera faces ~313° NW, ~54° depression, from surveyed coords;
  confirmed not moved across Fit 6. rvec rotation-convention mismatch parked for V3.
- V1 — _pending_ — data source identified: prod reprocess commit log on the LiveORC box (P3).
- V2 — _pending_
- V3 — _pending_
- V4 — _pending_
- V5 — _pending_

## 9. Open questions

- **What is the date span of the reprocessed history?** (~1,297 videos; sample seen is 2026-05-16.)
  If it only covers ~May–Jun it's all near the solstice → limited seasonal-transition leverage for
  V1. This is the first thing to check when the prod log is in hand. (bounds V1)
- ~~Did the Fit 6 swap change camera position/aim?~~ — **answered: no** (V0).
- Was the camera model / capture config unchanged across the Fit 6 swap? (V1 confound)
- Does the prod reprocess `pyorc_error` reliably encode a *WL-detection* failure? (sets V1 method)
- Water-roughness input for V3 — measurable from the video, or assume a range?
