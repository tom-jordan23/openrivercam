# 10.3 Configuring the PtBox - Adding Cross-Sections

This section configures cross-section data for discharge calculations. While velocity measurements use the coordinate transformation from Section 10.2, discharge calculation requires channel geometry. Cross-section bathymetry surveyed in Section 9.11 now integrates with PtBox to enable Q = v × A calculations.

Cross-section configuration connects surveyed bed elevations with the camera image, allowing the system to calculate wetted area at any water level. Combined with velocity measurements, this produces discharge estimates for operational monitoring.

By the end of this section, you will be able to:
- Export cross-section survey data from SW Maps
- Import cross-section coordinates into PtBox
- Define cross-section location and orientation in camera view
- Associate surveyed cross-section with image position
- Verify cross-section alignment with velocity measurement area
- Configure water level reference for area calculation
- Save cross-section configuration for discharge calculations

**Reference:** Builds on Section 9.11 (Cross-Section Survey) and Section 3 (Discharge = Velocity × Area).

---

## Understanding Cross-Section Purpose in OpenRiverCam

### The Discharge Equation

**From Chapter 3 hydrology concepts:**

**Discharge: Q = v × A**

Where:
- **Q** = discharge (m³/s, cubic meters per second)
- **v** = mean velocity (m/s, from OpenRiverCam surface velocity measurement × depth correction factor)
- **A** = cross-sectional area (m², from surveyed bathymetry and current water level)

**OpenRiverCam measures velocity (v) using camera images:**
- Particle Image Velocimetry (PIV) tracks surface features
- Coordinate transformation (Section 10.2) converts pixel movement to meters per second
- Velocity correction factor (typically 0.85-0.90) converts surface velocity to mean velocity

**Cross-section provides area (A):**
- Surveyed bed elevations define channel geometry (Section 9.11)
- Current water level determines wetted area
- Cross-sectional area calculation: A = f(bed elevations, water level)

**Without cross-section configuration:**
- PtBox can measure velocity but cannot calculate discharge
- Velocity data alone insufficient for flood monitoring or water resource management
- Cross-section is essential for operational discharge estimates

### How Cross-Sections Work in PtBox

**Cross-section configuration establishes:**

**Spatial reference:**
- Cross-section location relative to camera field of view
- Alignment with velocity measurement area
- Position of cross-section endpoints (left bank, right bank)

**Geometric data:**
- Bed elevation at each station across channel
- Distance between stations (horizontal spacing)
- Channel shape (bathymetric profile)

**Water level reference:**
- How to determine current water level (from stage sensor, visual reference, or manual input)
- Calculation of wetted depth at each station: depth = water level - bed elevation
- Integration of wetted area: A = Σ(depth × station spacing)

**Operational use:**
1. **Measure surface velocity** from camera images (PIV processing)
2. **Convert to mean velocity** (apply depth correction factor)
3. **Measure current water level** (stage sensor or manual reading)
4. **Calculate cross-sectional area** from cross-section geometry and water level: A = A(h)
5. **Calculate discharge** Q = v × A

**Multiple cross-sections:**
- Some sites use multiple cross-sections (upstream, downstream, at different locations)
- Configuration process similar for each cross-section
- Discharge calculations may use average of multiple cross-sections or specific cross-section aligned with velocity measurement

---

## Preparing Cross-Section Data for Import

### Exporting Cross-Section Data from SW Maps

**From Section 9.11, cross-section data stored in SW Maps:**

**Export procedure:**

1. **Open SW Maps project containing cross-section survey**

2. **Select cross-section layer:**
   - Layer name: "Discharge Cross Section" or "Level Cross Section"
   - Contains all stations surveyed along transect (XS1_ST1, XS1_ST2, etc.)

3. **Export layer to CSV format:**
   - SW Maps menu → Export → Select CSV
   - Choose fields to export:
     - **Required:** point_id, X coordinate, Y coordinate, Z coordinate
     - **Useful:** station_number, distance_from_LB, water_depth, bed_elevation
   - Save with clear filename: `CrossSection_XS1_Site01_20241115.csv`

4. **Transfer file to configuration device** (laptop for PtBox configuration)

