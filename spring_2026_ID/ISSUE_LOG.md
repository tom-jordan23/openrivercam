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

### ISS-FIELD-005: LiveORC's nginx SSL config was load-bearing and existed in exactly one place

| Field | Value |
|-------|-------|
| **Date opened** | 2026-08-27 |
| **Site** | LiveORC server (AWS) |
| **Risk** | Site outage on any container recreate |
| **Impact** | High |
| **Status** | RESOLVED 2026-08-27 |

**Problem:**
During TODO-112 Phase 7 the `liveorc_webapp` container was recreated for the
first time since May. nginx then failed to start:

```
[emerg] unknown directive "ssl" in /liveorc/nginx/nginx-ssl.conf:32
```

LiveORC 0.3.0 generates `nginx-ssl.conf` from a template using the standalone
`ssl on;` directive. nginx **removed** that directive in 1.25.1, and LiveORC's
own image ships nginx 1.26.3 — so the shipped template cannot work with the
shipped nginx. gunicorn kept running, so the container reported healthy while
the site was unreachable; `curl` returned `000` because `docker-proxy` held
80/443 with nothing behind it.

**Why it had not been seen:** the container had run since May and was only ever
`docker start`ed, never recreated. A hand-patched `nginx-ssl.conf` had been
living in the writable layer, with no copy anywhere and no record that it
existed. Deleting that layer — the entire point of the media migration —
removed it.

This is the *same failure class* the migration was fixing, in a different file:
critical state present in exactly one place, invisible until something forced a
rebuild. The media was the known instance. This was not.

**Resolution:**
Two idempotent `sed`s in `/opt/LiveORC/start-liveorc.sh` (a local wrapper, so it
survives LiveORC upgrades) patch both the template and the generated config on
every start, folding `ssl on;` into `listen 8000 ssl deferred;`. A third check
makes "nginx not running after start" fatal, so a healthy-looking container
serving nothing can never again pass as success.

The seds match nothing once upstream fixes the template, so the repair retires
itself rather than masking a future fix — which is why it is not a `:ro` bind
mount over the template.

**Upstream:** LiveORC 0.3.0 ships a template incompatible with its own bundled
nginx. Worth reporting alongside TODO-105.

---

### ISS-FIELD-006: `liveorc.sh` scales a worker service upstream has commented out

| Field | Value |
|-------|-------|
| **Date opened** | 2026-08-27 |
| **Site** | LiveORC server (AWS) |
| **Risk** | Any `LORC_DEFAULT_NODES > 0` takes the whole stack down |
| **Impact** | High |
| **Status** | RESOLVED 2026-08-27 (keep `LORC_DEFAULT_NODES=0`) |

> **This issue was first written on a wrong premise** — that
> `LORC_DEFAULT_NODES=0` had disabled video processing during the August
> outage. It had not. Corrected the same day; the original reasoning is kept
> below because the wrong version was acted on and briefly took the site down.

**Problem:**
`liveorc.sh:336` appends `--scale liveorc_worker=$LORC_DEFAULT_NODES` whenever
the value is above 0. But `docker-compose.rabbitmq.yml` has the entire
`liveorc_worker` service **commented out** upstream, under:

```
# TODO: add back workers that connect to ORC-OS API
```

`git status` confirms that file is unmodified locally — this is upstream's own
state. So `docker compose` fails with `no such service: liveorc_worker: not
found` and **aborts before starting anything**, taking `liveorc_webapp` and `db`
down with it. Not a degraded start: a total one.

**How it was found:** `.env` showed a local change of `LORC_DEFAULT_NODES` from
`1` to `0`, and the October 2025 journal showed a worker running. That looked
like emergency triage during the outage that was never reverted. Setting it back
to `1` took LiveORC down for about six minutes. Reverting to `0` restored it.

The October journal is real, but `/opt/LiveORC` was updated between then and
now, and the newer upstream dropped the worker. **`0` is the correct value for
this version.** Whoever set it was fixing a config that would otherwise break
the stack.

**Lesson:** a local diff against upstream shows *what* changed, not *why*, and
"reverting to upstream's value" is not automatically safe when the surrounding
code has moved. Check that the service being scaled still exists before scaling
it.

**Upstream:** `liveorc.sh` should not scale a service its own compose files
comment out. Worth reporting with ISS-FIELD-005 and TODO-105.

---

