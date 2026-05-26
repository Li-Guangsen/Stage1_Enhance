from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Sequence


THIS_DIR = Path(__file__).resolve().parent
METRICS_DIR = THIS_DIR.parent
PROJECT_ROOT = METRICS_DIR.parent
DEFAULT_DATE = datetime.now().date().strftime("%Y%m%d")
DEFAULT_OUTPUT_MD = PROJECT_ROOT / "docs" / f"stage1_full2770_execution_readiness_{DEFAULT_DATE}_cn.md"
DEFAULT_OUTPUT_JSON = PROJECT_ROOT / "docs" / f"stage1_full2770_execution_readiness_{DEFAULT_DATE}_cn.json"

SOURCE_ROOT = Path(r"D:\Desktop\去水印所有藻类图像")
EXPECTED_IMAGES = 2770
EXPECTED_OUTPUT_FILES = EXPECTED_IMAGES * 6 * 2


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build a read-only readiness package for the future Stage1 full2770 "
            "cv2-readable candidate full-pool run. This script does not run main.py, "
            "create output roots, generate enhanced images, or recompute metrics."
        )
    )
    parser.add_argument("--output-md", default=str(DEFAULT_OUTPUT_MD))
    parser.add_argument("--output-json", default=str(DEFAULT_OUTPUT_JSON))
    return parser.parse_args()


def read_json(path: Path) -> Dict[str, object]:
    if not path.exists():
        return {"_missing": True, "_path": str(path)}
    return json.loads(path.read_text(encoding="utf-8"))


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def read_manifest(path: Path) -> Dict[str, object]:
    raw_rows = 0
    rows: List[str] = []
    seen: set[str] = set()
    duplicates = 0
    if not path.exists():
        return {
            "exists": False,
            "raw_rows": 0,
            "unique_rows": 0,
            "duplicates": 0,
            "first": "",
            "last": "",
        }
    for line in path.read_text(encoding="utf-8").splitlines():
        item = line.strip().lstrip("\ufeff")
        if not item or item.startswith("#"):
            continue
        raw_rows += 1
        if item in seen:
            duplicates += 1
            continue
        seen.add(item)
        rows.append(item)
    return {
        "exists": True,
        "raw_rows": raw_rows,
        "unique_rows": len(rows),
        "duplicates": duplicates,
        "first": rows[0] if rows else "",
        "last": rows[-1] if rows else "",
    }


