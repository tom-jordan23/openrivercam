# Power System Design Questions - RC-Box

This document contains critical questions that must be answered before finalizing the power system design for the RC-Box humanitarian river monitoring device.

## 1. POWER BUDGET & CONSUMPTION

### 1.1 Device Power Requirements
- [ ] What is the idle power consumption of Raspberry Pi 5 (no peripherals)?
- [ ] What is the peak power consumption during:
  - Video recording (2x Pi Camera Module V3 active)?
  - Video processing/encoding?
  - Data transmission (WiFi/cellular)?
  - All systems active simultaneously?
- [ ] What is the power draw of each peripheral:
  - Each camera module (active vs standby)?
  - Storage devices (SSD/HDD vs microSD)?
  - USB accessories?
  - Optional cellular modem?
  - Visual indicators (LEDs)?
- [ ] What is the startup current surge for the RPi5?

### 1.2 Operational Profile
- [ ] What is the intended duty cycle:
  - Recording frequency (continuous, hourly, daily)?
  - Recording duration per cycle?
  - Processing time per recording?
  - Upload/sync frequency?
- [ ] What is the daily "ON" time vs "OFF" time?
- [ ] Should the device maintain network connectivity when not recording?
- [ ] What is acceptable maximum power consumption (watts) during active mode?
- [ ] What is the target standby power consumption?

### 1.3 Power Budget Scenarios
- [ ] Typical daily energy consumption (Wh/day) for:
  - Minimal operation (1 recording/day)?
  - Normal operation (expected usage)?
  - Maximum operation (worst case)?
- [ ] Peak power requirement (watts) for sizing inverter/DC-DC converters?

## 2. BATTERY SYSTEM

### 2.1 Battery Chemistry Selection
- [ ] LiFePO4 vs Li-ion vs SLA - which chemistry is preferred and why?
  - Temperature tolerance (-20C to +60C)?
  - Cycle life requirements (how many years × 365 cycles)?
  - Safety considerations (fire risk in humanitarian contexts)?
  - Availability for field replacement?
  - Cost constraints?
- [ ] Are there shipping restrictions for different battery chemistries to deployment regions?
- [ ] Can local suppliers provide replacement batteries in target deployment countries?

### 2.2 Battery Capacity Sizing
- [ ] How many days of autonomy without solar input (cloudy days)?
  - Minimum acceptable (1-2 days)?
  - Target (3-5 days)?
  - Extreme case (7+ days)?
- [ ] What depth of discharge (DoD) is acceptable:
  - For battery longevity (50%)?
  - For operational requirements (80%)?
- [ ] What is the minimum battery capacity (Ah) at operational voltage (5V, 12V, or other)?
- [ ] Should batteries be field-replaceable without tools, or is screwdriver access acceptable?
- [ ] Are there size/weight constraints for shipping or pole mounting?

### 2.3 Battery Configuration
- [ ] Single battery or multiple cells in series/parallel?
- [ ] Voltage requirement: 5V direct, or 12V/24V with DC-DC conversion?
- [ ] Should battery be internal to enclosure or external (easier replacement)?
- [ ] Hot-swap capability needed for battery replacement without shutdown?

## 3. SOLAR PANEL SYSTEM

### 3.1 Solar Panel Sizing
- [ ] What are the worst-case solar irradiance conditions across deployment regions:
  - Tropical rainy season?
  - Northern latitudes in winter?
  - Dusty/hazy environments?
- [ ] What is the daily solar energy available (kWh/m²/day) in worst-case location?
- [ ] Sizing methodology:
  - Daily consumption (Wh) × safety factor / (solar hours × panel efficiency)?
  - What safety factor (1.5x, 2x, 3x)?
- [ ] Minimum panel wattage required (10W, 20W, 50W, 100W)?
- [ ] Panel voltage: 6V, 12V, 18V, 24V?

### 3.2 Solar Panel Mounting & Deployment
- [ ] Mounting method:
  - Same pole as camera (vibration concerns)?
  - Separate mounting (more complex deployment)?
  - Ground-based with cable to device?
