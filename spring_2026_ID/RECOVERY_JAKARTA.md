# Jakarta Station Recovery Guide

**For PMI field staff rebuilding the Jakarta ORC station from scratch.**

This USB drive contains everything needed to restore the Jakarta station
if the SD card fails or the Pi needs to be replaced.

---

## What's on this drive

| Item | Description |
|------|-------------|
| `orc-os-jakarta.img.gz` | Compressed SD card image (flash with Pi Imager) |
| `openrivercam/` | Full repo with deploy.sh, overlays, camera profiles, docs |
| `camera_profiles/` | Camera XML profiles for camtool.py |
| `RECOVERY_JAKARTA.md` | This file |

---

## Recovery Steps

### 1. Flash the SD card

Use Raspberry Pi Imager (or `dd`) to write the image to a 64GB+ SD card.

**With Pi Imager:**
1. Download and install Pi Imager on a laptop
2. Choose OS → "Use custom" → select `orc-os-jakarta.img.gz`
3. Choose Storage → select the SD card
4. **Do NOT change any settings** (hostname, WiFi, SSH are already configured)
5. Write and wait for verification

**With dd (Linux/macOS):**
```bash
gunzip -c orc-os-jakarta.img.gz | sudo dd of=/dev/sdX bs=4M status=progress
sync
```

### 2. First boot

1. Insert SD card into Pi 5
2. Insert the SanDisk 250GB USB data drive (blue USB 3.0 port)
3. Connect ethernet to PoE switch
4. Apply AC power
5. Wait 2-3 minutes for boot

The station should come up automatically with all services running.

### 3. Verify

SSH into the Pi (connect laptop to the maintenance WiFi hotspot, or use
Tailscale if available):

```bash
ssh pi@orc-jakarta.local
# or
ssh pi@100.84.178.72    # Tailscale IP
```

Run the preflight check:
```bash
orc-preflight
```

**Target:** 0 FAILs. See `docs/REBOOT_CHECKLIST_JAKARTA.md` for detailed checks.

### 4. If starting from a fresh ORC-OS image (not our backup)

If the backup image is unavailable and you're starting from a stock ORC-OS
image from Hessel:

1. Flash the stock ORC-OS image
2. Boot and wait for first-boot expansion (auto-reboots once)
3. SSH in and clone or copy this repo:
   ```bash
   # Copy from this USB drive:
   sudo mount /dev/sda1 /mnt
   cp -r /mnt/openrivercam ~/code/git/openrivercam
   sudo umount /mnt
   ```
4. Insert the SanDisk data drive and run deploy:
   ```bash
   cd ~/code/git/openrivercam/spring_2026_ID/pi
   bash deploy.sh jakarta
   ```
5. Set camera credentials:
   ```bash
   echo 'BASE_PASSWD=<ask tjordan for password>' > ~/.orc_deploy_jakarta
   ```
6. Apply the UAS fix (if not already in the image):
   ```bash
   # Check if quirk is present:
   cat /boot/firmware/cmdline.txt | grep -o 'usb-storage.quirks=[^ ]*'

   # If missing, append it:
   sudo sed -i 's/$/ usb-storage.quirks=0781:5583:u/' /boot/firmware/cmdline.txt
   ```
7. Reboot and verify:
   ```bash
   sudo reboot
   # After reboot:
   orc-preflight
   ```

### 5. Camera configuration

If the camera has been factory-reset:

```bash
# Set camera password first (via camera's web UI or ISAPI)
# Then push config profiles:
camtool.py --password '<camera-password>' push jakarta-cam1
```

---

## Important Notes

- **Timezone must be UTC** — do NOT change it. The ORC API will crash.
- **Do NOT remove `/etc/udev/rules.d/90-qemu.rules`** — the Pi won't boot without it.
- **USB drive uses `nofail`** — if the data drive is missing, the Pi still boots but captures will fail (symlink points to nothing).
- **Backout scripts** are at `/home/pi/uas-revert.sh` and `/home/pi/usb-video-revert.sh`.

---

## Support

- **tjordan** — station builder, remote support
- **Hessel** — ORC-OS software
- Repo: this USB drive or the remote git origin
