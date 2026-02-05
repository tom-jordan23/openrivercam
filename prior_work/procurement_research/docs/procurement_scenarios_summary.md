# RC-Box Procurement Scenarios Summary

**Date:** December 2025
**Purpose:** Simplified sourcing strategies for humanitarian deployment

---

## Overview

Four procurement scenarios optimized for:
- **Simplified sourcing** from stable, internationally-capable suppliers
- **Solar/battery sourced locally** in deployment countries (avoids Dangerous Goods shipping)
- **Electronics from single primary supplier** with global reach

---

## Scenario Comparison

| Scenario | Primary Supplier | Solar Strategy | Suppliers | Lead Time | Cost Range | Best For |
|----------|------------------|----------------|-----------|-----------|------------|----------|
| **1: DigiKey Primary** | DigiKey (80%) | Local in-country | 2-3 | 2-4 weeks | $760-1,190 | Technical teams, global deployment |
| **2: Mouser + Victron** | Mouser (60%) + Victron | Local + Victron distributor | 3-4 | 2-4 weeks | $930-2,300 | Critical/long-term deployments |
| **3: Renogy Turnkey** | DigiKey + Renogy | Renogy complete kits | 2-3 | 2-8 weeks | $665-1,960 | US-accessible, no solar expertise |
| **4: Regional Hub** | DigiKey (pre-position) | Local in deployment region | 2-3 | 3-6 weeks | $1,086-1,441 | Multi-country humanitarian |

---

## Scenario 1: DigiKey Primary + Local Solar

**File:** `procurement_scenario_1_digikey_primary.csv`

### Strategy
- **80-90% from DigiKey** - single international supplier
- **Solar/battery locally** in deployment country
- **Amazon** for commodity items (cameras, IR lights)

### Why DigiKey
- Ships to **170+ countries**
- **8 regional support centers** (Israel, Germany, Netherlands, China, India, Hong Kong, South Korea, Japan)
- **Same-day shipping** for in-stock items
- **Excellent IP67 component selection** (Hammond enclosures, Amphenol connectors)
- 24/7 technical support

### Cost Breakdown
| Configuration | DigiKey | Local Solar | Amazon | **Total** |
|---------------|---------|-------------|--------|-----------|
| Budget (50Ah/100W) | $385 | $280 | $95 | **$760** |
| Standard (50Ah/100W) | $410 | $280 | $105 | **$795** |
| Enhanced (100Ah/200W) | $455 | $440 | $120 | **$1,015** |
| Premium (Victron) | $510 | $560 | $120 | **$1,190** |

### Key Links
- DigiKey: https://www.digikey.com
- UUGear (Witty Pi): https://www.uugear.com
- Hammond Enclosures: https://www.hammfg.com/electronics/small-case/plastic/1555f

---

## Scenario 2: Mouser + Victron Premium

**File:** `procurement_scenario_2_mouser_victron.csv`

### Strategy
- **Mouser for electronics** - Foreign Trade Zone customs pre-clearance
- **Victron via global distributor network** - premium power system
- **Local solar panels/batteries** in deployment region

### Why Victron
- **5-year warranty** - industry leading
- **VRM remote monitoring** - cloud-based system dashboard
- **Global distributor network** with local support
- **Data logging** - historical export for analysis
- Premium reliability for **5+ year deployments**

### Victron Components
| Component | Model | Price | Link |
|-----------|-------|-------|------|
| MPPT Controller | SmartSolar 100/20 | $89 | https://www.victronenergy.com/solar-charge-controllers/smartsolar-100-20 |
| MPPT Controller | SmartSolar 100/30 | $128 | https://www.victronenergy.com/solar-charge-controllers/smartsolar-100-30 |
| Battery Monitor | SmartShunt 500A | $75 | https://www.victronenergy.com/battery-monitors/smart-battery-shunt |
| System Monitor | Cerbo GX | $295 | https://www.victronenergy.com/communication-centres/cerbo-gx |

### Cost Breakdown
| Configuration | Mouser | Victron | Local | Amazon | **Total** |
|---------------|--------|---------|-------|--------|-----------|
| Standard | $420 | $165 | $260 | $85 | **$930** |
| Enhanced | $520 | $205 | $390 | $95 | **$1,210** |
| Full Monitoring | $680 | $485 | $390 | $95 | **$1,650** |
| Mission Critical | $680 | $485 | $1,040 | $95 | **$2,300** |

