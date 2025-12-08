# RC-Box Bill of Materials: Single-Supplier Analysis

**Document Date:** December 7, 2025
**Objective:** Determine feasibility of sourcing all RC-Box components from a single supplier (Mouser or DigiKey)

---

## Executive Summary

**Finding: Neither Mouser nor DigiKey can supply a complete RC-Box BOM.**

| Metric | Mouser | DigiKey |
|--------|--------|---------|
| **Component Types Covered** | ~40-50% | ~68% |
| **Cost Coverage** | ~20-30% | ~35-40% |
| **Best Categories** | Electronic components, connectors, terminal blocks | Raspberry Pi, enclosures, cable glands |
| **Critical Gaps** | Cameras, batteries, solar, Pi, enclosures | Cameras, batteries, solar, IR illuminators |

**Recommendation:** Use a **hybrid procurement strategy** with 3-4 suppliers:
1. **Primary Electronics:** DigiKey OR Mouser (choose one)
2. **Solar/Battery:** Renogy, Victron, or Amazon
3. **Cameras:** Specialized industrial camera supplier or Amazon
4. **Security/IR:** Amazon or security equipment distributor

---

## Complete BOM: Component-by-Component Availability

### Category 1: Core Computing

| Component | Spec | Mouser | DigiKey | Best Source |
|-----------|------|--------|---------|-------------|
| Raspberry Pi 5 8GB | Main compute | Limited | **IN STOCK (SC1112)** | DigiKey |
| Raspberry Pi 5 4GB | Alternative | Limited | **IN STOCK (SC1111)** | DigiKey |
| Witty Pi 4 HAT | Power management | ❌ No | Limited (Adafruit) | UUGear direct |
| MicroSD 64GB Industrial | Storage | Limited | **Kingston SDCE/64GB** | DigiKey |
| M.2 NVMe SSD 512GB | Extended storage | ❌ No | ❌ No | Amazon/Newegg |
| 4G LTE USB Modem | Connectivity | ❌ No | Limited (Sixfab) | Amazon |
| USB 3.0 Powered Hub | If needed | ❌ No | ❌ No | Amazon |

### Category 2: Power System

| Component | Spec | Mouser | DigiKey | Best Source |
|-----------|------|--------|---------|-------------|
| LiFePO4 Battery 12V 50Ah | Energy storage | ❌ No | ❌ No | Renogy/BattleBorn |
| MPPT Charge Controller | Solar charging | ❌ No | ❌ No | Victron/Renogy |
| Solar Panel 100W | Power generation | ❌ No | ❌ No | Local/Renogy |
| DC-DC Buck 12V→5V 5A | Pi power | **RECOM R-78E** | **TI/Diodes Inc** | Either |
| 5A Polyfuse PTC | Protection | **Littelfuse** | **Littelfuse/Eaton** | Either |
| TVS Diode 5.5V | Surge protection | **Bourns SMAJ5.0A** | **Bourns/Nexperia** | Either |
| 1N4007 Diodes (5x) | Flyback protection | **✓ Multiple** | **✓ Multiple** | Either |

### Category 3: Enclosures & Sealing

| Component | Spec | Mouser | DigiKey | Best Source |
|-----------|------|--------|---------|-------------|
| IP67 Enclosure 200x150x100mm | Compute box | Limited | **Rose/BUD** | DigiKey |
| IP67 Enclosure 300x250x150mm | Power box | Limited | **Rose/BUD** | DigiKey |
| IP67 Enclosure 400x300x200mm | Combined | Limited | **Rose/BUD** | DigiKey |
| M12 IP68 Cable Glands (4x) | 3-6mm cables | **HARTING** | **Amphenol** | Either |
| M16 IP68 Cable Glands (6x) | 4-8mm cables | **HARTING** | **Amphenol** | Either |
| M20 IP68 Cable Glands (5x) | 6-12mm cables | **HARTING** | **Amphenol** | Either |
| M16 IP68 Blanking Plugs (4x) | Unused holes | **✓ Available** | **✓ Available** | Either |
| GORE Vent M12 (2x) | Pressure equalization | Limited | **Amphenol LTW** | DigiKey |
| SMA Bulkhead IP67 (2x) | Antenna pass-through | **Amphenol RF** | **Amphenol RF** | Either |

### Category 4: Cameras & Cabling

