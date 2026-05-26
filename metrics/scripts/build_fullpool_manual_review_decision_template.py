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
DEFAULT_REVIEW_DIR = PROJECT_ROOT / "metrics" / "manifests" / "full_algae_dewatermark_v1_manual_review"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build a fillable manual-review decision template for full_algae_dewatermark_v1. "
            "This does not fill or apply decisions."
        )
    )
    parser.add_argument("--review-dir", default=str(DEFAULT_REVIEW_DIR))
    parser.add_argument("--date", default=datetime.now().date().strftime("%Y%m%d"))
    return parser.parse_args()


def read_tsv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle, delimiter="\t")]


def write_tsv(path: Path, rows: Sequence[Dict[str, object]], fieldnames: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(rows)


def int_value(value: str) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 10**9


def build_template_rows(queue_rows: Sequence[Dict[str, str]], issue_rows: Sequence[Dict[str, str]]) -> List[Dict[str, object]]:
    issue_map = {row["issue_id"]: row for row in issue_rows}
    template_rows: List[Dict[str, object]] = []
    for row in sorted(queue_rows, key=lambda item: int_value(item.get("review_order", ""))):
        issue = issue_map.get(row.get("issue_id", ""), {})
        template_rows.append(
            {
                "review_order": row.get("review_order", ""),
                "issue_id": row.get("issue_id", ""),
                "priority": row.get("priority", ""),
                "issue_type": row.get("issue_type", ""),
                "target_review_sheet": row.get("target_review_sheet", ""),
                "relative_path": row.get("relative_path", ""),
                "related_paths": row.get("related_paths", ""),
                "top_level_folder": issue.get("top_level_folder", ""),
                "evidence_summary": row.get("evidence_summary", ""),
                "allowed_decisions": issue.get("allowed_decisions", ""),
                "recommended_review_action": issue.get("recommended_review_action", ""),
                "machine_suggestion": row.get("machine_suggestion", ""),
                "suggestion_reason": row.get("suggestion_reason", ""),
                "preview_path": row.get("preview_path", ""),
                "current_review_status": issue.get("review_status", ""),
                "current_reviewer_decision": issue.get("reviewer_decision", ""),
                "review_status_to_apply": "",
                "reviewer_decision_to_apply": "",
                "decision_reason_to_apply": "",
                "reviewer_to_apply": "",
                "review_date_to_apply": "",
                "reviewer_notes": "",
            }
        )
    return template_rows


def write_summary_md(path: Path, summary: Dict[str, object]) -> None:
    lines = [
        "# full_algae_dewatermark_v1 manual review decision template",
        "",
        f"日期：{datetime.now().date().isoformat()}",
        "",
        "本文档说明配套 TSV 模板的用途。模板用于人工填写决策，不是自动决策，不修改 review sheets，也不生成 clean manifest。",
        "",
        "## Outputs",
        "",
        f"- Decision template: `{summary['decision_template']}`",
        f"- Summary JSON: `{summary['summary_json']}`",
        "",
        "## Summary",
        "",
        f"- Template rows: `{summary['template_rows']}`",
        f"- Expected review rows: `{summary['expected_review_rows']}`",
        f"- Template status: `{summary['template_status']}`",
        f"- Priority counts: `{summary['priority_counts']}`",
        "",
        "## How To Fill",
        "",
        "- 只填写以下列：`review_status_to_apply`、`reviewer_decision_to_apply`、`decision_reason_to_apply`、`reviewer_to_apply`、`review_date_to_apply`、`reviewer_notes`。",
        "- `review_status_to_apply` 可填 `reviewed` 或 `needs_followup`；如果要保持未处理，留空。",
        "- `reviewer_decision_to_apply` 必须来自同一行的 `allowed_decisions`。",
        "- `review_date_to_apply` 使用 `YYYY-MM-DD`。",
        "- 填完后先 dry-run，不要直接 apply。",
        "",
        "```bat",
        "D:\\Desktop\\EdgeDetection\\my_env\\python.exe metrics\\scripts\\apply_fullpool_manual_review_decisions.py",
        "```",
        "",
        "只有 dry-run 无 invalid 后，才可以显式加 `--apply` 写回 review sheets。写回后仍必须运行 `validate_fullpool_manual_review.py` 和 `derive_fullpool_review_artifacts.py`。",
        "",
        "## Boundary",
        "",
        "- 本模板不替代人工判断。",
        "- 本模板中的 `machine_suggestion` 不是 `reviewer_decision`。",
        "- 任何决策在显式 `--apply` 前都不会写回 review sheets。",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    review_dir = Path(args.review_dir)
    queue_path = review_dir / "all_priority_review_queue.tsv"
    issue_path = review_dir / "all_manual_review_issues.tsv"
    queue_rows = read_tsv(queue_path)
    issue_rows = read_tsv(issue_path)
    template_rows = build_template_rows(queue_rows, issue_rows)
    fieldnames = [
        "review_order",
        "issue_id",
        "priority",
        "issue_type",
        "target_review_sheet",
        "relative_path",
        "related_paths",
        "top_level_folder",
        "evidence_summary",
        "allowed_decisions",
        "recommended_review_action",
        "machine_suggestion",
        "suggestion_reason",
        "preview_path",
        "current_review_status",
        "current_reviewer_decision",
        "review_status_to_apply",
        "reviewer_decision_to_apply",
        "decision_reason_to_apply",
        "reviewer_to_apply",
        "review_date_to_apply",
        "reviewer_notes",
    ]
    template_path = review_dir / "manual_review_decision_template.tsv"
    write_tsv(template_path, template_rows, fieldnames)
    priority_counts = Counter(row["priority"] for row in template_rows)
    template_status = "ready_for_human_fill" if len(template_rows) == len(issue_rows) else "count_mismatch_check_required"
    summary = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "template_status": template_status,
        "template_rows": len(template_rows),
        "expected_review_rows": len(issue_rows),
        "priority_counts": dict(sorted(priority_counts.items())),
        "decision_template": str(template_path.relative_to(PROJECT_ROOT)),
        "summary_json": str((review_dir / f"manual_review_decision_template_{args.date}.json").relative_to(PROJECT_ROOT)),
        "boundary": (
            "This template is for human decisions only. It does not apply decisions, change manifests, "
            "run enhancement, or replace formal 502/496 protocols."
        ),
    }
    summary_json_path = review_dir / f"manual_review_decision_template_{args.date}.json"
    summary_md_path = review_dir / f"manual_review_decision_template_{args.date}.md"
    summary_json_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    write_summary_md(summary_md_path, summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
