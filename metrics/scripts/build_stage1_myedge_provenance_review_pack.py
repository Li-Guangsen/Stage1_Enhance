from __future__ import annotations

import argparse
import csv
import json
import textwrap
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

from PIL import Image, ImageDraw, ImageFont, ImageOps


THIS_DIR = Path(__file__).resolve().parent
METRICS_DIR = THIS_DIR.parent
PROJECT_ROOT = METRICS_DIR.parent
DEFAULT_DATE = datetime.now().date().strftime("%Y%m%d")
DEFAULT_FULLPOOL_ROOT = Path(r"D:\Desktop\去水印所有藻类图像")
DEFAULT_REVIEW_DIR = PROJECT_ROOT / "metrics" / "manifests" / "stage1_myedge_provenance_review"
DEFAULT_QUEUE = DEFAULT_REVIEW_DIR / "provenance_priority_review_queue.tsv"
DEFAULT_OUTPUT_DIR = DEFAULT_REVIEW_DIR / "p0_p1_review_pack"
DEFAULT_SUMMARY_MD = DEFAULT_OUTPUT_DIR / f"provenance_p0_p1_review_pack_summary_{DEFAULT_DATE}.md"
DEFAULT_SUMMARY_JSON = DEFAULT_OUTPUT_DIR / f"provenance_p0_p1_review_pack_summary_{DEFAULT_DATE}.json"
DEFAULT_INDEX_TSV = DEFAULT_OUTPUT_DIR / "provenance_p0_p1_review_pack_index.tsv"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build contact sheets for Stage1/MyEdge provenance P0/P1 manual review. "
            "This script creates visual review aids only; it does not fill reviewer_decision "
            "or derive provenance conclusions."
        )
    )
    parser.add_argument("--queue", default=str(DEFAULT_QUEUE))
    parser.add_argument("--fullpool-root", default=str(DEFAULT_FULLPOOL_ROOT))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--summary-md", default=str(DEFAULT_SUMMARY_MD))
    parser.add_argument("--summary-json", default=str(DEFAULT_SUMMARY_JSON))
    parser.add_argument("--index-tsv", default=str(DEFAULT_INDEX_TSV))
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


def resolve_candidate_path(row: Dict[str, str], fullpool_root: Path) -> Path:
    candidate_path = row.get("candidate_path", "").strip()
    if candidate_path:
        return Path(candidate_path)
    relpath = row.get("candidate_relpath", "").strip()
    if row.get("candidate_group") == "fullpool_2774" and relpath:
        return fullpool_root / relpath
    return Path(relpath)


def find_font(size: int) -> ImageFont.ImageFont:
    candidates = [
        Path(r"C:\Windows\Fonts\msyh.ttc"),
        Path(r"C:\Windows\Fonts\simsun.ttc"),
        Path(r"C:\Windows\Fonts\arial.ttf"),
    ]
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


def load_image(path: Path, size: Tuple[int, int]) -> Image.Image:
    canvas = Image.new("RGB", size, (245, 245, 245))
    if not path.exists():
        return canvas
    try:
        with Image.open(path) as img:
            img = ImageOps.exif_transpose(img).convert("RGB")
            img.thumbnail((size[0] - 8, size[1] - 8), Image.Resampling.LANCZOS)
            x = (size[0] - img.width) // 2
            y = (size[1] - img.height) // 2
            canvas.paste(img, (x, y))
    except Exception:
        return canvas
    return canvas


def draw_wrapped(
    draw: ImageDraw.ImageDraw,
    xy: Tuple[int, int],
    text: str,
    font: ImageFont.ImageFont,
    fill: Tuple[int, int, int],
    width_chars: int,
    max_lines: int,
    line_height: int,
) -> int:
    lines: List[str] = []
    for part in str(text).splitlines() or [""]:
        wrapped = textwrap.wrap(part, width=width_chars, break_long_words=True, replace_whitespace=False)
        lines.extend(wrapped or [""])
    lines = lines[:max_lines]
    x, y = xy
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += line_height
    return y


