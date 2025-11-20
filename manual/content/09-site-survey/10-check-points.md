# 9.10 Survey Execution - Check Points

This section covers the critical quality control procedure of establishing and monitoring check points throughout the survey. Check points validate that the RTK system maintains accuracy over time and that survey data is reliable.

Check point drift is the primary quality validation metric for the entire survey session. If drift exceeds acceptable thresholds, survey data quality is questionable, and measurements may need to be repeated.

By the end of this section, you will be able to:
- Establish a permanent check point (CP_START) with proper procedure
- Re-measure check points throughout the day (CP_NOON, CP_END)
- Calculate drift between measurements
- Interpret drift magnitude relative to acceptable thresholds
- Troubleshoot excessive drift
- Validate survey quality based on check point monitoring

**Reference:** SURVEY_PROCESS.md Section 4 - Check Points

---

## Check Point Purpose and Importance

### What Are Check Points

**Check points are permanent reference locations surveyed multiple times throughout the survey day** to validate RTK system accuracy and stability.

**From SURVEY_PROCESS.md Section 4:**

```
Check Points:
Establish CP_START:
- 20-50m from base, stable high ground
- RTK FIX for 30 seconds
- 3 independent 60s measurements
- Agreement within 1cm H, 2cm V
- Mark permanently, photograph

Monitor Throughout Day:
- CP_NOON: Re-measure after 4-6 hours
- CP_END: Final check before packing
- Total drift must be ≤3cm H, ≤4cm V
```

**Check point timeline in survey:**

```
08:00 - Base station setup begins
09:00 - Base survey-in complete, rover achieves FIX
09:15 - CP_START established (3 measurements, average position recorded)
09:30-14:30 - GCPs, water level, cross-sections surveyed
14:30 - CP_NOON re-measurement (compare to CP_START)
14:30-16:30 - Additional measurements, second cross-section, etc.
16:30 - CP_END re-measurement (compare to CP_START)
16:45 - Survey concludes, equipment packed

Total survey duration: ~8 hours
Check point monitoring: Start, midpoint, end
```

### Why Check Points Are Critical

**Quality control validation:**
- Proves RTK system delivering consistent positions over entire survey duration
- Single measurement could be accurate by luck; repeated measurements prove reliability
- Drift within tolerance (≤3-4cm) = system working correctly, data trustworthy
- Drift exceeds tolerance (>5cm) = system problem, data questionable

**Detects system failures:**
- Base station movement (tripod shifted, ground subsided)
- Radio link interruption (corrections lost, solution degraded)
- Equipment malfunction (antenna cable failure, receiver error)
- Atmospheric anomalies (ionospheric disturbance, signal interference)

**Documents survey quality:**
- Check point drift quantifies survey accuracy
- Low drift (1-2cm) = excellent quality survey
- Moderate drift (2-4cm) = acceptable quality survey
- High drift (>5cm) = poor quality survey, may require re-survey

**Provides confidence in data:**
- Before using survey data for transformation, verify check point drift acceptable
- If drift good: Proceed with confidence
- If drift poor: Investigate, correct issues, potentially re-survey

**Check points are quality assurance for the entire survey.** All GCP, water level, and cross-section measurements depend on RTK system accuracy. Check points validate this accuracy.

---

## Part 1: Establishing CP_START

**CP_START is the first and most important check point measurement.** It establishes the reference position against which all subsequent check point measurements are compared.

### Step 1: Select Check Point Location

**From SURVEY_PROCESS.md Section 4:**
> 20-50m from base, stable high ground

**Ideal check point location characteristics:**

**Stability:**
- **Solid ground that will not move:** Rock outcrop, concrete pad, stable soil (not loose sand, soft mud, or fill)
- **Above flood level:** Will not be submerged if water rises during survey
- **Not disturbed during survey:** Away from vehicle traffic, foot paths, work areas

**Accessibility:**
- **Easy to relocate:** Distinctive features nearby (large rock, tree, building corner)
- **Quick access:** Should be able to walk to check point in 2-3 minutes from work area
- **Safe access:** Stable footing, no hazards (cliffs, unstable banks, traffic)

