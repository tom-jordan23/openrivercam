#!/usr/bin/env python3
"""Tests for the RTC write guard in pi/deploy.sh (ISS-FIELD-015). No station, no root.

    python3 -I pi/tests/deploy_rtc_guard/test_rtc_guard.py

deploy.sh used to pipe `1` into wp5 (write the system clock to the Witty Pi RTC) unconditionally in fix
mode. On Sukabumi that would have moved the RTC by ~304 days and left the station with no future startup.
The guard (rtc_sync_fix, between the BEGIN/END rtc_write_guard markers) is extracted and run here against
stub wp5 / chronyc / reporting functions. A stub wp5 records every menu choice it is fed, so a WRITE (menu 1)
is distinguishable from a read (menu 14). The suite is then run against deliberately broken copies.
"""
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEPLOY = Path(os.environ.get("DEPLOY_TEST_SCRIPT") or HERE.parents[1] / "deploy.sh")
QUIET = bool(os.environ.get("DEPLOY_TEST_QUIET"))

CHRONY = {
    "real": "Reference ID    : CB591F0D (x)\nStratum         : 4\nLeap status     : Normal\n",
    "none": "Reference ID    : 00000000 ()\nStratum         : 0\nLeap status     : Not synchronised\n",
    "local": "Reference ID    : 7F7F0101 ()\nStratum         : 5\nLeap status     : Normal\n",
    "stratum10": "Reference ID    : CB591F0D (x)\nStratum         : 10\nLeap status     : Normal\n",
}


def extract(path):
    text = Path(path).read_text()
    m = re.search(r"# BEGIN rtc_write_guard\n(.*?)# END rtc_write_guard", text, re.S)
    if not m:
        raise SystemExit("rtc_write_guard markers not found in " + str(path))
    return m.group(1)


def scenario(guard_src, drift_s=None, chrony="real", rtc_text=None, force=False, limit=None):
    """Run rtc_sync_fix once. Returns (wrote, reports) where reports is a list of tag lines."""
    d = Path(tempfile.mkdtemp(prefix="rg_")); (d / "bin").mkdir()
    if rtc_text is None and drift_s is not None:
        rtc_text = (datetime.now(timezone.utc) - timedelta(seconds=drift_s)).strftime("%Y-%m-%d %H:%M:%S")
    (d / "bin/wp5").write_text(
        '#!/bin/bash\nin=$(cat)\necho "$in" | tr "\\n" " " >> "$T/wp5.in"; echo >> "$T/wp5.in"\n'
        'if [ -n "$RTC_TXT" ]; then echo "RTC Time: $RTC_TXT"; fi\n')
    (d / "bin/chronyc").write_text('#!/bin/bash\ncat "$T/chrony.txt"\n')
    for n in ("wp5", "chronyc"): (d / "bin" / n).chmod(0o755)
    (d / "chrony.txt").write_text(CHRONY[chrony])
    harness = (
        'set -euo pipefail\n'
        'pass()  { echo "PASS|$1"; }\nwarn()  { echo "WARN|$1"; }\nfixed() { echo "FIXD|$1"; }\n'
        + guard_src + '\nrc=0; rtc_sync_fix || rc=$?; echo "RC|$rc"\n')
    env = dict(os.environ, T=str(d), PATH=f"{d}/bin:{os.environ['PATH']}", RTC_TXT=rtc_text or "")
    env.pop("DEPLOY_FORCE_RTC_WRITE", None); env.pop("RTC_WRITE_MAX_DRIFT_S", None)
    if force: env["DEPLOY_FORCE_RTC_WRITE"] = "1"
    if limit is not None: env["RTC_WRITE_MAX_DRIFT_S"] = str(limit)
    r = subprocess.run(["bash", "-c", harness], env=env, capture_output=True, text=True, timeout=60)
    ins = (d / "wp5.in").read_text().splitlines() if (d / "wp5.in").exists() else []
    wrote = any(l.split()[:1] == ["1"] for l in ins)         # menu 1 = write system time to the RTC
    return wrote, r.stdout.strip().splitlines(), r.returncode


