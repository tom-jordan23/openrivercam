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
│   12V IN ──┬──► DDR-60G-5 (12V→5V) ──► WITTY PI 5 ──► PI 5              │
│            │                                                               │
│            └──► DDR-60G-12 (12V→12V reg) ──► RELAY ──► PoE SWITCH       │
│                                                         │                 │
│   ┌─────────────────────────────────────────────────────┼───────────────┐ │
│   │                    PI 5 + HAT STACK                  │               │ │
│   │  ┌─────────────┐                                    │               │ │
│   │  │ Geekworm    │◄── GPIO terminals for LEDs,        │               │ │
│   │  │ G469        │    button, sensors                  │               │ │
│   │  ├─────────────┤                                    │               │ │
│   │  │ Witty Pi 5  │◄── Power management, RTC,           │               │ │
│   │  │   HAT+      │    scheduling (solar duty cycling) │               │ │
│   │  ├─────────────┤                                    │               │ │
│   │  │   Pi 5      │◄── USB: Flash Drive, Modem, Relay  │               │ │
│   │  │   8GB       │    ETH: PoE Switch uplink          │               │ │
│   │  └─────────────┘                                    │               │ │
│   └─────────────────────────────────────────────────────┘               │ │
│                                                                            │
│   USB CONNECTIONS:                                                         │
│   ├── USB 3.0 (blue) ──► SanDisk 256GB USB Flash Drive                   │
│   ├── USB 2.0 ──► Quectel Modem (EXVIST mPCIe-USB)                       │
│   └── USB 2.0 ──► Relay coil power (passive trigger)                     │
│                                                                            │
│   ETHERNET CONNECTION:                                                     │
│   └── ETH Port ──► LINOVISION PoE Switch (uplink) ──► Camera via Cat6   │
│                                                                            │
│   ANTENNA:                                                                 │
│   └── Proxicast ANT-122-S02 Puck Antenna (12mm hole mount, IP67)         │
│       Main + Diversity SMA pigtails to modem U.FL connectors             │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
           │                                         │
           │                                         │
           ▼                                         ▼
    ┌──────────────────────────┐            ┌────────────────┐
    │    ANNKE C1200 PoE       │            │   RAIN GAUGE   │
    │    CAMERA (IP67)         │            │   Hydreon RG-15│
    │  [Built-in IR, factory   │            │   (UART/GPIO)  │
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
          │ (18 AWG wire, through SP13 DC power bulkhead)
          ▼
    ┌─────────────────────────────────────────────────────────────┐
    │                    TERMINAL BLOCK TB1                        │
    │   ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐        │
    │   │ 12+ │ 12+ │ 12+ │ 12- │ 12- │ GND │ GND │ GND │        │
    │   │ IN  │ CPU │ CAM │ IN  │ OUT │     │     │     │        │
    │   └──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴─────┴─────┘        │
    │      │     │     │     │     │     │                         │
    └──────┼─────┼─────┼─────┼─────┼─────┼─────────────────────────┘
           │     │     │     │     │     │
           │     │     │     │     │     └──► GND bus (all ground returns)
           │     │     │     │     │
           │     │     │     │     └──► LED cathodes, button, sensors
           │     │     │     │
           │     │     │     └──► 12V return from all 12V devices
           │     │     │
           │     │     └──[FUSE 5A]──► DDR-60G-12 ──► RELAY ──► PoE Switch
           │     │
           │     └──[FUSE 5A]──► DDR-60G-5 (12V→5V) ──► Witty Pi 5
           │
           └──► From solar controller 12V+


5V POWER PATH:
┌────────────────┐      ┌─────────────┐      ┌─────────────┐
│ 12V Terminal   │──►   │ DDR-60G-5   │──►   │ Witty Pi 5  │
│ Block (TB1)    │      │ DC-DC Conv  │      │ HAT+ (5V    │
│                │      │ 12V → 5V    │      │  input)     │
└────────────────┘      └─────────────┘      └──────┬──────┘
                                                    │
                                                    ▼
                                             ┌─────────────┐
                                             │ Raspberry   │
                                             │ Pi 5        │
                                             │ (powered    │
                                             │ via HAT)    │
                                             └─────────────┘

12V REGULATED PATH (CAMERA):
┌────────────────┐      ┌─────────────┐      ┌─────────────┐
│ 12V Terminal   │──►   │ DDR-60G-12  │──►   │ RELAY       │
│ Block (TB1)    │      │ DC-DC Conv  │      │ (USB-powered│
│                │      │ 12V → 12V   │      │  from Pi)   │
└────────────────┘      │ regulated   │      └──────┬──────┘
                        └─────────────┘             │
                                                    ▼
                                             ┌─────────────┐
                                             │ LINOVISION  │
                                             │ PoE Switch  │
                                             │ (12V in)    │
                                             └─────────────┘
```

---

## PoE Camera Circuit

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         POE CAMERA CIRCUIT                                  │
└─────────────────────────────────────────────────────────────────────────────┘

                    ELECTRONICS-SALON RELAY MODULE
                    ┌─────────────────────────────────────┐
                    │  Coil: USB-powered from Pi 5        │
                    │  Pi ON  = relay closed = PoE ON     │
                    │  Pi OFF = relay open = PoE OFF      │
                    │                                     │
12V reg ──────────►│  NO (12V regulated in)              │
(from DDR-60G-12)  │  COM (12V switched out) ──────────►│──►
                    └─────────────────────────────────────┘
                                                          │
                    LINOVISION INDUSTRIAL PoE SWITCH       │
                    ┌─────────────────────────────────────┐│
                    │                                     ││
                    │  ┌─────────┐       ┌─────────┐     ││
12V switched ──────►│  │  12V+   │       │ UPLINK  │◄────┼┼── Short Ethernet
                    │  │  INPUT  │       │ (to Pi) │     ││    to Pi 5 ETH port
GND ───────────────►│  │  12V-   │       ├─────────┤     ││
                    │  │  INPUT  │       │  PoE    │◄────┼┼── Cat6 outdoor cable
                    │  └─────────┘       │  OUT    │     ││    to camera
                    │                    └─────────┘     ││
                    └─────────────────────────────────────┘│
                                              │            │
                                              │ Cat6 outdoor (shielded)
                                              │ through CNLINKO bulkhead
                                              ▼
                    ┌─────────────────────────────────────┐
                    │       ANNKE C1200 PoE CAMERA        │
                    │                                     │
                    │   • 12MP resolution                 │
                    │   • Built-in IR LEDs (auto on/off)  │
                    │   • Factory-sealed IP67             │
                    │   • RTSP streaming                  │
                    │   • DHCP IP: 192.168.50.139         │
                    │                                     │
                    └─────────────────────────────────────┘

OPERATION:
1. Witty Pi wakes → Pi boots → USB powers relay coil
2. Relay closes → 12V regulated to PoE switch
3. PoE switch provides 48V PoE to camera over Ethernet
4. Camera boots (~45-60s), establishes DHCP IP
5. Pi captures video via RTSP over Ethernet connection
6. Camera IR LEDs auto-enable in low light (built-in photocell)
7. Witty Pi sleeps → Pi shuts down → USB power lost → relay opens → camera off

ADVANTAGE: Camera power-cycled with Pi saves solar budget.
Built-in IR eliminates need for separate IR light and relay.
DDR-60G converters provide regulated voltage from battery
(which varies 10-14V depending on charge state).
```

---

## GPIO Connections (Geekworm G469)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       GEEKWORM G469 GPIO MAP                                │
└─────────────────────────────────────────────────────────────────────────────┘

Geekworm G469 Terminal Block (top of HAT stack)
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
         │   └──► SHT40 SCL (I2C clock, addr 0x44)
         │
         └──► SHT40 SDA (I2C data)


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


RAIN GAUGE WIRING (UART):
┌────────────────────────────────────────────────────────────────────────────┐
│                                                                            │
│   Hydreon RG-15              Geekworm G469 / TB1                          │
│   ┌──────────────┐           ┌─────────────┐                              │
│   │  VCC         │───────────│  12V (TB1)  │  (7-24V input range)        │
│   │  GND         │───────────│  GND (TB1)  │                              │
│   │  TX (out)    │───────────│  GPIO 15/RX │  RS232 TTL 3.3V             │
│   │  RX (in)     │───────────│  GPIO 14/TX │  RS232 TTL 3.3V             │
│   └──────────────┘           └─────────────┘                              │
│                                                                            │
│   No level shifter needed. RG-15 signal is 3.3V TTL.                     │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘


SHT40 TEMPERATURE/HUMIDITY SENSOR (I2C):
┌────────────────────────────────────────────────────────────────────────────┐
│                                                                            │
│   SHT40 (I2C addr 0x44)     Geekworm G469                                │
│   ┌──────────────┐           ┌─────────────┐                              │
│   │  VCC         │───────────│    3V3      │                              │
│   │  GND         │───────────│    GND      │                              │
│   │  SDA         │───────────│  GPIO 2/SDA │                              │
│   │  SCL         │───────────│  GPIO 3/SCL │                              │
│   └──────────────┘           └─────────────┘                              │
│                                                                            │
│   STEMMA QT to bare wire cable (200mm). Inside enclosure.                │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘


DS18B20 WATERPROOF TEMPERATURE PROBE (1-Wire):
┌────────────────────────────────────────────────────────────────────────────┐
│                                                                            │
│   3.3V ──[4.7kΩ]──┬── GPIO 24 (1-Wire data)                              │
│                    │                                                       │
│                    │   ┌───────────────────────┐                           │
│                    ├───│  DS18B20 Waterproof    │                           │
│                    │   │  Temperature Probe     │                           │
│                    │   │  (stainless, 1m cable) │                           │
│   GND ─────────────┼───│                        │                           │
│                    │   │  OUTSIDE enclosure     │                           │
│                    │   │  (through PG9 gland)   │                           │
│                    │   └───────────────────────┘                           │
│                    │                                                       │
│                    └── Pull-up resistor on Geekworm G469 terminals        │
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
│   │Ethernet │◄──┼──│LINOVISION │──┼────┼──► Camera via Cat6 outdoor     │
│   │  Port   │   │  │PoE Switch │  │    │    (factory-sealed housing)    │
│   └─────────┘   │  │(uplink)   │  │    │                                 │
│                 │  └───────────┘  │    │   [Built-in IR LEDs]           │
└─────────────────┘    │            │    │                                 │
                  PoE port          │    └─────────────────────────────────┘
                       │            │
                       │ Cat6       │
                       ▼            │
              ┌─────────────────┐   │
              │ CNLINKO         │◄──┘
              │ Ethernet        │
              │ Bulkhead (IP67) │
              │ (enclosure wall)│
              └─────────────────┘

CABLE DETAILS:
- Cat6 outdoor shielded cable (UV-resistant jacket)
- CNLINKO weatherproof ethernet bulkhead at enclosure wall (IP67)
- Apply dielectric grease to outdoor connections
- Secure cable to pole with UV-resistant cable ties
```

---

## Complete Enclosure Layout

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ENCLOSURE INTERNAL LAYOUT (Top View)                     │
└─────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────────┐
    │ [Gore Vent]              [Puck Antenna]              [Gore Vent]    │
    │                          (12mm hole)                                 │
    │                                                                     │
    │  ┌──────────────────────────────────────────────────────────────┐  │
    │  │                        DIN RAIL                               │  │
    │  │  ┌──────────┐  ┌────────┐  ┌──────┐  ┌──────────────────┐   │  │
    │  │  │ PI STACK │  │LINOVIS.│  │ RELAY│  │  DDR-60G-5/12    │   │  │
    │  │  │ (3 HATs) │  │PoE Sw  │  │MODULE│  │  FUSE  │  TB1    │   │  │
    │  │  └──────────┘  └────────┘  └──────┘  └──────────────────┘   │  │
    │  └──────────────────────────────────────────────────────────────┘  │
    │                                                                     │
    │  ┌────────────────┐                                                │
    │  │  LTE MODEM     │                                                │
    │  │  + EXVIST mPCIe│                                                │
    │  │  (Velcro)      │                                                │
    │  └────────────────┘                                                │
    │                                                                     │
    │  ○ ○ ○   [●]        [CNLINKO]   [SP13]    [PG9]   [PG9]           │
    │  LEDs   Button      PoE cam     12V in    Rain    DS18B20          │
    │  R Y G              (IP67)      power     gauge   probe            │
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘

LEGEND:
○ = 10mm LED (panel mount)
● = 16mm Button (panel mount)
[CNLINKO] = Weatherproof ethernet bulkhead (IP67)
[SP13] = Weatherproof DC power bulkhead (IP68)
[PG9] = Cable gland for sensor cables
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
│12+ │12+ │12+ │12- │GND │GND │
│ IN │CPU │CAM │ IN │    │    │
└────┴────┴────┴────┴────┴────┘
```

---

**PRINT THIS DOCUMENT - LAMINATE FOR FIELD USE**

**Document Version:** 3.0
**Last Updated:** March 9, 2026
**Changes from v2.0:**
- Replaced Planet IPOE-260-12V PoE injector with LINOVISION PoE Switch + Electronics-Salon relay
- Added DDR-60G-5 (12V→5V for Witty Pi/Pi power) and DDR-60G-12 (12V→12V regulated for PoE switch)
- Renamed Pi-EzConnect → Geekworm G469
- Replaced M.2 SSD with SanDisk 256GB USB flash drive
- Replaced DFRobot SEN0575 I2C rain gauge with Hydreon RG-15 UART (GPIO 14/15)
- Added SHT40 temp/humidity sensor (I2C) and DS18B20 temperature probe (1-Wire)
- Replaced SMA bulkheads with Proxicast ANT-122-S02 puck antenna (12mm hole)
- Replaced cable glands with CNLINKO ethernet bulkhead and SP13 DC power bulkhead
