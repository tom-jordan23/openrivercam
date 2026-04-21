# Methodology: Automated Camera Calibration for OpenRiverCam (Sukabumi, Spring 2026)

**Purpose:** Explain the approach we are taking to calibrate the camera at the Sukabumi site from the existing survey data, and the plan for building the automation that does this work.

**Audience:** The deployment team (PMI staff, hydrologist, software helper). Written to be readable end-to-end without deep photogrammetry or computer-vision background. Undergrad CS knowledge (matrices, algorithm complexity, Gaussian noise, hash functions) is assumed. Domain-specific terms — GCPs, UTM, PnP, RMSE, RANSAC, SIFT, ArUco — are expanded inline the first time they appear and defined more fully in **Appendix A (§12)**.

**Date:** 2026-04-21. This document will change as we learn more during Phase 1 and Phase 2 (see "Roadmap" below).

**Scope — one-time salvage for Sukabumi 2026 only.** This pipeline exists *only* because the Sukabumi 2026 survey data is noisier than planned and the markers are already physically placed. It is built once, for this dataset, and the design is judged against that scope — not against any notion of reusability. How future sites avoid ending up in the same situation is out of scope for this document.

---

## 1. What problem are we solving?

OpenRiverCam measures river flow by watching the water surface in a camera. For those measurements to be in real physical units (metres per second, cubic metres per second), the software needs to know where the camera is and where it is pointing. This is called **camera calibration**.

Calibration works by matching things we can see in the video (pixels on the screen) to things we measured on the ground (GPS positions in **UTM** coordinates — *Universal Transverse Mercator*, a projected system measured in metres rather than latitude/longitude; see §12). The things we measure on the ground are called **Ground Control Points** (GCPs). At Sukabumi we placed 20 GCPs — black-and-white checkerboard tiles and painted X-marks — on the riverbanks and in the water channel, then surveyed each one with a GPS rover.

The calibration step answers the question: *"given these 20 points in the video and these 20 GPS positions on the ground, where is the camera and which way is it pointing?"* In photogrammetry this is called the **Perspective-n-Point** or **PnP** problem. Given the camera's internal parameters (focal length, lens distortion) and `n` known 3D-to-2D correspondences, PnP solves for the camera's rotation `R` and position `t` — six unknowns in total (three for orientation, three for position). OpenCV provides `cv2.solvePnP` as the standard solver. Appendix A (§12) walks through the math in more detail.

Once we can answer that, the software can turn pixel motion in the video into flow rate.

---

## 2. Why is this harder than it should be?

Two problems with the survey data we have:

**Problem 1 — The GPS survey has more error than planned.** On a good day, **RTK** (*Real-Time Kinematic*) GPS gives centimetre-level accuracy. RTK works by having a stationary base station at a known location that continuously transmits position-correction data to a moving rover — most of the common-mode GPS errors (ionospheric delay, satellite clock drift) cancel out on the rover side. At Sukabumi, the **check-point comparison** — the same physical point surveyed twice at different times — shows about 99 cm horizontal and 139 cm vertical spread. Those two measurements should have been identical. That is roughly **30×** worse than our 3 cm / 4 cm target and points to a problem with the base-station setup or the rover fixes. A re-survey with better equipment is already planned, but we do not want to wait for it before starting — partly to make progress, partly because the re-survey will benefit from what we learn now.

**Putting those numbers in perspective.** To give the team a physical feel for the distances involved:

| Length | Roughly as big as | In our context |
|---|---|---|
| 3 cm / 4 cm | AA battery width / paperclip length | The "acceptable" gate for RTK-grade survey work |
| 5 cm | A golf ball | Our per-GCP pixel-registration target for the auto-tool (a different thing from survey accuracy — see §5) |
| 30 cm | A standard ruler | What a consumer-grade GPS (no RTK) typically achieves |
| 90 cm | Adult waist height; one natural stride | Our **actual** horizontal survey noise |
| 139 cm | Chest height on an adult | Our **actual** vertical survey noise |
| 3 m | Length of a compact car | The surveyed cross-section width of the river at our site |
| 20 m | Length of a school bus | The camera's range to the middle of the scene |

