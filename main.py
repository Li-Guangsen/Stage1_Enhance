"""Main entry for the seven-stage underwater enhancement pipeline.

当前主流程顺序固定为：

`Original -> BPH -> IMF1Ray -> RGHS -> CLAHE -> Fused -> Final`

可以把它理解成三层结构：

- `BPH`：先把颜色失衡压回相对稳定的起点
- `IMF1Ray / RGHS / CLAHE`：分别生成高频细节、主体对比、局部可见性三条分支
- `Fused / Final`：先做分支职责融合，再做最后的亮度收口
"""

import argparse
import json
import os
from pathlib import Path
import cv2
import numpy as np
from pybemd import imf1Ray_from_bgr
from wb_safe_contrast import wb_safe_contrast
from clahe_guided_visibility import clahe_3ch_wb_safe
from fusion_three import fuse_three_images_bgr
from lvbo import Gaussian_lvbo, entropy_boost_Lab
from lgsbph import lgs_accc_bgr_improved
from stage1_full_flow_mainline import (
    is_full_flow_mainline_mode,
    run_full_flow_downstream_stage1_mainline,
)
from stage1_e01_task_guided_family import (
    is_e01_task_guided_mode,
    run_e01_task_guided_family,
)
from stage1_downstream_candidates import _final_source_requirements, run_downstream_final_mode


STAGE_DIRS = ["BPH", "IMF1Ray", "RGHS", "CLAHE", "Fused", "Final"]
IMAGE_EXTS = (".jpg", ".png", ".jpeg", ".bmp", ".tif", ".tiff", ".webp")


def ensure_output_dirs(results_dir):
    for fmt in ["jpg", "png"]:
        fmt_root = os.path.join(results_dir, fmt)
        os.makedirs(fmt_root, exist_ok=True)
        for stage in STAGE_DIRS:
            os.makedirs(os.path.join(fmt_root, stage), exist_ok=True)


def _read_bgr(path):
    data = np.fromfile(str(path), dtype=np.uint8)
    img = cv2.imdecode(data, cv2.IMREAD_COLOR)
    if img is None:
        raise RuntimeError(f"cv2.imdecode 失败: {path}")
    return img


def _write_image(path, img_uint8):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    ok, encoded = cv2.imencode(path.suffix, img_uint8)
    if not ok:
        raise RuntimeError(f"cv2.imencode 失败: {path}")
    encoded.tofile(str(path))


def _result_variant_path(results_dir, fmt, stage_name, src_rel_path):
    src_rel = Path(src_rel_path)
    stem_path = src_rel.with_suffix("")
    stage_root = Path(results_dir) / fmt / stage_name
    if stem_path.parent != Path("."):
        stage_root = stage_root / stem_path.parent
    return stage_root / f"{stem_path.name}_{stage_name}.{fmt}"


def save_result_variants(img_uint8, results_dir, stage_name, src_rel_path):
    jpg_path = _result_variant_path(results_dir, "jpg", stage_name, src_rel_path)
    _write_image(jpg_path, img_uint8)

    png_path = _result_variant_path(results_dir, "png", stage_name, src_rel_path)
    _write_image(png_path, img_uint8)


def _project_path(path_text, base_dir):
    path = Path(path_text)
    if path.is_absolute():
        return path
    return Path(base_dir) / path


def _read_manifest(manifest_path):
    items = []
    seen = set()
    with open(manifest_path, "r", encoding="utf-8") as f:
        for line in f:
            item = line.strip().lstrip("\ufeff")
            if not item or item.startswith("#"):
                continue
            token = item
            if len(token) >= 2 and token[0] == token[-1] and token[0] in {"'", '"'}:
                token = token[1:-1]
            if token and token not in seen:
                items.append(token)
                seen.add(token)
    return items


def _strip_stage_suffix(stem):
    for suffix in STAGE_DIRS:
        tag = f"_{suffix}"
        if stem.lower().endswith(tag.lower()):
            return stem[: -len(tag)]
    return stem


