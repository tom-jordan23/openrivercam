# 10.1 Configuring the PtBox - Orienting the Image

This section begins the critical process of configuring OpenRiverCam software to transform camera images into accurate discharge measurements. With survey data collected in Chapter 9, you now configure the PtBox to interpret video data correctly.

Image orientation is the first configuration step. The camera may be mounted at various angles, and the PtBox needs to know how the image is oriented relative to the river flow. Proper orientation ensures velocity vectors point in correct directions and coordinates align with surveyed ground control points.

Upon completion of this section, practitioners will possess the ability to access the PtBox web interface for configuration, load sample video collected during survey operations, assess current image orientation, apply rotation or flip transformations as required, verify that orientation matches field conditions, and save orientation configuration for operational deployment.

**Reference:** This connects directly to Section 9.8 (Sample Video Collection) and precedes Section 10.2 (Adding Control Points).

---

## Why Image Orientation Matters

### Understanding Camera Mounting Variations

**Cameras are mounted in various orientations depending on site constraints:**

**Standard upright mounting:**
- Camera mounted with top of image pointing up
- Left side of image is left bank (looking downstream)
- Right side of image is right bank
- Flow direction is downstream (typically toward bottom or middle of image)

**Rotated mounting:**
- Camera may be rotated 90°, 180°, or 270° from standard orientation
- Reasons: Mounting structure limitations, optimal field of view, camera housing design
- Example: Camera rotated 90° clockwise to maximize vertical coverage of tall banks

**Flipped or mirrored mounting:**
- Some camera installations require mounting behind protective glass or with lens orientation constraints
- Image may be horizontally flipped (left-right reversed) or vertically flipped

**Why software must know orientation:**

Without correct orientation configuration:
- Velocity vectors point in wrong directions
- GCP coordinates do not align with surveyed positions
- Discharge calculations use incorrect flow direction
- Spatial analysis fails (cannot distinguish left bank from right bank)

**Orientation configuration tells the PtBox:**
- Which direction is "up" in the real world
- Which direction is flow (downstream vs. upstream)
- How to align image coordinates with surveyed ground control points
- How to interpret tracked movements (positive X = downstream? positive Y = across river?)

---

## Accessing the PtBox Interface

### Prerequisites for Configuration

**Before beginning configuration, verify:**

- [ ] PtBox powered on and accessible via network
- [ ] Sample video collected during survey (Section 9.8)
- [ ] Sample video transferred to PtBox or accessible from configuration interface
- [ ] Configuration device (laptop or tablet) connected to PtBox network
- [ ] Survey data ready (GCP coordinates, cross-section data) for subsequent configuration steps

**Configuration typically occurs:**
- **After survey completion:** All field data collected, return to office or base
- **During site commissioning:** Survey team completes field work, technical team configures software
- **Remotely:** If PtBox accessible via internet, configuration can occur from distant location

### Connecting to PtBox Web Interface

**Access procedure:**

1. **Ensure PtBox is powered and network-accessible:**
   - If local installation: Connect laptop to PtBox WiFi network or local area network
   - If remote access: Verify VPN or internet connection to PtBox
   - Typical network configurations: Direct WiFi connection, Ethernet connection, or cellular data link

2. **Open web browser on configuration device:**
   - Recommended browsers: Chrome, Firefox, or Edge (modern versions)
   - Avoid older browsers (may not support interface features)

3. **Navigate to PtBox IP address:**
   - Example URL: `http://192.168.1.100:8080` (IP and port vary by installation)
   - IP address should be documented during installation (Section 8)
   - If IP unknown: Check PtBox documentation or contact system administrator

4. **Enter credentials:**
   - Username and password provided during installation
   - Default credentials should have been changed during commissioning (security best practice)
   - If credentials forgotten: May require physical access to PtBox for reset

5. **Access configuration interface:**
   - Navigate to "Configuration" or "Camera Setup" section
   - Interface typically organized in tabs or menu sections:
     - Camera settings
     - Calibration
     - Ground control points
     - Cross-sections
     - Server connection
     - Automation settings

**Troubleshooting connection issues:**

**Cannot reach PtBox IP address:**
- Verify laptop connected to correct network
- Ping PtBox IP to test connectivity: `ping 192.168.1.100`
- Check firewall settings (may block connection)
- Verify PtBox powered on (status lights visible if physical access available)

**Credentials not accepted:**
- Verify username and password spelling (case-sensitive)
- Check for extra spaces before/after username or password
- Contact system administrator for credential reset

**Interface loads but appears broken:**
- Try different web browser
- Clear browser cache and reload
- Check browser console for error messages (press F12, view Console tab)
- Verify PtBox software version compatible with browser

