import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('test1.jpg',0)
img = cv2.medianBlur(img,5)

ret,th1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)

titles = ['Original Image','Global THresholding (v = 127)','Adaptive Mean THresholding','Adaptive Gaussian Thresholding']
image = [img, th1, th2, th3]

for i in range(4):
    plt.subplot(2,2,i+1),plt.imshow(image[i],'gray')
    plt.title(titles[i])
    plt.xticks([]),
    plt.yticks([])

plt.show()
