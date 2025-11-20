# 9.9 Survey Execution - Water Level

This section covers the procedure for measuring and surveying water level during site survey. Water level measurement serves two critical purposes: documenting the reference elevation for coordinate transformation and establishing baseline data for hydraulic analysis and rating curve development.

The homography transformation assumes all features lie on a plane (the water surface). Accurate water level measurement ensures this assumption is valid and enables correlation between survey-time and operation-time conditions.

By the end of this section, you will be able to:
- Measure water surface elevation accurately with RTK rover
- Record pole depth at water surface
- Document flow conditions and surface characteristics
- Take multiple measurements and average if needed
- Record water level data in SW Maps
- Connect water level to GCP survey and transformation validation

**Reference:** SURVEY_PROCESS.md Section 6 - Water Level Survey

---

## Survey Workflow Position

**In the complete survey sequence:**

1. Establish check points (CP_START)
2. Survey camera position
3. Collect sample video and survey GCPs
4. **Survey water level** ← YOU ARE HERE
5. Survey cross-section
6. Re-measure check points (CP_NOON, CP_END)

**Water level surveyed after GCPs** because GCPs are the most time-critical measurement (highest accuracy requirement). Water level measurement is quicker and can be done anytime during survey, but logical sequence is after GCPs and before cross-section.

---

## Water Level Measurement Purpose

### Why Measure Water Level

**Transformation reference plane:**

The homography transformation (Section 4.3) assumes all tracked features lie on a plane. For river monitoring:
- **The plane is the water surface**
- GCPs establish real-world coordinates of features on or near this plane
- Water level at survey time documents the elevation of this reference plane
- If water level changes between survey and operation, transformation accuracy degrades

**Example scenario:**
```
Survey conditions:
- Water level = 140.25m elevation
- GCPs surveyed at banks and waterline at 140.25m
- Transformation calibrated for water surface at 140.25m

Operational conditions (3 months later):
- Water level = 140.75m elevation (50cm higher)
- Water surface now 50cm above GCP reference plane
- Transformation has 50cm vertical error (assumes wrong elevation)
- Surface velocity measurements biased (incorrect scale)
```

**Solution:** Document water level at survey time, monitor water level during operations, recalibrate transformation if water level changes significantly (>20-30cm typical threshold).

### Additional Uses of Water Level Data

**Rating curve development (Chapter 3 connection):**
- Rating curve relates water level (stage) to discharge (Q)
- Water level measurements over time + discharge measurements = rating curve
- Survey establishes initial water level reference for rating curve development

**Flood monitoring and alert levels:**
- Survey water level = baseline or typical condition
- Compare operational water levels to survey baseline
- Identify high water or flood conditions (water level >> survey level)

**Cross-section validation:**
- Water level at time of cross-section survey documents which stations were underwater
- Enables separation of bathymetry (underwater) from bank topography (dry land)
- Water depth measurements referenced to surveyed water level

**Discharge calculation (Q = v × A):**
- Cross-sectional area A depends on water level
- Different water level = different wetted area = different discharge for same velocity
- Water level ties velocity measurements to specific flow conditions

---

## Water Level Survey Procedure

### Step 1: Identify Water Level Measurement Point

**Select appropriate location for water level measurement:**

**Ideal characteristics:**
- **Calm water surface:** Not turbulent, rapids, or eddies (steady water level easier to measure)
- **Representative of general flow:** Not local pooling, backwater, or drawdown (should represent typical water level at site)
- **Accessible for rover pole:** Bank edge, wading depth, or boat access (rover pole must reach water surface)
- **Safe access:** Stable bank, not slippery or steep (crew safety first)
- **Near cross-section or GCP area:** Water level should represent conditions in monitoring area

**Common measurement locations:**
- **Bank edge at calm pool:** Step to bank edge, lower pole into calm water
- **Shallow wading area:** Wade into river (if safe and <0.5m depth), position pole in representative flow
- **Staff gauge location:** If staff gauge installed (Section 7 site planning), measure at gauge location for correlation

