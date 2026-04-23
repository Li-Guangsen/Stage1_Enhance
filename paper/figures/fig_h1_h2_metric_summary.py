"""
Figure: Internal evidence summary for H1 and H2.

This script follows the repo's currently accepted evidence sources:
- H1 white-balance summary.json
- H2 selection.json

Outputs:
- fig_h1_h2_metric_summary.png
- fig_h1_h2_metric_summary.svg
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


ROOT = Path(__file__).resolve().parents[2]
H1_SUMMARY = ROOT / "experiments" / "h1-graypixel-bph-ablation" / "outputs" / "full506" / "eval" / "summary.json"
H2_SELECTION = ROOT / "experiments" / "h2-full506-direct" / "outputs" / "full506" / "eval" / "selection.json"

OUTPUT_PNG = Path(__file__).with_suffix(".png")
OUTPUT_SVG = Path(__file__).with_suffix(".svg")


CELL_COLORS = ["#4E79A7", "#F28E2B", "#E15759", "#76B7B2", "#59A14F", "#EDC948"]
COLORBLIND_SAFE = ["#0077BB", "#33BBEE", "#009988", "#EE7733", "#CC3311", "#EE3377"]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def setup_style() -> None:
    sns.set_theme(style="whitegrid")
    plt.rcParams.update(
        {
            "font.size": 10,
            "axes.titlesize": 12,
            "axes.labelsize": 10,
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
            "legend.fontsize": 9,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "savefig.dpi": 450,
            "savefig.bbox": "tight",
        }
    )


def h1_data(summary: dict) -> tuple[list[str], np.ndarray, np.ndarray]:
    methods = ["r2_02_G_P", "r2_05_G_P_A_B", "r2_08_G_P_A2_B"]
    baseline = summary["methods"]["r2_00_baseline"]["metrics"]
    base_ms = float(baseline["MS_SSIM"]["mean"])
    base_psnr = float(baseline["PSNR"]["mean"])

    delta_ms = []
    delta_psnr = []
    for method in methods:
        metrics = summary["methods"][method]["metrics"]
        delta_ms.append(float(metrics["MS_SSIM"]["mean"]) - base_ms)
        delta_psnr.append(float(metrics["PSNR"]["mean"]) - base_psnr)
    return methods, np.array(delta_ms), np.array(delta_psnr)


def h2_heatmap_data(selection: dict) -> tuple[list[str], list[str], np.ndarray]:
    stages = ["rghs", "clahe", "fusion"]
    stage_labels = ["RGHS", "CLAHE", "Fusion"]
    metric_labels = ["MS-SSIM", "PSNR (dB)", "UCIQE", "UIQM"]
    matrix = []
    for stage in stages:
        official = selection[stage]["winner"]["official"]
        matrix.append(
            [
                float(official["delta_ms_ssim"]),
                float(official["delta_psnr"]),
                float(official["delta_uciqe"]),
                float(official["delta_uiqm"]),
            ]
        )
    return stage_labels, metric_labels, np.array(matrix, dtype=float)


def annotate_bar(ax: plt.Axes, values: np.ndarray, fmt: str) -> None:
    for idx, value in enumerate(values):
        offset = 0.02 * max(1.0, np.max(np.abs(values)))
        y = value + offset if value >= 0 else value - offset
        va = "bottom" if value >= 0 else "top"
        ax.text(idx, y, format(value, fmt), ha="center", va=va, fontsize=8)


def main() -> None:
    setup_style()

    h1_summary = load_json(H1_SUMMARY)
    h2_selection = load_json(H2_SELECTION)

    methods, delta_ms, delta_psnr = h1_data(h1_summary)
    stage_labels, metric_labels, heatmap = h2_heatmap_data(h2_selection)

    fig = plt.figure(figsize=(11.5, 4.8))
    grid = fig.add_gridspec(1, 3, width_ratios=[1.0, 1.0, 1.35], wspace=0.35)

    ax1 = fig.add_subplot(grid[0, 0])
    bars1 = ax1.bar(methods, delta_ms, color=CELL_COLORS[:3], edgecolor="white", linewidth=0.8)
    ax1.axhline(0.0, color="#666666", linewidth=0.9)
    ax1.set_title("(a) H1 delta MS-SSIM vs baseline")
    ax1.set_ylabel("Delta MS-SSIM")
    ax1.tick_params(axis="x", rotation=20)
    annotate_bar(ax1, delta_ms, ".4f")

    ax2 = fig.add_subplot(grid[0, 1])
    bars2 = ax2.bar(methods, delta_psnr, color=COLORBLIND_SAFE[:3], edgecolor="white", linewidth=0.8)
    ax2.axhline(0.0, color="#666666", linewidth=0.9)
    ax2.set_title("(b) H1 delta PSNR vs baseline")
    ax2.set_ylabel("Delta PSNR (dB)")
    ax2.tick_params(axis="x", rotation=20)
    annotate_bar(ax2, delta_psnr, ".3f")

    ax3 = fig.add_subplot(grid[0, 2])
    sns.heatmap(
        heatmap,
        ax=ax3,
        cmap=sns.diverging_palette(220, 20, as_cmap=True),
        center=0.0,
        annot=True,
        fmt=".3f",
        cbar_kws={"shrink": 0.85, "label": "Delta vs locked mainline"},
        linewidths=0.8,
        linecolor="white",
        xticklabels=metric_labels,
        yticklabels=stage_labels,
    )
    ax3.set_title("(c) H2 accepted winner deltas")
    ax3.tick_params(axis="x", rotation=20)
    ax3.tick_params(axis="y", rotation=0)

    fig.suptitle("Internal Evidence Summary for the Current Underwater Enhancement Mainline", y=1.02, fontsize=13)

    fig.savefig(OUTPUT_PNG, dpi=450)
    fig.savefig(OUTPUT_SVG)
    plt.close(fig)


if __name__ == "__main__":
    main()