- [ ] Panel orientation:
  - Fixed tilt angle (what angle for various latitudes)?
  - Adjustable mounting (more complex)?
  - Vertical mounting on pole (reduced efficiency but simpler)?
- [ ] Cable length from panel to battery/controller (voltage drop considerations)?
- [ ] Connector type: MC4 (industry standard) or custom weatherproof?
- [ ] Panel frame: aluminum (corrosion in coastal areas?) or other?

### 3.3 Solar Panel Durability
- [ ] Wind load rating required (pole-mounted panels catch wind)?
- [ ] Impact resistance (shipping, hail, vandalism)?
- [ ] Operating temperature range (-40C to +85C typical, is this sufficient)?
- [ ] Marine/coastal environment rating (salt fog resistance)?
- [ ] Replacement availability - commercial off-the-shelf critical?

## 4. POWER MANAGEMENT CONTROLLER

### 4.1 PiJuice vs PiSugar Comparison
- [ ] PiJuice capabilities:
  - Max charge current?
  - Battery capacity support range?
  - Solar input voltage range and max wattage?
  - RTC accuracy and battery backup?
  - Programmable wake/sleep schedules?
  - I2C monitoring capabilities?
  - Button/switch support?
- [ ] PiSugar capabilities:
  - (Same questions as PiJuice)
- [ ] Which platform has better:
  - Python API for scheduling?
  - Community support and documentation?
  - Field replacement availability?
  - Cost (with consideration for bulk purchasing)?
  - Reliability/MTBF data?

### 4.2 Alternative Power Management Solutions
- [ ] Should we consider custom MPPT charge controller instead?
  - More expensive but more flexible?
  - Allows larger solar panels and batteries?
  - Industry-standard component (easier replacement)?
- [ ] Examples: Victron SmartSolar, EPSolar, Genasun?
- [ ] RTC function: separate RTC module if not using PiJuice/PiSugar?

### 4.3 Power Management Features Required
- [ ] MPPT (Maximum Power Point Tracking) vs PWM solar charging?
- [ ] Charge current programmability (for different battery sizes)?
- [ ] Load disconnect at low battery voltage?
- [ ] Programmable under-voltage and over-voltage protection thresholds?
- [ ] Temperature compensation for charging (critical in variable climates)?
- [ ] Data logging: voltage, current, battery state of charge?
- [ ] Alert/shutdown thresholds for battery protection?

## 5. ENVIRONMENTAL & CLIMATE CONSIDERATIONS

### 5.1 Temperature Effects
- [ ] Operating temperature range for deployment locations:
  - Minimum (arctic, high altitude)?
  - Maximum (desert, tropical direct sun)?
- [ ] Battery charging adjustments needed for temperature:
  - Charging disabled below 0C for Li-ion?
  - Charging voltage adjustment for temperature?
- [ ] Solar panel derating at high temperatures (efficiency loss)?
- [ ] Internal enclosure temperature rise (does it affect battery life)?
- [ ] Heating or cooling needed for electronics or batteries?

### 5.2 Climate-Specific Challenges
- [ ] Tropical environments:
  - High humidity effects on electronics?
  - Frequent rain (days of low solar input)?
  - Fungal growth on solar panels?
- [ ] Cold climates:
  - Battery capacity reduction in cold?
  - Snow accumulation on solar panels?
  - Condensation/ice formation?
- [ ] Dusty/arid environments:
  - Dust accumulation on solar panels (how much efficiency loss)?
  - Cleaning frequency and method?
  - Dust intrusion into enclosure?

### 5.3 Seasonal Variations
- [ ] How does power budget change across seasons:
  - Winter: less solar, potentially more recording needed (flood season)?
  - Summer: more solar, less recording?
- [ ] Should battery size account for worst-case seasonal solar availability?
- [ ] Operational adjustments for seasons (automatic or manual reconfiguration)?

