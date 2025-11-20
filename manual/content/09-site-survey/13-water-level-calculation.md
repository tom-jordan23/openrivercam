# 9.13 Survey Data Processing - Water Level Calculation

This section covers the extraction and processing of water level data from survey measurements. Water level (also called stage or water surface elevation) is a fundamental parameter for river monitoring - it determines which portions of the cross-section are wetted, enables calculation of cross-sectional area, and serves as the independent variable in stage-discharge rating curves.

Water level is the reference elevation that connects survey bathymetry to real-time discharge measurements. Every discharge calculation requires knowing the current water level to determine wetted area from the surveyed cross-section.

By the end of this section, you will understand:
- How to extract water surface elevation from survey data
- The coordinate system requirements for water level measurements
- How to relate surveyed water level to staff gauge readings (if present)
- How water level initiates stage-discharge relationship development
- Documentation requirements for rating curve development
- Quality control for water level data

**Reference:** SURVEY_PROCESS.md Section 6 - Water Level Survey

---

## Water Level Fundamentals

### What is Water Level

**Water level (stage) is the elevation of the water surface at a specific location and time.**

**In surveying terms:**
- Water level is a horizontal plane at a specific elevation above a reference datum
- For UTM coordinates: Water level = Z_water (elevation in meters above WGS84 ellipsoid)
- Example: "Water level at time of survey = 140.25m" (UTM Zone 48S elevation)

**Water level varies with:**
- **Time:** Changes constantly (rising during storms, falling during dry periods)
- **Location:** Different elevations along river (drops with distance downstream due to slope)
- **Flow conditions:** Higher during floods, lower during droughts

**For OpenRiverCam discharge monitoring:**
- Water level determines wetted cross-sectional area A (in Q = v × A)
- Measure velocity with camera (v)
- Calculate area from water level and surveyed bathymetry (A = A(h))
- Calculate discharge Q = v × A

### Water Level Measurement During Survey

**From SURVEY_PROCESS.md Section 6:**

```
Water Level Survey:
- Survey water surface elevation with rover pole
- Note depth on pole, maintain RTK FIX
- Record in Water Level layer with flow conditions
- Take multiple measurements if water is moving
```

**Survey procedure (field work, completed during survey day):**

**Step 1: Position rover pole at water surface**
- Lower pole tip TO water surface (not through water to bed)
- Keep pole tip just touching water (not submerged, not above water)
- Level pole (bubble centered)

**Step 2: Achieve RTK FIX and average**
- Standard quality gates (FIX, satellites ≥12, PDOP ≤2.5)
- Averaging time: 60-120 seconds
- RTK measures antenna elevation: Z_antenna

**Step 3: Measure pole height**
- Pole height from water surface TO antenna: h_pole_water
- Example: 2.15m from water surface to antenna
- Record in field notebook and SW Maps attributes

**Step 4: Calculate water surface elevation**
```
Z_water = Z_antenna - h_pole_water
```

**Example:**
- RTK measures antenna: Z_antenna = 142.40m
- Pole height (water surface to antenna): h_pole_water = 2.15m
- Water level: Z_water = 142.40 - 2.15 = 140.25m

**This 140.25m is the water surface elevation at the time of survey** (critical reference for all subsequent discharge calculations).

---

## Extracting Water Level from Survey Data

### Method 1: Direct Water Level Measurement

**If water level was measured directly during survey (recommended method):**

**From SW Maps export, water level measurement appears as point in "Water Level" layer:**

**Attribute data:**
- `point_id`: WL_001 (water level measurement ID)
- `x_coord`: 685435.20 (easting)
- `y_coord`: 9456781.50 (northing)
- `z_coord`: 142.40 (antenna elevation)
- `pole_height`: 2.15 (water surface to antenna)
- `survey_time`: 2024-11-14 14:35:00
- `flow_conditions`: "Moderate flow, slight ripples"
- `notes`: "Water level measurement at cross-section XS1 centerline"

**Calculate water surface elevation:**
```
Z_water = z_coord - pole_height
Z_water = 142.40 - 2.15 = 140.25m
```

**This is the primary water level value for the survey.**

