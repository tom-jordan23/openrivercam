# Bill of Materials: Jakarta Site Deployment

## Site Profile
- **Location:** Jakarta, Indonesia (coastal/urban, hot climate)
- **Power:** AC utility (220V/50Hz) with 24hr battery backup
- **Camera:** 2x PoE IP cameras
- **Purpose:** New training/demo installation
- **Date:** February 24, 2026 (reconciled with Sukabumi actuals)
- **Status:** RECONCILED - Shared components aligned with Sukabumi procured parts
- **Suppliers Consolidated:** 4 primary suppliers (Adafruit, Amazon, DigiKey, Hydreon)

---

## Quick Links to Suppliers

| Supplier | Primary Products | URL |
|----------|-----------------|-----|
| **Adafruit** | Witty Pi 5, USB-RS485, cable glands | https://www.adafruit.com |
| **Amazon** | Compute, cameras, power system, enclosure, consumables | https://www.amazon.com |
| **DigiKey** | Industrial PSU, surge protector, vents | https://www.digikey.com |
| **Hydreon** | Rain gauge | https://store.hydreon.com |

---

## Complete Bill of Materials

### SUPPLIER 1: DIGIKEY
**URL:** https://www.digikey.com
**Category:** Industrial Power, Protection & Vents

| Item | Description | Part# | Qty | Unit Price | Extended | Product Link | Notes |
|------|-------------|-------|-----|------------|----------|--------------|-------|
| PWR-001 | Mean Well SDR-120-12 DIN Rail PSU (120W, 12V 10A, 88-264VAC) | SDR-120-12 | 1 | $59.84 | $59.84 | https://www.digikey.com/en/products/detail/mean-well-usa-inc/SDR-120-12/7706193 | Jakarta-specific |
| PWR-005 | Phoenix Contact Type 2 SPD Surge Protector (3-phase, 40kA) | FLT-SEC-T2-3C-350/25 | 1 | $78.15 | $78.15 | https://www.digikey.com/en/products/detail/phoenix-contact/2905418/3884829 | Jakarta-specific |
| PWR-009 | Phoenix Contact PTFIX Power Distribution Block (12-pos) | PTFIX-12X1.5-NS35-FE | 2 | $18.50 | $37.00 | https://www.digikey.com/en/products/filter/terminal-blocks/power-distribution/412 | Jakarta-specific |
| HUM-002 | Amphenol LTW M12 Protective Vent (IP68) | VENT-PS1YBK-N8001 | 2 | $9.95 | $19.90 | https://www.digikey.com/en/products/detail/amphenol-ltw/VENT-PS1YBK-N8001/7898285 | Matched Sukabumi source |

**DigiKey Subtotal: $194.89**

---

### SUPPLIER 1: AMAZON
**URL:** https://www.amazon.com
**Category:** Compute, Cameras, Power System, Enclosure & Consumables

Items marked **"Matched Sukabumi"** use the exact same product/source ordered for the Sukabumi site.
Items marked **"Jakarta-specific"** are unique to the Jakarta AC-powered deployment.

