from __future__ import annotations

import argparse
import csv
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

from PIL import Image, ImageOps


THIS_DIR = Path(__file__).resolve().parent
METRICS_DIR = THIS_DIR.parent
PROJECT_ROOT = METRICS_DIR.parent
DEFAULT_MYEDGE_ROOT = Path(r"D:\Desktop\MyEdgeCodex")
DEFAULT_FULLPOOL_ROOT = Path(r"D:\Desktop\去水印所有藻类图像")
DEFAULT_DATE = datetime.now().date().strftime("%Y%m%d")
DEFAULT_OUTPUT_MD = PROJECT_ROOT / "docs" / f"stage1_myedge_visual_relation_audit_{DEFAULT_DATE}_cn.md"
DEFAULT_OUTPUT_JSON = PROJECT_ROOT / "docs" / f"stage1_myedge_visual_relation_audit_{DEFAULT_DATE}_cn.json"
DEFAULT_OUTPUT_TSV = (
    PROJECT_ROOT / "metrics" / "manifests" / f"stage1_myedge_visual_relation_candidates_{DEFAULT_DATE}.tsv"
)


STAGE1_ORIGINAL_ROOT = PROJECT_ROOT / "data" / "inputImg" / "Original"
FULL502_MANIFEST = PROJECT_ROOT / "metrics" / "manifests" / "full502_clean_v1.txt"
COMPARE496_MANIFEST = PROJECT_ROOT / "metrics" / "manifests" / "compare9_complete496_v1.txt"
FULLPOOL_MANIFEST = PROJECT_ROOT / "metrics" / "manifests" / "full_algae_dewatermark_v1.txt"
FULLPOOL_CV2_MANIFEST = PROJECT_ROOT / "metrics" / "manifests" / "full_algae_dewatermark_v1_cv2_readable_candidate.txt"


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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build a read-only visual-fingerprint relation audit between MyEdge 168 raw inputs, "
            "Stage1 formal originals, and the full algae dewatermark pool. This is a data audit, "
            "not enhancement, sampling, edge evaluation, or metric recomputation."
        )
    )
    parser.add_argument("--myedge-root", default=str(DEFAULT_MYEDGE_ROOT))
    parser.add_argument("--fullpool-root", default=str(DEFAULT_FULLPOOL_ROOT))
    parser.add_argument("--output-md", default=str(DEFAULT_OUTPUT_MD))
    parser.add_argument("--output-json", default=str(DEFAULT_OUTPUT_JSON))
    parser.add_argument("--output-tsv", default=str(DEFAULT_OUTPUT_TSV))
    parser.add_argument("--top-k", type=int, default=5)
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


def stem_of(value: str) -> str:
    text = normalize_path_text(value)
    name = text.rsplit("/", 1)[-1]
    path = Path(name)
    if path.suffix.lower() in IMAGE_SUFFIXES:
        return path.stem
    return name


def hamming(hex_a: Optional[str], hex_b: Optional[str]) -> Optional[int]:
    if not hex_a or not hex_b:
        return None
    return bin(int(hex_a, 16) ^ int(hex_b, 16)).count("1")


def bits_to_hex(bits: Iterable[bool]) -> str:
    value = 0
    for bit in bits:
        value = (value << 1) | int(bool(bit))
    return f"{value:016x}"


def load_image(path: Path) -> Image.Image:
    with Image.open(path) as img:
        img = ImageOps.exif_transpose(img)
        return img.convert("RGB")


def average_hash(img: Image.Image) -> str:
    gray = img.convert("L").resize((8, 8), Image.Resampling.LANCZOS)
    values = list(gray.getdata())
    mean = sum(values) / len(values)
    return bits_to_hex(v >= mean for v in values)


def difference_hash(img: Image.Image) -> str:
    gray = img.convert("L").resize((9, 8), Image.Resampling.LANCZOS)
    rows = [list(gray.getdata())[idx : idx + 9] for idx in range(0, 72, 9)]
    return bits_to_hex(row[col] > row[col + 1] for row in rows for col in range(8))


def thumb_vector(img: Image.Image) -> List[int]:
    gray = img.convert("L").resize((32, 32), Image.Resampling.LANCZOS)
    return list(gray.getdata())


