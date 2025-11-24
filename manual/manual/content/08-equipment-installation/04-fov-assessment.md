# 8.4 Assessing the Camera Scene and Marking FOV

## Overview

After installing the camera, it is critical to verify that the field of view (FOV) covers the required area for water level measurement and surface velocity monitoring (Muste et al., 2008). This section describes procedures for capturing test images, assessing FOV coverage, physically marking FOV boundaries in the field, and verifying staff gauge visibility. Proper FOV assessment ensures accurate measurements and helps field teams understand the camera's viewing area. The time required for this procedure is approximately 2-3 hours.

The following prerequisites must be met before beginning FOV assessment. First, the camera must be installed and powered as described in Section 8.3. Network connectivity to the camera must be established, and the camera must be aimed at the target area. The staff gauge must be installed and visible within the camera's field of view. Finally, safe access to the river or stream bank must be available for field personnel to conduct the assessment work.

## Safety Considerations

Field personnel conducting FOV assessment work must observe critical safety protocols when working near water bodies (ISO, 2019). Working near water presents significant drowning risk, particularly on unstable banks or when working close to the water's edge. Personnel must wear life jackets or personal flotation devices during all activities near water. River banks and wet rocks present slippery surfaces that require appropriate non-slip footwear with good traction.

Flash flood risk requires constant awareness of upstream weather and flow conditions. Field personnel must cease work immediately if water levels rise unexpectedly or if weather conditions deteriorate. The camera system is electrically powered, creating electrical hazards that require personnel to avoid contact with electrical components. Local wildlife and vegetation hazards, including snakes, insects, and poisonous plants, necessitate appropriate precautions and awareness.

Personal protective equipment (PPE) requirements include life jackets or personal flotation devices when working near water, non-slip footwear such as water shoes or boots, and long pants and sleeves for protection from vegetation. Personnel should wear hats and sunscreen for sun protection, apply insect repellent as applicable to local conditions, and ensure first aid kits are accessible at all times during field operations.

## Equipment and Tools Checklist

Field personnel must assemble comprehensive equipment before beginning FOV assessment activities. Computer equipment requirements include a laptop or tablet with network capability, network cables for wired camera connections, and portable WiFi routers if the camera has wireless capability. Personnel should bring power banks or extra batteries for laptop computers, USB drives for storing test images, and appropriate camera configuration software or web browsers for accessing camera interfaces.

Field marking equipment comprises survey flags or stakes in bright colors (minimum 10 units), flagging tape in highly visible colors such as orange, pink, or yellow, and measuring tapes ranging from 30 to 50 meters in length. Range finders or laser distance meters enable accurate distance measurement. Permanent markers, optional spray paint for semi-permanent marking, whiteboards or marking boards for creating reference markers, camera tripods for ground-level photography, and smartphones or cameras for documentation complete the field marking toolkit.

Documentation materials include field notebooks and pencils, site maps or sketches, clipboards, cameras or smartphones for photographs, GPS units or GPS-enabled smartphones, and standardized forms for recording FOV coordinates (Wheaton et al., 2010). Safety and utility equipment comprises life jackets, first aid kits, water and snacks, sun protection items, communication devices such as radios or phones, and rope for accessing difficult areas.

## Step 1: Initial Test Image Capture

### 1.1 Access Camera Live View

Personnel must first establish connection to the camera system to access the live view interface. The operator connects the laptop to the camera network, opens a web browser, and navigates to the camera's IP address. After logging in with the credentials configured in Section 8.3, the operator navigates to the live view page to begin image assessment.

Camera operation verification requires the operator to confirm that the live video stream displays correctly and that image quality is acceptable for monitoring purposes. The frame rate must be smooth without significant lag or stuttering. The operator should check for any error messages or warnings that might indicate system problems.

