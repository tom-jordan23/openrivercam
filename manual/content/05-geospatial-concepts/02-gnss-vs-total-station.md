# 5.2 Differential GNSS vs Total Station

Section 5.1 established that OpenRiverCam requires centimeter-level survey accuracy, and identified two viable methods: RTK GNSS and total station surveying. This section examines both methods in detail, helping you understand when to use which approach.

By the end of this section, you will understand:
- What GNSS is and how it works for positioning
- What total station surveying is and how it differs from GNSS
- The practical advantages and limitations of each method
- Which situations favor GNSS vs total station
- Equipment and skill requirements for each approach
- How to make an informed decision for your deployment

---

## Understanding GNSS: The Global Navigation Satellite System

### What is GNSS?

When most people say "GPS," they are actually referring to GNSS - Global Navigation Satellite System. GPS is just one GNSS constellation among several.

**GNSS includes multiple satellite systems:**
- **GPS:** United States system, 31 satellites
- **GLONASS:** Russian system, 24 satellites
- **Galileo:** European Union system, 30 satellites
- **BeiDou:** Chinese system, 35 satellites

Modern GNSS receivers track satellites from all these systems simultaneously. More satellites = better accuracy and reliability.

### How GNSS Positioning Works (Simplified)

Think of it like this: if you know your distance to three landmarks, you can figure out where you are.

**Basic GNSS positioning:**

1. **Satellites broadcast signals:** Each satellite continuously transmits a radio signal containing:
   - Its precise orbital position
   - The exact time the signal was transmitted

2. **Your receiver measures timing:** Your GNSS receiver records when each satellite signal arrives.

3. **Calculate distances:** Since radio signals travel at the speed of light (known constant), the receiver calculates distance to each satellite:
   - Distance = signal travel time × speed of light

4. **Triangulate position:** With distances to four or more satellites, the receiver calculates your 3D position (latitude, longitude, elevation).

**The challenge:** This basic approach provides accuracy of only 2-10 meters. Why so poor?

**Sources of error:**
- **Atmospheric delays:** Signal slows passing through ionosphere and troposphere
- **Satellite orbit errors:** Satellite positions not perfectly known
- **Clock errors:** Timing inaccuracies in receiver and satellites
- **Multipath:** Signals bounce off buildings, water, metal before reaching receiver
- **Signal noise:** Interference and general radio noise

For navigation - finding a street address or hiking trail - this 2-10 meter accuracy is fine. For OpenRiverCam ground control points requiring 2 cm accuracy, it is completely inadequate.

**This is why we use differential GNSS methods like RTK.**

[VISUAL PLACEHOLDER: Diagram showing basic GNSS positioning. Top view of Earth with 4 satellites above sending signals to ground receiver. Each satellite-to-receiver line labeled with distance measurement. Receiver location shown as intersection of four spheres. Caption: "GNSS positioning requires signals from 4+ satellites to calculate 3D position. Basic accuracy: 2-10 meters."]

### From Standard GNSS to Differential GNSS

Differential GNSS improves accuracy by using two receivers:
- **Base station:** Stationary at a known location
- **Rover:** Mobile, surveying unknown points

**The key insight:** Many GNSS errors affect both receivers similarly, so we can calculate and remove them.

**How differential correction works:**

1. **Base station knows its true position** (either from long-term measurement or previous survey)

2. **Base station compares measured position to true position:**
   - If base measures position as 2.3 meters east of truth, there is a 2.3 meter eastward error at that moment

3. **Base station broadcasts corrections:**
   - "Right now, I am seeing 2.3m east error, 0.8m north error, 1.5m up error"

4. **Rover applies corrections to its own measurements:**
   - Rover subtracts the same errors from its position
   - Assumes it experiences similar errors (true if base and rover are close together)

5. **Result:** Rover achieves much better accuracy relative to base station

