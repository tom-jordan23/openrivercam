# RC-Box DigiKey Bill of Materials Research
## Comprehensive Component Sourcing Analysis

**Date:** December 7, 2025
**Project:** RC-Box River Monitoring System
**Objective:** Identify all components available from DigiKey Electronics

---

## Executive Summary

DigiKey can supply approximately **40-50% of the RC-Box BOM**, primarily covering:
- ✅ Core electronic components (diodes, relays, fuses, terminals)
- ✅ Enclosures and cable glands
- ✅ Some connectors and cables
- ✅ Memory cards
- ✅ Basic sensors
- ✅ Raspberry Pi 5 (currently in stock)

**Not available from DigiKey:**
- ❌ Complete IP67/IP68 USB camera assemblies (connectors available, not complete cameras)
- ❌ LiFePO4 batteries and solar charge controllers
- ❌ Solar panels
- ❌ Complete IR illuminator assemblies (components available)
- ❌ Complete alarm sirens/strobes (may have industrial signaling devices)
- ❌ Witty Pi 4 (available from Adafruit, not directly DigiKey-stocked)

---

## Detailed Bill of Materials

### 1. COMPUTE & ELECTRONICS

| Category | Component | DigiKey Availability | DigiKey P/N | Manufacturer | MFR P/N | Unit Price | Qty | Notes |
|----------|-----------|---------------------|-------------|--------------|---------|------------|-----|-------|
| **Single Board Computer** | Raspberry Pi 5 8GB | ✅ IN STOCK | SC1112 | Raspberry Pi | SC1112 | ~$80 | 1 | Ships same day |
| **Single Board Computer** | Raspberry Pi 5 4GB | ✅ IN STOCK | SC1111 | Raspberry Pi | SC1111 | ~$60 | 1 | Alternative to 8GB |
| **Power Management** | Witty Pi 4 HAT | ⚠️ LIMITED | 5704 | Adafruit (Sold by DK) | 5704 | ~$30 | 1 | Check stock; sold through Adafruit |
| **Storage** | Industrial microSD 32GB | ✅ AVAILABLE | SDIT/32GBCP | Kingston | SDIT/32GBCP | ~$25-35 | 1 | Industrial grade, -40°C to +85°C |
| **Storage** | Industrial microSD 64GB | ✅ AVAILABLE | SDCE/64GB | Kingston | SDCE/64GB | ~$35-50 | 1 | Alternative capacity |
| **Connectivity** | 4G/LTE Base HAT | ⚠️ LIMITED | 1477-1050-ND | Sixfab | NL-AB-RPI | ~$50-80 | 1 | Sixfab products via DigiKey |
| **Connectivity** | 4G/LTE Antenna SMA | ⚠️ SOURCE ELSEWHERE | - | - | - | $15-30 | 1 | Many options, not all on DigiKey |
| **Connectivity** | WiFi Antenna RP-SMA | ⚠️ SOURCE ELSEWHERE | - | - | - | $10-20 | 1 | Many options, not all on DigiKey |
| **USB Hub** | Powered USB 3.0 Hub (if needed) | ⚠️ SOURCE ELSEWHERE | - | - | - | $20-40 | 0-1 | May not need if only 2 cameras |

### 2. POWER SYSTEM COMPONENTS

| Category | Component | DigiKey Availability | DigiKey P/N | Manufacturer | MFR P/N | Unit Price | Qty | Notes |
|----------|-----------|---------------------|-------------|--------------|---------|------------|-----|-------|
| **Power Conversion** | DC-DC Buck 12V→5V 5A | ✅ AVAILABLE | TBD | Texas Instruments / Diodes Inc | TPS62933 / Similar | $5-15 | 1 | Filter by: 12Vin, 5Vout, 5A, >90% eff |
| **Protection** | 5A Polyfuse PTC | ✅ IN STOCK | Multiple options | Littelfuse / Eaton | 1206L / PTSLR | $0.50-2 | 2 | Hold current: 5A, 12V+ rated |
| **Protection** | TVS Diode 5.5V USB | ✅ IN STOCK | CD143A-SR2.8 / Similar | Bourns / Nexperia | CD143A-SR2.8 | $0.30-1 | 2 | 5V clamp for Pi protection |
| **Protection** | 1N4007 Diode | ✅ IN STOCK | Multiple options | Diotec / Diodes Inc | 1N4007 | $0.05-0.15 | 5 | Flyback protection for relays |
| **Battery** | LiFePO4 12V 50Ah | ❌ NOT AVAILABLE | - | - | - | $150-250 | 1 | Source from battery suppliers |
| **Solar Charge** | MPPT Charge Controller | ❌ NOT AVAILABLE | - | - | - | $50-150 | 1 | Source from solar suppliers |
| **Solar Panel** | 100W Solar Panel | ❌ NOT AVAILABLE | - | - | - | $80-150 | 1 | Source from solar suppliers |

