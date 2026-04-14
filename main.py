import argparse
import json
import os
from pathlib import Path
import cv2
import numpy as np
from pybemd import imf1Ray_from_bgr
from RGHS import wb_safe_contrast
from CLAHE import clahe_3ch_wb_safe
from fusion_three import fuse_three_images_bgr
from lvbo import Gaussian_lvbo, entropy_boost_Lab
from lgsbph import lgs_accc_bgr_improved


STAGE_DIRS = ["BPH", "IMF1Ray", "RGHS", "CLAHE", "Fused", "Final"]
IMAGE_EXTS = (".jpg", ".png", ".jpeg", ".bmp", ".tif", ".tiff")


def ensure_output_dirs(results_dir):
    for fmt in ["jpg", "png"]:
        fmt_root = os.path.join(results_dir, fmt)
        os.makedirs(fmt_root, exist_ok=True)
        for stage in STAGE_DIRS:
            os.makedirs(os.path.join(fmt_root, stage), exist_ok=True)


def save_result_variants(img_uint8, results_dir, stage_name, src_name):
    stem = os.path.splitext(src_name)[0]

    jpg_name = f"{stem}_{stage_name}.jpg"
    jpg_path = os.path.join(results_dir, "jpg", stage_name, jpg_name)
    cv2.imwrite(jpg_path, img_uint8)

    png_name = f"{stem}_{stage_name}.png"
    png_path = os.path.join(results_dir, "png", stage_name, png_name)
    cv2.imwrite(png_path, img_uint8)


def _project_path(path_text, base_dir):
    path = Path(path_text)
    if path.is_absolute():
        return path
    return Path(base_dir) / path


def _read_manifest(manifest_path):
    stems = []
    seen = set()
    with open(manifest_path, "r", encoding="utf-8") as f:
        for line in f:
            item = line.strip().lstrip("\ufeff")
            if not item or item.startswith("#"):
                continue
            token = item.split("#", 1)[0].strip().split()[0].split(",")[0]
            path = Path(token)
            stem = path.stem if path.suffix.lower() in IMAGE_EXTS else path.name
            for suffix in STAGE_DIRS:
                tag = f"_{suffix}"
                if stem.lower().endswith(tag.lower()):
                    stem = stem[: -len(tag)]
                    break
            if stem not in seen:
                stems.append(stem)
                seen.add(stem)
    return stems


def _list_inputs(input_dir, manifest_path=None, limit=None):
    files = [p for p in Path(input_dir).iterdir() if p.is_file() and p.suffix.lower() in IMAGE_EXTS]
    by_stem = {p.stem: p for p in files}
    if manifest_path:
        names = _read_manifest(manifest_path)
        selected = []
        missing = []
        for stem in names:
            path = by_stem.get(stem)
            if path is None:
                missing.append(stem)
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
    if not params_json:
        return {}
    with open(params_json, "r", encoding="utf-8") as f:
        return json.load(f)


def _final_refine(fused_uint8, final_params):
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
    raise ValueError(f"未知 final mode: {mode}")


def process_one_image(img_path, results_dir, params, resize_to=(320, 320), skip_existing=False):
    name = img_path.name
    stem = img_path.stem
    final_png = Path(results_dir) / "png" / "Final" / f"{stem}_Final.png"
    if skip_existing and final_png.exists():
        print(f"[SKIP] 已存在 Final PNG: {name}")
        return

    img_bgr = cv2.imread(str(img_path), cv2.IMREAD_COLOR)
    if img_bgr is None:
        raise RuntimeError(f"cv2.imread 失败: {img_path}")

    print(f"[INFO] 原始尺寸 {name}: {img_bgr.shape}")
    if resize_to is not None:
        w, h = resize_to
        if img_bgr.shape[0] != h or img_bgr.shape[1] != w:
            img_bgr = cv2.resize(img_bgr, (w, h), cv2.INTER_CUBIC)

    img = img_bgr.astype(np.float32) / 255.0
    print("正在处理:", name)

    bph_bgr = lgs_accc_bgr_improved(img, **params.get("bph", {}))
    bph_uint8 = np.clip(bph_bgr * 255, 0, 255).astype(np.uint8)
    save_result_variants(bph_uint8, results_dir, "BPH", name)
    print("白平衡完成")

    imf_params = {"aggressive": True}
    imf_params.update(params.get("imf1ray", {}))
    imf1_bgr = imf1Ray_from_bgr(bph_bgr, **imf_params)
    imf1_uint8 = np.clip(imf1_bgr * 255, 0, 255).astype(np.uint8)
    save_result_variants(imf1_uint8, results_dir, "IMF1Ray", name)
    print("IMF1 Rayleigh 增强完成")

    rghs_bgr = wb_safe_contrast(bph_bgr, **params.get("rghs", {}))
    rghs_uint8 = np.clip(rghs_bgr * 255, 0, 255).astype(np.uint8)
    save_result_variants(rghs_uint8, results_dir, "RGHS", name)
    print("RGHS 增强完成")

    clahe_bgr = clahe_3ch_wb_safe(bph_bgr, **params.get("clahe", {}))
    clahe_uint8 = np.clip(clahe_bgr * 255, 0, 255).astype(np.uint8)
    save_result_variants(clahe_uint8, results_dir, "CLAHE", name)
    print("CLAHE 增强完成")

    fused_bgr = fuse_three_images_bgr(imf1_bgr, rghs_bgr, clahe_bgr, **params.get("fusion", {}))
    fused_uint8 = np.clip(fused_bgr * 255, 0, 255).astype(np.uint8)
    save_result_variants(fused_uint8, results_dir, "Fused", name)
    print("融合完成:", stem + "_Fused")

    final_uint8 = _final_refine(fused_uint8, params.get("final", {}))
    save_result_variants(final_uint8, results_dir, "Final", name)
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
        )


if __name__ == "__main__":
    main()

