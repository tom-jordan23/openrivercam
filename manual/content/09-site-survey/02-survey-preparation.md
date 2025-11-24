# 9.2 Survey Preparation (Day Before)

The distinction between efficient survey operations and problematic field experiences frequently originates from preparation quality. Systematic allocation of 2-3 hours on the day preceding survey operations for equipment preparation, software configuration, and logistics planning typically reduces field troubleshooting time by several hours while substantially increasing survey success rates (Wheaton et al., 2010; Turnipseed & Sauer, 2010).

This section presents comprehensive day-before preparation protocols derived from established RTK surveying procedures, explaining the technical rationale for each preparatory step and providing validated execution procedures based on geodetic surveying standards (Federal Geographic Data Committee, 2017).

Upon completion of this section, practitioners will possess understanding of equipment preparation and functional testing procedures, software configuration and integration validation protocols, power management and battery capacity strategies consistent with extended field operations, team coordination and role assignment frameworks based on professional survey practices, site access and permissions verification processes, meteorological assessment and contingency planning procedures, and the connections between preparation activities and field execution success metrics.

---

## Equipment Checklist

From SURVEY_PROCESS.md Section 2, the equipment check ensures everything works before you arrive at the remote site.

### Power Systems Preparation

**Base station power:**
```
☐ Base station: Full charge + backup battery
☐ Verify charging cable works (test connection before leaving unattended)
☐ Check battery health (hold charge? no swelling?)
☐ Backup battery fully charged
```

**Why this matters:**
The base station must remain powered for the entire survey session (6-12 hours for RINEX logging). A dead base station mid-survey invalidates all rover measurements afterward. You cannot continue surveying without base corrections.

**Testing procedure:**
1. Plug in base station and charge overnight before survey
2. Verify LED indicators show charging status correctly
3. Check battery level indicator (should show 100%)
4. Test backup battery connection (does it power the unit?)
5. Pack both batteries and charging cables

**If using external power bank:**
- Verify cable compatibility (USB-C, barrel connector, etc.)
- Charge power bank fully
- Test that base station runs from power bank
- Calculate capacity: base station draws ~2-5W, 20,000mAh power bank provides ~15+ hours

**Rover power:**
```
☐ Rover: Full charge
☐ Verify rover powers on and LED indicators work
☐ Test that rover holds charge (not draining when off)
```

The rover typically uses less power than base (no radio transmission) and only needs to last for active surveying (4-6 hours). Full charge usually sufficient, but bring charging equipment for extended sessions.

**Android device power:**
```
☐ Android: 100% charge
☐ Power bank fully charged (10,000+ mAh recommended)
☐ USB cable tested (charge + data transfer working)
```

The Android device runs GNSS Master and SW Maps continuously during survey. Screen on, GPS processing, app running = high power consumption (4-8 hours typical battery life).

**Power bank strategy:**
- Bring 10,000+ mAh power bank
- Keep device plugged into power bank during survey
- This extends operation to full day without recharge concerns

**All USB cables tested:**
```
☐ Base to laptop (for u-center configuration)
☐ Rover to Android (data transfer verified)
☐ Android charging cable
```

Not all USB cables support data transfer (some are charge-only). Test each cable before field day:
- Connect base to laptop with u-center running (verify data appears)
- Connect rover to Android with GNSS Master running (verify position data received)
- Connect Android to power bank (verify charging indicator)

**Pack spare cables** if you have them. Cables fail in the field, and you cannot survey without them.

### Physical Equipment Check

**Survey poles:**
```
☐ Primary survey pole (rover mounting)
☐ Backup survey pole (if available)
☐ Bipod for stability (optional but recommended)
☐ Verify pole height measurements marked clearly (tape measure against pole)
```

**Why two poles?**
If the primary pole's bubble level breaks or the pole becomes damaged, you need to continue surveying. A backup pole means equipment failure does not end the survey day.

**Pole height reference:**
Measure and mark pole height clearly with permanent marker or tape:
- Measure from pole tip (ground contact point) to antenna reference point (ARP)
- Mark at 0.5m, 1.0m, 1.5m, 2.0m for quick reference
- You will measure pole height at each survey point, so clear markings speed up field work

