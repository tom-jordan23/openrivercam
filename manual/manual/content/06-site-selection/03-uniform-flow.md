# 6.3 Uniform Flow Requirement

OpenRiverCam measures surface velocity at one location and combines it with cross-sectional area to calculate discharge (Q = v × A). This approach assumes that the measured velocity represents the average flow through the entire cross-section. For this assumption to be valid, flow must be relatively uniform across the measurement area. This section explains what uniform flow means, why it matters, and how to identify suitable cross-sections during site selection.

By the end of this section, you will be able to:
- Understand what constitutes uniform flow
- Recognize flow patterns that indicate good cross-sections
- Identify flow complications that degrade measurement accuracy
- Evaluate channel characteristics for measurement suitability
- Make informed site selection decisions based on flow uniformity

---

## Review: Why Uniform Flow Matters

### The Fundamental Assumption

Recall from Section 3.1 that discharge equals velocity multiplied by cross-sectional area:

**Q = v × A**

Where:
- Q = discharge (total flow in m³/s)
- v = average velocity across the entire cross-section (m/s)
- A = cross-sectional area (m²)

OpenRiverCam measures velocity at the water surface. The software tracks tracers moving across the field of view and calculates their velocity. This measurement captures velocity in the visible area - typically a section that is 10-30 meters long (along the flow direction) and the full width of the river.

**The critical question:** Does the velocity measured in this visible area represent the average velocity throughout the entire cross-section?

**If flow is uniform:** Velocity is similar everywhere in the cross-section. The measured surface velocity (adjusted for depth) reasonably represents the average.

**If flow is non-uniform:** Velocity varies dramatically across the cross-section - fast in some areas, slow or even reversed in others. A measurement in one area does not represent the average.

[VISUAL PLACEHOLDER: Two side-by-side overhead diagrams:
1. Uniform flow - arrows showing consistent velocity across river width
2. Non-uniform flow - arrows showing fast flow in center, slow/eddying flow near banks]

### What Can Go Wrong with Non-Uniform Flow

**Scenario 1: Measurement area captures only fast center flow**
- Camera views the center channel where flow is fastest
- Misses slower flow near the banks
- Measured velocity is higher than true average
- Calculated discharge is overestimated

**Scenario 2: Measurement area captures recirculating eddy**
- Camera views an area with disturbed, swirling flow
- Flow direction is inconsistent or even reversed in some areas
- Measured velocity is not representative
- Calculated discharge is unreliable

**Scenario 3: Measurement area is downstream of major obstruction**
- Flow patterns are still reorganizing after passing around a large rock or pier
- Velocity distribution is chaotic and not representative of the overall cross-section
- Measured velocity varies dramatically depending on exactly where tracers happen to pass
- Measurement consistency is poor

**The goal:**
Select measurement locations where flow is organized, predictable, and relatively uniform across the cross-section. This ensures that measurements represent the actual discharge.

---

## What is Uniform Flow?

### Defining Hydraulic Characteristics

"Uniform flow" is a hydraulic engineering term. For practical site selection purposes, here's what it means:

### Characteristic 1: Parallel Flow Lines

**What this means:**
Water moves in generally parallel paths downstream. Flow lines (the paths that water parcels follow) run parallel to each other and parallel to the banks.

**Visual indicators:**
- Foam lines run straight downstream, not crossing each other
- Floating debris moves in predictable straight paths
- No swirling or spiraling patterns on the surface

**Why this matters:**
Parallel flow indicates that velocity is organized and consistent across the width. Each part of the cross-section contributes proportionally to discharge.

[VISUAL PLACEHOLDER: Photo of river with parallel foam lines running straight downstream, annotated to show parallel flow paths]

### Characteristic 2: Consistent Depth Across Width

**What this means:**
The riverbed profile is relatively smooth across the cross-section. While the center is typically deeper than the edges (normal for natural channels), there are no sudden drops, pools, or shallow bars that create extreme depth variation.

**Visual indicators:**
- Water surface appears relatively level across the width (accounting for slight bank height differences)
- No visible shallow bars or deep pools within the cross-section
- Flow appears to be moving at similar pace across the width

**Why this matters:**
Extreme depth variations create velocity variations. Very shallow areas have slow flow (friction with bed), very deep areas may have fast flow. Moderate, consistent depth creates more uniform velocity distribution.

