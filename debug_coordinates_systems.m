% COLMAP
colmap_3D_points = importdata('data/coop7/model_points3D.txt');

% ARCore - They load up in text file name order.
dinfo = dir('data/coop7/arcore_data/correspondences/cpuImageCorrespondences*.txt');
ar_core_3D_points = [];
for i = 1 : length(dinfo)
    dinfo(i).name
    correspondence  = importdata(fullfile('data/coop7/arcore_data/correspondences/', dinfo(i).name));
    ar_core_3D_points = [ar_core_3D_points ; correspondence(:,3:5) ];    
end

figure
pcshow(colmap_3D_points,'VerticalAxis','Y','VerticalAxisDir','down','MarkerSize', 30);
hold on;
pcshow(ar_core_3D_points,'VerticalAxis','Y','VerticalAxisDir','down','MarkerSize', 30);
hold on;
plot3(0,0,0,'g*');
hold on;
x_axis = mArrow3([0 0 0],[5 0 0], 'color', 'red', 'stemWidth', 0.2);
hold on;
y_axis = mArrow3([0 0 0],[0 5 0], 'color', 'green', 'stemWidth', 0.2);
hold on;
z_axis = mArrow3([0 0 0],[0 0 5], 'color', 'blue', 'stemWidth', 0.2);

title('Debug');
xlabel('X');
ylabel('Y');
zlabel('Z');

