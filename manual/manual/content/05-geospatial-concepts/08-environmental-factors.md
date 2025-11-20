# 5.8 Physical and Environmental Factors

You have learned how RTK GPS achieves centimeter-level accuracy through precise satellite positioning and correction broadcasting. You understand fix status, coordinate systems, and post-processing workflows. But one critical question remains: **What environmental conditions enable or degrade this precision in the field?**

RTK GPS is powerful technology, but its performance depends heavily on the physical environment where you survey. The same equipment that achieves 1-2 cm accuracy in ideal conditions may struggle to obtain fix, or deliver degraded accuracy, in challenging environments.

This section addresses practical field considerations:
- What makes a good survey site vs. a problematic site
- How physical obstructions affect GPS signals
- Atmospheric and timing factors that impact accuracy
- Recognizing and avoiding conditions that degrade survey quality
- Practical mitigation strategies for challenging environments

**Why this matters for OpenRiverCam:**
- You often survey in natural environments with vegetation, terrain, and weather challenges
- River sites may have obstructed sky views (trees, canyon walls, bridges)
- Survey timing may be constrained by hydrology (water levels, flood events)
- Understanding environmental factors helps you maximize survey quality within real-world constraints

This is practical field knowledge that helps you recognize when conditions support high-accuracy surveying, and when you need to adjust approach or expectations.

---

## Sky Visibility and Satellite Geometry

GPS positioning requires clear "view" of satellites. Obstructions degrade signal quality and limit which satellites are usable.

### Line-of-Sight Requirements

**GPS signals are line-of-sight (like light):**
- Travel in straight lines from satellite to receiver antenna
- Cannot penetrate solid objects (buildings, rocks, tree canopy, earth)
- Can be reflected (multipath - discussed later)
- Weakened by vegetation (leaves attenuate signal)

**For RTK positioning, you need:**
- Clear view to minimum number of satellites (≥10, ideally ≥12)
- Satellites distributed across sky (not clustered in one area)
- Continuous tracking (gaps cause loss of fix, requiring re-initialization)

**Analogy:** Imagine you are trying to photograph stars at night. If you are in a narrow canyon with walls blocking most of the sky, you can only see a few stars directly overhead. From an open field with clear horizon, you see many stars in all directions. GPS works the same way - more visible sky = more satellites = better positioning.

### Obstructions That Block Satellites

**Common obstructions in field surveys:**

**1. Vegetation (trees, bushes):**
- **Light foliage (sparse branches, no leaves):** Minimal impact, may still achieve fix
- **Medium canopy (partial cover):** Reduced satellite count, slower fix acquisition, degraded accuracy
- **Dense canopy (full forest cover):** Severe signal blockage, RTK fix unlikely or impossible
- **Seasonal variation:** Deciduous trees less problematic in winter (no leaves) vs. summer (full foliage)

**2. Terrain (hills, cliffs, canyon walls):**
- Block satellites low on horizon
- Reduce satellite count and geometry quality
- Particularly problematic for narrow river canyons (steep walls on both sides)
- Example: River in deep gorge may only have clear sky directly overhead (poor geometry)

**3. Structures (buildings, bridges, towers):**
- Complete signal blockage in shadowed areas
- Often cause multipath (reflected signals) nearby
- Urban canyons (streets between tall buildings) are worst-case scenario
- Bridges over rivers: Good base station site away from bridge; challenging rover surveys underneath

**4. Vehicles and equipment:**
- Large metal objects reflect and block signals
- Base station: Keep >10m away from vehicles, containers, metal structures
- Rover: Surveyor's body can block signals if standing between antenna and satellites

**From SURVEY_PROCESS.md base station site selection criteria:**
- Open sky >15° elevation (meaning unobstructed from 15° above horizon upward)
- >10m from metal objects or vehicles
- Stable ground, accessible for monitoring

**These criteria ensure adequate satellite visibility for survey-in and RTK correction generation.**

### Elevation Mask and Sky Obstruction Angle

**Elevation angle:** Angle from horizontal ground to satellite, measured at receiver location
- 0° elevation: Satellite on horizon
- 45° elevation: Satellite halfway from horizon to directly overhead
- 90° elevation: Satellite directly overhead (zenith)

**GPS receivers use elevation mask to reject low-elevation satellites:**
- Typical elevation mask: 10-15°
- Satellites below mask are ignored (even if visible)
- Why: Low-elevation satellites have longer signal path through atmosphere (more error), more prone to multipath, weaker signals

**For RTK surveying, 15° elevation mask is standard:**
- Rejects satellites below 15° (near horizon)
- Focuses on higher-elevation satellites with better geometry and signal quality
- Trade-off: Fewer satellites available, but higher quality measurements

**Sky obstruction angle:** Angle above horizontal where obstructions block sky view
- Example: Trees surrounding site create obstruction up to 30° elevation
- Effective elevation mask = 30° (can only use satellites >30° elevation)
- **Higher obstruction angle = fewer usable satellites = worse conditions for RTK**

**Rule of thumb:**
- **Open sky >15°:** Excellent conditions (10-20+ satellites visible)
- **Obstruction to 20-25°:** Acceptable (8-12 satellites, may achieve fix)
- **Obstruction to 30-35°:** Marginal (6-10 satellites, fix uncertain, degraded accuracy)
- **Obstruction >40°:** Poor (RTK fix unlikely, consider relocating base or waiting)

**How to estimate obstruction angle in the field:**
- Stand at proposed base station or rover survey point
- Look at horizon in all directions
- Identify highest obstructions (tree tops, building peaks, terrain)
- Estimate angle from horizontal to top of obstruction
  - 15°: Obstruction about 1/6 of way from horizon to overhead
  - 30°: Obstruction about 1/3 of way
  - 45°: Obstruction halfway to overhead
