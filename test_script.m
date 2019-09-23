points3D = importdata('results/arcore/3D_points_direct.txt');
translation = importdata('results/arcore/pnp_ransac_translation_vector_direct.txt');
rotation_quat = importdata('results/arcore/rotation_direct_matching_as_quaternion.txt');
rotation_quat = rotation_quat';
% qw, qx, qy, qz - here!
rotation_matrix = quat2rotm([rotation_quat(4) rotation_quat(1) rotation_quat(2) rotation_quat(3)]);

ar_core_poses = [];

dinfo = dir('matlab_debug_data/ar_core_poses/poses/*.txt');
for i = 1 : length(dinfo)
%    dinfo(i).name
   ar_core_poses = [ar_core_poses ; importdata(fullfile('matlab_debug_data/ar_core_poses/poses/', dinfo(i).name))];
end

rt_points3D = [rotation_matrix translation ; [ 0 0 0 1 ]] * [points3D ones(size(points3D,1),1)]';

ar_translation = [ar_core_poses(1,1) ; ar_core_poses(1,2) ; ar_core_poses(1,3)];
% qw, qx, qy, qz - here!
ar_quat = [ar_core_poses(1,7) ar_core_poses(1,4)  ar_core_poses(1,5) ar_core_poses(1,6)];
ar_rotation_matrix = quat2rotm(ar_quat);

ar_rt_points_3D = inv([ar_rotation_matrix ar_translation ; [ 0 0 0 1 ]]) * rt_points3D;
ar_rt_points_3D = ar_rt_points_3D';

figure;
% scatter3(ar_rt_points_3D(:,1),ar_rt_points_3D(:,2),ar_rt_points_3D(:,3),'.');
% hold on;
plotCamera('Location', ar_translation, 'Orientation', ar_rotation_matrix, 'Size', 0.1);
hold on;
plot3(0,0,0,'g*');
hold on;

for i = 2 : length(ar_core_poses) % since the first was used
    pause
    trans = [ar_core_poses(i,1) ; ar_core_poses(i,2) ; ar_core_poses(i,3)];
    % qw, qx, qy, qz - here!
    quat = [ar_core_poses(i,7) ar_core_poses(i,4)  ar_core_poses(i,5) ar_core_poses(i,6)];
    rotation_matrix = quat2rotm(quat);
    
    plotCamera('Location', trans, 'Orientation', rotation_matrix, 'Size', 0.1);
    hold on;
end