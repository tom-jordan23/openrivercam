# Split Camera/Compute Architecture — Design Exploration

**Status:** Design exploration for future deployments
**Not a change to:** Current Sukabumi or Jakarta stations
**Date:** April 2026

---

## Motivation

The team asked whether future deployments could place the camera and sensors at the river while keeping compute in a nearby office building.

Moving compute indoors eliminates the primary reliability risks in tropical deployments (heat, humidity, condensation, UV) and makes maintenance trivial (SSH over LAN, no pole climbing, no weatherproof enclosure to open).

**Key design principle: complexity only where it adds value.** Once sensors move to an ESP32 and the camera is on IP, the compute node is just software — `orc-capture` (RTSP pull or clip fetch), `sensors_logger.py` (HTTP fetch), and an upload job. There's no GPIO, no Witty Pi scheduler, no hardware-specific dependency. A Pi is one option, but a Docker container on any available machine (office desktop, NUC, shared server) works equally well and may already be on-site.

---

## Architecture: River Node + Compute (Software)

```
┌─────────────────────────────────┐         ┌──────────────────────────────┐
│         RIVER NODE              │         │     COMPUTE (INDOOR)         │
│     (outdoor enclosure)         │         │  (Pi, Docker, NUC, etc.)     │
│                                 │  Cat6   │                              │
│  ANNKE C1200 PoE camera ◄──┐   │  fiber  │  orc-capture (fetch clips)   │
│  Hydreon RG-15 rain gauge   │   │  or     │  sensors_logger.py (HTTP)    │
│  DS18B20 temperature probe  │   │  VDSL2  │  upload agent → Pangolin     │
│                             │   │◄───────►│                              │
│  ESP32 sensor bridge ───────┤   │         │  Internet (office LAN or LTE)│
│  LINOVISION PoE switch ─────┘   │         │                              │
│  Power (solar or AC)            │         │  Powered from wall outlet    │
└─────────────────────────────────┘         └──────────────────────────────┘
```

**River Node** (outdoor enclosure on pole):
- ANNKE C1200 PoE camera (unchanged, IP67, built-in IR)
- Hydreon RG-15 rain gauge + DS18B20 temperature probe
- LINOVISION 12V PoE switch (feeds camera via short patch cable)
- ESP32 sensor bridge (reads sensors, exposes data over HTTP)
- Power system (site-dependent: solar or AC)

