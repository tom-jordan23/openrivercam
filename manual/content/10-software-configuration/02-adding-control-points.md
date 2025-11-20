# 10.2 Configuring the PtBox - Adding Control Points

This section covers the most critical configuration step: establishing the coordinate transformation that converts camera pixels to real-world meters. Ground Control Points (GCPs) surveyed in Section 9.8 now connect image space to physical space, enabling accurate velocity and discharge measurements.

Adding control points means identifying each surveyed GCP in the sample video, entering its surveyed coordinates, and allowing the PtBox to calculate the mathematical transformation. The quality of this transformation determines the accuracy of all subsequent measurements.

By the end of this section, you will be able to:
- Import or enter surveyed GCP coordinates into PtBox
- Locate each GCP in the sample video frame
- Precisely identify GCP pixel positions
- Associate image points with surveyed coordinates
- Calculate the coordinate transformation
- Verify transformation quality using reprojection error
- Identify and resolve problematic GCPs
- Save the transformation configuration for operational use

**Reference:** Builds directly on Section 9.8 (GCP Survey) and Section 4.1 (Coordinate Transformation Concepts).

---

## Understanding the GCP Configuration Process

### What This Step Accomplishes

**From Section 4.1, recall the transformation concept:**

**Two coordinate systems must be connected:**
1. **Image coordinate system:** Pixel positions (u, v) in camera image
2. **Real-world coordinate system:** Physical positions (X, Y, Z) in meters

**GCPs provide the connection:**
- Each GCP exists in both systems simultaneously
- In image: GCP appears at specific pixel position (u, v)
- In real world: GCP surveyed at specific physical position (X, Y, Z)
- Multiple GCPs provide enough information to calculate mathematical relationship between the two systems

**Configuration workflow:**
1. **Load surveyed GCP coordinates** (X, Y, Z from Section 9.8 survey)
2. **Identify each GCP in sample video** (determine pixel position u, v for each GCP)
3. **Create GCP pairs** (match surveyed coordinates to image positions)
4. **Calculate transformation** (software computes mathematical formulas converting pixels to meters)
5. **Verify transformation quality** (check reprojection error for each GCP)
6. **Refine if needed** (remove problematic GCPs or improve identification accuracy)
7. **Save transformation** (persist for operational velocity measurements)

### Minimum Requirements Review

**From Section 4.1:**

**Number of GCPs:**
- **Absolute minimum:** 4 GCPs (mathematically necessary for homography calculation)
- **Practical minimum:** 6 GCPs (allows error checking via overdetermination)
- **Recommended:** 8-10 GCPs (provides better accuracy, redundancy, and error detection)

**GCP distribution:**
- Spread throughout camera field of view (near/far, left/right)
- Cover monitoring area where velocity measurements occur
- Sufficient vertical spread (different elevations for depth information)

**Survey quality:**
- GCP coordinates surveyed to 2-3 cm accuracy (RTK GPS, Section 9.8)
- Consistent coordinate reference system (all GCPs in same CRS)
- Accurate pole height measurements (ensures Z coordinates correct)

**Image quality:**
- All GCPs clearly visible in sample video
- GCP markers identifiable (can point to precise location)
- Video captured under similar conditions to operational monitoring

**If any requirement not met, transformation quality will suffer.**

---

## Preparing GCP Data for Import

### Exporting GCP Coordinates from SW Maps

**From Section 9.8 survey, GCP data stored in SW Maps:**

**Export procedure:**

1. **Open SW Maps project containing GCP survey data**
2. **Select Ground Control Points layer** (layer used during GCP survey)
3. **Export layer to CSV or GeoPackage format:**
   - SW Maps menu → Export → Select format (CSV recommended for simplicity)
   - Choose fields to export: point_id, X coordinate, Y coordinate, Z coordinate (minimum required)
   - Additional useful fields: description, visibility, h_precision, v_precision
4. **Save export file** with clear filename: `GCPs_Site01_20241115.csv`
5. **Transfer file to configuration device** (laptop used for PtBox configuration)

**CSV format example:**
```
point_id,X,Y,Z,description,visibility
GCP1,685445.23,9456795.47,142.15,Left bank orange X on rock,Clear
GCP2,685447.85,9456798.22,141.98,Left bank painted circle,Clear
GCP3,685452.10,9456796.80,140.45,Mid-channel floating target,Partial
GCP4,685458.32,9456795.15,141.75,Right bank survey stake,Clear
GCP5,685460.15,9456792.50,142.30,Right bank rock outcrop,Clear
GCP6,685448.50,9456802.10,141.20,Upstream left bank marker,Clear
GCP7,685455.80,9456801.90,140.95,Upstream mid-channel,Clear
GCP8,685461.20,9456800.45,141.50,Upstream right bank,Clear
```

