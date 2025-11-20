# 5.6 Logging, RINEX, and PPP Corrections

This section addresses a critical question: After completing your RTK survey with centimeter-level relative accuracy, how do you improve the absolute position accuracy of your data?

Your RTK survey achieves excellent relative accuracy (1-3 cm between surveyed points), but the absolute geographic position has moderate accuracy (~25 cm) limited by the base station survey-in process. For many applications, this absolute accuracy is inadequate:

- Integrating survey data with satellite imagery or maps
- Comparing surveys from different dates or different base station setups
- Providing data for hydrologic modeling or engineering design
- Meeting requirements for official mapping or cadastral work

**Post-Processed Kinematic (PPP) correction solves this problem** by improving the base station position from ~25 cm to 2-10 cm absolute accuracy. This correction is then applied to all survey points, improving their absolute accuracy while maintaining the excellent relative accuracy.

This section explains the complete workflow:
- Why raw data logging matters during field surveys
- What RINEX format is and why it is needed
- How PPP (Precise Point Positioning) works
- When to use PPP corrections
- Step-by-step PPP processing workflow
- Expected accuracy improvements and limitations

**Complexity warning:** This is the most technically complex section in Chapter 5. The concepts involve satellite orbit refinement, atmospheric modeling, and post-processing workflows. However, the practical implementation (as detailed in SURVEY_PROCESS.md) is straightforward: convert files, upload to service, apply corrections. You do not need to understand the mathematics to successfully use PPP.

---

## Why Log Raw GNSS Data?

During your field survey, the base station should continuously log raw satellite observations in addition to broadcasting real-time corrections to the rover.

### What Raw Data Captures

**Raw GNSS data logging records:**

**Carrier phase measurements:**
- Precise measurements of GPS signal wave cycles from each satellite
- Same measurements used for RTK positioning
- Recorded every second (1 Hz typical) or faster

**Pseudorange measurements:**
- Travel time from satellite to receiver
- Less precise than carrier phase, but helps resolve ambiguities

**Satellite ephemeris (broadcast):**
- Orbital position data transmitted by satellites
- Approximate satellite positions (accurate to ~1-2 meters)
- This is what satellites broadcast in real-time

**Observation metadata:**
- Timestamp for each measurement
- Satellite ID (which satellite measured)
- Signal strength, quality indicators
- Receiver position estimates

**What is NOT captured in real-time RTK:**
- **Precise ephemeris:** More accurate satellite orbit data (accurate to ~5 cm)
- **Satellite clock corrections:** Precise satellite clock error data
- **Ionospheric/tropospheric models:** Refined atmospheric delay models

**These precise products become available hours to days after the satellite observations, published by analysis centers (IGS - International GNSS Service, and others).**

**This is why raw data logging matters:** You record observations in the field using broadcast ephemeris (~1-2m satellite position accuracy). Later, you reprocess using precise ephemeris (~5cm satellite position accuracy) to improve your position solution.

### The Base Station vs Rover Logging

**Base station logging:**
- **Required for PPP post-processing**
- Base station is stationary, so observations are ideal for PPP
- Logged data will be post-processed to determine improved base position
- Correction (improved base position - survey-in position) applied to all rover survey points

**Rover logging:**
- **Not typically needed for OpenRiverCam surveys**
- Rover measurements already relative to base with centimeter accuracy
- Post-processing rover data (PPK - Post-Processed Kinematic) is possible but adds complexity
- For standard workflow: Only base station raw data is required

**From SURVEY_PROCESS.md workflow:**
- Log base station raw data entire survey session (6-12 hours)
- Convert base station UBX log to RINEX format
- Submit base station RINEX to PPP service (AUSPOS)
- Receive improved base station coordinates
- Calculate correction: PPP base position - survey-in base position
- Apply this correction to all rover survey points

**This workflow improves absolute accuracy of entire survey with single PPP processing task.**

### File Formats and Storage

**Native logging format (u-blox receivers):**
- UBX format: u-blox proprietary binary format
- Efficient storage (50-200 MB per day of logging)
- Contains all raw observation data needed for post-processing
- Requires conversion to RINEX for use with PPP services

**Storage requirements:**
- Typical: 10-20 MB per hour of logging
- 8-hour survey session: 80-160 MB
- Multiple days: Plan for 500 MB - 1 GB storage
- Use sufficient capacity SD card or computer storage

**Backup raw data:**
- Raw observation data is irreplaceable (cannot be re-created after survey)
- Make multiple backups immediately after survey
- Copy to separate devices (computer, cloud storage, external drive)
- Verify file integrity before deleting from field equipment

**Data retention:**
- Keep raw data for entire project duration
- May need to reprocess with different parameters or newer precise products
- Archive long-term for future reference or validation

---

## RINEX Format Overview

RINEX (Receiver Independent Exchange Format) is the standard format for exchanging GNSS observation data between different receiver types and processing software.

### What is RINEX and Why It Exists

**The problem RINEX solves:**

Different GNSS receiver manufacturers use different proprietary formats:
- u-blox: UBX format
- Trimble: RT17, T02, DAT formats
- Leica: MDB format
- Septentrio: SBF format
- Etc.

**Post-processing software needs a common format** to accept data from any receiver type.

**RINEX provides this standard:**
- Defined by IGS (International GNSS Service)
- ASCII text format (human-readable, easy to debug)
- Contains all observation data needed for precise positioning
- Supported by all professional GNSS post-processing software
- PPP services require RINEX format for submission

**Analogy:** RINEX is like PDF for documents - a standard format that any software can read, regardless of what software originally created the data.

### RINEX File Types

A complete RINEX dataset consists of multiple files:

**Observation file (.obs or .YYo extension):**
- Contains carrier phase and pseudorange measurements
- Organized by time (epoch) and satellite
- This is the main file for PPP processing
- Example filename: `base001a.24o` (observation file, day 001, year 2024)

**Navigation file (.nav or .YYn extension):**
- Contains satellite ephemeris (broadcast orbital data)
- Orbital positions for satellites during observation period
- Example filename: `base001a.24n` (navigation file)

**Meteorological file (.met, optional):**
- Weather data (temperature, pressure, humidity)
- Helps refine tropospheric delay models
- Not typically recorded by basic RTK receivers

**RINEX versions:**
- RINEX 2.x: Older standard, still widely supported
- RINEX 3.x: Current standard, supports multiple GNSS constellations better
- RINEX 4.x: Newest, not yet universally supported

