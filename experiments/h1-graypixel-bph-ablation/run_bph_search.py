from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

import cv2
import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[2]
METRICS_DIR = PROJECT_ROOT / "metrics"
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(METRICS_DIR) not in sys.path:
    sys.path.insert(0, str(METRICS_DIR))

from metrics.protocol_common import read_bgr, resolve_project_path, write_lines


EXPERIMENT_DIR = Path(__file__).resolve().parent
OUTPUT_ROOT = EXPERIMENT_DIR / "outputs"
DEFAULT_BASE_CONFIG = PROJECT_ROOT / "experiments" / "optimization_v1" / "configs" / "best_full506_r4_03.json"
DEFAULT_ORIGINAL_DIR = PROJECT_ROOT / "data" / "inputImg" / "Original"
DEFAULT_EXPLORE_MANIFEST = PROJECT_ROOT / "data" / "eval_subset_explore64_full506_bph_v1.txt"
DEFAULT_FULL_MANIFEST = (
    PROJECT_ROOT / "metrics" / "outputs" / "evaluate_protocol_v2" / "full506_c25" / "complete_case_manifest.txt"
)
DEFAULT_SEED = 20260413


ROUND1_CANDIDATES: List[Dict[str, object]] = [
    {"name": "bph00_baseline", "family": None, "bph": {}},
    {"name": "bph10_gp_strict", "family": "G", "bph": {"gray_s_thr": 12, "lum_low": 0.12, "lum_high": 0.88}},
    {"name": "bph11_gp_mid", "family": "G", "bph": {"gray_s_thr": 16, "lum_low": 0.10, "lum_high": 0.90}},
    {"name": "bph12_gp_loose", "family": "G", "bph": {"gray_s_thr": 24, "lum_low": 0.08, "lum_high": 0.92}},
    {"name": "bph13_gp_narrow_mid", "family": "G", "bph": {"gray_s_thr": 20, "lum_low": 0.15, "lum_high": 0.85}},
    {"name": "bph20_pregain_conservative", "family": "P", "bph": {"pre_gain_clip": 2.0, "red_gain_extra": 1.15}},
    {"name": "bph21_pregain_mid", "family": "P", "bph": {"pre_gain_clip": 2.3, "red_gain_extra": 1.25}},
    {"name": "bph22_pregain_aggressive", "family": "P", "bph": {"pre_gain_clip": 3.0, "red_gain_extra": 1.45}},
    {"name": "bph30_accc_conservative", "family": "A", "bph": {"accc_alpha": 0.50, "accc_delta_max": 0.18}},
    {"name": "bph31_accc_mid", "family": "A", "bph": {"accc_alpha": 0.60, "accc_delta_max": 0.22}},
    {"name": "bph32_accc_aggressive", "family": "A", "bph": {"accc_alpha": 0.85, "accc_delta_max": 0.30}},
    {"name": "bph40_brightness_tight", "family": "B", "bph": {"brightness_scale_clip": [0.90, 1.10]}},
    {"name": "bph41_brightness_loose", "family": "B", "bph": {"brightness_scale_clip": [0.75, 1.25]}},
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="H1 gray-pixel BPH ablation orchestrator.")
    parser.add_argument(
        "--stage",
        choices=["build-manifest", "smoke", "round1", "round2", "full506", "all"],
        default="all",
    )
    parser.add_argument("--original-dir", default=str(DEFAULT_ORIGINAL_DIR))
    parser.add_argument("--explore-manifest", default=str(DEFAULT_EXPLORE_MANIFEST))
    parser.add_argument("--full-manifest", default=str(DEFAULT_FULL_MANIFEST))
    parser.add_argument("--base-config", default=str(DEFAULT_BASE_CONFIG))
    parser.add_argument("--explore-count", type=int, default=64)
    parser.add_argument("--smoke-count", type=int, default=5)
    parser.add_argument("--diag-round1", type=int, default=8)
    parser.add_argument("--diag-round2", type=int, default=12)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--force-manifest", action="store_true")
    parser.add_argument("--skip-diagnostics", action="store_true")
    return parser.parse_args()


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def read_json(path: Path) -> Dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def run_python(args: Sequence[str]) -> None:
    cmd = [sys.executable, *args]
    print(f"[RUN] {' '.join(str(x) for x in cmd)}")
    subprocess.run(cmd, cwd=PROJECT_ROOT, check=True)


