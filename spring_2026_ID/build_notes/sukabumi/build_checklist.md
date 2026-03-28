# Sukabumi Build Checklist

**Site:** Sukabumi, Indonesia
**Power:** Solar (existing 200W/50Ah system)
**Camera:** PoE (ANNKE C1200, power-cycled with Pi)
**Build Start Date:** _______________
**Builder:** _______________

---

## How to Use This Checklist

1. Complete phases in order - dependencies noted
2. Do not skip verification steps
3. Record actual values, not just pass/fail
4. Take required photos at each phase
5. Stop at hold points until sign-off complete
6. Document issues immediately in Known Issues section

---

## Phase 0: Incoming Inspection

**Goal:** Verify all components received, undamaged, and functional before build
**Hold Point:** Must pass before proceeding to Phase 1

### 0.1 Environmental Conditions

| Date | Time | Temp (°C) | Humidity (%) |
|------|------|-----------|--------------|
| | | | |

### 0.2 Component Registry

Record serial numbers, date codes, and supplier info for traceability.

#### Compute Platform

| Component | Serial / ID | Date Code | Supplier | Order # | Photo |
|-----------|-------------|-----------|----------|---------|-------|
| Raspberry Pi 5 8GB | | | Amazon | Coupa #484665 | [photo](photos/raspberry_pi_5.png) |
| Witty Pi 5 HAT+ | | | Adafruit | #3625618 | [photo](photos/witty_pi_5_hat.png) |
| Stacking Headers | | | Amazon | Coupa #484665 | [photo](photos/stacking_headers.png) |
| GPIO Breakout (G469) | | | Amazon | Coupa #484666 | [photo](photos/gpio_breakout_g469.png) |
| USB Flash 256GB | | | Amazon | Coupa #484667 | [photo](photos/usb_flash_256gb.png) |
| SD Card (primary) | | | Amazon | Coupa #484671 | [photo](photos/sd_cards.png) |
| SD Card (backup) | | | | | [photo](photos/sd_cards.png) |
| Active Cooler | | | Amazon | Coupa #484671 | [photo](photos/active_cooler.png) |

#### Modem & Connectivity

| Component | Serial / IMEI | Date Code | Supplier | Order # | Photo |
|-----------|---------------|-----------|----------|---------|-------|
| Quectel EG25-G | IMEI: | | Amazon | Coupa #484668 | [photo](photos/quectel_eg25g.png) |
| WWAN-USB Adapter | | | Amazon | Coupa #484669 | [photo](photos/wwan_usb_adapter.png) |
| Proxicast Antenna | | | Amazon | Coupa #484670 | [photo](photos/proxicast_antenna.png) |

#### Camera System

| Component | Serial / MAC | Date Code | Supplier | Order # | Photo |
|-----------|--------------|-----------|----------|---------|-------|
| ANNKE C1200 | MAC: | | Amazon | Coupa #484671 | [photo](photos/annke_c1200_camera.png) |
| PoE Switch (12V) | | | Amazon | Coupa #484673 | [photo](photos/poe_switch_12v.png) |
| Vertical Mount | | | Amazon | Coupa #484672 | [photo](photos/vertical_mount.png) |

#### Sensors

| Component | Serial / ID | Date Code | Supplier | Order # | Photo |
|-----------|-------------|-----------|----------|---------|-------|
| Hydreon RG-15 | | | Hydreon | #OEDES-00049484 | [photo](photos/hydreon_rg15.png) |

#### Enclosure & Mounting

| Component | Condition | Supplier | Order # | Photo |
|-----------|-----------|----------|---------|-------|
| NEMA 4X Enclosure 16x12x8 | | Amazon | Coupa #484671 | [photo](photos/nema_4x_enclosure.png) |
| DIN Rail 35mm x 300mm | | Amazon | Coupa #484671 | [photo](photos/din_rail.png) |
| DIN Clip for Pi | | Amazon | Coupa #484671 | [photo](photos/din_clip_pi.png) |
| DIN Terminal Blocks | | Amazon | Coupa #484671 | [photo](photos/din_terminal_blocks.png) |
| Gore Vent M12 | | DigiKey | #97227035 | [photo](photos/gore_vent_m12.png) |

#### User Interface

| Component | Quantity | Condition | Photo |
|-----------|----------|-----------|-------|
| Multi-color LEDs | /5 | | [photo](photos/status_leds.png) |
| IP67 Pushbutton 16mm | | | [photo](photos/ip67_pushbutton.png) |
| PG9 Cable Gland | | | [photo](photos/cable_glands.png) |
| LED Resistors | | | [ ] |

#### Protection & Consumables

| Component | Expiry/Condition | Supplier | Photo |
|-----------|------------------|----------|-------|
| Conformal Coating | Exp: | Amazon | [photo](photos/conformal_coating.png) |
| Dielectric Grease | | Amazon | [photo](photos/dielectric_grease.png) |
| 12V Power Couplers | | Amazon | [photo](photos/12v_power_couplers.png) |

#### Cables

| Component | Length | Condition | Photo |
|-----------|--------|-----------|-------|
| USB-C Power Cable | | | [ ] |
| USB-A Cables (3-pack) | | | [ ] |
| Cat6 Ethernet (outdoor) | | | [ ] |

### 0.3 Visual Inspection

| Component | Package Intact | No Damage | Correct Part | Accessories | Pass |
|-----------|---------------|-----------|--------------|-------------|------|
| Raspberry Pi 5 | [ ] | [ ] | [ ] | [ ] | [ ] |
| Witty Pi 5 HAT+ | [ ] | [ ] | [ ] | [ ] Battery | [ ] |
| Stacking Headers | [ ] | [ ] Pins straight | [ ] | [ ] | [ ] |
| GPIO Breakout | [ ] | [ ] | [ ] | [ ] | [ ] |
| USB Flash Drive | [ ] | [ ] | [ ] | [ ] | [ ] |
| SD Cards | [ ] | [ ] | [ ] | [ ] | [ ] |
| Active Cooler | [ ] | [ ] Fan free | [ ] | [ ] | [ ] |
| Quectel Modem | [ ] | [ ] | [ ] | [ ] | [ ] |
| WWAN-USB Adapter | [ ] | [ ] | [ ] | [ ] Cables | [ ] |
| Antenna | [ ] | [ ] Cables intact | [ ] | [ ] | [ ] |
| ANNKE C1200 | [ ] | [ ] Lens clean | [ ] | [ ] Mount | [ ] |
| PoE Switch | [ ] | [ ] | [ ] | [ ] Power | [ ] |
| Rain Gauge | [ ] | [ ] Lens clean | [ ] | [ ] Cable | [ ] |
| Enclosure | [ ] | [ ] No cracks | [ ] | [ ] Gasket | [ ] |
| DIN Rail | [ ] | [ ] Not bent | [ ] | [ ] Screws | [ ] |
| Gore Vent | [ ] | [ ] Membrane ok | [ ] | [ ] | [ ] |
| LEDs | [ ] | [ ] | [ ] Colors | [ ] | [ ] |
| Pushbutton | [ ] | [ ] | [ ] | [ ] | [ ] |
| Conformal Coating | [ ] | [ ] Not expired | [ ] | [ ] | [ ] |

### 0.4 Functional Pre-Test

Test core components independently before assembly.

#### Raspberry Pi 5 (bare, no HATs)

**Precondition:** Fresh Raspberry Pi OS on SD card

| Test | Expected | Actual | Pass |
|------|----------|--------|------|
| Insert SD, connect power/HDMI/keyboard | | | |
| Boots to login prompt | Yes | | [ ] |
| No display artifacts | Clean display | | [ ] |
| USB port detects keyboard | Yes | | [ ] |
| Record serial from `/proc/cpuinfo` | | | [ ] |

**Pi Serial Number:** ________________________

#### Active Cooler

| Test | Expected | Actual | Pass |
|------|----------|--------|------|
| Connect to powered Pi fan header | | | |
| Fan spins | Yes | | [ ] |
| Fan speed varies with load | Yes | | [ ] |

#### Camera (standalone)

| Test | Expected | Actual | Pass |
|------|----------|--------|------|
| Connect to PoE switch, power switch | | | |
| Camera boots (LEDs active) | Yes, ~60s | | [ ] |
| Web UI accessible at default IP | Yes | | [ ] |
| Record MAC address | | | [ ] |

**Camera Default IP:** ________________________
**Camera MAC:** ________________________

#### Rain Gauge (visual only)

| Test | Expected | Pass |
|------|----------|------|
| Optical lens clean, no scratches | Yes | [ ] |
| Wiring harness intact | Yes | [ ] |

### 0.5 Items to Source

| Item | Specification | Status | Notes |
|------|---------------|--------|-------|
| SIM Card | Telkomsel, pre-activated | [ ] | |
| Cat6 Cable | Outdoor, length for site | [ ] | |

### 0.6 Hold Point Sign-Off

| Verification | Initials | Date |
|--------------|----------|------|
| All components received | | |
| Visual inspection complete - no damage | | |
| Functional pre-tests passed | | |
| Component registry complete | | |
| Photos taken (all components) | | |
| **Approved to proceed to Phase 1** | | |

