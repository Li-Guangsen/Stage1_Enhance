from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Sequence


THIS_DIR = Path(__file__).resolve().parent
METRICS_DIR = THIS_DIR.parent
PROJECT_ROOT = METRICS_DIR.parent
DEFAULT_MYEDGE_ROOT = Path(r"D:\Desktop\MyEdgeCodex")
DEFAULT_DATE = datetime.now().date().strftime("%Y%m%d")
DEFAULT_OUTPUT_MD = PROJECT_ROOT / "docs" / f"stage1_myedge_p1_execution_readiness_{DEFAULT_DATE}_cn.md"
DEFAULT_OUTPUT_JSON = PROJECT_ROOT / "docs" / f"stage1_myedge_p1_execution_readiness_{DEFAULT_DATE}_cn.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build a read-only Stage1-side readiness package for the future MyEdge P1 "
            "fixed-detector coupling execution. This script does not run staging, sampling, "
            "eval.py, show.py, report sync, or metric recomputation."
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


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


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


def as_int(value: object, default: int = -1) -> int:
    if value is None:
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def table_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def extract_match(text: str, pattern: str) -> str:
    match = re.search(pattern, text, flags=re.IGNORECASE)
    return match.group(1).strip() if match else ""


def extract_confirmation_phrase(project_state_text: str) -> str:
    match = re.search(r"confirmation_phrase:\s*(.+)", project_state_text)
    return match.group(1).strip() if match else "我确认执行高风险操作"


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
    execution_scope: str,
    command: str,
    risk_level: str,
    expected_evidence: str,
    stop_rule: str,
) -> Dict[str, str]:
    return {
        "step_id": step_id,
        "title": title,
        "execution_scope": execution_scope,
        "command": command,
        "risk_level": risk_level,
        "expected_evidence": expected_evidence,
        "stop_rule": stop_rule,
    }


