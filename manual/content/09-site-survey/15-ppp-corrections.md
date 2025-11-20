# 9.15 Survey Data Processing - PPP Corrections

This is the MOST CRITICAL post-processing section in the entire survey workflow. Precise Point Positioning (PPP) corrections transform your survey from local relative accuracy (~25 cm absolute) to global absolute accuracy (2-10 cm). This improvement is essential when integrating OpenRiverCam data with satellite imagery, base maps, hydrologic models, or multi-site monitoring networks.

PPP processing uses global reference station networks and precise satellite orbit data to correct your base station position. Since all rover measurements are relative to the base station, correcting the base station position automatically improves the absolute accuracy of ALL survey points - ground control points, cross-sections, water level measurements, and camera positions.

This section provides the complete step-by-step workflow from raw base station logs to corrected survey coordinates ready for PtBox import.

By the end of this section, you will understand:
- How to convert UBX logs to RINEX format using CONVBIN
- How to submit RINEX data to AUSPOS for PPP processing
- Antenna selection and height entry considerations
- How to interpret and validate PPP results
- How to apply coordinate corrections in QGIS
- How to update geometry and export corrected data
- Quality control for the entire PPP workflow
- How this connects to Section 5.6 concepts and SURVEY_PROCESS.md procedures

**Reference:** SURVEY_PROCESS.md Section 10 - PPP & Data Processing (THE COMPLETE WORKFLOW)

---

## PPP Workflow Overview

### The Complete Processing Chain

**From field survey to corrected coordinates:**

```
FIELD SURVEY (Day 1):
Base station survey-in (30-60 min) → Local coordinates (±25 cm absolute)
RINEX logging started (6-12 hours)
Rover survey (GCPs, cross-sections, etc.) → Relative to base (±2 cm relative)
RINEX logging stopped
Survey data exported from SW Maps

POST-PROCESSING (Day 2-7):
Step 1: Convert UBX to RINEX (CONVBIN) → RINEX observation files
Step 2: Submit RINEX to AUSPOS → PPP processing (wait 30 min - 24 hours)
Step 3: Download PPP results → Corrected base station coordinates (±2-5 cm absolute)
Step 4: Calculate translation vector → ΔE, ΔN, ΔZ corrections
Step 5: Apply corrections in QGIS → All survey points corrected
Step 6: Update geometry → Corrected Geopackage
Step 7: Export XYZ for PtBox → Ready for camera configuration
```

**Why this workflow:**
- Field survey completes in one day (efficient, no waiting for PPP during survey)
- Post-processing improves accuracy after field work (flexible timeline)
- All rover measurements corrected together (consistent improvement)
- Option to use local coordinates immediately OR wait for PPP-corrected global coordinates

**From Section 5.6 (PPP Concepts Recap):**
- Base station survey-in provides ~25 cm absolute accuracy (adequate for local reference)
- PPP post-processing improves to 2-10 cm absolute accuracy (global reference quality)
- Rover measurements maintain 1-3 cm relative accuracy (unchanged by PPP)
- PPP correction shifts all coordinates by same translation (ΔE, ΔN, ΔZ)

---

## Step 1: UBX to RINEX Conversion Using CONVBIN

### Understanding File Formats

**UBX format (u-blox proprietary):**
- Binary format used by u-blox GNSS receivers (ArduSimple base station)
- Contains raw GNSS observations: Carrier phase, pseudorange, satellite ephemeris
- NOT directly usable by PPP services (requires conversion)
- File extension: .ubx
- Created by: u-center data logging during survey

**RINEX format (Receiver Independent Exchange):**
- Standard ASCII format for GNSS observations (worldwide standard)
- Readable by all PPP services (AUSPOS, GAPS, CSRS-PPP, etc.)
- Multiple files:
  - .obs or .yyo: Observation data (carrier phase, pseudorange measurements)
  - .nav or .yyn: Navigation data (satellite ephemeris, orbital information)
- Created by: Converting UBX with CONVBIN or similar tools

### CONVBIN Command-Line Tool

**CONVBIN is part of RTKLIB (open-source GNSS software):**

**Installation:**
- Download RTKLIB: https://www.rtklib.com/
- Extract archive
- CONVBIN executable location:
  - Windows: `rtklib\bin\convbin.exe`
  - Linux: `rtklib/bin/convbin` (compile from source)
  - Mac: Compile from source or use pre-compiled binary

**Add CONVBIN to system PATH (optional but recommended):**
- Enables running `convbin` from any directory
- Windows: System Properties → Environment Variables → PATH → Add RTKLIB bin folder
- Linux/Mac: Add to .bashrc or .zshrc: `export PATH=$PATH:/path/to/rtklib/bin`

### CONVBIN Command Syntax

**From SURVEY_PROCESS.md Section 10, Step 1:**

```bash
convbin -od -os -oi -ot -f 1 your_file.ubx
```

**Command options explained:**

**`-od`**: Output observation data
- Creates .obs file (or .YYo where YY = year)
- Contains carrier phase and pseudorange observations
- Required for PPP processing

**`-os`**: Output satellite ephemeris
- Creates .nav file (or .YYn for GPS navigation data)
- Contains satellite orbital information
- Required for PPP (though AUSPOS can use precise ephemeris instead)

**`-oi`**: Output ionosphere parameters
- Includes ionosphere model corrections
- Optional but recommended (improves PPP accuracy)

**`-ot`**: Output time parameters
- Includes time system corrections
- Optional but recommended

**`-f 1`**: RINEX format version 1
- RINEX version 1 (older but widely compatible)
- Alternatives: `-f 2` (RINEX 2.x), `-f 3` (RINEX 3.x)
- AUSPOS accepts all versions (use version 1 for maximum compatibility)

**`your_file.ubx`**: Input UBX file
- Replace with actual filename from u-center logging
- Example: `base_station_20241114.ubx`

### Running CONVBIN - Step by Step

