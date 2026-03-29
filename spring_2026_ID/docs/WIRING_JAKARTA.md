# Wiring Diagram - Jakarta Site

**Print and laminate for field reference**

---

## System Overview

```
+-----------------------------------------------------------------------------+
|                           JAKARTA SITE WIRING                               |
|                   AC Power / PoE Camera / 24hr UPS                          |
+-----------------------------------------------------------------------------+

            220V AC (Building Power)
                    |
                    v
            +---------------+
            | SURGE         |
            | PROTECTOR     |
            | (Heschen      |
            |  HS-40-N 2P)  |
            +-------+-------+
                    |
                    v
            +---------------+         +-------------------+
            | MEAN WELL     |         |                   |
            | SDR-120-12    |--12V--->|  LiFePO4 CHARGER  |
            | (120W, 12V)   |         |  (20A)            |
            +-------+-------+         +---------+---------+
                    |                           |
                    |                           v
                    |                   +-------------------+
                    |                   |  LiFePO4 BATTERY  |
                    |                   |  12V 100Ah        |
                    |                   |  (1280Wh)         |
                    |                   |  BMS built-in     |
                    |                   |  low-voltage      |
                    |                   |  cutoff           |
                    |                   +---------+---------+
                    |                             |
                    +------------+----------------+
                                 |
                                 v
                    +-----------------------------+
                    |      12V DISTRIBUTION       |
                    |      (Terminal Block)       |
                    +--------------+--------------+
                                   |
              +--------------------+--------------------+
              |                    |                    |
              v                    v                    v
    +-----------------+  +-----------------+  +-----------------+
    |  PoE SWITCH     |  |   DDR-60G-5     |  |  PTC HEATER     |
    |  LINOVISION     |  |   (12V -> 5V)   |  |  (Enclosure)    |
    |  + FUSE + RELAY |  |   -> Pi 5 GPIO  |  |  + FANS         |
    +--------+--------+  +--------+--------+  +-----------------+
                                  |
                           +------+------+
                           | Raspberry   |
                           | Pi 5        |
                           |             |    +-----------------+
                           |  J2 header -+--->| POWER BUTTON    |
                           |  (2-pin)    |    | (IP67 momentary |
                           |             |    |  panel-mount)   |
                           +-------------+    +-----------------+
             |
             v
      +----------+
      | CAMERA 1 |
      | (PoE)    |
      +----------+
```

---

## AC Power Input Detail

The surge suppressor is a PARALLEL device — it does not pass power through.
It sits across the AC line and clamps voltage spikes. The PSU and surge
suppressor both tap off the same AC bus via DIN rail terminal blocks.

DC ground (TB1) is a separate floating ground — do NOT connect DC ground to AC PE.

```
+-----------------------------------------------------------------------------+
|                         AC POWER INPUT                                      |
+-----------------------------------------------------------------------------+

                    BUILDING 220V AC
                          |
                          | L (Brown), N (Blue), PE (Green/Yellow)
                          |
                +---------------------+
                |  SP13 AC MAINS      |
                |  INPUT BULKHEAD     |
                |  (IP68)             |
                +---------+----------+
                          |
         +----------------+----------------+
         |                |                |
         | L (Brown)      | N (Blue)       | PE (Green/Yellow)
         v                v                |
  +------------+   +------------+          |
  | DIN TERM   |   | DIN TERM   |          |
  | BLOCK (L)  |   | BLOCK (N)  |          |
  | 2x bridged |   | 2x bridged |          |
  +--+--+--+---+   +--+--+--+---+          |
     |  |  |          |  |  |              |
     |  |  +-------+  |  |  +-------+     |
     |  |          |  |  |          |     |
     |  v          v  |  v          v     v
     | PSU L    SURGE  | PSU N    SURGE  SURGE
     | input    L term | input    N term PE term
     |                 |                    |
     v                 v                    v
  +---------------------------+      BUILDING GROUND
  |   MEAN WELL SDR-120-12   |      (through SP13 bulkhead)
  |   (DIN Rail Mount)       |
  |                          |
  |   AC INPUT:  L, N        |
  |   (88-264V auto-ranging) |
  |                          |
  |   DC OUTPUT:             |
  |   +-----+  +-----+      |
  |   | +V  |  | -V  |      |
  |   | 12V |  | GND |      |
  |   +--+--+  +--+--+      |
  +------+--------+----------+
         |        |
         v        v
  TO TERMINAL BLOCK TB1 (top rail)
  Red 18 AWG solid: PSU V+ --> TB1 12V+
  Black 18 AWG solid: PSU V- --> TB1 GND
  (12V DC floating ground — NOT connected to AC PE)
```