**Notes:**
```




```

---

## Phase 1: Workspace Preparation

**Goal:** Establish workspace, prepare tools, flash SD card
**Prerequisite:** Phase 0 complete

### 1.1 Environmental Conditions

| Date | Time | Temp (°C) | Humidity (%) |
|------|------|-----------|--------------|
| | | | |

### 1.2 Workspace Setup

| Requirement | Specification | Verified |
|-------------|---------------|----------|
| Work surface | Clean, non-static (wood, anti-static mat) | [ ] |
| ESD protection | Grounding strap or metal contact point | [ ] |
| Lighting | Adequate for small components | [ ] |
| Ventilation | Adequate for conformal coating | [ ] |

### 1.3 Tools Verification

| Tool | Available |
|------|-----------|
| Phillips screwdriver set (#0, #1, #2) | [ ] |
| Adjustable wrench (6") | [ ] |
| Wire strippers (18-22 AWG) | [ ] |
| Multimeter (tested, battery OK) | [ ] |
| Small brush (for coating) | [ ] |
| Masking tape / Kapton tape | [ ] |
| Isopropyl alcohol 99% + lint-free wipes | [ ] |
| Laptop with SSH client | [ ] |
| USB keyboard | [ ] |
| Micro-HDMI to HDMI adapter | [ ] |
| Ethernet cable (short) | [ ] |
| USB-C power supply (5V/5A quality) | [ ] |
| 12V bench power supply | [ ] |
| Camera/phone for photos | [ ] |

### 1.4 Software Preparation

| Item | Version/Source | Downloaded |
|------|----------------|------------|
| Raspberry Pi OS Lite (64-bit) | | [ ] |
| SHA256 verified | | [ ] |
| Raspberry Pi Imager | | [ ] |

### 1.5 Flash SD Card

| Step | Completed |
|------|-----------|
| Insert SD card into computer | [ ] |
| Flash Raspberry Pi OS Lite using Imager | [ ] |
| Configure via Imager advanced options: | |
| - Hostname: `sukabumi-orc` | [ ] |
| - Enable SSH | [ ] |
| - Set username/password | [ ] |
| - Timezone: Asia/Jakarta | [ ] |
| Safely eject SD card | [ ] |
| Label SD card: "Sukabumi Primary - [date]" | [ ] |

**Credentials (store securely, NOT in this document):**
- Documented in secure location: [ ]

### 1.6 Verification

| Check | Pass |
|-------|------|
| Workspace meets ESD requirements | [ ] |
| All tools available | [ ] |
| SD card flashed and labeled | [ ] |
| Components organized by phase | [ ] |

**Notes:**
```



```

---

## Phase 1B: Complete Dry Fit & Verification

**Goal:** Verify EVERYTHING fits and works BEFORE any irreversible actions
**Prerequisite:** Phase 1 complete
**Why:** Confirm fit, compatibility, and function before coating, drilling, or cutting

**After this phase, components are still returnable. After Phase 2+, they are not.**

### 1B.1 Environmental Conditions

| Date | Time | Temp (°C) | Humidity (%) |
|------|------|-----------|--------------|
| | | | |

---

### 1B.2 Dry Fit: HAT Stack

Assemble WITHOUT conformal coating.

| Step | Completed |
|------|-----------|
| Ground yourself (ESD) | [ ] |
| Install active cooler on Pi 5 | [ ] |
| Insert stacking headers (long pins UP) | [ ] |
| Seat Witty Pi 5 HAT+ | [ ] |
| Attach GPIO Breakout on top | [ ] |

| Check | Pass |
|-------|------|
| All headers fully seated | [ ] |
| Stack is stable, no wobble | [ ] |
| Boards are parallel (no tilt) | [ ] |
| No physical interference between boards | [ ] |
| Active cooler clears Witty Pi | [ ] |

**Stack height (measure):** _______ mm

---

### 1B.3 Dry Fit: Modem Assembly

| Step | Completed |
|------|-----------|
| Insert Quectel EG25-G into WWAN-USB adapter | [ ] |
| Verify fit is correct | [ ] |
| Attach antenna cables (don't overtighten) | [ ] |
| Verify SIM slot accessible | [ ] |

| Check | Pass |
|-------|------|
| Modem seats properly in adapter | [ ] |
| Antenna connectors fit | [ ] |
| SIM can be inserted/removed | [ ] |

---

### 1B.4 Dry Fit: DIN Rail Components

Test fit components on DIN rail OUTSIDE the enclosure first.

| Component | Fits on Rail | Secure | Removable |
|-----------|--------------|--------|-----------|
| Pi + HAT stack in DIN clip | [ ] | [ ] | [ ] |
| Terminal blocks | [ ] | [ ] | [ ] |
| PoE switch (if DIN mount) | [ ] | [ ] | [ ] |

| Check | Pass |
|-------|------|
| DIN clip fits Pi with full HAT stack | [ ] |
| Clip holds securely | [ ] |
| Can remove/reinstall without damage | [ ] |

**DIN rail length needed:** _______ mm (rail provided: 300mm)

---

### 1B.5 Dry Fit: Enclosure Layout

Place components in enclosure WITHOUT mounting to verify layout.

| Step | Completed |
|------|-----------|
| Place DIN rail in enclosure (don't drill yet) | [ ] |
| Place Pi + stack on rail | [ ] |
| Place PoE switch | [ ] |
| Place modem + adapter | [ ] |
| Place terminal blocks | [ ] |
| Arrange for cable routing space | [ ] |

| Check | Pass |
|-------|------|
| All components fit in enclosure | [ ] |
| Adequate clearance between components | [ ] |
| Space for cable routing | [ ] |
| Airflow path for cooling | [ ] |
| USB ports accessible | [ ] |
| SD card accessible | [ ] |

**Sketch layout (or take photo):**
```
+------------------------------------------+
|                                          |
|                                          |
|                                          |
|                                          |
|                                          |
|                                          |
|                                          |
+------------------------------------------+
```

---

### 1B.6 Dry Fit: Panel Components

Test fit panel-mount components WITHOUT drilling.

| Component | Fits | Clearance OK | Location Planned |
|-----------|------|--------------|------------------|
| Gore vent (M12) | [ ] | [ ] | |
| Green LED | [ ] | [ ] | |
| Yellow LED | [ ] | [ ] | |
| Red LED | [ ] | [ ] | |
| Maintenance button (16mm) | [ ] | [ ] | |
| Cable gland - power | [ ] | [ ] | |
| Cable gland - Ethernet | [ ] | [ ] | |
| Cable gland - antenna | [ ] | [ ] | |
| Cable gland - rain gauge | [ ] | [ ] | |

**Plan hole positions (sketch or photo):**
```
Enclosure lid/front:


Enclosure sides/bottom:


```

---

### 1B.7 Dry Fit: Camera & Mount

| Step | Completed |
|------|-----------|
| Attach camera to vertical mount | [ ] |
| Verify mounting hardware fits | [ ] |
| Test adjustment range | [ ] |

| Check | Pass |
|-------|------|
| Camera mounts securely | [ ] |
| Angle adjustment sufficient | [ ] |
| Mount hardware complete | [ ] |

---

### 1B.8 Dry Fit: Rain Gauge

| Check | Pass |
|-------|------|
| Mounting holes accessible | [ ] |
| Cable length sufficient | [ ] |
| Wire colors identifiable | [ ] |

---

### 1B.9 Boot Test (Uncoated)

Verify the system actually works before coating.

| Step | Completed |
|------|-----------|
| Insert SD card | [ ] |
| Insert USB flash drive | [ ] |
| Connect power, HDMI, keyboard | [ ] |
| Power on | [ ] |

```bash
# After login, verify:
sudo i2cdetect -y 1    # Should show 69
lsblk                   # Should show USB drive
vcgencmd measure_temp   # Should be reasonable
```

| Check | Expected | Actual | Pass |
|-------|----------|--------|------|
| System boots | ≤60s | s | [ ] |
| Login prompt appears | Yes | | [ ] |
| I2C device at 0x69 | Yes | | [ ] |
| USB flash detected | ~256GB | GB | [ ] |
| Active cooler runs | Yes | | [ ] |
| CPU temp reasonable | <50°C | °C | [ ] |

---

### 1B.10 Peripheral Tests

Connect and verify peripherals work (can skip modem data test if no SIM yet).

**Modem (physical only if no SIM):**

| Check | Pass |
|-------|------|
| Modem detected in lsusb | [ ] |
| /dev/ttyUSB* ports appear | [ ] |

**Camera:**

| Step | Completed |
|------|-----------|
| Connect camera to PoE switch | [ ] |
| Connect PoE switch to Pi or network | [ ] |
| Power PoE switch | [ ] |
| Wait for camera boot (~60s) | [ ] |

| Check | Pass |
|-------|------|
| Camera boots (LEDs active) | [ ] |
| Can access camera web UI | [ ] |
| Can capture test frame via RTSP (`orc-capture --skip-relay --dry-run`) or ISAPI snapshot | [ ] |

**Rain Gauge (if wiring to GPIO breakout):**

| Check | Pass |
|-------|------|
| Wiring fits in screw terminals | [ ] |
| Serial communication works | [ ] |

---

### 1B.11 Disassemble for Coating/Modification

| Step | Completed |
|------|-----------|
| Power off system | [ ] |
| Disconnect all cables | [ ] |
| Remove SD card | [ ] |
| Remove USB flash drive | [ ] |
| Remove Pi from DIN clip | [ ] |
| Carefully disassemble HAT stack | [ ] |
| Remove active cooler | [ ] |
| Disassemble modem from adapter | [ ] |
| Return all components to anti-static storage | [ ] |
| Inspect all components for damage | [ ] |

---

### 1B.12 Dry Fit Summary

| Category | Status | Issues |
|----------|--------|--------|
| HAT stack fit | [ ] Pass | |
| Modem assembly | [ ] Pass | |
| DIN rail mounting | [ ] Pass | |
| Enclosure layout | [ ] Pass | |
| Panel components | [ ] Pass | |
| Camera mount | [ ] Pass | |
| Rain gauge | [ ] Pass | |
| Boot test | [ ] Pass | |
| Peripheral tests | [ ] Pass | |
| All components undamaged | [ ] Pass | |

---

### 1B.13 Hold Point Sign-Off

**STOP - Do not proceed until ALL dry fit checks pass.**

After this point:
- Phase 2: Conformal coating applied (boards non-returnable)
- Phase 10: Enclosure drilled/cut (enclosure non-returnable)

| Verification | Initials | Date |
|--------------|----------|------|
| All components fit correctly | | |
| Enclosure layout verified | | |
| Boot test passed | | |
| I2C detected (Witty Pi at 0x69) | | |
| Camera streaming verified | | |
| No fit issues requiring resolution | | |
| No components need to be returned/exchanged | | |
| **Approved to proceed to Phase 2 (Coating)** | | |

**Notes:**
```
Issues discovered:


Components that don't fit or need exchange:


Layout changes from original plan:


```

---

## Phase 2: Conformal Coating

**Goal:** Apply silicone conformal coating to PCBs
**Prerequisite:** Phase 1B complete (dry fit verified)
**Time Required:** ~1 hour application + 24 hour cure
**Hold Point:** Must cure 24 hours before Phase 3

### 2.1 Environmental Conditions

| Date | Time | Temp (°C) | Humidity (%) |
|------|------|-----------|--------------|
| | | | |

**Recommended:** <60% humidity during application

### 2.2 Clean PCBs

| Board | Cleaned with IPA | Dried | Inspected |
|-------|------------------|-------|-----------|
| Raspberry Pi 5 | [ ] | [ ] | [ ] |
| Witty Pi 5 HAT+ | [ ] | [ ] | [ ] |
| GPIO Breakout | [ ] | [ ] | [ ] |

### 2.3 Mask Components

**Raspberry Pi 5 - Mask:**

| Area | Masked |
|------|--------|
| GPIO header (40-pin) | [ ] |
| USB-A ports (x2) | [ ] |
| USB-C power port | [ ] |
| Ethernet port | [ ] |
| Micro-HDMI ports (x2) | [ ] |
| SD card slot | [ ] |
| CSI/DSI connectors | [ ] |
| Thermal contact area (CPU) | [ ] |
| Active cooler mounting holes | [ ] |
| PoE header | [ ] |
| Debug header | [ ] |

**Witty Pi 5 HAT+ - Mask:**

| Area | Masked |
|------|--------|
| GPIO header (bottom) | [ ] |
| GPIO header (top passthrough) | [ ] |
| JST battery connector | [ ] |
| Screw terminals (if any) | [ ] |
| I2C address jumpers | [ ] |

**GPIO Breakout - Mask:**

| Area | Masked |
|------|--------|
| Header/connector | [ ] |
| All screw terminals | [ ] |

### 2.4 Pre-Coating Photos

| Photo | Taken |
|-------|-------|
| Pi 5 top (masked) | [ ] |
| Pi 5 bottom | [ ] |
| Witty Pi top (masked) | [ ] |
| Witty Pi bottom | [ ] |
| GPIO Breakout (masked) | [ ] |

### 2.5 Apply Coating

| Board | Top Coated | Bottom Coated | No Drips | No Pooling |
|-------|------------|---------------|----------|------------|
| Raspberry Pi 5 | [ ] | [ ] | [ ] | [ ] |
| Witty Pi 5 HAT+ | [ ] | [ ] | [ ] | [ ] |
| GPIO Breakout | [ ] | [ ] | [ ] | [ ] |

**Application time:** _______________

### 2.6 Cure

| Check | Value |
|-------|-------|
| Boards placed on clean surface | [ ] |
| Boards not touching | [ ] |
| Cure start time | |
| Cure environment temp | °C |
| Cure environment humidity | % |

### 2.7 Post-Cure Inspection (after 24 hours)

**Cure end time:** _______________
**Total cure duration:** _______________ hours (minimum 24)

| Board | Masking Removed | Coverage Complete | No Connector Intrusion | Photo Taken |
|-------|-----------------|-------------------|------------------------|-------------|
| Raspberry Pi 5 | [ ] | [ ] | [ ] | [ ] |
| Witty Pi 5 HAT+ | [ ] | [ ] | [ ] | [ ] |
| GPIO Breakout | [ ] | [ ] | [ ] | [ ] |

### 2.8 Hold Point Sign-Off

| Verification | Initials | Date |
|--------------|----------|------|
| Cure time ≥24 hours | | |
| All boards pass coverage inspection | | |
| No coating on connectors | | |
| Before/after photos taken | | |
| **Approved to proceed to Phase 3** | | |

**Notes:**
```



```

---

## Phase 3: Compute Platform Assembly

**Goal:** Assemble Pi + Witty Pi + GPIO Breakout stack
**Prerequisite:** Phase 2 complete (coating cured)

### 3.1 Environmental Conditions

| Date | Time | Temp (°C) | Humidity (%) |
|------|------|-----------|--------------|
| | | | |

### 3.2 Install Active Cooler

| Step | Completed |
|------|-----------|
| Remove masking from Pi thermal contact area | [ ] |
| Position cooler over CPU/RAM | [ ] |
| Press until clips engage | [ ] |
| Connect fan cable to Pi fan header | [ ] |
| Verify cooler firmly seated, no wobble | [ ] |

### 3.3 Stack Assembly

**Assembly order (bottom to top):**
1. Raspberry Pi 5
2. Stacking headers (long pins UP)
3. Witty Pi 5 HAT+
4. GPIO Breakout (if pass-through) OR ribbon cable

| Step | Completed |
|------|-----------|
| Ground yourself (ESD) | [ ] |
| Insert stacking headers into Pi GPIO | [ ] |
| Verify long pins pointing UP | [ ] |
| Align Witty Pi 5 over headers | [ ] |
| Press Witty Pi firmly until seated | [ ] |
| Verify no exposed pins between boards | [ ] |
| Attach GPIO Breakout on top | [ ] |
| Verify stack is stable, no wobble | [ ] |
| Boards are parallel (no tilting) | [ ] |

### 3.4 Insert Storage

| Step | Completed |
|------|-----------|
| Insert SD card (prepared in Phase 1) | [ ] |
| Card clicks into place | [ ] |
| Insert USB flash drive into USB 3.0 (blue) port | [ ] |

### 3.5 Photos

| Photo | Taken |
|-------|-------|
| Stack side view (all layers visible) | [ ] |
| Stack top view | [ ] |
| Fan cable connection | [ ] |
| SD card inserted | [ ] |
| USB flash drive inserted | [ ] |

### 3.6 Verification

| Check | Pass |
|-------|------|
| All headers fully seated | [ ] |
| Stack stable, no wobble | [ ] |
| Active cooler secure | [ ] |
| Fan cable connected | [ ] |
| SD card inserted | [ ] |
| USB flash drive inserted | [ ] |

**Notes:**
```



```

---

## Phase 4: Initial Boot Test

**Goal:** Verify compute platform boots and functions correctly
**Prerequisite:** Phase 3 complete
**Hold Point:** Must pass all criteria before Phase 5+

### 4.1 Environmental Conditions

| Date | Time | Temp (°C) | Humidity (%) |
|------|------|-----------|--------------|
| | | | |

### 4.2 Bench Power-Up

| Step | Completed |
|------|-----------|
| Connect USB-C power (5V/5A quality supply) | [ ] |
| Connect HDMI monitor | [ ] |
| Connect USB keyboard | [ ] |
| Power on | [ ] |
| Start timer | [ ] |

### 4.3 Boot Observation

| Observation | Expected | Actual | Pass |
|-------------|----------|--------|------|
| Red power LED | Solid on | | [ ] |
| Green activity LED | Flashing | | [ ] |
| Active cooler fan | Spins, then regulates | | [ ] |
| Boot messages on screen | Yes | | [ ] |
| Login prompt appears | Yes | | [ ] |
| Boot time | ≤60 seconds | s | [ ] |

### 4.4 System Verification

Login and run these commands:

```bash
# System info
uname -a
cat /etc/os-release

# Memory
free -h

# Storage
lsblk
df -h

# I2C devices
sudo i2cdetect -y 1

# Temperature
vcgencmd measure_temp

# CPU info (get serial)
cat /proc/cpuinfo | grep Serial
```

| Check | Expected | Actual | Pass |
|-------|----------|--------|------|
| OS version | Raspberry Pi OS Lite 64-bit | | [ ] |
| Memory | ~8 GB total | GB | [ ] |
| SD card detected | Yes | | [ ] |
| USB flash detected (/dev/sda) | ~256 GB | GB | [ ] |
| I2C device at 0x69 | Yes (Witty Pi) | | [ ] |
| CPU temp at idle | ≤50°C | °C | [ ] |
| Pi serial matches registry | | | [ ] |

### 4.5 Configure Basic Settings

```bash
sudo raspi-config
```

| Setting | Value | Configured |
|---------|-------|------------|
| Hostname | sukabumi-orc | [ ] |
| SSH | Enabled | [ ] |
| I2C | Enabled | [ ] |
| Serial Port - Login shell | Disabled | [ ] |
| Serial Port - Hardware | Enabled | [ ] |
| Timezone | Asia/Jakarta | [ ] |

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Reboot
sudo reboot
```

| Check | Pass |
|-------|------|
| System updated without errors | [ ] |
| System reboots successfully | [ ] |
| Settings persist after reboot | [ ] |
| SSH accessible from another machine | [ ] |

### 4.6 Acceptance Criteria

| Criterion | Requirement | Actual | Pass |
|-----------|-------------|--------|------|
| Boot time | ≤60 seconds | s | [ ] |
| Memory | 7.5-8.0 GB | GB | [ ] |
| USB flash | Detected, ~256 GB | GB | [ ] |
| I2C 0x69 | Present | | [ ] |
| CPU temp idle | ≤50°C | °C | [ ] |
| Active cooler | Running | | [ ] |
| SSH | Accessible | | [ ] |
| Reboot | Stable | | [ ] |

**All criteria must pass.**

### 4.7 Hold Point Sign-Off

| Verification | Initials | Date |
|--------------|----------|------|
| All acceptance criteria pass | | |
| OS and kernel version recorded | | |
| Pi serial verified against registry | | |
| **Approved to proceed to Phase 5+** | | |

**Notes:**
```
OS Version:
Kernel Version:
Pi Serial:


```

---

## Phase 5: Witty Pi Configuration

**Goal:** Install Witty Pi software and verify RTC
**Prerequisite:** Phase 4 complete

### 5.1 Environmental Conditions

| Date | Time | Temp (°C) | Humidity (%) |
|------|------|-----------|--------------|
| | | | |

### 5.2 Install Witty Pi Software

```bash
wget https://www.uugear.com/repo/WittyPi5/install.sh
sudo sh install.sh
# Reboot when prompted
sudo reboot
```

| Step | Completed |
|------|-----------|
| Download install script | [ ] |
| Run install script | [ ] |
| Installation completes without error | [ ] |
| Reboot | [ ] |

### 5.3 Verify Witty Pi

```bash
cd ~/wittypi
./wittyPi.sh
```

| Check | Expected | Actual | Pass |
|-------|----------|--------|------|
| Witty Pi utility runs | Yes | | [ ] |
| RTC time displayed | Correct | | [ ] |
| Temperature reading | Reasonable | °C | [ ] |
| Voltage reading | ~5V | V | [ ] |

### 5.4 Sync RTC

If RTC time is wrong:
```bash
# In wittyPi.sh menu, select option to sync RTC with Pi time
```

| Check | Pass |
|-------|------|
| RTC synced with system time | [ ] |
| Time persists after reboot | [ ] |

### 5.5 Schedule Configuration

**Do NOT enable schedule yet** - will enable in Phase 14 after all testing.

| Task | Completed |
|------|-----------|
| Review schedule file format | [ ] |
| Note schedule file location | [ ] |
| **Schedule remains DISABLED** | [ ] |

**Schedule file location:** `~/wittypi/schedules/`

### 5.6 Verification

| Check | Pass |
|-------|------|
| Witty Pi software installed | [ ] |
| RTC time correct | [ ] |
| Temperature sensor working | [ ] |
| Schedule NOT enabled | [ ] |

**Notes:**
```



```

---

## Phase 6: Modem Assembly & Test

**Goal:** Assemble modem, install SIM, verify connectivity, configure Pangolin
**Prerequisite:** Phase 4 complete

### 6.1 Environmental Conditions

| Date | Time | Temp (°C) | Humidity (%) |
|------|------|-----------|--------------|
| | | | |

### 6.2 Modem Assembly

| Step | Completed |
|------|-----------|
| Insert Quectel EG25-G into WWAN-USB adapter | [ ] |
| Connect antenna cables (main + diversity) | [ ] |
| Verify SIM slot accessible | [ ] |

### 6.3 Install SIM Card

| Step | Completed |
|------|-----------|
| Power off Pi | [ ] |
| Insert Telkomsel SIM (note orientation) | [ ] |
| SIM orientation: contacts _______ | [ ] |

**SIM details (store securely):**
- Carrier: Telkomsel
- Phone number: _______________
- Data plan: _______________

### 6.4 Connect to Pi

| Step | Completed |
|------|-----------|
| Connect USB cable from adapter to Pi | [ ] |
| Connect Proxicast antenna cables to adapter | [ ] |
| Antenna positioned for signal | [ ] |

### 6.5 Photos

| Photo | Taken |
|-------|-------|
| Modem in adapter | [ ] |
| Antenna connections | [ ] |
| USB connection to Pi | [ ] |

### 6.6 Test Modem

Power on Pi and run:

```bash
# Check USB detection
lsusb | grep -i quectel

# Check serial ports
ls /dev/ttyUSB*

# Install ModemManager if needed
sudo apt install modemmanager -y

# Check modem status
mmcli -L
mmcli -m 0
```

| Check | Expected | Actual | Pass |
|-------|----------|--------|------|
| Modem in lsusb | Quectel device | | [ ] |
| Serial ports | ttyUSB0-3 | | [ ] |
| ModemManager sees modem | Yes | | [ ] |
| SIM detected | Yes | | [ ] |
| Signal strength | >30% | % | [ ] |

### 6.7 Test Data Connection

```bash
# Connect (Telkomsel APN)
mmcli -m 0 --simple-connect="apn=internet"

# Check interface
ip addr

# Test connectivity
ping -c 5 8.8.8.8
ping -c 5 google.com
```

| Check | Expected | Actual | Pass |
|-------|----------|--------|------|
| Connection established | Yes | | [ ] |
| IP address assigned | Yes | | [ ] |
| Ping 8.8.8.8 | Success | | [ ] |
| Ping google.com | Success | | [ ] |

### 6.8 Configure Pangolin Client

**Prerequisite:** Obtain Pangolin server details from ORC team

```bash
# Install Pangolin client
# (Follow ORC team instructions)

# Configure with server details
# (Document in secure location)
```

| Step | Completed |
|------|-----------|
| Pangolin client installed | [ ] |
| Server configured | [ ] |
| Device registered | [ ] |
| Test connection from remote | [ ] |

**Pangolin details (store securely, NOT here):**
- Documented in secure location: [ ]

### 6.9 Verification

| Check | Pass |
|-------|------|
| Modem detected | [ ] |
| SIM recognized | [ ] |
| Data connection works | [ ] |
| Pangolin configured | [ ] |
| Remote access tested | [ ] |

**Notes:**
```
Signal strength:
Carrier detected:
APN used:


```

---

## Phase 7: Camera Configuration

**Goal:** Configure ANNKE C1200 and verify RTSP capture

**Prerequisite:** Phase 4 complete

### 7.1 Environmental Conditions

| Date | Time | Temp (°C) | Humidity (%) |
|------|------|-----------|--------------|
| | | | |

### 7.2 Camera Setup

| Step | Completed |
|------|-----------|
| Connect camera to PoE switch | [ ] |
| Connect PoE switch to Pi Ethernet (or local network) | [ ] |
| Power on PoE switch (12V) | [ ] |
| Wait for camera boot (~60s) | [ ] |

### 7.3 Find Camera IP

```bash
# If camera uses DHCP
nmap -sn 192.168.1.0/24
# Or check router DHCP leases
# Or use camera default IP from manual
```

| Check | Value |
|-------|-------|
| Camera IP address | |
| Camera boot time | s |

### 7.4 Configure Camera via Web UI

Access from laptop/desktop browser.

| Setting | Value | Configured |
|---------|-------|------------|
| Login with default credentials | | [ ] |
| Change password | (store securely) | [ ] |
| Video Stream 1 (Main) | H.264, 4K/12MP, 10fps | [ ] |
| Video Stream 2 (Sub) | H.264, 720p, 10fps | [ ] |
| Network - Static IP | | [ ] |
| Scheduled Snapshot | Configured per ORC requirements | [ ] |
| IR LEDs | Auto | [ ] |
| NTP | Disabled | [ ] |

**Static IP assigned:** _______________

### 7.5 Test RTSP Capture

```bash
# Ensure camera is powered and booted (wait ~90s after power-on)
# Run capture script manually
/usr/local/bin/orc-capture.sh

# Verify output
ls -la /home/pi/Videos/
ffprobe /home/pi/Videos/*.mp4
```

| Check | Expected | Actual | Pass |
|-------|----------|--------|------|
| orc-capture.sh runs without error | Yes | | [ ] |
| .mp4 file created | Yes | | [ ] |
| Video duration | ~5s | s | [ ] |
| Video resolution | ≥1080p | | [ ] |
| Video plays correctly | Yes | | [ ] |

### 7.6 Test IR Mode

| Test | Pass |
|------|------|
| Cover lens / darken room | [ ] |
| IR LEDs activate | [ ] |
| Image visible in dark | [ ] |
| Uncover / restore light | [ ] |
| IR LEDs deactivate | [ ] |

### 7.7 Acceptance Criteria

| Criterion | Requirement | Actual | Pass |
|-----------|-------------|--------|------|
| Camera boot time | ≤90 s | s | [ ] |
| Web UI accessible | Yes | | [ ] |
| RTSP capture working | Yes | | [ ] |
| Video codec | H.264/H.265 | | [ ] |
| Video resolution | ≥1920x1080 | | [ ] |
| Video duration | 5.0 ±0.5 s | s | [ ] |
| IR auto-switching | Works | | [ ] |
| Focus | Sharp | | [ ] |

### 7.8 Record Configuration

**Camera details (store password securely):**

| Field | Value |
|-------|-------|
| Camera IP | |
| Camera MAC | |
| Firmware version | |
| Username | admin |
| RTSP URL | rtsp://admin:PASSWORD@192.168.50.139:554/Streaming/channels/101 |

**Notes:**
```



```

---

## Phase 8: Rain Gauge Setup

**Goal:** Connect and test Hydreon RG-15
**Prerequisite:** Phase 4 complete

### 8.1 Environmental Conditions

| Date | Time | Temp (°C) | Humidity (%) |
|------|------|-----------|--------------|
| | | | |

### 8.2 Wiring

**RG-15 to GPIO Breakout:**

| RG-15 Wire | Color | Function | Connect To | Connected |
|------------|-------|----------|------------|-----------|
| VCC | Red | Power (5-15V) | 5V terminal | [ ] |
| GND | Black | Ground | GND terminal | [ ] |
| TX | Green | Serial out | Pi RX (GPIO15) | [ ] |
| RX | White | Serial in | Pi TX (GPIO14) | [ ] |

**Note:** TX↔RX crossover - gauge TX → Pi RX

### 8.3 Photo

| Photo | Taken |
|-------|-------|
| Wiring at GPIO breakout | [ ] |

### 8.4 Test Serial Communication

```bash
# Install minicom
sudo apt install minicom -y

# Connect (9600 baud, 8N1)
minicom -b 9600 -D /dev/serial0

# In minicom, type 'R' to request reading
# Expected response:
# Acc 0.00 mm, EventAcc 0.00 mm, TotalAcc 0.00 mm, RInt 0.00 mmph

# Exit: Ctrl-A then X
```

| Check | Expected | Actual | Pass |
|-------|----------|--------|------|
| Serial connection | Established | | [ ] |
| Response to 'R' command | Reading displayed | | [ ] |
| Reading format | Acc, EventAcc, TotalAcc, RInt | | [ ] |

### 8.5 Test Rain Detection

```bash
# With minicom open:
# Option A: Drip small amount of water on sensor
# Option B: Type 'K' to simulate rain event
```

| Check | Pass |
|-------|------|
| Rain detection triggers | [ ] |
| EventAcc or RInt changes | [ ] |

### 8.6 Verification

| Check | Pass |
|-------|------|
| Wiring correct (TX↔RX crossover) | [ ] |
| Serial communication works | [ ] |
| Rain detection works | [ ] |
| Photo taken | [ ] |

**Notes:**
```



```

---

## Phase 9: Status LEDs & Maintenance Button

**Goal:** Wire and test status LEDs and maintenance button
**Prerequisite:** Phase 4 complete

### 9.1 Environmental Conditions

| Date | Time | Temp (°C) | Humidity (%) |
|------|------|-----------|--------------|
| | | | |

### 9.2 GPIO Pin Selection

**Avoid pins used by:**
- Witty Pi (check documentation)
- Serial (GPIO14, GPIO15)
- I2C (GPIO2, GPIO3)

**Selected pins:**

| Function | GPIO # | Physical Pin | Selected |
|----------|--------|--------------|----------|
| Green LED | | | [ ] |
| Yellow LED | | | [ ] |
| Red LED | | | [ ] |
| Maint Button | | | [ ] |

### 9.3 LED Wiring

**For each LED:**
- Anode (long leg, +) → Resistor → GPIO pin
- Cathode (short leg, -) → GND

| LED | Resistor (Ω) | GPIO | GND | Wired |
|-----|--------------|------|-----|-------|
| Green | 220-330 | | | [ ] |
| Yellow | 220-330 | | | [ ] |
| Red | 220-330 | | | [ ] |

### 9.4 Test LEDs

```bash
sudo apt install gpiod -y

# Test each LED (replace PIN with GPIO number)
gpioset gpiochip4 PIN=1  # Turn on
gpioset gpiochip4 PIN=0  # Turn off
```

| LED | Lights On | Turns Off | Pass |
|-----|-----------|-----------|------|
| Green (GPIO __) | [ ] | [ ] | [ ] |
| Yellow (GPIO __) | [ ] | [ ] | [ ] |
| Red (GPIO __) | [ ] | [ ] | [ ] |

### 9.5 Button Wiring

**Button wiring (using internal pull-up):**
- Common (C) → GND
- Normally Open (NO) → GPIO pin

| Connection | Terminal | Connected |
|------------|----------|-----------|
| Button Common | GND | [ ] |
| Button NO | GPIO __ | [ ] |

### 9.6 Test Button

```bash
# Read button state
gpioget gpiochip4 PIN
# Returns 1 when not pressed, 0 when pressed
```

| State | Expected | Actual | Pass |
|-------|----------|--------|------|
| Not pressed | 1 | | [ ] |
| Pressed | 0 | | [ ] |

### 9.7 Photos

| Photo | Taken |
|-------|-------|
| LED wiring at GPIO breakout | [ ] |
| Button wiring | [ ] |

### 9.8 Verification

| Check | Pass |
|-------|------|
| Green LED works | [ ] |
| Yellow LED works | [ ] |
| Red LED works | [ ] |
| Button works | [ ] |
| All photos taken | [ ] |

**GPIO Assignments (record for reference):**

| Function | GPIO | Physical Pin |
|----------|------|--------------|
| Green LED | | |
| Yellow LED | | |
| Red LED | | |
| Maint Button | | |

**Notes:**
```



```

---

## Phase 10: Enclosure Assembly

**Goal:** Mount all components in NEMA enclosure
**Prerequisite:** Phases 3-9 complete
**Hold Point:** Enclosure is difficult to rework after sealing

### 10.1 Environmental Conditions

| Date | Time | Temp (°C) | Humidity (%) |
|------|------|-----------|--------------|
| | | | |

### 10.2 Enclosure Preparation

| Step | Completed |
|------|-----------|
| Plan hole positions for: | |
| - Cable glands (power, Ethernet, antenna, rain gauge) | [ ] |
| - LEDs (3x panel mount) | [ ] |
| - Maintenance button (16mm) | [ ] |
| - Gore vent (M12) | [ ] |
| Mark hole positions | [ ] |
| Drill/cut holes | [ ] |
| Deburr all holes | [ ] |
| Test-fit glands and mounts | [ ] |

**Hole positions (record for documentation):**
```
Sketch or notes:




```

### 10.3 Install DIN Rail

| Step | Completed |
|------|-----------|
| Position DIN rail | [ ] |
| Mark mounting holes | [ ] |
| Drill and secure | [ ] |
| Verify rail is level and secure | [ ] |

### 10.4 Mount Components

| Component | Mounted | Secure |
|-----------|---------|--------|
| Pi + HAT stack in DIN clip | [ ] | [ ] |
| Terminal blocks (power distribution) | [ ] | [ ] |
| Terminal blocks (sensors) | [ ] | [ ] |
| PoE switch | [ ] | [ ] |
| Modem + adapter | [ ] | [ ] |

### 10.5 Install Panel Components

| Component | Installed | Functional |
|-----------|-----------|------------|
| Gore M12 vent | [ ] | [ ] |
| Green LED | [ ] | [ ] |
| Yellow LED | [ ] | [ ] |
| Red LED | [ ] | [ ] |
| Maintenance button | [ ] | [ ] |
| Cable glands (loose, for routing) | [ ] | [ ] |

### 10.6 Route Cables

| Cable | Routed | Strain Relief | Labeled |
|-------|--------|---------------|---------|
| Power (12V in) | [ ] | [ ] | [ ] |
| Ethernet (to camera) | [ ] | [ ] | [ ] |
| Antenna cables | [ ] | [ ] | [ ] |
| Rain gauge wires | [ ] | [ ] | [ ] |
| LED wires | [ ] | [ ] | [ ] |
| Button wires | [ ] | [ ] | [ ] |

### 10.7 Seal Enclosure

| Step | Completed |
|------|-----------|
| Apply dielectric grease to gland threads | [ ] |
| Tighten all cable glands | [ ] |
| Verify Gore vent membrane intact | [ ] |
| Close enclosure lid | [ ] |
| Verify gasket seated properly | [ ] |

### 10.8 Photos

| Photo | Taken |
|-------|-------|
| Interior - component placement | [ ] |
| Interior - cable routing | [ ] |
| Exterior - all penetrations | [ ] |
| Exterior - front (LEDs, button) | [ ] |

### 10.9 Acceptance Criteria

| Criterion | Pass |
|-----------|------|
| DIN rail secure (pull test) | [ ] |
| Pi + HAT stack secure in clip | [ ] |
| All terminal blocks secure | [ ] |
| All cable glands tight | [ ] |
| Dielectric grease applied | [ ] |
| Gore vent installed, membrane OK | [ ] |
| All 3 LEDs visible from exterior | [ ] |
| Button actuates freely | [ ] |
| No cables pinched | [ ] |
| Cables have strain relief | [ ] |
| Lid closes fully | [ ] |
| Shake test - no rattles (30s) | [ ] |

### 10.10 Hold Point Sign-Off

**Enclosure is difficult to rework after sealing. Verify everything.**

| Verification | Initials | Date |
|--------------|----------|------|
| All acceptance criteria pass | | |
| Interior photos taken | | |
| Exterior photos taken | | |
| Wiring matches intended design | | |
| **Approved to proceed to Phase 11** | | |

**Notes:**
```



```

---

## Phase 11: ORC Software Installation

**Goal:** Install NodeORC software, configure LiveORC connectivity, and set up RTSP-based video capture

**Prerequisite:** Phase 10 complete
**Note:** Use upstream packages - do not fork. See https://github.com/localdevices/nodeorc

> **Software Ecosystem:**
> - **NodeORC** = edge device orchestration (runs on the Pi, processes videos, reports to server)
> - **pyorc (pyOpenRiverCam)** = processing library (installed as NodeORC dependency)
> - **LiveORC** = cloud server (receives results, distributes tasks to devices)
> - **ORC-OS** = newer full dashboard project (alternative to NodeORC - discuss with ORC team)
>
> NodeORC does NOT capture video itself. It processes videos placed in its `incoming/` folder.
> The `orc-capture` script pulls video via RTSP from the camera and places it in `incoming/`.

### 11.1 Environmental Conditions

| Date | Time | Temp (°C) | Humidity (%) |
|------|------|-----------|--------------|
| | | | |

### 11.2 Prepare USB Flash Storage

NodeORC stores videos and results on disk. The Samsung FIT Plus 256GB USB flash drive
(mounted in Phase 4 as /dev/sda) must be formatted and mounted as the NodeORC home folder.

```bash
# Verify USB flash is detected
lsblk

# Create filesystem (if not already formatted)
# WARNING: This erases all data on the USB drive
sudo mkfs.ext4 -L nodeorc /dev/sda1

# Create mount point
sudo mkdir -p /mnt/usb

# Add to fstab for persistent mount
# Use LABEL to survive device reordering
echo 'LABEL=nodeorc /mnt/usb ext4 defaults,noatime 0 2' | sudo tee -a /etc/fstab

# Mount and verify
sudo mount -a
df -h /mnt/usb
```

| Check | Expected | Actual | Pass |
|-------|----------|--------|------|
| USB flash detected | /dev/sda | | [ ] |
| Filesystem created | ext4 | | [ ] |
| Mounted at /mnt/usb | Yes | | [ ] |
| Available space | ~230 GB | GB | [ ] |
| Persists after reboot | Yes | | [ ] |

### 11.3 Install NodeORC

**Source:** https://github.com/localdevices/nodeorc/releases
**Latest verified version:** v0.2.4 (March 2025) - confirm latest before install

```bash
# Download the setup script from latest release
wget https://github.com/localdevices/nodeorc/releases/latest/download/setup.sh

# Make executable and run full installation
chmod +x setup.sh
./setup.sh --all
```

The setup wizard will prompt for:
1. **LiveORC server URL** - obtain from ORC team (e.g., `https://liveorc.example.com:8000`)
2. **Username** - LiveORC account credentials
3. **Password** - LiveORC account credentials (not stored locally; only tokens retained)
4. **Storage location** - select USB storage (`/mnt/usb`)

> **Note:** Run `./setup.sh` without `--all` to see individual installation steps.
> Credentials are NOT stored locally - only temporary access tokens are retained.
>
> **CONFIRM WITH ORC TEAM:** LiveORC server URL and account credentials before this step.

| Step | Completed |
|------|-----------|
| setup.sh downloaded | [ ] |
| setup.sh executed without errors | [ ] |
| LiveORC server URL entered | [ ] |
| LiveORC credentials entered | [ ] |
| Storage location set to /mnt/usb | [ ] |
| NodeORC service started | [ ] |

```bash
# Verify installation
sudo systemctl status nodeorc.service
sudo journalctl -u nodeorc.service --no-pager -n 20
```

| Check | Expected | Actual | Pass |
|-------|----------|--------|------|
| nodeorc.service active | active (running) | | [ ] |
| No errors in journal | Clean startup | | [ ] |

**NodeORC version:** _______________

### 11.4 Verify Directory Structure

After installation, the home folder (`/mnt/usb`) should contain:

```bash
ls -la /mnt/usb/
```

| Directory/File | Purpose | Present |
|----------------|---------|---------|
| `incoming/` | New video files placed here for processing | [ ] |
| `results/` | Processing output (NetCDF, JPG) by day | [ ] |
| `success/` | Successfully processed videos by day | [ ] |
| `failed/` | Failed processing attempts by day | [ ] |
| `tmp/` | Temporary processing workspace | [ ] |
| `water_level/` | Water level data files | [ ] |
| `log/` | Daily log subdirectories | [ ] |
| `nodeorc_data.db` | Local processing database | [ ] |
| `settings/config_device.json` | Device configuration | [ ] |

### 11.5 Configure NodeORC Settings

**Configuration file:** `/mnt/usb/settings/config_device.json`

Review and adjust disk management settings:

```bash
# View current configuration
cat /mnt/usb/settings/config_device.json
```

| Setting | Recommended Value | Actual | Configured |
|---------|-------------------|--------|------------|
| home_folder | /mnt/usb | | [ ] |
| min_free_space | 2 (GB) | | [ ] |
| critical_space | 1 (GB) | | [ ] |

> **Disk management behavior:** When free space drops below `min_free_space`, NodeORC
> automatically removes oldest files from `failed/`, then `success/`, then `results/`.
> At `critical_space`, the service shuts down to preserve system accessibility.

To apply configuration changes:
```bash
python nodeorc upload-config /mnt/usb/settings/config_device.json
```

### 11.6 Configure RTSP Video Capture

**NodeORC does not capture video.** Videos must be placed in `incoming/` by an
external mechanism. The `orc-capture` script on the Pi pulls a ~5s video clip from the
camera's RTSP stream using ffmpeg.

**Architecture:**
1. `orc-capture` runs on the Pi (triggered by the duty-cycle schedule)
2. ffmpeg connects to the camera's RTSP stream and records a clip
3. The clip is placed in NodeORC's `incoming/` directory for processing

```bash
# Verify orc-capture is installed
which orc-capture.sh
cat /usr/local/bin/orc-capture.sh

# Test a manual capture
/usr/local/bin/orc-capture.sh

# Verify the output
ls -la /home/pi/Videos/
ffprobe /home/pi/Videos/*.mp4
```

| Step | Completed |
|------|-----------|
| orc-capture.sh installed at /usr/local/bin/ | [ ] |
| Camera RTSP stream accessible | [ ] |
| Manual capture produces valid .mp4 | [ ] |
| Video placed in NodeORC incoming/ directory | [ ] |
| File naming/format confirmed with ORC team | [ ] |

### 11.7 Test Manual Capture

```bash
# Ensure camera is powered and booted (wait ~90s after power-on)
# Run capture script manually
/usr/local/bin/orc-capture.sh

# Verify output
ls -la /mnt/usb/incoming/
ffprobe /mnt/usb/incoming/*.mp4
```

| Check | Expected | Actual | Pass |
|-------|----------|--------|------|
| Capture script runs without error | Yes | | [ ] |
| .mp4 file created in incoming/ | Yes | | [ ] |
| Filename format | YYYYMMDD_HHMMSS.mp4 | | [ ] |
| Video duration | ~5s | s | [ ] |
| Video resolution | ≥1080p | | [ ] |
| Video plays correctly | Yes | | [ ] |

### 11.8 Verify NodeORC Processing

After the capture script places a video in `incoming/`, NodeORC should automatically
detect and process it.

```bash
# Watch NodeORC logs in real time
sudo journalctl -u nodeorc.service -f
```

(In another terminal, run `/usr/local/bin/orc-capture.sh`, then watch the logs.)

| Check | Expected | Actual | Pass |
|-------|----------|--------|------|
| NodeORC detects new video | Log shows pickup | | [ ] |
| Processing begins | Log shows processing | | [ ] |
| Video moves to success/ or failed/ | File moved from incoming/ | | [ ] |
| Results appear in results/ | NetCDF/JPG files | | [ ] |

> **Note:** Processing will likely fail until a valid task is configured via LiveORC.
> At this stage, confirming that NodeORC *detects* the video and *attempts* processing
> is sufficient. Full end-to-end processing requires LiveORC task configuration (Phase 12).

### 11.9 Configure LiveORC Task Retrieval

NodeORC automatically polls the LiveORC server every 5 minutes for task configurations.
NodeORC v0.2.4 has built-in configuration pickup from LiveORC (GitHub Issue #49, closed
October 2024). No separate configuration retrieval mechanism is needed.

```bash
# Check if device has registered with LiveORC
sudo journalctl -u nodeorc.service | grep -i "task\|config\|announce"
```

| Check | Expected | Actual | Pass |
|-------|----------|--------|------|
| Device announces to LiveORC | Yes (in logs) | | [ ] |
| Polling for tasks (every 5 min) | Yes (in logs) | | [ ] |
| Task downloaded (if configured) | Yes/Pending | | [ ] |

> **CONFIRM WITH ORC TEAM:** Has a task template been configured on LiveORC for this device?
> Task templates define how videos are processed (velocity analysis parameters, etc.).
> Preparing task forms requires the LiveORC web interface.

### 11.10 Water Level Data Setup

NodeORC requires external water level data for discharge calculations.
Water level cannot be read optically by NodeORC.

**File location:** `/mnt/usb/water_level/all_levels.txt`
**Format:** Space-separated, no headers - datetime string and water level value

```
20260301_000000 92.367
20260301_001500 92.368
```

> **CONFIRM WITH ORC TEAM:** How will water level data be supplied at Sukabumi?
> Options:
> 1. Manual file updates via Pangolin remote access
> 2. API harvesting script (if water levels posted to central platform)
> 3. Direct sensor reading (requires additional hardware/software)

| Step | Completed |
|------|-----------|
| water_level/ directory exists | [ ] |
| Water level data source identified | [ ] |
| Data supply method documented | [ ] |

**Water level data source:** _______________
**Supply method:** _______________

### 11.11 Verification

| Check | Pass |
|-------|------|
| USB flash mounted at /mnt/usb | [ ] |
| NodeORC installed and service running | [ ] |
| Directory structure correct | [ ] |
| config_device.json reviewed | [ ] |
| RTSP capture configured and tested | [ ] |
| Manual capture produces valid video | [ ] |
| NodeORC detects videos in incoming/ | [ ] |
| LiveORC connectivity confirmed | [ ] |
| Water level data approach documented | [ ] |

**Notes:**
```
NodeORC version:
Config file path: /mnt/usb/settings/config_device.json
LiveORC server URL:
RTSP capture script: /usr/local/bin/orc-capture.sh
Water level approach:
ORC team contact for task configuration:


```

### 11.12 Open Items for ORC Team Coordination

These items require input from the ORC team before Phase 12:

| Item | Status | Contact/Notes |
|------|--------|---------------|
| LiveORC server URL and credentials | [ ] Obtained | |
| LiveORC task template configured | [ ] Confirmed | |
| RTSP capture verified | [ ] Tested | |
| Water level data approach agreed | [ ] Documented | |
| ORC-OS vs NodeORC decision | [ ] Discussed | See note below |
| Credential management approach | [ ] Agreed | For camera password |

> **ORC-OS Note:** The ORC team has a newer project called ORC-OS
> (https://github.com/localdevices/ORC-OS) that provides a full web dashboard with
> FastAPI backend. It may be a better fit than raw NodeORC depending on team direction.
> Discuss with ORC team before finalizing - both approaches are compatible with LiveORC.

---

## Phase 12: Integration Testing

**Goal:** Test complete system end-to-end
**Prerequisite:** Phase 11 complete
**Critical:** Test Pangolin remote access before final assembly

### 12.1 Environmental Conditions

| Date | Time | Temp (°C) | Humidity (%) |
|------|------|-----------|--------------|
| | | | |

### 12.2 Power Cycle Test

| Step | Result | Pass |
|------|--------|------|
| Power off completely | | |
| Disconnect bench power | | |
| Connect 12V supply (simulating solar) | | |
| System boots | | [ ] |
| All components initialize | | [ ] |

### 12.3 Full Capture Cycle

Run a full RTSP capture cycle and verify NodeORC processes the result:

```bash
# Ensure camera is booted (wait ~90s after power-on)
# Run capture script
/usr/local/bin/orc-capture.sh

# Monitor NodeORC processing
sudo journalctl -u nodeorc.service -f
```

| Step | Expected | Actual | Pass |
|------|----------|--------|------|
| System boot | ≤60s | s | [ ] |
| Camera RTSP ready | ≤90s from boot | s | [ ] |
| RTSP capture completes | .mp4 in incoming/ | | [ ] |
| NodeORC detects video | Log shows pickup | | [ ] |
| NodeORC processes video | Log shows processing | | [ ] |
| Results or callback | success/ or failed/ | | [ ] |
| Rain gauge reading | Value returned | | [ ] |
| Data upload (or queue) | Success/queued | | [ ] |
| LEDs indicate status | Correct colors | | [ ] |

### 12.4 Pangolin Remote Access Test

**CRITICAL: Test before enclosure is difficult to access**

| Test | From | Result | Pass |
|------|------|--------|------|
| SSH via Pangolin | Remote machine | | [ ] |
| Commands execute | Remote | | [ ] |
| File transfer | Remote | | [ ] |
| Connection stable | 5+ minutes | | [ ] |

### 12.5 Maintenance Mode Test

| Step | Expected | Actual | Pass |
|------|----------|--------|------|
| Long-press button (3s) | Mode activates | | [ ] |
| LED indicates maintenance | Yes | | [ ] |
| WiFi hotspot starts | SSID visible | | [ ] |
| Connect to hotspot | Success | | [ ] |
| SSH via hotspot | Success | | [ ] |
| Exit maintenance mode | Works | | [ ] |

### 12.6 NodeORC Service Resilience

```bash
# Verify service restarts after reboot
sudo reboot
# (after reboot)
sudo systemctl status nodeorc.service
```

| Test | Action | Expected Behavior | Pass |
|------|--------|-------------------|------|
| Service survives reboot | Reboot Pi | nodeorc.service active | [ ] |
| LiveORC polling resumes | Check logs after reboot | "announce" or "task" in logs | [ ] |
| USB storage remounts | Check /mnt/usb after reboot | Mounted, files intact | [ ] |

### 12.7 Error Condition Tests

| Test | Action | Expected Behavior | Pass |
|------|--------|-------------------|------|
| Camera offline | Disconnect Ethernet | Capture script fails, error logged | [ ] |
| Modem offline | Remove antenna | NodeORC queues callbacks for retry | [ ] |
| Rain gauge offline | Disconnect | Graceful failure, logged | [ ] |
| LiveORC unreachable | Block outbound | NodeORC continues with existing tasks | [ ] |
| Disk full simulation | Fill /mnt/usb to min_free_space | Automatic cleanup of oldest files | [ ] |

### 12.8 Verification

| Check | Pass |
|-------|------|
| Power cycle works | [ ] |
| Full capture + processing cycle works | [ ] |
| NodeORC service resilient across reboots | [ ] |
| Pangolin remote access works | [ ] |
| Maintenance mode works | [ ] |
| Error handling works | [ ] |
| LiveORC connectivity confirmed | [ ] |

**Notes:**
```
NodeORC processing status (success/failed/pending task):
Pangolin connection details (document securely):
Capture cycle total time (boot to shutdown-ready):


```

---

## Phase 13: Power Budget Verification

**Goal:** Verify power consumption within solar budget
**Prerequisite:** Phase 12 complete
**Target:** <94 Wh/day

### 13.1 Environmental Conditions

| Date | Time | Temp (°C) | Humidity (%) |
|------|------|-----------|--------------|
| | | | |

### 13.2 Test Setup

| Item | Value |
|------|-------|
| Power supply voltage | V |
| Measurement method | (inline ammeter / bench supply) |
| Multimeter model | |

### 13.3 Current Measurements

| State | Duration | Current (A) | Power (W) |
|-------|----------|-------------|-----------|
| Boot (Pi + camera) | ~60s | | |
| Active (capture/upload) | ~90s | | |
| Idle | ~10s | | |
| Sleep (Witty Pi only) | ~13 min | mA | mW |

### 13.4 Acceptance Criteria - Current

| State | Maximum | Measured | Pass |
|-------|---------|----------|------|
| Boot peak | 3.5 A | A | [ ] |
| Boot steady | 3.0 A | A | [ ] |
| Active steady | 2.5 A | A | [ ] |
| Idle | 1.5 A | A | [ ] |
| Sleep | 50 mA | mA | [ ] |

### 13.5 Calculate Daily Energy

**Cycle timing:**
- Boot: 60s
- Active: 90s
- Idle: 10s
- Sleep: 780s
- Cycles/day: ~92

| Phase | Power (W) | Time (s) | Energy/cycle (Wh) |
|-------|-----------|----------|-------------------|
| Boot | | 60 | |
| Active | | 90 | |
| Idle | | 10 | |
| Sleep | | 780 | |
| **Total/cycle** | | | |

**Daily energy:** _______ Wh/cycle × 92 cycles = _______ Wh/day

### 13.6 Acceptance Criteria - Energy

| Metric | Target | Maximum | Actual | Pass |
|--------|--------|---------|--------|------|
| Daily consumption | <80 Wh | 94 Wh | Wh | [ ] |
| Battery autonomy | >5 days | >3 days | days | [ ] |

**Battery autonomy:** 480 Wh (50Ah × 12V × 0.8) ÷ _____ Wh/day = _____ days

### 13.7 Verification

| Check | Pass |
|-------|------|
| All current measurements within limits | [ ] |
| Daily energy within budget | [ ] |
| Battery autonomy acceptable | [ ] |

**Notes:**
```



```

---

## Phase 14: Schedule Testing

**Goal:** Verify Witty Pi automatic wake/sleep cycles
**Prerequisite:** Phase 13 complete
**Hold Point:** Schedule must work reliably

### 14.1 Environmental Conditions

| Date | Time | Temp (°C) | Humidity (%) |
|------|------|-----------|--------------|
| | | | |

### 14.2 Short Test Schedule (3 cycles)

Set temporary schedule: 1 min on, 2 min off

```bash
cd ~/wittypi
./wittyPi.sh
# Configure and enable short test schedule
```

| Cycle | Expected Wake | Actual Wake | Expected Sleep | Actual Sleep | Pass |
|-------|---------------|-------------|----------------|--------------|------|
| 1 | | | | | [ ] |
| 2 | | | | | [ ] |
| 3 | | | | | [ ] |

| Check | Pass |
|-------|------|
| Wakes on schedule (±5s) | [ ] |
| Sleeps on schedule (±5s) | [ ] |
| RTC time accurate | [ ] |

### 14.3 Production Schedule Test (4+ cycles)

Set production schedule: 2.5 min on, 12.5 min off

| Cycle | Wake | Camera Ready | Capture OK | Upload | Sleep | Pass |
|-------|------|--------------|------------|--------|-------|------|
| 1 | | [ ] | [ ] | | | [ ] |
| 2 | | [ ] | [ ] | | | [ ] |
| 3 | | [ ] | [ ] | | | [ ] |
| 4 | | [ ] | [ ] | | | [ ] |
| 5 | | [ ] | [ ] | | | [ ] |
| 6 | | [ ] | [ ] | | | [ ] |

### 14.4 Verify LiveORC Task Polling

| Cycle | Task Poll Logged | Result |
|-------|------------------|--------|
| 1 | [ ] | unchanged / updated / unreachable |
| 2 | [ ] | unchanged / updated / unreachable |

### 14.5 Acceptance Criteria

| Criterion | Requirement | Actual | Pass |
|-----------|-------------|--------|------|
| Wake accuracy | ±10s | s | [ ] |
| Sleep accuracy | ±10s | s | [ ] |
| Camera ready margin | ≥30s before capture | s | [ ] |
| Consecutive successful cycles | ≥4 | | [ ] |
| Missed wakes | 0 | | [ ] |
| LiveORC task poll runs | Each wake | | [ ] |

### 14.6 Hold Point Sign-Off

| Verification | Initials | Date |
|--------------|----------|------|
| Short test passed | | |
| Production test (4+ cycles) passed | | |
| LiveORC task polling working | | |
| **Approved to proceed to Phase 15** | | |

**Schedule file used:** _______________

**Notes:**
```



```

---

## Phase 15: Environmental Testing

**Goal:** Verify thermal performance and enclosure sealing
**Prerequisite:** Phase 14 complete

### 15.1 Environmental Conditions

| Date | Time | Temp (°C) | Humidity (%) |
|------|------|-----------|--------------|
| | | | |

### 15.2 Thermal Test

Run system continuously for 30+ minutes.

```bash
# Monitor temperature
watch -n 5 vcgencmd measure_temp
```

| Time | CPU Temp (°C) | Ambient (°C) | Notes |
|------|---------------|--------------|-------|
| 0 min | | | |
| 10 min | | | |
| 20 min | | | |
| 30 min | | | |

| Check | Requirement | Actual | Pass |
|-------|-------------|--------|------|
| CPU temp stable | ≤70°C | °C | [ ] |
| No thermal throttling | None in dmesg | | [ ] |
| Active cooler running | Yes | | [ ] |

### 15.3 Seal Inspection

| Check | Pass |
|-------|------|
| All cable glands tight | [ ] |
| Enclosure gasket seated | [ ] |
| Gore vent intact | [ ] |
| No visible gaps | [ ] |

### 15.4 Shake/Vibration Test

| Check | Pass |
|-------|------|
| Shake enclosure firmly (30s) | [ ] |
| No rattles or loose items | [ ] |
| System still functions after | [ ] |

### 15.5 Verification

| Check | Pass |
|-------|------|
| Thermal performance OK | [ ] |
| Enclosure sealed | [ ] |
| Vibration test passed | [ ] |

**Notes:**
```



```

---

## Phase 16: Final Verification

**Goal:** Complete all documentation and verify deployment readiness
**Prerequisite:** Phase 15 complete
**Hold Point:** Final sign-off required

### 16.1 Documentation Checklist

| Document | Location | Complete |
|----------|----------|----------|
| This build checklist | sukabumi/ | [ ] |
| Component registry | Phase 0 | [ ] |
| All photos | sukabumi/photos/ | [ ] |
| Wiring diagram | sukabumi/ | [ ] |
| Configuration backup | Secure location | [ ] |
| Credentials | Secure location | [ ] |

### 16.2 Configuration Backup

| Item | Backed Up | Location |
|------|-----------|----------|
| SD card image | [ ] | |
| ORC config file | [ ] | |
| Witty Pi schedule | [ ] | |
| Network settings | [ ] | |
| Camera config documented | [ ] | |

### 16.3 System State

| Check | Status |
|-------|--------|
| All phases complete | [ ] |
| All hold points signed | [ ] |
| Schedule | DISABLED (enable at deployment) |
| System shutdown | Clean |

### 16.4 Physical Verification

| Check | Pass |
|-------|------|
| Enclosure sealed | [ ] |
| All screws tight | [ ] |
| All cable glands tight | [ ] |
| Antenna secure | [ ] |
| Gore vent intact | [ ] |
| LEDs functional | [ ] |
| Button functional | [ ] |
| All cables labeled | [ ] |
| Exterior clean | [ ] |

### 16.5 Spare Parts

| Item | Qty | Packed |
|------|-----|--------|
| Spare SD card (imaged) | 1 | [ ] |
| Spare fuses | 2 | [ ] |
| Spare cable glands | 3 | [ ] |
| Conformal coating | 1 | [ ] |
| Dielectric grease | 1 | [ ] |
| Cable ties | 20+ | [ ] |
| Spare resistors | 5 | [ ] |

### 16.6 Build Summary

| Metric | Value |
|--------|-------|
| Build start date | |
| Build completion date | |
| Total build time | |
| Issues encountered | |
| Daily power consumption | Wh/day |

### 16.7 Final Acceptance

| Criterion | Met |
|-----------|-----|
| All 16 phases complete | [ ] |
| All 6 hold points passed | [ ] |
| Power budget met (<94 Wh/day) | [ ] |
| Schedule tested (4+ cycles) | [ ] |
| Remote access verified | [ ] |
| Documentation complete | [ ] |
| Spare parts packed | [ ] |

### 16.8 Sign-Off

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Builder | | | |
| Reviewer | | | |

**Unit is approved for deployment: [ ]**

**Notes:**
```



```

---

## Known Issues

Document any issues encountered during build.

### Issue Log

| # | Phase | Description | Resolution | Status |
|---|-------|-------------|------------|--------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

### Issue Detail Template

```
## Issue #X: [Brief description]

**Phase:**
**Date:**
**Severity:** Blocking / Major / Minor

### Symptoms


### Root Cause


### Resolution


### Prevention / Checklist Update Needed

```

---

## Appendix: Quick Reference

### GPIO Assignments

| Function | GPIO | Pin |
|----------|------|-----|
| Green LED | | |
| Yellow LED | | |
| Red LED | | |
| Maint Button | | |
| Rain Gauge TX | 15 | 10 |
| Rain Gauge RX | 14 | 8 |

### Network Configuration

| Device | IP Address | Credentials Location |
|--------|------------|---------------------|
| Pi (Ethernet) | | |
| Pi (Cellular) | Dynamic | |
| Camera | | Secure storage |

### Key Commands

```bash
# Witty Pi
cd ~/wittypi && ./wittyPi.sh

# Modem status
mmcli -m 0

# Camera test (ISAPI snapshot)
curl --digest -u admin:PASSWORD http://CAMERA_IP/ISAPI/Streaming/channels/101/picture -o /tmp/test.jpg

# Rain gauge
minicom -b 9600 -D /dev/serial0

# Temperature
vcgencmd measure_temp

# I2C scan
sudo i2cdetect -y 1
```
