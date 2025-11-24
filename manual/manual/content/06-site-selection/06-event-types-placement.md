# 6.6 Hydrologic Event Types and Placement Strategy

Not all floods are the same. A rapid flash flood triggered by intense afternoon thunderstorms behaves completely differently from a seasonal flood that rises gradually over two weeks as monsoon rains accumulate. A snowmelt flood follows yet another pattern entirely. Understanding these different flood types is essential for strategic monitoring site placement - because the monitoring requirements for each type are different. This section explains the major flood types you may encounter in humanitarian contexts and how to position monitoring sites to provide effective early warning for each.

By the end of this section, readers will develop the ability to recognize different flood event types and their distinguishing characteristics, understand how flood type fundamentally affects monitoring requirements, position monitoring sites strategically for different event types, integrate river monitoring systems with rainfall data collection, coordinate effectively with existing monitoring stations, and design comprehensive early warning systems capable of addressing diverse flood scenarios.

---

## Review: The Hydrograph Concept

### Understanding How Floods "Look" Over Time

A **hydrograph** is a graph showing how river flow (discharge) changes over time. It is the fundamental tool for understanding flood behavior and planning monitoring strategies.

**The basic shape:**

Imagine a storm occurs in a catchment. Rainfall generates runoff that flows into the river. The hydrograph shows what happens:

1. **Before the storm:** River at base flow (normal low level)
2. **Storm begins:** Water starts entering river, flow begins rising
3. **Peak flow:** Maximum discharge as accumulated runoff reaches the river
4. **Recession:** Flow gradually falls as runoff drains from catchment
5. **Return to base flow:** River returns to normal low level

**Key hydrograph characteristics:**

- **Rising limb:** How quickly flow increases (steep = rapid rise; gentle = slow rise)
- **Peak discharge:** Maximum flow reached
- **Time to peak:** How long from start of rain to peak flow
- **Recession limb:** How quickly flow decreases after peak
- **Duration:** Total time from start of rise to return to base flow

**Why this matters for monitoring:**

Different flood types produce different hydrograph shapes. The shape tells you how to design monitoring and early warning:

- Steep rising limb → Short warning time → Need upstream sites
- Gentle rising limb → Long warning time → Can use downstream sites
- Short duration → Event-specific warnings
- Long duration → Sustained warnings and ongoing monitoring

[VISUAL PLACEHOLDER: Example hydrograph showing:
- X-axis: Time (hours or days)
- Y-axis: Discharge (m³/s)
- Curve showing base flow, rising limb, peak, recession limb
- Key features labeled: time to peak, peak discharge, duration
- Annotations explaining each part]

---

## Flash Flood Events

### Rapid-Onset, Short-Duration Floods

Flash floods are the most dangerous flood type for humanitarian operations. They occur with little warning in small, steep catchments following intense rainfall.

### Flash Flood Characteristics

**Timing:**
- Develop within minutes to hours (typically 1-6 hours) after intense rainfall
- Very short warning time from observable rainfall to peak flood
- Often occur during single storm event (afternoon thunderstorm, intense squall)

**Hydrograph shape:**
- Very steep rising limb (flow can increase 10x or more in 30-60 minutes)
- Short, sharp peak (highest flow lasts minutes to 1-2 hours)
- Relatively rapid recession (though slower than rise)
- Total duration: Hours (typically 3-12 hours from start to return to base flow)

**Catchment characteristics:**
- Small catchments (typically <500 km², often <100 km²)
- Steep terrain (mountains, hills, steep valleys)
- Sparse vegetation or impermeable surfaces (urban areas, degraded land, rocky terrain)
- Short flow paths (rain reaches river quickly)

**Geographic occurrence:**
- Mountain regions (East Africa highlands, Afghanistan, Nepal, Andes)
- Steep coastal areas (Philippines, Indonesia, Pacific islands)
- Urban settings with impermeable surfaces (city drainage, refugee camp runoff)
- Degraded landscapes (deforested catchments, overgrazed semi-arid areas)

**Humanitarian impact:**
- Most deadly flood type (little warning time, extreme velocities)
- Destroys infrastructure rapidly (camps, roads, bridges)
- Catches people in vulnerable locations (sleeping at night, working in fields)
- Difficult to predict precisely (localized thunderstorms hard to forecast)

[VISUAL PLACEHOLDER: Flash flood hydrograph showing:
- Steep rising limb (1-3 hours from base to peak)
- Sharp peak
- Moderate recession
- Total duration ~6-8 hours
- Annotations showing "Intense rainfall event" at start
- Comparison showing discharge rising from 2 m³/s to 45 m³/s in 2 hours]

### Flash Flood Monitoring Strategy

**The fundamental challenge:**

Flash floods develop so quickly that traditional long-distance early warning is impractical. By the time a site 50 km upstream detects rising water, the flood wave has already passed 20 km downstream.

**Monitoring approach:**

Flash flood early warning systems must combine:
1. **Rainfall monitoring** (primary warning trigger)
2. **River monitoring** (confirmation and magnitude assessment)
3. **Very local placement** (near at-risk communities)

**Rainfall monitoring as primary warning:**

For flash floods, rain gauges upstream of the community often provide better early warning than river monitoring alone.

**Why:** Rainfall precedes runoff by 30 minutes to 2 hours in small catchments. Detecting rainfall in the catchment provides the earliest possible warning that a flood is developing.

**Rain gauge placement:**
- Distributed across upstream catchment
- Positioned to detect intense storms before runoff reaches river
- Automatic gauges with real-time transmission (manual readings too infrequent)

**River monitoring as confirmation and magnitude:**

OpenRiverCam sites complement rainfall monitoring by:
- Confirming that rainfall is actually generating significant runoff (not all storms cause floods)
- Measuring flood magnitude (how high will it be?)
- Providing ongoing situation awareness as event develops

**River monitoring site placement for flash floods:**

**Principle 1: Close to at-risk area (5-20 km upstream)**

Flash floods move fast. A site 50 km upstream provides insufficient warning because flood wave travels 50 km in 3-6 hours - not enough time for response.

