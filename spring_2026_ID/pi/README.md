# Pi Configuration Files

Source of truth for all Raspberry Pi customizations applied on top of the
Rainbow Sensing ORC-OS base image. For base image flashing and initial setup,
follow the [ORC-OS README](https://github.com/localdevices/ORC-OS/blob/main/README.md).
Files here are manually copied to each Pi **after** the base image setup is
complete — there is no automated deployment.

## Package Manifest

See [PACKAGES.md](PACKAGES.md) for system and Python packages that must be
installed on top of the base image.

## Layout Convention

Files are stored under the **filesystem path they occupy on the Pi**, relative
to `/`. The top level splits into `shared/` (all sites) and per-site
directories:

```
pi/
├── shared/          # Files identical across ALL ORC sites
│   └── etc/
│       └── ...
├── sukabumi/        # Sukabumi site-specific files
│   └── etc/
│       └── ...
└── jakarta/         # Jakarta site-specific files
    └── etc/
        └── ...
```

Example: `pi/sukabumi/etc/dnsmasq.d/cameras.conf` → goes to
`/etc/dnsmasq.d/cameras.conf` on the Sukabumi Pi.

If a file exists in both `shared/` and a site directory, the **site version
wins**. In practice this means you copy `shared/` files first, then overwrite
with site-specific files.

### .gitkeep files

Empty directories aren't tracked by git. The `.gitkeep` files are zero-byte
placeholders that force git to preserve the directory structure. They have no
effect on the Pi — do not copy them. Delete a `.gitkeep` once the directory
contains a real file.

## File Inventory

<!-- Update this table whenever you add or remove a file. -->

| Repo path | Pi path | Description | Shared / Site | Credentials? | Upstream candidate? |
|-----------|---------|-------------|---------------|:------------:|:-------------------:|
| `shared/etc/dnsmasq.d/maintenance.conf` | `/etc/dnsmasq.d/maintenance.conf` | DHCP server for camera PoE network on eth0 | Shared | No | No |
| `shared/usr/local/bin/poe-relay` | `/usr/local/bin/poe-relay` | Control PoE switch relay (on/off/status) via GPIO 24 | Shared | No | No |
| `shared/usr/local/bin/orc-capture` | `/usr/local/bin/orc-capture` | Capture 5s video from PoE camera via RTSP with quality gate | Shared | No | Yes |
| `shared/usr/local/bin/orc-preflight` | `/usr/local/bin/orc-preflight` | Thin wrapper: runs `deploy.sh <site> --check` (auto-detects site from hostname) | Shared | No | No |
| `shared/etc/systemd/system/orc-capture.service` | `/etc/systemd/system/orc-capture.service` | Oneshot service: runs orc-capture on each boot (conflicts with orc-gpio-relays) | Shared | No | No |
| `shared/etc/orc-sensors/sht40.conf` | `/etc/orc-sensors/sht40.conf` | SHT40 sensor config (I2C addr, interval, log dir, CSV columns) | Shared | No | Yes |
| `shared/usr/local/bin/orc-sensors` | `/usr/local/bin/orc-sensors` | Wrapper: sources per-sensor configs, execs into Python logger | Shared | No | Yes |
| `shared/usr/local/lib/orc-sensors/sensors_logger.py` | `/usr/local/lib/orc-sensors/sensors_logger.py` | Multi-sensor reader: I2C read, CRC validation, CSV append, log rotation | Shared | No | Yes |
| `shared/etc/systemd/system/orc-sensors.service` | `/etc/systemd/system/orc-sensors.service` | Oneshot service: reads all due sensors and appends to daily CSVs | Shared | No | Yes |
| `shared/etc/systemd/system/orc-sensors.timer` | `/etc/systemd/system/orc-sensors.timer` | Timer: ticks every 60s, per-sensor interval checked in Python | Shared | No | Yes |
| `shared/update-motd.d/30-camera-status` | `/etc/update-motd.d/30-camera-status` | Dynamic MOTD: relay status, Witty Pi 5 RTC/temp/voltage, eth0 IP, camera reachability | Shared | No | No |
| `shared/update-motd.d/40-power-management` | `/etc/update-motd.d/40-power-management` | Dynamic MOTD: ORC-OS shutdown/reboot settings, Witty Pi 5 wake schedule, how to change | Shared | No | No |
| `shared/update-motd.d/20-led-status` | `/etc/update-motd.d/20-led-status` | Dynamic MOTD: LED service status, compact color guide | Shared | No | No |
| `shared/update-motd.d/90-links` | `/etc/update-motd.d/90-links` | Dynamic MOTD: quick reference links (ORC-OS URL, camera, commands) | Shared | No | No |
| `shared/etc/chrony/conf.d/camera-net.conf` | `/etc/chrony/conf.d/camera-net.conf` | NTP server for camera network (Pi serves time to cameras) | Shared | No | Yes |
| `shared/etc/orc-capture.conf` | `/etc/orc-capture.conf` | Capture settings template with all options documented (overridden by site-specific versions) | Shared (template) | No | No |
| `sukabumi/etc/orc-capture.conf` | `/etc/orc-capture.conf` | Sukabumi capture config: RELAY_MODE=cycle, CAMERA_IP=192.168.50.139 | Sukabumi | No | No |
| `jakarta/etc/orc-capture.conf` | `/etc/orc-capture.conf` | Jakarta capture config: RELAY_MODE=always, CAMERA_IP=192.168.50.101 | Jakarta | No | No |
| `jakarta/etc/NetworkManager/system-connections/camera-net.nmconnection` | `/etc/NetworkManager/system-connections/camera-net.nmconnection` | Static IP (192.168.50.1) for eth0 camera network | Jakarta | No | No |
| `jakarta/etc/cloud/templates/hosts.debian.tmpl` | `/etc/cloud/templates/hosts.debian.tmpl` | Hosts file template with camera hostname | Jakarta | No | No |
| `jakarta/etc/dnsmasq.d/cameras.conf` | `/etc/dnsmasq.d/cameras.conf` | Jakarta camera DHCP reservation (MAC placeholder) | Jakarta | Yes (MAC) | No |
| `shared/usr/local/bin/orc-led-status` | `/usr/local/bin/orc-led-status` | Bash wrapper for LED status daemon (validates config, execs Python) | Shared | No | Yes |
| `shared/usr/local/lib/orc-led-status/led_status.py` | `/usr/local/lib/orc-led-status/led_status.py` | LED status daemon: polls health, drives WS2812B on GPIO 18 via RP1 PIO | Shared | No | Yes |
| `shared/usr/local/bin/orc-led-test` | `/usr/local/bin/orc-led-test` | LED hardware test: cycles all status colors/patterns for visual verification | Shared | No | Yes |
| `shared/etc/systemd/system/orc-led-status.service` | `/etc/systemd/system/orc-led-status.service` | Simple service: long-running LED daemon (requires root for /dev/pio0) | Shared | No | Yes |
| `shared/etc/orc/led-status.yaml` | `/etc/orc/led-status.yaml` | LED status config: colors, patterns, error suppression, GPIO pin | Shared | No | Yes |
| `sukabumi/etc/cloud/templates/hosts.debian.tmpl` | `/etc/cloud/templates/hosts.debian.tmpl` | Hosts file template with camera hostname | Sukabumi | No | No |
| `sukabumi/etc/NetworkManager/system-connections/camera-net.nmconnection` | `/etc/NetworkManager/system-connections/camera-net.nmconnection` | Static IP (192.168.50.1) for eth0 camera network | Sukabumi | No | No |

**Column guide:**
- **Credentials?** — Yes if the file contains passwords, keys, or secrets that
  must be filled in after copying to the Pi. Tracked files use placeholders
  (e.g. `<CAMERA_PASSWORD>`); real values are never committed.
- **Upstream candidate?** — Yes if this file should be submitted to Rainbow
  Sensing for inclusion in future base images.

## How to Apply

### Automated (recommended): deploy.sh

The `deploy.sh` script is the single source of truth for station configuration.
It always checks the full system state first (102 checks across packages, files,
services, hardware, network), then prompts before applying any fixes. It replaces
both the old deploy script and the old orc-preflight tool.

**Workflow:**

1. Flash ORC-OS image with Pi Imager:
   - Device: Raspberry Pi 5
   - OS: Use custom → select the ORC-OS `.img.gz` file
   - Click the gear icon (OS customisation) and set:
     - **Hostname:** `orc-sukabumi` or `orc-jakarta`
     - **Username:** `pi` (do NOT change — ORC-OS requires this)
     - **Enable SSH:** Yes (password authentication or public key)
     - **Configure WiFi:** Yes — enter your SSID and password
       (needed for initial setup; field deployment uses LTE)
   - Flash to SD card
2. Insert SD card into Pi, power on
3. First boot — wait 2-3 minutes for ORC-OS init (filesystem expand, auto-reboot)
4. SSH into the Pi: `ssh pi@orc-jakarta.local` (or use IP from router)
5. Clone or copy this repo to the Pi
6. Run deploy.sh:

```bash
cd spring_2026_ID/pi
./deploy.sh sukabumi      # or: ./deploy.sh jakarta
```

**Options:**
```
./deploy.sh <site> --check            # check only, no fixes (replaces orc-preflight)
./deploy.sh <site> --yes              # apply fixes without prompting
./deploy.sh <site> --skip-packages    # skip apt/pip checks (offline/air-gapped)
./deploy.sh <site> --skip-config-txt  # skip config.txt checks
```

You can also run `orc-preflight` from anywhere — it auto-detects the site
from the hostname and runs `deploy.sh <site> --check`.

The script creates a backup of modified files at
`/tmp/orc-deploy-backup-<timestamp>/` and a report at
`/tmp/orc-deploy-report-<timestamp>.txt`.

### Manual (single file updates)

For updating individual files after the initial deploy:

```bash
# From the repo root — replace PI_HOST with the Pi's IP or hostname
scp spring_2026_ID/pi/shared/usr/local/bin/orc-capture PI_HOST:/tmp/
ssh PI_HOST 'sudo cp /tmp/orc-capture /usr/local/bin/ && sudo chmod +x /usr/local/bin/orc-capture && rm /tmp/orc-capture'
```

## How to Add a New File

1. Create the file under the correct path:
   - `shared/` if it applies to all sites
   - `sukabumi/` or `jakarta/` if site-specific
   - Mirror the on-Pi filesystem path (e.g. a file that goes to
     `/etc/foo/bar.conf` → `pi/shared/etc/foo/bar.conf`)
2. If the file contains credentials, use placeholders (`<CAMERA_PASSWORD>`,
   `<ADMIN_KEY>`, etc.) and note it in the inventory table.
3. Update the **File Inventory** table above.
4. Commit.

## Credentials Policy

Real passwords and secrets are **never committed**. Files that need credentials
use obvious placeholders. After copying a file to the Pi, replace placeholders
with real values in-place:

```bash
ssh PI_HOST 'sudo sed -i "s/<CAMERA_PASSWORD>/actual_password/" /etc/some/config'
```

If a local-only variant is ever needed, use the `*.local` suffix (e.g.
`cameras.conf.local`) — these are gitignored.

## Rainbow Sensing Upstream

Files in `shared/` that would benefit all ORC-OS deployments are
candidates for upstream inclusion. The **Upstream candidate?** column in the
inventory table tracks which files to submit.

| File | Status | Notes |
|------|--------|-------|
| *(none yet)* | | |

When submitting upstream, include the rationale (what problem it solves, what
it replaces in the base image) so Rainbow Sensing can evaluate.
