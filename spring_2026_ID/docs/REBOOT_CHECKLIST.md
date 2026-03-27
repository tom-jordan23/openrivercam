# Post-Reboot Verification Checklist

Run after rebooting the Pi to confirm all services and configurations persist.

## Context: What changed (2026-03-27)

We restored `/etc/udev/rules.d/90-qemu.rules` to preserve the original boot
process from the Rainbow Sensing image. This means:

- `/dev/mmcblk0` is a **symlink to sda** (USB drive), NOT the real SD card
- `/boot/firmware` will NOT mount (the PARTUUID lookup finds the USB drive, not
  the boot partition) — this is the same as the original image behavior
- Cloud-init is disabled (`/etc/cloud/cloud-init.disabled`)
- Root password is set for emergency recovery

**Do NOT remove 90-qemu.rules.** Removing it causes a boot partition enumeration
failure that drops the system into emergency mode. See `BOOT_FAILURE_ANALYSIS.md`.

## Quick Check

```bash
orc-preflight
```

Should show 0 FAILs. Expected WARNs: minicom (optional), orc-capture not enabled
(until service file is deployed to /etc/systemd/system/), sensor hardware not
connected.

## Step-by-Step Verification

### 1. Boot and Root Filesystem

```bash
mount | grep "on / "             # should show ext4 root mounted
uptime                           # confirms clean boot
```

Note: `/boot/firmware` will NOT be mounted. This is expected — see Context above.

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
immediately — see `BOOT_FAILURE_ANALYSIS.md` for details.

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

### 4. USB Storage

```bash
mount | grep /mnt/usb          # should show /dev/sda1 on /mnt/usb type ext4
df -h /mnt/usb                 # should show ~229G
ls -la /home/pi/Videos         # should show: Videos -> /mnt/usb/incoming
ls -la /mnt/usb/incoming/      # should exist, owned by ftpcam
dmesg | grep -i sda | tail -10 # check for I/O errors
```

If not mounted but drive is present (`lsblk | grep sda`), try `sudo mount /mnt/usb`.
Check dmesg for I/O errors — the SanDisk 3.2Gen1 has shown intermittent
offline/reconnect events.

- [ ] USB drive mounted at /mnt/usb (ext4, nofail in fstab)
- [ ] ~/Videos is a symlink to /mnt/usb/incoming
- [ ] No I/O errors in dmesg for sda

### 5. Services

```bash
systemctl is-active vsftpd chrony dnsmasq NetworkManager
systemctl is-enabled orc-gpio-relays
```

- [ ] vsftpd: active
- [ ] chrony: active
- [ ] dnsmasq: active
- [ ] NetworkManager: active
- [ ] orc-gpio-relays: **disabled** (must not be enabled)

### 6. LTE Modem

```bash
mmcli -L                       # should show Quectel EG25-G
lsusb | grep -i 2c7c           # should show Quectel USB device
ls /dev/ttyUSB*                 # should show ttyUSB0-3
```

**Known issue:** The modem has been disconnecting from the USB bus with URB
error storms (`qmi_wwan: nonzero urb status received: -71`). This causes
keyboard input lag while the errors are active. If the modem is gone:

```bash
# Check if modem is on the bus at all
lsusb | grep -i 2c7c
# If missing, try replugging the USB adapter or rebooting
# Check error history
dmesg | grep -c "nonzero urb status"
```

- [ ] Quectel modem detected by ModemManager
- [ ] /dev/ttyUSB0-3 present
- [ ] No URB error storm in dmesg

### 7. Timezone

```bash
timedatectl | grep "Time zone"
```

- [ ] Time zone: Asia/Jakarta (WIB, +0700)

### 8. PoE Relay and Camera

```bash
poe-relay on
# wait ~60s for camera boot
ping -c 1 192.168.50.139
```

- [ ] Relay powers on (GPIO 24 HIGH)
- [ ] Camera reachable after boot

### 9. Camera Configuration (after camera is up)

```bash
curl -s --digest -u admin:<password> \
  http://192.168.50.139/ISAPI/Image/channels/1 | grep supplementLightMode
```

- [ ] Expect `eventIntelligence` (reverts on power cycle — this is the known bug)

### 10. Capture Script (end-to-end test)

```bash
orc-capture --dry-run
```

This will: enforce irLight -> capture 5s -> validate quality gate -> relay off.

- [ ] `Enforcing camera config` line appears
- [ ] `Fixed: supplementLightMode -> irLight` (or "already set" if run twice)
- [ ] Quality gate PASSED (1920x1080, ~16 Mbps, ~5s)
- [ ] Relay OFF after script completes: `poe-relay status`

### 11. FTP Server

```bash
curl -s -T /etc/hostname ftp://ftpcam:<password>@127.0.0.1/reboot_test.txt
ls /mnt/usb/incoming/reboot_test.txt
sudo rm /mnt/usb/incoming/reboot_test.txt
```

- [ ] FTP upload succeeds
- [ ] File appears in /mnt/usb/incoming/

### 12. NTP for Camera

```bash
chronyc clients | head -5
```

- [ ] chrony is serving time (camera IP should appear as client after boot)

### 13. Git Status (no unintended changes)

```bash
cd ~/code/git/openrivercam && git status --short
```

- [ ] No unexpected modifications (working tree matches pre-reboot state)
