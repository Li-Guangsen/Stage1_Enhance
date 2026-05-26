from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Sequence


THIS_DIR = Path(__file__).resolve().parent
METRICS_DIR = THIS_DIR.parent
PROJECT_ROOT = METRICS_DIR.parent
DEFAULT_MYEDGE_ROOT = Path(r"D:\Desktop\MyEdgeCodex")
DEFAULT_FULLPOOL_ROOT = Path(r"D:\Desktop\去水印所有藻类图像")
DEFAULT_DATE = datetime.now().date().strftime("%Y%m%d")
DEFAULT_OUTPUT_MD = PROJECT_ROOT / "docs" / f"stage1_myedge_file_relation_audit_{DEFAULT_DATE}_cn.md"
DEFAULT_OUTPUT_JSON = PROJECT_ROOT / "docs" / f"stage1_myedge_file_relation_audit_{DEFAULT_DATE}_cn.json"


FORMAL_RESULT_ROOT = (
    PROJECT_ROOT
    / "experiments"
    / "h2-full506-direct"
    / "outputs"
    / "full506"
    / "runs"
    / "full506_final_mainline"
)
STAGE1_ORIGINAL_ROOT = PROJECT_ROOT / "data" / "inputImg" / "Original"
FULL502_MANIFEST = PROJECT_ROOT / "metrics" / "manifests" / "full502_clean_v1.txt"
COMPARE496_MANIFEST = PROJECT_ROOT / "metrics" / "manifests" / "compare9_complete496_v1.txt"
FULLPOOL_MANIFEST = PROJECT_ROOT / "metrics" / "manifests" / "full_algae_dewatermark_v1.txt"
FULLPOOL_CV2_MANIFEST = PROJECT_ROOT / "metrics" / "manifests" / "full_algae_dewatermark_v1_cv2_readable_candidate.txt"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build a read-only file-level relation audit between Stage1 formal outputs, "
            "the MyEdge 168-test coupling manifest, and the full algae dewatermark pool. "
            "This script does not run Stage1, MyEdge sampling, metric evaluation, or output staging."
        )
    )
    parser.add_argument("--myedge-root", default=str(DEFAULT_MYEDGE_ROOT))
    parser.add_argument("--fullpool-root", default=str(DEFAULT_FULLPOOL_ROOT))
    parser.add_argument("--output-md", default=str(DEFAULT_OUTPUT_MD))
    parser.add_argument("--output-json", default=str(DEFAULT_OUTPUT_JSON))
    return parser.parse_args()


def read_lines(path: Path) -> List[str]:
    if not path.exists():
        return []
    return [
        line.strip().replace("\\", "/")
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines()
        if line.strip()
    ]


