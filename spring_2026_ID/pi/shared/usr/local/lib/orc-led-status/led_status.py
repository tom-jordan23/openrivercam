#!/usr/bin/env python3
"""orc-led-status — drive WS2812B status LED based on system health.

Long-running daemon that polls subsystem health and sets a single WS2812B
NeoPixel LED color/pattern accordingly. Designed for Raspberry Pi 5.

Configuration: /etc/orc/led-status.yaml (or ORC_LED_STATUS_CONF env var)
Spec:          docs/LED_STATUS_SPEC.md

Requires: adafruit-blinka, adafruit-circuitpython-neopixel (import neopixel),
          adafruit-blinka-raspberry-pi5-neopixel (auto-loaded Pi 5 backend),
          PyYAML
Must run as root (RP1 PIO access via /dev/pio0).

NOTE: rpi-ws281x does NOT work on Pi 5 — see ISSUE_LOG.md ISS-007.
"""

import argparse
import math
import os
import re
import signal
import subprocess
import sys
import time

import yaml

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

TICK_HZ = 50                       # main loop frequency (Hz)
TICK_PERIOD = 1.0 / TICK_HZ       # 20 ms
DEFAULT_CONF = "/etc/orc/led-status.yaml"
ORC_CAPTURE_CONF = "/etc/orc-capture.conf"

# Fixed cycle order for error display
ERROR_ORDER = ["camera", "network", "storage", "power"]

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

DEFAULT_CONFIG = {
    "led": {"gpio_pin": 18, "brightness": 200},
    "poll_interval_s": 5,
    "states": {
        "boot":        {"color": [255, 255, 255], "pattern": "solid"},
        "idle":        {"color": [0, 255, 0],     "pattern": "solid"},
        "capture":     {"color": [0, 255, 0],     "pattern": "flash", "flash_hz": 2},
        "maintenance": {"color": [0, 255, 255],   "pattern": "solid"},
        "shutdown":    {"color": [0, 255, 0],      "pattern": "pulse"},
    },
    "errors": {
        "camera":  {"color": [255, 0, 0],     "suppressed": False},
        "network": {"color": [0, 0, 255],     "suppressed": False},
        "storage": {"color": [255, 255, 0],   "suppressed": False},
        "power":   {"color": [255, 0, 255],   "suppressed": False},
    },
    "error_display": {"cycle_interval_s": 3, "blink_hz": 4},
    "overrides": {},
}


def load_config(path):
    """Load YAML config, merge with defaults."""
    cfg = dict(DEFAULT_CONFIG)
    if os.path.isfile(path):
        with open(path) as f:
            user = yaml.safe_load(f)
        if user:
            _deep_merge(cfg, user)
    return cfg


def _deep_merge(base, override):
    """Recursively merge override into base dict (in place)."""
    for k, v in override.items():
        if k in base and isinstance(base[k], dict) and isinstance(v, dict):
            _deep_merge(base[k], v)
        else:
            base[k] = v


def parse_orc_capture_conf(path=ORC_CAPTURE_CONF):
    """Read KEY=VALUE config to extract CAMERA_IP."""
    result = {}
    if not os.path.isfile(path):
        return result
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            m = re.match(r'^([A-Z_]+)=(.*)$', line)
            if m:
                val = m.group(2).strip('"').strip("'")
                # Strip inline comments (e.g. "192.168.50.101  # comment")
                if "#" in val:
                    val = val[:val.index("#")].rstrip()
                result[m.group(1)] = val
    return result


# ---------------------------------------------------------------------------
# LED Driver
# ---------------------------------------------------------------------------

