# 3.1 Fundamental Relationships: Velocity, Area, Flow, and Discharge

This section explains the core hydrological concepts that make OpenRiverCam work. For those who are not hydrologists or engineers, these concepts are more accessible than they may initially appear. The following discussion builds understanding from everyday experiences that are already familiar.

By the end of this section, readers will understand what river discharge means and why it matters, how velocity and cross-sectional area combine to create flow, why each component requires measurement, and how these measurements inform humanitarian decisions.

---

## Starting with What You Already Know

### The Water Hose Analogy

The experience of using a garden hose contains the entire foundation of river flow measurement. When the tap is turned on, water flows out. To increase the rate at which water fills a bucket, one can either turn the tap higher to increase water velocity, or use a hose with a wider opening to increase cross-sectional area. This simple experience demonstrates the fundamental concepts: velocity represents how fast the water moves (analogous to turning the tap higher), area represents how large the opening is (analogous to using a wider hose), and flow represents how much water is obtained (analogous to how quickly the bucket fills). Rivers operate according to the same principles. A river can be conceptualized as a very large hose lying on its side, with water flowing through it.

[VISUAL PLACEHOLDER: Split illustration showing garden hose on left, river cross-section on right, with arrows showing velocity and area labeled identically on both]

### The Highway Traffic Analogy

Consider traffic flow on a highway. The number of vehicles passing a point in one hour depends on how fast the vehicles are moving (30 km/h in a traffic jam versus 100 km/h on an open road) and how many lanes the highway has (a 2-lane road versus a 6-lane highway). Even if vehicles move slowly, many vehicles still pass if the highway has many lanes. Conversely, even if the highway is narrow, many vehicles still pass if they move very fast. The total number of vehicles passing equals speed multiplied by the number of lanes.

Rivers function identically. The amount of water passing a point depends on how fast the water moves and how much space (area) the water fills.

---

## The Fundamental Equation: Q = v × A

### Breaking Down the Components

The relationship between velocity, area, and flow is captured in one fundamental equation:

**Q = v × A**

Where Q represents discharge (the total flow), v represents velocity (how fast the water moves), and A represents cross-sectional area (how much space the water fills). Understanding each component is essential.

### Discharge (Q): How Much Water is Flowing

Discharge represents the volume of water flowing past a point each second, measured in cubic meters per second (m³/s) or liters per second (L/s). Hydrologists use the technical term "discharge," though "flow" conveys the same meaning. When encountering the term "discharge," one should think "how much water is flowing."

To make this concrete, one cubic meter equals 1,000 liters, representing a cube one meter on each side filled with water. If discharge is 10 m³/s, this corresponds to 10 of these cubes flowing past every single second, which equals 10,000 liters per second—enough to fill a small swimming pool in less than a minute.

Real-world discharge values vary considerably. Small streams typically exhibit discharge of 0.5-5 m³/s. Medium rivers, such as those near refugee camps, commonly show 10-100 m³/s. Large rivers like the Mekong during normal flow display 1,000-5,000 m³/s. Major floods on large rivers can exceed 10,000 m³/s.

Discharge matters critically in humanitarian contexts for several reasons. For flood warning, when discharge exceeds certain levels, flooding begins. For water supply, one must know if the river has sufficient flow to supply camp needs. For infrastructure safety, bridges and water intakes are designed for specific discharge levels. For shared resources, fair water allocation requires knowing how much water is available (Merwade, 2009).

[VISUAL PLACEHOLDER: Diagram showing cubes of water (1m³ each) flowing past a point in a river, with "10 m³/s = 10 cubes per second = 10,000 liters per second" labeled]

### Velocity (v): How Fast the Water is Moving

Velocity represents the speed at which water moves downstream, measured in meters per second (m/s). To make this concrete, walking speed approximates 1.5 m/s (one could walk alongside the water and keep pace), jogging speed approximates 3 m/s (one would need to jog to keep up with the water), and running speed approximates 5-6 m/s (one would struggle to keep up even at full sprint).

Real-world river velocities span a wide range. Very slow flow, resembling pond-like conditions, shows 0.1-0.3 m/s. Slow rivers during typical low flow exhibit 0.3-0.8 m/s. Medium flow under typical normal conditions demonstrates 0.8-1.5 m/s. Fast flow during high water or the beginning of floods shows 1.5-3 m/s. Very fast flow under flood conditions reaches 3-6 m/s. Extreme flow during dangerous floods exceeds 6 m/s.