```
DIN RAIL TERMINAL BLOCK DETAIL:

Each L and N bus uses 2 DIN rail terminal blocks bridged together.
Bridge bar connects all 4 lugs electrically.

  +--------+--------+
  | BLOCK 1| BLOCK 2|          Each block has 2 lugs
  |        |        |          (left and right screw terminals)
  | L1  L2 | L3  L4 |
  +---++---+---++---+          Bridge bar
      ||           ||          connects all 4 lugs
      ++=====+====++
             |
         BRIDGE BAR
    (U-shaped metal strip,
     break to 2-segment length,
     drop into slot on top of blocks,
     tighten screw)

  L1 = AC input line (from SP13 bulkhead)
  L2 = Mean Well PSU L terminal
  L3 = Surge suppressor L terminal
  L4 = spare

  Same layout for N bus (use blue blocks).
```

---

## Battery & UPS System

```
+-----------------------------------------------------------------------------+
|                         BATTERY / UPS SYSTEM                                |
+-----------------------------------------------------------------------------+

FROM MEAN WELL 12V OUTPUT
         |
         +----------------------------------+
         |                                  |
         v                                  v
+---------------------+            +---------------------+
|  TERMINAL BLOCK     |            |  LiFePO4 CHARGER    |
|  TB1 (System 12V)   |            |  (20A, 14.6V max)   |
|                     |            |                     |
|  Powers loads when  |            |  Bulk -> Absorb ->  |
|  AC present         |            |  Float charging     |
+---------------------+            +----------+----------+
                                              |
                                              v
                                   +---------------------+
                                   |  LiFePO4 BATTERY    |
                                   |  12V 100Ah          |
                                   |  (1280Wh capacity)  |
                                   |                     |
                                   |  BMS Built-in:      |
                                   |  - Over-discharge   |
                                   |    (low-V cutoff)   |
                                   |  - Over-charge      |
                                   |  - Over-current     |
                                   |  - Temperature      |
                                   +----------+----------+
                                              |
                                              v
                                   +---------------------+
                                   |  TERMINAL BLOCK     |
                                   |  TB1 (System 12V)   |
                                   |                     |
                                   |  Battery feeds TB1  |
                                   |  when AC fails      |
                                   +---------------------+


POWER PATH LOGIC:
+----------------------------------------------------------------------------+
|                                                                            |
|  AC PRESENT:                                                               |
|  - Mean Well powers all loads directly via TB1                            |
|  - Charger maintains battery at float voltage                              |
|  - Battery on standby (BMS manages health)                                |
|                                                                            |
|  AC FAILS:                                                                 |
|  - Mean Well output drops to 0V                                           |
|  - Battery discharges through TB1 to all loads                            |
|  - BMS disconnects at low-voltage cutoff to protect battery               |
|                                                                            |
|  AC RESTORED:                                                              |
|  - Mean Well resumes powering loads                                       |
|  - Charger resumes charging battery                                       |
|  - BMS reconnects when battery recovers                                   |
|                                                                            |
+----------------------------------------------------------------------------+
```

---

## 12V Distribution

