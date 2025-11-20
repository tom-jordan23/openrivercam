# 9.8 Survey Execution - Control Points and Sample Video

This section covers the critical procedure for collecting sample video and surveying Ground Control Points (GCPs). GCPs are the foundation of the coordinate transformation that converts camera image pixels to real-world geographic coordinates. This is the most accuracy-critical measurement in the entire survey.

Sample video collection comes before GCP survey to confirm all planned GCPs are visible in the camera field of view. No point surveying GCPs to 2cm accuracy if they cannot be seen in the image.

By the end of this section, you will be able to:
- Connect to PtBox and collect sample video showing all GCPs
- Confirm GCP visibility and adjust placement if needed
- Photograph and number GCPs for reference
- Survey each GCP to required accuracy (2-3cm)
- Record complete GCP attributes in SW Maps
- Verify GCP distribution meets transformation requirements

**Reference:** SURVEY_PROCESS.md Section 5 (Camera & Control Points) and Appendix D (Sample Video Collection)

---

## Survey Workflow Position

**In the complete survey sequence:**

1. Establish check points (CP_START)
2. Survey camera position
3. **Collect sample video and photograph GCPs** ← YOU START HERE
4. **Survey all GCPs to high accuracy** ← THEN COMPLETE THIS
5. Survey water level
6. Survey cross-section
7. Re-measure check points (CP_NOON, CP_END)

**Sample video first, GCP survey second.** This sequence prevents wasted effort surveying GCPs that turn out to be invisible or poorly visible in the camera image.

---

## Part 1: Sample Video Collection

Sample video serves two critical purposes:
1. **Validation:** Confirms all planned GCPs are visible in camera field of view
2. **Reference:** Provides image data for identifying GCP pixel positions during PtBox configuration

**From SURVEY_PROCESS.md Appendix D:**

```
Sample Video Collection:
- Connect to PtBox, put in Maintenance Mode
- Select "Aim the camera in the field"
- Take a 5 second video, note video name and timestamp
- Ensure all control points visible in video
- Take a photo and number the control points for reference
```

### Step 1: Connect to PtBox

**Prerequisites:**
- PtBox powered on and accessible (connected to local network or direct WiFi)
- Camera already mounted or temporarily positioned at survey location
- GCP markers already placed (Section 9.3 guidance)
- Survey crew has WiFi-capable device (laptop, tablet, or phone)

**Connection procedure:**

1. **Put PtBox in Maintenance Mode:**
   - Access PtBox via FTP service or web interface
   - Navigate to maintenance/service menu
   - Activate Maintenance Mode
   - Wait for PtBox to restart and come online (typically 2-3 minutes)

2. **Log into PtBox web interface:**
   - Open web browser on WiFi device
   - Navigate to PtBox IP address (typically provided during site planning)
   - Enter credentials (username and password)
   - Verify connection successful

3. **Select "Aim the camera in the field":**
   - This mode provides live camera view without starting full recording
   - Allows preview of field of view and GCP visibility
   - Enables test video capture

**IMPORTANT NOTE from SURVEY_PROCESS.md:**
> Do not try to start the cameras in this view. This PtBox has a bad camera, and attempting to start the bad camera will cause the PtBox to lock up.

**If PtBox locks up:**
- Power cycle the PtBox (disconnect power, wait 30 seconds, reconnect)
- Wait for reboot (2-3 minutes)
- Reconnect and resume (avoid triggering camera start that caused lockup)

### Step 2: Frame the Camera View

**With live camera preview active:**

1. **Check field of view extent:**
   - Verify river section of interest is visible
   - Confirm left bank to right bank coverage adequate
   - Check upstream and downstream extent matches site plan

2. **Verify GCP visibility:**
   - Scan systematically through each planned GCP location
   - Confirm GCP markers visible in image
   - Assess visibility quality:
     - **Clear:** GCP marker easily identifiable, high contrast, fully visible
     - **Partial:** GCP marker visible but low contrast, partial obstruction, or edge of frame
     - **Obscured:** GCP marker blocked by vegetation, glare, shadows, or outside frame

3. **Adjust camera if needed:**
   - If GCPs obscured or outside frame: Adjust camera pan, tilt, or zoom
   - If partial visibility: Consider adjusting camera or moving GCP markers
   - Goal: All GCPs clearly visible with good contrast

