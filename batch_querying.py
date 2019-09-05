import glob
import os
import pdb
import numpy as np
import sqlite3
import sys
import scipy.io as sio

data_dir = sys.argv[1]
query_images_dir = data_dir+"/query_images/*"

for fname in glob.glob(query_images_dir):
    fname = fname.split('/')[3]
    os.system("python2.7 get_pose.py 0 0 "+fname+" data/coop6 0 intrinsics_matrices/iphone_intrinsics.txt 0")