def load_fixed_downstream(base_config_path: Path) -> Dict[str, object]:
    base_config = read_json(base_config_path)
    final_cfg = base_config.get("final", {})
    if not final_cfg:
        raise ValueError(f"Missing final config in {base_config_path}")
    return {"fusion": {}, "final": final_cfg}


def candidate_params(fixed_downstream: Dict[str, object], bph_overrides: Dict[str, object]) -> Dict[str, object]:
    params: Dict[str, object] = {
        "fusion": fixed_downstream.get("fusion", {}),
        "final": fixed_downstream["final"],
    }
    if bph_overrides:
        params["bph"] = bph_overrides
    return params


def classify_tertile(value: float, q1: float, q2: float) -> str:
    if value <= q1:
        return "low"
    if value <= q2:
        return "mid"
    return "high"


def compute_manifest_stats(image_paths: Sequence[Path]) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for i, path in enumerate(image_paths, start=1):
        img = read_bgr(path)
        y = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)[:, :, 0].astype(np.float32)
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB).astype(np.float32)
        a = lab[:, :, 1] - 128.0
        b = lab[:, :, 2] - 128.0
        chroma = np.sqrt(a * a + b * b)
        rows.append(
            {
                "stem": path.stem,
                "filename": path.name,
                "Y_mean": float(np.mean(y)),
                "Y_std": float(np.std(y)),
                "Chroma_mean": float(np.mean(chroma)),
            }
        )
        if i == 1 or i == len(image_paths) or i % 50 == 0:
            print(f"[MANIFEST] stats {i}/{len(image_paths)} {path.name}")
    return rows


