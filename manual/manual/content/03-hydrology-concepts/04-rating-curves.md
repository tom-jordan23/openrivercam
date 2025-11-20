# 3.4 Stage-Discharge Relationship (Rating Curve)

This section explains rating curves - the single most important concept for understanding how OpenRiverCam provides practical, continuous discharge estimates. If you understand only one technical concept from this manual, make it this one.

By the end of this section, you will understand:
- What a rating curve is and why it matters
- How rating curves are developed and established
- Using rating curves to convert water level into discharge estimates
- When and why rating curves need updating
- The limitations and uncertainty in rating curve estimates

---

## Starting With a Problem: Measuring Discharge is Hard

### The Challenge We Face

In Section 3.1, you learned that discharge equals velocity multiplied by area: Q = v × A. To know discharge at any moment, you must measure velocity at that moment. For OpenRiverCam, this means:

1. Camera tracks surface features
2. Software calculates velocity
3. Velocity combined with cross-sectional area gives discharge
4. This process runs continuously

This works - but it has challenges:

**Computational demand:** Processing video to track features requires computing power. Running this every few minutes continuously demands constant processing.

**Feature dependency:** The system needs visible tracers (foam, debris, ripples) on the water surface. If tracers are sparse, velocity measurement becomes uncertain.

**Quality variability:** Some conditions produce excellent velocity measurements (abundant tracers, good lighting). Other conditions produce marginal measurements (few tracers, poor lighting, extreme turbulence).

**The question:** Is there a simpler, more reliable way to estimate discharge continuously without measuring velocity every time?

**The answer:** Yes - if you can measure just the water level and convert it to discharge using a pre-established relationship. This relationship is called a rating curve.

[VISUAL PLACEHOLDER: Split diagram showing (1) "Direct Method" - measure velocity every time (complex, variable) and (2) "Rating Curve Method" - measure only water level (simple, reliable). Both produce discharge estimates.]

---

## The Restaurant Menu Analogy (Review and Expansion)

### A Familiar Concept

In Section 3.1, we briefly introduced the restaurant menu analogy. Let's expand it to fully understand rating curves.

**The menu concept:**

When you go to a restaurant, you look at the menu to find out prices. The menu tells you:
- Chicken curry → 150 pesos
- Vegetable stir-fry → 120 pesos
- Fried rice → 80 pesos

You do not need to recalculate the cost every time you order chicken curry. Someone already did the work of determining that chicken curry costs 150 pesos - considering ingredients, labor, overhead, and profit. That information is recorded on the menu. When you order, you simply read it from the menu.

**How this applies to rivers:**

A rating curve is a river's "menu" - it tells you:
- Water level 1.0 meter → Discharge approximately 15 m³/s
- Water level 1.5 meters → Discharge approximately 35 m³/s
- Water level 2.0 meters → Discharge approximately 65 m³/s

Once the rating curve exists, you do not need to measure velocity every time you want to know discharge. You simply:
1. Measure the current water level (easy and reliable)
2. Look up the corresponding discharge on the rating curve
3. You have your discharge estimate

**Creating the menu:**

Just as a restaurant must carefully calculate costs before printing the menu, creating a rating curve requires careful measurement work upfront. You must:
1. Measure discharge directly (using velocity measurement) at many different water levels
2. Plot these measurements to see the relationship
3. Establish the mathematical "menu" that converts any water level to discharge

Once created, the rating curve makes ongoing operations much simpler.

[VISUAL PLACEHOLDER: Restaurant menu on left showing items and prices. River rating "menu" on right showing water levels and discharge values, formatted similarly. Caption: "A rating curve is a conversion chart - like a menu that tells you discharge for any water level"]

---

## The Conversion Chart Analogy

### Another Way to Think About It

If the menu analogy doesn't resonate, think of a rating curve as a conversion chart - like converting between currencies or units.

**Currency conversion example:**

If you travel from the US to Europe, you need to convert dollars to euros. A conversion chart tells you:
- $10 → €9.20
- $50 → €46.00
- $100 → €92.00

You do not recalculate exchange rates every time you make a purchase. You refer to the conversion chart and get your answer instantly.

**Temperature conversion example:**

Converting Fahrenheit to Celsius:
- 32°F → 0°C
- 68°F → 20°C
- 86°F → 30°C

The mathematical relationship exists (C = 5/9 × (F - 32)), but rather than doing the math every time, you can simply look it up on a conversion chart.

**River discharge conversion:**

Converting water level (stage) to discharge:
- 1.0 m → 15 m³/s
- 1.5 m → 35 m³/s
- 2.0 m → 65 m³/s

The relationship exists because of the river's physical characteristics. Once you have established it through measurements, you can convert any water level to discharge instantly.

**The power of pre-established relationships:**

In all these cases, the hard work happens once (establishing the relationship), and then the easy lookups happen thousands of times. This is exactly how rating curves make continuous river monitoring practical.

[VISUAL PLACEHOLDER: Three conversion charts side by side - currency conversion, temperature conversion, and river stage-discharge conversion - showing similar table structures. Caption: "Rating curves work like familiar conversion charts - hard work upfront, easy use forever"]

---

## What Exactly is a Rating Curve?

### The Technical Definition (In Plain Language)

**Rating curve definition:**
A rating curve is a graph or equation showing the relationship between water level (called "stage") and discharge for a specific location on a river.

Let's break down each part:

**Water level (stage):**
- The depth or elevation of the water surface
- Measured in meters (or feet)
- Easy to measure with a simple staff gauge (a pole marked like a ruler)
- Can be measured automatically with pressure sensors or ultrasonic sensors
- Changes continuously as flow increases or decreases

