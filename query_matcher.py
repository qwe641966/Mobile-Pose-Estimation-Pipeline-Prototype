import sqlite3
import numpy as np
import pdb
import sys
import cv2
import scipy.io as sio
import os
import math

# This file will return the camera intrinsics of the query image and also the
# initial rotation and translation from the similar image to the query image in the database.
#
# when RANSAC is used then it will apply SIFT matching between the sift features of the
# query image and the similar image. Then the final array will be a correspondences array
# between the 2D points of the query image and 3D points (that were fetched from the similar image - that already had
# the 3D points data from COLMAP)

database_dir = sys.argv[1]
data_dir = sys.argv[2]
query_image_name = sys.argv[3]

IS_PYTHON3 = sys.version_info[0] >= 3

class COLMAPDatabase(sqlite3.Connection):

    @staticmethod
    def connect(database_path):
        return sqlite3.connect(database_path, factory=COLMAPDatabase)

def blob_to_array(blob, dtype, shape=(-1,)):
    if IS_PYTHON3:
        return np.fromstring(blob, dtype=dtype).reshape(*shape)
    else:
        return np.frombuffer(blob, dtype=dtype).reshape(*shape)

def truncate(f, n):
    return math.floor(f * 10 ** n) / 10 ** n

db = COLMAPDatabase.connect(database_dir)

#Note: the sift features should be extracted from COLMAP so they match the ones from the SFM dataset

#query image stuff
query_image_id = '1' #usually one as there is only 1

query_image_keypoints_data = db.execute("SELECT data FROM keypoints WHERE image_id = "+ "'" + query_image_id + "'")
query_image_keypoints_data = query_image_keypoints_data.fetchone()[0]
query_image_keypoints_data_cols = db.execute("SELECT cols FROM keypoints WHERE image_id = "+ "'" + query_image_id + "'")
query_image_keypoints_data_cols = int(query_image_keypoints_data_cols.fetchone()[0])
query_image_keypoints_data = blob_to_array(query_image_keypoints_data, np.float32)
query_image_keypoints_data_rows = np.shape(query_image_keypoints_data)[0]/query_image_keypoints_data_cols
query_image_keypoints_data = query_image_keypoints_data.reshape(query_image_keypoints_data_rows, query_image_keypoints_data_cols)
query_image_keypoints_data_xy = query_image_keypoints_data[:,0:2]

query_image_descriptors_data = db.execute("SELECT data FROM descriptors WHERE image_id = "+ "'" + query_image_id + "'")
query_image_descriptors_data = query_image_descriptors_data.fetchone()[0]
query_image_descriptors_data = blob_to_array(query_image_descriptors_data, np.uint8)
descs_rows = np.shape(query_image_descriptors_data)[0]/128
query_image_descriptors_data = query_image_descriptors_data.reshape([descs_rows,128])

query_keypoints_xy_descriptors = np.concatenate((query_image_keypoints_data_xy, query_image_descriptors_data), axis=1)
points2D_for_softposit = query_keypoints_xy_descriptors[:,0:2]
sio.savemat("results/"+query_image_name+"/points2D_for_softposit.mat", { 'value' : points2D_for_softposit })

closest_image_filename_cursor = db.execute("SELECT name FROM images WHERE image_id = "+ "'" + query_image_id + "'")
closest_image_filename = closest_image_filename_cursor.fetchone()[0]
closest_image_id_cursor = db.execute("SELECT camera_id FROM images WHERE name = " + "'" + closest_image_filename + "'")

closest_camera_id = closest_image_id_cursor.fetchone()[0]
closest_camera_parameters = db.execute("SELECT params FROM cameras WHERE camera_id = " + "'" + str(closest_camera_id) + "'" )
closest_camera_parameters = blob_to_array(closest_camera_parameters.fetchone()[0], np.float64)
closest_camera_parameters = np.array(closest_camera_parameters)

sio.savemat("results/"+query_image_name+"/camera_intrinsics.mat", { 'value' : closest_camera_parameters })

images_text_file = data_dir+"/sparse_model/images.txt"
f = open(images_text_file, 'r')
lines = f.readlines()
lines = lines[4:] #skip comments
f.close()

closest_image_id = 10 # this will have to be automatically acquired from an image retrieval system!! TODO: WRONG!!!
for i in range(0,len(lines),2):
    if (lines[i].split(" ")[0] == str(closest_image_id)):
        image_first_line = lines[i] # IMAGE_ID, QW, QX, QY, QZ, TX, TY, TZ, CAMERA_ID, NAME
        points2D_x_y_3Did = lines[i+1] # POINTS2D[] as (X, Y, POINT3D_ID)
        break

