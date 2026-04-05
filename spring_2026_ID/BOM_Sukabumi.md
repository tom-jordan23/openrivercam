# Bill of Materials - Sukabumi Site
## Indonesia River Monitoring Station Deployment

**Site:** Sukabumi, Indonesia (foothills)
**Power:** Solar (existing 200W panel / 50Ah battery - reused from failed unit)
**Camera:** Single PoE IP camera (ANNKE C1200) with built-in IR
**Purpose:** Replacement of failed river monitoring unit
**Date:** January 9, 2026
**Budget Target:** <$1,500 USD (half of $3,000 total for both sites)

---

## Design Approach

**Standalone Enclosure (deployable with or without outer box):**
- **Primary enclosure:** VEVOR carbon steel hinged IP66 box (16×12×8" / 406×305×203mm) houses all electronics
- Hinged door with lock for easy field access — no screws to remove
- Includes removable galvanized mounting plate (backplate)
- Fully self-contained: Pi stack, PoE injector, modem, USB flash drive, terminal blocks, status LED, pushbutton, antenna
- Can be pole-mounted standalone at sites without an existing outer box
- At Sukabumi: sits inside existing outer aluminum box for bonus physical protection
- Gore vent for pressure equalization; all cables enter through IP68 cable glands

**Camera Strategy:**
- Factory-sealed PoE IP camera (ANNKE C1200, 12MP, built-in IR LEDs)
- Planet IPOE-260-12V PoE injector powered from 12V solar battery
- PoE injector power-cycled with Pi via Witty Pi schedule (camera boots each cycle)
- 1 camera installed, 1 spare from 2-pack
- Day/night configuration switching handled in ORC software

**Humidity Protection Strategy (Layered):**
1. **Primary:** IP66 sealed carbon steel enclosure with Gore vent
2. **Secondary:** Silicone conformal coating (MG 422C) on all PCBs
3. NO PTC heaters (solar power budget constraint)
4. NO desiccant (ineffective at 95% RH)

**Key Principles:**
- Commodity electronics only (no custom PCBs)
- No soldering or cable cutting (screw terminals only)
- Field serviceable by semi-technical personnel
- All connections via plug-in or screw terminals

---

## Component Categories

1. [Compute Platform](#1-compute-platform)
2. [PoE Camera System](#2-poe-camera-system)
3. [User Interface](#3-user-interface)
4. [Humidity Protection](#4-humidity-protection)
5. [Enclosure & Mounting](#5-enclosure--mounting)
6. [Rain Gauge](#6-rain-gauge)
7. [Cables & Connectors](#7-cables--connectors)
8. [Hardware & Fasteners](#8-hardware--fasteners)

---

## 1. Compute Platform

| Item | Description | Qty | Unit Price | Ext. Price | Source | Notes |
|------|-------------|-----|------------|------------|--------|-------|
| **RPi5-8GB** | Raspberry Pi 5, 8GB RAM | 1 | $80.00 | $80.00 | Adafruit, CanaKit | MSRP, verify availability |
| **WittyPi5** | Witty Pi 5 HAT+ (power mgmt, RTC, I2C-only) | 1 | $46.00 | $46.00 | UUGear | Per CLAUDE.md research |
| **CR2032** | CR2032 Coin Cell Battery for Witty Pi 5 RTC | 1 | $3.00 | $3.00 | Amazon | Replaces Pi 5 ML-2020 (connector failed on both boards) |
| **EZCONNECT** | Adafruit Pi-EzConnect (ID 2711, GPIO terminal block) | 1 | $19.95 | $19.95 | Adafruit | Stacks on Witty Pi 5 HAT+ |
| ~~**USB-DRIVE**~~ | ~~Samsung FIT Plus 256GB USB 3.1 flash drive (MUF-256AB)~~ | ~~1~~ | ~~$25.00~~ | ~~$0.00~~ | | **REMOVED** — UAS boot storm (see known_issues.md #1). Captures on SD card rootfs (~43GB free) |
| **MODEM** | Quectel EG25-G LTE Cat 4 module | 1 | $35.00 | $35.00 | AliExpress, Mouser | Verify Indonesian bands |
| **MODEM-USB** | EXVIST Mini PCIe-USB adapter (P2U52V02USB) for EG25-G | 1 | $15.00 | $15.00 | AliExpress | USB interface for modem |
| **ANT-PUCK** | Proxicast ANT-122-S02 2x2 MIMO LTE puck antenna (IP67, screw mount) | 1 | $65.00 | $65.00 | [Amazon](https://www.amazon.com/Proxicast-Profile-Omni-Directional-Screw-Mount-Antenna/dp/B07DDC9WV5) | Main + diversity in single sealed unit; 600-6000 MHz; eliminates bulkhead connectors |
| **SD-CARD** | MicroSD card 32GB (SanDisk/Samsung) | 1 | $8.00 | $8.00 | Amazon | For OS boot |
| **HEATSINK** | Heatsink for Raspberry Pi 5 | 1 | $8.00 | $8.00 | Included or Amazon | Active or passive |
| **USB-RS485** | USB to RS485 converter (FTDI chip) | 1 | $18.00 | $18.00 | Amazon, DigiKey | For Modbus devices |
| **SENSOR-TH** | Adafruit Sensirion SHT40 Temp/Humidity Sensor (I2C, STEMMA QT) | 1 | $5.95 | $5.95 | [Adafruit](https://www.adafruit.com/product/4885) | Enclosure climate monitoring; ±1.8% RH full range; on-chip heater for high-humidity drift recovery |
| **CABLE-QT** | Adafruit STEMMA QT to bare wire cable (4-pin JST SH, 200mm) | 1 | $0.95 | $0.95 | [Adafruit](https://www.adafruit.com/product/4209) | Connects SHT40 to G469 screw terminals (SDA=GPIO2, SCL=GPIO3, 3.3V, GND) |
| **PROBE-TEMP** | DS18B20 Waterproof Temperature Probe (stainless, 1m cable, 4-pack) | 1 | $9.99 | $9.99 | [Amazon](https://www.amazon.com/Temperature-Waterproof-Stainless-Compatible-Raspberry/dp/B0FH4WRN6H) | Outside temp for dew point calculation; 1-Wire GPIO; IP67 |
| | | | **Subtotal** | **$336.84** | | |

**Notes:**
- Pi 5 8GB preferred for ORC (4GB minimum would save ~$15)
- Quectel EG25-G confirmed compatible with Telkomsel (B1/B3/B5/B8/B40)
- ~~Samsung FIT Plus 256GB~~ — removed from build due to UAS driver boot storm (228 USB disconnects in 12 min). See `build_notes/sukabumi/known_issues.md` for details. SD card rootfs provides ~43GB, sufficient for weeks of video buffer at 5s/15min capture rate. USB 3.0 port available if a compatible drive is added later (requires `cmdline.txt` quirk or non-UAS drive)
- Witty Pi 5 HAT+ provides scheduling, RTC, and low-power sleep
- Pi-EzConnect enables future sensor expansion via screw terminals
- Proxicast ANT-122-S02 replaces basic stick antennas + bulkhead connectors; IP67 sealed screw-mount puck eliminates connector corrosion failure point; same model used at Jakarta site (see `research/lte_antenna_weatherproof_research.md`)

---

## 2. PoE Camera System

| Item | Description | Qty | Unit Price | Ext. Price | Source | Notes |
|------|-------------|-----|------------|------------|--------|-------|
| **CAM-001** | ANNKE C1200 PoE IP Camera (12MP, 134° FOV, 2-pack) | 1 | $119.99 | $119.99 | [Amazon](https://www.amazon.com/ANNKE-Security-Surveillance-Detection-Spotlight/dp/B0DBHRMT1V) | 1 camera installed, 1 spare; built-in IR LEDs for night vision |
| **CAM-002** | Planet IPOE-260-12V PoE Injector (2-port, 60W, 12V input) | 1 | $164.00 | $164.00 | [Planet Technology](https://planetechusa.com/product/ipoe-260-12v-industrial-2-port-10-100-1000t-802-3at-poe-injector-hub-12v-booster/) | Native 12V input from solar battery; power-cycled with Pi |
| **CAM-004** | Outdoor Cat6 Shielded Cable (300ft, UV-resistant) | 1 | $79.99 | $79.99 | [Amazon](https://www.amazon.com/s?k=outdoor+Cat6+shielded+cable+300ft+UV) | Camera cabling |
| **CAM-005** | IP68 RJ45 Waterproof Coupler (2-pack) | 1 | $12.99 | $12.99 | [Amazon](https://www.amazon.com/s?k=IP68+RJ45+coupler+waterproof) | Weatherproof connections |
| **CAM-006** | Camera Pole Mount Bracket (stainless, 2-pack) | 1 | $22.99 | $22.99 | [Amazon](https://www.amazon.com/s?k=camera+pole+mount+bracket+stainless) | Camera mounting |
| **RELAY-POE** | Electronics-Salon DIN Rail 4-SPDT 10A Relay Module, 5V | 1 | $18.00 | $18.00 | [Amazon](https://www.amazon.com/Electronics-Salon-Mount-Interface-Module-Version/dp/B00M1MW5BW) | Switches 12V to PoE injector; GPIO or passive USB trigger. See [research](research/poe_switch_relay_research.md) |
| | | | **Subtotal** | **$417.96** | | |

**Notes:**
- **Power-cycled operation:** PoE injector power switched by Electronics-Salon DIN relay. Relay can be triggered by GPIO pin (systemd service) or passively by USB power (zero software). When Witty Pi 5 cuts power at sleep, relay opens and PoE injector loses 12V. See [poe_switch_relay_research.md](research/poe_switch_relay_research.md) for wiring details.
- **Camera boot time:** ~45-60 seconds. Active phase extended to ~150s per cycle to accommodate boot + capture + upload.
- **Built-in IR:** ANNKE C1200 has integrated IR LEDs with automatic day/night switching. No separate IR illuminator or relay needed.
- **Day/night config:** ORC software will handle switching between day and night capture configurations.
- **1 camera installed** at Sukabumi (single viewpoint). Second camera from 2-pack kept as spare at PMI office.
- Same camera model as Jakarta site for parts commonality.
- Pre-configure camera before deployment: set static IP, set credentials, push streaming/image/NTP config via `camtool.py`. Video capture is via RTSP pull (orc-capture), not FTP.

---

## 3. User Interface

| Item | Description | Qty | Unit Price | Ext. Price | Source | Notes |
|------|-------------|-----|------------|------------|--------|-------|
| **LED-WS2812B** | WS2812B (NeoPixel) addressable RGB LED pixel PCB | 1 | $3.40 | $3.40 | Amazon (FILN 5-pack, Coupa #484675) | Single LED, all colors via GPIO 18. See `docs/LED_STATUS_SPEC.md` |
| **BTN-MAINT** | IP67 momentary pushbutton (C&K AP or E-Switch PVA6) | 1 | $12.00 | $12.00 | DigiKey, Mouser | Maintenance mode input |
| **GLAND-BTN** | PG9 cable gland for button wiring | 1 | $3.00 | $3.00 | Amazon, DigiKey | 16mm panel hole |
| | | | **Subtotal** | **$18.40** | | |

**Notes:**
- WS2812B status LED driven from GPIO 18 (PWM0) via Pi-EzConnect screw terminals; powered from 5V Pi rail
- Color meanings config-driven via `/etc/orc/led-status.yaml`; see `docs/LED_STATUS_SPEC.md` for full state table
- Button: Short press = show status, Long press (3s) = enter maintenance mode
- Maintenance mode: prevents auto-shutdown, starts WiFi hotspot, enables SSH
- LED visible at 3-5m distance behind sealed acrylic light window (no display power needed)
- Recessed button mounting prevents accidental activation

---

## 4. Humidity Protection

| Item | Description | Qty | Unit Price | Ext. Price | Source | Notes |
|------|-------------|-----|------------|------------|--------|-------|
| **COAT-SIL** | MG Chemicals 422C silicone conformal coat (55ml) | 1 | $22.00 | $22.00 | DigiKey, Amazon | Backup protection for PCBs |
| **BRUSH** | Application brush (acid brush or fine bristle) | 2 | $2.00 | $4.00 | Hardware store | Clean, lint-free |
| **MASK-TAPE** | Masking tape (low-tack, 1" width) | 1 | $4.00 | $4.00 | Hardware store | Protect connectors during coating |
| **IPA-WIPES** | Isopropyl alcohol wipes (99%) | 1 | $8.00 | $8.00 | Amazon | Pre-coating cleaning |
| | | | **Subtotal** | **$38.00** | | |

**Notes:**
- **Primary protection:** Sealed IP67 inner enclosure (see Section 6)
- **Secondary protection:** Conformal coating on PCBs (belt-and-suspenders approach)
- Apply conformal coating to: Raspberry Pi 5, Witty Pi 5 HAT+, Pi-EzConnect
- MASK: All connectors (USB, HDMI, GPIO pins, SD card slot), heat sink contact areas
- Apply in low-humidity environment (ideally <60% RH), allow 24hr cure before assembly
- Gore vent on inner box (Section 6) provides pressure equalization
- NO PTC heaters due to solar power budget constraint
- NO desiccant (ineffective at 95% RH)

---

## 5. Enclosure & Mounting

**Standalone enclosure** capable of outdoor deployment with or without existing outer box. Houses all electronics except solar panel, charge controller, and battery.

| Item | Description | Qty | Unit Price | Ext. Price | Source | Notes |
|------|-------------|-----|------------|------------|--------|-------|
| **ENCLOSURE** | | | | | | |
| **ENC-001** | VEVOR carbon steel hinged IP66 enclosure (16×12×8" / 406×305×203mm) | 1 | $60.00 | $60.00 | [Amazon](https://www.amazon.com/dp/B0924DJGJ9) | Hinged door with lock; includes mounting plate |
| **VENT-ENC** | Gore M12 protective vent | 1 | $12.00 | $12.00 | DigiKey, Mouser | Pressure equalization without humidity ingress |
| **CABLE ENTRY** | | | | | | |
| **ENC-004** | Cable Gland Assortment (PG9/PG13.5/PG16, 20-pack) | 1 | $18.99 | $18.99 | Amazon | Various cable entries |
| **MOUNTING HARDWARE** | | | | | | |
| **VELCRO-LOCK** | 3M Dual Lock reclosable fastener (25mm × 1m) | 1 | $12.00 | $12.00 | Amazon | Mount modem, PoE injector |
| **STANDOFFS** | M2.5/M3 standoff kit (brass or nylon) | 1 | $12.00 | $12.00 | Amazon | Pi stack mounting |
| **TERM-BLOCK** | Screw terminal blocks (2-8 position, assorted) | 1 | $10.00 | $10.00 | Amazon, DigiKey | Power distribution |
| **DIN-PCB** | Molence C45 PCB DIN Rail Clip-Pairs (10 sets) | 1 | $9.00 | $9.00 | [Amazon](https://www.amazon.com/Molence-Mounting-Adapter-Circuit-Bracket/dp/B09KZHY8G4) | Mount bare PCBs to DIN rail. See [research](research/din_rail_mounting_clips_research.md) |
| **DIN-CLIP** | CNQLIS 1.65" Aluminum DIN Rail Mounting Clips (10-pack) | 1 | $13.00 | $13.00 | [Amazon](https://www.amazon.com/CNQLIS-Universal-Mounting-Bracket-Countersunk/dp/B0CJJ1DBZM) | Mount modem, USB adapters, misc items via screws/zip ties. See [research](research/din_rail_mounting_clips_research.md) |
| | | | **Subtotal** | **$146.99** | | |

**Notes:**

**Enclosure Strategy:**
- **VEVOR 16×12×8" carbon steel hinged enclosure** — hinged door with lock eliminates removing screws for field access
- Includes removable galvanized mounting plate (backplate) for component mounting
- 1.5mm cold-rolled steel, powder-coated, IP66/NEMA 4X rated
- **Standalone-capable:** Can be wall/pole-mounted directly at sites without an existing outer enclosure
- **At Sukabumi:** Sits inside existing outer aluminum box for bonus physical/weather protection
- Components mounted with standoffs (Pi stack) and Velcro/Dual Lock (modem, PoE injector) on mounting plate
- ~~Samsung FIT Plus~~ removed — see Section 1 notes

**Panel-Mount Components (drilled into enclosure lid or side):**
- 1× 10-12mm hole for status LED light window
- 1× 16mm hole for IP67 pushbutton
- 1× 12mm hole for Proxicast antenna mount (1/2" + locking nut)
- Cable glands for: 12V power in, Cat6 to camera, rain gauge cable
- LED light window, button, and antenna housings self-seal against panel

**Antenna Mounting:**
- Proxicast ANT-122-S02 screw-mounts to top surface of enclosure (single 1/2" / 12mm hole + locking nut)
- 2× SMA cables route internally to Quectel EG25-G main + diversity ports
- No external SMA bulkhead connectors needed (eliminates corrosion failure point)
- Same antenna model used at Jakarta site for parts commonality

**Cable Entry:**
- PG9: Rain gauge serial + 12V (×1), 12V power in (×1), antenna (internal)
- PG13.5/PG16: Cat6 to camera (×1)
- Spare glands for future expansion

---

## 6. Rain Gauge

| Item | Description | Qty | Unit Price | Ext. Price | Source | Notes |
|------|-------------|-----|------------|------------|--------|-------|
| **RAIN-GAUGE** | Hydreon RG-15 Optical Rain Gauge (solid-state, RS232 TTL 3.3V + pulse output) | 1 | $99.00 | $99.00 | [Hydreon Store](https://store.hydreon.com/RG-15.html) | No moving parts; self-cleaning lens; ±10% accuracy |
| | | | **Subtotal** | **$99.00** | | |

**Notes:**
- **Solid-state optical sensor** — no tipping bucket, no moving parts, no clogging from tropical debris
- Self-cleaning round lens surface discourages debris collection
- **Dual output:** RS232 TTL at 3.3V (connects directly to Pi UART via EzConnect terminals) + open-collector pulse output emulating tipping bucket
- Serial interface provides real-time rainfall rate, accumulated total, and configurable resolution (0.2mm or 0.02mm)
- DIP switches for configuration (units, resolution, operating mode); also configurable via serial commands
- Very low power: ~110µA idle (dry), under 2mA active (raining); well-suited to solar applications
- Powered from 12V system supply (5-35V input range per manufacturer)
- Built-in mounting holes — no separate bracket needed
- Operating temp: -40°C to +60°C
- Mount in open area away from structures (>2m from walls/trees)
- Order direct from Hydreon (US-based); Amazon third-party sellers charge 2x+ markup

**Data Collection During Power Cycling (Sukabumi-specific):**

The Pi power-cycles every 15 minutes (awake ~150s, asleep ~14 min). The RG-15 must
collect rainfall continuously, including while the Pi sleeps.

- **Hardware solution:** RG-15 is powered from TB1 (always-on 12V battery bus), not from
  a relay-switched circuit. It draws ~150µA idle — negligible impact on solar budget
  (~0.04 Wh/day). The RG-15 stays powered 24/7 and accumulates rainfall internally.
- **Software requirement:** On each wake cycle, the capture script must:
  1. Open UART (`/dev/ttyAMA0`, 9600 baud, 8N1)
  2. Send `A\n` command to read accumulated rainfall since last `A` poll
     (returns e.g. `Acc 0.000 in`). Note: `R\n` returns a full data dump
     (Acc + EventAcc + TotalAcc + RInt) — either works, `A` is simpler to parse
  3. Compare to the previous reading (stored on disk) to compute interval rainfall
  4. Log the interval rainfall with timestamp
  5. Optionally send `O\n` to reset TotalAcc counter (or just track deltas)
- **Why not reset each cycle?** Tracking deltas (rather than resetting) is safer — if a
  read fails or the Pi crashes mid-cycle, no rainfall data is lost. The accumulator
  persists as long as the RG-15 has power.
- **Jakarta:** This is not an issue at Jakarta since the Pi runs continuously on AC power
  and can poll the RG-15 at any interval.

---

## 7. Cables & Connectors

| Item | Description | Qty | Unit Price | Ext. Price | Source | Notes |
|------|-------------|-----|------------|------------|--------|-------|
| **BUCK-5V** | Mean Well DDR-60G-5 DIN Rail DC-DC Converter (5V 10.8A, 9-36V input) | 1 | $39.00 | $39.00 | [Amazon](https://www.amazon.com/s?k=DDR-60G-5+Mean+Well) | Powers Pi + modem + status LED + rain sensor. See [research](research/dc_dc_buck_converter_research.md) |
| **BUCK-12V** | Mean Well DDR-60G-12 DIN Rail DC-DC Converter (12V 5A, 9-36V input) | 1 | $39.00 | $39.00 | [Amazon](https://www.amazon.com/s?k=DDR-60G-12+Mean+Well) | Powers PoE injector + camera. See [research](research/dc_dc_buck_converter_research.md) |
| **USB-C-PWR** | USB-C power cable (1.5m, right-angle) | 1 | $8.00 | $8.00 | Amazon | Pi 5 power from 5V buck converter |
| **USB-A-SHORT** | USB-A cables (0.5m, various) | 3 | $4.00 | $12.00 | Amazon | Modem, relay, short runs |
| **HDPE-CONDUIT** | HDPE flexible conduit (20mm × 5m) | 1 | $15.00 | $15.00 | Hardware store | Cable protection (if not using Bulgin) |
| **HEAT-SHRINK** | Heat shrink tubing kit (assorted sizes) | 1 | $10.00 | $10.00 | Amazon | Cable sealing, strain relief |
| **CABLE-TIES** | UV-resistant cable ties (assorted, 100pc) | 1 | $8.00 | $8.00 | Amazon | Cable management |
| **WIRE-18AWG** | 18AWG stranded wire (red/black, 10m each) | 1 | $15.00 | $15.00 | Amazon | Power distribution |
| **FERRULES** | Wire ferrules (assorted, crimper kit) | 1 | $18.00 | $18.00 | Amazon | Professional terminal connections |
| | | | **Subtotal** | **$164.00** | | |

**Notes:**
- Mean Well DDR-60G pair provides regulated 12V and 5V from battery. See [dc_dc_buck_converter_research.md](research/dc_dc_buck_converter_research.md) for full analysis
- Cell modem and status LED powered via Pi USB/GPIO (load on 5V rail, not 12V)
- Right-angle USB-C connector reduces strain on Pi 5 power port
- Ferrules recommended for all screw terminal connections (prevents wire fraying)
- UV-resistant cable ties essential for outdoor tropical environment
- HDPE conduit provides budget alternative to IP67-rated cable runs

---

## 8. Hardware & Fasteners

| Item | Description | Qty | Unit Price | Ext. Price | Source | Notes |
|------|-------------|-----|------------|------------|--------|-------|
| **SS-SCREWS** | Stainless steel screw assortment (M3, M4, M5) | 1 | $15.00 | $15.00 | Amazon | 304/316 grade for corrosion resistance |
| **SS-NUTS** | Stainless steel nut assortment (M3, M4, M5) | 1 | $10.00 | $10.00 | Amazon | Nyloc and standard |
| **SS-WASHERS** | Stainless steel washer assortment | 1 | $8.00 | $8.00 | Amazon | Flat and split lock |
| **POLE-CLAMP** | Stainless U-bolt clamp (for pole mounting, 60mm) | 2 | $8.00 | $16.00 | Amazon | Camera housing mount |
| **SEALANT** | Silicone sealant (outdoor, clear) | 1 | $6.00 | $6.00 | Hardware store | Cable gland sealing |
| **DI-GREASE** | Dielectric grease (small tube) | 1 | $8.00 | $8.00 | Amazon | Connector protection |
| **DESICCANT** | Silica gel packets (for initial assembly only) | 1 | $6.00 | $6.00 | Amazon | Not for field maintenance |
| **BAND-SS** | 3/4" Stainless Steel Banding with Buckles (pole mount kit or roll) | 1 | $40.00 | $40.00 | Amazon | No-drill pole mount; 2-3 bands around enclosure + pole |
| **PAD-EPDM** | EPDM Rubber Sheet 1/8" (12"×12") | 1 | $10.00 | $10.00 | Amazon | Galvanic isolation between carbon steel enclosure and galvanized pole |
| | | | **Subtotal** | **$119.00** | | |

**Notes:**
- Use stainless steel 304 minimum (316 preferred for coastal areas)
- Apply dielectric grease to all outdoor connectors (SMA, power terminals)
- Desiccant included for initial assembly in controlled environment only
- Do NOT plan to replace desiccant in field (defeats Gore vent strategy)

---

## TOTAL BOM COST SUMMARY

| Category | Subtotal |
|----------|----------|
| 1. Compute Platform | $336.84 |
| 2. PoE Camera System | $417.96 |
| 3. User Interface | $18.40 |
| 4. Humidity Protection | $38.00 |
| 5. Enclosure & Mounting | $146.99 |
| 6. Rain Gauge | $99.00 |
| 7. Cables & Connectors | $164.00 |
| 8. Hardware & Fasteners | $119.00 |
| **TOTAL (Materials)** | **$1,340.19** |

**Budget Status:** ✅ Within $1,500 target for Sukabumi site
**Remaining Budget (of $3,000 total):** ~$1,727 for Jakarta site + shared spares
**Note:** Equipment travels with installer under humanitarian exemption — no shipping, customs, or contingency costs.

---

## Power Budget Analysis

### Solar System (Existing)
- Solar panel: 200W
- Battery: 12V 50Ah = 600Wh capacity
- Usable capacity (50% DoD): 300Wh/day

### Daily Power Consumption Estimate

**Active Phase (15-minute cycle, 96 cycles/day):**

Note: Active phase is ~150s per cycle to accommodate PoE camera boot time (~45-60s) + capture (5s) + upload.

| Component | Power | Duration/Cycle | Energy/Cycle | Daily (96 cycles) |
|-----------|-------|----------------|--------------|-------------------|
| Raspberry Pi 5 (active) | 8W | 150s | 0.33 Wh | 32.0 Wh |
| USB flash drive | 0.5W | 150s | 0.02 Wh | 2.0 Wh |
| PoE Camera (via injector) | 8W | 150s | 0.33 Wh | 32.0 Wh |
| PoE Injector (overhead) | 5W | 150s | 0.21 Wh | 20.0 Wh |
| LTE Modem (upload) | 3W | 30s | 0.025 Wh | 2.4 Wh |
| Witty Pi 5 (active) | 0.5W | 150s | 0.021 Wh | 2.0 Wh |
| **Active subtotal** | | | | **90.4 Wh/day** |

**Sleep Phase (always-on loads):**
| Component | Power | Duration | Daily Energy |
|-----------|-------|----------|--------------|
| Witty Pi 5 (sleep) | 0.025W | 22.5 hr | 0.56 Wh |
| LTE Modem (standby) | 0.1W | 24 hr | 2.4 Wh |
| DDR-60G-5 (quiescent) | 0.5W | 24 hr | 12.0 Wh |
| DDR-60G-12 (quiescent) | 0.5W | 24 hr | 12.0 Wh |
| Hydreon RG-15 (idle) | 0.002W | 24 hr | 0.04 Wh |
| **Sleep subtotal** | | | **27.0 Wh/day** |

**Note:** The DDR-60G buck converters are always powered from TB1 (they have no enable/shutdown pin). Their quiescent draw (~0.5W each) is the largest always-on load. The RG-15's 150µA idle draw is negligible. If sleep-phase power becomes a concern, adding a relay or load switch to disconnect the DDR-60G-12 (camera circuit) during sleep would save ~12 Wh/day.

**LED Status Indicator:**
| Component | Power | Duration | Daily Energy |
|-----------|-------|----------|--------------|
| 1× WS2812B (typical) | 0.1W | 24 hr | 2.4 Wh |

**TOTAL DAILY CONSUMPTION:** ~120 Wh/day (90.4 active + 27.0 sleep + 2.4 LED)

**Solar Generation (Sukabumi - foothills, decent sun):**
- 200W panel × 4.5 peak sun hours × 0.8 efficiency = ~720 Wh/day
- **Margin:** 720 Wh generation - 120 Wh consumption = **600 Wh surplus**

**Battery Runtime (no sun):**
- 300 Wh usable ÷ 120 Wh/day = **2.5 days autonomy**

**Status:** ✅ Good power budget margin. The always-on buck converter quiescent draw (~24 Wh/day) is notable but well within solar capacity. If autonomy needs to be extended, the DDR-60G-12 (camera circuit) could be disconnected during sleep via a relay to save ~12 Wh/day.

---

## Critical Path Items (Long Lead Times)

### URGENT - Order Immediately for March/April Deployment

| Item | Lead Time | Action Required |
|------|-----------|-----------------|
| **Witty Pi 5 HAT+** | 1-2 weeks | Order from UUGear (stock availability varies) |
| **Quectel EG25-G + EXVIST Mini PCIe-USB** | 2-4 weeks | AliExpress or Mouser (verify stock) |
| **Planet IPOE-260-12V** | 1-2 weeks | Check Planet Technology distributor stock |

### Standard Lead Time (1-2 weeks)

All other components (ANNKE cameras, Cat6 cable, enclosures, etc.) available from Amazon, DigiKey, Mouser with standard shipping.

---

## Local Sourcing Recommendations (Indonesia)

### Items to Source Locally in Indonesia (Avoid Shipping)

| Item | Reason | Where to Buy |
|------|--------|--------------|
| Enclosures | Heavy, bulky, reduce shipping costs | Toko elektronik, Tokopedia |
| Cable glands | Available locally, cheap | Industrial supply stores |
| HDPE conduit | Heavy, cheap locally | Toko bangunan (hardware stores) |
| Stainless hardware | Heavy, reduce customs scrutiny | Hardware stores |
| Silicone sealant | Liquid restrictions | Hardware stores |
| Cable ties | Bulky, cheap | Any electronics store |
| Dielectric grease | Liquid, available locally | Auto parts stores |

**Estimated savings:** ~$150 in shipping costs

### Items to Bring from US

- Raspberry Pi 5 (may not be available in Indonesia)
- Witty Pi 5 HAT+ (specialty item)
- Adafruit Pi-EzConnect (specialty item)
- ANNKE C1200 PoE camera (quality/warranty)
- Planet IPOE-260-12V PoE injector (specialty item)
- Conformal coating (specific product required)
- Proxicast ANT-122-S02 LTE antenna (specialty item, counterfeit risk locally)
- Hydreon RG-15 rain gauge (specialty item, order direct from Hydreon)

---

## Import Notes

Equipment travels with installer under humanitarian exemption. No shipping or customs duties apply.

### IMEI Registration

- Quectel modem IMEI must be registered with Indonesian telecom authority
- Process can take 1-2 days; plan for this during deployment
- Coordinate with local PMI staff

---

## Assembly Notes

### Pre-Deployment Preparation (US - Low Humidity Environment)

1. **Apply conformal coating** to all PCBs (Pi 5, Witty Pi 5, Pi-EzConnect)
   - Mask all connectors, GPIO pins, SD card slot
   - Apply thin, even coat of MG 422C silicone
   - Allow 24hr cure in <60% RH environment
   - Document which boards are coated

2. **Test compute stack** before coating
   - Verify Pi 5 boots, SSD recognized, modem connects
   - Test ORC software with PoE camera (verify RTSP capture via orc-capture)
   - Verify Witty Pi 5 scheduling works
   - Test WS2812B status LED (GPIO 18)

3. **Pre-configure software**
   - Install ORC, configure for single PoE camera
   - Set up Witty Pi 5 schedule (15-minute wake cycles)
   - Configure day/night capture settings in ORC
   - Test maintenance mode WiFi hotspot
   - Pre-load Indonesian SIM config (if known)

4. **Pre-configure PoE camera**
   - Set static IP address, set credentials
   - Use `camtool.py` to push streaming, image, and NTP config
   - Verify built-in IR LEDs activate in darkness

### Field Assembly (Indonesia)

1. **Mount components** inside enclosure
   - Pi 5 stack on standoffs (with coated PCBs)
   - Terminal blocks on enclosure wall or base
   - PoE injector (Velcro/Dual Lock mount)
   - Modem (Velcro/Dual Lock mount)
   - ~~Samsung FIT Plus~~ removed from build (UAS issue)

2. **Drill panel holes** in enclosure lid or side
   - 1× 10-12mm hole for LED light window
   - 1× 16mm hole for IP67 pushbutton
   - 1× 12mm hole for Proxicast antenna mount
   - Cable gland holes per gland sizes

3. **Wire power distribution**
   - 12V from solar controller to terminal blocks (via cable gland)
   - USB-C power to Pi 5 (via terminal block or direct)
   - 12V to PoE injector (power-cycled with Pi via Witty Pi or shared switched circuit)

4. **Connect peripherals**
   - Modem to Pi 5 via USB
   - ~~Samsung FIT Plus~~ removed from build (UAS issue)
   - Proxicast ANT-122-S02 cables to modem SMA ports (main + diversity)
   - Cat6 from PoE injector to camera (via cable gland)
   - Rain gauge serial TX/RX + 12V power to Pi-EzConnect UART terminals (via cable gland)
   - WS2812B and pushbutton wired to GPIO via Pi-EzConnect terminals

5. **Mount camera** on pole
   - Use stainless U-bolt clamps and pole mount bracket
   - Run Cat6 cable through conduit or direct with UV protection
   - Apply dielectric grease to outdoor RJ45 connections
   - Use IP68 waterproof coupler at camera connection

5. **System test**
   - Verify Pi boots and status LED indicates state
   - Test RTSP capture via orc-capture
   - Verify camera IR LEDs activate in darkness (cover lens to test)
   - Verify LTE connectivity (may need IMEI registration first)
   - Test rain gauge serial communication (RS232 TTL over Pi UART)
   - Test maintenance mode (button press)
   - Verify PoE injector powers off during Pi sleep cycle

6. **Seal enclosure**
   - Apply silicone sealant around cable glands
   - Verify all Gore vents are installed and not blocked
   - Close enclosure, ensure gasket seals properly
   - Do NOT add desiccant packs (defeats Gore vent strategy)

---

## Maintenance & Spares Strategy

### Consumables (Expect to Replace)

- MicroSD card: Every 6-12 months (write wear)
- Conformal coating: Reapply if PCB replaced
- Silicone sealant: Reapply annually if degraded

### Likely Failure Points

1. **SD card** - Most common failure (write wear)
2. **PoE camera** - Factory-sealed IP67, but outdoor exposure; spare available from 2-pack
3. **LTE antenna** - Mitigated by Proxicast ANT-122-S02 sealed puck (IP67); main risk is cable damage
4. **Cat6 cable** - UV degradation if conduit not used
5. **Cable glands** - Gasket degradation from UV/ozone

### Spare Parts (Keep at PMI Office)

See CLAUDE.md "Tools & Spares Inventory" section for comprehensive list. Key spares for Sukabumi:

- Raspberry Pi 5 (1× shared with Jakarta)
- Witty Pi 5 HAT+ (1× shared)
- MicroSD cards (2×, pre-imaged)
- ANNKE C1200 PoE camera (1× spare from 2-pack)
- Proxicast ANT-122-S02 antenna (1×, spare)
- Cat6 cable (spare length)
- IP68 RJ45 couplers (spare)
- Cable glands (3× each size)

---

## Troubleshooting Quick Reference

### System Won't Boot

1. Check solar battery voltage (should be >11.5V)
2. Check fuses (12V input, USB-C power)
3. Try known-good microSD card
4. Check LED indicators on Pi 5

### Camera Not Capturing

1. Verify Cat6 cable connection at camera and PoE injector
2. Check PoE injector status LEDs (verify 12V power to injector)
3. Verify camera has IP address (check DHCP or static config)
4. SSH into Pi, run `orc-capture --skip-relay --dry-run` to test RTSP capture
5. Check ORC logs: `/var/log/orc/`
6. Verify camera boots within the active cycle window (~60s boot time)

### Camera IR Not Working at Night

1. Block camera lens to simulate darkness (IR should activate automatically)
2. Verify camera IR LED settings in web interface (may be disabled)
3. Check ORC day/night configuration is set correctly
4. Verify camera has sufficient PoE power (check injector port LEDs)

### No LTE Connectivity

1. Verify SIM card installed and activated
2. Check Proxicast puck antenna SMA connections to modem (finger-tight)
3. Verify modem LED indicators
4. May require IMEI registration with Indonesian telecom
5. Check signal strength: `mmcli -m 0 --signal-get`

### High Humidity Condensation

1. Verify Gore vents are not blocked
2. Check conformal coating integrity (visual inspection)
3. Consider adding temporary ventilation during hottest part of day
4. **Do NOT add desiccant** (will saturate and make problem worse)

---

## Success Criteria

Deployment is successful when:

- [ ] System captures 5-second video every 15 minutes
- [ ] Videos upload successfully to ORC server
- [ ] IR illumination activates automatically at night
- [ ] Rain gauge data logs correctly
- [ ] LTE connectivity stable (registered with Indonesian network)
- [ ] Status LED indicates system health accurately
- [ ] Maintenance mode accessible via pushbutton
- [ ] Power consumption <120 Wh/day (verified with solar controller; see ISS-001 for corrected budget ~118 Wh/day)
- [ ] System runs for 7 days without intervention
- [ ] All enclosures properly sealed (no water ingress after rain)
- [ ] PMI staff trained on basic troubleshooting

---

## Revision History

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2026-04-05 | 2.6 | Samsung FIT Plus USB drive removed (UAS boot storm, known_issues.md #1); captures on SD card rootfs. Power target corrected from <50 to <120 Wh/day per ISS-001. Circuit diagram updated for Witty Pi 5 RTC and USB removal. | tjordan + Claude (Opus 4.6) |
| 2026-04-01 | 2.5 | Replaced 3x IP67 panel-mount LEDs (Red/Yellow/Green) + resistors + relay channels with single WS2812B NeoPixel on GPIO 18 (5V Pi rail). Saves $19.60, frees relay channels, config-driven via `/etc/orc/led-status.yaml`. See `docs/LED_STATUS_SPEC.md` | Claude (Opus 4.6) |
| 2026-01-30 | 2.4 | Replaced DFRobot SEN0575 tipping bucket rain gauge with Hydreon RG-15 solid-state optical rain gauge ($99 vs $48) — no moving parts, self-cleaning, RS232 3.3V TTL direct to Pi UART, ±10% accuracy; removed mount bracket and cable (built-in mounting, powered from 12V system) | Claude (Opus 4.5) |
| 2026-01-30 | 2.3 | Replaced M.2 SATA SSD + USB enclosure with Samsung FIT Plus 256GB USB flash drive — IP67, smaller, cheaper ($25 vs $65), no mounting needed | Claude (Opus 4.5) |
| 2026-01-30 | 2.2 | Switched to VEVOR carbon steel hinged enclosure (16×12×8") — hinged door for field access, includes mounting plate; saves $30 vs cast aluminum | Claude (Opus 4.5) |
| 2026-01-30 | 2.1 | Replaced dual-enclosure (inner+outer) with standalone 400×310×190mm cast aluminum enclosure; dropped DIN rail for standoff/Velcro mounting | Claude (Opus 4.5) |
| 2026-01-30 | 2.0 | Switched from USB camera + IR illuminator to PoE camera system (ANNKE C1200 + Planet IPOE-260-12V); removed Camera System and IR Illumination sections; power-cycled PoE with Pi | Claude (Opus 4.5) |
| 2026-01-30 | 1.6 | Changed antenna from Poynting PUCK-2 to Proxicast ANT-122-S02 (better availability, same model as Jakarta) | Claude (Opus 4.5) |
| 2026-01-30 | 1.5 | Replaced basic LTE antennas + bulkhead connectors with sealed MIMO puck antenna | Claude (Opus 4.5) |
| 2026-01-28 | 1.4 | Changed inner enclosure from polycarbonate to BestTong aluminum (thermal concern) | Claude (Opus 4.5) |
| 2026-01-22 | 1.3 | Dual-enclosure strategy: inner IP67 box inside existing aluminum box | Claude (Opus 4.5) |
| 2026-01-22 | 1.2 | Reuse existing aluminum enclosure; external panel-mount LEDs/button | Claude (Opus 4.5) |
| 2026-01-22 | 1.1 | Changed enclosure to opaque body + small window (thermal/greenhouse concern) | Claude (Opus 4.5) |
| 2026-01-09 | 1.0 | Initial BOM creation | Claude (comprehensive-researcher) |

---

## References

- `/spring_2026_ID/CLAUDE.md` - Component research and decisions
- Phase 1-5 research documents (internal mounting, GPIO stacking, humidity management, etc.)
- DESIGN_SPECS.md - Guiding principles and requirements
- SITES.md - Site profiles and equipment lists

---

## Contact Information

**Planet Technology (PoE Injector):**
- Website: planetechusa.com
- Product: IPOE-260-12V (native 12V input)
- Sales: sales@planetechusa.com

**UUGear (Witty Pi 5 HAT+):**
- Website: uugear.com
- Product: Witty Pi 5 HAT+

---

**END OF BOM**
