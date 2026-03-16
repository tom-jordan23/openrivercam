# Wiring Diagram - Jakarta Site

**Print and laminate for field reference**

---

## System Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           JAKARTA SITE WIRING                               │
│                   AC Power / PoE Cameras / 24hr UPS                         │
└─────────────────────────────────────────────────────────────────────────────┘

            220V AC (Building Power)
                    │
                    ▼
            ┌───────────────┐
            │ SURGE         │
            │ PROTECTOR     │
            │ (Heschen      │
            │  HS-40-N 2P)  │
            └───────┬───────┘
                    │
                    ▼
            ┌───────────────┐         ┌───────────────────┐
            │ MEAN WELL     │         │                   │
            │ SDR-120-12    │──12V───►│  LiFePO4 CHARGER  │
            │ (120W, 12V)   │         │  (20A)            │
            └───────┬───────┘         └─────────┬─────────┘
                    │                           │
                    │                           ▼
                    │                   ┌───────────────────┐
                    │                   │  LiFePO4 BATTERY  │
                    │                   │  12V 100Ah        │
                    │                   │  (1280Wh)         │
                    │                   │  BMS built-in     │
                    │                   │  low-voltage      │
                    │                   │  cutoff           │
                    │                   └─────────┬─────────┘
                    │                             │
                    └────────────┬────────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────────┐
                    │      12V DISTRIBUTION       │
                    │      (Terminal Block)       │
                    └──────────────┬──────────────┘
                                   │
              ┌────────────────────┼────────────────────┐
              │                    │                    │
              ▼                    ▼                    ▼
    ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
    │  PoE SWITCH     │  │   DDR-60G-5     │  │  PTC HEATER     │
    │  LINOVISION     │  │   (12V → 5V)   │  │  (Enclosure)    │
    │  + RELAY        │  │   → Pi 5 GPIO   │  │  + FANS         │
    └────────┬────────┘  └────────┬────────┘  └─────────────────┘
                                  │
                           ┌──────┴──────┐
                           │ Raspberry   │
                           │ Pi 5        │
                           │             │    ┌─────────────────┐
                           │  J2 header ─┼───►│ POWER BUTTON    │
                           │  (2-pin)    │    │ (IP67 momentary │
                           │             │    │  panel-mount)   │
                           └─────────────┘    └─────────────────┘
             │
      ┌──────┴──────┐
      │             │
      ▼             ▼
┌──────────┐  ┌──────────┐
│ CAMERA 1 │  │ CAMERA 2 │
│ (PoE)    │  │ (PoE)    │
└──────────┘  └──────────┘
```

---

## AC Power Input Detail

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         AC POWER INPUT                                      │
└─────────────────────────────────────────────────────────────────────────────┘

                    BUILDING 220V AC
                          │
                          │ (through SP13 DC power bulkhead)
                          ▼
                ┌─────────────────────┐
                │  SP13 DC POWER      │
                │  BULKHEAD (IP68)    │
                └─────────┬──────────┘
                          │
     ┌────────────────────┼────────────────────┐
     │ L (Line/Hot)       │ N (Neutral)        │ PE (Earth/Ground)
     │ Brown              │ Blue               │ Green/Yellow
     ▼                    ▼                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                   HESCHEN HS-40-N 2P SURGE PROTECTOR                    │
│                       (40kA, 275V)                                      │
│  ┌─────┐  ┌─────┐  ┌─────┐                                             │
│  │  L  │  │  N  │  │ PE  │                                             │
│  │ IN  │  │ IN  │  │ IN  │                                             │
│  └──┬──┘  └──┬──┘  └──┬──┘                                             │
│     │        │        │                                                 │
│  ┌──┴──┐  ┌──┴──┐  ┌──┴──┐                                             │
│  │  L  │  │  N  │  │ PE  │                                             │
│  │ OUT │  │ OUT │  │ OUT │                                             │
│  └──┬──┘  └──┬──┘  └──┬──┘                                             │
└─────┼───────┼───────┼───────────────────────────────────────────────────┘
      │       │       │
      │       │       └──► GROUND BAR ──► GROUND ROD (1.5m copper)
      │       │
      ▼       ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     MEAN WELL SDR-120-12                                │
│                     (DIN Rail Mount)                                    │
│                                                                         │
│  AC INPUT:                    DC OUTPUT:                                │
│  ┌─────┐  ┌─────┐            ┌─────┐  ┌─────┐                          │
│  │  L  │  │  N  │            │ +V  │  │ -V  │                          │
│  │     │  │     │            │ 12V │  │ GND │                          │
│  └─────┘  └─────┘            └──┬──┘  └──┬──┘                          │
│                                 │        │                              │
│    88-264V AC input             │        │    12V DC output            │
│    (auto-ranging)               │        │    10A max (120W)           │
└─────────────────────────────────┼────────┼──────────────────────────────┘
                                  │        │
                                  ▼        ▼
                           TO TERMINAL BLOCK TB1
```

