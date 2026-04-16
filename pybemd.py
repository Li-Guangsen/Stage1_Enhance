"""IMF1Ray 细节分支实现。

这个模块名基本符合当前实现。它不是“直接导出原始 IMF1”，而是先在 Lab 的
L 通道上提取第一 IMF / 高频响应，再叠加边缘与局部纹理增强，最后做
Rayleigh 亮度匹配，输出供融合阶段使用的高频细节分支图。
"""

# -*- coding: utf-8 -*-
import numpy as np
import cv2
from scipy.interpolate import Rbf, griddata

# ===================== 基础工具 =====================
def _to_float01(img):
    if img.dtype == np.uint8:
        return img.astype(np.float32) / 255.0
    x = img.astype(np.float32)
    if x.min() < 0.0 or x.max() > 1.0:
        x = np.clip(x, 0.0, 1.0)
    return x

def _to_uint8(img01):
    return np.clip(np.round(img01 * 255.0), 0, 255).astype(np.uint8)

def _normalize01(x, eps=1e-6):
    x = x.astype(np.float32, copy=False)
    mn, mx = float(np.min(x)), float(np.max(x))
    if mx - mn < eps:
        return np.zeros_like(x, dtype=np.float32)
    return (x - mn) / (mx - mn)

def _bgr2lab01(img_bgr01):
    u8 = _to_uint8(img_bgr01)
    lab = cv2.cvtColor(u8, cv2.COLOR_BGR2LAB).astype(np.float32)
    L = lab[..., 0] / 255.0
    a = (lab[..., 1] - 128.0) / 127.0
    b = (lab[..., 2] - 128.0) / 127.0
    return L, a, b

def _lab01_to_bgr(L01, a_norm, b_norm):
    L8 = np.clip(L01 * 255.0, 0, 255)
    a8 = np.clip(a_norm * 127.0 + 128.0, 0, 255)
    b8 = np.clip(b_norm * 127.0 + 128.0, 0, 255)
    lab = np.stack([L8, a8, b8], axis=-1).astype(np.uint8)
    return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR).astype(np.float32) / 255.0

def _scharr_mag(gray01):
    gx = cv2.Scharr(gray01, cv2.CV_32F, 1, 0)
    gy = cv2.Scharr(gray01, cv2.CV_32F, 0, 1)
    return _normalize01(np.sqrt(gx * gx + gy * gy))

def _resample_L(L, scale):
    """仅用于 EMD 的重采样（>1 上采样，<1 下采样，=1 原样）"""
    if abs(scale - 1.0) < 1e-6:
        return L
    H, W = L.shape
    s = float(scale)
    if s > 1.0:
        tmp = cv2.GaussianBlur(L, (0, 0), 0.6)
        return cv2.resize(tmp, (int(W * s), int(H * s)), interpolation=cv2.INTER_CUBIC)
    else:
        tmp = cv2.GaussianBlur(L, (0, 0), 0.8)
        return cv2.resize(tmp, (max(1, int(W * s)), max(1, int(H * s))), interpolation=cv2.INTER_AREA)

# ===================== 引导滤波（质量优先） =====================
def _guided_filter(guide01, src01, r=5, eps=1e-3):
    I = guide01.astype(np.float32); p = src01.astype(np.float32)
    k = 2 * r + 1
    mean_I = cv2.boxFilter(I, -1, (k, k), borderType=cv2.BORDER_REFLECT)
    mean_p = cv2.boxFilter(p, -1, (k, k), borderType=cv2.BORDER_REFLECT)
    corr_I  = cv2.boxFilter(I * I, -1, (k, k), borderType=cv2.BORDER_REFLECT)
    corr_Ip = cv2.boxFilter(I * p, -1, (k, k), borderType=cv2.BORDER_REFLECT)
    var_I = corr_I - mean_I * mean_I
    cov_Ip = corr_Ip - mean_I * mean_p
    a = cov_Ip / (var_I + eps)
    b = mean_p - a * mean_I
    mean_a = cv2.boxFilter(a, -1, (k, k), borderType=cv2.BORDER_REFLECT)
    mean_b = cv2.boxFilter(b, -1, (k, k), borderType=cv2.BORDER_REFLECT)
    q = mean_a * I + mean_b
    return np.clip(q, 0.0, 1.0).astype(np.float32)

