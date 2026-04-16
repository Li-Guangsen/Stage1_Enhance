from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import cv2
import numpy as np

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from libs.EME import EME
from libs.EMEE import EMEE
from libs.Gradient import Gradient
from libs.UCIQE import calc_uciqe
from libs.UIQM import calc_uiqm
from libs.calc_InEntropy import get_entropy
from libs.Contrast_ratio import contrast
from libs.msssim import msssim
from protocol_common import (
    PROJECT_ROOT,
    MethodSpec,
    build_image_index,
    parse_method_specs,
    read_bgr,
    read_manifest,
    resize_bgr,
    resolve_project_path,
    select_common_stems,
    write_lines,
)


METRIC_NAMES = [
    "EME",
    "EMEE",
    "Entropy",
    "Contrast",
    "AvgGra",
    "MS_SSIM",
    "PSNR",
    "UCIQE",
    "UIQM",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Protocol v2 evaluator for underwater algae image enhancement."
    )
    parser.add_argument("--original-dir", default="data/inputImg/Original")
    parser.add_argument("--result-dir", default="results/png/Final")
    parser.add_argument("--method-name", default=None)
    parser.add_argument(
        "--method",
        action="append",
        default=None,
        help="Evaluate an additional method as name=directory. Repeat for multiple methods.",
    )
    parser.add_argument(
        "--methods-root",
        default=None,
        help="Evaluate every immediate child directory as a method.",
    )
    parser.add_argument(
        "--methods-subdir",
        default=None,
        help="Optional subdirectory below each --methods-root child, e.g. Final.",
    )
    parser.add_argument("--manifest", default=None, help="Optional manifest of canonical stems or filenames.")
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--limit", type=int, default=None, help="Debug limit after manifest/common matching.")
    parser.add_argument("--resize-to", nargs=2, type=int, default=(320, 320), metavar=("WIDTH", "HEIGHT"))
    parser.add_argument("--no-resize", action="store_true")
    parser.add_argument("--quiet", action="store_true")
    return parser.parse_args()


def default_output_dir() -> Path:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return PROJECT_ROOT / "metrics" / "outputs" / "evaluate_protocol_v2" / stamp


def finite_or_none(value: float) -> Optional[float]:
    value = float(value)
    if math.isfinite(value):
        return value
    return None


def csv_value(value: float) -> str:
    value = float(value)
    if math.isfinite(value):
        return f"{value:.10g}"
    if math.isinf(value):
        return "inf" if value > 0 else "-inf"
    return "nan"


def summarize_metric(rows: Sequence[Dict[str, object]], metric_name: str) -> Dict[str, object]:
    values = []
    nonfinite = 0
    for row in rows:
        value = float(row[metric_name])
        if math.isfinite(value):
            values.append(value)
        else:
            nonfinite += 1

    if not values:
        return {
            "count": 0,
            "nonfinite": nonfinite,
            "mean": None,
            "std": None,
            "median": None,
            "min": None,
            "max": None,
        }

    arr = np.asarray(values, dtype=np.float64)
    return {
        "count": int(arr.size),
        "nonfinite": int(nonfinite),
        "mean": float(np.mean(arr)),
        "std": float(np.std(arr, ddof=0)),
        "median": float(np.median(arr)),
        "min": float(np.min(arr)),
        "max": float(np.max(arr)),
    }


def compute_metrics(
    original_path: Path,
    result_path: Path,
    resize_to: Optional[Tuple[int, int]],
) -> Dict[str, float]:
    original_bgr = resize_bgr(read_bgr(original_path), resize_to)
    result_bgr = resize_bgr(read_bgr(result_path), resize_to)

    original_gray = cv2.cvtColor(original_bgr, cv2.COLOR_BGR2GRAY)
    result_gray = cv2.cvtColor(result_bgr, cv2.COLOR_BGR2GRAY)

    return {
        "EME": float(EME(result_gray)),
        "EMEE": float(EMEE(result_gray)),
        "Entropy": float(get_entropy(result_gray)),
        "Contrast": float(contrast(result_gray)),
        "AvgGra": float(Gradient(result_gray)),
        "MS_SSIM": float(msssim(original_bgr, result_bgr)),
        "PSNR": float(cv2.PSNR(original_gray, result_gray)),
        "UCIQE": float(calc_uciqe(result_bgr)),
        "UIQM": float(calc_uiqm(result_bgr)),
    }


