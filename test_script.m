t = importdata('results/arcore/pnp_ransac_translation_vector_direct.txt');
quat = importdata('results/arcore/rotation_direct_matching_as_quaternion.txt');
quat = [quat(4), quat(1), quat(2), quat(3)]; % because matlab does (w,x,y,z)
points3D = importdata('results/arcore/3D_points_direct.txt');
points3D = [points3D ones(size(points3D,1),1)];

R = quat2rotm(quat);

Rt = [R t];

Rt = [Rt ; 0 0 0 1];

points3D_Rt = Rt * points3D';

% arcore [x:-0.097, y:0.052, z:-0.005], q:[x:0.03, y:-0.03, z:-0.72, w:-0.69]

t_ar_core = [-0.097, 0.052, -0.005]';
quat_ar_core = [-0.69, 0.03, -0.03, -0.72]; % matlab notation
R_ar_core = quat2rotm(quat_ar_core);

Rt_ar_core = [R_ar_core t_ar_core];
Rt_ar_core = [Rt_ar_core ; 0 0 0 1];

last_points = [inv(Rt_ar_core) * points3D_Rt]';

figure;
plot3(last_points(:,1),last_points(:,2),last_points(:,3),'*');