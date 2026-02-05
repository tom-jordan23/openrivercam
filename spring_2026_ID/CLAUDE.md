# Indonesia Spring 2026 Deployment - Planning Guide

**Target:** March/April 2026 deployment of two ORC river monitoring stations in Indonesia
**Sites:** Sukabumi (solar, PoE camera) and Jakarta (AC power, PoE camera)
**Budget:** $3,000 USD total for both sites (target: less than $3,000)
**Stakeholder:** tjordan

---

## Overview

This document provides a structured approach for developing site-specific Bills of Materials for the two Indonesia deployments. Each site uses a different camera strategy based on power availability and lessons learned from previous deployments.

| Site | Power | Camera Strategy | Status |
|------|-------|-----------------|--------|
| Sukabumi | Solar (existing 200W/50Ah) | Factory-sealed PoE camera (power-cycled with Pi) | Replacement of failed unit |
| Jakarta | AC utility (new install) | Factory-sealed PoE cameras (continuous) | New training/demo site |

---

## Guiding Principles

All component and assembly decisions must follow these principles (from DESIGN_SPECS.md):

1. **Commodity electronics only** - No custom PCBs, no single-source components
2. **No fabrication or soldering** - All connections via screw terminals, plugs, or headers
3. **No specialized skills** - Assembly and maintenance by non-technical personnel
4. **Common tools only** - Phillips screwdriver, adjustable wrench, wire strippers
5. **Field serviceable** - Maximum 5 minutes to replace any component

**If a proposed solution requires cutting cables, soldering, or custom wiring, it must be redesigned.**

---

## Operating Parameters

### Status Display & Maintenance Mode

**Requirements:**

| Feature | Requirement |
|---------|-------------|
| Status display | Visual indication of system state (boot, capture, upload, error, sleep) |
| Visibility | Readable without opening enclosure (through window or external mount) |
| Maintenance mode | Tactile input (button/switch) to enter maintenance mode |
| Maintenance behavior | See below |

**Maintenance Mode Behavior:**
- Prevents auto-shutdown (stays awake indefinitely)
- Starts local WiFi hotspot (direct connection, no internet/Pangolin required)
- Enables SSH access over hotspot
- Status display shows "MAINTENANCE" and hotspot SSID/password
- Exit by: button press, reboot, or timeout (e.g., 30 min inactivity)

**Options to Research:**

