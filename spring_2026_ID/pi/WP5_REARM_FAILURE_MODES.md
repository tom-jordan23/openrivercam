# Failure modes: orc-wp5-rearm and orc-wake-ceiling

Date: 2026-11-04. Scope: `pi/sukabumi/usr/local/bin/orc-wp5-rearm`, `orc-wake-ceiling`, their units and `orc-wp5-rearm.conf`.
Method: the scripts were run as copies with paths redirected and `wp5`, `logger`, `systemctl` and `sleep` replaced by stubs. Nothing touched the station.
Each finding is marked EXECUTED (observed in a run) or REASONED (read from the code, not yet run). Section 3 holds the truncation test results and corrects three REASONED findings from section 2 (R2, R5, R6).

## 1. Executed: normal and fault paths (23 scenarios)

Behaved as designed: not due, due, no stamp, stamp in the future, junk stamp, no armed startup, script not in use, wrong version, script absent, duplicate name, name that is a prefix of another, wrong confirmation text, missing "done", hung `wp5`, missing and empty config, item number above 9.

Defects found:

| # | Finding | Effect |
|---|---------|--------|
| E1 | Activation succeeds but the verify header has no RTC time, or does not show the script in use: no stamp is written | Re-arm on every boot, about 33 s each |
| E2 | `REARM_INTERVAL_H=abc`: `unbound variable` at line 102 | Script exits 1 with no log line; `wp5-rearm.last` is empty; re-arming stops until someone reads the journal |
| E3 | Only dots are escaped in `SCHEDULE_SCRIPT` before it is used as a regex | `prod+30.wpi` cannot match its own entry (fails safe: abort) |
| E4 | `grep -i` on the list | `PROD_30.WPI` is accepted for `prod_30.wpi` (benign) |

`orc-wake-ceiling`: both holds work; with neither present it calls `systemctl poweroff` (stubbed). Syntax check clean. `shellcheck` is not installed here.

## 2. Reasoned: invalid and truncated inputs

| # | Finding |
|---|---------|
| R1 | Stamp write result is not checked (`orc-wp5-rearm:146`). On a full or read-only disk the log says `OK: activated` while no valid stamp exists, so every boot re-arms. |
| R2 | A `wp5` crash (not a timeout) that cuts the pass-1 list right after `[n] prod_30.wpi` matches even if the real entry is `prod_30.wpi.bak`. The wrong number is then chosen. |
| R3 | Pass 2 does not re-read the list. A wrong choice is detected only by the `You have chosen` check after it is applied. |
| R4 | Stamp is written non-atomically without fsync. A shortened number reads as very old and causes one extra re-arm. |
| R5 | Empty `REARM_INTERVAL_H=` is an arithmetic syntax error. A negative value is always due. An unquoted value with a space leaves `SCHEDULE_SCRIPT` empty, which disables re-arming with exit 0. CRLF line endings make the name never match (loud abort every boot). |
| R6 | Dead RTC battery (year about 2000): negative age, re-arm every boot. |
| R7 | The 90 s timeout can kill `wp5` while the firmware regenerates the 4,096-entry list. Not testable with stubs. |

Not verified: how `/run/orc-maintenance-mode` is created and cleared (a stale marker would keep the Pi awake past the 12-minute ceiling).

## 3. Truncation and invalid-input test results (EXECUTED, 27 scenarios)

Harness: `pi/tests/rearm_harness/` (`drive.sh`, `extra.sh`; stub `wp5` can cut its output at a chosen string and set an exit status). The RTC is fixed at 2026-11-04 10:00:00 UTC.

Corrections to section 2:

- **R2 is not reproducible.** The script's `Version` and option-6 checks read the header that `wp5` prints after the list. Any output cut before the end of that header aborts before a number is chosen (T07 to T10, X1). A prefix-named script (`prod_30.wpi.bak`) is not matched (X2). A wrong pick would need `wp5` itself to print a shortened file name.
- **R5, empty `REARM_INTERVAL_H=`:** no syntax error. An empty variable evaluates to 0, so the script re-arms on every boot (T21).
- **R6, dead RTC (year 2000):** it re-armed once and wrote a consistent stamp (T23). Whether it repeats on every boot depends on whether the RTC keeps counting between boots; not tested.

