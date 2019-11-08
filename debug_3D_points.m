clear all;

% one camera at a time this time we do frame_1572625139.txt

% COLMAP
colmap_correspondences = importdata('data/coop7/points_correspondences/frame_1572625139_correspondences.txt');
colmap_points3D = colmap_correspondences(:,131:133);
colmap_points2D = colmap_correspondences(:,129:130);
colmap_pose_data_gt = importdata('data/coop7/colmap_ground_truth_data_poses/frame_1572625139gt_pose.txt');
quat = colmap_pose_data_gt(1:4,1);
trans = colmap_pose_data_gt(5:7,1);
rotm = quat2rotm(quat');
camera_location = -rotm' * trans;
colmap_pose = [rotm trans ; 0 0 0 1];

figure
pcshow(colmap_points3D,'VerticalAxis','Y','VerticalAxisDir','down','MarkerSize', 20);
hold on;
plotCamera('Location', camera_location, 'Orientation', rotm, 'Size', 0.6, 'Color', [1, 0, 0]);
hold on;
plot3(0,0,0,'g*');
title('COLMAP Pose and Map for 1572625139');
xlabel('X');
ylabel('Y');
zlabel('Z');

% ARCORE
cpuCameraIntrinsics = importdata('matlab_debug_data/cpuCameraIntrinsics.txt');
cameraParams = cameraParameters('IntrinsicMatrix', cpuCameraIntrinsics');
arcore_3D_correspondences = importdata('data/coop7/arcore_data/test_data/cpuImageCorrespondences_1572625139.txt');
arcore_3D_points = arcore_3D_correspondences(:,3:5);
[worldOrientation, worldLocation] = estimateWorldCameraPose(arcore_3D_correspondences(:,1:2),arcore_3D_correspondences(:,3:5),cameraParams);
[rotationMatrix, translationVector] = cameraPoseToExtrinsics(worldOrientation,worldLocation);
ar_core_pose = [rotationMatrix translationVector' ; 0 0 0 1];

figure
pcshow(arcore_3D_points,'VerticalAxis','Y','VerticalAxisDir','down','MarkerSize', 20);
hold on;
plotCamera('Location', worldLocation, 'Orientation', worldOrientation, 'Size', 0.1, 'Color', [0, 0, 1]);
hold on;
plot3(0,0,0,'g*');
title('ARCore Pose and Map for 1572625139');
xlabel('X');
ylabel('Y');
zlabel('Z');

colmap_points3D = [colmap_points3D  ones(length(colmap_points3D),1)];
final_3D_points = [inv(colmap_pose) * ar_core_pose * colmap_points3D']'; % correct ?
final_3D_points_plain = final_3D_points(:,1:3);

figure
pcshow(final_3D_points_plain,'VerticalAxis','Y','VerticalAxisDir','down','MarkerSize', 20);
hold on;
plotCamera('Location', worldLocation, 'Orientation', worldOrientation, 'Size', 0.6, 'Color', [0, 0, 1]);
hold on;

plot3(0,0,0,'g*');
hold on;
x_axis = mArrow3([0 0 0],[6 0 0], 'color', 'red', 'stemWidth', 0.1);
hold on;
y_axis = mArrow3([0 0 0],[0 6 0], 'color', 'green', 'stemWidth', 0.1);
hold on;
z_axis = mArrow3([0 0 0],[0 0 6], 'color', 'blue', 'stemWidth', 0.1);

title('COLMAP Points in ARCore reference frame for 1572625139');
xlabel('X');
ylabel('Y');
zlabel('Z');

% points_2D_projected_for_ARCore_frame = [cpuCameraIntrinsics * colmap_correspondences']';
% points_2D_projected_for_ARCore_frame = points_2D_projected_for_ARCore_frame ./ points_2D_projected_for_ARCore_frame(:,3);
% 
points_2D_projected_for_ARCore_frame = cpuCameraIntrinsics * arcore_3D_correspondences(:,3:5)';
points_2D_projected_for_ARCore_frame = points_2D_projected_for_ARCore_frame';
points_2D_projected_for_ARCore_frame = points_2D_projected_for_ARCore_frame ./ points_2D_projected_for_ARCore_frame(:,3);

save('colmap_points2D.mat', 'points_2D_projected_for_ARCore_frame');

term = [colmap_pose * colmap_points3D']';
term = term(:,1:3);
my_colmap_2D_points = [cpuCameraIntrinsics * term']';
my_colmap_2D_points = my_colmap_2D_points ./ my_colmap_2D_points(:,3);

term = [colmap_pose * eye(4) * colmap_points3D']';
term = term(:,1:3);
my_colmap_2D_points_eye = [cpuCameraIntrinsics * term']';
my_colmap_2D_points_eye = my_colmap_2D_points_eye ./ my_colmap_2D_points_eye(:,3);

term = [inv(ar_core_pose) * colmap_pose * colmap_points3D']';
term = term(:,1:3);

points_2D_projected_for_ARCore_frame = [cpuCameraIntrinsics * term']';
points_2D_projected_for_ARCore_frame = points_2D_projected_for_ARCore_frame ./ points_2D_projected_for_ARCore_frame(:,3);
points_2D_projected_for_ARCore_frame = points_2D_projected_for_ARCore_frame(:,1:2);

save('points_2D_projected_for_ARCore_frame_1.mat', 'points_2D_projected_for_ARCore_frame');

term = [ar_core_pose * inv(colmap_pose) * colmap_points3D']';
term = term(:,1:3);

points_2D_projected_for_ARCore_frame = [cpuCameraIntrinsics * term']';
points_2D_projected_for_ARCore_frame = points_2D_projected_for_ARCore_frame ./ points_2D_projected_for_ARCore_frame(:,3);
points_2D_projected_for_ARCore_frame = points_2D_projected_for_ARCore_frame(:,1:2);

save('points_2D_projected_for_ARCore_frame_2.mat', 'points_2D_projected_for_ARCore_frame');

term = [inv(colmap_pose) * ar_core_pose * colmap_points3D']';
term = term(:,1:3);

points_2D_projected_for_ARCore_frame = [cpuCameraIntrinsics * term']';
points_2D_projected_for_ARCore_frame = points_2D_projected_for_ARCore_frame ./ points_2D_projected_for_ARCore_frame(:,3);
points_2D_projected_for_ARCore_frame = points_2D_projected_for_ARCore_frame(:,1:2);

save('points_2D_projected_for_ARCore_frame_3.mat', 'points_2D_projected_for_ARCore_frame');

term = [colmap_pose * inv(ar_core_pose) * colmap_points3D']';
term = term(:,1:3);

points_2D_projected_for_ARCore_frame = [cpuCameraIntrinsics * term']';
points_2D_projected_for_ARCore_frame = points_2D_projected_for_ARCore_frame ./ points_2D_projected_for_ARCore_frame(:,3);
points_2D_projected_for_ARCore_frame = points_2D_projected_for_ARCore_frame(:,1:2);

save('points_2D_projected_for_ARCore_frame_4.mat', 'points_2D_projected_for_ARCore_frame');