---

## Loading Sample Video

### Locating Sample Video File

**Sample video collected during survey (Section 9.8):**

**From field notes, identify:**
- **Video filename:** e.g., `test_video_20241115_1045.mp4`
- **Timestamp:** Date and time of capture
- **Water level at capture:** Documented in Section 9.9 survey data
- **Flow conditions:** Notes about river conditions during video capture

**Video should already be on PtBox:**
- If video captured directly by PtBox camera: Video stored in PtBox file system
- If video captured by external device: Video must be uploaded to PtBox via interface or file transfer

### Uploading Video (If Needed)

**If sample video not yet on PtBox:**

1. **Navigate to video upload interface:**
   - Configuration section → Sample Videos → Upload
   - Or Files → Video Upload

2. **Select video file from local device:**
   - Browse to video file location on laptop
   - Typical location: Survey data folder → Videos → sample_video_20241115.mp4

3. **Upload video:**
   - Click "Upload" or drag-and-drop video file to upload area
   - Monitor upload progress (may take 1-5 minutes depending on video size and network speed)
   - Verify upload successful (video appears in list of available videos)

**Video file requirements:**
- **Format:** MP4, AVI, or other standard video formats
- **Resolution:** Match camera capture resolution (e.g., 1920×1080 or 1280×720)
- **Duration:** 5-30 seconds (short clips adequate for configuration)
- **Content:** All GCPs visible, water surface visible, stable image (camera not moving during capture)

### Loading Video for Orientation Check

**In configuration interface:**

1. **Navigate to Camera Calibration or Orientation section**

2. **Select sample video from dropdown list:**
   - Videos listed by filename or timestamp
   - Select the video captured during survey: `test_video_20241115_1045.mp4`

3. **Load video:**
   - Click "Load Video" or "Preview"
   - Video preview appears in configuration interface
   - Video may display as still frame (first frame of video) or playable clip

4. **Verify correct video loaded:**
   - Check that video shows expected river scene
   - Confirm GCPs visible (refer to annotated photo from Section 9.8)
   - Verify water surface visible and image quality adequate

**If wrong video loaded or video not displaying:**
- Reselect video from dropdown
- Verify video file not corrupted (try playing video in external media player)
- Check browser console for error messages
- Refresh page and reload video

---

## Assessing Current Image Orientation

### Visual Inspection of Loaded Video

**With sample video displayed in interface:**

**Check these orientation indicators:**

**Flow direction:**
- Identify flow direction in image: Which way is water moving?
- Compare with field notes: Flow should be downstream (typically left-to-right or top-to-bottom in standard view)
- If flow appears to move upstream or sideways, orientation may be incorrect

**Bank orientation:**
- Identify left bank and right bank in image
- Verify left bank is on left side of image, right bank on right side (looking downstream)
- If banks reversed, image may be horizontally flipped

**Vertical orientation:**
- Sky or banks should appear at top of image
- Water surface should appear in lower/middle portion
- If image appears upside-down, 180° rotation needed

**Reference features:**
- Locate known features from survey: GCP markers, survey stakes, visible landmarks
- Compare positions in image with annotated photo from Section 9.8
- Positions should match (same left-right, up-down relationships)

### Comparing with Field Annotations

**Use annotated GCP photo from Section 9.8 as reference:**

**Photo shows GCP numbering and positions:**
- GCP1: Left bank, near top of image
- GCP2: Left bank, mid-height
- GCP3: Mid-channel, lower portion
- GCP4: Right bank, mid-height
- (etc., depending on GCP layout)

**Compare photo positions with loaded video:**
- Do GCPs appear in same relative positions?
- Is GCP1 in upper-left corner of both photo and loaded video?
- Is GCP4 in right-center area of both?

**If positions do not match:**
- Image orientation likely incorrect
- Determine what rotation or flip would align loaded video with annotated photo

**Common mismatches and required corrections:**

| Observed Problem | Required Correction |
|-----------------|---------------------|
| Image upside-down | Rotate 180° |
| Image rotated 90° clockwise | Rotate 90° counterclockwise |
| Image rotated 90° counterclockwise | Rotate 90° clockwise |
| Left-right reversed | Horizontal flip |
| Top-bottom reversed | Vertical flip (less common) |

### Verifying Flow Direction

**Critical check: Ensure flow direction correct**

**Play video (if playable preview available):**
- Observe water surface features moving
- Foam, waves, or debris should move downstream
- Downstream typically flows:
  - Left to right (standard orientation)
  - Top to bottom (some installations)
  - Diagonal (if river bends in field of view)