Display optimization involves maximizing the browser window for optimal viewing, disabling any overlays or on-screen information that obscure the view, ensuring adequate display refresh rate, and adjusting browser zoom as needed to examine details clearly. Quality checks confirm that the live stream is clear and stable, the full image frame is visible on screen without cropping, no error messages appear, and the staff gauge is visible within the image frame.

### 1.2 Capture Reference Images

Reference image capture creates baseline images under current conditions for comprehensive assessment (Perks et al., 2016). The operator captures images at the current water level by taking snapshots or saving frames from the live stream. Images should be saved with descriptive filenames following the recommended format YYYY-MM-DD_HHMM_baseline.jpg, and the operator must record the current water level reading from the gauge in the field notes.

Documentation of current conditions includes recording the time of capture, weather conditions, lighting conditions, water surface conditions such as calm, ripples, or waves, and any obstructions or issues visible in the image. Multiple image capture involves taking images at 5-10 minute intervals, capturing at least 5 images for thorough assessment, varying lighting conditions when possible to test camera performance under different scenarios, and noting any changes in image quality that occur with changing environmental conditions.

Image storage procedures require the operator to store images on the laptop, copy files to USB drives for backup, include images in installation documentation, and upload to project folders when remote access is available. This redundant storage approach ensures data preservation and accessibility for analysis and documentation purposes.

### 1.3 Assess Image Quality

**Image Quality Assessment:**

Image quality assessment begins with clarity and focus verification. Operators must confirm that staff gauge markings appear sharp and readable in captured images, with gauge numbers legible at full resolution. Water surface texture must be visible to enable velocity tracking, and background features should demonstrate adequate sharpness (Muste et al., 2008). Exposure and lighting conditions require careful evaluation to ensure the image is neither overexposed with blown out highlights nor underexposed with lost shadow detail. Adequate contrast between the gauge and background must exist, with no significant glare or reflections obscuring gauge visibility.

Field of view coverage assessment verifies that the entire staff gauge remains visible, including both the highest and lowest marks. Adequate margins above and below the gauge must exist to accommodate water level variation. Sufficient horizontal coverage for surface velocity measurement is essential, and the image should show no vignetting or dark corners that would limit usable area (Perks et al., 2016).

Operators must document any quality issues identified during assessment. Areas of poor visibility, reflections or glare, obstructions from vegetation or debris, perspective distortion, and any other quality concerns require documentation for future reference and troubleshooting. When image quality issues are identified, operators should adjust camera settings including exposure and focus, reposition the camera if necessary, address physical obstructions, install or adjust sunshades, and refer to troubleshooting procedures detailed in Section 8.3.

## Step 2: Field of View Boundary Determination

### 2.1 Understand Field of View Geometry

Field of view (FOV) represents the area visible to the camera, defined by horizontal and vertical angles determined by lens focal length and sensor size (Hauet et al., 2008). Wider angle lenses produce larger FOV coverage, while telephoto lenses create smaller, more focused FOV areas. Understanding FOV geometry is essential for accurate spatial measurement and monitoring coverage assessment.

FOV calculations at a given distance D follow standard geometric relationships. Horizontal FOV width equals 2 × D × tan(horizontal_angle / 2), while vertical FOV height equals 2 × D × tan(vertical_angle / 2). For example, a camera with 60° horizontal FOV positioned 15 meters from the river produces horizontal coverage of 2 × 15 × tan(30°) = 17.3 meters.

Personnel must recognize that actual FOV varies with distance from the camera. Objects closer to the camera occupy more pixels than distant objects, affecting measurement resolution and accuracy across the monitored area. This geometric relationship influences the placement of ground control points and the interpretation of velocity measurements derived from image analysis.

### 2.2 Determine FOV Extent on Water Surface

**Reference Information:**
- Camera height above water: _____ meters
- Distance to near edge of desired FOV: _____ meters
- Distance to far edge of desired FOV: _____ meters
- Camera horizontal FOV angle: _____ degrees (from camera specifications)
- Camera vertical FOV angle: _____ degrees

**Method 1: Using Live View and Helper in Field**

**Procedure:**

