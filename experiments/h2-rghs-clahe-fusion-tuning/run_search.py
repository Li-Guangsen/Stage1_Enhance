from __future__ import annotations

import argparse
import csv
import json
import math
import subprocess
import sys
from copy import deepcopy
from datetime import datetime
from functools import cmp_to_key
from pathlib import Path
from typing import Any, Dict, List, Sequence, Tuple


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
METRICS_DIR = PROJECT_ROOT / "metrics"
if str(METRICS_DIR) not in sys.path:
    sys.path.insert(0, str(METRICS_DIR))

from metrics.protocol_common import build_image_index, read_manifest, resolve_project_path, write_lines


EXPERIMENT_DIR = Path(__file__).resolve().parent
CONFIGS_DIR = EXPERIMENT_DIR / "configs"
LOGS_DIR = EXPERIMENT_DIR / "logs"
MANIFESTS_DIR = EXPERIMENT_DIR / "manifests"
RESULTS_DIR = EXPERIMENT_DIR / "results"
SCORES_DIR = EXPERIMENT_DIR / "scores"

ANALYSIS_PATH = EXPERIMENT_DIR / "analysis.md"
SELECTION_PATH = EXPERIMENT_DIR / "selection.json"
STATUS_PATH = EXPERIMENT_DIR / "status.json"
WINNER_RGHS_PATH = EXPERIMENT_DIR / "winner_rghs.json"
WINNER_CLAHE_PATH = EXPERIMENT_DIR / "winner_clahe.json"
WINNER_FULL506_PATH = EXPERIMENT_DIR / "winner_full506.json"

DEFAULT_BASE_CONFIG = PROJECT_ROOT / "experiments" / "optimization_v1" / "configs" / "locked_full506_mainline.json"
DEFAULT_PILOT_MANIFEST = PROJECT_ROOT / "data" / "eval_subset_pilot92_v1.txt"
DEFAULT_FULL_MANIFEST = PROJECT_ROOT / "metrics" / "outputs" / "evaluate_protocol_v2" / "full506_c25" / "complete_case_manifest.txt"
DEFAULT_FULL506_BASELINE_DIR = (
    PROJECT_ROOT
    / "experiments"
    / "h1-graypixel-bph-ablation"
    / "outputs"
    / "full506"
    / "runs"
    / "full506_locked_mainline"
)
DEFAULT_ORIGINAL_DIR = PROJECT_ROOT / "data" / "inputImg" / "Original"

SMOKE_COUNT = 12
SMOKE_KEEP = {"rghs": 3, "clahe": 3, "fusion": 4}
PILOT_LIMIT = {"rghs": 5, "clahe": 5, "fusion": 6}
FULL506_LIMIT = 2

SMOKE_GATE = {"ms_ssim": 0.0, "psnr": -0.02, "inclusive": True}
SOFT_GATE = {"ms_ssim": 0.0, "psnr": -0.02, "inclusive": True}
FULL506_GATE = {"ms_ssim": 0.0, "psnr": 0.0, "inclusive": False}

PRIMARY_METRICS = ("MS_SSIM", "PSNR", "UCIQE", "UIQM")


RGHS_COARSE: List[Dict[str, Any]] = [
    {"name": "rghs_s01", "params": {"strength": 0.50, "clip_limit": 1.40, "brightness_boost": 1.04, "chroma_preserve": 0.84, "post_L_stretch": [2.0, 98.0], "post_chroma_gain": 1.02, "flat_floor": 0.45}},
    {"name": "rghs_s02", "params": {"strength": 0.55, "clip_limit": 1.50, "brightness_boost": 1.08, "chroma_preserve": 0.83, "post_L_stretch": [1.5, 98.5], "post_chroma_gain": 1.03, "flat_floor": 0.42}},
    {"name": "rghs_s03", "params": {"strength": 0.60, "clip_limit": 1.60, "brightness_boost": 1.06, "chroma_preserve": 0.82, "post_L_stretch": [2.0, 98.0], "post_chroma_gain": 1.03, "flat_floor": 0.40}},
    {"name": "rghs_s04", "params": {"strength": 0.68, "clip_limit": 1.80, "brightness_boost": 1.05, "chroma_preserve": 0.80, "post_L_stretch": [1.8, 98.2], "post_chroma_gain": 1.04, "flat_floor": 0.36}},
    {"name": "rghs_s05", "params": {"strength": 0.70, "clip_limit": 2.00, "brightness_boost": 1.04, "chroma_preserve": 0.84, "post_L_stretch": [2.0, 97.5], "post_chroma_gain": 1.03, "flat_floor": 0.35}},
    {"name": "rghs_s06", "params": {"strength": 0.58, "clip_limit": 1.70, "brightness_boost": 1.07, "chroma_preserve": 0.83, "post_L_stretch": [1.0, 99.0], "post_chroma_gain": 1.02, "flat_floor": 0.43}},
    {"name": "rghs_s07", "params": {"strength": 0.65, "clip_limit": 1.90, "brightness_boost": 1.08, "chroma_preserve": 0.80, "post_L_stretch": [1.0, 99.0], "post_chroma_gain": 1.04, "flat_floor": 0.38}},
    {"name": "rghs_s08", "params": {"strength": 0.62, "clip_limit": 1.50, "brightness_boost": 1.05, "chroma_preserve": 0.86, "post_L_stretch": [2.5, 97.5], "post_chroma_gain": 1.01, "flat_floor": 0.46}},
]