---

## Battery & UPS System

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         BATTERY / UPS SYSTEM                                │
└─────────────────────────────────────────────────────────────────────────────┘

FROM MEAN WELL 12V OUTPUT
         │
         ├──────────────────────────────────┐
         │                                  │
         ▼                                  ▼
┌─────────────────────┐            ┌─────────────────────┐
│  TERMINAL BLOCK     │            │  LiFePO4 CHARGER    │
│  TB1 (System 12V)   │            │  (20A, 14.6V max)   │
│                     │            │                     │
│  Powers loads when  │            │  Bulk → Absorb →    │
│  AC present         │            │  Float charging     │
└─────────────────────┘            └──────────┬──────────┘
                                              │
                                              ▼
                                   ┌─────────────────────┐
                                   │  LiFePO4 BATTERY    │
                                   │  12V 100Ah          │
                                   │  (1280Wh capacity)  │
                                   │                     │
                                   │  BMS Built-in:      │
                                   │  - Over-discharge   │
                                   │    (low-V cutoff)   │
                                   │  - Over-charge      │
                                   │  - Over-current     │
                                   │  - Temperature      │
                                   └──────────┬──────────┘
                                              │
                                              ▼
                                   ┌─────────────────────┐
                                   │  TERMINAL BLOCK     │
                                   │  TB1 (System 12V)   │
                                   │                     │
                                   │  Battery feeds TB1  │
                                   │  when AC fails      │
                                   └─────────────────────┘


POWER PATH LOGIC:
┌────────────────────────────────────────────────────────────────────────────┐
│                                                                            │
│  AC PRESENT:                                                               │
│  - Mean Well powers all loads directly via TB1                            │
│  - Charger maintains battery at float voltage                              │
│  - Battery on standby (BMS manages health)                                │
│                                                                            │
│  AC FAILS:                                                                 │
│  - Mean Well output drops to 0V                                           │
│  - Battery discharges through TB1 to all loads                            │
│  - BMS disconnects at low-voltage cutoff to protect battery               │
│                                                                            │
│  AC RESTORED:                                                              │
│  - Mean Well resumes powering loads                                       │
│  - Charger resumes charging battery                                       │
│  - BMS reconnects when battery recovers                                   │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## 12V Distribution

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         12V DISTRIBUTION                                    │
└─────────────────────────────────────────────────────────────────────────────┘

                    TB1 (MAIN 12V BUS)
         ┌──────────────────────────────────────┐
         │ 12+  12+  12+  12-  12-  12-  GND GND│
         └──┬────┬────┬────┬────┬────┬────┬────┬┘
            │    │    │    │    │    │    │    │
            │    │    │    └────┴────┴────┴────┴──► All GND returns
            │    │    │
            │    │    └──[FUSE 10A]──► RELAY → LINOVISION PoE SWITCH (12V)
            │    │
            │    └──[FUSE 5A]──► DDR-60G-5 (12V→5V) → hardwired 5V/GND → PI 5 GPIO
            │
            └──[FUSE 5A]──► PTC HEATER (via hygrostat) + FANS


