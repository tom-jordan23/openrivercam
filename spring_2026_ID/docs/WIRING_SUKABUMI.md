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
│   12V IN ──┬──► DDR-60G-5 (12V→5V) ──► hardwired 5V ──► PI 5           │
│            │                                                               │
│            └──► DDR-60G-12 (12V→12V reg) ──► RELAY ──► PoE SWITCH       │
│                                                         │                 │
│   ┌─────────────────────────────────────────────────────┼───────────────┐ │
│   │                    PI 5 + HAT STACK                  │               │ │
│   │  ┌─────────────┐                                    │               │ │
│   │  │ Geekworm    │◄── GPIO terminals for relay,        │               │ │
│   │  │ G469        │    LEDs, button, sensors            │               │ │
│   │  ├─────────────┤                                    │               │ │
│   │  │   Pi 5      │◄── USB: Flash Drive, Modem         │               │ │
│   │  │   8GB       │    ETH: PoE Switch uplink          │               │ │
│   │  │  (ML-2020   │    RTC: ML-2020 coin cell          │               │ │
│   │  │   RTC cell) │    J2:  External power button      │               │ │
│   │  │             │    Scheduling via built-in RTC     │               │ │
│   │  └─────────────┘                                    │               │ │
│   └─────────────────────────────────────────────────────┘               │ │
│                                                                            │
│   USB CONNECTIONS:                                                         │
│   ├── USB 3.0 (blue) ──► SanDisk 256GB USB Flash Drive                   │
│   └── USB 2.0 ──► Quectel Modem (EXVIST mPCIe-USB)                       │
│                                                                            │
│   GPIO TO RELAY (Electronics-Salon 4ch SPDT, 5V coil from G469):         │
│   ├── GPIO 24 ──► IN1 (PoE Switch power)                                 │
│   ├── GPIO 17 ──► IN2 (Green LED 12V)                                    │
│   ├── GPIO 27 ──► IN3 (Yellow LED 12V)                                   │
│   └── GPIO 22 ──► IN4 (Red LED 12V)                                      │
│   Relay 5V/GND from G469 Pin 2 (5V) / Pin 6 (GND)                       │
│                                                                            │
│   POWER BUTTON (Pi 5 J2 header, NOT GPIO):                                │
│   └── J2 (2-pin) ──► IP67 momentary switch (panel-mount, 22 AWG)         │
│       Brief press = power on (if halted) / clean shutdown (if running)    │
│       Hold ~10s = force power off (if frozen)                             │
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
           │     └──[FUSE 5A]──► DDR-60G-5 (12V→5V) ──► hardwired 5V ──► Pi 5
           │
           └──► From solar controller 12V+


5V POWER PATH:
┌────────────────┐      ┌─────────────┐      ┌─────────────┐
│ 12V Terminal   │──►   │ DDR-60G-5   │──►   │ Raspberry   │
│ Block (TB1)    │      │ DC-DC Conv  │      │ Pi 5        │
│                │      │ 12V → 5V    │      │ (hardwired  │
└────────────────┘      └─────────────┘      │  5V/GND)    │
                                             └─────────────┘

Pi 5 built-in RTC (ML-2020 coin cell) handles scheduling.

12V REGULATED PATH (CAMERA):
┌────────────────┐      ┌─────────────┐      ┌─────────────┐
│ 12V Terminal   │──►   │ DDR-60G-12  │──►   │ RELAY       │
│ Block (TB1)    │      │ DC-DC Conv  │      │ (GPIO-      │
│                │      │ 12V → 12V   │      │  triggered) │
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

                    ELECTRONICS-SALON 4ch SPDT RELAY MODULE
                    ┌─────────────────────────────────────┐
                    │  Coil: 5V from G469 Pin 2/Pin 6     │
                    │  GPIO 24 → IN1 triggers PoE relay   │
                    │  ACTIVE-HIGH (verified 2026-03-26):  │
                    │  GPIO HIGH = relay ON  = PoE ON     │
                    │  GPIO LOW  = relay OFF = PoE OFF    │
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
                    │   • RTSP stream to Pi               │
                    │   • DHCP IP: 192.168.50.139         │
                    │                                     │
                    └─────────────────────────────────────┘

OPERATION:
1. Pi 5 RTC wakes Pi (or external power button brief press) → Pi boots
2. GPIO 24 set HIGH → Relay CH1 energized → NO closes → 12V to PoE switch
3. PoE switch provides 48V PoE to camera over Ethernet
4. Camera boots (~45-60s), establishes DHCP IP
5. Pi captures 5s video via RTSP pull (orc-capture script)
6. Camera IR LEDs auto-enable in low light (built-in photocell)
7. Pi sets GPIO 24 LOW → relay de-energized → NO opens → camera off → Pi sleeps

NOTE: Active-high logic (verified 2026-03-26). Differs from ORC orc-gpio-relays.py
active-low convention — a PR will be submitted to make ORC polarity configurable.
At boot (GPIO unconfigured), relay defaults to de-energized = cameras off (fail-safe).

