#!/usr/bin/env python3
"""sensors_logger.py — read configured sensors and append to daily CSVs.

Called by /usr/local/bin/orc-sensors on each timer tick. For each sensor
config in the config directory:
  1. Check if the sensor's interval has elapsed since its last reading
  2. If due, read the sensor and append a row to its daily CSV
  3. Rotate old CSV files past the retention window

Each sensor gets its own CSV with its own columns and schedule.
"""

import os
import sys
import time
import glob as globmod
from datetime import datetime, timedelta
from pathlib import Path

TAG = "[orc-sensors]"
CONFIG_DIR = os.environ.get("ORC_SENSORS_CONF_DIR", "/etc/orc-sensors")


def log(msg):
    print(f"{datetime.now():%Y-%m-%d %H:%M:%S} {TAG} {msg}", flush=True)


def err(msg):
    print(f"{datetime.now():%Y-%m-%d %H:%M:%S} {TAG} ERROR: {msg}",
          file=sys.stderr, flush=True)


# ─── Config parsing ──────────────────────────────────────────────────

def parse_conf(path):
    """Parse a bash-style KEY=VALUE config file into a dict."""
    conf = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, _, val = line.partition("=")
            # Strip inline comments and surrounding quotes
            val = val.split("#")[0].strip().strip('"').strip("'")
            conf[key.strip()] = val
    return conf


# ─── Interval check ─────────────────────────────────────────────────

def is_due(log_dir, label, interval_sec):
    """Check if enough time has passed since the last CSV entry."""
    today = datetime.now().strftime("%Y-%m-%d")
    csv_path = os.path.join(log_dir, f"{label}_{today}.csv")

    if not os.path.exists(csv_path):
        return True

    # Read the last line's timestamp
    try:
        with open(csv_path, "rb") as f:
            # Seek to end, scan backwards for last newline
            f.seek(0, 2)
            size = f.tell()
            if size < 10:
                return True
            # Read last 256 bytes (more than enough for one CSV row)
            f.seek(max(0, size - 256))
            chunk = f.read().decode("utf-8", errors="replace")

        lines = chunk.strip().split("\n")
        last_line = lines[-1]
        if last_line.startswith("timestamp"):
            return True  # only header exists

        last_ts_str = last_line.split(",")[0]
        last_ts = datetime.fromisoformat(last_ts_str)
        elapsed = (datetime.now().astimezone() - last_ts).total_seconds()
        # Allow 10% early to avoid drift accumulation
        return elapsed >= (interval_sec * 0.9)
    except Exception:
        return True


# ─── CRC-8 (Sensirion standard: polynomial 0x31, init 0xFF) ─────────

def crc8(data):
    crc = 0xFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x80:
                crc = (crc << 1) ^ 0x31
            else:
                crc = crc << 1
            crc &= 0xFF
    return crc


# ─── Sensor drivers ──────────────────────────────────────────────────
# Each driver returns a dict of column_name: value.
# Add new sensor types here as functions named read_<SENSOR_TYPE>.

def read_sht40(conf):
    """Read SHT40 temperature/humidity via I2C. Returns dict."""
    from smbus2 import SMBus, i2c_msg

    bus_num = int(conf.get("I2C_BUS", "1"))
    addr = int(conf.get("I2C_ADDR", "0x44"), 0)

    bus = SMBus(bus_num)
    try:
        write = i2c_msg.write(addr, [0xFD])
        bus.i2c_rdwr(write)
        time.sleep(0.05)

        read = i2c_msg.read(addr, 6)
        bus.i2c_rdwr(read)
        data = list(read)
    finally:
        bus.close()

    if crc8(data[0:2]) != data[2]:
        raise ValueError(
            f"CRC mismatch on temperature: expected {crc8(data[0:2]):#x}, "
            f"got {data[2]:#x} (raw: {data})")
    if crc8(data[3:5]) != data[5]:
        raise ValueError(
            f"CRC mismatch on humidity: expected {crc8(data[3:5]):#x}, "
            f"got {data[5]:#x} (raw: {data})")

    t_raw = (data[0] << 8) | data[1]
    h_raw = (data[3] << 8) | data[4]

    temp_c = round(-45.0 + 175.0 * t_raw / 65535.0, 2)
    humidity_pct = round(max(0.0, min(100.0, -6.0 + 125.0 * h_raw / 65535.0)), 1)

    return {"temp_c": temp_c, "humidity_pct": humidity_pct}


