import numpy as np
import pdb
import cv2
import sys
import scipy.io as sio
import os

query_image = sys.argv[1]

points_correspondences = sio.loadmat('final_match_array.mat')
points_correspondences = points_correspondences['value']

points2D = points_correspondences[:,0:2]
points3D = points_correspondences[:,2:5]

cameraParams = sio.loadmat('camera_intrinsics.mat')
cameraParams = cameraParams['value']

focalLength = cameraParams[0,0]
center = np.array([cameraParams[0,1], cameraParams[0,2]])
intrinsicMatrix = np.array([ focalLength, 0, 0, 0, focalLength, 0, center[0], center[1], 1])
intrinsicMatrix = intrinsicMatrix.reshape(3,3)
radialDistortion = np.array([0, 0])

pnp_ransac_rot = sio.loadmat('pnp_ransac_rotation_vector.mat')
pnp_ransac_rot = pnp_ransac_rot['value']
pnp_ransac_trans = sio.loadmat('pnp_ransac_translation_vector.mat')
pnp_ransac_trans = pnp_ransac_trans['value']

pnp_ransac_rot = cv2.Rodrigues(pnp_ransac_rot)[0]

no_points3D = np.shape(points3D)[0]
ones = np.ones(no_points3D)
ones = ones.reshape(no_points3D,1)
points3D = np.concatenate((points3D, ones), axis=1)

points2D_projected = np.dot(np.dot(np.transpose(intrinsicMatrix), np.concatenate((pnp_ransac_rot, pnp_ransac_trans),axis=1)), np.transpose(points3D))
points2D_projected = np.transpose(points2D_projected)
points2D_projected = points2D_projected / points2D_projected[:,2].reshape(no_points3D,1)
points2D_projected = np.round(points2D_projected)
points2D_projected = points2D_projected[:,0:2]

rows = np.shape(points2D_projected)[0]
img = cv2.imread("query_image/"+query_image)

for i in range(rows):
    x = int(points2D_projected[i][0])
    y = int(points2D_projected[i][1])
    center = (np.shape(img)[1]-y,x) # weird matlab to python indexing..
    cv2.circle(img, center, 10, (0, 0, 255), -1)

cv2.imwrite('result.png',img)
os.system("open result.png")