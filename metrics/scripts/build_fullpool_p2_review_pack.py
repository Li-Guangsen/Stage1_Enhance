from __future__ import annotations

import argparse
import csv
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

from PIL import Image, ImageDraw, ImageFont, ImageOps


THIS_DIR = Path(__file__).resolve().parent
METRICS_DIR = THIS_DIR.parent
PROJECT_ROOT = METRICS_DIR.parent
DEFAULT_REVIEW_DIR = PROJECT_ROOT / "metrics" / "manifests" / "full_algae_dewatermark_v1_manual_review"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build a P2 visual review pack for full_algae_dewatermark_v1 manual review. "
            "This creates previews and machine suggestions only; it does not fill reviewer decisions."
        )
    )
    parser.add_argument(
        "--inventory",
        default=str(PROJECT_ROOT / "metrics" / "manifests" / "full_algae_dewatermark_v1_inventory.tsv"),
    )
    parser.add_argument("--near-review", default=str(DEFAULT_REVIEW_DIR / "near_duplicates_review.tsv"))
    parser.add_argument("--quality-review", default=str(DEFAULT_REVIEW_DIR / "quality_outliers_review.tsv"))
    parser.add_argument("--output-dir", default=str(DEFAULT_REVIEW_DIR / "p2_review_pack"))
    parser.add_argument("--quality-contact-sheet-chunk-size", type=int, default=40)
    return parser.parse_args()


def read_tsv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle, delimiter="\t")]