FUSE SPECIFICATIONS:
┌─────────────────────────────────────────────────────────────────────────────┐
│  FUSE        │  RATING  │  PROTECTS                                        │
├──────────────┼──────────┼────────────────────────────────────────────────────┤
│  F1 (Main)   │  15A     │  Entire 12V bus from battery/PSU                 │
│  F2 (PoE)    │  10A     │  Relay + PoE switch (60W max = 5A, plus margin)  │
│  F3 (Pi)     │  5A      │  DDR-60G-5 + Pi (25W max = 2A, plus margin)     │
│  F4 (Heater) │  5A      │  PTC heater + fans (25W max, plus margin)       │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## PoE Camera System

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         POE CAMERA SYSTEM                                   │
└─────────────────────────────────────────────────────────────────────────────┘

12V FROM TB1
    │
    │ [FUSE 10A]
    │
    ▼
┌───────────────────────────────────────────────────────────────────────────┐
│               ELECTRONICS-SALON DIN RAIL RELAY MODULE                     │
│               (4-SPDT, GPIO-triggered via G469 breakout)                  │
│                                                                           │
│  Coil power: 5V/GND from Pi via Geekworm G469 breakout                  │
│  Control: GPIO 24 → IN1 (PoE switch)                                    │
│  GPIO HIGH = relay energized = NO contact closed = 12V passes            │
│  GPIO LOW  = relay de-energized = NO contact open = 12V cut              │
│                                                                           │
│  IN (12V from TB1) ──► CH1 NO contact ──► OUT (12V to PoE switch)       │
└───────────────────────────────────┬───────────────────────────────────────┘
                                    │
                                    │ 12V (switched)
                                    ▼
┌───────────────────────────────────────────────────────────────────────────┐
│                    LINOVISION INDUSTRIAL PoE SWITCH                       │
│                    (Gigabit, 12V DC input)                                │
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────────────┐ │
│  │  DC INPUT        UPLINK         POE OUT 1        POE OUT 2         │ │
│  │  ┌─────┐        ┌──────┐       ┌────────┐       ┌────────┐        │ │
│  │  │ 12+ │        │ RJ45 │       │  RJ45  │       │  RJ45  │        │ │
│  │  │ 12- │        │      │       │ 802.3at│       │ 802.3at│        │ │
│  │  └──┬──┘        └───┬──┘       └───┬────┘       └───┬────┘        │ │
│  └─────┼───────────────┼──────────────┼─────────────────┼────────────┘ │
│        │               │              │                 │             │
└────────┼───────────────┼──────────────┼─────────────────┼─────────────┘
         │               │              │                 │
From      │               │              │                 │
relay ────┘               │              │                 │
                          │              │                 │
              ┌───────────┘              │                 │
              │                          │                 │
              ▼                          │                 │
    ┌─────────────────┐                  │                 │
    │  Raspberry Pi 5 │                  │                 │
    │  Ethernet Port  │                  │                 │
    │                 │                  │                 │
    │  (short patch   │                  │                 │
    │   cable to      │                  │                 │
    │   uplink port)  │                  │                 │
    └─────────────────┘                  │                 │
                                         │                 │
                           ┌─────────────┘                 │
                           │                               │
                 ┌─────────┴──────────┐          ┌────────┴──────────┐
                 │  CNLINKO ETHERNET  │          │  CNLINKO ETHERNET │
                 │  BULKHEAD (IP67)   │          │  BULKHEAD (IP67)  │
                 └─────────┬──────────┘          └────────┬──────────┘
                           │                              │
                           │ Cat6 10ft cable               │ Cat6 10ft cable
                           │ (pre-terminated)              │ (pre-terminated)
                           │ (to Camera 1)                │ (to Camera 2)
                           │                              │
                 ┌─────────┴──────────┐          ┌────────┴──────────┐
                 │   ANNKE C1200     │          │   ANNKE C1200     │
                 │   Camera 1        │          │   Camera 2        │
                 │                   │          │                   │
                 │   IP: .101        │          │   IP: .102        │
                 │   12MP, PoE+      │          │   12MP, PoE+      │
                 │   Built-in IR     │          │   Built-in IR     │
                 │   IP67 sealed     │          │   IP67 sealed     │
                 └───────────────────┘          └───────────────────┘


