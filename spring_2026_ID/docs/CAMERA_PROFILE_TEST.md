# Camera Profile Test — Field Procedure

Run this procedure at the Jakarta site (AC power, continuous operation)
before deploying to Sukabumi. The goal is to determine which camera
streaming profile produces the best video for ORC surface velocity
measurement.

---

## Prerequisites

On the Pi:
- Camera reachable and `orc-capture` working
- `camtool.py` configured with credentials (see `camera/README.md`)
- Python 3.9+ with `opencv-python-headless` and `numpy`
- `ffpiv` installed (`pip install ffpiv`) for PIV analysis

Verify camera connectivity before starting:
```bash
python3 camtool.py info jakarta-cam1
```

---

## What We're Testing

The ANNKE C1200 baseline config delivers ~15.5 Mbps over RTSP against a
16 Mbps CBR target. ORC (via pyorc/FFPIV) recommends 20 Mbps at 1080p,
with 15 Mbps as the practical floor. We're testing alternate streaming
profiles to find the configuration that gives FFPIV the best signal.

### Profiles

| Profile | Resolution | Bitrate | Codec | Method | Hypothesis |
|---------|-----------|---------|-------|--------|------------|
| **baseline** | 1920x1080 | 16 Mbps CBR | H.264 | RTSP | Current default |
| **A** | 1920x1080 | 20 Mbps CBR | H.264 | RTSP | Higher bitrate ceiling |
| **B** | 1280x720 | 20 Mbps CBR | H.264 | RTSP | Max bits/pixel (4.5x baseline quality/pixel) |
| **C** | 1920x1080 | 20 Mbps VBR | H.264 | Local SD | Bypass RTSP transport overhead |
| **E** | 1920x1080 | 12 Mbps CBR | H.265 | RTSP | Equivalent quality at 40% less bandwidth |

---

## What Gets Measured

### Proxy metrics (always available)

| Metric | What it means | Source |
|--------|---------------|--------|
| Delivered bitrate | Actual kbps in the file | ffprobe |
| Spatial Information (SI) | Texture/edge detail per frame (Sobel std dev) | ITU-T P.910 |
| Temporal Information (TI) | Frame-to-frame motion (diff std dev) | ITU-T P.910 |
| Blockiness | H.264 compression artifact severity at 8×8 block boundaries | Gradient ratio |

### PIV metrics (the ones that matter)

These run the same FFPIV cross-correlation engine used by pyorc directly
on the captured video frames.

| Metric | What it means | pyorc default |
|--------|---------------|---------------|
| **Correlation pass rate** | % of interrogation windows where the cross-correlation peak ≥ threshold | `corr_min = 0.2` |
| **SNR pass rate** | % of windows where signal-to-noise ratio ≥ threshold | `s2n_min = 3.0` |
| **Combined PIV pass rate** | % passing BOTH correlation AND SNR — the key comparison number | — |
| **Displacement in range** | % of displacements ≤ ¼ of interrogation window size | ¼-window rule |

**Important:** PIV analysis runs on raw (non-orthorectified) frames. Use
results for **relative comparison** between profiles, not as absolute
go/no-go thresholds. The definitive test is always running the video
through the full ORC pipeline (Phase 5 in the test plan).

### Why PIV metrics beat proxy metrics

SI and TI measure generic image properties. They correlate with PIV
quality but don't measure it directly. A video with high SI could still
fail PIV if the texture is compression artifacts (which don't move with
the water). The PIV pass rate measures what FFPIV actually cares about:
can it find a reliable correlation peak between consecutive frames?

---

## Running the Test

### Quick start (automated)

```bash
cd spring_2026_ID/camera/profiles

# Test all profiles, 10 captures each
./run_profile_test.sh

# Test specific profiles
./run_profile_test.sh --profiles baseline,a,b --captures 5

# Focus analysis on the water surface (exclude sky/bank)
./run_profile_test.sh --roi 200,100,1600,900

# Preview what would happen
./run_profile_test.sh --dry-run
```

The script will:
1. Push each profile config to the camera via `camtool.py`
2. Wait 15 seconds for the camera to adjust
3. Capture N videos per profile using `orc-capture`
4. Run `video_quality_test.py` on each set of captures
5. Restore the baseline config when done
6. Generate a cross-profile comparison

Results go to `tests/camera_profiles_<timestamp>/`.

### Manual analysis

```bash
# Analyze a single video (full scorecard)
python3 video_quality_test.py video.mp4

# Compare multiple videos side-by-side
python3 video_quality_test.py baseline/*.mp4 profile-a/*.mp4 --compare

# Custom PIV window size (default: 64px, 50% overlap)
python3 video_quality_test.py *.mp4 --compare --window-size 96

# Focus on water ROI
python3 video_quality_test.py *.mp4 --compare --roi 200,100,1600,900

# Skip PIV analysis (proxy metrics only — faster)
python3 video_quality_test.py *.mp4 --compare --no-piv

# JSON output for scripting
python3 video_quality_test.py video.mp4 --json
```

