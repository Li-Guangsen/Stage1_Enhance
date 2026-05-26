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
DEFAULT_DATE = datetime.now().date().strftime("%Y%m%d")
DEFAULT_REVIEW_DIR = PROJECT_ROOT / "metrics" / "manifests" / "stage1_myedge_provenance_review"
DEFAULT_VISUAL_JSON = PROJECT_ROOT / "docs" / f"stage1_myedge_visual_relation_audit_{DEFAULT_DATE}_cn.json"
DEFAULT_VISUAL_TSV = PROJECT_ROOT / "metrics" / "manifests" / f"stage1_myedge_visual_relation_candidates_{DEFAULT_DATE}.tsv"
DEFAULT_OUTPUT_TEMPLATE = DEFAULT_REVIEW_DIR / "provenance_review_template.tsv"
DEFAULT_OUTPUT_QUEUE = DEFAULT_REVIEW_DIR / "provenance_priority_review_queue.tsv"
DEFAULT_OUTPUT_MD = DEFAULT_REVIEW_DIR / f"provenance_review_index_{DEFAULT_DATE}.md"
DEFAULT_OUTPUT_JSON = DEFAULT_REVIEW_DIR / f"provenance_review_index_{DEFAULT_DATE}.json"


DECISION_VALUES = [
    "confirmed_same_original",
    "confirmed_same_visual_subject_reencoded_or_cropped",
    "confirmed_related_same_species_not_same_original",
    "confirmed_different",
    "uncertain_needs_followup",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build a manual provenance-review template from the Stage1/MyEdge visual relation audit. "
            "This script only creates review assets. It does not fill reviewer decisions, rewrite manifests, "
            "run Stage1, run MyEdge, or compute edge metrics."
        )
    )
    parser.add_argument("--visual-json", default=str(DEFAULT_VISUAL_JSON))
    parser.add_argument("--visual-tsv", default=str(DEFAULT_VISUAL_TSV))
    parser.add_argument("--output-template", default=str(DEFAULT_OUTPUT_TEMPLATE))
    parser.add_argument("--output-queue", default=str(DEFAULT_OUTPUT_QUEUE))
    parser.add_argument("--output-md", default=str(DEFAULT_OUTPUT_MD))
    parser.add_argument("--output-json", default=str(DEFAULT_OUTPUT_JSON))
    return parser.parse_args()


