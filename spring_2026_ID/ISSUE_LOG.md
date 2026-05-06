# Issue Log - Indonesia Spring 2026 Deployment

Tracks discovered issues, design corrections, and open questions across both sites.

| Status | Meaning |
|--------|---------|
| OPEN | Needs action |
| RESOLVED | Fix applied, verified |
| CLOSED | No longer relevant |
| PARKED | Action depends on external dependency (IPB engagement, etc.) |

Issues prefixed `ISS-FIELD-*` were discovered during the April 2026
deployment trip; earlier issues (`ISS-001`–`ISS-007`) date from the
build phase.

---

## Issues

### ISS-FIELD-001: Jakarta intended site permission fell through; station not deployed

| Field | Value |
|-------|-------|
| **Date opened** | 2026-04-19 (in-country) |
| **Site** | Jakarta |
| **Risk** | Project schedule |
| **Impact** | High |
| **Status** | PARKED (pending IPB site re-selection) |

**Problem:**
Permission to install the Jakarta station at the intended site did not
come through during the April 2026 trip. Without an authorized location
and the associated logistical arrangements (mounting, AC power tap,
network access, on-site security), the station could not be installed.
The station is built, software-configured, and bench-tested.

**Resolution path:**
Engaging IPB (Institut Pertanian Bogor / Bogor University) to advise on
a viable alternate site that is (a) hydrologically useful, (b) in
catchment of interest to PMI's flood-warning use case, and (c) has the
physical/permission profile that makes a deployment feasible. Until a
site is identified and authorized, the Jakarta station stays in the US
in storage.

**What this means for the rest of the project:**
- The TODO and BOM items that assume Jakarta-on-river (mounting hardware,
  GCP survey, sensor field testing, PMI training at Jakarta) are paused.
- Software work that benefits both sites continues against the Sukabumi
  station and against the bench-built Jakarta station as a soak rig.

---

### ISS-FIELD-002: Sukabumi RTK survey failed twice — same ~99 cm H / 139 cm V noise both times

| Field | Value |
|-------|-------|
| **Date opened** | 2026-04-20 (initial), reproduced 2026-04-21 |
| **Site** | Sukabumi |
| **Risk** | Calibration accuracy / discharge certifiability |
| **Impact** | High |
| **Status** | PARKED (pending IPB total station survey) |

**Problem:**
Two RTK survey attempts at the Sukabumi site, on consecutive days with
the same equipment (Emlid Reach RS+ rover + temporary base) and the
same methods, both produced check-point spreads of ~99 cm horizontal
and ~139 cm vertical between repeat occupations of the same physical
markers. The 3 cm horizontal / 4 cm vertical RTK gate was exceeded by
roughly 30×. Same-marker drifts between day 1 and day 2: 29 cm (GCP2),
75 cm (GCP4), 89 cm (GCP3). See `survey_data/output/metadata.yaml` for
the recorded check-point spread and full warnings.

**Why this matters:**
Calibration accuracy is bounded below by survey accuracy. Discharge
estimates published from this survey alone would carry the survey's
noise as a multiplicative scaling error of similar magnitude (~30%) on
absolute flow values. Qualitative monitoring (rising/falling, faster/
slower) is unaffected; quantitative discharge in m³/s with a stated
uncertainty band is not certifiable from this data.

**Resolution path:**
Engaging IPB for a **total station** survey at Sukabumi. RTK-with-our-
equipment has now produced the same noise twice; that's strong evidence
to try a fundamentally different methodology rather than a third RTK
attempt. Total station gives sub-cm accuracy independent of GNSS sky
conditions or base-station setup quality and avoids whatever is causing
the RTK noise (possible causes include poor base-station coordinate
quality, sky obstruction, RF interference at the urban canal site).

**Interim:**
The auto-fit salvage pipeline (`survey/Sukabumi_survey_salvage_methodology.md`)
identifies a 6-GCP subset (GCP7, GCP8, GCP10, GCP13, GCP14, GCP3.2)
that produces a calibration with 4.61 cm RMSE — passes the 5 cm gate.
This is the calibration the deployed station runs on. End-to-end has
been verified once against the calibration video (`q_50 = 0.51 m³/s`);
absolute flow numbers from the salvage calibration are *not* certified.