**Coordinate reference system (CRS) verification:**
- Verify CRS used for survey: Typically UTM zone (e.g., UTM Zone 48S, WGS84)
- PtBox must be configured to use same CRS
- If CRS mismatch, coordinates will be misinterpreted (transformation will fail)
- Check SW Maps project settings for CRS information
- Document CRS in export filename or accompanying notes: `GCPs_UTM48S_WGS84.csv`

### Verifying Data Quality Before Import

**Before loading into PtBox, quality check GCP data:**

**Completeness check:**
- [ ] All surveyed GCPs included in export (GCP1 through GCP8, etc.)
- [ ] No missing coordinates (each GCP has X, Y, Z values)
- [ ] Point IDs match numbering from annotated photo (Section 9.8)

**Coordinate sanity check:**
- [ ] X and Y coordinates reasonable for site location (check against known coordinates)
- [ ] Z coordinates (elevations) reasonable (within expected range for site)
- [ ] No obvious typos (coordinates off by factor of 10 or with decimal point errors)

**Coordinate range check:**
```
Example sanity check for UTM coordinates:
X (Easting): Should vary by 10-50m across site (e.g., 685445 to 685461)
Y (Northing): Should vary by 5-20m across site (e.g., 9456792 to 9456802)
Z (Elevation): Should vary by 1-5m across site (e.g., 140.45 to 142.30)

If X coordinates span 5000m, likely error (decimal point misplaced or wrong units)
If all Z coordinates identical, likely error (pole height not applied correctly)
```

**If data quality issues identified:**
- Return to SW Maps, verify export settings
- Check original survey data for errors
- Re-export with corrections
- Do not proceed to import until data verified correct

---

## Loading GCP Coordinates into PtBox

### Accessing GCP Configuration Interface

**In PtBox web interface (from Section 10.1):**

1. **Navigate to Ground Control Points section:**
   - Configuration menu → Calibration → Ground Control Points
   - Or Camera Setup → GCPs
   - Or similar navigation depending on interface version

2. **Verify sample video still loaded:**
   - Video preview should display with correct orientation (from Section 10.1)
   - If video not showing, reload sample video

3. **Access GCP import/entry interface:**
   - Look for "Import GCPs", "Add Control Points", or "Load GCP Coordinates" button
   - Interface typically provides two options:
     - **File import:** Upload CSV or GeoPackage file
     - **Manual entry:** Type coordinates directly into form

### Importing from CSV File (Recommended)

**If interface supports file import:**

1. **Click "Import GCPs" or "Load from File" button**

2. **Select GCP CSV file:**
   - Browse to file location: `GCPs_Site01_20241115.csv`
   - Click "Open" or "Upload"

3. **Map CSV columns to PtBox fields:**
   - Interface may display column mapping dialog
   - Match CSV columns to required fields:
     - CSV "point_id" → PtBox "GCP ID"
     - CSV "X" → PtBox "Easting" or "X coordinate"
     - CSV "Y" → PtBox "Northing" or "Y coordinate"
     - CSV "Z" → PtBox "Elevation" or "Z coordinate"
   - Verify units: Meters (typically default)
   - Verify CRS: Must match survey data CRS (e.g., UTM Zone 48S, WGS84)

4. **Preview imported data:**
   - Interface typically shows table of imported GCPs
   - Review for completeness and accuracy
   - Check that point IDs, coordinates display correctly

5. **Confirm import:**
   - Click "Import", "Accept", or "Load" to complete import
   - GCPs now stored in PtBox configuration

**If import fails:**
- Check CSV file format (correct column headers, no extra commas)
- Verify file encoding (UTF-8 recommended)
- Check for special characters in point IDs or descriptions
- Try manual entry if file import not working

### Manual Entry Alternative

**If file import unavailable or problematic:**

**For each GCP, enter coordinates manually:**

1. **Click "Add GCP" or "New Control Point"**
2. **Fill in GCP attributes:**
   - **Point ID:** GCP1 (match survey numbering)
   - **X coordinate (Easting):** 685445.23 (meters)
   - **Y coordinate (Northing):** 9456795.47 (meters)
   - **Z coordinate (Elevation):** 142.15 (meters)
   - **Description:** "Left bank orange X on rock" (optional but helpful)
3. **Save GCP**
4. **Repeat for all GCPs** (GCP2, GCP3, ..., GCP8)

**Manual entry is tedious but reliable** if file import causes issues.

**After all GCPs entered (import or manual):**
- Verify GCP table complete (all GCPs listed)
- Check coordinates display correctly
- Proceed to image identification step

---

## Identifying GCPs in Sample Video

### Using the Annotated Reference Photo

