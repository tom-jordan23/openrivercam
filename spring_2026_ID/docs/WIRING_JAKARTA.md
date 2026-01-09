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
            │ (Type 2)      │
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
                    │                   └─────────┬─────────┘
                    │                             │
                    │                             ▼
                    │                   ┌───────────────────┐
                    │                   │ BATTERY PROTECT   │
                    │                   │ (Victron 65A)     │
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
    │  POE INJECTOR   │  │   PI 5 POWER    │  │  PTC HEATERS    │
    │  Planet         │  │   (USB-C or     │  │  (Camera +      │
    │  IPOE-260-12V   │  │   Witty Pi)     │  │   Enclosure)    │
    └────────┬────────┘  └─────────────────┘  └─────────────────┘
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
                          │ (through M25 cable gland)
                          ▼
                ┌─────────────────────┐
                │    CABLE GLAND     │
                │       M25          │
                └─────────┬──────────┘
                          │
     ┌────────────────────┼────────────────────┐
     │ L (Line/Hot)       │ N (Neutral)        │ PE (Earth/Ground)
     │ Brown              │ Blue               │ Green/Yellow
     ▼                    ▼                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                   PHOENIX CONTACT SURGE PROTECTOR                       │
│                       (Type 2, 40kA)                                    │
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
                                   │  - Over-charge      │
                                   │  - Over-current     │
                                   │  - Temperature      │
                                   └──────────┬──────────┘
                                              │
                                              ▼
                                   ┌─────────────────────┐
                                   │  VICTRON BATTERY    │
                                   │  PROTECT 65A        │
                                   │                     │
                                   │  Set: 11.0V cutoff  │
                                   │       11.5V recover │
                                   │                     │
                                   │  IN+ ◄── Battery +  │
                                   │  IN- ◄── Battery -  │
                                   │  OUT+ ──► Load +    │
                                   │  OUT- ──► Load -    │
                                   └──────────┬──────────┘
                                              │
                                              ▼
                                   ┌─────────────────────┐
                                   │  TERMINAL BLOCK     │
                                   │  TB2 (Battery 12V)  │
                                   │                     │
                                   │  Powers loads when  │
                                   │  AC fails           │
                                   └─────────────────────┘


POWER PATH LOGIC:
┌────────────────────────────────────────────────────────────────────────────┐
│                                                                            │
│  AC PRESENT:                                                               │
│  - Mean Well powers all loads directly via TB1                            │
│  - Charger maintains battery at float voltage                              │
│  - BatteryProtect passes through (battery as backup)                      │
│                                                                            │
│  AC FAILS:                                                                 │
│  - Mean Well output drops to 0V                                           │
│  - Battery discharges through BatteryProtect to TB2                       │
│  - All loads continue on battery power                                    │
│  - BatteryProtect disconnects at 11.0V to protect battery                 │
│                                                                            │
│  AC RESTORED:                                                              │
│  - Mean Well resumes powering loads                                       │
│  - Charger resumes charging battery                                       │
│  - BatteryProtect reconnects when battery >11.5V                          │
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
            │    │    └──[FUSE 10A]──► POE INJECTOR (12V+ input)
            │    │
            │    └──[FUSE 5A]──► WITTY PI 5 / PI POWER
            │
            └──[FUSE 5A]──► PTC HEATERS (via thermostat/hygrostat)


