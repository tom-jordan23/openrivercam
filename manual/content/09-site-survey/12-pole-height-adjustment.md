# 9.12 Survey Data Processing - Pole Height Adjustment

This section covers the post-survey calculation of true bed elevations from surveyed rover positions. During field survey, the RTK rover antenna measures its own position in space, not the position of the channel bed. Converting antenna elevation to bed elevation requires accounting for pole height - the distance from the pole tip on the bed to the antenna reference point.

Pole height adjustment is the first and most fundamental data processing step. Without this correction, your survey data represents antenna positions floating in space above the channel, not the actual bed elevations needed for discharge calculations and topographic analysis.

By the end of this section, you will understand:
- Why pole height correction is essential
- How to calculate bed elevation from surveyed points
- How pole height was measured during field survey
- How to verify pole height corrections are applied correctly
- Common errors and how to detect them
- Quality control checks for bed elevation data

**Reference:** SURVEY_PROCESS.md Section 10 - PPP & Data Processing

---

## Why Pole Height Correction is Needed

### What RTK Measures vs. What We Need

**RTK GNSS measures the position of the antenna reference point (ARP):**

The rover antenna sits atop a survey pole. When RTK achieves FIX and calculates a position, it reports the 3D coordinates of the antenna reference point:
- Easting: E_antenna (e.g., 685432.15m)
- Northing: N_antenna (e.g., 9456782.33m)
- Elevation: Z_antenna (e.g., 142.10m)

**What we need for OpenRiverCam is the position of points on the ground or channel bed:**
- Ground control point elevation: Z_gcp (elevation of survey marker on bank)
- Bed elevation: Z_bed (elevation of river bed at cross-section station)
- Water level elevation: Z_water (elevation of water surface)

**The antenna is NOT touching the ground or bed** - it is elevated on a survey pole:

```
                [ANTENNA] ← RTK measures this position (Z_antenna = 142.10m)
                    |
                    |
                    | ← Pole height (h_pole = 2.85m)
                    |
                    |
        ============|============ Water surface
                    |
                    |
                    * ← Pole tip on bed - THIS is what we need (Z_bed = ?)
```

**The difference between Z_antenna and Z_bed is the pole height (h_pole).**

### The Pole Height Correction Equation

**For any surveyed point, the bed elevation is:**

```
Z_bed = Z_antenna - h_pole
```

Where:
- **Z_bed** = Elevation of bed or ground (what we need for analysis)
- **Z_antenna** = Elevation of antenna reference point (what RTK measured)
- **h_pole** = Pole height, measured from pole tip to antenna (vertical distance)

**Example calculation:**

During cross-section survey, Station 5:
- RTK measurement: E_antenna = 685432.15m, N_antenna = 9456782.33m, Z_antenna = 142.10m
- Pole height measured with tape: h_pole = 2.85m
- Bed elevation: Z_bed = 142.10 - 2.85 = 139.25m

**This 2.85m correction is essential** - without it, your "bed elevation" would be 142.10m (wrong by nearly 3 meters, rendering data useless for discharge calculations).

### Why Pole Height Varies Between Points

**Pole height is NOT constant throughout survey** - it varies from point to point based on local conditions.

**Factors that cause pole height variation:**

**Water depth variation:**
- Deep water station: Pole extended longer to reach bed through water (h_pole = 3.5m)
- Shallow water station: Pole partially retracted (h_pole = 2.2m)
- Dry bank station: Pole at minimum extension (h_pole = 2.0m)

**Operator height and comfort:**
- Tall operator: May extend pole higher for comfortable handling
- Short operator: May use shorter pole extension
- Different operators during same survey: Pole heights vary between crew members

**Terrain variation:**
- Survey from high bank: Pole extended to reach lower ground (h_pole = 3.8m)
- Survey on flat ground: Pole at standard extension (h_pole = 2.3m)

**Example pole height variation across cross-section:**

