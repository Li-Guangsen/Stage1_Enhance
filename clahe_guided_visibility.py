"""CLAHE-guided visibility branch implementation.

`CLAHE` 也是沿用的历史阶段名。这里不是直接输出传统 CLAHE 图，而是先用
三通道 CLAHE 推导亮度增益，再用 guided filter 平滑增益图，最后做 Lab
空间后处理，因此更准确地说是“CLAHE 引导的局部可见性增强分支”。

从 2026-04-17 起，主实现文件名从 `CLAHE.py` 调整为
`clahe_guided_visibility.py`。阶段名 `CLAHE` 仍保留在结果目录、配置字段
和实验记录里，用于兼容既有资产。
"""

import cv2
import numpy as np

_EPS = 1e-6

# -------- 基础工具 --------
def _to_float01_and_uint8(img):
    arr = np.asarray(img)
    if arr.ndim != 3 or arr.shape[2] != 3:
        raise ValueError("输入必须是 H×W×3 彩色图像")
    if np.issubdtype(arr.dtype, np.floating):
        img01 = np.clip(arr, 0.0, 1.0).astype(np.float32)
        img_u8 = np.clip(np.round(img01 * 255.0), 0, 255).astype(np.uint8)
        return img01, img_u8, True
    img_u8 = np.clip(arr, 0, 255).astype(np.uint8)
    img01 = img_u8.astype(np.float32) / 255.0
    return img01, img_u8, False

def _srgb_to_linear(x):
    x = np.clip(x, 0.0, 1.0).astype(np.float32)
    a = (x <= 0.04045).astype(np.float32)
    return a * (x / 12.92) + (1.0 - a) * np.power((x + 0.055) / 1.055, 2.4)

def _linear_to_srgb(y):
    y = np.clip(y, 0.0, 1.0).astype(np.float32)
    a = (y <= 0.0031308).astype(np.float32)
    return a * (12.92 * y) + (1.0 - a) * (1.055 * np.power(y, 1.0/2.4) - 0.055)

def _mad_std01(x):
    med = np.median(x); mad = np.median(np.abs(x - med)) + _EPS
    return 1.4826 * mad

def _adaptive_tile_grid(h, w):
    base = max(4, int(round(min(h, w) / 70.0)))
    base = min(base, 16)
    if base % 2 != 0: base += 1
    return (base, base)

def _adaptive_clip_limit(gray01):
    rstd = _mad_std01(gray01)
    clip = 1.6 + 5.0 * rstd
    return float(np.clip(clip, 1.2, 4.8))

def _guided_filter(I, p, r=6, eps=1e-4):
    I = I.astype(np.float32); p = p.astype(np.float32)
    k = (2*r+1, 2*r+1)
    mean_I = cv2.boxFilter(I, -1, k, borderType=cv2.BORDER_REFLECT)
    mean_p = cv2.boxFilter(p, -1, k, borderType=cv2.BORDER_REFLECT)
    mean_Ip = cv2.boxFilter(I*p, -1, k, borderType=cv2.BORDER_REFLECT)
    cov_Ip = mean_Ip - mean_I * mean_p
    mean_II = cv2.boxFilter(I*I, -1, k, borderType=cv2.BORDER_REFLECT)
    var_I = np.maximum(mean_II - mean_I*mean_I, 0.0)
    a = cov_Ip / (var_I + eps)
    b = mean_p - a * mean_I
    mean_a = cv2.boxFilter(a, -1, k, borderType=cv2.BORDER_REFLECT)
    mean_b = cv2.boxFilter(b, -1, k, borderType=cv2.BORDER_REFLECT)
    return mean_a * I + mean_b