FUSE SPECIFICATIONS:
┌─────────────────────────────────────────────────────────────────────────────┐
│  FUSE        │  RATING  │  PROTECTS                                        │
├──────────────┼──────────┼────────────────────────────────────────────────────┤
│  F1 (Main)   │  15A     │  Entire 12V bus from battery/PSU                 │
│  F2 (PoE)    │  10A     │  PoE injector (60W max = 5A, plus margin)        │
│  F3 (Pi)     │  5A      │  Pi + accessories (25W max = 2A, plus margin)    │
│  F4 (Heater) │  5A      │  PTC heaters (25W max = 2A, plus margin)         │
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
│                    PLANET IPOE-260-12V                                    │
│                    (Industrial PoE Injector)                              │
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────────────┐ │
│  │  DC INPUT          DATA IN          POE OUT 1       POE OUT 2       │ │
│  │  ┌─────┐          ┌──────┐         ┌────────┐      ┌────────┐      │ │
│  │  │ 12+ │          │ RJ45 │         │  RJ45  │      │  RJ45  │      │ │
│  │  │ 12- │          │      │         │ 802.3at│      │ 802.3at│      │ │
│  │  └──┬──┘          └───┬──┘         └───┬────┘      └───┬────┘      │ │
│  └─────┼─────────────────┼────────────────┼───────────────┼───────────┘ │
│        │                 │                │               │             │
└────────┼─────────────────┼────────────────┼───────────────┼─────────────┘
         │                 │                │               │
From TB1─┘                 │                │               │
                           │                │               │
              ┌────────────┘                │               │
              │                             │               │
              ▼                             │               │
    ┌─────────────────┐                     │               │
    │  Raspberry Pi 5 │                     │               │
    │  Ethernet Port  │                     │               │
    │                 │                     │               │
    │  (short patch   │                     │               │
    │   cable)        │                     │               │
    └─────────────────┘                     │               │
                                            │               │
                              ┌─────────────┘               │
                              │                             │
                    ┌─────────┴─────────┐         ┌────────┴─────────┐
                    │  M20 CABLE GLAND  │         │  M20 CABLE GLAND │
                    └─────────┬─────────┘         └────────┬─────────┘
                              │                            │
                              │ Cat6 Outdoor               │ Cat6 Outdoor
                              │ Shielded Cable             │ Shielded Cable
                              │ (to Camera 1)              │ (to Camera 2)
                              │                            │
                    ┌─────────┴─────────┐         ┌────────┴─────────┐
                    │  IP68 RJ45 COUPLER│         │  IP68 RJ45 COUPLER│
                    │  (at camera)      │         │  (at camera)      │
                    └─────────┬─────────┘         └────────┬─────────┘
                              │                            │
                              ▼                            ▼
                    ┌─────────────────┐           ┌─────────────────┐
                    │   ANNKE C1200   │           │   ANNKE C1200   │
                    │   Camera 1      │           │   Camera 2      │
                    │                 │           │                 │
                    │   IP: .101      │           │   IP: .102      │
                    │   12MP, PoE+    │           │   12MP, PoE+    │
                    └─────────────────┘           └─────────────────┘


NETWORK TOPOLOGY:
┌────────────────────────────────────────────────────────────────────────────┐
│                                                                            │
│   Pi 5 (192.168.1.100)                                                    │
│      │                                                                     │
│      │ Ethernet (to PoE injector DATA port)                               │
│      │                                                                     │
│      ├─────────────────────────────────────────────────────────┐          │
│      │                                                         │          │
│      │                     PoE Injector                        │          │
│      │                   (Layer 2 switch)                      │          │
│      │                                                         │          │
│      ├─────────────────────┬───────────────────────────────────┤          │
│      │                     │                                   │          │
│   Camera 1              Camera 2                            (LAN)        │
│   192.168.1.101         192.168.1.102                                    │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## GPIO Connections (Pi-EzConnect)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       PI-EZCONNECT GPIO MAP                                 │
└─────────────────────────────────────────────────────────────────────────────┘

