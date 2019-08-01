import os
import sys
import pdb

data_images_dir = sys.argv[1]
data_dir = data_images_dir.rsplit("/",1)[0]

# setting up the dataset
os.system("ls -d "+data_images_dir+"/* > " + data_dir + "/data_images_list")
os.system("/Users/alex/Projects/EngDLocalProjects/Lego/Libvot/libvot/build/bin/libvot_feature " + data_dir + "/data_images_list")
os.system("ls -d "+data_images_dir+"/*.sift > data_images_sift_list")
# TODO: might need to modify image_search to make it faster
os.system("/Users/alex/Projects/EngDLocalProjects/Lego/Libvot/libvot/build/bin/image_search data_images_sift_list ." + data_dir + "/model_images_vocab_out 6 8 0")
os.system("rm data_images_sift_list")