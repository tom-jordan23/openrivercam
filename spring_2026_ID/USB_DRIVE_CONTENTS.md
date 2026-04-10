# USB Drive & Tackle Box Contents — Leave-Behind for PMI Team

**Purpose:** Two USB sticks left with the local team, plus a small parts tackle box.
One USB per site, each containing everything needed to rebuild or troubleshoot that station.

---

## USB Drive Contents (both drives get everything)

### 1. ORC-OS Base Image
- [x] ORC-OS `.img.gz` from Hessel / Rainbow Sensing (latest)
- [x] Rainbow Sensing documentation
- ~~Raspberry Pi Imager installer~~ — download from raspberrypi.com as needed

### 2. This Repository (full clone)
- [x] `spring_2026_ID/` directory — complete snapshot at time of departure

### 3. Printable Documentation (PDF exports)
- [x] All 13 English PDFs in `docs/pdf/`
- [x] All 13 Indonesian PDFs in `docs/pdf/id/`
- [x] Markdown source in `spring_2026_ID/docs/` for regeneration

### 4. Wiring Diagrams (print-ready)
- [x] All diagrams included in `spring_2026_ID/diagrams/`

### 5. Camera Configuration
- [x] `camera/` directory (camtool.py + all XML configs + profiles)
- ~~Camera credentials~~ — stored on each Pi at `~/.orc_deploy_*`, not on USB

### 6. Pi Overlay Files & Deploy Script
- [x] `pi/` directory (deploy.sh + shared/ + sukabumi/ + jakarta/)
- [x] Witty Pi schedule files included

### 7. Operator, Field, and Survey Guides
- [x] All included in PDFs and markdown source
- [x] Survey process + InaCORS HOWTO in `survey/`

### 8. Build Reference Photos
- [x] Curated photos in `spring_2026_ID/docs/images/`

### 9. BOMs & Spares Lists
- [x] All BOMs included in `spring_2026_ID/`

### Excluded (easily obtainable)
- Raspberry Pi Imager — download from raspberrypi.com
- Camera credentials — on each Pi, not distributed on USB
- Pre-flashed SD cards — rebuild with ORC-OS image + deploy.sh

---

## Small Parts Tackle Box

Leave behind with the PMI team for field service. Organized in a small compartment tackle box.

### Connectors & Adapters
- [ ] SMA gender changers (male-male, female-female) — for antenna troubleshooting
- [ ] Nano SIM card carriers / adapters (nano → micro, nano → full)
- [ ] Spare SIM ejector pins
- [ ] IP68 RJ45 waterproof couplers (spare)
- [ ] RJ45 connectors + boots (10x) — crimper not included, source locally
- [ ] Cable glands — M12, M16, M20 (2-3 each)
- [ ] Dupont connector kit (male/female headers + housings)
- [ ] Ferrules — assorted sizes (match wire gauges used: 18, 22, 23 AWG)
- [ ] Ferrule crimper

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
- [ ] CR2032 coin cell batteries for Witty Pi 5 RTC (2x spare)

---

## Notes

- Label each USB drive clearly: "ORC Field Service — All Sites"
- Use USB 3.0 drives, 32GB minimum
- Format as exFAT (readable on Windows, Mac, Linux)
- Include a top-level README.txt on each drive explaining the contents
- PDF exports should be generated from the markdown files before departure
