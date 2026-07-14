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
| **P3** | LiveORC query path (server per `reference_liveorc_server` memory): historical daytime result density for the **pre-Fit 6** period | V1 baseline | ☐ confirm access |
| **P4** | Sky-state proxy: on-station rain gauge log, and/or in-frame hard-shadow detector | V4 | ☐ decide source |

All station-side tools stay **read-only**. Derived datasets committed must remain **coordinate-free**
(raw bundles carry private UTM survey coords — never commit them).

---

## 4. Phases

Ordered by information-value ÷ cost. Each phase has a **decision gate**; we stop and talk at each.

### V0 — Verify the camera pose (gate for everything geometric) ☐
- **Question:** is the derived orientation (313° NW / 54° depression) actually correct, and was it
  the **same** on the pre-Fit 6 unit (or was the camera re-aimed at the swap)?
- **Method:** (a) sanity-check pose against a real frame (does "up-left in image" map to the
  expected compass direction?); (b) confirm intended aim from install notes/photos; (c) note
  whether the Fit 6 swap changed camera position/aim (a confound for V1 history).
- **Output:** confirmed azimuth/depression ± uncertainty; a yes/no on "aim changed at swap."
- **Gate:** if pose is wrong or aim changed at the swap → revise the geometric model and the V1
  interpretation before proceeding.

### V1 — Onset & baseline: did it work before? (answers Q1) ☐
- **Question:** reconstruct daytime optical-WL failure rate over time; is onset seasonal or a step?
- **Method:**
  - ☐ P1: pull the full video history from the station DB → per-day counts of DONE vs ERROR,
    split by **morning (06–12)** and **afternoon (12–18)** WIB.
  - ☐ P3: for the pre-Fit 6 months, use LiveORC — plot **density of successful daytime results
    per day** over the prior months (daytime gaps = failures, since only successes upload).
  - ☐ Overlay solar declination (and sunset azimuth relative to 313°) on the failure-rate timeline.
- **Output:** a failure-rate-vs-date chart (am/pm split) spanning as far back as data allows.
- **Gate:**
  - Onset **tracks the sun going north / sunset entering the NW** → seasonal (H3 supported); proceed.
  - **Step change on a single date** → a discrete regression (H0); pivot to find that event
    (lens, camera nudge, water-level drop, recipe change) before any seasonal modelling.
  - Too little history (only ~3 weeks; unit deployed 2026-06-24) → rely on V3+V5 (model + forward
    monitoring) instead, and say so explicitly.

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

- Camera re-aimed at the Fit 6 swap (V0) — would break V1 history continuity.
- LiveORC "gaps" may reflect upload/comms outages, not WL failures — cross-check against known
  outage windows (see sensor-upload memories) before reading a gap as a failure.
- Dry-season clear skies raise *both* glint (direct sun) and radiation fog — don't attribute both
  peaks to one cause.
- Water level itself changes seasonally (dry season) — a lower/rougher surface could shift S/N
  independently of sun; V3/V2 should watch for it.
- Sampling caps in the gather tool (100-most-recent) — use P1 full-history paging for rates.

## 8. Results log (fill inline as phases complete)

- V0 — _pending_
- V1 — _pending_
- V2 — _pending_
- V3 — _pending_
- V4 — _pending_
- V5 — _pending_

## 9. Open questions

- How far back does station/LiveORC history actually go for Sukabumi? (bounds V1)
- Did the Fit 6 swap change camera position/aim? (V0)
- Does LiveORC record failures, or only successful results? (sets the V1 method)
- Water-roughness input for V3 — measurable from the video, or assume a range?