1. **Position Helper at Various Locations:**
   - One person observes camera live view on laptop
   - Second person walks along river carrying bright flag or marker board
   - Observer directs helper to edge of visible area via radio or phone

2. **Mark Corner Points:**
   - Start with upstream-left corner of desired FOV
   - Helper moves until at edge of camera view
   - Observer confirms position visible in camera
   - Helper places survey flag at that location
   - Record GPS coordinates: _____

3. **Repeat for All Corners:**
   - Upstream-right corner
   - Downstream-right corner
   - Downstream-left corner
   - Mark each with survey flag

4. **Mark Intermediate Points:**
   - Place additional flags along FOV boundaries
   - Every 5-10 meters depending on site size
   - Helps visualize FOV extent

**Method 2: Using Calculated Distances**

**Procedure:**

1. **Calculate FOV Width at Water Surface:**
   - Measure distance from camera to water surface (perpendicular distance)
   - Use camera FOV angle specifications
   - Calculate width: W = 2 × D × tan(horizontal_angle / 2)
   - Example: Distance 15m, FOV 60° → Width = 17.3m

2. **Mark Calculated Distances:**
   - Use measuring tape or range finder
   - Measure from reference point (e.g., directly below camera)
   - Mark calculated FOV boundaries
   - Verify with camera live view

3. **Adjust for Camera Tilt:**
   - Camera typically aimed downward
   - Near edge of FOV is closer to camera than far edge
   - FOV coverage is wider at far edge than near edge
   - Account for this when marking boundaries

**Quality Check:**
- All corner points marked clearly
- Markers are visible from camera position
- Markers are secure and will not wash away
- GPS coordinates recorded for all points

### 2.3 Verify FOV Coverage Requirements

**Coverage Checklist:**

**Staff Gauge Coverage:**
- [ ] Entire staff gauge visible in frame
- [ ] Gauge positioned in central area of image (not at extreme edge)
- [ ] Adequate margin above highest gauge mark (minimum 0.5m)
- [ ] Adequate margin below lowest gauge mark (minimum 0.5m)

**Velocity Measurement Area:**
- [ ] Sufficient upstream-to-downstream coverage for particle tracking
- [ ] Minimum 5-10 meters of river length visible
- [ ] Water surface texture visible throughout area
- [ ] No obstructions within measurement area

**Reference Points:**
- [ ] Fixed reference points visible (bridge, bank features, structures)
- [ ] At least 3-4 ground control points visible for georeferencing
- [ ] Reference points distributed throughout frame

**If Coverage is Insufficient:**
- Adjust camera aim to increase coverage
- Consider changing lens (wider angle if available)
- Reposition camera if necessary
- Update site plan to reflect actual coverage

## Step 3: Physical FOV Marking

### 3.1 Install Permanent FOV Markers

**Purpose:** Physical markers help field teams understand camera coverage and assist in maintenance and troubleshooting.

**Marker Types:**

Physical markers for FOV demarcation fall into three categories based on longevity and installation method. Survey flags provide temporary marking suitable for initial assessment, utilizing bright colors visible in camera images with the advantage of easy repositioning. These temporary markers should be replaced with more permanent installations once FOV boundaries are finalized (Wheaton et al., 2010).

Semi-permanent painted markers employ spray paint applied to rocks or other fixed natural features. Bright colors including orange, yellow, or pink ensure visibility, and markers should be labeled with "CAMERA FOV" or similar identification. Paint-based markers require periodic refreshing as weathering causes fading over time.

Permanent installed markers provide the most durable FOV demarcation. These include bright fabric flags mounted on poles, PVC pipes painted in bright colors, metal or wooden stakes driven into the ground, and concrete markers for maximum permanence. Permanent markers offer long-term reliability but require more substantial installation effort (ISO, 2019).

**Procedure:**

1. **Select Marker Locations:**
   - All four corners of FOV at water surface
   - Intermediate points along FOV boundaries
   - Additional markers at key features (gauge, measurement area)

