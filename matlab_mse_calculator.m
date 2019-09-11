% mse_data format
% ground_truth_rotation_quarternion, ground_truth_trans, 
%     est_rotation_quarternion_direct, translation_vector_est_direct, 
%     est_rotation_quarternion_image_retrieval, translation_vector_image_retrieval, 
%     ransac_est_direct, ransac_est_image_retrieval
%     IMG_[number], the number i.e IMG_8067 is 8067
mse_data = load('mse_data.mat');
mse_data = mse_data.value;

names = mse_data(:,24);

%ground truth
ground_truths_rotation_quarternions = mse_data(:,1:4);
rotation_matrices_gt = quat2rotm(ground_truths_rotation_quarternions);
translations_gt = mse_data(:,5:7);

est_rotation_quarternions_direct = mse_data(:,8:11);
rotation_matrices_est_direct = quat2rotm(est_rotation_quarternions_direct);
translation_vectors_est_direct = mse_data(:,12:14);

est_rotation_quarternions_image_retrieval = mse_data(:,15:18);
rotation_matrices_est_image_retrieval = quat2rotm(est_rotation_quarternions_image_retrieval);
translation_vectors_est_image_retrieval = mse_data(:,19:21);

ransac_est_direct = mse_data(:,22);
ransac_est_image_retrieval = mse_data(:,23);

% The first three elements of every row specify the rotation axis, 
% and the last element defines the rotation angle (in radians).
axang_gt = rotm2axang(rotation_matrices_gt);
axang_est_direct = rotm2axang(rotation_matrices_est_direct);
axang_est_image_retrieval = rotm2axang(rotation_matrices_est_image_retrieval);

len = size(translations_gt);

% direct matching errors
trans_errors_direct = [];
for i = 1:len(1)
	t_error = norm(translations_gt(i,:) - translation_vectors_est_direct(i,:));
    trans_errors_direct(i) = t_error;
end

angle_errors_direct = [];
for i = 1:len(1)
	a_error = norm(axang_gt(i,4) - axang_est_direct(i,4));
    angle_errors_direct(i) = a_error;
end

rotations_errors_direct = [];
for i = 1:len(1)
	r_error = norm(cross(axang_gt(i,1:3), axang_est_direct(i,1:3)));
    rotations_errors_direct(i) = r_error;
end

% image retrieval errors
trans_errors_image_retrieval = [];
for i = 1:len(1)
	t_error = norm(translations_gt(i,:) - translation_vectors_est_image_retrieval(i,:));
    trans_errors_image_retrieval(i) = t_error;
end

angle_errors_image_retrieval = [];
for i = 1:len(1)
	a_error = norm(axang_gt(i,4) - axang_est_image_retrieval(i,4));
    angle_errors_image_retrieval(i) = a_error;
end

rotations_errors_image_retrieval = [];
for i = 1:len(1)
	r_error = norm(cross(axang_gt(i,1:3), axang_est_image_retrieval(i,1:3)));
    rotations_errors_image_retrieval(i) = r_error;
end

% Christian's approach - compare camera centers
camera_center_errors_direct = [];
for i = 1:len(1)
    camera_center_gt = -rotation_matrices_gt(:,:,i)'*translations_gt(i,:)';
	camera_center_est = -rotation_matrices_est_direct(:,:,i)' * translation_vectors_est_direct(i,:)';
    
    camera_center_error = sqrt(mean((camera_center_gt - camera_center_est).^2));
    camera_center_errors_direct(i) = camera_center_error;
end

camera_center_errors_image_retrieval = [];
for i = 1:len(1)
    camera_center_gt = -rotation_matrices_gt(:,:,i)'* translations_gt(i,:)';
	camera_center_est = -rotation_matrices_est_image_retrieval(:,:,i)' * translation_vectors_est_image_retrieval(i,:)';
    
    camera_center_error = sqrt(mean((camera_center_gt - camera_center_est).^2));
    camera_center_errors_image_retrieval(i) = camera_center_error;
end

figure;

