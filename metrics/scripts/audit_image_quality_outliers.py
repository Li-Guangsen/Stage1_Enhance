from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import cv2
import numpy as np
from PIL import Image, ImageOps


THIS_DIR = Path(__file__).resolve().parent
METRICS_DIR = THIS_DIR.parent
PROJECT_ROOT = METRICS_DIR.parent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Compute lightweight quality statistics and outlier candidates for the full algae image pool. "
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
        default=str(PROJECT_ROOT / "metrics" / "manifests" / "full_algae_dewatermark_v1_quality_audit"),
        help="Output prefix. Writes .tsv, _outliers.tsv, .summary.json, and .summary.md.",
    )
    parser.add_argument(
        "--outlier-percentile",
        type=float,
        default=2.0,
        help="Tail percentile used for candidate quality outlier thresholds.",
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


def decode_cv2_rgb(path: Path) -> Optional[np.ndarray]:
    data = np.fromfile(str(path), dtype=np.uint8)
    image = cv2.imdecode(data, cv2.IMREAD_UNCHANGED)
    if image is None:
        return None
    if image.ndim == 2:
        return cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    if image.ndim == 3 and image.shape[2] == 4:
        return cv2.cvtColor(image, cv2.COLOR_BGRA2RGB)
    if image.ndim == 3 and image.shape[2] == 3:
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    raise ValueError(f"unsupported image shape: {image.shape}")


def decode_pillow_rgb(path: Path) -> np.ndarray:
    with Image.open(path) as image:
        image = ImageOps.exif_transpose(image)
        return np.array(image.convert("RGB"))


def decode_rgb(path: Path) -> Tuple[np.ndarray, str]:
    image = decode_cv2_rgb(path)
    if image is not None:
        return image, "cv2"
    return decode_pillow_rgb(path), "pillow_fallback"


def entropy_u8(gray: np.ndarray) -> float:
    hist = np.bincount(gray.reshape(-1), minlength=256).astype(np.float64)
    prob = hist / max(float(hist.sum()), 1.0)
    prob = prob[prob > 0]
    return float(-(prob * np.log2(prob)).sum())


def tenengrad(gray: np.ndarray) -> float:
    gx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    gy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    mag_sq = gx * gx + gy * gy
    return float(np.mean(mag_sq))


def quality_metrics(rgb: np.ndarray) -> Dict[str, float]:
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    height, width = gray.shape[:2]
    lap_var = float(cv2.Laplacian(gray, cv2.CV_64F).var())
    return {
        "width": float(width),
        "height": float(height),
        "megapixels": float((width * height) / 1_000_000),
        "aspect_ratio": float(width / height) if height else float("nan"),
        "luma_mean": float(gray.mean()),
        "luma_std": float(gray.std()),
        "luma_p01": float(np.percentile(gray, 1)),
        "luma_p99": float(np.percentile(gray, 99)),
        "saturation_mean": float(hsv[:, :, 1].mean()),
        "saturation_std": float(hsv[:, :, 1].std()),
        "laplacian_var": lap_var,
        "tenengrad": tenengrad(gray),
        "entropy": entropy_u8(gray),
    }


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
            "quality_readable": "False",
            "decoder": "",
            "width": "",
            "height": "",
            "megapixels": "",
            "aspect_ratio": "",
            "luma_mean": "",
            "luma_std": "",
            "luma_p01": "",
            "luma_p99": "",
            "saturation_mean": "",
            "saturation_std": "",
            "laplacian_var": "",
            "tenengrad": "",
            "entropy": "",
            "outlier_flags": "",
            "error": "",
        }
        try:
            if not path.exists():
                raise FileNotFoundError("file does not exist")
            result["exists"] = "True"
            rgb, decoder = decode_rgb(path)
            result["decoder"] = decoder
            metrics = quality_metrics(rgb)
            result.update({key: f"{value:.8g}" for key, value in metrics.items()})
            result["quality_readable"] = "True"
        except Exception as exc:  # pragma: no cover - exercised by bad data.
            result["error"] = f"{type(exc).__name__}: {exc}"
        output.append(result)
    return output