```
+-----------------------------------------------------------------------------+
|                         12V DISTRIBUTION                                    |
+-----------------------------------------------------------------------------+

                    TB1 (MAIN 12V BUS)
         +--------------------------------------+
         | 12+  12+  12+  12-  12-  12-  GND GND|
         +--+----+----+----+----+----+----+----++
            |    |    |    +----+----+----+----+--> All GND returns
            |    |    |
            |    |    +--[FUSE 5A]----> Relay CH1 COM ---> PoE SWITCH (12V)
            |    |                      (see PoE Camera System section)
            |    |
            |    +--[FUSE 5A]---> DDR-60G-5 (12V->5V) -> hardwired 5V/GND -> PI 5 GPIO
            |
            +--[FUSE 5A]---> PTC HEATER (via hygrostat) + FANS


FUSE SPECIFICATIONS (3 fuse holders):
+-----------------------------------------------------------------------------+
|  FUSE        |  RATING  |  PROTECTS                                        |
+--------------+----------+----------------------------------------------------+
|  F2 (PoE)    |  5A      |  Relay + PoE switch (1 camera, ~20W max)         |
|  F3 (Pi)     |  5A      |  DDR-60G-5 + Pi (25W max = 2A, plus margin)     |
|  F4 (Heater) |  5A      |  PTC heater + fans (25W max, plus margin)       |
+-----------------------------------------------------------------------------+
F1 (15A main bus fuse) removed — redundant with 3 branches all at 5A.
```

---

## PoE Camera System

```
+-----------------------------------------------------------------------------+
|                         POE CAMERA SYSTEM                                   |
+-----------------------------------------------------------------------------+

12V FROM TB1
    |
    | [FUSE 5A]
    |
    v
+-------------------------------------------------------------------------+
|               ELECTRONICS-SALON DIN RAIL RELAY MODULE                   |
|               (4-SPDT, GPIO-triggered via G469 breakout)                |
|                                                                         |
|  Coil power: 5V/GND from Pi via Geekworm G469 breakout                |
|    Relay VCC <- G469 Pin 4 (5V)                                        |
|    Relay GND <- G469 Pin 20 (GND)                                      |
|  Control: GPIO 24 (Pin 18) -> IN1 (PoE switch)                        |
|  ACTIVE-HIGH LOGIC (verified empirically 2026-03-26):                 |
|  GPIO HIGH = relay energized = NO contact closed = 12V passes          |
|  GPIO LOW  = relay de-energized = NO contact open = 12V cut            |
|                                                                         |
|  NOTE: ORC's orc-gpio-relays.py uses active-LOW convention             |
|  (GPIO.LOW = relay ON). Our hardware is active-HIGH. A PR will be      |
|  submitted to make ORC's relay polarity configurable.                  |
|                                                                         |
|  WHY NO (NORMALLY OPEN):                                               |
|  Fail-safe design. If Pi crashes, hangs, or hasn't booted yet,        |
|  GPIO floats LOW (or unconfigured), relay de-energizes, NO opens,     |
|  camera loses power automatically. Prevents battery drain.            |
|  NC would leave camera powered indefinitely on Pi failure.             |
|                                                                         |
|  IN (12V from fuse) --> CH1 COM --> CH1 NO --> OUT (12V to PoE switch) |
+---------------------------------+---------------------------------------+
                                  |
                                  | 12V (switched)
                                  v
+-------------------------------------------------------------------------+
|                    LINOVISION INDUSTRIAL PoE SWITCH                     |
|                    (Gigabit, 12V DC input)                              |
|                                                                         |
|  +---------------------------------------------------------------+     |
|  |  DC INPUT        UPLINK         POE OUT 1                    |     |
|  |  +-----+        +------+       +--------+                   |     |
|  |  | 12+ |        | RJ45 |       |  RJ45  |                   |     |
|  |  | 12- |        |      |       | 802.3at|                   |     |
|  |  +--+--+        +---+--+       +---+----+                   |     |
|  +-----+---------------+-------------+-------------------------+     |
|        |               |              |                              |
+--------+---------------+--------------+------------------------------+
         |               |              |
From      |               |              |
relay ----+               |              |
                          |              |
              +-----------+              |
              |                          |
              v                          |
    +-----------------+                  |
    |  Raspberry Pi 5 |                  |
    |  Ethernet Port  |                  |
    |                 |                  |
    |  (short patch   |                  |
    |   cable to      |                  |
    |   uplink port)  |                  |
    +-----------------+                  |
                                         |
                           +-------------+
                           |
                 +---------+----------+
                 |  CNLINKO ETHERNET  |
                 |  BULKHEAD (IP67)   |
                 +---------+----------+
                           |
                           | Cat6 10ft cable
                           | (pre-terminated)
                           | (to Camera 1)
                           |
                 +---------+----------+
                 |   ANNKE C1200     |
                 |   Camera 1        |
                 |                   |
                 |   IP: .101        |
                 |   12MP, PoE+      |
                 |   Built-in IR     |
                 |   IP67 sealed     |
                 +-------------------+


NETWORK TOPOLOGY:
+----------------------------------------------------------------------------+
|                                                                            |
|   Pi 5 (192.168.50.1)                                                     |
|      |                                                                     |
|      | Ethernet (to PoE switch UPLINK port)                               |
|      |                                                                     |
|      +-----------------------------------------------------+             |
|      |                                                       |             |
|      |                  LINOVISION PoE Switch                |             |
|      |                   (Layer 2 switch)                    |             |
|      |                                                       |             |
|      +---------------------+                             |  |             |
|      |                     |                             |  |             |
|   Camera 1              (LAN)                               |             |
|   192.168.50.101                                             |             |
|                                                                            |
+----------------------------------------------------------------------------+
```

