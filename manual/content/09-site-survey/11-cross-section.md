# 9.11 Survey Execution - Cross-Section Survey

This section covers the procedure for surveying river cross-sections. Cross-section bathymetry is essential for discharge calculation because discharge equals velocity multiplied by cross-sectional area (Q = v × A). While OpenRiverCam measures surface velocity, converting this to discharge requires knowing the geometry of the channel.

Cross-section survey captures the shape of the river bed from left bank to right bank, documenting bed elevations, water depths, and channel geometry. This data combines with velocity measurements to calculate discharge and develop rating curves.

By the end of this section, you will be able to:
- Understand cross-section purpose and connection to discharge calculation
- Establish cross-section reference points on banks
- Determine appropriate station spacing
- Survey systematic transect from left bank to right bank
- Record water depth at each station
- Measure pole height for each measurement
- Document cross-section data in SW Maps
- Connect cross-section to water level and velocity measurements

**Reference:** SURVEY_PROCESS.md Section 8 - Cross-Section Survey

---

## Survey Workflow Position

**In the complete survey sequence:**

1. Establish check points (CP_START)
2. Survey camera position
3. Collect sample video and survey GCPs
4. Survey water level
5. **Survey cross-section** ← YOU ARE HERE
6. Re-measure check points (CP_NOON, CP_END)

**Cross-section surveyed after water level** because water level measurement documents which stations are underwater vs. dry land. Cross-section is typically the final measurement task before CP_END validation.

---

## Cross-Section Purpose and Connection to Discharge

### Why Survey Cross-Sections

**From Chapter 3 hydrology concepts:**

**Discharge equation: Q = v × A**

Where:
- Q = discharge (m³/s or cubic meters per second)
- v = mean velocity (m/s, from OpenRiverCam surface velocity × depth-correction factor)
- A = cross-sectional area (m², from cross-section survey)

**OpenRiverCam measures surface velocity (v_surface).** To calculate discharge:

1. **Measure surface velocity** from camera images (PIV or optical tracking)
2. **Convert to mean velocity:** v_mean = v_surface × k (where k ≈ 0.85-0.90, velocity correction factor)
3. **Determine cross-sectional area (A)** from surveyed bathymetry and current water level
4. **Calculate discharge:** Q = v_mean × A

**Without cross-section survey, cannot calculate discharge.** Velocity alone is insufficient - must know channel geometry.

### Cross-Section Defines Channel Geometry

**Cross-section provides:**

**Bed elevation profile:**
- Elevation of river bed at multiple stations across channel
- Shape of channel (V-shaped, U-shaped, trapezoidal, compound channel)
- Location of thalweg (deepest point)

**Water depth distribution:**
- Depth at each station (water level - bed elevation)
- Wetted perimeter (total length of bed in contact with water)
- Hydraulic radius (area / wetted perimeter, affects flow resistance)

**Cross-sectional area calculation:**
- Divide cross-section into segments between stations
- Calculate area of each segment (trapezoidal approximation)
- Sum segments to get total cross-sectional area: A = Σ A_segments

**Example cross-section calculation:**
```
Water level: 140.25m
Cross-section stations (10 stations, 2m spacing):

Station  Distance  Bed Elev  Water Depth  Notes
-------  --------  --------  -----------  -----
ST1      0m        141.15m   Dry (0.0m)   Left bank
ST2      2m        140.45m   Dry (0.0m)   Bank slope
ST3      4m        139.95m   0.30m        Waterline
ST4      6m        139.65m   0.60m        Channel
ST5      8m        138.75m   1.50m        Thalweg (deepest)
ST6      10m       139.55m   0.70m        Channel
ST7      12m       139.85m   0.40m        Channel
ST8      14m       140.35m   Dry (0.0m)   Bank slope
ST9      16m       141.05m   Dry (0.0m)   Right bank

Wetted width: ST3 to ST7 = 10m
Cross-sectional area A ≈ 7.5 m² (sum of trapezoidal segments)

If mean velocity v = 0.6 m/s:
Discharge Q = v × A = 0.6 × 7.5 = 4.5 m³/s
```

### Rating Curve Development

**From Chapter 3 connection:**

