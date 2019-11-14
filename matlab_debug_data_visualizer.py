import numpy as np
import pdb
import cv2
import sys
import scipy.io as sio
import os

image = 'frame_1573310727320.jpg'

colmap_to_arcore_points2D = sio.loadmat('points2D_frame_1573310727320.mat')
colmap_to_arcore_points2D = colmap_to_arcore_points2D['points2D']

rows = np.shape(colmap_to_arcore_points2D)[0]
img = cv2.imread(image)

for i in range(rows):
    x = int(colmap_to_arcore_points2D[i][0])
    y = int(colmap_to_arcore_points2D[i][1])
    center = (x, y)
    # center = (np.shape(img)[1]-y,x) # weird matlab to python indexing..
    # print "x: " + str(center[0]) + ", y: " + str(center[1])
    cv2.circle(img, center, 4, (0, 0, 255), -1)

cv2.imwrite("frame_1573310727320_result.jpg",img)

image = 'frame_1573310727320.jpg'

colmap_to_arcore_points2D = sio.loadmat('points2D_frame_1573310727320_colmap.mat')
colmap_to_arcore_points2D = colmap_to_arcore_points2D['points2D']

rows = np.shape(colmap_to_arcore_points2D)[0]
img = cv2.imread(image)

for i in range(rows):
    x = int(colmap_to_arcore_points2D[i][0])
    y = int(colmap_to_arcore_points2D[i][1])
    center = (x, y)
    # center = (np.shape(img)[1]-y,x) # weird matlab to python indexing..
    # print "x: " + str(center[0]) + ", y: " + str(center[1])
    cv2.circle(img, center, 4, (0, 0, 255), -1)

cv2.imwrite("frame_1573310727320_result_colmap.jpg",img)