### ISS-FIELD-007: Video processing error rate jumped 8x while the root disk filled

| Field | Value |
|-------|-------|
| **Date opened** | 2026-08-27 |
| **Site** | LiveORC server (AWS) / Sukabumi |
| **Risk** | ~377 videos captured but never turned into timeseries |
| **Impact** | Medium-High |
| **Status** | OPEN |

**Problem:**
`api_video.status` distribution from the 2026-08-27 backup (4 = Finished,
5 = Error):

| Month | Finished | Error | Rate |
|---|---|---|---|
| 2025-11 | 518 | 28 | 5% |
| 2026-05 | 430 | 10 | 2% |
| 2026-06 | 700 | 20 | 3% |
| **2026-07** | 896 | **280** | **24%** |
| **2026-08** | 205 | **97** | **32%** |

The baseline is 2-5%. It jumps eightfold in July and stays there.

**Correlation:** media began accumulating in the container writable layer on
2026-05-14, and the root filesystem reached 100% on 2026-08-10 (TODO-112). The
error spike tracks the disk filling. Processing writes keyframes and thumbnails
into `MEDIA_ROOT`; on a full disk those writes fail.

That is a hypothesis, not a conclusion — the error reason per video has not been
read yet, and July's spike starts before the disk was completely full.

**Why it matters:** roughly 377 videos were captured, uploaded and stored but
never became timeseries. The video files are on the media volume, so if the
cause was infrastructure it is very likely recoverable now that `/` sits at 27%.

**Next steps:**
- Read the actual failure reason on a sample of status-5 videos rather than
  trusting the correlation.
- If it is disk-related, these are candidates for reprocessing — coordinate with
  TODO-113, which already plans a reprocess run and has to reconcile with
  TODO-101's cross-section reversal first.
- Nobody noticed a 32% failure rate. Whatever monitoring covers this, it is not
  working — the same gap as the missing disk alarm.

---

### ISS-FIELD-008: Sukabumi misses a wake and stays down — 22% downtime since May

| Field | Value |
|-------|-------|
| **Date opened** | 2026-08-27 |
| **Site** | Sukabumi |
| **Risk** | Station is down now, and has been unavailable ~1 day in 5 since May |
| **Impact** | High |
| **Status** | OPEN |

**Problem:**
The station periodically misses a Witty Pi wake and does not recover on its
own. TODO-116 recorded the mechanism; this is the measurement behind it,
reconstructed from `sensor_readings` — the station writes rows on every wake,
so their absence is an exact record of when it was down.

Run `liveorc_server/station-health/station_gaps.py` to regenerate any of this.

| Went down (WIB) | Came back (WIB) | Down |
|---|---|---|
| 05-02 06:31 | 05-02 07:31 | 1.0 h |
| 05-11 23:01 | 05-13 13:03 | 38 h |
| 05-16 00:47 | 05-25 07:00 | **9.3 d** |
| 06-25 04:30 | 07-02 10:38 | **7.3 d** |
| 07-02 10:43 | 07-03 09:47 | 23 h |
| 08-15 01:30 | 08-20 10:39 | **5.4 d** |
| 08-20 10:39 | 08-21 08:14 | 22 h |
| **08-27 04:30** | **— still down** | **ongoing** |

**25.4 days down out of 117.9 observed — 22%.** Nobody noticed, which is the
same monitoring gap ISS-FIELD-007 closes with.

**Two patterns in the timing:**

- Every failure since May begins between **23:00 and 04:30 WIB** — the bottom
  of the battery's nightly discharge.
- Every recovery lands between **07:00 and 13:00 WIB**. This was first read as
  a person pressing the button during working hours. **That reading is probably
  wrong** — see the 08-27 event below. Mid-morning is also when solar pushes a
  depleted battery back over a voltage threshold, and the two explanations are
  not separable by time of day alone.

**The 2026-08-27 event — the station recovered on its own.**

It failed at 04:30 WIB and came back at **11:00:21 WIB, 6.5 hours later**, with
nobody asked to attend site. That is the first directly observed recovery, and
it was unattended. It makes solar-driven voltage recovery the better
explanation for the whole 07:00–13:00 cluster, and it means the TODO-116
premise — "stays down until someone physically pushes the button" — is not
established and may be false.

