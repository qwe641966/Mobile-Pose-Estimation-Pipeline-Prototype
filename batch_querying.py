import glob
import os
import pdb
import numpy as np
import sqlite3
import sys
import scipy.io as sio

data_dir = sys.argv[1]
intrinsics_matrix = sys.argv[2]

query_images_dir = data_dir+"/query_images/*.JPG"
# For the benchmarking to work you have to move the model images in the query folder!
benchmarking = '1'

for fname in glob.glob(query_images_dir): # change accordingly
    fname = fname.split('/')[3]
    print fname
    os.system("python2.7 get_pose.py 0 0 "+fname+" "+ data_dir +" "+benchmarking+" " +intrinsics_matrix+ " 0")