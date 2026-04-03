# Post-Reboot Verification Checklist

Run after rebooting the Pi to confirm all services and configurations persist.

## Context

This Pi runs a Rainbow Sensing image with `/etc/udev/rules.d/90-qemu.rules`
that symlinks `sda → mmcblk0`. This is **required for boot** — removing it
causes a PARTUUID lookup failure that drops into emergency mode. See
`BOOT_FAILURE_ANALYSIS.md`.

Consequences of 90-qemu.rules:
- `/boot/firmware` will NOT mount (PARTUUID points to USB drive, not SD boot)
- Cloud-init is disabled (`/etc/cloud/cloud-init.disabled`)
- Root password is set for emergency recovery

**Do NOT remove 90-qemu.rules.**

## Quick Check

```bash
orc-preflight
```

Should show **0 FAILs**. Expected WARNs:
- minicom not installed (optional)
- `/boot/firmware` not mounted (expected with 90-qemu.rules)
- `config.txt` not accessible (same reason)
- orc-capture service not enabled (until deployed to systemd)
- orc-sensors.timer not enabled (until deployed to systemd)
- SHT40 sensor not detected at 0x44 (if sensor hardware not connected)

## Step-by-Step Verification

### 1. Boot and Root Filesystem

```bash
mount | grep "on / "             # should show ext4 root mounted
uptime                           # confirms clean boot
```

- [ ] Root filesystem mounted (ext4)
- [ ] System booted without emergency mode

### 2. QEMU udev Rules (must exist)

```bash
cat /etc/udev/rules.d/90-qemu.rules
```

Should show:
```
KERNEL=="sda", SYMLINK+="mmcblk0"
KERNEL=="sda?", SYMLINK+="mmcblk0p%n"
```

**If this file is missing, the system may not survive a reboot.** Restore it
immediately — see `BOOT_FAILURE_ANALYSIS.md`.

- [ ] 90-qemu.rules exists with correct contents

### 3. CPU and Memory

```bash
uptime                         # load averages should be < 2.0
free -h                        # used RAM should be well under total (8GB)
vcgencmd measure_temp          # should be < 70°C (throttles at 80°C)
vcgencmd get_throttled         # should be 0x0 (no throttling)
```

If `get_throttled` is non-zero, decode with:
- `0x1` = under-voltage detected
- `0x2` = arm frequency capped
- `0x4` = currently throttled
- `0x50000` = throttling has occurred since boot

- [ ] Load average < 2.0
- [ ] RAM usage reasonable (< 50% at idle)
- [ ] CPU temp < 70C
- [ ] No throttling (0x0)

### 4. I2C Bus and RTC

```bash
ls /dev/i2c-1                  # should exist (I2C enabled in config.txt)
i2cdetect -y 1                 # look for 0x44 (SHT40) and 0x68 (RTC)
timedatectl                    # RTC time should match system time
cat /boot/firmware/config.txt | grep -E "i2c_arm|bbat"
```

Expected config.txt entries:
- `dtparam=i2c_arm=on` — enables I2C bus 1 on GPIO 2/3
- `dtparam=rtc_bbat_vchg=3000000` — trickle-charges RTC backup battery at 3V
- `usb_max_current_enable=1` — raises USB current limit (required when powering Pi via 5V GPIO rail)

- [ ] `/dev/i2c-1` exists
- [ ] RTC battery charging enabled (`rtc_bbat_vchg=3000000`)
- [ ] SHT40 sensor at 0x44 (if connected)
- [ ] RTC time correct
- [ ] If SHT40 connected: `orc-sensors` returns readings and appends to CSV

### 5. USB Storage — DEFERRED

**Status (2026-03-28):** Samsung FIT Plus 256GB is **removed from the build**.
The UAS (USB Attached SCSI) driver causes boot-time enumeration storms that
crash the entire USB bus (modem, keyboard, mouse all disconnect-cycle). Both
`uas` and `usb-storage` are kernel built-ins, so the fix requires adding
`usb-storage.quirks=0781:5583:u` to `cmdline.txt` — which is inaccessible
while 90-qemu.rules is active. See `USB_POWER_TEST_CHECKLIST.md` for full
root cause analysis.

