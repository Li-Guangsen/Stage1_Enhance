from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Sequence


THIS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = THIS_DIR.parent.parent
DEFAULT_MYEDGE_ROOT = Path(r"D:\Desktop\MyEdgeCodex")
DEFAULT_DATE = datetime.now().date().strftime("%Y%m%d")
DEFAULT_OUTPUT_MD = PROJECT_ROOT / "docs" / f"stage1_downstream_edge_negative_diagnostic_{DEFAULT_DATE}_cn.md"
DEFAULT_OUTPUT_JSON = PROJECT_ROOT / "docs" / f"stage1_downstream_edge_negative_diagnostic_{DEFAULT_DATE}_cn.json"
DEFAULT_OUTPUT_CSV = PROJECT_ROOT / "docs" / f"stage1_downstream_edge_metric_deltas_{DEFAULT_DATE}.csv"

METRICS = ("ods", "ois", "ap", "ac")
DISPLAY = {"ods": "ODS", "ois": "OIS", "ap": "AP", "ac": "AC"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build a read-only diagnostic summary for existing Stage1 -> MyEdge fixed-detector results. "
            "This script does not run Stage1 enhancement, MyEdge sampling, WSL eval.py/show.py, training, "
            "or metric recomputation."
        )
    )
    parser.add_argument("--myedge-root", default=str(DEFAULT_MYEDGE_ROOT))
    parser.add_argument("--output-md", default=str(DEFAULT_OUTPUT_MD))
    parser.add_argument("--output-json", default=str(DEFAULT_OUTPUT_JSON))
    parser.add_argument("--output-csv", default=str(DEFAULT_OUTPUT_CSV))
    return parser.parse_args()


