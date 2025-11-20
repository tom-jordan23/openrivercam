# 5.4 Base and Rover Stations

Section 5.3 explained how RTK works conceptually - two receivers working together to cancel out GPS errors. This section provides practical detail on the two components: what each station does, how to set them up, and how they communicate.

Understanding the distinct roles of base and rover helps you:
- Choose good locations for base station setup
- Troubleshoot communication problems
- Understand range limitations
- Recognize when equipment is working correctly
- Make informed decisions during field surveys

This is practical, operational knowledge that directly supports the field procedures in Chapter 9.

---

## The Two-Station System Architecture

RTK requires two distinct GPS receivers with different roles:

**Base Station (Static Reference):**
- Remains stationary throughout the survey session
- Establishes a reference position through survey-in process
- Continuously measures GPS errors
- Generates correction data in real-time
- Broadcasts corrections to rover via radio or cellular link
- Logs raw satellite data for post-processing (PPP)

**Rover Station (Mobile Measurement):**
- Carried to each survey point
- Receives normal GPS satellite signals
- Receives correction data from base station
- Applies corrections to achieve centimeter accuracy
- Provides position data to data collection device (smartphone/tablet)
- Requires continuous base connection to maintain RTK fix

**Think of it like this analogy:**

Imagine you are measuring distances with a rubber measuring tape that stretches unpredictably due to temperature and humidity.

**Base station role:** Keep the tape permanently stretched between two known reference points exactly 10.000 meters apart. Continuously monitor how much the tape has stretched - "Right now the tape reads 10.273 meters for a distance that should be 10.000 meters, so it is stretching by +0.273 meters."

**Rover role:** Use the same tape to measure your unknown distances. Apply the stretch correction - "The tape reads 15.487 meters. I know the tape is currently stretched by +0.273 meters. So the true distance is 15.487 - 0.273 = 15.214 meters."

**This works because the tape stretches the same amount for both measurements** (they are taken at the same time and place). RTK works because GPS errors affect both receivers similarly (they are observing the same satellites through the same atmosphere).

[VISUAL PLACEHOLDER: System diagram showing base and rover in context. Base station on left: tripod setup, antenna, receiver unit, radio transmitter, connected to laptop (optional). Rover on right: survey pole with antenna, receiver unit, radio receiver, connected to smartphone via USB. Satellites shown overhead sending signals to both. Correction data stream shown as radio waves from base to rover. Landscape shows river, trees, typical survey environment. Distance annotation: "Typical range 1-10 km depending on terrain and radio equipment."]

---

## Base Station: The Reference Foundation

The base station establishes the reference framework for your entire survey. Understanding its role helps you set it up correctly and maintain survey quality.

### Base Station Functions in Detail

**1. Survey-In: Establishing Reference Position**

When you power on the base station at the start of the day, it does not yet know its exact position. The survey-in process determines this.

**How survey-in works:**
- Base station receives standard GPS signals from satellites
- It continuously measures its position using these signals
- Each individual measurement has typical GPS errors: ±0.5-2 meters
- But the base station is not moving, so errors are random in different directions
- Over time (30-60 minutes), averaging thousands of measurements cancels random errors
- Final position accuracy: ~25 centimeters (much better than single measurement)

**Analogy:** Imagine 1,000 people independently estimate the location of a street corner using GPS on their phones. Each person's estimate is off by a few meters in random directions. But if you average all 1,000 estimates, the random errors cancel out and you get close to the true location.

**Survey-in parameters from SURVEY_PROCESS.md:**
- Duration: 30-60 minutes
- Minimum satellite count: ≥15 satellites
- Required geometry: PDOP ≤1.5
- Target accuracy: 0.25 meters

**Why these requirements matter:**
- **30-60 minutes:** Longer duration provides more measurements to average, reducing uncertainty
- **≥15 satellites:** More satellites provide better geometry and redundancy
- **PDOP ≤1.5:** Ensures satellites are well-distributed across the sky (not bunched in one area)
- **0.25m accuracy:** Adequate for most survey applications; can be improved with PPP post-processing

**Important understanding:** The base station's 25 cm absolute position accuracy is moderate, but this is acceptable because:
- **Relative accuracy** between survey points is 1-3 cm (this is what matters for OpenRiverCam transformation)
- **Absolute accuracy** can be improved to 2-10 cm later through PPP post-processing (Section 5.6)
- The base position establishes a stable reference - as long as it does not move, your survey is internally consistent

**2. Error Measurement: Calculating Corrections**

Once survey-in completes, the base station knows its reference position. It then continuously:

**Measures GPS signals:**
- Tracks all visible satellites (typically 15-25 satellites)
- Measures carrier phase and pseudorange for each satellite
- Calculates what its position should be based on current signals

**Compares to reference:**
- Known position: (100.000m East, 200.000m North, 150.000m elevation)
- Measured position right now: (100.237m E, 200.189m N, 149.845m elevation)
- **Detected errors:** +0.237m E, +0.189m N, -0.155m elevation

**Generates corrections:**
- These errors are satellite-specific and change every second
- Base station packages corrections into standard RTCM3 messages
- Corrections include:
  - Carrier phase corrections for each satellite
  - Pseudorange corrections
  - Station reference position
  - GPS/GLONASS/Galileo satellite-specific data