Re-scaled to the river itself:

- **A 99 cm horizontal error is about one third of the river's surveyed width (3 m).** That is the error in knowing where the bank *is*, not where the water *is*.
- **A 139 cm vertical error is more than twice the channel's actual water depth.** The cross-section tape measurements show a maximum depth of about 60 cm at mid-flow. The survey's elevation error alone is bigger than the river is deep.
- What this means for the end product: velocity readings from OpenRiverCam depend on both the image (pixels per second) and the calibration (pixels per metre). A 30-% error on the geometry scales directly into a 30-% error on any absolute flow-rate number we publish. For *qualitative* monitoring — "the river is rising," "flow is faster than last hour" — this is tolerable. For *quantitative* discharge estimates (cubic metres per second with a stated uncertainty), it is not.

This is the hard fact behind "salvage mode." Even a perfect calibration cannot improve on a noisy survey — geometry in is geometry out. The purpose of the auto-tool is to find out *how far* we can get with what we have, and to quantify how much a re-survey would buy us.

**Problem 2 — The current calibration process is manual, and the noisy survey makes subset search (trying different GCP combinations) expensive.** Today, the operator opens the video, looks at the first frame, and clicks each of the 20 markers by hand. For a single fit this is fine. But to make an honest *salvage* decision on a noisy dataset, we need to try many different combinations of GCPs to see which subset gives the best fit. Each new combination would require re-clicking every time. Doing that by hand, dozens of times, is impractical — so we automate the clicking so that the subset search itself becomes feasible.

A click log is also hard to audit: we cannot re-verify later that the clicks were accurate. An automated tool leaves a deterministic decision log that the re-survey decision can rest on.

We want to replace the manual cycle with a software tool. The tool will do three things:

1. Find each marker automatically in the video.
2. Try different combinations of markers to find the one that gives the best calibration.
3. Honestly report when the survey data is too noisy to give us a good calibration — telling us the re-survey is necessary, rather than hiding the problem.

Everything the tool does is in service of making a defensible *one-time* decision about the Sukabumi 2026 data. It is not scaffolding for future sites.

---

## 3. What we already did (2026-04-21)

**Survey data corrections pipeline ran successfully.** The field crew returned to the site on Day 2 and captured the missing camera position (called CAM) plus extra GCPs and re-shoots of earlier points. The correction pipeline now produces a complete set of inputs for the calibration step. All corrections are recorded in `spring_2026_ID/survey_data/corrections.md` with SHA-256 hashes of every input file, so any later change to a source file breaks its recorded hash and the audit trail flags it.

**We know the survey is not clean enough for a full-quality calibration.** The pipeline flags the problem clearly: the check-point gate fires with "EXCEEDS GATE" and says to investigate before trusting the data. We kept that warning on purpose — it is the honest signal that the 2026-04-21 dataset is a salvage attempt, not a final result.

**We checked four independent reviews before picking the approach.** Before writing any code for the automation, four specialised reviewers (test strategy, software-library internals, research on existing tools, and architecture) read our first draft and reported back. Their feedback changed several decisions — see "Key decisions" below.

---

## 4. The approach — three stages

The automation has three stages. Each stage does one job and passes its result to the next.

### Stage 1 — Educated guess

We already know, from the survey, where the camera is (CAM). We also know where the 20 GCPs are. The Stage-1 software takes these facts and makes a rough guess about which way the camera is pointing. The guess does not need to be perfect; it only needs to be close enough to narrow the search for each marker.

Concretely, Stage 1 constructs a preliminary **extrinsic matrix** — the rotation `R` and translation `t` that map world coordinates into camera coordinates (see §12 for the pinhole model). We set `t` to the CAM position; point the camera's optical axis at the centroid of the 20 GCPs; and assume the camera is level (zero roll). Combined with the intrinsics (focal length ≈ 1500 px, principal point at image centre, zero distortion as a default), this `(K, R, t)` triple lets us project every GCP's UTM coordinate to a predicted pixel by the standard equation `p ≈ K · (R · X + t)` (up to a projective scale factor — see §12.2).

