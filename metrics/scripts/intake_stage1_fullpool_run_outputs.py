from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
STAGES = ["BPH", "IMF1Ray", "RGHS", "CLAHE", "Fused", "Final"]
FORMATS = ["jpg", "png"]
IMAGE_EXTS = {".jpg", ".png", ".jpeg", ".bmp", ".tif", ".tiff", ".webp"}

DEFAULT_MANIFEST = REPO_ROOT / "metrics/manifests/full_algae_dewatermark_v1_cv2_readable_candidate.txt"
DEFAULT_OUTPUT_DIR = (
    REPO_ROOT
    / "experiments/full-algae-dewatermark-v1/outputs/cv2readable2770/runs/full2770_locked_final_mainline"
)
DEFAULT_STATUS_JSON = (
    REPO_ROOT
    / "experiments/full-algae-dewatermark-v1/outputs/cv2readable2770/runs/full2770_locked_final_mainline_intake_status_20260525.json"
)
DEFAULT_STATUS_MD = (
    REPO_ROOT
    / "experiments/full-algae-dewatermark-v1/outputs/cv2readable2770/runs/full2770_locked_final_mainline_intake_status_20260525.md"
)


@dataclass(frozen=True)
class ManifestRows:
    paths: list[Path]
    raw_count: int
    unique_count: int


