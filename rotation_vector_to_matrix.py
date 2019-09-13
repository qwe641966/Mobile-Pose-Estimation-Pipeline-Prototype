import numpy as np
import pdb
import cv2
import sys
import scipy.io as sio
import os

query_image_name = sys.argv[1]

pnp_ransac_rot = np.loadtxt("results/"+query_image_name+"/pnp_ransac_rotation_vector_direct.txt")
pnp_ransac_rot = cv2.Rodrigues(pnp_ransac_rot)[0]

pdb.set_trace();