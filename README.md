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

## Current Focus

Both stations are in active build. Sukabumi is in software integration
testing. Jakarta wiring is underway. Departure ~April 15, 2026.

### Deployment Overview

**Trip:** April 2026
**Sites:** Sukabumi (redeploy) + Jakarta (new install)
**Budget:** $3,000 USD for both sites
**Method:** Personal carry with humanitarian papers

### Site Summary

| Site | Power | Camera | Status |
|------|-------|--------|--------|
| **Sukabumi** | Solar (existing 200W/50Ah) | Factory-sealed PoE (1 camera) | ORC-OS config and capture testing |
| **Jakarta** | AC utility + 24hr UPS | Factory-sealed PoE (1 camera) | 12V/5V wiring complete, relay wired, first Pi boot done |

### Project Status

- **Research phases 1-5:** Complete
- **BOMs:** Complete — equipment ordered and mostly received
- **Travel/import strategy:** Documented (TRAVEL_AND_IMPORT.md)
- **Wiring diagrams:** Complete for both sites
- **Assembly docs:** Comprehensive step-by-step guides with build photos, continuity checklists, door sheets, and bilingual exterior placards
- **Sukabumi hardware:** Mounted, wired, powered on, relay tested, RTC and SHT40 installed. ORC-OS software integration in progress.
- **Jakarta hardware:** AC power chain complete (surge suppressor → PSU → 12V distribution). 5V buck converter trimmed and wired to Pi. Relay 5V side wired. CH1 PoE path wired. First boot successful.
- **Software:** `orc-capture` script with quality gate, `poe-relay` control, `orc-sensors` for SHT40, `orc-sensors-upload` (incremental scp of sensor CSVs to LiveORC on every boot / hourly), `orc-preflight` checks. Site-specific config via `RELAY_MODE` (cycle for solar, always for AC).
- **Remaining:** LED decision (ISS-005), rain gauge external wiring, J2 power buttons, conformal coating, final integration testing, Jakarta battery+charger (sourced in-country)

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

1. Finalize status LED design (ISS-005 — decision by 3/30)
2. Complete ORC-OS software integration on Sukabumi
3. Complete Jakarta wiring (sensors, rain gauge, power button)
4. Conformal coat both stations
5. Final integration testing (end-to-end capture on both)
6. Print and laminate door sheets and exterior placards
7. Pack per TRAVEL_AND_IMPORT.md

## Related Projects

| Project | Description | Link |
|---------|-------------|------|
| **ORC-OS** | Raspberry Pi operating system for ORC field stations | [github.com/localdevices/ORC-OS](https://github.com/localdevices/ORC-OS) |
| **LocalDevices** | Organization behind ORC and ORC-OS | [github.com/localdevices](https://github.com/localdevices) |