**Types of differential GNSS:**
- **DGPS (Differential GPS):** Basic corrections, 0.5-2 meter accuracy
- **RTK (Real-Time Kinematic):** Advanced corrections using carrier phase, 1-3 cm accuracy

**RTK is what OpenRiverCam uses** - it is covered in detail in Section 5.3.

### GNSS Advantages for River Surveying

**1. Works across obstacles:**
GNSS does not require line-of-sight between base and rover - only clear sky view. This means:
- Survey across rivers without special setup
- Survey GCPs distributed across wide areas
- Work around terrain, vegetation, structures

**Example:** River site with GCPs on both banks, 30 meters apart. With GNSS, you simply walk to each GCP and measure. No need to see across the water.

**2. Portable and field-suitable:**
- Base and rover fit in backpacks
- Powered by rechargeable batteries (6-12 hours)
- No heavy equipment to transport
- Can access remote sites on foot

**Humanitarian context:** You can carry GNSS equipment to sites without vehicle access - river crossings, mountainous areas, remote locations.

**3. Relatively fast setup and measurement:**
- Base initialization: 30-60 minutes (one time per survey day)
- Per point measurement: 1-2 minutes (with RTK fix)
- Efficient for multiple points
- Can survey large areas in single day

**4. Learnable with moderate training:**
- Not a professional surveyor specialty
- IM officers can develop competence in 2-3 days training
- Systematic procedures to follow
- Quality indicators tell you when measurements are good

**5. Increasingly affordable:**
- Low-cost RTK systems: $1,500-2,500
- Open-source hardware and software options
- Cost barrier lowering over time

### GNSS Limitations for River Surveying

**1. Requires clear sky view:**

GNSS receivers need unobstructed view of satellites above 15 degrees elevation angle.

**Cannot work well:**
- Under dense tree canopy
- Between tall buildings (urban canyons)
- In narrow valleys with steep walls
- Under bridges or overhanging structures

**Workaround:** Position GCPs in locations with sky view. Often possible by moving a few meters.

**2. Subject to multipath interference:**

Signals bouncing off reflective surfaces cause positioning errors:
- Large metal structures (bridges, towers, vehicles)
- Water surfaces (especially when surveying near water edge)
- Metal roofs or walls
- Wet ground

**Mitigation:**
- Keep base station away from reflective surfaces (10+ meters)
- Survey GCPs away from metal structures
- Avoid surveying during rain when possible
- Use longer averaging times near challenging surfaces

**3. Requires time to achieve RTK fix:**

RTK positioning requires 10-20 minutes to initialize when starting rover, or when RTK fix is lost.

**Practical impact:**
- Cannot measure instantly - must wait for fix
- If fix is lost (driving under bridge, entering trees), must re-acquire
- Adds time to survey workflow

**Patience is required** - this is normal GNSS behavior.

**4. Limited range between base and rover:**

Correction data must be transmitted from base to rover:
- Radio systems: typically 1-5 km range (line-of-sight)
- Cellular systems: unlimited range (requires cell coverage)

For most OpenRiverCam sites where base and rover are within 500 meters, this is not a problem.

**5. Absolute accuracy requires post-processing:**

RTK provides excellent relative accuracy (1-3 cm between points) but moderate absolute accuracy (0.3-2 meters). The base station position has uncertainty.

**Solution:** PPP (Precise Point Positioning) post-processing improves base station accuracy to 2-10 cm. Covered in Section 5.6.

---

## Understanding Total Station Surveying

Total station surveying is the traditional land surveying method, predating GNSS by decades. It remains valuable for situations where GNSS does not work well.

### What is a Total Station?

A total station is an optical instrument that measures angles and distances with very high precision.

**The device combines:**
- **Electronic distance meter (EDM):** Laser or infrared beam measures distance to target
- **Electronic theodolite:** Measures horizontal and vertical angles precisely
- **Computer:** Calculates coordinates from angles and distances
- **Data storage:** Records measurements