**Base station equipment:**
```
☐ Base tripod (stable, legs extend fully)
☐ Antenna cables (connect base to antenna)
☐ Radio antenna and cable (if using radio link)
☐ Verify all connectors tight (antenna connectors can loosen during transport)
```

**Critical: Connect antenna BEFORE powering on base.**
Powering GPS receivers without antenna connected can damage the receiver. This is emphasized in SURVEY_PROCESS.md Section 3.

**Field marking and measurement tools:**
```
☐ Steel tape measure (3m or longer, for pole height and antenna height)
☐ Permanent markers (mark GCPs, check points)
☐ Survey stakes or flags (mark locations)
☐ Spray paint (if marking on rock or pavement)
```

You will establish check points and mark GCP locations. Bring materials appropriate for your site:
- Soil: wooden stakes or flags
- Rock: spray paint or adhesive markers
- Pavement: chalk or spray paint
- Water edge: weighted markers or painted rocks

**Documentation materials:**
```
☐ Waterproof field notebook
☐ Pencils (work when wet, unlike pens)
☐ Camera or smartphone for photographs
☐ Printed copy of SURVEY_PROCESS.md procedures
```

Document everything during survey:
- Base station location and antenna height measurements
- Check point positions and measurements
- GCP locations and conditions
- Any deviations from standard procedure
- Weather and site conditions

Waterproof notebook is essential. River sites = humid, possibility of rain or water splash.

### Equipment Transport

**Organization strategy:**
- Base station + tripod + cables in one bag/case
- Rover + pole + bipod in one bag/case
- Android + power bank + cables in one bag/case
- Marking supplies + notebook + tools in one bag/case

**Organized packing means efficient setup.** You do not want to search through tangled cables while clock ticks during base station survey-in.

**Protect equipment:**
- Use padded bags or cases (equipment contains sensitive GPS receivers)
- Keep electronics dry (waterproof bags if rain possible)
- Secure small items (connectors, cables easily lost)

**Weight consideration:**
Complete RTK system weighs 5-10 kg. If site requires walking 1+ km, consider:
- Multiple trips (setup base station, return for rover)
- Team members carrying different components
- Backpack vs. carry bags (backpack more comfortable for distance)

---

## Software Setup and Testing

From SURVEY_PROCESS.md Section 1, software configuration must be completed at home where you have WiFi, desk space, and time to troubleshoot. Do not attempt first-time software setup in the field.

### Android and GNSS Master Setup

**Enable Developer Options and Mock Location:**

1. Settings → About Phone → Tap "Build Number" 7 times (activates developer mode)
2. Settings → Developer Options → Enable USB Debugging
3. Settings → Developer Options → Select Mock Location App → GNSS Master

**Why mock location?**
SW Maps needs GPS position to record survey points. The Android device's internal GPS is not accurate enough (3-10 meters). GNSS Master receives high-accuracy position from rover (1-3 cm via RTK) and provides it to SW Maps as if it were the device's GPS position ("mock location").

**GNSS Master configuration:**

```
☐ Install GNSS Master from Google Play Store
☐ Grant all permissions (Location: Allow all the time, Storage, Phone)
☐ Battery optimization: Don't optimize (prevents Android from killing app)
☐ Connection: Menu → Receiver → USB
☐ Mock Location: Menu → Mock Location → Enable
```

**Test GNSS Master:**
1. Connect rover to Android via USB OTG cable
2. Power on rover
3. Wait 30-60 seconds for rover to acquire satellites
4. GNSS Master should show satellite list and position
5. Open Google Maps - blue dot should appear (mock location working)

**If GNSS Master does not detect rover:**
- Check USB debugging enabled
- Try different USB cable (must support data)
- Check USB OTG adapter working (test with USB drive)
- Power cycle rover and Android
- Check rover is in correct output mode (NMEA on USB port)

**Do not skip this test.** If GNSS Master does not work at home, it will not work in the field.

### SW Maps Project Configuration

**Create new project:**

Project name: `Site_Name_YYYY_MM_DD` (e.g., `Ciliwung_River_2024_11_15`)

**Set coordinate system:**

From SURVEY_PROCESS.md Section 1:
```
Search: 32748 (or your site's UTM zone EPSG code)
Select: WGS 84 / UTM zone 48S
VERIFY: EPSG:32748, units = metre
```