| Component | Spec | Mouser | DigiKey | Best Source |
|-----------|------|--------|---------|-------------|
| IP67 USB Camera w/IR (2x) | Video capture | ❌ No | ❌ No | ELP/SVPRO (Amazon) |
| USB Active Extension 10m (2x) | Camera cables | ❌ No | **Tripp Lite U330-10M-1** | DigiKey |
| IP67 USB Bulkhead (2x) | Panel mount | Limited | **Conec/Same Sky** | DigiKey |
| Camera Mounting Brackets (2x) | Adjustable | ❌ No | ❌ No | Amazon |

### Category 5: IR Spotlight System

| Component | Spec | Mouser | DigiKey | Best Source |
|-----------|------|--------|---------|-------------|
| 850nm IR Flood 20W 12V (1-2x) | Night illumination | ❌ No | ❌ No | Amazon (OOSSXX) |
| 5V Relay Module SPDT 10A | Pi-triggered control | **Omron/Panasonic** | **Omron/TE** | Either |
| 12V Photoresistor Relay | Light-sensing | ❌ No | ❌ No | Amazon (XH-M131) |

### Category 6: Electrical Components

| Component | Spec | Mouser | DigiKey | Best Source |
|-----------|------|--------|---------|-------------|
| DIN Rail 35mm 200mm (2x) | Internal mounting | **✓ Available** | **Phoenix/TE** | Either |
| DIN Rail Terminal 10A (6x) | DC distribution | **Phoenix Contact** | **Phoenix Contact** | Either |
| Fuse Holder 20A + Fuses | Main protection | **Littelfuse** | **Littelfuse** | Either |
| Fuse Holder 5A + Fuses | Circuit protection | **Littelfuse** | **Littelfuse** | Either |
| Ground Lug (2x) | Earth connection | **✓ Available** | **✓ Available** | Either |
| MC4 Connectors (pair) | Solar panel | Limited | **✓ Available** | DigiKey |
| DC Surge Protector | Solar input | **✓ Available** | Limited | Mouser |
| Coax Lightning Arrestor | Antenna protection | Limited | Limited | Specialized |
| 18AWG Wire Red/Black (6m) | IR/sensor wiring | **Alpha Wire** | **Alpha Wire/Belden** | Either |
| 14AWG Wire Red/Black (4m) | DC power | **Alpha Wire** | **Alpha Wire/Belden** | Either |
| Heat Shrink Kit | Insulation | **TE/3M** | **TE/3M** | Either |
| Wire Ferrule Kit | Terminals | **Phoenix Contact** | **Phoenix Contact** | Either |

### Category 7: Anti-Theft System

| Component | Spec | Mouser | DigiKey | Best Source |
|-----------|------|--------|---------|-------------|
| Plunger Tamper Switch NC (2x) | Lid detection | ❌ No | **C&K/Honeywell** | DigiKey/Security |
| Vibration Sensor | Shock detection | Limited | **Adafruit/Parallax** | DigiKey |
| Tilt Sensor | Pole removal | Limited | **✓ Available** | Either |
| 12V Siren 110dB IP65 | Audible alarm | ❌ No | ❌ No | Amazon |
| 12V Strobe Light IP67 | Visual alarm | ❌ No | ❌ No | Amazon |
| Latching Relay 12V | Alarm hold | Limited | **Omron G9TA** | DigiKey |
| Key Switch SPST | Reset/arm | Limited | **✓ Available** | DigiKey |

### Category 8: Connectivity

| Component | Spec | Mouser | DigiKey | Best Source |
|-----------|------|--------|---------|-------------|
| 4G LTE Antenna SMA | Cellular | Limited | Limited | Amazon/Sixfab |
| WiFi Antenna RP-SMA | WiFi | Limited | Limited | Amazon |
| USB-RS485 Adapter | Sensor interface | Limited | Limited | Amazon (DSD TECH) |

### Category 9: Consumables

| Component | Spec | Mouser | DigiKey | Best Source |
|-----------|------|--------|---------|-------------|
| Silicone Sealant (Marine) | Weatherproofing | ❌ No | ❌ No | Hardware store |
| Dielectric Grease | Connector protection | ❌ No | ❌ No | Hardware store |
| Cable Labels | Identification | **Brady/Panduit** | **Brady/Panduit** | Either |
| Desiccant Packs | Initial moisture | Limited | **✓ Available** | DigiKey |

---

## Cost Analysis

