# Wiring Diagram - Sukabumi Site

**Print and laminate for field reference**

---

## System Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           SUKABUMI SITE WIRING                              │
│                      Solar Power / USB Camera / IR Light                    │
└─────────────────────────────────────────────────────────────────────────────┘

                                    ┌──────────────┐
                                    │  SOLAR PANEL │
                                    │    200W      │
                                    └──────┬───────┘
                                           │
                                           ▼
                        ┌──────────────────────────────────┐
                        │      EXISTING SOLAR SYSTEM       │
                        │  ┌────────────┐  ┌────────────┐  │
                        │  │  Charge    │  │  12V 50Ah  │  │
                        │  │ Controller │──│  Battery   │  │
                        │  └─────┬──────┘  └────────────┘  │
                        └────────┼─────────────────────────┘
                                 │ 12V Output
                                 ▼
┌────────────────────────────────────────────────────────────────────────────┐
│                          COMPUTE ENCLOSURE                                  │
│                                                                            │
│   12V IN ──┬──[FUSE 5A]──► RELAY ──[FUSE 5A]──► TO IR LIGHT (12V)        │
│            │                                                               │
│            └──► [12V→5V USB-C] ──► WITTY PI 5 ──► PI 5                    │
│                                                                            │
│   ┌─────────────────────────────────────────────────────────────────┐     │
│   │                    PI 5 + HAT STACK                              │     │
│   │  ┌─────────────┐                                                │     │
│   │  │ Pi-EzConnect│◄── GPIO terminals for LEDs, button, sensors    │     │
│   │  ├─────────────┤                                                │     │
│   │  │ Witty Pi 5  │◄── Power management, RTC, scheduling           │     │
│   │  │   HAT+      │                                                │     │
│   │  ├─────────────┤                                                │     │
│   │  │   Pi 5      │◄── USB: Camera, SSD, Modem, Relay             │     │
│   │  │   8GB       │                                                │     │
│   │  └─────────────┘                                                │     │
│   └─────────────────────────────────────────────────────────────────┘     │
│                                                                            │
│   USB CONNECTIONS:                                                         │
│   ├── USB 3.0 (blue) ──► SSD Enclosure                                   │
│   ├── USB 2.0 ──► Quectel Modem (PU201)                                  │
│   ├── USB 2.0 ──► Numato Relay Module                                    │
│   └── USB 2.0 ──► USB Camera (via cable gland)                           │
│                                                                            │
│   ANTENNAS:                                                               │
│   ├── SMA Bulkhead 1 ──► LTE Antenna (Main)                              │
│   └── SMA Bulkhead 2 ──► LTE Antenna (Diversity)                         │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
           │                    │                    │
           │                    │                    │
           ▼                    ▼                    ▼
    ┌────────────┐      ┌────────────┐      ┌────────────────┐
    │ USB CAMERA │      │  IR LIGHT  │      │   RAIN GAUGE   │
    │  (NoIR)    │      │ Tendelux   │      │   (I2C/GPIO)   │
    │            │      │   AI4      │      │                │
    └────────────┘      └────────────┘      └────────────────┘
```

---

## Power Distribution Detail

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         POWER DISTRIBUTION                                  │
└─────────────────────────────────────────────────────────────────────────────┘

SOLAR CONTROLLER 12V OUTPUT
          │
          │ (18 AWG wire, through M12 gland)
          ▼
    ┌─────────────────────────────────────────────────────────────┐
    │                    TERMINAL BLOCK TB1                        │
    │   ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐        │
    │   │ 12+ │ 12+ │ 12- │ 12- │ GND │ GND │ GND │ GND │        │
    │   │ IN  │ OUT │ IN  │ OUT │     │     │     │     │        │
    │   └──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴─────┴─────┴─────┘        │
    │      │     │     │     │     │                               │
    └──────┼─────┼─────┼─────┼─────┼───────────────────────────────┘
           │     │     │     │     │
           │     │     │     │     └──► GND bus (all ground returns)
           │     │     │     │
           │     │     │     └──► LED cathodes, button, sensors
           │     │     │
           │     │     └──► 12V return from all 12V devices
           │     │
           │     ├──[FUSE 5A]──► Numato Relay ──► IR Light circuit
           │     │
           │     └──► 12V→5V USB-C adapter ──► Witty Pi 5 power input
           │
           └──► From solar controller 12V+


USB-C POWER PATH:
┌────────────────┐      ┌─────────────┐      ┌─────────────┐
│ 12V Terminal   │──►   │ 12V → 5V    │──►   │ Witty Pi 5  │
│ Block          │      │ USB-C       │      │ HAT+ USB-C  │
│                │      │ Adapter     │      │ Input       │
└────────────────┘      └─────────────┘      └──────┬──────┘
                                                    │
                                                    ▼
                                             ┌─────────────┐
                                             │ Raspberry   │
                                             │ Pi 5        │
                                             │ (powered    │
                                             │ via HAT)    │
                                             └─────────────┘
```