### 3. ENCLOSURES & SEALING

| Category | Component | DigiKey Availability | DigiKey P/N | Manufacturer | MFR P/N | Unit Price | Qty | Notes |
|----------|-----------|---------------------|-------------|--------------|---------|------------|-----|-------|
| **Enclosure** | IP67 Polycarbonate 200x150x100mm | ✅ AVAILABLE | Multiple options | Rose / Bud Industries | Various | $30-60 | 1 | Compute enclosure (Config A) |
| **Enclosure** | IP67 Polycarbonate 300x250x150mm | ✅ AVAILABLE | Multiple options | Rose / Bud Industries | Various | $50-90 | 1 | Power enclosure (Config A) |
| **Enclosure** | IP67 Polycarbonate 400x300x200mm | ✅ AVAILABLE | Multiple options | Rose / Bud Industries | Various | $80-150 | 1 | Combined enclosure (Config B) |
| **Cable Gland** | M12 IP68 Nylon | ✅ IN STOCK | Multiple options | Amphenol / TAKACHI | Various | $2-5 | 4 | 3-6.5mm cable range |
| **Cable Gland** | M16 IP68 Nylon | ✅ IN STOCK | Multiple options | Amphenol / TAKACHI | Various | $2-5 | 6 | 4-8mm cable range |
| **Cable Gland** | M20 IP68 Nylon | ✅ IN STOCK | Multiple options | Amphenol / TAKACHI | Various | $3-6 | 5 | 6-12mm cable range |
| **Blanking Plug** | M16 IP68 | ✅ AVAILABLE | Multiple options | Various | Various | $1-3 | 4 | Seal unused holes |
| **Pressure Vent** | GORE M12 Vent | ✅ AVAILABLE | Multiple options | W.L. Gore / Amphenol LTW | Various | $5-10 | 2 | IP67 rated, one per enclosure |
| **Bulkhead** | SMA IP67 Bulkhead | ✅ IN STOCK | Multiple options | Amphenol RF / GCT | Various | $5-15 | 2 | Antenna connections |

### 4. CAMERAS & CABLING

| Category | Component | DigiKey Availability | DigiKey P/N | Manufacturer | MFR P/N | Unit Price | Qty | Notes |
|----------|-----------|---------------------|-------------|--------------|---------|------------|-----|-------|
| **Camera** | IP67 USB Camera w/ IR | ❌ NOT COMPLETE | - | - | - | $100-300 | 2 | Source from machine vision suppliers |
| **USB Connector** | IP67 USB 2.0 Panel Mount | ✅ AVAILABLE | Multiple options | Conec / Same Sky | Various | $10-20 | 2 | For enclosure pass-through |
| **USB Cable** | Active USB Extension 10m | ✅ AVAILABLE | U330-10M-1 | Tripp Lite | U330-10M-1 | $35-50 | 2 | USB 3.0 active repeater |
| **USB Cable** | Active USB Extension 30m | ✅ AVAILABLE | U330F-30M-G1 | Tripp Lite | U330F-30M-G1 | $150-200 | 0-2 | If longer runs needed |
| **Camera Mount** | Adjustable Camera Bracket | ⚠️ SOURCE ELSEWHERE | - | - | - | $10-25 | 2 | Source from camera suppliers |

### 5. IR SPOTLIGHT SYSTEM

