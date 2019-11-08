import numpy as np
import pdb
import cv2
import sys
import scipy.io as sio
import os

image = 'frame_1572625139_rotated.jpg'

points2D_projected_1 = sio.loadmat('points_2D_projected_for_ARCore_frame_1.mat')
points2D_projected_1 = points2D_projected_1['points_2D_projected_for_ARCore_frame']

points2D_projected_2 = sio.loadmat('points_2D_projected_for_ARCore_frame_2.mat')
points2D_projected_2 = points2D_projected_2['points_2D_projected_for_ARCore_frame']

points2D_projected_3 = sio.loadmat('points_2D_projected_for_ARCore_frame_3.mat')
points2D_projected_3 = points2D_projected_3['points_2D_projected_for_ARCore_frame']

points2D_projected_4 = sio.loadmat('points_2D_projected_for_ARCore_frame_4.mat')
points2D_projected_4 = points2D_projected_4['points_2D_projected_for_ARCore_frame']

colmap_points2D = sio.loadmat('colmap_points2D.mat')
colmap_points2D = colmap_points2D['colmap_points2D']

rows = np.shape(colmap_points2D)[0]
img = cv2.imread(image)

for i in range(rows):
    x = int(colmap_points2D[i][0])
    y = int(colmap_points2D[i][1])
    center = (x, y)
    # center = (np.shape(img)[1]-y,x) # weird matlab to python indexing..
    # print "x: " + str(center[0]) + ", y: " + str(center[1])
    cv2.circle(img, center, 4, (0, 0, 255), -1)

cv2.imwrite("matlab_result_0.jpg",img)

rows = np.shape(points2D_projected_1)[0]
img = cv2.imread(image)

for i in range(rows):
    x = int(points2D_projected_1[i][0])
    y = int(points2D_projected_1[i][1])
    center = (x, y)
    # center = (np.shape(img)[1]-y,x) # weird matlab to python indexing..
    # print "x: " + str(center[0]) + ", y: " + str(center[1])
    cv2.circle(img, center, 4, (0, 0, 255), -1)

cv2.imwrite("matlab_result_1.jpg",img)

rows = np.shape(points2D_projected_2)[0]
img = cv2.imread(image)

for i in range(rows):
    x = int(points2D_projected_2[i][0])
    y = int(points2D_projected_2[i][1])
    center = (x, y)
    # center = (np.shape(img)[1]-y,x) # weird matlab to python indexing..
    # print "x: " + str(center[0]) + ", y: " + str(center[1])
    cv2.circle(img, center, 4, (0, 0, 255), -1)

cv2.imwrite("matlab_result_2.jpg",img)

rows = np.shape(points2D_projected_3)[0]
img = cv2.imread(image)

for i in range(rows):
    x = int(points2D_projected_3[i][0])
    y = int(points2D_projected_3[i][1])
    center = (x, y)
    # center = (np.shape(img)[1]-y,x) # weird matlab to python indexing..
    # print "x: " + str(center[0]) + ", y: " + str(center[1])
    cv2.circle(img, center, 4, (0, 0, 255), -1)

cv2.imwrite("matlab_result_3.jpg",img)

rows = np.shape(points2D_projected_4)[0]
img = cv2.imread(image)

for i in range(rows):
    x = int(points2D_projected_4[i][0])
    y = int(points2D_projected_4[i][1])
    center = (x, y)
    # center = (np.shape(img)[1]-y,x) # weird matlab to python indexing..
    # print "x: " + str(center[0]) + ", y: " + str(center[1])
    cv2.circle(img, center, 4, (0, 0, 255), -1)

cv2.imwrite("matlab_result_4.jpg",img)
