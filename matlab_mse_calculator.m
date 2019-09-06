% these were aquired using the image retrieval method.
mse_data = load('mse_data.mat');
mse_data = mse_data.value;

%ground truth
ground_truths_rotation_quarternions = mse_data(:,1:4);
rotation_matrices_gt = quat2rotm(ground_truths_rotation_quarternions);
ground_truths_trans = mse_data(:,5:7);

%estimated calculations
rotation_vectors_calculated = mse_data(:,8:10);
translation_vectors_calculated = mse_data(:,11:13);

len = size(rotation_vectors_calculated);
rotation_matrices_est = [];

for i = 1:len(1)
    rot_vector = rotation_vectors_calculated(i,:);
	rotation_matrices_est(:,:,i) = rotationVectorToMatrix(rot_vector);
end

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
	t_error = norm(ground_truths_trans(i,:) - translation_vectors_calculated(i,:));
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

% bar(trans_errors); % distance
% bar(rotations_errors); % axis
% bar(angle_errors); % angle
% title('Errors Normalised (variance = 1)', 'FontSize', 16 );
% xlabel('Image File Index', 'FontSize', 16 );
% ylabel('MSE', 'FontSize', 16 );

trans_errors_norm = (trans_errors - mean(trans_errors)) ./ std(trans_errors);
rotations_errors_norm = (rotations_errors - mean(rotations_errors)) ./ std(rotations_errors);
angle_errors_norm = (angle_errors - mean(angle_errors)) ./ std(angle_errors);

scatter3(trans_errors_norm, rotations_errors_norm, angle_errors_norm, 80, 'filled');

title('Errors Normalised (variance = 1)', 'FontSize', 16 );
xlabel('Translation Errors', 'FontSize', 16 );
ylabel('Rotation Errors', 'FontSize', 16 );
zlabel('Angle Errors', 'FontSize', 16 );

% List of images..
% Getting info for.. IMG_8023
% Getting info for.. IMG_8024
% Getting info for.. IMG_8012
% Getting info for.. IMG_8015
% Getting info for.. IMG_8070
% Getting info for.. IMG_8048
% Getting info for.. IMG_8014
% Getting info for.. IMG_8013
% Getting info for.. IMG_8025
% Getting info for.. IMG_8022
% Getting info for.. IMG_8049
% Getting info for.. IMG_8071
% Getting info for.. IMG_7941
% Getting info for.. IMG_7948
% Getting info for.. IMG_7924
% Getting info for.. IMG_7923
% Getting info for.. IMG_7949
% Getting info for.. IMG_7925
% Getting info for.. IMG_7938
% Getting info for.. IMG_7936
% Getting info for.. IMG_7931
% Getting info for.. IMG_7965
% Getting info for.. IMG_7996
% Getting info for.. IMG_7962
% Getting info for.. IMG_7998
% Getting info for.. IMG_7930
% Getting info for.. IMG_7937
% Getting info for.. IMG_7939
% Getting info for.. IMG_7999
% Getting info for.. IMG_7955
% Getting info for.. IMG_7963
% Getting info for.. IMG_7964
% Getting info for.. IMG_8062
% Getting info for.. IMG_8065
% Getting info for.. IMG_8007
% Getting info for.. IMG_8038
% Getting info for.. IMG_8031
% Getting info for.. IMG_8036
% Getting info for.. IMG_8009
% Getting info for.. IMG_8064
% Getting info for.. IMG_8063
% Getting info for.. IMG_8037
% Getting info for.. IMG_8008
% Getting info for.. IMG_8030
% Getting info for.. IMG_8006
% Getting info for.. IMG_8039
% Getting info for.. IMG_8001
% Getting info for.. IMG_8045
% Getting info for.. IMG_8018
% Getting info for.. IMG_8027
% Getting info for.. IMG_8020
% Getting info for.. IMG_8029
% Getting info for.. IMG_8016
% Getting info for.. IMG_8011
% Getting info for.. IMG_8010
% Getting info for.. IMG_8028
% Getting info for.. IMG_8017
% Getting info for.. IMG_8021
% Getting info for.. IMG_8019
% Getting info for.. IMG_8026
% Getting info for.. IMG_7927
% Getting info for.. IMG_7929
% Getting info for.. IMG_7989
% Getting info for.. IMG_7928
% Getting info for.. IMG_7926
% Getting info for.. IMG_7961
% Getting info for.. IMG_7966
% Getting info for.. IMG_7959
% Getting info for.. IMG_7935
% Getting info for.. IMG_7969
% Getting info for.. IMG_7967
% Getting info for.. IMG_7958
% Getting info for.. IMG_7960
% Getting info for.. IMG_7934
% Getting info for.. IMG_7933
% Getting info for.. IMG_8004
% Getting info for.. IMG_8003
% Getting info for.. IMG_8035
% Getting info for.. IMG_8032
% Getting info for.. IMG_8059
% Getting info for.. IMG_8066
% Getting info for.. IMG_8061
% Getting info for.. IMG_8033
% Getting info for.. IMG_8034
% Getting info for.. IMG_8002
% Getting info for.. IMG_8005
% Getting info for.. IMG_8060
% Getting info for.. IMG_8058
% Getting info for.. IMG_8067