Output: for each GCP, the approximate pixel on the screen where we expect to see it, plus a search window around that pixel of about ±50 pixels in each direction.

### Stage 2 — Look, detect, refine

For each GCP, Stage 2 looks only inside the small search window from Stage 1. Inside that window the software runs a marker detector: a **Shi-Tomasi corner detector** (a classic algorithm that finds pixel neighbourhoods with large local intensity variation in both directions — i.e., corners and X-junctions) followed by a local "checker-pattern validator" that confirms the four quadrants around each candidate really do alternate dark-light-dark-light. When the validator accepts a candidate, that pixel is recorded as the location of that GCP in the video.

Once Stage 2 has found as many GCPs as it can, it feeds those `(UTM, pixel)` correspondences into **PnP again** — this time using the MAGSAC++ variant of RANSAC (see §12) to automatically reject any correspondence that disagrees with the rest. The surviving "inlier" set produces a better `(R, t)` than the Stage-1 guess. The improved pose is then used to shrink the search windows from ±50 px down to ±20 px, and the detection pass is repeated. After two or three rounds, the inlier set stops changing — the pose has converged.

The important design point here is **"look where we expect to look."** A simpler version of the software was tried first, which ran the marker detector over the whole image. That version produced around 100 possible markers in a frame that has only about 10 real ones — the image is full of contrasty cobbles and wall edges that fool the detector. By looking only in the small windows, we cut that false-positive problem down to essentially zero. This is a deliberate trade-off: we could run a more elaborate detector globally, but a simple detector locally is both faster and more reliable when the pose prior is strong.

### Stage 3 — Try leaving markers out

Not every GCP will be equally reliable. Some were surveyed with a tall bamboo pole (more wobble); some sit in water; some are partly hidden. The "best" calibration does not use all 20 — it uses the subset of GCPs that gives the lowest overall error.

Stage 3 uses a **greedy drop-one search**. At each step it removes the GCP whose removal most reduces the RMSE, then repeats:

1. Start with all GCPs Stage 2 found. Compute **RMSE** — *Root Mean Square Error*, `sqrt( mean( residual_i² ) )`, the standard way to summarise how badly predicted pixels disagree with observed pixels (see §12 for the formal definition). In pyorc the RMSE is reported in world-metres, not pixels, because residuals are un-projected to the ground plane.
2. Remove each remaining GCP one at a time and see which removal drops the RMSE the most.
3. Apply that removal. Repeat.
4. Stop when removing any further GCP would (a) raise the RMSE instead of lowering it, (b) leave fewer than 6 GCPs, or (c) leave one of the image's four quadrants empty.

Conditions (b) and (c) are safety rules. Below 6 GCPs a PnP solve is mathematically underdetermined against noise — the answer gets jumpy. If all the near-bank GCPs are removed, the pose can drift toward the far bank even though the RMSE number looks fine, because the remaining GCPs no longer pin down enough of the geometry to catch that drift.

**Complexity note.** With 20 GCPs there are 2²⁰ ≈ 1,048,576 possible subsets, which is tractable but wasteful. Greedy drop-one is O(n²) PnP solves — about 400 for 20 GCPs — and usually converges in 5–10 iterations. Each PnP solve (with pre-computed intrinsics — see Decision 2) is about 1 ms, so a full greedy search finishes in under a second. If the greedy result has 15 or fewer candidates we also run a full exhaustive check over `C(n, 6) + … + C(n, n)` subsets of that smaller set as a local-optimum sanity check. For n = 15 that is about 32,000 solves, still under a minute.

At the end, Stage 3 reports:

- The chosen subset.
- The RMSE on that subset, in world-metres.
- Every subset that was evaluated and why each was accepted or rejected, in a file called `auto_fit_audit.json` that can be inspected after the fact.

