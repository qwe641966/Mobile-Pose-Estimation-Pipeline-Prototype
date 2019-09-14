all_3d_points = importdata('data/home_small_boxes/model_points3D.txt');

% get a pose here


% camera center ?
location_for_IMG_7944 = -R_for_IMG_7944' * t_for_IMG_7944;
orientation_for_IMG_7944 = R_for_IMG_7944;

location_ar_core = -R_for_ar_core_JPG' * t_for_ar_core_JPG;
orientation_ar_core = R_for_ar_core_JPG;

figure;
plot3(all_3d_points(:,1),all_3d_points(:,2),all_3d_points(:,3),'*');
hold on
plot3(0,0,0,'g*');
hold on
plotCamera('Location', location_ar_core, 'Orientation', orientation_ar_core, 'Size', 1);