# RC-Box Mechanical Design Questionnaire

## Executive Summary
This document outlines critical design questions that must be answered before finalizing the RC-Box enclosure and mechanical systems. Questions are organized by system category and prioritized by impact on design decisions.

---

## 1. ENVIRONMENTAL PROTECTION & IP RATING

### 1.1 Operating Environment Specifications
- [ ] What is the minimum/maximum operating temperature range? (-40°C to +60°C? Wider?)
- [ ] What is the minimum/maximum storage temperature range?
- [ ] What is the maximum humidity exposure (continuous vs. intermittent)?
- [ ] What is the expected UV exposure duration (hours/day over equipment lifetime)?
- [ ] Are there specific chemical exposure risks (salt spray, agricultural runoff, industrial pollutants)?
- [ ] What is the maximum altitude for deployment?
- [ ] Are there specific regions/climates that represent worst-case scenarios we should design for?

### 1.2 Ingress Protection Requirements
- [ ] What IP rating is required? (IP65, IP67, IP68?)
- [ ] Do we need submersion protection, or just rain/spray protection?
- [ ] If submersion: to what depth and for how long?
- [ ] What is the maximum expected water pressure (from rain, spray, or flooding)?
- [ ] Do we need protection against windblown dust/sand in desert environments?
- [ ] What particle size must be excluded (fine dust vs. coarse debris)?

### 1.3 Weatherproofing Strategy
- [ ] Gasket material preference (silicone, EPDM, neoprene, Viton)?
- [ ] Should the enclosure be vented (breathable membrane) or completely sealed?
- [ ] If vented: what are the desiccant/breather requirements and replacement schedule?
- [ ] Do we need pressure equalization (barometric vent)?
- [ ] What is the acceptable condensation level inside the enclosure?
- [ ] Should we include humidity sensors/indicators?

---

## 2. THERMAL MANAGEMENT

### 2.1 Heat Generation
- [ ] What is the total power dissipation under maximum load (Raspberry Pi 5 + accessories)?
- [ ] What is the typical duty cycle (continuous operation vs. intermittent)?
- [ ] What are the peak thermal loads during video capture/processing?
- [ ] Does the PiJuice/PiSugar generate significant heat during charging?

### 2.2 Cooling Strategy
- [ ] Is passive cooling (heat sinks + conduction) sufficient, or do we need active cooling?
- [ ] If active cooling: fans acceptable, or do they compromise waterproofing/reliability?
- [ ] What is the maximum acceptable internal temperature?
- [ ] Should we use thermal interface materials (TIM) between components and enclosure?
- [ ] What color should the external enclosure be to minimize solar heat gain (white/light gray)?
- [ ] Do we need internal reflective/insulative barriers?

### 2.3 Cold Weather Operation
- [ ] What is the minimum starting temperature for the electronics?
- [ ] Do we need heaters or thermal blankets for cold climates?
- [ ] If heated: what is the power budget and control strategy?
- [ ] Do we need battery protection for low-temperature operation?
- [ ] What is the cold-soak duration the system must survive before startup?

### 2.4 Thermal Design Details
- [ ] Should the enclosure be metal (for heat dissipation) or plastic (for insulation)?
- [ ] If metal: aluminum, stainless steel, or coated steel?
- [ ] If plastic: ABS, polycarbonate, fiberglass, or composite?
- [ ] What wall thickness is needed for structural + thermal requirements?
- [ ] Should we thermally isolate the battery from other components?

---

## 3. ENCLOSURE MATERIALS & CONSTRUCTION

### 3.1 Material Selection
- [ ] Primary enclosure material: aluminum, polycarbonate, ABS, fiberglass, or NEMA-rated commercial enclosure?
- [ ] What are the UV resistance requirements (years of exposure)?
- [ ] What impact resistance is required (IK rating or joule rating)?
- [ ] Should materials be flame-retardant (UL94 rating)?
- [ ] Are there restrictions on materials for shipping/customs (e.g., wood packaging materials)?
- [ ] Do materials need to be RoHS/REACH compliant?

### 3.2 Manufacturing Approach
- [ ] Custom fabrication vs. modified commercial enclosure (e.g., Pelican, Hammond, Bud)?
- [ ] If custom: injection molded, rotationally molded, machined, or fabricated?
- [ ] What production volume justifies tooling costs?
- [ ] Should we design for multi-stage assembly or single-piece construction?
- [ ] Are there local manufacturing capabilities we should leverage?

