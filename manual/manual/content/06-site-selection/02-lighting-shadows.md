# 6.2 Lighting and Shadow Considerations

A camera-based measurement system lives or dies by lighting conditions. Even with excellent tracers and perfect flow characteristics, poor lighting can make the water surface invisible to the camera. This section provides practical guidance for evaluating lighting conditions at potential sites and understanding how lighting affects measurement quality throughout the day and across seasons.

By the end of this section, you will be able to:
- Recognize optimal and problematic lighting conditions
- Assess how sun angle affects measurement quality
- Evaluate shadow impacts on the camera field of view
- Predict seasonal lighting variations
- Make informed site selection decisions based on lighting requirements

---

## Why Lighting Matters for Camera-Based Measurement

### The Camera's Challenge

Human eyes are remarkably adaptable. You can see clearly in bright sunlight, at dusk, and even in dim indoor lighting. Your brain automatically adjusts to varying light levels and compensates for glare.

Cameras are less forgiving. While modern cameras have improved dynamic range and light sensitivity, they still struggle with:
- **Extreme contrast:** Very bright and very dark areas in the same image
- **Direct glare:** Sunlight reflecting directly into the lens
- **Insufficient light:** Low-light conditions that create grainy, low-contrast images
- **Rapidly changing conditions:** Clouds passing causing sudden brightness changes

For OpenRiverCam to track surface features, the camera must produce clear images showing distinct tracers against the water surface. Poor lighting undermines this in multiple ways.

[VISUAL PLACEHOLDER: Side-by-side comparison - same river scene under good lighting (clear, distinct features visible) vs. poor lighting (washed out, features indistinguishable)]

### How Lighting Affects Tracer Visibility

**Good lighting conditions:**
- Tracers (foam, debris, ripples) appear as distinct features
- Sufficient contrast between tracers and water surface
- Even illumination across the field of view
- Camera captures clear, high-quality images
- Software can reliably track features

**Poor lighting conditions:**
- Glare washes out surface details
- Shadows obscure parts of the field of view
- Extreme contrast between bright and shadowed areas
- Camera adjusts exposure for bright areas, making shadowed areas too dark (or vice versa)
- Features that are physically present become invisible to the camera

**Critical insight:**
You can have excellent tracers on the water surface, but if lighting makes them invisible to the camera, they might as well not exist. Lighting assessment is equally important as tracer assessment.

---

## Optimal Lighting Conditions

### What Creates Ideal Conditions for Camera-Based Measurement

### Diffuse, Even Illumination

**Best case scenario: Overcast days**

Cloudy skies create diffuse lighting - sunlight scattered by clouds illuminates the scene evenly from all directions. This produces:
- No harsh shadows
- Minimal glare on water surface
- Even exposure across the entire field of view
- Excellent contrast between tracers and water surface
- Consistent conditions throughout the day

**Why this works:**
Water surface texture, foam, and debris all become more visible when illumination is even. There are no bright spots (sun glare) or dark spots (shadows) to confuse the camera's exposure settings.

**Practical implication:**
Sites that frequently have cloud cover (tropical regions during wet season, temperate maritime climates) benefit from naturally favorable lighting conditions.

**Real-world example from Sukabumi:**
Deployment occurred during Indonesia's late dry season, which typically has morning cloud cover breaking to afternoon sun. Morning measurements consistently showed better feature visibility than afternoon measurements. The team noted this pattern and recognized that wet season (more consistent cloud cover) would likely improve overall data quality.

[VISUAL PLACEHOLDER: Photo of river under overcast sky showing excellent feature visibility with even illumination]

### Low-Angle Sun (Dawn and Dusk)

**Second-best scenario: Early morning or late afternoon**

When the sun is low on the horizon (within 2 hours of sunrise or sunset), several beneficial effects occur:
- Sunlight strikes the water at a low angle, reducing direct reflection into a camera positioned above the river
- Longer shadows can actually enhance feature visibility by creating depth contrast
- Light intensity is moderate, not overwhelming camera sensors

**Why this works:**
Low-angle sun creates favorable geometry. Direct reflection (glare) bounces away from a camera looking downward, rather than into the lens.

**Limitations:**
- Only available for limited hours per day
- Requires matching measurement timing to favorable lighting (not suitable for continuous monitoring)
- Shadows can still be problematic if they cross the measurement area