**Rating curve relates water level (stage) to discharge:**
- Measure discharge at multiple water levels (Q₁, Q₂, Q₃ at h₁, h₂, h₃)
- Fit curve: Q = f(h), typically power law Q = a × (h - h₀)^b
- Use rating curve for future discharge estimates (measure h, look up Q)

**Cross-section enables rating curve development:**
- Cross-section provides A at different water levels
- For each water level h, calculate wetted area A(h)
- Measure velocity v(h) with OpenRiverCam
- Calculate discharge Q(h) = v(h) × A(h)
- Plot Q vs. h, fit rating curve

**Cross-section is static (channel geometry), water level varies:**
- Survey cross-section once (unless channel morphology changes)
- Measure water level continuously or periodically
- Calculate cross-sectional area for current water level: A = A(h_current)
- Combine with velocity measurement to get discharge: Q = v × A(h_current)

**This is why cross-section survey is essential for operational discharge monitoring.**

---

## Cross-Section Survey Procedure

### Step 1: Establish Cross-Section Line and Reference Points

**From SURVEY_PROCESS.md Section 8:**

```
Cross-Section Survey:
Establish LB/RB reference points on stable ground
Plan station spacing (1-2m typical)
```

**Select cross-section location:**

**Ideal characteristics:**
- **Perpendicular to flow:** Cross-section line crosses river at right angle to flow direction (minimizes flow angle effects)
- **Straight reach:** Not at bend, expansion, or constriction (flow is uniform and representative)
- **Stable bed:** Not actively eroding or depositing (cross-section remains valid over time)
- **Representative of monitoring area:** Near camera field of view or velocity measurement location
- **Accessible:** Safe to wade or survey from banks (crew safety paramount)

**Common cross-section locations:**
- At bridge or structure (provides fixed reference, easy to resurvey)
- Upstream or downstream from camera (documents flow conditions in monitoring reach)
- At natural control (rock outcrop, stable riffle) that stabilizes channel geometry

**Establish reference points:**

**Left Bank Reference (LB_START):**
1. Select stable point on left bank (looking downstream)
   - Above flood level (will not be submerged during high flows)
   - Permanent feature (rock, tree, structure) or mark with survey stake
   - Open sky view for GPS (good RTK conditions)
2. Survey LB_START with rover (60s averaging, standard quality gates)
3. Record as cross-section reference point (layer: Discharge Cross Section or Level Cross Section)
4. Mark and photograph (enables future resurvey)

**Right Bank Reference (RB_END):**
1. Select stable point on right bank (looking downstream)
   - Aligned approximately perpendicular to flow with LB_START
   - Similar characteristics as LB_START (stable, permanent, good GPS)
2. Survey RB_END with rover
3. Record as cross-section reference point
4. Mark and photograph

**Reference points anchor the cross-section** and enable precise resurvey in the future (if channel morphology changes, or for multi-year monitoring).

### Step 2: Plan Station Spacing

**From SURVEY_PROCESS.MD Section 8:**
> Plan station spacing (1-2m typical)

**Station spacing depends on:**

**Channel complexity:**
- **Simple channel (uniform bed, gentle slopes):** 2-3m spacing adequate (fewer stations, faster survey)
- **Complex channel (variable bed, steep banks, multiple thalwegs):** 1-1.5m spacing needed (more stations for accuracy)

**Channel width:**
- **Narrow channel (<10m wide):** 1m spacing or finer (need sufficient resolution)
- **Medium channel (10-30m wide):** 1.5-2m spacing typical (balance resolution and survey time)
- **Wide channel (>30m wide):** 2-3m spacing acceptable (many stations even with coarse spacing)

**Example spacing decisions:**
```
Small stream (8m wide, simple bed):
- Station spacing: 1.5m
- Number of stations: 8m / 1.5m ≈ 6 stations
- Survey time: 6 stations × 3 min/station = 18 minutes

Medium river (18m wide, moderately complex):
- Station spacing: 2m
- Number of stations: 18m / 2m = 9 stations
- Survey time: 9 stations × 3 min/station = 27 minutes

Large river (45m wide, complex with multiple channels):
- Station spacing: 3m for banks, 1.5m for main channel (variable spacing)
- Number of stations: ~20 stations
- Survey time: 20 stations × 3 min/station = 60 minutes
```

**General guidance:**
- **Minimum stations: 8-10** (provides reasonable cross-section profile)
- **Typical stations: 10-15** (good balance for most rivers)
- **Complex channels: 15-25+** (captures detailed bathymetry)

