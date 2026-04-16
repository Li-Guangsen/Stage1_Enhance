"""Three-branch fusion implementation.

这个模块对应流水线里的 `Fused` 阶段。它不是简单把三张增强图做平均，而是：

1. 把 `IMF1Ray / RGHS / CLAHE` 三个分支统一到 Lab 的 L 通道上比较
2. 为每个分支构造梯度、纹理、显著性、曝光等特征权重
3. 通过 guided filter 和拉普拉斯金字塔做层级融合
4. 用 `RGHS` 作为颜色锚点，主要融合亮度结构而不是直接混色

按当前职责分工理解：

- `IMF1Ray` 负责高频细节和边缘响应
- `RGHS` 负责主体层次、亮度托底和色彩锚定
- `CLAHE` 负责中层可见性、背景与暗部补偿
"""

# -*- coding: utf-8 -*-
import cv2
import numpy as np
import os

# ----------------- 基础与颜色空间 -----------------
def _to_float01(img):
    if img.dtype == np.uint8:
        return img.astype(np.float32)/255.0
    x = img.astype(np.float32)
    if x.max() > 1.5:  # 0~255 float
        x = x/255.0
    return np.clip(x, 0.0, 1.0)

def _to_uint8(x):
    return np.clip(np.round(x*255.0), 0, 255).astype(np.uint8)

def _ensure_same_size(imgs):
    H, W = imgs[0].shape[:2]
    out = []
    for im in imgs:
        if im.shape[:2] != (H, W):
            im = cv2.resize(im, (W, H), interpolation=cv2.INTER_CUBIC)
        out.append(im)
    return out

def _bgr2lab01(img01):
    # 全 float 路径，避免量化误差
    lab = cv2.cvtColor(img01.astype(np.float32), cv2.COLOR_BGR2LAB)  # L:[0,100]
    L = lab[...,0]/100.0
    a = lab[...,1]/127.0
    b = lab[...,2]/127.0
    return L, a, b

def _lab01_to_bgr(L01, a_norm, b_norm):
    lab = np.stack([L01*100.0, a_norm*127.0, b_norm*127.0], -1).astype(np.float32)
    bgr = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    return np.clip(bgr, 0.0, 1.0)

# ----------------- 特征/权重 -----------------
def _normalize01(x, eps=1e-6):
    x = x.astype(np.float32)
    mn, mx = float(x.min()), float(x.max())
    if mx - mn < eps: return np.zeros_like(x, np.float32)
    return (x - mn) / (mx - mn)

def _scharr_mag(gray01):
    gx = cv2.Scharr(gray01, cv2.CV_32F, 1, 0)
    gy = cv2.Scharr(gray01, cv2.CV_32F, 0, 1)
    return _normalize01(np.sqrt(gx*gx + gy*gy))

def _highpass(gray01, sigma=3.0):
    blur = cv2.GaussianBlur(gray01, (0,0), sigma, sigma, borderType=cv2.BORDER_REFLECT)
    return np.abs(gray01 - blur)

def _saliency(gray01, sigma=7.0):
    mu = cv2.GaussianBlur(gray01, (0,0), sigma, sigma, borderType=cv2.BORDER_REFLECT)
    return np.abs(gray01 - mu)

def _local_contrast(gray01, win=9):
    k = max(3, int(win))
    if k % 2 == 0:
        k += 1
    mean = cv2.boxFilter(gray01, -1, (k,k), borderType=cv2.BORDER_REFLECT)
    mean2 = cv2.boxFilter(gray01 * gray01, -1, (k,k), borderType=cv2.BORDER_REFLECT)
    var = np.maximum(mean2 - mean * mean, 0.0)
    std = np.sqrt(var + 1e-8)
    return _normalize01(std)

def _exposure_weight(L01, sigma=0.30):
    # 中灰最优，偏离越大权重越小
    return np.exp(-0.5*((L01 - 0.5)**2)/(sigma**2))

