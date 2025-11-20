# 6.1 Visible Tracers Requirement

When selecting a site for OpenRiverCam deployment, the single most important question is: "Will there be enough visible features on the water surface for the camera to track?" Without visible tracers, velocity measurement is impossible. This section provides practical guidance for assessing whether a potential site will have adequate tracers throughout the year.

By the end of this section, you will be able to:
- Evaluate natural tracer availability at potential sites
- Understand seasonal variations in tracer conditions
- Recognize situations where tracers will be insufficient
- Make informed site selection decisions based on tracer requirements

---

## Review: Why Tracers Matter

### The Foundation of Velocity Measurement

As you learned in Section 3.2, OpenRiverCam measures velocity by tracking visible features on the water surface. The camera watches foam patches, floating debris, ripples, and texture patterns move downstream, calculating how fast they travel. These visible features - called tracers - move with the water, revealing the water's velocity.

**Without tracers, the system cannot measure velocity. Without velocity, it cannot calculate discharge.**

This makes tracer assessment the first and most critical step in site selection. All other site characteristics - access, power availability, security - matter only if the site has adequate tracers.

[VISUAL PLACEHOLDER: Photo showing river with abundant tracers (foam lines, scattered debris, surface texture) with overlay circles highlighting trackable features. Caption: "Abundant natural tracers: foam, debris, and ripples provide multiple features for velocity tracking"]

---

## What Makes Good Tracers: Assessment Criteria

### Visibility Requirements

When evaluating a site, look for tracers that meet these criteria:

**1. Sufficient Contrast**
- Features must be visible against the water surface
- Dark features (shadows from foam, debris) stand out against light-colored water
- Light features (white foam, reflected sunlight on ripples) stand out against dark water
- Color variations (sediment plumes, organic matter) create trackable patterns

**How to assess:**
Stand at the planned camera position and observe the water surface. Can you clearly see distinct features? If you cannot see features with your eyes, the camera will struggle too.

**2. Adequate Distribution**
- Features should appear across the full width of the river, not just near one bank
- Spacing between features should be moderate - neither too sparse nor too dense
- Features should be present in both the center channel and near the banks

**How to assess:**
Observe whether features appear throughout the field of view or are concentrated in specific areas. Imagine dividing the river into three sections (left, center, right) - are there trackable features in all three?

**3. Appropriate Persistence**
- Features must last long enough to track across multiple video frames
- Typically need features to persist for 2-5 seconds as they move through the field of view
- Very short-lived features (bursting bubbles, momentary ripples) are less useful

**How to assess:**
Watch individual features as they float downstream. Do they remain visible and distinct as they move, or do they quickly disappear or merge with other features?

**4. Representative Movement**
- Features must move with the water, not be influenced by wind or caught on obstacles
- Surface-floating materials are ideal
- Partially submerged objects may move slower than surface water

**How to assess:**
Observe whether features move consistently downstream or are affected by wind gusts. Watch for debris caught on rocks or vegetation - these stationary features could confuse tracking algorithms.

[VISUAL PLACEHOLDER: Four-panel comparison showing:
1. Good contrast: distinct features clearly visible
2. Poor contrast: uniform surface, no distinguishable features
3. Good distribution: features spread across river width
4. Poor distribution: features clustered near one bank only]

---

## Natural Tracer Sources

### Understanding What Creates Tracers

Natural tracers appear from several sources. Understanding these sources helps you evaluate whether a site will consistently have adequate tracers.

### Turbulence-Generated Foam

**What creates it:**
When water tumbles over rocks, drops over riffles, or flows through rapids, turbulence incorporates air into the water. This creates foam - clusters of bubbles that float on the surface, often forming visible white lines and patches.

**Where to find it:**
- Immediately downstream of rapids or riffles
- Below small waterfalls or drops
- Around large rocks that create turbulence
- In areas where two channels merge and create mixing

**Seasonal variation:**
- More abundant during higher flows when water velocity creates more turbulence
- Less abundant during very low flows when water barely trickles over obstacles
- Generally reliable except during extreme low-water periods

**Assessment questions:**
- Are there riffles, rapids, or rocky sections upstream of the measurement area?
- Does water flow over rocks or obstacles that create turbulence?
- Is foam visible on the current flow conditions during your site visit?