---

## IR Light Control Circuit

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         IR LIGHT CONTROL                                    │
└─────────────────────────────────────────────────────────────────────────────┘

                         PI 5 USB PORT
                              │
                              │ (USB-A cable)
                              ▼
                    ┌─────────────────────┐
                    │   NUMATO 1-CH       │
                    │   USB RELAY         │
                    │                     │
                    │  ┌───┐ ┌───┐ ┌───┐  │
                    │  │COM│ │NO │ │NC │  │
                    │  └─┬─┘ └─┬─┘ └───┘  │
                    └────┼─────┼──────────┘
                         │     │
                         │     │ (NO = Normally Open)
                         │     │ (Closes when Pi powered + relay activated)
                         │     │
12V+ ──[FUSE 5A]─────────┘     │
                               │
                    ┌──────────┴──────────┐
                    │                     │
                    │    TENDELUX AI4     │
                    │    850nm IR LIGHT   │
                    │                     │
                    │   ┌───┐             │
                    │   │12+│◄────────────┼─── From relay COM
                    │   ├───┤             │
                    │   │12-│◄────────────┼─── To GND (terminal block)
                    │   └───┘             │
                    │                     │
                    │  [Built-in photocell│
                    │   controls on/off   │
                    │   based on ambient  │
                    │   light level]      │
                    │                     │
                    └─────────────────────┘

OPERATION:
1. Pi boots → systemd service sends "relay on 0" command
2. Relay closes → 12V available at Tendelux
3. Tendelux photocell senses light level:
   - Daytime: IR stays OFF (photocell open)
   - Nighttime: IR turns ON (photocell closed)
4. Pi shuts down → relay opens → Tendelux unpowered
```

---

## GPIO Connections (Pi-EzConnect)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       PI-EZCONNECT GPIO MAP                                 │
└─────────────────────────────────────────────────────────────────────────────┘

Pi-EzConnect Terminal Block (top of HAT stack)
┌────────────────────────────────────────────────────────────────────────────┐
│                                                                            │
│  3V3  5V  SDA SCL GP4 GND GP17 GP27 GP22 3V3 GP10 GP9 GP11 GND ...       │
│   │    │   │   │   │   │   │    │    │    │   │    │   │    │             │
│   ○    ○   ○   ○   ○   ○   ○    ○    ○    ○   ○    ○   ○    ○   ...       │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
         │   │       │   │    │    │
         │   │       │   │    │    └──► RED LED (+) via 330Ω
         │   │       │   │    │
         │   │       │   │    └──► YELLOW LED (+) via 330Ω
         │   │       │   │
         │   │       │   └──► GREEN LED (+) via 330Ω
         │   │       │
         │   │       └──► GND bus (LED cathodes, button)
         │   │
         │   └──► Rain gauge SCL (I2C clock)
         │
         └──► Rain gauge SDA (I2C data)


STATUS LED WIRING:
┌────────────────────────────────────────────────────────────────────────────┐
│                                                                            │
│   GPIO 17 ──[330Ω]──► GREEN LED (+) ──┐                                   │
│                                        │                                   │
│   GPIO 27 ──[330Ω]──► YELLOW LED (+) ──┼──► GND (common cathode)          │
│                                        │                                   │
│   GPIO 22 ──[330Ω]──► RED LED (+) ────┘                                   │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘


MAINTENANCE BUTTON WIRING:
┌────────────────────────────────────────────────────────────────────────────┐
│                                                                            │
│   GPIO 23 (with internal pull-up enabled)                                  │
│      │                                                                     │
│      └──────────────┐                                                      │
│                     │                                                      │
│              ┌──────┴──────┐                                               │
│              │   BUTTON    │                                               │
│              │  (NO, IP67) │                                               │
│              └──────┬──────┘                                               │
│                     │                                                      │
│                     └──────────────► GND                                   │
│                                                                            │
│   Button press: GPIO 23 goes LOW (active low)                             │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘


RAIN GAUGE WIRING (I2C):
┌────────────────────────────────────────────────────────────────────────────┐
│                                                                            │
│   DFRobot SEN0575            Pi-EzConnect                                 │
│   ┌──────────────┐           ┌─────────────┐                              │
│   │  VCC (red)   │───────────│    3V3      │                              │
│   │  GND (black) │───────────│    GND      │                              │
│   │  SDA (blue)  │───────────│  GPIO 2/SDA │                              │
│   │  SCL (yellow)│───────────│  GPIO 3/SCL │                              │
│   └──────────────┘           └─────────────┘                              │
│                                                                            │
│   I2C Address: Check datasheet (typically 0x1D or similar)                │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## USB Camera Connection

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         USB CAMERA CONNECTION                               │
└─────────────────────────────────────────────────────────────────────────────┘

INSIDE ENCLOSURE                    │    OUTSIDE ENCLOSURE
                                    │
┌─────────────────┐                 │    ┌─────────────────────────────────┐
│  Raspberry Pi 5 │                 │    │      VA IMAGING MVEC167         │
│                 │                 │    │      CAMERA HOUSING             │
│   ┌─────────┐   │                 │    │                                 │
│   │ USB 2.0 │◄──┼── Bulgin USB ───┼────┼──► USB Camera Board            │
│   │  Port   │   │    Cable        │    │    (8MP IMX179 NoIR)           │
│   └─────────┘   │    (IP67)       │    │                                 │
│                 │                 │    │   [Gore M12 Vent installed]    │
└─────────────────┘                 │    │                                 │
                              M16 Cable   └─────────────────────────────────┘
                                Gland
                                    │
                                    │
                            ┌───────┴───────┐
                            │               │
                            │  ENCLOSURE    │
                            │    WALL       │
                            │               │
                            └───────────────┘

CABLE DETAILS:
- Bulgin PX0840 series IP67 USB cable (2-3m)
- OR: Standard USB in HDPE conduit with sealed glands
- Seal cable gland with silicone after installation
```

