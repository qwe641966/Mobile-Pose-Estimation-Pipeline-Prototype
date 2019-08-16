import glob
import os

path = "data/coop3/query_images/*.JPG"
for fname in glob.glob(path):
    os.system("python2.7 get_pose.py 0  0 "+fname.split('/')[3]+" data/coop3 0")
