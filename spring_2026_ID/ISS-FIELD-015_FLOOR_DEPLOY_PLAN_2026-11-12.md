# Plan: apply the clock floor to Sukabumi safely

Written 2026-11-12. Related: `ISS-FIELD-015_STATUS_2026-11-12.md`,
`research/witty_pi_5_rtc_month_investigation_2026-11-12.md`, `ISSUE_LOG.md` (ISS-FIELD-015).
Nothing in this plan has been done on the station. Every station change below needs Tom's explicit approval.

## 1. What is being deployed

| Item | Where | State |
|---|---|---|
| `orc-clock-floor` (script) and `orc-clock-floor.service` | `pi/sukabumi/usr/local/bin/`, `pi/sukabumi/etc/systemd/system/` | Built. 38 tests pass; 12 deliberately broken copies are caught. Committed and pushed. Not deployed. |
| `clock_state` / `clock_adj_s` columns in `sensors_logger.py` | `pi/shared/usr/local/lib/orc-sensors/` | Built, inert until a sensor `CSV_HEADER` lists them. Committed and pushed. |
| Log-rotation fix in `sensors_logger.py` | same file | **Not written yet.** |
| Four code changes in section 3 | floor script and logger | **Not written yet.** |

## 2. How much damage this can do (blast radius)

- The floor never calls `wp5`, never touches I2C, the RTC or the schedule. It cannot stop the station from waking.
- It does two things: at boot it can move the system clock **forward**; at shutdown it writes one small file
  (`/var/lib/orc-clock-floor/floor`).
- Worst realistic failures, all bounded:
  - The unit hangs: `orc-api` and the sensors start up to 45 s late. The wake still ends normally.
  - The floor is wrong (too high): the clock starts too far ahead. chrony corrects it within about 25 s when
    the network is up. Bounded by the 2036 ceiling and the "advance at most 2 days when unsynced" rule.
  - The disk is full: the floor is not saved. Logged, harmless.
- Recovery never needs a button press, because the schedule is untouched.

## 3. Changes to make first (code, tested locally, no station contact)

1. **Limit the upload watermark's influence.** `restore` sets the clock to the later of the saved floor and the
   watermark file's mtime. A future-dated watermark would push the clock into the future. Accept the
   watermark only if it is within one day of the saved floor.
2. **Add `--dry-run`** to `restore` and `save`: print the decision, write nothing, never set the clock. Used to verify on
   the station.
3. **Repair the month instead of compressing time.** At restore the clock still holds the RTC copy: correct day
   and time of day, wrong month. Take year and month from the floor, and day and time from the RTC copy. Accept
   the result only if it falls between the floor and the floor plus 35 days; otherwise fall back to the floor.
   This gives offline rows true timestamps. Without it, each offline wake starts where the previous one ended,
   so a day offline is squeezed into about two hours of fake time. It reads no hardware.
4. **Fix log rotation.** Do not rotate while the clock is implausible (before the deployment date), and never
   delete files named with dates before the deployment (these are evidence of a wrong clock).
5. Extend the tests for items 1 to 4, then repeat the "broken copy" check for each new rule.

## 4. Do not use `deploy.sh`

In fix mode, `pi/deploy.sh` (line about 801) pipes `1` into `wp5`, which is "Write system time to RTC",
unconditionally. The October deploys ran it (`rearm_deploy_2026-10-12.sh` calls `deploy.sh sukabumi --yes`), and
that was harmless then because the clock was right. **Today it would write the corrected date (+304 days) into the
RTC. The active schedule list is built on the January calendar, so the Witty Pi would have no future startup and
the station would stop until a button press.** Also patch `deploy.sh` later so this write is not unconditional.

Install instead, from this workstation, with the exact tested files:

1. Copy the files to a staging directory on the station and compare `sha256sum` on both sides.
2. `python3 -m py_compile` on the new `sensors_logger.py`.
3. `systemd-analyze verify` on the new unit.
4. Back up the installed `sensors_logger.py` (current sha256 equals the repo version at `eb7c7b0`).
5. Install with `install` to a temporary name, then `mv` into place.
6. `systemctl daemon-reload`, then `systemctl enable orc-clock-floor.service`. **Do not start it mid-wake.**
7. Seed the floor once with `orc-clock-floor save` after chrony has synced.

The October scripts stop when the checkout has tracked changes. The station checkout has two deleted `.pyc`
files, so a git-based path would stop. Copying files avoids that and leaves the checkout alone.

## 5. Read-only checks on the station before installing

- `systemctl cat` for `orc-api.service`, `orc-sensors.timer`, `orc-sensors.service`, `chrony.service`,
  `wp5d.service`, and `systemd-analyze critical-chain orc-api.service`. Reason: a dependency cycle at boot makes
  systemd drop a unit. This is the failure we cannot catch locally.
- `python3 --version`; free disk (about 6 GB free of 58 GB, 90% used); upload watermark mtime.
- Current sha256 of the installed overlay files (done: all 46 equal the checkout `eb7c7b0`).

## 6. Rehearsal (there is no spare Witty Pi or Pi to test on)

- Run `synced()` against the real chrony output captured on 11-11 ("Reference ID CB591F0D … Stratum 4 … Leap status Normal").
- Optional: boot the unit files in a container or VM with systemd and stub `wp5d` and chrony. This checks ordering, the
  timeouts, and that the shutdown-time `save` runs.
- Independent code review of the final diff before anything is copied.

## 7. Go / no-go

Go only when all of these are true:

- [ ] Section 3 changes written, tests pass, broken-copy checks catch each new rule.
- [ ] Code review has no open findings.
- [ ] Section 5 reads show no ordering cycle and enough disk.
- [ ] Tom has approved the file copy, the install and the `enable`.
- [ ] A daytime (WIB) weekday wake; the install happens in the first 60 s of the wake, read-only checks in a different wake.
- [ ] Nothing else is changing at the same time (no firmware or software upgrade, no RTC rewrite).

## 8. Staged install (two wakes)

- **Wake A (read and stage):** section 5 reads; copy files to a staging directory; hash, `py_compile`, `systemd-analyze verify`. No installation.
- **Wake B (install):** backup, install, `daemon-reload`, `enable`, `save` once (after chrony syncs), `--dry-run` restore. Do not start the unit.

## 9. Verify after the first boot, then watch

Read-only, at the first wake after the install:

- `systemctl is-enabled` and `is-active orc-clock-floor`; journal lines tagged `orc-clock-floor`;
  `/var/lib/orc-clock-floor/floor` and `/run/orc-clock-floor/state`.
- That the sensor rows carry correct dates and the 13:00-type first-tick loss (rows stamped January) no longer occurs.
- Watch at least 48 hours (about 96 wakes) for any change in the cycle, boot time or upload behaviour.

## 10. Rollback

- `systemctl disable orc-clock-floor.service`; restore the backed-up `sensors_logger.py`; remove the unit and script.
  Takes effect at the next boot. No button press is needed.
- If the floor file is wrong: delete `/var/lib/orc-clock-floor/floor`.

## 11. Out of scope for this change

- Writing the RTC, re-arming the schedule, the firmware update, the software upgrade, fitting a CR2032.
- Fixing `deploy.sh`'s RTC write (do it in a separate commit before anyone runs it on Sukabumi).
- Recovering the deleted offline data (it no longer exists).

## 12. Decisions needed from Tom

1. Approve writing section 3 (four code changes plus tests).
2. Container rehearsal: yes or no.
3. Install timing: which wake, and whether the team should be on standby (not required, because the schedule is untouched).
