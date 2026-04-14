import cv2
import numpy as np

def homomorphic_filter(img, gamma_low=0.5, gamma_high=1.8, cutoff_freq=65):
    """
    应用同态滤波来校正非均匀光照并增强细节。
    
    参数:
    img (numpy.ndarray): 输入图像 (应为单通道灰度图)。
    gamma_low (float): 低频增益 (小于1以压缩动态范围)。
    gamma_high (float): 高频增益 (大于1以增强细节)。
    cutoff_freq (int): 截止频率 (高斯高通滤波器的D0)。
    """
    
    # 1. 检查图像是否为单通道
    if len(img.shape) == 3:
        # 如果是彩色图，在V通道或L通道处理
        # 为简单起见，此处转为灰度图。
        # 更好的方法是在L*a*b*的L通道上执行此操作（见第三部分）
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        img_gray = img
        
    # 2. 转换为浮点数并取对数 (I -> log(I))
    # 加1以避免log(0) 
    img_log = np.log1p(img_gray.astype(np.float32))

    # 3. 傅里叶变换 (log(I) -> F(log(I)))
    img_fft = np.fft.fft2(img_log)
    img_fft_shifted = np.fft.fftshift(img_fft)

    # 4. 构建高斯高通滤波器 (Butterworth或Gaussian均可) [30]
    rows, cols = img_gray.shape
    u, v = np.meshgrid(np.arange(cols), np.arange(rows))
    center_u, center_v = cols // 2, rows // 2
    
    # D(u,v) - 距离中心的距离
    D_sq = (u - center_u)**2 + (v - center_v)**2
    
    # 高斯高通滤波器的传递函数 H(u,v)
    # H(u,v) = (gamma_high - gamma_low) * (1 - exp(-c * D^2 / D0^2)) + gamma_low
    # 我们使用一个简化的形式，c=1
    H = (gamma_high - gamma_low) * (1 - np.exp(-(D_sq / (2 * cutoff_freq**2)))) + gamma_low
    
    # 5. 应用滤波器 (F(log(I)) * H)
    img_fft_filtered = img_fft_shifted * H

    # 6. 逆傅里叶变换 (F' -> log(I)')
    img_ifft_shifted = np.fft.ifftshift(img_fft_filtered)
    img_ifft = np.fft.ifft2(img_ifft_shifted)

    # 7. 取指数 (log(I)' -> I')
    # 取实部并反对数化
    img_filtered = np.real(img_ifft)
    img_exp = np.expm1(img_filtered) # exp(x) - 1

    # 8. 归一化到 
    # img_enhanced = cv2.normalize(img_exp, None, 0.0, 1.0, cv2.NORM_MINMAX, dtype=cv2.CV_32F)
    img_enhanced = cv2.normalize(img_exp, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    return img_enhanced
import cv2
import numpy as np

def entropy_boost_Lab(
    img_bgr,
    p_low=1.0, p_high=99.0,   # 亮度分位数，调节拉伸强度
    clahe_clip=1.4,           # 局部对比限制，1.2~1.8 之间
    clahe_tile=(8, 8),        # 分块大小
    mix_global=0.6,           # 全局拉伸占比
    mix_local=0.4,            # 局部 CLAHE 占比
    chroma_gain=1.03          # 轻微色度增益，1.0~1.06
):
    """
    输入:  BGR uint8 [0,255] 或 float32 [0,1]
    输出:  BGR uint8 [0,255]
    作用:  只在 Lab 的 L 上拉开直方图 + 一点点 CLAHE，稍微拉饱和度 → 提高 Entropy/UCIQE
    """
    arr = np.asarray(img_bgr)
    if arr.dtype == np.uint8:
        img01 = arr.astype(np.float32) / 255.0
    else:
        img01 = np.clip(arr.astype(np.float32), 0.0, 1.0)

    # BGR -> Lab
    lab = cv2.cvtColor(img01, cv2.COLOR_BGR2LAB).astype(np.float32)
    L, a, b = lab[..., 0], lab[..., 1], lab[..., 2]

    # ---- (1) L 的全局分位拉伸 ----
    lo, hi = np.percentile(L, [p_low, p_high])
    if hi <= lo + 1e-3:
        Lg = L.copy()
    else:
        Lg = np.clip((L - lo) * (100.0 / (hi - lo)), 0.0, 100.0)

    # ---- (2) L 上做一个弱 CLAHE（局部对比）----
    L_u8 = np.clip(np.round(L / 100.0 * 255.0), 0, 255).astype(np.uint8)
    clahe = cv2.createCLAHE(clipLimit=float(clahe_clip),
                            tileGridSize=tuple(clahe_tile))
    Lc_u8 = clahe.apply(L_u8)
    Lc = (Lc_u8.astype(np.float32) / 255.0) * 100.0

    # ---- (3) 三路融合：原始 L、全局拉伸 Lg、局部 CLAHE Lc ----
    # 这里给一点原始 L，防止太激进
    w0 = 1.0 - mix_global - mix_local
    w0 = max(0.0, w0)      # 防止权重负值
    wg = float(mix_global)
    wl = float(mix_local)

    L_new = np.clip(w0 * L + wg * Lg + wl * Lc, 0.0, 100.0)

    # ---- (4) 色度轻微增强（围绕 0 拉开一点）----
    if chroma_gain is not None and abs(chroma_gain - 1.0) > 1e-3:
        cg = float(chroma_gain)
        a0, b0 = a.copy(), b.copy()
        a = np.clip(a * cg, -127.0, 127.0)
        b = np.clip(b * cg, -127.0, 127.0)

        # 控制 std 不超过原来的 ~1.1 倍，防止过饱和
        std_a0, std_b0 = float(np.std(a0)), float(np.std(b0))
        std_a1, std_b1 = float(np.std(a)),  float(np.std(b))
        if std_a1 > 1e-6 and std_a0 > 1e-6:
            a *= min(1.1, std_a0 / (std_a1 + 1e-6) * 1.05)
        if std_b1 > 1e-6 and std_b0 > 1e-6:
            b *= min(1.1, std_b0 / (std_b1 + 1e-6) * 1.05)

    lab_new = np.stack([L_new, a, b], axis=-1).astype(np.float32)
    out01 = cv2.cvtColor(lab_new, cv2.COLOR_LAB2BGR)
    out01 = np.clip(out01, 0.0, 1.0)
    return np.clip(out01 * 255.0, 0, 255).astype(np.uint8)

def Gaussian_lvbo(
    img_dark_fused,
    gamma_low=0.5,
    gamma_high=1.8,
    cutoff_freq=65,
    brightness_match=True,
):
    # 输入bgr[0,255] uint8
    # 输出bgr[0,255] uint8
    lab = cv2.cvtColor(img_dark_fused, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    # 3. 仅对L通道应用同态滤波
    l_enhanced = homomorphic_filter(
        l,
        gamma_low=float(gamma_low),
        gamma_high=float(gamma_high),
        cutoff_freq=float(cutoff_freq),
    )

    # 4. 合并通道并转回BGR
    lab_enhanced = cv2.merge((l_enhanced, a, b))
    img_final_homomorphic = cv2.cvtColor(lab_enhanced, cv2.COLOR_LAB2BGR)
    # 5. 亮度恢复：计算缩放因子
    before_gray = (0.2126 * img_dark_fused[:, :, 2] + 0.7152 * img_dark_fused[:, :, 1] + 0.0722 * img_dark_fused[
        :, :, 0]).astype(np.float32)
    after_gray = (0.2126 * img_final_homomorphic[:, :, 2] + 0.7152 * img_final_homomorphic[:, :, 1] + 0.0722 *
                  img_final_homomorphic[:, :, 0]).astype(np.float32)
    scale = float(np.mean(before_gray) / (np.mean(after_gray) + 1e-6)) if brightness_match else 1.0

    # 按比例缩放滤波结果，使整体亮度与原图接近
    out = np.clip(img_final_homomorphic.astype(np.float32) * scale, 0, 255).astype(np.uint8)
    return out

if __name__ == '__main__':
    # 1. 加载您已生成的、偏暗的融合图像
    img_dark_fused = cv2.imread('haiyangkadun.3_original_Fused.jpg')
    # 输入bgr[0,255] uint8
    # 输出bgr[0,255] uint8
    # 2. 为保持色彩在L*a*b*空间处理L通道
    lab = cv2.cvtColor(img_dark_fused, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    # 3. 仅对L通道应用同态滤波
    l_enhanced = homomorphic_filter(l, gamma_low=0.5, gamma_high=1.8, cutoff_freq=65)

    # 4. 合并通道并转回BGR
    lab_enhanced = cv2.merge((l_enhanced, a, b))
    img_final_homomorphic = cv2.cvtColor(lab_enhanced, cv2.COLOR_LAB2BGR)
    # 5. 亮度恢复：计算缩放因子
    before_gray = (0.2126 * img_dark_fused[:, :, 2] + 0.7152 * img_dark_fused[:, :, 1] + 0.0722 * img_dark_fused[
        :, :, 0]).astype(np.float32)
    after_gray = (0.2126 * img_final_homomorphic[:, :, 2] + 0.7152 * img_final_homomorphic[:, :, 1] + 0.0722 *
                  img_final_homomorphic[:, :, 0]).astype(np.float32)
    scale = float(np.mean(before_gray) / (np.mean(after_gray) + 1e-6))

    # 按比例缩放滤波结果，使整体亮度与原图接近
    out = np.clip(img_final_homomorphic.astype(np.float32) * scale, 0, 255).astype(np.uint8)
    cv2.imwrite('haiyangkadun.3_original_Fused_phic.jpg', out)