Status Display:
- Small OLED (1.3" SSD1306, I2C) - low power, high contrast, works in sunlight
- LCD character display (16x2 or 20x4) - larger text, may need backlight
- LED array - simple status codes (green=OK, yellow=uploading, red=error)
- E-ink display - zero power when static, excellent sunlight readability

Maintenance Mode Input:
- IP67 momentary pushbutton (panel mount) - press to toggle mode
- IP67 toggle switch - physical ON/OFF for maintenance
- Magnetic reed switch - activate with external magnet through enclosure wall (no penetration needed)
- Hall effect sensor - similar to magnetic, no moving parts

**Design Considerations:**
- Display should be visible from ground level if unit is pole-mounted
- Maintenance input should be accessible but not accidentally triggered
- Both should be weatherproof (IP67) if externally mounted
- Consider combining: single button press = show status, long press = enter maintenance mode

---

### Conformal Coating

Electronics exposed to tropical humidity benefit from conformal coating - a thin protective layer that prevents moisture, dust, and corrosion damage.

**Components to consider coating:**
- Raspberry Pi 5 PCB (avoid connectors, GPIO pins, heat sink contact areas)
- Witty Pi 5 HAT+ PCB
- GPIO terminal block riser
- Relay modules
- Any exposed PCBs in the enclosure

**Coating Options:**

| Type | Application | Cure Time | Rework | Notes |
|------|-------------|-----------|--------|-------|
| **Acrylic (MG 422B)** | Brush/spray | 10-30 min | Easy (solvent) | Good general purpose, **NOT for >95% RH** |
| **Silicone (MG 422C)** ✅ | Brush/spray | 24 hr | Moderate | Flexible, wide temp range, **best for high humidity** |
| **Urethane** | Brush/spray | 24 hr | Difficult | Tough, chemical resistant |
| **Nano-coating (NeverWet, Liquipel)** | Spray | 30 min | N/A | Hydrophobic, but less robust |

**Recommendation:** ✅ **Silicone conformal coat (MG Chemicals 422C)** - MG 422B explicitly states it is NOT intended for extended exposure to >95% RH. Pure silicone (422C) performs better in tropical humidity.

**Application Notes:**
- Apply in low-humidity environment before deployment
- Mask off: GPIO pins, USB/HDMI ports, SD card slot, heat sink mounting points, any connectors
- Allow full cure before assembly
- Document which boards are coated (for future service)

---

### Internal Mounting Strategy

All components inside enclosures must be securely mounted - no loose items. **Mounting approach is an open research question - do not assume DIN rail.**

**Requirements:**
- Secure against vibration (pole-mounted units sway in wind)
- Field-serviceable with common tools
- Components swappable by semi-technical staff
- Good cable management
- Adequate airflow for heat dissipation
- No specialized skills for assembly

**Components to mount:**
- Raspberry Pi 5 + Witty Pi 5 HAT+ + GPIO terminal block riser (stacked)
- USB flash drive (Samsung FIT Plus) - plugs directly into Pi USB port
- Quectel modem + PU201 adapter
- Relay modules
- Terminal blocks
- Fuse holders
- PoE injector (both sites)
- Status display (must be visible externally)

**Options to Research:**

| Option | Notes |
|--------|-------|
| DIN rail (35mm) | Industrial standard; requires clips for each component |
| Standoffs + mounting plate | Direct PCB mounting; need hole spacing for each board |
| Velcro/dual-lock | Quick swap; heat and humidity concerns |
| 3M VHB tape | Very strong; difficult to remove for service |
| Custom mounting plate (laser-cut) | Tailored fit; requires design and fabrication |
| Pre-made Pi enclosures | May not fit HAT stack; check Pi 5 + Witty Pi compatibility |
| Modular industrial systems | Phoenix Contact, Wago, etc.; may be overkill |
| Pegboard/perforated plate | Flexible; amateur appearance |

**Research Questions:**
- What do professional outdoor IoT/telemetry deployments use?
- Are there complete Pi 5 industrial mounting kits?
- How to secure items without mounting holes (SSD, modem)?
- What works best in high-humidity tropical environments?
- What's the total cost comparison?

**Decision needed before BOM finalization.**

---

### Default Capture Schedule

| Phase | Duration | Notes |
|-------|----------|-------|
| Startup | ~20-30s | Pi boot, camera init, network |
| Video capture | 5s | Per camera |
| Data upload | Variable | Depends on connectivity |
| Shutdown | ~5s | Clean shutdown |
| Sleep | ~14 min | Until next cycle |
| **Cycle interval** | **15 minutes** | 96 cycles/day |

**Duty cycle estimate:** ~1-2 minutes active per 15-minute cycle = 6-13% duty cycle

This schedule drives power budget calculations. PoE cameras at Jakarta run 24/7; PoE camera at Sukabumi is power-cycled with the Pi (camera boots each cycle) to conserve solar power.

---

## Tools & Spares Inventory (PMI Office)

Keep the following at the local PMI office for field service. Covers both Sukabumi and Jakarta sites.

### Common Tools

| Tool | Qty | Notes |
|------|-----|-------|
| Phillips screwdriver set | 1 | #0, #1, #2 sizes |
| Adjustable wrench (6") | 1 | For cable glands, pole clamps |
| Wire strippers | 1 | For 18-22 AWG |
| Multimeter | 1 | DC voltage, continuity testing |
| Ethernet cable tester | 1 | For PoE camera troubleshooting (both sites) |
| Headlamp or flashlight | 1 | For enclosure work |
| Cable ties (assorted) | 1 bag | Cable management |
| Electrical tape | 2 rolls | |
| Laptop with SSH client | 1 | For maintenance mode access |
| Smartphone/tablet | 1 | WiFi hotspot connection, camera viewing |

### Spare Parts - Common (Both Sites)

| Item | Qty | Notes |
|------|-----|-------|
| Raspberry Pi 5 | 1 | Shared spare |
| Witty Pi 5 HAT+ | 1 | Shared spare |
| GPIO terminal block riser | 1 | |
| Samsung FIT Plus 256GB USB flash drive | 1 | Pre-imaged with OS if possible |
| SD card (32GB) with OS image | 2 | For quick Pi recovery |
| Quectel EG25-G modem + PU201 | 1 | Shared spare |
| LTE antenna | 2 | |
| USB-RS485 adapter | 1 | |
| IP67 panel-mount LEDs (Red/Yellow/Green) | 1 set | Status indication |
| Maintenance mode button/switch | 1 | |
| Inline fuse holders + fuses (5A, 10A) | 5 each | |
| Cable glands (M12, M16, M20) | 3 each | |
| Terminal blocks | 6 | Type TBD pending mounting research |
| **Mounting hardware** | 1 kit | DIN rail clips, standoffs, stainless hardware |
| Hydreon RG-15 rain gauge | 1 | Spare for either site |
| Silicone sealant (outdoor) | 1 tube | |
| Dielectric grease | 1 tube | |
| GORE vents (M12) | 2 | |

### Spare Parts - Sukabumi (PoE Camera / Solar)

| Item | Qty | Notes |
|------|-----|-------|
| PoE camera (same model as installed) | 1 | ANNKE C1200 (spare from 2-pack) |
| Cat6 outdoor cable (30m) | 1 | |
| IP68 RJ45 feedthrough connector | 2 | |
| PoE injector (Planet IPOE-260-12V) | 1 | Shared spare with Jakarta |

### Spare Parts - Jakarta (PoE Camera / AC Power)

| Item | Qty | Notes |
|------|-----|-------|
| PoE camera (same model as installed) | 1 | ANNKE C1200 or Reolink |
| Cat6 outdoor cable (30m) | 1 | |
| IP68 RJ45 feedthrough connector | 2 | |
| RJ45 connectors + boots | 10 | |
| RJ45 crimp tool | 1 | |
| PoE injector (Planet IPOE-260-12V or equiv) | 1 | |
| AC-DC power supply | 1 | Match installed unit |
| Surge protector | 1 | |
| UPS battery (if replaceable) | 1 | Match installed UPS |

### Consumables

| Item | Qty | Notes |
|------|-----|-------|
| SIM cards (pre-activated) | 2 | For modem replacement |
| ~~Desiccant packs~~ | ~~10~~ | **NOT NEEDED** - desiccant + Gore vents is not viable at 95% RH |
| Conformal coat (MG 422C silicone) | 1 bottle | For replacement board coating |
| Masking tape | 1 roll | For conformal coating prep |
| Cable ties (assorted) | 1 bag | |
| Heat shrink tubing | 1 set | |
| Isopropyl alcohol wipes | 1 pack | Cleaning contacts, pre-coating prep |
| Microfiber cloths | 5 | Cleaning camera lenses |
| Stainless steel screws/standoffs | 1 kit | Assorted M2.5, M3 sizes |
| Velcro/dual-lock strips | 1 pack | For SSD mounting |

### Documentation (Laminated)

| Document | Qty | Notes |
|----------|-----|-------|
| Wiring diagram - Sukabumi | 2 | Inside enclosure + spare |
| Wiring diagram - Jakarta | 2 | Inside enclosure + spare |
| Troubleshooting guide | 2 | Quick reference flowchart |
| Maintenance mode instructions | 2 | Hotspot SSID, default password, SSH commands |
| Contact information | 2 | Emergency contacts, support numbers |

---

## BOM Development Steps

### Phase 1: Requirements Validation

1. ~~**Review SITES.md** - Confirm equipment lists with stakeholders~~ ✓ Complete (stakeholder: tjordan)
2. **Cross-reference research** - Check `/rc-box/research/camera_options_summary.md` for camera decisions
3. **Verify existing equipment** - Confirm Sukabumi's solar system specs and condition
4. **Validate capture schedule** - 5s video every 15 min affects power budget and storage sizing

### Phase 2: Sukabumi BOM Development

#### 2.1 Compute Platform
- [x] Raspberry Pi 5 8GB
- [x] Witty Pi 5 HAT+ for scheduling + RTC
- [x] Adafruit Pi-EzConnect (GPIO terminal block riser)
- [x] Samsung FIT Plus 256GB USB flash drive (IP67, plugs directly into Pi)
- [x] Quectel EG25-G modem + PU201 adapter
- [x] Proxicast ANT-122-S02 MIMO LTE puck antenna (IP67, eliminates SMA bulkhead connectors)
- [x] USB-RS485 adapter for Modbus/rain gauge
- [x] 3× IP67 panel-mount LEDs (Red/Yellow/Green)
- [x] IP67 momentary pushbutton for maintenance mode

#### 2.2 PoE Camera System
- [x] PoE camera: ANNKE C1200 (12MP, built-in IR LEDs) - 1 installed, 1 spare from 2-pack
- [x] Planet IPOE-260-12V PoE injector (native 12V input from solar battery)
- [x] Outdoor Cat6 shielded cable
- [x] IP68 RJ45 waterproof couplers
- [x] Pole mount bracket (stainless steel)

**Power-Cycled Operation:** PoE injector powered from same switched 12V circuit as Pi. Camera boots when Pi wakes (~45-60s boot time), captures, then powers down with Pi sleep cycle. Active phase extended to ~150s per cycle to accommodate boot + capture + upload.

**IR Illumination:** Built-in IR LEDs on ANNKE C1200 handle day/night automatically. No separate IR illuminator or relay needed.

#### 2.4 Enclosure & Mounting
- [ ] Small enclosure for Pi/electronics (sized to fit within existing power box, or separate)
- [ ] Cable glands (M12, M16, M20 as needed)
- [ ] **Internal mounting system** - TBD pending research (DIN rail, standoffs, mounting plate, etc.)
- [ ] Terminal blocks
- [ ] Fuse holders
- [ ] Strain relief for cables
- [ ] Stainless steel hardware

#### 2.5 Conformal Coating & Protection
- [ ] Silicone conformal coat (MG 422C) - for Pi, Witty Pi, GPIO riser, relay modules
- [ ] Masking tape (for protecting connectors during coating)
- [ ] Application brush or spray

#### 2.6 Rain Gauge
- [x] Hydreon RG-15 optical rain gauge (~$99) - solid-state, no moving parts, self-cleaning
- [x] RS232 TTL 3.3V output connects directly to Pi UART via Pi-EzConnect terminals
- [x] Built-in mounting holes (no separate bracket needed)

### Phase 3: Jakarta BOM Development

#### 3.1 Power System (AC)
- [ ] AC-DC power supply (12V/10A or 24V/5A industrial grade)
- [ ] UPS system (size for 24hr backup at ~50W load)
- [ ] Surge protector (critical for Indonesia power quality)
- [ ] Power distribution (terminal blocks, fuses)

#### 3.2 Enclosure & Mounting
- [ ] Outdoor enclosure with active cooling (research options)
- [ ] GORE vent for pressure equalization
- [ ] Cable glands (M12, M16, M20 as needed)
- [ ] **Internal mounting system** - TBD pending research (DIN rail, standoffs, mounting plate, etc.)
- [ ] Terminal blocks
- [ ] Fuse holders
- [ ] Strain relief for cables
- [ ] Stainless steel hardware
- [ ] Conformal coat supplies (same as Sukabumi)

#### 3.3 Compute Platform
- [ ] Same as Sukabumi (Pi 5, Witty Pi 5 HAT+, **GPIO terminal block riser**, SSD, modem, **status display**, **maintenance input**)

#### 3.4 PoE Camera System
- [ ] 2x PoE cameras: ANNKE C1200 (12MP) or Reolink RLC-810A (8MP)
- [ ] 12V PoE injector or switch (Planet IPOE-260-12V or equivalent)
- [ ] Outdoor Cat6 shielded cable
- [ ] IP68 RJ45 feedthrough connectors
- [ ] Pole mount brackets (stainless steel)

#### 3.5 Infrastructure
- [ ] Mounting pole + installation hardware
- [ ] Grounding system (rod, cable, lugs)

#### 3.6 Rain Gauge
- [x] Hydreon RG-15 optical rain gauge (~$99) - solid-state, no moving parts, self-cleaning
- [x] RS232 TTL 3.3V output connects directly to Pi UART via Pi-EzConnect terminals
- [x] Built-in mounting holes (no separate bracket needed)

### Phase 4: Validation

1. **Price verification** - Get current pricing from suppliers
2. **Availability check** - Confirm stock and lead times
3. **Compatibility testing** - Verify critical integrations work
4. **Power budget calculation** - Confirm system can run on available power
5. **Thermal analysis** - Verify components rated for tropical temperatures

---

## Research Plan (Phased)

Research is organized into phases with checkpoints. Complete each phase and get feedback before proceeding. This reduces risk of going down the wrong path.

---

### Phase 1: Foundational Decisions (BLOCKING) ✅ COMPLETE

These decisions affect multiple downstream choices. Complete first.

| # | Topic | Question to Answer | Deliverable | Status |
|---|-------|-------------------|-------------|--------|
| 1.1 | **Internal mounting solutions** | What's the best way to mount Pi + HATs, SSD, modem, relays inside enclosures? | Comparison table of options (DIN rail, standoffs, plates, etc.) with recommendation | ✅ **DIN rail (35mm) approved** |
| 1.2 | **GPIO terminal block riser** | Does a stackable riser exist that works with Witty Pi 5 HAT+ on Pi 5? | Specific product recommendation or "not available" | ✅ **Adafruit Pi-EzConnect (ID 2711) approved** - $19.95 |
| 1.3 | **Camera/enclosure humidity tolerance** | Can IMX317/IMX219 sensors operate at 80-95% RH? | Yes/No + source. Determines humidity management strategy | ✅ **See decisions below** |

**Checkpoint 1:** ✅ APPROVED (January 8, 2026)

#### Phase 1 Decisions - Humidity Management Strategy

**Key Finding:** Passive desiccant + Gore vents is NOT viable at 95% RH. Desiccant saturates in days due to vapor permeability of Gore vents. Industry standard is conformal coating + active heating.

**Decision: Site-specific approach**

| Site | Strategy | Rationale |
|------|----------|-----------|
| **Jakarta** (AC power) | Conformal coating (MG 422C) + PTC heaters + Gore vents | Full industrial approach - reference site for testing |
| **Sukabumi** (solar) | Conformal coating (MG 422C) + Gore vents only (NO heaters) | Avoid solar system upgrade; test coating-only approach |

**Jakarta humidity protection:**
- Silicone conformal coating (MG 422C) on all PCBs
- PTC heaters in compute enclosure for nighttime humidity control
- Gore M12 vents for pressure equalization
- NO desiccant
- PoE cameras are factory-sealed IP67 - no additional camera housing protection needed

**Sukabumi humidity protection:**
- Silicone conformal coating (MG 422C) on all PCBs
- Gore M12 vents for pressure equalization
- NO heaters (power budget constraint)
- NO desiccant
- PoE camera is factory-sealed IP67 - no additional camera housing protection needed
- Accept higher failure risk for compute enclosure; budget for replacement parts

**Research documents:**
- `research/internal_mounting_solutions_research.md`
- `research/gpio_terminal_block_research.md`
- `research/sealed_camera_module_research.md`
- `research/humidity_management_tropical_enclosures_research.md`
- `research/witty_pi_5_research.md`
- `research/GPIO_STACKING_ANALYSIS.md`

---

### Phase 2: User Interface Components ✅ COMPLETE

Status display and maintenance mode - common to both sites.

| # | Topic | Question to Answer | Deliverable | Status |
|---|-------|-------------------|-------------|--------|
| 2.1 | **Status display** | Which display type works best? (OLED, LCD, LED, e-ink) | Comparison with recommendation | ✅ **LED array approved** (3× 10mm IP67 LEDs: Red/Yellow/Green) |
| 2.2 | **Maintenance mode input** | What's the best tactile input? (button, switch, magnetic) | Specific product recommendation | ✅ **IP67 pushbutton approved** (C&K AP Series or E-Switch PVA6) |
| 2.3 | **Conformal coating procedure** | ~~Is MG 422B appropriate?~~ **MG 422C selected.** What to mask on Pi 5? | Application procedure document | ✅ **Procedure complete** |

**Checkpoint 2:** ✅ APPROVED (January 8, 2026)

#### Phase 2 Decisions Summary

**Status Display:** 3× 10mm IP67 panel-mount LEDs
- Green = OK/Ready
- Yellow = Working (capture, upload)
- Red = Error
- Cost: ~$10-20 total
- Visible at 3-5m distance, excellent sunlight readability

**Maintenance Mode Input:** IP67 momentary pushbutton
- C&K AP Series ($8-14) or E-Switch PVA6 Series ($12-18)
- 16mm panel hole + PG9 cable gland
- Recessed mounting prevents accidental activation
- Long press (3s) = enter maintenance mode

**Conformal Coating:** MG 422C silicone
- See `research/conformal_coating_procedure.md` for detailed masking and application

**Research documents:**
- `research/status_display_research.md`
- `research/maintenance_input_research.md`
- `research/conformal_coating_procedure.md`

---

### Phase 3: Sukabumi-Specific (PoE Camera / Solar) ✅ COMPLETE (UPDATED)

Depends on Phase 1 decisions. **Updated January 2026: Switched from USB camera to PoE camera approach.**

| # | Topic | Question to Answer | Deliverable | Status |
|---|-------|-------------------|-------------|--------|
| 3.1 | **PoE camera selection** | Which factory-sealed PoE camera with built-in IR? | Product recommendation | ✅ ANNKE C1200 (12MP, built-in IR) |
| 3.2 | **PoE power strategy** | How to power PoE from 12V solar? | PoE injector with native 12V input | ✅ Planet IPOE-260-12V |
| 3.3 | **Power cycling** | Can camera boot fast enough for duty-cycled operation? | Boot time verification | ✅ ~45-60s boot, 150s active cycle |

**Checkpoint 3:** ✅ APPROVED (January 30, 2026) - Updated to PoE camera approach

#### Phase 3 Decisions Summary

**PoE Camera System:**
- ANNKE C1200 PoE IP camera (12MP, 134° FOV, built-in IR LEDs)
- Factory-sealed IP67 housing eliminates humidity concerns
- 2-pack purchased: 1 installed, 1 spare
- Same camera model as Jakarta site for parts commonality

**PoE Power Strategy:**
- Planet IPOE-260-12V PoE injector (native 12V input)
- Powered from 12V solar battery via Witty Pi switched circuit
- Camera power-cycled with Pi to conserve solar budget

**Power Budget Impact:**
- Higher than USB camera approach (~94 Wh/day vs ~47 Wh/day)
- Still within solar capacity (200W panel generates ~720 Wh/day)
- 3.2 days autonomy with 50Ah battery

**Research documents:**
- `research/poe_injector_research.md` (same as Jakarta)
- BOM_Sukabumi.md Section 2 for full details

---

### Phase 4: Jakarta-Specific (PoE Camera / AC Power) ✅ COMPLETE

Depends on Phase 1 decisions. Can run in parallel with Phase 3.

| # | Topic | Question to Answer | Deliverable | Status |
|---|-------|-------------------|-------------|--------|
| 4.1 | **Tropical enclosure cooling** | What cooling options work for 40°C+ ambient? | Comparison of thermoelectric, fan, passive options with power draw | ✅ Passive cooling (budget decision) |
| 4.2 | **24hr UPS system** | What 12V UPS can provide ~1200Wh backup? | Product options with cost/size comparison | ✅ LiFePO4 100Ah + charger |
| 4.3 | **PoE injector verification** | Confirm Planet IPOE-260-12V works with 12V battery input | Datasheet confirmation or alternative | ✅ Confirmed - native 12V support |
| 4.4 | **AC power supply** | Which industrial 220V→12V supply? | Product recommendation rated for Indonesia power quality | ✅ Mean Well SDR-120-12 |

**Checkpoint 4:** ✅ APPROVED (January 8, 2026)

#### Phase 4 Decisions Summary

**Site Context:** Jakarta is coastal/urban (hotter). Sukabumi is foothills (cooler).

**Enclosure Cooling (Budget Approach):**
- ~~Peltier cooler~~ - too expensive (~$1,800)
- **Passive cooling strategy:**
  - Oversized aluminum enclosure (~400x300x200mm) for thermal mass
  - Mount in shaded location (under eave, north-facing)
  - Internal heat sinks on Pi 5 and PoE injector
  - Gore vent for pressure equalization
  - Accept internal temps up to 55-60°C on hottest days (Pi 5 throttles at 80°C)
- PTC heater still used for nighttime humidity control
- Cost: ~$100-150 vs $1,800 for active cooling

**24hr UPS System:**
- 12V 100Ah LiFePO4 battery (~$300-400)
- 20A LiFePO4 charger (~$80-100)
- Victron BatteryProtect (~$50-80)
- Total: ~$500-630
- Runtime: 20-25 hours at 50W load
- LiFePO4 chosen for tropical heat tolerance (vs AGM which degrades above 30°C)

**PoE Injector:**
- Planet IPOE-260-12V ✅ CONFIRMED
- Native 12-56V DC input (no external converter needed)
- 2× PoE+ ports, 60W total @ 12V input
- Handles 2 cameras easily (~30W total)
- Price: ~$164

**AC Power Supply:**
- Mean Well SDR-120-12 (DIN rail)
- 88-264V AC input (handles Indonesia voltage swings)
- 12V/10A output (120W)
- Active PFC + SEMI F47 voltage sag immunity
- Price: ~$55-105
- Add external Type 2 surge protector for lightning

**PTC Heaters (humidity control):**
- Camera housing: 5-7W heater (~$25-35)
- Compute enclosure: 10-15W heater (~$30-40)
- Total: ~$55-75

**Research documents:**
- `research/enclosure_cooling_research.md`
- `research/ups_backup_research.md`
- `research/poe_injector_research.md`
- `research/ac_power_supply_research.md`

---

### Phase 5: Connectivity & Optional ✅ COMPLETE

Lower priority. Can be deferred if needed.

| # | Topic | Question to Answer | Deliverable | Status |
|---|-------|-------------------|-------------|--------|
| 5.1 | **Indonesian cellular** | Does EG25-G support Telkomsel, Indosat, XL bands? | Band compatibility confirmation | ✅ EG25-G fully compatible, use Telkomsel |
| 5.2 | **Rain gauge** | What rain gauge is available? | Product recommendation | ✅ Pulse tipping bucket (both sites) |
| 5.3 | **ORC software check** | Does current software handle single-camera config? | Yes/No + any required changes | ✅ Validated - hardware IR approach bypasses issues |

**Checkpoint 5:** ✅ APPROVED (January 8, 2026)

#### Phase 5 Decisions Summary

**Indonesian Cellular:**
- Quectel EG25-G confirmed compatible with all Indonesian carriers
- **Recommended carrier: Telkomsel** (98% coverage, best for rural Sukabumi)
- Bands supported: B1, B3, B5, B8, B40 - covers all major carriers

**Rain Gauge (BOTH SITES):**
- **Hydreon RG-15** optical rain gauge (~$99)
- Solid-state, no moving parts, self-cleaning lens
- RS232 TTL 3.3V output connects directly to Pi UART
- Resolution: 0.2mm or 0.02mm (configurable)
- Very low power: ~150µA sleep, 15mA active
- Operating temp: -40°C to +60°C

**ORC Software:**
- PoE cameras with built-in IR handle day/night automatically - no software changes needed
- Both sites now use identical PoE camera approach (ANNKE C1200)
- RTSP capture via ffmpeg already supported in ORC

**Research documents:**
- `research/indonesian_cellular_research.md`
- `research/rain_gauge_research.md`
- `research/orc_software_compatibility.md`

---

### Phase 6: Pricing & Availability

Only after component selections are finalized.

| # | Topic | Deliverable |
|---|-------|-------------|
| 6.1 | **Sukabumi BOM pricing** | Complete BOM with current prices, sources, lead times |
| 6.2 | **Jakarta BOM pricing** | Complete BOM with current prices, sources, lead times |
| 6.3 | **Spares inventory pricing** | Priced list for PMI office stock |
| 6.4 | **Shipping strategy** | What to ship vs. source locally in Indonesia |

**Checkpoint 6:** Final BOM review. Confirm total cost is acceptable.

---

### Phase 6.5: Customs & Import Review

Evaluate customs and import considerations for traveling US → Indonesia with equipment.

| # | Topic | Deliverable |
|---|-------|-------------|
| 6.5.1 | **Air travel restrictions** | LiFePO4 battery rules, lithium limits, carry-on vs checked |
| 6.5.2 | **Indonesian customs duties** | Duty rates for electronics, cameras, batteries |
| 6.5.3 | **Import permits/certifications** | IMEI registration for modems, any required permits |
| 6.5.4 | **Documentation needed** | Commercial invoice, packing list, equipment manifest |
| 6.5.5 | **Items to source locally** | Heavy/restricted items better purchased in Indonesia |
| 6.5.6 | **Carnet ATA consideration** | Temporary import for equipment that will be installed |

**Key Considerations:**
- LiFePO4 batteries have airline Wh limits (typically 100Wh carry-on, 160Wh with approval)
- Indonesian customs may charge duty on electronics (0-15% typical)
- Modems with IMEI may require registration with Indonesian telecom authority
- Solar panels/large batteries may be better sourced in Indonesia
- Document everything as "professional equipment for installation" not "goods for sale"

**Checkpoint 6.5:** Customs strategy confirmed. Packing list finalized.

---

### Phase 7: Documentation

After all decisions are made.

| # | Topic | Deliverable |
|---|-------|-------------|
| 7.1 | **Assembly guide - Sukabumi** | Step-by-step with photos/diagrams |
| 7.2 | **Assembly guide - Jakarta** | Step-by-step with photos/diagrams |
| 7.3 | **Troubleshooting guide** | Flowchart for common issues |
| 7.4 | **Wiring diagrams** | Both sites, lamination-ready |

**Final Checkpoint:** Documentation review before production.

---

## Specialized Agents

| Agent | Use For |
|-------|---------|
| `comprehensive-researcher` | Product research, comparisons, pricing |
| `documentation-expert` | Assembly guides, procedures |
| `backend-architect` | Power budget calculations |
| `Explore` | Cross-checking against existing specs |
| `security-engineer` | Safety review (surge, grounding, fusing) |

---

## Validation and Fact-Checking

### Price Verification
1. Check DigiKey, Mouser for electronics with specific part numbers
2. Check Amazon for consumer items (cameras, enclosures, cables)
3. Get quotes from specialty suppliers (Planet Technology, VA Imaging)
4. Record date of price check - prices change

### Specification Verification
1. Cross-reference camera specs against `/rc-box/research/camera_options_summary.md`
2. Verify temperature ratings meet -20C to +50C minimum
3. Confirm IP ratings (IP67 minimum for outdoor components)
4. Check power consumption against budget

### Compatibility Verification
1. PoE cameras (ANNKE C1200) support RTSP and work with ffmpeg
2. Planet IPOE-260-12V works with native 12V input (both sites)
3. Modem works with Indonesian carriers
4. Witty Pi 5 HAT+ compatible with Pi 5

### Lead Time Verification
1. Check stock status at time of ordering
2. Add buffer for international shipping to Indonesia
3. Account for customs clearance (see DESIGN_SPECS.md shipping section)

---

## Potential Gaps and Missing Items

Based on research review, the following items may need attention:

### Sukabumi Site

| Gap | Risk | Action Needed |
|-----|------|---------------|
| **PoE camera boot time** | Low | Camera needs ~45-60s to boot each cycle. Active phase extended to 150s. ✅ Resolved |
| **Higher power consumption** | Low | PoE camera uses ~94 Wh/day vs ~47 Wh/day for USB. Solar capacity (720 Wh/day) is adequate. ✅ Resolved |
| **Cat6 cable routing** | Low | Need UV-resistant outdoor Cat6 from enclosure to camera. ✅ In BOM |

**Note:** Switching to factory-sealed PoE camera (ANNKE C1200) eliminates previous USB camera risks: IR sensitivity, Gore vent housing, humidity management, custom housing assembly.

### Jakarta Site

| Gap | Risk | Action Needed |
|-----|------|---------------|
| **Active cooling for enclosure** | High | SITES.md mentions active cooling but no research exists. Need to specify: thermoelectric, exhaust fan, or AC unit |
| **UPS sizing** | High | 24hr backup at ~50W load = 1200Wh. This is a large UPS. Research 12V UPS options or consider separate battery bank |
| **12V PoE switch vs injector** | Medium | SITES.md says "12v PoE switch" but most PoE switches need 48V. Planet IPOE-260-12V is an injector, not a switch. Clarify network topology |
| **AC input voltage** | Low | Indonesia uses 220V/50Hz. Verify power supply accepts 220V |
| **Mounting pole** | Low | No specs for pole. Standard camera pole or custom? Height? Material? |
| **Camera RTSP configuration** | Low | Cameras ship with RTSP disabled. Pre-configure before deployment |

### Both Sites

| Gap | Risk | Action Needed |
|-----|------|---------------|
| **GPIO terminal block riser** | Medium | Need to source HAT/riser that exposes GPIO as screw terminals while Witty Pi 5 HAT+ is installed. Enables future expansion without resoldering |
| **Modbus sensor details** | Medium | What device will connect via Modbus? Rain gauge? Water level sensor? External data logger? Need to specify interface requirements |
| **SIM card strategy** | Medium | Pre-paid or postpaid? Which carrier? Data plan size? |
| **ORC software compatibility** | Low | Both sites use PoE cameras with built-in IR - standard RTSP capture, no special day/night handling needed |
| **Shipping strategy** | Low | Batteries/panels may need local sourcing per DESIGN_SPECS.md shipping section |
| **Customs documentation** | Low | Prepare commercial invoices, HS codes, IMEI list for modems |

### Research Status

See **Research Plan (Phased)** section above for organized research tasks with checkpoints.

**Current Phase:** Phase 1 ✅ Phase 2 ✅ Phase 3 ✅ Phase 4 ✅

**Next Action:** Phase 5 (Connectivity/Optional) then Phase 6 (Pricing & BOM finalization)

---

## File References

Key documents for BOM development:

| Document | Location | Contents |
|----------|----------|----------|
| Previous verified BOM | `/rc-box/BOM_VERIFIED.md` | PoE camera approach, pricing |
| Design specifications | `/rc-box/DESIGN_SPECS.md` | Requirements, principles, shipping |
| Camera options research | `/rc-box/research/camera_options_summary.md` | Camera comparison, recommendations |
| PoE camera boot times | `/rc-box/research/ip_camera_boot_times.md` | Camera startup timing |
| PoE power research | `/rc-box/research/poe_power_12v.md` | 12V to PoE conversion |
| Nitrogen/sealed enclosures | `/rc-box/research/nitrogen_sealed_enclosures.md` | Housing options |

---

## Workflow

### Creating Sukabumi BOM

```
1. Start with compute platform (Pi 5, Witty Pi 5 HAT+, GPIO terminal block riser, USB flash drive, modem)
2. Add PoE camera system (ANNKE C1200 + Planet IPOE-260-12V injector)
3. Size enclosure based on components
4. Calculate power budget against existing 200W/50Ah system
5. Add rain gauge (Hydreon RG-15)
6. Get pricing from suppliers
7. Review against guiding principles (no fabrication, commodity parts only)
```

### Creating Jakarta BOM

```
1. Start with power system research (UPS, cooling)
2. Size enclosure for all components + cooling
3. Add compute platform (Pi 5, Witty Pi 5 HAT+, GPIO terminal block riser, SSD, modem)
4. Select PoE cameras from camera_options_summary.md
5. Design PoE power distribution (injector vs switch)
6. Add mounting infrastructure
7. Add surge protection and grounding
8. Calculate power budget
9. Get pricing from suppliers
10. Review against guiding principles (no fabrication, commodity parts only)
```

---

## Success Criteria

BOMs are complete when:

- [ ] All items from SITES.md are addressed
- [ ] Each line item has: quantity, description, part number (if applicable), unit price, source
- [ ] **No soldering, cable cutting, or fabrication required** - all connections via screw terminals or plug-in
- [ ] **GPIO terminal block riser included** for future expansion
- [ ] Power budget calculated and verified
- [ ] Temperature ratings verified for all outdoor components
- [ ] IP ratings verified (IP67+ for outdoor)
- [ ] Prices verified with date stamp
- [ ] Lead times checked
- [ ] Shipping strategy defined
- [ ] Gaps/risks documented with mitigation
- [ ] Assembly/installation notes included
- [ ] Spare parts list defined
