from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Sequence, Tuple


THIS_DIR = Path(__file__).resolve().parent
METRICS_DIR = THIS_DIR.parent
PROJECT_ROOT = METRICS_DIR.parent
DEFAULT_REVIEW_DIR = PROJECT_ROOT / "metrics" / "manifests" / "full_algae_dewatermark_v1_manual_review"
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


DECISION_FIELDS = ["review_status", "reviewer_decision", "decision_reason", "reviewer", "review_date"]
TEMPLATE_FIELDS = [
    "review_status_to_apply",
    "reviewer_decision_to_apply",
    "decision_reason_to_apply",
    "reviewer_to_apply",
    "review_date_to_apply",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Validate and optionally apply full_algae_dewatermark_v1 manual review decisions. "
            "Default mode is dry-run; use --apply to write review sheets."
        )
    )
    parser.add_argument("--review-dir", default=str(DEFAULT_REVIEW_DIR))
    parser.add_argument(
        "--decisions",
        default=str(DEFAULT_REVIEW_DIR / "manual_review_decision_template.tsv"),
    )
    parser.add_argument("--date", default=datetime.now().date().strftime("%Y%m%d"))
    parser.add_argument("--apply", action="store_true", help="Actually write validated decisions to review sheets.")
    return parser.parse_args()