Position sites:
- 5-10 km upstream for very steep, fast rivers (1-2 hour warning)
- 10-20 km upstream for moderate terrain (2-4 hour warning)
- Closer is better if it still allows protective action time

**Principle 2: Multiple small sites rather than one regional site**

Each vulnerable community or camp location may need its own monitoring because flash flood conditions are highly localized. A storm producing catastrophic flooding on one tributary may not affect the adjacent tributary 15 km away.

Budget permitting, deploy:
- One site per at-risk community
- Sites on different tributaries even if distances are short
- Sites monitoring small, local catchments rather than regional rivers

**Principle 3: Integration with rainfall monitoring**

Design the system as an integrated network:

**Tier 1 - Rainfall detection (earliest warning):**
- Rain gauges distributed across catchment
- Alert when intense rainfall detected (e.g., >20mm in 1 hour)
- Warning message: "Heavy rainfall upstream - prepare for possible flood"

**Tier 2 - River level initial rise (confirmation):**
- OpenRiverCam detects water level rising above threshold
- Alert confirms runoff is occurring
- Warning message: "River level rising - flood developing, take protective action"

**Tier 3 - River level critical threshold (final warning):**
- Water level reaches known flood threshold
- Alert provides flood magnitude estimate
- Warning message: "Severe flooding imminent - evacuate immediately"

**Example deployment for flash flood context:**

**Setting:** Refugee camp in valley below steep mountain catchment (catchment area 85 km²). Flash floods from afternoon thunderstorms are primary threat.

**Monitoring network:**

**3 tipping bucket rain gauges:**
- Positioned across upper catchment (15-25 km from camp)
- Alert threshold: >15 mm in 30 minutes or >25 mm in 1 hour
- Warning time: 1-3 hours before flood peak at camp

**1 OpenRiverCam site:**
- Positioned 8 km upstream of camp on main river
- Alert threshold Level 1: Water level >1.2 m (moderate flood developing)
- Alert threshold Level 2: Water level >1.8 m (severe flood imminent)
- Warning time: 1.5-2.5 hours before peak at camp

**Operational protocol:**

1. Rain gauge triggers: Camp leadership receives "Prepare" alert, monitors situation
2. River monitoring confirms rising level: Camp leadership issues "Take Action" alert, begin protective measures
3. River level reaches critical threshold: "Evacuate Now" alert, final clearance of at-risk areas

**Result:** Combined rainfall + river monitoring provides 1-3 hours actionable warning for flash floods despite limited upstream distance.

[VISUAL PLACEHOLDER: Diagram showing:
- Steep mountain catchment
- Three rain gauge locations in upper catchment
- River monitoring site 8 km upstream of camp
- Camp location at downstream end
- Flow direction arrows
- Warning timeline showing: Rain detected (T-3h) → River rising (T-2h) → Critical level (T-1h) → Flood peak at camp (T-0)
- Annotation showing monitoring tiers]

### Flash Flood Site Selection Checklist

**Assessing sites for flash flood monitoring:**

- [ ] **Proximity:** Site is 5-20 km upstream of at-risk area (provides 1-4 hour warning based on terrain)
- [ ] **Local catchment:** Site monitors local tributary or small river, not distant regional catchment
- [ ] **Rainfall integration:** Rainfall monitoring available or planned for upstream catchment
- [ ] **Rapid data transmission:** Site can transmit data every 10-30 minutes (critical for fast-changing conditions)
- [ ] **Event-specific thresholds:** Clear alert thresholds established based on local flood history
- [ ] **Community-specific:** Site specifically monitors area threatening this community (not general regional monitoring)
- [ ] **Complementary sites:** If resources allow, multiple sites cover different tributaries or sub-catchments

**Red flags (unsuitable for flash flood warning):**

- Site is >30 km upstream (warning time insufficient for flash flood response)
- Site monitors large regional catchment (averages out localized intense storms)
- Data transmission only daily or less (too infrequent for rapidly changing flash floods)
- No rainfall monitoring in catchment (river monitoring alone insufficient for very short lead times)

[VISUAL PLACEHOLDER: Checklist with good/poor examples showing:
- Good: Close site (8 km) with rain gauges
- Poor: Distant site (45 km) with no rainfall monitoring]

---

## Seasonal Riverine Floods

### Slow-Onset, Long-Duration Floods

Seasonal floods are the most common flood type in many humanitarian contexts. They develop over days or weeks as monsoon rains or extended wet seasons generate widespread runoff.

### Seasonal Flood Characteristics

**Timing:**
- Develop over days to weeks (typically 3-30 days from rainfall onset to peak)
- Long warning time from early indicators to peak flood
- Often follow predictable seasonal patterns (monsoon timing, wet season months)

**Hydrograph shape:**
- Gentle rising limb (flow increases steadily over days)
- Broad peak (maximum flow may persist for days or weeks)
- Very slow recession (can take weeks to return to normal flow)
- Total duration: Weeks to months (wet season floods may sustain high levels for 2-4 months)

**Catchment characteristics:**
- Large catchments (typically >1,000 km², often >10,000 km²)
- Gentle to moderate terrain (large river floodplains, lowland areas)
- Multiple tributary contributions (many streams join to create cumulative runoff)
- Long flow paths (rain takes days to reach main river and travel downstream)

**Geographic occurrence:**
- Major river basins (Ganges, Brahmaputra, Mekong, Niger, Zambezi)
- Monsoon-affected regions (South Asia, Southeast Asia, West Africa)
- Tropical lowlands (Amazon, Congo basin)
- Anywhere with seasonal rainfall patterns and large river systems

**Humanitarian impact:**
- Affects millions of people (floods vast areas)
- Extended displacement (floodwaters persist for weeks)
- Agricultural devastation (crops submerged for extended periods)
- Infrastructure disruption (roads, bridges, water systems flooded)
- Disease outbreaks (standing water, contamination)
- BUT: Lower mortality than flash floods (warning time allows evacuation)

[VISUAL PLACEHOLDER: Seasonal flood hydrograph showing:
- Gentle rising limb (1-2 weeks from base to peak)
- Broad, sustained peak (2-4 weeks at or near maximum)
- Very slow recession (4-8 weeks declining)
- Total duration 2-3 months
- Annotations showing "Monsoon rainfall period" spanning entire event
- Comparison showing discharge rising from 350 m³/s to 2,800 m³/s over 12 days]