**Updates continuously:**
- Corrections generated every 1 second
- Broadcast to rover in real-time
- Rover applies corrections to its own simultaneous measurements

**Why this works:** The rover is nearby (within 10 km), so it sees almost exactly the same satellite signals through the same atmosphere. The errors affecting the base also affect the rover. By measuring and transmitting the errors, the base enables the rover to cancel them out.

**3. Correction Broadcast: Real-Time Transmission**

The base station transmits corrections to the rover using one of these methods:

**Radio Link (Most Common for Field Surveys):**
- Frequency: Typically 433 MHz or 915 MHz (license-free bands)
- Range: 1-10 kilometers depending on terrain and power
- Advantages: No ongoing costs, works anywhere, reliable
- Limitations: Line-of-sight helpful, range limited by terrain
- Protocol: RTCM3 messages via radio serial connection

**Cellular/Internet Link (NTRIP):**
- Uses cellular data connection to transmit corrections
- Rover connects via internet to base station's NTRIP server
- Range: Unlimited (anywhere with cell coverage)
- Advantages: No range limitations, works in urban areas
- Limitations: Requires cell coverage, ongoing data costs
- Protocol: RTCM3 via NTRIP (Networked Transport of RTCM via Internet Protocol)

**Which to use:**
- **Field surveys in remote areas:** Radio link (reliable, no infrastructure needed)
- **Urban or permanent installations:** NTRIP (unlimited range, no line-of-sight issues)
- **OpenRiverCam typical use:** Radio link is standard

**Correction data rate:**
- Typical: 1 Hz (corrections sent once per second)
- Higher rates (5-10 Hz) provide slightly better performance for moving rovers
- For static surveying (measuring stationary points), 1 Hz is adequate

**Data volume:**
- RTCM3 messages: ~500-1000 bytes per second
- Radio bandwidth: Easily handled by typical telemetry radios
- Cellular bandwidth: Minimal data usage (few MB per day)

**4. Raw Data Logging: Enabling Post-Processing**

While broadcasting real-time corrections, the base station should also log raw satellite observations for later PPP post-processing (Section 5.6).

**What gets logged:**
- Raw carrier phase measurements for each satellite
- Pseudorange measurements
- Satellite ephemeris data (orbital information)
- All data needed to recreate precise position solutions offline

**File format:**
- Logged as UBX format (u-blox proprietary binary)
- Later converted to RINEX format for PPP processing
- Typical file size: 50-200 MB per day

**Why this matters:**
- PPP post-processing can improve base station position from 25 cm to 2-10 cm accuracy
- This correction is then applied to all survey points (Section 5.6)
- Provides absolute position accuracy suitable for integration with maps, satellite imagery, other data sources

**From SURVEY_PROCESS.md:**
- Start RINEX logging at beginning of base station survey-in
- Continue logging entire survey session (6-12 hours typical)
- Stop logging at end of day before powering down base

### Base Station Setup Requirements

Understanding why each requirement matters helps you select good base station locations.

**Site Selection Criteria:**

**Open sky view >15° above horizon:**
- **Requirement:** Clear view of sky from 15 degrees above horizon to zenith
- **Why:** Satellites need clear signal path to antenna; obstructions cause signal loss
- **Practical check:** Stand at proposed base location, look around horizon - no trees, buildings, or terrain blocking sky above 15° angle
- **What happens if violated:** Reduced satellite count, poor geometry (high PDOP), survey-in takes longer or fails

**>10 meters from metal structures and vehicles:**
- **Requirement:** Keep base antenna at least 10 meters from large metal objects, vehicles, fences
- **Why:** GPS signals reflect off metal surfaces (multipath), causing false measurements
- **Practical check:** Look for metal roofs, vehicles, chain-link fences, large equipment
- **What happens if violated:** Noisy measurements, poor survey-in accuracy, unstable corrections

**Stable ground:**
- **Requirement:** Ground that will not move, settle, or vibrate during survey session
- **Why:** Any base station movement invalidates all corrections sent to rover
- **Practical check:** Avoid soft soil, active construction zones, areas with vehicle traffic vibration
- **What happens if violated:** Survey becomes unreliable; check points show excessive drift

**Accessible for monitoring:**
- **Requirement:** Safe, accessible location where you can check base periodically
- **Why:** Need to verify base remains operational, check battery, monitor radio link
- **Practical check:** Can you safely visit this location 2-3 times during survey day?
- **What happens if violated:** Cannot troubleshoot problems if rover loses fix

**For canal/irrigation surveys - additional requirement:**
- **High ground >20 meters from water:**
- **Why:** Multipath from water surface reflection causes signal interference
- **Practical check:** Position base on levee or high ground overlooking survey area
- **What happens if violated:** Degraded base station performance, more difficult to achieve rover fix

**Site selection priority:**
1. Sky view (most critical)
2. Stable ground (second most critical)
3. Distance from metal/reflective surfaces
4. Accessibility
5. Radio line-of-sight to survey area (helpful but not essential)

