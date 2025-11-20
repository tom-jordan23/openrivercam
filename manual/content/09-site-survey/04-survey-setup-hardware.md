# 9.4 Survey Setup - Hardware

This section provides step-by-step procedures for physical setup of your RTK survey equipment in the field. These procedures come directly from SURVEY_PROCESS.md Section 3 (Base Station Setup) with additional context from Chapter 5 concepts.

Proper hardware setup is critical. Shortcuts or mistakes during setup compromise the entire survey. A base station that moves during survey invalidates all measurements. An incorrectly measured antenna height introduces systematic errors in all elevations. Taking time to do setup correctly ensures reliable survey data.

By the end of this section, you will understand:
- Base station site selection criteria and rationale
- Step-by-step base station setup procedure
- Antenna height measurement technique and importance
- Rover equipment assembly and testing
- Radio link verification procedures
- Communication checks before beginning survey
- Quality control during setup

---

## Base Station Site Selection

The base station establishes the reference position for the entire survey. Site selection directly affects survey quality and reliability.

### Site Selection Criteria

**From SURVEY_PROCESS.md Section 3:**

```
Site Selection:
☐ Open sky >15°, >10m from metal/vehicles
☐ Stable ground, accessible for monitoring
☐ For canals: High ground >20m from water
```

Let's understand why each criterion matters.

**Open sky view >15 degrees above horizon:**

**Why this matters (from Section 5.3):**
Base station needs strong satellite signals to:
- Achieve good survey-in accuracy (averaging GPS measurements)
- Track sufficient satellites (need 15+ for reliable survey-in)
- Minimize multipath errors (signals bouncing off obstacles)

**How to verify:**
Stand at potential base station location. Look around 360 degrees. Sky should be visible from 15 degrees above horizon upward in all directions.

**Obstructions to avoid:**
- Trees (especially dense canopy overhead)
- Tall buildings or structures
- Steep valley walls
- Overhanging cliffs

**Acceptable:**
- Sparse trees (some branches, but mostly open sky)
- Distant hills or buildings (at horizon, not overhead)
- Open ground with clear sky above

**If site has marginal sky view:**
- Expect longer survey-in time (may need 60-90 minutes instead of 30-60)
- May achieve fewer satellites (14-16 instead of 18-20)
- Still workable if PDOP remains <1.5 and satellites >15

**>10 meters from metal structures and vehicles:**

**Why this matters (from Section 5.8):**
Metal structures cause multipath errors:
- Satellite signals reflect off metal before reaching antenna
- Receiver sees both direct signal and reflected signal
- Creates positioning errors (can be 10-20 cm or more)

**Problematic metal structures:**
- Vehicles (cars, trucks)
- Metal buildings or sheds
- Large metal fences
- Metal bridges
- Power line towers

**How to verify:**
Measure distance from potential base station location to nearest large metal object. Should be >10 meters.

**If <10 meters is unavoidable:**
- Position base station on opposite side from velocity measurement area
- Use longer survey-in time (60+ minutes to average out multipath)
- Monitor survey-in precision (should achieve 0.25m; if precision worse, consider relocating)

**Stable ground:**

**Why this matters (critical):**
If base station moves during survey (even 1-2 cm), all rover measurements are shifted by that movement. Base station establishes the reference frame - movement invalidates the reference.

**Stable ground characteristics:**
- Rock outcrop (ideal - will not move)
- Compacted soil (acceptable - minimal settlement)
- Concrete or pavement (ideal - stable)

**Unstable ground to avoid:**
- Soft soil (may settle under tripod weight)
- Loose sand or gravel (tripod legs may shift)
- Vegetation mats (can compress unevenly)
- Recently disturbed ground

**Testing stability:**
- Press down on potential location with foot (should not compress)
- Set up tripod and press down firmly on top (tripod should not shift)
- Check tripod after 5-10 minutes (should be in same position)

**Accessible for monitoring:**

**Why this matters (practical):**
You may need to check base station during survey:
- Verify still powered on (battery not depleted)
- Check u-center logs (RINEX logging continuing)
- Troubleshoot if rover loses corrections

