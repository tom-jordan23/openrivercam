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
