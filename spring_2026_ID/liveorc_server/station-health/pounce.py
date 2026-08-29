#!/usr/bin/env python3
"""pounce.py — win a seconds-long wake window, and grab the one thing that matters.

THE QUESTION THIS EXISTS TO ANSWER
    Is Sukabumi dying early, or just staying off? Everything else pivots on it:
    a station that boots every 30 minutes and dies young needs a different fix
    from one that mostly never powers on, and from outside they look identical.

    `/var/log/wp5d.log` settles it in one read. Every boot writes
    "Startup reason: ...", so the spacing of those lines through the outage is
    a direct record of how often the Witty Pi actually powered the Pi up —
    independent of whether anything reached the server.

WHY station_watch.py CANNOT GET IT
    It polls tcp/22 every 15 s and, on success, runs the full read-only
    collector. That was sized for a ~60 s wake. The 2026-08-29 00:00 WIB wake
    registered with the Tailscale control plane and pushed two files in a few
    seconds, and tcp/22 was never seen open at all. A 15 s poll cannot win a
    window that short, and the broad collector is the wrong first thing to
    spend it on.

WHAT THIS DOES DIFFERENTLY
    1. Triggers on Tailscale's LastSeen advancing, not on tcp/22. LastSeen
       moves as soon as the control plane hears from the node, which is earlier
       in the boot than sshd being reachable. It means "it is awake RIGHT NOW",
       which is the cue to start trying rather than the cue to give up.
    2. On any sign of life, pounces: probes tcp/22 every second for POUNCE_SECS
       instead of every fifteen.
    3. Grabs the decisive artefact FIRST and alone — one short command, no
       sudo, no pipeline. The broad collector only runs afterwards, if the
       window is still open. A truncated grab that yields the power-on history
       beats a complete one that yields nothing.

READ-ONLY. It runs `tail` and `cat` over SSH and writes files locally. It does
not deploy, configure, or restart anything on the station.
"""

import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import station_watch as sw  # noqa: E402  (reuse its ssh/askpass/port helpers)

HOST = "orc-sukabumi"
USER = "pi"
OUT = HERE.parents[2] / "data" / "station-forensics"
IDLE_POLL_S = 5.0        # how often to check for signs of life
POUNCE_POLL_S = 1.0      # how often to probe tcp/22 once life is detected
POUNCE_SECS = 240        # how long to keep trying after a sign of life

# The decisive grab, deliberately tiny. wp5d.log lines are ~60 bytes; 400 of
# them spans days of boots and still returns in well under a second.
PRIMARY_CMD = (
    "echo '--- date ---'; date -u; "
    "echo '--- uptime ---'; uptime; "
    # 1. The pivot: dying early or staying off. Everything else is secondary.
    "echo '--- wp5d.log tail ---'; tail -n 400 /var/log/wp5d.log; "
    # 2. The maintenance chain. The flag itself cannot be stuck — /run is tmpfs
    #    and every failure path in orc-maintenance-check rm -f's it — but the
    #    CHECK retries GitHub 12 times at up to 15 s and is ordered
    #    Before=orc-api.service, so an unreachable GitHub stalls the capture
    #    chain for up to 180 s on every boot. That is longer than a healthy
    #    wake, and would produce long wakes and missing video with maintenance
    #    mode never set. The journal timestamps show which branch ran and how
    #    long it took; the ls settles the flag question directly rather than
    #    from the tmpfs argument.
    "echo '--- maintenance flag ---'; ls -la /run/orc-maintenance-mode 2>&1 || true; "
    "echo '--- /run is tmpfs? ---'; findmnt -no FSTYPE /run 2>/dev/null || true; "
    "echo '--- orc-maintenance journal ---'; "
    "journalctl -t orc-maintenance -n 40 --no-pager 2>/dev/null || true; "
    "echo '--- maintenance unit ---'; "
    "systemctl status orc-maintenance-check --no-pager -n 5 2>/dev/null || true; "
    # 3. Cheap context: disk is ISS-FIELD-009's whole thesis, and undervolt bits
    #    are the only power evidence available without the Witty Pi.
    "echo '--- disk ---'; df -h / | tail -2; "
    "echo '--- throttled ---'; vcgencmd get_throttled 2>/dev/null || true"
)


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")


