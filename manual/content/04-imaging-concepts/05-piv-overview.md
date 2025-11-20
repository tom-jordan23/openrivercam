# 4.5 Particle Image Velocimetry Overview: How OpenRiverCam Measures Flow

This is the most important section in Chapter 4. Everything you have learned so far - the fundamental equation Q = v × A, tracers and surface features, pixel-to-physical transformation, lens and perspective distortion - comes together here to explain how OpenRiverCam actually works.

Particle Image Velocimetry (PIV) and Particle Tracking Velocimetry (PTV) are the technical terms for the methods OpenRiverCam uses to measure velocity. These names sound complex, but the concepts are accessible. We will build your understanding step by step, connecting each piece to what you already know from previous sections.

This section is longer than others because the concept is critical and complex. Take your time. By the end, you will understand the complete system - from camera capture to discharge estimate - and how every component connects.

By the end of this section, you will understand:
- What PIV and PTV are and how they differ
- The complete workflow from video capture to velocity field
- How features are detected and tracked across frames
- How individual velocity vectors become a complete velocity field
- The role of spatial averaging and uncertainty
- How surface velocity converts to discharge
- Why the entire system depends on every previous concept
- How to evaluate measurement quality

---

## Starting with the Complete Picture

Before diving into technical details, let's understand what the complete system does.

### The Goal: From Video to Discharge

**What you start with:**
A video camera mounted on a river bank, recording the water surface.

**What you need to know:**
How much water is flowing past (discharge in m³/s).

**The steps in between:**
1. **Video capture**: Camera records water surface at 10-30 frames per second
2. **Feature detection**: Software identifies trackable features (foam, debris, ripples) in each frame
3. **Feature tracking**: Software follows each feature from frame to frame, measuring how far it moved
4. **Pixel velocity calculation**: For each tracked feature, calculate velocity in pixels per second
5. **Coordinate transformation**: Convert pixel velocities to real-world velocities using the transformation from ground control points
6. **Velocity field generation**: Combine thousands of individual velocity measurements into a spatial map showing velocity across the entire river surface
7. **Spatial averaging**: Average velocities across the river width and along the flow direction
8. **Surface-to-depth correction**: Apply 0.85 factor to convert surface velocity to average velocity throughout depth
9. **Discharge calculation**: Multiply average velocity by cross-sectional area (Q = v × A)

**The result:**
Discharge estimate with uncertainty bounds (e.g., "Current discharge: 67.3 ± 4.2 m³/s").

This nine-step process happens automatically. As an operator, you provide the inputs (camera installation, ground control points, cross-section survey) and receive the outputs (discharge measurements). Understanding how the process works helps you provide better inputs and interpret the outputs more effectively.

[VISUAL PLACEHOLDER: Flowchart showing complete process from "Video capture" through nine steps to "Discharge estimate". Each box labeled with step name and brief description. Arrows showing information flow. Key inputs highlighted: GCPs (step 5), cross-section (step 9).]

---

## Understanding the Terms: PIV and PTV

### What Do These Acronyms Mean?

**PIV: Particle Image Velocimetry**
- **Particle**: The features we track (foam, debris, ripples - called "particles" because they act like small markers)
- **Image**: Using images (video frames) to observe the particles
- **Velocimetry**: Measuring velocity (from Latin velocitas = speed, metry = measurement)

**PTV: Particle Tracking Velocimetry**
- **Particle**: Same as PIV - the features we track
- **Tracking**: Following individual particles across multiple frames
- **Velocimetry**: Measuring velocity

**The practical difference:**
- **PIV**: Analyzes how patterns of many particles shift between frames (treats clusters of features as a group)
- **PTV**: Tracks individual particles one by one (identifies each feature and follows it specifically)

**For OpenRiverCam:**
The software uses hybrid approaches - sometimes tracking individual features (PTV-like), sometimes analyzing pattern shifts in regions (PIV-like), depending on what works best for the conditions. As an operator, you do not need to know which method is being used at any moment. The software chooses automatically based on the tracer conditions.

**The simplified explanation we will use:**
Throughout this section, we will refer to "feature tracking" rather than PIV or PTV. This is more intuitive and captures what the system does: detecting features and tracking how they move.

[VISUAL PLACEHOLDER: Two side-by-side diagrams. Left labeled "PTV approach" shows individual features labeled A, B, C tracked separately with connecting lines. Right labeled "PIV approach" shows region-based analysis with grids and pattern matching. Both show same river view with foam and debris.]

---

## Step 1: Feature Detection - What Can the Software See?

The first step is identifying features that can be tracked. Understanding how the software "sees" the water surface helps you recognize good vs. poor measurement conditions.

### How Cameras See (Review from Section 3.2)

Cameras do not see "foam" or "leaves" or "ripples" the way humans do. Instead, cameras see patterns of light and dark - regions where pixel brightness or color differs from surrounding areas.

**What the software looks for:**
- **Brightness contrast**: Dark patches on a lighter background, or light patches on a darker background
- **Texture**: Regions where pixel patterns have structure (not uniform or random)
- **Edges**: Boundaries where brightness changes sharply
- **Identifiable patterns**: Shapes or texture configurations that can be recognized in the next frame

**Real-world examples:**
- **Foam**: Appears as light-colored patches against darker water (high contrast)
- **Floating debris**: Casts shadow or appears as dark object (contrast and texture)
- **Ripples**: Create patterns of light and shadow as water reflects sunlight at different angles (texture)
- **Color variations**: Sediment plumes, algae patches - anything creating visible difference from surrounding water

### Feature Detection Process

**Simplified explanation:**

