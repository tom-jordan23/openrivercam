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
| `modemmanager` | LTE modem management (Quectel EG25-G) | Cellular data | Pulls libqmi-utils, libmbim-utils as dependencies |
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

## Already in Base Image (no action needed)

These are provided by Raspberry Pi OS or the ORC-OS image:

- `pinctrl` — GPIO control (Pi 5 recommended tool, part of raspi-utils)
- `NetworkManager` — network configuration
- `ip` / `iproute2` — network diagnostics
- `ssh` / `openssh-server` — remote access
- Python 3, pip
