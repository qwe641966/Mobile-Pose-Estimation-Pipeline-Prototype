import os
import sys
import pdb

# You might need to run this in the query images folder:
# sips -r -90 *.JPG && sips -r 90 *.JPG or sips -r 270 *.JPG

build_retrieval_database = sys.argv[1]
create_correspondences = sys.argv[2]
query_image_arg = sys.argv[3] # i.e IMG_7932.JPG
data_dir = sys.argv[4] # i.e data/coop3
benchmarking  = sys.argv[5] # use this if you are test an images already in the dataset
intrinsics_matrix_path = sys.argv[6]
run_direct_matching_3D_points_feature_builder = sys.argv[7]

# run_soft_posit = sys.argv[5]

query_image_arg_no_ext = query_image_arg.split(".")[0]

os.system("mkdir results/")
os.system("mkdir results/"+query_image_arg_no_ext)

if(build_retrieval_database == '1'):
    print "Creating retrieval database"
    print "python2.7 image_retrieval_database_creation.py "+data_dir+"/model_images"
    os.system("rm -rf "+data_dir+"/model_images_vocab_out")
    os.system("python2.7 image_retrieval_database_creation.py "+data_dir+"/model_images")

if(create_correspondences == '1'):
    print "Creating correspondences"
    print "python2.7 correspondences_builder.py "+data_dir+"/model_images_database "+data_dir+"/points_correspondences"
    os.system("python2.7 correspondences_builder.py "+data_dir+"/model_images_database "+data_dir+"/points_correspondences")

if(run_direct_matching_3D_points_feature_builder == '1'):
    print "Creating Direct Matching 3D features matches"
    print "python2.7 direct_matching_3D_points_feature_builder.py "+data_dir+"/model_images_database"
    os.system("python2.7 direct_matching_3D_points_feature_builder.py "+data_dir+"/model_images_database")

print "Running script 1/4"
print "python2.7 image_retrieval_query_image.py "+data_dir+"/query_images/"+query_image_arg
os.system("python2.7 image_retrieval_query_image.py "+data_dir+"/query_images/"+query_image_arg)

print "Running script 2/4"
print "python2.7 query_image_feature_extraction.py "+data_dir+" "+query_image_arg
os.system("python2.7 query_image_feature_extraction.py "+data_dir+" "+query_image_arg)

print "Running script 3/4"
print "python2.7 query_matcher_improved_ransac.py "+data_dir+" "+query_image_arg+" "+benchmarking + " " + intrinsics_matrix_path
os.system("python2.7 query_matcher_improved_ransac.py "+data_dir+" "+query_image_arg+" "+benchmarking + " " + intrinsics_matrix_path)
# if(run_soft_posit == '1'):
#     print 'Running softposit script'
#     run matlab script here
print "Running script 4/4"
print "python2.7 visualizer.py "+data_dir+"/query_images/"+query_image_arg + " " + intrinsics_matrix_path
os.system("python2.7 visualizer.py "+data_dir+"/query_images/"+query_image_arg + " " + intrinsics_matrix_path)
