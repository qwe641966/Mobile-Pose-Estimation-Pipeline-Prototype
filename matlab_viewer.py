import numpy as np
import pdb
import cv2
import sys
import scipy.io as sio
import os


points2D = np.loadtxt("matlab_debug_data/data_ar/cpuImageCorrespondencesXY.txt")

rows = np.shape(points2D)[0]
img = cv2.imread("matlab_debug_data/data_ar/cpuFrame.jpg")

for i in range(rows):
    x = int(points2D[i][0])
    y = int(points2D[i][1])
    center = (x, y)
    # center = (np.shape(img)[1]-y,x) # weird matlab to python indexing..
    # print "x: " + str(center[0]) + ", y: " + str(center[1])
    cv2.circle(img, center, 3, (0, 0, 255), -1)

cv2.imwrite("matlab_debug_data/data_ar/result.jpg",img)

cpuCameraIntrinsics = np.loadtxt("matlab_debug_data/data_ar/cpuCameraIntrinsics.txt")
opencv_2D3D = np.loadtxt("matlab_debug_data/data_ar/opencv_2D3D.txt")

# verify pose
(_, R, t, inliers) = cv2.solvePnPRansac(opencv_2D3D[:,2:5], opencv_2D3D[:,0:2], cpuCameraIntrinsics, None, iterationsCount = 500, confidence = 0.99, flags = cv2.SOLVEPNP_EPNP)
R = cv2.Rodrigues(R)[0]

pdb.set_trace()