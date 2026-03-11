# OpenRiverCam - Indonesia Spring 2026 Deployment

River monitoring for flood early warning using camera-based surface velocity measurement. This repository tracks planning and documentation for the Spring 2026 deployment to Indonesia.

## Current Focus

Equipment ordered. Assembling the Sukabumi device, then Jakarta.

### Deployment Overview

**Trip:** March/April 2026
**Sites:** Sukabumi (redeploy) + Jakarta (new install)
**Budget:** $3,000 USD for both sites
**Method:** Personal carry with humanitarian papers

### Site Summary

| Site | Power | Camera | Status |
|------|-------|--------|--------|
| **Sukabumi** | Solar (existing 200W/50Ah) | Factory-sealed PoE (1 camera) | Assembly in progress |
| **Jakarta** | AC utility + 24hr UPS | Factory-sealed PoE (1 camera) | Pending Sukabumi completion |

### Project Status

- **Research phases 1-5:** Complete (mounting, humidity, UI, cameras, connectivity)
- **BOMs:** Complete - equipment ordered
- **Travel/import strategy:** Documented - what to carry vs source locally
- **Wiring diagrams:** Complete for both sites
- **Assembly:** Sukabumi build in progress

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
- Jakarta: Conformal coating + PTC heaters + Gore vents (full industrial approach)
- Sukabumi: Conformal coating + Gore vents only (solar power constraint)

**Camera strategy:**
- Both sites: Single ANNKE C1200 factory-sealed PoE camera with built-in IR

**IR illumination:** Tendelux AI4 with built-in photocell + Numato USB relay (no cable cutting)

## Next Steps

1. Assemble and test Sukabumi device
2. Conformal coat electronics before travel
3. Assemble and test Jakarta device
4. Request humanitarian letter from sponsoring organization
