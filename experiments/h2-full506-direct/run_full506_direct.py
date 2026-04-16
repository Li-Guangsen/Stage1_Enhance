from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from datetime import datetime
from functools import cmp_to_key
from pathlib import Path
from typing import Any, Dict, List, Sequence, Tuple

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
METRICS_DIR = PROJECT_ROOT / "metrics"
if str(METRICS_DIR) not in sys.path:
    sys.path.insert(0, str(METRICS_DIR))

from clahe_guided_visibility import clahe_3ch_wb_safe
from wb_safe_contrast import wb_safe_contrast
from fusion_three import fuse_three_images_bgr
from lvbo import Gaussian_lvbo, entropy_boost_Lab
from metrics.protocol_common import build_image_index, read_bgr, read_manifest, resolve_project_path, write_image


EXPERIMENT_DIR = Path(__file__).resolve().parent
CONFIGS_DIR = EXPERIMENT_DIR / "configs"
LOGS_DIR = EXPERIMENT_DIR / "logs"
RESULTS_DIR = EXPERIMENT_DIR / "results"
SCORES_DIR = EXPERIMENT_DIR / "scores"
ANALYSIS_PATH = EXPERIMENT_DIR / "analysis.md"
SELECTION_PATH = EXPERIMENT_DIR / "selection.json"
STATUS_PATH = EXPERIMENT_DIR / "status.json"

BASE_CONFIG = PROJECT_ROOT / "experiments" / "optimization_v1" / "configs" / "locked_full506_mainline.json"
BASELINE_DIR = PROJECT_ROOT / "experiments" / "h1-graypixel-bph-ablation" / "outputs" / "full506" / "runs" / "full506_locked_mainline"
FULL_MANIFEST = PROJECT_ROOT / "metrics" / "outputs" / "evaluate_protocol_v2" / "full506_c25" / "complete_case_manifest.txt"


RGHS_CANDIDATES: List[Dict[str, Any]] = [
    {"name": "rghs_s01", "params": {"strength": 0.50, "clip_limit": 1.40, "brightness_boost": 1.04, "chroma_preserve": 0.84, "post_L_stretch": [2.0, 98.0], "post_chroma_gain": 1.02, "flat_floor": 0.45}},
    {"name": "rghs_s02", "params": {"strength": 0.55, "clip_limit": 1.50, "brightness_boost": 1.08, "chroma_preserve": 0.83, "post_L_stretch": [1.5, 98.5], "post_chroma_gain": 1.03, "flat_floor": 0.42}},
    {"name": "rghs_s03", "params": {"strength": 0.60, "clip_limit": 1.60, "brightness_boost": 1.06, "chroma_preserve": 0.82, "post_L_stretch": [2.0, 98.0], "post_chroma_gain": 1.03, "flat_floor": 0.40}},
    {"name": "rghs_s04", "params": {"strength": 0.68, "clip_limit": 1.80, "brightness_boost": 1.05, "chroma_preserve": 0.80, "post_L_stretch": [1.8, 98.2], "post_chroma_gain": 1.04, "flat_floor": 0.36}},
    {"name": "rghs_s05", "params": {"strength": 0.70, "clip_limit": 2.00, "brightness_boost": 1.04, "chroma_preserve": 0.84, "post_L_stretch": [2.0, 97.5], "post_chroma_gain": 1.03, "flat_floor": 0.35}},
    {"name": "rghs_s06", "params": {"strength": 0.58, "clip_limit": 1.70, "brightness_boost": 1.07, "chroma_preserve": 0.83, "post_L_stretch": [1.0, 99.0], "post_chroma_gain": 1.02, "flat_floor": 0.43}},
    {"name": "rghs_s07", "params": {"strength": 0.65, "clip_limit": 1.90, "brightness_boost": 1.08, "chroma_preserve": 0.80, "post_L_stretch": [1.0, 99.0], "post_chroma_gain": 1.04, "flat_floor": 0.38}},
    {"name": "rghs_s08", "params": {"strength": 0.62, "clip_limit": 1.50, "brightness_boost": 1.05, "chroma_preserve": 0.86, "post_L_stretch": [2.5, 97.5], "post_chroma_gain": 1.01, "flat_floor": 0.46}},
]

