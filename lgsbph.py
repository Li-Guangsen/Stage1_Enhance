"""BPH white-balance implementation.

这个模块对应流水线里的 `BPH` 阶段。当前主实现不是论文里 ACCC 的直接照搬，
而是“灰像素引导预白平衡 + 稳健化 ACCC 循环补偿 + 亮度回调”的工程化版本。

按当前项目语境理解：

- `lgs_accc_bgr` 是较接近基础公式的版本
- `lgs_accc_bgr_improved` 是主线实际使用的改进版白平衡入口
"""

import numpy as np
import cv2


def lgs_accc_bgr(
    bgr,
    max_iters=10,
    loss_thresh=1e-4,
    eps=1e-8
):
    """
    参数
    ----
    bgr : np.ndarray
        输入图像，float32/float64，范围 [0,1]，形状 (H, W, 3)，BGR 顺序。
    max_iters : int
        式 (3)(4) 的最大迭代次数。
    loss_thresh : float
        收敛阈值， Loss <= 10^-4。
    eps : float
        防止除零用的小数。

    返回
    ----
    bgr_out : np.ndarray
        白平衡后图像，float32，[0,1]，BGR 顺序。
    """

    if bgr.ndim != 3 or bgr.shape[2] != 3:
        raise ValueError("输入必须是 H×W×3 的 BGR 图像")

    # 统一 float32 & [0,1]
    img = np.clip(bgr.astype(np.float32), 0.0, 1.0)
    B = img[..., 0]
    G = img[..., 1]
    R = img[..., 2]

    # ---------- (1) 通道平均值，定义 Ia / Ib / Ic ----------
    # I_c_bar = 1/(HW) sum I_c，c ∈ {R,G,B}
    means = np.array([B.mean(), G.mean(), R.mean()], dtype=np.float32)
    order = np.argsort(means)  # 升序：最小、中、最大

    idx_c = int(order[0])  # 最小 -> Ic
    idx_b = int(order[1])  # 中   -> Ib
    idx_a = int(order[2])  # 最大 -> Ia

    ch_list = [B.copy(), G.copy(), R.copy()]
    Ia = ch_list[idx_a]    # large channel
    Ib = ch_list[idx_b]    # medium channel
    Ic = ch_list[idx_c]    # small channel



    # ---------- 辅助函数：计算 Īa, Īb, Īc ----------
    def _channel_means(Ia_arr, Ib_arr, Ic_arr):
        return float(Ia_arr.mean()), float(Ib_arr.mean()), float(Ic_arr.mean())

    # ---------- (3)(4)(5) 中、小通道循环补偿 ----------
    # I_b^CR = I_b + (Īa - Īb)*(1 - I_b)*I_a
    # I_c^CR = I_c + (Īa - Īc)*(1 - I_c)*I_a
    # Loss  = (Īa - Īb)^2 + (Īa - Īc)^2

    for it in range(max_iters):
        Ia_bar, Ib_bar, Ic_bar = _channel_means(Ia, Ib, Ic)
        loss = (Ia_bar - Ib_bar) ** 2 + (Ia_bar - Ic_bar) ** 2

        if loss <= loss_thresh:
            # 已满足 Loss <= 10^-4，停止
            break

        # 一轮补偿
        Ib_new = Ib + (Ia_bar - Ib_bar) * (1.0 - Ib) * Ia
        Ic_new = Ic + (Ia_bar - Ic_bar) * (1.0 - Ic) * Ia

        Ib = np.clip(Ib_new, 0.0, 1.0)
        Ic = np.clip(Ic_new, 0.0, 1.0)

    # ---------- 映射回 BGR 顺序 ----------
    out_ch = [None, None, None]
    out_ch[idx_a] = Ia
    out_ch[idx_b] = Ib
    out_ch[idx_c] = Ic

    B_out = out_ch[0]
    G_out = out_ch[1]
    R_out = out_ch[2]

    bgr_out = np.stack([B_out, G_out, R_out], axis=-1)
    bgr_out = np.clip(bgr_out, 0.0, 1.0).astype(np.float32)
    return bgr_out




