# TODO List - Indonesia Spring 2026 Deployment

**Last updated:** 2026-04-03
**Departure:** April 12, 2026 (9 days)

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

## Completed (weeks 1-2)

Moved to Completed table at bottom of file.

---

## Today (April 3) — Hardware finish day

**Goal: Finish rain gauge wiring for both stations, boot Jakarta, box everything this weekend.**

### Sukabumi — rain gauge completion
- [ ] Complete rain gauge external wiring (SD16 bulkhead + Molex/Dupont to RG-15 J2)
- [ ] End-to-end rain gauge continuity test (Pi → bulkhead → cable → RG-15)
- [ ] Rain gauge serial test if time permits (UART, 9600 baud, `R` command)

### Jakarta — catch up to Sukabumi
- [x] AC wiring complete and tested (12.11V at PSU output)
- [x] 12V distribution wired (PSU → TB1)
- [x] DDR-60G-5 trimmed to 5.10V, wired to G469 Pin 2/Pin 25
- [x] Relay 5V side wired (G469 → relay VCC/GND/IN1-4)
- [x] Relay CH1 → fuse → PoE switch wired
- [x] J2 power button header soldered
- [x] Wire rain gauge internal side (bulkhead end loose, labeled)
- [x] Wire rain gauge external side (SD16 bulkhead + Molex/Dupont to RG-15 J2)
- [x] Wire SHT40 sensor
- [ ] Wire DS18B20 external temp probe
- [x] Install RTC battery + enable charging in config.txt
- [ ] Wire WS2812B LED (GPIO 18)
- [x] Wire J2 power button (Dupont female to header → external button) — wired, not yet tested
- [x] Full continuity and isolation checks (use Jakarta checklist)
- [x] Quick 12V rail → GPIO isolation recheck (post SHT40/RTC additions)
- [x] First boot on Jakarta — verify Pi boots from AC mains

---

## This Weekend (April 4-6) — Box, coat, cure, close

### Saturday (April 4)
**Goals: Fix Jakarta power switch, build wiring harnesses, mount devices in boxes.**
- [ ] Fix Jakarta J2 power button (not working)
- [ ] Build inside wiring harnesses — rain gauge (both stations)
  - [ ] Continuity test each SD16 cable end-to-end before connecting levers — SD16 pin numbering may have introduced accidental TX/RX crossover. Correct at lever connectors if needed.
- [ ] Build inside wiring harnesses — DS18B20 temp probe (both stations)
- [ ] Zip tie and strain relief all internal wiring (both stations)
- [ ] Install both stations into enclosures (DIN rail, cable routing, glands)
- **Stretch:** Finish bottom plates (LED light windows, power button, external connectors)

**Coating (push to after boxing is done, or Sunday):**
- [ ] Remove Pi from both enclosures (detach G469 header, lift Pi out)
- [ ] Mask in-place: G469 header pins + screw terminal faces, relay module screw terminals
- [ ] Mask Pi on bench: GPIO pins, USB, HDMI, ethernet, SD slot, J5, J2 header, heatsink pads
- [ ] Apply MG 422C silicone conformal coat:
  - Pi PCBs (on bench)
  - G469 breakout + relay module (in-place in enclosure)
- [ ] Set aside to cure (24 hours minimum)
- [ ] Install LED light windows (acrylic sandwich + neutral-cure silicone — also needs 24hr cure)

### Sunday (April 5)
- [ ] Remove masking tape after cure
- [ ] Inspect coating coverage, recoat bare spots if needed
- [ ] Reinstall Pis (seat onto G469 headers)
- [ ] Hot glue Dupont connectors (power button pigtails, LED connectors)
- [ ] Final continuity checks on both stations
- [ ] Power-on test both stations
- [ ] Verify relay/PoE/camera works on both
- [ ] Close up enclosures — ready for software week

---

## Mon–Wed (April 7–9) — Software integration

