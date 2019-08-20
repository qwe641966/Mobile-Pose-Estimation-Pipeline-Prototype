import sqlite3
import numpy as np
import pdb
import sys
import cv2
import scipy.io as sio
import os
import math
import pdb

# This script should return a text file for each image in the SFM data
# that each text file's row is [SIFT desc, 2D xy, 3D xyz].
# That is each 2D point and its 3D point corresponding along with the SIFT of that
# 2D point

database_dir = sys.argv[1]

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

points3D = np.empty((0, 4))
points3D_text_file = database_dir+"/../sparse_model/points3D.txt"
f = open(points3D_text_file, 'r')
lines = f.readlines()
lines = lines[3:] #skip comments
f.close()

for i in range(len(lines)):
    line = lines[i].split(" ")
    point3Did = line[0]
    point3Did_x = line[1]
    point3Did_y = line[2]
    point3Did_z = line[3]
    points3D = np.append(points3D, [point3Did, point3Did_x, point3Did_y, point3Did_z ])

points3D = np.reshape(points3D, [np.shape(points3D)[0]/4,4])
points3D = points3D.astype(float)

db = COLMAPDatabase.connect(database_dir+"/database.db")

images_names = db.execute("SELECT name FROM images")
images_names = images_names.fetchall()

for images_name in images_names:
    image_id = db.execute("SELECT image_id FROM images WHERE name = "+"'"+str(images_name[0])+"'")
    image_id = str(image_id.fetchone()[0])
    images_name = str(images_name[0]).split(".")[0]

    print "Getting correspondences for image " + images_name

    image_keypoints_data = db.execute("SELECT data FROM keypoints WHERE image_id = "+ "'" + image_id + "'")
    image_keypoints_data = image_keypoints_data.fetchone()[0]
    image_keypoints_data_cols = db.execute("SELECT cols FROM keypoints WHERE image_id = "+ "'" + image_id + "'")
    image_keypoints_data_cols = int(image_keypoints_data_cols.fetchone()[0])
    image_keypoints_data = blob_to_array(image_keypoints_data, np.float32)
    image_keypoints_data_rows = np.shape(image_keypoints_data)[0]/image_keypoints_data_cols
    image_keypoints_data = image_keypoints_data.reshape(image_keypoints_data_rows, image_keypoints_data_cols)
    image_keypoints_data_xy = image_keypoints_data[:,0:2]

    image_descriptors_data = db.execute("SELECT data FROM descriptors WHERE image_id = "+ "'" + image_id + "'")
    image_descriptors_data = image_descriptors_data.fetchone()[0]
    image_descriptors_data = blob_to_array(image_descriptors_data, np.uint8)
    descs_rows = np.shape(image_descriptors_data)[0]/128
    image_descriptors_data = image_descriptors_data.reshape([descs_rows,128])

    keypoints_xy_descriptors = np.concatenate((image_keypoints_data_xy, image_descriptors_data), axis=1)

    images_text_file = database_dir+"/../sparse_model/images.txt"
    f = open(images_text_file, 'r')
    lines = f.readlines()
    lines = lines[4:] #skip comments
    f.close()

    for i in range(0,len(lines),2):
        if (lines[i].split(" ")[0] == str(image_id)):
            # print lines[i] # IMAGE_ID, QW, QX, QY, QZ, TX, TY, TZ, CAMERA_ID, NAME
            points2D_x_y_3Did = lines[i+1] # POINTS2D[] as (X, Y, POINT3D_ID)
            break

    points2D_x_y_3Did = points2D_x_y_3Did[:-1].split(" ")
    points3Dids = np.empty((0, 1))

    points2D_x_y_3Did = np.reshape(points2D_x_y_3Did,[np.shape(points2D_x_y_3Did)[0]/3,3])
    points3Dids = points2D_x_y_3Did[:,2].astype(np.float32)
    points3Dids_rows = np.shape(points3Dids)[0]

    keypoints_xy_descriptors_3DpointId = np.concatenate((keypoints_xy_descriptors, np.reshape(points3Dids,[points3Dids_rows,1])), axis = 1)

    # get rid of keypoints that have no 3D point
    keypoints_xy_descriptors_3DpointId = keypoints_xy_descriptors_3DpointId[np.where(keypoints_xy_descriptors_3DpointId[:,130] !=-1)[0]]
    keypoints_xy_descriptors_3DpointId = keypoints_xy_descriptors_3DpointId.astype(float)
    # each row: the 2D point and its SIFT descriptor and its 3D point id
    # each 2D point has one 3D point or none (-1)
    # os.system("mkdir "+database_dir+"/../points_correspondences/"+images_name)

    keypoints_points3Dids = keypoints_xy_descriptors_3DpointId[:,130]

    all_matching_points3D = np.empty((0, 3))

    for i in range(len(keypoints_points3Dids)):
        point3Did = np.where(points3D[:,0] == keypoints_points3Dids[i])[0][0]
        point3Dxyz = points3D[point3Did][1:4]
        all_matching_points3D = np.append(all_matching_points3D, [point3Dxyz])

    all_matching_points3D = np.reshape(all_matching_points3D, [np.shape(all_matching_points3D)[0]/3,3])
    keypoints_xy_descriptors_3DpointId_xyz = np.concatenate((keypoints_xy_descriptors_3DpointId, all_matching_points3D), axis=1)

    pdb.set_trace()

    correspondences = np.concatenate((keypoints_xy_descriptors_3DpointId_xyz[:,0:2], keypoints_xy_descriptors_3DpointId_xyz[:,131:134]), axis=1)
    correspondences = np.concatenate((keypoints_xy_descriptors_3DpointId_xyz[:,2:130], correspondences), axis=1)

    # np.savetxt(database_dir+"/../direct_matching_data/"+images_name+"/correspondences.txt", correspondences)