**GPS conditions:**
- **Open sky view:** >15° elevation mask, minimal tree cover or obstructions
- **Away from reflective surfaces:** >10m from metal structures, vehicles, water (avoids multipath)
- **Representative distance from base:** 20-50m typical (similar to GCP distances, validates corrections at working range)

**Example good check point locations:**
- Large boulder with flat top (stable, easy to mark, easy to relocate)
- Concrete foundation or pad (very stable, can mark with paint or chalk)
- Exposed bedrock with distinctive feature (stable, permanent)
- Solid ground near permanent structure (building corner, fence post) for reference

**Example poor check point locations:**
- Soft ground or recently disturbed soil (may subside or shift)
- Flood plain or low-lying area (may be submerged if water rises)
- Near vehicles or equipment (may need to be moved, multipath from metal)
- Under heavy tree cover (poor satellite visibility, marginal GPS quality)

### Step 2: Mark Check Point Permanently

**Physical marking methods:**

**Preferred: Permanent mark on rock or concrete:**
- Paint or chalk mark (X, circle, or cross-hair)
- Spray paint (bright color, high contrast - orange, pink, yellow)
- Mark should be 5-10cm size (large enough to see, small enough for precise positioning)

**Acceptable: Survey stake driven firmly into ground:**
- Drive stake at least 30cm into ground (stable, will not shift easily)
- Use hammer or rock to drive stake (hand pressure insufficient)
- Mark stake top with bright flagging tape or paint (visible from distance)
- If using nail in stake top: Drive nail flush or slightly recessed (provides precise reference point)

**Temporary (if permanent marking not allowed):**
- Natural feature with identifiable point (specific point on large rock, tree root intersection)
- Document carefully with photos and description (must be able to relocate precisely)
- Note in field notes: "Check point is apex of triangular granite outcrop, 2m south of oak tree"

**Purpose of marking:**
- Enables precise repositioning of rover pole for re-measurement
- Reduces operator variability (different operators can find exact same point)
- Provides permanent reference if return visit needed (future re-survey, verification)

### Step 3: Photograph Check Point

**Documentation photos:**

1. **Close-up showing mark clearly:**
   - Mark in center of frame
   - Sharp focus (not blurry)
   - Shows mark type (painted X, stake, rock point)

2. **Context photo showing surroundings:**
   - Shows check point relative to nearby features (rocks, trees, structures)
   - Wide enough view to aid relocation (if returning weeks or months later)
   - Include base station in background if visible (shows proximity)

3. **Long-distance reference photo:**
   - Stand 10-20m away, photograph check point location
   - Shows approach path and general context
   - Helps orient for relocation

**Label photos:**
- CP_START_closeup.jpg
- CP_START_context.jpg
- CP_START_approach.jpg

**Photos serve as backup for relocating check point** if physical mark is disturbed or obscured.

### Step 4: Take Three Independent Measurements

**From SURVEY_PROCESS.md Section 4:**
> 3 independent 60s measurements
> Agreement within 1cm H, 2cm V

**Why three measurements:**
- Proves repeatability (single measurement could be lucky)
- Identifies outliers (if one measurement differs significantly, operator error likely)
- Provides average position (more reliable than single measurement)

**Independent measurement procedure:**

**Measurement 1:**
1. Position rover pole tip precisely on check point mark center
2. Level pole (bubble centered)
3. Verify RTK FIX maintained ≥30 seconds (ensures stable FIX before averaging)
4. Start 60-second averaging in SW Maps
5. Keep pole vertical and stable throughout averaging
6. Measure pole height (tip to antenna reference point)
7. Fill in attributes: point_id = CP_START_1, description = "Check point measurement 1"
8. Save point

**Break between measurements:**
- Lift rover pole from check point
- Walk around briefly (10-20 steps away and back, or circle check point)
- Purpose: Breaks any "lock" or memory effect in receiver positioning
- Wait 10-20 seconds before next measurement

**Measurement 2:**
- Reposition rover pole on check point mark (independent positioning, not just setting pole down in same spot)
- Repeat full procedure: level pole, verify FIX ≥30s, average 60s, measure pole height, save as CP_START_2

