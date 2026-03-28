# orc-capture Timing Test — 2026-03-28

20 full relay-on/capture/relay-off cycles using built-in defaults (no config
file). All runs used `--dry-run` (captured but not delivered to ORC-OS).

## Environment

- Pi: Raspberry Pi 5 8GB, Bookworm
- Camera: ANNKE C1200, PoE via relay on GPIO 24
- Network: direct Ethernet (Pi ↔ PoE injector ↔ camera)
- Config: built-in defaults (no /etc/orc-capture.conf)
- RTSP: tcp transport, codec copy, 5s duration

## Results

**20/20 PASS — 100% success rate**

| Metric | Average | Min | Max |
|--------|---------|-----|-----|
| Total cycle | 69.4s | 68.4s | 73.6s |
| Camera boot | 36.8s | 36s | 40s |
| Settle wait | 15.0s | 15s | 15s |
| ISAPI enforcement | <1s | <1s | <1s |
| RTSP capture | 5.7s | 5s | 6s |
| Quality gate | 0.3s | 0s | 1s |
| Bitrate | 15,502 kbps | 14,837 | 16,557 |
| Resolution | 1920x1080 | — | — |
| Duration | 5.037s | — | — |
| Frames | 64 | — | — |

Note: ISAPI, capture, and quality gate timings have 1-second resolution
(parsed from log timestamps). Actual sub-second values are in the total_ms
column of the CSV.

## Observations

- Camera boot dominates at 53% of total cycle time
- 15s settle time is conservative — may be reducible (future test)
- Iteration 7 was the outlier (40s boot, 73.6s total)
- Bitrate is stable at ~15.5 Mbps, well above the 12 Mbps quality gate
- supplementLightMode was already set to irLight on every iteration
  (enforcement was a no-op), but the white spotlight still fires briefly
  during camera boot — see spotlight issue in project notes

## Raw Data

See [capture_timing_20260328.csv](capture_timing_20260328.csv) for per-iteration data.
