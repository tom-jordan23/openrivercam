# Witty Pi 5: why the RTC month reads 01 for November

Investigation of ISS-FIELD-015, written 2026-11-12. Question from Tom: the Witty Pi RTC has the right day
and time of day but the wrong month (01 for 11). Is it plausible, and are we using the board wrongly?

**How to read this document.** "Read by me" means I read the text or code myself (the vendor manual via
`pdftotext`, or our repository). "Reported by fetcher" means a delegated web fetcher returned the quoted
code or text; I did not open the page myself, so treat it as a lead with a source, not as verified.

## 1. What we observed

| Observation | Source |
|---|---|
| 2026-10-21 14:30:15: `wp5d` copied the RTC to the system and the date was correct (`Wed Oct 21 … 2026`) | station `wp5d.log` (read by me) |
| 2026-11-11 07:52: header `RTC Time: 2026-01-11 07:52:11` against `SYS Time: 2026-11-11 07:52:12` | press-boot capture (read by me) |
| Every wake since then: the RTC copy reads `Jan 11`, `Jan 12`; day of month and time of day match real UTC | `wp5d.log` (read by me) |
| The Pi was off, with no `wp5d` activity, from 10-21 14:32 to 11-11 07:51 | `wp5d.log` (read by me) |
| The offset is exactly 10 months (Nov to Jan); weekday names printed by `date` match January | `wp5d.log` (read by me) |
| The daemon judged the RTC "valid" at the press boot | `wp5d.log` (read by me) |

## 2. What the vendor code does (reported by fetcher; sources in section 8)

- The RTC chip is an **Epson RX8025T-UB** (manual, read by me). The RP2350 firmware talks to it at I2C
  0x32; the Raspberry Pi sees it through "virtual registers" 80 to 86 (seconds … year) at address 0x51.
- **Month decoding is correct in every path found.** The Pi software (`wp5lib.c`, `get_rtc_time`) and the
  firmware (`rtc.c`, `rtc_get_time`) both decode with `bcd_to_dec(x) = (x >> 4) * 10 + (x & 0x0F)` and
  apply no mask. 0x10 decodes to 10, 0x11 to 11 and 0x12 to 12. These functions are identical in software
  v5.0.0 (the version on our station) and v5.3.1 (main). So a simple "tens digit masked on read" bug is
  **not supported** by the code, for these versions.
- The Pi software copies the RTC to the system only **once, when the daemon first connects to the board**
  (`wp5d.c`), through `sudo date -s "YYYY-MM-DD hh:mm:ss"` built from the decoded fields. It judges the RTC
  "valid" only by field ranges (`month 1..12`, `year > 2024`, and so on). It does not check the chip's
  voltage-low flag, the month length or the weekday.
- **Nothing in the vendor daemon ever writes network or NTP time to the RTC.** `wp5d` never calls the
  network sync. That function is the manual menu item 3 (it takes the time from the HTTP `Date` header of
  www.google.com, not NTP). Option 1 writes system time to the RTC. So with chrony running, the RTC is
  never disciplined, and any error in it persists until someone writes it.
- The firmware keeps its own log, `/log/WittyPi5.log`, on an emulated USB drive (manual, read by me).
  Lines are `[MM-DD HH:mm:ss.SSS] message`. It records alarm scheduling, "Scheduled startup is due",
  RTC/pulse-wake collisions and DST wakes. The manual says it holds the most complete low-level debug
  information, including when the Pi fails to start.
- Menu item "Administrate [3] Reset RTC" resets the RTC (manual, read by me). Our scripts never use it.

## 3. Known firmware and software fixes after our versions (reported by fetcher)

Our software is **5.0.0** (10 Jun 2025). Our firmware version is **unknown**: the 5.0.0 software does not
display it. The firmware releases page lists v1.0 to v1.7, newest v1.7 (19 Oct). Quoted fragments:

| Version | Fix (verbatim fragments) |
|---|---|
| v1.4 (29 May) | "the debug log timestamp conversion was using the POWMAN timer value directly"; "rtc_get_scheduled_time() did not correctly calculate the next future occurrence"; "could prevent startup alarms from being programmed when the configured day was smaller than the current day" |
| v1.5 (22 Jun) | "avoid internal I2C pointer race when accessing virtual registers" |
| v1.6 (31 Aug) | "configuration or log persistence could interrupt an active external I2C transaction" (with "incorrect register reads"); "The external I2C slave is safely paused during flash/filesystem operations" |
| v1.7 (19 Oct) | "Improved RTC Alarm Reliability"; "Fixed a race condition that could cause scheduled startup events to be missed when an RTC alarm occurred"; "Preserved pending RTC alarm flags during normal RTC initialization"; "Ensured pending RTC alarms are processed even when another wake-up source is triggered first"; "verified through 195 consecutive scheduled startup/shutdown cycles without any missed actions"; "…could cause the firmware to schedule an action whose time had already passed" |
| software 5.3.0 (31 Aug) | I2C reliability: tolerate temporary firmware unavailability, bounded retries, "Failed I2C reads are no longer interpreted as valid-looking measurement values" |

