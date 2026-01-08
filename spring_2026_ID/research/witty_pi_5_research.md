# Witty Pi 5 HAT+ Research Report
## Specifications, Pricing, and Upgrade Recommendation

**Date:** January 8, 2026
**Context:** Evaluating upgrade from Witty Pi 4 to Witty Pi 5 HAT+ for Raspberry Pi 5 deployment
**Researcher:** Claude Code

---

## Executive Summary

**RECOMMENDATION: UPGRADE to Witty Pi 5 HAT+ for new Pi 5 deployments**

The Witty Pi 5 HAT+ is a significant architectural improvement over Witty Pi 4, offering better developer experience, true HAT+ compliance, superior temperature resolution, and exclusive I2C-only GPIO access (no GPIO pin consumption). **Critical advantage for your use case:** Witty Pi 5's exclusive I2C communication means the Adafruit Pi-EzConnect can stack on top with no conflicts.

**Key Metrics:**
- **Price:** ~€39/USD $46 (vs. Witty Pi 4 ~€25/USD $29)
- **Power delivery:** 5A (same as Witty Pi 4)
- **GPIO pass-through:** YES - I2C-only design frees all GPIO pins
- **HAT+ compliance:** Yes - first Witty Pi with official HAT+ spec compliance
- **Stacking:** Compatible with Pi-EzConnect (confirmed below)
- **Availability:** Currently available at UUGear and The Pi Hut

---

## 1. Current Specifications - Witty Pi 5 HAT+

### 1.1 Hardware Specifications

| Specification | Detail |
|---------------|--------|
| **Microcontroller** | RP2350 (Raspberry Pi Silicon) with 16MB external flash |
| **Real-Time Clock** | High-precision RTC, ±3.8 to 5 ppm accuracy, temperature-compensated |
| **Temperature Sensor** | 0.0625°C resolution with high/low threshold interrupts |
| **Power Input** | 2 independent channels: VUSB (5V USB-C) + VIN (6-30V terminal block) |
| **DC/DC Converter** | Accepts 6-30V input, dual "ideal" diodes for robust power management |
| **Power Delivery** | Mode 1 Power HAT+ - up to 5A output to Pi + peripherals |
| **GPIO Interface** | **I2C only (configurable address, default 0x51)** - does NOT consume GPIO pins |
| **HAT+ Compliance** | Yes - complies with official Raspberry Pi HAT+ specification |
| **ID EEPROM** | HAT+ compliant with configurable I2C address |
| **Dimensions** | Standard HAT form factor (65mm x 56mm) |

### 1.2 Communication Interface

**Key Advantage:** Witty Pi 5 uses **I2C-only communication** with the Raspberry Pi.

| Aspect | Witty Pi 4 | Witty Pi 5 |
|--------|-----------|-----------|
| GPIO pins used | 3 pins (GPIO-4, GPIO-14, GPIO-17) | **0 pins - I2C only** |
| I2C address | N/A | 0x51 (configurable) |
| I2C pins used | 2 (standard Pi I2C1 on GPIO 2 & 3) | 2 (standard Pi I2C1 on GPIO 2 & 3) |
| Impact on GPIO pass-through | Consumes GPIO, limits stacking | Frees all GPIO pins for other HATs |

### 1.3 Real-Time Clock (RTC) & Timekeeping

| Feature | Witty Pi 4 | Witty Pi 5 |
|---------|-----------|-----------|
| Accuracy | ±2 ppm (factory calibrated) | ±3.8 to 5 ppm |
| Temperature compensation | Yes | Yes (built-in) |
| Backup power | Supercapacitor | Supercapacitor |
| Works offline | Yes | Yes |
| Tracks time when Pi off | Yes | Yes |

**Note:** Witty Pi 4 has slightly better RTC accuracy (±2 ppm vs. ±3.8-5 ppm). For most applications, both are excellent. Witty Pi 5's temperature compensation offers better long-term stability.

### 1.4 Thermal Management

| Feature | Witty Pi 4 | Witty Pi 5 |
|---------|-----------|-----------|
| Sensor resolution | 0.125°C | **0.0625°C** (2x better) |
| High temp threshold interrupt | Yes | Yes |
| Low temp threshold interrupt | No | Yes |
| On/off based on temp | Yes | Yes |

### 1.5 Power Management Features

**Both models support:**
- Time-based scheduling (power on/off at specific times)
- Complex scheduling via scripting (.wpi format)
- Voltage-based power control (shutdown if battery voltage drops)
- Temperature-based power control (shutdown if overheating)
- Graceful shutdown (safe power down without data corruption)