**CSV format example:**
```
point_id,station_number,X,Y,Z,distance_from_LB,bed_elevation,water_depth
XS1_ST1,1,685443.50,9456794.20,141.15,0.0,141.15,Dry
XS1_ST2,2,685445.45,9456794.40,140.45,2.0,140.45,Dry
XS1_ST3,3,685447.40,9456794.60,139.95,4.0,139.95,0.30
XS1_ST4,4,685449.35,9456794.80,139.65,6.0,139.65,0.60
XS1_ST5,5,685451.30,9456795.00,138.75,8.0,138.75,1.50
XS1_ST6,6,685453.25,9456795.20,139.55,10.0,139.55,0.70
XS1_ST7,7,685455.20,9456795.40,139.85,12.0,139.85,0.40
XS1_ST8,8,685457.15,9456795.60,140.35,14.0,140.35,Dry
XS1_ST9,9,685459.10,9456795.80,141.05,16.0,141.05,Dry
```

**Key fields explained:**

**point_id:**
- Unique identifier for each station: XS1_ST1, XS1_ST2, etc.
- XS1 = Cross-section 1, ST1 = Station 1
- Sequential numbering from left bank to right bank

**X, Y, Z coordinates:**
- Real-world position of each station (surveyed with RTK GPS)
- X = Easting, Y = Northing (UTM or local coordinate system)
- Z = Elevation (bed elevation at station)

**station_number:**
- Sequential number: 1, 2, 3, ..., 9
- Identifies order along cross-section transect

**distance_from_LB:**
- Horizontal distance from left bank reference point (meters)
- Example: ST1 at 0m, ST2 at 2m, ST3 at 4m (2m station spacing)
- Used for plotting cross-section profile

**bed_elevation:**
- Elevation of river bed at this station (Z coordinate)
- May be calculated: bed_elevation = antenna_elevation - pole_height
- Or directly recorded during survey

**water_depth:**
- Water depth at time of survey: water_level - bed_elevation
- "Dry" indicates station above waterline
- Useful for verification but not required for configuration

### Calculating Additional Fields (If Needed)

**Some fields may require post-processing:**

**Distance from left bank:**
- If not calculated during survey, compute from coordinates:
```
For each station:
distance_from_LB = sqrt((X - X_LB)² + (Y - Y_LB)²)

Where (X_LB, Y_LB) is left bank reference point (first station)
```

**Bed elevation:**
- If not calculated during survey:
```
bed_elevation = Z_antenna - pole_height

Where Z_antenna is measured elevation (from RTK) and pole_height measured during survey
```

**Calculate in spreadsheet before import, or PtBox may calculate automatically if raw data provided.**

### Verifying Data Quality

**Before importing, quality-check cross-section data:**

**Completeness check:**
- [ ] All stations included (ST1 through ST9, or however many surveyed)
- [ ] No missing coordinates (each station has X, Y, Z)
- [ ] Stations in correct sequence (ST1 = left bank, ST9 = right bank)

**Coordinate sanity check:**
- [ ] X, Y coordinates reasonable for site location
- [ ] Z coordinates (bed elevations) reasonable (within expected range)
- [ ] Bed elevations decrease toward thalweg (deepest point mid-channel, higher at banks)

**Profile shape check:**
- Plot bed elevation vs. distance from left bank
- Profile should show logical channel shape (V-shaped, U-shaped, or trapezoidal)
- No obvious outliers or impossible jumps (e.g., ST5 bed elevation 5m lower than ST4 and ST6)

**Example quality check:**
```
Station  Distance  Bed Elev   Notes
ST1      0m        141.15m    Left bank (highest)
ST2      2m        140.45m    Bank slope (decreasing elevation)
ST3      4m        139.95m    Waterline
ST4      6m        139.65m    Channel (continuing decrease)
ST5      8m        138.75m    Thalweg (lowest point - good)
ST6      10m       139.55m    Channel (increasing elevation)
ST7      12m       139.85m    Bank slope
ST8      14m       140.35m    Right bank slope
ST9      16m       141.05m    Right bank (high again - good)

Profile shape: U-shaped channel, logical progression ✓
```

**If data quality issues identified:**
- Return to SW Maps, verify export settings
- Check original survey data (Section 9.11) for errors
- Recalculate derived fields (distance, bed elevation)
- Do not proceed to import until data verified

---

## Loading Cross-Section Data into PtBox

