clear all;

dinfo = dir('data/coop7/arcore_data/correspondences/cpuImageCorrespondences*.txt');
ar_core_3D_points = [];
ar_core_2D_points = [];
for i = 1 : length(dinfo)
    ar_core_correspondence  = importdata(fullfile('data/coop7/arcore_data/correspondences/', dinfo(i).name));
    ar_core_3D_points(:,:,i) = ar_core_correspondence(1:50,3:5);
    ar_core_2D_points(:,:,i) = ar_core_correspondence(1:50,1:2);
end

[cameraParams,imagesUsed,estimationErrors] = estimateCameraParameters(ar_core_2D_points,ar_core_3D_points);