2. **Install Corner Markers:**
   - Dig hole or drive stake into ground
   - Install marker pole or stake (minimum 1-1.5m height)
   - Attach bright flag or paint marker
   - Ensure marker is vertical and secure
   - Label marker: "CAM FOV - NW CORNER" (for example)

3. **Install Intermediate Markers:**
   - Every 5-10 meters along FOV boundaries
   - Similar installation to corner markers
   - Can use shorter stakes for intermediate markers
   - Ensure visible from camera

4. **Document Marker Locations:**
   - Record GPS coordinates of each marker
   - Photograph each marker
   - Create map showing marker positions
   - Note marker IDs in site documentation

**Quality Check:**
- All markers installed securely
- Markers clearly visible in camera image
- Markers will withstand weather and minor floods
- Marker locations documented

### 3.2 Mark Staff Gauge Coverage Area

**Purpose:** Clearly identify which portion of staff gauge is visible to camera.

**Procedure:**

1. **Verify Gauge Visibility:**
   - View live camera image
   - Identify highest gauge marking visible: _____ m
   - Identify lowest gauge marking visible: _____ m
   - Note any partially visible markings

2. **Mark Visible Range on Gauge:**
   - Use bright flagging tape or paint
   - Mark top of camera-visible area on gauge
   - Mark bottom of camera-visible area
   - Label: "CAMERA VISIBLE ABOVE/BELOW THIS MARK"

3. **Document Coverage:**
   - Record visible range in installation documentation
   - Photograph gauge showing visible range
   - Note range in site logbook

**If Gauge Coverage Insufficient:**
- Adjust camera tilt to increase vertical coverage
- Reposition camera if necessary
- Install additional gauge sections if required
- Update site plan

## Step 4: Ground Control Point Establishment

### 4.1 Select Ground Control Points (GCPs)

**Purpose:** GCPs are fixed reference points used for georeferencing images and calculating real-world measurements from image coordinates.

**GCP Requirements:**

Effective ground control points must satisfy several critical criteria to ensure measurement accuracy and reliability. GCPs must occupy fixed locations that do not move or change over time, remaining clearly identifiable in all captured images (Muste et al., 2008). Spatial distribution throughout the FOV is essential, with points accessible for surveying using appropriate equipment. Features selected as GCPs should be permanent or semi-permanent in nature to provide consistent reference across the monitoring period (Hauet et al., 2008).

Suitable GCP examples include painted marks on stable rock outcrops, corners of concrete structures exhibiting no movement, bridge abutments or piers fixed in position, permanent survey markers installed for geodetic purposes, corners of buildings within the camera view, and fixed fence posts or poles securely anchored. These features provide reliable, unchanging reference points for georeferencing calculations.

Unsuitable GCP examples must be avoided as they compromise measurement accuracy. Vegetation grows and moves with wind and seasonal changes, rendering it unsuitable. Debris or temporary objects may be removed or relocated. Moving water features by definition lack the fixity required for ground control. Areas prone to erosion may shift position over time, and any items that may be intentionally or accidentally removed fail to provide the permanence necessary for long-term monitoring applications (Perks et al., 2016).

**Procedure:**

1. **Identify Potential GCPs:**
   - Survey site for suitable fixed features
   - Look for features distributed across FOV
   - Verify features are stable and permanent
   - Minimum 4 GCPs recommended, 6-10 preferred

2. **Mark or Enhance GCPs:**
   - If using natural features, enhance visibility:
     - Paint bright marker on rock
     - Install reflective target
     - Create painted target pattern (circle or cross)
   - Ensure marker is clearly visible in camera image

3. **Document GCPs:**
   - Assign ID number to each GCP (GCP-01, GCP-02, etc.)
   - Photograph each GCP from camera view
   - Photograph each GCP from ground level
   - Record description of each GCP location

### 4.2 Survey Ground Control Points

**Methods for Determining GCP Coordinates:**