It also makes this outage **6.5 hours against a prior range of 21 hours to 9
days.** The 13 V recovery voltage was set around 08-21. One event is not a
result, but the obvious hypothesis is that the setting is working as intended
and is converting unbounded outages into single-morning ones. That inverts its
status: it was a suspect, and it may be the fix.

**The oscillation tracks the solar transitions, not the clock.**

Boot cadence on 2026-08-27 after recovery:

| Window (WIB) | Behaviour |
|---|---|
| 11:00 – 18:30 | clean 30-min schedule |
| **18:35 – 21:00** | **restarts every ~5 min — 20 off-schedule boots** |
| 21:30 – 00:00 | clean 30-min schedule |

Sunset at Sukabumi is ~17:50 WIB. The burst starts ~45 minutes after it and
stops after ~2.5 hours. The 08-24/25 bursts ran 06:05–10:05, just after
sunrise.

**This holds for the post-08-21 period only.** Binned by hour, 08-21 onward
(n=66) is **zero between 11:00 and 17:00** — the whole peak-sun block — with
everything in 18:00–02:00 and 05:00–10:00. May (n=332) does not look like that
at all: it is roughly flat across the day, because May's episodes were
continuous hunting that ran for hours or days at a stretch rather than bursts
tied to a transition. Do not describe the solar-transition shape as a general
property of the failure; it is a property of how it has behaved since the
recovery voltage went in, and that difference may itself be the most
informative thing here.

That is the signature of Vin crossing a threshold band: the Witty Pi cuts at
the low threshold, the unloaded battery rebounds above the recovery threshold,
it restarts, the camera/PoE load pulls it back down, and it cuts again. Each
hunt costs a full boot and produces no video. It is consistent with the video
evidence below, and it is falsifiable the moment Vin is logged.

**The failure is two mechanisms, and they are worth fixing separately:**

1. **The trigger** — a brownout kills a wake cycle. Suspected battery,
   unproven (see below).
2. **The latch** — the missed cycle leaves the Witty Pi's next-startup alarm in
   the past and nothing re-arms it, so one missed cycle becomes nine days.

Fixing the latch is the higher-value half and is independent of the trigger: it
converts an unbounded outage into a 30-minute one. Fixing the trigger is a
solar/battery capacity question needing a site visit and hardware budget.

**Cross-checked against the video path.** `sensor_readings` reaching the server
proves the *pipeline* worked, not that the station was up. The videos travel a
completely separate route (station -> LiveORC API), so the two together
separate a station outage from a broken path. From the TODO-114 mirror
manifest:

| Both paths dark | Station was genuinely off — 06-25, 08-15, 08-20 boundaries match to the minute |
| Sensors dark, video flowing | 05-16 -> 06-07. Not a station outage: this is the known sensor-upload incident (LTE warm-up race + alphabetical starvation), diagnosed and fixed 2026-07-07 — see `pi/tools/README.md` |
| Video dark, sensors clean 48/day | 06-21 -> 06-22, and **07-30 -> 08-11 (12 days)**. The station was healthy throughout. The August one ends the day after LiveORC was restored for the demo, so it is very likely server-side, alongside ISS-FIELD-007 |

Two consequences. The station-down total is **~22.7 days, not 25.4** — the
05-16 sensor gap was three days longer than the outage under it. And there is a
12-day hole in captured video that has nothing to do with power and that nobody
noticed.

**Off-schedule boots — a second, unexplained behaviour:**

The station also wakes when the schedule says it should be off, in episodes,
typically at 5-minute spacing. Counts by month: **April 924** (bring-up, mostly
hands-on work — discount it), **May 332, June 20, July 5, August 49.** The
densest run was the night of 2026-08-25→26, restarting every five minutes from
22:05 to 02:30 with no charge source — a battery being cycled under load all
night for no captures worth having.

Two candidate mechanisms, **not distinguishable from timestamps**:

- A voltage threshold restarting the Pi as Vin crosses it.
- The Witty Pi re-powering the Pi inside its own 25-minute `ON` window after
  ORC-OS shuts down early. Note the 5-minute spacing is exactly the `OFF M5`
  window in `prod_30.wpi`, which is suggestive and nothing more.

The `wp5` power-on-reason log on the Pi records `alarm` vs voltage vs button.
**It is the single highest-value artefact to collect the moment the station is
back up, before anything else touches it.**

**What this signal is not:** it is tempting to read it as a precursor, and it
isn't one. The May 07–09 episodes were followed by no outage. The 08-15 outage
arrived out of a completely clean cadence. Do not build an alarm on it.