```
Station  Location      Terrain           h_pole   Z_antenna   Z_bed
------   ---------     ---------------   ------   ---------   -----
ST1      Left bank     High bank         2.15m    141.30m     139.15m
ST2      Bank slope    Descending slope  2.35m    141.60m     139.25m
ST3      Waterline     Shallow water     2.65m    142.25m     139.60m
ST4      Channel       Mid depth         2.95m    142.55m     139.60m
ST5      Thalweg       Deep water        3.45m    142.20m     138.75m
ST6      Channel       Mid depth         2.85m    142.40m     139.55m
ST7      Waterline     Shallow water     2.55m    142.40m     139.85m
ST8      Bank slope    Rising slope      2.25m    142.60m     140.35m
ST9      Right bank    High bank         2.05m    143.10m     141.05m
```

**Pole height varies from 2.05m to 3.45m** across this 9-station transect. Using a single "average" pole height would introduce errors of 0.5-1.0m in bed elevations (unacceptable for discharge calculations).

**The fundamental rule: Measure and record pole height at EVERY surveyed point.**

---

## Pole Height Measurement Technique

### Field Measurement Procedure

**From SURVEY_PROCESS.md Section 8:**
> Measure pole height tip-to-ARP each shot

**Standard procedure used during field survey:**

**Step 1: Position pole tip on bed or ground**
- Lower pole until tip rests firmly on bed (or ground for GCPs, banks)
- Push tip firmly but not excessively (avoid pushing into soft sediment)
- Keep pole vertical (bubble level centered)

**Step 2: Measure from pole tip to antenna reference point**
- Use tape measure or ruler
- Start at pole tip (bottom of pole where it contacts bed)
- Measure upward along pole to antenna reference point
- Read measurement to nearest centimeter (e.g., 2.85m)

**Step 3: Record immediately in field notebook**
- Write down pole height before moving to next station
- Label clearly: "ST5: h_pole = 2.85m"
- Prevents confusion between measurements from different stations

**Step 4: Enter into SW Maps attributes**
- Fill in pole_height attribute field: 2.85
- This preserves pole height with the surveyed point data
- Enables automated calculation of bed elevations in post-processing

**Common pole height measurement errors and prevention:**

**Error: Reading tape measure incorrectly**
- Tape measure may have end hook or zero offset
- Solution: Verify tape zero point (some tapes start at 1cm, not 0cm)
- Double-check reading before recording

**Error: Measuring to wrong reference point on antenna**
- Antennas have multiple features (bottom, center, connector)
- Antenna Reference Point (ARP) is typically bottom center of antenna
- Solution: Check antenna specifications for ARP location, measure consistently to same point

**Error: Pole not vertical during measurement**
- If pole tilted, measured length > true vertical height
- Solution: Level pole with bubble before measuring, measure along pole axis

**Error: Recording wrong value or transposing digits**
- Writing 3.25m instead of 2.35m
- Solution: Read measurement twice, verify recorded value makes sense (compare to previous stations)

### Recording Pole Height in SW Maps

**SW Maps attribute configuration (from Section 9.5 setup):**

**For cross-section points:**
- Attribute field name: `pole_height`
- Data type: Decimal (meters)
- Required: YES (cannot leave blank)
- Example value: 2.85

**For ground control points:**
- Same `pole_height` field
- Typically shorter values (GCPs on stable ground, not in deep water)
- Example values: 1.95m to 2.50m

**For water level measurements:**
- `pole_height` field critical for calculating water surface elevation
- Record pole height to water surface, not to bed (if measuring from surface)
- Or record pole height to bed and separate water depth measurement

**Attribute entry during survey:**
- Fill in immediately after measuring (while value fresh in mind)
- Verify value entered correctly (re-read from notebook)
- SW Maps saves attribute with point coordinates (preserved in export)

---

## Calculating Bed Elevations

### Post-Survey Calculation Process

**After exporting data from SW Maps, calculate bed elevations for all points:**

**Option 1: Spreadsheet calculation (CSV export)**

**Step 1: Export survey data from SW Maps**
- Export as CSV format
- Columns include: point_id, x_coord, y_coord, z_coord, pole_height, ...

