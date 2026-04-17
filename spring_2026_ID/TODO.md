# TODO List - Indonesia Spring 2026 Deployment

**Last updated:** 2026-04-17
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
- [x] ~~Fix Jakarta J2 power button~~ — was working, false alarm
- [x] Build inside wiring harnesses — Sukabumi (rain gauge + DS18B20) ✓ isolation passed
- [x] Build inside wiring harnesses — Jakarta (rain gauge + DS18B20)
- [ ] Zip tie and strain relief all internal wiring (both stations)
- [x] Install Jakarta into enclosure
- [ ] Wire fans (Jakarta) — do this once components are in the box
- **Stretch:** Finish bottom plates (LED light windows, power button, external connectors)

**⚠ PIVOT: Witty Pi 5 HAT+ reinstated (both stations)**
Pi 5 RTC battery Molex connector broke on BOTH boards (traces tore). Switching to Witty Pi 5.
- [x] Install Witty Pi 5 on Jakarta (on hand) — 3-board stack: Pi 5 + Witty Pi 5 + G469
- [x] Verify G469 still seats properly on extended stack
- [x] Verify 5V power delivery through Witty Pi (DDR-60G-5 → Witty Pi → Pi) — V-IN 11.9V, V-OUT 5.3V, I-OUT ~1A
- [ ] Sukabumi Witty Pi ordered next-day from Adafruit — expected Tuesday April 7
- [ ] Buy CR2032 coin cell batteries for Witty Pi 5 (need 2 + at least 2 spares)

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
- [x] Run deploy.sh — Jakarta done 2026-04-07, Sukabumi done 2026-04-08 (109 PASS, 0 FAIL)
- [x] Remote maintenance mode — GitHub-based kill switch (orc-pmi-stations repo + Actions workflow + orc-maintenance-check service)
- [x] Install Witty Pi 5 software (wp5 v5.0.0 deb) — Jakarta done 2026-04-05
- [x] Sync Witty Pi 5 RTC to system clock — Jakarta done 2026-04-05
- [x] Disable orc-rpi5-power-management.service — Jakarta done 2026-04-05
- [ ] Set Witty Pi "Default state when powered" to ON for Jakarta (`wp5` → 11 → 1)
- [ ] Configure Witty Pi wake/sleep schedule for Sukabumi (`wp5` → 6)
- [ ] Test Witty Pi schedule: short cycle (1m on / 2m off, 3 cycles)
- [ ] Test Witty Pi schedule: production cycle (5m on / 10m off, 4+ cycles)
- [ ] ORC-OS web UI: configure daemon settings per station:
  - Jakarta (always-on): "Shutdown after task" OFF, "Reboot after" 86400s (24hr safety net)
  - Sukabumi (duty-cycle): "Shutdown after task" ON, "Reboot after" 3600s (1hr safety net)
  - Both: video_file_fmt `{%Y%m%dT%H%M%S}.mp4`, parse_dates_from_file ON, allowed_dt 3600 (NodeORC default)
- [x] Configure ORC-OS capture schedule (video filename template, daemon runner, ORC-OS timer service)
- [x] Camera ISAPI config via camtool.py — Sukabumi done 2026-04-08 (irLight, whiteLightBrightness=0)
- [x] orc-capture end-to-end test (relay → camera boot → RTSP → quality gate → ORC-OS pickup)
- [x] Implement rain gauge + DS18B20 sensor drivers (sensors_logger.py + config files)
- [ ] Rain gauge serial communication test — deferred to in-country
- [ ] DS18B20 temperature probe test — deferred to in-country
- [ ] SHT40 sensor verification — deferred to in-country
- [ ] LED status daemon test
- [ ] Pangolin remote access (pre-installed on RS image; configure via ORC-OS web UI)
- [ ] Power status MOTD script (undervoltage false positive)
  - [ ] MOTD: add SHT40 temperature + humidity readout
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
- [x] ~~Jakarta battery + charger~~ → APC 900VA UPS procured locally
- [ ] Jakarta mounting hardware (pending site survey)
- [ ] SIM cards (purchase in-country)
- [ ] Coordinate with PMI: RTK gear, ground control points, and survey poles last used at Sukabumi — need them at Jakarta site first

