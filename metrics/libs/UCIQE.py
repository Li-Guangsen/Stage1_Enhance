import cv2
import numpy as np

def calc_uciqe(bgr_img: np.ndarray) -> float:
    """
    计算 UCIQE 指标
    输入：BGR uint8 图像 (H, W, 3)
    输出：float (UCIQE 数值)
    """

    if bgr_img is None:
        raise ValueError("Input image is None")

    # 转 Lab 空间
    lab = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2LAB).astype(np.float32)
    L, a, b = cv2.split(lab)

    # 1) 色度 C = sqrt(a^2 + b^2)
    C = np.sqrt(a ** 2 + b ** 2)
    sigma_c = np.std(C)               # 色度标准差

    # 2) 亮度对比度 con_l
    # 这里用 L 通道的 1% 和 99% 分位数之差 / 中值，常见写法
    L_vec = L.flatten()
    L_sorted = np.sort(L_vec)
    n = L_sorted.size
    L_1 = L_sorted[int(0.01 * n)]
    L_99 = L_sorted[int(0.99 * n)]
    con_l = (L_99 - L_1) / max(L_99 + L_1, 1e-6)

    # 3) 饱和度均值 μs
    # 先转 HSV 计算饱和度
    hsv = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2HSV).astype(np.float32)
    H, S, V = cv2.split(hsv)
    mu_s = np.mean(S / 255.0)         # 归一化到 [0,1]

    # 线性组合系数（来自原文）
    k1, k2, k3 = 0.4680, 0.2745, 0.2576
    uciqe = k1 * sigma_c + k2 * con_l + k3 * mu_s
    return float(uciqe)
