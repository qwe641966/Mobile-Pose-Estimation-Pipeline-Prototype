% colmap_worldPoints_before_RT_from_direct = importdata('results/IMG_7999/3D_points_direct.txt');
% colmap_worldPoints_after_RT_from_direct = importdata('results/IMG_7999/3Dpoints_after_RT_multiplication.txt');
% cam_est_rotation_vector = importdata('results/IMG_7999/pnp_ransac_rotation_vector_direct.txt');
% cam_est_trans_vector = importdata('results/IMG_7999/pnp_ransac_translation_vector_direct.txt');

all_3d_points = importdata('data/coop3/model_points3D.txt');

R_for_ar_core_JPG = [-0.131500 -0.965200 -0.226200
                      0.961100 -0.180100  0.209500
                     -0.243000 -0.189900  0.951300];

t_for_ar_core_JPG = [-2.991200, 0.603600, 3.640600]';

R_for_IMG_7944 = [0.998500 -0.006900 -0.053600;
                  0.009600  0.998700  0.049200;
                  0.053200 -0.049600  0.997400];
    
t_for_IMG_7944 = [-0.314300, 0.607500, 0.333600]';

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
hold on
plotCamera('Location', location_for_IMG_7944, 'Orientation', orientation_for_IMG_7944, 'Size', 1, 'Color', [0, 1, 0]);