def run_suite(guard_src, report):
    def check(name, cond, detail=""):
        report.append((name, bool(cond), detail))

    w, out, rc = scenario(guard_src, drift_s=2)
    check("G1 RTC within 5 s: in sync, not written", not w and out[0].startswith("PASS|") and rc == 0, out)
    w, out, rc = scenario(guard_src, drift_s=120)
    check("G2 small drift + chrony synced: written, reported as fixed", w and out[0].startswith("FIXD|") and not any(l.startswith("WARN") for l in out), (w, out))
    w, out, rc = scenario(guard_src, drift_s=120, chrony="none")
    check("G3 small drift but system clock not confirmed by chrony: NOT written", not w and out[0].startswith("WARN|") and "chrony" in out[0], (w, out))
    w, out, rc = scenario(guard_src, drift_s=304 * 86400)
    check("G4 the Sukabumi case (RTC 304 days behind), chrony synced: NOT written, warns about the button press",
          not w and out[0].startswith("WARN|") and "button press" in out[0] and rc == 0, (w, out))
    w, out, rc = scenario(guard_src, drift_s=304 * 86400, force=True)
    check("G5 forced large correction with chrony synced: written, and a re-arm warning follows",
          w and any(l.startswith("FIXD|") for l in out) and any(l.startswith("WARN|") and "re-arm" in l for l in out), (w, out))
    w, out, rc = scenario(guard_src, drift_s=304 * 86400, force=True, chrony="none")
    check("G6 force never lifts the chrony requirement: NOT written", not w, (w, out))
    w, out, rc = scenario(guard_src, rtc_text="")
    check("G7 RTC unreadable: NOT written", not w and out[0].startswith("WARN|") and "could not read" in out[0], (w, out))
    w, out, rc = scenario(guard_src, drift_s=300, chrony="local")
    check("G8 chrony on its own local reference does not count as synced", not w, (w, out))
    w, out, rc = scenario(guard_src, drift_s=300, chrony="stratum10")
    check("G8b stratum 10 does not count as synced", not w, (w, out))
    w, out, rc = scenario(guard_src, drift_s=3600 - 5)
    check("G9 just inside the 3600 s limit: written", w, (w, out))
    w, out, rc = scenario(guard_src, drift_s=3600 + 60)
    check("G9b just past the limit: NOT written", not w, (w, out))
    w, out, rc = scenario(guard_src, drift_s=-10 * 86400)
    check("G10 RTC AHEAD of the clock by 10 days: NOT written and WARNED (not reported as in sync)", not w and out[0].startswith("WARN|"), (w, out))
    w, out, rc = scenario(guard_src, drift_s=-120)
    check("G10b RTC 2 minutes AHEAD of the clock: written (drift is absolute)", w and out[0].startswith("FIXD|"), (w, out))
    w, out, rc = scenario(guard_src, drift_s=600, limit=300)
    check("G11 RTC_WRITE_MAX_DRIFT_S is honoured", not w, (w, out))
    check("G12 every refusal still returns 0 (set -e must not abort deploy.sh)",
          all(scenario(guard_src, drift_s=x, chrony=c)[2] == 0 for x, c in ((304 * 86400, "real"), (120, "none"), (2, "real"))))


def static_checks(report):
    text = DEPLOY.read_text()
    inside = re.search(r"# BEGIN rtc_write_guard\n(.*?)# END rtc_write_guard", text, re.S).group(1)
    writes = [m.start() for m in re.finditer(r"printf '1\\n14\\n'", text)]
    report.append(("T1 exactly one `printf '1\\n14\\n' | wp5` in deploy.sh, and it is inside the guard",
                   len(writes) == 1 and text.count("printf '1\\n14\\n'") == inside.count("printf '1\\n14\\n'"), writes))
    report.append(("T2 the fix path calls rtc_sync_fix", "            rtc_sync_fix\n" in text, ""))


def main():
    report = []
    guard = extract(DEPLOY)
    run_suite(guard, report)
    static_checks(report)
    for name, ok, detail in report:
        print(("PASS " if ok else "FAIL ") + name + ("" if ok else f"   <-- {detail}"))
    bad = [n for n, ok, _ in report if not ok]
    print(f"\n{len(report) - len(bad)}/{len(report)} passed" + (f"; FAILED: {bad}" if bad else ""))
    if bad or os.environ.get("DEPLOY_TEST_SCRIPT"):
        sys.exit(1 if bad else 0)

    # ── broken copies of the guard: the suite must catch each ─────────
    mutants = {
        "drift limit removed": ('if [ "$drift" -gt "$RTC_WRITE_MAX_DRIFT_S" ] && [ "${DEPLOY_FORCE_RTC_WRITE:-0}" != "1" ]; then', 'if false; then'),
        "chrony check removed": ('if ! rtc_chrony_synced; then', 'if false; then'),
        "force also skips chrony": ('if ! rtc_chrony_synced; then', 'if [ "${DEPLOY_FORCE_RTC_WRITE:-0}" != "1" ] && ! rtc_chrony_synced; then'),
        "local reference counts as synced": ("if grep -qE '^Reference ID *: *(00000000|7F7F0101)' <<<\"$t\"; then return 1; fi", ""),
        "drift not absolute": ('drift=${drift#-}', ''),
        "already-in-sync shortcut removed": ('if [ "$drift" -le 5 ]; then', 'if false; then'),
        "unreadable RTC still writes": ('if [ -z "$rtc_txt" ] || [ "$rtc_epoch" -eq 0 ]; then', 'if false; then'),
    }
    survivors = []
    for name, (old, new) in mutants.items():
        if guard.count(old) != 1:                    # mutate the guard only; the same text exists in the check-only path
            print(f"BROKEN MUTANT ({guard.count(old)}x in the guard): {name}"); survivors.append(name); continue
        rep = []
        try:
            run_suite(guard.replace(old, new), rep)
        except Exception as e:                                   # a crash also counts as caught
            rep.append(("crash", False, str(e)))
        caught = any(not ok for _, ok, _ in rep)
        print(("CAUGHT   " if caught else "SURVIVED ") + name)
        if not caught: survivors.append(name)
    print(f"\n{len(mutants) - len(survivors)}/{len(mutants)} broken copies caught" + (f"; SURVIVORS: {survivors}" if survivors else ""))
    sys.exit(1 if survivors else 0)


if __name__ == "__main__":
    main()