**Step 2: Open in spreadsheet software (Excel, LibreOffice Calc)**
- Import CSV file
- Verify columns imported correctly

**Step 3: Add bed_elevation column**
- Insert new column: "bed_elevation"
- Formula: `=z_coord - pole_height`
- Example for row 2: `=D2 - E2` (if z_coord in column D, pole_height in column E)

**Step 4: Apply formula to all rows**
- Copy formula down entire column (all surveyed points)
- Verify calculations: Spot-check several rows manually

**Step 5: Save corrected data**
- Save as new CSV file: `site_survey_bed_elevations.csv`
- Preserve original export (never overwrite raw data)

**Example spreadsheet layout:**

```
point_id    x_coord      y_coord       z_coord   pole_height   bed_elevation
--------    ---------    ----------    -------   -----------   -------------
XS1_ST1     685430.15    9456780.22    141.30    2.15          =C2-D2  → 139.15
XS1_ST2     685432.20    9456780.45    141.60    2.35          =C3-D3  → 139.25
XS1_ST3     685434.25    9456780.68    142.25    2.65          =C4-D4  → 139.60
XS1_ST4     685436.30    9456780.91    142.55    2.95          =C5-D5  → 139.60
XS1_ST5     685438.35    9456781.14    142.20    3.45          =C6-D6  → 138.75
...
```

**Option 2: QGIS Field Calculator (Geopackage export)**

**Step 1: Import Geopackage into QGIS**
- SW Maps can export directly as Geopackage (preserves CRS and geometry)
- QGIS: Layer → Add Layer → Add Vector Layer → select .gpkg file
- Verify CRS correct (should be EPSG:32748 or appropriate UTM zone)

**Step 2: Open Attribute Table**
- Right-click layer → Open Attribute Table
- Verify pole_height column exists and populated

**Step 3: Open Field Calculator**
- Attribute Table toolbar → Open Field Calculator button
- Check "Create new field"

**Step 4: Define bed_elevation field**
- Output field name: `bed_elevation`
- Output field type: Decimal number (real)
- Precision: 2 decimal places (e.g., 139.25)

**Step 5: Enter calculation expression**
```
"z_coord" - "pole_height"
```
Or if using geometry Z value:
```
z($geometry) - "pole_height"
```

**Step 6: Execute calculation**
- Click OK
- QGIS calculates bed_elevation for all features
- New column appears in Attribute Table

**Step 7: Verify calculations**
- Sort by bed_elevation (check for anomalies)
- Spot-check several features (manual calculation vs. QGIS result)

**Step 8: Save changes**
- Click Save Edits (pencil icon in Attribute Table toolbar)
- Changes saved to Geopackage layer

---

## Quality Control and Verification

### Verifying Pole Height Corrections

**After calculating bed elevations, perform these quality checks:**

**Check 1: Bed elevations lower than antenna elevations**

**Expected:** Z_bed < Z_antenna (bed elevation must be lower than antenna elevation)
**Reason:** Pole height is positive (antenna above bed), so Z_bed = Z_antenna - h_pole must be less than Z_antenna

**Verification:**
- Filter or sort data: Z_bed > Z_antenna (should return zero results)
- If any points have Z_bed > Z_antenna: ERROR - pole height recorded as negative or correction applied incorrectly

**Common cause of this error:**
- Formula reversed: `bed_elevation = pole_height - z_coord` (WRONG - should be z_coord - pole_height)
- Pole height recorded as negative value (should always be positive)

**Check 2: Bed elevation range is reasonable**

**Expected:** Bed elevations should vary smoothly across site, within reasonable range

**Verification:**
- Calculate min and max bed elevations
- Example site: Z_bed ranges from 138.5m to 141.2m (2.7m total relief, reasonable for river channel)
- If range excessive (e.g., 50m range): ERROR - likely data entry error or coordinate system issue

**Common causes:**
- One or more points measured in wrong coordinate system (mixed WGS84 geographic with UTM)
- Pole height for one point recorded in feet instead of meters (3.28× too large)
- Typo in pole height (30.5m instead of 3.05m)

