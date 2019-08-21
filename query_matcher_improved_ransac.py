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

data_dir = sys.argv[1]
query_image_name_with_ext = sys.argv[2]
query_image_name = query_image_name_with_ext.split(".")[0]

query_image_database = data_dir +"/query_images_databases/database_for_"+query_image_name+".db"
model_images_database = data_dir +"/model_images_database/database.db"

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

def get_good_matches(matches):
    good = []
    for m,n in matches:
        if m.distance < 0.7 * n.distance: # or 0.75
            good.append([m])
    return good

db_query = COLMAPDatabase.connect(query_image_database)
db_model = COLMAPDatabase.connect(model_images_database)

# Note: the sift features should be extracted from COLMAP so they match the ones from the SFM dataset
# Another note: same query name just using different databases for the ids
query_image_id_data = db_query.execute("SELECT image_id FROM images WHERE name = "+ "'" + query_image_name_with_ext + "'")
query_image_id = str(query_image_id_data.fetchone()[0])
model_image_id_data = db_model.execute("SELECT image_id FROM images WHERE name = "+ "'" + query_image_name_with_ext + "'")
model_image_id = str(model_image_id_data.fetchone()[0])

query_image_keypoints_data = db_query.execute("SELECT data FROM keypoints WHERE image_id = "+ "'" + query_image_id + "'")
query_image_keypoints_data = query_image_keypoints_data.fetchone()[0]
query_image_keypoints_data_cols = db_query.execute("SELECT cols FROM keypoints WHERE image_id = "+ "'" + query_image_id + "'")
query_image_keypoints_data_cols = int(query_image_keypoints_data_cols.fetchone()[0])
query_image_keypoints_data = blob_to_array(query_image_keypoints_data, np.float32)
query_image_keypoints_data_rows = np.shape(query_image_keypoints_data)[0]/query_image_keypoints_data_cols
query_image_keypoints_data = query_image_keypoints_data.reshape(query_image_keypoints_data_rows, query_image_keypoints_data_cols)
query_image_keypoints_data_xy = query_image_keypoints_data[:,0:2]

query_image_descriptors_data = db_query.execute("SELECT data FROM descriptors WHERE image_id = "+ "'" + query_image_id + "'")
query_image_descriptors_data = query_image_descriptors_data.fetchone()[0]
query_image_descriptors_data = blob_to_array(query_image_descriptors_data, np.uint8)
descs_rows = np.shape(query_image_descriptors_data)[0]/128
query_image_descriptors_data = query_image_descriptors_data.reshape([descs_rows,128])

query_keypoints_xy_descriptors = np.concatenate((query_image_keypoints_data_xy, query_image_descriptors_data), axis=1)

images_result_text_file = "results/"+query_image_name+"/image_retrieval_results_for_"+query_image_name+".txt"

f = open(images_result_text_file, 'r')
similar_images_names = f.readlines()
print similar_images_names
f.close()

if(query_image_name+"\n" in similar_images_names):
    print "Test image name will be removed from results"
    similar_images_names.remove(query_image_name+"\n")

pdb.set_trace()

all_images_text_file = data_dir+"/sparse_model/images.txt"
f = open(all_images_text_file, 'r')
lines = f.readlines()
lines = lines[4:] #skip comments
f.close()

for i in range(0,len(lines),2):
    if (lines[i].split(" ")[0] == str(model_image_id)):
        image_first_line = lines[i] # IMAGE_ID, QW, QX, QY, QZ, TX, TY, TZ, CAMERA_ID, NAME
        points2D_x_y_3Did = lines[i+1] # POINTS2D[] as (X, Y, POINT3D_ID)
        break

image_first_line = image_first_line.split(' ')
qw = image_first_line[1]
qx = image_first_line[2]
qy = image_first_line[3]
qz = image_first_line[4]

tx = image_first_line[5]
ty = image_first_line[6]
tz = image_first_line[7]

