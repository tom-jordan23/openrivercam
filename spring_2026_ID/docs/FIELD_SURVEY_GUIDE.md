# ORC Field Survey — Field Reference

**Version:** 1.0 — April 2026
**Purpose:** Abbreviated checklist for PMI field staff. Tom will provide
detailed guidance at each step. For full procedures, see
`survey/SURVEY_PROCESS_v3.md`.

**Equipment:**
- ArduSimple RTK rover (high-precision GPS receiver) + survey pole + spirit level (waterpass / bubble level)
- Android phone with GNSS Master + SW Maps (+ cell data for NTRIP (internet-based GPS correction service))
- Ground control point markers (high contrast — white/red or checkerboard)
- Notebook + pen (backup)
- Phone/tablet for photos of each GCP

**RTK corrections:** InaCORS NTRIP (primary) | Base station (fallback)
See `survey/InaCORS_HOWTO.md` for NTRIP setup.

---

## Day Before

- [ ] Charge all equipment (rover, phone, base station if needed)
- [ ] Verify InaCORS account is active and subscribed (Step 1.3 in InaCORS HOWTO)
- [ ] Confirm cell coverage at survey site (Telkomsel)
- [ ] Prepare GCP markers (minimum 8, high contrast)
- [ ] Load SW Maps project with site name and UTM zone

---

## At the Site — Before Survey

- [ ] Camera is mounted in final position and powered on
- [ ] Camera angle covers the full cross section (both banks, upstream to downstream)
- [ ] Connect rover to InaCORS NTRIP via GNSS Master
  - Host: `103.22.171.6`, Port: `2001`, Mountpoint: `VRS`
  - If no cell coverage: deploy base station instead (see SURVEY_PROCESS_v3 Section 4)
- [ ] Wait for **RTK FIX (highest-accuracy GPS mode)** (30-120 seconds, up to 5 min near equator)
- [ ] Verify: accuracy < 5cm, 12+ satellites, PDOP (Position Dilution of Precision — lower numbers are better) < 2.5
- [ ] **CRITICAL:** Do NOT run InaCORS and base station radio simultaneously

---

## Step 1: Place Ground Control Points

GCPs are reference points with known positions. The software uses them to calculate real distances from the camera image.

- [ ] Place **8-10 markers** visible in the camera's field of view
- [ ] Spread across **both banks** — left and right
- [ ] Spread **upstream to downstream** — not all in a line
- [ ] Cover a large part of the image, but not at the very edges
- [ ] Tilt markers slightly toward the camera
- [ ] Use high-contrast markers (white center + dark border, or checkerboard)

**Incorrect:** All points on one bank, or all in a straight line.
**Correct:** Points scattered across both banks and near/far from camera.

---

## Step 2: Record Calibration Video

- [ ] Verify all GCP markers are visible in the camera frame
- [ ] Clear the scene — **no people, boats, or obstructions** in view
- [ ] Record a **5-second video** (normal capture or manual trigger)
- [ ] Verify the video file exists and is not corrupted

**This video is critical** — it's used to calibrate the camera in ORC-OS.
If any GCP marker is moved or disturbed during the survey, record a second video at the end.

---

## Step 3: Survey GCPs

For each marker:
- [ ] Place rover pole on the **center** of the marker
- [ ] Hold pole **perfectly vertical** (check spirit level!)
- [ ] Wait for **RTK FIX** — do NOT record on FLOAT (medium accuracy — not reliable enough for survey) or SINGLE (low accuracy — not usable)
- [ ] Record the point in SW Maps
- [ ] Take a photo of the marker with your phone (for later ID)
- [ ] Label: GCP1, GCP2, etc. — match labels between survey data and photos

**Complete all GCP measurements in one continuous session. Do not turn off the base/NTRIP.**

---

## Step 4: Survey Cross Section

A line of bottom elevation points, **at a right angle (90 degrees) to the direction of water flow — crossing from one bank to the other**.

- [ ] Walk the rover across the channel perpendicular to flow
- [ ] Walk in as straight a line as possible
- [ ] Record more points where bottom shape changes
- [ ] Fewer points where bottom is flat
- [ ] **Go beyond what the camera sees** — measure the full channel width
  including banks above the water line
- [ ] For submerged points: note pole length (bottom to antenna center)

You may need to walk through the water. Keep the GPS antenna above the water surface at all times.

---

## Step 5: Survey Water Level

- [ ] Place the rover at the **water's edge** (where water meets land)
- [ ] Record this point
- [ ] Do this on at least one bank, ideally both

---

## Step 6: Survey Camera Position

- [ ] Place the rover as close to the **camera lens** as possible
- [ ] Record the point

---

## Step 7: Check Points (Quality Control)

Measure 2-3 GCPs a second time as independent check points.

- [ ] Re-measure at least 2 GCPs (do NOT reuse same measurement)
- [ ] Compare: difference should be **< 3cm horizontal, < 4cm vertical**
- [ ] If drift exceeds thresholds, investigate before leaving site

---

## Step 8: Before Leaving

- [ ] Verify all data saved (export from SW Maps)
- [ ] Photo of SW Maps point count screen (backup)
- [ ] Record second calibration video if any GCP marker was moved or disturbed
- [ ] Remove all markers and equipment from the site
- [ ] Quick count: GCPs + cross section + water level + camera position all present?

---

## Post-Survey (Office/Laptop)

See `survey/SURVEY_DATA_PROCESSING.md` for detailed steps.

- [ ] Export survey data as GeoJSON from SW Maps
- [ ] Convert coordinates to UTM format (a map coordinate system that uses meters) (see `survey/QGIS_Reproject_WGS84_to_UTM48S.md`)
- [ ] Split into two files: **GCPs** and **Cross section**
- [ ] Subtract pole length from cross section elevation (height) values
- [ ] Upload calibration video to ORC-OS
- [ ] Upload GCP file → match points to pixels in calibration video
- [ ] Upload cross section file
- [ ] Enter water level measurement
- [ ] Enter camera position
- [ ] Run calibration — verify GCP fit looks correct
- [ ] If the calibration results show large errors or the GCP positions do not match the video → **redo the survey**

---

## Common Mistakes

| Mistake | Why it matters |
|---------|---------------|
| All GCPs on one bank | Camera can't understand depth/perspective |
| GCPs in a straight line | Same problem — the software cannot calculate depth or distance correctly |
| Recording on FLOAT status | Position error 10-50cm |
| Tilted survey pole | Even small tilt = large error |
| Base + NTRIP running at same time | Silently wrong positions, no error flag |
| Cross section too short | Can't estimate flow at higher water levels |
| No calibration video | Survey is useless without it |
| People in calibration video | Interferes with GCP identification |
| Turning off base mid-survey | Coordinate system shifts — all points wrong |

---

## Field Reference: InaCORS NTRIP

| Parameter | Value |
|-----------|-------|
| Host | `103.22.171.6` |
| Port | `2001` |
| Mountpoint | `VRS` (Java/Bali/Sumatra) or `nearest` |
| Format | RTCM3 |
| Send GGA | Yes (required) |
| Account | Register at `http://nrtk.big.go.id/sbc/Account/Register` |

Full setup: `survey/InaCORS_HOWTO.md`
