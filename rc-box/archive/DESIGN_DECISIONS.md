# RC-Box Design Decisions

This document captures confirmed design decisions for the RC-Box hardware platform.

## Confirmed Decisions (2024-11-28)

### 1. Camera System
- **Decision**: Pi Camera V3 via USB adapter preferred
- **Alternative**: Commodity USB cameras acceptable if they use the Pi V3 chipset (Sony IMX708)
- **Rationale**: Maintains image quality consistency while allowing field replacement flexibility
- **Housing**: Separate weatherproof housings for each camera (not integrated into main enclosure)

### 2. Power Duty Cycle
- **Decision**: 2-3 minutes of runtime every 15 minutes
- **Calculated**: ~8-12 minutes per hour = 192-288 minutes/day (~3.2-4.8 hours/day)
- **Implications**:
  - ~20% duty cycle
  - Significant power savings from scheduled operation
  - RTC wake capability required
  - **Must account for rainy seasons and reduced winter sunlight at higher latitudes** (solar sizing)

### 3. Storage Capacity
- **Decision**: 1-2 weeks of video storage with no connectivity
- **Calculated**: At 1080p30 H.264 (~5 Mbps), 4.8 hours/day = ~10.8 GB/day
  - 1 week = ~75 GB
  - 2 weeks = ~150 GB
- **Recommendation**: Minimum 256GB storage, 512GB preferred for safety margin
- **Requirements**:
  - Storage must be extensible (support for additional/larger drives)
  - Storage must be field serviceable (easy replacement without special tools)

### 4. Enclosure Style
- **Decision**: NEMA-style enclosure for main electronics
- **Mounting Options**:
  - Primary: Utility pole, 3-6" (75-150mm) diameter
  - Secondary: Pre-existing structures (bridges, buildings, etc.)
- **Implications**:
  - Need versatile mounting system for both poles and flat surfaces
  - Standard NEMA enclosure allows use of off-the-shelf components
  - **Cameras in separate weatherproof housings** (confirmed)

### 5. Physical Controls
- **Confirmed switches**:
  1. Power switch (on/off)
  2. Mode switch (normal/maintenance)
  3. WiFi hotspot toggle
  4. Reset button (recessed)
- **Style**: No preference; must meet IP67 rating

### 6. Mounting System
- **Main enclosure**: Fixed mount to pole or structure (no adjustment needed post-install)
- **Camera mounts**:
  - Adjustable during initial setup
  - Lock-down mechanism after adjustment
  - Ball joint or pan/tilt head with locking screws
  - Each camera independently adjustable
- **Note**: Only cameras require repositioning capability; Pi enclosure is fixed

### 7. Connectivity
- **Decision**: Both cellular AND WiFi required
- **Cellular**:
  - Global deployment; SIM cards procured locally per region
  - Modem must support multi-band for worldwide compatibility
  - USB dongle or HAT form factor
- **WiFi**:
  - For local configuration/hotspot mode
  - Failover logic between cellular and WiFi networks

### 8. Status Display
- **Decision**: Display screen preferred (over LEDs only)
- **Implications**:
  - Small OLED/LCD display (128x64 or similar)
  - Must be sunlight readable
  - Must be visible through enclosure (window or external mount)
  - Shows: mode, battery %, network status, storage, errors

### 9. Operating Temperature Range
- **Decision**: Equatorial tropics to freezing temperatures
- **Interpreted range**: -20°C to +50°C (-4°F to 122°F)
- **Implications**:
  - LiFePO4 battery chemistry (better cold performance than LiPo)
  - May need heating element for extreme cold
  - Thermal management for hot climates
  - Component selection must meet industrial temp ratings
  - **Camera housing must prevent lens condensation in hot, humid environments**

### 10. IP Rating
- **Decision**: IP67 target
- **Meaning**: Dust-tight, protected against temporary immersion (1m for 30 min)
- **Implications**:
  - All cable entries need IP67-rated glands
  - Display window must maintain seal
  - Switches must be IP67-rated or use sealed membrane
  - Careful attention to gasket design

---

## Derived Requirements

Based on the above decisions, the following requirements are derived:

### Power Budget (Preliminary)
| Component | Active Power | Standby Power |
|-----------|-------------|---------------|
| Raspberry Pi 5 | 5-8W | <1W (with RTC wake) |
| 2x Pi Camera V3 | ~0.5W each | 0W |
| Display | 0.1-0.5W | 0W |
| Cellular modem | 2-4W (transmit) | 0.1W |
| WiFi | 0.5-1W | 0W |
| Storage (SSD) | 0.5-2W | 0W |
| **Total Active** | **~10-17W** | |
| **Total Standby** | | **~1-2W** |

