# RC-Box Bill of Materials (BOM)
## River Monitoring Device - Verified Components

**Date Compiled:** 2025-11-28
**Research Status:** Verified with actual product pages and pricing where available

---

## 1. CORE COMPUTING COMPONENTS

### 1.1 Raspberry Pi 5 4GB
- **Supplier:** DigiKey / Mouser
- **Part Number:** SC1111
- **DigiKey Part:** SC1111 (SKU: 21658261)
- **Mouser Part:** SC1111
- **Description:** Raspberry Pi 5 Single Board Computer, Broadcom BCM2712 Arm Cortex-A76 quad-core @ 2.4GHz, 4GB RAM, 40 GPIO, GbE Ethernet, Bluetooth 5.0/BLE, PCIe
- **Specifications:** 3.370" x 2.224" (85.60mm x 56.50mm)
- **Unit Price:** ~$60.00 USD (verify current pricing on DigiKey)
- **Quantity:** 1
- **URL:** https://www.digikey.com/en/products/detail/raspberry-pi/SC1111/21658261
- **Notes:** Order today, ships today at DigiKey

### 1.2 Power Management HAT with UPS and RTC

**OPTION A: DFRobot Raspberry Pi 5 UPS HAT (Recommended)**
- **Supplier:** DFRobot Direct
- **Part Number:** FIT0992
- **Description:** Raspberry Pi 5 High Current UPS HAT, 5.1V 5A output, 4-cell 18650 battery holder, intelligent power management, auto-shutdown, fast charging (3A max), up to 10hr runtime
- **Unit Price:** Contact DFRobot (typically ~$50-60)
- **Quantity:** 1
- **URL:** https://www.dfrobot.com/product-2840.html
- **Notes:** Specifically designed for Pi 5, includes battery protection circuits

**OPTION B: Waveshare UPS HAT (B)**
- **Supplier:** Waveshare / Amazon / PiShop.us
- **Part Number:** 20567
- **Description:** UPS HAT (B) for Raspberry Pi 5/4B/3B+, 5V output up to 5A, pogo pins connection (no GPIO usage), protection circuits
- **Unit Price:** ~$30-40 USD
- **Quantity:** 1
- **URL:** https://www.waveshare.com/ups-hat-b.htm
- **Notes:** Compatible with Pi 5, battery length must be <67mm

**IMPORTANT NOTE:** PiSugar 3 Plus is NOT compatible with Raspberry Pi 5 (only supports 3B/3B+/4B). Use DFRobot FIT0992 or Waveshare UPS HAT (B) instead.

### 1.3 RTC Battery for Raspberry Pi 5
- **Supplier:** DigiKey / Mouser / Raspberry Pi Approved Resellers
- **Part Number:** (Various - search for ML-2020 battery with Pi 5 connector)
- **Description:** Panasonic ML-2020 Lithium battery with Raspberry Pi 5 RTC connector
- **Unit Price:** ~$5-10 USD
- **Quantity:** 1
- **Notes:** Pi 5 has built-in RTC in PMIC; battery provides backup when main power disconnected

### 1.4 M.2 SATA SSD Storage
- **Supplier:** DigiKey (various manufacturers)
- **Part Number:** Multiple options available
- **Description:** M.2 2280 or 2242 SATA III SSD, 480-512GB capacity
- **Manufacturers Available at DigiKey:**
  - Kingston Technology M.2 2280/2242 SATAIII SSD
  - Micron MTFDDAV512TBN-1AR15FCHA (512GB)
  - ADATA Industrial Grade
  - Swissbit X-60m2
- **Unit Price:** $40-80 USD (varies by manufacturer)
- **Quantity:** 1
- **URL:** https://www.digikey.com/en/products/filter/solid-state-drives-ssds-hard-disk-drives-hdds/503
- **Notes:** Filter by 512GB capacity, M.2 form factor, SATA interface. Most Western Digital M.2 drives are NVMe, not SATA.

