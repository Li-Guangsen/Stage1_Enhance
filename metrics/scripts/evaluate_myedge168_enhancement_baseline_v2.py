from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

import cv2
import numpy as np

try:
    from scipy.stats import skew as scipy_skew
except Exception:  # pragma: no cover - scipy is available in the project env.
    scipy_skew = None

try:
    from scipy.fftpack import dct as scipy_dct
except Exception:  # pragma: no cover - scipy is available in the project env.
    scipy_dct = None


STAGE1_ROOT = Path(__file__).resolve().parents[2]
METRICS_ROOT = STAGE1_ROOT / "metrics"
if str(METRICS_ROOT) not in sys.path:
    sys.path.insert(0, str(METRICS_ROOT))

from libs.EME import EME
from libs.EMEE import EMEE
from libs.Gradient import Gradient
from libs.UCIQE import calc_uciqe
from libs.UIQM import calc_uiqm
from libs.calc_InEntropy import get_entropy
from libs.Contrast_ratio import contrast
from libs.msssim import msssim


RUN_ROOT = STAGE1_ROOT / "experiments" / "myedge168_compare9_rerun_20260527"
RAW_MANIFEST = RUN_ROOT / "manifests" / "myedge168_input_manifest.csv"
OUTPUT_ROOT = RUN_ROOT / "metrics" / "enhancement_metrics_eaai_aligned_v2"
NORMALIZED_ROOT = RUN_ROOT / "outputs_normalized"

IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp")
ENHANCEMENT_METHODS = [
    "Ours",
    "HVDualformer",
    "ABC-Former",
    "GDCP",
    "CBF",
    "HLRP",
    "SGUIE-Net",
    "Histoformer",
    "WWPF",
]
NO_WWPF_METHODS = [m for m in ENHANCEMENT_METHODS if m != "WWPF"]
HIGH_NOISE_METHODS = {"HLRP", "Histoformer"}
INCOMPLETE_METHODS = {"WWPF"}

BASE_METRICS = [
    "EME",
    "EMEE",
    "Entropy",
    "Contrast",
    "AvgGra",
    "MS_SSIM",
    "PSNR",
    "UCIQE",
    "UIQM",
    "SSEQ",
    "SIFT_GOOD_MATCHES",
    "SIFT_MATCH_RATIO",
]
MAIN_METRICS = ["UIQM", "UCIQE", "SSEQ", "SIFT_MATCH_RATIO"]
SSEQ_FEATURE_COLUMNS = [
    "SSEQ_S1_SPATIAL_MEAN",
    "SSEQ_S1_SPATIAL_SKEW",
    "SSEQ_S1_SPECTRAL_MEAN",
    "SSEQ_S1_SPECTRAL_SKEW",
    "SSEQ_S2_SPATIAL_MEAN",
    "SSEQ_S2_SPATIAL_SKEW",
    "SSEQ_S2_SPECTRAL_MEAN",
    "SSEQ_S2_SPECTRAL_SKEW",
    "SSEQ_S3_SPATIAL_MEAN",
    "SSEQ_S3_SPATIAL_SKEW",
    "SSEQ_S3_SPECTRAL_MEAN",
    "SSEQ_S3_SPECTRAL_SKEW",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Recompute MyEdge 168 enhancement metrics with EAAI-aligned SSEQ and SIFT matching."
    )
    parser.add_argument("--run-root", type=Path, default=RUN_ROOT)
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_ROOT)
    parser.add_argument("--resize-to", nargs=2, type=int, default=(320, 320), metavar=("WIDTH", "HEIGHT"))
    parser.add_argument("--lowe-ratio", type=float, default=0.75)
    parser.add_argument("--block-size", type=int, default=8)
    return parser.parse_args()


def read_bgr(path: Path) -> np.ndarray:
    data = np.fromfile(str(path), dtype=np.uint8)
    img = cv2.imdecode(data, cv2.IMREAD_COLOR)
    if img is None:
        raise RuntimeError(f"cv2.imdecode failed: {path}")
    return img


