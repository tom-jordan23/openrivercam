"""Human-readable Markdown report emitter for auto-fit runs.

A run produces several artefacts (see AUTO_FIT_DESIGN.md §6); this module
produces the single-page .md report that is the human-facing summary.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any


def format_residual_table(
    gcp_ids: list[str],
    per_gcp_px: dict[str, float],
    per_gcp_m: dict[str, float],
    inlier_ids: set[str],
    detection_scores: dict[str, float],
    detection_accepted: dict[str, bool],
) -> str:
    lines = [
        "| GCP | Residual (px) | Residual (m) | Inlier | Detect score | Detect accepted |",
        "|---|---:|---:|:---:|---:|:---:|",
    ]
    # sort worst-first
    order = sorted(
        gcp_ids,
        key=lambda g: per_gcp_m.get(g, float("inf")),
        reverse=True,
    )
    for g in order:
        res_px = per_gcp_px.get(g)
        res_m = per_gcp_m.get(g)
        score = detection_scores.get(g)
        accepted = detection_accepted.get(g, False)
        in_inliers = g in inlier_ids
        px_str = f"{res_px:6.2f}" if res_px is not None else "   —  "
        m_str = f"{res_m:.4f}" if res_m is not None else "  —  "
        score_str = f"{score:5.1f}" if score is not None else "  —  "
        lines.append(
            f"| {g} | {px_str} | {m_str} | {'✓' if in_inliers else '✗'} | "
            f"{score_str} | {'✓' if accepted else '✗'} |"
        )
    return "\n".join(lines)


def write_report(
    path: Path,
    run_info: dict[str, Any],
    gcp_ids: list[str],
    per_gcp_px: dict[str, float],
    per_gcp_m: dict[str, float],
    inlier_ids: list[str],
    outlier_ids: list[str],
    detection_scores: dict[str, float],
    detection_accepted: dict[str, bool],
    detection_skipped: list[str],
    rmse_px: float,
    rmse_m: float,
    acceptance_a1: dict[str, Any],
    certification_status: str = "ok",
    demo_banner: bool = False,
    support_plot: str | None = None,
    subset_info: dict[str, Any] | None = None,
    pair_drift_m: dict[str, float] | None = None,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    lines: list[str] = []
    if demo_banner:
        lines.append(
            "> **DEMO-UNCERTIFIED — do not use for certified flow, discharge,"
            " or water-level measurements.**"
        )
        lines.append("")
    lines.append(f"# Auto-fit report — {run_info.get('run_tag', 'untagged')}")
    lines.append("")
    lines.append(f"Generated {datetime.now().isoformat(timespec='seconds')}")
    lines.append("")
    lines.append(f"- **Site:** {run_info.get('site', '—')}")
    lines.append(f"- **Run directory:** `{run_info.get('output_dir', '—')}`")
    lines.append(f"- **Certification status:** `{certification_status}`")
    lines.append(f"- **Video:** `{run_info.get('video', '—')}` (frame {run_info.get('frame_index', 0)})")
    lines.append(f"- **Frame SHA-256:** `{run_info.get('frame_sha256', '—')}`")
    lines.append(f"- **GCPs CSV:** `{run_info.get('gcps_csv', '—')}` (sha256 `{run_info.get('gcps_csv_sha256', '—')}`)")
    lines.append(f"- **Camera position:** `{run_info.get('camera_position_csv', '—')}`")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(
        f"- **GCPs loaded:** {run_info.get('n_gcps', 0)}"
        f"  |  **detected (accepted):** {run_info.get('n_accepted', 0)}"
        f"  |  **inliers after PnP:** {len(inlier_ids)}"
    )
    lines.append(
        f"- **RMSE on inliers:** {rmse_px:.2f} px  |  {rmse_m:.4f} m (world-ground units)"
    )
    lines.append("")
    if detection_skipped:
        lines.append(
            f"- **Not detected (below score threshold or no corner in window):** "
            f"{', '.join(detection_skipped)}"
        )
    if outlier_ids:
        lines.append(
            f"- **MAGSAC rejected (outliers):** {', '.join(outlier_ids)}"
        )
    lines.append("")
    lines.append("## A1 — Registration accuracy vs ground truth")
    lines.append("")
    if acceptance_a1.get("ground_truth_available"):
        n_total = acceptance_a1.get("n_compared", 0)
        n_within = acceptance_a1.get("n_within_target", 0)
        target_m = acceptance_a1.get("target_m", 0.05)
        pct = (100.0 * n_within / n_total) if n_total else 0.0
        status = "PASS" if pct >= 70.0 else "FAIL"
        lines.append(
            f"- {n_within}/{n_total} GCPs within {target_m*100:.0f} cm of"
            f" manual click (**{pct:.1f} %**). Target ≥ 70 %. → **{status}**"
        )
        worst = acceptance_a1.get("worst", [])
        if worst:
            lines.append(f"- Worst offenders: {', '.join(worst[:5])}")
    else:
        lines.append(
            "- Ground-truth file not supplied — A1 not evaluated this run. "
            "Re-run with `--gt-clicks <path>` once Phase 0 is complete."
        )
    lines.append("")
    if subset_info:
        lines.append("## Subset search (Stage 3)")
        lines.append("")
        best = subset_info.get("best", {})
        baseline = subset_info.get("baseline_rmse_m", None)
        lines.append(
            f"- **Baseline** (all {len(gcp_ids)} GCPs): RMSE = "
            f"{baseline*100:.2f} cm" if baseline is not None else "- Baseline: —"
        )
        lines.append(
            f"- **Best subset** ({best.get('size', '—')} GCPs, "
            f"exhaustive over {subset_info.get('exhaustive_considered', '—')} "
            f"valid subsets): **RMSE = {best.get('rmse_m', 0)*100:.2f} cm**"
        )
        lines.append(f"- **Chosen GCPs:** `{', '.join(best.get('ids', []))}`")
        traj = subset_info.get("greedy_trajectory", [])
        if traj:
            lines.append("")
            lines.append("Greedy drop-one trajectory (each step = 1 GCP removed):")
            lines.append("")
            lines.append("| |S| | RMSE (cm) |")
            lines.append("|---:|---:|")
            for ev in traj:
                lines.append(f"| {ev['size']} | {ev['rmse_m']*100:.2f} |")
        lines.append("")

    if support_plot:
        lines.append("## Why this survey was hard — GCP support of the geometry")
        lines.append("")
        lines.append(f"![GCP support of best-subset geometry]({support_plot})")
        lines.append("")
        lines.append(
            "Bars show each clicked GCP's reprojection residual under the"
            " best-subset pose, on a log scale. **Green** = chosen for the"
            " best fit; **orange** = excluded by the subset search."
            " **Hatched** bars were surveyed with a pole ≥ 150 cm"
            " (the 2.42 m bamboo pole in this survey). The **Δpair** text"
            " above a bar is the UTM-space distance between that GCP and"
            " its day-1/day-2 re-shoot counterpart — large values mean the"
            " RTK system didn't repeat on itself between occupations."
        )
        lines.append("")

    if pair_drift_m is not None:
        same_marker = {
            gid: info for gid, info in pair_drift_m.items()
            if isinstance(info, dict) and info.get("classification") == "same_marker_drift"
        }
        diff_markers = {
            gid: info for gid, info in pair_drift_m.items()
            if isinstance(info, dict) and info.get("classification") == "different_markers"
        }

        if same_marker:
            lines.append("### Day-1 ↔ day-2 re-occupation drift (same physical marker)")
            lines.append("")
            lines.append(
                "Verified same-marker pairs — the operator clicked both"
                " labels on the same feature in the video frame. UTM"
                " disagreement here is real RTK drift between"
                " occupations. For RTK work these pairs should agree to"
                " within a few centimetres; anything above ~10 cm is a"
                " survey-quality problem."
            )
            lines.append("")
            lines.append("| Pair | UTM drift (cm) | Click distance (px) |")
            lines.append("|---|---:|---:|")
            seen = set()
            for gid, info in sorted(
                same_marker.items(),
                key=lambda kv: -kv[1]["utm_distance_m"],
            ):
                base = gid[:-2] if gid.endswith(".2") else gid
                if base in seen:
                    continue
                seen.add(base)
                click_d = info.get("click_pixel_distance")
                click_s = f"{click_d:.1f}" if click_d is not None else "—"
                lines.append(
                    f"| {base} ↔ {base}.2 | {info['utm_distance_m']*100:.0f} | {click_s} |"
                )
            lines.append("")

        if diff_markers:
            lines.append("### Mislabelled pairs (different physical markers)")
            lines.append("")
            lines.append(
                "Pairs where the `.2` label was a **field mislabel**: the"
                " operator's clicks land on visibly different features"
                " in the video frame (≥ 15 px apart), so the two points"
                " are distinct physical markers — not the same point"
                " measured twice. Their UTM distance is real geometry,"
                " not RTK drift. Both points still have to stand on"
                " their individual survey merits in the fit."
            )
            lines.append("")
            lines.append("| Pair | Click distance (px) | UTM distance (cm) |")
            lines.append("|---|---:|---:|")
            seen = set()
            for gid, info in diff_markers.items():
                base = gid[:-2] if gid.endswith(".2") else gid
                if base in seen:
                    continue
                seen.add(base)
                click_d = info.get("click_pixel_distance")
                lines.append(
                    f"| {base} vs {base}.2 | {click_d:.0f} | "
                    f"{info['utm_distance_m']*100:.0f} |"
                )
            lines.append("")

    lines.append("## Per-GCP residual table (worst first)")
    lines.append("")
    inlier_set = set(inlier_ids)
    lines.append(
        format_residual_table(
            gcp_ids=gcp_ids,
            per_gcp_px=per_gcp_px,
            per_gcp_m=per_gcp_m,
            inlier_ids=inlier_set,
            detection_scores=detection_scores,
            detection_accepted=detection_accepted,
        )
    )
    lines.append("")
    lines.append("## Inputs & parameters")
    lines.append("")
    lines.append("```")
    for k, v in sorted(run_info.get("parameters", {}).items()):
        lines.append(f"{k} = {v}")
    lines.append("```")
    lines.append("")
    lines.append(
        "Artefacts from this run are in the run directory alongside this report."
        " See `audit.json` for the full decision log."
    )
    lines.append("")

    path.write_text("\n".join(lines))