### Accessing Cross-Section Configuration Interface

**In PtBox web interface:**

1. **Navigate to Cross-Sections section:**
   - Configuration menu → Discharge → Cross-Sections
   - Or River Geometry → Cross-Sections
   - Or similar navigation depending on interface version

2. **Verify prerequisites complete:**
   - [ ] Image orientation configured (Section 10.1)
   - [ ] Coordinate transformation established (Section 10.2, GCPs configured)
   - [ ] Sample video loaded and visible

3. **Access cross-section import interface:**
   - Look for "Add Cross-Section", "Import Cross-Section", or "New Cross-Section" button

### Importing Cross-Section from CSV

**If interface supports file import (recommended):**

1. **Click "Import Cross-Section" or "Load from File"**

2. **Select cross-section CSV file:**
   - Browse to: `CrossSection_XS1_Site01_20241115.csv`
   - Click "Open" or "Upload"

3. **Map CSV columns to PtBox fields:**
   - Interface may display column mapping dialog
   - Match CSV columns to required fields:
     - CSV "point_id" → PtBox "Station ID"
     - CSV "X" → PtBox "Easting" or "X coordinate"
     - CSV "Y" → PtBox "Northing" or "Y coordinate"
     - CSV "Z" or "bed_elevation" → PtBox "Bed Elevation"
     - CSV "distance_from_LB" → PtBox "Distance" or "Chainage"
   - Verify units: Meters (typically default)
   - Verify CRS: Must match survey data CRS (same as GCPs)

4. **Specify cross-section metadata:**
   - **Cross-section ID:** XS1 or CrossSection_1
   - **Cross-section name:** "Main channel cross-section" (descriptive)
   - **Survey date:** 2024-11-15 (date of survey)
   - **Notes:** "9 stations, 2m spacing, left bank to right bank"

5. **Preview imported data:**
   - Interface typically displays table of stations
   - May show cross-section profile plot (distance vs. elevation)
   - Review for completeness and logical profile

6. **Confirm import:**
   - Click "Import", "Accept", or "Load"
   - Cross-section data now stored in PtBox

**If import fails:**
- Check CSV format (correct column headers, proper delimiter)
- Verify no missing data (each row complete)
- Check for special characters or formatting issues
- Try manual entry if file import problematic

### Manual Entry Alternative

**If file import unavailable:**

**Create new cross-section:**
1. Click "Add Cross-Section" or "New Cross-Section"
2. Enter cross-section metadata (ID, name, date)

**For each station, enter data manually:**
1. Click "Add Station"
2. Fill in station attributes:
   - Station ID: XS1_ST1
   - Station number: 1
   - X coordinate: 685443.50
   - Y coordinate: 9456794.20
   - Bed elevation: 141.15
   - Distance from LB: 0.0
3. Save station
4. Repeat for all stations (ST2, ST3, ..., ST9)

**Manual entry time-consuming but reliable** if file import not working.

---

## Defining Cross-Section Location in Camera View

### Understanding Cross-Section Visualization

**Cross-section must be positioned relative to camera view:**

**Two spatial references:**
1. **Real-world position:** Surveyed X, Y, Z coordinates of each station
2. **Image position:** Where cross-section appears in camera field of view

**PtBox uses coordinate transformation** (from Section 10.2) to project cross-section onto camera image:
- Transformation converts real-world coordinates (X, Y, Z) to pixel coordinates (u, v)
- Cross-section stations appear as overlay on video frame
- Overlay shows where cross-section intersects camera field of view

**Why visualize cross-section in image:**
- Verify cross-section aligned with velocity measurement area
- Confirm cross-section visible in camera view (or at least portions visible)
- Check for spatial correspondence between velocity and area measurements

### Viewing Cross-Section Overlay

**After importing cross-section:**

1. **Enable cross-section overlay in video preview:**
   - Look for "Show Cross-Section" checkbox or toggle
   - Or "Overlay → Cross-Sections → XS1"

2. **Cross-section appears as line or points in video frame:**
   - Each station may display as marker (dot, circle, or cross)
   - Stations connected by line showing cross-section transect
   - Endpoints labeled (LB = left bank, RB = right bank)

3. **Assess cross-section position:**
   - **Does cross-section appear in expected location?**
   - **Is cross-section aligned perpendicular to flow?**
   - **Are some stations visible in camera view?**