**Measurement 3:**
- Repeat full procedure again, save as CP_START_3

**Quality requirements for each measurement:**
- RTK FIX maintained throughout 60-second averaging
- Satellites ≥12, PDOP ≤2.5
- Horizontal precision ≤2cm, Vertical precision ≤3cm
- Pole vertical (bubble centered)
- Pole height measured for each (should be very similar, ~2.00m ± 2cm)

### Step 5: Verify Repeatability and Calculate Average

**Compare the three measurements:**

**Example calculation:**
```
CP_START measurements (after subtracting pole height, ground elevation):

Measurement 1: E = 685432.234, N = 9456782.178, Z = 142.456
Measurement 2: E = 685432.228, N = 9456782.182, Z = 142.461
Measurement 3: E = 685432.231, N = 9456782.175, Z = 142.458

Calculate differences:
Horizontal (E, N):
  E range: 685432.234 - 685432.228 = 0.006m = 0.6cm
  N range: 685432.182 - 685432.175 = 0.007m = 0.7cm
  Max horizontal difference: ~1.0cm ✓ (within 1cm threshold)

Vertical (Z):
  Z range: 142.461 - 142.456 = 0.005m = 0.5cm ✓ (within 2cm threshold)

Calculate average position:
E_avg = (685432.234 + 685432.228 + 685432.231) / 3 = 685432.231
N_avg = (9456782.178 + 9456782.182 + 9456782.175) / 3 = 9456782.178
Z_avg = (142.456 + 142.461 + 142.458) / 3 = 142.458

CP_START reference position: E = 685432.231, N = 9456782.178, Z = 142.458
```

**Acceptable repeatability:**
- Horizontal spread ≤1cm: **Excellent** (confirms precise positioning and stable RTK)
- Vertical spread ≤2cm: **Excellent**
- These thresholds from SURVEY_PROCESS.md Section 4

**If repeatability exceeds thresholds (>1cm H or >2cm V):**
- Investigate causes:
  - **Pole positioning inconsistent?** Practice positioning pole tip on exact mark center
  - **Pole not vertical?** Check bubble level more carefully, use bipod
  - **RTK quality marginal?** Check satellites, PDOP, precision estimates
  - **Multipath or obstruction?** Move check point 2-3m to better location
  - **Inadequate averaging?** Extend averaging to 120 seconds
- Take additional measurements (4th, 5th) to understand variability
- If cannot achieve acceptable repeatability: **Do not proceed with survey** (RTK system not delivering required accuracy)

**If repeatability good:** Record average position as CP_START reference, proceed with survey.

### Step 6: Record CP_START Reference in Field Notebook

**Field notebook documentation:**

```
Check Point CP_START
Date: 2024-11-15
Time: 09:15-09:25
Location: Granite boulder 35m west of base station, 15m upstream from camera

Physical mark: Orange spray paint X on boulder top

Three measurements:
CP_START_1: E=685432.234, N=9456782.178, Z=142.456, Pole=2.02m
CP_START_2: E=685432.228, N=9456782.182, Z=142.461, Pole=2.01m
CP_START_3: E=685432.231, N=9456782.175, Z=142.458, Pole=2.02m

Repeatability:
H: 0.7cm (excellent)
V: 0.5cm (excellent)

Average reference position (CP_START):
E = 685432.231 m
N = 9456782.178 m
Z = 142.458 m

Quality indicators:
Satellites: 14-15
PDOP: 1.7-1.9
H precision: 1.2-1.5cm
V precision: 2.0-2.3cm

All measurements RTK FIX, 60s averaging
Check point approved for survey quality control
```

**Field notebook is authoritative reference** for CP_START position. All drift calculations reference this recorded position.

---

## Part 2: Re-measuring Check Points (CP_NOON and CP_END)

**After establishing CP_START, re-measure the check point at intervals throughout the survey** to validate continued accuracy.

### CP_NOON: Midpoint Check

**From SURVEY_PROCESS.md Section 4:**
> CP_NOON: Re-measure after 4-6 hours