**Daily Energy Estimate**:
- Active: 15W × 4.8 hours = 72 Wh
- Standby: 1.5W × 19.2 hours = 29 Wh
- **Total: ~100 Wh/day**

### Power Configurations
Two deployment configurations supported (either/or, not both simultaneously):

**Configuration A: Solar-Powered**
- Solar panel + battery + charge controller
- 3-5 days battery autonomy = 300-500 Wh
- Solar panel sized for worst-case conditions (rainy season, high latitude winter)
- Estimated panel: 50-100W (depends on location analysis)

**Configuration B: Grid-Powered**
- AC adapter input (universal 100-240V)
- Small backup battery for graceful shutdown during outages
- Simpler installation where grid power available

### Storage Sizing
- 512GB M.2 NVMe SSD recommended (or larger)
- Provides ~3-4 weeks of storage at calculated rates
- Faster and more reliable than SD card
- Must support field replacement

### Camera Housing Requirements
- Separate IP67-rated housings for each camera
- **Off-the-shelf housing acceptable** if it meets anti-fog requirements
- Adjustable mount with locking mechanism
- Cable gland for USB connection to main enclosure

### Anti-Fog System (MANDATORY - All Variants)

**Problem**: Passive desiccant-only solutions have failed in Indonesia deployment. Silica gel saturates within days in 90-100% RH tropical environments and cannot prevent condensation when lens temperature drops below dew point.

**Required Solution**: Active anti-fog system with multiple layers:

| Component | Specification | Purpose | Est. Cost |
|-----------|--------------|---------|-----------|
| **Pressure-equalizing vent** | Gore PMF200408 or Nitto TEMISH | Eliminates moisture pumping from thermal cycling | $15 |
| **Molecular sieve desiccant** | Type 4A, 100g per housing | Works at >90% RH (unlike silica gel) | $8 |
| **Lens heater** | 12V 5W astronomy-style heater ring | Keeps lens above dew point | $25 |
| **Thermostat controller** | STC-1000 or equivalent | Activates heater when temp <25°C | $18 |
| **Anti-fog coating** | Cat Crap or equivalent | Backup: makes any condensation transparent | $7 |
| **Per camera total** | | | **$73** |

**Power Impact**:
- Heater draws 5W when active
- Thermostat control limits runtime to ~6-8 hours/night
- **Additional 30-50 Wh/day per camera** (60-100 Wh/day total for 2 cameras)
- Solar configuration must add 75-100W panel capacity

**Field Service Kit** (include with each deployment):
- 4x spare molecular sieve desiccant packs
- 1x spare lens heater
- 1x Cat Crap anti-fog paste
- 1x spare breather vent
- **Kit cost: ~$75**

**Maintenance**:
- Replace/regenerate desiccant every 6 months
- Reapply anti-fog coating during maintenance visits
- Check heater function annually

**Expected Performance**: 95%+ elimination of fog/condensation events

---

## Open Questions (Follow-up Required)

### Camera System
- [ ] USB adapter solution: Arducam or other? Need to test Pi 5 compatibility
- [ ] Cable length limit for USB camera connection?
- [ ] Specific off-the-shelf camera housing model to evaluate?

### Power System
- [x] ~~Solar charging required?~~ → Yes, as one of two configurations
- [x] ~~Commercial AC power option needed?~~ → Yes, as one of two configurations
- [ ] Battery chemistry confirmation: LiFePO4 vs Li-ion?
- [ ] PiJuice vs PiSugar vs custom power board?
- [ ] Worst-case solar conditions to design for (specific locations)?
- [ ] Solar panel wattage (preliminary estimate: 50-100W)

### Physical Controls
- [x] ~~Additional switches beyond power and mode?~~ → WiFi hotspot + reset confirmed
- [x] ~~Switch type preference?~~ → No preference; must meet IP67

### Display
- [ ] Display size preference (1.3", 2.4", larger)?
- [ ] Color vs monochrome?
- [ ] Should display be on continuously or activate on button press?

### Mounting
- [ ] Camera offset/cable length from main enclosure?
- [ ] Camera adjustment mechanism: ball head, pan/tilt, or custom bracket?
- [ ] Mounting hardware for flat surfaces (in addition to pole clamps)?

### Connectivity
- [x] ~~Specific cellular bands required?~~ → Global multi-band; local SIM procurement
- [ ] Preferred cellular modem (Quectel, SIMCom, etc.)?
- [ ] SIM management: single SIM, dual SIM, eSIM?

### Enclosure
- [ ] Preferred NEMA enclosure size/model?
- [ ] Material: polycarbonate, fiberglass, or aluminum?
- [ ] Internal mounting: DIN rail, standoffs, or custom plate?
