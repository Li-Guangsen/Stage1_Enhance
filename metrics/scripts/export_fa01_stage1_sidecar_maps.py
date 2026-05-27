from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import cv2
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DEFAULT_STEMS = [
    "weixiaoyuanjia.26",
    "xuehong.9",
    "donghaiyuanjia.26",
    "tama.14",
    "jianci.4",
]

MAP_DEFINITIONS = {
    "topology_anchor_luma": "Raw Lab-L luma; keeps raw topology as the primary edge-distribution anchor.",
    "color_compensation_magnitude": "Robust-normalized Lab ab magnitude between BPH and raw; highlights where gray-pixel/BPH color formation acts.",
    "frequency_detail_evidence": "Robust-normalized absolute luma difference between IMF1Ray and BPH; captures IMF/frequency detail evidence.",
    "contrast_visibility_evidence": "Robust-normalized max luma change from RGHS/CLAHE against BPH; captures contrast and local-visibility evidence.",
    "fusion_luma_delta_risk": "Robust-normalized absolute luma difference between Final and raw; marks where direct replacement changes raw topology.",
    "background_false_edge_risk": "Final-gradient gain in weak raw-gradient regions, weighted by Final-vs-raw luma delta; flags possible new background edges.",
    "weak_boundary_support": "Frequency detail retained outside background-risk regions; sidecar signal for weak-boundary support.",
}