**Expected alignment:**
- Cross-section typically positioned across river (left bank to right bank)
- Perpendicular to flow direction
- May be partially in field of view (some stations visible, some outside frame)
- Or fully in field of view (all stations visible)

### Verifying Cross-Section Alignment

**Quality checks for cross-section positioning:**

**Check 1: Endpoints match surveyed locations**
- Left bank endpoint (ST1) should appear near surveyed left bank position
- Right bank endpoint (ST9) should appear near surveyed right bank position
- If endpoints misaligned, possible causes:
  - Coordinate transformation incorrect (GCPs need recalibration)
  - Cross-section coordinates in wrong CRS
  - Cross-section data import error

**Check 2: Cross-section orientation**
- Cross-section line should run left-to-right (or at angle matching survey transect)
- Perpendicular to flow direction (approximately)
- If orientation wrong, check coordinate transformation and cross-section data

**Check 3: Vertical alignment**
- If video shows water surface and banks, cross-section should intersect logically
- Stations on banks (ST1, ST9) should overlay near bank features
- Mid-channel stations (ST5, ST6) should overlay on water surface area

**Check 4: Spatial correspondence with velocity area**
- Velocity measurements occur across entire field of view or specified region
- Cross-section should be representative of velocity measurement area
- Ideally cross-section positioned where velocities measured (same transect)
- Or upstream/downstream by short distance (<50m) if necessary

**If cross-section position unexpected:**
- Review coordinate transformation quality (Section 10.2 reprojection errors)
- Verify cross-section coordinates correct (check CSV data)
- Check CRS match between GCPs and cross-section
- Confirm cross-section surveyed at same site (not different location)

---

## Configuring Cross-Section Properties

### Setting Cross-Section Reference Parameters

**PtBox needs additional configuration for cross-section use:**

**Cross-section orientation:**
- **Upstream or downstream:** Which side is upstream?
- **Left bank definition:** Which station is left bank (looking downstream)?
- Direction matters for discharge calculations if using directional velocity

**Water level reference:**
- **How water level determined:**
  - Option 1: Stage sensor (pressure transducer, ultrasonic sensor)
  - Option 2: Visual staff gauge (manual reading)
  - Option 3: Camera-based water level detection
  - Option 4: Manual input (operator enters current water level)
- **Stage datum:** What is reference elevation for water level?
  - Typically same elevation datum as cross-section survey (e.g., meters above WGS84 ellipsoid)
  - Or relative to local benchmark (e.g., meters above arbitrary zero)

**Measurement frequency:**
- How often to calculate discharge
- Typically same as velocity measurement frequency (e.g., every 5 minutes)
- Or on-demand (calculate when requested)

### Defining Water Level Integration

**For discharge calculation, PtBox must know current water level:**

**Configuration options:**

**Option 1: Stage sensor integration (recommended)**
- PtBox connected to stage sensor via serial, analog, or network interface
- Sensor measures water surface elevation continuously
- PtBox reads sensor value automatically for each discharge calculation
- Configuration:
  - Sensor type and communication protocol
  - Sensor elevation datum (must match cross-section elevation datum)
  - Sensor offset calibration (if needed)

**Option 2: Manual water level input**
- Operator enters current water level before each discharge calculation
- Suitable for occasional measurements or sites without automated stage sensor
- Configuration:
  - Input interface (web form, API, or local interface)
  - Units and datum (meters above ellipsoid, or relative to benchmark)

**Option 3: Camera-based water level detection**
- Some PtBox configurations estimate water level from camera image
- Detect waterline position relative to reference markers
- Less accurate than stage sensor but may be adequate
- Configuration:
  - Reference markers surveyed and identified in image
  - Waterline detection algorithm parameters

**Elevation datum consistency critical:**
- Cross-section bed elevations in meters above WGS84 ellipsoid: 138.75m, 139.65m, etc.
- Water level must be in same datum: e.g., 140.25m above WGS84 ellipsoid
- If datums different, offset must be applied
- Example: Cross-section elevations above local benchmark, water level above sea level → must convert to common datum

### Configuring Discharge Calculation Parameters

**Additional parameters for Q = v × A calculation:**

