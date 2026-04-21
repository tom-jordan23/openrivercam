#!/usr/bin/env python3
"""orc_auto_fit — automated GCP detection + MAGSAC PnP fit.

Phase 1 MVP per AUTO_FIT_DESIGN.md v0.2. Stages:

    1. Bootstrap pose from CAM + GCP centroid look-at.
    2. For each surveyed GCP:
         - project its UTM into pixel space
         - run the local checker-score detector in a window around the
           projection
         - if detected, sub-pixel refine
    3. Collect (UTM, pixel) correspondences, run cv2.solvePnPRansac with
       USAC_MAGSAC, report per-GCP residuals in world-metres.
    4. Write outputs into a timestamped run directory so multiple
       iterations never collide.

Deferred to later phases:

    - Phase 1.5: photo pose-prior (conditional on A1 failing).
    - Phase 2:   subset search for minimum RMSE.
    - Phase 3:   tests, `--from-auto` plumbing, usage doc.

Example:

    python3 survey/orc_auto_fit.py \\
        --video  spring_2026_ID/survey_data/source_data/20260420T034813.mp4 \\
        --gcps   spring_2026_ID/survey_data/output/gcps.csv \\
        --camera-position spring_2026_ID/survey_data/output/camera_position.csv \\
        --water-level     spring_2026_ID/survey_data/output/water_level.csv \\
        --gt-clicks       survey/tests/fixtures/sukabumi_gt_clicks_v1.json \\
        --site   sukabumi \\
        --tag    dry_run_1
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

import cv2
import numpy as np

# Allow running as a script without installing the package
_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from auto_fit import bootstrap as bs
from auto_fit import detect_local as dl
from auto_fit import refine as rf
from auto_fit import report as rp
from auto_fit import visualize as vz
from auto_fit import subset_search as ss
from auto_fit import plots as pl


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def load_frame(video_path: Path, frame_idx: int) -> np.ndarray:
    cap = cv2.VideoCapture(str(video_path))
    n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if frame_idx < 0 or frame_idx >= n:
        cap.release()
        raise SystemExit(
            f"frame_index {frame_idx} out of range (video has {n} frames)"
        )
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
    ok, frame_bgr = cap.read()
    cap.release()
    if not ok:
        raise SystemExit(f"could not read frame {frame_idx} from {video_path}")
    return frame_bgr


def frame_sha256_png(frame_bgr: np.ndarray) -> str:
    ok, buf = cv2.imencode(".png", frame_bgr)
    if not ok:
        raise RuntimeError("failed to PNG-encode frame")
    return hashlib.sha256(buf.tobytes()).hexdigest()


def load_water_level(path: Path) -> float:
    with open(path) as f:
        r = csv.DictReader(f)
        row = next(r)
        return float(row["z"])


def load_pole_lengths_cm(path: Path | None) -> dict[str, float]:
    """Read pole_lengths.csv (Station,Pole_Len_Cm,...) into a dict."""
    if path is None or not path.exists():
        return {}
    out: dict[str, float] = {}
    with open(path) as f:
        r = csv.DictReader(f)
        for row in r:
            name = row["Station"].strip()
            try:
                out[name] = float(row["Pole_Len_Cm"].strip())
            except (ValueError, KeyError):
                pass
    return out


def classify_pairs(
    world_by_id: dict,
    pixel_by_id: dict | None = None,
    pixel_same_marker_threshold: float = 15.0,
) -> dict:
    """Classify each day-1 / day-2 pair by whether the pixel clicks
    actually land on the same physical marker.

    A `.2` label is *supposed* to mean "re-occupation of the day-1 GCP
    with the same suffix-stripped name." That assumption can be checked
    against human clicks on the calibration frame: if both labels got
    clicked on the same feature (pixel distance < threshold) the pair
    is a legitimate re-occupation, and the UTM-space disagreement is
    survey drift. If the clicks landed on completely different features
    in the frame, the `.2` label is a field mislabel — the two points
    are different physical markers and their UTM distance is real
    geometry, not drift.

    Returns a dict keyed by BOTH members of each pair with entries:
        {
          "utm_distance_m": float,
          "click_pixel_distance": float | None,
          "classification": "same_marker_drift" | "different_markers" | "unknown",
          "partner": str,
        }
    """
    out: dict = {}
    for gid, xyz in world_by_id.items():
        if not gid.endswith(".2"):
            continue
        base = gid[:-2]
        if base not in world_by_id:
            continue
        utm_d = float(np.linalg.norm(xyz - world_by_id[base]))

        click_d = None
        if pixel_by_id is not None:
            b = pixel_by_id.get(base)
            s = pixel_by_id.get(gid)
            if b is not None and s is not None:
                click_d = float(np.hypot(b[0] - s[0], b[1] - s[1]))

        if click_d is None:
            cls = "unknown"
        elif click_d < pixel_same_marker_threshold:
            cls = "same_marker_drift"
        else:
            cls = "different_markers"

        for member, partner in ((gid, base), (base, gid)):
            out[member] = {
                "utm_distance_m": utm_d,
                "click_pixel_distance": click_d,
                "classification": cls,
                "partner": partner,
            }
    return out


def compute_pair_drift_m(
    world_by_id: dict,
    pixel_by_id: dict | None = None,
) -> dict:
    """Back-compat helper: returns only the same-marker drifts (i.e.
    the values where the pair-drift story is real). Consumers wanting
    the full classification should call classify_pairs() instead."""
    classes = classify_pairs(world_by_id, pixel_by_id=pixel_by_id)
    return {
        gid: info["utm_distance_m"]
        for gid, info in classes.items()
        if info["classification"] == "same_marker_drift"
    }


def load_gt_clicks(path: Path) -> dict:
    return json.loads(path.read_text())


def evaluate_a1(
    detected: dict[str, tuple[float, float]],
    gt_clicks: dict[str, list[float]],
    camera_position: np.ndarray,
    world_points_by_id: dict[str, np.ndarray],
    focal_px: float,
    target_m: float = 0.05,
) -> dict:
    """Compare auto-detected pixel locations to ground-truth clicks.

    Convert pixel distances to world-metres using per-GCP camera range so
    the numbers are comparable across near / far GCPs.
    """
    n_compared = 0
    n_within = 0
    per_gcp: dict[str, dict] = {}
    for gid, auto_xy in detected.items():
        if gid not in gt_clicks:
            continue
        gt = gt_clicks[gid]
        if gt is None:
            continue
        dx = auto_xy[0] - gt[0]
        dy = auto_xy[1] - gt[1]
        dist_px = float(np.hypot(dx, dy))
        # metres conversion via GCP's actual distance to the camera
        world_pt = world_points_by_id.get(gid)
        if world_pt is None:
            continue
        range_m = float(np.linalg.norm(world_pt - camera_position))
        dist_m = dist_px * range_m / focal_px
        per_gcp[gid] = {
            "pixel_error": dist_px,
            "metre_error": dist_m,
            "range_m": range_m,
        }
        n_compared += 1
        if dist_m <= target_m:
            n_within += 1
    worst = sorted(per_gcp.items(), key=lambda kv: -kv[1]["metre_error"])
    return {
        "ground_truth_available": True,
        "target_m": target_m,
        "n_compared": n_compared,
        "n_within_target": n_within,
        "per_gcp": per_gcp,
        "worst": [g for g, _ in worst],
    }


def save_clicks_json(path: Path, clicks: dict[str, tuple[float, float]]) -> None:
    path.write_text(
        json.dumps(
            {gid: [round(x, 2), round(y, 2)] for gid, (x, y) in clicks.items()},
            indent=2,
        )
        + "\n"
    )


def make_run_dir(base: Path, site: str, tag: str) -> Path:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    tag_clean = tag.replace(" ", "_")
    run = base / f"{ts}_{site}_{tag_clean}"
    run.mkdir(parents=True, exist_ok=False)
    return run


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Automated GCP detection + MAGSAC PnP fit (Phase 1 MVP).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument("--video", type=Path, required=True)
    ap.add_argument("--gcps", type=Path, required=True)
    ap.add_argument("--camera-position", type=Path, required=True)
    ap.add_argument("--water-level", type=Path,
                    help="water_level.csv for z_0 (not required for MVP)")
    ap.add_argument("--gt-clicks", type=Path,
                    help="Phase 0 ground-truth clicks JSON; if supplied, A1 is evaluated")
    ap.add_argument("--frame-index", type=int, default=0,
                    help="Video frame index to fit against (default 0)")
    ap.add_argument("--site", required=True)
    ap.add_argument("--tag", default="run",
                    help="Short tag for this run (used in the output dir name)")
    ap.add_argument("--focal-px", type=float, default=bs.DEFAULT_FOCAL_PX,
                    help="Bootstrap focal length (px); frozen for the run")
    ap.add_argument("--window-passes", type=int, nargs="+", default=[60, 30],
                    help="Half-window (px) for each refinement pass. Multiple values -> multiple passes, typically shrinking")
    ap.add_argument("--score-threshold", type=float,
                    default=dl.DEFAULT_SCORE_THRESHOLD)
    ap.add_argument("--reprojection-px", type=float, default=8.0,
                    help="RANSAC reprojection threshold (px) for MAGSAC PnP")
    ap.add_argument("--a1-target-m", type=float, default=0.05,
                    help="A1 acceptance threshold (world metres); default 0.05 = 5 cm")
    ap.add_argument("--rng-seed", type=int, default=0)
    ap.add_argument("--output-base", type=Path,
                    default=Path("spring_2026_ID/survey_data/auto_fit_runs"),
                    help="Parent directory for per-run output folders")
    ap.add_argument("--pole-lengths",
                    type=Path,
                    default=Path("spring_2026_ID/survey_data/pole_lengths.csv"),
                    help="Optional: pole_lengths.csv for diagnostic plot"
                         " hatching (bamboo-pole GCPs flagged).")
    ap.add_argument("--bootstrap-from-gt", action="store_true",
                    help="Derive the bootstrap pose from the ground-truth "
                         "clicks (requires --gt-clicks). Isolates detector "
                         "quality from bootstrap-pose-construction errors.")
    ap.add_argument("--use-clicks", type=Path,
                    help="Skip auto-detection entirely and use the provided "
                         "clicks JSON directly as the correspondence set. "
                         "Same format as --gt-clicks. The pipeline still "
                         "runs MAGSAC PnP, produces per-GCP residuals, and "
                         "writes the visualization. Use this to measure the "
                         "achievable fit quality given trusted pixels, "
                         "independent of detector quality. Implies "
                         "--bootstrap-from-gt semantically; the detector "
                         "loop is replaced by the clicks file.")
    ap.add_argument("--subset-search", action="store_true",
                    help="After the initial fit, run Stage-3 subset search "
                         "(greedy drop-one + conditional exhaustive). "
                         "Produces the lowest-RMSE subset of ≥ 6 GCPs with "
                         "coverage across all four image quadrants. "
                         "Implementation per AUTO_FIT_DESIGN.md §5.3.")
    ap.add_argument("--min-subset-size", type=int, default=6)
    ap.add_argument("--exhaustive-below-n", type=int, default=15,
                    help="Run exhaustive search over C(n, k..n) if the "
                         "greedy result has n ≤ this value (default 15).")
    args = ap.parse_args(argv)

    # --- Load inputs -------------------------------------------------------
    frame_bgr = load_frame(args.video, args.frame_index)
    frame_gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
    frame_h, frame_w = frame_gray.shape
    frame_sha = frame_sha256_png(frame_bgr)

    gcps = bs.load_gcps(args.gcps)
    gcps_sha = sha256_file(args.gcps)
    camera_xyz = bs.load_camera_position(args.camera_position)

    world_by_id = {gid: p for gid, p in gcps}
    gt = load_gt_clicks(args.gt_clicks) if args.gt_clicks else None
    gt_clicks = gt.get("clicks", {}) if gt else None

    # --- Run directory -----------------------------------------------------
    run_dir = make_run_dir(args.output_base, args.site, args.tag)
    print(f"run directory: {run_dir}")

    # Snapshot the frame we actually used
    cv2.imwrite(str(run_dir / "frame.png"), frame_bgr)
    (run_dir / "frame.sha256").write_text(frame_sha + "\n")

    # --- Stage 1: bootstrap pose ------------------------------------------
    boot = bs.bootstrap_pose(
        gcps=gcps,
        camera_position=camera_xyz,
        frame_size=(frame_w, frame_h),
        focal_px=args.focal_px,
    )
    bootstrap_source = "look_at"

    # Optional: override the bootstrap by solving PnP on the GT clicks.
    # Isolates "detector works given correct pose" from "bootstrap is wrong."
    if args.bootstrap_from_gt:
        if gt_clicks is None:
            raise SystemExit(
                "--bootstrap-from-gt requires --gt-clicks; none supplied"
            )
        gt_ids = [gid for gid, _ in gcps if gid in gt_clicks]
        if len(gt_ids) < 6:
            raise SystemExit(
                f"--bootstrap-from-gt needs ≥ 6 GT clicks; only {len(gt_ids)} "
                "in the fixture"
            )
        gt_wp = np.array([world_by_id[g] for g in gt_ids])
        gt_ip = np.array([gt_clicks[g] for g in gt_ids])
        gt_res = rf.refine_pose_magsac(
            gcp_ids=gt_ids,
            world_points=gt_wp,
            image_points=gt_ip,
            K=boot.K,
            dist_coeffs=boot.dist_coeffs,
            camera_position_world=camera_xyz,
            reprojection_threshold_px=args.reprojection_px,
            rng_seed=args.rng_seed,
        )
        if gt_res is None:
            raise SystemExit("PnP on GT clicks failed")
        boot.rvec = gt_res.rvec
        boot.tvec = gt_res.tvec
        bootstrap_source = "pnp_on_gt"
        print(
            f"bootstrap pose: derived from GT clicks — PnP on "
            f"{len(gt_res.inlier_ids)}/{len(gt_ids)} inliers, "
            f"rmse={gt_res.rmse_px:.2f} px / {gt_res.rmse_m:.4f} m"
        )
    print(
        f"bootstrap source: {bootstrap_source}  "
        f"GCP centroid = ({boot.gcp_centroid_world[0]:.2f}, "
        f"{boot.gcp_centroid_world[1]:.2f}, {boot.gcp_centroid_world[2]:.2f})"
    )

    # Project each GCP under the bootstrap pose
    world_array = np.array([world_by_id[gid] for gid, _ in gcps])
    projected_initial = bs.project_points(
        world_array, boot.K, boot.dist_coeffs, boot.rvec, boot.tvec
    )
    bootstrap_proj = {
        gid: (float(p[0]), float(p[1]))
        for (gid, _), p in zip(gcps, projected_initial)
    }
    print(f"bootstrap projections computed for {len(gcps)} GCPs")

    # --- Stage 2: project-detect-refine loop ------------------------------
    rvec = boot.rvec
    tvec = boot.tvec
    K = boot.K
    dist = boot.dist_coeffs

    detections_per_pass: list[dict] = []
    per_gcp_scores: dict[str, float] = {}
    per_gcp_accepted: dict[str, bool] = {}
    final_detections: dict[str, tuple[float, float]] = {}

    # Short-circuit: --use-clicks replaces the detector loop with the
    # supplied clicks verbatim. Useful for measuring achievable fit quality
    # when detection is unreliable (see AUTO_FIT_DESIGN.md §8 risk row 1).
    if args.use_clicks:
        clicks_in = json.loads(args.use_clicks.read_text())
        clicks_dict = clicks_in.get("clicks", clicks_in)
        for gid, xy in clicks_dict.items():
            if xy is None:
                continue
            final_detections[gid] = (float(xy[0]), float(xy[1]))
            per_gcp_accepted[gid] = True
            per_gcp_scores[gid] = float("inf")  # trusted by user
        detections_per_pass.append({
            "pass": "use_clicks",
            "source": str(args.use_clicks),
            "n_accepted": len(final_detections),
            "note": "detector loop skipped; clicks used verbatim",
        })
        print(
            f"--use-clicks: skipping detector, loaded "
            f"{len(final_detections)} clicks from {args.use_clicks}"
        )

    for pass_i, half in enumerate(args.window_passes if not args.use_clicks else []):
        # project with current pose
        projected = bs.project_points(world_array, K, dist, rvec, tvec)
        pass_detections: list[dict] = []
        correspondences: list[tuple[str, np.ndarray, np.ndarray]] = []

        for (gid, _), pred in zip(gcps, projected):
            det = dl.detect_in_window(
                frame_gray,
                predicted_xy=(float(pred[0]), float(pred[1])),
                half_window=int(half),
                score_threshold=float(args.score_threshold),
            )
            if det.accepted:
                x_ref, y_ref = dl.refine_subpixel(
                    frame_gray, (det.x, det.y), window=5
                )
                final_detections[gid] = (x_ref, y_ref)
                correspondences.append((gid, world_by_id[gid],
                                        np.array([x_ref, y_ref])))
            per_gcp_scores[gid] = det.score if np.isfinite(det.score) else float("nan")
            per_gcp_accepted[gid] = det.accepted
            pass_detections.append({
                "gcp": gid,
                "predicted_px": [float(pred[0]), float(pred[1])],
                "detected_px": [det.x, det.y] if det.accepted else None,
                "score": det.score if np.isfinite(det.score) else None,
                "scale": det.scale,
                "accepted": det.accepted,
                "n_candidates_in_window": det.n_candidates,
                "window_half_px": int(half),
            })

        detections_per_pass.append({
            "pass": pass_i,
            "window_half_px": int(half),
            "n_accepted": sum(1 for d in pass_detections if d["accepted"]),
            "detections": pass_detections,
        })
        print(
            f"pass {pass_i} (half={half} px): "
            f"{sum(1 for d in pass_detections if d['accepted'])}/{len(gcps)} detected"
        )

        # refine pose from accepted detections
        if len(correspondences) >= 4:
            ids = [c[0] for c in correspondences]
            wp = np.array([c[1] for c in correspondences])
            ip = np.array([c[2] for c in correspondences])
            result = rf.refine_pose_magsac(
                gcp_ids=ids,
                world_points=wp,
                image_points=ip,
                K=K,
                dist_coeffs=dist,
                camera_position_world=camera_xyz,
                reprojection_threshold_px=args.reprojection_px,
                rng_seed=args.rng_seed,
            )
            if result is not None:
                rvec = result.rvec
                tvec = result.tvec
                print(
                    f"  refined pose: inliers={len(result.inlier_ids)}/{len(ids)} "
                    f"rmse={result.rmse_px:.2f} px / {result.rmse_m:.4f} m"
                )

    # --- Final MAGSAC over the final detection set ------------------------
    if len(final_detections) < 4:
        print(
            f"ERROR: only {len(final_detections)} GCPs detected; need ≥ 4 "
            "for PnP. Dumping diagnostic outputs and exiting.",
            file=sys.stderr,
        )
        (run_dir / "detections_by_pass.json").write_text(
            json.dumps(detections_per_pass, indent=2)
        )
        return 2

    ids = list(final_detections.keys())
    wp = np.array([world_by_id[g] for g in ids])
    ip = np.array([list(final_detections[g]) for g in ids])
    final_result = rf.refine_pose_magsac(
        gcp_ids=ids,
        world_points=wp,
        image_points=ip,
        K=K,
        dist_coeffs=dist,
        camera_position_world=camera_xyz,
        reprojection_threshold_px=args.reprojection_px,
        rng_seed=args.rng_seed,
    )
    if final_result is None:
        print("ERROR: final PnP failed on detected set.", file=sys.stderr)
        return 3

    # --- Stage 3: subset search (optional) --------------------------------
    subset_result = None
    if args.subset_search:
        print()
        print("running subset search (greedy drop-one + exhaustive)...")
        pixel_by_id = {g: tuple(final_detections[g]) for g in ids}
        subset_result = ss.subset_search(
            all_ids=ids,
            world_by_id=world_by_id,
            pixel_by_id=pixel_by_id,
            K=K,
            dist_coeffs=dist,
            camera_position_world=camera_xyz,
            init_rvec=final_result.rvec,
            init_tvec=final_result.tvec,
            frame_size=(frame_w, frame_h),
            min_size=args.min_subset_size,
            require_all_quadrants=True,
            exhaustive_below_n=args.exhaustive_below_n,
        )
        b = subset_result.best
        print(f"  baseline ({len(ids)} GCPs):  rmse = "
              f"{subset_result.baseline.rmse_px:.2f} px / "
              f"{subset_result.baseline.rmse_m:.4f} m")
        print(f"  greedy steps:               {len(subset_result.greedy_trajectory) - 1}")
        print(f"  exhaustive subsets scored:  {subset_result.exhaustive_considered}")
        print(f"  best subset ({len(b.ids)} GCPs): {list(b.ids)}")
        print(f"  best RMSE:                  {b.rmse_px:.2f} px / {b.rmse_m:.4f} m")

        # Compute per-GCP residuals for ALL clicked GCPs under the
        # best-subset pose. The 6 chosen GCPs have small residuals; the
        # excluded ones' residuals show HOW MUCH they disagreed.
        all_clicked_ids = list(pixel_by_id.keys())
        clicked_wp = np.array([world_by_id[g] for g in all_clicked_ids])
        clicked_ip = np.array([list(pixel_by_id[g]) for g in all_clicked_ids])
        projected_under_best, _ = cv2.projectPoints(
            clicked_wp.reshape(-1, 1, 3),
            b.rvec, b.tvec, K, dist,
        )
        projected_under_best = projected_under_best.reshape(-1, 2)
        residuals_px_best = np.linalg.norm(
            clicked_ip - projected_under_best, axis=1
        )
        ranges_m_best = np.linalg.norm(clicked_wp - camera_xyz, axis=1)
        focal_px = float(0.5 * (K[0, 0] + K[1, 1]))
        residuals_m_best = (residuals_px_best * ranges_m_best / focal_px).tolist()
        support_residuals_m = {
            gid: float(r) for gid, r in zip(all_clicked_ids, residuals_m_best)
        }
        # Enriching plot with survey-quality diagnostics: pole length
        # (bamboo vs standard) and pair classification (same-marker
        # drift vs. field-mislabelled different markers). The former is
        # an RTK quality signal; the latter is just "these are different
        # points" and should not be conflated with drift.
        pole_lengths = load_pole_lengths_cm(args.pole_lengths)
        pair_classification = classify_pairs(world_by_id, pixel_by_id)
        # Only pass *same-marker* drifts to the plot — showing a "Δpair"
        # annotation on a different-marker pair would perpetuate the
        # mislabel. Different-marker pairs are called out separately.
        pair_drift_for_plot = {
            gid: info["utm_distance_m"]
            for gid, info in pair_classification.items()
            if info["classification"] == "same_marker_drift"
        }

        pl.plot_gcp_support(
            output_path=run_dir / "gcp_support.png",
            clicked_ids=all_clicked_ids,
            residuals_m=support_residuals_m,
            subset_ids=set(b.ids),
            pole_length_cm=pole_lengths,
            pair_drift_m=pair_drift_for_plot,
            a1_target_m=args.a1_target_m,
            noise_floor_m=0.90,
            title=f"GCP support of best-subset geometry "
                  f"(RMSE {b.rmse_m*100:.2f} cm on {len(b.ids)} GCPs)  |  "
                  f"hatched bars = ≥150 cm pole  |  "
                  f"Δpair = day-1/day-2 drift (same-marker only)",
        )
        print(f"  support plot:  {run_dir / 'gcp_support.png'}")

        same_marker = {
            gid: info["utm_distance_m"]
            for gid, info in pair_classification.items()
            if info["classification"] == "same_marker_drift"
        }
        diff_markers = {
            gid: info
            for gid, info in pair_classification.items()
            if info["classification"] == "different_markers"
        }
        if same_marker:
            print("  same-marker pair drift (RTK repeat quality):")
            seen = set()
            for gid, d in sorted(same_marker.items(), key=lambda kv: -kv[1]):
                base = gid[:-2] if gid.endswith(".2") else gid
                if base in seen:
                    continue
                seen.add(base)
                print(f"    {base} ↔ {base}.2:  {d*100:.0f} cm UTM drift")
        if diff_markers:
            print("  mislabelled pairs (clicks land on different markers):")
            seen = set()
            for gid, info in diff_markers.items():
                base = gid[:-2] if gid.endswith(".2") else gid
                if base in seen:
                    continue
                seen.add(base)
                print(
                    f"    {base} vs {base}.2:  clicks {info['click_pixel_distance']:.0f} px apart, "
                    f"{info['utm_distance_m']*100:.0f} cm in UTM — "
                    "these are different physical points; `.2` label is a field mislabel"
                )

    # --- Evaluate A1 if ground truth supplied -----------------------------
    a1_info: dict
    if gt_clicks is not None:
        a1_info = evaluate_a1(
            detected=final_detections,
            gt_clicks=gt_clicks,
            camera_position=camera_xyz,
            world_points_by_id=world_by_id,
            focal_px=float(0.5 * (K[0, 0] + K[1, 1])),
            target_m=args.a1_target_m,
        )
    else:
        a1_info = {"ground_truth_available": False}

    # --- Save outputs -----------------------------------------------------
    clicks_path = run_dir / "clicks.json"
    save_clicks_json(clicks_path, final_detections)

    (run_dir / "detections_by_pass.json").write_text(
        json.dumps(detections_per_pass, indent=2)
    )

    labels_out = {
        gid: {
            "pixel": list(final_detections[gid]),
            "residual_px": final_result.per_gcp_residual_px.get(gid),
            "residual_m": final_result.per_gcp_residual_m.get(gid),
            "inlier": gid in set(final_result.inlier_ids),
        }
        for gid in ids
    }
    (run_dir / "labels.json").write_text(json.dumps(labels_out, indent=2))

    # Full audit trail
    audit = {
        "run_tag": args.tag,
        "site": args.site,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "inputs": {
            "video": str(args.video),
            "frame_index": args.frame_index,
            "frame_sha256": frame_sha,
            "gcps_csv": str(args.gcps),
            "gcps_csv_sha256": gcps_sha,
            "camera_position_csv": str(args.camera_position),
            "gt_clicks": str(args.gt_clicks) if args.gt_clicks else None,
        },
        "parameters": {
            "focal_px": args.focal_px,
            "window_passes": list(args.window_passes),
            "score_threshold": args.score_threshold,
            "reprojection_px": args.reprojection_px,
            "a1_target_m": args.a1_target_m,
            "rng_seed": args.rng_seed,
        },
        "bootstrap": {
            "gcp_centroid_world": boot.gcp_centroid_world.tolist(),
            "camera_position_world": boot.camera_center_world.tolist(),
        },
        "stage2_passes": detections_per_pass,
        "final_fit": {
            "rvec": final_result.rvec.flatten().tolist(),
            "tvec": final_result.tvec.flatten().tolist(),
            "inlier_ids": final_result.inlier_ids,
            "outlier_ids": final_result.outlier_ids,
            "rmse_px": final_result.rmse_px,
            "rmse_m": final_result.rmse_m,
            "per_gcp_residual_px": final_result.per_gcp_residual_px,
            "per_gcp_residual_m": final_result.per_gcp_residual_m,
            "pnp_flags": final_result.pnp_flags,
        },
        "a1": a1_info,
    }
    if subset_result is not None:
        audit["subset_search"] = {
            "constraints": subset_result.constraints,
            "baseline_rmse_px": subset_result.baseline.rmse_px,
            "baseline_rmse_m": subset_result.baseline.rmse_m,
            "greedy_trajectory": [
                {
                    "size": len(ev.ids),
                    "ids": list(ev.ids),
                    "rmse_px": ev.rmse_px,
                    "rmse_m": ev.rmse_m,
                }
                for ev in subset_result.greedy_trajectory
            ],
            "exhaustive_considered": subset_result.exhaustive_considered,
            "exhaustive_best": (
                {
                    "size": len(subset_result.exhaustive_best.ids),
                    "ids": list(subset_result.exhaustive_best.ids),
                    "rmse_px": subset_result.exhaustive_best.rmse_px,
                    "rmse_m": subset_result.exhaustive_best.rmse_m,
                }
                if subset_result.exhaustive_best is not None
                else None
            ),
            "best": {
                "size": len(subset_result.best.ids),
                "ids": list(subset_result.best.ids),
                "rmse_px": subset_result.best.rmse_px,
                "rmse_m": subset_result.best.rmse_m,
                "per_gcp_residual_m": subset_result.best.per_gcp_residual_m,
            },
        }
    (run_dir / "audit.json").write_text(json.dumps(audit, indent=2))

    # Visualization — single most useful diagnostic for iteration.
    final_proj_array = bs.project_points(
        world_array, K, dist, final_result.rvec, final_result.tvec
    )
    final_proj = {
        gid: (float(p[0]), float(p[1]))
        for (gid, _), p in zip(gcps, final_proj_array)
    }
    vz.annotate_run(
        frame_bgr=frame_bgr,
        gcp_ids=[gid for gid, _ in gcps],
        bootstrap_proj=bootstrap_proj,
        final_proj=final_proj,
        detections=final_detections,
        inlier_set=set(final_result.inlier_ids),
        gt_clicks=gt_clicks,
        output_path=run_dir / "annotated.png",
    )

    # Markdown report
    rp.write_report(
        path=run_dir / "report.md",
        run_info={
            "run_tag": args.tag,
            "site": args.site,
            "output_dir": str(run_dir),
            "video": str(args.video),
            "frame_index": args.frame_index,
            "frame_sha256": frame_sha,
            "gcps_csv": str(args.gcps),
            "gcps_csv_sha256": gcps_sha,
            "camera_position_csv": str(args.camera_position),
            "n_gcps": len(gcps),
            "n_accepted": len(final_detections),
            "parameters": audit["parameters"],
        },
        gcp_ids=[gid for gid, _ in gcps],
        per_gcp_px=final_result.per_gcp_residual_px,
        per_gcp_m=final_result.per_gcp_residual_m,
        inlier_ids=final_result.inlier_ids,
        outlier_ids=final_result.outlier_ids,
        detection_scores=per_gcp_scores,
        detection_accepted=per_gcp_accepted,
        detection_skipped=[
            gid for gid, _ in gcps if gid not in final_detections
        ],
        rmse_px=final_result.rmse_px,
        rmse_m=final_result.rmse_m,
        acceptance_a1=a1_info,
        support_plot=("gcp_support.png" if subset_result is not None else None),
        subset_info=audit.get("subset_search"),
        pair_drift_m=(
            classify_pairs(world_by_id, pixel_by_id=pixel_by_id)
            if subset_result is not None else None
        ),
    )

    print()
    print(f"==== done.  run dir: {run_dir} ====")
    print(f"   RMSE (inliers): {final_result.rmse_px:.2f} px  |  "
          f"{final_result.rmse_m:.4f} m")
    if a1_info.get("ground_truth_available"):
        n_t = a1_info["n_compared"]
        n_w = a1_info["n_within_target"]
        pct = 100.0 * n_w / n_t if n_t else 0.0
        print(f"   A1: {n_w}/{n_t} within {args.a1_target_m*100:.0f} cm ({pct:.1f} %)")
    print(f"   open {run_dir}/report.md for the full report")

    return 0


if __name__ == "__main__":
    sys.exit(main())
