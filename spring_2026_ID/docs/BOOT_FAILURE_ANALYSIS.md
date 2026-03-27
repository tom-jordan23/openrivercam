# Boot Failure Analysis — 2026-03-27

## Symptom

After rebooting the Pi (following removal of QEMU udev rules and USB drive
troubleshooting), the system dropped into emergency mode with the message that
the root account was locked and a console could not be opened.

## Timeline

| Time (WIB) | Event |
|-------------|-------|
| ~13:46 | Claude session on Pi: removed 90-qemu.rules, recreated mmcblk0/mmcblk0p1 device nodes with mknod, mounted /boot/firmware manually, updated preflight and REBOOT_CHECKLIST |
| 17:59 | Boot 1 — **succeeded**. All services started, USB mounted, cloud-init completed. But /boot/firmware mount status is unclear (not logged). |
| 18:46 | Boot 2 — **failed**. systemd-fsck immediately fails for PARTUUID=5264e4c7-01, boot-firmware.mount fails, local-fs.target fails. Cloud-init stalls. System enters emergency mode. |
| 18:49 | Boot 3 — **failed**. Same as boot 2. Emergency shell started but root account locked, no console available. |

## Root Cause (layered)

There are three interacting problems:

### 1. QEMU udev rules masked a long-standing boot partition issue

The image was built in QEMU, which added `/etc/udev/rules.d/90-qemu.rules`:

```
KERNEL=="sda", SYMLINK+="mmcblk0"
KERNEL=="sda?", SYMLINK+="mmcblk0p%n"
```

This mapped the USB drive (sda) to appear as mmcblk0. On real Pi hardware, the
actual SD card is also mmcblk0 (major:minor 179:0). The result was device name
confusion: `blkid` showed mmcblk0p1 as the USB drive (ext4, orc-data) rather
than the real boot partition (vfat, bootfs).

**With QEMU rules active, /boot/firmware was NEVER mounting successfully** — but
the system booted fine because no critical service depended on it. This is
confirmed by checking boot.log.2 through boot.log.4: none show boot-firmware
mounting or failing.

The previous Claude session correctly identified and removed 90-qemu.rules, then
manually recreated the real device nodes:

```bash
sudo rm /dev/mmcblk0 /dev/mmcblk0p1
sudo mknod /dev/mmcblk0 b 179 0
sudo mknod /dev/mmcblk0p1 b 179 1
sudo udevadm trigger
sudo mount /boot/firmware
```

After this fix, `blkid -p /dev/mmcblk0p1` correctly showed:

```
/dev/mmcblk0p1: LABEL_FATBOOT="bootfs" LABEL="bootfs" UUID="016C-FDB7"
  TYPE="vfat" PART_ENTRY_DISK="179:0" PART_ENTRY_UUID="5264e4c7-01"
```

And `/dev/disk/by-partuuid/5264e4c7-01 -> ../../mmcblk0p1` was created.

### 2. Manual mknod nodes don't survive reboot

The `mknod` fix created block device nodes on devtmpfs, which is a RAM
filesystem. On reboot, devtmpfs is recreated fresh and udev repopulates it from
kernel device events.

After the QEMU rules were removed, the kernel needed to enumerate the SD card
partitions through its MMC driver. On the Pi 5 (BCM2712), there appears to be a
timing issue where:

- The **initramfs** finds PARTUUID=5264e4c7-02 (root) and mounts it successfully
- But after pivot_root, when **systemd** starts and udev runs, the boot partition
  (PARTUUID=5264e4c7-01) is not yet available or not being probed
- systemd-fstab-generator creates a mount unit for /boot/firmware from fstab
- The mount unit waits up to 90 seconds for the PARTUUID device to appear
- It never appears → mount fails → local-fs.target fails → emergency mode

**Evidence:** The second boot (18:46) shows the fsck failure for PARTUUID-01
as the very first event after e2fsck runs on root — it fails immediately, not
after a timeout. This suggests the device simply doesn't exist in
`/dev/disk/by-partuuid/` at all.

### 3. Fstab entry for /boot/firmware lacks nofail

```
PARTUUID=5264e4c7-01  /boot/firmware  vfat    defaults          0       2
```

This is the default Raspberry Pi OS fstab entry. With just `defaults`, a mount
failure is **fatal** — it fails `local-fs.target`, which triggers emergency mode.

The USB drive entry correctly has `nofail`:

```
UUID=80c40680-0ed7-4075-8497-f05e71fb23a7  /mnt/usb  ext4  defaults,noatime,nofail  0  2
```