### Characteristic 3: Straight or Gently Curving Reach

**What this means:**
The measurement cross-section is located in a straight section of river, or in a very gentle curve (large radius). Avoid tight bends.

**Visual indicators:**
- Looking upstream and downstream, the river runs straight for at least 5-10 channel widths
- If there is curvature, it is gradual (you can barely notice it)
- Banks are parallel, not converging or diverging

**Why this matters:**
In curves, flow accelerates on the outside of the bend and slows on the inside. This creates cross-sectional velocity variation. Straight reaches have more uniform flow.

[VISUAL PLACEHOLDER: Overhead satellite or diagram view showing straight river reach (preferred) vs. tight bend (avoid)]

### Characteristic 4: Steady, Non-Turbulent Flow

**What this means:**
Flow is smooth and predictable, not chaotic or highly turbulent. Some turbulence is fine (it generates foam, which provides tracers), but extreme turbulence indicates non-uniform flow.

**Visual indicators:**
- Water surface has ripples and texture but not violent standing waves or white water
- Foam patches persist and move predictably downstream
- No large boils, whirlpools, or sudden surges

**Why this matters:**
Extreme turbulence indicates complex flow patterns - possibly recirculation, flow separation, or hydraulic jumps. These conditions create velocity variations that are difficult to measure accurately.

### Characteristic 5: Free-Flowing (Not Backwater Affected)

**What this means:**
Flow is driven by the river's natural slope and is not influenced by downstream obstructions that slow or pond the water.

**Visual indicators:**
- Water is clearly moving downstream (visible tracer movement)
- No ponding or reservoir-like appearance
- Velocity appears consistent with the river's slope

**Why this matters:**
Backwater from dams, weirs, or constrictions downstream creates slow, pooled flow that is not representative of the river's discharge capacity. Measurements in backwater zones are unreliable.

[VISUAL PLACEHOLDER: Photo showing smooth, steady flow with visible tracers moving consistently downstream]

---

## Identifying Good Cross-Sections

### Where to Look for Suitable Measurement Locations

### Ideal Location: Straight Reach with Moderate Flow

**Characteristics:**
- Straight channel for 5-10 channel widths upstream and downstream
- Moderate velocity (0.5-2.0 m/s is often ideal)
- Consistent bed profile (no sudden bars or holes)
- Banks are stable and relatively parallel
- Some turbulence from bed roughness (creates tracers) but not extreme

**Why this is ideal:**
These locations naturally produce uniform flow. Water organizes into parallel flow paths with predictable velocity distribution.

**How to find them:**
- Walk or drive along the river, observing channel characteristics
- Look for sections where the river appears "well-behaved" - steady, organized flow
- Straight sections between bends are often good candidates
- Avoid sections immediately upstream or downstream of bridges, structures, or major confluences

**Real-world example from Sukabumi:**
One evaluated site was located in a naturally straight reach approximately 100 meters downstream of a bridge. The river in this section was approximately 20 meters wide with consistent depth of 1.5-2 meters. Flow appeared organized with parallel foam lines. Velocity estimated at 0.8-1.2 m/s based on timing floating debris. This site exhibited excellent flow uniformity characteristics.

### Good Alternative: Controlled Section (Bridge or Structure)

**Characteristics:**
- Flow passes under a bridge or through a controlled section
- Bridge piers or abutments are well upstream of measurement area (>20 meters)
- Flow has reorganized into uniform patterns downstream of the structure
- Channel may be partially straightened or stabilized by the structure

**Why this can work:**
Bridges and structures sometimes create uniform flow conditions downstream. If the structure acts like a flow straightener and the measurement area is far enough downstream for flow to reorganize, conditions can be excellent.

**Caution:**
Too close to the structure (within 5-10 meters downstream of piers), flow may still be disrupted. Observe carefully to ensure flow is uniform in the measurement area itself.

**Real-world example from Sukabumi:**
The selected deployment site was approximately 15 meters downstream of bridge piers. While this is close to a structure, observation revealed that flow had reorganized by this distance. Foam lines from pier turbulence provided excellent tracers, and flow appeared uniform across the cross-section. The bridge also provided excellent camera mounting, making this an ideal combination of flow conditions and practical access.

[VISUAL PLACEHOLDER: Diagram showing bridge with piers, indicating disrupted flow zone (0-10m downstream) and reorganized uniform flow zone (15-30m downstream) where measurement occurs]

