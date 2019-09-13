import glob
import os
import pdb
import numpy as np
import sqlite3
import sys
import scipy.io as sio
import cv2
from scipy.spatial.transform import Rotation as R

# run extract_gt_data_from_database.py first!

# use this path to get the mses again
path = "results/*"
data_dir = sys.argv[1]
model_images_database = data_dir +"/model_images_database/database.db"

all_images_text_file = data_dir+"/sparse_model/images.txt"
f = open(all_images_text_file, 'r')
lines = f.readlines()
lines = lines[4:] #skip comments
f.close()

mse_data = np.empty((0, 24))

index = 1;
for fname in glob.glob(path):
    fname = fname.split('/')[1]

    if len(fname) == 8: # pick up only images!

        ground_truth_rotation_quarternion = np.loadtxt("results/"+fname+"/camera_gt_R_quarternion.txt")
        ground_truth_trans = np.loadtxt("results/"+fname+"/camera_gt_trans.txt")

        #direct
        rotation_vector_est_direct = np.loadtxt("results/"+fname+"/pnp_ransac_rotation_vector_direct.txt")
        translation_vector_est_direct = np.loadtxt("results/"+fname+"/pnp_ransac_translation_vector_direct.txt")

        #image retrieval
        rotation_vector_est_image_retrieval = np.loadtxt("results/"+fname+"/pnp_ransac_rotation_vector_image_retrieval.txt")
        translation_vector_image_retrieval = np.loadtxt("results/"+fname+"/pnp_ransac_translation_vector_image_retrieval.txt")

        # convert rotation vector to quarternion because of matlab
        rotation_matrix_est_direct = cv2.Rodrigues(rotation_vector_est_direct)[0] # [1] is a jacobian matrix
        scipy_rotation = R.from_dcm(rotation_matrix_est_direct)
        scipy_rotation_quat = scipy_rotation.as_quat()
        # matlab format
        est_rotation_quarternion_direct = np.array([ scipy_rotation_quat[3], scipy_rotation_quat[0], scipy_rotation_quat[1], scipy_rotation_quat[2]])

        # convert rotation vector to quarternion because of matlab
        rotation_matrix_est_image_retrieval = cv2.Rodrigues(rotation_vector_est_image_retrieval)[0] # [1] is a jacobian matrix
        scipy_rotation = R.from_dcm(rotation_matrix_est_image_retrieval)
        scipy_rotation_quat = scipy_rotation.as_quat()
        # matlab format
        est_rotation_quarternion_image_retrieval = np.array([ scipy_rotation_quat[3], scipy_rotation_quat[0], scipy_rotation_quat[1], scipy_rotation_quat[2]])

        # ransac percentages
        try:
            ransac_est_direct = np.loadtxt("results/"+fname+"/ransanc_direct_percentage_ratio.txt")
        except IOError, e:
            ransac_est_image_retrieval = np.array([0])

        ransac_est_direct = ransac_est_direct.reshape([1])

        try:
            ransac_est_image_retrieval = np.loadtxt("results/"+fname+"/ransanc_image_retrieval_percentage_ratio.txt")
        except IOError, e:
            ransac_est_image_retrieval = np.array([0])

        ransac_est_image_retrieval = ransac_est_image_retrieval.reshape([1])

        image_no_name = np.array([int(fname.split('_')[1])]).reshape([1])

        row = np.concatenate((ground_truth_rotation_quarternion, ground_truth_trans, est_rotation_quarternion_direct, translation_vector_est_direct, est_rotation_quarternion_image_retrieval, translation_vector_image_retrieval, ransac_est_direct, ransac_est_image_retrieval, image_no_name), axis=0)
        row = row.reshape([1,24])
        mse_data = np.concatenate((mse_data, row), axis=0)
        index = index + 1

mse_data = mse_data.astype(np.float64)
sio.savemat(data_dir+'/mse_data.mat', {'value' : mse_data})