---

## In-Country

### Camera quality evaluation (Jakarta — do BEFORE Sukabumi)

Determine if the ANNKE C1200 at current/improved settings meets ORC's
quality requirements, or if a camera replacement is needed. Run all tests
at the Jakarta site where we have AC power and continuous operation.

**Phase 1: Baseline measurement**
- [ ] Capture 10 videos with current config (baseline: 1080p, 16 Mbps CBR)
- [ ] Run `video_quality_test.py *.mp4 --compare` — check PIV pass rate, bitrate, blockiness
- [ ] Record PIV combined pass rate as baseline to beat

**Phase 2: Profile A test (20 Mbps CBR, 1080p)**
- [ ] Push Profile A: `python3 camtool.py push jakarta-cam1 --config profiles/profile-a/streaming_101.xml`
- [ ] Capture 10 videos
- [ ] Run `video_quality_test.py *.mp4 --compare` against baseline captures
- [ ] Key question: does RTSP actually deliver higher bitrate, or is transport the bottleneck?
- [ ] Compare PIV pass rate to baseline

**Phase 3: Profile B test (20 Mbps CBR, 720p)**
- [ ] Push Profile B: `python3 camtool.py push jakarta-cam1 --config profiles/profile-b/streaming_101.xml`
- [ ] Update orc-capture.conf: EXPECTED_WIDTH=1280, EXPECTED_HEIGHT=720
- [ ] Capture 10 videos
- [ ] Run comparison — look for higher PIV pass rate and lower blockiness
- [ ] Key question: does 720p provide sufficient spatial coverage of the cross section?

**Phase 4: Profile C test (local SD recording — if A/B insufficient)**
- [ ] Only attempt if Profiles A and B do not reliably exceed 15 Mbps delivered
- [ ] Requires orc-capture modification for ISAPI recording (see profile-c/CAPTURE_NOTES.md)
- [ ] Capture 10 videos via local SD + copy
- [ ] Compare PIV pass rate and bitrate against RTSP profiles

**Phase 5: ORC processing validation (definitive test)**
- [ ] For each viable profile, create a separate ORC-OS video configuration
- [ ] Run calibration video + GCPs + cross section through ORC for each profile
- [ ] Compare ORC results: velocity confidence, PIV correlation pass rate, discharge estimates
- [ ] Select the profile that produces the most reliable ORC results

**Decision gate:**
- If any RTSP profile reliably delivers 15+ Mbps with acceptable ORC results → keep ANNKE C1200
- If no RTSP profile works but Profile C does → implement ISAPI capture method
- If no profile produces acceptable ORC results → plan camera replacement before Sukabumi deployment

### Network convention migration (.139/.101 → .100)
- [ ] Fix `pi/shared/etc/dnsmasq.d/maintenance.conf`: change dhcp-range to `.200,.254,24h`, remove Sukabumi-specific dhcp-host line (move to site-specific file)
- [ ] Create `pi/sukabumi/etc/dnsmasq.d/cameras.conf` with Sukabumi camera MAC → .100
- [ ] Update `pi/jakarta/etc/dnsmasq.d/cameras.conf` camera IP from .101 → .100
- [ ] Sukabumi: update `/etc/orc-capture.conf` CAMERA_IP to 192.168.50.100
- [ ] Jakarta: update `/etc/orc-capture.conf` CAMERA_IP to 192.168.50.100
- [ ] Update `pi/shared/etc/orc-capture.conf` default CAMERA_IP to 192.168.50.100
- [ ] Update `camera/cameras.json` IPs for both sites
- [ ] Both: update camera static IP (via camtool or camera web UI)
- [ ] Both: verify `ping 192.168.50.100` and `orc-capture --skip-relay --dry-run`
- [ ] Both: run `deploy.sh <site>` to normalize all configs

### Jakarta station software fixes
- [ ] Fix ORC-OS daemon setting: allowed_dt was set to 900, should be 3600 (NodeORC default)
- [ ] Fix ORC-OS daemon setting: reboot_after was set to 3600, should be 86400 (daily)
- [ ] Verify video_file_fmt is `{%Y%m%dT%H%M%S}.mp4` and parse_dates_from_file is ON

