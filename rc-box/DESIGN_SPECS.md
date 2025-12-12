# RC-Box Design Specifications

**Document Status:** Authoritative Specification
**Version:** 1.1
**Last Updated:** 2024-12-03

This document defines the official specifications for the RC-Box river monitoring hardware platform. Use this as the reference when comparing parts and suppliers.

---

## Table of Contents

1. [Design Principles](#design-principles)
2. [System Overview](#system-overview)
3. [Camera Specifications](#camera-specifications)
4. [Camera Mount System](#camera-mount-system)
5. [Power System Specifications](#power-system-specifications)
6. [Power Management & Scheduling](#power-management--scheduling)
7. [IR Spotlight System](#ir-spotlight-system)
8. [Data Logger & Sensor Integration](#data-logger--sensor-integration)
9. [Enclosure Configurations](#enclosure-configurations)
10. [Cable Glands & Connectors](#cable-glands--connectors)
11. [Environmental Protection](#environmental-protection)
12. [Anti-Theft & Tamper Detection](#anti-theft--tamper-detection)
13. [Grounding & Surge Protection](#grounding--surge-protection)
14. [International Shipping & Customs](#international-shipping--customs)
15. [Stereo Camera System (Stretch Goal)](#stereo-camera-system-stretch-goal)
16. [Bill of Materials Summary](#bill-of-materials-summary)
17. [Supplier Evaluation Criteria](#supplier-evaluation-criteria)

---

## Design Principles

All component and design decisions must adhere to these core principles:

### Principle 1: Widely Available Components with Good Community Support

| Requirement | Specification |
|-------------|---------------|
| Supplier redundancy | Every critical component must have 2-3 alternative suppliers or compatible substitutes |
| Standards compliance | Prefer commodity standards: USB, 12V DC, screw terminals, M-series cable glands, 40-pin GPIO |
| Community support | Components must have active forums, documentation, and troubleshooting resources |
| Documentation | Datasheets, schematics, and repair guides must be publicly available |
| Global availability | Purchasable from Amazon, AliExpress, DigiKey, Mouser, or regional equivalents |
| Technology maturity | Proven technology with 1-2 years minimum market presence; avoid bleeding edge |

**Acceptable:**
- Raspberry Pi ecosystem components
- LiFePO4 batteries (commodity chemistry)
- Standard USB cameras and cables
- M-series cable glands (M12, M16, M20, M25)
- Common relay modules, fuses, terminal blocks

**Not Acceptable:**
- Custom PCBs without open-source designs
- Proprietary connectors or interfaces
- Single-source components
- Components requiring specialized programming tools

### Principle 2: Resilient in All Environments

| Environmental Challenge | Required Design Response |
|------------------------|--------------------------|
| Shipping damage | Foam-padded internals; secure mounting; no fragile components |
| Rough handling | Tool-free external operation; recessed switches; no exposed connectors during transport |
| Temperature extremes | Components rated -20°C to +50°C minimum |
| High humidity (tropics) | IP67 sealed enclosures; factory-sealed cameras; GORE vents; ant-proofing |
| Dust and sand | IP6x dust-tight rating on all enclosures and cameras |
| Rain and flooding | IP67 waterproof rating; elevated mounting; sealed cable entries |
| Power fluctuations | Surge protection on all inputs; quality DC-DC conversion; battery buffer |
| Vibration (pole sway) | Locking connectors; secure cable routing; no loose wires |
| UV exposure | UV-stabilized enclosure materials; shaded components where possible |
| Vandalism/theft | Security screws option; pole mounting; GPS tracking option |

**Design Rules:**
- All connections mechanically secured (screw terminals preferred over push-fit)
- All cables must have strain relief at entry points
- System must survive 1-meter drop when packaged
- System must survive complete power loss and restart cleanly
- Design for worst-case environment, not best-case

### Principle 3: Easily Field Serviceable

| Requirement | Specification |
|-------------|---------------|
| Modularity | Each function is a separate, replaceable module (camera, battery, Pi, modem, power controller) |
| No soldering | All connections via screw terminals, plugs, or headers |
| Common tools only | Phillips screwdriver, adjustable wrench, wire strippers - no specialized tools |
| Visual diagnostics | Status LEDs visible from ground level; display shows system status |
| Labeling | Every wire, connector, and component has printed/engraved labels |
| Documentation | Photos of correct assembly included inside each unit |
| Spare parts | Extra fuses, glands, terminals, connectors shipped with each deployment |
| Remote diagnostics | System reports health metrics; remote support can diagnose issues |
| Graceful degradation | Single component failure should not brick entire system |

**Design Rules:**
- Maximum 5 minutes to replace any component
- Every cable labeled at both ends
- Different connector types/colors for different functions (prevent mis-connection)
- QR codes linking to video repair guides
- All repair procedures tested with non-technical personnel before finalizing

**Serviceability Validation Checklist:**
- [ ] Can a non-technical person identify which component failed?
- [ ] Can they obtain a replacement locally or from shipped spares?
- [ ] Can they swap the component with only common tools?
- [ ] Can they verify the repair worked without special equipment?
- [ ] Is there printed documentation for this repair included in the unit?

### Principle 4: Shippable Worldwide

**Why this matters:** RC-Box units will be deployed to humanitarian operations globally. Components must clear customs without excessive delays, duties, or licensing requirements.

| Requirement | Implementation |
|-------------|----------------|
| No embargoed technology | Avoid military/dual-use components; no restricted encryption hardware |
| Battery compliance | LiFePO4 batteries require UN38.3 certification; consider local sourcing |
| Minimal customs friction | Use commodity electronics; avoid items needing import licenses |
| Clear documentation | Full commercial invoices; HS codes; country of origin marking |
| Modular shipping | Ship batteries/panels separately or source locally; components clear customs individually |
| No "tactical" marketing | Avoid products marketed for military/surveillance applications |

**Items to Source Locally (Not Ship Internationally):**
- LiFePO4 batteries (>100Wh requires dangerous goods handling)
- Solar panels (complex import duties, especially into US)
- Consider: Cellular modems (IMEI registration requirements vary by country)

**Acceptable for International Shipping:**
- Raspberry Pi and HATs (consumer electronics, trade compliance docs available)
- USB cameras (standard electronics)
- Enclosures, cable glands, connectors (commodity hardware)
- Cables, fuses, terminal blocks (no restrictions)

**See [International Shipping & Customs](#international-shipping--customs) section for detailed requirements.**

---

## System Overview

### Core Components

| Component | Quantity | Primary Function |
|-----------|----------|------------------|
| Raspberry Pi 5 | 1 | Main compute platform |
| Sealed IP67/IP68 cameras | 2 | Video capture (day and night) |
| LiFePO4 battery | 1 | Energy storage |
| Solar panel | 1 | Primary power generation |
| MPPT charge controller | 1 | Battery charging and management |
| Power management HAT | 1 | RTC wake/shutdown scheduling |
| 4G cellular modem | 1 | Data connectivity |
| IR spotlight | 1-2 | Night illumination |
| Weatherproof enclosure(s) | 1-2 | Environmental protection |

### Operating Parameters

| Parameter | Specification |
|-----------|---------------|
| Operating temperature | -20°C to +50°C |
| Storage temperature | -30°C to +60°C |
| Humidity | 0-100% RH (sealed enclosure) |
| IP rating | IP67 minimum (dust-tight, waterproof 1m/30min) |
| Power duty cycle | 2-3 minutes ON every 15 minutes |
| Data connectivity | 4G cellular primary, WiFi secondary |
| Local storage | Minimum 512GB (2+ weeks video buffer) |
| Design lifetime | 5+ years with field maintenance |

---

## Camera Specifications

### Primary Requirement: Factory-Sealed IP67/IP68 Cameras

| Specification | Requirement | Notes |
|---------------|-------------|-------|
| Quantity | 2 per station | Dual camera coverage |
| Sealing | IP67 minimum, IP68 preferred | Factory-sealed, not field-sealed |
| Connectivity | USB (preferred) or WiFi | Must work with Pi 5 |
| IR sensitivity | Required | NoIR or IR-capable sensor |
| Resolution | 1080p minimum | Higher acceptable |
| Frame rate | 30fps minimum | |
| Field of view | 60-90° | Suitable for river cross-section |
| Low-light performance | Required | For dawn/dusk operation |
| Operating temperature | -20°C to +50°C | |
| Mounting | Standard tripod thread (1/4"-20) preferred | Adjustable bracket compatible |

### Connectivity Options

| Connection Type | Max Distance | Requirements |
|-----------------|--------------|--------------|
| USB 2.0 native | 5m | Standard cable |
| USB 2.0 with active repeater | 30m | Active repeater cable |
| USB over Ethernet | 100m | USB extender adapters |
| WiFi | Site-dependent | IP camera with WiFi, P2P bridge for range |

### Fallback Option

If sealed cameras prove unsuitable, active dehumidification system required:
- GORE-TEX pressure vent
- Type 4A molecular sieve desiccant (100g per housing)
- 12V 5W lens heater with thermostat
- Anti-fog coating

---

## Camera Mount System

### Design Requirement: Fixed Stereo Geometry

Both cameras must be mounted on a **single rigid bracket** that maintains fixed geometric relationship. This is required for:
- Consistent video framing between cameras
- Future stereo survey capability (see [Stereo Camera System](#stereo-camera-system-stretch-goal))
- Simplified field setup (aim once, both cameras aligned)

**Cameras are NOT independently adjustable.** The entire mount assembly is aimed as a unit.

### Mount Specifications

| Specification | Requirement |
|---------------|-------------|
| Camera spacing (baseline) | 200-500mm (adjustable at manufacturing, fixed in field) |
| Camera alignment | Parallel optical axes, ±0.5° |
| Material | Powder-coated aluminum or stainless steel |
| Mounting interface | 1/4"-20 tripod thread per camera |
| Pole attachment | Adjustable clamp for 75-150mm (3-6") poles |
| Adjustment | Pan, tilt, rotation of entire assembly |
| Locking | Positive locking mechanism (no drift over time) |
| Cable routing | Integrated cable clips or channel |
| IP rating | Mounting hardware outdoor rated (stainless fasteners) |

### Mount Design Concept

```
        [Pole Clamp]
             │
        [Swivel Joint]
        (pan/tilt/lock)
             │
    ┌────────┴────────┐
    │   RIGID BAR     │
    │  (fixed length) │
    └────────┬────────┘
        ┌────┴────┐
        │         │
    [Cam 1]   [Cam 2]

    Both cameras point same direction
    Baseline is fixed after manufacturing
    Only the swivel joint is adjustable
```

### Baseline Selection

The camera baseline (spacing) affects stereo capability:

| Baseline | Best For | Trade-off |
|----------|----------|-----------|
| 200mm | Narrow rivers (<10m), close subjects | Lower depth precision at distance |
| 300mm | Medium rivers (10-20m) | Good balance |
| 500mm | Wide rivers (20-30m), distant subjects | Larger mount, harder to transport |

**Recommendation:** Standardize on 300mm baseline for general use. This provides reasonable stereo geometry for rivers up to 20m wide while keeping the mount compact.

### Reference Designs

Similar rigid stereo mounts used in:
- **StereoPi** - Raspberry Pi stereo camera projects
- **ZED stereo cameras** - Commercial stereo vision systems
- **Photogrammetry rigs** - Aerial survey camera mounts

### Sun Shade

The mount should include an integrated sun shade to:
- Reduce lens flare
- Minimize thermal stress on cameras
- Protect from direct rain

| Specification | Requirement |
|---------------|-------------|
| Coverage | Both cameras shaded |
| Material | Aluminum or UV-stable plastic |
| Color | Black (non-reflective) or white (heat rejection) |
| Design | Does not obstruct camera field of view |

### Bill of Materials: Camera Mount

| Component | Qty | Est. Cost | Notes |
|-----------|-----|-----------|-------|
| Rigid stereo bar (aluminum, 300mm) | 1 | $20-40 | Custom or off-shelf camera rail |
| 1/4"-20 camera mount screws | 2 | $2 | Stainless steel |
| Ball head or pan/tilt mount | 1 | $25-50 | Heavy-duty with locking |
| Pole clamp (75-150mm range) | 1 | $15-30 | Stainless or galvanized |
| Sun shade bracket | 1 | $10-20 | Aluminum |
| Cable clips | 4 | $2 | Adhesive or screw-mount |
| **Total** | | **$75-145** | |

---

## Power System Specifications

### Design Philosophy

**Overbuild by 50-100%.** Power system failure in remote locations is unacceptable. Size for rainy season/winter conditions, not optimal conditions.

### Battery Specifications

| Specification | Requirement |
|---------------|-------------|
| Chemistry | LiFePO4 only (no lead-acid) |
| Voltage | 12V nominal (4S configuration) |
| Cycle life | 2000+ cycles minimum |
| Depth of discharge | 90% usable |
| Operating temperature | -20°C to +60°C |
| Built-in BMS | Required |
| Certification | UL, CE, or equivalent |

### Tiered Configurations

| Tier | Solar Panel | Battery | Daily Generation | Backup Days | Use Case |
|------|-------------|---------|------------------|-------------|----------|
| **Low** | 50W | 20Ah LiFePO4 (256Wh) | 191Wh | 2.1 days | Budget deployments, good sun |
| **Mid** | 100W | 50Ah LiFePO4 (640Wh) | 428Wh | 3.6 days | Standard deployments |
| **High** | 200W | 100Ah LiFePO4 (1280Wh) | 864Wh | 4+ days | Remote/harsh environments |

### Solar Panel Specifications

| Specification | Requirement |
|---------------|-------------|
| Type | Monocrystalline (preferred) or polycrystalline |
| Voltage | 18V nominal (12V system compatible) |
| Connectors | MC4 standard |
| Frame | Aluminum, corrosion-resistant |
| IP rating | IP65 minimum |
| Temperature coefficient | -0.4%/°C or better |
| Warranty | 10+ years |

### Charge Controller Specifications

| Specification | Minimum | Preferred |
|---------------|---------|-----------|
| Type | PWM | MPPT |
| Efficiency | 85% | 95%+ |
| Current rating | Match panel (10-30A) | |
| Battery chemistry | LiFePO4 compatible | Programmable profiles |
| Temperature compensation | Required | |
| Load output | Optional | 5V USB output (3A+) |
| Display/monitoring | LED indicators | LCD or Bluetooth app |

### 5V Power Conditioning

| Specification | Minimum | Preferred |
|---------------|---------|-----------|
| Output voltage | 5.0-5.2V ±0.1V | 5.1V fixed |
| Output current | 3A continuous | 5A continuous |
| Efficiency | 85% | 90%+ |
| Input voltage range | 10-18V | 8-30V |
| Ripple/noise | <100mV p-p | <50mV p-p |
| Protections | OVP, OCP, short circuit | + reverse polarity, thermal |

**Required:** 5A polyfuse if powering Pi via GPIO header.

---

## Power Management & Scheduling

### Requirements

| Requirement | Specification |
|-------------|---------------|
| RTC accuracy | ±5ppm or better |
| Schedule capability | Complex ON/OFF sequences (e.g., 2-3 min every 15 min) |
| Wake source | RTC alarm |
| Input voltage | Compatible with 12V battery (5-26V range preferred) |
| Pi 5 compatibility | Confirmed required |
| GPIO output | Required for IR spotlight control |
| Software | Open-source, documented API |

### Recommended: Witty Pi 4

| Feature | Specification |
|---------|---------------|
| Compatibility | All 40-pin Pi models including Pi 5 |
| RTC accuracy | ±2ppm (factory calibrated, temperature compensated) |
| Input voltage | 5-26V DC |
| Schedule scripts | Supported |
| Software | Web interface (UWI), command line, open source |
| Price | ~$25-35 |
| Documentation | Extensive, English |

### Alternative: PiSugar 3 Plus

| Feature | Specification |
|---------|---------------|
| Compatibility | Pi Zero, 3, 4, 5 |
| Built-in battery | 5000mAh LiPo (UPS function) |
| RTC | Yes, scheduled wake |
| Input | 5V USB-C |
| Software | Web interface, Python API |
| Price | ~$40-50 |

---

## IR Spotlight System

### Purpose

Infrared illumination for night recording. Cameras must be IR-sensitive (NoIR type or equivalent).

### Design Philosophy: Commodity Parts Only

Per Principle 1, the IR control system must use **widely available, easily replaceable components**. The solution uses:
- Standard 5V USB relay module (triggered by Pi power state)
- Photoresistor relay module (automatic dusk/dawn sensing)
- No custom electronics, no specialized programming

This creates a two-stage control: spotlight only turns on when **both** the Pi is awake **and** it's dark outside.

### IR Spotlight Specifications

| Specification | Requirement |
|---------------|-------------|
| Wavelength | 850nm (preferred) or 940nm |
| Power | 20-30W |
| Voltage | 12V DC |
| Beam angle | 60-90° flood |
| Range | 50-80m (supports rivers up to 30m wide) |
| IP rating | IP65 minimum |
| Control | External (no built-in photosensor) |
| Mounting | Adjustable bracket |

**Wavelength Selection:**
- 850nm: Better range, faint red glow visible at LEDs - **recommended for river monitoring**
- 940nm: Invisible, 30-40% less range - only for covert applications

### Control System: Two-Stage Commodity Approach

The IR spotlight control uses two commodity modules in series:

#### Stage 1: USB Power Relay

A 5V relay module powered by Pi USB port. When Pi wakes up, USB provides power; relay closes. When Pi shuts down, USB power drops; relay opens.

| Component | Specification | Example Products |
|-----------|---------------|------------------|
| USB relay module | 5V coil, SPDT contacts, 10A+ rating | HiLetgo 5V relay module, Tolako 5V relay |
| Power source | Pi USB-A port (5V, 500mA available) | Any USB-A port |
| Wiring | USB → relay coil; relay contacts in 12V circuit | |

**Key Point:** No GPIO programming required. USB power presence = relay closed.

#### Stage 2: Photoresistor Light Sensor Relay

A 12V light-sensing relay module that only passes power when ambient light is below threshold (darkness).

| Component | Specification | Example Products |
|-----------|---------------|------------------|
| Photoresistor relay module | 12V input, adjustable light threshold, 10A contacts | XH-M131, HiLetgo light sensor relay |
| Light threshold | Adjustable potentiometer (set for dusk level) | |
| Sensor placement | External to enclosure, pointed at sky | Needs weatherproofing |

**Adjustment:** Turn potentiometer to set the light level at which relay activates. Test at dusk to calibrate.

### Control Circuit Wiring

```
                              [12V from Terminal Block]
                                        │
                                  [Fuse 5A]
                                        │
                    ┌───────────────────┴───────────────────┐
                    │                                       │
             [Stage 1: USB Relay]                   [Photoresistor
              Powered by Pi USB                      Module Power]
                    │                                       │
              [Relay Contacts]                    [Light Sensor Relay]
               (N.O. closes                        (closes when dark)
              when Pi is ON)                              │
                    │                                       │
                    └───────────┬───────────────────────────┘
                                │
                        [Both stages in series]
                                │
                         [IR Spotlight]
                                │
                              [GND]


    LOGIC TABLE:
    ┌─────────────┬───────────┬────────────────┐
    │ Pi Power    │ Daylight  │ IR Spotlight   │
    ├─────────────┼───────────┼────────────────┤
    │ OFF         │ Day       │ OFF            │
    │ OFF         │ Night     │ OFF            │
    │ ON          │ Day       │ OFF            │
    │ ON          │ Night     │ ON             │
    └─────────────┴───────────┴────────────────┘
```

### Detailed Wiring Diagram

```
[Pi 5 USB-A Port]
        │
        │ (USB cable, cut to expose 5V and GND wires)
        │
   ┌────┴────┐
   │  5V+    │───────────────► [5V Relay Module VCC]
   │  GND    │───────────────► [5V Relay Module GND]
   └─────────┘                         │
                                [Relay Coil]
                                       │
                               [Relay Contacts: COM, NO, NC]
                                       │
                                    (use NO - Normally Open)
                                       │
                              ┌────────┴────────┐
                              │                 │
                         [12V+ In]        [12V+ Out to
                    (from fused            Photoresistor
                     terminal block)        Module]
                                              │
                                     [Photoresistor Module]
                                     (12V light-sensing relay)
                                              │
                              ┌───────────────┴───────────────┐
                              │                               │
                     [Photoresistor                    [Relay Contacts]
                      (external sensor)]                      │
                                                    [12V+ Out to
                                                     IR Spotlight]
                                                              │
                                                       [IR Spotlight]
                                                         (12V)
                                                              │
                                                           [GND]
                                                    (common with battery)
```

### Photoresistor Sensor Placement

The light sensor must be positioned to detect ambient daylight:

| Requirement | Implementation |
|-------------|----------------|
| Location | Outside enclosure, pointed at sky (not at spotlight!) |
| Weatherproofing | Potted in clear epoxy, or inside small clear dome |
| Cable | 2-wire extension from module (can be 1-5m) |
| Mounting | On enclosure top, or on separate bracket facing up |
| Protection | Avoid direct sunlight on sensor (can cause false readings); north-facing ideal |

**Alternative:** Some photoresistor modules include the sensor on the PCB. These can be mounted inside an enclosure with a clear window, or use a separate weatherproof light sensor with cable.

### Component Specifications

#### USB 5V Relay Module

| Specification | Requirement |
|---------------|-------------|
| Coil voltage | 5V DC |
| Coil current | <100mA (must work with USB 500mA limit) |
| Contact rating | 10A @ 12V DC minimum |
| Contact type | SPDT (use N.O. contacts) |
| Size | Compact (~30x30mm typical) |
| Optoisolation | Optional but preferred |

**Example products:**
- HiLetgo 5V 1-channel relay module (~$2)
- Tolako 5V relay module (~$3)
- SunFounder 5V relay module (~$4)

#### Photoresistor Light Sensor Relay Module

| Specification | Requirement |
|---------------|-------------|
| Input voltage | 12V DC |
| Output | Relay contacts, 10A minimum |
| Light sensor | Photoresistor (LDR) with adjustable threshold |
| Threshold adjustment | Potentiometer on board |
| Mode | Configurable: output ON when dark (required) |
| Operating temperature | -20°C to +50°C |

**Example products:**
- XH-M131 12V Light Control Switch (~$3)
- HiLetgo 12V Photoresistor Relay Module (~$4)
- Geekcreit Light Sensor Switch Module (~$3)

**Note:** Some modules default to "ON when bright" - verify the module can be configured for "ON when dark" or has a mode switch.

### Power Budget

| Component | Power | Daily Energy (at 20% duty cycle, 50% at night) |
|-----------|-------|------------------------------------------------|
| 25W IR spotlight | 25W | 40-60 Wh (only runs when Pi ON + dark) |
| 5V relay coil | 0.3W | 0.5-1 Wh |
| Photoresistor module | 0.1W | 2.4 Wh (24h standby) |
| **Total** | 25.4W active | **43-64 Wh/day** |

*Already included in power system headroom calculations.*

### Bill of Materials: IR Spotlight Control

| Component | Qty | Est. Cost | Notes |
|-----------|-----|-----------|-------|
| 850nm IR flood light (12V, 20-30W, IP65) | 1-2 | $40-80 | One per camera, or single wide-angle |
| 5V USB relay module (10A contacts) | 1 | $2-4 | Powered by Pi USB |
| 12V photoresistor relay module (XH-M131 or equiv) | 1 | $3-5 | Light sensor, adjustable threshold |
| USB-A cable (for cutting) | 1 | $2 | Salvage 5V/GND wires |
| 1N4007 diode | 2 | $0.20 | Flyback protection (one per relay) |
| 18AWG wire (red/black) | 3m | $2 | 12V power runs |
| 5A inline fuse + holder | 1 | $3 | IR circuit protection |
| M16 IP68 cable gland | 1 | $3 | IR power cable entry |
| Weatherproof enclosure for photoresistor | 1 | $5 | Clear dome or potted sensor |
| **Total** | | **$60-105** | |

---

## Data Logger & Sensor Integration

### Purpose

RC-Box stations are often deployed alongside other hydrological instruments. This section specifies how to connect **commercial off-the-shelf sensors and data loggers** using standard interfaces.

### Design Philosophy

Per Principle 1 (Widely Available Components):
- **Use commercial sensors** - No custom sensor development; buy proven equipment
- **Standard interfaces only** - RS485/Modbus is the primary protocol
- **Commodity adapters** - USB-RS485 adapters available worldwide for ~$10-20
- **Time-series logging** - RC-Box logs sensor data locally; ORC software integration is a future project

**What RC-Box provides:**
- RS485/Modbus interface via USB adapter
- 12V power output for sensors (from main battery)
- Local time-series data storage
- Data available for future ORC software integration

**What RC-Box does NOT do (yet):**
- Process or analyze sensor data
- Display sensor data in ORC interface
- Trigger alerts based on sensor readings

---

### Standard Interface: RS485 / Modbus RTU

RS485/Modbus is the industry standard for environmental sensors. Most commercial rain gauges, weather stations, and water level sensors support this interface.

| Specification | Requirement |
|---------------|-------------|
| Physical layer | RS485 differential signaling |
| Protocol | Modbus RTU |
| Connector | Screw terminal block (A+, B-, GND, 12V+) |
| Adapter | USB-RS485 (commodity module) |

#### Interface Hardware

| Component | Specification | Example Products |
|-----------|---------------|------------------|
| USB-RS485 adapter | USB to RS485 converter | DSD TECH SH-U10, Waveshare USB-RS485 |
| Terminal block | 4-position screw terminal | Standard DIN rail mount |
| Termination resistor | 120Ω at end of bus | Built into many adapters |

#### Wiring

```
[RC-Box Enclosure]
        │
   [USB-RS485 Adapter] ──── [Pi USB Port]
        │
   [Terminal Block]
    A+ B- GND 12V+
     │  │   │   │
     │  │   │   └──── [From 12V terminal block]
     │  │   │
[4-wire shielded cable to sensor(s)]
     │  │   │
     A+ B- GND ─────── [Commercial Sensor]
```

---

### Supported Commercial Equipment

Any Modbus RTU sensor can be connected. Common categories:

#### Rain Gauges

| Type | Output | Example Products |
|------|--------|------------------|
| Tipping bucket with Modbus | RS485 | Texas Electronics TR-525M, Onset RG3-M |
| Tipping bucket (pulse) | Contact closure | Many manufacturers (requires pulse counter) |

#### Weather Stations

| Type | Output | Example Products |
|------|--------|------------------|
| Compact all-in-one | RS485/Modbus | Lufft WS-series, Gill MaxiMet |
| Modular stations | RS485/Modbus | Davis Vantage Pro2 (with adapter), Campbell Scientific |

#### Water Level Sensors

| Type | Output | Example Products |
|------|--------|------------------|
| Pressure transducer | RS485/Modbus | In-Situ Level TROLL, Keller Series 36 |
| Ultrasonic | RS485/Modbus | Senix ToughSonic |

---

### Data Logging

RC-Box logs all sensor readings locally as time-series data.

| Specification | Requirement |
|---------------|-------------|
| Storage format | CSV or JSON files |
| Timestamp | ISO 8601 UTC |
| Storage location | Local SSD alongside video data |
| Retention | Same as video data retention policy |

**Future integration:** Logged sensor data will be accessible to ORC software for display and analysis. This integration is a separate project.

---

### Power Budget

| Component | Power | Notes |
|-----------|-------|-------|
| USB-RS485 adapter | 0.2W | From Pi USB |
| Typical Modbus sensor | 0.1-0.5W | When polled |
| Weather station | 0.5-2W | Continuous |
| **Total sensor system** | **1-3W** | Add to power budget |

---

### Cable Entry Points

Add sensor cable entry to enclosure:

| Entry | Cable/Connection | Gland Size | Type |
|-------|-----------------|------------|------|
| Sensor RS485 | 4-wire shielded (A+, B-, GND, 12V+) | M16 or M20 | IP68 compression |

---

### Bill of Materials: Sensor Interface

| Component | Qty | Est. Cost | Notes |
|-----------|-----|-----------|-------|
| USB-RS485 adapter | 1 | $10-20 | DSD TECH or Waveshare |
| 4-position screw terminal block | 1 | $2 | For sensor connection |
| 120Ω termination resistor | 1 | $0.50 | End of RS485 bus |
| 4-wire shielded cable | varies | $1/m | Belden 9842 or equivalent |
| M16 IP68 cable gland | 1 | $3 | Sensor cable entry |
| **Interface total** | | **$20-30** | Sensors purchased separately |

**Note:** Sensors are purchased separately based on site requirements. RC-Box provides the standard interface; sensor selection is a deployment decision.

---

## Enclosure Configurations

Two configurations supported:

### Configuration A: Separate Boxes (Two-Box System)

**Use when:** Thermal separation needed, flexible positioning, easier servicing of individual components.

#### Box 1: Compute Enclosure

| Specification | Requirement |
|---------------|-------------|
| Contents | Pi 5, power management HAT, 4G modem, USB hub |
| Size | ~200mm x 150mm x 100mm (8" x 6" x 4") |
| Material | Polycarbonate or ABS |
| IP rating | IP67 |
| Color | White or light gray (heat reflection) |
| Mounting | Wall/pole brackets |

**Cable Entry Points:**

| Entry | Connection | Gland Size | Type |
|-------|------------|------------|------|
| 1 | DC Power In (12V) | M20 | IP68 compression |
| 2 | USB Camera 1 | M16 | IP68 USB pass-through or gland |
| 3 | USB Camera 2 | M16 | IP68 USB pass-through or gland |
| 4 | Cellular Antenna | M12 | IP67 SMA bulkhead |
| 5 | WiFi Antenna | M12 | IP67 RP-SMA bulkhead |
| 6 | Spare | M16 | IP68 blanking plug |

#### Box 2: Power/Electrical Enclosure

| Specification | Requirement |
|---------------|-------------|
| Contents | LiFePO4 battery, charge controller, fuses, terminal blocks |
| Size | ~300mm x 250mm x 150mm (12" x 10" x 6") - varies by battery |
| Material | Polycarbonate or fiberglass, UV stabilized |
| IP rating | IP67 |
| Ventilation | GORE-TEX pressure vent (M12) |
| Mounting | Wall/pole brackets |

**Cable Entry Points:**

| Entry | Connection | Gland Size | Type |
|-------|------------|------------|------|
| 1 | Solar Panel MC4+ | M20 | IP68 gland or MC4 pass-through |
| 2 | Solar Panel MC4- | M20 | IP68 gland or MC4 pass-through |
| 3 | DC Output to Compute Box | M20 | IP68 compression |
| 4 | IR Spotlight Power | M16 | IP68 compression |
| 5 | Ground/Earth | M16 | IP68 compression |
| 6 | Spare | M16 | IP68 blanking plug |

### Configuration B: Combined Box (Single-Box System)

**Use when:** Simpler installation, fewer cable runs, single mounting point.

| Specification | Requirement |
|---------------|-------------|
| Contents | All components except cameras and solar panel |
| Size | ~400mm x 300mm x 200mm (16" x 12" x 8") |
| Material | Fiberglass or polycarbonate, UV stabilized |
| IP rating | IP67 |
| Ventilation | GORE-TEX pressure vent (M12) |
| Internal divider | Optional thermal barrier between battery and compute |
| Mounting | Heavy-duty pole/wall brackets |

**Cable Entry Points:**

| Entry | Connection | Gland Size | Type |
|-------|------------|------------|------|
| 1 | Solar Panel MC4+ | M20 | IP68 gland |
| 2 | Solar Panel MC4- | M20 | IP68 gland |
| 3 | USB Camera 1 | M16 | IP68 USB gland |
| 4 | USB Camera 2 | M16 | IP68 USB gland |
| 5 | Cellular Antenna | M12 | IP67 SMA bulkhead |
| 6 | WiFi Antenna | M12 | IP67 RP-SMA bulkhead |
| 7 | Ground/Earth | M16 | IP68 compression |
| 8 | IR Spotlight Power | M16 | IP68 compression |
| 9 | Spare | M16 | IP68 blanking plug |

---

## Cable Glands & Connectors

### Cable Gland Specifications

| Size | Thread | Cable OD Range | Use |
|------|--------|----------------|-----|
| M12 | M12x1.5 | 3-6mm | Antenna cables, sensor wires |
| M16 | M16x1.5 | 4-8mm | USB cables, small power cables |
| M20 | M20x1.5 | 6-12mm | DC power cables, solar cables |
| M25 | M25x1.5 | 9-16mm | Large cable bundles |

### Gland Requirements

| Specification | Requirement |
|---------------|-------------|
| IP rating | IP68 |
| Material | Nylon PA66 (UV stabilized) or stainless steel |
| Sealing | Silicone or EPDM insert |
| Temperature range | -40°C to +100°C |
| Locknut | Included |

### USB Pass-Through Options

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| IP68 USB bulkhead | Panel-mount USB-A F/F | Clean, disconnectable | Higher cost |
| USB cable through gland | Standard cable through M16 gland | Low cost | Cable captive |
| Sealed USB assemblies | Pre-made IP67 cables | Highest reliability | Limited lengths |

### Antenna Connections

| Specification | Requirement |
|---------------|-------------|
| Connector type | SMA or RP-SMA bulkhead |
| IP rating | IP67 minimum |
| Material | Brass, nickel-plated |
| Sealing | Apply silicone sealant around threads |

---

## Environmental Protection

### Ant-Proofing (Critical)

Field experience confirms ants will enter enclosures through any gap >0.5mm.

| Measure | Requirement |
|---------|-------------|
| Maximum gap size | 0.5mm at any penetration |
| Cable glands | Correctly sized for cable OD; tightened to spec |
| Thread sealant | Silicone sealant on all gland threads |
| Unused holes | IP68 blanking plugs in all unused knockouts |
| Gland fill | Dielectric grease in remaining gaps |
| Lid gasket | Inspect for damage; verify proper seating |

**Optional Additional Measures:**
- Ant-repellent coating around enclosure base
- Permethrin-treated tape on mounting pole
- Dielectric grease on all connections
- Mount on smooth metal pole

### Pressure Equalization

| Specification | Requirement |
|---------------|-------------|
| Vent type | GORE-TEX or equivalent ePTFE membrane |
| Thread size | M12 |
| IP rating | IP67/IP68 when installed |
| Location | Highest point of enclosure |
| Protection | Rain shield/hood recommended |
| Quantity | One per enclosure |

### Moisture Management

| Measure | Specification |
|---------|---------------|
| Primary | Factory-sealed IP67/IP68 cameras (no internal moisture source) |
| Secondary | GORE vent for pressure equalization |
| Tertiary | Desiccant pack inside enclosure (optional, for initial assembly moisture) |

---

## Anti-Theft & Tamper Detection

### Design Philosophy

Remote monitoring equipment is vulnerable to theft and tampering. The goal is **deterrence and notification**, not physical prevention (which is impractical for pole-mounted equipment). A loud alarm draws attention and makes theft uncomfortable.

### Recommended: Screamer Alarm System

A "screamer" is a loud siren (100-120dB) triggered by tamper detection. At 120dB, it's painful to be near and audible from hundreds of meters away.

#### Components Required

| Component | Specification | Purpose |
|-----------|---------------|---------|
| Tamper switch | Plunger-type, N.C. (normally closed) | Detects enclosure opening |
| Vibration/shock sensor | Adjustable sensitivity | Detects prying, cutting, impacts |
| Tilt sensor | >5° threshold | Detects pole removal or severe tilting |
| 12V siren | 110-120dB, weatherproof | Audible deterrent |
| Strobe light | 12V, high-visibility | Visual deterrent, locating aid |
| Alarm controller | 12V, latching with remote reset | Manages sensors, triggers siren |

#### Tamper Switch Specifications

| Specification | Requirement |
|---------------|-------------|
| Type | Plunger/microswitch, normally closed (N.C.) |
| Activation | Opens circuit when lid/door opened |
| Contacts | Silver-plated for reliability |
| Mounting | Screw-mount inside enclosure lid area |
| Example | [SECO-LARM SS-073Q](https://www.seco-larm.com/product/ss-073q/), GRI TSC-20 |

#### Vibration/Shock Sensor Specifications

| Specification | Requirement |
|---------------|-------------|
| Sensitivity | Adjustable (to avoid false alarms from wind/weather) |
| Output | N.C. contact or digital signal |
| Power | 12V DC |
| Weatherproof | Required if mounted externally |
| Example | [YoLink Vibration Sensor](https://shop.yosmart.com/products/ys7201) or similar |

#### Tilt Sensor Specifications

| Specification | Requirement |
|---------------|-------------|
| Threshold | 5-15° adjustable |
| Output | N.C. contact |
| Power | 12V DC or battery |
| Purpose | Detect pole being cut down or unit being forcibly removed |

#### Siren/Strobe Specifications

| Specification | Requirement |
|---------------|-------------|
| Sound level | 110dB minimum, 120dB preferred |
| Voltage | 12V DC (powered from main battery) |
| Current draw | <500mA |
| IP rating | IP65 minimum (outdoor rated) |
| Strobe | Integrated or separate, high-visibility |
| Tamper protection | Anti-tamper switch on siren enclosure |
| Example | [12V Industrial Siren 120dB](https://www.amazon.com/Wireless-Industrial-Security-Waterproof-Emergency/dp/B0863F92K4) |

### Wiring Diagram

```
                    [12V from Terminal Block]
                            │
                      [Fuse 2A]
                            │
                    [Alarm Controller]
                      │    │    │
          ┌───────────┤    │    ├───────────┐
          │           │    │    │           │
    [Tamper SW]  [Vibration] [Tilt]    [Siren + Strobe]
     (N.C.)       (N.C.)    (N.C.)         │
          │           │    │    │           │
          └───────────┴────┴────┴───────────┘
                            │
                         [GND]
```

**N.C. (Normally Closed) Logic:**
- All sensors wired in series
- Any sensor opening the circuit triggers alarm
- Cutting wires also triggers alarm (fail-secure)

### Alarm Controller Options

#### Option 1: Simple Relay-Based (DIY)

| Component | Purpose |
|-----------|---------|
| 12V latching relay | Holds alarm ON until manually reset |
| N.C. sensor chain | Series-wired tamper, vibration, tilt sensors |
| Reset switch | Key switch or hidden button for authorized reset |

**Pros:** Simple, low cost, no programming
**Cons:** No remote notification, must physically reset

#### Option 2: Smart Alarm Module

| Feature | Requirement |
|---------|-------------|
| Inputs | 2-4 N.C. zones |
| Outputs | Siren, strobe |
| Power | 12V DC |
| Notification | Optional: cellular/WiFi alert |
| Remote arm/disarm | Optional: via app or SMS |

**Pros:** Remote notification, remote reset, configurable
**Cons:** More complex, requires connectivity

#### Option 3: Integration with Pi (Software-Based)

Use Pi GPIO to monitor sensors and control siren:

```python
import RPi.GPIO as GPIO
import time

TAMPER_PIN = 27      # N.C. tamper switch
VIBRATION_PIN = 22   # N.C. vibration sensor
SIREN_PIN = 17       # Relay to siren

GPIO.setmode(GPIO.BCM)
GPIO.setup(TAMPER_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(VIBRATION_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SIREN_PIN, GPIO.OUT)

def check_tamper():
    if GPIO.input(TAMPER_PIN) == GPIO.HIGH:  # N.C. opened
        return True
    if GPIO.input(VIBRATION_PIN) == GPIO.HIGH:
        return True
    return False

def trigger_alarm():
    GPIO.output(SIREN_PIN, GPIO.HIGH)
    # Send notification via cellular...
    # Log event...

# In main monitoring loop
while True:
    if check_tamper():
        trigger_alarm()
    time.sleep(0.1)
```

**Pros:** Integrated with system, can send alerts via existing cellular connection
**Cons:** Only works when Pi is awake; requires backup for when Pi is sleeping

### Recommended Configuration

For RC-Box, use **hybrid approach**:

1. **Hardware alarm controller** (Option 1 or 2) that works independently of Pi
2. **Pi monitors alarm state** when awake and can send notifications
3. **Siren sounds immediately** on tamper, regardless of Pi state

### Physical Security Measures

In addition to electronic alarm:

| Measure | Implementation |
|---------|----------------|
| Security screws | Torx or hex security screws for enclosure and mounts |
| Locking enclosure | Padlock hasp or key lock on enclosure |
| Cable locks | Steel cable through mounting brackets |
| Height | Mount high enough to require ladder |
| Signage | "Alarm Protected" warning signs |
| Marking | Engrave or etch ID number on all components |

### Power Budget for Anti-Theft System

| Component | Standby | Active | Notes |
|-----------|---------|--------|-------|
| Tamper switch | 0W | 0W | Passive, no power |
| Vibration sensor | 0.01W | 0.01W | Minimal |
| Tilt sensor | 0W | 0W | Often passive |
| Alarm controller | 0.1W | 0.1W | Standby monitoring |
| Siren (during alarm) | 0W | 6W | Only when triggered |
| **Total standby** | **~0.1W** | | Negligible impact on power budget |

### Bill of Materials: Anti-Theft System

| Component | Qty | Notes |
|-----------|-----|-------|
| Plunger tamper switch (N.C.) | 1-2 | One per enclosure |
| Vibration/shock sensor | 1 | Adjustable sensitivity |
| Tilt sensor (optional) | 1 | For high-risk locations |
| 12V siren (110-120dB) | 1 | Outdoor rated, IP65+ |
| 12V strobe light | 1 | Or combo siren/strobe unit |
| Alarm controller or relay module | 1 | 12V, latching preferred |
| Key switch or reset button | 1 | For authorized reset |
| 22AWG wire | 5m | Sensor wiring |
| 2A fuse + holder | 1 | Siren circuit protection |
| "Alarm Protected" signage | 2 | Deterrent |
| Security screws + driver | 1 set | Torx or hex security |

---

## Grounding & Surge Protection

### Grounding Requirements

| Specification | Requirement |
|---------------|-------------|
| Ground lug | One per enclosure, bonded to enclosure body |
| Ground wire | Green/yellow, 10 AWG minimum |
| Ground rod | 8ft copper rod at installation site |
| Exit gland | M16 IP68 compression gland |

### Surge Protection

| Location | Protection Type |
|----------|-----------------|
| Solar panel input | DC surge protector (MOV or TVS based) |
| Inter-box DC cable | DC surge protector (if Configuration A) |
| Antenna cables | Coax surge protector / lightning arrestor |
| 5V to Pi | TVS diode (5.5V clamp) |

All surge protectors must be bonded to common ground point.

---

## International Shipping & Customs

### Design Philosophy

RC-Box units will be shipped worldwide to humanitarian deployments. Component selection must avoid:
- Items commonly embargoed or restricted
- Components that trigger lengthy customs inspections
- Technologies requiring special export licenses
- Items with complex import duties or quotas

### Principle 4: Shippable Worldwide

| Requirement | Implementation |
|-------------|----------------|
| Avoid embargoed technology | No military/dual-use components; no restricted encryption hardware |
| Battery compliance | LiFePO4 ≤100Wh per battery; proper UN38.3 certification |
| Minimal customs friction | Use commodity electronics; avoid items requiring import licenses |
| Clear documentation | Full commercial invoices; HS codes; country of origin marking |
| Modular shipping | Ship batteries separately if needed; components can clear customs individually |

---

### Lithium Battery Shipping (Critical)

LiFePO4 batteries are classified as **UN3481** (lithium-ion batteries packed with equipment) under [IATA Dangerous Goods Regulations](https://www.iata.org/en/programs/cargo/dgr/lithium-batteries/).

#### Watt-Hour Limits

| Battery Size | Watt-Hours | Air Shipping Status |
|--------------|------------|---------------------|
| 20Ah × 12V | 256Wh | **Requires DG declaration** (>100Wh) |
| 50Ah × 12V | 640Wh | **Requires DG declaration** (>100Wh) |
| 100Ah × 12V | 1280Wh | **Requires DG declaration** (>100Wh) |

**All RC-Box batteries exceed 100Wh and require:**
- UN38.3 test certification (must be provided by battery manufacturer)
- Dangerous Goods Declaration (DGD) for air freight
- Class 9 hazard label + lithium battery handling mark
- State of charge ≤30% for air cargo
- Maximum 5kg of batteries per package
- Trained shipper certification (renewed every 2 years)

#### Shipping Recommendations

| Method | Recommendation |
|--------|----------------|
| **Air freight** | Use DG-certified freight forwarder; expensive but fast |
| **Sea freight** | Fewer restrictions; preferred for bulk shipments |
| **Ship separately** | Battery ships via sea; electronics ship via air |
| **Source locally** | Purchase LiFePO4 batteries in-country where possible |

**Design Consideration:** Consider specifying batteries that are commonly available in destination countries to avoid shipping batteries internationally altogether.

---

### Solar Panel Considerations

Solar panels have complex import duties in some countries, particularly the United States.

| Issue | Details |
|-------|---------|
| US Section 201 tariffs | 14.5%+ on crystalline silicon panels from many countries |
| AD/CVD duties | Can exceed 200% on panels from China, Vietnam, Malaysia, Thailand, Cambodia |
| UFLPA restrictions | Panels with Xinjiang supply chain connections blocked from US import |
| EU duties | Currently 0% on most solar panels |

#### Recommendations

| Recommendation | Rationale |
|----------------|-----------|
| **Source panels locally** | Avoid import duties; support local economy |
| **Specify generic requirements** | Don't lock into specific brands that may have supply chain issues |
| **Consider bifacial panels** | Exempt from some US tariffs |
| **Document supply chain** | May be required for customs clearance |

**Design Consideration:** Solar panels are bulky and have complex duties. Specify wattage and electrical requirements only; source panels in destination country or region.

---

### Cellular Modem Considerations

Cellular modems with 4G/LTE capability may face:
- IMEI registration requirements in destination country
- Radio frequency certification requirements
- Import license requirements (especially in Southeast Asia)

#### Countries with IMEI Registration

| Country | Requirement | Grace Period |
|---------|-------------|--------------|
| Turkey | Registration required; substantial fee | 120 days |
| Indonesia | Customs declaration required | 90 days |
| Pakistan | DIRBS registration; duties may apply | 120 days |
| Chile | SUBTEL registration required | 30 days |
| Uzbekistan | UZIMEI registration required | Varies |

#### Recommendations

| Recommendation | Rationale |
|----------------|-----------|
| **Use global-band modems** | Works on more networks worldwide |
| **Document IMEI numbers** | Required for registration in many countries |
| **Budget for registration fees** | Some countries charge substantial fees |
| **Consider local SIM strategy** | Local operator may assist with registration |
| **Malaysia/Singapore: Import license needed** | For any WiFi/Bluetooth/cellular device |

---

### Raspberry Pi and Electronics

Raspberry Pi and similar single-board computers are generally **low-risk for customs** because:
- Consumer electronics, widely available
- No restricted encryption hardware (general-purpose computing exemption)
- Excluded from Wassenaar Arrangement controls for retail products
- [Raspberry Pi provides trade compliance documentation](https://pip.raspberrypi.com/categories/604-international-trade-compliance)

#### Countries with General Electronics Restrictions

| Country | Issue |
|---------|-------|
| North Korea | Total embargo (US, UK, EU, UN) |
| Iran | Significant restrictions (US) |
| Cuba | Significant restrictions (US) |
| Syria | Significant restrictions (US) |
| Russia/Belarus | Significant restrictions (US, EU) - since 2022 |
| Crimea/Donetsk/Luhansk | Significant restrictions (US, EU) |

**These countries are unlikely humanitarian deployment targets, but verify before shipping.**

---

### Recommended Shipping Strategy

#### Option A: Full Kit Shipping (Preferred for Small Quantities)

Ship complete assembled units via freight forwarder experienced with:
- Dangerous goods (for batteries)
- Electronics
- Destination country customs

| Component | Shipping Method |
|-----------|-----------------|
| Assembled unit (no battery) | Air freight |
| LiFePO4 battery | Sea freight or local purchase |
| Solar panel | Local purchase in-country |
| Cellular modem | Included; document IMEI |

#### Option B: Component Shipping (For Larger Deployments)

Ship components separately; assemble in-country:

| Component | Shipping Method | Notes |
|-----------|-----------------|-------|
| Pi, HATs, electronics | Air freight | Low customs risk |
| Cameras, cables, glands | Air freight | Low customs risk |
| Enclosures | Air or sea | Bulky but no restrictions |
| Batteries | Local purchase | Avoid shipping entirely |
| Solar panels | Local purchase | Avoid duties |
| Cellular modems | Air freight | Document IMEIs |

#### Option C: Regional Hubs

Establish regional inventory hubs in customs-friendly locations:
- Singapore (Asia-Pacific)
- Dubai (Middle East/Africa)
- Panama (Americas)

Pre-position components; ship short distances to final destinations.

---

### Documentation Checklist

Every international shipment must include:

- [ ] Commercial invoice with:
  - [ ] Itemized list of all components
  - [ ] HS codes for each item category
  - [ ] Declared values (cannot be $0)
  - [ ] Country of origin for each item
  - [ ] IMEI numbers for cellular devices
- [ ] Packing list with weights and dimensions
- [ ] Battery documentation:
  - [ ] UN38.3 test summary (from manufacturer)
  - [ ] MSDS/SDS (Material Safety Data Sheet)
  - [ ] Dangerous Goods Declaration (if air freight)
- [ ] Shipper's declaration (if DG)
- [ ] Import license (if required by destination country)
- [ ] End-use statement (for some countries)

---

### Component Selection: Shipping-Friendly Choices

| Component | Preferred Choice | Avoid |
|-----------|------------------|-------|
| Battery | Locally-sourced LiFePO4 | Shipping large batteries internationally |
| Solar panel | Locally-sourced | Importing to US (duties); China-origin to US |
| Compute | Raspberry Pi 5 | Custom boards; FPGAs; encryption hardware |
| Modem | Global-band 4G with documented IMEI | Locked/carrier-specific modems |
| Camera | Standard USB; no night vision marketed as "surveillance" | Military-spec thermal cameras |
| Enclosure | Commodity NEMA/IP67 boxes | Custom fabrication |
| IR spotlight | Standard security lighting | "Covert" or "tactical" marketing |

---

### HS Codes Reference

Common HS codes for RC-Box components (verify with customs broker):

| Component | HS Code | Description |
|-----------|---------|-------------|
| Raspberry Pi | 8471.50 | Digital processing units |
| USB camera | 8525.80 | Television cameras, digital cameras |
| LiFePO4 battery | 8507.60 | Lithium-ion accumulators |
| Solar panel | 8541.40 | Photosensitive semiconductor devices |
| Charge controller | 8504.40 | Static converters |
| Cellular modem | 8517.12 | Telephones for cellular networks |
| Plastic enclosure | 3926.90 | Other articles of plastics |
| Cable glands | 8536.90 | Electrical apparatus for connections |

---

## Stereo Camera System (Stretch Goal)

### Purpose

The two-camera RC-Box configuration can potentially be used as a stereo vision system to **improve the survey process only**. This does not replace or modify the LSPIV flow measurement approach - ORC's core velocity measurement will continue to use the existing single-camera LSPIV method.

**Stereo capability is specifically for:**
1. **Survey assistance** - Help derive cross-section geometry and GCP positions
2. **Survey validation** - Cross-check manual survey measurements for errors
3. **Survey simplification** - Reduce the number of manual measurements required during site setup

**Stereo capability is NOT for:**
- Replacing LSPIV velocity measurement
- Real-time 3D flow analysis
- Changing how ORC processes video for discharge calculation

**Status:** STRETCH GOAL - Experimental capability for survey process improvement research.

### Technical Requirements for Stereo Vision

Stereo photogrammetry requires precise synchronization between cameras to capture the same moment in time.

| Requirement | Specification | Why It Matters |
|-------------|---------------|----------------|
| Shutter synchronization | <1ms difference | Moving water surface must be captured at same instant |
| Known baseline | ±1mm accuracy | Distance between cameras affects depth calculation |
| Known orientation | ±0.1° accuracy | Camera angles must be precisely calibrated |
| Overlapping field of view | 60-80% overlap | Stereo matching requires common features |
| Consistent exposure | Same settings both cameras | Brightness differences complicate matching |

### Synchronization Approaches

#### Option 1: Hardware-Synchronized Camera Modules (Recommended if Available)

Some camera modules expose hardware sync signals that allow frame-accurate synchronization.

| Camera Type | Sync Capability | Notes |
|-------------|-----------------|-------|
| Arducam Stereo Camera HAT | Hardware sync, 2x cameras | Designed for stereo; requires Pi Camera ports |
| Sony IMX477 (HQ Camera) | XVS/XHS sync pins exposed | Can be synchronized with external trigger |
| Sony IMX296 (Global Shutter) | XVS sync pin | Global shutter eliminates rolling shutter artifacts |
| Sony IMX708 (Pi Camera V3) | No external sync | NOT suitable for stereo without modification |

**Arducam Solutions:**
- [Arducam 12MP Synchronized Stereo Camera](https://www.arducam.com/product/arducam-12mp-synchronized-stereo-camera-bundle-kit-for-raspberry-pi/) - IMX477 based
- [Arducam Global Shutter Stereo](https://www.arducam.com/product/arducam-1mp-global-shutter-synchronized-stereo-camera-bundle-kit-for-raspberry-pi/) - IMX296 based

**Connection:** Requires MIPI CSI interface, NOT USB. Would require different camera approach than main RC-Box design.

#### Option 2: Software Synchronization with USB Cameras

USB cameras can be triggered as close as possible in software, but true synchronization is limited.

| Approach | Synchronization Accuracy | Feasibility |
|----------|--------------------------|-------------|
| Sequential capture | 50-100ms typical | Water movement visible between frames |
| Threaded capture | 10-50ms typical | Better but still visible motion |
| V4L2 multi-open | 5-20ms | Depends on USB bandwidth |
| External trigger (if supported) | <1ms | Requires specific camera models |

**Conclusion:** Software synchronization with standard USB cameras is likely **inadequate** for moving water stereo imaging.

#### Option 3: High-Speed Burst with Interpolation

Capture high-frame-rate video from both cameras and select the closest matching frames.

| Parameter | Requirement |
|-----------|-------------|
| Frame rate | 60fps or higher per camera |
| Maximum sync error | 1/60s = 16ms at 60fps |
| USB bandwidth | ~24 Mbps per camera at 1080p60 |

**Feasibility:** May work for slow-moving water, but reduces effective resolution and increases processing complexity.

### Survey Process Improvement Potential

If stereo vision is achieved, it could assist the survey process in several ways. **Note:** This is about improving site setup and calibration, not changing how ORC measures flow.

#### Current Survey Requirements

1. Ground Control Points (GCPs) - minimum 6 visible in camera view
2. GCP survey with RTK GPS or total station (sub-cm accuracy)
3. Cross-section survey at water level
4. Manual entry of survey data into ORC software

#### How Stereo Could Help

| Survey Task | Current Approach | Stereo Assistance |
|-------------|------------------|-------------------|
| GCP positioning | Manual survey each point | Validate surveyed positions; detect transcription errors |
| Cross-section geometry | Wading or boat survey | Assist with bank geometry above water line |
| Camera orientation | Manual calculation | Derive from stereo calibration |
| Scale reference | Measured distance in scene | Cross-check with stereo-derived distances |
| Setup verification | Re-survey if doubts | Quick stereo check before leaving site |

**What stereo will NOT do:**
- Measure underwater bathymetry (water surface reflects/refracts)
- Replace the need for at least some survey measurements (need reference scale)
- Work automatically without calibration

**Realistic expectations:**
- Accuracy depends on baseline length, camera resolution, and distance to subject
- At 10m distance with 0.5m baseline and 1080p cameras, theoretical accuracy is ~5-10cm
- Useful for error detection and reducing (not eliminating) survey effort
- Primary value: catch mistakes that would otherwise require a return visit

### Error Detection Capabilities

Even if stereo measurements are less accurate than traditional survey, they can detect errors:

| Error Type | Detection Method |
|------------|------------------|
| GCP mismatch | Compare stereo-derived GCP positions to entered values |
| Scale error | Compare stereo-derived distances to survey distances |
| Orientation error | Compare stereo horizon to expected level |
| Camera movement | Detect change in stereo geometry over time |

**Value:** Catch survey errors that would otherwise propagate to flow calculations.

### Implementation Path

#### Phase 1: Feasibility Assessment (No Hardware Changes)

1. Research USB cameras with external trigger support
2. Test software synchronization accuracy with current hardware concept
3. Evaluate if moving water matching is achievable
4. Determine minimum accuracy requirements for useful stereo

**Deliverable:** Go/no-go decision on stereo capability

#### Phase 2: Hardware Selection (If Go)

1. Select synchronized camera solution (likely Arducam MIPI or triggered USB)
2. Design mounting bracket with fixed, calibrated baseline
3. Source calibration targets and procedures
4. Update enclosure design for new camera connection

**Deliverable:** Updated hardware specification for stereo configuration

#### Phase 3: Software Development (If Go)

1. Implement synchronized capture
2. Implement stereo calibration routine
3. Implement stereo matching for water surface
4. Implement 3D reconstruction
5. Integrate with ORC survey workflow

**Deliverable:** Stereo survey software module

### Stereo Camera Bill of Materials (Tentative)

**Note:** These components are for evaluation only. Final selection pending feasibility assessment.

| Component | Qty | Est. Cost | Notes |
|-----------|-----|-----------|-------|
| Arducam Stereo Camera HAT | 1 | $80-150 | Includes 2x synchronized cameras |
| OR: IMX296 global shutter cameras | 2 | $100 each | With sync cable |
| Stereo mounting bracket | 1 | $30-50 | Custom or 3D printed |
| Calibration target (checkerboard) | 1 | $15 | For initial calibration |
| Longer MIPI cables (300mm) | 2 | $10 | Camera positioning flexibility |
| **Total** | | **$150-350** | Evaluation kit |

### Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Water surface too challenging for stereo | Medium | High | Test with actual river footage early |
| USB sync accuracy insufficient | High | High | Require hardware sync from start |
| Accuracy insufficient for survey replacement | Medium | Medium | Position as error detection, not survey replacement |
| Added complexity not worth benefit | Low | Medium | Keep as optional configuration |
| MIPI cameras don't fit IP67 housing concept | Medium | High | Research sealed MIPI camera options or waterproof adapters |

### Conclusion

Stereo camera capability for survey assistance is a **useful experimental feature** worth exploring. The main challenges are:
1. Achieving adequate synchronization with commodity hardware
2. Stereo matching on static scene elements (banks, GCPs) - water surface matching is NOT required for survey use
3. Maintaining IP67 sealing with MIPI camera connections

**Key insight:** Since we only need stereo for surveying the static scene (not tracking moving water), synchronization requirements may be less stringent than initially assessed. A single synchronized frame capture during setup may be sufficient.

**Recommendation:** Pursue as research effort in parallel with main RC-Box development. Do not block main product on stereo capability. Focus initial experiments on static scene reconstruction for GCP and bank geometry validation.

---

## Bill of Materials Summary

### Configuration A: Two-Box System

| Category | Component | Qty |
|----------|-----------|-----|
| **Compute** | Raspberry Pi 5 (4GB or 8GB) | 1 |
| | Witty Pi 4 | 1 |
| | 4G Modem (USB or HAT) | 1 |
| | SSD (512GB+ M.2 or USB) | 1 |
| | 5V DC-DC converter (if needed) | 1 |
| | 5A polyfuse | 1 |
| **Cameras** | Sealed IP67/IP68 USB camera | 2 |
| | USB cables (outdoor rated) | 2 |
| | Camera mounting brackets | 2 |
| **Power** | LiFePO4 battery (20/50/100Ah) | 1 |
| | Solar panel (50/100/200W) | 1 |
| | MPPT charge controller | 1 |
| | 20A fuse + holder | 1 |
| **IR System** | 850nm IR flood light (12V) | 1-2 |
| | 5V relay module | 1 |
| | 1N4007 diode | 1 |
| | 5A fuse + holder | 1 |
| **Enclosures** | Compute enclosure (IP67, ~200x150x100) | 1 |
| | Power enclosure (IP67, ~300x250x150) | 1 |
| | M20 IP68 cable glands | 5 |
| | M16 IP68 cable glands | 6 |
| | M12 IP67 SMA bulkhead | 2 |
| | M16 IP68 blanking plugs | 4 |
| | M12 GORE vent | 2 |
| **Electrical** | DIN rail (35mm) | 2 |
| | Terminal blocks (10A) | 6 |
| | Grounding lug | 2 |
| | DC power cable (14 AWG, 2m) | 1 |
| | Surge protectors (DC + coax) | 3 |
| **Anti-Theft** | Plunger tamper switch (N.C.) | 2 |
| | Vibration/shock sensor | 1 |
| | 12V siren/strobe (110-120dB, IP65) | 1 |
| | Alarm controller or latching relay | 1 |
| | Key switch (reset) | 1 |
| | Security screws + driver | 1 set |
| | "Alarm Protected" signage | 2 |
| **Consumables** | Silicone sealant (outdoor) | 1 tube |
| | Dielectric grease | 1 tube |
| | Cable labels | 1 set |
| | Spare fuses | 4 |
| | Spare glands | 4 |

### Configuration B: Single Combined Box

| Category | Component | Qty |
|----------|-----------|-----|
| **Compute** | Raspberry Pi 5 (4GB or 8GB) | 1 |
| | Witty Pi 4 | 1 |
| | 4G Modem (USB or HAT) | 1 |
| | SSD (512GB+ M.2 or USB) | 1 |
| | 5V DC-DC converter (if needed) | 1 |
| | 5A polyfuse | 1 |
| **Cameras** | Sealed IP67/IP68 USB camera | 2 |
| | USB cables (outdoor rated) | 2 |
| | Camera mounting brackets | 2 |
| **Power** | LiFePO4 battery (20/50/100Ah) | 1 |
| | Solar panel (50/100/200W) | 1 |
| | MPPT charge controller | 1 |
| | 20A fuse + holder | 1 |
| **IR System** | 850nm IR flood light (12V) | 1-2 |
| | 5V relay module | 1 |
| | 1N4007 diode | 1 |
| | 5A fuse + holder | 1 |
| **Enclosure** | Combined enclosure (IP67, ~400x300x200) | 1 |
| | M20 IP68 cable glands | 2 |
| | M16 IP68 cable glands | 6 |
| | M12 IP67 SMA bulkhead | 2 |
| | M16 IP68 blanking plugs | 2 |
| | M12 GORE vent | 1 |
| | Internal thermal divider (optional) | 1 |
| **Electrical** | DIN rail (35mm) | 2 |
| | Terminal blocks (10A) | 6 |
| | Grounding lug | 1 |
| | Surge protectors (DC + coax) | 3 |
| **Anti-Theft** | Plunger tamper switch (N.C.) | 1 |
| | Vibration/shock sensor | 1 |
| | 12V siren/strobe (110-120dB, IP65) | 1 |
| | Alarm controller or latching relay | 1 |
| | Key switch (reset) | 1 |
| | Security screws + driver | 1 set |
| | "Alarm Protected" signage | 2 |
| **Consumables** | Silicone sealant (outdoor) | 1 tube |
| | Dielectric grease | 1 tube |
| | Cable labels | 1 set |
| | Spare fuses | 4 |
| | Spare glands | 4 |

---

## Supplier Evaluation Criteria

When comparing suppliers, evaluate against these criteria:

### Mandatory Requirements

| Criterion | Requirement |
|-----------|-------------|
| Specification compliance | Meets all specs in this document |
| Availability | In stock or <4 week lead time |
| Multiple sources | At least 2 alternative suppliers identified |
| Documentation | Datasheet available in English |
| Shipping | Ships internationally |

### Weighted Scoring Criteria

| Criterion | Weight | Scoring |
|-----------|--------|---------|
| Price | 25% | Lower = better |
| Lead time | 15% | Shorter = better |
| Quality/reliability | 20% | Reviews, brand reputation, certifications |
| Community support | 15% | Forums, tutorials, troubleshooting resources |
| Serviceability | 15% | Ease of replacement, local availability |
| Documentation | 10% | Quality of datasheets, install guides |

### Preferred Suppliers (Examples)

| Category | Preferred Sources |
|----------|-------------------|
| Electronics | DigiKey, Mouser, Adafruit, SparkFun |
| Raspberry Pi | Official resellers, The Pi Hut, Pimoroni |
| Batteries | Reputable LiFePO4 brands (Battle Born, Renogy, SOK) |
| Solar | Renogy, Rich Solar, established brands |
| Enclosures | Polycase, Hammond, Fibox, TAKACHI |
| Cable glands | LAPP, Hummel, WISKA, or quality generics |
| General | Amazon (verified sellers), AliExpress (established stores with good ratings) |

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-12-01 | Initial specification based on design decisions |
| 1.1 | 2024-12-03 | Added: IR spotlight commodity control (USB relay + photoresistor); Data logger & sensor integration (RS485/Modbus, rainfall, weather station); Stereo camera stretch goal |

---

## References

- [Polycase IP67 Enclosures](https://www.polycase.com/ip67-enclosures)
- [TAKACHI Cable Glands](https://www.takachi-enclosure.com/cat/cable_glands)
- [Bulgin USB Connectors](https://www.bulgin.com/us/products/range/circular-data-connectors/400-series-usb.html)
- [GORE Protective Vents](https://www.gore.com/products/gore-protective-vents)
- [Witty Pi 4](https://www.uugear.com/product/witty-pi-4/)
- [PiSugar 3 Series](https://docs.pisugar.com/docs/product-wiki/battery/pisugar3/pisugar-3-series)
- [AXTON IR Illuminators](https://axtontech.com/)
