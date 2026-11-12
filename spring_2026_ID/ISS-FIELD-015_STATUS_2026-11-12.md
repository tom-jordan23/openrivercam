# ISS-FIELD-015 status summary — Sukabumi, 2026-11-12

Updated 2026-11-12 about 14:30 UTC, after the collection grab
(`data/station-forensics/orc-sukabumi-iss015-collect-20261112T140049Z.txt`). The full record is in
`ISSUE_LOG.md` (ISS-FIELD-015, dated updates). This file is the short version. Times are UTC.

## 1. Bottom line

- The station is cycling on the 30-minute grid and is reachable (12:30, 13:00, 13:30, 14:00 on 11-12).
- **The Witty Pi missed no scheduled startup** from the 11-11 press to 11-12 14:00: 32 of 32 slots on
  11-11 and 29 of 29 on 11-12, no gap over 35 minutes (`wp5d.log`). The "gaps" seen from outside were
  wakes with no network. The mobile data balance had expired; it has been topped up.
- **We lost data, and our own software did it.** The offline wakes ran on the Witty Pi RTC's January date.
  The sensor logger's log rotation deletes any CSV whose name date is older than 30 days. When NTP
  corrected the clock, the next tick deleted the January-dated files that held the offline sensor
  rows. They were present at 12:30 and gone by 14:00. They were never uploaded.
- The video files from the offline wakes are on the station under January-dated directories.
- The 10-21 stop (21 days with no startups) is a different event and is still unexplained.

## 2. What we know (measured)

| Fact | Evidence |
|---|---|
| Every scheduled slot fired from 11-11 08:00 to 11-12 14:00; one extra boot from a press at 11-12 03:41:50 | collect grab section 1 (`wp5d.log`) |
| The press-boot grab at 11-11 07:51:26 is the only other press in this window. Earlier presses: 07-03, 08-20/21, 10-09/10 | same |
| `wp5d.log` has no line at all between 10-21 14:32 and the 11-11 press. No non-routine event is logged near 10-21 | same |
| `wp5d` logged I2C register read-back retries at shutdown (`set Reg71 … read back 0x01`) on 06-19, 08-25 and 09-27, and register changes on `Reg14` and `Reg80`. None after 09-27 | same (non-routine events) |
| chrony could not reach any NTP source in the 11-12 12:00 wake; it stepped the clock by +304 days about 19–24 s after boot at 12:30, 13:00, 13:30 and 14:00 | collect grab section 6 |
| Without an NTP step the clock stays on the RTC, which reads January (month 01 for 11) | `wp5d.log`, press-boot capture |
| `rotate_logs` deletes `<label>_*.csv` whose name date is older than `LOG_ROTATE_DAYS` (30) relative to the current clock | `sensors_logger.py`, function `rotate_logs` |
| `sht40_2026-01-11.csv` (600 B) and `sht40_2026-01-12.csv` (1215 B) existed at 12:30; at 14:00 only one-row January files from the current wake remain | press-boot capture section 7 against collect grab section 2 |
| The first sensor tick can run before the clock step. The 14:00 wake wrote a January-dated row in each of 4 sensor files; the server lacks the first batch at 13:00 and one row at 12:30 | collect grab section 2; server row counts |
| The video directory holds 68,647 files, 42.2 GB. The oldest file is dated 2026-01-11 12:32 (directory `20260111`). The disk is 90% full | collect grab section 3 |
| The three 11-11 boot journals (07:51 press, 12:00, 17:00) are not in the journal. It holds 1053 boots, mostly July to mid-October, at the 200 MB limit | collect grab sections 4–5 |
| `journalctl --list-boots` labels are unreliable for these boots (the current boot is listed with a July date) | collect grab section 4 |
| 46 installed overlay files hashed; all equal the station's checkout (`eb7c7b0`). A deploy from `HEAD` would change one existing file (`sensors_logger.py`) and add two (`orc-clock-floor`, its unit) | collect grab section 7 against `git` |
| A pull would fast-forward 7 commits, all by Tom, 29 files, and install nothing | `git log eb7c7b0..origin/main` |