**How it looks:** Mounted on tripod, resembles a camera with telescope. Operator looks through eyepiece or at display screen to aim at targets.

### How Total Station Surveying Works

**Basic principle:** If you know where you are standing, and you measure the direction and distance to another point, you can calculate that point's coordinates.

**Survey procedure:**

1. **Set up total station at known point:**
   - Level instrument on tripod
   - Enter known coordinates of instrument position
   - Orient instrument by sighting to another known point (reference bearing)

2. **Measure target points:**
   - Assistant places reflective prism on survey pole at point to be measured
   - Operator aims total station at prism through telescope
   - Instrument measures horizontal angle, vertical angle, and distance
   - Calculates and records target point coordinates

3. **Move to next point if needed:**
   - If some targets not visible from first setup, relocate total station
   - Set up at new known point and continue

**Reflective prism:** Special target that reflects laser/infrared beam directly back to instrument. Allows measurements at distances up to several kilometers with high accuracy.

[VISUAL PLACEHOLDER: Diagram showing total station survey. Left side: total station on tripod, operator looking through eyepiece. Dotted line showing line-of-sight to reflective prism on survey pole held at GCP (right side). Inset shows prism detail - circular reflective target. Measurements labeled: horizontal angle 127.3°, vertical angle 12.5°, slope distance 23.847m.]

### Total Station Advantages for River Surveying

**1. Very high precision:**
- Typical accuracy: 2-5 millimeters
- Professional-grade instruments: 1-2 millimeters
- Far exceeds OpenRiverCam requirements (20-30 mm)

**Application:** If your project requires absolute maximum accuracy - engineering design, structural monitoring, scientific research - total station provides it.

**2. Works without satellite signals:**
- No dependency on GNSS satellites or atmospheric conditions
- Works under tree canopy
- Works between buildings, in valleys, anywhere with line-of-sight

**Critical use case:** Dense forest canopy site where GNSS cannot get satellite lock. Total station may be only option.

**3. No electromagnetic interference issues:**
- Not affected by radio interference
- No multipath errors from reflective surfaces (when used properly)
- Very reliable measurements

**4. No post-processing required:**
- Coordinates calculated immediately
- No correction files or waiting for PPP processing
- Final results available at end of survey day

### Total Station Limitations for River Surveying

**1. Requires line-of-sight:**

This is the critical limitation. You must be able to see the prism at every point you want to survey.

**Cannot measure:**
- Points blocked by terrain, vegetation, or structures
- Points across river unless you can set up elevated position seeing both banks
- Distributed points requiring multiple instrument setups

**Example scenario:** River site with GCPs on both banks, 30 meters wide with trees on far bank. Total station on near bank cannot see through trees to far bank GCPs. You would need to:
- Set up on elevated position seeing both banks, OR
- Cross river and set up second station on far bank, OR
- Clear line-of-sight through vegetation

This adds significant complexity.

**2. Crossing water is challenging:**

For river sites, many points are across water. Total station requires:
- Elevated setup position viewing both banks
- Clear line-of-sight over water
- Very stable setup (any instrument movement invalidates measurements)

**GNSS alternative:** Simply carry rover across water (boat, wading, bridge) and measure. Much simpler.

**3. Slower and more labor-intensive:**
- Precise instrument leveling required (15-30 minutes per setup)
- Must aim at each prism manually
- Two people required (instrument operator + prism holder)
- Multiple setups if points are distributed
- More complex workflow

**Time impact:** Total station survey typically takes 50-100% longer than equivalent GNSS survey.

**4. Less portable:**
- Heavier equipment (instrument + tripod + prism + accessories)
- More delicate - requires careful handling
- Difficult to transport to remote sites on foot

**5. Requires professional training:**
- Leveling procedure is precise
- Understanding traverse calculations
- Coordinate transformation from local to global system
- Troubleshooting measurement errors

**Skill level:** Typically requires professional surveyor or several weeks of dedicated training. Not easily learned by IM officers in a few days.

