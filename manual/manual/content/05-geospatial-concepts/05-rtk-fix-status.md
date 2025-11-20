# 5.5 RTK Fix Status

This is the single most important concept for field surveying: understanding RTK fix status.

Everything in your survey workflow depends on knowing when you have RTK fix. Fix means centimeter accuracy and you can survey. Float or single means inadequate accuracy and you must wait.

This section explains:
- What "fix" actually means in technical terms
- The difference between fix and float (and why it matters critically)
- When you can collect survey points safely
- Quality indicators that tell you fix is reliable
- How to troubleshoot situations where you cannot achieve fix
- Realistic expectations for achieving and maintaining fix

Mastering fix status recognition is the key skill that separates successful RTK surveying from unreliable data collection. This section gives you the detailed understanding to operate confidently in the field.

---

## What is RTK Fix?

Section 5.3 introduced the concept of carrier phase ambiguity resolution. This section provides deeper practical understanding.

### The Ambiguity Problem

Remember from Section 5.3: RTK achieves centimeter accuracy by measuring carrier phase - your position within the GPS radio wave.

**GPS L1 signal wavelength: ~19 centimeters**

If you can measure "I am 0.735 of the way through this wave cycle," you get sub-centimeter measurement resolution.

**The challenge:** You do not know WHICH wave cycle you are measuring.

**Analogy:** Imagine measuring distance with meter sticks laid end-to-end. You have a very precise tool that tells you "You are 0.347 meters along a meter stick." But you do not know if you are on meter stick number 100, 101, or 102.

**Your measurement:** X meters + 0.347m where X is unknown

This is precise (to the millimeter) but not accurate (you do not know which meter you are measuring).

**For GPS carrier phase:**
- You measure 0.735 of a wavelength (very precise measurement)
- But you do not know if you are in wave cycle 1,000,000 or 1,000,001 or 1,000,002
- Each wrong cycle = 19 cm position error
- **This unknown cycle count is the "integer ambiguity"**

### Ambiguity Resolution: The Fix Process

**RTK fix means the receiver has resolved the integer ambiguities.**

**How resolution works (simplified):**

The RTK receiver uses multiple strategies simultaneously:

**1. Multiple satellites:**
- You receive signals from 12-20 satellites
- Each satellite has its own ambiguity (unknown cycle count)
- But the ambiguities are mathematically related - your receiver is in one specific location that must be consistent across all satellites
- Receiver tests different integer combinations to find the one set that makes all satellites agree on the same position

**2. Multiple frequencies:**
- Modern receivers track L1 and L2 GPS signals simultaneously (different frequencies)
- Different wavelengths create patterns that help narrow down which cycle you are measuring
- Like using two rulers with different spacing - the combined pattern repeats less frequently

**3. Time series:**
- Receiver tracks satellites continuously over time
- Satellite geometry changes as satellites move across sky
- Watching how measurements change over time helps constrain possible ambiguity values

**4. Differential baseline:**
- Both base and rover track same satellites
- Base has resolved its own position (survey-in)
- Comparing base and rover measurements (double-differencing) cancels many errors and makes ambiguity resolution easier

**When resolution succeeds:**
- Receiver determines: "Satellite 1 is wave cycle 1,000,532, Satellite 2 is cycle 987,432..." (all integer values determined)
- Position calculated using these resolved ambiguities
- Accuracy: 1-3 centimeters
- **Status: RTK FIX**

**When resolution fails:**
- Receiver cannot determine integer values with confidence
- Position calculated using approximate (floating-point) ambiguity estimates
- Accuracy: 10-100 centimeters
- **Status: RTK FLOAT**

### What "Fix" Means Operationally

**Fix = The RTK receiver has successfully determined the integer ambiguities and is calculating position with centimeter accuracy.**

**Characteristics of fix solution:**
- Ambiguities resolved to integer values
- Position calculation uses fixed (not floating) ambiguity values
- Accuracy: 1-3 cm horizontal, 2-4 cm vertical typical
- Solution stable (does not jump around)
- **This is what you need for surveying**

**Fix does NOT mean:**
- Perfect accuracy (still 1-3 cm uncertainty)
- Absolutely certain (small possibility of wrong ambiguity resolution - rare with good satellite geometry)
- Permanent (can lose fix if satellite conditions degrade)

**Fix DOES mean:**
- Ready to survey
- Adequate accuracy for GCP measurement
- Meeting quality requirements for OpenRiverCam transformation

---

## Float vs Fix: The Critical Distinction

Understanding why float is inadequate is essential. Many beginners make the mistake of surveying with float because it "looks pretty good."

### Float Solution Characteristics

**Float = Receiver receiving corrections from base, but ambiguities not resolved to integer values.**