**For PPP processing, RINEX 2.x or 3.x observation files are required.** Most PPP services accept either version.

### RINEX File Structure (High-Level)

You do not need to understand RINEX format in detail, but seeing its structure helps demystify the format.

**RINEX observation file structure:**

```
HEADER SECTION (metadata)
- Format version
- Receiver type, antenna type
- Approximate position
- Observation types recorded
- First/last observation time
- Antenna height
END OF HEADER

OBSERVATION SECTION (measurements)
> 2024 11 14 10 00 00.0000000  Epoch timestamp
G01  23456789.123  123456789.123  ...   GPS satellite 1 measurements
G03  24567890.234  134567890.234  ...   GPS satellite 3 measurements
G07  25678901.345  145678901.345  ...   GPS satellite 7 measurements
...
> 2024 11 14 10 00 01.0000000  Next epoch (1 second later)
G01  23456790.456  123456790.456  ...
...
(continues for entire observation session)
```

**Key information in header:**
- **Antenna type:** Critical for PPP (affects where antenna measures position)
- **Antenna height:** Height from ground to Antenna Reference Point
- **Approximate position:** Rough location (survey-in coordinates)

**Observation measurements:**
- Each epoch (time point) lists all visible satellites
- Multiple measurements per satellite (carrier phase on L1, L2, pseudorange, etc.)
- Organized for efficient processing by software

**PPP services read RINEX files and:**
- Extract carrier phase and pseudorange measurements
- Combine with precise ephemeris (downloaded from IGS)
- Apply atmospheric models
- Calculate precise receiver position

**You do not manually edit RINEX files.** Conversion software (RTKLIB CONVBIN, RTKCONV) handles creation from UBX format. PPP services automatically read and process RINEX data.

---

## Converting UBX to RINEX

Your base station logs data in UBX format (u-blox proprietary). PPP services require RINEX format. Conversion is straightforward using RTKLIB software.

### RTKLIB CONVBIN Command-Line Conversion

**From SURVEY_PROCESS.md procedure (recommended method):**

**Step 1: Install RTKLIB**
- Download RTKLIB (free, open-source): http://www.rtklib.com/
- Extract to folder on computer
- CONVBIN executable located in `bin/` folder

