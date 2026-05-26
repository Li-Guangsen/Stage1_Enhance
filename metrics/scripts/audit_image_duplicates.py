from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

import cv2
import numpy as np
from PIL import Image, ImageOps


THIS_DIR = Path(__file__).resolve().parent
METRICS_DIR = THIS_DIR.parent
PROJECT_ROOT = METRICS_DIR.parent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Audit exact and perceptual duplicate candidates for the full algae image pool. "
            "This is a read-only data audit; it does not run enhancement or evaluation."
        )
    )
    parser.add_argument(
        "--inventory",
        default=str(PROJECT_ROOT / "metrics" / "manifests" / "full_algae_dewatermark_v1_inventory.tsv"),
        help="TSV inventory with relative_path, absolute_path, and include_candidate columns.",
    )
    parser.add_argument(
        "--output-prefix",
        default=str(PROJECT_ROOT / "metrics" / "manifests" / "full_algae_dewatermark_v1_duplicate_audit"),
        help="Output prefix. Writes .tsv, .summary.json, .summary.md, exact groups, and near pairs.",
    )
    parser.add_argument(
        "--phash-threshold",
        type=int,
        default=4,
        help="Maximum pHash Hamming distance for near-duplicate candidate pairs.",
    )
    parser.add_argument(
        "--dhash-threshold",
        type=int,
        default=8,
        help="Maximum dHash Hamming distance for near-duplicate candidate pairs.",
    )
    parser.add_argument(
        "--max-near-pairs",
        type=int,
        default=5000,
        help="Maximum near-duplicate pairs to write. The total count is still reported.",
    )
    parser.add_argument("--limit", type=int, default=None, help="Optional smoke limit.")
    return parser.parse_args()