### Jakarta maintenance mode deployment
- [ ] Run `deploy.sh jakarta` to deploy orc-maintenance-check service (included in overlay)
- [ ] Verify: `sudo /usr/local/bin/orc-maintenance-check` returns production mode
- [ ] Test: toggle via GitHub Actions workflow, verify orc-api stops

### Jakarta Witty Pi schedule loading
- [ ] Load `.wpi` schedule files onto Jakarta's Witty Pi 5 via laptop USB during setup
  - Shut down the Pi, connect laptop USB to Witty Pi USB-C
  - Copy schedule files into `schedule/` on the emulated drive
  - Eject, disconnect, boot Pi, run `wp5` option 6 to select schedule (or option 11 → 1 for always-on)
  - **Do NOT connect Pi USB-A to Witty Pi USB-C** — causes reboot loop

### Power button verification (both stations)
- [ ] Confirm brief press powers on Pi from off state
- [ ] Confirm brief press initiates clean shutdown from running state
- [ ] Confirm long press (3s) enters maintenance mode
- [ ] Confirm hold (10s) forces power off
- [ ] Update OPERATOR_GUIDE.md Section 4 if behavior differs from documented

### Sensor field testing (both stations)

Run `deploy.sh <site>` first to deploy config files + w1-gpio overlay. Reboot required
for DS18B20 (1-Wire overlay).

**RG-15 rain gauge:**
- [ ] Verify UART wiring: `minicom -D /dev/ttyAMA0 -b 9600` — type `R`, expect `Acc ... mm` response
- [ ] Verify orc-sensors reads it: `sudo orc-sensors` — check journal for `rg15: acc_mm=... interval_mm=...`
- [ ] Verify CSV output: `ls /var/log/orc/sensors/rg15_*.csv`
- [ ] Verify state file: `cat /var/lib/orc-sensors/rg15_acc.txt`
- [ ] Simulate rain (pour water on dome) and verify acc_mm increases on next read
- [ ] On Sukabumi: verify state file persists across sleep/wake cycles (delta should be non-zero after rain)

**DS18B20 temperature probe:**
- [ ] Verify 1-Wire device detected: `ls /sys/bus/w1/devices/28-*`
- [ ] Verify raw reading: `cat /sys/bus/w1/devices/28-*/temperature` (millidegrees C)
- [ ] Verify orc-sensors reads it: `sudo orc-sensors` — check journal for `ds18b20: temp_c=...`
- [ ] Verify CSV output: `ls /var/log/orc/sensors/ds18b20_*.csv`
- [ ] Sanity check temperature against SHT40 reading (should be close)

**SHT40 (verification only — already deployed):**
- [ ] Verify orc-sensors reads it: `sudo orc-sensors` — check journal for `sht40: temp_c=... humidity_pct=...`
- [ ] Verify CSV output: `ls /var/log/orc/sensors/sht40_*.csv`

---

## Jakarta Software Status

**Jakarta is software-ready for deployment.** Remaining physical work
(rain gauge wiring, DS18B20 temp probe, cable glands on baseplate) will
be done in-country to avoid shipping damage. These are stretch goals —
Jakarta is AC-powered and always-on, so development can continue
post-deployment.

---

## Outstanding tasks (not yet scheduled)

- [x] Power status MOTD script — done (40-power-management)
- [x] deploy.sh script for OS image re-application — done
- [x] Jakarta-specific overlay files — done (NM connection, hosts, dnsmasq)
- [x] Move update-motd.d/ into etc/update-motd.d/ — done (consistent overlay paths)
- [x] Fix 30-camera-status to read camera IP from config instead of hardcoding — done (reads from orc-capture.conf)

---

## P0 — Blocking

### TODO-001: Implement rain gauge capture script for power-cycled operation (Sukabumi)

| Field | Value |
|-------|-------|
| **Status** | DONE (2026-04-09) — code complete, needs field testing |
| **Site** | Both |
| **Target** | In-country field testing |

