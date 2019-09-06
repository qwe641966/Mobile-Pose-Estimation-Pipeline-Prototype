import glob
import os
import pdb
import numpy as np
import sqlite3
import sys
import scipy.io as sio

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

mse_data = np.empty((0, 13))

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

        quarternion = np.array([qw, qx, qy, qz])

        ground_truth_rotation_quarternion = quarternion
        ground_truth_trans = np.array([tx, ty, tz]).astype(np.float64)

        translation_vector_calculated = np.loadtxt("results/"+fname+"/pnp_ransac_translation_vector_image_retrieval.txt")
        rotation_vector_calculated = np.loadtxt("results/"+fname+"/pnp_ransac_rotation_vector_image_retrieval.txt")

        row = np.concatenate((ground_truth_rotation_quarternion, ground_truth_trans, rotation_vector_calculated, translation_vector_calculated), axis=0)
        row = row.reshape([1,13])
        mse_data = np.concatenate((mse_data, row), axis=0)
        index = index + 1

mse_data = mse_data.astype(np.float64)
sio.savemat('mse_data.mat', {'value':mse_data})