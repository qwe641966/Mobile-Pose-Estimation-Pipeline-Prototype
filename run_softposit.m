function [] = run_softposit(query_image_name)
	
    points2D = load(strcat('results/',query_image_name,'/points2D_for_softposit.mat'));
    points2D = points2D.value;
    points3D = load(strcat('results/',query_image_name,'/points3D_for_softposit.mat'));
    points3D = points3D.value;
    points3D = points3D(:,2:4);
    
    cameraParams = load(strcat('results/',query_image_name,'/camera_intrinsics.mat'));
    focalLength = cameraParams.value(1,1);
    center = [cameraParams.value(1,2) cameraParams.value(1,3)]; % check order ?
    
    colmap_rot = load(strcat('results/',query_image_name,'/colmap_rot.mat'));
    colmap_rot = [str2double(colmap_rot.value(1,:)) ; str2double(colmap_rot.value(2,:)) ; str2double(colmap_rot.value(3,:)) ; str2double(colmap_rot.value(4,:))]';
    colmap_rot = quat2rotm(colmap_rot);
    colmap_trans = load(strcat('results/',query_image_name,'/colmap_trans.mat'));
    colmap_trans = colmap_trans.value;
    
    [r, c] = size(points2D);
    imageAdj = zeros(r); % r by r
    [r, c] = size(points3D);
    worldAdj = zeros(r); % r by r
    dispLevel = 0;
    kickout.numMatchable = 3000;
    kickout.rthldfbeta = zeros(1,2000);
    
    [SOFTPosit_rot, SOFTPosit_trans, assignMat, projWorldPts, foundPose, stats] = ...
        softPosit(points2D, imageAdj, points3D, worldAdj, 0.0001, 1, ...
                     colmap_rot, colmap_trans, focalLength, dispLevel, kickout, center);

    quit
end

% [SOFTPosit_rot, SOFTPosit_trans, assignMat, projWorldPts, foundPose, stats] = ...
%     softPosit(point2DSOFTPosit, imageAdj, point3DSOFTPosit, worldAdj, 2.0e-04, 0, ...
%                  colmap_rot, colmap_trans, focalLength, dispLevel, kickout, center);