**Undocumented config change:** a **recovery voltage of 13 V** was set on the
Witty Pi around **2026-08-21**. It is recorded nowhere in this repo —
`deploy.sh:347` excludes `pi/sukabumi/*.wpi` from the overlay, so no committed
file would have caught it.

**The battery is LiFePO4** (Tom, 2026-08-28), and that changes what 13 V means.
On lead-acid, 13 V is a charging voltage you rarely see at rest. On a 4S LiFePO4
it is an utterly ordinary *resting* voltage — roughly 20–40% state of charge,
sitting in the flattest part of the discharge curve, where the pack spends most
of its life. So the earlier worry that recovery might never fire is wrong: 13 V
is reached easily and often.

The real problem is the opposite. A threshold planted in the middle of the flat
plateau gets crossed by ordinary load sag in both directions — the camera/PoE
load pulls terminal voltage under it, removing the load lets it rebound over.
That is a hunting oscillator by construction, and it is the best explanation yet
for the ~5-minute restarts. It also fits the shape: no hunting midday (charging
holds 13.6–14.4 V, far above), hunting through the post-sunset settling window
as the pack relaxes back through 13 V, then quiet again once it is solidly
below.

The off-schedule boots **predate the change by months**, so 13 V did not
introduce the behaviour — but on this chemistry it is a poorly chosen threshold
and a plausible amplifier. A recovery point clear of the plateau (~13.4 V, near
full) would not sit where normal operation crosses it.

The number that matters is not the recovery voltage alone but its distance from
the **low-voltage cutoff**, measured against how far Vin sags under load. Wide
gap gives hysteresis; narrow gap, or a load sag that straddles it, gives
exactly this hunting. Both thresholds need reading off the device.

**No power telemetry exists.** `sensor_readings` carries `ds18b20`, `rg15` and
`sht40` and nothing electrical, so "battery is the leading suspect" is
currently unfalsifiable. The Witty Pi reports Vin/Vout/current over the same
I2C link `orc-sensors` already uses.

**ROOT CAUSE FOUND 2026-08-27 — see ISS-FIELD-009.** The station's disk is
pinned at its 5 GB purge threshold. Processing errors on 43% of videos, the
ORC-OS task never completes, `shutdown_after_task` never fires (it is set to 1,
confirmed on the device), and the Pi runs to the Witty Pi's 25-minute backstop
instead of shutting down at ~2 minutes — roughly 12x the energy budget for that
cycle. That is what flattens the battery before dawn.

Everything below stands as measurement, and the conclusion it reached — that
this is not a battery-sizing problem — was right for the wrong reason. The pack
is the last link in the chain, not the first.

**Would more battery fix it? The energy budget says no.**

Measured overnight draw, 18:00-06:00 WIB, using the BOM power budget normalised
to the 30-minute cycle the station actually runs (48 wakes/day, not the 96 the
budget was written for):

| Night | Boots | Draw | Share of 600 Wh nominal |
|---|---|---|---|
| healthy, 07-19/20 | 24 | 37.3 Wh | 6.2% |
| healthy, 08-13/14 | 24 | 37.3 Wh | 6.2% |
| **failed 08-27 04:30** | **24** | **37.3 Wh** | **6.2%** |
| last night, with hunting, survived | 27 | 40.1 Wh | 6.7% |

**The night it died drew exactly what the nights it survived drew.** Same boot
count, same load, and no overnight hunting on that particular night - the
08-25/26 burst was the night before. Load is not the variable.

The absolute number is the argument, and LiFePO4 makes it worse rather than
better. A 12 V 50 Ah pack is 600 Wh nominal; the lead-acid convention derates
that to 300 Wh at 50% depth of discharge, but LiFePO4 tolerates 80–90%, so
usable is more like **~500 Wh**. The station asks it for **37 Wh across twelve
hours** and it cannot deliver. Design autonomy with no sun at all is **over six
days** on this chemistry; observed autonomy is about **ten hours**. That is not
a 20–30% sizing shortfall a second battery would cover — it is more than
**15x**.

So the battery is not too small. One of these is true instead:

1. **The BMS is disconnecting the pack early, most likely on cell imbalance.**
   This is the strongest candidate on LiFePO4 and it has no lead-acid analogue.
   In a 4S pack where one cell has drifted low, that cell hits the BMS per-cell
   floor while the other three are still half full; the BMS opens and the pack
   goes to zero with most of its energy still in it. That produces exactly this
   signature — a 15x apparent shortfall from a pack that measures fine at rest
   and holds voltage under charge. The BOM records it as "existing 200W panel /
   50Ah battery — reused from failed unit": inherited hardware, out of a station
   that had already failed, age unrecorded.
   Plain capacity wear is the weaker version: LiFePO4 takes thousands of cycles,
   so four months of deep discharge should not have worn it out, though sustained
   38–41 °C enclosure temperatures do accelerate ageing.
2. **The low-voltage cutoff is set too high**, so the Witty Pi cuts while most
   of the charge is still in the battery. Costs nothing to fix, and nothing we
   have rules it out - the value has never been read.
3. **There is an unbudgeted parasitic load.** To actually consume ~500 Wh
   overnight the always-on draw would have to be ~25 W against a designed 1.2 W.
   BOM Section 4 already flags that the DDR-60G converters are permanently
   powered from TB1 with no enable pin, and TODO-107 still has "verify DDR-60G
   quiescent draw against the 0.5 W estimate" open.

All three say **do not buy a second battery yet.** Two are fixed by *replacing*
the battery rather than adding to it - and paralleling a new battery with a
degraded one is actively harmful: the weak one becomes a load on the good one
and both end up chronically undercharged.

**What settles it: one night of Vin.** The three separate cleanly in a single
overnight voltage trace, with no site visit:

LiFePO4 reference points (4S, at rest): ~13.4 V full, ~13.1 V at 50%, ~12.9 V
at 20%, knee below ~12.5 V, BMS per-cell disconnect under that.

| Observation | Conclusion |
|---|---|
| Sits ~13.0–13.2 V most of the night, then drops to **zero abruptly in one sample** | BMS disconnect, almost certainly cell imbalance. The pack still held most of its energy. Balance or service it — a second battery in parallel would not help and would worsen the imbalance |
| Slides steadily 12.9 → 12.5 V and through the knee over hours | genuine capacity exhaustion — pack worn, or the real load is far above budget |
| Still above ~12.9 V when the Witty Pi cuts | cutoff misconfigured for this chemistry — free fix |
| Falls fast *while the Pi is asleep* | parasitic load — find it before buying anything |

The flat plateau is what makes this readable: on LiFePO4 a gradual slide and an
abrupt cliff look nothing alike, where on lead-acid both would just be a sag.

That trace needs Witty Pi Vin logged through `orc-sensors`, which needs one good
SSH window. It is the cheapest decisive measurement available and it gates the
hardware spend.

**What would justify adding capacity:** a Vin trace showing the battery holds
voltage well and simply runs out across consecutive sunless days. That is a
wet-season failure mode, and we have not seen it - the August failures followed
a week of zero rain and high insolation.

**Next steps:**
- Collect the `wp5` power-on-reason log and both voltage thresholds the moment
  the station is reachable — before any other change.
  `liveorc_server/station-health/station_watch.py` waits for the station and
  runs `pi/tools/orc_wp5_state.sh` over Tailscale automatically. The awake
  window measured on 08-27 was **under 60 seconds**, so this cannot be done by
  hand.
- Log Witty Pi Vin plus the power-on reason through `orc-sensors`, so this stops
  being inferred from missing rows. Also closes TODO-012's open question about
  DDR-60G quiescent draw.
- Bench-reproduce on the Jakarta station, which is in the US and already wanted
  as a soak rig by TODO-108: load `prod_30.wpi`, set the same 13 V, sweep the
  input voltage and watch for the hunting band directly.
- Before asking PMI to send someone, decide whether they should back the
  recovery voltage off while on site, and have them read the battery at the
  terminals first — two of the previous trips bought a single cycle.
- Record the active schedule and the voltage thresholds somewhere committed.
  Nothing in the repo tracks either, and the running schedule (30 min) does not
  match what the assembly docs call the default (`prod_15.wpi`).

---

### ISS-FIELD-009: Station disk pinned at its purge threshold; half of all captured video never reached the server

| Field | Value |
|-------|-------|
| **Date opened** | 2026-08-27 |
| **Site** | Sukabumi |
| **Risk** | Station is unreliable and self-limiting; sync fails on half of all captures |
| **Impact** | **High** — very likely the root cause behind ISS-FIELD-008 / TODO-116 |
| **Status** | OPEN — no remediation attempted, deliberately |

