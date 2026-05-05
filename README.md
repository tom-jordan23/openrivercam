# OpenRiverCam - Indonesia Spring 2026 Deployment

**This is a field deployment repository, not the OpenRiverCam software itself.**

This repo contains hardware build documentation, wiring guides, bills of
materials, and deployment planning for two river monitoring stations in
Indonesia. The actual river monitoring software is
[OpenRivercam (ORC)](https://github.com/localdevices/ORC) and its Raspberry
Pi operating system [ORC-OS](https://github.com/localdevices/ORC-OS),
developed and maintained by [LocalDevices](https://github.com/localdevices).

We are grateful to the ORC authors — particularly Hessel Winsemius — for
creating an excellent open-source platform for camera-based river surface
velocity measurement, and for their generous support and guidance throughout
our deployments.

## Current Status (post-trip, May 2026)

The April 2026 deployment trip is complete. Outcomes:

| Site | Outcome |
|------|---------|
| **Sukabumi** | Hardware deployed and operating. Two RTK surveys (2026-04-20 + 2026-04-21) reproduced the same ~99 cm H / 139 cm V check-point spread, ~30× worse than the 3 cm RTK gate. We are engaging IPB (Bogor University) for a **total station** re-survey. In the meantime the station is being brought up using the auto-fit salvage pipeline (`survey/Sukabumi_survey_salvage_methodology.md`), which finds a 6-GCP subset producing a 4.61 cm RMSE calibration that passes the standard quality gate (the absolute discharge inherits the survey noise floor — qualitative monitoring is fine, certified discharge needs the IPB re-survey). |
| **Jakarta** | **Not deployed.** Permission for the intended site fell through during the trip. The pre-built station was not installed. We are consulting with IPB on site selection before the next attempt. |

### Active workstreams

1. **Sukabumi configuration** — promote the salvage `CameraConfig` (4.61 cm RMSE on the 6-GCP subset) into the deployed station's ORC-OS so it produces velocity fields from live captured video. End-to-end has already run once on the calibration video (`q_50 = 0.51 m³/s`); remaining work is enabling that on real captures and locking down `h_ref = 617.065 m` through the dashboard so it survives subsequent saves.
2. **Grafana on the LiveORC server** — stand up a Grafana instance on the AWS LiveORC host to visualize sensor CSVs (rain gauge, SHT40, DS18B20) being uploaded by `orc-sensors-upload`.
3. **LiveORC upload verification** — confirm video and sensor uploads from Sukabumi are landing on the LiveORC server cleanly.

Pre-trip planning docs (departure schedule, day-by-day TODO list, pre-trip task tracking) have been moved to `spring_2026_ID/archive/` for reference.

### Deployment Overview (as conducted)

**Trip:** April 12–24, 2026
**Sites attempted:** Sukabumi (redeploy) + Jakarta (new install)
**Method:** Personal carry with humanitarian papers

## Repository Structure

### Active Work

```
spring_2026_ID/
├── SITES.md                 # Site requirements and equipment lists
├── TRAVEL_AND_IMPORT.md     # Customs, packing, local sourcing strategy
├── BOM_Sukabumi.md/csv      # Bill of materials - solar site
├── BOM_Jakarta.md/csv       # Bill of materials - AC power site
├── BOM_Spares.md/csv        # Spare parts for PMI office
├── diagrams/                # KiCad schematics and wiring diagrams
├── docs/                    # Assembly and wiring documentation
├── camera/                  # Camera config management (camtool.py + ISAPI XML)
├── pi/                      # Pi OS overlay files (network, dnsmasq, MOTD)
├── build_notes/             # Assembly notes and photos
└── research/                # Technical research (25+ documents)
```

### Hardware Platform

```
rc-box/
├── DESIGN_SPECS.md          # Authoritative hardware specifications
├── BOM_VERIFIED.md          # Reference BOM (PoE camera approach)
└── research/                # Camera, power, enclosure research
```

### Survey Procedures

```
survey/
├── SURVEY_PROCESS_v2.md     # RTK survey field procedures
├── SURVEY_DATA_PROCESSING.md # Post-processing workflows
├── QGIS_Reproject_WGS84_to_UTM48S.md
├── PPP_TRANSLATION.md       # Coordinate transformation
└── QUICK_NOTES.md
```

### Reference

- **manual/** - Comprehensive humanitarian river monitoring manual (~280k words, 75+ files)
- **prior_work/** - Archived documentation organized by topic

## Key Decisions

**Humidity management:**
- Jakarta: Conformal coating (MG 422C silicone) + PTC heaters + Gore vents
- Sukabumi: Conformal coating + Gore vents only (solar power constraint)
- Coating applied after full hardware testing (dry-fit first, coat last)

**Camera strategy:**
- Both sites: Single ANNKE C1200 factory-sealed PoE camera with built-in IR
- Video captured via RTSP pull (`orc-capture` script), not camera FTP push
- Camera power-cycled on Sukabumi (RELAY_MODE=cycle), always-on on Jakarta (RELAY_MODE=always)

**Power delivery:**
- Pi powered via GPIO header (DDR-60G-5 buck converter, 5.1V), not USB-C
- Relay uses NO (normally open) contacts as fail-safe — camera powers down if Pi crashes
- Active-high relay logic (verified empirically, differs from ORC-OS default)

**Wiring standards:**
- Solid core wire for all DC internal DIN rail wiring (no ferrules)
- One wire per screw terminal (no doubling up)
- AC and DC wiring physically separated (AC between rails, DC over top rail)
- Jakarta AC wiring: 2.5 mm² / 14 AWG per IEC 60364 / Indonesian SNI

## Next Steps

1. **Sukabumi: load salvage CameraConfig into ORC-OS** so the deployed station produces velocity fields from real video. The auto-fit pipeline (`survey/orc_auto_fit.py` + `--demo-override`) has already produced a `*_DEMO_UNCERTIFIED.json` config at 4.61 cm RMSE; remaining work is loading it via the ORC-OS dashboard and confirming end-to-end processing on a recent capture.
2. **Stand up Grafana on the AWS LiveORC server** to display sensor data (RG-15 rainfall, SHT40 temp/humidity, DS18B20 water/air temp) from the CSVs uploaded by `orc-sensors-upload`.
3. **Verify LiveORC video and sensor uploads** from Sukabumi are working end-to-end (capture → upload → visible in LiveORC + Grafana).
4. **Coordinate IPB engagement** for (a) Jakarta site selection and (b) total station survey at Sukabumi.

## Related Projects

| Project | Description | Link |
|---------|-------------|------|
| **ORC-OS** | Raspberry Pi operating system for ORC field stations | [github.com/localdevices/ORC-OS](https://github.com/localdevices/ORC-OS) |
| **LocalDevices** | Organization behind ORC and ORC-OS | [github.com/localdevices](https://github.com/localdevices) |