Two points follow. First, v1.7's own text says scheduled startups could be missed because of an RTC alarm
race. That is the kind of failure we saw on 10-21 (armed `[21 15:00]`, no wake). Second, our station has
never been updated, and we call `wp5` far more often than a typical installation: the sensors tick runs it
up to six times a minute, plus `wp5d` and the re-arm.

## 4. What we do that may be wrong (read by me)

1. **`deploy.sh` writes the Pi's clock into the RTC unconditionally** in fix mode
   (`pi/deploy.sh` line 801: `printf '1\n14\n' | timeout 30 wp5`). There is no drift check and no check that
   the system clock is right. **Running a full `deploy.sh` on the station now would write the corrected date
   (+304 days) into the RTC.** The active schedule list is built on the January calendar, so the Witty Pi
   would then have no future startup and the station would stop until a button press, unless the schedule is
   re-armed in the same wake. Do not run `deploy.sh` in fix mode on Sukabumi until this is changed.
2. **We never write NTP time back to the RTC.** The vendor's own daemon does not either. Any RTC error
   persists. Our `orc-clock-floor` fixes the system clock, not the RTC.
3. **We never updated the software or firmware** (5.0.0 against 5.3.1, firmware unknown against v1.7).
4. **Our `wp5` access pattern is heavy** relative to the vendor's examples (sensors tick, daemon, re-arm).
   The vendor fixed several I2C race and misread problems in firmware v1.5 and v1.6 and software 5.3.0.
5. We do not know whether a **CR2032 battery** is fitted. The manual says it is optional and that without
   it the board still works when external power is always connected. Our earlier research note said the
   board uses a supercapacitor and cannot take a battery; the manual contradicts that (CR2032 holder and
   an RTC battery header). That note is wrong on this point.

## 5. Hypotheses, ranked by how well they fit

**H1. The month register's tens-digit bit (bit 4) was lost after 10-21 and reads as 0.** Months 10, 11, 12
would then read 00, 01, 02. This fits everything: the code decodes correctly, so the register itself must
hold 0x01; October read correctly on 10-21, so the loss happened after; month 00 is "invalid" and month 01 is
"valid", which explains why the daemon accepted the RTC at the press (once the real month rolled over on
11-01). It also fits a single event around 10-21 that disturbed the RTC at the same moment the 15:00 alarm
failed to fire. **Prediction: on 2026-12-01 the RTC will read February.** Not proven.

**H2. A firmware fault in an RTC or alarm path (versions before v1.7), possibly with the I2C races** fixed in
v1.5 and v1.6. Fits the missed alarm better than the month. Unknown until the firmware version and log are read.

