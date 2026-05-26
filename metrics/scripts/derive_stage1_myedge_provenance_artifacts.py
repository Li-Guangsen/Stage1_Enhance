from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Sequence


THIS_DIR = Path(__file__).resolve().parent
sys.path.append(str(THIS_DIR))

from validate_stage1_myedge_provenance_review import validate_row  # noqa: E402


METRICS_DIR = THIS_DIR.parent
PROJECT_ROOT = METRICS_DIR.parent
DEFAULT_DATE = datetime.now().date().strftime("%Y%m%d")
DEFAULT_REVIEW_DIR = PROJECT_ROOT / "metrics" / "manifests" / "stage1_myedge_provenance_review"
DEFAULT_TEMPLATE = DEFAULT_REVIEW_DIR / "provenance_review_template.tsv"
DEFAULT_OUTPUT_DIR = DEFAULT_REVIEW_DIR / "derived_provenance_artifacts"
DEFAULT_STATUS_MD = DEFAULT_OUTPUT_DIR / f"provenance_artifacts_status_{DEFAULT_DATE}.md"
DEFAULT_STATUS_JSON = DEFAULT_OUTPUT_DIR / f"provenance_artifacts_status_{DEFAULT_DATE}.json"


POSITIVE_DECISIONS = {
    "confirmed_same_original",
    "confirmed_same_visual_subject_reencoded_or_cropped",
}
PAPER_USE_VALUES = {"yes", "only_with_boundary"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Derive Stage1/MyEdge provenance artifacts from manually reviewed rows. "
            "If review is pending or invalid, this script emits status and empty guarded outputs only."
        )
    )
    parser.add_argument("--template", default=str(DEFAULT_TEMPLATE))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--status-md", default=str(DEFAULT_STATUS_MD))
    parser.add_argument("--status-json", default=str(DEFAULT_STATUS_JSON))
    return parser.parse_args()


