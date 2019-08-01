import os
import sys

query_image_file_location = sys.argv[1]
query_image_filename = query_image_file_location.split("/")[len(query_image_file_location.split("/"))-1].split(".")[0]
query_image_dir = query_image_file_location.rsplit("/", 1)[0]

os.system("ls -d "+query_image_dir+"/* > query_image_list")
os.system("/Users/alex/Projects/EngDLocalProjects/Lego/Libvot/libvot/build/bin/libvot_feature query_image_list")
os.system("/Users/alex/Projects/EngDLocalProjects/Lego/Libvot/libvot/build/bin/web_search "+query_image_dir+"/"+query_image_filename+".sift data_images_list model_images_vocab_out/db.out")
os.system("head -1 "+query_image_filename+".rank > image_retrieval_result_for_"+query_image_filename+".txt")
os.system("rm "+query_image_dir+"/"+query_image_filename+".sift")