CLAHE_COARSE: List[Dict[str, Any]] = [
    {"name": "clahe_s01", "params": {"clip_limit": 1.80, "tile_size": [6, 6], "gmin": 0.90, "gmax": 2.40, "gain_gamma": 0.98, "gf_radius": 10, "post_L_stretch": [2.0, 98.0], "post_chroma_gain": 1.02}},
    {"name": "clahe_s02", "params": {"clip_limit": 2.00, "tile_size": [5, 5], "gmin": 0.90, "gmax": 2.60, "gain_gamma": 1.00, "gf_radius": 9, "post_L_stretch": [1.5, 98.5], "post_chroma_gain": 1.03}},
    {"name": "clahe_s03", "params": {"clip_limit": 2.40, "tile_size": [6, 6], "gmin": 0.85, "gmax": 3.00, "gain_gamma": 1.05, "gf_radius": 7, "post_L_stretch": [1.0, 99.0], "post_chroma_gain": 1.05}},
    {"name": "clahe_s04", "params": {"clip_limit": 2.60, "tile_size": [5, 5], "gmin": 0.82, "gmax": 3.20, "gain_gamma": 1.06, "gf_radius": 7, "post_L_stretch": [1.0, 99.0], "post_chroma_gain": 1.05}},
    {"name": "clahe_s05", "params": {"clip_limit": 2.20, "tile_size": [7, 7], "gmin": 0.88, "gmax": 2.80, "gain_gamma": 1.08, "gf_radius": 8, "post_L_stretch": [0.8, 99.2], "post_chroma_gain": 1.04}},
    {"name": "clahe_s06", "params": {"clip_limit": 2.80, "tile_size": [4, 4], "gmin": 0.85, "gmax": 3.00, "gain_gamma": 1.03, "gf_radius": 6, "post_L_stretch": [1.0, 99.0], "post_chroma_gain": 1.05}},
    {"name": "clahe_s07", "params": {"clip_limit": 1.90, "tile_size": [8, 8], "gmin": 0.92, "gmax": 2.50, "gain_gamma": 0.95, "gf_radius": 12, "post_L_stretch": [2.0, 98.0], "post_chroma_gain": 1.02}},
    {"name": "clahe_s08", "params": {"clip_limit": 2.50, "tile_size": [6, 6], "gmin": 0.84, "gmax": 3.40, "gain_gamma": 1.10, "gf_radius": 7, "post_L_stretch": [0.8, 99.2], "post_chroma_gain": 1.06}},
]