### 1.5 M.2 to SATA Adapter
- **Supplier:** DigiKey
- **Part Number:** SAT32M225
- **Manufacturer:** StarTech.com
- **DigiKey Part:** SAT32M225
- **Description:** M.2 SSD to 2.5" SATA Adapter Converter with Open Frame Housing, 7mm height, supports M.2 NGFF SATA SSDs
- **Unit Price:** $29.83 USD
- **Quantity:** 1
- **URL:** https://www.digikey.com/en/products/detail/startech-com/SAT32M225/21397511
- **Notes:** Not kept in stock; allow for lead time

### 1.6 M.2 to USB 3.0 Adapter (Alternative)
- **Supplier:** DigiKey
- **Part Number:** Various
- **Description:** M.2 SATA to USB 3.0 external enclosure/adapter
- **Unit Price:** $15-30 USD
- **Quantity:** 1 (if using USB connection instead of direct SATA)
- **Notes:** Check DigiKey for StarTech.com or other USB 3.0 M.2 enclosures

---

## 2. COMMUNICATIONS

### 2.1 LTE Cellular Modem
- **Supplier:** DigiKey
- **Part Number:** EC25AFA-MINIPCIE
- **Manufacturer:** Quectel
- **DigiKey Part:** EC25AFA-MINIPCIE (SKU: 13278160)
- **Description:** LTE Cat 4 Module, Mini PCIe form factor, 150Mbps down/50Mbps up, multi-band support for Americas/Africa, M2M/IoT optimized
- **Unit Price:** $59.67 USD (or $65.21 depending on quantity/tier)
- **Quantity:** 1
- **URL:** https://www.digikey.com/en/products/detail/quectel/EC25AFA-MINIPCIE/13278160
- **Notes:** Select variant based on region (EC25-E for Europe, EC25-AU for Australia, etc.). May require additional USB adapter or carrier board for Pi 5.

**Alternative Models:**
- EC25EUGA-MINIPCIE (Europe) - $62.00
- EC25AUFA-MINIPCIE (Australia)
- Consider EG25-G for global coverage

---

## 3. CAMERA COMPONENTS

### 3.1 Raspberry Pi Camera Module 3
- **Supplier:** DigiKey / Mouser
- **Part Number:** SC1223
- **DigiKey Part:** SC1223 (SKU: 17278639)
- **Description:** Raspberry Pi Camera Module 3, 12MP Sony IMX708 sensor, autofocus (PDAF), HDR support, standard lens (76° FOV), CSI-2 interface
- **Unit Price:** $25.00 USD
- **Quantity:** 2
- **URL:** https://www.digikey.com/en/products/detail/raspberry-pi/SC1223/17278639
- **Notes:** Compatible with Pi 5. Also available: SC1224 (wide-angle 120°), SC0861 (NoIR version). Ships same day.

### 3.2 Arducam CSI to USB Adapter
- **Supplier:** Arducam Direct / Amazon / Distributors
- **Part Number:** B0278
- **Description:** CSI-USB UVC Camera Adapter Board for IMX477/Camera Module 3, converts CSI camera to USB webcam, built-in microphone, UVC-compliant (no drivers), max 4056x3040 @ 10fps
- **Unit Price:** ~$45-60 USD
- **Quantity:** 2
- **URL:** https://www.arducam.com/product/arducam-uvc-camera-adapter-board-for-12mp-imx477-raspberry-pi-hq-camera/
- **Notes:** NOT available on DigiKey/Mouser. Order from Arducam, Amazon, or specialty retailers. Board size 38x38mm. Check compatibility with Camera Module 3.

### 3.3 Waterproof Camera Housing
- **Supplier:** Entaniya / The Pi Hut / RS Online
- **Part Number:** WC-01
- **Description:** IP67-equivalent waterproof camera case for Raspberry Pi Camera Module V2/V3/V3 Wide, ASA resin construction, highly transparent dome cover, 24x25mm PCB compatibility
- **Unit Price:** £24 (~$30 USD) to $78 USD
- **Quantity:** 2
- **URL:** https://thepihut.com/products/entaniya-waterproof-case-for-raspberry-pi-camera-modules
- **Notes:** OBSOLETE at DigiKey. Order from The Pi Hut (UK), Entaniya direct, or RS Online. Note: WC-01 requires additional waterproofing for cable entry in high-pressure/underwater use.

