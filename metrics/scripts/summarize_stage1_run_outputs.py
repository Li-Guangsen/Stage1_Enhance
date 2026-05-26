from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List


STAGES = ["BPH", "IMF1Ray", "RGHS", "CLAHE", "Fused", "Final"]
FORMATS = ["jpg", "png"]
IMAGE_EXTS = {".jpg", ".png", ".jpeg", ".bmp", ".tif", ".tiff", ".webp"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize Stage1 output completeness against a relative-path manifest.")
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--output-json", default=None)
    return parser.parse_args()


def read_manifest(path: Path, limit: int | None = None) -> List[Path]:
    items: List[Path] = []
    seen = set()
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            item = line.strip().lstrip("\ufeff")
            if not item or item.startswith("#"):
                continue
            if len(item) >= 2 and item[0] == item[-1] and item[0] in {"'", '"'}:
                item = item[1:-1]
            if item in seen:
                continue
            seen.add(item)
            rel_path = Path(item)
            if rel_path.suffix.lower() not in IMAGE_EXTS:
                rel_path = rel_path.with_suffix(".jpg")
            items.append(rel_path)
            if limit is not None and len(items) >= limit:
                break
    return items


def expected_output_path(output_dir: Path, fmt: str, stage: str, src_rel_path: Path) -> Path:
    stem_path = src_rel_path.with_suffix("")
    stage_root = output_dir / fmt / stage
    if stem_path.parent != Path("."):
        stage_root = stage_root / stem_path.parent
    return stage_root / f"{stem_path.name}_{stage}.{fmt}"


def summarize(manifest: Path, output_dir: Path, limit: int | None) -> Dict[str, object]:
    rel_paths = read_manifest(manifest, limit)
    checks: Dict[str, object] = {}
    all_complete = True

    for fmt in FORMATS:
        checks[fmt] = {}
        for stage in STAGES:
            missing = []
            present_count = 0
            for rel_path in rel_paths:
                expected = expected_output_path(output_dir, fmt, stage, rel_path)
                if expected.exists():
                    present_count += 1
                elif len(missing) < 20:
                    missing.append(str(expected))
            complete = present_count == len(rel_paths)
            all_complete = all_complete and complete
            checks[fmt][stage] = {
                "expected": len(rel_paths),
                "present": present_count,
                "missing": len(rel_paths) - present_count,
                "complete": complete,
                "missing_examples": missing,
            }

    return {
        "manifest": str(manifest),
        "output_dir": str(output_dir),
        "limit": limit,
        "expected_images": len(rel_paths),
        "all_complete": all_complete,
        "checks": checks,
    }


def main() -> None:
    args = parse_args()
    summary = summarize(Path(args.manifest), Path(args.output_dir), args.limit)
    text = json.dumps(summary, ensure_ascii=False, indent=2)
    if args.output_json:
        Path(args.output_json).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output_json).write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