def render_tile(row: Dict[str, str], fullpool_root: Path, tile_size: Tuple[int, int]) -> Image.Image:
    tile = Image.new("RGB", tile_size, (255, 255, 255))
    draw = ImageDraw.Draw(tile)
    font = find_font(14)
    small = find_font(12)
    title = find_font(16)

    border_color = {
        "P0": (185, 40, 40),
        "P1": (196, 120, 20),
    }.get(row.get("priority", ""), (80, 80, 80))
    draw.rectangle((0, 0, tile_size[0] - 1, tile_size[1] - 1), outline=border_color, width=3)

    header = f"{row.get('review_id')} | {row.get('priority')} | {row.get('relation_scope')}"
    draw.text((10, 8), header, font=title, fill=(20, 20, 20))

    source_path = Path(row.get("source_path", ""))
    candidate_path = resolve_candidate_path(row, fullpool_root)
    source_img = load_image(source_path, (170, 170))
    candidate_img = load_image(candidate_path, (170, 170))
    tile.paste(source_img, (12, 42))
    tile.paste(candidate_img, (198, 42))
    draw.text((62, 216), "source", font=small, fill=(70, 70, 70))
    draw.text((246, 216), "candidate", font=small, fill=(70, 70, 70))

    text_x = 390
    y = 44
    meta = [
        f"source: {row.get('source_id')}",
        f"candidate: {row.get('candidate_id')}",
        f"band: {row.get('candidate_band')}",
        f"hamming: {row.get('combined_hash_hamming')} | rmse32: {row.get('thumb_rmse_32')}",
        f"same_dims: {row.get('same_dimensions')}",
        f"suggestion: {row.get('machine_suggestion')}",
    ]
    for item in meta:
        y = draw_wrapped(draw, (text_x, y), item, small, (30, 30, 30), 46, 2, 16)
        y += 2
    draw_wrapped(draw, (10, 238), str(candidate_path).replace("\\", "/"), small, (70, 70, 70), 88, 2, 15)
    return tile


def chunked(items: Sequence[Dict[str, str]], size: int) -> Iterable[Sequence[Dict[str, str]]]:
    for idx in range(0, len(items), size):
        yield items[idx : idx + size]