**Files:**
- `spring_2026_ID/survey_data/output/metadata.yaml` — recorded spread
- `spring_2026_ID/survey_data/sukabumi_handoff/` — calibration handoff
  files used to load the station
- `survey/Sukabumi_survey_salvage_methodology.md` — methodology
- `survey/outsourced_survey_brief.md` — vendor SOW for the IPB survey

---

### ISS-FIELD-003: ORC-OS dashboard "save" silently clobbers SQL-edited camera_config fields

| Field | Value |
|-------|-------|
| **Date opened** | 2026-04-22 |
| **Site** | Sukabumi |
| **Status** | OPEN — workaround documented |

**Problem:**
Editing `camera_config.data` directly in `~/.ORC-OS/orc-os.db` (e.g.
`UPDATE camera_config SET data = json_set(data, '$.gcps.h_ref', 617.065) WHERE id=3`)
is durable in SQL only. The next time the dashboard fires a websocket
`{action: 'save'}` for that camera config — which can happen on any
form interaction, not only an explicit save click — the in-memory
form copy of `data` overwrites the DB row, reverting the SQL edit.
This bit us during the Sukabumi bring-up: `h_ref` was set to 617.065
via SQL, the dashboard later saved, the value reverted to 0.0, and the
subsequent Process run fell through to optical water-level detection.

**Workaround:**
Always set camera-config values through the dashboard form (or through
the `/api/camera_config/` PATCH endpoint). The SQL path is non-durable
and should not be used.

**Followup:**
Worth flagging upstream to the ORC-OS team — at minimum the websocket
save should be a partial PATCH, not a wholesale clobber of `data`.

---

## Build-phase issues

### ISS-001: Sleep-phase power budget was understated by ~24 Wh/day

| Field | Value |
|-------|-------|
| **Date opened** | 2026-03-13 |
| **Site** | Sukabumi |
| **Risk** | Low |
| **Impact** | High |
| **Status** | RESOLVED |

**Problem:**
The Sukabumi power budget omitted the quiescent draw of the two DDR-60G buck converters (~0.5W each, 24/7) and the Hydreon RG-15 rain gauge idle current (~150µA, 24/7). These are always-on loads connected directly to TB1 (battery bus) — they draw power even while the Pi is sleeping.

The previous budget showed ~94 Wh/day total consumption. The corrected figure is **~118 Wh/day** — a 25% increase. Battery autonomy dropped from 3.2 days to **2.5 days** (no sun).

**Why this matters:**
The system still has ample solar margin (602 Wh surplus), so normal operation is unaffected. But during extended cloudy periods (monsoon season), the station runs out of battery ~17 hours sooner than previously estimated. For a remote site where physical visits are expensive, accurate autonomy estimates matter for planning maintenance windows and alert thresholds.

**Resolution:**
- Updated `BOM_Sukabumi.md` power budget sleep-phase table to include DDR-60G-5 (0.5W), DDR-60G-12 (0.5W), and RG-15 (0.002W)
- Revised daily total from ~94 Wh to ~118 Wh
- Revised autonomy from 3.2 days to 2.5 days
- Noted that disconnecting DDR-60G-12 during sleep (via relay) could recover ~12 Wh/day if needed

**Files changed:** `BOM_Sukabumi.md` (Section 8: Power Budget)

---

### ISS-002: Rain gauge data collection during Pi sleep was undocumented

| Field | Value |
|-------|-------|
| **Date opened** | 2026-03-13 |
| **Site** | Sukabumi |
| **Risk** | Low |
| **Impact** | High |
| **Status** | RESOLVED |

**Problem:**
The Pi sleeps ~14 out of every 15 minutes. The Hydreon RG-15 rain gauge must collect rainfall continuously — including while the Pi is off. No documentation described how this works or what the software must do on each wake cycle.