> **The lost video itself does not matter.** Sukabumi is a pilot station being
> used to test the technology; it is not contributing data to anything yet
> (Tom, 2026-08-27). So none of this is a data-rescue exercise, old video can be
> deleted freely to reclaim space, and there is no reason to attempt a bulk
> upload of the backlog.
>
> What matters is the opposite reading: **a 51% sync failure rate is a finding
> about the system**, and finding it is exactly what a pilot is for. It would be
> disqualifying in a deployment that anyone relied on. Treat the numbers below
> as a verdict on the design, not as an inventory of losses.

**Measured on the station 2026-08-27, over three wake windows.**

```
/dev/mmcblk0p2   58G   51G  5.1G  91% /

43G   /home/pi
37G   /home/pi/.ORC-OS
36G   /home/pi/.ORC-OS/uploads/videos
3.9G  /home/pi/code/git
1.2G  /home/pi/.ORC-OS/tmp

disk_management: min_free_space = 5.0 GB, critical_space = 2.0 GB, frequency = 300 s
```

Free space is **5.1 GB against a 5.0 GB threshold.** Not "nearly full" — pinned to
the line. The disk manager checks every 300 s, purges just enough to clear the
minimum, and is back under it by the next check. The purge fires on the first
check of every fresh boot.

**The video accounting is the serious part.**

```
ORC-OS video table: 5406 rows, 2026-04-08 -> 2026-08-27
  status       DONE 2957 | ERROR 2324 | NEW 125       -> 43% failed processing
  sync_status  SYNCED 2536 | FAILED 2744 | LOCAL 126  -> 51% never reached the server

  mp4s still on disk: 3216, oldest 2026-06-07
  table rows with no file behind them: 2190
```

**2744 videos have never reached LiveORC** — half of everything the station has
captured. The table reaches back to 08 April; the files only to 07 June. Roughly
2190 records no longer have a file.

This reframes two earlier findings. The 12-day video gap (2026-07-30 -> 08-11,
recorded in ISS-FIELD-008) was read as probably server-side; it is at least as
likely that those captures happened, failed to sync, and were purged. And
ISS-FIELD-007's server-side error spike now has a station-side sibling that is
larger.

**Why this is very likely the root cause of ISS-FIELD-008 / TODO-116**

Disk pinned at the threshold -> pyorc processing runs out of room and errors
(43%) -> the ORC-OS task never completes -> `shutdown_after_task` never fires
(it is set to 1, confirmed) -> the Pi runs to the Witty Pi's 25-minute backstop
instead of shutting down at ~2 minutes -> roughly **12x the energy budget for
that cycle** -> the battery is flat before dawn -> the overnight outage.

The battery is the **last** link in that chain, not the first. The energy
arithmetic in ISS-FIELD-008 already said the pack was being asked for 6% of its
nameplate and failing; this explains what was actually drawing it down. Buying
battery capacity would have treated the symptom furthest from the cause.

**What is NOT yet established**

- Whether the purge deletes the `.mp4` itself or only the `output/` artifacts.
  The captured log shows it removing `piv.nc`, transects, plots and
  `camera_config.json` under `output/`. The 2190 fileless rows strongly imply
  the mp4s go too, but nobody has watched one disappear.
- **Why** the 2744 syncs failed. Until that is known, freeing space delays the
  loss rather than stopping it, and the backlog keeps growing.
- Whether the ERROR and FAILED sets overlap, and how far back the FAILED ones
  reach — i.e. how much of the un-synced backlog still exists on disk to be
  recovered at all.
- Why `/home/pi/code/git` is 3.9 GB on a station.

**ACTION TAKEN 2026-08-27 — pre-July video purged, 8.81 GiB reclaimed.**

`pi/tools/orc_purge_synced.py --before-date 20260701 --apply` removed 19 date
directories (20260515, then 20260607–20260624), 0 failures. **Free space
5.00 -> 13.83 GiB**, well clear of the 5.0 GB threshold, so the continuous
purge should now stop. Sukabumi is a pilot and the video was not feeding
anything, so this was a space decision rather than a data one.

The synced-only pass found **nothing** to delete — every SYNCED video had
already been removed by ORC-OS's own purge, which means what it had started
eating was un-synced material, the only copy. That also corrects an earlier
claim in this entry: the purge is not sync-blind, it takes the safe material
first and had simply run out of it.