def render_sheets(
    rows: Sequence[Dict[str, str]],
    output_dir: Path,
    fullpool_root: Path,
) -> List[Dict[str, object]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    sheet_rows: List[Dict[str, object]] = []
    tile_size = (760, 280)
    cols = 1
    rows_per_sheet = 4
    sheet_size = (tile_size[0] * cols, tile_size[1] * rows_per_sheet)
    grouped: Dict[Tuple[str, str], List[Dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[(row.get("priority", ""), row.get("relation_scope", ""))].append(row)

    for (priority, scope), group in sorted(grouped.items(), key=lambda item: (item[0][0], item[0][1])):
        safe_scope = scope.replace("/", "_").replace(" ", "_")
        for page_idx, page_rows in enumerate(chunked(group, rows_per_sheet), start=1):
            sheet = Image.new("RGB", sheet_size, (238, 238, 238))
            for tile_idx, row in enumerate(page_rows, start=1):
                tile = render_tile(row, fullpool_root=fullpool_root, tile_size=tile_size)
                sheet.paste(tile, (0, (tile_idx - 1) * tile_size[1]))
                sheet_rows.append(
                    {
                        "review_id": row.get("review_id"),
                        "priority": priority,
                        "relation_scope": scope,
                        "sheet_file": f"{priority}_{safe_scope}_page{page_idx:03d}.png",
                        "sheet_page": page_idx,
                        "tile_index": tile_idx,
                        "source_id": row.get("source_id"),
                        "candidate_id": row.get("candidate_id"),
                        "candidate_band": row.get("candidate_band"),
                        "reviewer_decision": row.get("reviewer_decision"),
                    }
                )
            sheet_path = output_dir / f"{priority}_{safe_scope}_page{page_idx:03d}.png"
            sheet.save(sheet_path)
    return sheet_rows


def count_by(rows: Sequence[Dict[str, str]], key: str) -> Dict[str, int]:
    return dict(sorted(Counter(row.get(key, "") for row in rows).items()))


def render_table(counts: Dict[str, int]) -> str:
    lines = ["| Item | Count |", "|---|---:|"]
    lines.extend(f"| {key or '(blank)'} | {value} |" for key, value in counts.items())
    return "\n".join(lines)


def render_md(summary: Dict[str, object]) -> str:
    return f"""# Stage1-MyEdge Provenance P0/P1 复核辅助包

生成时间：`{summary["generated_at"]}`

状态：`{summary["status"]}`

本辅助包为 provenance P0/P1 优先队列生成 source/candidate 并排 contact sheets，只服务于人工复核。它不填写 `reviewer_decision`，不推断同源关系，不运行 Stage1，不运行 MyEdge，不生成指标。

## 计数

- P0/P1 review rows：`{summary["row_count"]}`
- contact sheets：`{summary["contact_sheet_count"]}`
- reviewer_decision filled：`{summary["reviewer_decision_filled"]}`
- reviewer_decision pending：`{summary["reviewer_decision_pending"]}`

## Priority Counts

{render_table(summary["priority_counts"])}

## Relation Scope Counts

{render_table(summary["relation_scope_counts"])}

## Candidate Band Counts

{render_table(summary["candidate_band_counts"])}

## 输出

- contact sheets 目录：`{summary["contact_sheet_dir"]}`
- pack index：`{summary["pack_index_tsv"]}`

## 边界

- contact sheet 是人工复核辅助，不是论文图。
- `machine_suggestion` 和视觉指标不能作为人工结论。
- 只有人工填写并通过 provenance 校验/派生后，才能更新数据来源说明。
"""


def main() -> None:
    args = parse_args()
    queue = Path(args.queue)
    fullpool_root = Path(args.fullpool_root)
    output_dir = Path(args.output_dir)
    summary_md = Path(args.summary_md)
    summary_json = Path(args.summary_json)
    index_tsv = Path(args.index_tsv)
    contact_sheet_dir = output_dir / "contact_sheets"

    rows = read_tsv(queue)
    pack_rows = render_sheets(rows, contact_sheet_dir, fullpool_root=fullpool_root)
    reviewer_filled = sum(1 for row in rows if row.get("reviewer_decision", "").strip())
    summary: Dict[str, object] = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "status": "review_aid_ready_pending_manual_decision",
        "queue": str(queue),
        "row_count": len(rows),
        "priority_counts": count_by(rows, "priority"),
        "relation_scope_counts": count_by(rows, "relation_scope"),
        "candidate_band_counts": count_by(rows, "candidate_band"),
        "contact_sheet_count": len({row["sheet_file"] for row in pack_rows}),
        "reviewer_decision_filled": reviewer_filled,
        "reviewer_decision_pending": len(rows) - reviewer_filled,
        "contact_sheet_dir": str(contact_sheet_dir),
        "pack_index_tsv": str(index_tsv),
        "boundary": "This pack is a manual review aid only and does not confirm provenance.",
    }

    fields = [
        "review_id",
        "priority",
        "relation_scope",
        "sheet_file",
        "sheet_page",
        "tile_index",
        "source_id",
        "candidate_id",
        "candidate_band",
        "reviewer_decision",
    ]
    output_dir.mkdir(parents=True, exist_ok=True)
    write_tsv(index_tsv, pack_rows, fields)
    summary_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    summary_md.write_text(render_md(summary), encoding="utf-8")
    print(f"Wrote {summary_md}")
    print(f"Wrote {summary_json}")
    print(f"Wrote {index_tsv}")
    print(f"status={summary['status']}")


if __name__ == "__main__":
    main()