MANUAL POWER CONTROL (external power button on Pi 5 J2 header):
- Pi is off/halted: Brief press → powers on
- Pi is running:    Brief press → initiates clean shutdown
- Pi is frozen:     Hold ~10s  → forces power off

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
         │   │   │   │    │    │
         │   │   │   │    │    └──► RELAY IN4 → RED LED (12V panel-mount)
         │   │   │   │    │
         │   │   │   │    └──► RELAY IN3 → YELLOW LED (12V panel-mount)
         │   │   │   │
         │   │   │   └──► RELAY IN2 → GREEN LED (12V panel-mount)
         │   │   │
         │   │   └──► GND bus (button, sensors)
         │   │
         │   └──► SHT40 SCL (I2C clock, addr 0x44)
         │
         └──► SHT40 SDA (I2C data)

Additional GPIO connections (active on G469 but not shown in header above):
  GP4  (Pin 7)  ──► DS18B20 1-Wire data (with 4.7kΩ pull-up to 3V3)
  GP24 (Pin 18) ──► RELAY IN1 (PoE switch power)
  5V   (Pin 2)  ──► Relay module VCC
  GND  (Pin 6)  ──► Relay module GND


STATUS LED WIRING (12V panel-mount LEDs via relay channels):
┌────────────────────────────────────────────────────────────────────────────┐
│                                                                            │
│   GPIO 17 ──► RELAY IN2 ──► CH2 COM/NO ──► GREEN LED (+) ──┐              │
│                                                              │              │
│   GPIO 27 ──► RELAY IN3 ──► CH3 COM/NO ──► YELLOW LED (+) ──┼──► GND      │
│                                                              │              │
│   GPIO 22 ──► RELAY IN4 ──► CH4 COM/NO ──► RED LED (+) ────┘              │
│                                                                            │
│   12V from TB1 ──► RELAY CH2/CH3/CH4 COM (common 12V supply)              │
│   LEDs are 12V panel-mount (IP67), switched by relay channels             │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘


POWER BUTTON WIRING (Pi 5 J2 header — NOT GPIO):
┌────────────────────────────────────────────────────────────────────────────┐
│                                                                            │
│   Pi 5 J2 header (2-pin, near USB-C port)                                 │
│      │                                                                     │
│      └──────────────┐  (22 AWG, 2 wires)                                  │
│                     │                                                      │
│              ┌──────┴──────┐                                               │
│              │   BUTTON    │                                               │
│              │  (NO, IP67  │                                               │
│              │  momentary) │                                               │
│              └──────┬──────┘                                               │
│                     │                                                      │
│                     └──────────────► J2 Pin 2                              │
│                                                                            │
│   This is a dedicated hardware power header, NOT a GPIO pin.              │
│   Active low — button shorts the two J2 pins together.                    │
│                                                                            │
│   Brief press (halted) = power on                                         │
│   Brief press (running) = clean shutdown                                  │
│   Long press (3s, running) = enter maintenance mode                       │
│   Hold ~10s (frozen) = force power off                                    │
│                                                                            │
│   Single button handles power control AND maintenance mode.               │
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
│   3.3V ──[4.7kΩ]──┬── GPIO 4 (Pin 7, 1-Wire data)                        │
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
    │  │  │ (2 HATs) │  │PoE Sw  │  │MODULE│  │  FUSE  │  TB1    │   │  │
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
    │  LEDs   Power      PoE cam     12V in    Rain    DS18B20          │
    │  R Y G  Button     (IP67)      power     gauge   probe            │
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘

LEGEND:
○ = 10mm LED (panel mount)
● = Power button (panel mount, IP67 momentary, Pi 5 J2 header)
    Brief press = power on/off, long press (3s) = maintenance mode
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
| **Yellow** | 5V (Pi power to relay module VCC) |
| **Blue** | GPIO signal — relay IN1 (PoE switch) |
| **Green** | GPIO signal — relay IN2 (Green LED) |
| **Blue stripe** | GPIO signal — relay IN3 (Yellow LED) |
| **Green stripe** | GPIO signal — relay IN4 (Red LED) |

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

**Document Version:** 3.2
**Last Updated:** March 30, 2026
**Changes from v3.1:**
- Removed separate maintenance button (GPIO 23) — maintenance mode now triggered by long press (3s) on J2 power button
- Enclosure layout updated: 1 button (power) instead of 2
- Removed maintenance button wiring section

**Changes from v3.0:**
- Added external power button wired to Pi 5 J2 header (dedicated hardware power control, not GPIO)

**Changes from v2.0:**
- Replaced Planet IPOE-260-12V PoE injector with LINOVISION PoE Switch + Electronics-Salon relay
- Added DDR-60G-5 (12V→5V for Pi 5, hardwired) and DDR-60G-12 (12V→12V regulated for PoE switch)
- Renamed Pi-EzConnect → Geekworm G469
- Replaced M.2 SSD with SanDisk 256GB USB flash drive
- Replaced DFRobot SEN0575 I2C rain gauge with Hydreon RG-15 UART (GPIO 14/15)
- Added SHT40 temp/humidity sensor (I2C) and DS18B20 temperature probe (1-Wire)
- Replaced SMA bulkheads with Proxicast ANT-122-S02 puck antenna (12mm hole)
- Replaced cable glands with CNLINKO ethernet bulkhead and SP13 DC power bulkhead
