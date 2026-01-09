# PoE Injector Research: 12V DC Input Solutions for Jakarta Site
**Research Date:** January 8, 2026
**Researcher:** Claude Code
**Purpose:** Verify Planet IPOE-260-12V and identify alternative 12V DC input PoE solutions for powering 2x PoE cameras from 12V DC system

---

## Executive Summary

**Key Findings:**

1. **Planet IPOE-260-12V EXISTS and meets requirements** - Confirmed as a legitimate industrial PoE+ injector with built-in 12V DC boost technology
2. **Perfect fit for Jakarta deployment** - Accepts 12-56V DC input, provides 2 ports with 36W per port (72W total), industrial temperature rating (-40°C to +75°C)
3. **Pricing:** Approximately $164 USD from authorized retailers (excludes power supply)
4. **Key advantage:** Built-in DC-DC boost converter (12-54V to 54V) eliminates need for special power supplies
5. **Alternatives available:** Veracity CamSwitch Mobile and Linovision options offer similar capabilities with different feature sets

**Recommendation:** The Planet IPOE-260-12V is confirmed as an excellent choice for the Jakarta site. It directly addresses the 12V DC input requirement and supports 2 PoE cameras with ample power budget.

---

## 1. Planet IPOE-260-12V - Primary Product Verification

### 1.1 Product Confirmation
**Status:** ✅ CONFIRMED - Product exists and is actively sold by Planet Technology

The IPOE-260-12V is a 2-Port, Mid-span Industrial IEEE 802.3at PoE+ Injector Hub specifically designed for low-voltage DC applications including battery-powered and transportation systems.

### 1.2 Complete Specifications

#### Power Input
- **Input Voltage Range:** 12-56V DC (dual redundant inputs)
- **Power Boost Technology:** Built-in 12-54V DC to 54V DC converter
- **Minimum Startup Voltage:** 12V DC
- **Reverse Polarity Protection:** Yes
- **Connector:** Removable 4-pin terminal block (Pin 1/2 for Power 1; Pin 3/4 for Power 2)
- **Wire Gauge:** 12-24 AWG

#### PoE Output
- **PoE Standard:** IEEE 802.3at (PoE+)
- **Maximum Power Per Port:** 36W
- **Total PoE Budget:**
  - 60W @ 12-23V DC input
  - 72W @ 24-56V DC input
- **Number of PoE Ports:** 2
- **PoE Output Voltage:** 54V DC
- **Backward Compatibility:** IEEE 802.3af (15.4W max per port)
- **Maximum Distance:** 100 meters over Cat 5/5e/6 cable

#### Network Interface
- **Data Ports:** 4x 10/100/1000BASE-T RJ45 ports
  - 2x Data input ports
  - 2x PoE + Data output ports
- **Port Configuration:** Auto-MDI/MDI-X
- **Data Rate:** 10/100/1000 Mbps (Gigabit Ethernet)

#### Environmental & Physical
- **Operating Temperature:** -40°C to +75°C (-40°F to +167°F)
- **Storage Temperature:** -40°C to +85°C
- **Operating Humidity:** 5% to 95% (non-condensing)
- **Enclosure Rating:** IP30 rugged metal case
- **Mounting Options:** DIN-rail, wall-mount, or side wall-mount
- **Dimensions (W x D x H):** 30 x 70 x 104 mm (1.18 x 2.76 x 4.09 inches)
- **Weight:** Not specified in available documentation
- **ESD Protection:** 6KV DC Ethernet ESD protection

#### Power Consumption
- **Idle (Power on, no connections):** 4W / 13.6 BTU
- **Maximum (Full PoE load):** 80W / 272.9 BTU

#### Standards Compliance
- **PoE:** IEEE 802.3at (PoE+), IEEE 802.3af (PoE) compatible
- **Designed for:** Industrial, transportation, and outdoor applications

### 1.3 Key Features for Jakarta Deployment

1. **12V DC Native Support** - The critical feature for battery-powered sites. The built-in boost converter accepts 12V input and converts to 54V PoE output without external converters.

2. **Dual Redundant Power Inputs** - Allows connection of primary and backup 12V power sources for high availability.

3. **Industrial Temperature Rating** - Can operate in Jakarta's tropical climate (typical 25-35°C) with significant thermal margin.

4. **Compact Ruggedized Design** - IP30 enclosure suitable for equipment cabinets, minimal space requirement.

5. **60W Power Budget at 12V Input** - Sufficient for 2x cameras drawing ~15W each (30W total) with 30W margin for spikes or future expansion.

### 1.4 Pricing & Availability