**Accessibility balance:**
- Too accessible: Visible from road, risk of public interference
- Too remote: Difficult to check, long walk for troubleshooting
- Optimal: 20-100 meters from survey area, visible with short walk

**For canal environments (special case):**

```
For canals: High ground >20m from water
```

**Why this matters:**
- Canals typically have metal infrastructure (gates, culverts, reinforcement)
- Placing base near canal = multipath from metal + reflection from water
- High ground away from canal reduces these errors

**Canal-specific strategy:**
- Place base station on elevated ground 20-50 meters from canal
- Ensure clear line-of-sight for radio link to rover (rover will be near canal)
- Accept longer baseline (20-50m base to rover typical for canal surveys)

### Practical Site Selection Process

**Upon arriving at survey site:**

1. **Walk the site perimeter** (5-10 minutes)
   - Identify potential base station locations
   - Assess sky view, metal proximity, ground stability
   - Consider accessibility

2. **Select top 2-3 candidate locations**
   - Mark each with survey flag or note GPS position
   - Rank by sky view quality (most important factor)

3. **Choose primary location**
   - Best compromise of all factors
   - Ideally: excellent sky view, >10m from metal, stable rock

4. **Mark location clearly**
   - Place survey flag or marker
   - Record GPS position (waypoint in phone GPS)
   - Photograph location with surroundings (for relocation if needed)

**If primary location proves problematic during setup:**
- Have backup location identified
- Can relocate base station before survey-in completes
- Once survey-in completes, base station cannot be moved

---

## Base Station Setup Procedure

Follow this sequence systematically. Steps are ordered to prevent equipment damage and ensure reliable setup.

### Step 1: Tripod Setup

**Before connecting any electronics:**

1. **Extend tripod legs** to comfortable working height
   - Typical: 1.2-1.5 meters (tripod head at chest height)
   - Consider terrain slope (adjust leg lengths to level tripod)

2. **Position tripod on selected stable ground**
   - Press legs firmly into ground (if soil) or position on flat rock
   - Ensure wide stance (legs spread for stability)

3. **Level tripod head**
   - Use tripod's bubble level (most survey tripods have built-in level)
   - Adjust leg lengths or leg angles until bubble centered
   - Perfectly level not required (antenna orientation not critical for GPS), but level setup is good practice

4. **Test stability**
   - Press down on tripod head firmly (should not shift)
   - Rock tripod gently (should be solid)
   - If unstable: adjust leg positions, press legs deeper, or relocate

5. **Mark exact tripod position**
   - Use marker to trace around tripod feet
   - If tripod shifts during survey, you will notice (feet no longer on marks)
   - This is quality control for base station stability

### Step 2: Antenna Connection (CRITICAL)

**From SURVEY_PROCESS.md:**
```
☐ Connect antenna BEFORE powering base
```

**Why this is critical:**
GPS receivers have sensitive RF (radio frequency) circuits. Powering receiver without antenna connected can damage these circuits. This damage may not be immediately obvious but reduces receiver performance.

**Procedure:**

1. **Verify base station is OFF** (not powered)

2. **Connect antenna cable to receiver**
   - Locate antenna connector on receiver (typically TNC or SMA connector)
   - Align connector pins carefully
   - Screw connector on firmly (hand-tight, not excessively tight)
   - Verify connector is fully seated

3. **Mount antenna on tripod**
   - Attach antenna to tripod mounting bracket or antenna mast
   - Ensure antenna is secure (will not fall or tilt)
   - Position antenna level (GPS antennas should be horizontal)

4. **Route cable neatly**
   - Avoid cable strain on connectors
   - Keep cable away from tripod legs (will not be stepped on)
   - Use cable ties if available

**Never power on base receiver until antenna is connected.**

### Step 3: Power and Verification

**Now safe to power on:**

1. **Connect power source**
   - Battery pack or external power bank
   - Verify polarity correct (if using barrel connector)
   - Ensure connection firm

2. **Power on base station**
   - Press power button or connect power cable (depends on model)
   - Wait 5-10 seconds for boot-up