Results by group:

| Group | Scenarios | Result |
|-------|-----------|--------|
| Header cut at RTC, startup or "in use" line; empty output | T01-T05, T25 | Treated as due, then aborts at the option-6 or version check. Nothing chosen. Safe. Note: my stub cuts every header read, so a one-off cut in pass 0 only (a spurious extra re-arm) was not isolated. |
| List cut mid-name, mid-number, or before the entries | T07-T10 | Abort, nothing chosen. Safe. |
| `wp5` exits non-zero (139) with a complete header | T06 | Exit status is not checked unless it is the timeout's 124. The run proceeded normally ("not due"). Harmless here, but a crash with plausible output is accepted. |
| Stamp empty, 4 digits, trailing text, two lines | T11-T14 | Each causes one extra re-arm and the stamp is rewritten. Safe. |
| Stamp directory not writable | T15 | **Confirmed R1.** Bash prints `Permission denied` to stdout, but the script logs `OK: activated`, exits 0, and the old stamp stays. Every boot re-arms. |
| Config empty file | T16 | Re-arming disabled, exit 0, logged. |
| Config unterminated quote | T18 | **New.** Re-arming silently disabled, exit 0. The log says "SCHEDULE_SCRIPT empty", which hides the cause. The syntax error appears only on stdout. |
| Config value with a space | T19 | Same silent disable (`script.wpi: command not found` on stdout only). |
| Config truncated to `prod_3` | T17 | Abort, nothing chosen. |
| Config CRLF | T20 | Abort on every boot (loud). |
| `REARM_INTERVAL_H` negative or empty | T21, T22 | Always due. |
| RTC year 2000 | T23 | Re-armed, stamp written. The log shows a negative age. |
| RTC impossible date | T24 | Activation happens, then abort with no stamp. Re-arm on every boot. This is E1 again. |

Net result for truncated or invalid inputs: no case chose the wrong script. The real defects are all about silent failure: R1 (false OK on a failed stamp write), the config cases that disable re-arming with exit 0, and E1/E2/T24 (repeat re-arms).

## 4. Not covered

- One-off truncation of only the pass-0 header.
- `wp5` killed by the 90 s timeout mid-activation (R7).
- Disk-full behaviour on a real filesystem (T15 used a permission error as a stand-in).
- `orc-wake-ceiling` with a stale `/run/orc-maintenance-mode`.

## 5. Fixes applied to orc-wp5-rearm (2026-11-04), re-run results

Re-run: `tests/rearm_harness/drive.sh` (T01-T25), `extra.sh` (X1, X2), `regress.sh` (R01-R15). All 42 scenarios behave as intended. Not deployed to the station.

| Finding | Change | Result |
|---------|--------|--------|
| R1 stamp write unchecked | Write `stamp.tmp`, `sync`, `mv`; on failure `die` with the reason | T15: rc 1, ABORT logged, no false OK |
| Config errors disable re-arming silently | Source the conf with stderr captured; any output is fatal and logged. A missing conf is logged as "not found" | T18, T19: rc 1 with the shell error in the log |
| E2/R5 bad `REARM_INTERVAL_H` | Must be a positive integer, otherwise log a WARN and use 23 | T21, T22, R13: warn, keep daily cadence |
| `wp5` exit status ignored | Non-zero other than the timeout's 124 is logged as a WARN, not fatal (wp5's normal exit status was never verified, so failing on it could break a healthy station) | T06: WARN logged, run continues |
| E3 regex characters in the script name | Literal, case-insensitive whole-name compare through awk | R10 matches `prod+30.wpi`; R11 `prod_3.wpi` no longer matches `prod_30.wpi` |

Left as is, by design:

- No RTC time in the verify header (E1, T24): the age cannot be measured, so no stamp is written and the next boot re-arms.
- CRLF in the conf (T20): already aborts loudly.
- `/proc` and `wp5` hang paths: unchanged.
