# 9.6 Survey Execution - Process Overview

This section provides the systematic workflow for executing the complete survey. Sections 9.1-9.5 prepared you with concepts, equipment, and configuration. Now we integrate everything into a coordinated field procedure that produces accurate, complete survey data for OpenRiverCam deployment.

This overview connects directly to SURVEY_PROCESS.md Sections 4-9, providing the "why" and context for each procedural step.

By the end of this section, you will understand:
- The complete survey workflow sequence
- How different measurement types connect
- Team coordination during survey execution
- Quality control throughout the process
- Data backup and verification procedures
- End-of-day closure and validation
- How survey data flows into PtBox configuration

---

## Survey Workflow Overview

The complete survey follows this sequence:

**Setup phase (60-120 minutes):**
1. Arrive at site, establish base station
2. Start base station survey-in (30-60 min)
3. While base surveys, assemble rover and mark GCP locations
4. Base survey-in completes, rover achieves RTK FIX
5. Verify all quality gates met

**Measurement phase (3-5 hours):**
6. Establish check points (CP_START)
7. Survey camera position
8. Collect sample video showing all GCPs
9. Survey each GCP after video confirms visibility
10. Survey water level
11. Survey river cross-section
12. Re-measure check point (CP_NOON) after 4-6 hours
13. Additional measurements as needed (second cross-section, camera FOV documentation)

**Closure phase (30-60 minutes):**
14. Re-measure final check point (CP_END)
15. Verify check point drift ≤3cm H / ≤4cm V
16. Stop RINEX logging on base station
17. Export survey data from SW Maps
18. Multiple data backups
19. Pack equipment
20. Document deviations or issues

**This section explains the measurement phase workflow and quality control.**

---

## Sequencing: Why Order Matters

**From SURVEY_PROCESS.md, specific sequence:**
1. Check points first (establish quality control reference)
2. Camera position (documents monitoring setup)
3. Sample video (confirms GCP visibility)
4. GCPs (core transformation data)
5. Water level (documents hydraulic conditions)
6. Cross-sections (bathymetry for discharge calculations)

### Why Check Points First

**From SURVEY_PROCESS.md Section 4:**

```
Establish CP_START:
- 20-50m from base, stable high ground
- RTK FIX for 30 seconds
- 3 independent 60s measurements
- Agreement within 1cm H, 2cm V
- Mark permanently, photograph
```

**Purpose:**
Check points verify RTK system is working correctly and maintaining accuracy over time. Establishing CP_START at the beginning provides reference for end-of-day validation.

**Procedure:**

1. **Select check point location:**
   - Stable ground (will not move)
   - High ground (above flood level)
   - 20-50m from base station (representative distance)
   - Open sky view (good GPS conditions)
   - Accessible (easy to return for re-measurement)

2. **Mark location permanently:**
   - Painted mark on rock (ideal)
   - Survey stake driven firmly (acceptable)
   - Photograph with surroundings (aids relocation)

3. **Take 3 independent measurements:**
   - Measurement 1: Position rover, achieve FIX for 30s, average 60s, save as CP_START_1
   - Lift rover, walk around briefly (breaks any position "lock")
   - Measurement 2: Re-position rover at mark, FIX 30s, average 60s, save as CP_START_2
   - Repeat for Measurement 3
   - Record all three positions in field notebook

4. **Verify repeatability:**
   - Compare three measurements
   - Horizontal difference ≤1cm (excellent repeatability)
   - Vertical difference ≤2cm (acceptable)
   - If differences >2cm, investigate (poor pole positioning, multipath, inadequate averaging)

**Example check point measurements:**
```
CP_START (2024-11-15 09:45):
Measurement 1: E=685432.234, N=9456782.178, Z=142.456
Measurement 2: E=685432.228, N=9456782.182, Z=142.461
Measurement 3: E=685432.231, N=9456782.175, Z=142.458

Differences:
H: 0.7 cm (excellent)
V: 0.5 cm (excellent)

Average: E=685432.231, N=9456782.178, Z=142.458
```