def rel(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def read_manifest(path: Path, limit: int | None = None) -> ManifestRows:
    paths: list[Path] = []
    seen: set[str] = set()
    raw_count = 0
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            item = line.strip().lstrip("\ufeff")
            if not item or item.startswith("#"):
                continue
            raw_count += 1
            if len(item) >= 2 and item[0] == item[-1] and item[0] in {"'", '"'}:
                item = item[1:-1]
            if item in seen:
                continue
            seen.add(item)
            rel_path = Path(item)
            if rel_path.suffix.lower() not in IMAGE_EXTS:
                rel_path = rel_path.with_suffix(".jpg")
            paths.append(rel_path)
            if limit is not None and len(paths) >= limit:
                break
    return ManifestRows(paths=paths, raw_count=raw_count, unique_count=len(paths))


def expected_output_path(output_dir: Path, fmt: str, stage: str, src_rel_path: Path) -> Path:
    stem_path = src_rel_path.with_suffix("")
    stage_root = output_dir / fmt / stage
    if stem_path.parent != Path("."):
        stage_root = stage_root / stem_path.parent
    return stage_root / f"{stem_path.name}_{stage}.{fmt}"


def count_stage_outputs(output_dir: Path, rel_paths: list[Path]) -> tuple[dict[str, Any], int, int, bool]:
    checks: dict[str, Any] = {}
    present_total = 0
    missing_total = 0
    all_complete = True
    for fmt in FORMATS:
        checks[fmt] = {}
        for stage in STAGES:
            missing_examples: list[str] = []
            present = 0
            for rel_path in rel_paths:
                expected = expected_output_path(output_dir, fmt, stage, rel_path)
                if expected.exists():
                    present += 1
                elif len(missing_examples) < 20:
                    missing_examples.append(rel(expected))
            missing = len(rel_paths) - present
            complete = missing == 0
            present_total += present
            missing_total += missing
            all_complete = all_complete and complete
            checks[fmt][stage] = {
                "expected": len(rel_paths),
                "present": present,
                "missing": missing,
                "complete": complete,
                "missing_examples": missing_examples,
            }
    return checks, present_total, missing_total, all_complete


def sample_final_png_decode(output_dir: Path, rel_paths: list[Path], sample_count: int) -> dict[str, Any]:
    if sample_count <= 0 or not rel_paths:
        return {"requested": sample_count, "checked": 0, "ok": 0, "failures": []}
    try:
        import cv2
        import numpy as np
    except Exception as exc:  # pragma: no cover - environment specific
        return {
            "requested": sample_count,
            "checked": 0,
            "ok": 0,
            "failures": [f"cv2 import failed: {exc}"],
        }

    if len(rel_paths) <= sample_count:
        selected = rel_paths
    else:
        indexes = sorted({round(i * (len(rel_paths) - 1) / (sample_count - 1)) for i in range(sample_count)})
        selected = [rel_paths[i] for i in indexes]

    failures: list[str] = []
    ok = 0
    for rel_path in selected:
        path = expected_output_path(output_dir, "png", "Final", rel_path)
        if not path.exists():
            failures.append(f"missing: {rel(path)}")
            continue
        data = np.fromfile(str(path), dtype=np.uint8)
        img = cv2.imdecode(data, cv2.IMREAD_COLOR)
        if img is None:
            failures.append(f"decode_failed: {rel(path)}")
        else:
            ok += 1
    return {"requested": sample_count, "checked": len(selected), "ok": ok, "failures": failures[:20]}


def determine_status(output_dir: Path, present_total: int, all_complete: bool, log_exists: bool, run_report_exists: bool) -> str:
    if not output_dir.exists() or present_total == 0:
        return "not_started"
    if all_complete and log_exists and run_report_exists:
        return "complete_with_log_and_run_report"
    if all_complete:
        return "core_outputs_complete"
    return "incomplete_or_in_progress"


def write_markdown(path: Path, report: dict[str, Any]) -> None:
    lines = [
        "# Stage1 full_algae_dewatermark_v1 full-run intake status",
        "",
        f"日期：{report['date']}",
        "",
        "本文是完整增强图像池 full2770 run 的只读接收状态报告，不是运行记录本身。",
        "脚本只检查既有输出、日志和完整性；不会启动 `main.py`，不会生成增强图像，也不会创建 full run 输出根目录。",
        "",
        "## Summary",
        "",
        f"- Manifest: `{report['manifest']}`",
        f"- Output dir: `{report['output_dir']}`",
        f"- Status: `{report['status']}`",
        f"- Expected images: `{report['expected_images']}`",
        f"- Expected output files: `{report['expected_output_files']}`",
        f"- Present output files: `{report['present_output_files']}`",
        f"- Missing output files: `{report['missing_output_files']}`",
        f"- All complete: `{report['all_complete']}`",
        f"- Log exists: `{report['log_exists']}`",
        f"- Run report exists: `{report['run_report_exists']}`",
        "",
        "## Stage / Format Completeness",
        "",
        "| Format | Stage | Present | Expected | Missing | Complete |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for fmt in FORMATS:
        for stage in STAGES:
            item = report["checks"][fmt][stage]
            lines.append(
                f"| `{fmt}` | `{stage}` | `{item['present']}` | `{item['expected']}` | "
                f"`{item['missing']}` | `{item['complete']}` |"
            )
    lines.extend(["", "## Final PNG Decode Sample", ""])
    decode = report["final_png_decode_sample"]
    lines.extend(
        [
            f"- Requested: `{decode['requested']}`",
            f"- Checked: `{decode['checked']}`",
            f"- OK: `{decode['ok']}`",
            f"- Failures: `{decode['failures']}`",
            "",
            "## Boundary",
            "",
            "- `not_started` 或 `incomplete_or_in_progress` 不能写成 2770 张 full-pool enhancement 已完成。",
            "- 该 full-pool 仍不替代当前正式 `full502_clean_v1` / `compare9_complete496_v1` 论文结果口径。",
            "- 未来只有状态达到 `complete_with_log_and_run_report` 并经人工审阅后，才可把 2770 full-pool 写成完整扩展增强资产。",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_run_report(output_dir: Path, report: dict[str, Any], overwrite: bool) -> Path:
    output_path = output_dir / "run_report.md"
    if not output_dir.exists():
        raise FileNotFoundError(f"Output directory does not exist: {output_dir}")
    if output_path.exists() and not overwrite:
        raise FileExistsError(f"{output_path} exists; pass --overwrite-run-report to replace it")
    lines = [
        "# Stage1 full_algae_dewatermark_v1 full2770 locked run report",
        "",
        f"Date: {datetime.now().strftime('%Y-%m-%d')}",
        "",
        "## Summary",
        "",
        "- Run id: `full2770_locked_final_mainline`",
        "- Input pool: `full_algae_dewatermark_v1_cv2_readable_candidate`",
        f"- Manifest: `{report['manifest']}`",
        f"- Output dir: `{report['output_dir']}`",
        "- Config: `experiments/optimization_v1/configs/locked_full506_final_mainline.json`",
        "- Expected images: `2770`",
        "- Expected outputs: six stages x JPG/PNG = `33240` files",
        "",
        "## Completeness",
        "",
        f"- Present output files: `{report['present_output_files']}`",
        f"- Missing output files: `{report['missing_output_files']}`",
        f"- All complete: `{report['all_complete']}`",
        f"- Log exists: `{report['log_exists']}`",
        "",
        "## Boundary",
        "",
        "- This is a full-pool enhancement asset, not a replacement for current formal `full502_clean_v1` / `compare9_complete496_v1` paper tables.",
        "- The four OpenCV-decode-failed GIF-content candidates remain outside this cv2-readable run.",
        "- Any MyEdge GT-based downstream claim still requires separate edge-detection validation.",
        "",
    ]
    output_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    manifest = read_manifest(args.manifest, args.limit)
    checks, present_total, missing_total, all_complete = count_stage_outputs(args.output_dir, manifest.paths)
    log_path = args.output_dir / "logs/full2770_locked_final_mainline.log"
    run_report_path = args.output_dir / "run_report.md"
    decode_sample = sample_final_png_decode(args.output_dir, manifest.paths, args.decode_sample_count)
    status = determine_status(
        args.output_dir,
        present_total,
        all_complete,
        log_path.exists(),
        run_report_path.exists(),
    )
    return {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "manifest": rel(args.manifest),
        "manifest_raw_rows": manifest.raw_count,
        "manifest_unique_rows": manifest.unique_count,
        "output_dir": rel(args.output_dir),
        "output_dir_exists": args.output_dir.exists(),
        "log_path": rel(log_path),
        "log_exists": log_path.exists(),
        "run_report_path": rel(run_report_path),
        "run_report_exists": run_report_path.exists(),
        "expected_images": manifest.unique_count,
        "expected_output_files": manifest.unique_count * len(STAGES) * len(FORMATS),
        "present_output_files": present_total,
        "missing_output_files": missing_total,
        "all_complete": all_complete,
        "status": status,
        "checks": checks,
        "final_png_decode_sample": decode_sample,
        "no_main_py_execution": True,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Read-only intake for Stage1 full2770 full-pool outputs.")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--decode-sample-count", type=int, default=20)
    parser.add_argument("--status-json", type=Path, default=DEFAULT_STATUS_JSON)
    parser.add_argument("--status-md", type=Path, default=DEFAULT_STATUS_MD)
    parser.add_argument(
        "--write-run-report",
        action="store_true",
        help="Write output_dir/run_report.md only when core outputs are complete.",
    )
    parser.add_argument("--overwrite-run-report", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report = build_report(args)
    if args.write_run_report:
        if report["status"] not in {"core_outputs_complete", "complete_with_log_and_run_report"}:
            raise SystemExit(
                "Refusing to write run_report.md because core outputs are not complete. "
                f"Current status: {report['status']}"
            )
        write_run_report(args.output_dir, report, args.overwrite_run_report)
        report = build_report(args)
    args.status_json.parent.mkdir(parents=True, exist_ok=True)
    args.status_json.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_markdown(args.status_md, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
