import glob
import os
import pdb
import numpy as np
import sqlite3
import sys
import scipy.io as sio

data_dir = sys.argv[1]
query_images_dir = data_dir+"/query_images/*"
model_images_dir = data_dir+"/model_images/*.JPG"
# For the benchmarking to work you have to move the model images in teh query folder!
benchmarking = '1'

for fname in glob.glob(model_images_dir): # change accordingly
    fname = fname.split('/')[3]
    os.system("python2.7 get_pose.py 0 0 "+fname+" data/coop6 "+benchmarking+" intrinsics_matrices/iphone_intrinsics.txt 0")