**From Section 9.8, annotated photo provides visual reference:**

**Photo shows:**
- Each GCP marked with number (GCP1, GCP2, etc.)
- Visual description of marker (painted X, circle, stake, rock)
- Position relative to other features

**Use photo to identify GCPs systematically in sample video:**

1. **Display annotated photo alongside PtBox interface:**
   - Open photo on second monitor, tablet, or printed copy
   - Reference frequently during identification

2. **Match each GCP number to visible marker in video:**
   - Locate GCP1 in annotated photo
   - Find corresponding marker in sample video frame
   - Verify match (marker appearance, relative position)
   - Repeat for GCP2, GCP3, etc.

**Quality of identification determines transformation accuracy:**
- Precise identification (clicking exact GCP center): Transformation accurate
- Imprecise identification (clicking 10-20 pixels off center): Transformation degraded
- Wrong identification (clicking wrong feature): Transformation fails

**Take time to identify GCPs carefully.** Rushing this step creates errors that propagate through entire system.

### Systematic Identification Procedure

**For each GCP, follow this procedure:**

#### Step 1: Select GCP to Identify

**In PtBox interface:**
1. **Select GCP from list:** Click GCP1 in GCP table
2. **Interface highlights selected GCP** (typically row turns blue or yellow)
3. **Interface prompts for image position:** "Click GCP1 location in video frame"

#### Step 2: Locate GCP in Video Frame

**Using annotated photo as reference:**

1. **Find GCP in photo:**
   - Locate GCP1 in annotated photo
   - Note marker type and description: "Left bank orange X on rock"
   - Note position: Left side of image, near top, on large boulder

2. **Find corresponding feature in video frame:**
   - Look in same general area of video (left side, near top)
   - Identify large boulder (matches description)
   - Locate orange painted X on boulder surface

3. **Verify correct feature identified:**
   - Marker appearance matches description
   - Position relative to other features matches photo
   - If uncertain, refer to field notes or additional photos from Section 9.8

**If cannot locate GCP in video:**
- GCP may be outside field of view (camera angle changed since survey?)
- GCP may be obscured (vegetation, shadows, water level change)
- GCP may be too small or low contrast (not visible in video)
- **Do not guess or skip.** Document that GCP not visible, exclude from transformation

#### Step 3: Zoom for Precise Identification

**Most interfaces provide zoom capability:**

1. **Zoom in on GCP area:**
   - Use zoom control (slider, buttons, or mouse wheel)
   - Zoom to 200-400% magnification
   - Center GCP marker in zoomed view

2. **Identify precise GCP center:**
   - For painted X: Identify exact intersection of X arms
   - For painted circle: Identify center of circle
   - For survey stake: Identify top center of stake or nail head
   - For natural feature: Identify reference point specified during survey

**Pixel-level precision matters:**
- 1-2 pixel identification error: Acceptable (creates <2cm transformation error at GCP location)
- 5-10 pixel identification error: Marginal (creates 5-10cm transformation error)
- 20+ pixel identification error: Unacceptable (transformation will be poor quality)

**Use maximum zoom available** to identify GCP as precisely as possible.

#### Step 4: Click GCP Position

**With GCP centered in zoomed view:**

1. **Position cursor precisely on GCP center:**
   - Align cursor crosshairs with exact GCP point
   - Take care not to click slightly offset from center

2. **Click to mark GCP position:**
   - Left-click or tap (depending on interface)
   - Interface records pixel coordinates (u, v) for this GCP

3. **Verify marker placed correctly:**
   - Interface typically displays marker overlay (crosshair, circle, or dot) at clicked position
   - Verify marker overlay precisely on GCP center
   - If marker offset, interface may allow re-click or adjustment

**If marker misplaced:**
- Most interfaces allow correction:
  - Right-click and drag to adjust position
  - Or delete marker and re-click
  - Or click "Reselect" button and re-identify
- Correct immediately (easier than troubleshooting transformation errors later)

#### Step 5: Confirm GCP Identification

**After clicking:**

1. **Zoom out to normal view:**
   - Verify marker overlay still appears in correct location at normal zoom
   - Check marker not accidentally placed on wrong feature

2. **Interface typically moves to next GCP automatically:**
   - GCP1 complete, now prompting for GCP2
   - Or interface remains on GCP1, click "Next" or select GCP2 manually

3. **Document if needed:**
   - If identification uncertain, note in field notebook or configuration log
   - Example: "GCP3 partially obscured by shadow, identification approximate"

**Repeat Steps 1-5 for all GCPs** (GCP2, GCP3, ..., GCP8).

### Handling Difficult Identifications

**Some GCPs may be challenging to identify:**

