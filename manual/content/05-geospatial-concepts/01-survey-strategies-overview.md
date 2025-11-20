# 5.1 Centimeter-Level Survey Strategies Overview

This section introduces the critical topic of surveying accuracy for OpenRiverCam deployments. If you have been following the manual from the beginning, you already understand why surveying matters - Section 4.1 explained how the transformation from pixel coordinates to real-world coordinates depends entirely on accurately surveyed ground control points.

Now we explore the practical question: How do we achieve the centimeter-level accuracy that OpenRiverCam requires? What survey methods are available? What do they cost? How do we choose the right approach?

By the end of this section, you will understand:
- Why centimeter-level accuracy is essential, not optional
- How survey errors propagate through to discharge calculations
- The main survey methods available for this work
- The trade-offs between cost, accuracy, and complexity
- How to select an appropriate survey strategy for your context
- What to expect in terms of equipment, skills, and time

---

## Why Centimeter Accuracy Matters for River Monitoring

### Connecting Survey Accuracy to System Performance

In Section 4.1, we learned that OpenRiverCam transforms pixel measurements to physical measurements using ground control points. The accuracy of those GCP surveys directly determines the accuracy of every velocity and discharge measurement the system produces.

Let's make this concrete with a realistic scenario.

**Scenario: Flood warning system in humanitarian context**

Your organization operates an OpenRiverCam station to provide flood warnings for a refugee camp located along a river. The camp has 15,000 residents and must be evacuated when the river reaches a dangerous discharge level.

The river characteristics:
- Normal flow: 45 cubic meters per second (m³/s)
- Warning threshold: 120 m³/s (camp should prepare for possible evacuation)
- Danger threshold: 180 m³/s (evacuation must begin immediately)
- Evacuation requires 3-4 hours to complete safely

**Your survey accuracy directly affects these critical decisions.**

### The Error Amplification Chain

Remember the measurement chain from Section 4.1:
1. Survey GCPs → 2. Calculate transformation → 3. Track features → 4. Transform to real-world → 5. Calculate velocity → 6. Calculate discharge

Survey errors at step 1 propagate through to discharge at step 6.

**Example 1: High-quality RTK survey (2 cm accuracy)**

If your GCPs are surveyed with 2 cm accuracy:
- Transformation accuracy: ~2 cm
- Velocity measurement error: ~2%
- Discharge error: ~2%

At warning threshold (120 m³/s):
- True discharge: 120 m³/s
- Measured discharge: 117-123 m³/s
- Error: ±3 m³/s

**Decision impact:** You can confidently distinguish normal flow (45 m³/s) from warning level (120 m³/s) from danger level (180 m³/s). The system provides reliable decision support.

**Example 2: Standard GPS survey (3-5 meter accuracy)**

If your GCPs are surveyed with 3 meter accuracy:
- Transformation accuracy: ~3 meters (completely wrong)
- Velocity measurement error: ~60% or more
- Discharge error: ~60% or more

At actual warning threshold (120 m³/s):
- True discharge: 120 m³/s
- Measured discharge: Could show anywhere from 50-200 m³/s
- Error: ±70 m³/s or more

**Decision impact:** The system is useless. It cannot distinguish between safe conditions and dangerous floods. You might evacuate unnecessarily, or fail to evacuate when truly needed.

**Example 3: Moderate handheld GPS survey (0.5 meter accuracy)**

If your GCPs are surveyed with 50 cm accuracy:
- Transformation accuracy: ~50 cm
- Velocity measurement error: ~25%
- Discharge error: ~25%

At warning threshold (120 m³/s):
- True discharge: 120 m³/s
- Measured discharge: 90-150 m³/s
- Error: ±30 m³/s

**Decision impact:** The system provides rough guidance but cannot be trusted for operational decisions. The uncertainty is too large. You would need significant additional margin, defeating the purpose of automated monitoring.

[VISUAL PLACEHOLDER: Bar chart showing "Survey Accuracy vs. Discharge Measurement Quality" with three scenarios side by side. Each shows survey accuracy, resulting discharge error, and decision confidence level (green for RTK, yellow for handheld GPS, red for standard GPS). Include icons showing impact: checkmark for RTK "Reliable decisions," warning triangle for handheld GPS "Marginal utility," X for standard GPS "Unusable data."]

