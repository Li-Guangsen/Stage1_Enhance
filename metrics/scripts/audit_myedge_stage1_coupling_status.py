from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List


THIS_DIR = Path(__file__).resolve().parent
METRICS_DIR = THIS_DIR.parent
PROJECT_ROOT = METRICS_DIR.parent

DEFAULT_MYEDGE_ROOT = Path(r"D:\Desktop\MyEdgeCodex")
DEFAULT_OUTPUT_JSON = PROJECT_ROOT / "docs" / "stage1_myedge_coupling_status_20260525_cn.json"
DEFAULT_OUTPUT_MD = PROJECT_ROOT / "docs" / "stage1_myedge_coupling_status_20260525_cn.md"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Read MyEdgeCodex Stage1-coupling planning assets and write a Stage1-side status snapshot. "
            "This script is read-only with respect to MyEdgeCodex and does not run sampling or evaluation."
        )
    )
    parser.add_argument("--myedge-root", default=str(DEFAULT_MYEDGE_ROOT))
    parser.add_argument("--output-json", default=str(DEFAULT_OUTPUT_JSON))
    parser.add_argument("--output-md", default=str(DEFAULT_OUTPUT_MD))
    return parser.parse_args()


def read_json(path: Path) -> Dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def rel_or_abs(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root)).replace("\\", "/")
    except ValueError:
        return str(path)


