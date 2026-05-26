from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Sequence


THIS_DIR = Path(__file__).resolve().parent
METRICS_DIR = THIS_DIR.parent
PROJECT_ROOT = METRICS_DIR.parent
DEFAULT_REVIEW_DIR = PROJECT_ROOT / "metrics" / "manifests" / "full_algae_dewatermark_v1_manual_review"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build a consolidated manual-review dashboard and queue for full_algae_dewatermark_v1. "
            "This is a review aid only; it does not fill reviewer decisions."
        )
    )
    parser.add_argument("--review-dir", default=str(DEFAULT_REVIEW_DIR))
    parser.add_argument("--date", default=datetime.now().date().strftime("%Y%m%d"))
    return parser.parse_args()


def read_json(path: Path) -> Dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_tsv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle, delimiter="\t")]


def write_tsv(path: Path, rows: Sequence[Dict[str, object]], fieldnames: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(rows)


def issue_target_sheet(issue_type: str) -> str:
    return {
        "decode_failure": "decode_failures_review.tsv",
        "exact_duplicate_group": "exact_duplicates_review.tsv",
        "near_duplicate_pair": "near_duplicates_review.tsv",
        "quality_outlier": "quality_outliers_review.tsv",
    }.get(issue_type, "all_manual_review_issues.tsv")


def priority_order(priority: str) -> int:
    return {"P0": 0, "P1": 1, "P2": 2}.get(priority, 99)


def issue_type_order(issue_type: str) -> int:
    return {
        "decode_failure": 0,
        "exact_duplicate_group": 1,
        "near_duplicate_pair": 2,
        "quality_outlier": 3,
    }.get(issue_type, 99)


def load_recommendations(review_dir: Path) -> List[Dict[str, str]]:
    pack_paths = [
        ("P0", review_dir / "p0_review_pack" / "p0_review_recommendations.tsv"),
        ("P1", review_dir / "p1_review_pack" / "p1_review_recommendations.tsv"),
        ("P2", review_dir / "p2_review_pack" / "p2_review_recommendations.tsv"),
    ]
    rows: List[Dict[str, str]] = []
    for pack_priority, path in pack_paths:
        for row in read_tsv(path):
            row = dict(row)
            row["source_pack"] = pack_priority
            row["target_review_sheet"] = issue_target_sheet(row.get("issue_type", ""))
            rows.append(row)
    rows.sort(key=lambda row: (priority_order(row.get("priority", "")), issue_type_order(row.get("issue_type", "")), row.get("issue_id", "")))
    return rows


def build_queue_rows(recommendations: Sequence[Dict[str, str]]) -> List[Dict[str, object]]:
    queue_rows: List[Dict[str, object]] = []
    for index, row in enumerate(recommendations, start=1):
        queue_rows.append(
            {
                "review_order": index,
                "issue_id": row.get("issue_id", ""),
                "priority": row.get("priority", ""),
                "issue_type": row.get("issue_type", ""),
                "source_pack": row.get("source_pack", ""),
                "target_review_sheet": row.get("target_review_sheet", ""),
                "relative_path": row.get("relative_path", ""),
                "related_paths": row.get("related_paths", ""),
                "evidence_summary": row.get("evidence_summary", ""),
                "machine_suggestion": row.get("machine_suggestion", ""),
                "suggestion_reason": row.get("suggestion_reason", ""),
                "preview_path": row.get("preview_path", ""),
                "review_status": row.get("review_status", ""),
                "reviewer_decision": row.get("reviewer_decision", ""),
            }
        )
    return queue_rows


def count_by(rows: Iterable[Dict[str, object]], field: str) -> Dict[str, int]:
    return dict(Counter(str(row.get(field, "")) for row in rows))


def markdown_count_table(title: str, counts: Dict[str, int]) -> List[str]:
    lines = [f"### {title}", "", "| Key | Count |", "| --- | ---: |"]
    for key, count in sorted(counts.items(), key=lambda item: item[0]):
        lines.append(f"| `{key}` | {count} |")
    lines.append("")
    return lines


def write_dashboard_md(
    path: Path,
    summary: Dict[str, object],
    validation: Dict[str, object],
    derived: Dict[str, object],
    outputs: Dict[str, str],
) -> None:
    lines = [
        "# full_algae_dewatermark_v1 manual review dashboard",
        "",
        f"日期：{datetime.now().date().isoformat()}",
        "",
        "本文是完整增强图像池人工复核的统一入口。它只整合 P0/P1/P2 复核辅助包和校验状态，不填写人工决策，不修改 manifest，不运行增强。",
        "",
        "## Current Status",
        "",
        f"- Overall review status: `{validation.get('overall_status', '')}`",
        f"- Total review rows: `{validation.get('total_rows', '')}`",
        f"- Pending rows: `{validation.get('pending_rows', '')}`",
        f"- Reviewed rows: `{validation.get('reviewed_rows', '')}`",
        f"- Invalid rows: `{validation.get('invalid_rows', '')}`",
        f"- Derived clean manifest allowed: `{derived.get('can_generate_clean_manifest', False)}`",
        f"- Unified queue status: `{summary['queue_status']}`",
        "",
        "## Outputs",
        "",
    ]
    for label, value in outputs.items():
        lines.append(f"- {label}: `{value}`")
    lines.append("")
    lines.extend(markdown_count_table("Priority Counts", summary["priority_counts"]))
    lines.extend(markdown_count_table("Issue Type Counts", summary["issue_type_counts"]))
    lines.extend(markdown_count_table("Machine Suggestion Counts", summary["machine_suggestion_counts"]))
    lines.extend(
        [
            "## Recommended Review Order",
            "",
            "1. 先处理 P0：4 个 decode failures 和 3 个 exact duplicate groups。",
            "2. 再处理 P1：近重复强候选和低清晰度、低边缘能量、低对比等关键质量异常。",
            "3. 最后处理 P2：其余近重复和质量异常候选。",
            "4. 每一行的最终人工决策必须写回 `target_review_sheet` 对应 TSV 的 `review_status`、`reviewer_decision`、`decision_reason`、`reviewer` 和 `review_date`。",
            "",
            "## Decision Template Workflow",
            "",
            "如果不想直接编辑 4 个 review sheets，可先生成并填写统一决策模板：",
            "",
            "```bat",
            "D:\\Desktop\\EdgeDetection\\my_env\\python.exe metrics\\scripts\\build_fullpool_manual_review_decision_template.py",
            "D:\\Desktop\\EdgeDetection\\my_env\\python.exe metrics\\scripts\\apply_fullpool_manual_review_decisions.py",
            "```",
            "",
            "第二条命令默认 dry-run，只生成 apply plan，不写回 review sheets。只有 dry-run 无 invalid 后，才允许显式传 `--apply`。",
            "",
            "## Commands After Manual Review",
            "",
            "```bat",
            "D:\\Desktop\\EdgeDetection\\my_env\\python.exe metrics\\scripts\\validate_fullpool_manual_review.py",
            "D:\\Desktop\\EdgeDetection\\my_env\\python.exe metrics\\scripts\\derive_fullpool_review_artifacts.py",
            "```",
            "",
            "只有 `overall_status=complete_validated` 且 `can_generate_clean_manifest=True` 时，才能把派生 clean manifest 或 split leakage guard 作为后续 full-pool 协议入口。",
            "",
            "## Boundary",
            "",
            "- `machine_suggestion` 只是复核建议，不是 `reviewer_decision`。",
            "- P0/P1/P2 复核包和本 dashboard 不会删除、转换或排除任何原图。",
            "- P1/P2 质量异常优先作为退化分层、失败案例、数据覆盖或有效难例候选，不是自动排除依据。",
            "- P1/P2 近重复优先作为 future split leakage guard 候选，不是自动删除依据。",
            "- 当前仍不能启动或声明 2770 张 full-pool 正式增强完成；full run 需要单独批准并通过接收脚本。",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    review_dir = Path(args.review_dir)
    validation = read_json(review_dir / "manual_review_validation_status_20260525.json")
    derived = read_json(review_dir / "derived_review_artifacts" / "review_artifacts_status_20260525.json")
    p0_summary = read_json(review_dir / "p0_review_pack" / "p0_review_pack_summary.json")
    p1_summary = read_json(review_dir / "p1_review_pack" / "p1_review_pack_summary.json")
    p2_summary = read_json(review_dir / "p2_review_pack" / "p2_review_pack_summary.json")

    recommendations = load_recommendations(review_dir)
    queue_rows = build_queue_rows(recommendations)
    queue_path = review_dir / "all_priority_review_queue.tsv"
    queue_fields = [
        "review_order",
        "issue_id",
        "priority",
        "issue_type",
        "source_pack",
        "target_review_sheet",
        "relative_path",
        "related_paths",
        "evidence_summary",
        "machine_suggestion",
        "suggestion_reason",
        "preview_path",
        "review_status",
        "reviewer_decision",
    ]
    write_tsv(queue_path, queue_rows, queue_fields)

    expected_total = int(validation.get("total_rows", 0))
    queue_status = "ready_pending_manual_review" if len(queue_rows) == expected_total else "count_mismatch_check_required"
    summary = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "queue_status": queue_status,
        "queue_rows": len(queue_rows),
        "expected_review_rows": expected_total,
        "priority_counts": count_by(queue_rows, "priority"),
        "issue_type_counts": count_by(queue_rows, "issue_type"),
        "machine_suggestion_counts": count_by(queue_rows, "machine_suggestion"),
        "pack_totals": {
            "P0": p0_summary.get("total_p0_rows", 0),
            "P1": p1_summary.get("total_p1_rows", 0),
            "P2": p2_summary.get("total_p2_rows", 0),
        },
        "validation_status": validation.get("overall_status", ""),
        "derived_status": derived.get("overall_status", ""),
        "can_generate_clean_manifest": derived.get("can_generate_clean_manifest", False),
        "queue_path": str(queue_path.relative_to(PROJECT_ROOT)),
        "boundary": (
            "This dashboard is a manual-review aid only. It does not fill reviewer decisions, "
            "change manifests, convert files, run enhancement, or replace formal 502/496 protocols."
        ),
    }
    summary_json_path = review_dir / f"manual_review_dashboard_{args.date}.json"
    summary_md_path = review_dir / f"manual_review_dashboard_{args.date}.md"
    summary_json_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    write_dashboard_md(
        summary_md_path,
        summary,
        validation,
        derived,
        {
            "unified review queue": str(queue_path.relative_to(PROJECT_ROOT)),
            "dashboard json": str(summary_json_path.relative_to(PROJECT_ROOT)),
            "review sheet": str(Path(validation.get("review_sheet", "")).relative_to(PROJECT_ROOT)) if validation.get("review_sheet") else "",
            "validation status": str((review_dir / "manual_review_validation_status_20260525.md").relative_to(PROJECT_ROOT)),
            "derived status": str((review_dir / "derived_review_artifacts" / "review_artifacts_status_20260525.md").relative_to(PROJECT_ROOT)),
        },
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