---

## GPIO Connections (Geekworm G469)

```
+-----------------------------------------------------------------------------+
|                       GEEKWORM G469 GPIO MAP                                |
+-----------------------------------------------------------------------------+

RELAY MODULE INPUT WIRING:
+----------------------------------------------------------------------------+
|                                                                            |
|   G469 Pin 4  (5V)      ---> Relay VCC                                    |
|   G469 Pin 20 (GND)     ---> Relay GND                                    |
|   G469 Pin 18 (GPIO 24) ---> Relay IN1  (PoE switch)                     |
|   G469 Pin 11 (GPIO 17) ---> Relay IN2  (Green LED)                      |
|   G469 Pin 13 (GPIO 27) ---> Relay IN3  (Yellow LED)                     |
|   G469 Pin 15 (GPIO 22) ---> Relay IN4  (Red LED)                        |
|                                                                            |
+----------------------------------------------------------------------------+


STATUS LED WIRING (12V panel-mount LEDs via relay channels):
+----------------------------------------------------------------------------+
|                                                                            |
|   12V (TB1) ---> RELAY CH2 COM ---> CH2 NO ---> GREEN LED (+) ---> GND   |
|                 GPIO 17 -> IN2                                             |
|                                                                            |
|   12V (TB1) ---> RELAY CH3 COM ---> CH3 NO ---> YELLOW LED (+) ---> GND  |
|                 GPIO 27 -> IN3                                             |
|                                                                            |
|   12V (TB1) ---> RELAY CH4 COM ---> CH4 NO ---> RED LED (+) ---> GND     |
|                 GPIO 22 -> IN4                                             |
|                                                                            |
|   LEDs are 12V panel-mount indicators (built-in resistor).               |
|   Each LED switched by its own relay channel.                             |
|                                                                            |
+----------------------------------------------------------------------------+


MAINTENANCE BUTTON WIRING:
+----------------------------------------------------------------------------+
|                                                                            |
|   GPIO 23 (Pin 16, internal pull-up) ---> BUTTON ---> GND (Pin 14)       |
|                                                                            |
|   Button press: GPIO 23 goes LOW (active low)                             |
|                                                                            |
+----------------------------------------------------------------------------+


EXTERNAL POWER BUTTON WIRING (Pi 5 J2 Header):
+----------------------------------------------------------------------------+
|                                                                            |
|   Pi 5 J2 Header ---> IP67 MOMENTARY SWITCH ---> (loop back to J2)       |
|   (2-pin, near USB-C)   (panel-mount)                                     |
|                                                                            |
|   J2 is UNPOPULATED (bare through-holes). Use bolt-through method:       |
|   M2 bolt through each hole, O-ring terminal crimp on 18 AWG solid wire, |
|   secured with nut. Alternative: solder a 2-pin 2.54mm header.           |
|                                                                            |
|   This is a DEDICATED HARDWARE power header on the Pi 5 -- NOT a GPIO.   |
|   Active low -- button shorts the two pins together.                      |
|                                                                            |
|   Behavior:                                                                |
|   - Pi is OFF:     Brief press -> powers on                               |
|   - Pi is RUNNING: Brief press -> initiates clean shutdown                |
|   - Pi is FROZEN:  Hold ~10s  -> forces power off                        |
|                                                                            |
|   Separate from the maintenance pushbutton (GPIO 23).                     |
|   Maintenance button = software function (enters maintenance mode).       |
|   Power button = hardware power control (on/off/force-off).              |
|                                                                            |
+----------------------------------------------------------------------------+


RAIN GAUGE WIRING (UART via SD16 4-pin bulkhead connector):
+----------------------------------------------------------------------------+
|                                                                            |
|   OUTSIDE (18/4 stranded jacketed cable, bulkhead plug to RG-15):        |
|                                                                            |
|   SD16 Pin 1 (12V)   <--- 18/4 cable ---> RG-15 red    (VIN)            |
|   SD16 Pin 2 (GND)   <--- 18/4 cable ---> RG-15 black  (GND)            |
|   SD16 Pin 3 (TX>RX) <--- 18/4 cable ---> RG-15 green  (RX)             |
|   SD16 Pin 4 (RX>TX) <--- 18/4 cable ---> RG-15 yellow (TX)             |
|                                                                            |
|   INSIDE (solid core 22 AWG, bulkhead socket to G469/TB1):              |
|                                                                            |
|   SD16 Pin 1 (12V)   ---> TB1 12V output                                 |
|   SD16 Pin 2 (GND)   ---> G469 Pin 9  (GND)                             |
|   SD16 Pin 3 (TX>RX) ---> G469 Pin 8  (GPIO 14 / TXD)                   |
|   SD16 Pin 4 (RX>TX) ---> G469 Pin 10 (GPIO 15 / RXD)                   |
|                                                                            |
|   No level shifter needed. RG-15 signal is 3.3V TTL.                     |
|   SD16 contacts require solder termination.                               |
|   No-solder alternative: PG9 cable gland (pigtail passes through         |
|   directly, but requires opening enclosure to disconnect gauge).          |
|                                                                            |
+----------------------------------------------------------------------------+


SHT40 TEMPERATURE/HUMIDITY SENSOR (I2C):
+----------------------------------------------------------------------------+
|                                                                            |
|   SHT40 (I2C addr 0x44)     Geekworm G469                                |
|   +------------------+       +---------------+                             |
|   |  VCC             |-------|    3V3        |                             |
|   |  GND             |-------|    GND        |                             |
|   |  SDA             |-------|  GPIO 2/SDA   |                             |
|   |  SCL             |-------|  GPIO 3/SCL   |                             |
|   +------------------+       +---------------+                             |
|                                                                            |
|   STEMMA QT to bare wire cable (200mm). Inside enclosure.                |
|   Mount with double-sided tape to a nearby DIN-mounted component's       |
|   carrier tray. Position away from heat sources.                          |
|                                                                            |
+----------------------------------------------------------------------------+


DS18B20 WATERPROOF TEMPERATURE PROBE (1-Wire):
+----------------------------------------------------------------------------+
|                                                                            |
|   3.3V --[4.7k]--+-- GPIO 4 (Pin 7, 1-Wire data)                        |
|                    |                                                       |
|                    |   +------------------------+                          |
|                    +---|  DS18B20 Waterproof     |                          |
|                    |   |  Temperature Probe      |                          |
|                    |   |  (stainless, 1m cable)  |                          |
|   GND -------------+---|                         |                          |
|                    |   |  OUTSIDE enclosure      |                          |
|                    |   |  (through PG9 gland)    |                          |
|                    |   +------------------------+                          |
|                    |                                                       |
|                    +-- Pull-up resistor on Geekworm G469 terminals        |
|                                                                            |
+----------------------------------------------------------------------------+
```