**Do not proceed to video capture until satisfied with GCP visibility.** Easier to adjust now than to resurvey GCPs later.

### Step 3: Capture Sample Video

**Recording the sample video:**

1. **Start recording:**
   - Use PtBox interface to capture video (button typically labeled "Capture" or "Record Test Video")
   - Record for 5-30 seconds (5 seconds minimum, longer if water moving or multiple flow conditions)

2. **Note video details:**
   - Record video filename (PtBox typically auto-generates, e.g., "test_video_20241115_1045.mp4")
   - Record timestamp (date and time of capture)
   - Document in field notebook: "Sample video: test_video_20241115_1045.mp4 at 10:45 local time"

3. **During video capture:**
   - Keep camera stable (do not adjust pan/tilt during recording)
   - Ensure water surface visible (transformation assumes planar water surface)
   - If possible, capture some water motion (aids velocity validation later)

**Video requirements:**
- **Minimum duration:** 5 seconds (enough to capture stable image and identify GCPs)
- **All GCPs visible:** Each GCP marker must appear clearly in at least some video frames
- **Water surface visible:** Transformation assumes GCPs reference water surface plane
- **Stable image:** Camera not moving during capture (if camera mount not finalized, stabilize temporarily)

### Step 4: Review Video Immediately

**Playback and verification:**

1. **Play back video in PtBox interface or download for review:**
   - Watch entire video start to finish
   - Verify recording quality adequate (not corrupted, frozen, or blank)

2. **Systematically check each GCP:**
   - GCP1: Visible? Clear or partial? Can you identify marker precisely?
   - GCP2: Visible? Clear or partial? Can you identify marker precisely?
   - (Continue for all GCPs)

3. **Assess overall GCP distribution:**
   - Are GCPs spread across field of view (left/right, near/far)?
   - Are any areas of field of view lacking GCP coverage?
   - Are there too many GCPs clustered in one area?

**Quality criteria for sample video:**
- [ ] All planned GCPs visible in at least some video frames
- [ ] GCP markers identifiable with reasonable confidence (can point to precise location)
- [ ] Water surface clearly visible
- [ ] Video quality adequate (resolution, focus, exposure)
- [ ] No major obstructions or glare obscuring critical areas

**If quality criteria not met:**
- Adjust camera position, pan, tilt, or zoom
- Move or enhance GCP markers (repaint, add flags, improve contrast)
- Capture new sample video
- Repeat until satisfied with GCP visibility

**Only proceed to GCP survey after confirming sample video shows all GCPs clearly.**

### Step 5: Capture Photo and Number GCPs

**From SURVEY_PROCESS.md Appendix D:**
> Also take a photo, and use the photo to number the control points so that you have a reference to use when entering the control points into the PtBox software later.

**Photo capture procedure:**

1. **Capture still image from live camera view:**
   - Use PtBox interface to capture photo (or extract frame from sample video)
   - Save image with clear filename: "GCP_reference_20241115.jpg"

2. **Download photo to field device:**
   - Transfer photo to laptop, tablet, or phone
   - Use image editing software or annotation app

3. **Annotate photo with GCP numbers:**
   - Mark each GCP location in photo with number (GCP1, GCP2, GCP3, etc.)
   - Add arrow or circle highlighting each GCP marker
   - Ensure numbering is clear and legible

**Example annotation:**
```
[Image of river with arrows and labels]
GCP1 → (left bank, orange X on rock)
GCP2 → (left bank, painted circle)
GCP3 → (mid-channel, floating target)
GCP4 → (right bank, stake with flag)
...etc...
```

**Purpose of numbered photo:**
- **Field reference:** Survey crew knows which physical marker corresponds to which GCP number
- **PtBox configuration reference:** When entering GCP pixel positions in PtBox, analyst can identify which GCP is which
- **Quality control:** Prevents mix-ups between similar-looking GCPs
- **Documentation:** Permanent record of GCP numbering scheme for this survey

**Save annotated photo with survey data** (include in backup and export with other survey files).

---

## Part 2: GCP Survey Procedure

With sample video confirming all GCPs are visible, now survey each GCP to high accuracy. GCPs are the most critical measurements in the entire survey because they establish the coordinate transformation accuracy.

**Accuracy requirement: 2-3cm** (compared to 5-10cm for camera position, or 5-10cm for cross-section stations). Take time and care with GCP survey - transformation quality depends on it.

