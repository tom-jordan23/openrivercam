# RC-Box Bill of Materials (Verified)

**Target:** Complete dual-camera unit with anti-fog
**Date:** 2025-11-29
**Revision:** 3 - LeMotech housing with integrated anti-fog system

---

## CRITICAL COMPATIBILITY NOTES

1. **Camera System Change:** The Arducam CSI-to-USB adapter (B0278) is **NOT compatible** with Camera Module 3 (IMX708). Must use Arducam's integrated USB cameras (B0304/B0305) which have IMX708 built-in.

2. **Global Modem:** Quectel EG25-G supports 15 LTE bands covering Americas, Europe, Asia-Pacific, and Africa. Regional variants (EC25-AF, EC25-E) do NOT provide global coverage.

3. **Power Management:** PiSugar 3 Plus is **NOT compatible** with Pi 5. Use Waveshare UPS HAT (B) instead.

---

## DigiKey/Mouser Order

| Qty | Part Number | Manufacturer | Description | Unit Price | Ext Price | Source |
|-----|-------------|--------------|-------------|------------|-----------|--------|
| 1 | SC1111 | Raspberry Pi | Raspberry Pi 5 4GB | $60.00 | $60.00 | DigiKey |
| 1 | EG25GGB-MINIPCIE | Quectel | LTE Cat 4 Modem **GLOBAL** (15 bands) | $78.93 | $78.93 | DigiKey |
| 6 | CG-PG9-2-BK | Essentra | PG9 Cable Gland IP68 4-8mm | $1.17 | $7.02 | DigiKey |
| 3 | VENT-PS1NGY-N8002 | Amphenol LTW | M12 Breather Vent IP69K | $8.50 | $25.50 | DigiKey |
| 4 | M2012SS1W01 | NKK Switches | SPST Toggle Switch IP67 | $12.50 | $50.00 | DigiKey |
| 1 | 26295 | Universal Solder | 1.3" OLED 128x64 I2C SSD1306 | $15.00 | $15.00 | DigiKey |
| 3 | 559-QS103XXR12 | Apem | 10mm LED 12V Red Panel Mount | $3.50 | $10.50 | Mouser |

**DigiKey/Mouser Subtotal: ~$247**

---

## Camera System (Arducam Integrated USB Cameras)

**NOTE:** These are complete USB UVC cameras with IMX708 sensor built-in. NOT CSI-to-USB adapters.

| Qty | Part Number | Manufacturer | Description | Unit Price | Ext Price | Source |
|-----|-------------|--------------|-------------|------------|-----------|--------|
| 2 | B0304 | Arducam | 12MP IMX708 USB UVC Camera (75° FOV) | $45.00 | $90.00 | Arducam |
| - | *or B0305* | Arducam | 12MP IMX708 USB UVC Camera (102° Wide) | $49.00 | $98.00 | Arducam |

**Camera Specs:**
- Sensor: Sony IMX708 (same as Pi Camera Module 3)
- Resolution: 4608×2592 (12MP stills), 1080p30 video
- Interface: USB 2.0 UVC (plug-and-play, no drivers)
- Output: MJPG and YUV
- Compatible: Windows, Linux, Mac, Android

**Arducam Camera Subtotal: ~$90-98**

---

## Specialty Electronics

| Qty | Part Number | Manufacturer | Description | Unit Price | Ext Price | Source |
|-----|-------------|--------------|-------------|------------|-----------|--------|
| 1 | 20567 | Waveshare | UPS HAT (B) for Pi 5, 5V/5A | $35.99 | $35.99 | Waveshare |
| 1 | - | Various | M.2 SATA 512GB SSD | $40.00 | $40.00 | Amazon |
| 1 | - | StarTech/Sabrent | M.2 SATA to USB 3.0 Enclosure | $15.00 | $15.00 | Amazon |
| 1 | - | Various | Mini PCIe to USB Adapter (for modem) | $25.00 | $25.00 | Amazon |
| 1 | - | Various | LTE Antenna (SMA, 700-2700MHz) | $10.00 | $10.00 | Amazon |

**Specialty Electronics Subtotal: ~$126**

---

