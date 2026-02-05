# Power System Field Deployment & Troubleshooting Guide

This guide provides practical instructions for deploying and servicing the RC-Box power system in the field.

## Pre-Deployment Checklist

### 1. Component Verification

Before shipping or deploying:

- [ ] Battery voltage check: _____ V (should be 50-80% charged for shipping)
- [ ] Battery physical condition: no swelling, damage, or corrosion
- [ ] Solar panel condition: no cracks, delamination, or scratches
- [ ] All connectors present and undamaged
- [ ] Fuses: correct rating installed, spares included
- [ ] Cables: no cuts, proper length, strain relief installed
- [ ] Visual indicators (LEDs): all functional
- [ ] Switches: smooth operation, no sticking
- [ ] Enclosure: seals intact, no cracks, all fasteners present

### 2. Functional Testing

Power system bench test before deployment:

- [ ] Connect solar panel (or DC power supply simulating panel)
- [ ] Verify charging indicator shows battery charging
- [ ] Connect Raspberry Pi load
- [ ] Verify system boots and runs normally
- [ ] Check all LED indicators show correct states
- [ ] Test all switches (power, maintenance mode, WiFi)
- [ ] Measure battery voltage under load: _____ V
- [ ] Measure solar input current: _____ A (if sun/simulator available)
- [ ] Run for minimum 24 hours, verify no shutdowns
- [ ] Document test results and date: _____

### 3. Spare Parts & Tools

Pack the following with each deployment:

**Spare Parts:**
- [ ] Fuses: _____ rating, quantity: _____
- [ ] Extra wire: _____ gauge, _____ meters
- [ ] Heat shrink tubing: assorted sizes
- [ ] Cable ties / Velcro straps
- [ ] Spare connectors: types _____, quantity _____
- [ ] Terminals: types _____, quantity _____
- [ ] Spare battery (if budget allows): _____
- [ ] Electrical tape
- [ ] Weatherproof sealant / silicone

**Tools:**
- [ ] Multimeter (voltage/current measurement)
- [ ] Screwdriver set (Phillips, flat, hex as needed)
- [ ] Wire strippers
- [ ] Crimping tool (if crimped terminals used)
- [ ] Small adjustable wrench
- [ ] Flashlight / headlamp
- [ ] Camera (for documentation)

**Documentation:**
- [ ] This field guide (printed, laminated)
- [ ] Wiring diagram (printed, laminated)
- [ ] Component datasheets
- [ ] Contact information for remote support

## Deployment Procedure

### Step 1: Site Survey

Before mounting system:

- [ ] Identify mounting location for device enclosure
- [ ] Verify pole/mast meets specifications:
  - Diameter: _____ cm
  - Material: _____ (metal, wood, concrete)
  - Height: _____ m above ground
  - Rigidity: no excessive sway in wind
- [ ] Identify solar panel mounting location:
  - Maximum sun exposure (south-facing in N hemisphere, north in S hemisphere)
  - Minimal shading (trees, buildings, etc.)
  - Tilt angle: _____ degrees (approximately = latitude)
  - Secure from theft/vandalism
- [ ] Measure cable run from panel to enclosure: _____ m
- [ ] Take photos of site for documentation

### Step 2: Solar Panel Installation

- [ ] Mount panel bracket securely
- [ ] Attach panel to bracket
- [ ] Verify panel orientation: azimuth _____ °, tilt _____ °
- [ ] Check panel is secure (pull test)
- [ ] Route cable to enclosure location
- [ ] Use cable ties to secure cable to pole/structure
- [ ] Ensure cable has drip loop (prevents water ingress)
- [ ] Label panel cable at both ends: "SOLAR +" and "SOLAR -"
- [ ] Take photos of installation

### Step 3: Battery Installation

**CAUTION: Observe proper polarity. Incorrect connection can damage components or cause fire.**

- [ ] Open enclosure
- [ ] Verify battery mounting location is secure
- [ ] Check battery voltage: _____ V (should be >50% charged)
- [ ] Connect battery to charge controller:
  - **RED wire to POSITIVE (+) terminal**
  - **BLACK wire to NEGATIVE (-) terminal**
- [ ] Secure connections (tighten terminals, insert connectors fully)
- [ ] Verify polarity with multimeter BEFORE installing fuse
- [ ] Install battery fuse
- [ ] Check charge controller LED: should indicate battery connected
- [ ] Label battery cables: "BATTERY +" and "BATTERY -"
- [ ] Take photo of connections

### Step 4: Solar Panel Connection

