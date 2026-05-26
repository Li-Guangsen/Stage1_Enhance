from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List


THIS_DIR = Path(__file__).resolve().parent
METRICS_DIR = THIS_DIR.parent
PROJECT_ROOT = METRICS_DIR.parent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build manual review sheets from full_algae_dewatermark_v1 audit outputs. "
            "This script only creates review TSV/Markdown files; it does not change manifests."
        )
    )
    parser.add_argument(
        "--decode-failures",
        default=str(PROJECT_ROOT / "metrics" / "manifests" / "full_algae_dewatermark_v1_decode_failures.tsv"),
    )
    parser.add_argument(
        "--exact-groups",
        default=str(
            PROJECT_ROOT
            / "metrics"
            / "manifests"
            / "full_algae_dewatermark_v1_duplicate_audit_exact_duplicate_groups.tsv"
        ),
    )
    parser.add_argument(
        "--near-pairs",
        default=str(
            PROJECT_ROOT
            / "metrics"
            / "manifests"
            / "full_algae_dewatermark_v1_duplicate_audit_near_duplicate_pairs.tsv"
        ),
    )
    parser.add_argument(
        "--quality-outliers",
        default=str(PROJECT_ROOT / "metrics" / "manifests" / "full_algae_dewatermark_v1_quality_audit_outliers.tsv"),
    )
    parser.add_argument(
        "--output-dir",
        default=str(PROJECT_ROOT / "metrics" / "manifests" / "full_algae_dewatermark_v1_manual_review"),
    )
    return parser.parse_args()


def read_tsv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle, delimiter="\t")]