**Method 1: RTK GNSS Survey (Most Accurate)**
- Use RTK GPS equipment
- Achieve centimeter-level accuracy
- Record X, Y, Z coordinates in appropriate coordinate system
- Required accuracy: ±0.05m or better

**Method 2: Standard GNSS (GPS)**
- Use standard GPS unit or smartphone
- Accuracy typically ±3-5 meters
- Less expensive but lower accuracy
- Sufficient for many applications

**Method 3: Total Station Survey**
- Use surveying total station
- High accuracy (millimeter level)
- Requires survey expertise
- Best for precise applications

**Method 4: Photogrammetry from Known Points**
- Use known reference points to determine other points
- Requires specialized software
- Good for relative positioning

**Procedure (Using GNSS):**

1. **Set Up GNSS Equipment:**
   - Power on GPS receiver
   - Allow adequate time for satellite acquisition (5-10 minutes)
   - Verify adequate satellite coverage (minimum 6 satellites)
   - Check position dilution of precision (PDOP < 3 preferred)

2. **Occupy Each GCP:**
   - Position GNSS antenna directly over GCP marker
   - Use bipod or range pole for positioning
   - Measure antenna height above ground
   - Record position for 30-60 seconds (improves accuracy)

3. **Record Coordinates:**
   - Note coordinate system used (WGS84, local datum, etc.)
   - Record X (Easting), Y (Northing), Z (Elevation)
   - Record horizontal and vertical accuracy estimates
   - Convert to consistent coordinate system if needed

**Example GCP Record:**
```
GCP-01: Painted mark on large boulder, upstream left
X: 684523.45 m (UTM Zone 48S)
Y: 9234567.89 m
Z: 432.56 m (above mean sea level)
Horizontal accuracy: ±0.03 m
Vertical accuracy: ±0.05 m
Date surveyed: 2024-01-15
Surveyed by: Field Team A
```

4. **Create GCP Database:**
   - Compile all GCP coordinates into spreadsheet
   - Include GCP ID, description, coordinates, accuracy, photos
   - Store with installation documentation
   - Upload to project database

**Quality Check:**
- All GCPs surveyed with adequate accuracy
- Coordinates recorded in consistent system
- GCP descriptions clear and complete
- Photos document each GCP
- Data backed up in multiple locations

## Step 5: Staff Gauge Visibility Verification

### 5.1 Gauge Readability Assessment

**Test at Multiple Water Levels (if possible):**

**Procedure:**

1. **Current Water Level Test:**
   - Capture image at current water level
   - Zoom to 100% magnification
   - Read gauge markings from image
   - Verify markings are legible
   - Record smallest division readable: _____ cm

2. **Readability Criteria:**
   - **Excellent:** Can read individual centimeters clearly
   - **Good:** Can read 5cm or 10cm divisions clearly
   - **Marginal:** Can identify meter marks only
   - **Poor:** Gauge not readable from image

3. **Assess Readability Throughout Water Level Range:**
   - If possible, test at low, medium, and high water levels
   - Note any water levels where gauge becomes difficult to read
   - Identify issues (reflections, glare, distance, angle)

4. **Document Results:**
   - Record water level range where gauge is readable
   - Note any problematic water levels
   - Photograph gauge at each test water level
   - Document lighting conditions affecting readability

**If Readability is Poor:**
- Adjust camera position closer to gauge
- Increase camera resolution
- Use zoom lens or higher focal length
- Improve gauge visibility (paint, lighting)
- Adjust camera exposure settings

### 5.2 Gauge Orientation and Perspective Check

**Procedure:**

1. **Assess Gauge Angle in Image:**
   - Measure apparent angle of gauge in image
   - Ideal: Gauge appears vertical in image
   - Acceptable: Gauge tilted but all markings visible
   - Problem: Perspective distortion obscures markings

2. **Check for Perspective Distortion:**
   - Verify gauge width appears consistent top to bottom
   - Check that markings are evenly spaced in image
   - Look for "keystone" distortion (trapezoid shape)
   - Assess if distortion affects readability