**Implemented as:** `read_rg15()` driver in `sensors_logger.py` + `rg15.conf` config file.
Plugs into existing `orc-sensors.timer` (no new service needed).

On each reading (every 300s, or each wake cycle on Sukabumi):
1. Opens UART (`/dev/ttyAMA0`, 9600 baud)
2. Sends `R` command, parses `Acc` field from response
3. Reads previous accumulated value from `/var/lib/orc-sensors/rg15_acc.txt`
4. Computes delta (interval rainfall), handles gauge reset/rollover
5. Appends `timestamp,acc_mm,interval_mm` to daily CSV
6. Saves current Acc to state file for next reading

**Decision:** Implemented as sensor driver within existing orc-sensors framework,
not a standalone script or NodeORC plugin. Can be upstreamed later if useful.

**Needs field testing:** UART wiring, serial communication, Acc parsing, delta logic.

---

### TODO-002: Jakarta battery + charger selection

| Field | Value |
|-------|-------|
| **Status** | DONE (2026-04-16) |
| **Site** | Jakarta |

**Resolution:** Switched from 12V LiFePO4 battery + charger to a commercial
APC 900VA AC UPS (220V, line-interactive). Procured locally in Jakarta.
The UPS sits upstream of the Mean Well PSU on the AC side — no DC-side
battery integration, no charger, no battery box needed. Provides ~3-5
hours of backup power at 12-15W measured system load (derated for Jakarta
heat and battery aging). Simplifies wiring and eliminates the charger/BMS
compatibility questions.

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

**Sukabumi — completed 2026-04-08:**
- [x] Credentials set (stored in ~/.orc_deploy_sukabumi)
- [x] Image config pushed (irLight mode, whiteLightBrightness=0)
- [x] NTP config verified (matches desired state)
- [x] Streaming config verified (1920x1080, H.264, 12.5fps)
- [x] RTSP verified via `orc-capture --skip-relay --dry-run` (12.4 Mbps, 64 frames)
- [x] Full relay-cycled capture verified (13.4 Mbps, quality gate PASS)

Remaining (Jakarta):
- [ ] Push streaming config (1920x1080, H.264, 16 Mbps CBR, 12.5fps)
- [ ] Push image config (IR-only supplement light, auto IR cut filter)
- [ ] Push NTP config (Pi as NTP server)
- [ ] Verify RTSP stream accessible from Pi

---

## P1 — Important

### TODO-005: Correct stale power consumption figure in success criteria

| Field | Value |
|-------|-------|
| **Status** | DONE (2026-04-05) |
| **Site** | Sukabumi |

`BOM_Sukabumi.md` success criteria updated from <50 Wh/day to <120 Wh/day per ISS-001.

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

### TODO-008: Remote access setup

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Site** | Both |
| **Target** | Week 2 |

**Pangolin/Newt** is pre-installed on the Rainbow Sensing ORC-OS image. Configure
via ORC-OS web UI (no software installation needed). If using a different base
image, operators must provision their own remote access service.

**Tailscale** will be evaluated in-country as an alternative. May be a better fit
in some situations, but not usable in countries that disallow third-party VPN
services.

Remaining:
- Configure Pangolin via ORC-OS web UI (server URL, credentials)
- Test connectivity before sealing enclosures
- Evaluate Tailscale as alternative during in-country testing

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

### TODO-015: USB storage — disable UAS driver via cmdline.txt

| Field | Value |
|-------|-------|
| **Status** | DONE (2026-04-07 Jakarta, 2026-04-08 Sukabumi) |
| **Site** | Both |
| **Target** | Post-deployment (Jakarta), pre-deployment (Sukabumi) |

Samsung FIT Plus (0781:5583) uses UAS driver which crashes at boot,
causing USB enumeration storms that take down the modem. Fix is to add
`usb-storage.quirks=0781:5583:u` to `/boot/firmware/cmdline.txt`. This
forces the stable `usb-storage` (BOT) driver instead of UAS.

Both `uas` and `usb-storage` are kernel built-ins, so modprobe.d quirks
don't work — cmdline.txt is the only option.

