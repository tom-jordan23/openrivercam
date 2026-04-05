# Known Issues - Sukabumi Build

Document issues encountered during build. Update checklist if process changes needed.

---

## Open Issues

### Issue #1: Samsung FIT Plus USB drive causes UAS boot storm

**Phase:** 4 (Initial Boot Test)
**Date Found:** 2026-03-28
**Severity:** Blocking
**Status:** Deferred — deploying without USB drive

#### Symptoms

228 USB disconnects and 158 URB errors in 12 minutes at boot. Modem dropped
off bus entirely. All USB devices affected by cascading re-enumeration.

#### Root Cause

Samsung FIT Plus (0781:5583) uses the UAS driver, which repeatedly crashes and
re-enumerates during boot. Both `uas` and `usb-storage` are kernel built-ins,
so `modprobe.d` quirks are ignored. The only fix is a `cmdline.txt` kernel
parameter (`usb-storage.quirks=0781:5583:u`).

#### Resolution

Drive removed from build. Captures stored on SD card rootfs (~43GB free).
USB bus is clean and stable without the drive. See `docs/USB_POWER_TEST_CHECKLIST.md`
for full investigation.

#### Prevention

For future builds: add `usb-storage.quirks=0781:5583:u` to `cmdline.txt` before
first boot, or select a USB drive that does not use UAS.

### Issue #2: I2C bus 1 not enabled

**Phase:** 4 (Initial Boot Test)
**Date Found:** 2026-03-28
**Severity:** Minor
**Status:** Open

#### Symptoms

`dtparam=i2c_arm=on` is commented out in `/boot/firmware/config.txt`.
`/dev/i2c-1` does not exist. Only system I2C buses (13, 14) are present.

#### Impact

Not currently blocking capture pipeline, but SHT40 temp/humidity sensor is
in the BOM (item SENSOR-TH) and requires I2C bus 1. Enable before deployment
or SHT40 will not be detected.

---

## Resolved Issues

### Issue #3: orc-capture cannot deliver to ~/Videos (permission denied)

**Phase:** Capture testing
**Date Found:** 2026-03-28
**Severity:** Blocking
**Status:** Resolved (obsolete — FTP setup removed)

#### Symptoms

`mv: cannot create regular file '/home/pi/Videos/video_*.mp4': Permission denied`

`~/Videos` symlinked to `/mnt/usb/incoming/` which was owned by `ftpcam:ftpcam`.

#### Root Cause

Permission conflict between `ftpcam` (FTP upload user) and `pi` (capture user).

#### Resolution

This issue is now moot. The FTP-based capture pipeline was removed (see ISS-003).
Video capture uses RTSP pull via `orc-capture`, and files are delivered directly
to `/home/pi/Videos` which is owned by `pi`. No `ftpcam` user or vsftpd needed.

---

## Issue Template

Copy and fill in for each new issue:

```markdown
## Issue #X: [Brief description]

**Phase:**
**Date Found:** YYYY-MM-DD
**Severity:** Blocking / Major / Minor
**Status:** Open / Investigating / Resolved

### Symptoms

[What was observed - be specific]

### Expected Behavior

[What should have happened]

### Investigation

[Steps taken to diagnose]

### Root Cause

[Why it happened]

### Resolution

[What fixed it]

### Prevention

[How to avoid in future builds]

### Checklist Updates

[Any changes needed to build_checklist.md]
```

---

## Issue Details

*(Add issues below as encountered)*