---

## PTC Heater & Fan Wiring

```
+-----------------------------------------------------------------------------+
|                    PTC HEATER & FAN SYSTEM                                  |
+-----------------------------------------------------------------------------+

12V FROM TB1
    |
    | [FUSE 5A]
    |
    +--------------------------------------------------------------+
    |                                                              |
    v                                                              v
+---------------------------------------+     +-------------------------------+
|     ENCLOSURE HEATER (15W)            |     |     40 CFM FANS (x2)         |
|                                       |     |                               |
|  12V+ --> [HYGROSTAT] --> PTC+ --+    |     |  12V+ --> Fan 1 + --+         |
|                             PTC  |    |     |                     |         |
|  GND -----------------> PTC- -+  |    |     |  12V+ --> Fan 2 + --+         |
|                                       |     |                     |         |
|  Hygrostat setting: ON when >70% RH   |     |  GND --> Fan 1/2 - +         |
|                                       |     |                               |
|                                       |     |  Always-on when 12V present  |
+---------------------------------------+     +-------------------------------+


NOTES:
- PTC heater is self-regulating (won't overheat)
- Hygrostat controls enclosure heater based on humidity
- ANNKE C1200 camera is factory-sealed IP67 -- no camera heater needed
- Fans provide internal air circulation
```

