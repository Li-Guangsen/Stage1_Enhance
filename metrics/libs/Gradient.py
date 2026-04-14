import numpy as np
import math


def Gradient(img):
    height, width = img.shape
    total = 0
    # img1 = cv2.cvtColor(in, cv2.COLOR_BGR2GRAY)  # 彩色转为灰度图片
    img1 = np.float32(img)
    for i in range(1,height):
        for j in range(1,width):
            piandaox = img1[i,j] - img1[i-1,j]
            piandaoy = img1[i,j] - img1[i,j-1]
            total = math.sqrt(piandaox ** 2 + piandaoy ** 2) + total
    avg_gradient = total / ((height - 1)*(width - 1))
    return avg_gradient



