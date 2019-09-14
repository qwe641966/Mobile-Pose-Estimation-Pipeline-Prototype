import sqlite3
import numpy as np
import pdb
import sys
import cv2
import scipy.io as sio
import os
import math
from direct_matcher import direct_matching
from image_retrieval_matcher import image_retrieval_matching

# This file will return the camera intrinsics of the query image and also the
# initial rotation and translation from the similar image to the query image in the database.
#
# when RANSAC is used then it will apply SIFT matching between the sift features of the
# query image and the similar image. Then the final array will be a correspondences array
# between the 2D points of the query image and 3D points (that were fetched from the similar image - that already had
# the 3D points data from COLMAP)

data_dir = sys.argv[1]
query_image_name_with_ext = sys.argv[2]
benchmarking = sys.argv[3]
intrinsics_matrix_path = sys.argv[4]
query_image_name = query_image_name_with_ext.split(".")[0]
query_image_path = data_dir+"/query_images/"+query_image_name_with_ext

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

if benchmarking == "1":
    db = COLMAPDatabase.connect(model_images_database)
else:
    db = COLMAPDatabase.connect(query_image_database)


# Note: the sift features should be extracted from COLMAP so they match the ones from the SFM dataset
# Another note: same query name just using different databases for the ids
query_image_id_data = db.execute("SELECT image_id FROM images WHERE name = "+ "'" + query_image_name_with_ext + "'")
query_image_id = str(query_image_id_data.fetchone()[0])

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

images_result_text_file = "results/"+query_image_name+"/image_retrieval_results_for_"+query_image_name+".txt"

f = open(images_result_text_file, 'r')
similar_images_names = f.readlines()
print similar_images_names
f.close()

if benchmarking == "1":
    if(query_image_name+"\n" in similar_images_names):
        print "Test image name will be removed from results"
        similar_images_names.remove(query_image_name+"\n")

    all_images_text_file = data_dir+"/sparse_model/images.txt"
    f = open(all_images_text_file, 'r')
    lines = f.readlines()
    lines = lines[4:] #skip comments
    f.close()

    model_image_id_data = db.execute("SELECT image_id FROM images WHERE name = "+ "'" + query_image_name_with_ext + "'")
    model_image_id = str(model_image_id_data.fetchone()[0])

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

final_match_array_image_retrieval, image_retrieval_good_matches_no = image_retrieval_matching(query_keypoints_xy_descriptors, data_dir, similar_images_names)
final_match_array_direct, direct_good_matches_no = direct_matching(data_dir,query_keypoints_xy_descriptors)

intrinsics_matrix = np.loadtxt(intrinsics_matrix_path)

np.savetxt("results/"+query_image_name+"/final_match_array_image_retrieval_matching.txt", final_match_array_image_retrieval)
np.savetxt("results/"+query_image_name+"/3D_points_only_image_retrieval_matching.txt", np.around(final_match_array_image_retrieval[:,2:5],  decimals=4),  fmt='%f')

np.savetxt("results/"+query_image_name+"/final_match_array_direct.txt", final_match_array_direct)
np.savetxt("results/"+query_image_name+"/3D_points_direct.txt", np.around(final_match_array_direct[:,2:5],  decimals=4),  fmt='%f')

np.savetxt("results/"+query_image_name+"/intrinsics_matrix.txt", intrinsics_matrix)

# TODO: get ratio of ransanc correspondences/inliers?
(_, pnp_ransac_rotation_vector_image_retrieval, pnp_ransac_translation_vector_image_retrieval, inliers_image_retrieval) = cv2.solvePnPRansac(final_match_array_image_retrieval[:,2:5], final_match_array_image_retrieval[:,0:2], intrinsics_matrix, None, iterationsCount = 500, confidence = 0.99, flags = cv2.SOLVEPNP_EPNP)
(_, pnp_ransac_rotation_vector_direct, pnp_ransac_translation_vector_direct, inliers_direct) = cv2.solvePnPRansac(final_match_array_direct[:,2:5], final_match_array_direct[:,0:2], intrinsics_matrix, None, iterationsCount = 500, confidence = 0.99, flags = cv2.SOLVEPNP_EPNP)

if inliers_image_retrieval is None:
    print "NO inliers from image retrieval!"
else:
    print "RANSAC inliers inliers_image_retrieval " + str(np.shape(inliers_image_retrieval)[0])
    percentage = np.shape(inliers_image_retrieval)[0] * 100 / image_retrieval_good_matches_no
    print "RANSAC inliers to matches inliers_image_retrieval ratio " + str(np.shape(inliers_image_retrieval)[0]) + "/" + str(image_retrieval_good_matches_no) + ", " + str(percentage) + "%"
    np.savetxt("results/"+query_image_name+"/ransanc_image_retrieval_percentage_ratio.txt", np.array([percentage]), fmt='%f')

if inliers_direct is None:
    print "NO inliers from direct matching!"
else:
    print "RANSAC inliers direct " + str(np.shape(inliers_direct)[0])
    percentage = np.shape(inliers_direct)[0] * 100 / direct_good_matches_no
    print "RANSAC inliers to matches direct ratio " + str(np.shape(inliers_direct)[0]) + "/" + str(direct_good_matches_no) + ", " + str(percentage) + "%"
    np.savetxt("results/"+query_image_name+"/ransanc_direct_percentage_ratio.txt", np.array([percentage]), fmt='%f')

