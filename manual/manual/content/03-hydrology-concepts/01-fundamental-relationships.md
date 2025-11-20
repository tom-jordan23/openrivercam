# 3.1 Fundamental Relationships: Velocity, Area, Flow, and Discharge

This section explains the core hydrological concepts that make OpenRiverCam work. If you are not a hydrologist or engineer, do not worry - these concepts are simpler than they sound. We will build your understanding from everyday experiences you already have.

By the end of this section, you will understand:
- What river discharge means and why it matters
- How velocity and cross-sectional area combine to create flow
- Why we measure each component
- How these measurements inform humanitarian decisions

---

## Starting with What You Already Know

### The Water Hose Analogy

You have used a garden hose. When you turn the tap, water flows out. If you want more water to fill a bucket faster, you can:
1. Turn the tap higher to make the water come out faster
2. Use a hose with a wider opening

This simple experience contains the entire foundation of river flow measurement:
- **Velocity** = how fast the water moves (turning the tap higher)
- **Area** = how big the opening is (using a wider hose)
- **Flow** = how much water you get (how fast the bucket fills)

Rivers work exactly the same way. A river is just a very large hose lying on its side, with water flowing through it.

[VISUAL PLACEHOLDER: Split illustration showing garden hose on left, river cross-section on right, with arrows showing velocity and area labeled identically on both]

### The Highway Traffic Analogy

Think about traffic on a highway. How many vehicles pass a point in one hour depends on:
1. **How fast the vehicles are moving** - 30 km/h in a traffic jam versus 100 km/h on an open road
2. **How many lanes the highway has** - a 2-lane road versus a 6-lane highway

Even if vehicles move slowly, many vehicles still pass if the highway has many lanes. Even if the highway is narrow, many vehicles still pass if they move very fast. The total number of vehicles passing equals speed multiplied by the number of lanes.

Rivers work identically. The amount of water passing a point depends on how fast the water moves and how much space (area) the water fills.

---

## The Fundamental Equation: Q = v × A

### Breaking Down the Components

The relationship between velocity, area, and flow is captured in one simple equation:

**Q = v × A**

Where:
- **Q** = Discharge (the total flow)
- **v** = Velocity (how fast the water moves)
- **A** = Cross-sectional area (how much space the water fills)

Let's understand each component.

### Discharge (Q): How Much Water is Flowing

**What it is:**
Discharge is the volume of water flowing past a point each second. It is measured in cubic meters per second (m³/s) or sometimes liters per second (L/s).

**Why "discharge" and not just "flow"?**
Hydrologists use the technical term "discharge," but "flow" means the same thing. We will use both terms interchangeably. When you see "discharge," think "how much water is flowing."

**Making it concrete:**
- 1 cubic meter = 1,000 liters (think of a cube 1 meter on each side, filled with water)
- If discharge is 10 m³/s, imagine 10 of these cubes flowing past every single second
- That is 10,000 liters per second - enough to fill a small swimming pool in less than a minute

**Real-world numbers:**
- Small stream: 0.5-5 m³/s
- Medium river (like those near refugee camps): 10-100 m³/s
- Large river (like the Mekong during normal flow): 1,000-5,000 m³/s
- Major flood on large river: 10,000+ m³/s

**Why discharge matters in humanitarian contexts:**
- **Flood warning**: When discharge exceeds certain levels, flooding begins
- **Water supply**: You need to know if the river has enough flow to supply camp needs
- **Infrastructure safety**: Bridges and water intakes are designed for specific discharge levels
- **Shared resources**: Fair water allocation requires knowing how much water is available

[VISUAL PLACEHOLDER: Diagram showing cubes of water (1m³ each) flowing past a point in a river, with "10 m³/s = 10 cubes per second = 10,000 liters per second" labeled]

### Velocity (v): How Fast the Water is Moving

**What it is:**
Velocity is the speed at which water moves downstream. It is measured in meters per second (m/s).

**Making it concrete:**
- Walking speed: about 1.5 m/s (you could walk alongside the water and keep pace)
- Jogging speed: about 3 m/s (you would need to jog to keep up with the water)
- Running speed: about 5-6 m/s (you would struggle to keep up even at full sprint)

