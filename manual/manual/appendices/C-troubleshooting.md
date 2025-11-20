# Appendix C: Troubleshooting Guide

This appendix provides systematic troubleshooting procedures for common problems encountered during OpenRiverCam deployment and operation. Problems are organized by system category with symptoms, causes, diagnostic procedures, and solutions.

---

## How to Use This Guide

1. **Identify the symptom**: Find the problem category that matches what you observe
2. **Follow diagnostic steps**: Work through the checklist systematically
3. **Apply solutions**: Try solutions in the order presented (simplest first)
4. **Document and escalate**: If problem persists after trying all solutions, document what you tried and contact technical support

**General Troubleshooting Principles:**
- Start with the simplest explanation (loose cable before equipment failure)
- Change one thing at a time (so you know what fixed the problem)
- Document what you try (helps support team if you need to escalate)
- Check power first (surprisingly common cause of "equipment failure")

---

## 1. Survey Equipment Problems

### 1.1 RTK Rover Cannot Achieve Fix (Stuck in Float)

**Symptom:**
- RTK solution shows "FLOAT" for extended period (>20 minutes)
- Never transitions to "FIX" status
- Cannot survey because fix is required

**Common Causes:**
1. Insufficient satellites or poor geometry
2. Obstructed sky view
3. Multipath interference
4. Base station corrections not being received
5. Baseline too long (rover too far from base)
6. Ionospheric disturbance

**Diagnostic Steps:**

**Check 1: Verify base station is operational**
- Is base station powered on?
- Has base station completed survey-in? (Check in u-center or base display)
- Is base radio transmitting? (Check indicator lights)

**Check 2: Verify rover receiving corrections**
- SW Maps display: Check "Age of corrections"
- Should be <3 seconds
- If >10 seconds or "No corrections": Communication problem (see Section 1.4)

**Check 3: Check satellite count and geometry**
- SW Maps display: Check satellite count
- Need: ≥12 satellites for standard conditions, ≥10 for canal
- Check PDOP value: Should be ≤2.5 (standard) or ≤3.0 (canal)
- If satellites low: Move to location with better sky view

**Check 4: Assess sky view at rover location**
- Look up: Any obstructions above 15° from horizon?
- Trees, buildings, terrain blocking portions of sky?
- Move 10-20 meters to more open location and wait 5 minutes

**Check 5: Check for multipath sources**
- Large metal objects within 10 meters? (Vehicles, fences, equipment)
- Water surface nearby? (Reflections cause multipath)
- Buildings with reflective windows?
- Move 5-10 meters away from reflective surfaces

**Check 6: Verify baseline distance**
- How far is rover from base? (Check on map if unsure)
- Optimal: <1 km
- Good: 1-5 km
- Marginal: 5-10 km
- Poor: >10 km (fix very difficult)
- If baseline too long: Move closer to base or relocate base

**Solutions (in order of likelihood):**

**Solution 1: Wait patiently**
- Initial fix acquisition can take 5-20 minutes
- Satellite geometry changes over time (may improve)
- Wait 20-30 minutes before concluding fix is impossible

**Solution 2: Move to better location**
- Walk 10-20 meters to spot with more open sky
- Away from trees, buildings, metal structures
- Wait 5-10 minutes in new location

**Solution 3: Power cycle rover**
- Turn rover off, wait 30 seconds, power on
- Re-initialization sometimes resolves stuck float
- Wait 10-15 minutes after restart

**Solution 4: Check base station position**
- Visit base station physically
- Verify base has good sky view (not obstructed)
- Verify base survey-in completed successfully
- Check base radio is transmitting (indicator lights)

**Solution 5: Postpone survey**
- If ionospheric conditions poor (solar storm, geomagnetic disturbance)
- Fix may be impossible regardless of other factors
- Check space weather: https://www.swpc.noaa.gov/
- Reschedule survey for different day

**When to Escalate:**
- Tried all solutions
- Base station operational and nearby (<1 km)
- Good sky view, adequate satellites (>12)
- Age of corrections <3 seconds
- Still stuck in float after 30+ minutes
- **Contact:** Technical support with details (location, satellite count, PDOP, baseline distance)

---

### 1.2 RTK Fix Achieved but Poor Precision

**Symptom:**
- SW Maps shows "RTK FIX" status
- But precision estimates exceed requirements (>2cm H, >3cm V)
- Fix seems unstable (frequent loss and re-acquisition)

**Common Causes:**
1. Poor satellite geometry despite adequate count
2. Marginal sky view
3. High PDOP value
4. Weak signal strength
5. Multipath interference
6. Pole not level (introduces error)

**Diagnostic Steps:**

**Check 1: Verify fix is genuine**
- Fix duration: Should be >10 seconds
- If <10 seconds: May be false fix, wait longer

**Check 2: Check PDOP value**
- SW Maps display: Check PDOP
- Good: <2.0
- Acceptable: 2.0-2.5
- Marginal: 2.5-3.0
- Poor: >3.0
- High PDOP = poor geometry even if satellite count adequate

**Check 3: Check satellite count**
- Need ≥12 for reliable fix with good precision
- 10-12: Marginal, precision may suffer
- <10: Insufficient