def rel(path: Path, root: Path = PROJECT_ROOT) -> str:
    try:
        return str(path.relative_to(root)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def evidence(path: Path, root: Path = PROJECT_ROOT) -> str:
    suffix = "" if path.exists() else " (missing)"
    return f"`{rel(path, root)}`{suffix}"


def yes_no(value: object) -> str:
    return "yes" if bool(value) else "no"


def table_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def prerequisite(
    item_id: str,
    requirement: str,
    satisfied: bool,
    evidence_text: str,
    blocking_if_failed: str,
) -> Dict[str, object]:
    return {
        "item_id": item_id,
        "requirement": requirement,
        "satisfied": satisfied,
        "evidence": evidence_text,
        "blocking_if_failed": blocking_if_failed,
    }


def future_step(
    step_id: str,
    title: str,
    command: str,
    risk_level: str,
    expected_evidence: str,
    stop_rule: str,
) -> Dict[str, str]:
    return {
        "step_id": step_id,
        "title": title,
        "command": command,
        "risk_level": risk_level,
        "expected_evidence": expected_evidence,
        "stop_rule": stop_rule,
    }


def disk_free_gib(path: Path) -> float:
    usage = shutil.disk_usage(path)
    return round(usage.free / (1024**3), 2)


def build_pack() -> Dict[str, object]:
    paths = {
        "source_root": SOURCE_ROOT,
        "locked_config": PROJECT_ROOT / "experiments" / "optimization_v1" / "configs" / "locked_full506_final_mainline.json",
        "manifest": PROJECT_ROOT / "metrics" / "manifests" / "full_algae_dewatermark_v1_cv2_readable_candidate.txt",
        "decode_summary": PROJECT_ROOT
        / "metrics"
        / "manifests"
        / "full_algae_dewatermark_v1_decode_audit.summary.json",
        "manual_validation": PROJECT_ROOT
        / "metrics"
        / "manifests"
        / "full_algae_dewatermark_v1_manual_review"
        / "manual_review_validation_status_20260525.json",
        "derived_review": PROJECT_ROOT
        / "metrics"
        / "manifests"
        / "full_algae_dewatermark_v1_manual_review"
        / "derived_review_artifacts"
        / "review_artifacts_status_20260525.json",
        "reviewed_clean_manifest": PROJECT_ROOT
        / "metrics"
        / "manifests"
        / "full_algae_dewatermark_v1_manual_review"
        / "derived_review_artifacts"
        / "reviewed_cv2_clean_manifest.txt",
        "smoke_summary": PROJECT_ROOT
        / "experiments"
        / "full-algae-dewatermark-v1"
        / "outputs"
        / "cv2readable2770"
        / "runs"
        / "smoke_summary.md",
        "smoke10_completeness": PROJECT_ROOT
        / "experiments"
        / "full-algae-dewatermark-v1"
        / "outputs"
        / "cv2readable2770"
        / "runs"
        / "smoke_limit10_locked_final_mainline_completeness.json",
        "budget": PROJECT_ROOT / "experiments" / "full-algae-dewatermark-v1" / "run_budget_estimate.md",
        "run_script": PROJECT_ROOT
        / "experiments"
        / "full-algae-dewatermark-v1"
        / "run_full_cv2readable2770_locked.ps1",
        "intake_script": PROJECT_ROOT / "metrics" / "scripts" / "intake_stage1_fullpool_run_outputs.py",
        "summarize_script": PROJECT_ROOT / "metrics" / "scripts" / "summarize_stage1_run_outputs.py",
        "intake_status": PROJECT_ROOT
        / "experiments"
        / "full-algae-dewatermark-v1"
        / "outputs"
        / "cv2readable2770"
        / "runs"
        / "full2770_locked_final_mainline_intake_status_20260525.json",
        "output_dir": PROJECT_ROOT
        / "experiments"
        / "full-algae-dewatermark-v1"
        / "outputs"
        / "cv2readable2770"
        / "runs"
        / "full2770_locked_final_mainline",
    }

    manifest = read_manifest(paths["manifest"])
    decode_summary = read_json(paths["decode_summary"])
    manual_validation = read_json(paths["manual_validation"])
    derived_review = read_json(paths["derived_review"])
    smoke10 = read_json(paths["smoke10_completeness"])
    intake_status = read_json(paths["intake_status"])
    run_script_text = read_text(paths["run_script"])

    candidate_images = decode_summary.get("candidate_images", {}) if isinstance(decode_summary, dict) else {}
    source_exists = paths["source_root"].exists()
    output_exists = paths["output_dir"].exists()
    free_gib = disk_free_gib(PROJECT_ROOT)
    has_enough_space = free_gib >= 5.0
    script_has_locked_config = "locked_full506_final_mainline.json" in run_script_text and "--params-json" in run_script_text
    script_has_manifest = "full_algae_dewatermark_v1_cv2_readable_candidate.txt" in run_script_text and "--manifest" in run_script_text
    script_has_skip_existing = "--skip-existing" in run_script_text
    clean_manifest_ready = paths["reviewed_clean_manifest"].exists() and bool(derived_review.get("can_generate_clean_manifest"))

    prerequisites: List[Dict[str, object]] = [
        prerequisite(
            "F01",
            "External source root is available",
            source_exists,
            str(paths["source_root"]),
            "Stop before long run; the external full algae image pool is not accessible.",
        ),
        prerequisite(
            "F02",
            "cv2-readable candidate manifest exists with 2770 unique rows",
            bool(manifest["exists"])
            and int(manifest["raw_rows"]) == EXPECTED_IMAGES
            and int(manifest["unique_rows"]) == EXPECTED_IMAGES
            and int(manifest["duplicates"]) == 0,
            (
                f"{evidence(paths['manifest'])}; raw={manifest['raw_rows']}; unique={manifest['unique_rows']}; "
                f"duplicates={manifest['duplicates']}; first={manifest['first']}; last={manifest['last']}"
            ),
            "Stop before long run; rebuild or inspect the manifest.",
        ),
        prerequisite(
            "F03",
            "Decode audit supports the cv2-readable candidate split",
            int(candidate_images.get("rows") or -1) == 2774
            and int(candidate_images.get("readable") or -1) == EXPECTED_IMAGES
            and int(candidate_images.get("decode_failures") or -1) == 4,
            (
                f"{evidence(paths['decode_summary'])}; candidate_rows={candidate_images.get('rows')}; "
                f"readable={candidate_images.get('readable')}; decode_failures={candidate_images.get('decode_failures')}"
            ),
            "Stop before long run; decode audit and manifest counts disagree.",
        ),
        prerequisite(
            "F04",
            "Locked final mainline config and resumable run script are present and aligned",
            paths["locked_config"].exists()
            and paths["run_script"].exists()
            and script_has_locked_config
            and script_has_manifest
            and script_has_skip_existing,
            (
                f"config={evidence(paths['locked_config'])}; run_script={evidence(paths['run_script'])}; "
                f"has_locked_config={script_has_locked_config}; has_manifest={script_has_manifest}; has_skip_existing={script_has_skip_existing}"
            ),
            "Stop before long run; the run script must explicitly pass the locked config and candidate manifest.",
        ),
        prerequisite(
            "F05",
            "Smoke and completeness assets exist",
            paths["smoke_summary"].exists()
            and paths["smoke10_completeness"].exists()
            and bool(smoke10.get("all_complete")),
            f"{evidence(paths['smoke_summary'])}; {evidence(paths['smoke10_completeness'])}; all_complete={smoke10.get('all_complete')}",
            "Stop before 2770 run; rerun or inspect smoke if completeness is not true.",
        ),
        prerequisite(
            "F06",
            "Budget, summarizer and intake scripts are present",
            paths["budget"].exists() and paths["summarize_script"].exists() and paths["intake_script"].exists(),
            f"{evidence(paths['budget'])}; {evidence(paths['summarize_script'])}; {evidence(paths['intake_script'])}",
            "Stop before long run; post-run intake must be available before execution.",
        ),
        prerequisite(
            "F07",
            "Full2770 output root is not started",
            not output_exists
            and intake_status.get("status") == "not_started"
            and not bool(intake_status.get("output_dir_exists"))
            and int(intake_status.get("present_output_files") or 0) == 0,
            (
                f"output={rel(paths['output_dir'])}; output_exists={output_exists}; intake_status={intake_status.get('status')}; "
                f"present_output_files={intake_status.get('present_output_files')}; expected_output_files={intake_status.get('expected_output_files')}"
            ),
            "Stop and inspect existing outputs before starting or resuming the run.",
        ),
        prerequisite(
            "F08",
            "Minimum disk-space recommendation is currently met",
            has_enough_space,
            f"free_space_gib={free_gib}; minimum_recommended_gib=5; preferred_with_future_artifacts_gib=8-10",
            "Stop before long run or free space; expected output is about 3.04 GiB plus logs/future artifacts.",
        ),
    ]
    candidate_ready = all(bool(item["satisfied"]) for item in prerequisites)
    clean_protocol_gate = {
        "status": "blocked_pending_manual_review" if not clean_manifest_ready else "ready",
        "manual_pending_rows": manual_validation.get("pending_rows"),
        "manual_invalid_rows": manual_validation.get("invalid_rows"),
        "can_generate_clean_manifest": derived_review.get("can_generate_clean_manifest"),
        "reviewed_clean_manifest_exists": paths["reviewed_clean_manifest"].exists(),
        "boundary": (
            "The cv2-readable 2770 run can be prepared as a candidate coverage run after explicit approval, "
            "but a reviewed clean full-pool protocol remains blocked until manual review is complete."
        ),
    }
    overall_status = (
        "candidate_full2770_ready_after_explicit_approval_clean_protocol_blocked"
        if candidate_ready and not clean_manifest_ready
        else "candidate_full2770_ready_after_explicit_approval"
        if candidate_ready
        else "not_ready_reconcile_first"
    )

    future_steps = [
        future_step(
            "S0",
            "Optional read-only preflight refresh",
            "D:\\Desktop\\EdgeDetection\\my_env\\python.exe metrics\\scripts\\intake_stage1_fullpool_run_outputs.py",
            "read_only",
            "Updated intake status remains not_started before execution.",
            "If output root exists unexpectedly, stop and inspect before running main.py.",
        ),
        future_step(
            "S1",
            "Run Stage1 cv2-readable 2770 candidate full run",
            "powershell -ExecutionPolicy Bypass -File experiments\\full-algae-dewatermark-v1\\run_full_cv2readable2770_locked.ps1",
            "high_risk_long_run",
            "full2770_locked_final_mainline output root, logs/full2770_locked_final_mainline.log, six stages x JPG/PNG outputs.",
            "Requires explicit user authorization; stop if free disk is below 5 GiB or the planned output root already contains mixed outputs.",
        ),
        future_step(
            "S2",
            "Read-only post-run intake",
            "D:\\Desktop\\EdgeDetection\\my_env\\python.exe metrics\\scripts\\intake_stage1_fullpool_run_outputs.py",
            "read_only_after_long_run",
            "Intake status reaches core_outputs_complete or complete_with_log_and_run_report.",
            "Do not write completion claims while status is not_started or incomplete_or_in_progress.",
        ),
        future_step(
            "S3",
            "Write run_report only after core outputs are complete",
            "D:\\Desktop\\EdgeDetection\\my_env\\python.exe metrics\\scripts\\intake_stage1_fullpool_run_outputs.py --write-run-report",
            "guarded_report_write",
            "output_dir/run_report.md exists and intake status reaches complete_with_log_and_run_report.",
            "The intake script refuses to write run_report unless core outputs are complete.",
        ),
        future_step(
            "S4",
            "Decide whether to promote any full-pool evidence",
            "manual review plus document update; no command",
            "human_decision",
            "README/status/research-state/research-log updated only after intake and human review.",
            "Do not replace full502_clean_v1 or compare9_complete496_v1 without a separately accepted protocol.",
        ),
    ]

    acceptance_criteria = [
        "Manifest raw and unique rows are exactly 2770.",
        "Run command explicitly passes locked_full506_final_mainline.json and full_algae_dewatermark_v1_cv2_readable_candidate.txt.",
        "Log exists at experiments/full-algae-dewatermark-v1/outputs/cv2readable2770/runs/full2770_locked_final_mainline/logs/full2770_locked_final_mainline.log.",
        "Each of six stages has 2770 JPG and 2770 PNG outputs, for 33240 files total.",
        "Final PNG decode sample succeeds after post-run intake.",
        "run_report.md is generated only after core outputs are complete.",
        "State docs and research-log are updated only after intake proves completion.",
    ]
    paper_boundaries = [
        "Current status can only be written as candidate full2770 ready after explicit approval, not executed.",
        "The four GIF89a-content files remain outside the cv2-readable run unless converted through a separate reviewed decision.",
        "Manual review still blocks a reviewed clean full-pool manifest.",
        "Full2770 coverage evidence does not replace the current formal full502_clean_v1 and compare9_complete496_v1 paper result protocols.",
        "Full2770 enhancement outputs alone do not prove downstream edge gains; MyEdge GT validation is still required.",
    ]

    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "stage1_root": str(PROJECT_ROOT),
        "source_root": str(paths["source_root"]),
        "no_experiment_executed": True,
        "overall_status": overall_status,
        "candidate_run_ready_after_explicit_approval": candidate_ready,
        "expected_images": EXPECTED_IMAGES,
        "expected_output_files": EXPECTED_OUTPUT_FILES,
        "free_space_gib": free_gib,
        "source_status_files": {name: str(path) for name, path in paths.items()},
        "manifest": manifest,
        "current_intake": {
            "status": intake_status.get("status"),
            "output_dir_exists": intake_status.get("output_dir_exists"),
            "log_exists": intake_status.get("log_exists"),
            "run_report_exists": intake_status.get("run_report_exists"),
            "present_output_files": intake_status.get("present_output_files"),
            "missing_output_files": intake_status.get("missing_output_files"),
            "no_main_py_execution": intake_status.get("no_main_py_execution"),
        },
        "clean_protocol_gate": clean_protocol_gate,
        "prerequisites": prerequisites,
        "future_execution_sequence": future_steps,
        "acceptance_criteria": acceptance_criteria,
        "paper_boundaries": paper_boundaries,
        "hard_stops": [
            "Do not run the full2770 PowerShell script without explicit user authorization.",
            "Do not use the candidate cv2-readable run as a reviewed clean manifest.",
            "Do not claim 2770 completion before intake reaches complete_with_log_and_run_report.",
            "Do not overwrite current formal 502/496 result directories.",
        ],
    }


