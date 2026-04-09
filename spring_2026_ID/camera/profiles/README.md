# Camera Streaming Profiles

Alternate streaming configurations optimized for different bitrate/quality
tradeoffs. Each profile is a `streaming_101.xml` replacement that can be
pushed to a camera via camtool.py.

## The Problem

ORC recommends 20 Mbps at 1080p for reliable surface velocity detection.
Our baseline config is 16 Mbps CBR, but actual RTSP captures average
15.5 Mbps with dips to 12 Mbps. The RTSP transport overhead and network
buffering consume some of the available bitrate.

## Profiles

| Profile | Resolution | FPS | Bitrate | Codec | Method | Use Case |
|---------|-----------|-----|---------|-------|--------|----------|
| **baseline** | 1920x1080 | 12.5 | 16 Mbps CBR | H.264 | RTSP pull | Current default |
| **profile-a** | 1920x1080 | 12.5 | 20 Mbps CBR | H.264 | RTSP pull | Higher bitrate ceiling, same resolution |
| **profile-b** | 1280x720 | 12.5 | 20 Mbps CBR | H.264 | RTSP pull | Max bits per pixel — 4.5x baseline quality/pixel |
| **profile-c** | 1920x1080 | 12.5 | 20 Mbps VBR (peak 25) | H.264 | Local SD + copy | Bypasses RTSP — full encoder quality |
| **profile-e** | 1920x1080 | 12.5 | 12 Mbps CBR | H.265 | RTSP pull | ~20 Mbps H.264 equivalent quality at 40% less bandwidth |
| **profile-f** | TBD (cropped) | 12.5 | 20 Mbps CBR | H.264 | RTSP pull | Digital crop to reduce FOV — needs ISAPI investigation |

**Note on HFOV:** The ANNKE C1200 has a very wide field of view (134 degrees).
We likely do not need the full frame width for the cross section. If the
useful scene occupies only the center portion of the frame, Profile B's
720p may provide equal or better effective resolution on the water surface
compared to 1080p — the wider FOV means many edge pixels are wasted on
bank/sky. Evaluate in the field before committing to a resolution.

## How to Use

```bash
# Push a profile to a camera
python3 camtool.py push sukabumi-cam1 --config profiles/profile-a/streaming_101.xml

# Revert to baseline
python3 camtool.py push sukabumi-cam1 --config common/streaming_101.xml
```

## Testing Protocol

For each profile, capture 10 videos and compare:
1. Actual delivered bitrate (`ffprobe -show_format`)
2. Frame count and framerate
3. Visual quality (zoom into water surface texture)
4. ORC processing results (velocity confidence, pattern detection)

Document results in `tests/` before committing to a profile for deployment.

## Notes

- The ANNKE C1200 (Hikvision G6 platform) supports up to ~32 Mbps at 1080p
- H.265 is available on the camera but Pi 5 lacks hardware H.265 decode — do
  not use H.265 for RTSP profiles unless the Pi can handle it in software
- Profile C bypasses RTSP entirely — the camera writes to its internal SD card
  at full quality, then the Pi copies the file. This eliminates transport
  overhead but adds transfer latency after capture.
- FPS is set to 1250 (12.5 fps in ISAPI tenths format) to match our actual
  observed capture rate. Setting 50 fps wastes bitrate on frames RTSP cannot
  deliver.
