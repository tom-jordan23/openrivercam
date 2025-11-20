# 9.5 Survey Setup - Software

This section provides detailed software configuration procedures for all three software components used in RTK surveying: u-center (base station configuration), GNSS Master (Android positioning bridge), and SW Maps (survey data collection). These procedures connect directly to SURVEY_PROCESS.md Appendices A, B, and C.

Software configuration is as critical as hardware setup. Wrong coordinate system configuration means coordinates in the wrong location. Wrong base station mode means rover will not achieve fix. Wrong quality thresholds mean poor data gets saved. Following these procedures systematically ensures software supports accurate surveying.

By the end of this section, you will understand:
- u-center configuration for base station survey-in and RTCM broadcasting
- Base station RINEX logging setup for PPP post-processing
- GNSS Master configuration for rover position output
- SW Maps project setup with correct coordinate system
- Survey layer creation with appropriate attributes
- GPS integration testing and validation
- Quality threshold configuration matching SURVEY_PROCESS.md standards
- Troubleshooting common software issues

---

## Base Station Configuration with u-center

u-center is u-blox software for configuring GPS receivers. It controls base station operating mode, correction output, and data logging.

### Initial Connection and Configuration

**From SURVEY_PROCESS.md Appendix C:**

**Connection Setup:**
1. Launch u-center application on laptop
2. File → New (start clean configuration)
3. Connect base station to laptop via USB cable
4. Receiver → Connection → Select COM port (USB device should appear in list)
5. Set Baud rate: 38400 or 115200 (check your receiver specifications)
6. Click "Connect"

**Verification:**
- Satellite view should appear showing satellites (dots representing visible satellites)
- Data streaming in message view (UBX messages updating)
- Status bar showing position updates

**If connection fails:**
- Check USB cable connected firmly
- Check COM port correct (try different ports if multiple listed)
- Check baud rate matches receiver settings
- Power cycle receiver and retry
- Check USB drivers installed (u-blox receiver driver)

### Survey-In Configuration (TMODE3)

**From SURVEY_PROCESS.md Appendix C:**

TMODE3 is u-blox's survey-in mode. The receiver measures its position for a specified duration and accuracy target, then establishes that averaged position as its reference.

**Configuration procedure:**

1. **Open configuration view:**
   - View → Configuration View (opens UBX configuration interface)
   - Navigate to UBX → CFG → TMODE3

2. **Set survey-in parameters:**
   ```
   Mode: Survey-in
   Minimum time: 1800-3600 seconds (30-60 minutes)
   Required accuracy: 0.25 meters
   ```

3. **Send configuration:**
   - Click "Send" button (transfers settings to receiver)
   - Receiver begins survey-in immediately

**Why these parameters:**

**Minimum time: 30-60 minutes**
- Longer duration = better averaging = better reference position
- 30 minutes: adequate for local frame (achieves ~25 cm absolute accuracy)
- 60 minutes: better for precision work or challenging conditions
- From SURVEY_PROCESS.md: "30-60 minute survey-in for 0.25m accuracy"

**Required accuracy: 0.25 meters**
- Target accuracy for survey-in completion
- Receiver will continue survey-in until both time requirement AND accuracy requirement met
- 0.25m is appropriate for local reference frame

**Survey-in monitoring:**

**Open survey-in status view:**
- View → Messages View → UBX → NAV → SVIN (shows survey-in status)

**Monitor these values:**
- **Time elapsed:** How long survey-in has been running (target: 1800-3600 seconds)
- **Mean 3D accuracy:** Current position accuracy estimate (target: ≤0.25m)
- **Valid:** Survey-in complete (YES when both time and accuracy criteria met)
- **Observations:** Number of position measurements averaged (more = better)

**Quality indicators to watch during survey-in:**

From SURVEY_PROCESS.md:
```
Monitor: PDOP ≤1.5, Satellites ≥15
```

**How to view these in u-center:**
- View → Messages View → UBX → NAV → PVT (shows position, velocity, time)
- Look for:
  - **numSV:** Number of satellites (should show 15-20)
  - **pDOP:** Position dilution of precision (should show ≤1.5, lower better)