**From field notes:**
- Flow direction documented during survey
- Compare observed flow in video with expected flow from notes
- If flow appears opposite, image may be flipped or rotated 180°

**Why flow direction matters:**
- Velocity vectors calculated from movement direction
- If image orientation wrong, velocities will have incorrect sign (upstream vs. downstream)
- Discharge calculations require correct flow direction for cross-section integration

---

## Applying Orientation Corrections

### Using Interface Orientation Controls

**Most PtBox interfaces provide orientation adjustment controls:**

**Rotation controls:**
- Buttons or dropdown for rotation: "Rotate 90° CW", "Rotate 90° CCW", "Rotate 180°"
- Apply rotation incrementally until image oriented correctly
- Preview updates after each rotation applied

**Flip controls:**
- "Flip Horizontal" (mirror left-right)
- "Flip Vertical" (mirror top-bottom)
- Use if image reversed but rotation alone does not correct orientation

### Step-by-Step Correction Procedure

**If rotation needed:**

1. **Assess required rotation angle:**
   - Compare current orientation with desired standard orientation
   - Determine rotation direction and angle (90° CW, 90° CCW, or 180°)

2. **Apply rotation:**
   - Click rotation button (e.g., "Rotate 90° CW")
   - Image preview updates with rotation applied
   - Visual inspection: Does orientation now match expected view?

3. **Verify after rotation:**
   - Check flow direction (downstream flowing correct direction?)
   - Check bank positions (left bank on left, right bank on right?)
   - Check GCP positions (match annotated photo?)

4. **Apply additional rotation if needed:**
   - If first rotation insufficient, apply additional rotation
   - Example: Image was 180° incorrect, apply "Rotate 180°" once or "Rotate 90° CW" twice

**If flip needed:**

1. **Identify flip type:**
   - Horizontal flip: Left-right reversal (left bank appears on right side of image)
   - Vertical flip: Top-bottom reversal (sky appears at bottom of image - rare)

2. **Apply flip:**
   - Click "Flip Horizontal" or "Flip Vertical" button
   - Image preview updates with flip applied

3. **Verify after flip:**
   - GCP positions now match annotated photo?
   - Flow direction correct?
   - Banks correctly positioned?

**Combining rotation and flip:**
- Some orientations require both rotation and flip
- Apply rotation first, then flip (or vice versa, depending on interface logic)
- Example: Image rotated 90° CW and horizontally flipped
- Experiment with combination until orientation correct

### Common Orientation Scenarios

**Scenario 1: Camera mounted upside-down**
- **Symptoms:** Sky at bottom of image, water at top, banks inverted
- **Correction:** Rotate 180°
- **Result:** Image now right-side up, sky at top, water at bottom

**Scenario 2: Camera rotated 90° for vertical field of view**
- **Symptoms:** River appears to flow vertically in image instead of horizontally
- **Correction:** Rotate 90° CW or CCW to align flow horizontally
- **Result:** Flow now horizontal (left-to-right or right-to-left)

**Scenario 3: Camera behind mirror or reversed optics**
- **Symptoms:** Left bank on right side of image, right bank on left side (mirrored)
- **Correction:** Flip horizontal
- **Result:** Banks now correctly positioned (left bank on left, right bank on right)

**Scenario 4: Camera rotated and flipped**
- **Symptoms:** Both rotation and left-right reversal
- **Correction:** Apply rotation first (e.g., 90° CW), then flip horizontal
- **Result:** Image oriented correctly after combined transformations

---

## Verifying Orientation Configuration

### Final Orientation Checks

**Before saving orientation configuration, verify all criteria met:**

**Flow direction check:**
- [ ] Play video or observe water surface movement
- [ ] Confirm flow moves downstream (correct direction per field notes)
- [ ] Velocity vectors will point downstream when tracking enabled

**Bank position check:**
- [ ] Left bank (looking downstream) appears on left side of image
- [ ] Right bank appears on right side of image
- [ ] Bank positions match field observations

**GCP position check:**
- [ ] Compare loaded video with annotated GCP photo (Section 9.8)
- [ ] Each GCP appears in same relative position in video as in photo
- [ ] GCP numbering sequence matches (GCP1, GCP2, GCP3, etc., in correct spatial arrangement)

**Vertical alignment check:**
- [ ] Sky or banks at top of image
- [ ] Water surface in middle or lower portion of image
- [ ] Image not upside-down or inverted

**Reference feature check:**
- [ ] Known landmarks visible in expected positions
- [ ] Survey stakes, painted rocks, or other markers appear where expected based on field notes

