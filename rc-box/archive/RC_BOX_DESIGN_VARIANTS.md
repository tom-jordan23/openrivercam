# RC-Box Design Variants: Stakeholder Review Document

**Document Version:** 1.0
**Date:** 2025-11-28
**Status:** Draft for Review

## Executive Summary

This document presents three optimized design variants for the RC-Box river monitoring system. Each variant meets all core requirements but optimizes for different deployment priorities: cost minimization, maximum reliability, or ease of use for non-technical operators.

**Core Requirements (All Variants):**
- Raspberry Pi 5 processor
- 2x Pi Camera V3 (USB adapter, separate housings)
- 2-3 min runtime every 15 min (~100 Wh/day consumption)
- 512GB+ SSD storage (1-2 weeks video)
- IP67 weatherproof rating
- Operating range: -20°C to +50°C
- Cellular AND WiFi connectivity
- 4 switches: power, mode, WiFi hotspot, reset
- Status display screen
- Dual power configuration support: solar OR grid
- NEMA enclosure with pole/structure mounting
- Field serviceable components

---

## Variant 1: Budget-Optimized Design

**Target Use Case:** High-volume deployments where cost per unit is critical. Organizations with central technical support and ability to ship replacement parts.

### Component Specifications

#### Core Electronics
| Component | Model/Spec | Rationale | Est. Cost |
|-----------|-----------|-----------|-----------|
| **Power Management** | PiSugar 3 Plus | Integrated battery, simple installation, adequate for 100Wh/day with external battery pack | $55 |
| **Battery (Solar Config)** | 2x LiFePO4 3.2V 50Ah cells (3S configuration = 9.6V, 160Wh) | Commodity 18650-style cells in holder, field replaceable, 1.6 days autonomy | $45 |
| **Battery (Grid Config)** | LiFePO4 12V 10Ah | Small UPS battery for shutdown only | $25 |
| **Solar Panel** | 50W 12V polycrystalline | Standard size, widely available, adequate worst-case output (~175 Wh/day @ 50% efficiency) | $35 |
| **Solar Charge Controller** | PWM 10A controller with temperature compensation | Simple, reliable, works with PiSugar | $12 |
| **Grid Power Supply** | Mean Well RS-25-12 (25W, 12V) | Industrial-grade SMPS, global input (85-264VAC) | $18 |
| **Cellular Modem** | Quectel EC25-E Mini PCIe with USB adapter | Supports LTE Cat 4, multi-band (B1/3/7/8/20), widely available | $35 |
| **SIM Configuration** | Single nano-SIM slot | Keep it simple, local procurement | - |
| **Storage** | Kingston A400 512GB M.2 SATA SSD with USB adapter | Commodity SSD, reliable, field replaceable via USB | $35 |
| **Camera Adapters** | Arducam B0370 (2x) | Proven Pi Camera V3 to USB adapter | $40 |

#### Display & Interface
| Component | Model/Spec | Rationale | Est. Cost |
|-----------|-----------|-----------|-----------|
| **Display** | 1.3" I2C OLED (128x64, monochrome) | Small, low power, adequate visibility, button-activated | $8 |
| **Display Control** | Single momentary button (IP67) | Press to illuminate display for 30 seconds | $3 |
| **Switches** | 4x IP67 toggle switches | Simple, reliable, widely available | $16 |
| **Status LEDs** | 3x 10mm LEDs (power/mode/network) | Visible from ground, always-on indicators | $3 |