## 6. HARDWARE SWITCHES & CONTROLS

### 6.1 Switch Requirements
- [ ] Power On/Off switch:
  - Master power disconnect (battery isolation)?
  - Soft power button to RPi (GPIO trigger)?
  - Both?
- [ ] Maintenance Mode switch:
  - Momentary or latching?
  - How does RPi detect state (GPIO, I2C)?
  - Visual indication of mode?
- [ ] WiFi Hotspot switch:
  - Physical switch or same as maintenance mode?
  - Auto-timeout after X hours?

### 6.2 Switch Specifications
- [ ] Current rating for power switches (continuous and surge)?
- [ ] Waterproof/weatherproof rating (IP67/IP68)?
- [ ] Illuminated switches (consume power)?
- [ ] Vandal-resistant design (recessed, require tool)?
- [ ] Cable gland compatibility for through-panel mounting?

### 6.3 Switch Mounting & Access
- [ ] External enclosure access (require opening case)?
- [ ] Panel-mount through enclosure wall?
- [ ] Sealed magnetic switches (no enclosure penetration)?
- [ ] Location on enclosure for easy access from ground with pole hook?

## 7. VISUAL INDICATORS

### 7.1 Indicator Requirements
- [ ] What states need indication:
  - Power on/off?
  - Battery charging (solar input active)?
  - Battery level (full, medium, low, critical)?
  - System status (booting, running, error)?
  - Maintenance mode active?
  - WiFi hotspot active?
  - Recording in progress?
- [ ] Visibility requirements:
  - Distance (visible from ground, ~3-5 meters)?
  - Daylight visibility?
  - Night visibility (too bright = power waste)?

### 7.2 LED Selection
- [ ] LED types:
  - Standard 5mm LEDs (low power)?
  - High-brightness LEDs (visible in daylight)?
  - RGB LEDs (multiple states with one component)?
- [ ] Power consumption per LED (1-20mA)?
- [ ] Total power budget for indicators (always-on vs pulsed)?
- [ ] Control: direct GPIO, PWM for brightness, LED driver IC?

### 7.3 Indicator Design
- [ ] Light pipe to bring LED to exterior surface (no enclosure penetration)?
- [ ] External weatherproof LED panel?
- [ ] Flash patterns vs solid on (e.g., slow flash = charging, fast flash = error)?
- [ ] Audio indicators (beeper for errors) or visual only?

## 8. PROTECTION CIRCUITS

### 8.1 Input Protection (Solar)
- [ ] Reverse polarity protection (diode, MOSFET, or built into controller)?
- [ ] Over-voltage protection (TVS diode, crowbar circuit)?
- [ ] Short circuit protection (fuse, breaker, electronic)?
- [ ] Lightning/surge protection (needed for outdoor pole mount)?
  - GDT (Gas Discharge Tube)?
  - MOV (Metal Oxide Varistor)?
  - Grounding strategy?

### 8.2 Battery Protection
- [ ] Over-charge protection (voltage and current limits)?
- [ ] Over-discharge protection (low-voltage disconnect)?
- [ ] Over-current protection (fuse rating)?
- [ ] Temperature monitoring (cutoff if too hot/cold)?
- [ ] Cell balancing (if multi-cell battery pack)?
- [ ] Fusing: inline with battery, what rating (A)?

### 8.3 Load Protection (Raspberry Pi)
- [ ] Input voltage range for RPi5 (5V USB-C, tolerance)?
- [ ] Transient protection (voltage spikes during switching)?
- [ ] Current limiting to prevent USB-C power supply damage?
- [ ] Reverse current protection (back-feed from RPi)?
- [ ] Brown-out detection and clean shutdown trigger?

### 8.4 Safety & Compliance
- [ ] Fusing strategy:
  - Solar input fuse?
  - Battery fuse?
  - Load fuse?
  - Fuse accessibility for field replacement?
- [ ] Regulatory compliance needed:
  - CE marking?
  - FCC (if RF components)?
  - Shipping certifications (UN38.3 for batteries)?