**Closer spacing in areas with rapid depth change:**
- Thalweg area (deepest part, depth changes rapidly)
- Bank slopes (elevation changes rapidly)
- Underwater features (ledges, steps, boulders)

**Coarser spacing in uniform areas:**
- Flat banks (elevation constant)
- Uniform channel bed (depth changes gradually)

### Step 3: Walk Cross-Section Transect from Left Bank to Right Bank

**From SURVEY_PROCESS.md Section 8:**
> Walk LB → RB systematically

**Systematic transect procedure:**

1. **Start at LB_START (left bank reference point)**
   - Verify LB_START surveyed and recorded
   - This is Station 0 or Station 1 (depending on numbering preference)

2. **Pace or measure to first station:**
   - If 2m spacing: Walk 2m from LB_START perpendicular toward right bank
   - Use tape measure for precision, or pace (calibrate your pace: typical pace ≈ 0.8-1.0m)
   - Mark station location temporarily (stick, rock, or visual alignment)

3. **Survey station (detailed procedure in Step 4 below)**

4. **Move to next station:**
   - Advance 2m (or planned spacing) along transect line
   - Keep transect reasonably straight (perpendicular to flow)
   - Visual alignment: Look back at LB_START and ahead to RB_END (stay on line)

5. **Continue systematically until reaching RB_END:**
   - Survey all stations: ST1, ST2, ST3, ..., ST_N
   - Do not skip stations (gaps create interpolation errors in cross-sectional area)
   - Verify reached right bank (RB_END should be last or second-to-last station)

**Walking transect in water:**

**If wading required (shallow water):**
- Wade carefully (test footing, use wading staff or pole for support)
- Maintain transect line (current may push you downstream, correct course)
- Safety first: Do not wade if >waist deep, fast current (>1 m/s), or unstable bed

**If water too deep to wade:**
- Use boat (if available and crew experienced with boat surveying)
- Survey from banks only (left bank edge, right bank edge, interpolate middle - less accurate but acceptable)
- Use sonar or depth sounder (boat-mounted, provides bed elevations without wading)
- If no boat or sonar: Cross-section survey may not be feasible (document limitation)

### Step 4: Survey Each Station

**For each cross-section station, follow this procedure:**

#### Position Rover Pole at Station

1. **Position pole tip on channel bed (or ground if on bank):**
   - Lower pole until tip rests on bed
   - Push pole firmly but not excessively (tip should just touch solid bed, not pushed into soft sediment)
   - If underwater: Push pole through water to bed

2. **Level the pole:**
   - Use bubble level (center bubble)
   - Pole must be vertical (not leaning upstream/downstream or left/right)
   - Critical for accurate elevation measurement

3. **Maintain stable position:**
   - Keep pole on bed (not floating or lifted)
   - Keep pole vertical throughout averaging
   - If current strong: Brace pole or use bipod for stability

#### Note Water Depth on Pole

**If station underwater:**

**From SURVEY_PROCESS.md Section 8:**
> Record water depth

1. **Observe where water surface intersects pole:**
   - Look at pole markings (many poles have graduated marks every 10cm or 0.5ft)
   - Note water depth: Distance from pole tip (on bed) to water surface
   - Example: "Water surface at 1.2m mark on pole" = 1.2m water depth at this station

2. **Record water depth in field notebook:**
   - Station ST5: Water depth 1.2m (marked on pole)
   - This is backup documentation if SW Maps attribute entry incomplete

**If station on dry land (bank):**
- Water depth = 0 (or "Dry")
- Note in attributes: "Bank station, no water"

**Why record water depth:**
- Quality control: Verifies pole tip on bed (not floating or pushed into sediment)
- Cross-check calculation: Water depth = Water level - Bed elevation (from survey)
- Documents survey conditions: Identifies wetted vs. dry stations

#### Achieve RTK FIX and Average

**Quality gates for cross-section survey:**

Cross-section can use relaxed quality gates compared to GCPs:

- [ ] Solution type: RTK FIX (preferred) or Float (acceptable for cross-sections)
- [ ] Fix maintained: ≥10 seconds before starting averaging
- [ ] Satellites: ≥10 (relaxed from GCP ≥12)
- [ ] PDOP: ≤3.0 (relaxed from GCP ≤2.5)
- [ ] Horizontal precision: ≤5cm (relaxed from GCP ≤2cm)
- [ ] Vertical precision: ≤8cm (relaxed from GCP ≤3cm)

