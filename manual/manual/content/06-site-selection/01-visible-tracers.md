# 6.1 Visible Tracers Requirement

The selection of an appropriate site for OpenRiverCam deployment hinges primarily on a fundamental consideration: whether sufficient visible features exist on the water surface for camera-based tracking. The absence of visible tracers renders velocity measurement impossible through optical methods, as the technique relies entirely on tracking the movement of surface features to infer water velocity (Muste et al., 2008). This section presents systematic guidance for evaluating whether a candidate site possesses adequate surface tracers throughout the annual hydrologic cycle.

Upon completion of this section, practitioners will possess the competencies necessary to evaluate natural tracer availability at candidate sites, comprehend seasonal variations in tracer conditions, identify circumstances where tracers prove insufficient for measurement purposes, and apply tracer-based criteria to site selection decision-making processes.

---

## Review: Why Tracers Matter

### The Foundation of Velocity Measurement

As presented in Section 3.2, OpenRiverCam measures velocity by tracking visible features on the water surface. The camera monitors foam patches, floating debris, ripples, and texture patterns as they move downstream, calculating their travel velocity. These visible features, termed tracers, move with the water and reveal the water's velocity.

**Without tracers, the system cannot measure velocity. Without velocity, it cannot calculate discharge.**

This makes tracer assessment the first and most critical step in site selection. All other site characteristics - access, power availability, security - matter only if the site has adequate tracers.

[VISUAL PLACEHOLDER: Photo showing river with abundant tracers (foam lines, scattered debris, surface texture) with overlay circles highlighting trackable features. Caption: "Abundant natural tracers: foam, debris, and ripples provide multiple features for velocity tracking"]

---

## What Makes Good Tracers: Assessment Criteria

### Visibility Requirements

When evaluating a site, look for tracers that meet these criteria:

**1. Sufficient Contrast**

Features must be visible against the water surface to enable effective tracking. Dark features, such as shadows cast by foam or debris, stand out prominently against light-colored water. Conversely, light features including white foam and reflected sunlight on ripples create clear contrast against dark water. Color variations produced by sediment plumes and organic matter also generate trackable patterns across the water surface.

**How to assess:**

Practitioners should stand at the planned camera position and observe the water surface carefully. The ability to clearly see distinct features with the naked eye serves as a reliable indicator of camera performance; if features cannot be distinguished visually from the camera position, the camera will similarly struggle to detect them (Muste et al., 2008).

**2. Adequate Distribution**

Features should appear across the full width of the river rather than being concentrated near a single bank. Optimal spacing between features is moderate, avoiding both excessive sparsity that limits tracking opportunities and excessive density that causes features to merge and become indistinguishable. Tracers should be present in both the center channel and near the banks to enable comprehensive velocity field characterization.

**How to assess:**

Practitioners should observe whether features appear throughout the entire field of view or are concentrated in specific areas. A useful mental framework involves dividing the river into three sections (left, center, and right) and evaluating whether trackable features are present in all three zones. This spatial distribution assessment helps ensure that velocity measurements will represent the full cross-sectional flow pattern.

**3. Appropriate Persistence**

Features must last long enough to be tracked across multiple video frames to enable velocity calculation. Typically, features need to persist for 2-5 seconds as they move through the field of view. Very short-lived features such as bursting bubbles or momentary ripples provide insufficient temporal continuity for reliable tracking.

**How to assess:**

Practitioners should watch individual features as they float downstream, observing whether they remain visible and distinct as they move or whether they quickly disappear or merge with other features. Features that maintain their identity throughout the measurement zone provide the most reliable velocity data.

**4. Representative Movement**

Features must move with the water rather than being influenced by wind or caught on obstacles. Surface-floating materials prove ideal for velocity measurement, as they faithfully represent surface water velocity. Partially submerged objects may move slower than the surface water, introducing systematic bias into velocity estimates.

**How to assess:**

Practitioners should observe whether features move consistently downstream or are affected by wind gusts. Special attention should be paid to debris caught on rocks or vegetation, as these stationary features could confuse tracking algorithms and produce erroneous velocity measurements. Consistent downstream movement aligned with expected flow patterns indicates suitable tracer behavior.

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