**Check 4: Verify pole is level**
- Check bubble level: Bubble centered?
- Pole tilt introduces horizontal error
- 2m pole tilted 5° = 17cm horizontal error!

**Check 5: Observe precision over time**
- Does precision improve if you wait?
- Precision estimates update as more measurements collected
- Wait 30-60 seconds, check if precision improves

**Solutions:**

**Solution 1: Extend averaging time**
- Instead of 60 seconds, use 120 seconds
- Longer averaging reduces noise
- Accept slightly slower survey pace for better quality

**Solution 2: Move slightly**
- Shift position 2-3 meters
- May avoid local multipath or interference
- Re-establish fix, check if precision improves

**Solution 3: Use bipod or pole support**
- Holding 2m pole vertical for 60 seconds is tiring
- Fatigue causes drift even if bubble looks centered
- Bipod (two-leg support) or monopod helps stability
- Cost: $30-80, significantly improves results

**Solution 4: Wait for better satellite geometry**
- PDOP changes as satellites move across sky
- Wait 30-60 minutes, PDOP may improve
- Continue other survey tasks (marking GCPs, photography) while waiting

**Solution 5: Accept marginal precision for non-critical points**
- If precision 3-4 cm horizontal, 4-6 cm vertical
- Not ideal but usable for some applications
- Document lower precision in notes
- Consider re-surveying later if critical

**When to Escalate:**
- Fix maintained for >30 seconds
- PDOP <2.5, satellites >12
- Precision consistently >5 cm horizontal or >8 cm vertical
- Tried extending averaging, moving location
- **Contact:** Technical support - possible receiver calibration issue

---

### 1.3 Check Points Show Excessive Drift

**Symptom:**
- Check point measurements throughout day show >3cm horizontal or >4cm vertical drift
- Example: CP_START measured at 100.023m E, CP_END measured at 100.058m E (3.5cm drift = FAIL)

**This is a serious problem indicating survey data may be unreliable.**

**Common Causes:**
1. Base station moved during survey
2. Base station survey-in was poor quality
3. Equipment malfunction
4. Major atmospheric disturbance
5. Check point marker actually moved (unstable ground)

**Diagnostic Steps:**

**Check 1: Verify base station has not moved**
- Visit base station physically
- Check tripod position against original mark
- Has tripod settled into soft ground?
- Has tripod been bumped or disturbed?
- Check antenna is still securely mounted

**Check 2: Verify check point marker has not moved**
- Is check point on truly stable ground?
- Could marker have shifted? (Placed on soft soil, disturbed by people/animals)
- If uncertain, establish new check point on bedrock or structure

**Check 3: Review base station survey-in quality**
- What were survey-in conditions? (PDOP, satellite count, duration)
- If survey-in was marginal (high PDOP, few satellites, short duration)
- Poor survey-in leads to poor reference position

**Check 4: Check for systematic direction of drift**
- Are all measurements drifting in same direction?
- Systematic drift suggests base position error or movement
- Random scatter suggests poor precision (different cause)

**Solutions:**

**Solution 1: If base station has moved**
- **All survey data collected after movement is invalid**
- Note exact time base was disturbed (check base station logs)
- Invalidate all survey points collected after that time
- Re-survey those points
- Consider ending survey day and restarting next day

**Solution 2: If check point marker moved**
- Establish new check point on more stable location
- Concrete surface, bedrock, building foundation
- Re-measure new check point at intervals
- Original check point was not actually a problem if new CP stable

**Solution 3: If survey-in was poor quality**
- All data has degraded absolute accuracy
- Relative accuracy (between points) may still be OK
- PPP post-processing will improve absolute accuracy
- Continue survey if relative accuracy is priority
- Document issue in survey notes

**Solution 4: If atmospheric disturbance suspected**
- Check space weather: https://www.swpc.noaa.gov/
- If severe geomagnetic storm in progress
- All GNSS accuracy degraded globally
- Consider postponing survey to next day

**Solution 5: Equipment malfunction**
- If base station, rover, or antennas malfunctioning
- Swap suspected component with backup if available
- Test with backup equipment
- Send faulty equipment for service

**When to Escalate:**
- Check point drift exceeds limits
- Base station verified stable
- Check point verified stable
- No atmospheric disturbances
- **Contact:** Technical support immediately
- **Action:** Consider ending survey, do not rely on data until issue diagnosed

---

### 1.4 No RTK Corrections Received

**Symptom:**
- Rover shows "No corrections" or "Age of corrections >10 seconds"
- Rover solution status: Single (not Float or Fix)
- Cannot survey

**Common Causes:**
1. Base station radio not transmitting
2. Rover radio not receiving
3. Out of radio range
4. Terrain/obstacles blocking radio signal
5. Radio frequency mismatch
6. Base station offline or not in RTK mode

**Diagnostic Steps:**

**Check 1: Verify base station operational**
- Visit base station
- Is base powered on?
- Has survey-in completed? (Check display/software)
- Is base in "RTK base mode" (not still surveying-in)?

**Check 2: Check base radio transmission**
- Base radio powered on?
- Indicator lights showing transmission activity?
- Antenna connected to radio?
- If radio has diagnostics: Check transmission status