CLAHE_CANDIDATES: List[Dict[str, Any]] = [
    {"name": "clahe_s01", "params": {"clip_limit": 1.80, "tile_size": [6, 6], "gmin": 0.90, "gmax": 2.40, "gain_gamma": 0.98, "gf_radius": 10, "post_L_stretch": [2.0, 98.0], "post_chroma_gain": 1.02}},
    {"name": "clahe_s02", "params": {"clip_limit": 2.00, "tile_size": [5, 5], "gmin": 0.90, "gmax": 2.60, "gain_gamma": 1.00, "gf_radius": 9, "post_L_stretch": [1.5, 98.5], "post_chroma_gain": 1.03}},
    {"name": "clahe_s03", "params": {"clip_limit": 2.40, "tile_size": [6, 6], "gmin": 0.85, "gmax": 3.00, "gain_gamma": 1.05, "gf_radius": 7, "post_L_stretch": [1.0, 99.0], "post_chroma_gain": 1.05}},
    {"name": "clahe_s04", "params": {"clip_limit": 2.60, "tile_size": [5, 5], "gmin": 0.82, "gmax": 3.20, "gain_gamma": 1.06, "gf_radius": 7, "post_L_stretch": [1.0, 99.0], "post_chroma_gain": 1.05}},
    {"name": "clahe_s05", "params": {"clip_limit": 2.20, "tile_size": [7, 7], "gmin": 0.88, "gmax": 2.80, "gain_gamma": 1.08, "gf_radius": 8, "post_L_stretch": [0.8, 99.2], "post_chroma_gain": 1.04}},
    {"name": "clahe_s06", "params": {"clip_limit": 2.80, "tile_size": [4, 4], "gmin": 0.85, "gmax": 3.00, "gain_gamma": 1.03, "gf_radius": 6, "post_L_stretch": [1.0, 99.0], "post_chroma_gain": 1.05}},
    {"name": "clahe_s07", "params": {"clip_limit": 1.90, "tile_size": [8, 8], "gmin": 0.92, "gmax": 2.50, "gain_gamma": 0.95, "gf_radius": 12, "post_L_stretch": [2.0, 98.0], "post_chroma_gain": 1.02}},
    {"name": "clahe_s08", "params": {"clip_limit": 2.50, "tile_size": [6, 6], "gmin": 0.84, "gmax": 3.40, "gain_gamma": 1.10, "gf_radius": 7, "post_L_stretch": [0.8, 99.2], "post_chroma_gain": 1.06}},
]