def read_json(path: Path) -> Dict[str, object]:
    if not path.exists():
        return {"_missing": True, "_path": str(path)}
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path, root: Path = PROJECT_ROOT) -> str:
    try:
        return str(path.relative_to(root)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def evidence(path: Path, root: Path = PROJECT_ROOT) -> str:
    suffix = "" if path.exists() else " (missing)"
    return f"`{rel(path, root)}`{suffix}"


def metric_value(run: Dict[str, object], metric: str) -> float | None:
    if metric == "ac":
        value = run.get("ac")
    else:
        mat_eval = run.get("mat_eval") or {}
        value = mat_eval.get(metric) if isinstance(mat_eval, dict) else None
    if value is None:
        return None
    return float(value)


def run_name(run: Dict[str, object]) -> str:
    return str(run.get("stage") or run.get("label") or run.get("run_id") or "")


def find_run(runs: Sequence[Dict[str, object]], name: str) -> Dict[str, object]:
    for run in runs:
        if run_name(run) == name:
            return run
    return {}


def metric_profile(run: Dict[str, object]) -> Dict[str, float | None]:
    return {metric: metric_value(run, metric) for metric in METRICS}


def classify_delta(delta: float | None, eps: float = 1e-9) -> str:
    if delta is None:
        return "missing"
    if delta > eps:
        return "positive"
    if delta < -eps:
        return "negative"
    return "tie"


def classify_row(deltas: Dict[str, float | None]) -> str:
    counts = Counter(classify_delta(value) for value in deltas.values())
    if counts["missing"]:
        return "incomplete"
    if counts["negative"] == len(METRICS):
        return "all_metrics_lower"
    if counts["positive"] == len(METRICS):
        return "all_metrics_higher"
    if counts["negative"] >= 3:
        return "mostly_lower"
    if counts["positive"] >= 3:
        return "mostly_higher"
    return "mixed"


def is_near_raw(deltas: Dict[str, float | None]) -> bool:
    """Loose diagnostic gate for small 168-image deltas, not a paper claim."""
    limits = {"ods": 0.0025, "ois": 0.0030, "ap": 0.0100, "ac": 0.0040}
    for metric, limit in limits.items():
        value = deltas.get(metric)
        if value is None or value < -limit:
            return False
    return True


def comparison_rows(
    group: str,
    detector: str,
    comparison_kind: str,
    base_run: Dict[str, object],
    candidate_runs: Iterable[Dict[str, object]],
) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    base_profile = metric_profile(base_run)
    for run in candidate_runs:
        profile = metric_profile(run)
        deltas = {
            metric: None if profile[metric] is None or base_profile[metric] is None else profile[metric] - base_profile[metric]
            for metric in METRICS
        }
        status = classify_row(deltas)
        if comparison_kind in {"variant_vs_historical_raw", "variant_vs_same_round_original"} and is_near_raw(deltas):
            status = "near_raw_edge_safe_candidate"
        rows.append(
            {
                "group": group,
                "detector": detector,
                "comparison_kind": comparison_kind,
                "baseline": run_name(base_run),
                "candidate": run_name(run),
                "candidate_type": str(run.get("variant_type") or ""),
                "status": status,
                **{f"{metric}": profile[metric] for metric in METRICS},
                **{f"delta_{metric}": deltas[metric] for metric in METRICS},
            }
        )
    return rows


def build_report(myedge_root: Path) -> Dict[str, object]:
    coupling_root = myedge_root / "docs" / "paper_assets" / "stage1_coupling"
    paths = {
        "stagewise_baseline_json": coupling_root / "stagewise_baseline_p2_results_20260525.json",
        "stagewise_baseline_md": coupling_root / "stagewise_baseline_p2_results_20260525.md",
        "stagewise_msfi_json": coupling_root / "stagewise_msfi_p3_results_20260525.json",
        "stagewise_msfi_md": coupling_root / "stagewise_msfi_p3_results_20260525.md",
        "p4_json": coupling_root / "downstream_variant_p4_results_20260525.json",
        "p4_md": coupling_root / "downstream_variant_p4_results_20260525.md",
        "p5c_json": coupling_root / "downstream_variant_baseline_p5c_results_20260525.json",
        "p5c_md": coupling_root / "downstream_variant_baseline_p5c_results_20260525.md",
        "p6b_md": coupling_root / "downstream_variant_structure_p6_paired_review_20260525.md",
        "p7_msfi_json": coupling_root / "generic_control_p7_msfi_results_20260525.json",
        "p7_msfi_md": coupling_root / "generic_control_p7_msfi_results_20260525.md",
        "p7_baseline_json": coupling_root / "generic_control_p7_baseline_results_20260525.json",
        "p7_baseline_md": coupling_root / "generic_control_p7_baseline_results_20260525.md",
        "p7_paired_md": coupling_root / "generic_control_p7_structure_paired_review_20260525.md",
        "p8_json": coupling_root / "stage1_repeat_control_p8_results_20260525.json",
        "p8_md": coupling_root / "stage1_repeat_control_p8_results_20260525.md",
        "p8_gate_json": coupling_root / "stage1_repeat_control_p8_gate_20260525.json",
        "p8_gate_md": coupling_root / "stage1_repeat_control_p8_gate_20260525.md",
    }
    data = {key: read_json(path) for key, path in paths.items() if path.suffix == ".json"}

    stage_rows: List[Dict[str, object]] = []
    for key, detector in (
        ("stagewise_baseline_json", "DiffusionEdge baseline 50k"),
        ("stagewise_msfi_json", "MSFI 50k"),
    ):
        runs = data[key].get("runs") or []
        if not isinstance(runs, list) or not runs:
            continue
        raw = find_run(runs, "Raw")
        candidates = [run for run in runs if run_name(run) != "Raw"]
        stage_rows.extend(comparison_rows("stagewise", detector, "stage_vs_raw", raw, candidates))

    variant_rows: List[Dict[str, object]] = []
    variant_specs = (
        ("p4_json", "MSFI 50k", "P4 downstream-driven variants"),
        ("p5c_json", "DiffusionEdge baseline 50k", "P5C downstream-driven variants"),
        ("p7_msfi_json", "MSFI 50k", "P7 generic controls"),
        ("p7_baseline_json", "DiffusionEdge baseline 50k", "P7 generic controls"),
    )
    for key, detector, group in variant_specs:
        runs = data[key].get("runs") or []
        if not isinstance(runs, list) or not runs:
            continue
        historical = next((run for run in runs if "historical_raw" in run_name(run)), {})
        original = find_run(runs, "edge_preserve_original_control")
        candidates = [run for run in runs if run_name(run) != run_name(historical)]
        variant_rows.extend(comparison_rows(group, detector, "variant_vs_historical_raw", historical, candidates))
        if original:
            against_original = [run for run in runs if run_name(run) not in {run_name(historical), run_name(original)}]
            variant_rows.extend(
                comparison_rows(group, detector, "variant_vs_same_round_original", original, against_original)
            )

    p8 = data.get("p8_json", {})
    p8_gate = data.get("p8_gate_json", {})
    p8_status = str(p8.get("overall_status") or "missing")
    p8_gate_decision = str(p8_gate.get("decision") or "missing")
    status_counts = Counter(str(row.get("status")) for row in stage_rows + variant_rows)
    stage_status_counts = Counter(str(row.get("status")) for row in stage_rows)
    variant_status_counts = Counter(str(row.get("status")) for row in variant_rows)

    legacy_final_rows = [
        row
        for row in stage_rows + variant_rows
        if str(row.get("candidate")).lower() in {"final", "legacy_stage1_final_p1"}
        and row.get("comparison_kind") in {"stage_vs_raw", "variant_vs_historical_raw"}
    ]
    edge_safe_rows = [
        row
        for row in variant_rows
        if row.get("status") == "near_raw_edge_safe_candidate"
        and "legacy" not in str(row.get("candidate")).lower()
        and row.get("comparison_kind") == "variant_vs_historical_raw"
    ]

    answer = {
        "legacy_stage1_final_hurts_downstream": bool(legacy_final_rows)
        and all(row.get("status") in {"all_metrics_lower", "mostly_lower"} for row in legacy_final_rows),
        "stagewise_baseline_summary": (
            "DiffusionEdge baseline fixed-detector P2 shows every Stage1 stage has lower ODS/OIS/AP/AC than Raw."
        ),
        "stagewise_msfi_summary": (
            "MSFI fixed-detector P3 shows every Stage1 stage has lower ODS/OIS/AC than Raw; "
            "IMF1Ray is the only AP exception, but its ODS/OIS/AC still drop."
        ),
        "edge_safe_variant_summary": (
            "P4/P5C/P7 variants largely remove the legacy Final damage and P8 repeat/control supports "
            "repeat-stable near-raw rescue for main rows, but generic gamma controls are competitive and "
            "baseline-side structure remains mixed; therefore they are not stable Stage1-specific positive paper evidence."
        ),
    }

    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "myedge_root": str(myedge_root),
        "overall_status": "negative_diagnostic_locked_p8_completed_control_competitive",
        "answer": answer,
        "counts": {
            "stage_rows": len(stage_rows),
            "variant_rows": len(variant_rows),
            "status_counts": dict(status_counts),
            "stage_status_counts": dict(stage_status_counts),
            "variant_status_counts": dict(variant_status_counts),
            "legacy_final_rows": len(legacy_final_rows),
            "near_raw_edge_safe_candidate_rows": len(edge_safe_rows),
            "p8_status": p8_status,
            "p8_gate_decision": p8_gate_decision,
        },
        "stage_rows": stage_rows,
        "variant_rows": variant_rows,
        "source_paths": {key: str(path) for key, path in paths.items()},
        "source_paths_rel": {key: rel(path) for key, path in paths.items()},
        "evidence_markdown": {key: evidence(path) for key, path in paths.items()},
        "boundaries": [
            "This report reads existing MyEdge Stage1 coupling JSON/MD assets only.",
            "It does not run Stage1 enhancement, MyEdge sampling, WSL eval.py, WSL show.py, training, or metric recomputation.",
            "The 168-image MyEdge split has GT edge maps and is valid for diagnosis, but it is not the 2770 full-pool result.",
            "P8 repeat/control is complete as a 168-image fixed-detector diagnostic; it does not establish Stage1-specific positive downstream benefit because generic gamma controls are competitive and baseline-side structure remains mixed.",
            "Do not claim stable Stage1 downstream improvement until larger-scope evidence and manually frozen degradation/failure analysis are synchronized.",
        ],
    }