**If multiple water level measurements taken:**
- Average multiple measurements (reduces uncertainty from ripples, waves)
- Example: WL_001 = 140.25m, WL_002 = 140.23m, WL_003 = 140.26m
- Average: Z_water = (140.25 + 140.23 + 140.26) / 3 = 140.25m
- Standard deviation: 0.015m (excellent repeatability)

### Method 2: Extract from Cross-Section Survey

**If direct water level measurement not collected, extract from cross-section:**

**From cross-section data, identify stations that are at waterline:**
- Waterline stations: Transition from dry (bank) to wet (channel)
- Left waterline: Last dry station on left bank, or first wet station entering water
- Right waterline: First wet station on right bank, or last wet station exiting water

**Example cross-section data:**

```
Station  Distance  Z_bed    Water Depth   Status
-------  --------  -----    -----------   ------
ST1      0m        141.15m  Dry           Bank (above water)
ST2      2m        140.45m  Dry           Bank (above water)
ST3      4m        139.95m  0.30m         WATERLINE (first wet station)
ST4      6m        139.65m  0.60m         Channel (underwater)
ST5      8m        138.75m  1.50m         Channel (underwater)
ST6      10m       139.55m  0.70m         Channel (underwater)
ST7      12m       139.85m  0.40m         Channel (underwater)
ST8      14m       140.35m  Dry           WATERLINE (last wet station)
ST9      16m       141.05m  Dry           Bank (above water)
```

**Calculate water level from waterline stations:**

**At ST3 (first wet station):**
- Bed elevation: Z_bed = 139.95m
- Water depth: d = 0.30m
- Water level: Z_water = Z_bed + d = 139.95 + 0.30 = 140.25m

**At ST8 (last wet station, right waterline):**
- Bed elevation: Z_bed = 140.35m
- Water depth: d = 0.00m (or very shallow, at waterline)
- Water level: Z_water ≈ 140.35m (bed at water level)

**Alternatively, calculate from any underwater station:**

**At ST5 (thalweg, deepest point):**
- Bed elevation: Z_bed = 138.75m
- Water depth: d = 1.50m
- Water level: Z_water = 138.75 + 1.50 = 140.25m

**All methods should yield same water level** (within measurement uncertainty):
- From ST3: Z_water = 140.25m
- From ST5: Z_water = 140.25m
- From ST8: Z_water ≈ 140.35m (or 140.25m, small variation expected at waterline)

**Use average of multiple stations for best estimate.**

### Method 3: Staff Gauge Correlation (If Available)

**If staff gauge installed at site:**

**Staff gauge provides local water level measurement:**
- Staff gauge reading: 1.85m (height above staff gauge zero point)
- Staff gauge zero elevation: 138.40m (surveyed during installation)
- Water level: Z_water = 138.40 + 1.85 = 140.25m

**Survey process establishes relationship between staff gauge and absolute elevation:**

**During survey:**
1. **Read staff gauge:** Record staff gauge reading at survey time (e.g., 1.85m)
2. **Survey water level:** Measure water surface elevation with RTK (e.g., 140.25m)
3. **Survey staff gauge zero:** Measure elevation of staff gauge zero mark (e.g., 138.40m)

**Validate relationship:**
```
Z_water (from RTK) = Z_gauge_zero + gauge_reading
140.25m = 138.40m + 1.85m  ✓ Consistent
```

**For future monitoring:**
- Read staff gauge: 2.15m
- Calculate water level: Z_water = 138.40 + 2.15 = 140.55m
- No RTK needed (staff gauge provides water level directly)

**Staff gauge enables continuous water level monitoring:**
- Manual readings (person visits site, reads gauge, records value)
- Camera-based readings (capture gauge image, extract reading from image)
- Pressure transducer (automated sensor, records depth → converted to elevation)

---

## Coordinate System for Water Level

### Water Level Must Use Same CRS as Survey

**Critical requirement:** Water level elevation MUST be in same coordinate reference system as all other survey data.

**From SURVEY_PROCESS.md Section 1:**
```
CRS: UTM Zone 48 South (EPSG:32748)
```