def read_csv_rows(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def read_bgr(path: Path) -> np.ndarray:
    img = cv2.imdecode(np.fromfile(str(path), dtype=np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError(f"Cannot decode image: {path}")
    return img


def write_image(path: Path, img: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    ok, encoded = cv2.imencode(path.suffix, img)
    if not ok:
        raise RuntimeError(f"Failed to encode image: {path}")
    encoded.tofile(str(path))


def resize_like(img: np.ndarray, ref: np.ndarray) -> np.ndarray:
    if img.shape[:2] == ref.shape[:2]:
        return img
    return cv2.resize(img, (ref.shape[1], ref.shape[0]), interpolation=cv2.INTER_AREA)


def lab_luma(img_bgr: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)[:, :, 0].astype(np.float32)


def lab_ab(img_bgr: np.ndarray) -> np.ndarray:
    lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB).astype(np.float32)
    return lab[:, :, 1:3] - 128.0


def robust_norm(values: np.ndarray, high_percentile: float = 99.0) -> np.ndarray:
    arr = np.nan_to_num(values.astype(np.float32), nan=0.0, posinf=0.0, neginf=0.0)
    arr = np.maximum(arr, 0.0)
    high = float(np.percentile(arr, high_percentile))
    if high <= 1e-6:
        return np.zeros_like(arr, dtype=np.float32)
    return np.clip(arr / high, 0.0, 1.0)


def to_u8(values: np.ndarray) -> np.ndarray:
    return np.clip(np.round(values * 255.0), 0, 255).astype(np.uint8)


def gradient_norm(luma: np.ndarray) -> np.ndarray:
    gx = cv2.Sobel(luma, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(luma, cv2.CV_32F, 0, 1, ksize=3)
    return robust_norm(cv2.magnitude(gx, gy), high_percentile=98.0)


def stage_path(stage_root: Path, stage: str, stem: str) -> Path:
    return stage_root / stage / f"{stem}_{stage}.png"


def raw_paths_by_stem(stage_paths_csv: Path) -> Dict[str, str]:
    paths: Dict[str, str] = {}
    for row in read_csv_rows(stage_paths_csv):
        paths.setdefault(row["stem"], row.get("raw_path", ""))
    return paths


def add_label(img: np.ndarray, label: str) -> np.ndarray:
    out = img.copy()
    cv2.rectangle(out, (0, 0), (out.shape[1], 24), (0, 0, 0), thickness=-1)
    cv2.putText(out, label[:28], (6, 17), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1, cv2.LINE_AA)
    return out


def tile_image(img: np.ndarray, size: Tuple[int, int]) -> np.ndarray:
    w, h = size
    if img.ndim == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    ih, iw = img.shape[:2]
    scale = min(w / iw, h / ih)
    nw = max(1, int(round(iw * scale)))
    nh = max(1, int(round(ih * scale)))
    resized = cv2.resize(img, (nw, nh), interpolation=cv2.INTER_AREA)
    canvas = np.full((h, w, 3), 245, dtype=np.uint8)
    y0 = (h - nh) // 2
    x0 = (w - nw) // 2
    canvas[y0 : y0 + nh, x0 : x0 + nw] = resized
    return canvas


def make_panel(path: Path, stem: str, raw: np.ndarray, final: np.ndarray, maps: Dict[str, np.ndarray]) -> None:
    tile_size = (210, 160)
    items = [
        ("Raw", raw),
        ("FF02 Final", final),
        ("Raw luma", maps["topology_anchor_luma"]),
        ("Color comp", maps["color_compensation_magnitude"]),
        ("Freq detail", maps["frequency_detail_evidence"]),
        ("Visibility", maps["contrast_visibility_evidence"]),
        ("Luma risk", maps["fusion_luma_delta_risk"]),
        ("False-edge risk", maps["background_false_edge_risk"]),
        ("Weak-boundary", maps["weak_boundary_support"]),
    ]
    tiles = [add_label(tile_image(img, tile_size), label) for label, img in items]
    rows = [np.hstack(tiles[:3]), np.hstack(tiles[3:6]), np.hstack(tiles[6:9])]
    header = np.full((36, rows[0].shape[1], 3), 35, dtype=np.uint8)
    cv2.putText(header, f"{stem} sidecar smoke", (8, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.64, (255, 255, 255), 2, cv2.LINE_AA)
    panel = np.vstack([header, *rows])
    write_image(path, panel)


def build_maps(raw: np.ndarray, stages: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
    bph = stages["BPH"]
    imf = stages["IMF1Ray"]
    rghs = stages["RGHS"]
    clahe = stages["CLAHE"]
    final = stages["Final"]

    raw_l = lab_luma(raw)
    bph_l = lab_luma(bph)
    imf_l = lab_luma(imf)
    rghs_l = lab_luma(rghs)
    clahe_l = lab_luma(clahe)
    final_l = lab_luma(final)

    color_comp = robust_norm(np.linalg.norm(lab_ab(bph) - lab_ab(raw), axis=2), high_percentile=99.0)
    freq_detail = robust_norm(np.abs(imf_l - bph_l), high_percentile=99.0)
    visibility = robust_norm(np.maximum(np.abs(rghs_l - bph_l), np.abs(clahe_l - bph_l)), high_percentile=99.0)
    luma_delta = robust_norm(np.abs(final_l - raw_l), high_percentile=99.0)
    raw_grad = gradient_norm(raw_l)
    final_grad = gradient_norm(final_l)
    background_risk = np.clip(final_grad * (1.0 - raw_grad) * np.maximum(luma_delta, 0.35 * freq_detail), 0.0, 1.0)
    weak_support = np.clip(freq_detail * (1.0 - background_risk) * (0.35 + 0.65 * visibility), 0.0, 1.0)

    return {
        "topology_anchor_luma": raw_l.astype(np.uint8),
        "color_compensation_magnitude": to_u8(color_comp),
        "frequency_detail_evidence": to_u8(freq_detail),
        "contrast_visibility_evidence": to_u8(visibility),
        "fusion_luma_delta_risk": to_u8(luma_delta),
        "background_false_edge_risk": to_u8(background_risk),
        "weak_boundary_support": to_u8(weak_support),
    }


def export_stem(stem: str, raw_path: Path, stage_root: Path, output_dir: Path) -> Dict[str, object]:
    raw = read_bgr(raw_path)
    stages: Dict[str, np.ndarray] = {}
    source_paths: Dict[str, str] = {"raw": str(raw_path)}
    for stage in ["BPH", "IMF1Ray", "RGHS", "CLAHE", "Final"]:
        path = stage_path(stage_root, stage, stem)
        stages[stage] = resize_like(read_bgr(path), raw)
        source_paths[stage] = str(path)

    maps = build_maps(raw, stages)
    stem_dir = output_dir / "maps" / stem
    map_paths: Dict[str, str] = {}
    for name, img in maps.items():
        out_path = stem_dir / f"{stem}_{name}.png"
        write_image(out_path, img)
        map_paths[name] = str(out_path.relative_to(PROJECT_ROOT)).replace("\\", "/")

    panel_path = output_dir / "panels" / f"{stem}_sidecar_smoke_panel.jpg"
    make_panel(panel_path, stem, raw, stages["Final"], maps)
    metadata = {
        "stem": stem,
        "raw_path": str(raw_path),
        "stage_root": str(stage_root),
        "source_paths": source_paths,
        "map_paths": map_paths,
        "panel_path": str(panel_path.relative_to(PROJECT_ROOT)).replace("\\", "/"),
        "image_shape_hw": [int(raw.shape[0]), int(raw.shape[1])],
        "map_definitions": MAP_DEFINITIONS,
        "scope": "no-training sidecar export smoke; not a downstream detector result",
    }
    metadata_path = stem_dir / f"{stem}_sidecar_metadata.json"
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    metadata["metadata_path"] = str(metadata_path.relative_to(PROJECT_ROOT)).replace("\\", "/")
    return metadata


def write_manifest(path: Path, rows: Sequence[Dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "stem",
        "raw_path",
        "stage_root",
        "panel_path",
        "metadata_path",
        "topology_anchor_luma",
        "color_compensation_magnitude",
        "frequency_detail_evidence",
        "contrast_visibility_evidence",
        "fusion_luma_delta_risk",
        "background_false_edge_risk",
        "weak_boundary_support",
    ]
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            flat = {
                "stem": row["stem"],
                "raw_path": row["raw_path"],
                "stage_root": row["stage_root"],
                "panel_path": row["panel_path"],
                "metadata_path": row["metadata_path"],
            }
            flat.update(row["map_paths"])
            writer.writerow(flat)


def write_markdown(path: Path, index: Dict[str, object], rows: Sequence[Dict[str, object]]) -> None:
    lines: List[str] = []
    lines.append("# FA01 Stage1 sidecar map definition and no-training smoke\n")
    lines.append("日期：2026-05-27\n")
    lines.append("## 1. 定位\n")
    lines.append(
        "本文件把 Stage1 full-flow 从“直接替换 raw 的增强图”纠偏为“raw 主输入 + Stage1 sidecar evidence maps”的可执行入口。"
        "本次只导出 maps，不训练 detector，不改 checkpoint，不跑 MyEdge eval，也不声称 downstream positive。\n"
    )
    lines.append("## 2. Sidecar Maps\n")
    lines.append("| map | definition |")
    lines.append("|---|---|")
    for name, definition in MAP_DEFINITIONS.items():
        lines.append(f"| `{name}` | {definition} |")
    lines.append("\n## 3. No-training Smoke\n")
    lines.append(f"- stage root: `{index['stage_root']}`")
    lines.append(f"- generated stems: `{index['generated_count']}` / requested `{len(index['requested_stems'])}`")
    lines.append("- scope: sidecar export completeness only; no detector validation.")
    lines.append("\n| stem | panel | metadata |")
    lines.append("|---|---|---|")
    for row in rows:
        lines.append(f"| {row['stem']} | [panel]({row['panel_path']}) | [metadata]({row['metadata_path']}) |")
    lines.append("\n## 4. Decision Boundary\n")
    lines.append(
        "sidecar route 只有在 MyEdge/MSFI 侧建立独立 adaptation run sheet、raw-only adapted baseline、训练配置和 168 eval 后，"
        "才能讨论 downstream gain。当前 smoke 只证明：Stage1 的灰像素/BPH、IMF/frequency、RGHS/CLAHE visibility、fusion risk "
        "可以被稳定拆成可消费的 evidence/risk maps。"
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export FA01 Stage1 sidecar evidence maps without training.")
    parser.add_argument(
        "--stage-root",
        default="experiments/full_flow_downstream_stage1_mainline_v2/outputs/myedge168/full_flow_downstream_stage1_mainline_v2/png",
    )
    parser.add_argument(
        "--stage-paths-csv",
        default="docs/fa01_high_risk_sample_index_20260527/fa01_high_risk_stage1_paths.csv",
    )
    parser.add_argument("--output-dir", default="docs/fa01_stage1_sidecar_map_smoke_20260527")
    parser.add_argument("--stem", action="append", default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    stage_root = (PROJECT_ROOT / args.stage_root).resolve()
    stage_paths_csv = (PROJECT_ROOT / args.stage_paths_csv).resolve()
    output_dir = (PROJECT_ROOT / args.output_dir).resolve()
    stems = args.stem or DEFAULT_STEMS
    raw_lookup = raw_paths_by_stem(stage_paths_csv)

    rows: List[Dict[str, object]] = []
    failures: List[Dict[str, str]] = []
    for stem in stems:
        raw_text = raw_lookup.get(stem, "")
        try:
            if not raw_text:
                raise FileNotFoundError("raw path not found in stage paths CSV")
            rows.append(export_stem(stem, Path(raw_text), stage_root, output_dir))
        except Exception as exc:
            failures.append({"stem": stem, "error": str(exc)})

    write_manifest(output_dir / "fa01_stage1_sidecar_map_manifest.csv", rows)
    index = {
        "name": "fa01_stage1_sidecar_map_smoke_20260527",
        "date": "2026-05-27",
        "stage_root": str(stage_root.relative_to(PROJECT_ROOT)).replace("\\", "/"),
        "stage_paths_csv": str(stage_paths_csv.relative_to(PROJECT_ROOT)).replace("\\", "/"),
        "output_dir": str(output_dir.relative_to(PROJECT_ROOT)).replace("\\", "/"),
        "requested_stems": stems,
        "generated_count": len(rows),
        "failures": failures,
        "map_definitions": MAP_DEFINITIONS,
        "scope": "no-training sidecar export smoke; no detector run; no candidate gate",
    }
    (output_dir / "fa01_stage1_sidecar_map_smoke_index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    write_markdown(PROJECT_ROOT / "docs/stage1_sidecar_map_definition_fa01_20260527_cn.md", index, rows)
    print(json.dumps(index, ensure_ascii=False, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