### ROI selection

The `--roi x,y,width,height` flag crops analysis to the water surface,
excluding sky and riverbank pixels that would skew the metrics. Determine
the ROI by opening a captured frame in an image viewer and noting the
pixel coordinates of the water area. The same ROI should be used for all
profiles in a test run.

---

## Reading the Results

### Scorecard (single video)

```
============================================================
  VIDEO QUALITY SCORECARD — capture_001.mp4
============================================================

  Container:
    Resolution:   1920x1080
    Codec:        h264
    Bitrate:      15523.4 kbps

  Analysis (ROI: 200,100,1600,900, 125 frames):

    Spatial Info (SI):      32.4  [MODERATE]
    Temporal Info (TI):      5.1  [MODERATE]
    Blockiness:              1.082 [MINOR]

  PIV Analysis (59 pairs, 420 windows/pair, 64px window):

    Correlation (≥0.2):    72.3% pass  [FAIR]
      median 0.312  (p25: 0.178, p75: 0.489)
    SNR (≥3.0):            61.8% pass  [FAIR]
      median 3.42   (p25: 2.11, p75: 5.67)
    Combined pass rate:    58.1%       [FAIR]

    Displacement:          median 2.3 px/frame  (max 14.7)
      ≤ ¼ window (16px): 94.2%  [OK]
```

### Comparison table (multiple profiles)

The comparison table shows all metrics side-by-side. Focus on:

1. **PIV pass rate %** — the primary comparison number, higher is better
2. **Disp in range %** — should be > 90%; if not, try `--window-size 96`
3. **Bitrate** — must exceed 15000 kbps (15 Mbps floor)
4. **Blockiness** — should be < 1.15; above 1.3 is a hard fail

### Interpreting displacement problems

If displacement is frequently out of range (> ¼ window):
- **Too much motion:** Water is fast relative to frame rate and window
  size. Try a larger `--window-size` (96 or 128).
- **Too little motion:** Water is slow or the camera is far from the
  surface. This is less common but means TI will also be low.

The ¼-window rule exists because larger displacements mean fewer particles
stay within the interrogation window between frames, degrading the
cross-correlation signal.

---

## Decision Criteria

### Phase 1–4: Profile selection

| Criterion | Threshold | Action if failed |
|-----------|-----------|------------------|
| PIV combined pass rate | Higher is better across profiles | Pick the highest |
| Delivered bitrate | ≥ 15 Mbps | Eliminate profile |
| Blockiness | < 1.3 | Eliminate profile |
| Displacement in range | > 90% | Try larger window size before eliminating |

### Phase 5: ORC validation

The profile test narrows the field. The final decision requires running
the best profile(s) through the full ORC pipeline:

1. Capture a calibration video with the selected profile
2. Set up GCPs and cross section in pyorc
3. Process velocimetry and check:
   - PIV correlation pass rate in the orthorectified domain
   - Velocity field coherence (do vectors point downstream?)
   - Discharge estimate plausibility
4. Compare across candidate profiles

### Decision gate

- If any RTSP profile reliably delivers 15+ Mbps with acceptable ORC
  results → **keep ANNKE C1200** with that profile
- If no RTSP profile works but Profile C (local SD) does → **implement
  ISAPI capture method** in orc-capture
- If no profile produces acceptable ORC results → **plan camera
  replacement** before Sukabumi deployment

---

## Output Structure

```
tests/camera_profiles_20260415_103022/
├── baseline/
│   ├── capture_001.mp4
│   ├── capture_002.mp4
│   ├── ...
│   └── quality_report.txt
├── a/
│   ├── capture_001.mp4
│   ├── ...
│   └── quality_report.txt
├── b/
│   └── ...
└── comparison.txt          ← cross-profile comparison table
```

---

## Troubleshooting

**"ffpiv not installed" in scorecard:**
Install with `pip install ffpiv`. Without it, only proxy metrics are
reported and you lose the PIV pass rate — the most useful comparison
metric.

**PIV analysis fails with memory error:**
The tool samples up to 60 frames. If the video is very high resolution
and the window size is small, the correlation array can be large. Try
`--window-size 96` or `--roi` to reduce the analysis area.

**All profiles show similar PIV pass rates:**
The camera may be the limiting factor regardless of encoding settings.
Check if blockiness is consistently high — if so, the encoder hardware
may not be capable of preserving enough texture. Consider Profile C
(local SD) or camera replacement.

**Displacement out of range for all profiles:**
The flow is fast relative to the frame rate. This is a property of the
scene, not the encoding. Options:
- Increase `--window-size` (96 or 128)
- If the camera supports higher FPS, test a higher frame rate profile
- Move the camera closer to the water surface (reduces pixel velocity)
