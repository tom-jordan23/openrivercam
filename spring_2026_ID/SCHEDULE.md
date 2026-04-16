# Deployment Schedule - Indonesia Spring 2026

**Created:** 2026-04-12
**Travel:** April 12-24, 2026
**Route:** Jakarta (7 days) then Sukabumi (4 days)
**Return flight:** April 24

---

## Phase 1: Jakarta (Days 1-7)

### Day 1 — Sun April 13: Arrival + Procurement

**Morning/Afternoon** (post-arrival)
- Clear customs (green channel, humanitarian papers)
- Get to PMI office / accommodation, unpack both stations
- Visual inspection of both stations — check nothing shifted in transit

**Late Afternoon**
- Purchase Telkomsel prepaid SIMs (kiosk or Grapari store)
- ~~Order LiFePO4 100Ah battery~~ → APC 900VA UPS procured locally
- Order grounding equipment if not visiting hardware store today (rod, cable, lugs)
- Start IMEI registration for both Quectel modems (https://imei.kemenperin.go.id/)

**Evening**
- Inventory check against BOM — confirm nothing missing or damaged
- Charge laptop, organize tools and documentation

---

### Day 2 — Mon April 14: Jakarta Station Bring-Up

**Morning**
- Bench-power Jakarta station on AC
- Verify full chain: AC → SDR-120-12 → 12V → DDR-60G-5 → 5V → Pi boots
- Verify relay → PoE injector → camera → RTSP stream
- Push Jakarta camera config via `camtool.py` (streaming, image, NTP)

**Afternoon**
- Fix ORC-OS daemon settings (allowed_dt → 3600, reboot_after → 86400)
- Run `deploy.sh jakarta`
- Set Witty Pi "Default state when powered" → ON (`wp5` → 11 → 1)
- Load `.wpi` schedule files via laptop USB
- Network IP migration (.101 → .100) if needed

**Evening**
- Verify end-to-end: `orc-capture` produces quality-gated video
- Start overnight soak test (capture every 15 min)
- Capture baseline batch: 10 videos at current config (1080p, 16 Mbps CBR)

---

### Day 3 — Tue April 15: Camera Quality Gate (CRITICAL)

This is the blocking decision for both sites. Must complete before Sukabumi.

**Morning**
- Review overnight soak — check for crashes, missed captures, storage growth
- Run `video_quality_test.py *.mp4 --compare` on baseline — record PIV pass rate
- Push Profile A (20 Mbps CBR 1080p), capture 10 videos, run comparison
- Push Profile B (20 Mbps CBR 720p), capture 10 videos, run comparison

**Afternoon**
- If A and B insufficient: test Profile C (local SD recording)
- If C needed: implement ISAPI capture modifications per `profile-c/CAPTURE_NOTES.md`
- **Decision gate: select streaming profile for both sites**
- Deploy chosen profile to Jakarta camera

**Evening**
- Start soak test on final profile (leave running overnight)
- ~~Battery may arrive~~ → UPS already procured

**Decision gate summary:**
- If any RTSP profile reliably delivers 15+ Mbps with acceptable ORC results → keep ANNKE C1200
- If no RTSP profile works but Profile C does → implement ISAPI capture method
- If no profile produces acceptable ORC results → plan camera replacement before Sukabumi

---

### Day 4 — Wed April 16: Sensor Wiring + Battery Integration

**Morning**
- Review overnight soak on final profile — confirm stability
- Jakarta sensor wiring (deferred from pre-travel):
  - Install cable glands on baseplate
  - Wire DS18B20 temperature probe (GPIO 4)
  - Wire WS2812B LED (GPIO 18)
  - Wire rain gauge external (SD16 bulkhead → RG-15)

**Afternoon**
- Test sensors:
  - Rain gauge: `minicom -D /dev/ttyAMA0 -b 9600`, send `R`, expect `Acc` response
  - DS18B20: `ls /sys/bus/w1/devices/28-*`, read temperature
  - SHT40: verify via `sudo orc-sensors`
  - LED: run `orc-led-test` for all status colors
- Verify CSV output for all sensors
- Simulate rain (pour water on RG-15 dome), confirm acc_mm increases

**Evening**
- Connect UPS: building AC → UPS input, station AC cord → UPS outlet
- Test UPS: unplug building AC, verify system stays running, replug
- Wire fans (if not yet done)
- Test fans — verify air circulation

---

### Day 5 — Thu April 17: Remote Access + Integration Testing

**Morning**
- Power button verification:
  - Brief press → power on from off
  - Brief press → clean shutdown from running
  - Long press (3s) → maintenance mode
  - Hold (10s) → force power off
- Test maintenance mode: WiFi hotspot up, SSH accessible
- Configure Pangolin remote access via ORC-OS web UI (or evaluate Tailscale)

**Afternoon**
- Test remote connectivity end-to-end (reach Pi from outside network)
- LED status daemon test — verify correct colors for each state
- Deploy maintenance mode: verify `orc-maintenance-check` returns production mode
- Test kill switch: toggle via GitHub Actions, verify orc-api stops
- Wire Mean Well DC OK signal to GPIO (TODO-011) if time permits

**Evening**
- Start 24hr+ final soak test with complete configuration
- All sensors, camera, remote access, battery backup running
- Power status MOTD script + SHT40 readout verification

---

### Day 6 — Fri April 18: Jakarta Site Installation

**Morning**
- Review soak test results — confirm 24hr+ stable operation
- Visit Jakarta site for survey (if not yet done):
  - Determine mounting surfaces, heights, cable run lengths
  - Plan camera angle for river cross-section coverage
  - Identify AC power source and grounding rod placement
- Purchase any remaining local hardware (mounting pole, brackets, conduit, concrete)

**Afternoon**
- Install grounding rod and run ground cable
- Mount enclosure at site (pole/wall mount)
- Mount camera on pole/bracket — aim at river cross-section
- Run Cat6 from camera to enclosure
- Crimp RJ45 connectors, test with cable tester
- Connect AC power, verify system boots at site

**Evening**
- Verify RTSP stream shows correct river view from final camera position
- Run `orc-capture` from installed position — verify quality gate passes
- Mount rain gauge (clear sky view, away from obstructions)
- Mount DS18B20 probe (water-adjacent if accessible, or air temp)
- Leave system running overnight at site

---

### Day 7 — Sat April 19: Jakarta Commissioning + Sukabumi Prep

**Morning**
- GCP survey at Jakarta site:
  - Set up RTK GPS
  - Survey 6+ ground control points visible in camera frame
  - Record coordinates, mark GCPs for future reference
  - Photograph each GCP with reference markers
- Camera calibration via ORC-OS web UI using GCPs
- Run ORC processing validation: calibration video + GCPs + cross section

**Afternoon**
- PMI staff training session at Jakarta site:
  - Walk through OPERATOR_GUIDE.md
  - Practice power button operations
  - Practice maintenance mode entry/exit
  - Show LED status meanings
  - Walk through TROUBLESHOOTING.md flowchart
  - Hand over laminated documentation + USB sticks

**Evening**
- Final Jakarta checks:
  - Remote access working from phone/laptop away from site
  - All sensors logging (verify CSV files growing)
  - Kill switch toggles correctly
  - System stable, capturing on schedule
- Pack tools and Sukabumi station for travel
- Confirm transport to Sukabumi (3-4 hr drive)

---

## Phase 2: Sukabumi (Days 8-11)

### Day 8 — Sun April 20: Travel + Sukabumi Bring-Up

**Morning**
- Travel Jakarta → Sukabumi (~3-4 hours by car)
- Bring: RTK gear, survey poles, GCP markers, Sukabumi station, tools

**Afternoon**
- Bench-power Sukabumi station at local workspace
- Install Witty Pi 5 (if not already done pre-travel) + CR2032 battery
- Verify 5V power delivery through Witty Pi stack
- Sync Witty Pi RTC to system clock
- Push final camera profile (chosen on Day 3) via `camtool.py`

**Evening**
- Run `deploy.sh sukabumi` — verify all checks pass
- Configure Witty Pi wake/sleep schedule:
  - Short test cycle first: 1 min on / 2 min off, 3 cycles — verify wake/sleep works
  - Then production cycle: 5 min on / 10 min off, 4+ cycles
- Verify camera boots within duty cycle window (~45-60s boot + capture + upload within 150s active phase)
- Verify relay power-cycles PoE injector correctly each wake

---

### Day 9 — Mon April 21: Sukabumi Sensor Testing + Site Prep

**Morning**
- Sensor field testing:
  - Rain gauge: UART serial test, verify `orc-sensors` reads it, simulate rain
  - DS18B20: verify 1-Wire detection, temperature reading, CSV output
  - SHT40: verify readings, compare against DS18B20 as sanity check
- **Critical test:** verify RG-15 state file persists across sleep/wake cycles
  - Simulate rain, let Pi sleep, wake, check delta is non-zero
- Power button verification (same sequence as Jakarta Day 5)

**Afternoon**
- Visit Sukabumi site:
  - Assess existing solar panel + battery condition (200W panel, 50Ah LiFePO4)
  - Verify panel output and battery health
  - Plan camera mounting position for river cross-section
  - Measure cable run lengths
  - Check existing mounting hardware / what needs replacement

**Evening**
- Prepare any site-specific modifications
- Configure Pangolin / Tailscale remote access for Sukabumi
- Leave station running overnight on production duty cycle
- Monitor remotely from phone — verify captures arriving on schedule

---

### Day 10 — Tue April 22: Sukabumi Site Installation

**Morning**
- Install Sukabumi station at site:
  - Connect to existing solar power system (200W panel → charge controller → 50Ah LiFePO4)
  - Mount enclosure (existing location or new position if needed)
  - Mount camera on pole — aim at river cross-section
  - Run Cat6 from camera to enclosure
  - Connect rain gauge, DS18B20 probe

**Afternoon**
- GCP survey at Sukabumi site:
  - Set up RTK GPS
  - Survey 6+ ground control points in camera frame
  - Record coordinates, photograph GCPs
- Camera calibration via ORC-OS web UI
- Run ORC processing validation: calibration video + GCPs + cross section
- Verify full duty cycle at site: wake → relay on → camera boot → capture → quality gate → upload → sleep

**Evening**
- Leave system running on production schedule overnight
- Monitor remotely — verify captures, sensor data, sleep/wake cycling
- Check power budget: monitor battery voltage across several cycles

---

### Day 11 — Wed April 23: Sukabumi Commissioning + Wrap-Up

**Morning**
- Review overnight results:
  - All captures passed quality gate?
  - Sensors logging correctly across sleep/wake?
  - Battery voltage stable? (target: <118 Wh/day consumption)
  - No missed wake cycles?
- Fix any issues found overnight
- If needed: re-run ORC processing to validate velocity/discharge output

**Afternoon**
- PMI staff / local partner training at Sukabumi:
  - Same walkthrough as Jakarta (operator guide, troubleshooting, button ops)
  - Hand over laminated docs + USB stick
  - Solar-specific items: don't add loads, check battery voltage, panel cleaning
- Final remote checks on both sites:
  - Jakarta still capturing and uploading? Sensors logging?
  - Sukabumi duty-cycling correctly?
  - Remote access working for both?

**Evening**
- Travel back to Jakarta (~3-4 hours) or stay overnight near Sukabumi
- Pack tools, remaining spares → PMI office spare parts tackle box
- Document any as-built deviations from plans

---

## Day 12 — Thu April 24: Departure

**Morning**
- Final remote check on both stations from laptop/phone
- Verify both stations captured successfully overnight
- Hand off remaining spares + tools to PMI office
- Update TODO.md with final status
- Note any follow-up items for remote support

**Afternoon/Evening**
- Depart Jakarta

---

## Schedule Summary

| Day | Date | Location | Focus |
|-----|------|----------|-------|
| 1 | Sun 4/13 | Jakarta | Arrival, procurement, SIMs |
| 2 | Mon 4/14 | Jakarta | Station bring-up, software config |
| 3 | Tue 4/15 | Jakarta | **Camera quality gate (blocking)** |
| 4 | Wed 4/16 | Jakarta | Sensor wiring, battery integration |
| 5 | Thu 4/17 | Jakarta | Remote access, integration testing |
| 6 | Fri 4/18 | Jakarta | Site installation |
| 7 | Sat 4/19 | Jakarta | GCP survey, commissioning, PMI training |
| 8 | Sun 4/20 | Travel → Sukabumi | Bench bring-up, Witty Pi schedule |
| 9 | Mon 4/21 | Sukabumi | Sensor testing, site survey |
| 10 | Tue 4/22 | Sukabumi | Site installation, GCP survey |
| 11 | Wed 4/23 | Sukabumi | Commissioning, training, wrap-up |
| 12 | Thu 4/24 | Jakarta | Final checks, departure |

---

## Risk and Float

**Critical path:** Day 3 (camera quality gate) must complete before Sukabumi deployment. If it takes longer, Days 4-5 have flexibility to absorb overflow.

**UPS:** APC 900VA procured locally. Standalone appliance — plug in and go, no integration work.

**Weather:** Tropical rain could delay site installation (Days 6, 10). Indoor work (sensor wiring, software) can fill rain days. Build in the expectation that one day may get rained out.

**Sukabumi is tight at 4 days.** If Jakarta runs long, Sukabumi buffer shrinks. Minimum Sukabumi path: bring-up (half day) → install + survey (1 day) → verify overnight → depart = 2.5 days.

**Day 11 evening travel** back to Jakarta is optional. If Sukabumi wraps early on Day 11, drive back same day. Otherwise, leave early morning Day 12.

---

## Key Commands Reference

```bash
# Camera config
python3 camtool.py push jakarta-cam1 --config profiles/profile-a/streaming_101.xml

# Quality testing
python3 video_quality_test.py *.mp4 --compare

# Deploy overlay
./deploy.sh jakarta
./deploy.sh sukabumi

# Sensor testing
minicom -D /dev/ttyAMA0 -b 9600          # Rain gauge serial
ls /sys/bus/w1/devices/28-*               # DS18B20 detection
sudo orc-sensors                          # All sensors
orc-led-test                              # LED status colors

# Witty Pi
wp5                                       # Main menu
# Option 6: select schedule
# Option 11 → 1: default state = ON

# Maintenance mode
sudo /usr/local/bin/orc-maintenance-check # Check mode

# Capture test
orc-capture --skip-relay --dry-run        # Quick RTSP test
```
