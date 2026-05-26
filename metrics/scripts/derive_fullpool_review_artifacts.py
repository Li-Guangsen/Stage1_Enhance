from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Set

from validate_fullpool_manual_review import validate_row


THIS_DIR = Path(__file__).resolve().parent
METRICS_DIR = THIS_DIR.parent
PROJECT_ROOT = METRICS_DIR.parent

DEFAULT_REVIEW_DIR = PROJECT_ROOT / "metrics" / "manifests" / "full_algae_dewatermark_v1_manual_review"
DEFAULT_OUTPUT_DIR = DEFAULT_REVIEW_DIR / "derived_review_artifacts"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Derive downstream artifact lists from validated full_algae_dewatermark_v1 manual review decisions. "
            "This script never edits source images or formal 502/496 manifests."
        )
    )
    parser.add_argument(
        "--review-sheet",
        default=str(DEFAULT_REVIEW_DIR / "all_manual_review_issues.tsv"),
    )
    parser.add_argument(
        "--base-cv2-manifest",
        default=str(PROJECT_ROOT / "metrics" / "manifests" / "full_algae_dewatermark_v1_cv2_readable_candidate.txt"),
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
    )
    return parser.parse_args()


def read_tsv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle, delimiter="\t")]


def read_manifest(path: Path) -> List[str]:
    entries: List[str] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            value = line.strip()
            if value and not value.startswith("#"):
                entries.append(value)
    return entries


