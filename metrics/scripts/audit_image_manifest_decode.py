from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional

import cv2
import numpy as np


THIS_DIR = Path(__file__).resolve().parent
METRICS_DIR = THIS_DIR.parent
PROJECT_ROOT = METRICS_DIR.parent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Audit image decode, dimensions, channels, and dtypes for a manifest inventory. "
            "This is a data audit only; it does not run enhancement or evaluation."
        )
    )
    parser.add_argument(
        "--inventory",
        default=str(PROJECT_ROOT / "metrics" / "manifests" / "full_algae_dewatermark_v1_inventory.tsv"),
        help="TSV inventory with absolute_path and include_candidate columns.",
    )
    parser.add_argument(
        "--output-prefix",
        default=str(PROJECT_ROOT / "metrics" / "manifests" / "full_algae_dewatermark_v1_decode_audit"),
        help="Output prefix. The script writes .tsv, .summary.json, and .summary.md.",
    )
    parser.add_argument(
        "--readable-manifest",
        default=str(PROJECT_ROOT / "metrics" / "manifests" / "full_algae_dewatermark_v1_cv2_readable_candidate.txt"),
        help="Manifest containing candidate images that OpenCV can decode.",
    )
    parser.add_argument(
        "--failure-output",
        default=str(PROJECT_ROOT / "metrics" / "manifests" / "full_algae_dewatermark_v1_decode_failures.tsv"),
        help="TSV listing files that failed OpenCV decode or existence checks.",
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


def decode_image(path: Path) -> np.ndarray:
    data = np.fromfile(str(path), dtype=np.uint8)
    image = cv2.imdecode(data, cv2.IMREAD_UNCHANGED)
    if image is None:
        raise RuntimeError("cv2.imdecode returned None")
    return image


def read_magic(path: Path, length: int = 12) -> tuple[str, str]:
    data = path.read_bytes()[:length]
    magic_hex = data.hex(" ")
    magic_ascii = "".join(chr(b) if 32 <= b <= 126 else "." for b in data)
    return magic_hex, magic_ascii


def infer_channels(image: np.ndarray) -> int:
    if image.ndim == 2:
        return 1
    if image.ndim == 3:
        return int(image.shape[2])
    return 0


def infer_color_category(channels: int) -> str:
    if channels == 1:
        return "grayscale"
    if channels == 3:
        return "color_3ch"
    if channels == 4:
        return "color_alpha_4ch"
    return "other"


def finite_ratio(width: int, height: int) -> str:
    if height <= 0:
        return "nan"
    value = width / height
    if not math.isfinite(value):
        return "nan"
    return f"{value:.8g}"


def audit_rows(rows: Iterable[Dict[str, str]]) -> List[Dict[str, object]]:
    output: List[Dict[str, object]] = []
    for row in rows:
        absolute_path = Path(row.get("absolute_path", ""))
        include_candidate = parse_bool(row.get("include_candidate"))
        result: Dict[str, object] = {
            "include_candidate": str(include_candidate),
            "relative_path": row.get("relative_path", ""),
            "top_level_folder": row.get("top_level_folder", ""),
            "file_name": row.get("file_name", ""),
            "extension": row.get("extension", "").lower(),
            "size_bytes": row.get("size_bytes", ""),
            "absolute_path": str(absolute_path),
            "exists": "False",
            "readable": "False",
            "width": "",
            "height": "",
            "channels": "",
            "dtype": "",
            "ndim": "",
            "shape": "",
            "color_category": "",
            "aspect_ratio": "",
            "megapixels": "",
            "magic_hex": "",
            "magic_ascii": "",
            "error": "",
        }
        try:
            if not absolute_path.exists():
                raise FileNotFoundError("file does not exist")
            result["exists"] = "True"
            magic_hex, magic_ascii = read_magic(absolute_path)
            result["magic_hex"] = magic_hex
            result["magic_ascii"] = magic_ascii
            image = decode_image(absolute_path)
            height, width = int(image.shape[0]), int(image.shape[1])
            channels = infer_channels(image)
            result.update(
                {
                    "readable": "True",
                    "width": str(width),
                    "height": str(height),
                    "channels": str(channels),
                    "dtype": str(image.dtype),
                    "ndim": str(image.ndim),
                    "shape": "x".join(str(x) for x in image.shape),
                    "color_category": infer_color_category(channels),
                    "aspect_ratio": finite_ratio(width, height),
                    "megapixels": f"{(width * height) / 1_000_000:.8g}",
                }
            )
        except Exception as exc:  # pragma: no cover - exercised by bad data.
            result["error"] = f"{type(exc).__name__}: {exc}"
        output.append(result)
    return output


def write_tsv(path: Path, rows: List[Dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "include_candidate",
        "relative_path",
        "top_level_folder",
        "file_name",
        "extension",
        "size_bytes",
        "absolute_path",
        "exists",
        "readable",
        "width",
        "height",
        "channels",
        "dtype",
        "ndim",
        "shape",
        "color_category",
        "aspect_ratio",
        "megapixels",
        "magic_hex",
        "magic_ascii",
        "error",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(rows)


def numeric_values(rows: Iterable[Dict[str, object]], field: str) -> List[float]:
    values: List[float] = []
    for row in rows:
        try:
            value = float(str(row.get(field, "")))
        except ValueError:
            continue
        if math.isfinite(value):
            values.append(value)
    return values


def summarize_subset(rows: List[Dict[str, object]]) -> Dict[str, object]:
    readable_rows = [row for row in rows if row.get("readable") == "True"]
    failed_rows = [row for row in rows if row.get("readable") != "True"]
    missing_rows = [row for row in rows if row.get("exists") != "True"]
    widths = numeric_values(readable_rows, "width")
    heights = numeric_values(readable_rows, "height")
    megapixels = numeric_values(readable_rows, "megapixels")
    aspect_ratios = numeric_values(readable_rows, "aspect_ratio")

    shape_counts = Counter(str(row.get("shape", "")) for row in readable_rows)
    channel_counts = Counter(str(row.get("channels", "")) for row in readable_rows)
    dtype_counts = Counter(str(row.get("dtype", "")) for row in readable_rows)
    category_counts = Counter(str(row.get("color_category", "")) for row in readable_rows)
    extension_counts = Counter(str(row.get("extension", "")) for row in rows)

    return {
        "rows": len(rows),
        "readable": len(readable_rows),
        "decode_failures": len(failed_rows),
        "missing_files": len(missing_rows),
        "width_min": int(min(widths)) if widths else None,
        "width_max": int(max(widths)) if widths else None,
        "height_min": int(min(heights)) if heights else None,
        "height_max": int(max(heights)) if heights else None,
        "megapixels_min": min(megapixels) if megapixels else None,
        "megapixels_max": max(megapixels) if megapixels else None,
        "aspect_ratio_min": min(aspect_ratios) if aspect_ratios else None,
        "aspect_ratio_max": max(aspect_ratios) if aspect_ratios else None,
        "extension_counts": dict(sorted(extension_counts.items())),
        "channel_counts": dict(sorted(channel_counts.items())),
        "dtype_counts": dict(sorted(dtype_counts.items())),
        "color_category_counts": dict(sorted(category_counts.items())),
        "top_shapes": [{"shape": shape, "count": count} for shape, count in shape_counts.most_common(20)],
        "failed_examples": [
            {
                "relative_path": str(row.get("relative_path", "")),
                "absolute_path": str(row.get("absolute_path", "")),
                "error": str(row.get("error", "")),
            }
            for row in failed_rows[:20]
        ],
    }


def summarize_by_folder(rows: List[Dict[str, object]]) -> List[Dict[str, object]]:
    groups: Dict[str, List[Dict[str, object]]] = defaultdict(list)
    for row in rows:
        groups[str(row.get("top_level_folder", ""))].append(row)

    output: List[Dict[str, object]] = []
    for folder, folder_rows in sorted(groups.items(), key=lambda item: item[0].lower()):
        readable_rows = [row for row in folder_rows if row.get("readable") == "True"]
        shape_counts = Counter(str(row.get("shape", "")) for row in readable_rows)
        output.append(
            {
                "top_level_folder": folder,
                "rows": len(folder_rows),
                "readable": len(readable_rows),
                "decode_failures": len(folder_rows) - len(readable_rows),
                "dominant_shape": shape_counts.most_common(1)[0][0] if shape_counts else "",
                "dominant_shape_count": shape_counts.most_common(1)[0][1] if shape_counts else 0,
                "unique_shapes": len(shape_counts),
            }
        )
    return output


def write_folder_summary(path: Path, rows: List[Dict[str, object]]) -> None:
    fieldnames = [
        "top_level_folder",
        "rows",
        "readable",
        "decode_failures",
        "dominant_shape",
        "dominant_shape_count",
        "unique_shapes",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(rows)


def write_readable_manifest(path: Path, rows: List[Dict[str, object]]) -> None:
    path.write_text(
        "\n".join(str(row.get("relative_path", "")) for row in rows if row.get("include_candidate") == "True" and row.get("readable") == "True")
        + "\n",
        encoding="utf-8",
    )


def write_failures(path: Path, rows: List[Dict[str, object]]) -> None:
    fieldnames = [
        "include_candidate",
        "relative_path",
        "absolute_path",
        "extension",
        "size_bytes",
        "exists",
        "readable",
        "magic_hex",
        "magic_ascii",
        "error",
    ]
    failures = [row for row in rows if row.get("readable") != "True"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for row in failures:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def write_summary_md(path: Path, summary: Dict[str, object], folder_summary_name: str) -> None:
    all_images = summary["all_images"]
    candidate = summary["candidate_images"]
    root = summary["root_level_images"]

    lines = [
        "# full_algae_dewatermark_v1 decode / dimension audit",
        "",
        f"Generated at: `{summary['generated_at']}`",
        "",
        "This is a data audit only. It does not run Stage1 enhancement, MyEdge evaluation, or any metric experiment.",
        "",
        "## Summary",
        "",
        "| Scope | Rows | Readable | Decode failures | Missing files | Width range | Height range |",
        "| --- | ---: | ---: | ---: | ---: | --- | --- |",
        (
            f"| All images | {all_images['rows']} | {all_images['readable']} | {all_images['decode_failures']} | "
            f"{all_images['missing_files']} | {all_images['width_min']}-{all_images['width_max']} | "
            f"{all_images['height_min']}-{all_images['height_max']} |"
        ),
        (
            f"| Candidate images | {candidate['rows']} | {candidate['readable']} | {candidate['decode_failures']} | "
            f"{candidate['missing_files']} | {candidate['width_min']}-{candidate['width_max']} | "
            f"{candidate['height_min']}-{candidate['height_max']} |"
        ),
        (
            f"| Root-level images | {root['rows']} | {root['readable']} | {root['decode_failures']} | "
            f"{root['missing_files']} | {root['width_min']}-{root['width_max']} | "
            f"{root['height_min']}-{root['height_max']} |"
        ),
        "",
        "## Candidate Channel / Dtype Counts",
        "",
        f"- Channels: `{candidate['channel_counts']}`",
        f"- Dtypes: `{candidate['dtype_counts']}`",
        f"- Color categories: `{candidate['color_category_counts']}`",
        "",
        "## Candidate Top Shapes",
        "",
        "| Shape | Count |",
        "| --- | ---: |",
    ]
    for item in candidate["top_shapes"][:10]:
        lines.append(f"| `{item['shape']}` | {item['count']} |")
    lines.extend(
        [
            "",
            "## Outputs",
            "",
            f"- Per-image audit TSV: `{summary['output_tsv_name']}`",
            f"- Folder summary TSV: `{folder_summary_name}`",
            f"- Machine summary JSON: `{summary['summary_json_name']}`",
            f"- OpenCV-readable candidate manifest: `{summary['readable_candidate_manifest_name']}`",
            f"- Decode failure list: `{summary['failure_output_name']}`",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    inventory_path = Path(args.inventory)
    output_prefix = Path(args.output_prefix)
    readable_manifest_path = Path(args.readable_manifest)
    failure_output_path = Path(args.failure_output)
    output_prefix.parent.mkdir(parents=True, exist_ok=True)
    readable_manifest_path.parent.mkdir(parents=True, exist_ok=True)
    failure_output_path.parent.mkdir(parents=True, exist_ok=True)

    source_rows = read_inventory(inventory_path, args.limit)
    audited_rows = audit_rows(source_rows)

    tsv_path = output_prefix.with_suffix(".tsv")
    json_path = output_prefix.with_suffix(".summary.json")
    md_path = output_prefix.with_suffix(".summary.md")
    folder_summary_path = output_prefix.with_name(output_prefix.name + "_folder_summary.tsv")

    write_tsv(tsv_path, audited_rows)
    write_readable_manifest(readable_manifest_path, audited_rows)
    write_failures(failure_output_path, audited_rows)

    candidate_rows = [row for row in audited_rows if row.get("include_candidate") == "True"]
    root_rows = [row for row in audited_rows if row.get("include_candidate") != "True"]
    folder_summary = summarize_by_folder(candidate_rows)
    write_folder_summary(folder_summary_path, folder_summary)

    summary = {
        "id": "full_algae_dewatermark_v1_decode_audit",
        "status": "decode_dimension_audit_completed",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "inventory": str(inventory_path),
        "output_tsv": str(tsv_path),
        "output_tsv_name": tsv_path.name,
        "folder_summary_tsv": str(folder_summary_path),
        "summary_md": str(md_path),
        "summary_json_name": json_path.name,
        "readable_candidate_manifest": str(readable_manifest_path),
        "readable_candidate_manifest_name": readable_manifest_path.name,
        "failure_output": str(failure_output_path),
        "failure_output_name": failure_output_path.name,
        "limit": args.limit,
        "all_images": summarize_subset(audited_rows),
        "candidate_images": summarize_subset(candidate_rows),
        "root_level_images": summarize_subset(root_rows),
    }
    json_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    write_summary_md(md_path, summary, folder_summary_path.name)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
