# Wiring Diagram - Sukabumi Site

**Print and laminate for field reference**

---

## System Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           SUKABUMI SITE WIRING                              │
│                    Solar Power / PoE Camera (power-cycled)                  │
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
│   12V IN ──┬──[FUSE 5A]──► PLANET PoE INJECTOR ──► PoE CAMERA            │
│            │                                                               │
│            └──► WITTY PI 5 (12V direct) ──► PI 5                          │
│                                                                            │
│   ┌─────────────────────────────────────────────────────────────────┐     │
│   │                    PI 5 + HAT STACK                              │     │
│   │  ┌─────────────┐                                                │     │
│   │  │ Pi-EzConnect│◄── GPIO terminals for LEDs, button, sensors    │     │
│   │  ├─────────────┤                                                │     │
│   │  │ Witty Pi 5  │◄── Power management, RTC, scheduling           │     │
│   │  │   HAT+      │                                                │     │
│   │  ├─────────────┤                                                │     │
│   │  │   Pi 5      │◄── USB: SSD, Modem | ETH: PoE Camera          │     │
│   │  │   8GB       │                                                │     │
│   │  └─────────────┘                                                │     │
│   └─────────────────────────────────────────────────────────────────┘     │
│                                                                            │
│   USB CONNECTIONS:                                                         │
│   ├── USB 3.0 (blue) ──► SSD Enclosure                                   │
│   └── USB 2.0 ──► Quectel Modem (PU201)                                  │
│                                                                            │
│   ETHERNET CONNECTION:                                                     │
│   └── ETH Port ──► Planet PoE Injector (DATA) ──► Camera via Cat6        │
│                                                                            │
│   ANTENNAS:                                                               │
│   ├── SMA Bulkhead 1 ──► LTE Antenna (Main)                              │
│   └── SMA Bulkhead 2 ──► LTE Antenna (Diversity)                         │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
           │                                         │
           │                                         │
           ▼                                         ▼
    ┌──────────────────────────┐            ┌────────────────┐
    │    ANNKE C1200 PoE       │            │   RAIN GAUGE   │
    │    CAMERA (IP67)         │            │   (I2C/GPIO)   │
    │  [Built-in IR, factory   │            │                │
    │   sealed, power-cycled   │            │                │
    │   with Pi via PoE]       │            │                │
    └──────────────────────────┘            └────────────────┘
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
           │     ├──[FUSE 5A]──► Planet PoE Injector ──► PoE Camera
           │     │
           │     └──► Witty Pi 5 power input (12V direct)
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

## PoE Camera Circuit

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         POE CAMERA CIRCUIT                                  │
└─────────────────────────────────────────────────────────────────────────────┘

                    PLANET IPOE-260-12V PoE INJECTOR
                    ┌─────────────────────────────────────┐
                    │                                     │
                    │  ┌─────────┐       ┌─────────┐     │
12V+ ──[FUSE 5A]───►│  │  12V+   │       │  DATA   │◄────┼──── Short Ethernet
                    │  │  INPUT  │       │ (to Pi) │     │     to Pi 5 ETH port
12V- (GND) ────────►│  │  12V-   │       ├─────────┤     │
                    │  │  INPUT  │       │DATA+PWR │◄────┼──── Cat6 outdoor cable
                    │  └─────────┘       │(to cam) │     │     to camera
                    │                    └─────────┘     │
                    └─────────────────────────────────────┘
                                              │
                                              │ Cat6 outdoor (shielded)
                                              │ through IP68 RJ45 feedthrough
                                              ▼
                    ┌─────────────────────────────────────┐
                    │       ANNKE C1200 PoE CAMERA        │
                    │                                     │
                    │   • 12MP resolution                 │
                    │   • Built-in IR LEDs (auto on/off)  │
                    │   • Factory-sealed IP67             │
                    │   • RTSP streaming                  │
                    │   • Static IP: 192.168.100.10       │
                    │                                     │
                    └─────────────────────────────────────┘

OPERATION:
1. Witty Pi wakes → 12V powers PoE injector
2. PoE injector provides 48V PoE to camera over Ethernet
3. Camera boots (~45-60s), establishes static IP
4. Pi captures video via RTSP over Ethernet connection
5. Camera IR LEDs auto-enable in low light (built-in photocell)
6. Witty Pi sleeps → 12V cuts off → camera powers down

ADVANTAGE: Camera power-cycled with Pi saves solar budget.
Built-in IR eliminates need for separate IR light and relay.
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

## PoE Camera Connection

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         POE CAMERA CONNECTION                               │
└─────────────────────────────────────────────────────────────────────────────┘

INSIDE ENCLOSURE                    │    OUTSIDE ENCLOSURE
                                    │
┌─────────────────┐                 │    ┌─────────────────────────────────┐
│  Raspberry Pi 5 │                 │    │      ANNKE C1200 PoE            │
│                 │                 │    │      CAMERA (IP67)              │
│   ┌─────────┐   │  ┌───────────┐  │    │                                 │
│   │Ethernet │◄──┼──│Planet PoE │──┼────┼──► Camera via Cat6 outdoor     │
│   │  Port   │   │  │Injector   │  │    │    (factory-sealed housing)    │
│   └─────────┘   │  │(DATA port)│  │    │                                 │
│                 │  └───────────┘  │    │   [Built-in IR LEDs]           │
└─────────────────┘    │            │    │                                 │
                  DATA+PWR port     │    └─────────────────────────────────┘
                       │            │
                       │ Cat6       │
                       ▼            │
              ┌─────────────────┐   │
              │ IP68 RJ45       │◄──┘
              │ Feedthrough     │
              │ (enclosure wall)│
              └─────────────────┘

CABLE DETAILS:
- Cat6 outdoor shielded cable (UV-resistant jacket)
- IP68 RJ45 waterproof coupler at enclosure wall
- Apply dielectric grease to outdoor RJ45 connections
- Secure cable to pole with UV-resistant cable ties
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
    │  │  ┌──────────┐  ┌────────┐  ┌──────┐  ┌──────────────────┐   │  │
    │  │  │ PI STACK │  │PoE Inj │  │ FUSE │  │  TERMINAL BLOCK  │   │  │
    │  │  │          │  │ Planet │  │HOLDER│  │  12V+ 12V- GND   │   │  │
    │  │  └──────────┘  └────────┘  └──────┘  └──────────────────┘   │  │
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
    │  ○ ○ ○   [●]        [M12]    [RJ45]   [M12]                        │
    │  LEDs   Button      12V in   PoE cam  Rain                         │
    │  R Y G              power    (IP68)   gauge                        │
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘

LEGEND:
○ = 10mm LED (panel mount)
● = 16mm Button (panel mount)
[M12] = Cable gland size
[RJ45] = IP68 RJ45 feedthrough for PoE camera
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

**Document Version:** 2.0
**Last Updated:** February 11, 2026
**Change:** Updated from USB camera + IR relay to PoE camera (ANNKE C1200) approach