**Purpose:**
- Validates RTK system still accurate after several hours of operation
- Detects problems early (if drift large at midpoint, stop survey and investigate)
- Provides quality assurance before completing second half of survey

**Timing:**
- After 4-6 hours of surveying (midpoint of typical 8-10 hour survey day)
- After completing most GCPs and water level (critical measurements done)
- Before cross-section or additional measurements (validates quality before continuing)

**Procedure:**

1. **Return to CP_START location** (use photos and description to relocate mark precisely)

2. **Take single measurement:**
   - Position rover pole tip on check point mark (same physical mark as CP_START)
   - Level pole (bubble centered)
   - Verify RTK FIX ≥30 seconds
   - Average 60 seconds (same as CP_START measurements)
   - Measure pole height
   - Fill in attributes: point_id = CP_NOON, description = "Check point midpoint measurement"
   - Save point

3. **Calculate drift from CP_START:**
   - Compare CP_NOON coordinates to CP_START average coordinates
   - Calculate horizontal drift: Δ_H = sqrt((E_NOON - E_START)² + (N_NOON - N_START)²)
   - Calculate vertical drift: Δ_V = |Z_NOON - Z_START|

**Example drift calculation:**
```
CP_START average: E = 685432.231, N = 9456782.178, Z = 142.458
CP_NOON measurement: E = 685432.248, N = 9456782.165, Z = 142.443

Horizontal drift:
Δ_E = 685432.248 - 685432.231 = +0.017m = +1.7cm
Δ_N = 9456782.165 - 9456782.178 = -0.013m = -1.3cm
Δ_H = sqrt(1.7² + 1.3²) = sqrt(2.89 + 1.69) = sqrt(4.58) = 2.1cm ✓

Vertical drift:
Δ_V = |142.443 - 142.458| = |-0.015| = 1.5cm ✓

Drift within acceptable limits (≤3cm H, ≤4cm V)
Survey quality validated, continue with second half
```

### Acceptable Drift Thresholds

**From SURVEY_PROCESS.md Section 4:**
> Total drift must be ≤3cm H, ≤4cm V

**Drift interpretation:**

**Excellent quality (≤1cm H, ≤2cm V):**
- Minimal drift, system performing optimally
- Survey data high confidence
- Proceed with full confidence

**Good quality (1-2cm H, 2-3cm V):**
- Low drift, system stable
- Survey data reliable
- Proceed with confidence

**Acceptable quality (2-3cm H, 3-4cm V):**
- Moderate drift, approaching threshold
- Survey data acceptable but not optimal
- Proceed with caution, monitor closely

**Marginal quality (3-4cm H, 4-5cm V):**
- Drift at or slightly exceeding threshold
- Survey data questionable
- Investigate cause before proceeding
- Consider re-surveying if critical measurements

**Poor quality (>4cm H or >5cm V):**
- Excessive drift, system problem likely
- Survey data unreliable
- **Do not proceed** until issue resolved
- Investigate and correct problem, potentially re-survey all measurements

### Troubleshooting Excessive Drift

**If CP_NOON drift exceeds acceptable thresholds, investigate causes:**

**Cause 1: Base station moved**

**Symptoms:**
- Systematic drift in one direction (all measurements shifted consistently)
- Drift magnitude correlates with base distance (farther points have more drift)

**Check:**
- Inspect base station tripod (has it shifted or subsided?)
- Check ground mark beneath tripod (does tripod still align with mark?)
- Look for signs of disturbance (foot prints, vehicle tracks, wind damage)

**Solution:**
- If base moved: **Survey compromised, consider re-survey**
- If base stable: Investigate other causes

**Cause 2: Radio link interruption**

**Symptoms:**
- Solution reverted to Float or DGNSS during some measurements (noticed in logs or SW Maps data)
- Intermittent RTK FIX (achieves FIX, then loses it, then re-achieves)

**Check:**
- Verify rover receiving RTCM corrections (check age of corrections in GNSS Master)
- Test radio link (check signal strength, interference, battery level)
- Review SW Maps logs (were all measurements in FIX mode?)

