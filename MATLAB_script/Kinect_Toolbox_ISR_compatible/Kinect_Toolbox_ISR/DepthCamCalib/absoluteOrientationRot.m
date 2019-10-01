%
% function T = absoluteOrientation(P1,P2)
% 
% determines the relative pose between 2 frames from at least 3 pairs of 3D 
% point coordinates relative to both frames (Horn, 87)
%
% INPUT:
%   P1 - 3xN matrix with columns as 3D point coordinates in frame 1
%   P2 - 3xN matrix with columns as 3D point coordinates in frame 2
%
% OUTPUT:
%   T  - Homogeneous rigid transformation from frame 1 to frame 2
%

function R = absoluteOrientationRot(P1,P2)

N_POINTS = size(P1,2);

if N_POINTS < 3
    error('At least 3 points are needed to compute absolute orientation');
elseif N_POINTS ~= size(P2,2)
    error('P1 and P2 must have the same number of columns');
end


% rotation
M = zeros(3,3);
for i = 1:size(P1,2)
    M = M + P2(:,i)*P1(:,i).';
end

N = [M(1,1)+M(2,2)+M(3,3)        M(2,3)-M(3,2)         M(3,1)-M(1,3)         M(1,2)-M(2,1)
            M(2,3)-M(3,2) M(1,1)-M(2,2)-M(3,3)         M(1,2)+M(2,1)         M(3,1)+M(1,3)
            M(3,1)-M(1,3)        M(1,2)+M(2,1) -M(1,1)+M(2,2)-M(3,3)         M(2,3)+M(3,2)
            M(1,2)-M(2,1)        M(3,1)+M(1,3)         M(2,3)+M(3,2) -M(1,1)-M(2,2)+M(3,3)];
[V, e] = eig(N);

q      = V(:,end)/norm(V(:,end));
R     = quat2dcm(q.');