**What happens in float:**
- Receiver has narrowed down ambiguities to approximate values
- Example: Ambiguity is somewhere between 1,000,531.2 and 1,000,532.8 (not yet determined to be exactly 1,000,532)
- Position calculated using decimal approximations of ambiguities
- Accuracy: 0.1-1 meter typical (much better than no corrections, but not centimeter-level)

**Why float seems deceptively good:**
- Position is much better than single solution (2-10 meters)
- Position may appear stable on screen (does not jump around much)
- Precision estimates might show "0.15m" which seems close to the 0.02m target
- **But it is NOT adequate for centimeter surveying**

### The Deceptive Nature of Float

**Common beginner mistake:**

You arrive at GCP, check the rover display:
- Status: FLOAT
- Precision estimate: 0.18 meters horizontal
- Position appears stable on screen
- You think: "0.18 meters is pretty close to my 0.02m requirement. That seems good enough. I will save this point."

**This is WRONG. You must have FIX, not FLOAT.**

**Why float is inadequate:**

**Experiment demonstrating float unreliability:**

Survey the same GCP three times in one day:

**Measurement 1 (Float solution):**
- East: 100.347m, North: 200.521m, Elevation: 150.189m
- Precision estimate: 0.15m

**Measurement 2 (Float solution, 2 hours later):**
- East: 100.291m, North: 200.508m, Elevation: 150.227m
- Difference from Measurement 1: 5.6cm E, 1.3cm N, 3.8cm elevation

**Measurement 3 (Fix solution, 4 hours later):**
- East: 100.023m, North: 200.503m, Elevation: 150.145m
- Precision estimate: 0.015m
- Difference from Measurement 1: **32.4cm E**, 1.8cm N, **4.4cm elevation**
- Difference from Measurement 2: 26.8cm E, 0.5cm N, 8.2cm elevation

**Analysis:**
- Float solutions (1 and 2) differed by 5.6 cm - seems OK
- Fix solution (3) differed from float by **26-32 cm** - NOT OK!
- The fix solution is the true position (±1-3cm)
- Float solutions were systematically wrong by 25-30 cm
- **Float precision estimates (0.15m) did not capture true error**

**Conclusion: Float is not adequate. You must have fix.**

### Why Float Precision Estimates Are Unreliable

**Precision estimates in float are based on signal quality and geometry** - how scattered the measurements are. They do NOT account for the unresolved ambiguity error.

**Analogy:** Imagine measuring someone's height with a very precise ruler, but you do not know if you are measuring from ground level, 1 meter above ground, or 2 meters above ground.

Your ruler gives you millimeter precision: "Height is 172.347 cm above reference point."

But your uncertainty about which reference point = tens of centimeters error.

**Your precision estimate: 0.1 cm (ruler resolution)**
**Your accuracy error: 50-100 cm (wrong reference point)**

**Float solution is similar:** Centimeter-level precision relative to wrong reference (unresolved ambiguity). This does not provide centimeter accuracy.

### When Float Appears Better Than It Is

Float solution can be misleading in specific scenarios:

**Short observation time:**
- Float position over 10-20 seconds might appear stable
- But if you measured same point 10 minutes later, float position could shift 10-50 cm
- Fix position measured 10 minutes apart: Within 1-3 cm

**Good satellite geometry:**
- Float with excellent conditions (PDOP 1.2, 20 satellites) might show precision "0.10m"
- This seems close to fix precision "0.015m"
- But the ambiguity error is still present (20-40 cm typical)
- **Do not be fooled - you still need fix**

**Comparison to autonomous GPS:**
- Float (0.5m accuracy) seems amazing compared to phone GPS (5m accuracy)
- For navigation, float is excellent
- **For surveying GCPs, float is inadequate - you need 50× better accuracy**

**Critical rule: For surveying, fix is required. Do not survey with float, no matter how good it looks.**

---

## The Three Solution Types

Your RTK rover can report three different solution types. Understanding all three helps you interpret status displays.

### Single (Autonomous) Solution

**Single = Receiver using satellite signals alone, no corrections from base station.**

**Characteristics:**
- No correction data received (or receiver ignoring corrections)
- Standard GPS positioning using satellite signals
- Accuracy: 2-10 meters typical (same as phone GPS)
- Similar to autonomous positioning mode

**When you see single:**
- Base station not transmitting corrections
- Rover not receiving corrections (radio link broken)
- Rover just powered on (has not yet acquired correction stream)
- Rover configured incorrectly (not set to RTK mode)

**What to do:**
- Check base station operational
- Check radio link (rover radio on, in range)
- Wait for rover to acquire correction stream (may take 30-60 seconds after power-on)
- Verify rover configuration (should be in "rover" or "moving base" mode)

**Single solution is completely inadequate for surveying** - 2-10 meter accuracy vs 0.02m requirement.

### Float Solution

**Float = Receiver receiving corrections, but carrier phase ambiguities not resolved.**

