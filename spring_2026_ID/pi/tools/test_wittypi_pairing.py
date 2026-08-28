#!/usr/bin/env python3
"""test_wittypi_pairing.py — prove read_wittypi() pairs V and I from one sample.

WHY THIS EXISTS
    TODO-117. The first version of read_wittypi() aggregated voltage across
    samples and took current from the last one, so every uploaded row described
    a voltage swing and a current measured at different instants. That is fatal
    for the only question the sensor exists to answer — an effective source
    resistance, R = dV/dI — and it was invisible in the data until someone
    noticed two rows reporting the same 0.852 A with a 0.009 V and a 0.479 V
    spread.

    It was invisible because nothing exercised the driver off-station. The
    deploy script py_compiles the logger, which catches a syntax error and
    nothing else. This runs the actual sampling logic against synthetic wp5
    output, so the pairing property is checked before a deploy rather than
    inferred from uploaded rows a day later.

WHAT IT TOUCHES
    Nothing. It imports sensors_logger, replaces _wp5_sample with a stub, and
    calls read_wittypi() in-process. No wp5, no CSV, no network, no Pi.

USAGE
    ./test_wittypi_pairing.py          # exits 0 on pass, 1 on failure
"""

import importlib.util
import sys
from pathlib import Path

LOGGER = (Path(__file__).resolve().parents[1]
          / "shared/usr/local/lib/orc-sensors/sensors_logger.py")

spec = importlib.util.spec_from_file_location("sensors_logger", LOGGER)
sl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sl)

CONF = {"SAMPLES": "4", "SAMPLE_GAP_SEC": "0", "READ_TIMEOUT_SEC": "1"}

failures = []


def check(name, cond, detail=""):
    print(f"  {'PASS' if cond else 'FAIL'}  {name}" + (f" — {detail}" if detail else ""))
    if not cond:
        failures.append(name)


def stub(samples):
    """Replace _wp5_sample with a scripted sequence of (vin, vout, iout).

    Formatted as the real Witty Pi 5.0.0 status header, so the module's own
    regexes do the parsing. A stub that returned dicts directly would pass even
    if the patterns broke — and the patterns have broken before: an early
    version looked for "vin" and matched nothing, because the firmware prints
    "V-IN" with a hyphen.
    """
    seq = iter(samples)

    def fake(timeout_s):
        vin, vout, iout = next(seq)
        raw = f"  V-IN: {vin}V   V-OUT: {vout}V   I-OUT: {iout}A  \n"
        vals = {}
        for key, pat in sl._WP5_PATTERNS.items():
            m = pat.search(raw)
            if m:
                vals[key] = float(m.group(1))
        return vals, raw

    sl._wp5_sample = fake


# ── 1. The property the whole change exists for ──────────────────────
#
# A pack with a real source resistance: Vin falls as Iout rises. Here Vin drops
# 0.30 V as Iout climbs 0.60 A, so the paired extremes must recover exactly
# those two endpoints — not a mean paired with a last sample.
print("\npairing: Vin recorded in the same read as Iout")
stub([(12.90, 5.30, 0.20),
      (12.75, 5.30, 0.50),
      (12.60, 5.30, 0.80),
      (12.70, 5.30, 0.60)])
out = sl.read_wittypi(CONF)

check("iout_min_a is the lowest current seen", out["iout_min_a"] == 0.2, str(out["iout_min_a"]))
check("iout_max_a is the highest current seen", out["iout_max_a"] == 0.8, str(out["iout_max_a"]))
check("vin_at_imin_v comes from the 0.20 A read", out["vin_at_imin_v"] == 12.9,
      str(out["vin_at_imin_v"]))
check("vin_at_imax_v comes from the 0.80 A read", out["vin_at_imax_v"] == 12.6,
      str(out["vin_at_imax_v"]))

# The point of all of it: a slope that survives arithmetic.
r_out = (out["vin_at_imin_v"] - out["vin_at_imax_v"]) / (out["iout_max_a"] - out["iout_min_a"])
check("recovers the 0.500 ohm/A_out slope that was synthesised",
      abs(r_out - 0.5) < 1e-9, f"{r_out:.4f}")