### 3.3 Enclosure Dimensions
- [ ] What is the minimum internal volume needed for all components?
- [ ] What clearances are needed around components for:
  - [ ] Heat dissipation?
  - [ ] Serviceability?
  - [ ] Cable routing?
  - [ ] Future expansion?
- [ ] What is the maximum size/weight for:
  - [ ] One-person installation?
  - [ ] Shipping in standard containers?
  - [ ] Air freight restrictions?
- [ ] Should the design be modular (stackable/expandable sections)?

### 3.4 Surface Treatment & Finish
- [ ] What coating/finish is needed (powder coat, anodize, UV-resistant paint)?
- [ ] Should the exterior be textured or smooth?
- [ ] Are there visibility/color requirements (safety orange, camouflage, neutral)?
- [ ] Should labels/markings be engraved, embossed, or adhesive?
- [ ] Do we need anti-graffiti coatings?

---

## 4. MOUNTING SYSTEM DESIGN

### 4.1 Pole/Mast Specifications
- [ ] What pole diameter range must be accommodated (50mm-150mm? Wider?)?
- [ ] What pole materials (steel, aluminum, wood, concrete, fiberglass)?
- [ ] What pole shapes (round, square, triangular, irregular)?
- [ ] What is the maximum pole installation height?
- [ ] Are there maximum lateral load specifications we must provide to users?
- [ ] Should we design for horizontal surfaces (walls, bridges) as well as vertical poles?

### 4.2 Mounting Hardware
- [ ] Clamp style: U-bolt, band clamp, split collar, or quick-release?
- [ ] Material: stainless steel, galvanized steel, aluminum, or composite?
- [ ] Should mounting be tool-free or require tools?
- [ ] If tools required: what tools should be included/specified?
- [ ] How many mounting points are needed for stability?
- [ ] Should the mount be adjustable after installation without removing the enclosure?

### 4.3 Orientation & Adjustment
- [ ] What angular adjustment range is needed (pan, tilt, roll)?
- [ ] Should adjustments be continuous or indexed (discrete positions)?
- [ ] How is angular position locked (set screws, friction locks, ratchets)?
- [ ] Should we include angle indicators or scales?
- [ ] Can adjustment be done with enclosure in place, or must it be removed?
- [ ] What is the adjustment frequency (one-time setup vs. regular repositioning)?

### 4.4 Load & Vibration Analysis
- [ ] What is the total system weight (enclosure + electronics + cameras + mounting)?
- [ ] What is the center of gravity location?
- [ ] What wind loading must the mount withstand (steady-state and gusts)?
- [ ] If using a camera arm: what is the moment arm length and resulting cantilever load?
- [ ] What vibration frequencies/amplitudes are expected (wind, traffic, water flow)?
- [ ] Do we need vibration isolation/damping?
- [ ] Should we conduct finite element analysis (FEA) or physical load testing?

### 4.5 Anti-Theft & Security
- [ ] Should mounting hardware be tamper-resistant or security fasteners?
- [ ] Do we need physical locks, security cables, or alarm sensors?
- [ ] Should the enclosure be inconspicuous or clearly marked as monitoring equipment?
- [ ] Are there local regulations about equipment marking/labeling?

---

## 5. CAMERA SYSTEM MECHANICAL DESIGN

### 5.1 Camera Housing
- [ ] Should cameras be in separate housings or integrated into main enclosure?
- [ ] If separate: what IP rating for camera housings?
- [ ] Should we use commercial camera housings or custom design?
- [ ] What lens size/focal length drives the housing window size?
- [ ] What window material (glass, polycarbonate, acrylic)?
- [ ] What optical clarity requirements (transmission %, distortion limits)?
- [ ] How do we prevent window fogging, condensation, or UV degradation?
- [ ] Should windows have hydrophobic coating or heaters?

### 5.2 Camera Mounting & Adjustment
- [ ] How are cameras attached (ball joint, gimbal, fixed angles, pan-tilt mechanism)?
- [ ] What adjustment range is needed (vertical angle, horizontal angle, rotation)?
- [ ] Should adjustments be marked/measured (angle scales, click-stops)?
- [ ] Can cameras be adjusted independently or linked together?
- [ ] What is the mechanism for locking camera position?
- [ ] How do we ensure repeatable positioning after service?
- [ ] Should we include alignment aids (laser pointers, sighting lines)?