def write_tsv(path: Path, rows: Sequence[Dict[str, object]], fieldnames: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(rows)


def write_manifest(path: Path, entries: Iterable[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(entries) + "\n", encoding="utf-8")


def split_related_paths(row: Dict[str, str]) -> List[str]:
    values: List[str] = []
    relative_path = row.get("relative_path", "").strip()
    if relative_path:
        values.append(relative_path)
    related_paths = row.get("related_paths", "").strip()
    if related_paths:
        values.extend(part.strip() for part in related_paths.split(" | ") if part.strip())
    return values


def path_sort_key(value: str) -> str:
    return value.replace("\\", "/").casefold()


def row_status(rows: Sequence[Dict[str, str]], invalid_rows: Sequence[Dict[str, object]]) -> Dict[str, object]:
    status_counts = Counter(row.get("review_status", "") for row in rows)
    decision_counts = Counter(row.get("reviewer_decision", "") for row in rows if row.get("reviewer_decision", ""))
    pending = int(status_counts.get("pending", 0))
    needs_followup = int(status_counts.get("needs_followup", 0))
    unresolved_decisions = sum(1 for row in rows if row.get("reviewer_decision", "") == "needs_manual_visual_check")

    if invalid_rows:
        overall_status = "invalid_review_sheet"
        can_generate_clean_manifest = False
    elif pending:
        overall_status = "pending_manual_review"
        can_generate_clean_manifest = False
    elif needs_followup or unresolved_decisions:
        overall_status = "review_ready_with_followups"
        can_generate_clean_manifest = False
    else:
        overall_status = "complete_validated"
        can_generate_clean_manifest = True

    return {
        "overall_status": overall_status,
        "can_generate_clean_manifest": can_generate_clean_manifest,
        "total_rows": len(rows),
        "pending_rows": pending,
        "needs_followup_rows": needs_followup,
        "invalid_rows": len(invalid_rows),
        "unresolved_decision_rows": unresolved_decisions,
        "status_counts": dict(sorted(status_counts.items())),
        "decision_counts": dict(sorted(decision_counts.items())),
    }


def derive_rows(rows: Sequence[Dict[str, str]]) -> Dict[str, List[Dict[str, object]]]:
    conversions: List[Dict[str, object]] = []
    exclusions: List[Dict[str, object]] = []
    deduplicate_drops: List[Dict[str, object]] = []
    split_guards: List[Dict[str, object]] = []
    subset_labels: List[Dict[str, object]] = []

    for row in rows:
        status = row.get("review_status", "")
        decision = row.get("reviewer_decision", "")
        if status == "pending" or not decision:
            continue

        issue_id = row.get("issue_id", "")
        issue_type = row.get("issue_type", "")
        paths = split_related_paths(row)

        if issue_type == "decode_failure":
            path = row.get("relative_path", "")
            if decision == "convert_to_png":
                conversions.append(
                    {
                        "issue_id": issue_id,
                        "relative_path": path,
                        "decision": decision,
                        "decision_reason": row.get("decision_reason", ""),
                    }
                )
            elif decision in {"exclude_from_opencv_fullpool", "keep_external_only"}:
                exclusions.append(
                    {
                        "issue_id": issue_id,
                        "relative_path": path,
                        "decision": decision,
                        "exclusion_scope": "opencv_fullpool",
                        "decision_reason": row.get("decision_reason", ""),
                    }
                )

        elif issue_type == "exact_duplicate_group":
            if decision == "deduplicate_for_clean_pool":
                sorted_paths = sorted(paths, key=path_sort_key)
                keep_path = sorted_paths[0] if sorted_paths else ""
                for drop_path in sorted_paths[1:]:
                    deduplicate_drops.append(
                        {
                            "issue_id": issue_id,
                            "keep_path": keep_path,
                            "drop_path": drop_path,
                            "decision": decision,
                            "decision_reason": row.get("decision_reason", ""),
                        }
                    )
                    exclusions.append(
                        {
                            "issue_id": issue_id,
                            "relative_path": drop_path,
                            "decision": decision,
                            "exclusion_scope": "reviewed_clean_pool",
                            "decision_reason": row.get("decision_reason", ""),
                        }
                    )
            if decision in {"deduplicate_for_clean_pool", "keep_but_split_guard"}:
                split_guards.append(
                    {
                        "issue_id": issue_id,
                        "guard_type": "exact_duplicate_group",
                        "relative_paths": " | ".join(paths),
                        "decision": decision,
                        "decision_reason": row.get("decision_reason", ""),
                    }
                )

        elif issue_type == "near_duplicate_pair":
            if decision in {"mark_duplicate", "keep_but_split_guard"}:
                split_guards.append(
                    {
                        "issue_id": issue_id,
                        "guard_type": "near_duplicate_pair",
                        "relative_paths": " | ".join(paths),
                        "decision": decision,
                        "decision_reason": row.get("decision_reason", ""),
                    }
                )

        elif issue_type == "quality_outlier":
            path = row.get("relative_path", "")
            if decision == "quality_exclude_from_clean_pool":
                exclusions.append(
                    {
                        "issue_id": issue_id,
                        "relative_path": path,
                        "decision": decision,
                        "exclusion_scope": "reviewed_clean_pool",
                        "decision_reason": row.get("decision_reason", ""),
                    }
                )
            elif decision in {"valid_degradation_case", "failure_case_candidate", "subset_label_only"}:
                subset_labels.append(
                    {
                        "issue_id": issue_id,
                        "relative_path": path,
                        "decision": decision,
                        "evidence_summary": row.get("evidence_summary", ""),
                        "decision_reason": row.get("decision_reason", ""),
                    }
                )

    return {
        "conversions": conversions,
        "exclusions": exclusions,
        "deduplicate_drops": deduplicate_drops,
        "split_guards": split_guards,
        "subset_labels": subset_labels,
    }


def write_summary_md(path: Path, summary: Dict[str, object]) -> None:
    lines = [
        "# full_algae_dewatermark_v1 derived review artifacts",
        "",
        f"日期：{datetime.now().date().isoformat()}",
        "",
        "本文是人工复核决策派生清单的状态报告，不是清洗结果本身，也不运行增强。",
        "",
        "## Summary",
        "",
        f"- Overall status: `{summary['overall_status']}`",
        f"- Can generate clean manifest: `{summary['can_generate_clean_manifest']}`",
        f"- Total review rows: `{summary['total_rows']}`",
        f"- Pending rows: `{summary['pending_rows']}`",
        f"- Needs-followup rows: `{summary['needs_followup_rows']}`",
        f"- Invalid rows: `{summary['invalid_rows']}`",
        f"- Unresolved decision rows: `{summary['unresolved_decision_rows']}`",
        f"- Conversion candidates: `{summary['conversion_rows']}`",
        f"- Exclusion rows: `{summary['exclusion_rows']}`",
        f"- Deduplicate drop rows: `{summary['deduplicate_drop_rows']}`",
        f"- Split guard rows: `{summary['split_guard_rows']}`",
        f"- Subset label rows: `{summary['subset_label_rows']}`",
        f"- Reviewed clean manifest: `{summary.get('reviewed_clean_manifest', '') or 'not_generated'}`",
        "",
        "## Boundary",
        "",
        "- 只有 `overall_status=complete_validated` 时，本脚本才生成 reviewed clean manifest。",
        "- `pending_manual_review` 或 `review_ready_with_followups` 时，只能查看状态和空/部分派生表，不能作为清洗完成证据。",
        "- 本脚本不修改原图、不转换文件、不运行 Stage1，也不替代 `full502_clean_v1` / `compare9_complete496_v1`。",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    review_sheet = Path(args.review_sheet)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    rows = read_tsv(review_sheet)
    invalid_rows: List[Dict[str, object]] = []
    for row in rows:
        errors = validate_row(row)
        if errors:
            invalid_row = dict(row)
            invalid_row["validation_errors"] = " | ".join(errors)
            invalid_rows.append(invalid_row)

    status = row_status(rows, invalid_rows)
    derived = derive_rows(rows)

    conversion_path = output_dir / "conversion_candidates.tsv"
    exclusion_path = output_dir / "exclusion_candidates.tsv"
    dedup_path = output_dir / "deduplicate_drop_candidates.tsv"
    split_guard_path = output_dir / "split_leakage_guard_candidates.tsv"
    subset_path = output_dir / "subset_label_candidates.tsv"
    invalid_path = output_dir / "invalid_rows.tsv"
    summary_json_path = output_dir / "review_artifacts_status_20260525.json"
    summary_md_path = output_dir / "review_artifacts_status_20260525.md"
    clean_manifest_path = output_dir / "reviewed_cv2_clean_manifest.txt"

    write_tsv(
        conversion_path,
        derived["conversions"],
        ["issue_id", "relative_path", "decision", "decision_reason"],
    )
    write_tsv(
        exclusion_path,
        derived["exclusions"],
        ["issue_id", "relative_path", "decision", "exclusion_scope", "decision_reason"],
    )
    write_tsv(
        dedup_path,
        derived["deduplicate_drops"],
        ["issue_id", "keep_path", "drop_path", "decision", "decision_reason"],
    )
    write_tsv(
        split_guard_path,
        derived["split_guards"],
        ["issue_id", "guard_type", "relative_paths", "decision", "decision_reason"],
    )
    write_tsv(
        subset_path,
        derived["subset_labels"],
        ["issue_id", "relative_path", "decision", "evidence_summary", "decision_reason"],
    )
    invalid_fieldnames = list(rows[0].keys()) + ["validation_errors"] if rows else ["validation_errors"]
    write_tsv(invalid_path, invalid_rows, invalid_fieldnames)

    reviewed_clean_manifest = ""
    if status["can_generate_clean_manifest"]:
        base_entries = read_manifest(Path(args.base_cv2_manifest))
        exclusions: Set[str] = {
            str(row["relative_path"])
            for row in derived["exclusions"]
            if row.get("exclusion_scope") in {"reviewed_clean_pool", "opencv_fullpool"}
        }
        clean_entries = [entry for entry in base_entries if entry not in exclusions]
        write_manifest(clean_manifest_path, clean_entries)
        reviewed_clean_manifest = str(clean_manifest_path.relative_to(PROJECT_ROOT))

    summary: Dict[str, object] = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "review_sheet": str(review_sheet),
        "base_cv2_manifest": str(Path(args.base_cv2_manifest)),
        "output_dir": str(output_dir),
        **status,
        "conversion_rows": len(derived["conversions"]),
        "exclusion_rows": len(derived["exclusions"]),
        "deduplicate_drop_rows": len(derived["deduplicate_drops"]),
        "split_guard_rows": len(derived["split_guards"]),
        "subset_label_rows": len(derived["subset_labels"]),
        "conversion_candidates_tsv": str(conversion_path),
        "exclusion_candidates_tsv": str(exclusion_path),
        "deduplicate_drop_candidates_tsv": str(dedup_path),
        "split_leakage_guard_candidates_tsv": str(split_guard_path),
        "subset_label_candidates_tsv": str(subset_path),
        "invalid_rows_tsv": str(invalid_path),
        "reviewed_clean_manifest": reviewed_clean_manifest,
        "boundary": (
            "Derived artifacts are valid only after manual review decisions are complete and validated. "
            "This script does not edit source images, convert files, run enhancement, or replace formal 502/496 protocols."
        ),
    }
    summary_json_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    write_summary_md(summary_md_path, summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
