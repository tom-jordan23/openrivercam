#!/usr/bin/env python3
"""test_orccapture.py — prove read_orccapture() classifies a run correctly.

WHY THIS EXISTS
    ISS-FIELD-010. "No daytime video" is two different failures — midday the
    station finishes fast and produces nothing, evening it hangs — and they
    need opposite fixes. The driver's whole job is to tell them apart from
    orc-capture's journal and ship the verdict on the sensor upload.

    A misclassification here is worse than no data: it would send a site visit
    after the wrong component. So the classification is exercised against
    synthetic journal text off-station, the same way the wittypi pairing is.

USAGE
    ./test_orccapture.py           # exits 0 on pass, 1 on failure
"""
import importlib.util, os, sys, tempfile
from pathlib import Path

LOGGER = (Path(__file__).resolve().parents[1]
          / "shared/usr/local/lib/orc-sensors/sensors_logger.py")
spec = importlib.util.spec_from_file_location("sensors_logger", LOGGER)
sl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sl)

failures = []


def check(name, cond, detail=""):
    print(f"  {'PASS' if cond else 'FAIL'}  {name}" + (f" — {detail}" if detail else ""))
    if not cond:
        failures.append(name)


def classify(journal_text):
    """Run the driver against synthetic journal output."""
    sl._journal_tail = lambda unit, ident, lines, timeout: journal_text
    return sl.read_orccapture({})


# Journal timestamps must be recent: the driver suppresses capture_age_s when
# it exceeds 24 h, which is the guard against a stale RTC. A fixed date in the
# fixture would silently stop exercising that column.
from datetime import datetime, timedelta
_BASE = datetime.now() - timedelta(minutes=3)
def P(sec, _unused=None):
    t = (_BASE + timedelta(seconds=sec))
    return f"{t:%Y-%m-%dT%H:%M:%S} orc-sukabumi orc-capture[1]: {t:%Y-%m-%d %H:%M:%S} [orc-capture] "

print("\nclassification: one outcome per run")

ok = classify(P(1,1) + "Attempt 1/3: capturing as x.mp4\n"
              + P(9,9) + "Delivered: /home/pi/Videos/x.mp4\n"
              + P(10,10) + "Capture cycle complete\n")
check("a delivered run scores 1", ok["capture_result_code"] == 1.0, str(ok))
check("attempts are parsed", ok.get("capture_attempts") == 1.0, str(ok.get("capture_attempts")))

cam = classify(P(1,1) + "Waiting for camera at 192.168.50.139 (timeout: 90s)...\n"
               + P(91,91) + "ERROR: Camera unreachable — aborting\n")
check("camera unreachable scores 4 — power/PoE, not picture",
      cam["capture_result_code"] == 4.0, str(cam["capture_result_code"]))

gate = classify(P(1,1) + "Attempt 1/3: capturing as x.mp4\n"
                + P(8,8) + "ERROR:   FAIL: bitrate 4200 kbps (minimum 12000 kbps)\n"
                + P(8,8) + "ERROR:   Quality gate FAILED (1 check(s))\n")
check("a rejected picture scores 6", gate["capture_result_code"] == 6.0, str(gate["capture_result_code"]))
check("the failing gate is identified as bitrate",
      gate.get("capture_gate_code") == 5.0 and gate.get("capture_gate") == "bitrate",
      f"{gate.get('capture_gate_code')} / {gate.get('capture_gate')}")

# THE REGRESSION THAT MATTERS. A run that exhausts its retries contains the
# "Quality gate FAILED" lines that caused it. Taking the FIRST match would
# report a gate rejection and hide that nothing was delivered at all — the same
# first-vs-last error that produced a wrong downtime_s in the wp5d parser.
allf = classify(P(1,1) + "Attempt 1/3: capturing as x.mp4\n"
                + P(8,8) + "ERROR:   Quality gate FAILED (1 check(s))\n"
                + P(20,20) + "Attempt 2/3: capturing as x.mp4\n"
                + P(28,28) + "ERROR:   Quality gate FAILED (1 check(s))\n"
                + P(40,40) + "Attempt 3/3: capturing as x.mp4\n"
                + P(48,48) + "ERROR:   FAIL: file is empty or missing\n"
                + P(48,48) + "ERROR:   Quality gate FAILED (1 check(s))\n"
                + P(49,49) + "ERROR: All 3 attempts failed — no video delivered\n")