def read_csv_dicts(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def normalize_path_text(value: str) -> str:
    return str(value).strip().replace("\\", "/")


IMAGE_SUFFIXES = {
    ".bmp",
    ".gif",
    ".jpeg",
    ".jpg",
    ".png",
    ".tif",
    ".tiff",
    ".webp",
}


def stem_of(value: str) -> str:
    text = normalize_path_text(value)
    name = text.rsplit("/", 1)[-1]
    path = Path(name)
    if path.suffix.lower() in IMAGE_SUFFIXES:
        return path.stem
    return name


def filename_of(value: str) -> str:
    return normalize_path_text(value).rsplit("/", 1)[-1]


def count_duplicates(values: Iterable[str]) -> Dict[str, object]:
    counter = Counter(values)
    duplicates = {key: count for key, count in counter.items() if count > 1}
    return {
        "duplicate_key_count": len(duplicates),
        "duplicate_item_count": sum(duplicates.values()),
        "examples": dict(list(duplicates.items())[:10]),
    }


def sha256(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def file_fingerprint(path: Path) -> Dict[str, object]:
    if not path.exists():
        return {"exists": False, "size": None, "sha256": None}
    return {"exists": True, "size": path.stat().st_size, "sha256": sha256(path)}


def rel(path: Path, root: Path = PROJECT_ROOT) -> str:
    try:
        return str(path.relative_to(root)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def table_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def load_sets(fullpool_root: Path) -> Dict[str, object]:
    full502_lines = read_lines(FULL502_MANIFEST)
    compare496_lines = read_lines(COMPARE496_MANIFEST)
    fullpool_lines = read_lines(FULLPOOL_MANIFEST)
    fullpool_cv2_lines = read_lines(FULLPOOL_CV2_MANIFEST)

    return {
        "full502_lines": full502_lines,
        "full502_stems": {stem_of(line) for line in full502_lines},
        "compare496_lines": compare496_lines,
        "compare496_stems": {stem_of(line) for line in compare496_lines},
        "fullpool_lines": fullpool_lines,
        "fullpool_relpaths": {normalize_path_text(line) for line in fullpool_lines},
        "fullpool_filenames": {filename_of(line) for line in fullpool_lines},
        "fullpool_stems": {stem_of(line) for line in fullpool_lines},
        "fullpool_existing_relpaths": {
            normalize_path_text(line)
            for line in fullpool_lines
            if (fullpool_root / line).exists()
        },
        "fullpool_cv2_lines": fullpool_cv2_lines,
        "fullpool_cv2_relpaths": {normalize_path_text(line) for line in fullpool_cv2_lines},
        "fullpool_cv2_filenames": {filename_of(line) for line in fullpool_cv2_lines},
        "fullpool_cv2_stems": {stem_of(line) for line in fullpool_cv2_lines},
        "fullpool_cv2_existing_relpaths": {
            normalize_path_text(line)
            for line in fullpool_cv2_lines
            if (fullpool_root / line).exists()
        },
    }


def build_audit(myedge_root: Path, fullpool_root: Path) -> Dict[str, object]:
    manifest_path = (
        myedge_root
        / "docs"
        / "paper_assets"
        / "stage1_coupling"
        / "stage1_myedge_168_coupling_manifest_20260524.csv"
    )
    rows = read_csv_dicts(manifest_path)
    sets = load_sets(fullpool_root)

    row_audits: List[Dict[str, object]] = []
    for row in rows:
        stem = row.get("stem", "").strip()
        raw_filename = row.get("raw_input_filename", "").strip()
        raw_path = Path(row.get("raw_input_path", ""))
        gt_path = Path(row.get("annotation_path", ""))
        stage1_original_path = STAGE1_ORIGINAL_ROOT / raw_filename
        stage1_final_path = Path(row.get("stage1_final_path", ""))
        stage_paths = {
            "BPH": Path(row.get("stage1_bph_path", "")),
            "IMF1Ray": Path(row.get("stage1_imf1ray_path", "")),
            "RGHS": Path(row.get("stage1_rghs_path", "")),
            "CLAHE": Path(row.get("stage1_clahe_path", "")),
            "Fused": Path(row.get("stage1_fused_path", "")),
            "Final": stage1_final_path,
        }
        raw_fp = file_fingerprint(raw_path)
        stage1_original_fp = file_fingerprint(stage1_original_path)
        raw_stage1_sha_equal = (
            bool(raw_fp["exists"])
            and bool(stage1_original_fp["exists"])
            and raw_fp["sha256"] == stage1_original_fp["sha256"]
        )
        raw_stage1_size_equal = (
            bool(raw_fp["exists"])
            and bool(stage1_original_fp["exists"])
            and raw_fp["size"] == stage1_original_fp["size"]
        )

        row_audits.append(
            {
                "row_id": row.get("row_id", ""),
                "stem": stem,
                "raw_filename": raw_filename,
                "myedge_raw_exists": raw_path.exists(),
                "gt_exists": gt_path.exists(),
                "stage1_original_exists_by_filename": stage1_original_path.exists(),
                "stage1_all_stage_paths_exist": all(path.exists() for path in stage_paths.values()),
                "stage1_final_exists": stage1_final_path.exists(),
                "in_full502_clean_v1_by_stem": stem in sets["full502_stems"],
                "in_compare9_complete496_v1_by_stem": stem in sets["compare496_stems"],
                "in_fullpool_2774_by_filename": raw_filename in sets["fullpool_filenames"],
                "in_fullpool_2774_by_stem": stem in sets["fullpool_stems"],
                "in_fullpool_cv2_2770_by_filename": raw_filename in sets["fullpool_cv2_filenames"],
                "in_fullpool_cv2_2770_by_stem": stem in sets["fullpool_cv2_stems"],
                "myedge_raw_size": raw_fp["size"],
                "stage1_original_size": stage1_original_fp["size"],
                "myedge_raw_sha256": raw_fp["sha256"],
                "stage1_original_sha256": stage1_original_fp["sha256"],
                "raw_stage1_size_equal": raw_stage1_size_equal,
                "raw_stage1_sha256_equal": raw_stage1_sha_equal,
                "stage1_original_path": rel(stage1_original_path),
                "stage1_final_path": rel(stage1_final_path),
                "raw_input_path": str(raw_path).replace("\\", "/"),
                "annotation_path": str(gt_path).replace("\\", "/"),
            }
        )

    def count_true(key: str) -> int:
        return sum(1 for row in row_audits if bool(row.get(key)))

    stems = [str(row.get("stem", "")) for row in row_audits]
    filenames = [str(row.get("raw_filename", "")) for row in row_audits]
    stage1_originals = sorted(STAGE1_ORIGINAL_ROOT.glob("*"))
    stage1_original_stems = {path.stem for path in stage1_originals if path.is_file()}
    stage1_original_filenames = {path.name for path in stage1_originals if path.is_file()}

    counts = {
        "myedge_coupling_rows": len(row_audits),
        "myedge_unique_stems": len(set(stems)),
        "myedge_unique_filenames": len(set(filenames)),
        "myedge_raw_exists": count_true("myedge_raw_exists"),
        "gt_exists": count_true("gt_exists"),
        "stage1_original_exists_by_filename": count_true("stage1_original_exists_by_filename"),
        "stage1_all_stage_paths_exist": count_true("stage1_all_stage_paths_exist"),
        "stage1_final_exists": count_true("stage1_final_exists"),
        "in_full502_clean_v1_by_stem": count_true("in_full502_clean_v1_by_stem"),
        "in_compare9_complete496_v1_by_stem": count_true("in_compare9_complete496_v1_by_stem"),
        "in_fullpool_2774_by_filename": count_true("in_fullpool_2774_by_filename"),
        "in_fullpool_2774_by_stem": count_true("in_fullpool_2774_by_stem"),
        "in_fullpool_cv2_2770_by_filename": count_true("in_fullpool_cv2_2770_by_filename"),
        "in_fullpool_cv2_2770_by_stem": count_true("in_fullpool_cv2_2770_by_stem"),
        "raw_stage1_size_equal": count_true("raw_stage1_size_equal"),
        "raw_stage1_sha256_equal": count_true("raw_stage1_sha256_equal"),
        "stage1_original_file_count": len(stage1_original_filenames),
        "stage1_original_unique_stems": len(stage1_original_stems),
        "full502_clean_v1_count": len(sets["full502_lines"]),
        "compare9_complete496_v1_count": len(sets["compare496_lines"]),
        "fullpool_2774_count": len(sets["fullpool_lines"]),
        "fullpool_2774_existing_files": len(sets["fullpool_existing_relpaths"]),
        "fullpool_cv2_2770_count": len(sets["fullpool_cv2_lines"]),
        "fullpool_cv2_2770_existing_files": len(sets["fullpool_cv2_existing_relpaths"]),
    }

    missing_examples: Dict[str, List[Dict[str, object]]] = {}
    for key in [
        "myedge_raw_exists",
        "gt_exists",
        "stage1_original_exists_by_filename",
        "stage1_all_stage_paths_exist",
        "stage1_final_exists",
        "in_full502_clean_v1_by_stem",
        "in_compare9_complete496_v1_by_stem",
        "in_fullpool_2774_by_stem",
        "in_fullpool_cv2_2770_by_stem",
        "raw_stage1_sha256_equal",
    ]:
        missing_examples[key] = [
            {
                "row_id": row["row_id"],
                "stem": row["stem"],
                "raw_filename": row["raw_filename"],
                "myedge_raw_size": row["myedge_raw_size"],
                "stage1_original_size": row["stage1_original_size"],
            }
            for row in row_audits
            if not bool(row.get(key))
        ][:20]

    status = "ready"
    if counts["myedge_coupling_rows"] != 168:
        status = "unexpected_coupling_manifest_count"
    elif counts["stage1_all_stage_paths_exist"] == 168 and counts["gt_exists"] == 168:
        if counts["raw_stage1_sha256_equal"] != 168:
            status = "stage1_myedge_168_outputs_aligned_raw_bytes_differ_or_unproven"
        else:
            status = "stage1_myedge_168_outputs_and_raw_bytes_aligned"
    else:
        status = "stage1_myedge_168_alignment_incomplete"

    paper_safe_claims = [
        (
            "MyEdge ALGAE 168-row coupling manifest can be used as a future fixed-detector "
            "Stage1-to-edge protocol source only after explicit execution approval."
        ),
        (
            "All rows with existing Stage1 six-stage paths and GT support a future staged "
            "comparison of Original/Stage1 Final under the same MyEdge evaluation code."
        ),
        (
            "The current audit is file-level evidence only; it is not a downstream metric result "
            "and does not prove Stage1 improves edge detection."
        ),
    ]
    if counts["raw_stage1_sha256_equal"] != counts["myedge_coupling_rows"]:
        paper_safe_claims.append(
            "MyEdge raw inputs and Stage1 formal originals should be described as stem/path aligned, "
            "not byte-identical, unless a later provenance audit proves identity."
        )

    boundaries = [
        "No Stage1 full2770 run was executed.",
        "No MyEdge staging, sampling, eval.py, show.py, report sync, training, or metric recomputation was executed.",
        "Full-pool 2774/2770 membership by filename/stem is only a local filename relation; it does not establish identical acquisition split, GT identity, or reference-paper overlap.",
        "Manual full-pool review remains required before a clean full-pool protocol can be claimed.",
    ]

    next_actions = [
        "If the user explicitly approves high-risk MyEdge operations, run P1 fixed-detector Stage1 Final -> MSFI and Stage1 Final -> DiffusionEdge baseline exactly from the readiness pack.",
        "Before writing any dataset-same claim, add an original-id/provenance table that can connect the 2777 full pool, Stage1 formal 502, MyEdge 168, and reference-paper datasets beyond filename stems.",
        "Finish manual review for the 544 full-pool rows before creating any clean full-pool manifest.",
        "Keep Stage1 as task-driven structure-preserving support for MyEdge/MSFI, not as a standalone SOTA enhancement claim.",
    ]

    duplicate_audits = {
        "myedge_stem_duplicates": count_duplicates(stems),
        "myedge_filename_duplicates": count_duplicates(filenames),
        "full502_stem_duplicates": count_duplicates(stem_of(line) for line in sets["full502_lines"]),
        "compare496_stem_duplicates": count_duplicates(stem_of(line) for line in sets["compare496_lines"]),
        "fullpool_2774_stem_duplicates": count_duplicates(stem_of(line) for line in sets["fullpool_lines"]),
        "fullpool_cv2_2770_stem_duplicates": count_duplicates(stem_of(line) for line in sets["fullpool_cv2_lines"]),
    }

    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "status": status,
        "paths": {
            "project_root": str(PROJECT_ROOT),
            "myedge_root": str(myedge_root),
            "fullpool_root": str(fullpool_root),
            "coupling_manifest": str(manifest_path),
            "stage1_original_root": str(STAGE1_ORIGINAL_ROOT),
            "formal_result_root": str(FORMAL_RESULT_ROOT),
            "full502_manifest": str(FULL502_MANIFEST),
            "compare496_manifest": str(COMPARE496_MANIFEST),
            "fullpool_manifest": str(FULLPOOL_MANIFEST),
            "fullpool_cv2_manifest": str(FULLPOOL_CV2_MANIFEST),
        },
        "counts": counts,
        "duplicate_audits": duplicate_audits,
        "missing_or_negative_examples": missing_examples,
        "paper_safe_claims": paper_safe_claims,
        "boundaries": boundaries,
        "next_actions": next_actions,
        "rows": row_audits,
    }


def render_md(audit: Dict[str, object]) -> str:
    counts: Dict[str, int] = audit["counts"]  # type: ignore[assignment]
    paths: Dict[str, str] = audit["paths"]  # type: ignore[assignment]
    duplicate_audits: Dict[str, object] = audit["duplicate_audits"]  # type: ignore[assignment]
    missing: Dict[str, Sequence[Dict[str, object]]] = audit["missing_or_negative_examples"]  # type: ignore[assignment]

    count_rows = [
        ("MyEdge coupling rows", counts["myedge_coupling_rows"]),
        ("MyEdge raw exists", counts["myedge_raw_exists"]),
        ("GT exists", counts["gt_exists"]),
        ("Stage1 original exists by filename", counts["stage1_original_exists_by_filename"]),
        ("Stage1 all six stage paths exist", counts["stage1_all_stage_paths_exist"]),
        ("Stage1 Final exists", counts["stage1_final_exists"]),
        ("In full502_clean_v1 by stem", counts["in_full502_clean_v1_by_stem"]),
        ("In compare9_complete496_v1 by stem", counts["in_compare9_complete496_v1_by_stem"]),
        ("In full pool 2774 by filename", counts["in_fullpool_2774_by_filename"]),
        ("In full pool 2774 by stem", counts["in_fullpool_2774_by_stem"]),
        ("In full pool cv2-readable 2770 by filename", counts["in_fullpool_cv2_2770_by_filename"]),
        ("In full pool cv2-readable 2770 by stem", counts["in_fullpool_cv2_2770_by_stem"]),
        ("MyEdge raw and Stage1 original same size", counts["raw_stage1_size_equal"]),
        ("MyEdge raw and Stage1 original same SHA256", counts["raw_stage1_sha256_equal"]),
    ]
    table = ["| Item | Count |", "|---|---:|"]
    table.extend(f"| {table_escape(name)} | {value} |" for name, value in count_rows)

    duplicate_rows = ["| Set | Duplicate keys | Duplicate items | Example |", "|---|---:|---:|---|"]
    for name, info in duplicate_audits.items():
        data = info if isinstance(info, dict) else {}
        examples = data.get("examples", {})
        duplicate_rows.append(
            "| {name} | {keys} | {items} | {examples} |".format(
                name=table_escape(name),
                keys=data.get("duplicate_key_count", ""),
                items=data.get("duplicate_item_count", ""),
                examples=table_escape(examples),
            )
        )

    negative_sections: List[str] = []
    for key, examples in missing.items():
        if not examples:
            continue
        rows = ["| row_id | stem | raw_filename | MyEdge size | Stage1 original size |", "|---:|---|---|---:|---:|"]
        for item in examples[:10]:
            rows.append(
                "| {row_id} | {stem} | {filename} | {myedge_size} | {stage1_size} |".format(
                    row_id=table_escape(item.get("row_id", "")),
                    stem=table_escape(item.get("stem", "")),
                    filename=table_escape(item.get("raw_filename", "")),
                    myedge_size=table_escape(item.get("myedge_raw_size", "")),
                    stage1_size=table_escape(item.get("stage1_original_size", "")),
                )
            )
        negative_sections.append(f"### Negative examples: `{key}`\n\n" + "\n".join(rows))

    claims = "\n".join(f"- {item}" for item in audit["paper_safe_claims"])  # type: ignore[index]
    boundaries = "\n".join(f"- {item}" for item in audit["boundaries"])  # type: ignore[index]
    next_actions = "\n".join(f"- {item}" for item in audit["next_actions"])  # type: ignore[index]

    return f"""# Stage1-MyEdge 文件级关系审计（只读）

生成时间：`{audit["generated_at"]}`

状态：`{audit["status"]}`

本审计只读取本地 manifest 和文件元数据，用于确认 Stage1 正式结果、MyEdge 168 测试集、完整去水印藻类图像池之间的文件级关系。它不运行 Stage1，不运行 MyEdge，不生成指标，不生成图表。

## 输入路径

| Role | Path |
|---|---|
| Stage1 root | `{table_escape(paths["project_root"])}` |
| MyEdge root | `{table_escape(paths["myedge_root"])}` |
| Full algae pool root | `{table_escape(paths["fullpool_root"])}` |
| Coupling manifest | `{table_escape(paths["coupling_manifest"])}` |
| Stage1 original root | `{table_escape(paths["stage1_original_root"])}` |
| Stage1 formal result root | `{table_escape(paths["formal_result_root"])}` |
| full502 manifest | `{table_escape(paths["full502_manifest"])}` |
| compare496 manifest | `{table_escape(paths["compare496_manifest"])}` |
| full pool manifest | `{table_escape(paths["fullpool_manifest"])}` |
| full pool cv2-readable manifest | `{table_escape(paths["fullpool_cv2_manifest"])}` |

## 核心计数

{chr(10).join(table)}

## 重复键检查

{chr(10).join(duplicate_rows)}

## 可以写入论文/文档的安全表述

{claims}

## 不能越界的地方

{boundaries}

## 下一步动作

{next_actions}

## 负例/边界样例

{chr(10).join(negative_sections) if negative_sections else "无。"}
"""


def main() -> None:
    args = parse_args()
    myedge_root = Path(args.myedge_root)
    fullpool_root = Path(args.fullpool_root)
    output_md = Path(args.output_md)
    output_json = Path(args.output_json)

    audit = build_audit(myedge_root=myedge_root, fullpool_root=fullpool_root)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
    output_md.write_text(render_md(audit), encoding="utf-8")
    print(f"Wrote {output_md}")
    print(f"Wrote {output_json}")
    print(f"status={audit['status']}")


if __name__ == "__main__":
    main()