**Avoid:**
- Rapids or turbulent areas (water surface moving and changing elevation)
- Eddies or backwaters (water level not representative of main channel)
- Steep or unstable banks (crew safety risk)
- Deep water requiring boat access (unless boat readily available and crew experienced)

### Step 2: Position Rover Pole at Water Surface

**From SURVEY_PROCESS.md Section 6:**

```
Water Level Survey:
- Survey water surface elevation with rover pole
- Note depth on pole, maintain RTK FIX
- Record in Water Level layer with flow conditions
- Take multiple measurements if water is moving
```

**Pole positioning procedure:**

1. **Lower rover pole until pole tip touches water surface:**
   - Pole tip should just touch water surface (not pushed below surface)
   - Observe where water meets pole (waterline on pole)
   - If water calm: pole tip position stable at water surface
   - If water moving: pole tip position may fluctuate (see Step 5 for multiple measurements)

2. **Level the pole:**
   - Use bubble level to ensure pole is vertical (not leaning)
   - Center bubble in circular level
   - Critical for accurate elevation measurement

3. **Maintain stable pole position:**
   - Hold pole steady during averaging (minimize movement)
   - Keep pole tip at water surface (do not push deeper or lift above surface)
   - Use bipod if available (much easier to maintain stable position)

### Step 3: Note Pole Depth at Water Surface

**From SURVEY_PROCESS.md Section 6:**
> Note depth on pole

**Record where water intersects the pole:**

**Method 1: Direct observation during measurement:**
- Observe which mark on pole is at water surface
- Many survey poles have graduated markings (every 10cm or every foot)
- Record in field notebook: "Water surface at 0.75m mark on pole"
- This documents how far antenna is above water surface (height of pole above water)

**Method 2: Mark pole at waterline:**
- Use hand or chalk to mark where water meets pole
- After measurement complete, measure distance from pole tip to mark
- Record: "Water surface 0.75m from pole tip"

**Purpose of pole depth notation:**
- **Quality control:** Verifies pole tip was at water surface (not pushed below or held above)
- **Documentation:** Records measurement method for future reference
- **Troubleshooting:** If water level calculation seems wrong, pole depth note helps diagnose (was pole pushed too deep?)

**Example pole depth notes:**
- "Water surface at 0.80m mark" (pole extended 0.80m into water to touch surface)
- "Pole tip at water surface, approximately 0.0m depth" (pole tip barely touching water)
- "Water surface at 1.25m mark, moderate current" (longer pole extension, water moving)

### Step 4: Achieve RTK FIX and Average

**Quality gates for water level measurement:**

Water level measurement can use slightly relaxed quality gates compared to GCPs:

- [ ] Solution type: RTK FIX (preferred) or Float (acceptable if FIX unavailable)
- [ ] Fix maintained: ≥10 seconds before starting averaging
- [ ] Satellites: ≥10 (relaxed from GCP requirement of ≥12)
- [ ] PDOP: ≤3.0 (relaxed from GCP requirement of ≤2.5)
- [ ] Horizontal precision: ≤5cm (relaxed from GCP requirement of ≤2cm)
- [ ] Vertical precision: ≤5cm (relaxed from GCP requirement of ≤3cm)

**Why relaxed quality gates acceptable:**
- Water level measurement accuracy requirement: 3-5cm (vs. 2-3cm for GCPs)
- Water surface may be moving (natural variability >5cm in turbulent conditions)
- Measurement typically taken near water (possibly challenging GPS conditions - tree overhang, bank obstruction)

**Averaging time:**
- **Calm water: 60 seconds** (standard averaging)
- **Moving water: 120 seconds** (longer averaging smooths out surface fluctuations)
- **Turbulent water: Consider multiple measurements** (see Step 5)

**During averaging:**
- Keep pole vertical (monitor bubble level)
- Keep pole tip at water surface (observe waterline on pole)
- Maintain RTK FIX (if FIX lost, extend averaging or retry)

