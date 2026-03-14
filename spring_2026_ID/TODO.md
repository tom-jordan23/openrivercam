# TODO List - Indonesia Spring 2026 Deployment

**Last updated:** 2026-03-13

---

## How to Use

| Priority | Meaning |
|----------|---------|
| P0 | Blocking deployment — must resolve before travel |
| P1 | Important — should resolve before travel, workaround exists |
| P2 | Nice to have — can resolve in-country or post-deployment |

| Status | Meaning |
|--------|---------|
| OPEN | Not started |
| IN PROGRESS | Work underway |
| BLOCKED | Waiting on external input or dependency |
| DONE | Complete |

---

## P0 — Blocking

### TODO-001: Implement rain gauge capture script for power-cycled operation (Sukabumi)

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Site** | Sukabumi |
| **Relates to** | ISS-002 |
| **Depends on** | NodeORC architecture understanding |

The RG-15 accumulates rainfall while the Pi sleeps, but no software exists to read it.
On each wake cycle the capture script must:

1. Open UART (`/dev/ttyAMA0`, 9600 baud)
2. Send `R` command, parse `Acc` field from response
3. Read previous accumulated value from disk
4. Compute delta, log interval rainfall with timestamp
5. Write new accumulated value to disk

**Decision needed:** Should this be a standalone script, a NodeORC plugin, or a PR to
the upstream NodeORC repo? See `build_notes/CLAUDE.md` software ecosystem principles —
prefer upstream contribution over local fork.

---

### TODO-002: Jakarta battery + charger selection

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Site** | Jakarta |
| **Depends on** | Local supplier availability in Jakarta |

BOM_Jakarta.md lists "12V LiFePO4 Battery + Charger" as TBD, price TBD.
Need to select specific product and source from Tokopedia/Shopee before travel.
Must match: 12V LiFePO4, ≥100Ah, with compatible charger, fits in weatherproof box.

---

### TODO-003: Jakarta mounting hardware — site survey needed

| Field | Value |
|-------|-------|
| **Status** | BLOCKED |
| **Site** | Jakarta |
| **Blocked by** | Site survey not yet completed |

Multiple items deferred pending site survey:
- Hikvision DS-1275ZJ vertical mounting plates (HOLD)
- SS L-brackets, concrete anchors, SS banding
- Camera pole height and material
- Grounding rod placement

Cannot finalize until someone visits the Jakarta site and determines mounting surfaces,
heights, and cable run lengths.

---

### TODO-004: Pre-configure cameras (FTP upload, credentials)

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Site** | Both |

ANNKE C1200 cameras need FTP upload configured before deployment.
Use the ISAPI config tool (see `camera/README.md`):
- Configure FTP upload to Pi (192.168.50.1)
- Set credentials (must match Pi's FTP server user)
- Set resolution and image format per ORC requirements
- Configure scheduled snapshot/video capture
- Verify FTP upload delivers files to Pi

Also need FTP server (vsftpd) installed and configured on each Pi,
with upload directory pointing to NodeORC's `incoming/` folder.

Do this during build Phase 7 + 11 (Sukabumi) / equivalent for Jakarta.

---

## P1 — Important

### TODO-005: Correct stale power consumption figure in success criteria

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Site** | Sukabumi |
| **Relates to** | ISS-001 |

`BOM_Sukabumi.md` success criteria says "Power consumption <50 Wh/day" but the
corrected power budget is ~118 Wh/day. The 50 Wh figure is from the old USB camera
approach. Update to reflect current PoE camera architecture.

---

### TODO-006: Jakarta power budget calculation

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Site** | Jakarta |

No detailed power budget exists for Jakarta. Need to calculate:
- Continuous load (Pi + 2 cameras + modem + sensors + fans)
- UPS runtime estimate with selected battery
- PTC heater duty cycle and impact

Less critical than Sukabumi (AC power is abundant) but needed for UPS sizing.

---

### TODO-007: Jakarta wiring diagram

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Site** | Jakarta |

Sukabumi has detailed wiring docs (`WIRING_SUKABUMI.md`, `GPIO_WIRING.md`,
`circuit_diagram.txt`). Jakarta has assembly instructions but no equivalent
wire-by-wire diagram. Needed before build.

Key differences from Sukabumi:
- No Witty Pi (uses Pi 5 built-in RTC)
- AC power supply (Mean Well SDR-120-12) instead of battery direct
- 2 cameras instead of 1
- Fans for active cooling
- PTC heater (humidity control)
- Surge protector on AC input

---

### TODO-008: Pangolin remote access setup

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Site** | Both |

Build CLAUDE.md references Pangolin (Newt client) for remote access but no
credentials or server details documented yet. Need:
- Pangolin server URL and account
- Newt client configuration for each device
- Test connectivity before sealing enclosures

---

### TODO-009: NodeORC installation and LiveORC connectivity

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Site** | Both |

Build Phase 11. Need to:
- Install NodeORC on each Pi
- Configure LiveORC server URL and device credentials
- Verify task polling works on scheduled wake cycles (Sukabumi)
- Verify continuous operation (Jakarta)
- Coordinate with OpenRiverCam team on device registration

---

### TODO-010: SIM card strategy finalized

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Site** | Both |

Carrier decided (Telkomsel) but logistics not finalized:
- Pre-paid vs post-paid?
- Data plan size? (96 video uploads/day × ~5MB each = ~500MB/day minimum)
- Purchase SIMs in-country or arrange in advance?
- IMEI registration required?

---

### TODO-011: Re-export circuit_diagram.pdf from updated drawio

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Site** | Sukabumi |

The drawio source was updated (March 2026) but the PDF was not regenerated.
Open `diagrams/sukabumi/sukabumi_system.drawio` in draw.io → Export as PDF →
save as `circuit_diagram.pdf`. Need draw.io (desktop or web).

---

## P2 — Nice to Have

### TODO-012: Jakarta build checklist

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Site** | Jakarta |

Sukabumi has a detailed build checklist (`build_notes/sukabumi/build_checklist.md`).
Jakarta needs an equivalent, adapted for its different architecture (AC power, no
Witty Pi, 2 cameras, UPS, surge protection, fans).

---

### TODO-013: Verify DDR-60G quiescent power draw

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Site** | Sukabumi |
| **Relates to** | ISS-001 |

The 0.5W quiescent figure per converter is an estimate. During build Phase 13
(power budget verification), measure actual quiescent draw of both DDR-60G-5 and
DDR-60G-12 with Pi sleeping. If significantly different, update power budget.

---

### TODO-014: Train PMI staff on troubleshooting

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Site** | Both |

Success criteria includes "PMI staff trained on basic troubleshooting."
Prepare training materials or plan a walkthrough session during deployment trip.
Reference: `docs/TROUBLESHOOTING.md` (already written, needs field validation).

---

### TODO-015: Spares inventory finalized and priced

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Site** | Both |
| **Depends on** | CLAUDE.md Phase 6.3 |

`BOM_Spares.md` exists but needs final pricing pass and confirmation of what's
already covered by ordered quantities vs. what needs separate ordering.

---

### TODO-016: CLAUDE.md phase status needs updating

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Site** | N/A |

CLAUDE.md still says "Next Action: Phase 5 then Phase 6" but Phase 5 is complete.
Phase 6 (pricing) is partially done (orders submitted for both sites). Phase 6.5
(customs/import) has TRAVEL_AND_IMPORT.md written. Phase 7 (documentation) is
largely complete for Sukabumi. Update phase statuses to reflect current reality.

---