### Key Links
- Mouser: https://www.mouser.com
- Victron Distributors: https://www.victronenergy.com/where-to-buy
- SINES Export (EU Wholesaler): https://www.sines-export.com/victron-energy-distributor-wholesale.html

---

## Scenario 3: Renogy Turnkey Solar

**File:** `procurement_scenario_3_renogy_turnkey.csv`

### Strategy
- **Renogy complete solar kits** - plug-and-play power system
- **DigiKey for electronics**
- **No solar design expertise required**

### Why Renogy
- **Pre-matched components** - all guaranteed compatible
- **5-year product warranty** + 25-year panel performance
- **Turnkey kits** with panels, controller, cables, mounting
- Regular promotions (current: 20%+ off through Dec 15, 2025)

### Renogy Kit Options
| Kit | Contents | Price | Link |
|-----|----------|-------|------|
| Starter 200W | Panels + PWM + cables (no battery) | $200 | https://www.renogy.com/200w-12v-starter-rv-kit/ |
| Premium 400W | Panels + MPPT + smart monitoring | $580 | https://www.renogy.com/400w-12v-premium-kit-with-100a-dc-dc/ |
| Complete 400W | Panels + MPPT + 2x100Ah LiFePO4 + inverter | $1,600 | https://www.renogy.com/400w-12-volt-complete-solar-kit-with-two-100ah-lifepo4-batteries/ |
| Essential 600W | Panels + MPPT + 3.6kWh option | $1,000 | https://www.renogy.com/600w-12v-essential-off-grid-solar-kit/ |

### Limitations
- **International shipping limited** - primarily US market
- May need US forwarding service for other regions
- Battery DG shipping still applies internationally

### Cost Breakdown
| Configuration | Renogy Kit | DigiKey | Amazon | **Total** |
|---------------|------------|---------|--------|-----------|
| Budget (200W + 50Ah) | $330 | $155 | $180 | **$665** |
| Standard (400W + 100Ah) | $805 | $155 | $205 | **$1,165** |
| Complete (400W + 200Ah) | $1,600 | $155 | $205 | **$1,960** |

### Key Links
- Renogy: https://www.renogy.com
- Redodo (Budget Batteries): https://www.redodopower.com

---

## Scenario 4: Regional Hub Strategy

**File:** `procurement_scenario_4_regional_hub.csv`

### Strategy
- **Pre-position electronics** at regional logistics hubs
- **Source solar/battery locally** in each deployment country
- Optimized for **multi-country humanitarian operations**

### Suggested Regional Hubs
| Region | Hub Location | Key Suppliers |
|--------|--------------|---------------|
| East Africa | Nairobi, Kenya | African Energy, Victron distributors |
| West Africa | Lagos/Accra | Local solar, growing manufacturing |
| Southern Africa | Cape Town/Johannesburg | Renogy SA (new), Victron SA |
| Southeast Asia | Singapore/Bangkok | Strong distribution infrastructure |
| South Asia | Mumbai/Colombo | Note: India has strict import regs |
| Latin America | Miami (gateway) | US suppliers, regional distributors |

### What Ships Easily (Pre-position)
- Raspberry Pi 5 (HS 8471.50)
- USB Cameras (HS 8525.80)
- Enclosures (HS 3926.90)
- Connectors, cable glands
- Wiring, protection components
- IR illuminators

### Source Locally
- **Solar panels** - avoid tariffs, support local economy
- **LiFePO4 batteries** - avoid DG air shipping
- **Grounding rods** - too heavy/bulky to ship
- **Some mounting hardware** - stereo bar, hose clamps can be fabricated/sourced locally

### Pre-Position at Hub
- **Ball head mounts** - specialized camera hardware
- **RAM mounts** - quality swivel and pole clamps
- **DIN rail and adapters** - internal mounting
- **Industrial fasteners** - standoffs, velcro

### Cost Breakdown
| Configuration | Pre-Position | Local Source | Shipping | **Total** |
|---------------|--------------|--------------|----------|-----------|
| Budget (50Ah/100W) | $606 | $395 | $85 | **$1,086** |
| Standard (100Ah/200W) | $606 | $565 | $85 | **$1,256** |
| Enhanced (Victron) | $681 | $665 | $95 | **$1,441** |

