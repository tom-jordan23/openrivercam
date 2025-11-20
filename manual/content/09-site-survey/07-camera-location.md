# 9.7 Survey Execution - Camera Location

This section covers the practical procedure for surveying the camera mounting position. Camera position documentation establishes the monitoring perspective and provides reference data for system configuration, maintenance, and troubleshooting.

While camera position accuracy is less critical than GCP accuracy (10-20cm acceptable vs. 2-3cm for GCPs), recording this information systematically supports long-term monitoring success and enables future adjustments or equipment replacement.

By the end of this section, you will be able to:
- Survey camera mounting position accurately
- Record camera height above water
- Document viewing direction and tilt angle
- Record camera position attributes in SW Maps
- Connect camera position data to GCP survey and PtBox configuration

**Reference:** SURVEY_PROCESS.md Section 5 - Camera & Control Points

---

## When to Survey Camera Position

**In the survey workflow sequence:**

1. Establish check points (CP_START) - validates system quality
2. **Survey camera position - documents monitoring setup** ← YOU ARE HERE
3. Collect sample video - confirms GCP visibility
4. Survey GCPs - establishes transformation
5. Survey water level - documents hydraulic conditions
6. Survey cross-section - provides discharge calculation data

**Survey camera position after establishing check points but before GCP survey.** Camera position measurement is quick (5-10 minutes) and provides context for the subsequent GCP placement.

---

## Camera Position Measurement Purpose

### Why Record Camera Position

**System documentation:**
- Establishes monitoring perspective for reference
- Aids interpretation of field of view and GCP distribution
- Provides baseline for future adjustments

**Troubleshooting support:**
- If camera shifts or requires repositioning, original position is documented
- Enables comparison between survey-time and operation-time camera position
- Supports transformation validation (verifies camera perspective matches assumptions)

**Engineering reference:**
- Documents installation for maintenance crews
- Provides data for site planning and system expansion
- Supports analysis of optimal camera placement

**Camera position is primarily documentation, not transformation data.** Transformation uses GCP positions (measured to 2-3cm accuracy) rather than camera position. However, documenting camera position improves overall system understanding and maintainability.

### What to Measure

**From SURVEY_PROCESS.md Section 5:**

```
Camera Position:
- 5-10m height, 15-45° viewing angle
- Survey camera position with rover
- Record height, direction, tilt angle
```

**Four key measurements:**

1. **Camera position coordinates (X, Y, Z):** RTK survey of camera mounting point
2. **Height above water:** Vertical distance from camera to water surface
3. **Viewing direction:** Compass bearing the camera looks toward (azimuth)
4. **Tilt angle:** Angle below horizontal the camera points (depression angle)

**These measurements establish the camera's position and orientation in 3D space.**

---

## Camera Position Survey Procedure

### Step 1: Locate Camera Mounting Point

**If camera already installed:**
- Survey the exact mounting point (bracket, pole mount, or attachment location)
- Position rover pole directly beneath camera lens (vertical projection)
- Note any offset if pole cannot reach exact point (record offset distance and direction)

**If camera not yet installed (pre-installation survey):**
- Survey the planned mounting location identified during site planning
- Mark exact position where camera will be mounted (paint, stake, or marker)
- Document mounting method planned (pole, bracket, tree mount, etc.)

**Ensure rover pole positioned as close as possible to camera lens horizontal position.** If mounting point is elevated (on pole or bracket) and inaccessible, survey ground point directly beneath camera and record vertical offset.

### Step 2: Achieve RTK FIX and Verify Quality

**Standard quality gates for camera position measurement:**

- [ ] Solution type: RTK FIX (not Float or Single)
- [ ] Fix maintained: ≥10 seconds
- [ ] Satellites: ≥12 (standard conditions) or ≥10 (challenging conditions)
- [ ] PDOP: ≤2.5 (standard) or ≤3.0 (canal/urban)
- [ ] Horizontal precision: ≤5cm (relaxed vs. GCP requirement of ≤2cm)
- [ ] Vertical precision: ≤8cm (relaxed vs. GCP requirement of ≤3cm)
- [ ] Age of corrections: <3 seconds

**Camera position quality requirements are relaxed compared to GCPs** because camera position is documentation rather than transformation-critical. Accuracy of 5-10cm is sufficient for this purpose.

**If quality gates not met:**
- Wait 2 minutes for conditions to improve
- Check base station status (verify RTCM corrections flowing)
- Move slightly if obstructions affecting signal (2-3m adjustment)
- Extend averaging time if marginal quality

### Step 3: Start Averaging and Measure Pole Height

**Averaging time:**
- **Standard: 60 seconds** (typical for camera position)
- **Challenging conditions: 120 seconds** (if quality marginal or near obstructions)