### Seasonal Flood Monitoring Strategy

**The fundamental advantage:**

Seasonal floods develop slowly, providing substantial time for early warning. This allows monitoring sites to be positioned strategically for maximum catchment representation rather than purely for proximity.

**Monitoring approach:**

Seasonal flood early warning systems emphasize:
1. **Basin-scale monitoring** (large catchment coverage)
2. **Upstream sentinel sites** (early indicators of developing conditions)
3. **Network of coordinated sites** (comprehensive system understanding)
4. **Integration with forecasting** (prediction models using upstream data)

**Site placement for seasonal floods:**

**Principle 1: Upstream sentinel sites (50-200 km upstream or more)**

Position monitoring sites far upstream to detect early stages of flood development.

**Why:** Seasonal floods develop over days. A site 100 km upstream may provide 3-7 days warning as the flood wave travels downstream. This is adequate time for:
- Pre-positioning emergency supplies
- Evacuating large populations in organized manner
- Fortifying infrastructure (sandbagging, raising equipment)
- Activating response coordination

Position sentinel sites:
- On main river upstream of major population centers
- 50-200 km upstream depending on river size and flow velocity
- At locations that capture basin-wide rainfall patterns

**Principle 2: Downstream operational sites (near at-risk areas)**

Position additional sites near population centers for operational decision-making.

**Why:** While upstream sites provide early warning, downstream sites provide precise, local information for final operational decisions:
- Exact flood magnitude at the community location
- Rate of rise in the final hours before peak
- Verification of upstream predictions

Position operational sites:
- 10-30 km upstream of at-risk communities (1-2 days warning)
- Directly representing local conditions
- Downstream of major tributary junctions (captures combined flow)

**Principle 3: Network of multiple sites**

Seasonal flood monitoring is most effective with cascading networks of sites along the river.

**Why:** Multiple sites allow:
- Tracking flood wave as it moves downstream
- Refining forecasts as event develops
- Redundancy if one site fails
- Understanding tributary contributions

**Example network:**

**River system:** 800 km from headwaters to at-risk community
**Catchment:** 48,000 km² at community location

**Site 1 - Upper basin sentinel (500 km upstream of community):**
- Catchment: 12,000 km²
- Purpose: Early detection of basin-wide flood development
- Warning time: 5-8 days before peak at community
- Alert message: "Basin-wide flooding developing - prepare for major flood event"

**Site 2 - Mid-basin tributary junction (250 km upstream):**
- Catchment: 28,000 km² (includes major tributary)
- Purpose: Confirm magnitude and track flood wave progression
- Warning time: 3-5 days before peak at community
- Alert message: "Major flood confirmed - peak expected in 3-5 days"

**Site 3 - Lower basin operational (40 km upstream):**
- Catchment: 45,000 km² (nearly full catchment)
- Purpose: Precise local forecasting and final operational decisions
- Warning time: 1-2 days before peak at community
- Alert message: "Flood peak approaching - final evacuation window"

**Site 4 - Community location (optional):**
- Catchment: 48,000 km² (full catchment)
- Purpose: Real-time monitoring during event, verification for future events
- Warning time: None (at community) but provides real-time situation awareness
- Information: Actual flood levels for response operations

**Operational use:**

**Day 1:** Site 1 detects water level rising above seasonal average
- Forecast: Significant flood developing
- Action: Humanitarian partners begin preparedness (pre-position supplies, alert staff)

**Day 3:** Site 2 confirms major flood wave, magnitude higher than typical
- Forecast: Major flood expected, peak in 4-6 days
- Action: Issue early warning to communities, begin evacuation planning

**Day 5:** Site 3 detects flood wave arrival, level consistent with predictions
- Forecast: Peak expected in 36-48 hours, level projected at 4.2-4.5m
- Action: Final evacuation, move assets to high ground

**Day 7:** Sites 3 and 4 measure actual peak, 4.4m (within forecast range)
- Information: Real-time flood extent for response operations
- Action: Deploy emergency assistance to affected areas

**Result:** Cascading network provides progressive warning with increasing precision, allowing well-planned response.