**Why relaxed quality acceptable:**
- Cross-section accuracy requirement: 5-10cm (vs. 2-3cm for GCPs)
- Cross-sectional area calculation averages many measurements (individual point errors average out)
- Measurement often in water or near banks (challenging GPS conditions)

**Averaging time:**
- **Standard: 60 seconds** (typical for cross-section stations)
- **Challenging conditions: 120 seconds** (if quality marginal, near obstructions, or accuracy critical)

**During averaging:**
- Keep pole tip on bed (not lifted or pushed deeper)
- Keep pole vertical (monitor bubble level)
- Maintain RTK FIX (if lost, extend averaging or retry)

#### Measure Pole Height

**From SURVEY_PROCESS.md Section 8:**
> Measure pole height tip-to-ARP each shot

1. **Measure from pole tip (on bed) to antenna reference point:**
   - Use tape measure along pole
   - Read carefully to nearest centimeter
   - Example: "Pole height 2.85m from bed to antenna"

2. **Record in field notebook:**
   - Station ST5: Pole height 2.85m
   - Record immediately (prevents confusion between stations)

**Pole height calculation:**
- Antenna elevation: Z_antenna (from RTK measurement)
- Pole height: h_pole
- Bed elevation: Z_bed = Z_antenna - h_pole
- Example: Z_antenna = 142.10m, h_pole = 2.85m → Z_bed = 142.10 - 2.85 = 139.25m

**Pole height varies between stations** (water depth differs, pole extension adjusts):
- Deep water: Pole extended longer (taller pole height, e.g., 3.5m)
- Shallow water: Pole retracted shorter (shorter pole height, e.g., 2.2m)
- Dry bank: Pole shortest (pole height ~2.0m)

**Measure pole height at EVERY station.** Do not assume pole height constant across transect.

#### Fill in Cross-Section Attributes in SW Maps

**In SW Maps, use "Discharge Cross Section" or "Level Cross Section" layer** (configured in Section 9.5).

**Fill in all attributes:**

**Required fields:**
- `point_id`: XS1_ST5 (Cross-section 1, Station 5)
  - Systematic numbering: XS1_ST1, XS1_ST2, XS1_ST3, ...
  - Identifies which cross-section and which station within that cross-section
- `description`: "Cross-section station 5, 8m from left bank, thalweg"
- `surveyed_by`: Operator name
- `survey_time`: Timestamp (auto-filled)

**Cross-section identification fields:**
- `cross_section_id`: XS1 (or CROSS_SECTION_1, identifies which cross-section)
- `station_number`: 5 (sequential station number within cross-section)
- `point_role`: "Cross-section station" (or "Bank reference" if LB_START/RB_END)

**Position and measurement fields:**
- `distance_from_LB`: 8m (distance along transect from left bank reference)
  - Calculate from coordinates after survey, or measure directly with tape
  - Enables plotting cross-section profile (distance vs. elevation)
- `water_depth`: 1.2m (depth measured on pole, or calculated: water level - bed elevation)
- `pole_height`: 2.85m (measured with tape, from bed to antenna)
- `bed_elevation`: 139.25m (calculated: Z_antenna - pole_height, or calculate post-survey)

**Quality indicator fields:**
- `satellites`: Number of satellites
- `pdop`: Position dilution of precision
- `h_precision`: Horizontal precision (cm)
- `v_precision`: Vertical precision (cm)
- `fix_type`: "RTK FIX", "Float", etc.

**Notes field:**
- `notes`: Additional observations
  - "Thalweg, deepest point in cross-section"
  - "Bank station, dry land"
  - "Gravel bed, firm footing"
  - "Soft mud bed, pole pushed 5cm into sediment (bed elevation may be overestimated)"

**Save point in SW Maps after all attributes filled.**

#### Photograph Station (Selected Stations)

**Photograph selected stations for documentation:**

**Photograph LB_START and RB_END:**
- Shows transect endpoints (enables resurvey)
- Context photos showing surroundings

**Photograph thalweg or deepest station:**
- Shows maximum water depth
- Documents channel morphology