**Why 3 measurements:**
Proves RTK system is delivering consistent, repeatable positions. Single measurement could be lucky. Three measurements averaging to within 1-2cm demonstrate system reliability.

**Check point as quality control:**
- If CP_NOON and CP_END measurements drift >3-4cm from CP_START, something went wrong
- Possible causes: base station moved, equipment malfunction, atmospheric anomaly
- Large drift = do not trust survey data from that session

### Why Camera Position Before GCPs

**From SURVEY_PROCESS.md Section 5:**

```
Camera Position:
- 5-10m height, 15-45° viewing angle
- Survey camera position with rover
- Record height, direction, tilt angle
```

**Purpose:**
Documents the monitoring perspective. Camera position is less accuracy-critical than GCPs (10-20cm accuracy acceptable vs. 2-3cm for GCPs), so can be measured quickly with standard 60s averaging.

**Procedure:**

1. **Position rover at camera mounting point** (or planned camera location)
2. **Achieve RTK FIX, verify quality gates**
3. **Average 60 seconds** (standard averaging sufficient)
4. **Record attributes:**
   - point_id: CAM1 or CAMERA_LOCATION
   - description: Camera mounting point on left bank
   - height_above_water: Measure with tape (e.g., 8.2m)
   - direction: Compass bearing camera looks (e.g., 045° = northeast)
   - tilt_angle: Angle below horizontal (e.g., -35°)
5. **Photograph mounting location** (documents installation context)

**Why measure height and angles:**
- Aids future camera adjustments or replacement
- Helps interpret field of view and GCP distribution
- Documents for site planning and engineering

**Camera position measurement is informational**, not critical for transformation (transformation uses GCP positions, not camera position). But worth recording while rover is active.

### Why Sample Video Before Surveying GCPs

**From SURVEY_PROCESS.MD Section 5 and Appendix D:**

```
Control Points:
- Place 6+ visible targets in camera FOV
- Take sample video
- Survey each control point after video
```

**Purpose:**
Confirms all planned GCPs are actually visible in the camera image before investing time surveying them. No point surveying GCPs to 2cm accuracy if they are not visible in the image.

**Procedure:**

1. **Connect to PtBox or camera** (if camera already mounted, or use handheld camera at mounting position)
2. **Frame field of view** showing planned GCP locations
3. **Record 5-30 second video** showing:
   - All GCP markers clearly visible
   - Water surface and river extent
   - Banks and surroundings
4. **Review video immediately:**
   - Can you identify each GCP marker?
   - Are GCPs distributed well (near/far, left/right)?
   - Is anything obscuring GCPs (vegetation, glare, shadows)?
5. **Adjust GCP locations if needed:**
   - Move GCPs that are obscured or barely visible
   - Add GCPs if coverage appears inadequate
   - Repaint markers if contrast poor
6. **Take photo and number GCPs in photo:**
   - Use photo as reference when entering GCPs into PtBox later
   - Clear identification: "GCP1 = left bank near rock", etc.

**From SURVEY_PROCESS.md Appendix D:**
> Also take a photo, and use the photo to number the control points so that you have a reference to use when entering the control points into the PtBox software later.

**Why this sequence matters:**
- Sample video first = discover visibility problems early
- GCP survey second = only survey GCPs confirmed to be visible and usable

**If surveying GCPs first, then discovering invisibility during PtBox configuration:**
- Wasted survey time on unusable GCPs
- Need to return to site to survey additional GCPs
- Delays deployment

**Sample video and photo documentation prevent this problem.**

### Why GCPs After Video Confirmation

**From SURVEY_PROCESS.md Section 5:**

```
Survey each control point after video
Use Ground Control Points layer
```

**Purpose:**
GCPs are the most critical measurements in the entire survey. They establish the transformation from image to real-world coordinates. Accuracy requirement: 2-3cm. Take time to do this correctly.

