#!/usr/bin/env python3
"""video_quality_test.py — Measure video quality metrics for ORC suitability.

Analyzes captured video files and produces a scorecard of metrics relevant
to ORC surface velocity detection:

  Proxy metrics (always available):
  - Delivered bitrate (from container metadata)
  - Spatial Information (SI) — texture/edge detail per frame
  - Temporal Information (TI) — frame-to-frame motion
  - Blockiness index — H.264 compression artifact detection
  - Frame count, effective FPS, resolution

  PIV metrics (requires ffpiv):
  - Correlation coefficient distribution and pass rate (corr_min = 0.2)
  - Signal-to-noise ratio distribution and pass rate (s2n_min = 3.0)
  - Combined PIV pass rate — the key number for profile comparison
  - Displacement magnitude vs. ¼-window rule

Usage:
    python3 video_quality_test.py VIDEO_FILE
    python3 video_quality_test.py VIDEO_FILE --roi 200,100,1600,900
    python3 video_quality_test.py *.mp4 --compare
    python3 video_quality_test.py *.mp4 --compare --window-size 96
    python3 video_quality_test.py VIDEO_FILE --no-piv
    python3 video_quality_test.py VIDEO_FILE --json

ROI (Region of Interest) crops analysis to the water surface area,
excluding sky and bank. Format: x,y,width,height in pixels.

Metrics Reference (ITU-T P.910):
    SI = std_dev(Sobel(frame))     — higher = more texture detail
    TI = std_dev(frame_n - frame_n-1) — higher = more visible motion
    Both correlate with ORC's ability to detect surface velocity patterns.

PIV Reference (FFPIV / pyorc):
    The PIV analysis runs the same cross-correlation algorithm used by
    pyorc (via ffpiv) directly on the raw video frames. This gives the
    actual pass rates that determine whether a video is usable for
    velocimetry — not proxy estimates, but the real signal.

    - corr_min = 0.2: minimum cross-correlation peak (pyorc default)
    - s2n_min = 3.0: minimum signal-to-noise ratio (pyorc default)
    - ¼-window rule: displacement must not exceed 25% of window size

    Note: these results are on RAW (non-orthorectified) frames. Actual
    pyorc processing includes orthorectification and normalization, so
    real pass rates may differ. Use these for relative comparison across
    camera profiles, not as absolute go/no-go thresholds.

ORC-Specific Context (from pyorc velocimetry docs):
    - 20 Mbps at 1080p is the recommended bitrate (pyorc docs)
    - 15 Mbps is the practical floor (per Hessel Winsemius)

Requires:
    pip install opencv-python-headless numpy
    pip install ffpiv          (optional — enables PIV pass-rate analysis)
    pip install ffpiv          (optional — enables PIV pass-rate analysis)
"""

import argparse
import json
import os
import subprocess
import sys

import cv2
import numpy as np

try:
    import ffpiv
    HAS_FFPIV = True
except ImportError:
    HAS_FFPIV = False


