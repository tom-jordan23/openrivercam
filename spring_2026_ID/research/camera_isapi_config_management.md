# Camera Configuration Management via Hikvision ISAPI
**Research Date:** March 8, 2026
**Context:** ANNKE C1200 PoE cameras (both Indonesia sites) need repeatable, version-controlled configuration

---

## Executive Summary

The ANNKE C1200 (Hikvision OEM, G6 platform) supports the **Hikvision ISAPI**
protocol — an HTTP REST API that exposes every camera setting as an XML
resource. This enables programmatic configuration management: store XML configs
in git, pull from live cameras, push changes, and detect drift.

**Decision:** Build a single-file Python CLI tool (`camtool.py`) that wraps
ISAPI into a git-friendly workflow. Configs use the same layered
common/site-specific pattern established by `pi/`.

**Key advantage over manual web GUI:** Config changes are reviewable in git
diffs, reproducible across cameras, and recoverable if a camera is factory
reset or replaced.

---

## 1. ISAPI Protocol Background

### What is ISAPI?

ISAPI (Internet Server Application Programming Interface) is Hikvision's HTTP
REST API available on all Hikvision cameras and NVRs, as well as OEM products
like the ANNKE C1200. It predates ONVIF and is more comprehensive — nearly
every camera setting is accessible.

### How it works

- **Transport:** HTTP (port 80 by default)
- **Authentication:** HTTP Digest Auth (RFC 2617)
- **Payloads:** XML with Hikvision namespace `http://www.hikvision.com/ver20/XMLSchema`
- **Read:** `GET /ISAPI/path/to/resource` → returns current XML config
- **Write:** `PUT /ISAPI/path/to/resource` with XML body → applies config
- **Capabilities:** `GET /ISAPI/path/to/resource/capabilities` → returns allowed values/ranges

### Example: reading streaming config

```
GET /ISAPI/Streaming/channels/101 HTTP/1.1
Authorization: Digest username="admin", ...

→ 200 OK
<?xml version="1.0" encoding="UTF-8"?>
<StreamingChannel xmlns="http://www.hikvision.com/ver20/XMLSchema">
  <id>101</id>
  <Video>
    <videoCodecType>H.265</videoCodecType>
    <videoResolutionWidth>3840</videoResolutionWidth>
    <videoResolutionHeight>2160</videoResolutionHeight>
    <maxFrameRate>2500</maxFrameRate>
    ...
  </Video>
</StreamingChannel>
```

### Why not ONVIF?

- ONVIF covers a subset of settings (streaming profiles, PTZ, events)
- ISAPI exposes everything: image tuning, IR behavior, OSD overlays, NTP, FTP,
  motion detection, firmware info, etc.
- ANNKE C1200 firmware has full ISAPI support out of the box
- ONVIF requires a heavier SOAP/XML stack; ISAPI is plain HTTP + simple XML

---

## 2. ANNKE C1200 ISAPI Endpoints

These are the endpoints relevant to ORC deployment. The ANNKE C1200 supports
many more (alarms, recording, network, users, etc.) but these cover the
settings we need to manage.

| Config Area | Endpoint | Description |
|-------------|----------|-------------|
| Main stream | `/ISAPI/Streaming/channels/101` | Codec, resolution, FPS, bitrate |
| Sub stream | `/ISAPI/Streaming/channels/102` | Lower-res stream for preview |
| Image | `/ISAPI/Image/channels/1` | Brightness, contrast, saturation, WDR |
| IR cut filter | `/ISAPI/Image/channels/1/ircutFilter` | Day/night switching mode |
| ISP/IR LEDs | `/ISAPI/Image/channels/1/ISPMode` | IR LED behavior (auto/on/off) |
| System time | `/ISAPI/System/time` | Timezone, time mode (NTP/manual) |
| NTP | `/ISAPI/System/time/NtpServers/1` | NTP server address and interval |
| OSD overlays | `/ISAPI/System/Video/inputs/channels/1/overlays` | Text/date overlays on video |
| FTP | `/ISAPI/System/Network/ftp` | FTP upload config (if used) |
| Motion detect | `/ISAPI/System/Video/inputs/channels/1/motionDetection` | Motion detection enable/disable |
| Device info | `/ISAPI/System/deviceInfo` | Model, serial, firmware (read-only) |

### Channel numbering

Hikvision uses a 3-digit channel ID: `X0Y` where X = video channel (1 for
single-channel cameras) and Y = stream number (1 = main, 2 = sub). So:

- `101` = channel 1, main stream
- `102` = channel 1, sub stream

---