### GCP Survey Workflow for Each GCP

For each GCP, follow this systematic procedure:

### Step 1: Walk to GCP Location with Rover

**Approach GCP systematically:**
- Survey GCPs in logical order (e.g., left bank to right bank, or upstream to downstream)
- Carry rover on pole (antenna remains connected and tracking satellites)
- Monitor RTK FIX status as you move (should remain in FIX mode between measurement points)

**Identify GCP marker:**
- Refer to numbered photo and field plan
- Locate physical marker (painted X, painted circle, survey stake, flag, etc.)
- Verify this is correct GCP (match marker appearance to plan and photo)

### Step 2: Position Rover Pole Precisely on GCP Marker

**Pole positioning is critical for accuracy:**

1. **Place pole tip on GCP marker center:**
   - For painted X: Position pole tip exactly at intersection of X
   - For painted circle: Position pole tip at circle center
   - For survey stake: Position pole tip on stake top or nail (if nail driven into stake top)
   - For natural feature: Position pole tip at identified reference point (e.g., specific point on rock)

2. **Level the pole using bubble level:**
   - **Critical:** Pole must be vertical (not leaning)
   - Check circular bubble level on rover or pole
   - Center bubble precisely (bubble must be in center circle, not just close)
   - If rover has dual-axis bubble level, check from two perpendicular directions

3. **Stabilize the pole:**
   - If using bipod: Set up bipod and position pole in bipod (much easier to maintain vertical and stable position)
   - If handheld: Brace pole against your body or use two hands for stability
   - Minimize movement during averaging (wind, hand tremor, shifting weight)

**Pole positioning accuracy directly affects GCP coordinate accuracy.** If pole is 5cm off center or leaning 2° from vertical, GCP coordinates will have corresponding error. Take care with positioning.

### Step 3: Verify RTK FIX and Quality Gates

**Before starting averaging, verify all quality gates met:**

**From SURVEY_PROCESS.md quality gates for standard conditions:**

- [ ] Solution type: **RTK FIX** (not Float, DGNSS, or Single)
- [ ] Fix maintained: **≥10 seconds** (wait if just achieved FIX)
- [ ] Satellites tracked: **≥12** (standard) or **≥10** (canal/urban)
- [ ] PDOP: **≤2.5** (standard) or **≤3.0** (canal/urban)
- [ ] Horizontal precision estimate: **≤2cm** (standard) or **≤4cm** (canal)
- [ ] Vertical precision estimate: **≤3cm** (standard) or **≤6cm** (canal)
- [ ] Age of corrections: **<3 seconds** (recent corrections from base station)

**How to check quality gates in SW Maps:**
- Satellite count: Displayed in GPS status indicator or info panel
- PDOP: Displayed in GPS status (lower is better, <2.5 excellent)
- Precision estimates: H precision and V precision values (check before starting averaging)
- Fix type: Status shows "RTK FIX" (green indicator typically)
- Age of corrections: Check RTCM status (should be <3s, indicates recent base station data)

**If any quality gate not met:**
- **Wait 2 minutes:** Satellite geometry changes, PDOP may improve
- **Check base station:** Verify base station still operating (radio link, RTCM corrections flowing)
- **Move 2-3 meters:** Multipath or obstruction may be affecting this specific location
- **Extend averaging time:** 120 seconds instead of 60 seconds if quality marginal
- **Do not compromise on quality for GCPs:** GCP accuracy determines transformation quality for entire deployment

**Only proceed to averaging when all quality gates met.**

### Step 4: Start Averaging

**SW Maps averaging procedure:**

1. **Select Ground Control Points layer in SW Maps**
2. **Tap "Add Point" or "Collect Feature"** (button to start new point collection)
3. **SW Maps begins averaging:**
   - **Standard averaging time: 60 seconds** (adequate for good conditions)
   - **Canal/challenging conditions: 120 seconds** (recommended if PDOP marginal, satellite count low, or near obstructions)
4. **Countdown timer displays progress** (e.g., "Averaging: 45 seconds remaining")

**During the 60-120 second averaging period:**

- [ ] **Keep pole vertical:** Monitor bubble level continuously, maintain level throughout averaging
- [ ] **Keep pole stable:** Do not shift position, minimize movement (use bipod if available)
- [ ] **Monitor RTK FIX:** Verify FIX maintained throughout averaging (if reverts to Float or Single, discard and retry)
- [ ] **Monitor quality indicators:** If precision estimates degrade during averaging, consider extending averaging time
- [ ] **Prepare for pole height measurement:** Have tape measure ready