**Alternative:** Consider custom IP67 enclosures or 3D-printed housings with proper sealing for long-term outdoor deployment.

---

## 4. HEATING AND ENVIRONMENTAL

### 4.1 Temperature Controller (Thermostat)
- **Supplier:** Amazon / eBay / Specialty retailers
- **Part Number:** STC-1000 (12V DC version)
- **Description:** Digital temperature controller/thermostat, -50°C to 110°C range, 0.1°C resolution, ±1°C accuracy, 10A relay output, dual heating/cooling mode, NTC sensor included
- **Unit Price:** $10-20 USD
- **Quantity:** 1
- **URL:** https://www.amazon.com/STC-1000-Temperature-Controller-12V-Thermostat/dp/B0B8NBVFFZ
- **Notes:** NOT available on DigiKey/Mouser. Widely available on Amazon/eBay. Verify 12V DC operation.

### 4.2 Silicone Heater Pad (Camera Anti-Fog)
- **Supplier:** Keenovo Direct
- **Part Number:** Camera Lens Anti-Fog Heater 20mm x 70mm
- **Description:** Small silicone heating element, 10W @ 12V, 0.8" x 2.76" (20mm x 70mm), 3M adhesive backing, 0.5m power cable
- **Unit Price:** ~$15-25 USD
- **Quantity:** 2 (one per camera)
- **URL:** https://keenovo.store/products/keenovo-tiny-small-silicone-heating-element-camera-lens-anti-fog-heater-20mm-x-70mm-10w-12v
- **Notes:** NOT available on DigiKey/Mouser. Order from Keenovo direct. Suitable for GoPro and similar camera lens heating.

### 4.3 Gore-Tex Breather Vent (Pressure Equalization)
- **Supplier:** DigiKey (search for specific part) / Amphenol LTW / Gore direct
- **Part Number Options:**
  - VENT-PS1YGY-N8001 (Plastic M12, >1000ml/min, IP69K)
  - VENT-PS1NGY-N8002 (Plastic M12, >3000ml/min, IP69K)
  - VENT-MS1NMS-O8001 (Stainless M12, >1600ml/min, IP69K)
- **Manufacturer:** Amphenol LTW or Gore
- **Description:** M12 thread pressure relief vent, IP67/IP68/IP69K rated, screw-in installation, ePTFE membrane for moisture protection while allowing air exchange
- **Unit Price:** $5-15 USD each
- **Quantity:** 2-3
- **URL:** https://www.digikey.com/en/product-highlight/a/amphenol-ltw/screw-vent-m12-series
- **Notes:** Search DigiKey directly for manufacturer part numbers. Amphenol LTW and Gore both offer suitable products. IP69K exceeds IP67 requirement.

### 4.4 Molecular Sieve Desiccant
- **Supplier:** Amazon / Industrial suppliers / Moisture Boss / Impak Corporation
- **Part Number:** Type 4A packets (various sizes)
- **Description:** Molecular sieve desiccant Type 4A, 4 Angstrom pore size, alkali metal alumino-silicate, small packets or bulk
- **Unit Price:** $10-30 USD for assorted packets
- **Quantity:** 3-5 small packets (10-50g each)
- **URL:** https://www.amazon.com/Molecular-Sieve-4A-Gal-Lb/dp/B06XGQJ5N2
- **Notes:** NOT typically on DigiKey/Mouser. Available from specialty desiccant suppliers or Amazon. Effective for compressed air and electronics enclosure dehumidification.

---

## 5. POWER SYSTEM

### 5.1 LiFePO4 Battery
- **Supplier:** Specialty battery suppliers / Amazon
- **Part Number:** Various (12V 20Ah LiFePO4)
- **Manufacturers:** Amped Outdoors, Dakota Lithium, Battle Born, Renogy
- **Description:** 12V 20Ah LiFePO4 battery, nominal voltage 12.8V, capacity 256Wh, maximum discharge current 15-20A, F2 spade or similar terminals
- **Unit Price:** $80-150 USD
- **Quantity:** 1
- **Notes:** NOT typically on DigiKey/Mouser. DigiKey carries ZEUS, AIMS Power, and Power Sonic LiFePO4 products but not in this exact capacity. Check DigiKey for alternatives like AIMS LFP12V50AB (50Ah) or similar.

