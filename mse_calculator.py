import glob
import os
import pdb
import numpy as np
import sqlite3
import sys
import scipy.io as sio
import cv2
from scipy.spatial.transform import Rotation as R

# use this path to get the mses again
path = "results/*"
data_dir = sys.argv[1]
model_images_database = data_dir +"/model_images_database/database.db"

class COLMAPDatabase(sqlite3.Connection):

    @staticmethod
    def connect(database_path):
        return sqlite3.connect(database_path, factory=COLMAPDatabase)

db_model = COLMAPDatabase.connect(model_images_database)

all_images_text_file = data_dir+"/sparse_model/images.txt"
f = open(all_images_text_file, 'r')
lines = f.readlines()
lines = lines[4:] #skip comments
f.close()

mse_data = np.empty((0, 14))

index = 1;
for fname in glob.glob(path):
    fname = fname.split('/')[1]
    if len(fname) == 8:
        model_image_id_data = db_model.execute("SELECT image_id FROM images WHERE name = "+ "'" + fname + ".JPG'")
        model_image_id = str(model_image_id_data.fetchone()[0])

        print "Doing.. " + fname + " index " + str(index) + " db id " + str(model_image_id)

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

        ground_truth_rotation_quarternion = np.array([qw, qx, qy, qz]) #same as matlab
        ground_truth_trans = np.array([tx, ty, tz]).astype(np.float64)

        # switch between direct and image retrieval
        rotation_vector_est_direct = np.loadtxt("results/"+fname+"/pnp_ransac_rotation_vector_direct.txt")
        translation_vector_est_direct = np.loadtxt("results/"+fname+"/pnp_ransac_translation_vector_direct.txt")

        # convert rotation vector to quarternion because of matlab
        rotation_matrix_est_direct = cv2.Rodrigues(rotation_vector_est_direct)[0] # [1] is a jacobian matrix
        scipy_rotation = R.from_dcm(rotation_matrix_est_direct)
        scipy_rotation_quat = scipy_rotation.as_quat()
        # matlab format
        est_rotation_quarternion = np.array([ scipy_rotation_quat[3], scipy_rotation_quat[0], scipy_rotation_quat[1], scipy_rotation_quat[2]])

        row = np.concatenate((ground_truth_rotation_quarternion, ground_truth_trans, est_rotation_quarternion, translation_vector_est_direct), axis=0)
        row = row.reshape([1,14])
        mse_data = np.concatenate((mse_data, row), axis=0)
        index = index + 1

mse_data = mse_data.astype(np.float64)
sio.savemat('mse_data.mat', {'value' : mse_data})