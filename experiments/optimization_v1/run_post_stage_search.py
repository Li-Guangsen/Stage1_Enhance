from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import cv2
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
METRICS_DIR = PROJECT_ROOT / "metrics"
if str(METRICS_DIR) not in sys.path:
    sys.path.insert(0, str(METRICS_DIR))

from fusion_three import fuse_three_images_bgr
from lvbo import Gaussian_lvbo, entropy_boost_Lab
from metrics.protocol_common import (
    build_image_index,
    read_bgr,
    read_manifest,
    resolve_project_path,
    safe_output_stem,
    select_common_stems,
    write_image,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Search fusion/refinement candidates from existing stage PNGs.")
    parser.add_argument("--manifest", default="data/eval_subset_pilot92_v1.txt")
    parser.add_argument("--output-dir", default="experiments/optimization_v1/results/post_stage_search")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--bph-dir", default="results/png/BPH")
    parser.add_argument("--imf1-dir", default="results/png/IMF1Ray")
    parser.add_argument("--rghs-dir", default="results/png/RGHS")
    parser.add_argument("--clahe-dir", default="results/png/CLAHE")
    parser.add_argument(
        "--candidates-json",
        default=None,
        help="Optional JSON file with a list of candidate configs. Uses built-in coarse candidates if omitted.",
    )
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args()


def candidates() -> List[Dict[str, object]]:
    return [
        {"name": "c00_current", "fusion": {}, "final": {"mode": "homomorphic"}},
        {"name": "c01_fused_only", "fusion": {}, "final": {"mode": "none"}},
        {
            "name": "c02_homo_mild",
            "fusion": {},
            "final": {"mode": "homomorphic", "gamma_low": 0.60, "gamma_high": 1.55, "cutoff_freq": 75},
        },
        {
            "name": "c03_homo_strong",
            "fusion": {},
            "final": {"mode": "homomorphic", "gamma_low": 0.45, "gamma_high": 2.05, "cutoff_freq": 55},
        },
        {
            "name": "c04_entropy_final",
            "fusion": {},
            "final": {
                "mode": "entropy",
                "p_low": 0.8,
                "p_high": 99.2,
                "clahe_clip": 1.5,
                "mix_global": 0.55,
                "mix_local": 0.35,
                "chroma_gain": 1.04,
            },
        },
        {
            "name": "c05_homo_entropy",
            "fusion": {},
            "final": {
                "mode": "homomorphic_entropy",
                "gamma_low": 0.55,
                "gamma_high": 1.70,
                "cutoff_freq": 70,
                "entropy": {
                    "p_low": 1.0,
                    "p_high": 99.0,
                    "clahe_clip": 1.25,
                    "mix_global": 0.35,
                    "mix_local": 0.20,
                    "chroma_gain": 1.02,
                },
            },
        },
        {
            "name": "c10_more_rghs",
            "fusion": {"rghs_low_boost": 1.8, "rgh_fg_bias": 0.60, "post_sigmoid_alpha": 0.22},
            "final": {"mode": "homomorphic"},
        },
        {
            "name": "c11_more_clahe",
            "fusion": {"clahe_floor_mid": 0.18, "boost_clahe": 0.18, "post_sigmoid_alpha": 0.30},
            "final": {"mode": "homomorphic"},
        },
        {
            "name": "c12_more_imf",
            "fusion": {"boost_imf1": 0.12, "imf_detail_bias": 0.55, "level_gain_imf": 0.50},
            "final": {"mode": "homomorphic"},
        },
        {
            "name": "c13_higher_contrast",
            "fusion": {"post_stretch": [0.5, 99.5], "post_sigmoid_k": 1.35, "post_sigmoid_alpha": 0.35},
            "final": {"mode": "homomorphic"},
        },
        {
            "name": "c14_entropy_conserve",
            "fusion": {"post_stretch": [1.0, 99.0], "post_sigmoid_k": 1.10, "post_sigmoid_alpha": 0.12},
            "final": {"mode": "homomorphic"},
        },
        {
            "name": "c20_current_entropy_light",
            "fusion": {},
            "final": {
                "mode": "homomorphic_entropy",
                "gamma_low": 0.50,
                "gamma_high": 1.80,
                "cutoff_freq": 65,
                "entropy": {
                    "p_low": 1.2,
                    "p_high": 98.8,
                    "clahe_clip": 1.10,
                    "mix_global": 0.15,
                    "mix_local": 0.10,
                    "chroma_gain": 1.01,
                },
            },
        },
        {
            "name": "c21_current_entropy_mid",
            "fusion": {},
            "final": {
                "mode": "homomorphic_entropy",
                "gamma_low": 0.50,
                "gamma_high": 1.80,
                "cutoff_freq": 65,
                "entropy": {
                    "p_low": 1.0,
                    "p_high": 99.0,
                    "clahe_clip": 1.18,
                    "mix_global": 0.25,
                    "mix_local": 0.15,
                    "chroma_gain": 1.015,
                },
            },
        },
        {
            "name": "c22_homo_entropy_soft",
            "fusion": {},
            "final": {
                "mode": "homomorphic_entropy",
                "gamma_low": 0.58,
                "gamma_high": 1.62,
                "cutoff_freq": 78,
                "entropy": {
                    "p_low": 1.0,
                    "p_high": 99.0,
                    "clahe_clip": 1.18,
                    "mix_global": 0.25,
                    "mix_local": 0.15,
                    "chroma_gain": 1.015,
                },
            },
        },
        {
            "name": "c23_homo_entropy_balanced",
            "fusion": {},
            "final": {
                "mode": "homomorphic_entropy",
                "gamma_low": 0.52,
                "gamma_high": 1.72,
                "cutoff_freq": 72,
                "entropy": {
                    "p_low": 1.0,
                    "p_high": 99.0,
                    "clahe_clip": 1.22,
                    "mix_global": 0.30,
                    "mix_local": 0.18,
                    "chroma_gain": 1.02,
                },
            },
        },
        {
            "name": "c24_strong_entropy_light",
            "fusion": {},
            "final": {
                "mode": "homomorphic_entropy",
                "gamma_low": 0.45,
                "gamma_high": 2.00,
                "cutoff_freq": 58,
                "entropy": {
                    "p_low": 1.2,
                    "p_high": 98.8,
                    "clahe_clip": 1.10,
                    "mix_global": 0.12,
                    "mix_local": 0.08,
                    "chroma_gain": 1.01,
                },
            },
        },
        {
            "name": "c25_rghs_entropy_mid",
            "fusion": {"rghs_low_boost": 1.8, "rgh_fg_bias": 0.60, "post_sigmoid_alpha": 0.22},
            "final": {
                "mode": "homomorphic_entropy",
                "gamma_low": 0.50,
                "gamma_high": 1.80,
                "cutoff_freq": 65,
                "entropy": {
                    "p_low": 1.0,
                    "p_high": 99.0,
                    "clahe_clip": 1.18,
                    "mix_global": 0.25,
                    "mix_local": 0.15,
                    "chroma_gain": 1.015,
                },
            },
        },
    ]


def load_candidate_configs(path: Optional[str]) -> List[Dict[str, object]]:
    if not path:
        return candidates()
    candidate_path = resolve_project_path(path)
    configs = json.loads(candidate_path.read_text(encoding="utf-8"))
    if not isinstance(configs, list):
        raise ValueError(f"Candidate JSON must contain a list: {candidate_path}")
    seen = set()
    for idx, cfg in enumerate(configs, start=1):
        if not isinstance(cfg, dict):
            raise ValueError(f"Candidate #{idx} must be an object")
        name = cfg.get("name")
        if not name or not isinstance(name, str):
            raise ValueError(f"Candidate #{idx} has invalid name")
        if name in seen:
            raise ValueError(f"Duplicate candidate name: {name}")
        seen.add(name)
        cfg.setdefault("fusion", {})
        cfg.setdefault("final", {"mode": "homomorphic"})
    return configs


def to_float01(img_bgr: np.ndarray) -> np.ndarray:
    return np.clip(img_bgr.astype(np.float32) / 255.0, 0.0, 1.0)


def to_uint8(img01: np.ndarray) -> np.ndarray:
    return np.clip(np.round(img01 * 255.0), 0, 255).astype(np.uint8)


def apply_final(fused_uint8: np.ndarray, final_cfg: Dict[str, object]) -> np.ndarray:
    cfg = dict(final_cfg)
    mode = cfg.pop("mode", "homomorphic")
    if mode == "none":
        return fused_uint8
    if mode == "homomorphic":
        return Gaussian_lvbo(fused_uint8, **cfg)
    if mode == "entropy":
        return entropy_boost_Lab(fused_uint8, **cfg)
    if mode == "homomorphic_entropy":
        entropy_cfg = cfg.pop("entropy", {})
        first = Gaussian_lvbo(fused_uint8, **cfg)
        return entropy_boost_Lab(first, **entropy_cfg)
    raise ValueError(f"Unknown final mode: {mode}")


def load_stage_indexes(args: argparse.Namespace) -> Tuple[Dict[str, object], List[str]]:
    stage_dirs = {
        "BPH": resolve_project_path(args.bph_dir),
        "IMF1Ray": resolve_project_path(args.imf1_dir),
        "RGHS": resolve_project_path(args.rghs_dir),
        "CLAHE": resolve_project_path(args.clahe_dir),
    }
    indexes = {name: build_image_index(path, include_normalized_keys=True) for name, path in stage_dirs.items()}
    manifest = read_manifest(args.manifest)
    stems = list(manifest)
    for stage_name, index in indexes.items():
        missing = [stem for stem in stems if stem not in index.by_key]
        if missing:
            raise RuntimeError(f"{stage_name} missing {len(missing)} manifest images; first: {missing[:5]}")
    if args.limit is not None and args.limit > 0:
        stems = stems[: args.limit]
    return indexes, stems


def main() -> int:
    args = parse_args()
    output_dir = resolve_project_path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    indexes, stems = load_stage_indexes(args)
    configs = load_candidate_configs(args.candidates_json)

    for ci, cfg in enumerate(configs, start=1):
        name = str(cfg["name"])
        final_dir = output_dir / name / "Final"
        final_dir.mkdir(parents=True, exist_ok=True)
        print(f"[CANDIDATE] {ci}/{len(configs)} {name}")
        for i, stem in enumerate(stems, start=1):
            imf = to_float01(read_bgr(indexes["IMF1Ray"].by_key[stem]))
            rghs = to_float01(read_bgr(indexes["RGHS"].by_key[stem]))
            clahe = to_float01(read_bgr(indexes["CLAHE"].by_key[stem]))
            fused = fuse_three_images_bgr(imf, rghs, clahe, **dict(cfg.get("fusion", {})))
            fused_uint8 = to_uint8(fused)
            final_uint8 = apply_final(fused_uint8, dict(cfg.get("final", {})))
            out_name = f"{safe_output_stem(stem)}_Final.png"
            write_image(final_dir / out_name, final_uint8)
            if args.verbose or i == 1 or i == len(stems) or i % 10 == 0:
                print(f"[OK] {name} {i}/{len(stems)} {stem}")

    config_out = output_dir / "candidate_configs.json"
    config_out.write_text(json.dumps(configs, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[DONE] Wrote candidates to {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