3. **Verify LEDs indicate normal operation**
   - Power LED should be solid (not flashing or off)
   - Satellite LED should blink (receiving satellite signals)
   - Refer to your receiver's manual for LED patterns

4. **Check battery level**
   - If receiver has battery indicator, verify adequate charge
   - For 6-12 hour survey, need full charge or large external battery

**If receiver does not power on or shows error LEDs:**
- Check power connections
- Verify battery charged
- Check antenna connection
- Consult troubleshooting guide
- Use backup base station if available

### Step 4: Antenna Height Measurement

**From SURVEY_PROCESS.md:**
```
☐ Measure antenna height to ARP (3 measurements)
```

**Why this matters:**
PPP processing requires exact antenna height to calculate accurate position. 1 cm error in antenna height = 1 cm error in elevation for all survey points.

**Antenna Reference Point (ARP):**
GPS antennas have a defined reference point (usually bottom of antenna or specific mark on antenna body). PPP services need to know height from ground to this ARP.

**Measurement procedure:**

1. **Identify ARP on your antenna**
   - Check antenna documentation
   - Typically: bottom of antenna (where it mounts on mast)
   - Sometimes: specific mark or groove on antenna body

2. **Measure from ground to ARP vertically**
   - Use steel tape measure (more accurate than cloth tape)
   - Measure true vertical distance (not slant distance along tripod leg)
   - Hold tape measure taut (no sag)

3. **Record three independent measurements**
   - Measurement 1: ________ m
   - Measurement 2: ________ m
   - Measurement 3: ________ m

4. **Verify measurements agree within 0.5 cm**
   - If measurements differ by >0.5 cm, re-measure carefully
   - Average the three measurements: Height = (M1 + M2 + M3) / 3

5. **Record in field notebook and survey data**
   - You will need this value for PPP submission
   - Include in survey metadata

**Example measurement:**
- Measurement 1: 1.523 m
- Measurement 2: 1.525 m
- Measurement 3: 1.522 m
- Average: 1.523 m
- Agreement: within 0.3 cm (excellent)

**Mark the spot where tripod stands:**
If you need to return for future surveys and place base station at same position, marking enables repeatability.

---

## Base Station Survey-In

**From SURVEY_PROCESS.md:**
```
Survey-In:
☐ 30-60 minute survey-in for 0.25m accuracy
☐ Monitor: PDOP ≤1.5, Satellites ≥15
☐ Record final coordinates in UTM 48S
☐ Start RINEX logging (6-12 hours)
```

**Survey-in establishes the base station's reference position** through averaging GPS measurements over time. This procedure is covered in detail in Section 9.5 (Software Setup) as it requires u-center configuration.

**Hardware monitoring during survey-in:**

**What to watch:**
- Base station remains powered throughout (LED indicators stay on)
- Antenna cable does not get disconnected or damaged
- Tripod does not shift or become unstable
- No one approaches and bumps equipment

**If survey-in fails or interrupted:**
- Must restart survey-in from beginning
- 30-60 minutes lost
- Prevention: careful setup, guard equipment, mark "do not disturb"

**After survey-in completes:**
- Base station position established
- Base station begins broadcasting corrections
- Rover can now achieve RTK FIX
- Base station must remain stable and powered for rest of survey

---

## Rover Equipment Assembly

With base station setup and survey-in initiated (30-60 minutes), you can assemble rover equipment.

### Rover Receiver Preparation

**Procedure:**

1. **Connect rover antenna BEFORE powering receiver**
   - Same critical rule as base station
   - Attach antenna cable firmly to receiver

2. **Mount antenna on survey pole**
   - Secure antenna to pole top using mounting bracket
   - Ensure antenna is stable (will not rotate or fall off)
   - Keep antenna horizontal (GPS antennas work best level)

3. **Attach pole bubble level**
   - Most survey poles have circular bubble level at eye height
   - Verify bubble moves freely (not stuck or broken)
   - This level is critical for keeping pole vertical during measurements

4. **Mark pole height reference**
   - Measure from pole tip (ground contact point) to antenna ARP
   - Mark pole at known intervals (0.5m, 1.0m, 1.5m, 2.0m)
   - You will measure pole height at each survey point