**Step 1: Locate UBX file**
- Find UBX file from u-center data logging
- Example path: `C:\Users\Survey\Desktop\base_20241114_survey.ubx`
- File size: Typically 50 MB - 500 MB (depends on logging duration)

**Step 2: Open command prompt/terminal**
- Windows: Press Win+R, type `cmd`, press Enter
- Mac/Linux: Open Terminal application

**Step 3: Navigate to directory containing UBX file**
```bash
cd C:\Users\Survey\Desktop
```
(Or drag/drop folder to terminal window on Mac/Linux)

**Step 4: Run CONVBIN command**
```bash
convbin -od -os -oi -ot -f 1 base_20241114_survey.ubx
```

**CONVBIN processes file (may take 30 seconds to several minutes for large files):**
```
[Terminal output]
reading base_20241114_survey.ubx...
scanning observation data...
  time: 2024/11/14 09:00:00 - 2024/11/14 17:30:00 (8.5 hours)
  receiver: u-blox ZED-F9P
  observation types: L1C L2C C1C C2C D1C D2C S1C S2C
creating base_20241114_survey.obs...
creating base_20241114_survey.nav...
done
```

**Step 5: Verify output files created**
```bash
dir
# or on Mac/Linux:
ls -l
```

**Expected output files:**
- `base_20241114_survey.obs` (observation data, ~10-100 MB)
- `base_20241114_survey.nav` (navigation data, ~1-5 MB)

**If conversion successful:**
- Two RINEX files created (.obs and .nav)
- Proceed to Step 2 (submit to AUSPOS)

**If conversion fails:**
- See troubleshooting section below

### CONVBIN Advanced Options

**Convert specific time range (useful for long logging sessions):**

```bash
convbin -od -os -ts 2024/11/14 10:00:00 -te 2024/11/14 18:00:00 base_20241114_survey.ubx
```

**Options:**
- `-ts YYYY/MM/DD HH:MM:SS`: Start time (begin conversion from this time)
- `-te YYYY/MM/DD HH:MM:SS`: End time (stop conversion at this time)

**Example use case:**
- Logged 24 hours but only need 8-hour survey window
- Reduces file size and PPP processing time
- Specify survey start and end times

**Convert to RINEX version 3 (newer format):**
```bash
convbin -od -os -oi -ot -f 3 base_20241114_survey.ubx
```

**Use RINEX 3 if:**
- PPP service specifically requires it
- Processing multi-constellation data (GPS + GLONASS + Galileo + BeiDou)

**Most cases: Use RINEX version 1 (-f 1) for maximum compatibility**

### Troubleshooting CONVBIN

**Issue: "Command not found" or "convbin is not recognized"**

**Cause:** CONVBIN not installed or not in system PATH

**Solutions:**
- Verify RTKLIB installed (check for convbin.exe in RTKLIB bin folder)
- Use full path to convbin: `C:\rtklib\bin\convbin.exe -od -os ...`
- Or navigate to RTKLIB bin folder: `cd C:\rtklib\bin` then run `convbin ...`

**Issue: "No observation data found" or "Empty output file"**

**Cause:** UBX file does not contain raw observation data (wrong message types)

**Diagnosis:**
- Check u-center configuration: UBX-RXM-RAWX and UBX-RXM-SFRBX must be enabled
- Verify file size: UBX file should be >10 MB for multi-hour session (if tiny, no data logged)

**Solutions:**
- Verify u-center configuration before next survey (see SURVEY_PROCESS.md Appendix C)
- If current file invalid: Cannot proceed with PPP (must re-survey)

**Issue: Conversion creates .obs file but it is very small (<1 MB)**

**Cause:** Partial data logging (receiver lost power, USB disconnected during session)

**Diagnosis:**
- Check .obs file duration: Should match survey session length (6-12 hours)
- If duration short (e.g., 30 minutes instead of 8 hours): Incomplete data

**Solutions:**
- Partial session may still be processable (AUSPOS requires minimum ~2 hours)
- Submit to AUSPOS and check results (may have larger uncertainty)
- If duration <2 hours: PPP results likely poor (consider re-survey)

**Issue: RINEX files created but AUSPOS rejects upload**

**Cause:** RINEX format errors, incompatible version, or corrupted data

**Solutions:**
- Try different RINEX version: `-f 2` or `-f 3` instead of `-f 1`
- Use RTKCONV GUI instead of CONVBIN (alternative conversion method)
- Check RINEX file with text editor (should be ASCII text, not binary)

### Alternative: RTKCONV GUI Method

**If CONVBIN command-line difficult:**

**RTKCONV is graphical interface for same conversion:**

**Step 1: Launch RTKCONV**
- RTKLIB folder → bin → rtkconv.exe (double-click)
- Window opens: "RINEX Converter"

**Step 2: Select input file**
- Input File: Click [...] button
- Browse to UBX file, select, Open

**Step 3: Set format options**
- Format: Select "u-blox" or "u-blox UBX"
- RINEX Version: 2.11 (or 3.03 for RINEX 3)
- Observation Types: GPS L1/L2 (or All if multi-constellation)

**Step 4: Set time range (optional)**
- Time Start: Leave blank for entire session
- Time End: Leave blank for entire session
- Or specify start/end times if subsetting data

**Step 5: Convert**
- Click "Convert" button
- RTKCONV processes file (progress bar shown)
- Output files created in same directory as input

**Step 6: Verify output**
- Check for .obs and .nav files
- Proceed to AUSPOS submission

---

## Step 2: RINEX File Submission to AUSPOS

### AUSPOS Service Overview

**AUSPOS (Australian Online GPS Processing Service):**
- Free PPP service provided by Geoscience Australia
- Global coverage (processes data from anywhere on Earth, not just Australia)
- Uses APREF network (Asia-Pacific Reference Frame) + IGS global stations
- Accepts RINEX observation files from any GNSS receiver
- Returns corrected coordinates in multiple formats (ITRF, GDA, WGS84)

