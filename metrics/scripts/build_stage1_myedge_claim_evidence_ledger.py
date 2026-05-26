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
DEFAULT_OUTPUT_MD = PROJECT_ROOT / "docs" / f"stage1_myedge_claim_evidence_ledger_{DEFAULT_DATE}_cn.md"
DEFAULT_OUTPUT_JSON = PROJECT_ROOT / "docs" / f"stage1_myedge_claim_evidence_ledger_{DEFAULT_DATE}_cn.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build a read-only paper claim-to-evidence ledger for Stage1Codex and MyEdgeCodex. "
            "This script does not run Stage1 enhancement, MyEdge sampling, eval.py, show.py, "
            "training, figure generation, or metric recomputation."
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


def evidence(path: Path, root: Path = PROJECT_ROOT) -> str:
    suffix = "" if path.exists() else " (missing)"
    return f"`{rel(path, root)}`{suffix}"


def table_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def manifest_count(path: Path) -> int:
    if not path.exists():
        return 0
    count = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        item = line.strip().lstrip("\ufeff")
        if item and not item.startswith("#"):
            count += 1
    return count


def find_experiment(rows: Sequence[Dict[str, str]], experiment_id: str) -> Dict[str, str]:
    for item in rows:
        if item.get("id") == experiment_id:
            return item
    return {}


def claim(
    claim_id: str,
    claim_scope: str,
    claim_text_cn: str,
    write_status: str,
    allowed_wording: str,
    current_evidence: str,
    missing_evidence: str,
    paper_boundary: str,
    next_gate: str,
    source_docs: Sequence[str],
) -> Dict[str, object]:
    return {
        "claim_id": claim_id,
        "claim_scope": claim_scope,
        "claim_text_cn": claim_text_cn,
        "write_status": write_status,
        "allowed_wording": allowed_wording,
        "current_evidence": current_evidence,
        "missing_evidence": missing_evidence,
        "paper_boundary": paper_boundary,
        "next_gate": next_gate,
        "source_docs": list(source_docs),
    }


def preflight_ready(report: Dict[str, object]) -> bool:
    if report.get("_missing"):
        return False
    variants = report.get("variant_reports") or []
    return int(report.get("row_count") or 0) == 168 and bool(variants) and all(
        bool(item.get("ready")) for item in variants if isinstance(item, dict)
    )