Velocity varies within a river cross-section for several reasons. Surface water moves faster than water near the bottom, as friction with the riverbed slows deep water. Water in the center of the river moves faster than water near the banks, as friction with the sides slows edge water. Straight sections move faster than curved sections, and narrow sections often move faster than wide sections. When measuring velocity, hydrologists are typically interested in the average velocity—the typical speed throughout the entire river cross-section (Rantz et al., 1982).

OpenRiverCam measures velocity at the surface, which the camera can observe. Water at the surface moves faster than the average throughout the full depth. Based on decades of hydrological research, surface velocity is typically multiplied by 0.85 to estimate average velocity (Costa et al., 2000). For example, if surface velocity measures 2.0 m/s, the average velocity throughout the entire depth approximates 2.0 × 0.85 = 1.7 m/s.

[VISUAL PLACEHOLDER: Side-view diagram of river showing velocity profile - fastest at surface, slowest at bottom, with arrows of different lengths representing velocity at different depths]

### Cross-Sectional Area (A): How Much Space the Water Fills

Cross-sectional area represents the amount of space water occupies when one conceptually slices through the river from bank to bank. Imagining cutting the river like slicing through a loaf of bread, the cross-section is what one would see if looking at that slice head-on. This is measured in square meters (m²).

To make this concrete, imagine a river that is 10 meters wide and 2 meters deep at the center. If the river had a perfectly rectangular cross-section (it does not, but this simplifies the mathematics), area would equal width × depth = 10 m × 2 m = 20 m². This 20 m² represents the space filled with flowing water.

Real rivers do not have rectangular cross-sections. They have irregular shapes: deeper in the middle and shallower at the edges, uneven bottoms with rocks, pools, and riffles, and banks that slope rather than stand vertical. This is why proper measurement requires surveying the actual riverbed shape—hydrologists need to know the real profile, not assume a simple rectangle (Herschy, 2009).

As the river rises, cross-sectional area increases. When water is low, perhaps only 15 m² is filled. When water is at normal level, perhaps 25 m² is filled. When water is at flood level, perhaps 50 m² or more is filled. More area means more flow, even if velocity stays the same.

[VISUAL PLACEHOLDER: Three diagrams showing the same river cross-section at low, normal, and high water levels, with the filled area shaded and labeled (15 m², 25 m², 50 m²)]

---

## Putting It All Together: How Q = v × A Works

### A Worked Example with Real Numbers

Consider calculating discharge for a medium river at normal flow. Given average velocity (v) = 1.2 m/s and cross-sectional area (A) = 30 m², discharge is calculated as Q = v × A = 1.2 m/s × 30 m² = 36 m³/s. This means every second, 36 cubic meters of water (36,000 liters) flow past this point. In one hour, that equals 129,600 cubic meters—enough water to fill 50 Olympic-size swimming pools.

### Understanding the Interaction

The power of Q = v × A lies in understanding how velocity and area interact. During a rising flood, water level rises, increasing area from 30 m² to 50 m². Velocity also increases from 1.2 m/s to 2.0 m/s, as deeper water flows faster. New discharge becomes Q = 2.0 × 50 = 100 m³/s. Discharge has nearly tripled, even though velocity did not even double. This demonstrates why floods are so dangerous—small increases in water level create large increases in discharge.

Conversely, during dry season, water level drops, decreasing area from 30 m² to 12 m². Velocity also decreases from 1.2 m/s to 0.6 m/s, as shallow water flows slower. New discharge becomes Q = 0.6 × 12 = 7.2 m³/s. Discharge has dropped to one-fifth of normal. This demonstrates why dry seasons stress water supplies—available water drops dramatically.

[VISUAL PLACEHOLDER: Side-by-side comparison showing normal flow (Q=36 m³/s), flood conditions (Q=100 m³/s), and dry season (Q=7.2 m³/s) with labeled velocity and area values for each]

### Why We Measure Both Components

