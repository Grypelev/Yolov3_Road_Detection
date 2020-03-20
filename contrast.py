import numpy as np
import cv2
import matplotlib.pyplot as plt
import json
import os


# os.environ["opinion"]
# print(opinion)


# print("Enter file name: ")
# name = input()
# img = cv2.imread(name) 
img = cv2.imread('dst.jpg',0)
equ = cv2.equalizeHist(img)

height = img.shape[0]
width = img.shape[1]

alpha = 2
beta = 0

res = cv2.addWeighted(img, alpha, np.zeros(img.shape, img.dtype), 0, beta)

# res = np.hstack((img,equ))

cv2.imwrite("result_rgb.jpg", equ)
cv2.imwrite("result_gray.jpg", res)

# cv2.imshow("result", result)
# cv2.waitKey(0)
# cv2.destroyAllWindows