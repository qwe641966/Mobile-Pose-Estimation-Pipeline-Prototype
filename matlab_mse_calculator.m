% these were aquired using the image retrieval method.
mse_data = load('mse_data.mat');
mse_data = mse_data.value;

%ground truth
ground_truths_rotation_quarternions = mse_data(:,1:4);
rotation_matrices_gt = quat2rotm(ground_truths_rotation_quarternions);
translations_gt = mse_data(:,5:7);

%est values
est_rotation_quarternions = mse_data(:,8:11);
rotation_matrices_est = quat2rotm(est_rotation_quarternions);
translations_est = mse_data(:,12:14);

% The first three elements of every row specify the rotation axis, 
% and the last element defines the rotation angle (in radians).
axang_gt = rotm2axang(rotation_matrices_gt);
axang_est = rotm2axang(rotation_matrices_est);

% errors calculation
% In this scheme the error is in fact a 3-tuple, 
% the distance error, the axis error, and the angle error.
total_errors = [];

trans_errors = [];
for i = 1:len(1)
	t_error = norm(translations_gt(i,:) - translations_est(i,:));
    trans_errors(i) = t_error;
end

angle_errors = [];
for i = 1:len(1)
	a_error = norm(axang_gt(i,4) - axang_est(i,4));
    angle_errors(i) = a_error;
end

rotations_errors = [];
for i = 1:len(1)
    if i == 77
        foo = i;
    end
	r_error = norm(cross(axang_gt(i,1:3),axang_est(i,1:3)));
    rotations_errors(i) = r_error;
end

% Christian's approach - compare camera centers
camera_center_errors = [];
for i = 1:len(1)
    camera_center_gt = -rotation_matrices_gt(:,:,i)'*translations_gt(i,:)';
	camera_center_est = -rotation_matrices_est(:,:,i)'*translations_est(i,:)';
    
    camera_center_error = sqrt(mean((camera_center_gt - camera_center_est).^2));
    camera_center_errors(i) = camera_center_error;
end

bar(camera_center_errors); % camera center's error
title('Camera Center Errors', 'FontSize', 16 );
xlabel('Image File Index', 'FontSize', 16 );
ylabel('MSE', 'FontSize', 16 );

% 2D errors
% bar(trans_errors); % distance
% bar(rotations_errors); % axis
%  bar(angle_errors); % angle
% title('Errors Normalised (variance = 1)', 'FontSize', 16 );
% xlabel('Image File Index', 'FontSize', 16 );
% ylabel('MSE', 'FontSize', 16 );

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