**Critical: Verify the EPSG code is correct.**
Wrong coordinate system = coordinates in wrong location (hundreds of meters or kilometers off).

**GPS Settings configuration:**
```
☐ GPS Source: Device internal GPS (will receive mock location from GNSS Master)
☐ Averaging Method: By Time
☐ Default averaging time: 60 seconds (standard), 120 seconds (canal/challenging)
☐ Precision thresholds: H=2cm / V=3cm (standard), H=4cm / V=6cm (canal)
```

These thresholds match the quality gates from SURVEY_PROCESS.md. SW Maps will warn if precision exceeds thresholds.

**Create survey layers:**

From SURVEY_PROCESS.md Appendix B, create these point layers:
1. Camera FOV
2. Camera Location
3. Check Point Location
4. Ground Control Points
5. Discharge Cross Section
6. Level Cross Section
7. Water Level

**For each layer, define attributes:**

Example for "Ground Control Points" layer:
- **point_id** (text): Unique identifier (GCP1, GCP2, etc.)
- **description** (text): Location description ("Left bank, upstream from bridge")
- **marker_type** (text): What marks this point ("Painted rock", "Survey stake", etc.)
- **visibility** (text): Visible in camera? ("Yes", "Partial", "No")
- **surveyed_by** (text): Operator name
- **survey_time** (datetime): When surveyed

Attributes help document survey conditions and support quality control later.

### Integration Test

**This is the most important pre-survey test.**

Full system test: Base → Rover → GNSS Master → SW Maps

**Test procedure:**

1. **Set up base station:**
   - Connect antenna BEFORE powering on
   - Power on base
   - Connect base to laptop with u-center
   - Start base in survey-in mode (short test, 1-2 minutes)
   - Verify base is broadcasting corrections (RTCM messages on radio or serial)

2. **Set up rover:**
   - Connect antenna
   - Power on rover
   - Connect rover to Android via USB OTG

3. **Start GNSS Master:**
   - Should detect rover within 30 seconds
   - Should show satellite list
   - Mock location enabled

4. **Start SW Maps:**
   - Open project
   - Open "Ground Control Points" layer
   - Tap "Add Point"
   - GPS indicator should show position (from GNSS Master mock location)
   - Wait for rover to achieve RTK FIX (5-20 minutes with good sky view)

5. **Verify RTK FIX appears in SW Maps:**
   - Status should show "RTK FIX" or similar (depends on how GNSS Master passes status)
   - Precision estimates should show cm-level values
   - Satellite count should display

6. **Test point collection:**
   - With RTK FIX, tap "Save Point" in SW Maps
   - Verify point appears on map
   - Check attributes populated correctly
   - Verify coordinates look reasonable (correct UTM zone, values make sense)

**If integration test succeeds:**
You are ready for field survey. All software configured correctly, integration working.

**If integration test fails:**
Troubleshoot at home with WiFi and desk space. Common issues:
- Mock location not working (check Developer Options settings)
- SW Maps not receiving GPS (check GNSS Master mock location enabled)
- RTK FIX not achieved (need better sky view, or wait longer)
- Coordinates wrong (check SW Maps coordinate system settings)

**Do not go to field until integration test succeeds.**

### Software Configuration Backup

**After successful configuration:**
1. Export SW Maps project (creates .swmaps file with all layers and settings)
2. Save export to cloud storage (Google Drive, Dropbox, etc.)
3. Save copy to laptop
4. Document settings in field notebook (EPSG code, averaging times, thresholds)

If Android device fails in field or settings get corrupted, you can restore configuration quickly.

---

## Team Coordination

Surveying is typically a two-person job, though possible solo with experience.

### Role Assignment

**Primary operator (runs rover and data collection):**
- Carries rover on survey pole to each measurement point
- Monitors GNSS Master and SW Maps quality indicators
- Decides when conditions meet quality gates
- Initiates measurements and saves points
- Records observations in field notebook

**Secondary operator (base station monitoring and support):**
- Monitors base station operation throughout day
- Checks u-center logs periodically
- Assists with pole setup (holds bipod, measures pole height)
- Handles field notebook and camera for documentation
- Marks GCP locations and maintains check point markers