**Real-world river velocities:**
- Very slow flow (pond-like): 0.1-0.3 m/s
- Slow river (typical low flow): 0.3-0.8 m/s
- Medium flow (typical normal conditions): 0.8-1.5 m/s
- Fast flow (high water, beginning of flood): 1.5-3 m/s
- Very fast flow (flood conditions): 3-6 m/s
- Extreme flow (dangerous flood): 6+ m/s

**Why it varies:**
Water does not move at the same speed everywhere in a river:
- **Surface water** moves faster than water near the bottom (friction with the riverbed slows deep water)
- **Center of the river** moves faster than water near the banks (friction with the sides slows edge water)
- **Straight sections** move faster than curved sections
- **Narrow sections** often move faster than wide sections

When we measure velocity, we are typically interested in the average velocity - the typical speed throughout the entire river cross-section.

**The surface velocity adjustment:**
OpenRiverCam measures the velocity at the surface (what the camera can see). Water at the surface moves faster than the average throughout the full depth. Based on decades of hydrological research, surface velocity is typically multiplied by 0.85 to estimate average velocity.

Think of it like this: if you measure surface velocity at 2.0 m/s, the average velocity throughout the entire depth is approximately 2.0 × 0.85 = 1.7 m/s.

[VISUAL PLACEHOLDER: Side-view diagram of river showing velocity profile - fastest at surface, slowest at bottom, with arrows of different lengths representing velocity at different depths]

### Cross-Sectional Area (A): How Much Space the Water Fills

**What it is:**
Cross-sectional area is the amount of space water occupies when you slice through the river from bank to bank. Imagine cutting the river like slicing through a loaf of bread - the cross-section is what you would see if you looked at that slice head-on.

It is measured in square meters (m²).

**Making it concrete:**
Imagine a river that is 10 meters wide and 2 meters deep at the center. If the river had a perfectly rectangular cross-section (it does not, but this simplifies the math):
- Area = width × depth = 10 m × 2 m = 20 m²

This 20 m² is the space filled with flowing water.

**Real-world complexity:**
Rivers do not have rectangular cross-sections. They have irregular shapes:
- Deeper in the middle, shallower at the edges
- Uneven bottoms with rocks, pools, and riffles
- Banks that slope rather than stand vertical

This is why proper measurement requires surveying the actual riverbed shape - we need to know the real profile, not assume a simple rectangle.

**How area changes with water level:**
As the river rises, the cross-sectional area increases:
- When the water is low, maybe only 15 m² is filled
- When the water is at normal level, maybe 25 m² is filled
- When the water is at flood level, maybe 50 m² or more is filled

More area means more flow, even if velocity stays the same.

[VISUAL PLACEHOLDER: Three diagrams showing the same river cross-section at low, normal, and high water levels, with the filled area shaded and labeled (15 m², 25 m², 50 m²)]

---

## Putting It All Together: How Q = v × A Works

### A Worked Example with Real Numbers

Let's calculate discharge for a medium river at normal flow:

**Given information:**
- Average velocity (v) = 1.2 m/s
- Cross-sectional area (A) = 30 m²

**Calculate discharge:**
Q = v × A
Q = 1.2 m/s × 30 m²
Q = 36 m³/s

**What this means:**
Every second, 36 cubic meters of water (36,000 liters) flow past this point. In one hour, that is 129,600 cubic meters - enough water to fill 50 Olympic-size swimming pools.

### Understanding the Interaction

The power of Q = v × A is understanding how velocity and area interact:

**Scenario 1: Rising flood**
- Water level rises, increasing area from 30 m² to 50 m²
- Velocity also increases from 1.2 m/s to 2.0 m/s (deeper water flows faster)
- New discharge: Q = 2.0 × 50 = 100 m³/s
- Discharge has nearly tripled, even though velocity did not even double

This shows why floods are so dangerous - small increases in water level create large increases in discharge.

**Scenario 2: Dry season**
- Water level drops, decreasing area from 30 m² to 12 m²
- Velocity also decreases from 1.2 m/s to 0.6 m/s (shallow water flows slower)
- New discharge: Q = 0.6 × 12 = 7.2 m³/s
- Discharge has dropped to one-fifth of normal

This shows why dry seasons stress water supplies - available water drops dramatically.

[VISUAL PLACEHOLDER: Side-by-side comparison showing normal flow (Q=36 m³/s), flood conditions (Q=100 m³/s), and dry season (Q=7.2 m³/s) with labeled velocity and area values for each]

### Why We Measure Both Components

