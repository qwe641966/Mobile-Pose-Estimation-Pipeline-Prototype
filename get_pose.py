import os
import sys
import pdb

build_retrieval_database = sys.argv[1]
create_correspondences = sys.argv[2]
query_image_arg = sys.argv[3] # i.e IMG_7932.JPG
data_dir = sys.argv[4] # i.e data/coop3
run_soft_posit = sys.argv[5]

query_image_arg_no_ext = query_image_arg.split(".")[0]

os.system("mkdir results/")
os.system("mkdir results/"+query_image_arg_no_ext)

if(build_retrieval_database == '1'):
    print "Creating retrieval database"
    os.system("rm -rf "+data_dir+"/model_images_vocab_out")
    os.system("python2.7 image_retrieval_database_creation.py "+data_dir+"/model_images")

if(create_correspondences == '1'):
    print "Creating correspondences"
    os.system("python2.7 correspondences_builder.py "+data_dir+"/model_images_database "+data_dir+"/points_correspondences")

print "Running script 1/4"
os.system("time python2.7 image_retrieval_query_image.py "+data_dir+"/query_images/"+query_image_arg)
print "Running script 2/4"
os.system("time python2.7 query_image_feature_extraction.py "+data_dir+" "+query_image_arg)

print "Running script 3/4"
os.system("time python2.7 query_matcher_improved_ransac.py "+data_dir+" "+query_image_arg_no_ext)
if(run_soft_posit == '1'):
    print 'Running softposit script'
    # run matlab script here
print "Running script 4/4"
os.system("time python2.7 visualizer.py "+data_dir+"/query_images/"+query_image_arg)