**Solution:**
- If radio link was interrupted: Identify which measurements affected (may need to re-measure those)
- If radio link stable: Investigate other causes

**Cause 3: Atmospheric conditions**

**Symptoms:**
- Drift develops gradually over time (not sudden)
- Affects all measurements somewhat equally (not localized to one area)
- Satellite quality indicators degrade (PDOP increases, precision estimates worsen)

**Check:**
- Compare quality indicators from CP_START and CP_NOON (satellites, PDOP)
- Check weather conditions (heavy clouds, storm fronts can affect GPS)

**Solution:**
- Wait for conditions to improve (30-60 minutes)
- Extend averaging times (120 seconds instead of 60 seconds)
- Accept slightly higher drift threshold if systematic and consistent (document in notes)

**Cause 4: Operator error (check point repositioning)**

**Symptoms:**
- Drift magnitude similar to expected positioning error (2-5cm)
- Only one check point measurement affected (CP_NOON high drift, CP_START was good)

**Check:**
- Was pole positioned on exact same mark as CP_START? (verify with photos)
- Was pole vertical? (bubble centered throughout averaging?)
- Was pole height measured correctly? (compare to CP_START pole heights, should be similar)

**Solution:**
- Re-measure CP_NOON (careful positioning, verify bubble level, careful pole height measurement)
- If second CP_NOON measurement shows low drift: First measurement was operator error
- If second CP_NOON measurement also shows high drift: System problem, not operator error

### CP_END: Final Validation

**From SURVEY_PROCESS.md Section 4:**
> CP_END: Final check before packing

**Purpose:**
- Final validation of survey quality before leaving site
- Calculates cumulative drift over entire survey session (8-10 hours typical)
- Provides confidence that all survey data reliable

**Timing:**
- After completing all survey measurements (GCPs, water level, cross-sections)
- Before packing equipment and leaving site
- Typically 6-8 hours after CP_START

**Procedure:**
- Same as CP_NOON (single measurement, 60s averaging, compare to CP_START)
- Calculate drift: Δ_H and Δ_V from CP_START to CP_END
- Evaluate total drift relative to thresholds (≤3cm H, ≤4cm V)

**Example CP_END calculation:**
```
CP_START average: E = 685432.231, N = 9456782.178, Z = 142.458
CP_END measurement: E = 685432.253, N = 9456782.192, Z = 142.441

Horizontal drift:
Δ_E = +2.2cm
Δ_N = +1.4cm
Δ_H = sqrt(2.2² + 1.4²) = 2.6cm ✓ (within 3cm threshold)

Vertical drift:
Δ_V = 1.7cm ✓ (within 4cm threshold)

Total survey drift: 2.6cm H, 1.7cm V
Quality: Good (well within acceptable limits)
Survey validated, data reliable for transformation and discharge
```

**If CP_END drift acceptable:**
- Survey successful, data validated
- Proceed with data export and backup (Section 9.6)
- Use survey data with confidence for PtBox configuration

**If CP_END drift excessive:**
- Survey quality questionable
- Investigate cause (same troubleshooting as CP_NOON)
- Consider re-survey if critical deployment (transformation accuracy depends on survey quality)
- If re-survey not feasible: Document large drift, note increased uncertainty in survey data

---

## Check Point Monitoring Best Practices

### Continuous Monitoring Throughout Survey

**Beyond CP_NOON and CP_END, consider additional check point measurements:**

**If passing near check point:**
- Quick re-measurement (5 minutes) provides continuous quality validation
- Example: After surveying GCP1-GCP4 (2 hours), passing near check point, measure CP_MID1

**If quality concerns arise:**
- RTK FIX intermittent during some measurements
- Satellite quality degraded (PDOP increased, satellites decreased)
- Unusual observations (coordinates seem offset, repeatability poor)
- **Re-measure check point immediately** to validate system still accurate

**If survey extends over multiple days:**
- Establish check point on Day 1, re-measure at end of Day 1 (CP_DAY1_END)
- Re-measure check point at start of Day 2 (CP_DAY2_START)
- Compare Day 2 START to Day 1 average (validates system recalibrated correctly)