---

## 5. How accurate do we want to be?

The accuracy target for each individual GCP is **5 cm on the ground** — roughly the diameter of a golf ball. This is the distance between where the software places a marker in the video and where the operator would place it by clicking manually. It is effectively a "the tool is as good as a careful human" benchmark.

Converting that to pixels: the camera is roughly 20 m from the centre of the scene (a school-bus length away), and our bootstrap focal length is 1500 px. One pixel on the screen spans `20 m × (1 / 1500) ≈ 1.3 cm` on the ground. So our 5 cm target is about **3.75 px on the screen** — about one human-click's worth of precision. It's tight but within what a careful local detector with sub-pixel corner refinement can achieve on a well-lit marker.

**Crucially, this 5 cm target is a separate thing from the 90 cm survey noise discussed in §2.**

- **Registration accuracy (5 cm):** how well the software's clicking compares to a human's clicking. A test of the automation itself.
- **Calibration quality (90 cm floor):** how well *any* calibration can match reality, given the GPS survey we have as input. A test of the survey.

Even a perfect registration — 0 cm error, every marker landed to the pixel — cannot beat the survey's 90 cm horizontal and 139 cm vertical noise. The "reprojection error floor" (the smallest RMSE any calibration can achieve on this data) works out to `0.9 m / 20 m × 1500 px ≈ 67 px`. That is about **3.5 % of the 1920-px frame width**, or roughly the visible size of one marker tile in the image. That is our ceiling, not our goal.

The question the auto-tool answers is *"how close can we get to that ceiling, and is the ceiling low enough to do useful science?"* Not *"can we beat physics?"* We cannot.

If the tool does not hit 5 cm for most GCPs, we add a backup stage (Phase 1.5 in the roadmap) that uses the photos of each GCP to help the initial guess. Phase 1.5 uses **SIFT** (*Scale-Invariant Feature Transform*, a keypoint detector + descriptor algorithm that finds matching points across images taken at different scales and angles) to align each photo to the video frame via a **homography** (a 3×3 matrix that maps pixels between two views of the same planar scene). See §12 for both terms.

---

## 6. Key decisions and why we made them

These are the choices that shaped the approach above.

**Decision 1 — Start without photos; add them only if we need to.** The field crew took photos of each GCP. Early on we assumed those photos would be central to the automation. The research review showed they are useful but not essential: if the Stage-1 guess is accurate enough, Stage 2 finds the markers without needing the photos. So we build the simpler version first, measure accuracy, and add the photo step only if accuracy is not good enough.

**Decision 2 — Bypass one of the software library's features to keep the subset search fast.** pyorc's `CameraConfig.set_gcps()`, when called without explicit camera **intrinsics** (the 3×3 matrix `K` containing focal length, principal point, and distortion terms — see §12.1), runs a nonlinear optimiser (`scipy.optimize.differential_evolution`) to re-tune those intrinsics from scratch. That step takes a few seconds per call. Stage 3 calls the solver hundreds of times, so that would dominate runtime. We pre-compute the intrinsics once — either from the charuco calibration video when it becomes available, or from the default focal = 1500 px — and hand them into `set_gcps()` up front. The solver then falls through to a direct `cv2.solvePnP` call, about 1 ms. The full subset search runs in under a minute.

**Decision 3 — Use hard limits instead of soft penalties in Stage 3.** The first draft scored each subset with a weighted sum of three terms: error, "spread" (markers on both banks), and count. Soft weights like these need to be tuned, and nobody tunes them. The architecture review suggested replacing the soft penalties with hard rules: never go below 6 markers, never leave a side of the image without a marker. The error is then the only number that gets optimised. This is simpler and easier to audit.

**Decision 4 — The tool must say "re-survey needed" when the data is too noisy.** This is the single most important design decision. We are calibrating on a survey we already know is noisy. The tool must not hide that fact by picking a subset that happens to have low error. If every subset of at least 6 GCPs has high error, the tool will say so in the report and will not write a calibration file. This makes automation honest, not a way to paper over bad data.