**6. Higher cost for river-suitable instruments:**
- Entry-level total stations ($3,000-6,000) have short range and lower accuracy
- River surveying often needs long range (50-100m+ to see across water)
- Professional instruments with adequate range: $8,000-15,000+

---

## Equipment and Skill Comparison

### GNSS RTK Equipment Package

**Core components:**
- RTK base station (receiver + antenna + radio)
- RTK rover (receiver + antenna + radio)
- Survey pole for rover
- Tripod for base station
- Data collection device (smartphone/tablet running SW Maps)
- Batteries and chargers
- USB cables and connections

**Optional but useful:**
- Bipod for rover pole stability
- Backup batteries
- Solar panels for extended operation
- Cellular modem for NTRIP corrections

**Weight:** 5-10 kg total (easily portable)

**Cost range:**
- Budget RTK system (ArduSimple): $1,500-2,500
- Mid-range (Emlid): $3,000-4,000
- Professional (Trimble, Leica): $10,000-15,000+

**For humanitarian OpenRiverCam: Budget systems are adequate.**

### Total Station Equipment Package

**Core components:**
- Total station instrument
- Tripod (heavy-duty, very stable)
- Reflective prism and prism pole
- Data collector or on-board storage
- Batteries and chargers
- Level for precise setup
- Weatherproof transport case

**Optional but useful:**
- Multiple prisms for efficiency
- Prism pole bipod
- Laser rangefinder for approximate layouts
- Known control points at site

**Weight:** 15-25 kg total (requires vehicle or multiple trips)

**Cost range:**
- Entry-level: $3,000-6,000
- Mid-range: $8,000-12,000
- Professional robotic: $15,000-25,000+

**For river surveying: Mid-range minimum for adequate range.**

### Skill Requirements Comparison

| Aspect | GNSS RTK | Total Station |
|--------|----------|---------------|
| **Basic understanding** | Satellite positioning, differential correction | Optical measurement, triangulation |
| **Setup procedure** | Mount antennas, connect cables, initialize | Precise leveling, orientation to reference |
| **Measurement technique** | Hold pole level, wait for fix, record | Aim at prism, measure, record |
| **Quality assessment** | Check fix status, PDOP, satellite count | Verify backsight, check residuals |
| **Troubleshooting** | Recognize poor sky view, multipath | Identify collimation errors, refraction |
| **Training time** | 2-3 days for competence | 1-2 weeks minimum, professional course ideal |
| **Suitable for IM officer?** | Yes, with training | Marginal, better to hire surveyor |

**Honest assessment:** Most humanitarian IM officers can learn RTK GNSS with focused training. Total station requires professional surveyor or extensive training investment.

---

## Decision Framework: Which Method to Use?

Here is a practical decision process for selecting survey method:

### Primary Question: Can GNSS Work at This Site?

**Check these conditions:**

1. **Sky view at GCP locations:**
   - Walk to each planned GCP position
   - Look up - can you see open sky above 15 degrees elevation?
   - Dense tree canopy or narrow valley walls may block satellites

2. **Major metal structures nearby:**
   - Large metal bridges, towers, buildings within 20 meters?
   - These can cause multipath errors

3. **Access for equipment:**
   - Can you carry 10 kg of equipment to site?
   - Is base station location accessible?

**If answers are mostly "yes, no problem" → Use GNSS RTK (recommended path)**

### Secondary Question: Are There Show-Stoppers for GNSS?

**Consider total station if:**

- **Severe sky obstruction:** Dense forest canopy with no clearings, or deep narrow valley
- **Extreme multipath environment:** Directly under large metal bridge, surrounded by metal structures
- **Scientific research requiring absolute maximum accuracy:** Sub-centimeter precision needed for specific application

**Note:** These situations are uncommon for typical river monitoring sites.

### Practical Decision Matrix