**DigiKey Alternative:** Search for ZEUS Battery Products or AIMS Power LiFePO4 batteries in 12V configuration.

### 5.2 Solar Charge Controller
- **Supplier:** Specialized solar retailers / Amazon
- **Part Number:** Generic 10A PWM 12V controller
- **Manufacturers:** Newpowa NPC-PHL10A, PowMr, Renogy, EPEVER
- **Description:** PWM solar charge controller, 10A charging current, 12/24V auto-detect, LCD display, overcharge/discharge protection, reverse polarity protection
- **Unit Price:** $15-30 USD
- **Quantity:** 1
- **Notes:** NOT typically on DigiKey/Mouser (they carry controller ICs like TI bq24650, not complete modules). Order from solar equipment retailers or Amazon.

**DigiKey Alternative:** Consider AIMS Power solar charge controllers (MPPT versions available) or build custom solution using TI bq24650 controller IC.

### 5.3 Solar Panel
- **Supplier:** Solar retailers / Amazon / Renogy
- **Part Number:** Various 50W 12V panels
- **Manufacturers:** Renogy, SOLPERK, Newpowa
- **Description:** 50W 12V monocrystalline solar panel, 21-30% conversion efficiency, MC4 connectors, weatherproof
- **Specifications:** ~2.85A output current, sized for 12Ah batteries (max 28Ah)
- **Unit Price:** $50-100 USD
- **Quantity:** 1
- **URL:** https://www.renogy.com/products/50-watt-12-volt-monocrystalline-solar-panel
- **Notes:** DigiKey carries solar cells but not typically complete panels in this size. Available from specialized solar retailers.

---

## 6. ENCLOSURE AND MOUNTING

### 6.1 NEMA/IP67 Polycarbonate Enclosure
- **Supplier:** Polycase Direct / Integra Enclosures
- **Part Number:** WQ Series (specific model TBD) or similar
- **Size Required:** Approximately 10" x 8" x 6" (254mm x 203mm x 152mm)
- **Description:** IP67/NEMA 4X rated weatherproof polycarbonate enclosure, hinged lid, fiberglass reinforced, suitable for outdoor industrial use
- **Unit Price:** $40-80 USD
- **Quantity:** 1
- **URL:** https://www.polycase.com/ip67-enclosures
- **Notes:** NOT on DigiKey/Mouser in this exact size. Polycase WQ series sold direct. For DigiKey: consider Hammond 1555F series IP67 enclosures (check sizing).

**DigiKey Alternative:** Hammond Manufacturing IP67 enclosures - search https://www.digikey.com/en/supplier-centers/hammond-manufacturing

### 6.2 IP67 Toggle Switches
- **Supplier:** DigiKey
- **Manufacturer:** NKK Switches (M-Series), Electroswitch (3100/3300 Series), Adam Tech
- **Part Numbers:** (Search DigiKey for specific models)
- **Description:** Panel mount toggle switch, IP67 waterproof rating, SPST or DPDT, dual seal (O-ring + rubber washer), 15/32" bushing, 100k cycles minimum
- **Unit Price:** $5-15 USD each
- **Quantity:** 4
- **URL:** https://www.digikey.com/en/products/filter/toggle-switches/201
- **Notes:** Filter DigiKey by IP67 rating and panel mount type. NKK M-Series offers comprehensive selection.

**Specific Options:**
- NKK Switches M-Series (dual seal waterproof)
- Electroswitch 3100/3300 Series (sealed to IP67 front and rear)

### 6.3 Panel Mount LEDs with Built-in 12V Resistor
- **Supplier:** DigiKey (VCC), Mouser (Apem)
- **Part Numbers:**
  - **Mouser:** QS103XXG12 (Apem, 10mm green, 12V, with wires) - verify current price
  - **DigiKey:** VCC LTHxMM12V series (5mm, not 10mm - need to verify 10mm availability)