class LedDriver:
    """Thin wrapper around Adafruit Blinka Pi5 NeoPixel for a single WS2812B.

    Uses the RP1 PIO peripheral on Raspberry Pi 5 via /dev/pio0.
    The rpi_ws281x library does NOT work on Pi 5 (error -3:
    "Hardware revision is not supported") because the Pi 5's RP1 chip
    replaced the BCM2711 DMA/PWM peripherals that rpi_ws281x relied on.
    """

    def __init__(self, gpio_pin, brightness):
        import board
        import neopixel

        pin = getattr(board, f"D{gpio_pin}")
        self._strip = neopixel.NeoPixel(
            pin, 1, auto_write=False, brightness=brightness / 255.0,
        )
        self._current = (0, 0, 0)

    def set_color(self, r, g, b):
        if (r, g, b) != self._current:
            self._strip[0] = (r, g, b)
            self._strip.show()
            self._current = (r, g, b)

    def set_brightness(self, brightness):
        self._strip.brightness = brightness / 255.0
        self._strip.show()

    def off(self):
        self.set_color(0, 0, 0)

    def cleanup(self):
        self.off()


# ---------------------------------------------------------------------------
# Health Checks
# ---------------------------------------------------------------------------

def _run(cmd, timeout=3):
    """Run a command, return (returncode, stdout). Swallow errors."""
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return -1, ""


def check_camera(camera_ip):
    """Check camera reachability and last capture result.

    Returns (has_error, is_blinking).
    Steady = camera unreachable. Blinking = capture failed.
    """
    if not camera_ip:
        return False, False  # no camera configured — not an error

    rc, _ = _run(["ping", "-c1", "-W1", camera_ip], timeout=3)
    if rc != 0:
        return True, False  # unreachable → steady

    # Camera reachable — check if last capture failed
    rc, out = _run(["systemctl", "show", "orc-capture", "-p", "Result"], timeout=3)
    if rc == 0 and "Result=exit-code" in out:
        return True, True  # capture failed → blinking

    return False, False


def check_network():
    """Check internet connectivity.

    Returns (has_error, is_blinking).
    Steady = no connectivity. Blinking = modem registered but no route.
    """
    rc, _ = _run(["ping", "-c1", "-W3", "8.8.8.8"], timeout=5)
    if rc == 0:
        return False, False  # internet reachable

    # No internet — check if modem is at least registered
    rc, out = _run(["mmcli", "-m", "0", "-J"], timeout=5)
    if rc == 0 and '"registered"' in out.lower():
        return True, True   # registered but no route → blinking

    return True, False      # modem down → steady


def check_storage(path="/home/pi/Videos", threshold_pct=90):
    """Check disk usage.

    Returns (has_error, is_blinking). Blinking not used for storage.
    """
    rc, out = _run(["df", "--output=pcent", path], timeout=2)
    if rc != 0:
        return True, False  # can't check → treat as error

    for line in out.strip().split("\n"):
        line = line.strip().rstrip("%")
        if line.isdigit():
            if int(line) >= threshold_pct:
                return True, False  # over threshold → steady
            return False, False

    return False, False


def check_power():
    """Check for undervoltage via vcgencmd.

    Returns (has_error, is_blinking). Blinking not used for power.
    Bit 0 of get_throttled = under-voltage detected right now.
    """
    rc, out = _run(["vcgencmd", "get_throttled"], timeout=2)
    if rc != 0:
        return False, False  # can't check — don't raise error

    # Output: throttled=0x50000 (hex)
    m = re.search(r'throttled=(0x[0-9a-fA-F]+)', out)
    if m:
        flags = int(m.group(1), 16)
        if flags & 0x1:  # bit 0 = under-voltage now
            return True, False
    return False, False


def is_maintenance_mode():
    """Check if the Pi is in maintenance mode (WiFi hotspot active)."""
    rc, _ = _run(["systemctl", "is-active", "hostapd"], timeout=2)
    return rc == 0


def is_capture_active():
    """Check if orc-capture is currently running."""
    rc, out = _run(["systemctl", "is-active", "orc-capture"], timeout=2)
    # "activating" also counts (oneshot in progress)
    return rc == 0 or "activating" in out


# ---------------------------------------------------------------------------
# Status Daemon
# ---------------------------------------------------------------------------

