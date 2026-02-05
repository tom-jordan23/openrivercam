# OpenRiverCam - Indonesia Spring 2026 Deployment

River monitoring for flood early warning using camera-based surface velocity measurement. This repository tracks planning and documentation for the Spring 2026 deployment to Indonesia.

## Current Focus

**Trip:** March/April 2026
**Sites:** Sukabumi (redeploy) + Jakarta (new install)
**Budget:** $3,000 USD for both sites
**Method:** Personal carry with humanitarian papers

### Site Summary

| Site | Power | Camera | Status |
|------|-------|--------|--------|
| **Sukabumi** | Solar (existing 200W/50Ah) | USB + Gore vent housing | Replacing failed unit due to humidity damage |
| **Jakarta** | AC utility + 24hr UPS | Factory-sealed PoE (2 cameras) | New training/demonstration site |

### Planning Status

- **Research phases 1-5:** Complete (mounting, humidity, UI, cameras, connectivity)
- **BOMs:** In progress - site-specific bills of materials with pricing
- **Travel/import strategy:** Documented - what to carry vs source locally
- **Wiring diagrams:** Complete for both sites

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
- Sukabumi: Custom NoIR USB camera in VA Imaging aluminum housing
- Jakarta: ANNKE C1200 factory-sealed PoE cameras with built-in IR

**IR illumination:** Tendelux AI4 with built-in photocell + Numato USB relay (no cable cutting)

## Next Steps

1. Finalize BOMs with current pricing and lead times
2. Order long-lead items (custom NoIR camera needs 2-6 weeks)
3. Request humanitarian letter from sponsoring organization
4. Pre-configure and conformal coat electronics before travel
