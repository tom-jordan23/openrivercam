# Methodology: Automated Camera Calibration for OpenRiverCam (Sukabumi, Spring 2026)

**Purpose:** Explain the approach we are taking to calibrate the camera at the Sukabumi site from the existing survey data, and the plan for building the automation that does this work.

**Audience:** The deployment team (PMI staff, hydrologist, software helper). No deep software background is required to read this document. Technical terms are defined the first time they appear.

**Date:** 2026-04-21. This document will change as we learn more during Phase 1 and Phase 2 (see "Roadmap" below).

---

## 1. What problem are we solving?

OpenRiverCam measures river flow by watching the water surface in a camera. For those measurements to be in real physical units (metres per second, cubic metres per second), the software needs to know where the camera is and where it is pointing. This is called **camera calibration**.

Calibration works by matching things we can see in the video (pixels on the screen) to things we measured on the ground (GPS positions in UTM coordinates). The things we measure on the ground are called **Ground Control Points** (GCPs). At Sukabumi we placed 20 GCPs — black-and-white checkerboard tiles and painted X-marks — on the riverbanks and in the water channel, then surveyed each one with a GPS rover.

The calibration step answers the question: *"given these 20 points in the video and these 20 GPS positions on the ground, where is the camera and which way is it pointing?"*

Once we can answer that, the software can turn pixel motion in the video into flow rate.

---

## 2. Why is this harder than it should be?

Two problems with the survey data we have:

**Problem 1 — The GPS survey has more error than planned.** On a good day, RTK GPS gives centimetre-level accuracy. At Sukabumi the check-point comparison shows about 99 cm horizontal and 139 cm vertical spread between two points that should be identical. That is roughly ten times worse than our target. A re-survey with better equipment is already planned, but we do not want to wait for it before starting — partly to make progress, partly because the re-survey will benefit from what we learn now.

**Problem 2 — The current calibration process is manual.** Today, the operator opens the video, looks at the first frame, and clicks each of the 20 markers by hand. This works, but:

- Clicking is slow and hard to repeat exactly.
- Every time we want to try a different combination of markers, the clicking has to be redone.
- A click log is hard to audit: we cannot re-verify later that the clicks were accurate.
- When we move to the Jakarta site, the same manual process starts over.

We want to replace the clicking with a software tool. The tool will do three things:

1. Find each marker automatically in the video.
2. Try different combinations of markers to find the one that gives the best calibration.
3. Honestly report when the survey data is too noisy to give us a good calibration — telling us the re-survey is necessary, rather than hiding the problem.

---

## 3. What we already did (2026-04-21)

**Survey data corrections pipeline ran successfully.** The field crew returned to the site on Day 2 and captured the missing camera position (called CAM) plus extra GCPs and re-shoots of earlier points. The correction pipeline now produces a complete set of inputs for the calibration step. All corrections are recorded in `spring_2026_ID/survey_data/corrections.md` with cryptographic checksums so any later change can be detected.

**We know the survey is not clean enough for a full-quality calibration.** The pipeline flags the problem clearly: the check-point gate fires with "EXCEEDS GATE" and says to investigate before trusting the data. We kept that warning on purpose — it is the honest signal that the 2026-04-21 dataset is a salvage attempt, not a final result.

**We checked four independent reviews before picking the approach.** Before writing any code for the automation, four specialised reviewers (test strategy, software-library internals, research on existing tools, and architecture) read our first draft and reported back. Their feedback changed several decisions — see "Key decisions" below.

---

## 4. The approach — three stages

The automation has three stages. Each stage does one job and passes its result to the next.

### Stage 1 — Educated guess

We already know, from the survey, where the camera is (CAM). We also know where the 20 GCPs are. The Stage-1 software takes these facts and makes a rough guess about which way the camera is pointing. The guess does not need to be perfect; it only needs to be close enough to narrow the search for each marker.

Concretely: Stage 1 produces a number for each GCP — the approximate pixel on the screen where we expect to see it, plus a search window around that pixel of about 50 pixels in each direction.

### Stage 2 — Look, detect, refine

For each GCP, Stage 2 looks only inside the small search window from Stage 1. Inside that window the software runs a marker detector — a standard image-processing routine that finds the high-contrast checkerboard or X-pattern. When it finds one, that pixel is recorded as the location of that GCP in the video.

Once Stage 2 has found as many GCPs as it can, it uses all of them together to re-calculate the camera's position and direction. This new, better answer is then used to shrink the search windows from 50 pixels down to 20 pixels, and the search is repeated. After two or three rounds, the answer settles.

The important design point here is **"look where we expect to look."** A simpler version of the software was tried first, which ran the marker detector over the whole image. That version produced around 100 possible markers in a frame that has only about 10 real ones — the image is full of contrasty cobbles and wall edges that fool the detector. By looking only in the small windows, we cut that noise down to essentially zero.

### Stage 3 — Try leaving markers out

