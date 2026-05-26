from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Sequence


THIS_DIR = Path(__file__).resolve().parent
METRICS_DIR = THIS_DIR.parent
PROJECT_ROOT = METRICS_DIR.parent
DEFAULT_MYEDGE_ROOT = Path(r"D:\Desktop\MyEdgeCodex")
DEFAULT_DATE = datetime.now().date().strftime("%Y%m%d")
DEFAULT_OUTPUT_MD = PROJECT_ROOT / "docs" / f"stage1_myedge_evidence_gap_dashboard_{DEFAULT_DATE}_cn.md"
DEFAULT_OUTPUT_JSON = PROJECT_ROOT / "docs" / f"stage1_myedge_evidence_gap_dashboard_{DEFAULT_DATE}_cn.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build a read-only cross-project evidence gap dashboard for Stage1Codex and MyEdgeCodex. "
            "This script does not run enhancement, training, sampling, eval.py, or metric recomputation."
        )
    )
    parser.add_argument("--myedge-root", default=str(DEFAULT_MYEDGE_ROOT))
    parser.add_argument("--output-md", default=str(DEFAULT_OUTPUT_MD))
    parser.add_argument("--output-json", default=str(DEFAULT_OUTPUT_JSON))
    return parser.parse_args()


def read_json(path: Path) -> Dict[str, object]:
    if not path.exists():
        return {"_missing": True, "_path": str(path)}
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def rel(path: Path, root: Path = PROJECT_ROOT) -> str:
    try:
        return str(path.relative_to(root)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def exists_rel(path: Path, root: Path = PROJECT_ROOT) -> str:
    return f"`{rel(path, root)}`" if path.exists() else f"`{rel(path, root)}` (missing)"


def row(
    item_id: str,
    workstream: str,
    requirement: str,
    status: str,
    priority: str,
    evidence: str,
    next_action: str,
    boundary: str,
) -> Dict[str, str]:
    return {
        "item_id": item_id,
        "workstream": workstream,
        "requirement": requirement,
        "status": status,
        "priority": priority,
        "evidence": evidence,
        "next_action": next_action,
        "boundary": boundary,
    }


def find_experiment(rows: Sequence[Dict[str, str]], experiment_id: str) -> Dict[str, str]:
    for item in rows:
        if item.get("id") == experiment_id:
            return item
    return {}


def status_from_contract(contract_path: Path, result_rows: Sequence[Dict[str, str]], keyword: str) -> str:
    has_result = any(keyword.lower() in row.get("id", "").lower() for row in result_rows)
    if has_result:
        return "result_present_check_required"
    if contract_path.exists():
        return "planned_only"
    return "missing_contract"


def preflight_ready(report: Dict[str, object]) -> bool:
    if report.get("_missing"):
        return False
    variants = report.get("variant_reports") or []
    return int(report.get("row_count") or 0) == 168 and bool(variants) and all(
        bool(item.get("ready")) for item in variants if isinstance(item, dict)
    )


def build_dashboard(myedge_root: Path) -> Dict[str, object]:
    stage1_paths = {
        "locked_config": PROJECT_ROOT / "experiments" / "optimization_v1" / "configs" / "locked_full506_final_mainline.json",
        "locked_result": PROJECT_ROOT
        / "experiments"
        / "h2-full506-direct"
        / "outputs"
        / "full506"
        / "runs"
        / "full506_final_mainline",
        "stage_proxy_summary": PROJECT_ROOT
        / "metrics"
        / "outputs"
        / "downstream_edge_validation"
        / "official_full502_mainline"
        / "stage_full502_proxy"
        / "summary.json",
        "compare_proxy_summary": PROJECT_ROOT
        / "metrics"
        / "outputs"
        / "downstream_edge_validation"
        / "official_full502_mainline"
        / "compare9_complete496_proxy"
        / "summary.json",
        "inventory_doc": PROJECT_ROOT / "docs" / "full_enhancement_dataset_inventory_cn.md",
        "candidate_manifest": PROJECT_ROOT / "metrics" / "manifests" / "full_algae_dewatermark_v1.txt",
        "cv2_manifest": PROJECT_ROOT / "metrics" / "manifests" / "full_algae_dewatermark_v1_cv2_readable_candidate.txt",
        "manual_validation": PROJECT_ROOT
        / "metrics"
        / "manifests"
        / "full_algae_dewatermark_v1_manual_review"
        / "manual_review_validation_status_20260525.json",
        "manual_derived": PROJECT_ROOT
        / "metrics"
        / "manifests"
        / "full_algae_dewatermark_v1_manual_review"
        / "derived_review_artifacts"
        / "review_artifacts_status_20260525.json",
        "decision_template": PROJECT_ROOT
        / "metrics"
        / "manifests"
        / "full_algae_dewatermark_v1_manual_review"
        / "manual_review_decision_template.tsv",
        "clean_manifest": PROJECT_ROOT
        / "metrics"
        / "manifests"
        / "full_algae_dewatermark_v1_manual_review"
        / "derived_review_artifacts"
        / "reviewed_cv2_clean_manifest.txt",
        "full2770_intake": PROJECT_ROOT
        / "experiments"
        / "full-algae-dewatermark-v1"
        / "outputs"
        / "cv2readable2770"
        / "runs"
        / "full2770_locked_final_mainline_intake_status_20260525.json",
        "full2770_output": PROJECT_ROOT
        / "experiments"
        / "full-algae-dewatermark-v1"
        / "outputs"
        / "cv2readable2770"
        / "runs"
        / "full2770_locked_final_mainline",
        "long_plan": PROJECT_ROOT / "docs" / "stage1_myedge_long_term_closure_plan_cn.md",
        "coupling_snapshot": PROJECT_ROOT / "docs" / "stage1_myedge_coupling_status_20260525_cn.json",
    }
    myedge_paths = {
        "experiment_status_csv": myedge_root / "docs" / "paper_assets" / "experiment_status.csv",
        "paper_ready_results": myedge_root / "docs" / "paper_assets" / "paper_ready_results.md",
        "readiness_checklist": myedge_root / "docs" / "paper_assets" / "paper_submission_readiness_checklist_zh.md",
        "figure1": myedge_root / "docs" / "paper_assets" / "figures" / "figure1_overview.png",
        "figure2": myedge_root / "docs" / "paper_assets" / "figures" / "figure2_msfi_module.png",
        "component_ablation_contract": myedge_root
        / "docs"
        / "research_contracts"
        / "msfi_component_ablation_v1.md",
        "replacement_contract": myedge_root / "docs" / "research_contracts" / "msfi_replacement_module_v1.md",
        "degradation_contract": myedge_root
        / "docs"
        / "research_contracts"
        / "degradation_stratified_edge_analysis_v1.md",
        "efficiency_failure_contract": myedge_root
        / "docs"
        / "research_contracts"
        / "paper_efficiency_pr_failure_analysis_v1.md",
        "stage1_downstream_contract": myedge_root
        / "docs"
        / "research_contracts"
        / "stage1_downstream_edge_validation_v1.md",
        "stage1_p1_msfi_output": myedge_root
        / "output_test"
        / "stage1_coupling"
        / "msfi_50k"
        / "stage1_final_168_p1_20260524",
        "stage1_p1_baseline_output": myedge_root
        / "output_test"
        / "stage1_coupling"
        / "diffusionedge_baseline_50k"
        / "stage1_final_168_p1_20260525",
        "stagewise_baseline_results": myedge_root
        / "docs"
        / "paper_assets"
        / "stage1_coupling"
        / "stagewise_baseline_p2_results_20260525.json",
        "stagewise_msfi_results": myedge_root
        / "docs"
        / "paper_assets"
        / "stage1_coupling"
        / "stagewise_msfi_p3_results_20260525.json",
        "downstream_variant_p4_results": myedge_root
        / "docs"
        / "paper_assets"
        / "stage1_coupling"
        / "downstream_variant_p4_results_20260525.json",
        "downstream_variant_baseline_p5c_results": myedge_root
        / "docs"
        / "paper_assets"
        / "stage1_coupling"
        / "downstream_variant_baseline_p5c_results_20260525.json",
        "downstream_variant_structure_p6_results": myedge_root
        / "docs"
        / "paper_assets"
        / "stage1_coupling"
        / "downstream_variant_structure_p6_metrics_20260525.json",
        "downstream_variant_structure_p6_paired_review": myedge_root
        / "docs"
        / "paper_assets"
        / "stage1_coupling"
        / "downstream_variant_structure_p6_paired_review_20260525.json",
        "generic_control_p7_msfi_preflight": myedge_root
        / "docs"
        / "paper_assets"
        / "stage1_coupling"
        / "generic_control_p7_msfi_preflight_20260525.json",
        "generic_control_p7_baseline_preflight": myedge_root
        / "docs"
        / "paper_assets"
        / "stage1_coupling"
        / "generic_control_p7_baseline_preflight_20260525.json",
        "generic_control_p7_msfi_results": myedge_root
        / "docs"
        / "paper_assets"
        / "stage1_coupling"
        / "generic_control_p7_msfi_results_20260525.json",
        "generic_control_p7_baseline_results": myedge_root
        / "docs"
        / "paper_assets"
        / "stage1_coupling"
        / "generic_control_p7_baseline_results_20260525.json",
        "generic_control_p7_structure_metrics": myedge_root
        / "docs"
        / "paper_assets"
        / "stage1_coupling"
        / "generic_control_p7_structure_metrics_20260525.json",
        "generic_control_p7_structure_paired_review": myedge_root
        / "docs"
        / "paper_assets"
        / "stage1_coupling"
        / "generic_control_p7_structure_paired_review_20260525.json",
    }

    manual_validation = read_json(stage1_paths["manual_validation"])
    manual_derived = read_json(stage1_paths["manual_derived"])
    full2770_intake = read_json(stage1_paths["full2770_intake"])
    coupling = read_json(stage1_paths["coupling_snapshot"])
    experiment_rows = read_csv(myedge_paths["experiment_status_csv"])

    formal_msfi = find_experiment(experiment_rows, "myedge_msfi_ema_slide_50k_mat")
    baseline_diffusion = find_experiment(experiment_rows, "baseline_diffusionedge_50k_mat")
    p1_intake = coupling.get("p1_results_intake", {}) if isinstance(coupling, dict) else {}
    p1_status = str(p1_intake.get("overall_status", "unknown"))
    p1_runs = {str(run.get("run_id")): run for run in p1_intake.get("runs", [])}
    p1_msfi = p1_runs.get("stage1_final_to_msfi_50k", {})
    p1_baseline = p1_runs.get("stage1_final_to_diffusionedge_baseline_50k", {})
    stagewise_baseline = read_json(myedge_paths["stagewise_baseline_results"])
    stagewise_runs = stagewise_baseline.get("runs", []) if isinstance(stagewise_baseline, dict) else []
    stagewise_status = str(stagewise_baseline.get("overall_status", "missing"))
    stagewise_metric_text = "; ".join(
        (
            f"{run.get('stage')} ODS/OIS/AP/AC="
            f"{(run.get('mat_eval') or {}).get('ods')}/"
            f"{(run.get('mat_eval') or {}).get('ois')}/"
            f"{(run.get('mat_eval') or {}).get('ap')}/"
            f"{run.get('ac')}"
        )
        for run in stagewise_runs
        if run.get("stage") in {"Raw", "BPH", "IMF1Ray", "RGHS", "CLAHE", "Fused", "Final"}
    )
    stagewise_msfi = read_json(myedge_paths["stagewise_msfi_results"])
    stagewise_msfi_runs = stagewise_msfi.get("runs", []) if isinstance(stagewise_msfi, dict) else []
    stagewise_msfi_status = str(stagewise_msfi.get("overall_status", "missing"))
    stagewise_msfi_metric_text = "; ".join(
        (
            f"{run.get('stage')} ODS/OIS/AP/AC="
            f"{(run.get('mat_eval') or {}).get('ods')}/"
            f"{(run.get('mat_eval') or {}).get('ois')}/"
            f"{(run.get('mat_eval') or {}).get('ap')}/"
            f"{run.get('ac')}"
        )
        for run in stagewise_msfi_runs
        if run.get("stage") in {"Raw", "BPH", "IMF1Ray", "RGHS", "CLAHE", "Fused", "Final"}
    )
    downstream_variant_p4 = read_json(myedge_paths["downstream_variant_p4_results"])
    downstream_variant_p4_runs = downstream_variant_p4.get("runs", []) if isinstance(downstream_variant_p4, dict) else []
    downstream_variant_p4_status = str(downstream_variant_p4.get("overall_status", "missing"))
    downstream_variant_p4_metric_text = "; ".join(
        (
            f"{run.get('label')} ODS/OIS/AP/AC="
            f"{(run.get('mat_eval') or {}).get('ods')}/"
            f"{(run.get('mat_eval') or {}).get('ois')}/"
            f"{(run.get('mat_eval') or {}).get('ap')}/"
            f"{run.get('ac')}"
        )
        for run in downstream_variant_p4_runs
        if run.get("label")
        in {
            "historical_raw_msfi_anchor",
            "edge_preserve_original_control",
            "edge_preserve_raw_bph_mild_v1",
            "edge_preserve_raw_bph_moderate_v1",
            "legacy_stage1_final_p1",
        }
    )
    downstream_variant_baseline_p5c = read_json(myedge_paths["downstream_variant_baseline_p5c_results"])
    downstream_variant_baseline_p5c_runs = downstream_variant_baseline_p5c.get("runs", []) if isinstance(downstream_variant_baseline_p5c, dict) else []
    downstream_variant_baseline_p5c_status = str(downstream_variant_baseline_p5c.get("overall_status", "missing"))
    downstream_variant_baseline_p5c_metric_text = "; ".join(
        (
            f"{run.get('label')} ODS/OIS/AP/AC="
            f"{(run.get('mat_eval') or {}).get('ods')}/"
            f"{(run.get('mat_eval') or {}).get('ois')}/"
            f"{(run.get('mat_eval') or {}).get('ap')}/"
            f"{run.get('ac')}"
        )
        for run in downstream_variant_baseline_p5c_runs
        if run.get("label")
        in {
            "historical_raw_diffusionedge_anchor",
            "edge_preserve_original_control",
            "edge_preserve_raw_bph_mild_v1",
            "edge_preserve_raw_bph_moderate_v1",
            "legacy_stage1_final_p1",
        }
    )
    downstream_variant_structure_p6 = read_json(myedge_paths["downstream_variant_structure_p6_results"])
    downstream_variant_structure_p6_status = str(downstream_variant_structure_p6.get("status", "missing"))
    downstream_variant_structure_p6_paired = read_json(myedge_paths["downstream_variant_structure_p6_paired_review"])
    downstream_variant_structure_p6_paired_status = str(downstream_variant_structure_p6_paired.get("status", "missing"))
    generic_control_p7_msfi = read_json(myedge_paths["generic_control_p7_msfi_preflight"])
    generic_control_p7_baseline = read_json(myedge_paths["generic_control_p7_baseline_preflight"])
    generic_control_p7_msfi_results = read_json(myedge_paths["generic_control_p7_msfi_results"])
    generic_control_p7_baseline_results = read_json(myedge_paths["generic_control_p7_baseline_results"])
    generic_control_p7_msfi_results_status = str(generic_control_p7_msfi_results.get("overall_status", "missing"))
    generic_control_p7_baseline_results_status = str(generic_control_p7_baseline_results.get("overall_status", "missing"))
    generic_control_p7_structure = read_json(myedge_paths["generic_control_p7_structure_metrics"])
    generic_control_p7_structure_status = str(generic_control_p7_structure.get("status", "missing"))
    generic_control_p7_structure_paired = read_json(myedge_paths["generic_control_p7_structure_paired_review"])
    generic_control_p7_structure_paired_status = str(generic_control_p7_structure_paired.get("status", "missing"))
    generic_control_p7_msfi_runs = generic_control_p7_msfi_results.get("runs", []) if isinstance(generic_control_p7_msfi_results, dict) else []
    generic_control_p7_baseline_runs = generic_control_p7_baseline_results.get("runs", []) if isinstance(generic_control_p7_baseline_results, dict) else []
    generic_control_p7_result_complete = (
        generic_control_p7_msfi_results_status == "complete_with_report_assets"
        and generic_control_p7_baseline_results_status == "complete_with_report_assets"
    )
    generic_control_p7_metric_text = "; ".join(
        (
            f"MSFI/{run.get('label')} ODS/OIS/AP/AC="
            f"{(run.get('mat_eval') or {}).get('ods')}/"
            f"{(run.get('mat_eval') or {}).get('ois')}/"
            f"{(run.get('mat_eval') or {}).get('ap')}/"
            f"{run.get('ac')}"
        )
        for run in generic_control_p7_msfi_runs
        if run.get("label")
        in {
            "historical_raw_msfi_anchor",
            "generic_luma_clahe_mild_v1",
            "generic_luma_gamma_mild_v1",
            "legacy_stage1_final_p1",
        }
    )
    generic_control_p7_metric_text += "; " + "; ".join(
        (
            f"Baseline/{run.get('label')} ODS/OIS/AP/AC="
            f"{(run.get('mat_eval') or {}).get('ods')}/"
            f"{(run.get('mat_eval') or {}).get('ois')}/"
            f"{(run.get('mat_eval') or {}).get('ap')}/"
            f"{run.get('ac')}"
        )
        for run in generic_control_p7_baseline_runs
        if run.get("label")
        in {
            "historical_raw_diffusionedge_anchor",
            "generic_luma_clahe_mild_v1",
            "generic_luma_gamma_mild_v1",
            "legacy_stage1_final_p1",
        }
    )
    generic_control_p7_metric_text = generic_control_p7_metric_text.strip("; ")
    generic_control_p7_status = (
        "complete_with_report_assets"
        if generic_control_p7_result_complete
        else (
            "ready_for_sampling_not_evaluated"
            if preflight_ready(generic_control_p7_msfi) and preflight_ready(generic_control_p7_baseline)
            else "missing_or_incomplete_preflight"
        )
    )
    generic_control_p7_evidence = (
        f"{exists_rel(myedge_paths['generic_control_p7_msfi_preflight'], myedge_root)}; "
        f"{exists_rel(myedge_paths['generic_control_p7_baseline_preflight'], myedge_root)}; "
        f"{exists_rel(myedge_paths['generic_control_p7_msfi_results'], myedge_root)}; "
        f"{exists_rel(myedge_paths['generic_control_p7_baseline_results'], myedge_root)}; "
        f"{exists_rel(myedge_paths['generic_control_p7_structure_metrics'], myedge_root)}; "
        f"{exists_rel(myedge_paths['generic_control_p7_structure_paired_review'], myedge_root)}; "
        f"msfi_results={generic_control_p7_msfi_results_status}; "
        f"baseline_results={generic_control_p7_baseline_results_status}; "
        f"structure={generic_control_p7_structure_status}; "
        f"paired={generic_control_p7_structure_paired_status}; "
        f"{generic_control_p7_metric_text}"
    )
    p6_summary_rows = downstream_variant_structure_p6.get("summary", []) if isinstance(downstream_variant_structure_p6, dict) else []
    p6_key_rows = {
        (row.get("detector_group"), row.get("label")): row
        for row in p6_summary_rows
        if isinstance(row, dict)
        and (row.get("detector_group"), row.get("label"))
        in {
            ("msfi_p4", "historical_raw_msfi_anchor"),
            ("msfi_p4", "edge_preserve_raw_bph_moderate_v1"),
            ("msfi_p4", "legacy_stage1_final_p1"),
            ("diffusionedge_baseline_p5c", "historical_raw_diffusionedge_anchor"),
            ("diffusionedge_baseline_p5c", "edge_preserve_raw_bph_mild_v1"),
            ("diffusionedge_baseline_p5c", "legacy_stage1_final_p1"),
        }
    }
    downstream_variant_structure_p6_metric_text = "; ".join(
        (
            f"{detector}/{label} F1/precision/recall/false-edge/components/endpoints="
            f"{row.get('mean_boundary_f1_tol'):.4f}/"
            f"{row.get('mean_boundary_precision_tol'):.4f}/"
            f"{row.get('mean_boundary_recall_tol'):.4f}/"
            f"{row.get('mean_false_edge_ratio_tol'):.4f}/"
            f"{row.get('mean_pred_components_per_1k_edge_px'):.4f}/"
            f"{row.get('mean_endpoints_per_1k_skel_px'):.4f}"
        )
        for (detector, label), row in p6_key_rows.items()
    )
    formal_mat_rows = [
        item
        for item in experiment_rows
        if item.get("id", "").endswith("_mat") and item.get("status") in {"formal_main_result", "formal_comparison_completed", "formal_comparison_user_confirmed_unified_evidence_synced", "completed_local_eval", "completed_unified_local_eval", "completed_local_wsl_reeval_unified_evidence_synced"}
    ]

    rows: List[Dict[str, str]] = []
    rows.append(
        row(
            "S1-01",
            "Stage1 formal protocol",
            "锁定正式增强主线配置与正式结果目录",
            "complete" if stage1_paths["locked_config"].exists() and stage1_paths["locked_result"].exists() else "missing",
            "P0",
            f"{exists_rel(stage1_paths['locked_config'])}; {exists_rel(stage1_paths['locked_result'])}",
            "保持 502/496 正式论文口径，不用 full2770 替代当前主表。",
            "正式主线必须显式使用 locked_full506_final_mainline.json；不能写成直接 python main.py。",
        )
    )
    rows.append(
        row(
            "S1-02",
            "Stage1 formal protocol",
            "full502_clean_v1 与 compare9_complete496_v1 的无 GT 结构代理支撑包",
            "complete" if stage1_paths["stage_proxy_summary"].exists() and stage1_paths["compare_proxy_summary"].exists() else "missing",
            "P1",
            f"{exists_rel(stage1_paths['stage_proxy_summary'])}; {exists_rel(stage1_paths['compare_proxy_summary'])}",
            "用作结构保持与选图支撑；带 GT 的 ODS/OIS/AP/AC 必须回到 MyEdge。",
            "无 GT proxy 不是下游边缘检测正式结果。",
        )
    )
    rows.append(
        row(
            "S1-03",
            "Stage1 full-pool dataset",
            "2777 图像池 manifest、decode、duplicate、quality audit",
            "complete" if stage1_paths["inventory_doc"].exists() and stage1_paths["candidate_manifest"].exists() and stage1_paths["cv2_manifest"].exists() else "missing",
            "P0",
            f"{exists_rel(stage1_paths['inventory_doc'])}; {exists_rel(stage1_paths['candidate_manifest'])}; {exists_rel(stage1_paths['cv2_manifest'])}",
            "继续人工复核 544 条 issue；把 2777 图像池与参考论文数据子集关系写清。",
            "2777 是增强候选池，不等同于 MyEdge 当前 168 张 GT test，也不自动等同于参考论文公开写法。",
        )
    )
    rows.append(
        row(
            "S1-04",
            "Stage1 full-pool dataset",
            "人工复核决策、clean manifest、split leakage guard",
            "pending_manual_review" if manual_validation.get("pending_rows", 0) else "complete_validated",
            "P0",
            (
                f"{exists_rel(stage1_paths['manual_validation'])}; pending={manual_validation.get('pending_rows')}; "
                f"invalid={manual_validation.get('invalid_rows')}; template={exists_rel(stage1_paths['decision_template'])}"
            ),
            "先由人填写 manual_review_decision_template.tsv，再 dry-run apply；无 invalid 后才允许 --apply。",
            "machine_suggestion 不是 reviewer_decision；不能据此生成 clean manifest。",
        )
    )
    rows.append(
        row(
            "S1-05",
            "Stage1 full-pool dataset",
            "reviewed clean manifest",
            "missing_blocked_by_manual_review"
            if not stage1_paths["clean_manifest"].exists() and not manual_derived.get("can_generate_clean_manifest")
            else "complete",
            "P0",
            f"{exists_rel(stage1_paths['clean_manifest'])}; can_generate={manual_derived.get('can_generate_clean_manifest')}",
            "等人工复核完成后运行 derive_fullpool_review_artifacts.py。",
            "没有 clean manifest 前，不应用 reviewed pool 做正式长跑入口。",
        )
    )
    rows.append(
        row(
            "S1-06",
            "Stage1 full-pool enhancement",
            "2770 OpenCV-readable full run",
            str(full2770_intake.get("status", "unknown")),
            "P1",
            (
                f"{exists_rel(stage1_paths['full2770_intake'])}; output_exists={stage1_paths['full2770_output'].exists()}; "
                f"present={full2770_intake.get('present_output_files')}/{full2770_intake.get('expected_output_files')}"
            ),
            "人工复核优先；若授权长跑，再用 run_full_cv2readable2770_locked.ps1 并通过 intake 接收。",
            "full2770 只作为 coverage evidence；完成前不能写成已有结果。",
        )
    )

    rows.append(
        row(
            "ME-01",
            "MyEdge main result",
            "MSFI + EMA + slide/non-resize + 50k 正式主结果",
            "complete" if formal_msfi else "missing",
            "P0",
            (
                f"{exists_rel(myedge_paths['experiment_status_csv'], myedge_root)}; "
                f"ODS={formal_msfi.get('ods')}; OIS={formal_msfi.get('ois')}; AP={formal_msfi.get('ap')}; AC={formal_msfi.get('ac')}"
            ),
            "论文中写 mixed metric profile：ODS/OIS 高于 DiffusionEdge baseline，AP 低于 baseline，AC 基本持平。",
            "不能写全面优于、SOTA 或所有指标最优。",
        )
    )
    rows.append(
        row(
            "ME-02",
            "MyEdge comparison",
            "DiffusionEdge baseline 50k 与正式对比方法主表",
            "complete" if baseline_diffusion and len(formal_mat_rows) >= 9 else "partial_check_required",
            "P0",
            f"formal/comparison mat rows={len(formal_mat_rows)}; baseline_diffusionedge_50k_mat status={baseline_diffusion.get('status')}",
            "继续按 MyEdge claim-to-evidence 和 readiness checklist 控制表述。",
            "不同 baseline 训练协议不完全相同；不能把 nominal exposure 写成 identical training。",
        )
    )
    rows.append(
        row(
            "ME-03",
            "Stage1 -> MyEdge coupling",
            "168 张 Stage1 coupling manifest 与 P1 preflight",
            "ready_not_started"
            if coupling.get("overall_status") == "p1_not_started"
            else str(coupling.get("overall_status", "unknown")),
            "P0",
            (
                f"{exists_rel(stage1_paths['coupling_snapshot'])}; rows={coupling.get('manifest', {}).get('rows')}; "
                f"GT missing={coupling.get('manifest', {}).get('gt_missing_count')}; P1 status={p1_status}"
            ),
            "若 P1 已完成，则只在 168 张 / Stage1 Final / fixed detector 边界内解释；下一步补 stage-wise 与 generic enhancement controls。",
            "P1 完成不等于 Stage1 全阶段、full502/full2770 或所有退化场景的下游收益。",
        )
    )
    rows.append(
        row(
            "ME-04",
            "Stage1 -> MyEdge coupling",
            "P1 fixed-detector Stage1 Final 下游评测结果",
            p1_status
            if p1_status == "complete_with_report_assets"
            else (
                "not_started"
                if not myedge_paths["stage1_p1_msfi_output"].exists() and not myedge_paths["stage1_p1_baseline_output"].exists()
                else "output_present_intake_required"
            ),
            "P0",
            (
                f"{exists_rel(myedge_paths['stage1_p1_msfi_output'], myedge_root)}; "
                f"MSFI mat={p1_msfi.get('mat_eval')}; AC={p1_msfi.get('ac_from_show')}; "
                f"{exists_rel(myedge_paths['stage1_p1_baseline_output'], myedge_root)}; "
                f"Baseline mat={p1_baseline.get('mat_eval')}; AC={p1_baseline.get('ac_from_show')}"
            ),
            "当前 P1 结果应写成 Stage1 Final fixed-detector 诊断：绝对指标低于 raw-anchor 正式结果，不能写 Stage1 已带来下游增益。",
            "P1 是第一轮诊断结果；还不能替代 stage-wise、generic controls、退化子集和形态一致性证据。",
        )
    )
    rows.append(
        row(
            "ME-04B",
            "Stage1 -> MyEdge coupling",
            "DiffusionEdge baseline 固定检测器 Stage1 各阶段诊断矩阵",
            stagewise_status,
            "P0",
            f"{exists_rel(myedge_paths['stagewise_baseline_results'], myedge_root)}; {stagewise_metric_text}",
            "当前 baseline stage-wise 结果显示各 Stage1 阶段均低于 Raw anchor；下一步补 generic enhancement controls 与 MSFI stage-wise，定位是否为增强分布迁移或 detector-specific 问题。",
            "该矩阵只覆盖 DiffusionEdge baseline；不能外推到 MSFI，也不能写 Stage1 正向下游收益。",
        )
    )
    rows.append(
        row(
            "ME-04C",
            "Stage1 -> MyEdge coupling",
            "MSFI 固定检测器 Stage1 各阶段诊断矩阵",
            stagewise_msfi_status,
            "P0",
            f"{exists_rel(myedge_paths['stagewise_msfi_results'], myedge_root)}; {stagewise_msfi_metric_text}",
            "当前 MSFI stage-wise 结果同样显示各 Stage1 阶段整体低于 Raw anchor；下一步应停止把旧 Stage1 写成正向下游收益，并转向 downstream-driven enhancement variant 设计和 generic controls。",
            "该矩阵只覆盖 MSFI 50k 固定检测器和 168 张 MyEdge test split；不能外推到 full502/full2770，也不能写成 Stage1 正向下游收益。",
        )
    )
    rows.append(
        row(
            "ME-04D",
            "Stage1 -> MyEdge coupling",
            "MSFI 固定检测器 downstream-driven edge-preserve Stage1 P4 变体诊断矩阵",
            downstream_variant_p4_status,
            "P0",
            f"{exists_rel(myedge_paths['downstream_variant_p4_results'], myedge_root)}; {downstream_variant_p4_metric_text}",
            "当前 P4 结果显示 edge-preserve 变体已基本消除旧 Stage1 Final 的大幅下游损伤；后续应补 repeat/control 与 generic enhancement controls，再判断是否有稳定正向收益。",
            "该矩阵只覆盖 168 张 MyEdge test split 和固定 MSFI 50k；edge_preserve_raw_bph_moderate_v1 只能写成接近 Raw / 同轮 original-control 下 AP/OIS 有改善的候选，不能写成稳定优于 raw 或 full502/full2770 已提升。",
        )
    )
    rows.append(
        row(
            "ME-04E",
            "Stage1 -> MyEdge coupling",
            "DiffusionEdge baseline 固定检测器 downstream-driven edge-preserve Stage1 P5C 二次检测器诊断矩阵",
            downstream_variant_baseline_p5c_status,
            "P0",
            f"{exists_rel(myedge_paths['downstream_variant_baseline_p5c_results'], myedge_root)}; {downstream_variant_baseline_p5c_metric_text}",
            "当前 P5C 结果显示 edge-preserve 变体在 DiffusionEdge baseline 下也基本消除旧 Stage1 Final 的下游损伤；后续应补 repeat/control、generic enhancement controls 和结构/伪边指标，再判断是否有稳定正向收益。",
            "该矩阵只覆盖 168 张 MyEdge test split 和固定 DiffusionEdge baseline 50k；mild 的 AP/OIS 正向信号不能单独写成稳定 Stage1 下游收益，AC 仍低于 raw。",
        )
    )
    rows.append(
        row(
            "ME-04F",
            "Stage1 -> MyEdge coupling",
            "P4/P5C 现有 MAT 输出的结构、断裂与伪边 proxy 诊断 P6",
            downstream_variant_structure_p6_status,
            "P0",
            (
                f"{exists_rel(myedge_paths['downstream_variant_structure_p6_results'], myedge_root)}; "
                f"paired={exists_rel(myedge_paths['downstream_variant_structure_p6_paired_review'], myedge_root)}; "
                f"{downstream_variant_structure_p6_metric_text}"
            ),
            "当前 P6/P6B 可用于解释旧 Final 的伪边与碎裂问题，并说明 P4/MSFI moderate 的伪边、碎裂与逐图配对候选信号；下一步仍需 generic enhancement controls 和 repeat/control。",
            "P6 只读取已有 P4/P5C MAT 与 GT，按各 run ODS threshold 二值化，tolerance=2px；它是结构诊断 proxy，不替代 ODS/OIS/AP/AC，也不能外推到 full502/full2770。",
        )
    )
    rows.append(
        row(
            "ME-04G",
            "Stage1 -> MyEdge coupling",
            "Generic luminance-only controls P7 诊断：CLAHE/gamma 两个非 BPH 轻量对照已完成固定 MSFI 与 DiffusionEdge baseline 评测",
            generic_control_p7_status,
            "P0",
            generic_control_p7_evidence,
            "当前 P7 结果应写成 generic luminance-only 轻量对照诊断：baseline/gamma 有 ODS/OIS/AP 小幅正向信号，MSFI/gamma 基本贴近 raw；P7 结构 proxy 与 paired review 已补，显示 MSFI/gamma 在 F1、precision、false-edge、碎裂和 endpoints 上有轻微信号，但 baseline/gamma 仍 mixed。下一步补 repeat/control，再判断是否进入更大口径。",
            "P7 只覆盖 168 张 MyEdge split 和两个轻量 luminance controls；尚不能写 Stage1 稳定提升下游，也不能替代 P4/P5C repeat 或 full502/full2770 证据。",
        )
    )
    rows.append(
        row(
            "ME-05",
            "MyEdge ablation",
            "MSFI component ablation",
            status_from_contract(myedge_paths["component_ablation_contract"], experiment_rows, "ablation"),
            "P1",
            exists_rel(myedge_paths["component_ablation_contract"], myedge_root),
            "完成 frequency token、spatial-frequency interaction、timestep gating、full MSFI 的组件级对比。",
            "合同存在不等于实验完成；未完成前不能写 gating/频带 token 独立有效。",
        )
    )
    rows.append(
        row(
            "ME-06",
            "MyEdge ablation",
            "Sobel/CIAFF-like/Fourier/CBAM/SE/ECA/ASPP/FPN 替换模块对比",
            status_from_contract(myedge_paths["replacement_contract"], experiment_rows, "replacement"),
            "P1",
            exists_rel(myedge_paths["replacement_contract"], myedge_root),
            "直接回应同方向 ESWA 参考论文的 Sobel/CIAFF 重合风险。",
            "替换对比未完成前，只能说这是待补证据。",
        )
    )
    rows.append(
        row(
            "ME-07",
            "MyEdge robustness",
            "低对比、弱边界、气泡/杂质、模糊边界等退化子集分析",
            status_from_contract(myedge_paths["degradation_contract"], experiment_rows, "degradation"),
            "P1",
            exists_rel(myedge_paths["degradation_contract"], myedge_root),
            "先用 Stage1 full-pool manual review 的子集标签沉淀候选，再在 MyEdge 侧形成带 GT 子集评测。",
            "没有人工标签或子集协议时，不能泛化宣称复杂退化鲁棒。",
        )
    )
    rows.append(
        row(
            "ME-08",
            "MyEdge paper assets",
            "效率、PR/AP trade-off、失败案例与投稿级 qualitative",
            status_from_contract(myedge_paths["efficiency_failure_contract"], experiment_rows, "efficiency"),
            "P1",
            exists_rel(myedge_paths["efficiency_failure_contract"], myedge_root),
            "补 Params/FLOPs/FPS/显存、PR curve、TP/FP/FN overlay、failure cases。",
            "没有效率实验前不能写更轻量、更快或部署优势。",
        )
    )
    rows.append(
        row(
            "ME-09",
            "MyEdge paper assets",
            "Figure 1/2 和 paper-ready result assets",
            "partial_complete"
            if myedge_paths["figure1"].exists() and myedge_paths["figure2"].exists() and myedge_paths["paper_ready_results"].exists()
            else "partial_or_missing",
            "P2",
            f"{exists_rel(myedge_paths['figure1'], myedge_root)}; {exists_rel(myedge_paths['figure2'], myedge_root)}; {exists_rel(myedge_paths['paper_ready_results'], myedge_root)}",
            "继续补 Figure 3 qualitative、PR/失败案例、Stage1 coupling 图组。",
            "Figure 1/2 是方法图资产，不是新增实验结论。",
        )
    )

    status_counts = Counter(item["status"] for item in rows)
    priority_counts = Counter(item["priority"] for item in rows)
    dashboard = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "stage1_root": str(PROJECT_ROOT),
        "myedge_root": str(myedge_root),
        "no_experiment_executed": True,
        "source_files": {
            "stage1_manual_validation": rel(stage1_paths["manual_validation"]),
            "stage1_manual_derived": rel(stage1_paths["manual_derived"]),
            "stage1_full2770_intake": rel(stage1_paths["full2770_intake"]),
            "stage1_coupling_snapshot": rel(stage1_paths["coupling_snapshot"]),
            "myedge_experiment_status": rel(myedge_paths["experiment_status_csv"], myedge_root),
            "myedge_paper_ready_results": rel(myedge_paths["paper_ready_results"], myedge_root),
        },
        "summary": {
            "overall_status": "major_evidence_gaps_remain",
            "status_counts": dict(sorted(status_counts.items())),
            "priority_counts": dict(sorted(priority_counts.items())),
            "stage1_manual_pending_rows": manual_validation.get("pending_rows"),
            "stage1_clean_manifest_exists": stage1_paths["clean_manifest"].exists(),
            "stage1_full2770_status": full2770_intake.get("status"),
            "myedge_formal_msfi_ods": formal_msfi.get("ods"),
            "myedge_formal_msfi_ois": formal_msfi.get("ois"),
            "myedge_formal_msfi_ap": formal_msfi.get("ap"),
            "myedge_formal_msfi_ac": formal_msfi.get("ac"),
            "myedge_p1_status": coupling.get("p1_results_intake", {}).get("overall_status"),
            "myedge_stagewise_baseline_status": stagewise_status,
            "myedge_stagewise_msfi_status": stagewise_msfi_status,
            "myedge_downstream_variant_p4_status": downstream_variant_p4_status,
            "myedge_downstream_variant_baseline_p5c_status": downstream_variant_baseline_p5c_status,
            "myedge_downstream_variant_structure_p6_status": downstream_variant_structure_p6_status,
            "myedge_downstream_variant_structure_p6_paired_status": downstream_variant_structure_p6_paired_status,
            "myedge_generic_control_p7_status": generic_control_p7_status,
        },
        "rows": rows,
        "boundary": (
            "This dashboard reads existing local Stage1Codex and MyEdgeCodex files only. "
            "It does not run Stage1 enhancement, MyEdge sampling, eval.py, show.py, training, or metric recomputation. "
            "Planned contracts and machine suggestions are not completed evidence."
        ),
    }
    return dashboard