def resize_bgr(img: np.ndarray, resize_to: Optional[Tuple[int, int]]) -> np.ndarray:
    if resize_to is None:
        return img
    width, height = resize_to
    if img.shape[1] == width and img.shape[0] == height:
        return img
    return cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)


def read_raw_manifest(path: Path) -> List[Dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 168:
        raise RuntimeError(f"MyEdge raw manifest must contain 168 rows, got {len(rows)}: {path}")
    seen = set()
    for row in rows:
        stem = row["stem"]
        if stem in seen:
            raise RuntimeError(f"Duplicate raw stem in manifest: {stem}")
        seen.add(stem)
        source = Path(row["source_path"])
        if not source.is_file():
            raise RuntimeError(f"Missing raw source path for {stem}: {source}")
    return rows


def list_images(root: Path) -> List[Path]:
    if not root.is_dir():
        return []
    return sorted(
        [p for p in root.iterdir() if p.is_file() and p.suffix.lower() in IMAGE_EXTS],
        key=lambda p: p.name.lower(),
    )


def build_output_index(method: str, normalized_root: Path) -> Dict[str, Path]:
    method_dir = normalized_root / method
    paths = list_images(method_dir)
    index: Dict[str, Path] = {}
    for path in paths:
        stem = path.stem
        if stem in index:
            raise RuntimeError(f"Duplicate output stem for {method}: {stem}")
        index[stem] = path
    return index


def block_values(gray: np.ndarray, block_size: int) -> np.ndarray:
    h, w = gray.shape[:2]
    usable_h = (h // block_size) * block_size
    usable_w = (w // block_size) * block_size
    if usable_h == 0 or usable_w == 0:
        return np.empty((0, block_size, block_size), dtype=gray.dtype)
    cropped = gray[:usable_h, :usable_w]
    blocks = cropped.reshape(usable_h // block_size, block_size, usable_w // block_size, block_size)
    return blocks.swapaxes(1, 2).reshape(-1, block_size, block_size)


def spatial_entropy_blocks(blocks: np.ndarray) -> List[float]:
    if blocks.size == 0:
        return []
    flat = np.clip(np.rint(blocks.reshape(blocks.shape[0], -1)), 0, 255).astype(np.int32)
    offsets = (np.arange(flat.shape[0], dtype=np.int32) * 256)[:, None]
    hist = np.bincount((flat + offsets).reshape(-1), minlength=flat.shape[0] * 256)
    hist = hist.reshape(flat.shape[0], 256).astype(np.float64)
    prob = hist / np.maximum(hist.sum(axis=1, keepdims=True), 1.0)
    with np.errstate(divide="ignore", invalid="ignore"):
        ent = -np.nansum(np.where(prob > 0, prob * np.log2(prob), 0.0), axis=1)
    return ent.astype(np.float64).tolist()


def spectral_entropy_blocks(blocks: np.ndarray) -> List[float]:
    if blocks.size == 0:
        return []
    blocks_f = blocks.astype(np.float32)
    if scipy_dct is not None:
        coeff = scipy_dct(scipy_dct(blocks_f, axis=1, norm="ortho"), axis=2, norm="ortho")
    else:
        coeff = np.stack([cv2.dct(block) for block in blocks_f], axis=0)
    power = np.square(np.abs(coeff)).reshape(blocks_f.shape[0], -1).astype(np.float64)
    prob = power / np.maximum(power.sum(axis=1, keepdims=True), 1e-12)
    with np.errstate(divide="ignore", invalid="ignore"):
        ent = -np.nansum(np.where(prob > 0, prob * np.log2(prob), 0.0), axis=1)
    ent = ent / math.log2(blocks_f.shape[1] * blocks_f.shape[2])
    return ent.astype(np.float64).tolist()


def safe_skew(values: Sequence[float]) -> float:
    if not values:
        return 0.0
    arr = np.asarray(values, dtype=np.float64)
    if arr.size < 3 or float(np.std(arr)) <= 1e-12:
        return 0.0
    if scipy_skew is not None:
        value = float(scipy_skew(arr, bias=False))
        return value if math.isfinite(value) else 0.0
    centered = arr - float(np.mean(arr))
    std = float(np.std(arr))
    return float(np.mean(np.power(centered / std, 3)))


def sseq_features(gray: np.ndarray, block_size: int = 8) -> Tuple[float, Dict[str, float]]:
    """Extract SSEQ-style spatial/spectral entropy features.

    This is a transparent reimplementation of the SSEQ feature extractor described
    by Liu et al. (2014). The original SSEQ release also uses a learned quality
    model. That private/official predictor is not bundled here, so the scalar
    `SSEQ` below is the mean of spatial/spectral entropy means across scales.
    """
    gray_f = gray.astype(np.float32)
    features: Dict[str, float] = {}
    entropy_means: List[float] = []
    current = gray_f
    for scale in range(1, 4):
        blocks = block_values(current, block_size)
        spatial = spatial_entropy_blocks(blocks)
        spectral = spectral_entropy_blocks(blocks)
        spatial_mean = float(np.mean(spatial)) if spatial else 0.0
        spectral_mean = float(np.mean(spectral)) if spectral else 0.0
        features[f"SSEQ_S{scale}_SPATIAL_MEAN"] = spatial_mean
        features[f"SSEQ_S{scale}_SPATIAL_SKEW"] = safe_skew(spatial)
        features[f"SSEQ_S{scale}_SPECTRAL_MEAN"] = spectral_mean
        features[f"SSEQ_S{scale}_SPECTRAL_SKEW"] = safe_skew(spectral)
        entropy_means.extend([spatial_mean, spectral_mean])
        if min(current.shape[:2]) < block_size * 2:
            current = cv2.resize(current, (max(1, current.shape[1] // 2), max(1, current.shape[0] // 2)))
        else:
            current = cv2.pyrDown(current)
    return float(np.mean(entropy_means)) if entropy_means else 0.0, features


def sift_match(raw_gray: np.ndarray, enhanced_gray: np.ndarray, lowe_ratio: float) -> Dict[str, Optional[float]]:
    sift = cv2.SIFT_create()
    kp_raw, des_raw = sift.detectAndCompute(raw_gray, None)
    kp_enh, des_enh = sift.detectAndCompute(enhanced_gray, None)
    raw_count = len(kp_raw) if kp_raw is not None else 0
    enhanced_count = len(kp_enh) if kp_enh is not None else 0
    if des_raw is None or des_enh is None or raw_count == 0 or enhanced_count == 0:
        return {
            "SIFT_RAW_KEYPOINTS": float(raw_count),
            "SIFT_ENHANCED_KEYPOINTS": float(enhanced_count),
            "SIFT_GOOD_MATCHES": 0.0,
            "SIFT_MATCH_RATIO": 0.0,
        }
    matcher = cv2.BFMatcher(cv2.NORM_L2, crossCheck=False)
    knn = matcher.knnMatch(des_raw, des_enh, k=2)
    good = []
    for pair in knn:
        if len(pair) < 2:
            continue
        m, n = pair
        if m.distance < lowe_ratio * n.distance:
            good.append(m)
    denom = max(min(raw_count, enhanced_count), 1)
    return {
        "SIFT_RAW_KEYPOINTS": float(raw_count),
        "SIFT_ENHANCED_KEYPOINTS": float(enhanced_count),
        "SIFT_GOOD_MATCHES": float(len(good)),
        "SIFT_MATCH_RATIO": float(len(good) / denom),
    }


def compute_metrics(
    raw_path: Path,
    result_path: Path,
    resize_to: Optional[Tuple[int, int]],
    lowe_ratio: float,
    block_size: int,
    is_raw_anchor: bool,
) -> Dict[str, object]:
    raw_bgr = resize_bgr(read_bgr(raw_path), resize_to)
    result_bgr = resize_bgr(read_bgr(result_path), resize_to)
    raw_gray = cv2.cvtColor(raw_bgr, cv2.COLOR_BGR2GRAY)
    result_gray = cv2.cvtColor(result_bgr, cv2.COLOR_BGR2GRAY)

    sseq_value, sseq_detail = sseq_features(result_gray, block_size=block_size)

    out: Dict[str, object] = {
        "EME": float(EME(result_gray)),
        "EMEE": float(EMEE(result_gray)),
        "Entropy": float(get_entropy(result_gray)),
        "Contrast": float(contrast(result_gray)),
        "AvgGra": float(Gradient(result_gray)),
        "MS_SSIM": float(msssim(raw_bgr, result_bgr)),
        "PSNR": float(cv2.PSNR(raw_gray, result_gray)),
        "UCIQE": float(calc_uciqe(result_bgr)),
        "UIQM": float(calc_uiqm(result_bgr)),
        "SSEQ": sseq_value,
        **sseq_detail,
    }
    if is_raw_anchor:
        out.update(
            {
                "SIFT_RAW_KEYPOINTS": "",
                "SIFT_ENHANCED_KEYPOINTS": "",
                "SIFT_GOOD_MATCHES": "",
                "SIFT_MATCH_RATIO": "",
                "SIFT_MATCH_STATUS": "reference_na",
            }
        )
    else:
        out.update(sift_match(raw_gray, result_gray, lowe_ratio=lowe_ratio))
        out["SIFT_MATCH_STATUS"] = "ok"
    return out


def is_number(value: object) -> bool:
    if value == "" or value is None:
        return False
    try:
        return math.isfinite(float(value)) or math.isinf(float(value))
    except Exception:
        return False


def csv_format(value: object) -> object:
    if value == "" or value is None:
        return ""
    if isinstance(value, str):
        return value
    try:
        v = float(value)
    except Exception:
        return value
    if math.isnan(v):
        return "nan"
    if math.isinf(v):
        return "inf" if v > 0 else "-inf"
    return f"{v:.10g}"


def write_csv(path: Path, rows: Sequence[Dict[str, object]], fieldnames: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: csv_format(row.get(field, "")) for field in fieldnames})


def summarize(rows: Sequence[Dict[str, object]], metrics: Sequence[str]) -> List[Dict[str, object]]:
    methods = []
    seen = set()
    for row in rows:
        method = str(row["method"])
        if method not in seen:
            seen.add(method)
            methods.append(method)
    summary_rows: List[Dict[str, object]] = []
    for method in methods:
        method_rows = [r for r in rows if r["method"] == method]
        out: Dict[str, object] = {
            "Method": method,
            "Role": method_rows[0].get("method_role", ""),
            "Count": len(method_rows),
        }
        for metric in metrics:
            values = []
            for row in method_rows:
                value = row.get(metric, "")
                if value == "" or value is None:
                    continue
                try:
                    f = float(value)
                except Exception:
                    continue
                if math.isinf(f):
                    values.append(f)
                elif math.isfinite(f):
                    values.append(f)
            if not values:
                out[metric] = ""
            elif any(math.isinf(v) for v in values):
                out[metric] = "inf"
            else:
                out[metric] = float(np.mean(values))
        summary_rows.append(out)
    return summary_rows


def markdown_table(rows: Sequence[Dict[str, object]], fieldnames: Sequence[str]) -> str:
    if not rows:
        return ""
    lines = []
    lines.append("| " + " | ".join(fieldnames) + " |")
    lines.append("| " + " | ".join(["---"] * len(fieldnames)) + " |")
    for row in rows:
        values = []
        for field in fieldnames:
            value = row.get(field, "")
            if isinstance(value, float):
                values.append(f"{value:.4f}")
            else:
                values.append(str(value))
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines) + "\n"


def write_markdown_table(path: Path, rows: Sequence[Dict[str, object]], fieldnames: Sequence[str], title: str) -> None:
    path.write_text(f"# {title}\n\n" + markdown_table(rows, fieldnames), encoding="utf-8")


def common_stems(raw_rows: Sequence[Dict[str, str]], indexes: Dict[str, Dict[str, Path]], methods: Sequence[str]) -> List[str]:
    stems = {row["stem"] for row in raw_rows}
    for method in methods:
        stems &= set(indexes[method].keys())
    return sorted(stems)


def method_role(method: str) -> str:
    if method == "raw":
        return "anchor_raw"
    if method in HIGH_NOISE_METHODS:
        return "enhancement_high_noise_diagnostic"
    if method in INCOMPLETE_METHODS:
        return "enhancement_incomplete_166_of_168"
    if method == "Ours":
        return "legacy_ours_reference"
    return "enhancement_reference"


def build_rows(
    raw_rows: Sequence[Dict[str, str]],
    indexes: Dict[str, Dict[str, Path]],
    stems: Sequence[str],
    methods: Sequence[str],
    resize_to: Optional[Tuple[int, int]],
    lowe_ratio: float,
    block_size: int,
    include_raw: bool = True,
) -> List[Dict[str, object]]:
    raw_by_stem = {row["stem"]: row for row in raw_rows}
    rows: List[Dict[str, object]] = []
    total = len(stems) * (len(methods) + (1 if include_raw else 0))
    done = 0
    started = datetime.now()
    for stem in stems:
        raw_row = raw_by_stem[stem]
        raw_path = Path(raw_row["source_path"])
        entries = []
        if include_raw:
            entries.append(("raw", raw_path, True))
        entries.extend((method, indexes[method][stem], False) for method in methods)
        for method, result_path, is_raw in entries:
            done += 1
            if done == 1 or done % 100 == 0 or done == total:
                elapsed = (datetime.now() - started).total_seconds()
                print(f"[metrics] {done}/{total} rows | elapsed {elapsed:.1f}s | current {method}:{stem}", flush=True)
            metrics = compute_metrics(
                raw_path=raw_path,
                result_path=result_path,
                resize_to=resize_to,
                lowe_ratio=lowe_ratio,
                block_size=block_size,
                is_raw_anchor=is_raw,
            )
            rows.append(
                {
                    "method": method,
                    "method_role": method_role(method),
                    "stem": stem,
                    "raw_filename": raw_row["filename"],
                    "raw_sha256": raw_row["sha256"],
                    "raw_path": str(raw_path),
                    "result_path": str(result_path),
                    **metrics,
                }
            )
    return rows


def build_rank_summary(summary_rows: Sequence[Dict[str, object]]) -> Tuple[List[Dict[str, object]], List[Dict[str, object]]]:
    rank_rows: List[Dict[str, object]] = []
    bottom_rows: List[Dict[str, object]] = []
    enhanced_rows = [r for r in summary_rows if r["Method"] != "raw"]
    for metric in MAIN_METRICS:
        metric_rows = []
        for row in enhanced_rows:
            value = row.get(metric, "")
            if value == "" or value is None:
                continue
            value_f = float(value)
            if not math.isfinite(value_f):
                continue
            metric_rows.append((str(row["Method"]), str(row["Role"]), value_f))
        metric_rows.sort(key=lambda item: item[2], reverse=True)
        total = len(metric_rows)
        bottom_cut = max(1, math.ceil(total / 3))
        bottom_methods = set(method for method, _, _ in metric_rows[-bottom_cut:])
        for rank, (method, role, value) in enumerate(metric_rows, start=1):
            rank_rows.append(
                {
                    "metric": metric,
                    "direction": "higher_is_better_for_screening",
                    "method": method,
                    "role": role,
                    "value": value,
                    "rank": rank,
                    "total_ranked": total,
                    "bottom_third": "yes" if method in bottom_methods else "no",
                }
            )
    by_method: Dict[str, Dict[str, object]] = {}
    for method in [str(r["Method"]) for r in enhanced_rows]:
        by_method[method] = {
            "method": method,
            "role": next(str(r["Role"]) for r in enhanced_rows if r["Method"] == method),
            "main_metric_bottom_third_count": 0,
            "screening_status": "",
        }
    for row in rank_rows:
        if row["bottom_third"] == "yes":
            by_method[str(row["method"])]["main_metric_bottom_third_count"] += 1
    for method, row in by_method.items():
        count = int(row["main_metric_bottom_third_count"])
        row["screening_status"] = "fails_future_candidate_rule" if count >= 3 else "passes_future_candidate_rule"
    bottom_rows = list(by_method.values())
    bottom_rows.sort(key=lambda row: (-int(row["main_metric_bottom_third_count"]), str(row["method"])))
    return rank_rows, bottom_rows


def write_diagnostic_methods(path: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# Diagnostic Method Notes",
                "",
                "- `raw` is an anchor, not an enhancement method. Its `SIFT_MATCH_RATIO` is `NA` because SIFT matching is defined as raw-enhanced matching.",
                "- `Ours` is the legacy Stage1 reference output for this MyEdge 168 rerun. It is retained for historical comparison and is not a hard target for future candidates.",
                "- `HLRP` and `Histoformer` remain in the numeric table but are marked as `enhancement_high_noise_diagnostic`; high no-reference scores from noisy outputs must not be interpreted as stable positive enhancement.",
                "- `WWPF` is marked as `enhancement_incomplete_166_of_168`; it failed on two MyEdge 168 stems in the rerun and is included only in the 166-stem complete-case main table.",
                "- Future candidates should use `UIQM`, `UCIQE`, `SSEQ`, and `SIFT_MATCH_RATIO` as the first screening group, but downstream fixed-detector validation remains the final criterion.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def write_metric_definitions(path: Path, args: argparse.Namespace) -> None:
    definitions = {
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "metric_policy": "EAAI-aligned enhancement baseline plus existing Stage1 diagnostic metrics",
        "main_enhancement_metrics": MAIN_METRICS,
        "diagnostic_metrics": ["EME", "EMEE", "Entropy", "Contrast", "AvgGra"],
        "structure_guard_metrics": ["MS_SSIM", "PSNR"],
        "sift_match": {
            "definition": "raw-enhanced grayscale OpenCV SIFT matching with Lowe ratio test",
            "lowe_ratio": args.lowe_ratio,
            "ratio_formula": "SIFT_GOOD_MATCHES / max(min(raw_keypoints, enhanced_keypoints), 1)",
            "raw_anchor_policy": "raw SIFT_MATCH_RATIO is NA and is excluded from SIFT_MATCH ranking",
        },
        "sseq": {
            "column": "SSEQ",
            "implementation": "SSEQ_reimplementation_feature_mean",
            "reference": "Liu et al. 2014, No-reference image quality assessment based on spatial and spectral entropies",
            "note": "The original SSEQ release also uses a learned quality predictor. This script extracts SSEQ-style spatial/spectral entropy features and reports the mean of spatial/spectral entropy means across three scales as a transparent scalar. It is not claimed to be the EAAI authors' private code.",
            "block_size": args.block_size,
            "feature_columns": SSEQ_FEATURE_COLUMNS,
        },
    }
    path.write_text(json.dumps(definitions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_run_report(path: Path, summary: Dict[str, object], bottom_rows: Sequence[Dict[str, object]]) -> None:
    lines = [
        "# MyEdge 168 Enhancement Metrics Baseline v2",
        "",
        f"- Created at: `{summary['created_at']}`",
        f"- Run root: `{summary['run_root']}`",
        f"- Output dir: `{summary['output_dir']}`",
        "- Scope: enhancement metrics only. No DiffusionEdge/MSFI inference, no `eval.py`, no `show.py`, no 502/496, no 2770.",
        "- Data source: `D:/Desktop/MyEdgeCodex/input_test/algae`, 168 raw images.",
        "- Main table policy: 9 enhancement methods on 166 complete-case stems because WWPF has 166/168 outputs.",
        "- Supplement table policy: raw + 8 complete methods on all 168 stems, excluding WWPF.",
        "- Main enhancement metrics: `UIQM`, `UCIQE`, `SSEQ`, `SIFT_MATCH_RATIO`.",
        "- Diagnostic metrics: `EME`, `EMEE`, `Entropy`, `Contrast`, `AvgGra`.",
        "- Structure consistency guards: `MS_SSIM`, `PSNR`.",
        "- `SSEQ` is `SSEQ_reimplementation_feature_mean`, not an EAAI private-code reproduction.",
        "- `SIFT_MATCH_RATIO` is raw-enhanced OpenCV SIFT matching with Lowe ratio 0.75; raw anchor is `NA`.",
        "",
        "## Outputs",
        "",
        "- `mean_metrics_9method_complete_case_166.csv/md`",
        "- `mean_metrics_8method_no_wwpf_168.csv/md`",
        "- `per_image_metrics_166.csv`",
        "- `per_image_metrics_168_no_wwpf.csv`",
        "- `rank_summary_166.csv/md`",
        "- `screening_rule_summary_166.csv/md`",
        "- `diagnostic_methods.md`",
        "- `metric_definitions.json`",
        "- `summary.json`",
        "",
        "## Future Candidate Screening Rule",
        "",
        "A future Stage1 enhancement candidate should not have 3 or more of the 4 main enhancement metrics in the bottom third: `UIQM`, `UCIQE`, `SSEQ`, `SIFT_MATCH_RATIO`. This is only the first enhancement-quality screen; fixed-detector MyEdge downstream validation remains the final criterion.",
        "",
        "## Current Methods Under This Rule",
        "",
        markdown_table(list(bottom_rows), ["method", "role", "main_metric_bottom_third_count", "screening_status"]),
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    run_root = args.run_root
    output_dir = args.output_dir
    manifest_path = run_root / "manifests" / "myedge168_input_manifest.csv"
    normalized_root = run_root / "outputs_normalized"
    resize_to = tuple(args.resize_to) if args.resize_to else None

    raw_rows = read_raw_manifest(manifest_path)
    indexes = {method: build_output_index(method, normalized_root) for method in ENHANCEMENT_METHODS}
    counts = {method: len(indexes[method]) for method in ENHANCEMENT_METHODS}
    if any(counts[m] != 168 for m in NO_WWPF_METHODS):
        raise RuntimeError(f"All no-WWPF methods must have 168 outputs, got {counts}")
    if counts["WWPF"] != 166:
        raise RuntimeError(f"WWPF must have 166 outputs for this protocol, got {counts['WWPF']}")

    complete166 = common_stems(raw_rows, indexes, ENHANCEMENT_METHODS)
    complete168_no_wwpf = common_stems(raw_rows, indexes, NO_WWPF_METHODS)
    if len(complete166) != 166:
        raise RuntimeError(f"9-method complete case must contain 166 stems, got {len(complete166)}")
    if len(complete168_no_wwpf) != 168:
        raise RuntimeError(f"8-method no-WWPF set must contain 168 stems, got {len(complete168_no_wwpf)}")

    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "complete_case_166_stems.txt").write_text("\n".join(complete166) + "\n", encoding="utf-8")
    (output_dir / "no_wwpf_168_stems.txt").write_text("\n".join(complete168_no_wwpf) + "\n", encoding="utf-8")

    print("[metrics] building shared raw + 8-method no-WWPF 168 rows", flush=True)
    rows168 = build_rows(
        raw_rows=raw_rows,
        indexes=indexes,
        stems=complete168_no_wwpf,
        methods=NO_WWPF_METHODS,
        resize_to=resize_to,
        lowe_ratio=args.lowe_ratio,
        block_size=args.block_size,
    )
    print("[metrics] building WWPF 166 rows", flush=True)
    wwpf_rows = build_rows(
        raw_rows=raw_rows,
        indexes=indexes,
        stems=complete166,
        methods=["WWPF"],
        resize_to=resize_to,
        lowe_ratio=args.lowe_ratio,
        block_size=args.block_size,
        include_raw=False,
    )
    complete166_set = set(complete166)
    rows166 = [row for row in rows168 if str(row["stem"]) in complete166_set] + wwpf_rows

    per_image_fields = [
        "method",
        "method_role",
        "stem",
        "raw_filename",
        "raw_sha256",
        "raw_path",
        "result_path",
        *BASE_METRICS,
        "SIFT_RAW_KEYPOINTS",
        "SIFT_ENHANCED_KEYPOINTS",
        "SIFT_MATCH_STATUS",
        *SSEQ_FEATURE_COLUMNS,
    ]
    mean_fields = ["Method", "Role", "Count", *BASE_METRICS]

    write_csv(output_dir / "per_image_metrics_166.csv", rows166, per_image_fields)
    write_csv(output_dir / "per_image_metrics_168_no_wwpf.csv", rows168, per_image_fields)

    summary166 = summarize(rows166, BASE_METRICS)
    summary168 = summarize(rows168, BASE_METRICS)
    write_csv(output_dir / "mean_metrics_9method_complete_case_166.csv", summary166, mean_fields)
    write_csv(output_dir / "mean_metrics_8method_no_wwpf_168.csv", summary168, mean_fields)
    write_markdown_table(
        output_dir / "mean_metrics_9method_complete_case_166.md",
        summary166,
        mean_fields,
        "Mean Metrics: 9 Enhancement Methods Complete-Case 166",
    )
    write_markdown_table(
        output_dir / "mean_metrics_8method_no_wwpf_168.md",
        summary168,
        mean_fields,
        "Mean Metrics: 8 Enhancement Methods Without WWPF, Full 168",
    )

    rank_rows, bottom_rows = build_rank_summary(summary166)
    rank_fields = ["metric", "direction", "method", "role", "value", "rank", "total_ranked", "bottom_third"]
    bottom_fields = ["method", "role", "main_metric_bottom_third_count", "screening_status"]
    write_csv(output_dir / "rank_summary_166.csv", rank_rows, rank_fields)
    write_csv(output_dir / "screening_rule_summary_166.csv", bottom_rows, bottom_fields)
    write_markdown_table(output_dir / "rank_summary_166.md", rank_rows, rank_fields, "Main Metric Rank Summary, 166 Complete-Case")
    write_markdown_table(
        output_dir / "screening_rule_summary_166.md",
        bottom_rows,
        bottom_fields,
        "Future Candidate Screening Rule Summary",
    )

    write_diagnostic_methods(output_dir / "diagnostic_methods.md")
    write_metric_definitions(output_dir / "metric_definitions.json", args)

    summary = {
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "run_root": str(run_root),
        "output_dir": str(output_dir),
        "raw_manifest": str(manifest_path),
        "raw_count": len(raw_rows),
        "method_output_counts": counts,
        "complete_case_166_count": len(complete166),
        "no_wwpf_168_count": len(complete168_no_wwpf),
        "methods": ENHANCEMENT_METHODS,
        "raw_anchor_included": True,
        "metrics": {
            "all": BASE_METRICS,
            "main": MAIN_METRICS,
            "diagnostic": ["EME", "EMEE", "Entropy", "Contrast", "AvgGra"],
            "structure_guards": ["MS_SSIM", "PSNR"],
        },
        "sseq_policy": "SSEQ_reimplementation_feature_mean; not EAAI private code",
        "sift_policy": "raw-enhanced SIFT with Lowe ratio 0.75; raw anchor SIFT_MATCH_RATIO is NA",
        "outputs": {
            "mean_166_csv": str(output_dir / "mean_metrics_9method_complete_case_166.csv"),
            "mean_168_no_wwpf_csv": str(output_dir / "mean_metrics_8method_no_wwpf_168.csv"),
            "per_image_166_csv": str(output_dir / "per_image_metrics_166.csv"),
            "per_image_168_no_wwpf_csv": str(output_dir / "per_image_metrics_168_no_wwpf.csv"),
            "rank_summary_csv": str(output_dir / "rank_summary_166.csv"),
            "screening_rule_summary_csv": str(output_dir / "screening_rule_summary_166.csv"),
            "run_report": str(output_dir / "run_report.md"),
        },
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_run_report(output_dir / "run_report.md", summary, bottom_rows)
    print(f"[metrics] done: {output_dir}", flush=True)


if __name__ == "__main__":
    main()
