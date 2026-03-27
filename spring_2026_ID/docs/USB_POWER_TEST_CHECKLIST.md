# USB Power Troubleshooting Log

**Date:** 2026-03-28
**Purpose:** Diagnose and fix USB bus instability (disconnect storms, URB errors)

## History

### Round 1: GPIO Backfeed (DDR-60G-5 → GPIO pins)

- 228 USB disconnects in 12 min
- 158 URB errors in 12 min
- Modem dropped off bus entirely
- Keyboard input lag during URB bursts
- **Hypothesis:** GPIO backfeed bypasses PMIC → USB bus instability

### Round 2: USB-C Power (DDR-60G-5 disconnected, USB-C PSU)

Switched to USB-C power to test PMIC hypothesis.

| Metric | GPIO backfeed | USB-C | Pass? |
|--------|---------------|-------|-------|
| USB disconnects | 228 / 12 min | 44 / 4 min | **FAIL** (rate similar) |
| URB errors | 158 / 12 min | 37 / 4 min | **FAIL** |
| Modem present | No | Briefly, then dropped | **FAIL** |
| Keyboard present | Flaky | Yes (cycling) | — |
| Mouse present | Flaky | Yes (cycling) | — |
| SanDisk present | Yes | Yes (cycling) | — |
| Throttled | 0x0 | 0x0 | OK |
| CPU temp | 56.5°C | 51.6°C | OK |

**Result: FAIL — USB-C power did NOT fix the problem. GPIO backfeed was not the root cause.**

### Round 3: Isolation Testing (USB-C power, device-by-device)

Unplugged devices one at a time to find the culprit.

| Configuration | Stable? | Disconnects | Notes |
|---------------|---------|-------------|-------|
| All 4 devices | No | 72 in ~3.5 min then stabilized | Modem fell off at t=212s |
| Modem removed, drive in | Yes | 0 new | Stable immediately |
| Both removed (kb+mouse only) | Yes | 0 new | Stable |
| **Modem in, drive out** | **Yes** | **0 new** | Modem + ttyUSB0-3 + mmcli all stable |
| **Both back in (re-seated)** | **Yes** | **0 new over 20s** | All devices stable after manual re-seat |

**Key finding:** The problem is a **boot-time enumeration storm**, not a steady-state issue.
Both devices coexist fine once the bus has settled. The storm happens when all
devices enumerate simultaneously at boot.

### Root Cause: UAS Driver + Samsung FIT

```
$ lsusb -t   (Bus 004)
    Port 001: Dev 020, If 0, Class=Mass Storage, Driver=uas, 5000M

$ lsusb -v -d 0781:5583 | grep MaxPower
    MaxPower              896mA

$ dmesg | grep "scsi host0: uas"
[    1.083335] scsi host0: uas      ← re-inits every ~20s during boot storm
[   14.955805] scsi host0: uas
[   34.788845] scsi host0: uas
   ... (repeated ~18 times through t=330s)
```

The Samsung FIT Plus (0781:5583) uses the **UAS (USB Attached SCSI)** driver, which
repeatedly crashes and re-enumerates during boot. Each re-enumeration cascades to
other USB devices (modem, keyboard, mouse). The drive also claims **896mA** — combined
with the modem's draw, the simultaneous enumeration causes bus brownouts.

**Existing fix attempt (not working):**
```
$ cat /etc/modprobe.d/sandisk-no-uas.conf
options usb-storage quirks=0781:5583:u
```

This file exists but is **NOT included in the initramfs**:
```
$ lsinitramfs /boot/initrd.img-$(uname -r) | grep sandisk
(no output)
```

The UAS module loads from initramfs before `usb-storage` sees the quirk, so UAS
claims the device first. The modprobe.d file is ignored.

## Fix: Rebuild Initramfs

Rebuild initramfs so it includes `/etc/modprobe.d/sandisk-no-uas.conf`. This makes
the `usb-storage` quirk available early enough to prevent UAS from claiming the drive.

### Pre-reboot steps

```bash
# Verify the quirk file is correct
cat /etc/modprobe.d/sandisk-no-uas.conf
# Should show: options usb-storage quirks=0781:5583:u

# Rebuild initramfs
sudo update-initramfs -u

# Verify the file is now included
lsinitramfs /boot/initrd.img-$(uname -r) | grep sandisk
# Should show: etc/modprobe.d/sandisk-no-uas.conf
```

### Post-reboot verification

```bash
# 1. Check UAS is NOT used for the SanDisk (most important check)
lsusb -t | grep "Mass Storage"
# PASS: Driver=usb-storage    FAIL: Driver=uas

# 2. USB disconnect count (wait 2 min after login)
dmesg | grep -c "USB disconnect"
# PASS: < 5    FAIL: > 10

# 3. URB errors
dmesg | grep -c "nonzero urb status"
# PASS: 0    FAIL: > 0

# 4. All 4 USB devices present and stable
lsusb
# Should show: Logitech keyboard, Logitech mouse, SanDisk Ultra Fit, Quectel 2c7c

# 5. Modem functional
ls /dev/ttyUSB*          # ttyUSB0-3
mmcli -L                 # Quectel EG25-G listed

# 6. USB storage mounted
mount | grep /mnt/usb    # /dev/sda1 on /mnt/usb type ext4
df -h /mnt/usb           # ~229G

# 7. No throttling
vcgencmd get_throttled   # 0x0

# 8. Wait 5 min, re-run checks 2-4 — counts should NOT increase
```

### If initramfs fix fails

Fallback: create a systemd service that unbinds the drive from UAS and rebinds
to usb-storage after boot. Less clean but does not require /boot/firmware access.

## Current Hardware State (2026-03-28)

- **Power:** USB-C PSU (DDR-60G-5 disconnected)
- **USB-A port 1:** Quectel EG25-G modem via EXVIST adapter
- **USB-A port 2:** Samsung FIT Plus 256GB (mounted at /mnt/usb)
- **USB-A port 3:** Logitech keyboard
- **USB-A port 4:** Logitech mouse
- **Bus status:** Stable (after manual re-seat of all devices)
- **/boot/firmware:** Not mounted (90-qemu.rules — see BOOT_FAILURE_ANALYSIS.md)
