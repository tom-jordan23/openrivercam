# orc-capture — Video Capture Pipeline

**Version:** 1.0 — April 2026
**Location:** `/usr/local/bin/orc-capture`
**Config:** `/etc/orc-capture.conf`
**Source:** `pi/shared/usr/local/bin/orc-capture`

---

## Contents

- [What It Does](#what-it-does)
- [How It Runs](#how-it-runs)
- [Capture Pipeline](#capture-pipeline)
- [Relay Modes](#relay-modes)
- [Quality Gate](#quality-gate)
- [Camera Config Enforcement](#camera-config-enforcement)
- [Maintenance Mode](#maintenance-mode)
- [Configuration Reference](#configuration-reference)
- [Credentials](#credentials)
- [Filename Format](#filename-format)
- [Command Line Usage](#command-line-usage)
- [Troubleshooting](#troubleshooting)
- [Extending orc-capture](#extending-orc-capture)

---

## What It Does

orc-capture is the core video capture script for the ORC stations. On each
run, it:

1. Controls the PoE relay to power the camera
2. Waits for the camera to boot and become reachable
3. Re-applies critical camera settings that revert after power cycles
4. Captures a 5-second video via RTSP
5. Validates the video against a quality gate (resolution, bitrate, duration, frame count)
6. Delivers the passing video to ORC-OS for processing

If a capture fails the quality gate, it retries up to 3 times before giving up.

## How It Runs

orc-capture is triggered by a systemd timer that runs every 15 minutes.
It is a **oneshot** service — it runs, completes, and exits. It does not
run as a long-lived daemon.

```
orc-capture.timer (every 15 min)
  → orc-capture.service (oneshot)
    → /usr/local/bin/orc-capture
```

On Sukabumi (duty-cycled), orc-capture runs once per wake cycle. The Witty Pi
wakes the Pi, orc-capture runs, ORC-OS processes the video and shuts down.

On Jakarta (always-on), orc-capture runs every 15 minutes continuously.

---

## Capture Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                     orc-capture pipeline                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. MAINTENANCE CHECK                                        │
│     Is /run/orc-maintenance-mode present?                    │
│     Yes → skip capture, exit 0                               │
│     No  → continue                                           │
│                                                              │
│  2. LOAD CONFIG                                              │
│     Source /etc/orc-capture.conf                             │
│     Load camera credentials from ~/.orc_deploy_*            │
│                                                              │
│  3. RELAY ON                                                 │
│     cycle mode: power on PoE relay (GPIO 24 HIGH)           │
│     always mode: assert relay on (stays on after capture)    │
│     --skip-relay: do nothing (camera already powered)        │
│                                                              │
│  4. WAIT FOR CAMERA                                          │
│     Ping camera IP every 2 seconds                           │
│     Timeout: 90 seconds (configurable)                       │
│     After first ping: settle 15 seconds (camera stabilize)   │
│                                                              │
│  5. ENFORCE CAMERA CONFIG                                    │
│     Check supplementLightMode via ISAPI — fix if wrong       │
│     Check OSD overlays via ISAPI — disable if enabled        │
│     (ANNKE C1200 settings can revert after power cycle)      │
│                                                              │
│  6. CAPTURE VIDEO                                            │
│     ffmpeg RTSP pull (TCP transport, codec copy)             │
│     Duration: 5 seconds                                      │
│     Output: /tmp/orc_capture_<timestamp>.<format>            │
│                                                              │
│  7. QUALITY GATE                                             │
│     Check: file exists and is not empty                      │
│     Check: ffprobe can parse the container                   │
│     Check: resolution matches expected (1920x1080)           │
│     Check: duration within tolerance (4-7 seconds)           │
│     Check: bitrate above minimum (12,000 kbps)              │
│     Warn:  frame count below threshold (40 frames)           │
│                                                              │
│  8. DELIVER OR RETRY                                         │
│     PASS → move file to /home/pi/Videos/<timestamp>.mp4      │
│            ORC-OS daemon picks it up within 5 seconds         │
│     FAIL → delete temp file, retry (up to 3 attempts)        │
│     --dry-run → validate but do not deliver                  │
│                                                              │
│  9. RELAY OFF (on exit, via trap)                            │
│     cycle mode: power off PoE relay (GPIO 24 LOW)            │
│     always mode: leave relay on                              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Relay Modes

The relay controls power to the PoE switch, which powers the camera.

| Mode | Behavior | Use case |
|------|----------|----------|
| `cycle` | Relay ON before capture, OFF after | Sukabumi (solar) — conserve battery |
| `always` | Relay ON at boot, never turned OFF | Jakarta (AC) — camera stays on 24/7 |

Set via `RELAY_MODE` in `/etc/orc-capture.conf`.

Both modes use **NO (Normally Open)** relay contacts. If the Pi crashes or
loses power, the relay opens and the camera loses power. This is a
fail-safe (designed to turn off safely when power is lost) — it prevents
the camera from draining the solar battery during a Pi failure.

The relay is controlled via the `poe-relay` helper script, which sets
GPIO 24 HIGH (relay on) or LOW (relay off).

---

## Quality Gate

Every captured video must pass these checks before delivery to ORC-OS:

| Check | Threshold | Failure behavior |
|-------|-----------|-----------------|
| File exists and not empty | > 0 bytes | Hard fail |
| Container parseable | ffprobe succeeds | Hard fail |
| Resolution | Must match EXPECTED_WIDTH x EXPECTED_HEIGHT | Hard fail |
| Duration | MIN_DURATION to MAX_DURATION seconds | Hard fail |
| Bitrate | Above MIN_BITRATE_KBPS | Hard fail |
| Frame count | Above MIN_FRAMES | Warning only |

**Why the quality gate exists:** ORC processing requires high-quality video
to detect water surface patterns. A corrupt, low-bitrate, or truncated video
wastes processing time and produces unreliable velocity estimates. The
quality gate catches these before they enter the pipeline.

**Bitrate context:** pyorc (the ORC processing library) recommends 20 Mbps
at 1080p. The quality gate minimum of 12 Mbps is a lower bound — videos
between 12 and 20 Mbps will pass but may produce lower-quality results.
See `camera/profiles/` for alternate camera configurations targeting
higher bitrates.

---

## Camera Config Enforcement

The ANNKE C1200 camera has settings that revert to factory defaults after a
power cycle. orc-capture re-applies critical settings via ISAPI on every run:

| Setting | What it does | Why it matters |
|---------|-------------|----------------|
| `supplementLightMode` → `irLight` | Forces IR-only illumination | Prevents white LED from flashing, which washes out the image and startles wildlife |
| OSD overlays → disabled | Removes date/time and channel name text burned into the video | Text overlays interfere with ORC pattern detection |

These are checked and fixed via HTTP PUT to the camera's ISAPI endpoints.
If the camera is already configured correctly, no changes are made.

---

## Maintenance Mode

Before starting a capture, orc-capture checks for the maintenance mode
flag file at `/run/orc-maintenance-mode`. If present, the script logs a
message and exits without capturing.

This flag is created by `orc-maintenance-check` at boot, which reads the
station's mode from GitHub. See the [Operator Guide](OPERATOR_GUIDE.md)
Section 6 for how maintenance mode works.

---

## Configuration Reference

All settings are in `/etc/orc-capture.conf`. The script sources this file
on every run.

### Relay

| Setting | Default | Description |
|---------|---------|-------------|
| `RELAY_MODE` | `cycle` | `cycle` or `always` |

### Camera Connection

| Setting | Default | Description |
|---------|---------|-------------|
| `CAMERA_IP` | `192.168.50.139` | Camera IP address |
| `CAMERA_USER` | `admin` | ISAPI / RTSP username |
| `RTSP_PORT` | `554` | RTSP port |
| `RTSP_PATH` | `Streaming/Channels/101` | RTSP stream path (main stream) |

### Video Capture

| Setting | Default | Description |
|---------|---------|-------------|
| `CAPTURE_DURATION` | `5` | Seconds of video to record |
| `VIDEO_FORMAT` | `mp4` | Output container format |
| `VIDEO_CODEC` | `copy` | ffmpeg codec (copy = no re-encode) |
| `VIDEO_AUDIO` | `0` | 0 = strip audio, 1 = keep |

### Output

| Setting | Default | Description |
|---------|---------|-------------|
| `INCOMING_DIR` | `/home/pi/Videos` | Where delivered videos land (ORC-OS watches this) |
| `FILENAME_TEMPLATE` | `%Y%m%dT%H%M%S` | strftime format for filename (matches ORC-OS template) |
| `TEMP_DIR` | `/tmp` | Scratch space for captures in progress |

### Timing

| Setting | Default | Description |
|---------|---------|-------------|
| `CAMERA_BOOT_TIMEOUT` | `90` | Max seconds to wait for camera ping |
| `CAMERA_SETTLE_TIME` | `15` | Seconds after first ping before RTSP capture |
| `MAX_RETRIES` | `3` | Capture attempts on quality gate failure |
| `RETRY_DELAY` | `5` | Seconds between retries |

### Quality Gate

| Setting | Default | Description |
|---------|---------|-------------|
| `MIN_BITRATE_KBPS` | `12000` | Minimum acceptable bitrate (kbps) |
| `EXPECTED_WIDTH` | `1920` | Expected horizontal resolution |
| `EXPECTED_HEIGHT` | `1080` | Expected vertical resolution |
| `MIN_DURATION` | `4.0` | Minimum acceptable duration (seconds) |
| `MAX_DURATION` | `7.0` | Maximum acceptable duration (seconds) |
| `MIN_FRAMES` | `40` | Minimum frame count (warning only) |

### Camera Config Enforcement

| Setting | Default | Description |
|---------|---------|-------------|
| `ISAPI_CHANNEL` | `/ISAPI/Image/channels/1` | ISAPI endpoint for image settings |
| `SUPPLEMENT_LIGHT_MODE` | `irLight` | Desired supplement light mode |

---

## Credentials

Camera passwords are **never stored in orc-capture.conf** (which is in
version control). Instead, credentials are loaded from:

1. `~/.orc_deploy_<site>` — a file created manually on each Pi
2. `CAMERA_PASS` environment variable (for testing)

The deploy file format is:
```bash
BASE_PASSWD=your_camera_password_here
```

---

## Filename Format

Videos are named using the strftime template in `FILENAME_TEMPLATE`:

```
20260410T143052.mp4
```

This matches the ORC-OS daemon template `{%Y%m%dT%H%M%S}.mp4`. ORC-OS
extracts the timestamp from the filename to associate the video with
water level readings.

**If you change the template**, update the ORC-OS daemon settings to match
(web UI > Settings > Expected video filename template).

---

## Command Line Usage

```bash
# Normal capture (relay + camera boot + RTSP + quality gate + deliver)
orc-capture

# Capture and validate, but do not deliver to ORC-OS
orc-capture --dry-run

# Skip relay control (camera already powered on)
orc-capture --skip-relay

# Both flags (useful for testing on the bench)
orc-capture --skip-relay --dry-run

# Show help
orc-capture --help
```

---

## Troubleshooting

### Camera unreachable

```
ERROR: Camera did not respond within 90s
```

- Is the PoE switch powered? Check fuse F2.
- Is the ethernet cable connected?
- Is the camera IP correct? Check `/etc/orc-capture.conf`.
- Run `poe-relay status` to verify relay state.
- Run `ping 192.168.50.100` manually.

### Quality gate failures

```
FAIL: bitrate 9500 kbps (minimum 12000 kbps)
```

- Camera may still be stabilizing after boot. Increase `CAMERA_SETTLE_TIME`.
- Camera encoding settings may be too low. Check streaming config via camtool.
- Network congestion between camera and Pi. Check ethernet cable quality.
- See `camera/profiles/` for alternate higher-bitrate configurations.

### Camera settings revert

```
Fixed: supplementLightMode → irLight
Fixed: OSD overlays disabled
```

These messages are **normal** on Sukabumi where the camera power-cycles each
capture. The ANNKE C1200 does not persist all settings through power cycles.
orc-capture detects and fixes this automatically.

If you see these on Jakarta (where the camera stays on), it means something
reset the camera (firmware update, factory reset, or manual change).

### No video delivered but no error

Check if maintenance mode is active:
```bash
cat /run/orc-maintenance-mode 2>/dev/null && echo "MAINTENANCE MODE" || echo "production"
```

Check the journal for orc-capture output:
```bash
journalctl -u orc-capture --no-pager -n 30
```

---

## Extending orc-capture

### Adding a new capture method

The current capture method is RTSP pull via ffmpeg. To add an alternative
(e.g., ISAPI local recording for Profile C), add a new function alongside
`capture_video()` and select based on a config variable:

```bash
CAPTURE_METHOD="${CAPTURE_METHOD:-rtsp}"

case "$CAPTURE_METHOD" in
    rtsp)   capture_video "$tmpfile" ;;
    isapi)  capture_video_isapi "$tmpfile" ;;
    *)      err "Unknown CAPTURE_METHOD: $CAPTURE_METHOD" ;;
esac
```

### Adding a new quality check

Add checks to the `quality_gate()` function. Follow the pattern:
- Extract the metric from ffprobe JSON output
- Compare against a threshold from the config
- Log PASS/FAIL
- Increment `failures` counter on fail

### Adding a new camera config enforcement

Add ISAPI check/fix logic to `enforce_camera_config()`. Follow the pattern:
- GET the current setting via curl + ISAPI endpoint
- Compare against desired value
- If wrong, PUT the corrected XML
- Log what changed
