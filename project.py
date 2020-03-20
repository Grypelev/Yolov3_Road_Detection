import numpy as np
import cv2
import matplotlib.pyplot as plt
import json
from math import sqrt, cos, degrees, atan, radians
import os


def triangle_solver(a,adj):
    opposite = sqrt((adj/cos(radians(a)))**2 - adj**2)
    return opposite

def a_and_adj_solver(x1, y1, x2, y2, height):
    if x1 < x2:flag = 1
    else: flag = 0
    a = degrees(atan(abs(x2-x1)/abs(y1-y2)))
    adj = abs(y1-y2)
    return a, adj, flag

def rectangles(edges):
    a,b = edges.shape
    rects = np.zeros((a,b))
    for i in range(a):
        rects[i,0] = max(0, int((edges[i][0] - (edges[i][2]/2))*width))
        rects[i,1] = max(0, int((edges[i][1] - (edges[i][3]/2)) * height))
        rects[i,2] = min(width, int((edges[i][0] + (edges[i][2]/2))*width))
        rects[i,3] = rects[i,1]
    return rects

def points(data, height, width):
    left=0
    right=0
    num_of_boxes = len(data[0]['objects'])
    edges = np.zeros((num_of_boxes, 4))
    for i in range(num_of_boxes):
        edges[i][0] = data[0]['objects'][i]['relative_coordinates']['center_x']
        edges[i][1] = data[0]['objects'][i]['relative_coordinates']['center_y']
        edges[i][2] = data[0]['objects'][i]['relative_coordinates']['width']
        edges[i][3] = data[0]['objects'][i]['relative_coordinates']['height']
        rects = rectangles(edges) 

    if num_of_boxes > 1: 
        pts = np.array([
            [rects[np.argmin(rects[:,1]),2], rects[np.argmin(rects[:,1]),3]], 
            [rects[np.argmin(rects[:,1]),0], rects[np.argmin(rects[:,1]),1]], 
            [rects[np.argmin(rects[:,0]),0], rects[np.argmin(rects[:,0]),1]],
            [0, height],
            [width, height],
            [rects[np.argmax(rects[:,3]),2], rects[np.argmax(rects[:,3]),3]]
            ])
        
        a, adj, flag = a_and_adj_solver(pts[2,0], pts[2,1], pts[1,0], pts[1,1], height)
        opposite = triangle_solver(a,adj)
        if flag == 1:
            tmp = pts[2,0]
            pts[2,0] = pts[2,0] - opposite
            if pts[2,0] >=0:
                pts[2,1] = height
                left=1
            elif pts[2,0] < 0:
                pts[2,0] = 0
                pts[2,1] = height- ((height - pts[2,1]) - triangle_solver(90-a,tmp))
        
        a, adj, flag = a_and_adj_solver(pts[5,0], pts[5,1], pts[0,0], pts[0,1], height)
        opposite = triangle_solver(a,adj)
        if flag == 0:
            tmp = pts[5,0]
            pts[5,0] = pts[5,0] + opposite
            if pts[5,0] <= width:
                pts[5,1] = height
                right=1
            elif pts[5,0] > width:
                pts[5,0] = width
                pts[5,1] = height- ((height - pts[5,1]) - triangle_solver(90-a,width-tmp))
        

        if right == 1:
            pts = np.delete(pts,4,0)
        if left == 1:
            pts = np.delete(pts,3,0)
    
    elif num_of_boxes == 1:

        pts = np.array([[rects[0,2], rects[0,3]], 
                        [rects[0,0], rects[0,1]], 
                        [rects[0,0], height], 
                        [rects[0,2], height]])
        print(rects)

    else:
        print("There is no object recognized. Try again!")
        exit()

    pts = pts.astype(int)  
    return pts


with open('result.json') as f:
    data = json.load(f)

print("Enter file name: ")
name = input()
img = cv2.imread(name) 
# img = cv2.imread("test14.jpg") 
height,width = img.shape[0:2]

print("Do you prefer to increase contrast?  (y|n)")
if input() == 'y':
    print("Nice. Do you want to allow equalizeHist (grayscale)?  (y|n)")
    if input() == 'y':
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        img = cv2.equalizeHist(gray)
    else:
        print("So the contrast will be regulized by a constant value")
        alpha = 1.5
        beta = 0
        img = cv2.addWeighted(img, alpha, np.zeros(img.shape, img.dtype), 0, beta)






# height = img.shape[0]
# width = img.shape[1]

pts = points(data,height,width)
# print(pts)
## (1) Crop the bounding rect
rect = cv2.boundingRect(pts)
x,y,w,h = rect
croped = img[y:y+h, x:x+w].copy()

## (2) make mask
pts = pts - pts.min(axis=0)

mask = np.zeros(croped.shape[:2], np.uint8)
cv2.drawContours(mask, [pts], -1, (255, 255, 255), -1, cv2.LINE_AA)

## (3) do bit-op
dst = cv2.bitwise_and(croped, croped, mask=mask)

## (4) add the white background
bg = np.ones_like(croped, np.uint8)*255
cv2.bitwise_not(bg,bg, mask=mask)
dst2 = bg + dst

#cv2.imwrite("croped.jpg", croped)
#cv2.imwrite("mask.jpg", mask)
cv2.imwrite("dst.jpg", dst)
#cv2.imwrite("dst2.jpg", dst2)
# plt.imshow(dst)
# plt.show()

##############################################################


# cv2.imwrite("result_rgb.jpg", img)
# cv2.imwrite("result_gray.jpg", equalized_gray)