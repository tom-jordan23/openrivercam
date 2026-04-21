"""Plot generators for the auto-fit report."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # headless; no display needed for report images

import matplotlib.pyplot as plt


def plot_gcp_support(
    output_path: Path,
    clicked_ids: list[str],
    residuals_m: dict[str, float],
    subset_ids: set[str],
    pole_length_cm: dict[str, float] | None = None,
    pair_drift_m: dict[str, float] | None = None,
    a1_target_m: float = 0.05,
    noise_floor_m: float = 0.90,
    title: str | None = None,
) -> None:
    """Diagnostic bar chart of per-GCP residual under the best-subset pose.

    Designed to answer "why was this survey hard?" not just "what's the
    residual?". Adds:

    - **Hatching** on the bar for GCPs recorded with a long (>150 cm)
      pole (e.g. the 2.42 m bamboo pole in the Sukabumi survey). Pole
      flex / sway is a suspected source of height error.
    - **Pair drift annotation** above the bar for GCPs that were
      re-occupied as a `.2` re-shoot; shows the UTM-space disagreement
      between the day-1 point and its day-2 counterpart. Large drift
      means the RTK system was not repeating on itself.
    - **Dashed threshold lines** for the 5 cm registration target and
      the ~90 cm survey-noise floor, so a reader can see at a glance
      where each GCP falls between those two limits.

    Colour encodes subset membership: green if chosen for the best fit,
    orange if excluded. Y-axis is log scale because residuals span mm
    (best-subset members) to metres (worst outliers).
    """
    items = [
        (gid, residuals_m[gid])
        for gid in clicked_ids
        if gid in residuals_m
    ]
    items.sort(key=lambda t: t[1])
    if not items:
        return

    ids = [t[0] for t in items]
    vals_cm = [t[1] * 100.0 for t in items]
    colours = [
        ("#2ca02c" if gid in subset_ids else "#ff7f0e")
        for gid in ids
    ]
    hatches = []
    if pole_length_cm:
        for gid in ids:
            pole = pole_length_cm.get(gid)
            hatches.append("///" if (pole is not None and pole >= 150) else "")
    else:
        hatches = ["" for _ in ids]

    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(
        ids, vals_cm, color=colours, edgecolor="black", linewidth=0.5,
    )
    for b, h in zip(bars, hatches):
        if h:
            b.set_hatch(h)

    # value labels above each bar
    for b, v in zip(bars, vals_cm):
        ax.text(
            b.get_x() + b.get_width() / 2,
            v * 1.02 if v > 0 else 0.1,
            f"{v:.1f}" if v >= 1 else f"{v:.2f}",
            ha="center", va="bottom", fontsize=8,
        )

    # pair-drift annotations (small text above each bar's value label)
    if pair_drift_m:
        for b, gid, v in zip(bars, ids, vals_cm):
            drift = pair_drift_m.get(gid)
            if drift is not None:
                ax.text(
                    b.get_x() + b.get_width() / 2,
                    v * 1.9 if v > 0 else 0.3,
                    f"Δpair\n{drift*100:.0f} cm",
                    ha="center", va="bottom", fontsize=7,
                    color="#555", style="italic",
                )

    ax.axhline(
        a1_target_m * 100, linestyle="--", color="#1f77b4",
        alpha=0.7, linewidth=1.2, label="5 cm registration target",
    )
    ax.axhline(
        noise_floor_m * 100, linestyle="--", color="#d62728",
        alpha=0.7, linewidth=1.2, label="~90 cm survey-noise floor",
    )

    ax.set_yscale("log")
    ax.set_ylabel("Residual under best-subset pose (cm, log scale)")
    ax.set_xlabel("GCP (sorted by agreement with chosen geometry)")
    if title:
        ax.set_title(title, fontsize=11)
    ax.legend(
        loc="upper left",
        handles=ax.get_legend_handles_labels()[0]
        + [
            plt.Rectangle((0, 0), 1, 1, color="#2ca02c",
                          label="in best subset"),
            plt.Rectangle((0, 0), 1, 1, color="#ff7f0e",
                          label="excluded by subset search"),
            plt.Rectangle((0, 0), 1, 1, facecolor="white",
                          edgecolor="black", hatch="///",
                          label="surveyed on ≥150 cm pole"),
        ],
        fontsize=9,
    )

    plt.setp(ax.get_xticklabels(), rotation=40, ha="right")
    ax.grid(axis="y", which="both", alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=130)
    plt.close(fig)

