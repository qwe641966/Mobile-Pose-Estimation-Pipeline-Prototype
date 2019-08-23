import glob
import os
import pdb
import numpy as np

# use this path to get the mses again
path = "results/*.png"

mse_errors = np.empty((0,1))

for fname in glob.glob(path):
    fname = fname.split("_result")[0].split("/")[1]
    mse = np.loadtxt("results/"+fname+"/mse_error.txt")
    print fname + " " + str(mse)
    mse_errors = np.concatenate((mse_errors, mse.reshape([1,1])),axis=0)
    np.savetxt("results/mse_errors.txt", mse_errors)

    # run only this line to get the mses again
    # os.system("python2.7 get_pose.py 0 0 "+fname+" data/coop3 0")
