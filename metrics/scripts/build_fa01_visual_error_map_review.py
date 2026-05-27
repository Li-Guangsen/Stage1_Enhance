from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

import cv2
import numpy as np

THIS_DIR = Path(__file__).resolve().parent
METRICS_DIR = THIS_DIR.parent
PROJECT_ROOT = METRICS_DIR.parent


DEFAULT_STEMS = [
    "weixiaoyuanjia.26",
    "xuehong.9",
    "xuehong.13",
    "xuehong.11",
    "donghaiyuanjia.26",
    "weixiaoyuanjia.21",
    "tama.14",
    "tama.11",
    "tama.9",
    "jianci.4",
    "donghaiyuanjia.18",
]

STAGE_VARIANTS = [
    ("raw_anchor", "Raw"),
    ("gt", "GT"),
    ("legacy_stage1_final", "Legacy Final"),
    ("P27_raw_detail_lowfreq_chroma", "P27"),
    ("D01_structure_flow", "D01"),
    ("FF01_full_flow_v8", "FF01"),
    ("FF02_detector_compatible", "FF02"),
]

DETECTOR_VARIANTS = [
    ("raw_anchor", "Raw"),
    ("legacy_stage1_final", "Legacy"),
    ("P27_raw_detail_lowfreq_chroma", "P27"),
    ("D01_structure_flow", "D01"),
    ("FF01_full_flow_v8", "FF01"),
    ("FF02_detector_compatible", "FF02"),
]

DETECTORS = [
    ("msfi_50k", "MSFI"),
    ("diffusionedge_baseline_50k", "DE"),
]


@dataclass
class Paths:
    raw_path: str = ""
    gt_path: str = ""
    selection_reasons: str = ""
    stage1_final_by_variant: Dict[str, str] = None
    error_map_by_detector_variant: Dict[Tuple[str, str], str] = None

    def __post_init__(self) -> None:
        if self.stage1_final_by_variant is None:
            self.stage1_final_by_variant = {}
        if self.error_map_by_detector_variant is None:
            self.error_map_by_detector_variant = {}