**Practical implication:**
Useful for manual verification measurements - schedule field surveys for early morning or late afternoon when possible.

### Light Rain or Mist

**Surprisingly good conditions**

Light rain creates excellent measurement conditions:
- Clouds provide diffuse lighting
- Rain droplets on the water surface create texture and trackable features
- Surface is activated with micro-ripples and patterns
- No glare

**Why this works:**
Rain both improves lighting (cloud cover) and enhances tracers (surface texture). Light rain is often the optimal combination of favorable conditions.

**Limitation:**
Heavy rain can create problems - rain on the camera lens obscures the view, and extreme surface disturbance from heavy droplets can make tracking difficult.

**Practical consideration:**
Camera housings should protect the lens from rain. Ensure any selected site allows for proper lens protection while maintaining clear view of the water surface.

[VISUAL PLACEHOLDER: Photo showing water surface during light rain with enhanced texture visible]

---

## Problematic Lighting Conditions

### Situations That Degrade Measurement Quality

### Direct Sunlight and Glare

**The most common lighting problem**

When sunlight reflects directly off the water surface into the camera lens, glare overwhelms the image. This happens when:
- Sun angle positions the reflection directly toward the camera
- Water surface is relatively calm (acts like a mirror)
- Camera is positioned to view the reflection path

**Visual result:**
- Bright white or silver area on the water surface
- No visible features in the glare zone
- Camera exposes for the bright glare, making non-glare areas too dark
- Or camera exposes for normal areas, making glare zone completely blown out (pure white)

**When this occurs:**
- **Midday:** Sun high overhead, especially problematic when camera is also positioned high (bridge mounting)
- **Specific times of day:** When sun angle aligns with camera viewing angle (varies by season and camera orientation)
- **Calm water:** Glare is worst on smooth surfaces; some texture or ripples scatter light and reduce glare

**Glare zones:**
Glare is often localized - affecting one part of the field of view while other areas remain visible. If glare covers 20-30% of the measurement area, the remaining 70-80% may still provide useful data. If glare covers the entire field of view, measurement becomes impossible during that period.

[VISUAL PLACEHOLDER: Photo showing severe glare - bright white area on water surface where no features are visible, with annotation showing unusable zone]

### Assessment question:
Stand at the planned camera location at different times of day. Observe when sunlight reflection creates glare in the viewing area. Note the times and duration - is glare present for 2 hours around midday, or for 6+ hours making most of the day unusable?

### Deep Shadows from Vegetation or Structures

**Problem:**
Trees, bridges, buildings, or steep riverbanks can cast shadows across the measurement area. Shadows create two problems:

1. **Reduced visibility in shadowed areas:**
   - Features in shadow become dark and difficult to distinguish
   - Contrast is reduced
   - Camera may underexpose shadowed areas if exposing for bright areas

2. **Extreme contrast between shadowed and lit areas:**
   - Camera struggles to expose correctly for both zones
   - Either bright areas are washed out or shadow areas are too dark
   - Transition zones between light and shadow create tracking confusion

**When shadows are problematic:**
- Shadows covering >50% of measurement area
- Shadows creating sharp boundaries through the field of view
- Shadow patterns that move during measurement periods (changing sun angle) - creates temporal inconsistency

**When shadows are acceptable:**
- Entire measurement area consistently shaded (no extreme contrast)
- Small shadows (<20% of area) that are consistent
- Shadows from camera mounting structure if they fall outside the measurement area

**Real-world example:**
One Sukabumi candidate site was positioned beneath a highway overpass. The overpass provided excellent camera mounting and power access. However, assessment revealed the overpass shadow covered the entire measurement cross-section during midday (9 AM - 3 PM). While this provided consistent conditions (entirely shaded, no glare), it meant relying on shadow lighting all day. The team evaluated whether shadow lighting would provide sufficient tracer visibility - ultimately determining that consistent shadow was acceptable but not ideal, and weighted this against other site advantages.

[VISUAL PLACEHOLDER: Photo showing bridge shadow crossing river with sharp light/shadow boundary creating high contrast]

### Assessment question:
Visit the site at different times of day. Observe when shadows cross the measurement area. Are shadows consistent or moving? Do they create extreme contrast or relatively even shading?

### Backlit Conditions