**Decision 5 — Scope is Sukabumi only; no investment in reusability.** This pipeline is written once, for this dataset, and is retired after Sukabumi is calibrated (or declared unsalvageable and re-surveyed). We do not design for portability, we do not invest in maintainability beyond the Sukabumi decision, and we do not treat this as a template for other sites. How any future site avoids ending up with noisy survey data is out of scope for this document and will be handled separately.

**Decision 6 — Explicit demonstration-only override for writing a calibration despite noise failure.** Decision 4 is "refuse by default when the data is too noisy." We intentionally pair it with a **deliberate, explicit bypass**: a `--demo-override` flag on the auto-fit CLI that writes a calibration file even when the normal acceptance criteria fail. The override is loud, not quiet:

- The output config JSON has `certification_status: "demo-only"` as a top-level field.
- The output filename has a distinct suffix — `*_DEMO_UNCERTIFIED.json` — so it cannot be confused with a normal fit on the filesystem.
- The accompanying report opens with a bold disclaimer: **This calibration is DEMO-ONLY. It must not be used to compute certified flow rate, discharge, or water-level measurements.**
- The audit JSON records the override flag, who set it, and the timestamp.

**Why we need this bypass.** The OpenRiverCam project has downstream components — velocimetry, report generation, operational dashboards — that we need to be able to demonstrate end-to-end at the Sukabumi site *before* any re-survey happens. Without a camera config, even an uncertified one, nothing downstream runs at all. Demo-mode lets us:

- Show the full pipeline to stakeholders (PMI leadership, funders, field staff) and walk through what the system *will* look like in production.
- Train operators on the full workflow using real site video.
- Catch downstream bugs (in the velocimetry code, the dashboard, the data-upload path) that would otherwise be blocked behind the calibration gate.

**What demo mode is not.** Not a way to publish flow numbers. Not a shortcut. Not something an operator would reach for by accident. The explicit flag + distinct filename + in-config marker + report disclaimer together ensure that any downstream consumer of the calibration — automated or human — sees "DEMO-UNCERTIFIED" at every integration point. A certified flow-rate or water-level number from Sukabumi still requires a successful re-survey and a normal (non-override) calibration run.

---

## 7. How we will know this worked

Three acceptance tests, each with a clear pass/fail line:

**A1 — Marker location accuracy.** At least 70% of the 20 GCPs must be located within 5 cm (golf-ball diameter, roughly 3.75 px on our frame) of a manual click by the operator. The comparison file (`sukabumi_gt_clicks_v1.json`) is the operator's one-time ground truth. Remember this measures the *automation*, not the *calibration* — see §5 for the distinction.

**A2 — Subset search quality.** The subset the software picks must not be worse than a subset picked by hand (same size, same data). "Worse" is measured by the calibration error in metres.

**A3 — Output compatibility.** The calibration file the tool writes must be readable by the OpenRiverCam software without changes. Tested by loading the file back and checking it matches what was written.

If A1 fails, we add Phase 1.5 (photos). If A2 or A3 fail, we fix the bug. If after all of that the error is still much larger than the known survey noise floor, the tool will report "re-survey needed" and we move to the fallback plan.

---

## 8. Risks and what we will do about them

| Risk | How likely | What we will do |
|---|---|---|
| A marker that is only on one side of the image is missed by the detector | Medium | Phase 1.5 (photos) as backup; or the operator clicks that one marker manually and the tool accepts the mixed input |
| The first guess is so wrong that Stage 2 cannot find the markers | Low | Phase 1.5 (photos) to sharpen the guess; widen the search window as a command-line option |
| A photo is labelled wrong (we already saw one: GCP15 appears in the photos but was not surveyed) | **High — already happened** | The tool checks label consistency before starting and refuses to guess |
| The tool picks a subset that happens to cluster on one bank | Low (hard rule blocks this) | The hard rule rejects any subset that leaves an image quadrant empty |
| The image library we depend on changes behaviour between versions | Low | We record the library version in the audit file; a pinned version is required to reproduce the result |
| The survey is too noisy for any subset to meet the quality bar | **High — this is the likely outcome on this dataset** | The tool says so clearly in the report and refuses to write a certified calibration by default. The operator may invoke the `--demo-override` flag (Decision 6) to write an uncertified calibration for end-to-end pipeline demonstration; that output is labelled `DEMO_UNCERTIFIED` in filename and config. Certified use still requires a re-survey — see `survey/outsourced_survey_brief.md`. |

