import os
import sys
import pdb

query_image_name = sys.argv[1]

os.system("ls -d query_image/* > query_image_list")
os.system("/Users/alex/Projects/EngDLocalProjects/Lego/Libvot/libvot/build/bin/libvot_feature query_image_list")
os.system("/Users/alex/Projects/EngDLocalProjects/Lego/Libvot/libvot/build/bin/web_search query_image/"+query_image_name+".sift data_images_list data_images_vocab_out/db.out")
os.system("head -1 "+query_image_name+".rank > image_retrieval_result.txt")
os.system("rm query_image/"+query_image_name+".sift")