def write_markdown(path: Path, pack: Dict[str, object]) -> None:
    prereqs: Sequence[Dict[str, object]] = pack["prerequisites"]
    steps: Sequence[Dict[str, str]] = pack["future_execution_sequence"]
    clean_gate: Dict[str, object] = pack["clean_protocol_gate"]
    intake: Dict[str, object] = pack["current_intake"]
    lines: List[str] = [
        "# Stage1 full2770 cv2-readable candidate execution readiness pack",
        "",
        f"日期：{datetime.now().date().isoformat()}",
        "",
        "本文是 Stage1 侧 2770 张 OpenCV 可读候选完整增强长跑的执行准备包。它只读取现有 manifest、审计、smoke、预算、run script 和 intake 状态，不运行 `main.py`，不创建 full2770 输出根目录，不生成增强图像，也不重算指标。",
        "",
        "## Summary",
        "",
        f"- Overall status: `{pack['overall_status']}`",
        f"- Candidate run ready after explicit approval: `{pack['candidate_run_ready_after_explicit_approval']}`",
        f"- Expected images: `{pack['expected_images']}`",
        f"- Expected output files: `{pack['expected_output_files']}`",
        f"- Current intake status: `{intake.get('status')}`",
        f"- Output dir exists: `{intake.get('output_dir_exists')}`",
        f"- Present output files: `{intake.get('present_output_files')}`",
        f"- Free space on project drive: `{pack['free_space_gib']}` GiB",
        f"- No experiment executed by this script: `{pack['no_experiment_executed']}`",
        "",
        "## Clean Protocol Gate",
        "",
        f"- Reviewed clean status: `{clean_gate.get('status')}`",
        f"- Manual review pending rows: `{clean_gate.get('manual_pending_rows')}`",
        f"- Manual review invalid rows: `{clean_gate.get('manual_invalid_rows')}`",
        f"- Can generate clean manifest: `{clean_gate.get('can_generate_clean_manifest')}`",
        f"- Reviewed clean manifest exists: `{clean_gate.get('reviewed_clean_manifest_exists')}`",
        "",
        "解释：`cv2readable2770` 可以作为候选覆盖长跑准备，但 reviewed clean full-pool protocol 仍被人工复核阻塞；两者不能混写。",
        "",
        "## Current Evidence",
        "",
        f"- Source root: `{pack['source_root']}`",
        f"- Manifest: {evidence(Path(pack['source_status_files']['manifest']))}",
        f"- Decode summary: {evidence(Path(pack['source_status_files']['decode_summary']))}",
        f"- Smoke summary: {evidence(Path(pack['source_status_files']['smoke_summary']))}",
        f"- Budget: {evidence(Path(pack['source_status_files']['budget']))}",
        f"- Run script: {evidence(Path(pack['source_status_files']['run_script']))}",
        f"- Intake status: {evidence(Path(pack['source_status_files']['intake_status']))}",
        "",
        "## Preconditions",
        "",
        "| ID | Requirement | Satisfied | Evidence | Blocking rule if failed |",
        "|---|---|---|---|---|",
    ]
    for item in prereqs:
        lines.append(
            "| {item_id} | {requirement} | `{satisfied}` | {evidence_text} | {blocking_if_failed} |".format(
                item_id=table_escape(item["item_id"]),
                requirement=table_escape(item["requirement"]),
                satisfied=yes_no(item["satisfied"]),
                evidence_text=table_escape(item["evidence"]),
                blocking_if_failed=table_escape(item["blocking_if_failed"]),
            )
        )
    lines.extend(
        [
            "",
            "## Future Execution Sequence",
            "",
            "以下步骤只是未来执行顺序。S1 是长时间高风险运行，必须先得到用户明确授权。",
            "",
        ]
    )
    for item in steps:
        lines.extend(
            [
                f"### {item['step_id']} - {item['title']}",
                "",
                f"- Risk level: `{item['risk_level']}`",
                f"- Expected evidence: {item['expected_evidence']}",
                f"- Stop rule: {item['stop_rule']}",
                "",
                "```text",
                item["command"],
                "```",
                "",
            ]
        )
    lines.extend(["## Acceptance Criteria", ""])
    for item in pack["acceptance_criteria"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Paper Claim Boundary", ""])
    for item in pack["paper_boundaries"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Hard Stops", ""])
    for item in pack["hard_stops"]:
        lines.append(f"- {item}")
    lines.append("")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    pack = build_pack()
    output_json = Path(args.output_json)
    output_md = Path(args.output_md)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(pack, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(output_md, pack)
    summary = {
        "overall_status": pack["overall_status"],
        "candidate_run_ready_after_explicit_approval": pack["candidate_run_ready_after_explicit_approval"],
        "expected_images": pack["expected_images"],
        "current_intake_status": pack["current_intake"]["status"],
        "prerequisites_satisfied": sum(1 for item in pack["prerequisites"] if item["satisfied"]),
        "prerequisite_count": len(pack["prerequisites"]),
        "no_experiment_executed": pack["no_experiment_executed"],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