def _list_inputs(input_dir, manifest_path=None, limit=None):
    input_root = Path(input_dir)
    files = [p for p in input_root.iterdir() if p.is_file() and p.suffix.lower() in IMAGE_EXTS]
    by_stem = {p.stem: p for p in files}
    by_name = {p.name: p for p in files}
    if manifest_path:
        names = _read_manifest(manifest_path)
        selected = []
        missing = []
        recursive_files = [p for p in input_root.rglob("*") if p.is_file() and p.suffix.lower() in IMAGE_EXTS]
        recursive_by_name = {p.name: p for p in recursive_files}
        recursive_by_stem = {p.stem: p for p in recursive_files}
        for item in names:
            manifest_item = Path(item)
            path = None
            if manifest_item.suffix.lower() in IMAGE_EXTS:
                relative_candidate = input_root / manifest_item
                if relative_candidate.is_file():
                    path = relative_candidate
                else:
                    path = by_name.get(manifest_item.name) or recursive_by_name.get(manifest_item.name)
            else:
                stem = _strip_stage_suffix(manifest_item.name)
                path = by_stem.get(stem) or recursive_by_stem.get(stem)
            if path is None:
                missing.append(item)
            else:
                selected.append(path)
        if missing:
            print(f"[WARN] manifest 中有 {len(missing)} 个样本在输入目录中找不到，前 5 个: {missing[:5]}")
    else:
        selected = sorted(files, key=lambda p: p.name.lower())
    if limit is not None and limit > 0:
        selected = selected[:limit]
    return selected


def _load_params(params_json):
    """Load stage-parameter overrides from a JSON file.

    约定的顶层 key 及其消费位置如下：

    - `bph` -> `lgs_accc_bgr_improved`
    - `imf1ray` -> `imf1Ray_from_bgr`
    - `rghs` -> `wb_safe_contrast`
    - `clahe` -> `clahe_3ch_wb_safe`
    - `fusion` -> `fuse_three_images_bgr`
    - `final` -> `_final_refine`

    额外说明：

    - `imf1ray` 会先以 `{"aggressive": True}` 作为默认基线，再叠加 JSON 中的覆写值
    - `final.mode` 当前支持：`homomorphic` / `entropy` / `homomorphic_entropy` /
      `none` / `original` / `bph` / `edge_preserve_blend` /
      `generic_luma_clahe` / `generic_luma_gamma` /
      `edge_safe_gamma_bph` / `boundary_aware_luma_bph` /
      `microstructure_csp_bph` /
      `topology_guarded_microfusion_bph` /
      `topology_pruned_microfusion_bph` /
      `endpoint_stabilized_weak_boundary_bph` /
      `ac_guarded_weak_boundary_bph` /
      `dual_anchor_false_edge_floor_bph` /
      `raw_detail_lowfreq_chroma_bph` /
      `e01_a_color_illumination_task_guided_v1` /
      `e01_b_wavelet_pyramid_weak_boundary_v1` /
      `full_flow_downstream_stage1_mainline_v1` /
      `full_flow_downstream_stage1_mainline_v2` /
      `topology_locked_visual_chroma_full_flow_v1` /
      `degradation_aware_pyramid_frequency_bph` /
      `weak_boundary_pyramid_fusion_bph`
    - `pipeline.save_intermediate_stages=false` 可用于只输出 `Final` 的诊断变体
    - JSON 中省略某个 stage key，表示该阶段使用代码默认参数
    - 未被主流程消费的顶层 key 当前会被忽略，不参与运行
    """
    if not params_json:
        return {}
    with open(params_json, "r", encoding="utf-8") as f:
        return json.load(f)



def _final_refine(fused_uint8, final_params, original_uint8=None, bph_uint8=None):
    """Dispatch the configured `Final` refinement mode."""
    params = dict(final_params or {})
    enabled = bool(params.pop("enabled", True))
    if not enabled:
        return fused_uint8
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
    if mode == "original":
        if original_uint8 is None:
            raise ValueError("final mode `original` requires original_uint8")
        return original_uint8
    if mode == "bph":
        if bph_uint8 is None:
            raise ValueError("final mode `bph` requires bph_uint8")
        return bph_uint8
    downstream_result = run_downstream_final_mode(
        mode,
        fused_uint8,
        original_uint8=original_uint8,
        bph_uint8=bph_uint8,
        **params,
    )
    if downstream_result is not None:
        return downstream_result
    raise ValueError(f"未知 final mode: {mode}")