**All hardware must be complete. No more wiring.**

### Both stations
- [ ] Flash new ORC-OS image from Hessel (when available)
- [ ] Run deploy.sh (once written) or manual overlay re-application
- [ ] Configure ORC-OS capture schedule
- [ ] Camera ISAPI config via camtool.py
- [ ] orc-capture end-to-end test (relay → camera boot → RTSP → quality gate)
- [ ] Rain gauge serial communication test
- [ ] SHT40/DS18B20 sensor verification
- [ ] LED status daemon test
- [ ] Tailscale remote access setup
- [ ] Implement rain gauge capture script (TODO-001)
- [ ] Power status MOTD script (undervoltage false positive)
- [ ] Full end-to-end soak test (leave running overnight Tue→Wed)

### Jakarta-specific
- [ ] Wire PTC heater and fans (if not done this weekend)
- [ ] Verify AC → 12V → relay → PoE → camera full chain

---

## Thu–Fri (April 10–11) — Final prep and pack

**Must be packed and ready by end of day Friday April 11.**

- [ ] Network convention migration (.139 → .100) if new ORC-OS image is deployed
- [ ] Print and laminate door sheets
- [ ] Print exterior placards (English + Bahasa Indonesia)
- [ ] Print continuity checklists (blank, for field use)
- [ ] Generate USB sticks for local team (see USB_DRIVE_CONTENTS.md)
- [ ] Assemble small parts tackle box for local team (see USB_DRIVE_CONTENTS.md spare parts section)
- [ ] Final integration test (both stations complete capture cycle)
- [ ] Pack equipment per TRAVEL_AND_IMPORT.md
- [ ] Humanitarian letter from sponsoring organization
- [ ] Verify passport, visa, travel docs

### Deferred to in-country
- [ ] Jakarta battery + charger (sourced locally by PMI team)
- [ ] Jakarta mounting hardware (pending site survey)
- [ ] SIM cards (purchase in-country)
- [ ] Coordinate with PMI: RTK gear, ground control points, and survey poles last used at Sukabumi — need them at Jakarta site first

---

## Outstanding tasks (not yet scheduled)

- [ ] Power status MOTD script (TODO — undervoltage false positive from GPIO power)
- [ ] deploy.sh script for OS image re-application (see pi/NETWORK_CONVENTION.md)
- [ ] Jakarta-specific overlay files (NM connection, hosts template, dnsmasq per-site)
- [ ] Move update-motd.d/ into etc/update-motd.d/ for consistent overlay path mapping
- [ ] Fix 30-camera-status to read camera IP from config instead of hardcoding

---

## P0 — Blocking

### TODO-001: Implement rain gauge capture script for power-cycled operation (Sukabumi)

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Site** | Sukabumi |
| **Target** | Week 2 |

The RG-15 accumulates rainfall while the Pi sleeps, but no software exists to read it.
On each wake cycle the capture script must:

1. Open UART (`/dev/ttyAMA0`, 9600 baud)
2. Send `R` command, parse `Acc` field from response
3. Read previous accumulated value from disk
4. Compute delta, log interval rainfall with timestamp
5. Write new accumulated value to disk

**Decision needed:** Should this be a standalone script, a NodeORC plugin, or a PR to
the upstream NodeORC repo?

---

### TODO-002: Jakarta battery + charger selection

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Site** | Jakarta |
| **Target** | Week 2 (order) or source in-country |

BOM_Jakarta.md lists "12V LiFePO4 Battery + Charger" as TBD, price TBD.
Need to select specific product and source from Tokopedia/Shopee before travel,
or plan to source locally in Jakarta.
Must match: 12V LiFePO4, >=100Ah, with compatible charger, fits in weatherproof box.

---

### TODO-003: Jakarta mounting hardware — site survey needed

| Field | Value |
|-------|-------|
| **Status** | BLOCKED |
| **Site** | Jakarta |
| **Blocked by** | Site survey not yet completed |