**Characteristics:**
- Correction data being received from base
- Corrections applied to satellite measurements
- Ambiguities estimated as decimal values (not integers)
- Accuracy: 0.1-1 meter typical
- Much better than single, but not adequate for surveying

**When you see float:**
- Normal during initial RTK startup (receiver working toward fix)
- Insufficient satellites or poor geometry (cannot resolve ambiguities)
- Signals too noisy (multipath, interference prevents resolution)
- Just lost fix (reverted to float when conditions degraded)
- Very long baseline (>10 km from base - ambiguity resolution fails)

**What to do:**
- If just started rover: Wait patiently (5-20 minutes for initial fix)
- If conditions inadequate: Wait for satellite geometry to improve, or move to better location
- If lost fix: Return to open sky location, wait for fix to re-establish (typically 2-5 minutes)

**Float solution is inadequate for surveying** - 0.1-1 meter accuracy vs 0.02m requirement.

### Fix (Fixed) Solution

**Fix = Ambiguities successfully resolved, centimeter-level accuracy achieved.**

**Characteristics:**
- Correction data received from base
- Integer ambiguities successfully resolved
- Position calculated using fixed ambiguity values
- Accuracy: 1-3 cm horizontal, 2-4 cm vertical typical
- Stable, reliable solution

**When you achieve fix:**
- Good satellite conditions: ≥12 satellites, PDOP ≤2.5
- Clean signals (open sky, minimal multipath)
- Adequate correction data (age <3 seconds)
- Reasonable baseline (<10 km from base)
- Sufficient time for ambiguity resolution (5-20 minutes initial, faster if re-acquiring)

**What to do:**
- **Survey!** This is what you need
- Verify other quality indicators (PDOP, precision estimates)
- Collect measurements while fix is maintained
- Move efficiently between points to maintain fix

**Fix solution is required for surveying** - 1-3 cm accuracy meets 0.02m target (with margin).

### Visual Indicators of Solution Type

Different software displays solution type differently. Learn to recognize your system's indicators.

**SW Maps (typical OpenRiverCam data collector):**
- Text status: "RTK FIX", "RTK FLOAT", "SINGLE" or "AUTONOMOUS"
- Color coding:
  - Green background = Fix (ready to survey)
  - Yellow/orange background = Float (wait, not ready)
  - Red/gray background = Single (not receiving corrections)
- Time since fix: "FIX 0:02:35" = fix maintained for 2 minutes 35 seconds

**GNSS Master (Android mock location app):**
- Solution quality code: 4 = Fix, 5 = Float, 1 = Single
- Numeric display may show "Q=4" for fix quality

**Other RTK systems:**
- "FIXED" or "FIX" or "INTEGER" = Fix status
- "FLOAT" or "FLOATING" = Float status
- "AUTONOMOUS" or "STANDALONE" or "DGPS" = Single/differential (not RTK)

**Hardware indicator lights (some receivers):**
- Solid green = Fix
- Blinking green/yellow = Float
- Red or no light = Single/no solution

**Learn your specific system's indicators before field deployment.**

---

## When to Collect Survey Points

This is the operational decision: when is it safe to save a survey point?

### Quality Gates for Standard Survey Points

**From SURVEY_PROCESS.md - all requirements must be met:**

**Solution type: RTK FIX**
- Absolutely required
- Float is not adequate
- Single is completely inadequate

**Fix duration: ≥10 seconds**
- Fix must be stable for at least 10 seconds
- Ensures ambiguities definitely resolved (not false fix)
- Reduces risk of momentary fix that reverts to float

**Satellite count: ≥12 satellites**
- More satellites = better reliability
- Typical with good sky view: 15-25 satellites (multi-GNSS receiver)
- Marginal: 10-12 satellites (fix possible but less reliable)
- Inadequate: <10 satellites (fix difficult or unlikely)

**PDOP: ≤2.5**
- Position Dilution of Precision - geometric quality indicator
- Lower is better: 1.0-1.5 excellent, 1.5-2.0 good, 2.0-2.5 acceptable
- >2.5 = poor geometry (satellites bunched, not well-distributed)

**Precision estimates: ≤2cm horizontal / 3cm vertical**
- Estimated accuracy based on signal quality and geometry
- Horizontal typically better than vertical (normal for GNSS)
- If precision exceeds limits: Extend averaging time, improve conditions, or move location

**Age of corrections: <3 seconds**
- How recently base corrections received
- <1 second ideal (real-time)
- 1-3 seconds acceptable
- >3 seconds marginal (degraded link, old corrections)
- >10 seconds or "no corrections" = base link lost

**All six requirements must be met simultaneously before saving point.**

### Quality Gates for Canal/Challenging Conditions

**From SURVEY_PROCESS.md - relaxed standards for difficult environments:**

**Solution type: RTK FIX**
- Still required (never compromise on fix vs float)

