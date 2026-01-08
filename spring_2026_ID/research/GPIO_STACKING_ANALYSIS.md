# GPIO Stacking Analysis: Witty Pi 4 vs. Witty Pi 5 with Adafruit Pi-EzConnect

**Context:** Determining if Witty Pi HAT can stack cleanly with Adafruit Pi-EzConnect for GPIO terminal block riser functionality.

---

## Background

The deployment uses a 3-board stack on Raspberry Pi 5:

```
[Level 3] Adafruit Pi-EzConnect (GPIO terminal block breakout)
[Level 2] Witty Pi (power + RTC management)
[Level 1] Raspberry Pi 5
```

**Critical question:** Do Witty Pi 4 and Witty Pi 5 conflict with Pi-EzConnect's GPIO usage?

---

## Witty Pi 4 GPIO Pinout

### Pins Consumed by Witty Pi 4

| GPIO Pin | Function | Usage |
|----------|----------|-------|
| **GPIO-4** | Shutdown signal input | Witty Pi 4 listens for Pi shutdown request |
| **GPIO-14** | Serial TXD | Witty Pi 4 receives serial data from Pi (bootloader) |
| **GPIO-17** | System UP signal output | Witty Pi 4 drives LED and status signal |

### Pi-EzConnect Pinout

Adafruit Pi-EzConnect exposes ALL 28 GPIO pins as screw terminals:
- GPIO-2 through GPIO-27 (all 40-pin header GPIO)
- Power rails (5V, 3.3V, GND)
- NO special pins consumed (pass-through only)

### Conflict Analysis: WP4 + Pi-EzConnect

| Pin | Witty Pi 4 | Pi-EzConnect | Conflict? |
|-----|-----------|--------------|-----------|
| GPIO-4 | Shutdown input | Available on terminal (screw-in) | ⚠ **YES** |
| GPIO-14 | Serial RX | Available on terminal (screw-in) | ⚠ **YES** |
| GPIO-17 | System UP output | Available on terminal (screw-in) | ⚠ **YES** |
| GPIO-2,3 | I2C1 (SDA,SCL) | Available on terminal (screw-in) | ⚠ **MAYBE** |

### The Problem

When Pi-EzConnect is installed on top of Witty Pi 4:

1. **GPIO-4, 14, 17 are unavailable** for user connections (terminal block)
2. **Screw-in connections** to GPIO-4, 14, or 17 create **parallel connections** to Witty Pi 4's signals
3. This can cause:
   - Current conflicts (both devices driving same pin)
   - Signal corruption (impedance mismatches)
   - Component damage (overcurrent on I/O pin)

**Example:** If user connects a relay control to "GPIO-17" terminal block while Witty Pi 4 is driving it as "System UP" signal = potential short circuit.

---

## Witty Pi 5 HAT+ GPIO Pinout

### Pins Consumed by Witty Pi 5

**ONLY I2C pins (standard):**

| GPIO Pin | Function | Protocol |
|----------|----------|----------|
| **GPIO-2** | I2C1 SDA (data line) | I2C (shared) |
| **GPIO-3** | I2C1 SCL (clock line) | I2C (shared) |

### No GPIO Signals Used

Witty Pi 5 does NOT use:
- GPIO-4 (no shutdown signal input)
- GPIO-14 (no serial communication)
- GPIO-17 (no system UP signal)
- Any other GPIO pins

### Why I2C-Only?