### Key Links
- African Energy: https://www.africanenergy.com
- Victron Distributors: https://www.victronenergy.com/where-to-buy
- Eurosender (Humanitarian Logistics): https://www.eurosender.com/en/shipping-non-profit-organisations

---

## Component Availability & Alternatives

### Limited Supply Items - Alternatives Identified

| Component | Issue | Primary Alternative | Secondary Alternative |
|-----------|-------|---------------------|----------------------|
| Renogy Rover 20A MPPT | Backordered | Renogy Rover 30A | EPEver Tracer 3210AN ($120) |
| Witty Pi 4 | EU shipping only | Witty Pi 5 HAT+ ($45) | DFRobot FIT0992 ($53) |
| Arducam B0304 IP67 | May need housing | ELP 1080P IP67 ($47) | SVPRO waterproof cameras |
| PiSugar 3 Plus | NOT Pi 5 compatible | Waveshare UPS HAT (B) | DFRobot FIT0992 |
| Renogy 100Ah Pro | Some backordered | Redodo 100Ah ($225) | LiTime 100Ah ($320) |

### December 2025 Price Updates
- **Raspberry Pi 5 4GB:** $70 (+$10 increase)
- **Raspberry Pi 5 8GB:** $95 (+$15 increase)
- Driven by LPDDR4 memory costs from AI demand

---

## Supplier International Capabilities

| Supplier | Countries | Key Strength | Limitations |
|----------|-----------|--------------|-------------|
| **DigiKey** | 170+ | 8 regional centers, same-day ship | No complete solar kits |
| **Mouser** | 170+ | FTZ customs pre-clearance, 20 support centers | No complete solar kits |
| **Amazon Business** | 100+ | DDP shipping, familiar platform | Variable quality |
| **Renogy** | 100+ | Complete solar kits, warranties | US-centric shipping |
| **Victron** | Global | Premium quality, 5yr warranty | Distributor only |
| **African Energy** | Africa | 600+ partners, harsh environment proven | Regional only |

---

## Recommendation by Use Case

### For Most Humanitarian Deployments
**Use Scenario 1 (DigiKey + Local Solar)**
- Single trusted electronics source
- Excellent international shipping
- Lowest complexity
- Total cost: **$760-$1,015**

### For Critical Long-Term Deployments
**Use Scenario 2 (Mouser + Victron)**
- Premium reliability for 5+ years
- Remote monitoring via VRM
- Global service network
- Total cost: **$930-$1,650**

### For US-Based or US-Accessible Projects
**Use Scenario 3 (Renogy Turnkey)**
- No solar expertise needed
- Pre-matched compatible components
- Single solar warranty
- Total cost: **$665-$1,165**

### For Multi-Country Programs
**Use Scenario 4 (Regional Hub)**
- Pre-position at strategic hubs
- Local sourcing reduces shipping complexity
- Supports local economies
- Total cost: **$1,086-$1,441**

---

## Mounting Hardware Included

All scenarios now include comprehensive mounting sections:

### Stereo Camera Mount System
| Component | Description | Est. Cost |
|-----------|-------------|-----------|
| Aluminum Stereo Bar 300mm | 6061 aluminum baseline for dual cameras | $25 |
| Ball Head Mounts (2x) | SmallRig 1/4"-20 adjustable | $36 |
| Pan/Tilt Swivel Mount | RAM B-201U central pivot | $35-40 |
| Pole Clamp | RAM B-231ZU stainless 2-4in | $25-30 |
| Sun Shade | Aluminum visor 350mm | $20 |
| **Subtotal** | | **$141-151** |

### Enclosure Pole Mounting
| Component | Description | Est. Cost |
|-----------|-------------|-----------|
| SS Hose Clamps (4x) | 304 stainless 4-6in diameter | $16-18 |
| SS Banding Kit (alt) | For large/square poles | $35-38 |
| EPDM Pole Padding | Rubber protection strips | $12 |
| L-Brackets (pair) | Stainless 90° enclosure mount | $28-30 |
| **Subtotal** | | **$56-98** |