**Fix duration: ≥10 seconds**
- Still required

**Satellite count: ≥10 satellites**
- Reduced from 12 (recognize that canal environments have limited sky view)

**PDOP: ≤3.0**
- Relaxed from 2.5 (accept poorer geometry in challenging conditions)

**Precision estimates: ≤4cm horizontal / 6cm vertical**
- Relaxed from 2cm/3cm (accept slightly lower precision)
- Still adequate for OpenRiverCam transformation

**Averaging time: 120 seconds (vs 60s standard)**
- Longer averaging compensates for poorer conditions
- Reduces measurement noise

**When to use canal standards:**
- Narrow irrigation canals with limited sky view
- Vegetation overhanging measurement locations
- Urban environments with buildings restricting sky
- Any challenging environment where standard gates cannot be achieved

**When NOT to use canal standards:**
- Open river sites where standard conditions achievable
- Do not relax standards unnecessarily
- Use tighter standards when possible for best accuracy

### Pre-Survey Quality Check

**Before starting averaging for a survey point, systematically verify all quality gates:**

**Step 1: Position rover at survey point**
- Pole tip on ground marker
- Pole approximately vertical (bubble roughly centered)

**Step 2: Check solution type**
- Verify display shows FIX (not float or single)
- If not fix: Wait, or move to better location

**Step 3: Check fix duration**
- Look for "time since fix" indicator
- If <10 seconds: Wait until ≥10 seconds
- This is quick (10 second wait)

**Step 4: Check satellite indicators**
- Satellite count ≥12 (or ≥10 for canal)
- PDOP ≤2.5 (or ≤3.0 for canal)
- If inadequate: Wait 5-10 minutes (geometry improving), or move location

**Step 5: Check precision estimates**
- Horizontal ≤2cm (or ≤4cm canal)
- Vertical ≤3cm (or ≤6cm canal)
- If inadequate: Check for multipath sources, extend averaging time

**Step 6: Check correction age**
- Age of corrections <3 seconds
- If old: Check base station, radio link

**Step 7: Start averaging measurement**
- Once all gates pass, begin averaging
- Standard: 60 seconds
- Canal: 120 seconds
- Maintain pole vertical (bubble centered) throughout averaging

**Step 8: Monitor during averaging**
- Verify fix maintained (does not revert to float)
- Keep bubble centered
- Watch for precision stability

**Step 9: Save point**
- After averaging completes, verify position looks reasonable
- Enter attributes (point ID, pole height, notes)
- Save to survey layer

**This systematic check takes 15-30 seconds with experience.** It becomes automatic - you glance at the display and see "all green" or "something wrong."

### What to Do If Quality Gates Fail

**Scenario 1: Fix, but satellite count low (8 satellites, need 12)**

**Diagnosis:** Obstructed sky view, or low satellite availability (time of day, location)

**Solutions:**
- Wait 10-20 minutes (satellite geometry changes, more satellites may rise)
- Move 10-20 meters to location with better sky view
- Check satellite visibility forecast (some apps show satellite positions) - survey at better time
- If persistent: Use canal relaxed standards (≥10 satellites) if appropriate for your accuracy requirements

**Scenario 2: Fix, but PDOP high (3.5, need ≤2.5)**

**Diagnosis:** Satellites bunched in one area of sky (poor geometry)

**Solutions:**
- Wait 15-30 minutes (satellites move, geometry improves)
- Check PDOP forecast - survey during time window with better geometry
- If marginal (PDOP 2.5-3.0): May still achieve acceptable precision with longer averaging
- If consistently poor at this site: Consider surveying at different time of day (morning vs afternoon satellite geometry differs)

**Scenario 3: Fix, but precision estimates exceed limits (5cm H, 8cm V, need ≤2/3cm)**

**Diagnosis:** Noisy signals, multipath, or poor satellite geometry despite adequate satellite count

**Solutions:**
- Check for multipath sources: Metal structures, water, vehicles nearby - move away
- Extend averaging time (try 120-180 seconds instead of 60s)
- Improve pole stability (use bipod instead of handheld if available)
- Wait for better satellite conditions
- Verify rover antenna orientation (should be level, not tilted)

**Scenario 4: Stuck in Float (cannot achieve fix)**

**This is the most common and frustrating problem.** See "Troubleshooting No-Fix Situations" section below for detailed diagnosis.

---

## Quality Indicators to Monitor

Understanding all quality indicators helps you make informed decisions and troubleshoot problems.

### Primary Indicators (Check Every Point)

**1. Solution Type (Fix/Float/Single)**
- **Most critical indicator**
- Tells you if ambiguities resolved
- Fix required for surveying
- Displayed prominently in all RTK software

**2. Fix Duration**
- How long fix has been maintained
- ≥10 seconds required for survey points
- Longer = more confidence in stability
- Resets to 0 if fix lost and re-acquired

