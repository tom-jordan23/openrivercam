#!/usr/bin/env python3
"""ISS-FIELD-015 follow-up: confirm Sukabumi cycles on the :00/:30 UTC grid again.

Run it after iss015_button_grab.sh has finished and the Pi has powered off. It
answers one question: did two consecutive wakes arrive on the grid?

PASSIVE. The only thing it runs is `tailscale status --json` on this machine. It
does not ssh, does not probe tcp/22, and sends the station nothing, so it cannot
disturb a wake. That is why it is safe to leave beside a grab, but it must still
run as a session-scoped process (Monitor), never systemd/nohup/linger
(no-unattended-station-monitoring, Tom 2026-09-01).

HOW A WAKE IS SEEN
    Tailscale `Online` is the control plane's own verdict. A wake starts at the
    first poll that sees Online=True after an Online=False poll, and ends at the
    first poll that sees Online=False (the end time is taken from LastSeen, which
    is closer to the real disconnect than the poll). A wake is ON GRID when it
    starts within GRID_TOL_S after a :00 or :30 UTC slot. Tailscale registration
    lags boot by tens of seconds; the 10-21 stop showed LastSeen 198 s after its
    slot at the END of a wake, so the start tolerance is much smaller than that.
    If Online=True on the very first poll, that is the button-press wake (or a
    wake already under way): it is reported and NOT counted.

SUCCESS = two counted wakes, both on grid, whose starts are a whole number of
30-minute slots apart (within tolerance). Gaps of hours are fine: the solar
schedule skips the night (423 wakes in 24 days is about 18 a day, not 48).

EXIT 0 two on-grid wakes; 1 an off-grid wake was seen (still keeps watching
unless --stop-on-offgrid); 2 deadline passed with fewer than two.

USAGE
    iss015_two_wakes.py [--poll 5] [--wait-s 50400] [--log PATH] [--selftest]
"""
import argparse
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
SLOT_S = 1800
GRID_TOL_S = 150      # start of a wake, seconds after a :00/:30 slot
GAP_TOL_S = 150       # tolerance on start-to-start spacing being a multiple of SLOT_S
FLAP_S = 300          # Online=False then True again within this long is the SAME wake (seen 11-11:
                      # 08:02:53 off, 08:03:08 on, 08:04:38 off; the boot list showed one boot)


