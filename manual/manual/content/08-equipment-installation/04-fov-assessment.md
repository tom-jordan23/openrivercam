# 8.4 Assessing the Camera Scene and Marking FOV

## Overview

After installing the camera, it is critical to verify that the field of view (FOV) covers the required area for water level measurement and surface velocity monitoring. This section describes procedures for capturing test images, assessing FOV coverage, physically marking FOV boundaries in the field, and verifying staff gauge visibility. Proper FOV assessment ensures accurate measurements and helps field teams understand the camera's viewing area.

**Time Required:** 2-3 hours

**Prerequisites:**
- Camera installed and powered (Section 8.3)
- Network connectivity to camera established
- Camera aimed at target area
- Staff gauge installed and visible
- Access to river/stream bank safe

## Safety Considerations

**SAFETY WARNINGS:**

- **Water Safety:** Working near water presents drowning risk. Wear life jacket if working close to water's edge or on unstable banks.
- **Slippery Surfaces:** River banks and wet rocks are slippery. Use appropriate footwear with good traction.
- **Flash Floods:** Be aware of upstream conditions. Cease work immediately if water level rises unexpectedly.
- **Electrical Hazards:** Camera system is powered. Avoid contact with electrical components.
- **Wildlife and Vegetation:** Be aware of local hazards (snakes, insects, poisonous plants).

**Personal Protective Equipment (PPE):**
- Life jacket or personal flotation device (if working near water)
- Non-slip footwear (water shoes or boots)
- Long pants and sleeves (protection from vegetation)
- Hat and sunscreen
- Insect repellent (if applicable)
- First aid kit accessible

## Equipment and Tools Checklist

**Computer Equipment:**
- Laptop or tablet with network capability
- Network cable (if accessing camera via wired connection)
- Portable WiFi router (if camera has wireless capability)
- Power bank or extra battery for laptop
- USB drive (for storing test images)
- Camera configuration software or web browser

**Field Marking Equipment:**
- Survey flags or stakes (brightly colored, minimum 10)
- Flagging tape (bright colors: orange, pink, or yellow)
- Measuring tape (30-50 meters)
- Range finder or laser distance meter
- Permanent markers
- Spray paint (optional, for semi-permanent marking)
- Whiteboard or marking board (for creating reference markers)
- Camera tripod (for ground-level photography)
- Smartphone or camera (for documentation)

**Documentation Materials:**
- Field notebook and pencils
- Site map or sketch
- Clipboard
- Camera/smartphone for photos
- GPS unit or GPS-enabled smartphone
- Forms for recording FOV coordinates

**Safety and Utility:**
- Life jacket
- First aid kit
- Water and snacks
- Sun protection
- Communication device (radio or phone)
- Rope (if accessing difficult areas)

## Step 1: Initial Test Image Capture

### 1.1 Access Camera Live View

**Procedure:**

1. **Connect to Camera:**
   - Connect laptop to camera network
   - Open web browser and navigate to camera IP address
   - Login with credentials configured in Section 8.3
   - Navigate to live view page

2. **Verify Camera Operation:**
   - Confirm live video stream is displaying
   - Check image quality is acceptable
   - Verify frame rate is smooth
   - Look for any error messages or warnings

3. **Optimize Display:**
   - Maximize browser window for best viewing
   - Disable any overlays or on-screen information that obscure view
   - Ensure display refresh rate is adequate
   - Adjust browser zoom if needed to see details

**Quality Check:**
- Live stream is clear and stable
- Full image frame is visible on screen
- No error messages
- Able to see staff gauge in image

### 1.2 Capture Reference Images

**Purpose:** Create baseline images under current conditions for assessment.

**Procedure:**

1. **Capture Images at Current Water Level:**
   - Take snapshot or save frame from live stream
   - Save image with descriptive filename
   - Recommended format: `YYYY-MM-DD_HHMM_baseline.jpg`
   - Record current water level reading from gauge: _____ m

2. **Note Current Conditions:**
   - Time of capture: _____
   - Weather: _____
   - Lighting conditions: _____
   - Water surface conditions: _____ (calm, ripples, waves, etc.)
   - Any obstructions or issues visible: _____

3. **Capture Multiple Images:**
   - Take images at 5-10 minute intervals
   - Capture at least 5 images for assessment
   - Vary lighting conditions if possible (cloudy vs. sunny)
   - Note any changes in image quality with changing conditions

**Save Images:**
- Store images on laptop
- Copy to USB drive for backup
- Include images in installation documentation
- Upload to project folder if remote access available

### 1.3 Assess Image Quality

**Image Quality Checklist:**

**Clarity and Focus:**
- [ ] Staff gauge markings are sharp and readable
- [ ] Numbers on gauge are legible at full resolution
- [ ] Water surface texture is visible (for velocity tracking)
- [ ] Background features are adequately sharp

**Exposure and Lighting:**
- [ ] Image is not overexposed (blown out highlights)
- [ ] Image is not underexposed (lost shadow detail)
- [ ] Adequate contrast between gauge and background
- [ ] No significant glare or reflections obscuring gauge

**Field of View Coverage:**
- [ ] Entire staff gauge is visible (highest and lowest marks)
- [ ] Adequate margin above and below gauge (for water level variation)
- [ ] Sufficient horizontal coverage for surface velocity measurement
- [ ] No vignetting or dark corners in image

**Issues to Note:**
- Areas of poor visibility
- Reflections or glare
- Obstructions (vegetation, debris)
- Perspective distortion
- Any other quality concerns

**If Image Quality Issues Found:**
- Adjust camera settings (exposure, focus)
- Reposition camera if necessary
- Address obstructions
- Install sunshade or adjust existing shade
- Refer to troubleshooting in Section 8.3

## Step 2: Field of View Boundary Determination

### 2.1 Understand Field of View Geometry

**Key Concepts:**

**Field of View (FOV):**
- The area visible to the camera, defined by horizontal and vertical angles
- FOV depends on lens focal length and sensor size
- Wider angle lenses = larger FOV
- Telephoto lenses = smaller FOV

**FOV Calculation:**
- **Horizontal FOV at distance D:**
  - Width = 2 × D × tan(horizontal_angle / 2)
- **Vertical FOV at distance D:**
  - Height = 2 × D × tan(vertical_angle / 2)

**Example:**
- Camera with 60° horizontal FOV
- Distance to river: 15 meters
- Horizontal coverage: 2 × 15 × tan(30°) = 17.3 meters

**Important:** Actual FOV varies with distance. Objects closer to camera occupy more pixels than distant objects.

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

**Survey Flags (Temporary):**
- Use for initial assessment
- Bright colors visible in images
- Easy to reposition
- Replace with permanent markers

**Painted Markers (Semi-Permanent):**
- Spray paint on rocks or fixed features
- Bright colors (orange, yellow, pink)
- Label with "CAMERA FOV" or similar
- Refresh periodically as paint fades

**Installed Markers (Permanent):**
- Bright fabric flags on poles
- PVC pipes painted bright colors
- Metal or wooden stakes
- Concrete markers

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
- Fixed location (not moving or changing)
- Clearly identifiable in images
- Distributed throughout FOV
- Accessible for surveying
- Permanent or semi-permanent features

**Good GCP Examples:**
- Painted marks on rock outcrops
- Corners of concrete structures
- Bridge abutments or piers
- Permanent survey markers
- Corners of buildings
- Fixed fence posts or poles

**Poor GCP Examples:**
- Vegetation (grows and moves)
- Debris or temporary objects
- Moving water features
- Areas prone to erosion
- Items that may be removed

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