**Frame 1 at time = 0.0 seconds:**
The software analyzes the image and identifies regions of interest:
- "Region at pixel (450, 320) has high contrast - potential feature"
- "Region at pixel (780, 510) has distinct texture - potential feature"
- "Region at pixel (1200, 650) has identifiable edge pattern - potential feature"

The software might identify 100-1000+ potential features in a single frame, depending on tracer conditions.

**Criteria for good features:**
- **Distinctiveness**: Feature looks different from surrounding area (stands out)
- **Size**: Large enough to be visible across multiple frames (typically 5-20 pixels across)
- **Stability**: Appears solid and coherent (not random noise or transient glare)

**What gets filtered out:**
- Uniform regions with no contrast (nothing to track)
- Random noise (single bright/dark pixels with no pattern)
- Extremely small features (1-2 pixels - too small to track reliably)
- Transient reflections or glare (appear in one frame, gone in the next)

[VISUAL PLACEHOLDER: River image with detected features highlighted. Overlay showing boxes around trackable features (foam patches, debris, ripples) with labels indicating "Good feature: high contrast, stable" vs. areas with no boxes labeled "No feature: uniform surface, no contrast".]

### The Feature Density Principle

**Too few features:**
If the software identifies only 5-10 features in the entire frame:
- Limited spatial coverage (features might all be in one area)
- High uncertainty (a few outliers significantly affect the average)
- Possible gaps in data if features disappear

**Too many features (dense clutter):**
If the software identifies 5,000+ features in overlapping clusters:
- Individual features become hard to distinguish from each other
- Tracking becomes ambiguous (which feature is which in the next frame?)
- Computational demands increase without improving accuracy