### Acceptable with Caution: Wide, Shallow Riffles

**Characteristics:**
- Flow spreads across a wide, relatively shallow section
- Bed is rocky or irregular, creating some turbulence
- Velocity is moderate to fast
- Flow is well-distributed across the width

**Why this can work:**
Riffles naturally distribute flow across the full width, which can promote uniformity. They also generate excellent tracers (foam from turbulence).

**Caution:**
Very shallow riffles (<30cm depth) may be too turbulent and chaotic. Moderate-depth riffles (50-100cm) work better. Ensure that flow is distributed, not concentrated in narrow fast channels with stagnant areas between.

**When to use:**
Consider riffle sections if other options are limited. Verify that flow appears organized despite the turbulence.

---

## Flow Complications to Avoid

### Recognizing Unsuitable Flow Patterns

### Avoid: Tight Bends and Meanders

**Problem:**
In river bends, centrifugal force pushes water toward the outside of the curve. This creates:
- Fast flow on the outside bank
- Slow flow on the inside bank
- Helical (spiral) flow patterns through the cross-section
- Highly non-uniform velocity distribution

**Visual indicators:**
- River curves sharply (small radius relative to channel width)
- Deep scour hole visible on outside of bend
- Shallow point bar on inside of bend
- Flow appears concentrated toward outside bank

**Why this is problematic:**
If you measure velocity in the fast zone (outside), you overestimate discharge. If you measure in the slow zone (inside), you underestimate. The variation can be 2x or more between fast and slow zones.

**Guideline:**
Avoid measurement cross-sections in bends where the radius of curvature is less than 5 times the channel width. Prefer straight sections or very gentle curves.

[VISUAL PLACEHOLDER: Overhead photo or diagram of river bend showing flow concentration on outside, point bar on inside, and non-uniform velocity distribution]

### Avoid: Immediately Downstream of Confluences

**Problem:**
Where two channels merge, flow patterns remain disturbed for considerable distance downstream as the two flows mix and merge. This creates:
- Shear zones where fast and slow flows meet
- Swirling and cross-currents
- Highly variable velocity across the width

**Visual indicators:**
- Visible seam or line on water surface where flows meet
- Different colors or turbidity on each side (sediment from different sources)
- Swirling patterns or eddies
- Inconsistent flow direction across the width

**Distance required:**
Flow typically requires 10-20 channel widths downstream of a confluence to fully reorganize. For a 20-meter-wide river, locate measurement sites at least 200-400 meters downstream of confluences.

**Guideline:**
Avoid sites immediately downstream of tributary inputs or channel mergers.

### Avoid: Immediately Upstream or Downstream of Large Obstructions

**Problem:**
Flow around large obstructions (bridge piers, large rocks, debris jams, islands) creates:
- **Upstream:** Flow accelerates as it squeezes around the obstruction
- **Immediately downstream:** Wake zones with recirculation, eddies, slow or reversed flow
- **Further downstream:** Turbulent mixing zone as flow reorganizes

**Visual indicators:**
- Standing waves upstream of obstruction (flow accelerating)
- Calm or swirling zone immediately behind obstruction (wake)
- Chaotic, turbulent zone extending downstream
- Foam patterns showing swirling or reversed flow

**Distance required:**
Avoid measurements within 5-10 obstruction widths upstream and 10-20 widths downstream. Larger obstructions require more distance.

**Example:**
Bridge pier is 2 meters wide: Avoid measurements within 10 meters upstream and 20-40 meters downstream of the pier.

**Guideline:**
If structures are present, ensure measurement area is far enough downstream for flow to reorganize into parallel flow paths.

[VISUAL PLACEHOLDER: Diagram showing flow around bridge pier - acceleration upstream, wake zone immediately downstream, reorganized flow further downstream with measurement zone indicated]

### Avoid: Backwater Zones

**Problem:**
Backwater occurs when downstream obstructions (dams, weirs, constrictions) slow the flow and pond water upstream. Backwater zones have:
- Very slow, nearly stagnant flow
- Little relationship between water level and discharge
- Flow driven by downstream conditions rather than river slope

**Visual indicators:**
- Water appears ponded, reservoir-like
- Very slow tracer movement or stationary tracers
- Water surface very smooth and flat
- Large fluctuations in water level with minimal flow change (if downstream gate opens/closes)

