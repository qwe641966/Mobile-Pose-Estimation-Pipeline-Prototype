import numpy as np
import pdb
import cv2
import sys
import scipy.io as sio
import os

query_image_path = sys.argv[1]
benchmarking = sys.argv[2]
query_image_name = query_image_path.rsplit("/",1)[1].split(".")[0]

points2D_projected_direct_matching = np.loadtxt("results/"+query_image_name+"/points2D_projected_direct_matching.txt")
points2D_projected_image_retrieval = np.loadtxt("results/"+query_image_name+"/points2D_projected_image_retrieval.txt")

# Direct Matching
rows = np.shape(points2D_projected_direct_matching)[0]
img = cv2.imread(query_image_path)

for i in range(rows):
    x = int(points2D_projected_direct_matching[i][0])
    y = int(points2D_projected_direct_matching[i][1])
    center = (x, y)
    # center = (np.shape(img)[1]-y,x) # weird matlab to python indexing..
    # print "x: " + str(center[0]) + ", y: " + str(center[1])
    cv2.circle(img, center, 4, (0, 0, 255), -1)

cv2.imwrite("results/" + query_image_name + "_result_direct_matching.png",img)

# Image Retrieval
rows = np.shape(points2D_projected_image_retrieval)[0]
img = cv2.imread(query_image_path)

for i in range(rows):
    x = int(points2D_projected_image_retrieval[i][0])
    y = int(points2D_projected_image_retrieval[i][1])
    center = (x, y)
    # center = (np.shape(img)[1]-y,x) # weird matlab to python indexing..
    # print "x: " + str(center[0]) + ", y: " + str(center[1])
    cv2.circle(img, center, 4, (0, 0, 255), -1)

cv2.imwrite("results/" + query_image_name + "_result_image_retrieval.png",img)

# if(benchmarking != "1"):
#     os.system("open results/" + query_image_name + "_result_direct_matching.png")
#     os.system("open results/" + query_image_name + "_result_image_retrieval.png")