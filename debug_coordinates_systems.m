clear all;

% -------

% COLMAP
colmap_3D_points = importdata('data/coop7/model_points3D.txt');

figure

pcshow(colmap_3D_points,'VerticalAxis','Y','VerticalAxisDir','down','MarkerSize', 20);
hold on;

% plot COLMAP poses (blue) and ARCore Poses (red)
dinfo = dir('data/coop7/colmap_ground_truth_data_poses/*.txt');
for i = 1 : length(dinfo)
    pose_data  = importdata(fullfile('data/coop7/colmap_ground_truth_data_poses/', dinfo(i).name));
    quat = pose_data(1:4,1);
    trans = pose_data(5:7,1);
    rotm = quat2rotm(quat');
    camera_location = -rotm' * trans;
    
    if(length(dinfo(i).name) > 19)
        fprintf('ARCore Pose %s  \n',dinfo(i).name)
        plotCamera('Location', camera_location, 'Orientation', rotm, 'Size', 0.3, 'Color', [1, 0, 0]);
    else
        fprintf('COLMAP pose %s  \n',dinfo(i).name)
        plotCamera('Location', camera_location, 'Orientation', rotm, 'Size', 0.3, 'Color', [0, 0, 1]);
    end
    
    hold on;
end

plot3(0,0,0,'g*');
hold on;
x_axis = mArrow3([0 0 0],[6 0 0], 'color', 'red', 'stemWidth', 0.1);
hold on;
y_axis = mArrow3([0 0 0],[0 6 0], 'color', 'green', 'stemWidth', 0.1);
hold on;
z_axis = mArrow3([0 0 0],[0 0 6], 'color', 'blue', 'stemWidth', 0.1);

title('COLMAP and ARCore Poses');
xlabel('X');
ylabel('Y');
zlabel('Z');

% -------

figure

% ARCore Data.
dinfo = dir('data/coop7/arcore_data/test_data/cpuImageCorrespondences*.txt');
ar_core_3D_points = [];
for i = 1 : length(dinfo)
    ar_core_correspondence  = importdata(fullfile('data/coop7/arcore_data/test_data/', dinfo(i).name));
    ar_core_3D_points = [ar_core_3D_points ; ar_core_correspondence(:,3:5) ];    
end

pcshow(ar_core_3D_points,'VerticalAxis','Y','VerticalAxisDir','down','MarkerSize', 20);
hold on;

dinfo = dir('data/coop7/arcore_data/test_data/displayOrientedPose*.txt');
for i = 1 : length(dinfo)
    pose_data = importdata(fullfile('data/coop7/arcore_data/test_data/', dinfo(i).name));
    rot = pose_data(1:3,1:3);
    trans = pose_data(1:3,4);
    camera_location = -rot' * trans;
    
    plotCamera('Location', camera_location, 'Orientation', rot, 'Size', 0.1, 'Color', [0, 1, 0], 'AxesVisible', true);
    hold on;
end

dinfo = dir('data/coop7/arcore_data/test_data/cameraPose*.txt');
for i = 1 : length(dinfo)
    pose_data = importdata(fullfile('data/coop7/arcore_data/test_data/', dinfo(i).name));
    rot = pose_data(1:3,1:3);
    trans = pose_data(1:3,4);
    camera_location = -rot' * trans;
    
    plotCamera('Location', camera_location, 'Orientation', rot, 'Size', 0.1, 'Color', [1, 1, 0], 'AxesVisible', true);
    hold on;
end

dinfo = dir('data/coop7/arcore_data/test_data/sensorPose*.txt');
for i = 1 : length(dinfo)
    pose_data = importdata(fullfile('data/coop7/arcore_data/test_data/', dinfo(i).name));
    rot = pose_data(1:3,1:3);
    trans = pose_data(1:3,4);
    camera_location = -rot' * trans;
    
    plotCamera('Location', camera_location, 'Orientation', rot, 'Size', 0.1, 'Color', [1, 0, 1], 'AxesVisible', true);
    hold on;
end

cpuCameraIntrinsics = importdata('matlab_debug_data/cpuCameraIntrinsics.txt');
cameraParams = cameraParameters('IntrinsicMatrix', cpuCameraIntrinsics');

dinfo = dir('data/coop7/arcore_data/test_data/cpuImageCorrespondences*.txt');
for i = 1 : length(dinfo)
    correspondence  = importdata(fullfile('matlab_debug_data/data_ar/', dinfo(i).name));
    [worldOrientation, worldLocation] = estimateWorldCameraPose(correspondence(:,1:2),correspondence(:,3:5),cameraParams);
    
    plotCamera('Location', worldLocation, 'Orientation', worldOrientation, 'Size', 0.1, 'Color', [1, 1, 1], 'AxesVisible', true); %'Label', dinfo(i).name);
    hold on;
end

plot3(0,0,0,'g*');
hold on;
x_axis = mArrow3([0 0 0],[1 0 0], 'color', 'red', 'stemWidth', 0.01);
hold on;
y_axis = mArrow3([0 0 0],[0 1 0], 'color', 'green', 'stemWidth', 0.01);
hold on;
z_axis = mArrow3([0 0 0],[0 0 1], 'color', 'blue', 'stemWidth', 0.01);

title('ARCore Poses and Map');
xlabel('X');
ylabel('Y');
zlabel('Z');