**3. Satellite Count**
- Number of satellites currently tracked and used in solution
- More is better: ≥12 standard, ≥15 excellent
- Typically 15-25 with modern multi-GNSS receivers in open sky
- <10 satellites: Difficult to achieve/maintain fix

**4. PDOP**
- Position Dilution of Precision
- Geometric quality (how well satellites distributed across sky)
- Lower is better: 1.0-2.0 excellent, 2.0-2.5 good, 2.5-3.0 marginal, >3.0 poor
- Purely geometric - does NOT account for signal quality

**5. Precision Estimates (Horizontal and Vertical)**
- Estimated accuracy of current position
- Based on satellite geometry, signal quality, solution type
- Typical fix values: 0.008-0.020m horizontal, 0.015-0.035m vertical
- Should be ≤0.02m H / 0.03m V for standard survey

**6. Age of Corrections**
- How recently correction data received from base
- Target: <1 second (real-time)
- Acceptable: 1-3 seconds
- Problem: >5 seconds (degraded link)
- Critical: >10 seconds (effectively no corrections)

### Secondary Indicators (Helpful for Diagnosis)

**HDOP (Horizontal Dilution of Precision):**
- Horizontal component of PDOP
- Useful for understanding if position problem is horizontal or vertical
- Typically 0.7-1.5 with good geometry

**VDOP (Vertical Dilution of Precision):**
- Vertical component of PDOP
- Usually higher than HDOP (vertical geometry inherently weaker)
- Typically 1.0-2.5 with good geometry

**Satellite signal strength (SNR - Signal to Noise Ratio):**
- How strong satellite signals are (higher is better)
- Typical: 35-50 dB-Hz for good signals
- <30 dB-Hz: Weak signal (obstruction, low elevation satellite)
- <25 dB-Hz: Very weak (likely not usable)
- Useful for diagnosing multipath or obstruction problems

**Baseline distance:**
- Distance from rover to base station
- Some systems display this
- Optimal: <1 km, Good: 1-5 km, Marginal: 5-10 km, Poor: >10 km

**Satellite sky plot:**
- Visual representation of satellite positions
- Shows which satellites visible and their elevations
- Helps identify obstructions (satellites in certain directions have weak signal)

**RMS (Root Mean Square) residuals:**
- How well measurements fit the calculated position
- Lower is better (typical: <0.01-0.02m)
- High RMS suggests measurement problems (multipath, interference)

### Reading the Quality Dashboard

Modern RTK software displays quality indicators together. Learn to scan this "dashboard" quickly.

**Example SW Maps display (good conditions):**

```
STATUS: RTK FIX               [Green background]
Fix time: 0:03:47
Satellites: 19
PDOP: 1.8
Precision: H=0.014m  V=0.023m
Corrections: 0.8s
Averaging: 45s / 60s
```

**Interpretation (2-3 second scan):**
- FIX + green = ✓ Solution type good
- 3m 47s = ✓ Well beyond 10s requirement
- 19 satellites = ✓ Excellent count
- PDOP 1.8 = ✓ Good geometry
- Precision 1.4cm H, 2.3cm V = ✓ Within limits
- Corrections 0.8s = ✓ Fresh corrections
- Averaging 45/60s = Currently averaging, 15s remaining

**Conclusion: All indicators good, measurement will be reliable**

**Example display (problem conditions):**

```
STATUS: FLOAT                 [Yellow background]
Fix time: --
Satellites: 9
PDOP: 3.7
Precision: H=0.38m  V=0.92m
Corrections: 1.1s
```

**Interpretation:**
- FLOAT + yellow = ✗ Not ready to survey
- No fix time = ✗ Never achieved fix
- 9 satellites = ✗ Below 12 requirement
- PDOP 3.7 = ✗ Poor geometry
- Precision 38cm H, 92cm V = ✗ Way outside limits
- Corrections 1.1s = ✓ Base link OK

**Diagnosis: Low satellite count + poor geometry → cannot resolve ambiguities**

**Action: Wait 10-20 minutes for satellite geometry to improve, or move to location with better sky view**

**With experience, this scan takes 3-5 seconds.** You learn to recognize "good" vs "problem" patterns instantly.

---

## Troubleshooting No-Fix Situations

This is the most common field problem: rover stuck in float, cannot achieve fix.

### Systematic Diagnosis Process

**Step 1: Verify base station operational**

**Check:**
- Is base powered on?
- Has base completed survey-in? (Not still initializing)
- Is base transmitting corrections? (Check base radio indicator lights)

**How to verify:**
- Check "age of corrections" on rover - should be <3 seconds
- If corrections old or missing, problem is base or communication link (not rover)

**Solutions if base problem:**
- Check base power, restart if necessary
- Verify survey-in completed (check base configuration software)
- Check base radio powered and transmitting

