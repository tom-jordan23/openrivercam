# RIVER SURVEY SOP
**Equipment:** ArduSimple RTK + Android + GNSS Master + SW Maps  
**Target:** Centimeter relative accuracy, ~0.25m absolute via PPP  
**CRS:** UTM Zone 48 South (EPSG:32748)

## TABLE OF CONTENTS

### DAY-BEFORE SETUP
1. [Software Setup](#1-software-setup)
2. [Equipment Check](#2-equipment-check)

### FIELD DAY  
3. [Base Station Setup](#3-base-station-setup)
4. [Check Points](#4-check-points)
5. [Camera & Control Points](#5-camera--control-points)
6. [Water Level Survey](#6-water-level-survey)
7. [Point Collection](#7-point-collection)
8. [Cross-Section Survey](#8-cross-section-survey)
9. [End of Day](#9-end-of-day)

### POST-PROCESSING
10. [PPP & Data Processing](#10-ppp--data-processing)

### APPENDICES
- [A. GNSS Master Setup](#appendix-a-gnss-master-setup)
- [B. SW Maps Configuration](#appendix-b-sw-maps-configuration)  
- [C. Base Station u-center Config](#appendix-c-base-station-u-center-config)
- [D. Sample Video Collection](#appendix-d-sample-video-collection)
- [E. Troubleshooting](#appendix-e-troubleshooting)
- [F. Field Reference Card](#appendix-f-field-reference-card)

---

## SURVEY SUCCESS CRITERIA
- [ ] RTK FIX maintained throughout survey
- [ ] Base station online entire duration
- [ ] Check point drift ≤3cm H, ≤4cm V
- [ ] Min 12 satellites, PDOP ≤2.5

## QUALITY GATES (All required before saving points)
**Standard:** RTK FIX ≥10s, PDOP ≤2.5, Sats ≥12, Precision ≤2cm H/3cm V  
**Canal:** RTK FIX ≥10s, PDOP ≤3.0, Sats ≥10, Precision ≤4cm H/6cm V

---

# DAY-BEFORE SETUP

## 1) Software Setup
**Test everything at home before field day**

### Android & GNSS Master
- [ ] Install GNSS Master app → [Full setup guide](#appendix-a-gnss-master-setup)
- [ ] Enable Developer Options, Mock Location
- [ ] Test USB connection with rover
- [ ] Verify mock location works with test apps

### SW Maps Project  
- [ ] Create new project → [Full configuration guide](#appendix-b-sw-maps-configuration)
- [ ] Set CRS to EPSG:32748 (UTM 48S)
- [ ] Create survey layers with attributes
- [ ] Test GPS integration with GNSS Master

### Integration Test
- [ ] Full system test: Base → Rover → GNSS Master → SW Maps
- [ ] Verify RTK FIX status appears in SW Maps
- [ ] Test point collection with quality thresholds

## 2) Equipment Check
**Power Systems:**
- [ ] Base station: Full charge + backup battery
- [ ] Rover: Full charge  
- [ ] Android: 100% + power bank
- [ ] All USB cables tested

**Physical Equipment:**
- [ ] Survey poles (primary + backup), bipod
- [ ] Steel tape measure, markers
- [ ] Base tripod, antenna cables
- [ ] Waterproof notebook, pencils

---

# FIELD DAY

## 3) Base Station Setup
**Site Selection:**
- [ ] Open sky >15°, >10m from metal/vehicles
- [ ] Stable ground, accessible for monitoring
- [ ] For canals: High ground >20m from water

**Setup Process:**
- [ ] Connect antenna BEFORE powering base
- [ ] Level tripod, mark exact point
- [ ] Measure antenna height to ARP (3 measurements)
- [ ] u-center configuration → [Detailed setup](#appendix-c-base-station-u-center-config)

**Survey-In:**
- [ ] 30-60 minute survey-in for 0.25m accuracy
- [ ] Monitor: PDOP ≤1.5, Satellites ≥15
- [ ] Record final coordinates in UTM 48S
- [ ] Start RINEX logging (6-12 hours)

## 4) Check Points
**Establish CP_START:**
- [ ] 20-50m from base, stable high ground  
- [ ] RTK FIX for 30 seconds
- [ ] 3 independent 60s measurements
- [ ] Agreement within 1cm H, 2cm V
- [ ] Mark permanently, photograph

**Monitor Throughout Day:**
- [ ] CP_NOON: Re-measure after 4-6 hours
- [ ] CP_END: Final check before packing
- [ ] Total drift must be ≤3cm H, ≤4cm V

## 5) Camera & Control Points
**Camera Position:**
- [ ] 5-10m height, 15-45° viewing angle
- [ ] Survey camera position with rover
- [ ] Record height, direction, tilt angle

**Control Points:**
- [ ] Place 6+ visible targets in camera FOV
- [ ] Take sample video → [Detailed procedure](#appendix-d-sample-video-collection)
- [ ] Survey each control point after video
- [ ] Use Ground Control Points layer

## 6) Water Level Survey
**Setup:**
- [ ] Identify stable water level measurement point
- [ ] Use staff gauge or direct measurement method
- [ ] Record water surface conditions (calm/turbulent)

**Measurement:**
- [ ] Survey water surface elevation with rover pole
- [ ] Touch pole to water surface, maintain RTK FIX
- [ ] Record in Water Level layer with flow conditions
- [ ] Take multiple measurements if water is moving
- [ ] Document measurement method and accuracy

## 7) Point Collection
**Quality Requirements:**
- [ ] All quality gates met (see top of document)
- [ ] Averaging times: 60s standard, 120s canal
- [ ] Pole bubble centered, measure height each shot

**Standard Protocol:**
- [ ] Verify RTK FIX ≥10 seconds
- [ ] Check precision estimates in SW Maps
- [ ] Record all required attributes
- [ ] If conditions fail: wait 2min → move 2-3m → retry

## 8) Cross-Section Survey
**Setup:**
- [ ] Establish LB/RB reference points on stable ground
- [ ] Plan station spacing (1-2m typical)
- [ ] Document section ID, flow conditions

**Collection:**
- [ ] Walk LB → RB systematically
- [ ] Each station: verify quality gates, 60-120s averaging
- [ ] Record station number, point role, water depth
- [ ] Measure pole height tip-to-ARP each shot

## 9) End of Day
**Final Checks:**
- [ ] Re-measure CP_END, calculate total drift
- [ ] Stop RINEX logging, record end time
- [ ] Export SW Maps data (CSV + native format)
- [ ] Multiple backups on different devices
- [ ] Document any deviations from protocol

---

# POST-PROCESSING

## 10) PPP & Data Processing

### Step 1: Extract Base Station RINEX
**U-Center RINEX Export:**
- [ ] Open base station UBX log file in u-center
- [ ] File → RINEX Converter → Select UBX file
- [ ] Output: RINEX 2.11 or 3.03 format
- [ ] Ensure observation interval matches logging (1s typical)
- [ ] Export to .obs file for PPP processing

### Step 2: PPP Processing  
**Submit for Processing:**
- [ ] Upload RINEX file to an online PPP service like AUSPOS or CSRS-PPP service
- [ ] Processing options: Static, 24-hour session preferred
- [ ] Download results: coordinates in WGS84 geographic
- [ ] Convert to UTM Zone 48S (EPSG:32748) using coordinate conversion tool

**Record PPP Results:**
- [ ] PPP coordinates: E_ppp, N_ppp, Z_ppp (UTM 48S)
- [ ] Survey-in coordinates: E_survey, N_survey, Z_survey
- [ ] Calculate translation: ΔE = E_ppp - E_survey, ΔN = N_ppp - N_survey, ΔZ = Z_ppp - Z_survey

### Step 3: Apply Corrections in QGIS
**Data Import:**
- [ ] Open QGIS, create new project
- [ ] Import SW Maps Geopackage export (preserves CRS metadata)
- [ ] Verify CRS is EPSG:32748 (UTM Zone 48S) - should be automatic
- [ ] Verify all survey points imported correctly with proper geometry

**Apply PPP Translation:**
- [ ] Open Field Calculator for each layer in Geopackage
- [ ] Create new fields: `E_corrected = "x_coord" + ΔE`, `N_corrected = "y_coord" + ΔN`, `Z_corrected = "z_coord" + ΔZ`
- [ ] Calculate bed elevations: `bed_elevation = Z_corrected - pole_height`
- [ ] Update geometry: Use "Update Geometry" tool with corrected coordinates
- [ ] Save changes to Geopackage (preserves all metadata)
- [ ] Validate: Check point repeatability should remain ≤3cm after correction

### Step 4: Export for PtBox
**Create XYZ Point Cloud:**
- [ ] Select cross-section and control point layers from corrected Geopackage
- [ ] Right-click layer → Export → Save Features As
- [ ] Format: "Comma Separated Value [CSV]"
- [ ] Geometry: AS_XYZ (exports X,Y,Z coordinates)
- [ ] Layer options: GEOMETRY=AS_XYZ, CREATE_CSVT=NO
- [ ] Save as `site_name_YYYYMMDD_survey.csv` (will contain X,Y,Z columns)
- [ ] Rename to `.xyz` extension if required by PtBox

**Archive and Quality Control:**
- [ ] Save corrected Geopackage as `site_name_YYYYMMDD_corrected.gpkg`
- [ ] Export backup as GeoJSON with CRS metadata
- [ ] Verify coordinate ranges are reasonable for site location
- [ ] Check elevation values match expected riverbed depths
- [ ] Confirm XYZ file format compatible with PtBox import requirements
- [ ] Test import with small subset if possible

---

# APPENDICES

## Appendix A: GNSS Master Setup

### Android Preparation
1. **Developer Options:**
   - Settings → About Phone → Tap Build Number 7x
   - Settings → Developer Options → Enable USB Debugging
   - Select Mock Location App → GNSS Master

2. **Permissions:**
   - Settings → Apps → GNSS Master → Permissions
   - Location: Allow all the time
   - Storage, Phone: Allow
   - Battery optimization: Don't optimize

### GNSS Master Configuration
1. **Install:** Download from Google Play Store
2. **Connection:** Menu → Receiver → USB
3. **Mock Location:** Menu → Mock Location → Enable
4. **Test:** Verify position appears in Google Maps

### USB Connection Setup
1. Connect USB OTG cable to Android
2. Connect to rover F9P USB port  
3. Power rover, wait 30 seconds
4. GNSS Master should auto-detect device
5. Verify satellite tracking and RTK status

---

## Appendix B: SW Maps Configuration

### Project Creation
1. **New Project:** `Canal_Survey_YYYY_MM_DD_Location`
2. **Coordinate System:**
   - Search: 32748
   - Select: WGS 84 / UTM zone 48S
   - VERIFY: EPSG:32748, units = metre

### GPS Settings  
- GPS Source: Device internal GPS
- Averaging Method: By Time
- Default times: 60s standard, 120s canal
- Precision thresholds: H=2cm/V=3cm (std), H=4cm/V=6cm (canal)

### Survey Layers
Create these feature layers in your SW Maps project (all should be POINT geometry):

 - **Camera FOV**
 - **Camera Location**
 - **Check Point Location**
 - **Ground Control Points**
 - **Discharge Cross Section**
 - **Level Cross Section**
 - **Water Level**


---

## Appendix C: Base Station u-center Config

### Connection Setup
1. Launch u-center, File → New
2. Receiver → Connection → Select COM port
3. Baud: 38400 or 115200, Connect

### Survey-In Configuration (TMODE3)
1. View → Configuration → UBX → CFG → TMODE3
2. Mode: Survey-in
3. Minimum time: 1800-3600 seconds (30-60 min)
4. Required accuracy: 0.25 meters
5. Send Configuration

### RTCM3 Output (if not using a pre-configured base and rover)
1. UBX → CFG → PRT → UART2 → Protocol out: RTCM3
2. UBX → CFG → MSG → Enable RTCM messages:
   - 1005 (Station ARP): Rate 10
   - 1077 (GPS MSM7): Rate 1
   - 1087 (GLONASS MSM7): Rate 1
   - 1097 (Galileo MSM7): Rate 1

### Raw Data Logging
1. UBX → CFG → MSG → Enable on USB:
   - UBX-RXM-RAWX: Rate 1
   - UBX-RXM-SFRBX: Rate 1
   - UBX-NAV-PVT: Rate 1
2. File → Database Logging → Start (UBX format)

---

## Appendix D: Sample Video Collection

### Connect to PtBox
 - Put the PtBox in Maintenance Mode using the FTP service
 - Wait for the PtBox to come online again, and log in
 - Select "Aim the camera in the field"
 - Take a 5 second video and note the video name and timestamp
 - Ensure that all control points are visible in the video. Adjust if needed and take a new video.
 - Also take a photo, and use the photo to number the control points so that you have a reference to use when entering the control points into the PtBox software later.
 - **NOTE:** Do not try to start the cameras in this view. This PtBox has a bad camera, and attempting to start the bad camera will cause the PtBox to lock up.

---

## Appendix E: Troubleshooting

### No RTK FIX
- Check base survey-in completed
- Verify radio link, RTCM messages
- Wait longer (up to 20 minutes)
- Move to better sky view

### Poor Precision  
- Check satellite count, PDOP
- Move away from reflective surfaces
- Use bipod for stability
- Extend averaging time

### USB Connection Issues
- Check USB OTG cable
- Power cycle rover and Android
- Verify USB debugging enabled
- Try different USB port

### Base Station Problems
- Check power, antenna connections
- Verify survey-in status in u-center
- Monitor RTCM output
- Restart if necessary

---

## Appendix F: Field Reference Card

```
📋 QUICK REFERENCE
Date: ________ Crew: ________ Weather: ________

🔋 EQUIPMENT STATUS (Check every 2 hours)
Base: [ ] Power [ ] Survey-In [ ] Radio TX [ ] Logging
Rover: [ ] Power [ ] RTK FIX [ ] Battery >30%

📡 QUALITY GATES (ALL required)
[ ] RTK FIX ≥10s [ ] PDOP ≤2.5 [ ] Sats ≥12 
[ ] Precision ≤2cm H/3cm V [ ] Pole centered

📍 CHECK POINT LOG
CP_START: E=_______ N=_______ Z=_______ (±__cm)
CP_NOON:  E=_______ N=_______ Z=_______ (±__cm)
CP_END:   E=_______ N=_______ Z=_______ (±__cm)
Drift: ΔE=__cm ΔN=__cm ΔZ=__cm [ ] ≤3cm OK

📊 BASE STATION
Setup: ___:___ Survey-in: ___:___ Logging: ___:___
Antenna Height: ____m (3 measurements: __, __, __)
Coordinates: E=_______ N=_______ Z=_______

⚠️ STOP IF:
[ ] RTK not FIX [ ] PDOP >2.5 [ ] Check drift >3cm
[ ] Base offline [ ] Equipment problems

Emergency: Supervisor _______ Technical _______
```