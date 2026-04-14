import numpy as np
import math
def EMEE(img, L=10):
    alpha = 0.3
    h, w = img.shape
    how_many = int( h / L)
    e = 0

    m1 = 1
    for i in range(0,how_many):
        n1 = 1
        for n in range(0,how_many):
            b1 = img[m1:m1 + L - 1, n1:n1 + L - 1]
            # B1 = np.array(B1)
            b_min = np.amin(b1)
            b_max = np.amax(b1)

            if b_min > 0:
                b_ratio = b_max / b_min
                e = e + alpha * (b_ratio ** alpha) + math.log(b_ratio)

            n1 = n1 + L
        m1 = m1 + L
    e = (e / how_many) / how_many
    return e