FUSION_COARSE: List[Dict[str, Any]] = [
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

STAGE_SPECS: Dict[str, Dict[str, Any]] = {
    "rghs": {"target_stage": "RGHS", "backstop_stage": "Final", "coarse_candidates": RGHS_COARSE, "smoke_keep": SMOKE_KEEP["rghs"], "pilot_limit": PILOT_LIMIT["rghs"], "winner_path": WINNER_RGHS_PATH},
    "clahe": {"target_stage": "CLAHE", "backstop_stage": "Final", "coarse_candidates": CLAHE_COARSE, "smoke_keep": SMOKE_KEEP["clahe"], "pilot_limit": PILOT_LIMIT["clahe"], "winner_path": WINNER_CLAHE_PATH},
    "fusion": {"target_stage": "Final", "backstop_stage": None, "coarse_candidates": FUSION_COARSE, "smoke_keep": SMOKE_KEEP["fusion"], "pilot_limit": PILOT_LIMIT["fusion"], "winner_path": None},
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sequential RGHS / CLAHE / fusion tuning for long-running H2.")
    parser.add_argument("--stage", choices=["setup", "rghs", "clahe", "fusion", "all"], default="all")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--stop-after", choices=["none", "smoke", "pilot", "full506"], default="none")
    parser.add_argument("--base-config", default=str(DEFAULT_BASE_CONFIG))
    parser.add_argument("--smoke-manifest", default=None)
    parser.add_argument("--pilot-manifest", default=str(DEFAULT_PILOT_MANIFEST))
    parser.add_argument("--full-manifest", default=str(DEFAULT_FULL_MANIFEST))
    parser.add_argument("--original-dir", default=str(DEFAULT_ORIGINAL_DIR))
    parser.add_argument("--full506-baseline-dir", default=str(DEFAULT_FULL506_BASELINE_DIR))
    parser.add_argument("--smoke-count", type=int, default=SMOKE_COUNT)
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


def deep_copy_jsonable(data: Any) -> Any:
    return json.loads(json.dumps(data))


def sanitize_name(name: str) -> str:
    return "".join(ch if ch.isalnum() or ch in "._-" else "_" for ch in name)


def selection_default(args: argparse.Namespace) -> Dict[str, Any]:
    return {
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "status": "initialized",
        "base_config": str(resolve_project_path(args.base_config)),
        "pilot_manifest": str(resolve_project_path(args.pilot_manifest)),
        "smoke_manifest": str((MANIFESTS_DIR / "smoke12.txt").resolve()),
        "full_manifest": str(resolve_project_path(args.full_manifest)),
        "full506_baseline_dir": str(resolve_project_path(args.full506_baseline_dir)),
        "setup": {},
        "rghs": {},
        "clahe": {},
        "fusion": {},
        "full506": {},
    }


def load_selection(args: argparse.Namespace) -> Dict[str, Any]:
    if SELECTION_PATH.exists():
        current = read_json(SELECTION_PATH)
        defaults = selection_default(args)
        for key, value in defaults.items():
            if key not in current or current[key] in ("", None, {}):
                current[key] = value
        return current
    data = selection_default(args)
    write_json(SELECTION_PATH, data)
    return data


def save_selection(selection: Dict[str, Any]) -> None:
    selection["updated_at"] = now_iso()
    write_json(SELECTION_PATH, selection)


def update_status(stage: str, state: str, current_candidate: str | None = None, current_chunk: str | None = None, last_eval_output: str | None = None) -> None:
    payload = {
        "updated_at": now_iso(),
        "stage": stage,
        "state": state,
        "current_candidate": current_candidate,
        "current_chunk": current_chunk,
        "last_eval_output": last_eval_output,
    }
    write_json(STATUS_PATH, payload)


def run_command(cmd: Sequence[str], stdout_path: Path, stderr_path: Path) -> None:
    ensure_dir(stdout_path.parent)
    ensure_dir(stderr_path.parent)
    print(f"[RUN] {' '.join(str(x) for x in cmd)}")
    with stdout_path.open("w", encoding="utf-8") as out, stderr_path.open("w", encoding="utf-8") as err:
        subprocess.run(cmd, cwd=PROJECT_ROOT, check=True, stdout=out, stderr=err)


def has_manifest_outputs(stage_dir: Path, manifest_path: Path) -> bool:
    if not stage_dir.is_dir():
        return False
    stems = read_manifest(manifest_path)
    if not stems:
        return False
    index = build_image_index(stage_dir, include_normalized_keys=True)
    return all(stem in index.by_key for stem in stems)


def run_pipeline(manifest_path: Path, output_dir: Path, params_json: Path, log_tag: str, resume: bool) -> None:
    final_dir = output_dir / "png" / "Final"
    if resume and has_manifest_outputs(final_dir, manifest_path):
        print(f"[SKIP] pipeline outputs already complete for {log_tag}")
        return
    cmd = [
        sys.executable,
        str(PROJECT_ROOT / "main.py"),
        "--input-dir",
        str(DEFAULT_ORIGINAL_DIR),
        "--output-dir",
        str(output_dir),
        "--manifest",
        str(manifest_path),
        "--params-json",
        str(params_json),
        "--skip-existing",
    ]
    run_command(
        cmd,
        LOGS_DIR / f"{sanitize_name(log_tag)}_stdout.log",
        LOGS_DIR / f"{sanitize_name(log_tag)}_stderr.log",
    )


def run_eval_methods(methods: Sequence[Tuple[str, Path]], manifest_path: Path, output_dir: Path, log_tag: str, resume: bool) -> None:
    summary_path = output_dir / "summary.json"
    if resume and summary_path.exists():
        print(f"[SKIP] evaluation already exists for {log_tag}")
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
    run_command(
        cmd,
        LOGS_DIR / f"{sanitize_name(log_tag)}_stdout.log",
        LOGS_DIR / f"{sanitize_name(log_tag)}_stderr.log",
    )


def run_eval_single(result_dir: Path, method_name: str, manifest_path: Path, output_dir: Path, log_tag: str, resume: bool) -> None:
    summary_path = output_dir / "summary.json"
    if resume and summary_path.exists():
        print(f"[SKIP] single-method evaluation already exists for {log_tag}")
        return
    cmd = [
        sys.executable,
        str(PROJECT_ROOT / "metrics" / "evaluate_protocol_v2.py"),
        "--quiet",
        "--manifest",
        str(manifest_path),
        "--output-dir",
        str(output_dir),
        "--result-dir",
        str(result_dir),
        "--method-name",
        method_name,
    ]
    run_command(
        cmd,
        LOGS_DIR / f"{sanitize_name(log_tag)}_stdout.log",
        LOGS_DIR / f"{sanitize_name(log_tag)}_stderr.log",
    )


def read_csv_rows(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def zscores(values: Sequence[float]) -> List[float]:
    if not values:
        return []
    mean = sum(values) / len(values)
    variance = sum((value - mean) ** 2 for value in values) / len(values)
    std = math.sqrt(variance)
    if std <= 1e-12:
        return [0.0 for _ in values]
    return [(value - mean) / std for value in values]


def select_smoke12(per_image_metrics_csv: Path, output_manifest: Path, count: int) -> List[str]:
    rows = read_csv_rows(per_image_metrics_csv)
    if not rows:
        raise RuntimeError(f"Missing baseline per-image metrics: {per_image_metrics_csv}")
    metrics = {metric: [float(row[metric]) for row in rows] for metric in PRIMARY_METRICS}
    zmap = {metric: zscores(values) for metric, values in metrics.items()}
    scored: List[Tuple[float, str]] = []
    for idx, row in enumerate(rows):
        score = (
            zmap["MS_SSIM"][idx]
            + zmap["PSNR"][idx]
            + zmap["UCIQE"][idx]
            + zmap["UIQM"][idx]
        )
        scored.append((score, row["stem"]))
    scored.sort(key=lambda item: (item[0], item[1].lower()))
    selected = [stem for _, stem in scored[:count]]
    lines = [
        "# smoke12 manifest derived from pilot92 baseline",
        f"# created_at: {now_iso()}",
        f"# count: {len(selected)}",
        *selected,
    ]
    write_lines(output_manifest, lines)
    return selected


def split_manifest(manifest_path: Path, chunk_prefix: str, num_chunks: int = 4) -> List[Path]:
    stems = read_manifest(manifest_path)
    if not stems:
        raise RuntimeError(f"Cannot split empty manifest: {manifest_path}")
    chunks: List[List[str]] = [[] for _ in range(num_chunks)]
    for idx, stem in enumerate(stems):
        chunks[idx % num_chunks].append(stem)
    chunk_paths: List[Path] = []
    for idx, chunk in enumerate(chunks, start=1):
        path = MANIFESTS_DIR / f"{chunk_prefix}_chunk{idx}.txt"
        lines = [
            f"# {chunk_prefix} chunk {idx}",
            f"# created_at: {now_iso()}",
            f"# count: {len(chunk)}",
            *chunk,
        ]
        write_lines(path, lines)
        chunk_paths.append(path)
    return chunk_paths


def serialize_override(params: Dict[str, Any]) -> str:
    return json.dumps(params, ensure_ascii=False, sort_keys=True)


def blend_value(value_a: Any, value_b: Any, weight_a: float) -> Any:
    if isinstance(value_a, (int, float)) and isinstance(value_b, (int, float)):
        mixed = weight_a * float(value_a) + (1.0 - weight_a) * float(value_b)
        return round(mixed, 6)
    if isinstance(value_a, list) and isinstance(value_b, list) and len(value_a) == len(value_b):
        return [blend_value(left, right, weight_a) for left, right in zip(value_a, value_b)]
    return deep_copy_jsonable(value_a)


def blend_param_dict(a: Dict[str, Any], b: Dict[str, Any], weight_a: float) -> Dict[str, Any]:
    mixed: Dict[str, Any] = {}
    for key in sorted(set(a) | set(b)):
        if key in a and key in b:
            mixed[key] = blend_value(a[key], b[key], weight_a)
        elif key in a:
            mixed[key] = deep_copy_jsonable(a[key])
        else:
            mixed[key] = deep_copy_jsonable(b[key])
    return mixed


def stage_override(stage_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
    return {stage_name: deep_copy_jsonable(params)}


def refinement_candidates(stage_name: str, shortlist: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    if not shortlist:
        return []
    base = shortlist[0]["override"][stage_name]
    generated: List[Dict[str, Any]] = []
    if len(shortlist) >= 2:
        second = shortlist[1]["override"][stage_name]
        generated.append({"name": f"{stage_name}_p01", "override": stage_override(stage_name, blend_param_dict(base, second, 0.5))})
        generated.append({"name": f"{stage_name}_p02", "override": stage_override(stage_name, blend_param_dict(base, second, 0.75))})
    elif len(shortlist) == 1:
        generated.append({"name": f"{stage_name}_p01", "override": stage_override(stage_name, blend_param_dict(base, base, 1.0))})
        generated.append({"name": f"{stage_name}_p02", "override": stage_override(stage_name, blend_param_dict(base, base, 1.0))})
    if len(shortlist) >= 3:
        third = shortlist[2]["override"][stage_name]
        generated[-1] = {"name": f"{stage_name}_p02", "override": stage_override(stage_name, blend_param_dict(base, third, 0.5))}
    return generated


def gate_pass(delta_ms_ssim: float, delta_psnr: float, gate: Dict[str, Any]) -> bool:
    inclusive = bool(gate.get("inclusive", True))
    ms_limit = float(gate["ms_ssim"])
    psnr_limit = float(gate["psnr"])
    if inclusive:
        return delta_ms_ssim >= ms_limit and delta_psnr >= psnr_limit
    return delta_ms_ssim > ms_limit and delta_psnr > psnr_limit


def compare_rank_rows(left: Dict[str, Any], right: Dict[str, Any]) -> int:
    if abs(left["delta_ms_ssim"] - right["delta_ms_ssim"]) > 0.001:
        return -1 if left["delta_ms_ssim"] > right["delta_ms_ssim"] else 1
    if abs(left["delta_psnr"] - right["delta_psnr"]) > 0.03:
        return -1 if left["delta_psnr"] > right["delta_psnr"] else 1
    if abs(left["visual_score"] - right["visual_score"]) > 1e-12:
        return -1 if left["visual_score"] > right["visual_score"] else 1
    if abs(left["delta_uciqe"] - right["delta_uciqe"]) > 1e-12:
        return -1 if left["delta_uciqe"] > right["delta_uciqe"] else 1
    if abs(left["delta_uiqm"] - right["delta_uiqm"]) > 1e-12:
        return -1 if left["delta_uiqm"] > right["delta_uiqm"] else 1
    return -1 if left["method"].lower() < right["method"].lower() else 1


def rank_summary(summary_path: Path, baseline_method: str, gate: Dict[str, Any]) -> List[Dict[str, Any]]:
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
        row["gate_pass"] = gate_pass(row["delta_ms_ssim"], row["delta_psnr"], gate)
        rows.append(row)
    uciqe_z = zscores([row["delta_uciqe"] for row in rows])
    uiqm_z = zscores([row["delta_uiqm"] for row in rows])
    for idx, row in enumerate(rows):
        row["z_uciqe"] = uciqe_z[idx]
        row["z_uiqm"] = uiqm_z[idx]
        row["visual_score"] = 0.5 * row["z_uciqe"] + 0.5 * row["z_uiqm"]
    ranked = sorted(rows, key=cmp_to_key(compare_rank_rows))
    for idx, row in enumerate(ranked, start=1):
        row["rank"] = idx
    return ranked


def write_rank_outputs(base_path: Path, ranked_rows: Sequence[Dict[str, Any]]) -> None:
    ensure_dir(base_path.parent)
    write_json(base_path.with_suffix(".json"), list(ranked_rows))
    fieldnames = [
        "rank",
        "method",
        "gate_pass",
        "MS_SSIM",
        "PSNR",
        "UCIQE",
        "UIQM",
        "delta_ms_ssim",
        "delta_psnr",
        "delta_uciqe",
        "delta_uiqm",
        "z_uciqe",
        "z_uiqm",
        "visual_score",
    ]
    with base_path.with_suffix(".csv").open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in ranked_rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def compose_params(base_config: Dict[str, Any], winners: Dict[str, Dict[str, Any]], override: Dict[str, Any]) -> Dict[str, Any]:
    params = deep_copy_jsonable(base_config)
    for stage_name in ("rghs", "clahe"):
        if stage_name in winners:
            params[stage_name] = deep_copy_jsonable(winners[stage_name])
    for key, value in override.items():
        params[key] = deep_copy_jsonable(value)
    return params


def write_candidate_config(stage_name: str, phase_name: str, candidate_name: str, params: Dict[str, Any]) -> Path:
    path = CONFIGS_DIR / stage_name / phase_name / f"{candidate_name}.json"
    write_json(path, params)
    return path


def stage_baseline_result_dir(stage_name: str) -> Path:
    return RESULTS_DIR / f"{stage_name}_baseline_pilot92"


def stage_candidate_result_dir(stage_name: str, phase_name: str, candidate_name: str) -> Path:
    return RESULTS_DIR / f"{stage_name}_{phase_name}" / candidate_name


def reusable_stage_baseline(stage_name: str, selection: Dict[str, Any]) -> Tuple[Path, Path | None]:
    setup_dir = Path(selection.get("setup", {}).get("baseline_pilot_dir", ""))
    setup_cfg = CONFIGS_DIR / "setup" / "baseline_mainline_pilot92.json"
    if stage_name == "rghs":
        return setup_dir, setup_cfg
    if stage_name == "clahe":
        winner = selection.get("rghs", {}).get("winner", {})
        if winner.get("name") and winner.get("name") != "baseline":
            return Path(winner["output_dir"]), Path(winner["params_json"])
        return setup_dir, setup_cfg
    if stage_name == "fusion":
        clahe_winner = selection.get("clahe", {}).get("winner", {})
        if clahe_winner.get("name") and clahe_winner.get("name") != "baseline":
            return Path(clahe_winner["output_dir"]), Path(clahe_winner["params_json"])
        rghs_winner = selection.get("rghs", {}).get("winner", {})
        if rghs_winner.get("name") and rghs_winner.get("name") != "baseline":
            return Path(rghs_winner["output_dir"]), Path(rghs_winner["params_json"])
        return setup_dir, setup_cfg
    return stage_baseline_result_dir(stage_name), None


def baseline_override_for_stage(stage_name: str, winners: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    if stage_name == "rghs":
        return {}
    if stage_name == "clahe":
        return {"rghs": deep_copy_jsonable(winners.get("rghs", {}))}
    if stage_name == "fusion":
        payload: Dict[str, Any] = {}
        if "rghs" in winners:
            payload["rghs"] = deep_copy_jsonable(winners["rghs"])
        if "clahe" in winners:
            payload["clahe"] = deep_copy_jsonable(winners["clahe"])
        return payload
    return {}


def phase_gate_for(stage_name: str, phase_name: str) -> Dict[str, Any]:
    if stage_name == "fusion" and phase_name == "pilot":
        return FULL506_GATE
    if phase_name == "smoke":
        return SMOKE_GATE
    return SOFT_GATE


def shortlist_rows(ranked_rows: Sequence[Dict[str, Any]], limit: int) -> List[Dict[str, Any]]:
    passers = [row for row in ranked_rows if row["gate_pass"]]
    return passers[:limit]


def unique_candidates(candidates: Sequence[Dict[str, Any]], stage_name: str, limit: int) -> List[Dict[str, Any]]:
    seen = set()
    unique: List[Dict[str, Any]] = []
    for candidate in candidates:
        signature = serialize_override(candidate["override"][stage_name])
        if signature in seen:
            continue
        seen.add(signature)
        unique.append(candidate)
        if len(unique) >= limit:
            break
    return unique


def render_table_preview(score_json_path: Path, top_n: int = 3) -> List[str]:
    if not score_json_path.exists():
        return ["- 尚无排序结果"]
    rows = read_json(score_json_path)
    if not rows:
        return ["- 排序结果为空"]
    lines: List[str] = []
    for row in rows[:top_n]:
        lines.append(
            f"- `{row['method']}`: ΔMS-SSIM={row['delta_ms_ssim']:.6f}, "
            f"ΔPSNR={row['delta_psnr']:.4f}, ΔUCIQE={row['delta_uciqe']:.4f}, "
            f"ΔUIQM={row['delta_uiqm']:.4f}, gate_pass={row['gate_pass']}"
        )
    return lines


def render_analysis(selection: Dict[str, Any]) -> None:
    lines = [
        "# H2 RGHS / CLAHE / Fusion 顺序优化",
        "",
        "## 当前状态",
        "",
        f"- 创建时间：`{selection.get('created_at', '')}`",
        f"- 最近更新：`{selection.get('updated_at', '')}`",
        f"- 总状态：`{selection.get('status', '')}`",
        f"- 主线基线：`{selection.get('base_config', '')}`",
        f"- smoke12 manifest：`{selection.get('smoke_manifest', '')}`",
        f"- pilot92 manifest：`{selection.get('pilot_manifest', '')}`",
        f"- full506 manifest：`{selection.get('full_manifest', '')}`",
        "",
        "## Setup",
        "",
        f"- pilot92 baseline 输出：`{selection.get('setup', {}).get('baseline_pilot_dir', '')}`",
        f"- pilot92 baseline 评测：`{selection.get('setup', {}).get('baseline_pilot_eval_dir', '')}`",
        f"- smoke12 baseline 评测：`{selection.get('setup', {}).get('baseline_smoke_eval_dir', '')}`",
        f"- full506 chunk manifests：`{selection.get('setup', {}).get('full_chunks', [])}`",
        "",
    ]
    for stage_name in ("rghs", "clahe", "fusion"):
        stage_info = selection.get(stage_name, {})
        lines += [
            f"## {stage_name.upper()}",
            "",
            f"- 状态：`{stage_info.get('status', 'pending')}`",
            f"- baseline 配置：`{stage_info.get('baseline_config_json', '')}`",
            f"- baseline pilot 输出：`{stage_info.get('baseline_pilot_dir', '')}`",
            f"- smoke 排序：`{stage_info.get('smoke', {}).get('official_score_json', '')}`",
        ]
        backstop_json = stage_info.get("smoke", {}).get("backstop_score_json")
        if backstop_json:
            lines.append(f"- smoke Final 回退检查：`{backstop_json}`")
        lines += render_table_preview(Path(stage_info.get("smoke", {}).get("official_score_json", ""))) if stage_info.get("smoke", {}).get("official_score_json") else ["- smoke 排序尚未生成"]
        lines += [
            "",
            f"- pilot 排序：`{stage_info.get('pilot', {}).get('official_score_json', '')}`",
        ]
        pilot_backstop_json = stage_info.get("pilot", {}).get("backstop_score_json")
        if pilot_backstop_json:
            lines.append(f"- pilot Final 回退检查：`{pilot_backstop_json}`")
        lines += render_table_preview(Path(stage_info.get("pilot", {}).get("official_score_json", ""))) if stage_info.get("pilot", {}).get("official_score_json") else ["- pilot 排序尚未生成"]
        winner = stage_info.get("winner", {})
        lines += [
            "",
            f"- winner：`{winner.get('name', 'baseline')}`",
            f"- winner 参数：`{winner.get('params_json', '')}`",
            "",
        ]
    full506_info = selection.get("full506", {})
    lines += [
        "## Full506",
        "",
        f"- 状态：`{full506_info.get('status', 'pending')}`",
        f"- baseline 目录：`{selection.get('full506_baseline_dir', '')}`",
        f"- 排序结果：`{full506_info.get('score_json', '')}`",
    ]
    if full506_info.get("score_json"):
        lines += render_table_preview(Path(full506_info["score_json"]))
    else:
        lines.append("- 尚未进入 full506")
    lines += [
        "",
        f"- 最终 winner：`{full506_info.get('winner', {}).get('name', '')}`",
        f"- 最终说明：`{full506_info.get('final_note', '')}`",
        "",
    ]
    ANALYSIS_PATH.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def setup_stage(args: argparse.Namespace, selection: Dict[str, Any], resume: bool) -> Dict[str, Any]:
    base_config_path = resolve_project_path(args.base_config)
    pilot_manifest = resolve_project_path(args.pilot_manifest)
    smoke_manifest = resolve_project_path(args.smoke_manifest) if args.smoke_manifest else (MANIFESTS_DIR / "smoke12.txt")
    full_manifest = resolve_project_path(args.full_manifest)

    update_status("setup", "running")
    base_config = read_json(base_config_path)
    baseline_pilot_dir = RESULTS_DIR / "baseline_mainline_pilot92"
    baseline_pilot_eval_dir = SCORES_DIR / "baseline_mainline_pilot92_final"
    baseline_smoke_eval_dir = SCORES_DIR / "baseline_mainline_smoke12_final"

    mainline_pilot_config = CONFIGS_DIR / "setup" / "baseline_mainline_pilot92.json"
    write_json(mainline_pilot_config, base_config)

    run_pipeline(pilot_manifest, baseline_pilot_dir, mainline_pilot_config, "setup_baseline_pilot92", resume)
    run_eval_single(baseline_pilot_dir / "png" / "Final", "baseline", pilot_manifest, baseline_pilot_eval_dir, "setup_baseline_pilot92_eval", resume)
    if not smoke_manifest.exists() or not args.smoke_manifest:
        selected = select_smoke12(baseline_pilot_eval_dir / "per_image_metrics.csv", smoke_manifest, int(args.smoke_count))
    else:
        selected = read_manifest(smoke_manifest)
    run_eval_single(baseline_pilot_dir / "png" / "Final", "baseline", smoke_manifest, baseline_smoke_eval_dir, "setup_baseline_smoke12_eval", resume)
    full_chunks = split_manifest(full_manifest, "full506")

    selection["status"] = "setup_completed"
    selection["smoke_manifest"] = str(smoke_manifest.resolve())
    selection["setup"] = {
        "baseline_pilot_dir": str(baseline_pilot_dir.resolve()),
        "baseline_pilot_eval_dir": str(baseline_pilot_eval_dir.resolve()),
        "baseline_smoke_eval_dir": str(baseline_smoke_eval_dir.resolve()),
        "smoke12_stems": selected,
        "full_chunks": [str(path.resolve()) for path in full_chunks],
    }
    save_selection(selection)
    render_analysis(selection)
    update_status("setup", "completed", last_eval_output=str(baseline_smoke_eval_dir.resolve()))
    return selection


def run_candidate_phase(
    stage_name: str,
    phase_name: str,
    target_stage: str,
    backstop_stage: str | None,
    manifest_path: Path,
    baseline_pilot_dir: Path,
    base_config: Dict[str, Any],
    winners: Dict[str, Dict[str, Any]],
    candidate_defs: Sequence[Dict[str, Any]],
    resume: bool,
) -> Dict[str, Any]:
    official_methods: List[Tuple[str, Path]] = [("baseline", baseline_pilot_dir / "png" / target_stage)]
    backstop_methods: List[Tuple[str, Path]] = []
    if backstop_stage:
        backstop_methods.append(("baseline", baseline_pilot_dir / "png" / backstop_stage))
    candidate_records: List[Dict[str, Any]] = []
    for candidate_def in candidate_defs:
        name = str(candidate_def["name"])
        override = deep_copy_jsonable(candidate_def["override"])
        params = compose_params(base_config, winners, override)
        params_json = write_candidate_config(stage_name, phase_name, name, params)
        output_dir = stage_candidate_result_dir(stage_name, phase_name, name)
        update_status(stage_name, f"{phase_name}_candidate_running", current_candidate=name)
        run_pipeline(manifest_path, output_dir, params_json, f"{stage_name}_{phase_name}_{name}", resume)
        official_methods.append((name, output_dir / "png" / target_stage))
        if backstop_stage:
            backstop_methods.append((name, output_dir / "png" / backstop_stage))
        candidate_records.append({"name": name, "override": override, "params_json": str(params_json.resolve()), "output_dir": str(output_dir.resolve())})

    official_eval_dir = SCORES_DIR / f"{stage_name}_{phase_name}_{target_stage.lower()}"
    run_eval_methods(official_methods, manifest_path, official_eval_dir, f"{stage_name}_{phase_name}_{target_stage.lower()}_eval", resume)
    official_ranked = rank_summary(official_eval_dir / "summary.json", "baseline", phase_gate_for(stage_name, phase_name))
    official_score_base = official_eval_dir / "ranked"
    write_rank_outputs(official_score_base, official_ranked)

    backstop_score_json: str | None = None
    if backstop_stage:
        backstop_eval_dir = SCORES_DIR / f"{stage_name}_{phase_name}_{backstop_stage.lower()}"
        run_eval_methods(backstop_methods, manifest_path, backstop_eval_dir, f"{stage_name}_{phase_name}_{backstop_stage.lower()}_eval", resume)
        backstop_ranked = rank_summary(backstop_eval_dir / "summary.json", "baseline", SOFT_GATE)
        backstop_score_base = backstop_eval_dir / "ranked"
        write_rank_outputs(backstop_score_base, backstop_ranked)
        backstop_score_json = str(backstop_score_base.with_suffix(".json").resolve())

    record_by_name = {record["name"]: record for record in candidate_records}
    shortlist = shortlist_rows(official_ranked, SMOKE_KEEP[stage_name] if phase_name == "smoke" else PILOT_LIMIT[stage_name])
    shortlisted_records: List[Dict[str, Any]] = []
    for row in shortlist:
        record = deepcopy(record_by_name[row["method"]])
        record["official_metrics"] = deepcopy(row)
        shortlisted_records.append(record)

    return {
        "official_eval_dir": str(official_eval_dir.resolve()),
        "official_score_json": str(official_score_base.with_suffix(".json").resolve()),
        "official_score_csv": str(official_score_base.with_suffix(".csv").resolve()),
        "backstop_score_json": backstop_score_json,
        "shortlist": shortlisted_records,
    }


def candidate_defs_from_coarse(stage_name: str, coarse_defs: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [{"name": item["name"], "override": stage_override(stage_name, item["params"])} for item in coarse_defs]


def stage_result_payload(phase_result: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "official_eval_dir": phase_result["official_eval_dir"],
        "official_score_json": phase_result["official_score_json"],
        "official_score_csv": phase_result["official_score_csv"],
        "backstop_score_json": phase_result["backstop_score_json"],
        "shortlist": [
            {
                "name": item["name"],
                "params_json": item["params_json"],
                "output_dir": item["output_dir"],
                "official_metrics": item["official_metrics"],
            }
            for item in phase_result["shortlist"]
        ],
    }


def run_tuning_stage(args: argparse.Namespace, selection: Dict[str, Any], stage_name: str, base_config: Dict[str, Any], winners: Dict[str, Dict[str, Any]], resume: bool) -> Dict[str, Any]:
    spec = STAGE_SPECS[stage_name]
    pilot_manifest = resolve_project_path(args.pilot_manifest)
    smoke_manifest = resolve_project_path(args.smoke_manifest) if args.smoke_manifest else resolve_project_path(selection["smoke_manifest"])

    update_status(stage_name, "baseline_running")
    baseline_pilot_dir, reusable_config = reusable_stage_baseline(stage_name, selection)
    if baseline_pilot_dir.is_dir() and has_manifest_outputs(baseline_pilot_dir / "png" / "Final", pilot_manifest):
        baseline_config_json = reusable_config if reusable_config is not None else write_candidate_config(stage_name, "baseline", f"{stage_name}_baseline", compose_params(base_config, {}, baseline_override_for_stage(stage_name, winners)))
    else:
        baseline_config = compose_params(base_config, {}, baseline_override_for_stage(stage_name, winners))
        baseline_config_json = write_candidate_config(stage_name, "baseline", f"{stage_name}_baseline", baseline_config)
        baseline_pilot_dir = stage_baseline_result_dir(stage_name)
        run_pipeline(pilot_manifest, baseline_pilot_dir, baseline_config_json, f"{stage_name}_baseline_pilot92", resume)

    smoke_result = run_candidate_phase(stage_name, "smoke", spec["target_stage"], spec["backstop_stage"], smoke_manifest, baseline_pilot_dir, base_config, winners, candidate_defs_from_coarse(stage_name, spec["coarse_candidates"]), resume)

    stage_info: Dict[str, Any] = {
        "status": "smoke_completed",
        "baseline_config_json": str(baseline_config_json.resolve()),
        "baseline_pilot_dir": str(baseline_pilot_dir.resolve()),
        "smoke": stage_result_payload(smoke_result),
        "pilot": {},
        "winner": {"name": "baseline", "params_json": str(baseline_config_json.resolve()), "override": {}},
    }

    smoke_shortlist = smoke_result["shortlist"]
    if not smoke_shortlist:
        stage_info["status"] = "plateau_after_smoke"
        selection[stage_name] = stage_info
        save_selection(selection)
        render_analysis(selection)
        return selection

    if args.stop_after == "smoke":
        selection[stage_name] = stage_info
        save_selection(selection)
        render_analysis(selection)
        return selection

    generated = refinement_candidates(stage_name, smoke_shortlist[:3])
    deduped = unique_candidates(
        [{"name": item["name"], "override": item["override"]} for item in smoke_shortlist + [{"name": item["name"], "override": item["override"]} for item in generated]],
        stage_name,
        spec["pilot_limit"],
    )
    pilot_result = run_candidate_phase(stage_name, "pilot", spec["target_stage"], spec["backstop_stage"], pilot_manifest, baseline_pilot_dir, base_config, winners, deduped, resume)

    stage_info["status"] = "pilot_completed"
    stage_info["pilot"] = stage_result_payload(pilot_result)
    pilot_shortlist = pilot_result["shortlist"]
    if pilot_shortlist:
        winner = deepcopy(pilot_shortlist[0])
        stage_info["winner"] = {
            "name": winner["name"],
            "params_json": winner["params_json"],
            "override": winner["override"],
            "output_dir": winner["output_dir"],
            "official_metrics": winner["official_metrics"],
        }
        winners[stage_name] = deepcopy(winner["override"][stage_name])
        if spec["winner_path"] is not None:
            write_json(spec["winner_path"], stage_info["winner"])
    else:
        stage_info["status"] = "plateau_after_pilot"

    selection[stage_name] = stage_info
    save_selection(selection)
    render_analysis(selection)
    return selection


def run_full506(args: argparse.Namespace, selection: Dict[str, Any], base_config: Dict[str, Any], winners: Dict[str, Dict[str, Any]], resume: bool) -> Dict[str, Any]:
    fusion_info = selection.get("fusion", {})
    pilot_shortlist = fusion_info.get("pilot", {}).get("shortlist", [])
    if not pilot_shortlist:
        selection["full506"] = {
            "status": "skipped",
            "final_note": "fusion pilot 阶段无候选满足 ΔMS-SSIM>0 且 ΔPSNR>0，自动停止于参数 plateau。",
            "winner": {},
        }
        save_selection(selection)
        render_analysis(selection)
        return selection

    full_manifest = resolve_project_path(args.full_manifest)
    chunk_paths = [Path(path_text) for path_text in selection.get("setup", {}).get("full_chunks", [])]
    baseline_dir = resolve_project_path(args.full506_baseline_dir)
    methods: List[Tuple[str, Path]] = [("baseline", baseline_dir / "png" / "Final")]
    winner_candidates: List[Dict[str, Any]] = []

    for item in pilot_shortlist[:FULL506_LIMIT]:
        name = str(item["name"])
        params = compose_params(base_config, winners, item["override"])
        params_json = write_candidate_config("full506", "finalists", name, params)
        output_dir = RESULTS_DIR / "full506" / name
        for chunk_idx, chunk_path in enumerate(chunk_paths, start=1):
            update_status("full506", "chunk_running", current_candidate=name, current_chunk=f"chunk{chunk_idx}")
            run_pipeline(chunk_path, output_dir, params_json, f"full506_{name}_chunk{chunk_idx}", resume)
        methods.append((name, output_dir / "png" / "Final"))
        winner_candidates.append({"name": name, "params_json": str(params_json.resolve()), "output_dir": str(output_dir.resolve()), "override": deep_copy_jsonable(item["override"])})

    eval_dir = SCORES_DIR / "full506_final"
    run_eval_methods(methods, full_manifest, eval_dir, "full506_final_eval", resume)
    ranked = rank_summary(eval_dir / "summary.json", "baseline", FULL506_GATE)
    score_base = eval_dir / "ranked"
    write_rank_outputs(score_base, ranked)
    record_by_name = {item["name"]: item for item in winner_candidates}
    shortlist = [row for row in ranked if row["gate_pass"]][:FULL506_LIMIT]

    full506_info: Dict[str, Any] = {
        "status": "completed",
        "score_json": str(score_base.with_suffix(".json").resolve()),
        "score_csv": str(score_base.with_suffix(".csv").resolve()),
        "winner": {},
        "final_note": "",
    }
    if shortlist:
        row = shortlist[0]
        record = record_by_name[row["method"]]
        winner = {"name": record["name"], "params_json": record["params_json"], "output_dir": record["output_dir"], "override": record["override"], "official_metrics": row}
        full506_info["winner"] = winner
        full506_info["final_note"] = "存在候选相对当前主线同时提升 MS-SSIM 与 PSNR。"
        write_json(WINNER_FULL506_PATH, winner)
    else:
        full506_info["final_note"] = "full506 阶段未出现同时提升 MS-SSIM 与 PSNR 的候选，主线保持不变。"

    selection["full506"] = full506_info
    selection["status"] = "completed"
    save_selection(selection)
    render_analysis(selection)
    update_status("full506", "completed", last_eval_output=str(eval_dir.resolve()))
    return selection


def load_winners_from_selection(selection: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    winners: Dict[str, Dict[str, Any]] = {}
    for stage_name in ("rghs", "clahe"):
        winner = selection.get(stage_name, {}).get("winner", {})
        override = winner.get("override", {})
        if stage_name in override:
            winners[stage_name] = deep_copy_jsonable(override[stage_name])
    return winners


def main() -> int:
    args = parse_args()
    ensure_dir(CONFIGS_DIR)
    ensure_dir(LOGS_DIR)
    ensure_dir(MANIFESTS_DIR)
    ensure_dir(RESULTS_DIR)
    ensure_dir(SCORES_DIR)

    selection = load_selection(args)
    base_config = read_json(resolve_project_path(args.base_config))

    if args.stage in {"setup", "all"}:
        selection = setup_stage(args, selection, resume=args.resume)
        if args.stage == "setup":
            return 0

    winners = load_winners_from_selection(selection)

    if args.stage in {"rghs", "all"}:
        selection = run_tuning_stage(args, selection, "rghs", base_config, winners, resume=args.resume)
        winners = load_winners_from_selection(selection)
        if args.stage == "rghs" or args.stop_after in {"smoke", "pilot"}:
            return 0

    if args.stage in {"clahe", "all"}:
        selection = run_tuning_stage(args, selection, "clahe", base_config, winners, resume=args.resume)
        winners = load_winners_from_selection(selection)
        if args.stage == "clahe" or args.stop_after in {"smoke", "pilot"}:
            return 0

    if args.stage in {"fusion", "all"}:
        selection = run_tuning_stage(args, selection, "fusion", base_config, winners, resume=args.resume)
        winners = load_winners_from_selection(selection)
        if args.stage == "fusion" or args.stop_after in {"smoke", "pilot"}:
            return 0

    if args.stage == "all":
        run_full506(args, selection, base_config, winners, resume=args.resume)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