[VISUAL PLACEHOLDER: Overhead view diagram showing good vs poor base station locations. Good location: Open field, marked with green checkmark, annotations showing "Clear sky >15°", "10m from vehicle", "Stable ground", radio range circles. Poor location: Under tree, near building, marked with red X, annotations showing blocked sky, multipath from building, unstable ground. Survey area shown with rover positions scattered in river vicinity.]

**Physical Setup Process:**

**1. Connect antenna BEFORE powering base:**
- **Critical:** NEVER power on GPS receiver without antenna connected
- **Why:** RF energy can damage receiver front-end if reflected back (no antenna = total reflection)
- **Procedure:** Connect antenna cable, verify secure connection, then apply power

**2. Level tripod, mark exact position:**
- **Level tripod:** Use bubble level, adjust tripod legs
- **Why level matters:** Antenna should be vertically oriented for optimal satellite reception
- **Mark position:** Spray paint or metal stake at exact tripod point
- **Why mark:** Allows re-establishing base at same location for multi-day surveys

**3. Measure antenna height:**
- **Requirement:** Three measurements from ground to Antenna Reference Point (ARP)
- **ARP location:** Typically bottom of antenna (marked on antenna or in specifications)
- **Average three measurements:** Reduces measurement error
- **Record to nearest 0.5 cm:** 0.001m precision (e.g., 1.687m)
- **Why this matters:** PPP processing requires exact antenna height; 1 cm error = 1 cm vertical position error for all survey points

**Example antenna height measurement:**
- Measurement 1: 1.685m
- Measurement 2: 1.689m
- Measurement 3: 1.687m
- Average: (1.685 + 1.689 + 1.687) / 3 = 1.687m
- Record: **Antenna height = 1.687m to ARP**

**4. Configure and start survey-in:**
- Use u-center software (Appendix C in SURVEY_PROCESS.md provides detailed steps)
- Set survey-in parameters: 30-60 minutes, 0.25m accuracy
- Monitor progress: Check satellite count (≥15), PDOP (≤1.5)
- Wait for completion: Patience required - this is not equipment failure, it is the reference establishment process
- Verify final position: Record coordinates in UTM Zone 48S (or your project CRS)

**5. Start raw data logging:**
- Enable UBX-RXM-RAWX and UBX-RXM-SFRBX messages in u-center
- Start database logging to save UBX file
- Logging runs entire survey session (6-12 hours)
- File will be converted to RINEX for PPP post-processing (Section 10 of SURVEY_PROCESS.md)

**Base station is now operational and providing corrections to rover.**

### Base Station Monitoring During Survey

The base station must remain operational throughout your survey session. Periodic monitoring ensures reliability.

**What to check during monitoring visits (2-3 times per survey day):**

**Power status:**
- Base receiver powered on, indicator lights active
- Battery level if using battery power (ensure >4 hours remaining)
- Backup battery connected and available if power fails

**Survey-in status:**
- Survey-in completed successfully (not in "Survey-in in progress" mode)
- Base station in "Fixed Mode" (transmitting corrections based on established reference position)

**Radio transmission:**
- Radio modem powered on, transmitting
- Indicator lights show data transmission activity
- If rover loses fix, check base station radio first

**Physical stability:**
- Tripod has not moved, settled, or been disturbed
- Antenna cable secure
- Equipment protected from weather if conditions change

**Software logging:**
- Raw data logging still active (check laptop/logger display)
- File size increasing (indicates data being recorded)

**Troubleshooting base station problems:**
- **Power loss:** Switch to backup battery immediately, note time of interruption
- **Survey-in reset:** If base accidentally reset, must restart survey-in (30-60 minutes) - all previous rover measurements invalidated
- **Radio failure:** Check connections, power cycle radio, verify configuration
- **Laptop/logger crash:** Restart logging immediately, note gap in raw data

**What to do if base station fails during survey:**
- **Minor interruption (<5 minutes):** Resume survey if base re-establishes quickly
- **Major interruption (>5 minutes) or position reset:** Re-survey check points, potentially restart entire survey session
- **Cannot restore base function:** End survey session, troubleshoot equipment before next field day

**Check point monitoring provides quality assurance** (Section 4 of SURVEY_PROCESS.md): If check points drift >3cm horizontal or >4cm vertical during the day, base station may have moved or experienced errors.

---

## Rover Station: The Mobile Measurement Unit

The rover is what you carry to each survey point. It receives corrections from the base and calculates precise positions.

### Rover Station Functions in Detail

**1. Satellite Signal Reception**

The rover antenna receives signals from all visible GNSS satellites (GPS, GLONASS, Galileo, BeiDou depending on receiver capabilities).

**What the rover tracks:**
- Carrier phase: Precise measurement of signal wave cycles (see Section 5.3 explanation)
- Pseudorange: Travel time from satellite to receiver
- Satellite ephemeris: Orbital position data
- All available satellite constellations for maximum satellite count

**Antenna requirements:**
- Clear view of sky (same as base station: >15° above horizon)
- Stable position during measurement (vertical on survey pole, bubble level centered)
- No body blocking between antenna and satellites (surveyor stands to side, not under antenna)
- Distance from reflective surfaces (metal, water) during measurement