**Low contrast markers:**
- GCP visible but low contrast with background
- Difficult to identify precise center
- **Solution:** Adjust video contrast/brightness in interface (if available), or use best judgment with wider error margin

**Partially obscured markers:**
- Vegetation, shadows, or glare partially cover GCP
- Visible but not entire marker clear
- **Solution:** Identify best estimate of center, note uncertainty in documentation

**Edge-of-frame markers:**
- GCP at extreme edge of camera field of view
- Visible but distorted or partially cut off
- **Solution:** Identify if possible, but consider excluding if quality poor

**Small or distant markers:**
- GCP far from camera, appears as only a few pixels
- Difficult to identify precise center
- **Solution:** Zoom maximum, identify best estimate, expect higher reprojection error

**Multiple similar features:**
- Several painted rocks or stakes in close proximity
- Uncertain which is correct GCP
- **Solution:** Use annotated photo carefully to distinguish, refer to GCP descriptions from survey, if uncertain exclude GCP

**Decision: Include or exclude problematic GCP?**

**Include if:**
- GCP visible, even if identification imprecise
- Contributes to overall transformation (more GCPs generally better)
- Reprojection error acceptable after calculation (see verification section)

**Exclude if:**
- GCP not visible or completely obscured
- Identification highly uncertain (would introduce more error than benefit)
- Better to use fewer high-quality GCPs than many low-quality GCPs

---

## Calculating the Coordinate Transformation

### Initiating Transformation Calculation

**After all GCPs identified (or maximum number identified):**

1. **Review GCP table:**
   - Verify all GCPs have both surveyed coordinates (X, Y, Z) and image coordinates (u, v)
   - Typically indicated by checkmark, green highlight, or "Complete" status
   - If any GCP missing image coordinates, either identify or remove from transformation

2. **Initiate transformation calculation:**
   - Click "Calculate Transformation", "Compute Homography", or "Generate Calibration" button
   - Interface processes GCP data and calculates transformation matrix

3. **Wait for calculation:**
   - Typically completes in seconds (transformation is fast computation)
   - Progress indicator or "Calculating..." message may display

4. **Calculation complete:**
   - Interface displays success message: "Transformation calculated successfully"
   - Or displays transformation parameters (matrix values - typically not human-readable)
   - Interface now ready for verification step

### What Happens During Calculation

**Mathematical process (simplified):**

**From Section 4.1 concepts:**

**Input data:**
- For each GCP: Image coordinates (u, v) and real-world coordinates (X, Y, Z)
- Example: GCP1 at pixel (450, 350) corresponds to real-world position (2.5, 5.0, 151.2)

**Calculation process:**
1. **Assemble equation system:** Each GCP provides constraints on transformation parameters
2. **Solve for transformation matrix:** Mathematical optimization finds best-fit transformation
3. **Account for perspective:** Homography transformation handles perspective distortion (objects farther away appear smaller)
4. **Minimize overall error:** If more than 4 GCPs (overdetermined system), calculation finds transformation that minimizes reprojection error across all GCPs

**Output:**
- **Transformation matrix:** Set of parameters defining mathematical relationship between pixel coordinates and real-world coordinates
- **For each pixel (u, v), transformation calculates real-world position (X, Y, Z)**
- Transformation now ready to use for velocity measurements

**Transformation quality depends on:**
- GCP survey accuracy (2-3 cm accuracy ensures good transformation)
- GCP image identification accuracy (1-2 pixel precision ensures good transformation)
- GCP distribution (spread throughout field of view ensures transformation accurate everywhere)
- Number of GCPs (8-10 GCPs provides redundancy and error averaging)

---

## Verifying Transformation Quality

### Understanding Reprojection Error

**From Section 4.1:**

**Reprojection error measures transformation quality:**

**What it is:**
- For each GCP, transformation converts image coordinates (u, v) back to real-world coordinates
- Compare transformed coordinates with original surveyed coordinates
- Difference is reprojection error for that GCP

**Calculation example:**
```
GCP3 surveyed position: (12.30, 8.50, 150.45) meters
GCP3 image position: (850, 520) pixels

Apply transformation to image position (850, 520):
Transformed position: (12.33, 8.48, 150.47) meters

Reprojection error:
ΔX = 12.33 - 12.30 = 0.03 m (3 cm)
ΔY = 8.48 - 8.50 = -0.02 m (2 cm)
ΔZ = 150.47 - 150.45 = 0.02 m (2 cm)

Total error: sqrt(0.03² + 0.02² + 0.02²) = 0.04 m = 4 cm

Reprojection error for GCP3: 4 cm (acceptable)
```

**What reprojection error indicates:**

**Small error (<3 cm):**
- Excellent transformation quality
- GCP surveyed accurately
- GCP identified precisely in image
- Transformation fits data well