**While averaging is running:**

1. **Keep rover pole vertical:**
   - Monitor bubble level throughout 60-second averaging
   - Use bipod if available (improves stability)
   - Ensure pole does not shift or lean during averaging

2. **Measure pole height:**
   - Use tape measure from pole tip to antenna reference point (ARP)
   - Record measurement in field notebook: "Camera position: Pole height 2.05m"
   - This height will be subtracted from antenna elevation to get ground/mounting point elevation

**If camera is elevated (on pole or bracket):**
- After surveying ground point, measure vertical distance from ground to camera lens
- Record this additional height: "Camera elevation above survey point: 3.5m"
- Total camera height = pole height calculation + elevation above survey point

### Step 4: Record Camera Position Attributes in SW Maps

**In SW Maps, use the "Camera Location" layer** (configured in Section 9.5).

**Fill in all attributes:**

**Required fields:**
- `point_id`: CAM1, CAMERA_1, or similar identifier
- `description`: "Camera mounting point on left bank, 12m upstream from GCP cluster"
- `surveyed_by`: Operator name
- `survey_time`: Timestamp (usually auto-filled by SW Maps)

**Measurement quality fields:**
- `satellites`: Number of satellites tracked (from quality indicators)
- `pdop`: Position dilution of precision value
- `h_precision`: Horizontal precision estimate (cm)
- `v_precision`: Vertical precision estimate (cm)
- `fix_duration`: How long FIX was maintained during averaging (≥60s)

**Camera-specific fields:**
- `pole_height`: Height from pole tip to antenna (e.g., 2.05m)
- `height_above_water`: Distance from camera to water surface (measure with tape or calculate from coordinates)
- `direction`: Compass bearing camera points (azimuth in degrees, 0-360°)
- `tilt_angle`: Angle below horizontal (depression angle, typically -15° to -45°)
- `mounting_type`: "Pole mount", "Tree bracket", "Steel frame", etc.
- `notes`: Additional observations ("Mounted at 3.5m on steel pole", "Clear field of view across river", "Partial obstruction from downstream tree")

**Save point in SW Maps after all attributes filled.**

### Step 5: Measure and Document Height Above Water

**Two methods for determining height above water:**

**Method 1: Direct measurement with tape measure (if accessible):**
- Lower tape measure from camera lens to water surface
- Record vertical distance directly
- Most accurate method if camera and water both accessible

**Method 2: Calculate from survey coordinates (typical approach):**
- Survey camera position with rover (obtain camera elevation Z_cam)
- Survey water level with rover (obtain water surface elevation Z_water, Section 9.9)
- Calculate height above water: h = Z_cam - Z_water
- Example: Camera at 148.25m elevation, water at 140.15m elevation = 8.10m height above water

**Record height above water in camera position attributes** (height_above_water field). This measurement provides quick reference for field of view interpretation and GCP planning.

**Typical height above water for OpenRiverCam:**
- Small streams: 3-6 meters
- Medium rivers: 5-10 meters
- Large rivers: 8-15 meters

**If height <3m:** May have limited field of view, risk of camera getting wet during high flows
**If height >15m:** May have difficulty resolving surface features, requires longer focal length

### Step 6: Document Viewing Direction and Tilt Angle

**Viewing direction (azimuth):**

**Using compass:**
1. Stand at camera position
2. Point compass in direction camera will look (or is looking if already installed)
3. Read bearing in degrees (0-360°)
4. Example: Camera pointing northeast = approximately 045°
5. Record in `direction` attribute

**Common viewing directions:**
- 000° = North (camera looking downstream toward north)
- 090° = East (camera looking across river toward east bank)
- 180° = South (camera looking downstream toward south)
- 270° = West (camera looking across river toward west bank)

**If compass not available:**
- Use phone compass app (adequate accuracy for this purpose)
- Estimate from map orientation (less accurate but better than no documentation)
- Note method used: "Direction estimated from site map: ~045°"

**Tilt angle (depression angle):**

**Using clinometer or angle measuring tool:**
1. Position clinometer or angle tool parallel to camera viewing line
2. Measure angle below horizontal
3. Record as negative value (e.g., -30° means camera tilted 30° below horizontal)

**If angle measuring tool not available:**
- Estimate based on camera positioning during installation
- Typical range: -15° to -45° (steeper angles for closer monitoring, shallower for distant field of view)
- Note estimation method: "Tilt angle estimated: approximately -35°"

**Using smartphone inclinometer app:**
1. Hold phone parallel to expected camera viewing line
2. Read angle from horizontal (phone apps typically show 0° = horizontal, negative values = downward tilt)
3. Record value with note: "Measured with phone inclinometer"