### 5.3 Camera Orientation Documentation
- [ ] How do we capture/record the intended orientation during installation?
  - [ ] Built-in inclinometers/accelerometers?
  - [ ] Mechanical angle indicators?
  - [ ] Photo documentation templates?
  - [ ] Software-based calibration process?
- [ ] How do we communicate orientation to the software?
- [ ] Should rotation settings be preserved if cameras are removed/reinstalled?

### 5.4 Camera Protection
- [ ] What impact resistance is needed for camera housings?
- [ ] Should cameras have sunshades or rain hoods?
- [ ] Do we need protective covers for transport/storage?
- [ ] How do we prevent bird strikes, insect intrusion, or debris accumulation?
- [ ] Should we include cleaning access (removable covers, wiper mechanisms)?

---

## 6. CABLE MANAGEMENT & PASS-THROUGHS

### 6.1 Cable Entry Strategy
- [ ] How many cables enter the enclosure (power, cameras, antennas, future expansion)?
- [ ] Cable gland type: compression (PG/M series), pass-through with potting, or bulkhead connectors?
- [ ] Should cable entries be on top, bottom, or sides of enclosure?
- [ ] What cable diameter range must be accommodated?
- [ ] Should we use sealed connectors (IP67 M12/M8) or field-terminated cables with glands?

### 6.2 Internal Cable Routing
- [ ] How are cables organized inside the enclosure (cable ties, raceways, Velcro)?
- [ ] What strain relief is needed at entry points and component connections?
- [ ] Should we provide cable length management (service loops, coiling)?
- [ ] How do we prevent cables from interfering with heat dissipation?
- [ ] Should cables be color-coded or labeled?

### 6.3 External Cable Protection
- [ ] What protection is needed for cables between enclosure and cameras?
  - [ ] Conduit, spiral wrap, braided sleeving, or UV-resistant jacketing?
- [ ] How are cables secured to the pole/mounting structure?
- [ ] What is the minimum bend radius for camera cables?
- [ ] Should cables be replaceable without opening the main enclosure?
- [ ] Do we need drip loops or water-shedding features?

### 6.4 Connector Specifications
- [ ] Should camera connections use USB-A, USB-C, or custom connectors?
- [ ] What is the connector retention force requirement?
- [ ] Should connectors be locking type (bayonet, threaded, snap)?
- [ ] What connector IP rating is needed?
- [ ] Should we use military-spec connectors for durability?
- [ ] Do we need EMI/RFI shielding on connectors?

---

## 7. VISUAL INDICATORS & USER INTERFACE

### 7.1 Status Indicator Requirements
- [ ] What information must be visible from ground level?
  - [ ] Power on/off?
  - [ ] Recording status?
  - [ ] Error conditions?
  - [ ] Network connectivity?
  - [ ] Battery level?
  - [ ] Maintenance mode?
- [ ] What is the maximum viewing distance for indicators?
- [ ] What is the minimum indicator size/brightness for daytime visibility?

### 7.2 Indicator Implementation
- [ ] LED type: single color, multi-color, addressable RGB?
- [ ] LED location: top of enclosure, multiple sides, dedicated tower?
- [ ] Should we use light pipes to route indicator light?
- [ ] Do we need fresnel lenses or diffusers for wide viewing angle?
- [ ] Should indicators be weatherproof standalone units or behind windows?
- [ ] What is the flash/blink pattern strategy for different states?
- [ ] Should we include audible indicators (buzzer, beeper)?

### 7.3 Visibility & Accessibility Trade-offs
- [ ] How do we balance indicator visibility with weatherproofing?
- [ ] Should indicators be recessed or flush-mount?
- [ ] Do indicators create light leak or ingress points?
- [ ] What is the power budget for indicators (battery impact)?

---

## 8. HARDWARE SWITCHES & CONTROLS

### 8.1 Switch Requirements
- [ ] How many switches are needed?
  - [ ] Power on/off?
  - [ ] Maintenance mode?
  - [ ] WiFi hotspot enable?
  - [ ] Mode selection (maintenance/cycling/recording)?
- [ ] Should switches be momentary or maintained (toggle/rocker)?
- [ ] Should switches be multi-position (rotary selector)?

### 8.2 Switch Protection & Access
- [ ] What IP rating is needed for switches?
- [ ] Should switches be behind access doors, under caps, or always exposed?
- [ ] If access doors: hinged, threaded caps, or snap-on covers?
- [ ] Should switches be recessed to prevent accidental activation?
- [ ] Do we need lockout/tagout capability?
- [ ] Should switches require tools to operate (theft/tamper prevention)?