**Velocity input:**
- Which velocity data to use for discharge calculation
- Options:
  - Mean velocity across entire field of view
  - Mean velocity in specified region (e.g., center 50% of frame)
  - Velocity at cross-section location (if PIV provides spatially-distributed velocity)
  - Manual velocity input (if PIV not operational)

**Velocity correction factor:**
- Surface velocity to mean velocity conversion: k = 0.85-0.90 (typically 0.87)
- Configuration:
  - Fixed value (0.87 default)
  - Variable based on water depth (deeper water → higher k)
  - Calibrated value from ADCP or current meter comparison

**Cross-sectional area calculation method:**
- Trapezoidal integration (standard): A = Σ (d_i + d_{i+1})/2 × Δx
- Simpson's rule (if more accurate integration desired)
- Interpolation between stations (if finer resolution needed)

**Output parameters:**
- Discharge units: m³/s (standard) or other units (L/s, cfs)
- Reporting frequency: Real-time, 5-minute average, 15-minute average
- Uncertainty estimation: Propagate velocity and area uncertainties to discharge uncertainty

---

## Verifying Cross-Section Configuration

### Visual Verification

**With cross-section overlay displayed:**

**Check 1: Cross-section visible in camera view**
- [ ] At least some stations appear in field of view
- [ ] Endpoints (left bank, right bank) identifiable
- [ ] Cross-section line orientation logical

**Check 2: Alignment with physical features**
- [ ] Cross-section overlays on river (not on land or completely outside frame)
- [ ] If specific features visible (rocks, stakes), cross-section passes through expected locations

**Check 3: Correspondence with velocity measurement area**
- [ ] Cross-section positioned in area where velocity measured
- [ ] Or near enough that velocity representative of cross-section flow

**If visual verification fails:**
- Recheck coordinate transformation (GCP calibration)
- Verify cross-section coordinates correct
- Confirm CRS consistency

### Test Discharge Calculation

**Most interfaces provide test calculation:**

**Test procedure:**

1. **Enter test water level:**
   - Example: Water level = 140.25 m (above ellipsoid)
   - Or use current stage sensor reading if available

2. **Enter test velocity:**
   - Example: Mean velocity = 0.65 m/s (from recent PIV measurement or estimate)

3. **Click "Calculate Discharge" or "Test Calculation"**

4. **Review results:**
   - **Calculated discharge:** Q = v × A = ?
   - **Cross-sectional area at this water level:** A = ?
   - **Wetted width:** Width of water surface at this level
   - **Maximum depth:** Deepest point in cross-section at this level

**Example test results:**
```
Water level: 140.25 m
Mean velocity: 0.65 m/s

Calculated cross-sectional area: 6.7 m²
Wetted width: 10.0 m (ST3 to ST7)
Maximum depth: 1.50 m (at ST5, thalweg)

Discharge: Q = 0.65 × 6.7 = 4.4 m³/s
```

**Sanity check results:**

**Is cross-sectional area reasonable?**
- For river width ~10m and average depth ~0.7m, area ~6-7 m² is logical
- If area unreasonably large (e.g., 50 m²) or small (e.g., 0.5 m²), investigate

**Is wetted width reasonable?**
- Should correspond to visible water width in camera view
- If wetted width much larger or smaller than observed, check water level datum

**Is maximum depth reasonable?**
- Should match observed conditions or survey notes
- If maximum depth much deeper than expected, verify bed elevations and water level datum consistent

**Is discharge reasonable?**
- For small/medium river with moderate velocity, 4-5 m³/s may be reasonable
- Compare with hydrograph expectations, seasonal patterns, or rainfall data
- If discharge obviously wrong (e.g., 500 m³/s for small stream), investigate calculation

**If test results unreasonable:**
- Check water level datum (most common error source)
- Verify bed elevations correct (check cross-section import)
- Confirm velocity input correct
- Review discharge calculation parameters

### Comparing with Alternative Measurements

**If available, compare with:**

**ADCP or current meter measurements:**
- Independent discharge measurements from field surveys
- Should agree within 10-20% (accounting for temporal variability and measurement uncertainty)

**Hydrometric data from nearby gauges:**
- Discharge at upstream or downstream gauge (adjust for tributary inflows)
- Rating curve estimates from similar flows