def build_ledger(myedge_root: Path) -> Dict[str, object]:
    stage1_paths = {
        "locked_config": PROJECT_ROOT / "experiments" / "optimization_v1" / "configs" / "locked_full506_final_mainline.json",
        "locked_result": PROJECT_ROOT
        / "experiments"
        / "h2-full506-direct"
        / "outputs"
        / "full506"
        / "runs"
        / "full506_final_mainline",
        "stage_manifest": PROJECT_ROOT / "metrics" / "manifests" / "full502_clean_v1.txt",
        "stage_summary": PROJECT_ROOT / "metrics" / "outputs" / "evaluate_protocol_v2" / "official_stage_progress_full502" / "summary.json",
        "stage_mean_table": PROJECT_ROOT / "metrics" / "outputs" / "evaluate_protocol_v2" / "official_stage_progress_full502" / "mean_metrics_table.md",
        "compare_manifest": PROJECT_ROOT / "metrics" / "manifests" / "compare9_complete496_v1.txt",
        "compare_summary": PROJECT_ROOT / "metrics" / "outputs" / "evaluate_protocol_v2" / "official_compare9_complete496" / "summary.json",
        "compare_mean_table": PROJECT_ROOT / "metrics" / "outputs" / "evaluate_protocol_v2" / "official_compare9_complete496" / "mean_metrics_table.md",
        "comparison_index": PROJECT_ROOT / "docs" / "comparison_methods_results_index_cn.md",
        "proxy_root": PROJECT_ROOT / "metrics" / "outputs" / "downstream_edge_validation" / "official_full502_mainline",
        "proxy_stage_summary": PROJECT_ROOT
        / "metrics"
        / "outputs"
        / "downstream_edge_validation"
        / "official_full502_mainline"
        / "stage_full502_proxy"
        / "summary.json",
        "proxy_compare_summary": PROJECT_ROOT
        / "metrics"
        / "outputs"
        / "downstream_edge_validation"
        / "official_full502_mainline"
        / "compare9_complete496_proxy"
        / "summary.json",
        "inventory": PROJECT_ROOT / "docs" / "full_enhancement_dataset_inventory_cn.md",
        "inventory_audit": PROJECT_ROOT / "metrics" / "manifests" / "full_algae_dewatermark_v1_audit.json",
        "full_manifest": PROJECT_ROOT / "metrics" / "manifests" / "full_algae_dewatermark_v1.txt",
        "cv2_manifest": PROJECT_ROOT / "metrics" / "manifests" / "full_algae_dewatermark_v1_cv2_readable_candidate.txt",
        "decode_summary": PROJECT_ROOT / "metrics" / "manifests" / "full_algae_dewatermark_v1_decode_audit.summary.json",
        "manual_validation": PROJECT_ROOT
        / "metrics"
        / "manifests"
        / "full_algae_dewatermark_v1_manual_review"
        / "manual_review_validation_status_20260525.json",
        "reviewed_clean_manifest": PROJECT_ROOT
        / "metrics"
        / "manifests"
        / "full_algae_dewatermark_v1_manual_review"
        / "derived_review_artifacts"
        / "reviewed_cv2_clean_manifest.txt",
        "full2770_readiness": PROJECT_ROOT / "docs" / "stage1_full2770_execution_readiness_20260525_cn.json",
        "p1_readiness": PROJECT_ROOT / "docs" / "stage1_myedge_p1_execution_readiness_20260525_cn.json",
        "gap_dashboard": PROJECT_ROOT / "docs" / "stage1_myedge_evidence_gap_dashboard_20260525_cn.json",
        "gate_board": PROJECT_ROOT / "docs" / "stage1_myedge_next_gate_board_20260525_cn.json",
        "coupling_status": PROJECT_ROOT / "docs" / "stage1_myedge_coupling_status_20260525_cn.json",
        "long_plan": PROJECT_ROOT / "docs" / "stage1_myedge_long_term_closure_plan_cn.md",
        "reference_dataset_relation_audit": PROJECT_ROOT / "docs" / "reference_dataset_relation_audit_20260525_cn.md",
        "evidence_pack": PROJECT_ROOT / "paper" / "underwater_image_enhancement_evidence_pack_cn.md",
        "draft": PROJECT_ROOT / "paper" / "underwater_image_enhancement_draft_cn.md",
        "eswa_note": PROJECT_ROOT / "literature" / "wu2026_eswa_hab_edge_detection.md",
        "eaai_note": PROJECT_ROOT / "literature" / "wu2026_eaai_hab_segmentation.md",
    }
    myedge_paths = {
        "experiment_status": myedge_root / "docs" / "paper_assets" / "experiment_status.csv",
        "paper_ready_results": myedge_root / "docs" / "paper_assets" / "paper_ready_results.md",
        "component_ablation_contract": myedge_root / "docs" / "research_contracts" / "msfi_component_ablation_v1.md",
        "replacement_contract": myedge_root / "docs" / "research_contracts" / "msfi_replacement_module_v1.md",
        "degradation_contract": myedge_root / "docs" / "research_contracts" / "degradation_stratified_edge_analysis_v1.md",
        "efficiency_failure_contract": myedge_root
        / "docs"
        / "research_contracts"
        / "paper_efficiency_pr_failure_analysis_v1.md",
        "p1_msfi_root": myedge_root / "output_test" / "stage1_coupling" / "msfi_50k" / "stage1_final_168_p1_20260524",
        "p1_baseline_root": myedge_root
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

    stage_summary = read_json(stage1_paths["stage_summary"])
    compare_summary = read_json(stage1_paths["compare_summary"])
    full2770_readiness = read_json(stage1_paths["full2770_readiness"])
    p1_readiness = read_json(stage1_paths["p1_readiness"])
    gap_dashboard = read_json(stage1_paths["gap_dashboard"])
    manual_validation = read_json(stage1_paths["manual_validation"])
    decode_summary = read_json(stage1_paths["decode_summary"])
    inventory_audit = read_json(stage1_paths["inventory_audit"])
    experiment_rows = read_csv(myedge_paths["experiment_status"])
    formal_msfi = find_experiment(experiment_rows, "myedge_msfi_ema_slide_50k_mat")
    baseline_diffusion = find_experiment(experiment_rows, "baseline_diffusionedge_50k_mat")

    full_image_count = int(inventory_audit.get("image_files_total") or manifest_count(stage1_paths["full_manifest"]))
    candidate_count = int(inventory_audit.get("candidate_manifest_count") or manifest_count(stage1_paths["full_manifest"]))
    cv2_count = manifest_count(stage1_paths["cv2_manifest"])
    stage_count = int(stage_summary.get("complete_success_count") or manifest_count(stage1_paths["stage_manifest"]))
    compare_count = int(compare_summary.get("complete_success_count") or manifest_count(stage1_paths["compare_manifest"]))
    compare_methods = sorted((compare_summary.get("methods") or {}).keys())
    decode_candidate = decode_summary.get("candidate_images", {}) if isinstance(decode_summary, dict) else {}
    manual_pending = manual_validation.get("pending_rows")
    p1_status = p1_readiness.get("overall_status")
    full2770_status = full2770_readiness.get("overall_status")
    coupling_status = read_json(stage1_paths["coupling_status"])
    p1_intake = coupling_status.get("p1_results_intake", {}) if isinstance(coupling_status, dict) else {}
    p1_intake_status = p1_intake.get("overall_status")
    p1_runs = {str(run.get("run_id")): run for run in p1_intake.get("runs", [])}
    p1_msfi = p1_runs.get("stage1_final_to_msfi_50k", {})
    p1_baseline = p1_runs.get("stage1_final_to_diffusionedge_baseline_50k", {})
    p1_msfi_mat = p1_msfi.get("mat_eval") or {}
    p1_baseline_mat = p1_baseline.get("mat_eval") or {}
    stagewise_baseline = read_json(myedge_paths["stagewise_baseline_results"])
    stagewise_status = stagewise_baseline.get("overall_status")
    stagewise_runs = stagewise_baseline.get("runs", []) if isinstance(stagewise_baseline, dict) else []
    stagewise_metrics = "; ".join(
        (
            f"{run.get('stage')} ODS/OIS/AP/AC "
            f"{(run.get('mat_eval') or {}).get('ods')}/"
            f"{(run.get('mat_eval') or {}).get('ois')}/"
            f"{(run.get('mat_eval') or {}).get('ap')}/"
            f"{run.get('ac')}"
        )
        for run in stagewise_runs
        if run.get("stage") in {"Raw", "BPH", "IMF1Ray", "RGHS", "CLAHE", "Fused", "Final"}
    )
    stagewise_msfi = read_json(myedge_paths["stagewise_msfi_results"])
    stagewise_msfi_status = stagewise_msfi.get("overall_status")
    stagewise_msfi_runs = stagewise_msfi.get("runs", []) if isinstance(stagewise_msfi, dict) else []
    stagewise_msfi_metrics = "; ".join(
        (
            f"{run.get('stage')} ODS/OIS/AP/AC "
            f"{(run.get('mat_eval') or {}).get('ods')}/"
            f"{(run.get('mat_eval') or {}).get('ois')}/"
            f"{(run.get('mat_eval') or {}).get('ap')}/"
            f"{run.get('ac')}"
        )
        for run in stagewise_msfi_runs
        if run.get("stage") in {"Raw", "BPH", "IMF1Ray", "RGHS", "CLAHE", "Fused", "Final"}
    )
    downstream_variant_p4 = read_json(myedge_paths["downstream_variant_p4_results"])
    downstream_variant_p4_status = downstream_variant_p4.get("overall_status")
    downstream_variant_p4_runs = downstream_variant_p4.get("runs", []) if isinstance(downstream_variant_p4, dict) else []
    downstream_variant_p4_metrics = "; ".join(
        (
            f"{run.get('label')} ODS/OIS/AP/AC "
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
    downstream_variant_baseline_p5c_status = downstream_variant_baseline_p5c.get("overall_status")
    downstream_variant_baseline_p5c_runs = downstream_variant_baseline_p5c.get("runs", []) if isinstance(downstream_variant_baseline_p5c, dict) else []
    downstream_variant_baseline_p5c_metrics = "; ".join(
        (
            f"{run.get('label')} ODS/OIS/AP/AC "
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
    downstream_variant_structure_p6_status = downstream_variant_structure_p6.get("status")
    downstream_variant_structure_p6_paired = read_json(myedge_paths["downstream_variant_structure_p6_paired_review"])
    downstream_variant_structure_p6_paired_status = downstream_variant_structure_p6_paired.get("status")
    generic_control_p7_msfi = read_json(myedge_paths["generic_control_p7_msfi_preflight"])
    generic_control_p7_baseline = read_json(myedge_paths["generic_control_p7_baseline_preflight"])
    generic_control_p7_msfi_results = read_json(myedge_paths["generic_control_p7_msfi_results"])
    generic_control_p7_baseline_results = read_json(myedge_paths["generic_control_p7_baseline_results"])
    generic_control_p7_msfi_results_status = generic_control_p7_msfi_results.get("overall_status")
    generic_control_p7_baseline_results_status = generic_control_p7_baseline_results.get("overall_status")
    generic_control_p7_structure = read_json(myedge_paths["generic_control_p7_structure_metrics"])
    generic_control_p7_structure_status = generic_control_p7_structure.get("status")
    generic_control_p7_structure_paired = read_json(myedge_paths["generic_control_p7_structure_paired_review"])
    generic_control_p7_structure_paired_status = generic_control_p7_structure_paired.get("status")
    generic_control_p7_msfi_runs = generic_control_p7_msfi_results.get("runs", []) if isinstance(generic_control_p7_msfi_results, dict) else []
    generic_control_p7_baseline_runs = generic_control_p7_baseline_results.get("runs", []) if isinstance(generic_control_p7_baseline_results, dict) else []
    generic_control_p7_result_complete = (
        generic_control_p7_msfi_results_status == "complete_with_report_assets"
        and generic_control_p7_baseline_results_status == "complete_with_report_assets"
    )
    generic_control_p7_metrics = "; ".join(
        (
            f"MSFI/{run.get('label')} ODS/OIS/AP/AC "
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
    generic_control_p7_metrics += "; " + "; ".join(
        (
            f"Baseline/{run.get('label')} ODS/OIS/AP/AC "
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
    generic_control_p7_metrics = generic_control_p7_metrics.strip("; ")
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
        f"{evidence(myedge_paths['generic_control_p7_msfi_preflight'], myedge_root)}; "
        f"{evidence(myedge_paths['generic_control_p7_baseline_preflight'], myedge_root)}; "
        f"{evidence(myedge_paths['generic_control_p7_msfi_results'], myedge_root)}; "
        f"{evidence(myedge_paths['generic_control_p7_baseline_results'], myedge_root)}; "
        f"{evidence(myedge_paths['generic_control_p7_structure_metrics'], myedge_root)}; "
        f"{evidence(myedge_paths['generic_control_p7_structure_paired_review'], myedge_root)}; "
        f"msfi_results={generic_control_p7_msfi_results_status}; "
        f"baseline_results={generic_control_p7_baseline_results_status}; "
        f"structure={generic_control_p7_structure_status}; paired={generic_control_p7_structure_paired_status}; "
        f"{generic_control_p7_metrics}"
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
    downstream_variant_structure_p6_metrics = "; ".join(
        (
            f"{detector}/{label} F1/precision/recall/false-edge/components/endpoints "
            f"{row.get('mean_boundary_f1_tol'):.4f}/"
            f"{row.get('mean_boundary_precision_tol'):.4f}/"
            f"{row.get('mean_boundary_recall_tol'):.4f}/"
            f"{row.get('mean_false_edge_ratio_tol'):.4f}/"
            f"{row.get('mean_pred_components_per_1k_edge_px'):.4f}/"
            f"{row.get('mean_endpoints_per_1k_skel_px'):.4f}"
        )
        for (detector, label), row in p6_key_rows.items()
    )

    claims: List[Dict[str, object]] = [
        claim(
            "C01",
            "Stage1 formal mainline",
            "Stage1 当前正式主线配置和正式结果目录已经锁定。",
            "allowed_fact",
            "可以写：正式主线显式使用 `locked_full506_final_mainline.json`，正式结果副本位于 `full506_final_mainline`。",
            f"{evidence(stage1_paths['locked_config'])}; {evidence(stage1_paths['locked_result'])}",
            "无。",
            "不能把默认 `python main.py` 写成正式论文主线；任何正式重跑都必须显式传锁定配置。",
            "保持只读；除非另立协议，不替换正式 502/496 口径。",
            [rel(stage1_paths["locked_config"]), rel(stage1_paths["locked_result"]), rel(stage1_paths["long_plan"])],
        ),
        claim(
            "C02",
            "Stage1 formal stage table",
            "`full502_clean_v1` 阶段进度表已经完成。",
            "allowed_fact",
            f"可以写：阶段表基于 `full502_clean_v1`，complete cases 为 `{stage_count}` 张。",
            f"{evidence(stage1_paths['stage_manifest'])}; {evidence(stage1_paths['stage_summary'])}; {evidence(stage1_paths['stage_mean_table'])}",
            "无。",
            "这是 Stage1 六阶段增强指标表，不是外部方法主表，也不是带 GT 边缘检测结果。",
            "用于中文主稿和证据包的正式阶段表。",
            [rel(stage1_paths["stage_manifest"]), rel(stage1_paths["stage_summary"]), rel(stage1_paths["stage_mean_table"])],
        ),
        claim(
            "C03",
            "Stage1 formal comparison table",
            "`compare9_complete496_v1` 九方法 complete-case 主表已经完成。",
            "allowed_fact",
            f"可以写：外部主比较基于 `{compare_count}` 张 complete-case，方法数 `{len(compare_methods)}`。",
            f"{evidence(stage1_paths['compare_manifest'])}; {evidence(stage1_paths['compare_summary'])}; {evidence(stage1_paths['compare_mean_table'])}",
            "无。",
            "`WWPF` 官方实现稳定输出 496 张，主表使用 complete-case；不能用各方法各自样本数均值混比。",
            "用于正式外部主比较；保留全部 9 方法。",
            [rel(stage1_paths["compare_manifest"]), rel(stage1_paths["compare_summary"]), rel(stage1_paths["comparison_index"])],
        ),
        claim(
            "C04",
            "Stage1 historical full506",
            "`full506` 只表示历史搜索与主线锁定背景。",
            "allowed_with_boundary",
            "可以写：历史 full506 用于参数搜索、锁定和正式结果副本背景；当前论文主表口径仍为 `full502_clean_v1` 与 `compare9_complete496_v1`。",
            f"{evidence(stage1_paths['long_plan'])}; {evidence(stage1_paths['evidence_pack'])}",
            "无。",
            "不能把 `full506` 写成当前正式阶段表或外部主表的样本口径。",
            "全文搜索 `full506`，确保只作为历史背景或路径名出现。",
            [rel(stage1_paths["long_plan"]), rel(stage1_paths["draft"]), rel(stage1_paths["evidence_pack"])],
        ),
        claim(
            "C05",
            "Metric interpretation",
            "`MS_SSIM` / `PSNR` 在当前增强协议中是相对原图的结构一致性。",
            "allowed_with_boundary",
            "可以写：二者反映增强结果相对原始输入的结构一致性或保守相似性。",
            f"{evidence(stage1_paths['draft'])}; {evidence(stage1_paths['evidence_pack'])}; {evidence(stage1_paths['comparison_index'])}",
            "无。",
            "不能写成相对增强真值的质量指标，也不能用它们证明增强视觉质量真值更好。",
            "继续在主稿、图注和表注中统一解释。",
            [rel(stage1_paths["draft"]), rel(stage1_paths["evidence_pack"]), rel(stage1_paths["comparison_index"])],
        ),
        claim(
            "C06",
            "External baseline boundaries",
            "外部方法的论文分类与当前协议下表现边界已经明确。",
            "allowed_with_boundary",
            "可以写：`WWPF` 是激进但可接受的强基线；`HLRP` / `Histoformer` 可作为当前 HAB 显微协议下失败案例或补充分析；`HVDualformer` / `ABC-Former` 是白平衡方法。",
            f"{evidence(stage1_paths['comparison_index'])}; methods={', '.join(compare_methods)}",
            "若写 related work 细节，仍需回到本地 Zotero/PDF 或本地文献笔记核验。",
            "不能删除 `WWPF`；不能把 HLRP/Histoformer 的当前复现问题泛化为原方法无效；不能把白平衡方法写成标准水下增强模型。",
            "主稿和图表计划中保持该分类。",
            [rel(stage1_paths["comparison_index"]), rel(stage1_paths["evidence_pack"])],
        ),
        claim(
            "C07",
            "Stage1 no-GT edge proxy",
            "Stage1 已形成无 GT 边缘结构 proxy 支撑包。",
            "allowed_with_boundary",
            "可以写：当前已有 Sobel/Otsu 风格的无 GT 边缘结构 proxy，可用于结构保持讨论、选图和失败案例筛查。",
            f"{evidence(stage1_paths['proxy_stage_summary'])}; {evidence(stage1_paths['proxy_compare_summary'])}",
            "MyEdge / DiffusionEdge 带 GT 的 ODS/OIS/AP/AC 仍缺。",
            "不能把无 GT proxy 写成下游边缘检测正式指标，也不能据此声称 Stage1 已提升 ODS/OIS/AP/AC。",
            "后续与 MyEdge P1 fixed-detector 结果衔接。",
            [rel(stage1_paths["proxy_root"]), rel(stage1_paths["gap_dashboard"])],
        ),
        claim(
            "C08",
            "Full algae image pool audit",
            "完整增强图像池已完成 manifest、decode、重复和质量审计。",
            "allowed_with_boundary",
            f"可以写：外部完整增强图像池含 `{full_image_count}` 张图像，默认候选 `{candidate_count}` 张，OpenCV 可读候选 `{cv2_count}` 张；当前人工复核仍 pending `{manual_pending}`。",
            f"{evidence(stage1_paths['inventory'])}; {evidence(stage1_paths['inventory_audit'])}; {evidence(stage1_paths['full_manifest'])}; {evidence(stage1_paths['cv2_manifest'])}; {evidence(stage1_paths['decode_summary'])}",
            "人工复核后的 clean manifest、split leakage guard、与两篇参考论文具体数据子集的本地重合关系仍缺。",
            "不能把 2777 图像池写成已清洗正式协议、已完成增强结果或带 GT edge 数据集。",
            "先完成人工复核，再决定 clean protocol 与 full-pool 长跑。",
            [rel(stage1_paths["inventory"]), rel(stage1_paths["inventory_audit"]), rel(stage1_paths["manual_validation"]), rel(stage1_paths["long_plan"])],
        ),
        claim(
            "C09",
            "Stage1 full2770 execution readiness",
            "Stage1 2770 张 OpenCV 可读候选长跑已经完成执行准备，但未执行。",
            "readiness_only",
            "可以写：`cv2readable2770` candidate run 在明确授权后具备执行条件；当前 full2770 输出根不存在，intake 为 `not_started`。",
            f"{evidence(stage1_paths['full2770_readiness'])}; status=`{full2770_status}`",
            "2770 张完整增强输出、post-run intake、run report、reviewed clean protocol 仍缺。",
            "不能写 full2770 已完成；不能把 candidate long run 写成 reviewed clean full-pool protocol。",
            "需要明确授权后才可运行长跑；完成后先 intake 再更新状态文档。",
            [rel(stage1_paths["full2770_readiness"]), rel(stage1_paths["long_plan"])],
        ),
        claim(
            "C10",
            "MyEdge formal MSFI result",
            "MyEdge MSFI 50k 主结果已存在，但指标画像是 mixed profile。",
            "allowed_with_boundary",
            (
                "可以写：MSFI 50k 相比 DiffusionEdge baseline 50k 在 ODS/OIS 上提升，AP 下降，AC 基本持平；"
                f"MSFI ODS `{formal_msfi.get('ods')}` / OIS `{formal_msfi.get('ois')}` / AP `{formal_msfi.get('ap')}` / AC `{formal_msfi.get('ac')}`；"
                f"baseline ODS `{baseline_diffusion.get('ods')}` / OIS `{baseline_diffusion.get('ois')}` / AP `{baseline_diffusion.get('ap')}` / AC `{baseline_diffusion.get('ac')}`。"
            ),
            f"{evidence(myedge_paths['experiment_status'], myedge_root)}; {evidence(myedge_paths['paper_ready_results'], myedge_root)}",
            "AP trade-off 的 PR 曲线/阈值分析、效率、失败案例和更多消融仍缺。",
            "不能写全面领先、SOTA、所有指标最优，也不能回避 AP 下降。",
            "下一步补 PR/AP trade-off、效率、失败案例和消融。",
            [rel(myedge_paths["experiment_status"], myedge_root), rel(stage1_paths["gap_dashboard"])],
        ),
        claim(
            "C11",
            "Stage1-to-MyEdge P1 status",
            "Stage1 Final -> MyEdge fixed-detector P1 已完成执行、intake 和 report asset sync。",
            "allowed_with_boundary" if p1_intake_status == "complete_with_report_assets" else "readiness_only",
            (
                "可以写：168 张 coupling manifest、Stage1 Final、GT、MSFI/baseline config template 和 baseline checkpoint 冻结记录均已核对；"
                f"P1 intake 当前为 `{p1_intake_status}`。"
            ),
            f"{evidence(stage1_paths['coupling_status'])}; readiness_status=`{p1_status}`; intake_status=`{p1_intake_status}`",
            "stage-wise、generic enhancement controls、退化子集和形态一致性证据仍缺。",
            "P1 只能按 168 张 / Stage1 Final / fixed detector 解释，不能外推到 full502/full2770 或所有阶段。",
            "下一步补 Stage1 stage-wise / generic enhancement controls。",
            [rel(stage1_paths["p1_readiness"]), rel(stage1_paths["coupling_status"])],
        ),
        claim(
            "C12",
            "Stage1 downstream edge gain",
            "Stage1 Final 当前能否作为 positive downstream edge enhancement 证据。",
            "allowed_with_boundary" if p1_intake_status == "complete_with_report_assets" else "planned_only_not_claimable",
            (
                "可以写：P1 fixed-detector 结果已完成，但当前不支持“Stage1 Final 提升下游边缘检测”的正向结论；"
                f"Stage1 Final -> MSFI mat ODS/OIS/AP/AC = `{p1_msfi_mat.get('ods')}` / `{p1_msfi_mat.get('ois')}` / `{p1_msfi_mat.get('ap')}` / `{p1_msfi.get('ac_from_show')}`；"
                f"Stage1 Final -> DiffusionEdge baseline mat ODS/OIS/AP/AC = `{p1_baseline_mat.get('ods')}` / `{p1_baseline_mat.get('ois')}` / `{p1_baseline_mat.get('ap')}` / `{p1_baseline.get('ac_from_show')}`；"
                f"DiffusionEdge baseline stage-wise 诊断状态为 `{stagewise_status}`，结果为 {stagewise_metrics}；"
                f"MSFI stage-wise 诊断状态为 `{stagewise_msfi_status}`，结果为 {stagewise_msfi_metrics}。"
            ),
            (
                f"{evidence(myedge_paths['p1_msfi_root'], myedge_root)}; "
                f"{evidence(myedge_paths['p1_baseline_root'], myedge_root)}; "
                f"{evidence(myedge_paths['stagewise_baseline_results'], myedge_root)}; "
                f"{evidence(myedge_paths['stagewise_msfi_results'], myedge_root)}; "
                f"{evidence(stage1_paths['coupling_status'])}"
            ),
            "还缺 generic enhancement controls、repeat/control、raw-anchor paired delta 表、退化子集与形态一致性指标。",
            "不能写 Stage1 Final 或 Stage1 各阶段已提升 ODS/OIS/AP/AC；当前 P1/P2 更应写成负向/诊断性证据。",
            "补 generic enhancement controls 和 P4 repeat/control，定位是否为增强分布迁移、detector-specific 问题或可稳定利用的 edge-safe 输入形成策略。",
            [rel(stage1_paths["coupling_status"]), rel(stage1_paths["gate_board"])],
        ),
        claim(
            "C13",
            "Stage1 downstream-driven P4 variant",
            "不覆盖旧主线的 edge-preserve Stage1 变体是否已把下游损伤拉回 raw 附近。",
            "allowed_with_boundary" if downstream_variant_p4_status == "complete_with_report_assets" else "planned_only_not_claimable",
            (
                "可以写：P4 downstream-driven edge-preserve 诊断已完成，旧 Stage1 Final 的大幅下游损伤可通过保留 raw luminance/spatial structure "
                "并只进行轻量 BPH color/illumination transfer 基本消除；"
                f"P4 状态为 `{downstream_variant_p4_status}`，结果为 {downstream_variant_p4_metrics}。"
            ),
            evidence(myedge_paths["downstream_variant_p4_results"], myedge_root),
            "P6B paired review 已完成并补强逐图配对诊断；仍缺 repeat/control、generic enhancement controls 和更稳的 502/168 交叉解释，P5C/P6/P6B 仍不足以支撑稳定正向收益。",
            "不能写 P4 稳定优于 raw；当前最强边界是 edge_preserve_raw_bph_moderate_v1 接近 historical raw anchor，并在同轮 original-control 下改善 AP/OIS 但 AC 略降。",
            "先补 repeat/control 与 generic enhancement controls；成功前不启动 full2770。",
            [rel(myedge_paths["downstream_variant_p4_results"], myedge_root), rel(stage1_paths["gate_board"])],
        ),
        claim(
            "C13B",
            "Stage1 downstream-driven P5C baseline-side check",
            "不覆盖旧主线的 edge-preserve Stage1 变体是否在第二检测器 DiffusionEdge baseline 下也接近 raw。",
            "allowed_with_boundary" if downstream_variant_baseline_p5c_status == "complete_with_report_assets" else "planned_only_not_claimable",
            (
                "可以写：P5C baseline-side 诊断已完成，edge-preserve 方向不是 MSFI-only；"
                f"P5C 状态为 `{downstream_variant_baseline_p5c_status}`，结果为 {downstream_variant_baseline_p5c_metrics}。"
            ),
            evidence(myedge_paths["downstream_variant_baseline_p5c_results"], myedge_root),
            "P6B paired review 已完成并补强逐图配对诊断；仍缺 repeat/control、generic enhancement controls 和 generic-vs-Stage1 对照，P6/P6B 仍不能替代稳定正向收益证据。",
            "不能写 P5C 证明 Stage1 稳定提升下游；mild 虽有 AP/OIS 正向信号，但 AC 仍低于 raw，且只覆盖 168 张 / 固定 DiffusionEdge baseline 50k。",
            "先补 repeat/control、generic enhancement controls 和结构连续性 / 背景伪边分析；成功前不启动 full2770。",
            [rel(myedge_paths["downstream_variant_baseline_p5c_results"], myedge_root), rel(stage1_paths["gate_board"])],
        ),
        claim(
            "C13C",
            "Stage1 downstream-driven P6 structure proxy",
            "P4/P5C 现有 MAT 输出的结构、碎裂与伪边 proxy 诊断已经完成。",
            "allowed_with_boundary" if downstream_variant_structure_p6_status == "complete" else "planned_only_not_claimable",
            (
                "可以写：P6 只读已有 P4/P5C MAT 与 GT，以各 run ODS threshold 二值化并用 2px tolerance 计算结构 proxy；"
                f"P6 状态为 `{downstream_variant_structure_p6_status}`，P6B paired review 状态为 `{downstream_variant_structure_p6_paired_status}`，关键结果为 {downstream_variant_structure_p6_metrics}。"
            ),
            f"{evidence(myedge_paths['downstream_variant_structure_p6_results'], myedge_root)}; paired={evidence(myedge_paths['downstream_variant_structure_p6_paired_review'], myedge_root)}",
            "还缺 repeat/control、generic enhancement controls、generic-vs-Stage1 对照和正式 full502/full2770 范围验证。",
            "P6/P6B 是 168 张 MyEdge split 上的结构诊断 proxy，不替代 ODS/OIS/AP/AC；只能支持旧 Final 伪边/碎裂严重、P4/MSFI moderate 有降低伪边与碎裂的诊断性叙述。",
            "基于 P6/P6B 设计下一轮 generic controls 与 repeat/control；成功前不启动 full2770。",
            [rel(myedge_paths["downstream_variant_structure_p6_results"], myedge_root), rel(myedge_paths["downstream_variant_structure_p6_paired_review"], myedge_root), rel(stage1_paths["gate_board"])],
        ),
        claim(
            "C13D",
            "Stage1 generic enhancement controls P7",
            "两个非 BPH 的 generic luminance-only controls 已完成 168 张固定 MSFI 与 DiffusionEdge baseline 下游诊断。",
            "allowed_with_boundary" if generic_control_p7_status == "complete_with_report_assets" else ("readiness_only" if generic_control_p7_status == "ready_for_sampling_not_evaluated" else "planned_only_not_claimable"),
            (
                "可以写：P7 在 168 张 MyEdge split 上完成 fixed MSFI 50k 与 fixed DiffusionEdge baseline 50k 诊断；"
                f"当前状态为 `{generic_control_p7_status}`，关键结果为 {generic_control_p7_metrics}。"
            ),
            generic_control_p7_evidence,
            "仍缺 P7 repeat/control 以及 full502/full2770 范围验证；P7 结构/伪边 proxy 与 paired review 已完成但仍属诊断证据。",
            "P7 只支持 lightweight luminance-only control 的 168 张诊断：gamma 在 baseline 侧有小幅 ODS/OIS/AP 信号，MSFI 侧基本贴近 raw；结构 proxy 上 MSFI/gamma 有轻微信号但 baseline/gamma 仍 mixed，不能写 Stage1 全流程或稳定正向下游收益。",
            "下一步优先做 P7 repeat/control；成功前不启动 full2770。",
            [
                rel(myedge_paths["generic_control_p7_msfi_preflight"], myedge_root),
                rel(myedge_paths["generic_control_p7_baseline_preflight"], myedge_root),
                rel(myedge_paths["generic_control_p7_msfi_results"], myedge_root),
                rel(myedge_paths["generic_control_p7_baseline_results"], myedge_root),
                rel(myedge_paths["generic_control_p7_structure_metrics"], myedge_root),
                rel(myedge_paths["generic_control_p7_structure_paired_review"], myedge_root),
                rel(stage1_paths["gate_board"]),
            ],
        ),
        claim(
            "C14",
            "MSFI component ablation",
            "MSFI 的 frequency token、spatial-frequency interaction、timestep gating 各自有效。",
            "planned_only_not_claimable",
            "当前只能写成 planned ablation 或 future evidence requirement。",
            evidence(myedge_paths["component_ablation_contract"], myedge_root),
            "组件级实验结果、统一评测表、统计解释和图组缺失。",
            "合同存在不等于结果完成；不能写任一组件已被独立证明有效。",
            "在 MyEdge 侧完成组件消融并同步结果。",
            [rel(myedge_paths["component_ablation_contract"], myedge_root), rel(stage1_paths["gap_dashboard"])],
        ),
        claim(
            "C15",
            "MSFI replacement comparison",
            "MSFI 优于 Sobel/CIAFF-like/Fourier/CBAM/SE/ECA/ASPP/FPN 替换模块。",
            "planned_only_not_claimable",
            "当前只能写成必须补齐的对标实验。",
            evidence(myedge_paths["replacement_contract"], myedge_root),
            "替换模块训练/评测结果缺失。",
            "不能借参考论文或计划文件推断 MSFI 已优于这些模块。",
            "在 MyEdge 侧完成替换模块对比，直接回应 ESWA 参考论文重合风险。",
            [rel(myedge_paths["replacement_contract"], myedge_root), rel(stage1_paths["eswa_note"])],
        ),
        claim(
            "C16",
            "Degradation subset robustness",
            "方法对低对比、弱边界、气泡/杂质、模糊边界等退化子集鲁棒。",
            "planned_only_not_claimable",
            "当前只能写成后续分层分析计划。",
            f"{evidence(myedge_paths['degradation_contract'], myedge_root)}; manual pending=`{manual_pending}`",
            "人工确认的退化子集标签、带 GT 子集 manifest、子集指标表缺失。",
            "不能泛化声称复杂退化鲁棒；也不能把质量异常机助建议直接当人工标签。",
            "先完成 full-pool manual review，再在 MyEdge 侧形成带 GT 子集评测。",
            [rel(myedge_paths["degradation_contract"], myedge_root), rel(stage1_paths["manual_validation"])],
        ),
        claim(
            "C17",
            "Efficiency, PR and failure cases",
            "论文已有投稿级效率、PR/AP trade-off、失败案例和 qualitative assets。",
            "planned_only_not_claimable",
            "当前只能写：Figure 1/2 与部分方法/结果资产已有，PR、效率和失败案例仍待补。",
            evidence(myedge_paths["efficiency_failure_contract"], myedge_root),
            "Params/FLOPs/FPS/显存、PR curve、TP/FP/FN overlay、failure-case panel 缺失或未在 Stage1 侧接收。",
            "不能写更快、更轻量、更可部署或已经完成 AP trade-off 解释。",
            "完成 MyEdge 效率与 paper asset 合同，并同步可引用文档。",
            [rel(myedge_paths["efficiency_failure_contract"], myedge_root), rel(stage1_paths["gap_dashboard"])],
        ),
        claim(
            "C18",
            "Dataset relation to two Wu et al. 2026 papers",
            "本项目数据与两篇同实验室一区论文数据集关系已经可以写清。",
            "allowed_with_boundary",
            "可以写：Zotero 本地缓存已核验两篇参考论文的数据描述字段；本项目当前只能确认自身 2777/2774/2770 图像池，尚不能证明与 676/1026 子集精确重合。",
            f"{evidence(stage1_paths['reference_dataset_relation_audit'])}; {evidence(stage1_paths['eswa_note'])}; {evidence(stage1_paths['eaai_note'])}; {evidence(stage1_paths['inventory'])}",
            "本项目自己的设备/倍率/物种/专家标注说明、与 676/1026 子集的文件级交集或差异证明仍缺。",
            "不能照搬参考论文的数据描述，也不能把“同实验室”写成已经本地核验的同一数据划分。",
            "补齐文件级清单、hash、原始采集编号、标注文件或实验室登记证明，才能声称与参考论文数据存在精确关系。",
            [
                rel(stage1_paths["reference_dataset_relation_audit"]),
                rel(stage1_paths["eswa_note"]),
                rel(stage1_paths["eaai_note"]),
                rel(stage1_paths["inventory"]),
            ],
        ),
        claim(
            "C19",
            "Overall paper framing",
            "论文主线应以 MyEdge/MSFI 为核心，Stage1 是任务驱动结构保持输入支撑。",
            "allowed_with_boundary",
            "可以写：Stage1 提供 structure-preserving input formation 和证据支撑；主创新应落在 spatial-frequency weak-boundary diffusion 与后续 GT edge evidence。",
            f"{evidence(stage1_paths['long_plan'])}; {evidence(stage1_paths['gap_dashboard'])}; {evidence(stage1_paths['gate_board'])}",
            "MyEdge 消融、Stage1 P1、退化子集和效率证据仍缺。",
            "不能把总论文写成简单的 Stage1 + MyEdge 流水线，也不能把 Stage1 单独包装成完整一区主创新闭环。",
            "按 gate board 推进 P1、消融、替换、退化子集、效率和写作同步。",
            [rel(stage1_paths["long_plan"]), rel(stage1_paths["gap_dashboard"]), rel(stage1_paths["gate_board"])],
        ),
    ]

    status_counts = Counter(str(item["write_status"]) for item in claims)
    scope_counts = Counter(str(item["claim_scope"]) for item in claims)
    immediate_claims = [
        item["claim_id"]
        for item in claims
        if item["write_status"] in {"allowed_fact", "allowed_with_boundary", "readiness_only"}
    ]
    experiment_waiting_claims = [
        item["claim_id"]
        for item in claims
        if item["write_status"] in {"planned_only_not_claimable", "missing"}
    ]
    forbidden_wording = [
        "Stage1 已提升 ODS/OIS/AP/AC，或 Stage1 Final 已被证明是 positive downstream enhancement。",
        "Stage1 full2770 已完成、reviewed clean manifest 已生成，或 2777 图像池已经是正式清洗协议。",
        "P6/P6B 结构 proxy 已证明 Stage1 稳定提升下游边缘检测，或可以替代 ODS/OIS/AP/AC。",
        "直接运行 `python main.py` 就是正式主线。",
        "`MS_SSIM` / `PSNR` 表示相对增强真值的质量。",
        "MSFI 全面领先、SOTA、所有指标最优，或回避 AP 下降。",
        "HLRP / Histoformer 在一般场景中无效。",
        "HVDualformer / ABC-Former 是标准水下增强模型。",
        "`WWPF` 因输出 496 张或激进指标而可以删除。",
        "机助 `machine_suggestion` 等同于人工 `reviewer_decision`。",
        "两篇参考论文的数据描述可以直接照搬到本项目。",
    ]
    paper_safe_claims = [
        "正式 Stage1 主线、正式结果目录、full502_clean_v1 阶段表和 compare9_complete496_v1 主表已经锁定。",
        "Stage1 当前只能作为 MyEdge/MSFI 论文中的 structure-preserving input formation 候选支撑；P1 和两条 fixed-detector stage-wise 诊断均不支持旧 Stage1 的正向下游增益。",
        "Stage1 P4/P5C downstream-driven edge-preserve 变体已把旧 Final 的下游损伤基本拉回 raw 附近，并在 MSFI 与 DiffusionEdge baseline 两个固定检测器下形成 edge-safe 候选证据；P6/P6B 进一步给出结构 proxy 与逐图配对诊断，但当前不能写稳定优于 raw。",
        "Generic controls P7 已完成固定 MSFI 与 DiffusionEdge baseline 评测、结构 proxy 和 paired review；当前只能写成 168 张轻量 luminance-only control 诊断，不能写成 Stage1 稳定正向下游收益。",
        "MyEdge MSFI 当前可写 mixed metric profile：ODS/OIS 提升，AP 下降，AC 基本持平。",
        "MyEdge P1、DiffusionEdge baseline stage-wise、MSFI stage-wise 与 P4 诊断已完成；当前结果整体不支持旧 Stage1 正向下游收益，full2770 仍只是执行准备，不能写结果。",
    ]
    claims_waiting = [
        "Generic enhancement controls 的 P7 repeat/control 和 generic-vs-Stage1 对照；P6B 与 P7 paired review 已完成但只属结构 proxy 诊断。",
        "MSFI frequency token / spatial-frequency interaction / timestep gating 的独立有效性。",
        "MSFI 相比 Sobel/CIAFF-like/Fourier/attention 替换模块的优势。",
        "低对比、弱边界、气泡/杂质、模糊边界子集鲁棒性。",
        "效率、PR/AP trade-off、失败案例与投稿级 qualitative 图组。",
        "与两篇同实验室参考论文数据集的精确关系和可投稿数据说明。",
    ]

    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "stage1_root": str(PROJECT_ROOT),
        "myedge_root": str(myedge_root),
        "no_experiment_executed": True,
        "overall_status": "claim_boundaries_locked_major_experiment_claims_pending",
        "summary": {
            "claim_count": len(claims),
            "status_counts": dict(sorted(status_counts.items())),
            "scope_counts": dict(sorted(scope_counts.items())),
            "immediate_claim_ids": immediate_claims,
            "experiment_waiting_claim_ids": experiment_waiting_claims,
            "stage1_stage_count": stage_count,
            "stage1_compare_count": compare_count,
            "full_image_pool_count": full_image_count,
            "default_candidate_count": candidate_count,
            "cv2_readable_candidate_count": cv2_count,
            "manual_pending_rows": manual_pending,
            "full2770_readiness_status": full2770_status,
            "myedge_p1_readiness_status": p1_status,
            "myedge_p1_intake_status": p1_intake_status,
            "myedge_stagewise_baseline_status": stagewise_status,
            "myedge_stagewise_msfi_status": stagewise_msfi_status,
            "myedge_downstream_variant_p4_status": downstream_variant_p4_status,
            "myedge_downstream_variant_baseline_p5c_status": downstream_variant_baseline_p5c_status,
            "myedge_downstream_variant_structure_p6_status": downstream_variant_structure_p6_status,
            "myedge_downstream_variant_structure_p6_paired_status": downstream_variant_structure_p6_paired_status,
            "myedge_generic_control_p7_status": generic_control_p7_status,
            "myedge_msfi_ods": formal_msfi.get("ods"),
            "myedge_msfi_ois": formal_msfi.get("ois"),
            "myedge_msfi_ap": formal_msfi.get("ap"),
            "myedge_msfi_ac": formal_msfi.get("ac"),
            "gap_dashboard_status": (gap_dashboard.get("summary") or {}).get("overall_status"),
        },
        "claims": claims,
        "paper_safe_claims": paper_safe_claims,
        "claims_waiting_for_evidence": claims_waiting,
        "forbidden_wording": forbidden_wording,
        "boundary": (
            "This ledger reads existing local Stage1Codex and MyEdgeCodex files only. It does not run Stage1 "
            "enhancement, MyEdge sampling, eval.py, show.py, training, figure generation, or metric recomputation. "
            "It records what can be written now, what can only be written as readiness, and what remains non-claimable."
        ),
    }


def write_markdown(path: Path, ledger: Dict[str, object]) -> None:
    summary: Dict[str, object] = ledger["summary"]  # type: ignore[assignment]
    claims: Sequence[Dict[str, object]] = ledger["claims"]  # type: ignore[assignment]
    lines: List[str] = [
        "# Stage1Codex + MyEdgeCodex claim-to-evidence ledger",
        "",
        f"日期：{datetime.now().date().isoformat()}",
        "",
        "本文是跨 Stage1Codex 与 MyEdgeCodex 的论文主张证据总账。它只读取本地已落盘文件，不运行增强、训练、采样、`eval.py`、`show.py`、图表生成或指标重算。",
        "",
        "## Executive Summary",
        "",
        f"- Overall status: `{ledger['overall_status']}`",
        f"- No experiment executed by this script: `{ledger['no_experiment_executed']}`",
        f"- Claim count: `{summary['claim_count']}`",
        f"- Stage1 formal stage count: `{summary['stage1_stage_count']}`",
        f"- Stage1 formal comparison count: `{summary['stage1_compare_count']}`",
        f"- Full image pool / default candidate / cv2-readable candidate: `{summary['full_image_pool_count']}` / `{summary['default_candidate_count']}` / `{summary['cv2_readable_candidate_count']}`",
        f"- Manual review pending rows: `{summary['manual_pending_rows']}`",
        f"- Stage1 full2770 readiness: `{summary['full2770_readiness_status']}`",
        f"- MyEdge P1 readiness: `{summary['myedge_p1_readiness_status']}`",
        f"- MyEdge P1 intake: `{summary['myedge_p1_intake_status']}`",
        f"- MyEdge MSFI stage-wise: `{summary['myedge_stagewise_msfi_status']}`",
        f"- MyEdge downstream-driven Stage1 P4: `{summary['myedge_downstream_variant_p4_status']}`",
        f"- MyEdge downstream-driven Stage1 baseline P5C: `{summary['myedge_downstream_variant_baseline_p5c_status']}`",
        f"- MyEdge downstream-driven Stage1 structure P6: `{summary['myedge_downstream_variant_structure_p6_status']}`",
        f"- MyEdge downstream-driven Stage1 structure P6 paired review: `{summary['myedge_downstream_variant_structure_p6_paired_status']}`",
        f"- MyEdge generic enhancement controls P7: `{summary['myedge_generic_control_p7_status']}`",
        f"- MyEdge MSFI metrics: ODS `{summary['myedge_msfi_ods']}`, OIS `{summary['myedge_msfi_ois']}`, AP `{summary['myedge_msfi_ap']}`, AC `{summary['myedge_msfi_ac']}`",
        "",
        "## Status Counts",
        "",
        "| Write status | Count |",
        "|---|---:|",
    ]
    for status, count in summary["status_counts"].items():  # type: ignore[index]
        lines.append(f"| `{status}` | {count} |")
    lines.extend(
        [
            "",
            "## Immediate Paper-Safe Claims",
            "",
        ]
    )
    for item in ledger["paper_safe_claims"]:  # type: ignore[index]
        lines.append(f"- {item}")
    lines.extend(["", "## Claims Waiting For Evidence", ""])
    for item in ledger["claims_waiting_for_evidence"]:  # type: ignore[index]
        lines.append(f"- {item}")
    lines.extend(["", "## Forbidden Wording", ""])
    for item in ledger["forbidden_wording"]:  # type: ignore[index]
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## Claim Matrix",
            "",
            "| ID | Scope | Claim | Write status | Allowed wording | Current evidence | Missing evidence | Paper boundary | Next gate |",
            "|---|---|---|---|---|---|---|---|---|",
        ]
    )
    for item in claims:
        lines.append(
            "| {claim_id} | {claim_scope} | {claim_text_cn} | `{write_status}` | {allowed_wording} | {current_evidence} | {missing_evidence} | {paper_boundary} | {next_gate} |".format(
                claim_id=table_escape(item["claim_id"]),
                claim_scope=table_escape(item["claim_scope"]),
                claim_text_cn=table_escape(item["claim_text_cn"]),
                write_status=table_escape(item["write_status"]),
                allowed_wording=table_escape(item["allowed_wording"]),
                current_evidence=table_escape(item["current_evidence"]),
                missing_evidence=table_escape(item["missing_evidence"]),
                paper_boundary=table_escape(item["paper_boundary"]),
                next_gate=table_escape(item["next_gate"]),
            )
        )
    lines.extend(
        [
            "",
            "## How To Use",
            "",
            "1. 写中文主稿或证据包时，先查 `allowed_fact` 与 `allowed_with_boundary` 行。",
            "2. `readiness_only` 行只能写“准备就绪但未执行”，不能写实验结果。",
            "3. `planned_only_not_claimable` 与 `missing` 行只能写成未来工作、待验证假设或实验计划。",
            "4. 后续只要 MyEdge P1、MSFI 消融、full2770 或人工复核状态变化，应重新运行本脚本并同步 `research-log.md`。",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    myedge_root = Path(args.myedge_root)
    ledger = build_ledger(myedge_root)
    output_json = Path(args.output_json)
    output_md = Path(args.output_md)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(ledger, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(output_md, ledger)
    print(json.dumps(ledger["summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