def read_json(path: Path) -> Dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_tsv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def write_tsv(path: Path, rows: Sequence[Dict[str, object]], fields: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def as_float(value: object, default: float = 9999.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def as_int(value: object, default: int = 9999) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def priority_for_relation(relation_scope: str, band: str, rank: int) -> str:
    if relation_scope == "myedge_raw_to_stage1_original_same_filename":
        if band in {"exact_or_reencoded_visual_candidate", "strong_visual_candidate"}:
            return "P0"
        if band == "possible_visual_candidate":
            return "P1"
        return "P2"
    if band == "exact_or_reencoded_visual_candidate":
        return "P0"
    if band == "strong_visual_candidate":
        return "P1"
    if band == "possible_visual_candidate":
        return "P2"
    if rank == 1:
        return "P3"
    return "P4"


def suggestion_for_relation(relation_scope: str, band: str) -> str:
    if relation_scope == "myedge_raw_to_stage1_original_same_filename":
        if band in {"exact_or_reencoded_visual_candidate", "strong_visual_candidate"}:
            return "inspect_and_confirm_same_original_or_reencoded_pair"
        return "inspect_before_using_as_same_input"
    if band in {"exact_or_reencoded_visual_candidate", "strong_visual_candidate"}:
        return "inspect_fullpool_candidate_for_possible_original_id_mapping"
    if band == "possible_visual_candidate":
        return "low_confidence_inspect_only_if_needed_for_provenance"
    return "negative_or_fallback_candidate_keep_pending_unless_reviewer_checks"


def review_row(
    review_id: str,
    relation_scope: str,
    source_group: str,
    source_id: str,
    source_stem: str,
    source_path: str,
    candidate_group: str,
    candidate_id: str,
    candidate_path: str,
    candidate_relpath: str,
    rank: int,
    band: str,
    ahash_hamming: object,
    dhash_hamming: object,
    combined_hash_hamming: object,
    thumb_rmse_32: object,
    same_dimensions: object,
    source_width: object = "",
    source_height: object = "",
    candidate_width: object = "",
    candidate_height: object = "",
) -> Dict[str, object]:
    priority = priority_for_relation(relation_scope, band, rank)
    return {
        "review_id": review_id,
        "priority": priority,
        "relation_scope": relation_scope,
        "source_group": source_group,
        "source_id": source_id,
        "source_stem": source_stem,
        "source_path": source_path,
        "source_width": source_width,
        "source_height": source_height,
        "candidate_group": candidate_group,
        "candidate_id": candidate_id,
        "candidate_path": candidate_path,
        "candidate_relpath": candidate_relpath,
        "candidate_width": candidate_width,
        "candidate_height": candidate_height,
        "rank": rank,
        "candidate_band": band,
        "ahash_hamming": ahash_hamming,
        "dhash_hamming": dhash_hamming,
        "combined_hash_hamming": combined_hash_hamming,
        "thumb_rmse_32": thumb_rmse_32,
        "same_dimensions": same_dimensions,
        "machine_suggestion": suggestion_for_relation(relation_scope, band),
        "reviewer_decision": "",
        "confirmed_original_id": "",
        "confirmed_relation_note": "",
        "species_label_checked": "",
        "split_overlap_risk": "",
        "paper_use_allowed": "",
        "reviewer": "",
        "review_date": "",
        "review_notes": "",
    }


def sort_key(row: Dict[str, object]) -> tuple:
    priority_order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3, "P4": 4}
    scope_order = {
        "myedge_raw_to_stage1_original_same_filename": 0,
        "myedge_raw_to_fullpool_visual_candidate": 1,
        "stage1_original_to_fullpool_visual_candidate": 2,
    }
    return (
        priority_order.get(str(row.get("priority")), 99),
        scope_order.get(str(row.get("relation_scope")), 99),
        as_int(row.get("combined_hash_hamming")),
        as_float(row.get("thumb_rmse_32")),
        str(row.get("source_id", "")),
        as_int(row.get("rank")),
    )


def build_rows(visual_json: Dict[str, object], visual_tsv_rows: Sequence[Dict[str, str]]) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []

    myedge_stage1_pairs = (
        visual_json.get("comparisons", {})
        .get("myedge_vs_stage1_same_filename", [])  # type: ignore[union-attr]
    )
    for idx, item in enumerate(myedge_stage1_pairs, start=1):
        stem = str(item.get("stem", ""))
        rows.append(
            review_row(
                review_id=f"MS-{idx:04d}",
                relation_scope="myedge_raw_to_stage1_original_same_filename",
                source_group="myedge_raw_168",
                source_id=stem,
                source_stem=stem,
                source_path=str(item.get("myedge_path", "")),
                source_width=item.get("myedge_width", ""),
                source_height=item.get("myedge_height", ""),
                candidate_group="stage1_original_same_filename",
                candidate_id=stem,
                candidate_path=str(item.get("stage1_original_path", "")),
                candidate_relpath=f"{stem}.jpg",
                candidate_width=item.get("stage1_width", ""),
                candidate_height=item.get("stage1_height", ""),
                rank=1,
                band=str(item.get("candidate_band", "")),
                ahash_hamming=item.get("ahash_hamming", ""),
                dhash_hamming=item.get("dhash_hamming", ""),
                combined_hash_hamming=item.get("combined_hash_hamming", ""),
                thumb_rmse_32=item.get("thumb_rmse_32", ""),
                same_dimensions=item.get("same_dimensions", ""),
            )
        )

    fullpool_counter = 0
    for item in visual_tsv_rows:
        fullpool_counter += 1
        relation_scope = (
            "myedge_raw_to_fullpool_visual_candidate"
            if item.get("source_group") == "myedge_raw_168"
            else "stage1_original_to_fullpool_visual_candidate"
        )
        rows.append(
            review_row(
                review_id=f"FP-{fullpool_counter:04d}",
                relation_scope=relation_scope,
                source_group=item.get("source_group", ""),
                source_id=item.get("source_id", ""),
                source_stem=item.get("source_stem", ""),
                source_path=item.get("source_path", ""),
                candidate_group=item.get("target_group", ""),
                candidate_id=item.get("candidate_id", ""),
                candidate_path="",
                candidate_relpath=item.get("candidate_relpath", ""),
                candidate_width=item.get("candidate_width", ""),
                candidate_height=item.get("candidate_height", ""),
                rank=as_int(item.get("rank")),
                band=item.get("candidate_band", ""),
                ahash_hamming=item.get("ahash_hamming", ""),
                dhash_hamming=item.get("dhash_hamming", ""),
                combined_hash_hamming=item.get("combined_hash_hamming", ""),
                thumb_rmse_32=item.get("thumb_rmse_32", ""),
                same_dimensions=item.get("same_dimensions", ""),
            )
        )

    rows.sort(key=sort_key)
    return rows


def count_by(rows: Iterable[Dict[str, object]], key: str) -> Dict[str, int]:
    return dict(sorted(Counter(str(row.get(key, "")) for row in rows).items()))


def build_summary(rows: Sequence[Dict[str, object]], visual_json: Dict[str, object]) -> Dict[str, object]:
    p0_p1 = [row for row in rows if row.get("priority") in {"P0", "P1"}]
    fullpool_review_rows = [
        row for row in rows if "fullpool" in str(row.get("relation_scope", ""))
    ]
    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "status": "pending_manual_provenance_review",
        "source_visual_audit_status": visual_json.get("status", ""),
        "row_count": len(rows),
        "priority_counts": count_by(rows, "priority"),
        "relation_scope_counts": count_by(rows, "relation_scope"),
        "candidate_band_counts": count_by(rows, "candidate_band"),
        "p0_p1_rows": len(p0_p1),
        "fullpool_candidate_rows": len(fullpool_review_rows),
        "reviewer_decision_filled": 0,
        "reviewer_decision_pending": len(rows),
        "allowed_reviewer_decisions": DECISION_VALUES,
        "boundary": (
            "This template contains machine-generated candidates only. Empty reviewer_decision "
            "fields mean no provenance relation has been confirmed."
        ),
    }


