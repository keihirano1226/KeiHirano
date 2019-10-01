
% Computes calibration error of a transformation T between a RGB Camera and a 
% Depth camera, given two planes
% Error is the euclidean distance between the planes
%
% INPUT
%   T     - 4x4 homogeneous transformation matrix from Camera RGB to Depth
%   PIcam - 4xN matrix with columns as N plane coordinates in camera frame
%   PIdep - 4xN matrix with columns as N plane coordinates in depth camera frame  
%

function e = DepthCamCalibError(T,PIcam,PIdep)

N_PLANES = size(PIcam,2);

TP = [[T(1:3,1:3); -T(1:3,4).'*T(1:3,1:3)] [0;0;0;1]];

e = zeros(1,N_PLANES);
for n=1:N_PLANES
    PIdepP = TP*PIcam(:,n);
    PIdepP = PIdepP(1:3)/PIdepP(4);
    e(n)  = sqrt(sum((PIdepP-PIdep(1:3,n)).^2));
% e(n)  = abs(norm(PIdepP)-norm(PIdep(1:3,n)));
end