**Jakarta — completed 2026-04-07:**
- [x] cmdline.txt quirk added: `usb-storage.quirks=0781:5583:u`
- [x] Verified: dmesg shows "UAS is ignored for this device, using usb-storage instead"
- [x] No USB enumeration storms on insert
- [x] fstab entry added (UUID, nofail), mounts at `/mnt/usb`
- [x] `/home/pi/Videos` symlinked to `/mnt/usb/incoming`
- [x] First capture verified landing on USB drive (20260407T163003.mp4)
- [x] deploy.sh updated: USB section handles fstab + symlink idempotently
- [x] Backout scripts: `~/uas-revert.sh` (cmdline), `~/usb-video-revert.sh` (fstab + symlink)

**Sukabumi — completed 2026-04-08:**
- [x] Verify `/boot/firmware` mounts (see TODO-016) — confirmed, mounts fine
- [x] Apply same cmdline.txt quirk — applied previous session, verified in cmdline
- [x] Insert USB drive, verify stable enumeration — SanDisk 3.2Gen1, no UAS errors
- [x] Format ext4, fstab UUID entry, mount at `/mnt/usb`
- [x] `/home/pi/Videos` symlinked to `/mnt/usb/incoming`
- [x] deploy.sh sukabumi --check: 105 PASS, 0 FAIL
- [x] First capture verified landing on USB drive (20260408T143741.mp4)

---

### TODO-016: Verify Sukabumi /boot/firmware matches Jakarta

| Field | Value |
|-------|-------|
| **Status** | DONE (2026-04-08) |
| **Site** | Sukabumi |

Both stations were flashed from the same image. Jakarta's `/boot/firmware`
mounts fine. Sukabumi had issues because we removed `90-qemu.rules` during
debugging (then restored it).

**Verified 2026-04-08:** `/boot/firmware` mounts, `cmdline.txt` accessible,
UAS quirk confirmed in `/proc/cmdline`. 90-qemu.rules present (deploy.sh confirms).

---

### TODO-017: GCP survey and camera calibration (both sites)

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Site** | Both |
| **Target** | In-country, after camera installation |

Survey 6+ ground control points at each site, calibrate cameras through
ORC-OS web UI. See ASSEMBLY_JAKARTA.md / ASSEMBLY_SUKABUMI.md
"Station Commissioning" section for checklist. Requires RTK GPS and
staff gauge.

---

### TODO-018: Rain gauge and temp probe wiring (Jakarta, in-country)

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Site** | Jakarta |
| **Target** | In-country |

Deferred to avoid cable gland damage during shipping. Stretch goal —
Jakarta is always-on so can be done post-deployment.

- [ ] Install cable glands on baseplate
- [ ] Wire rain gauge (SD16 bulkhead → RG-15)
- [ ] Wire DS18B20 external temp probe
- [ ] Wire WS2812B LED (GPIO 18)
- [ ] Test sensors via orc-sensors / orc-led-test

---

### TODO-019: Fix getty@tty1 login loop (hcwinsemius user)

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Site** | Sukabumi |
| **Priority** | P2 |

getty@tty1 is cycling every 5 seconds trying to auto-login user `hcwinsemius`,
which doesn't exist on this system. Causes constant authentication failures in
the journal (restart counter hits 25+ within minutes of boot). Likely a stale
autologin config from the ORC-OS image.

Check `/etc/systemd/system/getty@tty1.service.d/` or equivalent override for
the autologin user setting.

---

### TODO-020: Document unprovisioned-SIM diagnostic state

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Site** | Both |
| **Priority** | P1 |

Operator manual / troubleshooting guide should explain what an unprovisioned
SIM looks like in the field, so PMI staff don't chase host-side fixes for what
is a carrier-side activation problem.

**Symptom signature (observed on Sukabumi 2026-04-17):**
- `mmcli -m 0` reports `state: failed`, `failed reason: sim-missing`
- `mmcli -m 0 --enable` returns `Wrong state: modem in failed state`
- AT level (`/dev/ttyUSB2`) sees the SIM normally:
  - `AT+CPIN?` → `+CPIN: READY`
  - `AT+CCID` returns ICCID; `AT+CIMI` returns IMSI
  - `AT+CSQ` shows strong signal (e.g. `26,99` ≈ -61 dBm)
  - `AT+QENG="servingcell"` shows `LIMSRV` (limited service)
  - `AT+CREG?` / `AT+CGREG?` / `AT+CEREG?` all return `0,0`
  - `AT+COPS=0` fails with `+CME ERROR: 13` (SIM failure)
