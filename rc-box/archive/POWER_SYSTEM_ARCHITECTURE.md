# RC-Box Power System Architecture

This document illustrates the electrical architecture of the RC-Box power system with diagrams and connection details.

## High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        RC-Box Power System                          │
│                                                                     │
│  ┌──────────────┐                                                  │
│  │ Solar Panel  │                                                  │
│  │  (10-50W)    │                                                  │
│  │   12V/18V    │                                                  │
│  └──────┬───────┘                                                  │
│         │ Solar Input                                              │
│         │ (+ / -)                                                  │
│         ▼                                                          │
│  ┌──────────────────────────────────────┐                         │
│  │   Charge Controller / Power Mgmt     │                         │
│  │  (PiJuice / PiSugar / MPPT)          │                         │
│  │                                       │                         │
│  │  - MPPT/PWM solar charging            │                         │
│  │  - Battery management                 │                         │
│  │  - Over/under voltage protection      │                         │
│  │  - RTC for scheduled wake/sleep       │                         │
│  │  - I2C monitoring interface           │                         │
│  └────┬──────────────────────────┬───────┘                         │
│       │                          │                                 │
│       │ Charge                   │ 5V Regulated                    │
│       ▼                          ▼ Output                          │
│  ┌─────────────┐          ┌──────────────────────┐                │
│  │   Battery   │          │   Raspberry Pi 5     │                │
│  │             │          │                      │                │
│  │ 12V LiFePO4 │          │  ┌────────────────┐  │                │
│  │ 20-100Ah    │          │  │  2x Pi Camera  │  │                │
│  │ 240-1200Wh  │          │  │   Module V3    │  │                │
│  │             │          │  └────────────────┘  │                │
│  └─────────────┘          │                      │                │
│                           │  ┌────────────────┐  │                │
│                           │  │  Storage       │  │                │
│  ┌─────────────┐          │  │  (SSD/microSD) │  │                │
│  │  Protection │          │  └────────────────┘  │                │
│  │   Circuits  │          │                      │                │
│  │             │          │  ┌────────────────┐  │                │
│  │ - Fuses     │          │  │  WiFi/Network  │  │                │
│  │ - Polarity  │          │  └────────────────┘  │                │
│  │ - TVS/MOV   │          └──────────────────────┘                │
│  └─────────────┘                                                  │
│                                                                     │
│  ┌─────────────────────────────────────────┐                      │
│  │         User Interface Elements         │                      │
│  │                                         │                      │
│  │  - Power On/Off Switch                  │                      │
│  │  - Maintenance Mode Switch              │                      │
│  │  - WiFi Hotspot Switch                  │                      │
│  │  - LED Indicators (Power, Battery,      │                      │
│  │    Charging, System Status)             │                      │
│  └─────────────────────────────────────────┘                      │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Detailed Wiring Diagram - Option 1: PiJuice Configuration

```
                     SOLAR PANEL (10-20W, 12V)
                            [+] [-]
                             │   │
                    ┌────────┘   └────────┐
                    │                     │
                 [FUSE]                   │
                 (2A)                     │
                    │                     │
          ┌─────────▼─────────────────────▼─────────┐
          │         PiJuice HAT                     │
          │                                          │
          │  Solar In:  [+]              [-]         │
          │              │                │          │
          │         ┌────▼────────────────▼────┐     │
          │         │  Charge Controller       │     │
          │         │  - MPPT/PWM              │     │
          │         │  - Temp compensation     │     │
          │         └────┬─────────────────────┘     │
          │              │                            │
          │         Battery Connector                 │
          │              │                            │
          │         ┌────▼────────────────────┐       │
          │         │  Li-ion/LiPo Battery    │       │
          │         │  3.7V, 12,000mAh max    │       │
          │         │  (44 Wh)                │       │
          │         └─────────────────────────┘       │
          │                                            │
          │  ┌──────────────────────────────────┐     │
          │  │  RTC (Real-Time Clock)           │     │
          │  │  - CR2032 backup battery         │     │
          │  │  - Wake/sleep scheduling         │     │
          │  └──────────────────────────────────┘     │
          │                                            │
          │  ┌──────────────────────────────────┐     │
          │  │  GPIO Interface                  │     │
          │  │  - Button inputs (3x)            │     │
          │  │  - LED output (RGB)              │     │
          │  │  - I2C monitoring                │     │
          │  └──────────────────────────────────┘     │
          │                                            │
          │  5V Out:  [GPIO Header to RPi5]           │
          └────────────────┬───────────────────────────┘
                           │
                           │ Mounts directly on GPIO
                           ▼
          ┌────────────────────────────────────────────┐
          │         Raspberry Pi 5                     │
          │                                            │
          │  Power: 5V from PiJuice GPIO               │
          │  I2C: Battery monitoring & control         │
          │  GPIO: Detect button presses               │
          │                                            │
          │  Peripherals:                              │
          │  - 2x Camera Module V3 (CSI)               │
          │  - Storage (microSD/SSD)                   │
          │  - WiFi (onboard)                          │
          └────────────────────────────────────────────┘
```