# -------- 主函数：三通道 CLAHE（WB-safe 等比增益 + 后处理） --------
def clahe_3ch_wb_safe(
    img,
    # —— CLAHE 参数（可覆盖；None=自适应）——
    clip_limit=2.4,
    tile_size=(6,6),
    # —— 等比增益相关 ——
    only_boost=False,
    gmin=0.85,
    gmax=3.0,
    gain_gamma=1.05,
    # —— 引导滤波（边缘保真）——
    gf_radius=7,
    gf_eps=3e-4,
    # —— 新增：后端 L 拉伸 + 轻微色度增强 —— 
    post_L_stretch=(1.0, 99.0),   # 百分位范围，适度拉开亮度
    post_chroma_gain=1.05         # Lab a/b 的增益，建议 1.02~1.08
):
    """CLAHE-guided local visibility enhancement branch.

    调参时可以先按四组理解：

    1. `clip_limit`、`tile_size`
       控制 CLAHE 本体的局部增强力度和空间尺度。
    2. `only_boost`、`gmin`、`gmax`、`gain_gamma`
       控制亮度增益图的上下界和非线性，是“提多少、压不压过增强”的主组。
    3. `gf_radius`、`gf_eps`
       控制增益图平滑程度，影响块感、边缘泄漏和局部稳定性。
    4. `post_L_stretch`、`post_chroma_gain`
       控制后端 Lab 微调，主要负责把局部可见性结果再做温和收口。
    """
    img01, img_u8, is_float = _to_float01_and_uint8(img)
    h, w = img_u8.shape[:2]

    # --- CLAHE 参数 ---
    if tile_size is None:
        tile = _adaptive_tile_grid(h, w)
    else:
        tile = tuple(map(int, tile_size))
    if clip_limit is None:
        gray01 = cv2.cvtColor(img_u8, cv2.COLOR_BGR2GRAY).astype(np.float32)/255.0
        clip = _adaptive_clip_limit(gray01)
    else:
        clip = float(clip_limit)

    clahe = cv2.createCLAHE(clipLimit=clip, tileGridSize=tile)

    # --- 三通道 CLAHE（仅用来推导亮度增益） ---
    bgr_eq = cv2.merge([clahe.apply(img_u8[:, :, i]) for i in range(3)])

    # sRGB亮度（BT.709）
    y0 = (0.0722*img_u8[:,:,0] + 0.7152*img_u8[:,:,1] + 0.2126*img_u8[:,:,2]).astype(np.float32)/255.0
    y1 = (0.0722*bgr_eq[:,:,0] + 0.7152*bgr_eq[:,:,1] + 0.2126*bgr_eq[:,:,2]).astype(np.float32)/255.0

    gain = (y1 + 1e-3) / (y0 + 1e-3)
    if only_boost:
        gain = np.maximum(gain, 1.0)
    gain = np.clip(gain, max(gmin, 1.0 if only_boost else gmin), gmax)

    # 引导滤波（以 y0 为引导）
    if gf_radius is None:
        gf_radius = max(6, int(round(min(h, w) / 40.0)))
    gain = _guided_filter(y0, gain, r=gf_radius, eps=gf_eps)
    gain = np.clip(gain, gmin, gmax)

    # 可选幂次调节
    if abs(gain_gamma - 1.0) > 1e-3:
        gain = np.power(gain, gain_gamma)

    # 线性RGB等比缩放（保白平衡）
    lin = _srgb_to_linear(img01)
    out01 = _linear_to_srgb(np.clip(lin * gain[..., None], 0.0, 1.0))

    # ===== 新增：Lab 空间轻度对比 + 色度增强 =====
    # 只做很温和的调整，防止偏色
    try:
        lab = cv2.cvtColor(out01.astype(np.float32), cv2.COLOR_BGR2LAB)
        L = lab[..., 0]   # [0,100]
        a = lab[..., 1]   # 大约 [-127,127]
        b = lab[..., 2]

        # (1) L* 分位拉伸，增加对比度 & 熵
        pl, ph = post_L_stretch
        pl = float(pl); ph = float(ph)
        lo, hi = np.percentile(L, [pl, ph])
        if hi > lo + 1e-3:
            Ls = np.clip((L - lo) * (100.0 / (hi - lo)), 0.0, 100.0)
        else:
            Ls = L

        # (2) 轻微色度增益（围绕 0 放大 a/b）
        if post_chroma_gain is not None and abs(post_chroma_gain - 1.0) > 1e-3:
            cg = float(post_chroma_gain)
            a0 = a.copy(); b0 = b.copy()
            a = np.clip(a * cg, -127.0, 127.0)
            b = np.clip(b * cg, -127.0, 127.0)
            # 防止色度过大：控制 std 不超过原来的 1.1 倍
            std_a0, std_b0 = float(np.std(a0)), float(np.std(b0))
            std_a1, std_b1 = float(np.std(a)), float(np.std(b))
            if std_a1 > 1e-6 and std_a0 > 1e-6:
                a *= min(1.1, std_a0 / std_a1 * 1.05)
            if std_b1 > 1e-6 and std_b0 > 1e-6:
                b *= min(1.1, std_b0 / std_b1 * 1.05)
        else:
            Ls = L

        lab2 = np.stack([Ls, a, b], axis=-1).astype(np.float32)
        out01 = cv2.cvtColor(lab2, cv2.COLOR_LAB2BGR)
        out01 = np.clip(out01, 0.0, 1.0)
    except Exception:
        # 出问题就退回原始 out01，保证稳定
        out01 = np.clip(out01, 0.0, 1.0)

    return out01.astype(np.float32) if is_float else np.clip(np.round(out01*255.0), 0, 255).astype(np.uint8)


# -------- 预设参数集 --------
PRESETS = {
    "color_safe_mild":   dict(
        clip_limit=1.6, tile_size=(6,6),
        only_boost=True,  gmax=2.0,
        gf_radius=10, gf_eps=5e-4,
        gain_gamma=0.95,
        post_L_stretch=(2.0, 98.0),
        post_chroma_gain=1.02
    ),
    "standard_microscopy": dict(
        clip_limit=None, tile_size=None,
        only_boost=True,  gmax=2.6,
        gf_radius=None, gf_eps=1e-4,
        gain_gamma=1.0,
        post_L_stretch=(2.0, 98.0),
        post_chroma_gain=1.03
    ),
    # 重点推荐这个给你现在的显微藻类增强
    "entropy_boost_microscopy": dict(
        clip_limit=2.4, tile_size=(6,6),
        only_boost=False, gmin=0.85, gmax=3.0,
        gf_radius=7, gf_eps=3e-4,
        gain_gamma=1.05,
        post_L_stretch=(1.0, 99.0),
        post_chroma_gain=1.05
    ),
    "low_noise_scene":   dict(
        clip_limit=1.8, tile_size=(4,4),
        only_boost=True,  gmax=2.2,
        gf_radius=12, gf_eps=6e-4,
        gain_gamma=0.9,
        post_L_stretch=(3.0, 97.0),
        post_chroma_gain=1.02
    ),
}

if __name__ == "__main__":
    img_path = "inputImg\\duanjiao.9.jpg"
    img_bgr = cv2.imread(img_path, cv2.IMREAD_COLOR)
    enhanced_bgr = clahe_3ch_wb_safe(img_bgr, **PRESETS["entropy_boost_microscopy"])
    out_path = "enhanced_entropy_boost.jpg"
    cv2.imwrite(out_path, enhanced_bgr)
    print("增强完成，保存至:", out_path)