3. **Evaluate Gauge Position in Frame:**
   - Ideal: Gauge in center third of image (best lens quality)
   - Acceptable: Gauge in outer thirds but not at extreme edge
   - Problem: Gauge at extreme edge (vignetting, distortion)

**If Perspective Issues Found:**
- Reposition camera for more perpendicular view
- Move camera closer to reduce angle
- Consider repositioning gauge if camera cannot be moved
- Accept limitations and document in procedures

### 5.3 Create Gauge Reading Reference

**Purpose:** Help future users read water level from images.

**Procedure:**

1. **Capture Reference Images at Known Water Levels:**
   - If possible, capture images at multiple known levels
   - Record actual water level for each image
   - Take images at 0.5m or 1m intervals if feasible
   - Save images with water level in filename

2. **Create Visual Reference Guide:**
   - Compile reference images into document
   - Label each image with corresponding water level
   - Show how to read gauge from image
   - Include examples of difficult reading scenarios

3. **Document Gauge Characteristics:**
   - Gauge type and markings (cm, dm, m)
   - Color scheme and visibility
   - Zero point elevation and reference datum
   - Any special features or quirks

4. **Store Reference Materials:**
   - Include in installation documentation
   - Provide to operators and data analysts
   - Upload to project repository
   - Print laminated copy for field reference

## Step 6: FOV Documentation and Mapping

### 6.1 Create FOV Map

**Procedure:**

1. **Prepare Base Map:**
   - Use site survey map or create sketch
   - Include river, banks, structures, gauge, camera
   - Use appropriate scale (e.g., 1:100 or 1:200)
   - Orient map to north

2. **Add Camera Information:**
   - Mark camera location
   - Draw camera viewing direction
   - Indicate camera height and tilt angle
   - Show approximate FOV cone

3. **Plot FOV Boundaries:**
   - Mark all FOV corner points from survey
   - Draw FOV boundary on map
   - Label boundary points with coordinates
   - Show FOV markers installed in field

4. **Add Ground Control Points:**
   - Plot all GCPs on map
   - Label with GCP IDs
   - Include coordinates or coordinate table
   - Show GCP distribution across FOV

5. **Annotate Map:**
   - Add scale bar
   - Include north arrow
   - Show legend explaining symbols
   - Note map datum and projection
   - Include date and map creator

**Save Map:**
- Export as high-resolution image (PNG or PDF)
- Print copies for field and office use
- Include in installation documentation
- Upload to project database

### 6.2 Photographic Documentation

**Required Photographs:**

1. **Overall Site View:**
   - Wide shot showing camera, gauge, and river
   - Multiple angles
   - Include FOV markers if visible

2. **Camera View:**
   - From directly behind camera looking at scene
   - Shows what camera sees from camera position

3. **FOV Boundary Markers:**
   - Photo of each marker from camera position
   - Close-up of each marker showing details and labeling

4. **Staff Gauge:**
   - Full gauge from camera view
   - Close-up of gauge showing markings
   - Gauge with water level reading visible

5. **Ground Control Points:**
   - Each GCP from camera view
   - Close-up of each GCP marker

6. **Camera Image Examples:**
   - Screen captures of camera live view
   - Include current water level
   - Various lighting conditions if possible

**Organize Photos:**
- Create folder structure by category
- Use descriptive filenames with date
- Include photo captions/descriptions
- Store with installation documentation

### 6.3 Complete FOV Assessment Report

**Report Contents:**

**1. Site Information:**
- Site name and location
- Installation date
- Installation team
- Weather and water conditions during assessment

**2. Camera Configuration:**
- Camera make and model
- Lens specifications and FOV angles
- Camera position (coordinates, height, orientation)
- Image resolution and settings

**3. FOV Coverage:**
- FOV dimensions at water surface
- Corner point coordinates
- Coverage area (square meters)
- Coverage verification results