def build_explore_manifest(
    original_dir: Path,
    manifest_path: Path,
    stats_csv_path: Path,
    count: int,
    seed: int,
    force: bool,
) -> List[str]:
    if manifest_path.exists() and not force:
        print(f"[SKIP] manifest already exists: {manifest_path}")
        return [line.strip() for line in manifest_path.read_text(encoding="utf-8").splitlines() if line.strip() and not line.startswith("#")]

    image_paths = sorted((p for p in original_dir.iterdir() if p.is_file()), key=lambda p: p.name.lower())
    image_paths = [p for p in image_paths if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}]
    if not image_paths:
        raise RuntimeError(f"No images found in {original_dir}")

    rows = compute_manifest_stats(image_paths)
    y_mean = np.asarray([float(row["Y_mean"]) for row in rows], dtype=np.float64)
    y_std = np.asarray([float(row["Y_std"]) for row in rows], dtype=np.float64)
    chroma = np.asarray([float(row["Chroma_mean"]) for row in rows], dtype=np.float64)
    q = {
        "Y_mean": np.quantile(y_mean, [1.0 / 3.0, 2.0 / 3.0]),
        "Y_std": np.quantile(y_std, [1.0 / 3.0, 2.0 / 3.0]),
        "Chroma_mean": np.quantile(chroma, [1.0 / 3.0, 2.0 / 3.0]),
    }

    buckets: Dict[str, List[Dict[str, object]]] = {}
    for row in rows:
        bucket = "|".join(
            [
                classify_tertile(float(row["Y_mean"]), *q["Y_mean"]),
                classify_tertile(float(row["Y_std"]), *q["Y_std"]),
                classify_tertile(float(row["Chroma_mean"]), *q["Chroma_mean"]),
            ]
        )
        row["bucket"] = bucket
        buckets.setdefault(bucket, []).append(row)

    rng = np.random.default_rng(seed)
    for bucket_rows in buckets.values():
        order = rng.permutation(len(bucket_rows))
        bucket_rows[:] = [bucket_rows[int(i)] for i in order]

    selected: List[Dict[str, object]] = []
    seen = set()
    bucket_keys = sorted(buckets)
    made_progress = True
    while len(selected) < count and made_progress:
        made_progress = False
        for key in bucket_keys:
            bucket_rows = buckets[key]
            while bucket_rows and str(bucket_rows[0]["stem"]) in seen:
                bucket_rows.pop(0)
            if not bucket_rows:
                continue
            row = bucket_rows.pop(0)
            seen.add(str(row["stem"]))
            selected.append(row)
            made_progress = True
            if len(selected) >= count:
                break

    if len(selected) < count:
        for row in sorted(rows, key=lambda item: str(item["filename"]).lower()):
            stem = str(row["stem"])
            if stem in seen:
                continue
            seen.add(stem)
            selected.append(row)
            if len(selected) >= count:
                break

    selected = selected[:count]
    selected_stems = [str(row["stem"]) for row in selected]
    manifest_lines = [
        "# full506 explore subset for H1 BPH search",
        f"# created_at: {now_iso()}",
        f"# seed: {seed}",
        f"# count: {len(selected_stems)}",
        *selected_stems,
    ]
    write_lines(manifest_path, manifest_lines)

    stats_csv_path.parent.mkdir(parents=True, exist_ok=True)
    with stats_csv_path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["stem", "filename", "Y_mean", "Y_std", "Chroma_mean", "bucket", "selected"],
        )
        writer.writeheader()
        selected_set = set(selected_stems)
        for row in sorted(rows, key=lambda item: str(item["filename"]).lower()):
            writer.writerow(
                {
                    "stem": row["stem"],
                    "filename": row["filename"],
                    "Y_mean": f"{float(row['Y_mean']):.6f}",
                    "Y_std": f"{float(row['Y_std']):.6f}",
                    "Chroma_mean": f"{float(row['Chroma_mean']):.6f}",
                    "bucket": row["bucket"],
                    "selected": "1" if str(row["stem"]) in selected_set else "0",
                }
            )

    print(f"[DONE] wrote explore manifest: {manifest_path}")
    return selected_stems


def write_candidate_files(
    round_dir: Path,
    candidate_defs: Sequence[Dict[str, object]],
    fixed_downstream: Dict[str, object],
) -> Dict[str, Path]:
    config_dir = ensure_dir(round_dir / "candidate_params")
    matrix: List[Dict[str, object]] = []
    paths: Dict[str, Path] = {}
    for item in candidate_defs:
        name = str(item["name"])
        params = candidate_params(fixed_downstream, dict(item.get("bph", {})))
        target = config_dir / f"{name}.json"
        write_json(target, params)
        paths[name] = target
        matrix.append({"name": name, "family": item.get("family"), "params": params})
    write_json(round_dir / "candidate_matrix.json", matrix)
    return paths


def run_candidates(
    run_root: Path,
    manifest_path: Path,
    candidate_config_paths: Dict[str, Path],
    original_dir: Path,
    limit: Optional[int] = None,
) -> None:
    ensure_dir(run_root)
    ordered = list(candidate_config_paths.items())
    for idx, (name, config_path) in enumerate(ordered, start=1):
        output_dir = run_root / name
        args = [
            "main.py",
            "--input-dir",
            str(original_dir),
            "--manifest",
            str(manifest_path),
            "--output-dir",
            str(output_dir),
            "--params-json",
            str(config_path),
            "--skip-existing",
        ]
        if limit is not None:
            args.extend(["--limit", str(limit)])
        print(f"[CANDIDATE] {idx}/{len(ordered)} {name}")
        run_python(args)


def evaluate_methods(
    methods_root: Path,
    manifest_path: Path,
    output_dir: Path,
    original_dir: Path,
) -> Path:
    ensure_dir(output_dir)
    run_python(
        [
            "metrics/evaluate_protocol_v2.py",
            "--quiet",
            "--original-dir",
            str(original_dir),
            "--manifest",
            str(manifest_path),
            "--methods-root",
            str(methods_root),
            "--methods-subdir",
            "png/Final",
            "--output-dir",
            str(output_dir),
        ]
    )
    return output_dir / "summary.json"