The hardware wiring already supports this (RG-15 on always-on TB1 bus), but the design intent was implicit, not documented. A future maintainer could reasonably move the RG-15 to the switched circuit (to "save power") and break rainfall collection without realizing it.

**Why this matters:**
Rainfall data is a primary output of the station. If the RG-15 loses power between cycles, all rainfall between wake events is silently lost — there's no error, just missing data. This is the kind of issue that could go unnoticed for weeks until someone reviews the data and wonders why rainfall totals are too low.

**Resolution:**
Hardware (already correct):
- RG-15 powered from TB1 (always-on 12V battery bus)
- RG-15 accumulates rainfall internally while Pi sleeps (~150µA draw)

Software (requirement documented, not yet implemented):
- On each wake cycle, read RG-15 `Acc` register via UART
- Compare to previous reading (stored on disk) to compute interval rainfall
- Track deltas rather than resetting accumulator (safer against missed reads)

Documentation added:
- `BOM_Sukabumi.md` Section 6: "Data Collection During Power Cycling" notes
- `diagrams/sukabumi/circuit_diagram.txt`: "POWER CYCLING NOTE" annotation
- `docs/TROUBLESHOOTING.md`: Sukabumi rain gauge troubleshooting for power cycling
- `docs/ASSEMBLY_SUKABUMI.md`: Verification step to confirm RG-15 stays powered during sleep
- `CLAUDE.md`: Gaps table entry (resolved)

---

### ISS-003: Video capture method — RTSP (final)

| Field | Value |
|-------|-------|
| **Date opened** | 2026-03-13 |
| **Date updated** | 2026-03-28 |
| **Site** | Both |
| **Risk** | Low |
| **Impact** | High |
| **Status** | RESOLVED |

**History:**
The original design used RTSP streaming (Pi pulls video via ffmpeg). This was
changed to FTP-based capture (camera pushes to Pi) for higher quality, but the
ANNKE C1200 does not support the scheduled event triggers needed to push video
on a 15-minute duty cycle. FTP push requires motion detection or alarm events,
which are not suitable for continuous scheduled capture.

**Final decision (2026-03-28):**
Revert to RTSP-based capture via `orc-capture` script. The Pi pulls 5s video
clips from the camera's RTSP stream using ffmpeg (TCP transport, codec copy, no
re-encoding). Quality gate validation confirms 1920x1080 at ~15.5 Mbps average
across 20 consecutive tests (100% pass rate). This exceeds ORC requirements.

**Capture pipeline:**
- Pi wakes → powers camera via PoE relay → waits for boot (~37s) → pulls 5s
  RTSP clip → validates via quality gate → delivers to ORC-OS incoming directory
- Configuration driven by `/etc/orc-capture.conf`
- Script: `orc-capture` (see `pi/shared/usr/local/bin/orc-capture`)

**What this means:**
- vsftpd / ftpcam user are **not needed** — can be disabled
- Camera FTP config (`camera/common/ftp.xml`) is dormant — not pushed to camera
- `camtool.py` still manages all other ISAPI endpoints (streaming, image, NTP, etc.)
- No camera-side event/schedule configuration needed for capture

---

### ISS-004: ANNKE C1200 white spotlight fires on every power-on

| Field | Value |
|-------|-------|
| **Date opened** | 2026-03-28 |
| **Site** | Sukabumi, Jakarta |
| **Risk** | High |
| **Impact** | High |
| **Status** | OPEN |

**Problem:**
The ANNKE C1200 fires its white spotlight at full brightness for 2-3 seconds on
every power-on. This is a documented Hikvision firmware hardware self-check that
runs before the OS loads — no ISAPI configuration prevents it. With a 15-minute
duty cycle (96 power-on events/day), this is unacceptable for the Sukabumi site,
which is an urban canal with residences on both sides.