### The Critical Insight

**Centimeter-level survey accuracy is not a "nice to have" - it is the foundation that makes the entire system work.**

You cannot substitute:
- More ground control points for accurate surveying (10 GCPs surveyed poorly is worse than 6 surveyed accurately)
- Better cameras for accurate surveying (high resolution images do not fix transformation errors)
- Advanced software for accurate surveying (sophisticated algorithms cannot compensate for wrong input data)

The quality of your survey determines whether OpenRiverCam provides:
- **Reliable operational data** you can base decisions on, or
- **Expensive noise** that wastes resources and might cause dangerous mistakes

This is why the OpenRiverCam deployment process requires RTK-level surveying. Not because it is the most expensive option, but because it is the minimum accuracy level that produces useful results.

---

## Survey Measurement Fundamentals

Before comparing survey methods, we need to understand what we are actually measuring and what accuracy means.

### What Are We Surveying?

OpenRiverCam survey work involves measuring the three-dimensional positions of specific points:

**1. Ground Control Points (GCPs)**
- Visible markers in the camera's field of view
- Typically 6-10 points distributed across the scene
- Used to calculate the transformation from image to real-world coordinates
- Most critical measurement - requires highest accuracy

**2. Camera Position**
- The location of the camera itself
- Height above water surface
- Used for documentation and verification

**3. Water Level Reference**
- Water surface elevation at specific times
- Related to staff gauge if present
- Used for stage-discharge relationship (rating curve)

**4. River Cross-Section**
- Bathymetric profile across the river
- Spacing typically 1-2 meters
- Used to calculate cross-sectional area for discharge

**Each point needs three coordinate values:**
- **X**: Position east-west (easting in UTM)
- **Y**: Position north-south (northing in UTM)
- **Z**: Elevation above a reference level (height)

### Understanding Accuracy vs. Precision

These terms are often confused, but they mean different things:

**Precision** describes repeatability - how close multiple measurements of the same point are to each other.

Example: Measure the same GCP five times:
- Measurement 1: (100.012, 200.008, 150.315) meters
- Measurement 2: (100.015, 200.011, 150.318) meters
- Measurement 3: (100.013, 200.009, 150.316) meters
- Measurement 4: (100.014, 200.010, 150.317) meters
- Measurement 5: (100.011, 200.012, 150.314) meters

These measurements are very close together (within ~5mm). High precision.

**Accuracy** describes correctness - how close the measurements are to the true position.

What if the true position is actually (100.550, 200.480, 150.820)?
- Your measurements are precise (tightly clustered) but not accurate (offset by 50+ cm from truth)

**For OpenRiverCam, we need both:**
- **High precision** ensures our GCPs are surveyed consistently
- **High accuracy** ensures the absolute positions are correct

### Absolute vs. Relative Accuracy

Another important distinction:

**Relative accuracy** describes how accurately we know the distances and relationships between points.

Example: Two GCPs are 8.347 meters apart. If your survey measures them as 8.349 meters apart, relative accuracy is excellent (2 mm error over 8 meters).

**Absolute accuracy** describes how accurately we know the true geographic position of points on Earth.

Example: Those same two GCPs might be located at:
- True position: (100.550, 200.480) meters in UTM
- Surveyed position: (100.000, 200.000) meters in UTM
- Absolute error: 50+ cm

**For OpenRiverCam transformation, relative accuracy matters most.**

The transformation process primarily cares about the spatial relationships between GCPs - their distances and angles relative to each other. If those relationships are measured accurately (centimeter-level relative accuracy), the transformation will work correctly even if the absolute geographic position is off by meters.

However, absolute accuracy becomes important when:
- Integrating with other geospatial data (satellite imagery, maps)
- Comparing measurements across different survey sessions
- Coordinating with other monitoring stations
- Using survey data for engineering or planning purposes

**Practical implication:** We can achieve excellent transformation with high relative accuracy, then improve absolute accuracy through post-processing if needed. This is exactly what the PPP (Precise Point Positioning) correction process does, as explained in Section 5.6.

