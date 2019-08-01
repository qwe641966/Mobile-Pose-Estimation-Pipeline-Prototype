import os
import sys
import pdb

build_retrieval_database = sys.argv[1]
query_image_arg = sys.argv[2] # i.e IMG_7932.JPG
query_image_arg_no_ext = query_image_arg.split(".")[0]
data_dir = sys.argv[3] # i.e data/coop3

os.system("mkdir results/"+query_image_arg_no_ext)

if(build_retrieval_database == '1'):
    print "Creating retrieval database"
    os.system("python2.7 image_retrieval_database_creation.py "+data_dir+"/model_images")

print "Running script 1/5"
os.system("python2.7 image_retrieval_query_image.py "+data_dir+"/query_images/"+query_image_arg)
print "Running script 2/5"
os.system("python2.7 query_image_feature_extraction.py "+data_dir+" "+query_image_arg)
print "Running script 3/5"
os.system("python2.7 features_3Dpoints_builder.py "+data_dir+"/model_images_database image_retrieval_result_for_"+query_image_arg_no_ext+".txt " + query_image_arg_no_ext)
print "Running script 4/5"
os.system("python2.7 query_matcher.py "+data_dir+"/query_images_databases/database_for_"+query_image_arg_no_ext+".db "+data_dir+" " + query_image_arg_no_ext)
print "Running script 5/5"
os.system("python2.7 visualizer.py "+data_dir+"/query_images/"+query_image_arg)