Turbulence-generated foam appears immediately downstream of rapids or riffles, below small waterfalls or drops, around large rocks that create turbulence, and in areas where two channels merge and create mixing zones. These locations provide consistent foam generation whenever sufficient flow exists to create turbulence.

**Seasonal variation:**

Foam becomes more abundant during higher flows when increased water velocity creates greater turbulence. Conversely, foam becomes less abundant during very low flows when water barely trickles over obstacles. Foam generation proves generally reliable except during extreme low-water periods when insufficient flow velocity exists to generate turbulence.

**Assessment questions:**

Practitioners should evaluate whether riffles, rapids, or rocky sections exist upstream of the measurement area. Additional consideration should be given to whether water flows over rocks or obstacles that create turbulence, and whether foam is visible under the current flow conditions during the site visit. These questions help assess the reliability of foam as a tracer source across varying flow conditions.

**Real-world example from Sukabumi:**
During deployment in Indonesia, sites downstream of bridge piers consistently produced excellent foam tracers. The flow around the piers created constant turbulence, generating foam lines that persisted for 50-100 meters downstream. This provided reliable tracers even during moderate dry-season flows.

[VISUAL PLACEHOLDER: Photo from Sukabumi showing foam lines generated by flow around bridge piers, with annotation showing foam trails extending downstream]

### Organic Debris

**What creates it:**
Rivers collect organic material from the surrounding landscape - leaves, twigs, grass, seed pods, flowers, bark fragments - which float on the surface and serve as excellent tracers.

**Where to find it:**

Organic debris accumulates in rivers flowing through forested areas where consistent leaf fall occurs, in agricultural areas during harvest seasons when crop residues enter the water, and in urban areas with vegetation that contributes yard waste and landscaping debris. Rainfall events that wash accumulated material into the river provide episodic pulses of organic debris regardless of land cover type.

**Seasonal variation:**

During the wet season, organic debris proves usually abundant as rainfall washes material into rivers. The early dry season often retains plentiful debris from residual material carried over from wetter periods. However, late dry season conditions can produce scarce debris as accumulated material moves downstream. In temperate climates, autumn provides excellent debris from leaf fall, while spring offers good conditions in many climates due to flowering and new growth.

**Assessment questions:**

Practitioners should determine what type of land cover surrounds the river (forest, agriculture, or urban), observe whether visible organic debris is present on the water during the site visit, and consider whether seasonal changes will dramatically reduce debris availability. Understanding the relationship between watershed characteristics and debris supply helps predict tracer reliability throughout the year.

**Real-world example from Sukabumi:**
Urban river sections received consistent organic tracers from riverside vegetation and street runoff. Even during dry periods, daily influx of leaves and small debris provided adequate tracking features. In contrast, one heavily channelized section with concrete banks and no nearby vegetation showed very sparse debris - making it a less suitable site.

[VISUAL PLACEHOLDER: Photo showing floating organic debris (leaves, twigs) scattered across water surface, with circles highlighting individual trackable items]

### Surface Texture and Ripples

**What creates it:**
Water flowing over an uneven riverbed creates ripples, small waves, and texture patterns on the surface. These patterns create visible contrast that can be tracked even when discrete objects (foam, debris) are scarce.

**Where to find it:**

Surface texture and ripples develop in sections with moderate flow velocity (typically 0.5-2.0 m/s), in rivers with rocky or irregular beds, in areas with subtle depth variations, and in sections where flow moves around obstacles. These conditions create the flow patterns necessary to generate visible surface texture.

**Seasonal variation:**

Surface texture proves generally more pronounced during moderate to high flows but can disappear during very low flows when water becomes glassy. Unlike foam and organic debris, surface texture remains less affected by seasonal vegetation or debris availability, making it a more consistent but often weaker tracer source.

**Assessment questions:**

Practitioners should evaluate whether the water surface shows visible texture or ripple patterns, whether variations in surface appearance are caused by flow patterns, and whether texture would remain visible from the planned camera height and angle. These factors determine whether surface texture can contribute meaningfully to the overall tracer ensemble.

**Limitations:**
Surface texture alone is often insufficient for reliable tracking - it works best as a supplement to foam and debris rather than as the sole tracer source.

[VISUAL PLACEHOLDER: Photo showing river surface with visible ripple texture creating pattern of light and shadow]

