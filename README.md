# OpenRiverCam in Indonesia — field deployment record

Camera-based river monitoring stations built for **Palang Merah Indonesia (PMI)**
and the **American Red Cross**, deployed in Indonesia in April 2026.

This repository is the complete engineering record of that work: hardware
designs, bills of materials, wiring and assembly guides, survey procedures,
operator documentation in English and Bahasa Indonesia, and the field findings —
including the failures, which are the more useful half.

**This is not the OpenRiverCam software.** The measurement software is
[ORC](https://github.com/localdevices/ORC) and its Raspberry Pi operating system
[ORC-OS](https://github.com/localdevices/ORC-OS), developed and maintained by
[LocalDevices](https://github.com/localdevices). We are grateful to the ORC
authors — particularly Hessel Winsemius — for an excellent open platform and for
their support throughout these deployments. What is ours is everything around
it: the station that carries the camera, and what happened when it went outside.

---

## Start here

| If you are… | Start with |
|---|---|
| **A partner institution considering building one** | [Replicating this design](#replicating-this-design) — the bills of materials, assembly guides, and what we would change |
| **Evaluating the work** | [What we found](#what-we-found) — the field findings, written to be read cold |
| **Inheriting or operating the system** | [Operating a station](#operating-a-station) — operator guide, troubleshooting, runbooks |
| **Looking for the current state** | [Status](#status) — where the two stations actually are |

---

## Status

**As of 2026-09-03.** For the detail behind this table, see
[`spring_2026_ID/README.md`](spring_2026_ID/README.md); for open work, see
[`spring_2026_ID/TODO.md`](spring_2026_ID/TODO.md) and
[`PROGRAM_TODO.md`](PROGRAM_TODO.md).

| Site | State |
|------|-------|
| **Sukabumi** | **Deployed and operating.** Solar powered, 30-minute duty cycle. Calibrated from an **IPB total-station survey** — camera config `Fit 6`, applied 2026-06-11, **0.037 m RMSE** against a 5 cm target. Uploading video and sensor data to a LiveORC server. Availability and upload reliability are the active problems; both are documented in [`findings/`](spring_2026_ID/findings/). |
| **Jakarta** | **Built, never deployed.** Permission for the intended site fell through during the trip. The station is complete and software-ready, held at Wisma PMI in Jakarta and unpowered since April 2026. It is offered as a **study and test unit** for IPB or BHLK — not for operational service, since it carries the design we now recommend changing. |

Two RTK surveys at Sukabumi in April 2026 failed reproducibly, at roughly 30×
the applicable tolerance, and nothing on site caught it. That failure and its
consequences run through much of what follows. It was resolved by IPB
re-surveying the site with a total station.

---

## What we found

The [`spring_2026_ID/findings/`](spring_2026_ID/findings/) directory holds ten
write-ups from the deployed station. Each is written to be read without prior
context. Two are defects in upstream software rather than in our own work:

| Finding | What it establishes |
|---|---|
| [Optical water level fails through daylight](spring_2026_ID/findings/optical_wl_daytime_glint.md) | Every optical water-level rejection in a 200-capture sample fell between 06:00 and 19:00; none at night. Each failure costs the whole discharge measurement, not just the level. |
| [A duty-cycled station never drains its sync backlog](spring_2026_ID/findings/orc_os_backlog_sync_starvation.md) | Source-verified against ORC-OS 0.6.0 and reproduced in a local harness. Upstream-relevant. |
| [LiveORC returns 500 on a subset of video uploads](spring_2026_ID/findings/liveorc_video_500_timeseries_collision_2026-09-03.md) | A one-to-one field collision, not a transport fault. The clips are on the server; the station records them as failed. Upstream-relevant. |
| [Anatomy of the upload failures](spring_2026_ID/findings/sukabumi_upload_failures_anatomy_2026-09-03.md) | Nine post-outage failures resolve to three distinct faults, not one. |
| [Duty cycle and the 4.8-day outage](spring_2026_ID/findings/sukabumi_duty_cycle_2026-08-28_outage.md) | Reconstructed from 5,714 recorded boots. The cause was an unfunded prepaid SIM; the station was awake and healthy throughout. |

Also: [`ISSUE_LOG.md`](spring_2026_ID/ISSUE_LOG.md) tracks every build and field
issue with its resolution, and
[`LESSONS_LEARNED.md`](spring_2026_ID/LESSONS_LEARNED.md) is the trip
retrospective.

---

## Replicating this design

At a meeting with PMI, IPB and BHLK at Sukabumi on 21 August 2026, BHLK offered
to duplicate one to three units as a pilot. The material below is what that
would need.

**Start with the recommendations, not the build guides.**
[`spring_2026_ID/docs/RECOMMENDATIONS.md`](spring_2026_ID/docs/RECOMMENDATIONS.md)
is the source of record for **R1–R37**: what we would keep, what we would change,
and why. Several are substantial — an independent water-level reference rather
than optical detection alone (R1), mains power as the default rather than solar
(R11), and compute hardware with storage, power and timekeeping integrated
rather than assembled from separate boards (R37). A report presenting these for
IPB and BHLK is in internal review and will be linked here once circulated.

| Material | Path |
|---|---|
| Bills of materials, costed — ~USD 1,340 in materials for the solar station | [`BOM_Sukabumi.md`](spring_2026_ID/BOM_Sukabumi.md) · [`BOM_Jakarta.md`](spring_2026_ID/BOM_Jakarta.md) · [`BOM_Spares.md`](spring_2026_ID/BOM_Spares.md) |
| Assembly guides — full build, commissioning, EN + ID | [`ASSEMBLY_SUKABUMI.md`](spring_2026_ID/docs/ASSEMBLY_SUKABUMI.md) · [`ASSEMBLY_JAKARTA.md`](spring_2026_ID/docs/ASSEMBLY_JAKARTA.md) |
| Wiring — power distribution, GPIO, relay | [`WIRING_SUKABUMI.md`](spring_2026_ID/docs/WIRING_SUKABUMI.md) · [`WIRING_JAKARTA.md`](spring_2026_ID/docs/WIRING_JAKARTA.md) · [`diagrams/`](spring_2026_ID/diagrams/) |
| Survey procedures, and how ours failed | [`survey/`](survey/) · [`Sukabumi_survey_salvage_methodology.md`](survey/Sukabumi_survey_salvage_methodology.md) |
| Component research — 29 documents on cameras, power, enclosures, humidity, cellular | [`spring_2026_ID/research/`](spring_2026_ID/research/) · [`rc-box/research/`](rc-box/research/) |

**Design constraints**, held throughout and recommended for retention: commodity
multi-source parts only; no soldering or custom PCBs; assembly by non-specialist
personnel; common hand tools; any component replaceable in five minutes.

---

## Operating a station

Documentation is written in English and built to PDF in both English and Bahasa
Indonesia — 15 English and 13 Indonesian documents in
[`spring_2026_ID/docs/pdf/`](spring_2026_ID/docs/pdf/). Indonesian translations
are machine-generated, carry a disclaimer, and have not been reviewed by a human
translator.

| Document | For |
|---|---|
| [Operator Guide](spring_2026_ID/docs/OPERATOR_GUIDE.md) | Day-to-day operation, LED status, maintenance |
| [Troubleshooting](spring_2026_ID/docs/TROUBLESHOOTING.md) | Diagnostic flowcharts and command reference |
| [Field Survey Guide](spring_2026_ID/docs/FIELD_SURVEY_GUIDE.md) | Survey checklist for camera calibration |
| [Door sheets](spring_2026_ID/docs/DOOR_SHEET_SUKABUMI.md) | Fuse map and pinout, to laminate inside the enclosure |
| [Server runbooks](spring_2026_ID/liveorc_server/) | LiveORC server operation, media volume, reprocessing |

To rebuild the PDFs:

```bash
cd spring_2026_ID/docs
./build_pdf.sh              # English
./build_pdf.sh --lang id    # Bahasa Indonesia
./build_pdf.sh --list       # what is registered, and versions
```

---

## Repository layout

```
README.md                 This page
PROGRAM_TODO.md           Handoff and next-generation hardware work

spring_2026_ID/           The 2026 deployment — the bulk of the work
├── docs/                 Field documentation, PDF/deck build pipeline, figures
├── findings/             Field findings from the deployed station
├── research/             29 component and design research documents
├── diagrams/             Wiring and system diagrams (.drawio, .svg)
├── liveorc_server/       Server deployment, runbooks, station-health tooling
├── pi/                   Raspberry Pi overlay, services, deploy.sh
├── camera/               Camera configuration tool and ISAPI templates
├── sukabumi_bringup/     Station bring-up scripts
├── build_notes/          Assembly notes and photographs
├── archive/              Pre-trip planning, kept for reference
├── BOM_*.md/csv          Bills of materials
├── TODO.md               Operations task list
├── ISSUE_LOG.md          Build and field issues, with resolutions
└── LESSONS_LEARNED.md    Trip retrospective

survey/                   RTK and total-station procedures, auto-fit pipeline
rc-box/                   Earlier hardware platform specification and research
manual/                   Humanitarian river monitoring manual (76 files)
prior_work/               Archived research predating this deployment
```

Where documentation overlaps, this page carries the short dated status and points
outward; `spring_2026_ID/README.md` carries deployment detail; `TODO.md` and
`PROGRAM_TODO.md` are the working logs. Status is maintained in one place per
fact.

---

## Partners

**Palang Merah Indonesia (PMI)** · **Institut Pertanian Bogor (IPB)** ·
**Balai Hidrologi dan Lingkungan Keairan (BHLK)** · **American Red Cross**

IPB re-surveyed the Sukabumi site with a total station after our RTK surveys
failed, which is what makes the station's current calibration usable.

---

## Licence and reuse

**The intent is that this work is freely shareable** — code, documentation,
build notes and installation instructions alike. That position has been given to
PMI in writing, and partner institutions are welcome to study, copy and build on
the design.

**A formal licence file has not landed yet**, which means the repository does
not yet say this in the way a licence does. That is being fixed — see TODO-202
in [`PROGRAM_TODO.md`](PROGRAM_TODO.md). In the meantime, take the paragraph
above as the intent and get in touch if you need something more definite.

Two items here are **not ours to license** and are excluded from whatever
licence is adopted: the third-party flow-measurement guide redistributed under
`manual/`, and the partner organisation logos under
`spring_2026_ID/docs/logos/`.

## Related projects

| Project | Link |
|---------|------|
| **OpenRiverCam documentation** — the upstream software documentation | [openrivercam.org/documentation](https://openrivercam.org/documentation/) |
| **ORC** — the river monitoring software | [github.com/localdevices/ORC](https://github.com/localdevices/ORC) |
| **ORC-OS** — Raspberry Pi OS for ORC field stations | [github.com/localdevices/ORC-OS](https://github.com/localdevices/ORC-OS) |
| **LocalDevices** — the organisation behind both | [github.com/localdevices](https://github.com/localdevices) |

If you are looking for how the ORC software works, start with the documentation
site above. This repository covers what it took to put it in a river.