**Discharge:**
- The volume of water flowing past per second (m³/s)
- What we ultimately care about for decisions
- Harder to measure directly (requires velocity measurement)
- What the rating curve estimates from water level

**Relationship:**
- For any given water level at a location, there is a corresponding discharge
- This relationship is not random - it is determined by the river's physical shape and characteristics
- The relationship is curved (not a straight line) for reasons we will explain
- The relationship is specific to one location - each site needs its own rating curve

**Specific location:**
- Rating curves are site-specific
- The curve for one river location cannot be used at another location
- Even moving 100 meters upstream or downstream changes the relationship
- This is because the river's shape and characteristics differ at each location

[VISUAL PLACEHOLDER: Simple rating curve graph - water level (0-3 m) on vertical axis, discharge (0-120 m³/s) on horizontal axis, with smooth curved line showing relationship. Several points marked and labeled. Caption: "A rating curve: the relationship between water level and discharge at a specific river location"]

---

## Why Rating Curves Are Curved (Not Straight Lines)

### Understanding the Non-Linear Relationship

Many people expect that if 1 meter of water depth produces 15 m³/s of discharge, then 2 meters should produce 30 m³/s (double the depth, double the flow). But rivers don't work this way. The relationship is curved, and discharge increases faster than water level.

Let's understand why:

### The Double Effect: Area AND Velocity Both Increase

Remember the fundamental equation from Section 3.1: **Q = v × A**

When water level rises, TWO things change:

**Effect 1: Cross-sectional area increases**
- Higher water level means more space filled with water
- If a river is 10 meters wide and water depth increases from 1 meter to 2 meters:
  - At 1 meter: Area might be 10 m²
  - At 2 meters: Area might be 25 m² (not 20 m² because river banks typically slope outward)
- Area often increases more than proportionally because river banks widen as you go higher

**Effect 2: Velocity usually increases**
- Deeper water generally flows faster than shallow water
- Friction with the riverbed affects a smaller proportion of the water column in deep water
- At 1 meter depth: Average velocity might be 1.0 m/s
- At 2 meters depth: Average velocity might be 1.5 m/s

**Combined effect:**
The two effects multiply:
- At 1 meter: Q = 1.0 m/s × 10 m² = 10 m³/s
- At 2 meters: Q = 1.5 m/s × 25 m² = 37.5 m³/s

Doubling the water level more than tripled the discharge (10 m³/s → 37.5 m³/s).

This multiplicative effect creates the curved relationship.

[VISUAL PLACEHOLDER: Three diagrams showing the same river cross-section at three water levels (low, medium, high). Each shows:
- Water level marked
- Cross-sectional area shaded and labeled (10 m², 18 m², 28 m²)
- Average velocity arrows (varying lengths)
- Calculated discharge
Demonstrate how both area and velocity increase, creating non-linear discharge growth]

### Real-World Numbers for a Typical River

Let's look at actual numbers from a real rating curve to see the curved relationship:

| Water Level | Cross-Section Area | Average Velocity | Discharge | Discharge Ratio |
|-------------|-------------------|------------------|-----------|-----------------|
| 0.5 m       | 8 m²              | 0.6 m/s          | 4.8 m³/s  | 1.0× (baseline) |
| 1.0 m       | 15 m²             | 1.0 m/s          | 15 m³/s   | 3.1× baseline   |
| 1.5 m       | 24 m²             | 1.4 m/s          | 34 m³/s   | 7.1× baseline   |
| 2.0 m       | 35 m²             | 1.8 m/s          | 63 m³/s   | 13.1× baseline  |
| 2.5 m       | 48 m²             | 2.2 m/s          | 106 m³/s  | 22.1× baseline  |

**Key observations:**

1. **Water level increased by 5 times** (0.5 m → 2.5 m)
2. **Discharge increased by 22 times** (4.8 m³/s → 106 m³/s)
3. **The relationship accelerates** - each 0.5 m increase in level produces larger discharge jumps
4. **Small level changes at high water mean large discharge changes** - this is why floods intensify so rapidly

### Why This Matters for Flood Warning

The curved relationship has critical implications:

**During normal conditions:**
- Water level changes slowly
- Discharge changes slowly
- You have time to respond

**As flood levels approach:**
- A small increase in water level (say, 20 cm) can mean a very large increase in discharge
- Flow can intensify rapidly
- This is why floods seem to "suddenly" become dangerous - small visible changes (water level) correspond to massive invisible changes (discharge)

Understanding that the relationship is curved helps you interpret what you see: when water is already high, every centimeter matters much more than when water is low.

[VISUAL PLACEHOLDER: Graph with water level on vertical axis and discharge on horizontal axis, showing curved relationship. Two equal vertical distances on the graph (representing equal water level increases) connected to horizontal distances showing discharge changes - small discharge change at low levels, huge discharge change at high levels. Caption: "Why floods intensify rapidly: equal water level changes produce very different discharge changes depending on starting level"]

---

## How Rating Curves Are Developed: The Measurement Campaign

### The Process Overview

Creating a rating curve requires measuring discharge at many different water levels. Think of it as creating the restaurant menu - you must carefully determine each item's price (each water level's corresponding discharge) before you can write the menu.

**The rating curve development process:**

1. Measure discharge directly at one water level
2. Record the water level at that moment
3. Create one point on the rating curve: "At level X, discharge is Y"
4. Repeat at many different water levels
5. Collect enough points to see the relationship pattern
6. Fit a mathematical curve through the points
7. Use the curve to estimate discharge for any water level

**How many measurements do you need?**

Minimum: 15-20 discharge measurements at different water levels
Better: 30-40 measurements
Ideal: 50+ measurements spanning the full range from low flow to flood conditions

**Why so many?**