The last row is not a failure. It is the purpose of the automation: to quantify noise faster than a human click log can, so that the decision to re-survey is data-driven rather than a judgement call.

---

## 9. Roadmap

Each phase has a clear checkpoint. We pause at each checkpoint to review before moving on.

| Phase | What gets built | Who | Time | Checkpoint |
|---|---|---|---|---|
| 0 | Operator clicks each of the 20 GCPs once on the pinned video frame, saves a small file called `sukabumi_gt_clicks_v1.json`. Tool is already built (`survey/auto_fit/ground_truth_click.py`). | Tom | ~30 min | File saved with 20 clicks (or explicit skips) |
| 1 | Main pipeline: Stages 1–2 end-to-end. Command-line tool (`orc_auto_fit.py`). | Claude + Tom | 1 day | **A1:** ≥ 70% of GCPs within 5 cm |
| 1.5 | Only if A1 fails: add photo-based help to Stage 1. | Claude + Tom | 0.5 day | A1 after re-run |
| 2 | Stage 3 (subset search) and the audit log. | Claude + Tom | 0.5 day | **A2:** auto subset error ≤ hand-trimmed |
| 3 | Tests, manual-click compatibility, usage documentation. | Claude + Tom | 1 day | **A3:** full round-trip; tests all pass |

**Total estimate:** 2.5–3 days of focused work, including Phase 1.5 if it triggers.

---

## 10. What this document does not cover

- **Velocity measurement.** This document covers only camera calibration. The part of the OpenRiverCam pipeline that turns calibrated video into flow rate is a separate step and is not affected by this work.
- **The re-survey.** If and when the re-survey happens, the standard manual-click calibration path (in `orc_build_camera_config.py`) is used against the clean data — not this auto-fit pipeline. Re-survey planning itself is a separate document (`survey/outsourced_survey_brief.md`).
- **Other deployment sites.** This pipeline is for Sukabumi 2026 only. Methodology for other sites — including how they avoid landing in this salvage situation to begin with — is out of scope and is being handled in separate deployment planning.
- **Future reuse of the auto-fit code.** This is not a supported tool. Once Sukabumi is calibrated (or declared unsalvageable and re-surveyed), the code is legacy. The design intentionally does not invest in maintainability beyond that point.
- **Certification for flow-rate or water-level measurement.** A successful auto-fit run (meeting A1/A2/A3) is *necessary* but not *sufficient* for certified hydrological measurements — certification requires an independently-verified survey, documented lens calibration, a stage-gauge reference, and a QA process that is out of scope here. The `--demo-override` output (Decision 6) is emphatically *not* certified and its filename and config both carry that label. Any figures quoted from demo-mode output must be accompanied by the DEMO-UNCERTIFIED disclaimer.

---

## 11. Files and documents this links to

For anyone who wants to go deeper:

- `survey/AUTO_FIT_DESIGN.md` — the full technical design with every decision recorded, including the feedback from the four review agents.
- `survey/ORC_FIT_STRATEGY.md` — the manual calibration procedure this automation replaces.
- `survey/NEXT_SESSION_PLAN.md` — cold-start document for picking up this work.
- `spring_2026_ID/survey_data/20260421_rerun_plan.md` — the correction pipeline that produces the inputs to this calibration step.
- `spring_2026_ID/survey_data/corrections.md` — full log of every correction to the survey data, with checksums for audit.
- `survey/outsourced_survey_brief.md` — the plan if re-survey is required.
- `survey/research/professional_surveyor_and_escape_hatch.md` — deeper analysis of re-survey options A through G.