**Real-world example from Sukabumi:**
During deployment in Indonesia, sites downstream of bridge piers consistently produced excellent foam tracers. The flow around the piers created constant turbulence, generating foam lines that persisted for 50-100 meters downstream. This provided reliable tracers even during moderate dry-season flows.

[VISUAL PLACEHOLDER: Photo from Sukabumi showing foam lines generated by flow around bridge piers, with annotation showing foam trails extending downstream]

### Organic Debris

**What creates it:**
Rivers collect organic material from the surrounding landscape - leaves, twigs, grass, seed pods, flowers, bark fragments - which float on the surface and serve as excellent tracers.

**Where to find it:**
- Rivers flowing through forested areas (consistent leaf fall)
- Agricultural areas during harvest seasons (crop residues)
- Urban areas with vegetation (yard waste, landscaping debris)
- After rainfall events that wash material into the river

**Seasonal variation:**
- **Wet season:** Usually abundant - rainfall washes debris into rivers
- **Early dry season:** Often still plentiful from residual material
- **Late dry season:** Can become scarce as accumulated debris moves downstream
- **Autumn/fall:** Excellent in temperate climates with leaf fall
- **Spring:** Good in many climates with flowering and new growth

**Assessment questions:**
- What type of land cover surrounds the river (forest, agriculture, urban)?
- Is there visible organic debris on the water during your site visit?
- Will seasonal changes dramatically reduce debris availability?

**Real-world example from Sukabumi:**
Urban river sections received consistent organic tracers from riverside vegetation and street runoff. Even during dry periods, daily influx of leaves and small debris provided adequate tracking features. In contrast, one heavily channelized section with concrete banks and no nearby vegetation showed very sparse debris - making it a less suitable site.

[VISUAL PLACEHOLDER: Photo showing floating organic debris (leaves, twigs) scattered across water surface, with circles highlighting individual trackable items]

### Surface Texture and Ripples

**What creates it:**
Water flowing over an uneven riverbed creates ripples, small waves, and texture patterns on the surface. These patterns create visible contrast that can be tracked even when discrete objects (foam, debris) are scarce.

**Where to find it:**
- Sections with moderate flow velocity (0.5-2.0 m/s typically)
- Rivers with rocky or irregular beds
- Areas with subtle depth variations
- Sections with flow around obstacles

**Seasonal variation:**
- Generally more pronounced during moderate to high flows
- Can disappear during very low flows when water becomes glassy
- Less affected by seasonal vegetation or debris availability

**Assessment questions:**
- Does the water surface show visible texture or ripple patterns?
- Can you see variations in surface appearance caused by flow patterns?
- Would texture remain visible from camera height and angle?

**Limitations:**
Surface texture alone is often insufficient for reliable tracking - it works best as a supplement to foam and debris rather than as the sole tracer source.

[VISUAL PLACEHOLDER: Photo showing river surface with visible ripple texture creating pattern of light and shadow]

### Sediment-Laden Water

**What creates it:**
Rivers carrying high sediment loads often show visible color variations as different sediment concentrations mix. Muddy tributaries entering clearer main channels, or varying sediment from different parts of the channel, create trackable patterns.

**Where to find it:**
- Rivers in erosion-prone catchments (deforested areas, agricultural land, unstable geology)
- During and after rainfall events
- Where tributaries with different sediment loads merge
- In meandering sections where flow patterns create sediment sorting

**Seasonal variation:**
- Wet season: Usually abundant with high sediment loads
- Dry season: Often minimal as clear water base flow dominates
- Event-driven: Spikes with each rainfall

**Assessment questions:**
- Is the water visibly turbid or carrying sediment?
- Are there visible plumes or patterns of different sediment concentrations?
- Is sediment availability consistent or only during rain events?

**Cautions:**
Extremely turbid water can sometimes reduce contrast and make tracking difficult. Moderate sediment creating visible patterns is beneficial; very heavy sediment making the entire surface uniformly opaque is less helpful.

[VISUAL PLACEHOLDER: Photo showing sediment plumes or color variations in river water creating visible patterns]

---

## Assessing Tracer Availability: Site Visit Checklist

### Conducting a Tracer Assessment

When visiting a potential site, systematically evaluate tracer conditions using this framework:

### Step 1: Initial Visual Observation (5-10 minutes)

Stand at the planned camera location and observe the water surface.