bar(camera_center_errors_direct);
set(gca,'XTick',[1:len(1)],'xticklabel', names);
xtickangle(90);
title('Camera Center Errors - DM', 'FontSize', 16 );
xlabel('Image File Index', 'FontSize', 16 );
ylabel('RMSE', 'FontSize', 16 );

figure;

bar(camera_center_errors_image_retrieval);
set(gca,'XTick',[1:len(1)],'xticklabel', names);
xtickangle(90);
title('Camera Center Errors - Image Retrieval', 'FontSize', 16 );
xlabel('Image File Index', 'FontSize', 16 );
ylabel('RMSE', 'FontSize', 16 );

figure;

bar(trans_errors_direct);
set(gca,'XTick',[1:len(1)],'xticklabel', names);
xtickangle(90);
title('Translation Errors - DM', 'FontSize', 16 );
xlabel('Image File Index', 'FontSize', 16 );
ylabel('RMSE', 'FontSize', 16 );

figure;

bar(angle_errors_direct);
set(gca,'XTick',[1:len(1)],'xticklabel', names);
xtickangle(90);
title('Angle Errors - DM', 'FontSize', 16 );
xlabel('Image File Index', 'FontSize', 16 );
ylabel('RMSE', 'FontSize', 16 );

figure;

bar(rotations_errors_direct);
set(gca,'XTick',[1:len(1)],'xticklabel', names);
xtickangle(90);
title('Rotation Axis Errors - DM', 'FontSize', 16 );
xlabel('Image File Index', 'FontSize', 16 );
ylabel('RMSE', 'FontSize', 16 );

figure;

bar(trans_errors_image_retrieval);
set(gca,'XTick',[1:len(1)],'xticklabel', names);
xtickangle(90);
title('Translation Errors - Image Retrieval', 'FontSize', 16 );
xlabel('Image File Index', 'FontSize', 16 );
ylabel('RMSE', 'FontSize', 16 );

figure;

bar(angle_errors_image_retrieval);
set(gca,'XTick',[1:len(1)],'xticklabel', names);
xtickangle(90);
title('Angle Errors - Image Retrieval', 'FontSize', 16 );
xlabel('Image File Index', 'FontSize', 16 );
ylabel('RMSE', 'FontSize', 16 );

figure;

bar(rotations_errors_image_retrieval);
set(gca,'XTick',[1:len(1)],'xticklabel', names);
xtickangle(90);
title('Rotation Axis Errors - Image Retrieval', 'FontSize', 16 );
xlabel('Image File Index', 'FontSize', 16 );
ylabel('RMSE', 'FontSize', 16 );

figure;

bar(ransac_est_direct);
set(gca,'XTick',[1:len(1)],'xticklabel', names);
xtickangle(90);
title('Ransac Inliers Percentage - DM', 'FontSize', 16 );
xlabel('Image File Index', 'FontSize', 16 );
ylabel('RMSE', 'FontSize', 16 );

figure;

bar(ransac_est_image_retrieval);
set(gca,'XTick',[1:len(1)],'xticklabel', names);
xtickangle(90);
title('Ransac Inliers Percentage - Image Retrieval', 'FontSize', 16 );
xlabel('Image File Index', 'FontSize', 16 );
ylabel('RMSE', 'FontSize', 16 );

% 3D Errors
% trans_errors_norm = (trans_errors - mean(trans_errors)) ./ std(trans_errors);
% rotations_errors_norm = (rotations_errors - mean(rotations_errors)) ./ std(rotations_errors);
% angle_errors_norm = (angle_errors - mean(angle_errors)) ./ std(angle_errors);
% 
% scatter3(trans_errors_norm, rotations_errors_norm, angle_errors_norm, 80, 'filled');
% 
% title('Errors Normalised (variance = 1)', 'FontSize', 16 );
% xlabel('Translation Errors', 'FontSize', 16 );
% ylabel('Rotation Errors', 'FontSize', 16 );
% zlabel('Angle Errors', 'FontSize', 16 );