### PiJuice Connections Summary

| Connection | From | To | Wire/Connector | Notes |
|------------|------|-----|----------------|-------|
| Solar Input + | Solar Panel + | PiJuice Solar + | 18 AWG, MC4 to terminal | Red wire, fused |
| Solar Input - | Solar Panel - | PiJuice Solar - | 18 AWG, MC4 to terminal | Black wire |
| Battery + | PiJuice Batt + | Battery + | JST connector (included) | Included cable |
| Battery - | PiJuice Batt - | Battery - | JST connector (included) | Included cable |
| Power to RPi | PiJuice GPIO | RPi5 GPIO | Direct mount | No wires needed |
| I2C Data | PiJuice GPIO | RPi5 GPIO | Direct mount | SDA/SCL pins |
| Ground | PiJuice GPIO | RPi5 GPIO | Direct mount | Common ground |

## Detailed Wiring Diagram - Option 2: Custom MPPT Configuration

```
       SOLAR PANEL (50-100W, 18V)
              [+] [-]
               │   │
      ┌────────┘   └────────┐
      │                     │
   [FUSE]                   │
   (6A)                     │
      │                     │
      │    ┌────────────────┘
      │    │
      │    │   ┌─[TVS Diode]─┐  (Surge protection)
      │    │   │              │
      ▼    ▼   ▼              ▼
    ┌──────────────────────────────────┐
    │   MPPT Charge Controller         │
    │   (e.g., Victron 75/15)          │
    │                                   │
    │   Solar In:  [+]      [-]         │
    │               │        │          │
    │   Battery:   [+]      [-]         │
    │               │        │          │
    │   Load Out:  [+]      [-]         │
    │               │        │          │
    └───────────────┼────────┼──────────┘
                    │        │
         ┌──────────┘        └──────────┐
         │                               │
         ▼                               ▼
    ┌─────────────────────────────────────────┐
    │        12V LiFePO4 Battery              │
    │        20-100Ah (240-1200Wh)            │
    │                                         │
    │   [+]──[FUSE 20A]──┐                    │
    │   [-]──────────────┼───┐                │
    └────────────────────┼───┼────────────────┘
                         │   │
                         │   │
         ┌───────────────┘   └──────────┐
         │                               │
         ▼                               ▼
    ┌─────────────────────────────────────────┐
    │   DC-DC Buck Converter (12V → 5V)       │
    │   Output: 5V, 5A (25W max)              │
    │                                         │
    │   In:  [12V+] [12V-]                    │
    │   Out:  [5V+]  [5V-]                    │
    │          │      │                       │
    └──────────┼──────┼───────────────────────┘
               │      │
               ▼      ▼
         USB-C Cable (Power Delivery)
               │
               ▼
    ┌─────────────────────────────────────────┐
    │         Raspberry Pi 5                  │
    │                                         │
    │   Power: 5V/5A via USB-C                │
    │                                         │
    └─────────────────────────────────────────┘

    ┌─────────────────────────────────────────┐
    │   RTC Module (DS3231)                   │
    │   - I2C connection to RPi               │
    │   - CR2032 backup battery               │
    │   - Wake signal to power controller     │
    └─────────────────────────────────────────┘

    ┌─────────────────────────────────────────┐
    │   External Components                   │
    │                                         │
    │   - Power switch (DPST, 15A)            │
    │   - Mode switches (SPDT)                │
    │   - LED indicators (with resistors)     │
    │   - Voltage monitor (digital display)   │
    └─────────────────────────────────────────┘
```