[VISUAL PLACEHOLDER: Two diagrams side by side. Left diagram labeled "Relative Accuracy" shows three GCPs as dots with accurate distances between them (8.3m, 6.1m, 10.2m labeled) but positioned offset from a faint "true position" overlay. Right diagram labeled "Absolute Accuracy" shows same three points positioned correctly on true positions. Caption: "Relative accuracy = distances between points. Absolute accuracy = true geographic position. Both matter, but relative accuracy is critical for transformation."]

### Practical Accuracy Expectations

Different survey methods achieve different accuracy levels:

| Survey Method | Relative Accuracy | Absolute Accuracy | Suitable for ORC? |
|---------------|-------------------|-------------------|-------------------|
| Smartphone GPS | 3-10 meters | 3-10 meters | No - far too poor |
| Consumer handheld GPS | 2-5 meters | 2-5 meters | No - unusable |
| High-quality handheld GPS | 0.3-1 meter | 0.3-1 meter | No - marginal at best |
| Differential GPS (DGPS) | 0.5-2 meters | 0.5-2 meters | Marginal - barely adequate |
| RTK GPS (real-time) | 1-3 cm | 0.3-2 meters | Yes - excellent relative, moderate absolute |
| RTK + PPP correction | 1-3 cm | 2-10 cm | Yes - excellent for both |
| Total station | 2-5 mm | Depends on control | Yes - excellent relative accuracy |

**OpenRiverCam requirement: 2-3 cm relative accuracy for GCPs**

This requirement drives us toward RTK GPS or total station methods. Other methods simply cannot achieve the necessary precision.

---

## Survey Method Options

Now that we understand accuracy requirements, let's examine the main survey methods available.

### Option 1: RTK GPS (Real-Time Kinematic GPS)

**What it is:**
A satellite-based positioning system that uses two GPS receivers working together - a stationary base station and a mobile rover - to achieve centimeter-level accuracy through differential correction.

**How it works (simplified):**
- Base station sits at one location and measures GPS signals continuously
- Base station calculates correction data based on its measurements
- Rover receives both GPS signals and correction data from base
- Rover applies corrections in real-time to calculate precise position
- With good conditions, rover achieves 1-3 cm accuracy relative to base

**Advantages for humanitarian contexts:**
- Does not require line-of-sight between points (unlike total station)
- Can survey over obstacles like water
- Relatively quick to set up and use
- Works in any environment with open sky view
- Portable - can be transported in backpacks
- Increasingly affordable equipment options
- Can survey large areas efficiently

**Limitations:**
- Requires clear sky view (minimum 15° above horizon)
- Does not work under dense tree canopy
- Requires 10-20 minutes for initial satellite lock
- Radio or cellular connection needed between base and rover
- Limited range (typically 1-10 km depending on radio system)
- Vulnerable to interference near metal structures or power lines
- Requires technical training to operate correctly
- Post-processing needed for best absolute accuracy

**Typical equipment:**
- Base station GPS receiver and antenna
- Rover GPS receiver and antenna
- Radio communication system (or cellular connection)
- Survey pole for rover
- Tripod for base station
- Data collection device (smartphone or tablet)
- Power for both units (batteries, typically 6-12 hour operation)

**Cost range:** $1,500 - $15,000 depending on equipment quality
- Low-end RTK kits (e.g., ArduSimple): $1,500 - $3,000
- Mid-range systems: $5,000 - $8,000
- Professional-grade systems: $10,000 - $15,000+

**Time requirement:**
- Setup: 30-60 minutes (base station initialization)
- Per GCP measurement: 1-2 minutes (waiting for RTK fix, averaging)
- Full ORC site survey: 3-5 hours total
- Post-processing (PPP corrections): 1-2 hours office work

**Skill level:** Moderate
- Requires training on equipment setup
- Understanding of RTK fix status and quality indicators
- Ability to troubleshoot positioning problems
- Data management and export skills
- 2-3 days of training typically sufficient

**This is the recommended method for most OpenRiverCam deployments.**

