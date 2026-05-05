# Spring 2026 Indonesia Deployment

Two ORC river monitoring stations for flood early warning, built for
deployment to Indonesia in April 2026. Built on
[ORC-OS](https://github.com/localdevices/ORC-OS) running on Raspberry Pi 5
with Witty Pi 5 HAT+ power management.

**Organizations:** American Red Cross / Palang Merah Indonesia (PMI)

## Station Status (post-trip, May 2026)

| Site | Power | Camera | Compute Stack | Status |
|------|-------|--------|---------------|--------|
| **Sukabumi** | Solar (200W panel / 50Ah battery) | ANNKE C1200 PoE, power-cycled | Pi 5 + Witty Pi 5 + G469 | **Deployed.** Two RTK surveys reproduced the same ~99 cm H / 139 cm V check-point noise (vs the 3 cm gate). Engaging IPB (Bogor University) for a total station re-survey. Running on the auto-fit salvage calibration in the meantime — 4.61 cm RMSE on a 6-GCP subset, passes the standard quality gate, but absolute discharge inherits the survey noise floor (good for qualitative trends, not for certified flow numbers). |
| **Jakarta** | AC utility (Mean Well PSU) + APC 900VA UPS | ANNKE C1200 PoE, continuous | Pi 5 + Witty Pi 5 + G469 | **Not deployed.** Permission for the intended site fell through during the trip. Station is built and software-ready. Consulting with IPB on alternate site selection. |

Pre-trip planning docs (departure schedule, day-by-day pre-trip TODOs,
pre-trip checklists) live in [`archive/`](archive/) and capture the plan as
it was before travel.

## Key Architecture

- **Video capture:** `orc-capture` pulls 5s RTSP video from PoE camera every 15 minutes
- **Processing:** ORC-OS processes video into velocity fields and discharge estimates on the Pi
- **Upload:** Results sync to [LiveORC server](https://openrivercam.endlessprojects.info/) over LTE
- **Power management:** Witty Pi 5 controls wake schedule, ORC-OS controls shutdown
- **Remote access:** Pangolin tunneled HTTPS proxy for each station
- **Maintenance mode:** GitHub-based kill switch ([orc-pmi-stations](https://github.com/tom-jordan23/orc-pmi-stations))

## Documentation

### For Field Staff (PMI)

| Document | Description | PDF |
|----------|-------------|-----|
| [Operator Guide](docs/OPERATOR_GUIDE.md) | Day-to-day operation, LED status, maintenance, troubleshooting | [EN](docs/pdf/OPERATOR_GUIDE.pdf) / [ID](docs/pdf/id/OPERATOR_GUIDE.id.pdf) |
| [Field Survey Guide](docs/FIELD_SURVEY_GUIDE.md) | RTK survey checklist for camera calibration | [EN](docs/pdf/FIELD_SURVEY_GUIDE.pdf) / [ID](docs/pdf/id/FIELD_SURVEY_GUIDE.id.pdf) |
| [Troubleshooting](docs/TROUBLESHOOTING.md) | Diagnostic flowcharts and command reference | [EN](docs/pdf/TROUBLESHOOTING.pdf) / [ID](docs/pdf/id/TROUBLESHOOTING.id.pdf) |
| [LED Status Spec](docs/LED_STATUS_SPEC.md) | LED color/pattern meanings | [EN](docs/pdf/LED_STATUS_SPEC.pdf) / [ID](docs/pdf/id/LED_STATUS_SPEC.id.pdf) |

### For Technical Installers

| Document | Description | PDF |
|----------|-------------|-----|
| [Assembly — Jakarta](docs/ASSEMBLY_JAKARTA.md) | Full build guide: hardware, software, commissioning | [EN](docs/pdf/ASSEMBLY_JAKARTA.pdf) / [ID](docs/pdf/id/ASSEMBLY_JAKARTA.id.pdf) |
| [Assembly — Sukabumi](docs/ASSEMBLY_SUKABUMI.md) | Full build guide: hardware, software, commissioning | [EN](docs/pdf/ASSEMBLY_SUKABUMI.pdf) / [ID](docs/pdf/id/ASSEMBLY_SUKABUMI.id.pdf) |
| [Wiring — Jakarta](docs/WIRING_JAKARTA.md) | Power distribution, GPIO connections, relay wiring | [EN](docs/pdf/WIRING_JAKARTA.pdf) / [ID](docs/pdf/id/WIRING_JAKARTA.id.pdf) |
| [Wiring — Sukabumi](docs/WIRING_SUKABUMI.md) | Power distribution, GPIO connections, relay wiring | [EN](docs/pdf/WIRING_SUKABUMI.pdf) / [ID](docs/pdf/id/WIRING_SUKABUMI.id.pdf) |
| [GPIO Wiring Reference](diagrams/sukabumi/GPIO_WIRING.md) | Detailed pin map, step-by-step wiring, verification checklists | — |
| [Modem Verification](docs/MODEM_VERIFICATION_SUKABUMI.md) | LTE modem bench-test and AT commands | [EN](docs/pdf/MODEM_VERIFICATION_SUKABUMI.pdf) |

### Enclosure Reference (Print and Laminate)

| Document | Description | PDF |
|----------|-------------|-----|
| [Door Sheet — Jakarta](docs/DOOR_SHEET_JAKARTA.md) | Fuse map, wiring, GPIO pins, LED status | [EN](docs/pdf/DOOR_SHEET_JAKARTA.pdf) / [ID](docs/pdf/id/DOOR_SHEET_JAKARTA.id.pdf) |
| [Door Sheet — Sukabumi](docs/DOOR_SHEET_SUKABUMI.md) | Fuse map, wiring, GPIO pins, LED status | [EN](docs/pdf/DOOR_SHEET_SUKABUMI.pdf) / [ID](docs/pdf/id/DOOR_SHEET_SUKABUMI.id.pdf) |
| [Reboot Checklist](docs/REBOOT_CHECKLIST.md) | Post-reboot verification steps | [EN](docs/pdf/REBOOT_CHECKLIST.pdf) |
| [Reboot Checklist — Jakarta](docs/REBOOT_CHECKLIST_JAKARTA.md) | Jakarta-specific post-reboot checks | [EN](docs/pdf/REBOOT_CHECKLIST_JAKARTA.pdf) |

### Bills of Materials

| Path | Description |
|------|-------------|
| [BOM_Sukabumi.md](BOM_Sukabumi.md) | Full BOM with pricing — solar site |
| [BOM_Jakarta.md](BOM_Jakarta.md) | Full BOM with pricing — AC power site |
| [BOM_Spares.md](BOM_Spares.md) | Spare parts inventory for PMI field office |

### Software and Configuration

| Path | Description |
|------|-------------|
| [pi/](pi/) | Pi OS overlay files, deploy.sh, systemd services, sensor configs |
| [pi/README.md](pi/README.md) | File inventory and deployment instructions |
| [pi/deploy.sh](pi/deploy.sh) | Automated deployment script (overlay + config + verification) |
| [camera/](camera/) | Camera configuration tool (camtool.py) and ISAPI XML templates |

### Survey

The RTK approach failed twice at Sukabumi. The active path is now:

| Path | Description |
|------|-------------|
| [survey/Sukabumi_survey_salvage_methodology.md](../survey/Sukabumi_survey_salvage_methodology.md) | Salvage calibration pipeline used on the noisy survey data — auto-fit with subset search and `--demo-override` for the DEMO-UNCERTIFIED CameraConfig currently used at Sukabumi |
| [survey/AUTO_FIT_USAGE.md](../survey/AUTO_FIT_USAGE.md) | Operator guide for the auto-fit tool |
| [survey/outsourced_survey_brief.md](../survey/outsourced_survey_brief.md) | Vendor brief / SOW used to scope the IPB total station re-survey |

The original RTK process docs (`SURVEY_PROCESS_v3_base.md`, `SURVEY_PROCESS_v3_ntrip.md`, `InaCORS_HOWTO.md`, `SURVEY_DATA_PROCESSING.md`) are retained as reference but carry a status banner — RTK is parked at Sukabumi pending the IPB total station survey.

### Planning and Reference

| Path | Description |
|------|-------------|
| [SITES.md](SITES.md) | Site requirements, equipment lists, field conditions |
| [TODO.md](TODO.md) | Active post-trip task list |
| [ISSUE_LOG.md](ISSUE_LOG.md) | Problems encountered (build + field) and resolutions |
| [LESSONS_LEARNED.md](LESSONS_LEARNED.md) | Trip retrospective and recommendations for next deployment |
| [archive/](archive/) | Historic pre-trip planning docs (SCHEDULE.md, pre-trip TODO, departure checklists) |
| [TRAVEL_AND_IMPORT.md](TRAVEL_AND_IMPORT.md) | Customs strategy, airline restrictions, packing (historical reference) |
| [research/](research/) | 27 technical research documents |
| [USB_DRIVE_CONTENTS.md](USB_DRIVE_CONTENTS.md) | USB stick and tackle box contents for PMI team |

## Generating PDFs

All documentation is maintained as English markdown. PDFs (English and
Bahasa Indonesia) are generated with pandoc + xelatex.

```bash
cd docs

# English PDFs (all docs)
./build_pdf.sh

# Bahasa Indonesia PDFs (all docs — requires Google Translate)
./build_pdf.sh --lang id

# Single doc
./build_pdf.sh OPERATOR_GUIDE.md
./build_pdf.sh --lang id OPERATOR_GUIDE.md

# List available docs and versions
./build_pdf.sh --list
```

**Prerequisites:**
```bash
sudo apt install pandoc texlive-xetex texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended
python3 -m venv docs/.venv
docs/.venv/bin/pip install googletrans==4.0.0-rc1
```

Indonesian translations include an automated-translation disclaimer and
have not been reviewed by a human translator.

## Design Principles

All hardware decisions follow these rules:

1. **Commodity electronics only** — no custom PCBs, no single-source components
2. **No soldering** — all connections via screw terminals, plugs, or headers
3. **No specialized skills** — assembly by non-technical personnel
4. **Common tools only** — Phillips screwdriver, adjustable wrench, wire strippers
5. **Field serviceable** — maximum 5 minutes to replace any component

## Build Photos

Raw build photos are in `build_photos/` (gitignored). Curated photos with
metadata are in `docs/images/` (tracked). See `build_photos/PHOTO_METADATA.md`
for the catalog.
