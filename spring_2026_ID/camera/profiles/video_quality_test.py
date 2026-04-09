#!/usr/bin/env python3
"""video_quality_test.py — Measure video quality metrics for ORC suitability.

Analyzes captured video files and produces a scorecard of metrics relevant
to ORC surface velocity detection:

  - Delivered bitrate (from container metadata)
  - Spatial Information (SI) — texture/edge detail per frame
  - Temporal Information (TI) — frame-to-frame motion
  - Blockiness index — H.264 compression artifact detection
  - Frame count, effective FPS, resolution

Usage:
    python3 video_quality_test.py VIDEO_FILE
    python3 video_quality_test.py VIDEO_FILE --roi 200,100,1600,900
    python3 video_quality_test.py VIDEO_FILE --compare VIDEO_FILE_2
    python3 video_quality_test.py *.mp4 --summary

ROI (Region of Interest) crops analysis to the water surface area,
excluding sky and bank. Format: x,y,width,height in pixels.

Metrics Reference (ITU-T P.910):
    SI = std_dev(Sobel(frame))     — higher = more texture detail
    TI = std_dev(frame_n - frame_n-1) — higher = more visible motion
    Both correlate with ORC's ability to detect surface velocity patterns.

ORC-Specific Context (from pyorc velocimetry docs):
    - 20 Mbps at 1080p is the recommended bitrate (pyorc docs)
    - 15 Mbps is the practical floor (per Hessel Winsemius)
    - PIV correlation threshold (corr_min) = 0.2
    - PIV signal-to-noise ratio (s2n_min) = 3.0
    - If too many frame pairs fail these, the video is unusable
    - SI/TI thresholds below are ESTIMATES — the definitive test is
      running the video through ORC and checking PIV pass rates

Requires:
    pip install opencv-python-headless numpy
"""

import argparse
import json
import os
import subprocess
import sys

import cv2
import numpy as np


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


def print_scorecard(info, metrics):
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

    print()
    print("  NOTE: SI and TI have no defined ORC minimums. Use --compare")
    print("  across profiles to find the best option, then validate with")
    print("  ORC processing (check PIV corr_min and s2n_min pass rates).")

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

    for label, fn in rows:
        line = f"  {label:<25}"
        for r in results:
            line += f" {fn(r):>18}"
        print(line)

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
    args = parser.parse_args()

    results = []
    for video in args.videos:
        if not os.path.exists(video):
            print(f"SKIP: {video} not found", file=sys.stderr)
            continue

        info = get_ffprobe_info(video)
        metrics = analyze_frames(video, args.roi)
        results.append({"info": info, "metrics": metrics})

        if args.json:
            print(json.dumps({**info, **metrics}, indent=2))
        elif not args.compare:
            print_scorecard(info, metrics)

    if args.compare and len(results) > 1:
        print_comparison(results)


if __name__ == "__main__":
    main()
