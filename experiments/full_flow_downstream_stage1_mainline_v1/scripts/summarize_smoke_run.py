"""Summarize a full-flow Stage1 smoke run.

This script is intentionally local to the experiment directory. It computes
raw-vs-Final and per-stage proxy metrics, checks output completeness, and
creates visual panels without touching any locked Stage1 or MyEdge assets.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import cv2
import numpy as np


STAGES = ["BPH", "IMF1Ray", "RGHS", "CLAHE", "Fused", "Final"]


def _read_manifest(path: Path) -> list[str]:
    stems: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        item = line.strip()
        if not item or item.startswith("#"):
            continue
        suffix = Path(item).suffix.lower()
        if suffix in {".jpg", ".png", ".jpeg", ".tif", ".tiff", ".bmp"}:
            stems.append(Path(item).stem)
        else:
            stems.append(item)
    return stems


def _luma(img: np.ndarray) -> np.ndarray:
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB).astype(np.float32)
    return lab[..., 0] / 255.0


def _scharr_mean(luma: np.ndarray) -> float:
    gx = cv2.Scharr(luma.astype(np.float32), cv2.CV_32F, 1, 0)
    gy = cv2.Scharr(luma.astype(np.float32), cv2.CV_32F, 0, 1)
    mag = np.sqrt(gx * gx + gy * gy)
    return float(np.mean(mag))


def _metrics(raw: np.ndarray, candidate: np.ndarray) -> dict[str, float]:
    raw_f = raw.astype(np.float32)
    cand_f = candidate.astype(np.float32)
    raw_lab = cv2.cvtColor(raw, cv2.COLOR_BGR2LAB).astype(np.float32)
    cand_lab = cv2.cvtColor(candidate, cv2.COLOR_BGR2LAB).astype(np.float32)
    mse = float(np.mean((raw_f - cand_f) ** 2))
    psnr = 99.0 if mse <= 1e-12 else float(10.0 * np.log10((255.0 * 255.0) / mse))
    raw_grad = _scharr_mean(raw_lab[..., 0] / 255.0)
    cand_grad = _scharr_mean(cand_lab[..., 0] / 255.0)
    return {
        "mean_abs_bgr_delta": float(np.mean(np.abs(cand_f - raw_f))),
        "mean_abs_luma_delta": float(np.mean(np.abs(cand_lab[..., 0] - raw_lab[..., 0]))),
        "mean_abs_chroma_delta": float(np.mean(np.abs(cand_lab[..., 1:] - raw_lab[..., 1:]))),
        "psnr_vs_raw": psnr,
        "raw_grad_mean": raw_grad,
        "final_grad_mean": cand_grad,
        "grad_mean_ratio": float(cand_grad / (raw_grad + 1e-9)),
        "raw_luma_std": float(np.std(raw_lab[..., 0])),
        "final_luma_std": float(np.std(cand_lab[..., 0])),
        "luma_std_ratio": float(np.std(cand_lab[..., 0]) / (np.std(raw_lab[..., 0]) + 1e-9)),
    }


def _find_raw(input_dir: Path, stem: str) -> Path:
    for suffix in (".jpg", ".png", ".jpeg", ".tif", ".tiff", ".bmp"):
        path = input_dir / f"{stem}{suffix}"
        if path.exists():
            return path
    raise FileNotFoundError(f"Missing raw image for stem: {stem}")


def _stage_path(output_root: Path, stage: str, stem: str, fmt: str) -> Path:
    return output_root / fmt / stage / f"{stem}_{stage}.{fmt}"


def _put_label(img: np.ndarray, label: str) -> np.ndarray:
    out = img.copy()
    cv2.putText(
        out,
        label,
        (8, 18),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (0, 0, 255),
        1,
        cv2.LINE_AA,
    )
    return out


def _make_panel(raw: np.ndarray, stage_imgs: dict[str, np.ndarray], out_path: Path) -> None:
    images = [_put_label(raw, "Raw")]
    for stage in STAGES:
        images.append(_put_label(stage_imgs[stage], stage))
    h, w = raw.shape[:2]
    resized = [cv2.resize(img, (w, h), interpolation=cv2.INTER_AREA) for img in images]
    panel = cv2.hconcat(resized)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(out_path), panel, [int(cv2.IMWRITE_JPEG_QUALITY), 94])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--status", required=True)
    parser.add_argument("--decision", required=True)
    parser.add_argument("--input-dir", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--output-root", required=True)
    parser.add_argument("--experiment-root", default="experiments/full_flow_downstream_stage1_mainline_v1")
    parser.add_argument("--artifact-prefix", default="full_flow_downstream_stage1_mainline_v1")
    parser.add_argument("--title", default="full_flow_downstream_stage1_mainline_v1")
    parser.add_argument("--runtime-sec", type=float, required=True)
    args = parser.parse_args()

    run_id = args.run_id
    experiment_root = Path(args.experiment_root)
    input_dir = Path(args.input_dir)
    manifest = Path(args.manifest)
    output_root = Path(args.output_root)
    diagnostics_dir = experiment_root / "diagnostics" / run_id
    date = "20260527"

    stems = _read_manifest(manifest)
    completeness_rows: list[dict[str, object]] = []
    final_rows: list[dict[str, object]] = []
    stage_rows: list[dict[str, object]] = []
    missing: list[str] = []
    decode_failures: list[str] = []

    for stem in stems:
        raw_path = _find_raw(input_dir, stem)
        raw = cv2.imread(str(raw_path), cv2.IMREAD_COLOR)
        if raw is None:
            decode_failures.append(str(raw_path))
            continue
        stage_imgs: dict[str, np.ndarray] = {}
        for fmt in ("jpg", "png"):
            for stage in STAGES:
                path = _stage_path(output_root, stage, stem, fmt)
                if not path.exists():
                    missing.append(str(path))
                    continue
                img = cv2.imread(str(path), cv2.IMREAD_COLOR)
                if img is None:
                    decode_failures.append(str(path))
                    continue
                completeness_rows.append({"format": fmt, "stage": stage, "stem": stem})
                if fmt == "png":
                    row = {"stem": stem, "stage": stage}
                    row.update(_metrics(raw, img))
                    stage_rows.append(row)
                    stage_imgs[stage] = img
        if "Final" in stage_imgs:
            row = {"stem": stem}
            row.update(_metrics(raw, stage_imgs["Final"]))
            final_rows.append(row)
        if all(stage in stage_imgs for stage in STAGES):
            _make_panel(raw, stage_imgs, diagnostics_dir / f"{stem}_panel.jpg")

    artifact_prefix = args.artifact_prefix
    metrics_csv = experiment_root / f"{artifact_prefix}_{run_id}_metrics_{date}.csv"
    stage_csv = experiment_root / f"{artifact_prefix}_{run_id}_stage_metrics_{date}.csv"
    json_path = experiment_root / f"{artifact_prefix}_{run_id}_status_{date}.json"
    md_path = experiment_root / f"{artifact_prefix}_{run_id}_status_{date}.md"

    if final_rows:
        with metrics_csv.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(final_rows[0].keys()))
            writer.writeheader()
            writer.writerows(final_rows)
    if stage_rows:
        with stage_csv.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(stage_rows[0].keys()))
            writer.writeheader()
            writer.writerows(stage_rows)

    stage_counts: dict[str, dict[str, int]] = {}
    for row in completeness_rows:
        fmt = str(row["format"])
        stage = str(row["stage"])
        stage_counts.setdefault(fmt, {}).setdefault(stage, 0)
        stage_counts[fmt][stage] += 1

    mean_metrics: dict[str, float] = {}
    if final_rows:
        metric_names = [k for k in final_rows[0] if k != "stem"]
        for name in metric_names:
            mean_metrics[name] = float(np.mean([float(row[name]) for row in final_rows]))

    payload = {
        "run_id": run_id,
        "status": args.status,
        "decision": args.decision,
        "manifest": str(manifest),
        "output_root": str(output_root),
        "expected_images": len(stems),
        "runtime_sec": args.runtime_sec,
        "sec_per_image": args.runtime_sec / max(len(stems), 1),
        "projected_168_min": args.runtime_sec / max(len(stems), 1) * 168.0 / 60.0,
        "stage_counts": stage_counts,
        "missing_files": missing,
        "decode_failures": decode_failures,
        "final_rows": final_rows,
        "mean_metrics": mean_metrics,
        "metrics_csv": str(metrics_csv),
        "stage_metrics_csv": str(stage_csv),
        "visual_panels": [str(diagnostics_dir / f"{stem}_panel.jpg") for stem in stems],
    }
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        f"# {args.title} {run_id} status",
        "",
        "Date: 2026-05-27",
        "",
        "## Summary",
        "",
        f"- Status: `{args.status}`",
        f"- Manifest: `{manifest}`",
        f"- Output root: `{output_root}`",
        f"- Expected images: `{len(stems)}`",
        f"- Observed runtime: `{args.runtime_sec:.1f}` sec total, `{payload['sec_per_image']:.2f}` sec/image",
        f"- Projected 168 runtime: `{payload['projected_168_min']:.1f}` min",
        f"- Decision: `{args.decision}`",
        "",
        "## Output Completeness",
        "",
        "| Format | Stage | Count |",
        "|---|---|---:|",
    ]
    for fmt in ("jpg", "png"):
        for stage in STAGES:
            lines.append(f"| {fmt} | {stage} | {stage_counts.get(fmt, {}).get(stage, 0)} |")
    lines.extend([
        "",
        f"- Missing files: `{len(missing)}`",
        f"- Decode failures: `{len(decode_failures)}`",
        "",
        "## Raw-vs-Final Smoke Metrics",
        "",
        "| Stem | mean abs BGR delta | mean abs L delta | PSNR vs raw | grad mean ratio | luma std ratio |",
        "|---|---:|---:|---:|---:|---:|",
    ])
    for row in final_rows:
        lines.append(
            f"| {row['stem']} | {row['mean_abs_bgr_delta']:.3f} | "
            f"{row['mean_abs_luma_delta']:.3f} | {row['psnr_vs_raw']:.3f} | "
            f"{row['grad_mean_ratio']:.3f} | {row['luma_std_ratio']:.3f} |"
        )
    lines.extend([
        "",
        "Mean metrics:",
        "",
    ])
    for key in ("mean_abs_bgr_delta", "mean_abs_luma_delta", "mean_abs_chroma_delta", "psnr_vs_raw", "grad_mean_ratio", "luma_std_ratio"):
        if key in mean_metrics:
            lines.append(f"- {key}: `{mean_metrics[key]:.4f}`")
    lines.extend([
        "",
        "## Stage Metrics CSV",
        "",
        f"- `{stage_csv.name}`",
        "",
        "## Visual Panels",
        "",
    ])
    for stem in stems:
        lines.append(f"- `{diagnostics_dir / f'{stem}_panel.jpg'}`")
    lines.extend([
        "",
        "## Boundary",
        "",
        "- This is a smoke run only, not a downstream result.",
        "- It did not run MyEdge sampling, WSL eval/show, 502/496 metrics, or 2770 full-pool.",
        "- The decision only controls whether a broader visual/proxy smoke or 168 fixed-detector validation can be considered.",
        "",
    ])
    md_path.write_text("\n".join(lines), encoding="utf-8")
    print(md_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
