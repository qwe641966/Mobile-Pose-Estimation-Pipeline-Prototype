import os
import sys

data_images_dir = sys.argv[1]

# setting up the dataset
os.system("ls -d "+data_images_dir+"/* > data_images_list")
os.system("/Users/alex/Projects/EngDLocalProjects/Lego/Libvot/libvot/build/bin/libvot_feature data_images_list")
os.system("ls -d "+data_images_dir+"/*.sift > data_images_sift_list")
# TODO: might need to modify image_search to make it faster
os.system("/Users/alex/Projects/EngDLocalProjects/Lego/Libvot/libvot/build/bin/image_search data_images_sift_list ./data_images_vocab_out 6 8 0")