### Multiple Check Points for Large Surveys

**For extensive surveys (>100m extent, multiple cross-sections, complex sites):**

**Establish 2-3 check points:**
- CP1 near base station (validates near-field accuracy)
- CP2 near GCP cluster (validates accuracy in monitoring area)
- CP3 far from base (validates accuracy at maximum range)

**Re-measure all check points at midpoint and end:**
- Validates spatial consistency (drift uniform across site or localized?)
- Provides redundancy (if one check point disturbed, others validate)

**Example multi-check-point scenario:**
```
Large river site, 150m monitoring extent:
- Base station on left bank high ground
- CP1: 30m from base (near-field check)
- CP2: 80m from base, center of monitoring area (mid-range check)
- CP3: 140m from base, far cross-section (far-range check)

Midpoint re-measurement:
CP1_NOON drift: 1.8cm H, 2.1cm V (good)
CP2_NOON drift: 2.3cm H, 2.8cm V (good)
CP3_NOON drift: 3.5cm H, 4.2cm V (marginal)

Interpretation: Drift increases with distance from base (expected behavior)
CP3 drift marginally acceptable, suggests baseline length approaching limits
Consider second base station or shorter baseline for better accuracy at range
```

### Field Notebook Documentation

**Record all check point measurements systematically:**

**CP_START section:**
- Three measurements with full coordinates and quality indicators
- Repeatability calculation
- Average reference position
- Photos and mark description

**CP_NOON section:**
- Single measurement with full coordinates
- Drift calculation (Δ_H, Δ_V)
- Comparison to thresholds
- Decision: Continue survey or investigate?

**CP_END section:**
- Single measurement with full coordinates
- Drift calculation from CP_START
- Total survey drift assessment
- Survey validation: Pass or Fail?

**Example field notebook page:**
```
CHECK POINT MONITORING SUMMARY
Site: Ciliwung River Bridge
Date: 2024-11-15

CP_START (09:15): E=685432.231, N=9456782.178, Z=142.458
Repeatability: 0.7cm H, 0.5cm V (excellent)

CP_NOON (14:30): E=685432.248, N=9456782.165, Z=142.443
Drift: 2.1cm H, 1.5cm V (good - within limits)
Action: Continued survey

CP_END (16:30): E=685432.253, N=9456782.192, Z=142.441
Total drift: 2.6cm H, 1.7cm V (good - within limits)

SURVEY QUALITY VALIDATION: PASS ✓
All measurements reliable for transformation and discharge
```

---

## Connection to Survey Quality and Data Use

### Check Point Drift Validates Survey Data

**Check points provide confidence level for all survey measurements:**

**If check point drift ≤2cm H / ≤3cm V:**
- GCP survey: High confidence in 2-3cm accuracy claim
- Water level: High confidence in 3-5cm accuracy
- Cross-section: High confidence in 5-10cm accuracy
- Transformation: Expect low reprojection error (<5cm)

**If check point drift 2-4cm H / 3-5cm V:**
- GCP survey: Moderate confidence, accuracy may be 3-5cm rather than 2-3cm
- Water level: Moderate confidence, accuracy 5-8cm
- Cross-section: Moderate confidence, accuracy 8-12cm
- Transformation: Expect moderate reprojection error (5-10cm)

**If check point drift >4cm H / >5cm V:**
- GCP survey: Low confidence, accuracy may be 5-10cm or worse
- Water level: Low confidence, significant uncertainty
- Cross-section: Lower accuracy requirements, may still be acceptable (10-15cm)
- Transformation: Expect high reprojection error (>10cm), may need resurvey

**Check point drift sets realistic expectations** for how accurate the transformation and discharge calculations will be.

### Reporting Survey Quality

**Include check point data in survey report or documentation:**

