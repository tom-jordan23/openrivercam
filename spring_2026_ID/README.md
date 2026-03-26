# Spring 2026 Indonesia Deployment

Hardware build documentation for two ORC river monitoring stations deployed
to Indonesia in Spring 2026. These stations run
[ORC-OS](https://github.com/localdevices/ORC-OS) on Raspberry Pi 5.

## Sites

| Site | Power | Camera | Status |
|------|-------|--------|--------|
| **Sukabumi** | Solar (existing 200W/50Ah) | ANNKE C1200 PoE, power-cycled with Pi | Assembly in progress |
| **Jakarta** | AC utility + 24hr UPS | ANNKE C1200 PoE, continuous | Pending Sukabumi completion |

## Directory Guide

### Build Documentation

| Path | What's In It |
|------|-------------|
| [docs/ASSEMBLY_SUKABUMI.md](docs/ASSEMBLY_SUKABUMI.md) | Step-by-step assembly guide for the Sukabumi station |
| [docs/ASSEMBLY_JAKARTA.md](docs/ASSEMBLY_JAKARTA.md) | Step-by-step assembly guide for the Jakarta station |
| [docs/WIRING_SUKABUMI.md](docs/WIRING_SUKABUMI.md) | Power distribution and wiring overview — Sukabumi |
| [docs/WIRING_JAKARTA.md](docs/WIRING_JAKARTA.md) | Power distribution and wiring overview — Jakarta |
| [docs/MODEM_VERIFICATION_SUKABUMI.md](docs/MODEM_VERIFICATION_SUKABUMI.md) | LTE modem bench-test procedure and AT command reference |
| [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) | Diagnostic flowcharts for common issues |
| [docs/images/](docs/images/) | Build photos referenced in the docs |

### Wiring Diagrams

| Path | What's In It |
|------|-------------|
| [diagrams/sukabumi/GPIO_WIRING.md](diagrams/sukabumi/GPIO_WIRING.md) | Detailed GPIO wiring instructions with pin maps, verification checklists, and build photos |
| [diagrams/sukabumi/circuit_diagram.txt](diagrams/sukabumi/circuit_diagram.txt) | ASCII circuit diagram — full electrical schematic |
| [diagrams/sukabumi/](diagrams/sukabumi/) | Additional diagrams (DIN rail layout, system overview) |
| [diagrams/jakarta/](diagrams/jakarta/) | Jakarta site diagrams |

### Bills of Materials

| Path | What's In It |
|------|-------------|
| [BOM_Sukabumi.md](BOM_Sukabumi.md) | Full BOM with pricing and sourcing — solar site |
| [BOM_Jakarta.md](BOM_Jakarta.md) | Full BOM with pricing and sourcing — AC power site |
| [BOM_Spares.md](BOM_Spares.md) | Spare parts inventory for the PMI field office |
| CSV versions of each are also available for import into spreadsheets. |

### Software and Configuration

| Path | What's In It |
|------|-------------|
| [camera/](camera/) | Camera configuration tool (camtool.py) and ISAPI XML templates for ANNKE C1200 |
| [pi/](pi/) | Pi OS overlay files — network config, dnsmasq, MOTD, systemd services |

### Planning and Reference

| Path | What's In It |
|------|-------------|
| [SITES.md](SITES.md) | Site requirements, equipment lists, and field conditions |
| [TRAVEL_AND_IMPORT.md](TRAVEL_AND_IMPORT.md) | Customs strategy, airline restrictions, what to carry vs source locally |
| [TODO.md](TODO.md) | Current task tracking |
| [ISSUE_LOG.md](ISSUE_LOG.md) | Problems encountered and resolutions |
| [research/](research/) | 27 technical research documents covering components, power, humidity, cameras, and more |

### Build Notes and Photos

| Path | What's In It |
|------|-------------|
| [build_notes/](build_notes/) | Assembly notes, parts procurement tracking |
| build_photos/ | Raw build photo dumps (gitignored — not in version control) |

## Design Principles

All hardware decisions follow these rules (from the project
[DESIGN_SPECS](../rc-box/DESIGN_SPECS.md)):

1. **Commodity electronics only** — no custom PCBs, no single-source components
2. **No soldering** — all connections via screw terminals, plugs, or headers
3. **No specialized skills** — assembly by non-technical personnel
4. **Common tools only** — Phillips screwdriver, adjustable wrench, wire strippers
5. **Field serviceable** — maximum 5 minutes to replace any component