# ── 2. The aggregates must now be over the same sample set ───────────
print("\nconsistency: vin_v and iout_a are means over the same samples")
check("vin_v is the mean, not the last", out["vin_v"] == round((12.90+12.75+12.60+12.70)/4, 3),
      str(out["vin_v"]))
check("iout_a is the mean, not the last", out["iout_a"] == round((0.2+0.5+0.8+0.6)/4, 3),
      str(out["iout_a"]))
check("samples_n counts every Vin read", out["samples_n"] == 4, str(out["samples_n"]))
check("samples_paired_n counts reads with both rails",
      out["samples_paired_n"] == 4, str(out["samples_paired_n"]))

# ── 3. The 2026-08-28 failure must not be reproducible ───────────────
#
# The real rows: 04:02:15 reported iout 0.852 A with a 0.009 V spread, and
# 04:30:27 reported the same 0.852 A with a 0.479 V spread. Same current, 53x
# the sag, because the sag and the current came from different instants. Replay
# a wake where the LAST sample is quiet and an EARLIER one carries a big sag:
# the old code reported the quiet current against the loud voltage span. The
# new code must attribute the sag to the current that was flowing during it.
print("\nregression: a sag must carry the current that caused it")
stub([(12.83, 5.24, 0.85),   # quiet
      (12.32, 5.33, 1.60),   # the sag — high current, low Vin
      (12.80, 5.34, 0.86),
      (12.84, 5.24, 0.85)])  # quiet again, and LAST
out2 = sl.read_wittypi(CONF)

check("iout_max_a catches the transient, not the last sample",
      out2["iout_max_a"] == 1.6, str(out2["iout_max_a"]))
check("vin_at_imax_v is the sagged voltage", out2["vin_at_imax_v"] == 12.32,
      str(out2["vin_at_imax_v"]))
check("vin_min_v and vin_at_imax_v agree on the sag",
      out2["vin_min_v"] == out2["vin_at_imax_v"],
      f"{out2['vin_min_v']} vs {out2['vin_at_imax_v']}")

# The defect stated as an assertion: a large Vin spread may never be reported
# alongside a load spread of zero. That combination is what made the uploaded
# rows unfittable.
spread_v = out2["vin_max_v"] - out2["vin_min_v"]
spread_i = out2["iout_max_a"] - out2["iout_min_a"]
check("a Vin spread is never reported against a zero load spread",
      not (spread_v > 0.05 and spread_i == 0), f"dV={spread_v:.3f} dI={spread_i:.3f}")

# ── 4. Degraded reads must stay honest ───────────────────────────────
print("\ndegraded: partial parses must not fake a paired point")

# Vin parses, current never does. The overnight curve still works; the row must
# say plainly that it cannot support a fit rather than omit the field.
def fake_vin_only(timeout_s):
    raw = "  V-IN: 12.70V  \n"
    m = sl._WP5_PATTERNS["vin_v"].search(raw)
    return {"vin_v": float(m.group(1))}, raw

sl._wp5_sample = fake_vin_only
out3 = sl.read_wittypi(CONF)
check("vin_v still reported when current is missing", out3["vin_v"] == 12.7, str(out3["vin_v"]))
check("samples_paired_n is 0, not absent", out3.get("samples_paired_n") == 0,
      repr(out3.get("samples_paired_n")))
check("no paired fields are invented", "iout_max_a" not in out3,
      str(sorted(out3)))

# Current appears in only one read. That read is the only legitimate pair, and
# it must not be blended with voltages from reads that had no current.
print("\ndegraded: one paired read out of several")
seq = [("  V-IN: 12.90V  \n", ),
       ("  V-IN: 12.60V   V-OUT: 5.30V   I-OUT: 0.90A  \n", ),
       ("  V-IN: 12.88V  \n", ),
       ("  V-IN: 12.91V  \n", )]
it = iter(seq)


def fake_mixed(timeout_s):
    raw = next(it)[0]
    vals = {}
    for key, pat in sl._WP5_PATTERNS.items():
        m = pat.search(raw)
        if m:
            vals[key] = float(m.group(1))
    return vals, raw