**Check 3: Check rover radio reception**
- Rover radio powered on?
- Antenna connected?
- Indicator lights showing reception activity?
- If radio has RSSI (signal strength): Is signal present?

**Check 4: Verify radio range**
- How far is rover from base?
- Line-of-sight between base and rover?
- Hills, buildings, dense vegetation blocking path?
- Try moving to higher ground or closer to base

**Check 5: Check radio configuration match**
- Base and rover radios on same frequency?
- Same baud rate?
- Same modulation (if configurable)?
- Reconfigure if mismatch suspected

**Solutions:**

**Solution 1: Power cycle radios**
- Turn off both base and rover radios
- Wait 30 seconds
- Power on base radio first, wait for initialization
- Power on rover radio, wait for connection

**Solution 2: Check antenna connections**
- Unscrew radio antenna, inspect connector
- Clean if dirty or corroded
- Re-attach firmly (hand tight, not forced)
- Test again

**Solution 3: Move closer to base**
- Walk toward base station until corrections received
- Establishes if range is the issue
- If corrections received when close: Range/line-of-sight problem
- May need to relocate base or use higher-power radios

**Solution 4: Test radio link with short baseline**
- Position rover within 50 meters of base with clear line-of-sight
- Should definitely receive corrections if radios functional
- If no corrections even at short range: Radio configuration or hardware fault

**Solution 5: Switch to cellular/NTRIP (if available)**
- If radio link cannot be established
- Use smartphone cellular connection for corrections
- Configure rover for NTRIP instead of radio
- Requires cell coverage and NTRIP account/server

**When to Escalate:**
- Radios configured correctly (frequency, baud rate match)
- Base confirmed transmitting (indicator lights)
- Rover within range (<1km) with line-of-sight
- Still no corrections received
- **Contact:** Equipment vendor for radio diagnostics/replacement

---

### 1.5 SW Maps Not Showing RTK Position

**Symptom:**
- RTK rover shows fix in its own display
- But SW Maps shows inaccurate position (5-10 meters off)
- Or SW Maps shows phone's internal GPS position

**Common Causes:**
1. GNSS Master not running or not providing mock location
2. Mock location permission not granted
3. USB connection between rover and Android device failed
4. SW Maps using internal GPS instead of external

**Diagnostic Steps:**

**Check 1: Verify GNSS Master running**
- Open GNSS Master app
- Is it receiving data from rover? (Position updating, satellite count shown)
- Is "Mock Location" enabled in GNSS Master settings?

**Check 2: Check Android mock location setting**
- Settings → Developer Options → Mock Location App
- Should be set to "GNSS Master"
- If Developer Options not visible: Enable first (tap Build Number 7 times)

**Check 3: Verify USB connection**
- USB OTG cable firmly connected to Android device and rover?
- Try different USB cable (cable failure common)
- Try different USB port if device has multiple

**Check 4: Check SW Maps GPS source**
- SW Maps → Settings → GPS
- Source should be "Device internal GPS" (which receives mock location from GNSS Master)
- Verify position is updating in SW Maps

**Solutions:**

**Solution 1: Restart GNSS Master**
- Close GNSS Master app completely
- Disconnect USB cable
- Reconnect USB cable
- Open GNSS Master
- Check if rover detected and position shows

**Solution 2: Reconfigure mock location**
- Settings → Developer Options → Mock Location App
- Select different app, then reselect GNSS Master
- Restart GNSS Master
- Test in SW Maps

**Solution 3: Replace USB cable**
- USB OTG cables fail frequently (especially in field conditions)
- Try known-good cable
- Carry 2-3 spare cables in field kit

**Solution 4: Restart Android device**
- Sometimes mock location service gets stuck
- Restart device, reconnect rover, reopen apps
- Often resolves mysterious issues

**Solution 5: Test with different app**
- Use Google Maps or another location app
- See if RTK position appears correctly
- If yes: SW Maps configuration issue
- If no: GNSS Master or mock location issue

**When to Escalate:**
- USB connection verified working (GNSS Master shows position)
- Mock location permission granted
- SW Maps still shows wrong position
- **Contact:** SW Maps support or Android device troubleshooting

---

## 2. Power System Problems

### 2.1 Solar System Not Charging Battery

**Symptom:**
- Battery voltage dropping over days
- System shuts down at night or after cloudy days
- Solar charge controller shows no charging current

**Common Causes:**
1. Solar panel disconnected or damaged
2. Charge controller failure
3. Battery fully charged (no charging needed)
4. Incorrect wiring
5. Panel shaded or dirty

**Diagnostic Steps:**

**Check 1: Measure solar panel voltage**
- With multimeter, measure voltage at panel output
- In full sun, should read ~18-22V for 12V system, ~36-44V for 24V
- If no voltage: Panel disconnected, damaged, or wire broken
- If low voltage (<15V for 12V panel): Panel shaded or faulty

**Check 2: Check panel connections**
- Connectors firmly attached?
- Wires damaged by weather, animals, UV exposure?
- Junction box on back of panel secure?