## Camera Housing & Anti-Fog System

**Housing Solution:** LeMotech IP67 junction box with clear polycarbonate lid, modified with optical window for camera lens. Provides ample space for Arducam B0304 board (38x38mm) plus heater integration.

| Qty | Part Number | Manufacturer | Description | Unit Price | Ext Price | Source |
|-----|-------------|--------------|-------------|------------|-----------|--------|
| 2 | B0CZR9C9Y5 | LeMotech | IP67 Junction Box 120x90x68mm Clear Lid | $20.00 | $40.00 | Amazon |
| 2 | - | Keenovo | Silicone Heater 20x70mm 10W 12V | $20.00 | $40.00 | Keenovo/Amazon |
| 1 | STC-1000 | Elitech | Digital Thermostat 12V DC | $15.00 | $15.00 | Amazon |
| 2 | - | Generic | Clear Acrylic Disc 3" dia x 3mm | $5.00 | $10.00 | Amazon/TAP Plastics |
| 1 | - | Gorilla/Permatex | Clear Silicone Sealant | $8.00 | $8.00 | Amazon/Hardware |
| 1 | - | Various | Type 4A Molecular Sieve 1lb | $12.00 | $12.00 | Amazon |
| 2 | - | Various | Anti-fog Lens Coating (Cat Crap/RainX) | $4.00 | $8.00 | Amazon |

**Camera Housing/Anti-Fog Subtotal: ~$133**

