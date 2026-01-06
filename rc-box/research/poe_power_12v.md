# Power Solutions for Running PoE IP Cameras from 12V LiFePO4 Battery

## Executive Summary

Research conducted: January 5, 2026

**Key Findings:**

- **Best Overall Solution:** Industrial PoE switches with 12V DC input (Planet IGS-1020PTF-12V, TRENDnet TI-PG62B, IPCamPower PPS-DC8G2G-AT1) offer integrated power boost and PoE output in a single unit
- **Most Cost-Effective:** DC-DC converter + PoE injector modules (Tycon TP-DCDC-1248D, AIR802 PDCPOEVA48AF) at $50-125
- **Temperature Champion:** Industrial switches and injectors rated -40°C to 75°C exceed requirements
- **Active vs Passive PoE:** Active 802.3af/at strongly recommended for safety and compatibility
- **Power Budget:** At 12V input, total PoE output is typically limited to 60-90W (adequate for 2 cameras at 8-12W each)

---

## Introduction

This research investigates power solutions for converting 12V DC from a LiFePO4 battery system (10.5V-14.6V operating range) to 48V PoE for powering 2 IP cameras in an outdoor/field deployment scenario. Requirements include:

- Input: 12V DC (10.5V-14.6V range)
- Output: 48V PoE (802.3af or 802.3at) for 2 cameras
- Power per camera: 8-12W
- Field-serviceable (pluggable connectors, no soldering)
- Outdoor rated or suitable for sealed enclosure
- Wide temperature range (-20°C to +50°C minimum, -40°C to +75°C ideal)

---

## 1. Active PoE (802.3af/at) vs Passive PoE

### Active PoE (IEEE 802.3af/at/bt) - RECOMMENDED

**How It Works:**
Active PoE devices perform a "handshake" or verification process before delivering power. The Power Sourcing Equipment (PSE) sends a small voltage to detect a compatible Powered Device (PD), classifies the PD by determining its power requirements, then gradually increases voltage to the required level [CCTV Camera World, 2026].

**Power Levels:**
- PoE (IEEE 802.3af): Up to 15.4W DC power (12.95W at device after cable loss)
- PoE+ (IEEE 802.3at): Up to 30W DC power
- PoE++ (IEEE 802.3bt): Up to 60W (Type 3) or 90W (Type 4)

**Advantages:**
- Standardized by IEEE with cross-vendor interoperability
- Built-in safety mechanisms prevent damage from incorrect wiring
- Power negotiation and management
- Continuous monitoring for safe operation
- Industry standard for modern IP cameras

**Safety Note:**
Active PoE switches should always be the top choice for powering IP phones, IP cameras, and wireless access points. Passive PoE can damage equipment not rated for the specific voltage, as it supplies power regardless of what's plugged in [SecurityCamCenter, 2026].

### Passive PoE - NOT RECOMMENDED for this application

**How It Works:**
Passive PoE supplies a fixed DC voltage (usually 24V or 48V) on spare wire pairs without any intelligent power management or device detection.

**Disadvantages:**
- Not standardized (vendor incompatibilities common)
- No safety features - can damage incompatible devices
- No power negotiation
- Limited to simpler applications

**Use Cases:**
Acceptable for dedicated systems with matched passive PoE equipment (e.g., some MikroTik, Ubiquiti devices), but NOT recommended for standard 802.3af IP cameras.

---

## 2. Solution Category 1: Industrial PoE Switches with 12V DC Input

These switches integrate DC-DC power boost from 12V to 48V/54V and provide multiple PoE ports in a single unit. **BEST OVERALL SOLUTION** for reliability and integration.

### 2.1 Planet Technology IGS-1020PTF-12V

**Manufacturer:** Planet Technology
**Model:** IGS-1020PTF-12V V2

**Specifications:**
- **Input Voltage:** 12-54V DC, 7A max
- **PoE Standard:** IEEE 802.3at PoE+
- **Ports:** 8x 10/100/1000BASE-T PoE+ ports, 2x 100/1000X SFP uplink ports
- **PoE Budget:** Up to 240W total (at 54V input); reduced at 12V input
- **Power per Port:** Up to 30W per port (at 54V DC)
- **Operating Temperature:** -40°C to 75°C (**EXCEEDS REQUIREMENTS**)
- **Enclosure:** IP30 rugged aluminum housing
- **Mounting:** DIN-rail type
- **ESD Protection:** ±6kV DC contact/air discharge
- **Surge Immunity:** ±6kV
- **Type:** Unmanaged switch