**Problem:**
When the camera points toward the sun (or bright sky), the water surface becomes backlit - appearing dark against a bright background.

**Result:**
- Camera exposes for bright sky, making water surface too dark
- Surface features become silhouettes with little contrast
- Difficult to distinguish between different tracers

**When this occurs:**
- Camera oriented to view upstream or downstream in the direction of sun travel
- Morning sun if camera faces east, afternoon sun if camera faces west
- Worst at sunrise/sunset when sun is directly in frame

**Mitigation:**
Camera orientation should avoid pointing toward the sun during peak measurement hours. If possible, orient camera to view north-south rather than east-west to minimize backlighting issues.

[VISUAL PLACEHOLDER: Photo showing backlit water surface - dark water against bright sky background]

### Rapidly Changing Conditions

**Problem:**
Clouds passing in front of the sun create rapid transitions between bright and shaded conditions. Camera exposure settings may not adjust quickly enough, creating periods of poor image quality during transitions.

**When this is problematic:**
- Frequent isolated clouds (partly cloudy conditions)
- Fast-moving cloud systems
- If video clips are short (30-60 seconds), transitions may affect entire clips

**When this is acceptable:**
- Continuous cloud cover (consistent shading)
- Clear skies (consistent brightness, though glare may be issue)
- Slow-moving clouds where transitions are infrequent
- If camera exposure adjusts quickly (camera-specific capability)

**Practical consideration:**
This is usually a minor issue compared to glare or shadows. Most systems can tolerate some variability from clouds.

---

## Time of Day Considerations

### How Lighting Conditions Change Throughout the Day

Understanding daily lighting cycles helps predict when measurement quality will be best and worst.

### Typical Daily Pattern (Tropical and Subtropical Sites)

**Pre-dawn (5:00-6:00 AM):**
- Very low light
- May be too dark for good image quality
- Not recommended for optical measurement without artificial lighting

**Dawn (6:00-7:30 AM):**
- Increasing light, low sun angle
- Often excellent conditions - soft light, minimal glare
- Favorable period for measurements

**Mid-morning (7:30-10:00 AM):**
- Good to excellent light levels
- Sun angle still relatively low
- Generally favorable conditions
- Possible glare starting to develop depending on camera orientation

**Midday (10:00 AM - 2:00 PM):**
- Harsh, direct sunlight
- Highest glare potential
- Often the most challenging period
- May be problematic depending on specific site geometry

**Mid-afternoon (2:00-4:30 PM):**
- Similar to mid-morning
- Sun angle decreasing
- Glare reducing if it was present at midday
- Generally favorable conditions

**Late afternoon (4:30-6:00 PM):**
- Excellent conditions - soft light, low sun angle
- Similar to dawn period
- Favorable for measurements

**Dusk (6:00-7:00 PM):**
- Decreasing light
- May become too dark for good image quality toward the end of this period

**Night:**
- Too dark for optical measurement without artificial lighting
- Standard OpenRiverCam deployments do not operate at night

[VISUAL PLACEHOLDER: 24-hour timeline showing lighting quality rating (Excellent/Good/Fair/Poor) changing through the day with sun position diagram]

### Site-Specific Variations

**Actual timing depends on:**
- **Latitude:** Equatorial sites have consistent 12-hour days; high latitudes have huge seasonal variation
- **Season:** Summer vs. winter sun paths
- **Topography:** Mountains blocking early/late sun
- **Orientation:** Camera view direction affects when glare occurs

**Assessment approach:**
Visit the site at multiple times of day (morning, midday, afternoon). Observe how lighting changes. Identify the best and worst periods. Estimate what percentage of daylight hours provides acceptable lighting conditions.

**Decision criteria:**
- **Excellent site:** 10+ hours per day of good lighting
- **Acceptable site:** 6-10 hours per day of good lighting
- **Marginal site:** 3-6 hours per day of good lighting
- **Poor site:** <3 hours per day of good lighting

---

## Camera Orientation Relative to Sun

### Minimizing Glare Through Positioning

Camera orientation significantly affects glare and backlighting issues. When selecting camera mounting locations, consider viewing direction.

### North-South Viewing (Generally Preferred)

**Camera views north or south across the river:**
- Sun travels east-to-west (northern hemisphere) or appears to move along northern sky (southern hemisphere close to equator)
- Sun is never directly in front of or behind the camera
- Glare zones shift from side to side during the day rather than in/out of the field of view
- Minimal backlighting issues