**Step 2: Check rover correction reception**

**Check:**
- Age of corrections <3 seconds?
- Satellite count reasonable (≥8 satellites)?
- Rover in RTK rover mode (not base mode, not autonomous)?

**How to verify:**
- Age of corrections indicator in rover software
- Satellite count and signal strength display
- Rover configuration settings

**Solutions if correction problem:**
- Check rover radio powered on, antenna connected
- Verify rover in range of base (check baseline distance if displayed)
- Verify rover configured in correct mode

**Step 3: Assess satellite conditions**

**Check:**
- Satellite count: How many? (Need ≥10-12)
- PDOP: What value? (Need ≤2.5-3.0)
- Sky view: Is it obstructed?

**How to verify:**
- Satellite count and PDOP displayed in rover software
- Visual inspection of sky (trees, buildings blocking satellites?)
- Satellite sky plot if available (shows satellite positions and elevations)

**Solutions if satellite problem:**
- **Low count:** Wait 10-20 minutes (more satellites rise), or move to better location
- **High PDOP:** Wait 15-30 minutes (geometry improves), or survey at different time
- **Obstructed view:** Move 10-20 meters to location with clearer sky

**Step 4: Check for multipath and interference**

**Check:**
- Are you near metal structures, vehicles, chain-link fences?
- Is water nearby (reflects signals)?
- Are there other radios or electronics causing interference?

**How to verify:**
- Visual inspection of surroundings
- Signal strength indicators (weak or fluctuating SNR suggests multipath)
- RMS residuals high (suggests measurement noise)

**Solutions:**
- Move 5-10 meters away from reflective surfaces
- Turn off potential interference sources
- Try different antenna orientation (should be level)

**Step 5: Consider baseline distance**

**Check:**
- How far is rover from base? (If >10 km, this may be the problem)

**How to verify:**
- Baseline distance indicator if displayed
- Measure on map (rover GPS position vs base station position)

**Solutions if baseline too long:**
- Move closer to base station
- Relocate base station closer to survey area
- For very large areas, consider multiple base setups or using CORS network

**Step 6: Wait for ambiguity resolution**

**If all above checks pass but still float:**
- Ambiguity resolution takes time (5-20 minutes for initial fix)
- Be patient - this is not equipment failure
- Rover is mathematically solving for integer ambiguities

**What to do:**
- Keep rover stationary in good location
- Maintain power and correction link
- Wait 10-20 minutes
- Monitor progress (some systems show "convergence" indicators)

**If waiting 30+ minutes with no fix despite good conditions:**
- Power cycle rover (restart gives fresh ambiguity resolution attempt)
- Move to significantly different location (50+ meters)
- Check for equipment malfunction (test with known-good location)

### Common No-Fix Scenarios and Solutions

**Scenario: Just powered on rover, stuck in float**

**Diagnosis:** Normal - initial ambiguity resolution takes time

**Solution:** Wait patiently 5-20 minutes in location with good sky view and correction reception

**Scenario: Had fix, moved to new location, lost fix and cannot re-establish**

**Diagnosis:** New location has obstructed sky view or multipath

**Solution:** Move to more open location, wait 3-10 minutes for fix re-acquisition (faster than initial)

**Scenario: Float all day, never achieved fix**

**Diagnosis:** Fundamental problem - base, rover, or site conditions inadequate

**Solutions:**
- Verify base station survey-in completed successfully
- Check rover configuration (correct mode, correction format)
- Try known-good site (open field, clear sky) to verify equipment working
- Consider equipment malfunction if problem persists

**Scenario: Fix in morning, float in afternoon at same location**

**Diagnosis:** Satellite geometry changed, or ionospheric conditions degraded

**Solution:** Wait for better satellite geometry, or survey at different time of day (morning vs afternoon)

**Scenario: Fix at base station location, float at distant survey points**

**Diagnosis:** Baseline too long (>10 km), or radio link failing at distance

**Solutions:**
- Check age of corrections at distant points (if >5s, radio link problem)
- Reduce baseline by moving base closer
- Use higher-power radio or NTRIP for long baselines

**Scenario: Intermittent fix - achieve fix for 20 seconds, lose for 2 minutes, re-acquire, repeat**

**Diagnosis:** Marginal conditions (barely adequate satellite count/geometry), or intermittent correction reception

**Solutions:**
- Check age of corrections during float periods (if old, radio link is intermittent)
- Move to location with better sky view (more stable satellite count)
- Wait for better satellite geometry (more satellites, better PDOP)
- Extend averaging time and collect points during stable fix periods

### When to Abort Survey and Troubleshoot

**Continue surveying if:**
- Fix achieved and maintained at most survey points
- Occasional loss of fix at specific obstructed locations (expected)
- Fix re-establishes within 5-10 minutes when moving to better locations