# ===================== Rayleigh 直方图匹配（L通道） =====================
def _rayleigh_cdf_01(L=256, sigma=0.42):
    t = np.linspace(0.0, 1.0, L)
    cdf = 1.0 - np.exp(-(t * t) / (2.0 * (sigma ** 2) + 1e-12))
    return cdf / (cdf[-1] + 1e-12)

def _clip_and_redistribute_hist(hist, clip_limit_ratio=0.03, max_iter=5):
    hist = hist.astype(np.float64)
    total = hist.sum(); nbins = len(hist)
    if total <= 0: return hist
    clip_limit = clip_limit_ratio * (total / nbins)
    if clip_limit <= 0: return hist
    excess = np.sum(np.maximum(hist - clip_limit, 0.0))
    hist = np.minimum(hist, clip_limit)
    it = 0
    while excess > 0 and it < max_iter:
        inc = excess / nbins
        hist += inc
        overflow = np.sum(np.maximum(hist - clip_limit, 0.0))
        hist = np.minimum(hist, clip_limit)
        excess = overflow; it += 1
    if excess > 0:
        hist += (excess / nbins)
        hist = np.minimum(hist, clip_limit)
    return hist

def _rayleigh_match_L(L01, sigma=0.42, clip_limit_ratio=0.03, bins=256):
    L01 = np.clip(L01.astype(np.float32), 0, 1)
    hist, _ = np.histogram(L01.ravel(), bins=bins, range=(0.0, 1.0))
    hist = _clip_and_redistribute_hist(hist, clip_limit_ratio=clip_limit_ratio)
    cdf_src = np.cumsum(hist); cdf_src = cdf_src / (cdf_src[-1] + 1e-12)
    cdf_tgt = _rayleigh_cdf_01(L=bins, sigma=float(sigma))
    lut = np.interp(cdf_src, cdf_tgt, np.linspace(0.0, 1.0, bins)).astype(np.float32)
    idx = np.clip((L01 * (bins - 1)).round().astype(np.int32), 0, bins - 1)
    L_out = lut[idx]
    return np.clip(L_out, 0.0, 1.0).astype(np.float32)

# ===================== 高质量 2D-EMD：提 IMF1 =====================
def _gaussian_blur(x, s):
    return cv2.GaussianBlur(x, (0, 0), s, s, borderType=cv2.BORDER_REFLECT)

def _multiscale_highpass(gray01, sigmas=(0.6, 1.2, 2.0)):
    gray = gray01.astype(np.float32, copy=False)
    acc = np.zeros_like(gray, dtype=np.float32)
    wsum = 1e-6
    for s in sigmas:
        blur = _gaussian_blur(gray, float(s))
        hp = gray - blur
        w = 1.0 / (float(s) + 1e-6)
        acc += w * hp
        wsum += w
    acc = acc / wsum
    acc = np.tanh(acc * 3.5)
    return acc.astype(np.float32)

def _local_std_map(gray01, win=7):
    k = int(win)
    if k % 2 == 0:
        k += 1
    gray = gray01.astype(np.float32, copy=False)
    mean = cv2.boxFilter(gray, -1, (k, k), borderType=cv2.BORDER_REFLECT)
    mean2 = cv2.boxFilter(gray * gray, -1, (k, k), borderType=cv2.BORDER_REFLECT)
    var = np.maximum(mean2 - mean * mean, 0.0)
    std = np.sqrt(var + 1e-8)
    return _normalize01(std)

def _nonmax_extrema_mask(img, win=3, find_max=True):
    if find_max:
        neigh = cv2.dilate(img, np.ones((win, win), np.uint8))
        mask = (img >= neigh - 1e-12)
    else:
        neigh = cv2.erode(img, np.ones((win, win), np.uint8))
        mask = (img <= neigh + 1e-12)
    mask[[0, -1], :] = False; mask[:, [0, -1]] = False
    return mask

def _suppress_plateaus(img, mask, keep=1):
    lab_n, labels = cv2.connectedComponents(mask.astype(np.uint8), connectivity=8)
    if lab_n <= 1: return mask
    out = np.zeros_like(mask, dtype=bool)
    for lab in range(1, lab_n):
        ys, xs = np.where(labels == lab)
        if ys.size == 0: continue
        vals = img[ys, xs]
        idx = np.argsort(vals)[-keep:]
        out[ys[idx], xs[idx]] = True
    return out