np.savetxt("results/"+query_image_name+"/pnp_ransac_rotation_vector_image_retrieval.txt", pnp_ransac_rotation_vector_image_retrieval)
np.savetxt("results/"+query_image_name+"/pnp_ransac_translation_vector_image_retrieval.txt", pnp_ransac_translation_vector_image_retrieval)

np.savetxt("results/"+query_image_name+"/pnp_ransac_rotation_vector_direct.txt", pnp_ransac_rotation_vector_direct)
np.savetxt("results/"+query_image_name+"/pnp_ransac_translation_vector_direct.txt", pnp_ransac_translation_vector_direct)

# Results!
print("Parsing Results")

# Direct Matching
points_correspondences_direct_matching = np.loadtxt("results/"+query_image_name+"/final_match_array_direct.txt")
points3D_direct_matching = points_correspondences_direct_matching[:,2:5]
pnp_ransac_rot_direct_matching = np.loadtxt("results/"+query_image_name+"/pnp_ransac_rotation_vector_direct.txt")
pnp_ransac_trans_direct_matching = np.loadtxt("results/"+query_image_name+"/pnp_ransac_translation_vector_direct.txt")
pnp_ransac_rot_direct_matching = cv2.Rodrigues(pnp_ransac_rot_direct_matching)[0]

no_points3D_direct_matching = np.shape(points3D_direct_matching)[0]
ones = np.ones(no_points3D_direct_matching)
ones = ones.reshape(no_points3D_direct_matching,1)
points3D_direct_matching = np.concatenate((points3D_direct_matching, ones), axis=1) #make homogeneous
points3D_direct_matching = np.transpose(points3D_direct_matching)

rt_direct_matching = np.concatenate((pnp_ransac_rot_direct_matching, pnp_ransac_trans_direct_matching.reshape([3,1])),axis=1)
bottom_row = np.array([0,0,0,1]).reshape([1,4])
rt_direct_matching = np.concatenate((rt_direct_matching, bottom_row), axis=0) #make homogeneous
np.savetxt("results/"+query_image_name+"/RT_direct_matching.txt", np.around(rt_direct_matching, decimals=4), fmt='%f')

rt_points3D_direct_matching = np.dot(rt_direct_matching, points3D_direct_matching)
rt_points3D_direct_matching = rt_points3D_direct_matching[0:3,:] #un-make homogeneous

points2D_projected_direct_matching = np.dot(intrinsics_matrix, rt_points3D_direct_matching)
points2D_projected_direct_matching = np.transpose(points2D_projected_direct_matching)
points2D_projected_direct_matching = points2D_projected_direct_matching / points2D_projected_direct_matching[:,2].reshape(no_points3D_direct_matching,1)
points2D_projected_direct_matching = np.round(points2D_projected_direct_matching)
points2D_projected_direct_matching = points2D_projected_direct_matching[:,0:2]

rows = np.shape(points2D_projected_direct_matching)[0]
img = cv2.imread(query_image_path)

np.savetxt("results/"+query_image_name+"/points2D_projected_direct_matching.txt", points2D_projected_direct_matching)

# Image Retrieval
points_correspondences_image_retrieval = np.loadtxt("results/"+query_image_name+"/final_match_array_image_retrieval_matching.txt")
points3D_image_retrieval = points_correspondences_image_retrieval[:,2:5]
pnp_ransac_rot_image_retrieval = np.loadtxt("results/"+query_image_name+"/pnp_ransac_rotation_vector_image_retrieval.txt")
pnp_ransac_trans_image_retrieval = np.loadtxt("results/"+query_image_name+"/pnp_ransac_translation_vector_image_retrieval.txt")
pnp_ransac_rot_image_retrieval = cv2.Rodrigues(pnp_ransac_rot_image_retrieval)[0]

no_points3D_image_retrieval = np.shape(points3D_image_retrieval)[0]
ones = np.ones(no_points3D_image_retrieval)
ones = ones.reshape(no_points3D_image_retrieval,1)
points3D_image_retrieval = np.concatenate((points3D_image_retrieval, ones), axis=1) #make homogeneous
points3D_image_retrieval = np.transpose(points3D_image_retrieval)

rt_image_retrieval = np.concatenate((pnp_ransac_rot_image_retrieval, pnp_ransac_trans_image_retrieval.reshape([3,1])),axis=1)
bottom_row = np.array([0,0,0,1]).reshape([1,4])
rt_image_retrieval = np.concatenate((rt_image_retrieval, bottom_row), axis=0) #make homogeneous
np.savetxt("results/"+query_image_name+"/RT_image_retrieval", np.around(rt_image_retrieval, decimals=4), fmt='%f')

rt_points3D_image_retrieval = np.dot(rt_image_retrieval, points3D_image_retrieval)
rt_points3D_image_retrieval = rt_points3D_image_retrieval[0:3,:] #un-make homogeneous

points2D_projected_image_retrieval = np.dot(intrinsics_matrix, rt_points3D_image_retrieval)
points2D_projected_image_retrieval = np.transpose(points2D_projected_image_retrieval)
points2D_projected_image_retrieval = points2D_projected_image_retrieval / points2D_projected_image_retrieval[:,2].reshape(no_points3D_image_retrieval,1)
points2D_projected_image_retrieval = np.round(points2D_projected_image_retrieval)
points2D_projected_image_retrieval = points2D_projected_image_retrieval[:,0:2]

np.savetxt("results/"+query_image_name+"/points2D_projected_image_retrieval.txt", points2D_projected_image_retrieval)