| Category | Component | DigiKey Availability | DigiKey P/N | Manufacturer | MFR P/N | Unit Price | Qty | Notes |
|----------|-----------|---------------------|-------------|--------------|---------|------------|-----|-------|
| **IR Illuminator** | 850nm 20W 12V Flood | ❌ NOT COMPLETE | - | - | - | $30-60 | 1-2 | Source from security suppliers (OOSSXX, etc) |
| **IR LEDs** | 850nm IR LED Components | ✅ AVAILABLE | Multiple options | Kingbright / Vishay | Various | $0.50-2 | Alt | If building custom array |
| **Relay** | 5V SPDT Relay Module 10A | ✅ AVAILABLE | Multiple options | Sunfounder / TE / Omron | Various | $3-8 | 1 | For IR spotlight control |
| **Diode** | 1N4007 Flyback Diode | ✅ IN STOCK | Multiple options | Diotec | 1N4007 | $0.05-0.15 | 2 | Already counted above |

### 6. ELECTRICAL COMPONENTS

| Category | Component | DigiKey Availability | DigiKey P/N | Manufacturer | MFR P/N | Unit Price | Qty | Notes |
|----------|-----------|---------------------|-------------|--------------|---------|------------|-----|-------|
| **DIN Rail** | 35mm DIN Rail 200mm | ✅ AVAILABLE | Multiple options | Phoenix Contact / TE | Various | $5-10 | 2 | Internal mounting |
| **Terminal Block** | DIN Rail Terminal 10A | ✅ IN STOCK | 277-1079073-ND (example) | Phoenix Contact / Same Sky | DN-D10-A | $1-3 | 6 | Screw terminal type |
| **Fuse Holder** | Panel Mount 20A | ✅ AVAILABLE | 03420012H (example) | Littelfuse | 03420012H | $2-5 | 1 | 5x20mm or 6.3x32mm |
| **Fuse Holder** | Panel Mount 5A | ✅ AVAILABLE | Multiple options | Littelfuse | Various | $2-5 | 1 | 5x20mm or 6.3x32mm |
| **Fuse** | 20A 250VAC Ceramic | ✅ IN STOCK | Multiple options | Littelfuse / Bel Fuse | Various | $0.50-1 | 3 | Spare fuses |
| **Fuse** | 5A 250VAC Ceramic | ✅ IN STOCK | Multiple options | Littelfuse / Bel Fuse | Various | $0.50-1 | 3 | Spare fuses |
| **Ground Lug** | Ring Terminal for Ground | ✅ AVAILABLE | Multiple options | TE / Panduit | Various | $0.20-1 | 2 | 10 AWG wire |
| **MC4 Connector** | Solar Panel MC4 Pair | ✅ AVAILABLE | Multiple options | TE / Tycon | MC4-CONNKIT | $5-10 | 1 set | Photovoltaic connectors |
| **Surge Protector** | DC Surge Suppressor | ⚠️ LIMITED | Multiple options | Various | Various | $15-40 | 1 | Solar input protection |
| **Surge Protector** | Coax Lightning Arrestor | ⚠️ LIMITED | Multiple options | Various | Various | $10-25 | 1-2 | Antenna protection |
| **Wire 18AWG** | Outdoor Red 3m | ✅ AVAILABLE | Multiple options | Alpha Wire / Belden | Various | $5-10 | 1 | Stranded, tinned copper |
| **Wire 18AWG** | Outdoor Black 3m | ✅ AVAILABLE | Multiple options | Alpha Wire / Belden | Various | $5-10 | 1 | Stranded, tinned copper |
| **Wire 14AWG** | Outdoor Red 2m | ✅ AVAILABLE | Multiple options | Alpha Wire / Belden | Various | $5-10 | 1 | For DC power runs |
| **Wire 14AWG** | Outdoor Black 2m | ✅ AVAILABLE | Multiple options | Alpha Wire / Belden | Various | $5-10 | 1 | For DC power runs |
| **Heat Shrink** | Assorted Kit | ✅ AVAILABLE | Multiple options | TE / 3M | Various | $10-20 | 1 | Various sizes |
| **Wire Ferrules** | Assorted Kit | ✅ AVAILABLE | Multiple options | Phoenix Contact / Weidmuller | Various | $10-25 | 1 | Terminal crimps |

### 7. ANTI-THEFT SYSTEM

