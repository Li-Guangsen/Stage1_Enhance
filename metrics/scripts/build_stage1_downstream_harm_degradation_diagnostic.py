from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from statistics import mean
from typing import Dict, Iterable, List, Sequence, Tuple


THIS_DIR = Path(__file__).resolve().parent
METRICS_DIR = THIS_DIR.parent
PROJECT_ROOT = METRICS_DIR.parent
DEFAULT_MYEDGE_ROOT = Path(r"D:\Desktop\MyEdgeCodex")
DEFAULT_DATE = datetime.now().date().strftime("%Y%m%d")

DEFAULT_OUTPUT_MD = PROJECT_ROOT / "docs" / f"stage1_downstream_edge_harm_degradation_diagnostic_{DEFAULT_DATE}_cn.md"
DEFAULT_OUTPUT_JSON = PROJECT_ROOT / "docs" / f"stage1_downstream_edge_harm_degradation_diagnostic_{DEFAULT_DATE}_cn.json"
DEFAULT_OUTPUT_CSV = PROJECT_ROOT / "docs" / f"stage1_downstream_edge_harm_degradation_proxy_deltas_{DEFAULT_DATE}.csv"

METRIC_COLUMNS = [
    "boundary_f1_tol",
    "boundary_precision_tol",
    "boundary_recall_tol",
    "false_edge_ratio_tol",
    "missed_gt_ratio_tol",
    "pred_components_per_1k_edge_px",
    "endpoints_per_1k_skel_px",
    "p95_pred_to_gt_distance",
]

BAD_IF_POSITIVE = {
    "false_edge_ratio_tol",
    "missed_gt_ratio_tol",
    "pred_components_per_1k_edge_px",
    "endpoints_per_1k_skel_px",
    "p95_pred_to_gt_distance",
}

DEGRADATION_TAG_ORDER = [
    "low_contrast_boundary",
    "blurred_contour",
    "false_edge_background",
    "thin_structure",
    "overlap_clutter",
    "unassigned_proxy",
]

STRUCTURE_COMPARISONS = [
    {
        "source": "p6",
        "detector_group": "msfi_p4",
        "detector": "MSFI 50k",
        "raw_label": "historical_raw_msfi_anchor",
        "candidate_label": "legacy_stage1_final_p1",
        "comparison": "legacy_final_vs_raw_msfi",
        "candidate": "legacy Stage1 Final",
    },
    {
        "source": "p6",
        "detector_group": "diffusionedge_baseline_p5c",
        "detector": "DiffusionEdge baseline 50k",
        "raw_label": "historical_raw_diffusionedge_anchor",
        "candidate_label": "legacy_stage1_final_p1",
        "comparison": "legacy_final_vs_raw_baseline",
        "candidate": "legacy Stage1 Final",
    },
    {
        "source": "p6",
        "detector_group": "msfi_p4",
        "detector": "MSFI 50k",
        "raw_label": "historical_raw_msfi_anchor",
        "candidate_label": "edge_preserve_raw_bph_moderate_v1",
        "comparison": "p4_moderate_vs_raw_msfi",
        "candidate": "edge_preserve_raw_bph_moderate_v1",
    },
    {
        "source": "p6",
        "detector_group": "diffusionedge_baseline_p5c",
        "detector": "DiffusionEdge baseline 50k",
        "raw_label": "historical_raw_diffusionedge_anchor",
        "candidate_label": "edge_preserve_raw_bph_mild_v1",
        "comparison": "p5c_mild_vs_raw_baseline",
        "candidate": "edge_preserve_raw_bph_mild_v1",
    },
    {
        "source": "p7",
        "detector_group": "msfi_p7",
        "detector": "MSFI 50k",
        "raw_label": "historical_raw_msfi_anchor",
        "candidate_label": "generic_luma_gamma_mild_v1",
        "comparison": "p7_gamma_vs_raw_msfi",
        "candidate": "generic_luma_gamma_mild_v1",
    },
    {
        "source": "p7",
        "detector_group": "diffusionedge_baseline_p7",
        "detector": "DiffusionEdge baseline 50k",
        "raw_label": "historical_raw_diffusionedge_anchor",
        "candidate_label": "generic_luma_gamma_mild_v1",
        "comparison": "p7_gamma_vs_raw_baseline",
        "candidate": "generic_luma_gamma_mild_v1",
    },
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build a read-only diagnostic report for where Stage1 enhancement hurts downstream edge detection. "
            "The script reads already-generated Stage1/MyEdge report CSVs only. It does not run Stage1 "
            "enhancement, MyEdge sampling, WSL eval.py/show.py, training, or metric recomputation."
        )
    )
    parser.add_argument("--myedge-root", default=str(DEFAULT_MYEDGE_ROOT))
    parser.add_argument("--output-md", default=str(DEFAULT_OUTPUT_MD))
    parser.add_argument("--output-json", default=str(DEFAULT_OUTPUT_JSON))
    parser.add_argument("--output-csv", default=str(DEFAULT_OUTPUT_CSV))
    return parser.parse_args()


