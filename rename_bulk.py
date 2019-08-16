import glob
import os
import pdb

path = "video_data/*_result.png"
for fname in glob.glob(path):
    print fname
    if len(fname.split('/')[1].split('_')[1]) == 1:
        name =  fname.split('/')[1].split('_')[0] + "0"+fname.split('/')[1].split('_')[1]
    else:
        name =  fname.split('/')[1].split('_')[0] + fname.split('/')[1].split('_')[1]

    os.system("cp " + fname + " " + fname.split('/')[0]+"/"+name+".png")