**Why this is problematic:**
The fundamental assumption Q = v × A breaks down because velocity is so slow and variable. Small changes in downstream conditions create large changes in local water level without corresponding discharge changes.

**Guideline:**
Locate measurement sites in free-flowing reaches, well upstream of any downstream controls. If a dam or weir exists downstream, measure in rapids or riffles upstream where flow is clearly free-flowing.

### Avoid: Extremely Wide, Shallow Flows

**Problem:**
When rivers spread into very wide, very shallow flows:
- Depth may be <20-30cm across most of the width
- Extreme turbulence in shallow water
- Flow may concentrate in narrow fast channels with stagnant areas between
- Velocity distribution is chaotic

**Visual indicators:**
- River is 3-5x wider than normal (braided or flood-overflow conditions)
- Most of the width appears very shallow
- Fast channels visible (darker, more turbulent) with slow areas (lighter, smoother) between

**Why this is problematic:**
Velocity varies enormously across the width. Measurement in a fast channel overestimates; measurement across a slow area underestimates. Averaged measurements are unreliable.

**Guideline:**
Select measurement locations where flow is concentrated into a single channel at least 30-50cm deep across most of the cross-section.

[VISUAL PLACEHOLDER: Photo showing wide, shallow braided flow with multiple fast channels and slow areas - labeled as unsuitable]

### Avoid: Hydraulic Jumps and Standing Waves

**Problem:**
Hydraulic jumps occur when fast, shallow flow (supercritical) transitions to slow, deep flow (subcritical). This creates:
- Violent turbulence and standing waves
- Sudden velocity changes over short distances
- Recirculation and extremely non-uniform flow

**Visual indicators:**
- Sudden transition from smooth, fast flow to churning, turbulent flow
- Standing waves that do not move downstream
- White water and violent boiling
- Distinct change in water surface character

**Why this is problematic:**
Flow characteristics change drastically within meters. Measurement location even slightly upstream or downstream of the jump gives completely different results.

**Guideline:**
Avoid sites with hydraulic jumps. Select calmer sections upstream or downstream where flow is subcritical (slower, deeper, smooth).

---

## Optimal Channel Characteristics

### Physical Features That Promote Uniform Flow

### Channel Shape: Trapezoidal or Rectangular Cross-Sections

**Ideal profile:**
- Banks are relatively symmetrical
- Cross-section approximates a trapezoid (sloping banks) or rectangle (vertical banks)
- Center is deeper than edges (normal), but depth increases gradually, not suddenly
- No sudden bars, holes, or irregularities

**Why this promotes uniformity:**
Symmetrical cross-sections create symmetrical velocity distributions. Gradual depth changes create gradual velocity changes.

**Assessment:**
If possible, observe the riverbed at low water or review bathymetric surveys. Look for smooth, predictable bed profiles.

[VISUAL PLACEHOLDER: Cross-section diagrams showing ideal trapezoidal profile vs. problematic irregular profile with bars and holes]

### Channel Slope: Moderate and Consistent

**Ideal slope:**
- Moderate slope (not too flat, not too steep)
- Consistent slope through the reach (not accelerating or decelerating)
- Approximately 0.001-0.01 slope (1-10 meters drop per kilometer)

**Why this promotes uniformity:**
Consistent slope creates consistent velocity. Too flat and flow becomes sluggish and potentially affected by backwater; too steep and flow becomes torrential and chaotic.

**Assessment:**
Observe overall river character. Does the reach appear similar in slope to adjacent sections, or does it stand out as unusually steep or flat?

### Bed Material: Stable but Rough Enough to Generate Tracers

**Ideal bed:**
- Stable (not actively eroding or depositing large amounts of sediment)
- Moderately rough (gravel, cobbles, boulders) to create some turbulence and foam
- Not extremely rough (large boulders creating major obstacles) or extremely smooth (concrete lining creating no turbulence)

**Why this matters:**
Moderate roughness creates desirable turbulence (tracers) without creating chaotic flow. Stable bed means channel shape does not change rapidly, so rating curves remain valid.

**Assessment:**
Observe bed material if visible. Look for gravel to cobble-sized material in straight sections. Avoid extremely boulder-choked rapids or completely smooth artificial channels.

### Bank Stability: Firm Banks, Not Rapidly Eroding

