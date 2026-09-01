# Sukabumi duty cycle across the 2026-08-28 outage

**Issued:** 2026-09-01
**Site:** Sukabumi (pilot)
**Silent:** 2026-08-28 06:30 WIB → 2026-09-01 18:00 UTC (4.8 days)
**Evidence:** `/var/log/wp5d.log`, full file — 3.0 MB, 5,714 boots, 2026-04-07 → 2026-09-01
**Issue:** ISS-FIELD-011
**Published:** https://claude.ai/code/artifact/d31bab17-ef33-4603-94f8-dce5220562d5

Supporting data: `sukabumi_duty_cycle_daily.csv` (127 days).
Regenerate with `liveorc_server/station-health/wp5d_duty_cycle.py <wp5d.log>`.

---

## Summary

Sukabumi went silent for 4.8 days. It was running the whole time, on schedule,
at a normal duty cycle. The uplink failed because the Telkomsel prepaid account
ran out of money.

The first analysis of the returned data concluded the station had been awake
roughly 15 hours a day instead of 1.6, running nearly every cycle to the Witty
Pi's 25-minute backstop at about 9x its energy budget. That was inferred from
the spacing of sensor rows. The Witty Pi's own log measures the duty cycle
directly, and it was normal.

---

## What the log measures

Each cycle logs `Startup reason` (after the RTC write, so the clock is real) and
`Exit now.` at shutdown. The difference is the awake time.

| day | cycles | median wake | longest wake | awake/day |
|---|---|---|---|---|
| 08-21 | 47 | 2.03 min | 4.23 min | 98.7 min |
| 08-22 | 48 | 2.05 min | 4.37 min | 103.2 min |
| 08-23 | 48 | 2.74 min | 5.22 min | 131.2 min |
| 08-24 | 48 | 2.73 min | 5.18 min | 130.1 min |
| 08-25 | 45 | 2.92 min | **23.98 min** | 213.4 min |
| 08-26 | 48 | 2.23 min | 5.18 min | 123.6 min |
| 08-27 | 47 | 2.73 min | **24.27 min** | 171.8 min |
| **08-28** | 48 | 2.80 min | 5.15 min | **129.4 min** |
| **08-29** | 48 | 2.73 min | 2.95 min | **120.6 min** |
| **08-30** | 48 | 2.39 min | 2.95 min | **116.6 min** |
| **08-31** | 48 | 2.42 min | 2.92 min | **117.6 min** |

Bold days are the outage.

**48 scheduled boots a day, unbroken, before and through.** The Witty Pi powered
the Pi exactly on cadence the entire time.

**The duty cycle was not elevated.** Outage mean 121.1 min/day against a
preceding-week mean (08-21 → 08-27) of 138.9 — a ratio of **0.87x**. The station
was awake slightly *less* than in the week before it went quiet.

The baseline chosen is what produced the original error. Against the quieter
window of 08-10 → 08-13 (94–101 min/day) the outage reads as a mild 1.25x rise.
Against the week immediately preceding it, 0.87x. Daily awake time drifts
between roughly 95 and 215 minutes as a matter of course, and the outage days
land in the middle of that band. Neither baseline is anywhere near 9x.

**The maxima rule out the backstop claim outright.** Across the whole deployment
— 5,244 measured cycles over 127 days — the median wake is 1.95 min and only
**eight cycles have ever exceeded 20 minutes**. Two of those eight are in the
table above, on 08-25 and 08-27, both *before* the outage. During the outage the
longest single wake was 5.15 min, and the last three days never passed 2.95 min.

Startup reasons across the deployment: 5,645 Scheduled Startup, 40 Button Click,
17 Power Newly Connected, 12 Reboot.

---

## Claim ledger

| Status | Claim | Basis |
|---|---|---|
| Reported | The uplink failed because the Telkomsel prepaid account ran out of money | Tom, 2026-09-01. Consistent with every symptom; not independently verified from the station |
| Measured | 48 scheduled boots/day, unbroken, before and through | wp5d.log, 5,714 boots |
| Measured | Duty cycle during the outage was normal (0.87x the preceding week) | wp5d.log, 5,244 timed cycles |
| Measured | V-IN never fell below 12.149 V; reached 13.71 V | 679 samples in the flushed backlog |
| **Withdrawn** | "Awake ~15 h/day instead of 1.6, at ~9x its energy budget" | Inferred from sensor-row spacing. Measured: ~2 h/day |
| **Withdrawn** | "ORC-OS never completed its task, pinning the Pi to the backstop" | The task completed every cycle in under three minutes. No hang; the parallel to the ISS-FIELD-010 maintenance chain does not apply |
| **Withdrawn** | Night-onset pattern, dawn windows, three-missed-dawns, the site-visit case | All reasoned from absence of rows on a station that was working |
| **Withdrawn** | The recovery-voltage latch theory | 13.0 V is reached routinely. Every prior V-IN sample came from a 3-hour pre-dawn window |
| Weakened | "The pack is not the fault" | Still true for this event — V-IN held. But it rested on surviving 9x duty, and the real figure was 0.87x. The pack was never tested under load here |

---

## What changed

**Detection.** Nothing noticed for 4.8 days; the outage began as a single missed
upload. `db_watch.py` now alerts when the newest sensor row passes 95 minutes
old — three missed cycles — and again when uploads resume.

**Collection.** `pounce.py` grabbed only `tail -n 400` of wp5d.log, which
covered the last 20 hours of a 4.8-day outage. It now takes the whole file as a
second grab, gzipped, after the tail is safely down. On first use it re-grabbed
3 MB on every pounce — three identical copies in 90 seconds, 9 MB of prepaid LTE
for 3 MB of information. A 24-hour guard is now in place.

**Unattended operation stopped.** The watchers open SSH sessions to the station.
They now run only for the lifetime of an active session; `station-watch.service`
is retired and `enable-linger` stays off. A session left running since 08-28 was
found watching the station unattended for four days, and re-enabled the retired
unit 82 seconds after it was disabled. Accepted cost: wakes landing between
sessions are missed.

---

## Open

1. **Nothing watches the SIM balance.** The root cause, with no fix. A prepaid
   account that silently empties is a single point of failure for the station —
   not instrumented, not alerted, not on anyone's calendar. It will recur.
2. **No connectivity-loss handling in software.** Not the cause of the drain we
   thought we saw, but still absent.
3. **Power behaviour is measurable but unmeasured.** The flush delivered 679
   V-IN samples against 11 for the whole project before it, and only because a
   backlog forced them through.
4. **`station_gaps.py` rests on a false premise.** Absence of rows does not
   record downtime; that failed completely here. Anything built on it needs
   re-checking against the Witty Pi log.

---

## Method notes

Two traps in parsing wp5d.log, both of which produced clean-looking but false
tables before being caught:

- The daemon's `... daemon V5.0.0 started` line is written before the RTC is
  read back, so it carries a stale clock (2026-03-26 on this station). Cycles
  must be anchored on `Startup reason`.
- A cycle ends at `Exit now.`. Taking the last timestamped line before the next
  boot instead picks up the next boot's post-sync lines, and every cycle then
  measures exactly the 30-minute wake interval — healthy days included.

The file contains NUL bytes from unclean shutdowns and must be read as binary
and stripped.

Awake time is measured to daemon exit rather than to the power rail dropping, so
every figure is a slight underestimate — equally on both sides of the comparison
the conclusion rests on.