class StatusDaemon:
    """Main daemon: polls health, drives LED."""

    def __init__(self, config, led):
        self.cfg = config
        self.led = led
        self._shutting_down = False

        # State
        self._first_poll_done = False
        self._active_errors = []  # list of (name, color, is_blinking)
        self._in_maintenance = False
        self._in_capture = False

        # Error cycling
        self._cycle_index = 0
        self._cycle_time = 0.0

        # Timing
        self._poll_interval = config.get("poll_interval_s", 5)
        self._last_poll = 0.0

        # Resolve camera IP
        overrides = config.get("overrides") or {}
        self._camera_ip = overrides.get("camera_ip")
        if not self._camera_ip:
            orc_conf = parse_orc_capture_conf()
            self._camera_ip = orc_conf.get("CAMERA_IP")

        self._storage_path = overrides.get("storage_path", "/home/pi/Videos")
        self._storage_threshold = overrides.get("storage_threshold_pct", 90)

    def poll_subsystems(self):
        """Run all health checks and update internal state."""
        errors_cfg = self.cfg.get("errors", {})
        active = []

        checks = {
            "camera":  lambda: check_camera(self._camera_ip),
            "network": lambda: check_network(),
            "storage": lambda: check_storage(self._storage_path,
                                             self._storage_threshold),
            "power":   lambda: check_power(),
        }

        for name in ERROR_ORDER:
            ecfg = errors_cfg.get(name, {})
            if ecfg.get("suppressed", False):
                continue
            check_fn = checks.get(name)
            if not check_fn:
                continue
            has_error, is_blinking = check_fn()
            if has_error:
                color = tuple(ecfg.get("color", [255, 0, 0]))
                active.append((name, color, is_blinking))

        self._active_errors = active
        self._in_maintenance = is_maintenance_mode()
        self._in_capture = is_capture_active()
        self._first_poll_done = True

    def _get_display(self, now):
        """Determine (r, g, b, pattern, hz) for the current moment."""
        states = self.cfg.get("states", {})
        err_disp = self.cfg.get("error_display", {})
        blink_hz = err_disp.get("blink_hz", 4)
        cycle_s = err_disp.get("cycle_interval_s", 3)

        # Boot (before first poll)
        if not self._first_poll_done:
            s = states.get("boot", {})
            c = s.get("color", [255, 255, 255])
            return c[0], c[1], c[2], "solid", 0

        # Priority 1: Maintenance
        if self._in_maintenance:
            s = states.get("maintenance", {})
            c = s.get("color", [0, 255, 255])
            return c[0], c[1], c[2], "solid", 0

        # Priority 2: Capture in progress
        if self._in_capture:
            s = states.get("capture", {})
            c = s.get("color", [0, 255, 0])
            return c[0], c[1], c[2], "flash", s.get("flash_hz", 2)

        # Priority 3: Errors
        if self._active_errors:
            # Advance cycle if needed
            if now - self._cycle_time >= cycle_s:
                self._cycle_index = ((self._cycle_index + 1)
                                     % len(self._active_errors))
                self._cycle_time = now

            idx = self._cycle_index % len(self._active_errors)
            name, color, is_blinking = self._active_errors[idx]
            pattern = "flash" if is_blinking else "solid"
            hz = blink_hz if is_blinking else 0
            return color[0], color[1], color[2], pattern, hz

        # Priority 4: Idle
        s = states.get("idle", {})
        c = s.get("color", [0, 255, 0])
        return c[0], c[1], c[2], "solid", 0

    def run(self):
        """Main loop. Runs until SIGTERM."""
        log("Starting LED status daemon")
        log(f"Config: GPIO {self.cfg['led']['gpio_pin']}, "
            f"brightness {self.cfg['led']['brightness']}, "
            f"poll every {self._poll_interval}s")
        log(f"Camera IP: {self._camera_ip or '(none)'}")

        suppressed = [name for name in ERROR_ORDER
                      if self.cfg.get("errors", {}).get(name, {})
                      .get("suppressed", False)]
        if suppressed:
            log(f"Suppressed errors: {', '.join(suppressed)}")

        while not self._shutting_down:
            now = time.monotonic()

            # Poll if due
            if now - self._last_poll >= self._poll_interval:
                self._last_poll = now
                try:
                    self.poll_subsystems()
                except Exception as e:
                    log(f"Poll error: {e}")

                # Reset cycle when error list changes
                if self._active_errors:
                    if self._cycle_index >= len(self._active_errors):
                        self._cycle_index = 0
                        self._cycle_time = now

            # Determine display
            r, g, b, pattern, hz = self._get_display(now)

            # Apply pattern
            if pattern == "flash" and hz > 0:
                period = 1.0 / hz
                phase = (now % period) / period
                if phase < 0.5:
                    self.led.set_color(r, g, b)
                else:
                    self.led.set_color(0, 0, 0)
            elif pattern == "pulse":
                # Sinusoidal brightness for shutdown
                bright = (math.sin(now * 2 * math.pi * 0.5) + 1) / 2
                self.led.set_color(
                    int(r * bright), int(g * bright), int(b * bright))
            else:
                self.led.set_color(r, g, b)

            time.sleep(TICK_PERIOD)

    def shutdown(self, signum=None, frame=None):
        """Handle SIGTERM/SIGINT: brief pulse, then LED off."""
        if self._shutting_down:
            return
        self._shutting_down = True
        log(f"Received signal {signum}, shutting down")

        # Brief green pulse (0.6s)
        s = self.cfg.get("states", {}).get("shutdown", {})
        c = s.get("color", [0, 255, 0])
        start = time.monotonic()
        while time.monotonic() - start < 0.6:
            elapsed = time.monotonic() - start
            bright = (math.sin(elapsed * 2 * math.pi * 1.5) + 1) / 2
            self.led.set_color(
                int(c[0] * bright), int(c[1] * bright), int(c[2] * bright))
            time.sleep(TICK_PERIOD)

        self.led.cleanup()
        log("LED off, exiting")


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def log(msg):
    """Log with timestamp (captured by systemd journal)."""
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"{ts} [orc-led-status] {msg}", flush=True)