### Step 5: Multiple Measurements and Averaging (If Needed)

**From SURVEY_PROCESS.md Section 6:**
> Take multiple measurements if water is moving

**When to take multiple measurements:**
- **Water surface moving or fluctuating:** Waves, turbulence, or flow variations cause water level to vary by >2-3cm during observation
- **Uncertain measurement quality:** First measurement had marginal quality (PDOP high, precision poor)
- **Critical reference:** Water level particularly important for this site (e.g., strong water level variability expected during operations)

**Multiple measurement procedure:**

1. **Measurement 1:** Position pole at water surface, achieve FIX, average 60-120s, record as WL1
2. **Shift position slightly (1-2m along bank):** Breaks any position "lock" or local anomaly
3. **Measurement 2:** Reposition pole at water surface, achieve FIX, average 60-120s, record as WL2
4. **Repeat for Measurement 3 if desired**

**Calculate average water level:**
```
Example:
WL1 elevation: 140.245m
WL2 elevation: 140.238m
WL3 elevation: 140.251m

Average: (140.245 + 140.238 + 140.251) / 3 = 140.245m
Spread: 1.3cm (excellent repeatability)

Use average as water level: 140.245m
```

**If spread between measurements >5cm:**
- Investigate cause: Is water level actually varying? GPS conditions unstable? Pole positioning inconsistent?
- Take additional measurements to understand variability
- Document large spread in notes: "Water level varying by 8cm due to turbulent surface, average of 5 measurements"

**For calm, stable water:** Single measurement typically sufficient (60s averaging, good quality indicators)

**For moving or turbulent water:** 2-3 measurements recommended (average provides more reliable estimate of mean water level)

### Step 6: Measure Pole Height

**Standard pole height measurement procedure (same as for GCPs):**

1. **Measure from pole tip (at water surface) to antenna reference point:**
   - Use tape measure along pole
   - Read carefully to nearest centimeter or millimeter
   - Example: "Pole height 2.35m from water surface to antenna"

2. **Record in field notebook:**
   - "Water level: Pole height 2.35m"
   - Record immediately (prevents confusion with other pole height measurements)

3. **Water level elevation calculation:**
   - Antenna elevation (from RTK measurement): Z_antenna
   - Pole height: h_pole
   - Water level elevation: Z_water = Z_antenna - h_pole
   - Example: Z_antenna = 142.60m, h_pole = 2.35m → Z_water = 142.60 - 2.35 = 140.25m

**Pole height for water level measurement may differ from GCP pole heights** (different measurement locations, different pole extensions). Measure pole height for every measurement point.

### Step 7: Record Water Level Attributes in SW Maps

**In SW Maps, use the "Water Level" layer** (configured in Section 9.5).

**Fill in all attributes:**

**Required fields:**
- `point_id`: WL1, WATER_LEVEL_1, or similar identifier
- `description`: "Water level at left bank calm pool, 5m upstream from GCP3"
- `surveyed_by`: Operator name
- `survey_time`: Timestamp (auto-filled by SW Maps)

**Measurement quality fields:**
- `satellites`: Number of satellites tracked
- `pdop`: Position dilution of precision
- `h_precision`: Horizontal precision estimate (cm)
- `v_precision`: Vertical precision estimate (cm)
- `fix_type`: "RTK FIX", "Float", or other solution type

**Measurement method fields:**
- `pole_height`: Height from water surface to antenna (e.g., 2.35m)
- `pole_depth_mark`: Where water intersected pole (e.g., "0.80m mark")
- `measurement_method`: "Rover pole to water surface" (or "Staff gauge reading" if using gauge)

**Flow condition fields:**
- `flow_conditions`: Select from:
  - "Calm" (steady water surface, minimal movement)
  - "Moderate flow" (water moving, small waves or ripples)
  - "Turbulent" (strong current, significant waves or turbulence)
  - "Rapids" (white water, highly turbulent)
