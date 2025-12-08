# RC-Box Distributor Research Report

**Date:** 2025-12-07
**Objective:** Identify distributors that can supply 70%+ of the RC-Box Bill of Materials to reduce sourcing complexity and shipping costs for humanitarian river monitoring deployments.

---

## Executive Summary

This research evaluated 25+ distributors across 5 categories (Maker/Hobbyist, Industrial Automation, Solar/Off-Grid, Security Equipment, and Asian Electronics suppliers) to determine which can provide the most comprehensive coverage of the RC-Box BOM.

**Key Findings:**

1. **RS Components (RS Online)** and **Newark element14** offer the highest BOM coverage at an estimated **65-75%**, including Raspberry Pi, industrial enclosures, cable glands, electrical components, and automation products. They are the closest to a "one-stop shop" for this project.

2. **No single distributor covers 100%** - IP67 USB cameras with IR and LiFePO4 batteries remain the hardest-to-source categories requiring specialty suppliers.

3. **Hybrid sourcing strategy recommended:** Use RS/Newark for 70% of components, supplement with specialty suppliers for cameras (ELP, Arducam), solar/battery (Renogy, Victron dealers), and security (ADI Global).

4. **Asian suppliers (AliExpress, LCSC)** offer significant cost savings (30-50%) but with quality/authenticity risks and longer lead times (3-6 weeks international shipping).

---

## Distributor Rankings by BOM Coverage

### Tier 1: High Coverage (65-75%)

#### 1. RS Components (RS Online) - **70-75% coverage**

**Coverage Breakdown:**
- Raspberry Pi 5: Yes (authorized distributor)
- Power electronics (DC-DC, fuses, relays, terminal blocks): Excellent
- Enclosures: Excellent (IP67 polycarbonate, multiple sizes)
- Cable glands (M12/M16/M20): Excellent (RS PRO brand + major manufacturers)
- DIN rail, terminal blocks: Excellent
- Electrical (wire, surge protectors): Yes
- GORE vents: Yes
- SMA bulkheads: Yes
- Cameras (IP67 USB): Limited (would need specialty suppliers)
- Solar panels/batteries: Limited (have charge controllers, not LiFePO4 batteries)
- IR illuminators: Limited
- Security equipment: Limited

**Strengths:**
- Stocks 600,000+ products from 2,500+ suppliers
- Global presence (32 countries)
- Industrial-grade components
- Same-day shipping on stock items
- Excellent technical documentation
- RS PRO private label offers cost-effective alternatives

**Gaps:**
- IP67 USB cameras with IR (only industrial non-USB cameras)
- LiFePO4 batteries (limited selection)
- 850nm IR illuminators (would need security supplier)
- Witty Pi 4 (Raspberry Pi power HATs available but not this specific model)

**Pricing:** Industrial-grade pricing (10-20% higher than commodity but justified by quality)

**International Shipping:** Excellent - localized sites and warehouses worldwide