**Questions to answer:**
- [ ] Can I see distinct features on the water surface?
- [ ] How many visible features can I count in a typical river cross-section?
- [ ] Are features distributed across the full river width or concentrated in certain areas?
- [ ] What types of tracers are present (foam, debris, ripples, sediment patterns)?

**Rating scale:**
- **Excellent:** Numerous distinct features across full width (>20 visible features in view)
- **Good:** Moderate features well-distributed (10-20 visible features)
- **Marginal:** Few features or poorly distributed (5-10 visible features)
- **Poor:** Very few or no distinct features (<5 visible features)

**Document:**
Take photos of the water surface from camera position. These will help later comparison and provide visual reference for report documentation.

[VISUAL PLACEHOLDER: Assessment rating scale with example photos showing Excellent/Good/Marginal/Poor conditions]

### Step 2: Tracer Source Identification (5-10 minutes)

Identify what is creating the tracers you observe.

**Foam sources:**
- [ ] Are there rapids, riffles, or rocks creating turbulence?
- [ ] How far upstream is the turbulence source?
- [ ] Does foam persist into the measurement area?

**Organic debris sources:**
- [ ] What vegetation type surrounds the river?
- [ ] Is debris currently visible on the water?
- [ ] Are there seasonal leaf-fall patterns to consider?

**Texture sources:**
- [ ] Is surface texture visible from camera position?
- [ ] Does flow velocity create ripples?

**Document:**
Note the sources of tracers. Understanding what creates tracers helps predict seasonal variations.

### Step 3: Temporal Variability Assessment (15-30 minutes)

Observe how tracer conditions vary even during your short site visit.

**Short-term variability:**
- [ ] Watch for 15-30 minutes - do tracer densities fluctuate significantly?
- [ ] If wind gusts occur, do they disrupt tracer movement?
- [ ] Do passing clouds changing light conditions affect visibility?

**What this tells you:**
If tracer conditions vary significantly during a 30-minute observation, this suggests the site may have inconsistent measurement conditions. Highly variable conditions are less ideal than consistently moderate conditions.

**Document:**
Note any significant short-term variations and what caused them.

### Step 4: Seasonal Consideration (Research and Discussion)

Consider how tracer conditions will change through the year.

**Research to conduct:**
- [ ] What is the seasonal rainfall pattern?
- [ ] When does vegetation leaf-fall occur (if applicable)?
- [ ] Are there extreme low-flow periods?
- [ ] Do wet/dry seasons dramatically change river character?

**Questions for local knowledge:**
- [ ] Speak with community members: "What does this river look like during the driest time of year?"
- [ ] "Are there times when the water is very clear and calm with nothing floating on it?"
- [ ] "When does the river carry the most debris?"

**Document:**
Create a simple seasonal assessment:

| Season | Expected Tracer Conditions | Confidence Level |
|--------|---------------------------|------------------|
| Current (site visit) | Good - moderate foam and debris | High (observed) |
| Wet season | Excellent - high turbulence and debris | Medium (predicted) |
| Early dry | Good - residual debris | Medium (predicted) |
| Late dry | Marginal - possibly sparse tracers | Low (uncertain) |

[VISUAL PLACEHOLDER: Seasonal calendar template showing months with color-coded expected tracer conditions]

---

## Seasonal Variation Patterns

### Understanding Year-Round Tracer Availability

Different river types show different seasonal patterns. Understanding these patterns helps set realistic expectations.

### Tropical Rivers with Distinct Wet/Dry Seasons

**Typical pattern:**
- **Wet season (Nov-Mar):** Excellent tracers - high flows create turbulence, rainfall washes debris into river
- **Transition to dry (Apr-May):** Good tracers - flows remain moderate, debris still present
- **Mid dry season (Jun-Aug):** Marginal tracers - declining flow reduces turbulence, debris becomes sparse
- **Late dry season (Sep-Oct):** Poor to marginal tracers - low flows, minimal debris, potentially glassy surface
- **Return to wet (Nov):** Rapidly improving - first rains wash accumulated debris into river

**Implications for deployment:**
If your primary monitoring purpose is flood warning, excellent tracer availability during wet season (when floods occur) is most critical. Marginal conditions during late dry season (when floods are impossible) may be acceptable.

If your purpose is year-round water resource monitoring, late dry season gaps are more problematic.