def _guided(guide01, src01, r=7, eps=1e-4):
    I = guide01.astype(np.float32); p = src01.astype(np.float32)
    k = 2*r + 1
    mI  = cv2.boxFilter(I, -1, (k,k), borderType=cv2.BORDER_REFLECT)
    mP  = cv2.boxFilter(p, -1, (k,k), borderType=cv2.BORDER_REFLECT)
    cI  = cv2.boxFilter(I*I, -1, (k,k), borderType=cv2.BORDER_REFLECT)
    cIp = cv2.boxFilter(I*p, -1, (k,k), borderType=cv2.BORDER_REFLECT)
    var = cI - mI*mI
    cov = cIp - mI*mP
    a = cov/(var + eps); b = mP - a*mI
    ma = cv2.boxFilter(a, -1, (k,k), borderType=cv2.BORDER_REFLECT)
    mb = cv2.boxFilter(b, -1, (k,k), borderType=cv2.BORDER_REFLECT)
    q = ma*I + mb
    return np.clip(q, 0.0, 1.0).astype(np.float32)

# ----------------- 金字塔 -----------------
def _gauss_pyr(x, levels=5):
    pyr = [x]
    cur = x
    for _ in range(levels-1):
        cur = cv2.pyrDown(cur)
        pyr.append(cur)
    return pyr

def _lap_pyr(x, levels=5):
    gp = _gauss_pyr(x, levels)
    lp = []
    for i in range(levels-1):
        up = cv2.pyrUp(gp[i+1], dstsize=(gp[i].shape[1], gp[i].shape[0]))
        lp.append(gp[i] - up)
    lp.append(gp[-1])
    return lp

def _reconstruct(lp):
    cur = lp[-1]
    for i in range(len(lp)-2, -1, -1):
        up = cv2.pyrUp(cur, dstsize=(lp[i].shape[1], lp[i].shape[0]))
        cur = up + lp[i]
    return cur

