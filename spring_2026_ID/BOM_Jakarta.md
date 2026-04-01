# Bill of Materials: Jakarta Site Deployment

## Site Profile
- **Location:** Jakarta, Indonesia (coastal/urban, hot climate)
- **Power:** AC utility (220V/50Hz) with battery backup (sourced locally)
- **Camera:** 1x PoE IP camera (ANNKE C1200)
- **Purpose:** New training/demo installation
- **Date:** March 9, 2026 (reconciled against jakarta_order.csv)
- **Status:** ORDER SUBMITTED - Reconciled against authoritative jakarta_order.csv
- **Authoritative Source:** `jakarta_order.csv` is the single source of truth for what has been ordered

---

## Key Design Changes (March 2026 Order)

These decisions were made during ordering and differ from earlier BOM versions:

| Change | Old | New | Rationale |
|--------|-----|-----|-----------|
| **Witty Pi 5 dropped** | $59.95 | $0 | Hessel's new OS image works with Pi 5 built-in RTC |
| **Victron BatteryProtect dropped** | $53.55 | $0 | LiTime BMS has built-in low-voltage cutoff |
| **USB-RS485 adapter dropped** | $21.95 | $0 | GPIO breakout handles rain gauge RS232 |
| **Surge protector swapped** | Phoenix Contact $78.15 | Heschen HS-40-N $20.51 | Cheaper, single-phase (correct for site) |
| **Distribution block swapped** | DigiKey Phoenix Contact $37 | Amazon generic $23.12 | Cheaper, same function |
| **Cat6 cable right-sized** | 300ft spool $79.99 | 2x 10ft cables $11.98 | Runs are short (1 camera) |
| **Camera heater dropped** | PTC 10W $29.98 | $0 | ANNKE C1200 is factory-sealed IP67 |
| **Mounting hardware deferred** | $120+ | $0 | TBD after site survey |
| **Bulkhead connectors added** | Cable glands only | Ethernet + DC bulkheads $73.75 | Cleaner, more maintainable |
| **Fans added** | None | 40 CFM 2-pack $15.99 | Internal air circulation |
| **Neoprene isolation added** | EPDM sheet $10 | Neoprene $21.99 | Better for galvanic isolation |

---

## Ordered Items

### DigiKey

