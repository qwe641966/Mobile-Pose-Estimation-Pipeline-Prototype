import sqlite3
import numpy as np
import pdb
import sys
import cv2
import scipy.io as sio
import os
import math
import pdb

#  This will get just the [x,y,z] from the sparse_model folder/model

data_dir = sys.argv[1]

points3D = np.empty((0, 3))
points3D_text_file = data_dir+"/sparse_model/points3D.txt"
f = open(points3D_text_file, 'r')
lines = f.readlines()
lines = lines[3:] #skip comments
f.close()

print "Reading points3D.txt..."

for i in range(len(lines)):
    line = lines[i].split(" ")
    point3Did = line[0]
    point3Did_x = line[1]
    point3Did_y = line[2]
    point3Did_z = line[3]
    points3D = np.append(points3D, [point3Did_x, point3Did_y, point3Did_z ])

points3D = np.reshape(points3D, [np.shape(points3D)[0]/3,3])
points3D = points3D.astype(float)

np.savetxt(data_dir+"/model_points3D.txt", points3D)