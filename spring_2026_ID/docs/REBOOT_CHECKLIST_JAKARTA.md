# Post-Reboot Verification Checklist — Jakarta

Run after rebooting the Jakarta Pi to confirm deploy.sh changes took effect.

## Context

- **Site:** Jakarta (AC power, RELAY_MODE=always)
- **Image:** ORC-OS on Debian trixie, Pi 5 8GB
- **Hostname:** orc-jakarta
- **Camera:** ANNKE C1200 at 192.168.50.101
- **QEMU rules:** `/etc/udev/rules.d/90-qemu.rules` present (required for boot — do NOT remove)
- **Boot partition:** `/boot/firmware` mounts normally on this image (unlike Sukabumi)
- **USB drive:** None — captures go to SD card (~46GB free)

See `REBOOT_CHECKLIST.md` for the original Sukabumi checklist and detailed
background on QEMU rules, USB drive deferral, and timezone requirements.

## Quick Check

```bash
orc-preflight
```

**Target:** 0 FAILs. Expected WARNs after fresh deploy (before hardware is connected):
- `/mnt/usb` not mounted (no USB drive — by design)
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

### 2. config.txt Changes (applied by deploy.sh, need reboot)

```bash
grep -E "i2c_arm|bbat|enable_uart" /boot/firmware/config.txt
```

Expected (uncommented, at end of file):
```
dtparam=rtc_bbat_vchg=3000000
enable_uart=1
dtparam=i2c_arm=on
```

```bash
ls /dev/i2c-1                    # I2C bus enabled
ls /dev/ttyAMA0                  # UART enabled for rain gauge
```

- [ ] `dtparam=i2c_arm=on` present (uncommented)
- [ ] `dtparam=rtc_bbat_vchg=3000000` present
- [ ] `enable_uart=1` present
- [ ] `/dev/i2c-1` exists
- [ ] `/dev/ttyAMA0` exists

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
