# RC-Box Power System Design Documentation

This directory contains comprehensive documentation for designing the power system for the RC-Box humanitarian river monitoring device.

## Overview

The RC-Box requires a robust, solar-powered electrical system that can operate autonomously in diverse climates worldwide. The system must be deployable by personnel without specialized electrical training and field-serviceable with basic tools.

## Key Requirements (from CLAUDE.md)

- Scheduled startup/shutdown cycles for power conservation
- All-weather operation (tropical to arctic conditions)
- Field serviceable by non-specialists
- Visual power indicators visible from ground when pole-mounted
- Support for both solar and commercial power
- Hardware switches for power, maintenance mode, and WiFi hotspot
- Resilient against shipping damage and rough handling
- Adequate local storage to operate during periods without connectivity

## Documentation Structure

### 1. POWER_SYSTEM_DESIGN_QUESTIONS.md
**Purpose:** Comprehensive list of questions that must be answered before finalizing the power system design.

**Sections:**
- Power budget and consumption analysis (14 questions areas)
- Battery sizing and chemistry selection
- Solar panel sizing and mounting
- Power management controller comparison (PiJuice vs PiSugar vs custom MPPT)
- Environmental and climate considerations
- Hardware switches and visual indicators
- Protection circuits and safety
- Field serviceability requirements
- Commercial power option integration
- Power monitoring and software interface
- Sizing examples and verification
- Cost and procurement
- Risk analysis and failure modes

**Use this document to:**
- Guide initial design discussions
- Ensure all critical factors are considered
- Create specifications for component selection
- Identify gaps in knowledge that require research or testing

### 2. POWER_CONTROLLER_COMPARISON.md
**Purpose:** Detailed comparison of power management solutions suitable for the RC-Box.

**Sections:**
- Comparison matrix: PiJuice vs PiSugar 3 vs PiSugar S vs Custom MPPT
- Evaluation criteria (power scaling, deployment duration, solar panel size, environmental extremes, field serviceability, cost)
- Hybrid approach: custom power board concept
- Recommended phased approach (power budget analysis → controller selection → prototype testing → field trial)
- Additional resources needed

**Use this document to:**
- Understand pros/cons of each power management platform
- Select appropriate controller based on measured power requirements
- Plan prototype and testing phases
- Make informed procurement decisions

### 3. POWER_BUDGET_TEMPLATE.md
**Purpose:** Structured template for calculating power consumption and sizing battery/solar components.

**Sections:**
1. Component power consumption measurement (RPi5, cameras, storage, connectivity, indicators)
2. Operational duty cycle definition (recording schedule, power state timeline)
3. Power budget calculation (consumption by state, daily energy totals)
4. Battery sizing (autonomy requirements, depth of discharge, capacity calculation)
5. Solar panel sizing (irradiance data, panel output calculation, safety factors)
6. Charge controller selection
7. Energy balance verification (daily balance, recharge time after autonomy)
8. Summary and recommendations

**Use this document to:**
- Systematically measure and document power consumption
- Calculate required battery capacity for specified autonomy
- Size solar panel based on worst-case solar conditions
- Verify system will be energy-positive
- Create specifications for procurement

### 4. POWER_SYSTEM_FIELD_GUIDE.md
**Purpose:** Practical guide for deployment, operation, and troubleshooting in the field.

**Sections:**
- Pre-deployment checklist (component verification, functional testing, spare parts)
- Deployment procedure (site survey, solar panel installation, battery installation, wiring, startup)
- Operation and monitoring (daily/weekly/monthly/seasonal checks)
- Troubleshooting guide (no power, battery not charging, unexpected shutdowns, LED errors, solar panel issues)
- Emergency procedures (system shutdown, battery replacement, panel replacement)
- Maintenance log template
- Appendices (safe electrical practices, voltage reference charts, LED indicator meanings)

**Use this document to:**
- Train field personnel on deployment
- Guide installation at deployment sites
- Diagnose and fix problems remotely (walk technician through troubleshooting)
- Document maintenance activities
- Ensure safe electrical practices

## Recommended Workflow

### Phase 1: Requirements Definition (CURRENT PHASE)
**Deliverables:**
- [ ] Answer questions in POWER_SYSTEM_DESIGN_QUESTIONS.md
- [ ] Define operational duty cycle (how often does system record?)
- [ ] Identify deployment locations and climate data
- [ ] Establish budget constraints
- [ ] Define autonomy requirements (days without sun)

**Timeline:** 1-2 weeks