# ---------------------------------------------------------------------------
# CLI: --test-color
# ---------------------------------------------------------------------------

def test_color(args, config):
    """Set a static color for 5 seconds, then turn off. For wiring tests.
    Prefer orc-led-test for comprehensive testing."""
    r, g, b = args.test_color
    led_cfg = config.get("led", {})
    led = LedDriver(led_cfg.get("gpio_pin", 18),
                     led_cfg.get("brightness", 200))
    log(f"Test color: ({r}, {g}, {b}) for 5 seconds")
    led.set_color(r, g, b)
    time.sleep(5)
    led.cleanup()
    log("Test complete")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="WS2812B LED status indicator daemon")
    parser.add_argument(
        "--config", default=os.environ.get("ORC_LED_STATUS_CONF", DEFAULT_CONF),
        help="Path to YAML config file")
    parser.add_argument(
        "--test-color", nargs=3, type=int, metavar=("R", "G", "B"),
        help="Set a static color for 5 seconds (wiring test), then exit")
    parser.add_argument(
        "--off", action="store_true",
        help="Turn the LED off and exit (used as systemd ExecStopPost backstop)")
    args = parser.parse_args()

    config = load_config(args.config)

    if args.off:
        led_cfg = config.get("led", {})
        led = LedDriver(led_cfg.get("gpio_pin", 18),
                         led_cfg.get("brightness", 200))
        led.off()
        log("LED off")
        return

    if args.test_color:
        test_color(args, config)
        return

    led_cfg = config.get("led", {})
    led = LedDriver(led_cfg.get("gpio_pin", 18),
                     led_cfg.get("brightness", 200))

    daemon = StatusDaemon(config, led)

    signal.signal(signal.SIGTERM, daemon.shutdown)
    signal.signal(signal.SIGINT, daemon.shutdown)

    # Show boot state immediately
    boot = config.get("states", {}).get("boot", {})
    c = boot.get("color", [255, 255, 255])
    led.set_color(c[0], c[1], c[2])

    try:
        daemon.run()
    except Exception as e:
        log(f"Fatal error: {e}")
        led.cleanup()
        sys.exit(1)


if __name__ == "__main__":
    main()
