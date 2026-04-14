from __future__ import annotations

import argparse
import csv
import json
import random
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import cv2
import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from protocol_common import (
    PROJECT_ROOT,
    build_image_index,
    parse_method_specs,
    read_bgr,
    read_manifest,
    resize_bgr,
    resolve_project_path,
    safe_output_stem,
    select_common_stems,
    write_image,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Visual diagnostic sheets for underwater algae enhancement results."
    )
    parser.add_argument("--original-dir", default="data/inputImg/Original")
    parser.add_argument("--result-dir", default="results/png/Final")
    parser.add_argument("--method-name", default=None)
    parser.add_argument(
        "--method",
        action="append",
        default=None,
        help="Visualize method as name=directory. Repeat for multiple methods.",
    )
    parser.add_argument("--manifest", default=None)
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--limit", type=int, default=None, help="Limit before sampling.")
    parser.add_argument("--sample-count", type=int, default=12, help="0 or negative means all matched images.")
    parser.add_argument("--seed", type=int, default=20260412)
    parser.add_argument("--resize-to", nargs=2, type=int, default=(320, 320), metavar=("WIDTH", "HEIGHT"))
    parser.add_argument("--no-resize", action="store_true")
    parser.add_argument("--scatter-pixels", type=int, default=5000)
    parser.add_argument("--edge-low", type=int, default=None)
    parser.add_argument("--edge-high", type=int, default=None)
    return parser.parse_args()


def default_output_dir() -> Path:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return PROJECT_ROOT / "metrics" / "diagnostics" / stamp


def select_sample(stems: Sequence[str], sample_count: int, seed: int) -> List[str]:
    stems = list(stems)
    if sample_count <= 0 or sample_count >= len(stems):
        return stems
    rng = random.Random(seed)
    chosen = set(rng.sample(stems, sample_count))
    return [stem for stem in stems if stem in chosen]


def auto_canny(gray: np.ndarray, low: Optional[int], high: Optional[int]) -> np.ndarray:
    if low is None or high is None:
        median = float(np.median(gray))
        low_val = int(max(0, 0.66 * median)) if low is None else low
        high_val = int(min(255, 1.33 * median)) if high is None else high
    else:
        low_val, high_val = low, high
    if high_val <= low_val:
        high_val = min(255, low_val + 1)
    return cv2.Canny(gray, low_val, high_val)