### DigiKey-Sourceable Components

| Category | Items | Est. Cost |
|----------|-------|-----------|
| Raspberry Pi 5 8GB | 1 | $80 |
| Industrial MicroSD 64GB | 1 | $40 |
| Enclosures (2x) | 2 | $120-180 |
| Cable Glands (M12/M16/M20) | 15 | $50-75 |
| GORE Vents | 2 | $15-25 |
| SMA Bulkheads | 2 | $20-30 |
| USB Active Cables 10m | 2 | $80-100 |
| Terminal Blocks | 6 | $15-25 |
| DIN Rail | 2 | $15-20 |
| Fuse Holders + Fuses | 2 sets | $15-25 |
| DC-DC Converter | 1 | $10-20 |
| Protection (TVS, polyfuse, diodes) | Multiple | $10-20 |
| Relays | 2 | $15-25 |
| Wire + Heat Shrink + Ferrules | Assorted | $50-80 |
| Anti-theft sensors | 4 | $30-50 |
| **DigiKey Subtotal** | | **$565-775** |

### Must Source Elsewhere

| Category | Items | Est. Cost | Recommended Source |
|----------|-------|-----------|-------------------|
| Witty Pi 4 | 1 | $30 | UUGear/Adafruit |
| LiFePO4 Battery 50Ah | 1 | $200-300 | Renogy/BattleBorn |
| MPPT Charge Controller | 1 | $50-100 | Victron/Renogy |
| Solar Panel 100W | 1 | $80-150 | Local/Renogy |
| IP67 USB Cameras | 2 | $150-300 | ELP/SVPRO (Amazon) |
| 850nm IR Flood | 1-2 | $40-80 | Amazon (OOSSXX) |
| 12V Photoresistor Relay | 1 | $5-10 | Amazon (XH-M131) |
| 4G Modem + Antennas | 1 set | $80-150 | Amazon |
| 12V Siren + Strobe | 1 set | $40-80 | Amazon |
| USB-RS485 Adapter | 1 | $15-25 | Amazon |
| Camera Brackets | 2 | $20-40 | Amazon |
| Consumables | Misc | $25-40 | Hardware store |
| **Alternative Subtotal** | | **$735-1,275** |

### Total System Cost

| Configuration | DigiKey | Other | **TOTAL** |
|---------------|---------|-------|-----------|
| **Low (50W/20Ah)** | $565 | $585 | **$1,150** |
| **Mid (100W/50Ah)** | $650 | $850 | **$1,500** |
| **High (200W/100Ah)** | $775 | $1,275 | **$2,050** |

---

## Recommended Procurement Strategy

### Primary: DigiKey + 3 Supplemental Sources

**Order 1: DigiKey (~45% of cost)**
- Raspberry Pi 5 + Industrial MicroSD
- All enclosures and cable glands
- All DIN rail, terminal blocks, fuses
- Protection devices (TVS, polyfuse, diodes)
- Relays and wiring supplies
- USB active extension cables
- Anti-theft sensors

**Order 2: Renogy/Victron (~25% of cost)**
- Complete solar kit: Panel + MPPT + Battery
- MC4 cables and connectors
- *Benefit: Matched components, single warranty*

**Order 3: Amazon (~25% of cost)**
- IP67 USB cameras (ELP/SVPRO)
- IR flood lights (OOSSXX)
- 4G modem and antennas
- Siren, strobe, security items
- Camera brackets, USB-RS485

**Order 4: Local/Specialty (~5% of cost)**
- Witty Pi 4 (UUGear or Adafruit)
- Silicone sealant, dielectric grease
- Any region-specific consumables

---

## Single-Supplier Limitations

### Why 100% Single-Source Is Not Possible

1. **Mouser/DigiKey are electronic component distributors**
   - Focus on semiconductors, passives, connectors
   - Limited system-level products (complete cameras, batteries)
   - No solar equipment, limited power products

2. **Specialized product categories require specialized suppliers:**
   - **Batteries:** LiFePO4 requires battery specialists
   - **Solar:** Panels/controllers from solar distributors
   - **Cameras:** Industrial cameras from machine vision suppliers
   - **Security:** Alarms from security equipment distributors

3. **Design principle conflict:**
   - RC-Box is designed for field serviceability
   - This requires using globally-available commodity parts
   - Such parts come from multiple supplier ecosystems

