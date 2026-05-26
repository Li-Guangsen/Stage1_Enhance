from __future__ import annotations

import argparse
import csv
import json
import math
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

import cv2
import numpy as np
from skimage.measure import label as cc_label
from skimage.morphology import skeletonize

THIS_DIR = Path(__file__).resolve().parent
METRICS_DIR = THIS_DIR.parent
PROJECT_ROOT = METRICS_DIR.parent
if str(METRICS_DIR) not in sys.path:
    sys.path.insert(0, str(METRICS_DIR))

from protocol_common import (  # noqa: E402
    ImageIndex,
    MethodSpec,
    build_image_index,
    read_manifest,
    resolve_project_path,
    safe_output_stem,
    select_common_stems,
    write_lines,
)


METRIC_NAMES = [
    "luma_mean",
    "luma_std",
    "sobel_mean",
    "sobel_p90",
    "sobel_p95",
    "edge_threshold",
    "edge_pixels",
    "edge_density",
    "component_count",
    "component_count_per_1k_edge",
    "mean_component_area",
    "median_component_area",
    "largest_component_area_ratio",
    "small_component_ratio",
    "skeleton_pixels",
    "skeleton_density",
    "skeleton_endpoints",
    "skeleton_endpoint_density",
    "skeleton_branchpoints",
    "skeleton_branchpoint_density",
]

DELTA_NAMES = [
    "delta_edge_density_vs_original",
    "delta_sobel_mean_vs_original",
    "delta_skeleton_density_vs_original",
    "delta_skeleton_endpoint_density_vs_original",
    "ratio_edge_density_vs_original",
    "ratio_sobel_mean_vs_original",
]


@dataclass(frozen=True)
class MethodInfo:
    name: str
    directory: Path
    method_class: str
    note: str