### Custom MPPT Connections Summary

| Connection | From | To | Wire Gauge | Connector | Notes |
|------------|------|-----|------------|-----------|-------|
| Solar + | Panel + | MPPT Solar + | 14 AWG | MC4 to terminal | Fused, red |
| Solar - | Panel - | MPPT Solar - | 14 AWG | MC4 to terminal | Black |
| Battery + | MPPT Batt + | Battery + | 12 AWG | Ring terminal | Fused 20A |
| Battery - | MPPT Batt - | Battery - | 12 AWG | Ring terminal | Black |
| Load + | MPPT Load + | DC-DC In + | 14 AWG | Screw terminal | Red |
| Load - | MPPT Load - | DC-DC In - | 14 AWG | Screw terminal | Black |
| RPi Power + | DC-DC Out + | USB-C + | USB cable | USB-C PD cable | 5V |
| RPi Power - | DC-DC Out - | USB-C - | USB cable | USB-C PD cable | GND |

## Protection Circuit Details

### Fuse Sizing

```
Component              Voltage    Max Current    Fuse Rating    Fuse Type
─────────────────────────────────────────────────────────────────────────
Solar Input (10W)        12V         1A            2A          Fast-blow
Solar Input (20W)        12V         2A            3A          Fast-blow
Solar Input (50W)        18V         3A            5A          Fast-blow
Solar Input (100W)       18V         6A            10A         Fast-blow
Battery (20Ah)           12V         10A           15A         Slow-blow
Battery (50Ah)           12V         25A           30A         Slow-blow
Battery (100Ah)          12V         50A           60A         Slow-blow
RPi Load                 5V          5A            7.5A        Fast-blow
```

### Polarity Protection

**Method 1: Diode (Simple, lossy)**
```
    +12V ─────[Diode 1N5822]───── +12V (0.3V drop)
                Schottky
```
- Pros: Simple, cheap ($0.50)
- Cons: 0.3-0.5V drop, heat dissipation, power loss

**Method 2: P-Channel MOSFET (Efficient)**
```
    +12V ─────[P-MOSFET]───── +12V (0.01V drop)
          └──[Gate Control]
```
- Pros: Low drop (<0.1V), no heat
- Cons: More complex ($2-3), requires gate control circuit

**Recommendation:** Use MOSFET for battery connection, diode acceptable for low-current solar input.

### Overvoltage Protection

**TVS Diode across solar input:**
```
    Solar + ────┬──── To Charge Controller
                │
            [TVS Diode]  ← 18V breakdown voltage
                │
    Solar - ────┴──── To Charge Controller
```
- Part example: SMAJ18A (400W TVS, 18V standoff)
- Clamps voltage spikes from lightning, static, panel faults

### Reverse Current Protection

Solar panel at night can drain battery if no blocking diode:
```
Battery ──── [Schottky Diode] ──── Solar Panel
       (prevents reverse current flow at night)
```
- Most modern charge controllers have this built-in
- Verify in controller specs

## Hardware Switches

### Power Switch Configuration

**Master Power Switch (DPST - Double Pole Single Throw):**
```
    Battery +  ────[Switch Pole 1]──── System +
    Battery -  ────[Switch Pole 2]──── System -
```
- Disconnects both + and - for complete isolation
- Rating: 15A minimum
- Weatherproof toggle or rocker switch
- Panel mount through enclosure wall

### Soft Power Switch (for RPi shutdown)