**Deploy without the USB drive.** Captures go to SD card rootfs (~43GB free).

**Do NOT re-insert the Samsung FIT** until the cmdline.txt fix is applied.

- [x] USB drive removed (intentional — not a failure)

### 6. Services

```bash
systemctl is-active chrony dnsmasq NetworkManager
systemctl list-timers orc-sensors.timer
```

- [ ] chrony: active
- [ ] dnsmasq: active
- [ ] NetworkManager: active
- [ ] orc-sensors.timer: active (next activation shown)

> **Note:** vsftpd is not used. Video capture is via RTSP pull (`orc-capture`),
> not camera FTP push. See ISS-003 in ISSUE_LOG.md.

### 7. LTE Modem

```bash
mmcli -L                       # should show Quectel EG25-G
lsusb | grep -i 2c7c           # should show Quectel USB device
ls /dev/ttyUSB*                 # should show ttyUSB0-3
```

**Known issue:** The modem has been disconnecting from the USB bus with URB
error storms (`qmi_wwan: nonzero urb status received: -71`). This causes
keyboard input lag while the errors are active. If the modem is gone:

```bash
lsusb | grep -i 2c7c
# If missing, try replugging the USB adapter or rebooting
dmesg | grep -c "nonzero urb status"
```

- [ ] Quectel modem detected by ModemManager
- [ ] /dev/ttyUSB0-3 present
- [ ] No URB error storm in dmesg

### 8. Timezone

> **WARNING: Do NOT change the timezone from UTC.** The Rainbow Sensing image
> ships with GMT0/UTC as the default. If the timezone is changed to a regional
> zone (e.g. `Asia/Jakarta`), the ORC API passes the abbreviation (e.g. "WIB")
> to the frontend via `Intl.DateTimeFormat`. Browsers do not recognize these
> abbreviations and the frontend crashes with a white screen.

```bash
timedatectl | grep "Time zone"
```

- [ ] Time zone: Etc/UTC (UTC, +0000)

**If timezone is NOT UTC**, fix with:
```bash
sudo timedatectl set-timezone UTC
```
Then reboot or restart orc-api (`sudo systemctl restart orc-api`).

### 9. PoE Relay and Camera

```bash
poe-relay on
# wait ~60s for camera boot
ping -c 1 192.168.50.139
```

- [ ] Relay powers on (GPIO 24 HIGH)
- [ ] Camera reachable after boot

### 10. Camera Configuration (after camera is up)

The ANNKE C1200 may revert `supplementLightMode` to `eventIntelligence` on
power cycle (white LED flashes at night). `orc-capture` enforces `irLight`
on every cycle, so this is self-healing.

```bash
# Credentials in ~/.orc_deploy_sukabumi (BASE_PASSWD)
source ~/.orc_deploy_sukabumi
curl -s --digest -u "admin:${BASE_PASSWD}" \
  http://192.168.50.139/ISAPI/Image/channels/1 | grep supplementLightMode
```

- [ ] supplementLightMode is `irLight` or `eventIntelligence` (orc-capture fixes this)

### 11. Capture Script (end-to-end test)

```bash
orc-capture --skip-relay --dry-run
```

This will: enforce irLight, capture 5s via RTSP, validate quality gate.
Uses `--skip-relay` since relay is already on from step 8.

- [ ] `Enforcing camera config` line appears
- [ ] `Fixed: supplementLightMode -> irLight` (or "already set")
- [ ] Quality gate PASSED (1920x1080, ~15 Mbps, ~5s)

Then power off:
```bash
poe-relay off
```

- [ ] Relay OFF after test

### 12. NTP for Camera

```bash
sudo chronyc clients | head -5
```

Camera IP (192.168.50.139) should appear as a client if it has been powered
on long enough to make an NTP request. If only `localhost` appears, that's
OK — chrony is serving, camera just hasn't queried yet.

- [ ] chrony is running and configured to serve 192.168.50.0/24