def render_table(counts: Dict[str, int]) -> str:
    rows = ["| Item | Count |", "|---|---:|"]
    rows.extend(f"| {key} | {value} |" for key, value in counts.items())
    return "\n".join(rows)


def render_md(summary: Dict[str, object], template_path: Path, queue_path: Path) -> str:
    decision_values = "\n".join(f"- `{value}`" for value in DECISION_VALUES)
    return f"""# Stage1-MyEdge Provenance 人工复核入口

生成时间：`{summary["generated_at"]}`

状态：`{summary["status"]}`

本文件夹把视觉候选关系转成可人工填写的 provenance review 模板。它只服务于数据来源关系确认，不运行 Stage1，不运行 MyEdge，不生成指标，不生成图表。

## 文件

- 全量模板：`{template_path.as_posix()}`
- 优先队列：`{queue_path.as_posix()}`

## 计数

- 全量 review 行数：`{summary["row_count"]}`
- P0/P1 优先行数：`{summary["p0_p1_rows"]}`
- full-pool 候选行数：`{summary["fullpool_candidate_rows"]}`
- 已填写 reviewer decision：`{summary["reviewer_decision_filled"]}`
- pending reviewer decision：`{summary["reviewer_decision_pending"]}`

### Priority Counts

{render_table(summary["priority_counts"])}

### Relation Scope Counts

{render_table(summary["relation_scope_counts"])}

### Candidate Band Counts

{render_table(summary["candidate_band_counts"])}

## reviewer_decision 合法值

{decision_values}

## 使用规则

- `machine_suggestion` 只是机器建议，不能当作人工结论。
- `reviewer_decision` 为空表示尚未确认 provenance。
- 只有人工填写并经过后续校验的行，才能用于论文数据来源描述、original-id 映射或 split leakage guard。
- visual hash 候选不能证明同一原图、同一 split、同一 GT、同一采集协议或参考论文数据集 overlap。
"""


def main() -> None:
    args = parse_args()
    visual_json_path = Path(args.visual_json)
    visual_tsv_path = Path(args.visual_tsv)
    output_template = Path(args.output_template)
    output_queue = Path(args.output_queue)
    output_md = Path(args.output_md)
    output_json = Path(args.output_json)

    visual_json = read_json(visual_json_path)
    visual_tsv_rows = read_tsv(visual_tsv_path)
    rows = build_rows(visual_json, visual_tsv_rows)
    summary = build_summary(rows, visual_json)

    fields = [
        "review_id",
        "priority",
        "relation_scope",
        "source_group",
        "source_id",
        "source_stem",
        "source_path",
        "source_width",
        "source_height",
        "candidate_group",
        "candidate_id",
        "candidate_path",
        "candidate_relpath",
        "candidate_width",
        "candidate_height",
        "rank",
        "candidate_band",
        "ahash_hamming",
        "dhash_hamming",
        "combined_hash_hamming",
        "thumb_rmse_32",
        "same_dimensions",
        "machine_suggestion",
        "reviewer_decision",
        "confirmed_original_id",
        "confirmed_relation_note",
        "species_label_checked",
        "split_overlap_risk",
        "paper_use_allowed",
        "reviewer",
        "review_date",
        "review_notes",
    ]
    priority_rows = [row for row in rows if row.get("priority") in {"P0", "P1"}]

    output_template.parent.mkdir(parents=True, exist_ok=True)
    write_tsv(output_template, rows, fields)
    write_tsv(output_queue, priority_rows, fields)
    output_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    output_md.write_text(render_md(summary, output_template, output_queue), encoding="utf-8")

    print(f"Wrote {output_template}")
    print(f"Wrote {output_queue}")
    print(f"Wrote {output_md}")
    print(f"Wrote {output_json}")
    print(f"status={summary['status']}")


if __name__ == "__main__":
    main()