**Advantages:**
- More consistent lighting throughout the day
- Glare is reduced compared to east-west viewing
- Suitable for most sites

**Real-world application:**
When possible, select camera mounting points (bridges, structures, banks) that allow north-south viewing across the river.

[VISUAL PLACEHOLDER: Overhead diagram showing river running east-west with camera on north bank looking south - sun path crosses perpendicular to view, minimizing glare]

### East-West Viewing (More Challenging)

**Camera views east or west along the river:**
- Sun travels along the same axis as camera view
- Morning: sun may be directly in frame if viewing east, or backlighting if viewing west
- Afternoon: sun may be directly in frame if viewing west, or backlighting if viewing east
- Glare and backlighting issues more pronounced

**Challenges:**
- Significant periods of poor lighting when sun aligns with viewing direction
- May be unusable during sunrise (viewing east) or sunset (viewing west)

**When this orientation is necessary:**
Sometimes river orientation and accessible mounting points leave no choice. If you must use east-west viewing:
- Prefer viewing direction that avoids sun during peak measurement hours (e.g., if afternoon data is most important, view east to avoid afternoon sun)
- Accept that certain times of day will have poor conditions
- Document limitations clearly

### Adjustable Mounting

**Ideal scenario (but rarely practical):**
Camera on adjustable mount that can rotate to track optimal viewing angle as sun moves. This is technically possible but adds complexity, cost, and maintenance requirements - generally not practical for humanitarian field deployments.

**Practical approach:**
Select fixed mounting position and orientation that provides acceptable lighting for the longest portion of each day.

---

## Seasonal Sun Angle Changes

### How Lighting Conditions Vary Through the Year

Sun position changes seasonally. Sites near the equator experience minimal variation; sites at higher latitudes experience dramatic seasonal changes in sun angle and day length.

### Equatorial Sites (±10° Latitude)

**Characteristics:**
- Sun nearly overhead year-round
- Day length consistently 12 hours ±30 minutes
- Sun angle varies only slightly seasonally
- Lighting conditions relatively consistent through the year

**Implication for site selection:**
Lighting conditions observed during site visit are generally representative of year-round conditions. Seasonal variation is minimal.

**Example:**
Sukabumi, Indonesia (approximately 7°S latitude) experiences minimal seasonal sun angle change. Midday sun is nearly overhead throughout the year. Lighting patterns observed during October site visit were reasonably representative of conditions in other months.

### Tropical Sites (10-23° Latitude)

**Characteristics:**
- Sun high in sky but noticeable seasonal variation
- Summer: sun more directly overhead
- Winter: sun lower in sky but still relatively high
- Day length varies by 1-3 hours seasonally
- Lighting conditions moderately variable through year

**Implication:**
Site visit during one season provides reasonable indication of conditions, but verify that seasonal sun angle changes do not create new glare or shadow problems.

### Mid-Latitude Sites (23-50° Latitude)

**Characteristics:**
- Significant seasonal sun angle variation
- Summer: sun high in sky, long days (14-16 hours)
- Winter: sun low in sky, short days (8-10 hours)
- Shadow patterns dramatically different between summer and winter
- Lighting conditions highly variable through year

**Implication:**
Site assessment must explicitly consider seasonal variations. A site with excellent lighting in summer might have severe shadow problems in winter (low sun creates long shadows from nearby trees/structures).

**Assessment requirement:**
If possible, visit site in both summer and winter. If not possible, use sun angle calculators to predict seasonal shadow patterns and glare zones.

### High-Latitude Sites (>50° Latitude)

**Characteristics:**
- Extreme seasonal variation
- Summer: sun barely sets, very long days
- Winter: sun barely rises, very short days
- Potential for 24-hour monitoring in summer (if artificial lighting used)
- Very limited daylight in winter (may be only 4-6 hours)

**Implication:**
These sites face fundamental challenges for optical monitoring. Winter monitoring may be impractical. Ice cover is also a likely issue (see environmental factors).

**Assessment approach:**
Focus deployment on summer months when lighting and ice conditions are favorable. Accept winter data gaps.

[VISUAL PLACEHOLDER: Diagram showing sun path across sky for equatorial site (high, consistent) vs. mid-latitude site (high in summer, low in winter) with resulting shadow patterns]