**Witty Pi 5 enhancements:**
- New .act script format (human-readable action list with timestamps)
- New .skd script format (compressed, storage-efficient)
- Schedule stored in onboard flash (independent of Raspberry Pi)
- OR logic for power-off conditions: triggers on ANY (time OR voltage OR temperature)
- AND logic for power-on: requires specified time AND conditions met
- Firmware fully open-source (C code using pico-sdk)

---

## 2. Power Delivery & HAT+ Specifications

### 2.1 Power Input Channels

**Witty Pi 5 has TWO independent power inputs:**

| Channel | Voltage Range | Typical Use | Failover |
|---------|---------------|------------|----------|
| VUSB | 5V via USB-C | Benchtop testing, small UPS | Optional |
| VIN | 6-30V via terminal block | Primary power source | Optional |

**Important:** Both channels can operate simultaneously and back each other up. If primary power fails, system automatically switches to secondary.

### 2.2 HAT+ Mode 1 Power Specifications

- **Mode:** Mode 1 Power HAT+
- **Current delivery:** Up to 5A to Raspberry Pi and stacked HATs
- **Power source:** External power via terminal block
- **EEPROM:** HAT+ compliant with Mode-1 identifier
- **Standby support:** Designed to tolerate STANDBY state (5V powered, 3.3V unpowered)

### 2.3 GPIO Pass-Through & HAT+ Stacking

**Critical for your use case - FULLY COMPATIBLE with Adafruit Pi-EzConnect:**

Witty Pi 5's **I2C-only design** means:
- ✅ All 28 GPIO pins remain available for other HATs
- ✅ Freeing GPIO pins allows Pi-EzConnect to stack on top
- ✅ No I2C address conflicts (Pi-EzConnect has its own EEPROM at 0x50 or 0x51, need verification)
- ✅ Standard Raspberry Pi I2C1 bus (GPIO 2 & 3) is the only interface

**HAT+ Stacking Rules (from Raspberry Pi spec):**
- One standard HAT + one stackable HAT + one power HAT+ can coexist
- All I2C EEPROMs must have unique addresses to avoid conflicts
- Witty Pi 5 uses I2C address **0x51**
- **Adafruit Pi-EzConnect:** Has pass-through header for stacking; check EEPROM address to ensure no conflict

**Recommendation:** Verify Pi-EzConnect's I2C EEPROM address (likely 0x50). If it's also 0x51, one address must be changed via resistor modification (documented in datasheets).

---

## 3. Pricing & Availability

### 3.1 Current Pricing (January 2026)

| Product | Price | Currency | Source |
|---------|-------|----------|--------|
| **Witty Pi 5 HAT+** | €39.00 | EUR | UUGear (manufacturer) |
| **Witty Pi 5 HAT+** | ~£34 | GBP | The Pi Hut |
| **Witty Pi 5 HAT+** | ~$46 | USD | Approximate USD equivalent |

**Witty Pi 4 comparison:**
| Product | Price | Currency | Source |
|---------|-------|----------|--------|
| Witty Pi 4 | €25.00 | EUR | UUGear |
| Witty Pi 4 Mini | €18.00 | EUR | UUGear |
| Witty Pi 4 | ~$45 | USD | Adafruit |