def read_csv(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, rows: Sequence[Dict[str, object]], fieldnames: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({name: row.get(name, "") for name in fieldnames})


def to_float(value: object) -> float:
    if value is None or value == "":
        return float("nan")
    return float(value)


def safe_mean(values: Iterable[float]) -> float | None:
    vals = [v for v in values if v == v]
    if not vals:
        return None
    return mean(vals)


def fmt_float(value: object, digits: int = 6) -> str:
    if value is None or value == "":
        return ""
    try:
        number = float(value)
    except (TypeError, ValueError):
        return str(value)
    return f"{number:.{digits}f}"


def rel(path: Path, root: Path = PROJECT_ROOT) -> str:
    try:
        return str(path.relative_to(root)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def evidence(path: Path, root: Path = PROJECT_ROOT) -> str:
    suffix = "" if path.exists() else " (missing)"
    return f"`{rel(path, root)}`{suffix}"


def table_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def split_tags(value: str) -> List[str]:
    tags = [item.strip() for item in value.split(";") if item.strip()]
    return tags or ["unassigned_proxy"]


def stage_metric_rows(delta_rows: Sequence[Dict[str, str]]) -> List[Dict[str, object]]:
    rows = []
    for row in delta_rows:
        if row.get("group") != "stagewise":
            continue
        lowered = 0
        improved = 0
        for metric in ["ods", "ois", "ap", "ac"]:
            delta = to_float(row.get(f"delta_{metric}"))
            if delta < 0:
                lowered += 1
            elif delta > 0:
                improved += 1
        rows.append(
            {
                "detector": row.get("detector", ""),
                "candidate": row.get("candidate", ""),
                "status": row.get("status", ""),
                "lowered_metric_count": lowered,
                "improved_metric_count": improved,
                "delta_ods": to_float(row.get("delta_ods")),
                "delta_ois": to_float(row.get("delta_ois")),
                "delta_ap": to_float(row.get("delta_ap")),
                "delta_ac": to_float(row.get("delta_ac")),
            }
        )
    return rows


def worst_stage_by_metric(rows: Sequence[Dict[str, object]]) -> Dict[str, Dict[str, object]]:
    out: Dict[str, Dict[str, object]] = {}
    for metric in ["delta_ods", "delta_ois", "delta_ap", "delta_ac"]:
        valid = [row for row in rows if isinstance(row.get(metric), float)]
        if valid:
            out[metric] = min(valid, key=lambda item: float(item[metric]))
    return out


def build_tag_index(rows: Sequence[Dict[str, str]]) -> Dict[str, List[str]]:
    index: Dict[str, List[str]] = {}
    for row in rows:
        index[row["stem"]] = split_tags(row.get("candidate_tags", ""))
    return index


def pivot_structure_rows(rows: Sequence[Dict[str, str]]) -> Dict[Tuple[str, str, str], Dict[str, str]]:
    return {(row["detector_group"], row["label"], row["stem"]): row for row in rows}


def aggregate_structure_deltas(
    p6_rows: Sequence[Dict[str, str]],
    p7_rows: Sequence[Dict[str, str]],
    tag_index: Dict[str, List[str]],
) -> List[Dict[str, object]]:
    p6_pivot = pivot_structure_rows(p6_rows)
    p7_pivot = pivot_structure_rows(p7_rows)
    pivots = {"p6": p6_pivot, "p7": p7_pivot}
    output: List[Dict[str, object]] = []

    for spec in STRUCTURE_COMPARISONS:
        pivot = pivots[spec["source"]]
        raw_keys = {
            stem
            for detector_group, label, stem in pivot.keys()
            if detector_group == spec["detector_group"] and label == spec["raw_label"]
        }
        candidate_keys = {
            stem
            for detector_group, label, stem in pivot.keys()
            if detector_group == spec["detector_group"] and label == spec["candidate_label"]
        }
        stems = sorted(raw_keys & candidate_keys)

        buckets: Dict[str, List[Dict[str, float]]] = defaultdict(list)
        for stem in stems:
            raw = pivot[(spec["detector_group"], spec["raw_label"], stem)]
            candidate = pivot[(spec["detector_group"], spec["candidate_label"], stem)]
            delta_row: Dict[str, float] = {}
            for metric in METRIC_COLUMNS:
                delta_row[metric] = to_float(candidate.get(metric)) - to_float(raw.get(metric))
            all_tags = tag_index.get(stem, ["unassigned_proxy"])
            for tag in all_tags + ["all_auto_candidates"]:
                buckets[tag].append(delta_row)

        for tag in ["all_auto_candidates"] + DEGRADATION_TAG_ORDER:
            metric_rows = buckets.get(tag, [])
            item: Dict[str, object] = {
                "comparison": spec["comparison"],
                "detector": spec["detector"],
                "candidate": spec["candidate"],
                "tag": tag,
                "image_count_multilabel": len(metric_rows),
            }
            for metric in METRIC_COLUMNS:
                item[f"delta_{metric}"] = safe_mean(row[metric] for row in metric_rows)
            output.append(item)
    return output


def count_failure_tags(rows: Sequence[Dict[str, str]]) -> Dict[str, Dict[str, object]]:
    out: Dict[str, Dict[str, object]] = {}
    for category in sorted({row["category"] for row in rows}):
        category_rows = [row for row in rows if row["category"] == category]
        counter: Counter[str] = Counter()
        mean_delta_f1 = safe_mean(to_float(row.get("delta_f1")) for row in category_rows)
        mean_delta_precision = safe_mean(to_float(row.get("delta_precision")) for row in category_rows)
        mean_delta_false_edge = safe_mean(to_float(row.get("delta_false_edge")) for row in category_rows)
        for row in category_rows:
            counter.update(split_tags(row.get("candidate_tags", "")))
        out[category] = {
            "row_count": len(category_rows),
            "tag_counts": dict(counter),
            "mean_delta_f1": mean_delta_f1,
            "mean_delta_precision": mean_delta_precision,
            "mean_delta_false_edge": mean_delta_false_edge,
            "top_stems": [row["stem"] for row in category_rows[:5]],
        }
    return out


def metric_direction_note(metric: str) -> str:
    if metric in BAD_IF_POSITIVE:
        return "positive_delta_is_worse"
    return "negative_delta_is_worse"


def make_markdown(
    output_csv: Path,
    stage_rows: Sequence[Dict[str, object]],
    worst_by_metric: Dict[str, Dict[str, object]],
    structure_rows: Sequence[Dict[str, object]],
    failure_summary: Dict[str, Dict[str, object]],
    evidence_paths: Dict[str, Path],
) -> str:
    lines: List[str] = []
    lines.append("# Stage1 下游边缘负向与退化场景诊断（只读）")
    lines.append("")
    lines.append(f"生成日期：{datetime.now().date().isoformat()}")
    lines.append("")
    lines.append("## 结论边界")
    lines.append("")
    lines.append("- 本报告只读汇总已经落盘的 Stage1 / MyEdge 结果文件。")
    lines.append("- 未运行 Stage1 增强、MyEdge sampling、WSL `eval.py`、WSL `show.py`、训练或指标重算。")
    lines.append("- 退化场景来自 MyEdge 侧 `auto_proxy_quantile_20260525` 自动候选标签，当前仍是 `pending_manual_review`；它可以用于定位和排队人工复核，不能写成最终人工退化分层结论。")
    lines.append("- P6/P7 结构 proxy 不是 ODS/OIS/AP/AC 的替代，只用于解释边界连续性、伪边、断裂和定位误差方向。")
    lines.append("")
    lines.append("## 证据入口")
    lines.append("")
    for label, path in evidence_paths.items():
        root = PROJECT_ROOT if str(path).lower().startswith(str(PROJECT_ROOT).lower()) else path.anchor
        lines.append(f"- {label}: {evidence(path, PROJECT_ROOT)}")
    lines.append(f"- 聚合 CSV: `{rel(output_csv)}`")
    lines.append("")
    lines.append("## 1. 阶段与指标：旧 Stage1 增强在哪里伤害下游")
    lines.append("")
    lines.append("下表来自 Stage1 侧 `stage1_downstream_edge_metric_deltas_20260525.csv`，比较各阶段相对 Raw anchor 的 ODS/OIS/AP/AC delta。")
    lines.append("")
    lines.append("| Detector | Stage | status | lowered metrics | delta ODS | delta OIS | delta AP | delta AC |")
    lines.append("| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |")
    for row in stage_rows:
        lines.append(
            "| {detector} | {candidate} | {status} | {lowered_metric_count} | {delta_ods} | {delta_ois} | {delta_ap} | {delta_ac} |".format(
                detector=table_escape(row["detector"]),
                candidate=table_escape(row["candidate"]),
                status=table_escape(row["status"]),
                lowered_metric_count=row["lowered_metric_count"],
                delta_ods=fmt_float(row["delta_ods"]),
                delta_ois=fmt_float(row["delta_ois"]),
                delta_ap=fmt_float(row["delta_ap"]),
                delta_ac=fmt_float(row["delta_ac"]),
            )
        )
    lines.append("")
    lines.append("最明显的负向项：")
    lines.append("")
    for metric, row in worst_by_metric.items():
        lines.append(
            f"- `{metric.replace('delta_', '').upper()}` 最大下降：{row['detector']} / {row['candidate']}，delta `{fmt_float(row[metric])}`。"
        )
    lines.append("")
    lines.append("当前可写结论：旧 Stage1 的后半段增强，尤其 `RGHS -> CLAHE -> Fused -> Final`，在两个固定检测器下都显著拉低 ODS/OIS/AP/AC；`BPH` 和 `IMF1Ray` 损伤较小但也不是稳定正向。MSFI 侧 `IMF1Ray` 的 AP 例外不能抵消 ODS/OIS/AC 的下降。")
    lines.append("")
    lines.append("## 2. 自动退化标签下的结构 proxy 损伤")
    lines.append("")
    lines.append("下表按自动退化候选标签聚合 per-image 结构 proxy delta。`boundary_*` 为 candidate - raw，负值通常更差；`false_edge`、`missed_gt`、`components`、`endpoints`、`p95 distance` 为正值通常更差。多标签样本会计入多个标签，因此 count 是 multilabel count。")
    lines.append("")
    selected = [
        row
        for row in structure_rows
        if row["comparison"] in {"legacy_final_vs_raw_msfi", "legacy_final_vs_raw_baseline"}
        and row["tag"] != "all_auto_candidates"
    ]
    lines.append("| Comparison | Tag | n | delta F1 | delta precision | delta recall | delta false-edge | delta endpoints/kpx | delta p95 pred-GT dist |")
    lines.append("| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for row in selected:
        lines.append(
            "| {comparison} | {tag} | {n} | {df1} | {dp} | {dr} | {dfe} | {de} | {dd} |".format(
                comparison=table_escape(row["comparison"]),
                tag=table_escape(row["tag"]),
                n=row["image_count_multilabel"],
                df1=fmt_float(row["delta_boundary_f1_tol"]),
                dp=fmt_float(row["delta_boundary_precision_tol"]),
                dr=fmt_float(row["delta_boundary_recall_tol"]),
                dfe=fmt_float(row["delta_false_edge_ratio_tol"]),
                de=fmt_float(row["delta_endpoints_per_1k_skel_px"]),
                dd=fmt_float(row["delta_p95_pred_to_gt_distance"]),
            )
        )
    lines.append("")
    lines.append("当前可写结论：在自动候选标签下，legacy Stage1 Final 的损伤不是只发生在某一个孤立样本；低对比边界、模糊轮廓、背景伪边、细结构和重叠/杂质类候选中均出现 F1/precision 下降和 false-edge/endpoints 增加。该结论仍需人工冻结退化标签后才能升级为正式 per-stratum 结果。")
    lines.append("")
    lines.append("## 3. Top failure candidate 的标签集中情况")
    lines.append("")
    lines.append("下面只统计每类 top-20 failure/success candidate 的自动标签，帮助决定人工复核优先级。")
    lines.append("")
    lines.append("| Category | rows | mean delta F1 | mean delta precision | mean delta false-edge | top tags | top stems |")
    lines.append("| --- | ---: | ---: | ---: | ---: | --- | --- |")
    for category, summary in sorted(failure_summary.items()):
        tag_counts = Counter(summary["tag_counts"])
        top_tags = ", ".join(f"{tag}:{count}" for tag, count in tag_counts.most_common(4))
        top_stems = ", ".join(summary["top_stems"])
        lines.append(
            "| {category} | {rows} | {df1} | {dp} | {dfe} | {tags} | {stems} |".format(
                category=table_escape(category),
                rows=summary["row_count"],
                df1=fmt_float(summary["mean_delta_f1"]),
                dp=fmt_float(summary["mean_delta_precision"]),
                dfe=fmt_float(summary["mean_delta_false_edge"]),
                tags=table_escape(top_tags),
                stems=table_escape(top_stems),
            )
        )
    lines.append("")
    lines.append("## 4. 对下一版 Stage1 boundary-aware 实现的约束")
    lines.append("")
    lines.append("基于当前只读诊断，下一版 Stage1 不能再追求通用增强强度，而应把 hard guardrail 改成下游边界结构：")
    lines.append("")
    lines.append("- 不再以 `Final` 的强对比、强梯度、强无参考视觉指标作为优先目标。")
    lines.append("- 优先保留 Raw 的边界分布，只允许 mild luminance adjustment 和受控 chroma transfer。")
    lines.append("- 对低对比/模糊边界样本，目标是提升 recall 但不能牺牲 precision 到产生大量伪边。")
    lines.append("- 对背景伪边/细结构样本，目标是降低 false-edge 和 endpoint fragmentation，而不是简单增强高频。")
    lines.append("- 成功门槛不能是“接近 Raw”，而应至少在 fixed MSFI 与 DiffusionEdge baseline 中同时出现 ODS/OIS/AC 或结构 proxy 的稳定正向信号；P9 仍需 sampling/eval/show 后才能判断。")
    lines.append("")
    lines.append("## 5. 仍缺")
    lines.append("")
    lines.append("- 人工冻结退化标签；当前标签只是自动 proxy。")
    lines.append("- P8 repeat/control 与 P9 `edge_safe_gamma_bph_v1` 的 fixed-detector sampling/eval/show 和结果同步。")
    lines.append("- 真正连续 PR 曲线、阈值校准、MSFI 组件消融/替换、效率和人工确认的失败案例图组。")
    lines.append("- 在 P9 或后续候选没有稳定超过 Raw 前，不进入 2770 full-pool。")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    myedge_root = Path(args.myedge_root)
    output_md = Path(args.output_md)
    output_json = Path(args.output_json)
    output_csv = Path(args.output_csv)

    stage_delta_csv = PROJECT_ROOT / "docs" / "stage1_downstream_edge_metric_deltas_20260525.csv"
    degradation_csv = myedge_root / "docs" / "paper_assets" / "stage1_coupling" / "degradation_subset_candidates_20260525.csv"
    failure_csv = myedge_root / "docs" / "paper_assets" / "stage1_coupling" / "degradation_subset_candidates_20260525.failure_cases.csv"
    p6_per_image_csv = myedge_root / "docs" / "paper_assets" / "stage1_coupling" / "downstream_variant_structure_p6_metrics_20260525.per_image.csv"
    p7_per_image_csv = myedge_root / "docs" / "paper_assets" / "stage1_coupling" / "generic_control_p7_structure_metrics_20260525.per_image.csv"

    stage_delta_rows = read_csv(stage_delta_csv)
    degradation_rows = read_csv(degradation_csv)
    failure_rows = read_csv(failure_csv)
    p6_rows = read_csv(p6_per_image_csv)
    p7_rows = read_csv(p7_per_image_csv)

    tag_index = build_tag_index(degradation_rows)
    stage_rows = stage_metric_rows(stage_delta_rows)
    worst_by_metric = worst_stage_by_metric(stage_rows)
    structure_rows = aggregate_structure_deltas(p6_rows, p7_rows, tag_index)
    failure_summary = count_failure_tags(failure_rows)

    csv_fieldnames = [
        "comparison",
        "detector",
        "candidate",
        "tag",
        "image_count_multilabel",
    ] + [f"delta_{metric}" for metric in METRIC_COLUMNS] + [f"direction_{metric}" for metric in METRIC_COLUMNS]

    csv_rows = []
    for row in structure_rows:
        item = dict(row)
        for metric in METRIC_COLUMNS:
            item[f"direction_{metric}"] = metric_direction_note(metric)
        csv_rows.append(item)
    write_csv(output_csv, csv_rows, csv_fieldnames)

    evidence_paths = {
        "Stage1 stage/metric delta": stage_delta_csv,
        "MyEdge degradation candidates": degradation_csv,
        "MyEdge failure candidates": failure_csv,
        "P6 per-image structure proxy": p6_per_image_csv,
        "P7 per-image structure proxy": p7_per_image_csv,
    }

    payload = {
        "generated_date": datetime.now().date().isoformat(),
        "status": "readonly_harm_degradation_diagnostic_ready_auto_proxy_not_manual_strata",
        "no_stage1_enhancement_run": True,
        "no_myedge_sampling_eval_show_training": True,
        "stage_metric_rows": stage_rows,
        "worst_stage_by_metric": worst_by_metric,
        "structure_proxy_degradation_delta_rows": structure_rows,
        "failure_candidate_tag_summary": failure_summary,
        "outputs": {
            "md": rel(output_md),
            "json": rel(output_json),
            "csv": rel(output_csv),
        },
        "boundary": [
            "Degradation tags are automatic proxy candidates pending manual review.",
            "Structure proxy deltas are diagnostic only and do not replace ODS/OIS/AP/AC.",
            "No P8/P9 sampling, WSL eval.py, WSL show.py, training, or metric recomputation is executed by this script.",
        ],
    }

    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(
        make_markdown(output_csv, stage_rows, worst_by_metric, structure_rows, failure_summary, evidence_paths),
        encoding="utf-8",
    )
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(
        json.dumps(
            {
                "status": payload["status"],
                "stage_metric_rows": len(stage_rows),
                "structure_proxy_rows": len(structure_rows),
                "failure_categories": len(failure_summary),
                "output_md": str(output_md),
                "output_json": str(output_json),
                "output_csv": str(output_csv),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