- You need to capture the full range of flows (low, normal, high, flood)
- More measurements produce more accurate curves
- Measurements at many levels help you understand the shape of the relationship
- Multiple measurements at similar levels show you the uncertainty and variability

### Measuring Across the Range

The key challenge is measuring discharge at different water levels - especially very low and very high flows.

**Low flow measurements:**
- Usually easier and safer
- Can be done by wading if river is shallow
- Good conditions for ADCP or current meter
- Often done during dry season

**Normal flow measurements:**
- Moderately easy
- River at typical levels
- Good conditions for most measurement methods
- Most convenient time to measure

**High flow measurements:**
- More difficult and dangerous
- Wading may not be safe
- Boat-based ADCP may be risky
- Traditional methods may fail
- **This is where OpenRiverCam excels** - camera continues operating safely when traditional methods cannot

**Flood measurements:**
- Extremely difficult with traditional methods
- Very dangerous for personnel
- Equipment may be damaged
- **OpenRiverCam's major advantage** - continues measuring throughout floods when data is most critical

[VISUAL PLACEHOLDER: Timeline diagram showing measurement campaign over months/years. Points marked on a rating curve graph showing:
- Early measurements: low and normal flow (clustered)
- Later measurements: high flow (fewer, harder to get)
- Final measurements: flood events (rare but critical)
Caption: "Building a rating curve: collecting measurements across the full range of flow conditions"]

### OpenRiverCam's Approach

OpenRiverCam establishes rating curves through continuous operation:

**Phase 1: Initial measurements (first few months)**
- Camera measures velocity continuously
- Combined with water level to calculate discharge
- System operates during normal conditions
- Begin collecting data points automatically

**Phase 2: Capturing variability (through first year)**
- System continues operating through seasonal changes
- Automatically captures high flow events
- Records discharge and water level for each measurement
- Builds up database of measurements

**Phase 3: Rating curve development (after several months)**
- Enough measurements collected across different levels
- Software can fit a rating curve through the points
- Curve defines the stage-discharge relationship

**Phase 4: Operational mode (ongoing)**
- Once curve is established, can estimate discharge from water level alone
- Simpler than measuring velocity every time
- More reliable (water level measurement is very reliable)
- Continue velocity measurements periodically to verify curve remains accurate

**The advantage of continuous operation:**

Traditional methods require teams to return to the site many times at different flow levels - this takes months or years and requires luck to capture high flows. OpenRiverCam operates continuously, automatically capturing all flow levels as they occur naturally. The rating curve develops organically through normal operation.