| Item | Description | Part# | Qty | Unit Price | Extended | Link |
|------|-------------|-------|-----|------------|----------|------|
| PWR-001 | Mean Well SDR-120-12 DIN Rail PSU (120W 12V 10A 88-264VAC) | SDR-120-12 | 1 | $59.84 | $59.84 | [DigiKey](https://www.digikey.com/en/products/detail/mean-well-usa-inc/SDR-120-12/7706555) |
| HUM-002 | Amphenol LTW M12 Protective Vent (IP68) | VENT-PS1YBK-N8001 | 2 | $9.95 | $19.90 | [DigiKey](https://www.digikey.com/en/products/detail/amphenol-ltw/VENT-PS1YBK-N8001/7898285) |

**DigiKey Subtotal: $79.74**

---

### Amazon

| Item | Description | Qty | Unit Price | Extended | Link | Notes |
|------|-------------|-----|------------|----------|------|-------|
| **POWER** | | | | | | |
| PWR-005 | Heschen HS-40-N 2P Surge Protector (40kA 275V) | 1 | $20.51 | $20.51 | [Amazon](https://www.amazon.com/Heschen-Protective-HS-40N-2P-Low-Voltage/dp/B0CZ3J8TGW) | 220V single phase |
| PWR-009 | Power Distribution Block (12-pos DIN rail) | 2 | $11.56 | $23.12 | [Amazon](https://www.amazon.com/Position-Distribution-Module-Interface-Breakout/dp/B07J53DFNM) | For both sites |
| BUCK-5V | Mean Well DDR-60G-5 DC-DC Converter (5V 10.8A 9-36V in) | 1 | $25.20 | $25.20 | [Amazon](https://www.amazon.com/MEAN-WELL-DDR-60G-5-Converter-5V10-8A/dp/B07B64RCTR) | 12V bus → 5V for Pi |
| RELAY-POE | Electronics-Salon DIN Rail 4-SPDT 10A Relay Module 5V | 1 | $32.00 | $32.00 | [Amazon](https://www.amazon.com/Electronics-Salon-Mount-Interface-Module-Version/dp/B00M1MW5BW) | Switches 12V to PoE switch |
| **COMPUTE** | | | | | | |
| CPU-001 | Raspberry Pi 5 8GB RAM | 1 | $109.00 | $109.00 | [Amazon](https://www.amazon.com/Raspberry-Pi-8GB-SC1112-Quad-core/dp/B0CK2FCG1K) | |
| CPU-003B | GPIO Breakout Board (Geekworm G469) | 1 | $9.90 | $9.90 | [Amazon](https://www.amazon.com/Geekworm-G469-Terminal-Breakout-Raspberry/dp/B0DMNJ17PD) | Replaces Pi-EzConnect |
| CPU-004 | SanDisk 256GB USB Flash Drive | 1 | $30.99 | $30.99 | [Amazon](https://www.amazon.com/SanDisk-256GB-Ultra-Flash-Drive/dp/B0BY2TT9TD) | |
| CPU-007 | Quectel EG25-G LTE Mini PCIe Module | 1 | $75.00 | $75.00 | [Amazon](https://www.amazon.com/Generic-Quectel-EG25-G-Cellular-M2M-optimized/dp/B0CVQ2YLQQ) | |
| CPU-008 | Mini PCIe to USB Adapter (EXVIST) | 1 | $24.99 | $24.99 | [Amazon](https://www.amazon.com/EXVIST-Industrial-Adapter-Compatible-Connection/dp/B08GFM9536) | |
| CPU-009 | Proxicast ANT-122-S02 MIMO LTE Puck Antenna (IP67) | 1 | $64.95 | $64.95 | [Amazon](https://www.amazon.com/Proxicast-Profile-Omni-Directional-Screw-Mount-Antenna/dp/B07DDC9WV5) | |
| CPU-006 | MicroSD Card 64G x2 Pack (SanDisk) | 1 | $26.92 | $26.92 | [Amazon](https://www.amazon.com/SanDisk-128GB-MicroSDXC-Ultra-Memory/dp/B07XDCZ9J3) | |
| CPU-011 | Raspberry Pi 5 Active Cooler | 1 | $9.90 | $9.90 | [Amazon](https://www.amazon.com/Raspberry-Pi5-Temperature-Controlled-Aluminium-Dissipation/dp/B0CW164TCW) | |
| CPU-012 | Raspberry Pi 5 RTC Battery (ML-2020 JST-SH) | 2 | $5.00 | $10.00 | [Amazon](https://www.amazon.com/s?k=raspberry+pi+5+RTC+battery) | 1 Jakarta + 1 Sukabumi |
| **CAMERA** | | | | | | |
| CAM-001 | ANNKE C1200 PoE IP Camera (12MP 2-pack) | 1 | $85.00 | $85.00 | [Amazon](https://www.amazon.com/ANNKE-Outdoor-Security-Surveillance-Detection/dp/B0CMTHVCV8) | 1 camera used, 1 spare from 2-pack |
| CAM-003 | LINOVISION Industrial 12V PoE Switch (Gigabit) | 1 | $85.99 | $85.99 | [Amazon](https://www.amazon.com/LINOVISION-Industrial-Gigabit-DC12V-48V-IEEE802-3af/dp/B09HGWLZSD) | |
| CAM-004 | Outdoor Cat6 Shielded Cable UV-resistant (10ft) | 2 | $5.99 | $11.98 | [Amazon](https://www.amazon.com/Abireiv-Resistant-Waterproof-Buried-able-Compatible/dp/B09M6GXPBM) | 1 internal patch + 1 external to camera |
| **ENCLOSURE** | | | | | | |
| ENC-001 | VEVOR NEMA 4x Box (16"x12"x8") | 1 | $75.21 | $75.21 | [Amazon](https://www.amazon.com/dp/B0924DJGJ9?th=1) | Matches Sukabumi box |
| CLIP-RPI | DIN Rail Clip for Raspberry Pi | 1 | $18.99 | $18.99 | [Amazon](https://www.amazon.com/Mount-Bracket-Raspberry-Arduino-BeagleBone/dp/B08HRZVFCX) | |
| **BULKHEAD CONNECTORS** | | | | | | |
| ETH-BULKHEAD | CNLINKO Weatherproof Ethernet Bulkhead (IP67) | 1 | $17.88 | $17.88 | [Amazon](https://www.amazon.com/CNLINKO-Industrial-Connector-Receptacles-Waterproof/dp/B079BWPJNG) | Panel mount RJ45 for camera |
| DC-BULKHEAD | Uonecn SP13 DC Power Bulkheads (5-pack IP68) | 1 | $37.99 | $37.99 | [Amazon](https://www.amazon.com/Uonecn-Waterproof-Connectors-Connector-Circular/dp/B07HQ1K4LJ) | 13A 2-pin for 12V power |
| **HUMIDITY & THERMAL** | | | | | | |
| COAT-SIL | MG 422C Silicone Conformal Coating | 1 | $18.89 | $18.89 | [Amazon](https://www.amazon.com/MG-Chemicals-422C-Conformal-Coating/dp/B0B1N2XPH5) | Correct product for >95% RH |
| HUM-HEATER | PTC Heater 15W for Enclosure | 1 | $10.99 | $10.99 | [Amazon](https://www.amazon.com/Insulated-Temperature-Thermostatic-1-37x0-8inches-PTCYIDU/dp/B0BNZV3BLK) | Humidity management |
| HUM-TEMP-PROBES | DS18B20 Waterproof Temperature Probes | 1 | $9.99 | $9.99 | [Amazon](https://www.amazon.com/Temperature-Waterproof-Stainless-Compatible-Raspberry/dp/B0FH4WRN6H) | Dew point + heater control |
| FAN-01 | 40 CFM Fans (2-pack) | 1 | $15.99 | $15.99 | [Amazon](https://www.amazon.com/GDSTIME-Bearings-Brushless-Computer-Cooling/dp/B081N7BT4H?th=1) | Internal air circulation |
| **MOUNTING** | | | | | | |
| VIB-01 | Neoprene Rubber for Galvanic Isolation | 1 | $21.99 | $21.99 | [Amazon](https://www.amazon.com/Neoprene-Adhesive-Gaskets-Warehouse-Flooring/dp/B09T9F9GJB) | Between dissimilar metals |
| **CONSUMABLES** | | | | | | |
| CONS-006 | Isopropyl Alcohol 99% (16oz) | 1 | $8.99 | $8.99 | [Amazon](https://www.amazon.com/s?k=isopropyl+alcohol+99) | Cleaning |

**Amazon Subtotal: $882.36**

---

### Adafruit

| Item | Description | Part# | Qty | Unit Price | Extended | Link |
|------|-------------|-------|-----|------------|----------|------|
| HUM-SENSOR | SHT40 Temp/Humidity Sensor (I2C STEMMA QT) | 4885 | 2 | $5.99 | $11.98 | [Adafruit](https://www.adafruit.com/product/4885) |
| HUM-SENSOR-CABLE | JST to bare wire connector | 4209 | 4 | $0.95 | $3.80 | [Adafruit](https://www.adafruit.com/product/4209) |

**Adafruit Subtotal: $15.78**

---

### Hydreon

| Item | Description | Part# | Qty | Unit Price | Extended | Link |
|------|-------------|-------|-----|------------|----------|------|
| RAIN-001 | Hydreon RG-15 Optical Rain Gauge | RG-15 | 1 | $99.00 | $99.00 | [Hydreon](https://store.hydreon.com/RG-15.html) |

**Hydreon Subtotal: $99.00**

---

## Items Covered by Other Means

These are NOT in the Jakarta order because they're already available:

### From Sukabumi Order (covers both sites)
| Item | Description |
|------|-------------|
| CPU-003 | Stacking Headers (Geekworm) |
| CLIP-TERM | DIN Rail Terminal Block Kit |
| DIN-PCB | Molence C45 PCB DIN Rail Clip-Pairs |
| DIN-CLIP | CNQLIS Aluminum DIN Rail Mounting Clips |
| LED-WS2812B | WS2812B NeoPixel addressable RGB LED |
| BTN-MAINT | IP67 Momentary Pushbutton 16mm Stainless |
| PWR-12V | 12V Power Couplers - Screw Terminal |
| DI-GREASE | Dielectric Grease |
| CONS-002 | Silicone Sealant (RTV) |
| CONS-003 | UV-Resistant Zip Ties |

### Already Have
| Item | Description | Source |
|------|-------------|--------|
| ENC-003 | PG9 Cable Glands | Leftover from shuttle build |
| PWR-010 | 35mm DIN Rail with End Stops | Already have enough for both boxes |

### Shop Supplies (will purchase separately as needed)
PWR-006 (fuse holders), PWR-007/008 (fuses), ENC-004 (cable glands), ENC-008 (hardware kit), HUM-006 (kapton tape), USB-C-PWR, USB-A-SHORT, CONS-001 (heat shrink)

---

## Items Dropped (Not Needed)

| Item | Description | Reason |
|------|-------------|--------|
| CPU-002 | Witty Pi 5 HAT+ ($59.95) | Hessel's new OS image works with Pi 5 built-in RTC |
| PWR-004 | Victron BatteryProtect ($53.55) | LiTime BMS has built-in low-voltage cutoff |
| UI-005 | USB to RS485/232 Adapter ($21.95) | GPIO breakout handles rain gauge RS232 |
| HUM-003 | PTC Heater 10W for Camera ($29.98) | ANNKE C1200 is factory-sealed IP67; external heater can't reach lens |
| CAM-005 | IP68 RJ45 Waterproof Coupler ($12.99) | Replaced by ETH-BULKHEAD connectors |

---

## Items On Hold

| Item | Description | Reason |
|------|-------------|--------|
| CAM-006 | Hikvision DS-1275ZJ Vertical Mounting Plates | HOLD until we know how we're mounting |
| BRACKET-WALL | Heavy-duty SS L-brackets | Mounting TBD after site survey |
| ANCHOR-CON | Stainless concrete wedge anchors | Mounting TBD after site survey |
| BAND-SS | Stainless Steel Banding with Buckles | Mounting TBD after site survey |

---

## Local Sourcing (Indonesia)

| Item | Description | Est. Cost (IDR) | Est. Cost (USD) | Source | Notes |
|------|-------------|-----------------|-----------------|--------|-------|
| GND-001 | Copper Grounding Rod (1.5m x 16mm) | 200,000 | $13 | Glodok / ACE Hardware | |
| GND-002 | Grounding Cable (6 AWG copper 10m) | 150,000 | $10 | Electrical supply | Green/yellow insulation |
| GND-003 | Grounding Lugs & Connectors Kit | 50,000 | $3 | Electrical supply | Compression-type |
| GND-004 | Ground Rod Clamp (bronze) | 40,000 | $3 | Electrical supply | |
| ENC-010 | Mounting Pole (4m galvanized steel 50mm) | 500,000 | $32 | Toko bangunan / ACE | Heavy - don't ship |
| ENC-011 | Pole Base Flange + Concrete Anchors | 200,000 | $13 | Toko bangunan | |
| ENC-012 | U-Bolts for Pole Mounting (M8 x 150mm SS) | 100,000 | $6 | Toko bangunan | |
| RAIN-002 | Pole Mount Arm for Rain Gauge | 150,000 | $10 | Fabricate locally | |
| PWR-002 | 12V LiFePO4 Battery + Charger | TBD | TBD | Tokopedia / Shopee | Need charger matching battery chemistry |
| BATT-BOX | Weatherproof Battery Box | ~500,000 | ~$30 | ACE / Tokopedia | Size to fit battery + charger |
| MISC | Concrete mix, wire nuts, cable ties | 100,000 | $6 | Any hardware store | |

**Local Sourcing Subtotal: ~$126+ USD** (battery price TBD)

---

## Cost Summary

| Category | Subtotal | Notes |
|----------|----------|-------|
| DigiKey | $79.74 | PSU, vents |
| Amazon | $882.36 | Compute, camera, power, enclosure, bulkhead, fans, consumables |
| Adafruit | $15.78 | SHT40 sensors + cables |
| Hydreon | $99.00 | Rain gauge |
| **Ordered Total** | **$1,076.88** | All shipped items |
| Local Sourcing (Jakarta) | ~$126+ | Grounding, pole, misc (battery TBD) |
| **Project Total** | **~$1,203+** | Excluding battery system |

**NOTE:** jakarta_order.csv shows a total of $1,863.19 but that formula is stale — it does not reflect items zeroed out during ordering. The actual ordered total from line items is $1,076.88 (updated for 1-camera configuration).

**Budget comparison:** Jakarta $1,077 (shipped) + Sukabumi $948 (actual) = ~$2,025 shipped. Well within $3,000 target even with local sourcing and battery.

---

## Component Compatibility

- **Pi 5 + GPIO Breakout (G469):** Direct stack, no Witty Pi in between
- **Pi 5 built-in RTC:** Hessel's OS image handles scheduling (replaces Witty Pi 5)
- **ANNKE C1200 + LINOVISION 12V PoE Switch:** 802.3af/at compatible
- **Mean Well SDR-120-12:** 88-264VAC input (Indonesia 220V OK)
- **DDR-60G-5:** 9-36V input, covers battery voltage range
- **Quectel EG25-G:** Indonesian LTE bands B1/B3/B5/B8/B40
- **MG 422C:** Silicone conformal coat rated for >95% RH
- **SP13 DC bulkheads:** 13A/250V — adequate for 12V 8A bus
- **CNLINKO RJ45 bulkhead:** IP67 panel mount, PoE compatible (1 needed for 1 camera)

---

## Revision History

| Date | Version | Changes |
|------|---------|---------|
| 2026-03-26 | 5.1 | Reduced from 2 cameras to 1. Cat6 cables 4→2, CNLINKO bulkheads 2→1. Updated subtotals. |
| 2026-03-09 | 5.0 | Reconciled against authoritative jakarta_order.csv. Dropped Witty Pi 5 (Pi 5 RTC), Victron BatteryProtect (BMS cutoff), USB-RS485 (GPIO handles it), camera heater (sealed camera). Swapped Phoenix Contact SPD → Heschen HS-40-N, Phoenix PTFIX → Amazon generic. Right-sized Cat6 cable. Added fans, neoprene isolation, ethernet + DC bulkhead connectors. Deferred mounting hardware. Corrected conformal coat to MG 422C. Updated all prices to actual order prices. |
| 2026-03-06 | 4.0 | Split enclosure approach: electronics in VEVOR 16x12x8" (matched Sukabumi), battery + charger moved to external box sourced locally. |
| 2026-02-24 | 3.0 | Reconciled with Sukabumi actuals: matched shared components, reduced to 4 suppliers. |
| 2026-01-09 | 2.0 | Verified BOM with actual product links, consolidated suppliers. |
| 2026-01-09 | 1.0 | Initial BOM creation. |

---

**Document prepared:** January 9, 2026 | **Last updated:** March 26, 2026
**Version:** 5.1 (Updated for 1-camera configuration)
**Authoritative source:** `jakarta_order.csv`