**Momentary pushbutton connected to GPIO:**
```
    RPi GPIO Pin (e.g., GPIO3) ────[10kΩ]──── +3.3V
                │
                └──[Pushbutton]──── GND
```
- Short press: Trigger shutdown script
- Software detects button press, initiates graceful shutdown
- After shutdown, PiJuice/RTC can cut power

### Mode Switches

**3-Position Rotary Switch:**
```
    Position 1: Normal Operation
    Position 2: Maintenance Mode (always on, no auto-shutdown)
    Position 3: WiFi Hotspot Mode (enable hotspot for config)
```

Connected to GPIO pins:
```
    GPIO Pin A ────┬──[10kΩ]──── +3.3V
                   │
                   └──[Switch Common]

    GPIO Pin B ────┬──[10kΩ]──── +3.3V
                   │
                   └──[Switch Position Output]
```

Software reads GPIO states to determine mode.

## LED Indicator Design

### LED Circuit (per indicator)

```
    +5V ──┬──[Resistor]──[LED]──── GPIO Pin
          │
          └──[10kΩ]──── GND (pull-down)
```

**Resistor calculation:**
```
R = (Vsupply - VLED) / ILED
R = (5V - 2.0V) / 0.010A = 300Ω

Use standard 330Ω resistor
Power dissipation = (5V - 2V)² / 330Ω = 27mW (safe)
```

### Recommended LED Indicators

| LED Color | Function | State |
|-----------|----------|-------|
| Green | Power On | Solid = On, Off = Off |
| Yellow | Battery Charging | Solid = Charging, Flash = Full |
| Red | Battery Low | Flash = Low (<30%), Solid = Critical (<10%) |
| Blue | System Active | Pulse = Recording, Flash = Processing |
| White | WiFi/Network | Solid = Connected, Flash = Hotspot Active |

### High-Brightness LEDs for Daylight Visibility

For pole-mounted devices visible from ground in sunlight:
- Use high-brightness LEDs (1000-5000 mcd minimum)
- Consider diffused lens for wider viewing angle
- Light pipe from internal LED to external indicator
- Power consumption: 10-20mA per LED

**Example part:** Kingbright L-934SRD (5mm red, 2000mcd, 20mA)

## Power Budget by Configuration

### Configuration A: PiJuice + Small System

```
Components:
- PiJuice HAT
- 12,000mAh LiPo battery (44Wh)
- 10W solar panel
- Raspberry Pi 5
- 2x Camera Module V3
- microSD storage

Daily Budget:
- Recording: 10W × 1h = 10Wh
- Processing: 12W × 0.5h = 6Wh
- Idle: 5W × 6h = 30Wh
- Sleep: 0.1W × 16.5h = 1.7Wh
Total: 47.7 Wh/day

Battery Autonomy: 44Wh / 47.7Wh/day = 0.9 days (insufficient!)

Solar Generation (3.5 sun hours, 70% efficiency):
10W × 3.5h × 0.7 = 24.5 Wh/day (insufficient!)

Conclusion: This configuration is underpowered for the example duty cycle.
Either reduce recording frequency or upgrade to Configuration B.
```

### Configuration B: Custom MPPT + Medium System

```
Components:
- MPPT Charge Controller (Victron 75/15 or similar)
- 12V 50Ah LiFePO4 battery (600Wh)
- 50W solar panel
- DC-DC converter (12V → 5V)
- RTC module (DS3231)
- Raspberry Pi 5
- 2x Camera Module V3
- USB SSD storage

Daily Budget:
- Recording: 10W × 1h = 10Wh
- Processing: 12W × 0.5h = 6Wh
- Idle: 5W × 6h = 30Wh
- Sleep: 0.1W × 16.5h = 1.7Wh
Total: 47.7 Wh/day

Battery Autonomy (50% DoD): 600Wh × 0.5 / 47.7Wh/day = 6.3 days (excellent!)

Solar Generation (3.5 sun hours, 75% efficiency):
50W × 3.5h × 0.75 = 131 Wh/day (excess of 83 Wh/day)

Recharge time after 3 cloudy days:
Deficit: 47.7 × 3 = 143 Wh
Excess generation: 131 - 47.7 = 83 Wh/day
Recharge: 143 / 83 = 1.7 days

Conclusion: This configuration has excellent autonomy and can recover
quickly after cloudy periods. Recommended for reliable operation.
```