**Typical survey-in progress:**
```
0 min:  Time 0s,     Accuracy 5.2m,   PDOP 2.1, Sats 12  (just started)
10 min: Time 600s,   Accuracy 1.8m,   PDOP 1.6, Sats 15  (improving)
20 min: Time 1200s,  Accuracy 0.8m,   PDOP 1.4, Sats 17  (good progress)
30 min: Time 1800s,  Accuracy 0.24m,  PDOP 1.3, Sats 18  (near complete)
35 min: Time 2100s,  Accuracy 0.22m,  PDOP 1.3, Sats 18  (Valid = YES!)
```

**When survey-in completes:**
- SVIN message shows "Valid: YES"
- Base station now has established reference position
- Base station begins broadcasting corrections
- Rover can now achieve RTK FIX

**Record final coordinates:**

From SURVEY_PROCESS.md:
```
Record final coordinates in UTM 48S
```

**How to view and record coordinates:**
1. View → Messages View → UBX → NAV → PVT
2. Look for "lat" (latitude) and "lon" (longitude) in decimal degrees
3. Look for "hMSL" (height above mean sea level) in millimeters

**Convert to UTM if needed:**
- u-center displays geographic coordinates (lat/lon)
- Use coordinate conversion tool to convert to UTM (e.g., PROJ, online converters)
- Or record lat/lon and convert later in office

**Record in field notebook:**
```
Base Station Position (Survey-In Complete):
Date/Time: 2024-11-15 09:15
Latitude: -5.234567°
Longitude: 104.345678°
Elevation MSL: 142.34 m
UTM 48S: E=685432.15, N=9456782.33, Z=142.34
Antenna height: 1.523 m
Survey-in duration: 35 minutes
Mean accuracy: 0.22 m
PDOP: 1.3, Satellites: 18
```

This information is needed for:
- Documentation (permanent record of base station position)
- PPP processing (initial position estimate)
- Verification (check coordinates look reasonable for site location)

### RTCM3 Output Configuration

**RTCM3 is the standard correction message format.** Base station broadcasts RTCM3 messages containing correction data. Rover receives these messages to achieve RTK FIX.

**From SURVEY_PROCESS.md Appendix C:**

```
RTCM3 Output (if not using pre-configured base and rover)
```

**Note:** Many RTK systems come pre-configured with RTCM3 output enabled. Check your system documentation. If already configured, skip this section. If not configured, follow these steps.

**Configuration procedure:**

1. **Set output protocol:**
   - UBX → CFG → PRT → UART2 (or UART1, depending on output port)
   - Protocol out: Select "RTCM3"
   - Baud rate: 38400 or 57600 (match radio requirements)
   - Click "Send"

2. **Enable RTCM message types:**
   - UBX → CFG → MSG → Select RTCM3 message category

**Enable these RTCM3 messages:**
```
1005 (Station ARP - Antenna Reference Point): Rate 10
1077 (GPS MSM7 - Multi-Signal Message): Rate 1
1087 (GLONASS MSM7): Rate 1
1097 (Galileo MSM7): Rate 1
```

**What these messages do:**
- **1005:** Broadcasts base station position (rover uses to calculate baseline)
- **1077:** GPS satellite corrections (code and phase measurements)
- **1087:** GLONASS corrections (additional satellites)
- **1097:** Galileo corrections (additional satellites)

**Rate values:**
- Rate 1: Send every epoch (every measurement, typically 1 Hz = once per second)
- Rate 10: Send every 10 epochs (every 10 seconds)

**Why these rates:**
- Satellite corrections (1077, 1087, 1097): Need frequent updates (Rate 1 = every second)
- Station position (1005): Static, infrequent updates sufficient (Rate 10 = every 10 seconds)

3. **Verify RTCM output:**
   - View → Messages View → RTCM3 → Should see messages appearing
   - 1077, 1087, 1097 updating every second
   - 1005 updating every 10 seconds

**If no RTCM messages appear:**
- Check output port configuration (UART2 protocol set to RTCM3)
- Check messages enabled with correct rates
- Check receiver in correct mode (TMODE3 survey-in complete, now broadcasting)