def read_csv_rows(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def as_path(path_text: str) -> Optional[Path]:
    if not path_text:
        return None
    path = Path(path_text)
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    return path


def existing_path(path_text: str) -> Optional[Path]:
    path = as_path(path_text)
    if path is None or not path.is_file():
        return None
    return path


def load_paths(stage_csv: Path, detector_csv: Path) -> Dict[str, Paths]:
    records: Dict[str, Paths] = {}

    for row in read_csv_rows(stage_csv):
        stem = row["stem"]
        rec = records.setdefault(stem, Paths())
        rec.selection_reasons = row.get("selection_reasons", rec.selection_reasons)
        rec.raw_path = row.get("raw_path", rec.raw_path)
        rec.gt_path = row.get("gt_path", rec.gt_path)
        variant = row.get("variant", "")
        final_path = row.get("stage1_final_path", "")
        if variant and row.get("stage1_final_exists") == "True":
            rec.stage1_final_by_variant[variant] = final_path

    for row in read_csv_rows(detector_csv):
        stem = row["stem"]
        rec = records.setdefault(stem, Paths())
        rec.selection_reasons = row.get("selection_reasons", rec.selection_reasons)
        variant = row.get("variant", "")
        detector = row.get("detector", "")
        error_path = row.get("error_map_path", "")
        if variant and detector and row.get("error_map_exists") == "True":
            rec.error_map_by_detector_variant[(detector, variant)] = error_path

    return records


def load_metrics(merged_csv: Path) -> Dict[Tuple[str, str, str], Dict[str, float]]:
    metrics: Dict[Tuple[str, str, str], Dict[str, float]] = {}
    for row in read_csv_rows(merged_csv):
        key = (row["stem"], row["detector"], row["variant"])
        numeric: Dict[str, float] = {}
        for k, value in row.items():
            if k in {"stem", "detector", "variant"}:
                continue
            try:
                numeric[k] = float(value)
            except (TypeError, ValueError):
                pass
        metrics[key] = numeric
    return metrics


def read_bgr(path: Optional[Path], size: Tuple[int, int], fallback_label: str) -> np.ndarray:
    if path is None:
        return missing_tile(size, fallback_label)
    img = cv2.imdecode(np.fromfile(str(path), dtype=np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        return missing_tile(size, fallback_label)
    return resize_to_tile(img, size)


def resize_to_tile(img: np.ndarray, size: Tuple[int, int]) -> np.ndarray:
    target_w, target_h = size
    h, w = img.shape[:2]
    if h <= 0 or w <= 0:
        return missing_tile(size, "invalid")
    scale = min(target_w / w, target_h / h)
    new_w = max(1, int(round(w * scale)))
    new_h = max(1, int(round(h * scale)))
    resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
    canvas = np.full((target_h, target_w, 3), 245, dtype=np.uint8)
    x0 = (target_w - new_w) // 2
    y0 = (target_h - new_h) // 2
    canvas[y0 : y0 + new_h, x0 : x0 + new_w] = resized
    return canvas


def missing_tile(size: Tuple[int, int], label: str) -> np.ndarray:
    w, h = size
    tile = np.full((h, w, 3), 230, dtype=np.uint8)
    cv2.line(tile, (0, 0), (w - 1, h - 1), (180, 180, 180), 2)
    cv2.line(tile, (w - 1, 0), (0, h - 1), (180, 180, 180), 2)
    add_label(tile, f"missing: {label}", fill=(80, 80, 80))
    return tile


def add_label(img: np.ndarray, label: str, fill: Tuple[int, int, int] = (0, 0, 0)) -> np.ndarray:
    out = img
    cv2.rectangle(out, (0, 0), (out.shape[1], 26), fill, thickness=-1)
    cv2.putText(
        out,
        label[:40],
        (6, 18),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.48,
        (255, 255, 255),
        1,
        cv2.LINE_AA,
    )
    return out


def metric_suffix(metrics: Dict[Tuple[str, str, str], Dict[str, float]], stem: str, detector: str, variant: str) -> str:
    values = metrics.get((stem, detector, variant))
    if not values:
        return ""
    d_f1 = values.get("delta_boundary_f1_tol")
    if d_f1 is None:
        return ""
    return f"dF1 {d_f1:+.2f}"


def make_panel(
    stem: str,
    rec: Paths,
    metrics: Dict[Tuple[str, str, str], Dict[str, float]],
    output_path: Path,
    tile_size: Tuple[int, int],
) -> Dict[str, str]:
    rows: List[np.ndarray] = []

    stage_tiles = []
    for variant, label in STAGE_VARIANTS:
        if variant == "raw_anchor":
            path = existing_path(rec.raw_path)
        elif variant == "gt":
            path = existing_path(rec.gt_path)
        else:
            path = existing_path(rec.stage1_final_by_variant.get(variant, ""))
        tile = read_bgr(path, tile_size, label)
        stage_tiles.append(add_label(tile, label))
    rows.append(np.hstack(stage_tiles))

    for detector, detector_label in DETECTORS:
        det_tiles = []
        for variant, short_label in DETECTOR_VARIANTS:
            path = existing_path(rec.error_map_by_detector_variant.get((detector, variant), ""))
            tile = read_bgr(path, tile_size, f"{detector}:{variant}")
            suffix = metric_suffix(metrics, stem, detector, variant)
            label = f"{detector_label}: {short_label}" if not suffix else f"{detector_label}: {short_label} {suffix}"
            det_tiles.append(add_label(tile, label))
        if len(det_tiles) == len(stage_tiles) - 1:
            det_tiles.insert(1, add_label(missing_tile(tile_size, "GT not detector output"), "GT n/a"))
        rows.append(np.hstack(det_tiles))

    header_h = 38
    width = rows[0].shape[1]
    header = np.full((header_h, width, 3), 35, dtype=np.uint8)
    cv2.putText(header, stem, (8, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.72, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(
        header,
        "Stage1 outputs + fixed-detector error maps",
        (max(220, width // 3), 25),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.56,
        (230, 230, 230),
        1,
        cv2.LINE_AA,
    )
    panel = np.vstack([header, *rows])
    output_path.parent.mkdir(parents=True, exist_ok=True)
    ok, encoded = cv2.imencode(".jpg", panel, [int(cv2.IMWRITE_JPEG_QUALITY), 88])
    if not ok:
        raise RuntimeError(f"Failed to encode panel: {output_path}")
    encoded.tofile(str(output_path))

    return {
        "stem": stem,
        "selection_reasons": rec.selection_reasons,
        "panel_path": str(output_path.relative_to(PROJECT_ROOT)).replace("\\", "/"),
    }


def summarize_patterns(
    stem: str,
    rec: Paths,
    metrics: Dict[Tuple[str, str, str], Dict[str, float]],
    panel_rel: str,
) -> Dict[str, str]:
    values = []
    for (row_stem, detector, variant), m in metrics.items():
        if row_stem != stem:
            continue
        values.append((detector, variant, m))

    worst_f1 = min((m.get("delta_boundary_f1_tol", 0.0) for _, _, m in values), default=0.0)
    max_false = max((m.get("delta_false_edge_ratio_tol", 0.0) for _, _, m in values), default=0.0)
    max_end = max((m.get("delta_endpoints_per_1k_skel_px", 0.0) for _, _, m in values), default=0.0)
    max_bgr = max((m.get("mean_abs_bgr_delta", 0.0) for _, _, m in values), default=0.0)
    max_chroma = max((m.get("mean_abs_chroma_delta", 0.0) for _, _, m in values), default=0.0)
    max_grad = max((m.get("grad_mean_ratio", 1.0) for _, _, m in values), default=1.0)
    min_grad = min((m.get("grad_mean_ratio", 1.0) for _, _, m in values), default=1.0)

    tags: List[str] = []
    if worst_f1 <= -0.05:
        tags.append("boundary_f1_loss")
    if max_false >= 0.07:
        tags.append("false_edge_increase")
    if max_end >= 3.0:
        tags.append("endpoint_fragmentation")
    if max_grad >= 1.35 or min_grad <= 0.85:
        tags.append("luma_detail_topology_drift")
    if max_bgr >= 12.0 or max_chroma >= 7.0:
        tags.append("large_color_chroma_shift")
    if not tags:
        tags.append("mixed_or_localized_detector_sensitivity")

    return {
        "stem": stem,
        "selection_reasons": rec.selection_reasons,
        "failure_pattern_tags": ";".join(tags),
        "worst_delta_f1": f"{worst_f1:.6f}",
        "max_delta_false_edge": f"{max_false:.6f}",
        "max_delta_endpoints": f"{max_end:.6f}",
        "max_mean_abs_bgr_delta": f"{max_bgr:.6f}",
        "max_mean_abs_chroma_delta": f"{max_chroma:.6f}",
        "min_grad_mean_ratio": f"{min_grad:.6f}",
        "max_grad_mean_ratio": f"{max_grad:.6f}",
        "panel_path": panel_rel,
    }


def write_csv(path: Path, rows: Sequence[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def markdown_link(rel_path: str) -> str:
    return rel_path.replace("\\", "/")


def write_markdown(path: Path, pattern_rows: Sequence[Dict[str, str]], panel_rows: Sequence[Dict[str, str]]) -> None:
    lines: List[str] = []
    lines.append("# FA01 high-risk visual/error-map review\n")
    lines.append("日期：2026-05-27\n")
    lines.append("## 1. 目的\n")
    lines.append(
        "本审查只整理既有 FA01 证据：raw、GT、legacy Stage1 Final、P27、D01、FF01、FF02，以及 fixed MSFI/DiffusionEdge 的 error-map。"
        "它不是新候选、不是新实验，也不替代 168 fixed-detector gate。\n"
    )
    lines.append("## 2. 结论\n")
    lines.append(
        "- high-risk 样本的共同问题不是单一颜色偏移，而是 detector error-map 中的边界损失、背景 false-edge、骨架端点碎片化和 luma/detail topology drift 的组合。\n"
    )
    lines.append(
        "- FF01/FF02 的完整增强骨架在视觉/色度上比 P27/D01 更明显，但现有 fixed raw-trained detector 对这种输入分布并不稳定；继续 FF03 式同族小修没有足够证据价值。\n"
    )
    lines.append(
        "- 下一步应把 Stage1 输出拆成 sidecar evidence maps 或进入独立 MyEdge/MSFI adaptation protocol，而不是继续把增强图直接替换 raw 作为 fixed-detector 输入。\n"
    )
    lines.append("## 3. 审查样本与模式标签\n")
    lines.append("| stem | pattern tags | worst dF1 | max dFalse | max dEndpoints | max BGR | max chroma | panel |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---|")
    for row in pattern_rows:
        lines.append(
            f"| {row['stem']} | {row['failure_pattern_tags']} | {row['worst_delta_f1']} | "
            f"{row['max_delta_false_edge']} | {row['max_delta_endpoints']} | "
            f"{row['max_mean_abs_bgr_delta']} | {row['max_mean_abs_chroma_delta']} | "
            f"[panel]({markdown_link(row['panel_path'])}) |"
        )
    lines.append("\n## 4. 文件索引\n")
    lines.append("- `fa01_visual_error_map_panels.csv`：每个 panel 的相对路径和选样原因。")
    lines.append("- `fa01_visual_error_map_pattern_tags.csv`：基于 per-image proxy 的失败模式标签。")
    lines.append("- `fa01_visual_error_map_review_index.json`：生成参数、输入文件和输出统计。")
    lines.append("\n## 5. 后续约束\n")
    lines.append(
        "该审查支持 FA01 的决策：先停止 same-family full-flow patching，优先定义 Stage1 sidecar maps 和 no-training export smoke；"
        "若要证明 downstream 正收益，必须另立适配协议或新方法族，并保持 fixed-detector 结果与 adaptation 结果分账。"
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build FA01 high-risk visual/error-map review panels.")
    parser.add_argument(
        "--stage-paths-csv",
        default="docs/fa01_high_risk_sample_index_20260527/fa01_high_risk_stage1_paths.csv",
    )
    parser.add_argument(
        "--detector-paths-csv",
        default="docs/fa01_high_risk_sample_index_20260527/fa01_high_risk_detector_paths.csv",
    )
    parser.add_argument(
        "--merged-metrics-csv",
        default="docs/fa01_per_image_correlation_audit_20260527/fa01_per_image_enhancement_structure_merged.csv",
    )
    parser.add_argument("--output-dir", default="docs/fa01_visual_error_map_review_20260527")
    parser.add_argument("--stem", action="append", default=None, help="Stem to include. Repeatable.")
    parser.add_argument("--tile-width", type=int, default=220)
    parser.add_argument("--tile-height", type=int, default=170)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    stage_csv = (PROJECT_ROOT / args.stage_paths_csv).resolve()
    detector_csv = (PROJECT_ROOT / args.detector_paths_csv).resolve()
    merged_csv = (PROJECT_ROOT / args.merged_metrics_csv).resolve()
    output_dir = (PROJECT_ROOT / args.output_dir).resolve()

    records = load_paths(stage_csv, detector_csv)
    metrics = load_metrics(merged_csv)
    stems = args.stem or DEFAULT_STEMS

    panel_rows: List[Dict[str, str]] = []
    pattern_rows: List[Dict[str, str]] = []
    missing_stems: List[str] = []
    for stem in stems:
        rec = records.get(stem)
        if rec is None:
            missing_stems.append(stem)
            continue
        panel_path = output_dir / "panels" / f"{stem}_fa01_visual_error_map_panel.jpg"
        panel_row = make_panel(stem, rec, metrics, panel_path, (args.tile_width, args.tile_height))
        panel_rows.append(panel_row)
        pattern_rows.append(summarize_patterns(stem, rec, metrics, panel_row["panel_path"]))

    write_csv(output_dir / "fa01_visual_error_map_panels.csv", panel_rows)
    write_csv(output_dir / "fa01_visual_error_map_pattern_tags.csv", pattern_rows)
    index = {
        "name": "fa01_visual_error_map_review_20260527",
        "date": "2026-05-27",
        "stage_paths_csv": str(stage_csv.relative_to(PROJECT_ROOT)).replace("\\", "/"),
        "detector_paths_csv": str(detector_csv.relative_to(PROJECT_ROOT)).replace("\\", "/"),
        "merged_metrics_csv": str(merged_csv.relative_to(PROJECT_ROOT)).replace("\\", "/"),
        "output_dir": str(output_dir.relative_to(PROJECT_ROOT)).replace("\\", "/"),
        "requested_stems": stems,
        "generated_panel_count": len(panel_rows),
        "missing_stems": missing_stems,
        "tile_size": [args.tile_width, args.tile_height],
        "scope": "diagnostic review only; no new candidate, no detector run, no fixed-detector gate replacement",
    }
    (output_dir / "fa01_visual_error_map_review_index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    write_markdown(PROJECT_ROOT / "docs/fa01_visual_error_map_review_20260527_cn.md", pattern_rows, panel_rows)
    print(json.dumps(index, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
