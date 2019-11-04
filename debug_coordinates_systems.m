clear all;

% COLMAP
colmap_3D_points = importdata('data/coop7/model_points3D.txt');
iphoneCameraIntrinsics = importdata('intrinsics_matrices/iphone_intrinsics.txt');
iphoneCameraParams = cameraParameters('IntrinsicMatrix', iphoneCameraIntrinsics');

% ARCore - They load up in text file name order.
dinfo = dir('data/coop7/arcore_data/correspondences/cpuImageCorrespondences*.txt');
ar_core_3D_points = [];
for i = 1 : length(dinfo)
    correspondence  = importdata(fullfile('data/coop7/arcore_data/correspondences/', dinfo(i).name));
    ar_core_3D_points = [ar_core_3D_points ; correspondence(:,3:5) ];    
end

figure

pcshow(colmap_3D_points,'VerticalAxis','Y','VerticalAxisDir','down','MarkerSize', 20);
hold on;

% plot COLMAP cameras
dinfo = dir('data/coop7/colmap_ground_truth_data_poses/*.txt');
for i = 1 : length(dinfo)
    pose_data  = importdata(fullfile('data/coop7/colmap_ground_truth_data_poses/', dinfo(i).name));
    quat = pose_data(1:4,1);
    trans = pose_data(5:7,1);
    rotm = quat2rotm(quat');
    camera_location = -rotm' * trans;
    plotCamera('Location', camera_location, 'Orientation', rotm, 'Size', 0.5);
    hold on
end

% for i = 1 : length(camera_locations)
%     loc = camera_locations(i,:);
%     plot3(loc(1),loc(2),loc(3),'g*');
%     hold on
% end

% pcshow(ar_core_3D_points,'VerticalAxis','Y','VerticalAxisDir','down','MarkerSize', 30);
% hold on;
plot3(0,0,0,'g*');
hold on;
x_axis = mArrow3([0 0 0],[6 0 0], 'color', 'red', 'stemWidth', 0.1);
hold on;
y_axis = mArrow3([0 0 0],[0 6 0], 'color', 'green', 'stemWidth', 0.1);
hold on;
z_axis = mArrow3([0 0 0],[0 0 6], 'color', 'blue', 'stemWidth', 0.1);

title('Debug');
xlabel('X');
ylabel('Y');
zlabel('Z');

view(2);