[VISUAL PLACEHOLDER: Photo of RTK survey equipment in use at river site - shows base station on tripod in background, surveyor holding rover pole at GCP marker in foreground. Equipment labeled: base station, radio antenna, rover on survey pole, data collector (phone).]

### Option 2: Total Station

**What it is:**
An optical surveying instrument that measures angles and distances to a reflective prism, calculating precise positions through triangulation.

**How it works (simplified):**
- Total station sits on tripod at known survey point
- Operator aims instrument at reflective prism on survey pole
- Instrument measures horizontal angle, vertical angle, and distance
- Calculates 3D coordinates of prism position relative to station
- Multiple setups may be needed to survey all points

**Advantages:**
- Extremely high precision (2-5 mm possible)
- Not dependent on satellites (works anywhere)
- Works under tree canopy, near buildings, in valleys
- Very reliable - no signal interference issues
- Excellent for small, detailed surveys
- No post-processing needed

**Limitations:**
- Requires line-of-sight from station to every survey point
- Cannot survey across water unless special setup
- Slower than RTK for large areas
- Requires multiple setups for distributed points
- More complex to operate - needs trained surveyor
- Less portable - heavier equipment
- Setup time significant for each station position
- Difficult in windy conditions (affects prism on pole)

**Typical equipment:**
- Total station instrument
- Reflective prism on survey pole
- Tripod(s)
- Data collector or on-board storage
- Known control point or secondary GPS for absolute positioning
- Power for instrument

**Cost range:** $3,000 - $25,000+
- Entry-level total stations: $3,000 - $6,000
- Mid-range: $8,000 - $15,000
- High-precision robotic total stations: $20,000+

**Time requirement:**
- Setup per station position: 15-30 minutes
- Per point measurement: 2-5 minutes
- Full ORC site with multiple station setups: 4-6 hours
- May require multiple visits if all points not visible from one location

**Skill level:** Advanced
- Requires professional surveyor training
- Understanding of traverse calculations
- Leveling and instrument setup expertise
- Coordinate transformations
- Several weeks of training typically needed

**Best used when:**
- RTK GPS is not feasible (no sky view, extreme interference)
- Very high precision is required (engineering applications)
- All points can be surveyed from one or two setups
- Professional surveyor is available
- Budget allows for higher equipment and labor costs

[VISUAL PLACEHOLDER: Photo of total station setup at river site. Total station on tripod in foreground with surveyor behind it looking through eyepiece. Second person in background holding prism pole at GCP location. Dotted line showing line-of-sight between instrument and prism.]

### Option 3: DGPS (Differential GPS)

**What it is:**
GPS positioning with corrections from a remote base station, but without the real-time precision of RTK. Typically achieves 0.5-2 meter accuracy.

**Why not adequate for OpenRiverCam:**
While DGPS represents an improvement over standard GPS, its 0.5-2 meter accuracy falls far short of the 2-3 cm requirement. As shown earlier, this level of accuracy produces discharge errors of 25-50%, making the system unreliable for operational decisions.

DGPS is not recommended for OpenRiverCam deployments except possibly for very preliminary site assessment where approximate locations are sufficient.

### Option 4: Handheld Recreational GPS

**What it is:**
Consumer-grade GPS receivers designed for hiking, geocaching, or general navigation.

**Why not adequate:**
Accuracy of 2-10 meters is completely insufficient. These devices are designed for navigation ("find your way back to camp"), not precision surveying. Using handheld GPS for GCP surveys will result in unusable transformation and worthless velocity measurements.

**Never use standard GPS for OpenRiverCam ground control points.**

### Method Comparison Summary

| Factor | RTK GPS | Total Station | DGPS | Handheld GPS |
|--------|---------|---------------|------|--------------|
| Relative accuracy | 1-3 cm | 2-5 mm | 0.5-2 m | 2-10 m |
| Line-of-sight required | No | Yes | No | No |
| Works across water | Yes | Difficult | Yes | Yes |
| Sky view required | Yes | No | Yes | Yes |
| Setup complexity | Moderate | High | Low | Very low |
| Equipment cost | $1.5k-15k | $3k-25k+ | $500-2k | $100-500 |
| Operator skill | Moderate | Advanced | Low | Minimal |
| Survey speed | Fast | Moderate | Fast | Fast |
| **Suitable for ORC?** | **Yes** | **Yes** | **No** | **No** |
| **Recommended for?** | **Most deployments** | **Special cases** | **Not recommended** | **Never use** |