**If any check fails:**
- Return to orientation controls
- Apply additional rotation or flip corrections
- Repeat verification checks until all criteria met

### Test with GCP Overlay (If Available)

**Some interfaces allow GCP position preview:**

**If interface supports GCP overlay:**
1. **Load surveyed GCP coordinates** (from Section 9.8 survey data)
2. **Enable GCP overlay on video preview**
3. **Assess alignment:**
   - Software projects GCP positions onto image based on current orientation
   - GCP markers should overlay approximately on visible GCP features in video
   - If overlay misaligned, orientation likely incorrect

**Note:** Precise GCP alignment occurs in Section 10.2 (Adding Control Points). At this stage, rough alignment sufficient to confirm orientation reasonable.

**If GCP overlay severely misaligned:**
- Orientation incorrect: Reapply rotation or flip corrections
- Or GCP coordinates incorrect: Verify surveyed coordinates loaded correctly

**If GCP overlay roughly aligned:**
- Orientation likely correct
- Proceed to save configuration

---

## Saving Orientation Configuration

### Applying and Persisting Settings

**Once orientation verified:**

1. **Save orientation configuration:**
   - Click "Save", "Apply", or "Accept" button in interface
   - PtBox stores orientation parameters for use in all subsequent processing

2. **Verify save successful:**
   - Interface confirms "Configuration saved" or displays success message
   - Reload video or refresh preview: Orientation should persist (not revert to original)

3. **Document configuration:**
   - Record orientation settings in field notes or configuration log
   - Example: "Image rotated 90° clockwise, no flip applied"
   - Include date, operator name, and configuration session ID if applicable

### Configuration Parameters Saved

**Orientation configuration typically includes:**

**Rotation parameter:**
- Rotation angle: 0°, 90°, 180°, or 270°
- Stored as integer or enumeration (e.g., rotation = 90)

**Flip parameters:**
- Horizontal flip: True or False
- Vertical flip: True or False
- Stored as boolean flags

**Application scope:**
- Orientation applies to all videos processed by this PtBox
- Sample video, operational videos, and future videos all use same orientation
- If camera physically moved or re-mounted, orientation configuration must be updated

### Next Configuration Steps

**With orientation configured, proceed to:**

**Section 10.2: Adding Control Points (next step):**
- Load surveyed GCP coordinates
- Identify each GCP in sample video image
- Calculate coordinate transformation (homography)
- Verify reprojection error

**Subsequent sections:**
- Section 10.3: Adding cross-sections
- Section 10.4: Server integration
- Section 10.5: Automated collection and upload

**Do not skip orientation configuration:**
- All subsequent configuration depends on correct orientation
- Incorrect orientation will cause GCP alignment failures in Section 10.2
- Correcting orientation later requires reconfiguring GCPs and cross-sections

---

## Common Issues and Solutions

### Issue: Cannot determine correct orientation

**Symptoms:**
- Multiple orientations seem reasonable
- Uncertain which rotation or flip to apply
- No obvious "correct" orientation

**Solutions:**
- **Refer to annotated GCP photo:** This is definitive reference for correct orientation
- **Compare with field notes:** Sketch or description of camera view recorded during survey
- **Use known features:** Identify permanent landmarks (bridges, buildings, specific trees) and verify positions match field observations
- **Contact survey team:** If configuring remotely, ask field team to confirm flow direction and bank orientation

### Issue: Orientation looks correct but GCP overlay fails

**Symptoms:**
- Video appears correctly oriented (flow downstream, banks correct)
- When loading GCP overlay, positions severely misaligned
- GCPs appear far from expected locations

**Solutions:**
- **Verify GCP coordinates loaded correctly:** Check that surveyed X, Y, Z coordinates imported without errors
- **Check coordinate system:** GCP coordinates must be in correct coordinate reference system (CRS) matching PtBox configuration
- **Confirm GCP numbering:** GCP1 in coordinates should match GCP1 in video
- **Orientation may be subtle:** Try alternative rotation or flip (e.g., 180° rotation changes flow direction but banks stay same)

### Issue: Video preview does not update after applying orientation

**Symptoms:**
- Click rotation or flip buttons but image does not change
- Or changes temporarily then reverts

**Solutions:**
- **Refresh browser page:** Sometimes browser cache causes display issues
- **Clear browser cache:** Hard refresh (Ctrl+Shift+R or Cmd+Shift+R)
- **Try different browser:** Switch from Chrome to Firefox or vice versa
- **Check interface logs:** View browser console (F12) for error messages indicating software bug
- **Contact technical support:** May be software issue requiring PtBox update

### Issue: Orientation correct for GCPs but flow direction reversed

