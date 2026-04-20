# Package Manifest

Packages installed on top of the Rainbow Sensing ORC-OS base image.
The base image already includes Raspberry Pi OS defaults (`pinctrl`, `ip`,
`NetworkManager`, etc.) plus ORC-specific Python libraries.

Update this file whenever you `apt install` or `pip install` something
that the base image does not provide.

## System Packages (apt)

| Package | Purpose | Required by | Notes |
|---------|---------|-------------|-------|
| `dnsmasq` | DHCP server for camera PoE network on eth0 | Camera network | Assigns IP to camera on 192.168.50.0/24 subnet |
| `modemmanager` | LTE modem management (Huawei ME906s deployed; Quectel EG25-G spare) | Cellular data | Pulls libqmi-utils, libmbim-utils as dependencies |
| `gpiod` | GPIO tools (`gpioset`, `gpioget`) for relay/LED control | Relay control, LED testing | Also installs `python3-libgpiod` |
| `minicom` | Serial terminal for modem/rain gauge diagnostics | Debugging only | Optional — only needed for manual AT commands or UART testing |
| `chrony` | NTP server for camera time sync | Camera network | Pi serves NTP to cameras on isolated 192.168.50.0/24 network |
| `ffmpeg` | Video capture and transcoding | orc-capture | RTSP capture from camera, quality validation via ffprobe |

## Python Packages (pip)

| Package | Purpose | Required by | Notes |
|---------|---------|-------------|-------|
| `requests` | HTTP client for camera ISAPI configuration | `camera/camtool.py` | May already be in base image |
| `pyserial` | Serial port access for modem AT commands | Modem diagnostics | Optional — only for manual diagnostics |
| `smbus2` | I2C interface for SHT40 temp/humidity sensor | Sensor readout | |
| `adafruit-blinka` | Hardware abstraction layer for Pi GPIO | `orc-led-status` | Dependency of NeoPixel library |
| `adafruit-circuitpython-neopixel` | NeoPixel high-level API (`import neopixel`) | `orc-led-status` | The API code imports. Blinka auto-detects Pi 5 |
| `adafruit-blinka-raspberry-pi5-neopixel` | Pi 5 RP1 PIO backend for NeoPixel | `orc-led-status` | Auto-loaded by Blinka on Pi 5 via /dev/pio0. Replaces rpi-ws281x which does NOT work on Pi 5 |
| `pyyaml` | YAML config parser | `orc-led-status` | May already be in base image |

## Install Script

```bash
# System packages
sudo apt update
sudo apt install -y dnsmasq modemmanager gpiod minicom chrony

# Python packages
pip install requests pyserial smbus2 pyyaml

# LED status service (requires sudo for RP1 PIO access)
# NOTE: rpi-ws281x does NOT work on Pi 5 (error -3: "Hardware revision
# is not supported"). The Pi 5 RP1 chip replaced BCM2711 DMA/PWM.
# Use the Adafruit Blinka Pi5 NeoPixel library instead.
sudo pip install --break-system-packages adafruit-blinka adafruit-circuitpython-neopixel adafruit-blinka-raspberry-pi5-neopixel
```

## User/Group Setup

```bash
# Add the ORC user to dialout group for serial/modem access
sudo usermod -aG dialout $USER
```

## Witty Pi 5 HAT+ Software (wp5)

Installed via `deploy.sh` Phase 6b. Replaces the Pi 5 native RTC (ML-2020
battery connector failed on both boards).

- **Package:** `wp5_latest.deb` from https://www.uugear.com/repo/WittyPi5/
- **Command:** `wp5` (interactive CLI for RTC sync, scheduling, power config)
- **Daemon:** `wp5d.service` (auto-starts at boot, syncs RTC → system clock)
- **Poweroff hook:** `wp5d_poweroff.service` (informs Witty Pi when Pi halts)
- **Reboot hook:** `wp5d_reboot.service` (informs Witty Pi on reboot)
- **I2C address:** 0x51 (no GPIO pins consumed)
- **RTC backup:** CR2032 coin cell on HAT board
- **Schedule files:** Stored on Witty Pi 5 onboard flash (16MB), managed via
  `wp5` menu option 6 (choose schedule) and Admin → option 7 (load/generate)
- **Native RTC service:** `orc-rpi5-power-management.service` is disabled by
  deploy.sh (Pi 5 ML-2020 RTC has no battery backup)

## Already in Base Image (no action needed)

These are provided by Raspberry Pi OS or the ORC-OS image:

- `pinctrl` — GPIO control (Pi 5 recommended tool, part of raspi-utils)
- `NetworkManager` — network configuration
- `ip` / `iproute2` — network diagnostics
- `ssh` / `openssh-server` — remote access
- Python 3, pip