### Phase 2: Power Measurement & Calculation
**Deliverables:**
- [ ] Assemble Raspberry Pi 5 with 2x Camera Module V3, storage, WiFi
- [ ] Measure power consumption in each operational state using USB power meter
- [ ] Complete POWER_BUDGET_TEMPLATE.md with measured data
- [ ] Calculate required battery capacity
- [ ] Calculate required solar panel size
- [ ] Select appropriate charge controller

**Timeline:** 1-2 weeks

### Phase 3: Component Selection & Procurement
**Deliverables:**
- [ ] Use POWER_CONTROLLER_COMPARISON.md to select charge controller platform
- [ ] Create Bill of Materials (BOM) with part numbers and suppliers
- [ ] Identify primary and backup suppliers for each component
- [ ] Procure components for initial prototype
- [ ] Procure spare parts and tools per POWER_SYSTEM_FIELD_GUIDE.md

**Timeline:** 2-4 weeks (depending on lead times)

### Phase 4: Prototype Build & Bench Testing
**Deliverables:**
- [ ] Assemble power system (battery, solar panel, charge controller, Raspberry Pi)
- [ ] Create wiring diagram documenting as-built configuration
- [ ] Conduct functional tests per POWER_SYSTEM_FIELD_GUIDE.md checklist
- [ ] Run 30-day bench test with realistic duty cycle
- [ ] Monitor battery voltage, solar charging, any issues
- [ ] Simulate low-sun conditions (cover panel for X days)
- [ ] Verify system survives autonomy period
- [ ] Document test results

**Timeline:** 4-6 weeks

### Phase 5: Enclosure Integration & Environmental Testing
**Deliverables:**
- [ ] Design enclosure layout for power components
- [ ] Install components in weatherproof enclosure
- [ ] Install hardware switches and LED indicators
- [ ] Conduct environmental tests (if chamber available):
  - Temperature: -10°C to +50°C operation
  - Humidity: 95% RH
  - Vibration: simulate shipping and pole mounting
- [ ] Water resistance test: IP65 minimum (rain simulation)
- [ ] Document any failures or needed design changes

**Timeline:** 3-4 weeks

### Phase 6: Field Trial
**Deliverables:**
- [ ] Deploy prototype unit at test site
- [ ] Install per POWER_SYSTEM_FIELD_GUIDE.md procedures
- [ ] Monitor remotely (if connectivity available)
- [ ] Conduct weekly site visits for first month
- [ ] Log battery voltage, solar input, any issues
- [ ] Collect data on:
  - Days of successful operation
  - Battery minimum voltage reached
  - Any shutdowns or failures
  - Solar panel soiling rate (affects cleaning frequency)
- [ ] Iterate on design based on field experience

**Timeline:** 4-8 weeks

### Phase 7: Refinement & Documentation
**Deliverables:**
- [ ] Update design based on field trial lessons learned
- [ ] Finalize component selections
- [ ] Create final BOM with qualified suppliers
- [ ] Update POWER_SYSTEM_FIELD_GUIDE.md with actual specifications
- [ ] Create training materials for field deployment
- [ ] Prepare for production deployment

**Timeline:** 2-3 weeks

## Critical Design Decisions

The following decisions must be made early, as they affect component selection:

### 1. System Voltage
**Options:**
- 5V (direct from PiJuice/PiSugar to RPi GPIO)
- 12V (battery + DC-DC converter to 5V USB-C)
- 24V (larger systems, more efficient for long cable runs)

**Trade-offs:**
- 5V: Simple, fewer components, limited battery capacity
- 12V: Industry standard, large battery options, requires DC-DC converter
- 24V: Most efficient, best for high power, more complex

**Recommendation:** Depends on power budget from Phase 2 measurements.

### 2. Battery Chemistry
**Options:**
- LiFePO4 (Lithium Iron Phosphate): Long life, safe, temperature tolerant
- Li-ion: High energy density, lower cost, less temperature tolerant
- SLA (Sealed Lead Acid): Cheap, heavy, short life

**Trade-offs:**
- LiFePO4: Best for harsh environments, 3000-5000 cycles, no fire risk, expensive
- Li-ion: Good energy density, 500-1000 cycles, don't charge below 0°C, fire risk if damaged
- SLA: Cheap, reliable, heavy, 200-300 cycles, less efficient

**Recommendation:** LiFePO4 for long-term deployments in variable climates (worth extra cost).

