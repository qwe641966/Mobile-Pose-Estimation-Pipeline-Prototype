import os
import sys
import pdb

# You might need to run this in the query images folder:
# sips -r -90 *.JPG && sips -r 90 *.JPG or sips -r 270 *.JPG

build_retrieval_database = sys.argv[1]
create_correspondences = sys.argv[2]
run_direct_matching_3D_points_feature_builder = sys.argv[3]
query_image_arg = sys.argv[4] # i.e IMG_7932.JPG
data_dir = sys.argv[5] # i.e data/coop3
intrinsics_matrix_path = sys.argv[6]
extract_3D_points_from_sparse = sys.argv[7]
benchmarking  = sys.argv[8] # use this if you are testing an images already in the dataset

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
    print "python2.7 direct_matching_3D_points_feature_builder.py "+data_dir
    os.system("python2.7 direct_matching_3D_points_feature_builder.py "+data_dir)

print "Running script 1/4"
print "python2.7 image_retrieval_query_image.py "+data_dir+"/query_images/"+query_image_arg
os.system("python2.7 image_retrieval_query_image.py "+data_dir+"/query_images/"+query_image_arg)

print "Running script 2/4"
print "python2.7 query_image_feature_extraction.py "+data_dir+" "+query_image_arg
os.system("python2.7 query_image_feature_extraction.py "+data_dir+" "+query_image_arg)

print "Running script 3/4"
print "python2.7 query_matcher_improved_ransac.py "+data_dir+" "+query_image_arg+" "+benchmarking + " " + intrinsics_matrix_path
os.system("python2.7 query_matcher_improved_ransac.py "+data_dir+" "+query_image_arg+" "+benchmarking + " " + intrinsics_matrix_path)

print "Running script 4/4"
print "python2.7 visualizer.py "+data_dir+"/query_images/"+query_image_arg + " " + benchmarking
os.system("python2.7 visualizer.py "+data_dir+"/query_images/"+query_image_arg + " " + benchmarking)

if(extract_3D_points_from_sparse == "1"):
    print "Extracting 3D points from sparse model folder.."
    print "python2.7 model_points3D_extractor.py "+data_dir
    os.system("python2.7 model_points3D_extractor.py "+data_dir)