**Photograph representative bank stations:**
- Shows bank slope and vegetation
- Documents survey access and conditions

**Not necessary to photograph every station** (would be too many photos). Focus on key stations: endpoints, thalweg, bank slopes.

**Label photos:**
- XS1_LB_START.jpg
- XS1_ST5_thalweg.jpg
- XS1_RB_END.jpg

### Step 5: Complete Transect and Verify Coverage

**After surveying all stations:**

1. **Verify reached right bank reference (RB_END):**
   - Last station should be at or near RB_END
   - If RB_END not surveyed: Add as final station

2. **Check for gaps in station sequence:**
   - Review station numbers: ST1, ST2, ST3, ..., ST_N (continuous sequence)
   - If gap (e.g., ST5 missing): Return and survey missing station
   - Gaps create interpolation errors in cross-sectional area calculation

3. **Verify spatial coverage:**
   - Plot stations on map in SW Maps (should form roughly straight line across river)
   - Verify coverage spans full river width (left bank to right bank)

4. **Check for anomalies in data:**
   - Review bed elevations: Should vary smoothly (not jumps or outliers)
   - Example anomaly: ST4 = 139.2m, ST5 = 141.5m, ST6 = 139.3m (ST5 is outlier, likely error)
   - If anomaly detected: Re-survey suspect station

**Quality cross-section has:**
- Complete coverage (left bank to right bank, no gaps)
- Sufficient resolution (station spacing captures bed shape)
- Smooth profile (bed elevations vary logically, no gross errors)
- Documented water depths (identifies wetted vs. dry stations)

---

## Cross-Section Data Processing and Validation

### Calculate Bed Elevations

**From survey data:**
- Antenna elevation: Z_antenna (recorded by SW Maps from RTK measurement)
- Pole height: h_pole (measured with tape, recorded in attributes)
- Bed elevation: Z_bed = Z_antenna - h_pole

**SW Maps can calculate automatically** if configured with pole height offset, or calculate in post-processing:

**Example calculation for Station 5:**
```
RTK measurement: Z_antenna = 142.10m (UTM 48S elevation)
Pole height: h_pole = 2.85m (measured from bed to antenna)

Bed elevation:
Z_bed = 142.10 - 2.85 = 139.25m

This is elevation of river bed at Station 5
```

**Calculate bed elevation for all stations** (post-processing in spreadsheet or GIS).

### Calculate Water Depths

**From water level survey (Section 9.9) and bed elevations:**
- Water level: Z_water (e.g., 140.25m from Section 9.9 measurement)
- Bed elevation: Z_bed (calculated above)
- Water depth: d = Z_water - Z_bed

**Example calculation:**
```
Water level (from Section 9.9): Z_water = 140.25m

Station bed elevations and water depths:
ST1: Z_bed = 141.15m, d = 140.25 - 141.15 = -0.90m (negative = dry, 0.90m above water)
ST3: Z_bed = 139.95m, d = 140.25 - 139.95 = +0.30m (underwater, 0.30m depth)
ST5: Z_bed = 138.75m, d = 140.25 - 138.75 = +1.50m (underwater, 1.50m depth)
...
```

**Cross-check calculated depths with measured depths:**
- Measured depth (from pole observation): "Water surface at 1.2m mark"
- Calculated depth (from elevations): d = 1.50m
- Difference: 0.3m (reasonable agreement, accounting for measurement uncertainty and pole reading error)
- If large difference (>20cm): Investigate (pole height error? water level error? bed elevation error?)

### Plot Cross-Section Profile

**Visualize cross-section geometry:**

**X-axis: Distance from left bank (m)**
- ST1 at 0m, ST2 at 2m, ST3 at 4m, etc.

**Y-axis: Elevation (m)**
- Bed elevation for each station
- Water level as horizontal line

**Example plot:**
```
Elevation (m)
   142 |                  RB
       |              *
   141 |         *            * LB
       |
   140 |________________*____________  ← Water level
       |            *      *
   139 |         *
       |
   138 |              * ← Thalweg (deepest point)
       |
       +-----|-----|-----|-----|-----|
           0     5    10    15    20
                Distance from LB (m)
```

**Profile shows:**
- Channel shape (V-shaped, U-shaped, trapezoidal)
- Bank slopes (steep vs. gentle)
- Thalweg location (deepest point, typically near center)
- Wetted width (distance between waterlines on left and right banks)

