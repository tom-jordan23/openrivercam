# RIVER SURVEY PROCEDURE: A PRACTICAL GUIDE

**Equipment:** ArduSimple RTK + Android + GNSS Master + SW Maps
**Target Accuracy:** Centimeter-level relative positioning, ~0.25m absolute via PPP
**CRS:** UTM zone for your location (determine using instructions in Section 1)

## HOW THIS WORKS: UNDERSTANDING THE APPROACH

### Why We Need Survey-Grade Positioning

River flow measurements from video rely on a precise chain of data transformations. The camera captures moving water as pixels. Software converts those pixels into real-world velocities. Those velocities integrate across the channel to produce discharge estimates. Each step in this chain amplifies errors from the previous step.

The amplification matters. A 5cm error in ground control point position translates to velocity errors of 5-10 cm/s. Those velocity errors compound into discharge uncertainties of 10-20%. For river monitoring applications where management decisions depend on accurate flow data, these errors accumulate into decisions based on flawed information.

Survey-grade positioning prevents this error cascade. When you measure ground control points with centimeter accuracy, you establish a foundation that maintains precision through the entire processing chain. The camera transformation becomes reliable. The velocity calculations stay within acceptable bounds. The discharge estimates support confident decision-making.

### The Base-Rover System

We use Real-Time Kinematic positioning—a two-receiver system that achieves centimeter accuracy through error elimination. The base station sits at a known location, continuously receiving satellite signals and calculating what errors affect those signals. The rover moves to the points you want to measure. The base broadcasts corrections to the rover in real-time. Common errors—atmospheric delays, satellite clock drift, orbital uncertainties—cancel out because both receivers experience nearly identical conditions.

This approach works because proximity matters. When base and rover sit within 10-20 kilometers of each other, they look through essentially the same atmosphere to the same satellites. The errors affecting one receiver also affect the other. Subtract the base's known errors from the rover's measurements, and you achieve 1-2 cm horizontal accuracy, 2-3 cm vertical.

It's important to understand that RTK accuracy depends entirely on the base station's position accuracy. If your base coordinates are wrong by 30cm, your rover measurements will be wrong by 30cm. This is why we establish base positions using Precise Point Positioning—a global correction service that provides 2-5 cm absolute accuracy anywhere on Earth.

### Quality Control Through Check Points

You cannot verify accuracy by measuring the same points you used to establish accuracy. This circular logic hides systematic errors. Check points solve this problem by providing independent validation—points you measure with the same precision as ground control points but never use in processing.

Think of check points as the answer key for a test. You solve the photogrammetric transformation using your ground control points, then check your solution against known positions you held back. The difference between predicted and actual check point coordinates reveals your system's true accuracy. If check point errors stay below 5cm, your velocity measurements will maintain acceptable uncertainty. If errors exceed 10cm, something went wrong—base position, satellite geometry, atmospheric conditions, or measurement procedures.

This independent validation provides confidence that your system works correctly and quantifies the uncertainty in your final discharge estimates.