def build_pack(myedge_root: Path) -> Dict[str, object]:
    paths = {
        "coupling_status": PROJECT_ROOT / "docs" / "stage1_myedge_coupling_status_20260525_cn.json",
        "next_gate_board": PROJECT_ROOT / "docs" / "stage1_myedge_next_gate_board_20260525_cn.json",
        "myedge_project_state": myedge_root / "project-state.yaml",
        "command_sheet": myedge_root
        / "docs"
        / "research_contracts"
        / "stage1_myedge_coupling_p1_execution_command_sheet_v1.md",
        "minimum_matrix_sheet": myedge_root
        / "docs"
        / "research_contracts"
        / "stage1_myedge_coupling_minimum_matrix_run_sheet_v1.md",
        "manifest": myedge_root
        / "docs"
        / "paper_assets"
        / "stage1_coupling"
        / "stage1_myedge_168_coupling_manifest_20260524.csv",
        "preflight": myedge_root
        / "docs"
        / "paper_assets"
        / "stage1_coupling"
        / "p1_preflight_20260524.json",
        "intake_pending": myedge_root
        / "docs"
        / "paper_assets"
        / "stage1_coupling"
        / "p1_results_intake_pending_20260525.json",
        "sync_status": myedge_root
        / "docs"
        / "paper_assets"
        / "stage1_coupling"
        / "p1_report_asset_sync_status_20260525.json",
        "baseline_freeze": myedge_root
        / "docs"
        / "paper_assets"
        / "stage1_coupling"
        / "diffusionedge_baseline_p1_asset_freeze_20260525.md",
        "prepare_script": myedge_root / "docs" / "paper_assets" / "scripts" / "prepare_stage1_coupling_p1_assets.py",
        "intake_script": myedge_root / "docs" / "paper_assets" / "scripts" / "intake_stage1_coupling_p1_results.py",
        "sync_script": myedge_root / "docs" / "paper_assets" / "scripts" / "sync_stage1_coupling_p1_report_assets.py",
    }

    coupling_status = read_json(paths["coupling_status"])
    next_gate_board = read_json(paths["next_gate_board"])
    preflight = read_json(paths["preflight"])
    intake_pending = read_json(paths["intake_pending"])
    sync_status = read_json(paths["sync_status"])
    baseline_freeze_text = read_text(paths["baseline_freeze"])
    project_state_text = read_text(paths["myedge_project_state"])

    staging_root = Path(str(preflight.get("staging_root", "")))
    msfi_output_root = Path(str(preflight.get("msfi_output_root", "")))
    baseline_output_root = Path(str(preflight.get("baseline_output_root", "")))
    msfi_config = Path(str(preflight.get("msfi_config_template", "")))
    baseline_config = Path(str(preflight.get("baseline_config_template", "")))
    baseline_checkpoint_size = extract_match(baseline_freeze_text, r"Checkpoint size\s*\|\s*`?([0-9]+)`?\s*bytes")
    baseline_checkpoint_sha256 = extract_match(
        baseline_freeze_text, r"Checkpoint SHA256\s*\|\s*`?([A-Fa-f0-9]{64})`?"
    )
    confirmation_phrase = extract_confirmation_phrase(project_state_text)

    expected_count = int(intake_pending.get("expected_count") or preflight.get("row_count") or 0)
    runs: Sequence[Dict[str, object]] = intake_pending.get("runs", []) if isinstance(intake_pending.get("runs"), list) else []

    prerequisites: List[Dict[str, object]] = [
        prerequisite(
            "P01",
            "Stage1/MyEdge coupling manifest exists and has 168 rows",
            paths["manifest"].exists() and int(preflight.get("row_count") or 0) == 168,
            f"{evidence(paths['manifest'], myedge_root)}; row_count={preflight.get('row_count')}",
            "Stop before staging or sampling; regenerate/read-only audit the manifest first.",
        ),
        prerequisite(
            "P02",
            "All 168 Stage1 Final files and GT references are available",
            as_int(preflight.get("missing_stage1_final_count")) == 0
            and as_int(preflight.get("missing_gt_count")) == 0
            and as_int(preflight.get("duplicate_target_count")) == 0,
            (
                f"missing_stage1_final={preflight.get('missing_stage1_final_count')}; "
                f"missing_gt={preflight.get('missing_gt_count')}; duplicate_target={preflight.get('duplicate_target_count')}"
            ),
            "Stop before staging; inspect missing paths or duplicate target stems.",
        ),
        prerequisite(
            "P03",
            "Staging root has not been populated",
            not bool(preflight.get("staging_exists"))
            and int(preflight.get("staging_file_count") or 0) == 0
            and not bool(preflight.get("write_staging_executed")),
            f"{rel(staging_root, myedge_root)}; exists={preflight.get('staging_exists')}; file_count={preflight.get('staging_file_count')}",
            "Stop and inspect whether a prior staging run exists before writing/copying files.",
        ),
        prerequisite(
            "P04",
            "MSFI P1 config template exists and planned output root is absent",
            msfi_config.exists()
            and bool(preflight.get("ready_for_msfi_p1_after_approval"))
            and not bool(preflight.get("msfi_output_root_exists"))
            and not bool(preflight.get("msfi_output_root_nonempty")),
            (
                f"config={evidence(msfi_config, myedge_root)}; output={rel(msfi_output_root, myedge_root)}; "
                f"root_exists={preflight.get('msfi_output_root_exists')}; root_nonempty={preflight.get('msfi_output_root_nonempty')}"
            ),
            "Stop before sampling; do not overwrite a populated MSFI P1 root.",
        ),
        prerequisite(
            "P05",
            "DiffusionEdge baseline P1 config and frozen checkpoint evidence exist; planned output root is absent",
            baseline_config.exists()
            and bool(preflight.get("baseline_asset_freeze_exists"))
            and bool(preflight.get("ready_for_baseline_p1_after_approval"))
            and not bool(preflight.get("baseline_output_root_exists"))
            and not bool(preflight.get("baseline_output_root_nonempty")),
            (
                f"config={evidence(baseline_config, myedge_root)}; freeze={evidence(paths['baseline_freeze'], myedge_root)}; "
                f"checkpoint_size={baseline_checkpoint_size or 'not parsed'}; sha256={baseline_checkpoint_sha256 or 'not parsed'}; "
                f"output={rel(baseline_output_root, myedge_root)}; root_exists={preflight.get('baseline_output_root_exists')}"
            ),
            "Stop before baseline sampling; verify checkpoint size/hash or document any mismatch.",
        ),
        prerequisite(
            "P06",
            "P1 intake and report sync are still not-started check artifacts",
            intake_pending.get("overall_status") == "not_started"
            and bool(intake_pending.get("no_inference_or_eval"))
            and sync_status.get("overall_status") == "not_started"
            and not bool(sync_status.get("write_assets")),
            (
                f"intake_status={intake_pending.get('overall_status')}; intake_no_inference_or_eval={intake_pending.get('no_inference_or_eval')}; "
                f"sync_status={sync_status.get('overall_status')}; sync_write_assets={sync_status.get('write_assets')}"
            ),
            "Stop before writing paper claims; no P1 metric evidence exists yet.",
        ),
        prerequisite(
            "P07",
            "Stage1-side gate board still marks MyEdge P1 as ready only after explicit approval",
            "G05" in str(next_gate_board) and str(coupling_status.get("p1_results_intake", {}).get("overall_status")) == "not_started",
            (
                f"gate_board={evidence(paths['next_gate_board'])}; "
                f"coupling_p1_status={coupling_status.get('p1_results_intake', {}).get('overall_status')}"
            ),
            "Stop and reconcile Stage1/MyEdge status files before execution.",
        ),
    ]

    all_prerequisites_satisfied = all(bool(item["satisfied"]) for item in prerequisites)
    ready_for_approval = (
        all_prerequisites_satisfied
        and bool(preflight.get("ready_for_msfi_p1_after_approval"))
        and bool(preflight.get("ready_for_baseline_p1_after_approval"))
        and intake_pending.get("overall_status") == "not_started"
    )
    if intake_pending.get("overall_status") == "complete_with_report_assets":
        overall_status = "superseded_by_completed_p1"
    else:
        overall_status = "ready_for_approval_not_executed" if ready_for_approval else "not_ready_reconcile_first"

    future_steps = [
        future_step(
            "S0",
            "Refresh P1 preflight/config templates and root checks",
            "Windows PowerShell, D:/Desktop/MyEdgeCodex",
            "D:/Desktop/DeepLearning/my_env/python.exe docs/paper_assets/scripts/prepare_stage1_coupling_p1_assets.py --write-config",
            "guarded_write_config_only",
            "Updated config/preflight files and confirmed staging/output roots remain absent or empty.",
            "Do not proceed if root checks fail or config changes are unexpected.",
        ),
        future_step(
            "S1",
            "Populate 168 Stage1 Final inputs under original MyEdge stems",
            "Windows PowerShell, D:/Desktop/MyEdgeCodex",
            "D:/Desktop/DeepLearning/my_env/python.exe docs/paper_assets/scripts/prepare_stage1_coupling_p1_assets.py --write-config --write-staging",
            "high_risk_writes_staging_files",
            "168 PNG files under stage1_coupling_inputs/stage1_final_168_original_stem_20260524.",
            f"Requires user phrase `{confirmation_phrase}`; stop if staged PNG count is not 168.",
        ),
        future_step(
            "S2",
            "Run Stage1 Final -> MSFI 50k sampling",
            "Windows PowerShell, D:/Desktop/MyEdgeCodex",
            (
                "$msfiRoot = \"D:\\Desktop\\MyEdgeCodex\\output_test\\stage1_coupling\\msfi_50k\\stage1_final_168_p1_20260524\"\n"
                "New-Item -ItemType Directory -Force -Path \"$msfiRoot\\logs\" | Out-Null\n"
                "D:/Desktop/DeepLearning/my_env/python.exe sample_cond_ldm.py --cfg configs/stage1_coupling/msfi_stage1_final_168_p1_20260524.yaml 2>&1 |\n"
                "  Tee-Object -FilePath \"$msfiRoot\\logs\\sample.log\""
            ),
            "high_risk_sampling",
            "MSFI P1 png/mat counts are 168 and logs/sample.log exists.",
            f"Requires user phrase `{confirmation_phrase}`; stop if png/mat counts differ from 168.",
        ),
        future_step(
            "S3",
            "Run Stage1 Final -> DiffusionEdge baseline 50k sampling",
            "Windows PowerShell, D:/Desktop/MyEdgeCodex",
            (
                "$baseRoot = \"D:\\Desktop\\MyEdgeCodex\\output_test\\stage1_coupling\\diffusionedge_baseline_50k\\stage1_final_168_p1_20260525\"\n"
                "New-Item -ItemType Directory -Force -Path \"$baseRoot\\logs\" | Out-Null\n"
                "D:/Desktop/DeepLearning/my_env/python.exe sample_cond_ldm.py --cfg configs/stage1_coupling/diffusionedge_baseline_stage1_final_168_p1_20260525.yaml 2>&1 |\n"
                "  Tee-Object -FilePath \"$baseRoot\\logs\\sample.log\""
            ),
            "high_risk_sampling",
            "Baseline P1 png/mat counts are 168 and logs/sample.log exists.",
            f"Requires user phrase `{confirmation_phrase}`; stop if checkpoint hash/size differs or png/mat counts differ from 168.",
        ),
        future_step(
            "S4",
            "Evaluate MSFI P1 with eval.py/show.py",
            "WSL, /mnt/d/Desktop/MyEdgeCodex/eval-edge-py",
            (
                "PY=/root/miniconda3/envs/myenv/bin/python; "
                "MSFI_ROOT=/mnt/d/Desktop/MyEdgeCodex/output_test/stage1_coupling/msfi_50k/stage1_final_168_p1_20260524; "
                '"$PY" eval.py ../output_test/stage1_coupling/msfi_50k/stage1_final_168_p1_20260524 -d ALGAE -nw -f 2>&1 | tee "$MSFI_ROOT/logs/eval.log"; '
                '"$PY" show.py ../output_test/stage1_coupling/msfi_50k/stage1_final_168_p1_20260524 -f 2>&1 | tee "$MSFI_ROOT/logs/show.log"'
            ),
            "high_risk_evaluation",
            "nms count 168, mat-eval/eval_bdry.txt, nms-eval/eval_bdry.txt, logs/eval.log and logs/show.log.",
            f"Requires user phrase `{confirmation_phrase}`; stop if any eval/show artifact is missing.",
        ),
        future_step(
            "S5",
            "Evaluate DiffusionEdge baseline P1 with eval.py/show.py",
            "WSL, /mnt/d/Desktop/MyEdgeCodex/eval-edge-py",
            (
                "PY=/root/miniconda3/envs/myenv/bin/python; "
                "BASE_ROOT=/mnt/d/Desktop/MyEdgeCodex/output_test/stage1_coupling/diffusionedge_baseline_50k/stage1_final_168_p1_20260525; "
                '"$PY" eval.py ../output_test/stage1_coupling/diffusionedge_baseline_50k/stage1_final_168_p1_20260525 -d ALGAE -nw -f 2>&1 | tee "$BASE_ROOT/logs/eval.log"; '
                '"$PY" show.py ../output_test/stage1_coupling/diffusionedge_baseline_50k/stage1_final_168_p1_20260525 -f 2>&1 | tee "$BASE_ROOT/logs/show.log"'
            ),
            "high_risk_evaluation",
            "nms count 168, mat-eval/eval_bdry.txt, nms-eval/eval_bdry.txt, logs/eval.log and logs/show.log.",
            f"Requires user phrase `{confirmation_phrase}`; stop if any eval/show artifact is missing.",
        ),
        future_step(
            "S6",
            "Run read-only P1 results intake",
            "Windows PowerShell, D:/Desktop/MyEdgeCodex",
            "D:/Desktop/DeepLearning/my_env/python.exe docs/paper_assets/scripts/intake_stage1_coupling_p1_results.py",
            "read_only_intake_after_results_exist",
            "A non-pending P1 intake report with both runs core_complete=true.",
            "Do not update paper claims unless intake confirms complete core outputs.",
        ),
        future_step(
            "S7",
            "Generate visualization-only report assets after core results are ready",
            "Windows PowerShell, D:/Desktop/MyEdgeCodex",
            "D:/Desktop/DeepLearning/my_env/python.exe docs/paper_assets/scripts/sync_stage1_coupling_p1_report_assets.py --write-assets",
            "guarded_report_asset_write",
            "white/overlay/error_map/manifest.csv/run_report.md for each P1 root.",
            "Only run after intake reports core_results_ready_for_report_sync or equivalent complete state.",
        ),
    ]

    acceptance_criteria = [
        "Staging directory contains exactly 168 PNG files with original MyEdge stems.",
        "Both P1 output roots contain exactly 168 PNG and 168 MAT files.",
        "Both P1 output roots contain exactly 168 NMS PNG files after WSL evaluation.",
        "Both P1 roots contain mat-eval/eval_bdry.txt and nms-eval/eval_bdry.txt.",
        "Both P1 roots contain logs/sample.log, logs/eval.log and logs/show.log.",
        "Read-only intake reports both runs core_complete=true with parsed ODS/OIS/AP and AC where available.",
        "Report sync is run only after core completion and then produces manifest.csv, run_report.md, white/, overlay/ and error_map/.",
    ]
    paper_boundaries = [
        "Currently allowed: write that P1 is prepared and ready only after explicit high-risk approval.",
        "Currently forbidden: claim Stage1 Final improves ODS/OIS/AP/AC, false-edge suppression, morphology consistency or downstream edge detection.",
        "After results exist: compare Stage1 Final P1 only against existing raw-input anchors in MyEdge.",
        "If ODS/OIS improve but AP drops, write an operating-point/ranking trade-off, not comprehensive superiority.",
        "If only one detector benefits, write detector-specific or interaction-specific support only.",
    ]

    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "stage1_root": str(PROJECT_ROOT),
        "myedge_root": str(myedge_root),
        "no_experiment_executed": True,
        "overall_status": overall_status,
        "confirmation_phrase": confirmation_phrase,
        "expected_count": expected_count,
        "source_status_files": {name: str(path) for name, path in paths.items()},
        "current_preflight": {
            "row_count": preflight.get("row_count"),
            "staging_exists": preflight.get("staging_exists"),
            "staging_file_count": preflight.get("staging_file_count"),
            "write_staging_executed": preflight.get("write_staging_executed"),
            "msfi_output_root_exists": preflight.get("msfi_output_root_exists"),
            "baseline_output_root_exists": preflight.get("baseline_output_root_exists"),
            "ready_for_msfi_p1_after_approval": preflight.get("ready_for_msfi_p1_after_approval"),
            "ready_for_baseline_p1_after_approval": preflight.get("ready_for_baseline_p1_after_approval"),
            "no_inference_or_eval": preflight.get("no_inference_or_eval"),
        },
        "current_intake": {
            "overall_status": intake_pending.get("overall_status"),
            "no_inference_or_eval": intake_pending.get("no_inference_or_eval"),
            "run_count": len(runs),
            "runs": [
                {
                    "run_id": run.get("run_id"),
                    "status": run.get("status"),
                    "root_exists": run.get("root_exists"),
                    "core_complete": run.get("core_complete"),
                    "report_complete": run.get("report_complete"),
                    "counts": run.get("counts"),
                    "required_file_exists": run.get("required_file_exists"),
                }
                for run in runs
            ],
        },
        "baseline_checkpoint_record": {
            "size_bytes": baseline_checkpoint_size,
            "sha256": baseline_checkpoint_sha256,
            "source": str(paths["baseline_freeze"]),
            "hash_recomputed_by_this_script": False,
        },
        "prerequisites": prerequisites,
        "future_execution_sequence": future_steps,
        "acceptance_criteria": acceptance_criteria,
        "paper_boundaries": paper_boundaries,
        "hard_stops": [
            "Do not run S1-S5 without explicit MyEdge high-risk confirmation.",
            "Do not create or populate P1 output roots before confirming they are absent or empty.",
            "If P1 intake is complete_with_report_assets, treat this readiness pack as superseded and use the coupling status snapshot instead.",
            "Do not treat this readiness package as a result artifact.",
        ],
    }