def build_snapshot(myedge_root: Path) -> Dict[str, object]:
    files = {
        "myedge_readme": myedge_root / "readme.md",
        "myedge_project_state": myedge_root / "project-state.yaml",
        "coupling_manifest_summary": myedge_root
        / "docs"
        / "paper_assets"
        / "stage1_coupling"
        / "stage1_myedge_168_coupling_manifest_20260524.summary.json",
        "p1_preflight": myedge_root / "docs" / "paper_assets" / "stage1_coupling" / "p1_preflight_20260524.json",
        "p1_results_intake": myedge_root
        / "docs"
        / "paper_assets"
        / "stage1_coupling"
        / "p1_results_intake_pending_20260525.json",
        "p1_report_asset_sync": myedge_root
        / "docs"
        / "paper_assets"
        / "stage1_coupling"
        / "p1_report_asset_sync_status_20260525.json",
        "p1_execution_command_sheet": myedge_root
        / "docs"
        / "research_contracts"
        / "stage1_myedge_coupling_p1_execution_command_sheet_v1.md",
        "minimum_matrix_run_sheet": myedge_root
        / "docs"
        / "research_contracts"
        / "stage1_myedge_coupling_minimum_matrix_run_sheet_v1.md",
    }

    missing_files = [key for key, path in files.items() if not path.exists()]
    if missing_files:
        return {
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "myedge_root": str(myedge_root),
            "overall_status": "missing_required_myedge_assets",
            "missing_files": {key: str(files[key]) for key in missing_files},
            "no_training_sampling_or_eval": True,
        }

    manifest = read_json(files["coupling_manifest_summary"])
    preflight = read_json(files["p1_preflight"])
    intake = read_json(files["p1_results_intake"])
    sync = read_json(files["p1_report_asset_sync"])

    p1_roots_exist = any(bool(run.get("root_exists")) for run in intake.get("runs", []))
    p1_any_metrics = any(bool(run.get("mat_eval") or run.get("nms_eval") or run.get("ac_from_show")) for run in intake.get("runs", []))

    intake_status = str(intake.get("overall_status"))
    if intake_status == "not_started":
        interpretation_boundary = (
            "This Stage1-side snapshot only mirrors existing MyEdgeCodex planning/intake files. "
            "It does not execute training, sampling, eval.py, show.py, Stage1 full-pool enhancement, or metric recomputation. "
            "P1 status not_started means no Stage1 downstream edge benefit can be claimed."
        )
    elif intake_status == "complete_with_report_assets":
        interpretation_boundary = (
            "This Stage1-side snapshot mirrors completed MyEdgeCodex P1 intake/report assets. "
            "It does not execute training, sampling, eval.py, show.py, Stage1 full-pool enhancement, or metric recomputation. "
            "P1 metrics may be cited only with their fixed-detector, 168-image, Stage1-Final-input boundary."
        )
    else:
        interpretation_boundary = (
            "This Stage1-side snapshot only mirrors existing MyEdgeCodex planning/intake files. "
            "It does not execute training, sampling, eval.py, show.py, Stage1 full-pool enhancement, or metric recomputation. "
            "Do not claim Stage1 downstream edge benefit unless P1 intake/report assets are complete and interpreted with boundaries."
        )

    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "myedge_root": str(myedge_root),
        "overall_status": "p1_not_started" if intake_status == "not_started" else intake_status,
        "no_training_sampling_or_eval": True,
        "source_files": {key: rel_or_abs(path, myedge_root) for key, path in files.items()},
        "manifest": {
            "rows": manifest.get("row_count"),
            "gt_missing_count": manifest.get("gt_missing_count"),
            "all_stage_rows_complete": manifest.get("all_stage_rows_complete"),
            "stage_missing_counts": manifest.get("stage_missing_counts"),
            "msfi_reference_missing_count": manifest.get("msfi_reference_missing_count"),
            "diffusionedge_reference_missing_count": manifest.get("diffusionedge_reference_missing_count"),
            "planned_staging_note": manifest.get("planned_staging_note"),
        },
        "preflight": {
            "staging_exists": preflight.get("staging_exists"),
            "staging_file_count": preflight.get("staging_file_count"),
            "write_staging_executed": preflight.get("write_staging_executed"),
            "missing_stage1_final_count": preflight.get("missing_stage1_final_count"),
            "missing_gt_count": preflight.get("missing_gt_count"),
            "duplicate_target_count": preflight.get("duplicate_target_count"),
            "msfi_config_template": preflight.get("msfi_config_template"),
            "msfi_output_root_exists": preflight.get("msfi_output_root_exists"),
            "ready_for_msfi_p1_after_approval": preflight.get("ready_for_msfi_p1_after_approval"),
            "baseline_asset_freeze_exists": preflight.get("baseline_asset_freeze_exists"),
            "baseline_config_template_exists": preflight.get("baseline_config_template_exists"),
            "baseline_output_root_exists": preflight.get("baseline_output_root_exists"),
            "ready_for_baseline_p1_after_approval": preflight.get("ready_for_baseline_p1_after_approval"),
            "no_inference_or_eval": preflight.get("no_inference_or_eval"),
        },
        "p1_results_intake": {
            "overall_status": intake.get("overall_status"),
            "expected_count": intake.get("expected_count"),
            "p1_roots_exist": p1_roots_exist,
            "p1_any_metrics": p1_any_metrics,
            "runs": [
                {
                    "run_id": run.get("run_id"),
                    "detector": run.get("detector"),
                    "root": run.get("root"),
                    "status": run.get("status"),
                    "root_exists": run.get("root_exists"),
                    "counts": run.get("counts"),
                    "mat_eval": run.get("mat_eval"),
                    "nms_eval": run.get("nms_eval"),
                    "ac_from_show": run.get("ac_from_show"),
                }
                for run in intake.get("runs", [])
            ],
        },
        "p1_report_asset_sync": {
            "overall_status": sync.get("overall_status"),
            "write_assets": sync.get("write_assets"),
            "runs": [
                {
                    "run_id": run.get("run_id"),
                    "status": run.get("status"),
                    "core_complete": run.get("core_complete"),
                    "report_assets_complete": run.get("report_assets_complete"),
                    "action": run.get("action"),
                }
                for run in sync.get("runs", [])
            ],
        },
        "interpretation_boundary": interpretation_boundary,
    }