### 4. Root account locked (prevents emergency recovery)

`/etc/shadow` shows `root:*:...` — the account is locked (standard Raspberry Pi
OS). When emergency mode starts, `sulogin` tries to open a root console but
can't because there's no valid root password. Result: no way to fix anything
from the Pi itself.

### 5. Cloud-init causes boot delays

Cloud-init is configured with `seedfrom: file:///boot/firmware` (in
`/etc/cloud/cloud.cfg.d/99_raspberry-pi.cfg`). When /boot/firmware isn't
mounted, cloud-init stalls trying to read its datasource. This is what was
observed as "cloud-init stuck for a while" before emergency mode.

Cloud-init's status.json confirms the failure:

```json
"init": {
  "recoverable_errors": {
    "WARNING": [
      "Getting data from DataSourceNoCloud failed",
      "DataSourceNoCloudNet only uses seeds starting with http/https/ftp
       — file:///boot/firmware is not valid."
    ]
  }
}
```

## What was fixed (from init=/bin/bash recovery)

1. **Added `nofail,x-systemd.device-timeout=30`** to the /boot/firmware fstab
   entry. This means: try to mount it, wait up to 30 seconds, but if it fails,
   continue booting normally.

2. **Set root password** to `orc-emergency` via `chpasswd`. If emergency mode
   ever triggers again, you'll be able to get a shell. **Change this after
   deployment.**

3. **Disabled cloud-init** by touching `/etc/cloud/cloud-init.disabled`. The
   image is fully configured — cloud-init has nothing left to do and only causes
   boot delays when /boot/firmware is unavailable.

4. **Restored cmdline.txt** to the normal boot line (removed `init=/bin/bash`).

## Still unresolved: /boot/firmware not mounting

The fstab fix prevents emergency mode, but `/boot/firmware` is still not
mounting automatically. The boot partition (PARTUUID=5264e4c7-01) is not being
found by udev/systemd even though the root partition (PARTUUID=5264e4c7-02,
same disk) boots fine.

### Diagnostic steps

```bash
# What block devices does the kernel see?
lsblk
ls /dev/mmcblk0*

# Are PARTUUID symlinks created?
ls -la /dev/disk/by-partuuid/

# What does blkid report?
sudo blkid

# Does manual mount work by device path?
sudo mount /dev/mmcblk0p1 /boot/firmware

# If mmcblk0p1 doesn't exist, recreate and mount:
sudo mknod /dev/mmcblk0p1 b 179 1
sudo mount /dev/mmcblk0p1 /boot/firmware
```

### Potential permanent fixes

1. **Switch fstab from PARTUUID to device path:**
   ```
   /dev/mmcblk0p1  /boot/firmware  vfat  defaults,nofail  0  2
   ```
   Less portable but avoids the PARTUUID lookup race.

2. **Add a udev rule** to ensure mmcblk0p1 is created:
   ```
   # /etc/udev/rules.d/99-fix-mmcblk0p1.rules
   KERNEL=="mmcblk0", RUN+="/sbin/partprobe /dev/mmcblk0"
   ```

3. **Add a systemd service** that mounts /boot/firmware after boot:
   ```ini
   [Unit]
   Description=Mount boot firmware partition
   After=local-fs.target

   [Service]
   Type=oneshot
   ExecStartPre=/bin/sleep 5
   ExecStart=/bin/mount /boot/firmware
   RemainAfterExit=yes

   [Install]
   WantedBy=multi-user.target
   ```

4. **Regenerate initramfs** to ensure proper MMC module loading:
   ```bash
   sudo update-initramfs -u
   ```

## Other known issues from previous session

- **USB drive is a SanDisk 3.2Gen1**, not the Samsung FIT Plus from the BOM.
  dmesg showed I/O errors and device offline events. Monitor with
  `dmesg | grep -i sda`.
- **LTE modem disconnected** during a previous boot (Quectel ttyUSB0-3
  disconnected in dmesg). May need USB replug.
- **orc-capture service** not yet enabled (pending deployment).

## Key lesson for image building

When building Pi images in QEMU, the QEMU udev rules that map device names
**must be removed before the final image is written to SD card**. The image
build pipeline should include a cleanup step that:

1. Removes `/etc/udev/rules.d/90-qemu.rules`
2. Adds `nofail` to the /boot/firmware fstab entry (defensive)
3. Disables cloud-init if it won't be needed on real hardware
4. Sets a root password for emergency recovery