def add_label(img_bgr: np.ndarray, label: str) -> np.ndarray:
    out = img_bgr.copy()
    cv2.rectangle(out, (0, 0), (out.shape[1], 28), (0, 0, 0), thickness=-1)
    cv2.putText(out, label, (8, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1, cv2.LINE_AA)
    return out


def make_comparison(original_bgr: np.ndarray, result_bgr: np.ndarray) -> np.ndarray:
    return cv2.hconcat([add_label(original_bgr, "Original"), add_label(result_bgr, "Enhanced")])


def make_edge_panel(original_edge: np.ndarray, result_edge: np.ndarray) -> np.ndarray:
    orig_bgr = cv2.cvtColor(original_edge, cv2.COLOR_GRAY2BGR)
    result_bgr = cv2.cvtColor(result_edge, cv2.COLOR_GRAY2BGR)
    return cv2.hconcat([add_label(orig_bgr, "Original edges"), add_label(result_bgr, "Enhanced edges")])


def sample_pixels(img_bgr: np.ndarray, max_pixels: int, seed: int) -> np.ndarray:
    pixels = img_bgr.reshape(-1, 3)
    if max_pixels <= 0 or pixels.shape[0] <= max_pixels:
        return pixels
    rng = np.random.default_rng(seed)
    idx = rng.choice(pixels.shape[0], size=max_pixels, replace=False)
    return pixels[idx]


def plot_lab_scatter(ax: plt.Axes, original_bgr: np.ndarray, result_bgr: np.ndarray, max_pixels: int, seed: int) -> None:
    original_lab = cv2.cvtColor(sample_pixels(original_bgr, max_pixels, seed).reshape(-1, 1, 3), cv2.COLOR_BGR2LAB).reshape(-1, 3)
    result_lab = cv2.cvtColor(sample_pixels(result_bgr, max_pixels, seed + 1).reshape(-1, 1, 3), cv2.COLOR_BGR2LAB).reshape(-1, 3)
    ax.scatter(original_lab[:, 1] - 128, original_lab[:, 2] - 128, s=2, alpha=0.20, c="#1f77b4", label="Original")
    ax.scatter(result_lab[:, 1] - 128, result_lab[:, 2] - 128, s=2, alpha=0.20, c="#d62728", label="Enhanced")
    ax.axhline(0, color="0.75", linewidth=0.8)
    ax.axvline(0, color="0.75", linewidth=0.8)
    ax.set_xlim(-128, 127)
    ax.set_ylim(-128, 127)
    ax.set_xlabel("Lab a*")
    ax.set_ylabel("Lab b*")
    ax.set_title("Lab a-b scatter")
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(True, linewidth=0.3, alpha=0.35)


def plot_rgb_scatter(ax: plt.Axes, img_bgr: np.ndarray, title: str, max_pixels: int, seed: int) -> None:
    pixels_bgr = sample_pixels(img_bgr, max_pixels, seed).astype(np.float32)
    pixels_rgb = pixels_bgr[:, ::-1]
    colors = np.clip(pixels_rgb / 255.0, 0, 1)
    ax.scatter(pixels_rgb[:, 0], pixels_rgb[:, 1], c=colors, s=2, alpha=0.35, linewidths=0)
    ax.set_xlim(0, 255)
    ax.set_ylim(0, 255)
    ax.set_xlabel("R")
    ax.set_ylabel("G")
    ax.set_title(title)
    ax.grid(True, linewidth=0.3, alpha=0.35)


def plot_luminance_hist(ax: plt.Axes, original_bgr: np.ndarray, result_bgr: np.ndarray) -> None:
    original_y = cv2.cvtColor(original_bgr, cv2.COLOR_BGR2YCrCb)[:, :, 0]
    result_y = cv2.cvtColor(result_bgr, cv2.COLOR_BGR2YCrCb)[:, :, 0]
    ax.hist(original_y.ravel(), bins=64, range=(0, 255), density=True, alpha=0.45, color="#1f77b4", label="Original")
    ax.hist(result_y.ravel(), bins=64, range=(0, 255), density=True, alpha=0.45, color="#d62728", label="Enhanced")
    ax.set_xlim(0, 255)
    ax.set_xlabel("Y luminance")
    ax.set_ylabel("Density")
    ax.set_title("Luminance histogram")
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(True, linewidth=0.3, alpha=0.35)


def save_sheet(
    path: Path,
    stem: str,
    method_name: str,
    comparison_bgr: np.ndarray,
    edge_panel_bgr: np.ndarray,
    original_bgr: np.ndarray,
    result_bgr: np.ndarray,
    scatter_pixels: int,
    seed: int,
) -> None:
    fig, axes = plt.subplots(2, 3, figsize=(15, 9), dpi=140)
    fig.suptitle(f"{method_name}: {stem}", fontsize=13)

    axes[0, 0].imshow(cv2.cvtColor(comparison_bgr, cv2.COLOR_BGR2RGB))
    axes[0, 0].set_title("Side-by-side comparison")
    axes[0, 0].axis("off")

    axes[0, 1].imshow(cv2.cvtColor(edge_panel_bgr, cv2.COLOR_BGR2RGB))
    axes[0, 1].set_title("Canny edge maps")
    axes[0, 1].axis("off")

    plot_luminance_hist(axes[0, 2], original_bgr, result_bgr)
    plot_lab_scatter(axes[1, 0], original_bgr, result_bgr, scatter_pixels, seed)
    plot_rgb_scatter(axes[1, 1], original_bgr, "RGB scatter: original", scatter_pixels, seed)
    plot_rgb_scatter(axes[1, 2], result_bgr, "RGB scatter: enhanced", scatter_pixels, seed + 1)

    fig.tight_layout(rect=(0, 0, 1, 0.96))
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path)
    plt.close(fig)