Multiple items deferred pending site survey:
- Camera mounting plates/brackets
- Pole or wall mounting hardware
- Grounding rod placement
- Cable run lengths

Cannot finalize until someone visits the Jakarta site and determines mounting surfaces,
heights, and cable run lengths. May need to resolve in-country.

---

### TODO-004: Pre-configure cameras (credentials, streaming, image settings)

| Field | Value |
|-------|-------|
| **Status** | IN PROGRESS |
| **Site** | Both |
| **Target** | Week 1 (Sukabumi), Week 2 (Jakarta) |

ANNKE C1200 cameras configured via `camtool.py` using ISAPI.
FTP upload is **not used** — video is captured via RTSP pull (see ISS-003).

Remaining camera config:
- Set admin credentials (record securely)
- Push streaming config (1920x1080, H.264, 16 Mbps CBR, 12.5fps)
- Push image config (IR-only supplement light, auto IR cut filter)
- Push NTP config (Pi as NTP server)
- Verify RTSP stream accessible from Pi (`orc-capture --skip-relay --dry-run`)

---

## P1 — Important

### TODO-005: Correct stale power consumption figure in success criteria

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Site** | Sukabumi |

`BOM_Sukabumi.md` success criteria says "Power consumption <50 Wh/day" but the
corrected power budget is ~118 Wh/day. Update to reflect current PoE camera architecture.

---

### TODO-006: Jakarta power budget calculation

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Site** | Jakarta |

No detailed power budget exists for Jakarta. Need to calculate:
- Continuous load (Pi + 1 camera + modem + sensors + fans)
- UPS runtime estimate with selected battery
- PTC heater duty cycle and impact

Less critical than Sukabumi (AC power is abundant) but needed for UPS sizing.

---

### TODO-007: Jakarta GPIO wiring guide

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Site** | Jakarta |
| **Target** | Week 1-2 (build as we wire) |

Sukabumi has detailed GPIO_WIRING.md with step-by-step instructions, verification
checklists, and build photos. Jakarta needs equivalent, adapted for:
- AC power input (surge suppressor + PSU)
- 1 camera (same as Sukabumi)
- PTC heater + fans
- DS18B20 external temp probe (GPIO 4)
- Same relay, GPIO, rain gauge, SHT40 wiring as Sukabumi

Building incrementally as Jakarta wiring progresses.

---

### TODO-008: Pangolin remote access setup

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Site** | Both |
| **Target** | Week 2 |

Need:
- Pangolin server URL and account
- Newt client configuration for each device
- Test connectivity before sealing enclosures

---

### TODO-009: ORC-OS installation and configuration

| Field | Value |
|-------|-------|
| **Status** | IN PROGRESS |
| **Site** | Both |
| **Target** | Week 1 (Sukabumi), Week 2 (Jakarta) |

- Install/verify ORC-OS on each Pi
- Configure capture schedule
- Verify GPIO management (relay control)
- Verify camera FTP integration
- Coordinate with ORC team on device registration

---

### TODO-010: SIM card strategy finalized

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Site** | Both |
| **Target** | Week 2 |

Carrier decided (Telkomsel) but logistics not finalized:
- Pre-paid vs post-paid?
- Data plan size? (96 video uploads/day x ~5MB each = ~500MB/day minimum)
- Purchase SIMs in-country or arrange in advance?
- IMEI registration required?

---

### TODO-011: Wire Mean Well DC OK signal to Pi GPIO (Jakarta)

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Site** | Jakarta |
| **Target** | Week 2 |

The Mean Well SDR-120-12 has a DC OK dry contact relay output that closes when
the 12V output is stable. Wire this to a free GPIO pin (with pull-up) to let
the Pi detect whether AC mains power is present or the system is running on
battery backup. Useful for logging, power-saving behavior, and alerting.

Requires: 1 free GPIO pin, pull-up resistor (or use Pi internal pull-up),
2 wires from DC OK terminals to G469.