def thumb_rmse(a: Optional[Sequence[int]], b: Optional[Sequence[int]]) -> Optional[float]:
    if a is None or b is None:
        return None
    if len(a) != len(b):
        return None
    mse = sum((int(x) - int(y)) ** 2 for x, y in zip(a, b)) / len(a)
    return round(math.sqrt(mse), 4)


def build_fingerprint(path: Path, item_id: str, group: str, relpath: str = "") -> Dict[str, object]:
    record: Dict[str, object] = {
        "id": item_id,
        "group": group,
        "path": str(path).replace("\\", "/"),
        "relpath": relpath.replace("\\", "/"),
        "exists": path.exists(),
        "read_ok": False,
        "width": None,
        "height": None,
        "mode": None,
        "ahash": None,
        "dhash": None,
        "thumb": None,
        "error": None,
    }
    if not path.exists():
        record["error"] = "missing"
        return record
    try:
        img = load_image(path)
        record.update(
            {
                "read_ok": True,
                "width": img.width,
                "height": img.height,
                "mode": "RGB",
                "ahash": average_hash(img),
                "dhash": difference_hash(img),
                "thumb": thumb_vector(img),
            }
        )
    except Exception as exc:  # pragma: no cover - audit should keep going.
        record["error"] = repr(exc)
    return record


def stripped_fingerprint(record: Dict[str, object]) -> Dict[str, object]:
    return {key: value for key, value in record.items() if key != "thumb"}


def compare_records(a: Dict[str, object], b: Dict[str, object]) -> Dict[str, object]:
    ah = hamming(a.get("ahash"), b.get("ahash"))  # type: ignore[arg-type]
    dh = hamming(a.get("dhash"), b.get("dhash"))  # type: ignore[arg-type]
    combined = None if ah is None or dh is None else ah + dh
    rmse = thumb_rmse(a.get("thumb"), b.get("thumb"))  # type: ignore[arg-type]
    same_dimensions = (
        a.get("width") is not None
        and b.get("width") is not None
        and a.get("width") == b.get("width")
        and a.get("height") == b.get("height")
    )
    if combined is None:
        band = "unreadable"
    elif combined == 0 and (rmse is not None and rmse <= 1.0):
        band = "exact_or_reencoded_visual_candidate"
    elif combined <= 8 and (rmse is not None and rmse <= 12.0):
        band = "strong_visual_candidate"
    elif combined <= 16 and (rmse is not None and rmse <= 24.0):
        band = "possible_visual_candidate"
    else:
        band = "weak_or_no_visual_candidate"
    return {
        "ahash_hamming": ah,
        "dhash_hamming": dh,
        "combined_hash_hamming": combined,
        "thumb_rmse_32": rmse,
        "same_dimensions": same_dimensions,
        "candidate_band": band,
    }


def compare_hashes_only(a: Dict[str, object], b: Dict[str, object]) -> Dict[str, object]:
    ah = hamming(a.get("ahash"), b.get("ahash"))  # type: ignore[arg-type]
    dh = hamming(a.get("dhash"), b.get("dhash"))  # type: ignore[arg-type]
    combined = None if ah is None or dh is None else ah + dh
    return {
        "ahash_hamming": ah,
        "dhash_hamming": dh,
        "combined_hash_hamming": combined,
    }


def best_matches(
    source: Dict[str, object],
    candidates: Sequence[Dict[str, object]],
    top_k: int,
) -> List[Dict[str, object]]:
    ranked: List[Tuple[int, str, Dict[str, object]]] = []
    for candidate in candidates:
        comp = compare_hashes_only(source, candidate)
        combined = comp["combined_hash_hamming"]
        if combined is None:
            continue
        ranked.append((int(combined), str(candidate.get("id", "")), {"candidate": candidate, "comparison": comp}))
    ranked.sort(key=lambda item: (item[0], item[1]))

    results: List[Dict[str, object]] = []
    for rank, (_, _, payload) in enumerate(ranked[:top_k], start=1):
        candidate = payload["candidate"]
        comp = compare_records(source, candidate)
        results.append(
            {
                "rank": rank,
                "candidate_id": candidate.get("id"),
                "candidate_group": candidate.get("group"),
                "candidate_relpath": candidate.get("relpath"),
                "candidate_path": candidate.get("path"),
                "candidate_width": candidate.get("width"),
                "candidate_height": candidate.get("height"),
                **comp,
            }
        )
    return results