**Visual estimates:**
- Experienced hydrologists can estimate discharge by eye (within factor of 2-3)
- Very rough check but can identify gross errors

**If large discrepancy:**
- Double-check all configuration parameters
- Verify velocity measurements accurate
- Confirm cross-section representative of flow conditions
- May indicate need for calibration or refinement

---

## Handling Multiple Cross-Sections

### When to Use Multiple Cross-Sections

**Some sites benefit from multiple cross-sections:**

**Scenario 1: Non-uniform reach**
- Channel geometry varies along reach (expansion, contraction, bend)
- One cross-section not representative
- Solution: Survey 2-3 cross-sections, use average area or weighted average

**Scenario 2: Redundancy and validation**
- Multiple cross-sections provide check on discharge calculation
- If XS1 and XS2 produce similar discharge → confidence in results
- If XS1 and XS2 produce very different discharge → investigate

**Scenario 3: Stage-variable geometry**
- Low-flow cross-section (narrow, shallow channel)
- High-flow cross-section (includes floodplain or overbank areas)
- Use different cross-sections depending on water level

### Configuring Additional Cross-Sections

**Process same as first cross-section:**

1. **Export cross-section data from SW Maps** (e.g., XS2 with stations XS2_ST1, XS2_ST2, etc.)
2. **Import into PtBox** (specify XS2 as cross-section ID)
3. **Verify overlay in camera view** (XS2 appears in expected location)
4. **Configure XS2 parameters** (water level reference, calculation method)
5. **Test discharge calculation for XS2**

**Managing multiple cross-sections:**
- **Select active cross-section:** Interface typically allows choosing which cross-section to use for discharge calculation
- **Use all cross-sections:** Calculate discharge for each, report average or range
- **Conditional selection:** Use XS1 for low flows, XS2 for high flows (based on water level thresholds)

### Cross-Section Updates and Resurvey

**Over time, cross-sections may require updates:**

**When to resurvey:**
- **Channel morphology change:** Erosion, deposition, or bed scour alters cross-section shape
- **Seasonal vegetation:** Vegetation growth in channel changes effective area
- **Post-flood changes:** Major flood event may reshape channel
- **Validation:** Discharge calculations deviate from expected values or alternative measurements

**Updating cross-section in PtBox:**
1. Resurvey cross-section (Section 9.11 procedure)
2. Export new cross-section data from SW Maps
3. Import updated cross-section into PtBox (replace previous version)
4. Verify new cross-section configuration
5. Document change (date, reason, magnitude of change)

**Typical resurvey frequency:**
- **Stable bedrock channels:** Every 2-5 years (minimal change)
- **Sand/gravel bed rivers:** Every 6-12 months (moderate change)
- **Active channels:** Every 3-6 months or post-flood (significant change)

---

## Common Issues and Solutions

### Issue: Cross-section overlay not visible in video

**Symptoms:**
- Import cross-section successfully, but overlay does not appear on video frame
- Or overlay appears completely outside camera field of view

**Solutions:**
- **Check coordinate transformation:** GCP calibration (Section 10.2) must be correct for cross-section overlay to work
  - Verify GCP reprojection errors acceptable
  - Recalculate transformation if needed
- **Verify CRS match:** Cross-section coordinates must use same CRS as GCPs
  - Check SW Maps project CRS settings
  - Re-export cross-section in correct CRS if needed
- **Check cross-section location:** Cross-section may be at different site or far from camera view
  - Verify surveyed location matches camera installation location
  - Review survey field notes for cross-section position
- **Zoom out video view:** Cross-section may be just outside default view
  - Use zoom and pan controls to search for cross-section overlay

### Issue: Discharge calculation produces unreasonable results

**Symptoms:**
- Discharge extremely high (e.g., 500 m³/s for small stream)
- Or discharge extremely low (e.g., 0.05 m³/s for large river)
- Or discharge negative

**Solutions:**
- **Check water level datum:**
  - Most common error: Water level in different datum than bed elevations
  - Example: Water level 2.5m relative to staff gauge, bed elevations 140m above ellipsoid → incompatible
  - Convert water level to same datum as cross-section
- **Verify bed elevations:** Check cross-section import, confirm bed elevations reasonable
- **Check velocity input:** Confirm velocity value correct (not zero, not excessively high)
- **Review calculation parameters:** Verify velocity correction factor, area calculation method