**If FIX lost during averaging:**
- SW Maps typically discards measurement automatically
- Reposition pole, re-achieve FIX, start new averaging
- Investigate cause: Did base station lose power? Radio interference? Obstruction moved into signal path?

### Step 5: Measure Pole Height

**While averaging is running (or immediately after):**

1. **Measure from pole tip to antenna reference point (ARP):**
   - Pole tip: Positioned precisely on GCP marker
   - Antenna reference point: Marked on antenna or documented in equipment specifications (typically bottom of antenna or specific reference mark)
   - Stretch tape measure vertically along pole
   - Read measurement carefully (to nearest millimeter if possible)

2. **Record pole height in field notebook:**
   - Example: "GCP3: Pole height 2.15m"
   - Record immediately (easy to forget or confuse with previous measurement)

3. **Why pole height matters:**
   - Antenna measures its own elevation (height above ellipsoid)
   - GCP is at ground level (pole tip)
   - GCP elevation = Antenna elevation - Pole height
   - If pole height wrong by 5cm, GCP elevation wrong by 5cm

**Common pole heights for typical rover poles:**
- Short pole: 1.5-2.0m
- Medium pole: 2.0-2.5m
- Long pole: 2.5-3.0m

**Measure pole height for EVERY GCP measurement.** Pole height can vary slightly between measurements (pole extends/contracts, setup differs, operator height affects comfortable pole length).

### Step 6: Fill in GCP Attributes in SW Maps

**After averaging completes, SW Maps prompts for attributes.** Fill in all fields systematically:

**Required fields:**

- **point_id:** GCP identifier (GCP1, GCP2, GCP3, etc.)
  - Match numbering from annotated photo reference
  - Sequential numbering typically easiest (GCP1-GCP10)

- **description:** Clear description of GCP marker and location
  - Example: "Left bank, painted orange X on granite boulder, 8m upstream from camera"
  - Example: "Right bank, survey stake with orange flag at waterline"
  - Include enough detail to relocate GCP in future

- **marker_type:** Type of physical marker
  - "Painted rock - orange X"
  - "Painted rock - orange circle"
  - "Survey stake with flag"
  - "Natural feature - rock point"

- **visibility:** Visibility assessment from sample video review
  - "Clear" (GCP easily identifiable in video)
  - "Partial" (GCP visible but marginal - low contrast, edge of frame, partial obstruction)
  - "Obscured" (GCP difficult to identify in video - consider remarking or relocating)

**Surveyor and timestamp fields:**

- **surveyed_by:** Operator name or initials
- **survey_time:** Timestamp (typically auto-filled by SW Maps)

**Quality indicator fields (copy from GPS status):**

- **satellites:** Number of satellites tracked (e.g., 14)
- **pdop:** Position dilution of precision value (e.g., 1.8)
- **h_precision:** Horizontal precision estimate in cm (e.g., 1.5)
- **v_precision:** Vertical precision estimate in cm (e.g., 2.3)
- **fix_duration:** How long FIX maintained (≥10s for GCPs)
- **fix_type:** "RTK FIX" (or other solution type if quality degraded)

**Measurement fields:**

- **pole_height:** Height from pole tip (GCP marker) to antenna reference point (e.g., 2.15)
- **averaging_time:** Duration of averaging in seconds (60 or 120)

**Optional notes field:**

- **notes:** Additional observations or special conditions
  - "Stable rock surface, excellent GPS conditions"
  - "Partial tree cover, extended averaging to 120s"
  - "Water level at base of stake during survey"
  - "GCP may be submerged during high flows - resurvey if water level increases >50cm"

**Fill in all fields before saving point.** Complete attributes support quality control, troubleshooting, and future reference.

### Step 7: Save Point in SW Maps

**After all attributes filled:**

1. **Review coordinates and attributes one final time:**
   - Coordinates reasonable? (compare to previous GCP, check distance)
   - Pole height recorded correctly?
   - Point ID matches planned numbering?

2. **Save point** (button typically labeled "Save", "Done", or "Accept")

3. **Verify point saved successfully:**
   - Point appears on map at expected location
   - Attributes populated (tap point, view attribute table)
   - No error messages