**Multi-GNSS benefit:**
- Modern receivers track GPS + GLONASS + Galileo + BeiDou
- Typical satellite count: 18-30 satellites visible (vs 8-12 with GPS alone)
- More satellites = better geometry, easier fix acquisition, more reliable fix maintenance
- RTK ambiguity resolution is easier with more measurements

**2. Correction Data Reception**

Simultaneously with tracking satellites, the rover receives correction data from the base station.

**What corrections contain:**
- Carrier phase corrections for each satellite
- Pseudorange corrections
- Base station reference position
- Correction age timestamp (how recently correction was calculated)

**Reception methods:**
- **Radio link:** Rover has radio modem receiving RTCM3 corrections from base
- **NTRIP:** Rover connected via smartphone cellular to NTRIP server

**Quality indicators for corrections:**
- **Age of corrections:** How long since correction was generated
  - Target: <1 second (fresh corrections)
  - Acceptable: <3 seconds
  - Poor: >3 seconds (degraded performance)
  - No fix possible: >10 seconds or no corrections (connection lost)
- **Data completeness:** All required RTCM3 messages received (1005, 1077, 1087, 1097)

**What happens if correction link is lost:**
- RTK fix immediately degrades to float or single
- Position accuracy drops from 1-3 cm to 0.5-2 meters
- Cannot survey until connection restored
- Rover will attempt to maintain last known correction, but this degrades rapidly (within seconds)

**Troubleshooting correction reception:**
- Check radio link: Verify base radio transmitting, rover radio powered on
- Check line-of-sight: Terrain, buildings may block radio signal
- Check range: If rover >10 km from base, radio link may be too weak
- Check base station: Verify base is operational and transmitting

**3. RTK Position Calculation**

The rover combines satellite measurements with base corrections to calculate precise position.

**Processing steps (automated by receiver):**
- Receive satellite signals → measure carrier phase and pseudorange
- Receive base corrections → apply to satellite measurements
- Calculate position relative to base station
- Attempt to resolve carrier phase ambiguities (which wave cycle am I measuring?)
- If ambiguities resolved → **RTK FIX** (1-3 cm accuracy)
- If ambiguities not resolved → **RTK FLOAT** (10-100 cm accuracy)
- Update solution every second (1 Hz) or faster

**What determines fix vs float:**
- Satellite count and geometry (Section 5.3 discussion applies)
- Signal quality (clear sky view, minimal multipath)
- Distance from base (errors correlate well within 10 km)
- Time for ambiguity resolution (5-20 minutes initial, 2-5 minutes if fix lost and re-acquired)

**Solution types the rover can report:**
- **Single (Autonomous):** No corrections, 2-10 meter accuracy - NOT suitable for surveying
- **DGPS (Differential):** Pseudorange corrections only, 0.5-2 meter accuracy - NOT suitable for surveying
- **Float:** Receiving corrections, ambiguities not resolved, 0.1-1 meter - NOT suitable for surveying
- **Fix (Fixed):** Ambiguities resolved, 1-3 cm accuracy - **REQUIRED for surveying**

**4. Position Output to Data Collector**

The rover transmits its calculated position to a data collection device (smartphone or tablet).

**Connection methods:**
- **USB cable:** Rover connected to Android device via USB OTG cable (most common)
- **Bluetooth:** Wireless connection (some receivers support this)

**Data format:**
- NMEA sentences: Standard GPS text messages containing position, time, quality indicators
- Typical sentences: GGA (position), RMC (recommended minimum data), GSA (satellite status)
- Update rate: 1 Hz (once per second) typical

**GNSS Master app (from SURVEY_PROCESS.md):**
- Android app that receives NMEA data from rover via USB
- Decodes position, quality indicators, satellite info
- Provides position as "mock location" to other Android apps
- SW Maps (data collection app) uses this position for survey point recording

**Data flow:**
1. Rover calculates RTK position
2. Rover outputs NMEA sentences via USB
3. GNSS Master receives NMEA data
4. GNSS Master provides position to SW Maps via Android mock location API
5. SW Maps displays position, quality indicators, enables point collection

### Rover Hardware: Antenna and Survey Pole

Understanding the physical rover setup helps you measure accurately and maintain RTK fix.

**Survey Pole Configuration:**

**Components:**
- Survey pole: Telescoping or fixed-length pole (typically 2 meters)
- Rover antenna: Mounted on top of pole via threaded adapter
- Circular bubble level: Mounted on pole at eye level
- Pole tip: Sharp point or flat base contacts ground at survey point
- Height measurement: Tape measure along pole to determine precise height

**Pole setup:**
- Extend pole to appropriate height (typically 1.5-2.5 meters for comfortable viewing of bubble)
- Lock pole sections securely (must not slip during measurement)
- Attach rover antenna to top with secure threaded connection
- Ensure bubble level is visible from surveyor's position

**Maintaining vertical:**
- **Critical requirement:** Pole must be perfectly vertical during measurement
- **How to verify:** Center bubble in circular level
- **Why it matters:** Tilted pole introduces horizontal position error
  - 2-meter pole tilted 5° = 17 cm horizontal error (NOT acceptable!)
  - 2-meter pole tilted 1° = 3.5 cm horizontal error (marginal)
  - Pole vertical (bubble centered) = minimal error