### Rover Power and Connection

1. **Power on rover receiver**
   - Connect battery or power source
   - Verify LEDs indicate normal operation

2. **Connect rover to Android via USB OTG**
   - USB OTG cable from rover to Android device
   - Android should recognize USB device within 10-30 seconds

3. **Start GNSS Master on Android**
   - Should detect rover automatically (if configured correctly in day-before setup)
   - Should show satellite list within 30-60 seconds
   - Should show position (initially Single solution, then Float as base corrections received)

**If GNSS Master does not detect rover:**
- Check USB cable connected firmly at both ends
- Check USB debugging enabled on Android
- Try power-cycling rover
- Try different USB cable
- Refer to troubleshooting procedures from day-before setup

### Pole Assembly with Bipod (Optional)

**Bipod provides stability during measurements:**

1. **Attach bipod to survey pole**
   - Bipod clamps onto pole at comfortable height (hip level typical)
   - Tighten clamp firmly

2. **Extend bipod legs**
   - Adjust to appropriate length for terrain
   - On flat ground: legs extend horizontally
   - On slopes: adjust leg lengths to keep pole vertical

3. **Test stability**
   - Place pole tip on ground
   - Rest bipod legs on ground
   - Press down gently on pole top (should be very stable)

**Bipod benefits:**
- Easier to keep pole vertical (less operator fatigue)
- More stable during averaging period (reduced pole movement)
- Improves measurement accuracy (especially for long averaging times 60-120s)

**Bipod drawbacks:**
- Adds weight to carry
- Slower to reposition between points
- Less mobile in difficult terrain

**Decision:**
Use bipod for precise GCP measurements (where accuracy critical). Optionally skip for cross-section surveys (where speed more important).

---

## Radio Link Verification

**The rover needs corrections from base station to achieve RTK FIX.** Verify radio link is working.

### Radio Communication Check

**If using radio link (not cellular NTRIP):**

1. **Verify base station radio is transmitting**
   - Check radio LED on base station (should be blinking)
   - Radio should transmit RTCM corrections continuously

2. **Verify rover radio is receiving**
   - Check radio LED on rover (should be blinking when receiving)
   - GNSS Master should show "Age of corrections" <3 seconds

3. **Test range**
   - Walk rover to typical survey distance from base (50-200m)
   - Verify corrections still received (age of corrections remains <3s)
   - If corrections lost: reposition base radio antenna higher, or move base closer

**Common radio problems:**
- Radio antennas not connected (check connections)
- Radio powered off or in wrong mode (check settings)
- Radio frequency mismatch between base and rover (verify both on same frequency)
- Obstacle blocking line-of-sight (reposition for clearer path)

**Radio range expectations:**
- Line-of-sight: 1-5 km typical
- Obstructed (trees, buildings): 0.5-2 km typical
- For OpenRiverCam surveys (base to survey area usually <500m): range rarely limiting factor

### Cellular NTRIP Connection (if applicable)

**If using cellular connection instead of radio:**

1. **Verify Android has cellular data connection**
   - Mobile data enabled
   - Sufficient signal strength at site

2. **Configure rover for NTRIP**
   - NTRIP server address (may be base station broadcasting via cellular)
   - Authentication credentials
   - Verify connection in GNSS Master or rover configuration

3. **Verify corrections received**
   - GNSS Master shows age of corrections <3 seconds
   - Solution type changes from Single to Float (indicates corrections received)

**NTRIP advantage:**
Unlimited range (works anywhere with cellular coverage).

**NTRIP disadvantage:**
Requires cellular data plan and coverage at site.

---

## Communication Check

**Before beginning survey, verify all systems working together.**

### System Integration Verification

**With base station survey-in completed, rover assembled, and radio link verified:**

1. **Rover should achieve RTK FIX**
   - After 5-20 minutes, solution type should change to FIX
   - If stuck in Float >20 minutes, troubleshoot (check sky view, satellite count, PDOP)