### Seasonal Assessment Tool

When evaluating a site, consider seasonal lighting using this framework:

**Questions:**
1. What latitude is the site? (Determines magnitude of seasonal variation)
2. Are there structures (bridges, buildings) or vegetation (trees) that cast shadows?
3. How will shadow lengths and positions change seasonally?
4. Will low winter sun create glare zones that do not exist during summer?
5. Are winter daylight hours sufficient for monitoring needs?

**Resources:**
- Sun angle calculators (available online, require site latitude/longitude and date)
- Site visit photographs from different seasons (if available from previous monitoring)
- Local knowledge about seasonal shadow patterns

---

## Shadow Assessment Framework

### Systematic Evaluation of Shadow Impacts

Shadows are often the most site-specific lighting challenge. Use this framework to assess shadow impacts.

### Step 1: Identify Shadow Sources

From the planned camera position, identify all potential shadow sources:

**Natural features:**
- [ ] Trees on river banks (note species - deciduous vs. evergreen)
- [ ] Steep banks or cliffs
- [ ] Overhanging vegetation

**Built structures:**
- [ ] Bridges or overpasses
- [ ] Buildings
- [ ] Towers, poles, or other vertical structures
- [ ] Camera mounting structure itself

**Document:**
Sketch or photograph the field of view with shadow sources labeled.

### Step 2: Observe Current Shadow Patterns

During site visit, observe when and where shadows fall:

**Timing:**
- [ ] What time do shadows enter the measurement area?
- [ ] How long do shadows persist?
- [ ] Do shadows cover the entire area or only portions?

**Movement:**
- [ ] Are shadows stationary or moving (sun angle changing)?
- [ ] How quickly do shadow patterns change?

**Coverage:**
- [ ] What percentage of the measurement area is shadowed?
- [ ] Are shadows consistent (entire area shaded) or creating high contrast (part shaded, part lit)?

**Document:**
Note times and extent of shadow coverage. Take photographs showing shadow patterns.

### Step 3: Predict Seasonal Variation

Consider how shadow patterns will change seasonally:

**Deciduous trees:**
- Summer: Full foliage creates dense shadows
- Winter: No leaves, shadows minimal or absent
- Spring/Fall: Partial shading

**Sun angle effects:**
- Low winter sun creates long shadows from small obstacles
- High summer sun creates short shadows or none from low obstacles
- Shadow direction rotates seasonally

**Assessment:**
Will seasonal changes improve or worsen shadow conditions? If current site visit shows problematic shadows but occurs during the worst season (e.g., summer when trees have full foliage), conditions may improve seasonally. If current visit shows good conditions but is during the best season, conditions may worsen.

[VISUAL PLACEHOLDER: Series of photos or diagrams showing same site at different times of day and different seasons, illustrating how shadow patterns change]

### Step 4: Evaluate Shadow Acceptability

Not all shadows are problematic. Assess whether observed shadows will significantly degrade measurement quality:

**Acceptable shadow conditions:**
- [ ] Entire measurement area consistently shaded (no high contrast)
- [ ] Shadows cover <20% of area and are in low-priority zones
- [ ] Shadows present only during early morning or late afternoon (outside peak measurement hours)
- [ ] Seasonal changes will reduce shadow problems during critical monitoring period

**Problematic shadow conditions:**
- [ ] Shadows create sharp light/dark boundaries through the center of the measurement area
- [ ] Shadows cover >50% of area during peak measurement hours
- [ ] Moving shadows create constantly changing conditions
- [ ] Critical monitoring season has worst shadow conditions

**Decision:**
Based on this assessment, rate the site:
- **No shadow issues:** Shadows absent or negligible
- **Minor shadow issues:** Shadows present but acceptable
- **Moderate shadow issues:** Shadows reduce quality but site may still be viable if other factors are excellent
- **Severe shadow issues:** Shadows make site unsuitable

---

## Mitigation Strategies for Lighting Challenges

### Optimizing Sites with Suboptimal Lighting

When lighting conditions are less than ideal but the site has other advantages, several strategies can improve measurement quality.

### Strategy 1: Camera Settings Optimization

**Approach:**
Adjust camera exposure, gain, and white balance settings to optimize for site-specific lighting conditions.

