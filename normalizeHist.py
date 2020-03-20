import numpy as np
import cv2 
from matplotlib import pyplot as plt

img = cv2.imread('dst.jpg',0)
equ = cv2.equalizeHist(img)
# res = np.hstack((img,equ))



cv2.imshow("result", equ)
cv2.waitKey(0)