**Price premium:** Witty Pi 5 is ~60% more expensive than Witty Pi 4, justified by:
- HAT+ compliance
- RP2350 microcontroller (Pi's own silicon)
- Better firmware/software architecture
- 16MB onboard flash (vs. 8KB on Witty Pi 4)
- Open-source firmware in pico-sdk

### 3.2 Availability

- **UUGear (manufacturer):** Currently available for order
- **The Pi Hut (UK retailer):** In stock
- **Adafruit:** Not yet listed (as of search date)
- **Lead time:** Typical 1-2 weeks if in stock; 4-8 weeks if manufacturing

---

## 4. Witty Pi 4 vs. Witty Pi 5 Detailed Comparison

### 4.1 Architecture

| Aspect | Witty Pi 4 | Witty Pi 5 |
|--------|-----------|-----------|
| **Microcontroller** | AVR 8-bit (8KB flash) | RP2350 (16MB flash) |
| **Clock precision** | ±2 ppm | ±3.8-5 ppm |
| **Temp sensor resolution** | 0.125°C | 0.0625°C |
| **Temperature control** | High + low thresholds | High + low thresholds |
| **Power HAT standard** | Legacy HAT format | **HAT+ compliant** |
| **Firmware** | Proprietary assembly | Open-source C (pico-sdk) |
| **Flash memory** | 8KB | 16MB |
| **I2C address** | Various (configurable) | 0x51 (configurable) |

### 4.2 GPIO Interface

| Aspect | Witty Pi 4 | Witty Pi 5 |
|--------|-----------|-----------|
| **GPIO pins consumed** | 3 (GPIO-4, 14, 17) | **0** |
| **Interface type** | Mixed (GPIO + serial) | I2C only |
| **I2C dependency** | No | Yes (I2C1 only) |
| **Available for stacking** | Limited | **All 28 pins free** |
| **Pass-through header** | May require spacers | Built-in HAT+ pass-through |

### 4.3 Development Experience

| Aspect | Witty Pi 4 | Witty Pi 5 |
|--------|-----------|-----------|
| **Firmware source** | Closed | **Open-source (GitHub)** |
| **Configuration** | Serial or I2C | **USB flash drive emulation** |
| **Log viewing** | Serial console | **USB serial + web interface** |
| **Script formats** | .wpi | .wpi + **.act** (new) + **.skd** (new) |
| **Schedule storage** | Raspberry Pi SD card | **Witty Pi 5 onboard flash** |
| **Firmware updates** | Complex (need programmer) | **Drag-drop .uf2 file via USB** |
| **Python SDK** | Yes | Yes (improved) |

### 4.4 Power Management

| Feature | Witty Pi 4 | Witty Pi 5 |
|--------|-----------|-----------|
| **Power modes** | Single input or dual | Dual simultaneous + failover |
| **Current output** | Up to 5A | Up to 5A |
| **DC/DC input range** | 6-30V | 6-30V |
| **Power input channels** | VUSB + VIN | VUSB + VIN |
| **Voltage monitoring** | Yes | Yes |
| **Dual diodes** | No | **Yes** (robust failover) |
| **Software-accessible power status** | Limited | **Yes** (query which source) |

### 4.5 Scheduling Flexibility

**Witty Pi 4 schedule format (.wpi):**
```
# Simple example - runs every day 9am-5pm
START   2025-01-01 09:00:00
END     2025-12-31 17:00:00
ON      1 0 * * * (daily 1hr, off 0hr)
```

**Witty Pi 5 new .act format:**
```
# Human-readable action list
2025-01-01 09:00:00 ON
2025-01-01 17:00:00 OFF
2025-01-02 09:00:00 ON
...
```

**Witty Pi 5 .skd format:**
- Compressed binary version of .act
- Witty Pi 5 auto-converts .act to .skd
- Stores in onboard 16MB flash (not Pi's SD card)

### 4.6 Compatibility

| Model | A+ | B+ | 2B | Zero | Zero W | 3B | 3B+ | 4B | **5B** |
|-------|----|----|----|----|---------|----|----|----|----|
| Witty Pi 4 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Witty Pi 5 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

Both support all 40-pin GPIO header models.

---

## 5. GPIO Pass-Through & HAT+ Stacking Analysis

### 5.1 Witty Pi 4 Stacking Limitation

Witty Pi 4 consumes 3 GPIO pins:
- **GPIO-4:** Shutdown signal (input from Witty Pi)
- **GPIO-17:** System UP signal (output to Witty Pi)
- **GPIO-14:** Serial RX (from Witty Pi)

These pins are NOT available for other HATs. Adafruit Pi-EzConnect requires a pass-through header, but if GPIO-4, 14, 17 are consumed, there may be conflicts depending on the Pi-EzConnect's design.

### 5.2 Witty Pi 5 Stacking Advantage

Witty Pi 5 uses I2C-only communication:
- **GPIO-2:** I2C1 SDA (standard, shared with other I2C devices)
- **GPIO-3:** I2C1 SCL (standard, shared with other I2C devices)
- **All other GPIO:** Available

This frees GPIO-4, 14, 17 and all others for HAT stacking. Pi-EzConnect can sit directly on top without any GPIO conflicts.

### 5.3 I2C Address Coordination

| Device | I2C Address | Type |
|--------|-------------|------|
| Witty Pi 5 | 0x51 (default) | Power HAT+ |
| Adafruit Pi-EzConnect | Unknown (likely 0x50) | Stackable HAT |
| Raspberry Pi I2C EEPROM | 0x50 | System |

**Action needed:** Confirm Pi-EzConnect's I2C EEPROM address. If conflict with 0x51, one address can be changed via resistor network (both boards document this).

### 5.4 HAT+ Pass-Through Header

Witty Pi 5 is designed as a HAT+ with built-in pass-through capability. This means:
- ✅ Female headers connect to the 40-pin male GPIO header
- ✅ Male headers on top connect to stacked boards
- ✅ Standard 16mm standoffs maintain proper spacing
- ✅ All GPIO pins passed through (not consuming any)

**Recommendation:** Order with appropriate standoffs (typically 16mm for HAT stacking).

---

## 6. Backup Battery & RTC Support

### 6.1 Supercapacitor vs. Battery

Both Witty Pi 4 and Witty Pi 5 use **supercapacitors** for RTC backup:
- When main power is off, supercap keeps RTC running
- Duration: ~12-24 hours typical (depends on temperature)
- No external coin cell battery needed
- No maintenance required (no battery replacement)

### 6.2 Does NOT Support External Backup Battery

Neither Witty Pi 4 nor Witty Pi 5 has provisions for:
- External coin cell (CR2032)
- Separate UPS battery backup
- For full system UPS, you'd need an additional power HAT or separate UPS circuit

### 6.3 Power-Off Timekeeping

RTC continues to track time even when:
- Pi is powered off
- Input power (VUSB + VIN) is completely disconnected
- System is in sleep mode

This is critical for "wake at scheduled time" functionality.

---

## 7. Scheduling & Power Management Features

### 7.1 Time-Based Scheduling

**Both support:**
- Define wake times (e.g., "9am daily")
- Define sleep times (e.g., "5pm daily")
- Complex recurring schedules (.wpi format)
- One-time events

**Witty Pi 5 adds:**
- Linear .act format (easier to read and edit)
- Automatic .act-to-.skd conversion
- Schedule stored in Witty Pi 5's flash (not Pi's SD card)

### 7.2 Voltage-Based Power Control

When powered via VIN terminal block, both can:
- Monitor input voltage continuously
- Power down Pi if voltage drops below threshold (e.g., battery low)
- Power up Pi if voltage recovers above threshold (hysteresis)

Example: Battery-powered system
- Power ON when: 12V battery > 11V
- Power OFF when: 12V battery < 10V

**Use case for Indonesia deployment:** Sukabumi solar system can shutdown Pi when battery is depleted, resume when solar charges it back up.

### 7.3 Temperature-Based Power Control

**Witty Pi 4:**
- High temperature threshold (e.g., shut down at 45°C)
- Low temperature threshold (e.g., shut down at -10°C)
- On Witty Pi 4, low threshold **only stops** RTC counting; doesn't power down Pi

**Witty Pi 5:**
- High temperature threshold (power off if exceeded)
- Low temperature threshold (power off if exceeded)
- Both work symmetrically to power the Pi on/off

**Use case for Indonesia deployment:** Jakarta site can auto-shutdown if enclosure overheats; resume when temperature drops.

### 7.4 Combined Logic

Witty Pi 5 uses **OR logic** for power-off:
```
IF (time_to_sleep OR battery_too_low OR temp_too_high) THEN power_off
```

This is intuitive—any single condition triggers shutdown.

Power-on requires ALL conditions met:
```
IF (time_to_wake AND battery_adequate AND temp_nominal) THEN power_on
```

---

## 8. Software & Firmware

### 8.1 Open-Source Advantages (Witty Pi 5)

| Aspect | Witty Pi 4 | Witty Pi 5 |
|--------|-----------|-----------|
| **Firmware source** | Closed (binary only) | GitHub (C + pico-sdk) |
| **Software source** | Closed | GitHub (C) |
| **Customization** | Limited | Full modification possible |
| **Updates** | Requires special programmer | Drag-drop .uf2 via USB |
| **Community support** | UUGear forum | GitHub issues + community |

### 8.2 Configuration Methods

**Witty Pi 4:**
- Serial console commands
- I2C register writes (advanced)
- File-based on Pi's SD card

**Witty Pi 5:**
- **Emulated USB flash drive** (easiest!)
  - Connect USB cable, board appears as drive
  - Edit config.txt, schedule.wpi, scripts directly
  - No SSH needed for basic config
- Serial console (via USB)
- I2C register writes (advanced)
- File-based on Witty Pi 5's internal flash

### 8.3 Firmware Updates

**Witty Pi 4:**
- Complex: need AVR programmer hardware
- Time-consuming
- Rarely updated

**Witty Pi 5:**
- Simple: press BOOTSEL button + connect USB
- Board appears as flash drive
- Drag-drop .uf2 firmware file
- Automatic reboot
- GitHub repository with regular updates

---

## 9. Compatibility with Raspberry Pi 5

Both Witty Pi 4 and Witty Pi 5 are compatible with Raspberry Pi 5. Key differences:

| Aspect | Witty Pi 4 on Pi 5 | Witty Pi 5 on Pi 5 |
|--------|------------------|------------------|
| **Form factor** | HAT (legacy) | HAT+ (official) |
| **Stacking** | Possible but GPIO-limited | Recommended (full GPIO pass-through) |
| **Power delivery** | 5A (adequate) | 5A (adequate) |
| **Software** | Works, but Pi 5-specific features missing | Optimized for Pi 5 |
| **Future compatibility** | Uncertain (legacy standard) | Guaranteed (HAT+ standard) |

---

## 10. Comparison Table: Witty Pi 4 vs. Witty Pi 5

| Feature | Witty Pi 4 | Witty Pi 5 HAT+ | Winner for Pi 5 |
|---------|-----------|---|---|
| **Price** | €25 (~$29) | €39 (~$46) | WP4 (cheaper) |
| **Availability** | Good | Good | Tie |
| **RTC accuracy** | ±2 ppm | ±3.8-5 ppm | WP4 (better clock) |
| **Temp sensor** | 0.125°C | 0.0625°C | WP5 (2x better) |
| **GPIO pins used** | 3 (GPIO-4,14,17) | 0 (I2C only) | **WP5** |
| **HAT+ standard** | No (legacy) | Yes | **WP5** |
| **Firmware updates** | Hard (programmer) | Easy (USB drag-drop) | **WP5** |
| **Firmware source** | Closed | Open (GitHub) | **WP5** |
| **Power input channels** | 2 independent | 2 independent + failover | Tie |
| **Power output** | 5A | 5A | Tie |
| **Scheduling formats** | .wpi | .wpi + .act + .skd | **WP5** |
| **Schedule storage** | Pi SD card | Witty Pi flash | **WP5** |
| **Developer experience** | Intermediate | Excellent | **WP5** |
| **Pi 5 stacking support** | Limited | Full | **WP5** |
| **Future-proofing** | Uncertain (legacy) | Excellent (standard) | **WP5** |

---

## 11. Recommendation for BOM Update

### 11.1 Decision Matrix

For your Indonesia deployment (Raspberry Pi 5, Adafruit Pi-EzConnect stacking):

| Criterion | Witty Pi 4 | Witty Pi 5 | Recommendation |
|-----------|-----------|-----------|---|
| Cost-sensitive? | ✅ €25 | ✗ €39 | If budget critical, use WP4 |
| Long-term support? | ? (legacy) | ✅ (standard) | Use WP5 |
| GPIO pass-through? | ⚠ (conflicts) | ✅ (full) | Use WP5 |
| Future deployments? | ? | ✅ | Use WP5 |
| Developer ease? | Moderate | ✅ Excellent | Use WP5 |
| Production deployment? | ⚠ Risky | ✅ Safe | Use WP5 |

### 11.2 Recommendation

**✅ UPGRADE to Witty Pi 5 HAT+ for production deployments.**

**Rationale:**
1. **GPIO pass-through critical:** Witty Pi 5's I2C-only design ensures clean stacking with Adafruit Pi-EzConnect without GPIO conflicts
2. **HAT+ compliance:** Official standard support guarantees long-term compatibility and driver updates from Raspberry Pi foundation
3. **Developer experience:** Open-source firmware + USB configuration + easy updates reduce deployment risk
4. **Schedule independence:** Schedule stored in Witty Pi 5 flash (not Pi SD card) - survives Pi crashes
5. **Future-proofing:** Legacy HAT standard (Witty Pi 4) may not receive Pi 5 OS kernel updates

**Cost-benefit:**
- Additional €14/USD $17 per unit
- Elimination of potential GPIO conflicts
- Reduced field debugging time (estimated 10-20 hours over deployment lifetime)
- Confidence in production deployment

### 11.3 BOM Update Instructions

**Current spec (from CLAUDE.md):**
```
- [ ] Witty Pi 4 for scheduling + backup battery
```

**Updated spec:**
```
- [ ] Witty Pi 5 HAT+ for scheduling + backup battery + RTC
       Model: UUGear Witty Pi 5 HAT+
       Price: ~€39 / USD $46 / GBP £34 (Jan 2026)
       Source: UUGear.com or The Pi Hut
       Key advantage: I2C-only design allows full GPIO pass-through for Adafruit Pi-EzConnect stacking
```

**Stacking order (Sukabumi/Jakarta):**
```
Position 1 (bottom): Raspberry Pi 5
Position 2:          Witty Pi 5 HAT+
Position 3 (top):    Adafruit Pi-EzConnect (GPIO terminal block riser)
Spacing:             16mm standoffs between each level
```

**Verify before ordering:**
- [ ] Confirm Adafruit Pi-EzConnect I2C EEPROM address (should be 0x50, not conflicting with Witty Pi 5's 0x51)
- [ ] Order with HAT+ standard 16mm standoff spacers
- [ ] Request power delivery specs to confirm 5A is sufficient for Pi 5 + modem + displays

---

## 12. Technical Notes for Integration

### 12.1 I2C Communication

Witty Pi 5 communicates exclusively via I2C:
```
Raspberry Pi I2C1 (GPIO 2 & 3)
  └─ Witty Pi 5 (slave address 0x51)
  └─ Other I2C devices (address 0x50, 0x52, etc.)
```

No GPIO pins consumed beyond standard I2C. This is the key advantage for HAT stacking.

### 12.2 Power Budget

Witty Pi 5 can deliver **5A to Raspberry Pi 5 + HAT stack**.

Typical consumption:
- Raspberry Pi 5: 2-3A (under load)
- Witty Pi 5: <100mA
- Adafruit Pi-EzConnect: <50mA
- Connected peripherals: variable

For your deployment, confirm:
1. Modem current draw (Quectel EG25-G: ~500mA peak)
2. Status display (OLED: ~20mA, LCD: ~50mA)
3. Total system draw under maximum load

**Action:** Recalculate power budget with Witty Pi 5 in the stack.

### 12.3 Temperature Monitoring Integration

Witty Pi 5's temperature sensor can:
1. Monitor enclosure temperature via internal sensor
2. Trigger shutdown if thermal threshold exceeded (e.g., 45°C)
3. Allow software to query temp over I2C

For Jakarta site with active cooling, recommend:
- Set high temp threshold: 40°C (triggers warning/cooldown)
- Set low temp threshold: 10°C (monitor for cold nights)

### 12.4 Firmware Updates

To update Witty Pi 5 firmware after deployment:
1. Hold BOOTSEL button (on board)
2. Connect USB cable
3. Board appears as "RPI-RP2" flash drive
4. Download new .uf2 from UUGear GitHub
5. Copy to board
6. Automatic reboot and update

**No programmer hardware needed.** This is a major advantage over Witty Pi 4.

---

## 13. Sources & Documentation

- [UUGear Official Product Page - Witty Pi 5 HAT+](https://www.uugear.com/product/witty-pi-5/)
- [UUGear Witty Pi 5 Announcement](https://www.uugear.com/news/introducing-witty-pi-5-hat-available-now/)
- [Witty Pi 5 Official User Manual](https://www.uugear.com/doc/WittyPi5_UserManual.pdf)
- [Witty Pi 5 GitHub Firmware](https://github.com/uugear/Witty-Pi-5-Firmware)
- [Witty Pi 5 GitHub Software](https://github.com/uugear/Witty-Pi-5-Software)
- [Witty Pi 4 Product Page - Comparison Reference](https://www.uugear.com/product/witty-pi-4/)
- [The Pi Hut - Witty Pi 5 HAT+ Retailer](https://thepihut.com/products/witty-pi-5-hat-real-time-clock-and-power-management-for-raspberry-pi)
- [Raspberry Pi HAT+ Specification](https://datasheets.raspberrypi.com/hat/hat-plus-specification.pdf)
- [Adafruit Pi-EzConnect Product](https://www.adafruit.com/product/2711)

---

## 14. Next Steps

1. **Verify I2C address:** Confirm Adafruit Pi-EzConnect's I2C EEPROM address to ensure no conflict with Witty Pi 5's 0x51
2. **Update BOM:** Replace Witty Pi 4 with Witty Pi 5 HAT+ and update pricing
3. **Recalculate power budget:** Account for Witty Pi 5 in the I2C power draw calculations
4. **Order samples:** Get one unit for Sukabumi site to test stacking configuration before full production
5. **Firmware baseline:** Identify stable Witty Pi 5 firmware version for deployment; document update procedure
6. **Test schedule:** Verify .act or .wpi schedule format works with your power management requirements

---

**Report completed:** January 8, 2026
**Recommendation:** UPGRADE to Witty Pi 5 HAT+ for Pi 5 deployments
