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
- [Glossary](#glossary)

---

## What This Covers

Creating and activating the **video configuration** — the bundle of
geometry and algorithm settings that ORC-OS (the edge software running
on the Raspberry Pi) uses to turn each raw video into velocity and
discharge estimates. The video configuration contains:

- **Camera pose** — the camera's position (x, y, z) and orientation
  (yaw, pitch, roll) in a real-world coordinate system, solved from
  ground control points.
- **Ground control points (GCPs)** — physical markers placed at known
  3D coordinates, visible in the camera frame. The pose fit uses them
  to reconstruct camera geometry and lens distortion.
- **Lens distortion parameters** — corrections for how the lens bends
  straight lines near the edges of the frame.
- **Cross-section** — a line of bed-elevation points perpendicular to
  flow, used to compute wetted area for **discharge** (volumetric flow
  rate, m³/s).
- **Area of interest (AOI)**, a.k.a. bounding box — a rectangle on the
  water surface where velocities are estimated.
- **Processing recipe** — algorithm parameters for **PIV** (particle
  image velocimetry — the cross-correlation technique that estimates
  water-surface velocities by matching patterns between successive
  frames): frame range, spatial resolution, interrogation window size,
  and so on.

Without a finalized video configuration selected in **Daemon Settings**
(the ORC-OS page that controls automatic video processing), the
daemon ingests incoming videos but cannot process them. This doc covers
the full path from "station is mounted" to "daemon processes captures
end to end."

See the [Glossary](#glossary) at the end of this document for a full
list of terms and acronyms.

Related docs:

- Camera capture pipeline → `ORC_CAPTURE.md`
- Field survey procedure → `FIELD_SURVEY_GUIDE.md`
- Coordinate reprojection → `../survey/QGIS_Reproject_WGS84_to_UTM48S.md`
- Camera ISAPI config → `../camera/README.md`

---

## Background

> **Discovery note — first deployment at this camera class.**
> This is the first ORC deployment using a consumer-grade ANNKE C1200
> (Hikvision OEM 12-megapixel factory-sealed camera, powered and
> networked over a single Ethernet cable via **PoE** — Power over
> Ethernet). Known-good thresholds, recipes, and reprojection
> tolerances for this camera class do not yet exist. The steps below
> describe the happy-path procedure; quality thresholds are starting
> points, not gates. Record what you see so the next deployment has
> real data to tune against.

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
- [ ] **Maintenance-mode** flag is set (see `orc-pmi-stations` repo);
      this is the remote kill-switch that tells the 15-minute capture
      timer to skip capture cycles, so we can work on the station
      without the scheduler firing mid-setup.
- [ ] Field laptop can reach the Pi — either via the station's local
      maintenance WiFi hotspot, or via **Pangolin** (the remote-access
      VPN used for over-the-internet SSH and web UI access).
- [ ] Survey equipment ready per `FIELD_SURVEY_GUIDE.md`.
- [ ] `orc-calibration-preflight` reports no failures on the Pi (run it
      *now*, before you leave for the field):
      ```bash
      orc-calibration-preflight
      ```
      This checks camera reachability, **ISAPI** (Hikvision's HTTP REST
      camera API) authentication, camera clock drift, maintenance gate,
      disk space, and config files. The log is written to
      `/home/pi/calibration/<session>/preflight-<time>.log`.

### Session convention

All calibration tools write to a per-session directory under
`/home/pi/calibration/<session>/`. By default `<session>` is today's
date (`YYYYMMDD`); override with `--session NAME` if you run
calibration multiple times in a day or want a named session
(e.g. `--session profile-b-redo`).

Session directory contents after a full run:

```
/home/pi/calibration/20260417/
  preflight-083015.log             # from orc-calibration-preflight
  20260417T094210_profile-a.mp4    # calibration video (from orc-calibration-capture)
  20260417T094210_profile-a.json   # metadata sidecar
  session.log                      # append-only combined log
```

---

## Phase 1 — Field: Calibration Video

The calibration video must come from the station's own camera in its
final mounted position. A handheld sample will not work — pose, focal
length, and lens distortion must match the production captures.

1. Place GCP markers per `FIELD_SURVEY_GUIDE.md` Step 1. All 8–10 must
   be visible in the camera frame.
2. Clear the scene: no people, boats, vehicles, or waved markers.
3. SSH into the Pi from the field laptop.
4. Run preflight to confirm the station is still ready:
   ```bash
   orc-calibration-preflight
   ```
   Fix any FAIL before proceeding. WARN lines are allowed but read them.
5. Trigger one manual capture using the helper script:
   ```bash
   orc-calibration-capture --label profile-a
   ```
   The helper stops the 15-min capture timer, lifts the maintenance
   gate, runs `orc-capture --dry-run`, files the output with a metadata
   sidecar, then restores both timer and gate state on exit (even on
   Ctrl-C). Output lands in
   `/home/pi/calibration/<session>/<ts>_<label>.mp4` plus a `.json`
   sidecar with camera config, ffprobe output, and validation status.
6. Copy the MP4 and sidecar off the Pi to the field laptop:
   ```bash
   rsync -av pi@<station>:/home/pi/calibration/<session>/ ./calibration/
   ```
7. Open the video on the laptop. Verify:
   - All GCP markers are clearly visible.
   - No motion blur on the markers.
   - Image is sharp across the full frame.
   - No people or obstructions.
8. Check the sidecar JSON: `validation_passed` should be `true`, and
   the observed resolution/bitrate should match your expected profile.
9. If anything is wrong, fix and rerun `orc-calibration-capture` (same
   session dir). Keep only the best take.

> **Discovery note — bitrate may vary.** The quality gate minimum is
> 12 Mbps (megabits per second), but the actual delivered bitrate can
> be lower than the camera's **CBR** (constant-bitrate) setting
> depending on scene complexity. Check `ffprobe calibration.mp4` and
> record the actual bitrate alongside the profile name.

---

## Phase 2 — Field: GPS Survey

Follow `FIELD_SURVEY_GUIDE.md` Steps 3–7 end-to-end. The survey
produces 3D coordinates (east, north, elevation in meters) for every
physical point that ORC-OS needs to know about.

- [ ] GCPs surveyed (step 3) — all 8–10 markers, **RTK FIX** only
      (centimeter-accurate GNSS mode — the other modes are not precise
      enough for pose solving).
- [ ] Cross-section surveyed (step 4).
- [ ] Water level at time of calibration video recorded (step 5) —
      this number is `h_ref` (the water-surface elevation at the
      moment the calibration video was captured, in meters, in the
      same vertical datum as the GCPs).
- [ ] Camera position surveyed (step 6).
- [ ] Check points re-measured (step 7) — drift <3 cm H, <4 cm V.

Export all points from **SW Maps** (the Android RTK survey app used
in the field) as **GeoJSON** (a JSON-based standard for geographic
data).

---

## Phase 3 — Office: Survey Data Prep

Done on the field laptop. Use the helper script — it replaces manual
QGIS reprojection and CSV splitting, applies pole-length correction,
and runs a battery of cross-checks on the data.

9. Install dependencies once (laptop, virtualenv recommended):
   ```bash
   pip install pyproj
   ```
10. Export the survey from SW Maps as GeoJSON. Features must be labeled
    by convention (case-insensitive prefix on the `name`/`label`
    property):
    - `GCP1`, `GCP2`, ... — ground control points
    - `XS1`, `XS2`, ... — cross-section points (traversal order)
    - `WL1`, `WL2` — water-level edge points
    - `CAM` — camera position (exactly one)
11. Run the prep tool:
    ```bash
    python3 survey/orc_survey_prep.py survey_20260417.geojson \
        --site sukabumi \
        --pole-length 1.80 \
        --h-ref 12.34 \
        --output-dir ./calibration/
    ```
    The tool reprojects the survey from **WGS84** (the global lat/lon
    reference system that GPS devices report in) to **UTM 48S**
    (Universal Transverse Mercator zone covering western Indonesia;
    this is a local flat-meters projection more suitable for engineering
    work than lat/lon). It also applies pole-length subtraction on GCP
    and XS elevations (the rover antenna sits on top of the pole, so
    we subtract pole length to get the elevation of the point itself).
    Outputs: `gcps.csv`, `cross_section.csv`, `camera_position.csv`,
    `water_level.csv`, and `metadata.yaml`.
12. Review tool output. A hard FAIL stops the run; review the error and
    fix either the survey export, the label convention, or the CLI
    arguments. WARN lines are informational — read each one and decide
    whether to proceed.

Cross-checks the tool runs:

| Check | Level |
|-------|-------|
| GCP count ≥ 4 / cross-section ≥ 1 / exactly one CAM | FAIL |
| Duplicate labels within a bucket | FAIL |
| Source-**CRS** (Coordinate Reference System) coordinate bounds — valid lon/lat if **EPSG:4326** (the standard lookup code for WGS84 lat/lon; EPSG codes are registered identifiers for CRSs) | FAIL |
| Reprojected coords fall inside UTM-48S typical ranges | WARN |
| GCP count < 8 | WARN |
| GCP bbox aspect ratio < 0.2 (colinear) | WARN |
| GCP elevation spread < 0.5 m (poor Z constraint) | WARN |
| Gaps in GCP/XS numbering | WARN |
| Two points within 10 cm (likely duplicate measurement) | WARN |
| Camera elevation at or below h_ref | WARN |
| Camera less than 1 m above h_ref | WARN |
| h_ref disagrees with WL mean by > 0.5 m | WARN |
| h_ref outside XS elevation range (bed or banks missing) | WARN |
| WL point count < 2 | WARN |
| `--pole-length` outside [0.5, 4.0] m | WARN |
| `--h-ref` outside [-500, 6000] m | WARN |

Deliverables to carry into Phase 4:

| File | Used for |
|------|----------|
| `calibration.mp4` + sidecar `.json` | Pixel-to-world pose fit |
| `gcps.csv` | Pose fit ground-control points |
| `cross_section.csv` | Discharge integration geometry |
| `camera_position.csv` | Camera XYZ for AOI reprojection |
| `water_level.csv` | (reference only — `h_ref` is the number ORC-OS uses) |
| `metadata.yaml` | Session record: h_ref, pole length, CRS, warnings |

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
22. Run the **pose-fit solver** (the optimization routine that takes
    the list of 3D world coordinates and their corresponding 2D pixel
    locations and solves for the camera's position, orientation, and
    lens distortion that best explains the pixel matches).
23. Check the **RMS reprojection error** reported by the solver —
    root-mean-square distance, in pixels, between each clicked pixel
    location and where the solved pose re-projects the corresponding
    3D GCP onto the image. Lower is better.
    - **Target:** < 5 pixels.
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
    - **PIV window size:** start at **pyorc** (the Python library that
      implements ORC's video processing — orthorectification, PIV,
      discharge integration) defaults, typically a 25-pixel
      interrogation window.
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
38. Confirm the **LiveORC Site ID** is set. **LiveORC** is the cloud
    server that aggregates results from all stations; the **Site ID**
    is the numeric identifier assigned to this station on that server.
    The Site ID is created on the LiveORC admin page — see
    `ASSEMBLY_*.md`.
39. Exit maintenance mode:
    - Push the maintenance flag `OFF` in the `orc-pmi-stations` repo.
    - Reboot the Pi, or wait for the next maintenance-check cycle.
    - Confirm `/run/orc-maintenance-mode` is absent.
40. In `/settings`, set **Activate the daemon runner** → **ON**. The
    **daemon** is the long-running ORC-OS process that watches for new
    videos and processes them through the pipeline.

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

Per `TODO.md` Phase 5, multiple camera **profiles** (named encoding
presets — combinations of resolution, codec, bitrate, and framerate
stored as XML on the camera via ISAPI) are being tested: A (1080p /
16 Mbps), B (720p / 20 Mbps), C (local SD-card recording). Each
profile needs its own calibration-and-config run — but not everything
is redone.

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

1. Push the new camera profile via `camtool.py` (the ISAPI config
   management tool — see `camera/README.md`), e.g. Profile B 720p.
2. Update `orc-capture.conf` `EXPECTED_WIDTH`/`EXPECTED_HEIGHT` to
   match.
3. Repeat Phase 1 (calibration video at new resolution).
4. Repeat Phase 4 start-to-finish. Name the config clearly (e.g.
   `sukabumi-profile-b-2026-04-18`).
5. In `/settings`, swap the active video config to the new one.
6. Capture 10 cycles per profile for comparison.

> **Discovery note — decision gate.** Per `TODO.md`:
> - **RTSP** (Real-Time Streaming Protocol — the network protocol we
>   use to pull live video from the camera over the LAN) profile
>   delivers ≥ 15 Mbps and acceptable ORC results → keep ANNKE C1200.
> - No RTSP profile works but Profile C (local SD-card recording, then
>   retrieved via ISAPI) does → implement ISAPI capture method.
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

## Glossary

Ordered alphabetically. ORC-specific terms are called out; general
acronyms appear alongside them for quick reference.

- **ANNKE C1200** — the camera model used at both Indonesia sites. A
  consumer-grade 12-megapixel PoE camera (Hikvision OEM on the G6
  platform), factory-sealed to IP67, with built-in IR LEDs.
- **AOI (Area of Interest)** — a rectangular region on the water
  surface where PIV estimates velocities. Extends ≥ 2 m upstream and
  downstream of the cross-section and spans the full flow width.
  Also called the *bounding box*.
- **Bounding box** — see *AOI*.
- **Calibration video** — the single clean 5-second video used
  specifically for authoring the video configuration. Captured with
  `orc-calibration-capture` while all GCPs are visible and the scene
  is otherwise empty.
- **Camera pose** — the camera's position (x, y, z) and orientation
  (yaw, pitch, roll) in the site coordinate system. Solved from GCPs
  by the pose-fit solver.
- **Camera profile** — a named encoding preset stored as XML on the
  camera via ISAPI. Defines resolution, codec (H.264), bitrate
  (constant-bitrate target, kbps), framerate, etc. Profile A, B, C
  are test variants — see Profile Testing above.
- **camtool.py** — our Python tool for pushing, pulling, diffing, and
  verifying ISAPI camera configs against git-tracked XML. See
  `camera/README.md`.
- **CBR (Constant Bitrate)** — an encoder mode that tries to keep the
  output bitrate near a constant value, as opposed to VBR (variable
  bitrate). The ANNKE C1200 supports CBR on its main stream.
- **CRS (Coordinate Reference System)** — the mathematical framework
  for interpreting coordinates as positions on Earth. WGS84 and
  UTM 48S are examples. Every CRS has an EPSG code for lookup.
- **Cross-section** — a line of bed-elevation points crossing the
  river perpendicular to flow. Used to compute wetted area for
  discharge integration. Must extend beyond the water line to cover
  the banks.
- **Daemon** — the long-running ORC-OS process that watches a folder
  for new video files and runs them through the processing pipeline.
  Turned on via Daemon Settings → *Activate the daemon runner*.
- **Daemon Settings** — the ORC-OS web UI page (`/settings`) that
  configures filename templates, time-diff tolerance, LiveORC
  synchronization, and selects which video configuration the daemon
  should use.
- **Discharge** — volumetric flow rate, in cubic meters per second
  (m³/s). Integrated from depth × velocity across the cross-section.
  The primary output of the ORC pipeline.
- **EPSG** — the European Petroleum Survey Group code registry.
  Assigns a short integer to every common CRS so tools don't need
  long verbose names. Examples: EPSG:4326 = WGS84 (lat/lon),
  EPSG:32748 = UTM zone 48 South (meters).
- **GCPs (Ground Control Points)** — physical markers at known 3D
  coordinates, visible in the camera frame. Their correspondence to
  pixel locations lets the pose-fit solver reconstruct camera
  geometry. 8–10 GCPs, spread across both banks and at varying
  elevations, give a robust fit.
- **GeoJSON** — a JSON-based open standard for geographic data. SW
  Maps can export surveys in this format. Each point is a `Feature`
  with a `Point` geometry whose coordinates are [lon, lat, elevation].
- **h_ref** — water-surface elevation (meters, in the site's vertical
  datum) at the moment the calibration video was captured. ORC-OS
  uses this as the anchor for reprojecting the AOI on every
  subsequent video.
- **Hikvision** — the Chinese CCTV manufacturer whose G6 platform the
  ANNKE C1200 is built on. Exposes ISAPI.
- **ISAPI** — Hikvision's HTTP REST camera API (XML payloads, HTTP
  Digest Authentication). Every camera setting reachable through the
  web GUI is also reachable through ISAPI.
- **LiveORC** — the cloud server that aggregates processed results
  from all ORC stations into a unified dashboard. Hosted at
  `openrivercam.endlessprojects.info` for this project.
- **Maintenance mode** — a remote kill-switch, controlled via the
  `orc-pmi-stations` GitHub repo, that sets a flag file
  (`/run/orc-maintenance-mode`) on station boot. When the flag is
  present, `orc-capture` exits without capturing, so field work does
  not collide with the 15-min timer.
- **Mbps** — megabits per second (10⁶ bits/s).
- **ORC (OpenRiverCam)** — the open-source platform for camera-based
  river surface velocity measurement. This repo is the Indonesia
  deployment *of* ORC; the platform itself lives in
  `github.com/localdevices/ORC` and `ORC-OS`.
- **orc-calibration-capture** — our helper script that captures a
  single calibration video, cleanly suspending the 15-min timer and
  maintenance gate. See `pi/shared/usr/local/bin/`.
- **orc-calibration-preflight** — our helper script that verifies the
  station is ready for calibration before the capture step. Checks
  camera reachability, ISAPI auth, clock drift, disk space, etc.
- **orc-capture** — the production capture script that runs every 15
  minutes on a systemd timer. See `ORC_CAPTURE.md`. Our calibration
  helpers delegate to it under the hood.
- **ORC-OS** — the Raspberry Pi operating system and web application
  developed by LocalDevices for ORC stations. Handles video ingestion,
  processing, and synchronization to LiveORC.
- **Pangolin** — the remote-access VPN service pre-installed on each
  station, used for over-the-internet SSH and ORC-OS web UI access.
- **PIV (Particle Image Velocimetry)** — cross-correlation technique
  that estimates 2D velocity fields by matching image patterns
  (interrogation windows) between successive frames. The core of
  pyorc's processing.
- **PoE (Power over Ethernet)** — technique for powering a network
  device (here, the camera) over the same Ethernet cable that carries
  its data. The ANNKE C1200 is a PoE camera.
- **Pose fit** — the optimization step that solves for camera pose
  and lens distortion given GCP 3D coordinates and their clicked
  pixel positions. Output: a 6-DoF pose, distortion coefficients, and
  an RMS reprojection error.
- **Processing recipe** — the set of algorithm parameters stored in a
  video configuration: frame range, spatial resolution (m/px), PIV
  window size, post-processing thresholds, etc.
- **Profile (camera profile)** — see *Camera profile*.
- **pyorc** — the Python library implementing ORC's processing
  pipeline (orthorectification, PIV, discharge integration). Docs:
  `https://localdevices.github.io/pyorc/user-guide/`.
- **Quality gate** — checks that `orc-capture` runs against a
  captured video (resolution, duration, bitrate, frame count) before
  delivering it to ORC-OS. Detailed in `ORC_CAPTURE.md`.
- **RMS reprojection error** — root-mean-square distance, in pixels,
  between each clicked GCP pixel location and where the solved pose
  re-projects the corresponding 3D GCP onto the image. Lower = better
  fit.
- **RTK FIX** — centimeter-accurate GNSS mode, achieved when the
  rover receives live correction data from a base station or NTRIP
  service and the integer ambiguity is resolved. The survey-quality
  mode — do not record GCPs in FLOAT or SINGLE modes.
- **RTSP (Real-Time Streaming Protocol)** — network protocol for
  delivering live media streams. `orc-capture` uses RTSP over TCP to
  pull video from the camera.
- **Session (calibration session)** — a named or date-stamped
  directory under `/home/pi/calibration/` that groups all artifacts
  from one calibration trip: preflight log, calibration videos,
  metadata sidecars, session log. Default session name is today's
  date.
- **Site ID** — the numeric identifier LiveORC assigns to a station.
  Set in `/callback_url` on ORC-OS so the daemon knows where to
  upload results.
- **Sidecar** — the `.json` file that `orc-calibration-capture`
  writes alongside each MP4 — records observed resolution, bitrate,
  duration, orc-capture.conf digest, camera IP, and
  validation-passed status.
- **SW Maps** — the Android app used in the field with the
  ArduSimple RTK rover for recording survey points and exporting them
  as GeoJSON.
- **systemd** — the Linux service and timer manager used to schedule
  `orc-capture.service` every 15 minutes.
- **UTM 48S (Universal Transverse Mercator, zone 48 South)** — the
  flat-meters projected CRS covering western Indonesia (roughly
  102°E–108°E). EPSG:32748. Easting is ~100k–900k meters; northing
  for Java is ~9.0M–9.5M.
- **Video configuration** — the full bundle of geometry (camera
  pose, cross-section, AOI) and processing recipe that ORC-OS binds
  to incoming videos. The subject of this document.
- **WGS84 (World Geodetic System 1984)** — the global lat/lon CRS
  that GPS devices report in. EPSG:4326. We reproject to UTM 48S
  before engineering work.
- **Witty Pi 5 HAT+** — the realtime-clock + power-scheduling board
  stacked on the Raspberry Pi. Controls the station's wake/sleep
  cycle on solar-powered Sukabumi.

---

## Changelog

- **v1.1 (2026-04-17):** Defined terms on first use; added glossary.
- **v1.0 (2026-04-17):** Initial version. Happy-path procedure with
  discovery callouts for first ANNKE C1200 deployment.