def _grid_thin(xy, val, H, W, stride=16, topk=1):
    if xy.shape[0] == 0: return xy[:, 0], xy[:, 1], val
    xs, ys = xy[:, 0], xy[:, 1]
    gx = (xs // stride).astype(int); gy = (ys // stride).astype(int)
    key = gy * (W // stride + 1) + gx
    out_idx = []
    for k in np.unique(key):
        idxs = np.where(key == k)[0]
        if idxs.size == 0: continue
        sel = idxs[np.argsort(val[idxs])[-topk:]]
        out_idx.extend(sel.tolist())
    out_idx = np.array(out_idx, dtype=int)
    return xs[out_idx], ys[out_idx], val[out_idx]

def _add_border_samples(img, xs, ys, vs, step=8):
    H, W = img.shape
    xs_list = [int(i) for i in range(0, W, step)] + [W - 1]
    ys_list = [int(i) for i in range(0, H, step)] + [H - 1]
    bx = np.array(xs_list, dtype=np.int32)
    by_top = np.zeros_like(bx); by_bot = np.full_like(bx, H - 1)
    v_top = img[by_top, bx]; v_bot = img[by_bot, bx]
    by = np.array(ys_list, dtype=np.int32)
    bx_l = np.zeros_like(by); bx_r = np.full_like(by, W - 1)
    v_l = img[by, bx_l]; v_r = img[by, bx_r]
    xs = np.concatenate([xs, bx, bx, bx_l, bx_r]).astype(np.float64)
    ys = np.concatenate([ys, by_top, by_bot, by, by]).astype(np.float64)
    vs = np.concatenate([vs, v_top, v_bot, v_l, v_r]).astype(np.float64)
    return xs, ys, vs

def _rbf_surface(xs, ys, vs, H, W, smooth=1e-3):
    Xg, Yg = np.meshgrid(np.arange(W, dtype=np.float64), np.arange(H, dtype=np.float64))
    try:
        rbf = Rbf(xs, ys, vs, function='thin_plate', smooth=smooth)
        S = rbf(Xg, Yg).astype(np.float32)
    except Exception:
        try:
            S = griddata(points=np.stack([xs, ys], 1), values=vs, xi=(Xg, Yg), method='cubic').astype(np.float32)
        except Exception:
            S = griddata(points=np.stack([xs, ys], 1), values=vs, xi=(Xg, Yg), method='linear').astype(np.float32)
        if np.isnan(S).any():
            S = np.nan_to_num(S, nan=np.nanmedian(S)); S = _gaussian_blur(S, 1.0)
    return _gaussian_blur(S, 0.8)

class EMD2D:
    """
    二维经验模态分解（质量优先，用于提 IMF1）
    """
    def __init__(self,
                 extrema_win=3, plateau_keep=1,
                 grid_stride=16, border_step=8,
                 rbf_smooth=1e-3,
                 max_sift=30, tol_mean=0.05, tol_sd=0.2):
        self.extrema_win  = extrema_win
        self.plateau_keep = plateau_keep
        self.grid_stride  = grid_stride
        self.border_step  = border_step
        self.rbf_smooth   = rbf_smooth
        self.max_sift     = max_sift
        self.tol_mean     = tol_mean
        self.tol_sd       = tol_sd

    def _find_extrema_xyv(self, x):
        H, W = x.shape
        mask_max = _nonmax_extrema_mask(x, win=self.extrema_win, find_max=True)
        mask_min = _nonmax_extrema_mask(x, win=self.extrema_win, find_max=False)
        mask_max = _suppress_plateaus(x,  mask_max, keep=self.plateau_keep)
        mask_min = _suppress_plateaus(-x, mask_min, keep=self.plateau_keep)
        ys_max, xs_max = np.where(mask_max); ys_min, xs_min = np.where(mask_min)
        vmax = x[ys_max, xs_max] if xs_max.size else np.array([], dtype=np.float32)
        vmin = x[ys_min, xs_min] if xs_min.size else np.array([], dtype=np.float32)
        if xs_max.size:
            mx, my, mv = _grid_thin(np.stack([xs_max, ys_max], 1), vmax, H, W,
                                    stride=self.grid_stride, topk=1)
        else: mx = my = mv = np.array([], dtype=np.float32)
        if xs_min.size:
            nx, ny, nv = _grid_thin(np.stack([xs_min, ys_min], 1), vmin, H, W,
                                    stride=self.grid_stride, topk=1)
        else: nx = ny = nv = np.array([], dtype=np.float32)
        if mx.size: mx, my, mv = _add_border_samples(x, mx, my, mv, step=self.border_step)
        if nx.size: nx, ny, nv = _add_border_samples(x, nx, ny, nv, step=self.border_step)
        return mx, my, mv, nx, ny, nv

    def _envelopes(self, x):
        H, W = x.shape
        mx, my, mv, nx, ny, nv = self._find_extrema_xyv(x)
        if mx.size < 8 or nx.size < 8:
            up = _gaussian_blur(x, 1.2); lo = 2 * x - up
            return up.astype(np.float32), lo.astype(np.float32)
        up = _rbf_surface(mx, my, mv, H, W, smooth=self.rbf_smooth)
        lo = _rbf_surface(nx, ny, nv, H, W, smooth=self.rbf_smooth)
        return up.astype(np.float32), lo.astype(np.float32)

    def emd_first(self, img01):
        x = _to_float01(img01).astype(np.float32)
        h = x.copy()
        for _ in range(1, self.max_sift + 1):
            up, lo = self._envelopes(h)
            m  = 0.5 * (up + lo)
            hn = h - m
            sd    = float(np.sum((h - hn) ** 2) / (np.sum(h ** 2) + 1e-8))
            ratio = float(np.mean(np.abs(m)) / (np.mean(np.abs(h)) + 1e-8))
            h = hn
            if (ratio < self.tol_mean) or (sd < self.tol_sd): break
        h = h - np.mean(h)
        return h.astype(np.float32)

# ===================== 一体化主函数（含激进模式/仅EMD上采样/能量归一化） =====================
def imf1Ray_from_bgr(
    img_bgr,
    *,
    aggressive=False,         # True = 使用激进预设参数
    emd_scale=1.0,            # 仅在 EMD 求解阶段的上/下采样倍数（1.0=原尺寸，1.5≈只放大 EMD）
    # ——基线参数（会被 aggressive=True 覆盖为更猛的一组）——
    detail_gain=1.25,
    limit_tanh=2.0,
    edge_boost=0.70,
    gf_radius=4, gf_eps=1e-3,
    ray_sigma=0.42, ray_clip=0.03,
    emd_kwargs=None,          # 传递给 EMD2D 的 dict：extrema_win/plateau_keep/grid_stride/...
    # ——可选：局部能量归一化（更猛但抑制大块过冲）——
    energy_norm=False,
    energy_window=9,          # 局部窗口（奇数，建议 7/9/11）
    energy_gamma=0.6          # 0.5~0.8，越小越猛
):
    """
    输入：img_bgr (uint8 或 float32[0,1], BGR)
    输出：float32[0,1], BGR —— 用于融合的 IMF1 + Rayleigh 图

    调参时可以先按四组理解：

    1. `emd_scale` 与 `emd_kwargs`
       控制 IMF1 的提取尺度、极值点采样密度和 sift 强度，是“先从 L 通道里
       提什么样的高频骨架”这一层。
    2. `detail_gain`、`limit_tanh`
       控制 IMF1 注入前后的幅度与限幅，是“细节打得多重”的主旋钮。
    3. `gf_radius`、`gf_eps`、`edge_boost`
       控制边缘聚焦和细节平滑，是“让高频更贴边还是更散”的结构控制组。
    4. `ray_sigma`、`ray_clip`、`energy_norm*`
       控制亮度分布收口和局部能量重分配，决定输出更偏稳健还是更偏激进。
    """
    # 激进预设（更猛，更接近你“放大到960”的观感）
    if aggressive:
        detail_gain = 1.45
        limit_tanh  = 2.60
        # edge_boost  = 0.95
        edge_boost = 0.85
        # gf_radius, gf_eps = 2, 6e-4
        gf_radius, gf_eps = 3, 6e-4
        # ray_sigma, ray_clip = 0.38, 0.02
        ray_sigma, ray_clip = 0.38, 0.03
        emd_scale = max(emd_scale, 1.6)
        energy_norm = True
        energy_window = 9
        energy_gamma  = 0.7
        if emd_kwargs is None:
            emd_kwargs = dict(
                extrema_win=3, plateau_keep=1,
                grid_stride=8, border_step=4,
                # rbf_smooth=2e-4,
                rbf_smooth=5e-4,
                max_sift=50, tol_mean=0.035, tol_sd=0.12
            )
    else:
        if emd_kwargs is None:
            emd_kwargs = dict(
                extrema_win=3, plateau_keep=1,
                grid_stride=12, border_step=6,
                rbf_smooth=8e-4,
                max_sift=35, tol_mean=0.05, tol_sd=0.18
            )

    # —— 读入与 Lab 分解 ——
    img01 = _to_float01(img_bgr)
    L, a, b = _bgr2lab01(img01)

    # —— 仅 EMD 阶段的重采样（可 >1 只上采样 EMD）——
    L_emd = _resample_L(L, emd_scale)
    emd = EMD2D(**emd_kwargs)
    imf_scaled = emd.emd_first(L_emd)
    imf = cv2.resize(imf_scaled, (L.shape[1], L.shape[0]), interpolation=cv2.INTER_CUBIC)

    # —— 规范化 + 限幅 ——
    imf = imf / (np.std(imf) + 1e-6)
    imf = np.tanh(imf * float(limit_tanh))  # ~[-1,1]

    # —— 高频平滑（引导滤波） ——
    imf01 = _normalize01(imf) * 0.5 + 0.5
    imf_s = _guided_filter(L, imf01, r=int(gf_radius), eps=float(gf_eps))
    imf_s = (imf_s - 0.5) * 2.0  # 回到 ~[-1,1]

    # ——（可选）局部能量归一化：推高弱纹理、抑制大块过冲 ——
    if energy_norm:
        k = int(energy_window)
        if k % 2 == 0: k += 1
        E = cv2.boxFilter(imf_s * imf_s, -1, (k, k), borderType=cv2.BORDER_REFLECT)
        E = np.sqrt(E + 1e-6)
        imf_s = imf_s / (E ** float(energy_gamma) + 1e-3)
        imf_s = np.clip(imf_s, -1.5, 1.5)

    # — 高频纹理注入：结合 DoG 与局部方差（稳态 + 细节） —
    tex_win = max(5, int(gf_radius) * 2 + 1)
    texture_map = _local_std_map(L, win=tex_win)
    dog_hf = _multiscale_highpass(L)
    hf_strength = np.clip(0.45 + 0.75 * texture_map, 0.45, 1.4)
    hf_inject = dog_hf * (0.25 + 0.35 * texture_map)
    imf_hf = np.clip(imf_s * hf_strength + hf_inject, -1.8, 1.8)

    # —— 边缘权重（更聚焦于边界） ——
    edge = _scharr_mag(L)
    hf_response = _normalize01(np.abs(dog_hf))
    edge_mix = np.clip(0.6 * edge + 0.4 * hf_response, 0.0, 1.5)
    w_edge = (0.12 + 0.95 * edge_mix) if aggressive else (0.28 + float(edge_boost) * edge_mix)
    imf_edge = imf_hf * w_edge

    # —— 注入 L 并 Rayleigh 匹配 ——
    L_boost = np.clip(L + float(detail_gain) * imf_edge, 0, 1)
    L_ray = _rayleigh_match_L(L_boost, sigma=float(ray_sigma),
                              clip_limit_ratio=float(ray_clip), bins=256)

    # —— 合成回 BGR ——
    out = _lab01_to_bgr(L_ray, a, b)
    return np.clip(out, 0.0, 1.0).astype(np.float32)

# ===================== 直接运行测试 =====================
if __name__ == "__main__":
    # 示例：激进模式（320 输入，无需放大，EMD 阶段 1.6× 上采样）
    path = "input.jpg"
    bgr = cv2.imread(path, cv2.IMREAD_COLOR)
    out = imf1Ray_from_bgr(bgr, aggressive=True)  # 一行调用
    cv2.imwrite("output_imf1Ray.jpg", _to_uint8(out))