**Check 3: Check charge controller display**
- Does controller show panel voltage?
- Does it show battery voltage?
- Any error codes displayed?
- If controller has no display, check indicator LEDs

**Check 4: Measure battery voltage**
- 12V battery: Should be 12.0-12.8V (typical)
- If >13.0V: Battery fully charged (no charging needed - normal)
- If <11.5V: Battery severely discharged
- If <10.5V: Battery may be damaged

**Check 5: Check for shading or soiling**
- Is panel in full sun during midday?
- Any new obstructions? (Tree growth, structure built nearby)
- Is panel surface dirty? (Dust, bird droppings, leaves)

**Solutions:**

**Solution 1: Clean solar panel**
- Wipe panel surface with damp cloth
- Remove dust, dirt, bird droppings
- Can improve output 5-20% if dirty
- Do regularly (monthly in dusty environments)

**Solution 2: Re-seat connections**
- Disconnect and reconnect panel-to-controller wires
- Check polarity (+ to +, - to -)
- Tighten terminal screws firmly

**Solution 3: Bypass charge controller test**
- CAREFULLY connect panel directly to battery (correct polarity!)
- Only in daytime with sun
- Only for 1-2 minutes (battery can overcharge)
- If battery voltage rises: Controller is faulty
- If battery voltage does not rise: Panel or wiring faulty

**Solution 4: Replace damaged wiring**
- If wires corroded, broken, or damaged
- Use UV-resistant outdoor wire
- Proper gauge (12-14 AWG for most solar systems)
- Seal connections against moisture

**Solution 5: Replace charge controller**
- If controller not showing panel voltage
- No charging current despite good panel voltage
- Controller likely failed
- Replace with same voltage/current rating

**When to Escalate:**
- Panel producing voltage in sun
- Battery voltage OK
- Wiring verified correct
- Controller still not charging
- **Contact:** Solar equipment supplier for controller replacement

---

### 2.2 Battery Not Holding Charge

**Symptom:**
- Battery charges during day but depletes rapidly at night
- System runs only 1-2 hours after sunset (should run all night)
- Battery voltage drops quickly when loads connected

**Common Causes:**
1. Battery degraded/end of life
2. Battery undersized for load
3. Excessive load (equipment drawing more power than expected)
4. Battery damaged by deep discharge or overcharging
5. Poor connection causing voltage drop

**Diagnostic Steps:**

**Check 1: Measure battery voltage under load**
- With equipment running, measure battery voltage
- 12V battery: Should stay >11.8V under normal load
- If drops to <11.5V quickly: Battery weak or load too high

**Check 2: Measure battery voltage without load**
- Disconnect all loads
- Let battery rest 30 minutes
- Measure voltage
- 12V battery: Should be >12.4V if charged
- If <12.0V after resting: Battery has lost capacity

**Check 3: Check battery age**
- AGM battery: 3-5 year life typical
- Lithium battery: 8-10 year life typical
- If battery older than expected life: Replacement needed

**Check 4: Calculate actual load**
- Add up power consumption of all equipment
- Camera: Check actual power draw (may differ from specs)
- Network equipment, recording device, etc.
- Total draw more than battery capacity / expected runtime?

**Check 5: Check for short circuit or parasitic drain**
- Disconnect all loads
- Measure battery current with multimeter (should be near zero)
- If significant current with nothing connected: Short circuit or faulty controller

**Solutions:**

**Solution 1: Reduce load**
- Disable non-essential equipment at night
- Many cameras don't need to record at night (no useful data)
- Schedule recording only during daylight hours
- Can double battery runtime

**Solution 2: Add battery capacity**
- Parallel second battery of same type and rating
- Doubles capacity
- Ensure charge controller rated for increased capacity

**Solution 3: Replace battery**
- If battery >3 years old (AGM) or showing low voltage
- Replace with same or larger capacity
- Consider lithium upgrade (longer life, lighter, better performance)

**Solution 4: Upgrade solar panel**
- If battery drains because insufficient charging during day
- Larger panel = more charging
- Typical: 100W panel can sustain ~25-30W continuous load in good sun
- If running 40W load, need ~150-200W panel

**Solution 5: Fix poor connections**
- Clean battery terminals (corrosion reduces connection)
- Tighten all connections
- Poor connection causes voltage drop under load
- Use dielectric grease on terminals to prevent corrosion

**When to Escalate:**
- Battery voltage <11V even after full day of sun
- Battery less than 1 year old
- Load calculated within battery capacity
- Connections verified clean and tight
- **Contact:** Battery supplier - may be defective unit

---

### 2.3 Utility Power Issues

**Symptom:**
- Equipment not receiving power from grid
- Frequent power outages
- Equipment damage from power surges

**Common Causes:**
1. Circuit breaker tripped
2. GFCI outlet tripped
3. Loose wiring
4. Insufficient surge protection
5. Unreliable local grid

**Diagnostic Steps:**

**Check 1: Verify power at outlet**
- Use multimeter or plug in test device (phone charger, lamp)
- Is power present at outlet?
- If no power: Circuit breaker or wiring issue
- If power present: Equipment or power supply issue

