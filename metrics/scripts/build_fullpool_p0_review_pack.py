from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

from PIL import Image, ImageDraw, ImageFont, ImageOps


THIS_DIR = Path(__file__).resolve().parent
METRICS_DIR = THIS_DIR.parent
PROJECT_ROOT = METRICS_DIR.parent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build a P0 visual review pack for full_algae_dewatermark_v1 manual review. "
            "This script creates previews and machine suggestions only; it does not fill reviewer decisions."
        )
    )
    parser.add_argument(
        "--inventory",
        default=str(PROJECT_ROOT / "metrics" / "manifests" / "full_algae_dewatermark_v1_inventory.tsv"),
    )
    parser.add_argument(
        "--decode-review",
        default=str(
            PROJECT_ROOT
            / "metrics"
            / "manifests"
            / "full_algae_dewatermark_v1_manual_review"
            / "decode_failures_review.tsv"
        ),
    )
    parser.add_argument(
        "--exact-review",
        default=str(
            PROJECT_ROOT
            / "metrics"
            / "manifests"
            / "full_algae_dewatermark_v1_manual_review"
            / "exact_duplicates_review.tsv"
        ),
    )
    parser.add_argument(
        "--output-dir",
        default=str(PROJECT_ROOT / "metrics" / "manifests" / "full_algae_dewatermark_v1_manual_review" / "p0_review_pack"),
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


def relative_to_absolute_map(inventory_rows: List[Dict[str, str]]) -> Dict[str, Path]:
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
    thumb.thumbnail((size[0] - 16, size[1] - 46), Image.Resampling.LANCZOS)
    x = (size[0] - thumb.width) // 2
    y = 8
    canvas.paste(thumb, (x, y))
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.load_default()
    draw.text((8, size[1] - 32), label[:46], fill=(0, 0, 0), font=font)
    return canvas


def save_decode_preview(row: Dict[str, str], path_map: Dict[str, Path], output_dir: Path) -> str:
    issue_id = row["issue_id"]
    relative_path = row["relative_path"]
    image = open_rgb(path_map[relative_path])
    preview = thumbnail_canvas(image, issue_id)
    preview_path = output_dir / "previews" / f"{issue_id}.png"
    preview_path.parent.mkdir(parents=True, exist_ok=True)
    preview.save(preview_path)
    return str(preview_path.relative_to(PROJECT_ROOT))


def save_duplicate_preview(row: Dict[str, str], path_map: Dict[str, Path], output_dir: Path) -> str:
    issue_id = row["issue_id"]
    related_paths = [item.strip() for item in row["related_paths"].split("|") if item.strip()]
    panels: List[Image.Image] = []
    for index, relative_path in enumerate(related_paths, start=1):
        image = open_rgb(path_map[relative_path])
        panels.append(thumbnail_canvas(image, f"{issue_id}_{index}"))
    width = sum(panel.width for panel in panels)
    height = max(panel.height for panel in panels)
    canvas = Image.new("RGB", (width, height), "white")
    offset = 0
    for panel in panels:
        canvas.paste(panel, (offset, 0))
        offset += panel.width
    preview_path = output_dir / "previews" / f"{issue_id}.png"
    preview_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(preview_path)
    return str(preview_path.relative_to(PROJECT_ROOT))


def make_contact_sheet(preview_paths: List[Path], output_path: Path, columns: int = 2) -> None:
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


def build_recommendations(
    decode_rows: List[Dict[str, str]],
    exact_rows: List[Dict[str, str]],
    path_map: Dict[str, Path],
    output_dir: Path,
) -> List[Dict[str, object]]:
    recommendations: List[Dict[str, object]] = []
    for row in decode_rows:
        preview = save_decode_preview(row, path_map, output_dir)
        recommendations.append(
            {
                "issue_id": row["issue_id"],
                "issue_type": row["issue_type"],
                "priority": row["priority"],
                "relative_path": row["relative_path"],
                "related_paths": row.get("related_paths", ""),
                "evidence_summary": row["evidence_summary"],
                "machine_suggestion": "exclude_from_opencv_fullpool",
                "suggestion_reason": (
                    "File has GIF89a content behind a .jpg extension and fails cv2.imdecode; current safe full-pool "
                    "protocol already uses the 2770 OpenCV-readable manifest. Preserve the source file unless a "
                    "separate conversion protocol is approved."
                ),
                "preview_path": preview,
                "review_status": row["review_status"],
                "reviewer_decision": row.get("reviewer_decision", ""),
            }
        )
    for row in exact_rows:
        preview = save_duplicate_preview(row, path_map, output_dir)
        top_level_count = "top_level_folder_count=2" in row.get("evidence_summary", "")
        suggestion = "keep_but_split_guard" if top_level_count else "deduplicate_for_clean_pool"
        reason = (
            "Exact byte duplicate spans different top-level folders; preserve until taxonomy is checked, but enforce "
            "split leakage guard."
            if top_level_count
            else "Exact byte duplicate within the same top-level folder; deduplicate for a future clean pool unless a "
            "domain reviewer wants repeated acquisition retained."
        )
        recommendations.append(
            {
                "issue_id": row["issue_id"],
                "issue_type": row["issue_type"],
                "priority": row["priority"],
                "relative_path": row.get("relative_path", ""),
                "related_paths": row["related_paths"],
                "evidence_summary": row["evidence_summary"],
                "machine_suggestion": suggestion,
                "suggestion_reason": reason,
                "preview_path": preview,
                "review_status": row["review_status"],
                "reviewer_decision": row.get("reviewer_decision", ""),
            }
        )
    return recommendations


def write_index_md(path: Path, summary: Dict[str, object], outputs: Dict[str, str]) -> None:
    lines = [
        "# full_algae_dewatermark_v1 P0 review pack",
        "",
        f"日期：{datetime.now().date().isoformat()}",
        "",
        "本文是 P0 人工复核辅助包，不是最终人工决策，不修改 manifest，也不运行增强。",
        "",
        "## Summary",
        "",
        f"- Decode failure P0 rows: `{summary['decode_failure_rows']}`",
        f"- Exact duplicate P0 rows: `{summary['exact_duplicate_group_rows']}`",
        f"- Total P0 rows: `{summary['total_p0_rows']}`",
        f"- Current review status: `{summary['review_status']}`",
        "",
        "## Outputs",
        "",
    ]
    for label, value in outputs.items():
        lines.append(f"- {label}: `{value}`")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- `machine_suggestion` 只是复核建议，不是 `reviewer_decision`。",
            "- 不得根据本包直接改写 manifest、删除原图或转换原图。",
            "- 只有人工填写 review sheets 并通过 `validate_fullpool_manual_review.py` 后，才能进入清洗规则派生。",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    path_map = relative_to_absolute_map(read_tsv(Path(args.inventory)))
    decode_rows = read_tsv(Path(args.decode_review))
    exact_rows = read_tsv(Path(args.exact_review))
    recommendations = build_recommendations(decode_rows, exact_rows, path_map, output_dir)

    recommendations_path = output_dir / "p0_review_recommendations.tsv"
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
    write_tsv(recommendations_path, recommendations, fieldnames)
    preview_paths = [PROJECT_ROOT / str(row["preview_path"]) for row in recommendations]
    contact_sheet_path = output_dir / "p0_contact_sheet.png"
    make_contact_sheet(preview_paths, contact_sheet_path)

    summary = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "decode_failure_rows": len(decode_rows),
        "exact_duplicate_group_rows": len(exact_rows),
        "total_p0_rows": len(recommendations),
        "review_status": "recommendations_only_pending_manual_review",
        "recommendations_path": str(recommendations_path.relative_to(PROJECT_ROOT)),
        "contact_sheet_path": str(contact_sheet_path.relative_to(PROJECT_ROOT)),
        "boundary": (
            "Machine suggestions are not reviewer decisions. This pack does not change manifests, convert files, "
            "delete images, run enhancement, or replace formal 502/496 protocols."
        ),
    }
    summary_json_path = output_dir / "p0_review_pack_summary.json"
    summary_md_path = output_dir / "p0_review_pack_summary.md"
    summary_json_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    write_index_md(
        summary_md_path,
        summary,
        {
            "recommendations": str(recommendations_path.relative_to(PROJECT_ROOT)),
            "contact sheet": str(contact_sheet_path.relative_to(PROJECT_ROOT)),
            "summary json": str(summary_json_path.relative_to(PROJECT_ROOT)),
        },
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
