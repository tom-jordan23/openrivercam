# RC-Box Design Effort

## Project Overview

We are working to adapt the OpenRiverCam approach to humanitarian river monitoring, and we want to build a hardware package that will be easily deployable by National Societies that may not have specialized training in hydrology, GIS, survey processes or electronics / electrical systems.

The platform should consist of a Raspberry Pi 5 (with PiJuice / PiSugar to control a regular startup and shutdown process) running the ORC-OS software. It should include **2 sealed IP67/IP68 cameras** mounted separately and connected via USB or WiFi. The device must be easily deployable with basic training, and needs to be weatherproof in all environments and able to withstand the abuse of shipping, warehousing and being handled by untrained staff. Everything must be field serviceable. The device needs to be able to connect via wireless or cellular modem.

---

## Core Design Principles

### 1. Widely Available Components with Good Community Support

**Why this matters:** Humanitarian deployments happen in remote locations worldwide. Components must be sourceable, replaceable, and well-documented.

| Principle | Implementation |
|-----------|----------------|
| **No proprietary or single-source components** | Every critical component must have at least 2-3 alternative suppliers or compatible substitutes |
| **Prefer commodity standards** | USB, 12V DC, standard screw terminals, M-series cable glands, 40-pin GPIO header |
| **Active community/forums** | Raspberry Pi, Arduino ecosystem parts have years of community troubleshooting available |
| **Open documentation** | Datasheets, schematics, and repair guides must be publicly available |
| **Global availability** | Components should be purchasable from Amazon, AliExpress, DigiKey, Mouser, or regional equivalents |
| **Avoid bleeding edge** | Use proven technology (1-2 years in market minimum) over newest releases |

**Examples:**
- ✅ Raspberry Pi 5 - massive community, global availability, extensive documentation
- ✅ LiFePO4 batteries - commodity chemistry, multiple manufacturers
- ✅ USB cameras - standard interface, many options
- ✅ M16/M20 cable glands - industry standard, available everywhere
- ❌ Custom PCBs - hard to replace, no community support
- ❌ Proprietary connectors - lock-in, sourcing problems

### 2. Resilient in All Environments

**Why this matters:** These devices will be shipped internationally, stored in warehouses, installed by non-experts, and left unattended for months in harsh conditions.

| Challenge | Design Response |
|-----------|-----------------|
| **Shipping damage** | No fragile components; foam-padded internals; secure mounting for all parts |
| **Rough handling** | Tool-free external operation; recessed switches; no exposed connectors during transport |
| **Extreme temperatures** | -20°C to +50°C rated components; LiFePO4 chemistry; thermal management |
| **High humidity/tropics** | IP67 sealed enclosures; sealed cameras; GORE vents; ant-proofing |
| **Dust/sand** | IP6x dust-tight rating on all enclosures and cameras |
| **Rain/flooding** | IP67 waterproof; elevated mounting; sealed cable entries |
| **Power fluctuations** | Surge protection; quality DC-DC conversion; battery buffer |
| **Vibration (pole sway)** | Secure mounting; locking connectors; no loose wires |
| **UV exposure** | UV-stabilized enclosure materials; shaded components where possible |
| **Vandalism/theft** | Security screws; pole mounting; optional GPS tracking |

**Design rules:**
- Every connection must be mechanically secured (screw terminals, not push-fit)
- All cables must have strain relief
- No component should fail from a 1-meter drop (packaged)
- System must survive complete power loss and restart cleanly
- Assume worst-case environment, not best-case

### 3. Easily Field Serviceable

**Why this matters:** When something fails, a local volunteer with basic tools and a phone connection to remote support must be able to diagnose and fix it.

| Principle | Implementation |
|-----------|----------------|
| **Modular components** | Each function is a separate, replaceable module (camera, battery, Pi, modem) |
| **No soldering required** | All connections via screw terminals, plugs, or headers |
| **Common tools only** | Phillips screwdriver, adjustable wrench, wire strippers - nothing specialized |
| **Visual diagnostics** | LEDs visible from ground; display shows status; clear error indicators |
| **Labeled everything** | Every wire, connector, and component has printed/engraved labels |
| **Photo documentation** | Photos of correct assembly included in each unit for reference |
| **Spare parts included** | Ship extra fuses, glands, terminals, connectors with each deployment |
| **Remote diagnostics** | System reports health metrics; support can diagnose remotely |
| **Graceful degradation** | Single component failure shouldn't brick the entire system |

**Serviceability checklist:**
- [ ] Can a non-technical person identify which component failed?
- [ ] Can they obtain a replacement locally or from shipped spares?
- [ ] Can they swap the component with only common tools?
- [ ] Can they verify the repair worked without special equipment?
- [ ] Is there documentation (printed, in-box) for this repair?

