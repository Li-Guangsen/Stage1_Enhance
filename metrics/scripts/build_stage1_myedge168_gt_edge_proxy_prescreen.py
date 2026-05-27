from __future__ import annotations

import csv
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any

import cv2
import numpy as np
from scipy import ndimage as ndi
from skimage.morphology import skeletonize


PROJECT_ROOT = Path("D:/Desktop/Stage1Codex")
MYEDGE_ROOT = Path("D:/Desktop/MyEdgeCodex")
MANIFEST = MYEDGE_ROOT / "docs/paper_assets/stage1_coupling/stage1_myedge_168_coupling_manifest_20260524.csv"
OUT_PREFIX = PROJECT_ROOT / "docs/evidence/tlvc01_topology_locked/proxy_prescreen/stage1_myedge168_gt_edge_proxy_prescreen_topology_locked_visual_chroma_v1_myedgeinput_grayplane090_anchorfix_20260527_cn"
TOLERANCE_PX = 2

DOWNSTREAM_ROOT = PROJECT_ROOT / "experiments/downstream_driven_v1/outputs/myedge168"

VARIANTS = [
    {
        "label": "raw_input_anchor",
        "kind": "raw",
        "role": "raw MyEdge detector-domain input anchor",
    },
    {
        "label": "stage1_original_copy",
        "kind": "stage1_original",
        "role": "Stage1 repo input copy at data/inputImg/Original; protocol diagnostic for raw-copy mismatch",
    },
    {
        "label": "legacy_stage1_final",
        "kind": "manifest_path",
        "manifest_column": "stage1_final_path",
        "role": "locked Stage1 Final known to hurt fixed-detector MyEdge metrics",
    },
    {
        "label": "edge_preserve_original_control",
        "kind": "downstream_variant",
        "role": "same-chain original-control sanity check",
    },
    {
        "label": "edge_preserve_raw_bph_mild_v1",
        "kind": "downstream_variant",
        "role": "P4 mild raw-BPH edge-preserve variant",
    },
    {
        "label": "edge_preserve_raw_bph_moderate_v1",
        "kind": "downstream_variant",
        "role": "P4 moderate raw-BPH edge-preserve variant",
    },
    {
        "label": "generic_luma_clahe_mild_v1",
        "kind": "downstream_variant",
        "role": "P7 generic luminance CLAHE control",
    },
    {
        "label": "generic_luma_gamma_mild_v1",
        "kind": "downstream_variant",
        "role": "P7 generic luminance gamma control",
    },
    {
        "label": "edge_safe_gamma_bph_v1",
        "kind": "downstream_variant",
        "role": "P9 candidate, not MyEdge-evaluated yet",
    },
    {
        "label": "boundary_aware_luma_bph_v1",
        "kind": "downstream_variant",
        "role": "P10 candidate, not MyEdge-evaluated yet",
    },
    {
        "label": "skeleton_safe_luma_bph_v1",
        "kind": "downstream_variant",
        "role": "P11 skeleton-safe smooth-only candidate, not MyEdge-evaluated yet",
    },
    {
        "label": "c01_microstructure_csp_v1",
        "kind": "downstream_variant",
        "role": "P16 C01 microstructure-CSP candidate, Stage1 output only",
    },
    {
        "label": "topology_guarded_microfusion_v1",
        "kind": "downstream_variant",
        "role": "P17 topology-guarded microfusion candidate, Stage1 output only",
    },
    {
        "label": "topology_pruned_microfusion_v1",
        "kind": "downstream_variant",
        "role": "P18 component-pruned topology microfusion candidate, Stage1 output only",
    },
    {
        "label": "baseline_stabilized_microfusion_v1",
        "kind": "downstream_variant",
        "role": "P19 baseline-stabilized soft-pruned topology microfusion candidate, Stage1 output only",
    },
    {
        "label": "endpoint_stabilized_weak_boundary_v1",
        "kind": "downstream_variant",
        "role": "P20 endpoint-stabilized weak-boundary candidate, Stage1 output only",
    },
    {
        "label": "balanced_weak_boundary_pyramid_fusion_v1",
        "kind": "downstream_variant",
        "role": "P21 balanced P14/P15 weak-boundary candidate, Stage1 output only",
    },
    {
        "label": "ac_guarded_weak_boundary_fusion_v1",
        "kind": "downstream_variant",
        "role": "P22 AC/false-edge guarded weak-boundary candidate, Stage1 output only",
    },
    {
        "label": "precision_rebalanced_ac_guarded_weak_boundary_fusion_v1",
        "kind": "downstream_variant",
        "role": "P23 precision-rebalanced AC/false-edge guarded weak-boundary candidate, Stage1 output only",
    },
    {
        "label": "false_edge_floor_ac_guarded_weak_boundary_fusion_v1",
        "kind": "downstream_variant",
        "role": "P24 false-edge-floor AC/false-edge guarded weak-boundary candidate, Stage1 output only",
    },
    {
        "label": "ap_preserving_ac_guarded_weak_boundary_fusion_v1",
        "kind": "downstream_variant",
        "role": "P25 AP-preserving AC/false-edge guarded weak-boundary candidate, Stage1 output only",
    },
    {
        "label": "dual_anchor_false_edge_floor_v1",
        "kind": "downstream_variant",
        "role": "P26 dual-anchor false-edge floor candidate, Stage1 output only",
    },
    {
        "label": "raw_detail_lowfreq_chroma_v1",
        "kind": "downstream_variant",
        "role": "P27 raw-detail low-frequency luma/chroma candidate, Stage1 output only",
    },
    {
        "label": "raw_detail_chroma_guard_v1",
        "kind": "downstream_variant",
        "role": "P28 P27-based chroma false-edge guard candidate, Stage1 output only",
    },
    {
        "label": "d01_structure_flow_v1",
        "kind": "downstream_variant",
        "root": "experiments/downstream_driven_v2/outputs/myedge168/d01_structure_flow_v1",
        "role": "D01 downstream_driven_v2 modular structure-flow candidate, Stage1 output only",
    },
    {
        "label": "topology_locked_visual_chroma_full_flow_v1",
        "kind": "downstream_variant",
        "root": "experiments/topology_locked_visual_chroma_full_flow_v1/outputs/myedge168_v1",
        "role": "FA01-follow-up Stage1-only new method family: full branch evidence with raw-topology-locked visual chroma output",
    },
    {
        "label": "topology_locked_visual_chroma_full_flow_v1_cvgraylock092",
        "kind": "downstream_variant",
        "root": "experiments/topology_locked_visual_chroma_full_flow_v1/outputs/myedge168_v1_cvgraylock092",
        "role": "Current topology-locked visual-chroma flow with final cv-gray projection lock for raw-compatible fixed-detector edge topology",
    },
    {
        "label": "topology_locked_visual_chroma_full_flow_v1_grayplane090",
        "kind": "downstream_variant",
        "root": "experiments/topology_locked_visual_chroma_full_flow_v1/outputs/myedge168_v1_grayplane090",
        "role": "Current topology-locked visual-chroma flow with raw-gray-plane chroma projection, preserving cv2 BGR2GRAY topology while retaining branch chroma evidence",
    },
    {
        "label": "topology_locked_visual_chroma_full_flow_v1_grayplane090_anchorfix",
        "kind": "downstream_variant",
        "root": "experiments/topology_locked_visual_chroma_full_flow_v1/outputs/myedge168_v1_grayplane090_anchorfix",
        "role": "Raw-gray-plane chroma projection after fixing bounded output selection to use original anchor and final post-bound projection",
    },
    {
        "label": "topology_locked_visual_chroma_full_flow_v1_myedgeinput_grayplane090_anchorfix",
        "kind": "downstream_variant",
        "root": "experiments/topology_locked_visual_chroma_full_flow_v1/outputs/myedge168_v1_myedgeinput_grayplane090_anchorfix",
        "role": "Raw-gray-plane chroma projection generated from the exact MyEdge fixed-detector raw input copy",
    },
]

