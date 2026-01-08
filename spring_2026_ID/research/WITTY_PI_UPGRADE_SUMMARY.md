# Witty Pi Upgrade Summary - Quick Reference
## For Indonesia Spring 2026 BOM Update

---

## Bottom Line

**RECOMMEND: Upgrade from Witty Pi 4 to Witty Pi 5 HAT+ for new Raspberry Pi 5 deployments**

**Why:** I2C-only design enables clean stacking with Adafruit Pi-EzConnect (no GPIO conflicts)

---

## Key Comparison for Your Use Case

| Aspect | Witty Pi 4 | Witty Pi 5 HAT+ |
|--------|-----------|---|
| **Price** | €25 (~$29) | €39 (~$46) |
| **GPIO pins used** | 3 (GPIO-4,14,17) | **0 - I2C only** ✅ |
| **HAT+ compliant** | No | **Yes** ✅ |
| **Stacking with Pi-EzConnect** | ⚠ Possible conflicts | **Clean - no conflicts** ✅ |
| **Power delivery** | 5A | 5A |
| **Temperature sensor** | 0.125°C | 0.0625°C (2x better) |
| **Firmware updates** | Hard (need programmer) | **Easy (USB drag-drop)** ✅ |
| **Firmware source** | Closed | **Open (GitHub)** ✅ |

---

## Critical Stacking Benefit

### Witty Pi 4 (GPIO Consuming)
```
GPIO-2,3  → I2C1 (shared)
GPIO-4    → shutdown signal (CONFLICT?)
GPIO-14   → serial RX (CONFLICT?)
GPIO-17   → system UP (CONFLICT?)
GPIO-27   → available for other HATs
...
```
**Issue:** If Adafruit Pi-EzConnect uses any of GPIO-4, 14, or 17, there's a conflict.

### Witty Pi 5 (I2C Only)
```
GPIO-2,3  → I2C1 (shared, standard)
All others → AVAILABLE for other HATs
```
**Advantage:** ALL GPIO pins available for Pi-EzConnect. No conflicts.

---

## BOM Update Required

**File:** `/home/tjordan/code/git/openrivercam/spring_2026_ID/CLAUDE.md`

**Current entry (line 279):**
```
- [ ] Witty Pi 4 for scheduling + backup battery
```

**Updated entry:**
```
- [ ] Witty Pi 5 HAT+ for scheduling + backup battery + RTC
       UUGear Witty Pi 5 HAT+
       Price: €39 (Jan 2026) ≈ USD $46 / GBP £34
       Source: uugear.com or thepihut.com
       Key advantage: I2C-only GPIO frees all pins for Pi-EzConnect stacking
       Order note: Request 16mm standoff spacers for HAT+ stacking
```

---

## Stack Order (Sukabumi & Jakarta)

```
[Position 3]  Adafruit Pi-EzConnect (GPIO terminal block riser)
[Position 2]  Witty Pi 5 HAT+ (power & RTC)
[Position 1]  Raspberry Pi 5 (4GB minimum, 8GB preferred)
              ↓
         [16mm standoffs]

I2C address coordination:
- Raspberry Pi I2C1 EEPROM: 0x50
- Witty Pi 5: 0x51 (default, configurable)
- Pi-EzConnect: 0x50 or 0x51? → VERIFY BEFORE ORDERING
```

---

## Price Impact

| Item | Qty | Unit Cost | Total |
|------|-----|-----------|-------|
| Witty Pi 4 | 2 | €25 | €50 |
| Witty Pi 5 HAT+ | 2 | €39 | €78 |
| **Price increase** | | | **€28 total (+56%)** |
| **Per unit** | | | **€14 (+56%)** |

**For 2-unit deployment (Sukabumi + Jakarta): +€28 (~+USD $32)**

---

## Verification Tasks Before Ordering

1. **I2C EEPROM address check:**
   - Confirm Adafruit Pi-EzConnect uses 0x50 (not 0x51)
   - If conflict, address can be changed via resistor network
   - Document in assembly guide

2. **Power delivery check:**
   - Confirm Witty Pi 5 can deliver 5A under load
   - Include modem (Quectel EG25-G ~500mA peak) in calculation
   - Include display power (OLED ~20mA, LCD ~50mA)

3. **GPIO pass-through test:**
   - Order sample unit for Sukabumi site
   - Verify Pi-EzConnect mounts cleanly on top
   - Test I2C communication with both boards

4. **Firmware baseline:**
   - Identify stable Witty Pi 5 firmware version on GitHub
   - Document version number in deployment specs
   - Create recovery procedure if update needed in field

---

## Advantages of Witty Pi 5

1. **Official HAT+ compliance** → Future driver support guaranteed
2. **I2C-only design** → All GPIO freed for expansion (Pi-EzConnect)
3. **Open-source firmware** → Can customize for field conditions
4. **Easy firmware updates** → USB drag-drop vs. programmer hardware
5. **Schedule independence** → Stores schedule in Witty Pi flash, survives Pi crashes
6. **Better temperature sensor** → 0.0625°C vs. 0.125°C (tropical humidity monitoring)
7. **Future-proof** → Legacy HAT standard (WP4) may not get Pi 5 support

---

## Disadvantages of Witty Pi 5

1. **56% more expensive** → €14/unit additional cost
2. **Slightly worse RTC accuracy** → ±3.8-5 ppm vs. ±2 ppm (negligible difference)
3. **Requires I2C1** → Depends on two GPIO pins (but all others free)

---

## Deployment Confidence

| Aspect | WP4 Risk | WP5 Risk |
|--------|----------|----------|
| **HAT+ stacking** | ⚠ Medium (GPIO conflicts possible) | ✅ Low (I2C only) |
| **Long-term support** | ⚠ Uncertain (legacy standard) | ✅ High (official standard) |
| **Field maintenance** | ⚠ Medium (firmware updates hard) | ✅ Low (USB updates easy) |
| **GPIO expansion** | ⚠ Limited (3 pins consumed) | ✅ Full (all freed) |
| **Community help** | ⚠ Limited (older product) | ✅ Active (new product) |

**Overall:** Witty Pi 5 is the safer choice for production deployment.

---

## Documentation References

**Full research:** `/home/tjordan/code/git/openrivercam/witty_pi_5_research.md`

**Source documents:**
- UUGear Witty Pi 5 Product: https://www.uugear.com/product/witty-pi-5/
- Official User Manual: https://www.uugear.com/doc/WittyPi5_UserManual.pdf
- GitHub Firmware: https://github.com/uugear/Witty-Pi-5-Firmware
- HAT+ Specification: https://datasheets.raspberrypi.com/hat/hat-plus-specification.pdf

---

## Decision Checkpoint

**Question:** Should we proceed with Witty Pi 5 upgrade?

**Approval needed from:** tjordan (stakeholder)

**Items to decide:**
- [ ] Accept €14/unit additional cost?
- [ ] Proceed with Witty Pi 5 HAT+ for both sites?
- [ ] Order sample unit for Sukabumi test before full production?
- [ ] Schedule Witty Pi 5 firmware baseline identification?

---

**Document Date:** January 8, 2026
**Status:** Ready for BOM integration