**Design rules:**
- No component should require more than 5 minutes to replace
- Every cable must be clearly labeled at both ends
- Use different connector types/colors for different functions (can't plug wrong cable into wrong port)
- Include QR codes linking to video repair guides
- Test every repair procedure with a non-technical person before finalizing design

---

## Current Design Decisions (2024-12-01)

### Camera System: Sealed IP67/IP68 Units (Primary Approach)
- **Decision:** Use factory-sealed IP67/IP68 cameras instead of Pi Camera V3 in custom housings
- **Quantity:** 2 cameras per station
- **Connectivity Options:**
  - USB (5m native, up to 30m with active repeater, 100m via USB-over-Ethernet)
  - WiFi (for sites where cables cannot be run)
- **Rationale:** Factory sealing eliminates fogging/humidity issues that plagued Indonesia deployment; no desiccant maintenance required
- **Fallback:** Active dehumidification available for cameras and/or compute enclosure if sealed cameras prove unsuitable

### Power System: Overbuilt with LiFePO4
- **Design Principle:** Overbuild power by 50-100% - excess capacity is cheap insurance
- **Battery Chemistry:** LiFePO4 for all tiers (no lead-acid)
  - 2000-5000 cycle life vs 300-500 for lead-acid
  - 90% usable DOD vs 50% for SLA
  - No toxic materials, fully recyclable
  - Better tropical heat tolerance

| Tier | Solar | Battery | Headroom | Backup Days |
|------|-------|---------|----------|-------------|
| Low | 50W | 20Ah LiFePO4 | 72% | 2.1 days |
| Mid | 100W | 50Ah LiFePO4 | 166% | 3.6 days |
| High | 200W | 100Ah LiFePO4 | 200%+ | 4+ days |

### Environmental Protection
- **IP Rating:** Minimum IP67 (dust-tight, waterproof to 1m for 30 minutes)
- **Ant-Proof:** All entry points sealed; no gaps >0.5mm (critical lesson from Indonesia)
- **Temperature Range:** -20°C to +50°C
- **Humidity:** 0-100% RH (sealed enclosure with pressure vent)

---

## Power Management System

### Automated Startup/Shutdown (Required)

The Pi must wake on a schedule (e.g., 2-3 minutes every 15 minutes), record video, then shut down to conserve power. This requires RTC wake capability.

#### Option 1: Witty Pi 4 (Recommended for Pi 5)

| Feature | Specification |
|---------|---------------|
| Compatibility | All 40-pin Pi models including **Pi 5** |
| RTC Accuracy | ±2ppm (factory calibrated, temperature compensated) |
| Wake Scheduling | Complex schedule scripts supported |
| Power Input | 5-26V DC (wide input range) |
| Software | Web interface (UWI), command line tools |
| Price | ~$25-35 |

**Installation:**
```bash
wget https://www.uugear.com/repo/WittyPi4/install.sh
sudo sh install.sh
```

**Key Features:**
- Schedule scripts allow complex ON/OFF sequences
- RTC keeps time for 1+ year without power (with coin cell backup)
- Can trigger external devices via GPIO during wake cycles
- [Witty Pi 4 Product Page](https://www.uugear.com/product/witty-pi-4/)

#### Option 2: PiSugar 3 Plus

| Feature | Specification |
|---------|---------------|
| Compatibility | Pi Zero, 3, 4, **5** |
| Battery | Built-in 5000mAh LiPo (optional for UPS function) |
| RTC | Yes, with scheduled wake |
| Power Input | 5V USB-C |
| Software | Web interface, Python API |
| Price | ~$40-50 |

**Notes:**
- [PiSugar 3 Series](https://docs.pisugar.com/docs/product-wiki/battery/pisugar3/pisugar-3-series) includes hardware battery protection and software watchdog
- Built-in battery provides UPS functionality during power transitions
- Anti-mistaken touch switch prevents accidental shutdowns

#### Option 3: Native Pi 5 RTC (Simplest)

The Raspberry Pi 5 has a built-in RTC that can wake the system:

```bash
# Set wake alarm (seconds from now)
echo +300 > /sys/class/rtc/rtc0/wakealarm

# Verify alarm is set
date -d @$(cat /sys/class/rtc/rtc0/wakealarm)
```

**Limitations:**
- Requires external battery backup coin cell (CR2032)
- Only handles wake - shutdown must be scheduled via cron/at
- No integrated power switching - needs external relay or power HAT
- Less robust than dedicated power management boards

#### Recommendation

**Witty Pi 4** is recommended because:
- Confirmed Pi 5 compatibility
- Wide input voltage (5-26V) works directly with 12V battery system
- Schedule scripts handle complex duty cycles
- Does not require its own battery (uses main system battery)
- Provides GPIO output for triggering IR spotlight

---

## 5V Power Conditioning

### Power Quality Requirements

The Pi 5 requires clean, stable 5V power capable of 5A peak. Poor power quality causes:
- Undervoltage warnings (lightning bolt icon)
- SD card corruption
- Random reboots
- USB device disconnection

### Power Conditioning Strategy

#### If Using Quality MPPT Charge Controller with USB Output

Many MPPT controllers (e.g., Victron SmartSolar, Renogy Rover) include USB outputs with built-in regulation. Check specifications for:
- Output voltage stability: Should be 5.0-5.2V ±0.1V
- Current capacity: Minimum 3A, prefer 5A
- Ripple/noise: <50mV peak-to-peak
- Overcurrent/overvoltage protection

**If the controller's USB output meets these specs, no additional conditioning is needed.**

#### If Using 12V Battery → Buck Converter

When powering Pi from 12V battery via DC-DC converter, use a quality buck converter:

| Feature | Minimum Spec | Recommended |
|---------|-------------|-------------|
| Output Voltage | 5.0-5.2V adjustable | 5.1V fixed |
| Output Current | 3A continuous | 5A continuous |
| Efficiency | >85% | >90% |
| Input Voltage | 10-18V | 8-30V wide range |
| Protections | OVP, OCP, short circuit | + reverse polarity, thermal |
| Ripple | <100mV | <50mV |

**Recommended Products:**
- [PlusRoc Waterproof 12V-24V to 5V](https://www.amazon.com/PlusRoc-Waterproof-Converter-Compatible-Raspberry/dp/B09DGDQ48H) - 96% efficiency, USB-C, outdoor rated
- LM2596-based modules with adjustable output (verify quality)
- Mean Well industrial DC-DC converters

#### Additional Filtering (Optional)

For noisy environments or long cable runs, add a supercapacitor filter board:

| Component | Purpose |
|-----------|---------|
| [ConditionerPi](https://iancanada.ca/products/30a-conditionerpi-raspberry-pi-power-supply-conditioner-board-with-ultra-capacitors) | Ultra-capacitor filter HAT, reduces ESR and noise |
| 1000-10000µF electrolytic capacitor | Smooths voltage dips, placed near Pi |
| TVS diode (5.5V) | Transient voltage suppression for spikes |

**Wiring Notes:**
- Use 18AWG or thicker wire for 5V connections
- Keep 5V cable runs as short as possible (<30cm ideal)
- Connect to GPIO header pins 2,4 (+5V) and 6,9,14,20,25,30,34,39 (GND)
- Always include a 5A polyfuse if powering via GPIO (Pi 5 has no on-board polyfuse)

### Power Protection Chain

```
[Solar Panel] → [Surge Protector] → [Charge Controller] → [LiFePO4 Battery]
                                                                   │
                                                            [Fuse 20A]
                                                                   │
                    ┌──────────────────────────────────────────────┤
                    │                                              │
              [DC-DC 12V→5V]                              [IR Spotlight]
              with protection                              via relay
                    │
              [Polyfuse 5A]
                    │
              [Pi 5 via GPIO]
              or USB-C PD
```

---

## IR Spotlight System

### Purpose

Night recording requires infrared illumination. The sealed cameras must be "NoIR" type (no IR filter) or have IR sensitivity. The IR spotlight must:
- Turn on when Pi wakes for recording
- Turn off when Pi shuts down (to save power)
- Operate on 12V from main battery

### IR Wavelength Selection

| Wavelength | Visibility | Range | Use Case |
|------------|-----------|-------|----------|
| **850nm** | Faint red glow at LEDs | Full range | Recommended - better camera sensitivity |
| 940nm | Completely invisible | 30-40% less range | Covert installations only |

**Recommendation:** 850nm for river monitoring - visibility is not a concern, and range is important.

### IR Spotlight Options

#### Option 1: Standalone 12V IR Flood Light (Recommended)

| Specification | Requirement |
|--------------|-------------|
| Wavelength | 850nm |
| Power | 10-20W (12V DC) |
| Beam Angle | 60-90° flood |
| Range | 30-60m (100-200ft) |
| IP Rating | IP65 or better |
| Control | Via relay (no built-in sensor) |

**Example Products:**
- [OOSSXX IR Illuminator](https://oossxx.com/products/ir-illuminator-850nm-12-led-ir-illuminators-ir-lights-for-security-cameras-10ft-12v-2a-power-supply-ohwoai-long-range-infrared-light-outdoor-ir-floodlight-wide-angle-for-cctv-ip-camera-night-vision) - 12 LED, 850nm, 90°, 120ft range, IP65
- [CMVision IR Illuminators](https://cmvisionsecurity.com/collections/03-infrared-illuminator) - Various power/range options
- [AXTON IR Illuminators](https://axtontech.com/) - Professional grade, 850nm/940nm options

#### Option 2: Camera-Integrated IR

Some sealed IP cameras include built-in IR LEDs. If using these:
- Verify IR is controllable (not always-on)
- Check power consumption - may need to account for 5-10W extra
- Range may be limited (typically 5-15m)

### IR Spotlight Control Circuit

The IR spotlight is controlled by a relay triggered by Witty Pi 4 GPIO during wake cycles.

#### Components Required

| Component | Specification | Purpose |
|-----------|--------------|---------|
| Relay module | 5V coil, 12V/10A contacts | Switches IR spotlight power |
| GPIO wire | From Witty Pi 4 or Pi GPIO | Trigger signal |
| 12V power | From main battery/terminal block | Powers IR spotlight |
| Diode (1N4007) | Across relay coil | Flyback protection |

#### Wiring Diagram

```
                        [12V from Terminal Block]
                                  │
                            [Fuse 5A]
                                  │
                    ┌─────────────┼─────────────┐
                    │             │             │
              [IR Spotlight]      │        [Relay Module]
                    │             │         NC  COM  NO
                    │             └──────────────┤
                    │                            │
                    └────────────────────────────┘

                              [Relay Coil]
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
               [Diode 1N4007]              [GPIO Pin]
                    │                      (from Witty Pi 4
                    └───────[GND]───────────or Pi GPIO)
```

#### Software Control

**Witty Pi 4 Approach (Recommended):**

Witty Pi 4 can output a signal on GPIO during scheduled wake periods. Configure in schedule script:
```
# In Witty Pi schedule script
# GPIO goes HIGH when Pi is awake, LOW when shutdown
```

**Direct GPIO Control:**

Add to recording script:
```python
import RPi.GPIO as GPIO

IR_RELAY_PIN = 17  # Choose available GPIO

def ir_spotlight_on():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(IR_RELAY_PIN, GPIO.OUT)
    GPIO.output(IR_RELAY_PIN, GPIO.HIGH)

def ir_spotlight_off():
    GPIO.output(IR_RELAY_PIN, GPIO.LOW)
    GPIO.cleanup()

# In recording sequence:
ir_spotlight_on()
time.sleep(2)  # Allow IR to stabilize
# ... record video ...
ir_spotlight_off()
```

#### Power Budget for IR Spotlight

| Component | Power | Daily Usage (2-3 min/15 min) | Daily Energy |
|-----------|-------|------------------------------|--------------|
| 12W IR spotlight | 12W @ 12V = 1A | ~3.2-4.8 hours | 38-58 Wh |
| Relay coil | 0.5W | Same as spotlight | 1.6-2.4 Wh |
| **Total IR system** | 12.5W | | **40-60 Wh/day** |

**Note:** This is already accounted for in the power headroom. The 50-100% overbuilt solar/battery handles IR load.

### Bill of Materials: IR Spotlight System

| Component | Quantity | Notes |
|-----------|----------|-------|
| 850nm IR flood light (12V, 10-20W) | 1-2 | One per camera, or one wide-angle |
| 5V relay module | 1 | SPDT, 10A contacts minimum |
| 1N4007 diode | 1 | Flyback protection |
| 18AWG wire (red/black) | 2m | 12V power to spotlight |
| M16 IP68 cable gland | 1 | For IR power cable entry |
| Waterproof inline connector | 1 | For field disconnect of IR spotlight |

### Camera Entry Points (Updated)

Configuration B combined box now needs additional entry for IR spotlight:

| Entry | Cable/Connection | Gland Size | Type |
|-------|-----------------|------------|------|
| 1 | Solar Panel MC4+ | M20 | IP68 gland |
| 2 | Solar Panel MC4- | M20 | IP68 gland |
| 3 | USB Camera 1 | M16 | IP68 USB gland |
| 4 | USB Camera 2 | M16 | IP68 USB gland |
| 5 | Cellular Antenna | M12 | IP67 SMA bulkhead |
| 6 | WiFi Antenna | M12 | IP67 SMA/RP-SMA bulkhead |
| 7 | Ground/Earth | M16 | IP68 compression gland |
| 8 | **IR Spotlight power** | M16 | IP68 compression gland |
| 9 | Spare/Sensor | M16 | IP68 blanking plug |

---

## Enclosure Configurations

Two configurations are supported based on deployment requirements:

### Configuration A: Separate Compute Box
- **Box 1:** Compute enclosure (Pi 5, modem, USB hub)
- **Box 2:** Power enclosure (battery, charge controller, fuses)
- **Use Case:** Thermal separation, flexible positioning, easier servicing

### Configuration B: Combined Electrical + Compute Box
- **Single enclosure:** All components except cameras and solar panel
- **Use Case:** Simpler installation, fewer penetrations, single mounting point

See [Enclosure Specifications](#enclosure-specifications) below for detailed connection diagrams.

---

In a recent deployment in Indonesia, we assembled the following list of improvements for a future hardware platform:

Don't depend on local procurement for specialized items. Maybe minimize local procurement wherever we can.
Make sure hardware is resilient against shipping damage
Ship consumables that might be even remotely hard to source - we spent lots of time driving around to find little things that I could have easily packed or shipped
Include extras of fittings, terminals, fuses, etc. to leave behind in the box for later service
Mark all connections distinctly and then photograh to help with remote troubleshooting
Provide better engineering specs in advance for the pole or mast - diameter, material, rigidity, lateral load, etc.
If using an arm, calculate moment to factor into vibration or sway
Give time for at least two full surveys. Save original source data from both.
Hardware needs a visual indicator of whether it's on or not, and it needs to be visible from the ground while on the pole
Hardware soft power switch makes it impossible to know if the device has been turned on or not
We need a better way to capture the intended video orientation and angle, especially for steep banks. 
There's not an obvious way in the software to change the orientation of the video (portrait / landscape / rotate).
Need a mounting system that allows for easier changes in orientation to find a proper picture
Consider a different approach to cameras - something simpler, off the shelf and easily field replaceable.
Create a hardware switch we can use to turn on a local wireless hotspot for configuration.
Create a hardware switch we can use to put the device into maintenance mode / cycling mode / power on / power off
Provide a configuration that uses commercial power and / or network if available
Maybe a way to communicate what the startup / shutdown sequence is other than trying the website over and over again
Hardware should have a lot more local storage than what they appear to have - we need to make sure they can operate for a long time without a stable connection without losing data
Device should show in the UI whether it is in maintenance mode or not, and how long the timer. Should also give an option to extend maintenance mode.

---

## Enclosure Specifications

### Configuration A: Separate Compute Box (Two-Box System)

**Use Case:** Sites where thermal management is critical, or where compute unit needs to be positioned differently than power system.

#### Box 1: Compute Enclosure
Contains: Raspberry Pi 5, 4G modem/WiFi, USB hub (if needed)

**Enclosure Specifications:**
- Size: ~200mm x 150mm x 100mm (8" x 6" x 4")
- Material: Polycarbonate or ABS, IP67 rated
- Mounting: DIN rail or standoff mounts inside
- Color: White or light gray (heat reflection)

**Cable Entry Points:**

| Entry | Cable/Connection | Gland Size | Type |
|-------|-----------------|------------|------|
| 1 | DC Power In (12V from battery box) | M20 | IP68 compression gland |
| 2 | USB Camera 1 | M16 | IP68 USB pass-through or gland |
| 3 | USB Camera 2 | M16 | IP68 USB pass-through or gland |
| 4 | Cellular Antenna (SMA) | M12 | IP67 SMA bulkhead connector |
| 5 | WiFi Antenna (if external) | M12 | IP67 SMA/RP-SMA bulkhead |
| 6 | Spare/Sensor | M16 | IP68 blanking plug (until needed) |

#### Box 2: Power/Electrical Enclosure
Contains: LiFePO4 battery, charge controller, fuses/breakers, terminal blocks

**Enclosure Specifications:**
- Size: ~300mm x 250mm x 150mm (12" x 10" x 6") - varies by battery size
- Material: Polycarbonate or fiberglass, IP67 rated, UV stabilized
- Mounting: Wall/pole mount brackets
- Ventilation: GORE-TEX pressure vent (IP67 rated, allows pressure equalization)

**Cable Entry Points:**

| Entry | Cable/Connection | Gland Size | Type |
|-------|-----------------|------------|------|
| 1 | Solar Panel MC4+ | M20 | IP68 gland or MC4 pass-through |
| 2 | Solar Panel MC4- | M20 | IP68 gland or MC4 pass-through |
| 3 | DC Output to Compute Box | M20 | IP68 compression gland |
| 4 | Ground/Earth | M16 | IP68 compression gland |
| 5 | Spare | M16 | IP68 blanking plug |

#### Configuration A Wiring Diagram

```
                    ┌─────────────────────────────────────────┐
                    │           SOLAR PANEL (50-200W)         │
                    │              MC4+ ─┬─ MC4-              │
                    └───────────────────┼──┼──────────────────┘
                                        │  │
                    ┌───────────────────┼──┼──────────────────┐
                    │  POWER BOX        ▼  ▼                  │
                    │              [MC4 Entry Glands]         │
                    │                   │  │                  │
                    │              [Charge Controller]        │
                    │                   │                     │
                    │              [Fuse 20A]                 │
                    │                   │                     │
                    │         ┌────[LiFePO4 Battery]          │
                    │         │         │                     │
                    │         │    [Terminal Block]           │
                    │         │         │ (+12V, GND)         │
                    │     [Ground       │                     │
                    │      Lug]    [DC Out Gland]             │
                    └─────────┼─────────┼─────────────────────┘
                              │         │
                              │    2-wire DC cable (14 AWG)
                              │         │
                    ┌─────────┼─────────┼─────────────────────┐
                    │  COMPUTE BOX      │                     │
                    │              [DC In Gland]              │
                    │                   │                     │
                    │              [Fuse 5A]                  │
                    │                   │                     │
                    │         ┌────[5V/3A USB-C PD]           │
                    │         │         │                     │
                    │    [Ground   [Raspberry Pi 5]           │
                    │     Lug]          │                     │
                    │                   ├── USB ── [Gland] ── Camera 1
                    │                   ├── USB ── [Gland] ── Camera 2
                    │                   └── USB ── [4G Modem]
                    │                                   │
                    │                          [SMA Bulkhead]
                    │                               │
                    └───────────────────────────────┼─────────┘
                                                    │
                                              [Ext Antenna]
```

---

### Configuration B: Combined Electrical + Compute Box (Single-Box System)

**Use Case:** Simpler installation, fewer penetrations, lower cost, single mounting point.

**Enclosure Specifications:**
- Size: ~400mm x 300mm x 200mm (16" x 12" x 8") - varies by battery size
- Material: Fiberglass or polycarbonate, IP67 rated, UV stabilized
- Mounting: Heavy-duty pole/wall mount (heavier due to battery)
- Ventilation: GORE-TEX pressure vent (IP67 rated)
- Internal divider: Optional thermal barrier between battery and compute sections

**Cable Entry Points:**

| Entry | Cable/Connection | Gland Size | Type |
|-------|-----------------|------------|------|
| 1 | Solar Panel MC4+ | M20 | IP68 gland or MC4 pass-through |
| 2 | Solar Panel MC4- | M20 | IP68 gland or MC4 pass-through |
| 3 | USB Camera 1 | M16 | IP68 USB pass-through or gland |
| 4 | USB Camera 2 | M16 | IP68 USB pass-through or gland |
| 5 | Cellular Antenna (SMA) | M12 | IP67 SMA bulkhead connector |
| 6 | WiFi Antenna (if external) | M12 | IP67 SMA/RP-SMA bulkhead |
| 7 | Ground/Earth | M16 | IP68 compression gland |
| 8 | Spare/Sensor | M16 | IP68 blanking plug |

#### Configuration B Wiring Diagram

```
                    ┌─────────────────────────────────────────┐
                    │           SOLAR PANEL (50-200W)         │
                    │              MC4+ ─┬─ MC4-              │
                    └───────────────────┼──┼──────────────────┘
                                        │  │
┌───────────────────────────────────────┼──┼──────────────────────────────────┐
│  COMBINED BOX                         ▼  ▼                                  │
│                                  [MC4 Entry Glands]                         │
│                                       │  │                                  │
│   POWER SECTION                  [Charge Controller]      COMPUTE SECTION   │
│                                       │                                     │
│                                  [Fuse 20A]                                 │
│                                       │                                     │
│                             ┌────[LiFePO4 Battery]                          │
│                             │         │                                     │
│                             │    [Terminal Block] ──────► [5V USB-C PD]     │
│                             │                                    │          │
│                         [Ground                          [Raspberry Pi 5]   │
│                          Lug]                                    │          │
│                             │                    ┌───────────────┤          │
│                             │                    │               │          │
│                        [Gnd Gland]          [4G Modem]      USB  USB        │
│                             │                    │           │     │        │
│                             ▼               [SMA Bulkhead]   │     │        │
│                          TO GROUND               │       [Gland] [Gland]    │
│                                            [Antenna]         │       │      │
│                                                              ▼       ▼      │
│                        [GORE Vent]                       Camera1  Camera2   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Cable Gland & Connector Specifications

### Required IP68 Cable Glands

| Size | Thread | Cable OD Range | Typical Use |
|------|--------|----------------|-------------|
| M12 | M12x1.5 | 3-6mm | Antenna cables, sensor wires |
| M16 | M16x1.5 | 4-8mm | USB cables, small power cables |
| M20 | M20x1.5 | 6-12mm | DC power cables, solar cables |
| M25 | M25x1.5 | 9-16mm | Large cable bundles |

**Gland Features Required:**
- Nylon PA66 body (UV stabilized) or stainless steel
- Silicone or EPDM sealing insert
- IP68 rating when properly tightened
- Operating temperature: -40°C to +100°C
- Locknut included

### USB Pass-Through Options

**Option 1: IP68 USB Bulkhead Connectors**
- Panel-mount USB-A female to USB-A female
- Waterproof cap when not in use
- Maintains USB 2.0/3.0 speeds
- Examples: Bulgin 400 series, Switchcraft

**Option 2: USB Cable Through Gland**
- Standard USB cable passed through M16 gland
- Cable sheath provides seal surface
- Less expensive but cable is captive
- Must seal around cable jacket, not individual wires

**Option 3: Sealed USB Cable Assemblies**
- Pre-made cables with IP67/IP68 connectors on both ends
- Highest reliability
- Example: IP67 USB-A to USB-A extension cables

### Antenna Connections

**Cellular/WiFi Antennas:**
- SMA or RP-SMA bulkhead connectors, IP67 rated
- Mount antenna externally, connector passes through enclosure wall
- Use weatherproof antenna (IP67) on external side
- Apply silicone sealant around threads for extra protection

---

## Ant-Proofing Measures (CRITICAL)

### The Problem
Field experience in Indonesia shows ants will enter enclosures through incredibly small gaps. They are attracted to:
- Warmth from electronics
- Electrical fields (some ant species)
- Sheltered nesting sites

**Any gap larger than 0.5mm is an entry point.**

### Ant Prevention Strategy

#### 1. Seal All Penetrations
- Use IP68 cable glands with proper sealing inserts
- No gaps larger than 0.5mm anywhere
- Apply silicone sealant around all gland threads (belt and suspenders)
- Glands must be sized correctly for cable OD (not oversized)
- Tighten glands to manufacturer's torque spec

#### 2. Seal Enclosure Lid/Seams
- Verify gasket is intact and properly seated before each closure
- Apply thin bead of silicone around gasket channel if needed
- Use enclosures with tongue-and-groove sealing designs
- Check for gasket compression marks after closing

#### 3. Blanking Plugs for Unused Holes
- All unused knockouts/holes must have IP68 blanking plugs
- Never leave any opening unsealed, even temporarily

#### 4. Cable Entry Best Practices
- Fill any remaining gap in glands with dielectric grease
- Use glands with multiple sealing rings where possible
- Consider potting compound for permanent installations

#### 5. Chemical Barriers (Optional Additional Protection)
- Apply ant-repellent coating around enclosure base
- Dielectric grease in cable glands (also protects connections)
- Permethrin-treated tape around mounting pole (if allowed in deployment area)

#### 6. Physical Barriers
- Mount enclosure on metal pole (ants prefer to avoid smooth metal)
- Consider ant moat/barrier around mounting pole base
- Avoid mounting near vegetation or visible ant trails
- Keep vegetation trimmed away from installation

### Inspection Checklist
- [ ] All cable glands fully tightened (check monthly at first, then quarterly)
- [ ] No visible gaps around glands or enclosure seams
- [ ] Blanking plugs in all unused holes
- [ ] No ant trails leading toward enclosure
- [ ] Gasket clean and properly seated
- [ ] Silicone sealant intact around antenna bulkheads

---

## Pressure Equalization

### Why It's Needed
Sealed enclosures experience pressure differentials from:
- Temperature changes (day/night cycles can cause "breathing")
- Altitude changes during transport
- Weather system pressure changes

Without venting, seals can fail or moisture can be drawn in when pressure equalizes.

### Solution: GORE Protective Vents
- ePTFE membrane allows air/vapor exchange
- Blocks water, dust, and insects
- IP67/IP68 rated when installed
- Typical size: M12 thread
- Install at highest point of enclosure (heat rises)

**Installation Notes:**
- One vent per enclosure
- Position away from direct water spray
- Consider small rain shield/hood over vent
- Do not paint over or obstruct membrane

---

## Grounding & Lightning Protection

### All Enclosures Must Be Grounded
- Grounding lug inside enclosure, bonded to enclosure body
- Ground wire (green/yellow, 10 AWG minimum) exits via IP68 gland
- Connected to grounding rod at installation site (minimum 8ft copper rod)
- Protects against lightning-induced surges and static buildup

### Surge Protection
Install surge protectors on:
- Solar panel input (DC surge protector)
- DC output between boxes (if Configuration A)
- Antenna cables (coax surge protectors / lightning arrestors)

All surge protectors must be bonded to the same ground point.

---

## Bill of Materials: Enclosure Components

### Configuration A: Two-Box System

| Component | Quantity | Notes |
|-----------|----------|-------|
| Compute enclosure (IP67, ~200x150x100mm) | 1 | Polycarbonate, white/light gray |
| Power enclosure (IP67, ~300x250x150mm) | 1 | Fiberglass or PC, UV stabilized |
| M20 IP68 cable glands | 5 | Solar, DC power cables |
| M16 IP68 cable glands | 4 | USB cameras, ground |
| M12 IP67 SMA bulkhead | 2 | Cellular + WiFi antennas |
| M16 IP68 blanking plugs | 4 | Spares/unused holes |
| M12 GORE vent | 2 | One per box |
| DIN rail (35mm) | 2 | Internal mounting |
| Terminal blocks (10A) | 4 | DC distribution |
| Fuse holder + fuses (20A, 5A) | 2 sets | Overcurrent protection |
| Grounding lug | 2 | One per box |
| DC power cable (14 AWG, 2m, outdoor) | 1 | Inter-box connection |
| Silicone sealant (outdoor, clear) | 1 tube | Sealing threads |
| Dielectric grease | 1 tube | Gland and connector protection |

### Configuration B: Single Combined Box

| Component | Quantity | Notes |
|-----------|----------|-------|
| Combined enclosure (IP67, ~400x300x200mm) | 1 | Fiberglass, UV stabilized |
| M20 IP68 cable glands | 2 | Solar panel cables |
| M16 IP68 cable glands | 4 | USB cameras, ground |
| M12 IP67 SMA bulkhead | 2 | Cellular + WiFi antennas |
| M16 IP68 blanking plugs | 2 | Spares/unused holes |
| M12 GORE vent | 1 | Pressure equalization |
| DIN rail (35mm) | 2 | Internal mounting |
| Terminal blocks (10A) | 4 | DC distribution |
| Fuse holder + fuses (20A, 5A) | 2 sets | Overcurrent protection |
| Grounding lug | 1 | Earth connection |
| Silicone sealant (outdoor, clear) | 1 tube | Sealing |
| Dielectric grease | 1 tube | Protection |
| Internal divider (optional) | 1 | Thermal separation |

---

## Camera Mounting

### Sealed Camera Units (IP67/IP68)
- Cameras are factory-sealed, mounted externally to enclosure(s)
- USB cable runs from camera into enclosure through IP68 gland
- Camera mounting bracket should be adjustable for aiming
- Consider sun shade/hood to reduce lens heating and glare

### USB Cable Routing
- Use outdoor-rated USB cables with robust jacket
- Maximum length without active repeater: 5m
- For longer runs: Use active USB repeater cables (up to 30m) or USB-over-Ethernet
- Protect exposed cable with UV-resistant conduit or split loom

### Camera Positioning
- Mount cameras to see river cross-section
- Avoid pointing directly at sun path
- Consider vandalism/theft risk in camera placement
- Both cameras should have overlapping or complementary views

---

## Assembly Checklist

### Before Sealing Enclosure
- [ ] All internal wiring complete and tested
- [ ] All cable glands finger-tight in correct positions
- [ ] Blanking plugs in all unused holes
- [ ] GORE vent installed at highest point
- [ ] Ground lug connected to enclosure body
- [ ] Desiccant pack placed inside (optional, for initial moisture)
- [ ] All components secured (won't shift during transport)
- [ ] Photo taken of internal layout for documentation

### Sealing Procedure
1. Clean gasket and mating surfaces
2. Inspect gasket for damage, cracks, or debris
3. Apply thin silicone bead to cable gland threads (outside enclosure)
4. Tighten all cable glands to spec
5. Close enclosure, ensure gasket seats properly (no pinched wires)
6. Tighten lid fasteners in star pattern
7. Apply silicone around antenna bulkheads (optional extra seal)

### Post-Assembly Test
- [ ] Power on test - all systems functional
- [ ] Camera image quality check
- [ ] Cellular/WiFi connectivity test
- [ ] Water spray test (gentle hose, not pressure washer)
- [ ] Wait 10 minutes, check for any moisture ingress
- [ ] Visual inspection for gaps or unsealed areas
- [ ] Ant inspection after 24 hours in outdoor environment

---

## Supplier Research (Next Step)

The following components need supplier research and pricing:

### Cameras
1. IP67/IP68 sealed USB cameras with IR sensitivity (industrial/outdoor rated)
2. NoIR or IR-sensitive sealed cameras

### Enclosures & Sealing
3. IP67 polycarbonate/fiberglass enclosures (various sizes)
4. IP68 cable glands (M12, M16, M20, M25)
5. IP67 SMA bulkhead connectors
6. GORE protective vents (M12)
7. IP68 USB pass-through connectors or sealed cable assemblies
8. Outdoor-rated USB cables and active repeaters

### Power Management
9. Witty Pi 4 (or PiSugar 3 Plus) - RTC wake/shutdown controller
10. Quality 12V→5V DC-DC buck converter (5A, low ripple)
11. LiFePO4 batteries (20Ah, 50Ah, 100Ah 12V)
12. MPPT charge controllers (with USB output if possible)
13. 5A polyfuses
14. TVS diodes (5.5V)

### IR Spotlight System
15. 850nm IR flood lights (12V, 10-20W, IP65+)
16. 5V relay modules (10A contacts)
17. 1N4007 flyback diodes

### Electrical
18. Terminal blocks and DIN rail
19. Fuse holders and fuses (5A, 20A)
20. Surge protectors (DC and coax)
21. 18AWG outdoor-rated wire

### Anti-Theft System
22. Plunger tamper switches (N.C.) - e.g., SECO-LARM SS-073Q
23. Vibration/shock sensors (adjustable sensitivity)
24. Tilt sensors (optional, for high-risk sites)
25. 12V sirens (110-120dB, IP65+)
26. 12V strobe lights (or combo siren/strobe)
27. Alarm controller or latching relay module
28. Key switches for reset
29. Security screws and driver sets

### Consumables
30. Silicone sealant (outdoor/marine grade)
31. Dielectric grease
32. Cable labels
33. "Alarm Protected" warning signage

---

## References

- [Polycase IP67 Enclosures](https://www.polycase.com/ip67-enclosures)
- [TAKACHI Cable Glands](https://www.takachi-enclosure.com/cat/cable_glands)
- [Bulgin USB Connectors](https://www.bulgin.com/us/products/range/circular-data-connectors/400-series-usb.html)
- [GORE Protective Vents](https://www.gore.com/products/gore-protective-vents)
- [LUCID Vision Labs IP67 Cameras](https://thinklucid.com/ip67-cameras-and-accessories/)
