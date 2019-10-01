clear all;

points = importdata('matlab_debug_data/data_ar/points.txt');
points = reshape(points, 4, [])'; % (x, y, z, c)
points = [points(:,1:3) ones(size(points,1),1)];
posemtx = importdata('matlab_debug_data/data_ar/posemtx.txt');
projmtx = importdata('matlab_debug_data/data_ar/projmtx.txt');
viewmtx = importdata('matlab_debug_data/data_ar/viewmtx.txt');

ndc = projmtx * viewmtx * points';
x_screen = (ndc(1,:) + 1) * (1440 / 2 );
y_screen = (ndc(2,:) + 1) * (2880 / 2 );

x_screen = (ndc(1,:) + 1) * (1440 / 2 );
y_screen = (ndc(2,:) + 1) * (2880 / 2 );

xy = [x_screen' y_screen'];

save('matlab_debug_data/data_ar/xy.txt', 'xy', '-ascii', '-double');

% figure;
% plot3(points(:,1),points(:,2),points(:,3),'r*');
% hold on
% plot3(0,0,0,'g*');
% hold on
% plotCamera('Location', posemtx(1:3,4), 'Orientation', posemtx(1:3,1:3), 'Size', 0.05);

