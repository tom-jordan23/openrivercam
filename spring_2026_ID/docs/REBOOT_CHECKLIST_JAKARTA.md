# Post-Reboot Verification Checklist — Jakarta

Run after rebooting the Jakarta Pi to confirm deploy.sh changes took effect.

## Context

- **Site:** Jakarta (AC power, RELAY_MODE=always)
- **Image:** ORC-OS on Debian trixie, Pi 5 8GB
- **Hostname:** orc-jakarta
- **Camera:** ANNKE C1200 at 192.168.50.101
- **QEMU rules:** `/etc/udev/rules.d/90-qemu.rules` present (required for boot — do NOT remove)
- **Boot partition:** `/boot/firmware` mounts normally on this image (unlike Sukabumi)
- **USB drive:** SanDisk 3.2Gen1 250GB at `/mnt/usb` (UAS disabled via cmdline.txt quirk)

See `REBOOT_CHECKLIST.md` for the original Sukabumi checklist and detailed
background on QEMU rules, USB drive deferral, and timezone requirements.

## Quick Check

```bash
orc-preflight
```

**Target:** 0 FAILs. Expected WARNs after fresh deploy (before hardware is connected):
- eth0 no IP / PoE relay OFF (if camera not yet wired)
- DS18B20 not detected (if not connected)
- `/etc/hosts` missing camera hostname
- Sensor log directory not yet created (created on first orc-sensors run)

## Step-by-Step

### 1. Clean Boot

```bash
uptime                           # confirms clean boot, no emergency mode
mount | grep "on / "             # ext4 root mounted
mount | grep boot/firmware       # should be mounted (unlike Sukabumi)
```

- [ ] System booted without emergency mode
- [ ] Root filesystem mounted
- [ ] `/boot/firmware` mounted

### 1b. USB Storage

```bash
mount | grep /mnt/usb            # ext4 on /dev/sda1
ls -la /home/pi/Videos           # symlink -> /mnt/usb/incoming
df -h /mnt/usb                   # ~217GB free
dmesg | grep -i "UAS is ignored" # quirk active
```

- [ ] `/mnt/usb` mounted (SanDisk USB drive)
- [ ] `/home/pi/Videos` is symlink to `/mnt/usb/incoming`
- [ ] UAS disabled (using usb-storage instead)
- [ ] No USB enumeration storms in `dmesg`

> **If USB drive fails to mount:** fstab has `nofail` so boot continues.
> Captures will fail (symlink points to nothing). Check `dmesg` for USB errors.
> Backout: `sudo bash ~/usb-video-revert.sh` restores local SD card storage.
> UAS backout: `sudo bash ~/uas-revert.sh` removes the cmdline.txt quirk.

### 2. config.txt Changes (applied by deploy.sh, need reboot)

```bash
grep -E "i2c_arm|bbat|enable_uart|usb_max_current" /boot/firmware/config.txt
```

Expected (uncommented, at end of file):
```
enable_uart=1
dtparam=i2c_arm=on
usb_max_current_enable=1
```

(Note: `dtparam=rtc_bbat_vchg` is NOT needed — Witty Pi 5 HAT+ provides RTC with CR2032 backup)

```bash
ls /dev/i2c-1                    # I2C bus enabled
ls /dev/ttyAMA0                  # UART enabled for rain gauge
i2cdetect -y 1 | grep -E "44|51" # SHT40 (0x44) + Witty Pi 5 (0x51)
systemctl is-active wp5d         # Witty Pi 5 daemon running
```

- [ ] `dtparam=i2c_arm=on` present (uncommented)
- [ ] `enable_uart=1` present
- [ ] `usb_max_current_enable=1` present (required — Pi powered via 5V GPIO rail, no USB-C PD)
- [ ] `/dev/i2c-1` exists
- [ ] `/dev/ttyAMA0` exists
- [ ] Witty Pi 5 detected at I2C 0x51
- [ ] `wp5d` daemon active
- [ ] Witty Pi 5 RTC time correct (check via `wp5`)

### 3. System Config

```bash
timedatectl | grep "Time zone"   # must be UTC
cat /etc/fstab | grep boot/firmware  # must have nofail
ls /etc/cloud/cloud-init.disabled    # must exist
```

- [ ] Timezone: Etc/UTC
- [ ] Fstab `/boot/firmware` has `nofail`
- [ ] Cloud-init disabled

> **WARNING: Do NOT change timezone from UTC.** See REBOOT_CHECKLIST.md §8 for
> why — the ORC API frontend crashes with non-UTC timezone abbreviations.

### 4. CPU and Thermals

```bash
uptime                           # load < 2.0
free -h                          # RAM < 50% at idle
vcgencmd measure_temp            # < 70°C
vcgencmd get_throttled           # 0x0 = no throttling
```

- [ ] Load average < 2.0
- [ ] RAM reasonable
- [ ] CPU temp < 70°C
- [ ] No throttling (0x0)

### 5. Services

