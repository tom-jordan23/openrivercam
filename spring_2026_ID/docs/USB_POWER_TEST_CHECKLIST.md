# USB-C Power Test Checklist

**Date:** 2026-03-28
**Purpose:** Verify USB bus stability when Pi 5 is powered via USB-C instead of GPIO backfeed
**Hypothesis:** GPIO backfeed bypasses PMIC, causing USB bus instability (228 disconnects, 158 URB errors in 12 min)

## Setup

1. Disconnect DDR-60G-5 5V/GND leads from GPIO pins
2. Connect USB-C power supply to Pi 5 USB-C port
3. Leave all USB-A devices connected as-is:
   - Keyboard (Logitech, USB 2.0)
   - Mouse (Logitech, USB 2.0)
   - Samsung FIT Plus 256GB (USB 3.0)
   - Quectel EG25-G modem via EXVIST adapter (USB 2.0)
4. Power on

## Post-Boot Checks (wait 2 minutes after login prompt)

### A. USB Bus Stability (the key test)

```bash
# Count USB disconnect events — was 228 in 12 min with GPIO power
dmesg | grep -c "USB disconnect"

# Count URB errors — was 158 in 12 min with GPIO power
dmesg | grep -c "nonzero urb status"

# All 4 USB devices present?
lsusb
```

| Metric | GPIO backfeed (before) | USB-C (now) | Pass if |
|--------|----------------------|-------------|---------|
| USB disconnects | 228 in 12 min | | < 5 |
| URB errors | 158 in 12 min | | 0 |
| Keyboard present | Yes (flaky) | | Yes, no lag |
| Mouse present | Yes (flaky) | | Yes |
| SanDisk present | Yes | | Yes |
| Modem present (2c7c) | No (dropped off) | | Yes |

### B. Modem (was the first casualty)

```bash
lsusb | grep -i 2c7c
ls /dev/ttyUSB*
mmcli -L
```

| Check | Before | Now | Pass if |
|-------|--------|-----|---------|
| Modem in lsusb | Missing | | Present |
| /dev/ttyUSB0-3 | Missing | | All 4 present |
| ModemManager sees it | N/A | | Quectel EG25-G listed |

### C. USB Storage Mount

```bash
lsblk | grep sda
mount | grep /mnt/usb
df -h /mnt/usb
ls /mnt/usb/incoming/
```

| Check | Before | Now | Pass if |
|-------|--------|-----|---------|
| sda in lsblk | Yes | | Yes |
| Mounted at /mnt/usb | **No** | | Yes |
| Size ~229G | N/A | | Yes |
| incoming/ accessible | Via root (unmounted) | | Via /mnt/usb |

If not mounted: `sudo mount /mnt/usb` — but the real test is whether it auto-mounts on boot without disconnect cycling.

### D. Power & Thermal

```bash
vcgencmd get_throttled
vcgencmd measure_temp
uptime
```

| Check | Before | Now | Pass if |
|-------|--------|-----|---------|
| Throttled | 0x0 | | 0x0 |
| CPU temp | 56.5°C @ 12 min | | < 60°C |

### E. Keyboard Feel

No command — just type. With GPIO power the keyboard lagged during URB error bursts.

- [ ] Keyboard responsive, no input lag
- [ ] No dropped keystrokes

## Wait Test (5 minutes)

After completing checks above, wait 5 minutes with the system idle, then re-run:

```bash
dmesg | grep -c "USB disconnect"
dmesg | grep -c "nonzero urb status"
lsusb
ls /dev/ttyUSB*
```

- [ ] Counts have NOT increased since initial check
- [ ] All USB devices still present
- [ ] Modem still has ttyUSB0-3

## Result

- [ ] **PASS** — USB-C power resolves bus instability → update circuit diagram, DDR-60G-5 must feed USB-C
- [ ] **FAIL** — Problem persists → USB power path is not the root cause, investigate modem/cable/hub

## If PASS: Next Steps

1. Source USB-C cable with CC resistors for DDR-60G-5 → Pi connection
2. Update circuit diagram (DDR-60G-5 out → USB-C, not GPIO)
3. Verify DDR-60G-5 + USB-C cable powers Pi correctly (CC resistors needed for 5V negotiation)
4. Re-run full REBOOT_CHECKLIST.md
