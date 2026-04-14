def IE(img):
    tmp = []

    for i in range(256):
        tmp.append(0)
    tmp = np.array(tmp)
    tmp = np.float64(tmp)
    val = 0
    k = 0
    res = np.float64(0)
    img = np.array(img)
    for i in range(len(img)):
        for j in range(len(img[i])):
            val = img[i][j]
            tmp[val] = np.float64(tmp[val] + 1)
            k = np.float64(k + 1)
    for i in range(len(tmp)):
        tmp[i] = np.float64(tmp[i] / k)
    for i in range(len(tmp)):
         if(tmp[i] == 0):
             res = res
         else:
             res = np.float64(res - tmp[i] * (math.log(tmp[i]) / math.log(2.0)))
    return res


import cv2
import numpy as np
import math
import time
def get_entropy(img_):
    x, y = img_.shape[0:2]
    # img_ = cv2.resize(img_, (100, 100)) # 缩小的目的是加快计算速度
    tmp = []
    for i in range(256):
        tmp.append(0)
    val = 0
    k = 0
    res = 0
    img = np.array(img_)
    for i in range(len(img)):
        for j in range(len(img[i])):
            val = img[i][j]
            tmp[val] = float(tmp[val] + 1)
            k =  float(k + 1)
    for i in range(len(tmp)):
        tmp[i] = float(tmp[i] / k)
    for i in range(len(tmp)):
        if(tmp[i] == 0):
            res = res
        else:
            res = float(res - tmp[i] * (math.log(tmp[i]) / math.log(2.0)))
    return res