2. **SW Maps should show position**
   - Open SW Maps project
   - GPS indicator should show current position
   - Should update smoothly as you move rover

3. **Quality indicators should show good values**
   - Satellites ≥12 (ideally 15-20)
   - PDOP ≤2.5
   - Horizontal precision ≤2cm, Vertical precision ≤3cm
   - Age of corrections <3 seconds

**If all indicators good:**
System is ready to begin surveying. Proceed to establish check points.

**If any indicators poor:**
Troubleshoot before beginning survey:
- Single or Float solution: Check base station, radio link, sky view, wait longer
- Low satellites (<10): Check sky obstructions, antenna connection, wait for satellites to rise
- High PDOP (>3.0): Poor satellite geometry, wait 10-20 minutes for geometry to improve
- Poor precision (>5cm): Check multipath (move away from reflective surfaces), extend averaging time
- Old corrections (>3s): Check base station operating, check radio link

**Do not begin surveying until rover achieves FIX with good quality indicators.**

### Team Communication Establishment

**If two-person team with primary operator (rover) and secondary operator (base monitoring):**

1. **Test communication method**
   - Mobile phones (if signal available)
   - Two-way radios (if no mobile signal)
   - Visual signals (if line-of-sight)

2. **Establish check-in schedule**
   - Example: "Return to base every 2 hours to verify base station status"
   - Example: "Radio check every hour"

3. **Define emergency signals**
   - How to communicate if problem occurs
   - Where to meet if separated

**If solo operator:**
- Plan to check base station periodically (every 1-2 hours)
- Route survey to pass near base station regularly
- Carry mobile phone for emergency (even if no signal, may find signal if needed)

---

## Quality Control During Setup

**Setup quality determines survey quality.** Verify these before beginning measurements:

### Base Station Quality Checks

- [ ] Base station positioned on stable ground (not moving)
- [ ] Tripod level and stable (tested by pressing firmly)
- [ ] Antenna connected before power on (correct sequence followed)
- [ ] Antenna cable secure (not loose or disconnected)
- [ ] Antenna height measured 3 times, averaged, recorded
- [ ] Survey-in completed successfully (PDOP ≤1.5, Satellites ≥15)
- [ ] Base station broadcasting corrections (rover receiving, age <3s)
- [ ] RINEX logging started (will run 6-12 hours)
- [ ] Battery level adequate (will last entire survey session)

### Rover Quality Checks

- [ ] Rover antenna connected before power on (correct sequence)
- [ ] Antenna mounted securely on survey pole
- [ ] Pole bubble level working (bubble moves, not stuck)
- [ ] Pole height marked clearly (reference marks visible)
- [ ] USB connection to Android working (GNSS Master receiving data)
- [ ] SW Maps project configured (correct EPSG code, layers created)
- [ ] RTK FIX achieved (not stuck in Float or Single)
- [ ] Quality indicators good (satellites ≥12, PDOP ≤2.5, precision ≤2cm H / 3cm V)
- [ ] Age of corrections <3 seconds (radio link working)

### Team Readiness Checks

- [ ] Roles assigned (who runs rover, who monitors base if two-person team)
- [ ] Communication method tested (phones, radios, visual signals)
- [ ] Field notebook and documentation materials ready
- [ ] Marking supplies available (paint, stakes, flags)
- [ ] Water and sun protection for team (heat management)
- [ ] First aid kit accessible (safety preparation)
- [ ] Estimated survey duration discussed (when expect to finish)

**If all checks pass:**
Begin survey with check point establishment (covered in Section 9.6).

**If any checks fail:**
Troubleshoot and resolve before beginning survey. Poor setup leads to poor data.

---

## Troubleshooting Common Setup Problems

### Problem: Base station will not achieve good survey-in (PDOP >2.0, satellites <12)

**Diagnosis:** Poor sky view or multipath interference

**Solutions:**
- Relocate base station to better sky view location
- Move away from metal structures or trees
- Wait longer (satellite geometry improves as satellites move)
- Accept longer survey-in time (60-90 minutes instead of 30-60)

### Problem: Rover will not achieve RTK FIX (stuck in Float for >30 minutes)

