# RIVER SURVEY PROCEDURE FOR OPENRIVERCAM DEPLOYMENTS — NTRIP WORKFLOW

**Equipment:** ArduSimple RTK rover + Android + GNSS Master + SW Maps + **InaCORS NTRIP** + Leica Disto X6 P2P (optional, for cross-sections)
**Target Accuracy:** Centimeter-level absolute positioning via NTRIP (~3-5cm)
**CRS:** UTM zone for your location (determine using instructions in Section 1)

> **Which document is this?** This is the NTRIP-only workflow — use it when cellular coverage is available at your site and you will receive real-time corrections from the InaCORS network. If cell coverage is unavailable at your site, use `SURVEY_PROCESS_v3_base.md` (local base station with PPP post-processing) instead.
>
> **Important:** Do not run a local base station at the same time as NTRIP. The rover must have exactly one correction source. A base station transmitting RTCM while the rover is also receiving NTRIP corrections will confuse the rover and produce unreliable positions. If you want to cross-validate the two methods, run them on separate sessions (see the cross-validation note below).

## HOW THIS WORKS: UNDERSTANDING THE APPROACH

### Why We Need Survey-Grade Positioning

River flow measurements from video rely on a precise chain of data transformations. The camera captures moving water as pixels. Software converts those pixels into real-world velocities. Those velocities integrate across the channel to produce discharge estimates. Each step in this chain amplifies errors from the previous step. A 5cm error in ground control point position translates to velocity errors of 5-10 cm/s. Those velocity errors compound into discharge uncertainties of 10-20%.

Survey-grade positioning prevents this error cascade. When you measure ground control points with centimeter accuracy, you establish a foundation that maintains precision through the entire processing chain. The camera transformation becomes reliable. The velocity calculations stay within acceptable bounds. The discharge estimates support confident decision-making.

### NTRIP: Network RTK Without a Base Station

Instead of deploying your own base station, you connect to Indonesia's InaCORS network — a system of permanent GNSS reference stations operated by BIG (Badan Informasi Geospasial). The network provides real-time corrections via NTRIP (Networked Transport of RTCM via Internet Protocol), delivered to your rover over a cellular data connection.

This is the **primary method** for Indonesia deployments where cell coverage is available (Sukabumi, Jakarta, and most of Java). Your rover receives corrections from the nearest CORS stations and achieves centimeter-accurate absolute positions directly in the field. No base station deployment, no survey-in, no multi-hour PPP post-processing. The positions you collect in the field are your final coordinates.

The key requirement is a cellular data connection between your phone and the InaCORS server. Bandwidth needs are minimal — about 1-2 KB/second, or roughly 30-60 MB for a full survey day. A Telkomsel prepaid SIM with any data package works.

**Survey-in is not required for NTRIP.** Survey-in is a procedure for establishing the position quality of a local base station. InaCORS reference stations already have precisely known coordinates, so the rover receives absolute positions directly. Survey-in only applies when you deploy your own base station (see the base station workflow document).

### Cross-Validation Against a Local Base Station (Optional)

For maximum confidence — especially on your first deployment — you can compare NTRIP results against a local base station + PPP result. Run the two methods on separate sessions (different days, or different sessions at the same check points on the same day). Do not run them simultaneously. Details:

1. Session 1 — Survey with InaCORS NTRIP (this document) at a set of check points
2. Session 2 — Survey the same check points using a local base station and PPP post-processing (see `SURVEY_PROCESS_v3_base.md`)
3. Compare NTRIP-derived coordinates against PPP-corrected coordinates at the same check points

If the two independent methods agree within 3-5 cm, both are working correctly. This "belt and suspenders" approach validates NTRIP against the established PPP workflow and builds trust in the simpler NTRIP-only workflow for future surveys.

### Laser Distance Measurement for Cross-Sections

The Leica Disto X6 with DST 360-X adapter (P2P mode) provides an alternative method for measuring river cross-sections when RTK wading is not possible. From a single instrument station on one bank, you can measure distances and height differences to points on the opposite bank — up to 200m range (400m with reflector target).

This complements RTK wading for rivers that are too deep, too fast, or too dangerous to cross on foot. The Disto measures bank geometry and exposed features; it cannot target the water surface directly. For submerged bed topography in deep rivers, other methods (acoustic sounding, estimation) are still needed.

### Quality Control Through Check Points

You cannot verify accuracy by measuring the same points you used to establish accuracy. This circular logic hides systematic errors. Check points solve this problem by providing independent validation — points you measure with the same precision as ground control points but never use in processing.

Think of check points as the answer key for a test. You solve the photogrammetric transformation using your ground control points, then check your solution against known positions you held back. The difference between predicted and actual check point coordinates reveals your system's true accuracy. If check point errors stay below 5cm, your velocity measurements will maintain acceptable uncertainty. If errors exceed 10cm, something went wrong — correction source, satellite geometry, atmospheric conditions, or measurement procedures.

This independent validation provides confidence that your system works correctly and quantifies the uncertainty in your final discharge estimates.

---

## TABLE OF CONTENTS