---

## 12. Appendix A — Background concepts

Reference section. Readers already comfortable with camera calibration and photogrammetry can skip to §13. Written at undergrad CS level; matrices, vectors, Gaussian noise, and algorithm complexity are assumed.

### 12.1 The pinhole camera model

A camera is modelled by two sets of parameters:

- **Intrinsics** — a 3×3 matrix `K` describing the camera itself. Its key entries are the focal length `f` in pixel units and the principal point `(c_x, c_y)` — the pixel where the optical axis meets the sensor. Intrinsics also include lens distortion coefficients. Intrinsics do not change when the camera is moved.
- **Extrinsics** — the rotation `R` (3×3 orthogonal matrix) and translation `t` (3-vector) that map a point in world coordinates into the camera's local coordinate frame. Extrinsics change every time the camera moves.

Together they define the projection from a 3D world point `X = (X, Y, Z)` to a 2D pixel `p = (u, v)`:

```
[u]           [X]
[v]  ≈  K · (R · [Y] + t)
[1]           [Z]
```

where the `≈` hides a division by the third (homogeneous) component. This is the **pinhole projection equation**. Lens distortion is applied as a nonlinear correction on top; for short focal lengths it matters, for longer ones it can often be ignored.

### 12.2 Perspective-n-Point (PnP) and reprojection error

Given `n ≥ 3` known correspondences `(X_i, p_i)` — 3D world points and their 2D pixel observations — and the intrinsics `K`, the **Perspective-n-Point** problem is to find the extrinsics `(R, t)` that best explain the observations. It is the core problem in single-image camera pose estimation.

For each GCP, given a candidate `(R, t)`, we compute a **predicted pixel** `p_i_pred` via the projection equation, and the **residual** is the difference from the observed pixel:

```
residual_i = p_i_observed − p_i_predicted
```

The **reprojection error** is the vector of these residuals. PnP solvers minimise the sum of squared residuals — a nonlinear least-squares problem, typically solved by Levenberg-Marquardt after a closed-form initialisation (e.g. EPnP or P3P).

### 12.3 RMSE

The **Root Mean Square Error** of a residual set is

```
RMSE = sqrt( (1/n) · Σ_i ||residual_i||² )
```

It is the standard one-number summary of fit quality. A small RMSE means the pose matches the data. A large RMSE means either the pose is wrong, the `X_i` are wrong, or the `p_i` are wrong — pure PnP cannot tell these apart. pyorc reports RMSE in **world metres**, not pixels, because it un-projects residuals back to the ground plane via the current pose estimate. The conversion at our site is roughly 1 pixel ≈ 1.3 cm at 20 m range with a 1500 px focal length.

### 12.4 RANSAC and MAGSAC++

Plain least-squares (PnP or otherwise) is catastrophically sensitive to outliers — a single bad correspondence can drag the whole fit. **RANSAC** (*Random Sample Consensus*, Fischler & Bolles 1981) addresses this:

1. Sample a minimal subset of correspondences (4 for PnP — the minimum for a unique solution in general position).
2. Fit a model to that subset.
3. Count how many of the full set agree with that model within a pixel-distance threshold — the **inliers**.
4. Repeat for many random subsets; keep the model with the most inliers.
5. Re-fit on the full inlier set.

The hard inlier/outlier threshold is the knob that makes classical RANSAC brittle when the "noise" is actually continuous — every pixel error is "a bit noisy," not "clearly in or clearly out." **MAGSAC++** (Barath et al., CVPR 2020; available in OpenCV as `flags=cv2.USAC_MAGSAC`) replaces the hard threshold with a marginalised soft-weighting scheme. In effect, each point contributes to the score in proportion to how well it fits, with a smooth falloff. For Gaussian-like noise — which is what we expect from a GPS survey with roughly bounded but continuous error — MAGSAC++ is empirically more accurate than classical RANSAC.