def write_tsv(path: Path, rows: List[Dict[str, object]], fieldnames: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(rows)


def top_level_from_relative(relative_path: str) -> str:
    return relative_path.replace("\\", "/").split("/", 1)[0] if relative_path else ""


REVIEW_FIELDS = [
    "issue_id",
    "issue_type",
    "priority",
    "relative_path",
    "related_paths",
    "top_level_folder",
    "evidence_summary",
    "recommended_review_action",
    "allowed_decisions",
    "review_status",
    "reviewer_decision",
    "decision_reason",
    "reviewer",
    "review_date",
]


def blank_review_fields(row: Dict[str, object]) -> Dict[str, object]:
    row.update(
        {
            "review_status": "pending",
            "reviewer_decision": "",
            "decision_reason": "",
            "reviewer": "",
            "review_date": "",
        }
    )
    return row


def build_decode_review(rows: List[Dict[str, str]]) -> List[Dict[str, object]]:
    review_rows: List[Dict[str, object]] = []
    for index, row in enumerate(rows, start=1):
        relative_path = row.get("relative_path", "")
        review_rows.append(
            blank_review_fields(
                {
                    "issue_id": f"decode_failure_{index:04d}",
                    "issue_type": "decode_failure",
                    "priority": "P0",
                    "relative_path": relative_path,
                    "related_paths": "",
                    "top_level_folder": top_level_from_relative(relative_path),
                    "evidence_summary": (
                        f"extension={row.get('extension', '')}; size_bytes={row.get('size_bytes', '')}; "
                        f"magic_ascii={row.get('magic_ascii', '')}; error={row.get('error', '')}"
                    ),
                    "recommended_review_action": (
                        "Decide convert_to_png, exclude_from_opencv_fullpool, or keep_external_only."
                    ),
                    "allowed_decisions": "convert_to_png|exclude_from_opencv_fullpool|keep_external_only|needs_manual_visual_check",
                }
            )
        )
    return review_rows


def build_exact_review(rows: List[Dict[str, str]]) -> List[Dict[str, object]]:
    review_rows: List[Dict[str, object]] = []
    strict_rows = [row for row in rows if row.get("group_kind") == "file_sha256"]
    for index, row in enumerate(strict_rows, start=1):
        review_rows.append(
            blank_review_fields(
                {
                    "issue_id": f"exact_duplicate_group_{index:04d}",
                    "issue_type": "exact_duplicate_group",
                    "priority": "P0",
                    "relative_path": "",
                    "related_paths": row.get("relative_paths", ""),
                    "top_level_folder": row.get("top_level_folders", ""),
                    "evidence_summary": (
                        f"group_id={row.get('group_id', '')}; count={row.get('count', '')}; "
                        f"candidate_count={row.get('candidate_count', '')}; "
                        f"top_level_folder_count={row.get('top_level_folder_count', '')}; "
                        f"sha256={row.get('hash', '')}"
                    ),
                    "recommended_review_action": (
                        "Decide keep_all, deduplicate_for_clean_pool, or keep_but_split_guard."
                    ),
                    "allowed_decisions": "keep_all|deduplicate_for_clean_pool|keep_but_split_guard|needs_manual_visual_check",
                }
            )
        )
    return review_rows


def build_near_review(rows: List[Dict[str, str]]) -> List[Dict[str, object]]:
    review_rows: List[Dict[str, object]] = []
    for index, row in enumerate(rows, start=1):
        related_paths = f"{row.get('relative_path_a', '')} | {row.get('relative_path_b', '')}"
        top_folders = f"{row.get('top_level_folder_a', '')} | {row.get('top_level_folder_b', '')}"
        priority = "P1" if row.get("phash_distance") == "0" and row.get("dhash_distance") == "0" else "P2"
        review_rows.append(
            blank_review_fields(
                {
                    "issue_id": f"near_duplicate_pair_{index:04d}",
                    "issue_type": "near_duplicate_pair",
                    "priority": priority,
                    "relative_path": "",
                    "related_paths": related_paths,
                    "top_level_folder": top_folders,
                    "evidence_summary": (
                        f"source_pair_id={row.get('pair_id', '')}; "
                        f"phash_distance={row.get('phash_distance', '')}; "
                        f"dhash_distance={row.get('dhash_distance', '')}; "
                        f"ahash_distance={row.get('ahash_distance', '')}; "
                        f"same_top_level_folder={row.get('same_top_level_folder', '')}; "
                        f"same_file_sha256={row.get('same_file_sha256', '')}; "
                        f"same_gray_image_sha256={row.get('same_gray_image_sha256', '')}"
                    ),
                    "recommended_review_action": "Manual visual check; decide duplicate, keep_all, or split_guard.",
                    "allowed_decisions": "keep_all|mark_duplicate|keep_but_split_guard|needs_manual_visual_check",
                }
            )
        )
    return review_rows


def build_quality_review(rows: List[Dict[str, str]]) -> List[Dict[str, object]]:
    review_rows: List[Dict[str, object]] = []
    for index, row in enumerate(rows, start=1):
        relative_path = row.get("relative_path", "")
        flags = row.get("outlier_flags", "")
        priority = "P1" if any(flag in flags for flag in ["low_laplacian_sharpness", "low_tenengrad_edges", "low_contrast"]) else "P2"
        review_rows.append(
            blank_review_fields(
                {
                    "issue_id": f"quality_outlier_{index:04d}",
                    "issue_type": "quality_outlier",
                    "priority": priority,
                    "relative_path": relative_path,
                    "related_paths": "",
                    "top_level_folder": row.get("top_level_folder", top_level_from_relative(relative_path)),
                    "evidence_summary": (
                        f"flags={flags}; width={row.get('width', '')}; height={row.get('height', '')}; "
                        f"megapixels={row.get('megapixels', '')}; aspect_ratio={row.get('aspect_ratio', '')}; "
                        f"luma_mean={row.get('luma_mean', '')}; luma_std={row.get('luma_std', '')}; "
                        f"saturation_mean={row.get('saturation_mean', '')}; "
                        f"laplacian_var={row.get('laplacian_var', '')}; tenengrad={row.get('tenengrad', '')}"
                    ),
                    "recommended_review_action": (
                        "Label as valid_degradation_case, low_quality_exclude, or use_for_failure_case/subset."
                    ),
                    "allowed_decisions": (
                        "valid_degradation_case|quality_exclude_from_clean_pool|failure_case_candidate|subset_label_only|needs_manual_visual_check"
                    ),
                }
            )
        )
    return review_rows


def write_index_md(path: Path, summary: Dict[str, object], outputs: Dict[str, str]) -> None:
    lines = [
        "# full_algae_dewatermark_v1 manual review sheets",
        "",
        f"日期：{datetime.now().date().isoformat()}",
        "",
        "本文是完整增强图像池审计结果的人工复核入口，不是清洗结果，也不是增强实验结果。",
        "",
        "## Summary",
        "",
        f"- Decode failure review rows: `{summary['decode_failure_rows']}`",
        f"- Exact duplicate group review rows: `{summary['exact_duplicate_group_rows']}`",
        f"- Near duplicate pair review rows: `{summary['near_duplicate_pair_rows']}`",
        f"- Quality outlier review rows: `{summary['quality_outlier_rows']}`",
        f"- Unified review rows: `{summary['unified_review_rows']}`",
        "",
        "## Outputs",
        "",
    ]
    for label, output_path in outputs.items():
        lines.append(f"- {label}: `{output_path}`")
    lines.extend(
        [
            "",
            "## Review Rule",
            "",
            "- 所有行默认 `review_status=pending`。",
            "- 填写 `reviewer_decision` 前，不得修改 manifest、不得删除或转换原图。",
            "- 任何清洗决策都必须保留 `decision_reason`、`reviewer` 和 `review_date`。",
            "- 如果用于 MyEdge 训练/测试划分，严格重复和近重复至少应作为 split leakage guard。",
            "- 这些 sheets 不替代 `full502_clean_v1` 或 `compare9_complete496_v1`。",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    decode_review = build_decode_review(read_tsv(Path(args.decode_failures)))
    exact_review = build_exact_review(read_tsv(Path(args.exact_groups)))
    near_review = build_near_review(read_tsv(Path(args.near_pairs)))
    quality_review = build_quality_review(read_tsv(Path(args.quality_outliers)))
    unified_review = decode_review + exact_review + near_review + quality_review

    outputs = {
        "decode failures": output_dir / "decode_failures_review.tsv",
        "exact duplicates": output_dir / "exact_duplicates_review.tsv",
        "near duplicates": output_dir / "near_duplicates_review.tsv",
        "quality outliers": output_dir / "quality_outliers_review.tsv",
        "all issues": output_dir / "all_manual_review_issues.tsv",
        "summary json": output_dir / "manual_review_index.json",
        "summary md": output_dir / "manual_review_index.md",
    }
    write_tsv(outputs["decode failures"], decode_review, REVIEW_FIELDS)
    write_tsv(outputs["exact duplicates"], exact_review, REVIEW_FIELDS)
    write_tsv(outputs["near duplicates"], near_review, REVIEW_FIELDS)
    write_tsv(outputs["quality outliers"], quality_review, REVIEW_FIELDS)
    write_tsv(outputs["all issues"], unified_review, REVIEW_FIELDS)

    summary = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "decode_failure_rows": len(decode_review),
        "exact_duplicate_group_rows": len(exact_review),
        "near_duplicate_pair_rows": len(near_review),
        "quality_outlier_rows": len(quality_review),
        "unified_review_rows": len(unified_review),
        "review_status": "pending_manual_review",
        "boundary": (
            "These sheets are manual review inputs only. They do not change manifests, clean data, "
            "run enhancement, or replace formal 502/496 protocols."
        ),
    }
    outputs["summary json"].write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    relative_outputs = {label: str(path.relative_to(PROJECT_ROOT)) for label, path in outputs.items()}
    write_index_md(outputs["summary md"], summary, relative_outputs)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