# ----------------- 融合主函数 -----------------
def fuse_three_images_bgr(
    imf1_bgr, rghs_bgr, clahe_bgr,
    *,
    levels=5,
    # 分支偏好（保留原默认）
    imf1_w_grad=0.55, imf1_w_tex=0.35, imf1_w_sal=0.08, imf1_w_exp=0.02,
    clahe_w_grad=0.35, clahe_w_tex=0.20, clahe_w_sal=0.35, clahe_w_exp=0.10,
    rghs_w_grad=0.15, rghs_w_tex=0.10, rghs_w_sal=0.15, rghs_w_exp=0.60,
    gf_radius=7, gf_eps=1e-4,
    usm_amount=0.0,
    # ====== 新增：门控与熵增强 ======
    imf1_keep_levels=5,              # IMF1 仅参与前 N 层（0=最高频）
    clahe_mid_range=None,            # CLAHE 参与的层范围（含端点），默认 (1, levels-2)
    rghs_low_boost=1.5,              # 最底层 RGHS 加权（原 2.0，略降）
    # 层内最小占比（防 RGHS 全吞）：中频层给 CLAHE 留底
    clahe_floor_mid=0.10,            # 仅对 lv=1..levels-2 生效
    clahe_floor_high=0.06,           # 对 lv=0 的底线
    # 纹理/方差驱动的 CLAHE/IMF1 提升
    std_sigma=3.0,                   # 用 Lr 估局部 std
    boost_clahe=0.12,                # s_norm * 该系数 加到 W_cla
    boost_imf1=0.06,                 # edge_imf1 * 该系数 加到 W_imf
    # 区域/纹理偏置
    local_contrast_win=11,
    imf_detail_bias=0.40,
    clahe_bg_bias=0.35,
    rgh_fg_bias=0.45,
    level_gain_imf=0.35,
    level_gain_cla=0.25,
    # 融合后 L 的温和对比扩展（增加直方图分散度）
    post_stretch=(1.0, 99.0),        # 分位拉伸 P_low, P_high
    post_sigmoid_k=1.20,             # S型对比系数（1.1~1.3）
    post_sigmoid_alpha=0.25          # 与原 L 融合比例（0.15~0.35）
):
    """Fuse IMF1Ray / RGHS / CLAHE into the `Fused` stage output.

    这里的“融合”主要发生在亮度通道，颜色默认更依赖 `RGHS` 分支维持稳定，
    因此调参时更适合把它理解为“亮度结构分工 + 色彩锚定”，而不是传统三图混色。

    参数可以先按五组理解：

    1. `*_w_grad / *_w_tex / *_w_sal / *_w_exp`
       控制三个分支各自偏好哪类特征，是最基础的分支职责分配。
    2. `gf_radius`、`gf_eps`
       控制权重图向 `RGHS` 结构对齐的程度，影响融合边界是否干净。
    3. `imf1_keep_levels`、`clahe_mid_range`、`rghs_low_boost`
       控制不同分支参与哪些金字塔层，是“高频给谁、中频给谁、低频给谁”的核心。
    4. `clahe_floor_*`、`boost_*`、`*_bias`、`level_gain_*`
       控制层内保底和区域偏置，主要用来防止某一路把其余两路完全吞掉。
    5. `post_stretch`、`post_sigmoid_k`、`post_sigmoid_alpha`
       控制融合后 L 通道的最后收口，对整体通透感和观感影响最大。
    """
    # 统一 & 拉齐
    imf1_bgr = _to_float01(imf1_bgr)
    rghs_bgr = _to_float01(rghs_bgr)
    clahe_bgr= _to_float01(clahe_bgr)
    imf1_bgr, rghs_bgr, clahe_bgr = _ensure_same_size([imf1_bgr, rghs_bgr, clahe_bgr])

    # Lab
    Limf, aimf, bimf = _bgr2lab01(imf1_bgr)
    Lr,   ar,   br   = _bgr2lab01(rghs_bgr)     # 颜色锚点
    Lc,   ac,   bc   = _bgr2lab01(clahe_bgr)

    # 特征
    def _feat(L):
        G = _normalize01(_scharr_mag(L))
        T = _normalize01(_highpass(L, sigma=3.0))
        S = _normalize01(_saliency(L, sigma=7.0))
        E = _normalize01(_exposure_weight(L, sigma=0.25))
        return G,T,S,E

    Gimf, Timf, Simf, Eimf = _feat(Limf)
    Gr,   Tr,   Sr,   Er   = _feat(Lr)
    Gc,   Tc,   Sc,   Ec   = _feat(Lc)

    # 组合权重（未归一化）
    W_imf = imf1_w_grad*Gimf + imf1_w_tex*Timf + imf1_w_sal*Simf + imf1_w_exp*Eimf
    W_cla = clahe_w_grad*Gc   + clahe_w_tex*Tc   + clahe_w_sal*Sc   + clahe_w_exp*Ec
    W_rgh = rghs_w_grad*Gr    + rghs_w_tex*Tr    + rghs_w_sal*Sr    + rghs_w_exp*Er

    # ===== 纹理/方差驱动的提升（提高中高频在平坦区的发言权）=====
    # 用 RGHS 的 L 估局部方差；用 IMF1 的梯度做边缘提升
    g  = cv2.GaussianBlur(Lr, (0,0), std_sigma, std_sigma, borderType=cv2.BORDER_REFLECT)
    g2 = cv2.GaussianBlur(Lr*Lr, (0,0), std_sigma, std_sigma, borderType=cv2.BORDER_REFLECT)
    s  = np.sqrt(np.maximum(g2 - g*g, 0.0))
    s_norm = _normalize01(s)
    W_cla += float(boost_clahe) * s_norm
    W_imf += float(boost_imf1)  * _normalize01(Gimf)

    # ===== 区域/对比度偏置 =====
    contrast_map = _local_contrast(Lr, win=local_contrast_win)
    diff = np.clip(Lr - Lc, -1.0, 1.0)
    fg_mask = _normalize01(np.maximum(diff, 0.0))  # RGHS 更亮的区域
    bg_mask = 1.0 - fg_mask
    W_imf *= (1.0 + float(imf_detail_bias) * contrast_map)
    W_cla *= (1.0 + float(clahe_bg_bias) * bg_mask + 0.35 * contrast_map)
    W_rgh *= (1.0 + float(rgh_fg_bias) * fg_mask)

    # 引导滤波到 RGHS 结构
    guide = Lr
    W_imf = _guided(guide, W_imf, r=gf_radius, eps=gf_eps)
    W_cla = _guided(guide, W_cla, r=gf_radius, eps=gf_eps)
    W_rgh = _guided(guide, W_rgh, r=gf_radius, eps=gf_eps)

    # ---------- 层级门控 ----------
    if clahe_mid_range is None:
        clahe_mid_range = (1, max(1, levels-2))
    s_lv, e_lv = int(clahe_mid_range[0]), int(clahe_mid_range[1])

    g_imf = np.array([1.0 if lv < int(imf1_keep_levels) else 0.0 for lv in range(levels)], dtype=np.float32)
    g_cla = np.array([1.0 if (lv>=s_lv and lv<=e_lv) else 0.0 for lv in range(levels)], dtype=np.float32)
    g_rgh = np.ones(levels, np.float32); g_rgh[-1] *= float(rghs_low_boost)

    # 建金字塔
    Wimf_gp = _gauss_pyr(_normalize01(W_imf), levels)
    Wcla_gp = _gauss_pyr(_normalize01(W_cla), levels)
    Wrgh_gp = _gauss_pyr(_normalize01(W_rgh), levels)

    Limf_lp = _lap_pyr(Limf, levels)
    Lcla_lp = _lap_pyr(Lc,   levels)
    Lr_lp   = _lap_pyr(Lr,   levels)

    # 分层融合（加入 CLAHE 底线，限制 RGHS 吞占）
    fused_lp = []
    for lv in range(levels):
        w1 = Wimf_gp[lv] * g_imf[lv]
        w2 = Wcla_gp[lv] * g_cla[lv]
        w3 = Wrgh_gp[lv] * g_rgh[lv]

        if level_gain_imf > 1e-6:
            w1 = w1 * (1.0 + float(level_gain_imf) * _normalize01(np.abs(Limf_lp[lv])))
        if level_gain_cla > 1e-6:
            w2 = w2 * (1.0 + float(level_gain_cla) * _normalize01(np.abs(Lcla_lp[lv])))

        # —— 中频层给 CLAHE 底线；最高频也给一点底线
        if lv == 0:
            tau = float(clahe_floor_high)
            w2 = np.maximum(w2, tau)
        elif 1 <= lv <= levels-2:
            tau = float(clahe_floor_mid)
            w2 = np.maximum(w2, tau)

        Wsum = w1 + w2 + w3 + 1e-6
        w1, w2, w3 = w1/Wsum, w2/Wsum, w3/Wsum

        F = w1*Limf_lp[lv] + w2*Lcla_lp[lv] + w3*Lr_lp[lv]
        fused_lp.append(F)

    L_fused = np.clip(_reconstruct(fused_lp), 0.0, 1.0)

    # 可选 USM（只在 L）
    if usm_amount > 0:
        blur = cv2.GaussianBlur(L_fused, (0,0), 1.0, 1.0)
        L_fused = np.clip(L_fused + usm_amount*(L_fused - blur), 0.0, 1.0)

    # ===== 融合后：温和的直方图扩展 + S型对比（抬熵）=====
    pl, ph = float(post_stretch[0]), float(post_stretch[1])
    lo, hi = np.percentile(L_fused, pl), np.percentile(L_fused, ph)
    if hi <= lo: hi = lo + 1e-6
    Ls = np.clip((L_fused - lo)/(hi - lo), 0.0, 1.0)
    k = float(post_sigmoid_k); alpha = float(post_sigmoid_alpha)
    Lsig = 1.0 / (1.0 + np.exp(-k*(Ls - 0.5)))
    L_final = np.clip((1.0 - alpha)*Ls + alpha*Lsig, 0.0, 1.0)

    # 色度仍取 RGHS（颜色锚点）
    out01 = _lab01_to_bgr(L_final, ar, br)
    return out01


# ----------------- 从文件融合（可选） -----------------
def fuse_from_files(imf1_path, rghs_path, clahe_path, out_path, **kwargs):
    imf1 = cv2.imread(imf1_path, cv2.IMREAD_COLOR)
    rghs = cv2.imread(rghs_path, cv2.IMREAD_COLOR)
    cla  = cv2.imread(clahe_path, cv2.IMREAD_COLOR)
    if imf1 is None or rghs is None or cla is None:
        raise FileNotFoundError("三张输入图像有读取失败，请检查路径。")
    out01 = fuse_three_images_bgr(imf1, rghs, cla, **kwargs)
    cv2.imwrite(out_path, _to_uint8(out01))
    return out_path

if __name__ == "__main__":
    # 示例：按你命名习惯，给定三图路径融合
    imf1 = "haiyangkadun.3_IMF1Ray.jpg"
    rghs = "haiyangkadun.3_RGHS.jpg"
    cla  = "haiyangkadun.3_CLAHE.jpg"
    print(fuse_from_files(imf1, rghs, cla, "haiyangkadun.3_original_f.jpg"))