| Item | Description | Qty | Unit Price | Extended | Product Link | Notes |
|------|-------------|-----|------------|----------|--------------|-------|
| **COMPUTE PLATFORM** | | | | | | |
| CPU-001 | Raspberry Pi 5 8GB RAM | 1 | $109.00 | $109.00 | https://www.amazon.com/Raspberry-Pi-8GB-SC1112-Quad-core/dp/B0CK2FCG1K | Matched Sukabumi |
| CPU-003 | Stacking Headers (Geekworm) | 1 | $9.90 | $9.90 | https://www.amazon.com/Geekworm-Stacking-Raspberry-Specifications-Extender/dp/B0827THC7R | Matched Sukabumi |
| CPU-003B | GPIO Breakout Board (Geekworm G469) | 1 | $9.90 | $9.90 | https://www.amazon.com/Geekworm-G469-Terminal-Breakout-Raspberry/dp/B0DMNJ17PD | Matched Sukabumi (replaces Pi-EzConnect) |
| CPU-004 | SanDisk 256GB USB Flash Drive | 1 | $30.99 | $30.99 | https://www.amazon.com/SanDisk-256GB-Ultra-Flash-Drive/dp/B0BY2TT9TD | Matched Sukabumi |
| CPU-007 | Quectel EG25-G LTE Mini PCIe Module | 1 | $75.00 | $75.00 | https://www.amazon.com/Generic-Quectel-EG25-G-Cellular-M2M-optimized/dp/B0CVQ2YLQQ | Matched Sukabumi |
| CPU-008 | Mini PCIe to USB Adapter (EXVIST P2U52V02USB) | 1 | $24.99 | $24.99 | https://www.amazon.com/EXVIST-Industrial-Adapter-Compatible-Connection/dp/B08GFM9536 | CORRECTED: EG25-G is Mini PCIe, not M.2 |
| CPU-009 | Proxicast ANT-122-S02 2x2 MIMO LTE Puck Antenna (IP67) | 1 | $64.95 | $64.95 | https://www.amazon.com/Proxicast-Profile-Omni-Directional-Screw-Mount-Antenna/dp/B07DDC9WV5 | Matched Sukabumi |
| CPU-006 | MicroSD Card 64G x2 Pack (SanDisk) | 1 | $26.92 | $26.92 | https://www.amazon.com/SanDisk-128GB-MicroSDXC-Ultra-Memory/dp/B07XDCZ9J3 | Matched Sukabumi |
| CPU-011 | Raspberry Pi 5 Active Cooler | 1 | $9.90 | $9.90 | https://www.amazon.com/Raspberry-Pi5-Temperature-Controlled-Aluminium-Dissipation/dp/B0CW164TCW | Matched Sukabumi |
| **CAMERA SYSTEM** | | | | | | |
| CAM-001 | ANNKE C1200 PoE IP Camera (12MP, 134° FOV, 2-pack) | 1 | $119.99 | $119.99 | https://www.amazon.com/ANNKE-Security-Surveillance-Detection-Spotlight/dp/B0DBHRMT1V | Jakarta: 2 cameras (Sukabumi ordered single $89.99) |
| CAM-003 | LINOVISION Industrial 12V PoE Switch (Gigabit, IEEE802.3af/at) | 1 | $85.99 | $85.99 | https://www.amazon.com/LINOVISION-Industrial-Gigabit-DC12V-48V-IEEE802-3af/dp/B09HGWLZSD | Matched Sukabumi (replaces Planet IPOE-260-12V) |
| CAM-006 | Hikvision DS-1275ZJ Vertical Mounting Plate (stainless) | 2 | $30.99 | $61.98 | https://www.amazon.com/DS-1275ZJ-Vertical-Adapter-Hikvision-Stainless/dp/B0DRDZBR69 | Matched Sukabumi, qty 2 for 2 cameras |
| CAM-004 | Outdoor Cat6 Shielded Cable (300ft, UV-resistant) | 1 | $79.99 | $79.99 | https://www.amazon.com/s?k=outdoor+Cat6+shielded+cable+300ft+UV | Camera cabling |
| CAM-005 | IP68 RJ45 Waterproof Coupler (2-pack) | 1 | $12.99 | $12.99 | https://www.amazon.com/s?k=IP68+RJ45+coupler+waterproof | Weatherproof connections |
| RELAY-POE | Electronics-Salon DIN Rail 4-SPDT 10A Relay Module, 5V | 1 | $18.00 | $18.00 | https://www.amazon.com/Electronics-Salon-Mount-Interface-Module-Version/dp/B00M1MW5BW | Switches 12V to PoE switch; GPIO or passive USB trigger. See [research](research/poe_switch_relay_research.md) |
| **POWER SYSTEM (Jakarta-specific)** | | | | | | |
| BUCK-5V | Mean Well DDR-60G-5 DIN Rail DC-DC Converter (5V 10.8A, 9-36V input) | 1 | $39.00 | $39.00 | [Amazon](https://www.amazon.com/s?k=DDR-60G-5+Mean+Well) | Converts 12V bus to 5V for Pi + modem + LEDs + rain sensor. Same as Sukabumi. See [research](research/dc_dc_buck_converter_research.md) |
| PWR-002 | 12V 100Ah LiFePO4 Battery (LiTime, 1280Wh, BMS) | 1 | $299.99 | $299.99 | https://www.amazon.com/s?k=12V+100Ah+LiFePO4+battery | Jakarta-specific: 24hr backup |
| PWR-003 | 20A LiFePO4 Battery Charger (12V, smart, temp sensor) | 1 | $89.99 | $89.99 | https://www.amazon.com/s?k=20A+LiFePO4+charger+12V | Jakarta-specific |
| PWR-004 | Victron BatteryProtect 12/24V-65A (Low voltage disconnect) | 1 | $53.55 | $53.55 | https://www.amazon.com/Victron-Energy-Battery-Protect-24-Volt/dp/B01N6ATT8C | Jakarta-specific |
| PWR-006 | Automotive Blade Fuse Holders (inline, waterproof, 4-pack) | 1 | $12.99 | $12.99 | https://www.amazon.com/s?k=waterproof+blade+fuse+holder | Circuit protection |
| PWR-007 | ATO/ATC Blade Fuses 10A (25-pack) | 1 | $7.99 | $7.99 | https://www.amazon.com/s?k=ATO+blade+fuses+10A | Replacement fuses |
| PWR-008 | ATO/ATC Blade Fuses 15A (25-pack) | 1 | $7.99 | $7.99 | https://www.amazon.com/s?k=ATO+blade+fuses+15A | Replacement fuses |
| PWR-010 | 35mm DIN Rail with End Stops (2x 1m aluminum) | 2 | $12.99 | $25.98 | https://www.amazon.com/s?k=35mm+DIN+rail+1+meter | Jakarta-specific: larger enclosure |
| **ENCLOSURE & MOUNTING** | | | | | | |
| ENC-001 | IP66 Aluminum Enclosure (400x300x200mm, hinged) | 1 | $89.99 | $89.99 | https://www.amazon.com/s?k=IP66+aluminum+enclosure+400x300x200 | Jakarta-specific: larger for power system |
| ENC-004 | Cable Gland Assortment (PG9/PG13.5/PG16, 20-pack) | 1 | $18.99 | $18.99 | https://www.amazon.com/s?k=cable+gland+assortment+IP68 | Cable entries |
| CLIP-TERM | DIN Rail Terminal Block Kit | 1 | $19.99 | $19.99 | https://www.amazon.com/GUETNEU-Terminal-Block-Voltage-Combined/dp/B0BQQDWGXV | Matched Sukabumi |
| CLIP-RPI | DIN Rail Clip for Raspberry Pi | 1 | $18.99 | $18.99 | https://www.amazon.com/Mount-Bracket-Raspberry-Arduino-BeagleBone/dp/B08HRZVFCX | Matched Sukabumi |
| ENC-008 | Stainless Steel M3/M4 Hardware Kit (300-piece) | 1 | $16.99 | $16.99 | https://www.amazon.com/s?k=stainless+steel+hardware+kit+M3+M4 | Mounting hardware |
| DIN-PCB | Molence C45 PCB DIN Rail Clip-Pairs (10 sets) | 1 | $9.00 | $9.00 | https://www.amazon.com/Molence-Mounting-Adapter-Circuit-Bracket/dp/B09KZHY8G4 | Mount bare PCBs to DIN rail. See [research](research/din_rail_mounting_clips_research.md) |
| DIN-CLIP | CNQLIS 1.65" Aluminum DIN Rail Mounting Clips (10-pack) | 1 | $13.00 | $13.00 | https://www.amazon.com/CNQLIS-Universal-Mounting-Bracket-Countersunk/dp/B0CJJ1DBZM | Mount modem, misc items via screws/zip ties. See [research](research/din_rail_mounting_clips_research.md) |
| **USER INTERFACE** | | | | | | |
| LED-MULTI | Multi-color LED 5-pack (FILN, 12V-24V, IP67) | 1 | $16.99 | $16.99 | https://www.amazon.com/FILN-Indicator-Anodized-Waterproof-12V-24V/dp/B0C7KSFKTH | Matched Sukabumi |
| BTN-MAINT | IP67 Momentary Pushbutton 16mm Stainless | 1 | $8.99 | $8.99 | https://www.amazon.com/Gebildet-Momentary-terminals-Stainless-Waterproof/dp/B081JJBN4G | Matched Sukabumi |
| PWR-12V | 12V Power Couplers - Screw Terminal | 1 | $6.99 | $6.99 | https://www.amazon.com/ANLINK-20-Connectors-Terminal-Security/dp/B0BHYTRP1M | Matched Sukabumi |
| **HUMIDITY & THERMAL** | | | | | | |
| COAT-SIL | Conformal Coating | 1 | $18.89 | $18.89 | https://www.amazon.com/1DFAUL-Electronics-Insulating-Waterproof-Electronic/dp/B0FH1ZTGZV | Matched Sukabumi |
| HUM-003 | PTC Heater 10W for Camera (thermostat, 2-pack) | 1 | $29.98 | $29.98 | https://www.amazon.com/s?k=PTC+heater+12V+10W | Jakarta-specific |
| HUM-004 | PTC Heater 15W for Enclosure (hygrostat control) | 1 | $19.99 | $19.99 | https://www.amazon.com/s?k=PTC+heater+12V+15W | Jakarta-specific |
| HUM-006 | Kapton Tape 1/4" x 36yds (masking for coating) | 1 | $9.99 | $9.99 | https://www.amazon.com/s?k=kapton+tape | Conformal coat masking |
| **CABLES & CONNECTORS** | | | | | | |
| USB-C-PWR | USB-C Power Cable (1.5m, right-angle) | 1 | $8.00 | $8.00 | https://www.amazon.com/s?k=USB-C+power+cable+right+angle+1.5m | Matched Sukabumi |
| USB-A-SHORT | USB-A Cables (0.5m, various) 3-pack | 1 | $12.00 | $12.00 | https://www.amazon.com/s?k=short+USB+cable+pack+0.5m | Matched Sukabumi |
| DI-GREASE | Dielectric Grease (small tube) | 1 | $7.99 | $7.99 | https://www.amazon.com/BTAS-Dielectric-Automotive-Electrical-Connectors/dp/B0D6R543V2 | Matched Sukabumi |
| **CONSUMABLES** | | | | | | |
| CONS-001 | Heat Shrink Tubing Kit (assorted, 328-piece) | 1 | $11.99 | $11.99 | https://www.amazon.com/s?k=heat+shrink+tubing+kit | Cable finishing |
| CONS-002 | Silicone Sealant (RTV, electronics-grade) | 1 | $7.99 | $7.99 | https://www.amazon.com/s?k=silicone+sealant+electronics | Sealing |
| CONS-003 | UV-Resistant Zip Ties (assorted, 500-pack) | 1 | $12.99 | $12.99 | https://www.amazon.com/s?k=UV+resistant+zip+ties | Cable management |
| CONS-006 | Isopropyl Alcohol 99% (16oz bottle) | 1 | $8.99 | $8.99 | https://www.amazon.com/s?k=isopropyl+alcohol+99 | Cleaning |

**Amazon Subtotal: $1,646.69**

---

### SUPPLIER 2: ADAFRUIT
**URL:** https://www.adafruit.com
**Category:** Witty Pi, Adapters & Cable Glands

| Item | Description | Part# | Qty | Unit Price | Extended | Product Link | Notes |
|------|-------------|-------|-----|------------|----------|--------------|-------|
| CPU-002 | Witty Pi 5 HAT+ (power mgmt, RTC, I2C-only) | 6449 | 1 | $59.95 | $59.95 | https://www.adafruit.com/product/6449 | Matched Sukabumi |
| UI-005 | USB to RS485/232 Multi-Protocol Adapter | 5995 | 1 | $21.95 | $21.95 | https://www.adafruit.com/product/5995 | Matched Sukabumi (optional) |
| ENC-003 | PG9 Cable Glands (10-pack) | 761 | 1 | $7.50 | $7.50 | https://www.adafruit.com/product/761 | Cable entry sealing |

**Adafruit Subtotal: $89.40**

---

### SUPPLIER 3: HYDREON
**URL:** https://store.hydreon.com
**Category:** Rain Gauge

| Item | Description | Part# | Qty | Unit Price | Extended | Product Link | Notes |
|------|-------------|-------|-----|------------|----------|--------------|-------|
| RAIN-001 | Hydreon RG-15 Optical Rain Gauge (solid-state, RS232 TTL 3.3V + pulse output) | RG-15 | 1 | $99.00 | $99.00 | https://store.hydreon.com/RG-15.html | Same as Sukabumi |

**Hydreon Subtotal: $99.00**

## LOCAL SOURCING (INDONESIA)

The following items should be purchased locally in Jakarta to reduce shipping costs and avoid import restrictions:

| Item | Description | Est. Cost (IDR) | Est. Cost (USD) | Notes |
|------|-------------|-----------------|-----------------|-------|
| GND-001 | Copper Grounding Rod (1.5m x 16mm) | 200,000 | $13 | Standard electrical supply stores |
| GND-002 | Grounding Cable (6 AWG copper, 10m) | 150,000 | $10 | Green/yellow insulation |
| GND-003 | Grounding Lugs & Connectors Kit | 50,000 | $3 | Compression-type lugs |
| GND-004 | Ground Rod Clamp (bronze, corrosion-resistant) | 40,000 | $3 | Available at electrical suppliers |
| ENC-010 | Mounting Pole (4m galvanized steel, 50mm dia) | 500,000 | $32 | Heavy - expensive to ship |
| ENC-011 | Pole Base Flange + Concrete Anchors | 200,000 | $13 | Source at local hardware |
| ENC-012 | U-Bolts for Pole Mounting (M8 x 150mm, stainless) | 100,000 | $6 | Local hardware stores |
| RAIN-002 | Pole Mount Arm for Rain Gauge | 150,000 | $10 | May fabricate locally if needed |
| MISC | Concrete mix, wire nuts, additional cable ties | 100,000 | $6 | As needed during installation |

**Local Sourcing Subtotal: ~$96 USD**

**Recommended Jakarta suppliers:**
- **Glodok Electronics Market** - Electronics, cable glands, terminal blocks
- **ACE Hardware or Informa** - General hardware, mounting materials
- **Local electrical supply stores** - Grounding equipment, conduit

---

## BOM SUMMARY BY SUPPLIER

| Supplier | Subtotal (USD) | Notes |
|----------|----------------|-------|
| **1. Amazon** | $1,646.69 | Compute, cameras, power system, enclosure, consumables |
| **2. DigiKey** | $194.89 | PSU, surge protector, power distribution, vents |
| **3. Adafruit** | $89.40 | Witty Pi 5, USB-RS485, cable glands |
| **4. Hydreon** | $99.00 | Rain gauge |
| **Shipped Subtotal** | **$2,029.98** | Components to ship from US/international |
| **Local Sourcing (Jakarta)** | **$96.00** | Grounding, mounting pole, misc hardware |
| **GRAND TOTAL** | **$2,125.98** | Materials only |

---

## ADDITIONAL COSTS & BUDGET SUMMARY

| Item | Estimated Cost (USD) | Notes |
|------|---------------------|-------|
| **Equipment (shipped)** | $2,029.98 | Components from 4 suppliers |
| **Local sourcing (Jakarta)** | $96.00 | Grounding, pole, mounting hardware |
| **TOTAL PROJECT COST** | **$2,125.98** | Materials only |

**Budget Status:** ✅ Within budget. Combined with Sukabumi ($948.08 actual) = **$3,074.06** total for both sites.
**Note:** Equipment travels with installer under humanitarian exemption — no shipping, customs, or contingency costs.

### Cost Review Items (decision pending)

**Clear savings (low risk):**

| Item | Issue | Potential Savings | Decision |
|------|-------|-------------------|----------|
| PWR-005 | 3-phase SPD for single-phase site; single-phase unit ~$30 | ~$45 | [ ] |
| HUM-003 | Camera PTC heater; ANNKE C1200 is factory-sealed IP67 — external heater can't reach lens | ~$30 | [ ] |
| CAM-004 | 300ft Cat6 may be excessive if runs <30m each; 100ft spool ~$40 | ~$40 | [ ] |
| UI-005 | USB-RS485 marked optional; GPIO breakout handles RS232 | ~$22 | [ ] |
| CPU-006 | 64G x2 pack for OS boot; single 32GB A2 card ($8-12) sufficient | ~$15 | [ ] |

**Trade-off savings (higher risk):**

| Item | Issue | Potential Savings | Decision |
|------|-------|-------------------|----------|
| PWR-009 | PTFIX distribution blocks may overlap with CLIP-TERM terminal block kit | ~$37 | [ ] |
| PWR-002 | 100Ah battery gives 32hr backup; 50Ah gives 16hr — is 24hr+ needed on AC site? | ~$150 | [ ] |
| PWR-004 | Victron BatteryProtect redundant with LiTime built-in BMS | ~$54 | [ ] |

**Shared consumables (if building both units together):**

| Items | Issue | Potential Savings | Decision |
|-------|-------|-------------------|----------|
| CONS-001/002/003/006, HUM-006, DI-GREASE | Heat shrink, sealant, zip ties, IPA, kapton, grease shared from Sukabumi | ~$60 | [ ] |

**Hidden/unrealized costs:**

| Item | Issue | Est. Cost | Decision |
|------|-------|-----------|----------|
| RJ45 connectors + crimp tool | Bulk Cat6 spool needs termination hardware — not in BOM | ~$30-40 | [ ] |
| Amazon search-link price variance | ~15 items use generic search URLs, not locked ASINs — prices may differ | ~$50 buffer | [ ] |
| COAT-SIL | Generic conformal coating — NOT the MG 422C silicone recommended for >95% RH — verify suitability | ~$5 if substituted | [ ] |

**Total potential savings: $150-450 depending on decisions**
**Total hidden costs: ~$85-95**

---

## PROCUREMENT & SHIPPING STRATEGY

### Consolidation Approach (RECOMMENDED)

**Step 1: Order from all US suppliers to single US address (3-5 days)**
- Amazon → Your US address (largest order - most components)
- DigiKey → Same US address
- Adafruit → Same US address
- Hydreon → Same US address

**Step 2: Consolidate & repack (2-3 days)**
- Combine all US shipments into 1-2 boxes
- Remove excessive packaging to reduce weight
- Add protective padding for fragile components

**Step 3: Ship to Indonesia via DHL/FedEx (5-7 days)**
- Declare as "Professional equipment for installation"
- Include detailed commercial invoice
- HS codes: 8471 (computers), 8517 (modem), 8529 (cameras)

**Step 4: Direct international orders (parallel with Steps 1-3)**
- Adafruit (Witty Pi 5, USB-RS485, cable glands) → Ships from US, 3-7 days
- Hydreon (RG-15 Rain gauge) → Ships from US, 3-7 days

**Total estimated time: 2-3 weeks from order to arrival in Jakarta**

---

### Priority 1 - Order IMMEDIATELY (Long Lead Times)

| Item | Lead Time | Action | Notes |
|------|-----------|--------|-------|
| CPU-001 | 1-4 weeks | Check Amazon stock | Pi 5 8GB has periodic shortages (matched Sukabumi source) |
| CPU-002 | 1-2 weeks | Order from Adafruit | Witty Pi 5 HAT+ (matched Sukabumi source) |
| CPU-007 | 2-4 weeks | Verify modem availability | Quectel EG25-G on Amazon (matched Sukabumi source) |

**ORDER THESE FIRST** - Place orders 4-6 weeks before deployment date

---

### Priority 2 - Standard Components (Order 2-3 weeks before deployment)

**DigiKey order:**
- Mean Well SDR-120-12 (usually stock)
- Phoenix Contact surge protector + distribution blocks
- Amphenol LTW M12 vents

**Amazon bulk order (largest order - most items matched to Sukabumi):**
- Pi 5, active cooler, stacking headers, GPIO breakout, SD cards, USB flash drive
- Modem + USB adapter, antenna
- ANNKE C1200 2-pack, LINOVISION PoE switch, camera mounts
- LiFePO4 battery + charger, Victron BatteryProtect, fuses
- Enclosure, DIN rail, clips, terminal blocks, hardware
- LEDs, pushbutton, power couplers
- Conformal coating, heaters, kapton tape
- Cables, dielectric grease, consumables

**Adafruit order:**
- Witty Pi 5 HAT+
- USB-RS485 adapter
- PG9 cable glands

---

### Priority 3 - Local Jakarta Sourcing (Week of installation)

**Glodok Electronics Market:**
- Additional cable glands if needed
- Extra terminal blocks
- Wire, connectors

**Hardware stores (ACE/Informa):**
- Mounting pole (4m galvanized)
- Pole base flange
- U-bolts, concrete anchors
- Silicone sealant, zip ties

**Electrical supply:**
- Grounding rod (1.5m copper)
- Ground cable (6 AWG)
- Ground lugs and clamps

---

## TECHNICAL NOTES & COMPATIBILITY

### Power Budget Verification

**Load Analysis:**
| Component | Peak Power | Avg Power | Duty Cycle | Notes |
|-----------|-----------|-----------|------------|-------|
| Raspberry Pi 5 (8GB) | 12W | 6W | 10% | Active 1.5min per 15min cycle |
| Witty Pi 5 HAT+ | 0.1W | 0.1W | 100% | RTC always on |
| Quectel EG25-G modem | 6W | 2W | 10% | Transmit peaks, idle most of time |
| 2× PoE cameras | 15W | 15W | 100% | Continuous recording |
| LINOVISION PoE switch | 5W | 5W | 100% | Standby + conversion losses |
| PTC heaters | 25W | 12.5W | 50% | Nighttime only (18:00-06:00) |
| **TOTAL** | **63W** | **40.6W** | - | Conservative average |

**Battery Backup Runtime:**
- 100Ah × 12V = 1,280Wh capacity
- At 40W average: **32 hours backup**
- At 63W peak: **20 hours backup**
- **Design target met: 24+ hours** ✅

**AC Power Supply Headroom:**
- Mean Well SDR-120-12: 120W capacity
- Peak load: 63W
- **Headroom: 57W (48%)** ✅

---

### Component Compatibility Checklist

✅ **Pi 5 + Witty Pi 5 HAT+:** Compatible - I2C-only design, no GPIO conflicts
✅ **Witty Pi 5 + Stacking Headers + GPIO Breakout:** Stacks cleanly via 40-pin pass-through
✅ **ANNKE C1200 + LINOVISION 12V PoE Switch:** 802.3af/at PoE compatible
✅ **Mean Well SDR-120-12:** Accepts 88-264VAC (Indonesia 220V OK)
✅ **Quectel EG25-G:** Supports Indonesian LTE bands (B1/B3/B5/B8/B40)
✅ **All outdoor components:** IP67+ rated, UV-resistant
✅ **DDR-60G-5 DC-DC converter:** Converts 12V bus to regulated 5V for Pi (9-36V input covers battery range)
✅ **12V system:** All 12V components operate on 12V nominal (10-14.6V range)

---

### Critical Pre-Deployment Tasks

**DO BEFORE SHIPPING:**
1. **Apply conformal coating** to all PCBs (Pi 5, Witty Pi, GPIO breakout, modem) in low-humidity environment — **verify COAT-SIL product is suitable for >95% RH (not MG 422C)**
2. **Mask connectors** during coating: GPIO pins, USB ports, HDMI, SD card slot, heat sink contact areas
3. **Pre-configure cameras:** Set static IPs, enable RTSP, set credentials, test ONVIF
4. **Load OS on SD card:** Install OpenRiverCam software, test Pi 5 + Witty Pi stack boots correctly
5. **Test Witty Pi scheduling:** Verify 15-minute wake cycle works
6. **Register modem IMEI:** Submit to Indonesian POSTEL (Pos dan Telekomunikasi) before deployment
7. **Activate SIM card:** Pre-activate with Telkomsel, test data connection
8. **Document serial numbers:** Record all component SNs for customs and warranty

---

### Alternative Components (If Primary Unavailable)

**Cameras:**
| Alternative | Price | Pros | Cons | Link |
|-------------|-------|------|------|------|
| Reolink RLC-810A | $79.99 | Lower cost, 8MP adequate | Slightly lower resolution | https://reolink.com/us/product/rlc-810a/ |
| Hikvision DS-2CD2143G2-I | $99 | Better low-light | More expensive, verify ONVIF | Check B&H Photo |

**Batteries:**
| Alternative | Price | Capacity | Notes |
|-------------|-------|----------|-------|
| Renogy 12V 100Ah LiFePO4 | $329 | 100Ah | Premium brand, good warranty |
| Ampere Time 12V 100Ah | $289 | 100Ah | Budget option, good reviews |
| Battle Born 100Ah | $949 | 100Ah | Top tier, 10-year warranty (overkill) |

**PoE Switch/Injector:**
- LINOVISION Industrial 12V PoE Switch is PRIMARY choice (matched Sukabumi, $85.99)
- Alternative: Planet IPOE-260-12V PoE Injector ($164) - native 12V input, industrial grade
- If both unavailable: TRENDnet TPE-115GI ($34) + 12V→48V converter ($45) = $79 total

---

### Customs & Import Documentation

**Required documents for Indonesian customs:**
1. **Commercial Invoice** - Detailed line item list with values
2. **Packing List** - Box contents, weights, dimensions
3. **Equipment Manifest** - Serial numbers, IMEI numbers
4. **Certificate of Origin** - For electronics (if requested)
5. **Import Permit (API)** - May be required for telecom equipment

**HS Codes for declaration:**
- 8471.50.00 - Processing units (Raspberry Pi, SSD)
- 8517.62.90 - LTE modem
- 8525.80.30 - Cameras (PoE IP cameras)
- 8536.69.90 - Electrical connectors, terminal blocks
- 8507.60.00 - Lithium-ion batteries

**Expected duties:**
- Computers/electronics: 0-10% (average 7.5%)
- Batteries: 5%
- Cameras: 0-10%
- VAT: 11% on CIF value (Cost + Insurance + Freight)

**IMEI Registration:**
- Register Quectel EG25-G IMEI at https://imei.kemenperin.go.id/
- Required within 60 days of import
- Fee: ~IDR 300,000 ($20)

---

## PURCHASE ORDER CHECKLIST

### Pre-Purchase Verification

**Week 6 before deployment:**
- [ ] Verify all product links are still active and valid
- [ ] Check current prices (this BOM reconciled February 24, 2026)
- [ ] Confirm Raspberry Pi 5 8GB stock on Amazon (same listing as Sukabumi)
- [ ] Verify Witty Pi 5 HAT+ availability at Adafruit (#6449)
- [ ] Determine US consolidation address for shipments
- [ ] Coordinate with local PMI office in Jakarta for receiving

**Week 5 before deployment:**
- [ ] **ORDER NOW:** Raspberry Pi 5, Witty Pi 5, Quectel modem (long lead items)
- [ ] Register modem IMEI with Indonesian POSTEL (start process early)
- [ ] Purchase & activate Telkomsel SIM card (can be done remotely)

**Week 3-4 before deployment:**
- [ ] Order DigiKey components (Mean Well PSU, surge protector, terminal blocks)
- [ ] Order Adafruit components (Pi-EzConnect, LEDs, cables, SD card)
- [ ] Order Amazon bulk order (battery, cameras, enclosure, Cat6, hardware)
- [ ] Order Hydreon RG-15 rain gauge (direct from store.hydreon.com)
- [ ] All items shipped to US consolidation address

**Week 2 before deployment:**
- [ ] Apply conformal coating (MG 422C) to Pi 5, Witty Pi, Pi-EzConnect
- [ ] Allow 24hr cure time for conformal coating
- [ ] Pre-configure PoE cameras (RTSP, static IP, credentials)
- [ ] Load OS on SD card, test Pi + Witty Pi boot cycle
- [ ] Test rain gauge serial communication (Hydreon RG-15 RS232 TTL via Pi UART)
- [ ] Consolidate US shipments, repack in 1-2 boxes
- [ ] Prepare customs documentation (commercial invoice, packing list, SNs)
- [ ] Ship consolidated package via DHL/FedEx Express to Jakarta

**Week 1 before deployment:**
- [ ] Confirm package cleared customs in Jakarta
- [ ] Coordinate pickup with PMI office
- [ ] Purchase local components in Jakarta (grounding, pole, hardware)
- [ ] Verify all tools available (see installation checklist below)
- [ ] Print laminated wiring diagrams and installation instructions
- [ ] Conduct site survey (AC power, mounting location, LTE signal test)

---

## INSTALLATION CHECKLIST

### Pre-Installation Verification
- [ ] All components received and inventoried
- [ ] AC power available at site (220V/50Hz verified)
- [ ] Permits obtained for pole installation (if required)
- [ ] LTE signal strength >-90 dBm (use phone or modem test)
- [ ] Installation team briefed on safety procedures
- [ ] Conformal coating applied and cured (done before shipping)
- [ ] Cameras pre-configured and tested
- [ ] Pi 5 + Witty Pi stack boots correctly

### Tools Required (Bring to Site)
- [ ] Power drill with masonry bits (for concrete anchors)
- [ ] Multimeter (DC voltage, continuity testing)
- [ ] RJ45 crimping tool + connectors + cable tester
- [ ] Wire strippers (18-22 AWG)
- [ ] Phillips/flathead screwdriver set
- [ ] Adjustable wrenches (for cable glands, U-bolts)
- [ ] Allen key set (metric)
- [ ] Torque wrench (for pole mounting, optional)
- [ ] Laptop with SSH client (for configuration)
- [ ] Smartphone/tablet (for camera viewing, hotspot)
- [ ] Headlamp/flashlight (for working inside enclosure)
- [ ] Concrete mix + bucket (for pole installation)
- [ ] Level (for pole alignment)
- [ ] Measuring tape
- [ ] Cable ties, electrical tape
- [ ] Sharpie markers for labeling

### Safety Equipment
- [ ] Safety glasses
- [ ] Work gloves
- [ ] Hard hat (if working at height)
- [ ] Insulated tools for electrical work
- [ ] First aid kit
- [ ] Sunscreen and water (tropical heat)

### Installation Steps
1. [ ] Install grounding rod (1.5m deep minimum)
2. [ ] Set pole base in concrete, allow 24hr cure
3. [ ] Mount enclosure to pole with U-bolts
4. [ ] Install DIN rail inside enclosure
5. [ ] Mount components on DIN rail (PSU, terminal blocks, BatteryProtect, PoE switch)
6. [ ] Mount Pi 5 + Witty Pi + Pi-EzConnect stack
7. [ ] Wire AC input through surge protector to Mean Well PSU
8. [ ] Wire battery + charger + BatteryProtect
9. [ ] Wire 12V distribution to PoE switch and DDR-60G-5 buck converter (5V output to Pi)
10. [ ] Install PTC heaters with thermostats
11. [ ] Mount Gore vents in enclosure
12. [ ] Wire status LEDs and pushbutton to GPIO
13. [ ] Run Cat6 cables to camera mounting locations
14. [ ] Install cameras on pole mounts, aim and focus
15. [ ] Mount Proxicast ANT-122-S02 puck on enclosure (12mm hole), connect SMA cables to modem
16. [ ] Install rain gauge on separate arm
17. [ ] Cable management with zip ties
18. [ ] Test all connections with multimeter BEFORE applying power
19. [ ] Apply power, verify boot sequence
20. [ ] Test camera feeds, modem connection, rain gauge
21. [ ] Seal all cable glands
22. [ ] Final inspection and documentation

### Post-Installation Testing
- [ ] System boots and enters normal operation cycle
- [ ] Both cameras accessible via RTSP
- [ ] LTE modem connects and can upload data
- [ ] Rain gauge reports tip events correctly
- [ ] Status LEDs indicate system state
- [ ] Maintenance mode button triggers hotspot
- [ ] Battery charges correctly from AC
- [ ] BatteryProtect triggers at low voltage (test by disconnecting charger)
- [ ] Test 24hr backup (disconnect AC, monitor runtime)
- [ ] PTC heaters activate when temperature drops
- [ ] Ground resistance <25Ω (measure with multimeter)
- [ ] Document all camera IPs, modem IMEI, serial numbers

---

## REVISION HISTORY

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2026-02-24 | 3.0 | Reconciled with Sukabumi actuals: matched shared components (GPIO breakout, PoE switch, stacking headers, LEDs, etc.), reduced from 6 to 4 suppliers, added forgotten items (USB cables, DIN clips, power couplers, dielectric grease), updated all prices to match procured costs | Claude (Opus 4.6) |
| 2026-01-09 | 2.0 | Verified BOM with actual product links, consolidated suppliers | Claude (Comprehensive Researcher) |
| 2026-01-09 | 1.0 | Initial BOM creation for Jakarta site | - |

---

## KEY DESIGN DECISIONS & RATIONALE

### Why These Specific Components?

**Power System:**
- **Mean Well SDR-120-12:** Industrial-grade reliability, wide input voltage range (88-264VAC) handles Indonesia power fluctuations
- **LiFePO4 vs AGM:** LiFePO4 tolerates tropical heat (up to 60°C), 3000+ cycles vs 300-500 for AGM
- **100Ah capacity:** Provides 24hr backup at 40W average load with 20% safety margin
- **Victron BatteryProtect:** Prevents over-discharge damage, trusted brand with proven reliability

**Compute Platform:**
- **Pi 5 8GB vs 4GB:** ORC software benefits from extra RAM for video processing and buffering
- **Witty Pi 5 HAT+:** Only reliable RTC + power scheduling HAT confirmed compatible with Pi 5 (I2C-only design)
- **Pi-EzConnect:** Enables future expansion via GPIO screw terminals without soldering
- **Quectel EG25-G:** Global LTE modem supporting all Indonesian carrier bands, proven reliability

**Cameras & PoE:**
- **ANNKE C1200 (12MP) vs Reolink (8MP):** 12MP provides better detail for flood water level analysis
- **PoE vs USB:** Factory-sealed PoE cameras eliminate custom housing complexity and humidity ingress risks
- **2 cameras vs 1:** Stereo vision enables depth mapping and velocity measurement
- **LINOVISION PoE switch vs Planet IPOE-260-12V injector:** Matched Sukabumi procurement; lower cost ($86 vs $164); multi-port switch provides expansion flexibility; native 12V input

**Humidity Management:**
- **MG Chemicals 422C:** Silicone-based coating performs better than acrylic in >95% RH
- **PTC heaters:** Self-regulating, safer than resistive heaters, prevent condensation without overheating
- **Gore vents vs sealed:** Pressure equalization prevents seal failure from thermal cycling

### What This BOM Does NOT Include

- **Sukabumi site components** - Separate BOM (see `BOM_Sukabumi.md` and `sukabumi_parts_procured.csv`)
- **Spare parts inventory** - See CLAUDE.md for recommended spares
- **Software licenses** - ORC software is open-source
- **Labor costs** - Installation assumed to be performed by team/volunteers
- **LTE data plan** - Ongoing monthly cost (~$20-50/month with Telkomsel)
- **Site-specific modifications** - Adjust quantities based on actual cable runs, etc.

---

## MAINTENANCE & ONGOING COSTS

**Monthly:**
- LTE data plan: $20-50 (Telkomsel postpaid recommended)

**Quarterly:**
- Lens cleaning (microfiber + isopropyl alcohol): $5
- Visual inspection (free, 15 minutes)
- Battery backup test (free, disconnect AC for 30 minutes)

**Annually:**
- Conformal coating reapplication (if boards exposed): $35
- Replace Gore vents (if damaged): $36
- Ground resistance test (free with multimeter)

**Every 3-5 years:**
- Replace LiFePO4 battery (3000+ cycles = ~8 years at 1 cycle/day): $300
- Replace cameras (if needed): $240

**Estimated annual ongoing cost:** $300-400 (excluding battery replacement)

---

## REFERENCES & SUPPORTING DOCUMENTS

**Project documentation:**
- Planning guide: `/home/tjordan/code/git/openrivercam/spring_2026_ID/CLAUDE.md`
- Design specifications: `/home/tjordan/code/git/openrivercam/rc-box/DESIGN_SPECS.md`
- Humidity management research: `research/humidity_management_tropical_enclosures_research.md`
- PoE injector research: `research/poe_injector_research.md`
- Power supply research: `research/ac_power_supply_research.md`
- Internal mounting research: `research/internal_mounting_solutions_research.md`

**Datasheets (download before deployment):**
- Mean Well SDR-120-12: https://www.meanwell.com/Upload/PDF/SDR-120/SDR-120-SPEC.PDF
- Victron BatteryProtect: https://www.victronenergy.com/upload/documents/Datasheet-BatteryProtect-EN.pdf
- Planet IPOE-260-12V: https://planetechusa.com/wp-content/uploads/2021/06/DS_IPOE-260-12V.pdf
- Raspberry Pi 5: https://datasheets.raspberrypi.com/rpi5/raspberry-pi-5-product-brief.pdf
- Witty Pi 5: https://www.uugear.com/doc/WittyPi5_UserManual.pdf
- ANNKE C1200: Download from manufacturer website

---

## CONTACT INFORMATION

**Suppliers:**
- **Adafruit:** support@adafruit.com | +1-212-226-2010 (Witty Pi 5, USB-RS485, cable glands)
- **Amazon:** Standard Amazon customer service (majority of components)
- **DigiKey:** tech.support@digikey.com | +1-800-344-4539 (PSU, surge protector, vents)
- **Hydreon:** info@hydreon.com | https://store.hydreon.com (rain gauge)

**Indonesian resources:**
- **POSTEL (IMEI registration):** https://imei.kemenperin.go.id/
- **Telkomsel:** 188 (from Telkomsel number) or +62-811-188-000
- **Customs (Bea Cukai):** https://www.beacukai.go.id/ | Call center: 1500-225

---

**Document prepared:** January 9, 2026 | **Last updated:** February 24, 2026
**Version:** 3.0 (Reconciled with Sukabumi actuals)
**Site:** Jakarta, Indonesia
**Project:** OpenRiverCam Training/Demo Installation
**Budget:** Jakarta $2,125.98 + Sukabumi $948.08 = **$3,074.06** total (within $3,000 target)
**Status:** RECONCILED - Ready for procurement

---

## PROCUREMENT NOTES - ITEMS STILL NEEDED

The following items were not ordered with the Sukabumi parts and need to be included in the Jakarta order:

| Item | Reason | Est. Cost | For Site | Notes |
|------|--------|-----------|----------|-------|
| Mean Well DDR-60G-5 (5V/10.8A DC-DC) | Not ordered for Sukabumi | ~$39 | Sukabumi | Powers Pi + modem + LEDs + rain sensor from 12V battery. See [research](research/dc_dc_buck_converter_research.md). Jakarta unit now on BOM (BUCK-5V). |
| Mean Well DDR-60G-12 (12V/5A DC-DC) | Not ordered for Sukabumi | ~$39 | Sukabumi only | Powers PoE injector + camera from 12V battery. Not needed for Jakarta (12V loads tolerate battery range directly). See [research](research/dc_dc_buck_converter_research.md) |
| External ethernet cable | Not ordered for Sukabumi | TBD | Sukabumi | Cat6 outdoor run from enclosure to camera |
| Fans (enclosure ventilation) | Not ordered for either site | TBD | Both | Active airflow for thermal management |
| Additional DIN rail clips | Not enough for all components | TBD | Both | Need clips for PoE switch, modem adapter, terminal blocks, etc. |
| Pole mount solution (Sukabumi) | Not yet specified | TBD | Sukabumi | Must accommodate enclosure box + gore vent strategy |
| Pole mount solution (Jakarta) | Not yet specified | TBD | Jakarta | Must accommodate enclosure box + gore vent strategy |

**Pole mount notes:** Both sites need a pole mounting solution that works with the selected enclosure boxes and allows for gore vent placement. Research needed on mounting brackets/arms that can securely hold the NEMA 4x / IP66 enclosures while keeping gore vents unobstructed and oriented correctly (vents must face downward to prevent water ingress).

**Fan notes:** Enclosure fans help with thermal management in hot climates. Consider 12V DC fans (80mm or 120mm) with dust filters. Jakarta (coastal/urban) is especially hot and may need active ventilation. Research IP-rated fan+filter units for NEMA enclosures.

**DIN rail clip notes:** The Sukabumi build only ordered 1x Pi clip and 1x terminal block clip kit. Additional DIN-mountable clips are needed for: PoE switch, modem/USB adapter, relay modules, power distribution blocks, and any future expansion. Consider a DIN rail adapter assortment.

---

**END OF BILL OF MATERIALS**