def read_tsv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def write_tsv(path: Path, rows: Sequence[Dict[str, object]], fields: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def unique_join(values: Iterable[object]) -> str:
    unique = sorted({str(value) for value in values if str(value).strip()})
    return ";".join(unique)


def relation_fields() -> List[str]:
    return [
        "review_id",
        "relation_scope",
        "confirmed_original_id",
        "reviewer_decision",
        "paper_use_allowed",
        "split_overlap_risk",
        "source_group",
        "source_id",
        "source_path",
        "candidate_group",
        "candidate_id",
        "candidate_path",
        "candidate_relpath",
        "candidate_band",
        "combined_hash_hamming",
        "thumb_rmse_32",
        "reviewer",
        "review_date",
        "confirmed_relation_note",
        "review_notes",
    ]


def map_fields() -> List[str]:
    return [
        "confirmed_original_id",
        "relation_count",
        "source_groups",
        "source_ids",
        "candidate_groups",
        "candidate_ids",
        "relation_scopes",
        "reviewer_decisions",
        "paper_use_allowed_values",
        "split_overlap_risk_values",
        "reviewers",
        "review_dates",
        "notes",
    ]


def guard_fields() -> List[str]:
    return [
        "confirmed_original_id",
        "relation_scope",
        "source_id",
        "candidate_id",
        "source_group",
        "candidate_group",
        "split_overlap_risk",
        "paper_use_allowed",
        "reviewer_decision",
        "guard_reason",
    ]


def build_artifacts(rows: Sequence[Dict[str, str]]) -> Dict[str, object]:
    invalid_rows: List[Dict[str, str]] = []
    reviewed_rows: List[Dict[str, str]] = []
    positive_rows: List[Dict[str, str]] = []
    paper_rows: List[Dict[str, str]] = []
    negative_or_uncertain_rows: List[Dict[str, str]] = []

    for row in rows:
        errors = validate_row(row)
        if errors:
            invalid = dict(row)
            invalid["validation_errors"] = ";".join(errors)
            invalid_rows.append(invalid)
        decision = row.get("reviewer_decision", "").strip()
        if not decision:
            continue
        reviewed_rows.append(row)
        if decision in POSITIVE_DECISIONS:
            positive_rows.append(row)
        else:
            negative_or_uncertain_rows.append(row)
        if row.get("paper_use_allowed", "").strip() in PAPER_USE_VALUES:
            paper_rows.append(row)

    pending_count = len(rows) - len(reviewed_rows)
    can_generate_final_provenance = pending_count == 0 and not invalid_rows and bool(paper_rows)

    maps_by_original: Dict[str, List[Dict[str, str]]] = defaultdict(list)
    for row in positive_rows:
        original_id = row.get("confirmed_original_id", "").strip()
        if original_id:
            maps_by_original[original_id].append(row)

    original_map_rows: List[Dict[str, object]] = []
    for original_id, group in sorted(maps_by_original.items()):
        original_map_rows.append(
            {
                "confirmed_original_id": original_id,
                "relation_count": len(group),
                "source_groups": unique_join(row.get("source_group") for row in group),
                "source_ids": unique_join(row.get("source_id") for row in group),
                "candidate_groups": unique_join(row.get("candidate_group") for row in group),
                "candidate_ids": unique_join(row.get("candidate_id") for row in group),
                "relation_scopes": unique_join(row.get("relation_scope") for row in group),
                "reviewer_decisions": unique_join(row.get("reviewer_decision") for row in group),
                "paper_use_allowed_values": unique_join(row.get("paper_use_allowed") for row in group),
                "split_overlap_risk_values": unique_join(row.get("split_overlap_risk") for row in group),
                "reviewers": unique_join(row.get("reviewer") for row in group),
                "review_dates": unique_join(row.get("review_date") for row in group),
                "notes": unique_join(row.get("confirmed_relation_note") for row in group),
            }
        )

    guard_rows: List[Dict[str, object]] = []
    for row in positive_rows:
        guard_rows.append(
            {
                "confirmed_original_id": row.get("confirmed_original_id", ""),
                "relation_scope": row.get("relation_scope", ""),
                "source_id": row.get("source_id", ""),
                "candidate_id": row.get("candidate_id", ""),
                "source_group": row.get("source_group", ""),
                "candidate_group": row.get("candidate_group", ""),
                "split_overlap_risk": row.get("split_overlap_risk", ""),
                "paper_use_allowed": row.get("paper_use_allowed", ""),
                "reviewer_decision": row.get("reviewer_decision", ""),
                "guard_reason": "positive_provenance_relation_requires_split_leakage_attention",
            }
        )

    status = "pending_manual_provenance_review"
    if invalid_rows:
        status = "invalid_manual_provenance_review"
    elif can_generate_final_provenance:
        status = "final_provenance_artifacts_ready"

    return {
        "status": status,
        "row_count": len(rows),
        "pending_count": pending_count,
        "reviewed_count": len(reviewed_rows),
        "invalid_count": len(invalid_rows),
        "positive_relation_count": len(positive_rows),
        "paper_usable_relation_count": len(paper_rows),
        "negative_or_uncertain_count": len(negative_or_uncertain_rows),
        "confirmed_original_id_count": len(original_map_rows),
        "split_leakage_guard_candidate_count": len(guard_rows),
        "can_generate_final_provenance": can_generate_final_provenance,
        "invalid_rows": invalid_rows,
        "confirmed_positive_relations": positive_rows,
        "paper_usable_relations": paper_rows,
        "negative_or_uncertain_relations": negative_or_uncertain_rows,
        "confirmed_original_id_map": original_map_rows,
        "split_leakage_guard_candidates": guard_rows,
    }


def render_status(summary: Dict[str, object], paths: Dict[str, Path]) -> str:
    return f"""# Stage1-MyEdge provenance 派生 artifacts 状态

生成时间：`{summary["generated_at"]}`

状态：`{summary["status"]}`

本报告由人工 provenance review 模板派生。当前脚本只读取复核表，不推断人工结论，不运行 Stage1，不运行 MyEdge，不生成指标或图表。

## 计数

- 总行数：`{summary["row_count"]}`
- pending：`{summary["pending_count"]}`
- reviewed：`{summary["reviewed_count"]}`
- invalid：`{summary["invalid_count"]}`
- positive relations：`{summary["positive_relation_count"]}`
- paper-usable relations：`{summary["paper_usable_relation_count"]}`
- confirmed original IDs：`{summary["confirmed_original_id_count"]}`
- split leakage guard candidates：`{summary["split_leakage_guard_candidate_count"]}`
- can generate final provenance：`{summary["can_generate_final_provenance"]}`

## 输出

- confirmed positive relations：`{paths["positive"].as_posix()}`
- paper-usable relations：`{paths["paper"].as_posix()}`
- negative/uncertain relations：`{paths["negative"].as_posix()}`
- confirmed original-id map：`{paths["map"].as_posix()}`
- split leakage guard candidates：`{paths["guard"].as_posix()}`
- invalid rows：`{paths["invalid"].as_posix()}`

## 边界

- 当前如果仍有 pending 或 invalid，不能把任何派生表写成最终 provenance 结论。
- 即使 future 状态达到 `final_provenance_artifacts_ready`，它也只证明人工复核的 source relation；不能替代 MyEdge 带 GT 下游评测、Stage1 full2770 增强结果或参考论文 split/GT 证明。
"""


def main() -> None:
    args = parse_args()
    template = Path(args.template)
    output_dir = Path(args.output_dir)
    status_md = Path(args.status_md)
    status_json = Path(args.status_json)

    rows = read_tsv(template)
    artifacts = build_artifacts(rows)
    output_dir.mkdir(parents=True, exist_ok=True)

    paths = {
        "positive": output_dir / "confirmed_positive_relations.tsv",
        "paper": output_dir / "paper_usable_provenance_relations.tsv",
        "negative": output_dir / "reviewed_negative_or_uncertain_relations.tsv",
        "map": output_dir / "confirmed_original_id_map.tsv",
        "guard": output_dir / "split_leakage_guard_candidates.tsv",
        "invalid": output_dir / f"provenance_artifacts_invalid_rows_{DEFAULT_DATE}.tsv",
    }

    write_tsv(paths["positive"], artifacts["confirmed_positive_relations"], relation_fields())
    write_tsv(paths["paper"], artifacts["paper_usable_relations"], relation_fields())
    write_tsv(paths["negative"], artifacts["negative_or_uncertain_relations"], relation_fields())
    write_tsv(paths["map"], artifacts["confirmed_original_id_map"], map_fields())
    write_tsv(paths["guard"], artifacts["split_leakage_guard_candidates"], guard_fields())
    invalid_fields = list(rows[0].keys()) + ["validation_errors"] if rows else ["validation_errors"]
    write_tsv(paths["invalid"], artifacts["invalid_rows"], invalid_fields)

    summary = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "template": str(template),
        "output_dir": str(output_dir),
        "status": artifacts["status"],
        "row_count": artifacts["row_count"],
        "pending_count": artifacts["pending_count"],
        "reviewed_count": artifacts["reviewed_count"],
        "invalid_count": artifacts["invalid_count"],
        "positive_relation_count": artifacts["positive_relation_count"],
        "paper_usable_relation_count": artifacts["paper_usable_relation_count"],
        "negative_or_uncertain_count": artifacts["negative_or_uncertain_count"],
        "confirmed_original_id_count": artifacts["confirmed_original_id_count"],
        "split_leakage_guard_candidate_count": artifacts["split_leakage_guard_candidate_count"],
        "can_generate_final_provenance": artifacts["can_generate_final_provenance"],
        "outputs": {key: str(value) for key, value in paths.items()},
        "boundary": (
            "Derived artifacts are final only when can_generate_final_provenance is true. "
            "Pending or invalid review rows keep all provenance claims blocked."
        ),
    }

    status_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    status_md.write_text(render_status(summary, paths), encoding="utf-8")

    print(f"Wrote {status_md}")
    print(f"Wrote {status_json}")
    print(f"status={summary['status']}")


if __name__ == "__main__":
    main()
