% Minimal algorithm for registration of 3 planes and 3 planes viewed by 2
% cameras
%
% INPUT:
%   PIcam - 4x3 matrix with columns defining each plane
%   L     - 6x3 matrix with co-planar lines in plucker coordinates
%           NOTE: the lines MUST lie in the plane z=10 for this function to
%           work properly. If this is not the case, no errors are
%           displayed, but the output will be wrong
%   disp  - debug flag
%
% OUTPUT:
%   T - 4x4 matrix with the transformation from the planes reference frame
%       to the lines reference frame
%

function T = DepthCam3PlaneCalibNewRegist2(PIcam, PIcam2)
% PIcam and PIcam2 as (n 1)'

%thresh - value for considering that values are equal
if ~exist('disp','var')
    disp=0;
end
% PIcam, PIcam2 in homogeneous coordinates

% ROTATION 1st
P1 = PIcam(1:3,:);
P2 = PIcam2(1:3,:);

for i=1:3
    P1N(:,i) = P1(:,i)/norm(P1(:,i));
    P2N(:,i) = P2(:,i)/norm(P2(:,i));
end

d12 = norm(P1N(:,1)-P1N(:,2));
d13 = norm(P1N(:,1)-P1N(:,3));
d23 = norm(P1N(:,2)-P1N(:,3));


arrang(:,:,1) = [P2N(:,1) P2N(:,2) P2N(:,3)];
arrang(:,:,2) = [P2N(:,1) P2N(:,2) -P2N(:,3)];
arrang(:,:,3) = [P2N(:,1) -P2N(:,2) P2N(:,3)];
arrang(:,:,4) = [P2N(:,1) -P2N(:,2) -P2N(:,3)];
arrang(:,:,5) = [-P2N(:,1) P2N(:,2) P2N(:,3)];
arrang(:,:,6) = [-P2N(:,1) P2N(:,2) -P2N(:,3)];
arrang(:,:,7) = [-P2N(:,1) -P2N(:,2) P2N(:,3)];
arrang(:,:,8) = [-P2N(:,1) -P2N(:,2) -P2N(:,3)];

% Find d12 and d23 for the 8 possibilities and subtract by the "real"
% distances

for i=1:8
    dist12(i) = abs(norm(arrang(:,1,i)-arrang(:,2,i)) - d12);
    dist23(i) = abs(norm(arrang(:,2,i)-arrang(:,3,i)) - d23);
    dist13(i) = abs(norm(arrang(:,1,i)-arrang(:,3,i)) - d13);
end

%Pick 2 measures with largest ratio between the 2 distances in
%distab:

Vaux = unique(dist12);
rat(1) = max(Vaux)/min(Vaux);
Vaux = unique(dist23);
rat(2) = max(Vaux)/min(Vaux);
Vaux = unique(dist13);
rat(3) = max(Vaux)/min(Vaux);

[a b] = sort(rat,'descend');
switch b(1)
    case 1
        distF = dist12;
    case 2
        distF = dist23;
    case 3
        distF = dist13;
end
switch b(2)
    case 1
        distS = dist12;
    case 2
        distS = dist23;
    case 3
        distS = dist13;
end

dist12 = distF;
dist23 = distS;

m12 = min(dist12);
m23 = min(dist23);

%4 solutions:
idx12 = find(dist12 == m12);
idx23 = find(dist23 == m23);
ind=0;
for i=1:length(idx12)
    a=find(idx12 == idx23(i));
    if ~isempty(a)
        ind=ind+1;
        idxE(ind) = a;
    end
end

for i=1:length(idxE)
    sol(:,:,i) = arrang(:,:,idx12(idxE(i)));
    
end

% Test to choose correct solution: relative orientation between vectors in
% a piramid

vec_ref = cross(P1N(:,2)-P1N(:,1), P1N(:,3)-P1N(:,1));
ang_ref = dot(vec_ref,P1N(:,1));
ind = 0;
for i=1:size(sol,3)
    vec = cross(sol(:,2,i)-sol(:,1,i), sol(:,3,i)-sol(:,1,i));
    ang(i) = dot(vec,sol(:,1,i));
    if sign(ang(i)) == sign(ang_ref) || abs(ang(i)-ang_ref) < 1e-10
        ind=ind+1;
        solR(:,:,ind)=sol(:,:,i);
    end
end

for i=1:ind
    Rot(:,:,i)=absoluteOrientationRot(P1N,solR(:,:,i));
   
    % Determine translation for each solution:
    Aaux = [P2(:,1)'*P2(:,1)*P1(:,1)'
        P2(:,2)'*P2(:,2)*P1(:,2)'
        P2(:,3)'*P2(:,3)*P1(:,3)'];
    
    A=Aaux * Rot(:,:,i)';
    b = [P2(:,1)'*P2(:,1)-P2(:,1)'*Rot(:,:,i)*P1(:,1)
        P2(:,2)'*P2(:,2)-P2(:,2)'*Rot(:,:,i)*P1(:,2)
        P2(:,3)'*P2(:,3)-P2(:,3)'*Rot(:,:,i)*P1(:,3)];
    
    tout(:,1) = (A) \ b;
    T = [Rot(:,:,i) tout(:,1); 0 0 0 1];
    
end