You might ask: "Why not just measure water level? Why do we need velocity too?"

**The problem with water level alone:**
Water level (stage) tells you how deep the river is, but not how much water is flowing. Consider:

- A wide, shallow river at 1 meter depth might carry 20 m³/s
- A narrow, deep river at 1 meter depth might carry only 5 m³/s
- A very wide river at 1 meter depth might carry 200 m³/s

The same water level can mean completely different discharge depending on the river's shape and velocity.

**The advantage of measuring discharge directly:**
Discharge is the measurement that matters for decisions:
- "Is there enough water to supply the camp?" requires knowing discharge (m³/s), not just depth (m)
- "Will this flood overtop the levee?" depends on discharge, not just water level
- "How much water is available for downstream communities?" requires discharge

OpenRiverCam measures velocity directly (by tracking surface features) and combines it with cross-sectional area information to calculate discharge. This provides the actionable information you actually need.

---

## The Rating Curve: A Practical Shortcut

### What is a Rating Curve?

Once you have measured discharge at many different water levels, you can create a "rating curve" - a graph showing the relationship between water level and discharge for that specific location.

Think of a rating curve as a conversion chart:
- Water level 1.0 m → Discharge approximately 15 m³/s
- Water level 1.5 m → Discharge approximately 35 m³/s
- Water level 2.0 m → Discharge approximately 65 m³/s
- Water level 2.5 m → Discharge approximately 110 m³/s

Once you have this relationship established, you can estimate discharge by simply reading the water level. This is much simpler than measuring velocity every time.

**The restaurant menu analogy:**
A rating curve is like a restaurant menu. The menu tells you: "If you want chicken curry (discharge), it costs 150 pesos (water level)." Once the menu exists, you do not need to recalculate the cost every time - you just read it from the menu.

Similarly, once the rating curve exists, you do not need to measure velocity every time - you just read the discharge from the curve based on the current water level.

### Why Rating Curves Are Not Simple Straight Lines

You might expect that if 1 meter of depth gives 15 m³/s, then 2 meters of depth would give 30 m³/s (double the depth, double the flow). But rivers do not work this way.

As water level rises:
- Cross-sectional area increases (more space filled with water)
- Velocity usually increases too (deeper water flows faster)
- These effects multiply

Result: doubling water level often more than doubles discharge. The relationship is curved, not straight.

**Real-world numbers for a typical medium river:**
- 1.0 m depth → 15 m³/s discharge
- 1.5 m depth → 35 m³/s discharge (2.3 times more, not just 1.5 times)
- 2.0 m depth → 65 m³/s discharge (4.3 times more, not just 2 times)
- 2.5 m depth → 110 m³/s discharge (7.3 times more, not just 2.5 times)

This curved relationship is why small changes in water level during floods create large changes in discharge - and why floods can intensify so quickly.

[VISUAL PLACEHOLDER: Graph with water level on vertical axis (0-3m) and discharge on horizontal axis (0-150 m³/s), showing curved rating relationship with the example points above marked and labeled]

### How OpenRiverCam Establishes Rating Curves

OpenRiverCam establishes rating curves through repeated measurements:

**Step 1: Measure at different water levels**
Over time (weeks to months), the camera measures velocity at many different water levels - low flow, normal flow, high flow, and ideally some flood events.

**Step 2: Calculate discharge for each measurement**
For each measurement, OpenRiverCam calculates discharge using Q = v × A (velocity from camera tracking, area from cross-section survey and water level).

**Step 3: Plot the relationship**
Each measurement creates a point on the graph: "At this water level, discharge was this value." Accumulating many points reveals the rating curve.

**Step 4: Use the curve for continuous monitoring**
Once established, the system can estimate discharge from just the water level, making continuous monitoring more reliable and less computationally intensive.

---

## Why These Relationships Matter for Humanitarian Decisions

### Flood Early Warning: The Threshold Concept

Communities need to know: "When should we worry? When should we evacuate?"

**Water level alone is misleading:**
"The river is at 2.5 meters" does not tell you if this is dangerous. Different rivers flood at different levels.

**Discharge provides context:**
"The river is flowing at 110 m³/s, which is approaching the 130 m³/s level when the lower village floods" provides actionable information.