**Moderate error (3-5 cm):**
- Good transformation quality
- Acceptable for operational use
- Slight survey or identification imprecision, but within tolerance

**Large error (5-10 cm):**
- Marginal transformation quality
- Investigate cause (survey error? identification error?)
- May be acceptable if only one or two GCPs have large error (outliers)

**Very large error (>10 cm):**
- Unacceptable transformation quality
- Definite problem with this GCP (wrong survey coordinates? wrong identification? GCP moved?)
- Must investigate and resolve before using transformation

### Reviewing Reprojection Errors in Interface

**PtBox interface displays reprojection errors after calculation:**

**Typical display format:**

**Table view:**
```
GCP ID    Surveyed X    Surveyed Y    Surveyed Z    Reprojection Error
GCP1      685445.23     9456795.47    142.15        2.1 cm
GCP2      685447.85     9456798.22    141.98        1.8 cm
GCP3      685452.10     9456796.80    140.45        4.5 cm
GCP4      685458.32     9456795.15    141.75        2.3 cm
GCP5      685460.15     9456792.50    142.30        3.1 cm
GCP6      685448.50     9456802.10    141.20        2.9 cm
GCP7      685455.80     9456801.90    140.95        2.2 cm
GCP8      685461.20     9456800.45    141.50        15.2 cm  ← INVESTIGATE
```

**Visual overlay:**
- Video frame displays GCP markers with color coding:
  - Green: Reprojection error <3 cm (excellent)
  - Yellow: Reprojection error 3-5 cm (good)
  - Orange: Reprojection error 5-10 cm (marginal)
  - Red: Reprojection error >10 cm (problem)

**Summary statistics:**
- **RMS (Root Mean Square) reprojection error:** Overall quality metric averaging all GCPs
- **Maximum reprojection error:** Worst GCP error
- **Mean reprojection error:** Average error across GCPs

**Example summary:**
```
RMS reprojection error: 3.2 cm
Mean reprojection error: 2.8 cm
Maximum reprojection error: 15.2 cm (GCP8)

Overall assessment: GOOD (one outlier requires investigation)
```

### Interpreting Reprojection Error Results

**Scenario 1: All GCPs have small errors (<5 cm)**

**Example:**
```
GCP1: 2.1 cm
GCP2: 1.8 cm
GCP3: 4.5 cm
GCP4: 2.3 cm
GCP5: 3.1 cm
GCP6: 2.9 cm
GCP7: 2.2 cm
GCP8: 3.8 cm

RMS error: 3.0 cm
```

**Assessment: EXCELLENT**
- Transformation is high quality
- GCPs surveyed accurately and identified precisely
- Proceed with confidence to operational use
- No further action needed

**Scenario 2: Most GCPs small errors, one or two moderate errors (5-8 cm)**

**Example:**
```
GCP1: 2.1 cm
GCP2: 1.8 cm
GCP3: 7.5 cm ← Moderate error
GCP4: 2.3 cm
GCP5: 3.1 cm
GCP6: 6.2 cm ← Moderate error
GCP7: 2.2 cm
GCP8: 3.8 cm

RMS error: 4.1 cm
```

**Assessment: GOOD**
- Overall transformation acceptable
- Two GCPs (GCP3, GCP6) have moderate errors
- Possible causes: Slight identification imprecision, marginal survey quality at these locations
- **Action:** Review identification for GCP3 and GCP6 (recheck in zoomed video, verify clicked correct location)
- If identification confirmed correct, accept moderate errors (transformation still usable)

**Scenario 3: One GCP has large error (>10 cm), others good**

**Example:**
```
GCP1: 2.1 cm
GCP2: 1.8 cm
GCP3: 4.5 cm
GCP4: 2.3 cm
GCP5: 3.1 cm
GCP6: 2.9 cm
GCP7: 2.2 cm
GCP8: 15.2 cm ← Large error (outlier)

RMS error: 5.8 cm (elevated by outlier)
```

**Assessment: INVESTIGATE GCP8**
- Most GCPs excellent quality
- GCP8 is clear outlier (much larger error than others)
- Likely causes:
  - GCP8 identified incorrectly in image (clicked wrong feature)
  - GCP8 surveyed incorrectly (coordinate error in survey data)
  - GCP8 moved between survey and video capture
- **Action:** Investigate GCP8 (see troubleshooting section below)

**Scenario 4: Multiple GCPs have large errors (>10 cm)**

**Example:**
```
GCP1: 12.3 cm
GCP2: 8.7 cm
GCP3: 15.1 cm
GCP4: 11.5 cm
GCP5: 9.2 cm
GCP6: 14.8 cm
GCP7: 10.1 cm
GCP8: 13.5 cm

RMS error: 11.9 cm
```