**Visual inspection validates survey quality:**
- Profile looks reasonable? (smooth bed, logical shape)
- Any obvious errors? (jumps, outliers, impossible geometry)
- Wetted width matches field observations?

### Calculate Cross-Sectional Area

**Trapezoidal approximation (standard method):**

**Divide cross-section into segments between adjacent stations:**
- Segment 1: Between ST1 and ST2
- Segment 2: Between ST2 and ST3
- ...
- Segment N-1: Between ST(N-1) and ST(N)

**For each segment, calculate trapezoidal area:**
```
Segment area = (distance between stations) × (average water depth)

A_segment = Δx × (d₁ + d₂) / 2

Where:
Δx = distance between stations (e.g., 2m)
d₁ = water depth at station 1 (if dry, d = 0)
d₂ = water depth at station 2
```

**Example calculation:**
```
Segment ST3-ST4:
Δx = 2m (station spacing)
d_ST3 = 0.30m (water depth at ST3)
d_ST4 = 0.60m (water depth at ST4)

A_segment = 2.0 × (0.30 + 0.60) / 2 = 2.0 × 0.45 = 0.90 m²
```

**Sum all segment areas:**
```
Total cross-sectional area A = Σ A_segments

Example (9 stations, 8 segments):
Segment ST1-ST2: 0.00 m² (both dry)
Segment ST2-ST3: 0.15 m² (ST2 dry, ST3 shallow)
Segment ST3-ST4: 0.90 m² (both wet)
Segment ST4-ST5: 2.10 m² (increasing depth)
Segment ST5-ST6: 2.20 m² (near thalweg, deep)
Segment ST6-ST7: 1.10 m² (decreasing depth)
Segment ST7-ST8: 0.20 m² (ST8 shallow, ST9 dry)
Segment ST8-ST9: 0.00 m² (both dry)

Total A = 0.00 + 0.15 + 0.90 + 2.10 + 2.20 + 1.10 + 0.20 + 0.00 = 6.65 m²
```

**This cross-sectional area (6.65 m²) is used in discharge calculation:**
- Measure mean velocity with OpenRiverCam: v = 0.65 m/s
- Calculate discharge: Q = v × A = 0.65 × 6.65 = 4.3 m³/s

---

## Additional Cross-Sections

**Many sites benefit from multiple cross-sections:**

### Upstream and Downstream Cross-Sections

**Purpose:**
- Validate channel geometry consistency (are conditions uniform or variable?)
- Provide redundancy (if one cross-section becomes invalid due to erosion/deposition, other still usable)
- Capture changing geometry (in non-uniform reaches, multiple cross-sections capture variation)

**Procedure:**
- Survey second cross-section 10-50m upstream or downstream from first
- Use same procedure (establish LB/RB references, systematic transect, record all attributes)
- Number as XS2 (distinguish from XS1)
- Compare XS1 and XS2 profiles (similar or different?)

### Cross-Section at Control Point

**For rating curve development:**
- Survey cross-section at hydraulic control (riffle, rock outcrop, weir)
- Control stabilizes stage-discharge relationship (more reliable rating curve)
- Cross-section at control provides geometry for rating curve calculations

### Longitudinal Profile (Optional)

**In addition to lateral cross-sections:**
- Survey longitudinal thalweg profile (deepest points along river length)
- Provides bed slope and channel gradient data
- Useful for hydraulic modeling or complex discharge calculations

**Not typically required for basic OpenRiverCam deployment** (lateral cross-sections sufficient for Q = v × A).

---

## Common Issues and Solutions

### Issue: Water too deep to measure safely

**Symptoms:**
- Water depth >1.5m in mid-channel (unsafe to wade)
- Strong current (>1 m/s) makes wading unsafe
- No boat or sonar available

**Solutions:**
- **Survey banks only:** Measure left and right bank stations, interpolate middle (less accurate but acceptable)
- **Use weighted line:** Lower weighted tape measure or rope to bed, measure depth (less accurate than RTK pole)
- **Use sonar or depth sounder:** Boat-mounted or handheld acoustic sensor measures depth (combine with GPS for position)
- **Return at low flow:** Schedule survey during dry season or low flow conditions when wading safer
- **Document limitation:** Note in survey report: "Cross-section limited to wadeable areas, mid-channel interpolated"

