#!/usr/bin/env python3
"""Tests for orc-clock-floor (ISS-FIELD-015). No station, no root, no real clock.

    python3 -I pi/tests/clock_floor/test_clock_floor.py

orc-clock-floor reads time, uptime, chrony and the set-clock command through
ORC_CF_* env overrides, so every scenario runs against a fake clock in a temp
dir. The uploader test runs the REAL pi/shared/usr/local/bin/orc-sensors-upload
with a stub curl, to prove the watermark coupling the design depends on.
"""
import importlib.util
import os
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

HERE = Path(__file__).resolve().parent
PI = HERE.parents[1]
FLOOR = Path(os.environ.get("ORC_CF_TEST_SCRIPT") or PI / "sukabumi/usr/local/bin/orc-clock-floor")   # mutants for self-checking
UPLOADER = PI / "shared/usr/local/bin/orc-sensors-upload"
LOGGER = PI / "shared/usr/local/lib/orc-sensors/sensors_logger.py"

T_MAR = 1774547400      # 2026-03-26 17:50:00  image time before wp5d steps the clock
T_JAN = 1768132816      # 2026-01-11 12:00:16  the Witty Pi RTC date seen on 11-11
T_NOV = 1794398400      # 2026-11-11 12:00:00  the real date
BUILD = 1793491200      # 2026-11-01
results = []


def check(name, cond, detail=""):
    results.append((name, bool(cond)))
    print(("PASS " if cond else "FAIL ") + name + ("" if cond else f"   <-- {detail}"))


class Rig:
    """A fake station clock plus stubs, in a temp dir."""

    def __init__(self, clock=T_MAR, step_at=None, step_to=None, uptime=3.0, chrony=None):
        self.d = Path(tempfile.mkdtemp(prefix="cf_"))
        (self.d / "bin").mkdir()
        self.clock, self.uptime = clock, uptime
        self.step_at, self.step_to = step_at, step_to
        self.write_chrony(chrony)
        self.state()
        self.stub("now", 'cat "$T/clock"')
        self.stub("set", 'echo "$1" >> "$T/set.log"; [ -e "$T/setfail" ] && exit 1; echo "${1#@}" > "$T/clock"')
        self.stub("chronyc", 'cat "$T/chrony.txt"')
        # sleep advances uptime and the clock by n seconds; applies a one-time wp5d-style step
        self.stub("sleep", textwrap.dedent('''
            n=${1:-1}
            u=$(cut -d. -f1 "$T/uptime"); c=$(cat "$T/clock")
            u=$((u+n)); c=$((c+n))
            if [ -e "$T/step_at" ] && [ ! -e "$T/stepped" ] && [ "$u" -ge "$(cat "$T/step_at")" ]; then
                c=$(cat "$T/step_to"); touch "$T/stepped"
            fi
            echo "$u.00 0.00" > "$T/uptime"; echo "$c" > "$T/clock"
        '''), path_dir=True)
        self.env = dict(
            os.environ, T=str(self.d), PATH=f"{self.d}/bin:{os.environ['PATH']}",
            ORC_CF_DIR=str(self.d / "lib"), ORC_CF_RUN=str(self.d / "run"),
            ORC_CF_UPLOAD_STATE=str(self.d / "upload.state"),
            ORC_CF_NOW_CMD=str(self.d / "bin/now"), ORC_CF_SET_CMD=str(self.d / "bin/set"),
            ORC_CF_CHRONYC=str(self.d / "bin/chronyc"), ORC_CF_UPTIME_FILE=str(self.d / "uptime"),
            ORC_CF_MAX_WAIT="8", ORC_CF_BUILD_FLOOR=str(BUILD),
        )
        if step_at is not None:
            (self.d / "step_at").write_text(str(step_at)); (self.d / "step_to").write_text(str(step_to))

    def stub(self, name, body, path_dir=False):
        p = self.d / "bin" / name
        p.write_text(f'#!/bin/bash\n{body}\n'); p.chmod(0o755)

    def state(self):
        (self.d / "clock").write_text(str(self.clock)); (self.d / "uptime").write_text(f"{self.uptime:.2f} 0.00")

    def write_chrony(self, kind):
        txt = {
            None: "Reference ID    : 00000000 ()\nStratum         : 0\nLeap status     : Not synchronised\n",
            "real": "Reference ID    : CB591F0D (ns5.datautama.net.id)\nStratum         : 4\nLeap status     : Normal\n",
            "local": "Reference ID    : 7F7F0101 ()\nStratum         : 10\nLeap status     : Normal\n",
            # each guard on its own: local reference at a plausible stratum, and a
            # non-local reference at stratum 10 (what "local stratum 10" produces)
            "local5": "Reference ID    : 7F7F0101 ()\nStratum         : 5\nLeap status     : Normal\n",
            "real10": "Reference ID    : CB591F0D (x)\nStratum         : 10\nLeap status     : Normal\n",
            "notnormal": "Reference ID    : CB591F0D (x)\nStratum         : 4\nLeap status     : Not synchronised\n",
        }[kind]
        (self.d / "chrony.txt").write_text(txt)

    def set_floor(self, value):
        (self.d / "lib").mkdir(exist_ok=True)
        (self.d / "lib/floor").write_text(str(value))

    def floor(self):
        p = self.d / "lib/floor"
        return p.read_text().strip() if p.exists() else None

    def clock_now(self): return int((self.d / "clock").read_text())
    def set_log(self): p = self.d / "set.log"; return p.read_text().split() if p.exists() else []
    def run(self, *a):
        r = subprocess.run([str(FLOOR), *a], env=self.env, capture_output=True, text=True, timeout=60)
        return r

    def restore_state(self):
        p = self.d / "run/state"
        return dict(l.split("=", 1) for l in p.read_text().split()) if p.exists() else {}