```bash
systemctl is-active dnsmasq chrony NetworkManager orc-led-status
systemctl is-enabled orc-capture orc-sensors.timer orc-boot-usb-log
systemctl is-enabled orc-gpio-relays
systemctl list-timers orc-sensors.timer
```

- [ ] dnsmasq: active
- [ ] chrony: active
- [ ] NetworkManager: active
- [ ] orc-led-status: active (running)
- [ ] orc-capture: enabled
- [ ] orc-sensors.timer: enabled, next activation shown
- [ ] orc-boot-usb-log: enabled
- [ ] orc-gpio-relays: **disabled** (active-low, incompatible with our relay)

### 6. LTE Modem

```bash
mmcli -L                         # should show Quectel EG25-G
lsusb | grep -i 2c7c            # Quectel USB device
ls /dev/ttyUSB*                  # ttyUSB0-3
dmesg | grep -c "nonzero urb"   # should be 0 or very low
```

- [ ] Modem detected by ModemManager
- [ ] `/dev/ttyUSB0-3` present
- [ ] No URB error storm in dmesg

### 7. I2C Devices

```bash
i2cdetect -y 1                   # scan bus
```

Expected addresses:
- `0x44` — SHT40 temperature/humidity sensor (if connected)
- `0x68` — RTC (DS3231 on Witty Pi 5)

- [ ] I2C bus responds
- [ ] RTC at 0x68 (if Witty Pi installed)
- [ ] SHT40 at 0x44 (if connected)

### 8. Network (camera-net)

```bash
nmcli connection show            # camera-net should be listed
ip addr show eth0                # 192.168.50.1/24 when camera connected
```

- [ ] camera-net NM connection loaded
- [ ] eth0 configured for 192.168.50.0/24 (may be DOWN if camera not wired)

### 9. PoE Relay and Camera

Jakarta uses `RELAY_MODE=always` — relay stays on permanently.

```bash
poe-relay on                     # energize relay
# wait ~60s for camera boot
ping -c 3 192.168.50.101        # Jakarta camera IP
```

- [ ] Relay energizes (GPIO 24 HIGH)
- [ ] Camera reachable at 192.168.50.101 after boot

### 10. Capture Test (after camera is configured)

> **Skip this section until the camera password is set on the camera itself.**
> The camera is factory-fresh — configure it first via camtool.py.

```bash
orc-capture --skip-relay --dry-run
```

- [ ] Camera config enforced (supplementLightMode → irLight)
- [ ] RTSP capture succeeds
- [ ] Quality gate PASSED (1920x1080, ~15 Mbps, ~5s)

### 11. NTP for Camera

```bash
chronyc clients | head -5
```

Camera IP (192.168.50.101) should appear once it has been powered long
enough to query NTP. If only localhost appears, chrony is serving — camera
just hasn't queried yet.

- [ ] chrony running and serving 192.168.50.0/24

### 12. Power Management (Witty Pi 5 + ORC-OS)

Power management uses a split responsibility model:

- **Witty Pi 5** owns the wake/startup schedule (configured interactively via `wp5`)
- **ORC-OS** owns shutdown decisions (`shutdown_after_task`, `reboot_after`)
- **systemd ordering** ensures `wp5d` sets the system clock before ORC-OS starts,
  preventing the `reboot_after` watchdog from triggering prematurely due to a
  time jump

```bash
# Verify orc-api starts after wp5d (prevents time-jump reboot loop)
grep "wp5d" /etc/systemd/system/orc-api.service

# Check ORC-OS reboot_after setting (seconds; 0 or NULL = disabled)
python3 -c "
import sqlite3
conn = sqlite3.connect('/home/pi/.ORC-OS/orc-os.db')
c = conn.cursor()
c.execute('SELECT reboot_after, shutdown_after_task, active FROM settings')
print('reboot_after, shutdown_after_task, active:', c.fetchone())
"

# Check Witty Pi 5 status and schedule (interactive)
wp5
```

- [ ] `orc-api.service` has `After=... wp5d.service`
- [ ] ORC-OS `reboot_after` set appropriately (86400 = 24hr watchdog, or 0 to disable)
- [ ] Witty Pi 5 startup schedule configured (if duty-cycling)

#### Duty-Cycle Stations

For stations that power-cycle (solar or battery), configure the Witty Pi 5
wake schedule via the interactive `wp5` tool:

1. Run `wp5` (interactive menu)
2. Option 6 → Choose schedule script (for repeating on/off cycles)
3. Or Option 5 → Schedule next startup (for one-time wake)

ORC-OS handles shutdown via `shutdown_after_task=true` in daemon settings.
The Witty Pi 5 schedule brings the Pi back at the next interval.

#### AC-Powered Stations (Jakarta)

For always-on stations, the Witty Pi 5 "default state when powered" should be
ON (this is the factory default). ORC-OS `reboot_after` serves as a watchdog
to recover from hangs. No Witty Pi schedule script is needed unless the station
is later redeployed as a duty-cycle site.