**Step 2: Open command prompt/terminal**
- Navigate to folder containing your UBX file
- Example: `cd C:\Survey_Data\2024-11-14_RiverSurvey\`

**Step 3: Run CONVBIN conversion**

**Basic conversion command:**
```
convbin -od -os -oi -ot -f 1 your_file.ubx
```

**Parameter explanation:**
- `-od`: Output observation data (.obs file)
- `-os`: Output satellite ephemeris (.nav file)
- `-oi`: Output ionosphere parameters
- `-ot`: Output time system parameters
- `-f 1`: RINEX version 1 format (some services prefer this)
- `your_file.ubx`: Your UBX log file from base station

**Example actual command:**
```
convbin -od -os -oi -ot -f 1 base_20241114_survey.ubx
```

**Output files created:**
- `base_20241114_survey.obs` - Observation file (main file for PPP)
- `base_20241114_survey.nav` - Navigation file (satellite ephemeris)

**Alternative: Convert specific time range**

If your UBX file is very large (24-hour continuous logging) but you only surveyed for 8 hours, extract just the relevant time range:

```
convbin -od -os -ts 2024/11/14 09:00:00 -te 2024/11/14 17:00:00 base_20241114_survey.ubx
```

**Parameters:**
- `-ts`: Start time (YYYY/MM/DD HH:MM:SS)
- `-te`: End time

**This creates RINEX files containing only the specified time window,** reducing file size and PPP processing time.

### RTKCONV GUI Conversion (Alternative)

If command-line conversion fails or you prefer graphical interface:

**Step 1: Launch RTKCONV**
- Open RTKCONV (included in RTKLIB package)
- GUI application with file selection dialogs

**Step 2: Select input file**
- Click "..." button next to "Input File" field
- Browse to your UBX file, select it

**Step 3: Configure conversion options**
- Click "Options" button
- Set "Input Format": u-blox UBX
- Set "Output Format": RINEX OBS/NAV
- Set "RINEX Version": 2.10 or 3.03 (either acceptable for PPP)

**Step 4: Convert**
- Click "Convert" button
- RTKCONV processes file, shows progress
- Output RINEX files saved to same folder as input UBX file

**Step 5: Verify output**
- Check that .obs and .nav files created
- Open .obs file in text editor to verify it contains data (not empty)

### Troubleshooting Conversion Problems

**Problem: "No data in output files" or conversion fails**

**Diagnosis:** UBX file may not contain raw observation messages

**Solutions:**
- Verify UBX file contains RXM-RAWX and RXM-SFRBX messages (these are raw observation messages)
- Check base station configuration - raw logging may not have been enabled
- Try different RINEX version: `-f 2` or `-f 3` instead of `-f 1`
- Verify UBX file is not corrupted (check file size - should be >10 MB for multi-hour session)

**Problem: "Unsupported RINEX version" error from PPP service**

**Solution:**
- Re-convert with different RINEX version (try `-f 2` if `-f 1` fails, or vice versa)
- Some older PPP services prefer RINEX 2.x, some newer prefer RINEX 3.x

**Problem: Very large RINEX files (>500 MB)**

**Solution:**
- Convert only needed time range using `-ts` and `-te` parameters
- Compress RINEX file (zip or gzip) before uploading to PPP service (most accept compressed files)

**Problem: "Antenna type not recognized" error from PPP service**

**Solution:**
- Edit RINEX header to specify correct antenna type (advanced - see next section)
- Or select "Unknown antenna" option in PPP service (may reduce accuracy slightly)

### Editing RINEX Header Information

**Sometimes you need to edit RINEX header** to specify antenna information correctly for PPP processing.

**Critical header fields for PPP:**

**Antenna type:**
- Must match IGS antenna database (standard antenna names)
- Example: `TRM29659.00     NONE` (Trimble multiband antenna)
- Your u-blox antenna may not be in IGS database - see "Antenna Selection for PPP" section

**Antenna height:**
- Height from ground to Antenna Reference Point (ARP)
- Must be measured accurately during field survey
- Example: `1.687` (meters)

**Approximate position:**
- Survey-in coordinates (not critical for PPP, but should be reasonably close)

**How to edit RINEX header:**

**Option 1: Use RTKLIB RTKCONV**
- RTKCONV can set antenna type and height during conversion
- Options → Set antenna type, antenna height, approximate position
- Convert UBX to RINEX with corrected header

**Option 2: Manual editing (advanced)**
- Open .obs file in text editor
- Find header lines for antenna type, height
- Edit values carefully (maintain exact spacing and format)
- Save file
- **Risk:** Easy to corrupt file if formatting wrong - only for advanced users

**For OpenRiverCam surveys using ArduSimple or similar low-cost antennas:** Antenna type may not be in IGS database. PPP services allow "Unknown" antenna type, which uses generic model (may reduce accuracy by 1-3 cm).

---

## What is PPP (Precise Point Positioning)?

PPP is a GNSS positioning technique that achieves centimeter-level absolute accuracy using a single receiver and precise satellite orbit/clock data.

### PPP vs RTK: Different Approaches to Precision

**RTK (what you use in the field):**
- Requires two receivers (base and rover)
- Base measures errors, rover applies corrections in real-time
- Achieves relative accuracy: 1-3 cm rover-to-base
- Absolute accuracy: Limited by base position (~25 cm from survey-in)
- Real-time (immediate positioning)

**PPP (what you use for post-processing base position):**
- Uses one receiver (your base station)
- Combines observations with precise satellite products (downloaded later)
- Achieves absolute accuracy: 2-10 cm in global reference frame
- Post-processed (requires waiting hours to days for precise products)
- No local reference station needed

**Why both are useful:**
- RTK gives you excellent relative accuracy for field surveying (survey points accurate relative to each other)
- PPP gives you excellent absolute accuracy for base position (base position accurate in global reference frame)
- **Combine them:** RTK for relative positioning, PPP to correct base position, apply base correction to all survey points
- **Result:** Survey data with both excellent relative accuracy AND excellent absolute accuracy

### How PPP Achieves Centimeter Accuracy

**PPP accuracy depends on four key elements:**

**1. Precise satellite ephemeris (orbital positions):**

**Broadcast ephemeris (real-time):**
- Transmitted by satellites during operation
- Satellite position accuracy: ~1-2 meters
- Available immediately

**Precise ephemeris (post-processed):**
- Calculated by IGS analysis centers using global tracking networks
- Satellite position accuracy: ~2-5 centimeters
- Available 12-24 hours after observations (ultra-rapid), or 12-18 days for final (highest accuracy)

**Impact:** Using precise ephemeris instead of broadcast improves position accuracy by ~100× (from meter-level to centimeter-level).

**2. Precise satellite clock corrections:**

Satellite atomic clocks are very accurate, but still have nanosecond-level errors. 1 nanosecond clock error = 30 cm position error.

**Broadcast clock corrections:**
- Satellite-transmitted clock error estimates
- Accuracy: ~2-5 nanoseconds (60-150 cm position error)

**Precise clock corrections:**
- Post-processed clock error data from IGS
- Accuracy: ~0.1 nanoseconds (3 cm position error)

**Impact:** Precise clock corrections remove major systematic error source.

**3. Atmospheric delay models:**

**Ionospheric delay:**
- GPS signals slow down passing through ionosphere
- Delay varies with time of day, solar activity, location
- Dual-frequency receivers can measure and remove most ionospheric delay (L1/L2 combination)
- PPP uses global ionospheric models to further refine corrections

**Tropospheric delay:**
- GPS signals slow down in lower atmosphere (water vapor)
- Delay varies with weather (temperature, pressure, humidity)
- PPP models troposphere based on meteorological data or estimates from observations

**Impact:** Atmospheric modeling removes 10-50 cm of systematic error.

**4. Carrier phase ambiguity resolution:**

PPP must resolve carrier phase ambiguities just like RTK, but without a nearby reference station.

- PPP uses long observation periods (hours) to resolve ambiguities
- Satellite geometry changes over time help constrain solutions
- Requires continuous tracking of satellites (gaps degrade accuracy)

**Impact:** Ambiguity resolution enables centimeter-level precision.

**PPP processing workflow:**
1. PPP service receives your RINEX observation file
2. Downloads precise ephemeris and clock corrections from IGS
3. Applies atmospheric models
4. Processes carrier phase and pseudorange observations
5. Resolves carrier phase ambiguities using multi-hour observation period
6. Calculates position in global reference frame (ITRF - International Terrestrial Reference Frame)
7. Outputs coordinates in WGS84 or local datum (UTM, etc.)

**You do not perform these calculations - PPP service does this automatically.** You just upload RINEX file and receive results.

### PPP Observation Time Requirements

**PPP accuracy depends heavily on observation duration:**

**Short observations (30 minutes - 2 hours):**
- Accuracy: 10-20 cm horizontal, 20-40 cm vertical
- Ambiguities partially resolved
- Limited satellite geometry changes

**Medium observations (2-6 hours):**
- Accuracy: 3-8 cm horizontal, 5-15 cm vertical
- Most ambiguities resolved
- Good satellite geometry variation
- **Typical for OpenRiverCam field surveys**

**Long observations (6-24 hours):**
- Accuracy: 2-4 cm horizontal, 3-6 cm vertical
- All ambiguities resolved
- Excellent satellite geometry variation
- Optimal for high-accuracy applications

**Multi-day observations (24+ hours):**
- Accuracy: 1-3 cm horizontal, 2-4 cm vertical
- Best possible PPP accuracy
- Typically only for permanent reference stations

**From SURVEY_PROCESS.md:**
- Base station logs for entire survey session: 6-12 hours typical
- This provides 3-8 cm absolute accuracy (adequate for OpenRiverCam)
- If higher accuracy needed: Leave base station logging overnight (24 hours)

**Practical guideline: Longer is better, but 4-8 hours is sufficient for most applications.**

### PPP Reference Frames and Datums

**PPP calculates position in ITRF (International Terrestrial Reference Frame):**
- Global geodetic reference system
- Defined by precise positions of tracking stations worldwide
- Earth-centered, Earth-fixed coordinate system
- Updates periodically: ITRF2014, ITRF2020, etc.

**Your survey data is probably in WGS84 or local datum (NAD83, GDA2020, etc.):**
- WGS84: Used by GPS, very similar to ITRF (differences <1 cm)
- Local datums: Region-specific, may differ from ITRF by decimeters to meters

**PPP services typically provide results in:**
- ITRF (XYZ Cartesian coordinates or latitude/longitude/height)
- WGS84 (latitude/longitude/height) - essentially same as ITRF for cm-level work
- Can be transformed to local datums using coordinate transformation tools

**From SURVEY_PROCESS.md workflow:**
- AUSPOS PPP service outputs WGS84 geographic coordinates (latitude, longitude, height)
- Convert to UTM Zone 48S (EPSG:32748) using coordinate transformation
- This gives you base station position in your survey's CRS

**Coordinate transformation tools:**
- Online calculators (e.g., Geoscience Australia, NOAA CORS)
- GIS software (QGIS coordinate transformation)
- Geodetic software (GeoidEval, PROJ)

**Important:** Be consistent with coordinate reference systems throughout workflow to avoid introducing errors.

---

## When to Use PPP Corrections

PPP post-processing improves absolute accuracy. When is this improvement necessary?

### Applications Requiring Absolute Accuracy

**PPP corrections are valuable when you need to:**

**Integrate survey data with other geospatial datasets:**
- Overlay survey points on satellite imagery (imagery is georeferenced in absolute coordinates)
- Compare with existing maps or aerial photography
- Combine with LiDAR or photogrammetric data from other sources
- Merge surveys from different dates or base station setups

**Example:** You survey river cross-section in November 2024. In March 2025, you survey same cross-section to assess channel change. If base station positions differ by 25 cm between surveys, you will incorrectly measure 25 cm of channel change that is actually just base position error. PPP correcting both surveys ensures change measurements are reliable.

**Provide data for engineering or modeling:**
- Hydraulic modeling requires accurate elevation data (for water surface slope calculations)
- Engineering design (bridge design, culvert sizing) needs accurate absolute elevations
- Flood hazard mapping requires accurate terrain elevations in absolute reference frame

**Meet official mapping or regulatory requirements:**
- Cadastral surveying (property boundaries)
- Official topographic mapping
- Regulatory monitoring (water levels, flood marks)
- Legal documentation requirements

**Create permanent reference markers:**
- Establish control points for future surveys
- Create local reference network accurate in national datum
- Geodetic control for multi-year monitoring programs

**Maximize accuracy of integration with OpenRiverCam outputs:**
- Stage-discharge relationships may be integrated with external water level data (gauges)
- Velocity data may be compared with hydraulic model predictions
- Bathymetry data may be used for habitat mapping or sediment transport modeling

### When Relative Accuracy is Sufficient

**PPP correction may not be necessary if:**

**Standalone analysis within single survey session:**
- All measurements relative to same base station in single day
- Analysis only compares points within this survey (e.g., cross-section shape, GCP configuration)
- No integration with external data
- Example: Camera transformation calibration only needs accurate GCP positions relative to each other

**Short-term monitoring at single site:**
- Re-establish base at same marked location for each survey visit
- Compare relative changes over time (river bed elevation change, etc.)
- Accept that absolute elevation may be uncertain by ±25 cm, but relative change measurements are accurate to ±3 cm

**Exploratory or preliminary surveys:**
- Reconnaissance surveys before detailed monitoring setup
- Rapid assessments where absolute accuracy not critical
- Low-stakes applications

**Resource constraints:**
- PPP processing requires time (file conversion, upload, processing, waiting for results, applying corrections)
- May not be worth effort for every survey
- Can be applied selectively to important surveys

**Practical approach for OpenRiverCam:**
- **Always log raw base station data** (minimal effort, preserves option to do PPP later)
- **Apply PPP correction if:** Integrating with other data, multi-year monitoring, engineering applications
- **Skip PPP if:** Standalone camera calibration for one-time discharge measurement

### Expected Accuracy Improvements

**Understanding realistic improvements helps set expectations:**

**Base station position accuracy:**

**Survey-in (no PPP):**
- 30-60 minute survey-in: ~20-30 cm horizontal, ~30-50 cm vertical
- All survey points inherit this uncertainty in absolute position

**PPP correction (2-6 hour observation):**
- Horizontal: 3-8 cm
- Vertical: 5-15 cm
- **Improvement: ~3-5× better absolute accuracy**

**PPP correction (24 hour observation):**
- Horizontal: 2-4 cm
- Vertical: 3-6 cm
- **Improvement: ~5-10× better absolute accuracy**

**Survey point accuracy (after PPP correction applied):**

**Before PPP (survey-in only):**
- Relative accuracy: 1-3 cm (between survey points)
- Absolute accuracy: ~25 cm (all points shifted by base position error)

**After PPP correction:**
- Relative accuracy: 1-3 cm (unchanged - this was already excellent)
- Absolute accuracy: 3-8 cm (improved from 25 cm)

**Overall result: Survey data accurate to 5-10 cm in absolute position** (combining RTK relative accuracy with PPP-corrected base position).

**This is adequate for:**
- Integration with most geospatial data (satellite imagery: 1-10m resolution, LiDAR: 5-20 cm typical)
- Engineering design (tolerances typically ≥10 cm)
- Hydraulic modeling (elevation accuracy requirement: 5-10 cm)
- Regulatory mapping (accuracy standards typically 10-20 cm)

**When PPP is not sufficient:**
- Survey-grade control networks (require 1-2 cm absolute accuracy)
- Deformation monitoring (millimeter-level accuracy needed)
- Highly precise engineering (machine control, precision construction)

**For these applications, use longer PPP observation periods (24-72 hours) or traditional geodetic surveying methods (static GPS with multiple reference stations).**

---

## PPP Processing Workflow

This section describes the complete workflow for PPP correction, following SURVEY_PROCESS.md procedure.

### Step 1: Field Data Collection

**During survey, ensure base station logs raw data:**

**Configure base station for raw data logging (before survey begins):**
- Connect base station to computer running u-center (or equivalent software)
- Enable raw observation messages:
  - UBX-RXM-RAWX (raw measurements)
  - UBX-RXM-SFRBX (satellite broadcast ephemeris)
  - UBX-NAV-PVT (position/velocity/time - optional but helpful)
- Start database logging in u-center (File → Database Logging → Start)
- Set filename: Descriptive name with date, e.g., `base_20241114_river_survey.ubx`

**Monitor logging during survey:**
- Verify logging active (check file size increasing)
- Note start time (when logging began)
- Note end time (when logging stopped)
- Typical session: Start logging when base station survey-in begins, stop logging when packing up at end of day

**Record antenna information:**
- Antenna type: Make/model of base station antenna
- Antenna height: Measure from ground to Antenna Reference Point (ARP) - three measurements, average to 0.5 cm
- Example: "Antenna: u-blox ANN-MB-00, Height: 1.687m to ARP"

**At end of survey:**
- Stop logging in u-center
- Close UBX file
- Copy file to multiple locations (laptop, external drive, cloud storage)
- Verify file size reasonable (50-200 MB for 6-12 hours typical)

**Critical: Do not delete UBX file from base station until verified backups exist.** This data is irreplaceable.

### Step 2: Convert UBX to RINEX

**Using RTKLIB CONVBIN (recommended):**

See "Converting UBX to RINEX" section earlier for detailed instructions.

**Quick summary:**
```
convbin -od -os -oi -ot -f 2 base_20241114_river_survey.ubx
```

**Output files:**
- `base_20241114_river_survey.obs` (observation file for PPP)
- `base_20241114_river_survey.nav` (navigation file)

**Verify RINEX files:**
- Open .obs file in text editor
- Check header contains antenna height (matches your field measurement)
- Check observations start/end times match your survey session
- File size should be similar to UBX file size (ASCII RINEX is larger per byte but contains same data)

### Step 3: Select PPP Service and Submit

**Recommended PPP service for Asia-Pacific region (from SURVEY_PROCESS.md):**

**AUSPOS (Australia Geoscience):**
- URL: https://www.ga.gov.au/auspos
- Free service, available worldwide (not just Australia)
- Uses Asia-Pacific Reference Frame (APREF) tracking network
- Good accuracy for Indonesia and surrounding regions
- Processing time: Typically 1-24 hours depending on queue and precise product availability

**Alternative PPP services:**
- GAPS (Global Positioning System and GIS): https://gaps.gge.unb.ca (University of New Brunswick, Canada)
- MagicPPP: http://magicgnss.gmv.com/ppp (GMV, Spain)
- CSRS-PPP: https://webapp.geod.nrcan.gc.ca/geod/tools-outils/ppp.php (Natural Resources Canada)
- Trimble CenterPoint RTX: Commercial service (subscription required)

**All provide similar accuracy** (2-10 cm depending on observation duration). Choose based on region, processing speed, or preference.

**AUSPOS submission procedure:**

**1. Navigate to AUSPOS website**
- https://www.ga.gov.au/auspos
- Click "Process RINEX file" or similar

**2. Upload observation file**
- Select your .obs or .YYo RINEX observation file
- File size limit: Typically 100 MB (compress if larger)
- Navigation file (.nav) usually not required (AUSPOS downloads ephemeris automatically)

**3. Enter submission details**

**Antenna type:**
- Select from dropdown list of standard IGS antennas
- **For u-blox/ArduSimple antennas (not in IGS database):**
  - Choose closest generic match:
    - TRM29659.00 (Trimble multiband - good generic choice)
    - SEPCHOKE_MC (Septentrio multiband choke ring)
    - LEIAT504GG (Leica multiband)
  - Or select "Unknown antenna type" (may reduce accuracy by 1-3 cm)

**Antenna height:**
- Enter height measured in field: Distance from ground to Antenna Reference Point (ARP)
- Example: `1.687` meters
- **Critical:** This must match your field measurement exactly - 1 cm error here = 1 cm vertical error in results

**Processing options:**
- Processing mode: Static (for stationary base station)
- Solution type: Ambiguity-fixed (for highest accuracy)
- Observation duration: Automatic (uses full file duration)

**Email address:**
- Enter your email - results will be sent when processing completes
- Check spam folder if results not received within expected timeframe

**4. Submit processing request**
- Click "Submit" or "Process"
- Note submission ID or confirmation number
- Expect results in 1-24 hours (faster for recent observations, slower for older data requiring final precise products)

### Step 4: Receive and Interpret Results

**AUSPOS sends email with results when processing completes.**

**Results include:**

**Summary file (text or PDF):**
- Final coordinates in multiple formats (ITRF, WGS84, GDA2020)
- Estimated accuracy (standard deviations for East, North, Up)
- Processing details (observation duration, number of satellites, ambiguity resolution status)

**Coordinates typically provided:**

**Cartesian (ITRF):**
- X, Y, Z in meters (Earth-centered, Earth-fixed)
- Example: X = -1234567.123 m, Y = 5678901.234 m, Z = -2345678.345 m

**Geographic (WGS84):**
- Latitude, Longitude (degrees, minutes, seconds or decimal degrees)
- Ellipsoid height (meters above WGS84 ellipsoid)
- Example: Lat = -6.123456°, Lon = 106.789012°, h = 123.456 m

**Example AUSPOS results excerpt:**
```
FINAL COORDINATES (ITRF2020, Epoch 2024.870)
Latitude:    -6° 07' 24.4321"  (-6.123453° decimal)
Longitude:  106° 47' 20.4567"  (106.789012° decimal)
Ellipsoid Height: 123.456 m