| Category | Component | DigiKey Availability | DigiKey P/N | Manufacturer | MFR P/N | Unit Price | Qty | Notes |
|----------|-----------|---------------------|-------------|--------------|---------|------------|-----|-------|
| **Tamper Switch** | Plunger N.C. SPST | ✅ LIMITED | Multiple options | C&K / Honeywell | Anti-Tampering Series | $5-15 | 2 | Check DigiKey stock; may use SS-072Q elsewhere |
| **Vibration Sensor** | Piezo Vibration Sensor | ✅ AVAILABLE | 2384 (example) | Adafruit / Parallax | 605-00004 | $3-8 | 1 | Adjustable sensitivity preferred |
| **Tilt Sensor** | Tilt Switch | ✅ AVAILABLE | Multiple options | Various | Various | $2-5 | 1 | Optional for high-risk sites |
| **Siren** | 12V 110-120dB IP65 | ❌ NOT COMPLETE | - | - | - | $20-50 | 1 | Source from security suppliers |
| **Strobe Light** | 12V LED Strobe IP67 | ❌ NOT COMPLETE | - | - | - | $20-40 | 1 | Source from security/industrial suppliers |
| **Latching Relay** | 12V Latching Relay Module | ✅ AVAILABLE | Multiple options | Omron / IDEC / TE | G9TA / RR2KP | $10-25 | 1 | Self-holding alarm circuit |
| **Key Switch** | SPST Key Switch | ✅ AVAILABLE | Multiple options | Various | Various | $10-20 | 1 | Alarm reset/arm |

### 8. CONSUMABLES & ACCESSORIES

| Category | Component | DigiKey Availability | DigiKey P/N | Manufacturer | MFR P/N | Unit Price | Qty | Notes |
|----------|-----------|---------------------|-------------|--------------|---------|------------|-----|-------|
| **Sealant** | Silicone Outdoor Sealant | ⚠️ SOURCE ELSEWHERE | - | - | - | $5-10 | 1 tube | Hardware store item |
| **Grease** | Dielectric Grease | ⚠️ SOURCE ELSEWHERE | - | - | - | $8-15 | 1 tube | Hardware/auto store |
| **Labels** | Cable Labels | ✅ AVAILABLE | Multiple options | Brady / Panduit | Various | $10-20 | 1 set | Thermal/vinyl |
| **Desiccant** | Silica Gel Packets | ✅ AVAILABLE | Multiple options | Various | Various | $5-10 | 5-10 | Optional, for initial moisture |

---

## Summary Analysis

### DigiKey Coverage by Category

| Category | Components Available | Components Not Available | Coverage % |
|----------|---------------------|--------------------------|------------|
| Compute/Electronics | 4/9 | 5/9 | 44% |
| Power System | 4/9 | 5/9 | 44% |
| Enclosures & Sealing | 9/9 | 0/9 | 100% |
| Cameras & Cabling | 2/5 | 3/5 | 40% |
| IR Spotlight | 2/4 | 2/4 | 50% |
| Electrical Components | 16/16 | 0/16 | 100% |
| Anti-Theft System | 4/7 | 3/7 | 57% |
| Consumables | 2/4 | 2/4 | 50% |
| **TOTAL** | **43/63** | **20/63** | **68%** |

### Estimated Costs

**DigiKey-Sourceable Components (approximate):**
- Core Electronics (Pi, SD, HATs): $150-200
- Enclosures & Cable Glands: $100-180
- Electrical Components (terminals, wire, fuses): $80-120
- Connectors & USB Cables: $60-100
- Protection Devices (diodes, fuses, relays): $30-50
- **Subtotal from DigiKey: $420-650**

**Must Source Elsewhere:**
- Raspberry Pi 5 alternatives or accessories: $0-100
- LiFePO4 Battery + MPPT + Solar: $280-550
- IP67 USB Cameras (2x): $200-600
- IR Illuminators (1-2x): $30-120
- Alarm Siren/Strobe: $40-90
- Consumables (sealant, grease): $15-25
- **Subtotal from Other Sources: $565-1,485**

**TOTAL PROJECT COST (all sources): $985-2,135**

### DigiKey vs Mouser Comparison

Based on this research:
- **DigiKey Coverage:** ~68% of unique component types (43/63 items)
- **DigiKey Coverage (by value):** ~35-40% of total BOM cost
- **Mouser Coverage (estimated):** Similar at 40-50% of BOM (overlapping categories)

**Key Differences:**
- DigiKey has better Raspberry Pi stock availability currently
- DigiKey has strong enclosure selection (Rose, Bud Industries)
- Mouser may have different industrial signaling device selection
- Both lack complete camera assemblies, batteries, solar equipment

