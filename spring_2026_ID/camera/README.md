# Camera Configuration Management

## What This Is

The ANNKE C1200 PoE cameras at both Indonesia ORC sites are Hikvision OEM
devices (G6 platform). Like all Hikvision cameras, they expose every setting
through **ISAPI** — an HTTP REST API with XML payloads and HTTP Digest Auth.
Any setting you can change in the camera's web GUI can also be read with GET
and written with PUT against an ISAPI endpoint.

This directory stores camera configurations as XML files in git and provides
a CLI tool (`camtool.py`) to push, pull, diff, and verify them against
live cameras. The goal is reproducible, reviewable, recoverable camera config:

- **Reproducible:** Push the same config to a replacement camera in minutes
- **Reviewable:** Config changes show up as git diffs
- **Recoverable:** Factory reset? Just push from git

## Why Not Just Use the Web GUI?

The web GUI works for one-off changes, but it doesn't help when you need to:

- Configure a replacement camera identically to the one it replaces
- Know exactly what changed between two site visits
- Ensure all three cameras share the same baseline settings
- Recover from a factory reset without a manual checklist

## How It Relates to `pi/`

This follows the same layered pattern as the Pi configuration files in `pi/`:

| System | Tool | Storage Pattern |
|--------|------|----------------|
| Pi OS (dnsmasq, network, services) | Manual scp | `pi/shared/` → `pi/<site>/` |
| Camera (encoding, image, OSD, time) | `camtool.py` | `camera/common/` → `camera/<site>/<cam>/` |

Both use the same principle: shared baseline configs that can be overridden
per-site or per-device. Both keep credentials out of git using placeholders.

Camera IPs in `cameras.json` must match the DHCP reservations configured
in the Pi's dnsmasq (`pi/shared/etc/dnsmasq.d/maintenance.conf`).

---

## Quick Start

```bash
cd spring_2026_ID/camera/

# 1. Provide camera password (pick one method)
export CAMERA_PASSWORD=yourpassword
# or: echo "CAMERA_PASSWORD=yourpassword" > .env   (gitignored)

# 2. Verify connectivity
python3 camtool.py info sukabumi-cam1

# 3. Pull live config into git
python3 camtool.py pull sukabumi-cam1

# 4. Review pulled XML, edit as needed, commit

# 5. Check for drift later
python3 camtool.py diff sukabumi-cam1
```

### Dependencies

- Python 3.9+ (Pi OS Bookworm ships 3.11)
- `requests` (`pip install requests`)

No other dependencies. The tool runs from the Pi itself or any machine
with network access to the cameras.

---

## Directory Layout

```
camera/
├── camtool.py              # CLI tool
├── cameras.json            # Camera inventory (name → IP, site, username)
├── .env                    # Camera password (gitignored, not committed)
│
├── backups/                # Auto-created pre-push backups (gitignored)
│   └── <camera>/<YYYYMMDD_HHMMSS>/
│       └── <endpoint>.xml
│
├── common/                 # Baseline configs shared by ALL cameras
│   ├── streaming_101.xml   # Main stream: codec, resolution, FPS, bitrate
│   ├── streaming_102.xml   # Sub stream: lower-res preview
│   ├── image.xml           # Brightness, contrast, saturation, WDR
│   ├── ircutfilter.xml     # Day/night IR cut filter mode (auto)
│   ├── ispmode.xml         # IR LED mode (auto/on/off)
│   ├── time.xml            # Timezone (WIB, UTC+7)
│   ├── ntp.xml             # NTP server config
│   └── motion_detection.xml # Motion detection (disabled)
│
├── sukabumi/
│   └── cam1/               # Inherits common/ — overrides added as needed
│
└── jakarta/
    ├── cam1/
    │   └── overlays.xml    # OSD text: "ORC Jakarta - Cam 1 Upstream"
    └── cam2/
        └── overlays.xml    # OSD text: "ORC Jakarta - Cam 2 Downstream"
```

### About the XML stubs

The files in `common/` are **placeholder stubs** with approximate structure.
The real XML schemas come from the camera firmware and vary by version. The
intended workflow is:

1. Run `camtool.py pull` against a live camera
2. Review the pulled XML (now contains the camera's actual schema)
3. Edit values to your desired settings
4. Move shared settings to `common/`, keep camera-specific ones in the site dir
5. Commit

---

## Config Layering

For a given camera and endpoint, the tool resolves which XML file to use:

1. **Camera-specific** — `<site>/<camera>/<endpoint>.xml` (wins if present)
2. **Common baseline** — `common/<endpoint>.xml` (fallback)
3. Skip with warning if neither exists

**Example:** For `jakarta-cam1` and endpoint `streaming_101`:
- Checks `jakarta/cam1/streaming_101.xml` — not found
- Falls back to `common/streaming_101.xml` — uses this

For `jakarta-cam1` and endpoint `overlays`:
- Checks `jakarta/cam1/overlays.xml` — found, uses it

`pull` always writes to the camera-specific directory (`<site>/<cam>/`).
You decide what to promote to `common/`.

---

## Commands

```
camtool.py [-h] [--password PWD] [--dry-run] [--verbose] [--timeout N]
           {info,pull,push,diff,verify} camera_name [endpoints ...]
```

| Command  | Purpose | Reads camera | Writes camera | Writes disk |
|----------|---------|:---:|:---:|:---:|
| `info`   | Print device model, firmware, serial, MAC | GET | - | - |
| `pull`   | Download live config → XML files | GET | - | Yes |
| `push`   | Upload XML files → camera (backs up live config first) | GET | PUT | Yes |
| `diff`   | Show differences (local XML vs live) | GET | - | - |
| `verify` | Like diff but exit 0/1/2 for scripting | GET | - | - |

### Filtering by endpoint

All commands except `info` accept optional endpoint names to limit scope:

```bash
python3 camtool.py pull jakarta-cam1 streaming_101 image
python3 camtool.py push jakarta-cam2 overlays --dry-run
```

Available endpoints: `ftp`, `image`, `ircutfilter`, `ispmode`,
`motion_detection`, `ntp`, `overlays`, `streaming_101`, `streaming_102`,
`time`.

---

## Typical Workflows

### Initial setup (new camera)

```bash
# 1. Pull everything from the live camera
python3 camtool.py pull jakarta-cam1

# 2. Review the pulled XML files in jakarta/cam1/
# 3. Move shared settings to common/, keep camera-specific in site dir
# 4. Commit to git

# 5. Test that push + backup works end-to-end
python3 camtool.py push jakarta-cam1 streaming_101
#   Should print: "Backed up live config to backups/jakarta-cam1/<timestamp>/"
ls backups/jakarta-cam1/          # confirm backup was written
```

### Pushing a config change

```bash
# 1. Edit the XML file (e.g. common/streaming_101.xml)
# 2. Dry run to see what would happen
python3 camtool.py push sukabumi-cam1 streaming_101 --dry-run

# 3. Push for real (automatically backs up live config first)
python3 camtool.py push sukabumi-cam1 streaming_101
#   -> backups/sukabumi-cam1/20260310_143022/streaming_101.xml

# 4. Verify it took effect
python3 camtool.py diff sukabumi-cam1 streaming_101

# To skip the backup (not recommended):
python3 camtool.py push sukabumi-cam1 streaming_101 --no-backup
```

### Checking for config drift

```bash
# Interactive — shows each difference
python3 camtool.py diff sukabumi-cam1

# Scriptable — exit code only (0=match, 1=drift, 2=error)
python3 camtool.py verify sukabumi-cam1
```

### Replacing a camera

```bash
# 1. Configure the new camera's IP and admin password via web GUI
# 2. Push the full config from git
python3 camtool.py push jakarta-cam1

# 3. Verify everything matches
python3 camtool.py verify jakarta-cam1
```

### Recovering from a bad push

Every `push` automatically backs up the live config before writing. If a push
introduces a bad setting, restore from the backup:

```bash
# 1. Find the backup
ls backups/jakarta-cam1/

# 2. Copy the backup file over the current config
cp backups/jakarta-cam1/20260310_143022/streaming_101.xml jakarta/cam1/streaming_101.xml

# 3. Push the restored config
python3 camtool.py push jakarta-cam1 streaming_101
```

Backups are gitignored — they're a local safety net, not version-controlled.

---

## Cameras

Defined in `cameras.json`. IPs match DHCP reservations in
`pi/shared/etc/dnsmasq.d/maintenance.conf`.

| Name | IP | Site | Description |
|------|-----|------|-------------|
| sukabumi-cam1 | 192.168.50.139 | Sukabumi | River gauge - single camera |
| jakarta-cam1 | 192.168.50.101 | Jakarta | Upstream view |
| jakarta-cam2 | 192.168.50.102 | Jakarta | Downstream view |

All three are ANNKE C1200 (12MP, IP67, built-in IR, Hikvision G6 platform).
Sukabumi has one camera; Jakarta has two (upstream + downstream views).

---

## Credentials

Camera passwords are **never committed** to git.

### Password resolution order

1. `--password` CLI flag (one-off use)
2. `CAMERA_PASSWORD` environment variable
3. `camera/.env` file (gitignored): `CAMERA_PASSWORD=yourpassword`

### Sensitive XML fields

Some endpoints contain passwords (e.g. FTP config). On `pull`, these are
automatically scrubbed to placeholder tokens like `<FTP_PASSWORD>`. On
`push`, the tool injects real values from environment variables or `.env`.

This follows the same `<PLACEHOLDER>` convention used in `pi/` configs.

---

## ISAPI Endpoint Reference

The tool manages these ISAPI endpoints. Add or remove entries in the
`ENDPOINTS` dict in `camtool.py` to support different parameters.

| Endpoint key | ISAPI path | Controls |
|-------------|-----------|----------|
| `streaming_101` | `/ISAPI/Streaming/channels/101` | Main stream encoding |
| `streaming_102` | `/ISAPI/Streaming/channels/102` | Sub stream encoding |
| `image` | `/ISAPI/Image/channels/1` | Image quality settings |
| `ircutfilter` | `/ISAPI/Image/channels/1/ircutFilter` | Day/night IR switching |
| `ispmode` | `/ISAPI/Image/channels/1/ISPMode` | IR LED behavior |
| `time` | `/ISAPI/System/time` | Timezone and time mode |
| `ntp` | `/ISAPI/System/time/NtpServers/1` | NTP server config |
| `overlays` | `/ISAPI/System/Video/inputs/channels/1/overlays` | OSD text/date overlays |
| `ftp` | `/ISAPI/System/Network/ftp` | FTP upload config |
| `motion_detection` | `/ISAPI/System/Video/inputs/channels/1/motionDetection` | Motion detection |

### Adding new endpoints

To manage an additional camera setting, add its ISAPI path to the `ENDPOINTS`
dict in `camtool.py`. Then `pull` will fetch it and `push` will upload it.
Discover available endpoints by browsing `/ISAPI/System/capabilities` on the
camera, or by consulting Hikvision ISAPI documentation.

---

## Design Details

For the full rationale behind the architecture, protocol choice, security
considerations, and future work, see
`research/camera_isapi_config_management.md`.