**Ideal banks:**
- Stable, vegetated, or armored (rock riprap)
- Not actively slumping or eroding
- Parallel through the reach (not converging or diverging)

**Why this matters:**
Stable banks mean channel width remains constant, which preserves rating curves. Eroding banks indicate unstable channel that may change shape and characteristics.

**Assessment:**
Look for evidence of recent bank erosion (fresh scarps, exposed roots, slumped material). Stable banks have vegetation growing to the water's edge.

[VISUAL PLACEHOLDER: Photo showing stable, vegetated riverbanks vs. eroding, unstable banks]

### Width-to-Depth Ratio: Moderate

**Ideal ratio:**
- Width/depth ratio between 10:1 and 40:1
- For a 20-meter-wide river, depth of 0.5-2 meters is typical
- Avoid extremely wide, shallow (ratio >50:1) or narrow, deep (ratio <5:1) sections

**Why this matters:**
Moderate width-to-depth ratios promote uniform velocity distribution. Extremely wide, shallow sections have chaotic flow; extremely narrow, deep sections may have unusual velocity profiles.

**Assessment:**
Visually estimate width and depth. Does the river appear moderately wide with reasonable depth, or unusually extreme in one dimension?

---

## Field Assessment of Flow Uniformity

### Practical Evaluation During Site Visits

### Visual Observation Techniques

**Technique 1: Foam Line Tracking**

**Method:**
Observe foam lines or floating debris as they move downstream through the potential measurement area.

**What to look for:**
- [ ] Do foam lines run parallel to each other?
- [ ] Do they maintain consistent spacing as they move downstream?
- [ ] Do they move at similar speeds across the river width?
- [ ] Are there areas where foam swirls, reverses, or moves slower than surrounding areas?

**Interpretation:**
- Parallel, consistent foam lines = uniform flow ✓
- Crossing, swirling, or highly variable foam patterns = non-uniform flow ✗

[VISUAL PLACEHOLDER: Annotated photo showing parallel foam lines indicating uniform flow]

**Technique 2: Debris Velocity Comparison**

**Method:**
Time floating debris (leaves, sticks) as they travel through the measurement area. Compare velocities in different parts of the cross-section.

**What to do:**
1. Mark a fixed distance (e.g., 10 meters) along the river
2. Time debris floating down the center of the river
3. Time debris floating near the left bank
4. Time debris floating near the right bank
5. Calculate velocities (distance / time)
6. Compare values

**Interpretation:**
- Velocities within ±30% of each other = reasonably uniform ✓
- Velocities varying by more than 50% = poor uniformity ✗

**Example:**
- Center channel: 10m in 8 seconds = 1.25 m/s
- Left bank: 10m in 10 seconds = 1.0 m/s
- Right bank: 10m in 9 seconds = 1.1 m/s
- Variation: 20-25% - Acceptable uniformity

**Technique 3: Surface Pattern Observation**

**Method:**
Stand at the potential camera location and observe the water surface for several minutes.

**What to look for:**
- [ ] Is the surface character consistent across the width (similar ripples, texture)?
- [ ] Are there zones of obviously different flow (glassy smooth near one bank, turbulent in center)?
- [ ] Do patterns remain consistent over time or change chaotically?

**Interpretation:**
- Consistent surface character = uniform flow ✓
- Distinct zones with very different appearance = non-uniform flow ✗

### Quantitative Assessment (If Resources Available)

**Method:**
Use a handheld velocity meter or ADCP to measure velocity at multiple points across the cross-section.

**What to do:**
1. Measure velocity at 5-7 locations across the width (equal spacing)
2. Measure at mid-depth if using point velocity meter
3. Calculate average and standard deviation
4. Assess coefficient of variation (standard deviation / average)

**Interpretation:**
- Coefficient of variation <20% = excellent uniformity
- Coefficient of variation 20-35% = acceptable uniformity
- Coefficient of variation >35% = poor uniformity

**Example:**
Measurements across 20-meter-wide river at 4-meter spacing:
- 2m from left bank: 0.85 m/s
- 6m from left bank: 1.05 m/s
- 10m (center): 1.15 m/s
- 14m from left bank: 1.00 m/s
- 18m from left bank: 0.90 m/s
- Average: 0.99 m/s
- Standard deviation: 0.12 m/s
- Coefficient of variation: 12% - Excellent uniformity