- [ ] Fire safety: flame-retardant enclosures, thermal fuses?

## 9. FIELD SERVICEABILITY

### 9.1 Component Accessibility
- [ ] Tool requirements:
  - No tools (snap connectors)?
  - Screwdriver only (Phillips, flat, hex)?
  - Specialized tools (avoid)?
- [ ] Connectors:
  - Solar panel: MC4, barrel jack, Anderson Powerpole, screw terminals?
  - Battery: XT60, Anderson, proprietary?
  - Between boards: JST, Molex, screw terminals?
- [ ] Labeling strategy:
  - Color coding?
  - Printed labels (will they fade)?
  - Engraved markings?
  - Diagrammatic labels showing polarity?

### 9.2 Spare Parts & Consumables
- [ ] What components should have spares included:
  - Fuses (what ratings, how many)?
  - Connectors and terminals?
  - Wire (what gauge, lengths)?
  - Heat shrink tubing?
  - Mounting hardware (screws, bolts)?
  - Cable ties, velcro straps?
- [ ] Battery replacement frequency (2 years, 5 years)?
- [ ] Solar panel expected lifetime (10+ years)?

### 9.3 Documentation for Field Service
- [ ] Connection diagram format:
  - Photographic?
  - Illustrated schematic (simplified)?
  - Step-by-step disassembly/reassembly?
- [ ] Troubleshooting guide:
  - No power symptoms and checks?
  - Battery not charging symptoms?
  - LED error code meanings?
- [ ] Measurement points for voltage/current testing?
- [ ] Safe disassembly procedure (discharge caps, disconnect battery first, etc.)?

### 9.4 Modular Design
- [ ] Should power system be one replaceable module?
- [ ] Can non-technical person identify and replace failed component:
  - Battery?
  - Charge controller?
  - Fuse?
  - Solar panel?
  - Wiring harness?
- [ ] Keyed connectors to prevent incorrect assembly?

## 10. COMMERCIAL POWER OPTION

### 10.1 AC/DC Power Supply
- [ ] Input voltage range:
  - Universal (100-240VAC)?
  - Regional specific (need different versions)?
- [ ] Output voltage/current (5V/5A for RPi5 USB-C?)?
- [ ] Efficiency rating (80 Plus, Level VI)?
- [ ] Connector type (USB-C, barrel jack, screw terminal)?

### 10.2 Dual Power Configuration
- [ ] Auto-switching between solar and commercial power:
  - Prioritize commercial when available?
  - Use commercial to charge battery?
  - Isolate solar when on commercial?
- [ ] Switching mechanism:
  - Automatic (diode OR, ideal diode, relay)?
  - Manual switch?
- [ ] Does PiJuice/PiSugar support dual input, or need external circuit?

### 10.3 Commercial Power Deployment
- [ ] Enclosure considerations:
  - Cable gland for mains cable?
  - Internal/external power supply?
  - GFCI/RCD requirements for outdoor AC power?
- [ ] Grounding requirements for AC-powered installations?
- [ ] Certification requirements (UL, CE) if AC mains involved?

## 11. POWER MONITORING & SOFTWARE INTERFACE

### 11.1 Telemetry Requirements
- [ ] What power metrics should be logged:
  - Battery voltage, current, SoC%?
  - Solar input voltage, current, power?
  - Load current?
  - Temperature?
- [ ] Logging frequency (every minute, hourly)?
- [ ] Storage: local file, database, cloud upload?
- [ ] Display in web UI for field technicians?

### 11.2 Scheduling & Power Management
- [ ] Wake/sleep schedule:
  - RTC-based wake (PiJuice/PiSugar RTC)?
  - Cron job with system suspend?
  - Complete power-off and power-on cycles?
- [ ] Adaptive scheduling based on battery level:
  - Reduce recording frequency if battery low?
  - Automatic entry to low-power mode?
- [ ] Manual override: always-on maintenance mode duration?