**Optimal range:**
Typically 100-1,000 well-distributed features provide:
- Good spatial coverage across the river width
- Redundancy (outliers don't dominate)
- Manageable computational requirements
- Reliable velocity estimates

**Connection to Section 3.2:**
This is why we emphasized tracer conditions in Section 3.2. Good tracer conditions (scattered foam and debris) create optimal feature density. Poor tracer conditions (glassy smooth water or dense vegetation mats) create too few or too many features.

---

## Step 2: Feature Tracking - Following Features Across Frames

Once features are identified in Frame 1, the software must find the same features in Frame 2 to measure how far they moved.

### The Matching Problem

**The challenge:**
Frame 1 shows Feature A at position (450, 320). Frame 2 (captured 0.1 seconds later) shows many features. Which one is the same Feature A that has now moved?

**The solution: Template Matching**

Think of this like a puzzle:

1. **Create a template**: Extract a small region (perhaps 15×15 pixels) around Feature A in Frame 1. This is the "template" - what Feature A looks like.

2. **Search in Frame 2**: Look for regions in Frame 2 that match the template. The software searches nearby locations (if water flows at 2 m/s and frames are 0.1 seconds apart, the feature probably moved less than 0.2 meters, which might be 20-30 pixels).

3. **Find the best match**: Calculate similarity scores for each potential location. The location with the highest similarity is probably where Feature A moved to.

4. **Calculate displacement**: If Feature A was at (450, 320) in Frame 1 and matches best at (465, 325) in Frame 2, it moved 15 pixels right and 5 pixels down.

**Mathematical detail (optional):**
The software uses correlation techniques (comparing patterns mathematically) to find matches. You don't need to understand the mathematics, but knowing that it compares patterns helps you understand why distinct, stable features track better than uniform or transient features.

### Tracking Success and Failure

**When tracking works well:**
- Features are distinctive (unique patterns that don't look like other features)
- Features move reasonable distances (not too far, not too little)
- Features persist (don't disappear between frames)
- Image quality is good (adequate lighting, minimal blur)

**When tracking fails:**
- Feature disappears (submerges, moves out of frame)
- Feature changes appearance (foam bursts, debris rotates)
- Multiple features look identical (ambiguous matching)
- Feature moves too far (unexpected turbulence, outlier motion)

**What the software does with failures:**
Failed tracks are discarded. If 800 features were identified but only 600 tracked successfully, the software uses the 600 successful tracks. This is why redundancy matters - some failure is expected and acceptable.

[VISUAL PLACEHOLDER: Three-panel diagram showing tracking process. Panel 1: Frame 1 with Feature A marked at position (450, 320) with template box around it. Panel 2: Frame 2 showing search area with multiple potential matches. Panel 3: Confirmed match at (465, 325) with displacement arrow showing 15-pixel movement.]

### Multi-Frame Tracking

**Single-pair vs. sequence tracking:**

**Simple approach (pair matching):**
- Compare Frame 1 to Frame 2: identify features, track, calculate velocities
- Compare Frame 2 to Frame 3: identify features, track, calculate velocities
- Continue for each frame pair in the video sequence

**Advanced approach (trajectory tracking):**
- Track Feature A from Frame 1 → Frame 2 → Frame 3 → Frame 4 → ...
- Build a trajectory showing where the feature moved over multiple frames
- Calculate velocity from the trajectory (more robust, reduces noise)

OpenRiverCam software may use either or both approaches depending on conditions. The key result is the same: velocity estimates for each tracked feature.

---

## Step 3: From Pixel Movement to Pixel Velocity

Once we know how far a feature moved in pixels, we calculate its velocity in pixels per second.

### The Calculation

**Given information:**
- Feature moved from pixel (450, 320) to pixel (465, 325)
- Time between frames: 0.1 seconds

**Calculate displacement:**
- Horizontal displacement: 465 - 450 = 15 pixels
- Vertical displacement: 325 - 320 = 5 pixels
- Total displacement: sqrt(15² + 5²) = sqrt(225 + 25) = sqrt(250) = 15.8 pixels

**Calculate velocity:**
- Pixel velocity: 15.8 pixels / 0.1 seconds = 158 pixels per second

**Direction:**
The feature moved primarily to the right (positive horizontal) and slightly downward (positive vertical). The direction vector is (15, 5) or simplified (3, 1) after dividing by 5.

**Repeat for all features:**
If 600 features tracked successfully, we now have 600 velocity measurements:
- Feature 1: 158 pixels/s at direction (3, 1)
- Feature 2: 142 pixels/s at direction (2.8, 0.9)
- Feature 3: 165 pixels/s at direction (3.1, 1.2)
- ... (600 total measurements)

**At this stage:**
We have hundreds of velocity measurements in pixel space. These are not yet useful for calculating discharge because pixels are not physical units. We need transformation.

[VISUAL PLACEHOLDER: Annotated image showing multiple tracked features with velocity vectors. Each vector represented as an arrow showing magnitude (length) and direction. Pixel coordinates labeled. Scale bar showing "50 pixels/second" for reference.]

---

## Step 4: Coordinate Transformation - Pixel Velocities Become Real Velocities

This is where everything from Section 4.1 (Transformation) and Section 4.3 (Perspective) comes together.

### Applying the Homography Transformation

Recall from Section 4.1: we used ground control points (GCPs) to establish a transformation that converts pixel coordinates to real-world coordinates. Now we apply that transformation to the velocity measurements.

**For each tracked feature:**

**Feature at time 1:**
- Pixel position: (450, 320)
- Apply transformation → Real-world position: (6.2, 10.5) meters

**Feature at time 2:**
- Pixel position: (465, 325)
- Apply transformation → Real-world position: (6.9, 10.7) meters

**Real-world movement:**
- Horizontal distance: 6.9 - 6.2 = 0.7 meters
- Vertical distance: 10.7 - 10.5 = 0.2 meters
- Total distance: sqrt(0.7² + 0.2²) = 0.73 meters

**Real-world velocity:**
- Velocity: 0.73 meters / 0.1 seconds = 7.3 meters per second

**Key observation:**
The transformation accounts for perspective distortion automatically. The feature moved 15.8 pixels, which corresponded to 0.73 meters at this location in the image. At a different location (closer to camera or farther from camera), 15.8 pixels might correspond to a different physical distance. The transformation handles this variation.

### Why Transformation is Critical

Let's see what happens without proper transformation:

**Scenario: Using a constant scale factor (wrong approach)**

Suppose someone incorrectly assumes "1 pixel = 0.03 meters everywhere in the image":
- Feature moved 15.8 pixels
- Estimated distance: 15.8 × 0.03 = 0.47 meters
- Estimated velocity: 0.47 / 0.1 = 4.7 m/s

**Actual result using transformation (correct approach):**
- Feature moved 15.8 pixels
- Transformed distance: 0.73 meters (accounting for location-specific scale)
- Velocity: 0.73 / 0.1 = 7.3 m/s

**Error from wrong method:**
The constant scale factor underestimated velocity by 36%. This would make discharge estimates completely wrong.

**Connection to surveying (Section 4.1):**
The transformation is only as good as the GCP survey data. If GCPs were surveyed with 50 cm errors, the transformation would be wrong, and velocity measurements would be systematically biased. This is why centimeter-level RTK surveying is absolutely critical.

[VISUAL PLACEHOLDER: Split diagram showing transformation process. Left panel: Pixel space with feature track shown as arrow, pixel coordinates labeled. Arrow labeled "HOMOGRAPHY TRANSFORMATION (uses GCPs)". Right panel: Real-world space with same track shown in meters, coordinates labeled. Velocity calculation shown for both (158 px/s → 7.3 m/s).]

---

## Step 5: Building the Velocity Field - From Points to Surface

Now we have hundreds of individual velocity measurements scattered across the river surface. The next step is organizing these measurements into a structured velocity field.

### What is a Velocity Field?

A velocity field is a spatial map showing velocity at every location across the measured area.

**The sports field analogy:**
Imagine a weather map showing wind speed across a country. At each location, an arrow shows wind direction and speed. This is a velocity field for wind.

For OpenRiverCam, the velocity field shows water velocity across the river surface. At each location, we know how fast the water is flowing and in what direction.

**Why velocity fields matter:**
Rivers don't flow uniformly. Water moves faster in some locations than others:
- **Center of river**: Usually fastest
- **Near banks**: Usually slower (friction with banks)
- **Deep sections**: Complex velocity patterns
- **Near obstructions**: Turbulent or diverted flow

A single average velocity would miss this complexity. The velocity field captures spatial variation.

### Creating the Grid

**The discretization process:**

The river surface is divided into a grid of cells (like a checkerboard):
- Typical cell size: 0.5 m × 0.5 m to 1.0 m × 1.0 m
- Finer grid: More spatial detail, but requires more features to populate all cells
- Coarser grid: Less detail, but works with fewer features

**Example grid:**
A river 15 meters wide and covering 30 meters of length might use a 1 m × 1 m grid:
- Grid dimensions: 15 × 30 = 450 cells
- Each cell will have a velocity estimate

**Populating the grid:**

For each cell, the software identifies which velocity measurements fall within that cell:
- Cell at position (5m, 10m): Contains 3 velocity measurements (6.8 m/s, 7.1 m/s, 7.3 m/s)
- Average for cell: (6.8 + 7.1 + 7.3) / 3 = 7.07 m/s

**Cells with no measurements:**
If a cell contains no tracked features (perhaps due to lack of tracers in that area), the software may:
- Interpolate from neighboring cells (estimate based on nearby velocities)
- Leave cell empty (mark as no data)
- Apply spatial smoothing (blend values from surrounding cells)

The specific approach depends on software implementation. The key result is a complete grid with velocity estimates throughout the measurement area.

[VISUAL PLACEHOLDER: River surface divided into grid cells (checkerboard pattern). Each cell contains an arrow showing velocity magnitude and direction. Cells color-coded by velocity magnitude (blue = slow, green = medium, red = fast). Concentration of arrows in center (fastest flow), fewer near banks (slower flow).]

### Spatial Patterns in Velocity Fields

**What you typically see:**

**Cross-stream variation:**
- Fastest velocities in the center of the river (deepest channel, least friction)
- Moderate velocities in mid-sections
- Slowest velocities near banks (shallow water, friction with banks)

**Longitudinal variation:**
- Relatively consistent velocities along the flow direction (in straight sections)
- Acceleration in narrow sections (same discharge through smaller area requires higher velocity)
- Deceleration in wide sections (larger area accommodates flow at lower velocity)

**Turbulence and eddies:**
- Behind obstructions (rocks, bridge piers): Complex, swirling flow patterns
- Near bends: Faster flow on outside of curve, slower on inside
- At confluences: Mixing zones with variable velocities

**Why this matters:**
Understanding typical patterns helps you evaluate measurement quality:
- If the velocity field shows fastest flow near the banks (unusual), something may be wrong
- If the velocity field shows chaotic, random patterns (no coherent structure), data quality may be poor
- If the velocity field shows expected patterns (center fast, banks slow), confidence is high

---

## Step 6: Spatial Averaging - From Field to Representative Velocity

The velocity field shows spatial variation, but for discharge calculation we need a single representative velocity value. This is where spatial averaging comes in.

### Why We Average

**The discharge equation requires one velocity:**
Q = v × A requires a single average velocity (v) that represents the entire cross-section.

**But velocity varies spatially:**
The velocity field shows velocities ranging from 3 m/s near the banks to 8 m/s in the center. What value should we use?

**The solution:**
Calculate a spatial average that properly weights each measurement based on how much area it represents.

### Simple Area-Weighted Average

**The concept:**
Average all the velocities in the velocity field, giving equal weight to each grid cell.

**The calculation (simplified example):**

Suppose we have a 10-cell grid with these velocities:
- Cell 1: 6.5 m/s
- Cell 2: 7.2 m/s
- Cell 3: 7.8 m/s
- Cell 4: 8.1 m/s (center, fastest)
- Cell 5: 7.5 m/s
- Cell 6: 6.9 m/s
- Cell 7: 5.8 m/s
- Cell 8: 5.2 m/s
- Cell 9: 4.8 m/s (near bank, slowest)
- Cell 10: 5.5 m/s

**Average:**
(6.5 + 7.2 + 7.8 + 8.1 + 7.5 + 6.9 + 5.8 + 5.2 + 4.8 + 5.5) / 10 = 6.53 m/s

This 6.53 m/s is the average surface velocity across the measured area.

### Depth-Weighted Averaging (Advanced)

**The refinement:**
Not all areas of the river contribute equally to discharge. Deeper sections carry more water than shallow sections, so their velocities should be weighted more heavily.

**How it works:**
If cross-section depth information is available:
- Cell in deep channel (3 m depth): Contributes more to overall discharge, weight = 3
- Cell in shallow section (1 m depth): Contributes less, weight = 1

**Weighted average example:**
- Cell in deep section: velocity 8.0 m/s, depth 3 m, contribution = 8.0 × 3 = 24
- Cell in shallow section: velocity 5.0 m/s, depth 1 m, contribution = 5.0 × 1 = 5
- Weighted average: (24 + 5) / (3 + 1) = 29 / 4 = 7.25 m/s

The depth-weighted average (7.25 m/s) is higher than the simple average would be, because it properly accounts for the fact that the fast-flowing deep section carries more water.

**When this matters:**
- Rivers with highly variable depth across the width
- Channels with distinct deep thalweg (main channel) and shallow edges
- More accurate discharge estimates when depth information is available

**Practical note:**
Not all OpenRiverCam installations use depth-weighted averaging (requires detailed bathymetry data). Simple area-weighted averaging is often sufficient, especially if the river has relatively uniform depth or if the field of view focuses on the main channel.

[VISUAL PLACEHOLDER: Two diagrams showing averaging approaches. Top: Simple average - all cells weighted equally, calculation shown. Bottom: Depth-weighted average - cells sized proportionally to depth, calculation shown with weights. Both show final average velocity value.]

---

## Step 7: Surface-to-Depth Correction - From Surface to Average Velocity

Recall from Section 3.1: water at the surface moves faster than water at depth due to friction with the riverbed. OpenRiverCam measures surface velocity, but discharge calculation requires average velocity throughout the entire depth.

### The Velocity Profile (Revisited)

**Why velocity varies with depth:**
- **At the surface**: No friction above (just air), water moves fastest
- **At mid-depth**: Moderate friction from water layers above and below
- **Near the bed**: Maximum friction from riverbed, water moves slowest

**Typical profile:**
- Surface velocity: 100% (the measurement we have)
- Mid-depth velocity: ~90% of surface
- Near-bed velocity: ~50-60% of surface
- Average throughout depth: ~85% of surface

**The 0.85 factor:**
Based on extensive hydrological research across many rivers, surface velocity multiplied by 0.85 provides a good estimate of depth-averaged velocity:

**Average velocity = Surface velocity × 0.85**

### Applying the Correction

**From the previous step:**
Spatial averaging gave us: Surface velocity = 6.53 m/s

**Apply correction:**
Average velocity (through full depth) = 6.53 × 0.85 = 5.55 m/s

This 5.55 m/s is the velocity value we use in the discharge equation.

### When the 0.85 Factor Varies

**The 0.85 value is typical but not universal:**
- **Smooth beds (sand, silt)**: Factor might be 0.85-0.90 (less friction, flatter velocity profile)
- **Rough beds (large rocks, boulders)**: Factor might be 0.80-0.85 (more friction, steeper velocity profile)
- **Very shallow water**: Factor might be 0.75-0.80 (bed friction affects larger proportion of depth)
- **Very deep water**: Factor might be 0.88-0.92 (bed friction affects smaller proportion)

**How to determine the factor for your site:**
- **Default approach**: Use 0.85 (standard value, works for most rivers)
- **Calibration approach**: Conduct manual velocity measurements at depth (using current meter or ADCP) and compare with surface measurements to calculate site-specific factor
- **Literature approach**: Consult hydrological studies for similar river types

For humanitarian applications, the default 0.85 factor is usually adequate. Small variations (0.83 vs. 0.87) have minimal impact on operational decisions.

### Uncertainty from Surface-to-Depth Correction

**Source of uncertainty:**
The 0.85 factor is an approximation. The true factor might be 0.82 or 0.88, introducing ±3-5% uncertainty in the velocity estimate.

**Combined with other uncertainties:**
- Feature tracking: ±2-5%
- Transformation accuracy: ±2-5% (depends on GCP survey quality)
- Surface-to-depth factor: ±3-5%
- Total velocity uncertainty: ±5-10% (errors compound but don't add linearly)

**Impact on discharge:**
Since Q = v × A, a 10% error in velocity creates a 10% error in discharge (assuming area is known accurately).

For context: ±10% discharge uncertainty means a measurement of 60 m³/s could be anywhere from 54 to 66 m³/s. For flood warning or water resource decisions, this is usually acceptable accuracy.

[VISUAL PLACEHOLDER: Side-view diagram of river showing velocity profile. Vertical axis is depth (surface to bed), horizontal axis is velocity. Curved line showing velocity profile (fastest at surface, slowest at bed). Average velocity line shown at 85% of surface velocity. Formula shown: v_average = v_surface × 0.85]

---

## Step 8: Discharge Calculation - Bringing It All Together

Finally, we combine the average velocity with cross-sectional area to calculate discharge.

### The Fundamental Equation (Again)

**Q = v × A**

Where:
- **Q**: Discharge (what we want to know)
- **v**: Average velocity throughout depth (just calculated: 5.55 m/s)
- **A**: Cross-sectional area at current water level (from survey)

### Cross-Sectional Area at Current Water Level

**Where area comes from:**
During site setup (Chapter 9 - Surveying), the riverbed cross-section was surveyed:
- Distance across the river at many points
- Depth at each point (or elevation of the bed)
- Result: A profile showing the channel shape

**Example profile:**
- Left bank: elevation 150.0 m
- 3 m from left bank: bed elevation 148.5 m (1.5 m depth when water at 150.0 m)
- 6 m from left bank: bed elevation 147.2 m (2.8 m depth)
- 9 m from left bank: bed elevation 146.8 m (3.2 m depth - deepest point)
- 12 m from left bank: bed elevation 147.5 m (2.5 m depth)
- 15 m from left bank (right bank): elevation 150.2 m

**Current water level:**
The camera or a separate gauge measures current water level: 150.5 m elevation.

**Calculate current area:**
With water at 150.5 m:
- Depth profile: 2.0 m, 3.3 m, 3.7 m (deepest), 3.0 m, 0.3 m (near right bank, barely underwater)
- Cross-sectional area (using trapezoidal integration): 38.5 m²

**Discharge calculation:**
Q = v × A
Q = 5.55 m/s × 38.5 m²
Q = 213.7 m³/s

### Uncertainty in Discharge

**Sources of uncertainty:**
1. **Velocity uncertainty**: ±10% → velocity could be 5.0 to 6.1 m/s
2. **Area uncertainty**: ±5% (survey accuracy, water level measurement) → area could be 36.6 to 40.4 m²
3. **Combined**: Errors compound → discharge uncertainty approximately ±12%

**Discharge range:**
- Measured: 213.7 m³/s
- Uncertainty: ±12% → ±25.6 m³/s
- Range: 188 to 239 m³/s

**Reporting:**
The system reports: "Discharge: 214 ± 26 m³/s" or "Discharge: 214 m³/s (confidence interval 188-239 m³/s)"

**Interpreting uncertainty for decisions:**
- If flood threshold is 250 m³/s: Current measurement 214 m³/s is clearly below threshold (even upper bound 239 m³/s is below)
- If flood threshold is 220 m³/s: Current measurement is ambiguous (within uncertainty range) - exercise caution, monitor closely
- If flood threshold is 180 m³/s: Current measurement clearly exceeds threshold (even lower bound 188 m³/s is at threshold) - take action

Understanding uncertainty helps make informed decisions rather than treating discharge estimates as exact values.

[VISUAL PLACEHOLDER: Complete calculation flowchart showing: (1) Velocity field → Spatial average (6.53 m/s), (2) Apply 0.85 factor → Average velocity (5.55 m/s), (3) Cross-section at current water level → Area (38.5 m²), (4) Multiply → Discharge (213.7 m³/s), (5) Add uncertainty bounds → Final result (214 ± 26 m³/s). Each step labeled with values.]

---

## Complete System Integration: How Everything Connects

Now let's trace how every concept from previous sections contributes to the final discharge estimate.

### The Connected Chain

**1. Ground Control Points (Section 4.1):**
- Survey 8-10 points with RTK accuracy (±2 cm)
- Identify same points in camera image
- **Enables:** Coordinate transformation from pixels to meters

**2. Lens Distortion Correction (Section 4.2):**
- Camera calibration measures lens distortion
- Software unwarps images before processing
- **Enables:** Accurate pixel measurements (straight lines remain straight)

**3. Perspective Distortion Correction (Section 4.3):**
- Homography transformation calculated from GCPs
- Accounts for scale variation with distance from camera
- **Enables:** Correct conversion of pixel movement to real-world movement at any location in the image

**4. Tracers (Section 3.2):**
- Natural features (foam, debris, ripples) on water surface
- Provide the visible markers that can be tracked
- **Enables:** Feature detection and tracking (without tracers, no measurement possible)

**5. Feature Detection (This section):**
- Software identifies trackable regions of contrast and texture
- Creates list of features to track
- **Enables:** Velocity measurement at many points across the surface

**6. Feature Tracking (This section):**
- Software follows features from frame to frame
- Measures pixel displacement
- **Enables:** Velocity calculation in pixel space

**7. Coordinate Transformation (This section):**
- Apply homography to convert pixel velocities to real velocities
- Accounts for perspective distortion automatically
- **Enables:** Real-world velocity measurements

**8. Velocity Field Generation (This section):**
- Organize velocity measurements spatially
- Create structured map of velocities across river
- **Enables:** Understanding of spatial variation, quality assessment

**9. Spatial Averaging (This section):**
- Calculate representative velocity from field
- Weight by area or depth
- **Enables:** Single velocity value for discharge equation

**10. Surface-to-Depth Correction (This section):**
- Apply 0.85 factor (or site-specific factor)
- Convert surface velocity to depth-average
- **Enables:** Correct velocity for discharge calculation

**11. Cross-Section Survey (Section 3.1, Chapter 9):**
- Measure riverbed profile
- Calculate area at current water level
- **Enables:** Area component of discharge equation

**12. Discharge Calculation (This section):**
- Multiply average velocity by area: Q = v × A
- Report with uncertainty bounds
- **Delivers:** Actionable discharge estimate for decisions

**Every step depends on previous steps. If any step fails, the chain breaks.**

This is why:
- Survey accuracy matters so much (step 1 determines step 7 accuracy)
- Camera calibration matters (step 2 enables step 6)
- Tracer availability matters (step 4 enables step 5)
- Understanding the complete system helps you troubleshoot when something goes wrong

[VISUAL PLACEHOLDER: Large systems integration diagram showing all 12 steps as interconnected nodes. Arrows showing dependencies. Color-coded by chapter (green = hydrology concepts, blue = imaging concepts, orange = surveying, red = final output). Central path highlighted showing critical path from GCPs → Transformation → Velocity → Discharge.]

---

## Evaluating Measurement Quality

Understanding how PIV/PTV works helps you assess whether a measurement is reliable.

### Quality Indicators to Watch

**1. Number of tracked features:**
- **Excellent**: 500+ features tracked successfully
- **Good**: 100-500 features
- **Marginal**: 30-100 features
- **Poor**: <30 features

More features = more redundancy = more reliable average.

**2. Velocity field coherence:**
- **Good**: Velocities show expected spatial pattern (center fast, banks slow, smooth gradients)
- **Concerning**: Velocities show chaotic, random pattern (suggests tracking errors or very turbulent conditions)
- **Bad**: Velocities show impossible pattern (faster at banks than center, negative velocities)

Coherent patterns indicate reliable tracking.

**3. Velocity variance:**
- **Low variance**: Tracked features show similar velocities (e.g., most between 5-7 m/s with average 6 m/s)
- **High variance**: Tracked features show wildly different velocities (e.g., ranging from 2-15 m/s with average 6 m/s)

Low variance indicates consistent, reliable measurements. High variance suggests noise or outliers.

**4. Spatial coverage:**
- **Good**: Features tracked across entire river width
- **Concerning**: Features only in one section (e.g., only near left bank)
- **Bad**: Features only in small cluster

Broad coverage ensures the average represents the whole river, not just one section.

**5. Temporal consistency:**
- **Good**: Sequential measurements show smooth variation (6.2 m/s, 6.4 m/s, 6.3 m/s, 6.5 m/s over several minutes)
- **Concerning**: Sequential measurements jump erratically (6.2 m/s, 8.1 m/s, 4.5 m/s, 7.3 m/s)

Smooth temporal changes indicate stable conditions and reliable measurements.

### Red Flags That Demand Investigation

**Sudden change in measurement quality:**
- Previously getting 400 features, now getting 20 → Check tracer conditions, camera position, possible obstruction
- Previously coherent velocity field, now chaotic → Check for unusual conditions (heavy turbulence, dense debris)

**Measurements inconsistent with visual observation:**
- Camera shows slow-looking flow but measurement reports very high velocity → Check transformation (GCPs might be wrong)
- Camera shows obviously fast flow but measurement reports very low velocity → Check transformation

**Measurements inconsistent with context:**
- Discharge higher during obvious low-flow period → Investigate system calibration
- Discharge decreasing when rainfall is occurring upstream → Investigate measurement validity or check for upstream dam releases affecting expected patterns

**Systematic patterns in errors:**
- All measurements consistently 50% too high or too low → Check surface-to-depth factor, check transformation scale
- Measurements accurate at low flow but wrong at high flow → Check if GCPs are being submerged

Understanding quality indicators transforms you from a passive data receiver to an active quality controller.

---

## Common Problems and Troubleshooting

### Problem 1: "Very few features detected, poor measurement quality"

**Possible causes:**
- Insufficient tracers (smooth water, dry season)
- Camera focus problems (image blurry)
- Poor lighting (severe glare, too dark)
- Field of view changed (camera moved, vegetation grew)

**Diagnosis:**
- Review recent video footage
- Check tracer conditions (is water surface visible and textured?)
- Verify camera settings (focus, exposure)

**Solutions:**
- If seasonal tracer scarcity: Accept data gaps during that period, or consider artificial tracer seeding for critical measurements
- If camera issue: Refocus, clean lens, adjust settings
- If field of view issue: Reposition camera

### Problem 2: "Velocity measurements seem systematically too high or too low"

**Possible causes:**
- Transformation error (wrong GCP coordinates, GCPs moved)
- Surface-to-depth factor incorrect for this site
- Camera image scale changed (zoom adjusted, resolution changed)

**Diagnosis:**
- Conduct manual verification (measure velocity with current meter, compare with camera measurement)
- Check GCP survey data for errors
- Review transformation reprojection errors

**Solutions:**
- Re-survey GCPs if coordinates are wrong
- Adjust surface-to-depth factor if site-specific conditions differ from 0.85 assumption
- Recalculate transformation if camera settings changed

### Problem 3: "Velocity field shows nonsensical patterns"

**Possible causes:**
- Tracking failures (software matching wrong features)
- Extreme turbulence (features don't move with average flow)
- Large debris interfering (logs, boats creating unusual patterns)

**Diagnosis:**
- Review velocity field visualization (does it show impossible patterns?)
- Check tracked feature vectors (are there many outliers?)
- Review video footage for unusual conditions

**Solutions:**
- Filter outliers (software should do this automatically, but parameters may need adjustment)
- Accept that extreme conditions may not be measurable
- Wait for conditions to stabilize

### Problem 4: "Discharge estimates don't match expectations or downstream measurements"

**Possible causes:**
- Cross-section area wrong (survey error, water level measurement error)
- Velocity measurements accurate but area is at wrong water level
- Downstream measurement is different location (may legitimately differ due to tributaries, abstractions)

**Diagnosis:**
- Verify water level measurement
- Check cross-section survey data
- Calculate discharge manually from velocity and area to isolate which component is wrong

**Solutions:**
- Re-survey cross-section if it is incorrect
- Calibrate water level sensor if it is measuring wrong elevation
- Adjust expectations if downstream measurements legitimately differ

[VISUAL PLACEHOLDER: Troubleshooting flowchart showing decision tree. Start: "Problem with measurement?" → Branches for different symptoms (low quality, wrong values, nonsensical patterns, discharge mismatch) → Diagnostic steps → Solutions. Color-coded by severity (green = minor adjustment, yellow = requires investigation, red = critical issue).]

---

## Real-World Example: Complete Workflow

Let's work through a complete example from video capture to discharge estimate, using realistic numbers.

### Scenario Setup

**Site:** Medium river near refugee camp, OpenRiverCam installed for flood early warning

**Camera:** Mounted 8 meters above water surface, 10 meters from near bank, looking across and downstream at 35-degree angle

**Survey data:**
- 8 ground control points surveyed with RTK (±2 cm accuracy)
- Cross-section surveyed: river 14 m wide, depths ranging 1.2 m (near banks) to 3.5 m (center)
- Current water level: 151.2 m elevation (measured from staff gauge visible in camera)

**Current conditions:**
- Moderate flow (recent rains)
- Good tracer availability (foam, floating debris)
- Overcast day (good lighting, minimal glare)

### Step-by-Step Processing

**Video capture:**
- 30-second video captured at 15 frames per second (450 frames total)
- Image resolution: 1920 × 1080 pixels
- Focus on river surface from near bank to far bank

**Feature detection:**
- Software analyzes each frame
- Frame 1: Identifies 487 potential features (foam patches, debris, ripples)
- Features distributed across river width

**Feature tracking:**
- Software tracks features across frame sequences
- Frame 1 → Frame 2 (0.067 seconds apart, 15 fps)
- Successfully tracked 412 features (85% success rate - excellent)
- Failed tracks discarded (features that disappeared, ambiguous matches)

**Pixel velocity calculation:**
- Example Feature #237:
  - Frame 1 position: (856, 492)
  - Frame 2 position: (871, 497)
  - Displacement: 15 pixels horizontal, 5 pixels vertical = 15.8 pixels total
  - Time: 0.067 seconds
  - Pixel velocity: 15.8 / 0.067 = 236 pixels/second
- Repeat for all 412 tracked features
- Result: 412 pixel velocity measurements

**Coordinate transformation:**
- Apply homography transformation (calculated from 8 GCPs)
- Feature #237 at location (856, 492) is at position (8.2 m, 12.5 m) in real world
- Pixel displacement 15.8 pixels = real displacement 0.89 meters (at this location)
- Real velocity: 0.89 m / 0.067 s = 13.3 m/s surface velocity...

Wait - this seems too high. Let me recalculate with realistic numbers.

**Correction:** Let's use typical river velocities:
- Feature #237 pixel velocity: 35 pixels/second (more realistic for moderate flow)
- Transformation scale at this location: 1 pixel = 0.025 meters
- Real velocity: 35 × 0.025 = 0.875 m/s per second → 0.875 m/s surface velocity

**Velocity field generation:**
- Divide river surface into 0.5 m × 0.5 m grid cells
- 14 m wide × 20 m long = 28 × 40 = 1120 cells
- Assign each of 412 velocity measurements to appropriate cell
- Average velocities within each cell
- Result: Velocity field showing velocities ranging from 0.4 m/s (near banks) to 1.1 m/s (center)

**Spatial averaging:**
- Simple area-weighted average across all cells with data
- Average surface velocity: 0.82 m/s

**Surface-to-depth correction:**
- Apply 0.85 factor (standard)
- Average velocity through depth: 0.82 × 0.85 = 0.70 m/s

**Cross-sectional area:**
- Current water level: 151.2 m elevation
- From surveyed cross-section profile, calculate area at this level
- Area: 32.8 m²

**Discharge calculation:**
- Q = v × A
- Q = 0.70 m/s × 32.8 m²
- Q = 23.0 m³/s

**Uncertainty estimation:**
- Velocity uncertainty: ±10% → v = 0.63 to 0.77 m/s
- Area uncertainty: ±5% → A = 31.2 to 34.4 m²
- Discharge uncertainty: ±12% → Q = 20.2 to 25.8 m³/s

**Final result:**
"Discharge: 23.0 ± 2.8 m³/s (confidence interval 20.2-25.8 m³/s)"

**Interpretation:**
- Flood threshold for this site: 45 m³/s
- Current discharge: 23.0 m³/s (about 50% of flood threshold)
- Status: No flood warning needed
- Trend: Monitor over next 6-12 hours to see if discharge rising or stable

This complete example shows how every step connects to produce actionable information for humanitarian decisions.

[VISUAL PLACEHOLDER: Multi-panel visualization showing the complete workflow with this example. Panel 1: Raw video frame with features highlighted. Panel 2: Tracked features with displacement arrows. Panel 3: Velocity field color-coded by speed. Panel 4: Cross-section with area shaded. Panel 5: Final discharge calculation with uncertainty bounds. All labeled with specific values from example.]

---

## Summary: Key Concepts to Remember

**What PIV/PTV is:**
Particle Image Velocimetry and Particle Tracking Velocimetry - methods for measuring velocity by tracking visible features (particles) on the water surface across sequential video frames.

**The complete workflow:**
1. Detect features in video frames (foam, debris, ripples)
2. Track features from frame to frame (measure pixel displacement)
3. Calculate pixel velocities (distance divided by time)
4. Transform to real-world velocities (apply homography)
5. Generate velocity field (spatial map of velocities)
6. Average spatially (representative velocity)
7. Correct for depth (surface × 0.85 = average)
8. Calculate discharge (velocity × area)

**How everything connects:**
- **Tracers** (Section 3.2) provide features to track
- **Transformation** (Section 4.1) converts pixel to meters
- **Lens correction** (Section 4.2) ensures accurate pixel measurements
- **Perspective correction** (Section 4.3) ensures correct scale throughout image
- **Atmospheric effects** (Section 4.4) add uncertainty but don't prevent measurement
- **Cross-section** (Section 3.1) provides area for discharge calculation

**Quality indicators:**
- Number of tracked features (more = better)
- Velocity field coherence (expected patterns = good)
- Velocity variance (low variance = reliable)
- Spatial coverage (broad coverage = representative)
- Temporal consistency (smooth changes = stable)

**Sources of uncertainty:**
- Feature tracking: ±2-5%
- Coordinate transformation: ±2-5%
- Surface-to-depth factor: ±3-5%
- Cross-section area: ±3-5%
- Combined: ±5-15% depending on conditions

**Typical uncertainties acceptable:**
For humanitarian applications, knowing discharge to ±10-15% is vastly better than not knowing discharge at all. OpenRiverCam provides continuous, automated monitoring with acceptable accuracy for operational decisions.

**Troubleshooting approach:**
- Check tracer conditions (video review)
- Verify transformation (GCP accuracy)
- Assess feature tracking success (quality indicators)
- Validate results (manual verification, context checks)

**The critical takeaway:**
PIV/PTV is how OpenRiverCam works - it is the engine that converts video into discharge. Understanding this process helps you:
- Install systems correctly (knowing what matters for measurement)
- Interpret data quality (recognizing good vs. poor conditions)
- Troubleshoot problems (isolating which step is failing)
- Communicate with confidence (explaining the system to stakeholders)

You are now equipped with complete understanding of how OpenRiverCam measures river discharge. From camera to discharge, from pixels to cubic meters per second, from surface features to operational decisions - you understand the entire system.

The remaining chapters will apply this knowledge:
- **Chapter 5**: Understanding flow regimes and interpreting measurements in context
- **Chapter 6**: Selecting sites where these techniques will work well
- **Chapter 7**: Installing cameras to optimize measurement conditions
- **Chapter 9**: Surveying GCPs with the accuracy the system requires
- **Chapter 10**: Configuring software using the concepts you now understand
- **Chapter 11-12**: Operating systems and interpreting data with informed confidence

You have reached the summit of technical understanding. From here, everything builds on this foundation.

---

**Next Section:** Chapter 5: Understanding Flow Regimes and River Behavior

[VISUAL PLACEHOLDER: Comprehensive two-page visual summary showing: (1) Complete workflow diagram with all 9 steps illustrated, (2) Systems integration showing how all previous concepts connect, (3) Quality indicators checklist with visual examples, (4) Troubleshooting decision tree, (5) Real-world example summary, (6) Key formulas and factors, (7) Connection map to remaining manual chapters. Central message: "PIV/PTV - The Complete System: From Video to Discharge, Every Step Connected"]