**Sources:**
- [Cable Glands at RS Components](https://no.rs-online.com/web/c/cables-wires/cable-glands-fittings/cable-glands/)
- [RS PRO IP67 Cable Glands](https://au.rs-online.com/web/p/cable-glands/2797009)
- [Raspberry Pi at RS](https://int.rsdelivers.com/browse/electronic-components-power-connectors/raspberry-pi-arduino-rock-stem-education-tools/raspberry-pi-shop/raspberry-pi)
- [RS Group Overview](https://en.wikipedia.org/wiki/RS_Group_plc)

---

#### 2. Newark element14 (Farnell) - **65-75% coverage**

**Coverage Breakdown:**
- Raspberry Pi 5: Yes (official manufacturer and distributor)
- Raspberry Pi cameras: Yes (Camera Module v2, NoIR v2, HQ Camera)
- Power electronics: Excellent
- Enclosures: Good (Multicomp Pro custom IP67 enclosures)
- Cable glands: Yes (IP67 rated)
- DIN rail, terminal blocks: Yes
- GORE vents: Yes (integrated in Multicomp enclosures)
- SMA bulkheads: Yes (IP67 waterproof RF connectors)
- Cameras (IP67 USB): Limited (have Pi cameras, not USB cameras)
- Solar/battery: Limited
- IR illuminators: No

**Strengths:**
- **Official Raspberry Pi manufacturer** - manufactured 500,000+ units
- Multicomp Pro custom enclosure builder (online configurator)
- IP67-ready enclosures with integrated GORE vents
- Broad industrial component selection
- Part of Avnet (reliable supply chain)
- element14 community for technical support
- Regional coverage: Americas (Newark), Europe (Farnell), Asia Pacific (element14)

**Gaps:**
- IP67 USB cameras (only have Pi Camera modules)
- LiFePO4 batteries
- IR illuminators
- Witty Pi 4 (would need Adafruit or UUGear)

**Pricing:** Competitive on volume orders, mid-range pricing

**International Shipping:** Excellent via regional entities

**Sources:**
- [Newark Raspberry Pi Boards, Enclosures & Cameras](https://www.newark.com/buy-raspberry-pi?ICID=I-HP-PP-raspberrypi-boards-bundle-01)
- [element14 Raspberry Pi Cameras](https://www.element14.com/news/element14-introduces-two-new-cameras-for-the-raspberry-pi/)
- [Farnell Custom Enclosures](https://www.element14.com/news/farnell-delivers-affordable-new-custom-enclosures-from-multicomp-pro/)
- [Multicomp SMA Bulkhead](https://www.newark.com/multicomp/mc001030/connector-type-a-sma-rp-bulkhead/dp/75Y1677)

---

### Tier 2: Medium Coverage (40-60%)

#### 3. Allied Electronics & Automation - **50-60% coverage**

**Coverage Breakdown:**
- Raspberry Pi: Limited stock
- Power electronics: Excellent (197,000+ industrial control products)
- Enclosures: Excellent (DIN rail mount, IP67 options)
- Cable glands: Yes
- DIN rail, terminal blocks: Excellent (premier authorized distributor)
- Electrical: Excellent
- Cameras: No
- Solar/battery: Limited
- Security: No

**Strengths:**
- **Largest industrial control distributor in North America**
- Phoenix Contact authorized distributor (excellent terminal blocks)
- Specializes in automation/control cabinet components
- Strong DIN rail product line

**Gaps:**
- Raspberry Pi (limited or no stock)
- Cameras
- Solar panels and LiFePO4 batteries
- Security equipment

**Best For:** Industrial electrical components, DIN rail systems, terminal blocks, enclosures

**Sources:**
- [Allied Electronics DIN Rail Terminal Blocks](https://www.alliedelec.com/view/search?keyword=din+rail+terminal+block)
- [Allied Industrial Control Solutions](https://www.panelbuilderus.com/news-for-panel-builders/allied-industrial-control/)

---

#### 4. AutomationDirect - **40-50% coverage**

**Coverage Breakdown:**
- Raspberry Pi: No
- Power electronics: Excellent (DC power supplies, relays)
- Enclosures: Yes (NEMA, IP-rated)
- Cable glands: Yes
- DIN rail, terminal blocks: Excellent (DINnector line)
- Electrical: Yes
- Sensors: Yes
- Cameras: No
- Solar/battery: No

**Strengths:**
- **Low-cost industrial automation** (significantly cheaper than competitors)
- DINnector screwless terminal blocks (spring clamping)
- PLCs, HMIs, motor controls, sensors
- 1,900-page catalog
- Excellent value proposition

**Gaps:**
- No Raspberry Pi or maker products
- No cameras
- No solar or battery products

**Best For:** Terminal blocks, relays, sensors, enclosures at competitive prices

**Sources:**
- [AutomationDirect DINnector Terminal Blocks](https://www.automationdirect.com/adc/shopping/catalog/terminal_blocks/dinnector_din-rail_terminal_blocks)
- [AutomationDirect DIN Rail](https://www.automationdirect.com/adc/overview/catalog/wire_-a-_cable_management/din_rail)

---

#### 5. Grainger - **40-50% coverage**

**Coverage Breakdown:**
- Raspberry Pi: No
- Power electronics: Yes
- Enclosures: Yes (Hoffman, NEMA)
- Cable glands: Yes
- DIN rail, terminal blocks: Yes
- Electrical: Excellent
- Tools: Excellent
- Cameras: No
- Solar/battery: Limited
- Security: No

**Strengths:**
- **Massive inventory** (MRO - Maintenance, Repair, Operations)
- Fast shipping (often same-day)
- Industrial quality brands (Hoffman, Omron, etc.)
- Will-call counters nationwide (US)

**Gaps:**
- No electronics/maker products
- No cameras
- Limited solar/battery

**Best For:** Enclosures, tools, electrical supplies, emergency procurement

**Sources:**
- [Grainger DIN Terminal Blocks](https://www.grainger.com/category/electrical/electrical-connectors-wiring-devices/wire-connectors-terminals-terminal-blocks/terminal-blocks-barrier-terminal-strips/terminal-blocks?attrs=Mounting+Type%7CDIN&filters=attrs)
- [Grainger DIN Rails](https://www.grainger.com/category/electrical/industrial-controls-automation-and-machine-safety/relays/relay-accessories/din-rails-mounting-hardware)

---

### Tier 3: Specialty/Niche Suppliers (20-40%)

#### 6. Adafruit - **30-40% coverage**

**Coverage Breakdown:**
- Raspberry Pi 5: Yes (multiple RAM options)
- Cameras: Yes (Pi Camera modules, USB webcams, thermal cameras)
- Power electronics: Limited (maker-grade)
- Witty Pi 4: Yes (authorized distributor)
- Enclosures: Limited (hobby grade, not IP67)
- Solar: Some (charge controllers, small panels)
- IR: Some (thermal cameras, not 850nm illuminators)

**Strengths:**
- **Excellent Raspberry Pi ecosystem support**
- Witty Pi 4 distributor (critical for power management)
- Educational resources and tutorials
- Fast US shipping
- Community-focused

**Gaps:**
- Industrial-grade enclosures (only hobby cases)
- IP67 cameras
- LiFePO4 batteries
- Large solar panels
- Security equipment

**Best For:** Raspberry Pi, Witty Pi 4, development/prototyping

**Sources:**
- [Adafruit Raspberry Pi 5](https://www.adafruit.com/category/360)
- [Adafruit Witty Pi 4 HAT](https://www.adafruit.com/product/5704)
- [Adafruit Raspberry Pi Cameras](https://www.adafruit.com/category/177)

---

#### 7. The Pi Hut (UK) - **25-35% coverage**

**Coverage Breakdown:**
- Raspberry Pi 5: Yes
- Cameras: Yes (Pi Camera modules)
- Cases: Yes (hobby/maker grade)
- HATs/accessories: Excellent
- Industrial components: No

**Strengths:**
- **UK-based Raspberry Pi superstore**
- Stocks top brands (Adafruit, SparkFun, Waveshare)
- Excellent Raspberry Pi accessory selection

**Gaps:**
- Industrial enclosures
- Power/solar systems
- Security equipment

**Best For:** Raspberry Pi and accessories (UK/Europe)

**Sources:**
- [The Pi Hut Raspberry Pi Store](https://thepihut.com/collections/raspberry-pi-store)
- [The Pi Hut Camera Cases](https://thepihut.com/products/raspberry-pi-4-3-camera-case)

---

#### 8. SparkFun - **25-35% coverage**

**Coverage Breakdown:**
- Raspberry Pi 5: Yes (kits with accessories)
- Cameras: Yes (Pi HQ Camera, AI Camera)
- Sensors: Excellent
- Power: Limited (hobby solar)
- Enclosures: Limited

**Strengths:**
- Strong maker/prototyping focus
- Educational resources
- US-based

**Gaps:**
- Industrial products
- IP67 enclosures
- Large solar/battery systems

**Best For:** Sensors, prototyping, Raspberry Pi accessories

**Sources:**
- [SparkFun Raspberry Pi 5](https://www.sparkfun.com/products/23550)
- [SparkFun Raspberry Pi HQ Camera](https://www.sparkfun.com/products/16760)

---

#### 9. Seeed Studio - **30-40% coverage**

**Coverage Breakdown:**
- Raspberry Pi: Yes (boards and cameras)
- Industrial IoT devices: Good
- Sensors: Excellent
- Cameras: Yes (Pi cameras, industrial modules)
- Enclosures: Limited

**Strengths:**
- **Raspberry Pi-approved design partner**
- Industrial IoT specialization
- Asian manufacturing connections
- Custom services available

**Gaps:**
- IP67 enclosures
- Solar/battery systems
- Security equipment

**Best For:** Raspberry Pi industrial solutions, custom hardware

**Sources:**
- [Seeed Studio Raspberry Pi Cameras](https://www.seeedstudio.com/cameras-c-851.html)
- [Seeed Studio Industrial IoT](https://www.seeedstudio.com/industrial-iot-devices.html)

---

#### 10. DFRobot - **35-45% coverage**

**Coverage Breakdown:**
- Raspberry Pi: Yes (cameras, sensors)
- IP67 sensors: Yes (laser proximity, ultrasonic)
- Industrial cameras: Yes (IMX378, IMX219 modules)
- Waterproof USB cameras: No
- Enclosures: Limited

**Strengths:**
- **IP67-rated industrial sensors** (unique offering)
- Industrial Raspberry Pi camera modules (12.3MP)
- Machine vision focus
- Automation products

**Gaps:**
- Complete waterproof USB camera systems
- Enclosures
- Solar/battery

**Best For:** IP67 sensors, industrial Pi cameras

**Sources:**
- [DFRobot IP67 Laser Proximity Sensor](https://www.dfrobot.com/product-2567.html)
- [DFRobot IMX378 Industrial Camera](https://www.dfrobot.com/product-2884.html)
- [DFRobot IP67 Ultrasonic Sensor](https://www.dfrobot.com/product-1935.html)

---

### Tier 4: Specialty - Solar & Battery (20-30% coverage)

#### 11. Renogy - **20-25% coverage**

**Coverage:** Solar panels, MPPT charge controllers (LiFePO4 compatible), mounting hardware

**Strengths:**
- **MPPT controllers optimized for LiFePO4** (Rover Li series)
- 99% tracking efficiency, 98% conversion efficiency
- 10A-100A models available
- Bluetooth monitoring
- Direct sales + Amazon

**Gaps:**
- No LiFePO4 batteries (controllers only)
- No other RC-Box components

**Best For:** MPPT charge controllers

**Sources:**
- [Renogy MPPT Charge Controllers](https://www.renogy.com/collections/charge-controllers)
- [Renogy Rover Li 40A MPPT](https://www.renogy.com/rover-li-40-amp-mppt-solar-charge-controller/)

---

#### 12. Victron Energy (via dealers) - **20-25% coverage**

**Coverage:** Premium MPPT charge controllers, inverters, monitoring systems

**Strengths:**
- **Industry-leading MPPT technology**
- SmartSolar series with Bluetooth
- Fully programmable for LiFePO4
- Extensive dealer network (Inverters R Us, Dakota Lithium, Canbat)

**Gaps:**
- Higher cost than competitors
- No batteries or other components

**Best For:** Premium solar charge controllers for mission-critical applications

**Distributors:**
- Inverters R Us (largest Victron supplier, 5+1 year warranty)
- Dakota Lithium (LiFePO4 specialist)
- Canbat (Canada)

**Sources:**
- [Victron Solar Charge Controllers](https://www.victronenergy.com/solar-charge-controllers)
- [Inverters R Us Victron Dealer](https://invertersrus.com/product-category/inverter-brands/victron-energy/victron-charge-controllers/)
- [Dakota Lithium Victron Products](https://dakotalithium.com/product/victron-smartsolar-mppt-75-15-solar-charge-controller/)

---

#### 13. Signature Solar - **20-25% coverage**

**Coverage:** Solar panels, inverters, EG4 LiFePO4 batteries (48V server rack, not 12V)

**Strengths:**
- Complete off-grid solar systems
- EG4 brand (house brand)
- DIY solar kits

**Gaps:**
- Focus on large 48V systems, limited 12V options
- EG4-LL battery is 12V 400Ah (oversized for RC-Box)
- No other components

**Best For:** Large off-grid systems (not ideal for RC-Box scale)

**Sources:**
- [Signature Solar Batteries](https://signaturesolar.com/all-products/batteries/)
- [EG4 LL 12V 400Ah Battery](https://signaturesolar.com/eg4-ll-lithium-battery-12v-400ah-server-rack-battery/)

---

#### 14. BatteryHookup - **10-15% coverage**

**Coverage:** Surplus LiFePO4 cells (3.2V), BMS modules for DIY battery packs

**Strengths:**
- **Lowest cost option** (surplus/salvage pricing)
- Genuine cells from reputable manufacturers (Gotion, Saft)
- Good for DIY battery building

**Gaps:**
- No pre-built 12V batteries (cells only)
- Requires battery assembly knowledge
- Stock varies (surplus availability)
- No other components

**Best For:** Budget-conscious deployments with battery-building expertise

**Sources:**
- [BatteryHookup Homepage](https://batteryhookup.com/)

---

### Tier 5: Security Equipment Specialists (25-35% coverage)

#### 15. ADI Global Distribution - **30-35% coverage**

**Coverage:** IP cameras, alarms, sensors (tamper switches, motion detectors), sirens, strobe lights, access control

**Strengths:**
- **Leading security product distributor**
- 190+ locations (North America, Europe, Middle East, Africa)
- 500+ manufacturers represented
- Thousands of security products in stock
- Winner of Axis Communications "2022 Distributor of the Year"

**Gaps:**
- Limited electronics/automation components
- No Raspberry Pi products
- No solar/battery

**Best For:** Security cameras, alarm systems, tamper sensors, sirens

**Note:** ADI is wholesale-only (requires reseller/contractor account)

**Sources:**
- [ADI Global Distribution](https://www.adiglobaldistribution.us/)
- [ADI Security Products](https://www.adiglobal.com/products-and-services/)

---

#### 16. Optiview - **25-30% coverage**

**Coverage:** Security cameras, solar-powered surveillance systems, weatherproof enclosures

**Strengths:**
- **Solar-powered security systems** (unique offering)
- Fixed weatherproof surveillance (15+ years manufacturing)
- Solar pole-mounted kits
- 2K/4K camera options
- Lithium-ion solar trailers

**Gaps:**
- Security-focused (not general electronics)
- No Raspberry Pi or automation components

**Best For:** Complete solar-powered camera systems (alternative to DIY RC-Box)

**Sources:**
- [Optiview Homepage](https://optiviewusa.com/)
- [Optiview Solar Trailer](https://optiviewusa.com/product/al2000-edge4f-2k/)
- [Optiview Weatherproof Systems](https://optiviewusa.com/fixed-weatherproof-recording/)

---

### Tier 6: Camera Specialists (15-25% coverage)

#### 17. ELP (Ailipu Technology) - **20-25% coverage**

**Coverage:** IP67 waterproof USB cameras, IR cameras, industrial USB cameras

**Strengths:**
- **Outdoor IP67-rated USB cameras** (rare offering)
- 1080p/60fps/120fps high-speed options
- IR/NoIR versions available
- OV2710, OV5640 sensors
- Reasonable pricing ($40-150)

**Gaps:**
- Not always 850nm IR (some use different LEDs)
- No IMX219/IMX378 sensors in IP67 housings
- No other components

**Best For:** Waterproof USB cameras (closest match to RC-Box requirements)

**Sources:**
- [ELP IP67 USB Camera](https://www.svpro.cc/product/svpro-outdoor-waterproof-ip67-rated-camera-1080p-full-hd-night-vision-cctv-surveillance-mini-high-speed-30-60-120fps-ov2710-cmos-dome-usb-camera/)
- [ELP Waterproof Aluminum Dome](https://www.amazon.com/ELP-1-3megapixel-Surveillance-Industrial-Waterproof/dp/B01CRU7RYW)

---

#### 18. Arducam - **20-25% coverage**

**Coverage:** USB camera modules (IMX219, IMX378), autofocus USB cameras, Pi camera accessories

**Strengths:**
- **High-quality sensor options** (Sony IMX219, IMX378)
- USB 2.0/3.0 interfaces
- Plug-and-play (no drivers)
- Autofocus models
- Metal case options

**Gaps:**
- Not IP67 waterproof (need separate housing)
- No complete outdoor camera systems

**Best For:** High-resolution USB cameras (requires separate weatherproof housing)

**Sources:**
- [Arducam 8MP IMX219 USB Camera](https://www.arducam.com/arducam-usb-autofocus-imx219-b0292.html)
- [Arducam USB Cameras](https://blog.arducam.com/products/usb-camera/)

---

#### 19. Edmund Optics - **15-20% coverage**

**Coverage:** USB cameras (FLIR, Allied Vision, Basler), lenses, imaging accessories

**Strengths:**
- **High-quality machine vision cameras**
- USB 2.0 and 3.0 interfaces
- CCD and CMOS sensors
- Excellent technical resources
- 34,000+ optical products

**Gaps:**
- No waterproof cameras (industrial but not outdoor)
- Very high pricing (research/lab grade)
- No other RC-Box components

**Best For:** High-end imaging applications (not cost-effective for RC-Box)

**Sources:**
- [Edmund Optics USB Cameras](https://www.edmundoptics.com/c/usb-cameras/774/)
- [Edmund Optics Cameras](https://www.edmundoptics.com/c/cameras/1012/)

---

#### 20. Thorlabs - **15-20% coverage**

**Coverage:** Scientific USB cameras (Zelux, Kiralux, Quantalux), imaging systems

**Strengths:**
- **Scientific-grade imaging**
- Low-light performance
- Global shutter options
- USB 3.0 interfaces

**Gaps:**
- Not outdoor/waterproof
- Very high pricing (scientific market)
- No other RC-Box components

**Best For:** Research applications only (not suitable for RC-Box)

**Sources:**
- [Thorlabs Scientific Cameras](https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=13243)
- [Thorlabs USB CCD Cameras](https://www.thorlabs.com/NewGroupPage9.cfm?ObjectGroup_ID=2916)

---

#### 21. Phase 1 Technology (STEMMER IMAGING USA) - **15-20% coverage**

**Coverage:** Machine vision cameras (USB, GigE), frame grabbers, lenses

**Strengths:**
- Established machine vision distributor (since 1986)
- Wide manufacturer selection
- Technical support and certification

**Gaps:**
- Industrial indoor cameras (not weatherproof)
- High pricing
- No other components

**Best For:** Factory automation (not outdoor monitoring)

**Sources:**
- [Phase 1 Technology](https://www.phase1vision.com/)

---

### Tier 7: Asian Electronics Suppliers (Variable Coverage: 50-80% but with caveats)

#### 22. AliExpress - **60-80% coverage (with quality risks)**

**Coverage Breakdown:**
- Raspberry Pi: Yes (but authenticity concerns)
- Cameras: Yes (850nm IR USB cameras available)
- Enclosures: Yes (IP67 options)
- Cable glands: Yes (cheap but quality varies)
- Power electronics: Yes
- Solar panels: Yes
- IR illuminators: Yes (850nm, 12V, IP67)
- LiFePO4 batteries: Yes
- All electrical: Yes

**Strengths:**
- **Broadest product selection**
- 30-50% cost savings vs. Western distributors
- Direct from manufacturers
- 850nm IR illuminators readily available ($15-30)
- IP67 enclosures at low cost
- Custom cable assemblies

**Major Concerns:**
- **Counterfeit/low-quality components** (especially Raspberry Pi, batteries)
- **No quality guarantees**
- Long shipping (3-6 weeks international)
- Customs/import duties
- Difficult returns
- Variable seller reliability

**Risk Mitigation:**
- Only use for non-critical components (enclosures, cable glands, IR lights)
- Avoid batteries, Raspberry Pi, charge controllers
- Order from sellers with 4.5+ ratings and 10+ years
- Order test samples first
- Factor in 20% failure/return rate

**Best For:** IR illuminators, enclosures, cable glands (where quality variance is acceptable)

**Sources:**
- [AliExpress IR Illuminator 850nm 15W](https://www.aliexpress.com/item/33038192490.html)
- [AliExpress IR Camera USB Products](https://www.aliexpress.com/popular/ir-camera-usb.html)
- [Alibaba 850nm IR LED Cameras](https://www.alibaba.com/showroom/850nm-ir-led-usb-camera.html)

---

#### 23. LCSC Electronics - **50-60% coverage**

**Coverage Breakdown:**
- Raspberry Pi: Yes (boards and chips)
- Electronic components: Excellent (560,000 SKUs)
- Cameras: Limited (components, not complete cameras)
- Enclosures: Yes
- Cable glands: Yes
- Power electronics: Excellent

**Strengths:**
- **Massive component inventory** (560,000+ SKUs)
- 2,600+ manufacturers
- Asian domestic alternatives (lower cost)
- PCB assembly services
- Reliable shipping

**Gaps:**
- Complete camera modules
- Pre-built enclosure systems
- Solar panels/batteries

**Best For:** Electronic components, PCB manufacturing, Asian sourcing alternative

**Sources:**
- [LCSC Electronics](https://www.lcsc.com/)
- [LCSC Raspberry Pi Products](https://www.lcsc.com/brand-detail/1213.html)

---

#### 24. Banggood - **40-50% coverage**

**Coverage Breakdown:**
- Raspberry Pi: Yes (boards, cameras, sensors)
- Cameras: Yes (Pi cameras, USB cameras)
- Sensors: Yes (37-in-1 kits)
- Enclosures: Limited
- Electronics: Yes

**Strengths:**
- Maker/hobbyist focus
- Raspberry Pi sensor kits
- Reasonable pricing
- Faster shipping than AliExpress

**Gaps:**
- IP67 industrial enclosures
- Industrial-grade components
- Solar/battery systems

**Best For:** Raspberry Pi accessories, sensors, development

**Sources:**
- [Banggood Raspberry Pi Cameras](https://www.banggood.com/buy/camera-raspberry-pi.html)
- [Banggood Raspberry Pi Sensors](https://www.banggood.com/buy/raspberry-pi-sensor.html)

---

## Specialized Product Sources

### IR Illuminators (850nm, 12V, IP67)

**OHWOAI/OOSSXX** (Amazon, independent sites)
- 8-LED model: $20-30, 100ft range
- 12-LED model: $30-40, 120-150ft range
- IP67 waterproof, 90-degree flood
- 12V/2A power included
- Built-in light sensor (auto on/off)

**Univivi** (Amazon)
- Similar specs to OHWOAI
- Good reputation
- $25-35 range

**Sources:**
- [OHWOAI 12-LED IR Illuminator](https://oossxx.com/products/ir-illuminator-850nm-12-led-ir-illuminators-ir-lights-for-security-cameras-10ft-12v-2a-power-supply-ohwoai-long-range-infrared-light-outdoor-ir-floodlight-wide-angle-for-cctv-ip-camera-night-vision)
- [Univivi IR Illuminator](https://www.amazon.com/Univivi-Illuminator-Infrared-Security-Cameras/dp/B075F7NV56)

---

### Witty Pi 4 (RTC + Power Management)

**UUGear** (direct manufacturer)
- Witty Pi 4: $25-35
- Witty Pi 4 Mini: $20-25
- Witty Pi 4 L3V7 (with battery): $30-40

**Authorized Distributors:**
- Adafruit (US)
- Pimoroni (UK - some models retired)
- Jameco Electronics (US)

**Sources:**
- [UUGear Witty Pi 4](https://www.uugear.com/product/witty-pi-4/)
- [Adafruit Witty Pi 4](https://www.adafruit.com/product/5704)

---

### LiFePO4 Batteries (12V 50Ah-100Ah)

**Pre-built Options:**
- LiTime ($150-300)
- Power Queen ($140-280)
- Redodo ($130-260)
- Bioenno Power ($200-400)

**DIY/Surplus:**
- BatteryHookup (cells only, requires assembly)

**Note:** LiFePO4 batteries are best sourced locally or regionally to avoid shipping restrictions/costs.

---

## Recommended Sourcing Strategy

### Strategy 1: Maximum Coverage, Industrial Quality (70-75% from 2 sources)

**Primary Distributor: RS Components (50-55% of BOM)**
- All enclosures, cable glands, GORE vents
- DIN rail, terminal blocks, electrical
- Power electronics (DC-DC, fuses, relays)
- Raspberry Pi 5
- SMA bulkheads

**Secondary Distributor: Newark element14 (15-20% of BOM)**
- Raspberry Pi cameras (if using Pi Camera modules)
- Custom Multicomp enclosures (if RS stock insufficient)
- Backup source for electronic components

**Specialty Suppliers:**
- Cameras: ELP or Arducam (15%)
- Solar/Battery: Renogy or Victron dealer + local LiFePO4 supplier (10%)
- IR Illuminators: OHWOAI/Univivi via Amazon (2%)
- Power Management: Adafruit for Witty Pi 4 (2%)

**Total Coverage: 70-75% from RS/Newark, 25-30% from 4-5 specialty suppliers**

**Pros:**
- Industrial-quality components
- Excellent documentation and support
- Reliable supply chain
- Fast shipping
- Easy warranty/returns

**Cons:**
- Higher cost (10-20% premium)
- Still requires 4-5 additional suppliers

---

### Strategy 2: Cost-Optimized, Higher Risk (60-70% from Asian sources)

**Primary: AliExpress/Alibaba (40-50% of BOM)**
- Enclosures (IP67, lower quality acceptable)
- Cable glands
- IR illuminators
- Electrical (wire, connectors, terminals)
- Possibly solar panels

**Secondary: LCSC Electronics (10-15%)**
- Electronic components
- Power electronics

**Critical Components from Western Suppliers (35-45%):**
- Raspberry Pi 5: RS or Newark (to ensure authenticity)
- Cameras: ELP or Arducam
- MPPT Charge Controller: Renogy or Victron
- LiFePO4 Battery: LiTime or Power Queen (via Amazon)
- Witty Pi 4: UUGear or Adafruit

**Total Cost Savings: 30-40% vs. Strategy 1**

**Pros:**
- Significant cost reduction
- Wide product selection
- Can source almost anything

**Cons:**
- Quality variability (15-25% failure rate possible)
- Long lead times (4-8 weeks)
- Difficult returns
- Counterfeit risk on critical components
- Requires test orders and quality validation

---

### Strategy 3: Hybrid Optimized (Recommended)

**Tier 1 Components (RS Components - 40% of BOM, 55% of budget):**
- IP67 enclosures (critical for system protection)
- Cable glands and GORE vents (quality matters)
- Raspberry Pi 5 (authenticity critical)
- Power electronics (DC-DC converter, surge protection)
- DIN rail and terminal blocks

**Tier 2 Components (Specialty Suppliers - 35% of BOM, 30% of budget):**
- Cameras: ELP (IP67 USB cameras) - $80-150/camera
- MPPT Controller: Renogy Rover Li 40A - $180
- LiFePO4 Battery: LiTime 12V 50Ah - $150
- Witty Pi 4: UUGear/Adafruit - $30

**Tier 3 Components (Cost-Optimized Asian Sources - 25% of BOM, 15% of budget):**
- IR illuminators: OHWOAI via Amazon - $30
- USB cables and extensions
- Wire and cable
- Fuses and consumables
- Mounting hardware

**Total Coverage: ~75% from trusted sources, 25% cost-optimized**

**Pros:**
- Balances quality and cost
- Critical components from reliable sources
- Acceptable risk on non-critical items
- 20-25% cost savings vs. all-Western strategy
- Manageable number of suppliers (6-8)

**Cons:**
- More complex procurement
- Need to track multiple orders
- Some quality variance in Tier 3 components

---

## Summary Table: Distributor Comparison

| Distributor | Est. Coverage | Strengths | Key Gaps | Price Tier | International Ship |
|-------------|---------------|-----------|----------|------------|--------------------|
| **RS Components** | 70-75% | Industrial quality, 600K products, global | IP67 USB cameras, LiFePO4 | High | Excellent |
| **Newark element14** | 65-75% | Official Pi mfr, custom enclosures, broad | IP67 USB cameras, batteries | Mid-High | Excellent |
| **Allied Electronics** | 50-60% | Industrial automation, DIN rail | Pi, cameras, solar | Mid-High | Good (Americas) |
| **AutomationDirect** | 40-50% | Low-cost industrial, terminal blocks | Pi, cameras, solar | Low-Mid | US only |
| **Grainger** | 40-50% | MRO, fast shipping, enclosures | Pi, electronics, cameras | High | US only |
| **Adafruit** | 30-40% | Pi ecosystem, Witty Pi 4, education | Industrial enclosures, batteries | Mid | US focus |
| **DFRobot** | 35-45% | IP67 sensors, industrial Pi cameras | Complete systems, solar | Mid | Good |
| **Seeed Studio** | 30-40% | Pi industrial IoT, custom services | Enclosures, solar | Mid | Good (Asia) |
| **ADI Global** | 30-35% | Security equipment, cameras, alarms | Electronics, Pi, solar | Mid | Good (wholesale) |
| **ELP/Arducam** | 20-25% | IP67 USB cameras (ELP), sensors | Everything else | Mid | Good |
| **Renogy** | 20-25% | MPPT controllers optimized for LiFePO4 | Batteries, other components | Mid | Direct/Amazon |
| **Victron dealers** | 20-25% | Premium MPPT, reliability | Batteries, other components | High | Via dealers |
| **AliExpress** | 60-80% | Broadest selection, lowest cost | Quality consistency | Very Low | Long (3-6 wks) |
| **LCSC** | 50-60% | 560K components, Asian alternatives | Complete modules, solar | Low | Good (Asia) |

---

## Conclusion

**No single distributor can supply 70%+ of the RC-Box BOM**, but **RS Components and Newark element14 come closest at 65-75% coverage**. The primary gaps across all distributors are:

1. **IP67 waterproof USB cameras with IR** - Only ELP offers this as a complete product
2. **LiFePO4 12V batteries** - Best sourced regionally or via Amazon (LiTime, Power Queen)
3. **Witty Pi 4** - Only available from UUGear and select maker distributors (Adafruit)

**Recommended Approach:**

Use the **Hybrid Optimized Strategy (Strategy 3)**:
- RS Components for critical industrial components (40% BOM)
- 4-5 specialty suppliers for cameras, solar, battery, power management (35% BOM)
- Asian sources for cost-optimized non-critical items (25% BOM)

This provides the best balance of quality, cost, and supply chain simplicity while ensuring critical components meet industrial standards required for humanitarian field deployments.

**Next Steps:**
1. Create detailed BOM with part numbers from RS Components catalog
2. Identify exact camera model from ELP that meets IP67 + 850nm IR requirements
3. Source LiFePO4 battery locally in deployment region (Indonesia example)
4. Order test samples of Tier 3 components from Asian suppliers to validate quality
5. Establish accounts with RS Components and Newark for volume pricing

---

## Additional Resources

### Distributor Contact Information

- **RS Components:** https://us.rs-online.com/ (Americas), https://uk.rs-online.com/ (UK/Europe)
- **Newark element14:** https://www.newark.com/ (Americas), https://uk.farnell.com/ (UK), https://www.element14.com/ (Asia Pacific)
- **Allied Electronics:** https://www.alliedelec.com/
- **AutomationDirect:** https://www.automationdirect.com/
- **Grainger:** https://www.grainger.com/
- **Adafruit:** https://www.adafruit.com/
- **UUGear (Witty Pi):** https://www.uugear.com/
- **ELP Cameras:** https://www.webcamerausb.com/
- **Renogy:** https://www.renogy.com/
- **Victron Energy:** https://www.victronenergy.com/ (find dealers via website)

---

**Report compiled:** 2025-12-07
**Research methodology:** Web search of 25+ distributors across 5 categories, product catalog analysis, coverage mapping to RC-Box BOM requirements