- If average obstruction >25-30°, consider different location

**Practical tip:** Use smartphone clinometer app to measure obstruction angles objectively, or use "fist method": At arm's length, closed fist spans ~10° (varies with hand size, approximate).

### Satellite Geometry (DOP - Dilution of Precision)

Even with adequate satellite count, **how satellites are distributed across the sky** affects accuracy.

**DOP (Dilution of Precision):** Numerical measure of satellite geometry quality
- Lower DOP = better geometry = better accuracy
- Higher DOP = poor geometry = worse accuracy

**Types of DOP:**
- **PDOP (Position DOP):** Overall 3D position geometry
- **HDOP (Horizontal DOP):** 2D horizontal geometry
- **VDOP (Vertical DOP):** Vertical geometry
- PDOP ≈ √(HDOP² + VDOP²)

**PDOP values and interpretation:**
- **PDOP <1.5:** Excellent geometry (satellites well-distributed)
- **PDOP 1.5-2.5:** Good geometry (typical for RTK surveys)
- **PDOP 2.5-4.0:** Fair geometry (acceptable for lower-precision work)
- **PDOP 4.0-6.0:** Marginal (degraded accuracy, avoid if possible)
- **PDOP >6.0:** Poor (unreliable positioning, relocate or wait)

**From SURVEY_PROCESS.md quality gates:**
- Standard surveys: PDOP ≤2.5
- Challenging environments (canals with obstructions): PDOP ≤3.0
- Base station survey-in: PDOP ≤1.5

**What causes good vs. poor geometry:**

**Good geometry (low PDOP):**
- Satellites spread across sky in all directions
- Mix of low-elevation (horizon) and high-elevation (overhead) satellites
- No large gaps in satellite distribution

**Poor geometry (high PDOP):**
- Satellites clustered in one area of sky (e.g., all to the south)
- Only high-elevation satellites visible (obstructions block low-elevation)
- Large gaps in coverage (e.g., blocked by canyon walls to east and west)

**Example scenario:**
- **Open field:** 15 satellites visible: 4 to north, 4 to south, 3 to east, 3 to west, 1 overhead. PDOP = 1.3 (excellent)
- **Narrow canyon:** 8 satellites visible: All between north and south, directly overhead. East and west blocked by walls. PDOP = 4.2 (poor)

**Same satellite count, very different geometry quality.**

**Why vertical accuracy is worse than horizontal:**
- All satellites are above the horizon (none below)
- Vertical geometry is inherently weaker (limited angle variation)
- Typical: VDOP 1.5-2× higher than HDOP
- Result: Vertical accuracy ~1.5-2× worse than horizontal (3-4 cm vertical vs. 1-2 cm horizontal)

**You cannot control satellite positions** (they orbit continuously), but you can:
- Choose survey sites with clear sky view in all directions
- Avoid narrow canyons or heavily obstructed sites
- Monitor PDOP during survey - if PDOP suddenly increases, check for obstructions or wait for satellite geometry to improve
- Schedule surveys when GPS constellation geometry is favorable (satellite prediction tools available online)

---

## Multipath Interference

Multipath occurs when GPS signals reach the antenna via multiple paths: direct signal + reflections from surfaces. This degrades positioning accuracy.

### How Multipath Works

**Direct signal path:**
- Satellite → Receiver antenna (straight line)
- This is what GPS positioning relies on

**Reflected signal path (multipath):**
- Satellite → Reflective surface (ground, water, building) → Receiver antenna
- Longer path length (delayed arrival time)
- Receiver confuses reflected signal with direct signal
- Position calculation uses wrong signal travel time
- **Result: Position error (typically 5-50 cm, can be larger)**

**Analogy:** Imagine you are determining distance to a sound source by measuring how long sound takes to reach you. If you hear both direct sound and echo (reflected off a wall), you might measure time to echo instead of direct sound, calculating wrong distance.

### Common Multipath Sources

**Reflective surfaces that cause multipath:**

**1. Metal structures:**
- Vehicles, shipping containers, metal roofs, fences
- Highly reflective to GPS signals
- **Base station: Keep >10m from metal objects**
- **Rover: Avoid surveying near metal structures**

**2. Buildings and walls:**
- Concrete, glass, and metal buildings reflect signals
- Urban environments are multipath-intensive
- Position accuracy degrades near buildings (may be decimeter-level instead of centimeter)

**3. Water surfaces:**
- Calm water is highly reflective
- River surface can cause multipath for rover surveys near water level
- **From SURVEY_PROCESS.md: Base station for canal surveys should be >20m from water** (high ground, away from water surface)
- Rover pole height (antenna 1.5-2m above ground) helps reduce multipath from water

**4. Wet ground:**
- Rain-saturated ground is more reflective than dry ground
- Slight increase in multipath after heavy rain
- Impact typically small (few cm)

**5. Rock faces and cliffs:**
- Large vertical rock surfaces reflect signals
- Problematic in canyon or gorge environments

### Multipath Signatures and Detection

**How to recognize multipath in the field:**

**1. Unstable fix status:**
- RTK fix acquired, then lost, then reacquired repeatedly
- Fix "flickers" between FIX and FLOAT
- Suggests signal interference (multipath is one possible cause)

**2. Poor precision despite good satellite count:**
- SW Maps shows ≥12 satellites, PDOP <2.5, but precision is 5-10 cm (should be 1-3 cm)
- Multipath degrades accuracy even with good satellite geometry

