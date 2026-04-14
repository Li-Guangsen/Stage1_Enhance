import numpy as np
import cv2
from skimage.color import rgb2lab, lab2rgb

# 白平衡安全对比度增强（改进版）
def wb_safe_contrast(
        img01,
        strength=0.6,        # 稍微比之前 0.5 强一点
        clip_limit=1.6,       # 略增强 CLAHE 力度
        tile_grid=(16, 16),
        p_low=1.0, p_high=99.0,
        assume_bgr=True,
        gamut_guard=True,
        # 防果冻参数
        pre_blur_sigma=0.3,
        deblock_radius=2,
        deblock_sigma_color=15.0,
        flat_suppress=True,
        flat_floor=0.4,
        grad_sigma=1.0,
        # 色度保护
        chroma_preserve=0.82,   # 稍微放开一点，让颜色活一点
        adaptive_chroma=True,
        brightness_boost=1.06,  # 轻微提亮
        # 新增：后端全局对比/色度增强
        post_L_stretch=(2.0, 98.0),
        post_chroma_gain=1.03
):
    x = np.asarray(img01, dtype=np.float32)
    x = np.clip(x, 0.0, 1.0)
    is_bgr = bool(assume_bgr)
    rgb = x[..., ::-1] if is_bgr else x

    lab = rgb2lab(rgb).astype(np.float32)
    L, a, b = lab[..., 0], lab[..., 1], lab[..., 2]

    # 记录原始色度范围
    a_std_orig = float(np.std(a))
    b_std_orig = float(np.std(b))

    # 预拉伸
    lo, hi = np.percentile(L, [p_low, p_high])
    if hi - lo > 1e-5:
        Ln = np.clip((L - lo) * (100.0 / (hi - lo)), 0.0, 100.0)
    else:
        Ln = L.copy()
    Ln = Ln.astype(np.float32, copy=False)
    # CLAHE 前轻微平滑
    if pre_blur_sigma and pre_blur_sigma > 0:
        Ln = cv2.GaussianBlur(Ln, (0, 0), pre_blur_sigma)

    # CLAHE 增强
    L_u8 = np.clip(np.round(Ln / 100.0 * 255.0), 0, 255).astype(np.uint8)
    clahe = cv2.createCLAHE(clipLimit=float(clip_limit), tileGridSize=tuple(tile_grid))
    Lc_u8 = clahe.apply(L_u8)

    # 去块处理
    if deblock_radius and deblock_radius > 0:
        d = int(deblock_radius * 2 + 1)
        Lc_u8 = cv2.bilateralFilter(Lc_u8, d=d,
                                    sigmaColor=float(deblock_sigma_color),
                                    sigmaSpace=float(deblock_radius * 2 + 1))

    Lc = (Lc_u8.astype(np.float32) / 255.0) * 100.0

    # 均值对齐
    mean_orig = float(np.mean(L))
    mean_new = float(np.mean(Lc))
    Lc = np.clip(Lc - mean_new + mean_orig, 0.0, 100.0)

    # 平坦区抑制
    eff_strength = float(np.clip(strength, 0.0, 1.0))
    if flat_suppress:
        # Ln01 一并保证是 float32
        Ln01 = (Ln / 100.0).astype(np.float32, copy=False)
        gx = cv2.Sobel(Ln01, cv2.CV_32F, 1, 0, ksize=3)
        gy = cv2.Sobel(Ln01, cv2.CV_32F, 0, 1, ksize=3)
        grad = np.sqrt(gx * gx + gy * gy)
        if grad_sigma and grad_sigma > 0:
            grad = cv2.GaussianBlur(grad.astype(np.float32), (0, 0), grad_sigma)
        gmin, gmax = float(grad.min()), float(grad.max())
        gnorm = (grad - gmin) / (gmax - gmin + 1e-6)
        w = flat_floor + (1.0 - flat_floor) * gnorm
        L_out = np.clip((1.0 - eff_strength * w) * L + (eff_strength * w) * Lc, 0.0, 100.0)
    else:
        L_out = np.clip((1.0 - eff_strength) * L + eff_strength * Lc, 0.0, 100.0)

    # 轻微提亮
    if brightness_boost > 1.0:
        L_out = np.clip(L_out * brightness_boost, 0.0, 100.0)

    # 自适应色度衰减
    if adaptive_chroma:
        L_ratio = np.divide(L_out, L + 1e-6,
                            out=np.ones_like(L),
                            where=(L > 1e-6))
        damping = chroma_preserve + (1.0 - chroma_preserve) / (L_ratio + 0.5)
        damping = np.clip(damping, 0.5, 1.0)[..., None]
        ab_out = np.stack([a, b], axis=-1) * damping
        a_out, b_out = ab_out[..., 0], ab_out[..., 1]
    else:
        a_out = a * chroma_preserve
        b_out = b * chroma_preserve

    # 色度范围保护（防止过度去色）
    a_std_new = float(np.std(a_out))
    b_std_new = float(np.std(b_out))
    if a_std_new > 1e-6:
        a_out = a_out * min(1.0, a_std_orig / a_std_new * 0.95)
    if b_std_new > 1e-6:
        b_out = b_out * min(1.0, b_std_orig / b_std_new * 0.95)

    # 初次重建 LAB
    lab_out = np.stack([L_out, a_out, b_out], axis=-1)
    rgb_out = lab2rgb(lab_out).astype(np.float32)

    # 色域保护
    if gamut_guard:
        for iteration in range(3):
            clipped = np.mean((rgb_out <= 1e-4) | (rgb_out >= 1.0 - 1e-4))
            if clipped < 0.005:
                break
            mu_L = float(np.median(L_out))
            mu_a = float(np.median(a_out))
            mu_b = float(np.median(b_out))
            compress_ratio = 0.97 - iteration * 0.02

            L_out = mu_L + compress_ratio * (L_out - mu_L)
            a_out = mu_a + compress_ratio * (a_out - mu_a)
            b_out = mu_b + compress_ratio * (b_out - mu_b)

            lab_out = np.stack([
                np.clip(L_out, 0.0, 100.0),
                a_out,
                b_out
            ], axis=-1)
            rgb_out = lab2rgb(lab_out).astype(np.float32)

    # ===== 新增：后端 Lab 统一微调（提高 Entropy / UCIQE） =====
        # ===== 新增：后端 Lab 统一微调（提高 Entropy / UCIQE） =====
    try:
        lab_final = rgb2lab(np.clip(rgb_out, 0.0, 1.0).astype(np.float32))
        Lf, af, bf = lab_final[..., 0], lab_final[..., 1], lab_final[..., 2]

        # L* 分位拉伸
        pl, ph = post_L_stretch
        pl = float(pl); ph = float(ph)
        lo2, hi2 = np.percentile(Lf, [pl, ph])
        if hi2 > lo2 + 1e-3:
            Lf_s = (Lf - lo2) * (100.0 / (hi2 - lo2))
        else:
            Lf_s = Lf

        # 先把 L 限到合法范围
        Lf_s = np.clip(Lf_s, 0.0, 100.0)

        # 轻微色度增益
        if post_chroma_gain is not None and abs(post_chroma_gain - 1.0) > 1e-3:
            cg2 = float(post_chroma_gain)
            af0, bf0 = af.copy(), bf.copy()

            # 第一步：基础色度增益 + 裁剪
            af = np.clip(af * cg2, -127.0, 127.0)
            bf = np.clip(bf * cg2, -127.0, 127.0)

            # 第二步：按 std 微调，但不要过大
            std_a0, std_b0 = float(np.std(af0)), float(np.std(bf0))
            std_a1, std_b1 = float(np.std(af)), float(np.std(bf))

            if std_a1 > 1e-6 and std_a0 > 1e-6:
                scale_a = min(1.10, std_a0 / (std_a1 + 1e-6) * 1.05)
                af *= scale_a
            if std_b1 > 1e-6 and std_b0 > 1e-6:
                scale_b = min(1.10, std_b0 / (std_b1 + 1e-6) * 1.05)
                bf *= scale_b

            # 再次裁剪，保证回到合法 Lab 范围
            af = np.clip(af, -127.0, 127.0)
            bf = np.clip(bf, -127.0, 127.0)
        else:
            # 不做额外色度增益时，仍然做一次安全裁剪
            af = np.clip(af, -127.0, 127.0)
            bf = np.clip(bf, -127.0, 127.0)

        lab_final2 = np.stack([Lf_s, af, bf], axis=-1).astype(np.float32)

        # 这里的 Lab 已经做了“硬约束”，一般不会再触发 gamut warning
        rgb_out = lab2rgb(lab_final2).astype(np.float32)
        rgb_out = np.clip(rgb_out, 0.0, 1.0)
    except Exception:
        rgb_out = np.clip(rgb_out, 0.0, 1.0)


    out = np.clip(rgb_out, 0.0, 1.0)
    return out[..., ::-1] if is_bgr else out


if __name__ == '__main__':
    img_path = "inputImg/haiyangkadun.3_BPH.jpg"
    img_bgr = cv2.imread(img_path, cv2.IMREAD_COLOR)
    if img_bgr is None:
        raise FileNotFoundError(f"无法读取图像: {img_path}")

    img_bgr = img_bgr.astype(np.float32) / 255.0

    # 推荐给你现在用的“指标增强档”配置
    config = dict(
        strength=0.6,
        clip_limit=1.6,
        chroma_preserve=0.82,
        brightness_boost=1.06,
        post_L_stretch=(2.0, 98.0),
        post_chroma_gain=1.03
    )

    out = wb_safe_contrast(img_bgr, **config)
    output_path = "enhanced_rghs_entropy_boost.jpg"
    cv2.imwrite(output_path, np.clip(out * 255, 0, 255).astype(np.uint8))
    print(f"已保存: {output_path}")