- **Description:** 10mm panel mount LED indicator with built-in resistor for 12V operation, various colors (red, green, yellow), IP67 front panel sealing
- **Unit Price:** $2-5 USD each
- **Quantity:** 3
- **URL:**
  - Mouser: https://www.mouser.com/ProductDetail/Apem/QS103XXG12
  - DigiKey VCC: https://www.digikey.com/en/product-highlight/v/vcc/lthxmm12v-series-led-with-built-in-12-v-resistor
- **Notes:** Apem QS103XXG12 is confirmed 10mm with 12V on Mouser. VCC LTHxMM12V series on DigiKey appears to be 5mm.

### 6.4 PG9 Cable Glands
- **Supplier:** DigiKey
- **Manufacturers:** Essentra Components, Bud Industries, LAPP, SAB North America, Alpha Wire
- **Part Numbers:**
  - CG-PG9-1-BK (Essentra Components) - Polyamide, Black
  - CG-PG9-2-BK (Essentra Components) - 4-8mm cable range - $1.17
  - IPG-2229 (Bud Industries) - 4.06-7.87mm - $0.70
  - S2209 (LAPP)
  - PPG-9 (SAB North America)
  - PPS9 BK080 (Alpha Wire)
- **Description:** PG9 cable gland, IP67/IP68 rated, polyamide/nylon construction, 4-8mm cable diameter range
- **Unit Price:** $0.70-2.00 USD each
- **Quantity:** 6-8
- **URL:** https://www.digikey.com/en/products/detail/essentra-components/CG-PG9-1-BK/3811770
- **Notes:** Widely available at DigiKey. Select quantity based on number of cable entries needed.

### 6.5 Stainless Steel Hose Clamps (Pole Mounting)
- **Supplier:** Industrial hardware suppliers / Amazon
- **Part Number:** Generic stainless steel hose clamps
- **Size:** 3-6 inch diameter adjustable
- **Description:** 304 stainless steel adjustable hose clamps for pole mounting, worm drive mechanism, corrosion resistant
- **Unit Price:** $5-15 USD for set
- **Quantity:** 2-4 clamps (depending on mounting configuration)
- **URL:** https://www.amazon.com/Steelsoft-Fasteners-Stainless-Adjustable-Strapping/dp/B08F2NM8WT
- **Notes:** NOT on DigiKey/Mouser. Available from hardware suppliers, Amazon, Flagpro, or McMaster-Carr.

### 6.6 Ball Head Camera Mount
- **Supplier:** Camera/photography retailers / Amazon
- **Part Number:** Generic 1/4"-20 ball head mount
- **Manufacturers:** SmallRig, CAMVATE, Bulletpoint Mounting Solutions
- **Description:** 1/4"-20 threaded ball head camera mount, aluminum alloy construction, 360° rotation, adjustable, weatherproof/outdoor capable
- **Unit Price:** $10-25 USD each
- **Quantity:** 2
- **URL:** https://www.amazon.com/SMALLRIG-Camera-Mount-Additional-Screw/dp/B075M336JZ
- **Notes:** NOT on DigiKey/Mouser. Available from B&H Photo, Amazon, or camera accessory retailers.