def fmt_num(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        return f"{value:.6f}"
    return str(value)


def row_table(rows: Sequence[Dict[str, object]], include_metrics: bool = True) -> List[str]:
    if include_metrics:
        header = [
            "Group",
            "Detector",
            "Comparison",
            "Baseline",
            "Candidate",
            "Status",
            "ODS",
            "ΔODS",
            "OIS",
            "ΔOIS",
            "AP",
            "ΔAP",
            "AC",
            "ΔAC",
        ]
    else:
        header = ["Group", "Detector", "Comparison", "Baseline", "Candidate", "Status"]
    lines = ["| " + " | ".join(header) + " |", "|" + "|".join(["---"] * len(header)) + "|"]
    for row in rows:
        values = [
            row.get("group"),
            row.get("detector"),
            row.get("comparison_kind"),
            row.get("baseline"),
            row.get("candidate"),
            row.get("status"),
        ]
        if include_metrics:
            values.extend(
                [
                    row.get("ods"),
                    row.get("delta_ods"),
                    row.get("ois"),
                    row.get("delta_ois"),
                    row.get("ap"),
                    row.get("delta_ap"),
                    row.get("ac"),
                    row.get("delta_ac"),
                ]
            )
        lines.append("| " + " | ".join(fmt_num(value) for value in values) + " |")
    return lines


def write_markdown(report: Dict[str, object], output_md: Path) -> None:
    counts = report["counts"]
    answer = report["answer"]
    evidence_map = report["evidence_markdown"]
    stage_rows = report["stage_rows"]
    variant_rows = report["variant_rows"]

    stage_bad = [
        row
        for row in stage_rows
        if row.get("candidate") in {"BPH", "IMF1Ray", "RGHS", "CLAHE", "Fused", "Final"}
    ]
    legacy_rows = [
        row
        for row in stage_rows + variant_rows
        if str(row.get("candidate")).lower() in {"final", "legacy_stage1_final_p1"}
        and row.get("comparison_kind") in {"stage_vs_raw", "variant_vs_historical_raw"}
    ]
    edge_safe_rows = [
        row
        for row in variant_rows
        if row.get("status") == "near_raw_edge_safe_candidate"
        and "legacy" not in str(row.get("candidate")).lower()
        and row.get("comparison_kind") == "variant_vs_historical_raw"
    ]

    lines: List[str] = [
        "# Stage1 -> MyEdge Downstream Edge Negative Diagnostic",
        "",
        f"Generated at: `{report['generated_at']}`",
        "",
        f"- Overall status: `{report['overall_status']}`",
        f"- Stage-wise delta rows: `{counts['stage_rows']}`",
        f"- Variant delta rows: `{counts['variant_rows']}`",
        f"- P8 repeat/control status: `{counts['p8_status']}`",
        "",
        "## Direct Answer",
        "",
        (
            "- 当前结论：旧 Stage1 增强，尤其 legacy `Final`，在 168 张 MyEdge 带 GT edge split 上"
            "确实导致下游边缘检测指标下降；该结论在固定 DiffusionEdge baseline 50k 和固定 MSFI 50k 两个检测器下都成立。"
        ),
        f"- P2：{answer['stagewise_baseline_summary']}",
        f"- P3：{answer['stagewise_msfi_summary']}",
        f"- P4/P5C/P7：{answer['edge_safe_variant_summary']}",
        "",
        "## Legacy Final Harm",
        "",
        *row_table(legacy_rows),
        "",
        "## Stage-wise Diagnosis",
        "",
        *row_table(stage_bad),
        "",
        "## Edge-safe Candidate Rows",
        "",
        *row_table(edge_safe_rows),
        "",
        "## Source Evidence",
        "",
        f"- Baseline stage-wise P2: {evidence_map['stagewise_baseline_md']}",
        f"- MSFI stage-wise P3: {evidence_map['stagewise_msfi_md']}",
        f"- MSFI downstream variants P4: {evidence_map['p4_md']}",
        f"- DiffusionEdge baseline variants P5C: {evidence_map['p5c_md']}",
        f"- P6B paired structure proxy: {evidence_map['p6b_md']}",
        f"- P7 MSFI generic controls: {evidence_map['p7_msfi_md']}",
        f"- P7 baseline generic controls: {evidence_map['p7_baseline_md']}",
        f"- P7 paired structure proxy: {evidence_map['p7_paired_md']}",
        f"- P8 repeat/control result intake: {evidence_map['p8_md']}",
        "",
        "## Interpretation Boundaries",
        "",
    ]
    lines.extend(f"- {item}" for item in report["boundaries"])
    lines.extend(
        [
            "",
            "## Next Gate",
            "",
            "- 不要重复跑 P1/P2/P3/P4/P5C/P6/P6B/P7 首轮。",
            "- 下一步要么先人工复核退化/失败案例候选，要么在明确高风险确认后执行 P8 repeat/control。",
            "- 成功前不要进入 2770 full-pool；当前 edge-safe 变体不能写成稳定优于 raw 的论文结论。",
            "",
        ]
    )
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text("\n".join(lines), encoding="utf-8")


def write_csv(report: Dict[str, object], output_csv: Path) -> None:
    rows = list(report["stage_rows"]) + list(report["variant_rows"])
    fieldnames = [
        "group",
        "detector",
        "comparison_kind",
        "baseline",
        "candidate",
        "candidate_type",
        "status",
        "ods",
        "delta_ods",
        "ois",
        "delta_ois",
        "ap",
        "delta_ap",
        "ac",
        "delta_ac",
    ]
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field) for field in fieldnames})


def main() -> None:
    args = parse_args()
    myedge_root = Path(args.myedge_root)
    output_md = Path(args.output_md)
    output_json = Path(args.output_json)
    output_csv = Path(args.output_csv)

    report = build_report(myedge_root)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    write_csv(report, output_csv)
    write_markdown(report, output_md)

    print(
        json.dumps(
            {
                "status": report["overall_status"],
                "stage_rows": report["counts"]["stage_rows"],
                "variant_rows": report["counts"]["variant_rows"],
                "legacy_stage1_final_hurts_downstream": report["answer"][
                    "legacy_stage1_final_hurts_downstream"
                ],
                "p8_status": report["counts"]["p8_status"],
                "output_md": str(output_md),
                "output_json": str(output_json),
                "output_csv": str(output_csv),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