NETWORK TOPOLOGY:
┌────────────────────────────────────────────────────────────────────────────┐
│                                                                            │
│   Pi 5 (192.168.50.1)                                                     │
│      │                                                                     │
│      │ Ethernet (to PoE switch UPLINK port)                               │
│      │                                                                     │
│      ├─────────────────────────────────────────────────────────┐          │
│      │                                                         │          │
│      │                  LINOVISION PoE Switch                  │          │
│      │                   (Layer 2 switch)                      │          │
│      │                                                         │          │
│      ├─────────────────────┬───────────────────────────────────┤          │
│      │                     │                                   │          │
│   Camera 1              Camera 2                            (LAN)        │
│   192.168.50.101        192.168.50.102                                   │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## GPIO Connections (Geekworm G469)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       GEEKWORM G469 GPIO MAP                                │
└─────────────────────────────────────────────────────────────────────────────┘

Same as Sukabumi site:

STATUS LED WIRING (12V panel-mount LEDs via relay channels):
┌────────────────────────────────────────────────────────────────────────────┐
│                                                                            │
│   12V (TB1) ──► RELAY CH2 NO ──► GREEN LED (+) ──► GND                   │
│                 GPIO 17 → IN2                                              │
│                                                                            │
│   12V (TB1) ──► RELAY CH3 NO ──► YELLOW LED (+) ──► GND                  │
│                 GPIO 27 → IN3                                              │
│                                                                            │
│   12V (TB1) ──► RELAY CH4 NO ──► RED LED (+) ──► GND                     │
│                 GPIO 22 → IN4                                              │
│                                                                            │
│   LEDs are 12V panel-mount indicators (built-in resistor).               │
│   Each LED switched by its own relay channel.                             │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘


MAINTENANCE BUTTON WIRING:
┌────────────────────────────────────────────────────────────────────────────┐
│                                                                            │
│   GPIO 23 (internal pull-up) ──► BUTTON ──► GND                           │
│                                                                            │
│   Button press: GPIO 23 goes LOW (active low)                             │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘


EXTERNAL POWER BUTTON WIRING (Pi 5 J2 Header):
┌────────────────────────────────────────────────────────────────────────────┐
│                                                                            │
│   Pi 5 J2 Header ──► IP67 MOMENTARY SWITCH ──► (loop back to J2)         │
│   (2-pin, near USB-C)   (panel-mount, 22 AWG)                            │
│                                                                            │
│   This is a DEDICATED HARDWARE power header on the Pi 5 — NOT a GPIO.    │
│   Two wires (22 AWG) from J2 pin 1 and J2 pin 2 to the switch.          │
│   Active low — button shorts the two pins together.                       │
│                                                                            │
│   Behavior:                                                                │
│   - Pi is OFF:     Brief press → powers on                                │
│   - Pi is RUNNING: Brief press → initiates clean shutdown                 │
│   - Pi is FROZEN:  Hold ~10s  → forces power off                         │
│                                                                            │
│   Separate from the maintenance pushbutton (GPIO 23).                     │
│   Maintenance button = software function (enters maintenance mode).       │
│   Power button = hardware power control (on/off/force-off).              │
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

## PTC Heater & Fan Wiring

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PTC HEATER & FAN SYSTEM                                  │
└─────────────────────────────────────────────────────────────────────────────┘

12V FROM TB1
    │
    │ [FUSE 5A]
    │
    ├──────────────────────────────────────────────────────────────┐
    │                                                              │
    ▼                                                              ▼
