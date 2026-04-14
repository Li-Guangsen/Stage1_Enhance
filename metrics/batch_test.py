"""
批量计算图像增强指标 可用版
"""
import os
import sys
import cv2
import numpy as np
from datetime import datetime

from libs.EMEE import EMEE
from libs.calc_InEntropy import get_entropy
from libs.Contrast_ratio import contrast
from libs.EME import EME
from libs.Gradient import Gradient
from libs.SIFT import get_keypoint
from libs.msssim import msssim
from libs.UCIQE import calc_uciqe
from libs.UIQM import calc_uiqm
# 如需后续扩展：PSNR/SIFT等，可在这里导入

np.seterr(over='ignore')
# "D:\Desktop\2025AAAI_HVDual_former\lgsresults"
# "D:\Desktop\2025CVPR_ABC-Former\ABC-Former\lgsresults"
# "D:\Desktop\2018_Generalization-of-the-Dark-Channel-Prior\lgsresults"
# "D:\Desktop\2018_Color-Balance-and-fusion-for-underwater-image-enhancement\lgsresult"
# "D:\Desktop\2022_HLRP-main\HLRP_Code\lgsresult"
# "D:\Desktop\2022_SGUIE_Net_Simple\lgsresults"
# "D:\Desktop\2024_Histoformer-main\lgsresults"
# "D:\Desktop\2024_WWPF_code\2023-WWPE\datasets\lgsresults"
# "D:\Desktop\Stage1\results\Final"


# ===== 配置（按需修改） =====
ORIGINAL_DIR = r"D:\Desktop\Stage1\data\inputImg\Original"  # 原图目录
INPUT_DIR = r"D:\Desktop\Stage1\results\Final"      # 输入图片文件夹
OUT_TXT   = r"./Txt/our.txt"    # 输出结果txt路径
RESIZE_TO = (320, 320)                  # 设为 None 则不缩放，例如：None

# 支持的图片后缀
EXTS = (".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff")

def _safe_imread(path):
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    if img is None:
        raise RuntimeError(f"cv2.imread 失败: {path}")
    return img