[VISUAL PLACEHOLDER: Diagram showing OpenRiverCam's rating curve development over time. X-axis: months. Y-axis: discharge range. Points accumulate over time, filling in the rating curve. Different colors for low/normal/high flow measurements. Caption: "OpenRiverCam builds rating curves automatically through continuous operation"]

---

## Using Rating Curves: From Water Level to Discharge

### The Practical Workflow

Once a rating curve exists, estimating discharge becomes straightforward:

**Step 1: Measure current water level**
- Read from staff gauge (visual)
- Or get from automated sensor (pressure transducer, ultrasonic)
- Record: "Water level is currently 1.73 meters"

**Step 2: Look up discharge on the rating curve**
- Find 1.73 m on the water level axis
- Follow across to the rating curve line
- Read the corresponding discharge value
- Result: "Discharge is approximately 42 m³/s"

**Step 3: Use the discharge for decisions**
- Is 42 m³/s above flood warning threshold?
- Is it adequate for water supply needs?
- Is it safe for planned operations?

That's it. Three simple steps from water level to actionable information.

### A Worked Example with Real Numbers

Let's walk through a complete example using the rating curve we've been developing.

**Situation:**
A humanitarian organization operates a refugee camp along a river. They have established an OpenRiverCam system and developed a rating curve through several months of operation. They need to make decisions based on current river flow.

**Current observation:**
Staff gauge reading: 1.85 meters

**Rating curve data:**
The established rating curve for this site shows:

| Water Level (m) | Discharge (m³/s) |
|-----------------|------------------|
| 1.0             | 15               |
| 1.2             | 20               |
| 1.4             | 26               |
| 1.6             | 33               |
| 1.8             | 41               |
| 2.0             | 50               |
| 2.2             | 60               |

**Finding the discharge for 1.85 m:**

Since 1.85 m falls between 1.8 m (41 m³/s) and 2.0 m (50 m³/s), we can interpolate:

- 1.85 is 1/4 of the way between 1.8 and 2.0
- Discharge at 1.85 m ≈ 41 + (0.25 × (50 - 41))
- Discharge ≈ 41 + 2.25 = 43.25 m³/s
- **Rounded: approximately 43 m³/s**

(In practice, software does this calculation automatically - you simply enter water level and get discharge instantly.)

**Making decisions with this information:**

**Decision 1: Water supply**
- Camp needs 400 m³/day = 0.0046 m³/s
- River provides 43 m³/s
- Camp uses less than 0.01% of river flow
- **Decision:** Water extraction is highly sustainable

**Decision 2: Flood warning**
- Historical data shows flooding begins at approximately 85 m³/s
- Current flow is 43 m³/s (about 50% of flood threshold)
- **Decision:** No immediate flood concern, but continue monitoring

**Decision 3: River crossing operations**
- Disaster response team needs to establish a temporary footbridge
- Experience shows crossings are safe below 60 m³/s
- Current flow is 43 m³/s
- **Decision:** Safe to proceed with river crossing operations

**The power of the rating curve:**

With one simple water level reading (1.85 m), the rating curve provided the discharge estimate (43 m³/s) that enabled three separate operational decisions. Without the rating curve, each decision would require complex velocity measurements and calculations.

[VISUAL PLACEHOLDER: Visual workflow showing:
1. Staff gauge photo with water at 1.85 m
2. Rating curve graph with 1.85 m marked, line extending to curve, then to discharge axis showing 43 m³/s
3. Three decision boxes showing water supply (green check), flood warning (yellow caution), and river crossing (green check)
Caption: "Using the rating curve: one simple measurement enables multiple operational decisions"]

---

## Mathematical Representation (Optional Detail)

### For Those Who Want to Know the Math

You do not need to understand the mathematics to use rating curves - the software handles it all. But for those interested, here is how rating curves are mathematically expressed.

**The standard rating curve equation:**

Q = a × (h - h₀)ᵇ

Where:
- Q = discharge (m³/s)
- h = current water level (m)
- h₀ = water level at zero flow (m) - the level where discharge would be zero
- a = coefficient related to channel shape and roughness
- b = exponent (usually between 1.5 and 3.0) - determines the curve shape

**Example with numbers:**

For a specific river, the rating curve might be:

Q = 8.5 × (h - 0.30)²·¹

If current water level h = 1.80 m:
- Q = 8.5 × (1.80 - 0.30)²·¹
- Q = 8.5 × (1.50)²·¹
- Q = 8.5 × 2.46
- Q = 20.9 m³/s

**Why the exponent is greater than 1:**

The exponent b is typically 1.5 to 3.0 - this creates the curved relationship we discussed. An exponent of 2.0 means discharge increases with the square of the water depth above zero flow. This captures the combined effect of increasing area and increasing velocity.

**Logarithmic form:**

Engineers often work with rating curves in logarithmic form:

log(Q) = log(a) + b × log(h - h₀)

This converts the curved relationship into a straight line on log-log graph paper, making it easier to see if the data fits the expected pattern and to identify outliers.

**Again: you don't need to do this math**

Modern software automatically:
- Fits the rating curve equation to your measurements
- Calculates the coefficients a and b
- Computes discharge for any water level you enter
- Handles uncertainties and confidence intervals

Understanding the concept is important. Doing the calculations manually is not.

[VISUAL PLACEHOLDER: Two graphs side by side:
1. Normal rating curve - curved line on regular graph
2. Log-log rating curve - straight line on log-log graph
Both showing same data, different representations. Caption: "Mathematical representations of rating curves - engineers use log-log plots to verify the relationship, but software handles the calculations"]

---

## Rating Curve Uncertainty and Confidence

### Understanding That Estimates Are Not Perfect

Rating curves provide estimates, not exact measurements. It is important to understand the uncertainty and use it appropriately.

### Sources of Uncertainty

**Measurement uncertainty:**
- The original discharge measurements used to create the curve have uncertainty (typically ±5-20% depending on method)
- Multiple measurements at similar levels may show variation
- This variation carries through to the rating curve

**Curve fitting uncertainty:**
- The mathematical curve fit through the points is an approximation
- Points may scatter around the fitted line
- The curve represents an average relationship

**Extrapolation uncertainty:**
- Rating curves are most accurate within the range of measured flows
- Estimating discharge outside the range of measurements (extrapolation) is less certain
- If you measured flows up to 100 m³/s, estimating 150 m³/s involves extrapolation

**Temporal changes:**
- Rivers change over time (we will discuss this next)
- The rating curve may become less accurate as the channel changes
- Periodic verification is needed

**Typical uncertainty ranges:**

| Condition | Typical Uncertainty |
|-----------|---------------------|
| Within measured range, stable channel, recent curve | ±10-15% |
| Slight extrapolation, stable channel | ±15-25% |
| Significant extrapolation | ±25-40% |
| Curve several years old, no verification | ±20-50% |
| After major flood that changed channel | Rating curve invalid until updated |

### Using Uncertainty Appropriately

**For operational decisions, ±15% uncertainty is usually fine:**

"Is the river at 80 m³/s or 92 m³/s?" - for most humanitarian decisions, this difference does not matter. You need to know:
- Is it below normal flow (< 40 m³/s)?
- Is it approaching flood levels (60-90 m³/s)?
- Is it in flood (> 90 m³/s)?

A ±15% uncertainty does not prevent you from making these distinctions.

**When higher accuracy matters:**

If legal water allocation requires knowing discharge to within ±5%, a rating curve may not be sufficient. You would need direct discharge measurements for critical decisions.

For humanitarian applications, rating curve accuracy is almost always adequate.

**Express uncertainty when reporting:**

Rather than saying "The river is at 87.3 m³/s," say "The river is at approximately 85-90 m³/s" or "The river is at about 87 m³/s."

This conveys the appropriate level of precision and avoids false confidence.

[VISUAL PLACEHOLDER: Rating curve graph showing:
- Points (measurements) scattered around the fitted curve
- Confidence bands (shaded region) around the curve showing uncertainty
- "Well-constrained region" (many measurements) with narrow bands
- "Extrapolated region" (no measurements) with wide bands
Caption: "Rating curve uncertainty: estimates are less certain when extrapolating beyond measured flows or when measurements are sparse"]

---

## When Rating Curves Need Updating

### Rivers Change, So Curves Must Change Too

Rating curves are not permanent. They represent the relationship between stage and discharge at a given time, but rivers are dynamic systems that change over time.

### Why Rivers Change

**Natural changes:**

1. **Major floods:**
   - Scour (dig out) the riverbed, making it deeper
   - Deposit sediment, making it shallower
   - Erode banks, making the channel wider
   - Move large rocks or woody debris
   - Completely reshape the channel in extreme cases

2. **Seasonal vegetation:**
   - Aquatic plants grow in summer, increasing roughness (slowing flow)
   - Plants die back in winter, decreasing roughness (faster flow)
   - Affects primarily low-flow conditions

3. **Bank erosion:**
   - Gradual widening of the channel over years
   - Changes cross-sectional shape
   - Alters area-stage relationship

4. **Sediment deposition:**
   - Gradual filling of the channel with sediment
   - Raises the bed level
   - Reduces cross-sectional area

**Human-induced changes:**

1. **Upstream development:**
   - New dam changes flow patterns and sediment transport
   - Affects natural flow regime
   - Changes sediment dynamics

2. **Channel modifications:**
   - Dredging to deepen the channel
   - Bank stabilization structures
   - Flow diversion structures
   - Direct alteration of channel shape

3. **Land use changes:**
   - Deforestation increases sediment load
   - Urban development changes runoff patterns
   - Agricultural practices affect erosion

### Signs Your Rating Curve Needs Updating

**Clear indicators:**

1. **After a major flood:**
   - If you had significant flooding (say, >10 year return period), assume the channel changed
   - Update rating curve soon after flood recedes

2. **Systematic deviations:**
   - If recent discharge measurements consistently differ from rating curve predictions
   - If predicted discharge is always higher or always lower than measured
   - This indicates the relationship has shifted

3. **Visual channel changes:**
   - If you can see that the riverbed or banks have changed
   - New gravel bar formed, bank collapsed, channel widened, etc.

4. **Time-based trigger:**
   - If no verification for 2-3 years, assume curve needs checking
   - Even without obvious changes, gradual evolution occurs

**How to check if your curve is still good:**

1. Measure discharge directly (using velocity measurement) at several water levels
2. Compare measured discharge to what rating curve predicts for those levels
3. If measured and predicted values differ by >15-20%, rating curve needs updating

**How often to verify:**

- **Annually:** Minimum for operational systems
- **After major floods:** Within weeks of significant events
- **Bi-annually:** Better practice for critical applications
- **Continuously:** OpenRiverCam approach - ongoing velocity measurements allow automatic detection of curve shifts

### Updating Rating Curves

**Two approaches:**

**Full re-establishment:**
- Conduct new measurement campaign at many water levels
- Develop entirely new rating curve
- Time-consuming but gives complete confidence
- Necessary if channel completely reshaped

**Adjustment/shift:**
- Conduct a few verification measurements
- Determine systematic shift (e.g., all discharges now 10% higher)
- Apply adjustment factor to existing curve
- Faster but less thorough
- Appropriate for minor changes

**OpenRiverCam advantage:**

Because OpenRiverCam continues measuring velocity periodically (even while using the rating curve for most estimates), it can automatically detect when the curve shifts and alert you that recalibration is needed. Traditional stage-only systems cannot do this - they rely on manual verification schedules.

[VISUAL PLACEHOLDER: Before/after comparison showing:
- Original rating curve (blue line)
- New measurement points after a flood (red dots)
- Updated rating curve (red line)
- Annotation showing how the relationship shifted
Caption: "Rating curve update: after a major flood changed the channel, new measurements establish an updated curve"]

---

## Rating Curves in OpenRiverCam: The Hybrid Approach

### Best of Both Worlds

OpenRiverCam uses a hybrid approach that combines the reliability of rating curves with the verification power of ongoing velocity measurement.

### Phase 1: Initial Operation (First 3-6 Months)

**Direct velocity measurement:**
- Camera measures velocity for every flow estimate
- Combined with water level and cross-section to calculate discharge: Q = v × A
- More computationally intensive
- Works even before rating curve exists
- Builds database of discharge vs. stage measurements

**Outcome:**
- System provides discharge estimates from day one
- No need to wait for rating curve before getting useful data
- Automatically accumulating measurements to build rating curve

### Phase 2: Rating Curve Development (After 3-6 Months)

**Automatic curve fitting:**
- Software analyzes accumulated measurements
- Fits rating curve through the data points
- Establishes stage-discharge relationship
- Calculates uncertainty and confidence intervals

**Validation:**
- Check that curve fits measurements well
- Verify physically reasonable relationship
- Compare with any external measurements if available

**Outcome:**
- Rating curve established
- Ready to transition to rating-curve-based operation

### Phase 3: Rating Curve Mode (Ongoing)

**Primary mode - stage-based estimates:**
- For most time periods, discharge estimated from water level alone using rating curve
- Simple, reliable, low computational demand
- Water level measurement is very reliable (less dependent on tracers and conditions)

**Periodic verification - velocity measurements:**
- System continues measuring velocity occasionally (e.g., once per day or week)
- Compares velocity-based discharge with rating-curve estimate
- Checks if relationship still holds
- Alerts if systematic deviation detected

**Benefits:**
- Reliability: Rating curve provides consistent estimates even when velocity measurement conditions are poor
- Efficiency: Lower computational demand than continuous velocity measurement
- Verification: Ongoing velocity measurements detect if curve needs updating
- Adaptability: Can automatically adjust curve if gradual changes detected

### Phase 4: Automatic Curve Updates (Advanced)

**Continuous learning:**
- System accumulates new velocity-based measurements over time
- Periodically refits rating curve with updated data
- Gradually adapts to channel changes
- Maintains accuracy over years of operation

**Alert system:**
- If sudden deviation detected (e.g., after a flood), alerts operator
- Recommends increased verification measurements
- Suggests when recalibration needed

[VISUAL PLACEHOLDER: Flowchart showing OpenRiverCam's rating curve approach:
- Start: Direct measurement (Q = v × A)
- After 3-6 months: Develop rating curve
- Ongoing: Primary mode (stage → discharge via curve) + Periodic verification (velocity measurement)
- Continuous: Detect changes, alert if update needed
- Arrows showing the cycle and feedback loops
Caption: "OpenRiverCam's hybrid approach: combining rating curve simplicity with velocity measurement verification"]

---

## Practical Example: Rating Curve Through a Year

### Following a Real Deployment

Let's walk through how a rating curve develops and is used over a full year of OpenRiverCam operation.

**Location:** Medium river near humanitarian settlement
**Purpose:** Flood early warning and water resource monitoring

### Month 1-2: Initial Operation (Dry Season)

**Activity:**
- OpenRiverCam installed and operational
- Measures velocity directly for each discharge estimate
- Water levels during this period: 0.8-1.2 m (dry season low flow)
- Discharge measurements: 10-22 m³/s

**Measurements collected:**
- 45 discharge measurements at water levels between 0.8-1.2 m
- All in the low-flow range
- Building initial data points

**Status:**
- No rating curve yet (need measurements across wider range)
- System provides discharge estimates, but using direct measurement
- Waiting for higher flows to expand measurement range

### Month 3-4: Early Wet Season

**Activity:**
- First rains begin, water levels rise
- Water levels: 1.2-1.8 m (normal flow range)
- Discharge: 22-50 m³/s

**Measurements collected:**
- 38 additional discharge measurements at water levels between 1.2-1.8 m
- Now have measurements spanning 0.8-1.8 m (low to normal flow)
- Total: 83 measurements

**Status:**
- Still using direct velocity measurement for all estimates
- Beginning to see the curved relationship emerge
- Need high-flow measurements to complete curve

### Month 5: First Flood Event

**Activity:**
- Significant rain, river rises to flood levels
- Water levels reach 2.5 m (highest level yet)
- Discharge estimates: up to 110 m³/s
- **Critical moment:** Traditional gauges might fail or be inaccessible, but OpenRiverCam continues operating safely

**Measurements collected:**
- 12 discharge measurements at high water levels (1.8-2.5 m)
- Captured the flood peak and recession
- Total: 95 measurements spanning 0.8-2.5 m

**Status:**
- Now have measurements across full range of interest (dry season to flood)
- Sufficient data to develop rating curve
- Software analyzes data and fits curve

**Rating curve established:**
- Q = 9.2 × (h - 0.25)^2.3
- Where Q is discharge (m³/s), h is water level (m), 0.25 m is zero-flow level
- Uncertainty: ±12% within measured range (0.8-2.5 m)

[VISUAL PLACEHOLDER: Graph showing accumulated measurement points over 5 months:
- Months 1-2: cluster of points at low levels (0.8-1.2 m)
- Months 3-4: points expanding to normal levels (1.2-1.8 m)
- Month 5: points extending to high levels (1.8-2.5 m)
- Fitted rating curve through all points
Caption: "Building a rating curve: measurements accumulate over months, spanning low to high flows"]

### Month 6-11: Rating Curve Mode

**Activity:**
- System now operates primarily in rating curve mode
- Discharge estimated from water level using established curve
- Periodic velocity measurements (once per week) to verify curve accuracy
- Computational demand reduced
- More reliable continuous estimates (less dependent on tracer availability)

**During this period:**
- Water levels varied from 0.9 m (dry season return) to 2.1 m (another moderate flood)
- Rating curve provided discharge estimates for all conditions
- Weekly velocity measurements confirmed curve accuracy (deviations <10%)

**Example operational use:**

**Situation (Month 8):** Water level rising during rainstorm
- Hour 0: Stage 1.5 m → Rating curve → Discharge ~35 m³/s (normal flow)
- Hour 6: Stage 1.8 m → Rating curve → Discharge ~50 m³/s (high flow, approaching watch level)
- Hour 12: Stage 2.0 m → Rating curve → Discharge ~65 m³/s (warning level, alert issued to community)
- Hour 18: Stage 2.2 m → Rating curve → Discharge ~80 m³/s (flood imminent, evacuation triggered)

The rating curve enabled real-time decision-making throughout the event, with simple water level measurements instantly converted to actionable discharge information.

### Month 12: Major Flood and Curve Verification

**Activity:**
- Largest flood of the year
- Water level reaches 2.8 m (exceeds previous maximum)
- Discharge estimated at 145 m³/s (extrapolation beyond measured range - higher uncertainty)

**Post-flood check:**
- Visual inspection: riverbed appears changed (some bank erosion, new gravel deposits)
- Verification measurements taken at three water levels:
  - 1.2 m: Rating curve predicted 22 m³/s, velocity measurement showed 20 m³/s (9% lower)
  - 1.5 m: Rating curve predicted 35 m³/s, velocity measurement showed 31 m³/s (11% lower)
  - 1.8 m: Rating curve predicted 50 m³/s, velocity measurement showed 44 m³/s (12% lower)

**Analysis:**
- Systematic 10-12% under-prediction
- Flood changed channel (slightly wider/deeper)
- For same water level, discharge is now slightly less

**Action:**
- Adjustment factor applied: multiply rating curve estimates by 0.89 to correct
- Alternatively, collect new measurements to re-establish curve completely
- Organization chose adjustment factor (simpler, adequate accuracy)

**Updated curve:**
- Q_new = 0.89 × 9.2 × (h - 0.25)^2.3
- Verification measurements now match within 5%
- System continues operating with updated curve

[VISUAL PLACEHOLDER: Timeline graphic showing full year:
- Months 1-5: Building curve (points accumulating)
- Months 6-11: Using curve (smooth operation, periodic verification points)
- Month 12: Major flood (highest point), then verification showing shift, adjustment applied
Caption: "One year with a rating curve: development, use, verification, and update"]

---

## Common Misunderstandings About Rating Curves

### Clearing Up Confusion

**Misunderstanding 1: "Rating curves are exact mathematical laws"**

**Why this seems right:**
The rating curve is expressed as a mathematical equation, which seems precise and exact.

**Why this is wrong:**
Rating curves are empirical approximations based on measurements with uncertainty. They describe the average relationship, but nature has variability. Think of a rating curve like an average weather forecast - useful for planning, but not perfectly precise.

**The correct understanding:**
Rating curves provide estimates with typical uncertainties of ±10-20%. This is adequate for operational decisions but not laboratory precision.

---

**Misunderstanding 2: "Once you have a rating curve, you never need to measure velocity again"**

**Why this seems right:**
The rating curve converts water level to discharge, so you only need to measure water level.

**Why this is incomplete:**
Rating curves change when rivers change. You need periodic velocity measurements to verify the curve is still accurate. Without verification, you don't know if channel changes have invalidated your curve.

**The correct understanding:**
Rating curves make ongoing operations simpler (measure level, not velocity, most of the time), but periodic verification is essential to maintain accuracy.

---

**Misunderstanding 3: "I can use a rating curve from a similar river nearby"**

**Why this seems right:**
If two rivers look similar, their rating curves should be similar too.

**Why this is wrong:**
Rating curves are site-specific. Even on the same river, moving 100 meters changes the relationship because cross-section shape changes. Small differences in channel shape produce large differences in the stage-discharge relationship.

**The correct understanding:**
Every monitoring location needs its own rating curve developed from measurements at that specific location.

---

**Misunderstanding 4: "Water level and discharge are the same thing"**

**Why this seems right:**
Rating curves allow you to convert water level to discharge, so they must be the same concept.

**Why this is wrong:**
Water level (stage) is how deep the water is. Discharge is how much water is flowing past. They are related but different quantities. A wide, shallow river and a narrow, deep river could both have the same water level but very different discharge.

**The correct understanding:**
Water level is what you measure (depth). Discharge is what you estimate from water level using the rating curve (flow volume).

---

**Misunderstanding 5: "Higher accuracy in rating curves always means better decisions"**

**Why this seems right:**
More accurate information should enable better decisions.

**Why this is misleading:**
For most humanitarian decisions, knowing discharge ±15% vs. ±5% does not change what you decide. The value is in having objective information continuously, not in extreme precision. A ±15% rating curve that operates continuously is vastly better for decision-making than a ±5% direct measurement that happens once per week.

**The correct understanding:**
Appropriate accuracy, continuous availability, and timely information matter more than maximum precision for operational humanitarian decisions.

[VISUAL PLACEHOLDER: Five panels illustrating each misunderstanding with "Common Misconception" and "Reality" side-by-side visual comparisons]

---

## Rating Curves and Flood Warning: A Critical Application

### Why Rating Curves Make Flood Warning Practical

Let's examine in detail how rating curves enable effective flood early warning - one of the most important humanitarian applications of OpenRiverCam.

### The Challenge of Flood Warning

Effective flood warning requires:

1. **Knowing when floods are coming** - detecting rising water
2. **Knowing how severe** - distinguishing minor high water from dangerous flooding
3. **Reliable operation during events** - continuing to function during the flood itself
4. **Simple interpretation** - field staff can understand the data and make decisions
5. **Continuous monitoring** - floods can happen at any time, including night

Rating curves address all five requirements:

### Detecting Rising Water

**Without rating curves:**
You see water level rising, but what does it mean?
- Level rising from 1.5 m to 1.7 m
- Is this normal variation or the start of flooding?
- How concerned should you be?

**With rating curves:**
Convert levels to discharge for context:
- 1.5 m → 35 m³/s (normal high flow)
- 1.7 m → 45 m³/s (20% increase - this is significant but not yet dangerous)
- Historical data shows flooding typically begins above 85 m³/s
- Current flow is about 50% of flood level
- **Interpretation:** Rising but not yet dangerous; increase monitoring frequency

### Setting Warning Thresholds

**Discharge-based thresholds are more meaningful than level-based thresholds:**

**Level-based approach:**
- "Warning when water reaches 2.3 meters"
- But what does 2.3 meters mean?
- Different rivers flood at different levels
- Communicating "2.3 meters" to communities is abstract

**Discharge-based approach using rating curve:**
- Establish from historical records: flooding begins when discharge exceeds 85 m³/s
- Convert to water level using rating curve: 85 m³/s corresponds to 2.15 m at this location
- Set alert at 2.15 m
- But communicate to staff in terms of discharge: "flow approaching flood threshold"

**Multi-level warning system example:**

| Water Level | Discharge | Alert Level | Actions |
|-------------|-----------|-------------|---------|
| < 1.8 m     | < 50 m³/s | Green - Normal | Routine monitoring |
| 1.8-2.0 m   | 50-65 m³/s | Yellow - Watch | Increase monitoring, inform community leaders |
| 2.0-2.15 m  | 65-85 m³/s | Orange - Advisory | Prepare evacuation plans, move vulnerable assets |
| > 2.15 m    | > 85 m³/s | Red - Warning | Begin evacuation, activate response procedures |

The rating curve makes these thresholds practical - simple water level measurements trigger clear actions based on the discharge implications.

### Continuous Reliable Operation

**During flood events:**

**Challenge:** Velocity measurement can become difficult during extreme conditions
- Very turbulent water with inconsistent flow patterns
- Possible debris blocking camera view
- Lighting may be poor (storms, nighttime)

**Rating curve solution:**
- Water level measurement is very reliable regardless of conditions
- Pressure sensor or ultrasonic gauge works in all conditions
- Rating curve converts level to discharge even when velocity measurement would struggle
- System continues providing estimates throughout the event

**This is critical:** The time when data is most needed (during the flood) is precisely when direct velocity measurement is most challenging. Rating curves provide resilience when it matters most.

### Simple Field Interpretation

**For field staff:**

Imagine you are a humanitarian field officer, not a hydrologist. During a potential flood event, you receive updates:

**Update using raw data:**
"Camera tracking 347 surface features at average velocity 2.3 m/s with standard deviation 0.4 m/s, cross-sectional area calculated at 38 m² based on current stage..."

**Update using rating curve:**
"River flow currently 88 m³/s - just above flood warning threshold of 85 m³/s. Recommend activating evacuation procedures for low-lying areas."

The rating curve enables simplified communication focused on actionable information.

### Real-World Example: Flood Event Timeline

**Context:** Community flood warning system using OpenRiverCam with established rating curve

**Day 1 - Morning:**
- Water level: 1.6 m → Discharge: 38 m³/s (normal)
- Status: Green
- Forecast: Heavy rain expected in catchment

**Day 1 - Evening:**
- Water level: 1.9 m → Discharge: 58 m³/s (rising)
- Status: Yellow (watch level)
- Action: Inform community leaders, increase monitoring to hourly updates

**Day 2 - Early Morning (2 AM):**
- Water level: 2.1 m → Discharge: 72 m³/s (continued rise)
- Status: Orange (advisory level)
- Action: Wake emergency coordinator, prepare evacuation sites, move mobile assets to high ground

**Day 2 - Morning (6 AM):**
- Water level: 2.2 m → Discharge: 88 m³/s (exceeds flood threshold)
- Status: Red (warning level)
- Action: Begin evacuation of low-lying areas, activate full response plan

**Day 2 - Midday (12 PM):**
- Water level: 2.4 m → Discharge: 105 m³/s (flood peak)
- Status: Red
- Action: Evacuation complete, monitor for further rise

**Day 2 - Evening (6 PM):**
- Water level: 2.3 m → Discharge: 96 m³/s (beginning to recede)
- Status: Red (still above threshold)
- Action: Monitor recession, do not return yet

**Day 3 - Morning:**
- Water level: 2.0 m → Discharge: 65 m³/s (recession continues)
- Status: Orange (below flood threshold but still high)
- Action: Assess damage, plan safe return

**Day 3 - Evening:**
- Water level: 1.8 m → Discharge: 50 m³/s (returning toward normal)
- Status: Yellow
- Action: Begin safe return to evacuated areas

**Day 4:**
- Water level: 1.5 m → Discharge: 35 m³/s (normal levels)
- Status: Green
- Action: Resume normal operations

**The rating curve made this possible:**
- Simple, reliable water level measurements converted to meaningful discharge values
- Clear thresholds enabled decisive action
- System operated continuously throughout the event
- Field staff could interpret the data without hydrological expertise

[VISUAL PLACEHOLDER: Timeline graphic showing the flood event with:
- X-axis: Time (Day 1 morning through Day 4)
- Y-axis: Discharge (m³/s)
- Line showing discharge rise and fall
- Color-coded zones (green/yellow/orange/red)
- Action annotations at key points
Caption: "Flood event with rating curve-based early warning: clear thresholds enable timely, decisive actions"]

---

## Summary: Key Concepts to Remember

**What a rating curve is:**
- A relationship between water level (stage) and discharge for a specific river location
- Like a conversion chart or restaurant menu - look up discharge for any water level
- Enables simple water level measurements to provide discharge estimates

**Why the relationship is curved:**
- Both cross-sectional area AND velocity increase as water level rises
- These effects multiply, creating non-linear discharge growth
- Small water level changes at high levels mean large discharge changes - why floods intensify rapidly

**How rating curves are developed:**
- Measure discharge at many different water levels
- Plot the relationship
- Fit a mathematical curve through the measurements
- Need 15-50+ measurements spanning low to high flows
- OpenRiverCam builds curves automatically through continuous operation

**Using rating curves:**
- Measure current water level (simple and reliable)
- Look up corresponding discharge on the curve
- Use discharge for operational decisions
- Much simpler than measuring velocity continuously

**When curves need updating:**
- After major floods that reshape the channel
- If verification measurements show systematic deviations
- At least every 2-3 years for routine verification
- Rivers change, so curves must be updated to remain accurate

**Uncertainty and limitations:**
- Rating curves provide estimates, not exact measurements
- Typical uncertainty ±10-20% within measured range
- Higher uncertainty when extrapolating beyond measured flows
- Adequate accuracy for most humanitarian operational decisions

**OpenRiverCam's hybrid approach:**
- Start with direct velocity measurement
- Develop rating curve after collecting measurements across flow range
- Use rating curve for routine continuous estimates (simple, reliable)
- Continue periodic velocity measurements to verify curve accuracy
- Detect and adapt to channel changes over time

**Why rating curves matter:**
- Make continuous monitoring practical and reliable
- Enable flood warning with clear thresholds
- Simplify field operations and interpretation
- Provide resilient operation during extreme events when velocity measurement is difficult
- Critical bridge between easy-to-measure water level and decision-relevant discharge

**The big picture:**
Rating curves are what make OpenRiverCam practical for humanitarian operations. Direct velocity measurement establishes the curve and verifies accuracy. The curve enables simple, continuous, reliable discharge estimates that field staff can use confidently for life-safety decisions.

This is THE concept that makes river monitoring accessible to non-specialists. Master this, and you understand how OpenRiverCam works.

---

**Next Section:** [3.5 Understanding Uncertainty and Data Quality](05-uncertainty-and-quality.md)

[VISUAL PLACEHOLDER: One-page summary infographic with:
- Center: Rating curve graph showing curved relationship
- Surrounding sections: "What it is" (conversion chart analogy), "Why curved" (area + velocity effects), "How developed" (measurement campaign), "How used" (level → discharge → decision), "When to update" (after floods, periodic verification)
- Bottom: "Rating curves make continuous monitoring practical"
- Icons and minimal text for visual clarity]