def score_methods(summary_json: Path, reference_method: str, output_csv: Path) -> Path:
    run_python(
        [
            "metrics/score_protocol_v2.py",
            "--summary-json",
            str(summary_json),
            "--reference-method",
            reference_method,
            "--output-csv",
            str(output_csv),
        ]
    )
    return output_csv


def load_summary(summary_json: Path) -> Dict[str, object]:
    return json.loads(summary_json.read_text(encoding="utf-8"))


def load_scores(score_csv: Path) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    with score_csv.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            parsed: Dict[str, object] = {"method": row["method"]}
            for key, value in row.items():
                if key == "method":
                    continue
                if value is None or value == "":
                    parsed[key] = value
                elif key in {"reference_method"}:
                    parsed[key] = value
                elif key in {"count"}:
                    parsed[key] = int(float(value))
                else:
                    parsed[key] = float(value)
            rows.append(parsed)
    return rows


def metric_mean(summary: Dict[str, object], method_name: str, metric_name: str) -> float:
    methods = summary["methods"]
    method_summary = methods[method_name]
    metrics = method_summary["metrics"]
    value = metrics[metric_name]["mean"]
    if value is None:
        raise ValueError(f"Missing metric mean: {method_name} {metric_name}")
    return float(value)


def guardrail_ok(
    summary: Dict[str, object],
    method_name: str,
    baseline_name: str,
    max_ms_ssim_drop: float,
    max_psnr_drop: float,
) -> Tuple[bool, Dict[str, float]]:
    baseline_ms = metric_mean(summary, baseline_name, "MS_SSIM")
    baseline_psnr = metric_mean(summary, baseline_name, "PSNR")
    current_ms = metric_mean(summary, method_name, "MS_SSIM")
    current_psnr = metric_mean(summary, method_name, "PSNR")
    ms_drop = baseline_ms - current_ms
    psnr_drop = baseline_psnr - current_psnr
    ok = ms_drop <= max_ms_ssim_drop and psnr_drop <= max_psnr_drop
    return ok, {"ms_ssim_drop": ms_drop, "psnr_drop": psnr_drop}


def dynamic_guardrail_limits(
    row: Dict[str, object],
    base_ms_ssim_drop: float,
    base_psnr_drop: float,
    score_bonus_scale: float,
    max_ms_ssim_bonus: float,
    max_psnr_bonus: float,
) -> Dict[str, float]:
    composite_score = max(0.0, float(row.get("composite_score", 0.0) or 0.0))
    gain_ratio = min(1.0, composite_score / score_bonus_scale) if score_bonus_scale > 0 else 0.0
    return {
        "dynamic_gain_ratio": gain_ratio,
        "dynamic_ms_ssim_limit": base_ms_ssim_drop + max_ms_ssim_bonus * gain_ratio,
        "dynamic_psnr_limit": base_psnr_drop + max_psnr_bonus * gain_ratio,
    }