**Why AUSPOS for Indonesia/Asia-Pacific:**
- Excellent regional coverage (optimized for Asia-Pacific region)
- Free and reliable (government-operated service)
- Processing quality equivalent to commercial PPP services
- No account or subscription required

**AUSPOS URL:** https://www.ga.gov.au/auspos

**Alternatives (if AUSPOS unavailable or region-specific):**
- CSRS-PPP (Canada): https://webapp.csrs-scrs.nrcan-rncan.gc.ca/geod/tools-outils/ppp.php
- GAPS (Canada): https://gaps.gge.unb.ca/
- Trimble CenterPoint RTX: https://trimblertx.com/ (commercial, requires subscription)
- OPUS (USA): https://www.ngs.noaa.gov/OPUS/ (optimized for North America)

### AUSPOS Submission Procedure

**Step 1: Navigate to AUSPOS website**
- Open browser: https://www.ga.gov.au/auspos
- Page loads: "AUSPOS - Online GPS Processing Service"

**Step 2: Scroll to submission form**
- Section: "Submit RINEX file for processing"
- Form fields: File upload, email, antenna details, processing options

**Step 3: Upload RINEX observation file**
- Click "Choose File" or "Browse"
- Select .obs file (e.g., `base_20241114_survey.obs`)
- File uploads to AUSPOS server (may take 1-5 minutes for large files)

**Step 4: Enter email address**
- Field: "Email address for results"
- Enter your email (results will be sent here)
- Verify email correct (typo will prevent receiving results)

**Step 5: Select antenna type - CRITICAL DECISION**

**From SURVEY_PROCESS.md Section 10:**
```
Antenna Selection: Choose closest match from available options:
- TRM29659.00 (Trimble multiband, good generic choice)
- SEPCHOKE_MC (Septentrio choke ring, multiband)
- LEIAT504GG (Leica multiband)
- TWIVC6150 (Tallysman multiband)
- Or select "Unknown" if no close match available
```

**Antenna selection impacts PPP accuracy:**

**Why antenna type matters:**
- Different antennas have different phase center offsets (PCO)
- PPO: Distance from physical antenna reference point to electrical phase center
- PPP processing applies antenna model corrections
- Wrong antenna model → systematic error of 2-10 cm (mostly vertical)

**ArduSimple F9P typical antennas:**
- Survey GNSS multiband antenna (various brands: Tallysman, u-blox, Harxon)
- Most are "generic multiband" type (not in AUSPOS database)

**Recommended selection strategy:**

**Option 1: Select "TRM29659.00" (Trimble multiband)**
- Generic multiband antenna, widely used
- Antenna phase center similar to most survey-grade multiband antennas
- Provides reasonable approximation (error typically <5 cm)

**Option 2: Select antenna if exact model in list**
- Check antenna label/documentation for model number
- Search AUSPOS dropdown for exact match
- Example: "TWIVC6150" if using Tallysman VC6150

**Option 3: Select "Unknown"**
- AUSPOS uses default antenna model (generic phase center)
- Accuracy slightly reduced (±5-10 cm typical)
- Acceptable if no close match available

**Which to choose:**
- If antenna model known AND in AUSPOS list: Select exact match (best accuracy)
- If antenna model unknown OR not in list: Select "TRM29659.00" (good approximation)
- If unsure: Select "Unknown" (conservative choice, slightly lower accuracy)

**For most OpenRiverCam deployments: "TRM29659.00" or "Unknown" acceptable** (2-5 cm vs. 5-10 cm absolute accuracy both adequate for GCP transformation).

**Step 6: Enter antenna height - CRITICAL MEASUREMENT**

**From SURVEY_PROCESS.md Section 10:**
```
Antenna Height: Measure from ground to antenna phase center (bottom of antenna)
```

**Antenna height definition:**
- Vertical distance from base station ground point to antenna reference point (ARP)
- Typically measured to bottom center of antenna
- Measured during base station setup (Section 9.4)
- Recorded in field notebook: "Antenna height 1.85m" (example)

**How to measure (field procedure recap):**
1. Base station tripod set up, antenna mounted
2. Measure from ground directly below antenna to bottom of antenna
3. Use tape measure or ruler (vertical distance)
4. Record three measurements, average
5. Example: 1.83m, 1.85m, 1.86m → Average 1.85m

**Enter antenna height in AUSPOS form:**
- Field: "Antenna height (meters)"
- Enter value: 1.85
- Units: Meters (NOT feet)
- Precision: 0.01m (centimeter precision)

**Antenna height errors impact vertical accuracy:**
- 1 cm error in antenna height → 1 cm error in vertical position
- 10 cm error → 10 cm error in vertical (significant)
- Horizontal position barely affected by antenna height errors

**If antenna height not recorded during survey:**
- Estimate from tripod specifications (typical height 1.5-2.0m)
- Or from photos (compare antenna to known reference)
- Or assume 1.8m (typical survey tripod height)
- Accept uncertainty: ±5-10 cm vertical accuracy

**Step 7: Select processing options**

**Static positioning:**
- Processing mode: "Static" (default, correct for base station survey)
- NOT "Kinematic" (kinematic for moving receivers, not applicable)

**Processing duration:**
- AUSPOS automatically uses all data in RINEX file
- No need to specify duration (uses entire session)

**Output format:**
- Select output coordinate system:
  - ITRF (International Terrestrial Reference Frame) - global reference
  - GDA2020 (Australian datum) - regional
  - WGS84 (World Geodetic System 1984) - GPS native
- **Recommendation: Select ITRF or WGS84** (global datums, directly usable)

**Step 8: Submit for processing**
- Click "Submit" or "Process" button
- AUSPOS confirms: "File uploaded successfully, processing started"
- Email confirmation sent immediately

**Step 9: Wait for processing**

