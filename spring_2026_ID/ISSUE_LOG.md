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

### ISS-003: Video capture changed from RTSP to FTP

| Field | Value |
|-------|-------|
| **Date opened** | 2026-03-13 |
| **Site** | Both |
| **Risk** | Low |
| **Impact** | High |
| **Status** | RESOLVED (documentation updated; FTP server setup still needed) |

**Problem:**
The original design used RTSP streaming (Pi pulls video from camera via ffmpeg) for
video capture. RTSP quality is not high enough for ORC river monitoring analysis.

**Decision:**
Switch to FTP-based capture. The camera saves full-resolution video/snapshots and
pushes them via FTP to the Pi, which runs an FTP server (vsftpd). Files land in
NodeORC's `incoming/` directory for processing.

**Why this matters:**
This is a fundamental change to the capture pipeline. It affects camera configuration,
Pi software setup (FTP server needed), the capture workflow, and all documentation
that referenced RTSP/ffmpeg. The ANNKE C1200 already supports FTP via ISAPI, and
`camtool.py` already has an `ftp` endpoint, so the camera side is straightforward.

**What changed:**
- Camera config: FTP upload instead of RTSP streaming
- Pi software: needs FTP server (vsftpd) instead of ffmpeg capture script
- Capture flow: camera pushes → Pi receives (vs. Pi pulls via RTSP)

**Files updated:**
- `CLAUDE.md` — compatibility/gaps tables
- `BOM_Sukabumi.md` — camera notes, pre-deployment steps, troubleshooting
- `TODO.md` — TODO-004 updated
- `docs/ASSEMBLY_SUKABUMI.md` — checklists, camera config steps, verification
- `docs/ASSEMBLY_JAKARTA.md` — camera config steps, verification
- `docs/WIRING_SUKABUMI.md` — operation description
- `docs/TROUBLESHOOTING.md` — flowcharts, command reference
- `TRAVEL_AND_IMPORT.md` — pre-departure checklist
- `build_notes/CLAUDE.md` — phase description
- `build_notes/sukabumi/build_checklist.md` — Phase 7, 11, 12 updated

**Still needed:**
- FTP server setup procedure finalized (vsftpd config, user creation)
- Camera FTP schedule/trigger mechanism confirmed with ORC team
- File naming convention confirmed for NodeORC compatibility

---