- QMI (`qmicli -d /dev/cdc-wdm0 --uim-get-card-status`) reports
  `Card state: present` but `Application state: illegal`

**Conclusion:** SIM is physically fine, RF path is fine. The carrier has not
activated the line — modem is being rejected during authentication. Only fix
is to activate the SIM with the carrier (Telkomsel for these deployments).
Once activated, ModemManager auto-registers (default `COPS=0`); no host
config changes needed.

**Recovery sequence after activation:**
1. `sudo systemctl restart ModemManager`
2. `mmcli -m 0 --enable`
3. If still stuck: `printf 'AT+CFUN=1,1\r\n' | sudo tee /dev/ttyUSB2` to fully
   reset the radio, then re-run step 1-2 once `/dev/ttyUSB2` reappears.

**Docs to update:**
- `docs/TROUBLESHOOTING.md` — add a "Cellular won't register" section with the
  symptom signature and the AT/QMI/MM probe commands above.
- Operator manual — add a one-paragraph "if the LED is red because of no
  cellular, here's how to tell whether to call the carrier or call us" guide
  for PMI staff.
- Cross-link from TODO-010 (SIM card strategy).

---

### TODO-021: Tailscale persistent login — deploy.sh integration

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Site** | Both |
| **Priority** | P1 |

Stations must never log out of Tailscale. Sukabumi was found logged out on
2026-04-17 (controlplane.tailscale.com fetch failures during SIM flapping
left `tailscaled` stuck in "Needs login" state). Re-authenticated manually
via browser.

**Admin-console side (done for Sukabumi 2026-04-17):**
- Machine → ⋯ → Disable key expiry. Do the same for Jakarta when it comes
  online. Without this, node key rotates every 180d and the device logs
  itself out.

**Pi side (to implement):**
Auth key already staged at `/home/pi/.tailscale_nodekey` on Sukabumi
(reusable, non-expiring, pre-authorized, tagged as appropriate). Need to
teach `deploy.sh` to use it so a fresh SD image or a wiped state dir
re-joins the tailnet unattended.

Add a `run_tailscale()` section to `spring_2026_ID/pi/deploy.sh` (call it
from `run_all_checks` next to `run_remote_access`). Checks:

1. `tailscale` and `tailscaled` installed (install from
   `https://tailscale.com/install.sh` if fixing — or add to apt section).
2. `tailscaled.service` enabled and active.
3. `tailscale status` reports logged-in (not "Logged out" / "Needs login").
4. Node appears up with an IP in `100.64.0.0/10`.

Fix path when logged out:
- Read auth key from `/home/pi/.tailscale_nodekey` (fail with clear message
  if missing — tell operator to create it from admin console → Settings →
  Keys, reusable + non-expiring + pre-auth).
- `sudo tailscale up --auth-key="$(cat ~/.tailscale_nodekey)" \
    --hostname=orc-${SITE} --ssh --accept-dns=false`
- Verify with `tailscale status` after.

Also have the fix pass `chmod 600 ~/.tailscale_nodekey` — it's currently
664 and that file is a bearer credential.

**Verification:**
- Fresh reflash → run `deploy.sh sukabumi` → node appears in admin console
  without any browser step.
- `sudo systemctl stop tailscaled && sudo rm /var/lib/tailscale/tailscaled.state
  && sudo systemctl start tailscaled` → `deploy.sh` re-auths it.

**Cross-link:** TODO-008 (remote access setup).

---

### TODO-022: Verify RG-15 rain gauge responds and is in polling mode (Sukabumi)

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Site** | Sukabumi |
| **Priority** | P1 |
| **Target** | Next site visit |