### Solar Panel Mounting
| Component | Description | Est. Cost |
|-----------|-------------|-----------|
| Tilt Bracket Set | Adjustable 0-60° aluminum | $35-38 |
| Pole Mount Kit (alt) | Side-of-pole for 100-200W | $55-58 |
| U-Bolts SS (4x) | Pole attachment | $20 |
| **Subtotal** | | **$55-116** |

### Internal Component Mounting
| Component | Description | Est. Cost |
|-----------|-------------|-----------|
| DIN Rail 35mm (2x) | Standard aluminum rail | $16 |
| Pi 5 DIN Mount | Adapter for Raspberry Pi | $12-15 |
| M2.5 Standoff Kit | Nylon for PCBs/HATs | $8-10 |
| Industrial Velcro | Backup retention | $12-14 |
| **Subtotal** | | **$48-55** |

**Total Mounting Hardware: ~$300-420** (varies by configuration and local sourcing)

---

## High Humidity / Tropical Climate Package

**Required for:** Indonesia, SE Asia monsoon season, Amazon basin, Congo basin, and any deployment with >80% relative humidity.

**Important:** Sealed IP67/IP68 cameras handle their own condensation. This package protects **enclosure electronics only** (Pi 5, power HAT, charge controller, relay modules).

### Why It's Needed
The Indonesia deployment revealed that **passive desiccant (silica gel) fails above 60% RH** - it saturates within days in 90%+ humidity tropical environments. Active heating is required to keep electronics above the dew point and prevent condensation damage.

### Package Components

#### Enclosure Electronics Protection System
| Component | Purpose | Cost |
|-----------|---------|------|
| Silicone Heater Pad 75x150mm 25W | 12V adhesive for compute enclosure | $22 |
| Silicone Heater Pad 100x200mm 40W | 12V for power enclosure (Config A only) | $28 |
| STC-1000 Digital Thermostat (1-2x) | Activates heater when temp <25°C | $15-30 |
| DHT22 Humidity Sensor (1-2x) | Pi monitors enclosure conditions | $8-16 |
| Molecular Sieve Type 4A 200g (2x) | Works at >90% RH (silica gel fails) | $24 |
| GORE Vent M12 (additional 1-2x) | Improves pressure equalization | $12-24 |
| Conformal Coating Spray 200ml | MG Chemicals silicone for PCB protection | $18 |
| Humidity Indicator Cards (10) | Visual check without opening | $8 |

#### Tropical Spares Kit (~$92)
| Component | Purpose | Cost |
|-----------|---------|------|
| Spare Heater Pad 75x150mm | Compute enclosure replacement | $22 |
| Spare Heater Pad 100x200mm | Power enclosure replacement (Config A) | $28 |
| Spare Desiccant 500g | 6-12 month supply | $25 |
| Spare GORE Vents (2x) | Vents clog in dusty/humid conditions | $24 |
| Spare Conformal Coating | Field reapplication after repairs | $18 |

### Total High Humidity Package

| Configuration | Description | Total Cost |
|---------------|-------------|------------|
| **Config B (Single Box)** | All electronics in one enclosure | ~$238 |
| **Config A (Two Box)** | Separate compute + power enclosures | ~$287 |

**Power Budget Impact:**
- Config B: Active heating adds **60-100 Wh/day**
- Config A: Active heating adds **80-140 Wh/day**

For tropical deployments, recommend **minimum 100W solar panel and 100Ah battery**.

### Key Suppliers
- **Amazon** (STC-1000 thermostat, silicone heater pads)
- **DigiKey** (DHT22 sensor, GORE vents, conformal coating)
- **Industrial suppliers** (molecular sieve Type 4A desiccant)

---

## Files Created

```
hardware/
├── procurement_scenario_1_digikey_primary.csv
├── procurement_scenario_2_mouser_victron.csv
├── procurement_scenario_3_renogy_turnkey.csv
├── procurement_scenario_4_regional_hub.csv
└── procurement_scenarios_summary.md (this file)
```

---

## Research Sources

Full research reports available at:
- `RC-Box_Component_Procurement_Report_2025-12.md` - Detailed component availability and pricing
- `procurement_strategy_research.md` - Supplier strategy analysis

---

*Generated December 2025*
