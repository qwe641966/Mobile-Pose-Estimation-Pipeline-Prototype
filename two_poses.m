clear all;

colmap_correspondences = importdata('data/coop7/points_correspondences/frame_1572625116_correspondences.txt');
points3D_viewed_from_frame_0 = colmap_correspondences(:,131:133);
points3D_viewed_from_frame_0 = [points3D_viewed_from_frame_0  ones(length(points3D_viewed_from_frame_0),1)];

colmap_pose_data_gt = importdata('data/coop7/colmap_ground_truth_data_poses/frame_1572625116gt_pose.txt');
quat = colmap_pose_data_gt(1:4,1);
trans = colmap_pose_data_gt(5:7,1);
rotm = quat2rotm(quat');
colmap_pose = [rotm trans ; 0 0 0 1];

% cpuCameraIntrinsics
K = importdata('matlab_debug_data/cpuCameraIntrinsics.txt'); % the ar_core frame has  to in be in landscape
cameraParams = cameraParameters('IntrinsicMatrix', K'); %TODO - check the transpose ???

% pose for frame 0
arcore_3D_correspondences = importdata('data/coop7/arcore_data/test_data/cpuImageCorrespondences_1572625116.txt');
arcore_3D_points = arcore_3D_correspondences(:,3:5);
[worldOrientation, worldLocation] = estimateWorldCameraPose(arcore_3D_correspondences(:,1:2),arcore_3D_points,cameraParams);
[rotationMatrix, translationVector] = cameraPoseToExtrinsics(worldOrientation,worldLocation);
P0 = [rotationMatrix translationVector' ; 0 0 0 1];

% pose for frame 1
arcore_3D_correspondences = importdata('data/coop7/arcore_data/test_data/cpuImageCorrespondences_1572625114.txt');
arcore_3D_points = arcore_3D_correspondences(:,3:5);
[worldOrientation, worldLocation] = estimateWorldCameraPose(arcore_3D_correspondences(:,1:2),arcore_3D_points,cameraParams);
[rotationMatrix, translationVector] = cameraPoseToExtrinsics(worldOrientation,worldLocation);
P1 = [rotationMatrix translationVector' ; 0 0 0 1];

% frame 0
ar_core_pose_relative = eye(4);
term = ar_core_pose_relative * colmap_pose * points3D_viewed_from_frame_0';
term = term(1:3,:);
points2D = K * term;
points2D = points2D';
points2D = points2D ./ points2D(:,3);
points2D = points2D(:,1:2);

save('points2D_frame_1572625116.mat', 'points2D');

% frame 1
ar_core_pose_relative = inv(P1) * P0;
term = ar_core_pose_relative * colmap_pose * points3D_viewed_from_frame_0';
term = term(1:3,:);
points2D = K * term;
points2D = points2D';
points2D = points2D ./ points2D(:,3);
points2D = points2D(:,1:2);

save('points2D_frame_1572625114.mat', 'points2D');
