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

### ISS-FIELD-011: Sukabumi was unreachable for 4.8 days while running normally; cause was an unfunded prepaid SIM

| Field | Value |
|-------|-------|
| **Date opened** | 2026-09-01 |
| **Site** | Sukabumi |
| **Risk** | Every conclusion drawn from row-absence during 2026-08-28 → 09-01 was wrong |
| **Impact** | **High** — reverses ISS-FIELD-010's diagnosis and the site-visit case |
| **Status** | OPEN |

**The station came back at 2026-09-01 18:00 UTC (09-02 01:00 WIB) after 4.8 days
of silence, and flushed its entire backlog.** ~4,500 buffered rows landed in two
minutes. They show it had been running the whole time.

| | wake-minutes/day | rows/day |
|---|---|---|
| healthy, 10–14 Aug | ~53 | 240 |
| the "outage", 28 Aug – 1 Sep | **135–140** | **895–940** |

It was awake roughly **15 hours a day instead of 1.6** — running nearly every
cycle to the Witty Pi's 25-minute backstop. What failed at 08-28 06:30 WIB was
the **uplink**, not the station.

**This invalidates the analysis built on row-absence.** The night-onset pattern,
the dawn windows, the three-missed-dawns argument and the site-visit case were
all reasoning about a station that was sitting there running. A visit would have
found it working. `station_gaps.py`'s premise — absence of rows records
downtime — failed completely here, and ISS-FIELD-010 already carried the warning
after the 06:00/06:30 rows appeared mid-outage; that signal was right and was
under-weighted.

**The power record we never had.** 679 V-IN samples across the outage, against
11 for the whole project before it:

| day | n | V-IN min .. max |
|---|---|---|
| 08-28 | 127 | 12.558 .. 13.231 |
| 08-29 | 140 | 12.341 .. 13.320 |
| 08-30 | 135 | 12.261 .. 13.177 |
| 08-31 | 137 | 12.149 .. 13.714 |
| 09-01 | 139 | 12.593 .. 13.098 |

Two results follow immediately, both on measurement rather than inference:

- **The pack is not the fault.** Five days at ~9x the normal duty cycle and
  V-IN never fell below 12.149 V. A battery that survives that is not the
  limiting component, and the deep-discharge theory does not apply to this
  event.
- **13.0 V is reached routinely** — 13.23, 13.32, 13.71 V. The recovery-voltage
  latch theory is dead on evidence, not argument. Every V-IN sample the project
  held before today came from a 3-hour pre-dawn window, which is why the pack
  looked incapable of reaching 13 V.

**The uplink cause, reported by Tom 2026-09-01: the Telkomsel prepaid account
had run out of money.** No balance, no data, and the modem stays registered and
healthy throughout — which is exactly the signature seen. It also closes the
second half of the question on its own: an unfunded SIM makes every upload fail,
a capture that cannot upload is a task that never finishes, the Pi runs to the
25-minute backstop on every cycle, and the 9x drain follows. One unpaid bill
produced the entire event.

Two things this exposes, both worse than the outage:

- **Nothing watches the balance.** A prepaid SIM that silently expires is a
  single point of failure for the whole station, and it is not instrumented,
  not alerted, and not on anyone's calendar. It will do this again.
- **Nothing noticed for 4.8 days.** The outage began as one missed upload.
  `db_watch.py` now alerts when sensor rows stop for 95 minutes and again when
  they resume, which would have caught this on day one.

Still unexplained: nothing in the software treats "no connectivity" as a
terminating condition. ORC-OS should fail a capture it cannot upload rather than
hanging the cycle to the backstop; that shape is shared with the
maintenance-mode chain in ISS-FIELD-010 and is the real fix.

**Collected in the window (2026-09-01 18:00–18:04 UTC).** Three `wp5d.log`
grabs; the deploy of TODO-117, the Witty Pi boot context and the orc-capture
verdict, all verified working on the station; and confirmation that `pi` can
read both `/var/log/wp5d.log` and the journal. The station's own capture in that
window passed its quality gate at 15,955 kbps and delivered, and disk free space
was 11.27 GB.

**CORRECTION 2026-09-01, from the full wp5d.log: the 9x drain never happened.**
The whole log was collected on the 18:30 UTC wake — 3.0 MB, 5,714 boots,
2026-04-07 to 2026-09-01. It is the Witty Pi's own record of when it powered the
Pi, so it settles the duty cycle by measurement rather than by inference from
row counts.

Each cycle logs `Startup reason` (after the RTC write, so the clock is real) and
`Exit now.` at shutdown. The difference is the awake time:

| day | cycles | median awake | awake min/day |
|---|---|---|---|
| 08-10 | 48 | 1.97 min | 94 |
| 08-11 | 48 | 2.05 min | 101 |
| 08-12 | 48 | 2.07 min | 100 |
| 08-13 | 48 | 2.05 min | 97 |
| **08-28** | 48 | **2.80 min** | **129** |
| **08-29** | 48 | **2.73 min** | **121** |
| **08-30** | 48 | **2.39 min** | **117** |
| **08-31** | 48 | **2.42 min** | **118** |

**The station ran 48 scheduled boots a day, unbroken, before and through the
outage**, and the duty cycle was not elevated at all. Outage mean 121.1 min/day
against a preceding-week mean (08-21 → 08-27) of 138.9 — **0.87x**. It was awake
slightly *less* than in the week before it went quiet. Against the quieter
08-10 → 08-13 window above it reads as 1.25x; daily awake time drifts between
roughly 95 and 215 minutes as a matter of course, and the outage days land in
the middle of that band. The baseline chosen is what produced the original
error, and neither baseline is near 9x.

The maxima rule out the backstop claim outright. Across the whole deployment —
5,244 measured cycles over 127 days — the median wake is 1.95 min and **only
eight cycles have ever exceeded 20 minutes**. Two of those eight fall on 08-25
and 08-27, both *before* the outage. During the outage the longest single wake
was 5.15 min, and the last three days never passed 2.95 min.

Three things follow:

- **"Awake roughly 15 hours a day instead of 1.6" is withdrawn.** The measured
  figures are ~2.0 h/day during the outage against ~1.6 h/day healthy. The
  earlier numbers came from wake-minutes inferred from sensor rows, and the
  healthy baseline of ~53 min/day was low by about half, which is what inflated
  the ratio.
- **ORC-OS was not hanging.** The task completed in ~2.7 minutes every cycle, so
  "a capture that cannot upload is a task that never finishes" is not what
  happened here, and the parallel drawn to the ISS-FIELD-010 maintenance chain
  does not apply. That open question is closed: there was nothing to explain.
- **The pack's exoneration is weaker than stated.** "Five days at ~9x duty and
  V-IN never fell below 12.149 V" was five days at ~1.25x duty. V-IN did stay
  above 12.149 V, so the pack is still not implicated in this event, but it was
  not tested under extraordinary load and nothing here proves it would survive
  one.

Caveat on the method: awake time is measured to the daemon's exit, not to the
power rail actually dropping, so every figure is a slight underestimate — but
equally so on both sides of the comparison, which is what the ratio rests on.

Full write-up, the 127-day dataset and the reproducible measurement script:
`findings/sukabumi_duty_cycle_2026-08-28_outage.md`,
`findings/sukabumi_duty_cycle_daily.csv`,
`liveorc_server/station-health/wp5d_duty_cycle.py`.

**wp5d.log covers only the last 20 hours** of the outage — `tail -n 400` was
sized for a seconds-long window, not a 4.8-day one. Within that span: 40
startups, 100% on-cadence, no gap over 45 minutes, all "Scheduled Startup".
`pounce.py` now grabs the whole file (gzipped, as a second grab once the tail is
already safe) so the next window collects the rest.

---

### ISS-FIELD-010: The station can be alive and uploading while completely unreachable — and "no sensor rows" is not the same as "down"

| Field | Value |
|-------|-------|
| **Date opened** | 2026-08-28 |
| **Site** | Sukabumi |
| **Risk** | Every recovery window is missed; outage durations may be overstated |
| **Impact** | **High** — undermines both the watcher's trigger and the premise of `station_gaps.py` |
| **Status** | OPEN |

**Caught live at 2026-08-28 17:21Z (00:21 WIB 08-29), 17.8 h into the current
outage.** The monitor's `sensor_age` went *down* — 1070 min to 1066 min. Age
can only fall if a newer row landed. Three measurements, taken together:

- **8 new rows appeared**, total 28959 -> 28967: exactly the sht40 (temp,
  humidity) and rg15 (interval, totalacc) sets for **06:00:25 and 06:30:26
  WIB on 08-28** — timestamps *after* the 05:30 "outage onset". They were
  absent from a query of that same window run at ~15:00Z.
- **`tailscale status` read `offline, last seen 24m ago`**, against `14h ago`
  earlier the same day. The node was on the tailnet around 00:01 WIB.
- A direct tcp/22 probe timed out. The same line read `tx 11232 rx 0`, which
  this entry originally read as proof the return path was broken. **That was
  wrong — see the correction below.**

**Two independent conclusions, both consequential.**

**1. The station was awake at 06:00 and 06:30 WIB on 08-28 and logged sensor
rows then.** It did not stop at 05:30. What stopped at 05:30 was the *upload*.
So for this event the row gap measures upload failure, not downtime — at least
for that first hour.

**Correction (later the same evening): the upload was NOT cut short.** This
entry first said the missing ds18b20/wittypi rows for those two wakes meant the
upload stopped partway through its file list. The upload order disproves that.
`orc-sensors-upload` sends oldest-mtime-first, and `sensors_logger` writes the
sensors in config-filename order — ds18b20, rg15, sht40, wittypi — so if
ds18b20 had logged at 06:00/06:30 its file would have sorted *ahead* of rg15
and sht40 and shipped first. It never arrived; both of theirs did.

So ds18b20 and wittypi **did not write rows at all** at 06:00 and 06:30. Their
reads failed. That is a more informative failure than a truncated upload: the
Pi booted far enough to run orc-sensors and read sht40 (I2C) and rg15 (UART),
while the 1-wire probe and the Witty Pi HAT both came back with nothing — which
is what a degraded or brownout boot looks like, and is worth checking against
the power-on reason once TODO-117 ships.

This is a direct qualification of `station_gaps.py`'s stated premise, that "the
station writes a sensor row every wake, so the *absence* of rows is a precise
record of when it was down". It is a good premise and most of the record still
supports it, but it is not unconditional, and this is the second time this
project has been bitten by silently failing sensor uploads (TODO-103, fixed
2026-07-07).

*What still holds:* a station that is up but cannot upload accumulates rows
locally and backfills them on reconnect. The 13 historical outages are still
empty in the record long after their recoveries, so those were genuine
downtime — except where the 30-day CSV rotation could have destroyed the
backlog first, which is a real caveat for gaps older than 30 days. **The
2026-08-15 analysis is unaffected**: it recovered 08-20, well inside the
rotation window, and the gap never filled in.

**2. The upload path and the SSH path fail independently, and the watcher
watches only the SSH path.** Sensor upload goes to LiveORC over the public
internet via LTE. SSH goes over the Tailscale overlay. On this wake the first
worked and the second did not.

**Correction — the `rx 0` reasoning was wrong (2026-08-28, prompted by Tom
asking whether SSH behaviour was new).** This entry claimed `rx 0` showed the
tailnet return path never came up. It shows nothing of the kind. Every offline
peer on this tailnet reads `tx 0 rx 0`; the only online one reads tx 4.5 MB /
rx 4.3 MB. `orc-sukabumi` reads `tx 3432 rx 0` purely because **our own watcher
is sending it a SYN every 15 seconds** and an offline peer does not answer. The
counters are our traffic, not a diagnosis, and they reset per relay session —
which is why the figure has read 11232, 6240, 7176 and 3432 within two hours.

There is **no evidence of an SSH-specific fault.** SSH worked normally right up
to the failure: read-only collections succeeded at 2026-08-27 18:00Z and
18:30Z, and the wittypi sensor deploy went in at 21:01Z, ninety minutes before
the station's last full wake at 22:30Z. What we actually have is a station that
is either off or awake for only seconds.

`station_watch.py` triggers on tcp/22 and explicitly declines to act on a fresh
sensor row, on the grounds that a row "proves the station booted within the last
cycle, not that it is powered on now", and that "a collect that cannot connect
is a window spent for nothing". The reasoning is sound as far as it goes and the
tcp/22 change was still right — but it is not a superset of "the station is
alive", and treating it as one made a live station look dead. A second watch was
added that polls the server for advancing sensor data, which is
Tailscale-independent.

**This still does not give us a collect, but for a plainer reason than the one
first written here.** The 2026-08-29 00:00 WIB wake registered with the
Tailscale control plane and pushed two files; the watcher was polling tcp/22
every 15 s throughout and never saw it open. A wake of a few tens of seconds is
not long enough for the tailnet path to establish *and* be used, and no poll
rate fixes a window that short. The case for pushing diagnostics rather than
pulling them is unchanged and if anything stronger — it does not depend on the
tailnet being broken, only on the window being too small to win.

**Could the 13.0 V recovery voltage be oscillating it? (Tom, 2026-08-28.)**
The observable half of that is correct — the station does come back and die
immediately — but the timing says the trigger is the schedule, not the
threshold. A voltage-triggered recovery fires at an arbitrary moment, which is
what the 10 historical off-grid recoveries look like (3.6–14.9 min off-slot).
Every wake since the failure is on the grid: 05:30, 06:00 and 06:30 WIB all
land 24–29 s past the slot, which is just the sensor-logging delay after boot,
and the 08-29 wake registered with Tailscale at **00:00:00.1 WIB**. Those are
scheduled alarms. A boot too brief to log or register would be invisible, so
fast oscillation is not excluded, only unsupported.

**The voltage data suggests the opposite failure, and it is worth more.** All
11 V-IN samples ever collected sit between 12.558 and 12.868 V — **the pack has
never been observed above 12.87 V, and the recovery voltage is set to 13.0 V.**
If that setting gates power-on at all, it does not cycle the station, it
**latches it off**, because the condition to return can never be met. That fits
the record better than oscillation: 10 of 13 outages needed a person on site,
and this is the first outage under this setting.

Two things stop that being a conclusion:

- **The samples are all from the pre-dawn trough** (02:30–05:30 WIB on 08-28),
  the bottom of the discharge. Daylight bulk charge on a 4S LiFePO4 should push
  well past 13.0 V, so "never reaches 13.0 V" is established for that window
  only. If the panel is charging at all, recovery should be reachable by
  mid-morning — and the station still does not come back, which pushes the
  question back to whether charge is reaching the pack (ISS-FIELD-009's
  BMS/charge-controller latch).
- **The setting may simply be inert.** The low-voltage threshold is still UNSET
  (menu option 7), and recovery voltage may do nothing without it — unconfirmed
  against the firmware, see ISS-FIELD-008.

**Actionable regardless:** whoever next attends the site should read the pack
voltage at the terminals and reconsider a 13.0 V recovery threshold on a pack
that has never been seen above 12.87 V under load. That is a cheap change to
get wrong in the safe direction, and it is already flagged in ISS-FIELD-008's
next steps.