**H3. An RTC write by something on the Pi with a wrong month.** The only writers are `system_to_rtc` (menu
option 1, the daemon's "invalid RTC" branch, the network sync) and `deploy.sh`. None ran during the silence.
Unlikely.

**Ruled out for the versions examined:** a decode mask bug in the Pi software or the firmware read path.
**Not examined:** the firmware's virtual-register layer (`i2c.c`) and the DST code (`dst.c`); DST is off by
default (register 44, default 0) but its state on our unit has not been read.

## 6. Tests that would separate them

1. **Rewrite the RTC and read the month back.** If the month then reads 11, the chip's bit works and the
   loss was an event (H1 transient or H2). If it reads 01 again, the bit or the write path is faulty
   (hardware or firmware). This is also the RTC repair. It must be paired with a re-arm in the same wake
   (never alone), or the station stops. A forced re-arm already worked on 11-12 at 12:31.
2. **Read the firmware log** (`WittyPi5.log`) over USB-C, or by upgrading the software to 5.1.1 or later and
   using Administrate [7]. It may show what happened at 10-21 15:00 and how the firmware saw the RTC.
3. **Read the firmware version.** Software 5.0.0 does not show it. Software 5.3.1 prints
   `Model: … (firmware vX.Y)`. A direct I2C read of registers 1 and 2 is possible but should take the same
   file lock as `wp5lib` to avoid the I2C pointer race.
4. **Check the 12-01 prediction** (RTC reads February).
5. **Ask the team** whether a CR2032 is fitted, and have them read the label or markings on the board.

## 7. What I recommend

1. Treat the station's RTC as untrusted. Keep the clock floor. Never rely on the RTC month.
2. **Do not run `deploy.sh` in fix mode on Sukabumi.** Deploy the clock floor and the log-rotation fix by
   copying files and enabling the unit, or patch `deploy.sh` first so the RTC write is not unconditional.
3. Get the firmware version and the firmware log (USB-C by the team, or an approved software upgrade).
4. After that, decide on the RTC rewrite plus re-arm (test 1), and on updating the firmware to v1.7.
   Both are changes that need Tom's approval.
5. Fit a CR2032 if none is installed.

## 7b. Results of the station read (iss015_wp5_grab, 2026-11-12 14:30 UTC; read by me)

Capture: `data/station-forensics/orc-sukabumi-iss015-wp5-20261112T143048Z.txt`. Files and package metadata only;
no hardware access.

- **Installed build:** Debian package `wp5` version 1.00, files dated 2025-06-05 (software 5.0.0, the first
  public release). Never updated. `i2c-tools` 4.4 is installed. The firmware version is still unknown.
- **I2C lock file:** `/var/lock/wittypi5_i2c.lock` (both `wp5` and `wp5d` take it). A direct register read
  should take the same lock.
- **I2C trouble in `wp5d.log`:** 55 lines in 77,428. By date: 03-26 (9), 04-08 (2), 05-08 (2), 05-13 (29, the
  schedule activation day), 05-14 (1), 06-19 (5), 06-24 (1), 08-25 (4), 09-27 (2). **None after 09-27, none near
  10-21.** The shapes are write read-back retries (`set Reg71 … read back 0x01`, 44) and read-stability
  retries (`Reg14/Reg80 value changed`, 11). `wp5d.log` does not record the `wp5` command-line reads from
  the sensors, so I2C trouble seen by those reads is not visible here.
- **Voltage at the last wake before the silence (10-21 14:30):** `vin_v` 12.637, min 12.557, max 12.708;
  the whole day ranged 12.637 to 13.043. No brownout or dip in the data.
- **Nothing else on the box writes the RTC or the clock** (no cron, systemd unit, or script outside ours
  references `wp5`, `hwclock` or `date -s`).
- **The Pi 5's own RTC (`rpi-rtc`) has no battery:** the kernel sets the system clock to 1970 at boot, and
  systemd then raises it to the image floor of 2026-03-26 17:50. `config.txt` has
  `dtparam=rtc_bbat_vchg=3000000` (a charge setting for the Pi's own backup battery connector).
- The `wp5d` unit logs to `/var/log/wp5d.log`, not the journal, so the journal windows were empty.

**What this does and does not change.** It lowers the weight of an I2C-instability explanation for 10-21
(no trouble in the weeks before) and of a power event (voltage steady). It does not tell us the firmware
version or the raw month register. **Next read (needs Tom's go, because it is the first direct I2C access
outside the vendor tools):** with the vendor lock held, read virtual registers 1 and 2 (firmware version),
80 to 86 (raw RTC fields; register 85 is the month, to check whether it holds 0x01 or 0x11), 32 to 35 (startup
alarm), 44 (DST enable) and 94 (RTC flag register). Raw month 0x01 supports H1 (a lost bit in the chip
or the write path). Raw 0x11 with `wp5` showing 01 would contradict the code we read.

## 8. Sources

- Witty Pi 5 user manual (revision 1.01), text extracted from the PDF by me:
  https://www.uugear.com/doc/WittyPi5_UserManual.pdf
- Firmware releases and README (reported by fetcher):
  https://github.com/uugear/Witty-Pi-5-Firmware/releases ,
  https://github.com/uugear/Witty-Pi-5-Firmware
  (files cited: `src/rtc.c`, `src/rtc.h`, `src/i2c.h`, `src/util.h`, `src/dst_time.c`, `src/hibernate.c`,
  `src/log.c`, `src/file_admin.c`, `src/main.c`)
- Software repository (reported by fetcher):
  https://github.com/uugear/Witty-Pi-5-Software
  (files cited: `wp5lib.c`, `wp5lib.h`, `wp5.c`, `wp5d.c`; tags v5.0.0, v5.1.1, v5.2.0, v5.3.0, v5.3.1)
- A UUGear forum thread that ties the older daemon's RTC-to-system copy to boot (Witty Pi 4):
  https://www.uugear.com/forums/technial-support-discussion/ (search result, not opened by me)
- Our repository: `pi/deploy.sh` (line 801), `pi/sukabumi/usr/local/bin/orc-wp5-rearm`,
  `pi/shared/usr/local/lib/orc-sensors/sensors_logger.py` (read by me).