Not every GCP will be equally reliable. Some were surveyed with a tall bamboo pole (more wobble); some sit in water; some are partly hidden. The "best" calibration does not use all 20 — it uses the subset of GCPs that gives the lowest overall error.

Stage 3 tries different subsets in order of plausibility:

1. Start with all GCPs Stage 2 found.
2. Calculate the error.
3. Remove the worst-scoring GCP. Calculate the error again.
4. If the error went down, keep that GCP removed and repeat.
5. Stop when removing any further GCP makes the error go up, or when only 6 remain, or when we would lose all the GCPs on one side of the image.

The last two conditions are safety rules. Below 6 GCPs the calibration becomes unstable. If we remove all the near-bank GCPs, the camera position can drift even though the error number looks fine.

At the end, Stage 3 reports:

- The chosen subset.
- The error on that subset, in real-world units (metres).
- Every subset that was considered and why each was accepted or rejected, in a file called `auto_fit_audit.json` that can be inspected after the fact.

---

## 5. How accurate do we want to be?

The accuracy target for each individual GCP is **5 cm on the ground.** This is the distance between where the software places a marker in the video and where the operator would place it by clicking manually.

This number is not the same as the calibration error. The calibration error depends on how good the GPS survey is, and we already know that is about 90 cm. The 5 cm target is only about the software's ability to locate markers it can see — it is a test of the automation itself, not of the survey.

If the tool does not hit 5 cm for most GCPs, we add a backup stage (Phase 1.5 in the roadmap) that uses the photos of each GCP to help the initial guess.

---

## 6. Key decisions and why we made them

These are the choices that shaped the approach above.

**Decision 1 — Start without photos; add them only if we need to.** The field crew took photos of each GCP. Early on we assumed those photos would be central to the automation. The research review showed they are useful but not essential: if the Stage-1 guess is accurate enough, Stage 2 finds the markers without needing the photos. So we build the simpler version first, measure accuracy, and add the photo step only if accuracy is not good enough.

**Decision 2 — Bypass one of the software library's features to keep the subset search fast.** The library that does the calibration math (pyorc) has a calibration step that re-optimises the camera lens each time it is called. That step takes a few seconds. If we did that for every subset in Stage 3 (and there can be hundreds), the tool would take hours. We pre-compute the lens information once, then tell the library to use our version directly. Each subset now takes about one millisecond, so a full search finishes in under a minute.

**Decision 3 — Use hard limits instead of soft penalties in Stage 3.** The first draft scored each subset with a weighted sum of three terms: error, "spread" (markers on both banks), and count. Soft weights like these need to be tuned, and nobody tunes them. The architecture review suggested replacing the soft penalties with hard rules: never go below 6 markers, never leave a side of the image without a marker. The error is then the only number that gets optimised. This is simpler and easier to audit.

**Decision 4 — The tool must say "re-survey needed" when the data is too noisy.** This is the single most important design decision. We are calibrating on a survey we already know is noisy. The tool must not hide that fact by picking a subset that happens to have low error. If every subset of at least 6 GCPs has high error, the tool will say so in the report and will not write a calibration file. This makes automation honest, not a way to paper over bad data.

**Decision 5 — For future sites, use ArUco markers instead of ad-hoc X-marks.** ArUco is a standard type of marker (a small printed square with a unique code) that the image library can detect in one call. At Sukabumi the markers were already placed when this approach was being designed, so we cannot switch now. The next site (Jakarta) and any future site should use ArUco: it removes most of the work Stages 1 and 2 do today. The specifications for printing and placing ArUco boards will be added to the Jakarta deployment plan.

---

## 7. How we will know this worked

Three acceptance tests, each with a clear pass/fail line:

**A1 — Marker location accuracy.** At least 70% of the 20 GCPs must be located within 5 cm of a manual click by the operator. The comparison file (`sukabumi_gt_clicks_v1.json`) is the operator's one-time ground truth.

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
| The survey is too noisy for any subset to meet the quality bar | **High — this is the likely outcome on this dataset** | The tool says so clearly in the report and refuses to write a calibration. We move to the re-survey plan. |

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
- **The re-survey.** If and when the re-survey happens, the same pipeline runs against the new data. The re-survey planning is a separate document (`survey/outsourced_survey_brief.md`).
- **Jakarta.** The same tools will be used at Jakarta with different inputs. Jakarta should use ArUco markers from the start; this is a note for the Jakarta deployment plan, not part of the Sukabumi work.

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

## 12. What we would like from the team tomorrow

Concrete decisions to agree on:

1. **Is the 5 cm accuracy target correct for the automation?** Too tight, too loose, or right?
2. **Is the "re-survey needed" output acceptable if that is what the tool concludes?** In other words: if after all the work the honest answer is "the survey is not good enough," is the team ready to act on that?
3. **Who runs Phase 0?** (Default: Tom, on his machine, ~30 min.)
4. **When do we plan for Phase 1 day(s)?** To fit around other deployment work.
5. **For the Jakarta site:** do we commit now to using ArUco markers, or discuss at the site visit?

These are the points to review. Everything else in this document is informational.