**3. Position "jumping":**
- Rover antenna held still, but reported position shifts by 10-30 cm
- Reflects changing multipath as satellites move and reflections change

**4. Degraded position when near reflective surfaces:**
- RTK FIX with 2 cm precision in open area
- Move near metal building: Precision degrades to 8 cm
- Move back to open area: Precision improves to 2 cm again
- **Clear indication of multipath from building**

**GNSS receivers have anti-multipath features:**
- Choke ring antennas (suppress low-angle signals prone to ground reflection)
- Signal processing (reject signals with unusual characteristics)
- Carrier phase multipath mitigation algorithms
- These reduce but do not eliminate multipath

**Modern low-cost RTK receivers (ArduSimple F9P, etc.) have good multipath rejection, but:**
- Cannot eliminate multipath entirely
- Performance degrades in multipath-intensive environments
- Best solution: **Choose survey sites to minimize multipath sources**

### Avoiding and Mitigating Multipath

**Site selection strategies:**

**For base station:**
- Open ground away from buildings, vehicles, metal structures (>10m separation)
- Avoid setup near water bodies (>20m from canal, river when feasible)
- Natural vegetation (grass, small bushes) is less reflective than hard surfaces - acceptable
- Avoid asphalt, concrete pads near metal structures - prefer dirt or grass in open area

**For rover survey points:**
- Survey Ground Control Points and cross-section points in open areas when possible
- If surveying near water unavoidable (e.g., water level survey at river edge):
  - Use longer survey pole (antenna 1.5-2m above ground reduces ground/water multipath)
  - Verify precision ≤4 cm before saving point (relaxed threshold acknowledges multipath challenge)
  - Take multiple measurements, average if precision marginal
- Avoid positioning antenna near vertical metal or concrete surfaces

**Equipment techniques:**

**1. Antenna height:**
- Raising antenna above ground reduces ground-reflected multipath
- Base station: Tripod at 1.5-2m height (standard)
- Rover: Survey pole at 1.5-2m (measured accurately for height correction)

**2. Antenna type:**
- Multi-band antennas (L1/L2 or L1/L5) are more resistant to multipath than single-band
- Survey-grade antennas with ground plane or choke ring reduce multipath
- ArduSimple antennas (standard for OpenRiverCam) have basic multipath rejection - adequate for most conditions

**3. Observation time:**
- Longer observation time at each point averages out multipath variations (as satellites move, reflections change)
- From SURVEY_PROCESS.md: RTK FIX ≥10 seconds before saving point
- In multipath-prone areas: Consider 20-30 second observation per point

**Timing strategies:**

**Multipath varies with satellite positions:**
- As satellites orbit, reflection angles change
- Multipath severity changes throughout day
- If experiencing poor precision at site, wait 30-60 minutes and retry (satellite geometry will have changed, possibly reducing multipath)

**Post-processing mitigation:**

**If multipath suspected in collected data:**
- Collect check points (revisit same point multiple times during survey)
- Compare check point positions - differences indicate position uncertainty (may include multipath)
- If check point drift >5 cm, multipath (or other errors) may be present
- Consider repeating survey in better conditions or using different survey approach

**Multipath is less severe for RTK than for standalone GPS:**
- RTK corrections partially cancel multipath (base and rover experience similar multipath from same satellites)
- This assumes base and rover have similar environments - works well for open-site surveys
- Breaks down if rover in multipath-intensive environment while base is not

---

## Atmospheric Conditions and Signal Quality

GPS signals travel through Earth's atmosphere, where they are delayed and distorted. RTK partially corrects for atmospheric effects, but some residual errors remain.

### Ionospheric Effects

**Ionosphere:** Upper atmosphere layer (60-1000 km altitude), contains charged particles (ions, electrons)
- GPS signals passing through ionosphere are delayed
- Delay varies with electron density (Total Electron Content - TEC)
- TEC varies with time of day, season, geographic location, solar activity

**Ionospheric delay characteristics:**

**Time of day variation:**
- **Daytime (10:00-16:00):** Maximum ionization (sun overhead), maximum delay, highest variability
- **Nighttime (22:00-04:00):** Minimum ionization, minimum delay, more stable
- **Sunrise/sunset:** Rapidly changing ionization (transition periods)

**Solar activity variation:**
- **Solar maximum (11-year cycle peak):** High ionization, severe delays, frequent disturbances
- **Solar minimum:** Low ionization, minimal delays, stable conditions
- **Solar storms (geomagnetic events):** Sudden extreme ionization, can disrupt GPS for hours to days

**Geographic variation:**
- **Equatorial region (±20° latitude):** High ionization, large delays, variable
- **Mid-latitudes:** Moderate ionization
- **Polar regions:** Low ionization, but subject to auroral disturbances

**Indonesia location (6°S):** Near-equatorial region, experiences moderate to high ionospheric activity.

**How RTK handles ionosphere:**
- **Multi-frequency receivers (L1+L2 or L1+L5):** Measure ionospheric delay directly, can largely remove it
- **Single-frequency receivers:** Cannot measure ionospheric delay, rely on corrections
- **RTK correction:** Base and rover measure signals through similar atmosphere - ionospheric errors largely cancel (for baselines <10 km)
- **Residual ionospheric error:** Typically <1-2 cm for RTK (minimal impact for OpenRiverCam surveys)

**When ionosphere causes problems:**

**1. Geomagnetic storms:**
- Solar flares or coronal mass ejections cause extreme ionization
- GPS accuracy degrades globally for duration of storm (hours to days)
- RTK may lose FIX or show degraded precision
- **Solution:** Postpone survey until storm subsides (monitor space weather forecasts)

