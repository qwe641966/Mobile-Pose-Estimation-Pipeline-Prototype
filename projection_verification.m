clear all;

% for frame frame_1572625114

K = importdata('matlab_debug_data/cpuCameraIntrinsics.txt');
correspondences = importdata('data/coop7/points_correspondences/frame_1572625114_correspondences.txt');
points2D = correspondences(:,129:130);
points3D = correspondences(:,131:133);
points3D = [points3D  ones(length(points3D),1)];
ARPose = importdata('data/coop7/arcore_data/display_oriented_poses/displayOrientedPose_1572625114.txt');
COLMAPPose = importdata('data/coop7/colmap_ground_truth_data_poses/frame_1572625114gt_pose.txt');
quat = COLMAPPose(1:4,1);
trans = COLMAPPose(5:7,1);
rotm = quat2rotm(quat');
COLMAPPose = [rotm trans ; 0 0 0 1];

term = inv(ARPose) * COLMAPPose * points3D';
points2D_phone = K * term(1:3,:);
points2D_phone = points2D_phone';
points2D_phone = points2D_phone ./ points2D_phone(:,3);