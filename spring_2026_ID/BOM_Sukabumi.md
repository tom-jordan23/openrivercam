# Bill of Materials - Sukabumi Site
## Indonesia River Monitoring Station Deployment

**Site:** Sukabumi, Indonesia (foothills)
**Power:** Solar (existing 200W panel / 50Ah battery - reused from failed unit)
**Camera:** Single USB camera with IR night vision
**Purpose:** Replacement of failed river monitoring unit
**Date:** January 9, 2026
**Budget Target:** <$1,500 USD (half of $3,000 total for both sites)

---

## Design Approach

**Humidity Protection Strategy:**
- Silicone conformal coating (MG 422C) on all PCBs
- Gore M12 vents for pressure equalization
- NO PTC heaters (solar power budget constraint)
- NO desiccant (ineffective at 95% RH with vents)
- Accept higher failure risk; budget includes spare parts

**Key Principles:**
- Commodity electronics only (no custom PCBs)
- No soldering or cable cutting (screw terminals only)
- Field serviceable by semi-technical personnel
- All connections via plug-in or screw terminals

---

## Component Categories

1. [Compute Platform](#1-compute-platform)
2. [Camera System](#2-camera-system)
3. [IR Illumination](#3-ir-illumination)
4. [User Interface](#4-user-interface)
5. [Humidity Protection](#5-humidity-protection)
6. [Enclosure & Mounting](#6-enclosure--mounting)
7. [Rain Gauge](#7-rain-gauge)
8. [Cables & Connectors](#8-cables--connectors)
9. [Hardware & Fasteners](#9-hardware--fasteners)

---

## 1. Compute Platform

| Item | Description | Qty | Unit Price | Ext. Price | Source | Notes |
|------|-------------|-----|------------|------------|--------|-------|
| **RPi5-8GB** | Raspberry Pi 5, 8GB RAM | 1 | $80.00 | $80.00 | Adafruit, CanaKit | MSRP, verify availability |
| **WittyPi5** | Witty Pi 5 HAT+ (power mgmt, RTC, I2C-only) | 1 | $46.00 | $46.00 | UUGear | Per CLAUDE.md research |
| **EZCONNECT** | Adafruit Pi-EzConnect (ID 2711, GPIO terminal block) | 1 | $19.95 | $19.95 | Adafruit | Stacks on Witty Pi 5 HAT+ |
| **SSD-M2** | M.2 SATA SSD 512GB (ORICO or TEAMGROUP) | 1 | $50.00 | $50.00 | Amazon | Budget option (~$40-85 range) |
| **SSD-ENC** | USB 3.0 to M.2 SATA enclosure | 1 | $15.00 | $15.00 | Amazon | Tool-free, aluminum preferred |
| **MODEM** | Quectel EG25-G LTE Cat 4 module | 1 | $35.00 | $35.00 | AliExpress, Mouser | Verify Indonesian bands |
| **MODEM-USB** | PU201 USB adapter board for EG25-G | 1 | $15.00 | $15.00 | AliExpress | USB interface for modem |
| **ANT-LTE** | 4G LTE antenna (SMA male, 3-5dBi) | 2 | $8.00 | $16.00 | Amazon | Main + diversity |
| **ANT-BULK** | SMA bulkhead connector (female-female) | 2 | $4.00 | $8.00 | Amazon, DigiKey | Panel mount for antennas |
| **SD-CARD** | MicroSD card 32GB (SanDisk/Samsung) | 1 | $8.00 | $8.00 | Amazon | For OS boot |
| **HEATSINK** | Heatsink for Raspberry Pi 5 | 1 | $8.00 | $8.00 | Included or Amazon | Active or passive |
| **USB-RS485** | USB to RS485 converter (FTDI chip) | 1 | $18.00 | $18.00 | Amazon, DigiKey | For Modbus devices |
| | | | **Subtotal** | **$318.95** | | |

**Notes:**
- Pi 5 8GB preferred for ORC (4GB minimum would save ~$15)
- Quectel EG25-G confirmed compatible with Telkomsel (B1/B3/B5/B8/B40)
- SSD provides storage for ~2 weeks of video at 5s/15min capture rate
- Witty Pi 5 HAT+ provides scheduling, RTC, and low-power sleep
- Pi-EzConnect enables future sensor expansion via screw terminals

---

## 2. Camera System

| Item | Description | Qty | Unit Price | Ext. Price | Source | Notes |
|------|-------------|-----|------------|------------|--------|-------|
| **CAM-USB** | Custom 8MP IMX179 NoIR USB camera (ELP/SVPRO) | 1 | $85.00 | $85.00 | ELP (sales@elpcctv.com) | **LONG LEAD TIME: Order now for March/April delivery** |
| **CAM-HOUSING** | VA Imaging MVEC167 aluminum camera housing | 1 | $125.00 | $125.00 | VA Imaging | Aluminum for heat dissipation |
| **VENT-CAM** | Gore M12 protective vent (screw-in) | 1 | $12.00 | $12.00 | DigiKey, Mouser | Pressure equalization |
| **USB-CABLE** | Bulgin PX0840 IP67 USB cable (2-3m) | 1 | $45.00 | $45.00 | DigiKey, Newark | Or HDPE conduit option |
| | | | **Subtotal** | **$267.00** | | |

**Notes:**
- **CRITICAL ACTION:** Contact ELP/SVPRO NOW - custom NoIR orders take 2-6 weeks
- Request: 8MP IMX179 sensor WITHOUT IR-cut filter, 115°+ wide angle lens
- Alternative budget option: Standard USB in HDPE conduit through sealed gland (~$50 total)
- VA Imaging aluminum housing preferred over plastic (Entaniya) for tropical heat
- Gore vent essential for pressure equalization; prevents seal stress from temperature swings

---

## 3. IR Illumination

| Item | Description | Qty | Unit Price | Ext. Price | Source | Notes |
|------|-------------|-----|------------|------------|--------|-------|
| **IR-LIGHT** | Tendelux AI4 850nm IR illuminator (built-in photocell) | 1 | $35.00 | $35.00 | Amazon | Day/night sensing integrated |
| **RELAY-USB** | Numato Lab 1-channel USB relay module | 1 | $32.00 | $32.00 | Numato Lab, Amazon | Powers on with Pi boot |
| **PWR-12V** | 12V power cable with screw terminals (18AWG, 2m) | 1 | $8.00 | $8.00 | Amazon | From solar controller to relay |
| **FUSE-INLINE** | Inline fuse holder with 5A fuse (12V) | 1 | $6.00 | $6.00 | Amazon | Protection for IR circuit |
| | | | **Subtotal** | **$81.00** | | |

**Notes:**
- Tendelux AI4 includes photocell - only illuminates at night automatically
- Numato relay controlled by systemd service on Pi boot (closes circuit when Pi powered)
- All screw terminal connections - NO soldering or cable cutting required
- IR light powered from existing solar battery (minimal impact: ~15W × 8hr/night = 120Wh/day)
- Total IR duty cycle: ~8hr night × 13% (Pi active time) = ~1hr/night actual runtime

---

## 4. User Interface

| Item | Description | Qty | Unit Price | Ext. Price | Source | Notes |
|------|-------------|-----|------------|------------|--------|-------|
| **LED-RED** | 10mm IP67 panel-mount LED, Red | 1 | $6.00 | $6.00 | DigiKey, Mouser | Error indication |
| **LED-YEL** | 10mm IP67 panel-mount LED, Yellow | 1 | $6.00 | $6.00 | DigiKey, Mouser | Working (capture/upload) |
| **LED-GRN** | 10mm IP67 panel-mount LED, Green | 1 | $6.00 | $6.00 | DigiKey, Mouser | OK/Ready status |
| **BTN-MAINT** | IP67 momentary pushbutton (C&K AP or E-Switch PVA6) | 1 | $12.00 | $12.00 | DigiKey, Mouser | Maintenance mode input |
| **GLAND-BTN** | PG9 cable gland for button wiring | 1 | $3.00 | $3.00 | Amazon, DigiKey | 16mm panel hole |
| **RESISTOR** | Current-limiting resistors for LEDs (assorted) | 1 | $5.00 | $5.00 | Amazon, DigiKey | 220-470Ω range |
| | | | **Subtotal** | **$38.00** | | |

**Notes:**
- LEDs controlled via Pi-EzConnect GPIO screw terminals
- Button: Short press = show status, Long press (3s) = enter maintenance mode
- Maintenance mode: prevents auto-shutdown, starts WiFi hotspot, enables SSH
- LEDs visible at 3-5m distance, excellent sunlight readability (no display power needed)
- Recessed button mounting prevents accidental activation

---

## 5. Humidity Protection

| Item | Description | Qty | Unit Price | Ext. Price | Source | Notes |
|------|-------------|-----|------------|------------|--------|-------|
| **COAT-SIL** | MG Chemicals 422C silicone conformal coat (55ml) | 1 | $22.00 | $22.00 | DigiKey, Amazon | For 95%+ RH environments |
| **BRUSH** | Application brush (acid brush or fine bristle) | 2 | $2.00 | $4.00 | Hardware store | Clean, lint-free |
| **MASK-TAPE** | Masking tape (low-tack, 1" width) | 1 | $4.00 | $4.00 | Hardware store | Protect connectors during coating |
| **VENT-ENC** | Gore M12 protective vent (compute enclosure) | 2 | $12.00 | $24.00 | DigiKey, Mouser | 2× for larger enclosure |
| **IPA-WIPES** | Isopropyl alcohol wipes (99%) | 1 | $8.00 | $8.00 | Amazon | Pre-coating cleaning |
| | | | **Subtotal** | **$62.00** | | |

**Notes:**
- Apply conformal coating to: Raspberry Pi 5, Witty Pi 5 HAT+, Pi-EzConnect, relay module
- MASK: All connectors (USB, HDMI, GPIO pins, SD card slot), heat sink contact areas
- Apply in low-humidity environment (ideally <60% RH), allow 24hr cure before assembly
- Gore vents provide pressure equalization without active humidity control
- NO PTC heaters due to solar power budget constraint
- NO desiccant (ineffective at 95% RH with vents per research)

---

## 6. Enclosure & Mounting

| Item | Description | Qty | Unit Price | Ext. Price | Source | Notes |
|------|-------------|-----|------------|------------|--------|-------|
| **ENC-COMPUTE** | Outdoor enclosure (300×200×150mm, polycarbonate) | 1 | $45.00 | $45.00 | Amazon | IP65+ rated, clear lid option |
| **DIN-RAIL** | DIN rail 35mm × 300mm (aluminum) | 1 | $8.00 | $8.00 | Amazon, DigiKey | Internal mounting |
| **CLIP-RPI** | DIN rail clip for Raspberry Pi | 1 | $6.00 | $6.00 | Amazon | Specific to Pi 5 form factor |
| **CLIP-TERM** | DIN rail terminal block clips | 4 | $2.00 | $8.00 | Amazon, DigiKey | For various components |
| **TERM-BLOCK** | Screw terminal blocks (2-12 position, assorted) | 1 | $15.00 | $15.00 | Amazon, DigiKey | Power distribution |
| **GLAND-M12** | M12 cable gland (IP68) | 4 | $3.00 | $12.00 | Amazon | Camera, antenna, power |
| **GLAND-M16** | M16 cable gland (IP68) | 2 | $3.50 | $7.00 | Amazon | USB cable, larger runs |
| **GLAND-M20** | M20 cable gland (IP68) | 1 | $4.00 | $4.00 | Amazon | AC power inlet (if needed) |
| **VELCRO-LOCK** | 3M Dual Lock reclosable fastener (25mm × 1m) | 1 | $12.00 | $12.00 | Amazon | For SSD, modem mounting |
| **STANDOFFS** | M2.5/M3 standoff kit (brass or nylon) | 1 | $12.00 | $12.00 | Amazon | Backup mounting option |
| | | | **Subtotal** | **$129.00** | | |

**Notes:**
- DIN rail provides secure, vibration-resistant mounting (per internal mounting research)
- Enclosure size accommodates: Pi stack, SSD, modem, relay, terminal blocks
- Clear or windowed lid enables LED visibility without opening enclosure
- Velcro/Dual Lock for items without mounting holes (SSD, modem USB adapter)
- Consider mounting within or adjacent to existing solar controller enclosure

---

## 7. Rain Gauge

| Item | Description | Qty | Unit Price | Ext. Price | Source | Notes |
|------|-------------|-----|------------|------------|--------|-------|
| **RAIN-GAUGE** | DFRobot SEN0575 I2C tipping bucket rain gauge | 1 | $30.00 | $30.00 | DFRobot, DigiKey | Python libraries included |
| **MOUNT-RG** | Mounting bracket for rain gauge (stainless steel) | 1 | $8.00 | $8.00 | Amazon | Or fabricate from included hardware |
| **CABLE-RG** | 2-conductor shielded cable (22AWG, 5m) | 1 | $10.00 | $10.00 | Amazon | I2C connection to Pi |
| | | | **Subtotal** | **$48.00** | | |

**Notes:**
- Alternative: Misol WH-SP-RG (~$20, simple pulse output to GPIO)
- DFRobot SEN0575 provides I2C interface, easier software integration
- Resolution: 0.2-0.3mm per tip (adequate for flood monitoring)
- Connect via Pi-EzConnect I2C screw terminals
- Mount in open area away from structures (>2m from walls/trees)

---

## 8. Cables & Connectors

| Item | Description | Qty | Unit Price | Ext. Price | Source | Notes |
|------|-------------|-----|------------|------------|--------|-------|
| **USB-C-PWR** | USB-C power cable (1.5m, right-angle) | 1 | $8.00 | $8.00 | Amazon | Pi 5 power from solar controller |
| **USB-A-SHORT** | USB-A cables (0.5m, various) | 3 | $4.00 | $12.00 | Amazon | Modem, relay, short runs |
| **HDPE-CONDUIT** | HDPE flexible conduit (20mm × 5m) | 1 | $15.00 | $15.00 | Hardware store | Cable protection (if not using Bulgin) |
| **HEAT-SHRINK** | Heat shrink tubing kit (assorted sizes) | 1 | $10.00 | $10.00 | Amazon | Cable sealing, strain relief |
| **CABLE-TIES** | UV-resistant cable ties (assorted, 100pc) | 1 | $8.00 | $8.00 | Amazon | Cable management |
| **WIRE-18AWG** | 18AWG stranded wire (red/black, 10m each) | 1 | $15.00 | $15.00 | Amazon | Power distribution |
| **FERRULES** | Wire ferrules (assorted, crimper kit) | 1 | $18.00 | $18.00 | Amazon | Professional terminal connections |
| | | | **Subtotal** | **$86.00** | | |

**Notes:**
- Right-angle USB-C connector reduces strain on Pi 5 power port
- Ferrules recommended for all screw terminal connections (prevents wire fraying)
- UV-resistant cable ties essential for outdoor tropical environment
- HDPE conduit provides budget alternative to IP67-rated cable runs

---

## 9. Hardware & Fasteners

| Item | Description | Qty | Unit Price | Ext. Price | Source | Notes |
|------|-------------|-----|------------|------------|--------|-------|
| **SS-SCREWS** | Stainless steel screw assortment (M3, M4, M5) | 1 | $15.00 | $15.00 | Amazon | 304/316 grade for corrosion resistance |
| **SS-NUTS** | Stainless steel nut assortment (M3, M4, M5) | 1 | $10.00 | $10.00 | Amazon | Nyloc and standard |
| **SS-WASHERS** | Stainless steel washer assortment | 1 | $8.00 | $8.00 | Amazon | Flat and split lock |
| **POLE-CLAMP** | Stainless U-bolt clamp (for pole mounting, 60mm) | 2 | $8.00 | $16.00 | Amazon | Camera housing mount |
| **SEALANT** | Silicone sealant (outdoor, clear) | 1 | $6.00 | $6.00 | Hardware store | Cable gland sealing |
| **DI-GREASE** | Dielectric grease (small tube) | 1 | $8.00 | $8.00 | Amazon | Connector protection |
| **DESICCANT** | Silica gel packets (for initial assembly only) | 1 | $6.00 | $6.00 | Amazon | Not for field maintenance |
| | | | **Subtotal** | **$69.00** | | |

**Notes:**
- Use stainless steel 304 minimum (316 preferred for coastal areas)
- Apply dielectric grease to all outdoor connectors (SMA, power terminals)
- Desiccant included for initial assembly in controlled environment only
- Do NOT plan to replace desiccant in field (defeats Gore vent strategy)

---

## TOTAL BOM COST SUMMARY

| Category | Subtotal |
|----------|----------|
| 1. Compute Platform | $318.95 |
| 2. Camera System | $267.00 |
| 3. IR Illumination | $81.00 |
| 4. User Interface | $38.00 |
| 5. Humidity Protection | $62.00 |
| 6. Enclosure & Mounting | $129.00 |
| 7. Rain Gauge | $48.00 |
| 8. Cables & Connectors | $86.00 |
| 9. Hardware & Fasteners | $69.00 |
| **SUBTOTAL (Materials)** | **$1,098.95** |
| Shipping & Handling (est. 10%) | $110.00 |
| Customs/Import Duties (est. 5%) | $55.00 |
| Contingency (10%) | $110.00 |
| **TOTAL ESTIMATED COST** | **$1,373.95** |

**Budget Status:** ✅ Within $1,500 target for Sukabumi site
**Remaining Budget (of $3,000 total):** ~$1,626 for Jakarta site + shared spares

---

## Power Budget Analysis

### Solar System (Existing)
- Solar panel: 200W
- Battery: 12V 50Ah = 600Wh capacity
- Usable capacity (50% DoD): 300Wh/day

### Daily Power Consumption Estimate

**Active Phase (15-minute cycle, 96 cycles/day):**
| Component | Power | Duration/Cycle | Energy/Cycle | Daily (96 cycles) |
|-----------|-------|----------------|--------------|-------------------|
| Raspberry Pi 5 (active) | 8W | 90s | 0.20 Wh | 19.2 Wh |
| SSD | 2W | 90s | 0.05 Wh | 4.8 Wh |
| USB Camera | 2.5W | 5s | 0.003 Wh | 0.3 Wh |
| LTE Modem (upload) | 3W | 30s | 0.025 Wh | 2.4 Wh |
| Witty Pi 5 (active) | 0.5W | 90s | 0.0125 Wh | 1.2 Wh |
| **Active subtotal** | | | | **27.9 Wh/day** |

**Sleep Phase:**
| Component | Power | Duration | Daily Energy |
|-----------|-------|----------|--------------|
| Witty Pi 5 (sleep) | 0.025W | 22.5 hr | 0.56 Wh |
| LTE Modem (standby) | 0.1W | 24 hr | 2.4 Wh |
| **Sleep subtotal** | | | **2.96 Wh/day** |

**IR Illumination (nighttime only):**
| Component | Power | Duration | Daily Energy |
|-----------|-------|----------|--------------|
| IR Light (Tendelux AI4) | 15W | ~1 hr (actual runtime) | 15 Wh |
| Relay (closed) | 0.5W | ~1 hr | 0.5 Wh |
| **IR subtotal** | | | **15.5 Wh/day** |

**LED Status Indicators:**
| Component | Power | Duration | Daily Energy |
|-----------|-------|----------|--------------|
| 1× LED (average) | 0.02W | 24 hr | 0.48 Wh |

**TOTAL DAILY CONSUMPTION:** ~46.8 Wh/day

**Solar Generation (Sukabumi - foothills, decent sun):**
- 200W panel × 4.5 peak sun hours × 0.8 efficiency = ~720 Wh/day
- **Margin:** 720 Wh generation - 47 Wh consumption = **673 Wh surplus**

**Battery Runtime (no sun):**
- 300 Wh usable ÷ 47 Wh/day = **6.4 days autonomy**

**Status:** ✅ Excellent power budget margin. System can run indefinitely on existing solar setup.

---

## Critical Path Items (Long Lead Times)

### URGENT - Order Immediately for March/April Deployment

| Item | Lead Time | Action Required |
|------|-----------|-----------------|
| **Custom USB Camera (ELP/SVPRO)** | 2-6 weeks | Contact sales@elpcctv.com NOW. Specify: 8MP IMX179 NoIR (no IR-cut filter), 115°+ wide angle lens, USB interface |
| **VA Imaging MVEC167 Housing** | 2-4 weeks | Contact VA Imaging for quote/availability |
| **Witty Pi 5 HAT+** | 1-2 weeks | Order from UUGear (stock availability varies) |
| **Quectel EG25-G + PU201** | 2-4 weeks | AliExpress or Mouser (verify stock) |

### Standard Lead Time (1-2 weeks)

All other components available from Amazon, DigiKey, Mouser with standard shipping.

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
- Custom USB camera (already international shipping)
- Conformal coating (specific product required)
- Quality LTE antennas (counterfeit risk locally)
- Numato USB relay (specialty item)
- Tendelux IR illuminator (quality/warranty)

---

## Customs & Import Considerations

### Documentation Required

| Document | Purpose |
|----------|---------|
| Commercial invoice | Detailed item list with values |
| Packing list | Box contents, weights |
| Equipment manifest | Serial numbers (Pi, modem IMEI) |
| PMI letter of introduction | Humanitarian/research purpose |

### Estimated Import Duties (Indonesia)

- Electronics: 0-10% depending on classification
- Cameras: 0-5% (professional equipment)
- Batteries: May have restrictions (verify current regulations)
- **Strategy:** Declare as "professional monitoring equipment for humanitarian installation"

### Customs Value Declaration

- Use actual purchase prices (not retail)
- Include BOM spreadsheet as supporting documentation
- Highlight non-commercial nature (replacement of failed unit)

### IMEI Registration

- Quectel modem IMEI must be registered with Indonesian telecom authority
- Process can take 1-2 days; plan for this during deployment
- Coordinate with local PMI staff

---

## Assembly Notes

### Pre-Deployment Preparation (US - Low Humidity Environment)

1. **Apply conformal coating** to all PCBs (Pi 5, Witty Pi 5, Pi-EzConnect, relay)
   - Mask all connectors, GPIO pins, SD card slot
   - Apply thin, even coat of MG 422C silicone
   - Allow 24hr cure in <60% RH environment
   - Document which boards are coated

2. **Test compute stack** before coating
   - Verify Pi 5 boots, SSD recognized, modem connects
   - Test ORC software with USB camera
   - Verify Witty Pi 5 scheduling works
   - Test GPIO control of LEDs and relay

3. **Pre-configure software**
   - Install ORC, configure for single camera
   - Set up Witty Pi 5 schedule (15-minute wake cycles)
   - Configure IR relay control service
   - Test maintenance mode WiFi hotspot
   - Pre-load Indonesian SIM config (if known)

4. **Assemble camera module** (if possible in controlled environment)
   - Install USB camera in VA Imaging housing with Gore vent
   - Include small silica gel packet (one-time, for shipping)
   - Seal and test before shipping

### Field Assembly (Indonesia)

1. **Mount components to DIN rail** inside enclosure
   - Pi 5 stack (with coated PCBs)
   - Terminal blocks
   - Relay module
   - SSD (Velcro mount)
   - Modem (Velcro mount)

2. **Wire power distribution**
   - 12V from solar controller to terminal blocks
   - USB-C power to Pi 5 (via terminal block or direct)
   - 12V to IR relay circuit with inline fuse

3. **Connect peripherals**
   - USB camera, modem, relay, SSD to Pi 5
   - LTE antennas through bulkhead connectors
   - Rain gauge I2C to Pi-EzConnect terminals
   - LEDs to GPIO via Pi-EzConnect terminals
   - Pushbutton to GPIO via Pi-EzConnect terminals

4. **Mount camera and IR illuminator** on pole
   - Use stainless U-bolt clamps
   - Run USB cable through conduit or use IP67 cable
   - Mount Tendelux IR adjacent to camera
   - Apply dielectric grease to all outdoor connectors

5. **System test**
   - Verify Pi boots and LEDs indicate status
   - Test camera capture
   - Test IR illumination (cover photocell to simulate darkness)
   - Verify LTE connectivity (may need IMEI registration first)
   - Test rain gauge pulse counting
   - Test maintenance mode (button press)

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
2. **USB camera** - High humidity exposure
3. **LTE antennas** - UV degradation, connector corrosion
4. **Cable glands** - Gasket degradation from UV/ozone

### Spare Parts (Keep at PMI Office)

See CLAUDE.md "Tools & Spares Inventory" section for comprehensive list. Key spares for Sukabumi:

- Raspberry Pi 5 (1× shared with Jakarta)
- Witty Pi 5 HAT+ (1× shared)
- MicroSD cards (2×, pre-imaged)
- USB camera (1×, same model)
- LTE antennas (2×)
- Inline fuses (5×, various amperage)
- Cable glands (3× each size)
- USB cables (2×)

---

## Troubleshooting Quick Reference

### System Won't Boot

1. Check solar battery voltage (should be >11.5V)
2. Check fuses (12V input, USB-C power)
3. Try known-good microSD card
4. Check LED indicators on Pi 5

### Camera Not Capturing

1. Verify USB cable connection
2. Check camera power LED (if equipped)
3. SSH into Pi, run `lsusb` to verify camera detected
4. Check ORC logs: `/var/log/orc/`
5. Test with `ffmpeg` or `v4l2-ctl --list-devices`

### IR Not Illuminating

1. Cover Tendelux photocell (should turn on in "night" mode)
2. Check 12V power at IR light terminals
3. Verify relay clicks when Pi boots (listen for audible click)
4. Check fuse in IR circuit
5. Test relay with multimeter (continuity when Pi powered)

### No LTE Connectivity

1. Verify SIM card installed and activated
2. Check antenna connections (finger-tight on SMA)
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
- [ ] Status LEDs indicate system health accurately
- [ ] Maintenance mode accessible via pushbutton
- [ ] Power consumption <50 Wh/day (verified with solar controller)
- [ ] System runs for 7 days without intervention
- [ ] All enclosures properly sealed (no water ingress after rain)
- [ ] PMI staff trained on basic troubleshooting

---

## Revision History

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2026-01-09 | 1.0 | Initial BOM creation | Claude (comprehensive-researcher) |

---

## References

- `/spring_2026_ID/CLAUDE.md` - Component research and decisions
- Phase 1-5 research documents (internal mounting, GPIO stacking, humidity management, etc.)
- DESIGN_SPECS.md - Guiding principles and requirements
- SITES.md - Site profiles and equipment lists

---

## Contact Information

**ELP Camera (Custom USB NoIR):**
- Email: sales@elpcctv.com
- Request: 8MP IMX179 NoIR, 115°+ wide angle, USB interface

**VA Imaging (Camera Housing):**
- Product: MVEC167 aluminum housing
- Verify M12 vent compatibility

**UUGear (Witty Pi 5 HAT+):**
- Website: uugear.com
- Product: Witty Pi 5 HAT+

**Numato Lab (USB Relay):**
- Website: numato.com
- Product: 1-channel USB relay module

---

**END OF BOM**
