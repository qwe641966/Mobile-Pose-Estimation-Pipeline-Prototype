import numpy as np
import pdb
import cv2
import sys
import scipy.io as sio
import os

image = 'frame_1572625116.jpg'

colmap_to_arcore_points2D = sio.loadmat('colmap_points2D_mine.mat')
colmap_to_arcore_points2D = colmap_to_arcore_points2D['points_2D_projected_for_ARCore_frame']

rows = np.shape(colmap_to_arcore_points2D)[0]
img = cv2.imread(image)

for i in range(rows):
    x = int(colmap_to_arcore_points2D[i][0])
    y = int(colmap_to_arcore_points2D[i][1])
    center = (x, y)
    # center = (np.shape(img)[1]-y,x) # weird matlab to python indexing..
    # print "x: " + str(center[0]) + ", y: " + str(center[1])
    cv2.circle(img, center, 4, (0, 0, 255), -1)

cv2.imwrite("matlab_result_colmap_to_arcore.jpg",img)

colmap_original_points2D = sio.loadmat('colmap_points2D_original.mat')
colmap_original_points2D = colmap_original_points2D['colmap_points2D']

rows = np.shape(colmap_to_arcore_points2D)[0]
img = cv2.imread(image)

for i in range(rows):
    x = int(colmap_to_arcore_points2D[i][0])
    y = int(colmap_to_arcore_points2D[i][1])
    center = (x, y)
    # center = (np.shape(img)[1]-y,x) # weird matlab to python indexing..
    # print "x: " + str(center[0]) + ", y: " + str(center[1])
    cv2.circle(img, center, 4, (0, 0, 255), -1)

cv2.imwrite("matlab_result_colmap_original.jpg",img)

