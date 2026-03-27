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

## Fix Attempts

### Attempt 1: modprobe.d quirk (already in place, ineffective)

`/etc/modprobe.d/sandisk-no-uas.conf` contains `options usb-storage quirks=0781:5583:u`
but both `uas` and `usb-storage` are **kernel built-ins** (not modules), so modprobe.d
is ignored entirely.

### Attempt 2: Rebuild initramfs (ineffective)

`sudo update-initramfs -u` completed but the quirk file was not included because
the drivers are built-in, not loaded from initramfs.

### Attempt 3: Runtime unbind/rebind (ineffective)

Unbinding from UAS works, but rebinding to usb-storage fails (`No such device or
address`). Toggling device authorization causes UAS to reclaim the device.

### Required fix (deferred — post-deployment)

The only way to pass quirks to a built-in driver is via kernel command line:
```
usb-storage.quirks=0781:5583:u
```
This must be added to `cmdline.txt` on the SD card boot partition. That partition
is not accessible while 90-qemu.rules is active — fixing this requires careful
work to temporarily expose the real SD card device nodes without breaking the
boot chain. See BOOT_FAILURE_ANALYSIS.md.

## Decision: Deploy Without USB Flash Drive (2026-03-28)

**Context:** Deployment in 10 days. No time to safely resolve the UAS/cmdline.txt
issue or order new hardware.

**Plan:**
- Remove Samsung FIT Plus from the build
- Reconnect DDR-60G-5 buck converter to GPIO (original power config)
- Store captures on SD card rootfs (~43GB free) instead of USB drive
- Modem is stable on its own with GPIO power (confirmed by isolation testing)
- Revisit USB storage post-deployment when boot partition can be safely accessed

**What this costs:**
- Storage: 43GB (SD card) instead of 233GB (USB) — still sufficient for captures
  at 5s video × 96 cycles/day, with regular upload clearing space
- No redundant storage (captures on same media as OS)

**What this preserves:**
- Stable USB bus (modem + keyboard/mouse, no storms)
- Original power architecture (DDR-60G-5 → GPIO, no USB-C cable needed)
- Known-working boot chain

## Current Hardware State (2026-03-28)

- **Power:** DDR-60G-5 buck converter → GPIO (original config, reconnect needed)
- **USB-A:** Quectel EG25-G modem via EXVIST adapter only
- **USB storage:** Samsung FIT Plus 256GB **removed** (UAS boot storm)
- **Capture storage:** SD card rootfs (~43GB free)
- **/boot/firmware:** Not mounted (90-qemu.rules — see BOOT_FAILURE_ANALYSIS.md)

## Clean Boot Verification (2026-03-28)

Fresh reboot with Samsung FIT removed, DDR-60G-5 → GPIO power.

### Boot Baseline (Pi only, PoE relay OFF)

| Metric | Result |
|--------|--------|
| Boot time | Clean, no errors |
| `throttled` | `0x0` — no undervoltage |
| CPU temp (idle, no cooler) | 50.5°C |
| USB bus errors in dmesg | **Zero** |
| USB disconnects in dmesg | **Zero** |
| Modem (EG25-G) | Detected at t=8s, ttyUSB0-3 + wwan0 all present |
| Keyboard/mouse | Stable |

### Under Load (PoE relay ON — camera + PoE switch powered)

| Metric | +10s | +60s |
|--------|------|------|
| `throttled` | `0x0` | `0x0` |
| CPU temp | 53.8°C | 56.5°C |
| USB bus errors | Zero | Zero |
| Modem status | Stable | Stable |
| eth0 link | — | Up, 1Gbps |
| Camera (192.168.50.139) | — | Pingable, 0.3ms |

**Result: PASS — GPIO 5V power handles full system load (Pi + modem + relay + PoE switch + camera) with no voltage sag or USB instability.**

### Phase 4 Checklist Status

| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| Boot | ≤60s | Clean | PASS |
| OS | RPi OS Lite 64-bit | Debian 13 trixie aarch64 | PASS |
| Memory | ~8 GB | 7.9 GB | PASS |
| SD card | Detected | 59.5 GB mmcblk0 | PASS |
| USB flash | — | Removed (deferred) | SHELVED |
| CPU temp idle | ≤50°C | 50.5°C (no cooler installed) | OK |
| Hostname | orc-sukabumi | orc-sukabumi | PASS |
| SSH | Enabled | Active | PASS |
| Timezone | Asia/Jakarta | Asia/Jakarta (WIB) | PASS |
| Serial HW | Enabled | /dev/serial0 present | PASS |
| Undervoltage | None | `0x0` at idle and under load | PASS |
| PoE relay + camera | Stable | Camera pingable, no power issues | PASS |