def main():
    # ── restore ───────────────────────────────────────────────────────
    r = Rig(clock=T_MAR, step_at=6, step_to=T_JAN)
    r.set_floor(T_NOV)
    p = r.run("restore")
    st = r.restore_state()
    check("R1 wp5d steps to Jan; restore waits for it, then sets the floor",
          p.returncode == 0 and r.clock_now() >= T_NOV and st.get("restored") == "1" and st.get("stepped") == "1",
          f"clock={r.clock_now()} state={st} err={p.stderr[-200:]}")
    check("R1b adj_s is the distance moved (Jan->Nov, 304 d minus the wait)",
          abs(int(st.get("adj_s", 0)) - (T_NOV - T_JAN - 0)) < 20, st.get("adj_s"))

    r = Rig(clock=T_NOV + 50, step_at=6, step_to=T_NOV + 56)
    r.set_floor(T_NOV)
    r.run("restore")
    check("R2 clock already ahead of the floor: nothing set", r.set_log() == [] and r.restore_state().get("restored") == "0")

    r = Rig(clock=T_MAR, step_at=6, step_to=T_JAN)
    p = r.run("restore")
    check("R3 no floor and no watermark: nothing set, exit 0", r.set_log() == [] and p.returncode == 0 and r.floor() is None)

    for label, val in [("not a number", "abc"), ("empty", ""), ("before BUILD_FLOOR (Jan 2026)", T_JAN),
                       ("after CEIL (2040)", 2208988800), ("negative", "-5"), ("float", "1794398400.5")]:
        r = Rig(clock=T_MAR, step_at=6, step_to=T_JAN)
        r.set_floor(val)
        p = r.run("restore")
        check(f"R4 invalid floor ({label}) is ignored", r.set_log() == [] and p.returncode == 0, r.set_log())

    r = Rig(clock=T_MAR, step_at=6, step_to=T_JAN)
    r.set_floor(T_NOV)
    st_file = r.d / "upload.state"; st_file.write_text(""); os.utime(st_file, (T_NOV + 900, T_NOV + 900))
    r.run("restore")
    check("R5 upload watermark newer than the floor wins (+1 s)", r.clock_now() >= T_NOV + 901 and T_NOV + 901 in map(int, [x.lstrip('@') for x in r.set_log()]), r.set_log())

    r = Rig(clock=T_MAR)                      # wp5d never steps
    r.set_floor(T_NOV)
    p = r.run("restore")
    check("R6 no wp5d step within MAX_WAIT: still checks the floor and sets it",
          r.restore_state().get("stepped") == "0" and r.clock_now() >= T_NOV and p.returncode == 0, r.restore_state())

    r = Rig(clock=T_MAR, step_at=6, step_to=T_JAN)
    r.set_floor(2082758400 - 10)              # inside CEIL, > 5 years ahead of the clock
    r.run("restore")
    check("R7 floor > 5 years ahead of the clock is refused", r.set_log() == [], r.set_log())

    r = Rig(clock=T_MAR, step_at=6, step_to=T_JAN)
    r.set_floor(T_NOV); (r.d / "setfail").write_text("x")
    p = r.run("restore")
    check("R8 set-clock failure: exit 0, restored=0", p.returncode == 0 and r.restore_state().get("restored") == "0")

    r = Rig(); r.env["ORC_CF_NOW_CMD"] = "/nonexistent"
    p = r.run("restore")
    check("R9 unreadable clock never fails the boot", p.returncode == 0)

    # ── save ──────────────────────────────────────────────────────────
    r = Rig(clock=T_NOV + 300, chrony="real"); r.set_floor(T_NOV)
    r.run("save")
    check("S1 synced: floor advances to the clock", r.floor() == str(T_NOV + 300), r.floor())

    r = Rig(clock=T_NOV, chrony="real"); r.set_floor(T_NOV + 10 * 86400)
    r.run("save")
    check("S2 synced: a too-high floor is LOWERED to trusted time", r.floor() == str(T_NOV), r.floor())

    r = Rig(clock=T_NOV + 150, chrony="local"); r.set_floor(T_NOV)
    r.run("save")
    check("S3 'local stratum 10' is NOT synced; advance within bound still allowed", r.floor() == str(T_NOV + 150), r.floor())
    r = Rig(clock=T_NOV - 100, chrony="local"); r.set_floor(T_NOV)
    r.run("save")
    check("S3b unsynced + clock behind floor: floor never lowered", r.floor() == str(T_NOV), r.floor())
    r = Rig(clock=T_NOV + 3 * 86400, chrony="local"); r.set_floor(T_NOV)
    r.run("save")
    check("S3c unsynced + clock > 2 days ahead: not trusted, floor unchanged", r.floor() == str(T_NOV), r.floor())
    for kind, why in (("local5", "local reference even at stratum 5"), ("real10", "stratum 10 (the local-stratum value)"),
                      ("notnormal", "Leap status not Normal")):
        r = Rig(clock=T_NOV - 100, chrony=kind); r.set_floor(T_NOV)
        r.run("save")
        check(f"S3d unsynced by itself ({why}): a behind-floor clock never lowers the floor",
              r.floor() == str(T_NOV), r.floor())
    r = Rig(clock=T_NOV, chrony=None)
    r.run("save")
    check("S4 unsynced and no floor yet: nothing saved", r.floor() is None, r.floor())
    r = Rig(clock=T_JAN, chrony="real"); r.set_floor(T_NOV)
    r.run("save")
    check("S5 even 'synced', a clock before BUILD_FLOOR is never saved", r.floor() == str(T_NOV), r.floor())
    r = Rig(clock=T_NOV, chrony="real")
    r.run("save")
    check("S6 first ever save works when synced and no floor exists", r.floor() == str(T_NOV), r.floor())
    check("S6b save leaves no temp files behind", [p.name for p in (r.d / "lib").iterdir()] == ["floor"], list((r.d / "lib").iterdir()))

    # ── two no-data wakes: timestamps must strictly increase ──────────
    rig = Rig(clock=T_MAR, step_at=6, step_to=T_JAN)
    rig.set_floor(T_NOV)                         # last synced wake ended at T_NOV
    rows = []
    for wake in (1, 2, 3):
        rig.clock, rig.uptime = T_MAR, 3.0; rig.state()
        for f in ("stepped",): (rig.d / f).unlink(missing_ok=True)
        rig.write_chrony(None)                   # no data: chrony never syncs
        rig.run("restore")
        first = rig.clock_now() + 25             # first sensor row ~25 s later
        rig.clock = rig.clock_now() + 150; rig.state()   # the wake runs 150 s
        rig.run("save")
        rows.append((first, rig.clock_now()))
    increasing = all(rows[i][0] > rows[i - 1][1] - 1 for i in range(1, len(rows)))
    check("W 3 no-data wakes: each wake's first row is after the previous wake's last time",
          increasing and all(r[0] >= T_NOV for r in rows), rows)
    check("W floor advanced across the no-data wakes", int(rig.floor()) > T_NOV, rig.floor())

    # ── the real uploader and its mtime watermark ─────────────────────
    d = Path(tempfile.mkdtemp(prefix="up_"))
    logs = d / "logs"; logs.mkdir()
    (d / "bin").mkdir()
    (d / "bin/curl").write_text('#!/bin/bash\nfor a; do last="$a"; done; echo "${last##*/}" >> "$UPLOG"; exit 0\n')
    (d / "bin/logger").write_text('#!/bin/bash\nexit 0\n')
    for n in ("curl", "logger"): (d / "bin" / n).chmod(0o755)
    (d / "ca.pem").write_text("x")
    conf = d / "up.conf"
    conf.write_text(f'ENABLED=1\nUPLOAD_URL=https://x/sensors/upload\nLOG_DIR={logs}\nSTATE_FILE={d}/state\nCACERT={d}/ca.pem\n')
    env = dict(os.environ, PATH=f"{d}/bin:{os.environ['PATH']}", ORC_SENSORS_UPLOAD_CONF=str(conf),
               STATION="sukabumi", UPLOAD_TOKEN="t", UPLOG=str(d / "uploaded.txt"),
               RETRY_COUNT="0", RETRY_DELAY="0")

    def mk(name, mtime):
        p = logs / name; p.write_text("timestamp,x\n"); os.utime(p, (mtime, mtime)); return p

    state = d / "state"; state.write_text(""); os.utime(state, (T_NOV, T_NOV))     # last upload at 12:00
    mk("sht40_2026-01-11.csv", T_JAN)          # written under the January clock
    mk("sht40_2026-11-11.csv", T_NOV + 40)     # written after chrony's step
    subprocess.run([str(UPLOADER)], env=env, capture_output=True, text=True, timeout=30)
    up = (d / "uploaded.txt").read_text().split() if (d / "uploaded.txt").exists() else []
    check("U1 a file written under the January clock is NOT uploaded (the stranding)", "sht40_2026-01-11.csv" not in up, up)
    check("U1b a file written after the watermark IS uploaded", "sht40_2026-11-11.csv" in up, up)

    # With the floor: restore sets the clock to >= watermark+1, so a file written then is newer than the watermark.
    (d / "uploaded.txt").unlink(missing_ok=True)
    rig = Rig(clock=T_MAR, step_at=6, step_to=T_JAN)
    rig.set_floor(T_NOV - 1800)                 # floor older than the watermark: watermark must win
    ws = rig.d / "upload.state"; ws.write_text(""); os.utime(ws, (T_NOV, T_NOV))
    rig.run("restore")
    written_at = rig.clock_now() + 25
    mk("sht40_2026-11-11.csv", written_at)      # row written 25 s after restore
    os.utime(state, (T_NOV, T_NOV))
    subprocess.run([str(UPLOADER)], env=env, capture_output=True, text=True, timeout=30)
    up = (d / "uploaded.txt").read_text().split() if (d / "uploaded.txt").exists() else []
    check("U2 no-data wake: with the floor, the new file is newer than the watermark and uploads",
          written_at > T_NOV and "sht40_2026-11-11.csv" in up, (written_at, up))

    # ── logger columns ────────────────────────────────────────────────
    spec = importlib.util.spec_from_file_location("sensors_logger", LOGGER)
    sl = importlib.util.module_from_spec(spec)
    os.environ["ORC_SENSORS_CONF_DIR"] = str(d)
    spec.loader.exec_module(sl)
    sf = d / "clock_state"
    sl.CLOCK_STATE_FILE = str(sf)
    sf.write_text("restored=1\nadj_s=26265600\nfloor=1\n")
    check("L1 restored=1 -> clock_state 1 with adj", sl.clock_columns() == {"clock_state": 1, "clock_adj_s": 26265600}, sl.clock_columns())
    sf.write_text("restored=0\nadj_s=0\n")
    check("L2 restored=0 -> clock_state 0", sl.clock_columns() == {"clock_state": 0, "clock_adj_s": 0}, sl.clock_columns())
    sf.unlink()
    check("L3 no state file -> clock_state 2 (service did not run)", sl.clock_columns() == {"clock_state": 2, "clock_adj_s": ""}, sl.clock_columns())
    sf.write_text("restored=1\nadj_s=oops\n")
    check("L4 garbage in the state file -> clock_state 2, never raises", sl.clock_columns()["clock_state"] == 2)

    sl.DRIVERS["fake"] = lambda conf: {"x": 7}
    sf.write_text("restored=1\nadj_s=99\n")
    out = d / "out"; out.mkdir()
    for tag, header in (("with", "timestamp,x,clock_state,clock_adj_s"), ("without", "timestamp,x")):
        c = d / f"{tag}.conf"
        c.write_text(f"SENSOR_TYPE=fake\nSENSOR_LABEL={tag}\nLOG_DIR={out}\nINTERVAL_SEC=1\nCSV_HEADER={header}\n")
        sl.process_sensor(str(c))
    rows = {t: next(out.glob(f"{t}_*.csv")).read_text().strip().split("\n") for t in ("with", "without")}
    check("L5 header listing the columns gets them in the row", rows["with"][1].split(",")[2:] == ["1", "99"], rows["with"])
    check("L6 header without them: row unchanged (inert until a conf opts in)",
          rows["without"][0] == "timestamp,x" and len(rows["without"][1].split(",")) == 2, rows["without"])

    bad = [n for n, ok in results if not ok]
    print(f"\n{len(results) - len(bad)}/{len(results)} passed" + (f"; FAILED: {bad}" if bad else ""))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