**Processing time varies:**
- **Fast processing:** 30 minutes to 2 hours (typical for 6-8 hour session)
- **Slow processing:** 4-24 hours (if AUSPOS server busy, or very long session)
- **Typical:** 1-3 hours for standard survey session

**Email notification:**
- AUSPOS sends email when processing complete
- Subject: "AUSPOS Processing Results - [your filename]"
- Email contains:
  - Summary of results
  - Corrected coordinates (latitude, longitude, elevation)
  - Uncertainty estimates (σ_E, σ_N, σ_U)
  - Link to download detailed report (PDF)

**While waiting:**
- No need to keep browser open
- Check email periodically
- Processing runs on AUSPOS server (independent of your computer)

---

## Step 3: Downloading and Interpreting PPP Results

### AUSPOS Results Email

**Typical AUSPOS results email:**

```
Subject: AUSPOS Processing Results - base_20241114_survey.obs

Your RINEX file has been processed successfully.

Station: base_20241114_survey
Session: 2024/11/14 09:00:00 - 17:30:00 (8.5 hours)
Reference Frame: ITRF2020 (Epoch 2024.87)

COORDINATES (WGS84 Geographic):
Latitude:   -5° 14' 04.44123"  ±0.015m
Longitude: 104° 34' 04.40201"  ±0.012m
Ellipsoidal Height: 141.523m   ±0.025m

COORDINATES (Cartesian XYZ):
X: -1234567.890m  ±0.012m
Y: 5678901.234m   ±0.015m
Z: -987654.321m   ±0.018m

Processing Quality: Excellent
Number of Observations: 28,456
Satellite Systems: GPS, GLONASS, Galileo
```

**Key information from email:**

**Session duration:** 8.5 hours
- Confirms data duration (should match survey session)
- Longer duration → better accuracy (diminishing returns beyond 12 hours)

**Uncertainty estimates:** ±0.015m horizontal, ±0.025m vertical
- Typical PPP accuracy for 8-hour session
- Compare to survey-in accuracy: ~0.25m (10× improvement!)

**Coordinates provided:**
- **Geographic (lat/lon/height):** Most common format, but requires conversion to UTM
- **Cartesian XYZ:** ECEF coordinates (Earth-Centered, Earth-Fixed), less intuitive

**Processing quality:** Excellent/Good/Fair/Poor
- Excellent: High confidence results (use as-is)
- Good: Acceptable results (verify with cross-checks)
- Fair: Marginal quality (use with caution, note larger uncertainty)
- Poor: Unreliable results (consider re-processing or re-survey)

### Downloading Detailed Report

**AUSPOS email includes download link:**
- "Download detailed report (PDF): [link]"
- Click link to download full processing report

**Report contains:**
- Coordinate estimates in multiple formats (ITRF, GDA, WGS84)
- Uncertainty ellipse (horizontal and vertical error estimates)
- Processing statistics (number of satellites, observation quality)
- Time series plots (position variation during session)
- Residuals (observation fit quality)

**Review report for quality assurance:**
- Check coordinate repeatability (position should be stable throughout session)
- Verify satellite count (should be 10-20+ satellites throughout)
- Inspect residuals (should be small, <5 cm typically)

**Archive report with survey data:**
- Save PDF: `base_20241114_survey_AUSPOS_report.pdf`
- Include in survey archive (documents PPP processing)

### Converting Geographic Coordinates to UTM

**AUSPOS provides coordinates in WGS84 Geographic (latitude, longitude, ellipsoid height):**
- Latitude: -5° 14' 04.44123" (degrees, minutes, seconds)
- Longitude: 104° 34' 04.40201"
- Ellipsoid Height: 141.523m

**OpenRiverCam survey uses UTM (Universal Transverse Mercator):**
- Example: EPSG:32748 (UTM Zone 48 South)
- Need: Easting, Northing, Elevation (in meters)

**Conversion required: Geographic → UTM**

**Method 1: Online coordinate converter (quick and easy)**