quarternion = np.array([qw, qx, qy, qz])
quarternion = quarternion[1:4].astype(np.float64)
ground_truth_rotation = cv2.Rodrigues(quarternion)[0]
ground_truth_trans = np.array([tx, ty, tz]).astype(np.float64)
ground_truth_P = np.concatenate((ground_truth_rotation, ground_truth_trans.reshape([3,1])), axis =1)

print "loading correspondences.."
correspondences = np.empty((0, 133))
for similar_image in similar_images_names:
    similar_image_text_file = data_dir+"/points_correspondences/"+similar_image.split("\n")[0]+"/correspondences.txt"
    array = np.loadtxt(similar_image_text_file)
    correspondences = np.concatenate((correspondences, array), axis = 0)

print "matching.."
query_descriptors = query_keypoints_xy_descriptors[:,2:130]
train_descriptors = correspondences[:,0:128]
train_descriptors = train_descriptors.astype(np.float32) # minor formatting fix

# Brute Force
bf = cv2.BFMatcher()
matches = bf.knnMatch(query_descriptors, train_descriptors, k=2)
#
# # ..or FLANN
# FLANN_INDEX_KDTREE = 0
# index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
# search_params = dict(checks=50)   # or pass empty dictionary
# flann = cv2.FlannBasedMatcher(index_params,search_params)
#
# train_descriptors = train_descriptors.astype(np.float32) # minor formatting fix
# query_descriptors = np.ascontiguousarray(query_descriptors)
# train_descriptors = np.ascontiguousarray(train_descriptors)
#
# matches = flann.knnMatch(query_descriptors, train_descriptors, k=2)

good = get_good_matches(matches)

print "found this many good matches: " + str(np.shape(good))

final_match_array = np.empty((0, 5))
for good_match in good:
    queryIndex = good_match[0].queryIdx
    trainIndex = good_match[0].trainIdx
    final_match_array_row = np.concatenate((query_keypoints_xy_descriptors[queryIndex,0:2], correspondences[trainIndex,130:133]) , axis = 0)
    final_match_array = np.concatenate((final_match_array, final_match_array_row.reshape([1,5])), axis = 0)

# for IMG_7932.JPG
intrinsics_matrix = np.array([ [3492,    0,    2003],
                               [0,      3482,  1523],
                               [0,        0,     1  ]], dtype = "float")

# for google_ar1.JPG
# intrinsics_matrix = np.array([ [507.69,    0,    320.08],
#                                [0,      507.62,  238.19],
#                                [0,         0,       1  ]], dtype = "float")

# for google_arcore0.JPG
# intrinsics_matrix = np.array([ [1015,    0,    640.66],
#                                [0,      1015,  356.89],
#                                [0,        0,     1  ]], dtype = "float")

np.savetxt("results/"+query_image_name+"/final_match_array.txt",final_match_array)
np.savetxt("results/"+query_image_name+"/intrinsics_matrix.txt",intrinsics_matrix)

(_, pnp_ransac_rotation_vector, pnp_ransac_translation_vector, inliers) = cv2.solvePnPRansac(final_match_array[:,2:5], final_match_array[:,0:2], intrinsics_matrix, None, iterationsCount = 500, confidence = 0.99, flags = cv2.SOLVEPNP_EPNP)

pnp_ransac_rotation_matrix = cv2.Rodrigues(pnp_ransac_rotation_vector)[0]
calculated_P = np.concatenate((pnp_ransac_rotation_matrix, pnp_ransac_translation_vector), axis =1)

np.savetxt("results/"+query_image_name+"/pnp_ransac_rotation_vector.txt", pnp_ransac_rotation_vector)
np.savetxt("results/"+query_image_name+"/pnp_ransac_translation_vector.txt", pnp_ransac_translation_vector)

#save mse error
mse = (np.square(ground_truth_P - calculated_P)).mean(axis = None)
np.savetxt("results/"+query_image_name+"/mse_error.txt", [mse])