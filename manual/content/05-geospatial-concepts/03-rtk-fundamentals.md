# 5.3 RTK Fundamentals

This is the critical technical foundation for understanding OpenRiverCam survey work. If you only read one section in Chapter 5 carefully, make it this one.

RTK (Real-Time Kinematic) positioning is what enables centimeter-level accuracy for your surveys. It sounds complex and technical - and the mathematics behind it certainly is - but the core concepts are understandable with the right analogies and explanations.

By the end of this section, you will understand:
- What RTK actually is and why it achieves centimeter accuracy
- The role of base station and rover in the RTK system
- How real-time corrections work
- What RTK "fix" status means and why it matters critically
- The difference between "fix" and "float" solutions
- What quality indicators tell you about measurement reliability
- Realistic accuracy expectations for field conditions
- Why RTK revolutionized surveying accessibility

This section builds the mental model you need to operate RTK equipment confidently and troubleshoot problems in the field. Chapter 9 (Site Survey) will provide the step-by-step procedures, but this section gives you the "why" behind every procedure.

---

## Starting with What You Know: Your Smartphone GPS

Let's build from the familiar to the precise.

### How Your Phone Finds Your Location

Open a map application on your smartphone. Within a few seconds, a blue dot appears showing your location. This seems like magic, but here is what happens:

**Your phone's GPS chip:**
1. Receives signals from 4-10 satellites overhead
2. Measures how long each signal took to arrive
3. Calculates distances to those satellites (travel time × speed of light)
4. Determines where you must be for those distances to make sense
5. Shows your position on the map

**How accurate is it?**
- Clear outdoors: 5-10 meters (within a half-block)
- Near buildings: 10-20 meters (might show you on wrong side of street)
- Indoors: 20-100 meters or fails completely

**This is good enough for:**
- Finding a restaurant
- Getting driving directions
- Geotagging photos

