# Surveying Concepts for River Monitoring: A Plain-Language Guide

This guide explains essential surveying concepts for river monitoring applications. The focus is on helping you understand not just what these terms mean, but why they matter for accurate river flow measurements.

## Table of Contents
1. [RTK (Real-Time Kinematic) Positioning](#rtk-real-time-kinematic-positioning)
2. [PPP (Precise Point Positioning)](#ppp-precise-point-positioning)
3. [Base Station and Rover Setup](#base-station-and-rover-setup)
4. [RINEX Format](#rinex-format-and-why-we-convert-to-it)
5. [Survey-In Process](#survey-in-process)
6. [Check Points](#check-points-and-quality-control)
7. [PDOP, Precision Metrics, and Satellite Counts](#pdop-precision-metrics-and-satellite-counts)

---

## RTK (Real-Time Kinematic) Positioning

### What It Is

RTK is a GPS/GNSS positioning technique that provides centimeter-level accuracy (typically 1-2 cm) in real-time. Think of it as GPS on steroids - instead of the several-meter accuracy you get from your phone, RTK gives you survey-grade precision immediately.

### Why It Matters for River Monitoring

When you're measuring river flow using video analysis (photogrammetry), you need to know the exact positions of ground control points along the riverbank. Even small positioning errors get magnified when you're:
- Converting pixel coordinates to real-world distances
- Calculating water surface velocities from video
- Computing discharge (flow rate) from those velocities

A positioning error of just a few centimeters can translate to velocity errors of several centimeters per second, which compounds into significant discharge calculation errors. For river monitoring applications, research shows that GCP-based georeferencing can reduce velocity measurement uncertainty by up to 5 times compared to less precise methods.

### How It Works

RTK achieves this precision through a clever comparison process:

1. **Two Receivers Working Together**: You have a base station (stationary, at a known location) and a rover (mobile, measuring unknown points).

2. **Error Detection**: The base station knows exactly where it is. It receives signals from GPS/GNSS satellites and compares the calculated position with its true known position. The difference represents the errors affecting the satellite signals.

3. **Real-Time Corrections**: The base station broadcasts these error corrections via radio, cellular, or internet to the rover in real-time.

4. **Carrier Phase Measurement**: RTK uses the carrier phase of the GPS signal (the actual radio wave) rather than just the encoded timing information. This is like measuring the exact position of ripples on a wave rather than just when the wave arrives - much more precise.

5. **Common Error Elimination**: Because both base and rover are close together (typically within 10-20 km) and receiving signals from the same satellites at nearly the same time, they experience similar atmospheric delays and other errors. These common errors cancel out when the corrections are applied.

**The Result**: The rover achieves centimeter-level accuracy, typically 1-2 cm horizontal and 2-3 cm vertical.

### Key Limitations

- **Range Limited**: Works best within 10-20 km of the base station
- **Requires Communication**: Base and rover must maintain constant data link
- **Initialization Time**: Takes seconds to minutes to achieve fixed solution
- **Infrastructure Cost**: Requires setting up and maintaining a base station

---

## PPP (Precise Point Positioning)

### What It Is

PPP is an alternative positioning technique that also achieves centimeter-level accuracy but works fundamentally differently from RTK. Instead of using a local base station, PPP uses precise satellite orbit and clock correction data from global networks.

### How It Differs From RTK

| Aspect | RTK | PPP |
|--------|-----|-----|
| **Base Station** | Required locally (within 10-20 km) | Not needed |
| **Coverage** | Regional/local | Global (works anywhere) |
| **Initialization** | Fast (seconds to minutes) | Slow (20-40 minutes) |
| **Accuracy** | 1-2 cm (optimal) | 2-5 cm (after convergence) |
| **Data Link** | Required in real-time | Can be post-processed |
| **Cost** | Higher (base station equipment) | Lower (subscription service) |
| **Best For** | Local projects, real-time needs | Remote locations, post-processing |

### Why We Use It for River Monitoring

PPP is particularly valuable for river monitoring in several scenarios:

1. **Remote Locations**: Many rivers are far from established base stations or survey infrastructure. PPP works anywhere with a clear view of the sky.

2. **Permanent Base Stations**: When establishing a fixed base station for long-term monitoring, PPP provides the most accurate way to determine the base station's position. You can collect data for 24 hours and post-process it to get the true position within a few centimeters globally.

3. **Cost-Effectiveness**: For isolated monitoring sites, PPP eliminates the need for expensive base station equipment and infrastructure.

4. **Post-Processing Flexibility**: You can collect raw GNSS data in the field and process it later using online PPP services (like Natural Resources Canada's CSRS-PPP or NOAA's OPUS), which is ideal for research applications where real-time results aren't critical.

### The Trade-Off

The main drawback of PPP is convergence time - you typically need to collect data for 20-40 minutes (or longer for higher accuracy) while the receiver's calculations "converge" to the precise position. For a permanent base station setup, you might collect 24 hours of data and post-process it to achieve the best accuracy.

---

## Base Station and Rover Setup

### The Concept

The base-rover setup is the foundation of differential GNSS positioning (including RTK). Think of it as having a referee (base) with a known position watching a game and calling out corrections to the players (rovers) in real-time.

**Base Station**: A GNSS receiver placed at a precisely known, fixed location. It remains stationary during surveying operations.

**Rover**: A mobile GNSS receiver that you carry to the points you want to measure (like ground control points along a riverbank).

### Why This Approach Is Used

The base-rover setup solves a fundamental problem: GPS/GNSS signals are affected by errors as they travel from satellites to your receiver.

#### Major Error Sources:

1. **Ionospheric Delays**: Free electrons in the upper atmosphere refract (bend) satellite signals, causing delays up to 20 meters depending on solar activity and time of day.

2. **Tropospheric Delays**: The neutral atmosphere (the air we breathe) also refracts signals, contributing 2-20 meters of error depending on weather conditions and satellite elevation angle.

3. **Satellite Clock and Orbit Errors**: Even tiny inaccuracies in satellite clocks or orbit predictions accumulate into positioning errors.

4. **Multipath**: Signal reflections from nearby surfaces (buildings, water, terrain) can create false readings.

#### How Base-Rover Eliminates These Errors:

The brilliant insight is this: **if two receivers are close together, they experience nearly identical atmospheric conditions and receive signals from the same satellites through essentially the same atmosphere**.

1. The base station knows its exact position (surveyed or PPP-determined)
2. It calculates what position the satellite signals indicate
3. The difference between true position and calculated position = the errors
4. These errors are broadcast to the rover
5. The rover applies the inverse corrections to its measurements
6. Common errors (atmospheric delays, satellite clock issues) cancel out

### Practical Implications for River Monitoring

When setting up for river monitoring:

1. **Base Placement**: Your base should be on stable ground with a clear view of the sky, within 10-20 km of your monitoring site. Closer is better - errors increase with distance.

2. **Base Position Accuracy**: The rover's accuracy depends on knowing the base position precisely. Use PPP or a surveyed monument to establish the base position.

3. **Continuous Operation**: The base must run continuously during all rover measurements to provide corrections.

4. **Data Link**: Maintain a reliable connection between base and rover (radio for short distances, cellular/internet for longer ranges).

For permanent monitoring installations, you might set up a base station that runs 24/7, providing continuous corrections to your camera system's position or to rovers used for ground control measurements.

---

## RINEX Format and Why We Convert To It

### What RINEX Is

RINEX (Receiver Independent Exchange Format) is a standardized text file format for raw GNSS data. It's the "universal translator" of the GNSS world.

### The Problem RINEX Solves

Every GNSS receiver manufacturer (Trimble, Leica, Emlid, u-blox, etc.) stores raw satellite data in their own proprietary binary format. These formats are:
- **Incompatible** between brands
- **Optimized** for each manufacturer's own processing software
- **Binary** (not human-readable)
- **Designed** to lock users into specific software ecosystems

This creates a major problem: You can't easily share data between different systems or use specialized processing software that doesn't support every proprietary format.

### How RINEX Helps

RINEX was developed in 1989 during the European GPS campaign EUREF 89, which involved over 60 GPS receivers from 4 different manufacturers. Researchers needed a way to combine and process all this data together.

RINEX provides:

1. **Universal Compatibility**: Almost all GNSS processing software can read RINEX files
2. **Data Sharing**: Researchers and organizations can exchange data regardless of equipment brand
3. **Format Stability**: RINEX has well-documented versions (currently RINEX 3.x) that maintain backward compatibility
4. **Human Readability**: Text-based format that can be inspected and verified
5. **Long-term Archival**: Standardized format less likely to become obsolete than proprietary formats

### Why We Convert to RINEX for River Monitoring

For post-processing PPP workflows:

1. **Online PPP Services**: Services like CSRS-PPP (Canada) and OPUS (USA) require RINEX format input files.

2. **Post-Processing Software**: Programs like RTKLIB, which can compute precise positions from raw data, work best with RINEX.

3. **Data Verification**: You can use RINEX files to verify your base station position or rover measurements using different processing software for cross-checking.

4. **Archival**: Storing data in RINEX format ensures you can reprocess it years later as algorithms improve, regardless of whether your original receiver brand is still supported.

### Important Notes

- **Use Manufacturer Tools**: Always use the official conversion software from your receiver manufacturer when possible - they understand their data format best.
- **Preserve Raw Data**: Keep the original binary files as a backup, since some conversion processes can reduce data quality or lose information.
- **RINEX Version**: Use RINEX 3.x when possible, as it supports modern multi-GNSS constellations (GPS, GLONASS, Galileo, BeiDou) better than older RINEX 2.x.

---

## Survey-In Process

### What's Happening During Survey-In

The "survey-in" process is a method to establish your base station's position using the GNSS receiver itself, without knowing the coordinates in advance. The base station collects position measurements over time and averages them to determine its location.

Think of it like this: Each individual GPS measurement might be off by several meters due to atmospheric conditions and other errors. But if you take hundreds or thousands of measurements over time, the errors tend to cancel out as conditions change - sometimes the error pushes you north, sometimes south, sometimes east, west, up, or down. The average of all these measurements approaches the true position.

### The Technical Process

During survey-in, the receiver:

1. **Collects Position Fixes**: Continuously calculates its position from satellite signals
2. **Monitors Variation**: Tracks how much the calculated positions vary
3. **Calculates Average**: Computes a running average of all position fixes
4. **Checks Convergence**: Monitors whether positions stay within a specified radius (e.g., 2-5 meters)
5. **Declares Complete**: Marks the survey complete when positions remain within the target accuracy for the specified duration

### Survey-In Parameters

Most receivers let you set two parameters:

- **Minimum Time**: How long to collect data (e.g., 60 seconds to 24 hours)
- **Accuracy Threshold**: Maximum position variation allowed (e.g., positions must stay within 3 meters)

The survey is complete when BOTH conditions are met.

### Duration vs. Accuracy

| Survey Duration | Expected Accuracy | Best Use Case |
|----------------|-------------------|---------------|
| 60 seconds | 2-5 meters | Quick relative positioning, temporary setups |
| 5-10 minutes | 1-3 meters | Field surveys where relative accuracy matters more than absolute |
| 1 hour | 0.5-1 meter | Semi-permanent installations |
| 24 hours + PPP | 2-5 cm | Permanent base stations, highest accuracy |

### Why It Takes Time

The accuracy improves with time because:

1. **Satellite Geometry Changes**: As satellites move across the sky, you get measurements from different angles and configurations, which helps average out geometric dilution errors.

2. **Atmospheric Variations Average Out**: The ionosphere and troposphere fluctuate. Longer observations capture these variations, allowing them to cancel out in the average.

3. **Multipath Effects Vary**: Signal reflections change as satellite positions change, so longer observations reduce multipath impact.

4. **Statistical Confidence**: More measurements = smaller standard error = higher confidence in the final position.

### Survey-In vs. PPP

While survey-in is convenient, it has limitations:

- **Accuracy**: Survey-in typically achieves 1-5 meter accuracy, while PPP achieves centimeter-level
- **Absolute Position**: Survey-in gives you an averaged position but doesn't correct for systematic biases in the satellite system
- **Best Practice**: For permanent base stations, use survey-in to get a rough position initially, then run 24 hours of data collection and post-process with PPP to get the true position

### Practical Recommendations for River Monitoring

1. **Quick Field Setup**: If you're setting up a temporary base for a day of field measurements, a 5-10 minute survey-in is adequate. The relative accuracy between base and rover is what matters most.

2. **Permanent Installation**: For a fixed monitoring station, invest time in a proper PPP solution:
   - Do a quick survey-in to start collecting data
   - Run for 24 hours continuously
   - Convert to RINEX format
   - Process with online PPP service
   - Update base station with the precise coordinates

3. **Known Point**: If you have access to a surveyed benchmark or geodetic control point, set up your base directly on it and enter the known coordinates - this is always better than survey-in.

---

## Check Points and Quality Control

### What Check Points Are

Check points (also called checkpoints or independent check points) are precisely surveyed locations that are NOT used in processing your photogrammetric or surveying data. Instead, they're held back to verify the accuracy of your final results.

Think of check points like an answer key for a test - you solve the problem without looking at the answer, then check your solution against the answer key to see how well you did.

### Check Points vs. Ground Control Points (GCPs)

This is a crucial distinction:

| Ground Control Points (GCPs) | Check Points |
|------------------------------|--------------|
| **Used** during processing | **Not used** during processing |
| Help align and scale the model | Verify the model's accuracy |
| "Teach" the model where it is | "Test" how well the model learned |
| Minimum 3-5 needed | 1-3 per project recommended |
| Distributed throughout site | Distributed but kept separate |

### Why Check Points Matter

Without check points, you're operating blind. Here's why:

1. **Independent Validation**: GCPs can hide problems. If your GCPs have measurement errors or if your model overfits to them, everything might look perfect internally but be wrong in absolute terms. Check points provide independent validation.

2. **Quantify Real-World Accuracy**: Check points let you calculate actual RMSE (Root Mean Square Error) values - this tells you how accurate your measurements really are:
   - Excellent: < 5 cm RMSE
   - Good: 5-10 cm RMSE
   - Acceptable: 10-20 cm RMSE
   - Poor: > 20 cm RMSE

3. **Catch Systematic Errors**: Check points can reveal systematic problems like:
   - Base station position errors
   - Coordinate system transformation issues
   - Camera calibration problems
   - Atmospheric or multipath effects not corrected by RTK

4. **Professional Standards**: Survey-grade work requires independent verification. Check points demonstrate due diligence and provide documented accuracy metrics.

### Specific Importance for River Velocity Measurements

For river monitoring using video photogrammetry:

**Error Propagation**: Position errors in GCPs propagate through the transformation equations and affect velocity calculations. Research shows that GCP positional uncertainty directly impacts flow velocity measurements:
- A 5 cm GCP error can translate to velocity errors of 5-10 cm/s
- Velocity errors compound into discharge errors of 10-20%
- Check points reveal whether your GCP accuracy is adequate for your required discharge precision

**Oblique Camera Views**: River cameras often have oblique viewing angles to see the water surface. These viewing geometries are more sensitive to GCP errors. Research indicates that uncertainty from direct georeferencing can be five times larger than GCP-based approaches for oblique views, making check point validation even more critical.

**Temporal Verification**: For long-term monitoring, you can revisit check points periodically to verify that your system hasn't drifted or that base station positions remain accurate.

### How to Use Check Points Effectively

1. **Select Representative Locations**:
   - Distribute check points across your site
   - Include different elevations if terrain varies
   - Place some near the area of interest (the river) and some farther away
   - Aim for at least 1 check point per 5 GCPs used

2. **Survey to the Same Accuracy as GCPs**:
   - Use the same RTK/PPP methods
   - Apply the same care in setup and measurement
   - Occupy check points for the same duration as GCPs
   - Document check point coordinates separately

3. **Mark Them Clearly**:
   - Use distinct markers so you don't accidentally use them as GCPs
   - Photograph them from multiple angles
   - Record their locations in field notes
   - Consider using different colored targets (e.g., orange for GCPs, blue for check points)

4. **Calculate and Report Metrics**:
   After processing, measure the difference between your model's prediction and the true check point coordinates:

   ```
   Error_X = Predicted_X - True_X
   Error_Y = Predicted_Y - True_Y
   Error_Z = Predicted_Z - True_Z

   Horizontal_Error = sqrt(Error_X² + Error_Y²)
   Vertical_Error = abs(Error_Z)

   RMSE_Horizontal = sqrt(mean(Horizontal_Error²))
   RMSE_Vertical = sqrt(mean(Vertical_Error²))
   ```

5. **Acceptable Thresholds**:
   - If check point errors are similar to GCP residuals: your model is generalizing well
   - If check point errors are significantly larger: investigate potential issues
   - For river monitoring, aim for check point RMSE < 5 cm to minimize velocity measurement uncertainty

### Best Practices for River Monitoring Projects

- **Minimum Setup**: At least 4 GCPs + 1 check point
- **Better Setup**: 6-8 GCPs + 2 check points
- **Optimal Setup**: 10-15 GCPs + 3-4 check points

**GCP Distribution**: Place GCPs around the perimeter of your camera view, with some along the riverbanks at varying distances from the camera.

**Check Point Distribution**: Place check points in the middle of your site and at varying distances from the camera, ensuring they cover the river section where you're measuring velocities.

---

## PDOP, Precision Metrics, and Satellite Counts

### Understanding PDOP (Position Dilution of Precision)

PDOP is a number that tells you how good the satellite geometry is at any given moment. Think of it as a "quality score" for your position measurement based on where the satellites are in the sky.

**The Key Concept**: It's not just about how many satellites you can see, but WHERE they are in the sky relative to each other.

#### The Triangle Analogy

Imagine you're trying to figure out where you are using triangulation from three lighthouses:

- **Good Geometry (Low PDOP)**: The three lighthouses are spread far apart - one north, one south, one west. Their bearing lines cross at sharp angles. You can pinpoint your position precisely.

- **Poor Geometry (High PDOP)**: All three lighthouses are in nearly the same direction from you. Their bearing lines cross at very shallow angles. Small measurement errors create large uncertainty areas.

GPS/GNSS works the same way. Satellites spread across the sky (high above, low on horizons, north, south, east, west) give strong geometry and low PDOP. Satellites bunched in one part of the sky give weak geometry and high PDOP.

### PDOP Values and What They Mean

| PDOP Value | Rating | Meaning | Action |
|------------|--------|---------|--------|
| 1-2 | Excellent | Ideal satellite geometry | Perfect conditions |
| 2-3 | Good | Strong geometry, minimal error | Acceptable for all surveying |
| 3-4 | Acceptable | Adequate geometry | Fine for most work |
| 4-6 | Fair | Degraded geometry | Consider waiting for better conditions |
| 6-8 | Poor | Weak geometry | Avoid if possible |
| >8 | Very Poor | Very weak geometry | Do not use these measurements |

**Rule of Thumb**: For RTK surveying and river monitoring GCPs, target PDOP < 4, preferably < 3.

### Why PDOP Matters for River Monitoring

PDOP directly affects your measurement accuracy:

1. **Position Error Amplification**: Your receiver has an inherent measurement precision (say, 1 cm). PDOP multiplies this base error:
   ```
   Actual Position Error ≈ Receiver Precision × PDOP

   Example:
   - Receiver precision: 1 cm
   - PDOP = 2: Actual error ≈ 2 cm (good)
   - PDOP = 6: Actual error ≈ 6 cm (poor)
   ```

2. **GCP Quality**: When measuring ground control points with PDOP > 4, you're introducing unnecessary error into your photogrammetric model, which propagates to velocity measurements.

3. **Consistency**: PDOP varies throughout the day as satellites move. If you measure some GCPs at PDOP 2 and others at PDOP 6, you have inconsistent quality.

### Satellite Count: Why More Is Better

The number of satellites visible affects both PDOP and positioning reliability.

#### Minimum Requirements

- **4 satellites**: Minimum for 3D position (latitude, longitude, altitude) plus time
- **5 satellites**: Minimum for RTK positioning with quality checking
- **8+ satellites**: Recommended for reliable RTK surveying

#### Why More Satellites Improve Accuracy

1. **Better Geometry**: More satellites means better odds of having them well-distributed across the sky, lowering PDOP.

2. **Redundancy**: With 12 satellites visible instead of 5, the receiver can:
   - Detect and reject bad measurements (multipath, signal interference)
   - Maintain position even if some satellites are temporarily blocked
   - Use satellite selection algorithms to pick the best geometric configuration

3. **Multi-Constellation Benefits**: Modern receivers track multiple satellite systems simultaneously:
   - GPS (USA): ~30 satellites
   - GLONASS (Russia): ~24 satellites
   - Galileo (Europe): ~30 satellites
   - BeiDou (China): ~35 satellites

   Using all four systems, you might see 20-30 satellites at once instead of 6-8, dramatically improving PDOP and reliability.

4. **Obstruction Resilience**: In challenging environments (trees, buildings, terrain), more satellites mean you're more likely to maintain adequate coverage.

### Other Related Precision Metrics

#### HDOP (Horizontal Dilution of Precision)

- Focuses only on horizontal (X, Y / latitude, longitude) accuracy
- Usually lower than PDOP since it ignores vertical component
- Critical for river monitoring since velocity measurements are primarily horizontal
- Target: HDOP < 2 for high-quality GCPs

#### VDOP (Vertical Dilution of Precision)

- Focuses only on vertical (Z / altitude) accuracy
- Usually worse than HDOP (vertical geometry is always weaker)
- Less critical for river monitoring unless you need accurate water surface elevations
- Target: VDOP < 4 for most applications

#### Fix Quality / Solution Type

Your RTK receiver reports different solution types:

| Solution Type | Accuracy | Reliability | Meaning |
|---------------|----------|-------------|---------|
| **RTK Fixed** | 1-2 cm | High | Integer ambiguities resolved, best accuracy |
| **RTK Float** | 10-50 cm | Medium | Ambiguities not resolved, uncertain |
| **DGPS** | 0.5-2 m | Medium | Differential corrections applied, no RTK |
| **Autonomous** | 2-10 m | Low | No corrections, standard GPS |
| **No Fix** | N/A | None | Insufficient satellites or poor geometry |

**For ground control measurements, ONLY use RTK Fixed solutions.**

### Practical Monitoring Guidelines

When measuring GCPs or check points for river monitoring:

1. **Check PDOP Before Measuring**:
   - Wait for PDOP < 3 if possible
   - Never measure with PDOP > 6
   - Most receivers display PDOP in real-time

2. **Verify Satellite Count**:
   - Ensure 8+ satellites visible
   - Enable all available constellations (GPS+GLONASS+Galileo+BeiDou)
   - Check for satellite health warnings

3. **Confirm RTK Fixed Solution**:
   - Wait for "Fixed" status before recording
   - If stuck in "Float," check base station connection and PDOP
   - Never use Float solutions for GCPs

4. **Occupation Time**:
   - Even with good PDOP and Fixed solution, occupy each point for 30-60 seconds
   - Record multiple epochs and average them
   - This helps average out multipath and remaining errors

5. **Time of Day Considerations**:
   - Satellite geometry changes throughout the day
   - Plan field sessions during times with better satellite coverage
   - Early morning or late afternoon often have good geometry
   - Check satellite planning tools or your receiver's skyplot

6. **Obstruction Management**:
   - Clear view of sky is critical (avoid trees, buildings, terrain)
   - If you must work near obstructions, enable multi-constellation mode
   - Use a skyplot to identify obstructions and plan accordingly

### Example Field Workflow

Here's a practical checklist for measuring river monitoring GCPs:

```
Before measuring each point:
[ ] Power on rover, ensure base connection
[ ] Position antenna over mark precisely
[ ] Check receiver display:
    - Solution type: RTK Fixed
    - Satellite count: ≥ 8
    - PDOP: ≤ 3 (or ≤ 4 if unavoidable)
    - HDOP: ≤ 2
[ ] Wait 30 seconds at the point
[ ] Record position (or allow receiver to average automatically)
[ ] Note any warnings or degraded conditions in field log
[ ] Photograph point for documentation
```

---

## Summary: Putting It All Together for River Monitoring

### The Big Picture

All these concepts work together to achieve one goal: **accurately transforming camera pixel coordinates into real-world river surface velocities.**

The chain of accuracy looks like this:

```
Satellite signals
    ↓ (affected by atmospheric delays, satellite errors)
Base station position (established with PPP or survey-in)
    ↓ (RTK corrections broadcast)
Rover at GCPs (achieving cm-level accuracy if PDOP good, RTK fixed)
    ↓ (GCP coordinates used in photogrammetric transform)
Camera image geometry
    ↓ (pixel-to-world coordinate transformation)
Water surface velocities
    ↓ (integration across river cross-section)
Discharge estimates (flow rate)
```

**Every error compounds**: A 5 cm GCP error might become a 10 cm/s velocity error, which becomes a 15% discharge error.

### Key Takeaways

1. **RTK gives you real-time centimeter accuracy**, critical for rapid GCP surveys. Use it when base station is within 20 km.

2. **PPP provides global centimeter accuracy** but requires post-processing. Use it to establish your permanent base station position.

3. **Base-rover setup eliminates common errors** (atmospheric delays, satellite issues) by comparing measurements at two nearby locations.

4. **RINEX format enables post-processing** and data sharing across different software and receiver brands.

5. **Survey-in establishes base position** through averaging. Quick (5 min) for temporary setups, but use 24-hr PPP for permanent installations.

6. **Check points validate your accuracy** independently. They're your "ground truth" proving your system works correctly.

7. **PDOP indicates satellite geometry quality**. Target < 3, avoid > 6. More satellites (8+) generally mean better PDOP and reliability.

### Workflow Example: Setting Up River Monitoring

**Phase 1: Establish Base Station Position (One-time)**
1. Set up GNSS receiver at base location with clear sky view
2. Perform quick survey-in (5-10 min) to get approximate position
3. Collect raw GNSS data for 24 hours
4. Convert to RINEX format using manufacturer software
5. Submit to online PPP service (CSRS-PPP or OPUS)
6. Receive precise coordinates (within 2-5 cm globally)
7. Update base station firmware with precise coordinates

**Phase 2: Measure Ground Control Points (Each site visit)**
1. Power on base station at known position (broadcasting corrections)
2. Set up rover receiver with clear sky view
3. Wait for RTK Fixed solution
4. Check PDOP < 3, satellites ≥ 8
5. Measure 6-8 GCPs distributed around camera view (60 sec each)
6. Measure 2 check points in separate locations (do NOT use for processing)
7. Document all measurements with photos and field notes

**Phase 3: Process Video Data**
1. Import GCP coordinates into photogrammetry software
2. Process video to extract velocity field
3. Check model accuracy against check points
4. If check point RMSE < 5 cm: proceed with velocity analysis
5. If check point RMSE > 5 cm: investigate and remeasure if needed

**Phase 4: Quality Assurance**
1. Calculate check point residuals (errors)
2. Review PDOP values during GCP measurements
3. Verify all GCPs measured with RTK Fixed solutions
4. Document accuracy metrics in metadata
5. Archive RINEX files for potential reprocessing

### Accuracy Targets for River Discharge Monitoring

Based on research findings:

| Component | Target Accuracy | Why It Matters |
|-----------|----------------|----------------|
| Base station position | 2-5 cm (PPP) | Foundation for all rover measurements |
| GCP measurements | 1-3 cm (RTK Fixed, PDOP < 3) | Direct impact on velocity accuracy |
| Check point RMSE | < 5 cm | Validates transformation quality |
| Velocity uncertainty | < 5-10 cm/s | Acceptable for discharge calculations |
| Discharge uncertainty | < 10-15% | Professional hydrology standards |

### Common Mistakes to Avoid

1. **Using survey-in alone for permanent base stations**: Always validate with PPP for long-term installations.

2. **Measuring GCPs without checking PDOP**: High PDOP measurements introduce avoidable errors.

3. **Accepting RTK Float solutions**: Only RTK Fixed has centimeter accuracy.

4. **Not using check points**: You can't know your true accuracy without independent validation.

5. **Poor GCP distribution**: GCPs only near camera result in poor geometry; distribute them throughout the site.

6. **Ignoring satellite count**: Even with good PDOP, < 6 satellites creates reliability problems.

7. **Not documenting metadata**: Always record PDOP, satellite count, solution type, and occupation time.

8. **Forgetting to convert to RINEX**: Keep your options open for reprocessing and validation.

### Resources for Learning More

**Online PPP Services**:
- CSRS-PPP (Natural Resources Canada): https://webapp.geod.nrcan.gc.ca/geod/tools-outils/ppp.php
- OPUS (NOAA): https://www.ngs.noaa.gov/OPUS/

**Open Source Software**:
- RTKLIB: Open source RTK/PPP processing (http://www.rtklib.com/)
- Emlid Studio: User-friendly PPK post-processing (https://emlid.com/)

**Educational Resources**:
- Penn State GEOG 862: GPS and GNSS for Geospatial Professionals (free online course)
- IGS (International GNSS Service): Technical resources and documentation

---

**Document Compiled**: 2025-11-24
**Author**: Research synthesis for OpenRiverCam project
**Sources**: Academic literature, manufacturer documentation, geodetic survey guidelines, and hydrology research papers (2020-2025)