**Setting thresholds:**
By combining historical flood data with rating curves, you can establish meaningful thresholds:
- Normal flow: < 50 m³/s (green - no action needed)
- High flow: 50-80 m³/s (yellow - monitor closely)
- Warning level: 80-120 m³/s (orange - prepare for possible flooding)
- Flood level: > 120 m³/s (red - evacuate low-lying areas)

These discharge-based thresholds are consistent and meaningful, unlike water level thresholds that vary for each river.

### Water Resource Management: Understanding Availability

A WASH officer managing water supply for a refugee camp needs to know if there is sufficient flow to meet needs.

**Camp requirements:**
- Population: 20,000 people
- Minimum standard: 20 liters per person per day
- Total daily need: 400,000 liters = 400 m³

**Sustainable extraction:**
Good practice suggests extracting no more than 20% of river flow to avoid environmental damage and conflicts with downstream users.

**Calculating safe extraction:**
If river discharge is 30 m³/s:
- Flow per day: 30 m³/s × 86,400 seconds = 2,592,000 m³/day
- 20% of flow: 518,400 m³/day
- Camp needs: 400 m³/day
- Result: Extraction is sustainable - camp needs are less than 0.1% of river flow

If river discharge drops to 2 m³/s (dry season):
- Flow per day: 2 m³/s × 86,400 seconds = 172,800 m³/day
- 20% of flow: 34,560 m³/day
- Camp needs: 400 m³/day
- Result: Still sustainable, but camp is using 1.2% of river flow - monitoring is important

This objective data supports:
- Negotiating water allocation with host communities
- Planning for dry season shortages
- Justifying additional water sources (boreholes, storage)
- Demonstrating responsible resource use to host governments

### Disaster Response: Timing Interventions Safely

Response teams need to cross rivers, repair infrastructure, or establish operations near water bodies. Knowing whether flows are rising or falling informs safe timing.

**Without discharge data:**
"The river looks lower than yesterday" is subjective and potentially dangerous. Visual appearance misleads - a 10 cm drop in level might represent either a small decrease in discharge (flows still rising) or a significant decrease (flood receding).

**With discharge data:**
- Current discharge: 85 m³/s
- Discharge 6 hours ago: 95 m³/s
- Discharge 12 hours ago: 102 m³/s
- Trend: Discharge is dropping approximately 7-10 m³/s every 6 hours

Interpretation: "Flood is receding. If trend continues, discharge will be below 50 m³/s (safer threshold) in about 24 hours. We can plan interventions for tomorrow afternoon."

This objective trend analysis supports safer decision-making than visual estimates.

---

## Common Misunderstandings (What to Avoid)

### Misunderstanding 1: "Higher Water Level Always Means More Flow"

**Why this seems right:**
When the river rises, there is more water, so flow must be higher.

**Why this is incomplete:**
Water level can rise because:
- Discharge increased (yes, more flow)
- Something downstream blocked the flow (water backs up but discharge may not increase)
- Water is moving slower (deeper but slower water can give similar discharge to shallower but faster water)

**The correct understanding:**
Higher water level usually means more flow, but you cannot assume discharge without considering velocity. This is why measuring both components matters.

### Misunderstanding 2: "We Can Just Measure Velocity and Ignore Area"

**Why this seems right:**
Velocity changes with flow conditions - faster during floods, slower during dry periods. If we measure velocity, we have captured the important information.

**Why this is wrong:**
A very fast velocity in a small stream (v = 3 m/s, A = 2 m², Q = 6 m³/s) is less flow than a slow velocity in a large river (v = 0.5 m/s, A = 100 m², Q = 50 m³/s).

**The correct understanding:**
Both components matter. You need velocity AND area to calculate meaningful discharge.

### Misunderstanding 3: "Rating Curves Never Change"

**Why this seems right:**
We went through all the work of establishing the rating curve, so we can use it forever.

**Why this is wrong:**
Rivers change:
- Major floods reshape the riverbed (deeper channels, deposited sediment)
- Bank erosion widens the river
- Vegetation growth changes flow patterns
- Upstream dam operations alter natural flow patterns

**The correct understanding:**
Rating curves need periodic verification and recalibration - typically annually or after major flood events. OpenRiverCam can assist by making new velocity measurements to check if the curve still holds.

### Misunderstanding 4: "Surface Velocity Equals Average Velocity"

**Why this seems right:**
The camera measures surface velocity, so that must be the velocity we use.