---

## Complete Enclosure Layout

```
+-----------------------------------------------------------------------------+
|                    ENCLOSURE INTERNAL LAYOUT (Top View)                     |
|                    VEVOR NEMA 4x (16"x12"x8")                              |
+-----------------------------------------------------------------------------+

    +---------------------------------------------------------------------+
    | [Gore Vent]              [Puck Antenna]              [Gore Vent]     |
    |                          (12mm hole)                                  |
    |                                                                       |
    |  +------------------------------------------------------------------+|
    |  |                     UPPER DIN RAIL                                ||
    |  | +--------+  +----------+  +------------+  +--------------------+ ||
    |  | | SURGE  |  | MEAN     |  | TERMINAL   |  |   FUSE HOLDERS    | ||
    |  | | PROT   |  | WELL PSU |  | BLOCK TB1  |  |   F1 F2 F3 F4    | ||
    |  | +--------+  +----------+  +------------+  +--------------------+ ||
    |  +------------------------------------------------------------------+|
    |                                                                       |
    |  +------------------------------------------------------------------+|
    |  |                     LOWER DIN RAIL                                ||
    |  | +----------+  +-----------+  +------------+  +-----------------+ ||
    |  | | PI STACK |  | LINOVISION|  | RELAY      |  | DDR-60G-5       | ||
    |  | | (2 HATs) |  | PoE SWITCH|  | MODULE     |  | BUCK CONVERTER  | ||
    |  | +----------+  +-----------+  +------------+  +-----------------+ ||
    |  +------------------------------------------------------------------+|
    |                                                                       |
    |  +------------+  +------------+                [FAN 1]  [FAN 2]      |
    |  | LTE MODEM  |  |  CHARGER   |                                      |
    |  |  (Velcro)  |  |            |                                      |
    |  +------------+  +------------+                                      |
    |                                                                       |
    |  [CNLINKO]                                                            |
    |   Cam1 ETH                                                           |
    |                                                                       |
    |  [SP13]     [M16]     [SD16]    [PG9]                                |
    |  AC in      Ground    Rain      DS18B20                              |
    |                       Gauge                                           |
    |                                                                       |
    |  o o o   [*]    [*]                                                   |
    |  LEDs   Maint  Power                                                  |
    |  R Y G  Button Button                                                 |
    |                                                                       |
    +---------------------------------------------------------------------+

LEGEND:
o = 10mm LED (panel mount)
* = Pushbutton (panel mount, IP67 momentary NO)
    Left button  = Maintenance mode (GPIO 23)
    Right button = Power on/off (Pi 5 J2 header)
[CNLINKO] = Weatherproof ethernet bulkhead connector (IP67)
[SP13] = Weatherproof AC mains input bulkhead connector (IP68, 220V AC)
[SD16] = Weatherproof 4-pin bulkhead connector (IP68, rain gauge)
[M##] = Cable gland size
[PG9] = Cable gland for DS18B20 temperature probe
```