**2. Rapid ionospheric changes:**
- Sunrise/sunset transitions, localized disturbances
- Position solution may be temporarily unstable
- **Solution:** Wait for conditions to stabilize, or survey during more stable periods (midday or nighttime)

**Practical impact for OpenRiverCam:**
- **Normal conditions:** Ionosphere negligible concern for RTK (correction handles it)
- **Geomagnetic storm:** May need to postpone survey (RTK FIX difficult to obtain)
- **Survey timing:** Prefer morning (after sunrise stabilization) or afternoon (before sunset) over sunrise/sunset periods

**Monitoring space weather:**
- NOAA Space Weather Prediction Center: https://www.swpc.noaa.gov/
- Geomagnetic storm warnings (Kp index >5 indicates storm)
- If major storm forecasted, reschedule survey for subsequent days

### Tropospheric Effects

**Troposphere:** Lower atmosphere (surface to ~12 km altitude), contains water vapor and weather
- GPS signals refracted (bent) passing through troposphere
- Delay varies with temperature, pressure, humidity (especially water vapor)

**Tropospheric delay characteristics:**

**Weather dependence:**
- **High humidity:** Larger delay (water vapor refracts GPS signals)
- **Low humidity:** Smaller delay
- **High pressure:** Larger delay
- **Low pressure (storms):** Smaller delay but highly variable

**Spatial variation:**
- Tropospheric conditions vary horizontally (different weather at base vs. rover)
- For RTK baselines <10 km, conditions usually similar enough for effective correction
- For baselines >20 km, tropospheric gradients can introduce errors

**Temporal variation:**
- Changing weather (passing storms, temperature shifts) alters tropospheric delay
- Rapidly changing conditions = less stable positioning

**How RTK handles troposphere:**
- Base and rover experience similar tropospheric delay (short baseline)
- RTK corrections partially cancel tropospheric errors
- Residual tropospheric error: Typically 1-3 cm for RTK (vertical component larger than horizontal)

**Weather conditions that degrade RTK accuracy:**

**1. Heavy rain:**
- Rain droplets scatter and attenuate GPS signals
- Reduces signal strength (lower Signal-to-Noise Ratio - SNR)
- May lose tracking of some satellites
- Tropospheric refraction highly variable during rain
- **Impact:** Slower fix acquisition, potentially degraded accuracy (3-5 cm instead of 1-2 cm), possible loss of FIX during heavy downpours

**2. Thunderstorms:**
- Extreme tropospheric variability
- Electrical noise may interfere with signals
- Rapidly changing atmospheric conditions
- **Impact:** Unstable RTK solution, FIX may be lost during storm passage

**3. Fog and mist:**
- Water droplets in air increase refraction
- Mild signal attenuation
- **Impact:** Minimal (1-2 cm potential accuracy degradation)

**4. Temperature inversions:**
- Unusual atmospheric layering (temperature increases with altitude instead of decreasing)
- Can cause refraction anomalies
- **Impact:** Rare, usually minimal effect on RTK

**Practical guidance for weather:**

**Avoid surveying during:**
- Heavy rain (signal attenuation, poor precision)
- Active thunderstorms (unstable solution, safety concern from lightning)
- High wind (equipment stability issues, antenna movement degrades measurements)

**Acceptable conditions:**
- Light rain or drizzle (slight accuracy degradation, but RTK FIX usually maintained)
- Overcast (no direct impact - GPS signals penetrate clouds)
- Fog/mist (minimal impact)

**Optimal conditions:**
- Clear skies or high clouds
- Stable weather (no passing fronts or storms)
- Moderate humidity (low humidity better, but not critical)

**From SURVEY_PROCESS.md:** Survey session typically 6-12 hours. If weather deteriorates during session (rain starts), continue logging but pause rover surveys until conditions improve. Base station can continue survey-in and correction broadcast through light rain.

---

## Time of Day and Seasonal Considerations

Survey quality varies with time of day and season due to satellite geometry and atmospheric conditions.

### Daily Timing Factors

**Best times of day for RTK surveys:**

**Morning (08:00-11:00):**
- Ionosphere stabilized after sunrise transition
- Cooler temperatures (comfortable fieldwork)
- Good satellite availability
- **Recommended survey time**

**Midday (11:00-15:00):**
- Maximum ionospheric activity (not critical for RTK)
- Good satellite geometry (satellites well-distributed)
- Hot conditions (fieldwork challenging in tropical climates)
- Acceptable for RTK surveys, but less comfortable

**Afternoon (15:00-18:00):**
- Declining ionospheric activity
- Cooler than midday
- Good satellite availability
- **Recommended survey time**

**Avoid or use with caution:**

**Sunrise/sunset (±1 hour):**
- Rapid ionospheric changes (transition from night to day, or vice versa)
- Position solution may be less stable
- Not critical to avoid, but less optimal

**Night (20:00-06:00):**
- Minimal ionospheric activity (actually optimal for GPS)
- Poor visibility for fieldwork (safety concern, difficulty identifying survey points)
- **Impractical for most surveys** (even though GPS conditions good)

**Practical recommendation:** Schedule survey start for 08:00-09:00, survey through midday, finish by 16:00-17:00. This provides 7-9 hours for survey work in stable conditions.

### Seasonal Considerations

**Dry vs. wet season:**

**Dry season advantages:**
- Lower humidity (less tropospheric delay)
- Predictable weather (less risk of rain interrupting survey)
- Lower river levels (easier access to cross-section points)
- **Preferred for surveys when possible**

**Wet season challenges:**
- High humidity (increased tropospheric delay, but RTK handles this)
- Frequent rain (may interrupt surveys, degrade signal quality)
- High river levels (may limit access to survey points, safety concern)
- Muddy conditions (equipment handling more difficult)