### DAY-BEFORE SETUP
1. [Software Setup](#1-software-setup)
2. [NTRIP Setup](#2-ntrip-setup)
3. [Equipment Check](#3-equipment-check)

### FIELD DAY
4. [RTK Corrections Setup](#4-rtk-corrections-setup)
5. [Check Points](#5-check-points)
6. [Camera & Control Points](#6-camera--control-points)
7. [Water Level Survey](#7-water-level-survey)
8. [Point Collection](#8-point-collection)
9. [Cross-Section Survey](#9-cross-section-survey)
10. [End of Day](#10-end-of-day)

### HAND-OFF
11. [Hand-Off to the Video Configuration Workflow](#11-hand-off-to-the-video-configuration-workflow)

### APPENDICES
- [A. GNSS Master Setup](#appendix-a-gnss-master-setup)
- [B. SW Maps Configuration](#appendix-b-sw-maps-configuration)
- [C. Sample Video Collection](#appendix-c-sample-video-collection)
- [D. Troubleshooting](#appendix-d-troubleshooting)
- [E. InaCORS Quick Reference Card](#appendix-e-inacors-quick-reference-card)
- [F. Survey Equipment Rental in Jakarta](#appendix-f-survey-equipment-rental-in-jakarta)

---

## SURVEY SUCCESS CRITERIA

Every field day must meet these thresholds. Missing any single criterion compromises data quality and invalidates the survey. These are not suggestions — they are requirements derived from error propagation analysis in photogrammetric velocity measurements.

- [ ] RTK FIX maintained throughout survey
- [ ] NTRIP connection active entire duration (correction age <5s)
- [ ] Check point drift ≤3cm H, ≤4cm V
- [ ] Min 12 satellites, PDOP ≤2.5

**Why These Thresholds:** RTK FIX ensures centimeter accuracy. If the rover drops to FLOAT solution even briefly, that measurement degrades to 10-50cm accuracy. Correction interruptions — NTRIP disconnection — force the rover back to autonomous mode (2-10 meter accuracy). Check point drift exceeding 3cm indicates systematic problems with corrections or atmospheric modeling. PDOP above 2.5 means poor satellite geometry that amplifies measurement errors. Fewer than 12 satellites reduces redundancy and increases vulnerability to signal obstructions.

---

## QUALITY GATES

**You must verify these conditions before saving each point.** The software can display good-looking numbers while the underlying solution remains unreliable. These gates prevent collecting data that appears acceptable in the field but fails during post-processing.

**Standard Environment:** RTK FIX ≥10s, PDOP ≤2.5, Sats ≥12, Precision ≤2cm H/3cm V
**Canal Environment:** RTK FIX ≥10s, PDOP ≤3.0, Sats ≥10, Precision ≤4cm H/6cm V

**Why Different Standards:** Canal environments often present challenging satellite visibility due to vegetation, terrain, or structures. The relaxed thresholds acknowledge these constraints while maintaining acceptable accuracy for discharge measurements. Standard environments should achieve optimal accuracy since nothing prevents it. Applying canal thresholds in open environments wastes the opportunity for better precision.

**Understanding PDOP:** Position Dilution of Precision (PDOP) measures satellite geometry quality. PDOP multiplies your receiver's base precision to produce actual position error. With 1cm receiver precision and PDOP of 2.5, expect ~2.5cm actual error. PDOP above 6 means satellites cluster in one part of the sky — weak geometry that amplifies errors. PDOP below 2 indicates excellent satellite distribution across the sky dome.

**Why 10 Seconds:** RTK solutions can briefly achieve FIX status, then lose it. Requiring 10 seconds of stable FIX ensures the solution is robust, not a momentary convergence. This prevents recording points just as the solution degrades.

---

# DAY-BEFORE SETUP

Testing at home prevents discovering problems in the field. Every connection point in this system can fail — USB cables, mock location permissions, coordinate system settings, quality threshold configurations, NTRIP credentials. Finding failures at your desk costs minutes. Finding them at a remote river site costs hours and potentially invalidates the field day.

## 1) Software Setup

### Why This Matters

The positioning chain flows from the NTRIP correction source through the rover to GNSS Master to SW Maps. A misconfiguration anywhere in this chain breaks the entire system. USB debugging must be enabled or Android blocks the connection. Mock location must designate GNSS Master or the operating system ignores external GPS data. The coordinate system must match your processing workflow or points end up in the wrong location.

Testing the full system integration reveals these problems before they matter. You want to discover that SW Maps doesn't recognize RTK FIX status while sitting at home with documentation available, not while standing in a river trying to remember obscure settings.

### Android & GNSS Master
- [ ] Install GNSS Master app → [Full setup guide](#appendix-a-gnss-master-setup)
- [ ] Enable Developer Options, Mock Location
- [ ] Test USB connection with rover
- [ ] Verify mock location works with test apps

**Developer Options:** Android hides these settings by default. You must tap Build Number seven times to unlock them. This feels like a hack because it is — Google doesn't want average users enabling features they don't understand. You need these features because you're replacing the phone's internal GPS with survey-grade external positioning.

**Mock Location:** This setting tells Android which app is allowed to override the internal GPS. Without this designation, Android ignores GNSS Master's position data and continues using the phone's internal GPS — which provides 3-10 meter accuracy instead of centimeter-level precision. Verify this works by opening Google Maps and confirming it shows the external receiver's position.

### SW Maps Project
- [ ] Create new project → [Full configuration guide](#appendix-b-sw-maps-configuration)
- [ ] Determine correct UTM zone for your location → [Instructions below](#determining-your-utm-zone)
- [ ] Set CRS to your UTM zone EPSG code (example: EPSG:32748 for UTM 48S)
- [ ] Create survey layers with attributes
- [ ] Test GPS integration with GNSS Master

**Coordinate System Criticality:** Your UTM zone provides metric coordinates for your survey area. Getting this wrong means your points save in the wrong coordinate system — potentially wrong by hundreds of kilometers after transformation. SW Maps remembers this setting per project, so configure it correctly now rather than discovering mismatched coordinates during post-processing.

### Determining Your UTM Zone

The Universal Transverse Mercator system divides Earth into 60 north-south zones, each 6° of longitude wide. Using the correct zone for your location ensures minimal distortion and accurate metric coordinates.

**Find Your UTM Zone:**

1. **Locate your site coordinates** in decimal degrees (use Google Maps: right-click → "What's here?")
   - Example: Sukabumi, Indonesia = -6.9175°, 106.9269°

2. **Calculate UTM zone number** from longitude:
   - Formula: `Zone = floor((Longitude + 180) / 6) + 1`
   - Example: `floor((106.9269 + 180) / 6) + 1 = floor(47.82) + 1 = 48`
   - Or use online calculator: https://www.dmap.co.uk/utmworld.htm

3. **Determine hemisphere:**
   - Positive latitude (north of equator) = North (N)
   - Negative latitude (south of equator) = South (S)
   - Example: -6.9175° = South

4. **Find EPSG code:**
   - Northern hemisphere: `326XX` where XX is the zone number
   - Southern hemisphere: `327XX` where XX is the zone number
   - Example: Zone 48 South = 32748
   - Verify at https://epsg.io/

**Complete Example (Sukabumi, Indonesia):**
- Coordinates: -6.9175°, 106.9269°
- Zone: 48
- Hemisphere: South
- UTM designation: 48S
- EPSG code: 32748
- Full name: WGS 84 / UTM zone 48S

**Important Notes:**
- If your site spans a zone boundary, pick the zone containing most of the site
- Stay within the same zone for all related surveys
- Record the EPSG code in your field notes for reference

### Point Naming Convention

The post-processing script (`orc_survey_prep.py`) classifies each feature by matching the point name prefix. Name points in SW Maps according to the table below so the exported GeoJSON feeds directly into the script without manual cleanup.

| Point type | Name pattern | Examples |
|------------|--------------|----------|
| Ground control points | `GCP1`, `GCP2`, ... (sequential) | `GCP1` ... `GCP10` |
| Discharge cross-section stations | `XS1`, `XS2`, ... (traversal order, LB → RB) | `XS1` ... `XS15` |
| Water level edge points | `WL1`, `WL2`, ... (one per bank typical) | `WL1`, `WL2` |
| Camera position | `CAM` (exactly one) | `CAM` |

**Other points are ignored by the script** — check points (`CP_START`, `CP_NOON`, `CP_END`), camera FOV markers, and any second cross-section used only for water-level documentation. The script reports them as "unrecognized labels" warnings, which is expected. They stay in your GeoPackage for field records but do not flow into ORC processing.

**Why the prefix matters:** the script sorts features into `gcps.csv`, `cross_section.csv`, `water_level.csv`, and `camera_position.csv` purely from the name prefix. A GCP saved as "Point 3" instead of `GCP3` is skipped with a warning and never reaches the ORC pose fit.

**Numbering:** number sequentially without gaps. The script warns when it sees gaps (e.g. `GCP1, GCP2, GCP4`), because a gap usually means a point was lost or mislabeled.

### Integration Test
- [ ] Full system test: Rover → GNSS Master → SW Maps
- [ ] Verify RTK status appears in SW Maps
- [ ] Test point collection with quality thresholds

**Full System Verification:** Power on the rover, connect via USB, open GNSS Master, launch SW Maps. You should see satellite count, PDOP values, and precision estimates. Without NTRIP corrections active, you won't see RTK FIX — but you can verify that the data pipeline works end-to-end. Save a test point and verify all attributes populate correctly.

**Quality Threshold Testing:** Configure SW Maps to reject points that don't meet your quality gates. This prevents accidentally recording poor-quality data when you're focused on field logistics rather than data validation screens.

---

## 2) NTRIP Setup

### Why This Matters

NTRIP delivers network corrections from InaCORS — Indonesia's national CORS network — directly to your rover over cellular data. Setting this up the day before ensures your credentials work, the connection is stable, and you won't waste field time debugging network issues.

### InaCORS Registration
- [ ] Register at http://nrtk.big.go.id/sbc/Account/Register (free)
- [ ] Receive username and password via email
- [ ] Log in to verify account is active: http://nrtk.big.go.id/sbc/

**Registration Timing:** Register at least 2-3 days before your field day. Account activation may take 1-2 business days. The portal is in Indonesian — use browser translation if needed. A local phone number (Telkomsel SIM) may be required for registration.

### Check Coverage at Your Site
- [ ] Visit https://srgi.big.go.id/page/service-check
- [ ] Enter your site coordinates or browse the map
- [ ] Verify your site is within InaCORS coverage (green zone)

**Coverage Assessment:** Both Sukabumi and Jakarta are in areas with excellent InaCORS coverage on Java. If your site shows poor coverage or no coverage, NTRIP will not work reliably at your site — switch to the base station workflow (`SURVEY_PROCESS_v3_base.md`).

### NTRIP Client Configuration

Configure the NTRIP client in **SW Maps** (preferred — simplest setup) or **GNSS Master**:

| Setting | Value |
|---------|-------|
| **NTRIP Caster Host** | `103.22.171.6` (the caster is reachable by IP only — the `nrtk.big.go.id` hostname does not resolve for the NTRIP service) |
| **Port** | `2001` (**not** 2101 — InaCORS uses a non-standard port) |

> **Confirm the current IP before each field day.** The caster IP can change. Before your field day, log in to the InaCORS portal (http://nrtk.big.go.id/sbc/) and verify the caster address in the service details or announcements. If the IP listed above no longer works, check the portal for the current one.
| **Mountpoint** | `VRS` (primary) or `nearest` (fallback) |
| **Username** | Your InaCORS username |
| **Password** | Your InaCORS password |
| **Send NMEA GGA** | **Yes** (required for VRS — the caster needs your position) |
| **NTRIP Version** | 1.0 |

**Port 2001:** This is the most common source of connection failure. Standard NTRIP port is 2101 — InaCORS uses 2001. If your client auto-fills 2101, change it manually.

**VRS vs Nearest:** VRS (Virtual Reference Station) interpolates corrections from surrounding CORS stations tailored to your location — best accuracy. The "nearest" mountpoint connects to the single closest station — simpler but accuracy degrades with distance. Use VRS as primary, nearest as fallback.

**Send NMEA GGA:** The VRS mountpoint needs your approximate position to generate corrections for your location. Your NTRIP client sends this automatically via NMEA GGA messages. If this is disabled, VRS won't work — you'll get an error or no corrections.

### Cell Data Requirements
- [ ] Working SIM with data plan (Telkomsel recommended for best rural coverage)
- [ ] Verify 4G/LTE signal at or near your survey site
- [ ] Budget: ~30-60 MB for a full survey day (minimal bandwidth)

### Test the NTRIP Connection
- [ ] Connect rover to phone via USB
- [ ] Open GNSS Master → verify rover connected
- [ ] Open SW Maps → start NTRIP client with InaCORS settings
- [ ] Verify corrections flowing: correction age should update every 1-2 seconds
- [ ] Wait for RTK FIX (may take 10-60 seconds with NTRIP)
- [ ] If testing indoors: you may not achieve FIX, but verify the NTRIP connection establishes and correction data flows

**What Success Looks Like:** SW Maps or GNSS Master shows "NTRIP Connected" (or similar), correction age counts up from 0-1 seconds, and if you're outdoors with good sky view, the solution transitions from FLOAT to FIX within 1-2 minutes.

---

## 3) Equipment Check

Calculate your power budget conservatively — the rover runs 6-8 hours, the Android device 4-6 hours with screen on. With NTRIP, you don't need base station power, but the continuous cell data connection drains the phone battery faster than normal.

**Power Systems:**
- [ ] Rover: Full charge
- [ ] Android: 100% + power bank (NTRIP uses continuous cell data, which drains battery faster)
- [ ] All USB cables tested

**Cable Testing:** Test every cable you'll use by verifying data transfer, not just charging. A cable that charges a device might not support the USB serial communication the rover needs.

**Physical Equipment:**
- [ ] Survey poles (primary + backup), bipod if available
- [ ] Steel tape measure, markers
- [ ] Waterproof notebook, pencils
- [ ] If using Disto X6 P2P: Verify complete P2P package (Disto X6 + DST 360-X + TRI 120 + GZM 3), battery charged, test P2P function

**Redundancy Philosophy:** Bring backup survey poles. If you drop your primary pole in the river or damage it on rocks, you need a replacement immediately. The same applies to markers, notebooks, and anything else that's small, inexpensive, and critical to operations if lost.

---

# FIELD DAY

## 4) RTK Corrections Setup

This section establishes your correction source — the foundation for all measurements that follow. With NTRIP, your rover receives corrections from InaCORS via your phone's cellular data connection. No physical base station is used.

### Setup
- [ ] Power on rover, connect to phone via USB
- [ ] Open GNSS Master, verify rover connected
- [ ] Open SW Maps, start NTRIP client (settings from Section 2)
- [ ] Verify NTRIP connected and corrections flowing (correction age updating)
- [ ] Wait for RTK FIX — typically 10-60 seconds outdoors
- [ ] Verify: RTK FIX, PDOP ≤2.5, Satellites ≥12

**What to Monitor:** Correction age should stay below 5 seconds. If it climbs above 10 seconds, the NTRIP connection is intermittent. Above 30 seconds, the RTK solution will degrade to FLOAT. Watch for cell signal drops, especially near rivers in valleys.

**If NTRIP Won't Connect:** Try the fallback mountpoint ("nearest" instead of "VRS"). If that fails, check cell signal. If cell coverage is genuinely unavailable at your site, NTRIP cannot be used — switch to the base station workflow (`SURVEY_PROCESS_v3_base.md`) for this session.

**Do Not Run a Local Base Station Simultaneously:** If you also deploy a base station that transmits RTCM corrections while the rover is connected to NTRIP, the rover will receive two conflicting correction streams. This produces unreliable positions. Choose one correction source per session. If you want to cross-validate NTRIP against a base station + PPP result, run the two methods on separate sessions.

---

## 5) Check Points

Check points provide the only independent validation of your system accuracy. Without them, you're assuming your measurements are correct with no evidence. With them, you can quantify actual error and demonstrate that your data meets accuracy requirements.

### Why We Establish Check Points First

Survey check points at the start of the day, after 4-6 hours, and at the end of the day. This temporal sequence reveals whether your correction source drifts or your RTK solution degrades over time. Atmospheric conditions change throughout the day — ionospheric delays follow solar activity patterns, tropospheric delays respond to temperature and humidity changes. These changing conditions can cause apparent position shifts.

If your check point measurements agree within 3cm across the entire day, your system maintains stable accuracy. If drift exceeds 3cm, something changed — correction source problems, atmospheric modeling failure, or satellite geometry degradation. You need to identify and correct the problem before using that day's data.

### Establish CP_START
- [ ] 20-50m from survey area, stable high ground
- [ ] RTK FIX for 30 seconds
- [ ] 3 independent 60s measurements
- [ ] Agreement within 1cm H, 2cm V
- [ ] Mark permanently, photograph

**Distance from Survey Area:** Check points should be in representative conditions — similar satellite visibility and multipath environment as your survey points. The 20-50m range achieves this balance. Too close to obstructions and you're not testing real survey conditions. Too far and you might encounter different local conditions.

**Three Independent Measurements:** Measure the point, move the pole completely off the mark, then remeasure. Do this three times with 60 seconds of occupation each time. Calculate the spread in coordinates. If the three measurements don't agree within 1cm horizontal and 2cm vertical, your RTK solution is unstable — either poor satellite geometry, multipath contamination, or insufficient convergence time. Don't proceed with surveying until you resolve this.

**Why This Agreement Matters:** You're testing repeatability — the receiver's ability to measure the same point consistently. If you can't measure one point three times with centimeter agreement, you can't trust any individual measurement to be correct within centimeters. This test validates that your system delivers the precision you need before you invest hours measuring ground control points.

**Permanent Marking:** Drive a stake, spray a paint mark, or create a described position from photos. You'll return to this exact point twice more today. You might return to it on future field days to validate long-term system stability.

### Monitor Throughout Day
- [ ] CP_NOON: Re-measure after 4-6 hours
- [ ] CP_END: Final check before packing
- [ ] Total drift must be ≤3cm H, ≤4cm V

**Interpreting Drift:** Small drift (≤3cm) is normal and acceptable — atmospheric conditions change, satellite geometry evolves, receiver noise is random. Drift in this range doesn't compromise survey quality because it's smaller than your required accuracy threshold.

Drift exceeding 3cm horizontal or 4cm vertical signals problems. With NTRIP, this could indicate CORS station issues, poor VRS interpolation, or intermittent corrections. Investigate the cause and decide whether to continue surveying or restart.

**What to Do If Drift Exceeds Limits:** Stop surveying. Verify corrections are flowing (correction age <5s), check cell signal stability, try switching from VRS to nearest mountpoint. If problems persist, consider restarting the correction setup or postponing the field day.

---

## 6) Camera & Control Points

Ground control points tie the camera's pixel coordinate system to real-world UTM coordinates. The transformation quality depends on having well-distributed points with accurately known positions. Poor GCP distribution — clustering in one area or all at similar distances from the camera — creates a weak geometric solution that increases velocity uncertainty.

### Why GCP Distribution Matters

Imagine trying to level a table using only three points, all on one side. The other side remains unconstrained. GCP distribution follows the same principle. Points around the perimeter of the camera view constrain the transformation across the entire image. Points clustered in one area leave other regions poorly constrained.

Photogrammetric transformation errors increase with distance from the nearest GCP. If you measure five GCPs on the left bank but none on the right bank, velocity measurements on the right side will have higher uncertainty than those on the left. The software can still calculate velocities — but the errors might be 2-3 times larger in unsupported regions.

### Camera Position
- [ ] 5-10m height, 15-45° viewing angle
- [ ] Survey camera position with rover — save the point named exactly `CAM`
- [ ] Record height, direction, tilt angle

**Why Survey Camera Position:** Knowing the camera's exact position and orientation helps to reconstruct the scene when sorting through GIS points later. Ensuring that you have points for the camera and field of view can help you spot any survey locations that are outside the camera's view, etc.

**Recording Geometry:** Note the camera height above ground, compass direction it faces, and tilt angle. These parameters help reconstruct the viewing geometry during processing and support quality control checks. If calculated GCP positions don't align with observed camera geometry, something went wrong — either the GCP measurements or the processing.

### Control Points
- [ ] Place 6+ visible targets in camera FOV
- [ ] Take sample video → [Detailed procedure](#appendix-c-sample-video-collection)
- [ ] Survey each control point after video
- [ ] Save points to the **Ground Control Points** layer, named `GCP1`, `GCP2`, ... in the order you measure them ([naming convention](#point-naming-convention))

**Minimum Six Points:** Photogrammetric transformation solves for camera position, orientation, and lens distortion. This requires at least 6 ground control points with known 3D coordinates. More points improve the solution robustness and allow detecting outliers. Aim for 8-10 GCPs for reliable transformation. Having extras also allows you to discard points that don't resolve well in configuration.

**Survey After Video:** You need the video to show where the targets are positioned while the water is flowing. Survey the targets after recording because you'll spend 60+ seconds per point and can't leave the camera running that long. This sequence ensures the video captures representative flow conditions while the survey achieves required precision.

**Target Visibility:** Each target must be clearly identifiable in the video and accurately measurable in the field. High-contrast colored panels (orange, white, or checkerboard patterns) work well. Retroreflective tape improves visibility. Position targets on stable surfaces — rocks, concrete, driven stakes — not vegetation that might move in the wind.

---

## 7) Water Level Survey

Water surface elevation provides the reference datum for all cross-section measurements and enables converting surveyed bed elevations into flow depths. This simple measurement is surprisingly important — a 2cm error in water level produces a 2cm error in calculated depth for every point in the cross-section.

### Why Water Level Accuracy Matters

Discharge calculations integrate velocity across the cross-sectional area. Area depends on width (easy to measure accurately) and depth (depends on bed elevation and water surface elevation). If your water level measurement is wrong by 5cm, every depth value is wrong by 5cm, and the entire cross-sectional area shifts by channel_width × 0.05m. For a 10m wide channel, that's 0.5 m² of area error, which translates directly to discharge error.

### Setup
- [ ] Identify stable water level measurement point
- [ ] Use staff gauge or direct measurement method
- [ ] Record water surface conditions (calm/turbulent)

**Stable Measurement Location:** Avoid turbulent zones, surface boils, eddy lines, or wave action. Find a calm section where the water surface stays relatively level. In rivers with significant turbulence, you might need to average multiple measurements or accept higher uncertainty.

**Surface Conditions:** Note whether the water is calm, choppy, or turbulent. This metadata helps interpret measurement uncertainty and explains discrepancies during quality control. A ±2cm measurement in calm water is more reliable than ±2cm in turbulent conditions where the surface varies by 5-10cm.

### Measurement
- [ ] Survey water surface elevation with rover pole
- [ ] **Note depth on pole**, maintain RTK FIX
- [ ] Save to the **Water Level** layer, named `WL1`, `WL2`, ... (one per bank typical — [naming convention](#point-naming-convention))
- [ ] Take multiple measurements if water is moving
- [ ] Document measurement method and accuracy

**Pole Depth Recording:** You're measuring the water surface, not the pole tip. Hold the pole vertically with the tip submerged some distance below the surface. Note exactly where the water line crosses the pole. Measure this depth later with a tape measure. The water surface elevation equals the surveyed pole position minus the pole height measurement plus the depth below water.

Calculate the water level in azimuthal altitude (meters): `Water_Surface_Elevation = GPS_Position_Z - Pole_Height + Depth_Below_Surface`. Altitude (Z) will be displayed by default in Azimuth meters in SWMaps, so you can just subtract the pole height and then add back the submerged pole depth to get water surface level.

**RTK FIX Requirement:** This measurement needs the same accuracy as ground control points. Wait for stable RTK FIX, verify PDOP ≤2.5 and satellites ≥12, then occupy the position for 60 seconds. Don't shortcut this measurement because it affects every depth calculation.

**Multiple Measurements:** If the water surface moves (waves, turbulence, fluctuations), take 3-5 measurements and average them. This reduces the impact of instantaneous surface variations. Note the range of measurements as an uncertainty estimate.

---

## 8) Point Collection

Every point you save becomes part of your dataset. There's no "fixing" poor-quality points during post-processing — the errors are baked in. Quality gates prevent saving data that looks acceptable on-screen but contains hidden problems that emerge during analysis.

### Why Quality Gates Matter

RTK receivers display position information continuously, updating every second. These displays show positions even when the solution is poor — FLOAT mode with 50cm accuracy or autonomous mode with 5m accuracy. The coordinates appear on-screen with the same confidence as centimeter-accurate FIX mode. Nothing in the display says "this is wrong" — you must check solution status, PDOP, satellite count, and precision estimates to know whether the position is reliable.

Quality gates enforce these checks. Configure SW Maps to require RTK FIX, PDOP ≤2.5, satellites ≥12, and precision ≤2cm horizontal before allowing point saves. This prevents recording bad data when you're distracted by field logistics and not watching the status indicators carefully.

### Quality Requirements
- [ ] All quality gates met (see top of document)
- [ ] Averaging times: 60s standard, 120s canal
- [ ] Pole bubble centered, measure height each shot

**Averaging Time:** RTK positions jump around by ±1-2cm even in FIX mode due to remaining atmospheric noise, multipath, and receiver noise. Averaging over 60 seconds reduces this scatter and provides a more stable position. Longer averaging (120s) helps in challenging environments where signal quality is marginal.

Don't shortcut the averaging time. The software might achieve FIX status after 10 seconds, but that doesn't mean the position is fully converged. The full averaging period ensures the solution stabilizes and produces repeatable results.

**Pole Bubble:** Survey poles include a bubble level. Center it precisely before saving the point. A tilted pole introduces horizontal position error and elevation error. A 2m pole tilted 5° displaces the tip by ~17cm horizontally — far beyond your accuracy target. Keep the pole vertical.

**Measure Pole Height Every Shot:** Pole height measures from the GPS antenna to the pole tip. This varies slightly depending on how you configure the pole sections. Measure it with a tape measure before each point or at minimum verify it hasn't changed. A 1cm error in pole height produces a 1cm elevation error in the final coordinate.

### Standard Protocol
- [ ] Verify RTK FIX ≥10 seconds
- [ ] Check precision estimates in SW Maps
- [ ] Record all required attributes
- [ ] If conditions fail: wait 2min → move 2-3m → retry

**Precision Estimates:** SW Maps displays horizontal and vertical precision values calculated by the receiver. These represent the receiver's confidence in its position solution based on satellite geometry, signal quality, and correction age. Precision ≤2cm horizontal and ≤3cm vertical indicates good conditions. Higher values suggest problems even if you have RTK FIX status.

**Failure Recovery:** Sometimes a location has poor satellite visibility — tree cover, terrain shadowing, buildings. The receiver can't achieve FIX or maintains marginal quality. Wait 2 minutes to see if conditions improve as satellites move. If not, move 2-3 meters to escape multipath or obstruction issues. If problems persist, that location might not be measurable with your current setup — document it and consider an alternative GCP location.

**What to record per point:** the only attribute you set by hand is the point name, using the [naming convention](#point-naming-convention). SW Maps automatically records measurement time, PDOP, satellite count, horizontal/vertical precision, and fix status with each save. Add a short note only when something unusual affects the measurement (e.g. partial obstruction, unstable footing).

---

## 9) Cross-Section Survey

Cross-section surveys map the channel bed geometry from left bank to right bank. This data supports discharge calculations, validates rating curves, and documents channel changes over time. The survey accuracy requirements match those for ground control points — centimeter-level precision for reliable results.

### Why Systematic Collection Matters

You're creating a spatial model of the channel bed. Models work best with evenly spaced, high-quality data points. Clustering measurements in easy-to-reach areas while skipping difficult sections creates gaps that interpolation must fill. These gaps introduce uncertainty. Systematic spacing ensures the model accurately represents the bed geometry without artifacts from irregular sampling.

### Setup
- [ ] Establish LB/RB reference points on stable ground
- [ ] Plan station spacing (1-2m typical)
- [ ] Document section ID, flow conditions
- [ ] Plan to conduct two cross sections — one for discharge and another for water level

**Reference Points:** Mark clear left bank and right bank endpoints. Survey these with the rover to establish precise coordinates. They serve as anchor points for the cross-section and enable returning to the same transect line in future surveys. If you're monitoring temporal changes, you need to measure the same cross-section each time — these reference points make that possible.

**Station Spacing:** Choose spacing based on bed complexity. A uniform, smooth bed might need only 2m spacing. A complex bed with boulders, steps, or vegetation needs tighter spacing (1m or less) to capture features adequately. In the deepest part of the channel where velocity and flow are highest, tighter spacing improves accuracy since this zone contributes most to discharge.

**Flow Conditions:** Record whether the water is low, medium, or high flow, and whether it's rising or falling. This context helps interpret the discharge measurements and relate them to other hydrological data. Note any unusual conditions — debris accumulation, ice, aquatic vegetation — that might affect either the survey or the flow.

### Method A: RTK Wading (Primary Method)

RTK wading is the primary cross-section method — walk the transect with the rover pole, measuring bed elevation at each station. Use this for shallow, safe rivers where you can wade across.

#### Collection
- [ ] Walk LB → RB systematically
- [ ] Capture all water levels at both banks
- [ ] Each station: verify quality gates, 60-120s averaging
- [ ] Save to the **Discharge Cross Section** layer, named `XS1`, `XS2`, ... in the order you walk them (LB → RB — [naming convention](#point-naming-convention))
- [ ] Record water depth at each station (for cross-check against computed depth)
- [ ] Measure pole height tip-to-ARP each shot

**Systematic Traverse:** Start at left bank and walk toward right bank, measuring at planned intervals. Don't skip stations because they're difficult to reach or in deep water. Those difficult stations often represent important geometric features. If a station is truly impossible to measure safely using a pole, a bathymetric survey with sonar and GPS might be a better approach.

**Quality Verification:** Check RTK FIX status, PDOP, and satellite count before every point. Don't assume conditions remain good just because the previous point worked. Satellite geometry changes continuously, and local obstructions affect each position differently.

**Water Depth Recording:** At each station in the wetted channel, note the depth from the water surface to the bed. This provides redundant information — you're also calculating depth from the difference between water surface elevation and surveyed bed elevation. The two methods should agree within a few centimeters. If they don't, you've found a measurement error to investigate.

**Station Numbering:** Walk left bank → right bank and number stations as you go (`XS1` at LB, increasing toward RB). The point name *is* the station number — no separate attribute needed. The script sorts by the numeric suffix, so `XS2` always comes before `XS10` even if you saved them out of order.

### Method B: Disto X6 P2P (Optional — When Wading Is Not Possible)

If a Leica Disto X6 P2P is available, use it to measure cross-section points on rivers that are too deep, fast, or dangerous to wade. This method measures from one bank; it does not replace RTK wading where wading is feasible.

#### When to Use Disto P2P vs RTK Wading

| Condition | Method |
|-----------|--------|
| Shallow, safe river you can walk across | **RTK wading** (primary) |
| River too deep or fast to wade safely | **Disto P2P** (if available) |
| Need submerged bed topography | **RTK wading** (Disto can't target water surface) |
| Measuring bank geometry from a distance | **Disto P2P** |
| Both banks accessible on foot | **RTK wading** (higher accuracy) |

#### Equipment Required

The complete P2P package (SKU 950878):
- [ ] Leica Disto X6 — laser distance meter
- [ ] DST 360-X — precision tilt/pan adapter
- [ ] TRI 120 — tripod
- [ ] GZM 3 — reflective target plate (for targets >60m in bright conditions)

#### Setup

1. **Choose instrument station on one bank:**
   - Clear line of sight across the full cross-section
   - Stable ground (not soft mud or sand)
   - 2-5m back from bank edge for stability

2. **Set up tripod and mount Disto:**
   - Extend TRI 120 tripod legs, press firmly into ground
   - Mount DST 360-X adapter (5/8" thread)
   - Attach Disto X6 to adapter
   - Power on, allow compensator to self-level
   - Verify level indicator shows centered

3. **RTK-survey the instrument station position:**
   - Place rover pole adjacent to the tripod center
   - Survey with standard quality gates (60s, RTK FIX)
   - Record instrument height (tripod top to ground)
   - This gives the Disto an absolute position in UTM

4. **RTK-survey a reference direction point:**
   - Survey a second visible point 20+ meters away
   - This establishes the azimuth orientation for converting Disto angles to UTM bearings
   - Calculate bearing: `azimuth = atan2(ΔE, ΔN)` from instrument to reference point

#### Measurement Procedure

1. **Select P2P mode** on the Disto X6 (Menu → P2P)

2. **Aim at reference direction point first** to establish orientation

3. **Measure cross-section points systematically (LB → RB):**
   - Aim at each visible feature along the cross-section
   - Fire laser — record horizontal distance and height difference
   - Work systematically from left bank to right bank

4. **Use GZM 3 reflector plate for distant targets:**
   - Targets >60m in bright sunlight may not return enough signal
   - Have an assistant hold the reflector plate at the target point
   - Extends effective range to ~400m

5. **Take 3-5 repeat measurements per point and average:**
   - Discard obvious outliers (>3× typical spread)
   - Averaging reduces random angular error

#### Accuracy Expectations

| Target Distance | Lateral Accuracy (±0.1° angle) | Distance Accuracy |
|-----------------|-------------------------------|-------------------|
| 20 m | ±35 mm | ±1 mm |
| 50 m | ±87 mm | ±1 mm |
| 100 m | ±175 mm | ±1 mm |

- Adequate for monitoring-grade cross-sections on rivers up to ~50m wide
- Not sufficient for hydraulic model calibration requiring <2cm accuracy
- Distance accuracy (±1-2mm) is excellent regardless of range — angle is the limiting factor

#### Combining Disto Data with RTK Data

1. **Instrument station position** from RTK provides the absolute reference (E₀, N₀, Z₀)
2. **Reference direction** from RTK provides azimuth orientation
3. **For each Disto point**, convert polar to UTM:
   ```
   E = E₀ + horizontal_distance × sin(reference_azimuth + relative_angle)
   N = N₀ + horizontal_distance × cos(reference_azimuth + relative_angle)
   Z = Z₀ + height_difference
   ```
4. Combined accuracy: RTK station error (~3cm) + Disto angular error (distance-dependent)

#### Field Tips for Indonesia

- **Measure early morning or late afternoon** — avoid noon sun (heat shimmer distorts laser, bright light reduces dot visibility)
- **Cannot target water surface directly** — aim at bank features, stakes, or reflector plate held by an assistant
- **IP65 rated** — fine in light rain, but wipe lens if water droplets form; avoid heavy downpours
- **Battery lasts ~8 hours** — USB-C rechargeable, bring a power bank
- **Overcast days are ideal** for laser measurement — consistent lighting, less shimmer

#### Rental Note

Contact **Leica Store Jakarta** (Plaza Senayan, 3rd floor) or **Indosurta Group** for P2P package rental. Verify the complete package: Disto X6 + DST 360-X + TRI 120 + GZM 3. Test P2P function before leaving the shop. Alternative: rent a total station if the Disto P2P package is unavailable.

---

## 10) End of Day

The survey isn't complete until you've verified data quality, backed up files, and documented any deviations from standard procedure. Leaving the field site with unverified data means discovering problems when you can't return to fix them.

### Final Checks
- [ ] Re-measure CP_END, calculate total drift
- [ ] Export SW Maps data (CSV + geopackage)
- [ ] Multiple backups on different devices
- [ ] Document any deviations from protocol

**Check Point Verification:** The CP_END measurement tells you whether your system maintained accuracy throughout the day. Compare it to CP_START coordinates. If drift exceeds 3cm horizontal or 4cm vertical, you have a problem that requires investigation. Don't wait until you're back at the office to discover this — check it while you're still on-site with the equipment available to diagnose issues.

**Data Export:** SW Maps stores data in an internal database. Export it to CSV (human-readable, easy to process) and native GeoPackage format (preserves coordinate system metadata and attributes). Save both formats. CSV provides compatibility with generic processing tools. GeoPackage preserves spatial information correctly for GIS software.

**Multiple Backups:** Copy the exported files to at least two separate devices immediately — Android storage, USB drive, laptop, cloud storage. Memory cards fail. Phones get dropped in rivers. Having multiple backups means no single failure loses your day's work. Don't wait until evening at the hotel — back up on-site before leaving.

**Deviation Documentation:** If anything didn't go according to plan — abbreviated averaging times, relaxed quality thresholds, skipped check points, NTRIP disconnections — document it in writing while the details are fresh. These notes explain data anomalies during processing and help assess whether the data remains usable for its intended purpose.

---

# POST-PROCESSING

## 11) Hand-Off to the Video Configuration Workflow

With NTRIP, your field data already has centimeter-level absolute accuracy in SRGI2013 (≈ WGS84 for practical purposes). **No PPP post-processing, no coordinate translation, no QGIS work is required** — the positions you collected are your final coordinates.

From here, the survey procedure ends and the video configuration procedure takes over. Follow **Phase 4 of `../spring_2026_ID/docs/VIDEO_CONFIG_SETUP.md`** ("Office: Survey Data Prep"). Phase 4 drives the helper script `survey/orc_survey_prep.py`, which:

- Reprojects the GeoJSON from WGS84 (lat/lon) to your target UTM zone
- Subtracts pole length from GCP and cross-section elevations
- Splits the export into `gcps.csv`, `cross_section.csv`, `camera_position.csv`, `water_level.csv`
- Writes a `metadata.yaml` session record
- Runs a battery of cross-checks (GCP count and spread, numbering gaps, duplicate points, camera elevation vs. `h_ref`, UTM bounds, etc.)

### Hand-Off Checklist

- [ ] Export the survey from SW Maps as **GeoJSON** (EPSG:4326 WGS84 — the default)
- [ ] Confirm every feature the ORC script will consume is named per the [Point Naming Convention](#point-naming-convention) (`GCP1`, `GCP2`, ...; `XS1`, `XS2`, ...; `WL1`, `WL2`; `CAM`)
- [ ] Back up the GeoPackage as well (long-term archive — see [End of Day](#10-end-of-day))
- [ ] Open `VIDEO_CONFIG_SETUP.md` and start at Phase 4 with the GeoJSON in hand

Phases 5–7 of `VIDEO_CONFIG_SETUP.md` cover authoring the ORC-OS video configuration, activating the daemon, and validating. This survey document ends once the GeoJSON is ready for Phase 4.

---

# APPENDICES

## Appendix A: GNSS Master Setup

GNSS Master bridges the gap between your survey-grade rover receiver and consumer Android apps like SW Maps. Android devices expect GPS data in NMEA format through specific channels. The rover outputs UBX binary format through USB. GNSS Master translates between these systems and provides the mock location that overrides Android's internal GPS.

### Android Preparation

**1) Developer Options:**
   - Settings → About Phone → Tap Build Number 7x
   - Settings → Developer Options → Enable USB Debugging
   - Select Mock Location App → GNSS Master

**Why Developer Options:** Android hides advanced settings that most users shouldn't change. Enabling USB Debugging allows apps to communicate with external devices through USB. Mock Location permission lets an app replace the phone's GPS data — normally used for testing GPS apps, but essential for using external receivers.

**2) Permissions:**
   - Settings → Apps → GNSS Master → Permissions
   - Location: Allow all the time
   - Storage, Phone: Allow
   - Battery optimization: Don't optimize

**Location Permission:** GNSS Master needs continuous location access to function. The "Allow all the time" option prevents Android from suspending location services when the app is in the background. Without this, the mock location stops working when you switch to SW Maps.

**Battery Optimization:** Android aggressively limits background apps to save battery. If GNSS Master is optimized, Android will suspend it after a few minutes, killing the GPS feed. Disabling optimization keeps it running continuously throughout your survey session.

### GNSS Master Configuration

**1) Install:** Download from Google Play Store

**2) Connection:** Menu → Receiver → USB

**3) Mock Location:** Menu → Mock Location → Enable

**4) Test:** Verify position appears in Google Maps

**USB Connection:** This tells GNSS Master to expect the receiver on the USB port rather than Bluetooth or internal GPS. The app will look for a USB serial device when you connect the rover.

**Testing:** Open Google Maps and watch the position. If it shows your external receiver location and updates smoothly, the integration works. If it shows your phone's GPS position or doesn't update, the mock location isn't working — check permissions and app configuration.

### USB Connection Setup

1. Connect USB OTG cable to Android
2. Connect to rover F9P USB port
3. Power rover, wait 30 seconds
4. GNSS Master should auto-detect device
5. Verify satellite tracking and RTK status

**USB OTG:** On-The-Go cables let Android devices act as USB hosts rather than only peripherals. Your phone can connect to the rover the same way a computer would. Not all USB cables support OTG — verify you have an OTG cable.

**Auto-Detection:** GNSS Master scans for USB serial devices when you select USB connection mode. If it doesn't find the rover, check cable connections, verify the rover is powered, and confirm USB debugging is enabled on the Android device.

---

## Appendix B: SW Maps Configuration

SW Maps provides field data collection with quality control features, attribute forms, and GIS export capabilities. Proper configuration prevents data quality problems and simplifies post-processing.

### Project Creation

**1) New Project:** `Site_Name_YYYY_MM_DD`

**2) Coordinate System:**
   - Determine your UTM zone EPSG code (see Section 1 instructions)
   - Search for your EPSG code (example: 32748 for UTM 48S)
   - Select: WGS 84 / UTM zone XX[N/S]
   - VERIFY: Correct EPSG code, units = metre

**Project Naming:** Include the date and site name in the project name. When you create multiple projects for the same site, dates prevent confusion about which data is which. This is critical during post-processing when you're working with files copied to a computer weeks after field collection.

**Coordinate System Selection:** The EPSG code is unambiguous — it specifies WGS84 datum, UTM projection, zone number, and hemisphere. Searching by EPSG code prevents selecting wrong zones or similar-sounding systems. Verify the description matches your zone and units show "metre" not "degree". Degrees indicate geographic coordinates, not projected coordinates — a critical mistake.

**Example for Sukabumi, Indonesia:**
- Search: 32748
- Select: WGS 84 / UTM zone 48S
- Verify: EPSG:32748, units = metre

### GPS Settings

- GPS Source: Device internal GPS
- Averaging Method: By Time
- Default times: 60s standard, 120s canal
- Precision thresholds: H=2cm/V=3cm (std), H=4cm/V=6cm (canal)

**Device Internal GPS:** This seems counterintuitive when you're using an external receiver, but GNSS Master feeds the external receiver data through the Android internal GPS interface via mock location. SW Maps reads the "internal GPS" and receives the high-accuracy external data.

**Averaging Method:** Time-based averaging collects positions for a specified duration and averages them. This reduces noise and provides more stable coordinates than single-epoch measurements. Distance-based averaging (collect until the point doesn't move more than X centimeters) works poorly with RTK because the positions are already very stable and the app might never trigger the save.

**Precision Thresholds:** SW Maps can enforce quality gates by refusing to save points that exceed precision thresholds. Set these to match your quality requirements — 2cm horizontal, 3cm vertical for standard environments. This prevents accidentally saving poor-quality points when you're not paying attention to the status display.

### Survey Layers

Create these feature layers in your SW Maps project (all POINT geometry). The right column shows the name you give each point within that layer — this is what the post-processing script reads. See the full [Point Naming Convention](#point-naming-convention) in Section 1.

| Layer | Consumed by ORC script? | Point name |
|-------|-------------------------|------------|
| **Ground Control Points** | Yes | `GCP1`, `GCP2`, ... |
| **Discharge Cross Section** | Yes | `XS1`, `XS2`, ... (LB → RB) |
| **Water Level** | Yes | `WL1`, `WL2`, ... |
| **Camera Location** | Yes (one point only) | `CAM` |
| **Check Point Location** | No — survey QC only | `CP_START`, `CP_NOON`, `CP_END` |
| **Level Cross Section** | No — field records only | free-form (e.g. `LXS1`, `LXS2`, ...) |
| **Camera FOV** | No — field records only | free-form |

**Layer Organization:** Separate layers for different point types simplify processing and prevent mistakes. You can apply different symbology, filtering, and export rules to each layer. During post-processing, you load only the layers you need for each analysis step.

**Attribute Configuration:** Keep attributes minimal. The only attribute you set by hand is the point **name** (per the naming convention above), and optionally a free-form **notes** field. SW Maps records measurement time, PDOP, satellite count, horizontal/vertical precision, and fix status on every saved point automatically — you do not need to define those as layer attributes.

---

## Appendix C: Sample Video Collection

The sample video serves two purposes. First, it documents the flow conditions and visible features during your survey. Second, it provides the reference frame for identifying ground control points within the camera view.

### Connect to PtBox

 - Put the PtBox in Maintenance Mode using the FTP service
 - Wait for the PtBox to come online again, and log in
 - Select "Aim the camera in the field"
 - Take a 5 second video and note the video name and timestamp
 - Ensure that all control points are visible in the video. Adjust if needed and take a new video.
 - Also take a photo, and use the photo to number the control points so that you have a reference to use when entering the control points into the PtBox software later.
 - **NOTE:** Do not try to start the cameras in this view. This PtBox has a bad camera, and attempting to start the bad camera will cause the PtBox to lock up.

**Video Duration:** Five seconds provides enough frames to identify features clearly without consuming excessive storage. If flow conditions are highly variable (turbulent flow, changing light), consider 10-15 seconds to capture representative conditions.

**GCP Visibility:** Every ground control point you survey must be visible in the video. If a GCP is outside the camera field of view or occluded by vegetation or terrain, it cannot be used for photogrammetric processing. Check visibility before finalizing GCP locations.

**Photo for Numbering:** Take a still photo and annotate it with GCP numbers. This reference prevents mixing up control points during processing. Print the photo or keep it open on a screen while entering GCP coordinates in PtBox — visual confirmation prevents data entry errors.

---

## Appendix D: Troubleshooting

### NTRIP Connection Issues

- **Connection refused:** Verify port is 2001 (not 2101) and that you are using the IP `103.22.171.6` for the caster host — `nrtk.big.go.id` does not resolve for the NTRIP service
- **Authentication failed:** Log in at http://nrtk.big.go.id/sbc/ to verify account is active
- **No corrections received:** Ensure "Send NMEA GGA" is enabled (required for VRS mountpoint)
- **Intermittent connection:** Check cell signal strength, try moving to higher ground
- **VRS mountpoint unavailable:** Switch to "nearest" mountpoint as fallback
- **Correction age climbing:** NTRIP data stream is intermittent — check cell signal. If cell coverage is genuinely unavailable at your site, switch to the base station workflow (`SURVEY_PROCESS_v3_base.md`)

### No RTK FIX

- Check NTRIP connected and corrections flowing
- Verify correction stream: correction age should be <5 seconds
- Wait longer (up to 20 minutes for initial convergence)
- Move to better sky view

**NTRIP Correction Flow:** Verify the NTRIP client shows corrections being received. SW Maps or GNSS Master should display correction age that resets every 1-2 seconds. If correction age climbs steadily, the data stream has stopped — check cell connection.

**Initialization Time:** RTK solutions require resolving integer ambiguities in the carrier phase measurements. This process can take seconds in ideal conditions or minutes in challenging conditions. Be patient. If FIX doesn't occur within 20 minutes, something is wrong — poor satellite geometry, weak signal quality, or incorrect NTRIP configuration.

**Sky View:** Trees, buildings, and terrain block satellites and cause multipath. Move to a location with open sky down to 15° above all horizons. Even partial obstructions can prevent FIX solution.

### Poor Precision

- Check satellite count, PDOP
- Move away from reflective surfaces
- Use bipod for stability
- Extend averaging time

**Satellite Count:** Fewer than 8 satellites provides weak geometry. Enable all constellations (GPS + GLONASS + Galileo + BeiDou) to maximize satellite visibility. Check receiver configuration to confirm multi-constellation mode is active.

**Reflective Surfaces:** Water, metal roofs, vehicles, and smooth ground can reflect signals. The receiver sees both the direct signal and the delayed reflected signal, confusing the position calculation. Move 5-10 meters away from reflective surfaces.

**Pole Stability:** Hand-holding a 2m pole introduces centimeter-level position variations from hand shake and wind. A bipod or fixed mount eliminates these variations. If you must hand-hold, brace the pole against your body and take shallow breaths during measurement.

**Averaging Time:** Extended averaging (120s instead of 60s) helps in marginal conditions by averaging over more satellite geometry variations and atmospheric fluctuations. This can't fix systematic problems like multipath or poor PDOP, but it reduces random noise.

### USB Connection Issues

- Check USB OTG cable
- Power cycle rover and Android
- Verify USB debugging enabled
- Try different USB port

**Cable Quality:** USB cables have four wires — power, ground, and two data lines. Cheap cables sometimes omit the data lines (they only charge devices). Verify your cable supports data transfer by testing it with file transfer between devices.

**Power Cycling:** Connection issues often resolve with a complete power cycle. Turn off the rover, disconnect USB, close GNSS Master, wait 30 seconds, then reconnect and restart in sequence: rover power on, wait 30 seconds, connect USB, launch GNSS Master.

**USB Debugging:** Android blocks USB communication unless debugging is enabled. Check Settings → Developer Options → USB Debugging. If this keeps disabling itself, check for security software that restricts debugging.

**Port Selection:** Some Android devices have multiple USB modes (charging only, file transfer, MIDI, etc.). When you connect the rover, a notification appears asking which mode to use. Select "File transfer" or "USB tethering" mode to enable full communication.

---

## Appendix E: InaCORS Quick Reference Card

Print this card and keep it in your field notebook.

```
╔══════════════════════════════════════════════════════════╗
║              InaCORS NTRIP QUICK REFERENCE               ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  NTRIP Caster Host:  103.22.171.6  (IP only —            ║
║                      hostname does NOT resolve;          ║
║                      verify IP via InaCORS portal        ║
║                      before each field day)              ║
║  Port:               2001  (NOT 2101!)                   ║
║  Mountpoint:         VRS  (Java); nearest (fallback)     ║
║  NTRIP Version:      1.0                                 ║
║  Send NMEA GGA:      YES                                 ║
║                                                          ║
║  Registration:   http://nrtk.big.go.id/sbc/Account/      ║
║                  Register                                ║
║  Coverage check: https://srgi.big.go.id/page/            ║
║                  service-check                           ║
║                                                          ║
║  Coordinate system:  SRGI2013 (≈ WGS84 for practical    ║
║                      purposes)                           ║
║                                                          ║
║  Troubleshooting:                                        ║
║  1. Check port is 2001                                   ║
║  2. Check cell data connection                           ║
║  3. Verify Send GGA = YES                                ║
║  4. Confirm caster host is the IP (103.22.171.6)         ║
║  5. Try "nearest" if VRS unavailable                     ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
```

---

## Appendix F: Survey Equipment Rental in Jakarta

If you don't have your own RTK GNSS equipment, several companies in the Jakarta area rent survey-grade instruments. WhatsApp is the primary communication channel for most of these companies — initiate contact there rather than email.

### Jakarta-Based Companies

| Company | Phone / WhatsApp | Email | Location | Equipment |
|---------|-----------------|-------|----------|-----------|
| **Indosurta Group** | 021-5315-8019 / 0853-1204-2324 | info@indosurta.co.id | BSD City, Tangerang Selatan | GPS RTK, total station, **Leica Disto D510/X3/D2** |
| **Dinar Geoinstrument** | +62 878-7521-4418 / +62 822-2026-6662 | marketing@dinargeo.co.id | Pondok Kelapa, Jakarta Timur | GPS RTK, total station, theodolite |
| **CV. AMS** | 0812-8811-1186 (Susep) | admin@akurasimisisurvey.co.id | Jl. Salman 103, Kebon Jeruk, Jakarta Barat | GPS RTK, total station, theodolite |
| **Trans Survey** | 021-22544580 / 082119696710 | transsurvey1@gmail.com | Jl. Joglo Raya 27A, Jakarta Barat | GPS RTK, total station |
| **Sewatotalstation.com** | 0819-0861-1401 (Indra) / 0813-8585-7115 | indonesiasurvey@yahoo.com | Petukangan Utara, Jakarta Selatan | GPS RTK, total station (**Leica brand stocked**) |
| **PT Duta Basis Dataprima** | 021-22703696 | dutabasis@dutabasis.com | Jl. RC Veteran Raya 1, Bintaro, Jakarta Selatan | Leica 3D scanners, high-end survey equipment |
| **Duta Survey (Jakarta branch)** | 021-26964517 / 082299296105 | alatsurveytopcon@yahoo.com | Jl. Al-Fajri 14AH, Pasar Minggu, Jakarta Selatan | GPS RTK, total station |

### Companies Serving Jakarta from Nearby Cities

| Company | Phone / WhatsApp | Email | Base | Equipment |
|---------|-----------------|-------|------|-----------|
| **CV BNT** | 022-87521608 / 081222229059 | bnt.bdg@gmail.com | Bandung (ships to Jakarta) | GPS RTK, total station, drone |
| **CV ADHIJASA** | 081318699985 | Visit adhijasa.com | Bandung (delivers to Jakarta) | GPS RTK (Hi-Target, Trimble, Sokkia) |
| **DND Survey** | 022-5442-0354 / 082129900025 (Hana) | dndsurvey90@gmail.com | Bandung (delivers to Jakarta) | GPS RTK, total station |
| **MSDI** | Via msdi.co.id/contact-us | (website form) | Bali HQ (serves nationally) | Emlid RS2, Trimble R8S, drone LiDAR |

### Approximate Daily Rental Rates (2025-2026)

| Equipment | IDR/day | USD/day |
|-----------|---------|---------|
| GNSS RTK rover (entry-level) | 500,000 - 750,000 | $30 - 46 |
| GNSS RTK rover (mid-range, e.g. Emlid RS2) | 1,000,000 - 1,700,000 | $61 - 105 |
| GNSS RTK rover (high-end, e.g. Trimble/Leica) | 1,500,000 - 2,000,000+ | $92 - 125+ |
| Total station (reflectorless) | 600,000 - 1,200,000 | $37 - 74 |
| Leica Disto laser distance meter | Contact Indosurta or Sewatotalstation directly | — |

Weekly rates are typically 5-6x the daily rate. Most vendors require a 50% deposit.

### Notes

- **For Leica Disto rental specifically:** Indosurta Group is the best confirmed source (they list Disto D510, X3, D2 on their rental pages). Sewatotalstation.com and PT Duta Basis Dataprima are also worth contacting.
- **English-speaking service:** MSDI (msdi.co.id) and PT Duta Basis Dataprima (dutabasis.com) have the most professional English-language websites. Indosurta has partial English content.
- **Rental process:** Most transactions start via WhatsApp message. Expect to provide ID and a deposit. Larger companies (Indosurta, Duta Basis) provide formal rental agreements.
- **Delivery:** Many companies will deliver equipment to your project site within Jabodetabek (Jakarta, Bogor, Depok, Tangerang, Bekasi).

### Websites

- Indosurta rental page: https://indosurta.co.id/layanan/rental-sewa/
- CV BNT rental page: https://totalstation.co.id/product/rental-total-station-dan-gps-rtk-geodetik/
- MSDI rental page: https://www.msdi.co.id/services/rental-gnss-survey-instrument/
- DND Survey rental page: https://dndsurvey.id/rental-sewa-alatsurvey/
- Dinar Geoinstrument rental page: https://dinargeo.co.id/rental-sewa-alat-survey/
- CV AMS rental page: https://akurasimisisurvey.co.id/sewa-alat-survey/

---

**Document Version:** 2026-04-19
**Author:** Tom Jordan / OpenRiverCam Project
**Purpose:** Field procedure documentation — NTRIP workflow
**Companion document:** `SURVEY_PROCESS_v3_base.md` (local base station + PPP workflow, for sites without cell coverage)
**Supersedes:** `SURVEY_PROCESS_v3.md` (combined NTRIP + base station document)