### 3. Power Management Platform
**Options:**
- PiJuice HAT: Integrated solution, limited to ~40Wh battery
- PiSugar: Compact, even more limited (~25Wh battery)
- Custom MPPT: Scalable, industry components, more wiring

**Trade-offs:**
See POWER_CONTROLLER_COMPARISON.md for detailed analysis.

**Recommendation:** Depends on power budget:
- If <30Wh/day: PiSugar 3 acceptable
- If 30-60Wh/day: PiJuice with max battery
- If >60Wh/day: Custom MPPT required

### 4. Solar Panel Size
**Options:**
- Small (5-10W): Compact, lightweight, limited charging
- Medium (20-50W): Good balance, requires larger mounting
- Large (50-100W+): Maximum reliability, bulky, expensive

**Trade-offs:**
- Small: Easy to mount on device pole, may not keep up in cloudy weather
- Medium: Separate mounting or large pole, adequate for most conditions
- Large: Definitely separate mounting, very reliable, overkill for low power systems

**Recommendation:** 1.5-2× daily consumption (Wh) / (solar hours × 0.7 efficiency)

## Lessons from Indonesia Deployment

From CLAUDE.md, the Indonesia deployment identified these power-related issues:

**Issues:**
1. "Hardware needs a visual indicator of whether it's on or not, visible from ground while on pole"
   - **Solution:** External LED indicators designed into power system

2. "Hardware soft power switch makes it impossible to know if the device has been turned on or not"
   - **Solution:** Hardware power switch with mechanical ON/OFF indication

3. "Create a hardware switch we can use to turn on a local wireless hotspot for configuration"
   - **Solution:** Physical switch integrated into enclosure

4. "Create a hardware switch we can use to put the device into maintenance mode"
   - **Solution:** Multi-position switch or separate switches for modes

5. "Hardware should have a lot more local storage than what they appear to have - operate for a long time without stable connection"
   - **Power implication:** More storage = more power consumption during writes, factor into budget

6. "Device should show in the UI whether it is in maintenance mode or not, and how long the timer"
   - **Power implication:** Maintenance mode should prevent auto-shutdown, extend operating time

**These are addressed in the design questions and field guide.**

## Design Principles for Humanitarian Context

Based on the project requirements, the power system must prioritize:

1. **Reliability over Cost**
   - Oversized battery/solar is acceptable to ensure operation
   - Quality components reduce field service burden

2. **Simplicity over Optimization**
   - Clear, labeled connections over complex wiring
   - Mechanical switches over software-only controls
   - Standard components over custom designs (where possible)

3. **Field Serviceability over Compactness**
   - Screw terminals over soldered connections
   - Replaceable fuses over electronic protection (when safe)
   - Modular design allows component replacement

4. **Visible Feedback over Hidden Status**
   - External LEDs for all critical states
   - Physical switch positions indicate mode
   - No "black box" operation

5. **Documentation over Training**
   - Assume technician has basic skills but no specialized knowledge
   - Photographic guides showing correct assembly
   - Troubleshooting flowcharts for common issues

## Next Steps

1. **Review these documents** with the team
2. **Schedule power measurement session** to populate POWER_BUDGET_TEMPLATE.md
3. **Gather climate data** for target deployment regions (solar irradiance, temperature extremes)
4. **Define operational duty cycle** (how often will system record?)
5. **Establish budget** for power system components
6. **Begin Phase 1** of the recommended workflow

## Questions or Issues?

If you have questions about the power system design or these documents:

1. Check if the question is addressed in POWER_SYSTEM_DESIGN_QUESTIONS.md
2. Review the relevant section in POWER_CONTROLLER_COMPARISON.md or POWER_BUDGET_TEMPLATE.md
3. If still unclear, document the question and raise with the team

## Document Maintenance

These documents are living resources and should be updated as:
- Design decisions are made
- Components are selected
- Testing reveals new information
- Field deployments provide lessons learned

**Last Updated:** 2025-11-28
**Version:** 1.0
**Status:** Initial draft for review

---

## File Reference

All power system documentation:

- `README_POWER_SYSTEM.md` (this file) - Overview and workflow
- `POWER_SYSTEM_DESIGN_QUESTIONS.md` - Comprehensive design questions
- `POWER_CONTROLLER_COMPARISON.md` - Controller platform comparison
- `POWER_BUDGET_TEMPLATE.md` - Power calculation spreadsheet
- `POWER_SYSTEM_FIELD_GUIDE.md` - Deployment and troubleshooting guide
- `CLAUDE.md` - Original project requirements
