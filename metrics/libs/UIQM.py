import cv2
import numpy as np

def _uicm(bgr_img: np.ndarray) -> float:
    """
    Underwater Image Colorfulness Measure (简化版)
    """
    img = bgr_img.astype(np.float32)
    B, G, R = cv2.split(img)

    # 转成 RG 和 YB 色彩空间
    RG = R - G
    YB = 0.5 * (R + G) - B

    # 统计特征
    rg_mean, rg_std = np.mean(RG), np.std(RG)
    yb_mean, yb_std = np.mean(YB), np.std(YB)

    # 颜色丰富度度量（类似 Hasler & Süsstrunk 的公式）
    alpha = np.sqrt(rg_std ** 2 + yb_std ** 2)
    beta = np.sqrt(rg_mean ** 2 + yb_mean ** 2)
    uicm = alpha + 0.3 * beta
    return float(uicm)

def _local_eme(block, eps=1e-6):
    """
    计算单个块的 EME（对数对比）
    """
    block = block.astype(np.float32)
    max_val = np.max(block)
    min_val = np.min(block)
    if max_val < eps or min_val < eps or max_val == min_val:
        return 0.0
    return 20.0 * np.log10(max_val / (min_val + eps))


def _uism(bgr_img: np.ndarray, block_size: int = 10) -> float:
    """
    Underwater Image Sharpness Measure
    使用灰度梯度 + EME 思路
    """
    # 转灰度或取 V 通道
    hsv = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2HSV)
    _, _, V = cv2.split(hsv)
    V = V.astype(np.float32)

    # Sobel 梯度
    gx = cv2.Sobel(V, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(V, cv2.CV_32F, 0, 1, ksize=3)
    grad = np.hypot(gx, gy)

    h, w = grad.shape
    bs = block_size
    eme_sum = 0.0
    count = 0

    # 分块计算 EME
    for i in range(0, h - bs + 1, bs):
        for j in range(0, w - bs + 1, bs):
            block = grad[i:i+bs, j:j+bs]
            eme_sum += _local_eme(block)
            count += 1

    if count == 0:
        return 0.0
    return float(eme_sum / count)

def _uiconm(bgr_img: np.ndarray, block_size: int = 10) -> float:
    """
    Underwater Image Contrast Measure
    """
    # 亮度通道（Y 或 V、L 都可以，这里用 Y）
    ycrcb = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2YCrCb)
    Y, _, _ = cv2.split(ycrcb)
    Y = Y.astype(np.float32)

    h, w = Y.shape
    bs = block_size
    eme_sum = 0.0
    count = 0

    for i in range(0, h - bs + 1, bs):
        for j in range(0, w - bs + 1, bs):
            block = Y[i:i+bs, j:j+bs]
            eme_sum += _local_eme(block)
            count += 1

    if count == 0:
        return 0.0
    return float(eme_sum / count)

def calc_uiqm(bgr_img: np.ndarray) -> float:
    """
    计算 UIQM 指标
    输入：BGR uint8 图像
    输出：float
    """
    # 三个子指标
    uicm = _uicm(bgr_img)
    uism = _uism(bgr_img)
    uiconm = _uiconm(bgr_img)

    # 原文推荐权重
    c1, c2, c3 = 0.0282, 0.2953, 3.5753
    uiqm = c1 * uicm + c2 * uism + c3 * uiconm

    return float(uiqm)