**Compute** (indoor — runs on whatever's available):
- Docker container or bare-metal Pi, depending on what the site has
- Needs: network access to camera subnet + internet for Pangolin upload
- LTE modem only needed if no office internet; otherwise use existing connectivity

---

## Video Capture: Camera-Side Recording

The current design has the Pi pull a 5s RTSP stream via ffmpeg in real time. In the split architecture, a simpler approach: **the camera records locally to its own SD card, and the compute node periodically fetches the clips.**

The ANNKE C1200 (Hikvision-compatible) supports:
- On-camera SD card recording (schedule-based or event-based)
- ISAPI/FTP for file retrieval
- NTP sync from the local network

**Capture workflow (split architecture):**

1. Camera records to its local SD card on a schedule (e.g., 5s clips every 15 min)
2. Compute node fetches clips from the camera via ISAPI or FTP over the network link
3. Compute node validates and uploads to Pangolin

**Why this is better for the split case:**

- Decouples capture timing from network availability — if the link goes down briefly, clips accumulate on the camera and get fetched later
- Eliminates the real-time ffmpeg RTSP dependency — no more "ffmpeg failed" retries due to network hiccups
- Reduces the bandwidth profile from "15 Mbps sustained during capture" to "bulk file transfer at any convenient time"

**Storage math:** At 16 Mbps CBR, 5s = ~10 MB per clip, 96 clips/day = ~1 GB/day. A 32 GB SD card holds ~30 days of buffer.

**Fallback:** The current RTSP pull approach (`orc-capture` with ffmpeg) still works over the network link at all three distance tiers. Camera-side recording is an optimization, not a requirement.

**Needs investigation:**
- Can the ANNKE C1200 record fixed-duration clips on a schedule via ISAPI? Or does the compute node need to trigger each recording via ISAPI command?
- What's the retrieval API — ISAPI ContentMgmt search + download, or FTP?

---

## Sensors: ESP32 Bridge

The RG-15 (UART on GPIO 14/15) and DS18B20 (1-Wire on GPIO 4) currently connect directly to Pi GPIO. With compute in an office, these protocols can't traverse a long cable.

**Solution:** An Ethernet-equipped ESP32 board (e.g., Olimex ESP32-POE-ISO, ~$35) reads both sensors locally and serves data over HTTP on the same network as the camera.

```
Compute (office) --HTTP GET--> ESP32 (river) --UART--> RG-15
                                              --1-Wire--> DS18B20
```

The ESP32 exposes `GET /sensors` returning JSON:

```json
{"rg15": {"acc_mm": 1.23, "interval_mm": 0.04}, "ds18b20": {"temp_c": 24.5}}
```

**Software changes to `sensors_logger.py`:**

- Add `read_rg15_remote(conf)` and `read_ds18b20_remote(conf)` drivers
- Register in the `DRIVERS` dict as `rg15_remote` and `ds18b20_remote`
- New config files use `SENSOR_TYPE=rg15_remote` with `BRIDGE_IP=192.168.50.150`
- Existing CSV output format, log rotation, and interval logic are unchanged

**Relay control:** For AC-powered sites (the expected default for split deployments), run the camera continuously — no relay needed. For solar sites where power cycling matters, the ESP32 also drives the relay and accepts `POST /relay {"state":"on"}` from the compute node.

**Critical detail:** The ESP32 must be on the always-on power bus, not the switched relay circuit. If it's on the switched circuit, it reboots when the camera power-cycles and loses state.

---

## Three Distance Tiers

### Tier 1: Under 100m — Copper Ethernet

Single Cat6 outdoor shielded cable from river to office. The PoE switch stays at the river (camera gets PoE locally via short patch cable). Compute connects to the far end of the Cat6 and serves as DHCP server on 192.168.50.0/24.

- **Cable:** Outdoor-rated Cat6 F/UTP, UV-resistant PE jacket. If aerial, use figure-8 cable with integrated messenger wire. Shield grounded at office end.
- **Surge protection:** Ethernet SPDs on both ends (e.g., Ubiquiti ETH-SP-G2). Grounded to earth at each end.
- **River node power:** ~15-20W

### Tier 2: 100m - 300m — VDSL2 Extenders

Same as Tier 1, plus a VDSL2 Ethernet extender pair (one at each end). Commodity industrial devices used in elevator and CCTV installations. Transparent L2 bridge, 60-100 Mbps throughput at 300m.

- **Example:** Planet VC-231 VDSL2 converter pair (~$150-250/pair)
- **River node power:** ~20-25W

### Tier 3: Up to 1km — Single-Mode Fiber

Point-to-point single-mode fiber with SFP media converters at each end. Pre-terminated OS2 fiber cable (factory LC connectors, no field splicing). Total electrical isolation eliminates lightning/surge risk on the data link.

- **Example:** Planet IGT-900-1T1S media converters (~$60 each) + standard 1.25G SFP modules (~$15 each)
- **River node power:** ~18-23W

### Tier Summary

| Aspect | Tier 1 (<100m) | Tier 2 (100-300m) | Tier 3 (up to 1km) |
|--------|----------------|--------------------|--------------------|
| Link type | Cat6 copper | Cat6 + VDSL2 extenders | Single-mode fiber |
| Throughput | 1 Gbps | 60-100 Mbps | 1 Gbps |
| Extension gear cost | $0 | ~$200 | ~$200 |
| Lightning isolation | No (need SPDs) | No (need SPDs) | Yes (fiber is dielectric) |
| Field repair | Re-crimp RJ45 | Re-crimp RJ45 | Replace entire fiber run |

---

## Power at the River Node

**Sites with AC at the pole:** Small industrial PSU (Mean Well MDR-20-12, 20W) + Type 2 surge protector.

**Sites without AC:** Solar panel + small LiFePO4 battery. ESP32 stays powered 24/7 (for rain gauge accumulation). PoE switch and camera can be duty-cycled via ESP32 relay control. Budget: ~60 Wh/day with duty cycling. A 100W panel + 20Ah battery suffices.

---

## Compute Node Options

The split architecture decouples compute from hardware:

| Option | When to use | Hardware cost | Notes |
|--------|-------------|---------------|-------|
| **Docker on existing machine** | Office has a desktop/server with a spare NIC | ~$0 | Needs a Dockerfile and scheduler (cron) |
| **Docker on a NUC/mini-PC** | Dedicated compute wanted, no Pi hardware needed | ~$150-200 | More reliable than Pi, runs standard Linux |
| **Pi indoors** | No existing machine, or remote site with only LTE | ~$300-400 | Same software stack as today, minus GPIO deps |

The Pi is a stepping stone. The end state for office-based deployments is a Docker container that fetches video clips, reads sensor data over HTTP, and uploads to Pangolin.

---

## Advantages vs. Co-located Design

1. **Compute moves indoors** — eliminates heat, humidity, and UV exposure
2. **Easier maintenance** — SSH over LAN, physical access without climbing a pole
3. **No dedicated compute hardware required** — Docker on an existing machine eliminates the Pi + Witty Pi + G469 + modem + antenna + weatherproof enclosure (~$300-400)
4. **Smaller river enclosure** — just PoE switch + ESP32 + power
5. **Office internet for upload** — no LTE modem needed if office has connectivity
6. **Camera-side recording** — decouples capture from network availability

## Disadvantages

1. **Cable routing** — trenching, conduit, or aerial cable is a site-specific civil works problem
2. **ESP32 is a new component** — firmware to develop and maintain
3. **Two enclosures to manage** — river node still needs weatherproofing for PoE switch and ESP32
4. **Requires a nearby building** — not all river sites have one

---

## Open Questions

1. **Camera-side recording via ISAPI** — can the ANNKE C1200 be configured to produce fixed-duration clips on a schedule? What's the retrieval API?
2. **ESP32 long-term stability** — does the Olimex ESP32-POE-ISO run reliably 24/7 in a tropical outdoor enclosure? Needs bench testing.
3. **ESP32 firmware update path** — OTA updates over Ethernet would preserve the "non-technical personnel" principle.
4. **Containerization of ORC software** — how much of the current tooling is Pi-specific vs. portable Python? This determines the effort to produce a Docker image.
5. **Network topology at the office** — compute needs to reach the camera's 192.168.50.0/24 subnet. On a shared machine, this likely means a dedicated NIC or VLAN.
6. **Field testing priority** — start with Tier 1 at a site under 100m. A Pi indoors is the simplest first test; Docker comes after the architecture is proven.

---

## See Also

- [WIRING_SUKABUMI.md](WIRING_SUKABUMI.md) — current co-located wiring (Sukabumi)
- [WIRING_JAKARTA.md](WIRING_JAKARTA.md) — current co-located wiring (Jakarta)
- [SENSOR_WIRING_GUIDE.md](SENSOR_WIRING_GUIDE.md) — GPIO pin reference for current sensor wiring