@dataclass
class SuiteResult:
    suite: str
    output_dir: Path
    rows: List[Dict[str, object]]
    failures: List[Dict[str, str]]
    complete_stems: List[str]
    methods: List[MethodInfo]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run no-GT edge-structure proxy validation for the Stage1 enhancement package. "
            "This script does not replace GT-based MyEdge evaluation."
        )
    )
    parser.add_argument(
        "--registry",
        default=str(PROJECT_ROOT / "metrics" / "configs" / "official_method_registry.json"),
    )
    parser.add_argument(
        "--output-root",
        default=str(PROJECT_ROOT / "metrics" / "outputs" / "downstream_edge_validation" / "official_full502_mainline"),
    )
    parser.add_argument("--suite", choices=["stage", "compare", "both"], default="both")
    parser.add_argument("--stage-manifest", default=str(PROJECT_ROOT / "metrics" / "manifests" / "full502_clean_v1.txt"))
    parser.add_argument(
        "--compare-manifest",
        default=str(PROJECT_ROOT / "metrics" / "manifests" / "compare9_complete496_v1.txt"),
    )
    parser.add_argument("--resize-to", nargs=2, type=int, default=(320, 320), metavar=("WIDTH", "HEIGHT"))
    parser.add_argument("--no-resize", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--panel-count", type=int, default=4)
    parser.add_argument("--no-panels", action="store_true")
    parser.add_argument("--quiet", action="store_true")
    return parser.parse_args()


def load_registry(path: str | Path) -> Dict[str, object]:
    registry_path = resolve_project_path(path)
    return json.loads(registry_path.read_text(encoding="utf-8"))


def read_bgr(path: Path) -> np.ndarray:
    data = np.fromfile(str(path), dtype=np.uint8)
    image = cv2.imdecode(data, cv2.IMREAD_COLOR)
    if image is None:
        raise RuntimeError(f"cv2.imdecode failed: {path}")
    return image


def write_bgr(path: Path, image: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    ok, encoded = cv2.imencode(path.suffix, image)
    if not ok:
        raise RuntimeError(f"cv2.imencode failed: {path}")
    encoded.tofile(str(path))


def resize_bgr(image: np.ndarray, resize_to: Optional[Tuple[int, int]]) -> np.ndarray:
    if resize_to is None:
        return image
    width, height = resize_to
    h, w = image.shape[:2]
    if (w, h) == (width, height):
        return image
    return cv2.resize(image, (width, height), interpolation=cv2.INTER_CUBIC)


def finite_float(value: object) -> float:
    try:
        value_f = float(value)
    except Exception:
        return float("nan")
    return value_f if math.isfinite(value_f) else float("nan")


def csv_value(value: object) -> str:
    value_f = finite_float(value)
    if math.isfinite(value_f):
        return f"{value_f:.10g}"
    return "nan"


def otsu_edge_mask(gray_u8: np.ndarray) -> Tuple[np.ndarray, np.ndarray, float]:
    blurred = cv2.GaussianBlur(gray_u8, (3, 3), 0)
    gray_f = blurred.astype(np.float32) / 255.0
    gx = cv2.Sobel(gray_f, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(gray_f, cv2.CV_32F, 0, 1, ksize=3)
    mag = np.sqrt(gx * gx + gy * gy)
    max_mag = float(np.max(mag))
    if max_mag <= 1e-12:
        return mag, np.zeros_like(gray_u8, dtype=bool), 0.0
    mag_u8 = np.clip(mag / max_mag * 255.0, 0, 255).astype(np.uint8)
    threshold_u8, edge_u8 = cv2.threshold(mag_u8, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    threshold = float(threshold_u8) / 255.0 * max_mag
    edge_mask = edge_u8 > 0
    return mag, edge_mask, threshold


def skeleton_degrees(skeleton: np.ndarray) -> np.ndarray:
    sk = skeleton.astype(np.uint8)
    padded = np.pad(sk, ((1, 1), (1, 1)), mode="constant")
    neighbors = (
        padded[:-2, :-2]
        + padded[:-2, 1:-1]
        + padded[:-2, 2:]
        + padded[1:-1, :-2]
        + padded[1:-1, 2:]
        + padded[2:, :-2]
        + padded[2:, 1:-1]
        + padded[2:, 2:]
    )
    return neighbors


def compute_edge_metrics(path: Path, resize_to: Optional[Tuple[int, int]]) -> Dict[str, float]:
    image = resize_bgr(read_bgr(path), resize_to)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    mag, edge_mask, threshold = otsu_edge_mask(gray)
    h, w = gray.shape
    total_pixels = float(h * w)
    edge_pixels = int(np.count_nonzero(edge_mask))
    edge_density = edge_pixels / total_pixels if total_pixels else 0.0

    labels = cc_label(edge_mask, connectivity=2)
    component_areas = np.bincount(labels.ravel())[1:]
    component_count = int(component_areas.size)
    if component_count:
        mean_component_area = float(np.mean(component_areas))
        median_component_area = float(np.median(component_areas))
        largest_component_area_ratio = float(np.max(component_areas) / max(edge_pixels, 1))
        small_component_ratio = float(np.count_nonzero(component_areas <= 8) / component_count)
    else:
        mean_component_area = 0.0
        median_component_area = 0.0
        largest_component_area_ratio = 0.0
        small_component_ratio = 0.0

    skeleton = skeletonize(edge_mask)
    skeleton_pixels = int(np.count_nonzero(skeleton))
    degrees = skeleton_degrees(skeleton)
    skeleton_endpoints = int(np.count_nonzero(skeleton & (degrees == 1)))
    skeleton_branchpoints = int(np.count_nonzero(skeleton & (degrees >= 3)))

    return {
        "luma_mean": float(np.mean(gray)),
        "luma_std": float(np.std(gray)),
        "sobel_mean": float(np.mean(mag)),
        "sobel_p90": float(np.percentile(mag, 90)),
        "sobel_p95": float(np.percentile(mag, 95)),
        "edge_threshold": float(threshold),
        "edge_pixels": float(edge_pixels),
        "edge_density": float(edge_density),
        "component_count": float(component_count),
        "component_count_per_1k_edge": float(component_count / max(edge_pixels, 1) * 1000.0),
        "mean_component_area": mean_component_area,
        "median_component_area": median_component_area,
        "largest_component_area_ratio": largest_component_area_ratio,
        "small_component_ratio": small_component_ratio,
        "skeleton_pixels": float(skeleton_pixels),
        "skeleton_density": float(skeleton_pixels / total_pixels if total_pixels else 0.0),
        "skeleton_endpoints": float(skeleton_endpoints),
        "skeleton_endpoint_density": float(skeleton_endpoints / max(skeleton_pixels, 1)),
        "skeleton_branchpoints": float(skeleton_branchpoints),
        "skeleton_branchpoint_density": float(skeleton_branchpoints / max(skeleton_pixels, 1)),
    }


def build_method_infos(registry: Dict[str, object], suite: str) -> Tuple[Path, List[MethodInfo]]:
    original_dir = resolve_project_path(str(registry["original_dir"]))
    methods = [MethodInfo(name="Original", directory=original_dir, method_class="input", note="原始输入")]
    key = "stage_methods" if suite == "stage" else "compare_methods"
    for method in registry[key]:
        methods.append(
            MethodInfo(
                name=str(method["name"]),
                directory=resolve_project_path(str(method["directory"])),
                method_class=str(method.get("method_class", "")),
                note=str(method.get("note", "")),
            )
        )
    return original_dir, methods


def method_indexes(methods: Sequence[MethodInfo]) -> Dict[str, ImageIndex]:
    indexes: Dict[str, ImageIndex] = {}
    for method in methods:
        include_normalized = method.name != "Original"
        indexes[method.name] = build_image_index(method.directory, include_normalized_keys=include_normalized)
    return indexes


def add_deltas(rows: List[Dict[str, object]]) -> None:
    originals: Dict[str, Dict[str, object]] = {
        str(row["stem"]): row for row in rows if row["method"] == "Original"
    }
    for row in rows:
        original = originals.get(str(row["stem"]))
        if original is None:
            continue
        for metric in ("edge_density", "sobel_mean", "skeleton_density", "skeleton_endpoint_density"):
            row[f"delta_{metric}_vs_original"] = finite_float(row[metric]) - finite_float(original[metric])
        row["ratio_edge_density_vs_original"] = finite_float(row["edge_density"]) / max(
            finite_float(original["edge_density"]), 1e-12
        )
        row["ratio_sobel_mean_vs_original"] = finite_float(row["sobel_mean"]) / max(
            finite_float(original["sobel_mean"]), 1e-12
        )


def write_csv(path: Path, rows: Sequence[Dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "suite",
        "method",
        "method_class",
        "stem",
        "image_path",
        *METRIC_NAMES,
        *DELTA_NAMES,
    ]
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            out = dict(row)
            for metric in [*METRIC_NAMES, *DELTA_NAMES]:
                out[metric] = csv_value(out.get(metric, float("nan")))
            writer.writerow({name: out.get(name, "") for name in fieldnames})


def write_failures_csv(path: Path, rows: Sequence[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["suite", "phase", "method", "stem", "path", "error"]
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({name: row.get(name, "") for name in fieldnames})


def summarize(rows: Sequence[Dict[str, object]], methods: Sequence[MethodInfo]) -> List[Dict[str, object]]:
    summary_rows: List[Dict[str, object]] = []
    for method in methods:
        method_rows = [row for row in rows if row["method"] == method.name]
        out: Dict[str, object] = {
            "method": method.name,
            "method_class": method.method_class,
            "count": len(method_rows),
        }
        for metric in [*METRIC_NAMES, *DELTA_NAMES]:
            values = np.asarray([finite_float(row.get(metric, float("nan"))) for row in method_rows], dtype=np.float64)
            values = values[np.isfinite(values)]
            out[f"{metric}_mean"] = float(np.mean(values)) if values.size else float("nan")
            out[f"{metric}_std"] = float(np.std(values)) if values.size else float("nan")
        summary_rows.append(out)
    return summary_rows


def write_summary_csv(path: Path, rows: Sequence[Dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    metrics = [*METRIC_NAMES, *DELTA_NAMES]
    fieldnames = ["method", "method_class", "count"]
    for metric in metrics:
        fieldnames.extend([f"{metric}_mean", f"{metric}_std"])
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            out = dict(row)
            for key in fieldnames:
                if key not in ("method", "method_class", "count"):
                    out[key] = csv_value(out.get(key, float("nan")))
            writer.writerow({name: out.get(name, "") for name in fieldnames})


def metric_table_lines(summary_rows: Sequence[Dict[str, object]]) -> List[str]:
    lines = [
        "| Method | Count | Edge density | ΔEdge density | Sobel mean | ΔSobel | Skeleton density | ΔSkeleton density | Endpoint density |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in summary_rows:
        lines.append(
            "| {method} | {count} | {edge_density:.6f} | {delta_edge_density:.6f} | "
            "{sobel_mean:.6f} | {delta_sobel_mean:.6f} | {skeleton_density:.6f} | "
            "{delta_skeleton_density:.6f} | {endpoint_density:.6f} |".format(
                method=row["method"],
                count=int(row["count"]),
                edge_density=finite_float(row.get("edge_density_mean")),
                delta_edge_density=finite_float(row.get("delta_edge_density_vs_original_mean")),
                sobel_mean=finite_float(row.get("sobel_mean_mean")),
                delta_sobel_mean=finite_float(row.get("delta_sobel_mean_vs_original_mean")),
                skeleton_density=finite_float(row.get("skeleton_density_mean")),
                delta_skeleton_density=finite_float(row.get("delta_skeleton_density_vs_original_mean")),
                endpoint_density=finite_float(row.get("skeleton_endpoint_density_mean")),
            )
        )
    return lines


def write_method_note(path: Path, suite: str, manifest_path: Path, resize_to: Optional[Tuple[int, int]]) -> None:
    lines = [
        f"# Stage1 downstream edge proxy note: {suite}",
        "",
        "本结果是无 GT 的边缘结构代理验证，不替代 MyEdge / DiffusionEdge 体系中的 ODS、OIS、AP、AC 或人工标注边缘评测。",
        "",
        "## 固定口径",
        "",
        f"- manifest: `{manifest_path}`",
        f"- resize: `{resize_to}`" if resize_to else "- resize: `none`",
        "- edge method: grayscale -> Gaussian blur -> Sobel magnitude -> Otsu threshold -> binary edge mask",
        "- topology proxy: connected components and skeleton endpoints/branchpoints from the binary edge mask",
        "",
        "## 可写边界",
        "",
        "- 可用于筛查 Stage1 是否增加边缘响应、连通结构或碎片化风险。",
        "- 可用于选择投稿级定性图候选样本。",
        "- 不能写成已经证明下游边缘检测精度提升。",
        "- 不能把边缘响应变多直接解释为生物结构更准确。",
    ]
    write_lines(path, lines)


def edge_overlay(path: Path, resize_to: Optional[Tuple[int, int]]) -> np.ndarray:
    image = resize_bgr(read_bgr(path), resize_to)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, edge_mask, _ = otsu_edge_mask(gray)
    overlay = image.copy()
    overlay[edge_mask] = (0, 0, 255)
    return cv2.addWeighted(image, 0.72, overlay, 0.28, 0)


def draw_label(tile: np.ndarray, label: str) -> np.ndarray:
    out = tile.copy()
    cv2.rectangle(out, (0, 0), (out.shape[1], 24), (0, 0, 0), -1)
    cv2.putText(out, label, (6, 17), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (255, 255, 255), 1, cv2.LINE_AA)
    return out


def make_panel(
    path: Path,
    title: str,
    stem: str,
    method_paths: Sequence[Tuple[str, Path]],
    resize_to: Optional[Tuple[int, int]],
    overlay_edges: bool,
) -> None:
    tiles = []
    for method_name, image_path in method_paths:
        tile = edge_overlay(image_path, resize_to) if overlay_edges else resize_bgr(read_bgr(image_path), resize_to)
        tiles.append(draw_label(tile, method_name))
    if not tiles:
        return
    h = max(tile.shape[0] for tile in tiles)
    normalized = []
    for tile in tiles:
        if tile.shape[0] != h:
            scale = h / tile.shape[0]
            tile = cv2.resize(tile, (int(tile.shape[1] * scale), h), interpolation=cv2.INTER_CUBIC)
        normalized.append(tile)
    panel = np.concatenate(normalized, axis=1)
    header = np.zeros((34, panel.shape[1], 3), dtype=np.uint8)
    cv2.putText(header, f"{title}: {stem}", (8, 23), cv2.FONT_HERSHEY_SIMPLEX, 0.62, (255, 255, 255), 1, cv2.LINE_AA)
    panel = np.concatenate([header, panel], axis=0)
    write_bgr(path, panel)


def select_stage_stems(rows: Sequence[Dict[str, object]], panel_count: int) -> List[str]:
    final_rows = [row for row in rows if row["method"] == "Final"]
    final_rows = sorted(
        final_rows,
        key=lambda row: (
            finite_float(row.get("delta_sobel_mean_vs_original")),
            finite_float(row.get("delta_edge_density_vs_original")),
        ),
        reverse=True,
    )
    return [str(row["stem"]) for row in final_rows[:panel_count]]


def select_compare_stems(rows: Sequence[Dict[str, object]], panel_count: int) -> List[str]:
    by_stem: Dict[str, Dict[str, Dict[str, object]]] = {}
    for row in rows:
        by_stem.setdefault(str(row["stem"]), {})[str(row["method"])] = row

    scored = []
    for stem, method_rows in by_stem.items():
        ours = method_rows.get("Ours")
        histo = method_rows.get("Histoformer")
        hlrp = method_rows.get("HLRP")
        wwpf = method_rows.get("WWPF")
        if ours is None:
            continue
        score = 0.0
        for candidate in (histo, hlrp, wwpf):
            if candidate is not None:
                score += max(0.0, finite_float(candidate.get("edge_density")) - finite_float(ours.get("edge_density")))
                score += max(0.0, finite_float(candidate.get("skeleton_endpoint_density")) - finite_float(ours.get("skeleton_endpoint_density")))
        scored.append((score, stem))
    scored.sort(reverse=True)
    return [stem for _, stem in scored[:panel_count]]


def make_panels(result: SuiteResult, indexes: Dict[str, ImageIndex], resize_to: Optional[Tuple[int, int]], panel_count: int) -> None:
    panel_dir = result.output_dir / "qualitative_panels"
    panel_dir.mkdir(parents=True, exist_ok=True)

    if result.suite == "stage":
        stems = select_stage_stems(result.rows, panel_count)
        method_order = ["Original", "BPH", "IMF1Ray", "RGHS", "CLAHE", "Fused", "Final"]
        title = "stage_progress_candidate"
    else:
        stems = select_compare_stems(result.rows, panel_count)
        method_order = ["Original", "Ours", "GDCP", "CBF", "SGUIE-Net", "WWPF", "HLRP", "Histoformer"]
        title = "compare_failure_candidate"

    for stem in stems:
        method_paths = [(name, indexes[name].by_key[stem]) for name in method_order if name in indexes and stem in indexes[name].by_key]
        make_panel(
            panel_dir / f"{title}_{safe_output_stem(stem)}.png",
            title,
            stem,
            method_paths,
            resize_to,
            overlay_edges=False,
        )
        make_panel(
            panel_dir / f"{title}_{safe_output_stem(stem)}_edge_overlay.png",
            f"{title}_edge_overlay",
            stem,
            method_paths,
            resize_to,
            overlay_edges=True,
        )


def run_suite(
    suite: str,
    registry: Dict[str, object],
    manifest_path: Path,
    output_dir: Path,
    resize_to: Optional[Tuple[int, int]],
    limit: Optional[int],
    quiet: bool,
    make_qualitative_panels: bool,
    panel_count: int,
) -> SuiteResult:
    started = time.perf_counter()
    output_dir.mkdir(parents=True, exist_ok=True)
    original_dir, methods = build_method_infos(registry, suite)
    indexes = method_indexes(methods)
    failures: List[Dict[str, str]] = []

    for method_name, index in indexes.items():
        for key, first, second in index.collisions:
            failures.append(
                {
                    "suite": suite,
                    "phase": "indexing",
                    "method": method_name,
                    "stem": key,
                    "path": first,
                    "error": f"collision: {second}",
                }
            )

    method_indexes_for_common = {name: index for name, index in indexes.items() if name != "Original"}
    planned_stems, matching_failures = select_common_stems(
        original_index=indexes["Original"],
        method_indexes=method_indexes_for_common,
        manifest_stems=read_manifest(manifest_path),
        limit=limit,
    )
    for failure in matching_failures:
        failure["suite"] = suite
        failures.append(failure)

    write_lines(output_dir / "planned_manifest.txt", planned_stems)
    rows: List[Dict[str, object]] = []
    success_by_stem = {stem: set() for stem in planned_stems}
    method_names = {method.name for method in methods}

    for i, stem in enumerate(planned_stems, start=1):
        for method in methods:
            try:
                image_path = indexes[method.name].by_key[stem]
                metrics = compute_edge_metrics(image_path, resize_to)
                row: Dict[str, object] = {
                    "suite": suite,
                    "method": method.name,
                    "method_class": method.method_class,
                    "stem": stem,
                    "image_path": str(image_path),
                    **metrics,
                }
                rows.append(row)
                success_by_stem[stem].add(method.name)
            except Exception as exc:
                failures.append(
                    {
                        "suite": suite,
                        "phase": "evaluation",
                        "method": method.name,
                        "stem": stem,
                        "path": str(indexes.get(method.name, ImageIndex({}, [])).by_key.get(stem, "")),
                        "error": str(exc),
                    }
                )
        if not quiet and (i == 1 or i == len(planned_stems) or i % 25 == 0):
            print(f"[{suite}] {i}/{len(planned_stems)} {stem}")

    complete_stems = [stem for stem in planned_stems if success_by_stem[stem] == method_names]
    write_lines(output_dir / "complete_case_manifest.txt", complete_stems)
    add_deltas(rows)

    summary_rows = summarize([row for row in rows if str(row["stem"]) in set(complete_stems)], methods)
    write_csv(output_dir / "per_image_metrics.csv", rows)
    write_summary_csv(output_dir / "summary.csv", summary_rows)
    write_failures_csv(output_dir / "failed_files.csv", failures)
    write_method_note(output_dir / "method_note.md", suite, manifest_path, resize_to)

    summary = {
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "suite": suite,
        "proxy_type": "no_gt_sobel_otsu_edge_structure",
        "manifest": str(manifest_path),
        "output_dir": str(output_dir),
        "resize_to": list(resize_to) if resize_to else None,
        "planned_count": len(planned_stems),
        "complete_case_count": len(complete_stems),
        "failure_count": len(failures),
        "elapsed_seconds": round(time.perf_counter() - started, 3),
        "methods": [method.__dict__ | {"directory": str(method.directory)} for method in methods],
        "summary_csv": str(output_dir / "summary.csv"),
        "per_image_metrics_csv": str(output_dir / "per_image_metrics.csv"),
        "method_note": str(output_dir / "method_note.md"),
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        f"# Stage1 downstream edge proxy summary: {suite}",
        "",
        f"- created_at: `{summary['created_at']}`",
        f"- proxy_type: `{summary['proxy_type']}`",
        f"- manifest: `{manifest_path}`",
        f"- planned_count: `{len(planned_stems)}`",
        f"- complete_case_count: `{len(complete_stems)}`",
        f"- failure_count: `{len(failures)}`",
        f"- elapsed_seconds: `{summary['elapsed_seconds']}`",
        "",
        "本表是无 GT 边缘结构代理统计，只能用于 Stage1 支撑包筛查和选图，不能替代 MyEdge 的 ODS/OIS/AP/AC。",
        "",
        *metric_table_lines(summary_rows),
        "",
        "## Outputs",
        "",
        f"- `summary.csv`",
        f"- `per_image_metrics.csv`",
        f"- `method_note.md`",
        f"- `planned_manifest.txt`",
        f"- `complete_case_manifest.txt`",
        f"- `failed_files.csv`",
    ]
    write_lines(output_dir / "summary.md", lines)

    result = SuiteResult(
        suite=suite,
        output_dir=output_dir,
        rows=rows,
        failures=failures,
        complete_stems=complete_stems,
        methods=methods,
    )
    if make_qualitative_panels and complete_stems:
        make_panels(result, indexes, resize_to, panel_count)
    return result


def write_root_index(output_root: Path, results: Sequence[SuiteResult]) -> None:
    lines = [
        "# Stage1 enhancement-to-edge support package",
        "",
        f"Created at: `{datetime.now().isoformat(timespec='seconds')}`",
        "",
        "本目录保存 Stage1 的无 GT 边缘结构代理验证结果。它用于支撑后续 MyEdge 主论文中的 task-driven structure-preserving enhancement 证据链，不能替代带 GT 的边缘检测主实验。",
        "",
        "| Suite | Complete cases | Failures | Elapsed seconds | Summary | Per-image | Panels |",
        "| --- | ---: | ---: | ---: | --- | --- | --- |",
    ]
    for result in results:
        rel = result.output_dir.relative_to(output_root)
        panel_dir = result.output_dir / "qualitative_panels"
        summary_path = result.output_dir / "summary.json"
        elapsed = ""
        if summary_path.is_file():
            try:
                elapsed = str(json.loads(summary_path.read_text(encoding="utf-8")).get("elapsed_seconds", ""))
            except Exception:
                elapsed = ""
        lines.append(
            f"| `{result.suite}` | {len(result.complete_stems)} | {len(result.failures)} | {elapsed} | "
            f"`{rel / 'summary.md'}` | `{rel / 'per_image_metrics.csv'}` | "
            f"`{rel / 'qualitative_panels'}` |"
        )
    lines.extend(
        [
            "",
            "## Interpretation boundary",
            "",
            "- 可写：Stage1 已形成可供 MyEdge 接入的增强阶段、外部增强方法和边缘结构代理结果包。",
            "- 不可写：Stage1 已经证明 ODS/OIS/AP/AC 提升。",
            "- 不可写：边缘响应变多等于生物结构更准确。",
        ]
    )
    write_lines(output_root / "index.md", lines)


def main() -> int:
    args = parse_args()
    registry = load_registry(args.registry)
    output_root = resolve_project_path(args.output_root)
    output_root.mkdir(parents=True, exist_ok=True)
    resize_to = None if args.no_resize else tuple(args.resize_to)

    suites = ["stage", "compare"] if args.suite == "both" else [args.suite]
    results: List[SuiteResult] = []
    for suite in suites:
        manifest_path = resolve_project_path(args.stage_manifest if suite == "stage" else args.compare_manifest)
        output_dir = output_root / ("stage_full502_proxy" if suite == "stage" else "compare9_complete496_proxy")
        result = run_suite(
            suite=suite,
            registry=registry,
            manifest_path=manifest_path,
            output_dir=output_dir,
            resize_to=resize_to,
            limit=args.limit,
            quiet=args.quiet,
            make_qualitative_panels=not args.no_panels,
            panel_count=args.panel_count,
        )
        results.append(result)
        print(f"[DONE] {suite}: {len(result.complete_stems)} complete cases -> {result.output_dir}")

    write_root_index(output_root, results)
    print(f"[DONE] index -> {output_root / 'index.md'}")
    return 0 if all(result.complete_stems for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