**Check 3: Cross-section profile is smooth and logical**

**Expected:** Bed elevations should vary smoothly along cross-section (no sudden jumps)

**Verification:**
- Plot cross-section profile (distance from left bank vs. bed elevation)
- Visual inspection: Profile should show smooth channel shape (V-shaped, U-shaped, trapezoidal)
- Identify outliers: Any station with bed elevation drastically different from neighbors

**Example anomaly detection:**
```
Station  Distance  bed_elevation   Notes
-------  --------  -------------   -----
ST3      4m        139.60m         OK
ST4      6m        139.60m         OK
ST5      8m        141.25m         ERROR - 1.65m higher than neighbors (thalweg should be deepest, not highest)
ST6      10m       139.55m         OK
ST7      12m       139.85m         OK
```

**If ST5 should be deepest point (thalweg):**
- Expected: Z_bed ≈ 138.75m (lower than neighbors)
- Actual: Z_bed = 141.25m (much higher than neighbors)
- Diagnosis: Pole height error (recorded 0.50m instead of 3.50m, difference of 3.0m)
- Solution: Check field notebook for ST5 pole height, correct and recalculate

**Check 4: Water depths match field observations**

**Expected:** Calculated water depths should match water depths observed and recorded during survey

**Verification:**
- Calculate water depths: d_calculated = Z_water - Z_bed
- Compare to recorded water depths from field notes (observed water level on pole)
- Agreement should be within 10-20cm (accounting for measurement uncertainty)

**Example verification:**

```
Station  Z_water   Z_bed    d_calculated   d_observed   Difference
-------  -------   -----    ------------   ----------   ----------
ST3      140.25m   139.60m  0.65m          0.60m        0.05m  ✓ OK
ST4      140.25m   139.60m  0.65m          0.70m        0.05m  ✓ OK
ST5      140.25m   138.75m  1.50m          1.45m        0.05m  ✓ OK
ST6      140.25m   139.55m  0.70m          0.75m        0.05m  ✓ OK
```

All differences < 10cm: Pole height corrections verified correct.

**If large discrepancies (>20cm):**
- Pole height measurement error (tape misread)
- Pole tip pushed into soft sediment (bed elevation overestimated)
- Water level changed between stations (if survey took several hours)
- Water depth recorded incorrectly in field notes

---

## Common Errors and Troubleshooting

### Error 1: Pole Height Not Recorded

**Symptom:** `pole_height` field empty or zero for some points

**Impact:** Cannot calculate bed elevation for affected points (missing critical data)

**Causes:**
- Operator forgot to measure pole height during survey
- Pole height measured but not entered into SW Maps attributes
- Attribute field not configured in SW Maps project

**Solutions:**

**If field notebook has pole heights:**
- Manually enter pole heights from field notes into exported data
- Update Geopackage or CSV file
- Recalculate bed elevations

**If pole heights not recorded anywhere:**
- Affected points cannot be corrected (data unusable for bed elevations)
- Options:
  - Re-survey affected points (if site accessible)
  - Interpolate pole heights from neighboring points (less accurate but may be acceptable)
  - Discard affected points if redundant (e.g., extra cross-section stations)

**Prevention:**
- Configure SW Maps layers with REQUIRED pole_height attribute (prevents saving point without it)
- Standardize field procedure: Measure pole height, enter attribute, then save point (always in this order)
- Quality check during survey: Periodically verify pole_height field populated for recent points

### Error 2: Pole Height in Wrong Units

**Symptom:** Bed elevations drastically wrong (3.28× too high or too low)

**Impact:** All bed elevations incorrect, unusable for analysis

**Cause:** Pole height recorded in feet instead of meters (or vice versa)
- Example: Pole height is 9.5 feet (2.9m), but recorded as 9.5 in meters field
- Result: Z_bed = 142.10 - 9.50 = 132.60m (should be 142.10 - 2.90 = 139.20m, error of 6.6m)

