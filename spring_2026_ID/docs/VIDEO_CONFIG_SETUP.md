# Video Configuration Setup

**Version:** 1.0 — April 2026
**Purpose:** End-to-end process to create the ORC-OS video configuration
that the daemon uses to process each incoming capture.
**Audience:** Tom on-site; written so PMI staff can follow along or re-run it.

---

## Contents

- [What This Covers](#what-this-covers)
- [Background](#background)
- [Prerequisites](#prerequisites)
- [Phase 1 — Field: Calibration Video](#phase-1--field-calibration-video)
- [Phase 2 — Field: GPS Survey](#phase-2--field-gps-survey)
- [Phase 3 — Office: Survey Data Prep](#phase-3--office-survey-data-prep)
- [Phase 4 — ORC-OS UI: Author the Video Configuration](#phase-4--orc-os-ui-author-the-video-configuration)
- [Phase 5 — Activate the Daemon](#phase-5--activate-the-daemon)
- [Phase 6 — Validate](#phase-6--validate)
- [Profile Testing](#profile-testing)
- [Troubleshooting](#troubleshooting)

---

## What This Covers

Creating and activating the **video configuration** that ORC-OS binds to
each incoming capture. The video configuration contains:

- Camera pose (position + orientation, solved from GCPs)
- Lens distortion parameters
- Cross-section geometry (for discharge integration)
- Area-of-interest / bounding box (for PIV)
- Processing recipe (frame range, resolution, window size, etc.)

Without a finalized video config selected in Daemon Settings, ORC-OS
ingests incoming videos but cannot process them. This doc covers the
full path from "station is mounted" to "daemon processes captures end
to end."

Related docs:

- Camera capture pipeline → `ORC_CAPTURE.md`
- Field survey procedure → `FIELD_SURVEY_GUIDE.md`
- Coordinate reprojection → `../survey/QGIS_Reproject_WGS84_to_UTM48S.md`
- Camera ISAPI config → `../camera/README.md`

---

## Background

> **Discovery note — first deployment at this camera class.**
> This is the first ORC deployment using a consumer-grade ANNKE C1200
> (Hikvision OEM, 12MP, factory-sealed PoE). Known-good thresholds,
> recipes, and reprojection tolerances for this camera class do not yet
> exist. The steps below describe the happy-path procedure; quality
> thresholds are starting points, not gates. Record what you see so the
> next deployment has real data to tune against.

---

## Prerequisites

Before starting:

- [ ] Station is fully assembled, powered, and mounted in its final
      position. Re-aiming the camera after survey invalidates the pose.
- [ ] `orc-capture --skip-relay --dry-run` passes on the Pi — camera
      reachable, quality gate green. See `ORC_CAPTURE.md`.
- [ ] ORC-OS Daemon Settings already configured except for video config
      selection (filename template, time diff, reboot, LiveORC callback).
      See `ASSEMBLY_*.md` Step 5.
- [ ] **Daemon runner OFF** and Video Configurations field empty.
- [ ] Maintenance-mode flag is set (`orc-pmi-stations` repo) so the
      capture timer does not fire mid-setup.
- [ ] Field laptop can reach the Pi (maintenance hotspot or Pangolin).
- [ ] Survey equipment ready per `FIELD_SURVEY_GUIDE.md`.

---

## Phase 1 — Field: Calibration Video

The calibration video must come from the station's own camera in its
final mounted position. A handheld sample will not work — pose, focal
length, and lens distortion must match the production captures.

1. Confirm the station is in maintenance mode (check
   `/run/orc-maintenance-mode` exists, or the LED pattern).
2. Place GCP markers per `FIELD_SURVEY_GUIDE.md` Step 1. All 8–10 must
   be visible in the camera frame.
3. Clear the scene: no people, boats, vehicles, or waved markers.
4. SSH into the Pi from the field laptop.
5. Trigger one manual capture:
   ```bash
   sudo rm /run/orc-maintenance-mode       # temporarily lift the gate
   orc-capture --dry-run                    # captures to /tmp, no ORC-OS delivery
   sudo touch /run/orc-maintenance-mode     # restore the gate
   ```
6. Copy the MP4 off the Pi to the field laptop:
   ```bash
   scp pi@<station>:/tmp/orc_capture_*.mp4 ./calibration.mp4
   ```
7. Open the video on the laptop. Verify:
   - All GCP markers are clearly visible.
   - No motion blur on the markers.
   - Image is sharp across the full frame.
   - No people or obstructions.
8. If anything is wrong, fix and repeat from step 3. Keep only the best
   take.

> **Discovery note — bitrate may vary.** The quality gate minimum is
> 12 Mbps, but actual delivered bitrate can be lower than the camera's
> CBR setting depending on scene complexity. Check `ffprobe calibration.mp4`
> and record the actual bitrate alongside the profile name.

---

## Phase 2 — Field: GPS Survey

Follow `FIELD_SURVEY_GUIDE.md` Steps 3–7 end-to-end:

- [ ] GCPs surveyed (step 3) — all 8–10 markers, RTK FIX only
- [ ] Cross-section surveyed (step 4)
- [ ] Water level at time of calibration video recorded (step 5) — this
      is `h_ref`
- [ ] Camera position surveyed (step 6)
- [ ] Check points re-measured (step 7) — drift <3 cm H, <4 cm V

Export all points from SW Maps as GeoJSON.

---

## Phase 3 — Office: Survey Data Prep

Done on the field laptop using QGIS.

9. Reproject WGS84 → UTM 48S per `survey/QGIS_Reproject_WGS84_to_UTM48S.md`.
10. Split the point set into three files:
    - `gcps.csv` — columns: `id, x, y, z`
    - `cross_section.csv` — columns: `x, y, z`
    - `camera_position.csv` — single row: `x, y, z`
11. Subtract pole length from cross-section elevations (submerged
    points). See `SURVEY_PROCESS_v2.md`.
12. Record `h_ref` (the water-level reading at calibration-video time)
    as a decimal meter value in the same vertical datum.

Deliverables to carry into Phase 4:

| File | Used for |
|------|----------|
| `calibration.mp4` | Pixel-to-world pose fit |
| `gcps.csv` | Pose fit ground-control points |
| `cross_section.csv` | Discharge integration geometry |
| `h_ref` (number) | Water level at calibration time |
| `camera_position.csv` | Camera XYZ for AOI reprojection |

---

## Phase 4 — ORC-OS UI: Author the Video Configuration

Connect the field laptop to the Pi's maintenance hotspot and open the
ORC-OS web UI at `http://<station>.local`. Order matters — each step
feeds the next.

### 4.1 Upload the Calibration Video

13. Navigate to `/video`.
14. Drag `calibration.mp4` into the upload zone.
15. Set the timestamp close to when the video was captured.
16. Confirm the video appears in the list with a red blinking "video
    configuration" icon next to it.

### 4.2 Create the Camera Config

17. Click the video-config icon on `calibration.mp4` → **Edit** → new
    video configuration window opens.
18. Under **Name + details**, give it a descriptive name
    (e.g. `sukabumi-profile-a-2026-04-17`).
19. Under **Camera pose**, set image dimensions:
    - Profile A (default): **1920 × 1080**
    - Profile B: **1280 × 720**
    - Must match the video's actual resolution.

### 4.3 Upload GCPs and Match Pixels

20. Upload `gcps.csv` via the control-points interface.
21. For each GCP, click its pixel location in the video frame. Label
    order must match the CSV.
22. Run the pose-fit solver.
23. Check the RMS reprojection error reported by the solver.
    - **Target:** < 5 pixels
    - **Record the actual value** regardless of pass/fail.

> **Discovery note — RMS thresholds are unproven.** Consumer lenses
> with aggressive rectilinear correction may not hit < 5 px at 12MP. If
> the solver converges but RMS is higher, continue but flag the result.
> If the solver does not converge or RMS is > 15 px, stop — GCP
> coordinates, pixel matches, or camera aim is likely wrong.

### 4.4 Cross-Section

24. Switch to the **Cross sections** tab.
25. Upload `cross_section.csv` as the bed-following cross-section.
26. Enter `h_ref` as the water level at calibration time.
27. Verify the cross-section renders in the side-view panel with water
    level marked correctly.

### 4.5 Area of Interest (Bounding Box)

28. Switch to the **Camera pose → AOI** panel (or equivalent).
29. Draw the bounding box on the water surface:
    - Extends ≥ 2 m upstream and downstream of the cross-section.
    - Spans the full potential flow width, including bank areas that
      become inundated at high water.
    - Excludes sky, vegetation, and out-of-frame regions.
30. Confirm the box reprojects sensibly onto the top view.

### 4.6 Processing Recipe

31. Switch to the **Processing** tab.
32. Set starting parameters:
    - **First frame:** 0 (or the first clean frame if the scene is
      settling).
    - **Frame range:** full video length (~60 frames at 12.5 fps × 5 s).
    - **Spatial resolution:** start at 0.05 m/px (tune later).
    - **PIV window size:** start at pyorc defaults (typically 25 px
      interrogation window).
33. Save.

> **Discovery note — no known-good recipe for this camera.** pyorc
> recipes are currently tuned against higher-end cameras. Treat these
> values as initial guesses. See Profile Testing below for the iteration
> loop. Consult the pyorc user guide at
> https://localdevices.github.io/pyorc/user-guide/index.html for
> parameter meanings.

### 4.7 Finalize

34. Review all four tabs — each should show a green/completed state.
35. Save the video configuration as **finalized**. Only finalized
    configs appear in Daemon Settings.

---

## Phase 5 — Activate the Daemon

36. Navigate to `/settings`.
37. In **Video configurations**, select the config created in Phase 4.
38. Confirm **LiveORC Site ID** is set (created on LiveORC admin per
    `ASSEMBLY_*.md`).
39. Exit maintenance mode:
    - Push the maintenance flag `OFF` in the `orc-pmi-stations` repo.
    - Reboot the Pi, or wait for the next maintenance-check cycle.
    - Confirm `/run/orc-maintenance-mode` is absent.
40. In `/settings`, set **Activate the daemon runner** → **ON**.

---

## Phase 6 — Validate

41. Wait for the next 15-minute capture, or trigger one manually:
    ```bash
    sudo systemctl start orc-capture.service
    ```
42. In ORC-OS `/video`, the new capture should appear within a minute.
43. Status should progress: uploaded → linked to water-level → processed.
    A **processed** status with a velocity/discharge result means the
    pipeline works end-to-end.
44. Inspect the augmented-reality overlay on the processed video:
    - GCP reprojection overlay looks correctly placed on the markers.
    - Velocity vectors align with expected flow direction.
    - Discharge estimate is within an order of magnitude of a manual
      gauge reading (if available).
45. On the LiveORC server (`https://openrivercam.endlessprojects.info/admin/`),
    confirm the record appears under the correct Site ID.
46. Run one more capture cycle before leaving the site to confirm
    repeatability.

> **Discovery note — "reasonable" is not yet defined.** For this
> camera class, there is no reference dataset for what acceptable
> velocity confidence or PIV pass rate looks like. Capture 10 sequential
> cycles and compute mean/std of the discharge estimate. High variance
> at steady water level indicates PIV instability. Log the numbers in
> `tests/<site>/` for later comparison.

---

## Profile Testing

Per `TODO.md` Phase 5, multiple camera profiles (A: 1080p/16 Mbps,
B: 720p/20 Mbps, C: local SD recording) are being tested. Each profile
needs its own calibration-and-config run — but not everything is redone.

| Artifact | Reuse across profiles? | Notes |
|----------|-----------------------|-------|
| GCP survey (3D coords) | Yes | Markers do not move |
| Cross-section survey | Yes | Channel geometry does not change |
| `h_ref`, camera position | Yes | Same survey trip |
| Calibration video | **No** if resolution changes | Pixel coords are resolution-specific |
| Camera config (dimensions) | **No** if resolution changes | Bound to frame size |
| GCP pixel matches + pose fit | **No** if resolution changes | Pixel-dependent |
| AOI bounding box | **No** if resolution or pose changes | Pixel-dependent |
| Processing recipe | Usually new | Tune per bitrate/resolution |
| Video config | **New per profile** | This is the thing being compared |

Workflow for a second profile:

1. Push the new camera profile via `camtool.py` (e.g. Profile B 720p).
2. Update `orc-capture.conf` `EXPECTED_WIDTH`/`EXPECTED_HEIGHT` to match.
3. Repeat Phase 1 (calibration video at new resolution).
4. Repeat Phase 4 start-to-finish. Name the config clearly
   (e.g. `sukabumi-profile-b-2026-04-18`).
5. In `/settings`, swap the active video config to the new one.
6. Capture 10 cycles per profile for comparison.

> **Discovery note — decision gate.** Per `TODO.md`:
> - RTSP profile delivers ≥ 15 Mbps and acceptable ORC results → keep
>   ANNKE C1200.
> - No RTSP profile works but Profile C (local SD) does → implement
>   ISAPI capture method.
> - No profile produces acceptable results → plan camera replacement
>   before Sukabumi deployment.

Record per-profile findings in a shared log. Suggested location:
`tests/<site>/profile_comparison.md`.

---

## Troubleshooting

### Pose fit does not converge

- Verify GCP CSV labels match the pixel-click order exactly.
- Verify GCPs are spread in 3D — not all on one bank, not all in a line.
- Verify GCP coordinates are in the correct CRS (UTM 48S meters, not
  lat/lon).
- Try removing one GCP at a time — a single mis-surveyed point can
  prevent convergence.

### High RMS reprojection error (> 10 px)

- Check each GCP for a mis-click. The solver reports per-point residuals
  in the UI — the outlier is usually obvious.
- Verify the GCP marker has not shifted between survey and video
  (wind, animal, foot).
- Confirm the calibration video is from the same camera pose as the
  survey. Any re-aim invalidates the fit.

### Video config not selectable in Daemon Settings

- Config must be marked **finalized**. Return to Phase 4 and confirm
  every tab is green.
- Reload `/settings` after finalizing.

### Daemon is ON but captures do not process

- Confirm the selected video config matches the resolution of incoming
  captures. Mismatch → pipeline skips processing.
- Confirm `h_ref` is set and water-level time-series has a record within
  the allowed time difference (3600 s default).
- Check `journalctl -u orc-daemon` (or equivalent) for processing
  errors.

### Capture timer fires during setup

- Maintenance mode not active. Set the flag and reboot, or
  `sudo touch /run/orc-maintenance-mode` as a one-off.

### Results look wrong — flow direction reversed, magnitudes way off

- Cross-section point order may be reversed (left-bank-first vs
  right-bank-first). Verify against the survey map.
- Camera position Z may be below water surface (sign error in elevation
  datum).
- AOI may extend over non-flowing areas (bank vegetation, stagnant
  edges). Tighten the box.

---

## Changelog

- **v1.0 (2026-04-17):** Initial version. Happy-path procedure with
  discovery callouts for first ANNKE C1200 deployment.