[VISUAL PLACEHOLDER: Decision tree diagram titled "Selecting Survey Method for OpenRiverCam". Start with "Can you achieve 2-3 cm accuracy?" - if No, "Do not use for ORC" (red X). If Yes, "Is clear sky view available at all GCPs?" - if Yes, "Use RTK GPS (recommended)" (green checkmark). If No, "Is line-of-sight available from 1-2 positions?" - if Yes, "Use Total Station" (yellow check). If No, "Modify site or GCP placement."]

---

## Cost-Accuracy Trade-Offs

Budget constraints are real in humanitarian work. Let's examine the trade-offs honestly.

### The False Economy of Cheap Surveying

**Scenario: Attempting to save money with standard GPS**

Organization considers two options:
1. Purchase consumer handheld GPS ($300) and do survey themselves
2. Purchase RTK system ($2,500) or hire RTK survey service ($800)

**Option 1 costs:**
- Equipment: $300
- Staff time: 1 day survey (worth ~$200)
- Total: $500

**Option 1 results:**
- Survey accuracy: 3-5 meters
- Transformation quality: Unusable
- Velocity accuracy: ±60% or more
- Discharge accuracy: Worthless
- Decision value: Zero
- Effective cost: $500 wasted + entire OpenRiverCam system investment wasted

**Option 2 costs:**
- RTK equipment: $2,500 (or survey service: $800)
- Staff time: 1 day survey (worth ~$200)
- Total: $2,700 (or $1,000 with service)

**Option 2 results:**
- Survey accuracy: 2-3 cm
- Transformation quality: Excellent
- Velocity accuracy: ±2-3%
- Discharge accuracy: Operational quality
- Decision value: System fulfills intended purpose
- Effective cost: $2,700 well-invested (or $1,000 for service)

**The math is clear:** Saving $2,000 on survey equipment destroys $10,000+ of overall system value.

**Centimeter-level surveying is not optional. If you cannot achieve it, do not deploy OpenRiverCam.**

### Budget-Conscious RTK Options

If RTK surveying seems expensive, several approaches can reduce costs:

**1. Use low-cost RTK equipment (recommended for humanitarian contexts)**

Modern open-source RTK receivers have dramatically reduced costs:
- ArduSimple RTK kits: $1,500 - $2,500 complete
- Emlid Reach RS2+: $2,500 - $3,500
- Other affordable options emerging

These systems achieve the same 1-3 cm relative accuracy as professional units costing $15,000. The trade-offs:
- Slightly slower initialization
- More manual setup required
- Less automated quality checking
- Simpler data collection software

For OpenRiverCam purposes, these trade-offs are acceptable. The accuracy is identical.

**2. Contract local survey services**

Rather than purchasing equipment, hire a local surveyor with RTK capabilities for site survey days:
- Typical cost: $500 - $1,500 per day depending on location
- Surveyor brings equipment and expertise
- Results delivered in required format
- No equipment maintenance or storage needed

This works well if:
- Only occasional surveys needed (initial setup, annual verification)
- Local surveyors available with RTK equipment
- Can schedule surveys in advance
- Budget allows for recurring service costs

**3. Equipment sharing across organization**

If deploying multiple OpenRiverCam sites:
- Purchase one RTK system for organization
- Transport between sites for surveys
- Shared cost across multiple deployments
- Develop internal expertise

A $2,500 RTK system shared across 5 sites = $500 per site.

**4. Academic or NGO partnerships**

Universities, research institutes, or other NGOs may have RTK equipment:
- Explore partnerships for equipment loan or joint surveys
- Potential for capacity building and training
- May enable access to professional-grade equipment

### The Real Cost of RTK Surveying

Let's put RTK in context of overall OpenRiverCam deployment:

**Typical complete deployment budget:**
- Camera and housing: $2,000 - $5,000
- PtBox or computing: $1,000 - $2,000
- Solar power system: $1,500 - $3,000
- Mounting structure: $500 - $2,000
- Installation labor: $1,000 - $3,000
- **RTK survey equipment: $1,500 - $3,000** (or $800 service)
- Connectivity (cellular modem): $300 - $500
- Miscellaneous (cables, markers, etc.): $500

**Total: $8,300 - $18,500**

RTK surveying represents 8-15% of total deployment cost.

**Within this context, attempting to save on surveying makes no sense.** It compromises the entire investment for a small percentage of total cost.

[VISUAL PLACEHOLDER: Pie chart showing "OpenRiverCam Deployment Cost Breakdown". Segments: Camera/housing (25%), Power system (18%), PtBox/computing (12%), Installation labor (15%), Mounting structure (10%), RTK survey (12%), Connectivity (4%), Other (4%). RTK segment highlighted with note: "12% of budget - enables 100% of functionality."]

---

## Selecting an Appropriate Survey Strategy

How do you choose the right approach for your specific deployment?

### Decision Factors

**1. Site Accessibility and Conditions**

Can you get clear sky view at all GCP locations?
- **Yes:** RTK GPS is feasible (recommended)
- **No:** Consider total station, or modify GCP placement

Is line-of-sight available from 1-2 elevated positions to all GCPs?
- **Yes:** Total station is feasible
- **No:** RTK GPS required, or modify site

Can you access the site with survey equipment?
- RTK: Portable, can be carried in backpacks
- Total station: Heavier, more challenging transport

**2. Available Budget**

Can you invest $1,500 - $3,000 in RTK equipment?
- **Yes:** Purchase equipment for organizational use
- **No:** Consider survey service ($800/day) or equipment sharing

Can you allocate $500-1,500 for contracted survey?
- **Yes:** Hire local surveyor with RTK capability
- **No:** Explore partnerships or defer deployment until budget allows

**Do NOT compromise on accuracy to save money.** Better to delay deployment than to proceed with inadequate surveying.

**3. Available Expertise**

Do you have staff who can be trained on RTK operation?
- RTK requires 2-3 days training for competent operation
- Staff need basic technical aptitude
- English literacy helpful for software

Can you access professional survey support?
- Local surveyors may have total station or RTK
- May be available for hire or partnership

**4. Number of Sites**

Deploying one site?
- Survey service may be most cost-effective
- Or purchase affordable RTK if learning investment is worthwhile

Deploying multiple sites (3+)?
- Purchasing RTK equipment becomes cost-effective
- Develops internal organizational capacity
- Enables maintenance surveys and updates

**5. Long-Term Plans**

Will you need to resurvey annually or after floods?
- Owning equipment provides flexibility
- Service contracts may accumulate costs

Will you expand to additional monitoring locations?
- Internal RTK capability enables scaling
- Training investment pays dividends

### Recommended Strategy for Most Cases

**For typical humanitarian OpenRiverCam deployment:**

1. **Acquire low-cost RTK equipment** ($1,500 - $2,500)
   - ArduSimple or similar proven system
   - Appropriate for organizational capability building
   - Enables multiple deployments

2. **Invest in operator training** (2-3 days)
   - Train 2-3 staff members for redundancy
   - Hands-on field practice
   - Quality control procedures

3. **Plan for PPP post-processing** (improves absolute accuracy)
   - Included in Section 5.6 procedures
   - Uses free services (AUSPOS)
   - Provides verification of survey quality

4. **Budget for annual verification surveys**
   - Resurvey check points to verify stability
   - Update GCPs if camera moves or changes
   - Monitor long-term system accuracy

This strategy provides:
- Required accuracy for reliable OpenRiverCam operation
- Organizational capacity for future deployments
- Reasonable budget within overall system cost
- Flexibility for maintenance and updates

---

## What to Expect: The Survey Process

Understanding what surveying entails helps with planning and resource allocation.

### Timeline for Initial Site Survey