def qualified_rows(
    score_rows: Sequence[Dict[str, object]],
    summary: Dict[str, object],
    baseline_name: str,
    max_ms_ssim_drop: float,
    max_psnr_drop: float,
    dynamic_relaxation: Optional[Dict[str, float]] = None,
) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for row in score_rows:
        method_name = str(row["method"])
        ok, guard = guardrail_ok(summary, method_name, baseline_name, max_ms_ssim_drop, max_psnr_drop)
        enriched = dict(row)
        enriched.update(guard)
        enriched["hard_ms_ssim_limit"] = max_ms_ssim_drop
        enriched["hard_psnr_limit"] = max_psnr_drop
        enriched["hard_qualified"] = ok
        if dynamic_relaxation is not None and method_name != baseline_name:
            limits = dynamic_guardrail_limits(
                row,
                base_ms_ssim_drop=max_ms_ssim_drop,
                base_psnr_drop=max_psnr_drop,
                score_bonus_scale=float(dynamic_relaxation["score_bonus_scale"]),
                max_ms_ssim_bonus=float(dynamic_relaxation["max_ms_ssim_bonus"]),
                max_psnr_bonus=float(dynamic_relaxation["max_psnr_bonus"]),
            )
            dynamic_ok = (
                guard["ms_ssim_drop"] <= limits["dynamic_ms_ssim_limit"]
                and guard["psnr_drop"] <= limits["dynamic_psnr_limit"]
            )
            enriched.update(limits)
        else:
            enriched["dynamic_gain_ratio"] = 0.0
            enriched["dynamic_ms_ssim_limit"] = max_ms_ssim_drop
            enriched["dynamic_psnr_limit"] = max_psnr_drop
            dynamic_ok = ok
        enriched["qualified"] = dynamic_ok if dynamic_relaxation is not None else ok
        rows.append(enriched)
    return rows


def select_family_best(
    rows: Sequence[Dict[str, object]],
    candidate_defs: Sequence[Dict[str, object]],
) -> Dict[str, List[str]]:
    name_to_family = {str(item["name"]): item.get("family") for item in candidate_defs}
    groups: Dict[str, List[str]] = {"G": [], "P": [], "A": [], "B": []}
    for row in rows:
        if not row.get("qualified"):
            continue
        name = str(row["method"])
        family = name_to_family.get(name)
        if family in groups:
            groups[family].append(name)
    return groups


def run_visual_diagnostics(
    output_dir: Path,
    manifest_path: Path,
    original_dir: Path,
    sample_count: int,
    seed: int,
    methods: Sequence[Tuple[str, Path]],
) -> None:
    if not methods:
        return
    args = [
        "metrics/visual_diagnostics.py",
        "--original-dir",
        str(original_dir),
        "--manifest",
        str(manifest_path),
        "--output-dir",
        str(output_dir),
        "--sample-count",
        str(sample_count),
        "--seed",
        str(seed),
    ]
    for name, path in methods:
        args.extend(["--method", f"{name}={path}"])
    run_python(args)


def merge_bph_overrides(items: Iterable[Dict[str, object]]) -> Dict[str, object]:
    merged: Dict[str, object] = {}
    for item in items:
        merged.update(item)
    return merged


def family_override_lookup(candidate_defs: Sequence[Dict[str, object]]) -> Dict[str, Dict[str, object]]:
    return {str(item["name"]): dict(item.get("bph", {})) for item in candidate_defs}


def round1_candidate_defs() -> List[Dict[str, object]]:
    return [dict(item) for item in ROUND1_CANDIDATES]


def round2_candidate_defs(
    round1_selection: Dict[str, object],
    round1_candidates: Sequence[Dict[str, object]],
) -> List[Dict[str, object]]:
    override_map = family_override_lookup(round1_candidates)
    winners = round1_selection["family_winners"]
    secondaries = round1_selection["family_secondaries"]

    def lookup(name: Optional[str]) -> Dict[str, object]:
        if not name:
            return {}
        return dict(override_map.get(name, {}))

    g = lookup(winners.get("G"))
    p = lookup(winners.get("P"))
    a = lookup(winners.get("A"))
    b = lookup(winners.get("B"))
    g2 = lookup(secondaries.get("G"))
    p2 = lookup(secondaries.get("P"))
    a2 = lookup(secondaries.get("A"))

    raw = [
        ("r2_00_baseline", {}),
        ("r2_01_G", merge_bph_overrides([g])),
        ("r2_02_G_P", merge_bph_overrides([g, p])),
        ("r2_03_G_A", merge_bph_overrides([g, a])),
        ("r2_04_G_P_A", merge_bph_overrides([g, p, a])),
        ("r2_05_G_P_A_B", merge_bph_overrides([g, p, a, b])),
        ("r2_06_G2_P_A_B", merge_bph_overrides([g2, p, a, b])),
        ("r2_07_G_P2_A_B", merge_bph_overrides([g, p2, a, b])),
        ("r2_08_G_P_A2_B", merge_bph_overrides([g, p, a2, b])),
    ]

    defs: List[Dict[str, object]] = []
    seen = set()
    for name, params in raw:
        key = json.dumps(params, sort_keys=True, ensure_ascii=False)
        if key in seen:
            continue
        seen.add(key)
        defs.append({"name": name, "family": None, "bph": params})
    return defs