**All survey measurements in same CRS:**
- Ground control points: EPSG:32748 (UTM 48S)
- Cross-section bed elevations: EPSG:32748
- Water level: EPSG:32748 (same datum, same units)

**Why this matters:**

**Water depth calculation requires consistent elevations:**
```
Water depth = Z_water - Z_bed
```
If Z_water and Z_bed in different coordinate systems, calculation is invalid.

**Example of coordinate system error:**
```
Z_bed = 139.25m (UTM Zone 48S, elevation above WGS84 ellipsoid)
Z_water = 85.3m (elevation above local mean sea level datum)

Water depth = 85.3 - 139.25 = -53.95m (WRONG - nonsensical negative depth)
```

**This error occurs when mixing datums** (ellipsoid heights vs. geoid heights vs. local datums).

**Prevention:**
- Configure SW Maps with correct CRS before survey (EPSG:32748 or appropriate UTM zone)
- Export all data in same CRS (Geopackage preserves CRS metadata)
- Verify CRS when importing to QGIS or other software (should match expected EPSG code)

### Vertical Datum Considerations

**UTM coordinates use ellipsoid heights:**
- Elevation measured from WGS84 reference ellipsoid (mathematical model of Earth's shape)
- NOT measured from mean sea level (geoid)

**Difference between ellipsoid and geoid:**
- Varies by location (0-100m difference)
- Indonesia example: WGS84 ellipsoid ~70m above EGM96 geoid in some areas
- Absolute elevation values different, but RELATIVE elevations consistent

**For OpenRiverCam, absolute elevation values do not matter** - only relative elevations:
- Water depth = Z_water - Z_bed (relative difference)
- Cross-sectional area calculated from relative bed elevations
- Discharge calculation uses relative geometry, not absolute elevations

**As long as ALL measurements use same datum (WGS84 ellipsoid via UTM), calculations are valid.**

**If integrating with external datasets (topographic maps, flood models):**
- Verify datum consistency (WGS84 vs. local datum vs. geoid)
- Apply datum transformation if needed (ellipsoid → geoid conversion)
- Software like QGIS can transform between datums automatically (if CRS defined correctly)

---

## Relating to Staff Gauge (If Present)

### Establishing Staff Gauge Datum

**Staff gauge provides simple, low-cost water level monitoring:**

**Staff gauge characteristics:**
- Physical ruler mounted on stable structure (bridge pier, bank, post)
- Graduations every 1-5cm (easy to read visually)
- Zero point is arbitrary (does not correspond to absolute elevation)

**Survey establishes relationship between staff gauge readings and absolute elevations:**

**Procedure:**

**Step 1: Survey staff gauge zero mark**
- Position rover pole at staff gauge zero mark (bottom graduation)
- RTK measurement: Z_gauge_zero
- Example: Z_gauge_zero = 138.40m (UTM 48S)

**Step 2: Record water level at survey time**
- Read staff gauge: h_gauge = 1.85m
- Survey water surface with RTK: Z_water = 140.25m

**Step 3: Verify consistency**
```
Z_water = Z_gauge_zero + h_gauge
140.25m = 138.40m + 1.85m  ✓ Consistent (within measurement uncertainty)
```

**Step 4: Document relationship**
- Record in survey notes: "Staff gauge zero = 138.40m (EPSG:32748)"
- This datum enables conversion of future gauge readings to absolute elevations

**For operational monitoring:**
```
Read gauge: h_gauge = 2.35m
Calculate elevation: Z_water = 138.40 + 2.35 = 140.75m
```

### Quality Control for Staff Gauge

**Check for gauge movement or settling:**

**During initial survey:**
- Survey gauge zero: Z_gauge_zero = 138.40m
- Gauge reading at time of RTK water level measurement: 1.85m

**During follow-up survey (6 months later):**
- Re-survey gauge zero: Z_gauge_zero = 138.38m (2cm lower than initial survey)
- Indicates gauge has settled or moved

**Solution:**
- Update gauge zero datum to new value (138.38m)
- Or adjust historical data (add 2cm to all readings before gauge movement)

**Check for gauge reading accuracy:**

**Simultaneous RTK and gauge measurements:**
```
RTK water level:         Z_water = 140.52m
Gauge reading:           h_gauge = 2.15m
Calculated from gauge:   Z_calc = 138.40 + 2.15 = 140.55m
Difference:              0.03m (3cm - excellent agreement)
```

Agreement within 2-5cm indicates gauge readable and accurate.

**If large discrepancies (>5cm):**
- Gauge damaged or graduations faded (difficult to read accurately)
- Gauge zero has moved (resurvey needed)
- RTK measurement error (verify quality indicators)

---

## Stage-Discharge Relationship Initiation

### Water Level as Independent Variable

**Rating curve relates water level (stage) to discharge:**
```
Q = f(h)
```
Where:
- Q = discharge (m³/s, dependent variable)
- h = water level or stage (m, independent variable)

**Standard rating curve form (power law):**
```
Q = a × (h - h₀)^b
```
Where:
- a, b = calibration coefficients (determined from discharge measurements)
- h₀ = gauge zero or reference level (elevation where Q = 0)

**Survey provides initial data point for rating curve:**
- Water level at survey: h₁ = 140.25m
- Calculate discharge from survey: Q₁ = v × A (from OpenRiverCam velocity and cross-section area)
- First point on rating curve: (h₁, Q₁)

**Example:**
```
Survey date: 2024-11-14
Water level: h = 140.25m (from survey)
Cross-sectional area: A = 6.65 m² (from cross-section bathymetry at h = 140.25m)
Mean velocity: v = 0.65 m/s (from OpenRiverCam measurement)
Discharge: Q = v × A = 0.65 × 6.65 = 4.3 m³/s

Rating curve data point: (140.25m, 4.3 m³/s)
```

### Building Rating Curve Over Time

**Single survey provides one data point** - rating curve requires multiple points across range of water levels.

**Operational monitoring collects additional data points:**

**Week 1 (survey condition):**
- Water level: 140.25m
- Discharge: 4.3 m³/s

**Week 3 (higher flow after rain):**
- Water level: 140.55m (measured with staff gauge or RTK)
- Cross-sectional area: A = 8.2 m² (calculate from surveyed bathymetry at h = 140.55m)
- Mean velocity: 0.72 m/s (OpenRiverCam)
- Discharge: Q = 0.72 × 8.2 = 5.9 m³/s

**Week 5 (low flow, dry weather):**
- Water level: 140.05m
- Cross-sectional area: A = 5.1 m²
- Mean velocity: 0.55 m/s
- Discharge: Q = 0.55 × 5.1 = 2.8 m³/s

**Week 8 (moderate flow):**
- Water level: 140.35m
- Cross-sectional area: A = 7.0 m²
- Mean velocity: 0.68 m/s
- Discharge: Q = 0.68 × 7.0 = 4.8 m³/s

**Plot rating curve:**
```
Stage-Discharge Rating Curve

Discharge Q (m³/s)
    6 |                    •
      |
    5 |              •
      |
    4 |         •
      |
    3 |    •
      |
    2 |_____|_____|_____|_____|
      140.0  140.2  140.4  140.6
           Water Level h (m)
```

**Fit power law curve through points:**
```
Q = a × (h - h₀)^b
Fitted: Q = 245 × (h - 139.50)^1.85
```

**Use rating curve for future discharge estimates:**
- Measure water level: h = 140.40m (staff gauge or pressure sensor)
- Calculate discharge: Q = 245 × (140.40 - 139.50)^1.85 = 5.2 m³/s
- No velocity measurement needed (rating curve provides Q from h directly)

---

## Documentation for Rating Curve Development

### Survey Documentation Requirements

**For rating curve development, document:**

**Water level at survey:**
- Elevation: Z_water = 140.25m
- Coordinate system: EPSG:32748 (UTM Zone 48S)
- Measurement method: RTK GNSS, direct water surface survey
- Date and time: 2024-11-14, 14:35 local time
- Flow conditions: "Moderate flow, slight ripples on surface"

**Cross-section at survey water level:**
- Cross-section ID: XS1
- Wetted width: 10.0m (from ST3 to ST8)
- Cross-sectional area: A = 6.65 m² (calculated from bed elevations and h = 140.25m)
- Wetted perimeter: 12.5m

**Discharge at survey (if velocity measured):**
- Mean velocity: v = 0.65 m/s (OpenRiverCam measurement or current meter)
- Discharge: Q = v × A = 0.65 × 6.65 = 4.3 m³/s
- Measurement uncertainty: ±10-15% (typical for velocity-area method)

**Staff gauge datum (if present):**
- Gauge zero elevation: Z_gauge_zero = 138.40m (EPSG:32748)
- Gauge reading at survey: 1.85m
- Verification: Z_water = Z_gauge_zero + gauge_reading = 138.40 + 1.85 = 140.25m ✓

**Range of validity:**
- Minimum surveyed water level: 140.05m (lowest cross-section station still wet)
- Maximum surveyed water level: 141.00m (top of bank stations, before overbank flow)
- Rating curve valid within this range (140.05m to 141.00m)
- Extrapolation beyond range introduces uncertainty

### Data Archive for Long-Term Monitoring

**Create permanent archive of survey data:**

**Files to archive:**
- `site_YYYYMMDD_water_level.csv` - Water level measurements
- `site_YYYYMMDD_cross_section.csv` - Cross-section bathymetry
- `site_YYYYMMDD_survey_notes.pdf` - Field notebook scans
- `site_YYYYMMDD_photos.zip` - Survey photos
- `site_staff_gauge_datum.txt` - Staff gauge datum documentation

**Documentation template (staff_gauge_datum.txt):**
```
STAFF GAUGE DATUM DOCUMENTATION
Site: [Site name and location]
Survey Date: 2024-11-14
Surveyor: [Name]
Coordinate System: EPSG:32748 (WGS 84 / UTM Zone 48S)

STAFF GAUGE ZERO ELEVATION:
Easting: 685435.20m
Northing: 9456781.50m
Elevation: 138.40m
Measurement method: RTK GNSS, 60s averaging, FIX solution

VERIFICATION MEASUREMENT:
Water level (RTK): 140.25m
Gauge reading: 1.85m
Calculated: 138.40 + 1.85 = 140.25m ✓ Consistent

CONVERSION FORMULA:
Water_level (m, EPSG:32748) = 138.40 + Gauge_reading (m)

NOTES:
Staff gauge mounted on bridge pier, north side.
Graduations readable to ±2cm.
Gauge secured with stainless steel bolts.
Inspect annually for movement or damage.
```

**This documentation enables:**
- Future resurvey and comparison (has gauge moved?)
- Rating curve development (water level → discharge)
- Integration with other monitoring data (water level time series)
- Long-term trend analysis (channel morphology changes)

---

## Quality Control for Water Level Data

### Verification Checks

**Check 1: Water level above all wetted bed elevations**

**Expected:** Z_water > Z_bed for all underwater cross-section stations

**Verification:**
- Filter cross-section data: Z_bed > Z_water (should be zero results for underwater stations)
- Any underwater station with Z_bed > Z_water indicates error

**Example:**
```
Station  Z_bed    Z_water  Depth     Status
-------  -----    -------  -----     ------
ST3      139.95m  140.25m  +0.30m    ✓ OK (bed below water)
ST4      139.65m  140.25m  +0.60m    ✓ OK
ST5      138.75m  140.25m  +1.50m    ✓ OK
ST6      141.50m  140.25m  -1.25m    ✗ ERROR (bed above water, but station marked as wet)
```

ST6 error indicates:
- Pole height error (bed elevation calculation wrong)
- Water level error (Z_water too low)
- Station misclassified (ST6 actually dry, not wet)

**Check 2: Water level below all dry bank stations**

**Expected:** Z_water < Z_bed for all dry stations (banks above waterline)

**Verification:**
- Filter dry stations: Z_bed < Z_water (should be zero results)
- Bank stations should be above water level

**Check 3: Consistency across multiple measurements**

**If multiple water level measurements taken:**
- Calculate standard deviation
- Expected: σ < 5cm (excellent), σ < 10cm (acceptable)
- Large standard deviation (>10cm) indicates:
  - Water surface moving (waves, ripples, turbulence)
  - Measurement errors (pole not at surface, RTK losing FIX)
  - Water level changing during survey (long survey time, flow increasing/decreasing)

**Check 4: Staff gauge consistency**

**If staff gauge present:**
```
Z_water (RTK) = Z_gauge_zero + gauge_reading

Expected difference: < 5cm
```

Large discrepancy indicates:
- Gauge zero elevation surveyed incorrectly
- Gauge reading recorded incorrectly
- Gauge has moved since zero was surveyed

---

## Common Issues and Solutions

### Issue: Water Level Changes During Survey

**Symptom:** Water level measurements at beginning vs. end of survey differ by >5cm

**Cause:**
- Flow increasing (storm runoff arriving)
- Flow decreasing (recession after rain event)
- Tidal influence (coastal rivers)

**Solutions:**
- Record time with each measurement
- Use water level at mid-survey as representative value
- Or calculate time-averaged water level
- Document in notes: "Water level rising approximately 3cm/hour during survey"

**Impact on cross-sectional area:**
- Rising water: Wetted area larger at end of survey than beginning
- Calculate area at average water level
- Or note uncertainty: "Cross-sectional area = 6.65 ± 0.3 m² (due to water level change during survey)"

### Issue: Waves and Ripples on Water Surface

**Symptom:** Difficult to measure stable water surface (surface moving up/down)

**Solutions:**
- Average multiple measurements (ripples average out)
- Extend averaging time (120-180 seconds instead of 60 seconds)
- Measure in calm area (eddy behind obstacle, slack water near bank)
- Measure average between wave crest and trough

**Typical uncertainty:** ±2-5cm due to surface waves (acceptable for most purposes)

### Issue: No Staff Gauge at Site

**Symptom:** Cannot measure water level during routine monitoring (no RTK available for repeated visits)

**Solutions:**
- Install staff gauge during survey (permanent water level reference)
- Use pressure transducer (automated sensor, records water level continuously)
- Reference to fixed structure (mark bridge pier, record elevation, measure depth from mark to water)
- Document water level photographically (ruler or measuring tape in photo)

**For rating curve development:**
- Need water level for each discharge measurement
- Without staff gauge or sensor, must use RTK for every measurement (equipment-intensive)
- Staff gauge installation highly recommended (low cost, enables frequent measurements)

---

## Summary: Water Level Calculation

**Purpose:**
- Establish water surface elevation at time of survey
- Provide reference for calculating water depths and wetted area
- Initiate stage-discharge relationship for rating curve
- Enable operational discharge monitoring

**Key measurements:**
- Water surface elevation: Z_water (m, in same CRS as survey)
- Staff gauge datum: Z_gauge_zero (if gauge present)
- Gauge reading at survey time (verification)

**Calculation methods:**
1. Direct measurement: Z_water = Z_antenna - h_pole_water (pole tip at surface)
2. From cross-section: Z_water = Z_bed + water_depth (any underwater station)
3. From staff gauge: Z_water = Z_gauge_zero + gauge_reading

**Coordinate system:**
- MUST use same CRS as all survey data (e.g., EPSG:32748)
- UTM elevations are ellipsoid heights (WGS84), not mean sea level
- Consistency ensures valid water depth and area calculations

**Rating curve foundation:**
- Survey provides first (h, Q) data point
- Operational monitoring adds more points at different water levels
- Fit curve: Q = f(h), use for future discharge estimates from water level alone

**Quality control:**
- Z_water > Z_bed for all underwater stations
- Z_water < Z_bed for all dry bank stations
- Multiple measurements consistent (σ < 5-10cm)
- Staff gauge measurements verify RTK water level

**Documentation:**
- Water level elevation and timestamp
- Staff gauge datum (if present)
- Flow conditions
- Measurement method and uncertainty

**Workflow position:**
- **COMPLETED:** Pole height adjustment (Section 9.12)
- **CURRENT:** Water level calculation
- **NEXT:** UTM and XYZ conversion (Section 9.14, prepare data for PtBox)

With water level established, you can calculate water depths, wetted areas, and initiate rating curve development - connecting surveyed bathymetry to operational discharge monitoring.

---

**Next Section:** [9.14 Survey Data Processing - UTM and XYZ Conversion](14-utm-xyz-conversion.md)