**Record tilt angle in `tilt_angle` attribute** (e.g., -30, -35, -40).

**Why viewing direction and tilt angle matter:**
- Defines camera field of view geometry
- Aids GCP placement (GCPs should be distributed across field of view)
- Supports future camera adjustment or replacement
- Helps interpret transformation geometry and potential distortions

### Step 7: Photograph Camera Position

**Documentation photos:**

1. **Camera mounting point close-up:**
   - Shows exact position surveyed
   - Includes any markers or identifiers
   - Clear view of mounting hardware (if installed)

2. **Context photo from river:**
   - Stand in river (or on opposite bank)
   - Photograph showing camera position relative to river
   - Demonstrates camera field of view and monitoring perspective

3. **View from camera position:**
   - Stand at camera mounting point
   - Photograph river view showing what camera will see
   - Helps interpret GCP placement and field of view coverage

**Label photos clearly:**
- CAM1_mounting_point.jpg
- CAM1_view_from_river.jpg
- CAM1_field_of_view.jpg

**Photos support:**
- Site documentation and reporting
- Troubleshooting and system adjustment
- Training and knowledge transfer
- Future reference for maintenance or reinstallation

---

## Quality Checks for Camera Position Survey

**Before saving camera position point, verify:**

- [ ] RTK FIX maintained throughout 60-second averaging
- [ ] Quality indicators within acceptable range (H ≤5cm, V ≤8cm)
- [ ] Pole height measured and recorded (field notebook and SW Maps)
- [ ] All attributes filled in SW Maps (point_id, description, height_above_water, direction, tilt_angle)
- [ ] Coordinates are reasonable (compare to base station coordinates, check distance and elevation difference)
- [ ] Position marker clearly documented (photo taken, location described in notes)

**If any check fails:**
- Extend averaging time (try 120 seconds if 60 seconds insufficient)
- Adjust rover position slightly (move away from obstructions or multipath sources)
- Re-measure if quality poor (better to spend extra 5 minutes than accept poor data)

**Only save camera position point after all quality checks pass.**

---

## Common Issues and Solutions

### Issue: Camera position inaccessible with rover pole

**Symptoms:**
- Camera mounted high on pole or bracket
- Rover pole cannot reach mounting point
- Survey crew cannot access exact camera position safely

**Solutions:**
- Survey ground point directly beneath camera horizontal position
- Measure vertical offset from ground to camera lens (tape measure or known pole height)
- Record offset in notes: "Ground point surveyed, camera is 3.5m above this point"
- Calculate camera elevation: Z_camera = Z_ground + offset

### Issue: Poor GPS conditions at camera position

**Symptoms:**
- Satellites <12, PDOP >3.0
- RTK FIX intermittent or takes long time to achieve
- Precision estimates >10cm

**Solutions:**
- Wait for satellite geometry to improve (10-20 minutes)
- Move slightly to avoid obstructions (tree branches, overhangs, reflective surfaces)
- Use longer averaging time (120 seconds instead of 60 seconds)
- Accept slightly lower quality for camera position (5-10cm acceptable, unlike 2-3cm required for GCPs)
- If conditions very poor: skip camera position survey, focus on GCPs (camera position is documentation, not transformation-critical)

### Issue: Uncertain viewing direction or tilt angle

**Symptoms:**
- Camera not yet installed, direction not finalized
- Compass readings inconsistent
- Difficult to estimate tilt angle without installed camera

**Solutions:**
- Record best estimate with note explaining uncertainty: "Direction estimated: ~045°, subject to adjustment during installation"
- Use site plan or GCP layout to infer likely direction: "Camera will view northeast toward GCP cluster"
- Leave fields partially filled, update during installation or post-installation verification
- Prioritize surveying camera position coordinates (most important), document angles as estimates if needed

### Issue: Water level not yet surveyed

**Symptoms:**
- Height above water unknown (water level not yet measured)
- Cannot calculate vertical distance to water surface

**Solutions:**
- Leave `height_above_water` field blank initially
- Calculate and update after water level surveyed (Section 9.9)
- Use tape measure for rough estimate if needed: "Approximately 8m above water, to be confirmed after water level survey"

---

## Recording Camera Position Data

### Field Notebook Documentation

**Record in field notebook:**