---

## Grounding System

```
+-----------------------------------------------------------------------------+
|                         GROUNDING SYSTEM                                    |
+-----------------------------------------------------------------------------+

                              +---------------------+
                              |   SURGE PROTECTOR   |
                              |   PE Terminal       |
                              +----------+----------+
                                         |
                              +----------+----------+
                              |   GROUND BAR        |
                              |   (inside enclosure)|
                              +----------+----------+
                                         |
                              +----------+----------+
                              | M16 CABLE GLAND     |
                              | (for ground cable)  |
                              +----------+----------+
                                         |
                                         | 6 AWG Copper
                                         | Green/Yellow
                                         | (~3-5m run)
                                         |
                              +----------+----------+
                              |   GROUND CLAMP      |
                              |   (bronze, corrosion|
                              |    resistant)       |
                              +----------+----------+
                                         |
                              +----------+----------+
                              |   COPPER GROUND ROD |
                              |   1.5m x 16mm       |
                              |   (driven into soil)|
                              |                     |
                              |   ================  | <-- Ground level
                              |   ||            ||  |
                              |   ||            ||  |
                              |   ||  EARTH     ||  |
                              |   ||            ||  |
                              |   +============+|  |
                              +---------------------+

GROUND RESISTANCE: Measure with multimeter
- Target: <25 ohm
- If >25 ohm: Add second rod 2m away, bond together
```

---

## Wire Routing

Route all DC low-voltage wires (5V power, GPIO signals, sensor cables)
**over the top of the upper DIN rail**. AC mains wiring (L, N, PE) runs
**between the two rails** only. This physical separation:
- Prevents accidental contact between 220V AC and DC during service
- Makes each voltage domain visually distinct and easy to trace
- Reduces the chance of a wiring error during future maintenance

```
  [UPPER RAIL — 12V DC components]
         --- DC low-voltage wires route OVER the top ---

         --- AC mains wires route BETWEEN rails only ---

  [LOWER RAIL — AC power components]
```

---

## Wire Gauge Spec

| Domain | Gauge | Type | Standard |
|--------|-------|------|----------|
| AC mains (L, N, PE) | 2.5 mm² / 14 AWG minimum | Stranded | IEC 60364, Indonesian SNI 04-0225 |
| DC 12V internal | 18-22 AWG | Solid core | — |
| DC 5V / GPIO signal | 22 AWG | Solid core | — |

Do not use wire thinner than 1.5 mm² (16 AWG) for any AC connection.

---

## Wire Color Code

