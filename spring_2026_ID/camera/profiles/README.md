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

### Automated test

`run_profile_test.sh` cycles through profiles, captures videos for each,
and runs `video_quality_test.py` to produce per-profile scorecards and a
cross-profile comparison table.

```bash
# Test all profiles (10 captures each)
./run_profile_test.sh

# Test specific profiles, 5 captures each
./run_profile_test.sh --profiles baseline,a,b --captures 5

# Focus analysis on the water ROI
./run_profile_test.sh --roi 200,100,1600,900

# Dry run (show what would happen)
./run_profile_test.sh --dry-run
```

Results land in `tests/camera_profiles_<timestamp>/`.

### What gets measured

**Proxy metrics (always available):**
- Delivered bitrate vs. 20 Mbps target / 15 Mbps floor
- Spatial Information (SI) — texture/edge detail per frame
- Temporal Information (TI) — frame-to-frame motion
- Blockiness — H.264 compression artifact severity

**PIV metrics (requires `pip install ffpiv`):**
- **Correlation pass rate** — % of interrogation windows with cross-correlation
  peak ≥ 0.2 (pyorc `corr_min` default)
- **SNR pass rate** — % of windows with signal-to-noise ratio ≥ 3.0
  (pyorc `s2n_min` default)
- **Combined PIV pass rate** — the single number for comparing profiles
- **Displacement analysis** — whether frame-to-frame motion stays within
  the ¼-window rule for the chosen interrogation window size

The PIV analysis runs FFPIV (the same cross-correlation engine used by
pyorc) directly on raw video frames. This gives real pass rates instead
of proxy estimates. Note: results are on non-orthorectified frames, so
use them for **relative comparison** between profiles, not as absolute
go/no-go thresholds.

```bash
# Standalone analysis with custom PIV window size
python3 video_quality_test.py *.mp4 --compare --window-size 96

# Skip PIV (proxy metrics only)
python3 video_quality_test.py *.mp4 --compare --no-piv

# JSON output for further processing
python3 video_quality_test.py video.mp4 --json
```

### Decision criteria

1. **PIV pass rate** — higher is better; the profile with the highest
   combined pass rate preserves the most usable texture for velocimetry
2. **Displacement in range** — if < 90%, consider a larger `--window-size`
   or the flow is too fast for this frame rate
3. **Delivered bitrate** — must reliably exceed 15 Mbps (pyorc floor)
4. **Blockiness** — if severe (> 1.3), the encoder is destroying texture
   regardless of bitrate

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