**4. Staff Gauge Assessment:**
- Gauge type and specifications
- Visible water level range
- Readability assessment results
- Gauge position in frame

**5. Ground Control Points:**
- Number of GCPs established
- GCP coordinate table
- Survey method and accuracy
- GCP distribution assessment

**6. Image Quality:**
- Quality assessment results
- Any issues identified
- Adjustments made
- Final quality verification

**7. Field Markers:**
- Marker locations and types
- Installation details
- Maintenance requirements

**8. Maps and Photos:**
- FOV map
- Site photos
- Camera image examples
- GCP and marker photos

**9. Recommendations:**
- Any additional work needed
- Maintenance schedule
- Future monitoring priorities
- Issues to address

## Troubleshooting Guide

### Problem: FOV Does Not Cover Required Area

**Solutions:**
1. Adjust camera aim to shift FOV
2. Change lens to wider angle (if available)
3. Reposition camera further from target
4. Move camera to higher elevation
5. Adjust site requirements if camera limitations exist

### Problem: FOV Markers Not Visible in Images

**Solutions:**
1. Use brighter colors or larger markers
2. Raise marker height
3. Position markers against contrasting background
4. Add reflective material to markers
5. Enhance markers with paint or fabric

### Problem: Staff Gauge Not Readable

**Solutions:**
1. Move camera closer to gauge
2. Increase image resolution
3. Improve gauge visibility (repaint, add lighting)
4. Adjust camera exposure settings
5. Use zoom or telephoto lens

### Problem: Cannot Access Areas to Place Markers

**Solutions:**
1. Place markers at accessible locations nearby
2. Use calculated FOV boundaries instead of physical markers
3. Create virtual FOV map without physical markers
4. Wait for lower water level or better access conditions
5. Use drone or aerial imagery to verify FOV

### Problem: GCP Survey Accuracy Insufficient

**Solutions:**
1. Use higher-grade GNSS equipment
2. Increase occupation time at each point
3. Return for survey during better satellite conditions
4. Use differential correction if available
5. Hire professional survey services

### Problem: Image Quality Varies with Conditions

**Solutions:**
1. Test at various times of day and weather
2. Adjust camera settings for different conditions
3. Install automated exposure control
4. Add lighting for low-light conditions
5. Document acceptable operating conditions in procedures

## Maintenance and Monitoring

**Weekly (First Month):**
- Verify FOV coverage remains correct
- Check marker condition
- Confirm gauge readability
- Capture test images for comparison

**Monthly:**
- Inspect all FOV markers
- Verify GCPs are still visible and intact
- Check for vegetation growth affecting FOV
- Re-verify gauge coverage

**Quarterly:**
- Survey GCPs if any suspected movement
- Refresh marker paint or flags
- Clear vegetation if needed
- Update FOV map if any changes

**Annually:**
- Complete FOV reassessment
- Resurvey GCPs
- Replace deteriorated markers
- Update documentation

**After Significant Events:**
- Flood events: Verify markers remain, check for debris
- High winds: Check marker stability
- Equipment maintenance: Re-verify FOV after any camera adjustment
- Bank erosion: Resurvey if riverbank changes significantly

## Summary

Field of view assessment and marking is essential for ensuring the camera system will provide useful data for water level measurement and surface velocity monitoring. Key activities include:

1. **Test Image Capture:** Verify camera operates and produces quality images
2. **FOV Boundary Determination:** Calculate and physically mark FOV extent
3. **Physical Marking:** Install visible markers showing FOV coverage area
4. **GCP Establishment:** Survey fixed reference points for georeferencing
5. **Gauge Verification:** Confirm staff gauge is readable throughout water level range
6. **Documentation:** Create comprehensive maps, photos, and reports

Proper FOV assessment provides the foundation for accurate measurements and ensures field teams understand what the camera monitors.

**Installation Complete:** Camera system is now fully installed and assessed. Proceed to system commissioning and data collection procedures in subsequent chapters.