**Investigated and ruled out:**
- `supplementLightMode=irLight` via ISAPI — persists, but boot flash still fires
- `whiteLightBrightness=0` via ISAPI — persists, but boot flash still fires
- `/ISAPI/System/externalDevice` `enabled=false` — endpoint not supported on this firmware
- Disabling smart events / motion detection — boot flash is not event-triggered
- CGI endpoints — removed from G5/G6 firmware
- Telnet/SSH — not accessible on this firmware generation
- ONVIF auxiliary control — maps to wired relay outputs, not LED drivers
- Firmware update — no Hikvision firmware version offers a boot flash disable option

**Why tape won't work:**
IR and white LEDs are interleaved in the same ring behind a single dome. Covering
white LEDs also blocks IR night vision.

**Why always-on camera won't work:**
Keeping the camera powered 24/7 increases daily consumption from 118 Wh to 425 Wh.
Battery autonomy drops from 2.5 days to <1 day. Not viable on the solar budget.

**Possible solutions (not yet pursued):**
1. Replace with an IR-only camera model (Hikvision "-I" suffix, no white LEDs)
2. Longer duty cycle (30 min) to halve the frequency
3. Flash genuine Hikvision firmware and retest (unlikely to help per community reports)
4. File firmware feature request with Hikvision

---

### ISS-005: Status LED design — single RGB vs 3× single-color

