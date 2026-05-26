from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Sequence


THIS_DIR = Path(__file__).resolve().parent
METRICS_DIR = THIS_DIR.parent
PROJECT_ROOT = METRICS_DIR.parent
DEFAULT_DATE = datetime.now().date().strftime("%Y%m%d")
DEFAULT_REVIEW_DIR = PROJECT_ROOT / "metrics" / "manifests" / "stage1_myedge_provenance_review"
DEFAULT_TEMPLATE = DEFAULT_REVIEW_DIR / "provenance_review_template.tsv"
DEFAULT_OUTPUT_MD = DEFAULT_REVIEW_DIR / f"provenance_review_validation_status_{DEFAULT_DATE}.md"
DEFAULT_OUTPUT_JSON = DEFAULT_REVIEW_DIR / f"provenance_review_validation_status_{DEFAULT_DATE}.json"
DEFAULT_INVALID_TSV = DEFAULT_REVIEW_DIR / f"provenance_review_invalid_rows_{DEFAULT_DATE}.tsv"


DECISION_VALUES = {
    "confirmed_same_original",
    "confirmed_same_visual_subject_reencoded_or_cropped",
    "confirmed_related_same_species_not_same_original",
    "confirmed_different",
    "uncertain_needs_followup",
}
YES_NO_VALUES = {"", "yes", "no", "uncertain", "not_applicable"}
RISK_VALUES = {"", "none", "low", "medium", "high", "uncertain"}
PAPER_USE_VALUES = {"", "yes", "no", "only_with_boundary"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Validate the Stage1/MyEdge provenance review template after manual filling. "
            "This script does not infer decisions or write any clean manifest."
        )
    )
    parser.add_argument("--template", default=str(DEFAULT_TEMPLATE))
    parser.add_argument("--output-md", default=str(DEFAULT_OUTPUT_MD))
    parser.add_argument("--output-json", default=str(DEFAULT_OUTPUT_JSON))
    parser.add_argument("--invalid-tsv", default=str(DEFAULT_INVALID_TSV))
    return parser.parse_args()


def read_tsv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def write_tsv(path: Path, rows: Sequence[Dict[str, str]], fields: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def validate_row(row: Dict[str, str]) -> List[str]:
    errors: List[str] = []
    decision = row.get("reviewer_decision", "").strip()
    original_id = row.get("confirmed_original_id", "").strip()
    reviewer = row.get("reviewer", "").strip()
    review_date = row.get("review_date", "").strip()
    species_checked = row.get("species_label_checked", "").strip()
    split_risk = row.get("split_overlap_risk", "").strip()
    paper_use = row.get("paper_use_allowed", "").strip()

    if not decision:
        return errors
    if decision not in DECISION_VALUES:
        errors.append("invalid_reviewer_decision")
    if decision in {"confirmed_same_original", "confirmed_same_visual_subject_reencoded_or_cropped"} and not original_id:
        errors.append("confirmed_relation_requires_confirmed_original_id")
    if not reviewer:
        errors.append("reviewer_required_when_decision_filled")
    if not review_date or not DATE_RE.match(review_date):
        errors.append("review_date_required_yyyy_mm_dd_when_decision_filled")
    if species_checked not in YES_NO_VALUES:
        errors.append("invalid_species_label_checked")
    if split_risk not in RISK_VALUES:
        errors.append("invalid_split_overlap_risk")
    if paper_use not in PAPER_USE_VALUES:
        errors.append("invalid_paper_use_allowed")
    if paper_use in {"yes", "only_with_boundary"} and decision in {"confirmed_different", "uncertain_needs_followup"}:
        errors.append("paper_use_requires_confirmed_positive_relation")
    return errors


def count_by(rows: Sequence[Dict[str, str]], key: str) -> Dict[str, int]:
    return dict(sorted(Counter(row.get(key, "") for row in rows).items()))


def render_count_table(counts: Dict[str, int]) -> str:
    table = ["| Item | Count |", "|---|---:|"]
    table.extend(f"| {key or '(blank)'} | {value} |" for key, value in counts.items())
    return "\n".join(table)


def render_md(summary: Dict[str, object], invalid_tsv: Path) -> str:
    return f"""# Stage1-MyEdge Provenance 复核校验状态

生成时间：`{summary["generated_at"]}`

状态：`{summary["status"]}`

本校验只检查人工 provenance review 模板字段是否合法，不推断结论，不生成 clean manifest，不改变任何实验结果。

## 计数

- 总行数：`{summary["row_count"]}`
- pending 行数：`{summary["pending_count"]}`
- reviewed 行数：`{summary["reviewed_count"]}`
- invalid 行数：`{summary["invalid_count"]}`
- 可作为 paper-positive 的行数：`{summary["paper_positive_count"]}`
- invalid rows：`{invalid_tsv.as_posix()}`

## Decision Counts

{render_count_table(summary["decision_counts"])}

## Paper Use Counts

{render_count_table(summary["paper_use_counts"])}

## 边界

- pending 行不能用于 provenance 论文结论。
- invalid 行必须修正后才能使用。
- 即使校验通过，`paper_use_allowed=yes` 也只证明人工确认了本模板中的 provenance 关系，不自动证明 Stage1 下游收益或参考论文 overlap。
"""


def main() -> None:
    args = parse_args()
    template = Path(args.template)
    output_md = Path(args.output_md)
    output_json = Path(args.output_json)
    invalid_tsv = Path(args.invalid_tsv)

    rows = read_tsv(template)
    invalid_rows: List[Dict[str, str]] = []
    reviewed_rows = 0
    paper_positive = 0
    for row in rows:
        errors = validate_row(row)
        decision = row.get("reviewer_decision", "").strip()
        if decision:
            reviewed_rows += 1
        if errors:
            invalid = dict(row)
            invalid["validation_errors"] = ";".join(errors)
            invalid_rows.append(invalid)
        if row.get("paper_use_allowed", "").strip() in {"yes", "only_with_boundary"}:
            paper_positive += 1

    status = "valid_complete" if reviewed_rows == len(rows) and not invalid_rows else "pending_manual_provenance_review"
    if invalid_rows:
        status = "invalid_manual_provenance_review"

    summary: Dict[str, object] = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "status": status,
        "template": str(template),
        "row_count": len(rows),
        "pending_count": len(rows) - reviewed_rows,
        "reviewed_count": reviewed_rows,
        "invalid_count": len(invalid_rows),
        "paper_positive_count": paper_positive,
        "decision_counts": count_by(rows, "reviewer_decision"),
        "paper_use_counts": count_by(rows, "paper_use_allowed"),
        "boundary": "Validation checks fields only; it does not infer provenance or create a clean manifest.",
    }

    fields = list(rows[0].keys()) + ["validation_errors"] if rows else ["validation_errors"]
    write_tsv(invalid_tsv, invalid_rows, fields)
    output_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    output_md.write_text(render_md(summary, invalid_tsv), encoding="utf-8")
    print(f"Wrote {output_md}")
    print(f"Wrote {output_json}")
    print(f"Wrote {invalid_tsv}")
    print(f"status={status}")


if __name__ == "__main__":
    main()