image_first_line = image_first_line.split(' ')
points2D_x_y_3Did = points2D_x_y_3Did[:-1].split(" ") #get rid of the new line

qw = image_first_line[1]
qx = image_first_line[2]
qy = image_first_line[3]
qz = image_first_line[4]

tx = image_first_line[5]
ty = image_first_line[6]
tz = image_first_line[7]

quarternion = np.array([qw, qx, qy, qz])
sio.savemat("results/"+query_image_name+"/colmap_rot.mat", { 'value' : quarternion })
trans = np.array([tx, ty, tz])
sio.savemat("results/"+query_image_name+"/colmap_trans.mat", { 'value' : trans })

# the code below is for RANSAC applications - it will return the correspondences 2D - 3D points
query_keypoints_descriptors = query_keypoints_xy_descriptors[:,2:130]

#3D data and stuff from closest dataset image
keypoints_xy_descriptors_3DpointId = np.loadtxt(open("results/"+query_image_name+"/keypoints_xy_descriptors_3DpointId.txt", 'rb'))

points3Dids = keypoints_xy_descriptors_3DpointId[:,130]
# use the ones that only have a 3D point
# points3Dids_indices = np.where(points3Dids != -1)
# keypoints_xy_descriptors_3DpointId = keypoints_xy_descriptors_3DpointId[points3Dids_indices,:][0] #the array is inside another array for some reason...
keypoints_descriptors = keypoints_xy_descriptors_3DpointId[:,2:130]

keypoints_descriptors = keypoints_descriptors.astype(np.float32)

# at this point you have the descriptors of the query image in a N by 128 array
# and the descriptors of the closest image that its 2D features (points) have a 3D point which is a M by 128 array
# now we need to find which ones are good matches...

bf = cv2.BFMatcher()
matches = bf.knnMatch(query_keypoints_descriptors, keypoints_descriptors, k=2)

good = []
for m,n in matches:
    if m.distance < 0.75 * n.distance:
        good.append([m])

points3D = np.loadtxt(open("results/"+query_image_name+"/points3D.txt", 'rb')) #list of [id, x, y, z]
query_image_final_points = np.empty((0, 2))
final_points3D = np.empty((0, 2))
final_match_array = np.empty((0, 5))

for good_match in good:
    queryIndex = good_match[0].queryIdx
    trainIndex = good_match[0].trainIdx
    # distance = good_match[0].distance
    # print "query desc index: " + str(queryIndex) + " train index: " + str(trainIndex) + " distance: " + str(distance) + "3D point id: " + str(points3Dids[trainIndex])
    if(points3Dids[trainIndex] != -1):
        # print "2D - 3D match: " + str(query_image_keypoints_data_xy[queryIndex,:]) + " <-> " + str(points3Dids[trainIndex])
        query_image_final_points = np.append(query_image_final_points, query_image_keypoints_data_xy[queryIndex,:])
        matches3Did = points3Dids[trainIndex]
        for point3D in points3D:
            if(point3D[0] == matches3Did):
                final_points3D = np.append(final_points3D, [ point3D[1], point3D[2], point3D[3] ])

query_image_final_points = np.reshape(query_image_final_points,[np.shape(query_image_final_points)[0]/2,2])
final_points3D = np.reshape(final_points3D,[np.shape(final_points3D)[0]/3,3])
final_match_array = np.concatenate((query_image_final_points, final_points3D), axis=1)

np.savetxt("results/"+query_image_name+"/final_match_array.txt", final_match_array)
sio.savemat("results/"+query_image_name+"/final_match_array.mat", { 'value' : final_match_array })

focalLength = closest_camera_parameters[0]
cx = closest_camera_parameters[1]
cy = closest_camera_parameters[2]
center = (cx, cy)
camera_matrix = np.array([  [focalLength,      0,       center[0]],
                            [0,            focalLength, center[1]],
                            [0,                 0,           1  ]], dtype = "float")

(_, pnp_ransac_rotation_vector, pnp_ransac_translation_vector, inliers) = cv2.solvePnPRansac(final_points3D, query_image_final_points, camera_matrix, None, flags = cv2.SOLVEPNP_EPNP)

sio.savemat("results/"+query_image_name+"/pnp_ransac_rotation_vector.mat", { 'value' : pnp_ransac_rotation_vector })
sio.savemat("results/"+query_image_name+"/pnp_ransac_translation_vector.mat", { 'value' : pnp_ransac_translation_vector })