### 8.3 Switch Feedback
- [ ] Should switches have tactile feedback (click, detent)?
- [ ] Should switches have visual indicators (illuminated, label windows)?
- [ ] How are switch positions labeled (engraved, printed, molded)?
- [ ] Should labels be multi-language or iconographic?
- [ ] Do we need a decision tree/flowchart on the enclosure for switch operation?

### 8.4 Ergonomics
- [ ] Can switches be operated with gloves?
- [ ] What force is required to actuate switches?
- [ ] Are switches reachable with enclosure mounted at maximum height?
- [ ] Should we include a magnetic tool or pole-mounted actuator for high installations?

---

## 9. FIELD SERVICEABILITY

### 9.1 Access & Disassembly
- [ ] What components need regular access (battery, storage, connectors)?
- [ ] What components need occasional access (Raspberry Pi, power board)?
- [ ] Should there be multiple access points or one main door?
- [ ] What fastener type: captive screws, quarter-turn, snap latches, or hinged?
- [ ] How many fasteners are acceptable (balance security vs. service time)?
- [ ] Should we include a tool storage compartment?

### 9.2 Tool Requirements
- [ ] What tools are needed for field service?
  - [ ] Screwdrivers (sizes and types)?
  - [ ] Wrenches (metric or imperial)?
  - [ ] Specialty tools (torx, hex, spanner)?
- [ ] Should tools be included with each unit or provided separately?
- [ ] Should the enclosure be serviceable with a standard multi-tool?
- [ ] Do we need a dedicated service kit with specialized tools?

### 9.3 Component Replacement
- [ ] Should internal components mount on a removable tray/backplane?
- [ ] How are components secured (standoffs, clips, rails, Velcro)?
- [ ] Can components be replaced without removing cables?
- [ ] Should we use keyed connectors to prevent mis-assembly?
- [ ] What is the maximum time budget for common service tasks?
  - [ ] Battery replacement: ___ minutes?
  - [ ] Camera replacement: ___ minutes?
  - [ ] Full unit replacement: ___ minutes?

### 9.4 Spare Parts Strategy
- [ ] What spare parts should be included with each deployment?
  - [ ] Fuses, terminals, fasteners?
  - [ ] Gaskets, seals, cable glands?
  - [ ] Cables, connectors?
  - [ ] How many of each?
- [ ] Should spare parts be stored in the main enclosure or separate kit?
- [ ] What is the expected lifetime consumption of consumables?
- [ ] Should we include a service log/checklist in the enclosure?

### 9.5 Documentation & Labeling
- [ ] Should we include internal labeling/diagram of components?
- [ ] Should we laminate reference cards inside the enclosure?
- [ ] How do we identify cable connections (labels, color codes, connectors)?
- [ ] Should we photograph the "as-shipped" configuration for each unit?
- [ ] What QR codes or serial numbers are needed for traceability?
- [ ] Should we include a quick-start guide in a weatherproof pouch?

---

## 10. SHIPPING & HANDLING

### 10.1 Shipping Container Design
- [ ] Should the unit ship in a custom case (Pelican-style) or cardboard/wood crate?
- [ ] What drop height must the package survive (ISTA testing standards)?
- [ ] Should the shipping case be reusable for storage or transport between sites?
- [ ] What is the maximum shipping weight/size for air freight or remote delivery?
- [ ] Should we design for palletized shipping or individual units?

### 10.2 Packaging Protection
- [ ] What cushioning material (foam, bubble wrap, air pillows, corrugated inserts)?
- [ ] Should custom foam be cut for each component?
- [ ] Should cameras be pre-installed or shipped separately?
- [ ] Should cables be pre-attached or loose?
- [ ] Do we need desiccant packets for humidity control during shipping?
- [ ] What environmental data loggers (shock, temperature) should be included?

### 10.3 Assembly State
- [ ] Should units ship fully assembled, partially assembled, or as kit?
- [ ] If kit: what assembly is required in field (balance shipping volume vs. field labor)?
- [ ] Should cameras be pre-calibrated or calibrated in field?
- [ ] Should mounting hardware be pre-installed or separate?
- [ ] What is the acceptable field assembly time?