**What can be adjusted:**
- **Exposure time:** Longer exposure in low light, shorter in bright light
- **Gain/ISO:** Increase sensitivity in low light (but increases noise)
- **White balance:** Adjust color balance to improve contrast between water and tracers
- **Dynamic range settings:** High dynamic range (HDR) modes can help with high-contrast scenes

**Limitations:**
Camera settings can only partially compensate for poor lighting. Extreme glare or deep shadows may remain problematic even with optimal settings.

**Implementation:**
Conduct initial testing during installation, adjusting settings while observing image quality. Document final settings in system configuration.

**Real-world application:**
During Sukabumi deployment, initial camera settings produced washed-out images during midday. Exposure was reduced and contrast increased, improving feature visibility during bright periods without sacrificing image quality during overcast periods.

### Strategy 2: Camera Positioning to Avoid Glare Zones

**Approach:**
Fine-tune camera angle and position to minimize glare in the measurement area.

**Adjustments:**
- **Tilt angle:** Adjust camera tilt to change the reflection angle - even small changes (5-10 degrees) can move glare zones
- **Mounting height:** Higher mounting may reduce glare by changing viewing geometry
- **Lateral position:** Shift camera left/right along the mounting structure to change viewing angle relative to sun

**Limitations:**
Positioning must also satisfy flow measurement requirements (appropriate viewing angle for accurate velocity measurement, adequate coverage of cross-section). Lighting optimization cannot compromise measurement geometry.

**Implementation:**
During installation, test different positions and angles. Observe field of view at different times of day if possible. Select position that balances lighting and measurement requirements.

### Strategy 3: Temporal Filtering of Poor-Quality Data

**Approach:**
Accept that certain times of day will have poor lighting, and automatically filter out low-quality data during post-processing.

**How it works:**
- Camera operates continuously
- Some periods produce high-quality images (good lighting)
- Other periods produce low-quality images (glare, shadows)
- Software flags or discards measurements during poor-quality periods
- Continuous monitoring maintained, but with data gaps during unfavorable lighting

**Advantages:**
- Simple to implement (just flag low-quality periods)
- Maximizes useful data without manual intervention
- Works well if poor lighting is predictable (same times each day)

**Limitations:**
- Creates data gaps
- If poor lighting persists for extended periods (6+ hours daily), substantial data loss occurs
- Requires understanding which gaps are acceptable for monitoring objectives

**Implementation:**
Include data quality flags in processing workflow. Analyze patterns of poor-quality data to understand typical gaps.

### Strategy 4: Supplemental Lighting for Critical Applications

**Approach:**
Install artificial lighting to illuminate the measurement area during low-light periods (dawn, dusk, night).

**When this is justified:**
- 24-hour monitoring is critical (e.g., flood warning system must operate overnight)
- Site has excellent characteristics except for lighting
- Power is available for lighting (solar or grid)
- Cost and complexity are acceptable

**Lighting options:**
- LED floodlights on the mounting structure
- Infrared illumination with infrared-sensitive camera (invisible to human eye)
- Low-power LED strips for nighttime only

**Limitations:**
- Adds cost, complexity, maintenance requirements
- Power consumption (may require larger solar panels or grid connection)
- Potential light pollution concerns in natural areas
- Security concerns (lights may attract attention)

**Practical consideration:**
Supplemental lighting is rarely implemented in humanitarian OpenRiverCam deployments due to cost and complexity. More common in permanent infrastructure monitoring installations.

[VISUAL PLACEHOLDER: Diagram showing camera position adjustment to move glare zone out of measurement area]

---

## Lighting Assessment Checklist

### Site Evaluation Framework

Use this checklist when evaluating lighting conditions at a potential site:

### Daytime Lighting Assessment

**Optimal conditions present?**
- [ ] Frequent overcast conditions (diffuse lighting)
- [ ] Site experiences many hours of favorable lighting daily
- [ ] Camera orientation minimizes glare (north-south viewing preferred)

**Glare evaluation:**
- [ ] Observe water surface at multiple times - when does glare appear?
- [ ] What percentage of measurement area is affected by glare?
- [ ] How many hours per day is glare problematic?
- [ ] Can camera position be adjusted to reduce glare?