Two incidental confirmations from the deletion list. There was still a small
20260515 directory (10 MB), so "May is gone" was not quite right. And the June
run stops at the 24th with nothing from the 25th to the 30th — exactly the
06-25 -> 07-02 outage in ISS-FIELD-008, corroborating that outage from an
independent direction.

**FIRST RESULT — THE STATION FAILED ANYWAY (2026-08-28 05:30 WIB).**

Two hours after the purge, with 13.83 GiB free, the station stopped. All four
sensors cease at the same instant; Tailscale offline; four consecutive wakes
missed (06:00, 06:30, 07:00, 07:30). This is a TODO-116 outage on a station
whose disk problem had just been fixed.

**So "the disk is very likely the root cause" was overstated, and I am
recording that rather than quietly softening it.** The chain below is coherent
and every measurement in it stands, but its first prediction failed.

What the failure does NOT settle:

- **The pack may simply have had nothing left.** Free space fixes the *drain*,
  not the *reserve*. If weeks of extended wakes had already run the battery
  down, one good night was never going to refill it. The purge would then still
  be necessary and merely insufficient.
- **The long-wake test has not actually run yet.** Extended wakes are an
  evening phenomenon (18:30-21:00 WIB); the outage happened at dawn, before
  that window came round. Zero long wakes between 00:00 and 05:30 proves
  nothing — that period was always quiet.

What it does support: the **battery is back in play as a primary fault**, not
merely the last link. Two details point that way. The failure came at 05:30,
essentially at sunrise (~05:50) and the very bottom of the discharge curve,
later than the historical 23:00-04:30 window. And V-IN had been sitting at
12.56-12.72 V all night — on a 4S LiFePO4 that is already near the knee, where
a pack can fall away quickly.

Set against that: the 05:30 sample read 12.717 V with **zero** sag, which is
not the signature of a pack about to drop out. Something happened between
05:30 and 06:00 that the 30-minute sampling interval cannot see.

**Next honest test:** whether it self-recovers mid-morning as it did on 08-27
(11:00 WIB, unattended), and whether the 18:30-21:00 long-wake window is clean
once it is back. Until the evening window runs with a healthy disk, the disk
hypothesis is untested rather than disproved.

**This is now a live test of the causal chain.** If the chain in this entry is
right, the extended wakes should stop: with space available, pyorc should
finish, the ORC-OS task should complete, `shutdown_after_task` should fire, and
the Pi should shut down at ~2 minutes instead of running to the Witty Pi's
25-minute backstop. Check with
`liveorc_server/station-health/station_gaps.py` — the "long wakes" section
should fall to zero, and the overnight battery drain with it. If long wakes
continue with 13.8 GiB free, the disk was not the cause and this entry is
wrong.

**Next steps**

Ordered for a pilot whose job is to prove the technology, not to preserve the
video:

- [ ] **Free space, generously.** Old video can simply be deleted — there is
      nothing to rescue. Getting well clear of the 5 GB threshold stops the
      continuous purge, and should by itself end the processing errors, the
      extended wakes and the overnight battery flattening. This is the cheapest
      thing that tests the whole causal chain: if the station starts shutting
      down at ~2 minutes again, the chain is confirmed.
- [ ] **Then establish why sync fails.** Half of all captures never shipped.
      Harmless here, disqualifying in a real deployment, and it is the single
      most valuable thing this pilot has surfaced. `pi/tools/README.md` records
      a near-identical shape for the *sensor* uploader in July — fired before
      the LTE modem registered, all-or-nothing watermark that never advanced.
      Check whether video sync has the same race and no retry.
- [ ] **Size the disk properly — but not by adding one.** 58 GB against
      ~12 GB/month of video is a few months of runway at best. **A second disk
      is not the answer and has already been tried:** ORC-OS cannot handle video
      living on a different filesystem from its database (Tom, 2026-08-27). That
      is the same wall the S3 storage mount hit on the server. The 256 GB USB
      drive struck out of `BOM_Sukabumi.md` ran into this as well as the UAS boot
      storm, so the BOM's stated reason is only half the story.

      That leaves two real options: a larger root device (whole system, not a
      video-only mount), or bounded retention — which only becomes safe once
      sync is trustworthy, because today deleting an un-synced video loses it.