**If save fails:**
- Check data connection or SW Maps storage
- Verify all required fields filled
- Retry save or export project immediately (preserves data)

### Step 8: Photograph GCP

**Documentation photos for each GCP:**

1. **Close-up photo showing marker clearly:**
   - Frame marker in center of photo
   - Include enough context to identify location (nearby rocks, vegetation, bank features)
   - Ensure marker visible and identifiable

2. **Context photo showing surroundings:**
   - Step back to show GCP in broader context
   - Include reference features (large rocks, trees, bank profile)
   - Helps relocate GCP in future

**Label photos with GCP number:**
- GCP1_closeup.jpg
- GCP1_context.jpg
- GCP2_closeup.jpg
- GCP2_context.jpg
- (etc.)

**Purpose of GCP photos:**
- Verify correct GCP surveyed (quality control)
- Document GCP marker condition (fresh paint, clear contrast)
- Support future GCP resurvey (relocation reference)
- Provide visual documentation for reports and training

### Step 9: Move to Next GCP

**Systematic progression:**
- Walk to next GCP in sequence (GCP2, GCP3, etc.)
- Maintain RTK FIX while moving (monitor status)
- Repeat Steps 1-8 for each GCP
- Survey all GCPs (typically 6-10 GCPs for OpenRiverCam deployment)

**Between GCPs:**
- Check base station periodically (if passing nearby)
- Monitor battery levels (rover and Android device)
- Take brief notes if observing issues or special conditions

---

## GCP Survey Quality Control

### Real-Time Quality Checks

**For each GCP, before saving, verify:**

- [ ] RTK FIX maintained throughout 60-120 second averaging
- [ ] All quality gates met (satellites ≥12, PDOP ≤2.5, H ≤2cm, V ≤3cm)
- [ ] Pole positioned precisely on marker center (checked and rechecked)
- [ ] Pole vertical throughout averaging (bubble centered continuously)
- [ ] Pole height measured and recorded (field notebook and SW Maps)
- [ ] All attributes filled in SW Maps (point_id, description, marker_type, visibility, quality indicators, pole_height)
- [ ] Coordinates reasonable (distance from previous GCP sensible, elevation plausible)
- [ ] Point saved successfully in SW Maps (appears on map, attributes populated)
- [ ] GCP photographed (close-up and context photos captured)

**Only save GCP after all quality checks pass.** Do not rush or compromise on GCP accuracy.

### GCP Distribution Quality Check

**After surveying all GCPs, verify distribution meets transformation requirements:**

**From Section 9.3 (GCP placement principles):**

- [ ] **Minimum 6 GCPs** (more is better, 8-10 typical)
- [ ] **Distributed across field of view:** Left/right spread, near/far depth spread
- [ ] **Vertical spread:** GCPs at different elevations (banks and near water level)
- [ ] **No clustering:** GCPs not all in one small area
- [ ] **No gaps:** No large areas of field of view lacking nearby GCPs

**View GCPs on map in SW Maps:**
- Do GCPs form reasonable distribution pattern?
- Are there obvious gaps or clusters?
- Does distribution cover monitoring area adequately?

**If distribution inadequate:**
- Add additional GCPs in sparse areas (extend survey to include more GCPs)
- Resurvey any GCPs with poor visibility or quality issues
- Adjust GCP locations if large gaps identified

**Good GCP distribution enables accurate transformation across entire field of view.** Poor distribution (e.g., all GCPs on one bank) degrades transformation accuracy in areas far from GCPs.

### Cross-Check Between GCPs

**Compare adjacent GCP measurements for consistency:**

**Example cross-check:**
```
GCP1: H_precision = 1.5cm, V_precision = 2.2cm, Satellites = 14, PDOP = 1.8
GCP2: H_precision = 1.8cm, V_precision = 2.5cm, Satellites = 13, PDOP = 1.9
GCP3: H_precision = 1.2cm, V_precision = 2.0cm, Satellites = 15, PDOP = 1.7

Quality indicators consistent across GCPs (good sign - indicates stable conditions)

GCP4: H_precision = 8.5cm, V_precision = 12.3cm, Satellites = 9, PDOP = 4.2
↑ RED FLAG: Quality much worse than other GCPs
Action: Resurvey GCP4 (may have been near obstruction, or FIX was marginal)
```