**Day before survey (preparation):**
- Charge all batteries (base, rover, data collector)
- Configure survey software (SW Maps project setup)
- Test equipment integration
- Verify GCP markers are in place
- Check weather forecast
- Prepare field notes and checklists
**Time: 2-3 hours**

**Survey day:**

Morning (setup):
- Transport equipment to site
- Establish base station at suitable location
- Initiate base station survey-in (30-60 minutes)
- Set up rover and data collection system
- Establish check points for quality control
**Time: 2-3 hours**

Midday (data collection):
- Survey camera position
- Collect sample video showing all GCPs
- Survey each GCP (6-10 points, 1-2 minutes each)
- Survey water level
- Survey river cross-section (10-20 points)
- Monitor check points throughout day
**Time: 3-4 hours**

Afternoon (completion):
- Final check point measurement
- Verify data quality and completeness
- Stop base station logging
- Pack equipment
- Multiple data backups
**Time: 1 hour**

**Total field time: 6-8 hours for complete site survey**

**Post-processing (office):**
- Export survey data from data collector
- Convert RINEX files from base station
- Submit to PPP service (AUSPOS)
- Apply PPP corrections in QGIS
- Export final coordinates for PtBox
- Quality control checks
**Time: 2-3 hours** (plus wait time for PPP processing)

### Skills Required

**For RTK operator:**
- Basic understanding of GPS/GNSS principles
- Ability to follow systematic procedures
- Attention to detail for quality control
- Comfort with smartphone/tablet software
- Problem-solving when encountering fix issues
- Careful record keeping

**Training provides:**
- Equipment setup and initialization procedures
- Understanding of RTK fix status and quality indicators
- Proper measurement techniques (pole leveling, averaging times)
- Troubleshooting common problems
- Data export and backup procedures
- Safety considerations in river environments

**Most humanitarian IM officers can develop these skills with proper training.**

### Common Challenges and Solutions

**Challenge 1: Cannot get RTK fix at some GCP locations**
- **Cause:** Sky view obstructed, multipath interference
- **Solution:** Move GCP to nearby location with better sky view, or wait 15-20 minutes for satellite geometry to improve

**Challenge 2: Base station survey-in takes very long**
- **Cause:** Poor satellite conditions, obstructions
- **Solution:** Relocate base to better location, or accept longer survey-in time

**Challenge 3: Measurements seem inconsistent**
- **Cause:** Not waiting for stable fix, pole not level, rover moving during measurement
- **Solution:** Increase averaging time, verify pole bubble level, ensure pole is stable

**Challenge 4: Lost communication between base and rover**
- **Cause:** Exceeded radio range, obstruction, interference
- **Solution:** Move closer, reposition radio antenna, check radio configuration

**Challenge 5: Running out of battery power**
- **Cause:** Underestimated survey time, cold weather reduces battery life
- **Solution:** Carry backup batteries, minimize base station restarts

**These challenges are normal - experienced operators learn to anticipate and solve them quickly.**

[VISUAL PLACEHOLDER: Illustrated field guide showing survey day timeline with icons for each phase. Morning: base station setup icon, coffee cup. Midday: rover pole at GCP, sun icon. Afternoon: data export, checklist icon. Below timeline, show common challenges with small icons: blocked sky (tree icon), battery (low battery icon), radio connection (signal icon). Each with brief solution note.]

---

## Accuracy Requirements by Measurement Type

Different parts of the survey have different accuracy requirements:

### Critical Accuracy (1-3 cm required)

**Ground Control Points:**
- Most critical measurement in entire survey
- Directly determines transformation quality
- Requires RTK fix status
- Multiple measurements averaged (60-120 seconds)
- All quality gates must be met
- Check point drift monitoring throughout day

**Why critical:** Errors in GCPs propagate to every velocity measurement.

### High Accuracy (2-5 cm acceptable)

**Water level reference:**
- Used for rating curve development
- Affects discharge calculation accuracy
- Requires good RTK fix
- Multiple measurements averaged (30-60 seconds)

**Why important:** Determines stage-discharge relationship accuracy.

### Moderate Accuracy (5-10 cm acceptable)

**River cross-section:**
- Used for area calculation
- Many points averaged across width
- Bed elevation uncertainty acceptable within reason
- Standard RTK fix adequate (30-60 seconds averaging)