**Stop and troubleshoot if:**
- Never achieve fix anywhere (fundamental equipment or configuration problem)
- Fix at start of day but degraded to permanent float (base station problem, equipment malfunction)
- Check points show excessive drift (>3cm H, >4cm V) - indicates survey quality compromised

**Troubleshooting steps when stopping survey:**
- Return to base station, verify operational
- Re-measure check point to verify drift
- Test rover at base station location (should achieve easy fix if equipment working)
- Review base and rover configurations
- Check equipment connections, power, antennas
- Consider equipment swap if spare available

**Do not continue surveying without fix.** Float data is unreliable and will compromise OpenRiverCam transformation accuracy.

---

## Achieving Fix: Realistic Expectations

Understanding typical timelines and conditions helps you plan surveys and recognize normal vs problem situations.

### Initial Fix Acquisition Timeline

**Typical sequence when powering on rover:**

**0:00 - Power on rover, place in good location**
- Clear sky view, away from obstructions
- Base station already operational and transmitting corrections

**0:00-0:30 - Satellite acquisition**
- Rover starts tracking satellites
- Solution: Single (no corrections yet)
- Status display may show "Acquiring..." or low satellite count initially

**0:30-1:00 - Correction reception starts**
- Rover establishes radio link to base
- Starts receiving RTCM3 correction messages
- Solution: Single → Float (corrections applied but ambiguities not resolved)

**1:00-5:00 - Float solution, ambiguity convergence**
- Rover calculating ambiguity candidates
- Position may drift slowly as ambiguity estimates refine
- Solution: Float (improving)

**5:00-20:00 - Ambiguity resolution**
- Rover testing integer ambiguity combinations
- Looking for consistent solution across all satellites
- Solution: Float → attempting Fix

**Typical: 5-20 minutes - Fix achieved**
- Ambiguities successfully resolved
- Solution: **FIX**
- Ready to survey

**This 5-20 minute timeline is NORMAL for initial fix.** It is not equipment malfunction - it is the mathematical process of ambiguity resolution.

**Factors affecting initial fix time:**

**Faster fix (5-10 minutes):**
- Excellent satellite geometry (PDOP <1.5)
- High satellite count (>15 satellites)
- Clean signals (no multipath)
- Short baseline (<1 km)
- Multi-frequency receiver (L1+L2)

**Slower fix (10-20 minutes):**
- Marginal geometry (PDOP 2.0-2.5)
- Moderate satellite count (10-12 satellites)
- Some multipath or interference
- Longer baseline (5-10 km)
- Single-frequency receiver (L1 only)

**Very slow or no fix (>20 minutes):**
- Poor geometry (PDOP >3.0)
- Low satellite count (<10)
- Significant multipath or interference
- Very long baseline (>10 km)
- Equipment or configuration problem

### Re-Establishing Fix After Loss

**If you lose fix during survey (walked under trees, near building), re-acquisition is typically faster than initial.**

**Typical re-acquisition timeline: 2-10 minutes**

**Why faster:**
- Rover maintains ambiguity information from previous fix
- Starting point for new resolution is closer to correct values
- Satellite tracking already established
- Correction link already established

**What to do when fix is lost:**
- Move to location with good sky view
- Verify corrections still being received (age <3 seconds)
- Wait patiently 2-10 minutes
- Rover will typically re-establish fix without intervention

**If re-acquisition takes longer than initial:**
- Satellite conditions may have degraded (fewer satellites, worse geometry)
- Check if time of day changed (different satellite constellation overhead)
- Verify base station still operational

### Maintaining Fix During Survey

**Once fix is established, it can be maintained for hours if conditions remain good.**

**Strategies to maintain fix:**

**Plan survey route for continuous sky view:**
- Survey GCPs in sequence without passing through obstructed areas
- Save heavily-obstructed points for last (accept that re-acquisition will be needed)

**Move efficiently between points:**
- Don't linger under trees or near buildings
- Keep moving to next open location
- Fix maintained during movement if sky view maintained

**Monitor status continuously:**
- Glance at fix status while walking between points
- If fix lost, note what caused it (walked under tree canopy, passed near building)
- Learn which areas are problematic

**Accept that some fix losses are inevitable:**
- Cross-section surveys may require walking along riverbank with vegetation
- Some GCPs may be in challenging locations
- Build re-acquisition time into survey schedule

**Realistic surveying pace:**

**Ideal conditions (open field, maintained fix):**
- 1-2 minutes per point (60s averaging + attribute entry)
- 20-30 points per hour
- Very efficient

**Typical field conditions (occasional fix loss):**
- 3-5 minutes per point (including some re-acquisition time)
- 10-15 points per hour
- Normal pace

**Challenging conditions (frequent fix loss, poor geometry):**
- 5-10 minutes per point (significant re-acquisition time)
- 6-10 points per hour
- Slower but still feasible