**Assessment: TRANSFORMATION FAILED**
- Systematic problem affecting all or most GCPs
- Possible causes:
  - Wrong coordinate reference system (CRS mismatch between survey and PtBox)
  - Survey data has major errors (wrong units? decimal errors?)
  - Image orientation incorrect (from Section 10.1)
  - Fundamental mismatch between image and survey data
- **Action:** Do not proceed. Troubleshoot systematically (see troubleshooting section)

### Quality Thresholds

**Recommended reprojection error thresholds:**

**Individual GCP thresholds:**
- **<3 cm:** Excellent (no action needed)
- **3-5 cm:** Good (acceptable for most GCPs)
- **5-10 cm:** Marginal (investigate if possible, may accept for 1-2 GCPs)
- **>10 cm:** Unacceptable (must investigate and resolve)

**Overall RMS threshold:**
- **<3 cm:** Excellent transformation quality
- **3-5 cm:** Good transformation quality (acceptable for operational use)
- **5-8 cm:** Marginal transformation quality (use caution, verify with check measurements)
- **>8 cm:** Poor transformation quality (do not use operationally until resolved)

**Decision criteria:**

**Proceed to operational use if:**
- RMS reprojection error <5 cm
- No more than 2 GCPs with errors >5 cm
- No GCPs with errors >10 cm (or problematic GCPs excluded)

**Investigate and resolve before operational use if:**
- RMS reprojection error >5 cm
- Multiple GCPs with errors >5 cm
- Any GCPs with errors >10 cm

---

## Troubleshooting and Refining Transformation

### Investigating Individual GCP Problems

**When one GCP has large reprojection error (>10 cm):**

#### Step 1: Recheck Image Identification

**Most common cause: Wrong pixel location clicked**

1. **Zoom in on problematic GCP in video:**
   - Select GCP8 in interface
   - View GCP8 marker overlay position
   - Zoom to maximum magnification

2. **Compare with annotated photo:**
   - Is marker overlay on correct feature?
   - Did you click the right GCP (not adjacent marker)?
   - Is marker overlay precisely on GCP center, or offset?

3. **Reidentify if needed:**
   - Delete existing marker or click "Reselect"
   - Carefully re-identify GCP8 position
   - Click precise center of marker
   - Recalculate transformation
   - Check if reprojection error improved

**If reidentification resolves issue:** Problem was identification error. Transformation now acceptable.

#### Step 2: Verify Survey Coordinates

**If image identification definitely correct, check survey data:**

1. **Review GCP8 coordinates in loaded data:**
   - X: 685461.20
   - Y: 9456800.45
   - Z: 141.50

2. **Cross-check with original survey export:**
   - Open `GCPs_Site01_20241115.csv`
   - Find GCP8 row
   - Verify coordinates match what was loaded into PtBox

3. **Check for typos or data entry errors:**
   - Decimal point in wrong place? (685461.20 vs. 68546.120)
   - Digits transposed? (685461.20 vs. 685416.20)
   - Wrong GCP? (GCP8 data accidentally copied from GCP7?)

4. **If error found:**
   - Correct coordinates in PtBox (edit GCP8 entry)
   - Or re-export corrected data and re-import
   - Recalculate transformation

**If survey data definitely correct:** Problem may be GCP moved, or GCP visibility poor. Consider excluding GCP8.

#### Step 3: Check GCP Visibility and Marker Quality

**If identification and coordinates both verified:**

1. **Assess GCP8 visibility in video:**
   - Is marker clearly visible?
   - Obscured by shadows, vegetation, or glare?
   - Is marker precise (sharp painted point vs. diffuse marking)?

2. **Check for GCP movement:**
   - Did GCP move between survey and video capture?
   - Floating GCP displaced by current?
   - Marker on unstable surface (loose rock)?
   - Vandalism or accidental disturbance?

3. **If visibility poor or movement suspected:**
   - Exclude GCP8 from transformation
   - Recalculate with remaining GCPs
   - 7 GCPs still sufficient if well-distributed

#### Step 4: Exclude Problematic GCP

**If GCP cannot be corrected:**

1. **Disable GCP in interface:**
   - Uncheck "Include in transformation" checkbox for GCP8
   - Or click "Exclude" or "Remove from calculation"

2. **Recalculate transformation without GCP8**

3. **Check RMS reprojection error:**
   - Should improve significantly if GCP8 was outlier
   - Example: RMS drops from 5.8 cm to 3.0 cm after excluding GCP8

4. **Verify sufficient GCPs remain:**
   - Minimum 6 GCPs recommended (after exclusions)
   - If excluding GCP8 leaves only 5 GCPs, consider whether to continue or resurvey additional GCPs