def _relative_to_root(path, root):
    try:
        return path.relative_to(root)
    except ValueError:
        return Path(path.name)


def process_one_image(img_path, results_dir, params, resize_to=(320, 320), skip_existing=False, input_root=None):
    """Run the full seven-stage pipeline for one image and write stage artifacts.

    当前阶段参数在主流程里的接线关系是：

    - `bph` 先作用在原图，生成所有下游共享的白平衡起点
    - `imf1ray / rghs / clahe` 都从 `bph_bgr` 出发，各自生成分支图
    - `fusion` 只负责把三条分支合成为 `Fused`
    - `final` 只负责把 `Fused` 收口为 `Final`
    """
    img_path = Path(img_path)
    input_root = Path(input_root) if input_root is not None else img_path.parent
    src_rel_path = _relative_to_root(img_path, input_root)
    name = img_path.name
    stem = img_path.stem
    final_png = _result_variant_path(results_dir, "png", "Final", src_rel_path)
    if skip_existing and final_png.exists():
        print(f"[SKIP] 已存在 Final PNG: {name}")
        return

    img_bgr = _read_bgr(img_path)

    print(f"[INFO] 原始尺寸 {name}: {img_bgr.shape}")
    if resize_to is not None:
        w, h = resize_to
        if img_bgr.shape[0] != h or img_bgr.shape[1] != w:
            img_bgr = cv2.resize(img_bgr, (w, h), cv2.INTER_CUBIC)

    original_uint8 = img_bgr.copy()
    img = img_bgr.astype(np.float32) / 255.0
    print("正在处理:", name)

    final_params = params.get("final", {})
    pipeline_params = params.get("pipeline", {})
    save_intermediate_stages = bool(pipeline_params.get("save_intermediate_stages", True))
    final_mode = str(final_params.get("mode", "homomorphic"))
    if is_full_flow_mainline_mode(final_mode) or is_e01_task_guided_mode(final_mode):
        requirements = {"bph": True, "fused": False}
    else:
        requirements = _final_source_requirements(final_params)
    need_bph = save_intermediate_stages or requirements["bph"] or requirements["fused"]
    need_fused = save_intermediate_stages or requirements["fused"]

    bph_bgr = None
    bph_uint8 = None
    if need_bph:
        bph_bgr = lgs_accc_bgr_improved(img, **params.get("bph", {}))
        bph_uint8 = np.clip(bph_bgr * 255, 0, 255).astype(np.uint8)
        if save_intermediate_stages:
            save_result_variants(bph_uint8, results_dir, "BPH", src_rel_path)
        print("白平衡完成")

    if is_full_flow_mainline_mode(final_mode):
        full_flow_params = dict(final_params)
        full_flow_params.pop("mode", None)
        full_flow_params.pop("enabled", None)
        full_flow_params["_mode"] = final_mode
        full_flow_stages = run_full_flow_downstream_stage1_mainline(
            original_uint8,
            bph_uint8=bph_uint8,
            imf1ray_params=params.get("imf1ray", {}),
            rghs_params=params.get("rghs", {}),
            clahe_params=params.get("clahe", {}),
            fusion_params=params.get("fusion", {}),
            full_flow_params=full_flow_params,
        )
        if save_intermediate_stages:
            for stage_name in ["IMF1Ray", "RGHS", "CLAHE", "Fused"]:
                save_result_variants(full_flow_stages[stage_name], results_dir, stage_name, src_rel_path)
                print(f"{stage_name} full-flow stage 完成")
        save_result_variants(full_flow_stages["Final"], results_dir, "Final", src_rel_path)
        print("增强完成:", stem + "_Final")
        return

    if is_e01_task_guided_mode(final_mode):
        e01_params = dict(final_params)
        e01_params["_mode"] = final_mode
        e01_stages = run_e01_task_guided_family(
            original_uint8,
            bph_uint8=bph_uint8,
            e01_params=e01_params,
        )
        if save_intermediate_stages:
            for stage_name in ["IMF1Ray", "RGHS", "CLAHE", "Fused"]:
                save_result_variants(e01_stages[stage_name], results_dir, stage_name, src_rel_path)
                print(f"{stage_name} E01 stage 完成")
        save_result_variants(e01_stages["Final"], results_dir, "Final", src_rel_path)
        print("增强完成:", stem + "_Final")
        return

    fused_uint8 = original_uint8
    if need_fused:
        imf_params = {"aggressive": True}
        imf_params.update(params.get("imf1ray", {}))
        imf1_bgr = imf1Ray_from_bgr(bph_bgr, **imf_params)
        imf1_uint8 = np.clip(imf1_bgr * 255, 0, 255).astype(np.uint8)
        if save_intermediate_stages:
            save_result_variants(imf1_uint8, results_dir, "IMF1Ray", src_rel_path)
        print("IMF1 Rayleigh 增强完成")

        rghs_bgr = wb_safe_contrast(bph_bgr, **params.get("rghs", {}))
        rghs_uint8 = np.clip(rghs_bgr * 255, 0, 255).astype(np.uint8)
        if save_intermediate_stages:
            save_result_variants(rghs_uint8, results_dir, "RGHS", src_rel_path)
        print("RGHS 增强完成")

        clahe_bgr = clahe_3ch_wb_safe(bph_bgr, **params.get("clahe", {}))
        clahe_uint8 = np.clip(clahe_bgr * 255, 0, 255).astype(np.uint8)
        if save_intermediate_stages:
            save_result_variants(clahe_uint8, results_dir, "CLAHE", src_rel_path)
        print("CLAHE 增强完成")

        fused_bgr = fuse_three_images_bgr(imf1_bgr, rghs_bgr, clahe_bgr, **params.get("fusion", {}))
        fused_uint8 = np.clip(fused_bgr * 255, 0, 255).astype(np.uint8)
        if save_intermediate_stages:
            save_result_variants(fused_uint8, results_dir, "Fused", src_rel_path)
        print("融合完成:", stem + "_Fused")

    final_uint8 = _final_refine(
        fused_uint8,
        final_params,
        original_uint8=original_uint8,
        bph_uint8=bph_uint8,
    )
    save_result_variants(final_uint8, results_dir, "Final", src_rel_path)
    print("增强完成:", stem + "_Final")