**Radio connection:**
- Connect base station's UART output to radio input
- Radio transmits RTCM data to rover
- Rover receives and processes corrections

### Raw Data Logging for PPP

**From SURVEY_PROCESS.md Appendix C and Section 3:**

```
Start RINEX logging (6-12 hours)
```

**Why log raw data:**
PPP post-processing requires observation data from base station. RINEX is the standard format for post-processing.

**RINEX logging setup in u-center:**

1. **Enable raw data messages:**
   - UBX → CFG → MSG → UBX-RXM-RAWX: Rate 1 (raw measurement data)
   - UBX → CFG → MSG → UBX-RXM-SFRBX: Rate 1 (satellite broadcast ephemeris)
   - UBX → CFG → MSG → UBX-NAV-PVT: Rate 1 (position, velocity, time)
   - Send configuration for each message

2. **Start database logging:**
   - File → Database Logging → Start
   - File type: UBX (native u-blox format)
   - File name: `Base_YYYYMMDD_SiteName.ubx` (e.g., `Base_20241115_Ciliwung.ubx`)
   - Location: Save to laptop or external drive (ensure sufficient space: ~10-50 MB per hour)

3. **Verify logging active:**
   - Status bar shows "Logging" indicator
   - File size should increase (refresh file browser to verify)
   - Let logging run for 6-12 hours (entire survey session)

**Logging duration from SURVEY_PROCESS.md:**
- Minimum: 6 hours (provides 3-5 cm PPP accuracy)
- Recommended: 12 hours (provides 2-3 cm PPP accuracy)
- Longer is better, but diminishing returns beyond 24 hours

**Practical logging workflow:**
- Start logging when survey-in completes
- Leave base station running and logging while you survey with rover (3-5 hours active survey)
- Leave base station logging after finishing rover survey (return later or next day to stop and collect data)
- If site security allows overnight operation: leave logging overnight (12-24 hours total)

**Stop logging:**
- Return to base station after desired duration
- File → Database Logging → Stop
- Safely disconnect laptop
- Copy .ubx file to backup location (USB drive, cloud storage)

**Converting UBX to RINEX:**

This is done in office after field work. From SURVEY_PROCESS.md Section 10:

```bash
convbin -od -os -oi -ot -f 1 your_file.ubx
```

This creates .obs and .nav files in RINEX format for PPP submission.

**Detailed conversion procedure covered in Section 10 (Post-Processing).** For field work, just ensure UBX logging runs successfully.

---

## GNSS Master Configuration

GNSS Master bridges RTK rover position to SW Maps through Android's mock location feature.

### From SURVEY_PROCESS.md Appendix A

Most configuration was completed during day-before setup (Section 9.2). Here we verify configuration and start operation.

### Android Developer Settings Verification

**Before starting GNSS Master, verify:**

1. **Developer Options enabled:**
   - Settings → About Phone → Tap "Build Number" 7x (should see "You are now a developer")
   - Settings → Developer Options (should be visible)

2. **USB Debugging enabled:**
   - Settings → Developer Options → USB Debugging (toggle ON)

3. **Mock Location App selected:**
   - Settings → Developer Options → Select Mock Location App → GNSS Master

**Why this matters:**
Mock location allows GNSS Master to provide RTK position to SW Maps as if it were the device's internal GPS. Without this setting, SW Maps would use Android's internal GPS (3-10 meter accuracy) instead of RTK position (1-3 cm accuracy).

### GNSS Master Operation

**Start GNSS Master:**

1. **Launch app** (GNSS Master icon)

2. **Verify connection settings:**
   - Menu → Receiver → USB (should already be selected from day-before setup)

3. **Connect rover:**
   - Plug USB OTG cable from rover to Android
   - GNSS Master should auto-detect within 10-30 seconds
   - Screen should show "Connected" or similar status

4. **Verify satellite tracking:**
   - Main screen should show satellite list (GPS, GLONASS, Galileo satellites)
   - Satellite count should increase (10-20 satellites typical)
   - Signal strength bars should show (colored bars indicating signal quality)