**Procedure for each GCP:**

1. **Walk to GCP location with rover on pole**
2. **Position rover pole tip precisely on GCP marker center:**
   - For painted X: Place pole tip at intersection
   - For painted circle: Place pole tip at circle center
   - For survey stake: Place pole tip at stake top or nail
3. **Level pole using bubble level:**
   - Critical: pole must be vertical
   - Center bubble in circular level
   - Check from two perpendicular directions
4. **Verify RTK FIX quality gates:**
   - Solution type: FIX (not Float or Single)
   - Fix duration: ≥10 seconds (wait if recently achieved)
   - Satellites: ≥12 (standard) or ≥10 (canal)
   - PDOP: ≤2.5 (standard) or ≤3.0 (canal)
   - Horizontal precision: ≤2cm (standard) or ≤4cm (canal)
   - Vertical precision: ≤3cm (standard) or ≤6cm (canal)
   - Age of corrections: <3 seconds
5. **Start averaging:**
   - SW Maps begins 60s or 120s averaging (depending on configuration)
   - Keep pole vertical throughout averaging
   - Keep pole stable (use bipod if available)
   - Monitor quality indicators (if deteriorate, extend averaging or retry)
6. **Measure pole height:**
   - While averaging, use tape measure
   - Measure from pole tip (on GCP marker) to antenna reference point
   - Record measurement in field notebook: "GCP3: Pole height 2.15m"
   - This height will be subtracted from antenna elevation to get GCP ground elevation
7. **Fill in GCP attributes:**
   - point_id: GCP1, GCP2, GCP3, etc. (match numbering in sample video photo)
   - description: "Left bank, painted orange X on granite boulder, 8m upstream from camera"
   - marker_type: "Painted rock - orange X"
   - visibility: "Clear" (or "Partial" if marginal)
   - surveyed_by: Operator name
   - survey_time: Timestamp (usually auto-filled)
   - satellites, pdop, h_precision, v_precision: Copy from quality indicators
   - notes: Any relevant observations ("Stable rock, good sky view", or "Partial tree cover, extended averaging to 120s")
8. **Save point in SW Maps**
9. **Photograph GCP:**
   - Close-up showing marker
   - Context showing surroundings
   - Annotate or label photos (GCP1_closeup.jpg, GCP1_context.jpg)
10. **Move to next GCP and repeat**

**Survey all 6-10 GCPs systematically.**

**Quality control during GCP survey:**
- Verify each GCP meets all quality gates before saving
- If quality gates not met: wait 2 minutes, move 2-3m, or extend averaging
- Do not rush or compromise on GCP accuracy
- GCPs determine transformation quality for entire deployment

**Time estimate:**
- Each GCP: 2-5 minutes (including positioning, quality verification, averaging, attributes, photo)
- 8 GCPs: 16-40 minutes total
- Worth the time investment for accurate transformation

### Why Water Level After GCPs

**From SURVEY_PROCESS.md Section 6:**

```
Water Level Survey:
- Survey water surface elevation with rover pole
- Note depth on pole, maintain RTK FIX
- Record in Water Level layer with flow conditions
- Document measurement method and accuracy
```

**Purpose:**
Water level at time of survey establishes the reference elevation for transformation. The homography assumes all features are on a plane (the water surface). If water level changes significantly between survey and operation, transformation accuracy degrades.

**Procedure:**

1. **Identify measurement point:**
   - Stable water surface area (not turbulent rapids or eddies)
   - Accessible for rover pole (bank edge, wading, or boat)
   - Representative of general water level (not local pooling or drawdown)

2. **Lower rover pole into water:**
   - Pole tip touches water surface
   - Monitor pole position with bubble level (keep vertical)
   - Achieve RTK FIX and quality gates

3. **Record depth on pole:**
   - Note where water line intersects pole (mark with hand or observation)
   - Example: "Water surface at 0.75m mark on pole"
   - This documents how far antenna is above water surface