**Practical note:**
This quantitative assessment requires equipment and expertise not always available during humanitarian deployments. Visual observation techniques are sufficient for most site selection decisions.

---

## Flow Uniformity Assessment Checklist

### Systematic Site Evaluation

Use this checklist to assess flow uniformity at potential sites:

### Channel Geometry

- [ ] **Straight reach:** Measurement area is in a straight section or very gentle curve
  - Excellent: Straight for >10 channel widths upstream and downstream
  - Good: Gentle curve, radius >5× channel width
  - Poor: Tight bend, radius <3× channel width

- [ ] **Consistent cross-section:** Bed profile is relatively smooth and consistent
  - Excellent: Gradual depth variation, trapezoidal profile
  - Good: Some irregularity but no extreme bars or holes
  - Poor: Highly irregular with deep pools and shallow bars

- [ ] **Stable banks:** Banks are firm and parallel through the reach
  - Excellent: Vegetated, stable, parallel
  - Good: Generally stable with minor irregularities
  - Poor: Actively eroding or highly irregular

### Flow Patterns

- [ ] **Parallel flow lines:** Foam and debris move in parallel paths
  - Excellent: Clearly parallel, consistent spacing
  - Good: Generally parallel with minor variations
  - Poor: Swirling, crossing, or chaotic paths

- [ ] **Consistent surface character:** Water surface appearance similar across width
  - Excellent: Consistent ripples and texture everywhere
  - Good: Generally similar with minor variations
  - Poor: Distinct zones of very different character

- [ ] **Velocity consistency:** Estimated velocities similar across width
  - Excellent: Velocities within ±20% across width
  - Good: Velocities within ±30% across width
  - Poor: Velocities varying by >50% across width

### Obstructions and Features

- [ ] **Distance from structures:** Adequate distance from piers, rocks, etc.
  - Excellent: >20× obstruction width downstream, >10× upstream
  - Good: >10× obstruction width downstream, >5× upstream
  - Poor: <5× obstruction width

- [ ] **Distance from confluences:** Adequate distance from tributary inputs
  - Excellent: >20 channel widths downstream of confluence
  - Good: >10 channel widths downstream
  - Poor: <10 channel widths downstream

- [ ] **Free-flowing:** Not affected by downstream backwater
  - Excellent: Clearly free-flowing with visible current
  - Moderate: Slower flow but still visible movement
  - Poor: Ponded, nearly stagnant appearance

### Scoring Framework

**Total the number of "Excellent," "Good," and "Poor" ratings:**

**Excellent site for flow uniformity:**
- 5-6 "Excellent" ratings
- 0-1 "Poor" ratings
- Score: 8-9/9 points

**Acceptable site:**
- 3-5 "Excellent" or "Good" ratings
- 0-2 "Poor" ratings
- Score: 5-7/9 points

**Marginal site:**
- 1-3 "Excellent" or "Good" ratings
- 2-4 "Poor" ratings
- Score: 3-4/9 points

**Unsuitable site:**
- 0-1 "Excellent" or "Good" ratings
- 4+ "Poor" ratings
- Score: 0-2/9 points

[VISUAL PLACEHOLDER: Assessment scorecard template with checkboxes for each criterion and rating scales]

---

## Real-World Example: Sukabumi Flow Assessment

### Applying the Flow Uniformity Framework

During Sukabumi site selection, the team evaluated three candidate sites for flow uniformity:

### Site A: Natural Straight Reach (Upstream)

**Channel geometry:**
- Straight reach extending 150m upstream and downstream ✓
- Trapezoidal cross-section, approximately 18m wide, 1.5-2m deep ✓
- Stable vegetated banks ✓

**Flow patterns:**
- Parallel foam lines clearly visible moving downstream ✓
- Consistent surface texture across width ✓
- Debris timing showed velocities: center 1.1 m/s, edges 0.8-0.9 m/s (20-30% variation) ✓

**Obstructions:**
- No structures within 200m upstream or downstream ✓
- Small rapids 80m upstream provided tracers but did not affect flow uniformity in measurement area ✓

**Assessment:**
- Excellent ratings: 6/6
- Good ratings: 0
- Poor ratings: 0
- **Score: 9/9 - Excellent flow uniformity**

**Limitation:**
This site had excellent flow uniformity but was located in a remote area with difficult access and no existing infrastructure for camera mounting. While hydraulically ideal, practical considerations reduced its suitability.