**Check 2: Check circuit breaker panel**
- Breaker in "ON" position?
- Breaker may trip due to overload or ground fault
- Reset breaker, monitor if trips again

**Check 3: Check GFCI outlet**
- If outdoor outlet is GFCI (ground fault circuit interrupter)
- GFCI may trip due to moisture or ground fault
- Press "RESET" button on GFCI outlet
- If immediately trips again: Ground fault exists (serious - call electrician)

**Check 4: Check power supply/PoE injector**
- Is power supply outputting correct voltage?
- Measure with multimeter (should be 48V for PoE, 12V for DC cameras)
- If no output voltage: Power supply failed

**Solutions:**

**Solution 1: Install UPS (Uninterruptible Power Supply)**
- Provides battery backup during outages
- 500-1000VA unit provides 2-4 hours backup
- Protects against surges and power fluctuations
- Cost: $80-200
- Essential in areas with unreliable grid

**Solution 2: Install surge protector**
- Protects equipment from voltage spikes/lightning
- Commercial surge protector: $20-60
- Replace after major surge event (may sacrifice itself protecting equipment)

**Solution 3: Dedicated circuit**
- If sharing circuit with heavy loads (pumps, compressors)
- Ask electrician to install dedicated circuit for camera system
- Prevents tripping due to other equipment

**Solution 4: Improve wiring**
- If voltage drop over distance
- Use heavier gauge wire for long runs
- Verify connections tight and not corroded

**Solution 5: Switch to solar power**
- If grid unreliable and frequent outages
- Solar with battery backup may be more reliable
- See Appendix B for solar system specifications

**When to Escalate:**
- Power at outlet verified OK
- Equipment still not working
- Power supply verified outputting correct voltage
- **Contact:** Electrician for wiring issues; equipment vendor for device issues

---

## 3. Camera and Video Problems

### 3.1 Camera Not Producing Image

**Symptom:**
- Camera powered on but no video stream
- Cannot connect to camera via network
- Camera appears offline

**Common Causes:**
1. Network connection issue
2. Camera not powered (PoE issue)
3. IP address conflict or misconfiguration
4. Camera hardware failure
5. Firewall blocking access

**Diagnostic Steps:**

**Check 1: Verify camera has power**
- Check camera for LED indicators (usually near lens)
- If PoE: Verify PoE injector/switch has power and PoE enabled
- If DC power: Measure voltage at camera power connection (should be 12V ±10%)

**Check 2: Verify network connection**
- Is Ethernet cable connected firmly at both ends?
- Check cable for damage
- Try different cable (cable failure common)
- If switch has port LEDs: Check if port shows link

**Check 3: Ping camera IP address**
- From computer on same network, ping camera
- Command: `ping <camera_IP_address>`
- If ping succeeds: Network connection OK, camera software/configuration issue
- If ping fails: Network or power issue

**Check 4: Check IP address configuration**
- Camera may have lost IP configuration (reverted to default)
- Try accessing camera at default IP (check manual - often 192.168.1.64)
- May need to temporarily reconfigure computer IP to same subnet

**Check 5: Try camera discovery software**
- Most camera manufacturers provide discovery tool
- Hikvision: SADP tool
- Dahua: ConfigTool
- Scans network for cameras and shows IP addresses
- Can reset IP address to known value

**Solutions:**

**Solution 1: Power cycle camera**
- Disconnect power (PoE or DC)
- Wait 30 seconds
- Reconnect power
- Wait 2-3 minutes for camera to boot
- Try accessing again

**Solution 2: Replace Ethernet cable**
- Cable failure very common (especially outdoors)
- Try known-good cable
- If works with new cable: Old cable failed

**Solution 3: Reset camera to factory defaults**
- Most cameras have reset button (may be recessed)
- Press and hold 10-30 seconds while powering on
- Camera resets to factory IP address and password
- Reconfigure as needed

**Solution 4: Check PoE budget**
- If multiple PoE devices on one switch
- Switch may not provide enough power for all devices
- PoE switches have total power budget (e.g., 60W for 4-port switch)
- Disconnect other devices, see if camera powers on
- May need higher-capacity PoE switch

**Solution 5: Replace camera**
- If camera does not respond after reset
- No LED indicators even with power
- Likely hardware failure
- Replace camera with backup unit

**When to Escalate:**
- Power verified reaching camera (PoE or DC voltage correct)
- Network connection verified (other devices work on same port)
- Factory reset attempted
- Still no response from camera
- **Contact:** Camera manufacturer support - likely hardware failure

---

### 3.2 Poor Image Quality

**Symptom:**
- Image blurry, washed out, or too dark
- Cannot see water surface features clearly
- Image quality worse than expected

**Common Causes:**
1. Lens out of focus
2. Lens dirty (water spots, dust, condensation)
3. Incorrect exposure settings
4. Poor lighting conditions
5. Camera in wrong mode (night vision active during day)

**Diagnostic Steps:**

**Check 1: Inspect lens physically**
- Is lens clean?
- Water spots, dust, spider webs, bird droppings?
- Condensation inside housing?

**Check 2: Check focus setting**
- Many IP cameras have adjustable focus
- Access camera web interface
- Adjust focus while viewing live image
- Focus on object at similar distance as water surface

