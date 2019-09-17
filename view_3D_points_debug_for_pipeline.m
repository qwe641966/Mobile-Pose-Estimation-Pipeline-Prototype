all_3d_points = importdata('data/work_alt_desk/model_points3D.txt');

all_3d_points_dm = importdata('results/arcore/3D_points_direct.txt');
all_3d_points_image_retrieval = importdata('results/arcore/3D_points_image_retrieval.txt');

% ARCore mobile phone pose
ar_core_pose = importdata('data/work_alt_desk/ar_core_poses/pose.txt');
ar_core_pose_R = ar_core_pose(1:3,1:3);
ar_core_pose_t = ar_core_pose(1:3,4);
camera_location_arcore = -ar_core_pose_R' * ar_core_pose_t;

% Image retrieval pose:
pose_img_retrieval = importdata('results/arcore/RT_image_retrieval.txt');
camera_R_img_retrieval = pose_img_retrieval(1:3, 1:3);
camera_T_img_retrieval = pose_img_retrieval(1:3, 4);
camera_location_img_retrieval = -camera_R_img_retrieval' * camera_T_img_retrieval;

% Direct Matching:
pose_direct_matching = importdata('results/arcore/RT_direct_matching.txt');
camera_R_direct_matching = pose_direct_matching(1:3, 1:3);
camera_T_direct_matching = pose_direct_matching(1:3, 4);
camera_location_direct_matching = -camera_R_direct_matching' * camera_T_direct_matching;


homogeneous = ones(size(all_3d_points_dm(:,1),1),1);
all_3d_points_dm = [all_3d_points_dm homogeneous];

homogeneous = ones(size(all_3d_points_image_retrieval(:,1),1),1);
all_3d_points_image_retrieval = [all_3d_points_image_retrieval homogeneous];

% 3D point in ARCore
ar_core_3D_points = inv(ar_core_pose) * [[camera_R_img_retrieval camera_T_img_retrieval] ; 0 0 0 1] * all_3d_points_dm';
ar_core_3D_points = ar_core_3D_points';

figure;
plot3(ar_core_3D_points(:,1),ar_core_3D_points(:,2),ar_core_3D_points(:,3),'*');
hold on
plot3(0,0,0,'g*');
hold on
plotCamera('Location', camera_location_arcore, 'Orientation', ar_core_pose_R, 'Size', 1);

% write to file
fid = fopen('ar_core_3D_points_matlab.txt','wt');
for k = 1:size(ar_core_3D_points,1)
    fprintf(fid,'%4.5f ',ar_core_3D_points(k,1:3));
    fprintf(fid,'\n');
end
fclose(fid);
 
% figure;
% plot3(all_3d_points(:,1),all_3d_points(:,2),all_3d_points(:,3),'*');
% hold on
% plot3(0,0,0,'g*');
% hold on
% plotCamera('Location', camera_location_img_retrieval, 'Orientation', camera_R_img_retrieval, 'Size', 1);
% hold on
% plotCamera('Location', camera_location_direct_matching, 'Orientation', camera_R_direct_matching, 'Size', 1, 'Color', [0 1 0]);
% hold on
% plotCamera('Location', camera_location_arcore, 'Orientation', ar_core_pose_R, 'Size', 1, 'Color', [0 0 1]);