- `water_clarity`: "Clear", "Turbid", "Very turbid" (optional, helps interpret optical measurements)
- `surface_conditions`: "Smooth", "Rippled", "Waves", "Debris" (optional, documents surface characteristics)

**Notes field:**
- `notes`: Additional observations
  - "Average of 3 measurements, spread 1.3cm"
  - "Water level stable during measurement"
  - "Water level rising slowly (rain upstream)"
  - "Turbulent surface, measurement challenging, precision estimate marginal"

**Save point in SW Maps after all attributes filled.**

### Step 8: Document Flow Conditions

**Flow conditions documentation is critical for interpreting discharge measurements:**

**Observe and record:**

1. **Water surface characteristics:**
   - Calm and smooth (like glass)
   - Rippled (small waves or ripples)
   - Wavy (larger waves or undulations)
   - Turbulent (strong mixing, white water, rapids)

2. **Flow velocity (qualitative):**
   - Very slow (barely moving, <0.1 m/s)
   - Slow (gentle flow, 0.1-0.3 m/s)
   - Moderate (steady flow, 0.3-0.8 m/s)
   - Fast (strong current, 0.8-1.5 m/s)
   - Very fast (rapid flow, >1.5 m/s)

3. **Debris or features on surface:**
   - Clean water surface (no debris)
   - Light debris (few floating sticks or leaves)
   - Heavy debris (many floating objects, difficult to track)
   - Foam or scum (may affect optical tracking)

4. **Water clarity:**
   - Clear (can see bottom in shallow areas)
   - Slightly turbid (reduced visibility)
   - Turbid (cannot see bottom)
   - Very turbid (muddy, opaque water)

**Why document flow conditions:**
- Correlates with discharge (faster flow = higher Q typically)
- Affects velocity measurement quality (calm surface easier to track than turbulent)
- Helps interpret operational data (if flow conditions differ from survey, velocities may differ)
- Provides context for rating curve development (different conditions = different stage-discharge relationships)

**Record flow conditions in Water Level layer attributes** and in field notebook.

### Step 9: Photograph Water Level Measurement

**Documentation photos:**

1. **Rover pole at water surface:**
   - Shows pole positioned at waterline
   - Includes context (bank, river, surroundings)
   - Demonstrates measurement method

2. **Water surface conditions:**
   - Shows flow characteristics (calm, rippled, turbulent)
   - Includes river extent and flow patterns
   - Documents conditions at survey time

3. **Close-up of pole at waterline (optional):**
   - Shows exact waterline position on pole
   - Verifies pole tip at water surface (quality control)

**Label photos:**
- WL1_measurement.jpg
- WL1_flow_conditions.jpg
- WL1_pole_closeup.jpg

---

## Water Level Calculation and Validation

### Calculate Water Level Elevation

**From RTK survey data:**
- Antenna elevation: Z_antenna (from RTK measurement, SW Maps records this)
- Pole height: h_pole (measured with tape, recorded in attributes)
- Water level elevation: Z_water = Z_antenna - h_pole

**Example calculation:**
```
RTK measurement:
- Antenna coordinates: E=685440.12, N=9456790.34, Z=142.60m
- Pole height: 2.35m

Water level calculation:
Z_water = 142.60m - 2.35m = 140.25m

Record: Water level = 140.25m (UTM 48S elevation)
```

**SW Maps can calculate this automatically** if configured with pole height subtraction (some versions support "offset" or "vertical offset" settings).

### Cross-Check Water Level with Other Measurements

**Validate water level is reasonable:**

**Compare to GCP elevations:**
- GCPs near waterline should be at or near water level elevation
- Example: Water level = 140.25m, GCP3 (waterline marker) = 140.23m → Good agreement (2cm difference)
- If large difference (>10cm): Investigate (incorrect pole height? GCP or water level measurement error?)