**Excluding one or two problematic GCPs is acceptable.** Better to use 6-7 high-quality GCPs than 8-9 GCPs with outliers.

### Resolving Systematic Problems

**When multiple GCPs have large errors (Scenario 4):**

#### Problem: Wrong Coordinate Reference System (CRS)

**Symptoms:**
- All or most GCPs have large reprojection errors (>10 cm)
- Errors may show systematic pattern (all shifted in same direction)

**Cause:**
- Survey data in UTM Zone 48S, but PtBox configured for UTM Zone 47S
- Or survey data in WGS84 datum, but PtBox configured for different datum

**Solution:**
1. **Verify survey CRS:** Check SW Maps project settings or survey report
2. **Verify PtBox CRS:** Check PtBox configuration settings (typically in Camera Setup or General Configuration)
3. **Match CRS settings:** Configure PtBox to use same CRS as survey data
4. **Re-import GCP coordinates** (if CRS affects coordinate values)
5. **Recalculate transformation**

#### Problem: Image Orientation Incorrect

**Symptoms:**
- Large reprojection errors for all GCPs
- GCP overlay markers appear in wrong areas of image (e.g., GCP1 overlay on right side when GCP1 should be on left)

**Cause:**
- Image orientation not configured correctly in Section 10.1
- Camera view rotated or flipped, but orientation correction not applied

**Solution:**
1. **Return to Section 10.1 orientation configuration**
2. **Review and correct image orientation** (rotation and flip settings)
3. **Save corrected orientation**
4. **Return to GCP configuration:** GCP image positions may need reidentification after orientation change
5. **Reidentify GCPs in correctly-oriented image**
6. **Recalculate transformation**

#### Problem: Survey Data Units Incorrect

**Symptoms:**
- Reprojection errors very large (meters scale, not centimeters)
- Or transformation fails completely

**Cause:**
- Survey coordinates in feet, but PtBox expecting meters
- Or vice versa

**Solution:**
1. **Verify survey data units:** Check SW Maps export settings
2. **Convert if necessary:** If survey in feet, convert to meters (multiply by 0.3048)
3. **Re-import converted coordinates**
4. **Recalculate transformation**

---

## Saving Transformation Configuration

### Finalizing GCP Configuration

**Once reprojection errors acceptable:**

1. **Review final GCP configuration:**
   - Check number of GCPs included: Typically 6-10 GCPs
   - Check RMS reprojection error: Should be <5 cm
   - Verify no individual GCP with error >10 cm (or problematic GCPs excluded)

2. **Document configuration:**
   - Record in configuration log or field notebook:
     - Number of GCPs used: 8
     - RMS reprojection error: 3.2 cm
     - GCPs excluded (if any): "GCP8 excluded due to poor visibility"
     - Date and operator name

3. **Save transformation:**
   - Click "Save Transformation", "Accept Calibration", or "Finalize Configuration"
   - PtBox stores transformation parameters for operational use
   - Confirmation message: "Transformation saved successfully"

### Testing Transformation (Optional)

**Some interfaces provide test capability:**

**Test procedure:**
1. **Click random point in video frame**
2. **Interface displays transformed coordinates** (real-world X, Y, Z)
3. **Verify coordinates reasonable:**
   - Within expected range for site?
   - Corresponds to expected location (left bank, mid-channel, right bank)?

**Example test:**
- Click point on left bank near GCP1
- Transformed coordinates: (2.8, 5.3, 151.0) meters
- Expected: Similar to GCP1 coordinates (2.5, 5.0, 151.2)
- Assessment: Reasonable (within ~50 cm of GCP1, as expected for nearby point)

**Test multiple points across field of view:**
- Left bank, mid-channel, right bank
- Near GCPs and between GCPs
- Verify coordinates logical for all test points

**If test coordinates unreasonable:**
- Double-check transformation calculation completed correctly
- Verify GCP data correct and transformation saved
- May indicate problem requiring further investigation

---

## Common Issues and Solutions

### Issue: Cannot find all GCPs in video

**Symptoms:**
- Several GCPs clearly visible, but 2-3 GCPs cannot be located
- Annotated photo shows GCPs, but they do not appear in sample video

**Solutions:**
- **Camera view changed:** Camera angle or zoom adjusted between annotated photo capture and sample video
  - Verify sample video is the video captured during survey (check filename and timestamp)
  - If camera definitely changed, may need to recapture sample video or resurvey GCPs
- **GCPs outside field of view:** GCPs placed at edge of camera view, minor shift caused them to move out of frame
  - Accept fewer GCPs (6-7 may be sufficient)
  - Or adjust camera view to include missing GCPs and recapture sample video
- **Water level change:** GCPs submerged or exposed between survey and video capture
  - Document water level change in notes
  - Use GCPs that are visible at current water level
  - Consider adding permanent GCPs above waterline for future reference