**Consistency checks validate survey quality.** If one GCP has significantly worse quality than others, resurvey that GCP.

---

## Common Issues and Solutions

### Issue: GCP not visible in sample video

**Symptoms:**
- Sample video shows GCP location, but marker not identifiable
- GCP obscured by vegetation, shadows, or glare
- GCP outside camera field of view or at extreme edge

**Solutions:**
- Adjust camera pan, tilt, or zoom to improve GCP visibility
- Move GCP marker to more visible location (adjust left/right, up/down, or closer/farther)
- Enhance marker contrast (repaint with brighter color, add flag, increase size)
- Remove obstructing vegetation (if appropriate and permissible)
- Capture new sample video after adjustments
- Only survey GCPs after confirming clear visibility in video

### Issue: Cannot achieve RTK FIX at GCP location

**Symptoms:**
- Solution remains Float or DGNSS at GCP location
- FIX intermittent (achieves FIX briefly, then loses it)
- Quality indicators poor (satellites <12, PDOP >3.0)

**Solutions:**
- **Wait 2-5 minutes:** Satellite geometry changes, may achieve FIX with time
- **Move GCP 2-3 meters:** Original location may have obstruction or multipath (tree overhang, reflective surface)
- **Check base station:** Verify base still operating (corrections still flowing, radio link active)
- **Return later:** Survey other GCPs first, return to problematic GCP after satellite constellation improves
- **Extend averaging time:** Use 120 seconds instead of 60 seconds if FIX marginal
- **Accept canal/relaxed quality gates:** If site inherently challenging, use relaxed thresholds (H ≤4cm, V ≤6cm)
- **Last resort:** Mark GCP as "poor quality" in notes, consider excluding from transformation if quality very poor

### Issue: Pole height measurement uncertain

**Symptoms:**
- Difficult to read tape measure (wind, awkward position, pole tall)
- Antenna reference point unclear (no mark visible)
- Operator not confident in measurement accuracy

**Solutions:**
- **Two-person measurement:** One person holds tape at pole tip, other reads at antenna (more reliable than solo measurement)
- **Multiple measurements:** Measure 2-3 times, take average if readings differ
- **Reference mark on pole:** Pre-mark pole at known intervals (every 10cm or 25cm) as reference for tape reading
- **Use antenna documentation:** Check antenna specifications for reference point location (typically bottom of antenna or phase center)
- **Photograph tape measure:** Take photo showing tape measure reading (backup documentation if field notebook lost or unclear)

### Issue: GCP numbering confusion

**Symptoms:**
- Uncertain which physical marker corresponds to which GCP number
- Multiple similar markers (e.g., three orange painted rocks in same area)
- Numbering sequence unclear from annotated photo

**Solutions:**
- **Use annotated photo systematically:** Refer to photo before each GCP survey, confirm marker appearance matches photo
- **Add physical number markers:** Temporarily label markers in field (e.g., write "1", "2", "3" near each marker with chalk or marker pen)
- **Update field notebook continuously:** Record description for each GCP immediately after surveying (prevents confusion)
- **If confused:** Stop and re-establish numbering scheme (better to spend 5 minutes clarifying than to have wrong GCP numbers in data)

### Issue: Water level changes during GCP survey

**Symptoms:**
- GCP near waterline is dry at start of survey, submerged by end
- Or vice versa: GCP submerged at start, exposed by end

**Solutions:**
- **Note water level change in field notebook:** Document time and magnitude of change
- **Resurvey affected GCPs if significant change (>10cm):** Water level change affects transformation reference plane
- **Prioritize near-water GCPs:** Survey waterline GCPs first before water level changes
- **Document flow conditions:** Note if flows increasing/decreasing during survey (affects water level stability)
- **Consider timing survey during stable water period:** Avoid surveying during rapid rise or fall if possible

---

## Time Estimates

**Sample video collection and GCP photography:**
- Connect to PtBox and access camera view: 5-10 minutes
- Frame field of view and adjust camera: 5-10 minutes
- Capture sample video and verify quality: 2-5 minutes
- Capture and annotate photo reference: 5-10 minutes
- **Subtotal: 15-30 minutes** (before GCP survey begins)