### Maximum Achievable Single-Supplier Coverage

| Supplier | Max Coverage | Missing Critical Items |
|----------|--------------|----------------------|
| **DigiKey** | ~45% by cost | Batteries, solar, cameras, IR lights, Witty Pi |
| **Mouser** | ~35% by cost | Same as DigiKey + Pi5, enclosures |
| **Amazon** | ~60% by cost | Quality industrial components, some sensors |

*Amazon offers broadest selection but with quality/authenticity concerns for critical components.*

---

## DigiKey BOM Quick Reference

### Confirmed In-Stock Items (December 2025)

| Component | DigiKey Part # | Price | Notes |
|-----------|---------------|-------|-------|
| Raspberry Pi 5 8GB | SC1112 | $80 | Ships same day |
| Raspberry Pi 5 4GB | SC1111 | $60 | Ships same day |
| Kingston Industrial microSD 64GB | SDCE/64GB | $40 | Extended temp |
| Tripp Lite USB 3.0 Active 10m | U330-10M-1 | $40 | Active repeater |
| Phoenix Contact Terminal Block | 277-1079073-ND | $2 | DIN rail mount |
| Bourns TVS Diode 5V | SMAJ5.0A | $0.50 | USB protection |
| Littelfuse Polyfuse 5A | Various | $1 | Resettable PTC |
| 1N4007 Diode | Various | $0.10 | Flyback |

### Search Categories for Size-Specific Items

| Component | DigiKey Category | Filter By |
|-----------|------------------|-----------|
| IP67 Enclosures | Boxes > IP67 | Dimensions, material |
| Cable Glands | Cable Glands | Thread size, cable OD |
| SMA Bulkheads | RF Connectors > SMA | IP rating, panel mount |
| GORE Vents | Vents | IP rating, thread size |

---

## Mouser BOM Quick Reference

### Confirmed Available Items

| Component | Mouser Part # | Price | Notes |
|-----------|---------------|-------|-------|
| Bourns TVS Diode 5V | 576-SMAJ5.0A | $0.50 | In stock |
| Littelfuse TVS 6.8V | 576-P6KE6.8A | $0.30 | In stock |
| Keystone Fuse Holder 20A | 534-3557-20 | $2.50 | Automotive blade |
| HARTING Cable Gland M20 | 617-19000005182 | $5 | IP68, 6-12mm |
| Phoenix Contact Terminal | 651-3214024 | $3 | Push-in PTI series |
| RECOM DC-DC 5V 1A | R-78E5.0-1.0 | $4 | 90%+ efficiency |

### Mouser Gaps Compared to DigiKey
- Limited Raspberry Pi 5 stock
- Fewer enclosure options
- Similar gaps: cameras, batteries, solar

---

## Final Recommendation

**For RC-Box procurement, use DigiKey as primary supplier for:**
- All electronic components
- Enclosures and sealing
- Wiring and terminals
- Protection devices

**Supplement with:**
- **Renogy/Victron:** Solar system (matched components)
- **Amazon:** Cameras, IR lights, security, 4G modem
- **UUGear:** Witty Pi 4
- **Local:** Consumables

This approach provides:
- 45% from DigiKey (quality guaranteed, fast shipping)
- 25% from solar specialist (matched system)
- 25% from Amazon (convenience, availability)
- 5% local (deployment flexibility)

**Total supplier count: 4** (minimum practical for this design)

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-12-07 | Initial research and comparison |

## Sources

- [DigiKey Raspberry Pi 5](https://www.digikey.com/en/product-highlight/r/raspberry-pi/raspberry-pi-5)
- [DigiKey IP67 Enclosures](https://www.digikey.com/en/products/filter/boxes/ip67/594)
- [Mouser TVS Diodes](https://www.mouser.com/c/semiconductors/discrete-semiconductors/diodes-rectifiers/transient-voltage-suppression-diodes-tvs/)
- [Mouser Phoenix Contact Terminals](https://www.mouser.com/c/electromechanical/industrial-automation/industrial-terminal-blocks/din-rail-terminal-blocks/?m=Phoenix%20Contact)
- [GORE Protective Vents](https://www.gore.com/products/gore-protective-vents)
- [UUGear Witty Pi 4](https://www.uugear.com/product/witty-pi-4/)
- [Renogy Solar](https://www.renogy.com/)
- [Victron Energy](https://www.victronenergy.com/)