```
Camera Position Survey (CAM1)
Date: 2024-11-15
Time: 10:15
Location: Left bank, 12m upstream from main GCP cluster

Survey data:
- Point ID: CAM1
- Coordinates: E=685445.23, N=9456795.47, Z=148.25 (UTM 48S)
- Pole height: 2.05m
- Mounting elevation: 3.5m above survey point (on steel pole)
- Total camera elevation: Z = 148.25 + 3.5 = 151.75m

Camera orientation:
- Direction: 045° (northeast, looking across river)
- Tilt angle: -35° (moderate downward tilt)
- Field of view: Covers 20m river section, includes GCP1-GCP8

Quality indicators:
- Satellites: 14
- PDOP: 1.8
- H precision: 3cm
- V precision: 5cm
- Fix duration: 60s continuous

Notes:
- Camera mounted on 4m steel pole, survey at pole base
- Clear field of view, no obstructions
- Height above water (calculated later): 151.75 - 140.15 = 11.6m
```

**Field notebook serves as backup** if SW Maps data is lost or attributes incomplete.

### SW Maps Layer: Camera Location

**Verify data saved correctly in SW Maps:**

1. Open Camera Location layer in SW Maps
2. Verify point appears on map at expected location
3. Review attributes (tap point, view attribute table)
4. Check coordinates are reasonable (within site area, elevation sensible)
5. Verify all required fields filled

**If data incomplete or incorrect:**
- Edit attributes in SW Maps (tap point, edit, update fields)
- Re-survey if coordinates poor quality (better to re-measure than accept bad data)

---

## Connection to Subsequent Survey Steps

### Camera Position Informs GCP Placement

**After surveying camera position, you know:**
- Camera height above water (elevation difference)
- Camera viewing direction (azimuth toward river)
- Camera field of view orientation (tilt angle affects visible area)

**This information guides GCP placement:**
- GCPs should distribute across camera field of view
- Near GCPs (closer to camera): provide transformation accuracy in foreground
- Far GCPs (farther from camera): provide transformation accuracy in background
- Left/right GCPs: ensure coverage across full image width
- Vertical spread: GCPs at different elevations (banks and water level) capture 3D geometry

**Camera position documentation helps validate GCP distribution is adequate.**

### Camera Position Supports Sample Video Interpretation

**When collecting sample video (Section 9.8):**
- Camera direction and tilt documented from camera position survey
- Field of view extent predictable from height above water and tilt angle
- Sample video confirms GCPs visible within expected field of view
- Any discrepancies between expected and actual field of view indicate need for camera adjustment

### Camera Position Provides PtBox Configuration Reference

**During PtBox configuration:**
- Camera position coordinates available for reference
- Height above water helps interpret scale in image (pixels per meter)
- Direction and tilt help interpret perspective distortion
- Camera position data aids troubleshooting if transformation quality poor

**Camera position is supporting data, not required for transformation** (GCPs provide transformation data). But documenting camera position improves system understanding and aids future work.

---

## Time Estimate

**Camera position survey: 5-10 minutes total**

- Locate mounting point and position rover: 1-2 minutes
- Achieve RTK FIX and verify quality: 1-2 minutes
- Averaging (60 seconds) and measure pole height: 2 minutes
- Fill in attributes in SW Maps: 2-3 minutes
- Measure height above water or viewing angles: 1-2 minutes
- Photograph camera position: 1-2 minutes

**Camera position is quick measurement** compared to GCP survey (20-40 minutes for 8 GCPs) or cross-section survey (20-60 minutes). Worth the small time investment for complete site documentation.

---

## Summary: Camera Position Survey

**Purpose:**
- Document camera mounting position and orientation
- Provide reference for GCP placement and field of view interpretation
- Support future maintenance, troubleshooting, and system adjustment

**Key measurements:**
- Camera position coordinates (X, Y, Z) surveyed with RTK rover
- Height above water (vertical distance from camera to water surface)
- Viewing direction (compass bearing, azimuth 0-360°)
- Tilt angle (depression angle below horizontal, typically -15° to -45°)

**Quality requirements:**
- RTK FIX maintained for 60-120 seconds averaging
- Accuracy: 5-10cm (relaxed vs. GCP requirement of 2-3cm)
- Pole height measured and recorded
- All attributes documented in SW Maps and field notebook

**Workflow sequence:**
1. Check points (CP_START) established
2. **Camera position surveyed** ← COMPLETED
3. Next: Sample video collection (Section 9.8)

**With camera position documented, you have:**
- Reference point for monitoring system geometry
- Baseline for GCP placement planning
- Documentation for future camera adjustment or replacement
- Context for interpreting sample video and GCP visibility

**Move forward to Section 9.8** to collect sample video and confirm all GCPs visible in camera field of view before investing time surveying GCPs to high accuracy.

---

**References:**
- SURVEY_PROCESS.md Section 5: Camera & Control Points
- Section 9.6: Survey Execution - Process Overview (workflow context)
- Section 9.8: Survey Execution - Control Points and Sample Video (next step)
- Section 9.9: Survey Execution - Water Level (height above water calculation)