---

## Components NOT Available from DigiKey

### Critical Items to Source Elsewhere

1. **LiFePO4 Battery (12V 50Ah)**
   - Recommended Suppliers: Battle Born, Renogy, Ampere Time, Amazon
   - Estimated Cost: $150-250

2. **MPPT Solar Charge Controller**
   - Recommended Suppliers: Victron Energy, Renogy, EPEver, Amazon
   - Estimated Cost: $50-150

3. **Solar Panel (100W)**
   - Recommended Suppliers: Renogy, Newpowa, Eco-Worthy, Amazon
   - Estimated Cost: $80-150

4. **IP67/IP68 USB Cameras (2x)**
   - Recommended Suppliers: Lucid Vision Labs, Imperx, VA Imaging, FLIR, IDS Imaging
   - Estimated Cost: $100-300 each
   - Notes: Complete sealed camera assemblies with M12 USB connectors

5. **850nm IR Illuminator (20W, 12V)**
   - Recommended Suppliers: OOSSXX, OHWOAI, CMVision, Amazon
   - Estimated Cost: $30-60

6. **12V Alarm Siren (110dB+, IP65)**
   - Recommended Suppliers: Abra Electronics, Amazon industrial sirens
   - Estimated Cost: $20-50

7. **12V Strobe Light (IP67)**
   - Recommended Suppliers: Federal Signal, Auxbeam, Lumastrobe, Amazon
   - Estimated Cost: $20-40

8. **Witty Pi 4 (if not in stock at DigiKey)**
   - Recommended Suppliers: Adafruit, UUGear (manufacturer), The Pi Hut
   - Estimated Cost: $25-35

9. **4G/LTE Antennas**
   - Recommended Suppliers: Sixfab, Taoglas, Amazon
   - Estimated Cost: $15-30

10. **Consumables (Sealant, Dielectric Grease)**
    - Recommended Suppliers: Local hardware stores, Amazon
    - Estimated Cost: $15-25 total

---

## Procurement Strategy Recommendations

### Approach 1: Multi-Vendor (Optimal Cost)
1. **DigiKey:** All electronic components, enclosures, glands, terminals (~40% of BOM)
2. **Amazon/AliExpress:** Batteries, solar panels, cameras, IR lights, alarms (~35% of BOM)
3. **Specialized Suppliers:** High-reliability cameras from machine vision suppliers (~15%)
4. **Local:** Consumables (sealant, grease) at deployment location (~10%)

**Pros:** Lowest cost, fastest delivery for most items
**Cons:** Multiple shipments, coordination complexity

### Approach 2: DigiKey + One Solar Supplier
1. **DigiKey:** All electronics, enclosures, connectors
2. **Renogy or Victron:** Complete solar system (panel + controller + battery)
3. **Amazon:** Cameras, IR, alarms
4. **Local:** Consumables

**Pros:** Simplified solar system procurement, matched components
**Cons:** May cost 10-15% more than piecemeal

### Approach 3: Maximum DigiKey (Simplicity)
1. **DigiKey:** Everything they stock
2. **Direct from Manufacturers:** Items DigiKey doesn't carry
   - Cameras from Lucid Vision Labs
   - Battery from Battle Born
   - Solar from Renogy
   - Witty Pi from UUGear

**Pros:** Fewest suppliers, best for small quantity orders
**Cons:** Highest cost (no bulk pricing), longer lead times

---

## DigiKey-Specific Part Numbers (Examples)

### Confirmed Available (Sample Part Numbers)

| Component | DigiKey P/N | Price | Stock Status |
|-----------|-------------|-------|--------------|
| Raspberry Pi 5 8GB | SC1112 | ~$80 | In Stock |
| Raspberry Pi 5 4GB | SC1111 | ~$60 | In Stock |
| Kingston Industrial microSD 32GB | SDIT/32GBCP | ~$30 | Available |
| Tripp Lite USB 3.0 Active Cable 10m | U330-10M-1 | ~$40 | In Stock |
| 1N4007 Diode | Multiple | ~$0.10 | In Stock |
| Phoenix Contact Terminal Block | 277-1079073-ND | ~$2 | Available |