sl._wp5_sample = fake_mixed
out4 = sl.read_wittypi(CONF)
check("samples_n counts all four Vin reads", out4["samples_n"] == 4, str(out4["samples_n"]))
check("samples_paired_n counts only the one complete read",
      out4["samples_paired_n"] == 1, str(out4["samples_paired_n"]))
check("both paired endpoints come from that same read",
      out4["vin_at_imin_v"] == 12.6 and out4["vin_at_imax_v"] == 12.6,
      f"{out4['vin_at_imin_v']} / {out4['vin_at_imax_v']}")

# ── 5. Boot context from wp5d.log (ISS-FIELD-010) ────────────────────
#
# The power-on reason is the artefact that would have settled TODO-116 weeks
# ago and has never once been captured, because reading it needed an SSH window
# that Tailscale would not give us. It now rides the sensor upload instead. That
# makes it a passenger on the wittypi row, and passengers must not be able to
# hurt the host: the V/I telemetry has to survive anything this does.
print("\nboot context: /var/log/wp5d.log parsing")

import tempfile, os as _os
from datetime import datetime as _dt, timedelta as _td

def _fixture(body):
    fd, path = tempfile.mkstemp(suffix=".log")
    with _os.fdopen(fd, "w") as f:
        f.write(body)
    return path

_now = _dt.now()
_down_at = (_now - _td(seconds=3600)).strftime("%Y-%m-%d %H:%M:%S")
_up_at = (_now - _td(seconds=1800)).strftime("%Y-%m-%d %H:%M:%S")

# Shaped like the real 2026-08-27 capture: a daemon banner carrying the RTC's
# stale pre-sync time sits BETWEEN two real events, and "Scheduled Shutdown"
# occurs more than once. Both details are load-bearing — see the checks below.
FULL = f"""[2026-03-26 17:50:04] Witty Pi 5 daemon V5.0.0 started. PID = 767
[2026-03-26 17:50:05] Connected to Witty Pi 5
[2026-08-27 09:00:17] Startup reason: Scheduled Startup
[2026-08-27 12:54:59] Shutdown reason: Scheduled Shutdown
[2026-03-26 17:50:02] Witty Pi 5 daemon V5.0.0 started. PID = 736
[{_down_at}] Shutdown reason: Scheduled Shutdown
[{_up_at}] Startup reason: Scheduled Startup
"""
full_log = _fixture(FULL)
bc = sl.read_wp5d_boot_context(full_log)

check("power-on reason decodes to the scheduled code",
      bc["power_on_reason_code"] == 1.0, str(bc.get("power_on_reason_code")))
check("raw power-on reason text is preserved",
      bc.get("power_on_reason") == "Scheduled Startup", repr(bc.get("power_on_reason")))
check("previous shutdown reason decodes",
      bc["prev_shutdown_reason_code"] == 1.0, str(bc.get("prev_shutdown_reason_code")))

# The regression that matters. An earlier draft located the preceding shutdown
# with text.index(), which returns the FIRST occurrence of a string — and
# "Scheduled Shutdown" repeats every boot, so it always resolved to the oldest
# one. Here that would yield a downtime of many hours instead of 1800 s.
check("downtime_s spans the LAST shutdown before this boot, not the first",
      abs(bc.get("downtime_s", -1) - 1800) <= 2, str(bc.get("downtime_s")))
check("boot_age_s is measured from the most recent startup",
      abs(bc.get("boot_age_s", -1) - 1800) <= 5, str(bc.get("boot_age_s")))

# A missing log must cost nothing but the boot context itself.
gone = sl.read_wp5d_boot_context("/nonexistent/wp5d.log")
check("missing log yields the unreadable sentinel, not a crash",
      gone["power_on_reason_code"] == sl.REASON_UNREADABLE
      and gone["prev_shutdown_reason_code"] == sl.REASON_UNREADABLE,
      str(gone))
check("missing log emits no text columns", "power_on_reason" not in gone)

# A log with no reason lines is a different problem from an unreadable one and
# has to be distinguishable in the data.
empty = _fixture("[2026-08-27 09:00:17] Connected to Witty Pi 5\n")
bc_e = sl.read_wp5d_boot_context(empty)
check("log without reason lines yields the absent sentinel",
      bc_e["power_on_reason_code"] == sl.REASON_ABSENT, str(bc_e))