RG-15 has gone silent on `/dev/ttyAMA0` as of 2026-04-17 ~10:10 UTC.
Before that, every CSV entry read `Acc=0.0` across 43 samples (04:04–07:59
UTC). Root-cause recollection: gauge was configured in continuous ('C')
mode — pushing event lines to UART while the Pi was asleep, so `R`-based
polling never saw real data. Driver has since been rewritten (see below),
but the current hardware state needs a physical check.

**Driver changes already applied** (commits pending):
- `sensors_logger.py:read_rg15()` now sends `P\n` every read (idempotent
  force-polling), drains RX buffer, and parses `TotalAcc` (EEPROM-backed,
  survives power cycles) with exact-token match. Previous parser matched
  `Acc` first, which is the field that resets on power-cycle / `A`
  command — not what we want.
- `rg15.conf`: `CSV_HEADER` → `timestamp,totalacc_mm,interval_mm`,
  `STATE_FILE` → `rg15_totalacc.txt`. Stale `rg15_acc.txt` removed from
  `/var/lib/orc-sensors/`.

**Field check steps:**
1. Confirm RG-15 has 12V on TB1 (multimeter at gauge J2 VCC/GND).
2. Confirm UART TX wire (gauge → Pi GPIO 15/RXD) continuity.
3. `sudo systemctl stop orc-sensors.timer`
4. Passive listen for continuous mode:
   ```
   python3 -c "import serial,time; s=serial.Serial('/dev/ttyAMA0',9600,timeout=5); time.sleep(5); print(s.read(4096))"
   ```
   Any unsolicited bytes → gauge is in `C` mode.
5. Force polling + read:
   ```
   python3 -c "import serial,time; s=serial.Serial('/dev/ttyAMA0',9600,timeout=2); s.write(b'P\n'); time.sleep(0.5); s.reset_input_buffer(); s.write(b'R\n'); time.sleep(0.6); print(s.read(512))"
   ```
   Expect `Acc 0.xx mm, EventAcc ..., TotalAcc x.xx mm, RInt ...`.
6. `sudo systemctl start orc-sensors.timer` and tail
   `journalctl -u orc-sensors -f` — expect
   `rg15: totalacc_mm=..., interval_mm=0.0` on first read, non-zero
   intervals after rain.

**If gauge is still silent after power check**: power-cycle the gauge
(disconnect/reconnect TB1 feed — should emit a banner on boot). If still
silent, suspect TX wire or gauge firmware — swap to spare RG-15.

**Apply the same fix to Jakarta** once that gauge is wired (TODO-018).

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
| — | Sukabumi J2 power button: replaced dodgy Dupont connection with Wago 221 lever-nuts — tests passed | 2026-04-05 |
| — | Doc cleanup: RTC refs (ML-2020 → Witty Pi 5), Samsung FIT removal, power budget fix, J2 wiring methods | 2026-04-05 |
| TODO-015 | Jakarta: UAS disabled (cmdline.txt quirk), USB storage mounted, Videos symlinked, deploy.sh made idempotent | 2026-04-07 |
| TODO-015 | Sukabumi: USB formatted ext4, mounted, Videos symlinked, first capture on USB verified | 2026-04-08 |
| TODO-016 | Sukabumi: /boot/firmware mounts, cmdline.txt accessible, 90-qemu.rules present | 2026-04-08 |
| TODO-004 | Sukabumi: camera ISAPI config pushed (irLight, NTP, streaming verified), RTSP + relay-cycle capture PASS | 2026-04-08 |
| — | Sukabumi WS2812B LED wired, tested R/G/B + all status colors (orc-led-test) | 2026-04-01 |
| — | LED driver migrated from rpi-ws281x to Adafruit Blinka (Pi 5 PIO) — see ISS-007 | 2026-04-01 |
| — | GPIO_WIRING.md comprehensive update (Rev C) | 2026-03-20 |
| — | ASSEMBLY_SUKABUMI.md restructured (v3.2) | 2026-03-21 |
| — | ASSEMBLY_JAKARTA.md + WIRING_JAKARTA.md updated (v3.0) | 2026-03-25 |
| — | Door sheets created (both sites) | 2026-03-25 |
| — | Exterior placards created (bilingual) | 2026-03-25 |