**Why less critical:** Many measurements averaged, small errors at individual points acceptable.

### Lower Accuracy (10-20 cm acceptable)

**Camera position:**
- Documentation purposes
- Not used in transformation calculations
- Standard RTK fix acceptable (10-30 seconds)

**Why least critical:** Informational, does not directly affect measurements.

**The key insight: Focus survey effort where accuracy matters most - the ground control points.**

---

## Connection to Following Sections

This section introduced the strategic question: How do we achieve centimeter-level accuracy? The answer for most deployments is RTK GPS with PPP post-processing.

The following sections in Chapter 5 provide the technical understanding needed to execute RTK surveys successfully:

**Section 5.2: Differential GNSS vs. Total Station** - Deeper comparison of the two viable survey methods

**Section 5.3: RTK Fundamentals** - How RTK works, why it achieves centimeter accuracy, critical concepts

**Section 5.4: Base and Rover Stations** - Understanding the two-receiver RTK system

**Section 5.5: RTK Fix Status** - When to collect points, quality indicators, troubleshooting

**Section 5.6: Logging, RINEX, and PPP Corrections** - Post-processing for improved absolute accuracy

**Section 5.7: Coordinate Systems** - UTM zones, datums, coordinate reference systems

**Section 5.8: Physical and Environmental Factors** - Conditions affecting survey quality

After completing Chapter 5, you will understand the "why" and "how" of surveying. Chapter 9 (Site Survey) then provides the detailed step-by-step procedures for executing surveys in the field.

---

## Summary: Key Concepts to Remember

**Why centimeter accuracy matters:**
- Survey errors propagate to velocity and discharge measurements
- 2 cm survey error → 2% discharge error (acceptable)
- 50 cm survey error → 50% discharge error (unusable)
- Centimeter accuracy is not optional - it determines whether the system works

**Survey method requirements:**
- RTK GPS: 1-3 cm relative accuracy, suitable for most sites
- Total station: 2-5 mm accuracy, suitable when RTK not feasible
- DGPS, handheld GPS: Insufficient accuracy, never use for GCPs

**Cost considerations:**
- Low-cost RTK equipment: $1,500 - $2,500 (recommended)
- Survey service: $500 - $1,500 per day
- RTK represents ~12% of total deployment cost
- False economy to skimp on surveying - compromises entire system

**Realistic expectations:**
- Initial site survey: 6-8 hours field time
- Post-processing: 2-3 hours office time
- Operator training: 2-3 days for competence
- Skills achievable by most IM officers

**Accuracy hierarchy:**
- Ground control points: 1-3 cm (critical)
- Water level: 2-5 cm (high importance)
- Cross-section: 5-10 cm (moderate)
- Camera position: 10-20 cm (lower importance)

**Recommended strategy:**
- Acquire low-cost RTK equipment ($1,500-2,500)
- Train internal staff (2-3 people for redundancy)
- Use PPP post-processing for verification
- Build organizational capacity for multiple deployments

**The most important takeaway:**
OpenRiverCam requires centimeter-level surveying. This is achievable with affordable equipment and moderate training. Organizations should budget for RTK capability as essential infrastructure, not optional enhancement. Without it, the system cannot fulfill its purpose.

When you proceed to execute surveys (Chapter 9), you will apply these concepts with detailed field procedures. The foundation is clear: invest in proper survey capability, or do not deploy OpenRiverCam at all.

---

**Next Section:** [5.2 Differential GNSS vs. Total Station](02-differential-gnss-vs-total-station.md)

[VISUAL PLACEHOLDER: Summary infographic showing the survey accuracy chain: "Survey accuracy determines system accuracy." Flow from left to right: Survey GCPs (target icon, 2cm) → Calculate transformation (calculator icon) → Track features (camera icon) → Transform coordinates (grid icon) → Calculate velocity (water flow icon) → Calculate discharge (measurement icon, Q=v×A). Below, show failure scenario: Poor survey (10m GPS) leads to broken chain with X marks. Above, show success scenario: RTK survey leads to green checkmarks throughout chain.]