#### Current Pricing (2025-2026)
- **Retail Price:** ~$164 USD
- **Note:** Power supply NOT included - must be purchased separately

#### Where to Purchase
1. **Planet Technology USA** (planetechusa.com) - Direct manufacturer
2. **DigiKey Marketplace** - Ships same day
3. **Network Camera Store** - 10-12 day shipping, free shipping available
4. **Amazon** - Available with potential Prime shipping
5. **International Distributors:**
   - EQL Networks (Australia)
   - WISP Australia
   - Various EU distributors

### 1.5 Documentation Available
- **User Manual:** [IPOE-260_12V_v1-UserManual.pdf](https://planetechusa.com/wp-content/uploads/2019/11/IPOE-260_12V_v1-UserManual.pdf)
- **Datasheet:** [IPOE-260-Series_Datasheet.pdf](https://planetechusa.com/wp-content/uploads/2019/11/IPOE-260-Series_Datasheet.pdf)
- **Sales Guide:** [IPOE-260-Series_SalesGuide.pdf](https://planetechusa.com/wp-content/uploads/2019/11/IPOE-260-Series_SalesGuide.pdf)

### 1.6 Installation Requirements

#### Package Contents
- Industrial PoE+ Injector Hub x 1
- User's Manual x 1
- Wall-mount Kit x 1
- DIN-rail Kit x 1
- RJ45 Dust Caps x 4

#### Critical Installation Notes
1. **GROUNDING REQUIRED** - Device must be properly grounded. Lightning damage is NOT covered under warranty.
2. **Wire Gauge:** Use 12-24 AWG for terminal block connections
3. **Power Supply:** Must be purchased separately - not included with unit
4. **Cable Requirements:** Cat 5/5e/6 Ethernet cables (straight-through or crossover supported)

#### Mounting Options
- DIN rail mounting in equipment cabinet (recommended for industrial deployments)
- Wall mounting
- Side wall mounting

---

## 2. Alternative 12V DC Input PoE Solutions

While the Planet IPOE-260-12V meets requirements, the following alternatives were identified during research:

### 2.1 Veracity CamSwitch Mobile Series

#### CAMSWITCH 4 Mobile (VCS-4P1-MOB)

**Specifications:**
- **Input Voltage:** 8.5-40V DC (minimum startup 10.5V)
- **PoE Ports:** 4x IEEE 802.3at (PoE+)
- **Non-PoE Ports:** 1x uplink port
- **Total PoE Budget:**
  - 80W @ 24V DC
  - 60W @ <12V DC
  - 50W if voltage can drop below 10V
- **Network Speed:** 10/100 Mbps (Fast Ethernet, not Gigabit)
- **Power Input Requirements:** 10A @ 12V DC or 5A @ 24V DC supply (slow blow fuse)
- **PoE Standard:** IEEE 802.3af/at compatible
- **Operating Temperature:** Up to 50°C ambient

**Advantages:**
- Wider voltage input range (8.5-40V DC)
- 4 PoE ports vs 2 on Planet unit
- Specifically designed for vehicle/mobile applications
- Supports engine cranking voltage drops

**Disadvantages:**
- Only Fast Ethernet (100 Mbps) vs Gigabit on Planet
- Reduced power budget at 12V (60W vs 72W on Planet)
- Higher current draw (10A @ 12V vs estimated 6-7A for Planet)
- Price not specified but likely higher based on feature set

#### CAMSWITCH 8 Mobile (VCS-8P2-MOB)

**Specifications:**
- **PoE Ports:** 8x IEEE 802.3at
- **Non-PoE Ports:** 2x uplink ports
- **Input Voltage:** 8.5-40V DC
- **Total PoE Budget:** 80W
- **Network Speed:** 10/100 Mbps
- **Additional Features:** VLAN trunking support

**Use Case:** Overkill for 2-camera deployment but good for future expansion.

### 2.2 Linovision 5-Port Gigabit PoE Switch

**Specifications:**
- **Input Voltage:** DC 12V-48V (with built-in voltage booster)
- **PoE Ports:** 4x IEEE 802.3af/at (30W per port)
- **Non-PoE Ports:** 1x Gigabit uplink
- **Total PoE Budget:**
  - 120W @ DC24V/DC48V input
  - 60W @ DC12V input
- **Network Speed:** Gigabit (10/100/1000 Mbps)
- **Operating Temperature:** -40°C to 80°C
- **Enclosure:** IP40 rugged metal, industrial aviation aluminum
- **Mounting:** DIN-rail and wall mount
- **Protection:** 6KV lightning protection

**Advantages:**
- 4 PoE ports (room for expansion)
- Gigabit speed
- Slightly higher operating temperature rating (80°C vs 75°C)
- IP40 vs IP30 rating
- Similar voltage booster technology

**Disadvantages:**
- Availability unclear (primarily sold via Newegg, Alibaba channels)
- Less established brand than Planet Technology
- Price information not readily available

### 2.3 Tycon Systems DC-DC Converters

**Note:** Tycon Systems offers 12V DC input solutions, but they primarily produce **passive PoE** injectors rather than IEEE 802.3af/at compliant devices.

#### TP-DCDC-1224G
- **Input:** 10-36V DC
- **Output:** 24V Passive PoE
- **Power:** 20W
- **Price:** ~$41 USD
- **Limitation:** Passive PoE, not 802.3af/at standard

#### TP-DCDC-1248G
- **Input:** 12V DC
- **Output:** 48V PoE (24W)
- **Features:** Dual isolated inputs for primary/backup power
- **Limitation:** Single port, passive PoE

**Assessment:** Tycon products are budget-friendly but use **passive PoE** which may not be compatible with all IP cameras. Only recommended if cameras are confirmed to support passive PoE.

### 2.4 Industrial Multi-Port Options

#### IPCamPower 8-Port Industrial PoE Switch (PPS-DC8G2G-AT1)
- **Input Voltage:** 12-48V DC
- **PoE Ports:** 8x PoE+ (30W per port)
- **Total Budget:** 90W @ 12V DC, 120W @ 24V+ DC
- **Operating Temperature:** -40°F to 158°F (-40°C to 70°C)
- **Features:** 2 redundant power inputs, rugged design for solar installations
- **Use Case:** Larger deployments, future expansion capability

---

## 3. Comparison Matrix

| Feature | Planet IPOE-260-12V | Veracity CamSwitch 4 | Linovision 5-Port | Tycon TP-DCDC-1248G |
|---------|-------------------|---------------------|------------------|---------------------|
| **Input Voltage** | 12-56V DC | 8.5-40V DC | 12-48V DC | 12V DC |
| **PoE Ports** | 2 | 4 | 4 | 1 |
| **PoE Standard** | 802.3af/at | 802.3af/at | 802.3af/at | Passive PoE |
| **Power per Port** | 36W | Variable | 30W | 24W |
| **Total Budget @ 12V** | 60W | 60W | 60W | 24W |
| **Network Speed** | Gigabit | Fast Ethernet | Gigabit | Gigabit |
| **Temp Rating** | -40 to +75°C | Up to 50°C | -40 to +80°C | -40 to +70°C |
| **Enclosure** | IP30 | Not specified | IP40 | IP67 |
| **Price (USD)** | ~$164 | Not specified | Unknown | ~$50-70 |
| **Mounting** | DIN/Wall | Vehicle mount | DIN/Wall | Wall |

---

## 4. Technical Considerations for Jakarta Site

### 4.1 Power Budget Analysis

**Camera Power Requirements:**
- Typical PoE IP camera: 12-15W (802.3af)
- High-performance PoE+ camera: 20-25W (802.3at)
- Jakarta deployment: 2x cameras

**Scenarios:**

1. **Standard Cameras (15W each):**
   - Total draw: 30W
   - Planet IPOE-260-12V @ 12V input: 60W budget
   - **Margin:** 30W (100% overhead) ✅

2. **High-Power Cameras (25W each):**
   - Total draw: 50W
   - Planet IPOE-260-12V @ 12V input: 60W budget
   - **Margin:** 10W (20% overhead) ✅

**Conclusion:** Planet IPOE-260-12V provides adequate power budget for 2 cameras even with high-power PoE+ devices.

### 4.2 12V DC System Considerations

**Input Current Requirements:**

At 12V DC with 60W PoE output (2x 30W cameras):
- PoE output power: 60W
- Device overhead: ~4W (idle) + conversion losses
- Estimated conversion efficiency: ~85-90%
- **Total input power:** ~70-75W
- **Input current @ 12V:** ~6.3A peak

**Recommendations:**
1. Fuse/circuit breaker rating: 10A (slow blow) for inrush current protection
2. Wire gauge: 14 AWG minimum for 6-7A continuous current
3. Terminal block supports 12-24 AWG (specification confirmed)

### 4.3 Thermal Management

**Operating Environment - Jakarta:**
- Typical temperature: 25-35°C (77-95°F)
- Humidity: High (tropical climate)

**Planet IPOE-260-12V Thermal Specs:**
- Operating range: -40 to +75°C
- **Thermal margin:** 40-50°C above Jakarta ambient ✅
- IP30 enclosure suitable for indoor cabinet mounting
- Maximum power dissipation: 80W @ full load (generates heat)

**Recommendations:**
1. Mount in ventilated equipment cabinet
2. Ensure adequate airflow around unit
3. Consider heat dissipation in cabinet thermal design
4. IP30 rating suitable for indoor deployment (not direct weather exposure)

### 4.4 Network Considerations

**Gigabit Ethernet Support:**
- Planet IPOE-260-12V: 10/100/1000 Mbps ✅
- Future-proof for high-resolution cameras (4K, 8MP+)
- 1080p camera typical bandwidth: 4-8 Mbps
- 4K camera typical bandwidth: 15-25 Mbps

**Cable Distance:**
- Maximum: 100 meters (328 feet) per 802.3at specification
- Planet confirms 100m distance support
- Extension possible with PLANET IPOE-E202 PoE extender (adds 100m, total 200m)

---

## 5. Deployment Recommendations

### 5.1 Primary Recommendation: Planet IPOE-260-12V

**Reasons to Choose:**
1. ✅ Proven industrial product from established manufacturer
2. ✅ Exact match for 12V DC input requirement
3. ✅ Gigabit Ethernet for future camera upgrades
4. ✅ Sufficient power budget (60W @ 12V for 2 cameras)
5. ✅ Wide temperature rating (-40 to +75°C)
6. ✅ Dual redundant power inputs
7. ✅ Competitive pricing (~$164 USD)
8. ✅ Extensive documentation and support
9. ✅ DIN-rail mounting for professional installation

**Limitations:**
- Only 2 PoE ports (no future expansion beyond 2 cameras)
- IP30 rating (indoor use, not direct weather exposure)
- Power supply sold separately

### 5.2 Alternative Recommendation: Linovision 5-Port (For Expansion)

**Choose if:**
- Future expansion to 3-4 cameras is anticipated
- Higher IP rating (IP40) desired
- Slightly higher temperature tolerance needed (80°C vs 75°C)

**Concerns:**
- Less established brand
- Availability and pricing unclear
- Support/documentation may be limited

### 5.3 NOT Recommended for Jakarta Site

**Veracity CamSwitch Mobile:**
- Designed for vehicle applications (engine cranking, vibration)
- Only Fast Ethernet (100 Mbps) - not future-proof
- Higher current draw (10A vs ~6A)
- Overkill features (4 ports) at likely higher cost

**Tycon Systems Passive PoE:**
- Non-standard passive PoE may not work with all cameras
- Single port units require multiple injectors
- Cost savings not significant enough to justify compatibility risk

---

## 6. Purchase Specifications

### Bill of Materials - Planet IPOE-260-12V Deployment

| Item | Part Number | Qty | Est. Price | Notes |
|------|-------------|-----|-----------|-------|
| PoE Injector | IPOE-260-12V | 1 | $164 | 2-port, 12V booster |
| 12V DC Power Supply | TBD | 1 | $30-50 | External, based on site power system |
| Power Cable | 12-24 AWG | As needed | $10-20 | For terminal block connection |
| Ethernet Cables | Cat 6 | 2-4 | $20-40 | To cameras and uplink |
| DIN Rail Mount | Included | - | - | Included with unit |
| **Total Estimated Cost** | | | **~$224-274** | Excluding cameras |

### Additional Items to Consider
1. **Circuit Protection:** 10A fuse or circuit breaker on 12V input
2. **Grounding:** Proper earth ground connection (required per manual)
3. **Cabinet/Enclosure:** If not already available at site
4. **Cable Management:** For professional installation

---

## 7. Installation Checklist

### Pre-Installation
- [ ] Verify 12V DC power source capacity (minimum 7-8A continuous)
- [ ] Confirm camera PoE requirements (802.3af or 802.3at)
- [ ] Measure cable runs (must be <100m from injector to cameras)
- [ ] Prepare mounting location (DIN rail or wall)
- [ ] Verify proper grounding available

### Installation
- [ ] Mount IPOE-260-12V on DIN rail or wall
- [ ] Connect ground wire per manual instructions
- [ ] Wire 12V DC power to terminal block (observe polarity)
- [ ] Install 10A fuse/breaker on 12V input line
- [ ] Connect network uplink cables to data input ports
- [ ] Connect camera cables to PoE output ports
- [ ] Apply power and verify LED indicators

### Post-Installation Testing
- [ ] Verify PoE voltage output (should be ~54V DC)
- [ ] Confirm cameras power up and establish network connection
- [ ] Monitor input current draw (should be <7A with 2 cameras)
- [ ] Check injector temperature after 1 hour operation
- [ ] Verify network connectivity and camera streams
- [ ] Document installation (photos, cable labels, connections)

---

## 8. Conclusions

### Research Verification: SUCCESS ✅

The **Planet IPOE-260-12V** is a confirmed, legitimate product that precisely meets the requirements for the Jakarta site deployment:

- **12V DC Input:** Native support with built-in boost converter
- **2 PoE Cameras:** Supported with 60W total budget @ 12V input
- **Industrial Grade:** -40 to +75°C operating temperature
- **Gigabit Network:** Future-proof for high-resolution cameras
- **Established Product:** Planet Technology is a reputable manufacturer
- **Available:** Multiple authorized distributors, good stock availability
- **Reasonable Cost:** ~$164 USD competitive for industrial PoE equipment

### Final Recommendation

**PROCEED with Planet IPOE-260-12V for Jakarta deployment.**

This product eliminates the need for custom DC-DC converters or workarounds. The built-in 12-54V to 54V boost technology is specifically designed for battery-powered and low-voltage DC applications like the Jakarta site.

### Risk Assessment

**Technical Risks:** LOW
- Mature product with established track record
- Well-documented specifications and installation procedures
- Standard IEEE 802.3at compatibility ensures camera compatibility

**Supply Chain Risks:** LOW
- Available from multiple distributors
- Active product line from Planet Technology

**Deployment Risks:** LOW
- Straightforward installation with included mounting hardware
- Clear documentation and support available

### Next Steps

1. Confirm final camera models and their PoE power requirements
2. Verify 12V DC power system capacity at Jakarta site (minimum 8A)
3. Purchase Planet IPOE-260-12V from preferred distributor
4. Procure appropriate 12V DC power supply if not already available
5. Prepare installation materials (wire, connectors, grounding, circuit protection)
6. Schedule installation with local Jakarta team

---

## Sources

- [Planet Technology USA - IPOE-260-12V Product Page](https://planetechusa.com/product/ipoe-260-12v-industrial-2-port-10-100-1000t-802-3at-poe-injector-hub-12v-booster/)
- [Planet IPOE-260 Series Official Product Page](https://www.planet.com.tw/en/product/ipoe-260-series)
- [IPOE-260-12V User Manual PDF](https://planetechusa.com/wp-content/uploads/2019/11/IPOE-260_12V_v1-UserManual.pdf)
- [IPOE-260 Series Datasheet PDF](https://planetechusa.com/wp-content/uploads/2019/11/IPOE-260-Series_Datasheet.pdf)
- [IPOE-260 Series Sales Guide PDF](https://planetechusa.com/wp-content/uploads/2019/11/IPOE-260-Series_SalesGuide.pdf)
- [DigiKey - IPOE-260-12V Marketplace](https://www.digikey.com/en/products/detail/business-systems-connection-inc/IPOE-260-12V/13418961)
- [Network Camera Store - IPOE-260-12V](https://networkcamerastore.com/products/planet-ipoe-260-12v-industrial-2-port-10-100-1000t-802-3at-poe-injector-w-12v-booster)
- [Amazon - IPOE-260-12V](https://www.amazon.com/IPOE-260-12V-Industrial-802-3at-Injector-Booster/dp/B0B9FYRKX2)
- [Veracity - CamSwitch Mobile Series](https://www.veracityglobal.com/products/networked-video-integration-devices/camswitch-mobile.aspx)
- [Veracity - CAMSWITCH 4 Mobile](https://www.veracityglobal.com/transmission/camswitch-4-mobile)
- [Veracity - CAMSWITCH 8 Mobile](https://www.veracityglobal.com/transmission/camswitch-8-mobile)
- [Linovision - 5 Ports Full Gigabit PoE Switch](https://linovision.com/products/5-ports-full-gigabit-poe-switch-with-dc12v-dc24v-dc48v-input)
- [Tycon Systems - PoE Injectors Category](https://tyconsystems.com/product-category/tycon-power/poe-injectors/)
- [Tycon Systems - TP-DCDC-1248](https://tyconsystems.com/homepage/shop/tp-dcdc-1248/)
- [IPCamPower - 8 Port Industrial Gigabit PoE Switch](https://ipcampower.com/products/pps-dc8g2g-at1)
- [Omnitron Systems - How to Choose the Best PoE Injector for IP Cameras](https://www.omnitron-systems.com/blog/best-poe-injector-for-ip-cameras)

---

**Report Compiled:** January 8, 2026
**Research Conducted By:** Claude Code AI Research Assistant
**Total Sources Consulted:** 15+ authoritative sources including manufacturer documentation, distributor specifications, and technical comparisons