**Detection:**
- Bed elevations far too low (if pole height mistakenly in feet, appears 3.28× larger)
- Bed elevations slightly too high (if pole height mistakenly in meters, actually feet, appears 3.28× smaller)

**Solution:**
- Verify pole measurement units used during survey (check field notebook, ask operator)
- If in feet: Convert to meters (h_meters = h_feet / 3.28084)
- Recalculate all bed elevations with corrected pole heights

**Prevention:**
- Label attribute field clearly: `pole_height_m` (indicates meters)
- Brief crew: "All measurements in meters, including pole heights"
- Use metric tape measures (avoid feet/inches tapes)

### Error 3: Inconsistent Antenna Reference Point

**Symptom:** Bed elevations vary erratically despite smooth terrain

**Impact:** Bed elevations have systematic errors (offset by 5-15cm between portions of survey)

**Cause:** Pole height measured to different reference points on antenna
- First operator measured to bottom of antenna (ARP)
- Second operator measured to center of antenna (5cm higher)
- Result: Second operator's bed elevations systematically 5cm too high

**Detection:**
- Bed elevations show step change where operators changed
- Cross-section profile has discontinuity (jump in bed elevation mid-transect)

**Solution:**
- Determine which reference point is correct (usually bottom of antenna = ARP)
- Adjust pole heights for affected portion (add or subtract offset)
- Recalculate bed elevations

**Prevention:**
- Brief all operators: Show them antenna ARP location, standardize measurement technique
- Mark antenna reference point with tape or paint (visible indicator)
- First-time operators: Supervisor verifies pole height measurement technique before independent work

### Error 4: Pole Height Correction Formula Reversed

**Symptom:** Bed elevations are above antenna elevations (physically impossible)

**Impact:** All bed elevations completely wrong (unusable)

**Cause:** Formula applied as `bed_elevation = pole_height - z_coord` instead of `z_coord - pole_height`

**Detection:**
- All bed elevations greater than antenna elevations (Z_bed > Z_antenna)
- Immediate red flag (check this FIRST after calculation)

**Solution:**
- Correct formula: `bed_elevation = z_coord - pole_height` (antenna minus pole height)
- Recalculate entire dataset with correct formula

**Prevention:**
- Document correct formula clearly in processing procedures
- Verify formula on first few points before batch-applying to all data
- Sanity check: Z_bed must always be less than Z_antenna

---

## Summary: Pole Height Adjustment

**Purpose:**
- Convert RTK antenna elevations to bed/ground elevations
- Essential first step in survey data processing
- Enables calculation of true bed elevations, water depths, cross-sectional areas

**Key principle:**
```
bed_elevation = antenna_elevation - pole_height

Z_bed = Z_antenna - h_pole
```

**Critical requirements:**
- Pole height must be measured at EVERY surveyed point (varies throughout survey)
- Pole height measured from pole tip (on bed/ground) to antenna reference point (ARP)
- Pole height recorded immediately in SW Maps attributes (preserved with point data)
- Calculation performed in post-processing (spreadsheet or QGIS Field Calculator)

**Quality control checks:**
1. Z_bed < Z_antenna for all points (bed lower than antenna)
2. Bed elevation range reasonable for site (no extreme outliers)
3. Cross-section profiles smooth and logical (no sudden jumps)
4. Calculated water depths match field observations (within 10-20cm)

**Common errors:**
- Pole height not recorded (cannot calculate bed elevation)
- Pole height in wrong units (feet vs. meters)
- Inconsistent antenna reference point (systematic offset)
- Formula reversed (bed elevation > antenna elevation)

**Workflow position:**
- **COMPLETED:** Field survey (RTK antenna elevations and pole heights measured)
- **CURRENT:** Pole height adjustment (calculate bed elevations)
- **NEXT:** Water level calculation (Section 9.13, determine water surface elevation)

With pole height corrections applied, your survey data represents true bed and ground elevations - the foundation for all subsequent analysis (water depths, cross-sectional areas, discharge calculations, topographic mapping).

---

**Next Section:** [9.13 Survey Data Processing - Water Level Calculation](13-water-level-calculation.md)