| Site Condition | Recommended Method | Notes |
|----------------|-------------------|-------|
| Open river, clear sky view | GNSS RTK | Standard case, 80% of sites |
| Moderate tree cover | GNSS RTK | Position GCPs in clearings |
| Mixed terrain, obstacles | GNSS RTK | Does not require line-of-sight |
| Wide river (50m+) | GNSS RTK | No special setup required |
| Narrow valley, some sky view | GNSS RTK | May need patience for fix |
| Dense forest canopy | Total station or modify site | Last resort |
| Urban area, buildings | GNSS RTK | Avoid narrow urban canyons |
| Remote site, foot access only | GNSS RTK | Portability advantage |
| Scientific precision required | Total station | If sub-centimeter needed |

**In practice, GNSS RTK is suitable for the vast majority of OpenRiverCam deployments.**

### Cost-Benefit Analysis

**GNSS RTK:**
- Lower equipment cost ($1,500-3,000 for adequate system)
- Lower training cost (2-3 days)
- Faster surveys (1 day for complete site)
- Appropriate accuracy (1-3 cm achieves requirements)
- Organizational capacity building possible

**Total station:**
- Higher equipment cost ($8,000-12,000 for river-suitable system)
- Higher training cost (professional course or hire surveyor)
- Slower surveys (1.5-2 days for complete site)
- Excessive accuracy (2-5 mm exceeds requirements)
- Likely requires contracted services

**For humanitarian budgets and capacity: GNSS RTK provides better value in most cases.**

---

## Hybrid Approaches

In some situations, combining both methods offers advantages:

### Use GNSS for Most Points, Total Station for Problem Areas

**Scenario:** River site has good sky view for most GCPs, but 2-3 points are under tree canopy.

**Approach:**
- Survey accessible GCPs with GNSS RTK (fast, efficient)
- Use total station for canopy-blocked GCPs only
- Requires total station setup at position with line-of-sight to blocked points

**Value:** Saves time compared to total station for everything.

### Use Total Station to Establish Control Network, GNSS for Detail Surveying

**Scenario:** Long-term monitoring site requiring very high absolute accuracy.

**Approach:**
- Professional surveyor establishes high-precision control points with total station
- Connect control network to national geodetic survey benchmarks
- Use GNSS RTK for all routine surveys (GCPs, cross-sections, etc.), referencing established control

**Value:** Combines long-term accuracy of total station control with efficiency of GNSS field work.

### Reality Check

Hybrid approaches add complexity and cost. For most humanitarian OpenRiverCam deployments:
- Single-method approach is simpler and adequate
- GNSS RTK alone provides required accuracy
- Hybrid only justified for special circumstances

**Do not over-complicate unless truly necessary.**

---

## Real-World Considerations

### Availability of Equipment and Services

**GNSS RTK:**
- Increasingly available globally
- Online purchase and international shipping straightforward
- ArduSimple, Emlid, and others ship worldwide
- Growing support in developing regions

**Total station:**
- Widely available in urban areas (surveying companies)
- Less available in remote humanitarian contexts
- Rental possible in some locations
- Requires professional operator (hired service)

**Practical implication:** GNSS RTK equipment is easier to acquire and deploy to field locations.

### Organizational Capacity Building

**GNSS RTK:**
- Enables internal capacity development
- Multiple staff can be trained
- Equipment can be shared across projects
- Skills transfer to other applications (boundary surveys, infrastructure, etc.)

**Total station:**
- Typically remains specialist contractor service
- Less skill transfer to general staff
- Equipment requires more careful maintenance
- Contractor dependency for ongoing work

**For humanitarian organizations operating multiple sites: Building internal GNSS capacity offers long-term value.**

### Maintenance and Support

**GNSS RTK:**
- Minimal maintenance (keep batteries charged, protect from water)
- Firmware updates via USB (straightforward)
- Growing online community support
- Parts and accessories available online

**Total station:**
- Requires periodic calibration (professional service)
- More delicate - optical alignment can drift
- Fewer DIY support resources
- Typically manufacturer service required for repairs

