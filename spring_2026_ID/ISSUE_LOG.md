# Issue Log - Indonesia Spring 2026 Deployment

Tracks discovered issues, design corrections, and open questions across both sites.

| Status | Meaning |
|--------|---------|
| OPEN | Needs action |
| RESOLVED | Fix applied, verified |
| CLOSED | No longer relevant |

---

## Issues

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