def parse_args():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    default_params_json = os.path.join(
        base_dir,
        "experiments",
        "optimization_v1",
        "configs",
        "best_full506_r4_03.json",
    )
    parser = argparse.ArgumentParser(description="Stage1Codex underwater algae enhancement pipeline")
    parser.add_argument("--input-dir", default=os.path.join(base_dir, "data", "inputImg", "Original"))
    parser.add_argument("--output-dir", default=os.path.join(base_dir, "results"))
    parser.add_argument("--manifest", default=None)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--params-json", default=default_params_json)
    parser.add_argument("--skip-existing", action="store_true")
    parser.add_argument("--resize-to", nargs=2, type=int, default=(320, 320), metavar=("WIDTH", "HEIGHT"))
    parser.add_argument("--no-resize", action="store_true")
    return parser.parse_args()


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    args = parse_args()
    input_dir = _project_path(args.input_dir, base_dir)
    output_dir = _project_path(args.output_dir, base_dir)
    manifest = _project_path(args.manifest, base_dir) if args.manifest else None
    params_json = _project_path(args.params_json, base_dir) if args.params_json else None
    resize_to = None if args.no_resize else tuple(args.resize_to)

    os.makedirs(output_dir, exist_ok=True)
    ensure_output_dirs(output_dir)
    params = _load_params(params_json)

    img_paths = _list_inputs(input_dir, manifest, args.limit)
    print(f"[INFO] 输入目录: {input_dir}")
    print(f"[INFO] 输出目录: {output_dir}")
    print(f"[INFO] 参数文件: {params_json if params_json else '内置默认参数'}")
    print(f"[INFO] 待处理图像数: {len(img_paths)}")

    for idx, img_path in enumerate(img_paths, start=1):
        print(f"\n[{idx}/{len(img_paths)}]")
        process_one_image(
            img_path,
            output_dir,
            params,
            resize_to=resize_to,
            skip_existing=args.skip_existing,
            input_root=input_dir,
        )


if __name__ == "__main__":
    main()