### Configuration C: Custom MPPT + Large System (High Power)

```
Components:
- MPPT Charge Controller (Victron 100/30)
- 12V 100Ah LiFePO4 battery (1200Wh)
- 100W solar panel
- DC-DC converter (12V → 5V, high efficiency)
- RTC module
- Raspberry Pi 5
- 2x Camera Module V3
- USB SSD
- Cellular modem (optional)

Daily Budget (increased usage):
- Recording: 10W × 4h = 40Wh
- Processing: 15W × 1h = 15Wh
- Upload (cellular): 10W × 1h = 10Wh
- Idle: 6W × 8h = 48Wh
- Sleep: 0.1W × 10h = 1Wh
Total: 114 Wh/day

Battery Autonomy (50% DoD): 1200Wh × 0.5 / 114Wh/day = 5.3 days (good)

Solar Generation (2.5 sun hours worst-case, 75% efficiency):
100W × 2.5h × 0.75 = 187.5 Wh/day (excess of 73.5 Wh/day)

Conclusion: This configuration supports higher power consumption
(more frequent recording, cellular connectivity) even in poor
solar conditions. Suitable for critical deployments.
```

## Cable Sizing Guide

### Voltage Drop Calculation

```
Voltage Drop (V) = 2 × I × L × R
where:
  I = current (A)
  L = one-way cable length (m)
  R = resistance per meter (Ω/m)
  2 = factor for both + and - wires

Acceptable voltage drop: 3% for main power, 5% for less critical
```

### Wire Gauge Selection

| AWG | Diameter (mm) | Resistance (Ω/km) | Max Current (A) | Use Case |
|-----|---------------|-------------------|-----------------|----------|
| 18  | 1.02          | 21.0              | 7               | Solar (small panel) |
| 16  | 1.29          | 13.3              | 10              | Solar (medium panel) |
| 14  | 1.63          | 8.3               | 15              | Solar (large panel), Load |
| 12  | 2.05          | 5.2               | 20              | Battery (medium) |
| 10  | 2.59          | 3.3               | 30              | Battery (large) |

### Example Calculation

```
50W solar panel to charge controller, 5 meter cable run:
Current: 50W / 18V = 2.78A
Using 16 AWG (13.3 Ω/km = 0.0133 Ω/m):
Voltage drop = 2 × 2.78A × 5m × 0.0133 Ω/m = 0.37V
Percentage drop = 0.37V / 18V = 2.1% (acceptable)

If cable run is 10 meters, drop = 0.74V = 4.1% (marginal, consider 14 AWG)
```

## Connector Selection

| Connection | Recommended Connector | Rationale |
|------------|----------------------|-----------|
| Solar Panel | MC4 (industry standard) | Weatherproof, locking, field-proven |
| Battery (removable) | Anderson Powerpole | Color-coded, high current, polarized |
| Battery (permanent) | Ring terminals + bolt | Secure, low resistance, reliable |
| DC-DC to RPi | USB-C cable | Standard, widely available |
| Low voltage signal | JST-XH or Dupont | Keyed, compact, inexpensive |
| Switches/buttons | Screw terminals | Easy field service, no crimping |

## Grounding Strategy

### For Solar-Only Systems (Floating Ground)

```
    Solar Panel -  ──┬──  Battery -  ──┬──  System GND
                     │                 │
                  (Chassis)         (Enclosure)
                     │                 │
                     └─────────────────┘
                            │
                     (Earth Ground - optional)
```

- Floating ground is acceptable for low voltage DC systems
- Connect enclosure chassis to battery negative for safety
- Earth ground (grounding rod) optional but recommended for lightning protection

### For AC-Powered Systems (Required Ground)

```
    AC Mains ──[Power Supply]── +12V
                    │
                   GND ────┬──── System GND
                           │
                           └──── Earth Ground (required)
```