## 3. Design Decisions

### 3.1 Single-file tool (no package)

`camtool.py` is intentionally one file (~340 lines). It has a single external
dependency (`requests`). Rationale:

- Runs directly on the Pi or any machine with Python 3.9+ and requests
- No setup.py, no virtual env required for basic use
- Easy to scp to a Pi for field use
- Complexity doesn't warrant a package structure

### 3.2 Layered config (common → site → camera)

Mirrors the `pi/` convention (shared → site-specific):

```
camera/
├── common/              # Baseline for all cameras
│   ├── streaming_101.xml
│   ├── image.xml
│   └── ...
├── sukabumi/cam1/       # Overrides for this specific camera
└── jakarta/cam1/
    └── overlays.xml     # Camera-specific OSD text
```

Resolution order for a given endpoint:
1. `<site>/<camera>/<endpoint>.xml` — camera-specific (wins)
2. `common/<endpoint>.xml` — shared baseline
3. Skip (no config for this endpoint)

This means most settings live in `common/` and only truly per-camera settings
(like OSD overlay text) live in the site directories. The tool resolves this
automatically.

### 3.3 Pull-first workflow

The XML stubs checked into `common/` are placeholders with approximate
structure. The **real** XML schemas come from the camera itself:

1. `camtool.py pull <camera>` — downloads live XML from every endpoint
2. Review the pulled files — they now have the exact schema the camera uses
3. Edit values as needed
4. Move common settings to `common/`, keep camera-specific in site dir
5. Commit

This avoids guessing at Hikvision's XML schema (which varies by firmware
version) and ensures our stored configs are always valid.

### 3.4 Credential handling

Follows the `<PLACEHOLDER>` convention from `pi/README.md`:

- Camera password: `--password` flag > `CAMERA_PASSWORD` env var > `.env` file
- `.env` file is gitignored (`camera/.env`)
- Sensitive XML fields (FTP passwords, etc.) are scrubbed to `<FTP_PASSWORD>`
  on pull, injected from env vars on push
- No credentials ever appear in committed files

### 3.5 XML comparison

The diff/verify commands compare local XML against live camera config
element-by-element rather than text-diffing. This handles:

- Namespace prefix differences
- Attribute ordering
- Whitespace/indentation changes
- Volatile fields (`currentDeviceTime`, `upTime`) are excluded automatically

---

## 4. Relationship to Other Config

| System | Managed by | Storage |
|--------|-----------|---------|
| Pi OS configs (dnsmasq, network, services) | Manual scp from `pi/` | `pi/shared/`, `pi/<site>/` |
| Camera configs (encoding, image, OSD, etc.) | `camtool.py` from `camera/` | `camera/common/`, `camera/<site>/<cam>/` |
| Camera DHCP reservations | dnsmasq config in `pi/` | `pi/shared/etc/dnsmasq.d/maintenance.conf` |

The camera IP addresses in `cameras.json` must match the DHCP reservations in
the Pi's dnsmasq config. Both are tracked in git.

---

## 5. Security Considerations

- ISAPI uses HTTP Digest Auth (not Basic), which avoids sending passwords in
  cleartext. However, the connection itself is unencrypted HTTP.
- This is acceptable because cameras are on an isolated local network behind
  the Pi (no internet exposure). The Pi acts as the only gateway.
- Camera passwords should still be strong — they protect against anyone with
  physical network access at the site.

---

## 6. Limitations and Future Work

### Known limitations

- **No batch mode across cameras:** Each command targets one camera. To push
  to all cameras, run the command three times (or wrap in a shell loop).
- **No automatic camera discovery:** Cameras must be manually added to
  `cameras.json`. Could add mDNS/SSDP discovery later if needed.
- **No firmware update support:** ISAPI supports firmware upload but this is
  intentionally excluded — firmware updates should be manual and deliberate.
- **No rollback:** If a push causes problems, the fix is to edit the XML and
  push again (or pull from a known-good camera). Git history provides the
  rollback source.

### Possible future additions

- `camtool.py backup` — dump all endpoints (including ones not in ENDPOINTS
  dict) to a timestamped archive
- `camtool.py restore` — push a full backup archive to a replacement camera
- Endpoint auto-discovery via `/ISAPI/System/capabilities`
- Integration with Pi maintenance mode (push configs during field visits)

---

## 7. References

- Hikvision ISAPI documentation (available from Hikvision partner portal)
- ANNKE C1200 product page: 12MP PoE IP camera, Hikvision G6 platform
- Python `requests` library with HTTP Digest Auth
- Existing layered config pattern: `pi/README.md`