def iso(t):
    return datetime.fromtimestamp(t, timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")


def slot_offset(t):
    """Seconds since the most recent :00/:30 UTC slot."""
    return t % SLOT_S


class Tracker:
    """Pure state machine; feed it (now, online, last_seen_epoch_or_None)."""

    def __init__(self):
        self.first = True
        self.online = None
        self.cur_start = None
        self.cur_counted = False
        self.wakes = []       # counted wakes: dict(start, end, offset, ongrid)
        self.events = []      # human lines produced by the last update()
        self.last_off = None  # observation time of the last Online=False after a counted wake

    def update(self, now, online, last_seen):
        self.events = []
        if online is None:
            return
        if self.first:
            self.first = False
            self.online = online
            if online:
                self.cur_start, self.cur_counted = now, False
                self.events.append(f"baseline: Online=True at {iso(now)} - press wake or one under way; NOT counted")
            else:
                self.events.append(f"baseline: Online=False at {iso(now)} (LastSeen {iso(last_seen) if last_seen else '?'})")
            return
        if online and not self.online and self.wakes and self.last_off is not None \
                and now - self.last_off <= FLAP_S and self.wakes[-1]["end"] is not None:
            # back online shortly after going offline: same wake, not a new one
            self.wakes[-1]["end"] = None
            self.cur_start, self.cur_counted = self.cur_start or self.wakes[-1]["start"], True
            self.events.append(f"flap: back online {now - self.last_off:.0f} s after going offline - same wake {len(self.wakes)}")
            self.last_off = None
        elif online and not self.online:
            self.cur_start, self.cur_counted = now, True
            off = slot_offset(now)
            ongrid = off <= GRID_TOL_S
            self.wakes.append({"start": now, "end": None, "offset": off, "ongrid": ongrid})
            tag = "ON GRID" if ongrid else "OFF GRID"
            near = off if off <= SLOT_S / 2 else off - SLOT_S
            self.events.append(f"WAKE {len(self.wakes)} start {iso(now)} ({near:+.0f} s from slot) {tag}")
        elif not online and self.online:
            start = self.cur_start if self.cur_start is not None else now
            end = max(last_seen or now, start)     # LastSeen can predate the start; never report a negative length
            if self.cur_counted and self.wakes:
                self.wakes[-1]["end"] = end
                self.last_off = now
            self.events.append(f"wake ended ~{iso(end)} (observed {iso(now)}), lasted ~{end - start:.0f} s")
            self.cur_start = None
        self.online = online

    def verdict(self):
        """('OK'|'OFFGRID'|None, text)"""
        w = self.wakes
        if any(not x["ongrid"] for x in w):
            bad = next(x for x in w if not x["ongrid"])
            return "OFFGRID", f"off-grid wake at {iso(bad['start'])} ({bad['offset']:.0f} s after a slot)"
        if len(w) >= 2:
            a, b = w[0], w[1]
            gap = b["start"] - a["start"]
            k = round(gap / SLOT_S)
            if k >= 1 and abs(gap - k * SLOT_S) <= GAP_TOL_S:
                return "OK", (f"CYCLE OK: wake 1 {iso(a['start'])} (+{a['offset']:.0f} s), "
                              f"wake 2 {iso(b['start'])} (+{b['offset']:.0f} s), gap {gap/60:.0f} min = {k} slot(s)")
            return "OFFGRID", f"wakes {gap/60:.1f} min apart is not a whole number of 30-min slots"
        return None, f"{len(w)} counted wake(s) so far"


def tailscale_state(host_hint="sukabumi"):
    """(online, last_seen_epoch) or (None, None) if tailscale can't be read."""
    try:
        p = subprocess.run(["tailscale", "status", "--json"], capture_output=True,
                           text=True, timeout=25)
        d = json.loads(p.stdout)
        for peer in (d.get("Peer") or {}).values():
            if host_hint in (peer.get("HostName", "") + peer.get("DNSName", "")).lower():
                ls = None
                try:
                    ls = datetime.fromisoformat(str(peer.get("LastSeen")).replace("Z", "+00:00")).timestamp()
                except (ValueError, TypeError):
                    pass
                return bool(peer.get("Online")), ls
    except Exception:
        pass
    return None, None


def selftest():
    t0 = 1_800_000_000 - (1_800_000_000 % SLOT_S)      # a slot boundary
    def run(samples):
        tr = Tracker()
        for now, on, ls in samples:
            tr.update(now, on, ls)
        return tr
    # 1. press wake is not counted; two on-grid wakes 30 min apart -> OK
    s = [(t0 - 600, True, None), (t0 - 500, False, t0 - 520),
         (t0 + 1800 + 50, True, None), (t0 + 1800 + 200, False, t0 + 1800 + 180),
         (t0 + 3600 + 45, True, None), (t0 + 3600 + 190, False, t0 + 3600 + 170)]
    tr = run(s); v = tr.verdict(); assert v[0] == "OK" and len(tr.wakes) == 2, v
    # 2. gap of several hours (night) is fine
    s = [(t0, False, None), (t0 + 6 * 3600 + 60, True, None), (t0 + 6 * 3600 + 200, False, t0 + 6 * 3600 + 190),
         (t0 + 7 * 3600 + 30, True, None)]
    assert run(s).verdict()[0] == "OK"
    # 3. off-grid wake (starts 10 min after slot) is flagged
    s = [(t0, False, None), (t0 + 1800 + 600, True, None)]
    assert run(s).verdict()[0] == "OFFGRID"
    # 4. spacing not a whole number of slots
    s = [(t0, False, None), (t0 + 1800 + 40, True, None), (t0 + 1800 + 160, False, None),
         (t0 + 1800 + 40 + 2700, True, None)]
    assert run(s).verdict()[0] == "OFFGRID"
    # 5. one wake only -> undecided
    s = [(t0, False, None), (t0 + 1800 + 40, True, None)]
    assert run(s).verdict()[0] is None
    # 6. unreadable tailscale never counts as a transition
    s = [(t0, False, None), (t0 + 10, None, None), (t0 + 20, False, None)]
    assert len(run(s).wakes) == 0
    # 7. baseline already online is never counted
    tr = run([(t0 + 10, True, None), (t0 + 100, False, t0 + 90)]); assert tr.wakes == []
    # 8. 11-11 pattern: on, off, back on 15 s later, off again = ONE wake; next slot = second wake
    s = [(t0 - 60, False, None), (t0 + 43, True, None), (t0 + 173, False, t0 + 20),
         (t0 + 188, True, None), (t0 + 278, False, t0 + 270),
         (t0 + 1800 + 40, True, None), (t0 + 1800 + 170, False, t0 + 1800 + 160)]
    tr = run(s); assert len(tr.wakes) == 2 and tr.verdict()[0] == "OK", (len(tr.wakes), tr.verdict())
    assert all(w["end"] is None or w["end"] >= w["start"] for w in tr.wakes)
    # 9. a gap longer than FLAP_S is a new wake and, if off-grid, is still flagged
    s = [(t0 - 60, False, None), (t0 + 43, True, None), (t0 + 173, False, t0 + 160),
         (t0 + 173 + 400, True, None)]
    assert run(s).verdict()[0] == "OFFGRID"
    print("selftest ok")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--poll", type=float, default=5.0)
    ap.add_argument("--wait-s", type=int, default=14 * 3600)
    ap.add_argument("--log", default=None, help="also append every line here")
    ap.add_argument("--stop-on-offgrid", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        selftest(); return 0

    logf = open(a.log, "a") if a.log else None

    def out(msg):
        line = f"[{datetime.now(timezone.utc).strftime('%H:%M:%SZ')}] {msg}"
        print(line, flush=True)
        if logf:
            logf.write(line + "\n"); logf.flush()

    out(f"two-wake watch armed: passive (tailscale status only), poll {a.poll:g}s, "
        f"deadline {a.wait_s/3600:.1f} h; on grid = start within {GRID_TOL_S}s after :00/:30 UTC")
    tr = Tracker()
    deadline = time.time() + a.wait_s
    last_beat = time.time()
    unreadable = 0
    saw_offgrid = False
    while time.time() < deadline:
        online, ls = tailscale_state()
        now = time.time()
        if online is None:
            unreadable += 1
            if unreadable in (3, 60):
                out(f"WARNING: tailscale status unreadable {unreadable}x in a row - not counting anything")
        else:
            if unreadable >= 3:
                out("tailscale readable again")
            unreadable = 0
        tr.update(now, online, ls)
        for e in tr.events:
            out(e)
        kind, text = tr.verdict()
        if kind == "OK":
            out(text); return 0
        if kind == "OFFGRID" and not saw_offgrid:
            saw_offgrid = True
            out(f"*** {text} ***")
            if a.stop_on_offgrid:
                return 1
        if now - last_beat >= 3600:
            out(f"still watching: Online={tr.online}, {text}")
            last_beat = now
        time.sleep(a.poll)
    kind, text = tr.verdict()
    out(f"deadline reached: {text}" + (" [off-grid seen]" if saw_offgrid else ""))
    return 1 if saw_offgrid else 2


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("stopped.", flush=True)
        sys.exit(130)