5. **Enable mock location:**
   - Menu → Mock Location → Enable (toggle ON)
   - Status should show "Mock location active"

6. **Verify position output:**
   - Main screen should show coordinates (latitude, longitude)
   - Position should update every second
   - Solution type should display (Single → Float → Fix as corrections received)

**GNSS Master display should show:**
```
Status: Connected
Satellites: 16 GPS, 8 GLONASS, 6 Galileo (30 total)
Solution: RTK FIX (or FLOAT during initialization)
Latitude: -5.234567°
Longitude: 104.345678°
Altitude: 142.34 m
Precision: H=0.014m V=0.021m
Age of corrections: 0.8s
Mock location: Active
```

**If rover not detected:**
- Check USB cable connected firmly
- Check USB debugging enabled
- Try power cycle rover and restart GNSS Master
- Try different USB cable (must support data)
- Check rover output mode (should be NMEA on USB port)

**If satellites not appearing:**
- Check rover antenna connected
- Check rover has sky view (not indoors or under metal roof)
- Wait 1-2 minutes for satellite acquisition

**If solution stuck on Single (not progressing to Float):**
- Check base station operating and broadcasting corrections
- Check radio link (rover should receive corrections)
- Verify rover and base on same communication channel

**If solution stuck on Float (not achieving Fix):**
- Check satellite count (need ≥10)
- Check PDOP if displayed (need ≤3.0)
- Move to better sky view location
- Move away from reflective surfaces (metal, water edge)
- Wait longer (fix can take 10-20 minutes)

### Mock Location Testing

**Verify mock location is working:**

1. **Open Google Maps** (while GNSS Master running with mock location enabled)
2. **Blue dot should appear** showing current position
3. **Walk with rover** (blue dot should follow smoothly)
4. **Position should be precise** (not jumping around like normal GPS)

**If mock location not working:**
- Check Developer Options → Mock Location App set to GNSS Master
- Check GNSS Master → Mock Location enabled
- Restart GNSS Master
- Restart Android device if needed

**Once mock location verified working, open SW Maps.**

---

## SW Maps Project Configuration

SW Maps is the survey data collection app. It receives position from GNSS Master (mock location) and records surveyed points with attributes.

### From SURVEY_PROCESS.md Appendix B

Project creation and layer setup should have been completed during day-before preparation (Section 9.2). Here we verify configuration and test GPS integration.

### Project and Coordinate System Verification

**Open SW Maps:**

1. **Launch SW Maps app**

2. **Open project:**
   - Projects → Select your project (e.g., "Ciliwung_River_2024_11_15")