```
Survey Quality Summary:
Site: Ciliwung River Bridge
Date: 2024-11-15
Survey duration: 09:00-16:45 (7.75 hours)

Check Point Monitoring:
- CP_START established at 09:15 (3 measurements, repeatability 0.7cm H / 0.5cm V)
- CP_NOON at 14:30, drift 2.1cm H / 1.5cm V (within acceptable limits)
- CP_END at 16:30, drift 2.6cm H / 1.7cm V (within acceptable limits)

Survey Quality Assessment:
- Check point drift well within acceptable thresholds (≤3cm H, ≤4cm V)
- RTK system stable and accurate throughout survey session
- All survey data validated for use in transformation and discharge calculation

Expected Measurement Accuracy:
- GCPs: 2-3cm (high confidence)
- Water level: 3-5cm (high confidence)
- Cross-section: 5-10cm (validated)
- Transformation reprojection error: <5cm (expected)
```

---

## Time Estimates

**CP_START establishment (one-time):**
- Select and mark location: 5 minutes
- Photograph: 2 minutes
- Three measurements (3 × 3 minutes): 9 minutes
- Calculate repeatability and average: 3 minutes
- Field notebook documentation: 3 minutes
- **Total: 20-25 minutes**

**CP_NOON or CP_END re-measurement (each):**
- Walk to check point: 2 minutes
- Single measurement: 3 minutes
- Calculate drift: 2 minutes
- Field notebook documentation: 2 minutes
- **Total: 5-10 minutes each**

**Total check point time for survey:**
- CP_START: 20-25 minutes
- CP_NOON: 5-10 minutes
- CP_END: 5-10 minutes
- **Total: 30-45 minutes over entire survey day**

**Check points are small time investment** (30-45 minutes) for critical quality validation (validates 6-8 hours of survey work and all downstream data use).

---

## Summary: Check Point Monitoring

**Purpose:**
- Validate RTK system accuracy and stability over time
- Detect system problems (base station movement, equipment malfunction, atmospheric issues)
- Provide quality control for entire survey (all measurements depend on RTK accuracy)
- Document survey quality for data users and reporting

**Procedure:**

**CP_START (beginning of survey):**
1. Select stable, accessible location with good GPS conditions (20-50m from base)
2. Mark permanently (paint on rock or survey stake)
3. Photograph (close-up and context)
4. Take 3 independent measurements (60s averaging each, walk around between measurements)
5. Verify repeatability (≤1cm H, ≤2cm V)
6. Calculate average position (CP_START reference)
7. Record in field notebook

**CP_NOON (after 4-6 hours):**
1. Return to CP_START location
2. Take single measurement (60s averaging)
3. Calculate drift from CP_START (Δ_H and Δ_V)
4. Evaluate drift relative to thresholds (≤3cm H, ≤4cm V)
5. Continue survey if drift acceptable, investigate if excessive

**CP_END (end of survey):**
1. Return to CP_START location
2. Take single measurement (60s averaging)
3. Calculate total drift from CP_START
4. Validate survey quality (Pass if ≤3cm H / ≤4cm V)
5. Document final quality assessment

**Acceptable drift thresholds:**
- Horizontal: ≤3cm (excellent if ≤2cm, acceptable if 2-3cm, marginal if 3-4cm, poor if >4cm)
- Vertical: ≤4cm (excellent if ≤2cm, acceptable if 3-4cm, marginal if 4-5cm, poor if >5cm)

**If drift excessive:**
- Investigate: Base station moved? Radio link interrupted? Atmospheric conditions? Operator error?
- Resolve issue before continuing or concluding survey
- Consider re-survey if critical and drift very large (>5cm)

**Outcomes:**
- Check point monitoring validates survey quality
- Low drift = high confidence in all survey data (GCPs, water level, cross-section)
- Moderate drift = acceptable quality, document uncertainty
- High drift = survey questionable, investigate and potentially re-survey

**With check point monitoring complete and drift within acceptable limits, you have validated survey quality and can proceed with confidence to use survey data for transformation and discharge calculation.**

---

**References:**
- SURVEY_PROCESS.md Section 4: Check Points
- Section 9.6: Survey Execution - Process Overview (workflow context and quality control)
- Section 9.1: Survey Concepts Overview (RTK accuracy and error sources)
- Chapter 5: Geospatial Concepts (coordinate accuracy and uncertainty)