- **Technique:** Hold pole stable, adjust until bubble perfectly centered, hold during averaging period

[VISUAL PLACEHOLDER: Side-by-side comparison showing correct vs incorrect rover setup. Left (CORRECT, green checkmark): Pole vertical, bubble centered, surveyor standing to side not blocking antenna, pole tip firmly on ground at GCP marker. Right (INCORRECT, red X): Pole tilted, bubble off-center, surveyor standing under antenna blocking signals, pole tip not on marker. Annotations showing tilt angle and resulting horizontal error.]

**Measuring Pole Height:**

**Why measure pole height:**
- Rover measures position of antenna phase center (at top of pole)
- Survey requires position of ground point (at bottom of pole)
- Must subtract pole height from antenna elevation to get ground elevation

**Pole height measurement procedure:**
- Measure from pole tip to Antenna Reference Point (ARP) on antenna
- ARP is typically at bottom of antenna (check antenna specifications)
- Use metal tape measure, avoid cloth tape (stretches)
- Measure to nearest 0.5 cm (0.005m)
- Repeat measurement if changing pole height during survey

**Example calculation:**
- Rover measures antenna position: E=100.237m, N=200.456m, Elevation=152.347m
- Pole height measured: 2.150m
- GCP ground position: E=100.237m, N=200.456m, **Elevation=152.347 - 2.150 = 150.197m**

**Common pole height practice:**
- **Fixed pole height:** Set pole to one height (e.g., 2.000m), measure once, use for all points
  - Advantage: Measure height once, faster field work
  - Disadvantage: May need to adjust height for terrain, water measurements
- **Variable pole height:** Adjust pole for each measurement, measure height each time
  - Advantage: Optimal pole height for each situation
  - Disadvantage: More time, more measurement opportunities for error
- **OpenRiverCam surveys:** Fixed height is typical for GCPs, variable height may be needed for water surface or cross-sections in deep channels

**Pole height accuracy requirement:**
- Measure to 0.5 cm precision
- Vertical position accuracy target: 3 cm
- Pole height measurement error should be <1/6 of total error budget

### Rover Measurement Procedure in the Field

This is the practical workflow for surveying each GCP or cross-section point.

**Step 1: Approach survey point**
- Move to GCP location with rover on pole
- Monitor SW Maps display - verify RTK fix maintained during movement
- If fix lost during approach (walked under trees, near building), wait at open location for fix to re-establish

**Step 2: Position pole at survey point**
- Place pole tip precisely on ground marker (GCP target, cross-section station)
- Ensure stable contact (not rocking on uneven ground)
- Initial pole verticality (bubble approximately centered)

**Step 3: Verify RTK solution quality**

Check all quality gates from SURVEY_PROCESS.md before starting measurement:

**Solution status: RTK FIX**
- Verify display shows "FIX" not "FLOAT" or "SINGLE"
- If not fix: Wait, or move 2-3 meters to better location, retry

**Fix duration: ≥10 seconds**
- Check "time since fix acquired" indicator
- If <10 seconds: Wait for 10 seconds stable fix
- This ensures ambiguities are definitely resolved (not false fix)

**Satellite count: ≥12 (standard) or ≥10 (canal relaxed)**
- Check satellite count display
- If inadequate: Wait for satellite geometry to improve, or move to better sky view

**PDOP: ≤2.5 (standard) or ≤3.0 (canal relaxed)**
- Check PDOP indicator
- Lower is better: <2.0 excellent, 2.0-2.5 good, 2.5-3.0 acceptable for canal
- If too high: Wait for satellite geometry to change

**Precision estimates: ≤2cm H / 3cm V (standard) or ≤4cm H / 6cm V (canal)**
- Check horizontal and vertical precision in SW Maps display
- These are estimated accuracies based on current satellite geometry and signal quality
- If inadequate: Extend averaging time, improve pole stability, or move to better location

**Age of corrections: <3 seconds**
- Verify base corrections being received recently
- If corrections old or missing: Check base station, radio link

**Step 4: Start averaging measurement**

Once all quality gates passed:

- Select survey point in SW Maps
- Start GPS averaging (60 seconds standard, 120 seconds for canal)
- Carefully maintain pole verticality (bubble centered) throughout averaging period
- Hold pole stable (minimize movement)
- Monitor display - verify fix maintained, precision stable

**During averaging:**
- Focus on bubble level (keep centered)
- Do not talk on radio or get distracted
- If fix lost during averaging: Abort, restart measurement
- If pole tips or moves: Abort, restart measurement

**Step 5: Record point and attributes**

After averaging completes:

- SW Maps displays averaged position
- Verify position looks reasonable (not large jump from expected)
- Enter required attributes:
  - Point ID or station number
  - Point type (GCP, cross-section, water level, etc.)
  - Pole height
  - Notes (any unusual conditions)
- Save point

**SW Maps records:**
- Averaged East, North, Elevation coordinates (in project CRS: UTM 48S)
- Precision estimates
- Timestamp
- Number of satellites
- PDOP value
- All entered attributes

**Step 6: Verify and move to next point**