---

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
10. [Post-Processing & Coordinate Correction](#10-post-processing--coordinate-correction)

### APPENDICES
- [A. GNSS Master Setup](#appendix-a-gnss-master-setup)
- [B. SW Maps Configuration](#appendix-b-sw-maps-configuration)
- [C. Base Station u-center Config](#appendix-c-base-station-u-center-config)
- [D. Sample Video Collection](#appendix-d-sample-video-collection)
- [E. Troubleshooting](#appendix-e-troubleshooting)
- [F. AUSPOS Submission](#appendix-f-auspos-submission)
- [G. CSRS-PPP Submission](#appendix-g-csrs-ppp-submission)
- [H. GAPS Submission](#appendix-h-gaps-submission)

---

## SURVEY SUCCESS CRITERIA

Every field day must meet these thresholds. Missing any single criterion compromises data quality and invalidates the survey. These are not suggestions—they are requirements derived from error propagation analysis in photogrammetric velocity measurements.

- [ ] RTK FIX maintained throughout survey
- [ ] Base station online entire duration
- [ ] Check point drift ≤3cm H, ≤4cm V
- [ ] Min 12 satellites, PDOP ≤2.5

**Why These Thresholds:** RTK FIX ensures centimeter accuracy. If the rover drops to FLOAT solution even briefly, that measurement degrades to 10-50cm accuracy. Base station interruptions break the correction stream and force the rover back to autonomous mode—2-10 meter accuracy. Check point drift exceeding 3cm indicates systematic problems with the base position or atmospheric modeling. PDOP above 2.5 means poor satellite geometry that amplifies measurement errors. Fewer than 12 satellites reduces redundancy and increases vulnerability to signal obstructions.

---

## QUALITY GATES

**You must verify these conditions before saving each point.** The software can display good-looking numbers while the underlying solution remains unreliable. These gates prevent collecting data that appears acceptable in the field but fails during post-processing.

**Standard Environment:** RTK FIX ≥10s, PDOP ≤2.5, Sats ≥12, Precision ≤2cm H/3cm V
**Canal Environment:** RTK FIX ≥10s, PDOP ≤3.0, Sats ≥10, Precision ≤4cm H/6cm V

**Why Different Standards:** Canal environments often present challenging satellite visibility due to vegetation, terrain, or structures. The relaxed thresholds acknowledge these constraints while maintaining acceptable accuracy for discharge measurements. Standard environments should achieve optimal accuracy since nothing prevents it. Applying canal thresholds in open environments wastes the opportunity for better precision.

**Understanding PDOP:** Position Dilution of Precision measures satellite geometry quality. PDOP multiplies your receiver's base precision to produce actual position error. With 1cm receiver precision and PDOP of 2.5, expect ~2.5cm actual error. PDOP above 6 means satellites cluster in one part of the sky—weak geometry that amplifies errors. PDOP below 2 indicates excellent satellite distribution across the sky dome.

**Why 10 Seconds:** RTK solutions can briefly achieve FIX status, then lose it. Requiring 10 seconds of stable FIX ensures the solution is robust, not a momentary convergence. This prevents recording points just as the solution degrades.

---

# DAY-BEFORE SETUP

Testing at home prevents discovering problems in the field. Every connection point in this system can fail—USB cables, mock location permissions, coordinate system settings, quality threshold configurations. Finding failures at your desk costs minutes. Finding them at a remote river site costs hours and potentially invalidates the field day.

## 1) Software Setup

### Why This Matters

The positioning chain flows from base station through rover to GNSS Master to SW Maps. A misconfiguration anywhere in this chain breaks the entire system. USB debugging must be enabled or Android blocks the connection. Mock location must designate GNSS Master or the operating system ignores external GPS data. The coordinate system must match your processing workflow or points end up in the wrong location.

Testing the full system integration reveals these problems before they matter. You want to discover that SW Maps doesn't recognize RTK FIX status while sitting at home with documentation available, not while standing in a river trying to remember obscure settings.

### Android & GNSS Master
- [ ] Install GNSS Master app → [Full setup guide](#appendix-a-gnss-master-setup)
- [ ] Enable Developer Options, Mock Location
- [ ] Test USB connection with rover
- [ ] Verify mock location works with test apps

**Developer Options:** Android hides these settings by default. You must tap Build Number seven times to unlock them. This feels like a hack because it is—Google doesn't want average users enabling features they don't understand. You need these features because you're replacing the phone's internal GPS with survey-grade external positioning.

**Mock Location:** This setting tells Android which app is allowed to override the internal GPS. Without this designation, Android ignores GNSS Master's position data and continues using the phone's internal GPS—which provides 3-10 meter accuracy instead of centimeter-level precision. Verify this works by opening Google Maps and confirming it shows the external receiver's position.

### SW Maps Project
- [ ] Create new project → [Full configuration guide](#appendix-b-sw-maps-configuration)
- [ ] Determine correct UTM zone for your location → [Instructions below](#determining-your-utm-zone)
- [ ] Set CRS to your UTM zone EPSG code (example: EPSG:32748 for UTM 48S)
- [ ] Create survey layers with attributes
- [ ] Test GPS integration with GNSS Master

**Coordinate System Criticality:** Your UTM zone provides metric coordinates for your survey area. Getting this wrong means your points save in the wrong coordinate system—potentially wrong by hundreds of kilometers after transformation. SW Maps remembers this setting per project, so configure it correctly now rather than discovering mismatched coordinates during post-processing.

### Determining Your UTM Zone

The Universal Transverse Mercator system divides Earth into 60 north-south zones, each 6° of longitude wide. Using the correct zone for your location ensures minimal distortion and accurate metric coordinates.

**Find Your UTM Zone:**

1. **Locate your site coordinates** in decimal degrees (use Google Maps: right-click → "What's here?")
   - Example: Sukabumi, Indonesia = -6.9175°, 106.9269°

2. **Calculate UTM zone number** from longitude:
   - Formula: `Zone = floor((Longitude + 180) / 6) + 1`
   - Example: `floor((106.9269 + 180) / 6) + 1 = floor(47.82) + 1 = 48`
   - Or use online calculator: https://www.dmap.co.uk/utmworld.htm

3. **Determine hemisphere:**
   - Positive latitude (north of equator) = North (N)
   - Negative latitude (south of equator) = South (S)
   - Example: -6.9175° = South

4. **Find EPSG code:**
   - Northern hemisphere: `326XX` where XX is the zone number
   - Southern hemisphere: `327XX` where XX is the zone number
   - Example: Zone 48 South = 32748
   - Verify at https://epsg.io/

**Complete Example (Sukabumi, Indonesia):**
- Coordinates: -6.9175°, 106.9269°
- Zone: 48
- Hemisphere: South
- UTM designation: 48S
- EPSG code: 32748
- Full name: WGS 84 / UTM zone 48S

**Important Notes:**
- If your site spans a zone boundary, pick the zone containing most of the site
- Stay within the same zone for all related surveys
- Record the EPSG code in your field notes for reference

**Layer Attributes:** Define these before the field day. Creating attributes in the field slows collection and increases errors. Each layer needs specific attributes—point ID, measurement time, PDOP, satellite count, precision estimates, point role. Plan the attributes you'll need for quality control and processing.

### Integration Test
- [ ] Full system test: Base → Rover → GNSS Master → SW Maps
- [ ] Verify RTK FIX status appears in SW Maps
- [ ] Test point collection with quality thresholds

**Full System Verification:** Power on the base, connect the rover, open GNSS Master, launch SW Maps. You should see RTK FIX status, satellite count, PDOP values, and precision estimates. If any of these elements are missing, trace back through the connection chain to find the break. Save a test point and verify all attributes populate correctly.

**Quality Threshold Testing:** Configure SW Maps to reject points that don't meet your quality gates. Try to save a point without RTK FIX—it should refuse. This prevents accidentally recording poor-quality data when you're focused on field logistics rather than data validation screens.

---

## 2) Equipment Check

Battery failure represents the most common field day problem that ends the survey. Most other equipment issues can be addressed with available alternatives. Dead batteries provide no alternative and end the day. Calculate your power budget conservatively—the base station might run 8-12 hours, the rover 6-8 hours, the Android device 4-6 hours with screen on. Add backup capacity because cold weather reduces battery performance and you'll use more power than expected.

**Power Systems:**
- [ ] Base station: Full charge + backup battery
- [ ] Rover: Full charge
- [ ] Android: 100% + power bank
- [ ] All USB cables tested

**Cable Testing:** USB cables fail silently. They look fine but have broken data lines. Test every cable you'll use by verifying data transfer, not just charging. A cable that charges a device might not support the USB serial communication the rover needs.

**Physical Equipment:**
- [ ] Survey poles (primary + backup), bipod
- [ ] Steel tape measure, markers
- [ ] Base tripod, antenna cables
- [ ] Waterproof notebook, pencils

**Redundancy Philosophy:** Bring backup survey poles. If you drop your primary pole in the river or damage it on rocks, you need a replacement immediately. The same applies to markers, notebooks, and anything else that's small, inexpensive, and critical to operations if lost. Base equipment is large and expensive—you won't carry a backup tripod—so inspect it carefully before leaving.

---

# FIELD DAY

## 3) Base Station Setup

The base station is your reference point for the entire survey. Every measurement you make today depends on this station maintaining stable position and broadcasting corrections continuously. Take time to establish it correctly—rushing this step undermines everything that follows.

### Why Site Selection Matters

Satellite signals travel from space at radio frequencies. These frequencies experience delays when passing through the atmosphere, reflections when bouncing off surfaces, and complete blockage when hitting solid objects. Your base station must receive clean signals from satellites distributed across the sky dome to calculate accurate corrections.

Trees, buildings, vehicles, and terrain create reflections—multipath errors that show up as positions jumping around by several centimeters. Metal objects reflect signals particularly well. Water bodies can cause significant multipath. A poor site selection introduces errors that no amount of processing can remove.

### Site Selection
- [ ] Open sky >15° above horizon, >10m from metal/vehicles
- [ ] Stable ground, accessible for monitoring
- [ ] For canals: High ground >20m from water

**Elevation Mask (15°):** Satellites near the horizon transmit signals through more atmosphere—more delay, more error. The elevation angle cutoff rejects these poor-quality signals. Some receivers allow configuring this mask. Keep it at 10-15° for balanced coverage and quality.

**Metal and Water Setback:** Radio waves reflect off conductive surfaces. Park your vehicle 10+ meters away. If that's not possible, place the base on the opposite side from the work area so reflected signals don't contaminate measurements. Position the base well away from canal water—at least 20m—to avoid water surface reflections.

**Accessibility:** You need to monitor this base station periodically throughout the day. If RINEX logging stops, corrections halt, or power fails, you must know immediately. Place the base where you can check it without interrupting survey work.

### Setup Process
- [ ] Connect antenna BEFORE powering base
- [ ] Level tripod, mark exact point
- [ ] Measure antenna height to ARP (3 measurements)
- [ ] u-center configuration → [Detailed setup](#appendix-c-base-station-u-center-config)

**Antenna Connection Order:** GPS receivers can damage their RF front-end if powered on without an antenna connected. The power meant for the antenna reflects back into the receiver and potentially burns out sensitive components. Always connect the antenna before applying power. Always disconnect power before removing the antenna.

**Antenna Reference Point (ARP):** The receiver doesn't measure from the ground—it measures from a specific point in the antenna called the phase center. The ARP marks the bottom of the antenna where you measure height from. Measure from the mark on the ground to the ARP three times and average them. Height errors directly add to elevation errors in your final coordinates.

**Marking the Point:** You might need to return to this exact spot for future surveys or to verify position stability. A paint mark, labeled stake, or precisely described location in photos allows repositioning within centimeters.

### Survey-In Process
- [ ] 30-60 minute survey-in for 0.25m accuracy
- [ ] Monitor: PDOP ≤1.5, Satellites ≥15
- [ ] Record final coordinates in your UTM zone
- [ ] Start RINEX logging (6-12 hours)

**What Survey-In Does:** The base station collects position fixes continuously and averages them. Each individual fix might be wrong by several meters due to atmospheric conditions and satellite errors. But errors are random—sometimes north, sometimes south, sometimes up, sometimes down. Averaging over time cancels these random errors and converges toward true position.

**Duration vs. Accuracy:** A 60-second survey-in produces ~2-5 meter accuracy. Adequate for local relative positioning but poor for absolute coordinates. A 30-minute survey-in achieves ~0.5-1 meter—acceptable for temporary base setups. A 24-hour collection processed with PPP reaches 2-5 cm—required for permanent installations. We use 30-60 minutes for field days because rover accuracy depends more on stable base position than absolute base position. PPP post-processing corrects the absolute position later.

**RINEX Logging:** This raw data file enables PPP post-processing. The receiver saves every satellite observation—carrier phase measurements, pseudoranges, satellite ephemeris data—in a binary format. You'll convert this to RINEX format later for PPP processing. Start logging at the beginning of the day and stop at the end. The longer the observation session, the better the PPP accuracy.

**Why Good PDOP Matters Here:** The base station calculates corrections from its position solution. If that solution has poor geometry (high PDOP), the corrections contain errors. These errors propagate to the rover. Target PDOP ≤1.5 at the base for clean corrections.

---

## 4) Check Points

Check points provide the only independent validation of your system accuracy. Without them, you're assuming your measurements are correct with no evidence. With them, you can quantify actual error and demonstrate that your data meets accuracy requirements.

### Why We Establish Check Points First

Survey check points at the start of the day, after 4-6 hours, and at the end of the day. This temporal sequence reveals whether your base position drifts or your RTK solution degrades over time. Atmospheric conditions change throughout the day—ionospheric delays follow solar activity patterns, tropospheric delays respond to temperature and humidity changes. These changing conditions can cause apparent position shifts even when the base station stays physically stationary.

If your check point measurements agree within 3cm across the entire day, your system maintains stable accuracy. If drift exceeds 3cm, something changed—base position error, atmospheric modeling failure, or satellite geometry degradation. You need to identify and correct the problem before using that day's data.

### Establish CP_START
- [ ] 20-50m from base, stable high ground
- [ ] RTK FIX for 30 seconds
- [ ] 3 independent 60s measurements
- [ ] Agreement within 1cm H, 2cm V
- [ ] Mark permanently, photograph

**Distance from Base:** Check points should be far enough from the base to experience rover-like conditions but close enough to ensure solid RTK FIX. The 20-50m range achieves this balance. Too close and you're not testing real survey conditions. Too far and you might encounter RTK challenges that don't reflect conditions at the site.

**Three Independent Measurements:** Measure the point, move the pole completely off the mark, then remeasure. Do this three times with 60 seconds of occupation each time. Calculate the spread in coordinates. If the three measurements don't agree within 1cm horizontal and 2cm vertical, your RTK solution is unstable—either poor satellite geometry, multipath contamination, or insufficient convergence time. Don't proceed with surveying until you resolve this.

**Why This Agreement Matters:** You're testing repeatability—the receiver's ability to measure the same point consistently. If you can't measure one point three times with centimeter agreement, you can't trust any individual measurement to be correct within centimeters. This test validates that your system delivers the precision you need before you invest hours measuring ground control points.

**Permanent Marking:** Drive a stake, spray a paint mark, or create a described position from photos. You'll return to this exact point twice more today. You might return to it on future field days to validate long-term system stability.

### Monitor Throughout Day
- [ ] CP_NOON: Re-measure after 4-6 hours
- [ ] CP_END: Final check before packing
- [ ] Total drift must be ≤3cm H, ≤4cm V

**Interpreting Drift:** Small drift (≤3cm) is normal and acceptable—atmospheric conditions change, satellite geometry evolves, receiver noise is random. Drift in this range doesn't compromise survey quality because it's smaller than your required accuracy threshold.

Drift exceeding 3cm horizontal or 4cm vertical signals problems. The base station might have physically moved (tripod settling, ground instability). The base position calculation might have been wrong (insufficient survey-in duration, poor satellite geometry). Atmospheric conditions might have changed dramatically (ionospheric storm, rapid weather front). Investigate the cause and decide whether to continue surveying or restart the base setup.

**What to Do If Drift Exceeds Limits:** Stop surveying. Return to the base station and verify it hasn't moved physically. Check the base receiver display for RTCM output, satellite count, and position stability. Review the sky plot for satellite geometry changes. If everything looks normal at the base but check points show drift, you may be experiencing localized atmospheric anomalies or multipath at the check point location. Try measuring a different check point. If problems persist, consider restarting the survey-in process or postponing the field day.

---

## 5) Camera & Control Points

Ground control points tie the camera's pixel coordinate system to real-world UTM coordinates. The transformation quality depends on having well-distributed points with accurately known positions. Poor GCP distribution—clustering in one area or all at similar distances from the camera—creates a weak geometric solution that increases velocity uncertainty.

### Why GCP Distribution Matters

Imagine trying to level a table using only three points, all on one side. The other side remains unconstrained. GCP distribution follows the same principle. Points around the perimeter of the camera view constrain the transformation across the entire image. Points clustered in one area leave other regions poorly constrained.

Photogrammetric transformation errors increase with distance from the nearest GCP. If you measure five GCPs on the left bank but none on the right bank, velocity measurements on the right side will have higher uncertainty than those on the left. The software can still calculate velocities—but the errors might be 2-3 times larger in unsupported regions.

### Camera Position
- [ ] 5-10m height, 15-45° viewing angle
- [ ] Survey camera position with rover
- [ ] Record height, direction, tilt angle

**Why Survey Camera Position:** Knowing the camera's exact position enables direct georeferencing as a backup approach. If something goes wrong with GCP-based transformation—too few visible points, poor distribution, measurement errors—you can fall back to camera position and orientation. This redundancy provides insurance against field mistakes.

**Recording Geometry:** Note the camera height above ground, compass direction it faces, and tilt angle. These parameters help reconstruct the viewing geometry during processing and support quality control checks. If calculated GCP positions don't align with observed camera geometry, something went wrong—either the GCP measurements or the processing.

### Control Points
- [ ] Place 6+ visible targets in camera FOV
- [ ] Take sample video → [Detailed procedure](#appendix-d-sample-video-collection)
- [ ] Survey each control point after video
- [ ] Use Ground Control Points layer

**Minimum Six Points:** Photogrammetric transformation solves for camera position, orientation, and lens distortion. This requires at least 6 ground control points with known 3D coordinates. More points improve the solution robustness and allow detecting outliers. Aim for 8-10 GCPs for reliable transformation.

**Survey After Video:** You need the video to show where the targets are positioned while the water is flowing. Survey the targets after recording because you'll spend 60+ seconds per point and can't leave the camera running that long. This sequence ensures the video captures representative flow conditions while the survey achieves required precision.

**Target Visibility:** Each target must be clearly identifiable in the video and accurately measurable in the field. High-contrast colored panels (orange, white, or checkerboard patterns) work well. Retroreflective tape improves visibility. Position targets on stable surfaces—rocks, concrete, driven stakes—not vegetation that might move in the wind.

---

## 6) Water Level Survey

Water surface elevation provides the reference datum for all cross-section measurements and enables converting surveyed bed elevations into flow depths. This simple measurement is surprisingly important—a 2cm error in water level produces a 2cm error in calculated depth for every point in the cross-section.

### Why Water Level Accuracy Matters

Discharge calculations integrate velocity across the cross-sectional area. Area depends on width (easy to measure accurately) and depth (depends on bed elevation and water surface elevation). If your water level measurement is wrong by 5cm, every depth value is wrong by 5cm, and the entire cross-sectional area shifts by channel_width × 0.05m. For a 10m wide channel, that's 0.5 m² of area error, which translates directly to discharge error.

### Setup
- [ ] Identify stable water level measurement point
- [ ] Use staff gauge or direct measurement method
- [ ] Record water surface conditions (calm/turbulent)

**Stable Measurement Location:** Avoid turbulent zones, surface boils, eddy lines, or wave action. Find a calm section where the water surface stays relatively level. In rivers with significant turbulence, you might need to average multiple measurements or accept higher uncertainty.

**Surface Conditions:** Note whether the water is calm, choppy, or turbulent. This metadata helps interpret measurement uncertainty and explains discrepancies during quality control. A ±2cm measurement in calm water is more reliable than ±2cm in turbulent conditions where the surface varies by 5-10cm.

### Measurement
- [ ] Survey water surface elevation with rover pole
- [ ] **Note depth on pole**, maintain RTK FIX
- [ ] Record in Water Level layer with flow conditions
- [ ] Take multiple measurements if water is moving
- [ ] Document measurement method and accuracy

**Pole Depth Recording:** You're measuring the water surface, not the pole tip. Hold the pole vertically with the tip submerged some distance below the surface. Note exactly where the water line crosses the pole. Measure this depth later with a tape measure. The water surface elevation equals the surveyed pole position minus the pole height measurement plus the depth below water.

The math matters: `Water_Surface_Elevation = GPS_Position_Z - Pole_Height + Depth_Below_Surface`. Get the signs right or your water level will be wrong by twice the depth measurement.

**RTK FIX Requirement:** This measurement needs the same accuracy as ground control points. Wait for stable RTK FIX, verify PDOP ≤2.5 and satellites ≥12, then occupy the position for 60 seconds. Don't shortcut this measurement because it affects every depth calculation.

**Multiple Measurements:** If the water surface moves (waves, turbulence, fluctuations), take 3-5 measurements and average them. This reduces the impact of instantaneous surface variations. Note the range of measurements as an uncertainty estimate.

---

## 7) Point Collection

Every point you save becomes part of your dataset. There's no "fixing" poor-quality points during post-processing—the errors are baked in. Quality gates prevent saving data that looks acceptable on-screen but contains hidden problems that emerge during analysis.

### Why Quality Gates Matter

RTK receivers display position information continuously, updating every second. These displays show positions even when the solution is poor—FLOAT mode with 50cm accuracy or autonomous mode with 5m accuracy. The coordinates appear on-screen with the same confidence as centimeter-accurate FIX mode. Nothing in the display says "this is wrong"—you must check solution status, PDOP, satellite count, and precision estimates to know whether the position is reliable.

Quality gates enforce these checks. Configure SW Maps to require RTK FIX, PDOP ≤2.5, satellites ≥12, and precision ≤2cm horizontal before allowing point saves. This prevents recording bad data when you're distracted by field logistics and not watching the status indicators carefully.

### Quality Requirements
- [ ] All quality gates met (see top of document)
- [ ] Averaging times: 60s standard, 120s canal
- [ ] Pole bubble centered, measure height each shot

**Averaging Time:** RTK positions jump around by ±1-2cm even in FIX mode due to remaining atmospheric noise, multipath, and receiver noise. Averaging over 60 seconds reduces this scatter and provides a more stable position. Longer averaging (120s) helps in challenging environments where signal quality is marginal.

Don't shortcut the averaging time. The software might achieve FIX status after 10 seconds, but that doesn't mean the position is fully converged. The full averaging period ensures the solution stabilizes and produces repeatable results.

**Pole Bubble:** Survey poles include a bubble level. Center it precisely before saving the point. A tilted pole introduces horizontal position error and elevation error. A 2m pole tilted 5° displaces the tip by ~17cm horizontally—far beyond your accuracy target. Keep the pole vertical.

**Measure Pole Height Every Shot:** Pole height measures from the GPS antenna to the pole tip. This varies slightly depending on how you configure the pole sections. Measure it with a tape measure before each point or at minimum verify it hasn't changed. A 1cm error in pole height produces a 1cm elevation error in the final coordinate.

### Standard Protocol
- [ ] Verify RTK FIX ≥10 seconds
- [ ] Check precision estimates in SW Maps
- [ ] Record all required attributes
- [ ] If conditions fail: wait 2min → move 2-3m → retry

**Precision Estimates:** SW Maps displays horizontal and vertical precision values calculated by the receiver. These represent the receiver's confidence in its position solution based on satellite geometry, signal quality, and correction age. Precision ≤2cm horizontal and ≤3cm vertical indicates good conditions. Higher values suggest problems even if you have RTK FIX status.

**Failure Recovery:** Sometimes a location has poor satellite visibility—tree cover, terrain shadowing, buildings. The receiver can't achieve FIX or maintains marginal quality. Wait 2 minutes to see if conditions improve as satellites move. If not, move 2-3 meters to escape multipath or obstruction issues. If problems persist, that location might not be measurable with your current base setup—document it and consider an alternative GCP location.

**Required Attributes:** Record point ID, measurement time, PDOP, satellite count, precision estimates, point role (GCP, check point, cross-section, etc.), and any notes about conditions. These attributes enable quality control during processing and provide documentation for your dataset.

---

## 8) Cross-Section Survey

Cross-section surveys map the channel bed geometry from left bank to right bank. This data supports discharge calculations, validates rating curves, and documents channel changes over time. The survey accuracy requirements match those for ground control points—centimeter-level precision for reliable results.

### Why Systematic Collection Matters

You're creating a spatial model of the channel bed. Models work best with evenly spaced, high-quality data points. Clustering measurements in easy-to-reach areas while skipping difficult sections creates gaps that interpolation must fill. These gaps introduce uncertainty. Systematic spacing ensures the model accurately represents the bed geometry without artifacts from irregular sampling.

### Setup
- [ ] Establish LB/RB reference points on stable ground
- [ ] Plan station spacing (1-2m typical)
- [ ] Document section ID, flow conditions

**Reference Points:** Mark clear left bank and right bank endpoints. Survey these with the rover to establish precise coordinates. They serve as anchor points for the cross-section and enable returning to the same transect line in future surveys. If you're monitoring temporal changes, you need to measure the same cross-section each time—these reference points make that possible.

**Station Spacing:** Choose spacing based on bed complexity. A uniform, smooth bed might need only 2m spacing. A complex bed with boulders, steps, or vegetation needs tighter spacing (1m or less) to capture features adequately. In the deepest part of the channel where velocity and flow are highest, tighter spacing improves accuracy since this zone contributes most to discharge.

**Flow Conditions:** Record whether the water is low, medium, or high flow, and whether it's rising or falling. This context helps interpret the discharge measurements and relate them to other hydrological data. Note any unusual conditions—debris accumulation, ice, aquatic vegetation—that might affect either the survey or the flow.

### Collection
- [ ] Walk LB → RB systematically
- [ ] Each station: verify quality gates, 60-120s averaging
- [ ] Record station number, point role, water depth
- [ ] Measure pole height tip-to-ARP each shot

**Systematic Traverse:** Start at left bank and walk toward right bank, measuring at planned intervals. Don't skip stations because they're difficult to reach or in deep water. Those difficult stations often represent important geometric features. If a station is truly impossible to measure safely, document why and interpolate carefully during processing.

**Quality Verification:** Check RTK FIX status, PDOP, and satellite count before every point. Don't assume conditions remain good just because the previous point worked. Satellite geometry changes continuously, and local obstructions affect each position differently.

**Water Depth Recording:** At each station in the wetted channel, note the depth from the water surface to the bed. This provides redundant information—you're also calculating depth from the difference between water surface elevation and surveyed bed elevation. The two methods should agree within a few centimeters. If they don't, you've found a measurement error to investigate.

**Station Numbering:** Use a consistent convention: 0 at left bank, increasing toward right bank. This makes processing easier and reduces mistakes. Record the station number as an attribute so you can reconstruct the sequence during analysis.

---

## 9) End of Day

The survey isn't complete until you've verified data quality, backed up files, and documented any deviations from standard procedure. Leaving the field site with unverified data means discovering problems when you can't return to fix them.

### Final Checks
- [ ] Re-measure CP_END, calculate total drift
- [ ] Stop RINEX logging, record end time
- [ ] Export SW Maps data (CSV + native format)
- [ ] Multiple backups on different devices
- [ ] Document any deviations from protocol

**Check Point Verification:** The CP_END measurement tells you whether your system maintained accuracy throughout the day. Compare it to CP_START coordinates. If drift exceeds 3cm horizontal or 4cm vertical, you have a problem that requires investigation. Don't wait until you're back at the office to discover this—check it while you're still on-site with the equipment available to diagnose issues.

**RINEX Logging:** Stop the logging and safely save the file. This raw data enables PPP processing to determine accurate base station coordinates. Handle the file carefully—it's irreplaceable. If you lose this file, you can't apply PPP corrections, and your data remains at survey-in accuracy (~0.5-1m) rather than PPP accuracy (2-5cm).

**Data Export:** SW Maps stores data in an internal database. Export it to CSV (human-readable, easy to process) and native GeoPackage format (preserves coordinate system metadata and attributes). Save both formats. CSV provides compatibility with generic processing tools. GeoPackage preserves spatial information correctly for GIS software.

**Multiple Backups:** Copy the exported files to at least two separate devices immediately—Android storage, USB drive, laptop, cloud storage. Memory cards fail. Phones get dropped in rivers. Having multiple backups means no single failure loses your day's work. Don't wait until evening at the hotel—back up on-site before leaving.

**Deviation Documentation:** If anything didn't go according to plan—abbreviated averaging times, relaxed quality thresholds, skipped check points, base station interruptions—document it in writing while the details are fresh. These notes explain data anomalies during processing and help assess whether the data remains usable for its intended purpose.

---

# POST-PROCESSING

## 10) Post-Processing & Coordinate Correction

Post-processing transforms your field data from local relative accuracy to global absolute accuracy. The base station survey-in process provided ~0.5-1 meter coordinates adequate for RTK corrections, but you need centimeter-level absolute coordinates for long-term monitoring and data integration with other surveys.

### Why Post-Processing Matters

Precise positioning services use reference station networks and global satellite orbit and clock corrections to calculate your base station position within 2-5cm anywhere on Earth. This accuracy enables combining data from multiple surveys, integrating with existing geodetic infrastructure, and detecting long-term position changes at monitoring sites.

Without post-processing correction, your survey has excellent internal consistency—points measured relative to each other are accurate to 1-2cm—but unknown absolute position. With precise positioning, the entire survey has known global coordinates that support integration with other datasets and temporal analysis.

---

## Step 1: Convert UBX to RINEX

Your base station recorded raw observations in u-blox UBX format. This proprietary binary format works with u-blox software but isn't compatible with PPP services. RINEX (Receiver Independent Exchange Format) provides a standardized format that all PPP services accept.

### Using RTKLIB CONVBIN (Command Line)
- [ ] Open command prompt/terminal in directory with UBX file
- [ ] Run: `convbin -od -os -oi -ot -f 1 your_file.ubx`
  - `-od`: Output observation data (.obs)
  - `-os`: Output satellite ephemeris (.nav)
  - `-oi`: Output ionosphere parameters
  - `-ot`: Output time parameters
  - `-f 1`: RINEX version 1 format
- [ ] Alternative for specific time range: `convbin -od -os -ts 2024/11/14 10:00:00 -te 2024/11/14 18:00:00 your_file.ubx`
- [ ] Verify .obs and .nav files created successfully

**What These Flags Mean:** The CONVBIN command extracts different data types from the binary UBX file. Observation data (-od) contains the raw measurements from satellites. Ephemeris data (-os) contains satellite orbit predictions. Ionosphere and time parameters support atmospheric modeling. PPP services need all these data types to process your position accurately.

**Time Range Selection:** If your UBX file contains more than the survey session—for example, you left the receiver running overnight—you can extract only the relevant time range. This reduces file size and processing time. Use GPS time, not local time, for the start and end parameters.

**File Verification:** Check that both .obs and .nav files were created and contain data. Open them in a text editor—RINEX files are human-readable. You should see headers describing the receiver, antenna, and position, followed by rows of observation data. Empty files or files containing error messages indicate conversion problems.

### If CONVBIN Fails - Try RTKCONV GUI
- [ ] Launch RTKCONV, Input File: select .ubx file
- [ ] Options → Set "Input Format" to "u-blox UBX"
- [ ] Set "Output Format" to "RINEX OBS/NAV"
- [ ] Click Convert

**GUI Alternative:** The graphical version of CONVBIN provides the same functionality with a visual interface. Some users find it easier for occasional use. The command-line version excels for batch processing multiple files or integrating into automated workflows.

### Troubleshooting
- [ ] Ensure UBX file contains RXM-RAWX and RXM-SFRBX messages
- [ ] Try different RINEX versions (-f 2 or -f 3) if conversion fails
- [ ] Check file permissions and disk space

**Required Messages:** RXM-RAWX contains raw carrier phase measurements—the core data PPP needs. RXM-SFRBX contains satellite navigation data. If your base station wasn't configured to log these messages, the UBX file won't convert to useful RINEX. Verify the base station configuration before your next field day.

**RINEX Versions:** Version 3 supports modern multi-constellation GNSS better than version 2. However, some older PPP services only accept version 2. Try version 3 first, fall back to version 2 if the PPP service rejects the file.

---

## Step 2: Precise Positioning Service Processing

Precise positioning services process your base station observations to determine accurate global coordinates. These services use precise satellite orbit and clock products combined with reference station networks to achieve 2-5cm absolute accuracy.

### Understanding AUSPOS Processing

AUSPOS uses a network-based approach that combines your observations with data from up to 15 nearby reference stations from the IGS (International GNSS Service) and APREF (Asia-Pacific Reference Frame) networks. This differential processing method compares your measurements against known reference positions, using precise satellite products to model errors.

The key distinction: AUSPOS uses both precise satellite products AND a reference station network, which provides faster convergence and better accuracy for the Asia-Pacific region compared to standalone Precise Point Positioning (PPP) services that use only satellite products.

**Important Limitation:** AUSPOS processes GPS L1/L2 observations only. Your u-blox ZED-F9P receiver logs multi-GNSS data (GPS, GLONASS, Galileo, BeiDou), but AUSPOS ignores non-GPS observations during processing. This GPS-only approach still achieves excellent accuracy for the application.

### Submit for Processing (Indonesia Location)

**AUSPOS (Recommended for Asia-Pacific):** Upload RINEX to https://www.ga.gov.au/auspos
  - Network-based processing using APREF + IGS reference stations
  - Optimized for Indonesia and Southeast Asia region
  - Processes GPS L1/L2 dual-frequency data (other constellations ignored)
  - Free service provided by Geoscience Australia
  - **Antenna Selection:** Choose closest match from available options:
    - TRM29659.00 (Trimble multiband, good generic choice)
    - SEPCHOKE_MC (Septentrio choke ring, multiband)
    - LEIAT504GG (Leica multiband)
    - TWIVC6150 (Tallysman multiband)
    - Or select "Unknown" if no close match available
  - **Antenna Height:** Measure from ground to antenna phase center (bottom of antenna)

**Alternative Services (True PPP with Multi-GNSS):**

**CSRS-PPP (Natural Resources Canada):** https://webapp.csrs-scrs.nrcan-rncan.gc.ca/geod/tools-outils/ppp.php
  - True PPP with Ambiguity Resolution (PPP-AR) - fastest convergence
  - Multi-GNSS: GPS + GLONASS + Galileo
  - Sub-centimeter accuracy in <1 hour with PPP-AR
  - Best for shorter sessions (<4 hours)
  - Multiple product options (ultra-rapid, rapid, final)

**GAPS (University of New Brunswick):** https://gaps.gge.unb.ca
  - True PPP methodology
  - Multi-GNSS: GPS + GLONASS + Galileo
  - Academic service with well-documented algorithms
  - Best for cross-validation and research applications

**Processing Options:** Static, minimum 2-hour session (6-8 hours recommended, 24-hour optimal for best accuracy)

**Expected Accuracy:**
- AUSPOS (6-8 hours): 2-5cm horizontal, 5-10cm vertical
- CSRS-PPP (6-8 hours): 2-4cm horizontal, 3-6cm vertical
- CSRS-PPP with PPP-AR (<1 hour): Sub-centimeter horizontal
- GAPS (6-8 hours): 2-3cm horizontal, 3-5cm vertical

**Why AUSPOS for Indonesia:** Geoscience Australia operates and uses reference stations across the Asia-Pacific region (APREF network). This regional optimization provides excellent results for Southeast Asian locations. The service is free, reliable, and has processed over 1 million surveys globally. Research studies show AUSPOS performs particularly well in the Asia-Pacific region compared to global-only services.

### When to Use Each Service

**Use AUSPOS (Default) When:**
- Surveying in Indonesia, Southeast Asia, or Asia-Pacific region
- Following standard workflow with 6-8 hour base station sessions
- Want proven reliability with regional optimization
- GPS-only processing is sufficient for application needs

**Use CSRS-PPP When:**
- Survey sessions are shorter (<4 hours) and need fastest convergence
- Want to leverage multi-GNSS (GPS+GLONASS+Galileo) for better accuracy
- Need PPP-AR (Ambiguity Resolution) for sub-centimeter results in <1 hour
- AUSPOS is experiencing processing delays (>24 hours)
- Research or monitoring applications requiring multi-constellation data

**Use GAPS When:**
- Cross-validating AUSPOS results with independent service
- Academic research requiring well-documented PPP algorithms
- Algorithm transparency is important for publication or analysis
- Teaching or learning about PPP methodology

**Multi-GNSS Advantage:** Services like CSRS-PPP and GAPS that process multi-GNSS data can achieve 30-40% faster convergence and 18-30% better accuracy compared to GPS-only processing. For short sessions (<4 hours) or challenging observing conditions, multi-GNSS provides substantial benefits.

**Antenna Selection:** Precise positioning accuracy depends on knowing the antenna phase center—the electrical point where the antenna measures signals. This point varies by antenna model and frequency. Selecting the correct antenna model applies proper phase center corrections. If you can't find your exact model, choose a similar multiband antenna or "Unknown"—this degrades accuracy slightly (few millimeters) but remains better than wrong antenna selection.

**Antenna Height Accuracy:** Measure from your ground mark to the bottom of the antenna (the ARP) with millimeter precision. A 1cm error in antenna height produces a 1cm error in vertical coordinate. This measurement matters more for vertical accuracy than any other parameter you enter.

**Session Duration:** Precise positioning accuracy improves with observation time. A 2-hour session achieves ~5cm accuracy. A 6-hour session reaches ~3cm. A 24-hour session hits 2cm or better. Longer observations average out more atmospheric variations and satellite geometry changes. For permanent base stations, invest the time for 24-hour sessions. For temporary setups, 6-8 hours provides good accuracy with reasonable processing time.

### Service Comparison Table

| Feature | AUSPOS | CSRS-PPP | GAPS |
|---------|--------|----------|------|
| **Provider** | Geoscience Australia | NRCan Canada | Univ. New Brunswick |
| **Processing Method** | Network-based | True PPP with PPP-AR | True PPP |
| **Constellations** | GPS only (L1/L2) | GPS + GLO + GAL | GPS + GLO + GAL |
| **Accuracy (6-8hr)** | 2-5cm H, 5-10cm V | 2-4cm H, 3-6cm V | 2-3cm H, 3-5cm V |
| **Convergence (<1hr)** | N/A | Sub-cm (with PPP-AR) | Not specified |
| **Regional Optimization** | Asia-Pacific (APREF) | Global | Global |
| **Processing Time** | 1-4 hours | 2-8 hours | 2-6 hours |
| **Best For** | Indonesia/SEA surveys | Fast convergence | Cross-validation |
| **Cost** | Free | Free | Free |
| **Documentation** | [Appendix F](#appendix-f-auspos-submission) | [Appendix G](#appendix-g-csrs-ppp-submission) | [Appendix H](#appendix-h-gaps-submission) |

**Key:** H = Horizontal, V = Vertical, GLO = GLONASS, GAL = Galileo, PPP-AR = PPP with Ambiguity Resolution

All services accept RINEX files from your u-blox ZED-F9P receiver and provide adequate accuracy for river monitoring applications. The same RINEX file works for all services—submit to multiple services for cross-validation if desired.

### Record Processing Results
- [ ] Corrected coordinates: E_corrected, N_corrected, Z_corrected (in your UTM zone)
- [ ] Survey-in coordinates: E_survey, N_survey, Z_survey
- [ ] Calculate translation: ΔE = E_corrected - E_survey, ΔN = N_corrected - N_survey, ΔZ = Z_corrected - Z_survey

**Understanding the Translation:** Your rover measurements have centimeter accuracy relative to the survey-in base coordinates. The survey-in coordinates are wrong by ~0.5-1 meter in absolute terms. Precise positioning processing provides the true base coordinates. The difference between these coordinate sets represents the absolute error in your survey-in position.

You don't reprocess the RTK data—you simply translate all coordinates by this constant offset. This works because RTK relative accuracy is excellent even when the base coordinate is wrong. Adding the translation shifts everything to the correct absolute position while preserving the internal geometry.

**Coordinate Systems:** Processing services return coordinates in WGS84 geographic (latitude, longitude). Convert these to your UTM zone using a coordinate conversion tool or QGIS. This matches the coordinate system you used during field collection and simplifies the correction process. Use the same EPSG code you determined in Section 1.

**Equipment Compatibility Note:** Your u-blox ZED-F9P receiver logs observations from GPS, GLONASS, Galileo, and BeiDou constellations simultaneously. The RINEX file contains all constellation data. AUSPOS processes GPS L1/L2 only, ignoring other constellations. CSRS-PPP and GAPS process multi-GNSS data (GPS+GLONASS+Galileo), which can improve accuracy and convergence time by 18-40% compared to GPS-only processing. The same RINEX file works for all services—the processing service determines which constellations to use.

---

## Step 3: Apply Corrections in QGIS

QGIS provides tools for spatial data management, coordinate transformation, and quality control. The GeoPackage format SW Maps exports preserves all your coordinate system metadata and attribute information.

### Data Import
- [ ] Open QGIS, create new project
- [ ] Import SW Maps GeoPackage export (preserves CRS metadata)
- [ ] Verify CRS matches your UTM zone EPSG code - should be automatic
- [ ] Verify all survey points imported correctly with proper geometry

**GeoPackage vs. CSV:** GeoPackage is a spatial database format that stores geometry, attributes, and coordinate system information together. CSV stores only coordinates and attributes—you must specify the coordinate system manually. Using GeoPackage eliminates coordinate system mistakes and preserves complex attribute types.

**CRS Verification:** Check that QGIS recognized the coordinate system correctly. The project and all layers should show your UTM zone EPSG code (example: EPSG:32748 for UTM 48S). If you see EPSG:4326 (WGS84 geographic) or an unknown CRS, something went wrong during export or import. Fix this before proceeding—coordinate math only works when all data uses the same system.

### Apply PPP Translation
- [ ] Open Field Calculator for each layer in GeoPackage
- [ ] Create new fields: `E_corrected = "x_coord" + ΔE`, `N_corrected = "y_coord" + ΔN`, `Z_corrected = "z_coord" + ΔZ`
- [ ] Calculate bed elevations: `bed_elevation = Z_corrected - pole_height`
- [ ] Update geometry: Use "Update Geometry" tool with corrected coordinates
- [ ] Save changes to Geopackage (preserves all metadata)
- [ ] Validate: Check point repeatability should remain ≤3cm after correction

**Field Calculator:** This QGIS tool creates new attribute fields using calculations based on existing fields. You're adding the PPP translation to each coordinate. The x_coord and y_coord fields contain the original survey-in-based coordinates from the field. Adding ΔE and ΔN shifts them to PPP-corrected coordinates.

**Bed Elevation Calculation:** Your rover measured the pole tip position, not the bed. Subtract the pole height to get bed elevation. This calculation provides the critical data for cross-section analysis and discharge calculations. Verify the math—a wrong sign turns a subtraction into an addition and puts your bed above the water surface.

**Geometry Update:** The point features still have their original coordinates. Use the "Update Geometry" tool (or "Translate" tool in Processing Toolbox) to shift them by ΔE, ΔN, ΔZ. Now the point positions and attribute coordinates match and reflect PPP-corrected values.

**Validation Check:** Open the check point layer. Calculate the difference between your three CP measurements (START, NOON, END). If the corrected coordinates show drift ≤3cm, your data is consistent and the PPP correction worked properly. If drift exceeds 3cm, review the calculations for errors in translation values or coordinate system mismatches.

---

## Step 4: Export for PtBox

PtBox software processes the survey data to support velocity analysis and discharge calculations. It expects a simple XYZ format—three columns containing Easting, Northing, and Elevation for each point.

### Create XYZ Point Cloud
- [ ] Select cross-section and control point layers from corrected GeoPackage
- [ ] Right-click layer → Export → Save Features As
- [ ] Format: "Comma Separated Value [CSV]"
- [ ] Geometry: AS_XYZ (exports X,Y,Z coordinates)
- [ ] Layer options: GEOMETRY=AS_XYZ, CREATE_CSVT=NO
- [ ] Save as `site_name_YYYYMMDD_survey.csv` (will contain X,Y,Z columns)
- [ ] Rename to `.xyz` extension if required by PtBox

**Why XYZ Format:** This simple format works with almost all point cloud and photogrammetry software. Three columns: X (Easting), Y (Northing), Z (Elevation). Optional additional columns can contain attributes like point ID or point role. The simplicity makes it robust—no coordinate system confusion, no geometry interpretation issues.

**File Naming:** Include site name and date in the filename. When you have dozens of surveys across multiple sites, this naming convention prevents confusion about which data comes from where and when.

### Archive and Quality Control
- [ ] Save corrected Geopackage as `site_name_YYYYMMDD_corrected.gpkg`
- [ ] Export backup as GeoJSON with CRS metadata
- [ ] Verify coordinate ranges are reasonable for site location
- [ ] Check elevation values match expected riverbed depths
- [ ] Confirm XYZ file format compatible with PtBox import requirements
- [ ] Test import with small subset if possible

**Archive Strategy:** Keep the corrected GeoPackage as your master dataset. It contains all attributes, metadata, and quality control information. The XYZ export is a derivative product optimized for PtBox. If you need to reprocess later or export in different formats, work from the GeoPackage.

**Coordinate Range Check:** Look at the min/max values for Easting, Northing, and Elevation. Do they make sense for your site location? UTM coordinates should be ~200,000-800,000 for Easting and 0-10,000,000 for Northing depending on your zone and hemisphere. Elevations should match your site—river beds near sea level should have elevations near 0-100m, not 5000m or -1000m. Incorrect values indicate coordinate system problems or translation errors.

**Elevation Validation:** Compare your surveyed elevations to expected values from satellite imagery, topographic maps, or previous surveys. A 10m discrepancy means something went seriously wrong—wrong coordinate system, wrong PPP translation, wrong antenna height. A 0.5-1m discrepancy might represent datum differences between your survey and the reference data. Sub-decimeter differences are good agreement.

---

# APPENDICES

## Appendix A: GNSS Master Setup

GNSS Master bridges the gap between your survey-grade rover receiver and consumer Android apps like SW Maps. Android devices expect GPS data in NMEA format through specific channels. The rover outputs UBX binary format through USB. GNSS Master translates between these systems and provides the mock location that overrides Android's internal GPS.

### Android Preparation

**1) Developer Options:**
   - Settings → About Phone → Tap Build Number 7x
   - Settings → Developer Options → Enable USB Debugging
   - Select Mock Location App → GNSS Master

**Why Developer Options:** Android hides advanced settings that most users shouldn't change. Enabling USB Debugging allows apps to communicate with external devices through USB. Mock Location permission lets an app replace the phone's GPS data—normally used for testing GPS apps, but essential for using external receivers.

**2) Permissions:**
   - Settings → Apps → GNSS Master → Permissions
   - Location: Allow all the time
   - Storage, Phone: Allow
   - Battery optimization: Don't optimize

**Location Permission:** GNSS Master needs continuous location access to function. The "Allow all the time" option prevents Android from suspending location services when the app is in the background. Without this, the mock location stops working when you switch to SW Maps.

**Battery Optimization:** Android aggressively limits background apps to save battery. If GNSS Master is optimized, Android will suspend it after a few minutes, killing the GPS feed. Disabling optimization keeps it running continuously throughout your survey session.

### GNSS Master Configuration

**1) Install:** Download from Google Play Store

**2) Connection:** Menu → Receiver → USB

**3) Mock Location:** Menu → Mock Location → Enable

**4) Test:** Verify position appears in Google Maps

**USB Connection:** This tells GNSS Master to expect the receiver on the USB port rather than Bluetooth or internal GPS. The app will look for a USB serial device when you connect the rover.

**Testing:** Open Google Maps and watch the position. If it shows your external receiver location and updates smoothly, the integration works. If it shows your phone's GPS position or doesn't update, the mock location isn't working—check permissions and app configuration.

### USB Connection Setup

1. Connect USB OTG cable to Android
2. Connect to rover F9P USB port
3. Power rover, wait 30 seconds
4. GNSS Master should auto-detect device
5. Verify satellite tracking and RTK status

**USB OTG:** On-The-Go cables let Android devices act as USB hosts rather than only peripherals. Your phone can connect to the rover the same way a computer would. Not all USB cables support OTG—verify you have an OTG cable.

**Auto-Detection:** GNSS Master scans for USB serial devices when you select USB connection mode. If it doesn't find the rover, check cable connections, verify the rover is powered, and confirm USB debugging is enabled on the Android device.

---

## Appendix B: SW Maps Configuration

SW Maps provides field data collection with quality control features, attribute forms, and GIS export capabilities. Proper configuration prevents data quality problems and simplifies post-processing.

### Project Creation

**1) New Project:** `Site_Name_YYYY_MM_DD`

**2) Coordinate System:**
   - Determine your UTM zone EPSG code (see Section 1 instructions)
   - Search for your EPSG code (example: 32748 for UTM 48S)
   - Select: WGS 84 / UTM zone XX[N/S]
   - VERIFY: Correct EPSG code, units = metre

**Project Naming:** Include the date and site name in the project name. When you create multiple projects for the same site, dates prevent confusion about which data is which. This is critical during post-processing when you're working with files copied to a computer weeks after field collection.

**Coordinate System Selection:** The EPSG code is unambiguous—it specifies WGS84 datum, UTM projection, zone number, and hemisphere. Searching by EPSG code prevents selecting wrong zones or similar-sounding systems. Verify the description matches your zone and units show "metre" not "degree". Degrees indicate geographic coordinates, not projected coordinates—a critical mistake.

**Example for Sukabumi, Indonesia:**
- Search: 32748
- Select: WGS 84 / UTM zone 48S
- Verify: EPSG:32748, units = metre

### GPS Settings

- GPS Source: Device internal GPS
- Averaging Method: By Time
- Default times: 60s standard, 120s canal
- Precision thresholds: H=2cm/V=3cm (std), H=4cm/V=6cm (canal)

**Device Internal GPS:** This seems counterintuitive when you're using an external receiver, but GNSS Master feeds the external receiver data through the Android internal GPS interface via mock location. SW Maps reads the "internal GPS" and receives the high-accuracy external data.

**Averaging Method:** Time-based averaging collects positions for a specified duration and averages them. This reduces noise and provides more stable coordinates than single-epoch measurements. Distance-based averaging (collect until the point doesn't move more than X centimeters) works poorly with RTK because the positions are already very stable and the app might never trigger the save.

**Precision Thresholds:** SW Maps can enforce quality gates by refusing to save points that exceed precision thresholds. Set these to match your quality requirements—2cm horizontal, 3cm vertical for standard environments. This prevents accidentally saving poor-quality points when you're not paying attention to the status display.

### Survey Layers

Create these feature layers in your SW Maps project (all should be POINT geometry):

 - **Camera FOV**
 - **Camera Location**
 - **Check Point Location**
 - **Ground Control Points**
 - **Discharge Cross Section**
 - **Level Cross Section**
 - **Water Level**

**Layer Organization:** Separate layers for different point types simplify processing and prevent mistakes. You can apply different symbology, filtering, and export rules to each layer. During post-processing, you load only the layers you need for each analysis step.

**Attribute Configuration:** Each layer needs specific attributes. Ground Control Points should include point_id, measurement_time, PDOP, satellite_count, horizontal_precision, vertical_precision, pole_height, and notes. Cross sections add station_number, water_depth, and bed_type. Define these attributes during project creation so they're ready for field use.

---

## Appendix C: Base Station u-center Config

u-center is u-blox's configuration software for their GNSS receivers. You'll use it to configure the base station for survey-in mode, enable RTCM correction output, and start raw data logging for PPP processing.

### Connection Setup

1. Launch u-center, File → New
2. Receiver → Connection → Select COM port
3. Baud: 38400 or 115200, Connect

**COM Port Selection:** When you plug in the base station, Windows assigns it a COM port number. Device Manager (Windows) or terminal commands (Mac/Linux) show available ports. If multiple USB serial devices are connected, you might need to try each port to find the right one. u-center displays satellite data when connected successfully.

**Baud Rate:** This is the communication speed between computer and receiver. Most u-blox receivers support 38400 baud by default. Some run at 115200 for faster data transfer. Try the default first, then higher speeds if connection fails.

### Survey-In Configuration (TMODE3)

1. View → Configuration → UBX → CFG → TMODE3
2. Mode: Survey-in
3. Minimum time: 1800-3600 seconds (30-60 min)
4. Required accuracy: 0.25 meters
5. Send Configuration

**TMODE3:** This is u-blox's timing mode configuration message. It controls whether the receiver operates as a rover (normal mode), base station (survey-in or fixed mode), or timing reference. Survey-in mode tells the receiver to calculate its position through extended observation and then transmit corrections based on that position.

**Minimum Time:** The receiver must collect data for at least this duration before completing the survey-in. 1800 seconds (30 minutes) provides ~0.5m accuracy. 3600 seconds (60 minutes) improves to ~0.25m. The receiver might finish sooner if it achieves the required accuracy threshold quickly, but usually the time limit is the controlling factor.

**Required Accuracy:** This sets the position uncertainty threshold. The receiver monitors how much its calculated position varies. When the variation stays within this threshold for the specified duration, the survey-in completes. 0.25 meters is appropriate for RTK base stations—good enough for corrections while not requiring excessive observation time.

### RTCM3 Output (if not using a pre-configured base and rover)

1. UBX → CFG → PRT → UART2 → Protocol out: RTCM3
2. UBX → CFG → MSG → Enable RTCM messages:
   - 1005 (Station ARP): Rate 10
   - 1077 (GPS MSM7): Rate 1
   - 1087 (GLONASS MSM7): Rate 1
   - 1097 (Galileo MSM7): Rate 1

**RTCM3 Protocol:** Real-Time Correction Messages version 3 is the standard format for transmitting differential GNSS corrections from base to rover. The base sends messages describing its position, satellite observations, and calculated corrections. The rover receives these messages and applies them to its own observations.

**UART2:** This is a serial port on the receiver that can connect to a radio, cellular modem, or other communication device. By configuring UART2 to output RTCM3, the base automatically transmits corrections through whatever communication device you've connected.

**Message Types:** Message 1005 describes the base station position (the anchor reference point). GPS, GLONASS, and Galileo MSM7 messages contain full precision multi-signal carrier phase and pseudorange observations for each satellite system. The rover needs all these message types to achieve RTK FIX solution.

**Message Rates:** 1005 transmits every 10 seconds—the base position doesn't change, so infrequent updates are adequate. Observation messages (1077, 1087, 1097) transmit every second (Rate 1) to provide continuous corrections as satellites move and signals change.

### Raw Data Logging

1. UBX → CFG → MSG → Enable on USB:
   - UBX-RXM-RAWX: Rate 1
   - UBX-RXM-SFRBX: Rate 1
   - UBX-NAV-PVT: Rate 1
2. File → Database Logging → Start (UBX format)

**RXM-RAWX:** This message contains raw carrier phase and pseudorange measurements for each satellite. PPP processing needs these raw observations to calculate precise positions. Without RAWX, you only have processed positions, which aren't adequate for PPP.

**RXM-SFRBX:** Subframe buffer messages contain the navigation data broadcast by satellites—ephemeris (orbital parameters) and almanac (constellation status). PPP services need this data to determine satellite positions accurately.

**NAV-PVT:** Position Velocity Time messages contain the receiver's calculated position, velocity, and time. While not strictly necessary for PPP, these messages help verify the receiver is working correctly and provide context for the raw observations.

**UBX Format:** Save in u-blox binary format rather than NMEA text format. UBX contains more information and higher precision than NMEA. You'll convert UBX to RINEX later for PPP processing.

---

## Appendix D: Sample Video Collection

The sample video serves two purposes. First, it documents the flow conditions and visible features during your survey. Second, it provides the reference frame for identifying ground control points within the camera view.

### Connect to PtBox

 - Put the PtBox in Maintenance Mode using the FTP service
 - Wait for the PtBox to come online again, and log in
 - Select "Aim the camera in the field"
 - Take a 5 second video and note the video name and timestamp
 - Ensure that all control points are visible in the video. Adjust if needed and take a new video.
 - Also take a photo, and use the photo to number the control points so that you have a reference to use when entering the control points into the PtBox software later.
 - **NOTE:** Do not try to start the cameras in this view. This PtBox has a bad camera, and attempting to start the bad camera will cause the PtBox to lock up.

**Video Duration:** Five seconds provides enough frames to identify features clearly without consuming excessive storage. If flow conditions are highly variable (turbulent flow, changing light), consider 10-15 seconds to capture representative conditions.

**GCP Visibility:** Every ground control point you survey must be visible in the video. If a GCP is outside the camera field of view or occluded by vegetation or terrain, it cannot be used for photogrammetric processing. Check visibility before finalizing GCP locations.

**Photo for Numbering:** Take a still photo and annotate it with GCP numbers. This reference prevents mixing up control points during processing. Print the photo or keep it open on a screen while entering GCP coordinates in PtBox—visual confirmation prevents data entry errors.

---

## Appendix E: Troubleshooting

### Common Issues and Solutions



### No RTK FIX

- Check base survey-in completed
- Verify radio link, RTCM messages
- Wait longer (up to 20 minutes)
- Move to better sky view

**Survey-In Completion:** The base must finish its survey-in process before transmitting corrections. Check the base station display or u-center to confirm TMODE3 shows "Survey-in completed" or "Fixed" status. If the survey-in is still running, you'll receive corrections but they're based on an incomplete position calculation.

**Radio Link:** Verify the rover receives corrections. Most rover receivers display correction age and source. If correction age exceeds 60 seconds, the link is broken or intermittent. Check radio power, antenna connections, and distance between base and rover. Radio range varies with terrain, vegetation, and frequency—typical range is 1-5 km for low-power radios, 10-30 km for higher-power systems.

**Initialization Time:** RTK solutions require resolving integer ambiguities in the carrier phase measurements. This process can take seconds in ideal conditions or minutes in challenging conditions. Be patient. If FIX doesn't occur within 20 minutes, something is wrong—poor satellite geometry, weak signal quality, incorrect configuration, or excessive baseline distance.

**Sky View:** Trees, buildings, and terrain block satellites and cause multipath. Move to a location with open sky down to 15° above all horizons. Even partial obstructions can prevent FIX solution.

### Poor Precision

- Check satellite count, PDOP
- Move away from reflective surfaces
- Use bipod for stability
- Extend averaging time

**Satellite Count:** Fewer than 8 satellites provides weak geometry. Enable all constellations (GPS + GLONASS + Galileo + BeiDou) to maximize satellite visibility. Check receiver configuration to confirm multi-constellation mode is active.

**Reflective Surfaces:** Water, metal roofs, vehicles, and smooth ground can reflect signals. The receiver sees both the direct signal and the delayed reflected signal, confusing the position calculation. Move 5-10 meters away from reflective surfaces.

**Pole Stability:** Hand-holding a 2m pole introduces centimeter-level position variations from hand shake and wind. A bipod or fixed mount eliminates these variations. If you must hand-hold, brace the pole against your body and take shallow breaths during measurement.

**Averaging Time:** Extended averaging (120s instead of 60s) helps in marginal conditions by averaging over more satellite geometry variations and atmospheric fluctuations. This can't fix systematic problems like multipath or poor PDOP, but it reduces random noise.

### USB Connection Issues

- Check USB OTG cable
- Power cycle rover and Android
- Verify USB debugging enabled
- Try different USB port

**Cable Quality:** USB cables have four wires—power, ground, and two data lines. Cheap cables sometimes omit the data lines (they only charge devices). Verify your cable supports data transfer by testing it with file transfer between devices.

**Power Cycling:** Connection issues often resolve with a complete power cycle. Turn off the rover, disconnect USB, close GNSS Master, wait 30 seconds, then reconnect and restart in sequence: rover power on, wait 30 seconds, connect USB, launch GNSS Master.

**USB Debugging:** Android blocks USB communication unless debugging is enabled. Check Settings → Developer Options → USB Debugging. If this keeps disabling itself, check for security software that restricts debugging.

**Port Selection:** Some Android devices have multiple USB modes (charging only, file transfer, MIDI, etc.). When you connect the rover, a notification appears asking which mode to use. Select "File transfer" or "USB tethering" mode to enable full communication.

### Base Station Problems

- Check power, antenna connections
- Verify survey-in status in u-center
- Monitor RTCM output
- Restart if necessary

**Power Issues:** Verify the base station is receiving power—LEDs should be illuminated or flashing. Check battery voltage if using battery power. F9P receivers draw ~1W typically, more during initialization. A depleted battery might power the receiver but not at full capability.

**Antenna Connection:** Ensure the antenna cable is firmly connected at both ends. A loose connection degrades signal quality dramatically—the receiver might still track satellites but with poor signal strength and high noise.

**Survey-In Status:** Connect u-center to the base and check View → Messages View → NAV → SVIN (Survey-In). This shows the current survey-in status: duration elapsed, position variation, and whether survey-in completed. If variation isn't converging, satellite geometry is poor—wait longer or restart at a different time of day.

**RTCM Output:** Use u-center's Messages View to monitor RTCM messages on UART2. You should see 1005 messages every 10 seconds and 1077/1087/1097 messages every second. If messages aren't transmitting, check the PRT and MSG configuration.

---

## Appendix F: AUSPOS Submission

AUSPOS is the recommended processing service for Indonesia and Asia-Pacific surveys. It uses network-based processing with APREF regional reference stations.

### Submission Process

1. **Navigate to AUSPOS:** https://www.ga.gov.au/auspos

2. **Prepare your RINEX file:**
   - Convert UBX to RINEX using CONVBIN (see Step 1)
   - Locate the .obs file (RINEX observation data)
   - File should be 6-12 hours of base station observations

3. **Upload and Configure:**
   - Click "Choose File" and select your .obs file
   - Enter your email address (results sent here)
   - **Antenna Type:** Select from dropdown:
     - TRM29659.00 (recommended for ArduSimple multiband)
     - SEPCHOKE_MC (Septentrio multiband alternative)
     - "Unknown" if no good match available
   - **Antenna Height:** Enter height in meters (ground mark to antenna ARP)
   - **Processing Mode:** Static (default)

4. **Submit:**
   - Review information for accuracy
   - Click "Submit" button
   - Save confirmation number for tracking

5. **Receive Results:**
   - Typical processing time: 1-4 hours
   - Email notification when complete
   - Download results report (PDF with coordinates)

### Understanding AUSPOS Results

**Results Format:**
- Coordinates in WGS84 geographic (latitude, longitude, height)
- Quality indicators (RMS, standard deviations)
- Processing details (reference stations used, observation statistics)

**Extract Coordinates:**
- Note latitude, longitude, ellipsoidal height
- Convert to UTM using coordinate converter or QGIS
- Use these as your corrected base coordinates
- Calculate translation from survey-in coordinates

**Quality Indicators:**
- Horizontal RMS <5cm: Excellent
- Horizontal RMS 5-10cm: Good
- Horizontal RMS >10cm: Review for issues (short session, poor satellite geometry)

---

## Appendix G: CSRS-PPP Submission

CSRS-PPP provides true PPP with Ambiguity Resolution (PPP-AR), offering fastest convergence and multi-GNSS processing. Best for shorter sessions or when AUSPOS unavailable.

### Submission Process

1. **Navigate to CSRS-PPP:** https://webapp.csrs-scrs.nrcan-rncan.gc.ca/geod/tools-outils/ppp.php

2. **Prepare your RINEX file:**
   - Same .obs file used for AUSPOS
   - Can also submit compressed (.zip, .gz)
   - Multi-GNSS data (GPS+GLONASS+Galileo) will be processed

3. **Upload and Configure:**
   - Click "Browse" to select RINEX file
   - Enter email address
   - **Processing Mode:** Static
   - **Product Type:** Select based on needs:
     - **Final products:** Best accuracy (12-48 hour delay), recommended for most surveys
     - **Rapid products:** Good accuracy (2-8 hour delay), faster turnaround
     - **Ultra-rapid products:** Quick results (30 min delay), GPS+GLONASS only
   - **Antenna Type:** Select from list or use "Unknown"
   - **Antenna Height:** Enter in meters
   - **PPP-AR:** Enabled by default (recommended for Galileo data after Nov 2022)

4. **Advanced Options (Optional):**
   - Coordinate system: WGS84 (default), NAD83, ITRF
   - Can select specific output formats

5. **Submit:**
   - Review settings
   - Click "Submit" button
   - Note job ID for tracking

6. **Receive Results:**
   - Processing time: 2-8 hours (rapid), up to 48 hours (final)
   - Email with download link
   - Multiple format options (PDF, TXT, XML)

### Understanding CSRS-PPP Results

**Results Format:**
- Coordinates in selected reference frame (WGS84, NAD83, or ITRF)
- Quality estimates (formal errors, RMS)
- Ambiguity resolution status (fixed/float for each epoch)
- Multi-GNSS processing statistics

**PPP-AR Advantage:**
- Ambiguity resolution achieves sub-centimeter accuracy faster
- Look for "Fixed" ambiguity status in results
- Fixed ambiguities = better accuracy than float solution

**Multi-GNSS Benefit:**
- Results show which constellations were processed
- GPS+GLONASS+Galileo typically achieves 30-40% faster convergence
- More satellites = better geometry = better accuracy

---

## Appendix H: GAPS Submission

GAPS provides true PPP with well-documented algorithms, ideal for cross-validation and academic applications.

### Submission Process

1. **Navigate to GAPS:** https://gaps.gge.unb.ca

2. **Create Account (Optional but Recommended):**
   - Free registration
   - Allows tracking multiple submissions
   - Saves antenna preferences

3. **Prepare your RINEX file:**
   - Same .obs file used for other services
   - Accepts RINEX 2.x or 3.x
   - Multi-GNSS supported

4. **Upload and Configure:**
   - Select "Submit Data" from main menu
   - Upload .obs file
   - Enter email address
   - **Processing Mode:**
     - Static (for base station surveys)
     - Kinematic (for moving surveys - advanced)
   - **Antenna:**
     - Search database for your antenna model
     - Or enter "Generic" for unknown models
   - **Antenna Height:** Enter in meters
   - **GNSS Constellation Selection:**
     - GPS only
     - GPS + GLONASS
     - GPS + GLONASS + Galileo (recommended)

5. **Advanced Options:**
   - Elevation mask (default 10°)
   - Tropospheric modeling options
   - Ionospheric correction methods
   - Can leave defaults for standard processing

6. **Submit:**
   - Review parameters
   - Click "Process" button
   - Save submission confirmation

7. **Receive Results:**
   - Processing time: 2-6 hours typical
   - Email notification with results
   - Can also log in to view processing status

### Understanding GAPS Results

**Results Format:**
- Coordinates in ITRF (International Terrestrial Reference Frame)
- Can be transformed to WGS84 (nearly identical for most purposes)
- Position time series (shows convergence over session)
- Quality statistics and residuals

**Algorithm Transparency:**
- GAPS provides detailed processing reports
- Shows which satellites were used
- Explains which corrections were applied
- Good for understanding PPP methodology

**Cross-Validation:**
- Compare GAPS results with AUSPOS results
- Differences should be <2-3cm if both processed correctly
- Large differences (>5cm) indicate potential issues to investigate

---

**Document Version:** 2025-11-24
**Author:** Tom Jordan / OpenRiverCam Project
**Purpose:** Field procedure documentation with explanatory context for non-expert users
**Supersedes:** SURVEY_PROCESS.md (technical reference—both documents remain valid for different audiences)