### 11.3 Alerts & Notifications
- [ ] Low battery alert mechanism:
  - Local LED?
  - Remote notification (if connectivity available)?
  - Automatic graceful shutdown threshold?
- [ ] Solar fault detection (panel disconnected, shaded)?
- [ ] Temperature alerts (too hot/cold)?

## 12. SIZING EXAMPLE & VERIFICATION

### 12.1 Sample Calculation Needed
- [ ] Create reference design for typical deployment:
  - Location: tropical, rainy season, 3.5 kWh/m²/day solar
  - Duty cycle: 10 minute recording every 6 hours
  - 3 days autonomy
  - Calculate: battery Ah, solar panel W, charge controller rating
- [ ] Create reference design for worst-case deployment:
  - Location: northern latitude winter, 1.5 kWh/m²/day solar
  - Same duty cycle
  - 5 days autonomy
  - Calculate: battery Ah, solar panel W, charge controller rating

### 12.2 Testing & Validation
- [ ] How will power system be tested before deployment:
  - Bench test with simulated solar input?
  - Full-cycle test (charge, discharge, repeat)?
  - Temperature chamber testing?
- [ ] Acceptance criteria:
  - X days of operation on battery alone?
  - Battery charges to full within Y hours of sun?
  - No shutdowns during Z day field trial?

## 13. COST & PROCUREMENT

### 13.1 Budget Constraints
- [ ] Target cost per unit for power system (battery, solar, controller, protection)?
- [ ] Trade-off: reliability vs cost (spend more for MTBF?)?
- [ ] Bulk purchasing discounts for multi-unit deployments?

### 13.2 Supply Chain
- [ ] Lead time for components (plan for X month procurement)?
- [ ] Single supplier vs multiple sources (risk mitigation)?
- [ ] Import duties/taxes for destination countries?
- [ ] Compatibility with local voltage/frequency standards?

### 13.3 Lifecycle Cost
- [ ] Battery replacement cost and frequency?
- [ ] Solar panel degradation (assume 0.5%/year, affects sizing)?
- [ ] Shipping cost for replacement parts?
- [ ] Training cost for field service (factor into design complexity)?

## 14. RISK ANALYSIS

### 14.1 Failure Modes
- [ ] What happens if:
  - Battery fails (dead short, open circuit)?
  - Solar panel damaged (cable cut, panel broken)?
  - Charge controller fails?
  - Fuse blows repeatedly?
  - RPi doesn't shut down cleanly (corrupted SD card)?
- [ ] Fail-safe modes: what is safe state if control is lost?

### 14.2 Mitigation Strategies
- [ ] Redundancy: worth adding backup battery, dual charge controllers?
- [ ] Monitoring: remote diagnostics to detect issues before failure?
- [ ] Preventive maintenance schedule (battery check every X months)?

### 14.3 Harsh Environment Risks
- [ ] Shipping damage mitigation (protective packaging, shock indicators)?
- [ ] Warehousing in uncontrolled environment (temperature extremes during storage)?
- [ ] Handling by untrained staff (clear "this side up", "fragile" markings)?
- [ ] Theft/vandalism (locking enclosure, anti-tamper features)?

---

## Action Items

After answering these questions, the following deliverables should be created:

1. **Power Budget Spreadsheet** - detailed consumption breakdown and daily/seasonal energy calculations
2. **Component Selection Matrix** - comparison of charge controllers, batteries, solar panels with pros/cons
3. **Schematic Diagram** - electrical connections, protection circuits, switches, indicators
4. **BOM (Bill of Materials)** - with part numbers, suppliers, costs, lead times
5. **Mechanical Integration Plan** - enclosure layout, panel mounting, cable routing
6. **Field Service Manual** - troubleshooting, replacement procedures, spare parts list
7. **Test Plan** - bench tests, environmental tests, field trial criteria

---

**Document Version:** 1.0
**Date:** 2025-11-28
**Author:** RC-Box Design Team
**Status:** Draft for Review
