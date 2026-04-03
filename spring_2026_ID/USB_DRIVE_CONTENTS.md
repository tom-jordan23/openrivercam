# USB Drive & Tackle Box Contents — Leave-Behind for PMI Team

**Purpose:** Two USB sticks left with the local team, plus a small parts tackle box.
One USB per site, each containing everything needed to rebuild or troubleshoot that station.

---

## USB Drive Contents (both drives get everything)

### 1. ORC-OS Base Image
- [ ] ORC-OS `.img.gz` from Hessel / Rainbow Sensing (latest)
- [ ] Raspberry Pi Imager installer (Windows + Mac)

### 2. This Repository (full clone)
- [ ] `spring_2026_ID/` directory — complete snapshot at time of departure

### 3. Printable Documentation (PDF exports)
- [ ] Assembly guide — Sukabumi (`docs/ASSEMBLY_SUKABUMI.md`)
- [ ] Assembly guide — Jakarta (`docs/ASSEMBLY_JAKARTA.md`)
- [ ] Wiring guide — Sukabumi (`docs/WIRING_SUKABUMI.md`)
- [ ] Wiring guide — Jakarta (`docs/WIRING_JAKARTA.md`)
- [ ] GPIO wiring reference (`diagrams/sukabumi/GPIO_WIRING.md`)
- [ ] Troubleshooting guide (`docs/TROUBLESHOOTING.md`)
- [ ] Door sheet — Sukabumi (`docs/DOOR_SHEET_SUKABUMI.md`)
- [ ] Door sheet — Jakarta (`docs/DOOR_SHEET_JAKARTA.md`)
- [ ] Continuity checklist — Sukabumi (`docs/CONTINUITY_CHECKLIST_SUKABUMI.txt`)
- [ ] Continuity checklist — Jakarta (`docs/CONTINUITY_CHECKLIST_JAKARTA.txt`)
- [ ] LED status spec (`docs/LED_STATUS_SPEC.md`)
- [ ] Reboot checklist (`docs/REBOOT_CHECKLIST.md`)
- [ ] Network convention (`pi/NETWORK_CONVENTION.md`)

### 4. Wiring Diagrams (print-ready)
- [ ] Circuit diagram — Sukabumi (PDF + SVG)
- [ ] Circuit diagram — Jakarta (TXT — PDF not yet generated)
- [ ] DIN rail layout — Sukabumi (SVG)
- [ ] DIN rail layout — Jakarta (SVG)
- [ ] System overview — Sukabumi (SVG)
- [ ] System overview — Jakarta (SVG)

### 5. Camera Configuration
- [ ] `camera/` directory (camtool.py + all XML configs + cameras.json)
- [ ] Camera credentials document (separate encrypted file or printed)

### 6. Pi Overlay Files & Deploy Script
- [ ] `pi/` directory (deploy.sh + shared/ + sukabumi/ + jakarta/)
- [ ] `pi/PACKAGES.md` — package manifest

### 7. Build Reference Photos
- [ ] Normalized build photos (`build_notes/sukabumi/photos/`)
- [ ] Key assembly photos showing cable routing, component placement

### 8. BOMs & Spares Lists
- [ ] BOM_Sukabumi.md
- [ ] BOM_Jakarta.md
- [ ] BOM_Spares.md

---

## Small Parts Tackle Box

Leave behind with the PMI team for field service. Organized in a small compartment tackle box.

### Connectors & Adapters
- [ ] SMA gender changers (male-male, female-female) — for antenna troubleshooting
- [ ] Nano SIM card carriers / adapters (nano → micro, nano → full)
- [ ] Spare SIM ejector pins
- [ ] IP68 RJ45 waterproof couplers (spare)
- [ ] RJ45 connectors + boots (10x)
- [ ] Cable glands — M12, M16, M20 (2-3 each)
- [ ] Dupont connector kit (male/female headers + housings)

### Fasteners & Hardware
- [ ] Stainless steel screws — M2.5, M3 assorted lengths
- [ ] Standoffs — M2.5 assorted (for Pi mounting)
- [ ] DIN rail clips (spare)
- [ ] Fuses — 5A, 10A (5 each)
- [ ] Inline fuse holders (spare)
- [ ] Terminal block jumpers

### Consumables
- [ ] Cable ties (assorted sizes)
- [ ] Heat shrink tubing (assorted)
- [ ] Dielectric grease (small tube)
- [ ] Silicone sealant (small tube)
- [ ] Electrical tape (1 roll)
- [ ] Isopropyl alcohol wipes
- [ ] Microfiber cloths (for camera lens)
- [ ] GORE vent M12 (spare)

### Spares (small items only — not full components)
- [ ] SD cards (32GB) with OS image pre-flashed (2x)
- [ ] USB flash drive (Samsung FIT Plus 256GB) pre-imaged if possible
- [ ] LTE antenna (spare)
- [ ] ML-2020 RTC battery (spare)

---

## Notes

- Label each USB drive clearly: "ORC Field Service — All Sites"
- Use USB 3.0 drives, 32GB minimum
- Format as exFAT (readable on Windows, Mac, Linux)
- Include a top-level README.txt on each drive explaining the contents
- PDF exports should be generated from the markdown files before departure
