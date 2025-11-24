# 9.1 Survey Concepts Overview

This section bridges the conceptual understanding presented in Chapter 5 with the practical field procedures required for executing site surveys. Chapter 5 provided the theoretical foundations of RTK surveying, establishing the rationale for measurement approaches. This chapter transitions to the practical implementation of those concepts in field operations.

Before deploying equipment to field sites, it is essential to review the key concepts that will guide survey work. This section recapitulates the critical principles from Chapter 5 and explains how they translate into specific field procedures. Understanding the relationships between coordinate systems, reference frames, accuracy requirements, and quality standards enables field personnel to make informed decisions during survey execution (Takasu & Yasuda, 2009).

Field personnel completing this section will understand how coordinate systems determine spatial data representation, why UTM zone selection affects measurement accuracy for specific sites, the critical distinction between local and global reference frames, what RTK fix accuracy requirements mean for practical field operations, how the PPP workflow improves survey results through post-processing, the quality standards that ensure reliable measurements, and how theoretical concepts from Chapter 5 connect to practical procedures in Chapter 9.

---

## Coordinate Systems Recap

### Why Coordinate Systems Matter

Spatial data requires numerical representation through coordinate systems that provide the framework for describing positions on Earth's surface (Snyder, 1987). Every surveyed point requires coordinates that numerically describe its spatial location. Without a consistent coordinate system, survey points would consist of meaningless numbers lacking relationships to each other or to real-world positions.

As detailed in Section 5.7, coordinate systems establish the mathematical framework for position description. For OpenRiverCam applications, the Universal Transverse Mercator (UTM) coordinate system is typically employed. UTM divides the world into zones and provides coordinates in meters East (Easting) and meters North (Northing) from zone-specific origins (Hofmann-Wellenhof et al., 2007).

UTM is preferred for river monitoring applications for several reasons. First, UTM coordinates are expressed in meters, providing intuitive units for distance calculations. Second, UTM projections minimize distortion within each zone, ensuring accurate local measurements. Third, UTM coordinates are compatible with most GIS software and mapping tools, facilitating data integration. Fourth, UTM systems are widely adopted in humanitarian and engineering contexts, promoting interoperability.

The practical implications of coordinate system selection require careful consideration. When field personnel survey a ground control point and record its position as (E=685432.15, N=9456782.33, Z=142.45), those numerical values possess meaning only within a specific coordinate system. The same physical location might be represented as (685432, 9456782) in UTM Zone 48S or as (42.5°N, 123.4°E) in geographic coordinates. These represent different numerical descriptions of identical positions. Field personnel must ensure all measurements use the same coordinate system throughout survey operations to maintain data consistency and accuracy.

### UTM Zone Selection for Your Site

**The UTM system divides Earth into 60 zones:**
- Each zone spans 6 degrees of longitude
- Zones are numbered 1-60 from west to east
- Each zone has a North and South variant (Northern/Southern hemisphere)

**Example: Indonesia site**
From SURVEY_PROCESS.md, the example uses UTM Zone 48 South (EPSG:32748):
- Zone 48: Covers 102°E to 108°E longitude
- South: Southern hemisphere
- EPSG:32748: The standard code identifying this specific coordinate reference system

**How to determine your site's UTM zone:**

1. **Find your site's longitude** (from Google Maps, GPS, or existing data)
2. **Calculate zone number:** Zone = floor((longitude + 180) / 6) + 1
3. **Determine North or South** (based on latitude)

**Examples:**
- Site at 104.5°E, 5.2°S → Zone 48 South (EPSG:32748)
- Site at 97.3°E, 18.4°N → Zone 47 North (EPSG:32647)
- Site at 38.7°E, -3.1°S → Zone 37 South (EPSG:32737)

**The critical rule: Use the correct zone for your site.**

If your site is near a zone boundary (within ~2 km of the edge), you technically could use either adjacent zone. In practice:
- Choose the zone that centers your site (minimizes distortion)
- Be consistent - never mix zones in one project
- Document your choice clearly in all data files

