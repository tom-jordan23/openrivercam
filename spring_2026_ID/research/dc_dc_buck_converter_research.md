# DC-DC Buck Converter Research: Solar River Monitoring Station

**Date:** March 2, 2026
**Purpose:** Select DIN-rail-mountable DC-DC buck converters to power the Sukabumi and Jakarta monitoring stations from 12V battery systems
**Constraint:** No soldering - screw terminal connections only

---

## Requirements

### Input
- 12V LiFePO4 battery (operating range 10.5-14.6V)

### Outputs Needed

| Rail | Loads | Min Current |
|------|-------|-------------|
| **12V regulated** | PoE injector/switch + camera | 2-3A |
| **5V** | Raspberry Pi 5, USB cell modem, GPIO LEDs, rain sensor | 5A+ |

**Note:** The cell modem and LEDs are powered via the Pi's USB and GPIO, so they load the 5V rail, not the 12V rail.

### Form Factor
- DIN rail mountable (built-in or with compatible clip)
- Available on Amazon
- Screw terminals (no soldering)

---

## Recommendation: Mean Well DDR-60G Pair

Two separate single-output DIN-rail converters mounted side by side. No single DIN-rail converter provides both 12V and 5V at the required currents.

### DDR-60G-5 (5V Rail)

| Spec | Value |
|------|-------|
| Output | 5V @ 10.8A (54W) |
| Input | 9-36V DC (covers 12V LiFePO4 range) |
| DIN rail | Built-in mount |
| Connections | Screw terminals |
| Protections | Short circuit, overload, overvoltage, reverse polarity |
| Operating temp | -40 to +85C |
| Isolation | 4KV I/O |
| Width | 52.5mm (3 DIN units) |
| Amazon | Yes - search "DDR-60G-5" or ASIN B07B64RCTR |
| Price | ~$36-42 |

### DDR-60G-12 (12V Rail)

| Spec | Value |
|------|-------|
| Output | 12V @ 5A (60W) |
| Input | 9-36V DC (covers 12V LiFePO4 range) |
| DIN rail | Built-in mount |
| Connections | Screw terminals |
| Protections | Short circuit, overload, overvoltage, reverse polarity |
| Operating temp | -40 to +85C |
| Isolation | 4KV I/O |
| Width | 52.5mm (3 DIN units) |
| Amazon | Yes - search "DDR-60G-12" or ASIN B07W8YFBGD |
| Price | ~$36-42 |

### Combined Specs

| Metric | Value |
|--------|-------|
| Total DIN rail width | ~105mm (6 DIN units) |
| Total cost | ~$72-84 |
| Combined power capacity | 114W (54W + 60W) |

---

## Load Analysis

### 12V Rail (DDR-60G-12: 5A / 60W capacity)

| Load | Estimated Draw |
|------|---------------|
| PoE injector + camera | 1.0-2.5A |
| **Total** | **1.0-2.5A** |

The 12V rail runs at partial load (20-50% capacity). The DDR-60G-12 is the smallest Mean Well DIN-mount option in the DDR-G series, so it can't be downsized. The headroom means it runs cool and efficiently.

### 5V Rail (DDR-60G-5: 10.8A / 54W capacity)

| Load | Estimated Draw |
|------|---------------|
| Raspberry Pi 5 (under load) | 3.0-5.0A |
| Cell modem (USB) | 0.5-2.0A |
| Rain sensor | 0.05-0.1A |
| GPIO LEDs | 0.02-0.06A |
| **Total** | **3.6-7.2A** |

The 5V rail runs at 33-67% capacity, providing adequate margin for peak loads.

---

## Alternatives Evaluated

### TDK-Lambda DPX4024T0512 (Single-Unit Triple Output)
- **Input:** 18-36V (won't work with 12V battery)
- **5V rail:** 6A (marginal)
- **12V rail:** 1A (insufficient for PoE)
- **Verdict:** Does not meet requirements

### eletechsup DD32AJ4B (Budget 4-Channel)
- **5V rail:** 3A max (insufficient for Pi)
- **12V rail:** 3A max (can't produce 12V from 12V input - buck topology)
- **Verdict:** Underpowered, consumer-grade, not suitable for remote deployment

### eletechsup DDIS24QC (Single-Output Isolated)
- **5V version:** 2A (insufficient)
- **12V version:** 1.3A (insufficient)
- **Verdict:** Current ratings far too low

### PULS SLD2.100 (Premium Industrial)
- **Output:** 5V @ 8A (good)
- **Availability:** Not on Amazon (DigiKey/Mouser only)
- **Price:** ~$100-140
- **Verdict:** Premium but not Amazon-available, single-output only

---

## Mean Well Model Suffix Reference

The "G" suffix is critical - it determines input voltage range.

| Suffix | Input Range | Battery Match |
|--------|------------|---------------|
| -G | 9-36V | 12V or 24V |
| -L | 18-75V | 24V or 48V |
| -A (DDR-120) | 9-18V | 12V only |
| -B (DDR-120) | 16.8-33.6V | 24V only |
| -C (DDR-120) | 33.6-67.2V | 48V only |

---

## Why Two Units Instead of One

No single commodity DIN-rail DC-DC converter provides both 12V and 5V at the required currents. The Mean Well DDR-60G pair is the standard industrial approach: proven, well-documented, and widely available. The two units share the same battery input bus and mount side by side on the same DIN rail.