### Sediment-Laden Water

**What creates it:**
Rivers carrying high sediment loads often show visible color variations as different sediment concentrations mix. Muddy tributaries entering clearer main channels, or varying sediment from different parts of the channel, create trackable patterns.

**Where to find it:**

Sediment-laden water appears in rivers within erosion-prone catchments including deforested areas, agricultural land, and regions with unstable geology. It occurs during and after rainfall events, where tributaries with different sediment loads merge, and in meandering sections where flow patterns create sediment sorting. These conditions produce the color variations necessary for sediment-based tracking.

**Seasonal variation:**

Sediment tracers prove usually abundant during the wet season when high sediment loads occur, but become often minimal during the dry season as clear water base flow dominates. Sediment availability is fundamentally event-driven, spiking with each rainfall event that mobilizes watershed sediments.

**Assessment questions:**

Practitioners should determine whether the water is visibly turbid or carrying sediment, whether visible plumes or patterns of different sediment concentrations exist, and whether sediment availability is consistent or occurs only during rain events. These assessments help establish whether sediment-based tracers will provide reliable year-round tracking or only episodic measurement opportunities.

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

Practitioners should answer the following questions: Can distinct features be seen on the water surface? How many visible features can be counted in a typical river cross-section? Are features distributed across the full river width or concentrated in certain areas? What types of tracers are present (foam, debris, ripples, sediment patterns)? These fundamental observations establish the baseline tracer assessment.

**Rating scale:**

Sites can be rated as excellent when numerous distinct features appear across the full width (more than 20 visible features in view), good when moderate features are well-distributed (10-20 visible features), marginal when few features exist or distribution is poor (5-10 visible features), or poor when very few or no distinct features are present (fewer than 5 visible features).

**Document:**
Take photos of the water surface from camera position. These will help later comparison and provide visual reference for report documentation.

[VISUAL PLACEHOLDER: Assessment rating scale with example photos showing Excellent/Good/Marginal/Poor conditions]

### Step 2: Tracer Source Identification (5-10 minutes)

Practitioners should identify what is creating the observed tracers.

**Foam sources:**

Practitioners should determine whether rapids, riffles, or rocks are creating turbulence, how far upstream the turbulence source is located, and whether foam persists into the measurement area. These questions assess the reliability of foam generation.

**Organic debris sources:**

The evaluation should identify what vegetation type surrounds the river, whether debris is currently visible on the water, and whether seasonal leaf-fall patterns need to be considered. Understanding vegetation sources helps predict debris availability throughout the year.

**Texture sources:**

Practitioners should assess whether surface texture is visible from the camera position and whether flow velocity creates ripples. These observations determine whether texture can supplement other tracer types.

**Document:**
Note the sources of tracers. Understanding what creates tracers helps predict seasonal variations.

### Step 3: Temporal Variability Assessment (15-30 minutes)

Practitioners should observe how tracer conditions vary even during a short site visit.

**Short-term variability:**

Practitioners should watch for 15-30 minutes to determine whether tracer densities fluctuate significantly. If wind gusts occur during observation, attention should be paid to whether they disrupt tracer movement. Additionally, observers should note whether passing clouds that change light conditions affect visibility. These observations reveal the temporal stability of tracer conditions.

**What this tells you:**
If tracer conditions vary significantly during a 30-minute observation, this suggests the site may have inconsistent measurement conditions. Highly variable conditions are less ideal than consistently moderate conditions.

**Document:**
Note any significant short-term variations and what caused them.

### Step 4: Seasonal Consideration (Research and Discussion)

Consider how tracer conditions will change through the year.

**Research to conduct:**

Practitioners should research the seasonal rainfall pattern, determine when vegetation leaf-fall occurs (if applicable), identify whether extreme low-flow periods exist, and assess whether wet and dry seasons dramatically change river character. This background research provides context for predicting seasonal tracer variations.

**Questions for local knowledge:**

Engaging with community members provides valuable insights. Practitioners should ask what the river looks like during the driest time of year, whether times exist when the water is very clear and calm with nothing floating on it, and when the river carries the most debris. Local knowledge often reveals seasonal patterns that may not be apparent during a single site visit.

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