### Site B: Downstream of Bridge (Selected Site)

**Channel geometry:**
- Gentle curve, radius approximately 100m (5× channel width) - Good
- Cross-section slightly irregular due to bridge scour but generally trapezoidal - Good
- Banks stabilized with riprap near bridge - Excellent

**Flow patterns:**
- Foam lines from bridge pier turbulence reorganized into parallel patterns by measurement location (15m downstream) - Excellent
- Surface texture consistent across width - Excellent
- Debris timing showed velocities: center 1.0 m/s, edges 0.85-0.95 m/s (15-20% variation) - Excellent

**Obstructions:**
- Bridge piers 15m upstream (7-8× pier width) - Good (borderline acceptable distance)
- No other obstructions nearby - Excellent

**Assessment:**
- Excellent ratings: 5/6
- Good ratings: 1/6
- Poor ratings: 0
- **Score: 8/9 - Excellent flow uniformity**

**Advantages:**
This site combined excellent flow uniformity with practical benefits (bridge mounting for camera, power access, security). The proximity to bridge piers was borderline but observation confirmed flow had reorganized adequately.

**Decision:**
Selected for deployment based on combination of good flow uniformity and excellent practical characteristics.

### Site C: Channelized Section

**Channel geometry:**
- Perfectly straight concrete-lined channel - Excellent (geometrically)
- Rectangular cross-section, very uniform depth - Excellent (geometrically)
- Concrete banks - Stable but problematic for other reasons

**Flow patterns:**
- Almost no visible tracers (smooth concrete surface generated no foam) - N/A for flow assessment but critical deficiency
- Minimal surface texture due to very smooth bed - Poor (but uniform)
- Very little debris to time velocities - Unable to assess adequately

**Assessment:**
While this site had geometrically uniform flow (straight, consistent cross-section), it was eliminated due to inadequate tracers (Section 6.1) before detailed flow uniformity assessment was completed. This demonstrates that all site criteria must be met - excellent flow uniformity alone is insufficient if tracers are absent.

[VISUAL PLACEHOLDER: Map showing the three sites with flow assessment scores and final decision annotations]

---

## When Flow Uniformity is Borderline

### Strategies for Marginal Sites

Sometimes a site has acceptable but not excellent flow uniformity. Several strategies can improve success:

### Strategy 1: Optimize Measurement Cross-Section Location

**Approach:**
Within a general site area, fine-tune the exact measurement cross-section location to maximize uniformity.

**Example:**
If a bridge crossing provides mounting and power, you may have flexibility to position the measurement cross-section 10m, 15m, or 20m downstream of piers. Test each position to find where flow is most uniform.

**Implementation:**
During site preparation, use temporary markers at several possible cross-section locations. Observe flow patterns at each. Select the position with best uniformity.

### Strategy 2: Expand Field of View to Capture Full Width

**Approach:**
Ensure the camera field of view captures the full river width, not just one portion. This averages velocity across the entire width, compensating for some non-uniformity.

**Consideration:**
Camera height and lens selection must provide adequate field of view. This is primarily a camera positioning decision during installation (Chapter 7), but awareness during site selection helps.

### Strategy 3: Multiple Measurement Cross-Sections

**Approach:**
If resources allow, install cameras at multiple cross-sections within a reach. Average results from multiple locations to reduce errors from any single location's non-uniformity.

**Consideration:**
This approach is rarely used in humanitarian deployments due to cost (multiple cameras) and complexity. More common in research applications or high-value infrastructure monitoring.

### Strategy 4: Accept Limitations with Enhanced Verification

**Approach:**
Deploy at a marginally uniform site but plan enhanced verification measurements (manual ADCP surveys, current meter profiles) to validate and calibrate the camera-based measurements.

**Example:**
If a site has moderate flow non-uniformity but excellent practical advantages (access, security, power), deploy with the plan to conduct quarterly ADCP surveys to verify the rating curve and discharge estimates.

**Consideration:**
This approach acknowledges imperfection but uses supplemental data to maintain acceptable accuracy.

---

## Integration with Overall Site Selection

### Flow Uniformity in Context

Flow uniformity assessment must be integrated with tracers (Section 6.1), lighting (Section 6.2), and accessibility (Section 6.4).

### Balancing Trade-offs