FUSION_CANDIDATES: List[Dict[str, Any]] = [
    {"name": "fusion_s01", "params": {"rghs_low_boost": 1.50, "rgh_fg_bias": 0.45, "clahe_floor_mid": 0.10, "clahe_floor_high": 0.06, "boost_clahe": 0.12, "clahe_bg_bias": 0.35, "post_sigmoid_alpha": 0.25, "post_stretch": [1.0, 99.0]}},
    {"name": "fusion_s02", "params": {"rghs_low_boost": 1.80, "rgh_fg_bias": 0.60, "clahe_floor_mid": 0.10, "clahe_floor_high": 0.06, "boost_clahe": 0.10, "clahe_bg_bias": 0.30, "post_sigmoid_alpha": 0.22, "post_stretch": [1.0, 99.0]}},
    {"name": "fusion_s03", "params": {"rghs_low_boost": 1.50, "rgh_fg_bias": 0.40, "clahe_floor_mid": 0.16, "clahe_floor_high": 0.08, "boost_clahe": 0.18, "clahe_bg_bias": 0.45, "post_sigmoid_alpha": 0.28, "post_stretch": [1.0, 99.0]}},
    {"name": "fusion_s04", "params": {"rghs_low_boost": 1.40, "rgh_fg_bias": 0.38, "clahe_floor_mid": 0.12, "clahe_floor_high": 0.07, "boost_clahe": 0.14, "clahe_bg_bias": 0.38, "post_sigmoid_alpha": 0.20, "post_stretch": [1.5, 98.5]}},
    {"name": "fusion_s05", "params": {"rghs_low_boost": 1.60, "rgh_fg_bias": 0.48, "clahe_floor_mid": 0.12, "clahe_floor_high": 0.06, "boost_clahe": 0.14, "clahe_bg_bias": 0.36, "post_sigmoid_alpha": 0.32, "post_stretch": [0.8, 99.2]}},
    {"name": "fusion_s06", "params": {"rghs_low_boost": 1.60, "rgh_fg_bias": 0.50, "clahe_floor_mid": 0.14, "clahe_floor_high": 0.08, "boost_clahe": 0.16, "clahe_bg_bias": 0.42, "post_sigmoid_alpha": 0.18, "post_stretch": [1.0, 99.0]}},
    {"name": "fusion_s07", "params": {"rghs_low_boost": 1.40, "rgh_fg_bias": 0.40, "clahe_floor_mid": 0.18, "clahe_floor_high": 0.10, "boost_clahe": 0.20, "clahe_bg_bias": 0.50, "post_sigmoid_alpha": 0.24, "post_stretch": [1.0, 99.0]}},
    {"name": "fusion_s08", "params": {"rghs_low_boost": 1.70, "rgh_fg_bias": 0.55, "clahe_floor_mid": 0.15, "clahe_floor_high": 0.08, "boost_clahe": 0.17, "clahe_bg_bias": 0.44, "post_sigmoid_alpha": 0.24, "post_stretch": [0.8, 99.2]}},
    {"name": "fusion_s09", "params": {"rghs_low_boost": 1.50, "rgh_fg_bias": 0.43, "clahe_floor_mid": 0.11, "clahe_floor_high": 0.06, "boost_clahe": 0.10, "clahe_bg_bias": 0.33, "post_sigmoid_alpha": 0.16, "post_stretch": [1.5, 98.5]}},
    {"name": "fusion_s10", "params": {"rghs_low_boost": 1.60, "rgh_fg_bias": 0.50, "clahe_floor_mid": 0.13, "clahe_floor_high": 0.07, "boost_clahe": 0.15, "clahe_bg_bias": 0.40, "post_sigmoid_alpha": 0.30, "post_stretch": [0.5, 99.5]}},
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Direct full506 tuning with reused locked BPH/IMF1 outputs.")
    parser.add_argument("--stage", choices=["smoke", "rghs", "clahe", "fusion", "all"], default="all")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--base-config", default=str(BASE_CONFIG))
    parser.add_argument("--baseline-dir", default=str(BASELINE_DIR))
    parser.add_argument("--full-manifest", default=str(FULL_MANIFEST))
    parser.add_argument("--smoke-count", type=int, default=2)
    return parser.parse_args()


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    ensure_dir(path.parent)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def to_float01(img_bgr: np.ndarray) -> np.ndarray:
    return np.clip(img_bgr.astype(np.float32) / 255.0, 0.0, 1.0)


def to_uint8(img01: np.ndarray) -> np.ndarray:
    return np.clip(np.round(img01 * 255.0), 0, 255).astype(np.uint8)


def sanitize(name: str) -> str:
    return "".join(ch if ch.isalnum() or ch in "._-" else "_" for ch in name)


def selection_default(args: argparse.Namespace) -> Dict[str, Any]:
    return {
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "status": "initialized",
        "base_config": str(resolve_project_path(args.base_config)),
        "baseline_dir": str(resolve_project_path(args.baseline_dir)),
        "full_manifest": str(resolve_project_path(args.full_manifest)),
        "smoke_manifest": str((EXPERIMENT_DIR / "smoke_manifest.txt").resolve()),
        "rghs": {},
        "clahe": {},
        "fusion": {},
    }


def load_selection(args: argparse.Namespace) -> Dict[str, Any]:
    if SELECTION_PATH.exists():
        current = read_json(SELECTION_PATH)
        defaults = selection_default(args)
        for key, value in defaults.items():
            if key not in current or current[key] in ("", None):
                current[key] = value
        return current
    data = selection_default(args)
    write_json(SELECTION_PATH, data)
    return data


def save_selection(selection: Dict[str, Any]) -> None:
    selection["updated_at"] = now_iso()
    write_json(SELECTION_PATH, selection)


def update_status(stage: str, state: str, current_candidate: str | None = None, current_stem: str | None = None) -> None:
    write_json(
        STATUS_PATH,
        {
            "updated_at": now_iso(),
            "stage": stage,
            "state": state,
            "current_candidate": current_candidate,
            "current_stem": current_stem,
        },
    )


def stage_index(baseline_dir: Path, stage_name: str):
    return build_image_index(baseline_dir / "png" / stage_name, include_normalized_keys=True)


def final_refine(fused_uint8: np.ndarray, final_params: Dict[str, Any]) -> np.ndarray:
    params = dict(final_params or {})
    mode = params.pop("mode", "homomorphic")
    if mode == "homomorphic":
        return Gaussian_lvbo(fused_uint8, **params)
    if mode == "entropy":
        return entropy_boost_Lab(fused_uint8, **params)
    if mode == "homomorphic_entropy":
        entropy_params = params.pop("entropy", {})
        first = Gaussian_lvbo(fused_uint8, **params)
        return entropy_boost_Lab(first, **entropy_params)
    if mode == "none":
        return fused_uint8
    raise ValueError(f"Unknown final mode: {mode}")


def build_smoke_manifest(full_manifest: Path, smoke_count: int) -> Path:
    smoke_manifest = EXPERIMENT_DIR / "smoke_manifest.txt"
    stems = read_manifest(full_manifest)[:smoke_count]
    lines = [
        "# direct full506 smoke manifest",
        f"# created_at: {now_iso()}",
        f"# count: {len(stems)}",
        *stems,
    ]
    smoke_manifest.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return smoke_manifest


def save_stage_png(result_root: Path, stage_name: str, stem: str, img_uint8: np.ndarray) -> None:
    write_image(result_root / "png" / stage_name / f"{stem}_{stage_name}.png", img_uint8)


def run_rghs_candidate(stems: Sequence[str], baseline_dir: Path, base_config: Dict[str, Any], candidate: Dict[str, Any], resume: bool) -> Path:
    result_root = RESULTS_DIR / "rghs" / candidate["name"]
    bph_idx = stage_index(baseline_dir, "BPH")
    imf_idx = stage_index(baseline_dir, "IMF1Ray")
    clahe_idx = stage_index(baseline_dir, "CLAHE")
    for stem in stems:
        final_path = result_root / "png" / "Final" / f"{stem}_Final.png"
        if resume and final_path.exists():
            continue
        update_status("rghs", "running_candidate", current_candidate=candidate["name"], current_stem=stem)
        bph_bgr = to_float01(read_bgr(bph_idx.by_key[stem]))
        imf_bgr = to_float01(read_bgr(imf_idx.by_key[stem]))
        clahe_bgr = to_float01(read_bgr(clahe_idx.by_key[stem]))
        rghs_bgr = wb_safe_contrast(bph_bgr, **candidate["params"])
        fused_bgr = fuse_three_images_bgr(imf_bgr, rghs_bgr, clahe_bgr, **base_config.get("fusion", {}))
        fused_uint8 = to_uint8(fused_bgr)
        final_uint8 = final_refine(fused_uint8, base_config.get("final", {}))
        save_stage_png(result_root, "RGHS", stem, to_uint8(rghs_bgr))
        save_stage_png(result_root, "Fused", stem, fused_uint8)
        save_stage_png(result_root, "Final", stem, final_uint8)
    return result_root


def run_clahe_candidate(stems: Sequence[str], baseline_dir: Path, base_config: Dict[str, Any], rghs_winner_dir: Path, candidate: Dict[str, Any], resume: bool) -> Path:
    result_root = RESULTS_DIR / "clahe" / candidate["name"]
    bph_idx = stage_index(baseline_dir, "BPH")
    imf_idx = stage_index(baseline_dir, "IMF1Ray")
    rghs_idx = build_image_index(rghs_winner_dir / "png" / "RGHS", include_normalized_keys=True)
    for stem in stems:
        final_path = result_root / "png" / "Final" / f"{stem}_Final.png"
        if resume and final_path.exists():
            continue
        update_status("clahe", "running_candidate", current_candidate=candidate["name"], current_stem=stem)
        bph_bgr = to_float01(read_bgr(bph_idx.by_key[stem]))
        imf_bgr = to_float01(read_bgr(imf_idx.by_key[stem]))
        rghs_bgr = to_float01(read_bgr(rghs_idx.by_key[stem]))
        clahe_bgr = clahe_3ch_wb_safe(bph_bgr, **candidate["params"])
        fused_bgr = fuse_three_images_bgr(imf_bgr, rghs_bgr, clahe_bgr, **base_config.get("fusion", {}))
        fused_uint8 = to_uint8(fused_bgr)
        final_uint8 = final_refine(fused_uint8, base_config.get("final", {}))
        save_stage_png(result_root, "CLAHE", stem, to_uint8(clahe_bgr))
        save_stage_png(result_root, "Fused", stem, fused_uint8)
        save_stage_png(result_root, "Final", stem, final_uint8)
    return result_root


def run_fusion_candidate(stems: Sequence[str], baseline_dir: Path, base_config: Dict[str, Any], rghs_winner_dir: Path, clahe_winner_dir: Path, candidate: Dict[str, Any], resume: bool) -> Path:
    result_root = RESULTS_DIR / "fusion" / candidate["name"]
    imf_idx = stage_index(baseline_dir, "IMF1Ray")
    rghs_idx = build_image_index(rghs_winner_dir / "png" / "RGHS", include_normalized_keys=True)
    clahe_idx = build_image_index(clahe_winner_dir / "png" / "CLAHE", include_normalized_keys=True)
    for stem in stems:
        final_path = result_root / "png" / "Final" / f"{stem}_Final.png"
        if resume and final_path.exists():
            continue
        update_status("fusion", "running_candidate", current_candidate=candidate["name"], current_stem=stem)
        imf_bgr = to_float01(read_bgr(imf_idx.by_key[stem]))
        rghs_bgr = to_float01(read_bgr(rghs_idx.by_key[stem]))
        clahe_bgr = to_float01(read_bgr(clahe_idx.by_key[stem]))
        fused_bgr = fuse_three_images_bgr(imf_bgr, rghs_bgr, clahe_bgr, **candidate["params"])
        fused_uint8 = to_uint8(fused_bgr)
        final_uint8 = final_refine(fused_uint8, base_config.get("final", {}))
        save_stage_png(result_root, "Fused", stem, fused_uint8)
        save_stage_png(result_root, "Final", stem, final_uint8)
    return result_root


def run_eval(methods: Sequence[Tuple[str, Path]], manifest_path: Path, output_dir: Path, resume: bool) -> None:
    import subprocess

    ensure_dir(output_dir)
    summary_path = output_dir / "summary.json"
    if resume and summary_path.exists():
        return
    cmd = [
        sys.executable,
        str(PROJECT_ROOT / "metrics" / "evaluate_protocol_v2.py"),
        "--quiet",
        "--manifest",
        str(manifest_path),
        "--output-dir",
        str(output_dir),
    ]
    for method_name, method_dir in methods:
        cmd += ["--method", f"{method_name}={method_dir}"]
    stdout_path = LOGS_DIR / f"{sanitize(output_dir.name)}_stdout.log"
    stderr_path = LOGS_DIR / f"{sanitize(output_dir.name)}_stderr.log"
    with stdout_path.open("w", encoding="utf-8") as out, stderr_path.open("w", encoding="utf-8") as err:
        subprocess.run(cmd, cwd=PROJECT_ROOT, check=True, stdout=out, stderr=err)


def zscores(values: Sequence[float]) -> List[float]:
    if not values:
        return []
    mean = sum(values) / len(values)
    variance = sum((value - mean) ** 2 for value in values) / len(values)
    std = math.sqrt(variance)
    if std <= 1e-12:
        return [0.0 for _ in values]
    return [(value - mean) / std for value in values]


def compare_rank(left: Dict[str, Any], right: Dict[str, Any]) -> int:
    if abs(left["delta_ms_ssim"] - right["delta_ms_ssim"]) > 0.001:
        return -1 if left["delta_ms_ssim"] > right["delta_ms_ssim"] else 1
    if abs(left["delta_psnr"] - right["delta_psnr"]) > 0.03:
        return -1 if left["delta_psnr"] > right["delta_psnr"] else 1
    if abs(left["visual_score"] - right["visual_score"]) > 1e-12:
        return -1 if left["visual_score"] > right["visual_score"] else 1
    if left["method"].lower() == right["method"].lower():
        return 0
    return -1 if left["method"].lower() < right["method"].lower() else 1


def rank_summary(summary_path: Path, baseline_method: str) -> List[Dict[str, Any]]:
    summary = read_json(summary_path)
    methods = summary["methods"]
    baseline = methods[baseline_method]["metrics"]
    rows: List[Dict[str, Any]] = []
    for method_name, method_summary in methods.items():
        if method_name == baseline_method:
            continue
        metrics = method_summary["metrics"]
        row = {
            "method": method_name,
            "MS_SSIM": float(metrics["MS_SSIM"]["mean"]),
            "PSNR": float(metrics["PSNR"]["mean"]),
            "UCIQE": float(metrics["UCIQE"]["mean"]),
            "UIQM": float(metrics["UIQM"]["mean"]),
        }
        row["delta_ms_ssim"] = row["MS_SSIM"] - float(baseline["MS_SSIM"]["mean"])
        row["delta_psnr"] = row["PSNR"] - float(baseline["PSNR"]["mean"])
        row["delta_uciqe"] = row["UCIQE"] - float(baseline["UCIQE"]["mean"])
        row["delta_uiqm"] = row["UIQM"] - float(baseline["UIQM"]["mean"])
        rows.append(row)
    uciqe_z = zscores([row["delta_uciqe"] for row in rows])
    uiqm_z = zscores([row["delta_uiqm"] for row in rows])
    for idx, row in enumerate(rows):
        row["z_uciqe"] = uciqe_z[idx]
        row["z_uiqm"] = uiqm_z[idx]
        row["visual_score"] = 0.5 * row["z_uciqe"] + 0.5 * row["z_uiqm"]
        row["gate_pass"] = row["delta_ms_ssim"] >= 0 and row["delta_psnr"] >= 0
    ranked = sorted(rows, key=cmp_to_key(compare_rank))
    for idx, row in enumerate(ranked, start=1):
        row["rank"] = idx
    return ranked


def write_rank(path_base: Path, rows: Sequence[Dict[str, Any]]) -> None:
    write_json(path_base.with_suffix(".json"), list(rows))
    if not rows:
        return
    with path_base.with_suffix(".csv").open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def stage_config(base_config: Dict[str, Any], stage_name: str, winner_params: Dict[str, Any] | None = None, candidate_params: Dict[str, Any] | None = None) -> Dict[str, Any]:
    config = json.loads(json.dumps(base_config))
    if winner_params:
        config.update(winner_params)
    if candidate_params:
        config.update(candidate_params)
    return config


def choose_winner(official_rows: Sequence[Dict[str, Any]], final_rows: Sequence[Dict[str, Any]] | None = None) -> Dict[str, Any]:
    final_map = {row["method"]: row for row in (final_rows or [])}
    for row in official_rows:
        final_row = final_map.get(row["method"])
        if final_row is None or final_row["gate_pass"]:
            return {"official": row, "final_backstop": final_row}
    top = official_rows[0]
    return {"official": top, "final_backstop": final_map.get(top["method"])}


def render_analysis(selection: Dict[str, Any]) -> None:
    lines = [
        "# H2 full506 直跑调参",
        "",
        f"- 创建时间：`{selection.get('created_at', '')}`",
        f"- 最近更新：`{selection.get('updated_at', '')}`",
        f"- 总状态：`{selection.get('status', '')}`",
        f"- 基线配置：`{selection.get('base_config', '')}`",
        f"- 基线结果：`{selection.get('baseline_dir', '')}`",
        f"- full506 manifest：`{selection.get('full_manifest', '')}`",
        f"- smoke manifest：`{selection.get('smoke_manifest', '')}`",
        "",
    ]
    for stage_name in ("rghs", "clahe", "fusion"):
        info = selection.get(stage_name, {})
        lines += [
            f"## {stage_name.upper()}",
            "",
            f"- 状态：`{info.get('status', 'pending')}`",
            f"- 排序：`{info.get('official_score_json', '')}`",
            f"- Final 回退检查：`{info.get('final_score_json', '')}`",
        ]
        winner = info.get("winner", {})
        if winner:
            lines += [
                f"- winner：`{winner.get('name', '')}`",
                f"- 参数文件：`{winner.get('params_json', '')}`",
                f"- 官方胜出：ΔMS-SSIM=`{winner.get('official', {}).get('delta_ms_ssim', '')}`，ΔPSNR=`{winner.get('official', {}).get('delta_psnr', '')}`，ΔUCIQE=`{winner.get('official', {}).get('delta_uciqe', '')}`，ΔUIQM=`{winner.get('official', {}).get('delta_uiqm', '')}`",
            ]
            if winner.get("final_backstop"):
                lines.append(
                    f"- Final 回退：ΔMS-SSIM=`{winner['final_backstop'].get('delta_ms_ssim', '')}`，ΔPSNR=`{winner['final_backstop'].get('delta_psnr', '')}`，ΔUCIQE=`{winner['final_backstop'].get('delta_uciqe', '')}`，ΔUIQM=`{winner['final_backstop'].get('delta_uiqm', '')}`"
                )
        lines.append("")
    ANALYSIS_PATH.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def smoke_check(stems: Sequence[str], baseline_dir: Path, base_config: Dict[str, Any], rghs_candidate: Dict[str, Any], clahe_candidate: Dict[str, Any], fusion_candidate: Dict[str, Any], resume: bool) -> None:
    smoke_root = RESULTS_DIR / "smoke"
    run_rghs_candidate(stems, baseline_dir, base_config, rghs_candidate, resume)
    rghs_dir = RESULTS_DIR / "rghs" / rghs_candidate["name"]
    run_clahe_candidate(stems, baseline_dir, base_config, rghs_dir, clahe_candidate, resume)
    clahe_dir = RESULTS_DIR / "clahe" / clahe_candidate["name"]
    run_fusion_candidate(stems, baseline_dir, base_config, rghs_dir, clahe_dir, fusion_candidate, resume)
    write_json(smoke_root / "smoke_completed.json", {"completed_at": now_iso(), "stems": list(stems)})


def run_stage_rghs(stems: Sequence[str], baseline_dir: Path, base_config: Dict[str, Any], selection: Dict[str, Any], resume: bool) -> Dict[str, Any]:
    methods = [("baseline", baseline_dir / "png" / "RGHS")]
    final_methods = [("baseline", baseline_dir / "png" / "Final")]
    records: Dict[str, Dict[str, Any]] = {}
    for candidate in RGHS_CANDIDATES:
        result_root = run_rghs_candidate(stems, baseline_dir, base_config, candidate, resume)
        methods.append((candidate["name"], result_root / "png" / "RGHS"))
        final_methods.append((candidate["name"], result_root / "png" / "Final"))
        params_json = CONFIGS_DIR / "rghs" / f"{candidate['name']}.json"
        write_json(params_json, stage_config(base_config, "rghs", candidate_params={"rghs": candidate["params"]}))
        records[candidate["name"]] = {"result_root": str(result_root.resolve()), "params_json": str(params_json.resolve()), "params": candidate["params"]}
    official_dir = SCORES_DIR / "rghs_official"
    final_dir = SCORES_DIR / "rghs_final_backstop"
    run_eval(methods, resolve_project_path(selection["full_manifest"]), official_dir, resume)
    run_eval(final_methods, resolve_project_path(selection["full_manifest"]), final_dir, resume)
    official_rows = rank_summary(official_dir / "summary.json", "baseline")
    final_rows = rank_summary(final_dir / "summary.json", "baseline")
    write_rank(official_dir / "ranked", official_rows)
    write_rank(final_dir / "ranked", final_rows)
    winner = choose_winner(official_rows, final_rows)
    selected = winner["official"]["method"]
    return {
        "status": "completed",
        "official_score_json": str((official_dir / "ranked.json").resolve()),
        "final_score_json": str((final_dir / "ranked.json").resolve()),
        "winner": {
            "name": selected,
            "params_json": records[selected]["params_json"],
            "result_root": records[selected]["result_root"],
            "params": records[selected]["params"],
            "official": winner["official"],
            "final_backstop": winner["final_backstop"],
        },
    }


def run_stage_clahe(stems: Sequence[str], baseline_dir: Path, base_config: Dict[str, Any], selection: Dict[str, Any], resume: bool) -> Dict[str, Any]:
    rghs_dir = Path(selection["rghs"]["winner"]["result_root"])
    methods = [("baseline", baseline_dir / "png" / "CLAHE")]
    final_methods = [("baseline", baseline_dir / "png" / "Final")]
    records: Dict[str, Dict[str, Any]] = {}
    for candidate in CLAHE_CANDIDATES:
        result_root = run_clahe_candidate(stems, baseline_dir, base_config, rghs_dir, candidate, resume)
        methods.append((candidate["name"], result_root / "png" / "CLAHE"))
        final_methods.append((candidate["name"], result_root / "png" / "Final"))
        params_json = CONFIGS_DIR / "clahe" / f"{candidate['name']}.json"
        write_json(
            params_json,
            stage_config(base_config, "clahe", winner_params={"rghs": selection["rghs"]["winner"]["params"]}, candidate_params={"clahe": candidate["params"]}),
        )
        records[candidate["name"]] = {"result_root": str(result_root.resolve()), "params_json": str(params_json.resolve()), "params": candidate["params"]}
    official_dir = SCORES_DIR / "clahe_official"
    final_dir = SCORES_DIR / "clahe_final_backstop"
    run_eval(methods, resolve_project_path(selection["full_manifest"]), official_dir, resume)
    run_eval(final_methods, resolve_project_path(selection["full_manifest"]), final_dir, resume)
    official_rows = rank_summary(official_dir / "summary.json", "baseline")
    final_rows = rank_summary(final_dir / "summary.json", "baseline")
    write_rank(official_dir / "ranked", official_rows)
    write_rank(final_dir / "ranked", final_rows)
    winner = choose_winner(official_rows, final_rows)
    selected = winner["official"]["method"]
    return {
        "status": "completed",
        "official_score_json": str((official_dir / "ranked.json").resolve()),
        "final_score_json": str((final_dir / "ranked.json").resolve()),
        "winner": {
            "name": selected,
            "params_json": records[selected]["params_json"],
            "result_root": records[selected]["result_root"],
            "params": records[selected]["params"],
            "official": winner["official"],
            "final_backstop": winner["final_backstop"],
        },
    }


def run_stage_fusion(stems: Sequence[str], baseline_dir: Path, base_config: Dict[str, Any], selection: Dict[str, Any], resume: bool) -> Dict[str, Any]:
    rghs_dir = Path(selection["rghs"]["winner"]["result_root"])
    clahe_dir = Path(selection["clahe"]["winner"]["result_root"])
    methods = [("baseline", baseline_dir / "png" / "Final")]
    records: Dict[str, Dict[str, Any]] = {}
    for candidate in FUSION_CANDIDATES:
        result_root = run_fusion_candidate(stems, baseline_dir, base_config, rghs_dir, clahe_dir, candidate, resume)
        methods.append((candidate["name"], result_root / "png" / "Final"))
        params_json = CONFIGS_DIR / "fusion" / f"{candidate['name']}.json"
        write_json(
            params_json,
            stage_config(
                base_config,
                "fusion",
                winner_params={"rghs": selection["rghs"]["winner"]["params"], "clahe": selection["clahe"]["winner"]["params"]},
                candidate_params={"fusion": candidate["params"]},
            ),
        )
        records[candidate["name"]] = {"result_root": str(result_root.resolve()), "params_json": str(params_json.resolve()), "params": candidate["params"]}
    official_dir = SCORES_DIR / "fusion_final"
    run_eval(methods, resolve_project_path(selection["full_manifest"]), official_dir, resume)
    official_rows = rank_summary(official_dir / "summary.json", "baseline")
    write_rank(official_dir / "ranked", official_rows)
    winner = official_rows[0]
    selected = winner["method"]
    return {
        "status": "completed",
        "official_score_json": str((official_dir / "ranked.json").resolve()),
        "final_score_json": str((official_dir / "ranked.json").resolve()),
        "winner": {
            "name": selected,
            "params_json": records[selected]["params_json"],
            "result_root": records[selected]["result_root"],
            "params": records[selected]["params"],
            "official": winner,
            "final_backstop": winner,
        },
    }


def main() -> int:
    args = parse_args()
    ensure_dir(CONFIGS_DIR / "rghs")
    ensure_dir(CONFIGS_DIR / "clahe")
    ensure_dir(CONFIGS_DIR / "fusion")
    ensure_dir(LOGS_DIR)
    ensure_dir(RESULTS_DIR)
    ensure_dir(SCORES_DIR)

    selection = load_selection(args)
    baseline_dir = resolve_project_path(args.baseline_dir)
    base_config = read_json(resolve_project_path(args.base_config))
    full_manifest = resolve_project_path(args.full_manifest)
    stems = read_manifest(full_manifest)

    smoke_manifest = build_smoke_manifest(full_manifest, int(args.smoke_count))
    selection["smoke_manifest"] = str(smoke_manifest.resolve())
    save_selection(selection)

    if args.stage in {"smoke", "all"}:
        smoke_stems = read_manifest(smoke_manifest)
        smoke_check(smoke_stems, baseline_dir, base_config, RGHS_CANDIDATES[0], CLAHE_CANDIDATES[0], FUSION_CANDIDATES[0], args.resume)
        if args.stage == "smoke":
            selection["status"] = "smoke_completed"
            save_selection(selection)
            render_analysis(selection)
            return 0

    if args.stage in {"rghs", "all"}:
        selection["rghs"] = run_stage_rghs(stems, baseline_dir, base_config, selection, args.resume)
        selection["status"] = "rghs_completed"
        save_selection(selection)
        render_analysis(selection)
        if args.stage == "rghs":
            return 0

    if args.stage in {"clahe", "all"}:
        selection["clahe"] = run_stage_clahe(stems, baseline_dir, base_config, selection, args.resume)
        selection["status"] = "clahe_completed"
        save_selection(selection)
        render_analysis(selection)
        if args.stage == "clahe":
            return 0

    if args.stage in {"fusion", "all"}:
        selection["fusion"] = run_stage_fusion(stems, baseline_dir, base_config, selection, args.resume)
        selection["status"] = "completed"
        save_selection(selection)
        render_analysis(selection)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