def write_markdown(path: Path, pack: Dict[str, object], myedge_root: Path) -> None:
    prereqs: Sequence[Dict[str, object]] = pack["prerequisites"]
    steps: Sequence[Dict[str, str]] = pack["future_execution_sequence"]
    current_intake: Dict[str, object] = pack["current_intake"]
    baseline_record: Dict[str, object] = pack["baseline_checkpoint_record"]
    lines: List[str] = [
        "# Stage1-to-MyEdge P1 fixed-detector execution readiness pack",
        "",
        f"日期：{datetime.now().date().isoformat()}",
        "",
        "本文是 Stage1 侧的 MyEdge P1 执行准备包。它只读取现有状态文件并写入交接文档，不执行 staging、sampling、`eval.py`、`show.py`、report sync 或指标重算。",
        "",
        "## Summary",
        "",
        f"- Overall status: `{pack['overall_status']}`",
        f"- Expected image count: `{pack['expected_count']}`",
        f"- No experiment executed by this script: `{pack['no_experiment_executed']}`",
        f"- MyEdge high-risk confirmation phrase: `{pack['confirmation_phrase']}`",
        f"- Current P1 intake status: `{current_intake.get('overall_status')}`",
        f"- Current intake run count: `{current_intake.get('run_count')}`",
        "- Note: if overall status is `superseded_by_completed_p1`, use the coupling status snapshot and P1 run reports as result evidence.",
        "",
        "## Current Evidence",
        "",
        f"- MyEdge command sheet: {evidence(Path(pack['source_status_files']['command_sheet']), myedge_root)}",
        f"- Minimum matrix run sheet: {evidence(Path(pack['source_status_files']['minimum_matrix_sheet']), myedge_root)}",
        f"- P1 preflight JSON: {evidence(Path(pack['source_status_files']['preflight']), myedge_root)}",
        f"- P1 pending intake JSON: {evidence(Path(pack['source_status_files']['intake_pending']), myedge_root)}",
        f"- P1 report sync status JSON: {evidence(Path(pack['source_status_files']['sync_status']), myedge_root)}",
        f"- Stage1 coupling snapshot: {evidence(Path(pack['source_status_files']['coupling_status']))}",
        f"- Stage1 gate board: {evidence(Path(pack['source_status_files']['next_gate_board']))}",
        "",
        "## Baseline Checkpoint Record",
        "",
        "| Item | Value |",
        "|---|---|",
        f"| Size bytes | `{baseline_record.get('size_bytes') or 'not parsed'}` |",
        f"| SHA256 | `{baseline_record.get('sha256') or 'not parsed'}` |",
        f"| Source | `{rel(Path(str(baseline_record.get('source'))), myedge_root)}` |",
        f"| Recomputed by this script | `{baseline_record.get('hash_recomputed_by_this_script')}` |",
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
            "以下步骤只是未来执行顺序。除 S6 的只读 intake 外，任何 staging、sampling、WSL evaluation、report asset 写入都必须先回到 MyEdge 项目规则并获得明确高风险确认。",
            "",
        ]
    )
    for item in steps:
        lines.extend(
            [
                f"### {item['step_id']} - {item['title']}",
                "",
                f"- Execution scope: `{item['execution_scope']}`",
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

    lines.extend(
        [
            "## Acceptance Criteria",
            "",
        ]
    )
    for item in pack["acceptance_criteria"]:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## Paper Claim Boundary",
            "",
        ]
    )
    for item in pack["paper_boundaries"]:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## Hard Stops",
            "",
        ]
    )
    for item in pack["hard_stops"]:
        lines.append(f"- {item}")
    lines.append("")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    myedge_root = Path(args.myedge_root)
    pack = build_pack(myedge_root)
    output_json = Path(args.output_json)
    output_md = Path(args.output_md)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(pack, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(output_md, pack, myedge_root)
    summary = {
        "overall_status": pack["overall_status"],
        "expected_count": pack["expected_count"],
        "no_experiment_executed": pack["no_experiment_executed"],
        "current_intake_status": pack["current_intake"]["overall_status"],
        "prerequisites_satisfied": sum(1 for item in pack["prerequisites"] if item["satisfied"]),
        "prerequisite_count": len(pack["prerequisites"]),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
