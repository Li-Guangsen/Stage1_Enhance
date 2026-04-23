from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List


THIS_DIR = Path(__file__).resolve().parent
METRICS_DIR = THIS_DIR.parent
PROJECT_ROOT = METRICS_DIR.parent
if str(METRICS_DIR) not in sys.path:
    sys.path.insert(0, str(METRICS_DIR))

from protocol_common import build_image_index, list_image_files, resolve_project_path, write_lines


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build official clean manifests for Stage1Codex.")
    parser.add_argument(
        "--registry",
        default=str(PROJECT_ROOT / "metrics" / "configs" / "official_method_registry.json"),
    )
    parser.add_argument(
        "--output-dir",
        default=str(PROJECT_ROOT / "metrics" / "manifests"),
    )
    return parser.parse_args()


def load_registry(path: str | Path) -> Dict[str, object]:
    registry_path = resolve_project_path(path)
    return json.loads(registry_path.read_text(encoding="utf-8"))


def main() -> None:
    args = parse_args()
    registry = load_registry(args.registry)
    output_dir = resolve_project_path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    original_dir = resolve_project_path(registry["original_dir"])
    original_files = list_image_files(original_dir)
    original_stems = [path.stem for path in original_files]

    full_manifest_path = output_dir / "full502_clean_v1.txt"
    write_lines(full_manifest_path, original_stems)

    original_index = build_image_index(original_dir, include_normalized_keys=False)

    compare_methods = registry["compare_methods"]
    method_indexes = {}
    method_file_counts = {}
    method_match_counts = {}
    method_missing = {}
    for method in compare_methods:
        method_name = str(method["name"])
        method_dir = resolve_project_path(method["directory"])
        method_files = list_image_files(method_dir)
        image_index = build_image_index(method_dir, include_normalized_keys=True)
        method_indexes[method_name] = image_index
        method_file_counts[method_name] = len(method_files)
        method_match_counts[method_name] = len(set(original_stems) & set(image_index.by_key))
        missing = sorted(set(original_stems) - set(image_index.by_key), key=str.lower)
        method_missing[method_name] = missing

    compare_stems = set(original_index.by_key)
    for image_index in method_indexes.values():
        compare_stems &= set(image_index.by_key)
    compare_stems_sorted = sorted(compare_stems, key=str.lower)

    compare_manifest_path = output_dir / "compare9_complete496_v1.txt"
    write_lines(compare_manifest_path, compare_stems_sorted)

    report = {
        "version": registry.get("version", "official_v1"),
        "original_dir": str(original_dir),
        "full502_clean_manifest": str(full_manifest_path),
        "full502_clean_count": len(original_stems),
        "compare9_complete_manifest": str(compare_manifest_path),
        "compare9_complete_count": len(compare_stems_sorted),
        "compare_methods": [
            {
                "name": str(method["name"]),
                "display_name": str(method.get("display_name", method["name"])),
                "directory": str(resolve_project_path(method["directory"])),
                "file_count": method_file_counts[str(method["name"])],
                "matched_full502_count": method_match_counts[str(method["name"])],
                "missing_against_full502": method_missing[str(method["name"])],
            }
            for method in compare_methods
        ],
    }

    report_path = output_dir / "official_manifest_report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