**Using EPSG.io:**
1. Navigate to: https://epsg.io/transform
2. Input CRS: Select "EPSG:4326 - WGS 84 (geographic)"
3. Output CRS: Select "EPSG:32748 - WGS 84 / UTM zone 48S" (or your UTM zone)
4. Input coordinates:
   - Format: Decimal degrees (convert DMS to decimal first if needed)
   - Latitude: -5.234567° (convert from -5° 14' 04.44123")
   - Longitude: 104.567890° (convert from 104° 34' 04.40201")
5. Click "Transform"
6. Output displayed:
   - Easting: 685432.15m
   - Northing: 9456782.33m
7. Elevation: Use ellipsoid height from AUSPOS: 141.523m

**Convert DMS (degrees-minutes-seconds) to decimal degrees:**
```
Latitude: -5° 14' 04.44123"
= -(5 + 14/60 + 4.44123/3600)
= -5.234567° (decimal degrees)

Longitude: 104° 34' 04.40201"
= 104 + 34/60 + 4.40201/3600
= 104.567890° (decimal degrees)
```

**Method 2: QGIS coordinate transformation**

**Using QGIS "Coordinate Capture" or "Layer creation":**
1. Open QGIS, set project CRS to EPSG:32748 (UTM 48S)
2. Layer → Create Layer → New Temporary Scratch Layer
3. Geometry type: Point, CRS: EPSG:4326 (WGS84 Geographic)
4. Add point manually:
   - Edit mode → Add Point Feature
   - Enter coordinates: Lon=104.567890, Lat=-5.234567
   - Save
5. Export layer with reprojection:
   - Right-click layer → Export → Save Features As
   - CRS: EPSG:32748 (UTM 48S)
   - Export
6. Open attribute table of exported layer:
   - Add geometry columns: E, N (uses Field Calculator with `$x`, `$y`)
   - Read Easting and Northing values

**Method 3: Command-line (GDAL/PROJ)**

**Using cs2cs (PROJ tool):**
```bash
echo "104.567890 -5.234567" | cs2cs EPSG:4326 EPSG:32748 -f "%.2f"
```
Output:
```
685432.15  9456782.33
```

**Record PPP-corrected base station coordinates in UTM:**
- E_ppp = 685432.15m
- N_ppp = 9456782.33m
- Z_ppp = 141.52m (or 141.523m with full precision)

---

## Step 4: Calculate Translation Vector

### Survey-In vs. PPP Coordinates

**Your survey used base station survey-in coordinates (local reference):**
- Recorded during field survey (Section 9.4, base station setup)
- Example from survey notes:
  - E_survey = 685431.89m
  - N_survey = 9456782.15m
  - Z_survey = 141.75m

**PPP processing provides corrected coordinates (global reference):**
- From AUSPOS results (previous step):
  - E_ppp = 685432.15m
  - N_ppp = 9456782.33m
  - Z_ppp = 141.52m

**The differences represent the survey-in error** (deviation from true global position).

### Calculating Translation Vector

**Translation vector = PPP coordinates - Survey coordinates:**

```
ΔE = E_ppp - E_survey
ΔN = N_ppp - N_survey
ΔZ = Z_ppp - Z_survey
```

**Example calculation:**
```
E_ppp = 685432.15m    E_survey = 685431.89m
N_ppp = 9456782.33m   N_survey = 9456782.15m
Z_ppp = 141.52m       Z_survey = 141.75m

ΔE = 685432.15 - 685431.89 = +0.26m (26 cm east)
ΔN = 9456782.33 - 9456782.15 = +0.18m (18 cm north)
ΔZ = 141.52 - 141.75 = -0.23m (23 cm down)
```

**Translation vector: ΔE = +0.26m, ΔN = +0.18m, ΔZ = -0.23m**

**Interpreting the translation:**
- Positive ΔE: True position is 26 cm EAST of survey-in position
- Positive ΔN: True position is 18 cm NORTH of survey-in position
- Negative ΔZ: True position is 23 cm LOWER than survey-in position

**Magnitude of shift:**
```
Horizontal shift = √(ΔE² + ΔN²) = √(0.26² + 0.18²) = 0.32m (32 cm)
3D shift = √(ΔE² + ΔN² + ΔZ²) = √(0.26² + 0.18² + 0.23²) = 0.41m (41 cm)
```

**This ~40 cm total shift is typical for 30-60 minute survey-in** (matches expected accuracy).

**If shift is larger (>1m):**
- Check coordinate system consistency (UTM zone match?)
- Verify conversion calculations (DMS to decimal, geographic to UTM)
- Review survey-in duration and conditions (adequate satellites, stable position?)

**If shift is very small (<5 cm):**
- Excellent survey-in conditions (uncommon but possible)
- Or error in calculations (verify PPP coordinates match survey CRS)

### Documenting Translation Vector

**Record translation vector in survey processing log:**

```
SURVEY PROCESSING LOG
Site: [Site name]
Survey Date: 2024-11-14
Processing Date: 2024-11-16

BASE STATION COORDINATES:

Survey-In (Local Reference):
E_survey = 685431.89m
N_survey = 9456782.15m
Z_survey = 141.75m
CRS: EPSG:32748 (WGS 84 / UTM Zone 48S)

PPP Corrected (Global Reference):
E_ppp = 685432.15m
N_ppp = 9456782.33m
Z_ppp = 141.52m
CRS: EPSG:32748 (WGS 84 / UTM Zone 48S)
PPP Service: AUSPOS
Session: 8.5 hours
Uncertainty: ±0.015m H, ±0.025m V

TRANSLATION VECTOR:
ΔE = +0.26m
ΔN = +0.18m
ΔZ = -0.23m
Horizontal shift: 0.32m
3D shift: 0.41m

CORRECTION TO BE APPLIED:
All survey point coordinates will be shifted by:
E_corrected = E_survey + 0.26m
N_corrected = N_survey + 0.18m
Z_corrected = Z_survey - 0.23m
```

**Save this documentation** - critical for understanding coordinate transformations and validating results.

---

## Step 5: Apply Corrections in QGIS

### Data Import and Preparation

**From SURVEY_PROCESS.md Section 10, Step 3:**
```
Apply PPP Translation:
- Open Field Calculator for each layer in Geopackage
- Create new fields: E_corrected = "x_coord" + ΔE, N_corrected = "y_coord" + ΔN, Z_corrected = "z_coord" + ΔZ
- Calculate bed elevations: bed_elevation = Z_corrected - pole_height
- Update geometry: Use "Update Geometry" tool with corrected coordinates
```

**Complete procedure:**

**Step 1: Open QGIS and load survey data**
- Launch QGIS
- File → New Project
- Layer → Add Layer → Add Vector Layer
- Source: Select exported Geopackage (e.g., `site_20241114_survey.gpkg`)
- Add all layers:
  - Ground Control Points
  - Cross Section (Discharge and Level)
  - Water Level
  - Camera Location
  - Check Points

**Step 2: Verify data imported correctly**
- Check attribute tables (pole_height, point_id, etc. present?)
- Verify geometries (points displayed on map?)
- Confirm CRS (layer properties → should be EPSG:32748)

**Step 3: Save project**
- File → Save Project As
- Filename: `site_20241114_PPP_processing.qgz`
- Enables resuming work if interrupted

### Field Calculator - Create Corrected Coordinate Fields

**Process each layer separately (start with Ground Control Points layer):**

**Step 1: Open Attribute Table**
- Right-click "Ground Control Points" layer → Open Attribute Table

**Step 2: Enable editing**
- Click "Toggle Editing Mode" button (pencil icon)
- Layer becomes editable (yellow highlight in Layers panel)

**Step 3: Open Field Calculator**
- Click "Open Field Calculator" button (abacus icon)
- Field Calculator dialog opens

**Step 4: Create E_corrected field**
- Check "Create a new field"
- Output field name: `E_corrected`
- Output field type: Decimal number (real)
- Output field length: 10
- Precision: 2 (two decimal places: 685432.15)

**Step 5: Enter correction expression**

**In Expression box, enter:**
```
"x_coord" + 0.26
```

Replace `0.26` with your actual ΔE value (from translation vector calculation).

**Alternative if using geometry directly:**
```
$x + 0.26
```

**Step 6: Click OK**
- QGIS calculates E_corrected for all features
- New column appears in Attribute Table

**Step 7: Repeat for N_corrected**
- Field Calculator → Create new field
- Output field name: `N_corrected`
- Expression: `"y_coord" + 0.18` (replace 0.18 with your ΔN)
- Or: `$y + 0.18`
- Click OK

**Step 8: Repeat for Z_corrected**
- Field Calculator → Create new field
- Output field name: `Z_corrected`
- Expression: `"z_coord" - 0.23` (replace -0.23 with your ΔZ, note sign!)
- Or: `$z - 0.23`
- Click OK

**Verify calculations:**
- Scroll through Attribute Table
- Spot-check several features:
  - E_corrected = x_coord + ΔE? ✓
  - N_corrected = y_coord + ΔN? ✓
  - Z_corrected = z_coord + ΔZ? ✓

**Step 9: Calculate bed elevation (for cross-section and GCPs)**

**Create bed_elevation field:**
- Field Calculator → Create new field
- Output field name: `bed_elevation`
- Expression: `"Z_corrected" - "pole_height"`
- Click OK

**This combines PPP correction with pole height adjustment** (two corrections in one step):
```
bed_elevation = (z_coord + ΔZ) - pole_height
              = Z_corrected - pole_height
```

**Step 10: Save edits**
- Click "Save Edits" button (floppy disk icon)
- Changes written to Geopackage
- Click "Toggle Editing Mode" to exit editing

**Step 11: Repeat for all layers**
- Repeat Field Calculator process for:
  - Cross Section layers (Discharge and Level)
  - Water Level layer
  - Camera Location
  - Check Points
- Same expressions, same translation vector (ΔE, ΔN, ΔZ consistent across all layers)

### Update Geometry with Corrected Coordinates

**Geometry must be updated to match corrected coordinates:**

**Current state:**
- Geometry (point positions on map): Old survey-in coordinates (E_survey, N_survey, Z_survey)
- Attributes (E_corrected, N_corrected, Z_corrected): New PPP-corrected coordinates
- **Mismatch:** Points plot in wrong locations (not updated yet)

**Update geometry to corrected coordinates:**

**Method 1: Using "Geometry by Expression" (QGIS 3.x)**

**Step 1: Open Processing Toolbox**
- Processing menu → Toolbox
- Search: "Geometry by expression"
- Double-click "Geometry by expression" tool

**Step 2: Configure tool**
- Input layer: Ground Control Points
- Geometry type: Point
- Expression:
  ```
  make_point("E_corrected", "N_corrected", "Z_corrected")
  ```
- Output: Save to Geopackage
  - Filename: Same Geopackage (`site_20241114_survey.gpkg`)
  - Layer name: `GCP_corrected`

**Step 3: Run**
- Click "Run"
- New layer created: `GCP_corrected` with updated geometry

**Step 4: Verify**
- New layer should be shifted relative to original
- Shift magnitude: ~0.4m (your translation vector magnitude)
- Zoom in to compare old vs. new point positions

**Step 5: Replace original layer**
- Remove old "Ground Control Points" layer
- Rename "GCP_corrected" to "Ground Control Points"
- Or keep both for comparison (label clearly)

**Method 2: Using Field Calculator to update existing geometry**

**WARNING: This overwrites existing geometry (backup Geopackage first!)**

**Step 1: Enable editing (Attribute Table)**
- Toggle Editing Mode

**Step 2: Open Field Calculator**
- Check "Update existing field"
- Field to update: (Select geometry field, may be named "geom" or "geometry")

**Step 3: Expression**
```
make_point("E_corrected", "N_corrected", "Z_corrected")
```

**Step 4: OK and Save**
- Geometry updated in place
- Points now plot at corrected positions

**Repeat geometry update for all layers.**

### Validation and Quality Control

**After applying corrections and updating geometry:**

**Check 1: Coordinate shift magnitude**
- Compare original and corrected point positions
- Measure distance: Should equal translation vector magnitude (~0.4m in example)
- Use QGIS Measure tool to verify shift

**Check 2: Relative positions unchanged**
- Distance between two GCPs should be IDENTICAL before and after correction
- Translation shifts all points together (does not change relative positions)
- Measure GCP01 to GCP02 distance in original layer: 12.35m
- Measure GCP01 to GCP02 distance in corrected layer: Should also be 12.35m (within 1 cm)

**If relative distances changed:** ERROR - correction applied inconsistently or geometry update failed

**Check 3: Base map alignment (if available)**
- Add satellite imagery base map (Google, Bing, ESRI)
- Overlay corrected survey points
- Verify alignment: Points should match visible features (riverbanks, roads, structures)
- Original survey points (local frame): May be offset 20-40 cm from imagery
- Corrected points (global frame): Should align better (within 5-10 cm)

**Check 4: Bed elevations recalculated correctly**
- Verify: `bed_elevation = Z_corrected - pole_height`
- Spot-check several features manually
- Example:
  ```
  z_coord = 142.10m
  pole_height = 2.85m
  ΔZ = -0.23m

  Z_corrected = 142.10 - 0.23 = 141.87m
  bed_elevation = 141.87 - 2.85 = 139.02m  ✓ Correct
  ```

**Check 5: Check point repeatability (if check points surveyed)**
- Check points measured at CP_START, CP_NOON, CP_END (Section 9.10)
- After PPP correction, check point coordinates should still agree within 3 cm
- Example:
  ```
  CP_START (corrected): E=685435.10, N=9456783.20, Z=140.15
  CP_NOON (corrected):  E=685435.12, N=9456783.18, Z=140.17
  CP_END (corrected):   E=685435.11, N=9456783.21, Z=140.14

  Agreement: <3cm ✓ Excellent
  ```

**If check point repeatability degraded after PPP correction:** ERROR - verify translation vector applied correctly

---

## Step 6: Export Corrected Data

### Save Corrected Geopackage

**Step 1: Save all edits**
- Verify all layers saved (no unsaved changes)
- File → Save Project

**Step 2: Export corrected Geopackage (archival)**
- Right-click layer → Export → Save Features As
- Format: Geopackage
- File name: `site_20241114_survey_PPP_corrected.gpkg`
- CRS: EPSG:32748 (should be unchanged)
- Select all layers for export
- Click OK

**Corrected Geopackage contains:**
- Original survey coordinates (x_coord, y_coord, z_coord)
- Corrected coordinates (E_corrected, N_corrected, Z_corrected)
- Bed elevations (bed_elevation)
- Updated geometry (points at corrected positions)

**Archive this Geopackage** - permanent record of PPP-corrected survey data.

### Export XYZ for PtBox (Final Step)

**From SURVEY_PROCESS.md Section 10, Step 4:**
```
Create XYZ Point Cloud:
- Select cross-section and control point layers from corrected Geopackage
- Export as CSV with GEOMETRY=AS_XYZ
```

**Complete procedure:**

**Step 1: Select Ground Control Points layer (corrected)**
- Right-click "Ground Control Points" (corrected geometry)
- Export → Save Features As

**Step 2: Configure CSV export**
- Format: Comma Separated Value [CSV]
- File name: `site_20241114_GCP_PPP_corrected.xyz`
- CRS: EPSG:32748
- Layer Options:
  - Add: `GEOMETRY=AS_XYZ`
  - Add: `CREATE_CSVT=NO`
- Geometry: Points (will export XYZ coordinates)

**Step 3: Export**
- Click OK
- XYZ file created

**Step 4: Verify XYZ file**

**Open in text editor:**
```
X,Y,Z
685432.41,9456782.51,139.25
685435.46,9456785.28,139.45
685440.76,9456780.73,140.15
...
```

**Verify:**
- Coordinates = Corrected coordinates (E_corrected, N_corrected, bed_elevation)
- NOT original survey coordinates
- Shift of ~0.4m applied

**Optional: Compare to uncorrected XYZ**
- Export XYZ from original layer (before corrections)
- Compare coordinates in text editor
- Difference should equal translation vector (ΔE, ΔN, ΔZ)

**Step 5: Remove header row if needed (for PtBox compatibility)**
- Delete first line: `X,Y,Z`
- Or convert delimiter to space (see Section 9.14)
- Save as: `site_20241114_GCP_PPP_corrected.xyz`

**This XYZ file is ready for PtBox import** - contains PPP-corrected ground control point coordinates with 2-10 cm absolute accuracy.

---

## Quality Control for Entire PPP Workflow

### Validation Checklist

**Before finalizing PPP-corrected data, verify:**

- [ ] CONVBIN conversion successful (RINEX files created, sensible size)
- [ ] AUSPOS processing completed (email received with results)
- [ ] PPP uncertainty acceptable (horizontal ±5 cm, vertical ±10 cm or better)
- [ ] Translation vector calculated correctly (ΔE, ΔN, ΔZ from PPP - Survey)
- [ ] Translation magnitude reasonable (typically 10-50 cm, rarely >1m)
- [ ] Corrections applied to all layers consistently (same ΔE, ΔN, ΔZ for all)
- [ ] Bed elevations recalculated (bed_elevation = Z_corrected - pole_height)
- [ ] Geometry updated to corrected coordinates (points shifted on map)
- [ ] Relative positions unchanged (distances between points preserved)
- [ ] Check point repeatability maintained (<3 cm agreement)
- [ ] Corrected Geopackage saved and archived
- [ ] XYZ file exported with corrected coordinates
- [ ] PPP processing documented (translation vector, AUSPOS report archived)

### Common Errors and Troubleshooting

**Error: Translation vector very large (>1m)**

**Symptoms:**
- ΔE or ΔN or ΔZ > 1.0m (much larger than expected)

**Possible causes:**
- Survey-in coordinates recorded incorrectly (typo, wrong CRS)
- PPP coordinates converted to wrong UTM zone
- PPP coordinates in different CRS than survey coordinates

**Diagnosis:**
- Verify survey-in coordinates from field notes
- Verify PPP conversion (lat/lon → UTM zone match?)
- Check CRS consistency (both EPSG:32748?)

**Solutions:**
- Recalculate PPP coordinates in correct UTM zone
- Verify survey-in coordinates (check base station setup notes)
- If large shift is real (poor survey-in conditions): Accept large translation

**Error: Bed elevations dramatically wrong after correction**

**Symptoms:**
- Bed elevations too high or too low by >1m
- Water depths negative or impossibly large

**Possible causes:**
- ΔZ sign error (applied +ΔZ instead of -ΔZ, or vice versa)
- Pole height not subtracted (bed_elevation = Z_corrected, missing - pole_height)
- Translation applied twice (correction added to already-corrected coordinates)

**Diagnosis:**
- Recalculate one feature manually: bed_elevation = (z_coord + ΔZ) - pole_height
- Compare to Field Calculator result
- Check for duplicate correction (translation applied twice)

**Solutions:**
- Recalculate with correct formula and sign
- Start fresh from original export (before any corrections)

**Error: Geometry not updated (points still in wrong location)**

**Symptoms:**
- Attribute table shows E_corrected, N_corrected, Z_corrected (correct)
- Map shows points in original location (not shifted)

**Cause:**
- Geometry update step skipped or failed

**Solution:**
- Run "Geometry by expression" tool: `make_point("E_corrected", "N_corrected", "Z_corrected")`
- Or use Field Calculator to update geometry field directly

**Error: Relative positions changed after correction**

**Symptoms:**
- Distance between two GCPs changed by >5 cm after correction
- Cross-section profile shape changed

**Cause:**
- Translation applied inconsistently (different ΔE, ΔN, ΔZ for different features)
- Error in Field Calculator expression (typo, wrong field referenced)

**Solution:**
- Verify same translation vector used for all features
- Recalculate corrections from original data
- Check Field Calculator expressions for typos

---

## Connection to SURVEY_PROCESS.md and Chapter 5

### Complete Workflow Integration

**From field to final data:**

**DAY 1: FIELD SURVEY (SURVEY_PROCESS.md Sections 1-9)**
- Base station setup, survey-in, RINEX logging started
- Rover survey: GCPs, cross-sections, water level, check points
- RINEX logging stopped, survey data exported

**DAY 2-7: POST-PROCESSING (SURVEY_PROCESS.md Section 10 = This Section 9.15)**
1. Convert UBX to RINEX (CONVBIN)
2. Submit to AUSPOS (PPP processing)
3. Download results, convert to UTM
4. Calculate translation vector (ΔE, ΔN, ΔZ)
5. Apply corrections in QGIS (Field Calculator)
6. Update geometry (Geometry by Expression)
7. Export corrected XYZ (ready for PtBox)

**NEXT: CAMERA CONFIGURATION (Chapter 10 or separate manual)**
- Import XYZ into PtBox
- Click GCPs in image
- Calculate transformation
- Validate reprojection errors
- Configure camera for discharge monitoring

### Conceptual Foundation (Chapter 5 Connection)

**From Section 5.6 (PPP Concepts):**

**Concept:** Base station survey-in provides local reference (~25 cm absolute accuracy). PPP improves to global reference (2-10 cm absolute accuracy) using global reference networks and precise satellite orbits.

**Practice (this section):** AUSPOS provides PPP using IGS/APREF stations and precise ephemeris. Translation vector shifts all survey coordinates from local reference to global reference. Absolute accuracy improved 10×, relative accuracy unchanged.

**Concept:** Rover measurements are relative to base station (1-3 cm relative accuracy). Correcting base station position automatically corrects all rover measurements.

**Practice (this section):** Translation vector calculated from base station correction applies to all survey points (GCPs, cross-sections, water level). One correction improves entire survey.

**Concept:** PPP requires multi-hour observation session (2+ hours minimum, 6-12 hours recommended).

**Practice (this section):** RINEX logging duration 6-12 hours (field survey). AUSPOS processes entire session. Longer sessions → better accuracy (diminishing returns beyond 12 hours).

**Concept:** PPP accuracy degrades with shorter sessions. 2-hour session: ±5-10 cm. 6-hour session: ±2-5 cm. 24-hour session: ±1-3 cm.

**Practice (this section):** AUSPOS reports uncertainty estimates. Verify ≤5 cm horizontal, ≤10 cm vertical (acceptable for GCP transformation). Longer sessions provide better results (if field conditions allow).

---

## Summary: PPP Corrections Workflow

**Purpose:**
- Improve absolute coordinate accuracy from ~25 cm (survey-in) to 2-10 cm (PPP)
- Shift all survey points from local reference frame to global reference frame
- Enable integration with satellite imagery, base maps, and other geospatial data
- Provide highest-quality coordinates for PtBox GCP transformation

**Critical steps:**

1. **Convert UBX to RINEX (CONVBIN):**
   - Command: `convbin -od -os -oi -ot -f 1 base_file.ubx`
   - Output: .obs and .nav files

2. **Submit to AUSPOS:**
   - Upload .obs file
   - Select antenna type (TRM29659.00 or closest match)
   - Enter antenna height (measured during base station setup)
   - Wait for processing (30 min - 24 hours)

3. **Download and convert PPP results:**
   - Email contains lat/lon/height (WGS84 geographic)
   - Convert to UTM (same zone as survey): E_ppp, N_ppp, Z_ppp
   - Document uncertainty (should be ±2-5 cm H, ±5-10 cm V)

4. **Calculate translation vector:**
   - ΔE = E_ppp - E_survey
   - ΔN = N_ppp - N_survey
   - ΔZ = Z_ppp - Z_survey

5. **Apply corrections in QGIS:**
   - Field Calculator: Create E_corrected, N_corrected, Z_corrected
   - Expressions: `"x_coord" + ΔE`, `"y_coord" + ΔN`, `"z_coord" + ΔZ`
   - Calculate bed_elevation: `"Z_corrected" - "pole_height"`

6. **Update geometry:**
   - Geometry by Expression: `make_point("E_corrected", "N_corrected", "Z_corrected")`
   - Points shift on map (~0.3-0.5m typically)

7. **Export corrected data:**
   - Save corrected Geopackage (archive)
   - Export XYZ for PtBox (final GCP coordinates)

**Quality control:**
- Translation magnitude reasonable (10-50 cm typical)
- PPP uncertainty acceptable (≤5 cm H, ≤10 cm V)
- Relative positions unchanged (distances preserved)
- Check point repeatability maintained
- Bed elevations recalculated correctly

**Workflow completion:**
- **FIELD SURVEY COMPLETE** (Sections 9.1 - 9.11)
- **POST-PROCESSING COMPLETE** (Sections 9.12 - 9.15)
- **SURVEY DATA READY** for PtBox camera configuration
- **NEXT CHAPTER:** Camera configuration, transformation validation, operational discharge monitoring

---

**This completes Chapter 9: Site Survey.** Your survey data has been collected with centimeter-level relative accuracy, processed through pole height adjustments and water level calculations, and improved to centimeter-level absolute accuracy through PPP corrections. The corrected XYZ ground control points are ready for PtBox import and camera transformation configuration.

**Next steps:** Import GCP XYZ into PtBox, click GCP locations in camera image, calculate transformation, validate reprojection errors, and begin operational discharge monitoring with OpenRiverCam.

---

**Chapter 9 Complete - All Sections Finished**