### Issue: Soft bed (pole sinks into sediment)

**Symptoms:**
- Pole tip pushed into soft mud or loose sand
- Difficult to know when pole reaches firm bed
- Bed elevation may be overestimated (pole below true bed surface)

**Solutions:**
- **Use wide-foot pole tip:** Flat plate or disk on pole tip prevents sinking (distributes weight)
- **Push until resistance:** Push firmly but not excessively, stop when feeling firm resistance
- **Note in attributes:** "Soft mud bed, pole may have penetrated 5-10cm"
- **Accept uncertainty:** Soft bed inherently uncertain (±5-10cm typical)
- **Resurvey during dry season:** Measure bed when exposed (no water, firm surface)

### Issue: Cannot maintain straight transect line

**Symptoms:**
- Current pushes operator downstream while wading
- Difficult to stay aligned between LB_START and RB_END
- Stations plot on map as curved line (not straight)

**Solutions:**
- **Use visual alignment:** Frequently look back at LB_START and ahead at RB_END (stay on line between them)
- **Use tape or rope:** Stretch tape measure or rope across river (provides physical guide)
- **Accept minor deviations:** Curved transect acceptable if deviations small (±1-2m)
- **Use coordinate correction:** Calculate perpendicular distance from station to transect line, plot "corrected" profile

### Issue: RTK FIX difficult to maintain in water

**Symptoms:**
- Solution reverts to Float while wading (loses FIX)
- Tree overhang or steep banks obstruct satellites
- Quality indicators poor (high PDOP, low satellite count)

**Solutions:**
- **Wait for FIX:** Pause at each station until RTK FIX achieved (may take 1-2 minutes)
- **Accept Float solution:** Cross-section accuracy requirements less strict (5-10cm), Float acceptable
- **Extend averaging time:** 120 seconds instead of 60 seconds (improves solution quality)
- **Survey during better satellite geometry:** Early morning or late afternoon sometimes better than midday
- **Document solution type:** Note which stations were Float vs. FIX (expect lower accuracy for Float stations)

### Issue: Unclear where to end cross-section

**Symptoms:**
- Right bank slope very gradual (extends far from water)
- Uncertain how far up bank to survey
- Risk of incomplete transect (missing bank stations)

**Solutions:**
- **Survey to stable high ground:** Continue transect until clearly above flood level (stable reference)
- **Survey 1-2 stations beyond waterline:** Ensure bank slope fully captured
- **Use engineering judgment:** If bank extends 20m above water, stopping at 5-10m above water sufficient for most purposes
- **Error on side of too many stations:** Better to survey extra bank stations than to end transect too soon

---

## Time Estimates

**Cross-section survey time depends on number of stations:**

**Per station (typical time):**
- Position rover and achieve FIX: 1 minute
- Averaging (60-120 seconds): 1-2 minutes
- Measure pole height and water depth: 30 seconds
- Fill in attributes: 1 minute
- **Total per station: 3-5 minutes**

**Complete cross-section examples:**

**Simple cross-section (8 stations, 2m spacing, 16m width):**
- Establish LB/RB references: 10 minutes
- Survey 8 stations: 8 × 3 min = 24 minutes
- Photos and documentation: 5 minutes
- **Total: 35-40 minutes**

**Moderate cross-section (12 stations, 1.5m spacing, 18m width):**
- Establish references: 10 minutes
- Survey 12 stations: 12 × 4 min = 48 minutes
- Photos and documentation: 5 minutes
- **Total: 60-65 minutes (1 hour)**

**Complex cross-section (20 stations, variable spacing, 30m width):**
- Establish references: 15 minutes
- Survey 20 stations: 20 × 4 min = 80 minutes
- Photos and documentation: 10 minutes
- **Total: 105 minutes (1.75 hours)**

**Multiple cross-sections:**
- First cross-section: Full time (establish procedure, troubleshoot issues)
- Second cross-section: 70-80% of first cross-section time (crew experienced, workflow efficient)

---

## Connection to Discharge Calculation and Rating Curves

### Immediate Use: Discharge Calculation

**Cross-section enables discharge calculation for survey conditions:**