One might question why not simply measure water level, rather than requiring velocity measurement as well. Water level (stage) tells how deep the river is, but not how much water is flowing. A wide, shallow river at 1 meter depth might carry 20 m³/s. A narrow, deep river at 1 meter depth might carry only 5 m³/s. A very wide river at 1 meter depth might carry 200 m³/s. The same water level can mean completely different discharge depending on the river's shape and velocity.

Discharge is the measurement that matters for decisions. Questions such as "Is there enough water to supply the camp?" require knowing discharge (m³/s), not just depth (m). "Will this flood overtop the levee?" depends on discharge, not just water level. "How much water is available for downstream communities?" requires discharge.

OpenRiverCam measures velocity directly by tracking surface features and combines it with cross-sectional area information to calculate discharge. This provides the actionable information that decision-makers actually need (Rantz et al., 1982).

---

## The Rating Curve: A Practical Shortcut

### What is a Rating Curve?

Once discharge has been measured at many different water levels, one can create a "rating curve"—a graph showing the relationship between water level and discharge for that specific location. A rating curve functions as a conversion chart: water level 1.0 m corresponds to discharge approximately 15 m³/s, water level 1.5 m corresponds to approximately 35 m³/s, water level 2.0 m corresponds to approximately 65 m³/s, and water level 2.5 m corresponds to approximately 110 m³/s.

Once this relationship is established, one can estimate discharge by simply reading the water level. This is much simpler than measuring velocity every time. A rating curve resembles a restaurant menu. The menu tells you that chicken curry costs 150 pesos. Once the menu exists, one need not recalculate the cost every time—one simply reads it from the menu. Similarly, once the rating curve exists, one need not measure velocity every time—one simply reads the discharge from the curve based on the current water level.

### Why Rating Curves Are Not Simple Straight Lines

One might expect that if 1 meter of depth gives 15 m³/s, then 2 meters of depth would give 30 m³/s (double the depth, double the flow). However, rivers do not work this way. As water level rises, cross-sectional area increases (more space filled with water) and velocity usually increases too (deeper water flows faster). These effects multiply.

Real-world numbers for a typical medium river demonstrate this nonlinearity. At 1.0 m depth, discharge is 15 m³/s. At 1.5 m depth, discharge is 35 m³/s (2.3 times more, not just 1.5 times). At 2.0 m depth, discharge is 65 m³/s (4.3 times more, not just 2 times). At 2.5 m depth, discharge is 110 m³/s (7.3 times more, not just 2.5 times). This curved relationship explains why small changes in water level during floods create large changes in discharge—and why floods can intensify so quickly (Herschy, 2009).

[VISUAL PLACEHOLDER: Graph with water level on vertical axis (0-3m) and discharge on horizontal axis (0-150 m³/s), showing curved rating relationship with the example points above marked and labeled]

### How OpenRiverCam Establishes Rating Curves

OpenRiverCam establishes rating curves through repeated measurements. Over time (weeks to months), the camera measures velocity at many different water levels—low flow, normal flow, high flow, and ideally some flood events. For each measurement, OpenRiverCam calculates discharge using Q = v × A (velocity from camera tracking, area from cross-section survey and water level). Each measurement creates a point on the graph: "At this water level, discharge was this value." Accumulating many points reveals the rating curve. Once established, the system can estimate discharge from just the water level, making continuous monitoring more reliable and less computationally intensive.

---

## Why These Relationships Matter for Humanitarian Decisions

### Flood Early Warning: The Threshold Concept

Communities need to know when they should worry and when they should evacuate. Water level alone is misleading. Stating "The river is at 2.5 meters" does not indicate whether this is dangerous, as different rivers flood at different levels. Discharge provides context. Stating "The river is flowing at 110 m³/s, which is approaching the 130 m³/s level when the lower village floods" provides actionable information.

By combining historical flood data with rating curves, one can establish meaningful thresholds: normal flow below 50 m³/s (green—no action needed), high flow 50-80 m³/s (yellow—monitor closely), warning level 80-120 m³/s (orange—prepare for possible flooding), and flood level above 120 m³/s (red—evacuate low-lying areas). These discharge-based thresholds are consistent and meaningful, unlike water level thresholds that vary for each river.

### Water Resource Management: Understanding Availability

A WASH officer managing water supply for a refugee camp needs to know if there is sufficient flow to meet needs. Consider a camp with a population of 20,000 people requiring a minimum standard of 20 liters per person per day, totaling 400,000 liters = 400 m³ daily need. Good practice suggests extracting no more than 20% of river flow to avoid environmental damage and conflicts with downstream users (Gleick, 1996).