**GNSS RTK has lower ongoing support burden.**

---

## Recommendations for OpenRiverCam Deployments

Based on analysis of accuracy requirements, costs, practical constraints, and humanitarian contexts:

### Standard Recommendation: GNSS RTK

**For 90% of OpenRiverCam deployments, GNSS RTK is the appropriate choice:**

1. **Achieves required accuracy** (1-3 cm relative accuracy)
2. **Suitable for river environments** (works across water, does not require line-of-sight)
3. **Affordable** ($1,500-3,000 for adequate system)
4. **Learnable** (IM officers can develop competence)
5. **Portable** (accessible in humanitarian contexts)
6. **Efficient** (complete site survey in one day)

**Equipment recommendation:**
- ArduSimple RTK Kit (budget option, excellent value)
- Emlid Reach RS2+ (mid-range option, user-friendly)

**Training investment:**
- 2-3 days hands-on training
- Include 2-3 staff members for redundancy
- Practice with check points to verify skills

### Alternative Recommendation: Total Station

**Use total station only when:**

1. **GNSS is truly not feasible** (severe canopy, extreme multipath, no satellite access)
2. **Professional surveyor already available** (contract or partnership)
3. **Scientific precision required** (sub-centimeter for research purposes)
4. **Budget allows** (equipment cost + professional fees)

**Implementation approach:**
- Contract professional surveyor with total station
- Specify coordinate system requirements (UTM 48S EPSG:32748 for Indonesia)
- Request standard survey output format (CSV with X,Y,Z)
- Verify accuracy meets requirements (2-3 cm or better)

### Caution: Do Not Use

**Never use these methods for OpenRiverCam GCP surveys:**
- Standard smartphone GPS
- Consumer handheld GPS
- Basic DGPS (unless it achieves proven 2-3 cm accuracy)
- Mapping-grade GPS
- Tape measure from approximate locations

**These methods do not achieve required accuracy. The resulting system will not provide reliable data.**

---

## Summary: Key Concepts to Remember

**GNSS (Global Navigation Satellite System):**
- Satellite-based positioning using GPS + GLONASS + Galileo + BeiDou
- Basic accuracy: 2-10 meters
- Differential correction (RTK): 1-3 cm accuracy
- Requires clear sky view, works across obstacles
- Portable, learnable, increasingly affordable

**Total station:**
- Optical measurement using angles and distances
- Accuracy: 2-5 mm (very high precision)
- Requires line-of-sight to all points
- Professional equipment and training
- Best for canopy-blocked sites or scientific precision

**For OpenRiverCam deployment:**
- GNSS RTK recommended for 90% of cases
- Total station only for special situations
- Both methods achieve required 1-3 cm accuracy
- Choice depends on site conditions and available resources

**Decision factors:**
- Sky view availability → favors GNSS
- Line-of-sight availability → enables total station
- Budget constraints → favors GNSS
- Training capacity → favors GNSS
- Equipment access → GNSS more readily available

**The practical reality:**
Most humanitarian OpenRiverCam deployments will use low-cost GNSS RTK systems with moderate training investment. This provides required accuracy with appropriate cost and capacity development.

**Next section** (5.3 RTK Fundamentals) explains how RTK works in detail - the technical foundation you need to understand before executing surveys in the field.

---

**Next Section:** [5.3 RTK Fundamentals](03-rtk-fundamentals.md)

[VISUAL PLACEHOLDER: Summary comparison infographic. Left column "GNSS RTK" with satellite icon: works across obstacles (checkmark), portable (checkmark), moderate cost (checkmark), learnable (checkmark), requires sky view (caution icon). Right column "Total Station" with surveying instrument icon: extreme precision (checkmark), works anywhere (checkmark), requires line-of-sight (caution icon), professional training (caution icon), higher cost (caution icon). Bottom center: "For OpenRiverCam: GNSS RTK recommended" in highlighted box.]