**Real-world example from Sukabumi:**
Deployment occurred in October (late dry season). Site visits showed marginal tracer conditions - very limited foam, sparse debris. Local discussions revealed this was the worst time of year for tracers. The team accepted this limitation because:
1. Flood warning was primary purpose (wet season coverage critical)
2. Even marginal dry-season data provided more information than no monitoring
3. Site had infrastructure advantages (bridge mounting, power access) that outweighed seasonal tracer limitations

The team noted late dry season conditions as "expected low-quality period" and planned additional verification during the transition to wet season.

[VISUAL PLACEHOLDER: Graph showing seasonal tracer quality variation over 12 months for tropical wet/dry pattern, with photos from Sukabumi showing wet vs. dry season differences]

### Temperate Rivers with Year-Round Flow

**Typical pattern:**
- **Spring (Mar-May):** Excellent tracers - snowmelt or spring rain creates high flows, organic material from winter accumulation washes downstream
- **Summer (Jun-Aug):** Good tracers - vegetation growth provides organic material, moderate flows create foam
- **Autumn/Fall (Sep-Nov):** Excellent tracers - leaf fall provides abundant organic debris
- **Winter (Dec-Feb):** Variable - depends on freezing conditions; ice can block surface visibility but snow melt events can provide excellent conditions

**Implications:**
More consistent year-round tracer availability than tropical systems, but winter conditions may create challenges unrelated to tracers (ice, snow covering the camera lens, very short daylight periods).

### Arid/Semi-Arid Rivers with Ephemeral Flow

**Typical pattern:**
- **Wet events:** Excellent tracers - sudden flows mobilize all available debris, create high turbulence
- **Low flow periods:** Poor to non-existent - minimal or no flow means no measurement possible regardless of tracers

**Implications:**
These rivers are challenging for any measurement approach. OpenRiverCam may be suitable for capturing flood events (when tracers are excellent) but will have long no-flow periods. The question is less about tracers and more about whether intermittent event-based monitoring meets your needs.

[VISUAL PLACEHOLDER: Three river type comparison showing typical seasonal patterns on timeline graphs]

---

## When Tracers Are Insufficient

### Recognizing Unsuitable Conditions

Some site conditions will never provide adequate tracers. It is important to recognize these situations and either:
1. Select a different site location
2. Consider alternative monitoring approaches
3. Accept data quality limitations with clear documentation

### Permanently Unsuitable Conditions

**Condition 1: Deep, Slow-Moving Pools**

**Characteristics:**
- Very low velocity (<0.2 m/s)
- Deep water with minimal turbulence
- Smooth, glassy surface
- No upstream riffles or rapids to generate foam

**Why unsuitable:**
Minimal turbulence means no foam generation. Slow movement means debris settles or moves to banks. Surface appears uniform with no trackable features.

**Alternative:**
Move monitoring site to a riffle or rapid section upstream or downstream where flow is faster and creates tracers.

**Condition 2: Heavily Channelized Sections**

**Characteristics:**
- Concrete-lined channels
- No vegetation nearby
- No bed irregularities to create turbulence
- Uniform flow with no natural tracer sources

**Why unsuitable:**
Engineered channels eliminate natural tracer sources. Smooth surfaces create no turbulence, concrete banks provide no organic debris.

**Alternative:**
Find a natural channel section, or accept that measurement will be challenging and plan for artificial tracer addition during calibration/verification only.

**Condition 3: Very Wide, Shallow Flows**

**Characteristics:**
- River spreads into very wide, shallow sheet flow
- Depth <20cm across most of cross-section
- Flow may be fast but very turbulent and chaotic
- Individual features appear and disappear instantly

**Why unsuitable:**
Extreme turbulence in very shallow water creates features that persist only momentarily. Tracking becomes unreliable.

**Alternative:**
Find a section where flow is concentrated into a deeper channel rather than spread across a wide shallow area.

### Seasonally Unsuitable Conditions

**Condition 1: Late Dry Season in Low-Relief Catchments**

**Characteristics:**
- Minimal flow becomes nearly stagnant
- Water clears completely (no sediment)
- All organic debris has passed downstream
- Surface like glass