#### Enclosure & Mounting
| Component | Model/Spec | Rationale | Est. Cost |
|-----------|-----------|-----------|-----------|
| **Main Enclosure** | Polycase WC-42 (10"x8"x6") polycarbonate | Clear lid option for display visibility, IP67 rated | $35 |
| **Camera Housing** | 2x Mier BHR-001 budget bullet camera housing | Off-the-shelf CCTV housing, IP66, includes mounting bracket | $30 |
| **Anti-Fog System** | Active heating + molecular sieve + vent (per camera below) | **MANDATORY** - passive desiccant alone fails in tropics | $146 |

#### Anti-Fog System (Per Camera - MANDATORY)
| Component | Model/Spec | Rationale | Est. Cost |
|-----------|-----------|-----------|-----------|
| **Breather Vent** | Gore PMF200408 or Nitto TEMISH | Pressure equalization prevents moisture pumping | $15 |
| **Desiccant** | Type 4A Molecular Sieve 100g | Works at >90% RH (silica gel fails above 60% RH) | $8 |
| **Lens Heater** | Dew-Not DN001 or astronomy heater ring (5W, 12V) | Keeps lens above dew point | $25 |
| **Thermostat** | STC-1000 | Activates heater when temp <25°C | $18 |
| **Anti-Fog Coating** | Cat Crap paste | Backup: makes any condensation transparent | $7 |
| **Per camera subtotal** | | | **$73** |
| **Camera Cables** | 2x 3m USB3.0 cables (waterproof connectors) | Standard length, adequate for most setups | $24 |
| **Camera Mounts** | 2x Small ball head (photography style) | Commercial photo ball heads, lock with single screw | $20 |
| **Pole Mounting** | 2x stainless hose clamps (3-6" diameter) | Simple, adjustable, readily available globally | $8 |
| **Cable Glands** | 6x PG9 IP67 cable glands | Standard waterproof entry points | $12 |
| **Internal Mounting** | Plastic standoffs + foam padding | Simple internal organization | $8 |

### Total Bill of Materials

| Configuration | Estimated Cost (USD) |
|---------------|---------------------|
| **Base System** (no power) | $426 |
| **Solar Configuration** | $568 |
| **Grid Configuration** | $469 |
| **Anti-Fog Field Service Kit** | $75 |

**Anti-Fog Field Service Kit:** 4x spare molecular sieve desiccant packs, 1x spare lens heater, 1x Cat Crap paste, 1x spare breather vent.

**Additional Power Requirement:** Anti-fog heaters add 60-100 Wh/day. Solar panel increased to 75W minimum.

### Pros & Cons

**Advantages:**
- Lowest per-unit cost enables larger deployments
- All components commercially available from multiple suppliers
- Simple design reduces assembly time
- Standard parts mean easier to source replacements locally
- Adequate performance for stated requirements
- Lower shipping costs (smaller/lighter components)

**Disadvantages:**
- Less battery autonomy (1.6 days vs 3-5 days)
- Smaller display harder to read in bright sun
- Monochrome display provides less information at a glance
- Manual battery cell replacement requires more training
- Ball head mounts may loosen over time in high-vibration environments
- Requires more frequent maintenance/monitoring

### Best Deployment Scenarios

1. **Large-scale programs** (50+ units) where cost per unit is paramount
2. **Well-supported deployments** with regular site visits planned
3. **Moderate climates** without extreme temperature swings
4. **Locations with reliable cellular coverage** (less dependence on local WiFi)
5. **Organizations with central technical capacity** to troubleshoot and ship parts

### Operational Considerations

- **Maintenance interval:** Every 3-6 months recommended
- **Expected lifespan:** 3-5 years with battery replacement at year 2
- **Field repair complexity:** Moderate (requires basic electrical knowledge)
- **Training time:** 4-6 hours for installation and basic troubleshooting

---

## Variant 2: Resilience-Optimized Design

**Target Use Case:** Remote, harsh environments with infrequent access. Humanitarian deployments where system failure could compromise critical monitoring during emergencies.

### Component Specifications

#### Core Electronics
| Component | Model/Spec | Rationale | Est. Cost |
|-----------|-----------|-----------|-----------|
| **Power Management** | Waveshare UPS HAT (C) + separate MPPT controller | True UPS function, RTC wake, handles higher power loads | $48 |
| **Battery (Solar Config)** | 2x Battle Born 50Ah 12V LiFePO4 (parallel = 600Wh) | Premium quality, built-in BMS, 6 days autonomy, extreme temp performance | $450 |
| **Battery (Grid Config)** | Battle Born 25Ah 12V LiFePO4 | Same quality, smaller capacity for UPS function | $220 |
| **Solar Panel** | 2x Renogy 50W monocrystalline (100W total) | High efficiency, rugged construction, MC4 connectors, worst-case output ~350 Wh/day | $150 |
| **Solar Charge Controller** | Victron SmartSolar MPPT 75/15 | Premium MPPT, temperature compensation, Bluetooth monitoring, 97% efficiency | $95 |
| **Grid Power Supply** | Mean Well NDR-120-12 (120W, 12V DIN rail) | Industrial DIN rail mount, wide temp range, 3-year warranty | $45 |
| **Cellular Modem** | Sierra Wireless EM7455 with dual SIM | Industrial grade, wide temp range, automatic failover, global bands | $120 |
| **SIM Configuration** | Dual micro-SIM with automatic failover | Redundant connectivity across carriers | - |
| **Storage** | Samsung 870 EVO 1TB M.2 SATA SSD with industrial USB3 adapter | Enterprise-grade reliability, double storage capacity | $85 |
| **Camera Adapters** | Arducam B0370 (2x) with shielded cables | Same proven adapter with EMI protection | $50 |

#### Display & Interface
| Component | Model/Spec | Rationale | Est. Cost |
|-----------|-----------|-----------|-----------|
| **Display** | 2.4" TFT LCD (320x240, color, transflective) | Transflective = readable in direct sunlight, color shows more status info | $28 |
| **Display Mode** | Always-on with auto-brightness sensor | Visible from ground at all times, dims at night to save power | $5 |
| **Switches** | 4x IP68 marine-grade toggle switches | Exceeds IP67 spec, corrosion resistant, sealed to submersion level | $32 |
| **Status LEDs** | 4x industrial 12mm LEDs (power/charge/mode/network) | Extra bright, visible in daylight, conformal coated | $12 |

#### Enclosure & Mounting
| Component | Model/Spec | Rationale | Est. Cost |
|-----------|-----------|-----------|-----------|
| **Main Enclosure** | Fiberglass NEMA 4X (14"x12"x7") | UV-resistant fiberglass, better thermal management, corrosion-proof | $120 |
| **Camera Housing** | 2x Dotworkz D3 heated camera housing | Active heating for cold climates, integrated sunshield, IP68 | $280 |
| **Anti-Fog Solution** | Integrated in Dotworkz housing: heater + blower + Gore-Tex vent | Industrial-grade multi-layer approach (meets MANDATORY requirement) | Incl. |
| **Desiccant Backup** | Type 4A Molecular Sieve 100g per housing | Additional margin in extreme humidity | $16 |
| **Anti-Fog Coating** | Cat Crap paste (factory applied) | Belt-and-suspenders approach | $7 |
| **Camera Cables** | 2x 5m industrial USB3.0 with overmolded connectors | Longer reach, ruggedized, shielded | $60 |
| **Camera Mounts** | 2x Heavy-duty pan/tilt mounts with locking knobs | Stainless steel construction, maintains adjustment under vibration | $80 |
| **Pole Mounting** | Stainless U-bolt kit with anti-vibration pads | More secure than hose clamps, dampens vibration | $25 |
| **Cable Glands** | 8x IP68 brass cable glands with strain relief | Exceeds spec, metal construction, redundant entries | $40 |
| **Internal Mounting** | Aluminum DIN rail + modular brackets | Professional installation, serviceable, heat dissipation | $35 |

#### Additional Resilience Features
| Component | Model/Spec | Rationale | Est. Cost |
|-----------|-----------|-----------|-----------|
| **Environmental Monitoring** | BME280 sensor (temp/humidity/pressure) | Monitor internal conditions, predict failures | $8 |
| **Accelerometer** | ADXL345 3-axis | Detect excessive vibration/tampering | $6 |
| **GPS Module** | U-blox NEO-6M | Anti-theft tracking, accurate timestamping | $12 |
| **Backup RTC** | DS3231 with supercapacitor | Redundant timekeeping if primary fails | $8 |
| **Thermal Management** | 40mm fan + thermal sensor | Active cooling in extreme heat, prevents thermal shutdown | $12 |
| **Surge Protection** | TVS diodes on power inputs | Protect against lightning/power surges | $8 |

### Total Bill of Materials

| Configuration | Estimated Cost (USD) |
|---------------|---------------------|
| **Base System** (no power) | $710 |
| **Solar Configuration** | $1,505 |
| **Grid Configuration** | $1,175 |
| **Spare Parts Kit** | $150 |

**Spare Parts Kit:** Extra switches, LEDs, fuses, cable glands, silica gel, USB cables, spare camera adapter, thermal paste.

### Pros & Cons

**Advantages:**
- Maximum reliability and autonomy (6 days without sun)
- Heated camera housings work in extreme cold
- Dual SIM redundancy improves connectivity uptime
- Color display provides rich status information at a glance
- Heavy-duty mounts maintain calibration under harsh conditions
- Built-in monitoring sensors enable predictive maintenance
- Industrial-grade components rated for extreme temperatures
- GPS provides anti-theft tracking and precise timestamps
- MPPT charging maximizes solar capture in poor conditions
- 2 weeks of storage (vs 1 week) provides extra buffer

**Disadvantages:**
- Significantly higher cost (4x budget variant)
- Heavier (harder to ship, install)
- More complex (longer assembly time)
- Some premium components may have longer lead times
- Higher power consumption from heated housings and always-on display
- Overkill for benign environments
- May require import certifications for some industrial components

### Best Deployment Scenarios

1. **Remote locations** with difficult/dangerous access (e.g., conflict zones, extreme weather areas)
2. **Critical monitoring** during flood seasons where failure is unacceptable
3. **Harsh environments** (arctic, desert, tropical with extreme humidity)
4. **Long-term deployments** (5-10 years) where reliability justifies upfront cost
5. **Sites with high theft/vandalism risk** (GPS tracking provides recovery capability)
6. **Locations with poor cellular coverage** (dual SIM increases connection reliability)

### Operational Considerations

- **Maintenance interval:** Annual recommended, can go 18+ months
- **Expected lifespan:** 7-10 years with minimal component replacement
- **Field repair complexity:** Low (most failures can be diagnosed remotely via sensors)
- **Training time:** 6-8 hours (more features to understand)
- **Remote monitoring:** Full telemetry enables proactive intervention

---

## Variant 3: Ease-of-Use Optimized Design

**Target Use Case:** National Society volunteers and humanitarian workers with minimal technical training. Emphasis on clear feedback, simple setup, and tool-free maintenance.

### Component Specifications

#### Core Electronics
| Component | Model/Spec | Rationale | Est. Cost |
|-----------|-----------|-----------|-----------|
| **Power Management** | PiJuice HAT Zero pHAT | Best Python API, extensive documentation, proven in maker community | $60 |
| **Battery (Solar Config)** | Talentcell 12V 50Ah LiFePO4 with built-in BMS | Consumer-friendly battery pack with LED indicator, XT60 connectors (no exposed terminals) | $130 |
| **Battery (Grid Config)** | Talentcell 12V 20Ah LiFePO4 | Same series, smaller capacity, consistent interface | $65 |
| **Solar Panel** | Renogy 60W flexible solar panel with controller kit | Lightweight, includes integrated 10A PWM controller, plug-and-play MC4 connectors | $120 |
| **Grid Power Supply** | Mean Well GST60A12-P1J with barrel jack | Consumer-style barrel connector (like laptop charger), hard to reverse polarity | $22 |
| **Cellular Modem** | Waveshare SIM7600G-H 4G HAT | Stacks on Pi, clear documentation, active community | $65 |
| **SIM Configuration** | Single nano-SIM (tool-free tray) | SIM tray like smartphone, no tools needed | - |
| **Storage** | SanDisk Extreme Portable SSD 1TB | Consumer-grade, USB-C, rubber housing, tool-free connection | $95 |
| **Camera Adapters** | 2x Arducam B0370 (in labeled enclosure) | Same adapter but clearly labeled "Camera 1" and "Camera 2" | $40 |

#### Display & Interface
| Component | Model/Spec | Rationale | Est. Cost |
|-----------|-----------|-----------|-----------|
| **Display** | 3.5" TFT LCD (480x320, color, capacitive touch) | Touch interface simplifies interaction, large enough for clear icons/text | $35 |
| **Display Mode** | Always-on with auto-brightness and sleep | Always visible, but dims to save power when inactive | $5 |
| **Switches** | 3x large IP67 illuminated rocker switches | Illuminated shows active state, large levers easy to operate with gloves | $45 |
| **Reset Button** | Recessed push-button (pen-activated) | Prevents accidental reset | $3 |
| **Visual Feedback** | RGB LED strip (5 LEDs) inside clear enclosure lid | Multi-color status indication visible 360 degrees | $8 |

#### Enclosure & Mounting
| Component | Model/Spec | Rationale | Est. Cost |
|-----------|-----------|-----------|-----------|
| **Main Enclosure** | Polycase WC-53 (12"x10"x7") clear polycarbonate | Large clear lid shows internal status LEDs, easier access, color-coded labels | $55 |
| **Enclosure Closure** | Tool-free quarter-turn latches | No screwdriver needed for service access | Incl. |
| **Camera Housing** | 2x Eversecu clear dome housing | Transparent housing shows camera orientation, easy visual inspection | $45 |
| **Anti-Fog System** | Active heating + molecular sieve + vent (per camera below) | **MANDATORY** - passive desiccant alone fails in tropics | $146 |

#### Anti-Fog System (Per Camera - MANDATORY)
| Component | Model/Spec | Rationale | Est. Cost |
|-----------|-----------|-----------|-----------|
| **Breather Vent** | Gore PMF200408 or Nitto TEMISH | Pressure equalization prevents moisture pumping | $15 |
| **Desiccant** | Type 4A Molecular Sieve 100g | Works at >90% RH (silica gel fails above 60% RH) | $8 |
| **Lens Heater** | Dew-Not DN001 or astronomy heater ring (5W, 12V) | Keeps lens above dew point | $25 |
| **Thermostat** | STC-1000 with **LED indicator** | Activates heater when temp <25°C; LED visible from ground shows heater status | $20 |
| **Anti-Fog Coating** | Cat Crap paste | Backup: makes any condensation transparent | $7 |
| **Per camera subtotal** | | | **$75** |
| **Camera Cables** | 2x 4m USB3.0 (different colors: blue/red) | Color-coded so "Camera 1" always uses blue cable, reduces confusion | $40 |
| **Camera Mounts** | 2x Magnetic articulating mount with quick-release plate | Magnetic base adheres to any metal pole, articulating arm for easy positioning, quick-release camera | $60 |
| **Pole Mounting** | Quick-mount strap system (ratcheting) | Like backpack straps, no tools required, fits 2-8" poles | $25 |
| **Cable Glands** | 6x IP67 push-fit cable glands | Push cable through, automatic seal, no threading/wrenching | $30 |
| **Internal Mounting** | Color-coded foam insert with cutouts | Components fit into labeled foam sections, visually obvious if something is wrong | $15 |

#### Usability Features
| Component | Model/Spec | Rationale | Est. Cost |
|-----------|-----------|-----------|-----------|
| **Quick-Start Guide** | Laminated visual guide attached inside lid | Always accessible, weatherproof, picture-based instructions | $5 |
| **Cable Labels** | Printed heat-shrink labels on all cables | Every cable clearly labeled with source and destination | $8 |
| **Connector Keying** | Different connector types for each function | Impossible to plug wrong cable into wrong port | - |
| **Photo Documentation** | Printed photos of correct assembly | Attached inside enclosure, shows proper cable routing and component placement | $3 |
| **Alignment Tool** | 3D-printed camera alignment guide | Physical template to help set correct camera angle for steep banks | $5 |
| **Field Checklist** | Laminated checklist attached to enclosure | Step-by-step deployment and troubleshooting checklist | $3 |

### Total Bill of Materials

| Configuration | Estimated Cost (USD) |
|---------------|---------------------|
| **Base System** (no power) | $616 |
| **Solar Configuration** | $916 |
| **Grid Configuration** | $748 |
| **Anti-Fog Field Service Kit** | $75 |

**Anti-Fog Field Service Kit:** 4x spare molecular sieve desiccant packs, 1x spare lens heater, 1x Cat Crap paste, 1x spare breather vent, pre-labeled replacement cables, printed troubleshooting guide.

**Additional Power Requirement:** Anti-fog heaters add 60-100 Wh/day. Solar panel increased to 100W.

### Pros & Cons

**Advantages:**
- Minimal training required (2-3 hours vs 6-8 hours)
- Touch display enables intuitive GUI design
- Color-coded cables eliminate connection errors
- Tool-free assembly/disassembly (latches, push-fit, quick-release)
- Magnetic camera mounts allow repositioning without tools
- Clear visual indicators show system status at a glance
- Built-in instructions reduce reliance on manuals
- Alignment tool helps non-technical users set camera angles
- Hard-to-reverse connectors prevent damage from mistakes
- Consumer-grade battery packs have friendly interfaces (LED charge indicators)
- Transparent housings allow visual inspection without opening
- 3 days autonomy (middle ground between variants 1 and 2)

**Disadvantages:**
- Consumer components may have shorter lifespan than industrial versions
- Magnetic mounts could be stolen more easily than bolted systems
- Touch display more expensive and consumes more power
- Large enclosure may be overkill for internal space needed
- Tool-free closures may not be as secure as screw-down in extreme conditions
- Additional usability features add cost without improving core functionality
- Reliance on specific consumer products (less interchangeable)

### Best Deployment Scenarios

1. **Volunteer-operated programs** where technical expertise is limited
2. **Rapid deployment scenarios** (disaster response) where time is critical
3. **Training programs** for non-technical National Society staff
4. **Multiple operators** who may not all receive full training
5. **Locations requiring frequent camera repositioning** during setup phase
6. **Demonstration/proof-of-concept** deployments where ease of use builds confidence
7. **Resource-constrained organizations** that cannot provide extensive technical support

### Operational Considerations

- **Maintenance interval:** 6 months recommended
- **Expected lifespan:** 4-6 years
- **Field repair complexity:** Very low (most operations tool-free)
- **Training time:** 2-3 hours (focus on operational procedures, not technical details)
- **User error rate:** Significantly lower due to color-coding, keying, and visual aids
- **Deployment time:** 30-45 minutes vs 60-90 minutes for other variants

### Software UI Considerations

The touch display enables a more sophisticated UI:

**Home Screen:**
- Large icons with labels (battery %, network status, recording status)
- Color-coded status (green = good, yellow = warning, red = error)
- Touch "View Cameras" to see live preview from both cameras
- Touch "Settings" for WiFi configuration, recording schedule, etc.
- Touch "Help" for troubleshooting flowchart

**Camera Alignment Mode:**
- Split-screen view showing both camera feeds
- Overlay grid showing target area
- Real-time angle/pitch indicators
- "Lock" button when satisfied with positioning

**Maintenance Mode:**
- Clear countdown timer with "Extend" button
- Checklist of common maintenance tasks
- "Report Issue" wizard for remote support

---

## Comparison Matrix

### Summary Table

| Criteria | Budget Variant | Resilience Variant | Ease-of-Use Variant |
|----------|----------------|-------------------|---------------------|
| **Cost (Solar)** | $568 | $1,528 | $916 |
| **Cost (Grid)** | $469 | $1,198 | $748 |
| **Battery Autonomy** | 1.6 days | 6 days | 3 days |
| **Training Time** | 4-6 hours | 6-8 hours | 2-3 hours |
| **Deployment Time** | 60-90 min | 60-90 min | 30-45 min |
| **Maintenance Interval** | 3-6 months | 12-18 months | 6 months |
| **Expected Lifespan** | 3-5 years | 7-10 years | 4-6 years |
| **Tool Requirements** | Screwdrivers, wrenches | Screwdrivers, wrenches | None (tool-free) |
| **Field Repair Complexity** | Moderate | Low | Very Low |
| **Display** | 1.3" mono OLED | 2.4" color TFT | 3.5" color touch |
| **Camera Anti-Fog** | Active heater + vent + desiccant | Dotworkz heated housing | Active heater + vent + desiccant |
| **Mounting** | Hose clamps | U-bolts + anti-vibe | Quick-strap |
| **Best For** | Large deployments | Harsh/remote | Non-technical users |

### Performance Comparison

| Metric | Budget | Resilience | Ease-of-Use |
|--------|--------|------------|-------------|
| **Power Generation (worst-case)** | 260 Wh/day (75W panel) | 350 Wh/day | 350 Wh/day (100W panel) |
| **Power Consumption** | ~180 Wh/day (incl. anti-fog heaters) | ~185 Wh/day (heated housings) | ~183 Wh/day (incl. anti-fog heaters) |
| **Net Energy Balance** | +80 Wh/day | +165 Wh/day | +167 Wh/day |
| **Days to Recharge After Autonomy** | 2.0 days | 3.6 days | 1.8 days |
| **Storage Capacity** | 512GB (2.8 weeks) | 1TB (5.6 weeks) | 1TB (5.6 weeks) |
| **MTBF (Est.)** | 8,000 hours | 25,000 hours | 15,000 hours |
| **Operating Temp (Component Limited)** | -10°C to +45°C | -20°C to +50°C | -15°C to +48°C |
| **Anti-Fog Effectiveness** | 95%+ fog-free | 99%+ fog-free | 95%+ fog-free |

### Feature Comparison

| Feature | Budget | Resilience | Ease-of-Use |
|---------|--------|------------|-------------|
| **Cellular Connectivity** | Single SIM, Cat 4 | Dual SIM, Cat 6 | Single SIM, Cat 4 |
| **WiFi** | Built-in (RPi5) | Built-in (RPi5) | Built-in (RPi5) |
| **Status Display** | Button-activated | Always-on | Always-on touch |
| **Visual Indicators** | 3x LEDs | 4x LEDs + display | RGB strip + display |
| **Camera Anti-Fog** | Active heater + vent + desiccant | Heated Dotworkz + desiccant | Active heater + vent + desiccant |
| **GPS Tracking** | No | Yes | No |
| **Environmental Sensors** | No | Yes (temp/humidity/accel) | No |
| **Remote Monitoring** | Basic (connectivity only) | Full telemetry | Basic |
| **Assembly Method** | Screw terminals | DIN rail + terminals | Plug-and-play |
| **Service Access** | Screws | Screws | Quarter-turn latches |

### Cost-Benefit Analysis

#### Hardware Cost Comparison (Solar Configuration)

| Variant | Initial Hardware | Field Service Kit | Total Deployment Cost |
|---------|-----------------|-------------------|----------------------|
| **Budget** | $568 | $75 | **$643** |
| **Resilience** | $1,528 | $75 | **$1,603** |
| **Ease-of-Use** | $916 | $75 | **$991** |

*Note: Maintenance costs excluded as they vary significantly by deployment context. All variants include mandatory active anti-fog systems.*

---

## Decision Framework

### Selection Criteria

Use this framework to select the appropriate variant:

#### Choose Budget Variant if:
- [ ] Deploying 25+ units where aggregate cost is critical
- [ ] Sites are accessible (< 4 hours travel time)
- [ ] Regular maintenance visits are already planned for other reasons
- [ ] Climate is moderate (10°C to 35°C typical)
- [ ] Strong central technical support is available
- [ ] Operators have basic electrical knowledge
- [ ] Initial deployment is proof-of-concept (risk of requirements change)

#### Choose Resilience Variant if:
- [ ] Sites are remote or dangerous to access
- [ ] Operating in extreme climates (arctic, desert, tropical extremes)
- [ ] Monitoring is critical to life-safety decisions
- [ ] Deployment period is 5+ years
- [ ] Budget can accommodate higher upfront cost
- [ ] Maintenance visits are expensive (> $500 per visit)
- [ ] Sites have high theft/vandalism risk
- [ ] Poor cellular coverage requires redundant connectivity

#### Choose Ease-of-Use Variant if:
- [ ] Operators are volunteers with minimal training time
- [ ] Rapid deployment is required (disaster response)
- [ ] Multiple non-technical staff will handle equipment
- [ ] Organization has limited technical support capacity
- [ ] User error is a significant risk
- [ ] Equipment will be demonstrated to stakeholders/donors
- [ ] Camera repositioning may be needed frequently
- [ ] Training resources are constrained

### Hybrid Approaches

**Possible Mix-and-Match Strategies:**

1. **Tiered Deployment:** Use Resilience variant for remote/critical sites, Budget variant for accessible/backup sites.

2. **Staged Approach:** Start with Ease-of-Use variant for initial deployments and training, migrate to Budget variant as operators gain experience.

3. **Regional Customization:** Use Resilience variant in extreme climates, Budget variant in temperate regions.

4. **Component Sharing:** Standardize on some components (cameras, Pi 5, storage) but vary power/enclosure systems.

---

## Procurement Recommendations

### Lead Time Considerations

| Component Category | Budget Variant | Resilience Variant | Ease-of-Use Variant |
|-------------------|----------------|-------------------|---------------------|
| **Electronics** | 2-3 weeks | 4-6 weeks | 2-4 weeks |
| **Batteries** | 1-2 weeks | 6-8 weeks (Battle Born) | 2-3 weeks |
| **Solar Panels** | 1-2 weeks | 3-4 weeks | 2-3 weeks |
| **Enclosures** | 1-2 weeks | 4-6 weeks (custom NEMA) | 2-3 weeks |
| **Camera Housings** | 1 week | 6-8 weeks (Dotworkz) | 2 weeks |
| **Assembly & Testing** | 2 days/unit | 3 days/unit | 2 days/unit |

**Critical Path Items:**
- **Resilience variant:** Battle Born batteries and Dotworkz housings (longest lead time)
- **All variants:** Raspberry Pi 5 availability (check stock before committing)

### Bulk Ordering Discounts

Estimated savings at different quantities:

| Quantity | Budget Variant | Resilience Variant | Ease-of-Use Variant |
|----------|----------------|-------------------|---------------------|
| **1-5 units** | 0% (baseline) | 0% | 0% |
| **10 units** | -8% | -5% | -7% |
| **25 units** | -12% | -8% | -10% |
| **50 units** | -15% | -10% | -12% |
| **100+ units** | -18% | -12% | -15% |

### Supplier Recommendations

**Electronics:** Adafruit, DigiKey, Mouser (global shipping, reliable stock)
**Batteries:** Amazon/AliExpress (Budget/EoU), authorized distributors (Resilience)
**Solar:** Renogy direct, Amazon (consistent quality)
**Enclosures:** Polycase direct, Automation Direct
**Camera Housings:** Amazon (Budget/EoU), Dotworkz direct (Resilience)
**Miscellaneous:** McMaster-Carr (fasteners, glands), AliExpress (bulk commodity items)

### Country-Specific Procurement

For deployment in Indonesia (example):
- **Local sources:** Enclosures, cable glands, mounting hardware, tools
- **Regional sources (SE Asia):** Solar panels, basic electronics
- **International shipping required:** Raspberry Pi 5, cameras, specialty components
- **Include in initial shipment:** Desiccant, spare parts, consumables (hard to find locally)

---

## Testing & Validation Plan

### Prototype Testing (Recommended for All Variants)

#### Phase 1: Bench Testing (2 weeks)
- [ ] Assemble single unit of selected variant
- [ ] Measure actual power consumption under full load
- [ ] Verify battery autonomy by disconnecting solar
- [ ] Test all switches and display functionality
- [ ] Verify camera quality and field of view
- [ ] Test cellular connectivity with local SIM
- [ ] Run 48-hour continuous operation test
- [ ] Document any assembly issues or ambiguities

#### Phase 2: Environmental Testing (2 weeks)
- [ ] Hot soak test (enclosure in sun, measure internal temp)
- [ ] Cold test (if applicable for deployment region)
- [ ] Rain simulation (spray enclosure, check for leaks)
- [ ] Vibration test (simulate pole sway)
- [ ] Camera fog test (rapid temp changes, high humidity)
- [ ] Verify anti-fog measures are effective

#### Phase 3: Field Trial (4-6 weeks)
- [ ] Deploy prototype at representative site
- [ ] Monitor daily for first week
- [ ] Check weekly for remainder of trial
- [ ] Log any failures, warnings, or anomalies
- [ ] Collect user feedback from operators
- [ ] Measure actual solar generation vs predictions
- [ ] Verify video quality meets requirements
- [ ] Test remote access and data upload

#### Success Criteria
- [ ] Zero unplanned shutdowns during trial
- [ ] Battery never below 20% SOC
- [ ] All videos successfully uploaded
- [ ] No water ingress or component failures
- [ ] Operators able to perform basic maintenance
- [ ] Remote monitoring provides useful data

---

## Documentation & Training Materials

### Required Documentation (All Variants)

1. **Installation Guide**
   - Site survey checklist
   - Pole mounting instructions (photo-illustrated)
   - Camera positioning procedure with alignment tool
   - Cable routing and waterproofing
   - Initial power-on sequence
   - WiFi configuration steps
   - Cellular SIM installation

2. **Operation Manual**
   - Daily/weekly monitoring procedures
   - Status indicator meanings
   - Normal vs abnormal behavior
   - Data retrieval process
   - Maintenance mode usage

3. **Maintenance Guide**
   - 3-month maintenance checklist
   - 6-month maintenance checklist
   - Annual maintenance procedures
   - Desiccant replacement
   - Battery care and replacement
   - Camera cleaning procedures
   - Solar panel cleaning

4. **Troubleshooting Guide**
   - Flowchart-based problem diagnosis
   - Common issues and solutions
   - When to contact technical support
   - Remote support procedures
   - Factory reset process

5. **Spare Parts Catalog**
   - Illustrated parts breakdown
   - Part numbers and sources
   - Recommended spare parts inventory
   - Procurement contacts by region

### Training Program Recommendations

**Budget Variant (4-6 hours):**
- 1 hour: System overview and theory of operation
- 2 hours: Hands-on installation practice
- 1 hour: Maintenance procedures
- 1 hour: Troubleshooting scenarios
- 1 hour: Q&A and assessment

**Resilience Variant (6-8 hours):**
- 1.5 hours: System overview and advanced features
- 2 hours: Installation with emphasis on proper mounting
- 1 hour: Remote monitoring and telemetry
- 1.5 hours: Maintenance and repair procedures
- 1 hour: Advanced troubleshooting
- 1 hour: Q&A and assessment

**Ease-of-Use Variant (2-3 hours):**
- 0.5 hours: System overview (simplified)
- 1 hour: Hands-on installation (tool-free focus)
- 0.5 hours: Touch display interface walkthrough
- 0.5 hours: Basic maintenance
- 0.5 hours: Q&A and certification

---

## Next Steps

### Immediate Actions (Week 1)

1. **Stakeholder Review**
   - [ ] Circulate this document to key decision-makers
   - [ ] Gather feedback on variant preferences
   - [ ] Identify any missing requirements

2. **Budget Allocation**
   - [ ] Determine available budget per unit
   - [ ] Calculate number of units needed
   - [ ] Identify funding sources

3. **Site Assessment**
   - [ ] Identify initial deployment locations
   - [ ] Assess climate conditions (temperature range, solar potential)
   - [ ] Determine accessibility (influences maintenance frequency)

### Short-Term Actions (Weeks 2-4)

4. **Variant Selection**
   - [ ] Select primary variant based on decision framework
   - [ ] Determine if hybrid approach is needed
   - [ ] Finalize component specifications

5. **Procurement Planning**
   - [ ] Identify suppliers for each component
   - [ ] Get formal quotes (especially for bulk orders)
   - [ ] Check lead times for long-lead items
   - [ ] Place orders for prototype components

6. **Design Refinement**
   - [ ] Create detailed assembly drawings
   - [ ] Design internal layout and cable routing
   - [ ] Create labels and documentation templates

### Medium-Term Actions (Weeks 5-12)

7. **Prototype Build & Test**
   - [ ] Assemble first prototype
   - [ ] Complete bench testing
   - [ ] Complete environmental testing
   - [ ] Deploy field trial unit

8. **Documentation Development**
   - [ ] Write installation guide
   - [ ] Create maintenance procedures
   - [ ] Develop troubleshooting flowcharts
   - [ ] Design training materials

9. **Production Planning**
   - [ ] Based on prototype results, finalize BOM
   - [ ] Identify assembly location/team
   - [ ] Create quality control checklist
   - [ ] Plan production schedule

---

## Appendices

### Appendix A: Raspberry Pi 5 Power Consumption Data

Based on community testing and official specs:

| State | Power Draw | Notes |
|-------|-----------|-------|
| Idle (HDMI off, no peripherals) | 2.4W | Lowest power state while running |
| Idle (HDMI on) | 3.0W | Display connected |
| Light load (browsing, video playback) | 4.5W | Typical for camera preview |
| Heavy load (4K video encoding) | 8.0W | Peak during video processing |
| All cores maxed | 12W | Stress test, unlikely in normal use |

**For RC-Box duty cycle:**
- Recording (cameras + light processing): ~6W
- Encoding (heavy CPU load): ~8W
- Idle (between recordings): ~3W
- Assumed sleep/off: ~0.1W (RTC only)

### Appendix B: Camera Module V3 Specifications

| Parameter | Specification |
|-----------|---------------|
| Sensor | Sony IMX708, 11.9MP |
| Resolution | 4608 x 2592 (12MP stills), 1920x1080 (video) |
| Frame Rate | 1080p @ 30fps typical |
| Interface | CSI-2 (native) or USB via adapter |
| Power Consumption | ~0.3W active, 0W when disabled |
| Minimum Illumination | 0.5 lux (with good exposure) |
| Lens | Fixed focus (1m to infinity) |

**USB Adapter Considerations:**
- Arducam B0370: Supports dual cameras via USB3.0 hub
- Max cable length: 5m recommended (USB3.0 spec limit)
- Power: ~0.2W per adapter

### Appendix C: Environmental Performance Notes

#### Temperature Effects

**Cold Weather (<0°C):**
- LiFePO4 batteries cannot charge below 0°C (may need heating element or charge cutoff)
- LCD displays become sluggish below -10°C (TFT technology limitation)
- Camera lenses may frost (heated housings recommended below -5°C)
- Raspberry Pi operates to -20°C but throttles performance

**Hot Weather (>40°C):**
- Enclosure internal temps can reach +20°C above ambient (need ventilation or active cooling)
- LiFePO4 batteries degrade faster above 45°C (reduce charge voltage)
- Solar panels lose ~0.5% efficiency per °C above 25°C
- Camera sensors may produce noise in extreme heat

#### Humidity Effects

**High Humidity (>80% RH):**
- Condensation risk when temperature drops at night
- Camera lenses will fog without active prevention
- Silica gel saturates quickly (needs frequent replacement)
- Gore-Tex vents or active heating recommended

**Tropical Environments:**
- Rapid temperature swings at sunrise/sunset
- Near 100% humidity during rain
- Recommend heated camera housings or frequent desiccant changes
- Conformal coating on PCBs recommended

### Appendix D: Connectivity Considerations

#### Cellular Bands by Region

| Region | Key LTE Bands | Recommended Modem |
|--------|---------------|-------------------|
| Europe | B1, B3, B7, B20 | Quectel EC25-E |
| Americas | B2, B4, B5, B12, B17 | Quectel EC25-A |
| Asia-Pacific | B1, B3, B5, B8 | Quectel EC25-AU |
| Global (all regions) | Multi-band | Sierra Wireless EM7455 |

**Data Usage Estimates:**
- 1080p H.264 video @ 5Mbps = ~37.5 MB per 1-minute clip
- 2-3 min recording per cycle = ~75-110 MB per cycle
- 4 cycles per day = ~300-450 MB per day
- 30 days = ~9-13.5 GB per month

**Recommendation:** Plan for 15GB/month data allowance with margin

#### WiFi Configuration

**Hotspot Mode (for field configuration):**
- SSID: "RC-Box-[Serial Number]"
- Password: Printed on label inside enclosure
- IP: 192.168.4.1 (standard AP mode)
- Web interface for configuration

**Station Mode (normal operation):**
- Connect to predefined network (configured during install)
- Fallback to cellular if WiFi unavailable
- Automatic reconnection

### Appendix E: Mounting System Details

#### Pole Mounting Specifications

**Pole Diameter Compatibility:**
- Minimum: 2" (50mm)
- Maximum: 6" (150mm)
- Material: Steel, aluminum, wood, or concrete

**Mounting Methods by Variant:**

**Budget Variant (Hose Clamps):**
- 2x stainless steel hose clamps
- Rubber pad between clamp and enclosure
- Pros: Cheap, adjustable, available everywhere
- Cons: May loosen over time, requires periodic tightening

**Resilience Variant (U-Bolts):**
- Stainless steel U-bolts with anti-vibration pads
- Backing plate distributes load
- Pros: Very secure, resists vibration
- Cons: Less adjustable, requires specific size

**Ease-of-Use Variant (Ratchet Straps):**
- Heavy-duty ratchet straps (like backpack straps)
- Tool-free installation
- Pros: Fast, easy, no tools
- Cons: UV degradation, may stretch over time

#### Camera Mounting Specifications

**Ball Head Mounting (Budget/Resilience):**
- Standard 1/4"-20 thread (photo industry standard)
- Lock with single knob
- Pan: 360°, Tilt: -90° to +45°
- Typical: Manfrotto 492 or equivalent

**Magnetic Mount (Ease-of-Use):**
- Rare earth magnet base (25lb pull force)
- Articulating arm with quick-release plate
- Pros: Reposition without tools, fast setup
- Cons: Only works on ferrous poles, theft risk

**Pan/Tilt Mount (Resilience):**
- Heavy-duty pan/tilt head with dual lock knobs
- Stainless steel construction
- Maintains position under vibration
- Typical: Surveying equipment style

### Appendix F: Bill of Materials (Detailed)

*[Full itemized BOMs for each variant would be included here with part numbers, suppliers, and current pricing. Omitted for brevity but would include 50-80 line items per variant.]*

### Appendix G: Assembly Instructions (High-Level)

#### Budget Variant Assembly Sequence

1. Prepare enclosure (install cable glands, switches)
2. Mount Raspberry Pi 5 on standoffs
3. Install PiSugar 3 HAT
4. Mount storage SSD and cellular modem
5. Wire power connections (solar/grid)
6. Connect display to I2C header
7. Install camera adapters
8. Route and label all cables
9. Install status LEDs
10. Seal enclosure, verify IP67 integrity
11. Program and test system
12. Prepare camera housings with anti-fog measures
13. Final inspection and photography for documentation

*[Similar sequences would be provided for other variants]*

---

## Document Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-11-28 | System Architect | Initial draft for stakeholder review |

---

## Contact Information

**For questions or feedback on this document, contact:**

[Technical Lead Name]
[Organization]
[Email]
[Phone]

**For procurement inquiries:**

[Procurement Contact]
[Organization]
[Email]

**For deployment planning:**

[Operations Contact]
[Organization]
[Email]

---

**End of Document**
