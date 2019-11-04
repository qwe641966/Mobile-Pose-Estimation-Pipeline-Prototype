% DEBUG!

% COLMAP
colmap_3D_points = importdata('data/coop7/model_points3D.txt');

% ARCore - They load up in text file name order.
dinfo = dir('data/coop7/arcore_data/correspondences/cpuImageCorrespondences*.txt');
all_3D_points = [];
for i = 1 : length(dinfo)
    correspondence  = importdata(fullfile('data/coop7/arcore_data/correspondences/', dinfo(i).name));
    all_3D_points = [all_3D_points ; correspondence(:,3:5) ];    
end

colmap_3D_points = pointCloud(colmap_3D_points);
all_3D_points = pointCloud(all_3D_points);

tform = pcregistericp(all_3D_points,colmap_3D_points,'Extrapolate',true);

all_3D_points_new = pctransform(all_3D_points, invert(tform));

figure
pcshow(all_3D_points,'VerticalAxis','Y','VerticalAxisDir','down','MarkerSize', 30);
hold on
pcshow(colmap_3D_points,'VerticalAxis','Y','VerticalAxisDir','down','MarkerSize', 30);
hold on
pcshow(all_3D_points_new,'VerticalAxis','Y','VerticalAxisDir','down','MarkerSize', 30);
% pcshowpair(colmap_3D_points, all_3D_points ,'VerticalAxis','Y','VerticalAxisDir','Down')
title('Difference Between Two Point Clouds')
xlabel('X(m)')
ylabel('Y(m)')
zlabel('Z(m)')