### Issue: Transformation calculation fails

**Symptoms:**
- Click "Calculate Transformation" but interface displays error message
- "Insufficient GCPs" or "Transformation cannot be computed"

**Solutions:**
- **Not enough GCPs:** Must have minimum 4 GCPs with both image and surveyed coordinates
  - Verify each GCP has image position identified (click in video frame)
  - Verify each GCP has surveyed coordinates loaded
- **GCPs collinear:** All GCPs in straight line (mathematically problematic for homography)
  - Add GCPs with better distribution (spread across field of view)
  - Ensure GCPs not all on same bank or same elevation
- **Software bug or data corruption:**
  - Refresh interface and reload GCP data
  - Try exiting and restarting PtBox interface
  - Contact technical support if problem persists

### Issue: RMS error acceptable but velocities seem wrong later

**Symptoms:**
- Reprojection error looks good (<5 cm RMS)
- But when system operational, velocity measurements seem inaccurate
- Discharge estimates do not match expected values

**Solutions:**
- **GCP distribution poor:** GCPs clustered in one area, transformation inaccurate in other areas
  - Review GCP spatial distribution on map
  - Add GCPs in areas lacking coverage
  - Recalculate transformation with better distribution
- **Water level changed significantly:** Transformation calculated at one water level, used at very different level
  - Perspective changes with water level (especially in sloping channels)
  - May need to recalibrate transformation at new water level
  - Or survey additional GCPs at multiple elevations
- **Camera moved slightly:** Thermal expansion, wind vibration, or mounting structure settling
  - Check camera mounting security
  - Recapture sample video and recalculate transformation if camera definitely moved

---

## Time Estimates

**GCP configuration time varies with experience and number of GCPs:**

**First-time configuration (8 GCPs, learning interface):**
- Import or enter GCP coordinates: 5-10 minutes
- Identify all GCPs in video (careful identification): 20-30 minutes (2-4 min per GCP)
- Calculate transformation and review errors: 5 minutes
- Troubleshoot and refine (if needed): 10-20 minutes
- Save and document: 5 minutes
- **Total: 45-70 minutes**

**Experienced user (8 GCPs, familiar interface):**
- Import GCP coordinates: 2-3 minutes
- Identify all GCPs: 12-20 minutes (1.5-2.5 min per GCP)
- Calculate and review: 3 minutes
- Minor refinements: 5 minutes
- Save and document: 2 minutes
- **Total: 25-35 minutes**

**Additional time if troubleshooting required:**
- One outlier GCP to investigate: +10-15 minutes
- Multiple GCP problems: +20-40 minutes
- Systematic problem (CRS, orientation): +30-60 minutes (may require starting over)

**GCP configuration is most time-intensive step** in PtBox software configuration, but critical for accuracy.

---

## Summary: Adding Control Points

**Purpose:**
- Establish coordinate transformation converting camera pixels to real-world meters
- Connect image space (pixel coordinates) to physical space (surveyed coordinates)
- Enable accurate velocity and discharge measurements

**Key steps:**
1. Export surveyed GCP coordinates from SW Maps (Section 9.8 data)
2. Load GCP coordinates into PtBox (import CSV or manual entry)
3. Identify each GCP in sample video frame (precise pixel position)
4. Calculate coordinate transformation (homography)
5. Verify transformation quality (reprojection error)
6. Troubleshoot and refine (investigate outliers, exclude problematic GCPs)
7. Save transformation configuration for operational use

**Quality criteria:**
- RMS reprojection error <5 cm (excellent <3 cm)
- No individual GCP error >10 cm (or problematic GCPs excluded)
- Minimum 6 GCPs used (8-10 recommended)
- GCPs well-distributed across field of view

**Common issues and resolutions:**
- Outlier GCP (>10 cm error): Recheck identification, verify coordinates, or exclude
- Multiple large errors: Check CRS match, verify image orientation, verify survey data units
- Cannot find GCPs in video: Accept fewer GCPs or recapture video with better coverage

**Critical success factors:**
- Precise GCP identification in video (1-2 pixel accuracy)
- Accurate survey data from Chapter 9 (2-3 cm RTK accuracy)
- Good GCP distribution (near/far, left/right)
- Careful verification of reprojection errors before proceeding

**Next step:**
With transformation established, proceed to Section 10.3: Adding Cross-Sections to enable discharge calculations.

---

**References:**
- Section 9.8: Survey Execution - Control Points and Sample Video (GCP survey data source)
- Section 4.1: Pixel to Physical Transformation (coordinate transformation theory)
- Section 10.1: Orienting the Image (prerequisite configuration step)
- Section 10.3: Adding Cross-Sections (next configuration step)
