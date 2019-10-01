import numpy as np
import pdb
import cv2
import sys
import scipy.io as sio
import os


points2D_projected_direct_matching = np.loadtxt("matlab_debug_data/data_ar/xy.txt")


# Direct Matching
rows = np.shape(points2D_projected_direct_matching)[0]
img = cv2.imread("matlab_debug_data/data_ar/frame.jpg")

for i in range(rows):
    x = int(points2D_projected_direct_matching[i][0])
    y = int(points2D_projected_direct_matching[i][1])
    print str(x) + ", " + str(y)
    center = (x, y)
    # center = (np.shape(img)[1]-y,x) # weird matlab to python indexing..
    # print "x: " + str(center[0]) + ", y: " + str(center[1])
    cv2.circle(img, center, 12, (0, 0, 255), -1)

cv2.imwrite("matlab_debug_data/data_ar/res.jpg",img)