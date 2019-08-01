import sqlite3
import numpy as np
import pdb
import sys
import cv2
import scipy.io as sio
import os
import math
import pdb

database_dir = sys.argv[1]
image_retrieval_result_file = sys.argv[2]
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

db = COLMAPDatabase.connect(database_dir+"/database.db")

f = open("results/"+query_image_name+"/"+image_retrieval_result_file, 'r')
lines = f.readlines()
image_retrieval_result = lines[0].split("\n")[0] + ".JPG"

similar_image_id = db.execute("SELECT image_id FROM images WHERE name = "+ "'" + image_retrieval_result + "'")
similar_image_id = str(similar_image_id.fetchone()[0])

similar_image_keypoints_data = db.execute("SELECT data FROM keypoints WHERE image_id = "+ "'" + similar_image_id + "'")
similar_image_keypoints_data = similar_image_keypoints_data.fetchone()[0]
similar_image_keypoints_data_cols = db.execute("SELECT cols FROM keypoints WHERE image_id = "+ "'" + similar_image_id + "'")
similar_image_keypoints_data_cols = int(similar_image_keypoints_data_cols.fetchone()[0])
similar_image_keypoints_data = blob_to_array(similar_image_keypoints_data, np.float32)
similar_image_keypoints_data_rows = np.shape(similar_image_keypoints_data)[0]/similar_image_keypoints_data_cols
similar_image_keypoints_data = similar_image_keypoints_data.reshape(similar_image_keypoints_data_rows, similar_image_keypoints_data_cols)
similar_image_keypoints_data_xy = similar_image_keypoints_data[:,0:2]

similar_image_descriptors_data = db.execute("SELECT data FROM descriptors WHERE image_id = "+ "'" + similar_image_id + "'")
similar_image_descriptors_data = similar_image_descriptors_data.fetchone()[0]
similar_image_descriptors_data = blob_to_array(similar_image_descriptors_data, np.uint8)
descs_rows = np.shape(similar_image_descriptors_data)[0]/128
similar_image_descriptors_data = similar_image_descriptors_data.reshape([descs_rows,128])

keypoints_xy_descriptors = np.concatenate((similar_image_keypoints_data_xy, similar_image_descriptors_data), axis=1)

images_text_file = database_dir+"/../sparse_model/images.txt"
f = open(images_text_file, 'r')
lines = f.readlines()
lines = lines[4:] #skip comments
f.close()

for i in range(0,len(lines),2):
    if (lines[i].split(" ")[0] == str(similar_image_id)):
        # print lines[i] # IMAGE_ID, QW, QX, QY, QZ, TX, TY, TZ, CAMERA_ID, NAME
        points2D_x_y_3Did = lines[i+1] # POINTS2D[] as (X, Y, POINT3D_ID)
        break

points2D_x_y_3Did = points2D_x_y_3Did[:-1].split(" ")
points3Dids = np.empty((0, 1))

points2D_x_y_3Did = np.reshape(points2D_x_y_3Did,[np.shape(points2D_x_y_3Did)[0]/3,3])
points3Dids = points2D_x_y_3Did[:,2].astype(np.float32)
points3Dids_rows = np.shape(points3Dids)[0]
keypoints_xy_descriptors_3DpointId = np.concatenate((keypoints_xy_descriptors, np.reshape(points3Dids,[points3Dids_rows,1])), axis=1)

keypoints_xy_descriptors_3DpointId = keypoints_xy_descriptors_3DpointId.astype(float)
# each row: the 2D point and its SIFT descriptor and its 3D point id
# each 2D point has one 3D point or none (-1)
np.savetxt("results/"+query_image_name+"/keypoints_xy_descriptors_3DpointId.txt", keypoints_xy_descriptors_3DpointId)

# these are the 3Dpoints of the sparse model
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
np.savetxt("results/"+query_image_name+"/points3D.txt", points3D)