def parse_bool(value: object) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def read_inventory(path: Path, limit: Optional[int]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            rows.append(dict(row))
            if limit is not None and len(rows) >= limit:
                break
    return rows


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def decode_cv2(path: Path) -> Optional[np.ndarray]:
    data = np.fromfile(str(path), dtype=np.uint8)
    image = cv2.imdecode(data, cv2.IMREAD_UNCHANGED)
    if image is None:
        return None
    return image


def decode_pillow_gray(path: Path) -> np.ndarray:
    with Image.open(path) as image:
        image = ImageOps.exif_transpose(image)
        return np.array(image.convert("L"))


def cv2_to_gray(image: np.ndarray) -> np.ndarray:
    if image.ndim == 2:
        return image
    if image.ndim == 3 and image.shape[2] == 4:
        return cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
    if image.ndim == 3 and image.shape[2] == 3:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    raise ValueError(f"unsupported image shape for hash: {image.shape}")


def decode_gray(path: Path) -> Tuple[np.ndarray, str]:
    image = decode_cv2(path)
    if image is not None:
        return cv2_to_gray(image), "cv2"
    return decode_pillow_gray(path), "pillow_fallback"


def bits_to_hex(bits: Iterable[bool]) -> str:
    value = 0
    count = 0
    for bit in bits:
        value = (value << 1) | int(bool(bit))
        count += 1
    width = max(1, math.ceil(count / 4))
    return f"{value:0{width}x}"


def int_from_hex(value: str) -> Optional[int]:
    if not value:
        return None
    return int(value, 16)


def average_hash(gray: np.ndarray, hash_size: int = 8) -> str:
    resized = cv2.resize(gray, (hash_size, hash_size), interpolation=cv2.INTER_AREA)
    mean_value = float(resized.mean())
    return bits_to_hex((int(pixel) >= mean_value for pixel in resized.flatten()))


def difference_hash(gray: np.ndarray, hash_size: int = 8) -> str:
    resized = cv2.resize(gray, (hash_size + 1, hash_size), interpolation=cv2.INTER_AREA)
    diffs = resized[:, :-1] > resized[:, 1:]
    return bits_to_hex(diffs.flatten())


def perceptual_hash(gray: np.ndarray, hash_size: int = 8, highfreq_factor: int = 4) -> str:
    size = hash_size * highfreq_factor
    resized = cv2.resize(gray, (size, size), interpolation=cv2.INTER_AREA).astype(np.float32)
    dct = cv2.dct(resized)
    block = dct[:hash_size, :hash_size]
    flattened = block.flatten()
    median = float(np.median(flattened[1:])) if len(flattened) > 1 else float(np.median(flattened))
    return bits_to_hex((float(value) > median for value in flattened))


def hamming_hex(left: str, right: str) -> Optional[int]:
    left_int = int_from_hex(left)
    right_int = int_from_hex(right)
    if left_int is None or right_int is None:
        return None
    return (left_int ^ right_int).bit_count()


def image_sha256(gray: np.ndarray) -> str:
    normalized = np.ascontiguousarray(gray)
    digest = hashlib.sha256()
    digest.update(str(normalized.shape).encode("ascii"))
    digest.update(str(normalized.dtype).encode("ascii"))
    digest.update(normalized.tobytes())
    return digest.hexdigest()


def audit_rows(rows: List[Dict[str, str]]) -> List[Dict[str, object]]:
    output: List[Dict[str, object]] = []
    for index, row in enumerate(rows):
        path = Path(row.get("absolute_path", ""))
        result: Dict[str, object] = {
            "row_index": index,
            "include_candidate": str(parse_bool(row.get("include_candidate"))),
            "relative_path": row.get("relative_path", ""),
            "top_level_folder": row.get("top_level_folder", ""),
            "file_name": row.get("file_name", ""),
            "extension": row.get("extension", "").lower(),
            "size_bytes": row.get("size_bytes", ""),
            "absolute_path": str(path),
            "exists": "False",
            "hash_readable": "False",
            "decoder": "",
            "width": "",
            "height": "",
            "file_sha256": "",
            "gray_image_sha256": "",
            "ahash64": "",
            "dhash64": "",
            "phash64": "",
            "error": "",
        }
        try:
            if not path.exists():
                raise FileNotFoundError("file does not exist")
            result["exists"] = "True"
            result["file_sha256"] = sha256_file(path)
            gray, decoder = decode_gray(path)
            result["decoder"] = decoder
            result["height"] = str(int(gray.shape[0]))
            result["width"] = str(int(gray.shape[1]))
            result["gray_image_sha256"] = image_sha256(gray)
            result["ahash64"] = average_hash(gray)
            result["dhash64"] = difference_hash(gray)
            result["phash64"] = perceptual_hash(gray)
            result["hash_readable"] = "True"
        except Exception as exc:  # pragma: no cover - exercised by bad data.
            result["error"] = f"{type(exc).__name__}: {exc}"
        output.append(result)
    return output


def write_tsv(path: Path, rows: List[Dict[str, object]], fieldnames: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(rows)


def group_by_field(rows: List[Dict[str, object]], field: str) -> Dict[str, List[Dict[str, object]]]:
    groups: Dict[str, List[Dict[str, object]]] = defaultdict(list)
    for row in rows:
        value = str(row.get(field, ""))
        if value:
            groups[value].append(row)
    return {key: value for key, value in groups.items() if len(value) > 1}


def exact_group_rows(groups: Dict[str, List[Dict[str, object]]], group_kind: str) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for group_index, (hash_value, members) in enumerate(sorted(groups.items()), start=1):
        candidate_count = sum(1 for row in members if row.get("include_candidate") == "True")
        top_folders = sorted({str(row.get("top_level_folder", "")) for row in members})
        paths = [str(row.get("relative_path", "")) for row in members]
        rows.append(
            {
                "group_kind": group_kind,
                "group_id": f"{group_kind}_{group_index:04d}",
                "hash": hash_value,
                "count": len(members),
                "candidate_count": candidate_count,
                "top_level_folder_count": len(top_folders),
                "top_level_folders": " | ".join(top_folders),
                "relative_paths": " | ".join(paths),
            }
        )
    return rows


def near_duplicate_pairs(
    rows: List[Dict[str, object]],
    phash_threshold: int,
    dhash_threshold: int,
    max_pairs: int,
) -> Tuple[List[Dict[str, object]], int, bool]:
    hash_rows = [row for row in rows if row.get("hash_readable") == "True"]
    pairs: List[Dict[str, object]] = []
    total = 0
    truncated = False
    for i in range(len(hash_rows)):
        left = hash_rows[i]
        for j in range(i + 1, len(hash_rows)):
            right = hash_rows[j]
            pdist = hamming_hex(str(left.get("phash64", "")), str(right.get("phash64", "")))
            ddist = hamming_hex(str(left.get("dhash64", "")), str(right.get("dhash64", "")))
            if pdist is None or ddist is None:
                continue
            if pdist <= phash_threshold and ddist <= dhash_threshold:
                total += 1
                if len(pairs) >= max_pairs:
                    truncated = True
                    continue
                adist = hamming_hex(str(left.get("ahash64", "")), str(right.get("ahash64", "")))
                same_top = str(left.get("top_level_folder", "")) == str(right.get("top_level_folder", ""))
                same_file_sha = str(left.get("file_sha256", "")) == str(right.get("file_sha256", ""))
                same_gray_sha = str(left.get("gray_image_sha256", "")) == str(right.get("gray_image_sha256", ""))
                pairs.append(
                    {
                        "pair_id": f"near_{total:05d}",
                        "phash_distance": pdist,
                        "dhash_distance": ddist,
                        "ahash_distance": "" if adist is None else adist,
                        "same_top_level_folder": str(same_top),
                        "same_file_sha256": str(same_file_sha),
                        "same_gray_image_sha256": str(same_gray_sha),
                        "include_candidate_a": left.get("include_candidate", ""),
                        "include_candidate_b": right.get("include_candidate", ""),
                        "top_level_folder_a": left.get("top_level_folder", ""),
                        "top_level_folder_b": right.get("top_level_folder", ""),
                        "relative_path_a": left.get("relative_path", ""),
                        "relative_path_b": right.get("relative_path", ""),
                    }
                )
    pairs.sort(key=lambda row: (int(row["phash_distance"]), int(row["dhash_distance"]), str(row["relative_path_a"])))
    return pairs, total, truncated


def summarize(
    rows: List[Dict[str, object]],
    exact_file_groups: List[Dict[str, object]],
    exact_gray_groups: List[Dict[str, object]],
    near_pairs: List[Dict[str, object]],
    near_total: int,
    near_truncated: bool,
    args: argparse.Namespace,
) -> Dict[str, object]:
    candidate_rows = [row for row in rows if row.get("include_candidate") == "True"]
    readable_rows = [row for row in rows if row.get("hash_readable") == "True"]
    unreadable_rows = [row for row in rows if row.get("hash_readable") != "True"]
    candidate_readable_rows = [row for row in candidate_rows if row.get("hash_readable") == "True"]
    candidate_unreadable_rows = [row for row in candidate_rows if row.get("hash_readable") != "True"]
    decoder_counts = Counter(str(row.get("decoder", "")) for row in readable_rows)

    exact_file_images = sum(int(row["count"]) for row in exact_file_groups)
    exact_gray_images = sum(int(row["count"]) for row in exact_gray_groups)
    candidate_exact_file_images = sum(int(row["candidate_count"]) for row in exact_file_groups)
    candidate_exact_gray_images = sum(int(row["candidate_count"]) for row in exact_gray_groups)

    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "inventory": str(Path(args.inventory)),
        "rows_total": len(rows),
        "candidate_rows": len(candidate_rows),
        "hash_readable_total": len(readable_rows),
        "hash_unreadable_total": len(unreadable_rows),
        "candidate_hash_readable": len(candidate_readable_rows),
        "candidate_hash_unreadable": len(candidate_unreadable_rows),
        "decoder_counts": dict(sorted(decoder_counts.items())),
        "exact_file_duplicate_groups": len(exact_file_groups),
        "exact_file_duplicate_images": exact_file_images,
        "candidate_exact_file_duplicate_images": candidate_exact_file_images,
        "exact_gray_duplicate_groups": len(exact_gray_groups),
        "exact_gray_duplicate_images": exact_gray_images,
        "candidate_exact_gray_duplicate_images": candidate_exact_gray_images,
        "near_duplicate_pair_thresholds": {
            "phash_hamming_max": args.phash_threshold,
            "dhash_hamming_max": args.dhash_threshold,
        },
        "near_duplicate_pairs_total": near_total,
        "near_duplicate_pairs_reported": len(near_pairs),
        "near_duplicate_pairs_truncated": near_truncated,
        "near_duplicate_pairs_max_reported": args.max_near_pairs,
        "boundary": (
            "Near-duplicate pairs are candidates for manual review, not automatic removal decisions. "
            "This audit does not change the current formal 502/496 protocols and does not run enhancement."
        ),
    }


def write_summary_md(path: Path, summary: Dict[str, object], output_paths: Dict[str, str]) -> None:
    thresholds = summary["near_duplicate_pair_thresholds"]
    lines = [
        "# full_algae_dewatermark_v1 duplicate / near-duplicate audit",
        "",
        f"日期：{datetime.now().date().isoformat()}",
        "",
        "本文是完整增强图像池的只读内容重复审计，不是增强实验结果。",
        "",
        "## Summary",
        "",
        f"- Total image rows: `{summary['rows_total']}`",
        f"- Candidate rows: `{summary['candidate_rows']}`",
        f"- Hash-readable rows: `{summary['hash_readable_total']}`",
        f"- Candidate hash-readable rows: `{summary['candidate_hash_readable']}`",
        f"- Decoder counts: `{summary['decoder_counts']}`",
        f"- Exact file duplicate groups: `{summary['exact_file_duplicate_groups']}`",
        f"- Exact file duplicate images: `{summary['exact_file_duplicate_images']}`",
        f"- Candidate exact file duplicate images: `{summary['candidate_exact_file_duplicate_images']}`",
        f"- Exact grayscale-image duplicate groups: `{summary['exact_gray_duplicate_groups']}`",
        f"- Exact grayscale-image duplicate images: `{summary['exact_gray_duplicate_images']}`",
        f"- Candidate exact grayscale-image duplicate images: `{summary['candidate_exact_gray_duplicate_images']}`",
        f"- Near-duplicate thresholds: `pHash <= {thresholds['phash_hamming_max']}`, `dHash <= {thresholds['dhash_hamming_max']}`",
        f"- Near-duplicate candidate pairs total: `{summary['near_duplicate_pairs_total']}`",
        f"- Near-duplicate candidate pairs reported: `{summary['near_duplicate_pairs_reported']}`",
        f"- Near-duplicate report truncated: `{summary['near_duplicate_pairs_truncated']}`",
        "",
        "## Outputs",
        "",
    ]
    for label, output_path in output_paths.items():
        lines.append(f"- {label}: `{output_path}`")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- Exact file duplicate means byte-level SHA-256 equality.",
            "- Exact grayscale-image duplicate means decoded grayscale pixels are identical after decoder normalization.",
            "- Near-duplicate pairs are only manual-review candidates; they are not automatic deletion or exclusion decisions.",
            "- This audit does not replace `full502_clean_v1` or `compare9_complete496_v1`, and it does not run Stage1 full-pool enhancement.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    output_prefix = Path(args.output_prefix)
    inventory_rows = read_inventory(Path(args.inventory), args.limit)
    rows = audit_rows(inventory_rows)

    audit_tsv = output_prefix.with_suffix(".tsv")
    exact_groups_tsv = output_prefix.with_name(output_prefix.name + "_exact_duplicate_groups.tsv")
    near_pairs_tsv = output_prefix.with_name(output_prefix.name + "_near_duplicate_pairs.tsv")
    summary_json = output_prefix.with_suffix(".summary.json")
    summary_md = output_prefix.with_suffix(".summary.md")

    row_fields = [
        "row_index",
        "include_candidate",
        "relative_path",
        "top_level_folder",
        "file_name",
        "extension",
        "size_bytes",
        "absolute_path",
        "exists",
        "hash_readable",
        "decoder",
        "width",
        "height",
        "file_sha256",
        "gray_image_sha256",
        "ahash64",
        "dhash64",
        "phash64",
        "error",
    ]
    write_tsv(audit_tsv, rows, row_fields)

    exact_file_groups = exact_group_rows(group_by_field(rows, "file_sha256"), "file_sha256")
    exact_gray_groups = exact_group_rows(group_by_field(rows, "gray_image_sha256"), "gray_image_sha256")
    exact_groups = exact_file_groups + exact_gray_groups
    exact_group_fields = [
        "group_kind",
        "group_id",
        "hash",
        "count",
        "candidate_count",
        "top_level_folder_count",
        "top_level_folders",
        "relative_paths",
    ]
    write_tsv(exact_groups_tsv, exact_groups, exact_group_fields)

    near_pairs, near_total, near_truncated = near_duplicate_pairs(
        rows=rows,
        phash_threshold=args.phash_threshold,
        dhash_threshold=args.dhash_threshold,
        max_pairs=args.max_near_pairs,
    )
    near_pair_fields = [
        "pair_id",
        "phash_distance",
        "dhash_distance",
        "ahash_distance",
        "same_top_level_folder",
        "same_file_sha256",
        "same_gray_image_sha256",
        "include_candidate_a",
        "include_candidate_b",
        "top_level_folder_a",
        "top_level_folder_b",
        "relative_path_a",
        "relative_path_b",
    ]
    write_tsv(near_pairs_tsv, near_pairs, near_pair_fields)

    summary = summarize(
        rows=rows,
        exact_file_groups=exact_file_groups,
        exact_gray_groups=exact_gray_groups,
        near_pairs=near_pairs,
        near_total=near_total,
        near_truncated=near_truncated,
        args=args,
    )
    summary_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    write_summary_md(
        summary_md,
        summary,
        {
            "per-image audit": str(audit_tsv.relative_to(PROJECT_ROOT)),
            "exact duplicate groups": str(exact_groups_tsv.relative_to(PROJECT_ROOT)),
            "near duplicate pairs": str(near_pairs_tsv.relative_to(PROJECT_ROOT)),
            "summary json": str(summary_json.relative_to(PROJECT_ROOT)),
        },
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