If river discharge is 30 m³/s, flow per day equals 30 m³/s × 86,400 seconds = 2,592,000 m³/day. Twenty percent of this flow equals 518,400 m³/day. Camp needs of 400 m³/day represent less than 0.1% of river flow, indicating extraction is sustainable. If river discharge drops to 2 m³/s during dry season, flow per day equals 2 m³/s × 86,400 seconds = 172,800 m³/day. Twenty percent of this flow equals 34,560 m³/day. Camp needs of 400 m³/day represent 1.2% of river flow. Extraction remains sustainable, but the camp is using a measurable proportion of river flow, making monitoring important.

This objective data supports negotiating water allocation with host communities, planning for dry season shortages, justifying additional water sources such as boreholes or storage, and demonstrating responsible resource use to host governments.

### Disaster Response: Timing Interventions Safely

Response teams need to cross rivers, repair infrastructure, or establish operations near water bodies. Knowing whether flows are rising or falling informs safe timing. Without discharge data, subjective observations such as "The river looks lower than yesterday" can be dangerous. Visual appearance misleads—a 10 cm drop in level might represent either a small decrease in discharge (flows still rising) or a significant decrease (flood receding).

With discharge data showing current discharge at 85 m³/s, discharge 6 hours ago at 95 m³/s, and discharge 12 hours ago at 102 m³/s, the trend reveals discharge is dropping approximately 7-10 m³/s every 6 hours. This objective trend analysis enables the interpretation: "Flood is receding. If trend continues, discharge will be below 50 m³/s (safer threshold) in about 24 hours. We can plan interventions for tomorrow afternoon." This objective trend analysis supports safer decision-making than visual estimates.

---

## Common Misunderstandings (What to Avoid)

### Misunderstanding 1: "Higher Water Level Always Means More Flow"

This seems right because when the river rises, there is more water, suggesting flow must be higher. However, this is incomplete. Water level can rise because discharge increased (yes, more flow), something downstream blocked the flow (water backs up but discharge may not increase), or water is moving slower (deeper but slower water can give similar discharge to shallower but faster water). The correct understanding is that higher water level usually means more flow, but one cannot assume discharge without considering velocity. This is why measuring both components matters.

### Misunderstanding 2: "We Can Just Measure Velocity and Ignore Area"

This seems right because velocity changes with flow conditions—faster during floods, slower during dry periods. If velocity is measured, it appears the important information has been captured. However, this is wrong. A very fast velocity in a small stream (v = 3 m/s, A = 2 m², Q = 6 m³/s) represents less flow than a slow velocity in a large river (v = 0.5 m/s, A = 100 m², Q = 50 m³/s). The correct understanding is that both components matter. One needs velocity AND area to calculate meaningful discharge.

### Misunderstanding 3: "Rating Curves Never Change"

This seems right because considerable work was invested in establishing the rating curve, suggesting it can be used indefinitely. However, this is wrong. Rivers change through major floods that reshape the riverbed (deeper channels, deposited sediment), bank erosion that widens the river, vegetation growth that changes flow patterns, and upstream dam operations that alter natural flow patterns. The correct understanding is that rating curves need periodic verification and recalibration—typically annually or after major flood events. OpenRiverCam can assist by making new velocity measurements to check if the curve still holds (Herschy, 2009).

### Misunderstanding 4: "Surface Velocity Equals Average Velocity"

This seems right because the camera measures surface velocity, suggesting that must be the velocity used in calculations. However, this is wrong. Surface water moves faster than water at depth, as friction with the riverbed slows deep water. If surface velocity were used directly, discharge would be overestimated. The correct understanding is that surface velocity must be adjusted (typically multiply by 0.85) to estimate average velocity. OpenRiverCam performs this adjustment automatically, but understanding why is important (Costa et al., 2000).

[VISUAL PLACEHOLDER: Four panels illustrating each misunderstanding with "Common Mistake" and "Reality" side by side using simple diagrams]

---

## Real-World Example: Putting It All Together

