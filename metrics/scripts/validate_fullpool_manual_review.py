from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple


THIS_DIR = Path(__file__).resolve().parent
METRICS_DIR = THIS_DIR.parent
PROJECT_ROOT = METRICS_DIR.parent

DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Validate full_algae_dewatermark_v1 manual review sheets. "
            "This only checks review completeness and consistency; it does not change manifests."
        )
    )
    parser.add_argument(
        "--review-sheet",
        default=str(
            PROJECT_ROOT
            / "metrics"
            / "manifests"
            / "full_algae_dewatermark_v1_manual_review"
            / "all_manual_review_issues.tsv"
        ),
    )
    parser.add_argument(
        "--output-json",
        default=str(
            PROJECT_ROOT
            / "metrics"
            / "manifests"
            / "full_algae_dewatermark_v1_manual_review"
            / "manual_review_validation_status_20260525.json"
        ),
    )
    parser.add_argument(
        "--output-md",
        default=str(
            PROJECT_ROOT
            / "metrics"
            / "manifests"
            / "full_algae_dewatermark_v1_manual_review"
            / "manual_review_validation_status_20260525.md"
        ),
    )
    parser.add_argument(
        "--invalid-output",
        default=str(
            PROJECT_ROOT
            / "metrics"
            / "manifests"
            / "full_algae_dewatermark_v1_manual_review"
            / "manual_review_invalid_rows_20260525.tsv"
        ),
    )
    return parser.parse_args()


def read_tsv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle, delimiter="\t")]


def split_allowed_decisions(value: str) -> List[str]:
    return [item.strip() for item in value.split("|") if item.strip()]


def validate_row(row: Dict[str, str]) -> List[str]:
    errors: List[str] = []
    issue_id = row.get("issue_id", "")
    if not issue_id:
        errors.append("missing issue_id")
    status = row.get("review_status", "").strip()
    decision = row.get("reviewer_decision", "").strip()
    reason = row.get("decision_reason", "").strip()
    reviewer = row.get("reviewer", "").strip()
    review_date = row.get("review_date", "").strip()
    allowed = split_allowed_decisions(row.get("allowed_decisions", ""))

    if status not in {"pending", "reviewed", "needs_followup"}:
        errors.append(f"invalid review_status={status!r}")
        return errors

    if status == "pending":
        if any([decision, reason, reviewer, review_date]):
            errors.append("pending row should not contain decision fields")
        return errors

    if not decision:
        errors.append("reviewer_decision required for non-pending row")
    elif allowed and decision not in allowed:
        errors.append(f"reviewer_decision={decision!r} not in allowed_decisions")
    if not reason:
        errors.append("decision_reason required for non-pending row")
    if not reviewer:
        errors.append("reviewer required for non-pending row")
    if not review_date:
        errors.append("review_date required for non-pending row")
    elif not DATE_PATTERN.match(review_date):
        errors.append("review_date must be YYYY-MM-DD")
    return errors


def write_invalid_rows(path: Path, invalid_rows: List[Dict[str, str]], fieldnames: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(invalid_rows)


def make_summary(rows: List[Dict[str, str]], invalid_rows: List[Dict[str, str]], args: argparse.Namespace) -> Dict[str, object]:
    status_counts = Counter(row.get("review_status", "") for row in rows)
    issue_type_counts = Counter(row.get("issue_type", "") for row in rows)
    priority_counts = Counter(row.get("priority", "") for row in rows)
    decision_counts = Counter(row.get("reviewer_decision", "") for row in rows if row.get("reviewer_decision", ""))

    pending = int(status_counts.get("pending", 0))
    reviewed = int(status_counts.get("reviewed", 0))
    needs_followup = int(status_counts.get("needs_followup", 0))
    invalid = len(invalid_rows)
    if invalid:
        overall_status = "invalid_review_sheet"
    elif pending:
        overall_status = "pending_manual_review"
    elif needs_followup:
        overall_status = "review_ready_with_followups"
    else:
        overall_status = "complete_validated"

    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "review_sheet": str(Path(args.review_sheet)),
        "overall_status": overall_status,
        "total_rows": len(rows),
        "pending_rows": pending,
        "reviewed_rows": reviewed,
        "needs_followup_rows": needs_followup,
        "invalid_rows": invalid,
        "status_counts": dict(sorted(status_counts.items())),
        "issue_type_counts": dict(sorted(issue_type_counts.items())),
        "priority_counts": dict(sorted(priority_counts.items())),
        "decision_counts": dict(sorted(decision_counts.items())),
        "invalid_output": str(Path(args.invalid_output)),
        "boundary": (
            "This validation report only checks manual review fields. It does not clean data, "
            "change manifests, convert files, run enhancement, or replace formal 502/496 protocols."
        ),
    }


def write_summary_md(path: Path, summary: Dict[str, object]) -> None:
    lines = [
        "# full_algae_dewatermark_v1 manual review validation",
        "",
        f"日期：{datetime.now().date().isoformat()}",
        "",
        "本文是人工复核表的字段完整性校验，不是清洗结果，也不是增强实验结果。",
        "",
        "## Summary",
        "",
        f"- Overall status: `{summary['overall_status']}`",
        f"- Total rows: `{summary['total_rows']}`",
        f"- Pending rows: `{summary['pending_rows']}`",
        f"- Reviewed rows: `{summary['reviewed_rows']}`",
        f"- Needs-followup rows: `{summary['needs_followup_rows']}`",
        f"- Invalid rows: `{summary['invalid_rows']}`",
        f"- Status counts: `{summary['status_counts']}`",
        f"- Issue type counts: `{summary['issue_type_counts']}`",
        f"- Priority counts: `{summary['priority_counts']}`",
        f"- Invalid row report: `{summary['invalid_output']}`",
        "",
        "## Boundary",
        "",
        "- `pending_manual_review` 表示还不能生成清洗 manifest 或 split leakage guard。",
        "- `complete_validated` 只表示人工复核字段完整且合法，不表示已经执行清洗或增强。",
        "- 本报告不替代 `full502_clean_v1` 或 `compare9_complete496_v1`。",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    rows = read_tsv(Path(args.review_sheet))
    invalid_rows: List[Dict[str, str]] = []
    for row in rows:
        errors = validate_row(row)
        if errors:
            invalid = dict(row)
            invalid["validation_errors"] = " | ".join(errors)
            invalid_rows.append(invalid)

    fieldnames = list(rows[0].keys()) + ["validation_errors"] if rows else ["validation_errors"]
    write_invalid_rows(Path(args.invalid_output), invalid_rows, fieldnames)
    summary = make_summary(rows, invalid_rows, args)
    Path(args.output_json).write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    write_summary_md(Path(args.output_md), summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
