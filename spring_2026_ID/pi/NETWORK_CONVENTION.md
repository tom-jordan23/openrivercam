# Camera Network Convention

**Status:** Adopted 2026-04-02. Implementation pending — do not change configs
until Sukabumi station is fully tested.

---

## Network Design

Each ORC station runs an isolated 192.168.50.0/24 network on eth0. The Pi
acts as gateway, DHCP server (dnsmasq), and NTP server (chrony). Cameras
and any future devices on this network have no internet access — all
communication is local between the Pi and its connected devices.

This convention is identical across all stations. Since each station is a
self-contained network, there are no IP conflicts between sites.

## IP Address Assignments

| IP Range | Assignment | Notes |
|----------|-----------|-------|
| **192.168.50.1** | Pi (gateway, DHCP server, NTP server) | Always .1 on every station |
| **192.168.50.10–.19** | Infrastructure | Managed PoE switches (if applicable) |
| **192.168.50.100** | Camera 1 | Fixed DHCP reservation by MAC address |
| **192.168.50.101** | Camera 2 | Fixed DHCP reservation by MAC (if added) |
| **192.168.50.102–.149** | Future cameras | Sequential assignment |
| **192.168.50.200–.254** | DHCP discovery pool | For unknown devices before MAC is known |
| **192.168.50.2–.9** | Reserved | Future infrastructure |
| **192.168.50.150–.199** | Reserved | Future non-camera devices (sensors, etc.) |

## Hostnames

Cameras are numbered locally — no site name needed since the network is
self-contained per station.

| Hostname | IP | Description |
|----------|-----|-------------|
| `cam1` | 192.168.50.100 | First camera |
| `cam2` | 192.168.50.101 | Second camera (if installed) |
| `cam3` | 192.168.50.102 | Third camera (if installed) |

Hostnames are set in `/etc/cloud/templates/hosts.debian.tmpl` (or `/etc/hosts`)
on each Pi.

## dnsmasq Configuration

```
# Camera network DHCP server on eth0
interface=eth0
bind-dynamic

# Discovery pool for unknown devices
dhcp-range=192.168.50.200,192.168.50.254,24h

# Camera reservations (add MAC for each camera)
# dhcp-host=<CAM1_MAC>,192.168.50.100,cam1
# dhcp-host=<CAM2_MAC>,192.168.50.101,cam2
```

The `dhcp-host` lines are site-specific (each camera has a unique MAC) and
live in the site overlay directory, not in the shared config.

## Migration Plan

### Current state (do not change until Sukabumi testing is complete):
- Sukabumi camera: 192.168.50.139
- Jakarta camera: 192.168.50.101

### Target state:
- Sukabumi camera: 192.168.50.100
- Jakarta camera: 192.168.50.100

### Files that need updating when implemented:

| File | Change |
|------|--------|
| `pi/shared/etc/dnsmasq.d/maintenance.conf` | Split into shared network config + per-site camera reservation |
| `pi/sukabumi/etc/dnsmasq.d/cameras.conf` | Create: dhcp-host line with Sukabumi camera MAC → .100 |
| `pi/jakarta/etc/dnsmasq.d/cameras.conf` | Create: dhcp-host line with Jakarta camera MAC → .100 |
| `pi/sukabumi/etc/orc-capture.conf` | CAMERA_IP=192.168.50.139 → 192.168.50.100 |
| `pi/jakarta/etc/orc-capture.conf` | CAMERA_IP=192.168.50.101 → 192.168.50.100 (already same on new convention) |
| `pi/sukabumi/etc/cloud/templates/hosts.debian.tmpl` | Update camera hostname and IP |
| `pi/jakarta/etc/cloud/templates/hosts.debian.tmpl` | Create with cam1 → .100 |
| `pi/sukabumi/etc/NetworkManager/system-connections/camera-net.nmconnection` | No change (Pi IP stays .1) |
| `pi/jakarta/etc/NetworkManager/system-connections/camera-net.nmconnection` | Create (Pi IP .1, same as Sukabumi) |
| `pi/shared/update-motd.d/30-camera-status` | Read CAMERA_IP from /etc/orc-capture.conf instead of hardcoding |
| `docs/ASSEMBLY_SUKABUMI.md` | All references to .139 → .100 |
| `docs/ASSEMBLY_JAKARTA.md` | All references to .101 → .100 |
| `docs/DOOR_SHEET_SUKABUMI.md` | Camera IP .139 → .100 |
| `docs/DOOR_SHEET_JAKARTA.md` | Camera IP .101 → .100 |
| `docs/WIRING_JAKARTA.md` | Network topology diagram .101 → .100 |
| `docs/CONTINUITY_CHECKLIST_SUKABUMI.txt` | No change (no IPs in continuity checks) |
| `docs/CONTINUITY_CHECKLIST_JAKARTA.txt` | No change |
| `camera/cameras.json` | Update IPs for both sites |

### Implementation sequence:
1. Complete Sukabumi build and end-to-end testing at .139
2. Implement network convention changes in a single commit
3. Re-deploy to Sukabumi Pi via deploy.sh
4. Deploy to Jakarta Pi (fresh image) — gets .100 from the start
5. Update camera DHCP reservation with actual MAC addresses

### Why not change now:
The Sukabumi station is actively being tested with the camera at .139.
Changing the IP mid-build risks breaking the working capture pipeline and
would require re-testing everything. Apply this convention when:
- Flashing the new ORC-OS image from Hessel, OR
- After Sukabumi end-to-end testing is complete, whichever comes first