def numeric_values(rows: List[Dict[str, object]], field: str) -> List[float]:
    values: List[float] = []
    for row in rows:
        try:
            value = float(str(row.get(field, "")))
        except ValueError:
            continue
        if math.isfinite(value):
            values.append(value)
    return values


def percentile(values: List[float], q: float) -> float:
    if not values:
        return float("nan")
    return float(np.percentile(np.array(values, dtype=np.float64), q))


def build_thresholds(rows: List[Dict[str, object]], outlier_percentile: float) -> Dict[str, float]:
    candidate_rows = [row for row in rows if row.get("include_candidate") == "True" and row.get("quality_readable") == "True"]
    low = outlier_percentile
    high = 100.0 - outlier_percentile
    return {
        "low_luma_mean": percentile(numeric_values(candidate_rows, "luma_mean"), low),
        "high_luma_mean": percentile(numeric_values(candidate_rows, "luma_mean"), high),
        "low_luma_std": percentile(numeric_values(candidate_rows, "luma_std"), low),
        "low_laplacian_var": percentile(numeric_values(candidate_rows, "laplacian_var"), low),
        "low_tenengrad": percentile(numeric_values(candidate_rows, "tenengrad"), low),
        "low_saturation_mean": percentile(numeric_values(candidate_rows, "saturation_mean"), low),
        "high_saturation_mean": percentile(numeric_values(candidate_rows, "saturation_mean"), high),
        "low_megapixels": percentile(numeric_values(candidate_rows, "megapixels"), low),
        "high_megapixels": percentile(numeric_values(candidate_rows, "megapixels"), high),
        "low_aspect_ratio": percentile(numeric_values(candidate_rows, "aspect_ratio"), low),
        "high_aspect_ratio": percentile(numeric_values(candidate_rows, "aspect_ratio"), high),
    }


def to_float(row: Dict[str, object], field: str) -> Optional[float]:
    try:
        value = float(str(row.get(field, "")))
    except ValueError:
        return None
    return value if math.isfinite(value) else None


def assign_outlier_flags(rows: List[Dict[str, object]], thresholds: Dict[str, float]) -> None:
    for row in rows:
        if row.get("quality_readable") != "True" or row.get("include_candidate") != "True":
            continue
        flags: List[str] = []
        checks = [
            ("luma_mean", "<=", "low_luma_mean", "low_luminance"),
            ("luma_mean", ">=", "high_luma_mean", "high_luminance"),
            ("luma_std", "<=", "low_luma_std", "low_contrast"),
            ("laplacian_var", "<=", "low_laplacian_var", "low_laplacian_sharpness"),
            ("tenengrad", "<=", "low_tenengrad", "low_tenengrad_edges"),
            ("saturation_mean", "<=", "low_saturation_mean", "low_saturation"),
            ("saturation_mean", ">=", "high_saturation_mean", "high_saturation"),
            ("megapixels", "<=", "low_megapixels", "small_resolution"),
            ("megapixels", ">=", "high_megapixels", "large_resolution"),
            ("aspect_ratio", "<=", "low_aspect_ratio", "low_aspect_ratio"),
            ("aspect_ratio", ">=", "high_aspect_ratio", "high_aspect_ratio"),
        ]
        for field, op, threshold_key, flag in checks:
            value = to_float(row, field)
            threshold = thresholds.get(threshold_key)
            if value is None or threshold is None or not math.isfinite(threshold):
                continue
            if op == "<=" and value <= threshold:
                flags.append(flag)
            elif op == ">=" and value >= threshold:
                flags.append(flag)
        row["outlier_flags"] = ",".join(flags)