**For OpenRiverCam, survey timing often driven by hydrologic needs:**
- Discharge measurements needed during specific flow conditions
- May require wet-season surveys despite challenges
- **Adaptation:** Plan for weather interruptions, bring rain protection for equipment, allow extra time

**Vegetation seasonal changes:**

**Deciduous trees (if present):**
- Winter/dry season: No leaves, less signal obstruction
- Summer/wet season: Full foliage, more obstruction
- **Impact:** Can be 3-5 satellites difference between leaf-on and leaf-off conditions

**Tropical evergreen:**
- Less seasonal variation in canopy
- Consistently challenging if under dense forest

**Agricultural areas:**
- Crop height varies seasonally
- Open fields (post-harvest) vs. tall crops (mid-season)
- May affect base station site selection

### Satellite Constellation Timing

**GPS constellation repeats geometry every ~23 hours 56 minutes (sidereal day).**

**What this means:**
- Satellite positions at 09:00 today are nearly same as 09:00 tomorrow
- If PDOP is excellent at 10:00 on Monday, it will be excellent at 10:00 on Tuesday
- If satellite geometry poor at site at 14:00, it may be better at 10:00 or 16:00

**Multi-GNSS improves timing flexibility:**
- GPS alone: 24-32 satellites in constellation, ~6-12 visible at any time
- GPS + GLONASS + Galileo: 70+ satellites total, 15-25 visible at any time
- **More satellites = less sensitivity to specific time of day**

**From SURVEY_PROCESS.md:** Modern receivers use GPS + GLONASS + Galileo. Minimum 12 satellites required for standard surveys, typically 15-20 satellites visible in open conditions. **Time-of-day satellite geometry is rarely limiting factor with multi-GNSS.**

**If experiencing poor satellite geometry (PDOP >3.0):**
- Check for obstructions (more likely cause than satellite geometry)
- If obstructions ruled out, wait 1-2 hours and retry (satellite positions will change)
- Use online satellite prediction tools to identify optimal time windows (rarely needed with multi-GNSS)

---

## Recognizing Good vs. Bad Survey Conditions

Practical field guidance for assessing site suitability and real-time conditions.

### Pre-Survey Site Assessment

**Before committing to base station setup, evaluate site:**

**Sky visibility check:**
- Walk to proposed base station location
- Look up and around in all directions
- Identify obstructions: trees, buildings, terrain, structures
- Estimate average obstruction angle
  - <20°: Excellent
  - 20-30°: Good to acceptable
  - 30-40°: Marginal
  - >40°: Poor - consider alternate location

**Multipath source check:**
- Identify reflective surfaces within 20m: metal structures, buildings, water, vehicles
- Plan base station >10m from metal objects
- For canal surveys: >20m from water on elevated ground

**Access and stability check:**
- Ground stable? (not soft mud that will shift under tripod)
- Safe access for monitoring base station during survey?
- Protected from disturbance? (animals, people, vehicles)

**From SURVEY_PROCESS.md base station site criteria:**
- [ ] Open sky >15°
- [ ] >10m from metal/vehicles
- [ ] Stable ground
- [ ] Accessible for monitoring
- [ ] For canals: High ground >20m from water

**If site fails criteria:**
- Scout alternate locations (even 20-50m relocation can improve conditions significantly)
- Accept degraded conditions only if no alternative (adjust quality thresholds accordingly)

### Real-Time Quality Monitoring During Survey

**Monitor these indicators during survey work:**

**1. Satellite count:**
- Check GNSS Master or SW Maps satellite display
- **≥12 satellites:** Excellent
- **10-11 satellites:** Acceptable
- **<10 satellites:** Marginal - verify fix quality carefully

**2. PDOP:**
- Display in GNSS Master or base station interface
- **<2.0:** Excellent geometry
- **2.0-2.5:** Good (standard threshold)
- **2.5-3.0:** Acceptable for challenging conditions
- **>3.0:** Poor - assess whether to continue or relocate

**3. Fix status:**
- RTK FIX: Centimeter-level accuracy achieved
- RTK FLOAT: Decimeter-level accuracy (ambiguities not resolved)
- DGPS/SBAS: Meter-level accuracy (not acceptable for OpenRiverCam)
- **Only collect survey points during RTK FIX status**

**4. Precision estimates:**
- SW Maps displays horizontal and vertical precision
- **Standard survey thresholds:**
  - Horizontal ≤2 cm, Vertical ≤3 cm
- **Challenging conditions (canals):**
  - Horizontal ≤4 cm, Vertical ≤6 cm
- If precision exceeds thresholds, investigate cause (obstructions, multipath, poor satellite geometry)

**5. Fix stability:**
- FIX should remain stable (not flicker to FLOAT and back)
- Hold rover antenna still for 10+ seconds - position should not jump >1-2 cm
- If unstable, indicates signal quality issues (multipath, obstructions, atmospheric disturbance)

**From SURVEY_PROCESS.md quality gates (all required before saving point):**
- [ ] RTK FIX maintained ≥10 seconds
- [ ] PDOP ≤2.5 (standard) or ≤3.0 (canals)
- [ ] Satellites ≥12 (standard) or ≥10 (canals)
- [ ] Precision ≤2cm H / 3cm V (standard) or ≤4cm H / 6cm V (canals)

**If quality gates not met:**
- Wait for conditions to improve (satellite geometry changes, atmospheric settling)
- Move rover to location with better sky view (even 2-3m can help)
- Check base station status (ensure base has not lost fix or power)
- If persistent, consider pausing survey and reassessing site or timing

### Signs of Degraded Conditions