┌───────────────────────────────────────┐     ┌───────────────────────────────┐
│     ENCLOSURE HEATER (15W)            │     │     40 CFM FANS (×2)          │
│                                       │     │                               │
│  12V+ ──► [HYGROSTAT] ──► PTC+ ──┐    │     │  12V+ ──► Fan 1 + ──┐         │
│                             PTC  │    │     │                     │         │
│  GND ────────────────────► PTC- ─┘    │     │  12V+ ──► Fan 2 + ──┤         │
│                                       │     │                     │         │
│  Hygrostat setting: ON when >70% RH   │     │  GND ──► Fan 1/2 - ┘         │
│                                       │     │                               │
│                                       │     │  Always-on when 12V present  │
└───────────────────────────────────────┘     └───────────────────────────────┘


NOTES:
- PTC heater is self-regulating (won't overheat)
- Hygrostat controls enclosure heater based on humidity
- ANNKE C1200 cameras are factory-sealed IP67 — no camera heaters needed
- Fans provide internal air circulation
```

---

## Complete Enclosure Layout

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ENCLOSURE INTERNAL LAYOUT (Top View)                     │
│                    VEVOR NEMA 4x (16"×12"×8")                              │
└─────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────────────┐
    │ [Gore Vent]              [Puck Antenna]              [Gore Vent]       │
    │                          (12mm hole)                                    │
    │                                                                         │
    │  ┌────────────────────────────────────────────────────────────────────┐│
    │  │                     UPPER DIN RAIL                                 ││
    │  │ ┌────────┐  ┌──────────┐  ┌────────────┐  ┌────────────────────┐  ││
    │  │ │ SURGE  │  │ MEAN     │  │ TERMINAL   │  │   FUSE HOLDERS     │  ││
    │  │ │ PROT   │  │ WELL PSU │  │ BLOCK TB1  │  │   F1 F2 F3 F4      │  ││
    │  │ └────────┘  └──────────┘  └────────────┘  └────────────────────┘  ││
    │  └────────────────────────────────────────────────────────────────────┘│
    │                                                                         │
    │  ┌────────────────────────────────────────────────────────────────────┐│
    │  │                     LOWER DIN RAIL                                 ││
    │  │ ┌──────────┐  ┌───────────┐  ┌────────────┐  ┌─────────────────┐  ││
    │  │ │ PI STACK │  │ LINOVISION│  │ RELAY      │  │ DDR-60G-5       │  ││
    │  │ │ (2 HATs) │  │ PoE SWITCH│  │ MODULE     │  │ BUCK CONVERTER  │  ││
    │  │ └──────────┘  └───────────┘  └────────────┘  └─────────────────┘  ││
    │  └────────────────────────────────────────────────────────────────────┘│
    │                                                                         │
    │  ┌────────────┐  ┌────────────┐                [FAN 1]  [FAN 2]       │
    │  │ LTE MODEM  │  │  CHARGER   │                                        │
    │  │  (Velcro)  │  │            │                                        │
    │  └────────────┘  └────────────┘                                        │
    │                                                                         │
    │  [CNLINKO] [CNLINKO]                                                   │
    │   Cam1 ETH  Cam2 ETH                                                  │
    │                                                                         │
    │  [SP13]     [M16]     [PG9]    [PG9]                                   │
    │  AC in      Ground    Rain     DS18B20                                 │
    │                                                                         │
    │  ○ ○ ○   [●]    [●]                                                      │
    │  LEDs   Maint  Power                                                    │
    │  R Y G  Button Button                                                   │
    │                                                                         │
    └─────────────────────────────────────────────────────────────────────────┘

LEGEND:
○ = 10mm LED (panel mount)
● = 16mm Button (panel mount, IP67 momentary)
    Left button  = Maintenance mode (GPIO 23)
    Right button = Power on/off (Pi 5 J2 header)
[CNLINKO] = Weatherproof ethernet bulkhead connector (IP67)
[SP13] = Weatherproof DC power bulkhead connector (IP68)
[M##] = Cable gland size
[PG9] = Cable gland for sensor cables
```

---

## Grounding System

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         GROUNDING SYSTEM                                    │
└─────────────────────────────────────────────────────────────────────────────┘

                              ┌─────────────────────┐
                              │   SURGE PROTECTOR   │
                              │   PE Terminal       │
                              └──────────┬──────────┘
                                         │
                              ┌──────────┴──────────┐
                              │   GROUND BAR        │
                              │   (inside enclosure)│
                              └──────────┬──────────┘
                                         │
                              ┌──────────┴──────────┐
                              │ M16 CABLE GLAND     │
                              │ (for ground cable)  │
                              └──────────┬──────────┘
                                         │
                                         │ 6 AWG Copper
                                         │ Green/Yellow
                                         │ (~3-5m run)
                                         │
                              ┌──────────┴──────────┐
                              │   GROUND CLAMP      │
                              │   (bronze, corrosion│
                              │    resistant)       │
                              └──────────┬──────────┘
                                         │
                              ┌──────────┴──────────┐
                              │   COPPER GROUND ROD │
                              │   1.5m × 16mm       │
                              │   (driven into soil)│
                              │                     │
                              │   ════════════════  │ ◄── Ground level
                              │   ║              ║  │
                              │   ║              ║  │
                              │   ║  EARTH       ║  │
                              │   ║              ║  │
                              │   ╚══════════════╝  │
                              └─────────────────────┘

GROUND RESISTANCE: Measure with multimeter
- Target: <25Ω
- If >25Ω: Add second rod 2m away, bond together
```

---

## Wire Color Code

| Wire Color | Purpose |
|------------|---------|
| **Brown** | AC Line (Live/Hot) |
| **Blue** | AC Neutral |
| **Green/Yellow** | Earth Ground (PE) |
| **Red** | DC 12V positive (+) |
| **Black** | DC Ground / 12V negative (-) |
| **Yellow** | Signal (I2C SCL, GPIO) |
| **Blue (thin)** | Signal (I2C SDA) |
| **White** | Signal (alternate) |
| **White (22 AWG pair)** | Power button (J2 header to panel switch) |
| **Orange** | Cat6 pair 1 |

---

## Terminal Block Labels

Print and attach:

```
TB1 - MAIN 12V (from PSU / Battery)
┌────┬────┬────┬────┬────┬────┐
│12+ │12+ │12+ │12- │12- │GND │
│PSU │PoE │ Pi │PSU │RET │    │
└────┴────┴────┴────┴────┴────┘

GROUND BAR
┌────┬────┬────┬────┬────┐
│ PE │ PE │ PE │ PE │ PE │
│SURG│ENC │CAM │POLE│ROD │
└────┴────┴────┴────┴────┘
```

---

**PRINT THIS DOCUMENT - LAMINATE FOR FIELD USE**

**Document Version:** 2.1
**Last Updated:** March 12, 2026
**Changes from v2.0:**
- Added external power button wired to Pi 5 J2 header (dedicated hardware power control)
- Updated enclosure layout to show both maintenance button (GPIO 23) and power button (J2)

**Changes from v1.0:**
- Removed Victron BatteryProtect (LiFePO4 BMS has built-in cutoff)
- Removed Witty Pi 5 (Pi 5 built-in RTC sufficient for 24hr operation)
- Replaced Phoenix Contact surge protector with Heschen HS-40-N 2P
- Replaced Planet IPOE-260-12V PoE injector with LINOVISION PoE Switch + Electronics-Salon relay
- Added DDR-60G-5 buck converter (12V→5V) for Pi power
- Replaced Pi-EzConnect with Geekworm G469
- Replaced M.2 SSD with SanDisk USB flash drive
- Replaced DFRobot SEN0575 I2C rain gauge with Hydreon RG-15 UART
- Added SHT40 temp/humidity sensor and DS18B20 temperature probe
- Replaced SMA bulkheads with Proxicast puck antenna (single 12mm hole)
- Replaced M20 cable glands with CNLINKO weatherproof ethernet bulkheads
- Replaced M25 AC cable gland with SP13 DC power bulkhead
- Removed camera PTC heaters (ANNKE C1200 is IP67 factory-sealed)
- Added 40 CFM fans for internal air circulation
- Removed TB2 (no separate battery bus without BatteryProtect)
- Pi stack is 2-board (Pi 5 + G469), not 3