**Why this is wrong:**
Surface water moves faster than water at depth (friction with riverbed slows deep water). If you used surface velocity directly, you would overestimate discharge.

**The correct understanding:**
Surface velocity must be adjusted (typically multiply by 0.85) to estimate average velocity. OpenRiverCam does this adjustment automatically, but it is important to understand why.

[VISUAL PLACEHOLDER: Four panels illustrating each misunderstanding with "Common Mistake" and "Reality" side by side using simple diagrams]

---

## Real-World Example: Putting It All Together

Let's work through a complete scenario combining everything we have learned.

**Context:**
A humanitarian organization operates a refugee camp along a medium-sized river. They have installed an OpenRiverCam system to monitor river flow for water supply management.

**Current measurement:**
- Water level: 1.8 meters (measured from staff gauge visible in camera)
- Surface velocity: 1.6 m/s (measured by camera tracking foam and debris)
- Adjusted average velocity: 1.6 × 0.85 = 1.36 m/s
- Cross-sectional area at 1.8 m level: 42 m² (from previous survey)

**Calculate discharge:**
Q = v × A
Q = 1.36 m/s × 42 m²
Q = 57.1 m³/s

**Interpret for decision-making:**

**Water supply context:**
- Camp needs 400 m³ per day (0.005 m³/s)
- River provides 57.1 m³/s
- Camp uses less than 0.01% of river flow
- Extraction is highly sustainable - no concerns about over-use

**Flood risk context:**
- Historical data shows flooding begins around 95 m³/s
- Current discharge is 57.1 m³/s (about 60% of flood threshold)
- Not immediate flood risk, but system should monitor for rising trends

**Seasonal context:**
- Rating curve shows normal flow for this season is 45-65 m³/s
- Current 57.1 m³/s is in normal range
- No special action needed

**Operational decision:**
Based on this data, the WASH officer decides:
- Continue normal water pumping operations (flow is adequate)
- No flood warning needed (flow well below threshold)
- Schedule routine system check for next week
- No immediate concerns

**If conditions were different:**
If the measurement showed 95 m³/s and rising:
- Trigger flood alert to camp management
- Prepare to relocate vulnerable families from low-lying sections
- Secure loose materials that could be swept away
- Notify downstream communities if early warning system is connected

This demonstrates how understanding the fundamental relationships (Q = v × A) translates into practical operational decisions.

---

## Summary: Key Concepts to Remember

**The fundamental equation:**
Q = v × A (Discharge equals velocity multiplied by area)

**The three components:**
1. **Discharge (Q)**: Total flow - how much water passes each second (m³/s)
2. **Velocity (v)**: Water speed - how fast the water moves (m/s)
3. **Area (A)**: Cross-sectional space - how much space water fills (m²)

**Why each component matters:**
- **Discharge** is what informs decisions (enough for water supply? approaching flood level?)
- **Velocity** changes with flow conditions (faster during floods, slower during low flow)
- **Area** changes with water level (higher level fills more space)

**The rating curve shortcut:**
Once established through repeated measurements, a rating curve allows estimating discharge from water level alone, simplifying continuous monitoring.

**Real-world implications:**
- Small changes in water level can mean large changes in discharge (curved relationship)
- Understanding discharge enables objective thresholds for flood warnings
- Knowing available discharge supports sustainable water resource management
- Discharge trends (rising vs. falling) inform safe timing for interventions

**What OpenRiverCam does:**
- Measures velocity by tracking surface features with the camera
- Adjusts surface velocity to estimate average velocity (multiply by 0.85)
- Combines velocity with cross-sectional area to calculate discharge
- Builds rating curves over time to enable simpler continuous monitoring

You do not need to be a hydrologist to use OpenRiverCam, but understanding these fundamental relationships helps you:
- Interpret data correctly
- Make better decisions
- Troubleshoot when something seems wrong
- Communicate effectively with technical support
- Build confidence in the system

The next sections will build on this foundation, explaining how OpenRiverCam measures these components in practice and how to interpret the data for your specific humanitarian context.

---

**Next Section:** [3.2 Understanding River Cross-Sections and Bathymetry](02-cross-sections-and-bathymetry.md)

[VISUAL PLACEHOLDER: One-page summary infographic with Q = v × A at center, showing all three components with real-world analogies (garden hose, highway traffic) and example numbers, plus key decision contexts (flood warning, water supply, disaster response)]
