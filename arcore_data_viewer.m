clear all;

points = importdata('matlab_debug_data/data_ar/points3Dworld.txt');
points = reshape(points, 4, [])'; % (x, y, z, c)
points = [points(:,1:3) ones(size(points,1),1)];

correspondences = importdata('matlab_debug_data/data_ar/correspondences.txt');
cpuImageCorrespondences = importdata('matlab_debug_data/data_ar/cpuImageCorrespondences.txt');

correspondencesXY = correspondences(:,1:2);
cpuImageCorrespondencesXY = cpuImageCorrespondences(:,1:2);

cpuCameraIntrinsics = importdata('matlab_debug_data/data_ar/cpuCameraIntrinsics.txt');

posemtx_android_sensor = importdata('matlab_debug_data/data_ar/posemtx_android_sensor.txt');
posemtx_oriented = importdata('matlab_debug_data/data_ar/posemtx_oriented.txt');
posemtx_plain = importdata('matlab_debug_data/data_ar/posemtx_plain.txt');

projmtx = importdata('matlab_debug_data/data_ar/projmtx.txt');
projmtxFromFrame = importdata('matlab_debug_data/data_ar/projmtxFromFrame.txt');
viewmtx = importdata('matlab_debug_data/data_ar/viewmtx.txt');

ndc = projmtx * viewmtx * points';
ndc = ndc';
ndc = ndc ./ ndc(:,4);

x_screen = 1440 * ((ndc(:,1) + 1) / 2);
y_screen = 2880 * ((1 - ndc(:,2)) / 2 );

xy = [x_screen y_screen];

save('matlab_debug_data/data_ar/cpuImageCorrespondencesXY.txt', 'cpuImageCorrespondencesXY', '-ascii', '-double');

% for open cv pnp
opencv_2D3D = [cpuImageCorrespondencesXY points];
save('matlab_debug_data/data_ar/cpuCameraIntrinsics.txt', 'cpuCameraIntrinsics', '-ascii', '-double');
save('matlab_debug_data/data_ar/opencv_2D3D.txt', 'opencv_2D3D', '-ascii', '-double');

cameraParams = cameraParameters('IntrinsicMatrix', cpuCameraIntrinsics');
% worldLocation this is different from the one OpenCV returns. That is the
% translation
[worldOrientation, worldLocation] = estimateWorldCameraPose(opencv_2D3D(:,1:2),opencv_2D3D(:,3:5),cameraParams);

pcshow(opencv_2D3D(:,3:5),'VerticalAxis','Y','VerticalAxisDir','down','MarkerSize',30);
hold on
plotCamera('Size',0.1,'Orientation',worldOrientation,'Location',worldLocation);
xlabel('X');
ylabel('Y');
zlabel('Z');
hold off

% points = points(:,1:3)'; % only need (x,y,z) for the next steps
% 
% xy_cpuImage = cpuCameraIntrinsics * points;
% xy_cpuImage = xy_cpuImage';
% xy_cpuImage = xy_cpuImage ./ xy_cpuImage(:,3);
% save('matlab_debug_data/data_ar/xy_cpuImage.txt', 'xy_cpuImage', '-ascii', '-double');


t_posemtx_android_sensor = posemtx_android_sensor(1:3,4);
R_posemtx_android_sensor = posemtx_android_sensor(1:3,1:3);

t_posemtx_oriented = posemtx_oriented(1:3,4);
R_posemtx_oriented = posemtx_oriented(1:3,1:3);

t_posemtx_plain = posemtx_plain(1:3,4);
R_posemtx_plain = posemtx_plain(1:3,1:3);

c_posemtx_android_sensor = -R_posemtx_android_sensor' * t_posemtx_android_sensor;
c_posemtx_oriented = -R_posemtx_oriented' * t_posemtx_oriented;
c_posemtx_plain = -R_posemtx_plain' * t_posemtx_plain;

% figure;
% plot3(points(:,1),points(:,2),points(:,3),'r*');
% hold on
% plot3(0,0,0,'g*');
% hold on
% plotCamera('Location', c_posemtx_android_sensor, 'Orientation', R_posemtx_android_sensor', 'Size', 0.05, 'Color', [0 1 1]);
% hold on
% plotCamera('Location', c_posemtx_oriented, 'Orientation', R_posemtx_oriented', 'Size', 0.05, 'Color', [0 0 1]);
% hold on
% plotCamera('Location', c_posemtx_plain, 'Orientation', R_posemtx_plain', 'Size', 0.05, 'Color', [0 1 0]);
% xlabel('x')
% ylabel('y')
% zlabel('z')