Witty Pi 5 uses the RP2350 microcontroller with I2C slave functionality:
- Firmware is independent (not reliant on Pi's serial boot)
- Communication is purely I2C over GPIO-2,3 (standard pins)
- Can be updated independently (BOOTSEL mode)
- Allows schedule to run even if Pi crashes (onboard flash)

### Conflict Analysis: WP5 + Pi-EzConnect

| Pin | Witty Pi 5 | Pi-EzConnect | Conflict? |
|-----|-----------|--------------|-----------|
| GPIO-2 | I2C1 SDA | Available on terminal (screw-in) | ⚠ Shared, but safe |
| GPIO-3 | I2C1 SCL | Available on terminal (screw-in) | ⚠ Shared, but safe |
| GPIO-4 | **UNUSED** | Available on terminal (screw-in) | ✅ **NO** |
| GPIO-14 | **UNUSED** | Available on terminal (screw-in) | ✅ **NO** |
| GPIO-17 | **UNUSED** | Available on terminal (screw-in) | ✅ **NO** |
| All others | UNUSED | Available on terminals | ✅ **NO** |

### The Advantage

When Pi-EzConnect is installed on top of Witty Pi 5:

1. **All 28 GPIO pins available** for user connections
2. **I2C pins (GPIO-2,3) can be shared** safely:
   - Witty Pi 5: I2C slave at address 0x51
   - Other devices: Can use same I2C bus at different addresses
   - Pi-EzConnect: EEPROM at address 0x50 (or 0x51 if changed)
3. **No signal conflicts** - no parallel connections
4. **User can safely connect sensors, relays, etc. to GPIO-4, 14, 17**

---

## I2C Address Coordination

Both boards use I2C, so addresses must be unique:

| Device | I2C Address | Notes |
|--------|------------|-------|
| Witty Pi 5 | **0x51** (default) | Configurable via firmware |
| Adafruit Pi-EzConnect EEPROM | **0x50** (typical) | Verify on your unit |
| Raspberry Pi I2C EEPROM | **0x50** | System board |

**Potential conflict:** If Pi-EzConnect uses 0x51 (same as Witty Pi 5), one must be changed.

**Resolution:** Both boards document how to change I2C address via resistor network:
- Witty Pi 5: Firmware configurable or resistor mod
- Pi-EzConnect: Resistor network on board (see datasheet)

**Action:** Confirm Pi-EzConnect's address before ordering. If conflict, document resistor modification in assembly guide.

---

## Shared I2C Bus Safety

Is it safe to have Witty Pi 5 and Pi-EzConnect on the same I2C1 bus?

**YES - if addresses don't conflict:**

```
Raspberry Pi I2C1 (GPIO-2: SDA, GPIO-3: SCL)
├─ Witty Pi 5 (slave address 0x51)
│  └─ Responds to I2C reads/writes on 0x51
├─ Pi-EzConnect (EEPROM at address 0x50)
│  └─ Responds to I2C reads/writes on 0x50
└─ Other I2C devices (various addresses)
   └─ Temperature sensor, OLED display, etc.
```

Each device only responds to its own address. No conflicts.

**Common practice:** Most Raspberry Pi projects have 5-10 devices on the same I2C bus.

---

## Electrical Isolation

When Witty Pi 5 consumes only I2C pins:

| Signal Type | Witty Pi 5 | Pi-EzConnect | Isolation |
|-------------|-----------|--------------|-----------|
| **Power rails** | VCC, GND via header | VCC, GND via header | ✅ Common (OK) |
| **GPIO logic** | I2C only (GPIO-2,3) | All GPIO (2-27) | ✅ Isolated |
| **GPIO ground** | Single GND plane | Single GND plane | ✅ Common (OK) |

**No isolation problems.** Both devices share:
- 5V power rail
- 3.3V power rail
- Ground plane

This is expected for stacked HATs.

---

## Current Draw Impact

### Witty Pi 4 Current
- Logic: ~30mA
- RTC: ~5mA
- Total: ~35-50mA

### Witty Pi 5 Current
- RP2350 MCU: ~40mA
- RTC: ~5mA
- I2C communication: <1mA
- Total: ~45-60mA

### Pi-EzConnect Current
- No active components (passive terminal block)
- Current: <1mA
- Just provides screw terminals for GPIO

### Total System Current (with Pi 5)
- Raspberry Pi 5: 1500-2500mA (depending on load)
- Witty Pi: ~50-60mA
- Pi-EzConnect: <1mA
- Connected peripherals: variable

**Impact:** Negligible (0.1% of total). No concern.

---

## Thermal Impact

### Witty Pi 4 Heat Generation
- AVR microcontroller: ~0.5W (modest)
- No heatsink needed
- Operates 0-50°C ambient

### Witty Pi 5 Heat Generation
- RP2350 microcontroller: ~0.3-0.5W
- No heatsink needed
- Operates 0-50°C ambient

### Pi-EzConnect Heat Generation
- Passive (no active components)
- Just screw terminals

### Stacking Impact
- Three boards stacked creates minor airflow restriction
- Combined heat: ~0.5W (negligible vs. Pi 5's 5-10W under load)
- No thermal issues expected

**Recommendation:** Ensure enclosure has adequate ventilation (same as any Pi deployment).

---

## GPIO Availability Comparison

### With Witty Pi 4 + Pi-EzConnect

**Unavailable for user connections:**
- GPIO-2, GPIO-3: I2C1 (shared with system)
- GPIO-4: Witty Pi 4 shutdown signal
- GPIO-14: Witty Pi 4 serial RX
- GPIO-17: Witty Pi 4 system UP signal
- (Total: 5 pins consumed)

**Available for user connections:**
- GPIO-5 through GPIO-13: 9 pins
- GPIO-15, GPIO-16: 2 pins
- GPIO-18 through GPIO-27: 10 pins
- (Total: 21 pins available out of 28)

### With Witty Pi 5 + Pi-EzConnect

**Unavailable for user connections:**
- GPIO-2, GPIO-3: I2C1 (shared with system)
- (Total: 2 pins consumed)

**Available for user connections:**
- GPIO-4 through GPIO-27: 24 pins available out of 28

**Difference:** Witty Pi 5 frees up **3 additional GPIO pins** (GPIO-4, 14, 17) for user expansion.

---

## Recommendation

### Use Witty Pi 5 HAT+ for Clean Stacking

| Aspect | Witty Pi 4 | Witty Pi 5 | Recommendation |
|--------|-----------|-----------|---|
| **GPIO conflicts** | ⚠ GPIO-4,14,17 | ✅ None | Use WP5 |
| **I2C shared bus** | ✅ Only GPIO-2,3 | ✅ Only GPIO-2,3 | Tie |
| **Available GPIO** | 21/28 pins | **24/28 pins** | Use WP5 |
| **Current draw** | ~50mA | ~60mA | Negligible difference |
| **Thermal** | ~0.5W | ~0.5W | Negligible difference |
| **HAT+ compliant** | No | **Yes** | Use WP5 |

### Assembly Procedure (Witty Pi 5 + Pi-EzConnect)

1. **Install Witty Pi 5 on Pi 5** with 16mm standoffs
2. **Install Pi-EzConnect on Witty Pi 5** with 16mm standoffs
3. **Verify I2C addresses:**
   - Connect USB to both boards
   - Run `i2cdetect -y 1` from Pi SSH
   - Should see 0x50 (Pi-EzConnect) and 0x51 (Witty Pi 5)
   - If conflict, modify one address per board documentation

4. **Document final GPIO assignment:**
   - Create diagram showing which GPIO pins are available for user sensors/relays
   - Label screw terminals on Pi-EzConnect with pin numbers

---

## Risk Mitigation

### If Using Witty Pi 4 (Cheaper Option)

**IF you choose WP4 for cost reasons:**

1. **Document GPIO conflicts:**
   - GPIO-4, 14, 17 are NOT available via Pi-EzConnect terminals
   - Update assembly guide clearly

2. **Prevent user error:**
   - Label Pi-EzConnect terminals: "GPIO-4, 14, 17 not available (used by Witty Pi 4)"
   - Or physically block those terminals

3. **Test before deployment:**
   - Verify no sensors/relays try to use GPIO-4, 14, or 17
   - Check ORC software doesn't use these pins for any functions

### Recommended: Witty Pi 5 (Safe Option)

**All GPIO available. No documentation needed. No risk of user error.**

---

## Verification Checklist Before Ordering

- [ ] Confirm Adafruit Pi-EzConnect I2C EEPROM address (typically 0x50)
- [ ] Confirm Witty Pi 5 default address is 0x51
- [ ] If addresses conflict, identify resistor modification procedure for one board
- [ ] Verify 16mm standoff spacers are available (standard for HAT stacking)
- [ ] Test stacking order with sample unit before production
- [ ] Document final GPIO availability in assembly guide
- [ ] Update BOM with correct Witty Pi 5 part number

---

## Conclusion

**Witty Pi 5 HAT+ is the superior choice for stacking with Adafruit Pi-EzConnect.**

- ✅ No GPIO conflicts
- ✅ All 24+ pins available for expansion
- ✅ Official HAT+ compliance
- ✅ Future-proof
- ⚠️ Cost: €14/unit additional (justified)

Proceed with Witty Pi 5 upgrade for production deployment.

---

**Analysis Date:** January 8, 2026
**Status:** Ready for BOM integration
