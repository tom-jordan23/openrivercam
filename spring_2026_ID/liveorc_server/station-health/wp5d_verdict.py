#!/usr/bin/env python3
"""wp5d_verdict.py — answer "dying early or staying off?" from a wp5d.log grab.

WHY
    That question is the pivot for the whole ISS-FIELD-008/009/010 cluster: a
    station that boots every 30 minutes and dies young needs a different fix
    from one that mostly never powers on, and from outside the two are
    indistinguishable — both look like silence.

    /var/log/wp5d.log settles it, because every boot writes a "Startup reason"
    line whether or not anything ever reaches the server. The spacing of those
    lines through an outage IS the answer. This turns the grab into a verdict
    immediately, so the analysis is not being written while a wake window is
    open.

USAGE
    ./wp5d_verdict.py data/station-forensics/orc-sukabumi-wp5dlog-*.txt

Read-only. Takes a file; touches nothing.
"""
import re
import sys
from datetime import datetime
from pathlib import Path

LINE = re.compile(
    r"\[(?P<ts>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]\s+"
    r"(?P<kind>Startup|Shutdown)\s+reason:\s*(?P<reason>.+?)\s*$")

# The station runs UTC; the site is WIB (UTC+7). Report both, because every
# other artefact in this investigation is in WIB.
WIB_OFFSET_H = 7
CYCLE_MIN = 30.0


def parse(path):
    events = []
    for line in Path(path).read_text(errors="replace").splitlines():
        m = LINE.search(line.strip())
        if m:
            try:
                t = datetime.strptime(m.group("ts"), "%Y-%m-%d %H:%M:%S")
            except ValueError:
                continue
            events.append((t, m.group("kind"), m.group("reason")))
    return events


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    files = sorted(sys.argv[1:])
    events = []
    for f in files:
        events.extend(parse(f))
    if not events:
        sys.exit("no Startup/Shutdown reason lines found — is this a wp5d.log grab?")

    # Keep file order; the daemon writes a boot banner with the RTC's pre-sync
    # time, so sorting by timestamp reorders boots (see sensors_logger).
    ups = [(t, r) for t, k, r in events if k == "Startup"]
    downs = [(t, r) for t, k, r in events if k == "Shutdown"]
    print(f"{len(events)} reason lines: {len(ups)} startups, {len(downs)} shutdowns")

    reasons = {}
    for _t, _k, r in events:
        reasons[r] = reasons.get(r, 0) + 1
    print("\nreason strings seen (anything but 'Scheduled *' is new information):")
    for r, n in sorted(reasons.items(), key=lambda kv: -kv[1]):
        flag = "" if r.lower().startswith("scheduled") else "   <-- NOT previously observed"
        print(f"  {n:>4}x  {r}{flag}")

    print("\nlast 25 startups, with the gap since the previous one:")
    prev = None
    gaps = []
    for t, r in ups[-25:]:
        wib = t.replace(hour=t.hour)  # display helper below
        gap = "" if prev is None else f"{(t - prev).total_seconds()/60:8.1f} min"
        if prev is not None:
            gaps.append((t - prev).total_seconds() / 60)
        from datetime import timedelta
        print(f"  {t:%Y-%m-%d %H:%M:%S} UTC  = {t + timedelta(hours=WIB_OFFSET_H):%m-%d %H:%M} WIB  {gap}  {r}")
        prev = t

    # The discriminator is NOT "were there boots" — a healthy station boots every
    # 30 minutes too. Testing this against the 2026-08-27 capture, a period when
    # the station was working fine, produced "DYING EARLY" from 100% on-cadence
    # startups, which is exactly backwards. What matters is whether boots happened
    # DURING THE SILENCE: startups after the last row the server ever received.
    cutoff = None
    if "--since" in sys.argv:
        cutoff = datetime.strptime(sys.argv[sys.argv.index("--since") + 1],
                                   "%Y-%m-%d %H:%M:%S")
    else:
        try:
            sys.path.insert(0, str(Path(__file__).resolve().parent))
            import station_gaps as sg
            q = ("SELECT to_char(max(ts) AT TIME ZONE 'UTC','YYYY-MM-DD HH24:MI:SS') u "
                 "FROM sensor_readings WHERE station='sukabumi'")
            cutoff = datetime.strptime(
                sg.query(q, sg.DEFAULT_GRAFANA, sg.DEFAULT_CA)[1][0]["u"],
                "%Y-%m-%d %H:%M:%S")
        except Exception as e:
            print(f"\n  (could not fetch last server row: {e}; pass --since 'YYYY-MM-DD HH:MM:SS' UTC)")

    print(f"\n--- verdict ---")
    if cutoff is None:
        print("  no cutoff available — cannot separate boots-during-silence from normal ones.")
        return
    print(f"  last row the server ever received: {cutoff:%Y-%m-%d %H:%M:%S} UTC"
          f"  ({cutoff + timedelta(hours=WIB_OFFSET_H):%m-%d %H:%M} WIB)")

    # A grab whose log ends before the silence began cannot speak to it at all.
    # Without this guard such a file reports zero boots during the silence and
    # scores a confident "STAYING OFF" from evidence it does not contain — which
    # is what the 2026-08-27 capture did on the first run of this check.
    newest = max(t for t, r in ups)
    if newest < cutoff:
        print(f"  newest startup in this grab: {newest:%Y-%m-%d %H:%M:%S} UTC — BEFORE the cutoff.")
        print("\n  => NO EVIDENCE. This log predates the silence entirely; it says nothing")
        print("     about whether the station booted during it. Grab a fresher wp5d.log.")
        return

    after = [t for t, r in ups if t > cutoff]
    print(f"  startups recorded AFTER that moment: {len(after)}")
    for t in after[:12]:
        print(f"    {t:%Y-%m-%d %H:%M:%S} UTC = {t + timedelta(hours=WIB_OFFSET_H):%m-%d %H:%M} WIB")
    if len(after) > 12:
        print(f"    ... and {len(after)-12} more")

    if len(after) >= 3:
        span_h = (after[-1] - after[0]).total_seconds() / 3600
        rate = len(after) / span_h if span_h else 0
        print(f"\n  => DYING EARLY. {len(after)} boots over {span_h:.1f} h "
              f"({rate:.1f}/h against {60/CYCLE_MIN:.0f}/h scheduled) happened while the")
        print("     server received nothing. The Witty Pi is powering the Pi up; the boots")
        print("     are not surviving long enough to log or upload. The fault is after")
        print("     power-on, not in the power-on.")
    elif len(after) <= 1:
        print("\n  => STAYING OFF. Essentially no boots occurred during the silence, so")
        print("     the Witty Pi was not powering the Pi at all. The fault is upstream of")
        print("     the boot: the pack, the charge path, or the alarm itself.")
    else:
        print(f"\n  => INCONCLUSIVE: {len(after)} boots during the silence is too few to")
        print("     call. Report the timestamps, not a verdict.")


if __name__ == "__main__":
    main()