### Housing Specifications (LeMotech)
- **External:** 120 x 90 x 68mm (4.7" x 3.5" x 2.7")
- **Internal:** ~110 x 80 x 58mm (fits 38x38mm board + heater)
- **IP Rating:** IP67 certified
- **Material:** ABS base, polycarbonate clear lid
- **Includes:** Mounting plate, wall brackets, cable glands
- **Modification:** Drill 30mm hole in front, seal acrylic window with silicone

### Anti-Fog System Design
Each camera housing includes:
1. **Active heating:** 10W silicone heater pad mounted near optical window
2. **Thermostat control:** STC-1000 activates heaters when temp drops below 25°C
3. **Pressure equalization:** Breather vent prevents moisture pumping (from main BOM)
4. **Desiccant backup:** Type 4A molecular sieve packet (replace every 6 months)
5. **Lens coating:** Anti-fog treatment on acrylic window

---

## Power System (Solar Configuration)

| Qty | Part Number | Manufacturer | Description | Unit Price | Ext Price | Source |
|-----|-------------|--------------|-------------|------------|-----------|--------|
| 1 | - | Ampere Time/Redodo | LiFePO4 12V 20Ah Battery | $89.00 | $89.00 | Amazon |
| 1 | - | Renogy/Newpowa | 50W 12V Mono Solar Panel | $55.00 | $55.00 | Amazon |
| 1 | - | EPEVER/PowMr | PWM 10A Solar Charge Controller | $15.00 | $15.00 | Amazon |

**Power System Subtotal: ~$159**

---

## Enclosure & Mounting

| Qty | Part Number | Manufacturer | Description | Unit Price | Ext Price | Source |
|-----|-------------|--------------|-------------|------------|-----------|--------|
| 1 | WQ-57 | Polycase | IP67 Enclosure 11.8"x9.1"x5.5" | $45.00 | $45.00 | Polycase |
| 2 | - | SmallRig/Generic | Ball Head Mount 1/4-20 | $12.00 | $24.00 | Amazon |
| 2 | - | Generic | USB 3.0 Cable 3m Shielded | $12.00 | $24.00 | Amazon |
| 4 | - | Generic | SS Hose Clamp 3-6" | $3.00 | $12.00 | Amazon |
| 1 | - | Various | Wire, connectors, standoffs | $15.00 | $15.00 | Various |

**Enclosure/Mounting Subtotal: ~$120**

---

## TOTAL COST SUMMARY

| Category | Cost |
|----------|------|
| DigiKey/Mouser | $247 |
| Arducam Cameras (2x B0304) | $90 |
| Specialty Electronics | $126 |
| Camera Housing/Anti-Fog | $133 |
| Power System (Solar) | $159 |
| Enclosure/Mounting | $120 |
| **TOTAL (Solar)** | **$875** |
| **TOTAL (Grid)** | **~$795** |

**Note:** Grid power configuration saves ~$80 (no solar panel/controller, smaller battery).

---

## Cost Reduction Options

To reduce costs:

| Change | Savings | Notes |
|--------|---------|-------|
| Use Pi 5 2GB instead of 4GB | -$15 | Minimal impact for this application |
| Smaller battery (12V 10Ah) | -$40 | ~1 day autonomy |
| 30W panel instead of 50W | -$20 | Marginal in cloudy weather |
| 256GB SSD instead of 512GB | -$15 | Still ~2 weeks storage |
| Single camera initially | -$45 | Add second camera later |

**Realistic reduced total: ~$720-780**

---

## Notes

### Critical Compatibility (VERIFIED)
1. **PiSugar 3 Plus is NOT compatible with Pi 5** - Use Waveshare UPS HAT (B) instead
2. **Arducam CSI-to-USB adapters (B0278) do NOT work with IMX708** - Use B0304/B0305 integrated USB cameras
3. **Quectel EG25-G provides global coverage** - 15 LTE bands vs regional EC25 variants

### Items NOT on DigiKey/Mouser
- Arducam B0304/B0305 USB cameras → Arducam direct or Amazon
- Waveshare UPS HAT (B) → Waveshare direct or Amazon
- LeMotech IP67 junction boxes → Amazon (ASIN: B0CZR9C9Y5)
- Keenovo heater pads → Keenovo direct or Amazon
- STC-1000 thermostat → Amazon
- Clear acrylic discs → Amazon or TAP Plastics
- LiFePO4 batteries → Amazon (Ampere Time, Redodo)
- Solar panels/controllers → Amazon/Renogy
- Polycase enclosures → Polycase direct

### Verified DigiKey Part Numbers
- SC1111 - Raspberry Pi 5 4GB
- EG25GGB-MINIPCIE - Quectel LTE modem (GLOBAL)
- CG-PG9-2-BK - Essentra cable gland
- VENT-PS1NGY-N8002 - Amphenol breather vent
- M2012SS1W01 - NKK IP67 toggle switch

### Assembly Notes for Volunteers

#### Pre-Deployment Prep (Do Before Shipping)

1. **Camera housing fabrication (LeMotech box):**
   - Mark center point on front face of housing
   - Drill 30mm hole using hole saw (for camera lens)
   - Sand edges smooth
   - Apply silicone sealant around hole perimeter
   - Press 3" acrylic disc over hole from inside
   - Let cure 24 hours
   - Test waterproofing: submerge empty housing 30 min, check for leaks
   - Install breather vent in side wall (drill + seal)

2. **Heater installation:**
   - Clean inside surface near optical window
   - Attach Keenovo heater pad with 3M adhesive (position 5-10mm from window)
   - Route heater wires through cable gland
   - Apply anti-fog coating to acrylic window (both sides)

#### On-Site Assembly

3. **Camera installation:**
   - Mount Arducam B0304 to internal mounting plate using M2.5 standoffs
   - Align lens with optical window
   - Route USB cable through cable gland, tighten seal
   - Add molecular sieve desiccant packet
   - Close and latch lid

4. **Thermostat wiring:**
   - 12V power → STC-1000 input
   - STC-1000 relay output → Both heater pads (parallel)
   - NTC sensor → Inside one camera housing (route through gland)
   - Set temperature threshold: 25°C (heater ON when temp < 25°C)

5. **Main enclosure:**
   - Mount Pi 5 + Waveshare UPS HAT on standoffs
   - Install switches, LEDs, display on panel
   - Route camera USB cables through glands
   - Connect modem via Mini PCIe to USB adapter
   - Connect solar/battery to charge controller
   - Connect 12V to STC-1000 for heater control

### Spare Parts Kit (Ship with Each Unit)
- 1x complete spare camera housing (pre-assembled)
- 1x spare Arducam B0304 camera
- 2x spare acrylic windows
- 1x tube silicone sealant
- 5x desiccant packets
- 2x spare cable glands
- 1x spare heater pad