**Recognize these warning signs in the field:**

**Equipment indicators:**
- RTK FIX difficult to acquire (taking >5 minutes when should be <2 minutes)
- FIX unstable (lost and reacquired repeatedly)
- Precision values higher than expected (4-6 cm when normally 1-2 cm)
- Satellite count dropping below normal (8-10 when normally 15-20)

**Environmental observations:**
- Weather deteriorating (rain starting, storm approaching)
- Heavy clouds moving in (may precede rain)
- Wind increasing (antenna stability compromised)
- Vegetation moved by workers/animals (new obstructions created)

**Position quality signs:**
- Check points showing drift >3-4 cm (revisiting same point gives different coordinates)
- Cross-section profiles appear noisy or irregular (individual points offset from smooth profile)
- Ground control points for camera calibration show poor transformation residuals (may indicate coordinate errors)

**Appropriate responses:**

**Temporary conditions (weather, satellite geometry):**
- Pause rover surveys
- Keep base station running (continue logging, maintain survey-in position)
- Wait for improvement (30-60 minutes)
- Resume when quality gates met

**Persistent site issues (obstructions, multipath):**
- Relocate base station to better location (requires new survey-in, reset base position)
- Adjust survey plan (avoid problematic areas, survey different points)
- Accept degraded accuracy (document conditions, adjust quality thresholds)
- Consider alternate survey technology (total station if GPS unsuitable)

**Safety concerns (lightning, flooding):**
- Terminate survey immediately
- Protect equipment
- Personnel safety is paramount - equipment can be replaced

---

## Mitigation Strategies for Challenging Environments

When ideal conditions are not available, these strategies help maximize survey quality.

### Vegetation and Canopy Challenges

**Problem:** Dense vegetation blocks satellite signals, reduces satellite count, prevents fix.

**Mitigation approaches:**

**1. Base station placement:**
- Locate base in clearing or open area (even if 50-100m from survey area)
- RTK works with baselines up to 10 km - base does not need to be immediately adjacent to survey points
- Clear base station sky view is higher priority than proximity to survey area

**2. Survey timing:**
- Deciduous areas: Survey in leaf-off season (winter/dry season)
- Morning: Dew on leaves makes foliage more reflective (worse signal penetration) - afternoon may be better
- Not applicable to evergreen tropical canopy

**3. Selective clearing:**
- With landowner permission, trim branches directly above base station location
- Focus on creating clear cone from 15° above horizon upward
- Minimal clearing can significantly improve satellite visibility
- **Do not clear protected vegetation or without authorization**

**4. Rover technique:**
- Extend survey pole vertically above rover surveyor
- Raising antenna 30-50 cm above operator's head improves sky view
- Survey from small gaps in canopy when possible (openings between trees)

**5. Accept longer fix acquisition:**
- Under canopy, RTK FIX may take 5-10 minutes instead of 1-2 minutes
- Allow extra time per survey point
- Once fix acquired, verify quality (precision, stability) carefully before saving point

**6. Alternative survey technology:**
- If vegetation too dense for GPS, consider total station surveying from open area
- Or use GPS in open area to establish control, traverse through vegetation with total station

### Terrain and Canyon Challenges

**Problem:** Steep terrain, narrow canyons, or gorges block low-elevation satellites, degrade geometry.

**Mitigation approaches:**

**1. Base station on high ground:**
- Place base at highest accessible point with clear sky view
- Example: For river in canyon, place base on rim rather than canyon floor
- Baseline length (hundreds of meters vertical) less important than sky visibility

**2. Survey during optimal satellite passes:**
- Use satellite prediction tools to identify when satellites overhead (reducing dependence on low-elevation satellites)
- This is advanced technique, rarely necessary

**3. Extended observation time:**
- In marginal geometry, observe each point for 20-30 seconds instead of 10 seconds
- Longer observation averages out geometry-related uncertainties

**4. Lower precision expectations:**
- Canyon surveys may achieve 4-6 cm accuracy instead of 1-2 cm
- Still adequate for most OpenRiverCam applications
- Document conditions and accuracy estimates

**5. Hybrid survey approach:**
- GPS for accessible points with clear sky
- Total station for obstructed areas, tied to GPS control points

### Urban and Structure Challenges

**Problem:** Buildings and metal structures cause multipath and signal blockage.

**Mitigation approaches:**

**1. Base station in park or open space:**
- Even in urban area, parks, athletic fields, or plazas may have clear sky
- Base can be 1-2 km from rover survey area (within RTK range)

**2. Avoid surveying near buildings:**
- Survey points should be >20m from large buildings when possible
- Reduces multipath from reflections

**3. Recognize degraded accuracy:**
- Urban RTK may achieve 5-10 cm instead of 1-2 cm
- Accept this if no alternative
- Use check points to verify accuracy

**4. Post-processing options:**
- For critical urban surveys, consider PPK (Post-Processed Kinematic) instead of real-time RTK
- Allows more sophisticated multipath mitigation in processing software
- Requires logging rover raw data (additional complexity)

### Weather Adaptation

**Problem:** Rain, storms, or high humidity degrade signal quality.

**Mitigation approaches:**

**1. Equipment protection:**
- Use waterproof covers or bags for receivers
- Antenna is weatherproof, but connections should be protected
- Tablet/smartphone in waterproof case or bag

**2. Survey scheduling:**
- Monitor weather forecasts
- Plan surveys for stable weather windows
- Postpone if major storms forecasted

**3. Pause-and-resume:**
- If rain starts during survey, pause rover work
- Keep base station running (maintain survey-in reference)
- Resume when rain stops or lightens