- [ ] Locate solar panel cable at enclosure
- [ ] Identify positive and negative wires (usually marked on cable jacket)
- [ ] Connect solar cable to charge controller:
  - **RED wire to SOLAR IN +**
  - **BLACK wire to SOLAR IN -**
- [ ] Secure connections
- [ ] Install solar input fuse (if separate from controller)
- [ ] Check charge controller LED: should indicate solar input detected
- [ ] Measure solar input voltage: _____ V (should be ~17-22V for 12V panel in sun)
- [ ] Verify battery charging indicator is active (if sunny)
- [ ] Label solar input: "SOLAR IN +" and "SOLAR IN -"
- [ ] Take photo of connections

### Step 5: Load Connection (Raspberry Pi)

- [ ] Connect charge controller output to Raspberry Pi power input
  - If PiJuice/PiSugar: attach HAT to GPIO header
  - If custom MPPT: connect DC-DC converter output to USB-C
- [ ] Verify voltage at RPi input: _____ V (should be 4.75-5.25V)
- [ ] Do NOT power on yet
- [ ] Verify all connections are secure
- [ ] Check for any loose wires or potential shorts
- [ ] Take photo of complete wiring

### Step 6: System Startup

- [ ] Close enclosure (but do not seal yet, in case troubleshooting needed)
- [ ] Switch on power (if master switch present)
- [ ] Observe LED indicators:
  - Power indicator: should illuminate
  - Battery indicator: should show charging (if sunny) or charged state
  - RPi status: should show boot sequence
- [ ] Wait for RPi to fully boot (_____ seconds typical)
- [ ] Check RPi web interface (if accessible via WiFi)
- [ ] Verify system is functional
- [ ] If all OK, seal enclosure
- [ ] Mount enclosure to pole/structure
- [ ] Final photo of complete installation

### Step 7: Documentation

- [ ] Record installation date: _____
- [ ] Record GPS coordinates: _____, _____
- [ ] Record initial battery voltage: _____ V
- [ ] Record solar panel voltage: _____ V
- [ ] Record system serial number or ID: _____
- [ ] Update central database/spreadsheet with deployment info
- [ ] Mark on wiring diagram with colored pen showing actual configuration
- [ ] Leave copy of documentation in waterproof bag inside enclosure

## Operation & Monitoring

### Daily/Weekly Checks (if personnel available)

- [ ] Visual inspection: enclosure intact, no damage
- [ ] LED indicators: confirm normal operation
- [ ] Solar panel: clean, no debris or damage
- [ ] Any error indicators? Note and investigate

### Monthly Checks

- [ ] Measure battery voltage: _____ V (should be >12.0V for 12V system)
- [ ] Check for corrosion on external connections
- [ ] Verify system is recording and uploading data
- [ ] Download logs for review
- [ ] Clean solar panel if dusty/dirty

### Seasonal Maintenance

