mse_data = load('data/coop3/mse_data.mat');
mse_data = mse_data.value;

names = mse_data(:,24);
len = size(names);

% distance is in pixels here

% DM
reprojection_errors = [];
for i = 1:len(1)
	matches3d2d_direct = sprintf('results/IMG_%d/final_match_array_direct.txt', names(i));
    matches3d2d_direct = importdata(matches3d2d_direct);
    
    points2D_gt = matches3d2d_direct(:,1:2);
    points3D_gt = matches3d2d_direct(:,3:5);
    
    % make homogeneous
    points3D_gt_ones = size(points3D_gt);
    points3D_gt_ones = points3D_gt_ones(1);
    points3D_gt_ones = ones(points3D_gt_ones,1);
    points3D_gt = [points3D_gt points3D_gt_ones];
    
    trans_direct = sprintf('results/IMG_%d/pnp_ransac_translation_vector_direct.txt', names(i));
    trans_direct = importdata(trans_direct);
    
    intrinsics_matrix = sprintf('results/IMG_%d/intrinsics_matrix.txt', names(i));
    intrinsics_matrix = importdata(intrinsics_matrix);
    
    rotation_vector_direct = sprintf('results/IMG_%d/pnp_ransac_rotation_vector_direct.txt', names(i));
    rotation_vector_direct = importdata(rotation_vector_direct);
    
    rotation_matrix_direct = rotationVectorToMatrix(rotation_vector_direct)'; 
    
    rt_ransac = [rotation_matrix_direct trans_direct];
    rt_ransac = [ rt_ransac ; [0 0 0 1]];
    
    rt_result = rt_ransac * points3D_gt';
    rt_result = rt_result';
    rt_result = rt_result(:,1:3);
    points2D_est = intrinsics_matrix * rt_result';
    points2D_est = points2D_est';
    points2D_est = points2D_est ./ points2D_est(:,3);
    points2D_est = points2D_est(:,1:2);
    
    points_len = size(points2D_est);
    
    distances = [];
    for k = 1:points_len(1)
        distance = norm(points2D_est(k,:) - points2D_gt(k,:));
        distances = [distances ; distance];
    end
    
    reprojection_errors(i) = mean(distances);
end

figure;

bar(reprojection_errors);
set(gca,'XTick', [ 1:len(1) ],'xticklabel', names);
xtickangle(90);
title('Reprojection Error DM', 'FontSize', 16 );
xlabel('Image File Index', 'FontSize', 16 );
ylabel('Error in Pixels', 'FontSize', 16 );

mean(reprojection_errors)

%Image retrieval
reprojection_errors = [];
for i = 1:len(1)
	matches3d2d_direct = sprintf('results/IMG_%d/final_match_array_image_retrieval_matching.txt', names(i));
    matches3d2d_direct = importdata(matches3d2d_direct);
    
    points2D_gt = matches3d2d_direct(:,1:2);
    points3D_gt = matches3d2d_direct(:,3:5);
    
    % make homogeneous
    points3D_gt_ones = size(points3D_gt);
    points3D_gt_ones = points3D_gt_ones(1);
    points3D_gt_ones = ones(points3D_gt_ones,1);
    points3D_gt = [points3D_gt points3D_gt_ones];
    
    trans_direct = sprintf('results/IMG_%d/pnp_ransac_translation_vector_image_retrieval.txt', names(i));
    trans_direct = importdata(trans_direct);
    
    intrinsics_matrix = sprintf('results/IMG_%d/intrinsics_matrix.txt', names(i));
    intrinsics_matrix = importdata(intrinsics_matrix);
    
    rotation_vector_direct = sprintf('results/IMG_%d/pnp_ransac_rotation_vector_image_retrieval.txt', names(i));
    rotation_vector_direct = importdata(rotation_vector_direct);
    
    rotation_matrix_direct = rotationVectorToMatrix(rotation_vector_direct)'; 
    
    rt_ransac = [rotation_matrix_direct trans_direct];
    rt_ransac = [ rt_ransac ; [0 0 0 1]];
    
    rt_result = rt_ransac * points3D_gt';
    rt_result = rt_result';
    rt_result = rt_result(:,1:3);
    points2D_est = intrinsics_matrix * rt_result';
    points2D_est = points2D_est';
    points2D_est = points2D_est ./ points2D_est(:,3);
    points2D_est = points2D_est(:,1:2);
    
    points_len = size(points2D_est);
    
    distances = [];
    for k = 1:points_len(1)
        distance = norm(points2D_est(k,:) - points2D_gt(k,:));
        distances = [distances ; distance];
    end
    
    reprojection_errors(i) = mean(distances);
end

figure;

bar(reprojection_errors);
set(gca,'XTick', [ 1:len(1) ],'xticklabel', names);
xtickangle(90);
title('Reprojection Error Image Retrieval', 'FontSize', 16 );
xlabel('Image File Index', 'FontSize', 16 );
ylabel('Error in Pixels', 'FontSize', 16 );

mean(reprojection_errors)