1. **Survey cross-section at current water level** (Section 9.11)
2. **Document water level at survey time** (Section 9.9): Z_water = 140.25m
3. **Calculate cross-sectional area A** from bed elevations and water level: A = 6.65 m²
4. **Measure surface velocity with OpenRiverCam** (operational data): v_surface = 0.75 m/s
5. **Convert to mean velocity:** v_mean = v_surface × k = 0.75 × 0.87 = 0.65 m/s (assuming k=0.87)
6. **Calculate discharge:** Q = v_mean × A = 0.65 × 6.65 = 4.3 m³/s

**This discharge corresponds to water level 140.25m** (survey condition).

### Long-Term Use: Rating Curve Development

**Cross-section enables discharge calculation at different water levels:**

**As water level changes, cross-sectional area changes:**
- Higher water level → larger wetted area → higher A
- Lower water level → smaller wetted area → lower A

**Calculate A for different water levels using surveyed cross-section:**
```
Water level 140.00m: A = 5.2 m²
Water level 140.25m: A = 6.7 m² (survey condition)
Water level 140.50m: A = 8.4 m²
Water level 140.75m: A = 10.3 m²
```

**Measure velocity at different water levels** (OpenRiverCam operational data over weeks/months):
```
Date        h (m)    v_mean (m/s)   A (m²)   Q (m³/s)
2024-11-15  140.25   0.65           6.7      4.4
2024-11-22  140.45   0.72           8.0      5.8
2024-12-03  140.60   0.80           9.1      7.3
2024-12-18  140.15   0.58           5.9      3.4
...
```

**Plot Q vs. h, fit rating curve:**
- Rating curve: Q = a × (h - h₀)^b
- Fit parameters a, b, h₀ from discharge measurements
- Use rating curve to estimate Q from h (measure water level, look up discharge)

**Cross-section survey is the foundation** that enables discharge calculation at any water level (past, present, or future).

---

## Summary: Cross-Section Survey

**Purpose:**
- Document river bed geometry (bathymetry) for discharge calculation
- Provide cross-sectional area data (A in Q = v × A equation)
- Enable rating curve development (discharge at different water levels)
- Support hydraulic analysis and flood modeling

**Key measurements:**
- Bed elevation at each station (Z_bed = Z_antenna - h_pole)
- Water depth at each station (d = Z_water - Z_bed, or measured on pole)
- Station position (distance from left bank, spatial coordinates)
- Water level at survey time (documents which stations underwater vs. dry)

**Procedure:**
1. Establish cross-section line perpendicular to flow
2. Survey left bank and right bank reference points (LB_START, RB_END)
3. Plan station spacing (1-2m typical, adjust based on channel complexity)
4. Walk systematic transect from left bank to right bank
5. At each station:
   - Position rover pole on bed (vertical, stable)
   - Note water depth on pole (if underwater)
   - Achieve RTK FIX and average 60-120s
   - Measure pole height (tip to antenna)
   - Fill in all attributes (station number, water depth, pole height)
   - Save point in SW Maps
6. Complete transect (verify coverage, check for gaps)
7. Calculate bed elevations and cross-sectional area (post-processing)

**Quality requirements:**
- RTK FIX or Float acceptable (accuracy 5-10cm)
- Complete coverage (left bank to right bank, no gaps in station sequence)
- Sufficient resolution (station spacing captures bed shape)
- Water depths documented (identifies wetted area)

**Workflow sequence:**
1. Check points (CP_START)
2. Camera position
3. GCPs and sample video
4. Water level
5. **Cross-section surveyed** ← COMPLETED
6. Next: CP_END validation (Section 9.10, verify survey quality before leaving site)

**With cross-section surveyed, you have:**
- Complete bathymetric data for discharge calculation (Q = v × A)
- Foundation for rating curve development (A at different water levels)
- Baseline data for monitoring channel morphology changes (resurvey periodically)
- Integration with velocity measurements for operational discharge estimates

**Final survey step: Return to check point for CP_END measurement** (Section 9.10) to validate survey quality before leaving site.

---

**References:**
- SURVEY_PROCESS.md Section 8: Cross-Section Survey
- Section 9.9: Survey Execution - Water Level (water level data used to calculate water depths)
- Section 9.10: Survey Execution - Check Points (final quality validation)
- Chapter 3: Hydrology Concepts (Q = v × A, rating curves, cross-sectional area calculations)
- Section 4.3: Coordinate Transformations (homography provides velocity, cross-section provides area for discharge)