def read_tsv(path: Path) -> Tuple[List[Dict[str, str]], List[str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return [dict(row) for row in reader], list(reader.fieldnames or [])


def write_tsv(path: Path, rows: Sequence[Dict[str, object]], fieldnames: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(rows)


def split_allowed_decisions(value: str) -> List[str]:
    return [item.strip() for item in value.split("|") if item.strip()]


def has_template_decision(row: Dict[str, str]) -> bool:
    return any(row.get(field, "").strip() for field in TEMPLATE_FIELDS)


def issue_target_sheet(issue_type: str) -> str:
    return {
        "decode_failure": "decode_failures_review.tsv",
        "exact_duplicate_group": "exact_duplicates_review.tsv",
        "near_duplicate_pair": "near_duplicates_review.tsv",
        "quality_outlier": "quality_outliers_review.tsv",
    }.get(issue_type, "all_manual_review_issues.tsv")


def validate_template_row(row: Dict[str, str], issue_map: Dict[str, Dict[str, str]]) -> Tuple[Dict[str, str] | None, List[str]]:
    errors: List[str] = []
    issue_id = row.get("issue_id", "").strip()
    if not issue_id:
        return None, ["missing issue_id"]
    if issue_id not in issue_map:
        return None, [f"unknown issue_id={issue_id!r}"]
    if not has_template_decision(row):
        return None, []

    source = issue_map[issue_id]
    status = row.get("review_status_to_apply", "").strip()
    decision = row.get("reviewer_decision_to_apply", "").strip()
    reason = row.get("decision_reason_to_apply", "").strip()
    reviewer = row.get("reviewer_to_apply", "").strip()
    review_date = row.get("review_date_to_apply", "").strip()
    allowed = split_allowed_decisions(source.get("allowed_decisions", ""))

    if status not in {"pending", "reviewed", "needs_followup"}:
        errors.append(f"invalid review_status_to_apply={status!r}")
    if status == "pending":
        if any([decision, reason, reviewer, review_date]):
            errors.append("pending decision must leave decision/reason/reviewer/date blank")
    elif status in {"reviewed", "needs_followup"}:
        if not decision:
            errors.append("reviewer_decision_to_apply required")
        elif allowed and decision not in allowed:
            errors.append(f"reviewer_decision_to_apply={decision!r} not in allowed_decisions")
        if not reason:
            errors.append("decision_reason_to_apply required")
        if not reviewer:
            errors.append("reviewer_to_apply required")
        if not review_date:
            errors.append("review_date_to_apply required")
        elif not DATE_PATTERN.match(review_date):
            errors.append("review_date_to_apply must be YYYY-MM-DD")

    expected_target = issue_target_sheet(source.get("issue_type", ""))
    template_target = row.get("target_review_sheet", "").strip()
    if template_target and template_target != expected_target:
        errors.append(f"target_review_sheet={template_target!r} does not match expected {expected_target!r}")

    if errors:
        return None, errors

    return {
        "issue_id": issue_id,
        "target_review_sheet": expected_target,
        "review_status": status,
        "reviewer_decision": "" if status == "pending" else decision,
        "decision_reason": "" if status == "pending" else reason,
        "reviewer": "" if status == "pending" else reviewer,
        "review_date": "" if status == "pending" else review_date,
    }, []


def load_review_sheets(review_dir: Path) -> Tuple[Dict[str, Tuple[List[Dict[str, str]], List[str]]], Dict[str, Dict[str, str]]]:
    sheet_names = [
        "all_manual_review_issues.tsv",
        "decode_failures_review.tsv",
        "exact_duplicates_review.tsv",
        "near_duplicates_review.tsv",
        "quality_outliers_review.tsv",
    ]
    sheets: Dict[str, Tuple[List[Dict[str, str]], List[str]]] = {}
    issue_map: Dict[str, Dict[str, str]] = {}
    for name in sheet_names:
        rows, fieldnames = read_tsv(review_dir / name)
        sheets[name] = (rows, fieldnames)
        if name == "all_manual_review_issues.tsv":
            issue_map = {row["issue_id"]: row for row in rows}
    return sheets, issue_map


def apply_decisions_to_rows(rows: List[Dict[str, str]], decisions: Dict[str, Dict[str, str]]) -> int:
    changed = 0
    for row in rows:
        issue_id = row.get("issue_id", "")
        if issue_id not in decisions:
            continue
        decision = decisions[issue_id]
        for field in DECISION_FIELDS:
            row[field] = decision[field]
        changed += 1
    return changed


def write_summary_md(path: Path, summary: Dict[str, object]) -> None:
    mode = "apply" if summary["apply_mode"] else "dry-run"
    lines = [
        "# full_algae_dewatermark_v1 manual review decision apply report",
        "",
        f"日期：{datetime.now().date().isoformat()}",
        "",
        f"Mode: `{mode}`",
        "",
        "## Summary",
        "",
        f"- Status: `{summary['status']}`",
        f"- Template rows: `{summary['template_rows']}`",
        f"- Filled decision rows: `{summary['filled_decision_rows']}`",
        f"- Valid decision rows: `{summary['valid_decision_rows']}`",
        f"- Invalid decision rows: `{summary['invalid_decision_rows']}`",
        f"- Applied to review sheets: `{summary['applied_to_review_sheets']}`",
        f"- Plan TSV: `{summary['plan_tsv']}`",
        f"- Invalid TSV: `{summary['invalid_tsv']}`",
        "",
        "## Boundary",
        "",
        "- 默认 dry-run 不写回任何 review sheet。",
        "- 只有显式传 `--apply` 且无 invalid decision rows 时才会写回。",
        "- 写回后仍必须运行 `validate_fullpool_manual_review.py` 和 `derive_fullpool_review_artifacts.py`。",
        "- 本脚本不生成 clean manifest，不转换/删除原图，不运行增强。",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    review_dir = Path(args.review_dir)
    template_rows, template_fields = read_tsv(Path(args.decisions))
    sheets, issue_map = load_review_sheets(review_dir)

    valid_decisions: Dict[str, Dict[str, str]] = {}
    invalid_rows: List[Dict[str, str]] = []
    plan_rows: List[Dict[str, object]] = []
    duplicate_issue_ids: List[str] = []

    for row in template_rows:
        decision, errors = validate_template_row(row, issue_map)
        if errors:
            invalid = dict(row)
            invalid["validation_errors"] = " | ".join(errors)
            invalid_rows.append(invalid)
            continue
        if decision is None:
            continue
        issue_id = decision["issue_id"]
        if issue_id in valid_decisions:
            duplicate_issue_ids.append(issue_id)
            invalid = dict(row)
            invalid["validation_errors"] = "duplicate decision row"
            invalid_rows.append(invalid)
            continue
        valid_decisions[issue_id] = decision
        source = issue_map[issue_id]
        plan_rows.append(
            {
                "issue_id": issue_id,
                "priority": source.get("priority", ""),
                "issue_type": source.get("issue_type", ""),
                "target_review_sheet": decision["target_review_sheet"],
                "old_review_status": source.get("review_status", ""),
                "old_reviewer_decision": source.get("reviewer_decision", ""),
                "new_review_status": decision["review_status"],
                "new_reviewer_decision": decision["reviewer_decision"],
                "reviewer": decision["reviewer"],
                "review_date": decision["review_date"],
            }
        )

    if duplicate_issue_ids:
        # Duplicates are already present in invalid_rows; keep this branch explicit for summary clarity.
        pass

    plan_path = review_dir / f"manual_review_decision_apply_plan_{args.date}.tsv"
    invalid_path = review_dir / f"manual_review_decision_apply_invalid_{args.date}.tsv"
    plan_fields = [
        "issue_id",
        "priority",
        "issue_type",
        "target_review_sheet",
        "old_review_status",
        "old_reviewer_decision",
        "new_review_status",
        "new_reviewer_decision",
        "reviewer",
        "review_date",
    ]
    invalid_fields = list(template_fields) + ["validation_errors"]
    write_tsv(plan_path, plan_rows, plan_fields)
    write_tsv(invalid_path, invalid_rows, invalid_fields)

    applied_counts: Dict[str, int] = {}
    can_apply = bool(args.apply) and not invalid_rows
    if can_apply:
        for sheet_name, (rows, fieldnames) in sheets.items():
            relevant = valid_decisions if sheet_name == "all_manual_review_issues.tsv" else {
                issue_id: decision
                for issue_id, decision in valid_decisions.items()
                if decision["target_review_sheet"] == sheet_name
            }
            changed = apply_decisions_to_rows(rows, relevant)
            applied_counts[sheet_name] = changed
            write_tsv(review_dir / sheet_name, rows, fieldnames)

    filled_count = sum(1 for row in template_rows if has_template_decision(row))
    decision_counts = Counter(decision["reviewer_decision"] for decision in valid_decisions.values() if decision["reviewer_decision"])
    if invalid_rows:
        status = "invalid_decisions_found"
    elif not filled_count:
        status = "no_decisions_to_apply"
    elif args.apply:
        status = "applied"
    else:
        status = "dry_run_valid"

    summary = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "status": status,
        "apply_mode": bool(args.apply),
        "template": str(Path(args.decisions).relative_to(PROJECT_ROOT)),
        "template_rows": len(template_rows),
        "filled_decision_rows": filled_count,
        "valid_decision_rows": len(valid_decisions),
        "invalid_decision_rows": len(invalid_rows),
        "decision_counts": dict(sorted(decision_counts.items())),
        "applied_to_review_sheets": bool(can_apply),
        "applied_counts": applied_counts,
        "plan_tsv": str(plan_path.relative_to(PROJECT_ROOT)),
        "invalid_tsv": str(invalid_path.relative_to(PROJECT_ROOT)),
        "boundary": (
            "Dry-run mode does not write review sheets. This script never edits source images, "
            "runs enhancement, or generates a clean manifest."
        ),
    }
    summary_json_path = review_dir / f"manual_review_decision_apply_report_{args.date}.json"
    summary_md_path = review_dir / f"manual_review_decision_apply_report_{args.date}.md"
    summary_json_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    write_summary_md(summary_md_path, summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if invalid_rows:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