def write_tsv(path: Path, rows: List[Dict[str, object]], fieldnames: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(rows)


def summarize(rows: List[Dict[str, object]], thresholds: Dict[str, float], args: argparse.Namespace) -> Dict[str, object]:
    readable_rows = [row for row in rows if row.get("quality_readable") == "True"]
    candidate_rows = [row for row in rows if row.get("include_candidate") == "True"]
    candidate_readable_rows = [row for row in candidate_rows if row.get("quality_readable") == "True"]
    outlier_rows = [row for row in candidate_readable_rows if str(row.get("outlier_flags", ""))]
    flag_counter: Counter[str] = Counter()
    for row in outlier_rows:
        for flag in str(row.get("outlier_flags", "")).split(","):
            if flag:
                flag_counter[flag] += 1
    decoder_counts = Counter(str(row.get("decoder", "")) for row in readable_rows)

    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "inventory": str(Path(args.inventory)),
        "outlier_percentile": args.outlier_percentile,
        "rows_total": len(rows),
        "candidate_rows": len(candidate_rows),
        "quality_readable_total": len(readable_rows),
        "candidate_quality_readable": len(candidate_readable_rows),
        "quality_unreadable_total": len(rows) - len(readable_rows),
        "decoder_counts": dict(sorted(decoder_counts.items())),
        "outlier_candidate_rows": len(outlier_rows),
        "outlier_flag_counts": dict(sorted(flag_counter.items())),
        "thresholds": thresholds,
        "boundary": (
            "Quality outliers are percentile-based manual-review candidates, not automatic exclusion decisions. "
            "This audit does not change the current formal 502/496 protocols and does not run enhancement."
        ),
    }


def write_summary_md(path: Path, summary: Dict[str, object], output_paths: Dict[str, str]) -> None:
    lines = [
        "# full_algae_dewatermark_v1 quality outlier audit",
        "",
        f"日期：{datetime.now().date().isoformat()}",
        "",
        "本文是完整增强图像池的只读质量异常审计，不是增强实验结果。",
        "",
        "## Summary",
        "",
        f"- Total image rows: `{summary['rows_total']}`",
        f"- Candidate rows: `{summary['candidate_rows']}`",
        f"- Quality-readable rows: `{summary['quality_readable_total']}`",
        f"- Candidate quality-readable rows: `{summary['candidate_quality_readable']}`",
        f"- Decoder counts: `{summary['decoder_counts']}`",
        f"- Outlier percentile: `{summary['outlier_percentile']}`",
        f"- Candidate outlier rows: `{summary['outlier_candidate_rows']}`",
        f"- Outlier flag counts: `{summary['outlier_flag_counts']}`",
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
            "- Outlier thresholds are percentile-based over candidate images.",
            "- Flags indicate samples for manual review, not automatic deletion or exclusion.",
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
    thresholds = build_thresholds(rows, args.outlier_percentile)
    assign_outlier_flags(rows, thresholds)

    audit_tsv = output_prefix.with_suffix(".tsv")
    outliers_tsv = output_prefix.with_name(output_prefix.name + "_outliers.tsv")
    summary_json = output_prefix.with_suffix(".summary.json")
    summary_md = output_prefix.with_suffix(".summary.md")

    fieldnames = [
        "row_index",
        "include_candidate",
        "relative_path",
        "top_level_folder",
        "file_name",
        "extension",
        "size_bytes",
        "absolute_path",
        "exists",
        "quality_readable",
        "decoder",
        "width",
        "height",
        "megapixels",
        "aspect_ratio",
        "luma_mean",
        "luma_std",
        "luma_p01",
        "luma_p99",
        "saturation_mean",
        "saturation_std",
        "laplacian_var",
        "tenengrad",
        "entropy",
        "outlier_flags",
        "error",
    ]
    write_tsv(audit_tsv, rows, fieldnames)
    outlier_rows = [row for row in rows if str(row.get("outlier_flags", ""))]
    write_tsv(outliers_tsv, outlier_rows, fieldnames)

    summary = summarize(rows, thresholds, args)
    summary_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    write_summary_md(
        summary_md,
        summary,
        {
            "per-image quality audit": str(audit_tsv.relative_to(PROJECT_ROOT)),
            "outlier candidates": str(outliers_tsv.relative_to(PROJECT_ROOT)),
            "summary json": str(summary_json.relative_to(PROJECT_ROOT)),
        },
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