# The whole point of the 0 code: the only strings ever seen on this hardware are
# "Scheduled Startup"/"Scheduled Shutdown". Everything else in the table is a
# guess, so an unmatched string must degrade to "unrecognised, here is the text"
# rather than being silently forced into a neighbouring code.
odd = _fixture(f"[{_up_at}] Startup reason: Quantum Flux Anomaly\n")
bc_o = sl.read_wp5d_boot_context(odd)
check("unrecognised reason scores 0, not a wrong code",
      bc_o["power_on_reason_code"] == sl.REASON_UNRECOGNISED,
      str(bc_o["power_on_reason_code"]))
check("unrecognised reason still ships its raw text so it can be mapped later",
      bc_o.get("power_on_reason") == "Quantum Flux Anomaly", repr(bc_o.get("power_on_reason")))

# A comma would shift every later column and corrupt the voltage fields too.
comma = _fixture(f"[{_up_at}] Startup reason: Button, held 3s\n")
bc_c = sl.read_wp5d_boot_context(comma)
check("commas are stripped so the CSV cannot be shifted",
      "," not in bc_c.get("power_on_reason", ""), repr(bc_c.get("power_on_reason")))
check("a button reason still decodes to the button code",
      bc_c["power_on_reason_code"] == 2.0, str(bc_c["power_on_reason_code"]))

# "low voltage" must not be swallowed by the bare "voltage" entry.
lowv = _fixture(f"[{_down_at}] Shutdown reason: Low Voltage\n"
                f"[{_up_at}] Startup reason: Voltage Restored\n")
bc_l = sl.read_wp5d_boot_context(lowv)
check("low-voltage shutdown does not collide with voltage-restored",
      bc_l["prev_shutdown_reason_code"] == 7.0 and bc_l["power_on_reason_code"] == 3.0,
      f"{bc_l['prev_shutdown_reason_code']} / {bc_l['power_on_reason_code']}")

# Tail seek: a log larger than the read window must still parse, and must not
# be fooled by the partial line the seek lands in the middle of.
big = _fixture(("[2026-08-27 00:00:00] filler line to push past the tail window\n" * 3000)
               + f"[{_down_at}] Shutdown reason: Scheduled Shutdown\n"
               + f"[{_up_at}] Startup reason: Scheduled Startup\n")
bc_b = sl.read_wp5d_boot_context(big)
check("a log larger than the tail window still yields the latest boot",
      bc_b["power_on_reason_code"] == 1.0
      and abs(bc_b.get("downtime_s", -1) - 1800) <= 2, str(bc_b.get("downtime_s")))

# The host must survive the passenger. An unreadable log cannot cost the V/I row.
stub([(12.7, 5.3, 0.90), (12.4, 5.3, 1.40)])
out_broken = sl.read_wittypi({**CONF, "SAMPLES": "2", "WP5D_LOG": "/nonexistent/x.log"})
check("voltage telemetry survives an unreadable wp5d.log",
      out_broken.get("samples_paired_n") == 2 and "vin_v" in out_broken,
      str(out_broken.get("samples_paired_n")))


# ── 6. Every emitted key must have a column, and vice versa ──────────
#
# append_csv() builds rows from CSV_HEADER via values.get(col, ""), so a key the
# header does not list is silently dropped and a column the driver never emits
# silently becomes an empty cell. Neither raises. Check the two agree.
print("\nwiring: driver keys match CSV_HEADER in wittypi.conf")
conf_path = (Path(__file__).resolve().parents[1]
             / "shared/etc/orc-sensors/wittypi.conf")
header = next(l.split("=", 1)[1].strip()
              for l in conf_path.read_text().splitlines()
              if l.startswith("CSV_HEADER="))
cols = set(header.split(",")) - {"timestamp"}
# Use a run with a readable wp5d.log: on the sentinel path only the two *_code
# keys are emitted, and this check is about whether the header and the driver
# can agree at all, not about which path happened to run last.
stub([(12.7, 5.3, 0.90), (12.4, 5.3, 1.40)])
out_full = sl.read_wittypi({**CONF, "SAMPLES": "2", "WP5D_LOG": full_log})
emitted = set(out_full.keys())
check("no emitted key is missing from CSV_HEADER", emitted <= cols,
      f"missing: {sorted(emitted - cols)}")