Same as Sukabumi site:

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
│   GPIO 23 (internal pull-up) ──► BUTTON ──► GND                           │
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
└────────────────────────────────────────────────────────────────────────────┘
```

---

## PTC Heater Wiring

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         PTC HEATER SYSTEM                                   │
└─────────────────────────────────────────────────────────────────────────────┘

12V FROM TB1
    │
    │ [FUSE 5A]
    │
    ├──────────────────────────────────────────────────────────────┐
    │                                                              │
    ▼                                                              ▼
┌───────────────────────────────────────┐     ┌───────────────────────────────┐
│     ENCLOSURE HEATER (15W)            │     │    CAMERA HEATERS (10W×2)     │
│                                       │     │    (if cameras need heating)  │
│  12V+ ──► [HYGROSTAT] ──► PTC+ ──┐    │     │                               │
│                             PTC  │    │     │  12V+ ──► [THERMOSTAT] ──►    │
│  GND ────────────────────► PTC- ─┘    │     │           PTC heaters ──► GND │
│                                       │     │                               │
│  Hygrostat setting: ON when >70% RH   │     │  Thermostat: ON when <25°C    │
│                                       │     │  (prevents condensation)      │
└───────────────────────────────────────┘     └───────────────────────────────┘


NOTES:
- PTC heaters are self-regulating (won't overheat)
- Hygrostat controls enclosure heater based on humidity
- Thermostat controls camera heaters based on temperature
- Both help prevent condensation in humid tropical environment
- If cameras are rated for outdoor use (ANNKE C1200), camera heaters optional
```

---

## Complete Enclosure Layout

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ENCLOSURE INTERNAL LAYOUT (Top View)                     │
│                    (400mm × 300mm × 200mm)                                  │
└─────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────────────┐
    │ [Gore Vent]              [Gore Vent]              [Gore Vent]           │
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
    │  │ │ PI STACK │  │ POE       │  │ BATTERY    │  │ TERMINAL        │  ││
    │  │ │ (3 HATs) │  │ INJECTOR  │  │ PROTECT    │  │ BLOCK TB2       │  ││
    │  │ └──────────┘  └───────────┘  └────────────┘  └─────────────────┘  ││
    │  └────────────────────────────────────────────────────────────────────┘│
    │                                                                         │
    │  ┌────────────┐  ┌────────────┐  ┌────────────┐                        │
    │  │    SSD     │  │ LTE MODEM  │  │  CHARGER   │                        │
    │  │  (Velcro)  │  │  (Velcro)  │  │            │                        │
    │  └────────────┘  └────────────┘  └────────────┘                        │
    │                                                                         │
    │                    ┌────────────────────────────┐                       │
    │                    │     LiFePO4 BATTERY        │                       │
    │                    │     100Ah (floor mount)    │                       │
    │                    └────────────────────────────┘                       │
    │                                                                         │
    │  [SMA]  [SMA]                                                           │
    │  Ant 1  Ant 2                                                           │
    │                                                                         │
    │  [M25]    [M20]    [M20]    [M16]    [PG9]                              │
    │  AC in    Cam1     Cam2     Ground   Rain                               │
    │                                                                         │
    │  ○ ○ ○   [●]                                                            │
    │  LEDs   Button                                                          │
    │  R Y G                                                                  │
    │                                                                         │
    └─────────────────────────────────────────────────────────────────────────┘

LEGEND:
○ = 10mm LED (panel mount)
● = 16mm Button (panel mount)
[M##] = Cable gland size
[SMA] = SMA bulkhead antenna connector
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
| **Orange** | Cat6 pair 1 |

---

## Terminal Block Labels

Print and attach:

```
TB1 - MAIN 12V (from PSU)
┌────┬────┬────┬────┬────┬────┐
│12+ │12+ │12+ │12- │12- │GND │
│PSU │PoE │ Pi │PSU │RET │    │
└────┴────┴────┴────┴────┴────┘

TB2 - BATTERY 12V (from BatteryProtect)
┌────┬────┬────┬────┬────┬────┐
│12+ │12+ │12- │12- │GND │GND │
│BAT │OUT │BAT │OUT │    │    │
└────┴────┴────┴────┴────┴────┘

GROUND BAR
┌────┬────┬────┬────┬────┐
│ PE │ PE │ PE │ PE │ PE │
│SURG│ENC │CAM │POLE│ROD │
└────┴────┴────┴────┴────┘
```

---

**PRINT THIS DOCUMENT - LAMINATE FOR FIELD USE**

**Document Version:** 1.0
**Last Updated:** January 9, 2026
