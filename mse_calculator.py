import glob
import os
import pdb

path = "data/coop3/model_images/*.JPG"
for fname in glob.glob(path):
    fname = fname.split("/")[3]
    os.system("python2.7 get_pose.py 0 0 "+fname+" data/coop3 0")