def log(msg):
    print(f"[{now()}] {msg}", flush=True)


def last_seen():
    """Tailscale's LastSeen for the station, as a raw string, or None."""
    try:
        p = subprocess.run(["tailscale", "status", "--json"],
                           capture_output=True, text=True, timeout=25)
        import json
        d = json.loads(p.stdout)
        for peer in (d.get("Peer") or {}).values():
            name = (peer.get("HostName", "") + peer.get("DNSName", "")).lower()
            if "sukabumi" in name:
                return f"{peer.get('LastSeen')}|{peer.get('Online')}"
    except Exception:
        return None
    return None


def ssh_grab(cmd, label):
    """One short SSH round trip into a timestamped file. Returns bytes written."""
    OUT.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    dest = OUT / f"{HOST}-{label}-{stamp}.txt"
    password = sw.load_password()
    env = sw.askpass_env(password) if password else None
    argv = [
        "ssh",
        "-o", f"BatchMode={'no' if password else 'yes'}",
        "-o", "StrictHostKeyChecking=accept-new",
        "-o", "ConnectTimeout=5",
        "-o", "NumberOfPasswordPrompts=1",
        f"{USER}@{HOST}", cmd,
    ]
    try:
        with open(dest, "wb") as fh:
            subprocess.run(argv, stdout=fh, stderr=subprocess.STDOUT,
                           timeout=45, env=env)
    except subprocess.TimeoutExpired:
        pass
    size = dest.stat().st_size if dest.exists() else 0
    if size < 40:
        dest.unlink(missing_ok=True)
        return 0
    log(f"*** GRABBED {label}: {size} bytes -> {dest.name} ***")
    return size


def pounce(reason):
    log(f"*** SIGN OF LIFE ({reason}) — pouncing for {POUNCE_SECS}s ***")
    deadline = time.time() + POUNCE_SECS
    got_primary = False
    while time.time() < deadline:
        if sw.port_open(HOST, 22, timeout_s=2):
            log("tcp/22 OPEN — grabbing wp5d.log first")
            if not got_primary and ssh_grab(PRIMARY_CMD, "wp5dlog"):
                got_primary = True
                # Only now spend the rest of the window on the broad collector.
                collector = HERE.parents[1] / "pi/tools/orc_wp5_state.sh"
                if collector.is_file():
                    log("primary secured — attempting the full collector")
                    try:
                        sw.collect(USER, HOST, OUT, full=False)
                    except Exception as e:
                        log(f"full collector failed (primary is safe): {e}")
                return True
        time.sleep(POUNCE_POLL_S)
    log("pounce window expired without tcp/22 opening")
    return False


def main():
    log(f"pounce armed — idle poll {IDLE_POLL_S}s, pounce poll {POUNCE_POLL_S}s")
    prev = last_seen()
    log(f"baseline LastSeen: {prev}")
    # Keep a periodic line in the shared log. Without it a quiet log is
    # ambiguous between "watching, still down" and "watcher died", which is the
    # exact confusion this project has already had twice.
    last_beat = 0.0
    while True:
        if time.time() - last_beat >= 300:
            log(f"idle — tcp/22 closed, LastSeen {prev}")
            last_beat = time.time()
        # Cheap check first: if the port is somehow already open, go now.
        if sw.port_open(HOST, 22, timeout_s=2):
            pounce("tcp/22 already open")
            prev = last_seen()
            continue
        cur = last_seen()
        if cur and prev and cur != prev:
            log(f"LastSeen advanced: {prev} -> {cur}")
            pounce("tailscale LastSeen advanced")
            prev = last_seen()
        elif cur and not prev:
            prev = cur
        time.sleep(IDLE_POLL_S)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log("stopped.")