Consider a complete scenario combining everything learned. A humanitarian organization operates a refugee camp along a medium-sized river. They have installed an OpenRiverCam system to monitor river flow for water supply management. Current measurement shows water level at 1.8 meters (measured from staff gauge visible in camera), surface velocity at 1.6 m/s (measured by camera tracking foam and debris), adjusted average velocity at 1.6 × 0.85 = 1.36 m/s, and cross-sectional area at 1.8 m level at 42 m² (from previous survey).

Discharge is calculated as Q = v × A = 1.36 m/s × 42 m² = 57.1 m³/s. This can be interpreted for decision-making in several contexts. For water supply context, camp needs 400 m³ per day (0.005 m³/s). River provides 57.1 m³/s. Camp uses less than 0.01% of river flow. Extraction is highly sustainable with no concerns about over-use. For flood risk context, historical data shows flooding begins around 95 m³/s. Current discharge is 57.1 m³/s (about 60% of flood threshold). There is no immediate flood risk, but the system should monitor for rising trends. For seasonal context, the rating curve shows normal flow for this season is 45-65 m³/s. Current 57.1 m³/s is in normal range. No special action is needed.

Based on this data, the WASH officer decides to continue normal water pumping operations (flow is adequate), issue no flood warning (flow well below threshold), schedule routine system check for next week, and note no immediate concerns. If conditions were different and measurement showed 95 m³/s and rising, appropriate actions would include triggering flood alert to camp management, preparing to relocate vulnerable families from low-lying sections, securing loose materials that could be swept away, and notifying downstream communities if early warning system is connected.

This demonstrates how understanding the fundamental relationships (Q = v × A) translates into practical operational decisions.

---

## Summary: Key Concepts to Remember

The fundamental equation is Q = v × A (Discharge equals velocity multiplied by area). The three components are Discharge (Q), representing total flow or how much water passes each second (m³/s); Velocity (v), representing water speed or how fast the water moves (m/s); and Area (A), representing cross-sectional space or how much space water fills (m²).

Each component matters for specific reasons. Discharge informs decisions such as whether there is enough for water supply or if flow is approaching flood level. Velocity changes with flow conditions (faster during floods, slower during low flow). Area changes with water level (higher level fills more space).

The rating curve provides a shortcut. Once established through repeated measurements, a rating curve allows estimating discharge from water level alone, simplifying continuous monitoring. Small changes in water level can mean large changes in discharge due to the curved relationship. Understanding discharge enables objective thresholds for flood warnings. Knowing available discharge supports sustainable water resource management. Discharge trends (rising versus falling) inform safe timing for interventions.

OpenRiverCam measures velocity by tracking surface features with the camera, adjusts surface velocity to estimate average velocity (multiply by 0.85), combines velocity with cross-sectional area to calculate discharge, and builds rating curves over time to enable simpler continuous monitoring.

One need not be a hydrologist to use OpenRiverCam, but understanding these fundamental relationships helps interpret data correctly, make better decisions, troubleshoot when something seems wrong, communicate effectively with technical support, and build confidence in the system. The subsequent sections will build on this foundation, explaining how OpenRiverCam measures these components in practice and how to interpret the data for specific humanitarian contexts.

---

**Next Section:** [3.2 Understanding River Cross-Sections and Bathymetry](02-cross-sections-and-bathymetry.md)

[VISUAL PLACEHOLDER: One-page summary infographic with Q = v × A at center, showing all three components with real-world analogies (garden hose, highway traffic) and example numbers, plus key decision contexts (flood warning, water supply, disaster response)]

## References

Costa, J. E., Cheng, R. T., Haeni, F. P., Melcher, N., Spicer, K. R., Hayes, E., ... & Soggin, D. (2000). Use of radars to monitor stream discharge by noncontact methods. *Water Resources Research*, 36(10), 2809-2823.

Gleick, P. H. (1996). Basic water requirements for human activities: Meeting basic needs. *Water International*, 21(2), 83-92.

Herschy, R. W. (2009). *Streamflow measurement* (3rd ed.). Taylor & Francis.

Merwade, V. (2009). Effect of spatial trends on interpolation of river bathymetry. *Journal of Hydrology*, 371(1-4), 169-181.

Rantz, S. E., et al. (1982). *Measurement and computation of streamflow: Volume 1. Measurement of stage and discharge* (Water Supply Paper 2175). U.S. Geological Survey.