### 10.4 Documentation & Accessories
- [ ] What must ship with each unit?
  - [ ] Installation guide?
  - [ ] Mounting hardware?
  - [ ] Tools?
  - [ ] Consumables?
  - [ ] Spare parts?
  - [ ] Test equipment?
- [ ] Should documentation be printed, USB drive, or QR code link?
- [ ] What languages are needed for documentation?

### 10.5 Storage & Warehousing
- [ ] What storage temperature/humidity limits must packaging withstand?
- [ ] What is the expected storage duration before deployment?
- [ ] Should packaging be stackable?
- [ ] How should units be marked for inventory (labels, barcodes, RFID)?
- [ ] Are there hazmat or battery shipping regulations we must comply with?

---

## 11. POWER SYSTEM INTEGRATION

### 11.1 Power Input
- [ ] What input voltage range (battery-only, solar, commercial power, multi-source)?
- [ ] If commercial power: what plug type (region-specific) or hardwired connection?
- [ ] If solar: panel size, mounting location (on enclosure or separate)?
- [ ] Should we include a manual battery disconnect switch?
- [ ] What overcurrent protection (fuses, breakers, PTC)?

### 11.2 Battery Access
- [ ] Should batteries be easily accessible (external door) or protected (internal)?
- [ ] What is the expected battery replacement frequency?
- [ ] Should we use off-the-shelf batteries (18650, pouch) or custom packs?
- [ ] Do we need a battery management system (BMS) with external monitoring?
- [ ] Should battery status be visible externally?

### 11.3 Power Cable Routing
- [ ] Where does power enter the enclosure (bottom, side, dedicated port)?
- [ ] Should power cable be detachable or hardwired?
- [ ] What strain relief is needed for power cables?
- [ ] How do we protect low-voltage DC from short circuits?

---

## 12. REGULATORY & SAFETY COMPLIANCE

### 12.1 Certifications Needed
- [ ] What electrical safety standards (UL, CE, CSA, RCM)?
- [ ] What environmental standards (IP, NEMA, IK ratings)?
- [ ] What EMC/EMI compliance is needed?
- [ ] Are there wireless/RF certifications needed (FCC, RED, IC)?
- [ ] What transportation certifications (UN38.3 for batteries)?

### 12.2 Safety Markings
- [ ] What warning labels are required (electrical, battery, UV exposure)?
- [ ] Should we include pictograms for international deployments?
- [ ] What installation warnings are needed (height, falling hazard)?
- [ ] Do we need voltage ratings, current ratings, or power consumption labels?

### 12.3 Environmental Considerations
- [ ] Should we design for end-of-life recycling (material marking, disassembly)?
- [ ] Are there restricted substances (RoHS, REACH, California Prop 65)?
- [ ] Should we minimize plastic use or use recycled materials?
- [ ] What is the expected product lifetime (design for X years)?

---

## 13. COST & MANUFACTURING CONSTRAINTS

### 13.1 Budget Targets
- [ ] What is the target Bill of Materials (BOM) cost for enclosure + mechanical?
- [ ] What is the target all-in cost (including labor, tooling amortization)?
- [ ] What production volume justifies custom tooling vs. modified COTS?
- [ ] Should we design for multiple price tiers (basic/advanced versions)?

### 13.2 Supply Chain
- [ ] What lead times are acceptable for components (standard parts vs. custom)?
- [ ] Should we single-source or multi-source critical components?
- [ ] Are there geopolitical supply chain risks we should mitigate?
- [ ] Should we prioritize global availability or regional sourcing?

### 13.3 Manufacturing Location
- [ ] Should manufacturing be centralized or regional?
- [ ] What are the labor skill requirements for assembly?
- [ ] Should we design for automated assembly or hand assembly?
- [ ] What quality control/testing is needed at manufacturing?

---

## 14. FUTURE EXPANSION & MODULARITY

### 14.1 Upgrade Path
- [ ] Should the enclosure accommodate future hardware revisions?
- [ ] What internal volume margin should we include for expansion?
- [ ] Should we design mounting points for future sensors (flow meter, weather station)?
- [ ] Can the design accommodate larger batteries or solar panels?

### 14.2 Modularity Considerations
- [ ] Should we design a platform architecture (base unit + add-on modules)?
- [ ] Can camera units be upgraded independently of main enclosure?
- [ ] Should we design for field retrofits vs. factory configuration?
- [ ] What backwards compatibility is required?

---

## 15. TESTING & VALIDATION REQUIREMENTS

