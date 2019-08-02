import os
import sys
import pdb

data_dir = sys.argv[1]
query_image_filename = sys.argv[2]
query_image_filename_db_name = query_image_filename.split(".")[0]

os.system("touch "+data_dir+"/query_images_databases/database_for_"+query_image_filename_db_name+".db")
os.system("tools/colmap/COLMAP.app/Contents/MacOS/colmap feature_extractor --database_path "+data_dir+"/query_images_databases/database_for_"+query_image_filename_db_name+".db --image_path "+data_dir+"/query_images/")