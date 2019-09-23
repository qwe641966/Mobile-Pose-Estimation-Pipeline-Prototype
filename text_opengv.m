matched2D3D = importdata('results/arcore1280/final_match_array_direct.txt');
I = matched2D3D(:,1:2)';
P = matched2D3D(:,3:5)';
K = importdata('results/arcore1280/intrinsics_matrix.txt');

% from website
temp = K \ [I; ones(1,size(I,2))];
I_norms = sqrt(sum(temp.*temp));
I_normalized = temp ./ repmat(I_norms,3,1);

[X, inliers] = opengv('p3p_kneip_ransac',P,I_normalized);

R = X(:,1:3);
t = X(:,4);

% res = [R | T] * [3D points]
res = [X ; 0 0 0 1] * [P; ones(1,size(P,2))];
res = res(1:3,:);

res = K * res;
res = res ./ res(3,:);