**Plan survey schedules accordingly:** For 20 GCP survey in typical conditions, budget 2-3 hours field time (includes setup, check points, measurement, contingency).

### Satellite Geometry Changes Throughout Day

**Satellite positions change continuously (satellites orbit Earth every 12 hours for GPS).**

**This affects fix acquisition and quality:**

**Morning vs afternoon:**
- Different satellites overhead
- Different geometry (PDOP varies)
- Some times of day better than others for your location

**Optimal survey windows:**
- Check PDOP forecast for your location and date
- Plan surveys during low-PDOP windows (typically 4-8 hour windows with PDOP <2.0)
- Avoid high-PDOP periods if possible (some time windows may have PDOP >3.0)

**Multi-GNSS advantage:**
- GPS alone: ~8-12 satellites, PDOP varies significantly through day
- GPS+GLONASS+Galileo: ~18-30 satellites, more consistent PDOP
- Modern multi-GNSS receivers have much less time-of-day dependency

**Practical impact:**
- With multi-GNSS receiver: Can survey any time of day with reasonable reliability
- With GPS-only receiver: May need to plan survey timing more carefully

---

## Connection to Survey Procedures

This section explained RTK fix status in depth. Now you understand:

**When SURVEY_PROCESS.md requires "RTK FIX ≥10 seconds":**
- Fix means ambiguities resolved, centimeter accuracy achieved
- ≥10 seconds ensures stable, reliable fix (not momentary)
- Float is not adequate despite appearing "pretty good"

**When quality gates specify satellites, PDOP, precision:**
- These indicators predict when fix can be achieved and maintained
- They ensure measurement quality, not just fix status
- All must pass together for reliable survey point

**Initial rover setup timeline:**
- 5-20 minutes for first fix is normal (not equipment failure)
- Plan survey schedule to include initialization time
- Be patient during this period

**Troubleshooting no-fix situations:**
- Systematic diagnosis: Base → corrections → satellites → multipath → baseline
- Most common cause: Just need to wait for ambiguity resolution
- Second most common: Inadequate satellite count or geometry

**Section 5.6 next explains post-processing:**
- RINEX data logging during survey
- PPP corrections to improve base station position
- Workflow for applying corrections to survey points

You now understand the most critical field skill for RTK surveying: recognizing and achieving fix status. Chapter 9 provides step-by-step procedures that apply this knowledge.

---

## Summary: Key Concepts

**Fix vs Float - the critical distinction:**
- **Fix:** Ambiguities resolved, 1-3 cm accuracy, READY TO SURVEY
- **Float:** Ambiguities not resolved, 10-100 cm accuracy, NOT ADEQUATE
- **Single:** No corrections, 2-10 meter accuracy, COMPLETELY INADEQUATE

**Why float is inadequate:**
- Precision estimates are deceptive (show good precision relative to wrong reference)
- Position error 20-50 cm typical (vs 1-3 cm for fix)
- Never survey with float - always wait for fix

**Quality gates (all required):**
- Solution type: Fix
- Fix duration: ≥10 seconds
- Satellites: ≥12 (standard) or ≥10 (canal)
- PDOP: ≤2.5 (standard) or ≤3.0 (canal)
- Precision: ≤2cm H / 3cm V (standard) or ≤4cm H / 6cm V (canal)
- Age of corrections: <3 seconds

**Initial fix timeline:**
- Typical: 5-20 minutes (this is normal, not equipment failure)
- Re-acquisition after loss: 2-10 minutes (faster)
- Plan survey schedule with initialization time included

**Troubleshooting no-fix:**
- Check base station operational and transmitting
- Verify correction reception (age <3 seconds)
- Assess satellite count (≥12) and PDOP (≤2.5)
- Check for multipath (metal, water nearby)
- Consider baseline distance (<10 km)
- Wait patiently (ambiguity resolution takes time)

**Quality indicators to monitor:**
- Primary: Solution type, fix duration, satellites, PDOP, precision, correction age
- Secondary: HDOP/VDOP, SNR, baseline distance, satellite sky plot
- Learn to scan "dashboard" quickly (3-5 seconds)

**When to abort survey:**
- Never achieve fix anywhere (equipment/configuration problem)
- Check points show excessive drift (>3cm H, >4cm V)
- Fix lost and cannot re-establish after 30+ minutes

**Realistic expectations:**
- Fix maintained for hours in good conditions
- Occasional loss at obstructed locations is normal
- Survey pace: 10-20 points/hour typical
- Build re-acquisition time into schedule

**Critical rule: Only survey with RTK fix. Float is not adequate no matter how good it appears.**

Understanding fix status is the key skill for RTK surveying. With this knowledge, you can operate confidently in the field and recognize when measurements are reliable.

---

**Next Section:** [5.6 Logging, RINEX, and PPP Corrections](06-logging-rinex-ppp.md)