def get_ffprobe_info(video_path):
    """Extract container-level metrics via ffprobe."""
    cmd = [
        "ffprobe", "-v", "quiet",
        "-print_format", "json",
        "-show_format", "-show_streams",
        video_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffprobe failed: {result.stderr}")

    data = json.loads(result.stdout)
    fmt = data.get("format", {})

    # Find video stream
    video_stream = None
    for s in data.get("streams", []):
        if s.get("codec_type") == "video":
            video_stream = s
            break

    if not video_stream:
        raise RuntimeError("No video stream found")

    duration = float(fmt.get("duration", 0))
    size_bytes = int(fmt.get("size", 0))
    bitrate_kbps = int(fmt.get("bit_rate", 0)) / 1000

    width = int(video_stream.get("width", 0))
    height = int(video_stream.get("height", 0))
    codec = video_stream.get("codec_name", "unknown")
    nb_frames = int(video_stream.get("nb_frames", 0))
    fps = 0
    if duration > 0 and nb_frames > 0:
        fps = round(nb_frames / duration, 1)

    return {
        "file": os.path.basename(video_path),
        "codec": codec,
        "width": width,
        "height": height,
        "duration_s": round(duration, 2),
        "size_kb": round(size_bytes / 1024, 1),
        "bitrate_kbps": round(bitrate_kbps, 1),
        "nb_frames": nb_frames,
        "fps": fps,
    }


def parse_roi(roi_str, width, height):
    """Parse ROI string 'x,y,w,h' or return full frame."""
    if not roi_str:
        return 0, 0, width, height
    parts = [int(x) for x in roi_str.split(",")]
    if len(parts) != 4:
        raise ValueError("ROI must be x,y,width,height")
    return parts[0], parts[1], parts[2], parts[3]


def analyze_frames(video_path, roi_str=None):
    """Compute per-frame SI, TI, and blockiness metrics."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open video: {video_path}")

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    rx, ry, rw, rh = parse_roi(roi_str, width, height)

    si_values = []
    ti_values = []
    blockiness_values = []
    prev_gray = None
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Crop to ROI
        roi = frame[ry:ry+rh, rx:rx+rw]
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY).astype(np.float64)

        # Spatial Information: std dev of Sobel magnitude
        sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        sobel_mag = np.sqrt(sobel_x**2 + sobel_y**2)
        si = np.std(sobel_mag)
        si_values.append(si)

        # Temporal Information: std dev of frame difference
        if prev_gray is not None:
            diff = gray - prev_gray
            ti = np.std(diff)
            ti_values.append(ti)

        # Blockiness: detect 8x8 DCT block boundaries
        # Measure gradient magnitude at 8-pixel intervals vs elsewhere
        if gray.shape[0] >= 64 and gray.shape[1] >= 64:
            blockiness = compute_blockiness(gray)
            blockiness_values.append(blockiness)

        prev_gray = gray
        frame_count += 1

    cap.release()

    return {
        "frames_analyzed": frame_count,
        "roi": f"{rx},{ry},{rw},{rh}",
        "si_mean": round(np.mean(si_values), 2) if si_values else 0,
        "si_std": round(np.std(si_values), 2) if si_values else 0,
        "si_min": round(np.min(si_values), 2) if si_values else 0,
        "si_max": round(np.max(si_values), 2) if si_values else 0,
        "ti_mean": round(np.mean(ti_values), 2) if ti_values else 0,
        "ti_std": round(np.std(ti_values), 2) if ti_values else 0,
        "ti_min": round(np.min(ti_values), 2) if ti_values else 0,
        "ti_max": round(np.max(ti_values), 2) if ti_values else 0,
        "blockiness_mean": round(np.mean(blockiness_values), 4) if blockiness_values else 0,
        "blockiness_max": round(np.max(blockiness_values), 4) if blockiness_values else 0,
    }


def compute_blockiness(gray):
    """Estimate H.264 blocking artifact severity.

    Compares gradient magnitude at 8-pixel block boundaries to
    non-boundary locations. Higher ratio = more visible blocking.
    Returns a ratio: 1.0 = no blocking, >1.0 = blocking detected.
    """
    h, w = gray.shape

    # Horizontal gradients
    grad_h = np.abs(np.diff(gray, axis=1))

    # Gradients at 8-pixel boundaries
    boundary_cols = list(range(7, w-1, 8))
    non_boundary_cols = [c for c in range(w-1) if c not in boundary_cols]

    if not boundary_cols or not non_boundary_cols:
        return 1.0

    boundary_mean = np.mean(grad_h[:, boundary_cols])
    non_boundary_mean = np.mean(grad_h[:, non_boundary_cols])

    if non_boundary_mean < 0.01:
        return 1.0

    return round(boundary_mean / non_boundary_mean, 4)


def load_frames_gray(video_path, roi_str=None, max_frames=60):
    """Load grayscale frames from video as a numpy stack.

    Returns (stack, fps) where stack has shape (n_frames, height, width).
    Samples evenly across the video if it has more than max_frames.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open video: {video_path}")

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    rx, ry, rw, rh = parse_roi(roi_str, width, height)

    # Decide which frames to read
    if total <= max_frames:
        indices = set(range(total))
    else:
        indices = set(np.linspace(0, total - 1, max_frames, dtype=int))

    frames = []
    idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if idx in indices:
            roi = frame[ry:ry+rh, rx:rx+rw]
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            frames.append(gray)
        idx += 1
    cap.release()

    if len(frames) < 2:
        return None, fps
    return np.array(frames, dtype=np.uint8), fps


def compute_snr(corr_window):
    """Signal-to-noise ratio: peak correlation / mean of remainder.

    corr_window is a 2D correlation map for one interrogation window.
    Returns the ratio of the maximum value to the mean of non-peak values.
    """
    peak = np.nanmax(corr_window)
    if peak == 0 or np.isnan(peak):
        return 0.0
    # Mask out a 3x3 region around the peak
    mask = np.ones_like(corr_window, dtype=bool)
    peak_pos = np.unravel_index(np.nanargmax(corr_window), corr_window.shape)
    py, px = peak_pos
    y_lo = max(0, py - 1)
    y_hi = min(corr_window.shape[0], py + 2)
    x_lo = max(0, px - 1)
    x_hi = min(corr_window.shape[1], px + 2)
    mask[y_lo:y_hi, x_lo:x_hi] = False
    remainder = corr_window[mask]
    remainder = remainder[~np.isnan(remainder)]
    if len(remainder) == 0:
        return 0.0
    noise = np.mean(remainder)
    if noise < 1e-6:
        return peak / 1e-6  # cap at very high SNR
    return peak / noise


def analyze_piv(video_path, roi_str=None, window_size=64, overlap=32):
    """Run FFPIV cross-correlation on video frames and report quality metrics.

    Returns a dict with correlation, SNR, displacement, and pass-rate stats,
    or None if ffpiv is not available or analysis fails.
    """
    if not HAS_FFPIV:
        return None

    stack, fps = load_frames_gray(video_path, roi_str, max_frames=60)
    if stack is None:
        return None

    n_frames = stack.shape[0]
    ws = (window_size, window_size)
    ov = (overlap, overlap)

    # Get correlation maps: shape (n_pairs, n_windows, corr_h, corr_w)
    try:
        x_coords, y_coords, corr = ffpiv.cross_corr(
            stack, window_size=ws, overlap=ov, verbose=False
        )
    except Exception as e:
        print(f"  ffpiv cross_corr failed: {e}", file=sys.stderr)
        return None

    n_pairs = corr.shape[0]
    n_windows = corr.shape[1]

    # Peak correlation per window per pair
    peak_corr = np.nanmax(corr, axis=(-1, -2))  # (n_pairs, n_windows)

    # SNR per window per pair
    snr = np.zeros_like(peak_corr)
    for p in range(n_pairs):
        for w in range(n_windows):
            snr[p, w] = compute_snr(corr[p, w])

    # Displacement vectors
    try:
        u, v = ffpiv.piv_stack(stack, window_size=ws, overlap=ov)
        displacement = np.sqrt(u**2 + v**2)  # pixels per frame
    except Exception as e:
        print(f"  ffpiv piv_stack failed: {e}", file=sys.stderr)
        displacement = None

    # Pass rates using pyorc defaults
    corr_min = 0.2
    s2n_min = 3.0
    pass_corr = peak_corr >= corr_min
    pass_snr = snr >= s2n_min
    pass_both = pass_corr & pass_snr

    # Displacement vs 1/4-window rule
    quarter_window = window_size / 4.0
    if displacement is not None:
        disp_flat = displacement[~np.isnan(displacement)]
        pass_disp = disp_flat[disp_flat <= quarter_window]
        disp_ok_pct = 100.0 * len(pass_disp) / len(disp_flat) if len(disp_flat) > 0 else 0
    else:
        disp_flat = np.array([])
        disp_ok_pct = 0

    flat_corr = peak_corr[~np.isnan(peak_corr)]
    flat_snr = snr[~np.isnan(snr)]

    result = {
        "piv_frames_used": n_frames,
        "piv_pairs": n_pairs,
        "piv_windows_per_pair": n_windows,
        "piv_window_size": window_size,
        "piv_overlap": overlap,
        # Correlation stats
        "corr_median": round(float(np.median(flat_corr)), 3) if len(flat_corr) else 0,
        "corr_p25": round(float(np.percentile(flat_corr, 25)), 3) if len(flat_corr) else 0,
        "corr_p75": round(float(np.percentile(flat_corr, 75)), 3) if len(flat_corr) else 0,
        "corr_pass_pct": round(100.0 * np.sum(pass_corr) / pass_corr.size, 1),
        # SNR stats
        "snr_median": round(float(np.median(flat_snr)), 2) if len(flat_snr) else 0,
        "snr_p25": round(float(np.percentile(flat_snr, 25)), 2) if len(flat_snr) else 0,
        "snr_p75": round(float(np.percentile(flat_snr, 75)), 2) if len(flat_snr) else 0,
        "snr_pass_pct": round(100.0 * np.sum(pass_snr) / pass_snr.size, 1),
        # Combined pass rate — the key number
        "piv_pass_pct": round(100.0 * np.sum(pass_both) / pass_both.size, 1),
        # Displacement stats (pixels/frame)
        "disp_median": round(float(np.median(disp_flat)), 2) if len(disp_flat) else 0,
        "disp_p25": round(float(np.percentile(disp_flat, 25)), 2) if len(disp_flat) else 0,
        "disp_p75": round(float(np.percentile(disp_flat, 75)), 2) if len(disp_flat) else 0,
        "disp_max": round(float(np.max(disp_flat)), 2) if len(disp_flat) else 0,
        "disp_quarter_window": quarter_window,
        "disp_in_range_pct": round(disp_ok_pct, 1),
    }
    return result


def print_scorecard(info, metrics, piv=None):
    """Print a formatted scorecard."""
    print()
    print(f"{'='*60}")
    print(f"  VIDEO QUALITY SCORECARD — {info['file']}")
    print(f"{'='*60}")
    print()

    print("  Container:")
    print(f"    Resolution:   {info['width']}x{info['height']}")
    print(f"    Codec:        {info['codec']}")
    print(f"    Duration:     {info['duration_s']}s")
    print(f"    Frames:       {info['nb_frames']}")
    print(f"    FPS:          {info['fps']}")
    print(f"    Bitrate:      {info['bitrate_kbps']} kbps"
          f"  {'*** BELOW 15000' if info['bitrate_kbps'] < 15000 else ''}"
          f"  {'*** BELOW 20000' if 15000 <= info['bitrate_kbps'] < 20000 else ''}")
    print()

    print(f"  Analysis (ROI: {metrics['roi']}, {metrics['frames_analyzed']} frames):")
    print()

    # SI assessment (thresholds are estimates — validate with ORC processing)
    si = metrics['si_mean']
    si_grade = "HIGH" if si > 40 else "MODERATE" if si > 25 else "LOW" if si > 15 else "VERY LOW"
    print(f"    Spatial Info (SI):    {si:6.1f}  [{si_grade}]")
    print(f"      (range: {metrics['si_min']:.1f} — {metrics['si_max']:.1f}, "
          f"std: {metrics['si_std']:.1f})")
    print(f"      Higher = more texture. No ORC minimum defined — compare across profiles.")
    print()

    # TI assessment (thresholds are estimates — validate with ORC processing)
    ti = metrics['ti_mean']
    ti_grade = "HIGH" if ti > 8 else "MODERATE" if ti > 4 else "LOW" if ti > 2 else "VERY LOW"
    print(f"    Temporal Info (TI):   {ti:6.1f}  [{ti_grade}]")
    print(f"      (range: {metrics['ti_min']:.1f} — {metrics['ti_max']:.1f}, "
          f"std: {metrics['ti_std']:.1f})")
    print(f"      Higher = more frame-to-frame motion. Compare across profiles.")
    print()

    # Blockiness assessment
    bl = metrics['blockiness_mean']
    bl_grade = "CLEAN" if bl < 1.05 else "MINOR" if bl < 1.15 else "MODERATE" if bl < 1.3 else "SEVERE"
    print(f"    Blockiness:           {bl:6.3f}  [{bl_grade}]")
    print(f"      (max: {metrics['blockiness_max']:.3f})")
    print(f"      1.0 = no artifacts. Higher = encoder destroying texture.")
    print()

    # Overall assessment
    print("  Assessment:")
    issues = []
    if info['bitrate_kbps'] < 15000:
        issues.append("FAIL: Bitrate below 15 Mbps floor (pyorc recommendation)")
    elif info['bitrate_kbps'] < 20000:
        issues.append("WARN: Bitrate below 20 Mbps target (pyorc recommendation)")
    if bl > 1.3:
        issues.append("FAIL: Severe compression artifacts — texture likely destroyed")
    elif bl > 1.15:
        issues.append("WARN: Moderate compression artifacts — compare with higher-bitrate profile")

    if not issues:
        print("    Bitrate and compression: OK")
    else:
        for issue in issues:
            print(f"    {issue}")

    # PIV analysis (if ffpiv available)
    if piv:
        print()
        print(f"  PIV Analysis ({piv['piv_pairs']} pairs, "
              f"{piv['piv_windows_per_pair']} windows/pair, "
              f"{piv['piv_window_size']}px window):")
        print()

        # Correlation
        corr_grade = ("GOOD" if piv['corr_pass_pct'] > 80 else
                      "FAIR" if piv['corr_pass_pct'] > 50 else "POOR")
        print(f"    Correlation (≥0.2):   {piv['corr_pass_pct']:5.1f}% pass  [{corr_grade}]")
        print(f"      median {piv['corr_median']:.3f}  "
              f"(p25: {piv['corr_p25']:.3f}, p75: {piv['corr_p75']:.3f})")

        # SNR
        snr_grade = ("GOOD" if piv['snr_pass_pct'] > 80 else
                     "FAIR" if piv['snr_pass_pct'] > 50 else "POOR")
        print(f"    SNR (≥3.0):           {piv['snr_pass_pct']:5.1f}% pass  [{snr_grade}]")
        print(f"      median {piv['snr_median']:.2f}  "
              f"(p25: {piv['snr_p25']:.2f}, p75: {piv['snr_p75']:.2f})")

        # Combined
        piv_grade = ("GOOD" if piv['piv_pass_pct'] > 70 else
                     "FAIR" if piv['piv_pass_pct'] > 40 else "POOR")
        print(f"    Combined pass rate:   {piv['piv_pass_pct']:5.1f}%       [{piv_grade}]")
        print()

        # Displacement
        disp_grade = ("OK" if piv['disp_in_range_pct'] > 90 else
                      "WARN" if piv['disp_in_range_pct'] > 70 else "BAD")
        print(f"    Displacement:         median {piv['disp_median']:.1f} px/frame  "
              f"(max {piv['disp_max']:.1f})")
        print(f"      ≤ ¼ window ({piv['disp_quarter_window']:.0f}px): "
              f"{piv['disp_in_range_pct']:.1f}%  [{disp_grade}]")
        if piv['disp_in_range_pct'] < 90:
            print(f"      Consider {'larger window or lower FPS'}"
                  f" to keep displacement under ¼ window")
    elif HAS_FFPIV:
        print()
        print("  PIV Analysis: failed (see stderr)")
    else:
        print()
        print("  PIV Analysis: skipped (install ffpiv: pip install ffpiv)")

    print()
    print(f"{'='*60}")
    print()


def print_comparison(results):
    """Print side-by-side comparison of multiple videos."""
    print()
    print(f"{'='*80}")
    print("  PROFILE COMPARISON")
    print(f"{'='*80}")
    print()

    header = f"  {'Metric':<25}"
    for r in results:
        header += f" {r['info']['file'][:18]:>18}"
    print(header)
    print(f"  {'-'*25}" + "".join(f" {'-'*18}" for _ in results))

    rows = [
        ("Resolution", lambda r: f"{r['info']['width']}x{r['info']['height']}"),
        ("Bitrate (kbps)", lambda r: f"{r['info']['bitrate_kbps']:.0f}"),
        ("Frames", lambda r: f"{r['info']['nb_frames']}"),
        ("FPS", lambda r: f"{r['info']['fps']}"),
        ("SI mean", lambda r: f"{r['metrics']['si_mean']:.1f}"),
        ("TI mean", lambda r: f"{r['metrics']['ti_mean']:.1f}"),
        ("Blockiness", lambda r: f"{r['metrics']['blockiness_mean']:.3f}"),
    ]

    # Add PIV rows if any result has PIV data
    has_piv = any(r.get("piv") for r in results)
    if has_piv:
        rows.extend([
            ("", lambda r: ""),  # blank separator
            ("PIV pass rate %", lambda r: f"{r['piv']['piv_pass_pct']:.1f}" if r.get("piv") else "n/a"),
            ("  Corr pass %", lambda r: f"{r['piv']['corr_pass_pct']:.1f}" if r.get("piv") else "n/a"),
            ("  SNR pass %", lambda r: f"{r['piv']['snr_pass_pct']:.1f}" if r.get("piv") else "n/a"),
            ("  Corr median", lambda r: f"{r['piv']['corr_median']:.3f}" if r.get("piv") else "n/a"),
            ("  SNR median", lambda r: f"{r['piv']['snr_median']:.2f}" if r.get("piv") else "n/a"),
            ("Disp median (px/fr)", lambda r: f"{r['piv']['disp_median']:.1f}" if r.get("piv") else "n/a"),
            ("Disp in range %", lambda r: f"{r['piv']['disp_in_range_pct']:.1f}" if r.get("piv") else "n/a"),
        ])

    for label, fn in rows:
        line = f"  {label:<25}"
        for r in results:
            line += f" {fn(r):>18}"
        print(line)

    if has_piv:
        print()
        print("  PIV pass rate = % of windows passing both corr≥0.2 AND snr≥3.0")
        print("  Disp in range = % of displacements ≤ ¼ interrogation window")

    print()
    print(f"{'='*80}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Measure video quality metrics for ORC suitability")
    parser.add_argument("videos", nargs="+", help="Video file(s) to analyze")
    parser.add_argument("--roi", default=None,
                        help="Region of interest: x,y,width,height (pixels)")
    parser.add_argument("--compare", action="store_true",
                        help="Print side-by-side comparison table")
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON instead of formatted text")
    parser.add_argument("--no-piv", action="store_true",
                        help="Skip PIV analysis even if ffpiv is installed")
    parser.add_argument("--window-size", type=int, default=64,
                        help="PIV interrogation window size in pixels (default: 64)")
    parser.add_argument("--piv-overlap", type=int, default=None,
                        help="PIV window overlap in pixels (default: window_size/2)")
    args = parser.parse_args()

    piv_overlap = args.piv_overlap if args.piv_overlap is not None else args.window_size // 2
    run_piv = HAS_FFPIV and not args.no_piv

    results = []
    for video in args.videos:
        if not os.path.exists(video):
            print(f"SKIP: {video} not found", file=sys.stderr)
            continue

        info = get_ffprobe_info(video)
        metrics = analyze_frames(video, args.roi)

        piv = None
        if run_piv:
            piv = analyze_piv(video, args.roi, args.window_size, piv_overlap)

        entry = {"info": info, "metrics": metrics, "piv": piv}
        results.append(entry)

        if args.json:
            out = {**info, **metrics}
            if piv:
                out.update(piv)
            print(json.dumps(out, indent=2))
        elif not args.compare:
            print_scorecard(info, metrics, piv)

    if args.compare and len(results) > 1:
        print_comparison(results)


if __name__ == "__main__":
    main()