**Special Features:**
- **12V Power Boost Technology:** Converts 12-54V DC input to 54V DC output for PoE
- **Extended Mode:** Can operate at 10Mbps full duplex to extend distance up to 250 meters (vs. standard 100m limit), delivering 20-25W PoE

**Connectors:**
- RJ45 for Ethernet/PoE
- DC power input via terminal block or DC jack

**Availability & Pricing:**
- Available from DigiKey Marketplace (ships in ~15 days, $25 flat shipping fee)
- Available on Amazon
- Specific pricing not listed in search results - contact supplier

**Evaluation:**
- **Pros:** Industrial-grade, excellent temperature range, built-in boost converter, 8 ports (expandable), extended reach mode
- **Cons:** Overkill for 2 cameras, higher cost, larger form factor
- **Recommendation:** Excellent choice if you need room for expansion or extreme reliability

**Sources:** [Planet Technology USA](https://planetechusa.com/product/igs-1020ptf-12v-industrial-8-port-10-100-1000t-802-3at-poe-2-port-100-1000x-sfp-ethernet-switch-w-12v-booster-4075c/), [Planet Taiwan](https://www.planet.com.tw/en/product/igs-1020ptf-12v-v2), [DigiKey](https://www.digikey.com/en/products/detail/business-systems-connection-inc/IGS-1020PTF-12V/13418952)

---

### 2.2 TRENDnet TI-PG62B

**Manufacturer:** TRENDnet
**Model:** TI-PG62B (Version V2)

**Specifications:**
- **Input Voltage:** 12-56V DC (dual redundant inputs)
- **PoE Standard:** IEEE 802.3at PoE+
- **Ports:** 4x Gigabit PoE+ ports, 2x SFP slots
- **PoE Budget:** 60-120W (60W at 12V, 120W at 24V+)
- **Power per Port:** Up to 30W per port
- **Operating Temperature:** -40°C to 75°C (**EXCEEDS REQUIREMENTS**)
- **Enclosure:** IP30 rated metal housing
- **Switching Capacity:** 12Gbps
- **Mounting:** DIN-rail mount, wall mounting hardware included
- **Type:** Unmanaged switch

**Special Features:**
- **Dual Redundant Power Inputs:** Two separate 12-56V DC inputs with overload current protection
- **Power Failure Alarm Relay:** Alerts on power issues
- **Shock/Vibration Rated:** EN 60068-2-27 (shock), EN 60068-2-32 (freefall), EN 60068-2-6 (vibration)
- **NDAA/TAA Compliant:** Approved for US/Canada government installations

**Connectors:**
- RJ45 for Ethernet/PoE
- Dual DC power inputs (terminal block)
- Alarm relay output

**Availability & Pricing:**
- **Price:** $274.99 (new from TRENDnet)
- **Refurbished:** $174.99 + $12.99 shipping (Amazon)
- Available from TRENDnet store, Amazon

**Evaluation:**
- **Pros:** Perfect port count for 2 cameras + expansion, dual power inputs, excellent temperature range, competitive price, TAA compliant
- **Cons:** None significant for this application
- **Recommendation:** **TOP CHOICE** - best balance of features, ports, and price for 2-camera system

**Warranty:** Lifetime Protection from TRENDnet

**Sources:** [TRENDnet Official](https://www.trendnet.com/products/product-detail?prod=175_TI-PG62B), [Amazon](https://www.amazon.com/TRENDnet-Industrial-Dedicated-Protection-TI-PG62B/dp/B01MQXZWLY), [Network Hardwares](https://www.networkhardwares.com/products/trendnet-ti-pg62b-trendnet-6-port-industrial-gigabit-poe-din-rail-switch-12-56v-dual-redundant-12-56-vdc-power-inputs-with-overload-current-protection-ti-pg62b/)

---

### 2.3 IPCamPower PPS-DC8G2G-AT1

**Manufacturer:** IPCamPower
**Model:** PPS-DC8G2G-AT1

**Specifications:**
- **Input Voltage:** 12-48V DC (wide range)
- **PoE Standard:** IEEE 802.3af/at active PoE
- **Ports:** 8x PoE Gigabit ports, 2x Non-PoE uplink ports (10 total)
- **PoE Budget:** 90W at 12V DC, 120W at 24V+ DC
- **Power per Port:** Up to 30W per port
- **Operating Temperature:** -40°F to 158°F (-40°C to 70°C) (**EXCEEDS REQUIREMENTS**)
- **Mounting:** DIN rail mount included
- **Construction:** Heavy-duty metal
- **Type:** Unmanaged switch

**Special Features:**
- **Dual Power Inputs:** Redundancy for backup battery connection
- **Port Isolation:** PoE ports cannot communicate with each other (security feature)
- **All Ports Surge Protected**
- **Solar Optimized:** Specifically designed for solar trailer and off-grid installations
- **TAA/NDAA Compliant**

**Connectors:**
- RJ45 for Ethernet/PoE
- Dual DC power inputs (terminal blocks assumed)

**Availability & Pricing:**
- Available from IPCamPower.com
- Specific pricing not listed - contact supplier

**Evaluation:**
- **Pros:** Designed specifically for 12V battery/solar systems, port isolation feature, dual inputs, excellent for mobile/field deployments
- **Cons:** 8 ports may be overkill for 2 cameras, limited temperature spec documentation
- **Recommendation:** Excellent choice for solar/battery applications with potential for expansion

**Warranty:** 3 years

**Sources:** [IPCamPower](https://ipcampower.com/products/pps-dc8g2g-at1)

---

## 3. Solution Category 2: DC-DC PoE Converter/Injector Modules

These compact modules convert 12V DC to 48V and inject PoE into Ethernet cables. **MOST COST-EFFECTIVE** solution for exactly 2 cameras.

### 3.1 Tycon Power TP-DCDC-1248D

**Manufacturer:** Tycon Systems Inc.
**Model:** TP-DCDC-1248D

**Specifications:**
- **Input Voltage:** 9-36V DC (**COMPATIBLE with LiFePO4 range**)
- **Output Voltage:** Regulated 48V DC
- **Output Power:** 17W per port (2 ports total)
- **PoE Standard:** IEEE 802.3af compatible
- **Data Rate:** 10/100 Mbps (not Gigabit)
- **Operating Temperature:** Not specified in search results (consult datasheet)
- **Mounting:** DIN rail mountable (with optional DIN-ClipKit-UNI)

**Special Features:**
- **Dual Power Inputs:** Two common (-) and two (+) terminals for connecting primary and backup power sources
- **Integrated PoE Injector:** Applies 48V DC to CAT5/6 cable
- **Multiple Protections:** Surge, short circuit, and overload protection
- **PoE Pin Assignment:** Power on pins 4, 5 (V+) and 7, 8 (V-)

**Connectors:**
- **Power Input:** Screw terminal block (2x positive, 2x negative for redundancy)
- **Data In:** Shielded RJ45 jack
- **Data + PoE Out:** Shielded RJ45 jack

**Availability & Pricing:**
- **Price:** $55.19 (DigiKey UK), approximately $60-70 USD
- Available from DigiKey, Amazon, Tycon Systems direct

**Evaluation:**
- **Pros:** Very cost-effective, wide input voltage range, redundant power inputs, field-proven design
- **Cons:** Only 100Mbps (not Gigabit), temperature specs unclear, single 2-port unit
- **Recommendation:** Good budget option if 100Mbps sufficient

**Applications:** 12V/24V battery systems, wireless access points, IP cameras, security systems

**Sources:** [Tycon Systems](https://tyconsystems.com/homepage/shop/tp-dcdc-1248d/), [DigiKey](https://www.digikey.com/en/products/detail/tycon-systems-inc/TP-DCDC-1248D/11479894), [Amazon](https://www.amazon.com/Tycon-Systems-TP-DCDC-1248D-Converter-Inserter/dp/B00BNHYPZ0), [AllDatasheet](https://www.alldatasheet.com/datasheet-pdf/pdf/1807788/TYCONSYSTEMS/TP-DCDC-1248D.html)

---

### 3.2 AIR802 DC-DC PoE Converter 802.3af

**Manufacturer:** AIR802 Manufacturing
**Model:** PDCPOEVA48AF

**Specifications:**
- **Input Voltage:** 9-36V DC (**COMPATIBLE with LiFePO4 range**)
- **Output Voltage:** 48V DC
- **Output Power:** Up to 24W
- **PoE Standard:** IEEE 802.3af
- **Data Rate:** Assumed 10/100/1000 Mbps (confirm with manufacturer)
- **Operating Temperature:** Not specified (contact manufacturer)
- **Mounting:** DIN rail mounting

**Special Features:**
- **IEEE 802.3af Compliant:** True active PoE with handshake
- **Single-Port Design:** One PoE output per unit (need 2 units for 2 cameras)
- **Made in USA**

**Connectors:**
- **Two Shielded Ethernet Jacks:**
  - "Network" jack: Connects to switch/router/computer
  - "Equip + PoE" jack: Output to powered device with voltage

**Availability & Pricing:**
- **Price:** Approximately $50-70 (based on related products)
- Available from AIR802.com, Amazon

**Evaluation:**
- **Pros:** True 802.3af compliance, compact, Made in USA
- **Cons:** Single port (need 2 units for 2 cameras), unclear temperature rating, limited specs in search results
- **Recommendation:** Suitable if you need true 802.3af certification and compact form factor

**Applications:** Marine vessels, automotive, trucks, RVs, 12V/24V solar systems, wireless access points

**Note:** AIR802 also makes higher-power models (up to 90W) for 802.3at/bt applications.

**Sources:** [AIR802](https://www.air802.com/dc-dc-poe-converter-802.3af), [Amazon AIR802](https://www.amazon.com/AIR802-DC-Converter-802-3af-Injector/dp/B00HM77LP6)

---

### 3.3 Coolgear CG-POEIJ12V

**Manufacturer:** Coolgear Inc.
**Model:** CG-POEIJ12V

**Specifications:**
- **Input Voltage:** 12V DC (fixed, NOT 9-36V range)
- **Output Voltage:** 48V DC
- **PoE Standard:** IEEE 802.3af/at compliant (Type 1 & 2)
- **Maximum Power Delivered:**
  - Type 1 (802.3af): 15.4W
  - Type 2 (802.3at): 34.2W
- **Data Rate:** 10/100/1000 Mbps (Gigabit)
- **Operating Temperature:** Not specified in search results
- **Ports:** 2-port active injector

**Connectors:**
- **Power Input:** DC-Jack AND TB-2 terminal block (dual input options)

**Availability & Pricing:**
- **Price:** $123.01 (DigiKey)
- Available from DigiKey, Coolgear.com, Amazon

**Evaluation:**
- **Pros:** Gigabit support, dual power input options (jack + terminal block), IEEE 802.3af/at certified
- **Cons:** Fixed 12V input only (won't work at LiFePO4 low voltage ~10.5V), higher price, temperature specs unclear
- **Recommendation:** Only if you have regulated 12V supply; NOT suitable for direct battery connection with voltage fluctuation

**Datasheet:** Available (367KB, 1 page) from Coolgear/AllDatasheet

**Sources:** [Coolgear](https://www.coolgear.com/product/gigabit-ieee-802-3af-at-poe-injector-12v), [DigiKey](https://www.digikey.com/en/products/detail/coolgear/CG-POEiJ12V/26762814), [Amazon](https://www.amazon.com/Coolgear-Gigabit-IEEE-802-3af-Injector/dp/B07V9XCQRW)

---

### 3.4 Planet Technology IPOE-260-12V

**Manufacturer:** Planet Technology
**Model:** IPOE-260-12V

**Specifications:**
- **Input Voltage:** 12-54V DC (**COMPATIBLE with LiFePO4 range**)
- **Output Voltage:** 54V DC (boosted from 12V input)
- **PoE Standard:** IEEE 802.3at PoE+ (also compatible with 802.3af)
- **Ports:** 2 Data In, 2 PoE Out
- **Power per Port:** Up to 36W (with 12V booster), 15.4W (802.3af mode)
- **Operating Temperature:** -40°C to 75°C (**EXCEEDS REQUIREMENTS**)
- **Enclosure:** IP30 rugged case
- **Mounting:** DIN-rail or wall mounting
- **Network Support:** 10/100/1000BASE-T (Gigabit)

**Special Features:**
- **12V Power Boost Technology:** Converts 12-54V DC to 54V DC output
- **Industrial Grade:** Designed for transportation and industrial applications
- **Compact Design:** Space-efficient for 2-port applications

**Connectors:**
- **Power Input:** 1x power terminal block
- **Data/PoE:** 2x Data In RJ45, 2x PoE Out RJ45

**Availability & Pricing:**
- **Price:** $164.00 (Network Camera Store), €137.70 in Europe
- Available from Network Camera Store, Planet dealers

**Evaluation:**
- **Pros:** Perfect for 2 cameras, excellent temperature range, industrial-grade, Gigabit support, power boost from 12V
- **Cons:** Requires separate power supply purchase
- **Recommendation:** **EXCELLENT CHOICE** - purpose-built for exactly this application (2 cameras, 12V battery, industrial environment)

**Important Note:** Does NOT include power supply - must be purchased separately

**Sources:** [Planet Technology USA](https://planetechusa.com/product/ipoe-260-12v-industrial-2-port-10-100-1000t-802-3at-poe-injector-hub-12v-booster/), [Planet Taiwan](https://www.planet.com.tw/en/product/ipoe-260-series), [Network Camera Store](https://networkcamerastore.com/products/planet-ipoe-260-12v-industrial-2-port-10-100-1000t-802-3at-poe-injector-w-12v-booster)

---

## 4. Solution Category 3: Passive PoE Injectors (Budget Alternative)

**WARNING:** Passive PoE is NOT recommended for standard 802.3af/at IP cameras due to safety concerns. Included for completeness only.

### 4.1 Data Alliance APoE08 8-Port Passive PoE Injector

**Manufacturer:** Data Alliance / Alfa Network
**Model:** APoE08

**Specifications:**
- **Input Voltage:** 12-48V DC
- **Output:** Passes input voltage directly to PoE pins (no conversion)
- **Ports:** 8x 10/100 Mbps RJ45 ports
- **Type:** Passive PoE (no 802.3af handshake)
- **Pin Assignment:** Data: 1,2,3,6 / Power: (+) 4,5 / (-) 7,8

**Features:**
- Redundant power inputs (DC jack + terminal block)
- On/off switch
- Terminal block can connect to UPS
- Rackmount kit available (APOE-RK)

**Connectors:**
- **Power Input:** 2.1x5.5mm DC jack OR screw terminal block
- **Data/PoE:** 8x RJ45

**Availability & Pricing:**
- **Price:** $21.04
- Available from Data-Alliance.net

**Evaluation:**
- **Pros:** Very low cost, simple, redundant power inputs, 8 ports
- **Cons:** NOT 802.3af compliant, can damage incompatible devices, only 100Mbps, no voltage conversion (requires 48V input for PoE cameras)
- **Recommendation:** **NOT SUITABLE** for this application (cameras need 48V, battery provides 12V)

**Note:** There is a Gigabit version (APoE08G) for higher throughput.

**Sources:** [Data Alliance](https://www.data-alliance.net/poe-injector-8-ports-any-voltage-from-12vdc-to-48vdc-passive/), [Alfa Network](https://alfa-network.eu/apoe08)

---

## 5. Comparison Matrix

| Product | Category | Input V | PoE Standard | Ports | Temp Range | Price (USD) | Recommendation |
|---------|----------|---------|--------------|-------|------------|-------------|----------------|
| **TRENDnet TI-PG62B** | Switch | 12-56V | 802.3at | 4+2 SFP | -40 to 75°C | $275 ($175 refurb) | **TOP CHOICE** |
| **Planet IPOE-260-12V** | Injector | 12-54V | 802.3at | 2 | -40 to 75°C | $164 | **BEST 2-PORT** |
| **IPCamPower PPS-DC8G2G-AT1** | Switch | 12-48V | 802.3af/at | 8+2 | -40 to 70°C | TBD | Excellent for solar |
| **Planet IGS-1020PTF-12V** | Switch | 12-54V | 802.3at | 8+2 SFP | -40 to 75°C | TBD (higher) | Overkill, expandable |
| **Tycon TP-DCDC-1248D** | Converter | 9-36V | 802.3af | 2 | Unknown | $60-70 | Budget option |
| **AIR802 PDCPOEVA48AF** | Converter | 9-36V | 802.3af | 1 | Unknown | $50-70 ea | Need 2 units |
| **Coolgear CG-POEIJ12V** | Injector | 12V only | 802.3af/at | 2 | Unknown | $123 | Fixed 12V issue |
| **Data Alliance APoE08** | Passive | 12-48V | None (passive) | 8 | N/A | $21 | **NOT SUITABLE** |

---

## 6. Power Budget Considerations

### LiFePO4 Battery Voltage Range Impact

When using 12V DC input at the lower end of the LiFePO4 discharge curve (10.5V-11.5V), the DC-DC boost converter must work harder, which affects efficiency and total available PoE power budget.

**Typical Power Budget by Input Voltage:**
- **12V Input:** 60-90W total PoE output (depending on model)
- **24V Input:** 120-180W total PoE output
- **48V Input:** 180-240W total PoE output

**For This Application (2 cameras @ 8-12W each):**
- **Total Power Required:** 16-24W
- **12V Input Capability:** 60-90W
- **Headroom:** Excellent - 2.5x to 4x overhead

All recommended solutions provide adequate power budget even at minimum 12V input.

---

## 7. Connector Types Summary

### Power Input Connectors

**Screw Terminal Blocks** (Most Common - Industrial)
- **Pros:** Field-serviceable, accept wide range of wire gauges, secure connection, vibration-resistant
- **Cons:** Require wire prep, screwdriver for installation
- **Found on:** Planet IPOE-260-12V, TRENDnet TI-PG62B, IPCamPower switches, Tycon TP-DCDC-1248D

**DC Barrel Jacks** (Common - Commercial)
- **Pros:** Quick connect/disconnect, plug-and-play
- **Cons:** Less secure in high-vibration environments, polarity mistakes possible
- **Common Sizes:** 2.1x5.5mm, 2.5x5.5mm
- **Found on:** Coolgear CG-POEIJ12V (also has terminal block), Data Alliance APoE08

**Redundant Input Options:**
Many industrial units offer BOTH terminal block AND DC jack, plus dual inputs for backup power.

### Data/PoE Output Connectors

**RJ45 Ethernet Jacks** (Universal)
- Standard 8P8C modular connectors
- Most industrial units use shielded jacks for EMI protection
- Standard CAT5e/CAT6 cable compatible

---

## 8. Installation Recommendations

### For Outdoor Sealed Enclosure Deployment

**Recommended Approach:**

1. **Primary Recommendation: TRENDnet TI-PG62B or Planet IPOE-260-12V**
   - Install inside weatherproof NEMA enclosure
   - Connect to battery via terminal blocks with appropriate AWG wire for current
   - Route Ethernet cables via cable glands/conduit entries
   - Ensure adequate ventilation or thermal management in enclosure

2. **Cable Glands:**
   - Use IP68 cable glands for all cable entries
   - Properly seal around Ethernet cables

3. **Grounding:**
   - Connect chassis ground to enclosure ground
   - Surge protection recommended for long outdoor Ethernet runs

4. **Fusing:**
   - Install appropriate DC fuse between battery and PoE device
   - Recommended: 5A fast-blow fuse for devices drawing <60W

### Temperature Management

All recommended industrial solutions (-40 to 75°C rating) exceed the stated requirements (-20 to 50°C). However, in sealed enclosures:

- Consider convection cooling or small ventilation fans if ambient > 40°C
- Monitor internal enclosure temperature
- Allow clearance around switch/injector for airflow

---

## 9. Buying Guide & Suppliers

### Recommended Suppliers

**DigiKey (www.digikey.com)**
- Tycon TP-DCDC-1248D: In stock
- Coolgear CG-POEIJ12V: In stock
- Planet products: Marketplace (15-day lead time)
- Ships worldwide, reliable

**Amazon (www.amazon.com)**
- TRENDnet TI-PG62B: $275 new, $175 refurbished
- Many PoE products available with Prime shipping
- Easy returns

**Direct from Manufacturers:**
- Planet Technology USA: planetechusa.com
- TRENDnet: trendnet.com
- IPCamPower: ipcampower.com
- AIR802: air802.com
- Tycon Systems: tyconsystems.com

**Industrial Distributors:**
- Network Camera Store: networkcamerastore.com (Planet products)
- Data Alliance: data-alliance.net (Alfa passive PoE)

---

## 10. Final Recommendations

### BEST OVERALL SOLUTION: TRENDnet TI-PG62B

**Why:**
- Perfect port count (4 PoE + 2 SFP) for 2 cameras with room for expansion
- Dual redundant 12-56V DC inputs
- Excellent temperature rating (-40 to 75°C)
- Competitive price ($275 new, $175 refurbished)
- Industrial-grade reliability
- TAA/NDAA compliant for government use
- Lifetime warranty
- All features needed: screw terminals, DIN rail mount, alarm relay

**Price:** $274.99 new / $174.99 refurbished
**Buy from:** TRENDnet.com or Amazon

---

### BEST 2-PORT SOLUTION: Planet IPOE-260-12V

**Why:**
- Purpose-built for exactly 2 devices
- Excellent temperature rating (-40 to 75°C)
- Industrial-grade with power boost technology
- Smaller form factor than full switch
- Lower price than multi-port switches
- Gigabit support

**Price:** $164.00
**Buy from:** Network Camera Store, Planet dealers

---

### BUDGET OPTION: Tycon TP-DCDC-1248D

**Why:**
- Most cost-effective at ~$60-70
- Wide input voltage range (9-36V)
- Redundant power inputs
- Proven reliability
- Field-serviceable screw terminals

**Limitations:**
- Only 100Mbps (not Gigabit)
- Temperature specs unclear (verify before outdoor use)
- Less integrated solution

**Price:** $60-70
**Buy from:** DigiKey, Amazon, Tycon Systems

---

### NOT RECOMMENDED: Passive PoE Solutions

Passive PoE injectors (like Data Alliance APoE08) are NOT suitable because:
1. They don't convert 12V to 48V (pass-through only)
2. No 802.3af handshake - can damage cameras
3. Safety concerns with no device detection
4. Not compatible with standard IP cameras expecting 802.3af/at

---

## 11. Technical Considerations & Best Practices

### Voltage Drop in Long Ethernet Runs

At 100 meters (328 ft) maximum distance, voltage drop in Ethernet cable affects available power at camera:

- **802.3af (15.4W):** ~2.5W lost in cable = 12.95W available
- **802.3at (30W):** ~4.5W lost in cable = 25.5W available

For cameras drawing 8-12W, 802.3af provides adequate headroom. Keep runs under 100m for best performance.

### Power Efficiency

DC-DC boost converters from 12V to 48V typically operate at 85-92% efficiency. When battery is at low state of charge (10.5V), efficiency decreases slightly. Factor this into battery capacity calculations.

**Example Power Draw Calculation:**
- 2 cameras @ 12W each = 24W total PoE output
- At 85% efficiency: 24W / 0.85 = 28.2W from 12V battery
- At 10.5V: 28.2W / 10.5V = 2.69A battery draw
- At 14.6V: 28.2W / 14.6V = 1.93A battery draw

### Battery Protection

Ensure your LiFePO4 battery system has:
- Low-voltage disconnect (LVD) to prevent over-discharge
- Appropriate fusing between battery and PoE device
- Reverse polarity protection (many industrial PoE devices include this)

### Electromagnetic Compatibility (EMC)

Industrial PoE switches include:
- Shielded RJ45 jacks
- ESD protection (±6kV or higher)
- Surge immunity (±6kV or higher)

This protection is critical for outdoor installations with long Ethernet cable runs susceptible to lightning-induced surges.

---

## 12. Conclusion

For running 2 PoE IP cameras from a 12V LiFePO4 battery system in outdoor/field conditions, **industrial PoE switches with integrated 12V boost technology** provide the best combination of reliability, safety, and field-serviceability.

**Top Recommendation:** TRENDnet TI-PG62B offers the best value with dual redundant power inputs, excellent temperature rating, competitive pricing, and room for system expansion.

**Alternative:** For a minimal 2-port solution, the Planet IPOE-260-12V is purpose-built for this exact application at a lower price point.

Both solutions provide:
- True IEEE 802.3af/at active PoE with safety handshake
- Wide input voltage compatibility (12-56V covers full LiFePO4 range)
- Industrial temperature ratings (-40°C to 75°C)
- Screw terminal power inputs (field-serviceable)
- Adequate power budget (60-90W at 12V input)
- Proven reliability for outdoor/industrial deployments

**Avoid** passive PoE solutions and products with fixed 12V-only input that won't tolerate battery voltage fluctuations.

---

## 13. Additional Resources

### Standards Documentation
- IEEE 802.3af-2003: PoE Standard (15.4W)
- IEEE 802.3at-2009: PoE+ Standard (30W)
- IEEE 802.3bt-2018: PoE++ Standard (60-90W)

### Application Notes
- Tycon Systems: DC-DC PoE Converter Specification Sheet
- Planet Technology: Industrial PoE Switch Installation Guide
- TRENDnet: TI-PG62B User Guide

### Further Reading
- "Active vs Passive PoE: Understanding the Differences" - CCTV Camera World
- "Power over Ethernet Explained" - FS.com
- "Best PoE Injector for IP Cameras" - Omnitron Systems

---

## Sources

1. [CCTV Camera World - Difference Between Active vs. Passive PoE](https://www.cctvcameraworld.com/difference-active-vs-passive-poe/)
2. [NETGEAR - Active or Passive PoE](https://www.netgear.com/hub/business/network/active-or-passive/)
3. [Reolink - Passive PoE Full Guide](https://reolink.com/blog/passive-poe/)
4. [SecurityCamCenter - Active PoE vs Passive PoE](https://securitycamcenter.com/difference-active-poe-passive-poe/)
5. [FS.com - Active vs. Passive PoE Switch](https://www.fs.com/blog/active-vs-passive-poe-switch-which-should-we-choose-33.html)
6. [TRENDnet Official - TI-PG62B Product Page](https://www.trendnet.com/products/product-detail?prod=175_TI-PG62B)
7. [Planet Technology USA - IGS-1020PTF-12V](https://planetechusa.com/product/igs-1020ptf-12v-industrial-8-port-10-100-1000t-802-3at-poe-2-port-100-1000x-sfp-ethernet-switch-w-12v-booster-4075c/)
8. [Planet Technology USA - IPOE-260-12V](https://planetechusa.com/product/ipoe-260-12v-industrial-2-port-10-100-1000t-802-3at-poe-injector-hub-12v-booster/)
9. [IPCamPower - 8-Port Industrial PoE Switch](https://ipcampower.com/products/pps-dc8g2g-at1)
10. [Tycon Systems - TP-DCDC-1248D](https://tyconsystems.com/homepage/shop/tp-dcdc-1248d/)
11. [AIR802 - DC-DC PoE Converter 802.3af](https://www.air802.com/dc-dc-poe-converter-802.3af)
12. [Coolgear - Gigabit IEEE 802.3af/at PoE Injector (12V)](https://www.coolgear.com/product/gigabit-ieee-802-3af-at-poe-injector-12v)
13. [Data Alliance - 8-Port Passive PoE Injector](https://www.data-alliance.net/poe-injector-8-ports-any-voltage-from-12vdc-to-48vdc-passive/)
14. [Amazon - TRENDnet TI-PG62B](https://www.amazon.com/TRENDnet-Industrial-Dedicated-Protection-TI-PG62B/dp/B01MQXZWLY)
15. [DigiKey - Tycon TP-DCDC-1248D](https://www.digikey.com/en/products/detail/tycon-systems-inc/TP-DCDC-1248D/11479894)

---

**Document Version:** 1.0
**Research Date:** January 5, 2026
**Researcher:** Claude (Anthropic)
**Subject:** Power solutions for PoE IP cameras from 12V LiFePO4 battery systems
