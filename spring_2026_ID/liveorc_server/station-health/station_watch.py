#!/usr/bin/env python3
"""station_watch.py — wait for Sukabumi to come back, then grab its power state.

WHY
    ISS-FIELD-008 / TODO-116. The station is down, and every theory about why
    is decided by state that exists only on the Witty Pi: the power-on reason,
    the alarm time, the two voltage thresholds, the undervolt bits. None of it
    is uploaded. To read it, someone has to be logged in while the station is
    awake — and in production it is awake about two minutes in every thirty.

    A person cannot win that race; they would have to sit on a terminal for
    however many days it takes. A poller can. This watches for the station to
    reappear and runs the collector within seconds, unattended.

    It is written for the case where the station comes back **on its own**,
    which is the open question — every recovery so far landed in Indonesian
    business hours, which is what a person pressing the button looks like, not
    a voltage threshold. If it never fires, that is itself the answer.

WHAT IT TOUCHES
    Locally: a state file and an output directory. Remotely: one SSH session
    that runs a read-only collector. It changes nothing on the station — not
    the schedule, not the thresholds, not a service. See orc_wp5_state.sh.

    The Grafana query is anonymous and read-only (see station_gaps.py).

USAGE
    ./station_watch.py                      # poll until it comes back
    ./station_watch.py --once               # single check, for cron/systemd
    ./station_watch.py --dry-run            # report state, never SSH

    Leave it running in a terminal, or install the systemd user unit in
    station-watch.service.

WHICH SIGNAL FIRES IT
    A TCP connect to port 22, and nothing else. That is ground truth for "can
    I actually reach it", needs no credentials, and is the only thing that can
    justify spending an under-60-second window on an SSH.

    NOT Tailscale's Online flag. The Pi never disconnects cleanly — its power
    is cut — so the control plane keeps reporting Online for minutes after the
    station has slept. On 2026-08-27 a deploy fired on exactly that and the
    SSH timed out; `tailscale status` was printing `active; relay "sin"` and
    `offline, last seen 3m ago` for the same node in the same breath. This
    file carried that warning in two docstrings while check() went on trusting
    the flag anyway. It no longer does.

    NOT a fresh sensor row either. A row proves the station booted within the
    last cycle, not that it is powered on now. It is still polled and printed,
    throttled to --sensor-poll, so an off-tailnet workstation learns the
    station is running — but it never triggers a collect, because a collect
    that cannot connect is a window spent for nothing.
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
# spring_2026_ID/ — parents[0] is liveorc_server, [1] is the project dir. The
# collectors live under it at pi/tools/; parents[2] is the git root and misses.
REPO_ROOT = HERE.parents[1]
COLLECTOR = REPO_ROOT / "pi/tools/orc_wp5_state.sh"
FULL_BUNDLE = REPO_ROOT / "pi/tools/orc_collect.sh"

DEFAULT_HOST = "orc-sukabumi"
DEFAULT_USER = "pi"
DEFAULT_STATE = Path.home() / ".cache/orc-station-watch.json"
DEFAULT_OUT = REPO_ROOT.parent / "data/station-forensics"

sys.path.insert(0, str(HERE))
import station_gaps as sg  # noqa: E402


def tailscale_online(host):
    """True if the node is on the tailnet right now.

    CAUTION: this lags reality for a duty-cycled station. The Pi does not
    disconnect cleanly — its power is cut — so the control plane keeps
    reporting Online for minutes afterwards. On 2026-08-27 a deploy fired on a
    stale Online flag three minutes after the station had slept, and the SSH
    timed out. `tailscale status` was simultaneously printing
    `active; relay "sin"` and `offline, last seen 3m ago` for the same node.

    For anything that must actually connect, use port_open() instead: a TCP
    connect to 22 is ground truth and needs no credentials. This stays as the
    cheap wake-detection hint.

    Absence is not evidence of a down station — this machine may be off the
    tailnet itself — so a False here only ever defers to the sensor signal.
    """
    try:
        out = subprocess.run(
            ["tailscale", "status", "--json"], capture_output=True, text=True, timeout=15
        )
        if out.returncode != 0:
            return None
        peers = json.loads(out.stdout).get("Peer", {}) or {}
        for p in peers.values():
            names = [p.get("HostName", ""), p.get("DNSName", "").split(".")[0]]
            if host in names:
                return bool(p.get("Online"))
        return None
    except Exception:
        return None


def port_open(host, port=22, timeout_s=3):
    """True if a TCP connect to host:port succeeds right now.

    Ground truth for "can I actually reach it", as opposed to what the tailnet
    control plane last believed. No credentials, no auth attempt, no log noise
    on the station.
    """
    import socket
    try:
        with socket.create_connection((host, port), timeout=timeout_s):
            return True
    except OSError:
        return False


def sensor_age_minutes(station):
    """Minutes since the last sensor row, or None if unreachable."""
    sql = (
        "SELECT EXTRACT(epoch FROM (now() - max(ts))) / 60.0 AS age_min "
        f"FROM sensor_readings WHERE station = '{station}'"
    )
    try:
        rows = sg.query(sql, sg.DEFAULT_GRAFANA, sg.DEFAULT_CA, timeout=30)[1]
    except SystemExit:
        return None
    if not rows or rows[0]["age_min"] is None:
        return None
    return float(rows[0]["age_min"])


def load_password():
    """Read the pi account password from spring_2026_ID/.env, or None.

    Accepts either a bare password on its own line or KEY=VALUE. The file is
    gitignored (this repo is public); nothing here writes it anywhere, and the
    value is handed to ssh through the environment rather than argv so it never
    appears in the process list.
    """
    env = REPO_ROOT / ".env"
    if not env.is_file():
        return None
    for line in env.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        return line.split("=", 1)[1].strip() if "=" in line else line
    return None


def askpass_env(password):
    """Env + helper script letting ssh answer its own password prompt.

    OpenSSH >= 8.4 honours SSH_ASKPASS_REQUIRE=force, which uses the helper even
    when a tty is present. That avoids an sshpass dependency and, unlike
    `sshpass -p`, keeps the secret out of argv. BatchMode must be off for the
    prompt to happen at all.
    """
    helper = Path(tempfile.gettempdir()) / "orc-askpass.py"
    helper.write_text(
        "#!/usr/bin/env python3\n"
        "import os, sys\n"
        "sys.stdout.write(os.environ['ORC_SSH_PASSWORD'])\n"
    )
    helper.chmod(0o700)
    env = dict(os.environ)
    env.update({
        "ORC_SSH_PASSWORD": password,
        "SSH_ASKPASS": str(helper),
        "SSH_ASKPASS_REQUIRE": "force",
        "DISPLAY": env.get("DISPLAY", ":0"),
    })
    return env


def collect(user, host, outdir, full=False):
    """Run the read-only collectors over SSH, newest-value-first.

    orc_wp5_state.sh is ordered so that a truncated run still yields the
    decisive parts. The full bundle is attempted second and is allowed to fail:
    losing it costs nothing that the first grab did not already secure.
    """
    outdir.mkdir(parents=True, exist_ok=True)
    ok = False
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    results = []

    jobs = [("wp5-state", COLLECTOR)]
    if full:
        jobs.append(("collect", FULL_BUNDLE))

    for name, script in jobs:
        if not script.is_file():
            results.append(f"{name}: MISSING {script}")
            continue
        dest = outdir / f"{host}-{name}-{stamp}.txt"
        password = load_password()
        env = askpass_env(password) if password else None
        cmd = [
            "ssh",
            "-o", f"BatchMode={'no' if password else 'yes'}",
            "-o", "StrictHostKeyChecking=accept-new",
            "-o", "ConnectTimeout=10",
            "-o", "NumberOfPasswordPrompts=1",
            f"{user}@{host}",
            # -S so sudo takes the same password on stdin... except stdin is the
            # script. Rely on NOPASSWD (deploy.sh assumes it throughout) and let
            # a sudo prompt fail loudly rather than hang the window.
            "sudo -n bash -s",
        ]
        try:
            with open(script, "rb") as fh, open(dest, "wb") as out:
                p = subprocess.run(cmd, stdin=fh, stdout=out,
                                   stderr=subprocess.STDOUT, timeout=150, env=env)
            size = dest.stat().st_size

            # If sudo is not NOPASSWD, -n refuses instantly. Most of the
            # collector still works unprivileged (vcgencmd, wp5, uptime), and a
            # partial grab inside a 60-second window beats an empty one, so
            # retry without sudo rather than surrender the window.
            head = dest.read_bytes()[:400].decode("utf-8", "replace")
            if "sudo:" in head or (p.returncode != 0 and size < 2000):
                cmd_nosudo = cmd[:-1] + ["bash -s"]
                with open(script, "rb") as fh, open(dest, "wb") as out:
                    p = subprocess.run(cmd_nosudo, stdin=fh, stdout=out,
                                       stderr=subprocess.STDOUT, timeout=150, env=env)
                size = dest.stat().st_size
                results.append(f"{name}: sudo refused, retried unprivileged")

            results.append(f"{name}: rc={p.returncode} {size}B -> {dest}")
            if name == "wp5-state" and p.returncode == 0 and size > 2000:
                ok = True
        except subprocess.TimeoutExpired:
            results.append(f"{name}: TIMEOUT (partial output kept) -> {dest}")
        except Exception as exc:
            results.append(f"{name}: FAILED {exc}")
    return results, ok


def load_state(path):
    try:
        return json.loads(path.read_text())
    except Exception:
        return {}


def save_state(path, state):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2))


# Sensor age costs a round trip to Grafana, and the port poll now runs every
# few seconds. Cache it so the fast loop does not hammer the server.
_age_cache = {"at": 0.0, "value": None}


def cached_sensor_age(station, max_age_s):
    """sensor_age_minutes(), re-queried at most every max_age_s seconds."""
    now = time.monotonic()
    if _age_cache["value"] is None or now - _age_cache["at"] >= max_age_s:
        _age_cache["value"] = sensor_age_minutes(station)
        _age_cache["at"] = now
    return _age_cache["value"]


def check(args):
    """One evaluation. Returns (reachable, alive, human_readable_reason).

    reachable   a TCP connect to 22 succeeded right now. This is the ONLY
                signal that justifies spending the window on an SSH, and the
                only one that gates a collect.

    alive       a sensor row landed within one duty cycle. Says the station
                booted recently, NOT that it is powered on now — it is awake
                ~2 min in 30. Reported so an off-tailnet workstation still
                learns the station is running; never triggers a collect,
                because a collect it cannot connect for is a wasted window.

    Tailscale's Online flag is printed and deliberately trusted for nothing.
    It stays stale for minutes after this station sleeps — on 2026-08-27 a
    deploy fired on it three minutes after the Pi had slept and the SSH timed
    out. That is the bug this function used to have.
    """
    reachable = port_open(args.host, 22)
    ts_online = tailscale_online(args.host)
    age = cached_sensor_age(args.station, args.sensor_poll)
    alive = age is not None and age <= args.fresh_min

    reasons = [
        "tcp/22=" + ("OPEN" if reachable else "closed"),
        "tailscale=" + {True: "ONLINE", False: "offline", None: "unknown"}[ts_online],
        "sensor_age=" + ("unknown" if age is None else f"{age:.0f}m"),
    ]
    return reachable, alive, ", ".join(reasons)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--station", default="sukabumi")
    ap.add_argument("--host", default=DEFAULT_HOST, help="Tailscale name to SSH to")
    ap.add_argument("--user", default=DEFAULT_USER)
    # The awake window is under 60 seconds, so a 60-second poll can miss a
    # whole wake. The port probe is cheap (one TCP connect, 3 s timeout);
    # the expensive Grafana query is throttled separately by --sensor-poll.
    ap.add_argument("--interval", type=int, default=15, help="seconds between polls")
    ap.add_argument("--sensor-poll", type=int, default=300,
                    help="seconds between Grafana sensor-age queries (default 300)")
    ap.add_argument(
        "--fresh-min",
        type=float,
        default=35.0,
        help="a sensor row newer than this many minutes means the station is up "
             "(default 35: one 30-minute cycle plus slack)",
    )
    ap.add_argument("--once", action="store_true", help="check once and exit")
    ap.add_argument("--dry-run", action="store_true", help="never SSH; just report")
    ap.add_argument("--full", action="store_true",
                    help="also run the slower orc_collect.sh bundle")
    ap.add_argument("--state", type=Path, default=DEFAULT_STATE)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args()

    state = load_state(args.state)
    was_up = state.get("up", False)
    already = state.get("collected_for_boot", False)

    was_alive = state.get("alive", False)

    while True:
        now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
        up, alive, why = check(args)

        if up and not was_up:
            print(f"[{now}] *** STATION IS BACK — tcp/22 OPEN *** ({why})", flush=True)
            already = False
        elif not up and was_up:
            print(f"[{now}] station unreachable again ({why})", flush=True)
        elif alive and not was_alive:
            # Rows resumed but we cannot connect: it booted and we lost the
            # window, or this workstation is off the tailnet. Either way it is
            # news, and it is NOT grounds to try an SSH.
            print(f"[{now}] *** SENSOR ROWS RESUMED (not reachable) *** ({why})",
                  flush=True)
        else:
            print(f"[{now}] {'reachable' if up else 'down'} ({why})", flush=True)

        if up and not already:
            if args.dry_run:
                print("  --dry-run: would collect now", flush=True)
            else:
                print("  collecting...", flush=True)
                lines, ok = collect(args.user, args.host, args.out, args.full)
                for line in lines:
                    print("  " + line, flush=True)
                # Only a real grab ends the hunt. A refused or timed-out SSH
                # means we lost this window, not that the job is done.
                already = ok
                if not ok:
                    print("  grab failed — will retry on the next wake", flush=True)

        was_up, was_alive = up, alive
        state.update({"up": up, "alive": alive,
                      "collected_for_boot": already, "last_check": now})
        save_state(args.state, state)

        if args.once:
            return 0 if up else 1
        time.sleep(args.interval)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nstopped.")