**Symptoms:**
- GCP positions align correctly with surveyed locations
- But flow appears to move upstream instead of downstream
- Or velocity vectors point opposite direction

**Solutions:**
- **This may be acceptable:** Some installations have flow direction configured separately from image orientation
- **Check flow direction parameter:** Look for separate "Flow Direction" setting in interface
- **Apply 180° rotation:** If necessary to reverse flow direction without affecting GCP alignment
- **Verify during velocity calibration:** Flow direction can be validated in Section 10.5 when observing real-time velocity measurements

---

## Time Estimates

**Typical time for image orientation configuration:**

**First-time configuration (learning interface):**
- Access PtBox interface: 5 minutes
- Load sample video: 2-5 minutes
- Assess orientation and determine corrections: 5-10 minutes
- Apply and verify orientation: 5-10 minutes
- Save and document: 2 minutes
- **Total: 20-30 minutes**

**Experienced user (familiar with interface):**
- Access and load video: 2-3 minutes
- Determine and apply corrections: 3-5 minutes
- Verify and save: 2 minutes
- **Total: 7-10 minutes**

**Troubleshooting scenarios:**
- If orientation unclear or multiple attempts needed: Add 10-20 minutes
- If technical issues with interface: Add 15-30 minutes
- If coordinating with remote survey team: Add 15-30 minutes for communication

**Orientation is typically quick configuration step** compared to subsequent steps (GCPs and cross-sections are more time-intensive).

---

## Connection to Transformation Process

### How Orientation Affects Coordinate Transformation

**From Chapter 4 (Imaging Concepts):**

**Coordinate transformation converts pixel coordinates to real-world coordinates:**
- Pixel position (u, v) in image → Real-world position (X, Y, Z) in meters
- Transformation depends on knowing image orientation relative to real-world coordinate system

**Orientation configuration establishes:**

**Axis alignment:**
- Which image axis (horizontal or vertical pixels) corresponds to which real-world axis (downstream, across river, elevation)
- Example: If image rotated 90°, image horizontal axis may correspond to river cross-stream direction instead of downstream direction

**Coordinate sign conventions:**
- Does positive X in image correspond to positive X in real world, or negative X?
- Flipping image changes sign conventions

**Flow direction interpretation:**
- Velocity vectors calculated from pixel displacement (movement in image)
- Velocity vectors must be oriented correctly in real-world space
- Incorrect orientation causes velocity vectors to point wrong direction (upstream vs. downstream, or left vs. right)

**Orientation is applied before transformation calculation:**
1. Load sample video
2. Apply orientation correction (rotation/flip) → Corrected image
3. Identify GCPs in corrected image → Pixel coordinates
4. Match with surveyed GCP coordinates → Real-world coordinates
5. Calculate transformation from corrected pixel coordinates to real-world coordinates

**If orientation wrong:**
- GCP pixel coordinates measured in incorrectly-oriented image
- Transformation will be incorrect or fail entirely
- Velocity vectors point wrong directions
- Discharge calculations use wrong flow direction

**This is why orientation is first configuration step** - all subsequent configuration depends on correct orientation.

---

## Summary: Image Orientation Configuration

**Purpose:**
- Ensure camera image correctly oriented relative to real-world coordinate system
- Align image axes with surveyed ground control points
- Establish correct flow direction for velocity calculations

**Key steps:**
1. Access PtBox web interface for configuration
2. Load sample video collected during survey (Section 9.8)
3. Assess current orientation (compare with annotated GCP photo)
4. Apply rotation and/or flip corrections as needed
5. Verify orientation (flow direction, bank positions, GCP alignment)
6. Save orientation configuration

**Quality checks:**
- Flow moves downstream (correct direction per field notes)
- Left bank on left side of image, right bank on right side
- GCP positions match annotated photo from survey
- Vertical alignment correct (sky at top, water at bottom)

**Common corrections:**
- Rotate 90° CW, 90° CCW, or 180° for rotated camera mounts
- Flip horizontal for mirrored or reversed camera optics
- Combine rotation and flip for complex mounting orientations

**Critical success factor:**
- Orientation must be correct before proceeding to GCP configuration (Section 10.2)
- Incorrect orientation causes GCP alignment failures
- All subsequent configuration depends on correct orientation foundation

**Next step:**
With image properly oriented, proceed to Section 10.2: Adding Control Points to establish the coordinate transformation.

---

**References:**
- Section 9.8: Survey Execution - Control Points and Sample Video (sample video collection)
- Section 4.1: Pixel to Physical Transformation (coordinate systems and transformation concepts)
- Section 10.2: Adding Control Points (next configuration step)
