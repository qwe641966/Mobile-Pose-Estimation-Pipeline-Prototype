%view concecutive frame data
close all;

% first frame!

%load 3D points of frame
points3D = importdata('/Users/alex/Projects/EngDLocalProjects/Lego/fullpipeline/colmap_data/data/query_data/cpuImageCorrespondences_1579029504279.txt');
points3D = points3D(:,3:5);

%load camera pose of frame
% pose  = importdata('/Users/alex/Projects/EngDLocalProjects/Lego/fullpipeline/colmap_data/data/query_data/cameraPose_1579029504279.txt');
% rotm = pose(1:3,1:3);
% tvec = pose(1:3,4);
% camera_location = -inv(rotm) * tvec;
    
%plot them
figure
pcshow(points3D, 'MarkerSize', 200);
hold on
% plot3(0,0,0,'g*');
% hold on
% plot3(points3D(:,1), points3D(:,2), points3D(:,3),'b*');
% hold on

% plotCamera('Location', camera_location, 'Orientation', rotm, 'Size', 0.15, 'Color', [1, 0, 0]);

xlabel('X');
ylabel('Y');
zlabel('Z');
hold on