**4. Light rain tolerance:**
- RTK generally works in light rain (drizzle)
- Monitor precision - if still meeting quality gates, can continue
- Heavy rain (downpour): Pause survey, risk of losing FIX

**5. Post-rain resumption:**
- After rain stops, wet foliage may be more reflective (temporary signal degradation)
- Wait 30-60 minutes for canopy to dry if possible
- Ground saturation increases multipath slightly (minor effect)

### Quality Assurance in Challenging Conditions

**When working in less-than-ideal environments, strengthen QA:**

**1. More frequent check points:**
- Standard: 1-2 check points per survey session
- Challenging conditions: 3-5 check points
- Revisit check points throughout day to verify position repeatability

**2. Redundant measurements:**
- Measure critical points (GCPs, water level markers) multiple times
- Average positions if repeatability good
- Flag for review if repeatability poor (>5 cm variation)

**3. Tighter quality gate monitoring:**
- In marginal conditions, enforce quality gates strictly
- Do not relax thresholds "just this once" - maintains data integrity

**4. Documentation:**
- Photograph survey site conditions (sky view, obstructions, environment)
- Record environmental conditions in field notes (weather, vegetation, structures)
- Document any quality concerns or deviations from standard procedure
- Enables interpretation of results, justifies accuracy estimates

**5. Conservative accuracy claims:**
- If surveying in challenging conditions, report conservative accuracy estimates
- Example: "Survey achieved 3-5 cm horizontal accuracy under partial canopy" instead of claiming 1-2 cm
- Honesty about uncertainty builds trust and prevents misuse of data

---

## Connection to Survey Procedures

Understanding environmental factors enables you to apply SURVEY_PROCESS.md effectively:

**Base station site selection (Section 3):**
- Now you understand WHY open sky >15°, >10m from metal, stable ground are required
- You can assess site quality and make informed relocation decisions
- You know when conditions are marginal and extra care is needed

**Quality gates (All survey sections):**
- Quality thresholds (PDOP ≤2.5, Satellites ≥12, Precision ≤2cm H / 3cm V) are based on environmental factors
- You understand what causes quality gate failures (obstructions, multipath, weather)
- You can troubleshoot problems instead of just abandoning survey

**Challenging environments (canals):**
- Relaxed thresholds (PDOP ≤3.0, Satellites ≥10, Precision ≤4cm H / 6cm V) account for environmental constraints
- You recognize these are adaptations to vegetation/water multipath, not arbitrary choices

**Check point drift criteria (Section 4):**
- ≤3cm H, ≤4cm V drift threshold detects environmental problems (multipath, obstructions changing as satellites move)
- You understand check points verify environmental stability throughout survey

**Survey timing and planning:**
- Schedule surveys for morning or afternoon (stable ionosphere)
- Avoid heavy rain, storms, high wind
- Allow extra time in challenging conditions (longer fix acquisition, more careful quality verification)

**Equipment setup:**
- Antenna height (1.5-2m) reduces multipath
- Tripod stability prevents base station movement
- Proper cable connections prevent signal loss

**Real-time decisions:**
- Monitor satellite count, PDOP, precision, fix stability
- Pause surveys when quality degrades
- Resume when conditions improve
- Terminate if safety concerns (lightning, flooding)

You now have the knowledge to conduct surveys competently in real-world field environments - recognizing good conditions, adapting to challenging conditions, and maintaining quality standards throughout.

---

## Summary: Key Concepts

**Sky visibility and satellite geometry:**
- GPS requires line-of-sight to satellites (no penetration of solid objects)
- Minimum ≥10-12 satellites needed for RTK FIX
- Obstructions (trees, buildings, terrain) reduce satellite count and degrade geometry
- Elevation mask (15°) rejects low-elevation satellites (poor signal quality)
- PDOP <2.5 indicates good satellite geometry; >3.0 indicates poor geometry
- **Optimal:** Open sky from 15° above horizon upward, all directions

**Multipath interference:**
- Reflections from metal, buildings, water, ground cause position errors (5-50 cm)
- Base station: >10m from metal objects, >20m from water
- Rover: Avoid surveying near reflective surfaces when possible
- Antenna height (1.5-2m) reduces ground/water multipath
- Multipath causes unstable fix, degraded precision, position jumping
- **Mitigation:** Choose open sites, avoid reflective surfaces, observe quality indicators

**Atmospheric conditions:**
- Ionosphere (upper atmosphere): Delays signals, varies with time of day and solar activity
- Troposphere (lower atmosphere): Refraction varies with weather (humidity, temperature, pressure)
- RTK corrections cancel most atmospheric errors (base and rover through similar atmosphere)
- Heavy rain degrades signal quality, may cause loss of FIX temporarily
- Geomagnetic storms (rare) can disrupt GPS globally - postpone survey
- **Normal conditions:** Atmospheric effects minimal for RTK (<1-2 cm residual error)

**Time of day and seasonal factors:**
- **Best survey times:** Morning (08:00-11:00) or afternoon (15:00-18:00)
- Avoid sunrise/sunset (ionospheric transitions) if possible
- Dry season preferred (less rain, lower humidity) but not critical
- Vegetation: Deciduous trees less problematic in leaf-off season
- Multi-GNSS reduces time-of-day sensitivity (15-25 satellites available most times)

**Good vs. bad survey conditions:**

**Excellent conditions:**
- Open sky >15° all directions
- No metal structures, buildings, water within 20m
- Clear or partly cloudy weather (stable)
- Dry ground, no rain
- **Results:** RTK FIX <2 min, ≥15 satellites, PDOP <2.0, precision 1-2 cm H / 2-3 cm V