### 15.1 Environmental Testing
- [ ] What temperature cycling tests are needed (thermal shock, soak)?
- [ ] What humidity/condensation tests (steady-state, cycling)?
- [ ] What water ingress testing (IP rating validation, hose test, submersion)?
- [ ] What UV/weathering tests (accelerated aging, outdoor exposure)?
- [ ] What vibration/shock testing (during shipping, installed on pole)?
- [ ] What salt spray testing (coastal deployment validation)?

### 15.2 Mechanical Testing
- [ ] What structural load testing (static, dynamic, fatigue)?
- [ ] What impact/drop testing (IK rating, shipping drops)?
- [ ] What mounting system validation (torque testing, pull-out testing)?
- [ ] What camera adjustment mechanism durability testing?

### 15.3 Field Trials
- [ ] Where should pilot deployments occur (which climate zones)?
- [ ] How long should field trials run before production?
- [ ] What data collection is needed from field trials?
- [ ] Should we instrument pilot units with additional sensors?

### 15.4 Quality Assurance
- [ ] What inspection criteria for incoming materials?
- [ ] What functional tests at assembly?
- [ ] What final QA tests before shipping?
- [ ] Should every unit be thermally cycled or sample-tested?

---

## 16. USER EXPERIENCE & TRAINING

### 16.1 Installation Experience
- [ ] What is the target installation time for a trained user?
- [ ] What is the target installation time for a first-time user?
- [ ] What is the minimum team size for safe installation?
- [ ] Should we design for one-person installation or always require two+?

### 16.2 Training Requirements
- [ ] What skill level is assumed (no technical background, basic electrical, engineering)?
- [ ] What training materials are needed (video, manual, hands-on workshop)?
- [ ] Should we include a practice installation kit or training simulator?
- [ ] What certification or competency assessment is needed?

### 16.3 Usability Goals
- [ ] How do we minimize points of failure in installation?
- [ ] Can we eliminate steps that require judgment calls?
- [ ] Should we use color coding, symbols, or "keying" to prevent errors?
- [ ] What visual aids should be included (installation diagram, cable routing map)?

---

## PRIORITY MATRIX

### Critical Path (Must Answer Before Design):
1. Environmental operating range (temp, humidity, IP rating)
2. Material selection (metal vs. plastic, thermal properties)
3. Mounting system requirements (pole range, adjustment needs)
4. Camera housing strategy (integrated vs. separate)
5. Field serviceability goals (tool requirements, access points)

### High Priority (Affects Major Design Decisions):
6. Thermal management approach (passive vs. active)
7. Cable management strategy (number and type of pass-throughs)
8. Visual indicator requirements (visibility distance, information displayed)
9. Hardware switch specifications (number, type, protection)
10. Shipping container design (reusable case vs. disposable packaging)

### Medium Priority (Can Be Refined During Design):
11. Spare parts strategy and quantities
12. Connector specifications and types
13. Surface finish and coating requirements
14. Labeling and documentation approach
15. Testing and validation protocols

### Lower Priority (Can Be Finalized During Detail Design):
16. Fastener types and counts
17. Internal cable routing methods
18. Color scheme and aesthetics
19. QR code and serialization strategy
20. End-of-life recycling considerations

---

## NEXT STEPS

1. **Stakeholder Review**: Distribute this questionnaire to:
   - Field deployment teams (Indonesia experience)
   - National Society partners
   - Electronics/software teams
   - Manufacturing/procurement teams

2. **Requirements Workshop**: Conduct sessions to answer critical path questions and resolve conflicts between requirements (e.g., cost vs. durability)

3. **Trade-off Analysis**: For key decisions (material, mounting system, camera housing), develop side-by-side comparisons with pros/cons/costs

4. **Concept Sketches**: Once critical questions are answered, develop 2-3 preliminary concept designs for review

5. **Prototyping Plan**: Identify which aspects need physical mockups vs. CAD validation vs. full functional prototypes

---

## DOCUMENT CONTROL

**File**: `/Users/tjordan/code/git/openrivercam/rc-box/MECHANICAL_DESIGN_QUESTIONNAIRE.md`

**Version**: 1.0
**Date**: 2025-11-28
**Author**: System Architecture Team
**Status**: Initial Draft - Pending Stakeholder Review

**Change Log**:
- 2025-11-28: Initial creation based on CLAUDE.md requirements and Indonesia deployment feedback
