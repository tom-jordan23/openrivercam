# DIN Rail Mounting Clips & Adapters Research

**Date:** March 2, 2026
**Purpose:** Select generic DIN rail mounting solutions for miscellaneous components (LTE modem, small PCBs, etc.)
**Constraint:** No soldering, available on Amazon

---

## Recommendations

### 1. C45 PCB Clip-Pairs (For Bare PCBs)

**Molence 10 Sets C45 PCB DIN Rail Mounting Adapter**

| Spec | Value |
|------|-------|
| Amazon | B09KZHY8G4 |
| Price | ~$8-10 |
| Pack | 10 sets (20 clips + 40 screws) |
| Material | PA66 flame-retardant nylon |
| Rail compatibility | 35mm and 15mm DIN rail |
| Max PCB width | 100mm |

PCB edges slide into opposing clips that snap onto the DIN rail. Optional screw locks the board in place. Works for relay modules, breakout boards, and any PCB with clean edges.

### 2. Aluminum Snap-On Clips (For Arbitrary Items)

**CNQLIS 1.65" Width Aluminum DIN Rail Mounting Clips — 10-pack**

| Spec | Value |
|------|-------|
| Amazon | B0CJJ1DBZM |
| Price | ~$12-15 |
| Pack | 10 clips |
| Material | Aluminum alloy, oxidation sandblasted |
| Face width | 1.65" (42mm) |
| Mounting holes | Countersunk M3 |

Snap onto DIN rail, then attach components to the face using screws, zip ties, or Velcro through the countersunk holes. Two clips used together (top and bottom) with a zip tie can hold USB dongles, enclosed modules, or any oddball item.

---

## Alternatives Evaluated

### Winford Engineering Pre-Drilled Plates
- **2.2" x 4.0"** (B083X66YKK, ~$10-13) — FR4 plate with steel DIN clip, pre-drilled hole grid
- **4.0" x 4.0"** (B07ND1P6V4, ~$12-16) — larger version for multiple components
- **4.0" x 6.0"** (B083XQ9KTC, ~$14-18) — largest, for sub-assemblies
- Premium option with steel DIN bracket. Best if you need a proper flat mounting surface. Overkill for simple clip jobs but excellent for the LTE modem + USB adapter assembly if the aluminum clips aren't sufficient.

### DINrPlate Universal (B09DCDCJCX, ~$12-18)
- Adjustable sliding standoffs fit various PCB hole patterns (19x15mm to 99x64mm)
- Requires the PCB to have mounting holes — won't work for devices in plastic housings
- Good for SBCs but less versatile than clip-pairs or aluminum clips for random items

### Electronics-Salon 5 Sets DIN Rail Adapter (B00U6W7Y3I, ~$10-13)
- Same clip-pair concept as Molence but from a more established brand
- Works on 35mm, 32mm, and 15mm rails
- Slightly more expensive per set than Molence

### UM100S DIN Rail PCB Enclosure (B0G9M285Y3, ~$8-20)
- Snap-together plastic enclosure that mounts on DIN rail
- PCB slides into internal rails
- Requires PCB to be close to 100mm wide — not suitable for small modules

---

## What to Use Where

| Component | Mounting Solution |
|-----------|------------------|
| LTE modem + USB adapter | Aluminum clip pair with zip tie, or Winford plate |
| GPIO breakout board | C45 PCB clip-pair |
| Small relay modules | C45 PCB clip-pair |
| USB hub or dongle | Aluminum clip with zip tie |
| Fuse holders | Aluminum clip with screw |
| Anything with mounting holes | Aluminum clip or Winford plate with standoffs |