HIGHER_IS_BETTER = {
    "boundary_precision_tol",
    "boundary_recall_tol",
    "boundary_f1_tol",
}

LOWER_IS_BETTER = {
    "false_edge_ratio_tol",
    "missed_gt_ratio_tol",
    "pred_components_per_1k_edge_px",
    "endpoints_per_1k_skel_px",
    "edge_width_proxy",
    "mean_pred_to_gt_distance",
    "p95_pred_to_gt_distance",
    "mean_gt_to_pred_distance",
    "p95_gt_to_pred_distance",
    "mean_abs_luma_delta_vs_raw",
    "p95_abs_luma_delta_vs_raw",
}


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(PROJECT_ROOT.resolve())).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def read_manifest() -> list[dict[str, str]]:
    with MANIFEST.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def read_bgr(path: Path) -> np.ndarray:
    data = np.fromfile(str(path), dtype=np.uint8)
    image = cv2.imdecode(data, cv2.IMREAD_COLOR)
    if image is None:
        raise RuntimeError(f"cv2.imdecode failed: {path}")
    return image


def read_gt(path: Path, shape: tuple[int, int]) -> np.ndarray:
    data = np.fromfile(str(path), dtype=np.uint8)
    image = cv2.imdecode(data, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise RuntimeError(f"cv2.imdecode failed: {path}")
    gt = image > 0
    if gt.shape != shape:
        gt = cv2.resize(gt.astype(np.uint8), (shape[1], shape[0]), interpolation=cv2.INTER_NEAREST) > 0
    return gt


def variant_path(row: dict[str, str], variant: dict[str, str]) -> Path:
    kind = variant["kind"]
    if kind == "raw":
        return Path(row["raw_input_path"])
    if kind == "stage1_original":
        return PROJECT_ROOT / "data/inputImg/Original" / f"{row['stem']}.jpg"
    if kind == "manifest_path":
        return Path(row[variant["manifest_column"]])
    if kind == "downstream_variant":
        if "root" in variant:
            return PROJECT_ROOT / variant["root"] / "png" / "Final" / f"{row['stem']}_Final.png"
        return DOWNSTREAM_ROOT / variant["label"] / "png" / "Final" / f"{row['stem']}_Final.png"
    raise ValueError(f"Unknown variant kind: {kind}")


def safe_div(num: float, den: float) -> float:
    return float(num / den) if den > 0 else float("nan")


def image_edge_mask(image: np.ndarray) -> tuple[np.ndarray, np.ndarray, float]:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    gray_f = blurred.astype(np.float32) / 255.0
    gx = cv2.Sobel(gray_f, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(gray_f, cv2.CV_32F, 0, 1, ksize=3)
    mag = cv2.magnitude(gx, gy)
    max_mag = float(np.max(mag))
    if max_mag <= 1e-12:
        return gray, np.zeros_like(gray, dtype=bool), 0.0
    mag_u8 = np.clip(mag / max_mag * 255.0, 0, 255).astype(np.uint8)
    threshold_u8, edge_u8 = cv2.threshold(mag_u8, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    threshold = float(threshold_u8) / 255.0 * max_mag
    return gray, edge_u8 > 0, threshold


def connected_components(mask: np.ndarray) -> int:
    structure = np.ones((3, 3), dtype=np.uint8)
    _, count = ndi.label(mask.astype(np.uint8), structure=structure)
    return int(count)


def endpoint_count(skeleton: np.ndarray) -> int:
    if not np.any(skeleton):
        return 0
    kernel = np.ones((3, 3), dtype=np.uint8)
    neighbor_count = ndi.convolve(skeleton.astype(np.uint8), kernel, mode="constant", cval=0)
    return int(np.count_nonzero(skeleton & (neighbor_count == 2)))


def image_metrics(
    row: dict[str, str],
    variant: dict[str, str],
    raw_gray: np.ndarray,
    gt: np.ndarray,
) -> dict[str, Any]:
    path = variant_path(row, variant)
    image = read_bgr(path)
    if image.shape[:2] != raw_gray.shape:
        image = cv2.resize(image, (raw_gray.shape[1], raw_gray.shape[0]), interpolation=cv2.INTER_CUBIC)

    gray, pred, threshold = image_edge_mask(image)
    pixels = float(pred.size)
    pred_count = float(np.count_nonzero(pred))
    gt_count = float(np.count_nonzero(gt))

    dist_to_gt = ndi.distance_transform_edt(~gt)
    dist_to_pred = ndi.distance_transform_edt(~pred)
    matched_pred = pred & (dist_to_gt <= TOLERANCE_PX)
    matched_gt = gt & (dist_to_pred <= TOLERANCE_PX)
    matched_pred_count = float(np.count_nonzero(matched_pred))
    matched_gt_count = float(np.count_nonzero(matched_gt))
    false_pred_count = pred_count - matched_pred_count
    missed_gt_count = gt_count - matched_gt_count
    precision = safe_div(matched_pred_count, pred_count)
    recall = safe_div(matched_gt_count, gt_count)
    f1 = 2.0 * precision * recall / (precision + recall) if math.isfinite(precision + recall) and (precision + recall) > 0 else float("nan")

    comp_count = connected_components(pred)
    skel = skeletonize(pred)
    skel_count = float(np.count_nonzero(skel))
    endpoints = float(endpoint_count(skel))
    pred_dist_values = dist_to_gt[pred]
    gt_dist_values = dist_to_pred[gt]
    abs_luma_delta = np.abs(gray.astype(np.float32) - raw_gray.astype(np.float32))

    return {
        "stem": row["stem"],
        "variant": variant["label"],
        "role": variant["role"],
        "source_path": str(path),
        "edge_threshold": threshold,
        "pred_edge_pixels": int(pred_count),
        "gt_edge_pixels": int(gt_count),
        "pred_edge_density": safe_div(pred_count, pixels),
        "gt_edge_density": safe_div(gt_count, pixels),
        "boundary_precision_tol": precision,
        "boundary_recall_tol": recall,
        "boundary_f1_tol": f1,
        "false_edge_pixels_tol": int(false_pred_count),
        "false_edge_ratio_tol": safe_div(false_pred_count, pred_count),
        "false_edge_density_tol": safe_div(false_pred_count, pixels),
        "missed_gt_pixels_tol": int(missed_gt_count),
        "missed_gt_ratio_tol": safe_div(missed_gt_count, gt_count),
        "pred_component_count": comp_count,
        "pred_components_per_1k_edge_px": safe_div(comp_count * 1000.0, pred_count),
        "skeleton_pixels": int(skel_count),
        "skeleton_endpoint_count": int(endpoints),
        "endpoints_per_1k_skel_px": safe_div(endpoints * 1000.0, skel_count),
        "edge_width_proxy": safe_div(pred_count, skel_count),
        "mean_pred_to_gt_distance": float(np.mean(pred_dist_values)) if pred_dist_values.size else float("nan"),
        "p95_pred_to_gt_distance": float(np.percentile(pred_dist_values, 95)) if pred_dist_values.size else float("nan"),
        "mean_gt_to_pred_distance": float(np.mean(gt_dist_values)) if gt_dist_values.size else float("nan"),
        "p95_gt_to_pred_distance": float(np.percentile(gt_dist_values, 95)) if gt_dist_values.size else float("nan"),
        "mean_abs_luma_delta_vs_raw": float(np.mean(abs_luma_delta)),
        "p95_abs_luma_delta_vs_raw": float(np.percentile(abs_luma_delta, 95)),
    }


def finite_mean(values: list[float]) -> float | None:
    finite = [float(v) for v in values if math.isfinite(float(v))]
    return float(np.mean(finite)) if finite else None


def summarize(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_variant: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        by_variant.setdefault(str(row["variant"]), []).append(row)

    metric_keys = [
        "pred_edge_density",
        "boundary_precision_tol",
        "boundary_recall_tol",
        "boundary_f1_tol",
        "false_edge_ratio_tol",
        "false_edge_density_tol",
        "missed_gt_ratio_tol",
        "pred_components_per_1k_edge_px",
        "endpoints_per_1k_skel_px",
        "edge_width_proxy",
        "mean_pred_to_gt_distance",
        "p95_pred_to_gt_distance",
        "mean_gt_to_pred_distance",
        "p95_gt_to_pred_distance",
        "mean_abs_luma_delta_vs_raw",
        "p95_abs_luma_delta_vs_raw",
    ]
    out: list[dict[str, Any]] = []
    for variant in [v["label"] for v in VARIANTS]:
        v_rows = by_variant.get(variant, [])
        if not v_rows:
            continue
        summary = {
            "variant": variant,
            "role": v_rows[0]["role"],
            "image_count": len(v_rows),
            "tolerance_px": TOLERANCE_PX,
        }
        for key in metric_keys:
            summary[f"mean_{key}"] = finite_mean([float(r[key]) for r in v_rows])
        out.append(summary)
    return out


def delta_against_raw(summaries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_variant = {row["variant"]: row for row in summaries}
    raw = by_variant["raw_input_anchor"]
    rows: list[dict[str, Any]] = []
    fields = sorted(HIGHER_IS_BETTER | LOWER_IS_BETTER)
    for summary in summaries:
        row = {
            "variant": summary["variant"],
            "anchor": "raw_input_anchor",
        }
        favorable = 0
        unfavorable = 0
        for field in fields:
            key = f"mean_{field}"
            value = summary.get(key)
            base = raw.get(key)
            delta = None if value is None or base is None else float(value - base)
            row[f"delta_{field}"] = delta
            if delta is None:
                continue
            if field in HIGHER_IS_BETTER:
                if delta > 0:
                    favorable += 1
                elif delta < 0:
                    unfavorable += 1
            elif field in LOWER_IS_BETTER:
                if delta < 0:
                    favorable += 1
                elif delta > 0:
                    unfavorable += 1

        f1_delta = row.get("delta_boundary_f1_tol")
        false_delta = row.get("delta_false_edge_ratio_tol")
        endpoint_delta = row.get("delta_endpoints_per_1k_skel_px")
        if summary["variant"] == "raw_input_anchor":
            decision = "raw_anchor"
        elif summary["variant"] == "edge_preserve_original_control":
            decision = "raw_equivalent_control"
        elif f1_delta is not None and false_delta is not None and endpoint_delta is not None:
            if f1_delta >= 0 and false_delta <= 0 and endpoint_delta <= 0:
                decision = "proxy_positive_candidate"
            elif f1_delta >= -0.002 and false_delta <= 0.005 and endpoint_delta <= 1.0:
                decision = "proxy_edge_safe_candidate"
            elif f1_delta <= -0.010 or false_delta >= 0.020 or endpoint_delta >= 2.0:
                decision = "proxy_negative_or_risky"
            else:
                decision = "proxy_mixed_watch"
        else:
            decision = "proxy_incomplete"
        row["favorable_metric_count"] = favorable
        row["unfavorable_metric_count"] = unfavorable
        row["pre_screen_decision"] = decision
        rows.append(row)
    return rows


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row.keys():
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def fmt(value: Any, digits: int = 6) -> str:
    if value is None:
        return "NA"
    if isinstance(value, (int, np.integer)):
        return str(int(value))
    try:
        value_f = float(value)
    except (TypeError, ValueError):
        return str(value)
    if not math.isfinite(value_f):
        return "NA"
    return f"{value_f:.{digits}f}"


def write_markdown(path: Path, summaries: list[dict[str, Any]], deltas: list[dict[str, Any]], failures: list[dict[str, Any]]) -> None:
    delta_by_variant = {row["variant"]: row for row in deltas}
    lines = [
        "# Stage1/MyEdge168 GT Edge Proxy Prescreen",
        "",
        f"Date: {datetime.now().strftime('%Y-%m-%d')}",
        "",
        "## Scope",
        "",
        "- Reads MyEdge 168-image coupling manifest, raw inputs, GT edge maps, locked Stage1 Final outputs, and existing downstream-driven Stage1 candidate outputs.",
        "- Builds image-gradient proxy edges with Sobel magnitude + Otsu threshold, then matches them to GT edge maps with 2 px tolerance.",
        "- Does not run MyEdge sampling, WSL `eval.py`, WSL `show.py`, training, or formal Stage1 full502/full2770 enhancement.",
        "- This is a prescreen only. It cannot replace fixed-detector ODS/OIS/AP/AC, detector MAT structure proxy, repeat/control, or paper-ready downstream evidence.",
        "",
        "## Summary",
        "",
        "| Variant | n | Decision | F1 | Precision | Recall | False-edge ratio | Missed-GT ratio | Components / 1k edge px | Endpoints / 1k skeleton px | Mean abs luma delta | dF1 | dFalse-edge | dEndpoints |",
        "|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for summary in summaries:
        delta = delta_by_variant.get(summary["variant"], {})
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{summary['variant']}`",
                    str(summary["image_count"]),
                    f"`{delta.get('pre_screen_decision', 'NA')}`",
                    fmt(summary.get("mean_boundary_f1_tol")),
                    fmt(summary.get("mean_boundary_precision_tol")),
                    fmt(summary.get("mean_boundary_recall_tol")),
                    fmt(summary.get("mean_false_edge_ratio_tol")),
                    fmt(summary.get("mean_missed_gt_ratio_tol")),
                    fmt(summary.get("mean_pred_components_per_1k_edge_px")),
                    fmt(summary.get("mean_endpoints_per_1k_skel_px")),
                    fmt(summary.get("mean_mean_abs_luma_delta_vs_raw")),
                    fmt(delta.get("delta_boundary_f1_tol")),
                    fmt(delta.get("delta_false_edge_ratio_tol")),
                    fmt(delta.get("delta_endpoints_per_1k_skel_px")),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Reading",
            "",
            "- `proxy_positive_candidate`: the image-gradient proxy improves or preserves F1 while reducing false-edge ratio and skeleton endpoints versus raw.",
            "- `raw_equivalent_control`: the Stage1 diagnostic chain reproduced raw input for the control variant; this is a sanity check, not an enhancement gain.",
            "- `proxy_edge_safe_candidate`: the proxy remains close to raw under small F1, false-edge, and endpoint tolerances.",
            "- `proxy_mixed_watch`: mixed proxy behavior; do not prioritize without detector evidence.",
            "- `proxy_negative_or_risky`: likely boundary/proxy risk before detector sampling.",
            "",
            "## Boundary",
            "",
            "- These rows are image-gradient-to-GT proxies, not detector predictions.",
            "- A candidate can pass this prescreen and still fail fixed DiffusionEdge/MSFI sampling.",
            "- A candidate cannot be claimed as downstream-improving until MyEdge sampling/eval/show, result intake, detector MAT structure proxy, and review are complete.",
            "- Do not expand any candidate to 2770 full-pool from this prescreen alone.",
            "",
            "## Output Files",
            "",
            f"- Summary CSV: `{rel(OUT_PREFIX.with_suffix('.summary.csv'))}`",
            f"- Delta CSV: `{rel(OUT_PREFIX.with_suffix('.delta_vs_raw.csv'))}`",
            f"- Per-image CSV: `{rel(OUT_PREFIX.with_suffix('.per_image.csv'))}`",
            f"- JSON: `{rel(OUT_PREFIX.with_suffix('.json'))}`",
        ]
    )
    if failures:
        lines.extend(["", "## Failures", "", "| Variant | Stem | Path | Error |", "|---|---|---|---|"])
        for failure in failures[:20]:
            lines.append(
                f"| `{failure['variant']}` | `{failure['stem']}` | `{failure['path']}` | `{failure['error']}` |"
            )
        if len(failures) > 20:
            lines.append(f"| ... | ... | ... | {len(failures) - 20} more failures |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    manifest_rows = read_manifest()
    per_image_rows: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []

    for row in manifest_rows:
        try:
            raw_image = read_bgr(Path(row["raw_input_path"]))
            raw_gray = cv2.cvtColor(raw_image, cv2.COLOR_BGR2GRAY)
            gt = read_gt(Path(row["annotation_path"]), raw_gray.shape)
        except Exception as exc:
            failures.append({"variant": "manifest", "stem": row.get("stem", ""), "path": row.get("raw_input_path", ""), "error": str(exc)})
            continue

        for variant in VARIANTS:
            path = variant_path(row, variant)
            try:
                metrics = image_metrics(row, variant, raw_gray, gt)
                per_image_rows.append(metrics)
            except Exception as exc:
                failures.append({"variant": variant["label"], "stem": row["stem"], "path": str(path), "error": str(exc)})

    summaries = summarize(per_image_rows)
    deltas = delta_against_raw(summaries)

    write_csv(OUT_PREFIX.with_suffix(".per_image.csv"), per_image_rows)
    write_csv(OUT_PREFIX.with_suffix(".summary.csv"), summaries)
    write_csv(OUT_PREFIX.with_suffix(".delta_vs_raw.csv"), deltas)
    write_markdown(OUT_PREFIX.with_suffix(".md"), summaries, deltas, failures)
    OUT_PREFIX.with_suffix(".json").write_text(
        json.dumps(
            {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "status": "complete" if not failures else "complete_with_failures",
                "scope": "Stage1/MyEdge168 image-gradient-to-GT edge proxy prescreen",
                "manifest": str(MANIFEST),
                "image_count": len(manifest_rows),
                "variant_count": len(VARIANTS),
                "tolerance_px": TOLERANCE_PX,
                "summary": summaries,
                "delta_vs_raw": deltas,
                "failure_count": len(failures),
                "failures": failures,
                "boundary": "Prescreen only; does not run MyEdge sampling/eval/show and does not replace fixed-detector ODS/OIS/AP/AC.",
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "status": "complete" if not failures else "complete_with_failures",
                "images": len(manifest_rows),
                "variants": len(VARIANTS),
                "rows": len(per_image_rows),
                "failures": len(failures),
                "report": rel(OUT_PREFIX.with_suffix(".md")),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