def write_md(path: Path, snapshot: Dict[str, object]) -> None:
    manifest = snapshot.get("manifest", {})
    preflight = snapshot.get("preflight", {})
    intake = snapshot.get("p1_results_intake", {})
    sync = snapshot.get("p1_report_asset_sync", {})

    lines: List[str] = [
        "# Stage1 -> MyEdge coupling status snapshot",
        "",
        f"日期：{datetime.now().date().isoformat()}",
        "",
        "本文是 Stage1Codex 侧对 MyEdgeCodex 当前 Stage1 coupling 资产的只读镜像摘要，不是实验结果。",
        "",
        "## Summary",
        "",
        f"- MyEdge root: `{snapshot.get('myedge_root')}`",
        f"- Overall status: `{snapshot.get('overall_status')}`",
        f"- No training/sampling/eval executed by this script: `{snapshot.get('no_training_sampling_or_eval')}`",
        "",
        "## 168-image Manifest",
        "",
        f"- Rows: `{manifest.get('rows')}`",
        f"- GT missing: `{manifest.get('gt_missing_count')}`",
        f"- All Stage1 stages complete: `{manifest.get('all_stage_rows_complete')}`",
        f"- MSFI raw-reference missing: `{manifest.get('msfi_reference_missing_count')}`",
        f"- DiffusionEdge raw-reference missing: `{manifest.get('diffusionedge_reference_missing_count')}`",
        f"- Staging note: `{manifest.get('planned_staging_note')}`",
        "",
        "## P1 Preflight",
        "",
        f"- Staging exists: `{preflight.get('staging_exists')}`",
        f"- Staging file count: `{preflight.get('staging_file_count')}`",
        f"- Write staging executed: `{preflight.get('write_staging_executed')}`",
        f"- Missing Stage1 Final: `{preflight.get('missing_stage1_final_count')}`",
        f"- Missing GT: `{preflight.get('missing_gt_count')}`",
        f"- Duplicate target filenames: `{preflight.get('duplicate_target_count')}`",
        f"- Ready for MSFI P1 after approval: `{preflight.get('ready_for_msfi_p1_after_approval')}`",
        f"- Ready for DiffusionEdge baseline P1 after approval: `{preflight.get('ready_for_baseline_p1_after_approval')}`",
        "",
        "## P1 Result Intake",
        "",
        f"- Intake status: `{intake.get('overall_status')}`",
        f"- Expected count: `{intake.get('expected_count')}`",
        f"- P1 roots exist: `{intake.get('p1_roots_exist')}`",
        f"- P1 metrics present: `{intake.get('p1_any_metrics')}`",
        "",
        "| Run | Detector | Status | Root exists | mat-eval | nms-eval | AC |",
        "|---|---|---|---:|---|---|---|",
    ]
    for run in intake.get("runs", []):
        lines.append(
            "| `{run_id}` | {detector} | `{status}` | `{root_exists}` | `{mat_eval}` | `{nms_eval}` | `{ac}` |".format(
                run_id=run.get("run_id"),
                detector=run.get("detector"),
                status=run.get("status"),
                root_exists=run.get("root_exists"),
                mat_eval=run.get("mat_eval"),
                nms_eval=run.get("nms_eval"),
                ac=run.get("ac_from_show"),
            )
        )

    if intake.get("overall_status") == "complete_with_report_assets":
        boundary_lines = [
            "- 该快照只读取 MyEdgeCodex 已存在的 planning / intake / report asset 文件。",
            "- 当前 P1 已完成 report asset sync；P1 指标只能在 168 张、Stage1 Final 输入、固定 detector 的边界内引用。",
            "- P1 结果不能外推为 full2770、full502 或所有 Stage1 阶段的下游收益。",
            "- 若要证明 Stage1 不是普通 preprocessing，下一步仍需 stage-wise / generic enhancement control / degradation subset 矩阵。",
        ]
    else:
        boundary_lines = [
            "- 该快照只读取 MyEdgeCodex 已存在的 planning / intake 文件。",
            "- 当前 P1 为 `not_started`，不能写 Stage1 已提升 ODS/OIS/AP/AC。",
            "- 不能把该快照写成 pseudo-edge suppression、morphology consistency 或 downstream benefit 的结果证据。",
            "- 后续若执行 P1，必须在 MyEdgeCodex 侧按 command sheet 获得高风险确认后再 sampling/eval，并在接收脚本显示完整后再同步 Stage1 文档。",
        ]

    lines.extend(
        [
            "",
            "## Report Asset Sync",
            "",
            f"- Sync status: `{sync.get('overall_status')}`",
            f"- Write assets: `{sync.get('write_assets')}`",
            "",
            "## Boundary",
            "",
            *boundary_lines,
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    snapshot = build_snapshot(Path(args.myedge_root))
    output_json = Path(args.output_json)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
    write_md(Path(args.output_md), snapshot)
    print(json.dumps(snapshot, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