- Earth ground is REQUIRED when AC mains is present
- Use grounding rod, water pipe, or building ground
- Follow local electrical codes

## Thermal Management

### Heat Sources

| Component | Typical Heat (W) | Mitigation |
|-----------|------------------|------------|
| Raspberry Pi 5 (under load) | 5-8W | Heatsink, airflow |
| DC-DC converter (inefficiency) | 1-3W | Heatsink, efficient converter |
| Battery (charging) | 2-5W | Ventilation, temp sensor |
| Charge controller | 0.5-2W | Usually OK, mount on enclosure |

### Enclosure Ventilation

For sealed enclosures in hot climates:
- Internal temperature can reach +70°C in direct sun
- Electronics typically rated to +70°C or +85°C
- Battery should stay below +45°C for longevity

**Options:**
1. **Passive ventilation:** Vents with gore-tex membrane (breathable, waterproof)
2. **Thermal mass:** Use metal enclosure as heatsink
3. **Reflective coating:** White or aluminum finish reflects solar radiation
4. **Active cooling:** Small 12V fan with temperature control (adds power consumption)

## Enclosure Layout Recommendations

```
┌─────────────────────────────────────────────────┐  ← Top
│                                                 │
│  ┌──────────────────────────────────────────┐   │
│  │  Raspberry Pi 5 + HAT                    │   │  ← Upper level
│  │  (cameras, storage, connectivity)        │   │
│  └──────────────────────────────────────────┘   │
│                                                 │
│  ┌──────────────────────────────────────────┐   │
│  │  Charge Controller / PiJuice             │   │  ← Mid level
│  │  (accessible for LED viewing)            │   │
│  └──────────────────────────────────────────┘   │
│                                                 │
│  ┌──────────────────────────────────────────┐   │
│  │  Battery (lowest level)                  │   │  ← Lower level
│  │  (heavy, low center of gravity)          │   │  (center of gravity)
│  └──────────────────────────────────────────┘   │
│                                                 │
├─────────────────────────────────────────────────┤
│  [Power SW] [Mode SW] [WiFi SW]   [LEDs]       │  ← Front panel
└─────────────────────────────────────────────────┘

Side view:
                    ┌──────┐
                    │Vent  │  ← Top vent (passive airflow)
                    └──┬───┘
┌────────────────────────┼───────────────────────────┐
│                        ▼                           │
│  ┌──────────────────────────────────────────┐     │
│  │         Raspberry Pi + Cameras           │ ←───┼─ Warmest
│  └──────────────────────────────────────────┘     │
│                                                   │
│  ┌──────────────────────────────────────────┐     │
│  │         Charge Controller                │     │
│  └──────────────────────────────────────────┘     │
│                                                   │
│  ┌──────────────────────────────────────────┐     │
│  │         Battery (heat source when        │     │
│  │         charging)                        │ ←───┼─ Heat rises
│  └──────────────────────────────────────────┘     │
│                                                   │
│                        ▲                           │
│                    ┌───┴───┐                       │
│                    │Vent   │  ← Bottom vent (intake)
│                    └───────┘
└───────────────────────────────────────────────────┘
```

**Key principles:**
- Heat rises: put heat sources (battery, RPi) at bottom if passive cooling
- Battery at bottom: low center of gravity for pole mounting stability
- Controllers mid-level: accessible for LED indicators and service
- Vertical airflow path for passive convection
- Cable entry at bottom (with drip loop) to prevent water ingress

## Next Steps

1. **Choose configuration** (A, B, or C) based on power budget from measurements
2. **Select specific components** (part numbers, suppliers)
3. **Create detailed wiring schematic** in CAD or drawing tool
4. **Order components** for prototype build
5. **Build prototype** following this architecture
6. **Test and iterate** on design

---

**Document Version:** 1.0
**Date:** 2025-11-28
**Related Documents:**
- POWER_BUDGET_TEMPLATE.md (for calculations)
- POWER_CONTROLLER_COMPARISON.md (for component selection)
- POWER_SYSTEM_FIELD_GUIDE.md (for deployment procedures)