def read_rg15(conf):
    """Read Hydreon RG-15 rain gauge via UART. Returns dict.

    Forces polling mode ('P'), then requests a reading ('R') and parses
    TotalAcc (lifetime rainfall in EEPROM — survives power cycles and 'A'
    resets, unlike Acc). Interval rainfall is the delta against the last
    TotalAcc saved to disk.

    Response format: "Acc 0.01 mm, EventAcc 0.01 mm, TotalAcc 0.01 mm, RInt 0.00 mmph"
    """
    import serial

    port = conf.get("SERIAL_PORT", "/dev/ttyAMA0")
    baud = int(conf.get("SERIAL_BAUD", "9600"))
    state_file = conf.get("STATE_FILE", "/var/lib/orc-sensors/rg15_totalacc.txt")

    os.makedirs(os.path.dirname(state_file), exist_ok=True)

    prev_total = None
    if os.path.exists(state_file):
        try:
            with open(state_file) as f:
                prev_total = float(f.read().strip())
        except (ValueError, OSError):
            prev_total = None

    ser = serial.Serial(port, baud, timeout=3)
    try:
        # Drain any unsolicited bytes (in case gauge is in continuous mode)
        time.sleep(0.1)
        if ser.in_waiting:
            ser.read(ser.in_waiting)

        # Force polling mode (idempotent; prevents data loss from continuous mode)
        ser.write(b"P\n")
        time.sleep(0.3)
        if ser.in_waiting:
            ser.read(ser.in_waiting)

        ser.write(b"R\n")
        time.sleep(0.6)
        response = ser.read(512).decode("ascii", errors="replace").strip()
    finally:
        ser.close()

    if not response:
        raise ValueError(f"No response from RG-15 on {port}")

    # Parse TotalAcc with exact token match (Acc/EventAcc/TotalAcc all start with "Acc")
    total_mm = None
    for part in response.split(","):
        tokens = part.strip().split()
        if tokens and tokens[0] == "TotalAcc":
            for tok in tokens[1:]:
                try:
                    total_mm = float(tok)
                    break
                except ValueError:
                    continue
            break

    if total_mm is None:
        raise ValueError(f"Could not parse TotalAcc from RG-15 response: {response}")

    # First read ever: no delta available, treat interval as 0
    if prev_total is None:
        interval_mm = 0.0
    elif total_mm < prev_total:
        # TotalAcc should never decrease; if it does, treat as unrecoverable discontinuity
        interval_mm = 0.0
    else:
        interval_mm = round(total_mm - prev_total, 2)

    with open(state_file, "w") as f:
        f.write(str(total_mm))

    return {
        "totalacc_mm": total_mm,
        "interval_mm": interval_mm,
    }


def read_ds18b20(conf):
    """Read DS18B20 1-Wire temperature probe. Returns dict.

    Reads from sysfs: /sys/bus/w1/devices/<device_id>/temperature
    The kernel returns temperature in millidegrees Celsius.
    """
    device_id = conf.get("W1_DEVICE_ID", "")

    if not device_id:
        # Auto-detect: find the first 28-* device
        w1_dir = "/sys/bus/w1/devices"
        if os.path.isdir(w1_dir):
            for entry in os.listdir(w1_dir):
                if entry.startswith("28-"):
                    device_id = entry
                    break

    if not device_id:
        raise ValueError("No DS18B20 device found (no 28-* in /sys/bus/w1/devices/)")

    temp_path = f"/sys/bus/w1/devices/{device_id}/temperature"
    if not os.path.exists(temp_path):
        raise ValueError(f"DS18B20 sysfs path not found: {temp_path}")

    with open(temp_path) as f:
        raw = f.read().strip()

    temp_c = round(int(raw) / 1000.0, 2)

    return {"temp_c": temp_c}


# Registry of sensor drivers
DRIVERS = {
    "sht40": read_sht40,
    "rg15": read_rg15,
    "ds18b20": read_ds18b20,
}


# ─── CSV write ───────────────────────────────────────────────────────

def append_csv(log_dir, label, header, values):
    """Append a reading to today's CSV file, creating header if new."""
    today = datetime.now().strftime("%Y-%m-%d")
    csv_path = os.path.join(log_dir, f"{label}_{today}.csv")

    write_header = not os.path.exists(csv_path)

    with open(csv_path, "a") as f:
        if write_header:
            f.write(header + "\n")
        ts = datetime.now().astimezone().isoformat()
        # Build row from header columns (skip "timestamp", it's first)
        cols = [c.strip() for c in header.split(",")]
        row_parts = [ts]
        for col in cols[1:]:
            row_parts.append(str(values.get(col, "")))
        f.write(",".join(row_parts) + "\n")

    return csv_path


# ─── Log rotation ────────────────────────────────────────────────────

def rotate_logs(log_dir, label, keep_days):
    """Delete <label>_*.csv files older than keep_days."""
    cutoff = datetime.now() - timedelta(days=keep_days)
    pattern = os.path.join(log_dir, f"{label}_*.csv")

    for path in globmod.glob(pattern):
        fname = os.path.basename(path)
        try:
            date_str = fname.replace(f"{label}_", "").replace(".csv", "")
            file_date = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            continue
        if file_date < cutoff:
            os.remove(path)
            log(f"rotated {fname}")


# ─── Process one sensor ─────────────────────────────────────────────

def process_sensor(conf_path):
    """Load config, check interval, read sensor, write CSV."""
    conf = parse_conf(conf_path)
    sensor_type = conf.get("SENSOR_TYPE", "")
    label = conf.get("SENSOR_LABEL", sensor_type)
    log_dir = conf.get("LOG_DIR", "/var/log/orc/sensors")
    interval = int(conf.get("INTERVAL_SEC", "300"))
    rotate_days = int(conf.get("LOG_ROTATE_DAYS", "30"))
    header = conf.get("CSV_HEADER", "timestamp")

    if sensor_type not in DRIVERS:
        err(f"{conf_path}: unknown SENSOR_TYPE '{sensor_type}'")
        return False

    if not is_due(log_dir, label, interval):
        return True  # not due yet, not an error

    os.makedirs(log_dir, exist_ok=True)

    values = DRIVERS[sensor_type](conf)
    csv_path = append_csv(log_dir, label, header, values)

    # Format values for log line
    parts = [f"{k}={v}" for k, v in values.items()]
    log(f"{label}: {', '.join(parts)} → {csv_path}")

    rotate_logs(log_dir, label, rotate_days)
    return True


# ─── Main ────────────────────────────────────────────────────────────

def main():
    conf_files = sorted(globmod.glob(os.path.join(CONFIG_DIR, "*.conf")))
    if not conf_files:
        err(f"no config files found in {CONFIG_DIR}")
        sys.exit(1)

    errors = 0
    for conf_path in conf_files:
        try:
            process_sensor(conf_path)
        except Exception as e:
            err(f"{os.path.basename(conf_path)}: {e}")
            errors += 1

    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