- Check that point saved successfully
- If next point nearby: Move directly (fix typically maintained)
- If next point requires walking through obstructed area: Expect to lose fix, re-establish at next point
- Continue surveying remaining points

**Efficiency considerations:**
- Once fix established, you can survey 10-20 points per hour (with 60s averaging)
- Plan survey route to minimize losing fix (survey points in sequence without passing under trees)
- If working in challenging environment (forest, urban), budget extra time for fix re-acquisition

---

## Communication Between Base and Rover

Understanding the base-rover communication link helps troubleshoot problems and optimize setup.

### What Gets Transmitted

The base station transmits RTCM3 (Radio Technical Commission for Maritime Services) correction messages.

**Key RTCM3 messages used:**

**Message 1005: Station Coordinates**
- Contains base station reference position (X, Y, Z in ECRS coordinates)
- Transmitted periodically (every 10 seconds typical)
- Rover needs this to calculate its position relative to base

**Message 1077: GPS MSM7 (Multiple Signal Message)**
- GPS carrier phase and pseudorange corrections for all tracked GPS satellites
- Full precision, all signals (L1, L2, L5 if available)
- Transmitted every second (1 Hz)

**Message 1087: GLONASS MSM7**
- GLONASS carrier phase and pseudorange corrections
- Transmitted every second

**Message 1097: Galileo MSM7**
- Galileo carrier phase and pseudorange corrections
- Transmitted every second

**Message 1127: BeiDou MSM7** (if receiver supports)
- BeiDou carrier phase and pseudorange corrections
- Transmitted every second

**Why MSM7 (full precision) messages:**
- MSM7 provides highest precision corrections
- Required for RTK fix (lower message types like MSM4 provide less precision)
- Contains all information needed for carrier phase ambiguity resolution

**Data volume:**
- All messages combined: ~500-1000 bytes per second
- Per hour: ~2-3 MB
- Easily handled by radio telemetry links (typical 9600 baud or higher)

### Radio Link Setup and Range

Most field surveys use radio modems for base-rover communication.

**Typical radio configuration:**

**Frequency bands:**
- 433 MHz: Common in Europe, Asia (license-free ISM band)
- 915 MHz: Common in North America, Australia (license-free ISM band)
- Check local regulations for allowed frequencies and power levels

**Radio power:**
- Typical: 100 mW to 1 W transmit power
- Higher power = longer range, but battery drain increases
- Most field surveys: 100-500 mW adequate

**Modulation and baud rate:**
- LoRa (Long Range): Modern, excellent range and penetration
- FSK (Frequency Shift Keying): Traditional, reliable
- Baud rate: 9600-57600 bps typical (RTCM3 data rate easily supported)

**Range expectations:**

**Open terrain (flat, no obstructions):**
- Line-of-sight: 5-15 km depending on radio power and antenna
- Typical practical range: 5-10 km

**Rolling terrain (hills, vegetation):**
- Variable: 1-5 km depending on terrain profile
- Hilltops provide excellent range (base on high ground can see rover 10+ km)
- Valleys limit range (rover in valley may lose link even if base is 2 km away)

**Forest or dense vegetation:**
- Limited: 0.5-3 km depending on vegetation density
- Leaves attenuate radio signals
- Lower frequencies (433 MHz) penetrate better than higher (915 MHz)

**Urban environment:**
- Variable: 1-5 km depending on buildings
- Multipath and reflections complicate signal
- Line-of-sight critical (building in direct path may block link entirely)

**For OpenRiverCam surveys:**
- Typical base-rover separation: 50-500 meters
- Well within radio range for any terrain
- Radio link is rarely the limiting factor