### 12.5 Keypoint matching: SIFT and homography (used in Phase 1.5)

**SIFT** (*Scale-Invariant Feature Transform*, Lowe 2004) is a two-part algorithm:

- **Keypoint detector.** Finds image locations that are distinctive at a particular scale — typically corners, blobs, or other high-information regions. Detection is scale-invariant by building a pyramid of Gaussian-smoothed copies and finding extrema of the difference-of-Gaussians at each scale.
- **Descriptor.** Each keypoint gets a 128-element feature vector summarising the local gradient distribution. Two keypoints describing the same physical point in different images will have similar descriptors.

Match SIFT keypoints between two images (often via **Lowe's ratio test** — each descriptor's nearest match must be significantly closer than its second-nearest to count), and you get a set of correspondences between two views of the same scene.

A **homography** `H` is a 3×3 matrix that maps pixels from one view to another when all the matched points lie on a single plane:

```
p' ≈ H · p    (p, p' in homogeneous coordinates)
```

Riverbanks, walls, and water surfaces are approximately planar at our working distances, so a photo of the bank and a video frame of the same bank are related by `H` plus some distortion from depth variation. OpenCV's `cv2.findHomography(src, dst, cv2.RANSAC)` fits `H` from matched pairs and returns inlier flags. In Phase 1.5 we use this to warp the centroid of each GCP marker from a photo into video-frame coordinates, giving us an extra constraint for the Stage-1 pose bootstrap.

### 12.6 UTM and why we use it

**UTM** (*Universal Transverse Mercator*) is a projected coordinate system. Rather than expressing position as latitude and longitude on a sphere (which are angles), UTM projects the Earth onto a series of 60 cylindrical strips, each 6 degrees of longitude wide. Within a zone, positions are given as a pair `(easting, northing)` in metres. Sukabumi sits in Zone 48 South (EPSG code 32748).

The advantage is that Euclidean distance in UTM metres corresponds (to within a small projection scale factor) to physical distance on the ground. We can compute reprojection residuals, GCP spread, and pose offsets using ordinary matrix and vector operations — no spherical geometry needed. At our site scale (~50 m across), the projection distortion is negligible.

### 12.7 ArUco markers

**ArUco** markers (Garrido-Jurado et al., 2014) are square fiducials consisting of a black border surrounding a binary grid. A typical `4×4_50` dictionary encodes a 4-bit × 4-bit pattern selected from a dictionary of 50 mutually-distinguishable codes — so the marker's bit pattern is both easy to decode *and* resistant to confusion with other markers. OpenCV's `cv2.aruco.detectMarkers()` does the whole pipeline in one call: binary thresholding, contour extraction, quadrilateral filtering, bit decoding, and sub-pixel corner refinement.

Why they matter for us: an ArUco board physically placed at each GCP replaces the entire Stage 1 + Stage 2 logic with a single library call. The marker's ID tells us which GCP it is; its four corners give us sub-pixel pixel coordinates to plug directly into PnP. The only reason we are not using them at Sukabumi is that the markers were placed before the design called for ArUco; the boards that *are* in place are older ad-hoc checker tiles and painted X-marks, which SSIMS-Flow and similar tools confirm need the longer pipeline we designed. Jakarta will use ArUco.

---

## 13. What we would like from the team tomorrow

Concrete decisions to agree on:

1. **Is the 5 cm accuracy target correct for the automation?** Too tight, too loose, or right?
2. **Is the "re-survey needed" output acceptable if that is what the tool concludes?** In other words: if after all the work the honest answer is "the survey is not good enough," is the team ready to act on that?
3. **Who runs Phase 0?** (Default: Tom, on his machine, ~30 min.)
4. **When do we plan for Phase 1 day(s)?** To fit around other deployment work.
5. **Is the Sukabumi-only scope correct?** Decision 5 commits this pipeline to a single site. Any methodology for other sites is handled in separate planning, not here. Any concerns with that boundary?

These are the points to review. Everything else in this document is informational.