The wet season (November-March) provides excellent tracers as high flows create turbulence and rainfall washes debris into the river. During the transition to dry season (April-May), tracers remain good as flows remain moderate and debris is still present. The mid dry season (June-August) produces marginal tracers as declining flow reduces turbulence and debris becomes sparse. Late dry season (September-October) generates poor to marginal tracers due to low flows, minimal debris, and potentially glassy surfaces. The return to wet conditions (November) brings rapidly improving conditions as first rains wash accumulated debris into the river.

**Implications for deployment:**

When the primary monitoring purpose is flood warning, excellent tracer availability during the wet season (when floods occur) is most critical. Marginal conditions during late dry season (when floods are impossible) may be acceptable. However, when the purpose is year-round water resource monitoring, late dry season gaps become more problematic and may require alternative measurement strategies.

**Real-world example from Sukabumi:**

Deployment occurred in October (late dry season) when site visits showed marginal tracer conditions with very limited foam and sparse debris. Local discussions revealed this was the worst time of year for tracers. The team accepted this limitation because flood warning was the primary purpose (making wet season coverage critical), even marginal dry-season data provided more information than no monitoring, and the site had infrastructure advantages (bridge mounting and power access) that outweighed seasonal tracer limitations. The team documented late dry season conditions as an "expected low-quality period" and planned additional verification during the transition to wet season.

[VISUAL PLACEHOLDER: Graph showing seasonal tracer quality variation over 12 months for tropical wet/dry pattern, with photos from Sukabumi showing wet vs. dry season differences]

### Temperate Rivers with Year-Round Flow

**Typical pattern:**

Spring (March-May) provides excellent tracers as snowmelt or spring rain creates high flows and organic material from winter accumulation washes downstream. Summer (June-August) maintains good tracers as vegetation growth provides organic material and moderate flows create foam. Autumn (September-November) delivers excellent tracers as leaf fall provides abundant organic debris. Winter (December-February) produces variable conditions depending on freezing; ice can block surface visibility but snow melt events can provide excellent conditions.

**Implications:**
More consistent year-round tracer availability than tropical systems, but winter conditions may create challenges unrelated to tracers (ice, snow covering the camera lens, very short daylight periods).

### Arid/Semi-Arid Rivers with Ephemeral Flow

**Typical pattern:**

Wet events produce excellent tracers as sudden flows mobilize all available debris and create high turbulence. Low flow periods generate poor to non-existent conditions, as minimal or no flow means measurement is impossible regardless of tracer availability.

**Implications:**
These rivers are challenging for any measurement approach. OpenRiverCam may be suitable for capturing flood events (when tracers are excellent) but will have long no-flow periods. The question is less about tracers and more about whether intermittent event-based monitoring meets your needs.

[VISUAL PLACEHOLDER: Three river type comparison showing typical seasonal patterns on timeline graphs]

---

## When Tracers Are Insufficient

### Recognizing Unsuitable Conditions

Some site conditions will never provide adequate tracers. Practitioners must recognize these situations and select a different site location, consider alternative monitoring approaches, or accept data quality limitations with clear documentation.

### Permanently Unsuitable Conditions

**Condition 1: Deep, Slow-Moving Pools**

**Characteristics:**

Deep, slow-moving pools are characterized by very low velocity (less than 0.2 m/s), deep water with minimal turbulence, smooth glassy surfaces, and absence of upstream riffles or rapids to generate foam.

**Why unsuitable:**
Minimal turbulence means no foam generation. Slow movement means debris settles or moves to banks. Surface appears uniform with no trackable features.

**Alternative:**
Move monitoring site to a riffle or rapid section upstream or downstream where flow is faster and creates tracers.

**Condition 2: Heavily Channelized Sections**

**Characteristics:**

Heavily channelized sections feature concrete-lined channels, absence of nearby vegetation, no bed irregularities to create turbulence, and uniform flow with no natural tracer sources.

**Why unsuitable:**
Engineered channels eliminate natural tracer sources. Smooth surfaces create no turbulence, concrete banks provide no organic debris.

**Alternative:**
Find a natural channel section, or accept that measurement will be challenging and plan for artificial tracer addition during calibration/verification only.

**Condition 3: Very Wide, Shallow Flows**

**Characteristics:**