def write_index_csv(path: Path, rows: Sequence[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "method",
        "stem",
        "original_path",
        "result_path",
        "comparison_path",
        "edge_path",
        "sheet_path",
    ]
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def process_one(
    method_name: str,
    stem: str,
    original_path: Path,
    result_path: Path,
    output_dir: Path,
    resize_to: Optional[Tuple[int, int]],
    scatter_pixels: int,
    seed: int,
    edge_low: Optional[int],
    edge_high: Optional[int],
) -> Dict[str, str]:
    original_bgr = resize_bgr(read_bgr(original_path), resize_to)
    result_bgr = resize_bgr(read_bgr(result_path), resize_to)

    original_gray = cv2.cvtColor(original_bgr, cv2.COLOR_BGR2GRAY)
    result_gray = cv2.cvtColor(result_bgr, cv2.COLOR_BGR2GRAY)
    original_edge = auto_canny(original_gray, edge_low, edge_high)
    result_edge = auto_canny(result_gray, edge_low, edge_high)

    comparison = make_comparison(original_bgr, result_bgr)
    edge_panel = make_edge_panel(original_edge, result_edge)

    safe_name = f"{method_name}_{safe_output_stem(stem)}"
    comparison_path = output_dir / "comparisons" / f"{safe_name}_compare.png"
    edge_path = output_dir / "edges" / f"{safe_name}_edges.png"
    sheet_path = output_dir / "sheets" / f"{safe_name}_diagnostics.png"

    write_image(comparison_path, comparison)
    write_image(edge_path, edge_panel)
    save_sheet(
        sheet_path,
        stem,
        method_name,
        comparison,
        edge_panel,
        original_bgr,
        result_bgr,
        scatter_pixels,
        seed,
    )

    return {
        "method": method_name,
        "stem": stem,
        "original_path": str(original_path),
        "result_path": str(result_path),
        "comparison_path": str(comparison_path),
        "edge_path": str(edge_path),
        "sheet_path": str(sheet_path),
    }


def main() -> int:
    args = parse_args()
    original_dir = resolve_project_path(args.original_dir)
    output_dir = resolve_project_path(args.output_dir) if args.output_dir else default_output_dir()
    resize_to = None if args.no_resize else tuple(args.resize_to)

    methods = parse_method_specs(args.method, args.result_dir, args.method_name)
    original_index = build_image_index(original_dir, include_normalized_keys=False)
    method_indexes = {method.name: build_image_index(method.directory, include_normalized_keys=True) for method in methods}
    manifest_stems = read_manifest(args.manifest) if args.manifest else None
    planned_stems, failures = select_common_stems(
        original_index=original_index,
        method_indexes=method_indexes,
        manifest_stems=manifest_stems,
        limit=args.limit,
    )
    selected_stems = select_sample(planned_stems, args.sample_count, args.seed)

    rows: List[Dict[str, str]] = []
    for i, stem in enumerate(selected_stems, start=1):
        original_path = original_index.by_key[stem]
        for method in methods:
            result_path = method_indexes[method.name].by_key[stem]
            try:
                row = process_one(
                    method_name=method.name,
                    stem=stem,
                    original_path=original_path,
                    result_path=result_path,
                    output_dir=output_dir,
                    resize_to=resize_to,
                    scatter_pixels=args.scatter_pixels,
                    seed=args.seed + i,
                    edge_low=args.edge_low,
                    edge_high=args.edge_high,
                )
                rows.append(row)
                print(f"[OK] {i}/{len(selected_stems)} {method.name}: {stem}")
            except Exception as exc:
                failures.append(
                    {
                        "phase": "diagnostics",
                        "method": method.name,
                        "stem": stem,
                        "error": str(exc),
                    }
                )
                print(f"[FAIL] {i}/{len(selected_stems)} {method.name}: {stem} -> {exc}")

    write_index_csv(output_dir / "diagnostics_index.csv", rows)
    summary = {
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "project_root": str(PROJECT_ROOT),
        "original_dir": str(original_dir),
        "methods": {method.name: str(method.directory) for method in methods},
        "planned_stem_count": len(planned_stems),
        "selected_stem_count": len(selected_stems),
        "generated_count": len(rows),
        "resize_to": list(resize_to) if resize_to else None,
        "scatter_pixels": args.scatter_pixels,
        "seed": args.seed,
        "output_dir": str(output_dir),
        "failures": failures,
    }
    (output_dir / "diagnostics_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"[DONE] Generated {len(rows)} diagnostic entries.")
    print(f"[DONE] Output directory: {output_dir}")
    return 0 if rows else 1


if __name__ == "__main__":
    raise SystemExit(main())