**Shadow evaluation:**
- [ ] Identify all shadow sources (vegetation, structures)
- [ ] Observe shadow patterns at different times
- [ ] Estimate seasonal shadow changes
- [ ] What percentage of area is shadowed during peak measurement hours?
- [ ] Are shadows consistent (acceptable) or creating high contrast (problematic)?

**Daily lighting cycle:**
- [ ] How many hours of good lighting occur per day?
- [ ] Are unfavorable periods predictable and consistent?
- [ ] Do favorable periods align with monitoring priorities?

**Seasonal lighting variation:**
- [ ] What latitude is the site (determines magnitude of seasonal variation)?
- [ ] Will seasonal sun angle changes create new glare or shadow problems?
- [ ] Are winter daylight hours adequate?

### Scoring Framework

**Glare severity:**
- No glare or glare <10% of area: 3 points
- Moderate glare affecting 10-30% of area for 2-4 hours/day: 2 points
- Significant glare affecting 30-50% of area for 4-6 hours/day: 1 point
- Severe glare affecting >50% of area or persistent throughout day: 0 points

**Shadow severity:**
- No problematic shadows: 3 points
- Minor shadows affecting <20% of area or only during low-priority hours: 2 points
- Moderate shadows affecting 20-50% of area during peak hours: 1 point
- Severe shadows creating high contrast or covering >50% of area: 0 points

**Favorable lighting duration:**
- >10 hours per day of good lighting: 3 points
- 6-10 hours per day of good lighting: 2 points
- 3-6 hours per day of good lighting: 1 point
- <3 hours per day of good lighting: 0 points

**Total Score Interpretation:**
- **7-9 points:** Excellent lighting conditions - proceed with confidence
- **5-6 points:** Acceptable lighting - minor limitations manageable
- **3-4 points:** Marginal lighting - consider mitigation strategies or alternative sites
- **0-2 points:** Poor lighting - strongly consider alternative site

---

## Real-World Example: Sukabumi Lighting Assessment

### Applying the Lighting Framework

During Sukabumi site selection, the team evaluated lighting conditions at the downstream-of-bridge site (selected for tracer availability, as described in Section 6.1).

### Lighting Assessment Details

**Site characteristics:**
- Latitude: ~7°S (near equator, minimal seasonal sun angle variation)
- Camera mounted on bridge railing, viewing downstream
- View direction: approximately north-northeast
- Site visit: late October (late dry season)
- Typical weather: morning cloud cover, afternoon clearing

**Glare evaluation:**
- **Morning (7-10 AM):** Overcast, no glare observed
- **Midday (10 AM-2 PM):** Sun breaks through clouds, moderate glare affecting approximately 30% of downstream field of view for 1-2 hours around solar noon
- **Afternoon (2-5 PM):** Glare reduced as sun angle decreases
- **Assessment:** Moderate glare present but limited to 2-3 hours daily, affecting less than half of measurement area

**Shadow evaluation:**
- Bridge structure casts shadow on river, but shadow is downstream of measurement cross-section
- Shadow from camera mounting bracket affects approximately 5% of field of view (acceptable)
- No vegetation shadows (urban environment)
- **Assessment:** Shadow impacts minimal

**Daily lighting cycle:**
- Good lighting: 7-10 AM (3 hours) - excellent overcast conditions
- Moderate lighting: 10 AM-2 PM (4 hours) - partial glare but 70% of area still usable
- Good lighting: 2-5 PM (3 hours) - reducing glare as sun lowers
- **Total favorable: ~10 hours per day**

**Seasonal considerations:**
- Equatorial location means minimal seasonal sun angle variation
- Wet season (Nov-Mar) expected to increase cloud cover, likely improving lighting overall
- **Assessment:** Conditions observed during site visit represent worst-case (dry season); wet season improvements likely

### Scoring

- Glare severity: 2 points (moderate glare, 30% of area, 2-3 hours)
- Shadow severity: 3 points (minimal shadows)
- Favorable lighting duration: 3 points (10 hours/day)
- **Total: 8/9 points - Excellent lighting conditions**

### Decision

Lighting was assessed as excellent and not a limiting factor for site selection. The moderate midday glare was noted as a known limitation but acceptable given:
1. Glare limited to 2-3 hours daily
2. 70% of measurement area remained usable even during glare periods
3. Wet season (critical monitoring period) expected to improve conditions with more cloud cover

The team documented midday glare as "expected lower quality period" but determined this did not compromise monitoring objectives.