[VISUAL PLACEHOLDER: Map showing:
- 800 km river from headwaters to community
- Four monitoring sites marked with catchment areas
- Timeline showing warning progression: Day 1 (Site 1 alert) → Day 3 (Site 2 confirmation) → Day 5 (Site 3 final warning) → Day 7 (peak at community)
- Table showing each site's catchment, warning time, purpose]

**Principle 4: Integration with regional forecasting**

Seasonal floods often occur across entire regions simultaneously. Individual site monitoring is most valuable when integrated with:

- **Rainfall forecasts:** Meteorological forecasts predict rainfall 3-7 days ahead, indicating flood potential
- **Satellite monitoring:** Regional flood extent mapping (Google Flood Hub, GloFAS) provides context
- **National gauge networks:** Data from government hydrological services supplements humanitarian sites

**Integration approach:**

Use OpenRiverCam sites as local "ground truth" to verify and refine regional forecasts. Regional systems predict general conditions; local monitoring provides specific, actionable data.

**Example:** GloFAS predicts "Major flooding along Mekong River basin in 5-7 days." Your OpenRiverCam site at Location X measures actual magnitude and timing for that specific location, enabling precise local response planning.

### Seasonal Flood Site Selection Checklist

**Assessing sites for seasonal flood monitoring:**

- [ ] **Upstream positioning:** Sentinel site is 50-200+ km upstream of at-risk area (provides multi-day warning)
- [ ] **Large catchment representation:** Site monitors basin-scale conditions (>1,000 km² catchment typical)
- [ ] **Downstream of tributaries:** Site captures combined flow from major tributaries
- [ ] **Network coordination:** Site is part of cascading network or coordinates with other monitoring
- [ ] **Reliable data transmission:** Site transmits data 2-4 times daily minimum (every 1-6 hours ideal)
- [ ] **Seasonal operational planning:** Site installation and maintenance planned for dry season; autonomous operation during wet season
- [ ] **Regional forecast integration:** Site data can feed into or verify regional forecasting systems

**Optimization opportunities:**

- National gauge network exists: Coordinate with existing sites rather than duplicate
- Bridge or infrastructure exists at good location: Leverage for site installation
- Multiple humanitarian partners: Collaborate on multi-site network costs

[VISUAL PLACEHOLDER: Checklist with optimization notes and coordination recommendations]

---

## Snowmelt Flood Events

### Temperature-Driven, Predictable Floods

Snowmelt floods are common in mountain regions and temperate climates where winter snowpack accumulates and melts in spring/summer. While less common in typical humanitarian contexts, they occur in Afghanistan, Central Asia, Andes regions, and highland areas.

### Snowmelt Flood Characteristics

**Timing:**
- Seasonal pattern (spring/early summer in temperate climates; varies in tropics with altitude)
- Develops over weeks as temperatures rise
- Highly predictable timing (snowmelt occurs same months each year)
- Daily cycles (melt during warm afternoons, reduced flow at night)

**Hydrograph shape:**
- Very gradual rising limb (weeks of increasing flow)
- Sustained high flows (weeks to months of elevated discharge)
- Slow recession (gradual decline as melt season ends)
- Daily oscillations (diurnal cycles from day/night temperature changes)
- Total duration: Months (entire melt season)

**Catchment characteristics:**
- Mountain headwaters (snow accumulation at high elevation)
- Temperature-driven (warm air melts snow)
- Elevation gradients (melt progresses from low to high elevations through season)
- Often large catchments (major rivers sourced from mountain ranges)

**Geographic occurrence:**
- Mountain regions (Afghanistan highlands, Tajikistan, Kyrgyzstan, Peru, Bolivia)
- Temperate regions with winter snow (rare in typical humanitarian contexts)
- High-altitude tropical areas (East Africa highlands with seasonal snow)

**Humanitarian impact:**
- Generally lower risk than flash or seasonal floods (very predictable, slow development)
- Agricultural impacts (timing affects planting, irrigation availability)
- Infrastructure vulnerability (bridges, water intakes designed for base flow, not peak melt)
- Water resource opportunity (melt provides dry-season water, but over-extraction risks)

[VISUAL PLACEHOLDER: Snowmelt hydrograph showing:
- Very gradual rising limb over 4-6 weeks
- Sustained peak lasting 6-10 weeks
- Slow recession over 6-8 weeks
- Diurnal oscillations visible (small daily peaks and troughs)
- Total duration 4-6 months
- Annotations showing temperature trend and snow accumulation/depletion]

### Snowmelt Flood Monitoring Strategy

**The fundamental characteristic:**

Snowmelt floods are highly predictable. Monitoring strategy emphasizes understanding magnitude and resource availability rather than surprise early warning.

**Monitoring approach:**

Snowmelt flood monitoring focuses on:
1. **Snowpack assessment** (how much snow accumulated? How much water will it release?)
2. **Temperature monitoring** (when will melt accelerate?)
3. **River flow monitoring** (real-time melt contributions)
4. **Water resource management** (optimizing use of melt water)

**Site placement for snowmelt monitoring:**

**Principle 1: High-elevation sites for early indication**

Position sites in upper catchment where snowmelt begins earliest.

**Why:** Melt progresses from low to high elevations through the season. Monitoring where melt begins provides indication of total melt potential and seasonal timing.

Position sites:
- In headwater areas where snowpack accumulates
- At elevation where melt begins (not highest peaks where snow persists longest)
- Purpose: Early-season flow indicates melt season strength

**Principle 2: Mid-elevation sites for total contribution**

Position sites where snowmelt from upper catchment combines.

**Why:** These sites measure total melt contribution from snowpack, providing information for water resource management.

Position sites:
- Downstream of snow accumulation zone, before major lowland tributaries join
- Purpose: Measure specifically the snowmelt contribution (separating it from rainfall-generated flow)

**Principle 3: Downstream operational sites for combined resource**

Position sites where snowmelt combines with other water sources.

**Why:** Downstream users (communities, agriculture, camps) need to know total available water, not just snowmelt component.

Position sites:
- Near extraction or use points
- Downstream of all contributing sources
- Purpose: Operational management of water resource

**Example deployment for snowmelt context:**

**Setting:** Valley community in Afghanistan relies on snowmelt from mountains for dry-season irrigation. Excessive melt causes occasional flooding of lowland fields.

**Monitoring objectives:**
1. Predict peak melt timing and magnitude (flood risk, irrigation planning)
2. Monitor total water availability (irrigation allocation)
3. Manage seasonal reservoir operation

**Monitoring network:**

**Site 1 - Upper catchment (elevation 2,800m, in primary melt zone):**
- Catchment: 180 km² (mostly high-elevation snowpack area)
- Purpose: Early indication of melt season strength and timing
- Information: First sustained flow increase indicates melt season onset
- Decision support: Predict irrigation water availability for season

**Site 2 - Mid-catchment (elevation 1,600m, below snow zone, before lowland tributaries):**
- Catchment: 520 km² (captures most snowmelt, minimal rainfall contribution)
- Purpose: Quantify total snowmelt contribution
- Information: Peak flow at this site indicates total melt volume
- Decision support: Allocate irrigation quotas, predict flood risk

**Site 3 - Lower catchment (elevation 950m, near community and irrigation intakes):**
- Catchment: 2,100 km² (snowmelt + rainfall + groundwater)
- Purpose: Operational water management
- Information: Current available flow for irrigation extraction
- Decision support: Daily irrigation scheduling, flood threshold monitoring

**Operational use:**

**Early season (March):** Site 1 detects first sustained flow increase
- Information: Melt season beginning on schedule
- Decision: Prepare irrigation infrastructure for season

**Mid-season (April-May):** Site 2 measures peak melt flows
- Information: Peak melt is 35 m³/s, within normal range
- Decision: Allocate seasonal irrigation quotas, flood risk low

**Late season (June-July):** Site 3 monitors declining flows as melt ends
- Information: Flow dropping to 8 m³/s by late July
- Decision: Reduce irrigation extraction to maintain minimum river flows

**Result:** Multi-site network provides seasonal planning information, operational management data, and flood risk assessment.

[VISUAL PLACEHOLDER: Elevation profile showing:
- Mountain snowpack at top (elevation 3,500m)
- Site 1 at 2,800m (primary melt zone)
- Site 2 at 1,600m (below snow, above lowland)
- Site 3 at 950m (community level)
- Flow arrows showing melt contribution
- Table showing each site's purpose and decision support]

### Temperature-Flow Relationship

**Unique to snowmelt: Temperature is the primary driver.**

Unlike rainfall-driven floods where precipitation causes runoff, snowmelt floods are temperature-driven. Warm temperatures melt snow; cool temperatures slow melt.

**Diurnal (daily) cycling:**

On warm, sunny days:
- Afternoon temperatures peak (2-4 PM)
- Melt accelerates
- River flow peaks 4-8 hours later (evening/night) as melt water reaches river

On cool, cloudy days:
- Temperatures remain low
- Minimal melt
- River flow decreases

**Monitoring implication:**

If your monitoring objective is understanding snowmelt patterns, combining temperature monitoring with river flow monitoring provides comprehensive understanding:

- High temperature + rising flow = Active melt
- High temperature + flow not rising = Melt not yet reaching river (early season, snow far from streams)
- Low temperature + declining flow = Melt paused
- Rising flow despite cool weather = Rainfall, not melt (different flood risk)

**Simple temperature monitoring:** Low-cost temperature loggers can be deployed alongside OpenRiverCam to provide this additional context.

### Snowmelt Monitoring Checklist

**Assessing sites for snowmelt monitoring:**

- [ ] **Elevation strategy:** Sites positioned at appropriate elevations (high for early indication, mid for melt quantification, low for operational use)
- [ ] **Snowpack representation:** Upper sites in areas with reliable snowpack accumulation
- [ ] **Isolation of melt contribution:** At least one site captures primarily snowmelt, not rainfall
- [ ] **Operational relevance:** Lower site(s) positioned for water resource management decisions
- [ ] **Temperature data:** Temperature monitoring available or planned (understanding melt drivers)
- [ ] **Seasonal patterns understood:** Historical melt timing and magnitude documented for comparison
- [ ] **Diurnal variability acceptable:** Monitoring frequency captures daily melt cycles (measurements every 2-6 hours)

**Snowmelt-specific considerations:**

- Timing is predictable: Installation and maintenance can be planned well in advance
- Water resource management often more important than flood warning
- Integration with temperature monitoring improves understanding significantly

[VISUAL PLACEHOLDER: Elevation-based site strategy diagram with checklist]

---

## Upstream vs. Downstream Placement Trade-offs

### Strategic Positioning for Different Objectives

The decision to place monitoring sites upstream vs. downstream involves fundamental trade-offs that apply across all flood types.

### The Core Trade-Off

**Upstream placement:**

**Advantages:**
- Longer warning time (water must travel distance to reach downstream location)
- Earlier indication of developing events
- Potential to inform multiple downstream locations from one site

**Disadvantages:**
- May not represent full catchment (tributaries join downstream of site)
- Measurements less directly applicable to specific downstream location
- Channel changes between site and downstream location affect forecast accuracy
- Difficult to verify if very far from population centers

**Downstream placement:**

**Advantages:**
- Directly represents conditions at or near at-risk location
- Includes all upstream tributary contributions
- Measurements more precise for local decision-making
- Easier to verify and maintain if near communities

**Disadvantages:**
- Shorter warning time
- Site-specific (only monitors one location, not multiple downstream areas)
- May arrive too late for protective action if event develops rapidly

[VISUAL PLACEHOLDER: Diagram showing river with upstream and downstream site options, with pros/cons listed for each position, and warning time arrows]

### Balancing Warning Time and Representativeness

**The optimal balance depends on flood type and operational needs:**

**For flash floods:**
- **Priority:** Representativeness > Warning time
- **Reasoning:** Flash floods develop so fast that even short warning is valuable; measuring the right catchment is critical
- **Strategy:** Downstream placement (5-20 km upstream, maximize representativeness)

**For seasonal floods:**
- **Priority:** Warning time ≈ Representativeness (both important)
- **Reasoning:** Long development time allows upstream placement without sacrificing too much representativeness
- **Strategy:** Upstream sentinel sites (50-200 km) + downstream operational sites (10-30 km)

**For snowmelt floods:**
- **Priority:** Representativeness > Warning time
- **Reasoning:** Events are highly predictable; resource quantification more important than early warning
- **Strategy:** Downstream placement focused on operational water management

### Decision Framework: Upstream vs. Downstream

**Step 1: Define minimum acceptable warning time**

Ask: "What is the shortest warning time that allows effective protective action?"

- Evacuation: Typically 2-6 hours minimum
- Agricultural protection (move livestock, harvest crops): 6-24 hours
- Infrastructure preparation: 12-48 hours
- Water resource planning: Days to weeks

**Step 2: Calculate travel time from potential sites**

Estimate how long water takes to travel from site to at-risk location:
- Fast mountain rivers: 5-10 km/hour
- Moderate rivers: 2-5 km/hour
- Large, slow rivers: 1-3 km/hour

**Step 3: Identify upstream site that meets minimum warning time**

Find the closest site that provides minimum warning time.

**Example:**
- Minimum warning needed: 3 hours
- River travel speed: 4 km/hour
- Minimum upstream distance: 3 hours × 4 km/hour = 12 km

**Step 4: Assess representativeness at that distance**

Ask:
- [ ] Are major tributaries included? (If not, site underestimates flow)
- [ ] Is catchment character similar? (Steep vs. flat, forested vs. bare, etc.)
- [ ] Do rainfall patterns at site correlate with rainfall at at-risk location?

**Step 5: Adjust position to optimize balance**

**If representativeness is poor:**
- Move site downstream to improve representativeness
- Accept shorter warning time
- Supplement with rainfall monitoring to extend effective warning time

**If warning time is excessive:**
- Consider moving site downstream
- Use resources for multiple sites instead of one distant site
- Ensure operational site near at-risk area even if sentinel site is far upstream

**Outcome:** Select site position that balances warning time and representativeness for your specific operational needs and flood type.

[VISUAL PLACEHOLDER: Decision framework flowchart showing steps from defining warning time to final site selection, with decision points and adjustments]

---

## Integration with Rainfall Monitoring

### Combining River Flow and Rainfall Data

River monitoring alone provides incomplete information. Rainfall monitoring upstream of river sites dramatically improves early warning capability, especially for flash floods.

### Why Rainfall Monitoring Matters

**The relationship:**

Rainfall → Runoff → River flow

Rainfall is the cause; river flow is the effect. Monitoring both allows:

1. **Earlier warning:** Rain gauges detect rainfall before runoff reaches river (30 min - 6 hours earlier depending on catchment size)
2. **Improved forecasts:** Knowing how much rain has fallen allows prediction of how much flow will result
3. **Event characterization:** Distinguish flood types (intense local storm vs. widespread regional rain)
4. **Verification:** Understand why river flows are changing (recent rainfall vs. upstream release vs. anomaly)

**Strategic principle:**

River monitoring sites answer "What is happening in the river now?"
Rainfall monitoring answers "What will happen in the river soon?"

Combined monitoring provides comprehensive early warning.

### Rainfall Gauge Placement Strategy

**For integration with river monitoring:**

**Principle 1: Upstream of river monitoring site**

Position rain gauges in the catchment area that drains to your river monitoring site, upstream of the site.

**Why:** Rainfall in this area will generate runoff that flows past your river monitoring site. You can observe the rainfall-runoff relationship and use rainfall as a leading indicator.

**Principle 2: Distributed across catchment**

Position multiple gauges across the catchment rather than clustering them.

**Why:** Rainfall is spatially variable. One gauge may miss a localized storm that another gauge 10 km away detects. Distributed gauges capture catchment-average rainfall more accurately.

**Typical spacing:**
- Small catchments (<100 km²): 2-3 rain gauges
- Moderate catchments (100-500 km²): 3-5 rain gauges
- Large catchments (>500 km²): 5-10 rain gauges, or supplement with regional radar/satellite data

**Principle 3: Prioritize upper catchment**

If gauge numbers are limited, prioritize upper catchment areas where runoff originates.

**Why:** Rainfall in headwaters has the longest travel time to river mouth, providing maximum early warning. Rainfall near river mouth contributes immediately with minimal warning time.

**Example integrated network:**

**Setting:** Flash flood early warning for camp on small river (catchment 145 km², steep terrain)

**River monitoring:** 1 OpenRiverCam site 8 km upstream of camp

**Rainfall monitoring:** 4 tipping bucket rain gauges
- Gauge 1: Upper catchment, 22 km upstream of river site (30 km from camp)
- Gauge 2: Upper catchment, 18 km upstream of river site (26 km from camp)
- Gauge 3: Mid catchment, 12 km upstream of river site (20 km from camp)
- Gauge 4: Lower catchment, 5 km upstream of river site (13 km from camp)

**Warning sequence:**

**T-3 hours:** Gauges 1 and 2 detect intense rainfall (>25 mm in 45 minutes)
- Alert: "Heavy rainfall in upper catchment - possible flash flood developing"
- Action: Camp leadership alerted, prepare for possible evacuation

**T-2 hours:** Gauge 3 detects intense rainfall, storm moving downstream
- Alert: "Intense storm confirmed, flash flood likely"
- Action: Begin moving vulnerable populations to high ground

**T-1.5 hours:** River monitoring site detects rapid water level rise
- Alert: "Flash flood confirmed - evacuate immediately"
- Action: Final evacuation, clear at-risk areas

**T-0:** Flood peak passes camp
- Information: River monitoring provides real-time flood magnitude
- Action: Response operations begin once flood recedes

**Result:** Rainfall monitoring provided 3 hours early indication; river monitoring confirmed magnitude and provided precise timing. Combined network delivered effective early warning.

[VISUAL PLACEHOLDER: Map showing:
- Catchment boundary
- Four rain gauge locations in upper/mid/lower catchment
- River monitoring site
- Camp location
- Warning timeline T-3h to T-0
- Arrows showing rainfall detection, runoff generation, flood wave movement]

### Rainfall Threshold Development

**Using rainfall data for early warning requires establishing thresholds.**

Not all rainfall produces flooding. Thresholds define rainfall intensities or accumulations that generate significant runoff.

**Threshold types:**

**Intensity threshold:** Rainfall rate that produces flash flooding
- Example: >30 mm in 1 hour → Flash flood likely
- Example: >50 mm in 2 hours → Severe flash flood likely

**Accumulation threshold:** Total rainfall over period that produces seasonal flooding
- Example: >100 mm in 5 days → River will rise significantly
- Example: >200 mm in 10 days → Major seasonal flood likely

**Threshold development approaches:**

**Option 1: Historical analysis (data-rich contexts)**
- Analyze past flood events: How much rain fell before each flood?
- Identify patterns: "Every time >35 mm fell in 1 hour, flooding occurred"
- Establish thresholds based on historical relationships

**Option 2: Observed calibration (data-poor contexts)**
- Monitor rainfall and river response during wet season
- Record when river reaches flood levels and how much rain preceded it
- Develop thresholds progressively: "We observed flooding after 28 mm in 1 hour; set threshold at 25 mm to provide margin"

**Option 3: Community knowledge**
- Ask community members: "How much rain needs to fall for the river to flood?"
- Use descriptive thresholds initially: "Heavy rain for 2+ hours usually causes flooding"
- Refine with monitoring data over time

**Practical approach for humanitarian contexts:**

Start with conservative (cautious) thresholds:
- Set initial thresholds based on community knowledge or estimates
- Alert on moderate rainfall first wet season (cast wide net)
- Observe which alerts corresponded to actual flooding
- Refine thresholds in subsequent seasons based on experience

**Example:**
- **Year 1:** Alert on >20 mm in 1 hour (cautious threshold)
  - Result: 8 alerts issued, 3 actual floods occurred
  - Learning: 20 mm threshold produces false alarms; actual floods occurred with >28 mm
- **Year 2:** Adjust threshold to >25 mm in 1 hour
  - Result: 4 alerts issued, 3 actual floods (1 false alarm)
  - Learning: Threshold improved; one false alarm acceptable for safety

**Progressive refinement makes thresholds more accurate while maintaining safety margin.**

[VISUAL PLACEHOLDER: Graph showing:
- X-axis: Rainfall intensity (mm/hour)
- Y-axis: Flood occurrence (yes/no)
- Scattered points showing historical events
- Threshold line drawn at optimal point
- Annotations showing "False alarms" (rain but no flood) and "Missed events" (flood but below threshold)
- Optimal threshold balances false alarms and missed events]

---

## Coordination with Other Monitoring Stations

### Leveraging Existing Infrastructure and Networks

OpenRiverCam sites rarely operate in isolation. Most river basins have some existing monitoring - government gauges, research stations, community systems. Strategic coordination with existing networks multiplies effectiveness and reduces costs.

### Types of Existing Monitoring Infrastructure

**National hydrological networks:**

Most countries have government agencies operating hydrological monitoring networks:
- National meteorological services
- Water resource departments
- Irrigation ministries
- Flood forecasting centers

**Characteristics:**
- Professional-grade equipment (expensive, high-accuracy)
- Long historical records (decades of data)
- Standardized methods and protocols
- BUT: Often sparse coverage, focus on major rivers, limited data sharing

**Research and academic stations:**

Universities and research organizations often operate monitoring sites:
- Academic research projects
- International research programs (USAID, World Bank, research consortia)
- Short to medium-term deployments

**Characteristics:**
- High-quality data
- Innovative methods
- BUT: May be temporary, data not always publicly accessible

**Community-based monitoring:**

Local communities and NGOs sometimes operate simple monitoring:
- Staff gauges with manual reading
- Simple rain gauges
- Community observer networks

**Characteristics:**
- Local knowledge and context
- Sustained by community ownership
- BUT: Variable quality, inconsistent methods, limited technical capacity

**Humanitarian and development organization sites:**

Other humanitarian actors may have monitoring:
- UN agencies (UNICEF water points, WFP flood monitoring)
- International NGOs (IRC, Save the Children, etc.)
- Red Cross/Red Crescent societies

**Characteristics:**
- Operational focus (data used for programs)
- Often temporary (project-specific)
- Variable technical capacity

### Coordination Strategies

**Strategy 1: Data sharing with national networks**

**Approach:**
Coordinate with national hydrological services to share OpenRiverCam data and receive data from government gauges.

**Benefits:**
- Access to long historical records from government sites
- Context for interpreting your site data
- Institutional legitimacy (coordination with government)
- Potential technical support from professionals

**How to implement:**
1. Identify national agency responsible for hydrology (usually meteorological service or water resources ministry)
2. Request meeting to present OpenRiverCam project
3. Propose data sharing: "We will share our data if you share your nearby gauge data"
4. Establish technical contact person for coordination
5. Share data via agreed method (email, shared server, national database)

**Example:**

Humanitarian organization deploys OpenRiverCam site on river where government gauge exists 40 km downstream.

**Coordination:**
- Organization shares upstream data with government agency
- Government shares downstream gauge data with organization
- Combined data improves flood forecasting for both parties
- Government validates OpenRiverCam measurements against professional gauge
- Organization gains confidence in data quality through comparison

**Outcome:** Both parties benefit from expanded network coverage.

**Strategy 2: Fill gaps in existing networks**

**Approach:**
Position OpenRiverCam sites to complement existing gauges rather than duplicate them.

**Benefits:**
- Maximum coverage for available resources
- New data in previously unmonitored locations
- Justification for humanitarian deployment (filling actual gap)

**How to implement:**
1. Map existing gauge network
2. Identify gaps: tributaries not monitored, sections between distant gauges, small catchments unmonitored
3. Position OpenRiverCam to fill high-priority gaps
4. Avoid placing sites very close to existing professional gauges (unless specific calibration/comparison purpose)

**Example:**

**Existing network:**
Government operates gauges at 100 km intervals on main river (Sites A, B, C).

**Gap identified:**
Major tributary joins main river between Sites B and C. Tributary not monitored. Tributary contributes 35% of flow during wet season floods.

**OpenRiverCam deployment:**
Deploy on tributary 15 km upstream of junction with main river.

**Result:**
- Fills critical gap (tributary previously unmonitored)
- Complements existing network (explains flow increases at government Site C)
- Humanitarian organization contributes to national understanding of river system
- Government may incorporate tributary data into flood forecasting

**Strategy 3: Collaborate with other humanitarian actors**

**Approach:**
Coordinate with other humanitarian organizations monitoring the same river or basin.

**Benefits:**
- Share costs of equipment and expertise
- Avoid redundant monitoring
- Integrated early warning serves all actors
- Shared learning and capacity building

**How to implement:**
1. Participate in coordination mechanisms (cluster meetings, working groups)
2. Present monitoring plans and request coordination
3. Identify if other organizations have monitoring plans
4. Agree on division of responsibilities or cost-sharing

**Example:**

**Context:** Three organizations operate in same flood-prone basin:
- Organization A: Refugee camp on main river
- Organization B: Livelihood program in upstream agricultural area
- Organization C: Health program in downstream urban area

**Coordination:**

**Agreement:**
- Organization A deploys OpenRiverCam on main river near camp (central location serves all three)
- Organization B deploys rain gauge network in upper catchment (serves agriculture and provides early warning for downstream partners)
- Organization C contributes to maintenance costs (benefits from monitoring without deploying own system)

**Data sharing:**
- All three organizations access all monitoring data
- Joint interpretation of data during flood events
- Shared early warning messages to communities

**Result:** Comprehensive monitoring network for cost less than if each organization deployed independently.

**Strategy 4: Contribute to research and validation**

**Approach:**
Collaborate with research institutions using your sites for validation or research.

**Benefits:**
- Research institutions may provide technical expertise
- Validation studies improve confidence in OpenRiverCam methods
- Academic publications demonstrate impact
- Potential for equipment or funding support

**How to implement:**
1. Identify research institutions working on hydrology, remote sensing, or humanitarian innovation
2. Offer access to your monitoring sites for research purposes
3. Request technical support or capacity building in exchange
4. Co-author publications or reports documenting results

**Example:**

University research group studying camera-based river monitoring methods requests access to humanitarian organization's OpenRiverCam site for validation study.

**Agreement:**
- University conducts detailed verification measurements (ADCP) at site over one wet season
- University provides technical review of site setup and data quality
- University trains organization staff on advanced data analysis
- Organization provides site access and logistical support
- Both parties co-author paper on humanitarian applications

**Result:** Organization gains technical validation and capacity building; university gains real-world research site and humanitarian impact.

[VISUAL PLACEHOLDER: Diagram showing coordination scenarios:
- National network with OpenRiverCam filling gap
- Multiple humanitarian organizations sharing network
- Research collaboration
- Data flowing between parties]

### Data Sharing Platforms and Protocols

**Technical coordination requires compatible data formats and sharing mechanisms.**

**Recommended approaches:**

**1. Use standard data formats**
- Ensure discharge reported in m³/s (or L/s for very small streams)
- Water level in meters (or cm)
- Timestamps in UTC or clearly specified local time with timezone
- CSV or JSON formats for data exchange (widely compatible)

**2. Cloud-based data sharing**
- OpenRiverCam cloud platform allows guest access (share site link with partners)
- National data platforms may accept contributed data (register site with national agency)
- Shared Google Drive or Dropbox for simple data exchange

**3. Regular reporting**
- Provide weekly or monthly data summaries to partners (not just raw data)
- Include interpretation: "Flow is above seasonal average" or "Low flow conditions continue"
- Highlight anomalies or important events

**4. Real-time alerts**
- Share flood alerts with all relevant partners simultaneously
- Use SMS, email, WhatsApp groups, or coordination platforms
- Include specific information: "Site X: Water level 3.2m at 14:00, rising rapidly, flood threshold expected in 2-3 hours"

**5. Coordination meetings**
- Regular (monthly or quarterly) meetings with partners to review data, discuss system performance, plan maintenance
- Include national agencies, other humanitarians, community representatives
- Share lessons learned and coordinate response planning

[VISUAL PLACEHOLDER: Data sharing workflow diagram showing:
- OpenRiverCam site collecting data
- Cloud platform
- Automatic alerts
- Data shared with: National agency, Partner organizations, Community groups, Research institutions
- Coordination meeting cycle]

---

## Summary: Event-Specific Placement Strategies

**Fundamental principle:**
Different flood types require different monitoring strategies. Site placement must match event characteristics to provide effective early warning.

**Flash floods:**
- **Characteristics:** Rapid onset (1-6 hours), short duration, small catchments, steep terrain
- **Placement strategy:** Close to at-risk area (5-20 km upstream), multiple local sites
- **Integration:** Critical to combine with rainfall monitoring (primary early warning)
- **Warning time:** 1-4 hours typical

**Seasonal floods:**
- **Characteristics:** Slow onset (days to weeks), long duration, large catchments, gentle terrain
- **Placement strategy:** Upstream sentinel sites (50-200 km) + downstream operational sites (10-30 km)
- **Integration:** Coordinate with regional forecasting, national networks
- **Warning time:** Days to weeks typical

**Snowmelt floods:**
- **Characteristics:** Temperature-driven, highly predictable timing, gradual onset and recession
- **Placement strategy:** Elevation-based (high for early indication, low for operational use)
- **Integration:** Combine with temperature monitoring
- **Warning time:** Weeks (highly predictable seasonal pattern)

**Upstream vs. downstream trade-offs:**
- Upstream: Longer warning time, may not represent full catchment
- Downstream: Shorter warning time, better representativeness
- Optimal balance depends on flood type and minimum warning time needed

**Rainfall integration:**
- Provides earliest warning (rainfall precedes runoff)
- Position gauges distributed across catchment, upstream of river sites
- Develop rainfall-flood thresholds through observation
- Critical for flash flood early warning

**Coordination with existing networks:**
- Data sharing with national agencies (access historical data, legitimacy)
- Fill gaps in existing coverage (avoid duplication)
- Collaborate with other humanitarian actors (share costs, integrated warning)
- Contribute to research (validation, capacity building)

**Strategic decision framework:**
1. Identify flood type(s) threatening your area
2. Determine minimum acceptable warning time
3. Calculate upstream distance providing that warning time
4. Assess representativeness at that distance
5. Balance warning time and representativeness
6. Integrate rainfall monitoring if needed (especially flash floods)
7. Coordinate with existing networks to maximize coverage and minimize duplication

**Practical guidance for humanitarian contexts:**

- **Limited resources:** Prioritize one well-positioned site over multiple marginal sites
- **Flash flood risk:** Invest in rainfall monitoring as much as river monitoring
- **Seasonal flood risk:** Coordinate with national agencies, focus on gap-filling
- **Multi-hazard contexts:** Design network to address most critical threat first, expand later
- **Long-term operations:** Build relationships with national agencies and research partners for sustainability

**The goal:** Position monitoring sites strategically to provide actionable early warning for the specific flood hazards facing your communities, using appropriate integration and coordination to maximize effectiveness within resource constraints.

---

**Chapter Complete:** Congratulations! You have completed Chapter 6: Site Selection.

You now understand:
- Technical site requirements (tracers, lighting, flow uniformity, accessibility)
- Strategic placement based on monitoring objectives
- Event-specific strategies for different flood types
- Integration with rainfall monitoring and coordination with existing networks

**Next Chapter:** [Chapter 7: Site Planning and Preparation](../07-site-planning/01-camera-location.md)

This next chapter will guide you through the practical planning process once you have selected a site - determining camera positioning, planning power and communications infrastructure, and preparing for equipment installation.

[VISUAL PLACEHOLDER: One-page visual summary showing:
- Three flood type hydrographs (flash, seasonal, snowmelt) with characteristics
- Placement strategy maps for each flood type
- Upstream vs. downstream trade-off diagram
- Rainfall + river integration example
- Coordination network diagram
- Decision framework flowchart
- "Match monitoring strategy to flood type" key message]