| Wire Color | Purpose |
|------------|---------|
| **Brown** | AC Line (Live/Hot) |
| **Blue** | AC Neutral |
| **Green/Yellow** | Earth Ground (PE) |
| **Red** | DC 12V positive (+) |
| **Black** | DC Ground / 12V negative (-) |
| **Yellow** | 5V power (DDR-60G-5 -> Pi, and Pi -> relay VCC) |
| **Blue (thin)** | Signal (I2C SDA) |
| **White** | Signal (alternate) |
| **White (22 AWG pair)** | Power button (J2 header to panel switch) |
| **Orange** | Cat6 pair 1 |

---

## Terminal Block Labels

Print and attach:

```
TB1 - MAIN 12V (from PSU / Battery)
+----+----+----+----+----+----+
|12+ |12+ |12+ |12- |12- |GND |
|PSU |PoE | Pi |PSU |RET |    |
+----+----+----+----+----+----+

GROUND BAR
+----+----+----+----+----+
| PE | PE | PE | PE | PE |
|SURG|ENC |CAM |POLE|ROD |
+----+----+----+----+----+
```

---

**PRINT THIS DOCUMENT - LAMINATE FOR FIELD USE**

**Document Version:** 3.1
**Last Updated:** March 26, 2026
**Changes from v3.0:**
- Reduced Jakarta from 2 cameras to 1 camera
- Removed Camera 2 from all diagrams and network topology
- Reduced CNLINKO ethernet bulkheads from 2 to 1 in enclosure layout
- Reduced PoE fuse F2 from 10A to 5A (1 camera draws less current)

**Changes from v2.1:**
- Fixed relay pin assignments: VCC to G469 Pin 4 (5V), GND to G469 Pin 20 (avoids doubling up wires in screw terminals)
- Fixed SP13 bulkhead labeling: "SP13 AC MAINS INPUT BULKHEAD" (carries 220V AC, not DC)
- Added inline fuse between TB1 and relay CH1 COM in PoE camera system diagram
- Changed rain gauge from PG9 cable gland to SD16 4-pin IP68 bulkhead connector with 18/4 stranded jacketed external cable
- Changed "Yellow" wire color from "Signal (I2C SCL, GPIO)" to "5V power" to match Sukabumi convention
- Added NO vs NC fail-safe explanation in PoE camera system section
- Added relay module input wiring section with explicit pin assignments
- Updated J2 power button section with pogo pin method and hot glue note
- Updated SHT40 section with mounting note
- Updated enclosure layout to show SD16 rain gauge connector

**Changes from v2.0:**
- Added external power button wired to Pi 5 J2 header (dedicated hardware power control)
- Updated enclosure layout to show both maintenance button (GPIO 23) and power button (J2)

**Changes from v1.0:**
- Removed Victron BatteryProtect (LiFePO4 BMS has built-in cutoff)
- Removed Witty Pi 5 (Pi 5 built-in RTC sufficient for 24hr operation)
- Replaced Phoenix Contact surge protector with Heschen HS-40-N 2P
- Replaced Planet IPOE-260-12V PoE injector with LINOVISION PoE Switch + Electronics-Salon relay
- Added DDR-60G-5 buck converter (12V->5V) for Pi power
- Replaced Pi-EzConnect with Geekworm G469
- Replaced M.2 SSD with SanDisk USB flash drive
- Replaced DFRobot SEN0575 I2C rain gauge with Hydreon RG-15 UART
- Added SHT40 temp/humidity sensor and DS18B20 temperature probe
- Replaced SMA bulkheads with Proxicast puck antenna (single 12mm hole)
- Replaced M20 cable glands with CNLINKO weatherproof ethernet bulkheads
- Replaced M25 AC cable gland with SP13 AC mains input bulkhead
- Removed camera PTC heaters (ANNKE C1200 is IP67 factory-sealed)
- Added 40 CFM fans for internal air circulation
- Removed TB2 (no separate battery bus without BatteryProtect)
- Pi stack is 2-board (Pi 5 + G469), not 3