---

### TODO-012: Re-export circuit_diagram.pdf from updated drawio

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Site** | Sukabumi |
| **Target** | Week 3 |

The drawio source was updated but the PDF was not regenerated.

---

## P2 — Nice to Have

### TODO-012: Verify DDR-60G quiescent power draw

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Site** | Sukabumi |

Measure actual quiescent draw of DDR-60G-5 with Pi sleeping.
If significantly different from 0.5W estimate, update power budget.

---

### TODO-013: Train PMI staff on troubleshooting

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Site** | Both |
| **Target** | In-country |

Prepare training materials or plan a walkthrough session during deployment trip.
Reference: `docs/TROUBLESHOOTING.md`

---

### TODO-014: Spares inventory finalized and priced

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Site** | Both |

`BOM_Spares.md` exists but needs final pricing pass and confirmation of what's
already covered by ordered quantities vs. what needs separate ordering.

---

## Completed

| TODO | Description | Completed |
|------|-------------|-----------|
| — | Sukabumi DIN rail layout and mounting | 2026-03-20 |
| — | Sukabumi 5V buck converter wiring and test (5.1V verified) | 2026-03-20 |
| — | Sukabumi relay input wiring (5V side) | 2026-03-20 |
| — | Sukabumi relay CH1 output wiring (PoE switch) | 2026-03-21 |
| — | Sukabumi SHT40 sensor wiring | 2026-03-22 |
| — | Sukabumi RTC battery installed | 2026-03-22 |
| — | Sukabumi rain gauge internal wiring | 2026-03-25 |
| — | Sukabumi fuses installed, continuity passed | 2026-03-24 |
| — | Sukabumi first power-on (Pi boots) | 2026-03-24 |
| — | Sukabumi relay NC→NO fix | 2026-03-25 |
| — | Jakarta DIN rails mounted | 2026-03-25 |
| — | Jakarta AC distribution wired (L/N/PE terminal blocks) | 2026-03-25 |
| — | Jakarta AC power-on test (12.11V at PSU output) | 2026-03-26 |
| — | Jakarta 12V distribution wired (PSU → TB1) | 2026-03-26 |
| — | Jakarta DDR-60G-5 trimmed to 5.10V, wired to Pi | 2026-03-28 |
| — | Jakarta relay 5V side wired | 2026-03-28 |
| — | Jakarta relay CH1 → fuse → PoE switch wired | 2026-03-28 |
| — | Jakarta J2 power button header soldered | 2026-03-30 |
| — | ISS-005 resolved: LED design — WS2812B NeoPixel + acrylic sandwich | 2026-03-30 |
| — | Maintenance button removed, single power button (ISS-005/J2) | 2026-03-30 |
| — | Network convention documented (pi/NETWORK_CONVENTION.md) | 2026-04-02 |
| — | OS image management strategy planned | 2026-04-02 |
| — | orc-capture RELAY_MODE config (cycle vs always) | 2026-03-29 |
| — | Build photos cataloged and tagged (97 photos) | 2026-03-22 |
| — | Sukabumi J2 power button wired and tested (soldered pigtail + Dupont female) | 2026-04-01 |
| — | Sukabumi WS2812B LED wired, tested R/G/B + all status colors (orc-led-test) | 2026-04-01 |
| — | LED driver migrated from rpi-ws281x to Adafruit Blinka (Pi 5 PIO) — see ISS-007 | 2026-04-01 |
| — | GPIO_WIRING.md comprehensive update (Rev C) | 2026-03-20 |
| — | ASSEMBLY_SUKABUMI.md restructured (v3.2) | 2026-03-21 |
| — | ASSEMBLY_JAKARTA.md + WIRING_JAKARTA.md updated (v3.0) | 2026-03-25 |
| — | Door sheets created (both sites) | 2026-03-25 |
| — | Exterior placards created (bilingual) | 2026-03-25 |