**Compare to cross-section elevations (after cross-section survey):**
- Cross-section stations underwater should be below water level
- Cross-section stations on banks should be above water level
- Example: Water level = 140.25m, station XS1_ST5 = 140.18m (7cm below water) → Station underwater, consistent
- Example: Water level = 140.25m, station XS1_ST1 = 140.85m (60cm above water) → Station on bank, consistent

**Compare to camera height calculation:**
- Camera elevation - water level elevation = height above water
- Example: Camera at Z=151.75m, water level = 140.25m → Height above water = 11.50m
- Cross-check with tape measurement (if camera height measured directly): Should agree within 5-10cm

**Cross-checks validate survey consistency and catch errors early.**

---

## Common Issues and Solutions

### Issue: Water surface moving or fluctuating

**Symptoms:**
- Water level varies by >5cm during observation
- Waves, ripples, or turbulence cause unstable waterline
- Difficult to maintain pole tip at consistent water surface

**Solutions:**
- **Use longer averaging time:** 120 seconds instead of 60 seconds (smooths out fluctuations)
- **Take multiple measurements:** Average 2-3 measurements to estimate mean water level
- **Measure in calmer area:** Move to side channel, pool, or backwater with calmer surface (if representative)
- **Time measurement between waves:** If periodic waves, measure during trough (lowest point) and crest (highest point), average
- **Document variability:** Record in notes: "Water level fluctuating ±8cm due to turbulence, averaged 3 measurements"

### Issue: Cannot achieve RTK FIX at water surface

**Symptoms:**
- Solution remains Float or DGNSS at measurement location
- Tree overhang, bank obstruction, or poor satellite geometry preventing FIX

**Solutions:**
- **Move measurement location:** 5-10m upstream or downstream to better GPS conditions
- **Accept Float solution:** If FIX unavailable, Float solution acceptable for water level (lower accuracy but still usable)
- **Extend averaging time:** 120-180 seconds may improve solution quality
- **Use staff gauge:** If installed and visible, read staff gauge for water level (backup measurement method)
- **Return later:** Satellite geometry improves over time, FIX may be achievable after 30-60 minutes

### Issue: Water too deep to reach with pole

**Symptoms:**
- Water surface is 3-4m below bank level (steep bank, high flow stage)
- Rover pole not long enough to reach water surface from bank

**Solutions:**
- **Wade into shallower area:** If safe, wade into river where water depth <1m (pole can reach surface from standing position)
- **Use boat:** If available and crew experienced, use boat to access water surface
- **Use staff gauge reading:** If staff gauge installed and visible, read gauge instead of direct RTK measurement
- **Estimate water level:** Use tape measure to lower weighted line to water surface, measure depth below bank reference point, calculate elevation (less accurate but better than no data)
- **Defer measurement:** If water level not critical and conditions improving (water level dropping), return later when accessible

### Issue: Uncertain pole depth notation

**Symptoms:**
- Difficult to observe waterline on pole (glare, awkward viewing angle, pole markings unclear)
- Operator not confident in recorded pole depth

**Solutions:**
- **Mark waterline with chalk or hand:** Mark exact waterline on pole, measure after averaging complete
- **Use two observers:** One holds pole, other observes waterline from different angle (improves confidence)
- **Photograph pole at waterline:** Take photo showing waterline position on pole (backup documentation)
- **Use graduated pole with clear markings:** Pre-mark pole with tape or paint at 10cm intervals (easier to read)
- **Estimate and note uncertainty:** Record best estimate with note: "Pole depth approximately 0.80m ± 5cm (difficult to read marking)"

---

## Connection to Transformation and Discharge Calculation

### Water Level and Transformation Reference Plane

**Homography transformation assumes planar surface:**
- All tracked features (floating debris, ripples, foam) lie on the water surface plane
- Water level elevation defines this plane in 3D space
- GCPs at waterline establish transformation calibration for this plane

**If water level changes significantly between survey and operation:**
- Transformation assumes water surface at survey elevation (e.g., 140.25m)
- Actual water surface at different elevation (e.g., 140.75m, 50cm higher)
- Transformation error = vertical difference = 50cm
- Surface velocity measurements biased (scale incorrect)