Estimated Accuracy (95% confidence):
Latitude:  ±0.027 m
Longitude: ±0.021 m
Height:    ±0.043 m

Processing Summary:
Observation duration: 7.5 hours
Satellites used: GPS, GLONASS, Galileo
Ambiguities: Fixed (95% of epochs)
Reference frame: APREF stations
```

**Interpret accuracy estimates:**
- ±0.02-0.03 m horizontal: Excellent (multi-hour observation, good conditions)
- ±0.04-0.06 m vertical: Good to excellent
- ±0.05-0.10 m horizontal: Acceptable (shorter observation or challenging conditions)
- ±0.10-0.20 m: Marginal (short observation, poor conditions, or limited satellite coverage)

**If accuracy worse than expected:**
- Check observation duration (may need longer session)
- Check ambiguity resolution status (should be "fixed" for best accuracy)
- Consider reprocessing with different PPP service for comparison
- Verify antenna height was entered correctly

### Step 5: Transform Coordinates to Survey CRS

**AUSPOS provides WGS84 geographic coordinates.** Your survey data is in UTM Zone 48S (EPSG:32748). You must transform PPP coordinates to match.

**Coordinate transformation methods:**

**Option 1: Online coordinate transformation tool**

Example: Geoscience Australia Coordinate Transformation Tool
- Input: WGS84 latitude, longitude, ellipsoid height from AUSPOS
- Output CRS: EPSG:32748 (UTM Zone 48 South)
- Output: Easting, Northing, elevation in UTM

**Option 2: QGIS coordinate transformation**

- Open QGIS
- Create temporary point layer: Layer → Create Layer → New Temporary Scratch Layer
- Add point at AUSPOS latitude/longitude (input CRS: EPSG:4326 WGS84 geographic)
- Reproject layer to EPSG:32748: Right-click layer → Export → Save Features As → CRS = EPSG:32748
- Open attribute table of reprojected layer - read Easting, Northing coordinates

**Option 3: PROJ command-line tool** (for advanced users)
```
echo "106.789012 -6.123453 123.456" | cs2cs +init=epsg:4326 +to +init=epsg:32748
```

**Result: PPP base position in UTM Zone 48S:**
- E_ppp = Example: 501234.567 m
- N_ppp = Example: 9876543.210 m
- Z_ppp = Example: 123.456 m (elevation above ellipsoid)

**Note on elevation:** PPP provides ellipsoid height. Your survey uses orthometric height (elevation above mean sea level). For centimeter-level accuracy, apply geoid separation (ellipsoid height - geoid separation = orthometric height). For many applications, this correction is small (few meters) and can be ignored if consistency maintained.

### Step 6: Calculate Correction Translation

**You now have two base station positions:**

**Survey-in position (from field survey):**
- E_survey = What base station determined during 30-60 min survey-in
- N_survey = Recorded in base station configuration or field notes
- Z_survey = Example: 501234.347 m, 9876543.021 m, 123.231 m

**PPP position (from post-processing):**
- E_ppp = From coordinate transformation above
- N_ppp = Example: 501234.567 m, 9876543.210 m, 123.456 m
- Z_ppp

**Calculate translation (correction to apply to all survey points):**
- ΔE = E_ppp - E_survey = 501234.567 - 501234.347 = **+0.220 m**
- ΔN = N_ppp - N_survey = 9876543.210 - 9876543.021 = **+0.189 m**
- ΔZ = Z_ppp - Z_survey = 123.456 - 123.231 = **+0.225 m**

**Interpretation:**
- Survey-in position was 22 cm west, 19 cm south, and 22.5 cm below true position
- All rover survey points inherit this same offset (they are accurate relative to incorrect base position)
- Applying translation correction shifts all points to correct absolute position

**Record translation values carefully** - these will be applied to all survey data.

### Step 7: Apply Corrections in QGIS

**From SURVEY_PROCESS.md workflow:**

**1. Import survey data to QGIS**
- Open QGIS, create new project
- Import SW Maps Geopackage export (preserves CRS metadata)
- Verify CRS is EPSG:32748 (should be automatic)
- Verify all survey point layers loaded (Ground Control Points, Cross Sections, Water Level, etc.)

**2. Apply translation to coordinates**

**For each survey point layer:**

- Open attribute table
- Open Field Calculator (calculator icon in attribute table toolbar)
- Create new fields for corrected coordinates:

**Corrected Easting:**
```
Field name: E_corrected
Field type: Decimal (double)
Expression: "x_coord" + 0.220
```
(Replace 0.220 with your ΔE value)

**Corrected Northing:**
```
Field name: N_corrected
Field type: Decimal (double)
Expression: "y_coord" + 0.189
```
(Replace 0.189 with your ΔN value)

**Corrected Elevation:**
```
Field name: Z_corrected
Field type: Decimal (double)
Expression: "z_coord" + 0.225
```
(Replace 0.225 with your ΔZ value)

**3. Calculate ground elevations**

If survey includes pole height measurements (elevations are antenna heights, need ground elevations):

```
Field name: bed_elevation
Field type: Decimal (double)
Expression: "Z_corrected" - "pole_height"
```

**4. Update geometry to corrected coordinates**

**Option A: Update existing points**
- Use "Refactor Fields" tool or geometry generator to update X, Y coordinates
- Advanced - requires careful field mapping

**Option B: Create new corrected layer (recommended):**
- Layer → Create Layer → New Shapefile Layer or New Geopackage Layer
- Copy attributes from original layer
- Add geometries using corrected coordinates

**Option C: Use "Translate (move)" tool:**
- Vector → Geoprocessing Tools → Translate
- Offset X: 0.220 (ΔE)
- Offset Y: 0.189 (ΔN)
- Creates new layer with shifted coordinates

**5. Validate correction**

**Check point positions:**
- Overlay corrected survey points on satellite imagery
- Verify points appear in correct geographic locations
- Check coordinate ranges are reasonable for site location

**Check relative accuracy maintained:**
- Measure distances between corrected survey points
- Compare to distances between original survey points
- Should be identical (translation preserves relative positions)

**Check elevations:**
- Verify elevation values are reasonable for site (river elevations, terrain)
- Compare to expected elevations if known

**6. Save corrected data**

**Export corrected Geopackage:**
```
File name: site_name_YYYYMMDD_PPP_corrected.gpkg
CRS: EPSG:32748
Include all corrected attribute fields
```

**Create backup exports:**
- GeoJSON (with CRS metadata preserved)
- Shapefile (if needed for compatibility with other software)

**7. Export for OpenRiverCam PtBox**

**Create XYZ point cloud file:**
- Right-click corrected layer (cross-section or combined control + cross-section)
- Export → Save Features As
- Format: CSV (Comma Separated Value)
- Layer Options: GEOMETRY=AS_XYZ (exports X, Y, Z columns)
- Filename: `site_name_YYYYMMDD_survey_PPP.csv`
- Rename to `.xyz` extension if required by PtBox import

**Verify XYZ file format:**
```
501234.789,9876543.456,123.234
501235.123,9876543.567,123.187
501235.456,9876543.678,123.145
...
```
(X = Easting, Y = Northing, Z = Elevation, comma-separated, no header)

**Import to PtBox:**
- Follow PtBox point cloud import procedure
- Verify points appear in correct locations
- Use corrected coordinates for camera transformation calibration

### Workflow Summary Checklist

**Field work:**
- [ ] Configure base station for raw data logging (UBX-RXM-RAWX, UBX-RXM-SFRBX enabled)
- [ ] Start logging at beginning of survey session
- [ ] Record antenna type and measure antenna height (3 measurements, average)
- [ ] Log continuously for entire survey (6-12 hours minimum)
- [ ] Stop logging, backup UBX file to multiple locations

**Post-processing:**
- [ ] Convert UBX to RINEX using RTKLIB CONVBIN
- [ ] Verify RINEX observation file contains data (check header, observation records)
- [ ] Submit RINEX to PPP service (AUSPOS recommended)
- [ ] Enter correct antenna type and antenna height
- [ ] Wait for PPP results (1-24 hours)
- [ ] Transform PPP coordinates from WGS84 to survey CRS (UTM 48S)
- [ ] Calculate translation: ΔE, ΔN, ΔZ = PPP position - survey-in position
- [ ] Import survey data to QGIS
- [ ] Apply translation to create corrected coordinate fields
- [ ] Update geometry to corrected coordinates
- [ ] Validate results (overlay on imagery, check elevations, verify relative accuracy maintained)
- [ ] Export corrected Geopackage and XYZ point cloud
- [ ] Archive all data: original survey, PPP results, corrected outputs

**This workflow improves your survey absolute accuracy from ~25 cm to 3-8 cm** while maintaining excellent 1-3 cm relative accuracy.

---

## Accuracy Expectations and Limitations

Understanding realistic accuracy and PPP limitations helps set appropriate expectations.

### Factors Affecting PPP Accuracy

**Observation duration (most significant):**
- 1-2 hours: 10-20 cm horizontal, 20-40 cm vertical
- 2-6 hours: 3-8 cm horizontal, 5-15 cm vertical (typical OpenRiverCam)
- 6-24 hours: 2-4 cm horizontal, 3-6 cm vertical
- 24+ hours: 1-3 cm horizontal, 2-4 cm vertical (optimal)

**Satellite availability and geometry:**
- Multi-GNSS (GPS+GLONASS+Galileo): Better accuracy, faster convergence
- GPS-only: Slower convergence, slightly lower accuracy
- Good geometry (PDOP <2.0): Best accuracy
- Poor geometry (PDOP >3.0): Degraded accuracy

**Observation continuity:**
- Continuous tracking: Best accuracy
- Gaps in observations (power interruptions, obstruction periods): Degraded accuracy
- Each gap requires re-initializing ambiguity resolution

**Ionospheric activity:**
- Quiet ionosphere (solar minimum, nighttime): Better accuracy
- Active ionosphere (solar maximum, midday equatorial): Slower convergence
- Geomagnetic storms: Significantly degraded accuracy (may need 24+ hour sessions)

**Receiver quality:**
- Survey-grade multi-frequency: Best performance (ArduSimple F9P is good low-cost option)
- Single-frequency: Slower convergence, lower accuracy
- Low-quality receiver: May not achieve centimeter accuracy even with long sessions

**Precise product availability:**
- Ultra-rapid products (available 3-6 hours after observations): Slightly lower accuracy
- Rapid products (available 17-41 hours): Good accuracy
- Final products (available 12-18 days): Best accuracy
- If submitting recent data, PPP service may use ultra-rapid products (expect 5-10 cm vs 2-5 cm with final)

**Antenna type and calibration:**
- IGS-calibrated antenna: Best accuracy (antenna phase center precisely known)
- Generic/unknown antenna: Reduced accuracy by 1-3 cm (phase center approximated)
- Antenna height measurement error: 1 cm measurement error = 1 cm vertical error in results

### PPP Limitations

**PPP cannot improve relative accuracy:**
- RTK already provides 1-3 cm relative accuracy between survey points
- PPP only improves absolute position of base station
- Relative positions of rover survey points remain unchanged (defined by RTK measurements)

**PPP requires stable receiver position:**
- Base station must not move during observation session
- Any movement degrades PPP solution
- If base disturbed (tripod bumped, settled), PPP accuracy compromised

**PPP requires long observation periods:**
- Minimum 2-4 hours for useful accuracy
- Optimal 6-24 hours
- Rapid surveys (30-minute base setup) cannot be PPP corrected effectively

**PPP vertical accuracy is lower than horizontal:**
- Typical: Horizontal accuracy 1.5-2× better than vertical
- Reason: Satellite geometry (all satellites above horizon, weak vertical geometry)
- If vertical accuracy critical, use longer observation periods (12-24 hours)

**PPP accuracy depends on external data quality:**
- Precise ephemeris and clock corrections from IGS
- If IGS products delayed or degraded (rare), PPP accuracy suffers
- Generally reliable, but not controllable by user

### Comparing PPP to Other Positioning Methods

**Positioning method accuracy summary:**

**Smartphone GPS:**
- Accuracy: 5-10 meters
- Time to position: Seconds
- Equipment cost: $0 (included in phone)

**Survey-grade GPS (single receiver, no corrections):**
- Accuracy: 1-3 meters
- Time to position: Minutes (5-15 min for averaged position)
- Equipment cost: $3,000-10,000

**RTK (relative to base station):**
- Accuracy: 0.01-0.03 meters relative
- Time to position: 5-20 minutes (fix acquisition)
- Equipment cost: $1,500-5,000 (base + rover)

**RTK + PPP (absolute):**
- Accuracy: 0.03-0.08 meters absolute (0.01-0.03 relative maintained)
- Time to position: 6-12 hours observation + 1-24 hours processing
- Equipment cost: $1,500-5,000 (same as RTK, PPP processing often free)

**Static GPS post-processing (long observation):**
- Accuracy: 0.01-0.03 meters absolute
- Time to position: 4-24 hours observation + processing
- Equipment cost: $5,000-15,000 (survey-grade receiver)

**Traditional geodetic surveying (total station from control):**
- Accuracy: 0.005-0.02 meters (relative to control points)
- Time to position: Hours to days (depends on control network establishment)
- Equipment cost: $10,000-30,000 (total station + control network)

**RTK + PPP provides excellent cost-effectiveness:** Near-geodetic accuracy ($1,500-5,000 equipment) with reasonable field effort (6-12 hour observation).

### Quality Assurance for PPP Results

**How to verify PPP results are reliable:**

**Check observation duration:**
- Verify RINEX file duration matches expected (should be 6-12 hours for field survey)
- Longer = more confidence in results

**Check PPP accuracy estimates:**
- Horizontal: ±0.02-0.05 m excellent, ±0.05-0.10 m acceptable, >0.10 m marginal
- Vertical: ±0.03-0.08 m excellent, ±0.08-0.15 m acceptable, >0.15 m marginal
- If accuracy worse than expected for observation duration, investigate

**Check ambiguity resolution status:**
- Should report "ambiguities fixed" for most/all epochs
- If "float" or "poor convergence," accuracy is compromised

**Compare multiple PPP services:**
- Submit same RINEX to AUSPOS, GAPS, and CSRS-PPP
- Results should agree within 2-5 cm
- If large discrepancies (>10 cm), investigate cause (different precise products, processing options)

**Verify coordinates are reasonable:**
- Check PPP position against approximate survey-in position (should be within 20-50 cm)
- If PPP differs by meters, likely processing error (wrong antenna height, corrupted RINEX, etc.)
- Overlay PPP base position on satellite imagery - should appear at field location

**Validate with check points:**
- If you established permanent check point at start of survey
- Re-survey check point with PPP-corrected base position (future survey day)
- Check point should repeat within 3-5 cm (verifies PPP accuracy)

**Document PPP processing:**
- Keep PPP service results report (includes processing details, accuracy estimates)
- Record which PPP service used, submission date, observation duration
- Archive RINEX files, UBX files, and processing results
- Allows verification or reprocessing if questions arise later

---

## Connection to Survey Procedures

This section explained PPP post-processing workflow. Now you understand:

**When SURVEY_PROCESS.md specifies "Start RINEX logging":**
- Raw data enables PPP post-processing to improve absolute accuracy
- Logging must continue entire survey session (6-12 hours)
- UBX file will be converted to RINEX for PPP submission

**When procedure records antenna height measurement:**
- PPP requires accurate antenna height (1 cm error = 1 cm vertical position error)
- Three measurements averaged to 0.5 cm precision

**PPP workflow (Section 10 of SURVEY_PROCESS.md):**
- Convert UBX to RINEX using CONVBIN
- Submit to AUSPOS PPP service
- Transform coordinates to survey CRS (UTM 48S)
- Calculate translation (ΔE, ΔN, ΔZ)
- Apply corrections in QGIS to all survey points

**Expected results:**
- Base station position improved from ~25 cm to 3-8 cm absolute accuracy
- All survey points corrected by same translation
- Final survey accuracy: 3-8 cm absolute, 1-3 cm relative

**When PPP is valuable:**
- Integration with other geospatial data
- Multi-year monitoring programs
- Engineering applications requiring absolute accuracy
- Permanent reference marker establishment

**When PPP is optional:**
- Standalone camera calibration (relative accuracy sufficient)
- Short-term monitoring with consistent base setup
- Exploratory surveys where absolute accuracy not critical

You now understand the complete RTK + PPP workflow for achieving both excellent relative accuracy (RTK) and excellent absolute accuracy (PPP correction). Chapter 9 field procedures apply this knowledge in step-by-step operational instructions.

---

## Summary: Key Concepts

**Why log raw data:**
- Enables PPP post-processing to improve base station position
- Records carrier phase and pseudorange observations
- Combined with precise satellite products (available hours to days later) for centimeter-level absolute accuracy
- Always log base station data (minimal effort, preserves PPP option)

**RINEX format:**
- Standard format for GNSS observation data exchange
- Required by PPP processing services
- Convert from UBX using RTKLIB CONVBIN
- Contains carrier phase, pseudorange, ephemeris, metadata

**What PPP is:**
- Precise Point Positioning using single receiver + precise satellite products
- Achieves 2-10 cm absolute accuracy (vs ~25 cm survey-in)
- Post-processed (not real-time) - requires hours of observation + waiting for results
- Complements RTK (RTK for relative accuracy, PPP for absolute accuracy)

**PPP processing workflow:**
1. Log base station raw data (UBX format, 6-12 hours)
2. Convert UBX to RINEX (RTKLIB CONVBIN)
3. Submit RINEX to PPP service (AUSPOS recommended)
4. Receive PPP coordinates (WGS84 geographic)
5. Transform to survey CRS (UTM 48S)
6. Calculate translation: ΔE, ΔN, ΔZ
7. Apply corrections to all survey points in QGIS
8. Export corrected data (Geopackage, XYZ point cloud)

**Accuracy expectations:**
- 2-6 hour observation: 3-8 cm horizontal, 5-15 cm vertical
- 6-24 hour observation: 2-4 cm horizontal, 3-6 cm vertical
- Combines with RTK relative accuracy (1-3 cm) for overall 3-8 cm absolute accuracy

**When to use PPP:**
- Integration with other geospatial data (imagery, maps, LiDAR)
- Multi-year monitoring (compare surveys with different base setups)
- Engineering/modeling applications requiring absolute accuracy
- Official mapping or regulatory requirements

**PPP limitations:**
- Requires long observation periods (4-12 hours minimum)
- Cannot improve relative accuracy (RTK already excellent)
- Vertical accuracy lower than horizontal (1.5-2× worse)
- Requires stable base station (any movement degrades solution)

**Critical success factors:**
- Configure base for raw logging before survey
- Measure antenna height accurately (±0.5 cm)
- Log continuously entire session (gaps degrade accuracy)
- Back up UBX files immediately (irreplaceable data)
- Apply consistent coordinate transformations throughout workflow

**Practical impact:** RTK + PPP workflow provides survey-grade absolute accuracy (5-10 cm) at accessible cost ($1,500-5,000 equipment, free PPP processing), enabling humanitarian organizations to conduct high-accuracy surveys without expensive contractors.

You now have complete understanding of the RTK + PPP workflow for OpenRiverCam surveying. Chapter 9 provides step-by-step field procedures, and SURVEY_PROCESS.md gives detailed operational instructions for the entire workflow from field survey through PPP correction to final data delivery.

---

**End of Chapter 5: Geospatial Concepts**

This completes the technical foundation for understanding OpenRiverCam survey work. You now understand:
- Survey strategies and their tradeoffs (5.1)
- GNSS vs total station approaches (5.2)
- RTK fundamentals and how centimeter accuracy is achieved (5.3)
- Base and rover station roles and setup (5.4)
- RTK fix status and when to collect survey points (5.5)
- PPP post-processing for absolute accuracy improvement (5.6)

**Next steps:**
- **Chapter 9: Site Survey** provides field procedures that apply these concepts
- **SURVEY_PROCESS.md** gives detailed operational checklists and quality gates
- **Practice with equipment** to build confidence in RTK operation and fix recognition

The concepts in Chapter 5 may seem complex, but with field experience they become intuitive. Understanding the "why" behind survey procedures makes you a more capable and confident surveyor - able to troubleshoot problems, adapt to conditions, and ensure data quality.
