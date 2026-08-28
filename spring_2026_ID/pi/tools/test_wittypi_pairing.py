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

# ── 5. Every emitted key must have a column, and vice versa ──────────
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
emitted = set(out.keys())
check("no emitted key is missing from CSV_HEADER", emitted <= cols,
      f"missing: {sorted(emitted - cols)}")
check("no CSV_HEADER column is never emitted", cols <= emitted,
      f"unemitted: {sorted(cols - emitted)}")

print()
if failures:
    print(f"FAILED ({len(failures)}): " + ", ".join(failures))
    sys.exit(1)
print("all checks passed")