**GCP survey (per GCP):**
- Walk to GCP and position rover: 1-2 minutes
- Achieve FIX and verify quality gates: 1-2 minutes
- Averaging (60-120 seconds): 1-2 minutes
- Measure pole height: 30 seconds
- Fill in attributes in SW Maps: 1-2 minutes
- Photograph GCP: 1 minute
- **Per-GCP time: 5-8 minutes**

**Total GCP survey time (8 GCPs):**
- Sample video collection: 15-30 minutes
- Survey 8 GCPs: 40-65 minutes (8 × 5-8 minutes)
- Quality checks and cross-checks: 5-10 minutes
- **Total: 60-105 minutes (1-2 hours)** for complete GCP survey

**GCP survey is time investment,** but accuracy is critical. Rushing GCP survey risks poor transformation quality that degrades all subsequent velocity measurements.

---

## Connection to Transformation Configuration

**GCP survey data flows directly into PtBox transformation configuration:**

### Sample Video Provides Image Coordinates

**During PtBox configuration:**
- Load sample video in PtBox camera calibration tool
- Identify each GCP in video (refer to annotated photo reference)
- Click on each GCP marker in image to record pixel coordinates (u, v)
- Example: GCP1 at pixel (345, 678), GCP2 at pixel (456, 789), etc.

**Sample video establishes image-space coordinates for GCPs.**

### GCP Survey Provides Real-World Coordinates

**GCP coordinates from SW Maps export:**
- Load GCP coordinates from SW Maps CSV or Geopackage export
- Import into PtBox or transformation calculation tool
- Example: GCP1 at (E=685445.23, N=9456795.47, Z=142.15)

**GCP survey establishes real-world coordinates for GCPs.**

### Transformation Links Image to Real-World

**Homography calculation:**
- Input: GCP pixel coordinates (u, v) from sample video
- Input: GCP real-world coordinates (X, Y, Z) from survey
- Calculate transformation matrix (homography) mapping pixels to meters
- Apply transformation to every pixel in operational videos
- Result: Each pixel mapped to real-world coordinate (X, Y)

**GCP survey accuracy determines transformation accuracy.** If GCP survey has 2cm accuracy, transformation will have ~2cm accuracy. If GCP survey has 10cm accuracy, transformation will have ~10cm accuracy.

**This is why GCP survey requires highest accuracy of any measurement in the survey.**

---

## Summary: GCP Survey Process

**Sample video collection (Part 1):**
1. Connect to PtBox, put in Maintenance Mode
2. Access live camera view ("Aim the camera in the field")
3. Frame field of view, verify all GCPs visible
4. Capture 5-30 second sample video (note filename and timestamp)
5. Review video, confirm all GCPs clearly identifiable
6. Capture photo and annotate with GCP numbers (create reference)

**GCP survey (Part 2, for each GCP):**
1. Walk to GCP location, identify marker
2. Position rover pole precisely on marker center
3. Level pole (bubble centered, pole vertical)
4. Verify RTK FIX and all quality gates (satellites ≥12, PDOP ≤2.5, H ≤2cm, V ≤3cm)
5. Start averaging (60-120 seconds, keep pole stable and vertical)
6. Measure pole height (tip to antenna reference point)
7. Fill in all GCP attributes in SW Maps
8. Save point and verify saved successfully
9. Photograph GCP (close-up and context)
10. Move to next GCP and repeat

**Quality control throughout:**
- Confirm GCP visibility in sample video before surveying
- Verify all quality gates for every GCP before saving
- Cross-check quality indicators between GCPs (consistency)
- Verify GCP distribution meets transformation requirements (spread, no gaps)
- Photograph and document every GCP (supports quality assurance)

**Outcomes:**
- Sample video provides image coordinates for GCPs (pixel locations)
- GCP survey provides real-world coordinates to 2-3cm accuracy
- Combined data enables transformation calculation (image pixels → real-world meters)
- Complete GCP documentation supports PtBox configuration and future reference

**With GCP survey complete, you have the foundation for accurate coordinate transformation.** Next: Survey water level (Section 9.9) to document hydraulic conditions, then cross-section (Section 9.11) for discharge calculations.

---

**References:**
- SURVEY_PROCESS.md Section 5: Camera & Control Points
- SURVEY_PROCESS.md Appendix D: Sample Video Collection
- Section 9.3: Ground Control Point Placement (GCP planning)
- Section 9.6: Survey Execution - Process Overview (workflow context)
- Section 9.9: Survey Execution - Water Level (next step)
