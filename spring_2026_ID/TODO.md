# TODO List - Indonesia Spring 2026 Deployment

**Last updated:** 2026-03-25
**Departure:** ~April 15, 2026 (3 weeks)

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

## This Week (March 25–31)

### Sukabumi — ORC-OS config + power cycling + video capture

**Software first — gives maximum time to absorb problems:**
- [ ] Verify ORC-OS manages GPIO 24 (relay/PoE switch control)
- [ ] If ORC-OS doesn't manage GPIO 24, create systemd service as fallback
- [ ] Configure ORC-OS capture schedule (15-minute wake cycle)
- [ ] Camera ISAPI config (streaming, image, NTP via camtool.py)
- [ ] Rain gauge serial test (UART, 9600 baud, send `R` command)
- [ ] Pangolin/Newt remote access setup (TODO-008)

**Hardware verification (dependent on software above):**
- [x] Install 5x20mm fuses
- [x] Run full continuity checklist
- [x] First power-on (Pi boots from 12V bench supply)
- [x] Fix relay CH1 NC→NO error
- [x] Wire SHT40 sensor
- [x] Install RTC battery
- [x] Wire rain gauge internal side (bulkhead end loose, labeled)
- [ ] Power cycle test: Pi boots → GPIO 24 HIGH → PoE switch on → camera boots
- [ ] End-to-end: Pi wakes, orc-capture pulls RTSP, video delivered to ORC-OS
- [ ] Verify RTC keeps time after power off (5 minute test)
- [ ] Verify SHT40 readable (`i2cdetect -y 1` shows 0x44)

### Jakarta — complete wiring

- [x] Drill mounting plate, mount DIN rails
- [x] Mount surge suppressor, AC terminal blocks, Mean Well PSU
- [x] Wire AC distribution (L/N/PE terminal blocks)
- [ ] AC continuity checks (pre-power)
- [ ] First AC power-on — verify Mean Well 12V output
- [ ] Mount DDR-60G-5, relay, PoE switch, Pi stack, TB1, fuse holders on top rail
- [ ] Wire 12V distribution (TB1, fuses, DDR-60G-5 → Pi)
- [ ] Wire relay inputs (G469 → relay)
- [ ] Wire relay CH1 → fuse → PoE switch
- [ ] Wire SHT40 and DS18B20 sensors
- [ ] Install RTC battery
- [ ] Wire rain gauge internal side
- [ ] Full continuity and isolation checks
- [ ] Power-on test: AC → 12V → Pi boots

### Parts to arrive this week

- [x] SOMELINE crimp tool kit (Amazon, arrived — missing correct Molex KK fittings)
- [ ] SD16 4-pin bulkhead connectors ×2 (need to order)

### Before Chester's trip

- [x] Finalize LED choice — WS2812B NeoPixel RGB, config-driven status (see `docs/LED_STATUS_SPEC.md`)

### New tasks

- [ ] Power status MOTD script — Pi 5 reports undervoltage warnings when powered via GPIO instead of USB-C (expected, since PMIC doesn't see a USB-C negotiation). Write a simple script that checks `vcgencmd get_throttled` and reports recent power issues in the MOTD. Suppress or contextualize the false positive from GPIO power.

### Chester's Electronics trip (3/30)

- [ ] Molex KK 254 housings, 6-pin (Molex 22-01-3067 or equiv) — qty 2
- [ ] Molex KK 254 crimp pins (Molex 08-55-0131 or equiv) — qty 10+
- [ ] SD16 4-pin IP68 aviation connector pairs (plug + panel socket) — qty 2
- [x] ~~M1.6 or #0-80 bolts, nuts, washers (for J2 power button)~~ — not needed, used soldered pigtail approach instead
- [x] ~~O-ring crimp terminals for M1.6/#0 bolt, 18 AWG wire~~ — not needed, used soldered pigtail approach instead
- [ ] Green/yellow 12 AWG stranded wire — a few feet (Jakarta PE ground)

---

## Week 2 (March 31 – April 7)

### Sukabumi — finish integration

- [ ] Implement rain gauge capture script (TODO-001)
- [x] Wire and test J2 power button (soldered pigtail + Dupont female, strain relief zip tie)
- [ ] Wire rain gauge external side (SD16 bulkhead + 18/4 cable, once parts arrive)
- [ ] Wire WS2812B LED (GPIO 18 data, 5V/GND from G469) and install light window
- [ ] Full end-to-end soak test (leave running overnight on capture schedule)

### Jakarta — software + testing

- [ ] ORC-OS config (GPIO 24, capture schedule, RTSP capture)
- [ ] Pangolin/Newt remote access
- [ ] Power cycle test: Pi → relay → PoE switch → camera
- [ ] Test RTSP capture with orc-capture
- [ ] Wire and test J2 power button
- [ ] Wire PTC heater and fans
- [ ] Wire WS2812B NeoPixel LED (GPIO 18 data, 5V/GND from G469)
- [ ] Rain gauge serial test
- [ ] Full continuity and isolation checks

### Both sites

- [ ] Finalize SIM card strategy (TODO-010)
- [ ] Send Jakarta battery/charger specs to local team for sourcing

---

## Week 3 (April 7–14) — Final prep

### Both sites

- [ ] Conformal coating (MG 422C) — test first, coat, 24hr cure, reassemble, verify
  - [ ] Hot glue Dupont connector on power switch pigtail (secure detachable fitting)
- [ ] Final integration test (both stations running full capture cycle)
- [ ] Wire rain gauge external side (SD16 bulkhead + 18/4 cable)
- [ ] Print and laminate door sheets
- [ ] Print exterior placards (English + Bahasa Indonesia)
- [ ] Print continuity checklists (blank, for field use)
- [ ] Pack equipment per TRAVEL_AND_IMPORT.md
- [ ] Humanitarian letter from sponsoring organization (TODO still open?)

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
| — | Build photos cataloged and tagged (97 photos) | 2026-03-22 |
| — | Sukabumi J2 power button wired and tested (soldered pigtail + Dupont female) | 2026-04-01 |
| — | GPIO_WIRING.md comprehensive update (Rev C) | 2026-03-20 |
| — | ASSEMBLY_SUKABUMI.md restructured (v3.2) | 2026-03-21 |
| — | ASSEMBLY_JAKARTA.md + WIRING_JAKARTA.md updated (v3.0) | 2026-03-25 |
| — | Door sheets created (both sites) | 2026-03-25 |
| — | Exterior placards created (bilingual) | 2026-03-25 |