---

## Complete Enclosure Layout

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ENCLOSURE INTERNAL LAYOUT (Top View)                     │
└─────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────────┐
    │ [Gore Vent]                                          [Gore Vent]    │
    │                                                                     │
    │  ┌──────────────────────────────────────────────────────────────┐  │
    │  │                        DIN RAIL                               │  │
    │  │  ┌──────────┐  ┌───────┐  ┌──────┐  ┌────────────────────┐   │  │
    │  │  │ PI STACK │  │ RELAY │  │ FUSE │  │  TERMINAL BLOCK    │   │  │
    │  │  │          │  │       │  │HOLDER│  │  12V+ 12V- GND     │   │  │
    │  │  └──────────┘  └───────┘  └──────┘  └────────────────────┘   │  │
    │  └──────────────────────────────────────────────────────────────┘  │
    │                                                                     │
    │  ┌────────────┐      ┌────────────────┐                            │
    │  │    SSD     │      │  LTE MODEM     │                            │
    │  │  (Velcro)  │      │  + PU201       │                            │
    │  └────────────┘      │  (Velcro)      │                            │
    │                      └────────────────┘                            │
    │                                                                     │
    │  [SMA]  [SMA]                                                      │
    │  Ant 1  Ant 2                                                      │
    │                                                                     │
    │  ○ ○ ○   [●]        [M12]    [M16]    [M12]                        │
    │  LEDs   Button      12V in   USB cam  Rain                         │
    │  R Y G              power    cable    gauge                        │
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘

LEGEND:
○ = 10mm LED (panel mount)
● = 16mm Button (panel mount)
[M12/M16] = Cable gland size
[SMA] = SMA bulkhead antenna connector
```

---

## Wire Color Code

| Wire Color | Purpose |
|------------|---------|
| **Red** | 12V positive (+) |
| **Black** | Ground / 12V negative (-) |
| **Green** | Ground (earth) |
| **Yellow** | Signal (GPIO, I2C SCL) |
| **Blue** | Signal (I2C SDA) |
| **White** | Signal (alternate) |
| **Orange** | 5V positive (if used) |

---

## Terminal Block Labels

Print and attach to terminal blocks:

```
TB1 - MAIN POWER
┌────┬────┬────┬────┬────┬────┐
│12+ │12+ │12- │12- │GND │GND │
│ IN │OUT │ IN │OUT │    │    │
└────┴────┴────┴────┴────┴────┘
```

---

**PRINT THIS DOCUMENT - LAMINATE FOR FIELD USE**

**Document Version:** 1.0
**Last Updated:** January 9, 2026
