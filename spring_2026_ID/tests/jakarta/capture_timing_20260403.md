# orc-capture Timing Test — 2026-04-03

20 capture cycles using `--skip-relay --dry-run` (camera always-on, AC power).
Tests capture pipeline only (no relay cycling or boot wait).

## Environment

- Pi: Raspberry Pi 5 8GB, Bookworm
- Camera: ANNKE C1200, PoE via always-on relay on GPIO 24
- Network: direct Ethernet (Pi <-> PoE injector <-> camera)
- Config: /etc/orc-capture.conf (RELAY_MODE=always)
- RTSP: TCP transport, codec copy, 5s duration
- Streaming: 1920x1080, H.264, CBR 16384 kbps, 12.5 fps

## Results

**20/20 PASS — 100% success rate**

| Metric | Average | Min | Max |
|--------|---------|-----|-----|
| Total cycle | 6.0s | 5.9s | 6.1s |
| ISAPI enforcement | <1s | <1s | 1s |
| RTSP capture | 5.3s | 5s | 6s |
| Quality gate | 0.7s | <1s | 1s |
| Bitrate | 16,483 kbps | 16,017 | 17,226 |
| Resolution | 1920x1080 | — | — |
| Duration | 5.037s | — | — |
| Frames | 64 | — | — |

Note: ISAPI, capture, and quality gate timings have 1-second resolution
(parsed from log timestamps). Wall-clock total_ms is precise.

## Comparison with Sukabumi (relay-cycled)

| Metric | Jakarta (always-on) | Sukabumi (relay-cycled) |
|--------|-------------------|----------------------|
| Total cycle | 6.0s | 69.4s |
| Camera boot | 0s (already on) | 36.8s |
| Settle wait | 0s (already on) | 15.0s |
| RTSP capture | 5.3s | 5.7s |
| Bitrate | 16,483 kbps | 15,502 kbps |
| Success rate | 20/20 (100%) | 20/20 (100%) |

Jakarta's always-on relay mode eliminates the 52s boot+settle overhead,
reducing total cycle time from ~69s to ~6s. Bitrate is slightly higher
(16.5 vs 15.5 Mbps) — likely because the camera stream is already
stabilized rather than freshly started after boot.

## Observations

- All 20 captures produced identical resolution, duration, and frame count
- supplementLightMode was already irLight on every iteration (no enforcement needed)
- Bitrate varies ~6% (16,017-17,226 kbps) around the 16,384 CBR target — normal for CBR
- ffmpeg reports non-monotonic DTS warnings on every capture — cosmetic, does not affect output
- No retries triggered across all 20 iterations

## Raw Data

See [capture_timing_20260403.csv](capture_timing_20260403.csv) for per-iteration data.