4. **Average measurement (60s standard):**
   - Keep pole stable, tip just touching water surface
   - Pole tip should remain at water level (not pushed below)

5. **Measure pole height:**
   - From pole tip (water surface) to antenna reference point
   - Example: "Pole height 2.25m from water to antenna"

6. **Fill in attributes:**
   - point_id: WL1 or WATER_LEVEL_1
   - description: "Water level at left bank, calm surface"
   - measurement_method: "Rover pole to water surface"
   - flow_conditions: "Calm", "Moderate flow", "Turbulent", etc.
   - pole_depth_mark: "0.75m" (where water intersected pole)
   - notes: Document any challenges or special conditions

7. **Take photo:** Shows rover pole at water surface, documents conditions

**Why water level matters for transformation:**
- GCPs surveyed relative to water surface at survey time
- Camera will image water surface at operation time
- If water level changes by 50cm between survey and operation, transformation has 50cm vertical error
- For sites with variable water level: survey at typical operating level, or resurvey GCPs when water level changes significantly

**Water level measurement is quality control** ensuring GCPs and operational conditions match.

### Why Cross-Sections After Water Level

**From SURVEY_PROCESS.md Section 8:**

```
Cross-Section Survey:
- Establish LB/RB reference points on stable ground
- Plan station spacing (1-2m typical)
- Walk LB → RB systematically
- Each station: verify quality gates, 60-120s averaging
- Record station number, point role, water depth
- Measure pole height tip-to-ARP each shot
```

**Purpose:**
River bathymetry (cross-sectional profile) is needed for discharge calculation (Q = v × A, where A is cross-sectional area). While OpenRiverCam measures surface velocity, discharge requires knowing the cross-section geometry.

**Procedure:**

1. **Establish cross-section line:**
   - Typically perpendicular to flow direction
   - Spans full river width (left bank to right bank)
   - At representative location (not at obstruction, expansion, or constriction)

2. **Mark reference points:**
   - LB_START: Stable point on left bank (above water)
   - RB_END: Stable point on right bank (above water)
   - Survey both reference points with standard procedure
   - Reference points anchor cross-section and allow future resurvey

3. **Plan station spacing:**
   - 1-2 meter spacing typical (more stations for complex bathymetry, fewer for simple)
   - Closer spacing in areas with rapid depth change
   - Example: 15m wide river = 8-12 stations at 1.5-2m spacing

4. **Survey each station:**
   - Walk systematic transect from left bank to right bank
   - At each station:
     - Position rover pole vertically
     - If underwater: note water depth on pole (measure how far pole extends below water)
     - If on bank: note dry land
     - Achieve RTK FIX and quality gates
     - Average 60s (standard) or 120s (canal/challenging)
     - Measure pole height from tip to antenna
     - Fill in attributes:
       - point_id: XS1_ST1, XS1_ST2, etc. (Cross-section 1, Station 1, 2, etc.)
       - station_number: 1, 2, 3, ...
       - point_role: "Cross-section station" or "Bank reference"
       - water_depth: Depth at this station (measured on pole)
       - distance_from_LB: Distance along transect from left bank (can calculate later from coordinates)
     - Save point

5. **Complete transect:**
   - Survey all planned stations systematically
   - Do not skip stations (gaps make cross-section interpolation uncertain)
   - Verify reached right bank reference point

6. **Additional cross-sections if needed:**
   - Some sites benefit from multiple cross-sections (upstream/downstream, different flow conditions)
   - Follow same procedure, number as XS1, XS2, etc.

**Quality control for cross-sections:**
- Quality requirements can be slightly relaxed (5-10cm accuracy acceptable vs. 2-3cm for GCPs)
- Cross-section uses many measurements averaged to calculate area (individual point errors average out)
- Still verify RTK FIX and reasonable quality indicators
- Faster workflow than GCPs (less critical, can move through stations more quickly)