**Challenging conditions:**
- Partial canopy (trees to 25-30° obstruction)
- Water nearby (canal, river within 10-20m)
- Light rain, high humidity
- **Results:** RTK FIX 3-5 min, 10-12 satellites, PDOP 2.5-3.0, precision 3-5 cm H / 4-6 cm V

**Unacceptable conditions:**
- Dense canopy (>40° obstruction), narrow canyon
- Urban environment (buildings, multipath)
- Heavy rain, thunderstorm
- **Results:** RTK FIX unreliable or unattainable, <10 satellites, PDOP >3.5, precision >8-10 cm or FLOAT only

**Quality monitoring (from SURVEY_PROCESS.md):**
- Check before every point: RTK FIX status, satellite count, PDOP, precision estimates
- Quality gates: RTK FIX ≥10s, PDOP ≤2.5, Sats ≥12, Precision ≤2cm H / 3cm V
- If quality gates not met, do not save point - investigate cause, wait for improvement
- Check points verify environmental stability (drift ≤3cm H / 4cm V)

**Mitigation strategies for challenging environments:**
- **Vegetation:** Base in clearing, survey in leaf-off season, selective clearing (with permission)
- **Terrain:** Base on high ground, extended observation time, accept 4-6 cm accuracy
- **Urban:** Base in park/open space, avoid proximity to buildings, recognize degraded accuracy
- **Weather:** Postpone if storms, pause rover work during rain, resume when conditions improve
- **All:** Increase check points, redundant measurements, strict quality gate enforcement, document conditions

**Practical field guidance:**
- Pre-survey site assessment: Sky visibility, multipath sources, access, stability
- Real-time monitoring: Satellite count, PDOP, fix status, precision, stability
- Recognize warning signs: Difficulty acquiring fix, unstable fix, poor precision, check point drift
- Adapt approach: Pause and wait, relocate, adjust expectations, strengthen QA
- Document conditions: Photos, field notes, accuracy estimates reflect reality

**Critical success factors:**
- Choose survey sites with clear sky view (most important single factor)
- Avoid metal structures and water surfaces (multipath sources)
- Survey during stable weather conditions
- Monitor quality gates strictly - do not compromise on thresholds
- Use check points to verify position repeatability
- Document environmental conditions affecting survey quality

Understanding environmental factors transforms you from operator (following procedures without understanding) to practitioner (making informed decisions, adapting to conditions, ensuring quality). This knowledge enables you to conduct reliable surveys across diverse field environments and confidently assess data quality.

---

**End of Section 5.8**

This completes Chapter 5: Geospatial Concepts. You now have comprehensive understanding of:
- Survey strategies and tradeoffs (5.1)
- GNSS vs. total station positioning (5.2)
- RTK fundamentals and carrier phase positioning (5.3)
- Base and rover station roles and setup (5.4)
- RTK fix status and quality indicators (5.5)
- RINEX logging and PPP post-processing (5.6)
- Coordinate reference systems and UTM (5.7)
- Physical and environmental factors affecting survey quality (5.8)

**You are now prepared for Chapter 9: Site Survey field procedures,** which applies these concepts in step-by-step operational instructions. The geospatial concepts provide the "why" behind field procedures - enabling you to understand what you are doing, troubleshoot problems, and maintain survey quality in real-world conditions.

**Next steps in your learning:**
1. Review this chapter to consolidate understanding
2. Study SURVEY_PROCESS.md alongside Chapter 5 - connect concepts to procedures
3. Practice with equipment in controlled environment (verify understanding of fix status, quality indicators, environmental effects)
4. Conduct first field survey with supervision (apply concepts under guidance)
5. Progress to independent surveying (concepts become intuitive with experience)

The concepts may seem complex initially, but with field practice they become second nature. Understanding the principles makes you a capable, confident surveyor - able to deliver high-quality data that supports reliable OpenRiverCam discharge measurements and water resource management.

---

**[VISUAL PLACEHOLDER: Good vs bad survey site comparison showing:
- Side-by-side photos:
  - GOOD: Open field, clear sky, tripod on stable ground, no obstructions
  - BAD: Under trees, buildings nearby, narrow canyon, metal structures visible
- Satellite visibility diagrams for each (sky plot showing available satellites)
- Quality metrics comparison (satellite count, PDOP, expected precision)
- Site selection decision tree: Start → Check sky view → Check multipath sources → Check stability → Good/Marginal/Poor rating]**

**[VISUAL PLACEHOLDER: Obstruction angle diagram showing:
- Side view of surveyor with tripod
- Horizon line (0°)
- Various obstruction heights: 15° (low vegetation), 30° (medium trees), 45° (tall trees/buildings), 60° (dense canopy)
- Color-coded zones: Green (<20° obstruction = excellent), Yellow (20-30° = acceptable), Orange (30-40° = marginal), Red (>40° = poor)
- How to measure angle: fist method, clinometer app, visual estimation]**

**[VISUAL PLACEHOLDER: Multipath illustration showing:
- Satellite in sky
- Direct signal path to antenna (straight arrow, green = good)
- Reflected signal paths from: metal building, water surface, ground (curved arrows, red = bad)
- Receiver confusion: "Which signal is correct?"
- Position error diagram showing displacement due to multipath
- Prevention: Antenna height, distance from reflectors, site selection]**

**[VISUAL PLACEHOLDER: Environmental conditions decision matrix:
- Table with rows: Sky visibility, Multipath sources, Weather, Vegetation, Terrain
- Columns: Excellent / Good / Marginal / Poor
- Cell contents: Photos and criteria for each combination
- Bottom row: Recommended action (Proceed / Proceed with caution / Relocate / Postpone)
- Color-coded for quick field reference]**