def summarize_bands(items: Iterable[Dict[str, object]]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for item in items:
        band = str(item.get("candidate_band", "unknown"))
        counts[band] = counts.get(band, 0) + 1
    return dict(sorted(counts.items()))


def write_tsv(path: Path, rows: Sequence[Dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "source_group",
        "source_id",
        "source_stem",
        "source_path",
        "target_group",
        "rank",
        "candidate_id",
        "candidate_relpath",
        "candidate_width",
        "candidate_height",
        "ahash_hamming",
        "dhash_hamming",
        "combined_hash_hamming",
        "thumb_rmse_32",
        "same_dimensions",
        "candidate_band",
    ]
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def build_audit(myedge_root: Path, fullpool_root: Path, top_k: int) -> Tuple[Dict[str, object], List[Dict[str, object]]]:
    coupling_manifest = (
        myedge_root
        / "docs"
        / "paper_assets"
        / "stage1_coupling"
        / "stage1_myedge_168_coupling_manifest_20260524.csv"
    )
    coupling_rows = read_csv_dicts(coupling_manifest)
    fullpool_lines = read_lines(FULLPOOL_MANIFEST)
    fullpool_cv2_lines = read_lines(FULLPOOL_CV2_MANIFEST)
    full502_lines = read_lines(FULL502_MANIFEST)
    compare496_lines = read_lines(COMPARE496_MANIFEST)

    myedge_fps: List[Dict[str, object]] = []
    stage1_for_myedge_fps: List[Dict[str, object]] = []
    for row in coupling_rows:
        stem = row.get("stem", "")
        raw_filename = row.get("raw_input_filename", "")
        myedge_fps.append(build_fingerprint(Path(row.get("raw_input_path", "")), stem, "myedge_raw_168", raw_filename))
        stage1_for_myedge_fps.append(
            build_fingerprint(STAGE1_ORIGINAL_ROOT / raw_filename, stem, "stage1_original_for_myedge_168", raw_filename)
        )

    stage1_formal_fps = [
        build_fingerprint(STAGE1_ORIGINAL_ROOT / f"{stem}.jpg", stem, "stage1_original_full502", f"{stem}.jpg")
        for stem in full502_lines
    ]
    fullpool_fps = [
        build_fingerprint(fullpool_root / relpath, relpath, "fullpool_2774", relpath)
        for relpath in fullpool_lines
    ]
    fullpool_cv2_ids = {relpath.replace("\\", "/") for relpath in fullpool_cv2_lines}

    myedge_stage1_pairs: List[Dict[str, object]] = []
    for myedge_fp, stage1_fp in zip(myedge_fps, stage1_for_myedge_fps):
        comp = compare_records(myedge_fp, stage1_fp)
        myedge_stage1_pairs.append(
            {
                "stem": myedge_fp["id"],
                "myedge_path": myedge_fp["path"],
                "stage1_original_path": stage1_fp["path"],
                "myedge_width": myedge_fp["width"],
                "myedge_height": myedge_fp["height"],
                "stage1_width": stage1_fp["width"],
                "stage1_height": stage1_fp["height"],
                **comp,
            }
        )

    fullpool_readable = [item for item in fullpool_fps if item.get("read_ok")]
    myedge_best_fullpool: List[Dict[str, object]] = []
    tsv_rows: List[Dict[str, object]] = []
    for source in myedge_fps:
        matches = best_matches(source, fullpool_readable, top_k=top_k)
        myedge_best_fullpool.append({"source_id": source["id"], "source_path": source["path"], "matches": matches})
        for match in matches:
            tsv_rows.append(
                {
                    "source_group": "myedge_raw_168",
                    "source_id": source["id"],
                    "source_stem": stem_of(str(source["id"])),
                    "source_path": source["path"],
                    "target_group": "fullpool_2774",
                    **match,
                }
            )

    stage1_best_fullpool: List[Dict[str, object]] = []
    for source in stage1_formal_fps:
        matches = best_matches(source, fullpool_readable, top_k=1)
        stage1_best_fullpool.append({"source_id": source["id"], "source_path": source["path"], "matches": matches})
        for match in matches:
            tsv_rows.append(
                {
                    "source_group": "stage1_original_full502",
                    "source_id": source["id"],
                    "source_stem": stem_of(str(source["id"])),
                    "source_path": source["path"],
                    "target_group": "fullpool_2774",
                    **match,
                }
            )

    myedge_top1 = [item["matches"][0] for item in myedge_best_fullpool if item["matches"]]
    stage1_top1 = [item["matches"][0] for item in stage1_best_fullpool if item["matches"]]

    def count_read_ok(items: Sequence[Dict[str, object]]) -> int:
        return sum(1 for item in items if bool(item.get("read_ok")))

    def count_top1_band(items: Sequence[Dict[str, object]], band: str) -> int:
        return sum(1 for item in items if str(item.get("candidate_band")) == band)

    exact_stage1_pair = [
        item
        for item in myedge_stage1_pairs
        if item.get("candidate_band") == "exact_or_reencoded_visual_candidate"
    ]
    strong_stage1_pair = [
        item
        for item in myedge_stage1_pairs
        if item.get("candidate_band") in {"exact_or_reencoded_visual_candidate", "strong_visual_candidate"}
    ]

    exact_myedge_fullpool = [
        item
        for item in myedge_top1
        if item.get("candidate_band") == "exact_or_reencoded_visual_candidate"
    ]
    strong_myedge_fullpool = [
        item
        for item in myedge_top1
        if item.get("candidate_band") in {"exact_or_reencoded_visual_candidate", "strong_visual_candidate"}
    ]
    exact_stage1_fullpool = [
        item
        for item in stage1_top1
        if item.get("candidate_band") == "exact_or_reencoded_visual_candidate"
    ]
    strong_stage1_fullpool = [
        item
        for item in stage1_top1
        if item.get("candidate_band") in {"exact_or_reencoded_visual_candidate", "strong_visual_candidate"}
    ]

    status = "visual_candidates_only_not_proven_provenance"
    if len(exact_myedge_fullpool) == 168 or len(exact_stage1_fullpool) == 502:
        status = "high_confidence_visual_overlap_candidates_require_manual_provenance_review"

    audit: Dict[str, object] = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "status": status,
        "paths": {
            "project_root": str(PROJECT_ROOT),
            "myedge_root": str(myedge_root),
            "fullpool_root": str(fullpool_root),
            "coupling_manifest": str(coupling_manifest),
            "full502_manifest": str(FULL502_MANIFEST),
            "compare496_manifest": str(COMPARE496_MANIFEST),
            "fullpool_manifest": str(FULLPOOL_MANIFEST),
            "fullpool_cv2_manifest": str(FULLPOOL_CV2_MANIFEST),
        },
        "method": {
            "fingerprints": ["PIL RGB decode", "8x8 average hash", "9x8 difference hash", "32x32 grayscale RMSE"],
            "exact_or_reencoded_visual_candidate": "combined aHash+dHash hamming == 0 and 32x32 RMSE <= 1.0",
            "strong_visual_candidate": "combined aHash+dHash hamming <= 8 and 32x32 RMSE <= 12.0",
            "possible_visual_candidate": "combined aHash+dHash hamming <= 16 and 32x32 RMSE <= 24.0",
            "boundary": "Perceptual-hash candidates are review aids only; they do not prove provenance, identical source images, GT identity, or split overlap.",
        },
        "counts": {
            "myedge_rows": len(coupling_rows),
            "myedge_read_ok": count_read_ok(myedge_fps),
            "stage1_for_myedge_read_ok": count_read_ok(stage1_for_myedge_fps),
            "stage1_full502_rows": len(full502_lines),
            "stage1_full502_read_ok": count_read_ok(stage1_formal_fps),
            "compare496_rows": len(compare496_lines),
            "fullpool_2774_rows": len(fullpool_lines),
            "fullpool_2774_read_ok_by_pil": count_read_ok(fullpool_fps),
            "fullpool_cv2_2770_rows": len(fullpool_cv2_lines),
            "fullpool_cv2_2770_ids_seen": sum(1 for item in fullpool_fps if item.get("id") in fullpool_cv2_ids),
            "myedge_vs_stage1_exact_or_reencoded": len(exact_stage1_pair),
            "myedge_vs_stage1_strong_or_exact": len(strong_stage1_pair),
            "myedge_vs_fullpool_top1_exact_or_reencoded": len(exact_myedge_fullpool),
            "myedge_vs_fullpool_top1_strong_or_exact": len(strong_myedge_fullpool),
            "stage1_full502_vs_fullpool_top1_exact_or_reencoded": len(exact_stage1_fullpool),
            "stage1_full502_vs_fullpool_top1_strong_or_exact": len(strong_stage1_fullpool),
        },
        "band_counts": {
            "myedge_vs_stage1": summarize_bands(myedge_stage1_pairs),
            "myedge_vs_fullpool_top1": summarize_bands(myedge_top1),
            "stage1_full502_vs_fullpool_top1": summarize_bands(stage1_top1),
        },
        "examples": {
            "myedge_vs_stage1_first10": myedge_stage1_pairs[:10],
            "myedge_vs_fullpool_exact_or_strong_first20": [
                item for item in myedge_best_fullpool if item["matches"] and item["matches"][0] in strong_myedge_fullpool
            ][:20],
            "stage1_vs_fullpool_exact_or_strong_first20": [
                item for item in stage1_best_fullpool if item["matches"] and item["matches"][0] in strong_stage1_fullpool
            ][:20],
            "myedge_vs_fullpool_weak_first10": [
                item
                for item in myedge_best_fullpool
                if item["matches"] and item["matches"][0].get("candidate_band") == "weak_or_no_visual_candidate"
            ][:10],
        },
        "paper_safe_claims": [
            "MyEdge 168 and Stage1 formal originals are visually very close under perceptual hashes only if the exact/strong counts support it; this remains a candidate relation until manually reviewed.",
            "Full-pool visual candidate matches, if present, can guide provenance review and subset mapping, but cannot be cited as dataset identity without a manual source-id table.",
            "This audit is a data-provenance aid and not a downstream edge-detection result.",
        ],
        "boundaries": [
            "No Stage1 enhancement, full2770 run, MyEdge staging/sampling, eval.py, show.py, training, or metric recomputation was executed.",
            "Visual hash equality is not byte equality and does not prove same split, same GT, same annotation, same acquisition protocol, or reference-paper overlap.",
            "The full-pool manual review and clean manifest remain pending.",
        ],
        "next_actions": [
            "Use the TSV candidates to manually build an original-id/provenance table before any manuscript claim about shared data.",
            "If strong full-pool candidates are sparse, keep the 2777/2774/2770 full pool as an additional enhancement pool rather than claiming it contains the MyEdge 168 or reference-paper subsets.",
            "After provenance review, update the claim ledger and dataset description with confirmed, not inferred, relationships.",
        ],
        "fingerprints": {
            "myedge_raw_168": [stripped_fingerprint(item) for item in myedge_fps],
            "stage1_original_for_myedge_168": [stripped_fingerprint(item) for item in stage1_for_myedge_fps],
            "stage1_original_full502": [stripped_fingerprint(item) for item in stage1_formal_fps],
            "fullpool_2774": [stripped_fingerprint(item) for item in fullpool_fps],
        },
        "comparisons": {
            "myedge_vs_stage1_same_filename": myedge_stage1_pairs,
            "myedge_best_fullpool": myedge_best_fullpool,
            "stage1_full502_best_fullpool": stage1_best_fullpool,
        },
    }
    return audit, tsv_rows


def table_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def render_count_table(counts: Dict[str, object]) -> str:
    rows = ["| Item | Count |", "|---|---:|"]
    rows.extend(f"| {table_escape(key)} | {table_escape(value)} |" for key, value in counts.items())
    return "\n".join(rows)


def render_band_table(bands: Dict[str, Dict[str, int]]) -> str:
    rows = ["| Comparison | Band | Count |", "|---|---|---:|"]
    for comparison, counts in bands.items():
        for band, count in counts.items():
            rows.append(f"| {table_escape(comparison)} | {table_escape(band)} | {count} |")
    return "\n".join(rows)


def render_examples(items: Sequence[Dict[str, object]], max_rows: int = 10) -> str:
    rows = [
        "| source_id | rank | candidate | combined | rmse32 | band |",
        "|---|---:|---|---:|---:|---|",
    ]
    for item in items[:max_rows]:
        matches = item.get("matches", [])
        if not matches:
            continue
        match = matches[0]
        rows.append(
            "| {source} | {rank} | {candidate} | {combined} | {rmse} | {band} |".format(
                source=table_escape(item.get("source_id", "")),
                rank=table_escape(match.get("rank", "")),
                candidate=table_escape(match.get("candidate_relpath", "")),
                combined=table_escape(match.get("combined_hash_hamming", "")),
                rmse=table_escape(match.get("thumb_rmse_32", "")),
                band=table_escape(match.get("candidate_band", "")),
            )
        )
    return "\n".join(rows)


def render_md(audit: Dict[str, object], output_tsv: Path) -> str:
    paths: Dict[str, str] = audit["paths"]  # type: ignore[assignment]
    method: Dict[str, str] = audit["method"]  # type: ignore[assignment]
    examples: Dict[str, Sequence[Dict[str, object]]] = audit["examples"]  # type: ignore[assignment]
    claims = "\n".join(f"- {item}" for item in audit["paper_safe_claims"])  # type: ignore[index]
    boundaries = "\n".join(f"- {item}" for item in audit["boundaries"])  # type: ignore[index]
    next_actions = "\n".join(f"- {item}" for item in audit["next_actions"])  # type: ignore[index]

    return f"""# Stage1-MyEdge-fullpool 视觉关系审计（只读）

生成时间：`{audit["generated_at"]}`

状态：`{audit["status"]}`

本审计用 PIL 读取本地图片，计算 aHash、dHash 和 32x32 灰度缩略图 RMSE，用来辅助判断 MyEdge 168、Stage1 formal originals 与完整去水印图像池之间是否存在视觉级候选关系。它不运行 Stage1，不运行 MyEdge，不生成边缘检测指标，不生成新图表。

## 输入路径

| Role | Path |
|---|---|
| Stage1 root | `{table_escape(paths["project_root"])}` |
| MyEdge root | `{table_escape(paths["myedge_root"])}` |
| Full algae pool root | `{table_escape(paths["fullpool_root"])}` |
| Coupling manifest | `{table_escape(paths["coupling_manifest"])}` |
| full502 manifest | `{table_escape(paths["full502_manifest"])}` |
| compare496 manifest | `{table_escape(paths["compare496_manifest"])}` |
| fullpool manifest | `{table_escape(paths["fullpool_manifest"])}` |
| fullpool cv2-readable manifest | `{table_escape(paths["fullpool_cv2_manifest"])}` |
| candidate TSV | `{table_escape(output_tsv)}` |

## 判定口径

- exact/reencoded candidate：{method["exact_or_reencoded_visual_candidate"]}
- strong candidate：{method["strong_visual_candidate"]}
- possible candidate：{method["possible_visual_candidate"]}
- 边界：{method["boundary"]}

## 核心计数

{render_count_table(audit["counts"])}

## 候选等级分布

{render_band_table(audit["band_counts"])}

## 强候选样例：MyEdge raw -> fullpool

{render_examples(examples["myedge_vs_fullpool_exact_or_strong_first20"])}

## 强候选样例：Stage1 formal original -> fullpool

{render_examples(examples["stage1_vs_fullpool_exact_or_strong_first20"])}

## 可以写的安全表述

{claims}

## 不能越界的地方

{boundaries}

## 下一步动作

{next_actions}
"""


def main() -> None:
    args = parse_args()
    myedge_root = Path(args.myedge_root)
    fullpool_root = Path(args.fullpool_root)
    output_md = Path(args.output_md)
    output_json = Path(args.output_json)
    output_tsv = Path(args.output_tsv)

    audit, tsv_rows = build_audit(myedge_root=myedge_root, fullpool_root=fullpool_root, top_k=args.top_k)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
    output_md.write_text(render_md(audit, output_tsv=output_tsv), encoding="utf-8")
    write_tsv(output_tsv, tsv_rows)
    print(f"Wrote {output_md}")
    print(f"Wrote {output_json}")
    print(f"Wrote {output_tsv}")
    print(f"status={audit['status']}")


if __name__ == "__main__":
    main()