**Check 3: Check exposure settings**
- Is image too bright (washed out) or too dark?
- Automatic exposure may not be optimal for water surface
- Try adjusting exposure compensation (+/- settings)

**Check 4: Check IR cut filter setting**
- Day/night mode setting
- During day: IR filter should be IN (blocking IR light)
- If in night mode during day: Image may look washed out/purple
- Set to "Auto" or "Day" mode

**Check 5: Check time of day**
- Water surface best visible with oblique sunlight (early morning, late afternoon)
- Midday sun often creates glare
- May need to adjust camera angle or add lens hood

**Solutions:**

**Solution 1: Clean lens**
- Power off camera
- Wipe lens gently with microfiber cloth
- For stubborn spots: Lens cleaning solution (camera stores)
- Do not use abrasive materials (will scratch lens)
- Clean regularly (monthly or after dust storms)

**Solution 2: Adjust focus**
- Access camera via web browser (http://<camera_IP>)
- Find focus adjustment (may be manual slider or auto-focus button)
- Focus on staff gauge or fixed object at water surface distance
- Save settings

**Solution 3: Adjust exposure settings**
- Set exposure mode to "Manual" or "Custom"
- Reduce exposure if image too bright
- Increase exposure if image too dark
- Goal: Water surface features clearly visible without glare

**Solution 4: Add lens hood/sunshade**
- If direct sun hits lens (creates glare, washes out image)
- Install lens hood or sunshade
- DIY: PVC pipe section painted black
- Commercial: Camera-specific sunshades ($30-60)

**Solution 5: Reposition camera**
- If angle creates excessive glare
- Adjust camera tilt or rotation
- Oblique viewing angle usually better than straight-down
- May require re-surveying GCPs after repositioning

**When to Escalate:**
- Lens clean, focus adjusted
- Exposure settings optimized
- Image still poor quality
- **Contact:** Consider camera replacement (lens may be damaged) or **INFO NEEDED:** pyOpenRiverCam processing team for guidance on minimum acceptable image quality

---

### 3.3 Camera Network Connection Unstable

**Symptom:**
- Camera frequently goes offline
- Video stream drops intermittently
- Cannot reliably access camera remotely

**Common Causes:**
1. Poor Ethernet cable or connections
2. Network switch overheating or failing
3. IP address conflict
4. Inadequate PoE power delivery
5. Network congestion

**Diagnostic Steps:**

**Check 1: Check cable connections**
- Are connectors firmly seated?
- Check for corrosion (especially outdoor connections)
- Cable damaged by weather, animals, UV?

**Check 2: Test with shorter cable**
- Ethernet cable max length: 100 meters
- Long runs may have signal degradation
- Temporarily use short cable to test if camera stable
- If stable with short cable: Cable length or quality issue

**Check 3: Check network switch status**
- Is switch hot to touch? (Overheating can cause intermittent issues)
- Check switch LEDs: Solid or blinking erratically?
- Test camera on different switch port

**Check 4: Check for IP conflicts**
- Another device on network using same IP address?
- Symptom: Intermittent connectivity as devices fight for IP
- Assign camera static IP outside DHCP range
- Or use MAC address reservation in router

**Check 5: Monitor PoE power delivery**
- Some PoE switches show power per port
- Is camera drawing expected power? (Usually 4-10W)
- If power fluctuating: Power delivery issue

**Solutions:**

**Solution 1: Replace Ethernet cable**
- Use outdoor-rated CAT6 cable
- High-quality connectors (avoid bargain cables)
- Test with new cable before permanent installation
- Cable is often the culprit

**Solution 2: Add managed switch**
- Managed switch provides diagnostics (port errors, traffic)
- Can isolate problems
- Better quality than unmanaged switches
- Cost: $60-150 for 5-port PoE managed switch

**Solution 3: Use network extender**
- If cable run >100 meters
- PoE network extender repeats signal
- Adds another 100m range
- Cost: $40-80

**Solution 4: Improve outdoor connections**
- Use weatherproof junction boxes for connections
- Dielectric grease on connections
- Heat-shrink tubing over connections
- Prevents corrosion

**Solution 5: Add UPS to network equipment**
- Power fluctuations can reset switches
- UPS provides clean, stable power
- Prevents connection drops from brief power glitches

**When to Escalate:**
- Cable replaced with high-quality outdoor CAT6
- Connections verified clean and weatherproof
- Switch tested working with other devices
- Camera still unstable
- **Contact:** Network specialist to diagnose network infrastructure issues

---

## 4. Software and Processing Problems

### 4.1 pyOpenRiverCam Processing Errors

**Symptom:**
- Video processing fails or produces errors
- Velocity measurements seem unrealistic
- Processing completes but discharge values incorrect

**Common Causes:**
1. Poor quality video (inadequate tracers)
2. Incorrect ground control point coordinates
3. Incorrect cross-section data
4. Software configuration errors
5. Corrupted video files

**Diagnostic Steps:**

**Check 1: Verify video quality**
- Open video file in standard media player
- Are surface features (tracers) visible?
- Is image in focus?
- Is staff gauge readable?

**Check 2: Verify GCP coordinates**
- Are GCP coordinates in correct format? (X, Y, Z)
- Correct coordinate system (UTM zone matches survey)?
- Coordinates reasonable for location?

**Check 3: Check cross-section data**
- Cross-section points in correct order (bank to bank)?
- Elevations reasonable?
- Any duplicate points or errors?

**Check 4: Review processing configuration**
- Camera calibration parameters correct?
- Water level entered correctly?
- Velocity adjustment factor (usually 0.85) configured?

**Solutions:**

**Solution 1: Improve video quality**
- Adjust camera settings (focus, exposure)
- Ensure adequate lighting conditions
- Wait for better tracer conditions (more foam, debris)
- See Section 3.2 for image quality troubleshooting

**Solution 2: Verify GCPs in QGIS**
- Load GCP file in QGIS
- Visualize on map: Are points in reasonable locations?
- Check coordinate system matches video location
- Compare to satellite imagery if available

**Solution 3: Re-process cross-section data**
- Export cross-section from SW Maps
- Verify in spreadsheet: Any obvious errors?
- Plot in graphing software: Does profile look reasonable?
- Apply PPP corrections if not already done

**Solution 4: Start with simple test case**
- Use example video and data from pyOpenRiverCam documentation
- Verify software works with known-good data
- If test succeeds: Problem is with your data, not software
- If test fails: Software installation or environment issue

**Solution 5: Review pyOpenRiverCam documentation**
- Documentation: https://localdevices.github.io/pyorc/
- Examples and tutorials available
- Common issues addressed in FAQs

**When to Escalate:**
- Video quality verified good
- GCP and cross-section data verified correct
- Configuration checked against documentation
- Processing still fails or produces unrealistic results
- **Contact:** pyOpenRiverCam community (GitHub issues) or **INFO NEEDED:** Project technical support contact

---

### 4.2 SW Maps Data Export Issues

**Symptom:**
- Cannot export survey data from SW Maps
- Exported file missing data or corrupted
- Coordinate system incorrect in export

**Common Causes:**
1. SW Maps project corruption
2. Export format selected incorrectly
3. Coordinate system not set correctly in project
4. Insufficient storage space on device
5. Android permissions issue

**Diagnostic Steps:**

**Check 1: Verify project CRS**
- SW Maps → Project → Settings
- Check coordinate system (should be EPSG:32748 for Sukabumi or appropriate UTM zone)
- Verify units are meters

**Check 2: Check device storage**
- Settings → Storage
- Ensure adequate free space (>500MB)
- Clear cache if storage low

**Check 3: Try different export format**
- SW Maps supports multiple formats (CSV, GPX, Geopackage, GeoJSON)
- Try exporting as Geopackage (preserves CRS metadata)
- Also try CSV as simple backup

**Check 4: Check export settings**
- Are all layers selected for export?
- Geometry option: AS_XYZ for point clouds
- Are attributes included?

**Solutions:**

**Solution 1: Export project backup**
- SW Maps → Project → Backup
- Creates complete project backup
- Can be restored or opened on another device
- Email or upload to cloud storage

**Solution 2: Export layer-by-layer**
- Instead of exporting entire project
- Export each layer separately (GCPs, cross-sections, etc.)
- More reliable if project is large

**Solution 3: Use native Geopackage format**
- Most robust format
- Preserves coordinate system metadata
- Compatible with QGIS (needed for post-processing)

**Solution 4: Transfer via USB**
- If email/cloud export failing
- Connect device to computer via USB
- Copy SW Maps project folder directly
- Location: Internal Storage → SW Maps → Projects

**Solution 5: Reinstall SW Maps**
- If app corrupted or malfunctioning
- Export project backup first!
- Uninstall and reinstall SW Maps
- Restore project from backup

**When to Escalate:**
- Multiple export formats attempted
- Project verified not corrupted (can view data in SW Maps)
- Device has adequate storage
- Still cannot export usable data
- **Contact:** SW Maps support (support@swmaps.app)

---

## 5. Network and Connectivity Problems

### 5.1 No Cellular Connection for Remote Monitoring

**Symptom:**
- 4G/LTE router shows no signal or weak signal
- Cannot access camera remotely
- Data uploads failing

**Common Causes:**
1. No cellular coverage in area
2. Antenna not connected or poorly positioned
3. SIM card issue
4. Data plan expired or insufficient
5. APN settings incorrect

**Diagnostic Steps:**

**Check 1: Verify cellular coverage**
- Check carrier coverage map for deployment location
- Test with smartphone (same carrier as router SIM)
- If smartphone has no signal: Coverage issue (not equipment)

**Check 2: Check router status LEDs**
- Power LED: On (router has power)
- Signal LED: Indicates signal strength (usually 1-5 bars or colors)
- No signal: Antenna, coverage, or SIM issue

**Check 3: Check SIM card**
- Is SIM inserted correctly?
- Is SIM activated? (Try in smartphone)
- Is data plan active and not expired?
- Adequate data balance remaining?

**Check 4: Check APN settings**
- Router must be configured with carrier's APN
- Router admin page → Cellular settings → APN
- APN different for each carrier
- Contact carrier for correct APN if unsure

**Check 5: Check antenna**
- External antenna connected?
- Antenna positioned for best signal?
- Try repositioning antenna (higher, different orientation)

**Solutions:**

**Solution 1: Install external antenna**
- Internal router antenna often weak
- External 4G/LTE antenna: $30-80
- Mount antenna high (on pole or mast)
- Point toward nearest cell tower if known
- Can improve signal 10-20 dB

**Solution 2: Reposition router/antenna**
- Move to higher location
- Avoid metal enclosures (shield signal)
- Rotate antenna 90° (some polarizations work better)
- Even 1-2 meters higher can improve signal

**Solution 3: Switch carriers**
- If one carrier has no coverage, try another
- Get prepaid SIMs from 2-3 carriers
- Test signal strength
- Use carrier with best coverage at site

**Solution 4: Use WiFi connection instead**
- If nearby building has WiFi
- Negotiate WiFi access (humanitarian work often receives support)
- Use WiFi bridge to extend range if needed
- More reliable than cellular in many locations

**Solution 5: Accept intermittent connection**
- If remote monitoring is "nice to have" not critical
- Configure system to upload data when connection available
- Local storage during offline periods
- Manual data collection during site visits

**When to Escalate:**
- Cellular coverage verified exists (smartphone works)
- External antenna installed and positioned optimally
- SIM and APN settings verified correct
- Router still cannot connect
- **Contact:** Router manufacturer support or cellular carrier technical support

---

## 6. When to Seek Technical Support

### 6.1 Escalation Criteria

**Escalate to technical support when:**

1. You have followed all troubleshooting steps in this guide
2. Problem persists after trying all solutions
3. Problem affects critical functionality (cannot survey, cannot record video)
4. Equipment appears to have hardware failure
5. Data safety is at risk (survey data may be invalid)

**Before contacting support, prepare:**

- **Symptoms**: Exactly what is wrong (specific, measurable)
- **When it started**: Did something change? (weather event, configuration change, etc.)
- **What you tried**: List of troubleshooting steps already attempted
- **Equipment details**: Model numbers, firmware versions
- **Error messages**: Exact text of any error messages (screenshot if possible)
- **Site information**: Location, environmental conditions

### 6.2 Support Contacts

**Equipment-Specific Support:**

**RTK GPS Equipment:**
- ArduSimple: support@ardusimple.com (forum: https://www.ardusimple.com/question/)
- Emlid: support@emlid.com (forum: https://community.emlid.com/)
- CHC Nav, Trimble, Leica: Contact authorized dealer

**Camera Equipment:**
- Hikvision: Regional support centers
- Dahua: Regional support centers
- Axis, Bosch: Premium support included with purchase

**Software:**
- pyOpenRiverCam: GitHub issues (https://github.com/localdevices/pyorc/issues)
- SW Maps: support@swmaps.app

**Solar Equipment:**
- Renogy: support@renogy.com
- Victron Energy: https://www.victronenergy.com/support-and-downloads

**General OpenRiverCam Deployment Support:**
- **[INFO NEEDED: Project technical support contact]**
- **[INFO NEEDED: Community forum or mailing list]**

### 6.3 Preparing Equipment for Service

**If equipment must be returned for repair:**

1. **Backup all data** before removing equipment
2. **Document problem** in writing (for warranty claim)
3. **Clean equipment** (remove dirt, water exposure)
4. **Original packaging** if available (protects during shipping)
5. **Include all accessories** (antennas, cables, power supplies)
6. **Remove sensitive data** (SIM cards, recorded video, survey data)

---

## Troubleshooting Quick Reference

**Survey Issues:**
- No RTK fix → Check satellites (>12), PDOP (<2.5), corrections received (<3s age)
- Poor precision → Check pole level, extend averaging, check PDOP
- No corrections → Check base radio transmission, rover radio reception, range

**Power Issues:**
- Not charging → Check panel voltage (18-22V in sun), connections, controller
- Battery dying quickly → Check battery age (>3 years?), load calculation, replace if needed
- Utility power out → Check breaker, GFCI, install UPS

**Camera Issues:**
- No image → Check power (PoE or DC), network cable, IP address, reset camera
- Poor image → Clean lens, adjust focus and exposure, check day/night mode
- Unstable network → Replace Ethernet cable, check connections, test different port

**Software Issues:**
- Processing errors → Verify video quality, GCP coordinates, cross-section data
- Cannot export data → Use Geopackage format, export layer-by-layer, check storage space

**Network Issues:**
- No cellular signal → Install external antenna, reposition router, verify APN settings
- Remote access failing → Check router status, verify port forwarding, test with VPN

**General Approach:**
1. Check power and connections first
2. Check for recent changes (what was different when it last worked?)
3. Power cycle equipment
4. Try simplest solution first
5. Change one thing at a time
6. Document what you try
7. Escalate with complete information if problem persists

---

This troubleshooting guide covers the most common problems encountered during OpenRiverCam deployment and operation. For problems not covered here or issues that persist after following these procedures, contact technical support with detailed documentation of symptoms and troubleshooting steps attempted.