**Time estimate:**
- Simple cross-section (10 stations): 20-30 minutes
- Complex cross-section (20 stations): 40-60 minutes

---

## Team Roles and Coordination

For two-person team (recommended):

### Primary Operator (Rover)

**Responsibilities:**
- Carries rover pole between measurement points
- Positions pole precisely on markers or measurement points
- Monitors quality indicators (RTK fix, satellites, PDOP, precision)
- Decides when quality gates are met
- Starts averaging and collects measurements
- Measures pole height with tape measure
- Fills in attributes in SW Maps
- Saves points and verifies recorded correctly

**Skills:**
- Understands RTK quality indicators (trained on Chapter 5 concepts)
- Can identify when conditions meet quality gates
- Careful and systematic (precise pole positioning, accurate pole height measurement)
- Patient (waits for adequate quality rather than rushing)

### Secondary Operator (Base Monitor and Support)

**Responsibilities:**
- Monitors base station throughout survey (power, operation, RINEX logging)
- Checks base station periodically (every 1-2 hours)
- Maintains field notebook (records measurements, observations, conditions)
- Assists with pole positioning (holds bipod, checks bubble level from different angle)
- Measures pole height (cross-check primary operator's measurement)
- Handles camera for GCP and site documentation
- Marks GCP locations and maintains markers (paint, stakes, flags)
- Tracks survey progress (how many GCPs completed, time remaining)

**Communication:**
- Frequent verbal communication about quality (secondary confirms satellites, PDOP visible in GNSS Master)
- Collaborative decision-making (should we accept this measurement? extend averaging? move location?)

### Solo Operation

**If only one operator available:**
- Follow same procedures but perform all roles
- Check base station periodically (return to base every 1-2 hours)
- Route survey to pass near base (enables monitoring without long walks)
- Take extra care with pole leveling (no second observer to cross-check)
- Take extra photos (documentation compensates for lack of second observer)
- Allow more time (solo operation typically 30-50% slower than two-person team)

**Solo operation is feasible** but two-person team is more efficient and provides quality control through redundancy.

---

## Quality Control Throughout

Quality control is continuous, not just end-of-day:

### Real-Time Quality Checks

**Before starting each measurement:**
- [ ] RTK FIX achieved and maintained ≥10 seconds
- [ ] Satellite count ≥12 (standard) or ≥10 (canal)
- [ ] PDOP ≤2.5 (standard) or ≤3.0 (canal)
- [ ] Age of corrections <3 seconds
- [ ] Pole positioned precisely on marker or measurement point
- [ ] Pole vertical (bubble level centered)

**During averaging (60-120 seconds):**
- [ ] Pole remains stable (no movement or shifting)
- [ ] Pole remains vertical (monitor bubble level)
- [ ] RTK FIX maintained throughout (if lost, discard and retry)
- [ ] Quality indicators remain good (if deteriorate, extend averaging)

**After averaging, before saving:**
- [ ] Precision estimates meet thresholds (H ≤2cm/4cm, V ≤3cm/6cm)
- [ ] Position stable (coordinate display not jumping)
- [ ] Pole height measured and recorded
- [ ] Attributes filled in completely

**Only save measurement if all checks pass.**

### Check Point Monitoring

**From SURVEY_PROCESS.md Section 4:**

```
Monitor Throughout Day:
- CP_NOON: Re-measure after 4-6 hours
- CP_END: Final check before packing
- Total drift must be ≤3cm H, ≤4cm V
```

**CP_NOON measurement (after 4-6 hours):**
- Return to CP_START location
- Re-measure with same procedure (FIX 30s, average 60s)
- Compare to CP_START average position
- Calculate drift: Difference in H and V from CP_START

**Acceptable drift:**
- Horizontal: ≤3cm
- Vertical: ≤4cm

**If drift >3-4cm at CP_NOON:**
- Indicates problem (base station shifted, equipment issue, atmospheric anomaly)
- Investigate: Check base station (has tripod moved? is power stable?)
- If problem identified and fixed: Continue survey, but note time of fix in field notebook
- If no problem identified: Consider aborting survey (data may be unreliable)

**CP_END measurement (end of survey):**
- Final validation before leaving site
- Same procedure as CP_NOON
- Calculate cumulative drift from CP_START

**If cumulative drift CP_START to CP_END ≤3-4cm:**
- Survey successful, data reliable
- RTK system maintained accuracy throughout session

**If cumulative drift >3-4cm:**
- Survey data questionable
- Consider re-survey if critical, or note large uncertainty in documentation
- Investigate cause for future surveys

**Check point drift is the primary quality validation** for the entire survey session.

### Base Station Monitoring

**Throughout survey, periodically check:**
- [ ] Base station powered on (LEDs indicate normal operation)
- [ ] RINEX logging continuing (file size increasing in u-center)
- [ ] Base station stable (tripod has not shifted from marked position)
- [ ] No interference (people have not approached or bumped equipment)

**Check frequency:**
- Every 1-2 hours (quick walk to base station)
- After any unusual event (heavy wind, vehicle passing nearby, etc.)

**If base station has problem:**
- Rover will lose corrections (age of corrections increases, solution reverts to Float or Single)
- Fix immediately: Check power, check connections, restart if needed
- Document in field notebook: Time of interruption, duration, resolution

---

## Data Backup Procedures

**From SURVEY_PROCESS.md Section 9:**

```
End of Day:
- Export SW Maps data (CSV + native format)
- Multiple backups on different devices
```

### Immediate Backup

**Before leaving field site:**

1. **Export SW Maps data:**
   - Project → Export → Geopackage (native format, preserves all attributes and geometry)
   - Save as: `SiteName_YYYYMMDD_survey.gpkg` (e.g., `Ciliwung_20241115_survey.gpkg`)
   - Also export CSV for each layer (backup format, simpler but loses some metadata)

2. **Copy RINEX log from base station:**
   - Stop u-center database logging
   - Copy .ubx file to laptop and external drive
   - Save as: `Base_YYYYMMDD_SiteName.ubx`

3. **Copy photos and field notes:**
   - Transfer photos from camera/phone to laptop
   - Scan or photograph field notebook pages (if not using digital notes)

### Multiple Backups

**Create redundant copies:**

**Backup 1: Laptop**
- Primary working copy
- Used for post-processing

**Backup 2: External drive or USB stick**
- Carried separately from laptop
- Protects against laptop loss/damage

**Backup 3: Cloud storage**
- If internet available at site or upon return to office
- Upload to Google Drive, Dropbox, or organizational cloud
- Offsite backup protects against physical loss

**Backup 4: Phone or tablet**
- SW Maps data can be exported to device storage
- Photos already on phone
- Provides immediate redundancy even before returning to office

**Never leave field site with only one copy of data.** Data loss means complete re-survey.

### Data Verification Before Leaving Site

**Before packing equipment:**

1. **Verify SW Maps export successful:**
   - Check file exists and has reasonable size (>10 KB for even simple survey)
   - Open file (verify it loads correctly)
   - Check point count matches expected (counted GCPs + check points + cross-section)

2. **Verify RINEX log captured:**
   - Check .ubx file size (should be ~10-50 MB per hour logged)
   - Verify file created/modified timestamp matches survey time

3. **Verify photos captured:**
   - Count photos (should have close-up + context photo for each GCP, plus site photos)
   - Spot-check a few photos (verify image quality, not corrupted)

4. **Verify field notebook complete:**
   - Check point coordinates recorded
   - Antenna height recorded
   - Base station position recorded
   - Pole heights for GCPs recorded
   - Deviations or issues documented

**If any verification fails:**
- Fix immediately while still at site
- Re-export data, re-take photos, re-record notes as needed
- Do not leave site until all data verified

**Returning to site for missing data wastes time and resources.** Verify before leaving.

---

## End-of-Day Procedures

### Final Check Point Validation

**From SURVEY_PROCESS.md Section 9:**

```
Final Checks:
- Re-measure CP_END, calculate total drift
- Stop RINEX logging, record end time
```

1. **CP_END measurement:**
   - Follow same procedure as CP_START and CP_NOON
   - Save as CP_END in Check Point layer

2. **Calculate drift:**
   - Compare CP_END to CP_START average position
   - Horizontal drift: Difference in XY plane
   - Vertical drift: Difference in Z
   - Record in field notebook

3. **Evaluate drift:**
   - ≤3cm H, ≤4cm V: Excellent, survey successful
   - 3-5cm H, 4-6cm V: Acceptable, note larger uncertainty
   - >5cm H or >6cm V: Poor, survey quality questionable, consider re-survey

### Stop RINEX Logging

1. **Connect laptop to base station** (if disconnected)
2. **Stop logging in u-center:**
   - File → Database Logging → Stop
   - Record stop time in field notebook
3. **Calculate total logging duration:**
   - Example: Start 09:00, Stop 17:30 = 8.5 hours logged (good for PPP)
4. **Copy .ubx file immediately** (before disconnecting or powering off)

### Equipment Shutdown and Packing

**Systematic shutdown:**

1. **Rover:**
   - Stop GNSS Master and SW Maps
   - Disconnect USB OTG cable
   - Power off rover
   - Disconnect antenna
   - Pack rover, antenna, pole, bipod

2. **Base station:**
   - Verify RINEX log copied
   - Disconnect laptop
   - Power off base station
   - Disconnect antenna
   - Pack base station, tripod, antenna, cables

3. **Android device:**
   - Verify data exported and backed up
   - Power off or recharge for return trip

4. **Field equipment:**
   - Collect marking supplies, tape measure, field notebook
   - Pack camera and documentation materials
   - Leave no equipment or trash at site

### Site Restoration

**Leave site in appropriate condition:**
- If using survey stakes: Leave in place if permanent installation, or remove if temporary survey
- If used paint: Ensure markings are appropriate (coordinate with landowner/community)
- If site requires restoration: Document site condition, arrange follow-up if needed

### Documentation Completion

**Before leaving site vicinity:**

1. **Review field notebook** (ensure all sections complete)
2. **Verify data backups** (check multiple copies exist)
3. **Document any deviations from procedure:**
   - Example: "Extended averaging to 120s for GCP7 due to partial tree cover"
   - Example: "Base station check at 13:00 found power cable loose, reconnected, surveying continued"
4. **Record end time and team members:**
   - Survey end time: 17:30
   - Team: [Names]
   - Weather conditions: Sunny, light breeze, good visibility
   - Site conditions: Dry, stable, river level normal

### Return to Office Checklist

**Upon return:**

- [ ] Transfer all data to primary storage (project folder)
- [ ] Create backup copies on network drive or cloud
- [ ] Label data files clearly (site name, date, data type)
- [ ] Download photos and organize (name by GCP or subject)
- [ ] Transcribe field notes to digital format (if handwritten)
- [ ] Charge batteries for next survey
- [ ] Clean and inspect equipment (check for damage)
- [ ] Schedule PPP processing (submit RINEX to AUSPOS)

---

## Connection to PtBox Configuration

**Survey data flows into PtBox configuration:**

**GCP coordinates:**
- Exported from SW Maps (CSV or Geopackage)
- Imported into PtBox during camera configuration
- Used to calculate transformation (homography)

**Sample video:**
- Shows all GCPs in camera field of view
- Used to identify GCP pixel positions in PtBox
- Links image coordinates (pixels) to real-world coordinates (meters)

**Water level:**
- Documents water surface elevation at survey time
- Used to verify transformation plane matches operating conditions
- Updated in PtBox if water level changes significantly

**Cross-section:**
- Provides bathymetry for discharge calculation
- Imported into PtBox or separate analysis software
- Combined with velocity measurements to calculate Q = v × A

**Camera position:**
- Documents monitoring perspective
- Aids troubleshooting or system adjustment
- Reference for future maintenance or camera replacement

**Check point drift and base position:**
- Validates survey quality
- Provides confidence in transformation accuracy
- Documentation for quality assurance

**The complete survey package enables:**
1. Accurate transformation configuration (GCPs)
2. Discharge calculation (cross-section)
3. Water level correlation (water level measurements)
4. Quality validation (check point drift)
5. Future reference (complete documentation)

**Without complete survey:**
- Cannot configure transformation (missing GCPs or video)
- Cannot calculate discharge (missing cross-section)
- Cannot validate quality (missing check points)
- Cannot maintain system (missing documentation)

**Complete, accurate survey is the foundation** for reliable OpenRiverCam operation.

---

## Summary: Survey Execution Workflow

**Setup phase:**
- Establish base station, start survey-in (30-60 min)
- Assemble rover, achieve RTK FIX
- Verify quality gates met, system ready

**Measurement phase:**
1. **Check points:** Establish CP_START (3 measurements, verify repeatability)
2. **Camera position:** Survey camera location (60s averaging, record height/angles)
3. **Sample video:** Collect video showing all GCPs, confirm visibility
4. **GCPs:** Survey 6-10 GCPs (highest accuracy, 2-3cm, careful procedure)
5. **Water level:** Survey water surface elevation (documents conditions)
6. **Cross-sections:** Survey river bathymetry (10-20 stations per transect)
7. **Check points:** Re-measure CP_NOON after 4-6 hours, verify drift ≤3-4cm

**Closure phase:**
- Re-measure CP_END, validate total drift ≤3-4cm
- Stop RINEX logging (record end time, total duration)
- Export all survey data from SW Maps
- Multiple backups (laptop, external drive, cloud, phone)
- Pack equipment systematically
- Document deviations and complete field notes

**Quality control:**
- Real-time verification before saving each point (FIX, satellites, PDOP, precision)
- Check point monitoring throughout day (CP_START, CP_NOON, CP_END)
- Base station monitoring (power, logging, stability)
- Data verification before leaving site

**Time estimate:**
- Setup: 60-120 minutes (includes base station survey-in)
- Check points: 15-20 minutes (CP_START)
- Camera + video: 15-20 minutes
- GCPs (8 points): 20-40 minutes
- Water level: 5-10 minutes
- Cross-section: 20-60 minutes (depends on complexity)
- CP_NOON: 5 minutes
- Additional measurements: Variable
- Closure + CP_END: 30-45 minutes
- **Total: 4-6 hours typical** (complete site survey)

**Outcomes:**
- 8-10 GCPs surveyed to 2-3cm accuracy with full documentation
- Check point drift validates RTK system quality throughout session
- Water level and cross-section provide discharge calculation data
- Camera position and sample video enable PtBox configuration
- Complete data package backed up redundantly
- Quality-controlled survey ready for post-processing and transformation

**With survey execution complete, you have:**
- Accurate ground control for transformation (Section 4.3 connection)
- Validated survey quality (check point drift ≤3-4cm)
- Complete data for OpenRiverCam deployment
- RINEX data for PPP post-processing (Section 9.1 global frame)

**Next steps (beyond this chapter):**
- PPP post-processing (SURVEY_PROCESS.md Section 10)
- PtBox configuration with GCPs and sample video
- Transformation validation (reprojection error analysis)
- System calibration and testing

Chapter 9 has taken you from survey concepts (Section 9.1) through preparation (9.2), GCP planning (9.3), hardware setup (9.4), software configuration (9.5), and complete survey execution (9.6). You now have the knowledge and procedures to conduct accurate, quality-controlled surveys for OpenRiverCam deployment.

---

**End of Chapter 9: Site Survey**