**Zone errors cause problems:**
Using the wrong UTM zone can introduce errors of hundreds of meters or more. If your survey appears to place the river in the wrong location on satellite imagery, check the UTM zone first.

### The EPSG Code

EPSG codes are standardized identifiers for coordinate reference systems:
- EPSG:32648 = WGS 84 / UTM Zone 48 North
- EPSG:32748 = WGS 84 / UTM Zone 48 South
- WGS 84 = The datum (reference ellipsoid model of Earth's shape)

**Always specify the complete EPSG code in your survey configuration.** This ensures software interprets coordinates correctly.

**From SURVEY_PROCESS.md:**
> Set CRS to EPSG:32748 (UTM 48S)

This configuration step in SW Maps ensures all collected points use the correct coordinate system.

---

## Local vs Global Frame Decision

This is one of the most important conceptual decisions for your survey approach.

### Understanding the Two Reference Frames

**Local reference frame:**
- Base station establishes its own position through survey-in (30-60 minutes)
- Base station position has ~25 cm absolute accuracy
- All rover measurements are relative to base station with 1-3 cm relative accuracy
- Points are very accurate relative to each other, moderately accurate in global coordinates

**Global reference frame:**
- Base station position is corrected using PPP (Precise Point Positioning) post-processing
- Base station position improved to 2-10 cm absolute accuracy
- All rover measurements shifted by the PPP correction
- Points achieve high accuracy both relative to each other and in global coordinates

### When Local Frame is Sufficient

**Local frame works well when:**
- OpenRiverCam transformation is your primary use for survey data
- You do not need to integrate with other geospatial data
- You do not need to compare surveys across time (same base station location each time)
- Rapid results are more important than absolute positional accuracy

**What you achieve with local frame:**
- Ground control points accurate to 1-3 cm relative to each other (excellent for transformation)
- Camera transformation works perfectly (transformation only needs relative accuracy)
- Velocity measurements fully accurate
- Same-day results (no waiting for PPP processing)

**Example scenario:**
Single OpenRiverCam installation for flood early warning. The system measures discharge, and warnings are based on discharge thresholds. The absolute geographic position of measurements does not matter - only the accuracy of the velocity and cross-section data matters. Local frame is sufficient.

### When Global Frame is Necessary

**Global frame required when:**
- Integrating OpenRiverCam data with satellite imagery or base maps
- Comparing measurements from multiple surveys with different base station positions
- Coordinating with other monitoring sites or stations
- Engineering design or hydrologic modeling requiring accurate absolute positions
- Future verification or re-survey needs (return to exact locations years later)

**What you achieve with global frame:**
- All benefits of local frame (1-3 cm relative accuracy)
- PLUS: 2-10 cm absolute positional accuracy
- Data integrates seamlessly with other geospatial systems
- Permanent reference frame for long-term monitoring

**Example scenario:**
Regional river monitoring network with multiple OpenRiverCam sites, integrating with satellite-based flood mapping and hydrologic models. Absolute positions must be accurate for all sites to work together in coordinated analysis. Global frame (PPP correction) is necessary.

### The Practical Recommendation

**For most OpenRiverCam deployments:**
1. **Conduct field survey in local frame** (base station survey-in)
2. **Collect all data on survey day** (GCPs, cross-sections, water level)
3. **Log RINEX data from base station** (for later PPP processing)
4. **Process with PPP post-survey** (improve absolute accuracy)
5. **Apply PPP corrections in office** (shift all coordinates to global frame)

This workflow provides:
- Efficient field work (no waiting for PPP during survey)
- Excellent relative accuracy for transformation (1-3 cm)
- Improved absolute accuracy for integration (2-10 cm)
- Flexibility to use local frame immediately or global frame after processing

**From SURVEY_PROCESS.md, Section 3:**
> Survey-In: 30-60 minute survey-in for 0.25m accuracy
> Record final coordinates in UTM 48S
> Start RINEX logging (6-12 hours)

This procedure establishes local frame immediately while capturing data for global frame correction.

---

## RTK Fix Accuracy Requirements

Section 5.3 explained RTK fix status in detail. Here is the practical recap for field work.

### The Three Solution States

**Single/Autonomous:**
- No corrections from base station
- Accuracy: 2-10 meters
- Status: UNUSABLE - Do not collect points
- What to do: Wait for base station connection

**Float:**
- Receiving corrections but ambiguities not resolved
- Accuracy: 10-100 cm
- Status: NOT ADEQUATE - Do not collect points
- What to do: Wait for fix, ensure good satellite conditions

**Fix:**
- Corrections received and ambiguities resolved
- Accuracy: 1-3 cm horizontal, 2-4 cm vertical
- Status: READY TO SURVEY - Collect points
- What to do: Proceed with measurements

**The non-negotiable rule: Only collect survey points with RTK FIX status.**

### Quality Gates from SURVEY_PROCESS.md

**Standard measurement requirements:**
```
RTK FIX ≥ 10 seconds
PDOP ≤ 2.5
Satellites ≥ 12
Precision ≤ 2cm H / 3cm V
Averaging time: 60 seconds
```

**Canal/challenging conditions (relaxed standards):**
```
RTK FIX ≥ 10 seconds
PDOP ≤ 3.0
Satellites ≥ 10
Precision ≤ 4cm H / 6cm V
Averaging time: 120 seconds
```

**What each requirement ensures:**

**RTK FIX ≥ 10 seconds:**
- Confirms ambiguities are truly resolved (not momentary false fix)
- Ensures solution stability
- Reduces risk of saving Float solution by mistake

**PDOP ≤ 2.5 (standard) or ≤ 3.0 (canal):**
- Ensures adequate satellite geometry (satellites well-distributed across sky)
- Lower PDOP = better geometry = more reliable fix
- PDOP > 3.0 indicates poor geometry (satellites bunched, fix may be weak)

**Satellites ≥ 12 (standard) or ≥ 10 (canal):**
- More satellites = better ambiguity resolution
- More redundancy for reliability
- Fewer satellites = longer fix time, less reliable solution

**Precision ≤ 2cm H / 3cm V (standard) or ≤ 4cm H / 6cm V (canal):**
- Software's estimate of current measurement accuracy
- Based on signal quality, satellite geometry, fix status
- Confirms measurement meets requirements

**Averaging time: 60s (standard) or 120s (canal):**
- Longer averaging reduces random noise
- Provides more stable position estimate
- Extended for challenging conditions (tree cover, multipath, poor geometry)

### Achieving Fix in the Field

**Typical timeline:**
- 0:00 - Power on rover, acquiring satellites (Single solution)
- 0:30 - Receiving base corrections (Float solution)
- 1:00-5:00 - Resolving ambiguities (Float solution, attempting fix)
- 5:00+ - Ambiguities resolved (FIX - ready to survey!)

**Be patient during initialization.** 5-20 minutes for first fix is normal.

**If stuck in Float for >20 minutes:**
1. Check satellite count and PDOP (wait if satellites < 10 or PDOP > 3.5)
2. Check age of corrections (should be < 3 seconds; if not, check base station)
3. Move to location with better sky view (away from trees, buildings)
4. Move away from reflective surfaces (metal, water edge) by 5-10 meters
5. Wait for satellite geometry to improve (satellites moving, geometry changes)

**Once fix is achieved, maintain it:**
- Keep rover in open sky view
- Avoid passing under trees or near buildings
- Keep rover antenna level and stable during measurements
- Monitor status display continuously

---

## PPP Workflow Overview

Precise Point Positioning (PPP) improves base station absolute accuracy from ~25 cm to 2-10 cm.

### What PPP Does

**The principle:**
PPP services use global networks of reference stations with precisely known positions. They compare your RINEX observation data against precise satellite orbit and clock data, calculating corrections that improve your base station position.

**Think of it like this:**
- Your base station survey-in averages GPS errors for 30-60 minutes (achieves ~25 cm)
- PPP services average GPS errors globally over many hours using many stations (achieve ~2 cm)
- PPP applies those globally-averaged corrections to your specific observations
- Result: Your base station position improved to 2-10 cm accuracy

### PPP Processing Steps

**From SURVEY_PROCESS.md, Section 10:**

**Step 1: Convert UBX to RINEX**
```bash
convbin -od -os -oi -ot -f 1 your_file.ubx
```
This converts the base station's raw binary log file to RINEX format (standard observation format for PPP processing).

**Step 2: Submit to PPP Service**
- **AUSPOS (recommended for Asia-Pacific):** https://www.ga.gov.au/auspos
- Upload RINEX observation file (.obs) and navigation file (.nav)
- Select antenna type (or "Unknown" if not listed)
- Enter antenna height measured in field
- Processing takes 30 minutes to several hours

**Step 3: Receive Results**
- PPP service emails results with corrected base station coordinates
- Coordinates typically provided in WGS84 geographic (latitude, longitude, elevation)
- Convert to UTM using coordinate conversion tool if needed

**Step 4: Calculate Translation Vector**
```
ΔE = E_ppp - E_survey
ΔN = N_ppp - N_survey
ΔZ = Z_ppp - Z_survey
```
This vector describes how much to shift all your survey points.

**Step 5: Apply Corrections in QGIS**
- Import SW Maps Geopackage export
- Use Field Calculator to add ΔE, ΔN, ΔZ to all point coordinates
- Update geometry with corrected coordinates
- Export for use in PtBox or other systems

### When to Perform PPP

**Option 1: Before field configuration (recommended for permanent installations)**
- Process PPP immediately after survey
- Apply corrections to coordinates before entering into PtBox
- Configuration uses globally-accurate positions from the start

**Option 2: After initial deployment (acceptable for rapid deployment)**
- Use local frame coordinates for initial PtBox configuration
- Collect RINEX data for later PPP processing
- Apply PPP corrections if/when global frame needed for integration

**Option 3: Skip PPP entirely (acceptable if local frame sufficient)**
- If you never need global frame accuracy, PPP is optional
- Transformation quality depends only on relative accuracy (1-3 cm, achieved without PPP)
- Simplifies workflow for simple deployments

### PPP Accuracy Expectations

**Session length affects results:**
- 2-hour session: 5-10 cm accuracy (minimum useful)
- 6-hour session: 3-5 cm accuracy (good)
- 24-hour session: 2-3 cm accuracy (excellent)

**From SURVEY_PROCESS.md:**
> Start RINEX logging (6-12 hours)

This duration provides 3-5 cm PPP accuracy, excellent for most applications.

**The practical workflow balances:**
- Field efficiency (collect data, leave base station logging, leave site)
- Processing quality (longer logging = better PPP accuracy)
- Return schedule (need to return to collect equipment and stop logging)

6-hour minimum recommended, 12-hour or overnight logging ideal if site security allows equipment to remain unattended.

---

## Quality Standards

Quality standards ensure your survey data meets OpenRiverCam requirements. These standards connect directly to the accuracy needs explained in Section 5.1.

### Survey Success Criteria

**From SURVEY_PROCESS.md:**
```
☐ RTK FIX maintained throughout survey
☐ Base station online entire duration
☐ Check point drift ≤ 3cm H, ≤ 4cm V
☐ Min 12 satellites, PDOP ≤ 2.5
```

These criteria define a successful survey session.

### Check Point Quality Control

**The principle:**
Establish check points at the beginning of the survey and re-measure them throughout the day. If check point positions remain consistent (within 3-4 cm), your RTK system is working correctly and maintaining accuracy.

**From SURVEY_PROCESS.md, Section 4:**
```
Establish CP_START: 20-50m from base, stable high ground
- RTK FIX for 30 seconds
- 3 independent 60s measurements
- Agreement within 1cm H, 2cm V
- Mark permanently, photograph

Monitor Throughout Day:
- CP_NOON: Re-measure after 4-6 hours
- CP_END: Final check before packing
- Total drift must be ≤ 3cm H, ≤ 4cm V
```

**What this verifies:**
- Base station has not moved or shifted
- RTK system maintains consistent accuracy over time
- No equipment malfunction or configuration drift
- Atmospheric conditions have not caused unusual errors

**If check points fail (drift > 3-4 cm):**
- Something is wrong - do not trust survey data
- Possible causes: base station moved, equipment malfunction, extreme atmospheric disturbance
- Action: Investigate, troubleshoot, potentially re-survey

**Check points are your quality insurance.** They catch problems you might not notice during real-time measurements.

### Measurement Quality Thresholds

**For each surveyed point, verify:**
- Solution type = FIX (not Float or Single)
- Fix duration ≥ 10 seconds (stability)
- Satellites ≥ 12 (adequate signal)
- PDOP ≤ 2.5 (good geometry)
- Precision estimates ≤ 2cm H / 3cm V (software confirms quality)
- Age of corrections < 3 seconds (base station link working)

**Only save points that meet all thresholds.**

**If conditions fail:**
- Wait 2 minutes for improvement
- If still failing, move 2-3 meters to different location
- If persistently failing, wait 10-20 minutes for satellite geometry to change
- Do not compromise standards to "get the job done faster"

**Poor data is worse than no data** - it gives false confidence and wastes processing effort later.

### Reprojection Error Validation

After establishing the transformation in PtBox configuration, the software calculates reprojection error for each GCP:
- Transform GCP image coordinates to real-world coordinates using calculated transformation
- Compare transformed position to surveyed position
- Report error for each GCP

**Acceptable reprojection errors:**
- Individual GCPs: ≤ 5 cm (excellent), ≤ 10 cm (acceptable)
- RMS (overall): ≤ 5 cm (excellent), ≤ 8 cm (acceptable)

**Large reprojection errors indicate:**
- Survey accuracy problems (GCPs not surveyed with adequate accuracy)
- GCP identification errors (wrong pixel locations clicked in image)
- GCP movement (markers moved between survey and configuration)
- Water level mismatch (surveyed at different water level than image shows)

**Action if reprojection errors are large:**
- Verify survey accuracy (RTK fix logs, check point drift)
- Re-identify GCPs carefully in image (zoom in, precise clicking)
- Confirm GCPs have not moved
- Check water level consistency

---

## Recap: Chapter 5 Concepts in Practice

Let's connect the conceptual foundations from Chapter 5 to the practical procedures in Chapter 9.

### From Section 5.1 (Survey Strategies Overview)

**Concept:** Centimeter-level accuracy is essential for OpenRiverCam transformation quality.

**Practice:** All survey procedures target 1-3 cm relative accuracy through RTK fix requirements, quality gates, and check point validation.

### From Section 5.2 (Differential GNSS vs Total Station)

**Concept:** RTK GNSS works across obstacles and does not require line-of-sight, making it ideal for river monitoring.

**Practice:** Survey GCPs on both banks and at mid-river without needing to see across water. Base station can be on high ground while rover surveys distributed points.

### From Section 5.3 (RTK Fundamentals)

**Concept:** RTK achieves centimeter accuracy through carrier phase ambiguity resolution. Fix status indicates ambiguities are resolved. Float is not adequate.

**Practice:** Only collect points with FIX status maintained for ≥10 seconds. Wait patiently for fix during initialization (5-20 minutes normal).

### From Section 5.4 (Base and Rover Stations)

**Concept:** Base station establishes reference through survey-in. Rover calculates position relative to base with 1-3 cm accuracy.

**Practice:** Allow 30-60 minutes for base station survey-in. Position base on stable ground with open sky view. Maintain base station throughout entire survey session.

### From Section 5.5 (RTK Fix Status)

**Concept:** Quality indicators (satellites, PDOP, precision estimates) guide when to collect measurements.

**Practice:** Monitor SW Maps display continuously. Verify all quality gates are met before saving each point. Extend averaging time in challenging conditions.

### From Section 5.6 (Logging, RINEX, and PPP)

**Concept:** PPP post-processing improves base station absolute accuracy from ~25 cm to 2-10 cm using global reference networks.

**Practice:** Log RINEX data from base station (6-12 hours). Submit to AUSPOS for processing. Apply PPP corrections in QGIS to shift all coordinates to global frame.

### From Section 5.7 (Coordinate Systems)

**Concept:** UTM coordinate system provides meter-based coordinates appropriate for local surveying and GIS integration.

**Practice:** Configure SW Maps with correct UTM zone EPSG code for your site. Use consistent coordinate system for all data collection and processing.

### From Section 5.8 (Physical and Environmental Factors)

**Concept:** Sky view, multipath, and atmospheric conditions affect RTK performance and accuracy.

**Practice:** Select base station location with open sky >15° elevation. Keep rover away from reflective surfaces. Survey during favorable conditions (avoid extreme heat, heavy rain).

---

## The Integrated Survey Process

Chapter 5 provided the conceptual toolkit. Chapter 9 provides the procedural roadmap. The integration looks like this:

**Conceptual Understanding (Chapter 5):**
"I understand that RTK requires two receivers working together, that fix status indicates centimeter-level accuracy, that quality gates ensure reliable measurements, and that PPP improves absolute positioning."

**Procedural Execution (Chapter 9):**
"I will set up the base station with 30-60 minute survey-in, establish check points for quality control, collect GCP measurements only with FIX status and all quality gates met, monitor check points throughout the day, log RINEX data for PPP processing, and validate results through check point drift and reprojection errors."

**Outcome:**
Ground control points surveyed with 1-3 cm relative accuracy, suitable for accurate OpenRiverCam transformation. Optional PPP post-processing provides 2-10 cm absolute accuracy for geospatial integration.

The concepts explain why each procedure matters. The procedures ensure concepts translate into accurate field measurements.

---

## Summary: Key Concepts for Field Survey

**Coordinate systems:**
- Use correct UTM zone for your site (determine from longitude)
- Specify complete EPSG code in all configurations
- Be consistent throughout project

**Local vs global frame:**
- Local frame (base station survey-in): 1-3 cm relative, ~25 cm absolute
- Global frame (with PPP): 1-3 cm relative, 2-10 cm absolute
- Local frame sufficient for transformation, global frame needed for integration

**RTK fix requirements:**
- Only collect points with FIX status (not Float or Single)
- Maintain fix ≥10 seconds before saving
- Meet all quality gates (satellites, PDOP, precision)
- Be patient during initialization (5-20 minutes normal)

**PPP workflow:**
- Log RINEX data during survey (6-12 hours)
- Convert UBX to RINEX with convbin
- Submit to AUSPOS (or similar service)
- Apply corrections to all survey data in post-processing

**Quality standards:**
- Establish and monitor check points (CP_START, CP_NOON, CP_END)
- Accept ≤3cm H / ≤4cm V check point drift
- Verify all measurement quality gates before saving points
- Validate with reprojection errors (≤5cm excellent, ≤10cm acceptable)

**Chapter 5 to Chapter 9 connection:**
- Chapter 5 concepts explain why procedures matter
- Chapter 9 procedures ensure concepts translate into accurate data
- Understanding concepts makes you a better practitioner
- Following procedures ensures reliable results

You are now prepared to understand the detailed field procedures in the following sections. Each procedure implements these concepts systematically to achieve the accuracy OpenRiverCam requires.

---

**Next Section:** [9.2 Survey Preparation (Day Before)](02-survey-preparation.md)