**Diagnosis:** Insufficient corrections, poor sky view, or poor satellite geometry

**Solutions:**
- Verify rover receiving corrections (age <3s; if not, check base station and radio link)
- Check rover sky view (move to more open location)
- Check satellite count (need ≥10; wait if count low)
- Check PDOP (need ≤3.0; wait 10-20 min if PDOP high)
- Move away from reflective surfaces (metal, water edge) by 5-10 meters
- Wait longer (fix can take 20-30 minutes in challenging conditions)

### Problem: GNSS Master not receiving data from rover

**Diagnosis:** USB connection or configuration issue

**Solutions:**
- Check USB cable connected firmly at both ends
- Try different USB cable (must support data, not just charging)
- Verify USB debugging enabled on Android (Settings → Developer Options)
- Power cycle rover and Android
- Check rover output mode (should be NMEA on USB port)
- Review day-before integration test procedure

### Problem: Tripod or base station becomes unstable during setup

**Diagnosis:** Soft ground or poor tripod positioning

**Solutions:**
- Relocate to more stable ground (rock, compacted soil, pavement)
- Press tripod legs deeper into ground
- Widen tripod leg stance (increase stability)
- Place flat rocks or boards under tripod feet (prevent sinking)
- If relocating: must restart survey-in (cannot move during survey-in)

### Problem: Radio link does not work (corrections not received)

**Diagnosis:** Radio configuration, antenna, or range issue

**Solutions:**
- Verify radio antennas connected at base and rover
- Check radio power (LEDs indicate radio operating)
- Verify radio frequencies match between base and rover
- Reposition radio antennas for better line-of-sight
- Move rover closer to base (reduce range)
- Check radio configuration (baud rate, protocol)

**When to abort setup and reschedule:**
- Base station site has fundamentally inadequate sky view (PDOP >2.5 throughout survey-in)
- Equipment failure that cannot be fixed (receiver malfunction, broken antenna)
- Weather deteriorates to unsafe conditions (thunderstorm approaching)
- Critical equipment missing or forgotten (spare batteries, required cables)

**Better to abort and return with proper conditions/equipment than to collect poor data.**

---

## Summary: Hardware Setup Checklist

**Base station setup:**
1. Select site (open sky >15°, >10m from metal, stable ground)
2. Setup tripod (level, stable, mark position)
3. Connect antenna BEFORE powering on
4. Power on, verify LEDs indicate normal operation
5. Measure antenna height (3 measurements, average, record)
6. Start survey-in (30-60 min, monitor PDOP ≤1.5, Satellites ≥15)
7. Record base coordinates when survey-in completes
8. Start RINEX logging (6-12 hours)
9. Verify base broadcasting corrections

**Rover setup:**
1. Connect antenna BEFORE powering on
2. Mount antenna on survey pole with bubble level
3. Mark pole height references
4. Power on rover
5. Connect rover to Android via USB OTG
6. Start GNSS Master (verify rover detected)
7. Open SW Maps project
8. Verify rover receives corrections (age <3s)
9. Wait for RTK FIX (5-20 minutes typical)
10. Verify quality indicators good (satellites ≥12, PDOP ≤2.5, precision ≤2cm H / 3cm V)

**System verification:**
- Base station stable and broadcasting
- Rover achieving FIX with good quality indicators
- SW Maps displaying position and ready to collect data
- Radio link working (corrections received, age <3s)
- Team communication established
- All quality checks passed

**Time required:**
- Base station setup: 15-30 minutes
- Survey-in: 30-60 minutes
- Rover setup: 10-15 minutes
- FIX acquisition: 5-20 minutes
- Total: 60-125 minutes from arrival to ready-to-survey

**The investment in careful hardware setup ensures:**
- Reliable base station reference throughout survey
- Consistent RTK fix for accurate measurements
- No equipment failures during survey
- High-quality data suitable for transformation

With hardware setup complete and verified, you are ready for software configuration and survey execution (Sections 9.5 and 9.6).

---

**Next Section:** [9.5 Survey Setup - Software](05-survey-setup-software.md)