[VISUAL PLACEHOLDER: Photos from Sukabumi showing morning conditions (overcast, excellent), midday conditions (partial glare), and afternoon conditions (good)]

---

## Integration with Overall Site Selection

### Lighting in Context of Other Criteria

Lighting assessment must be integrated with evaluations of tracers (Section 6.1), flow uniformity (Section 6.3), and accessibility (Section 6.4).

### Decision Matrix Approach

**Example scenario:**
You are comparing two potential sites:

**Site A:**
- Tracers: Excellent (8/9 points)
- Lighting: Marginal (4/9 points) - severe shadows during midday
- Flow uniformity: Excellent (assessment pending Section 6.3)

**Site B:**
- Tracers: Good (6/9 points)
- Lighting: Excellent (8/9 points)
- Flow uniformity: Excellent (assessment pending)

**Which to select?**
This depends on whether lighting limitations at Site A can be mitigated:
- If shadows reduce usable measurement hours to 4-6 hours/day, but monitoring objectives can be met with this limited data collection, Site A may still be preferred (better tracers)
- If lighting limitations are unacceptable, Site B may be preferred despite slightly inferior tracers

**Key principle:**
No single factor dominates. The best site balances all requirements. Excellent tracers cannot compensate for completely inadequate lighting, just as excellent lighting cannot compensate for no tracers.

### Minimum Acceptable Thresholds

For a site to be viable, it must meet minimum thresholds for ALL critical criteria:

**Minimum lighting requirement:**
At least 4-6 hours per day of acceptable lighting conditions (no severe glare covering >70% of area, no high-contrast shadows across entire measurement zone).

**If a site fails to meet this minimum:**
Either implement mitigation strategies (camera positioning, temporal filtering) or eliminate the site regardless of other advantages.

---

## Summary: Key Concepts for Lighting Assessment

**Why lighting matters:**
Camera-based measurement requires clear images showing distinct tracers. Poor lighting makes physically present tracers invisible to the camera.

**Optimal lighting conditions:**
- Overcast days (diffuse illumination)
- Low-angle sun (early morning, late afternoon)
- Light rain (diffuse light + enhanced surface texture)

**Problematic lighting conditions:**
- Direct glare (sun reflecting off water into camera)
- Deep shadows (creating extreme contrast)
- Backlit conditions (camera pointing toward sun)
- Rapidly changing conditions (passing clouds)

**Time of day patterns:**
- Dawn/dusk: Often excellent (low sun angle)
- Midday: Often challenging (direct sun, glare potential)
- Night: Too dark without artificial lighting
- Site-specific timing depends on location and camera orientation

**Camera orientation:**
- North-south viewing preferred (minimizes glare)
- East-west viewing more challenging (sun alignment issues)
- Select mounting position to optimize orientation

**Seasonal variations:**
- Equatorial sites: Minimal seasonal change
- Tropical sites: Moderate seasonal variation
- Mid-latitude sites: Significant seasonal sun angle changes
- High-latitude sites: Extreme seasonal variation in day length and sun angle

**Shadow assessment:**
- Identify shadow sources (vegetation, structures)
- Observe shadow patterns and timing
- Predict seasonal changes
- Evaluate whether shadows create acceptable consistent shading or problematic high-contrast zones

**Mitigation strategies:**
- Camera settings optimization
- Positioning to avoid glare zones
- Temporal filtering of poor-quality data
- Supplemental lighting (rarely used in humanitarian deployments)

**Assessment framework:**
Score sites on glare severity (0-3), shadow severity (0-3), and favorable lighting duration (0-3). Sites scoring 7-9 are excellent, 5-6 acceptable, 3-4 marginal, 0-2 unsuitable.

**Integration with other criteria:**
Lighting assessment is one of four critical site selection criteria. Sites must meet minimum thresholds for lighting AND tracers AND flow uniformity AND accessibility.

---

**Next Section:** [6.3 Uniform Flow Requirement](03-uniform-flow.md)

[VISUAL PLACEHOLDER: One-page visual summary showing:
- Optimal vs. problematic lighting (comparison photos)
- Daily lighting cycle timeline
- Shadow assessment checklist
- Camera orientation diagram
- Scoring framework
- "Good lighting makes tracers visible - poor lighting makes them invisible" key message]