**Solo operation:**
- Set up base station, start survey-in
- Walk to first survey point with rover
- Monitor both GNSS Master/SW Maps (rover quality) and occasionally return to base to verify operation
- More time-consuming but feasible for experienced operators

### Training and Skill Development

**If team members are new to RTK surveying:**
- Review Chapter 5 concepts together
- Practice equipment setup at office before field day
- Conduct integration test together
- Assign experienced operator as primary, trainee as secondary
- Plan extra time for field day (learning curve)

**After 2-3 survey sessions:**
Most technical staff develop competence. RTK surveying is learnable, not a specialized professional skill.

### Communication Plan

**For remote sites:**
- Mobile phones likely have no signal
- Two-way radios useful if base and rover separated by distance
- Establish plan: "Return to base every 2 hours to verify operation"

**For accessible sites:**
- Base operator can communicate with rover operator easily
- Rover operator can periodically check base station status

**Emergency protocols:**
- What to do if equipment fails? (Spare equipment? Abort and reschedule?)
- What to do if weather turns bad? (Lightning safety, shelter locations)
- What to do if team member injured? (First aid kit, evacuation plan)

Discuss these before field day, not during an emergency.

---

## Site Permissions and Access

**Verify site access:**
```
☐ Permissions secured (landowner, community, authorities)
☐ Access route confirmed (roads, paths, river crossing)
☐ Access timing (gates locked? tides? river level?)
☐ Security concerns addressed (equipment theft? personal safety?)
```

**Permissions documentation:**
Bring written permission or contact information for landowner/community leader. If challenged while setting up equipment at river site, you need to explain quickly and credibly what you are doing.

**Access timing:**
- Will you arrive before gates open? (Need key or different plan?)
- Is river fordable, or do you need boat? (Current water level vs. expected level on survey day?)
- Tidal areas: Can you access at planned time, or does tide block access?

**Security considerations:**
- Will you leave equipment unattended (base station during survey)? Is theft a concern?
- Is site safe for team (steep slopes, slippery rocks, fast current)?
- Local security issues (civil unrest, wildlife hazards)?

Address security concerns before field day. Options:
- Hire local security guard to watch base station
- Coordinate with local community (they watch equipment as friendly observers)
- Schedule survey when team member can stay at base throughout
- Choose base station location not visible from road (reduce theft temptation)

---

## Weather Forecast Check

**From SURVEY_PROCESS.md:**
Check weather forecast for survey day. Ideal conditions:
- No rain (keeps equipment dry, reduces atmospheric delays)
- Minimal cloud cover (does not affect satellites, but may affect camera sample video)
- Moderate temperatures (extreme heat causes atmospheric shimmer)
- Light winds (rover pole stability)

**RTK works in light rain** but:
- Equipment wet = risk of damage
- Operator wet = miserable experience
- Water on Android screen = difficulty operating SW Maps
- Multipath increases (wet ground reflects signals more)

**Heavy rain or thunderstorms:**
- Lightning hazard (do not stand in open field holding 2-meter metal pole)
- POSTPONE survey if thunderstorms forecast

**Backup plan:**
- If weather forecast shows rain, consider rescheduling
- If rain possible but not certain, bring rain gear and waterproof equipment covers
- Have backup date identified in case survey must be postponed

**Heat management:**
- Extreme heat (35°C+) causes atmospheric shimmer (affects both RTK and camera imagery)
- Schedule survey for early morning (cooler, better atmospheric conditions)
- Bring water and sun protection for team

---

## Backup Plans

**Equipment failure scenarios:**

**Base station failure:**
- Backup plan: Abort survey, reschedule (cannot survey without base corrections)
- Prevention: Test base thoroughly day before

**Rover failure:**
- Backup plan: If backup rover available, switch equipment; otherwise abort
- Prevention: Test rover thoroughly day before

**Android device failure:**
- Backup plan: If backup device available (second phone/tablet with SW Maps configured), switch; otherwise abort
- Prevention: Fully charge, test integration

**Cable failure:**
- Backup plan: Switch to spare cable (bring spares!)
- Prevention: Test all cables, pack spares

**Power failure:**
- Backup plan: Backup battery for base, power bank for Android
- Prevention: Full charge all batteries day before

