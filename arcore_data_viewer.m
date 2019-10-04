clear all;

points = importdata('matlab_debug_data/data_ar/points3Dworld.txt');
points = reshape(points, 4, [])'; % (x, y, z, c)
points = [points(:,1:3) ones(size(points,1),1)];

correspondences = importdata('matlab_debug_data/data_ar/correspondences.txt');
cpuImageCorrespondences = importdata('matlab_debug_data/data_ar/cpuImageCorrespondences.txt');
cpuImageCorrespondencesXY = cpuImageCorrespondences(:,1:2);

posemtx_android_sensor = importdata('matlab_debug_data/data_ar/posemtx_android_sensor.txt');
posemtx_oriented = importdata('matlab_debug_data/data_ar/posemtx_oriented.txt');
posemtx_plain = importdata('matlab_debug_data/data_ar/posemtx_plain.txt');

projmtx = importdata('matlab_debug_data/data_ar/projmtx.txt');
viewmtx = importdata('matlab_debug_data/data_ar/viewmtx.txt');

ndc = projmtx * viewmtx * points';
ndc = ndc';
ndc = ndc ./ ndc(:,4);

x_screen = 1440 * ((ndc(:,1) + 1) / 2);
y_screen = 2880 * ((1 - ndc(:,2)) / 2 );

xy = [x_screen y_screen];

[regParams,Bfit,ErrorStats]=absor(correspondences(:,1:2)', cpuImageCorrespondencesXY');

cpuImageCorrespondencesXY = regParams.M * [correspondences(:,1:2) ones(size(correspondences,1),1)]';
cpuImageCorrespondencesXY = cpuImageCorrespondencesXY';

figure;
scatter(correspondences(:,1),correspondences(:,2));

figure;
scatter(cpuImageCorrespondencesXY(:,1),cpuImageCorrespondencesXY(:,2));

% restrict for testing
% correspondences = correspondences(1:4,1:2); % or xy
% cpuImageCorrespondencesXY = [x_screen*480/1440 , y_screen*640/2880];

save('matlab_debug_data/data_ar/correspondencesXY.txt', 'correspondences', '-ascii', '-double');
save('matlab_debug_data/data_ar/cpuImageCorrespondencesXY.txt', 'cpuImageCorrespondencesXY', '-ascii', '-double');

% cancel the pose
% points_raw = inv(posemtx) * points';

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