def write_csv(path: Path, rows: Sequence[Dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "method",
        "stem",
        "original_filename",
        "result_filename",
        "original_path",
        "result_path",
        *METRIC_NAMES,
    ]
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            out = dict(row)
            for name in METRIC_NAMES:
                out[name] = csv_value(float(out[name]))
            writer.writerow(out)


def write_failures_csv(path: Path, failures: Sequence[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["phase", "method", "stem", "original_path", "result_path", "error"]
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for failure in failures:
            writer.writerow({key: failure.get(key, "") for key in fieldnames})


def build_summary(
    methods: Sequence[MethodSpec],
    rows: Sequence[Dict[str, object]],
    failures: Sequence[Dict[str, str]],
    planned_stems: Sequence[str],
    output_dir: Path,
    original_dir: Path,
    resize_to: Optional[Tuple[int, int]],
    complete_success_stems: Sequence[str],
) -> Dict[str, object]:
    method_summaries: Dict[str, Dict[str, object]] = {}
    complete_set = set(complete_success_stems)
    complete_rows = [row for row in rows if str(row["stem"]) in complete_set]

    for method in methods:
        method_rows = [row for row in complete_rows if row["method"] == method.name]
        method_summaries[method.name] = {
            "directory": str(method.directory),
            "complete_case_count": len(method_rows),
            "metrics": {name: summarize_metric(method_rows, name) for name in METRIC_NAMES},
        }

    return {
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "project_root": str(PROJECT_ROOT),
        "original_dir": str(original_dir),
        "resize_to": list(resize_to) if resize_to else None,
        "summary_policy": "complete_cases_across_all_methods",
        "planned_stem_count": len(planned_stems),
        "complete_success_count": len(complete_success_stems),
        "failure_count": len(failures),
        "methods": method_summaries,
        "outputs": {
            "output_dir": str(output_dir),
            "per_image_csv": str(output_dir / "per_image_metrics.csv"),
            "summary_txt": str(output_dir / "summary.txt"),
            "summary_json": str(output_dir / "summary.json"),
            "failed_csv": str(output_dir / "failed_files.csv"),
            "planned_manifest": str(output_dir / "planned_manifest.txt"),
            "complete_case_manifest": str(output_dir / "complete_case_manifest.txt"),
        },
        "failures": list(failures),
    }


def write_summary_txt(path: Path, summary: Dict[str, object]) -> None:
    lines: List[str] = []
    lines.append("# Protocol v2 image enhancement evaluation")
    lines.append(f"Created at: {summary['created_at']}")
    lines.append(f"Original dir: {summary['original_dir']}")
    lines.append(f"Summary policy: {summary['summary_policy']}")
    lines.append(f"Planned stems: {summary['planned_stem_count']}")
    lines.append(f"Complete success stems: {summary['complete_success_count']}")
    lines.append(f"Failures: {summary['failure_count']}")
    lines.append("")

    methods = summary["methods"]
    assert isinstance(methods, dict)
    for method_name, method_summary in methods.items():
        lines.append(f"## {method_name}")
        lines.append(f"Directory: {method_summary['directory']}")
        lines.append(f"Count: {method_summary['complete_case_count']}")
        metrics = method_summary["metrics"]
        for metric_name in METRIC_NAMES:
            metric = metrics[metric_name]
            mean = metric["mean"]
            std = metric["std"]
            if mean is None:
                lines.append(f"{metric_name}: NA")
            else:
                lines.append(f"{metric_name}: mean={mean:.6f}, std={std:.6f}")
        lines.append("")

    if summary["failures"]:
        lines.append("## Failed files")
        for failure in summary["failures"]:
            lines.append(
                f"{failure.get('phase', '')}\t{failure.get('method', '')}\t"
                f"{failure.get('stem', '')}\t{failure.get('error', '')}"
            )

    write_lines(path, lines)


def main() -> int:
    args = parse_args()
    np.seterr(over="ignore")

    original_dir = resolve_project_path(args.original_dir)
    output_dir = resolve_project_path(args.output_dir) if args.output_dir else default_output_dir()
    output_dir.mkdir(parents=True, exist_ok=True)
    resize_to = None if args.no_resize else tuple(args.resize_to)

    method_args = list(args.method or [])
    if args.methods_root:
        methods_root = resolve_project_path(args.methods_root)
        children = [p for p in methods_root.iterdir() if p.is_dir()]
        for child in sorted(children, key=lambda p: p.name.lower()):
            method_dir = child / args.methods_subdir if args.methods_subdir else child
            method_args.append(f"{child.name}={method_dir}")
    methods = parse_method_specs(method_args or None, args.result_dir, args.method_name)
    original_index = build_image_index(original_dir, include_normalized_keys=False)
    method_indexes = {method.name: build_image_index(method.directory, include_normalized_keys=True) for method in methods}

    failures: List[Dict[str, str]] = []
    for key, first, second in original_index.collisions:
        failures.append({"phase": "indexing", "method": "original", "stem": key, "error": f"collision: {first} | {second}"})
    for method_name, index in method_indexes.items():
        for key, first, second in index.collisions:
            failures.append({"phase": "indexing", "method": method_name, "stem": key, "error": f"collision: {first} | {second}"})

    manifest_stems = read_manifest(args.manifest) if args.manifest else None
    planned_stems, matching_failures = select_common_stems(
        original_index=original_index,
        method_indexes=method_indexes,
        manifest_stems=manifest_stems,
        limit=args.limit,
    )
    failures.extend(matching_failures)

    write_lines(output_dir / "planned_manifest.txt", planned_stems)
    if not planned_stems:
        summary = build_summary(methods, [], failures, [], output_dir, original_dir, resize_to, [])
        (output_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
        write_summary_txt(output_dir / "summary.txt", summary)
        write_failures_csv(output_dir / "failed_files.csv", failures)
        print(f"[ERROR] No common images to evaluate. Output: {output_dir}")
        return 2

    rows: List[Dict[str, object]] = []
    success_by_stem = {stem: set() for stem in planned_stems}

    for i, stem in enumerate(planned_stems, start=1):
        original_path = original_index.by_key[stem]
        for method in methods:
            result_path = method_indexes[method.name].by_key[stem]
            try:
                metrics = compute_metrics(original_path, result_path, resize_to)
                row: Dict[str, object] = {
                    "method": method.name,
                    "stem": stem,
                    "original_filename": original_path.name,
                    "result_filename": result_path.name,
                    "original_path": str(original_path),
                    "result_path": str(result_path),
                    **metrics,
                }
                rows.append(row)
                success_by_stem[stem].add(method.name)
                if not args.quiet or i == 1 or i == len(planned_stems) or i % 25 == 0:
                    print(f"[OK] {i}/{len(planned_stems)} {method.name}: {stem}")
            except Exception as exc:
                failures.append(
                    {
                        "phase": "evaluation",
                        "method": method.name,
                        "stem": stem,
                        "original_path": str(original_path),
                        "result_path": str(result_path),
                        "error": str(exc),
                    }
                )
                print(f"[FAIL] {i}/{len(planned_stems)} {method.name}: {stem} -> {exc}")

    method_names = {method.name for method in methods}
    complete_success_stems = [stem for stem in planned_stems if success_by_stem[stem] == method_names]

    write_csv(output_dir / "per_image_metrics.csv", rows)
    write_failures_csv(output_dir / "failed_files.csv", failures)
    write_lines(output_dir / "complete_case_manifest.txt", complete_success_stems)

    summary = build_summary(
        methods=methods,
        rows=rows,
        failures=failures,
        planned_stems=planned_stems,
        output_dir=output_dir,
        original_dir=original_dir,
        resize_to=resize_to,
        complete_success_stems=complete_success_stems,
    )
    (output_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    write_summary_txt(output_dir / "summary.txt", summary)

    print(f"[DONE] Evaluated {len(complete_success_stems)} complete-case images.")
    print(f"[DONE] Output directory: {output_dir}")
    return 0 if complete_success_stems else 1


if __name__ == "__main__":
    raise SystemExit(main())