**Radio link failure (if using radio corrections):**
- Backup plan: Troubleshoot antenna positioning, check radio power
- If cannot fix: Abort survey (rover needs corrections to achieve fix)
- Prevention: Test radio link during integration test

**Weather contingency:**
- Backup date identified and communicated to team
- Transportation and access can be rescheduled
- No deadline pressures forcing unsafe surveying in poor conditions

**The principle:**
Better to postpone and conduct high-quality survey than to rush and collect poor data. Poor survey data wastes effort during processing and produces unreliable transformation.

---

## Pre-Survey Checklist Summary

**Day before survey, systematically check:**

**Power:**
- [ ] Base station fully charged + backup battery
- [ ] Rover fully charged
- [ ] Android device fully charged + power bank
- [ ] All USB cables tested

**Equipment:**
- [ ] Survey poles + bipod
- [ ] Base tripod + antenna cables
- [ ] Tape measure + markers + notebook
- [ ] All equipment organized in bags/cases

**Software:**
- [ ] GNSS Master configured and tested
- [ ] SW Maps project created with correct EPSG code
- [ ] Survey layers created with attributes
- [ ] Integration test successful (base → rover → GNSS Master → SW Maps → RTK FIX → save point)
- [ ] Software configuration backed up

**Logistics:**
- [ ] Team roles assigned
- [ ] Site access permissions confirmed
- [ ] Weather forecast checked
- [ ] Backup plans identified
- [ ] Transportation arranged
- [ ] Emergency contacts and first aid kit

**Documentation:**
- [ ] Printed copy of SURVEY_PROCESS.md
- [ ] Waterproof field notebook + pencils
- [ ] Camera for photo documentation

**Knowledge:**
- [ ] Team has reviewed Chapter 5 concepts
- [ ] Team has reviewed SURVEY_PROCESS.md procedures
- [ ] Team understands quality gates and thresholds
- [ ] Team knows how to recognize RTK FIX status

**Time estimate:**
Complete day-before preparation: 2-3 hours

This time investment typically saves 1-2 hours in the field (no troubleshooting, no forgotten equipment, no configuration delays) and dramatically increases success rate.

---

## Connection to Survey Day Execution

**Preparation enables execution.**

With thorough preparation:
- Arrive at site with all equipment working and tested
- Setup proceeds smoothly (no surprises)
- Software ready to collect data immediately
- Team knows roles and procedures
- Contingency plans ready if problems occur

Without preparation:
- Discover equipment failures in field (too late to fix)
- Spend hours troubleshooting software integration
- Team confused about procedures
- No backup plans when problems occur
- Survey day becomes frustrating and may fail

**The survey success rate correlation:**
Teams that invest 2-3 hours in day-before preparation have >90% survey success rate.
Teams that skip preparation have <50% survey success rate and much longer field time.

**Your choice is clear:** Invest preparation time, execute smoothly.

The following sections (9.3-9.6) assume you have completed this preparation and arrive at the field site with tested, working equipment and configured software. If you skip preparation, those field procedures will be much more difficult.

---

## Summary: Key Day-Before Tasks

**Equipment preparation:**
- Charge all batteries fully (base, rover, Android, power banks)
- Test all cables (data transfer, not just charging)
- Organize equipment in bags for efficient setup
- Bring backup batteries, spare cables, marking supplies

**Software configuration:**
- Set up GNSS Master with mock location enabled
- Create SW Maps project with correct EPSG code
- Configure GPS settings (averaging time, precision thresholds)
- Create survey layers with attributes

**Integration testing:**
- Full system test: base → rover → GNSS Master → SW Maps
- Verify RTK FIX appears and can collect points
- Test point collection and coordinate verification
- Do not go to field until integration test succeeds

**Logistics planning:**
- Assign team roles (primary operator, secondary support)
- Confirm site access permissions and routes
- Check weather forecast and have backup date
- Prepare emergency and contingency plans

**Time required:**
2-3 hours for complete preparation

**Success impact:**
Proper preparation increases survey success rate from <50% to >90% and reduces field time by 1-2 hours.

Invest the preparation time. Your survey day will thank you.

---

**Next Section:** [9.3 Ground Control Selection and Placement](03-ground-control-placement.md)