| Field | Value |
|-------|-------|
| **Date opened** | 2026-03-29 |
| **Site** | Both |
| **Status** | OPEN |
| **Decision needed by** | 2026-03-30 (before Chester's trip) |

**Problem:** The original design uses 3 single-color 12V panel-mount LEDs
(red/yellow/green) switched by relay channels CH2-4. This has several issues:
- Uses 3 relay channels, leaving none for future growth
- 3 panel holes = 3 potential seal failures in tropical humidity
- Limited to on/off per color (7 states total)
- 12V LEDs draw more power (relevant for Sukabumi solar budget)
- Current LEDs have minimal shoulder for weathersealing

**Requirements:**
- Daylight visible from ground level
- Weatherproof seal (IP67+) with solid bulkhead
- Multi-color to communicate different statuses
- Minimal panel holes (ideally 1)
- Low power (Sukabumi solar constraint)
- Free up relay channels for PMI team experimentation

**Options under consideration:**

| Option | Pros | Cons |
|--------|------|------|
| **A: APEM Q16 RGB, 12V, IP67** | Professional, great seal, Fresnel lens for daylight, 16mm mount | Still uses 3 relay channels, 12V power draw, ~$18/unit |
| **B: Bare RGB LED (3.3V) + IP67 housing** | Direct GPIO drive, no relays, low power | No off-the-shelf IP67 panel mount product exists at 3.3V |
| **C: WS2812B (NeoPixel), 5V, 1 data wire** | 1 GPIO pin, unlimited colors, ~60mA, frees all relay channels | No off-the-shelf IP67 panel mount, need custom housing or find suitable enclosure |
| **D: Internal mount behind clear window** | Zero additional panel holes, no seal risk | Less visible, may need light pipe, requires enclosure modification |

**Status color/pattern chart — see `docs/LED_STATUS_SPEC.md` for full spec:**

| Color | Pattern | Meaning |
|-------|---------|---------|
| White | Solid | Boot in progress |
| Green | Solid | System OK, idle |
| Green | Flash (2 Hz) | Capture running |
| Cyan | Solid | Maintenance mode active |
| Red | Solid / Blink | Camera error (unreachable / capture failed) |
| Blue | Solid / Blink | Network error (modem down / upload failed) |
| Yellow | Solid / Blink | Storage error (low space / write error) |
| Magenta | Solid | Power error (undervoltage) |
| OFF | — | Pi is off / sleeping (Sukabumi between cycles) |

Multiple errors: LED cycles through all active errors (3s each).
Config-driven (`/etc/orc/led-status.yaml`) — errors can be suppressed
per-subsystem for bench testing.

**Decision (2026-03-30):** WS2812B NeoPixel with silicone-filled acrylic
sandwich light window. Single LED inside enclosure, visible through a drilled
hole sealed with two acrylic sheets and clear neutral-cure silicone filling
the gap solid. No air cavity = no condensation risk. Uses 1 GPIO data pin,
5V power from Pi rail. Frees all 3 relay channels for future use by PMI team.

**Status:** RESOLVED

See assembly docs for installation procedure.

---

### ISS-007: rpi-ws281x library does NOT work on Raspberry Pi 5

| Field | Value |
|-------|-------|
| **Date opened** | 2026-04-01 |
| **Site** | Both |
| **Risk** | High (blocks LED functionality entirely) |
| **Impact** | High |
| **Status** | RESOLVED |

**Problem:**
The `rpi-ws281x` Python library (v5.0.0), which is the most commonly
referenced WS2812B/NeoPixel driver for Raspberry Pi, fails immediately on
Pi 5 with error code -3: "Hardware revision is not supported", followed by
a segfault. This is because the Pi 5 uses an RP1 southbridge chip for GPIO
that does not expose the BCM2711 DMA/PWM peripherals that rpi_ws281x relied
on. This is a hard incompatibility — no pin change or config.txt tweak fixes it.

**How we discovered it:**
First attempt to run `orc-led-test` after wiring the WS2812B to GPIO 18 hit
the error immediately. The library initializes, queries `/proc/device-tree`
for the hardware revision, and bails out when it finds a Pi 5.

**Resolution:**
Replaced `rpi-ws281x` with three Adafruit packages:
- `adafruit-blinka` (hardware abstraction layer)
- `adafruit-circuitpython-neopixel` (high-level NeoPixel API)
- `adafruit-blinka-raspberry-pi5-neopixel` (Pi 5 RP1 PIO driver)

These drive the WS2812B protocol through the RP1's **PIO** (Programmable I/O)
block via `/dev/pio0`, which is present in Raspberry Pi OS since mid-2024.
No hardware changes required — GPIO 18 wiring stays the same.

The code imports `neopixel` (from `adafruit-circuitpython-neopixel`). Blinka
auto-detects the Pi 5 and routes through the PIO backend — no Pi5-specific
import needed in application code.

Install:
```bash
sudo pip install --break-system-packages adafruit-blinka \
    adafruit-circuitpython-neopixel \
    adafruit-blinka-raspberry-pi5-neopixel
```

Also deploy the config file:
```bash
sudo mkdir -p /etc/orc
sudo cp pi/shared/etc/orc/led-status.yaml /etc/orc/led-status.yaml
```

**Files changed:**
- `pi/shared/usr/local/lib/orc-led-status/led_status.py` — LedDriver class rewritten
- `pi/shared/usr/local/bin/orc-led-test` — LedDriver class rewritten
- `pi/shared/usr/local/bin/orc-preflight` — Python package check updated
- `pi/shared/etc/systemd/system/orc-led-status.service` — comment updated
- `pi/PACKAGES.md` — rpi-ws281x replaced with Adafruit packages
- `docs/LED_STATUS_SPEC.md` — compatibility note added
- `diagrams/sukabumi/GPIO_WIRING.md` — software section updated with warning

**Note for future builders:** If you search online for "WS2812B Raspberry Pi
Python", almost every result will point you to `rpi-ws281x`. It does not work
on Pi 5. Use the Adafruit Blinka path instead.

---

### ISS-006: Minor solder contact on TP11 test pad (Jakarta Pi)

| Field | Value |
|-------|-------|
| **Date opened** | 2026-03-30 |
| **Site** | Jakarta |
| **Status** | MONITORING |

During soldering of the J2 power button header on the Jakarta Pi 5, a small
amount of solder contacted the TP11 test pad adjacent to J2. TP11 is a
manufacturing test point with no functional connection in normal operation.
Visual inspection confirms no solder bridge between TP11 and either J2 pin.

**Action:** No fix needed unless problems arise. If the Jakarta Pi exhibits
unexplained behavior (boot issues, power anomalies), inspect TP11 area for
a solder bridge as part of troubleshooting.

---