**Optimizing radio range:**
- **Base antenna height:** Elevate base radio antenna on mast or pole (3-5 meters)
- **Rover antenna position:** Keep rover radio antenna clear of body, equipment
- **Line-of-sight:** Position base with good view toward survey area
- **Radio power:** Use adequate power setting (don't use minimum power if battery allows more)

### Cellular/NTRIP Alternative

For some applications, cellular internet connection is preferred over radio link.

**NTRIP (Networked Transport of RTCM via Internet Protocol):**

**How it works:**
- Base station connected to internet (cellular modem, WiFi, or wired)
- Base runs NTRIP server software or connects to NTRIP caster
- Rover connects to NTRIP server via smartphone cellular internet
- RTCM3 corrections transmitted over internet instead of radio

**Advantages:**
- Unlimited range (rover can be anywhere with cellular coverage)
- No line-of-sight required
- Can support multiple rovers from one base
- Can use CORS (Continuously Operating Reference Station) networks instead of your own base

**Disadvantages:**
- Requires cellular coverage (not available in remote areas)
- Ongoing data costs (typically minimal: few MB per day)
- Dependent on cellular network reliability
- Slightly higher latency (internet routing delay) vs direct radio link

**When to use NTRIP:**
- Urban surveys with good cellular coverage
- Long-range surveys (rover >10 km from base)
- Multiple rovers working simultaneously
- Using existing CORS network instead of setting up base station

**When to use radio link:**
- Remote areas without cellular coverage (typical OpenRiverCam deployment context)
- Short-range surveys where radio is reliable
- Prefer independence from infrastructure
- Lower operating costs (no cellular data fees)

**OpenRiverCam typical approach:** Radio link is standard due to remote field locations and reliability.

### Troubleshooting Communication Problems

**Symptom: Rover shows "No corrections" or "Age of corrections >10 seconds"**

**Diagnosis and solutions:**

**1. Check base station:**
- Is base powered on and operational?
- Has base completed survey-in (not still initializing)?
- Is base radio transmitting? (Check radio indicator lights)
- Is base antenna connected?

**2. Check rover radio:**
- Is rover radio powered on?
- Check rover radio antenna connected
- Verify radio on same frequency/channel as base
- Check radio configuration (baud rate, modulation match base)

**3. Check range and line-of-sight:**
- How far is rover from base? (Check on map if uncertain)
- Is there terrain, vegetation, buildings blocking radio path?
- Try moving to higher ground or more open location

**4. Check interference:**
- Are other radios operating on same frequency nearby?
- Urban environment may have significant interference
- Try different radio channel if available

**5. Test radio link:**
- Use radio diagnostics if available (RSSI - Received Signal Strength Indicator)
- Walk toward base - does signal improve?
- If signal good when close to base but fails far away: Range limitation, need higher power or better antennas

**Symptom: Corrections received but rover stuck in Float**

**This is NOT a communication problem** - see Section 5.5 (RTK Fix Status) for fix vs float troubleshooting.

**Symptom: Intermittent loss of corrections (age of corrections jumps 0s → 5s → 0s → 8s)**

**Diagnosis:**
- Weak radio signal (rover at edge of range)
- Obstructions partially blocking line-of-sight (trees, terrain)
- Interference causing packet loss

**Solutions:**
- Move rover closer to base
- Reposition base for better line-of-sight to survey area
- Use higher radio power or better antenna
- Survey from locations with better radio visibility to base

---

## Operating Range and Practical Limitations

Understanding RTK operating range helps you plan surveys and choose base station locations.

### Range Limitations by Type

**Radio link range: 1-10 km typical**
- Determines communication, not RTK accuracy
- If radio link fails, rover cannot receive corrections (no RTK fix possible)
- Can be extended with higher power radios, better antennas, or repeaters
- For OpenRiverCam surveys (rover typically <500m from base), radio range is not limiting

**RTK accuracy range: 0-10 km (baseline distance)**
- This is the key RTK limitation
- Errors affecting base and rover are most correlated when close together
- As distance increases, atmospheric errors become less correlated
- RTK fix becomes more difficult to achieve and maintain at longer baselines

**Accuracy vs baseline distance:**

**0-1 km baseline:**
- Optimal RTK performance
- Fix acquisition: 2-10 minutes typical
- Fix reliability: Excellent
- Accuracy: 1-2 cm horizontal, 2-3 cm vertical

**1-5 km baseline:**
- Good RTK performance
- Fix acquisition: 5-15 minutes typical
- Fix reliability: Good
- Accuracy: 1-3 cm horizontal, 2-4 cm vertical

**5-10 km baseline:**
- Marginal RTK performance
- Fix acquisition: 10-30 minutes (or may not achieve fix)
- Fix reliability: Variable (may lose fix more easily)
- Accuracy: 2-5 cm horizontal, 3-6 cm vertical (when fix achieved)

**>10 km baseline:**
- Poor RTK performance
- Fix acquisition: Difficult or impossible
- Fix reliability: Poor
- Accuracy: Often stuck in float (10-50 cm)
- **Not recommended for standard RTK surveying**

**Why baseline distance matters:**
- Atmospheric delay (ionosphere, troposphere) varies across distance
- Base station at one location measures atmospheric delay there
- Rover 50 km away experiences different atmospheric delay
- Corrections no longer cancel errors effectively
- Carrier phase ambiguity resolution fails or becomes unreliable

**For OpenRiverCam deployments:**
- Base and rover typically within 50-500 meters
- Well within optimal RTK range
- Baseline distance is not a limiting factor
- Can confidently expect 1-3 cm accuracy

### Base Station Placement Strategy

**Minimizing baseline distance:**
- Place base station near center of survey area
- Reduces maximum baseline to any survey point
- Example: Survey area is 1 km × 1 km - place base in center, max baseline = 700m (diagonal)

**Line-of-sight for radio:**
- Position base with view toward survey area
- Higher ground helpful (base on levee overlooking river)
- Reduces radio transmission problems

**Accessibility for monitoring:**
- Must be able to safely visit base station 2-3 times during survey day
- Check battery, verify operation, troubleshoot if needed
- Balance remote positioning (good sky view) with safe access

**Multi-day surveys:**
- If surveying same site multiple days, mark base position
- Re-establish base at same location for consistency
- Reduces need to re-survey check points
- Allows comparing day-to-day results with confidence

### Equipment Requirements Summary

Understanding what equipment you need for base and rover helps with procurement and field preparation.

**Base Station Equipment:**
- GNSS receiver capable of RTK base mode (e.g., u-blox F9P or similar)
- Multi-band antenna (L1/L2 GPS + GLONASS + Galileo support)
- Tripod or stable mounting
- Radio modem for transmitting corrections (or cellular modem for NTRIP)
- Power source: Battery (8-12 hour capacity) or external power
- Antenna cable (connect antenna to receiver)
- Computer/logger for configuration and raw data logging (laptop or dedicated logger)
- Software: u-center (for u-blox receivers) or equivalent configuration software

**Rover Station Equipment:**
- GNSS receiver capable of RTK rover mode (same model as base is common)
- Multi-band antenna (same specifications as base)
- Survey pole (telescoping or fixed, 1.5-2.5 meters)
- Circular bubble level (mount on pole)
- Radio modem for receiving corrections (matched to base radio)
- Power source: Battery (6-8 hour capacity typical)
- Data collector: Smartphone or tablet running SW Maps
- USB OTG cable: Connect rover to Android device
- GNSS Master app: Provides mock location to SW Maps
- Tape measure: For pole height measurement

**Accessories and Field Supplies:**
- Spare batteries for base and rover
- Power bank for Android device
- Antenna cables, USB cables (spares)
- Field notebook, pencils (waterproof)
- Markers, spray paint (mark base position, GCPs)
- Sunscreen, water, field safety equipment
- Equipment cases (protective transport)

**Total equipment cost (indicative):**
- Base + Rover RTK system: $1,500-5,000 (affordable options like ArduSimple vs professional-grade)
- Antennas and cables: $200-500
- Radios: $100-400
- Survey poles and accessories: $100-300
- Data collection device: $200-500 (Android tablet)
- **Total system: $2,000-7,000 depending on quality level**

**This is affordable compared to traditional surveying:**
- Professional-grade total station: $10,000-30,000
- Survey-grade GPS (non-RTK): $5,000-15,000
- RTK has made centimeter surveying accessible to humanitarian organizations

---

## Connection to Survey Procedures

This section explained the practical operation of base and rover stations. Now you understand:

**When SURVEY_PROCESS.md specifies base station setup:**
- Open sky >15° → Ensures satellite reception for survey-in and corrections
- Stable ground → Prevents base movement that would invalidate survey
- 30-60 minute survey-in → Establishes reference position through averaging
- Antenna height measurement → Required for PPP post-processing accuracy

**When SURVEY_PROCESS.md specifies rover measurement procedure:**
- RTK FIX ≥10 seconds → Ensures ambiguities resolved and stable
- Pole vertical (bubble centered) → Prevents horizontal error from pole tilt
- Pole height measurement → Calculates ground elevation from antenna elevation
- Quality gates (satellites, PDOP, precision) → Ensures measurement reliability

**Next sections build on this foundation:**
- Section 5.5 explains RTK fix status in detail (how to achieve fix, troubleshoot float)
- Section 5.6 explains post-processing workflow (PPP corrections using logged base data)

You now have the operational knowledge to understand base and rover roles during field surveys. Chapter 9 provides step-by-step field procedures that apply this knowledge.

---

## Summary: Key Concepts

**Base station role:**
- Establishes reference position through survey-in (30-60 min averaging)
- Measures GPS errors by comparing signals to known reference
- Generates RTCM3 correction data for each satellite every second
- Broadcasts corrections to rover via radio or cellular link
- Logs raw data for PPP post-processing

**Rover station role:**
- Receives satellite signals (carrier phase and pseudorange)
- Receives correction data from base station
- Calculates position by applying corrections
- Resolves carrier phase ambiguities to achieve RTK fix
- Outputs position to data collector (smartphone via USB)

**Communication link:**
- Radio (typical): 1-10 km range, no infrastructure needed
- NTRIP (alternative): Unlimited range, requires cellular coverage
- RTCM3 messages: ~500-1000 bytes/second
- Age of corrections <3 seconds required for good performance

**Operating range:**
- Radio range: 1-10 km (communication limitation)
- RTK baseline: 0-10 km (accuracy limitation)
- Optimal RTK performance: <1 km baseline
- OpenRiverCam typical: 50-500 m baseline (well within optimal range)

**Base station setup:**
- Site selection: Open sky, stable ground, >10m from metal
- Antenna height measurement: Three measurements averaged to 0.5 cm
- Survey-in: 30-60 min, ≥15 satellites, PDOP ≤1.5
- Raw data logging: Entire session for PPP post-processing

**Rover measurement:**
- Position at survey point, verify RTK fix and quality gates
- Maintain pole vertical (bubble centered) during averaging
- 60-120 second averaging depending on point type
- Record pole height for each measurement
- Verify point saved successfully before moving

**Equipment needed:**
- Base: Receiver, antenna, tripod, radio, battery, computer/logger
- Rover: Receiver, antenna, survey pole, radio, battery, data collector
- Total system cost: $2,000-7,000 (accessible for humanitarian organizations)

**Critical success factors:**
- Base station must remain stable and operational throughout survey
- Rover requires continuous correction data to maintain fix
- Quality gates ensure reliable measurements
- Check points verify survey quality throughout the day

You now understand how base and rover stations work together to enable centimeter-accurate surveying. The next section explains RTK fix status in detail - the critical indicator of when you can survey.

---

**Next Section:** [5.5 RTK Fix Status](05-rtk-fix-status.md)