check("no CSV_HEADER column is never emitted", cols <= emitted,
      f"unemitted: {sorted(cols - emitted)}")

# ── 7. End-to-end: the row the station writes is the row the server ingests ──
#
# The station and the server agree only by convention: append_csv() lays out
# columns from CSV_HEADER, and sensor-ingest/app.py reads them back by name and
# drops anything that will not float. Nothing enforces that contract, and the
# boot context is the first thing to put a TEXT column in a sensor CSV. If the
# layout is wrong the failure is silent — shifted columns still parse as floats
# and land in the database under the wrong metric name.
print("\nend-to-end: append_csv -> sensor-ingest parse_file")

import importlib.util as _ilu

_INGEST = (Path(__file__).resolve().parents[2]
           / "liveorc_server/sensor-ingest/app.py")
_spec = _ilu.spec_from_file_location("ingest_app", _INGEST)
_ingest = _ilu.module_from_spec(_spec)
# app.py reads PG_DSN at import. Nothing connects until run(), and parse_file is
# pure, so a placeholder is enough to get at the real parser rather than a copy
# of it — a reimplementation here would agree with itself and prove nothing.
_os.environ.setdefault("PG_DSN", "postgresql://unused/unused")
_spec.loader.exec_module(_ingest)

_tmpdir = tempfile.mkdtemp()
stub([(12.70, 5.30, 0.90), (12.40, 5.30, 1.40)])
row = sl.read_wittypi({**CONF, "SAMPLES": "2", "WP5D_LOG": full_log})
csv_path = sl.append_csv(_tmpdir, "wittypi", header, row)

parsed = _ingest.parse_file(Path(csv_path), "sukabumi", "wittypi")
by_metric = {m: v for _ts, _st, _se, m, v in parsed}

check("the text reason columns are dropped by the ingest, not misparsed",
      "power_on_reason" not in by_metric and "prev_shutdown_reason" not in by_metric,
      str(sorted(by_metric)))
check("power_on_reason_code survives to the database as a number",
      by_metric.get("power_on_reason_code") == 1.0, str(by_metric.get("power_on_reason_code")))
check("downtime_s survives to the database",
      abs(by_metric.get("downtime_s", -1) - 1800) <= 2, str(by_metric.get("downtime_s")))
check("the voltage metrics still land correctly alongside",
      by_metric.get("vin_v") == row["vin_v"] and by_metric.get("iout_a") == row["iout_a"],
      f"{by_metric.get('vin_v')} / {by_metric.get('iout_a')}")

# The alignment check with teeth: every numeric column must come back under its
# OWN name. A comma in a text field would shift later columns and this is what
# would catch it.
mismatched = [k for k, v in by_metric.items()
              if isinstance(row.get(k), (int, float)) and abs(row[k] - v) > 1e-9]
check("no column is shifted — every numeric metric round-trips under its own name",
      not mismatched, f"mismatched: {mismatched}")

# And prove the shift is actually detectable: a reason containing a comma must
# not be able to produce this outcome.
comma_log = _fixture(f"[{_down_at}] Shutdown reason: Scheduled Shutdown\n"
                     f"[{_up_at}] Startup reason: Button, held 3s\n")
stub([(12.70, 5.30, 0.90), (12.40, 5.30, 1.40)])
row_c = sl.read_wittypi({**CONF, "SAMPLES": "2", "WP5D_LOG": comma_log})
csv_c = sl.append_csv(tempfile.mkdtemp(), "wittypi", header, row_c)
parsed_c = {m: v for _t, _s, _se, m, v in
            _ingest.parse_file(Path(csv_c), "sukabumi", "wittypi")}
check("a comma-bearing reason still cannot shift the numeric columns",
      parsed_c.get("vin_v") == row_c["vin_v"]
      and parsed_c.get("downtime_s") == row_c["downtime_s"],
      f"{parsed_c.get('vin_v')} / {parsed_c.get('downtime_s')}")

print()
if failures:
    print(f"FAILED ({len(failures)}): " + ", ".join(failures))
    sys.exit(1)
print("all checks passed")