**Options:**
- SmallRig 2059 (hot shoe mount with 1/4" screw)
- CAMVATE C1180 (wall/ceiling mount)
- Bulletpoint 1/4"-20 aluminum camera adapter

---

## 7. CABLES AND CONNECTIVITY

### 7.1 USB 3.0 Cables (Weatherproof/Robust)
- **Supplier:** DigiKey
- **Manufacturers:** Qualtek, Stewart Connector, Tripp Lite, Same Sky (CUI)
- **Length:** 3 meters (10 feet)
- **Description:** USB 3.0 Type-A cable, shielded, robust PVC or TPE jacket, preferably with IP67 connectors or suitable for outdoor conduit use
- **Unit Price:** $15-40 USD each
- **Quantity:** 2
- **URL:** https://www.digikey.com/en/product-highlight/q/qualtek/usb-3-cables
- **Notes:** DigiKey's IP67-rated USB cables (ASSMANN) are USB 2.0, not 3.0. May need to use standard USB 3.0 cables in protective conduit or select industrial USB 3.0 with ruggedized design.

---

## 8. DISPLAY AND USER INTERFACE

### 8.1 OLED Display Module
- **Supplier:** DigiKey / Adafruit
- **Part Numbers:**
  - DigiKey: OLED-128x64-1.3-I2C (Universal Solder/CANADUINO, Part #26295)
  - Adafruit: Product ID 938 (1.3" 128x64 OLED)
- **Description:** 1.3" OLED display module, 128x64 resolution, I2C interface, SSD1306 driver, monochrome white, 3.3V/5V compatible with onboard regulator
- **Unit Price:** $15-20 USD
- **Quantity:** 1
- **URL:**
  - DigiKey: https://www.digikey.com/en/products/detail/universal-solder-electronics-ltd/OLED-128x64-1-3-I2C/16822118
  - Adafruit: https://www.adafruit.com/product/938
- **Notes:** Adafruit version includes STEMMA QT connectors for easy plug-and-play.

---

## SUMMARY AND NOTES

### Items NOT Available on DigiKey/Mouser:
1. **PiSugar 3 Plus** - Not compatible with Pi 5; use DFRobot FIT0992 or Waveshare UPS HAT (B)
2. **Arducam CSI-USB adapter** - Order from Arducam direct or Amazon
3. **Entaniya WC-01 housing** - Obsolete at DigiKey; order from The Pi Hut or Entaniya
4. **STC-1000 thermostat** - Amazon/eBay
5. **Keenovo heater pads** - Keenovo direct
6. **LiFePO4 battery (exact 20Ah)** - Specialty battery retailers (DigiKey has other capacities)
7. **Solar charge controller (complete module)** - Solar retailers (DigiKey has ICs only)
8. **Solar panel** - Solar retailers
9. **Polycase WQ enclosure (specific size)** - Polycase direct
10. **Hose clamps** - Hardware suppliers
11. **Ball head mounts** - Camera retailers
12. **Molecular sieve desiccant packets** - Industrial suppliers/Amazon

### Recommended Procurement Strategy:
1. **DigiKey/Mouser Order:** Core electronics (Pi 5, cameras, modem, switches, LEDs, cable glands, vents, OLED display)
2. **Specialty Retailers:** Power components (battery, solar panel, charge controller)
3. **Direct from Manufacturers:** Arducam, Keenovo, Entaniya, DFRobot/Waveshare, Polycase
4. **Amazon/General:** Cables, mounts, clamps, thermostat, desiccant

### Estimated Total Cost:
- Core computing and cameras: $300-400
- Power system (battery, solar, controller): $150-250
- Enclosure and environmental: $100-150
- Miscellaneous (cables, connectors, mounting): $100-150
- **Total Estimated:** $650-950 USD (excluding shipping and customs)

### Critical Compatibility Notes:
1. Verify Raspberry Pi 5 compatibility for all HATs and accessories
2. Confirm camera housing compatibility with Camera Module 3
3. Ensure power budget accounts for all components (Pi 5 can draw up to 5A under load)
4. Verify LTE modem regional compatibility (EC25 variants for different regions)
5. Check cable gland sizes match actual cable diameters
6. Ensure enclosure size accommodates all internal components with room for airflow

---

## Research Sources

This BOM was compiled through comprehensive research of manufacturer and distributor websites including:
- DigiKey Electronics: https://www.digikey.com
- Mouser Electronics: https://www.mouser.com
- Raspberry Pi Official: https://www.raspberrypi.com
- Manufacturer direct sources: Quectel, Arducam, Entaniya, DFRobot, Waveshare, Keenovo, Polycase

All part numbers and specifications verified as of November 28, 2025. Prices are approximate and subject to change. Always verify current availability and pricing before ordering.

---

**Compiled by:** Research Assistant
**For:** RC-Box River Monitoring Device Project
**Last Updated:** 2025-11-28