def lgs_accc_bgr_improved(
    bgr,
    max_iters=8,
    loss_thresh=1e-4,
    eps=1e-8,
    # --- Stage 1: 灰像素预白平衡参数 ---
    gray_s_thr=20.0,      # Lab 中 a,b 的模长阈值，越小“越灰”（5~15 可调）
    lum_low=0.10,         # 参与估计的亮度下界 (相对 0~1)
    lum_high=0.90,        # 参与估计的亮度上界
    pre_gain_clip=2.5,    # 预补偿每通道 gain 上限（防止极端增益）
    red_gain_extra=1.3,   # 红通道允许更大一点增益，用于水下红衰减
    # --- Stage 2: ACCC 迭代参数 ---
    accc_alpha=0.7,       # 循环补偿步长 (0~1)，越小越稳健
    accc_delta_max=0.25,  # 单次迭代中 (Ia_bar - Ib_bar) 的截断上限
    # --- Stage 3: 亮度回调 ---
    brightness_preserve=True,
    brightness_scale_clip=(0.8, 1.2)  # 全局亮度缩放范围
):
    """
    改进版 LGS-ACCC 白平衡 (BGR, float [0,1])

    设计要点：
    1) Stage1：在 Lab 空间中用“近中性 & 中亮度”像素估计光源，并做一次
       灰像素引导的全局增益预补偿，弱化大面积绿色/蓝色背景的影响。
    2) Stage2：在预补偿结果上做 Fan 风格的循环补偿，但只在中亮度区域
       统计均值，并且对 (Ia_bar - Ib_bar) 做截断 + 步长控制，防止拉爆。
    3) Stage3：回调整体亮度到接近原图，避免过亮/过暗导致后续模块失衡。

    输入:
        bgr: float32/float64, [0,1], shape = (H, W, 3), BGR 顺序。

    输出:
        bgr_out: float32, [0,1], shape = (H, W, 3), BGR 顺序。

    这个函数在当前流水线中的职责是“把偏色和通道失衡先压到一个更稳的起点”，
    不是追求把图像直接增强到最终观感。

    调参时可以先按四组理解：

    1. `gray_s_thr`、`lum_low`、`lum_high`
       控制灰像素候选怎么选。阈值越严格，颜色估计越“干净”，但也越容易样本太少；
       亮度窗口越窄，越能避开阴影和高光干扰，但鲁棒性会下降。
    2. `pre_gain_clip`、`red_gain_extra`
       控制预白平衡增益上限。放大它们会更积极补偿偏色，尤其是水下红衰减；
       但过大时更容易把噪声、偏红或局部过曝一起推起来。
    3. `max_iters`、`loss_thresh`、`accc_alpha`、`accc_delta_max`
       控制 ACCC 补偿的收敛速度与安全边界。更大的步长和截断上限会更快更猛，
       但也更容易振荡或把通道拉爆；更保守则通常更稳。
    4. `brightness_preserve`、`brightness_scale_clip`
       控制最后是否回调整体亮度。它们不直接决定偏色校正能力，但会明显影响
       后续分支接手时的亮度起点是否稳定。
    """
    if bgr.ndim != 3 or bgr.shape[2] != 3:
        raise ValueError("输入必须是 H×W×3 的 BGR 图像")

    # ---------- 统一到 float32 [0,1] ----------
    img = np.clip(bgr.astype(np.float32), 0.0, 1.0)
    H, W = img.shape[:2]

    # 保存原始亮度均值，用于最后回调
    B0, G0, R0 = img[..., 0], img[..., 1], img[..., 2]
    Y0 = 0.114 * B0 + 0.587 * G0 + 0.299 * R0
    Y0_mean = float(Y0.mean())

    # ============================================================
    # Stage 1: 灰像素引导的全局预白平衡 (Gray-guided Global AWB)
    # ============================================================
    # 转到 Lab，利用 a,b 接近 0 的像素近似灰像素 (Gray Pixel)
    # 这里用的是一个简化版的灰像素思路，避免实现完整 MSGP/DGP。
    # 参考: Qian et al., "On Finding Gray Pixels", CVPR 2019.:contentReference[oaicite:3]{index=3}
    img_u8 = np.clip(np.round(img * 255.0), 0, 255).astype(np.uint8)
    lab = cv2.cvtColor(img_u8, cv2.COLOR_BGR2LAB)
    L_lab, a_lab, b_lab = cv2.split(lab)

    # 亮度范围掩模
    L_norm = L_lab.astype(np.float32) / 255.0
    mask_lum = (L_norm > lum_low) & (L_norm < lum_high)

    # 近中性掩模：sqrt(a^2 + b^2) < gray_s_thr
    a_f = a_lab.astype(np.float32) - 128.0
    b_f = b_lab.astype(np.float32) - 128.0
    s_ab = np.sqrt(a_f * a_f + b_f * b_f)
    mask_gray = s_ab < gray_s_thr

    mask_gp = mask_lum & mask_gray
    num_gp = int(mask_gp.sum())
    # print("L_norm min/max:", L_norm.min(), L_norm.max())
    # print("s_ab   min/max:", s_ab.min(), s_ab.max())
    # print("lum_low, lum_high:", lum_low, lum_high)
    # print("gray_s_thr:", gray_s_thr)
    # print("num_lum:", int(mask_lum.sum()), "num_gray:", int(mask_gray.sum()), "num_gp:", num_gp)


    B = img[..., 0]
    G = img[..., 1]
    R = img[..., 2]

    if num_gp > 0.001 * H * W:  # 至少占 0.1% 像素再采用灰像素估计
        print("使用gray_s_thr灰像素引导")
        B_gp = B[mask_gp]
        G_gp = G[mask_gp]
        R_gp = R[mask_gp]
        B_mean_gp = float(B_gp.mean())
        G_mean_gp = float(G_gp.mean())
        R_mean_gp = float(R_gp.mean())
    else:
        s_valid = s_ab[mask_lum]
        if s_valid.size > 0:
            print("灰像素过少，使用亮度合格像素中 s_ab 最小的前 0.1% 作为灰像素")
            # 0.1% 百分位
            p = 0.1  # 0.1%
            thr_dyn = np.percentile(s_valid, p)

            mask_gray_dyn = (s_ab <= thr_dyn)
            mask_gp_dyn = mask_lum & mask_gray_dyn
            num_gp_dyn = int(mask_gp_dyn.sum())
            if num_gp_dyn > 0:
                B_gp = B[mask_gp_dyn]
                G_gp = G[mask_gp_dyn]
                R_gp = R[mask_gp_dyn]
                B_mean_gp = float(B_gp.mean())
                G_mean_gp = float(G_gp.mean())
                R_mean_gp = float(R_gp.mean())
            else:
                # 极端兜底：真的什么都选不到，退回整幅图 Gray-World
                print("动态灰像素仍为空，退回整幅图 Gray-World 均值")
                B_mean_gp = float(B.mean())
                G_mean_gp = float(G.mean())
                R_mean_gp = float(R.mean())
        else:
            # 连亮度合格的像素都没有（极端情况）
            print("亮度合格像素为 0，退回整幅图 Gray-World 均值")
            B_mean_gp = float(B.mean())
            G_mean_gp = float(G.mean())
            R_mean_gp = float(R.mean())

    # 目标中性亮度（对这三者取平均）
    target_mean = (B_mean_gp + G_mean_gp + R_mean_gp) / 3.0

    # 每通道预增益（这里允许红通道稍微更大一点，用于补偿水下红衰减）
    gB = target_mean / (B_mean_gp + eps)
    gG = target_mean / (G_mean_gp + eps)
    gR = target_mean / (R_mean_gp + eps)

    # clip 增益，单独给 R 一个稍大的上限
    g_max_B_G = pre_gain_clip
    g_max_R = pre_gain_clip * red_gain_extra

    gB = np.clip(gB, 1.0 / g_max_B_G, g_max_B_G)
    gG = np.clip(gG, 1.0 / g_max_B_G, g_max_B_G)
    gR = np.clip(gR, 1.0 / g_max_R,  g_max_R)

    # 应用预增益
    B1 = np.clip(B * gB, 0.0, 1.0)
    G1 = np.clip(G * gG, 0.0, 1.0)
    R1 = np.clip(R * gR, 0.0, 1.0)
    img1 = np.stack([B1, G1, R1], axis=-1)

    # ============================================================
    # Stage 2: 截断 & 亮度约束的 ACCC 迭代
    # ============================================================
    B = img1[..., 0]
    G = img1[..., 1]
    R = img1[..., 2]

    # 重新根据通道均值排序，找 Ia / Ib / Ic
    means = np.array([B.mean(), G.mean(), R.mean()], dtype=np.float32)
    order = np.argsort(means)  # 升序: 最小, 中, 最大
    idx_c = int(order[0])      # 最小 -> Ic
    idx_b = int(order[1])      # 中   -> Ib
    idx_a = int(order[2])      # 最大 -> Ia

    ch_list = [B.copy(), G.copy(), R.copy()]
    Ia = ch_list[idx_a]
    Ib = ch_list[idx_b]
    Ic = ch_list[idx_c]

    # 只在中亮度区域统计均值，避免深阴影/高光影响
    Y1 = 0.114 * B + 0.587 * G + 0.299 * R
    mask_mid = (Y1 > 0.03) & (Y1 < 0.97)

    def _channel_means(Ia_arr, Ib_arr, Ic_arr, mask=None):
        if mask is not None and mask.any():
            Ia_m = float(Ia_arr[mask].mean())
            Ib_m = float(Ib_arr[mask].mean())
            Ic_m = float(Ic_arr[mask].mean())
        else:
            Ia_m = float(Ia_arr.mean())
            Ib_m = float(Ib_arr.mean())
            Ic_m = float(Ic_arr.mean())
        return Ia_m, Ib_m, Ic_m

    prev_loss = None
    for _ in range(max_iters):
        Ia_bar, Ib_bar, Ic_bar = _channel_means(Ia, Ib, Ic, mask_mid)
        diff_b = Ia_bar - Ib_bar
        diff_c = Ia_bar - Ic_bar

        # Loss 定义
        loss = diff_b * diff_b + diff_c * diff_c

        if loss <= loss_thresh:
            break
        if prev_loss is not None and loss > prev_loss:
            # 若损失变大，认为已经过补偿，直接停止
            break
        prev_loss = loss

        # 截断差值，避免一次性补偿过大
        diff_b_clamped = np.clip(diff_b, -accc_delta_max, accc_delta_max)
        diff_c_clamped = np.clip(diff_c, -accc_delta_max, accc_delta_max)

        # 一轮补偿（加入 accc_alpha 控制步长）
        Ib_new = Ib + accc_alpha * diff_b_clamped * (1.0 - Ib) * Ia
        Ic_new = Ic + accc_alpha * diff_c_clamped * (1.0 - Ic) * Ia

        Ib = np.clip(Ib_new, 0.0, 1.0)
        Ic = np.clip(Ic_new, 0.0, 1.0)

    # 映射回 BGR 顺序
    out_ch = [None, None, None]
    out_ch[idx_a] = Ia
    out_ch[idx_b] = Ib
    out_ch[idx_c] = Ic

    B_out = out_ch[0]
    G_out = out_ch[1]
    R_out = out_ch[2]
    bgr_out = np.stack([B_out, G_out, R_out], axis=-1)

    # ============================================================
    # Stage 3: 亮度回调 + 色域保护
    # ============================================================
    if brightness_preserve:
        Y2 = 0.114 * B_out + 0.587 * G_out + 0.299 * R_out
        Y2_mean = float(Y2.mean())
        if Y2_mean > eps and Y0_mean > eps:
            s = Y0_mean / (Y2_mean + eps)
            s = float(np.clip(s, brightness_scale_clip[0], brightness_scale_clip[1]))
            bgr_out = np.clip(bgr_out * s, 0.0, 1.0)

    return bgr_out.astype(np.float32)


if __name__ == "__main__":


    bgr_u8 = cv2.imread("haiyangkadun.4.jpg")          # BGR uint8 0~255
    bgr_f = bgr_u8.astype(np.float32) / 255.0      # 转成 float [0,1]

    bgr_wb = lgs_accc_bgr(bgr_f)

    bgr_wb_u8 = (np.clip(bgr_wb, 0.0, 1.0) * 255.0).astype(np.uint8)
    cv2.imwrite("lgs_image_wb_only.jpg", bgr_wb_u8)

    bgr_wb = lgs_accc_bgr_improved(bgr_f)

    bgr_out_u8 = np.clip(bgr_wb * 255.0, 0, 255).astype(np.uint8)
    cv2.imwrite("haiyangkadun.4_wb_improved2.jpg", bgr_out_u8)