def write_tsv(path: Path, rows: Sequence[Dict[str, object]], fieldnames: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(rows)


def relative_to_absolute_map(inventory_rows: Sequence[Dict[str, str]]) -> Dict[str, Path]:
    mapping: Dict[str, Path] = {}
    for row in inventory_rows:
        relative_path = row.get("relative_path", "")
        absolute_path = row.get("absolute_path", "")
        if relative_path and absolute_path:
            mapping[relative_path] = Path(absolute_path)
    return mapping


def open_rgb(path: Path) -> Image.Image:
    image = Image.open(path)
    image = ImageOps.exif_transpose(image)
    if getattr(image, "is_animated", False):
        image.seek(0)
    return image.convert("RGB")


def thumbnail_canvas(image: Image.Image, label: str, size: Tuple[int, int] = (320, 260)) -> Image.Image:
    canvas = Image.new("RGB", size, "white")
    thumb = image.copy()
    thumb.thumbnail((size[0] - 16, size[1] - 52), Image.Resampling.LANCZOS)
    canvas.paste(thumb, ((size[0] - thumb.width) // 2, 8))
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.load_default()
    draw.text((8, size[1] - 38), label[:48], fill=(0, 0, 0), font=font)
    return canvas


def split_related_paths(value: str) -> List[str]:
    return [item.strip() for item in value.split("|") if item.strip()]


def evidence_value(evidence: str, key: str) -> str:
    match = re.search(rf"{re.escape(key)}=([^;]+)", evidence)
    return match.group(1).strip() if match else ""


def parse_flags(evidence: str) -> List[str]:
    flags = evidence_value(evidence, "flags")
    return [item.strip() for item in flags.split(",") if item.strip()]


def save_pair_preview(row: Dict[str, str], path_map: Dict[str, Path], output_dir: Path) -> str:
    issue_id = row["issue_id"]
    panels: List[Image.Image] = []
    for index, relative_path in enumerate(split_related_paths(row["related_paths"]), start=1):
        image = open_rgb(path_map[relative_path])
        panels.append(thumbnail_canvas(image, f"{issue_id}_{index}"))
    canvas = Image.new("RGB", (sum(panel.width for panel in panels), max(panel.height for panel in panels)), "white")
    x = 0
    for panel in panels:
        canvas.paste(panel, (x, 0))
        x += panel.width
    preview_path = output_dir / "previews" / f"{issue_id}.png"
    preview_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(preview_path)
    return str(preview_path.relative_to(PROJECT_ROOT))


def save_quality_preview(row: Dict[str, str], path_map: Dict[str, Path], output_dir: Path) -> str:
    issue_id = row["issue_id"]
    relative_path = row["relative_path"]
    flags = ",".join(parse_flags(row.get("evidence_summary", "")))
    image = open_rgb(path_map[relative_path])
    preview = thumbnail_canvas(image, f"{issue_id} {flags}")
    preview_path = output_dir / "previews" / f"{issue_id}.png"
    preview_path.parent.mkdir(parents=True, exist_ok=True)
    preview.save(preview_path)
    return str(preview_path.relative_to(PROJECT_ROOT))


def make_contact_sheet(preview_paths: Sequence[Path], output_path: Path, columns: int = 2) -> None:
    if not preview_paths:
        return
    images = [Image.open(path).convert("RGB") for path in preview_paths]
    cell_width = max(image.width for image in images)
    cell_height = max(image.height for image in images)
    rows = (len(images) + columns - 1) // columns
    canvas = Image.new("RGB", (columns * cell_width, rows * cell_height), "white")
    for index, image in enumerate(images):
        x = (index % columns) * cell_width
        y = (index // columns) * cell_height
        canvas.paste(image, (x, y))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output_path)


def near_duplicate_suggestion(row: Dict[str, str]) -> Tuple[str, str]:
    evidence = row.get("evidence_summary", "")
    same_top = evidence_value(evidence, "same_top_level_folder") == "True"
    phash_distance = evidence_value(evidence, "phash_distance")
    dhash_distance = evidence_value(evidence, "dhash_distance")
    if same_top:
        return (
            "needs_manual_visual_check",
            f"P2 near-duplicate candidate is within the same folder with pHash={phash_distance} and dHash={dhash_distance}; visually decide whether it is a repeated acquisition, valid variant, or duplicate.",
        )
    return (
        "keep_but_split_guard",
        f"P2 near-duplicate candidate crosses folders with pHash={phash_distance} and dHash={dhash_distance}; keep until taxonomy is checked, but record it for future split leakage guard.",
    )


def quality_suggestion(row: Dict[str, str]) -> Tuple[str, str]:
    flags = set(parse_flags(row.get("evidence_summary", "")))
    if "small_resolution" in flags or "large_resolution" in flags:
        return (
            "subset_label_only",
            "P2 quality outlier mainly indicates resolution scale variation; label it for data-coverage reporting and later robustness subsets before excluding.",
        )
    if "low_luminance" in flags or "high_luminance" in flags:
        return (
            "subset_label_only",
            "P2 quality outlier mainly indicates illumination variation; label it for degradation subsets or failure-case screening before excluding.",
        )
    if "low_saturation" in flags or "high_saturation" in flags:
        return (
            "subset_label_only",
            "P2 quality outlier mainly indicates color/saturation variation; label it for data-coverage and degradation subsets before excluding.",
        )
    if "low_aspect_ratio" in flags or "high_aspect_ratio" in flags:
        return (
            "subset_label_only",
            "P2 quality outlier mainly indicates aspect-ratio variation; label it for data-coverage reporting and split design before excluding.",
        )
    return (
        "needs_manual_visual_check",
        "P2 quality outlier requires visual confirmation before deciding whether it is a valid hard sample, subset label, or clean-pool exclusion.",
    )


def build_recommendations(
    near_rows: Sequence[Dict[str, str]],
    quality_rows: Sequence[Dict[str, str]],
    path_map: Dict[str, Path],
    output_dir: Path,
) -> List[Dict[str, object]]:
    recommendations: List[Dict[str, object]] = []
    for row in near_rows:
        preview = save_pair_preview(row, path_map, output_dir)
        suggestion, reason = near_duplicate_suggestion(row)
        recommendations.append(
            {
                "issue_id": row["issue_id"],
                "issue_type": row["issue_type"],
                "priority": row["priority"],
                "relative_path": row.get("relative_path", ""),
                "related_paths": row.get("related_paths", ""),
                "evidence_summary": row.get("evidence_summary", ""),
                "machine_suggestion": suggestion,
                "suggestion_reason": reason,
                "preview_path": preview,
                "review_status": row["review_status"],
                "reviewer_decision": row.get("reviewer_decision", ""),
            }
        )
    for row in quality_rows:
        preview = save_quality_preview(row, path_map, output_dir)
        suggestion, reason = quality_suggestion(row)
        recommendations.append(
            {
                "issue_id": row["issue_id"],
                "issue_type": row["issue_type"],
                "priority": row["priority"],
                "relative_path": row.get("relative_path", ""),
                "related_paths": row.get("related_paths", ""),
                "evidence_summary": row.get("evidence_summary", ""),
                "machine_suggestion": suggestion,
                "suggestion_reason": reason,
                "preview_path": preview,
                "review_status": row["review_status"],
                "reviewer_decision": row.get("reviewer_decision", ""),
            }
        )
    return recommendations


def write_index_md(path: Path, summary: Dict[str, object], outputs: Dict[str, object]) -> None:
    lines = [
        "# full_algae_dewatermark_v1 P2 review pack",
        "",
        f"日期：{datetime.now().date().isoformat()}",
        "",
        "本文是 P2 人工复核辅助包，不是最终人工决策，不修改 manifest，也不运行增强。",
        "",
        "## Summary",
        "",
        f"- Near duplicate P2 rows: `{summary['near_duplicate_pair_rows']}`",
        f"- Quality outlier P2 rows: `{summary['quality_outlier_rows']}`",
        f"- Total P2 rows: `{summary['total_p2_rows']}`",
        f"- Current review status: `{summary['review_status']}`",
        "",
        "## Outputs",
        "",
    ]
    for label, value in outputs.items():
        if isinstance(value, list):
            lines.append(f"- {label}:")
            for item in value:
                lines.append(f"  - `{item}`")
        else:
            lines.append(f"- {label}: `{value}`")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- `machine_suggestion` 只是复核建议，不是 `reviewer_decision`。",
            "- P2 质量异常更适合优先作为数据覆盖、退化分层、失败案例或有效难例候选，而不是自动排除。",
            "- P2 近重复候选更适合优先形成未来 split leakage guard，而不是自动删除。",
            "- 不得根据本包直接改写 manifest、删除原图或转换原图。",
            "- 只有人工填写 review sheets 并通过 `validate_fullpool_manual_review.py` 后，才能进入清洗规则派生。",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def chunked(values: Sequence[Path], size: int) -> List[List[Path]]:
    return [list(values[index : index + size]) for index in range(0, len(values), size)]


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    path_map = relative_to_absolute_map(read_tsv(Path(args.inventory)))
    near_rows = [row for row in read_tsv(Path(args.near_review)) if row.get("priority") == "P2"]
    quality_rows = [row for row in read_tsv(Path(args.quality_review)) if row.get("priority") == "P2"]
    recommendations = build_recommendations(near_rows, quality_rows, path_map, output_dir)

    fieldnames = [
        "issue_id",
        "issue_type",
        "priority",
        "relative_path",
        "related_paths",
        "evidence_summary",
        "machine_suggestion",
        "suggestion_reason",
        "preview_path",
        "review_status",
        "reviewer_decision",
    ]
    recommendations_path = output_dir / "p2_review_recommendations.tsv"
    write_tsv(recommendations_path, recommendations, fieldnames)

    near_preview_paths = [
        PROJECT_ROOT / str(row["preview_path"]) for row in recommendations if row["issue_type"] == "near_duplicate_pair"
    ]
    quality_preview_paths = [
        PROJECT_ROOT / str(row["preview_path"]) for row in recommendations if row["issue_type"] == "quality_outlier"
    ]
    near_sheet_path = output_dir / "p2_near_duplicate_contact_sheet.png"
    make_contact_sheet(near_preview_paths, near_sheet_path, columns=1)
    quality_sheet_paths: List[Path] = []
    for index, paths in enumerate(chunked(quality_preview_paths, args.quality_contact_sheet_chunk_size), start=1):
        sheet_path = output_dir / f"p2_quality_contact_sheet_{index:03d}.png"
        make_contact_sheet(paths, sheet_path, columns=4)
        quality_sheet_paths.append(sheet_path)

    summary = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "near_duplicate_pair_rows": len(near_rows),
        "quality_outlier_rows": len(quality_rows),
        "total_p2_rows": len(recommendations),
        "review_status": "recommendations_only_pending_manual_review",
        "recommendations_path": str(recommendations_path.relative_to(PROJECT_ROOT)),
        "near_duplicate_contact_sheet_path": str(near_sheet_path.relative_to(PROJECT_ROOT)),
        "quality_contact_sheet_paths": [str(path.relative_to(PROJECT_ROOT)) for path in quality_sheet_paths],
        "boundary": (
            "Machine suggestions are not reviewer decisions. This pack does not change manifests, convert files, "
            "delete images, run enhancement, or replace formal 502/496 protocols."
        ),
    }
    summary_json_path = output_dir / "p2_review_pack_summary.json"
    summary_md_path = output_dir / "p2_review_pack_summary.md"
    summary_json_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    write_index_md(
        summary_md_path,
        summary,
        {
            "recommendations": str(recommendations_path.relative_to(PROJECT_ROOT)),
            "near duplicate contact sheet": str(near_sheet_path.relative_to(PROJECT_ROOT)),
            "quality contact sheets": [str(path.relative_to(PROJECT_ROOT)) for path in quality_sheet_paths],
            "summary json": str(summary_json_path.relative_to(PROJECT_ROOT)),
        },
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