## 3. What we infer (not verified)

- The offline sensor rows from about 11-11 12:30 to 11-12 13:00 are gone. The files were deleted and no
  other copy is known. Which sensors lost rows is not listed, because the 12:30 capture cut its listing.
- The January-dated videos have January dates in LiveORC and in ORC-OS. Not checked.
- The video retention purge, if it works by date, may treat them as old. Not checked.

## 4. What we got wrong on the way

- We read "no server rows" and "Tailscale offline" as "no wake". They only show "no network". The
  station's own `wp5d.log` is the only proof of wakes.
- We read "latest row" as "last wake". Rows arrive late, in whole-file re-sends.
- We used boot selection by journal timestamps. These are unreliable here. Select offline wakes by
  `journalctl --since/--until` on their January timestamps instead.
- The recovery runner's "already cycling" guard used journal wall-clock times and forced an unneeded
  (successful) schedule activation.

## 5. What we do not know

1. Why there were no startups between 10-21 14:32 and the 11-11 press. The header showed an armed
   startup (`[21 15:00]`) at the start of the last wake. Nothing logged the cause, and without a spare
   Witty Pi it cannot be tested.
2. Why the RTC month reads 01 for November, and when it started. One possibility, unproven: the month
   register's tens digit reads as 0, so months 10, 11, 12 read as 00, 01, 02. Check on 12-01.
3. The exact failure mode of the link (SIM attached with no data, or not registered). The grab did not
   isolate an offline boot's modem lines.
4. Whether the January-dated videos are safe from the purge, and what the ORC-OS queue holds.
5. When the data balance expired.

## 6. Recommended next steps, in order

1. **Fix log rotation, then deploy it with the clock floor.** Rotation must not delete a file whose
   name date is implausible (before the deployment date), and ideally only deletes files that were
   uploaded. The clock floor stops new January files from being created. Both are station code changes
   that need Tom's approval. The overlay is clean, so the deploy changes only those files.
   Also review the rest of `deploy.sh` (packages, services) before a full run.
2. **Check the January-dated videos now.** Look in LiveORC for Jan 11–12 entries and find out whether
   the ORC-OS purge works by date. These are the only copies of the video from the offline wakes.
3. **Instrument.** Record the RTC date and the next startup in the Witty Pi sensor CSV on every tick, so
   a recurrence of the 10-21 stop is visible on the server.
4. **Prevent the next lapse.** Track the data balance expiry date; run the server staleness alert
   (`liveorc_server/station-health/db_watch.py`, alerts after 95 minutes without data).
5. **If a modem diagnosis is wanted,** capture an offline wake's modem lines using
   `journalctl --since/--until` on its January timestamps (the next outage).
6. **RTC month and the 10-21 stop.** Check the 12-01 prediction. Writing the correct date to the RTC
   needs a re-arm in the same wake, never alone (the active list is built on the wrong calendar).

## 7. Current state

- Nothing of mine is running against the station.
- Pushed to `origin/main` through `35e77c3`. Uncommitted: `iss015_collect_grab.sh` and this file.
  The `todo119_*` scripts and `pi/tests/rearm_harness/run/` are not mine.
- Scripts in `liveorc_server/station-health/`: `iss015_two_wakes.py`, `iss015_clock_grab.sh`,
  `iss015_postmortem_grab.sh`, `iss015_press_boot.sh` (four approved root writes, one shot),
  `iss015_collect_grab.sh` (read-only). All run through `todo119_wake_runner.py` as session-scoped tasks.
- Rules kept: nothing polls or connects to the station without a live Claude session; no `nohup`,
  `disown`, systemd or tmux-detached watchers; read-only grabs unless Tom approves a write.
- Not deployed: the clock floor and the logger columns.