def _prepare_bgr_and_gray(img_bgr, resize_to=RESIZE_TO):
    if resize_to is not None:
        h, w = img_bgr.shape[:2]
        if (h, w) != (resize_to[1], resize_to[0]):
            img_bgr = cv2.resize(img_bgr, resize_to, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    return img_bgr, gray

def get_original_image(image_name_or_path,
                       original_dir=ORIGINAL_DIR,
                       resize_to=RESIZE_TO):
    image_name = os.path.basename(image_name_or_path)
    stem, _ = os.path.splitext(image_name)
    base = stem.split('_')[0]  # 去后缀标签
    # print(base)
    original_path = os.path.join(original_dir, base + '.jpg')
    img_bgr = cv2.imread(original_path, cv2.IMREAD_COLOR)
    if img_bgr is None:
        raise RuntimeError(f"原图未找到 读取失败: {base}.jpg")
    if resize_to is not None:
        h, w = img_bgr.shape[:2]
        if (h, w) != (resize_to[1], resize_to[0]):
            img_bgr = cv2.resize(img_bgr, resize_to, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    return img_bgr, gray

def _format_row(name, eme, emee, ent, ctr, avg_g, kp, ms_ssim, psnr,uciqe,uiqm):
    return (f"{name:<31}{eme:<8.4f}{emee:<9.4f}{ent:<9.4f}{ctr:<11.4f}{avg_g:<9.4f}{int(kp):<8}{ms_ssim:<8.4f}{psnr:<10.4f}"
            f"{uciqe:<8.4f}{uiqm:<8.4f}\n")

def main(input_dir=INPUT_DIR, out_txt=OUT_TXT):
    if not os.path.isdir(input_dir):
        print(f"[错误] 输入目录不存在: {input_dir}")
        sys.exit(1)

    files = [f for f in os.listdir(input_dir) if f.lower().endswith(EXTS)]
    files.sort()
    if not files:
        print(f"[警告] 目录内未找到图片: {input_dir}")
        # 仍然写一个空表头的txt，方便你检查
        with open(out_txt, "w", encoding="utf-8") as f:
            f.write("# Empty - no images found\n")
        print(f"[完成] 结果写入: {out_txt}")
        return

    # 统计
    cnt = 0
    s_eme = s_emee = s_ent = s_ctr = s_avg = s_ms_ssim = s_psnr = s_uciqe = s_uiqm = 0.0
    s_kp = 0
    failed = []

    with open(out_txt, "w", encoding="utf-8") as f:
        # 头部信息
        f.write(f"# Image Metrics (EME/EMEE/Entropy/Contrast/AvgGradient/SIFT_KP/MS_SSIM/PSNR/UCIQE/UIQM)\n")
        f.write(f"# Folder: {os.path.abspath(input_dir)}\n")
        f.write(f"# Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("# Notes:AvgGra -> AverageGradient\n")
        f.write("# Columns:\n")
        f.write("# {:<28} {:<7} {:<8} {:<8} {:<10} {:<7} {:<8} {:<8} {:<8} {:<8} {:<8}\n".format(
            "filename","EME","EMEE","Entropy","Contrast","AvgGra","SIFT_KP","MS_SSIM","PSNR","UCIQE","UIQM"))

        for name in files:
            path = os.path.join(input_dir, name)
            try:
                img_bgr = _safe_imread(path)
                img_bgr, gray = _prepare_bgr_and_gray(img_bgr, RESIZE_TO)
                orig_bgr, orig_gray = get_original_image(path)
                # 指标计算（与你的单图脚本保持一致）
                eme  = EME(gray)               # 需要灰度
                emee = EMEE(gray)              # 需要灰度
                ent  = get_entropy(gray)       # 需要灰度
                ctr  = contrast(gray)          # 需要灰度
                avgG = Gradient(gray)          # 需要灰度
                kp_count = get_keypoint(cv2.resize(img_bgr, (960, 960), cv2.INTER_CUBIC)) # SIFT关键点数目（彩色图）
                ms_ssim = msssim(orig_bgr, img_bgr)  # MSSSIM（灰度图）
                psnr = cv2.PSNR(orig_gray, gray)   # PSNR（灰度图）
                uciqe = calc_uciqe(img_bgr)        # UCIQE（彩色图）
                uiqm = calc_uiqm(img_bgr)          # UIQM（彩色图

                # 写入一行
                f.write(_format_row(name, eme, emee, ent, ctr, avgG, kp_count, ms_ssim, psnr,uciqe,uiqm))

                # 汇总
                cnt += 1
                s_eme  += float(eme)
                s_emee += float(emee)
                s_ent  += float(ent)
                s_ctr  += float(ctr)
                s_avg  += float(avgG)
                s_kp += int(kp_count)
                s_ms_ssim += float(ms_ssim)
                s_psnr += float(psnr)
                s_uciqe += float(uciqe)
                s_uiqm += float(uiqm)

                print(f"[OK] {name}")
            except Exception as e:
                failed.append((name, str(e)))
                print(f"[FAIL] {name}: {e}")

        # 尾部汇总
        f.write("\n# Summary\n")
        f.write(f"# Count: {cnt}\n")
        if cnt > 0:
            f.write(f"# Mean_EME\t{(s_eme/cnt):>18.4f}\n")
            f.write(f"# Mean_EMEE\t{(s_emee/cnt):>18.4f}\n")
            f.write(f"# Mean_Entropy\t{(s_ent/cnt):>14.4f}\n")
            f.write(f"# Mean_Contrast\t{(s_ctr/cnt):>14.4f}\n")
            f.write(f"# Mean_AvgGra\t{(s_avg/cnt):>14.4f}\n")
            f.write(f"# Mean_SIFT_KP\t{(s_kp/cnt):>14.4f}\n")
            f.write(f"# Mean_MS_SSIM\t{(s_ms_ssim/cnt):>14.4f}\n")
            f.write(f"# Mean_PSNR\t{(s_psnr/cnt):>18.4f}\n")
            f.write(f"# Mean_UCIQE\t{(s_uciqe/cnt):>14.4f}\n")
            f.write(f"# Mean_UIQM\t{(s_uiqm/cnt):>18.4f}\n")

        if failed:
            f.write("\n# Failed Files\n")
            for name, msg in failed:
                f.write(f"# {name}\t{msg}\n")

    print(f"[完成] 结果写入: {os.path.abspath(out_txt)}")
    if failed:
        print(f"[提示] 有 {len(failed)} 张图片失败，已写入文件尾部 Failed Files 区域。")

if __name__ == "__main__":
    # 如需命令行参数，可自行扩展 argparse；这里按你要求“直接可跑”
    main()