- [ ] Full system inspection
- [ ] Load test battery (verify capacity hasn't degraded significantly)
- [ ] Tighten all connections
- [ ] Check weatherproofing seals
- [ ] Update firmware/software if needed

## Troubleshooting Guide

### Symptom: No Power / System Won't Turn On

**Possible Causes:**

1. **Battery depleted**
   - Check: Measure battery voltage with multimeter
   - Expected: >11V for 12V battery, >4V for 5V system
   - If low: Charge battery with external charger or wait for solar charging
   - If very low (<10V for 12V): Battery may be damaged, consider replacement

2. **Fuse blown**
   - Check: Visually inspect fuse, use multimeter to check continuity
   - Replace: Install spare fuse of same rating
   - If blows again: SHORT CIRCUIT PRESENT - do not reconnect until found

3. **Loose connection**
   - Check: All cable connections secure
   - Fix: Tighten terminals, reseat connectors
   - Verify: Measure voltage at multiple points to find where it's lost

4. **Switch in off position**
   - Check: All switches in correct position
   - Fix: Toggle switches, verify operation

5. **Battery disconnected or damaged**
   - Check: Battery voltage, physical condition
   - Fix: Reconnect or replace battery

**Troubleshooting Steps:**
```
1. Measure battery voltage at battery terminals: _____ V
2. Measure battery voltage at charge controller input: _____ V
3. Measure voltage at RPi power input: _____ V
4. Check fuse continuity: PASS / FAIL
5. Check all connections: OK / LOOSE / DISCONNECTED
```

### Symptom: Battery Not Charging

**Possible Causes:**

1. **No solar input**
   - Check: Measure solar panel voltage (disconnect from controller first)
   - Expected: ~17-22V for 12V panel in full sun, ~5-7V for small USB panels
   - If zero: Panel disconnected, cable damaged, or panel facing away from sun
   - If very low: Panel shaded, dirty, or damaged

2. **Solar cable damaged**
   - Check: Continuity from panel to controller
   - Fix: Repair or replace cable

3. **Charge controller fault**
   - Check: Controller LEDs show error code?
   - Consult: Controller manual for error codes
   - Fix: Reset controller, or replace if faulty

4. **Battery already full**
   - Check: Battery voltage (fully charged = ~13.6V for 12V LiFePO4, ~14.4V for SLA)
   - This is normal - controller stops charging when full

5. **Temperature too cold**
   - Check: Ambient temperature (Li-ion shouldn't charge below 0°C)
   - Fix: Wait for warmer weather, or add insulation/heating

**Troubleshooting Steps:**
```
1. Measure solar panel open-circuit voltage (disconnected): _____ V
2. Measure solar input at controller: _____ V
3. Measure battery voltage: _____ V
4. Check controller LED indicators: _____
5. Ambient temperature: _____ °C
6. Visual inspection of panel: CLEAN / DIRTY / SHADED / DAMAGED
```

### Symptom: System Shuts Down Unexpectedly

**Possible Causes:**

1. **Battery voltage too low**
   - Check: Battery voltage under load
   - Expected: Should stay >11V for 12V system
   - If drops below cutoff: Battery depleted or undersized
   - Fix: Reduce power consumption, increase battery size, or add solar capacity

2. **Overcurrent condition**
   - Check: Measure current draw during operation
   - If excessive: Short circuit or component fault
   - Fix: Identify and repair/replace faulty component

3. **Thermal shutdown**
   - Check: Enclosure temperature
   - If too hot: Improve ventilation, add heat sinks, reduce sun exposure
   - If too cold: Add insulation, reduce power consumption to extend battery

4. **Software issue (not power-related)**
   - Check: System logs for errors
   - Fix: Debug software, reinstall OS

**Troubleshooting Steps:**
```
1. Measure battery voltage (no load): _____ V
2. Measure battery voltage (under load): _____ V
3. Measure current draw during operation: _____ A
4. Check enclosure temperature: _____ °C
5. Review system logs for errors: _____
```

### Symptom: LEDs Show Error / Unusual Pattern

**Refer to controller manual for LED error codes.**

Common patterns:
- **Rapid flashing:** Fault condition (overvoltage, overcurrent, temperature)
- **Slow flashing:** Low battery warning
- **Red LED:** Error or critical state
- **Green LED:** Normal operation
- **Yellow/Orange LED:** Warning or intermediate state

**Troubleshooting Steps:**
```
1. Note LED pattern: _____
2. Consult manual for error code: _____
3. Take corrective action per manual: _____
```

### Symptom: Solar Panel Not Producing Expected Power

**Possible Causes:**

1. **Shading**
   - Check: Any shadows on panel during peak sun hours?
   - Fix: Reorient panel or remove obstruction

2. **Dirt/Dust accumulation**
   - Check: Visual inspection of panel surface
   - Fix: Clean with soft cloth and water (no abrasives)

3. **Wrong orientation**
   - Check: Panel facing correct direction (south in N hemisphere)?
   - Check: Tilt angle approximately = latitude?
   - Fix: Adjust mounting

4. **Cloudy weather**
   - Check: Weather conditions (overcast reduces output by 50-90%)
   - This is normal - system should run on battery during cloudy periods

5. **Panel degradation**
   - Check: Age of panel (degrades ~0.5% per year)
   - If old: Consider replacement

**Troubleshooting Steps:**
```
1. Measure panel voltage (disconnected, full sun): _____ V
2. Measure panel current (connected, full sun): _____ A
3. Calculate power: V × A = _____ W
4. Compare to panel rating: _____ W
5. Visual inspection: CLEAN / DIRTY / DAMAGED
6. Shading during day: YES / NO
7. Weather: SUNNY / PARTLY CLOUDY / OVERCAST
```

## Emergency Procedures

### Complete System Shutdown

If system must be shut down immediately (e.g., fire risk, flooding):

1. Switch off main power switch (if present)
2. Disconnect solar panel (to prevent continued charging)
3. Disconnect battery (remove fuse or disconnect cables)
4. Document reason for shutdown and date
5. Contact technical support

**SAFETY:** If battery is swollen, hot, or smoking, do NOT touch. Evacuate area and contact emergency services.

### Battery Replacement (Field Procedure)

**Required:** Replacement battery (correct voltage and capacity), tools, multimeter

1. Shut down Raspberry Pi gracefully (via software if possible)
2. Switch off main power
3. Disconnect solar panel
4. **WAIT 30 seconds for capacitors to discharge**
5. Measure old battery voltage: _____ V (for reference)
6. Remove battery fuse
7. Disconnect battery cables (negative first, then positive)
8. Remove old battery from enclosure
9. Inspect battery compartment for corrosion or damage
10. Install new battery
11. Connect new battery cables (positive first, then negative)
12. **VERIFY POLARITY with multimeter BEFORE installing fuse**
13. Install fuse
14. Reconnect solar panel
15. Observe charge controller LEDs for normal operation
16. Switch on main power
17. Monitor system boot
18. Document replacement: Date _____, Old battery voltage _____, New battery ID _____

### Solar Panel Replacement

1. Disconnect solar panel cables at charge controller
2. Remove mounting hardware
3. Remove damaged panel
4. Install new panel
5. Secure mounting
6. Route cables to enclosure
7. **VERIFY POLARITY with multimeter**
8. Connect to charge controller
9. Verify charging operation
10. Document replacement

## Maintenance Log Template

**System ID:** _____
**Location:** _____
**Installation Date:** _____

| Date | Technician | Activity | Battery Voltage | Solar Voltage | Notes |
|------|-----------|----------|-----------------|---------------|-------|
| | | | | | |
| | | | | | |
| | | | | | |

## Contact Information

**Technical Support:**
- Name: _____
- Email: _____
- Phone: _____
- Available hours: _____

**Local Support (if available):**
- Name: _____
- Phone: _____
- Location: _____

**Emergency Contact:**
- Name: _____
- Phone: _____

## Appendix A: Safe Electrical Practices

**ALWAYS:**
- Disconnect power before working on system
- Verify voltage with multimeter before touching
- Use insulated tools
- Work in dry conditions
- Observe correct polarity (red = positive, black = negative)
- Wear safety glasses when working with batteries

**NEVER:**
- Short circuit battery terminals (risk of fire/explosion)
- Connect power with incorrect polarity
- Work on system during lightning storm
- Touch battery if swollen, leaking, or hot
- Use damaged cables or connectors
- Mix old and new batteries in same system

## Appendix B: Voltage Reference Chart

**12V LiFePO4 Battery:**
| State of Charge | Voltage (V) | Notes |
|----------------|-------------|-------|
| 100% | 13.6 | Fully charged |
| 90% | 13.4 | |
| 70% | 13.2 | |
| 50% | 13.0 | Recommended minimum |
| 30% | 12.8 | Low battery warning |
| 10% | 12.0 | Critical - shutdown soon |
| 0% | 11.0 | Depleted |

**12V SLA (Sealed Lead Acid) Battery:**
| State of Charge | Voltage (V) | Notes |
|----------------|-------------|-------|
| 100% | 12.8 | Fully charged |
| 75% | 12.5 | |
| 50% | 12.2 | Recommended minimum |
| 25% | 12.0 | Low battery warning |
| 0% | 11.6 | Depleted |

**5V Li-ion Battery (nominal 3.7V cell):**
| State of Charge | Voltage (V) | Notes |
|----------------|-------------|-------|
| 100% | 4.2 | Fully charged |
| 70% | 3.85 | |
| 50% | 3.75 | |
| 20% | 3.5 | Low battery |
| 0% | 3.0 | Depleted |

## Appendix C: Quick Reference - LED Indicators

**Power Indicator:**
- **Solid Green:** System powered, normal operation
- **Off:** No power

**Battery Indicator:**
- **Solid Green:** Battery full (>80%)
- **Slow Flash Green:** Battery charging
- **Solid Yellow:** Battery medium (50-80%)
- **Slow Flash Yellow:** Battery low (20-50%)
- **Fast Flash Red:** Battery critical (<20%)
- **Off:** No battery connected or fault

**Solar Indicator:**
- **Solid Green:** Solar input active, charging
- **Off:** No solar input (night or panel issue)
- **Flash Red:** Solar input fault

**System Status:**
- **Slow Pulse Blue:** Raspberry Pi booting
- **Solid Blue:** Raspberry Pi running
- **Flash Blue:** Recording in progress
- **Off:** Raspberry Pi off or shutdown

**Maintenance Mode:**
- **Solid Orange:** Maintenance mode active
- **Off:** Normal operation mode

**NOTE:** Actual LED indicators depend on final design. Update this section based on implementation.

---

**Document Version:** 1.0
**Date:** 2025-11-28
**Related Documents:**
- POWER_SYSTEM_DESIGN_QUESTIONS.md
- POWER_CONTROLLER_COMPARISON.md
- POWER_BUDGET_TEMPLATE.md