**Scenario 1:**
- Site A: Excellent flow uniformity (9/9), poor tracers (3/9), good lighting (7/9)
- Site B: Good flow uniformity (7/9), excellent tracers (9/9), excellent lighting (8/9)

**Decision:**
Site B is likely superior despite slightly inferior flow uniformity. Excellent tracers are essential; good (not perfect) flow uniformity is acceptable.

**Scenario 2:**
- Site A: Marginal flow uniformity (4/9), excellent tracers (9/9), excellent lighting (8/9)
- Site B: Excellent flow uniformity (9/9), good tracers (7/9), good lighting (7/9)

**Decision:**
This is a more difficult trade-off. Marginal flow uniformity (4/9) raises concerns about measurement accuracy. If "marginal" means "tight bend with 2× velocity variation across width," Site A is unsuitable despite other advantages. If "marginal" means "slight irregularities but generally acceptable," Site A might be acceptable.

**Key principle:**
All criteria must meet minimum thresholds. A site with excellent tracers and lighting but fundamentally non-uniform flow (e.g., tight bend, confluence, extreme turbulence) is unsuitable.

### Minimum Acceptable Flow Uniformity

**Minimum threshold:**
Cross-sectional velocity variation <50% (fastest zone vs. slowest zone differ by less than 2×).

**Example of minimum acceptable:**
- Center channel: 1.5 m/s
- Near banks: 0.8-1.0 m/s
- Ratio: 1.5 / 0.8 = 1.9× - Just within acceptable range

**Example of unacceptable:**
- Center channel: 2.0 m/s
- Inside of tight bend: 0.5 m/s
- Ratio: 2.0 / 0.5 = 4× - Unacceptable non-uniformity

If a site fails to meet this minimum threshold, eliminate it regardless of other advantages.

---

## Summary: Key Concepts for Flow Uniformity

**Why uniformity matters:**
OpenRiverCam measures velocity in one area and assumes it represents the average across the full cross-section. This assumption requires relatively uniform flow.

**Characteristics of uniform flow:**
- Parallel flow lines (foam, debris move in consistent downstream paths)
- Consistent depth across width (gradual variations, not extreme differences)
- Straight or gently curving reach
- Steady, non-turbulent flow (some turbulence acceptable, extreme chaos is not)
- Free-flowing (not backwater affected)

**Ideal measurement locations:**
- Straight reaches with moderate flow
- Well-organized sections downstream of flow-straightening structures
- Moderate-depth riffles with distributed flow

**Flow complications to avoid:**
- Tight bends (non-uniform velocity distribution)
- Confluences (mixing zones persist for 10-20 channel widths)
- Too close to obstructions (disrupted flow zones)
- Backwater zones (slow, ponded flow)
- Extreme shallow, wide flows (chaotic velocity distribution)
- Hydraulic jumps (violent transitions)

**Optimal channel characteristics:**
- Trapezoidal or rectangular cross-section
- Moderate, consistent slope
- Stable but moderately rough bed
- Stable, parallel banks
- Moderate width-to-depth ratio (10:1 to 40:1)

**Field assessment techniques:**
- Foam line tracking (parallel = uniform)
- Debris velocity comparison across width (variation <30% = acceptable)
- Surface pattern observation (consistent character = uniform)
- Quantitative velocity profiling if resources available (coefficient of variation <20% = excellent)

**Assessment framework:**
Evaluate channel geometry, flow patterns, and proximity to obstructions. Score sites on 6 criteria with Excellent/Good/Poor ratings. Sites with 5-6 "Excellent" ratings and 0-1 "Poor" ratings are ideal (8-9/9 points).

**Minimum acceptable threshold:**
Velocity variation across width must be <50% (fastest zone less than 2× slowest zone).

**Integration with other criteria:**
Flow uniformity is necessary but not sufficient. Sites must also have adequate tracers, acceptable lighting, and survey accessibility. Balance trade-offs, but ensure all criteria meet minimum thresholds.

---

**Next Section:** [6.4 Survey Accessibility at All Water Levels](04-survey-accessibility.md)

[VISUAL PLACEHOLDER: One-page visual summary showing:
- Uniform vs. non-uniform flow (overhead diagrams)
- Good cross-section characteristics (straight reach photo)
- Flow complications to avoid (bend, confluence photos)
- Field assessment checklist
- Scoring framework
- "Uniform flow ensures measurements represent true discharge" key message]