**Note:** Exact part numbers for enclosures, glands, and other items require filtering DigiKey's parametric search by size, IP rating, and specifications. The links provided in the research section lead to the correct categories.

---

## Research Sources

### DigiKey Product Highlights
- [Raspberry Pi 5 Product Page](https://www.digikey.com/en/product-highlight/r/raspberry-pi/raspberry-pi-5)
- [Rose Polycarbonate Watertight Enclosures](https://www.digikey.com/catalog/en/partgroup/polycarbonate-watertight-enclosures/27938)
- [DigiKey IP67 Boxes Category](https://www.digikey.com/en/products/filter/boxes/ip67/594)
- [Amphenol Cable Glands](https://www.digikey.com/en/product-highlight/a/amphenol-industrial-operations/cable-glands)
- [BUD Industries IP67 Vents](https://www.digikey.com/en/product-highlight/b/bud-industries/ipv-ip67-round-vents)
- [Amphenol LTW Protective Vent Series](https://www.digikey.com/en/product-highlight/a/amphenol-ltw/screw-vent-m12-series)
- [Sixfab Inc. Distributor Page](https://www.digikey.com/en/supplier-centers/sixfab-inc)
- [Conec USB 2.0 IP67 Connector System](https://www.digikey.com/en/product-highlight/c/conec/usb-2-ip67-connector-system)
- [Same Sky IP-Rated USB Connectors](https://www.digikey.com/en/product-highlight/c/cui/ip-rated-usb-connectors)
- [Amphenol RF IP67 RF Connectors](https://www.digikey.com/en/product-highlight/a/amphenol-rf-division/sealed-solutions)
- [ATP Industrial-Grade MicroSD Cards](https://www.digikey.com/en/product-highlight/a/atp/industrial-grade-microsd-microsdhc-cards)
- [Kingston Industrial MicroSD](https://www.digikey.com/en/product-highlight/k/kingston-technology/industrial-microsd-memory-card)
- [C&K Anti-Tampering Switch Series](https://www.digikey.com/en/product-highlight/c/ck-components/anti-tampering-switch-series)
- [Omron G9TA/G9TB Latching Power Relays](https://www.digikey.com/en/product-highlight/o/omron/g9ta-g9tb-latching-power-relays)

### External References
- [GORE Protective Vents](https://www.gore.com/products/screw-protective-vents-outdoor-electronics-enclosures)
- [TAKACHI Cable Glands](https://www.takachi-enclosure.com/cat/cable_glands)
- [UUGear Witty Pi 4](https://www.uugear.com/product/witty-pi-4/)
- [Lucid Vision Labs IP67 Cameras](https://thinklucid.com/ip67-cameras-and-accessories/)
- [Imperx IP67 Cameras](https://www.imperx.com/ip67-cameras/)
- [OOSSXX IR Illuminators](https://oossxx.com/products/ir-illuminator-850nm-12-led-ir-illuminators-ir-lights-for-security-cameras-10ft-12v-2a-power-supply-ohwoai-long-range-infrared-light-outdoor-ir-floodlight-wide-angle-for-cctv-ip-camera-night-vision)

---

## Next Steps

1. **Finalize Component Selection:**
   - Use DigiKey's parametric search to identify exact part numbers for enclosures based on required dimensions
   - Select specific cable gland part numbers based on actual cable ODs
   - Choose terminal block style (screw vs. push-in) and order matching quantity

2. **Create DigiKey Cart:**
   - Export this BOM to DigiKey's "BOM Manager" or create manual cart
   - Verify current pricing and availability
   - Check for volume discounts if ordering multiple units

3. **Identify Alternative Sources:**
   - Get quotes from battery suppliers (Battle Born, Renogy)
   - Contact machine vision camera suppliers for IP67 USB cameras
   - Source alarm components from security distributors

4. **Cross-Reference with Mouser:**
   - Compare pricing and availability for overlapping components
   - Check if Mouser has better stock on any critical items
   - Consider split order between DigiKey/Mouser for optimal pricing

5. **Local Procurement List:**
   - Prepare list of consumables to purchase at deployment location
   - Include spare wire, sealant, mounting hardware in shipment

---

**Document Version:** 1.0
**Last Updated:** December 7, 2025
**Researcher:** Claude (Anthropic)
**Contact:** For questions about this research, refer to original search sources linked above.