**Is the tcp/22 probe itself wrong? (Tom, 2026-08-28: "I used to ssh
routinely, SSH would always be available when the station was pingable.")** A
fair challenge, and `port_open()` had never actually gated a successful collect
— it was only wired into the trigger path on 08-28, so it had no production
track record. Checked:

- **The probe is sound.** `port_open()` returns OPEN against three endpoints
  known to be listening, including port 22 on two of them
  (`openrivercam.endlessprojects.info:9443`, `github.com:22`, `127.0.0.1:22`).
  MagicDNS resolves `orc-sukabumi` to 100.64.12.52 correctly.
- **The station is not pingable either.** ICMP `ping -c 3` returns 100% packet
  loss and `tailscale ping` gets no reply at all.

So the rule holds rather than being violated: ping and SSH are failing
*together*, which is what an asleep station looks like, not a port-specific
fault. Combined with the `rx 0` retraction above, there is no evidence of any
SSH-specific problem at this station. What we have is a station that is off,
and wakes too short to catch — which is a window problem, and the reason
collection moved to `pounce.py`.

**RETRACTED: the recovery voltage is not gating power-on (2026-08-29).** The
entry above floated a 13.0 V threshold latching the station off. Tom objected
that the pack failing at the same moment he set the threshold is an implausible
coincidence. He is right, and the wake record settles it — after the setting
went in, the station hit **every scheduled slot for six days**:

| day | wake-slots hit (48 = all) |
|---|---|
| 08-22 | 48 |
| 08-23 | 49 |
| 08-24 | 55 |
| 08-25 | 65 |
| 08-26 | 67 |
| 08-27 | 62 |

(Counts above 48 are long wakes adding extra sensor ticks.) A threshold that
gated power-on could not produce a perfect boot record. Drop it.

**THE CENTRAL ANOMALY, RESTATED: this station works at night and not in the
day.** Two independent signals agree, and every power-shortage explanation
tried so far predicts the opposite:

- The **only** wake in this entire outage was at **00:00 WIB** — midnight.
- Video, since 08-24, occurs **only in 01:00–05:00 WIB**, 0 of 72 daylight
  awake hours.
- Since continuous monitoring began at 01:47 WIB on 08-29, there have been
  **zero wakes across all of 08-29 daylight**, 06:00–20:00 WIB. On 08-28 the
  last data was 06:30 WIB, as the day began.

Daylight is when the panel charges, when bus voltage is highest, and when a
flat pack should recover. A battery-capacity story, the ISS-FIELD-009 energy
chain, the recovery threshold and the thermal explanation **all predict
night-worst**. The station is day-worst. That is why each of them has failed to
fit, and it should be the organising fact from here rather than an oddity noted
at the end.

**Untested candidate, named but not built on:** many solar charge controllers
have a load output with a dusk-to-dawn or timed mode — a street-lighting
feature — that energises the load only at night, and a controller either set
that way or failing while charging would reproduce this signature without
anything about the battery having changed. There is no evidence for it yet. It
is recorded so a site visit can check the controller's mode and its load
terminals, which nothing in this investigation has ever looked at.

**What this changes for a site visit.** The controller moves to the top of the
list, above the battery. Ask for: the controller's make/model and load-output
mode, whether the Pi and the PoE injector are fed from the controller's LOAD
terminals or straight off the battery, and bus voltage measured at midday and
after dark.

**THE STATION IS FED FROM THE CONTROLLER'S LOAD TERMINALS (Tom, 2026-08-29).**
That makes the charge controller a **series element in the station's power
path**, not merely a battery charger, and it is the first fact that makes the
day/night asymmetry mechanically explicable.

Two stages that had been treated as separate problems are one fault
progressing:

| period | Pi power | camera / video |
|---|---|---|
| 08-23 → 08-27 | fine — 48 wakes/day, around the clock | **fails all day**; works 01:00–05:00 WIB only |
| 08-28 → now | **fails all day**; one wake, 00:00 WIB | nothing |

The load output first cannot carry the **large** load (PoE injector + camera,
~30 W with inrush) during the day, and later cannot carry even the **small**
one. Monotonic, day-worst, and worsening.

**A thermal mechanism fits, and it answers the objection that killed the
earlier temperature test.** A controller's load switch derates when hot, and in
daylight it is both sitting in a 33–38 degC enclosure and dissipating its own
charging heat. Earlier this entry rejected temperature because 18:00–23:00 WIB
has the same *enclosure air* temperature as 01:00–05:00 yet produces no video.
That test used the wrong body: the controller's heatsink lags ambient by hours,
having charged all day, and is only genuinely cool by ~01:00. Air temperature
and device temperature are not the same measurement, and the earlier
disconfirmation does not apply to the controller.

**Still a hypothesis.** Nothing here has been measured at the controller — this
investigation has never looked at it. Do not treat it as established.

**The decisive test is a rewire, not a measurement.** Feed the station from the
**battery terminals through a fuse** instead of the LOAD terminals. If daytime
operation returns, it is the controller, and the station is usable again the
same afternoon. It is a five-minute change with screw terminals, which is what
`DESIGN_SPECS.md` requires of any field repair. The LiFePO4 pack's own BMS
still provides low-voltage protection, so removing the controller's LVD from
the path does not leave the battery unprotected — though it does mean nothing
will disconnect the load on a deeply discharged pack except the BMS, which
should be stated to whoever does the work.

**Supporting measurements to take while there**, in priority order:

1. Voltage at the **LOAD terminals vs the battery terminals**, under load, at
   **midday and after dark**. A drop across the controller that appears in
   daylight and disappears at night is the fault, directly measured.
2. The controller's make, model and **load-output mode** — several have a
   dusk-to-dawn or timed street-lighting mode that energises the load only at
   night, which would produce this signature with nothing failing at all.
3. Whether the controller is hot to the touch in the afternoon.

**THE WEATHER DID NOT CHANGE, SO TEMPERATURE IS NOT THE CAUSE (Tom,
2026-08-29).** The thermal framing above needs correcting. Measured:

| | daily max enclosure temp |
|---|---|
| before 08-23 (45 days, full coverage) | median **36.0 degC**, mean 35.7, max 39.6 |
| from 08-23 (5 days) | median **35.5 degC**, mean 36.0, max 37.9 |

Identical, marginally cooler since the fault. And **the hottest day on record —
39.6 degC on 2026-07-26 — falls inside the stretch when the station was working
perfectly**, 48 wakes/day with full 24-hour video. It has never failed on a day
as hot as ones it ran through without trouble.

So temperature can be the *stress that reveals* a fault whose margin has eroded,
but it cannot be what changed. Something in the station changed, and the dating
is tight: **the enclosure was opened on 08-20 and 08-21** (the two button-press
recoveries), and the degradation begins **08-23**.

**A loose or oxidising connection fits every feature, and needs nothing
environmental to move:**

- It dissipates I²R, so it is worst when current is highest — daylight, with
  the PoE injector and camera energised. That is the day-worst signature.
- Its resistance rises with temperature, so heating begets heating. Progressive
  and self-accelerating.
- It degrades further with each thermal cycle, so onset is dated to a
  disturbance rather than to weather.
- It fails the large load first and the small load later, which is exactly the
  08-23 (camera) then 08-28 (Pi) progression.

**This is the hypothesis TODO-117 was built to measure**, and the framing is
already in `wittypi.conf`: an effective source resistance separating *ohms*
(fuse holder, terminal, crimp) from *milliohms* (worn pack). The single sample
with a genuine load step showed a **0.479 V sag** (04:30:27, vin_min 12.318 /
vin_max 12.797), which is large. The fit was never completed because voltage
and current came from different instants — the defect the paired-sampling
change corrects. Once TODO-117 ships, a handful of wakes settles ohms vs
milliohms directly.

**Site brief, reordered again — connections before the controller:**

1. `/var/log/wp5d.log`, before touching anything.
2. **Every connection in the power path, checked under load**: the controller's
   LOAD screw terminals, the fuse holder, every crimp and lug. Warm or
   discoloured under a daytime camera cycle is the finding. Re-torque and
   inspect for oxidation — and note that simply re-seating them may *clear* the
   fault, so measure and photograph before disturbing anything.
3. Voltage drop LOAD terminals vs battery terminals under load, midday and
   after dark.
4. The bypass (battery through a fuse) as test and interim fix.
5. TODO-117 deploy.

Item 2 outranks the controller because a joint explains the dated onset and the
controller does not: the controller was not touched on 08-20/08-21, and its
thermal environment is unchanged.

**ALTERNATES THAT REQUIRE NO COINCIDENCE (Tom, 2026-08-29).** Tom's objection:
the scenarios above keep needing a sudden change on a specific date, and the
likelier story is that the recovery voltage badly aggravated a **pre-existing**
condition. That is better-disciplined than what preceded it and the alternates
below are recorded as first-class, not as fallbacks.

**First, the device's own menu, which should have been read before any of this
was theorised** (2026-08-27 capture, section 3):

```
  7. Set low voltage threshold                  <-- no value in brackets: UNSET
  8. Set recovery voltage threshold [13.0V]
  V-IN: 12.717V   V-OUT: 5.290V   I-OUT: 0.995A
```

The station was running normally at **12.717 V**, well below 13.0 V, so the
recovery threshold is not a gate on *running*. It is a live setting sitting
above where this system actually operates.

**Second, a constraint that had been walked past and that breaks most of the
scenarios above, including the connection one.** Capture works 01:00–05:00 WIB
— the pre-dawn trough, the pack's *lowest* state of charge — and fails
18:00–00:00 WIB, straight after a full day of charging, at its *highest*.
**Capture is anti-correlated with state of charge.** This is inference from
solar physics, not measurement — every V-IN sample we hold is from 02:30–05:30
— and confirming or killing it is the single most valuable thing TODO-117 will
deliver, because it needs only V-IN across a full day. If it holds, every
capacity-shortage explanation is dead, including the ones this entry has been
building.

**A. Smooth margin erosion crossing a step — no event at all.**
Nothing happened on 08-23. Something in the power path has degraded for months
(13 outages since April); 08-23 is where a smooth decline crossed the camera's
inrush requirement and 08-28 where it crossed the Pi's. The dates are
thresholds being crossed, not things happening. Requires no disturbance, no
setting, and no weather change, and it fits the two-stage progression better
than any discrete-event story.
*Discriminator:* source resistance trend once TODO-117 ships — a rising trend
with no step is this; a step is an event.

**B. Two cascaded voltage gates that do not know about each other — Tom's, made
mechanical.** The station is LOAD-fed, so the Witty Pi's V-IN *is* the
controller's LOAD output. The controller carries its own LVD and reconnect
thresholds, almost certainly factory-set for **lead-acid** on a reused system,
which places them inside a LiFePO4 pack's normal working band. Adding a second
gate at 13.0 V puts two independent cut/restore points in series with no
knowledge of each other. A marginal pack that previously just sagged now trips
a gate and must reach a higher voltage to clear it than the system can present
under load. **The condition is old; the setting is what made it
unrecoverable.**
*Discriminator:* read the controller's LVD/reconnect values and chemistry
profile on site, and check whether Witty Pi V-IN reads **0 V** (load
disconnected) rather than merely low — the two are completely different faults
and the current sampling cannot tell them apart.

**C. BMS cell imbalance under load.** One weak cell sags under the camera's
draw, the BMS opens, the load drops, voltage recovers, the BMS recloses. Worst
at highest current, progressive as imbalance grows, no coincidence. This was
the leading hypothesis before ISS-FIELD-009 displaced it, and nothing has
actually falsified it.
*Discriminator:* per-cell voltages at the pack; and V-IN collapsing abruptly to
zero rather than sagging.

**D. Controller output stage degrading while actively switching.** With no PV
at night the controller passes battery to load essentially statically; in
daylight it switches at high frequency to regulate charge. A degrading output
stage is far worse under switching. Day-worst, progressive, weather-independent.
*Discriminator:* LOAD-vs-battery terminal drop under load, midday against after
dark; and whether ripple is visible on the LOAD output while charging.

**What none of these explain yet** is the 18:00–00:00 dead zone: six hours
after sunset, controller passive, pack full, and still no capture. Any
successful theory has to account for that, and at present none of the four
does. It is the sharpest unexplained fact in this entry and should not be
smoothed over.

**TOM'S THEORY, AND WHAT THE DATA DOES TO IT (2026-08-29).** Proposed: the
disk failures extended runtime and completely discharged the battery in a way
never done before; the station then tries to boot before the pack has any depth
of charge and drops below shutdown voltage.

**The drain component is not supported — and its failure strengthens the
conclusion.** Long-wake ticks in the four days before this outage total **65**.
April's worst four-day window is **659**, an order of magnitude more; May
reaches 201. This outage was preceded by a *mild* drain by this station's own
history.

That inverts into a quantitative argument for pack degradation: **if 65 units
of drain now does what 659 did not in April, the usable capacity is a fraction
of what it was.** The discharge may well have been the deepest ever in relative
terms — the pack simply got there on a tenth of the energy. The failure
profiles agree:

| | drain / 4 d | outages | character |
|---|---|---|---|
| April | 659 | 6 in 4 days | shallow, self-cleared in hours |
| August | 65 | rare | catastrophic, days, needs a person |

High drain against decent capacity gives frequent shallow failures that clear
themselves. Low drain against a spent pack gives rare unrecoverable ones. That
is the transition, reached from the other direction.

**The boot-before-depth mechanism, extended, answers the daytime question —
which nothing else in this entry has.**

1. First true deep discharge -> **BMS undervoltage lockout**; the pack
   electrically disconnects.
2. The MPPT controller sees ~0 V where the battery should be and **will not
   start** — most refuse to output into a disconnected pack. No charging
   happens at all, all day, in full sun.
3. Hours of rest relax the cells above the BMS release threshold; it recloses,
   the station boots (**00:00 WIB**), the load collapses the cell in seconds,
   the BMS reopens.
4. Repeat.

Nothing happens during the day because the pack is not merely low, it is
*absent*. That accounts for two dawns producing nothing, for the single wake
arriving in the small hours after maximum rest, and for 10 of 13 outages
needing a person — a deadlock cannot clear itself.

**It makes a sharp, pending prediction.** `wp5d.log` should show dense
`Scheduled Startup` entries every 30 minutes right through the outage: the
Witty Pi firing faithfully into a pack that cannot hold it. That is exactly the
DYING EARLY verdict `wp5d_verdict.py` is built to return, and it is what
`pounce.py` is waiting to collect.

**A related test was run and came back inconclusive**, recorded so it is not
re-run in hope. If concurrent load were what blocks capture, long-wake hours
and capture hours should be mutually exclusive. Since 08-24: capture in 3/23
long-wake hours (13%) against 18/80 short-wake hours (22%). Both low, and the
two populations sit in different clock hours by construction, so the comparison
mostly measures the hour effect. It neither supports nor refutes.

**Still unexplained by this theory**, and it should not be papered over: the
18:00–00:00 dead zone, and the 01:00–05:00 capture window of 08-24 to 08-27,
which predates the total discharge and belongs to the run-in rather than the
deadlock.

**MAINTENANCE MODE EXPLAINS 9 OF THE 13 OUTAGES (2026-08-29).** Tom asked that
room be left for human error — forgetting to take the station out of
maintenance mode, and the like. That turned out to be the most productive
prompt of the investigation, though not in the way either of us expected.

**What maintenance mode does.** `orc-maintenance-check` fetches
`pi/<station>/station_mode` from the public repo `tom-jordan23/orc-pmi-stations`
on every boot. In `maintenance` it touches `/run/orc-maintenance-mode`, which
makes `orc-capture` **skip capture entirely** — and, in the script's own words,
"the Pi stays awake for the full Witty Pi ON window". That is exactly the
signature this investigation has been chasing:

- no video (capture skipped)
- long wakes (full 25-min ON window instead of ~2 min — the 12x drain)
- sensors logging normally throughout (independent of capture)

**It was NOT left on before this outage.** The file currently reads
`production`, and its last change was **2026-06-24**. Checked directly against
the GitHub API, the same endpoint the station uses.

**But its history is a natural experiment, and the chain fires every time.**
Seven maintenance windows totalling 549 h, 17% of the observation span:

| | long-wake ticks | rate |
|---|---|---|
| inside maintenance | 870 | **1.59/h** |
| outside | 477 | 0.18/h |

**8.8x the long-wake rate inside maintenance mode.** And the outage record:

| onset (WIB) | duration | relation |
|---|---|---|
| 04-17 06:23 – 04-20 14:13 (six outages) | 0.9–19.5 h | **all inside** the 04-08→04-21 window |
| 05-11 23:01 | 38.0 h | inside |
| 05-16 00:47 | **9.3 d** | inside |
| 06-25 04:30 | **7.3 d** | 7 h after a window closed |
| 05-02, 07-02, 08-15, 08-20 | | not associated |

**Nine of thirteen**, including the two longest in the historical set.

**Three consequences.**

1. **The extended-runtime → drain → outage chain is confirmed, not merely
   inferred.** Nine outages have an independently known cause for the extended
   runtime, and the chain completes every time. Tom's deep-discharge theory
   rests on measured ground now.

2. **Earlier statistics in this issue were contaminated, and one inference is
   withdrawn.** The "April cluster" agonised over above **is** the April
   maintenance window. And the headline result — long wakes precede 9/12 onsets
   at p = 2.7e-07 — is real as an association but its causal reading was wrong:
   maintenance mode was generating both terms. The chain survives on the
   natural experiment; the inference drawn from that correlation does not.

3. **It sharpens the open question rather than closing it.** Maintenance has
   been off since 06-24, so the genuinely unexplained outages are **08-15
   (5.4 d)** and **the current one** — and both carry the full maintenance-mode
   signature with maintenance mode not set. Something is making capture *fail*
   the way maintenance mode makes it *skip*. That is ISS-FIELD-009's territory
   (disk pinned at the purge threshold, pyorc failing, task never completing),
   and this is the strongest support that entry has had.

**Process finding, worth acting on independently of the fault.** Maintenance
mode has been left on for multi-day stretches repeatedly — 05-14 to 05-19 is
five days, 06-21 to 06-24 three — and nothing anywhere warns about it. It costs
roughly 12x the energy budget and produces no data at all. A station in
maintenance for more than a few hours should raise an alert; the mode is
readable from the GitHub API without touching the station, so the check is
trivial and could sit alongside the TODO-103 staleness alerting.

**COULD THE STATION BE STUCK IN MAINTENANCE MODE? (Tom, 2026-08-29.)** Asked
because the disk problems might have gummed up the maintenance chain. The
literal version is ruled out by design, but the question lands next to a worse
failure mode that had not been noticed.

**The flag cannot be stuck.** `orc-capture` tests `/run/orc-maintenance-mode`,
and `/run` is tmpfs — the flag is destroyed on every power cycle and recreated
only if GitHub returns `maintenance`. `orc-capture`'s own comment says so.
Every failure path in `orc-maintenance-check` also `rm -f`s the flag: missing
config, unresolvable hostname, unreachable GitHub, and any unrecognised value
all fall through to production. There is no path where a failure leaves the
station in maintenance.

**But the CHECK can stall the capture chain, and that is a real exposure.**

```
After=network-online.target
Before=orc-api.service
Type=oneshot
```

The fetch retries **12 times at up to 15 s each — up to 180 seconds** — and the
unit is ordered *before* `orc-api`. So an unreachable or slow GitHub delays the
capture chain by up to three minutes on every boot, which is longer than an
entire healthy wake (~2 min). That would produce **long wakes and missing video
with maintenance mode never set** — precisely the "capture fails the way
maintenance mode makes it skip" gap this issue is trying to close, and it needs
no hardware fault at all.

It also offers the first candidate mechanism for the **diurnal pattern**, which
nothing else has explained: capture succeeding only 01:00–05:00 WIB and failing
18:00–00:00 matches Indonesian mobile-network load, quietest in the small hours
and heaviest in the evening. That is a hypothesis, not a finding — sensor
uploads to our own server succeeded at all hours over the same period, so any
degradation would have to be specific to the GitHub API path rather than to
connectivity in general. Worth noting that these are different endpoints,
different TLS, and only one of them is retried for 180 s in front of capture.

**`pounce.py`'s primary grab now collects the evidence** so the next catch
settles it: `ls -la /run/orc-maintenance-mode` (the flag directly, rather than
by tmpfs argument), `findmnt /run`, the last 40 `orc-maintenance` journal lines
(which branch ran, and the timestamps show how long the fetch took), and
`systemctl status orc-maintenance-check` — alongside `wp5d.log`, `df -h /` and
`vcgencmd get_throttled`.

**THE STALL HYPOTHESIS DOES NOT COVER MIDDAY, AND THERE ARE TWO NO-CAPTURE
REGIMES (2026-08-29).** Tested immediately rather than left to look stronger
than it is. Since 08-24, by WIB hour:

| window | videos | long-wake ticks | reading |
|---|---|---|---|
| 01:00–04:00 | **29** | 11 | capture works |
| 11:00–17:00 | 0 | **0** | capture fails, wake stays short |
| 18:00–23:00 | 0 | **30** | capture fails, wake runs long |

Midday has neither capture nor stalls, so a boot stall cannot be the general
explanation: the station wakes, finishes quickly, and produces nothing. Evening
is the opposite failure — it hangs. **These are two different regimes and have
been treated as one ("no daytime video") throughout this issue.**

**A limitation of the instrument, which should have been stated earlier.** The
"long wake" detector only sees wakes longer than about five minutes, because it
counts extra 300-second sensor ticks. A capture that dies on the 90-second
`CAMERA_BOOT_TIMEOUT` produces no extra tick and is invisible to it. So
throughout this investigation **"short wake" has never meant "healthy wake"** —
it means "under five minutes", which includes a fast camera failure. Every
statement here of the form "the station was running normally at N wakes/day"
carries that caveat, including the 48-slots-per-day evidence used above to
clear the recovery-voltage theory. That evidence still stands for *booting*; it
was never evidence that the wakes were doing useful work.

The midday regime is consistent with `orc-capture` failing fast — camera not
answering, or the quality gate rejecting three attempts — and the evening one
with something hanging. Both are visible in `orc-capture`'s own log, which
nothing uploads. That is the second artefact the station should be pushing, and
the argument for it is now the same as for the Witty Pi power-on reason.

**Next steps**

- [ ] **Determine whether `rx 0` is systematic.** One wake is not a pattern.
      Every future wake should be checked for whether the tailnet return path
      establishes. If it never does, remote recovery is impossible and the
      station needs an out-of-band path.
- [x] **Reconsider the collection path — done 2026-08-28, awaiting deploy.**
      `read_wp5d_boot_context()` parses `/var/log/wp5d.log` and the wittypi row
      now carries `power_on_reason_code`, `prev_shutdown_reason_code`,
      `downtime_s` and `boot_age_s`, plus the raw reason strings as text.
      It rides the existing wittypi CSV rather than a new file, deliberately:
      the 08-28 wake died partway through its upload queue, so a new file would
      put the most valuable datum we have at the back of exactly that queue.

      `downtime_s` is the one that matters — measured by the station's own
      clock across the gap, it reports how long the station was really off
      regardless of whether any row reached the server, which is precisely what
      the row record could not tell us on 08-28.

      The text columns do not parse as floats, so `sensor-ingest/app.py` skips
      them and only the codes reach Grafana; the raw text stays in the CSV on
      the server for when a code comes back 0 (= reason string we have no
      mapping for). Only "Scheduled Startup"/"Scheduled Shutdown" have ever
      been observed, so every other mapping is an explicit guess that degrades
      to 0 rather than to a wrong code.

      Tested end-to-end against the real ingest parser, including that a comma
      in a reason string cannot shift the numeric columns. **Not deployed** —
      the station has been unreachable since. Ships with TODO-117.
- [ ] **Confirm `pi` can read `/var/log/wp5d.log`.** Unverified: the 08-27
      capture proves only that *root* could, because the collector ran under
      sudo. If pi cannot, the boot context degrades to code -2 and we learn
      nothing. `orc_deploy_wittypi_sensor.sh` now checks this as the service
      user and grants `o+r` if needed, but that may not survive wp5d rotating
      its log — so watch that `power_on_reason_code` stays above -2.
- [ ] **Re-check outage durations for upload-failure contamination**, at least
      for gaps under 30 days old where backfill would have survived rotation.
- [ ] Alarm on a station that is uploading but unreachable. It currently reads
      as identical to a dead one.

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

**THE LONG-WAKE PRECURSOR, TESTED ACROSS THE WHOLE RECORD (2026-08-28).**

Everything above argues the energy chain from one or two nights. With the
station unreachable there was no new station-side evidence to collect, but the
claim is testable server-side: if extended wakes drain the pack, onsets should
be preceded by long wakes far more often than an ordinary window is. All 13
outages plus the ongoing one, against every non-precursor window as baseline.

Two corrections had to be made before the numbers meant anything:

- **The April cluster.** Six of the 13 outages fall in 2026-04-17..20, a
  stretch when long wakes ran continuously. On the raw comparison precursor
  windows looked overwhelming (median 23 long-wake ticks vs 0 baseline), but
  temporal clustering alone reproduces that. Reported split below.
- **Dead windows.** The 07-02 10:43 and 08-20 10:39 onsets each begin *minutes
  after the previous outage ended*, so their preceding 6 h is mostly inside
  that outage — no rows, therefore zero long wakes by construction. Scoring
  them as "no precursor" would have been backwards. Both are excluded by a
  coverage screen (observed wakes / wakes expected at the duty cycle >= 80%).

Screened result, 6 h window:

| | with a long wake in the prior 6 h |
|---|---|
| outage onsets (12 usable of 14) | **9/12 = 75%** |
| baseline windows | 40/418 = 10% |
| | Fisher exact, one-sided: **p = 2.7e-07** |
| post-April onsets only | 3/6 = 50% |
| post-April baseline | 26/370 = 7% |

**This is the first real quantitative support the energy mechanism has had.**
It survives removing the April cluster, though on 6 post-April onsets that
half of the test is suggestive rather than conclusive.

**But long wakes are NOT necessary, and that is the more important half.**
Three usable onsets had none in the preceding 6 h, and two had none anywhere
in the preceding **72 h**:

| onset (WIB) | outage | clean cadence before it | long wakes in 72 h |
|---|---|---|---|
| 2026-05-02 06:31 | 1.0 h | 9.4 d | 0 |
| 2026-08-15 01:30 | **5.4 d** | **42.6 d** | 0 |
| 2026-08-28 05:30 | ongoing | 0.36 d | 58 (17 in 12 h, 0 in 6 h) |

2026-08-15 is the one that matters: **the second-longest outage on record came
out of 42.6 days of unbroken clean cadence with no extended wake within three
days.** No amount of disk space would have prevented it, because there was no
drain to prevent. There is a second failure path, it produces long outages, and
this entry does not describe it.

That also cuts against the chain independently: ISS-FIELD-007 has processing
errors rising through July (24%) and August (32%) as the disk filled, yet the
station ran clean from 07-03 to 08-15. Disk pressure and extended wakes are not
locked together the way this entry assumes.

**A temperature explanation was tested and killed.** The two clean-cadence
outages had the coldest 72 h minima in the onset table (19.8 and 18.8 degC),
which looked like a lead. It is not: 18.8 degC is only the **12th percentile**
of the site's own distribution, the baseline reaches 17.2 degC, and the coldest
decile (<= 18.0 degC) contains **zero** onsets. Recording it because eyeballing
a 12-row table is exactly how the April cluster nearly got through.

**Caveats, stated rather than buried.** This is association, not mechanism — a
long wake and an outage could share a third cause (a failing capture) with
energy playing no part. Long wakes are episodic and clustered, which inflates
any window-based comparator; the post-April split is the honest number. And the
"ongoing" row is the current outage, whose duration is not yet known.

**What it changes.** The purge was worth doing and the drain is real, but the
open question is no longer "is the disk the cause". It is **what killed the
station on 2026-08-15**, since whatever that was is still present and is the
better match for the current outage's clean final 6 hours. Reproduced by
`liveorc_server/station-health/station_gaps.py` plus the analysis in this
entry; the scripts are throwaway, the queries are read-only.

**WHAT HAPPENED ON 2026-08-15 (investigated 2026-08-28).**

The precursor test above made 08-15 the most informative event on record: a
5.4-day outage out of clean cadence. Four things were checked, and the first
three all came back negative.

**It did not die mid-cycle.** The final wake at 01:30 WIB wrote a complete row
set — sht40 temp and humidity, ds18b20, rg15 interval and total, all five
values, T23.0 degC / RH 77 / 0.0 mm. The station finished its wake and shut
down normally; the next scheduled boot simply never happened. (An apparently
truncated 01:00 wake is not a signature: the identical split — sht40 at :00 and
ds18b20 spilling to :01 — appears in the healthy 08-13 control. It is the
one-wire read taking an extra second.)

**There was no drain event.** Zero extended wakes in the preceding 72 h, and
exactly **48 sensor rows per day for 42 consecutive days** — the duty cycle
delivered perfectly, 2026-07-04 through 08-14, no missed wake and no long wake.

**Solar harvest was not declining.** With no panel telemetry the available
proxy is the enclosure's diurnal swing (daily max minus min sht40). Over those
42 days: median 15.3 degC, first third 15.1, last third 14.3 — flat. 08-14
itself swung 16.7, above median. A slowly failing charge source would have to
show here and does not.

**What did turn up is in how the outages END.** On-cadence wakes hold the Witty
Pi's :00/:30 grid very tightly — median 0.37 min off-slot, p99 1.20 min, over
4915 wakes. Recoveries do not:

| onset (WIB) | duration | recovery | off-slot |
|---|---|---|---|
| 2026-04-17 06:23 | 4.7 h | 04-17 11:03:39 | 3.6 min |
| 2026-04-17 15:01 | 2.1 h | 04-17 17:10:41 | 10.7 min |
| 2026-04-18 11:33 | 0.9 h | 04-18 12:26:10 | 3.8 min |
| 2026-04-19 08:20 | 4.9 h | 04-19 13:17:22 | 12.6 min |
| 2026-04-19 14:09 | 18.3 h | 04-20 08:30:03 | 0.1 min — on grid |
| 2026-04-20 14:13 | 19.5 h | 04-21 09:43:09 | 13.1 min |
| 2026-05-02 06:31 | 1.0 h | 05-02 07:31:10 | 1.2 min — on grid |
| 2026-05-11 23:01 | 38.0 h | 05-13 13:03:54 | 3.9 min |
| 2026-05-16 00:47 | 9.3 d | 05-25 07:00:21 | 0.3 min — on grid |
| 2026-06-25 04:30 | 7.3 d | 07-02 10:38:26 | 8.4 min |
| 2026-07-02 10:43 | 23.1 h | 07-03 09:47:08 | 12.9 min |
| **2026-08-15 01:30** | **5.4 d** | **08-20 10:39:01** | **9.0 min** |
| 2026-08-20 10:39 | 21.6 h | 08-21 08:14:56 | 14.9 min |

**10 of 13 outages end on an unscheduled boot** — 3.6 to 14.9 minutes off-slot,
against a p99 of 1.2 min for a scheduled startup. These outages are not being
cleared by the Witty Pi alarm. Power is being restored to a station that was
not going to wake up by itself, which is precisely the TODO-116 failure mode
stated as a measurement rather than an anecdote.

And **every one of the 13 recoveries falls between 07:00 and 17:10 WIB.** None
overnight, where 58% of a uniform distribution would land.

**Two readings of that, and the evidence here does not separate them.**

1. *Someone goes to the site and presses the button.* Fits the daylight-only
   window and the off-grid boots exactly.
2. *Power returns on its own in daylight* — e.g. a BMS that opened on
   undervoltage re-closing once solar has put charge back, which boots the Pi
   immediately rather than at an alarm. This also predicts off-grid daytime
   boots.

Reading 2 has a problem: solar should re-close a BMS within hours, not 5.4 or
9.3 days. That gap is explained if the charge controller will not start into a
pack the BMS has disconnected — a known MPPT behaviour when it sees no battery
voltage — which latches the station off until a human intervenes. That would
make reading 2 collapse into reading 1 for the long outages while still being
the trigger, and it is the best mechanism currently on the table for a station
that dies abruptly, shows no precursor, and then stays dead.

**Settled by asking (Tom, 2026-08-28): someone pressed the button.** The
08-20/08-21 recoveries were attended, and the 13.0 V recovery voltage was
configured some time after that. Reading 1 is correct for the off-grid boots.
**The station does not clear these outages by itself.**

**Which makes the three on-grid recoveries a separate mode, and they split
cleanly by clock:**

| mode | n | recovery window (WIB) | reading |
|---|---|---|---|
| on-grid (<= 1.2 min off-slot) | 3 | 07:00, 07:31, 08:30 | scheduled alarm finally succeeded |
| off-grid (3.6–14.9 min) | 10 | 08:14 – 17:10 | attended; button press |

The on-grid three all land in the 90 minutes after sunrise (~05:50) and nowhere
else. That is what a genuine self-recovery should look like: the pack takes
first charge at dawn, the next scheduled alarm has enough to boot, and the
station rejoins its own grid. The off-grid ten spread across the working day,
which is what site attendance looks like. So the station *can* self-recover
from a missed wake — it did so three times, once after 9.3 days — but it
usually does not, and 10 of 13 times a person had to go.

**Operational consequence for the outage running now.** It began 08-28 05:30
WIB. Two dawns (08-28, and 08-29 if it runs that long) are the moments an
unattended recovery would show, on-grid, between 07:00 and 08:30 WIB. The
08-28 dawn passed with nothing. On the base rate — 10 of 13 needing a visit,
and night onsets running 38 h to 9.3 d — this most likely needs a site visit,
and that call should not wait on the hope of a self-clear.

Note also that the 13.0 V recovery voltage postdates every outage in the table
above except the current one, so this outage is the **first test of that
setting**. Against that, the low-voltage threshold is still UNSET, and recovery
voltage may be inert without it (see ISS-FIELD-008) — which would mean the
setting cannot help here and the station is waiting on a person.

The remaining question is the *trigger*, not the recovery: what stops a station
that has run 42 flawless days. The Witty Pi power-on-reason log is the artefact
that speaks to it, still ungrabbed — see TODO-117 and the watcher.

**Corrected en route.** The first version of this test calibrated grid
discipline on "every wake outside an outage", which includes the 5-minute
long-wake ticks — off-grid by construction. That put p99 at 13.8 min and made
all 13 recoveries look scheduled, i.e. the exact opposite conclusion. The
reference set has to be wakes arriving one duty cycle apart.

**VIDEO CAPTURE COLLAPSED TO A 01:00–05:00 WIB WINDOW ON 2026-08-23.**

Prompted by Tom noticing no daytime video. Checked against the API inventory
(`mirror/orc_inventory.py --institute 1 --site 4`, 2649 records), and the
observation is correct and sharper than expected.

| day (WIB) | videos | first–last | daytime 06–18 |
|---|---|---|---|
| 08-22 | 45 | 00:01 – 23:31 | 22 |
| 08-23 | 14 | 00:01 – 09:01 | 5 |
| 08-24 | 6 | 01:31 – 05:01 | **0** |
| 08-25 | 6 | 01:31 – 04:31 | **0** |
| 08-26 | 7 | 01:45 – 05:03 | **0** |
| 08-27 | 6 | 01:01 – 04:01 | **0** |
| 08-28 | 6 | 01:31 – 04:31 | **0** |

Since 08-24 the station has produced **6–7 videos a day against 48 wakes**, all
inside 01:00–05:00 WIB, while logging a full 48 sensor rows a day — it was
awake the whole time. By awake hour since 08-24: 19 of 20 hours in 01:00–04:00
produced video; **0 of 72 hours from 06:00 to 00:00 did.**

**The timestamps are trustworthy.** Video times align to the minute with outage
boundaries derived independently from sensor rows: capture runs every half hour
through 08-14 and stops at 08-15 01:31, one minute after the 01:30 onset;
resumes 08-20 10:40 against the 10:39 recovery, and 08-21 08:16 against
08:14:56. Two datasets that have never been compared before agree exactly.

**It is not temperature.** Video never occurs above 25.9 degC, which looked like
a thermal ceiling, but hours 18:00–23:00 and 06:00–07:00 sit at the same
temperatures and produced nothing at all. Temperature is collinear with hour
here and hour is what survives.

**It is not a configured window.** `orc-capture.conf` has no hour-based gate;
its only clock settings are `NIGHT_START=11:00`/`NIGHT_END=23:00`, which are
UTC and switch the camera *profile* at 18:00/06:00 WIB. Those boundaries do not
match 01:00–05:00.

**It is not the upload.** Every record that exists reached the server within
~50 seconds of capture — median lag 0.8 min, max 0.9 min over the last 60
records. There is no sync backlog behind this. **The missing daytime videos
were never captured**, which distinguishes it from the 2744 historic
never-synced videos above.

**Unconfirmed chain worth testing, because it would unify this entry.**
`orc-capture` failing outside that window would produce exactly what is
observed AND explain the long wakes: a capture that never completes is an
ORC-OS task that never completes, so `shutdown_after_task` never fires and the
Pi runs to the Witty Pi's 25-minute backstop. The timing fits — long wakes
resume on 08-23/08-24, the same day daytime capture stops, and they fall
outside 01:00–05:00 (08-24 06:05–10:05, 08-25 07:05–09:35 and 19:35–22:15,
08-27 18:35–21:00). If true, the 12x energy drain and the video collapse are
one fault, not two.

Note it cuts against the obvious power reading, though: the camera is
power-cycled with the Pi (`RELAY_MODE=cycle`) and draws most on IR at night, so
a supply that cannot start the camera should fail at night first. It does the
opposite. Do not assume the cause is power without evidence.

**The day/night camera profile was proposed and does not explain it (Tom,
2026-08-28).** Worth testing — the working window does sit inside the night
profile — but the profile is not the discriminator:

- The night profile is one continuous span, **18:00 → 06:00 WIB**
  (`NIGHT_START=11:00`/`NIGHT_END=23:00`, UTC on the station). Within that
  single span, 18:00–00:00 WIB produced video in **0 of 24** awake hours and
  01:00–04:00 WIB in **19 of 20**. Nothing switches at 01:00 or 05:00 WIB, so
  a wrong profile cannot be what separates them.
- The "stuck in night mode" mechanism is not present either.
  `orc-camera-profile-switch` writes its state file only *after* a successful
  `camtool push` — it exits non-zero before the write if the push fails — so a
  failed push leaves the state stale and the next wake retries. There is no
  path where a failed transition is recorded as a completed one.
- The variant "captured, but failed to process because settings were nocturnal"
  is excluded by the record shape: that produces an `error` record, and there
  are **zero daytime records of any status** since 08-24.

**A latent fragility this did surface, though.** The switch pushes only on
transition — twice a day — and trusts a local state file to say what the camera
holds. But `RELAY_MODE=cycle` power-cycles the camera on every wake, ~48 times
a day. If a power cycle ever reverted the camera's stored image settings, the
state file would still read "night", no push would occur, and the camera would
stay wrong until the next scheduled transition. Not the cause here, but it
should be a `--force` push on some cadence, or a read-back verify, rather than
state we assume.

Note also that no timer in this repo fires near 01:00 WIB / 18:00 UTC — the
only one is `orc-sensors` at 60 s — so whatever anchors the window is ORC-OS
side or on the station, not in our configuration.

**What would settle it** is `orc-capture`'s own failure reason — the quality
gate it tripped, or whether the camera answered at all — which nothing
currently uploads. That is the same gap ISS-FIELD-010 just closed for the Witty
Pi power-on reason, and the same fix applies: push the last capture outcome
with the sensor CSVs instead of waiting for an SSH window.

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

**THE DAYTIME VIDEOS WERE CAPTURED. THE UPLOAD FAILED. (2026-09-01.)**

Measured from ORC-OS's own database on the station, `/home/pi/.ORC-OS/orc-os.db`,
read during the 19:31 UTC wake:

```
sync_status   FAILED 2978 | SYNCED 2541 | LOCAL 127
status        DONE 3121 | ERROR 2399 | NEW 125 | TASK 1
```

| day (WIB dates, UTC timestamps) | SYNCED | FAILED |
|---|---|---|
| 08-21 | 44 | 3 |
| 08-22 | 41 | 7 |
| **08-23** | **8** | **40** |
| 08-24 | 6 | 42 |
| 08-25 | 7 | 39 |
| 08-26 | 6 | 42 |
| 08-27 | 6 | 41 |
| 08-28 | 0 | 48 |
| 08-29 | 0 | 48 |
| 08-30 | 0 | 48 |
| 08-31 | 0 | 48 |
| 09-01 | 2 | 37 (+1 LOCAL) |

**The station created 48 video rows a day, every day**, including 08-28 → 08-31
when it was recorded as dead. Nothing about capture changed on 08-23. Sync did.

**This retracts the central conclusion of the video section above** — "the
missing daytime videos were never captured, which distinguishes it from the 2744
historic never-synced videos". It is the *same* failure, and the historic
backlog simply grew: 2744 on 08-27, **2978 FAILED + 127 LOCAL = 3105** now.

`/home/pi/.ORC-OS/uploads/videos` is **29 GB**. At the ~9 MB per clip measured
in tonight's capture log that is ~3,200 files against 3,105 unsynced records, so
the backlog is very likely still on disk rather than orphaned. Confirming file
existence directly is pending a wake window.

**Independent corroboration: the Witty Pi log splits on the same boundary.**
Wake durations, measured from `wp5d.log` (which knows nothing about videos):

| WIB day | median wake, 01–05h | median wake, rest of day |
|---|---|---|
| 08-21 | — | 2.03 min |
| 08-22 | 2.08 | 2.05 |
| **08-23** | **2.07** | **2.56** |
| 08-24 | 2.27 | 2.77 |
| 08-25 | 2.32 | 2.78 |
| 08-27 | 2.32 | 2.73 |

Before 08-23 both are ~2.0 min. From 08-23 the hours that sync stay at baseline
while the rest of the day stretches by ~0.7 min. That is an upload that hangs
and then gives up, and **a hard cutoff cannot produce it** — no connectivity
fails immediately. The link was present and too slow.

**This also refutes the power-path explanation for the video window.** That
argument held the controller's load output could not carry the PoE injector and
camera in daylight. But the camera was powering up and delivering gate-passed
video all day throughout — 48 rows a day, and tonight's cycle logs `Quality gate
PASSED`, 1920x1080, 5.0 s, 8.9 MB, `Delivered`. (Row creation implies a
gate-passed delivery, since `orc-capture` only delivers after the gate; the
per-day file/status breakdown is pending.)

Two further corrections to that argument:

- **Its progression evidence is gone.** It read "large load fails 08-23, small
  load fails 08-28" as one worsening fault. The 08-28 stage was the uplink, not
  power — ISS-FIELD-011 measures 48 boots/day unbroken through 08-31.
- **Supply voltage is higher in daylight, not lower.** V-IN by WIB hour: 12.7 V
  across 01:00–05:00, 12.9–13.1 V from 07:00–17:00. The camera failed when the
  supply was strongest, so sag is not the discriminator.

**Source resistance is now measured, and it is ohms.** TODO-117's paired V/I
shipped; all 691 samples carry both values across 0.567–1.337 A. Four wakes have
enough current spread to fit V = V0 − I·R: **0.468, 0.482, 0.593, 0.686 Ω**,
median 0.537. `wittypi.conf` framed this exact test as ohms (fuse holder,
terminal, crimp) versus milliohms (worn pack). It is ohms. At the Pi's 0.85 A
that is a 0.46 V drop; at ~2.5 A for camera plus injector, 1.34 V. Real, and
worth fixing — but on the evidence above it is not what stopped the video.
Caveat: 4 usable wakes, r² 0.52–0.89.

**THE QUOTA MODEL (Tom, 2026-09-01): a 01:00 reset, not midnight.**

The station wakes at **every** slot including 00:00, 00:30 and 03:00 — verified
against `wp5d.log` — so the gaps below are sync failures, not missed wakes.
Server-received slots, 00:00–06:30 WIB (`#` = arrived):

```
             0000 0030 0100 0130 0200 0230 0300 0330 0400 0430 0500 0530
2026-08-24    .    .    .    #    #    #    .    .    #    #    #    .
2026-08-25    .    .    .    #    #    #    .    #    #    #    .    .
2026-08-26    .    .    .    #    #    #    .    #    #    #    #    .
2026-08-27    .    .    #    #    #    .    #    #    #    .    .    .
2026-08-28    .    .    .    #    #    #    .    #    #    #    .    .
```

| observation | under a 01:00 reset with a small daily allowance |
|---|---|
| nothing succeeds 00:00–00:30, five nights running | previous day's allowance spent |
| first success 01:00–01:45 every night | the reset |
| 6, 6, 7, 6, 6 successes per night | a fixed allowance, ~55–60 MB at ~9 MB each |
| last success drifts 04:01–05:03 | exhaustion — a *moving* end, not a fixed window close |
| nothing from 05:00 to 01:00 | throttled |
| long wakes all day, short ones in-band | throttled uploads hang; unthrottled ones complete |
| sensor CSVs never stop | kilobytes pass a throttle |

The drifting end is what favours this over a fixed bonus window, which would
close at the same clock time nightly. An earlier objection here — that the
successes are not a contiguous prefix, so exhaustion is excluded — **was wrong**:
a transient failed transfer mid-band is compatible, because exhaustion only has
to end the band, not explain every hole in it.

**Two things the model does not cover.**

- **The 03:00 hole recurs on 4 of 5 nights at the same slot.** A random failed
  transfer should not prefer one slot that consistently. Unexplained; n=5.
- **A daily reset cannot explain the 08-23 onset.** A reset that was always
  there produces the same pattern every day, yet 08-21 and 08-22 synced 44 and
  41 videos — six or seven times any nightly allowance. Something separate
  changed that day: the main allowance exhausting, or the plan dropping into a
  throttled tier.

**The check that settles it is on the account, not the station:** the package's
reset hour, and what happened to the data balance on or around 08-23.

**THE SYNC ERROR IS A CONNECT TIMEOUT AT TOKEN REFRESH, NOT A SLOW UPLOAD
(2026-09-01 20:00 UTC).**

From the station journal:

```
ORC-OS - video - ERROR - Error syncing video to remote site:
HTTPSConnectionPool(host='openrivercam.endlessprojects.info', port=443):
Max retries exceeded with url: /api/token/refresh/
(Caused by ConnectTimeoutError(... 'connect timeout=5'))
```

Three things follow. The sync dies at **token refresh**, before any video bytes
move — so file size is not the immediate cause. The connect timeout is **5
seconds**, which is tight for a marginal LTE link. And video sync uses **port
443** while the sensor CSVs that never stopped go to **port 8443**.

This sharpens the quota model rather than contradicting it: on a throttled or
congested link a TCP connect can exceed 5 s, killing the sync at the handshake.
It also accounts for the +0.7 min daytime wakes — "max retries exceeded" means
urllib3 retried, and a few 5 s timeouts is about the 42 s of extra wake measured.
**If that holds, the fix is a timeout constant, not bandwidth.**

**Caveat, and it is the reason this is not yet a conclusion:** these lines are
from 09-01 13:32–14:32 UTC, inside the blackout, when everything failed. They do
not establish that the same error produced the 08-23 → 08-27 pattern. Pulling
sync errors from that date range specifically is the first task in TODO-119.

**Backlog, measured:** 3,101 unsynced rows carry a file path, but only **2,615
`.mp4` files exist** in the 29 GB tree — roughly 486 records have already lost
their files, so at most 2,615 clips are recoverable. (A per-file existence check
in the same grab returned MISSING for every sample and is **wrong**: the `file`
column is relative to `~/.ORC-OS/uploads/` and the test ran from `$HOME`.)

**No configured sync window exists in ORC-OS settings**, so the mundane
explanation is ruled out — tentatively, as the dump carries no column names.

**The station's own data confirms the 01:00 boundary** independently of the
server. Since 08-23, by WIB hour, hour 00 fails 19 of 20 while hours 02 and 04
fail only 9 of 20.

**Next: inventory the backlog and decide what to do with it.** Deferred to a
dedicated session. The question is not only how much is recoverable but whether
`FAILED` is terminal in ORC-OS — only 2 videos have synced since connectivity
returned, against ~4,500 sensor rows that flushed immediately, so nothing
suggests the backlog re-drives itself. If it does not, the disk manager will
eventually consume it, as it already did for the 2,190 records that lost their
files.

**THE 08-23 → 08-27 ERRORS ARE NOT THE CONNECT TIMEOUT (2026-09-01 20:30 UTC).**

The previous entry's caveat was the right one. Pulling `Error syncing video`
from the window itself, classified by cause:

| Cause | 08-23 | 08-24 | 08-25 | 08-26 | 08-27 |
|---|---|---|---|---|---|
| `ReadTimeout` (`read timeout=5`) | 22 | 22 | 24 | 15 | 21 |
| other, non-HTTP | 13 | 15 | 14 | 24 | 15 |
| `RemoteDisconnected` | 4 | 5 | 2 | 3 | 4 |
| `NewConnectionError` | 1 | 5 | 5 | 2 | — |
| `SSLError` (`UNEXPECTED_EOF_WHILE_READING`) | 1 | — | — | — | 1 |

**Not one `ConnectTimeoutError` in five days.** The connection was established
and bytes were moving; the failures land mid-transfer, and they hit `/api/video/`
as well as `/api/token/refresh/`. One is `Expecting value: line 2 column 1
(char 1)` — a JSON decode failure, i.e. the server answered with something that
was not JSON. **The claim that the sync "dies at token refresh, before any video
bytes move" is retracted for this window**; it described the blackout only.

What replaces it is narrower. The read timeout is **5 seconds** and the mean
clip is **9.2 MB**. The three syncs that succeeded on 09-01 took **5.18 s,
5.48 s and 5.44 s** wall clock from "Syncing video N" to "successful". The
transfers sit on the timeout. On that reading "a timeout constant" and
"bandwidth" are not competing explanations but the same one, and the
01:00–05:00 WIB band needs no quota to explain it: those are the hours the link
finishes a 9.2 MB POST inside 5 s. Measured at 04:00 WIB on 09-02, the link
completes a full TLS handshake in 0.52 s and a request in 0.82 s.

**`FAILED` IS NOT TERMINAL, BUT NOTHING AUTOMATIC EVER RETRIES IT.**

Both halves matter, and the first was assumed the other way round.
`orc_api/utils/queue.py:264-266` — inside `sync_videos_start_stop()` — builds
the sync list from `LOCAL`, then `UPDATED`, then `FAILED`, over a start/stop
range, and syncs it with `timeout=150`. A re-drive of the backlog is therefore a
supported operation in ORC-OS 0.6.0, not a database edit.

The boot-time scheduler does not call it. `schedulers.py:35`:

```python
videos_for_syncing = crud.video.get_list(db=session, sync_status=SyncStatus.QUEUE)
logger.info(f"There are {len(videos_for_syncing)} videos left to synchronize.")
```

`QUEUE` is the "was mid-flight when the process died" set. That is a
crash-recovery resubmit, and it is why the station logs **"There are 0 videos
left to synchronize"** on every boot with 3,101 `FAILED` rows in the table. The
log line is accurate about what it asked; it was never asking about the backlog.

**THE BACKLOG IS A THIRD OF WHAT WAS RECORDED.**

| | previous entry | measured 09-01 20:30 UTC |
|---|---|---|
| unsynced rows with a file path | 3,101 | 3,101 |
| files that still exist | ~2,615 | **1,190** |
| bytes to move | "29 GB" | **10.69 GB** |

The 29 GB is the whole `uploads/videos` tree; 1,426 of its 2,616 mp4s belong to
rows that already synced. **1,911 unsynced rows have lost their files** — not
roughly 486. The oldest surviving unsynced file is 2026-07-03 against an oldest
unsynced *row* of 2026-04-08, so everything that failed before July is gone. The
earlier count was reached by subtracting the whole-tree file count from the
unsynced row count, which silently assumed every extant mp4 belonged to an
unsynced row.

**AN EARLIER VIDEO-SYNC BLACKOUT, 2026-07-29 → 08-10, HAS NEVER BEEN RECORDED.**
48 of 48 clips unsynced every day for roughly thirteen days, then clean again
08-11 to 08-22, then the current window from 08-23. **The 08-23 onset is a
recurrence, not a first occurrence**, which weakens any explanation resting on
something that changed once on that date.

The backlog's distribution across the clock is flat — 111 to 147 clips in each
of the 24 WIB hours. That is not evidence against the 01:00–05:00 band: the
backlog is dominated by the two whole-day blackouts, in which every slot failed.
It does mean the backlog itself is not a daytime-only artefact.

**THE NAT64 HYPOTHESIS WAS TESTED AND IS WRONG.** `orc-sensors-upload` forces
`--ipv4` because Telkomsel runs NAT64 and large responses fragment into a black
hole; ORC-OS forces nothing, which would have explained the sensor/video
asymmetry. It does not apply. On the station, `getent ahosts` and Python's
`getaddrinfo` both return only `34.203.227.187`; curl with default selection,
with `--ipv4`, and against :8443 without the flag all take the same IPv4 path
with identical timings. `wwan0` does carry a global IPv6, but the carrier is not
synthesising AAAA for this host. Cost of the test: about 10 KB.

**WHY 443 AND 8443 IS NOT AN APN QUESTION.** Port 8443 is our own
`orc-sensor-upload` container, separate from LiveORC's nginx on 443, same host
and same address. The asymmetry is in the clients: video sync gets a 5 s
timeout, urllib3's default retries and no address-family preference; the CSV
uploader gets `--connect-timeout 10`, `--retry 5 --retry-connrefused
--retry-all-errors` and `--ipv4`. A link marginal enough to kill the first will
still pass the second. On 09-01 the 8443 PUTs failed too (`curl exit 7`), so
8443 gets no special treatment from the carrier.

**HOW LONG THE REMAINING 10.69 GB SURVIVES.** ORC-OS's `disk_management` table
reads `min_free_space = 5.0`, `critical_space = 2.0`, `frequency = 300.0`. Root
is at 12 G free and grows about 440 MB/day, giving roughly **16 days** —
about 2026-09-17 — before deletion resumes. The thresholds are read as GB rather
than percent because the 08-28 purge fired with the disk at exactly 5.00 GiB
free; that is corroboration, not proof, and the units are worth confirming
before the date is relied on.

**Open, and it decides the options:** which of orc_api's several 5-second
timeouts actually fired, and whether the re-drive is reachable as an HTTP
endpoint. See TODO-119 and `station-health/todo119_sync_source_grab.py`.

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

---

### ISS-FIELD-012: The video sync failures are a policed link, not an impatient client

| Field | Value |
|-------|-------|
| **Date opened** | 2026-09-01 |
| **Site** | Sukabumi → LiveORC server |
| **Risk** | Data delivery |
| **Impact** | Medium (pilot; the finding matters more than the bytes) |
| **Status** | OPEN |

**Problem:**
3,104 videos on the station have never reached LiveORC (2,978 FAILED, 126
LOCAL). Successive sessions attributed this to a five-second timeout and
looked for the one call that carried it. Three read-only grabs across the
2026-09-01 21:30 and 22:00 UTC wakes found the timeout, and then found that
the timeout is not the fault.

**Which five fired:**
`callback_url.py:115` in `get_set_refresh_tokens` —
`requests.post(url, data=data, timeout=5)` against `/api/token/refresh/`,
hardcoded and not governed by the caller's timeout. The urllib3 frames above
it end in `do_handshake`, so it stalled inside the TLS handshake before any
HTTP request was sent. No video bytes moved on that attempt.

**Why that is not the whole fault.**
Per failed sync across 08-23→08-28, counted from the one ERROR summary line
each writes:

| Failure | Count |
|---|---|
| `read timeout=5` | 85 |
| `ConnectionReset` | 75 |
| `read timeout=150` | 19 |
| `RemoteDisconnected` | 18 |
| `SSLError` | 4 |
| `ConnectTimeout` | **0** |

201 failures. **97 of them (48%) are resets or disconnects, which no timeout
value fixes**, and **19 had already waited the full 150 s**. The innermost-frame
tally agrees: 139 at `get_set_refresh_tokens` against 78 at
`callback_url.py:172`, the real data POST carrying 150. Zero connect timeouts in
five days — the TCP connection is always established, then torn down or stalled
mid-handshake. That is the signature of a policed or throttled link, not of a
client tuned too impatiently.

**`retry_timeout = 0.0`, and 0.0 is falsy.**
`min(retry_timeout, 150) if retry_timeout else 150` therefore resolves to **150**
in both the live capture path and `routers/video.py:548`. The upload path already
had 150 s. Nothing was clamping it to 5.

**The re-drive exists and is reachable.**
`routers/video.py:530` exposes `POST /api/video/sync/` taking
start/stop/site/sync_file/sync_image, calling `queue.sync_videos_start_stop` at
the same 150 s. It is served on port 80 — `GET /api/video/count/` returns 401 —
so it needs auth but no database edit. `schedulers.py:35` asks only for
`SyncStatus.QUEUE`, which is why every boot reports "0 videos left to
synchronize" beside 2,978 FAILED rows.

**Corrections this makes to earlier entries:**
- Commit `580512a` recorded that "bytes were moving; the failures land
  mid-transfer" and retracted the token-refresh explanation. The retraction was
  wrong for the refresh half: 139 failures do die at token refresh, before any
  request is sent. The mid-transfer reading was right for the other half.
- Earlier in this session I described the 08-24 04:02:58 sample as sitting at
  the edge of the nightly success band. It does not. **The station runs UTC**
  (`timedatectl`, NTP active), so that is 11:02 WIB — an ordinary daytime
  failure, consistent with the recorded 01:00–05:00 WIB window rather than a
  transition case.
- The traceback in grab 119c is grep-fragmented: `grep -A 40` matched both the
  ERROR line and the `ReadTimeoutError` line, so the frames between
  `do_handshake()` and the raised exception are not in hand. The innermost
  captured frame is still `do_handshake`.

**Open, and it decides what to do:**
- The station runs UTC. Station log timestamps need **+7 to reach WIB**. Confirm
  which timestamps each earlier WIB claim was derived from; anything read
  straight off the station without +7 is displaced by seven hours.
- Whether the re-drive survives the link, not merely the code path. It is
  reachable and runs at 150 s, but 19 failures already had 150 s and 97 were
  resets. Only a small-range test measures that, and it spends metered
  Telkomsel bytes on a SIM whose exhaustion caused ISS-FIELD-011.

**Not done:** no re-drive has been fired and nothing on the station has been
changed. All three grabs were read-only.

---

### ISS-FIELD-013: Sukabumi offline since 2026-10-02 05:00 WIB; data quota exhausted, and the station did not reconnect after the 2026-10-06 top-up

| Field | Value |
|-------|-------|
| **Date opened** | 2026-10-07 |
| **Site** | Sukabumi |
| **Risk** | Station availability; un-synced video backlog (TODO-119) |
| **Impact** | Medium (pilot station) |
| **Status** | OPEN — site visit requested 2026-10-07 |

**Observations (all read-only, from the server and the Tailscale control plane):**

- The last row in `sensor_readings` for Sukabumi is **2026-10-02 05:00:41 WIB**.
  All five streams (`wittypi`, `orccapture`, `rg15`, `sht40`, `ds18b20`) stop
  at the same wake. Before that the station was logging normally:
  2,400–2,630 rows per day from 09-28 to 10-01.
- Tailscale reports `orc-sukabumi` last seen at **2026-10-01 22:01:14 UTC**
  (10-02 05:01 WIB), the same wake. No connection since, as of 2026-10-07
  19:14 WIB.
- Power was normal up to the cutoff. Daily V-IN from the Witty Pi, 09-25 to
  10-02: `vin_min_v` 11.66–12.32 V at the daily low, `vin_max_v` up to
  14.16 V on 09-30 and 10-01. There is no downward trend and the panel was
  charging the pack.

**Uplink cause: the data quota was exhausted.** MyTelkomsel screenshots
supplied by Tom on 2026-10-07:

| | Before top-up | Immediately after top-up (2026-10-06) |
|---|---|---|
| Sisa kuota (data remaining) | 0 MB of 0 MB | 55.0 GB of 55.0 GB |
| Aktif hingga (account valid until) | 22 Nov 2026 | 22 Mar 2027 |
| Pulsa (credit) | Rp7.160 | Rp7.160 |

The package is the same one used previously. The cutoff falls about 30 days
after the station's recovery from ISS-FIELD-011 (2026-09-02 01:00 WIB), which
is consistent with a 30-day package expiring. This is the second outage caused
by the SIM account. The balance and quota are still not monitored.

The "after" screenshot was taken immediately after purchase, so it does not
show whether the station has used any of the new quota.

**The station did not reconnect after the top-up.** In ISS-FIELD-011 the
station reconnected by itself within hours of the account being funded. This
time it has not reconnected after more than 24 hours at 48 scheduled wakes per
day. The difference is not yet explained.

**Working hypothesis (Tom, 2026-10-07): the battery is exhausted.** When
uploads fail, the ORC-OS task does not finish and the Pi stays on until the
Witty Pi's 25-minute limit, instead of about 2 minutes. ISS-FIELD-011 measured
this at about 15 hours awake per day. If the Pi also failed to shut down at all,
the load would be continuous.

Against this: during ISS-FIELD-011 the station ran in the same condition for
4.8 days and V-IN never fell below 12.149 V. This outage has lasted 5.6 days as
of 2026-10-07, so exhaustion is plausible if solar input was lower, or if the
Pi stayed on continuously. There is no server data after 10-02 05:00 WIB to
confirm or exclude it.

**Why the 13.0 V recovery voltage has probably not restarted the station.**
The last Witty Pi configuration read (2026-09-01, `data/station-forensics/
orc-sukabumi-wp5-state-20260901T190154Z.txt`) shows:

```
  7. Set low voltage threshold                  <-- no value: UNSET
  8. Set recovery voltage threshold [13.0V]
```

The recovery voltage is the condition for powering the Pi on again *after a
low-voltage shutdown*. With no low-voltage threshold set, the Witty Pi never
performs that shutdown, so the recovery condition is probably never armed. This
was noted as "probably inert" in ISS-FIELD-008 and has not been confirmed
against the Witty Pi 5 firmware documentation. If the battery was exhausted,
the likely sequence is:

1. The Witty Pi does not cut the load at low voltage, because no threshold is set.
2. The pack discharges until its BMS disconnects it.
3. The Witty Pi loses all power. It has no low-voltage shutdown to recover
   from, so the recovery voltage has no effect.

**A second possible cause, independent of the Witty Pi settings:** a LiFePO4
pack whose BMS has disconnected reads about 0 V at its terminals. Many solar
charge controllers do not begin charging when they detect 0 V on the battery
input. If this controller behaves that way, the pack cannot recharge and the
BMS does not reconnect. This is the BMS/charge-controller latch raised in
ISS-FIELD-009. Ten of the thirteen historical outages ended with a button press
on site, which is consistent with it.

**Site visit checklist:**

1. **Before changing anything,** measure and record, with the time:
   - the voltage at the battery terminals;
   - the voltage at the charge controller's battery input;
   - the charge controller's display or status lights;
   - the Witty Pi and Pi status lights.

   About 0 V at the battery means the BMS has disconnected the pack. About
   12–13 V means the battery is connected and the fault is further downstream.
2. Please photograph the charge controller and the Witty Pi before and after.
3. If the BMS has disconnected the pack, reconnect it using the method the
   charge controller or BMS supports (for example, a short connection to a
   charger), then confirm the controller starts charging.
4. Restart the station and confirm it reports to the server. Rows in
   `sensor_readings` and Tailscale both confirm this.
5. Do not change the Witty Pi thresholds on site unless the values have been
   agreed in advance (see "Next steps").

**Data to collect once the station reconnects:**

- The Witty Pi values it uploads for the first wake: `power_on_reason_code`,
  `prev_shutdown_reason_code` and `downtime_s`. These show whether the station
  ran continuously, shut down on schedule, or lost power.
- The buffered sensor rows from 10-02 onwards. In ISS-FIELD-011 the station
  uploaded its whole buffer on reconnection. If rows arrive covering the
  outage, the station was running and the battery hypothesis is wrong.
- The Witty Pi log (`wp5d.log`) and `df -h /`. The disk was forecast to reach
  the 5 GB purge threshold between 10-04 and 10-07 (TODO-119), so un-synced
  video from July may already have been deleted.

**Next steps:**

- [ ] Site visit (requested 2026-10-07).
- [ ] Confirm against the Witty Pi 5 documentation whether the recovery voltage
      requires a low-voltage threshold.
- [ ] Choose a low-voltage threshold and recovery voltage together, with enough
      separation that load sag on the LiFePO4 plateau does not repeatedly cross
      both (ISS-FIELD-008), and set them on the next attended visit.
- [ ] Add the SIM quota expiry date to a calendar, or monitor it. The current
      package was bought 2026-10-06; if it is a 30-day package it expires about
      2026-11-05.

**Not done:** nothing on the station, the server or the account has been
changed. No connection to the station was possible.

**Update 2026-10-09: probable cause of the non-recovery found** (TODO-116).
The Witty Pi's schedule list runs out ~42.6 days after the script was last
activated, and a button press does not rebuild it. If the list was last
rebuilt on 08-21 (the recovery that held, run started ~01:14 UTC), it ran out
at about **10-02 16:45 UTC (23:45 WIB)**, about 19 hours after the quota cutoff.
That would explain why the 10-06 top-up had no effect: by then the station was
no longer waking. Test on the next contact:

- buffered sensor rows should continue past 10-02 05:00 WIB and stop at about
  10-02 23:45 WIB;
- `/log/WittyPi5.log` on the Witty Pi should contain `No future action is
  found in script.`

**Shutdown when uploads fail: wake limit added.** `orc-wake-ceiling.timer`
powers the Pi off 12 minutes after boot unless `/run/orc-maintenance-mode` or
`/run/orc-stay-awake` exists. It does not depend on ORC-OS finishing its task
or on the Witty Pi's schedule. Sukabumi overlay only; not yet deployed.

**Recovery plan (Tom, 2026-10-09):** catch the station on its first boot after
the button press and re-add the schedule by hand, as on 07-03 and 08-21; then
deploy `orc-wp5-rearm` and `orc-wake-ceiling` with `deploy.sh`.

**Update 2026-10-12: root cause confirmed.** The station came back on
2026-10-10 and was read on the 2026-10-12 13:00 UTC wake
(`data/station-forensics/orc-sukabumi-checkin1012-20261012T130044Z.txt`,
script `liveorc_server/station-health/checkin_2026-10-12.sh`, read-only), with
server rows from Grafana. Both predictions from 10-09 held:

| Time (WIB) | Witty Pi log / journal | Server rows |
|---|---|---|
| 10-02 05:00 → 23:30 | Scheduled startups every 30 min, clean `shutdown -h now` after each task | Present, uploaded later from the buffer |
| 10-02 23:30 | Last scheduled startup (16:30:16 UTC); clean shutdown at 16:33 UTC | Last row 23:32 |
| 10-02 23:33 → 10-09 10:32 | **No boot of any kind** (journal boot list and `wp5d.log` agree) | None |
| 10-09 10:32 | `Startup reason: Button Click`; one task, clean shutdown; no next startup | 3 wakes' rows |
| 10-10 10:02 | `Startup reason: Button Click` | Rows |
| 10-10 10:30 onward | `Scheduled Startup` every 30 min | Rows every cycle |

1. **The schedule list ran out at the predicted time.** The last scheduled
   startup was 10-02 16:30 UTC, within one cycle of the predicted 16:45 UTC.
   The station then shut down normally and nothing powered it on again.
2. **The battery hypothesis is not supported.** The station kept cycling for
   18.5 hours after the quota ran out, every wake ended with a normal
   shutdown, and V-IN on the last wakes was 12.4–12.9 V. On 10-09 and 10-10
   it was 12.5–13.1 V. The quota cut stopped uploads only.
3. **The 10-06 top-up had no effect because the station was already off.**
   It was not waking, so it could not reconnect.
4. **The first button press (10-09) gave one cycle, as predicted.** The
   schedule resumed only after the second press on 10-10. `orc-wp5-rearm` and
   `orc-wake-ceiling` are **not deployed** (no unit, no binary, no config), so
   the schedule was re-added by hand during the 10-10 03:02 UTC boot. The
   `wp5d.log` does not record the menu action.
5. Not checked: `No future action is found in script.` in the Witty Pi's
   internal log. That log is not mounted on the Pi, and the evidence above does
   not need it.

**State on 2026-10-12 13:00 UTC:**

- Witty Pi: schedule script in use, next shutdown 13:25, next startup 13:30
  UTC. Low-voltage threshold still unset, recovery 13.0 V.
- **The schedule list will run out again around 2026-11-21 18:25 UTC
  (11-22 01:25 WIB)**, 42.64 days after the 10-10 re-arm, unless
  `orc-wp5-rearm` is deployed first.
- Disk: 90% used, 6.25 GB free. The purge has not started: the oldest
  surviving un-synced clip is still 2026-07-03 09:31. Status counts: SYNCED
  3855, FAILED 3263, LOCAL 126. 1,475 un-synced clips still have their file.
- Link: LTE connected, signal 100%. `throttled=0x0`.

**Next steps (updated):**

- [ ] Deploy `orc-wp5-rearm` and `orc-wake-ceiling` before 2026-11-21.
- [ ] The SIM quota bought 10-06 probably expires about 2026-11-05 if it is a
      30-day package. That is earlier than the schedule deadline.
- [ ] The low-voltage and recovery thresholds are still unset. This no longer
      blocks recovery but remains open (ISS-FIELD-008).

**Update 2026-10-12 (later): `orc-wp5-rearm` and `orc-wake-ceiling` deployed.**
All steps were run from `liveorc_server/station-health/` through the wake
runner; output is in `data/station-forensics/` under the labels given.

1. `deploycheck1012b` (15:00 UTC): the station's checkout
   (`/home/pi/code/git/openrivercam`, clean, `main`) fast-forwarded from
   `f763f61` (2026-05-15) to `a5749ad`. `deploy.sh sukabumi --check
   --skip-packages`: 139 pass, 9 fail. All 9 failures came from 9b2e78f. No
   other drift.
2. `rearmprecheck1012` (16:30 UTC, read-only): `wp5d_poweroff.service` is
   present and enabled, so `systemctl poweroff` from the wake ceiling informs
   the Witty Pi. `wp5` is a compiled binary. The vendor source (uugear/
   Witty-Pi-5-Software `79f4e83`, v5.0.0, `wp5.c` `choose_schedule_script`)
   shows that an empty answer to option 6 chooses nothing.
3. `rearmlist1012` (16:31 UTC): the option-6 list pass, run once. The status
   header was identical before and after; the pass took 0.1 s. Scripts on the
   Witty Pi: `[1] prod_30.wpi`, `[2] maint.wpi`, `[3] prod_15.wpi`.
4. Offline: `orc-wp5-rearm` was run against a fake `wp5` that replays that
   output, in 10 cases (normal run, empty config, wrong version, script missing
   or listed twice, no confirmation, no "done", not in use afterwards, `wp5`
   hanging). Every fault case stopped; none chose a script after a failed list
   pass. The hang case was logged as "not version 5.0.0"; fixed in 32cb6b0.
5. `rearmdeploy1012` (17:30 UTC): pulled 32cb6b0, ran `deploy.sh sukabumi
   --yes --skip-packages` (10 fixed: the 9 above plus the RTC sync, 0 fail),
   then ran the re-arm once by hand. Result: `OK: activated prod_30.wpi
   (item 1)`, in 32.8 s. Activating during a scheduled wake kept that wake's
   shutdown (17:55) and the next startup (18:00).
6. `rearmfirstboot1012` (18:00 UTC): the station woke at 18:00 on the
   re-armed schedule. The re-arm ran by itself and succeeded; next startup
   18:30. `orc-api` started at 38.4 s after boot, when the re-arm finished.
   The wake-ceiling timer was due at 18:12:10, 12 min after boot. Capture
   delivered.

**Cost:** the re-arm holds `orc-api` back about 33 s on every boot. That is
about 33 s more awake per wake, roughly 26 min a day. Capture is not delayed,
because `orc-capture` runs independently of `orc-api`. Re-arming less often
would also prevent the list running out; this is not yet decided.

The 2026-11-21 run-out date above no longer applies while the re-arm runs on
every boot.

**Update 2026-10-12 (evening): re-arm reduced to once a day.** Tom chose a
daily re-arm over every boot.

- `088b30e`: every boot reads the status header (0.1 s) and re-arms only if
  the last success is missing, older than `REARM_INTERVAL_H` (23 h), or in
  the future, or if no startup is armed or no script is in use. Successes are
  stamped in `/var/lib/orc-wp5-rearm/last-ok`. Deployed on the 18:30 UTC wake
  (`rearmdaily1012`).
- **This did not work at first.** On the 19:00 boot it re-armed anyway
  (`rearmdailyboot1012b`). The re-arm runs about 4 s into boot, before
  `wp5d` has copied the RTC into the system clock, which still read
  2026-03-26 17:50. Every stamp therefore looked like it was in the future.
  `After=wp5d.service` waits only for wp5d to start. The unit's comment said
  the clock was already set; it was not.
- `eb7c7b0`: the age is now measured on the Witty Pi's RTC, from the
  header's `RTC Time` line, and the stamp is written from it too. Deployed on
  the 19:30 UTC wake (`rearmrtc1012`).
- **Verified on the 20:00 UTC boot** (`rearmrtcboot1012b`): `OK: not due
  (last re-arm 0h29m ago)`. The re-arm unit finished 4.4 s after boot; next
  startup 20:30; capture delivered.

**Correction to the cost stated above.** On the 20:00 boot `orc-api` started
at 21.8 s, not at about 5 s, so something other than the re-arm also holds it
until about 22 s (probably `orc-maintenance-check`; not confirmed). The
every-boot re-arm therefore added about 15 s per wake (37–38 s against
21.8 s), not 33 s: roughly 12 min a day, not 26.

**Daily re-arm:** the first boot at least 23 h after the last success, now
about 18:30–19:30 UTC. A boot with no armed startup re-arms regardless.

**Update 2026-10-14: check-in, and the disk is at the purge threshold.** Read
on the 13:00 UTC wake with `checkin_2026-10-12.sh` (read-only; output
`data/station-forensics/orc-sukabumi-checkin1014b-20261014T130041Z.txt`).
Server rows are present every day since 10-10, latest 12:30 UTC.

| | 2026-10-12 13:00 UTC | 2026-10-14 13:00 UTC |
|---|---|---|
| Root free | 6.25 GB | **5,109 MiB (4.99 GiB), 92% used** |
| SYNCED / FAILED / LOCAL | 3855 / 3263 / 126 | 3947 / 3267 / 126 |
| Un-synced clips with a file | 1,475 | 1,479 |
| Oldest surviving un-synced clip | 2026-07-03 09:31 | 2026-07-03 09:31 |

- `orc-wp5-rearm` last re-armed 17h59m before this wake (not due until 24 h);
  `orc-wake-ceiling.timer` active. Next startup 13:30 UTC. LTE connected,
  `throttled=0x0`.
- Free space fell about 0.6 GB/day. The purge has not started (oldest clip
  unchanged), but `min_free_space = 5.0` is probably GiB, so the next wake can
  start it. It deletes oldest-first, which is the clean 07-23 → 09-01 upload
  block.
- The re-arm journal lines carry 2026-03-26 timestamps: the known stale
  early-boot clock. The ages it reports are measured on the Witty Pi RTC.

**Decision (Tom, 2026-10-14): try to free space by other means before
deleting any synced video.** `todo119_space_census.sh` (read-only, written,
not yet run) measures `/home/pi/code/git` (3.9 GB on 08-27, 3 uncommitted
changes then), `.ORC-OS/tmp` (1.2 GB), caches, logs, and the non-mp4 output
inside `uploads/videos`. `pi/tools/orc_reclaim_nonvideo.sh` has a dry run and
`--apply`; `--apply` deletes caches, `__pycache__` and tmp files older than
24 h only, and was not run.

**Next:** run the census on a wake
(`python3 todo119_wake_runner.py todo119_space_census.sh census1014 --timeout 330`
from `liveorc_server/station-health/`; wakes at :00 and :30 UTC). Then choose
what to reclaim. Fallback if that is not enough: rebuild the verified list of
clips synced since 09-02 (`todo119_timestamp_join.py`), dry-run it, and delete
only with Tom's approval. Nothing on the station has been changed.

**Update 2026-10-14 (later): non-video space reclaimed; purge threshold cleared.**
Census (`orc-sukabumi-census1014-20261014T133046Z.txt`) then cleanup on the
14:00 UTC wake with `todo119_reclaim_wake.sh`
(`orc-sukabumi-reclaim1014-20261014T140039Z.txt`). Tom approved the cleanup and
the removal of the orcos qemu image. No video and nothing under
`.ORC-OS/uploads` was touched.

| Step | Free after (MiB) |
|---|---|
| Before | 5,106 |
| `.ORC-OS/tmp` (older than 24 h, 1.19 GB), caches, `__pycache__` | 6,833 |
| apt cache and lists | 7,176 |
| Old Claude binaries 2.1.116/117/132 (kept 2.1.133) | 7,869 |
| `rainbow-sensing/image/...orcos-qemu.img.gz` (2.55 GiB, ignored by git, not open) | 10,479 |

- At about 0.6 GB/day the station has roughly 9 days above the 5.0 GiB
  threshold (about 5.4 GiB of margin).
- Non-mp4 output under `uploads/videos` is 8.70 GiB, of which `.jpg` is 8.09
  GiB (7,339 files, mostly `output/plot_quiver.jpg`, up to 4.7 MB each) and
  `.nc` is 0.48 GiB. The earlier census per-extension sizes were wrong (awk
  `sub()` rewrote `$1`); the corrected table is in the reclaim output.
- Not yet explained: `git status` on the station checkout shows 2 lines after
  the cleanup; it showed 0 dirty on the census. Check what they are.
- Open decision: whether the quiver plots of already-synced videos can go.
  ORC-OS may reference them, so this needs Tom's explicit approval.

**Update 2026-11-13: orphaned quiver plots deleted; swap file is not the quick win it looked like.**
Free space had fallen back to 5.10 GiB (5,223 MiB at 14:30) against ORC-OS's 5.0 GiB minimum. The disk manager measures free space in
GiB (`5.0999 GB` logged at 14:30:55 is 5,222 MiB), runs about 5 s after each ORC-OS start (once per wake), and was losing about 11 to 14 MiB
per wake, so the first purge was projected at about 19:00 UTC. Purge order is oldest mtime first, ignoring sync state: the 48 January-dated
offline videos (0.549 GiB, all `FAILED`) first, then early July.
- **Plots.** `sync_image=1` and the sync only uploads a plot if the file exists; `/video/{id}/image/` returns a clean 404 when it is
  missing; the DB `image` column points at `output/plot_quiver.jpg`. The station had 3,387 plots (9.03 GiB): 2,311 with their mp4
  (6.18 GiB) and 1,076 **orphaned** (no mp4 in the video dir; 2.846 GiB, all `SYNCED`, July and August; they exist because the earlier
  reclaims deleted only the mp4s). All 1,076 matched a LiveORC record by timestamp (offset 0 h) whose `image` field is set (09-16 listing;
  the field being set does not prove the image file is readable).
- **Deleted at 17:01 UTC, `todo119_orphan_plot_reclaim_apply.sh` (build 2beb85a):** 1,076 files, 3,055,948,649 bytes, 0 failed; free
  5,162 -> 8,079 MiB (+2,917 MiB). Each file was re-checked on the station first (regular file, listed size, no mp4 in the dir, DB row
  `SYNCED`, older than 24 h, path under the videos dir). A dry run at 17:00 had 1,076 ok, 0 skipped. Manifest on the station:
  `/home/pi/orphan-plot-reclaim-20261113T170121Z.manifest`. Margin is now about 2.9 GiB, roughly 5 days at ~0.56 GiB/day.
- **`/var/swap` (2.0 GiB, fully allocated) must NOT be deleted or renamed.** It is the writeback backing file of the zram swap under
  `rpi-swap` 1.2.1 (`Mechanism=auto` is `zram+file`); `rpi-resize-swap-file` re-creates it with `fallocate` at every boot if it is missing.
  The supported removal is a drop-in with `[Main]` `Mechanism=zram` (then `rpi-remove-swap-file@var-swap.service` runs `rm -f` at the next
  boot, and the zram device is unchanged). Not applied. The generator was read, not run.
- **Other findings.** Processing-peak memory about 2 GiB of 8 GiB with swap unused; zero OOM-killer lines in the journal. mp4 on disk:
  1,807 `SYNCED` (16.24 GiB), 1,552 `FAILED` (13.96 GiB). `FAILED` is not necessarily not-uploaded (known 500-after-commit failures).
- **Not done / open:** the January videos remain first in the purge queue; whether LiveORC holds them (Tom to check); a retention policy for
  synced mp4s; the swap drop-in. The unit-test and broken-copy suites are `test_orphan_reclaim.py` and `run_orphan_reclaim_mutants.py`.

### ISS-FIELD-014: LiveORC server unreachable from the internet; all inbound security group rules were removed by an InfoSec administrator

| Field | Value |
|-------|-------|
| **Date opened** | 2026-10-28 |
| **Site** | LiveORC server (AWS us-east-1, instance `ip-172-31-90-132`, 34.203.227.187) |
| **Risk** | Service availability; station uploads; Grafana |
| **Impact** | High while it lasted (web app, Grafana and the station's sensor uploads all unreachable) |
| **Status** | OPEN — service restored 2026-10-28 15:40 UTC; InfoSec's reason and any standing agreement on the ports are not yet confirmed |

**What happened.** The security group `LiveORC-server` (`sg-0590532d52e77699a`)
lost all its inbound rules, so ports 80, 443, 8443 and 9443 timed out from the
internet. The host itself was healthy throughout. CloudTrail shows the rules
were removed and restored by hand, in the AWS console, by a person using the
SSO role `AWSReservedSSO_AWS-InfoSecTempAdmin` (an InfoSec staff member; the
individual's identity is in the CloudTrail events and is not recorded here).

**Timeline (UTC):**

| Time | Event |
|---|---|
| 2026-10-27 21:24 | Last outside request in the `liveorc_webapp` log (an API client, `POST /api/token/` then `GET /api/site/4/timeseries/`, both 200). |
| 2026-10-27, after 21:24 | Rules first removed. This CloudTrail event has not been retrieved. |
| 2026-10-27 | Tom reported the server unreachable. Probes from the workstation (47.7.209.76) to ports 22, 80, 443 and 9443 timed out. |
| 2026-10-28, before 14:39 | Tom re-added 80, 443 and 9443 (exact time not recorded). Verified reachable from the workstation. |
| 2026-10-28 14:39:39 | InfoSec role `RevokeSecurityGroupIngress` removed those three rules (80, 443, 9443; each TCP from `0.0.0.0/0`). Console session, source IP 104.177.7.231, session started 13:27:32. |
| 2026-10-28 15:08 | Probes from the workstation failed again on 80, 443, 8443 and 9443. |
| 2026-10-28 15:40:37 | Same role `AuthorizeSecurityGroupIngress` added four rules, all TCP from `0.0.0.0/0`: 80, 443, 8443 (description `orc-sensor-up`) and 9443 (description `grafana/sensor`). Console session started 15:32:48, same source IP. |
| 2026-10-28 16:04 | Verified from the workstation: all four ports accept connections; LiveORC 443 returns 302; Grafana `/api/health` returns 200; port 8443 answers 404 at `/`. An actual sensor upload was not tested. |

**Evidence that the cause was upstream of the host (all read-only):**

- Over Session Manager on 2026-10-27: seven containers up 2 months
  (`liveorc_webapp`, `orc-sensor-ingest`, `orc-grafana`, `orc-timescale`,
  `orc-sensor-upload`, `rabbitmq`, `db`); ports 80, 443 and 9443 listening on all
  interfaces; `curl localhost` returned 302 (LiveORC) and 200 (Grafana
  `/api/health`); root disk 27% used; host uptime 63 days; public IP still
  34.203.227.187.
- `tcpdump` on the host, filtered to SYN packets from the workstation, captured
  nothing while the workstation ran connection attempts to 443 and 9443. The
  packets never reached the instance, so the block was in AWS (security group),
  not iptables, Docker or the containers.
- The Tom-run console view showed `LiveORC-server` with no inbound rules. A
  group named `LiveORC-Security-Group` (the name in
  `prior_work/deployment_guides/LIVEORC_DEPLOY_GUIDE.md`) does not exist, and
  the `launch-wizard-*` groups in the account are not attached to this instance.

**Ports the service needs.** 80 (HTTP redirect; Let's Encrypt validation), 443
(LiveORC), 8443 (`orc-sensor-upload`, where the station PUTs sensor CSVs;
`pi/shared/etc/orc/sensors-upload.conf`), 9443 (Grafana). The deploy guide lists
only 80 and 443. While working on this the first re-add omitted 8443 and the
station-side check of the upload path was wrongly reported as passing; the
station's own config is the authority for the port list, not the guide.

**PHP2Shell (CVE-2026-109618 and CVE-2026-109619, reported patched 2026-10-21).**
Raised as a possible reason for the removal. On 2026-10-27 no PHP was found on
the host or in any of the seven running containers: `command -v php php-fpm
php8` returned nothing, the `dpkg`/`apk` PHP package count was 0 in every
container and on the host, and `pgrep php` returned nothing. An external probe
found no `X-Powered-By: PHP` header and 404 for `phpinfo.php`, `index.php`,
`info.php` and `wp-login.php`. The check does not cover PHP built outside the
package manager and `PATH`. InfoSec has not said that PHP2Shell was the reason.

**Not caused by this:** the Sukabumi station stopped sending on 2026-10-21, six
days before the removal. Its last server rows are 14:30:21–14:30:36 UTC
(21:30 WIB). `boot_age_s` 21.3 at 14:30:36 puts the wake at about 14:30:15; the
second Witty Pi reading and two of the three `orccapture` rows normally written
in the following two minutes are missing, so the cycle is incomplete. V-IN was
12.64 V on the last reading with no downward trend (daily minimum 12.46–12.64 V,
10-12 to 10-21). Tailscale shows `orc-sukabumi` offline, last seen 6 days before
2026-10-28. Tom reported on 2026-10-28 that the SIM still has a large balance.
Per ISS-FIELD-013 the earlier outage was the data quota, not the balance, and the
quota has not been checked for this stop. The cause of the 10-21 stop is open.

**Open items:**

1. Retrieve the 2026-10-27 `RevokeSecurityGroupIngress` event (CloudTrail Event
   history, us-east-1, resource name `sg-0590532d52e77699a`) to confirm the
   first removal was the same role.
2. Get InfoSec's stated reason and whether they accept the current rules: all
   four ports open to `0.0.0.0/0`. The station is on a cellular network in
   Indonesia, so its uploads cannot be restricted to a fixed source address.
   Port 9443 serves Grafana with anonymous Viewer access (see the LiveORC
   read-only query notes); that is worth raising with them.
3. Confirm a sensor upload reaches 8443 once the station next syncs.
4. Nothing monitors whether the server is reachable from outside. The
   station's SIM and this server's network path have each caused an outage that
   was found only when a person looked.

### ISS-FIELD-015: Sukabumi silent since 2026-10-21 14:30 UTC; station did not restart on its own; cause open

| Field | Value |
|-------|-------|
| **Date opened** | 2026-11-04 |
| **Site** | Sukabumi |
| **Risk** | Station availability; recurrence of the Witty Pi schedule failure after the ISS-FIELD-013 fix |
| **Impact** | Medium (pilot station) |
| **Status** | OPEN — mitigated, root cause open. Station cycling since the 2026-11-11 button press. Clock floor (installed 2026-11-13 18:00 UTC) and early-boot logger guard (installed 20:00 UTC) are live and verified on the real station. The 10-21 stop and the 304-day RTC month error are unexplained; firmware v1.1 is the leading candidate (ISS-FIELD-017); offline-wake timestamps are a known limit (ISS-FIELD-018) |

**Observations (read-only; server SQL via Grafana, local `tailscale status`, repo files):**

- Last server row: 2026-10-21 14:30:36 UTC (21:30 WIB). No rows in the 14
  days since (checked 2026-11-04 07:55 UTC). That wake contains one of the three
  data batches a wake normally delivers (boot_age_s 21.3). A normal wake
  delivers batches at about +20 s, +70 s and +120 s.
- Tailscale `LastSeen` for `orc-sukabumi`: 2026-10-21 14:33:18 UTC, 198 s after
  the 14:30 slot. In the 10-01 quota outage `LastSeen` came 33 s after the last
  row; here it came 162 s after, so a link or quota cut at 14:30:36 does not fit.
  A normal wake ends about 135–165 s after the slot, so 14:33:18 is consistent with
  a normal end. I have no measured baseline for `LastSeen` after a normal wake.
- V-IN at 14:30 UTC was 12.58 V. The same reading on the 8 previous days was
  12.58–12.63 V. The nightly lows (11.5–12.3 V) show no trend. Tom judges the
  battery and charge controller unlikely to be at fault, and the data show nothing
  against that.
- The 42.6-day schedule run-out does not apply. The newest activation was at most
  8 days old on 10-21 (daily re-arm, deployed 2026-10-12).
- Since 2026-09-02 the only other wake with a single Witty Pi reading is
  2026-10-12 17:30, the re-arm deploy itself.
- The server cannot show which wakes ran the re-arm. The first-reading boot_age is
  20–30 s and the fresh-capture row falls 130 s after the slot on 345 of 346 wakes
  since 10-12.
- The last server row is when the station stopped reporting, not when it stopped
  waking. In ISS-FIELD-013 the station cycled for 18 hours after its last row.

**Withdrawn interpretation.** An earlier reading in this investigation treated the
missing second and third batches as a truncated wake (power loss or crash about
40–60 s after boot). The evidence does not support it. The last wake may have been
complete, with the Pi powering off normally and no next startup armed, which is
the same shape as 10-02. Late batches going unshipped is also a known failure
(ISS-FIELD-010).

**Hypotheses, Witty Pi first. None is confirmed.**

1. **The schedule write left the next startup empty (Tom's hypothesis, 2026-11-04).**
   Two variants were proposed: a race in setting the schedule, and a Witty Pi
   NVRAM write (5–10 s through `wp5`) that had not completed before shutdown.
2. **The Witty Pi lost its alarm state.** The original TODO-116 latch: the next
   startup is left in the past and nothing fires it, triggered by something
   other than run-out.
3. **The Pi is on but offline.** The server cannot exclude it, and the data quota
   has not been checked for this stop (ISS-FIELD-014 records only that the SIM
   still has a large balance). The Tailscale timing argues against a quota cut at
   14:30:36.

**Attempts to disprove hypothesis 1 (what held and what did not):**

| Test | Result |
|---|---|
| Re-arm racing `orc-sensors` or ORC-OS shutdown | Closed. In the 10-12 boot captures `orc-api` and `orc-sensors.timer` start when the re-arm ends (37.2–38.4 s on activation boots, against about 22 s on others). The ordering `Before=orc-api.service` and `Before=orc-sensors.timer` holds. |
| NVRAM write cut short by poweroff | Not supported. The only schedule write is the activation. `wp5d.log` records nothing about arming at poweroff (5,250 plain `Caught signal 2 / Exit now`). The activation ends 33–38 s after boot, including the `sleep 10` and verify; poweroff follows at about +120–165 s, a margin of 85 s or more. Observed: both alarms populated at +10 s on all 5 distinct activations in the 10-12 captures (17:31, 18:00, 18:30, 18:31, 19:00). The daily activations after 10-13 were not captured. The microcontroller runs from VIN, not the Pi's 5 V, so Pi power-down does not stop a write it is doing itself; only killing the `wp5` command mid-transfer could. That last point is from reasoning, not from the firmware source. |
| Failure rate | Cannot exclude a rate of a few percent. About 5 activations were observed and about 8 more occurred unobserved. |
| Shutdown-time arming, over the full `wp5d.log` (2026-04-07 to 09-01) | 5,645 scheduled startups. Zero "Power Newly Connected" events after April. Since May the clean-poweroff-then-silence onsets are 05-11 (activation date unknown, so unexplained), 08-14 (run-out predicted 18:08, last wake 18:30) and 08-20→21. The 06-24 outage differs: the Pi stayed on for 7.26 days with no shutdown. The run-out matches are arithmetic from ISS-FIELD-013, not independent evidence. |
| Re-arm slot arithmetic | Predicts the 10-21 re-arm at 15:00 UTC (anchor: stamp 10-13 19:01, 30 minutes earlier each day), one slot after the stop. It assumes every re-arm succeeded. Any out-of-slot re-arm re-anchors it, and pass 0 treats an unreadable header as due. Weak evidence either way. |
| Exposure | Activations ran about 4 times in 5 months before 2026-10-12 and about daily since. A rare flaw in that path now has about 100 times the exposure. |

**Code paths that could leave the startup empty (`pi/sukabumi/usr/local/bin/orc-wp5-rearm`):**

1. Pass 3 requires only `Choose schedule script (in use)`. It does not require an
   armed startup, yet it writes `last-ok` and logs `OK`. If the firmware has not
   finished regenerating its 4,096-entry list at +10 s, the wake ends with
   nothing armed. Confirmed by reading the script. Not reproduced.
2. `wp5` killed between the firmware's delete and regenerate steps. Pass 2 runs
   under `timeout 90` and the unit has `TimeoutStartSec=150`. The firmware
   sequence has not been read.
3. Not a re-arm path: `orc-sensors` runs `wp5` status reads (up to 6 per tick,
   every 60 s) until the Pi powers off. Nothing locks them against
   `wp5d_poweroff`. Unverified.

**Plan for the button press** (no station DB writes). Tom, 2026-11-04: a watcher
will be armed so he does not need to be present for the press. The standing rule
from 2026-09-01 (nothing polls or touches the station without a live Claude
session) still applies: the watcher must be session-scoped, so a Claude session
stays running until the press. Not yet armed; no press time is set.


1. Before the press, check MyTelkomsel data remaining. The unit is enclosed, so
   LEDs cannot be photographed.
2. On the first boot, collect, read-only, with `liveorc_server/station-health/iss015_button_grab.sh`
   (run through `todo119_wake_runner.py`). **No `/run/orc-stay-awake` touch (Tom,
   2026-11-10):** the 12-minute ceiling runs once and skips for good if the file
   exists, a normal wake ends 2-3 minutes after boot when ORC-OS powers the Pi
   off (the file does not stop that), and a file left behind with nothing armed
   could keep the Pi on indefinitely. The grab must fit inside that 2-3 minute
   wake. It ends with a VERDICT (ARMED, NOT_ARMED, SUSPECT or UNKNOWN) read from
   the header. It collects:
   - `journalctl -t orc-wp5-rearm` across boots. The re-arm overwrites
     `/var/log/orc/wp5-rearm.last` and `/var/lib/orc-wp5-rearm/last-ok` on this
     boot, so the journal (persistent, about 109 boots) is the source. Its
     "re-arm due" line records the header **before** the re-arm changes anything.
     Early-boot journal times are stale (they read 2026-03-26).
   - `journalctl --list-boots`: the end time of the 2026-10-21 14:30 boot. About
     14:32:20–30 means a complete wake; about 14:31 means a truncated one.
   - The tail of `wp5d.log` around 10-21 14:30. Its format at shutdown has not
     been seen for this event.
   - `schedule.skd` and `schedule.act` mtime and size.
   - The wp5 header only (`14`). No menu choices.
3. Reading the result: a blank "Schedule next startup" means the startup was
   emptied (hypothesis 1); a past-dated startup means the alarm was missed
   (hypothesis 2); a Pi already on at site means hypothesis 3. Compare any armed
   time with the predicted 15:00 slot.
4. Before ending the session, confirm the header shows a next startup, then watch
   two on-grid wakes (:00 and :30) arrive. Use
   `liveorc_server/station-health/iss015_two_wakes.py`, started only after the grab
   reports DONE (armed during the boot it could count the press wake). It is passive
   (`tailscale status` only, no ssh) and must run session-scoped. Wakes may be hours
   apart: the solar schedule skips the night.

**Candidate fix, not built.** Nothing confirms that a startup is armed before the
Pi powers off, and that gap is common to the run-out, the NVRAM variant and the
verify-step path. Two changes would close it: make pass 3 fail unless "Schedule
next startup" shows a time, with one retry; and add a unit that runs before
poweroff, reads the header, and re-activates and waits if the startup is blank.
Both change the 10-12 fix, so they need Tom's approval.

**Next step (Tom, 2026-11-04):** execute each relevant code path to see which one
can leave the startup empty. Candidates: the three paths above, plus a forced
`die` after pass 2, a `timeout` kill of pass 2, and a `wp5` status read
overlapping an activation. Use a bench Witty Pi if one is available; running them
on the station is a station change and needs Tom's explicit approval.

**Code-path execution, 2026-11-04.** `orc-wp5-rearm` and `orc-wake-ceiling` were
run on a workstation as copies, with `wp5`, `logger`, `systemctl` and `sleep`
replaced by stubs (`pi/tests/rearm_harness/`; findings in
`pi/WP5_REARM_FAILURE_MODES.md`). No Witty Pi and no station were used. The stub
`wp5` was written from what the script searches for, not from a captured
transcript, so these runs show what the script does with a given menu output.
They do not show what the firmware outputs. 44 scenarios were run.

| Path | Result |
|---|---|
| Path 1: after the choice, the header shows "in use" but no armed startup (`paths.sh`, P1) | **Reproduced.** The script logs `OK: activated`, writes `last-ok` and exits 0 with "Schedule next startup" blank. This confirms that pass 3 does not check the startup. It does not show that the firmware ever returns that header at +10 s. The 10-12 captures showed both alarms populated at +10 s on all 5 activations. |
| `timeout` kill of pass 2 after the choice was sent (P2) | Script aborts with `wp5 choose pass failed or timed out`, exit 1, no `last-ok`, so the next boot re-arms. Whether the firmware is left with an empty list after being killed between its delete and regenerate steps cannot be tested with a stub. The firmware sequence is still unread. |
| Forced abort after pass 2 (no RTC time in the verify header, or script not marked in use) | Activation has happened, no `last-ok` is written, exit 1. The stub leaves the startup armed, so this path alone does not empty it. The next boot re-arms. |
| `wp5` status read overlapping an activation | Not tested. The stub has no shared state. |
| `wp5` output cut at the RTC, startup, "in use" or list lines; empty output; crash with a complete header | The script never chose a wrong schedule script. It aborts or treats the re-arm as due. A crash (exit 139) with a complete header is accepted. |

Other defects found in the same runs. None of them empties the startup by itself;
they bear on whether re-arming happens at all, or happens more often than needed:

1. A failed write of `last-ok` is logged as `OK` (exit 0), the old stamp stays and
   every later boot re-arms. That adds exposure to the path-1 gap.
2. A broken `/etc/orc-wp5-rearm.conf` (unterminated quote, value with a space)
   disables re-arming with exit 0, and the log says only "SCHEDULE_SCRIPT empty".
   A disabled re-arm would bring back the 42.6-day run-out. The station's conf has
   not been checked.
3. `REARM_INTERVAL_H` that is empty or negative re-arms on every boot. A
   non-numeric value ends the script with no log line.
4. No RTC time in the verify header leaves no `last-ok`, so each boot re-arms.

A patch for items 1 to 3 and the regex handling is saved as
`pi/tests/rearm_harness/proposed_fix.patch`. It is **not applied** and does
**not** add the startup check from the candidate fix above. The deployed script is
unchanged.

**Open items:**

1. Who presses the button, and when.
2. The read-only grab script is not yet written.
3. The data quota for this stop has not been checked.
4. ISS-FIELD-014 states the 10-21 stop is open; this entry now carries it.

#### Update 2026-11-11: button press, grab results, clock findings

Everything here was read from the station or the server. Items marked *inferred*
were not observed.

**Press and grab.** The press was at 07:51:26 UTC (wp5d.log: "Startup reason:
Button Click"). `iss015_button_grab.sh` ran at 07:51:55–07:52:12 through
`todo119_wake_runner.py`. It made no station changes. The `/run/orc-stay-awake`
touch was dropped on 2026-11-10 (Tom): `orc-wake-ceiling` runs once, 12 minutes
after boot, and does nothing if the file exists at that moment, and ORC-OS powers
the Pi off 2–3 minutes after boot whether or not the file exists.
Capture: `data/station-forensics/orc-sukabumi-iss015-button-20261111T075155Z.txt`.

| Finding | Evidence |
|---|---|
| The 10-21 14:30 wake was complete and a startup was armed | The re-arm line written at the start of that boot reads `OK: not due (last re-arm 22h59m ago); Schedule next shutdown [21 14:55:00]; Schedule next startup [21 15:00:00]`. The boot ran 14:30:15–14:32:22. No activation ran in that wake, so the schedule-write race and NVRAM-write variants of hypothesis 1 do not apply to it. |
| The Witty Pi RTC date is wrong | Header: `RTC Time: 2026-01-11 07:52:11`, `SYS Time: 2026-11-11 07:52:12`. Same day of month and time of day; the month reads 01 instead of 11 (304 days). wp5d.log shows the RTC correct on 10-21 (14:30:15). |
| Pre-change header at the button boot | Next shutdown `[20 15:55:00]`, next startup `[20 16:00:00]`, "last re-arm -24392363s ago". `[20 16:00]` is the first entry of the old list, which is what the header shows if the RTC date is earlier than the list. |
| The re-arm activated on the wrong calendar | `OK: activated prod_30.wpi (item 1)`; next startup `[11 08:00:00]`. Verdict: ARMED. |
| Other | V-IN 12.97 V at 1.2 A (recovery threshold 13.0 V). Disk 89% used. `wp5d.log` contains NUL bytes: `grep` reports "binary file matches"; use `grep -a`. `schedule.skd` was not found under `/home/pi`, `/opt` or `/usr/local`. |

**The station cycles.** `iss015_two_wakes.py` (passive, `tailscale status` only)
saw wakes at 08:00:43 and 08:30:40 UTC, 43 s and 40 s after their slots, and ten
wakes in total through 11:30 at +40 to +46 s. The server shows rows for each wake
in the normal 13/21/16 pattern, all dated 2026-11-11. Two entries the watcher
first flagged off-grid (08:03:08 and 10:03:36) were the node dropping off
Tailscale for about 15 s and returning inside the same wake. For 10:00 the boot
list shows one boot, 10:00:15–10:03:43 (3 min 28 s against about 2 min usual). For
08:03 the boot list did not reach back far enough. The watcher counted these as
wakes; it now treats a return within 300 s as the same wake. Replaying the
recorded events through the fixed watcher gives CYCLE OK at 08:30. The 10:00 wake
is missing its first server batch and has an extra batch at 10:03; unexplained.

**Clock findings** (`iss015_clock_grab.sh`, 12:00 UTC wake; capture
`orc-sukabumi-iss015-clock-20261111T120044Z.txt`):

1. Early boot reads the image time, 2026-03-26 17:50.
2. About 6 s in, wp5d copies the Witty Pi RTC into the system clock (Jan 11);
   chrony logs "Backward time jump".
3. About 25 s in, chrony reaches an Indonesian ISP NTP server over the cellular
   link and steps the clock by +26,265,600.76 s (exactly 304 days). Config:
   `pool 2.debian.pool.ntp.org iburst`, `makestep 1 3`, `rtcsync`.
4. `rtcsync` updates only the Pi's own RTC (`rpi-rtc`, which reads correctly).
   Nothing writes the Witty Pi RTC. It still read 2026-01-11 after the step, and
   wp5d.log shows the same Jan 11 copy at every wake since the press.

*Inferred, not tested:* with no NTP source the system clock would stay on the
RTC's Jan 11 date. The sensors take timestamps from `datetime.now()` at read time
with no check, and name the daily CSV from the same clock. In the 12:00 wake the
first row was written 4 s after the step. `orc-sensors-upload` sends only files
whose mtime is newer than a watermark file, so a file written under the January
clock would carry an older mtime and would not be uploaded. The server keeps
`(ts, station, sensor, metric)` unique with `ON CONFLICT DO NOTHING`, so repeated
timestamps are dropped silently. The server holds 126,308 Sukabumi rows, earliest
2026-04-16, none mis-dated; no January-clock row has been stored.

**Not known:** when or why the RTC date changed; whether it caused the missed
15:00 startup on 10-21.

**Change built, not deployed.** `pi/sukabumi/usr/local/bin/orc-clock-floor` and
`orc-clock-floor.service` save the current time as a floor at shutdown and, at
boot after wp5d's clock step, set the clock forward to the floor (or to the upload
watermark's mtime, if later). The floor is lowered only when chrony is synced to a
real upstream (the `local stratum 10` reference is excluded) and otherwise may
only advance, by at most 2 days. The script never writes the Witty Pi RTC, never
touches the schedule, and never fails the boot. `sensors_logger.py` can write
`clock_state` and `clock_adj_s` columns; they are inert until a sensor's
`CSV_HEADER` lists them. Tests: `pi/tests/clock_floor/test_clock_floor.py`, 38
checks, run against a fake clock and the real `orc-sensors-upload`; each guard was
also checked by running the tests against 12 deliberately broken copies of the
script. Not verified on hardware: `date -u -s @epoch`, and that `After=wp5d.service`
waits for the clock step (the script waits for it itself).

**Options still open.** (A) the floor above, which is built. (B) Write the system
time to the Witty Pi RTC after chrony syncs, then re-arm in the same wake. This
must not be done alone: the active list covers Jan 11 to about Feb 23 on the RTC
calendar, so correcting the RTC leaves no future startup. (C) Leave it and watch.

**Open items:**

1. Deploy the floor (see the deploy checks below once the station checkout is read).
2. Decide on B, and whether a bench Witty Pi is available to test menu item 1.
3. Find why the RTC date changed.
4. The 10:00 server batch anomaly.
5. The data quota for the 10-21 stop was not checked; the station is now on the
   cellular link normally, so this is no longer blocking.

#### Update 2026-11-12: gap and short wake on 11-11, press not visible, state at session end

Measured unless marked *inferred*. Times UTC.

- **11-11 12:00 wake** was complete for sensors (rows at 12:00, 12:01, 12:02). Its 12:01 and
  12:02 batches reached the server late, in a whole-file re-send of the daily CSV. A "latest row"
  query shortly after a wake therefore under-reports; check again later before concluding a wake
  was cut short.
- **12:30–16:30:** ten scheduled slots produced no wake. `prod_30.wpi` has no gap
  (`ON M25 / OFF M5`, 2026-01-01 to 2099, 48 a day). The daily CSV re-sent at the 17:00 wake held no
  rows for those slots, so the sensors did not run in them.
- **17:00:44:** one wake, on grid (+44 s). Tailscale showed it online for about 40 s; only the first
  batch (13 rows, 17:00:13) reached the server. No wake at 17:30, 18:00, 18:30 or 19:00.
- **Nothing visible since.** At 11:35 on 11-12: Tailscale offline (`LastSeen` 17:01:22 on 11-11),
  latest server row 17:00:38 on 11-11, and the recovery runner never saw tcp/22 open.
- **The team pressed the button** and shared a video showing the unit went through a cycle. The
  press time is not recorded here. A boot that none of Tailscale, the server or the runner saw
  means the Pi had no usable network path during it (*inferred*). Candidates, none established:
  the cellular data balance (not yet checked; Tom asked the team to check it), the modem, or the
  tailnet. This would also fit the partial deliveries at 12:00 and 17:00 (*inferred*).
- **Not known:** why wakes were skipped 12:30–16:30; why the 17:00 wake was short; whether the
  schedule is cycling now, unseen. A wake with no network leaves rows in the daily CSV, which are
  delivered whole once a PUT succeeds.

**Tools written and committed (nothing deployed):** `iss015_clock_grab.sh` (`65051b2`),
`iss015_postmortem_grab.sh` (`acac211`), `iss015_press_boot.sh` (`e93e6b6`, not pushed).
`iss015_press_boot.sh` runs through `todo119_wake_runner.py` at the first visible boot and makes four
root writes, approved by Tom on 2026-11-11: `sudo -n true`; `systemctl stop orc-sensors.timer
orc-sensors.service`; `rm -f /var/lib/orc-wp5-rearm/last-ok`; `systemctl start orc-wp5-rearm`. It
forces one fresh schedule activation, because the boot-time re-arm would say "not due" at a press
boot (stamp 16–21 h old, header shows an armed startup) and an armed header was not enough on 11-11
(12:00:50 showed `[11 12:30:00]`, no wake followed). It then reads evidence from files and the journal
only. Dry-run against stubs in nine scenarios; never run on the station. Uncommitted:
`iss015_postmortem_grab.sh` now finds boots by end time instead of `-1`.

**Evidence ages out.** The station journal held about 109 boots on 11-04. At 48 wakes a day the
11-11 12:00 and 17:00 boots may be rotated out within about two days of normal cycling. Read them
at the first reachable wake.

**Stopped at session end (Tom leaving the session):** the passive watcher and the recovery runner
were stopped on purpose so nothing polls or connects to the station without a live session. To
resume: re-arm both from `liveorc_server/station-health` with
`python3 -I iss015_two_wakes.py --poll 5 --wait-s 172800` and
`python3 todo119_wake_runner.py iss015_press_boot.sh iss015-pressboot --timeout 300 --wait 172800`,
as session-scoped tracked tasks (not `&`, `nohup` or `disown`). Reconfirm the four writes with Tom first,
and consider skipping the forced re-arm if the boot list shows the Pi already cycling on the grid.

**Open items:**
1. MyTelkomsel data balance (team checking, 2026-11-12).
2. The team's video: press time, how long the unit stayed on, status LED colours if visible.
3. Push `e93e6b6`; commit the postmortem boot-lookup fix.
4. Decide on the clock floor deploy (built and tested, not deployed; the station checkout state
   is in the press-boot script's section 9 output once it runs).
5. Option B (write the RTC, then re-arm in one wake) and the unexplained RTC date remain open.

#### Correction 2026-11-12 12:35: the station kept cycling; the "gaps" were network outages

Source: `data/station-forensics/orc-sukabumi-iss015-pressboot-20261112T123043Z.txt` (press-boot runner,
12:30:43 UTC wake). This supersedes the readings above that treat 11-11 12:30–16:30 as missed wakes and a
possible Witty Pi schedule fault.

- **The Witty Pi kept firing.** `wp5d.log` on the station records Scheduled Startups at 10:00, 10:30,
  11:00, 11:30, 12:00 and 12:30 on 11-12 (RTC date Jan 12), each ending in a normal shutdown after
  about 3 min. The re-arm journal shows the schedule advancing on the grid (next startup `[12 11:00]`,
  `[12 11:30]`, `[12 12:00]`, `[12 12:30]`, `[12 13:00]`) and a daily re-arm about 5 h before 12:30.
- **The Pi had no network in those wakes.** chrony in the 12:00 wake of 11-12 logs `Can't synchronise:
  no selectable sources`. With no NTP step the system clock stayed on the Witty Pi RTC date (Jan 12).
  Tailscale, uploads and the recovery runner could not see those wakes.
- **Rows were written but stranded.** `sht40_2026-01-11.csv` (600 B, last write Jan 11 23:30) and
  `sht40_2026-01-12.csv` (1215 B, last write Jan 12 12:30) hold sensor rows stamped with the RTC's month
  (01) and the real day and time. `orc-sensors-upload` sends only files newer than its watermark, so files
  with January mtimes are not uploaded. The section 7 listing was cut to 20 lines, so Jan files for the
  other sensors were not shown; their existence is unconfirmed. The sizes fit roughly one sht40 row per wake.
- **Network returned at the 12:30 wake** (tcp/22 open 12:30:43, +43 s). Cause not established; the team was
  asked to check the data balance.
- **What this means for the earlier items.** The 11-11 12:30–16:30 "gap", the short 17:00 wake and the
  absent 17:30–11-12 12:00 wakes were wakes without a working network, not a schedule fault. The RTC
  month error (01 for 11) is real and persists, but it did not stop the schedule from firing on the grid.
  The 10-21 stop is different: `wp5d.log` has no startups between 10-21 14:32 and the 11-11 press.
- **The recovery runner forced a fresh activation that was not needed.** It ran as approved:
  `OK: activated prod_30.wpi`, next startup `[12 13:00:00]`. Its "already cycling" guard counted 0 recent
  boots because the journal's end times are on the Jan/Jul clock, so it fell through to the forced path.
  The guard must not rely on the wall clock. Proof the activation did no harm is the 13:00 wake.
- **Videos (*inferred*).** Wakes with no NTP stamp January dates. LiveORC may show videos from these wakes
  under Jan 11–12. Not checked.
- **Station checkout** is at `eb7c7b0` (2026-10-12), branch `main`, upstream `origin/main`, with two tracked
  `__pycache__/*.pyc` files deleted locally. A pull would fast-forward 7 commits (all by Tom, 29 files:
  tooling, tests, docs, the clock-floor files, and changes to `pi/deploy.sh` and
  `pi/shared/.../sensors_logger.py`). Nothing incoming touches the installed re-arm, ceiling or uploader, or
  the two deleted files. Installed copies of the re-arm, ceiling, uploader and logger equal the checkout.
  A pull alone installs nothing; `deploy.sh` does. A full `deploy.sh` run has not been reviewed.

**Revised open items:** (1) confirm the 13:00 wake; (2) clock floor deploy now has a concrete case: it would
have kept rows out of January files (it does not fix the network); (3) recovering the stranded rows
(+304 days to each timestamp; the server drops duplicates) is a station-side file write and needs approval;
(4) why the network was down 11-11 12:00 to 11-12 12:30; (5) review a full `deploy.sh` run before deploying.

#### Update 2026-11-12 14:30: collection grab results; offline sensor data was deleted by log rotation

Source: `data/station-forensics/orc-sukabumi-iss015-collect-20261112T140049Z.txt` (read-only; 14:00:49
wake; 14 s). Supersedes earlier items where noted.

- **No scheduled startup was missed from the 11-11 press to 11-12 14:00.** `wp5d.log`: 32 Scheduled
  Startups on 11-11 (08:00 to 23:30) and 29 on 11-12 (00:00 to 14:00), no gap over 35 minutes, plus a
  press at 11-12 03:41:50. Earlier presses are logged on 07-03, 08-20/21 and 10-09/10.
- **The 21-day silence left no daemon trace.** No `wp5d.log` line exists between 10-21 14:32 and the
  11-11 press. Non-routine events in the log are I2C read-back retries at shutdown on 06-19, 08-25 and
  09-27 and register changes; none after 09-27. The cause of the 10-21 stop remains unknown.
- **Sensor data from the offline wakes was deleted by our log rotation.** `rotate_logs` removes
  `<label>_*.csv` whose name date is older than 30 days relative to the clock. Offline wakes wrote
  January-dated files (clock on the RTC). After NTP corrected the clock, the next tick removed them.
  `sht40_2026-01-11.csv` (600 B) and `sht40_2026-01-12.csv` (1215 B) existed at the 12:30 capture and
  were gone at 14:00. They had never been uploaded (the uploader skips files older than its
  watermark). No other copy is known. The affected span is about 11-11 12:30 to 11-12 13:00.
- **The first sensor tick races the clock step.** chrony steps +304 days 19–24 s after boot; the 14:00
  wake still wrote a January-dated row in four sensor files. The server lacks the 13:00 first batch.
- **Videos.** `/home/pi/.ORC-OS/uploads/videos` holds 68,647 files, 42.2 GB; the oldest is dated
  2026-01-11 12:32 (directory `20260111`). Disk is 90% used. Whether the January-dated videos are
  exposed to a date-based purge was not checked.
- **Journal.** The 11-11 07:51, 12:00 and 17:00 boots are not in the journal (1053 boots, at the 200 MB
  limit, mostly July to mid-October). `--list-boots` labels are unreliable for these boots.
- **Network.** chrony: no NTP source at the 11-12 12:00 wake; stepped at 12:30, 13:00, 13:30, 14:00.
  The modem-level failure mode was not isolated.
- **Deploy diff.** 46 installed overlay files hashed; all equal the station checkout (`eb7c7b0`). A
  deploy from `HEAD` would change one existing file (`sensors_logger.py`) and add `orc-clock-floor`
  and its unit. The rest of `deploy.sh` has not been reviewed.

**Revised open items:** (1) fix log rotation (do not delete implausibly dated files; prefer deleting
only uploaded files) and deploy it with the clock floor; (2) check LiveORC and the ORC-OS purge for
the January-dated videos; (3) add RTC date and next startup to the Witty Pi sensor CSV; (4) track the
data balance expiry and run the staleness alert; (5) the 10-21 stop and the RTC month stay open.
The earlier item "recover the stranded rows" is withdrawn: the files no longer exist.

#### Update 2026-11-12 16:15: data grab results (video purge exposure; whole-history wake census)

Sources: `data/station-forensics/orc-sukabumi-iss015-data-20261112T160045Z.txt`, `wp5d_filtered_2026-11-12.txt`,
`boots_2026-11-12.txt`, `server_gaps_2026-11-12.txt`. Read-only collection at the 16:00 wake.

- **Video purge exposure (time-sensitive).** ORC-OS `orc_api/utils/disk_management.py`, function `purge`, sorts every
  file under the media folder by file modification time (`os.path.getmtime`), oldest first, and deletes until free
  space is at least `min_free_space`. It does not look at upload state. `min_free_space` is 5.0 GB on this station
  (default in the code is 20; the DB default `critical_space` is 10, below which the service shuts down).
  Disk: 6.0 GB available of 62.2 GB, 90% used, so about 1.0 GB above the threshold. Directories `20260111` and
  `20260112` (48 mp4 files, about 589 MB, 787 files in all) hold the video from the offline wakes and are the oldest
  files on the disk by mtime (next oldest: `20260703`). They are first in line for deletion. Whether they were
  already uploaded to LiveORC is not known. The scheduler frequency (default 3600 s) against wakes of about 2 minutes
  means it may rarely run; the Sept notes record it was never seen firing. Not established either way.
- **Whole-history census of `wp5d.log`** (7,818 startup events from 2026-04-07: 7,745 scheduled, 44 button, 12 reboot,
  17 "Power Newly Connected", all of those in April). Every silent stop from May on matches the 42.6-day list run-out
  to within hours: 05-13 06:02 + 42.65 d = 06-24 21:30; 07-03 02:47 + 42.66 d = 08-14 18:30; 08-21 01:14 + 42.64 d =
  10-02 16:30 (each ended by a button press). **10-21 14:30 is the only stop since May that the run-out does not
  explain.** The daily re-arm (23 h interval, so a schedule activation every day) had been running since 10-12.
  One stop after nine daily activations is one observation, not evidence the activation caused it, but it is the only
  change in exposure. No I2C trouble lines within an hour of any of the stops.
- **Journal.** 1,056 boots listed; 1,051 end between 2026-07 and 2026-10-13, and only 5 end in November (all 11-12).
  The boots from 10-14 to 11-11, including the last wake before the silence, are not in the journal. For 10-21 the only
  surviving records are `wp5d.log` and the sensor CSVs.
- **Server-side history** (`station_gaps.py`): 18 outages since 04-16, 56.7 of 210.2 days. Read as "no rows", which
  includes no-network periods.
- **Files.** 68,719 files under the video directory; `20261111` and `20261112` hold the online wakes since the press.

**Candidate actions (none taken; all need Tom's approval):** (a) confirm in LiveORC whether Jan 11–12 videos exist;
(b) if not, protect them: free several GB by an approved reclaim, and/or reset the modification times of the 787 files
to a current date (metadata only, original times recorded first); (c) consider a longer re-arm interval
(`REARM_INTERVAL_H`; the list lasts 42.6 days, so a week would still be safe) to reduce activation exposure, weighing
that a daily re-arm also self-heals a bad list.


#### Update 2026-11-13: firmware v1.1, `deploy.sh` RTC guard, clock floor installed, early-boot guard installed

- **Firmware (read-only, `iss015_fw_version_read.sh`, 13:31 UTC):** the Witty Pi 5 reports id 0x51 (HAT+), **firmware v1.1**. It lacks the v1.4
  next-occurrence fix, the **v1.5 internal I2C pointer-race fix** (the release note says heavy firmware work such as schedule activation could
  corrupt register reads/writes and, "in practice", overwrite the RTC minute register) and the v1.7 RTC-alarm race fix. Our daily re-arm is a schedule
  activation, so pre-v1.5 is a live candidate (inference, unproven) for the wrong RTC month and the 10-21 stop. The vendor update path is physical
  (BOOTSEL + USB-C); a Pi-driven remote flash is not supported. Not done; needs a decision and probably a site visit. The investigation doc's old
  v1.6 row was wrong (v1.6 is "Fix configurable I2C slave address") and is corrected.
- **`pi/deploy.sh`:** the unconditional `wp5` RTC write is now `rtc_sync_fix` (writes only if chrony is synced to a real upstream and the RTC is within
  3,600 s; otherwise warns). Tested (17 checks, 7 broken copies); never run on a station. The floor install does not use `deploy.sh`.
- **Clock floor installed 18:00 UTC (wake B, build 62608e4):** `orc-clock-floor` + unit (enabled) and a new `sensors_logger.py` (rotation keeps files dated
  before 2026-03-01, which is what destroyed the offline Jan-named data after the clock was corrected). First boot with it (18:30): restore moved the clock
  from the RTC's Jan 13 to the floor within 2 s of wp5d's step (+26,263,831 s), chrony corrected it ~27 s in; unit active, no failed units, `orc-api` @23.8 s
  (28.0 s before), unit cost 2.1 s. 19:00: the shutdown-time `save` advanced the floor 18:00:49 -> 18:32:25. Video rows 7793-7800 `SYNCED` (Tom
  confirmed the 18:30 cycle uploaded a video).
- **Sensor rows reach the DB one wake late** (the uploader runs ~28 s into a wake and sends all files newer than its watermark), so a wake's later ticks
  arrive at the start of the next wake. I misread this as a fault for ~30 min on the first boot; it is not.
- **Side effect found 19:01, then fixed.** orc-capture runs the logger (`orc-capture-sensors` tag) ~14-25 s into a boot, before chrony steps the clock (~29 s).
  With the floor the clock then equals the previous shutdown time (~28 min behind), so rows were stamped early and clock-derived values were wrong:
  DB rows `orccapture` 18:32:32 (`capture_age_s` 54.2, true ~1,700) and `wittypi` 18:32:42 belong to the 19:00 boot. (Before the floor those rows got the RTC's
  January date, went to Jan CSVs and were never uploaded: lost, not mislabelled.) **Guard** (logger build `f2b79dd9`, commit 4f13423, installed 20:00 UTC by
  `iss015_logger_update_wake.sh`): `process_sensor` reads and writes nothing while the floor set the clock this boot, chrony is not synced to a real upstream
  and uptime < 45 s; the sensors are due again at the next tick. Offline wakes still log after 45 s (compressed floor-based stamps remain the known limit);
  unreadable uptime fails open. **Verified at the 20:30 boot:** journal `orccapture: deferred` and `wittypi: deferred` at 20:02:27 (floor clock), **0 rows**
  stamped in the floor window, guard state afterwards `untrusted False`; the uploader retried through four connection failures and finished at 20:30:35.
  **DB check after the 21:00 upload (21:01:40 UTC): no row stamped in any sleep window (20:03-20:30, 20:33:30-21:00)**; the 20:30 wake's rows are stamped
  20:31:13 to 20:32:12 (the normal pattern) and nothing sits on the floor-set clock around 20:02:27.
- **Tests (final commit dde7df3):** floor logic 65/65 (11 guard checks), broken copies 17/17, install/updater/rollback sandbox 25/25 (includes a forced
  post-install failure that restores the backup), `deploy.sh` guard 17/17 + 7/7. No systemd-level boot environment exists; unit ordering was checked with
  `systemd-analyze verify` against the station's real neighbouring units (no cycle) and then by the real boots above.
- **Backups and rollback:** `/var/lib/orc-clock-floor-backup/` holds the original logger (8fe3b052...) and the 18:00 build (4bb8f93a...). `iss015_floor_rollback.sh`
  restores the newest backup (the 18:00 build), disables the unit and removes the script and unit; no button press needed.
- **Open:** whether LiveORC holds the 48 January-dated offline videos (Tom); synced-mp4 retention policy; the zram-only swap drop-in (about 2 GiB);
  the raw RTC month register read and the 12-01 rollover observation; the firmware update decision; the compressed timestamps of offline wakes.


### ISS-FIELD-016: Sukabumi disk fills at about 0.56 GiB/day; the ORC-OS purge is oldest-first and ignores sync state; there is no retention policy

| Field | Value |
|-------|-------|
| **Date opened** | 2026-11-13 |
| **Site** | Sukabumi |
| **Risk** | Loss of the only copy of un-synced video; the purge reaching the 48 January-dated offline videos first |
| **Impact** | Medium (pilot station) |
| **Status** | OPEN — margin about 2.9 GiB (roughly 4.7 days) after the 2026-11-13 reclaim; next step is to move video off the station (TODO-119) |

**Observations (2026-11-13; read-only station grabs, station DB read-only, LiveORC listing of 09-16):**

- Free space 7,991 MiB at 20:30 UTC against ORC-OS's 5.0 GiB (5,120 MiB) minimum; it was 5,162 MiB at 17:00, which put the first purge at about
  19:00 UTC. The disk manager measures in **GiB**, runs about 5 s after each ORC-OS start (once per wake) and was losing about 11 to 14 MiB per wake.
- `purge()` sorts every file under the media folder by mtime and deletes the oldest first until free space is back above the minimum. It ignores sync state.
- mp4 on the station: 3,360 clips, 30.21 GiB: `SYNCED` 1,807 (16.24 GiB), `FAILED` 1,552 (13.96 GiB), `LOCAL` 1. `FAILED` does not mean not uploaded (the known
  500-after-commit failures leave some on the server), so the true un-uploaded set is smaller than 1,552 clips.
- The oldest files by mtime are the 48 January-dated offline videos (dirs 20260111 and 20260112, 0.549 GiB, all `FAILED`). The first GiB a purge would remove
  covers 213 videos: 153 `SYNCED`, 60 `FAILED`. Whether LiveORC already holds the January videos is not known (needs LiveORC credentials).
- Processing outputs are in the same tree: `output/plot_quiver.jpg` is referenced by the DB `image` column, uploaded when `sync_image=1`, and `/video/{id}/image/`
  returns a clean 404 if the file is missing.

**Done 2026-11-13:**

- Deleted the 1,076 **orphaned** quiver plots (video dir with the plot and no mp4; all `SYNCED`, July and August; they exist because the earlier reclaims deleted only
  the mp4s): 2.846 GiB, free 5,162 -> 8,079 MiB. Each was matched to a LiveORC record by timestamp (offset 0 h, all 1,076 with the image field set) and re-checked
  on the station before deletion. Allow-list: `data/station-forensics/orphan-plots-deleted-20261113-allowlist.txt`; manifest on the station:
  `/home/pi/orphan-plot-reclaim-20261113T170121Z.manifest`. Scripts: `todo119_orphan_plot_reclaim.sh.in` + `build_orphan_reclaim.py` (22 checks, 7 broken copies caught).
- `/var/swap` (2.0 GiB, fully allocated) is **not** reclaimable by deleting it: it is the zram writeback file under `rpi-swap` 1.2.1 and `rpi-resize-swap-file` re-creates it
  at every boot. The supported way is a drop-in with `[Main]` `Mechanism=zram`; not applied (about 2 GiB; generator read, not run).

**Options for headroom (none applied):** (1) upload the `FAILED` backlog (TODO-119; queue depth is the only throttle, the link resets about half the large uploads, the
prepaid balance is unmonitored); (2) copy selected files off the station by another route; (3) retention: delete `SYNCED` mp4s older than N days from a verified list
(precedent: the 09-02 reclaim; needs approval); (4) the zram-only swap drop-in; (5) a larger root device on a site visit (video must stay on the same disk as the ORC-OS DB).

**Next:** start moving some video off the station. First candidates: the 48 January videos (check LiveORC first), then the oldest `FAILED` clips.

### ISS-FIELD-017: Witty Pi 5 firmware v1.1 is six minor versions behind v1.7; the pre-v1.5 pointer race and the pre-v1.7 alarm race are live candidates for the wrong RTC month and the 10-21 stop

| Field | Value |
|-------|-------|
| **Date opened** | 2026-11-13 |
| **Site** | Sukabumi (Jakarta's unit not checked) |
| **Risk** | Recurrence of a missed startup; RTC date errors; every wake depends on the RTC alarm |
| **Impact** | Medium (pilot station) |
| **Status** | OPEN — decision needed on a firmware update (physical, needs a visit); raw RTC register read and the 12-01 rollover observation pending |

**Observations:**

- Read-only I2C reads of registers 0 to 2 (13:31 UTC): id 0x51 (HAT+), firmware **v1.1**. The installed software is 5.0.0 (June 2025), which cannot display the firmware version.
- Release notes read from the vendor repository tags: v1.2 deferred admin commands (adds a BUSY status); v1.3 fixed flash writes that "could result in corrupted data being
  written to flash"; v1.4 fixed the next-occurrence calculation and alarms not programmed when the configured day was smaller than the current day; **v1.5** fixed an internal I2C pointer
  race in which heavy firmware operations such as schedule activation could corrupt register reads/writes and, "in practice", overwrite the RTC minute register; v1.6 fixed the
  configurable I2C address; **v1.7** fixed an RTC-alarm race that could miss scheduled startups. Our daily re-arm is a schedule activation and `wp5` runs several times a minute.
- The RTC has the right day and time but the wrong month (reads Jan for Nov, +304 days). Vendor code decodes the month correctly, nothing on the Pi writes the RTC apart from
  `deploy.sh` (now guarded), and Vin was steady at the last wake before the 10-21 stop. The pointer race is **inference, not proof**: the release note names the minute register, not the month.
- Register reads: 0, 1, 2 and 80 to 86 are plain; 66 and 71 have read side effects (download stream byte, heartbeat); a read with no register byte reuses the last register. Registers 1 and 2
  carry no internal I2C access.

**Update path and risks (none attempted):** the vendor path is physical (power off, hold BOOTSEL, USB-C to a computer, copy the `.uf2`; HAT+ and Mini builds differ); no reset-to-BOOTSEL USB
interface was found, so a Pi-driven flash is not supported. Open risks: firmware v1.7 with software 5.0.0 is untested together (our `orc-wp5-rearm` drives the 5.0.0 menu and hard-checks the version);
whether `conf` and `schedule` survive a flash is unverified (copy the emulated drive's `conf`/`log`/`schedule` off first, which also gives `WittyPi5.log`); the RTC month stays wrong after an update
and any RTC write needs a schedule re-arm in the same wake. A spare Witty Pi 5 and Pi would allow a rehearsal; its existence is unknown.

**Next:** raw register 85 read (needs Tom's go); observe the RTC across 2026-11-30 -> 12-01 (month 02 and day 1 means the chip is fine and only the read is wrong; Jan 31 means the chip counts January);
ask the team about a spare unit, a laptop with a USB-C cable and a CR2032; decide on the update.

### ISS-FIELD-018: Offline wakes get compressed, floor-based timestamps; sensor rows reach the database one wake late (known limits of the clock floor)

| Field | Value |
|-------|-------|
| **Date opened** | 2026-11-13 |
| **Site** | Sukabumi |
| **Risk** | Mislabelled timestamps on sensor rows from wakes with no network |
| **Impact** | Low to medium (pilot station; rows were previously lost, not mislabelled) |
| **Status** | OPEN — accepted limitation of the clock floor; revisit after the 2026-12-01 RTC observation |

**What happens:** a wake with no network never gets a chrony step. `orc-clock-floor` sets the clock to the saved floor (the previous shutdown time) at boot and advances it only by the length of the wake, so
consecutive offline wakes start where the previous one ended: a day offline is squeezed into a few hours of timestamps just after the last synced wake. The rows are no longer stranded in January files
(which were also deleted by log rotation after the clock was corrected), but they upload later with wrong times. The logger defers rows only for the first 45 s of a floor-set boot while chrony is unsynced
(the early-boot guard, installed 2026-11-13 20:00 UTC); after that it logs with floor-based stamps.

**Month repair (deferred):** taking year and month from the floor and day and time of day from the RTC copy would give true timestamps, but it trusts the RTC's day-of-month and time of day, which are unproven until the
12-01 rollover: if the register really holds January, the RTC's day drifts at month end and the repair could accept a date about 30 days ahead inside its window.

**Also noted (not a fault):** the uploader runs about 28 s into each wake and sends every file newer than its watermark, so a wake's later sensor ticks reach the database at the start of the next wake.

**Options:** accept; add `clock_state` columns to the sensor `CSV_HEADER` confs (the ingest turns every numeric column into a metric, so no schema change, but two new metrics per sensor appear in Grafana and the sheets export);
the month repair after 12-01.
