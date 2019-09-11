colmap_worldPoints_before_RT_from_direct = importdata('results/IMG_7944/3D_points_direct.txt');
colmap_worldPoints_after_RT_from_direct = importdata('results/IMG_7944/3Dpoints_after_RT_multiplication.txt');
cam_est_rotation_vector = importdata('results/IMG_7944/pnp_ransac_rotation_vector_direct.txt');
cam_est_trans_vector = importdata('results/IMG_7944/pnp_ransac_translation_vector_direct.txt');

R = [0.998500 -0.006900 -0.053600;
     0.009600 0.998700 0.049200;
     0.053200 -0.049600 0.997400];
    
t = [-0.314300, 0.607500, 0.333600]';

% camera center ?
location = -R' * t;
orientation = R;

figure;
plot3(colmap_worldPoints_before_RT_from_direct(:,1),colmap_worldPoints_before_RT_from_direct(:,2),colmap_worldPoints_before_RT_from_direct(:,3),'*');
hold on
plot3(colmap_worldPoints_after_RT_from_direct(:,1),colmap_worldPoints_after_RT_from_direct(:,2),colmap_worldPoints_after_RT_from_direct(:,3),'*');
hold on
plot3(0,0,0,'g*');
hold on
cam_est = plotCamera('Location',location,'Orientation',orientation,'Size', 1);