**Note the shape of this.** Fixing sync is not just a quality finding, it is the
structural fix: with reliable sync, video can be deleted shortly after upload
and 58 GB stops mattering. Without it, any disk fills eventually and the station
returns to this state. Sync is the constraint that makes retention possible.
- [ ] Alarm this. Three disks have now filled unnoticed in this project — the
      LiveORC root (ISS-FIELD-007), the media volume (TODO-112), and now the
      station. None were alarmed. The station has no monitoring at all.
- [ ] ~~Revisit the BOM decision that struck out the 256 GB USB drive.~~
      **Not a live option — do not re-propose.** Three separate reasons, and I
      had written this up as though it were an oversight:
      1. ORC-OS cannot hold video on a different filesystem from its database,
         the same wall the S3 mount hit on the server. A second disk does not
         solve a video-space problem at all.
      2. The removal was a blocking hardware fault, not a budget slip:
         `build_notes/sukabumi/known_issues.md` #1 records **228 USB disconnects
         and 158 URB errors in 12 minutes at boot, and the modem dropped off the
         bus entirely.** The modem is the only remote access to this station, so
         a recurrence costs a site visit.
      3. The only fix is `usb-storage.quirks=0781:5583:u` in `cmdline.txt` —
         `uas` and `usb-storage` are kernel built-ins so `modprobe.d` is ignored.
         That is a boot-time parameter needing a reboot, which is not something
         to do remotely to a solar station with a flat battery.

      The drive is also not physically in the station; it was never deployed.
      Space has to come from retention or a larger root device.

---

### ISS-FIELD-004: Mirroring media through the REST API took the LiveORC host down

| Field | Value |
|-------|-------|
| **Date opened** | 2026-08-25 |
| **Site** | LiveORC server (AWS) |
| **Risk** | Production availability, data access |
| **Impact** | High — full outage, ~90 min |
| **Status** | RESOLVED (approach replaced) |

**Problem:**
TODO-114's mirror design pulled each video through the REST API
(`/api/site/4/video/{id}/playback/`). Run against production it managed
773 of 2630 files (7.0 GB) before the host stopped serving: HTTPS refused
connections, the SSM agent went offline, and the EC2 *instance*
reachability check went red while the *system* check stayed green — the
guest was wedged, the hypervisor was fine.

CloudWatch showed CPU credit **usage** climbing from ~0.9 to a pinned 7.05
per 5 min beginning at 14:05 UTC, which is the minute the first pull
started. A t3.large earns 36 credits/hour and this was consuming ~85.

**What it was not:**
Not disk. `df -h /` after recovery read 66% with 27 GB free, and TODO-114
had already documented `/` at 62%. The `No space left on device` messages
in the EC2 console log were from the **2026-08-10** boot — the console log
had not refreshed because the host had not rebooted since. That stale
evidence drove an incorrect diagnosis for some time; check the timestamps
on console output before trusting it.

**Resolution:**
A console reboot recovered the host in ~4 minutes. Nothing was lost — the
Let's Encrypt cert in `liveorc_webapp`'s writable layer survived unchanged
(expiry still 2026-11-08), which confirms the containers were *restarted*,
not recreated. `liveorc.service` is confirmed `disabled`, and it depends on
the failed `/mnt/s3-storage` mount, so it cannot start on its own.

The pull approach was abandoned rather than tuned. Media is now exported
host-side with `mirror/export-media-to-s3.sh`: `docker exec … tar -cf -`
streams straight into `aws s3 cp -`, throttled to 8 MB/s, touching neither
Django nor the host disk. The workstation then pulls from S3, putting zero
load on LiveORC. The full 30 GB moved in 61 minutes at a steady 8 MB/s
with no impact on the running service.

**Lessons:**
- Serving media through Django is expensive per byte in a way that copying
  the same files is not. The cost is the app server, not the bytes.
- `--delay` between requests paced politeness, not resource consumption.
  The throttle that worked was a bandwidth cap on the transfer itself.
- An hour-long job must not be tied to a Session Manager session. The
  first export died at 32% when the browser terminal timed out, killing
  `aws s3 cp` and orphaning a multipart upload. `systemd-run --unit=…`
  survives the disconnect; `journalctl -u <unit>` needs `sudo`.
- S3 multipart part timestamps are a good external progress signal for a
  job whose logs are silent: if the newest part stops advancing, the
  producer has died.
