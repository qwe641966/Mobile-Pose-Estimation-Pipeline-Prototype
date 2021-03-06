from point3D_loader import get_points3D, read_points3d_binary
from query_image import get_query_image_id_new_model
from evaluator import get_ARCore_pose_query_image
from evaluator import get_ARCore_pose_query_image_matrix_file
from query_image import get_query_image_global_pose_new_model
from get_scale import calc_scale
import numpy as np
import os
import sys

if(len(sys.argv) == 2 ):
    scale = float(sys.argv[1])
else:
    scale = 1

print("Scale: " + str(scale))

image_id_start = get_query_image_id_new_model("query.jpg")
points3D = get_points3D(image_id_start) #for query image
# points3D = read_points3d_binary('/Users/alex/Projects/EngDLocalProjects/Lego/fullpipeline/colmap_data/data/new_model/points3D.bin')
# print("Number of COLMAP 3D Points: " + str(len(points3D)))

colmap_pose = get_query_image_global_pose_new_model("query.jpg")

arcore_pose = get_ARCore_pose_query_image()
print("arcore_pose: ")
print(arcore_pose)

# arcore_pose_matrix_form = get_ARCore_pose_query_image_matrix_file()
# print("arcore_pose matrix: ")
# print(arcore_pose_matrix_form)

print("COLMAP Pose: ")
print(colmap_pose)

colmap_to_arcore_matrix = np.array([
    [1, 0, 0, 0],
    [0, -1, 0, 0],
    [0, 0, -1, 0]])
colmap_to_arcore_matrix = scale * colmap_to_arcore_matrix
colmap_to_arcore_matrix = np.r_[colmap_to_arcore_matrix, [np.array([0, 0, 0, 1])]]

print("colmap_to_arcore_matrix: ")
print(colmap_to_arcore_matrix)

rotZ = np.array([[0, 1, 0, 0],
                 [-1, 0, 0, 0],
                 [0, 0, 1, 0],
                 [0, 0, 0, 1]])

print("intermediate matrix: ")
intermediate_matrix = rotZ.dot(colmap_to_arcore_matrix)
print(intermediate_matrix)

# arcore_pose_inverse = np.linalg.inv(arcore_pose)
# print("arcore_pose_inverse: ")
# print(arcore_pose_inverse)

print('Matrix Final:')
print(rotZ.dot(arcore_pose.dot(rotZ.dot(colmap_to_arcore_matrix.dot(colmap_pose)))))

#from_colmap_world_to_colmap_camera
points3D = colmap_pose.dot(np.transpose(points3D))
#from_colmap_camera_to_arcore_camera
points3D = intermediate_matrix.dot(points3D)
#from_arcore_camera_to_arcore_world
points3D = (arcore_pose.dot(points3D))
points3D = np.transpose(points3D)

os.system("rm /Users/alex/Projects/EngDLocalProjects/LEGO/fullpipeline/colmap_data/data/points3D_AR.txt")
np.savetxt('/Users/alex/Projects/EngDLocalProjects/LEGO/fullpipeline/colmap_data/data/points3D_AR.txt', points3D)


#  before arcore world
# points3D = np.add(points3D.transpose(), [0.1567571, 0.038068496, 0.043509394, 0])
# points3D = points3D.transpose()