def write_markdown(path: Path, dashboard: Dict[str, object]) -> None:
    summary = dashboard["summary"]
    rows: Sequence[Dict[str, str]] = dashboard["rows"]
    lines: List[str] = [
        "# Stage1Codex + MyEdgeCodex evidence gap dashboard",
        "",
        f"日期：{datetime.now().date().isoformat()}",
        "",
        "本文是跨项目投稿证据缺口 dashboard，只读取本地 Stage1Codex 与 MyEdgeCodex 已有文件，不运行增强、训练、采样、评测或指标重算。",
        "",
        "## Executive Summary",
        "",
        f"- Overall status: `{summary['overall_status']}`",
        f"- Stage1 full-pool manual review pending rows: `{summary['stage1_manual_pending_rows']}`",
        f"- Stage1 reviewed clean manifest exists: `{summary['stage1_clean_manifest_exists']}`",
        f"- Stage1 full2770 run status: `{summary['stage1_full2770_status']}`",
        f"- MyEdge formal MSFI 50k: ODS `{summary['myedge_formal_msfi_ods']}`, OIS `{summary['myedge_formal_msfi_ois']}`, AP `{summary['myedge_formal_msfi_ap']}`, AC `{summary['myedge_formal_msfi_ac']}`",
        f"- MyEdge Stage1 coupling P1 status: `{summary['myedge_p1_status']}`",
        f"- MyEdge Stage1 baseline stage-wise status: `{summary['myedge_stagewise_baseline_status']}`",
        f"- MyEdge Stage1 MSFI stage-wise status: `{summary['myedge_stagewise_msfi_status']}`",
        f"- MyEdge downstream-driven Stage1 P4 status: `{summary['myedge_downstream_variant_p4_status']}`",
        f"- MyEdge downstream-driven Stage1 baseline P5C status: `{summary['myedge_downstream_variant_baseline_p5c_status']}`",
        f"- MyEdge downstream-driven Stage1 structure P6 status: `{summary['myedge_downstream_variant_structure_p6_status']}`",
        f"- MyEdge downstream-driven Stage1 structure P6 paired review status: `{summary['myedge_downstream_variant_structure_p6_paired_status']}`",
        f"- MyEdge generic enhancement controls P7 status: `{summary['myedge_generic_control_p7_status']}`",
        "",
        "## Status Counts",
        "",
        "| Status | Count |",
        "|---|---:|",
    ]
    for status, count in summary["status_counts"].items():
        lines.append(f"| `{status}` | {count} |")
    lines.extend(
        [
            "",
            "## Evidence Gap Matrix",
            "",
            "| ID | Workstream | Requirement | Status | Priority | Evidence | Next action | Boundary |",
            "|---|---|---|---|---|---|---|---|",
        ]
    )
    for item in rows:
        lines.append(
            "| {item_id} | {workstream} | {requirement} | `{status}` | `{priority}` | {evidence} | {next_action} | {boundary} |".format(
                **item
            )
        )
    lines.extend(
        [
            "",
            "## Recommended Long-Cycle Order",
            "",
            "1. 完成人工复核：先 P0，再 P1，再 P2；只有人工决策完成后才派生 clean manifest 和 split leakage guard。",
            "2. 已完成 MyEdge P1 fixed-detector coupling、DiffusionEdge baseline stage-wise、MSFI stage-wise 和 downstream-driven P4 诊断；当前旧 Stage1 增强不支持正向下游收益，P4 edge-preserve 变体只支持 edge-safe / 接近 raw 的候选结论。",
            "3. P6 结构 proxy、P6B paired review、P7 结构 proxy 与 P7 paired review 均已完成；generic controls P7 已完成固定 MSFI 与 DiffusionEdge baseline 评测。当前 P7 显示轻量 generic gamma 在 baseline 侧有小幅 ODS/OIS/AP 信号、MSFI 侧基本贴近 raw，结构 proxy 上 MSFI/gamma 有轻微信号但 baseline/gamma 仍 mixed；仍需 repeat/control，不进入 full2770。",
            "4. 再补 MyEdge 核心证据：MSFI 组件消融、替换模块、退化子集、PR/AP trade-off、效率和失败案例。",
            "5. 最后再决定 Stage1 full2770 长跑是否启动；full2770 作为 coverage evidence，不替代当前 502/496 正式主表。",
            "",
            "## Writing Boundary",
            "",
            "- 主论文定位应以 MyEdge/MSFI 的 spatial-frequency weak-boundary diffusion 为主；Stage1 是 task-driven structure-preserving input formation。",
            "- 当前不能把 Stage1 下游收益写成已完成 GT-based ODS/OIS/AP/AC 结论。",
            "- 当前不能写 MSFI 全面领先；必须保留 AP 低于 DiffusionEdge baseline 的 trade-off。",
            "- 合同文件、机助建议和 dashboard 都不是实验结果，只是后续工作入口。",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    dashboard = build_dashboard(Path(args.myedge_root))
    output_json = Path(args.output_json)
    output_md = Path(args.output_md)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(dashboard, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(output_md, dashboard)
    print(json.dumps(dashboard["summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