3. **Verify coordinate system:**
   - Project → Properties → Coordinate System
   - Should show: EPSG:32748 (or your site's correct UTM zone)
   - Units: metre (meters)

**Critical: Wrong coordinate system means coordinates in wrong location.**

If coordinate system incorrect:
- Close all layers
- Project → Properties → Change coordinate system
- Search for correct EPSG code
- Save and reopen project

### GPS Settings Configuration

**Configure GPS integration:**

1. **Open GPS settings:**
   - Menu → GPS → GPS Settings

2. **Verify settings match SURVEY_PROCESS.md standards:**

```
GPS Source: Device internal GPS (receives from GNSS Master mock location)
Averaging Method: By Time
Default averaging time: 60 seconds (standard)
                       120 seconds (canal/challenging conditions)
Horizontal precision threshold: 0.02 m (2 cm) for standard
                                0.04 m (4 cm) for canal
Vertical precision threshold: 0.03 m (3 cm) for standard
                              0.06 m (6 cm) for canal
```

**Why these settings:**

**Averaging Method: By Time**
- Averages position measurements for specified duration
- Reduces random noise
- More stable position estimate
- Alternative "By Distance" not suitable for stationary GCP surveying

**Averaging time: 60-120 seconds**
- From SURVEY_PROCESS.md quality gates
- 60s: standard conditions (good sky view, good satellite geometry)
- 120s: challenging conditions (partial obstructions, marginal satellite count)

**Precision thresholds:**
- From SURVEY_PROCESS.md quality gates
- SW Maps will warn if precision exceeds thresholds
- Prevents saving poor-quality data
- Standard: 2cm H / 3cm V (typical RTK accuracy)
- Canal: 4cm H / 6cm V (relaxed for challenging environments)

3. **Enable quality warnings:**
   - Settings should have option "Warn when precision exceeds threshold" (enable this)
   - SW Maps will display warning if trying to save point with precision worse than threshold

4. **Set measurement display:**
   - Display fix quality (shows RTK FIX, FLOAT, SINGLE status)
   - Display satellite count
   - Display precision estimates
   - Display coordinates (current position)

**Configured display helps operator make informed decisions** about when quality is adequate to save points.

### GPS Integration Testing

**With GNSS Master running and mock location active, rover with RTK FIX:**

1. **Check GPS indicator in SW Maps:**
   - Should show GPS icon (typically in status bar or toolbar)
   - Should show "connected" or "active" status
   - Should display current coordinates

2. **Verify position updates:**
   - Watch coordinate display (should update every 1-2 seconds)
   - Walk with rover (coordinates should change smoothly)
   - Position should not jump erratically (indicates mock location working correctly)

3. **Verify fix status displayed:**
   - SW Maps should show solution type (depends on how GNSS Master passes status)
   - Some GNSS Master / SW Maps combinations show "RTK FIX" text
   - Some show only precision estimates (if H ≤2cm and V ≤3cm, indicates fix)
   - Verify you can distinguish FIX from FLOAT (critical for survey decisions)

**If GPS not working in SW Maps:**
- Check GNSS Master mock location active
- Check SW Maps GPS settings (GPS Source = Device internal GPS)
- Try toggle SW Maps GPS off/on (Menu → GPS → Toggle)
- Restart SW Maps
- Restart Android device if needed

### Survey Layers Review

**From SURVEY_PROCESS.md Appendix B, verify these layers exist:**

1. **Camera FOV** (polygon or line layer for field of view documentation)
2. **Camera Location** (point layer for camera position)
3. **Check Point Location** (point layer for quality control check points)
4. **Ground Control Points** (point layer for GCPs - most important)
5. **Discharge Cross Section** (point layer for cross-section bathymetry)
6. **Level Cross Section** (point layer for additional cross-sections)
7. **Water Level** (point layer for water surface elevation)

**For each layer, verify attributes configured:**

**Example: Ground Control Points layer attributes:**
- **point_id** (text): GCP1, GCP2, etc.
- **description** (text): Location description
- **marker_type** (text): Painted rock, survey stake, etc.
- **visibility** (text): Clear, partial, obscured
- **surveyed_by** (text): Operator name
- **survey_time** (datetime): Timestamp
- **satellites** (integer): Satellite count at time of survey
- **pdop** (decimal): PDOP value
- **h_precision** (decimal): Horizontal precision estimate
- **v_precision** (decimal): Vertical precision estimate
- **notes** (text): Additional observations

**Attributes support quality control and documentation.** Record conditions at time of survey for later analysis.

**If layers or attributes missing:**
- Add layers (Layer → Add Layer → New Vector Layer)
- Add attributes (Layer → Properties → Fields → Add Field)
- Configure attribute types and constraints

**Should have been done during day-before setup.** If not, do now before beginning survey (better to spend 15 minutes configuring than collect incomplete data).

### Test Point Collection

**Before starting actual survey, test complete workflow:**

1. **Open Ground Control Points layer** (make layer active)

2. **Tap "Add Point" or "Collect Point"** (interface varies by SW Maps version)

3. **GPS positioning should activate:**
   - Shows current position
   - Shows quality indicators (satellites, precision, fix status)
   - Begins averaging (countdown timer typically displays)

4. **Wait for averaging to complete** (60 seconds standard setting)

5. **Verify quality gates met:**
   - RTK FIX status (not Float or Single)
   - Satellites ≥ 12
   - Horizontal precision ≤ 2cm
   - Vertical precision ≤ 3cm
   - Age of corrections < 3s (if displayed)

6. **Fill in attributes:**
   - point_id: TEST1
   - description: Integration test point
   - marker_type: Test (not actual GCP)
   - Fill other attributes as appropriate

7. **Save point**

8. **Verify point appears on map:**
   - Point should display at surveyed location
   - Tap point to view attributes (verify recorded correctly)
   - Check coordinate values (should be in UTM, values reasonable for site)

**If test point collection succeeds:**
System is ready for actual survey. Delete test point if not needed.

**If test point collection fails:**
Troubleshoot before starting survey:
- GPS not active: Check GNSS Master mock location, check SW Maps GPS settings
- Quality gates not met: Check rover RTK fix, check quality indicators
- Point not appearing: Check layer active, check map extent
- Coordinates wrong: Check project coordinate system (EPSG code)
- Attributes not saving: Check attribute field configuration

---

## Quality Threshold Configuration

**From SURVEY_PROCESS.md, two quality standard sets:**

### Standard Conditions

**Use for:**
- Open river sites with good sky view
- Stable ground conditions
- Good satellite coverage (typical)

**Thresholds:**
```
RTK FIX: Required (not Float or Single)
Fix duration: ≥10 seconds
PDOP: ≤2.5
Satellites: ≥12
Horizontal precision: ≤2 cm (0.02 m)
Vertical precision: ≤3 cm (0.03 m)
Averaging time: 60 seconds
Age of corrections: <3 seconds
```

**Configure in SW Maps:**
- GPS Settings → Precision thresholds → H: 0.02 m, V: 0.03 m
- GPS Settings → Averaging time → 60 seconds
- Enable precision warnings

**Operator verification (not automatically checked by SW Maps):**
- RTK FIX status (verify before starting averaging)
- Fix duration ≥10s (wait after fix achieved before collecting)
- PDOP ≤2.5 (check in GNSS Master or SW Maps if displayed)
- Satellites ≥12 (check in GNSS Master or SW Maps if displayed)
- Age of corrections <3s (check in GNSS Master if displayed)

### Canal / Challenging Conditions (Relaxed Standards)

**Use for:**
- Narrow canals with metal infrastructure
- Sites with partial sky obstructions
- Urban environments with buildings
- Areas with unavoidable multipath

**Thresholds:**
```
RTK FIX: Required (not Float or Single)
Fix duration: ≥10 seconds
PDOP: ≤3.0 (relaxed from 2.5)
Satellites: ≥10 (relaxed from 12)
Horizontal precision: ≤4 cm (0.04 m, relaxed from 2 cm)
Vertical precision: ≤6 cm (0.06 m, relaxed from 3 cm)
Averaging time: 120 seconds (extended from 60s)
Age of corrections: <3 seconds
```

**Configure in SW Maps for canal mode:**
- GPS Settings → Precision thresholds → H: 0.04 m, V: 0.06 m
- GPS Settings → Averaging time → 120 seconds

**Longer averaging time compensates for challenging conditions** - more measurements averaged = better noise reduction.

**Relaxed precision thresholds acknowledge reality** that some environments make 2cm accuracy difficult. 4cm is still adequate for transformation (Section 4.3 showed GCP accuracy of 5-10cm acceptable, though 2-3cm preferred).

**When to use relaxed standards:**
Only when standard conditions unachievable. Prefer standard thresholds when possible.

### Real-Time Quality Assessment

**During each point collection, operator should verify quality gates before saving:**

**Pre-averaging checks (before starting measurement):**
1. Is solution type FIX? (if Float, wait; if Single, troubleshoot base connection)
2. Has FIX been maintained ≥10 seconds? (if just achieved, wait)
3. Satellite count adequate (≥12 standard, ≥10 canal)?
4. PDOP acceptable (≤2.5 standard, ≤3.0 canal)?
5. Age of corrections <3s? (if >3s, check base station and radio link)

**During averaging (60-120 seconds):**
1. Keep pole vertical (monitor bubble level)
2. Keep pole stable (use bipod if available, minimize movement)
3. Monitor quality indicators (if deteriorate, extend averaging or retry)

**Post-averaging checks (before saving):**
1. Precision estimates within thresholds (H ≤2cm/4cm, V ≤3cm/6cm)?
2. FIX maintained throughout averaging? (if lost, discard measurement and retry)
3. Position stable? (coordinate display not jumping around)

**Only save point if all checks pass.**

**If checks fail:**
- Wait 2 minutes for conditions to improve (satellite geometry changes, fix stabilizes)
- If still failing, move 2-3 meters to different location (avoid local multipath)
- If persistently failing, extend averaging time (120s → 180s if needed)
- If cannot achieve quality gates, note in field notebook and skip point or accept relaxed standards

---

## Troubleshooting Common Software Issues

### Problem: u-center cannot connect to base station

**Diagnosis:** COM port or baud rate issue

**Solutions:**
- Verify USB cable connected
- Try different COM ports in connection menu
- Try different baud rates (38400, 57600, 115200)
- Check USB drivers installed (u-blox Windows driver)
- Power cycle base station
- Try different USB port on laptop

### Problem: Survey-in not completing (stuck at high accuracy value)

**Diagnosis:** Poor satellite conditions or multipath

**Solutions:**
- Check PDOP (if >2.0, poor satellite geometry)
- Check satellite count (if <12, insufficient satellites)
- Wait longer (satellite geometry improves over time)
- Relocate base station to better sky view
- Move away from metal structures or trees
- Accept longer survey-in duration (60-90 minutes)

### Problem: No RTCM messages appearing in u-center

**Diagnosis:** Output not configured or wrong port

**Solutions:**
- Verify RTCM messages enabled (CFG → MSG)
- Verify output port set to RTCM3 (CFG → PRT → Protocol out)
- Check survey-in completed (RTCM not broadcast during survey-in)
- Restart receiver after configuration changes
- Check correct message view open (View → Messages View → RTCM3)

### Problem: GNSS Master not detecting rover

**Diagnosis:** USB connection or Android settings issue

**Solutions:**
- Check USB cable connected firmly
- Check USB debugging enabled (Developer Options)
- Power cycle rover
- Restart GNSS Master
- Try different USB cable (must support data transfer)
- Check rover output mode (should be NMEA on USB)

### Problem: Mock location not working (SW Maps uses internal GPS)

**Diagnosis:** Developer settings or GNSS Master configuration

**Solutions:**
- Check Developer Options → Mock Location App set to GNSS Master
- Check GNSS Master → Menu → Mock Location enabled
- Restart GNSS Master with mock location enabled BEFORE starting SW Maps
- Restart Android device
- Test with Google Maps (blue dot should follow rover precisely)

### Problem: SW Maps not showing GPS position

**Diagnosis:** GPS integration or settings issue

**Solutions:**
- Check GNSS Master mock location active
- Check SW Maps → GPS Settings → GPS Source = Device internal GPS
- Toggle SW Maps GPS off and on (Menu → GPS)
- Check Android location services enabled (Settings → Location)
- Restart SW Maps
- Restart Android device

### Problem: Coordinates in SW Maps are wrong (not at survey site)

**Diagnosis:** Wrong coordinate system configured

**Solutions:**
- Check Project → Properties → Coordinate System (should show correct EPSG code)
- Check Units = metre (meters)
- Verify EPSG code matches site's UTM zone
- Change coordinate system if wrong (close layers first, then change, then reopen)
- Verify base map or satellite imagery aligned (coordinates should place you near visible site features)

### Problem: Quality indicators not meeting thresholds consistently

**Diagnosis:** Environmental conditions or equipment issues

**Solutions:**
- Check sky view at measurement location (move to more open area)
- Check for nearby reflective surfaces (move away from metal, water edge)
- Extend averaging time (60s → 120s → 180s)
- Check base station still operating correctly (verify corrections being received)
- Check rover antenna connection and position (keep level and unobstructed)
- Consider relaxed standards if site conditions make standard thresholds unachievable

---

## Pre-Survey Software Verification Checklist

**Before beginning actual survey, verify all software configured and operational:**

**Base station (u-center):**
- [ ] u-center connected to base station
- [ ] Survey-in completed successfully (SVIN Valid: YES)
- [ ] Final coordinates recorded (lat/lon or UTM)
- [ ] RTCM messages broadcasting (visible in message view)
- [ ] RINEX logging started (UBX file being written)
- [ ] Logging file path confirmed (saved to laptop or external drive)
- [ ] Base station will continue logging for 6-12 hours

**Rover (GNSS Master):**
- [ ] GNSS Master connected to rover via USB
- [ ] Satellite tracking active (15-20 satellites typical)
- [ ] Solution type showing (Single → Float → Fix progression)
- [ ] RTK FIX achieved (ambiguities resolved, 1-3cm accuracy)
- [ ] Mock location enabled and active
- [ ] Position updating smoothly (every 1-2 seconds)
- [ ] Quality indicators displayed (satellites, precision, age of corrections)

**Survey app (SW Maps):**
- [ ] SW Maps project opened (correct project for this survey)
- [ ] Coordinate system verified (correct EPSG code, units = metre)
- [ ] GPS integration working (position from GNSS Master mock location)
- [ ] GPS settings configured (averaging time, precision thresholds)
- [ ] Survey layers created (GCPs, Check Points, Cross Sections, Water Level)
- [ ] Layer attributes configured (point_id, description, quality fields)
- [ ] Test point collection successful (point saved with attributes)
- [ ] Test point coordinates reasonable (near survey site location)

**Quality gates configuration:**
- [ ] Standard or canal/relaxed standards selected (based on site conditions)
- [ ] Precision thresholds set (0.02/0.03m standard, 0.04/0.06m canal)
- [ ] Averaging time set (60s standard, 120s canal)
- [ ] Quality warning enabled (SW Maps will warn if thresholds exceeded)
- [ ] Operator knows how to check additional gates (FIX status, satellites, PDOP, age of corrections)

**Communication and documentation:**
- [ ] Team roles confirmed (who operates rover, who monitors base)
- [ ] Field notebook ready (record measurements, conditions, issues)
- [ ] Camera ready (document GCP locations and site conditions)
- [ ] Communication method established (phones, radios, check-in schedule)

**If all verifications pass:**
Software systems ready. Proceed with survey execution (Section 9.6).

**If any verifications fail:**
Troubleshoot and resolve before starting survey. Poor software configuration leads to poor data or failed survey.

---

## Summary: Software Configuration for Survey

**Base station (u-center):**
- Configure TMODE3 survey-in (30-60 min, 0.25m accuracy target)
- Monitor quality (PDOP ≤1.5, Satellites ≥15)
- Record final coordinates when survey-in completes
- Enable RTCM3 output (messages 1005, 1077, 1087, 1097)
- Start RINEX logging (6-12 hours for PPP post-processing)

**Rover (GNSS Master):**
- Connect via USB with mock location enabled
- Verify satellite tracking and RTK FIX achieved
- Monitor quality indicators (satellites, precision, age of corrections)
- Provides position to SW Maps via Android mock location

**Survey app (SW Maps):**
- Configure correct coordinate system (EPSG code for site's UTM zone)
- Set GPS integration (Device internal GPS receives mock location)
- Configure averaging time (60s standard, 120s canal)
- Set precision thresholds (2/3cm standard, 4/6cm canal)
- Create survey layers with attributes for documentation
- Test complete workflow before starting survey

**Quality standards:**
- Standard: FIX, 10s duration, ≥12 sats, ≤2.5 PDOP, ≤2cm H / ≤3cm V, 60s averaging
- Canal: FIX, 10s duration, ≥10 sats, ≤3.0 PDOP, ≤4cm H / ≤6cm V, 120s averaging
- Operator verifies all gates before saving each point

**Software setup time:**
- Base station configuration: 5-10 minutes
- Survey-in: 30-60 minutes (waiting, monitoring)
- Rover/GNSS Master verification: 5-10 minutes
- SW Maps configuration verification: 5-10 minutes
- Integration testing: 10-15 minutes
- Total: 55-105 minutes (most time is survey-in waiting)

**With software configured and verified, hardware setup complete (Section 9.4), and quality standards established, you are ready to begin survey execution (Section 9.6).**

---

**Next Section:** [9.6 Survey Execution - Process Overview](06-survey-execution-overview.md)