**This is not good enough for:**
- Property boundaries (you would be 5 meters into your neighbor's land)
- Construction layout (your wall would be 10 meters off)
- **Ground control points for OpenRiverCam (you need 50-500 times better accuracy)**

### Why Phone GPS is Not More Accurate

Think of it like measuring the length of a table with a clock.

You know the table is somewhere around 2 meters long. You ask a friend to walk from one end to the other at exactly 1 meter per second. You time them: "4.2 seconds."

**You calculate:** 4.2 seconds × 1 meter/second = 4.2 meters

**But you know the table is only 2 meters!** What went wrong?

**Possible errors:**
- Your friend walked slower than 1 m/s (speed error)
- Your clock was running slow (timing error)
- Your friend took a curved path (signal path error)
- You started timing late (synchronization error)
- Your friend paused briefly to step over something (delay error)

**This is exactly what happens with GPS:**
- Satellites' clock not perfectly synchronized (timing error)
- Signal slows down in atmosphere (atmospheric delay)
- Signal bounces off building before reaching your phone (multipath)
- Your phone's clock is not perfectly accurate (receiver clock error)
- Satellite's position not perfectly known (orbital error)

Each error is small - milliseconds or nanoseconds - but when you multiply by the speed of light (300,000 kilometers per second), tiny timing errors become large position errors.

**1 nanosecond timing error = 30 centimeters position error**

Your phone's GPS has timing uncertainty of roughly 10-30 nanoseconds = 3-10 meters position uncertainty.

**RTK solves these errors in a clever way.**

---

## The RTK Solution: Using Two Receivers Together

Here is the key insight that makes RTK work:

**If two GPS receivers are near each other (within 10 kilometers), they see almost exactly the same errors.**

Both receivers are looking at the same satellites through the same atmosphere at nearly the same time. So atmospheric delays, satellite orbit errors, and satellite clock errors affect both receivers almost identically.

**RTK uses this fact to cancel out the errors.**

### The Two-Receiver System

RTK requires two GPS receivers working as a team:

**1. Base Station (stationary)**
- Sits in one fixed location throughout your survey
- Records GPS measurements continuously
- Knows (or measures) its exact position
- Calculates corrections by comparing what it measures to what it should measure
- Broadcasts corrections to rover in real-time

**2. Rover (mobile)**
- The GPS receiver you carry to survey points
- Receives normal GPS signals from satellites
- Also receives correction data from base station
- Applies corrections to its own measurements
- Calculates precise position relative to base station

**Think of it like this analogy:**

Imagine you are measuring the distance between two markers using a rubber measuring tape. The tape is old and stretches unpredictably - sometimes it reads 10.3 meters, sometimes 10.8 meters for the same distance.

**Standard GPS approach:** Just use the tape and accept the uncertainty (maybe 10.5 meters ± 0.5 meters).

**RTK approach:**
- Place the tape between two other known markers exactly 5.000 meters apart (this is your "base station")
- The tape reads "5.43 meters" - you now know the tape is reading 0.43 meters too long right now
- Quickly measure your unknown distance - tape reads "10.73 meters"
- Subtract the error: 10.73 - 0.43 = 10.30 meters (much more accurate!)
- Keep monitoring the known distance and updating the correction factor

**The key:** The tape stretches the same way for both measurements (because they are taken at the same time). So if you know the error at one place, you can correct for it at another nearby place.

**RTK does exactly this with GPS signals.**

[VISUAL PLACEHOLDER: Two-panel illustration. Left panel labeled "Standard GPS" shows single receiver with signals from satellites above, multiple possible positions shown as scattered dots in 5-meter radius circle. Right panel labeled "RTK GPS" shows base station (left, on tripod) and rover (right, on survey pole) both receiving satellite signals, with correction data stream from base to rover (radio waves icon). Rover position shown as tight cluster of dots in 2-cm circle. Caption: "RTK precision: base station measures errors, rover applies corrections."]

---

## How RTK Achieves Centimeter Accuracy: Carrier Phase Tracking

The explanation above describes the basic concept of differential correction. But standard differential GPS (DGPS) only achieves 0.5-2 meter accuracy. How does RTK get to 1-3 centimeters?

**RTK uses a more sophisticated measurement: carrier phase tracking.**

### Understanding Carrier Phase (With an Analogy)

Imagine you are trying to measure distance using ocean waves.

**Simple approach (like basic GPS):**
- Count how many waves arrived in 1 minute
- You count 30 waves
- You know waves are traveling at 10 meters/second
- You know wave frequency is 0.5 waves/second (one wave every 2 seconds)
- Distance = (waves per second) × (time) × (wave speed) = approximately 600 meters

**Precision:** Limited by how accurately you can count waves (maybe ±1 wave = ±20 meters uncertainty).

**Sophisticated approach (like RTK):**
- Measure not just how many complete waves, but precisely where you are in the current wave
- "I have received 30 complete waves, plus I am currently 0.73 of the way through the 31st wave"
- Now distance = 600 meters + (0.73 × 2 meters) = 601.46 meters

**Precision:** Limited by how accurately you can measure your position within a wave (maybe ±0.01 of a wavelength = ±0.02 meters = 2 cm).

**This is carrier phase tracking.**

GPS signals are radio waves with very short wavelength (about 19 centimeters for L1 frequency). If you can measure your position within that wave very precisely - not just count waves, but determine "I am 0.735 of the way through this particular wave cycle" - you get centimeter-level precision.

**The challenge:** You do not know which wave you are measuring. You might be 0.735 of the way through wave number 1,000,000 or wave number 1,000,001. This is called the "ambiguity" problem.

**RTK solves this by:**
1. **Using two receivers** (base and rover) that both track the same satellites
2. **Comparing carrier phase measurements** between base and rover
3. **Solving for the integer ambiguities** (figuring out which wave cycle you are in)
4. **Once ambiguities are resolved** → You achieve centimeter accuracy (this is "RTK FIX" status)
5. **If ambiguities cannot be resolved** → You get meter-level accuracy (this is "FLOAT" status)

You do not need to understand the mathematics. You need to understand:
- **RTK FIX = ambiguities resolved = centimeter accuracy = ready to survey**
- **RTK FLOAT = ambiguities not resolved = meter accuracy = not ready to survey**

---

## RTK Fix Status: The Most Important Concept

This is the critical concept for field surveying. **Everything depends on understanding RTK fix status.**

### The Three Position Solution Types

Your RTK rover can be in one of three states:

**1. Single (or Autonomous)**
- Using satellite signals alone, no corrections
- Accuracy: 2-10 meters (like your phone GPS)
- **Status:** Not suitable for surveying
- **What to do:** Wait for base station connection

**2. Float**
- Receiving corrections from base station
- But carrier phase ambiguities not resolved
- Accuracy: 0.1-1 meter (much better than single, but still not adequate)
- **Status:** Not ready for surveying yet
- **What to do:** Wait for fix, ensure good satellite conditions

**3. Fix (or Fixed)**
- Receiving corrections from base station
- Carrier phase ambiguities successfully resolved
- Accuracy: 1-3 centimeters (suitable for surveying)
- **Status:** READY TO SURVEY - this is what you need!
- **What to do:** Collect measurements quickly while fix is maintained

**Think of it like focusing a camera:**

- **Single:** Camera is not even turned on - blurry smudge
- **Float:** Camera is on and trying to focus - you can see the subject but it is not sharp
- **Fix:** Camera achieved perfect focus - crystal clear, ready to take the photo

**For surveying GCPs: You must have RTK FIX. Float is not adequate. Single is completely inadequate.**

### How Your Equipment Shows Fix Status

Different systems display fix status differently:

**SW Maps (the data collection app used in SURVEY_PROCESS.md):**
- Displays "RTK FIX" or "RTK FLOAT" or "SINGLE" in status bar
- Color coding: Green = Fix, Yellow = Float, Red/Gray = Single
- Shows time since fix acquired ("Fix 0:00:35" = fix for 35 seconds)

**GNSS Master (Android mock location app):**
- Shows solution status in main window
- Quality indicator: 4 = fix, 5 = float, 1 = single

**Other data collectors:**
- Some show "Fixed," "Float," "Autonomous"
- Some use color indicators
- Some show numeric quality codes

**The critical requirement from SURVEY_PROCESS.md:**
- **RTK FIX maintained for ≥10 seconds before saving point**
- This ensures ambiguities are definitely resolved and stable

### What Determines If You Get Fix or Float?

RTK fix depends on several factors:

**1. Satellite geometry (PDOP value)**
- Need satellites distributed across the sky (not all clustered)
- **Good:** Satellites spread north, south, east, west, overhead (PDOP < 2.5)
- **Poor:** Satellites all bunched in one area (PDOP > 3.0)
- PDOP = Position Dilution of Precision (lower is better)

**Think of it like this:** If you are triangulating your position using landmarks, you want landmarks spread all around you, not all in the same direction. Same principle.

**2. Number of satellites**
- More satellites = more measurements = easier to resolve ambiguities
- **Good:** 12-20 satellites tracked (typical in open sky)
- **Adequate:** 10-12 satellites
- **Poor:** < 10 satellites (fix difficult or impossible)

**3. Signal quality**
- Clean, strong signals from satellites
- **Good:** Open sky, no obstructions above 15 degrees
- **Poor:** Trees, buildings blocking portions of sky

**4. Distance from base to rover**
- Errors become less correlated as distance increases
- **Optimal:** < 1 km from base to rover
- **Good:** 1-5 km
- **Challenging:** 5-10 km
- **Generally difficult:** > 10 km

For OpenRiverCam surveys where rover is typically 50-500 meters from base, this is not a limiting factor.

**5. Ionospheric conditions**
- Earth's atmosphere affects GPS signals
- Varies by time of day, season, solar activity
- **Generally better:** Late afternoon/evening, winter, solar minimum
- **More challenging:** Midday, summer, solar maximum (high solar activity)

You cannot control this factor, but being aware helps explain why some days are easier than others.

**6. Multipath and interference**
- Signals bouncing off metal or water confuse receiver
- Keep rover away from large metal structures, vehicles, reflective surfaces

### Practical Reality: Achieving and Maintaining Fix

**Typical timeline when starting rover:**

- **0:00 - Power on rover**
- **0:00-0:30 - Acquiring satellites** (solution: Single)
- **0:30-1:00 - Receiving base corrections** (solution: Float)
- **1:00-5:00 - Calculating ambiguities** (solution: Float → attempts to resolve)
- **5:00+ - Ambiguities resolved** (solution: **FIX** - ready to survey!)

**This 5-20 minute initialization is normal.** Be patient. It is not equipment failure, it is the mathematical process of resolving ambiguities.

**Once you have fix, you can survey very efficiently:**
- Move to GCP location (fix typically maintained if sky view OK)
- Wait 10-60 seconds averaging
- Save point
- Move to next GCP (fix usually maintained)
- Repeat

**You can survey 10-20 points per hour once fix is established.**

**If you lose fix:**
- Happens when walking under trees, near buildings, etc.
- Solution reverts to Float
- Must re-establish fix (typically 2-5 minutes, faster than initial acquisition)

**Strategy:** Plan survey route to minimize losing fix. Survey GCPs in sequence without passing through obstructed areas.

[VISUAL PLACEHOLDER: Flowchart showing RTK status progression. Start: "Power on rover" → "Acquiring satellites (2-5 min)" → "Float solution (2-10 min)" → "Attempting fix" → Diamond decision "Good satellite geometry + signal quality?" → If No, loop back to Float, if Yes → "FIX achieved" (large green checkmark) → "Survey GCP" → Decision diamond "Moving to next GCP" → "Sky view maintained?" → If Yes, return to "Survey GCP", if No → back to Float. Timing annotations on each stage.]

---

## The Base Station Role: Reference and Correction Source

Understanding the base station's role helps you set it up correctly and troubleshoot problems.

### What the Base Station Does

**Core functions:**

**1. Establishes reference position**

The base station determines its own position very accurately through a process called "survey-in":
- Measures GPS signals continuously for 30-60 minutes
- Averages thousands of measurements
- Calculates position with ~25 cm accuracy (without external corrections)
- Stores this position as its reference for the entire survey session

**From SURVEY_PROCESS.md:**
- 30-60 minute survey-in for 0.25m accuracy
- Required: PDOP ≤ 1.5, Satellites ≥ 15

**Think of survey-in like this:** Imagine you are standing on a street corner, and 100 different people give you directions using GPS on their phones. Each person's GPS is off by a few meters in random directions. But if you average all 100 directions, the random errors cancel out and you get a pretty accurate location.

**That is survey-in.** The base station averages out random GPS errors over time to determine its position accurately.

**2. Generates correction data**

Once the base knows its position, it continuously:
- Measures GPS signals from all visible satellites
- Compares measured position to its known position
- Calculates correction factors for each satellite
- Packages corrections into RTCM3 messages (standard correction format)

**Example:** Base station's known position is (100.000m, 200.000m, 150.000m). Right now, based on GPS signals, it calculates position as (100.237m, 200.189m, 149.845m).

**Corrections:** East +0.237m, North +0.189m, Up -0.155m

These corrections are satellite-specific and change every second.

**3. Transmits corrections to rover**

Corrections are broadcast via:
- **Radio link:** Most common, 1-10 km range, license-free frequencies
- **Cellular connection:** Unlimited range, requires cell coverage (NTRIP protocol)
- **Direct cable:** Only practical for very short range

Rover receives these corrections in real-time and applies them to its own measurements.

### Why Base Station Position Accuracy Matters (and Doesn't)

This is important to understand:

**Base station absolute position accuracy:**
- Survey-in: ~25 cm accuracy
- With PPP post-processing: ~2-10 cm accuracy

**Rover relative accuracy to base:**
- With RTK fix: 1-3 cm

**What this means:**
- **Relative accuracy** (between surveyed points) is excellent: 1-3 cm
- **Absolute accuracy** (true geographic position) is moderate: 25 cm initially

**For OpenRiverCam transformation, relative accuracy matters most.** The GCPs need to be accurate relative to each other. Their absolute geographic position is less critical for the camera transformation to work.

**However, absolute accuracy matters for:**
- Integrating with maps or satellite imagery
- Comparing to other surveys or data
- Hydrologic modeling or engineering design

**Solution:** PPP post-processing (Section 5.6) improves base station position to 2-10 cm absolute accuracy. You survey with 25 cm absolute accuracy, then correct all your points later in the office.

**Key takeaway:** Do not worry that your base station is "only" 25 cm accurate. Your GCPs will be 1-3 cm accurate relative to each other, which is what matters for transformation. PPP can improve absolute accuracy later if needed.

### Base Station Setup Requirements

**From SURVEY_PROCESS.md, these requirements make sense now:**

**Site selection:**
- **Open sky >15° above horizon** → Need satellites for survey-in and corrections
- **>10m from metal/vehicles** → Avoid multipath errors in base measurements
- **Stable ground** → Base cannot move during survey (any movement invalidates corrections)

**Survey-in requirements:**
- **30-60 minute duration** → Longer = better average = better reference position
- **PDOP ≤ 1.5** → Good satellite geometry required
- **Satellites ≥ 15** → More satellites = better averaging

**Antenna height measurement:**
- Measure from ground to antenna reference point (ARP)
- Needed for PPP post-processing
- Three measurements averaged for accuracy

**Why measure antenna height?** PPP services need to know exactly where the antenna phase center was to calculate corrections. Height error of 1 cm = vertical position error of 1 cm for all your survey points.

---

## The Rover Role: Mobile Measurement Station

The rover is what you carry to each survey point. Understanding its operation helps you collect good data.

### What the Rover Does

**1. Receives satellite signals**
- Tracks same satellites as base station
- Measures carrier phase and pseudorange
- Maintains continuous tracking while moving (if possible)

**2. Receives correction data from base**
- Via radio or cellular link
- Processes RTCM3 correction messages
- Must receive corrections at least once per second for good performance

**3. Calculates precise position**
- Applies corrections to its measurements
- Attempts to resolve carrier phase ambiguities
- Calculates position relative to base station
- Updates solution type: Single → Float → Fix

**4. Outputs position to data collector**
- Sends position data to smartphone/tablet via USB or Bluetooth
- Typically NMEA format (standard GPS sentence format)
- Data collector (SW Maps) displays position and allows saving

### Rover Measurement Procedure

**From SURVEY_PROCESS.md quality gates:**

**Standard points:**
- RTK FIX ≥ 10 seconds
- PDOP ≤ 2.5
- Satellites ≥ 12
- Precision ≤ 2cm horizontal / 3cm vertical
- Averaging time: 60 seconds

**Why each requirement?**

**RTK FIX ≥ 10 seconds:**
- Ensures ambiguities definitely resolved (not just momentary false fix)
- Confirms solution stability
- Reduces risk of saving a Float solution by mistake

**PDOP ≤ 2.5:**
- Ensures good satellite geometry
- Lower PDOP = satellites well-distributed across sky
- Poor geometry degrades accuracy even with fix

**Satellites ≥ 12:**
- More satellites = better ambiguity resolution
- Redundancy for reliability
- Typical with good sky view

**Precision ≤ 2cm horizontal / 3cm vertical:**
- Estimated accuracy based on signal quality and geometry
- Confirms measurement quality meets requirements
- Vertical typically less accurate than horizontal (normal for GNSS)

**Averaging time: 60 seconds:**
- Reduces random noise in measurements
- Averages out small variations
- Provides more stable position estimate
- Longer averaging for challenging conditions (120s for canals)

**These requirements are not arbitrary - each ensures measurement quality.**

### Rover Hardware: Antenna and Pole

**Antenna:**
- Must maintain clean satellite signal reception
- Keep antenna level and stable during measurement
- Do not block antenna with your body (stand to the side)

**Survey pole:**
- Rover antenna mounted on pole
- Pole has circular level bubble - must be centered
- Pole height measured with tape measure for each point

**Why measure pole height?**
- Rover measures position of antenna (top of pole)
- You need position of ground point (bottom of pole)
- Calculate: Ground point elevation = Antenna elevation - Pole height

**Example:**
- Rover measures antenna at 152.347m elevation
- Pole height is 2.150m
- GCP ground point elevation = 152.347 - 2.150 = 150.197m

**Accuracy requirement:** Measure pole height to 0.5 cm (half-centimeter). If you are achieving 2 cm GPS accuracy, 0.5 cm pole height measurement error is acceptable.

[VISUAL PLACEHOLDER: Diagram of rover setup. Survey pole (vertical, 2m tall) with height measurement tape shown. Rover antenna mounted on top. Circular bubble level shown at eye height (magnified inset shows bubble centered). Pole tip at ground marking GCP. Annotations: "Antenna (receiver measures position here)", "Pole height = 2.150m (measure carefully)", "Bubble level - keep centered", "GCP ground point (calculate position by subtracting pole height)". Surveyor figure shown standing to side, not blocking antenna.]

---

## Quality Indicators: Reading the Dashboard

Your RTK system provides continuous quality feedback. Learning to read these indicators is critical for successful surveying.

### The Key Indicators You Monitor

**1. Solution Type (Fix / Float / Single)**
- **Most important indicator**
- Fix = green light, proceed with survey
- Float or Single = wait, do not save points

**2. Satellites Tracked**
- Number of satellites currently tracked
- **Goal:** ≥ 12 satellites for standard survey
- More satellites = better reliability

**3. PDOP (Position Dilution of Precision)**
- Geometric quality of satellite distribution
- **Goal:** ≤ 2.5 for standard survey, ≤ 3.0 acceptable for canals
- Lower is better: 1.0 = excellent, 2.0 = good, 3.0 = marginal, 4.0+ = poor

**4. Precision Estimates (Horizontal / Vertical)**
- Estimated accuracy of current position
- **Goal:** ≤ 2cm horizontal, ≤ 3cm vertical for standard points
- Based on signal quality, satellite geometry, fix status

**5. Time Since Fix**
- How long fix has been maintained
- **Goal:** ≥ 10 seconds before saving standard points
- Longer = more confidence in fix stability

**6. Age of Corrections**
- How recently corrections were received from base
- **Goal:** < 3 seconds (ideally < 1 second)
- Old corrections = poor/lost base connection

### What Good Conditions Look Like

**Example display in SW Maps:**
```
Status: RTK FIX
Fix duration: 0:02:35
Satellites: 18
PDOP: 1.8
Precision: H=0.014m V=0.021m
Age of corrections: 0.7s
```

**Interpretation:**
- Fix = ✓ Ready to survey
- Fix for 2 minutes 35 seconds = ✓ Very stable
- 18 satellites = ✓ Excellent satellite count
- PDOP 1.8 = ✓ Good geometry
- Horizontal precision 1.4cm, vertical 2.1cm = ✓ Well within requirements
- Corrections 0.7 seconds old = ✓ Good base link

**Action: PROCEED WITH MEASUREMENT**

### What Problem Conditions Look Like

**Example display:**
```
Status: FLOAT
Fix duration: --
Satellites: 8
PDOP: 4.2
Precision: H=0.35m V=0.68m
Age of corrections: 1.2s
```

**Interpretation:**
- Float = ✗ NOT ready to survey
- No fix = ✗ Ambiguities not resolved
- 8 satellites = ✗ Below minimum requirement
- PDOP 4.2 = ✗ Poor geometry (satellites bunched)
- Precision 35cm horizontal = ✗ Not adequate (need < 2cm)
- Corrections OK = ✓ Base link working

**Diagnosis: Low satellite count + poor geometry → cannot achieve fix**

**Action: WAIT 5-10 minutes for satellite geometry to improve, or move to location with better sky view**

### Decision Tree for Survey Measurements

**Before saving any survey point, check:**

1. **Solution Type = Fix?**
   - No → WAIT, do not survey
   - Yes → Continue checking

2. **Fix duration ≥ 10 seconds?**
   - No → WAIT longer
   - Yes → Continue checking

3. **Satellites ≥ 12?** (or ≥10 for canal relaxed standards)
   - No → WAIT or move to better location
   - Yes → Continue checking

4. **PDOP ≤ 2.5?** (or ≤3.0 for canal)
   - No → WAIT or move to better location
   - Yes → Continue checking

5. **Precision ≤ 2cm H / 3cm V?** (or ≤4cm H / 6cm V for canal)
   - No → Extend averaging time or move location
   - Yes → Continue checking

6. **Age of corrections < 3 seconds?**
   - No → Check base station, radio link
   - Yes → ALL CHECKS PASSED

**ALL CHECKS PASSED → SAVE SURVEY POINT**

**This seems tedious, but with experience you scan the display quickly (2-3 seconds) and see "all green" or "something wrong."**

[VISUAL PLACEHOLDER: Visual decision flowchart with traffic light colors. Top shows SW Maps display screen with status indicators. Six checklist items below with green checkmark or red X for each. Bottom shows large green "SAVE POINT" button if all checks pass, or large red "WAIT / TROUBLESHOOT" warning if any check fails. Include realistic status values for good scenario and problem scenario side by side.]

---

## Fix vs Float: Why the Difference Matters So Much

This deserves emphasis because it is confusing for new users.

**Common beginner mistake:** "I have Float solution and precision shows 0.3 meters. That seems pretty good, close to my 2 cm requirement. Should I save the point?"

**NO! Float is not adequate. You must have Fix.**

### Why Float is Not Adequate

Remember the carrier phase ambiguity problem? Float means:

**The receiver has NOT definitively determined which wave cycle it is measuring.**

It has narrowed down the possibilities - maybe you are in wave cycle 1,000,000 or 1,000,001 or 1,000,002 - but it has not resolved this to a single answer.

**Float gives you decimal accuracy with integer uncertainty.**

**Analogy:** Imagine measuring someone's height. You have a very precise measuring device that tells you "The person's height is 172.347 centimeters **above some unknown reference floor**."

But you do not know if the reference floor is:
- Ground level
- 1 meter above ground
- 2 meters above ground

You have centimeter precision in your measurement relative to an unknown reference. This is not useful for absolute height.

**Float solution is similar:** Centimeter-level precision relative to an uncertain reference (unresolved ambiguity). This does not give you the centimeter-level accuracy you need.

**Fix means the ambiguity is resolved:** You have determined which wave cycle you are measuring. Now your centimeter-level precision provides centimeter-level accuracy. You know the reference point.

**Practical impact:**

**Scenario:** You survey a GCP with Float solution.
- Position appears stable: (100.347, 200.521, 150.189)
- Precision estimate: 0.15 meters

You save this point, thinking "0.15 meters is pretty good."

**Later you return and survey the same GCP with Fix solution:**
- Position: (100.023, 200.508, 150.145)
- Precision estimate: 0.015 meters

**The positions differ by 32 centimeters!** The Float solution was off by much more than its precision estimate suggested.

**The fix solution gives you the true position (within 1-3 cm).**

**This is why the survey procedure absolutely requires Fix status. Float appears deceptively good but is not adequate.**

### How to Get Fix When Stuck in Float

**Common causes and solutions:**

**1. Insufficient satellites or poor geometry**
- **Cause:** Obstructed sky view, satellites bunched in one area
- **Solution:** Wait 10-20 minutes for satellite geometry to change, or move to location with better sky view

**2. Just started rover**
- **Cause:** Normal initialization period
- **Solution:** Wait patiently 5-20 minutes for ambiguity resolution

**3. Multipath or interference**
- **Cause:** Signals bouncing off metal, water, buildings
- **Solution:** Move 5-10 meters away from reflective surfaces

**4. Long baseline (far from base)**
- **Cause:** Base and rover separated by > 10 km (errors no longer correlated)
- **Solution:** Move closer to base or relocate base

**5. Ionospheric disturbance**
- **Cause:** Solar activity, geomagnetic storm
- **Solution:** Wait for better conditions (sometimes hours), or reduce baseline distance

**6. Lost base corrections**
- **Cause:** Radio link broken, base station offline
- **Solution:** Check base power, check radio antenna, reposition for line-of-sight

**Most common scenario: Just need to wait.** Ambiguity resolution takes time. Be patient.

**Sometimes: Need to move.** If you wait 20+ minutes with no fix, location likely has obstructed view. Move 10-20 meters to spot with more open sky.

---

## Practical Accuracy Expectations

What accuracy should you realistically expect with RTK in field conditions?

### Horizontal Accuracy (East-North Position)

**RTK fix conditions, good satellite geometry:**
- **Typical:** 1-2 cm (10-20 millimeters)
- **Excellent conditions:** 0.5-1 cm
- **Marginal conditions:** 2-3 cm

**Measurement consistency (re-measure same point):**
- **Good conditions:** Repeat measurements within 0.5-1 cm
- **Marginal conditions:** Repeat measurements within 2-3 cm

**OpenRiverCam requirement: 2-3 cm** is readily achievable with RTK in typical field conditions.

### Vertical Accuracy (Elevation)

**Vertical accuracy is typically worse than horizontal** by factor of 1.5-2×.

**RTK fix conditions, good satellite geometry:**
- **Typical:** 2-3 cm
- **Excellent conditions:** 1-2 cm
- **Marginal conditions:** 3-5 cm

**Why worse than horizontal?**
- Satellite geometry: Satellites are above you, not below, so vertical component has weaker geometry
- Atmospheric delays affect vertical more than horizontal
- Multipath from ground reflection

**OpenRiverCam requirement: 3-5 cm vertical** is achievable but requires attention to quality gates.

### Relative vs Absolute Accuracy

Remember this distinction (from Section 5.1):

**Relative accuracy:** How accurately surveyed points relate to each other
- **RTK delivers:** 1-3 cm relative accuracy
- **This is what matters for OpenRiverCam transformation**

**Absolute accuracy:** How accurately points are positioned in global coordinate system
- **RTK delivers (without PPP):** 20-50 cm absolute accuracy (limited by base station survey-in)
- **RTK delivers (with PPP):** 2-10 cm absolute accuracy (after post-processing base position)

**For day-of-survey work:** Relative accuracy is excellent and adequate.
**For integration with other data:** PPP post-processing recommended (Section 5.6).

### Check Point Monitoring: Verifying Survey Quality

**From SURVEY_PROCESS.md procedure:**

Establish check points (stable, marked locations) and re-measure throughout the day:
- **CP_START:** Beginning of survey
- **CP_NOON:** After 4-6 hours
- **CP_END:** End of survey

**Acceptance criteria:**
- Check point drift ≤ 3cm horizontal, ≤ 4cm vertical

**This verifies your RTK system is working correctly** and maintaining accuracy throughout the survey session.

**Example acceptable results:**

CP_START measurements (0800): E=100.023m, N=200.015m, Z=150.123m

CP_NOON measurements (1300): E=100.019m, N=200.018m, Z=150.127m
- Drift: 0.5cm E, 0.3cm N, 0.4cm V = ✓ PASS (well within limits)

CP_END measurements (1600): E=100.025m, N=200.013m, Z=150.119m
- Drift: 0.2cm E, 0.2cm N, 0.4cm V = ✓ PASS (excellent consistency)

**Example unacceptable results:**

CP_END measurements (1600): E=100.061m, N=200.009m, Z=150.167m
- Drift: 3.8cm E, 0.6cm N, 4.4cm V = ✗ FAIL (exceeds limits)

**If check points fail:** Something went wrong (base station moved, equipment malfunction, major atmospheric disturbance). Do NOT trust survey data. Investigate and potentially re-survey.

**Check points are quality control insurance.** They catch problems you might not notice in real-time.

---

## Why RTK Revolutionized Surveying

Context helps appreciate the technology:

### Before RTK: Surveying Was Professional Specialty

**Traditional total station surveying:**
- Required professional surveyor (4+ years training)
- Equipment cost: $10,000-30,000
- Time-intensive setup and measurement
- Limited to line-of-sight measurements
- Difficult across rivers or obstacles

**Result:** Surveying was expensive contractor service, not accessible for routine field work by program staff.

### RTK Changed the Accessibility

**Modern RTK GPS surveying:**
- Learnable by technical staff (2-3 days training)
- Equipment cost: $1,500-5,000 (affordable options)
- Relatively quick measurement (1-2 min per point)
- Works across obstacles (rivers, vegetation, terrain)
- Real-time feedback on quality

**Result:** Organizations can develop internal survey capacity. Humanitarian IM officers can conduct their own surveys for monitoring sites.

**This is why OpenRiverCam deployments are feasible in humanitarian contexts.** Ten years ago, centimeter-level surveying would have required expensive contractors. Today, you can purchase equipment and train your staff.

### The Continuing Evolution

**RTK technology continues improving:**
- **Cost decreasing:** Open-source receivers, affordable commercial systems
- **Ease of use improving:** Better software, clearer displays, automated quality checking
- **Accuracy improving:** Multi-frequency receivers, better algorithms
- **Global coverage expanding:** More satellite constellations (Galileo, BeiDou)

**Practical impact:** Surveying will become even more accessible over time. What seems moderately complex today will be routine tomorrow.

**You are learning these skills at a good time** - mature enough to be reliable, accessible enough to be learnable, with improving tools on the horizon.

---

## Connection to Survey Procedures

This section provided the technical foundation. **Now you understand the "why" behind the survey procedures:**

**When SURVEY_PROCESS.md says:**
- "RTK FIX ≥10 seconds" → You understand: ambiguities must be resolved and stable
- "PDOP ≤2.5" → You understand: satellite geometry must be adequate
- "Satellites ≥12" → You understand: need sufficient satellites for ambiguity resolution
- "30-60 minute base survey-in" → You understand: averaging to establish reference position
- "Check point drift ≤3cm" → You understand: verify relative accuracy maintained

**The procedures are not arbitrary rules - they are systematic application of RTK principles to ensure survey quality.**

**Chapter 9 (Site Survey) provides step-by-step field procedures.** When you execute those procedures, you will understand what you are doing and why, making you a more confident and effective surveyor.

---

## Summary: Key Concepts to Remember

**What RTK is:**
- Real-Time Kinematic positioning using two GPS receivers (base and rover)
- Base station generates corrections, rover applies them
- Achieves 1-3 cm accuracy through carrier phase measurements
- Requires resolving integer ambiguities (wavelength cycle counting)

**Fix vs Float - the critical distinction:**
- **Fix:** Ambiguities resolved, 1-3 cm accuracy, READY TO SURVEY
- **Float:** Ambiguities not resolved, 10-100 cm accuracy, NOT ADEQUATE
- **Single:** No corrections, 2-10 meter accuracy, COMPLETELY INADEQUATE
- Only survey with Fix status

**Base station role:**
- Establishes reference position (survey-in: 30-60 minutes)
- Measures errors in GPS signals
- Broadcasts corrections to rover in real-time
- Must remain stable throughout survey

**Rover role:**
- Receives satellite signals and base corrections
- Resolves carrier phase ambiguities
- Calculates position relative to base (1-3 cm accuracy)
- Requires good sky view, adequate satellites, good geometry

**Quality indicators to monitor:**
- Solution type (Fix required)
- Fix duration (≥10 seconds)
- Satellite count (≥12 standard, ≥10 canal)
- PDOP (≤2.5 standard, ≤3.0 canal)
- Precision estimates (≤2cm H / 3cm V standard)
- Age of corrections (< 3 seconds)

**Accuracy expectations:**
- Horizontal: 1-2 cm typical, 2-3 cm in marginal conditions
- Vertical: 2-3 cm typical, 3-5 cm in marginal conditions
- Relative accuracy (between points): Excellent, 1-3 cm
- Absolute accuracy: Moderate without PPP (20-50 cm), good with PPP (2-10 cm)

**Common challenges:**
- Initial fix acquisition takes 5-20 minutes (be patient)
- Float stuck: wait for better satellite geometry or move to better location
- Lost fix when walking under trees or near buildings (re-establish at open location)
- Multipath near metal or water (move away from reflective surfaces)

**Why RTK works for humanitarian contexts:**
- Achieves required centimeter accuracy
- Learnable with moderate training (not professional surveyor specialty)
- Increasingly affordable equipment ($1,500-3,000)
- Portable and field-suitable
- Real-time quality feedback guides correct operation

**The critical takeaway:**
RTK provides centimeter-level accuracy through a two-receiver system that cancels common GPS errors. Understanding Fix vs Float status is essential - only survey with Fix. Follow quality gate requirements (satellites, PDOP, precision) to ensure reliable measurements. With proper procedures, IM officers can achieve survey accuracy previously requiring professional surveyors.

You now have the technical foundation to understand the survey process. Sections 5.4-5.6 provide additional detail on specific aspects, and Chapter 9 gives you the step-by-step field procedures.

---

**Next Section:** [5.4 Base and Rover Stations](04-base-and-rover-stations.md)

[VISUAL PLACEHOLDER: Summary infographic showing RTK system overview. Center: "RTK System" title. Top left: Base station on tripod with "Establishes reference, generates corrections, broadcasts to rover." Top right: Satellite constellation sending signals to base and rover. Bottom left: Rover on survey pole at GCP with "Receives signals + corrections, resolves ambiguities, achieves Fix = 1-3cm accuracy." Bottom right: Status display showing quality indicators with green checkmarks. Arrows showing signal flow: satellites → base, satellites → rover, base corrections → rover. Large "FIX STATUS = READY TO SURVEY" badge at bottom center.]