**Solution: Water level monitoring during operations:**
- Measure water level periodically (daily, weekly, or continuously with sensor)
- If water level changes >20-30cm from survey level: Recalibrate transformation or resurvey GCPs
- Document water level for each discharge measurement (enables correlation and rating curve)

### Water Level and Cross-Section Integration

**Cross-section survey references water level:**
- Cross-section elevations measured as absolute elevations (meters above ellipsoid)
- Water level at time of survey documents which stations were underwater vs. dry
- Water depth at each station = Water level - Bed elevation

**Example integration:**
```
Water level at survey: 140.25m

Cross-section station elevations:
XS1_ST1 (left bank): 141.15m → Dry land, 0.90m above water
XS1_ST3 (channel):   139.85m → Underwater, 0.40m depth
XS1_ST5 (thalweg):   138.75m → Underwater, 1.50m depth
XS1_ST7 (channel):   139.90m → Underwater, 0.35m depth
XS1_ST9 (right bank): 141.05m → Dry land, 0.80m above water

Wetted cross-section: Stations ST2-ST8 (water depth > 0)
Cross-sectional area: Calculated from bed elevations and water level
```

**Water level ties cross-section geometry to specific flow conditions:**
- Higher water level → larger wetted area → higher discharge for same velocity
- Lower water level → smaller wetted area → lower discharge for same velocity
- Rating curve relates water level to discharge: Q = f(h)

---

## Time Estimate

**Water level measurement: 5-10 minutes total**

- Identify measurement location and access: 1-2 minutes
- Position rover pole at water surface: 1 minute
- Achieve RTK FIX and verify quality: 1-2 minutes
- Averaging (60-120 seconds): 1-2 minutes
- Measure pole height and note pole depth: 1 minute
- Fill in attributes in SW Maps: 1-2 minutes
- Photograph water level: 1 minute

**Multiple measurements (if needed): +5 minutes per additional measurement**

**Water level is quick measurement** relative to GCP survey (60-90 minutes) or cross-section survey (20-60 minutes). Worth the time investment for critical reference data.

---

## Summary: Water Level Survey

**Purpose:**
- Document water surface elevation at survey time
- Establish transformation reference plane (homography assumes planar water surface)
- Provide baseline for rating curve development and discharge correlation
- Document flow conditions for hydraulic analysis

**Key measurements:**
- Water surface elevation (calculated: Z_water = Z_antenna - h_pole)
- Pole height (from water surface to antenna reference point)
- Pole depth notation (where water intersects pole, quality control)
- Flow conditions (calm, moderate, turbulent - affects optical tracking and discharge)

**Quality requirements:**
- RTK FIX preferred, Float acceptable (relaxed from GCP requirement)
- Accuracy: 3-5cm (relaxed from GCP requirement of 2-3cm)
- Multiple measurements if water moving (average to estimate mean water level)
- All attributes documented in SW Maps and field notebook

**Workflow sequence:**
1. Check points (CP_START)
2. Camera position
3. GCPs and sample video
4. **Water level surveyed** ← COMPLETED
5. Next: Cross-section survey (Section 9.11)

**With water level documented, you have:**
- Reference elevation for transformation validation
- Baseline data for rating curve development
- Context for discharge calculation (water level at survey = specific flow conditions)
- Quality control for cross-section survey (verifies which stations underwater)

**Move forward to Section 9.11** to survey river cross-section for bathymetry and discharge calculation. Cross-section survey will reference the water level you just measured.

---

**References:**
- SURVEY_PROCESS.md Section 6: Water Level Survey
- Section 9.6: Survey Execution - Process Overview (workflow context)
- Section 9.8: Survey Execution - Control Points and Sample Video (GCP correlation)
- Section 9.11: Survey Execution - Cross-Section Survey (next step, uses water level data)
- Chapter 3: Hydrology Concepts (Q = v × A, rating curves, water level-discharge relationship)
