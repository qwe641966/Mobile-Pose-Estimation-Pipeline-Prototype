import numpy as np
import pdb
import cv2
import sys
import scipy.io as sio
import os

query_image_path = sys.argv[1]
intrinsics_matrix_path = sys.argv[2]
query_image_name = query_image_path.rsplit("/",1)[1].split(".")[0]

points_correspondences = np.loadtxt("results/"+query_image_name+"/final_match_array.txt")
intrinsic_matrix = np.loadtxt(intrinsics_matrix_path)

points3D = points_correspondences[:,2:5]

# Switch between the ones below:
# Image Retrieval
pnp_ransac_rot = np.loadtxt("results/"+query_image_name+"/pnp_ransac_rotation_vector_direct.txt")
pnp_ransac_trans = np.loadtxt("results/"+query_image_name+"/pnp_ransac_translation_vector_direct.txt")
# Direct Matching
# pnp_ransac_rot = np.loadtxt("results/"+query_image_name+"/pnp_ransac_rotation_vector_image_retrieval.txt")
# pnp_ransac_trans = np.loadtxt("results/"+query_image_name+"/pnp_ransac_translation_vector_image_retrieval.txt")

pnp_ransac_rot = cv2.Rodrigues(pnp_ransac_rot)[0]

no_points3D = np.shape(points3D)[0]
ones = np.ones(no_points3D)
ones = ones.reshape(no_points3D,1)
points3D = np.concatenate((points3D, ones), axis=1) #make homogeneous

points2D_projected = np.dot(np.dot(intrinsic_matrix, np.concatenate((pnp_ransac_rot, pnp_ransac_trans.reshape([3,1])),axis=1)), np.transpose(points3D))
points2D_projected = np.transpose(points2D_projected)
points2D_projected = points2D_projected / points2D_projected[:,2].reshape(no_points3D,1)
points2D_projected = np.round(points2D_projected)
points2D_projected = points2D_projected[:,0:2]

rows = np.shape(points2D_projected)[0]
img = cv2.imread(query_image_path)

for i in range(rows):
    x = int(points2D_projected[i][0])
    y = int(points2D_projected[i][1])
    center = (x,y)
    # center = (np.shape(img)[1]-y,x) # weird matlab to python indexing..
    # print "x: " + str(center[0]) + ", y: " + str(center[1])
    cv2.circle(img, center, 9, (0, 0, 255), -1)

cv2.imwrite("results/" + query_image_name + "_result.png",img)
# do not use the following when doing batch
os.system("open results/" + query_image_name + "_result.png")