### Issue: Cross-section overlay misaligned with video features

**Symptoms:**
- Cross-section overlay appears in wrong location (e.g., 5m left of expected position)
- Or cross-section rotated relative to visible river channel

**Solutions:**
- **Recalibrate GCP transformation:** Misalignment indicates coordinate transformation problem
  - Review GCP reprojection errors (Section 10.2)
  - Check for GCP identification errors
  - Recalculate transformation with corrections
- **Verify cross-section survey accuracy:** Cross-section may have been surveyed incorrectly
  - Check survey field notes
  - Compare cross-section coordinates with camera position coordinates
  - Resurvey cross-section if major discrepancy

### Issue: Water level sensor reading does not match visual observation

**Symptoms:**
- Stage sensor reports water level 140.50m
- Visual observation in camera shows water at different level than expected for 140.50m

**Solutions:**
- **Check sensor calibration:** Stage sensor may have offset error
  - Compare sensor reading with manual staff gauge reading
  - Apply calibration offset in PtBox configuration
- **Verify sensor datum:** Sensor elevation reference must match cross-section datum
  - Resurvey sensor installation elevation if uncertain
  - Configure datum conversion in PtBox if needed
- **Check sensor functionality:** Sensor may be malfunctioning
  - Verify sensor power and communication
  - Test sensor in controlled conditions (known water level)

---

## Time Estimates

**Cross-section configuration time:**

**First-time configuration (single cross-section, 9 stations):**
- Export cross-section data from SW Maps: 5 minutes
- Import cross-section into PtBox: 5-10 minutes
- Verify overlay and alignment: 5-10 minutes
- Configure parameters (water level, discharge calculation): 10-15 minutes
- Test discharge calculation: 5-10 minutes
- Troubleshoot and refine (if needed): 10-20 minutes
- **Total: 40-70 minutes**

**Experienced user:**
- Export and import: 5 minutes
- Verify and configure: 10-15 minutes
- Test: 5 minutes
- **Total: 20-25 minutes**

**Multiple cross-sections:**
- First cross-section: Full time (above)
- Additional cross-sections: 10-15 minutes each (process familiar, configuration similar)

**Cross-section configuration faster than GCP configuration** (Section 10.2) because less precision required and fewer interactive steps.

---

## Summary: Adding Cross-Sections

**Purpose:**
- Enable discharge calculation by providing channel geometry (Q = v × A)
- Define cross-sectional area as function of water level: A = A(h)
- Integrate surveyed bathymetry with velocity measurements

**Key steps:**
1. Export cross-section survey data from SW Maps (Section 9.11)
2. Import cross-section coordinates into PtBox (CSV or manual entry)
3. Verify cross-section overlay in camera view (spatial alignment)
4. Configure cross-section properties (water level reference, calculation parameters)
5. Test discharge calculation (verify reasonable results)
6. Save cross-section configuration for operational use

**Quality criteria:**
- Cross-section visible or aligned with camera field of view
- Overlay position matches surveyed location (coordinate transformation accurate)
- Test discharge calculation produces reasonable results (logical Q, A, wetted width, max depth)
- Water level datum consistent with cross-section bed elevations

**Common issues and resolutions:**
- Overlay not visible: Check GCP transformation, verify CRS match
- Unreasonable discharge: Check water level datum compatibility
- Misaligned overlay: Recalibrate GCP transformation
- Stage sensor mismatch: Verify sensor datum and calibration

**Integration with velocity measurements:**
- PtBox measures velocity continuously (PIV processing)
- PtBox reads current water level (stage sensor or manual input)
- PtBox calculates cross-sectional area from cross-section geometry and water level
- PtBox calculates discharge: Q = v × A
- Discharge reported in real-time or at specified intervals

**Next step:**
With transformation and cross-section configured, proceed to Section 10.4: Server Integration to enable remote data access and Section 10.5: Automated Collection and Upload for operational monitoring.

---

**References:**
- Section 9.11: Survey Execution - Cross-Section Survey (cross-section data source)
- Section 3: Hydrology Concepts (Q = v × A, discharge calculations)
- Section 10.2: Adding Control Points (coordinate transformation prerequisite)
- Section 10.4: Server Integration (next configuration step)