Very wide, shallow flows occur when rivers spread into very wide, shallow sheet flow with depth less than 20 cm across most of the cross-section. Flow may be fast but very turbulent and chaotic, with individual features appearing and disappearing instantly.

**Why unsuitable:**
Extreme turbulence in very shallow water creates features that persist only momentarily. Tracking becomes unreliable.

**Alternative:**
Find a section where flow is concentrated into a deeper channel rather than spread across a wide shallow area.

### Seasonally Unsuitable Conditions

**Condition 1: Late Dry Season in Low-Relief Catchments**

**Characteristics:**

Late dry season conditions in low-relief catchments are characterized by minimal flow that becomes nearly stagnant, water that clears completely (no sediment), organic debris that has all passed downstream, and glass-like surfaces.

**Management approach:**

Practitioners should accept that this period will have poor data quality and document it as a known limitation. The limitation should be aligned with monitoring objectives (for example, flood warning systems do not require accurate dry-season data). Enhanced verification measurements should be planned when flows return to establish rating curve validity.

**Condition 2: Ice-Covered Periods**

**Characteristics:**

Ice-covered periods are characterized by surface ice that obscures water, preventing tracer visibility even if flow continues beneath the ice.

**Management approach:**

Practitioners should accept winter data gaps in ice-prone locations, consider heated camera housing if winter monitoring is critical (recognizing added cost and complexity), and focus deployment on ice-free seasons when optical measurement is feasible.

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

Sites can be scored on tracer density as follows: excellent conditions with more than 20 visible features across river width receive 3 points, good conditions with 10-20 well-distributed features receive 2 points, marginal conditions with 5-10 features or poorly distributed features receive 1 point, and poor conditions with fewer than 5 features or no distinct features receive 0 points.

**Tracer Sources:**

Scoring for tracer sources ranges from 3 points for multiple sources (foam plus debris plus texture), 2 points for two sources (such as foam plus debris), 1 point for one reliable source (such as foam only), to 0 points for no clear tracer sources.

**Seasonal Reliability:**

Seasonal reliability scoring awards 3 points when good tracers are expected year-round, 2 points when good tracers are expected during the critical monitoring season, 1 point when seasonal gaps occur during non-critical periods but remain acceptable, and 0 points when the critical season has poor tracers.

**Total Score Interpretation:**

Scores of 7-9 points indicate an excellent site for tracers where practitioners can proceed with confidence. Scores of 5-6 points represent a good site that is acceptable with documentation of seasonal patterns. Scores of 3-4 points suggest a marginal site where alternative locations should be considered or limitations accepted with mitigation strategies. Scores of 0-2 points indicate a poor site for tracers where alternative locations should be strongly considered.

### Integration with Other Site Criteria

Excellent tracer availability is necessary but not sufficient for site selection. A site must also meet requirements for uniform flow (Section 6.2), suitable lighting (Section 6.3), survey accessibility (Section 6.4), plus practical considerations including power, security, and permissions.

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

Good tracers demonstrate sufficient contrast against the water surface, distribution across the river width, persistence for 2-5 seconds, and movement representative of water flow.

**Natural tracer sources:**

Natural tracer sources include turbulence-generated foam (most reliable when present), organic debris (which varies seasonally), surface ripples and texture (supplementary), and sediment patterns (event-driven).

**Assessment process:**

The assessment process involves visual observation from the camera position, identification of tracer sources, evaluation of short-term variability, prediction of seasonal patterns, scoring using the framework, and integration with other site criteria.

**Seasonal considerations:**

Tropical wet and dry systems provide excellent tracers in the wet season but marginal tracers in the late dry season. Temperate systems prove generally consistent but may face winter challenges. Ephemeral systems are event-driven and provide excellent tracers during flows.

**When tracers are insufficient:**

When deep, slow pools are encountered, practitioners should select a different site. When concrete channels are present, a natural section should be found. Seasonal gaps may be acceptable if aligned with monitoring objectives. Alternative methods can supplement measurements during poor periods.

**Decision framework:**

Sites should be scored on density (0-3 points), sources (0-3 points), and seasonal reliability (0-3 points). Sites scoring 7-9 points are excellent, 5-6 points are acceptable, 3-4 points are marginal, and 0-2 points are unsuitable.

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