check("an exhausted run reports the FINAL outcome, not the first gate failure",
      allf["capture_result_code"] == 5.0, str(allf["capture_result_code"]))
check("it still records how many attempts were made",
      allf.get("capture_attempts") == 3.0, str(allf.get("capture_attempts")))
check("and which gate rejected the last one",
      allf.get("capture_gate") == "empty", str(allf.get("capture_gate")))

dis = classify(P(1,1) + "Capture disabled via ORC-OS, skipping\n")
check("CAPTURE_ENABLED=0 is distinguishable from a fault",
      dis["capture_result_code"] == 2.0, str(dis["capture_result_code"]))

mnt = classify(P(1,1) + "MAINTENANCE MODE — skipping capture cycle\n")
check("a maintenance skip is distinguishable from a fault",
      mnt["capture_result_code"] == 3.0, str(mnt["capture_result_code"]))

print("\ndegraded: the row must survive a missing or silent journal")
sl._journal_tail = lambda *a: None
un = sl.read_orccapture({})
check("unreadable journal yields -2, not a crash",
      un["capture_result_code"] == sl.CAPTURE_UNREADABLE, str(un))
check("unreadable journal emits no text columns", "capture_result" not in un)

nore = classify("2026-08-27T09:00:01 orc-sukabumi other[1]: [orc-capture] something unrelated\n")
check("journal with no recognised outcome yields -1, distinct from unreadable",
      nore["capture_result_code"] == sl.CAPTURE_ABSENT, str(nore))

print("\nwiring: driver keys match CSV_HEADER in orccapture.conf")
conf_path = (Path(__file__).resolve().parents[1] / "shared/etc/orc-sensors/orccapture.conf")
header = next(l.split("=", 1)[1].strip() for l in conf_path.read_text().splitlines()
              if l.startswith("CSV_HEADER="))
cols = set(header.split(",")) - {"timestamp"}
full = classify(P(1,1) + "Attempt 2/3: capturing as x.mp4\n"
                + P(8,8) + "ERROR:   FAIL: bitrate 4200 kbps (minimum 12000 kbps)\n"
                + P(8,8) + "ERROR:   Quality gate FAILED (1 check(s))\n")
check("no emitted key is missing from CSV_HEADER", set(full) <= cols,
      f"missing: {sorted(set(full) - cols)}")
check("no CSV_HEADER column is never emitted", cols <= set(full),
      f"unemitted: {sorted(cols - set(full))}")

print("\nend-to-end: append_csv -> the server's own sensor-ingest parser")
INGEST = (Path(__file__).resolve().parents[2] / "liveorc_server/sensor-ingest/app.py")
os.environ.setdefault("PG_DSN", "postgresql://unused/unused")
ispec = importlib.util.spec_from_file_location("ingest_app", INGEST)
ing = importlib.util.module_from_spec(ispec); ispec.loader.exec_module(ing)
tmp = tempfile.mkdtemp()
csv_path = sl.append_csv(tmp, "orccapture", header, full)
parsed = {m: v for _t, _s, _se, m, v in ing.parse_file(Path(csv_path), "sukabumi", "orccapture")}
check("numeric codes reach the database", parsed.get("capture_result_code") == 6.0
      and parsed.get("capture_gate_code") == 5.0, str(parsed))
check("text columns are dropped by the ingest, not misparsed",
      "capture_result" not in parsed and "capture_gate" not in parsed, str(sorted(parsed)))
mismatch = [k for k, v in parsed.items()
            if isinstance(full.get(k), (int, float)) and abs(full[k] - v) > 1e-9]
check("no column is shifted — every numeric metric round-trips", not mismatch, str(mismatch))

print()
if failures:
    print(f"FAILED ({len(failures)}): " + ", ".join(failures)); sys.exit(1)
print("all checks passed")