def save_selection_csv(path: Path, rows: Sequence[Dict[str, object]]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def pick_top_methods(rows: Sequence[Dict[str, object]], count: int, require_qualified: bool) -> List[str]:
    chosen: List[str] = []
    for row in rows:
        if require_qualified and not row.get("qualified"):
            continue
        chosen.append(str(row["method"]))
        if len(chosen) >= count:
            break
    return chosen


def pick_top_nonbaseline_methods(
    rows: Sequence[Dict[str, object]],
    baseline_name: str,
    count: int,
    require_qualified: bool,
) -> List[str]:
    chosen: List[str] = []
    for row in rows:
        if require_qualified and not row.get("qualified"):
            continue
        method_name = str(row["method"])
        if method_name == baseline_name:
            continue
        chosen.append(method_name)
        if len(chosen) >= count:
            break
    return chosen


def run_smoke(
    original_dir: Path,
    explore_manifest: Path,
    fixed_downstream: Dict[str, object],
    smoke_count: int,
) -> None:
    smoke_dir = ensure_dir(OUTPUT_ROOT / "smoke")
    candidates = [
        {"name": "bph00_baseline", "family": None, "bph": {}},
        {"name": "bph10_gp_strict", "family": "G", "bph": {"gray_s_thr": 12, "lum_low": 0.12, "lum_high": 0.88}},
    ]
    candidate_files = write_candidate_files(smoke_dir, candidates, fixed_downstream)
    run_candidates(smoke_dir / "runs", explore_manifest, candidate_files, original_dir, limit=smoke_count)


def run_round1(
    original_dir: Path,
    explore_manifest: Path,
    fixed_downstream: Dict[str, object],
    skip_diagnostics: bool,
    diag_count: int,
    seed: int,
) -> Dict[str, object]:
    round_dir = ensure_dir(OUTPUT_ROOT / "round1")
    candidate_defs = round1_candidate_defs()
    candidate_files = write_candidate_files(round_dir, candidate_defs, fixed_downstream)
    run_candidates(round_dir / "runs", explore_manifest, candidate_files, original_dir)

    summary_json = evaluate_methods(round_dir / "runs", explore_manifest, round_dir / "eval", original_dir)
    score_csv = score_methods(summary_json, "bph00_baseline", round_dir / "eval" / "composite_scores.csv")
    summary = load_summary(summary_json)
    score_rows = load_scores(score_csv)
    guarded = qualified_rows(score_rows, summary, "bph00_baseline", max_ms_ssim_drop=0.015, max_psnr_drop=0.20)
    save_selection_csv(round_dir / "eval" / "guardrail_scores.csv", guarded)

    family_lists = select_family_best(guarded, candidate_defs)
    family_winners = {family: (names[0] if names else None) for family, names in family_lists.items()}
    family_secondaries = {family: (names[1] if len(names) > 1 else None) for family, names in family_lists.items()}

    diag_methods = pick_top_methods(guarded, count=4, require_qualified=False)
    if not skip_diagnostics and diag_methods:
        methods = [(name, round_dir / "runs" / name / "png" / "Final") for name in diag_methods]
        run_visual_diagnostics(
            round_dir / "diagnostics",
            explore_manifest,
            original_dir,
            sample_count=diag_count,
            seed=seed,
            methods=methods,
        )

    selection = {
        "created_at": now_iso(),
        "baseline_method": "bph00_baseline",
        "summary_json": str(summary_json),
        "score_csv": str(score_csv),
        "guardrail_csv": str(round_dir / "eval" / "guardrail_scores.csv"),
        "family_winners": family_winners,
        "family_secondaries": family_secondaries,
        "diagnostic_methods": diag_methods,
    }
    write_json(round_dir / "selection.json", selection)
    return selection


def run_round2(
    original_dir: Path,
    explore_manifest: Path,
    fixed_downstream: Dict[str, object],
    round1_selection: Dict[str, object],
    skip_diagnostics: bool,
    diag_count: int,
    seed: int,
) -> Dict[str, object]:
    round_dir = ensure_dir(OUTPUT_ROOT / "round2")
    candidate_defs = round2_candidate_defs(round1_selection, round1_candidate_defs())
    candidate_files = write_candidate_files(round_dir, candidate_defs, fixed_downstream)
    run_candidates(round_dir / "runs", explore_manifest, candidate_files, original_dir)

    summary_json = evaluate_methods(round_dir / "runs", explore_manifest, round_dir / "eval", original_dir)
    score_csv = score_methods(summary_json, "r2_00_baseline", round_dir / "eval" / "composite_scores.csv")
    summary = load_summary(summary_json)
    score_rows = load_scores(score_csv)
    guarded = qualified_rows(score_rows, summary, "r2_00_baseline", max_ms_ssim_drop=0.015, max_psnr_drop=0.20)
    save_selection_csv(round_dir / "eval" / "guardrail_scores.csv", guarded)

    top3 = pick_top_nonbaseline_methods(
        guarded,
        baseline_name="r2_00_baseline",
        count=3,
        require_qualified=True,
    )
    diag_methods = ["r2_00_baseline", *top3]
    if not skip_diagnostics and diag_methods:
        methods = [(name, round_dir / "runs" / name / "png" / "Final") for name in diag_methods]
        run_visual_diagnostics(
            round_dir / "diagnostics",
            explore_manifest,
            original_dir,
            sample_count=diag_count,
            seed=seed,
            methods=methods,
        )

    selection = {
        "created_at": now_iso(),
        "baseline_method": "r2_00_baseline",
        "summary_json": str(summary_json),
        "score_csv": str(score_csv),
        "guardrail_csv": str(round_dir / "eval" / "guardrail_scores.csv"),
        "full506_candidates": top3,
        "diagnostic_methods": diag_methods,
    }
    write_json(round_dir / "selection.json", selection)
    return selection


def run_full506(
    original_dir: Path,
    full_manifest: Path,
    fixed_downstream: Dict[str, object],
    round2_selection: Dict[str, object],
    skip_diagnostics: bool,
    diag_count: int,
    seed: int,
) -> Dict[str, object]:
    round2_dir = OUTPUT_ROOT / "round2"
    full_dir = ensure_dir(OUTPUT_ROOT / "full506")
    dynamic_guardrail_policy = {
        "score_bonus_scale": 0.30,
        "max_ms_ssim_bonus": 0.005,
        "max_psnr_bonus": 0.05,
    }
    candidate_names = ["r2_00_baseline", *list(round2_selection.get("full506_candidates", []))]
    candidate_names = list(dict.fromkeys(candidate_names))
    if len(candidate_names) <= 1:
        raise RuntimeError("No qualified round2 candidates available for full506.")

    round2_defs = round2_candidate_defs(read_json(OUTPUT_ROOT / "round1" / "selection.json"), round1_candidate_defs())
    by_name = {str(item["name"]): item for item in round2_defs}
    candidate_defs = [by_name[name] for name in candidate_names]
    candidate_files = write_candidate_files(full_dir, candidate_defs, fixed_downstream)
    run_candidates(full_dir / "runs", full_manifest, candidate_files, original_dir)

    summary_json = evaluate_methods(full_dir / "runs", full_manifest, full_dir / "eval", original_dir)
    score_csv = score_methods(summary_json, "r2_00_baseline", full_dir / "eval" / "composite_scores.csv")
    summary = load_summary(summary_json)
    score_rows = load_scores(score_csv)
    guarded = qualified_rows(
        score_rows,
        summary,
        "r2_00_baseline",
        max_ms_ssim_drop=0.02,
        max_psnr_drop=0.20,
        dynamic_relaxation=dynamic_guardrail_policy,
    )
    save_selection_csv(full_dir / "eval" / "guardrail_scores.csv", guarded)

    metric_winner: Optional[str] = None
    for row in guarded:
        name = str(row["method"])
        if name == "r2_00_baseline":
            continue
        if row.get("qualified"):
            metric_winner = name
            break

    selection = {
        "created_at": now_iso(),
        "baseline_method": "r2_00_baseline",
        "summary_json": str(summary_json),
        "score_csv": str(score_csv),
        "guardrail_csv": str(full_dir / "eval" / "guardrail_scores.csv"),
        "guardrail_policy": {
            "mode": "dynamic_relaxed_full506_v1",
            "base_ms_ssim_drop": 0.02,
            "base_psnr_drop": 0.20,
            **dynamic_guardrail_policy,
        },
        "metric_winner": metric_winner,
        "manual_color_review_required": True,
        "winner_locked": False,
    }

    if not skip_diagnostics:
        methods = [(name, full_dir / "runs" / name / "png" / "Final") for name in candidate_names]
        run_visual_diagnostics(
            full_dir / "diagnostics",
            full_manifest,
            original_dir,
            sample_count=diag_count,
            seed=seed,
            methods=methods,
        )
    write_json(full_dir / "selection.json", selection)
    return selection


def main() -> int:
    args = parse_args()
    original_dir = resolve_project_path(args.original_dir)
    explore_manifest = resolve_project_path(args.explore_manifest)
    full_manifest = resolve_project_path(args.full_manifest)
    base_config = resolve_project_path(args.base_config)
    ensure_dir(OUTPUT_ROOT)

    fixed_downstream = load_fixed_downstream(base_config)
    build_explore_manifest(
        original_dir=original_dir,
        manifest_path=explore_manifest,
        stats_csv_path=OUTPUT_ROOT / "explore64_manifest_stats.csv",
        count=args.explore_count,
        seed=args.seed,
        force=args.force_manifest,
    )

    if args.stage == "build-manifest":
        return 0

    if args.stage in {"smoke", "all"}:
        run_smoke(original_dir, explore_manifest, fixed_downstream, args.smoke_count)

    round1_selection: Optional[Dict[str, object]] = None
    if args.stage in {"round1", "round2", "full506", "all"}:
        selection_path = OUTPUT_ROOT / "round1" / "selection.json"
        if args.stage in {"round2", "full506"} and selection_path.exists():
            round1_selection = read_json(selection_path)
        else:
            round1_selection = run_round1(
                original_dir,
                explore_manifest,
                fixed_downstream,
                skip_diagnostics=args.skip_diagnostics,
                diag_count=args.diag_round1,
                seed=args.seed,
            )

    round2_selection: Optional[Dict[str, object]] = None
    if args.stage in {"round2", "full506", "all"}:
        selection_path = OUTPUT_ROOT / "round2" / "selection.json"
        if args.stage == "full506" and selection_path.exists():
            round2_selection = read_json(selection_path)
        else:
            if round1_selection is None:
                raise RuntimeError("Round1 selection missing.")
            round2_selection = run_round2(
                original_dir,
                explore_manifest,
                fixed_downstream,
                round1_selection,
                skip_diagnostics=args.skip_diagnostics,
                diag_count=args.diag_round2,
                seed=args.seed + 1,
            )

    if args.stage in {"full506", "all"}:
        if round2_selection is None:
            raise RuntimeError("Round2 selection missing.")
        run_full506(
            original_dir,
            full_manifest,
            fixed_downstream,
            round2_selection,
            skip_diagnostics=args.skip_diagnostics,
            diag_count=args.diag_round2,
            seed=args.seed + 2,
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