**Management approach:**
- Accept that this period will have poor data quality
- Document as known limitation
- Ensure this limitation aligns with monitoring objectives (e.g., flood warning systems don't need accurate dry-season data)
- Plan enhanced verification measurements when flows return

**Condition 2: Ice-Covered Periods**

**Characteristics:**
- Surface ice obscures water
- Cannot see tracers even if flow continues beneath ice

**Management approach:**
- Accept winter data gaps in ice-prone locations
- Consider heated camera housing if winter monitoring is critical (adds cost and complexity)
- Focus deployment on ice-free seasons

[VISUAL PLACEHOLDER: Photos showing unsuitable conditions - deep pool with glassy surface, concrete channel, shallow sheet flow, ice-covered river]

---

## Strategies for Marginal Tracer Conditions

### Optimizing Sites with Borderline Tracer Availability

When a site has marginal but not completely inadequate tracers, several strategies can improve success.

### Strategy 1: Position Measurement Area Downstream of Tracer Sources

**Approach:**
Deliberately position the camera field of view immediately downstream of a tracer-generating feature (rapid, riffle, bridge pier, large rock).

**Example:**
If a bridge crosses the river, position the camera to view the section 10-30 meters downstream of the bridge piers. Flow around the piers generates foam that persists downstream into the measurement area.

**Consideration:**
Ensure the measurement area still has relatively uniform flow (see Section 6.3). Very close to turbulence sources, flow may be too disturbed for accurate cross-sectional velocity averaging.

**Real-world application from Sukabumi:**
At one site, initial camera positioning showed marginal tracers. The team repositioned to capture the area immediately downstream of bridge piers. The pier-generated foam improved tracer availability from marginal to good, enabling reliable measurements.

### Strategy 2: Time Critical Measurements for Favorable Conditions

**Approach:**
If some periods have better tracer conditions than others, schedule important verification measurements during favorable periods.

**Example:**
If morning light is better than harsh midday sun, conduct verification surveys in the morning. If wet season provides better tracers than dry season, prioritize curve development during wet months.

**Consideration:**
This helps with verification and calibration but does not solve continuous monitoring challenges if you need year-round data.

### Strategy 3: Accept Seasonal Data Gaps

**Approach:**
Design the monitoring program to acknowledge that certain periods will have poor data quality, and work around these limitations.

**Example:**
Flood early warning system operates with excellent data during wet season (when floods occur). Late dry season shows data gaps, but this period has no flood risk, so gaps are operationally acceptable.

**Consideration:**
Requires alignment between tracer availability patterns and monitoring objectives. Document limitations clearly so data users understand.

### Strategy 4: Supplement with Alternative Measurements

**Approach:**
Use OpenRiverCam when tracer conditions are good; supplement with alternative methods (manual measurements, stage-only recording) during poor tracer periods.

**Example:**
During late dry season when tracers are insufficient, conduct monthly manual discharge measurements with current meter or ADCP. Use these measurements to verify the rating curve. Continue automated stage recording with rating-curve-based discharge estimates. When tracers return (wet season), resume camera-based velocity measurement.

**Consideration:**
Requires additional equipment and expertise but provides continuity of records.

[VISUAL PLACEHOLDER: Diagram showing camera field of view positioned downstream of bridge pier turbulence source, with foam lines indicated flowing into measurement area]

---

## Tracer Assessment Summary Framework

### Decision-Making Tool for Site Selection

Use this framework to make final tracer-related site selection decisions:

### Assessment Scorecard

**Tracer Density:**
- [ ] Excellent (>20 visible features across river width) - 3 points
- [ ] Good (10-20 features, well distributed) - 2 points
- [ ] Marginal (5-10 features or poorly distributed) - 1 point
- [ ] Poor (<5 features or no distinct features) - 0 points

**Tracer Sources:**
- [ ] Multiple sources (foam + debris + texture) - 3 points
- [ ] Two sources (e.g., foam + debris) - 2 points
- [ ] One reliable source (e.g., foam only) - 1 point
- [ ] No clear tracer sources - 0 points

**Seasonal Reliability:**
- [ ] Expected good tracers year-round - 3 points
- [ ] Expected good tracers during critical monitoring season - 2 points
- [ ] Seasonal gaps during non-critical periods acceptable - 1 point
- [ ] Critical season has poor tracers - 0 points

**Total Score Interpretation:**
- **7-9 points:** Excellent site for tracers - proceed with confidence
- **5-6 points:** Good site - acceptable with documentation of seasonal patterns
- **3-4 points:** Marginal site - consider alternative locations or accept limitations with mitigation strategies
- **0-2 points:** Poor site for tracers - strongly consider alternative location

### Integration with Other Site Criteria

Remember: Excellent tracer availability is necessary but not sufficient for site selection. A site must also meet requirements for:
- Uniform flow (Section 6.2)
- Suitable lighting (Section 6.3)
- Survey accessibility (Section 6.4)
- Plus practical considerations like power, security, permissions

**Site selection decision rule:**
A site with excellent tracers but poor flow uniformity is still unsuitable. All criteria must be satisfied. However, tracers are typically the first assessment because if tracers are completely absent, no other factors matter.

---

## Real-World Example: Sukabumi Site Selection Tracer Assessment

### Application of Assessment Framework

During Sukabumi deployment, the team evaluated three potential sites. Here's how tracer assessment influenced selection:

### Site A: Upstream Natural Section

**Tracer Assessment:**
- **Current conditions (late dry season):** Marginal - minimal foam, sparse debris, some surface texture
- **Sources:** Small riffle 50m upstream provided limited foam, forested banks provided occasional leaves
- **Seasonal prediction:** Wet season expected to provide excellent tracers (rapids would generate significant foam, increased debris from runoff)
- **Score:** 5/9 - Good during wet season, marginal during dry season

**Decision:**
Acceptable for flood warning purpose (wet season data critical). Noted dry season limitations.

### Site B: Downstream of Bridge

**Tracer Assessment:**
- **Current conditions:** Good - bridge pier turbulence generated foam lines, urban debris present, good distribution
- **Sources:** Bridge piers provided consistent turbulence even at low flow, urban area provided steady organic debris input
- **Seasonal prediction:** Expected to remain good year-round due to consistent turbulence from infrastructure
- **Score:** 7/9 - Consistently good across seasons

**Decision:**
Preferred for tracer reliability. Selected as primary site.

### Site C: Channelized Section

**Tracer Assessment:**
- **Current conditions:** Poor - concrete channel, no vegetation, glassy surface, no visible tracers
- **Sources:** No natural tracer sources identified
- **Seasonal prediction:** Unlikely to improve significantly even during wet season
- **Score:** 1/9 - Poor tracer availability

**Decision:**
Eliminated due to insufficient tracers despite having excellent access and security.

**Outcome:**
Site B (downstream of bridge) was selected primarily because of superior and more reliable tracer availability. This decision proved correct during deployment - the site provided consistent measurements even during challenging late dry season conditions.

[VISUAL PLACEHOLDER: Map or diagram showing the three sites with tracer assessment scores and final decision annotations]

---

## Summary: Key Concepts for Tracer Assessment

**Critical principle:**
Without visible tracers, OpenRiverCam cannot measure velocity. Tracer assessment is the first and most fundamental site selection criterion.

**Good tracers have:**
- Sufficient contrast against water surface
- Distribution across the river width
- Persistence for 2-5 seconds
- Movement representative of water flow

**Natural tracer sources:**
- Turbulence-generated foam (most reliable when present)
- Organic debris (varies seasonally)
- Surface ripples and texture (supplementary)
- Sediment patterns (event-driven)

**Assessment process:**
1. Visual observation from camera position
2. Identify tracer sources
3. Evaluate short-term variability
4. Predict seasonal patterns
5. Score using framework
6. Integrate with other site criteria

**Seasonal considerations:**
- Tropical wet/dry: Excellent in wet season, marginal in late dry season
- Temperate: Generally consistent, possible winter challenges
- Ephemeral: Event-driven, excellent during flows

**When tracers are insufficient:**
- Deep, slow pools - select different site
- Concrete channels - find natural section
- Accept seasonal gaps if aligned with monitoring objectives
- Supplement with alternative methods during poor periods

**Decision framework:**
Score site on density (0-3), sources (0-3), and seasonal reliability (0-3). Sites scoring 7-9 are excellent, 5-6 acceptable, 3-4 marginal, 0-2 unsuitable.

**Integration with overall site selection:**
Excellent tracers are necessary but not sufficient. Sites must also meet flow uniformity, lighting, and accessibility requirements (following sections).

---

**Next Section:** [6.2 Lighting and Shadow Considerations](02-lighting-shadows.md)

[VISUAL PLACEHOLDER: One-page visual summary showing:
- Tracer types (photos of foam, debris, ripples)
- Assessment checklist
- Seasonal variation graph
- Decision framework scorecard
- "No tracers = No measurements" key message]
