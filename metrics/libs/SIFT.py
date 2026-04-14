import numpy as np
import cv2
from matplotlib import pyplot as plt

def SIFT(img):

    sift = cv2.SIFT_create()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    kp,des = sift.detectAndCompute(gray,None)

    img1=cv2.drawKeypoints(img,kp,img,color=(255,0,255))

    print("关键点数目:", len(kp))
    return img1

def get_keypoint(img):

    sift = cv2.SIFT_create()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    kp,des = sift.detectAndCompute(gray,None)

    return len(kp)

