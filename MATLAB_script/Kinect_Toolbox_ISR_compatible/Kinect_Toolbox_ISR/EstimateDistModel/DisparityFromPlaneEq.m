function dpred = DisparityFromPlaneEq(dK, PI, dc, Ppix, b)

% Compute disparities for a set of image points Ppix, knowing the plane
% equation and the depth cam intrinsic parameters Kd, dc
%Plane equation in mm
if nargin<5
    b=1;
end
x_d = Ppix(2,:);
y_d = Ppix(1,:);
cx_d = dK(1,3);
cy_d = dK(2,3);
fx_d = dK(1,1);
fy_d = dK(2,2);

%Find depths
% S = solve('Xp=(y_d-cx_d)*Zp/fx_d', 'Yp=(x_d-cy_d)*Zp/fy_d', ...
%     'nVec(1)*Xp+nVec(2)*Yp+nVec(3)*Zp+delta=0','Xp','Yp','Zp');

% XX=subs(S.Xp,{'nVec','delta','fx_d','fy_d','cx_d','cy_d','y_d','x_d'},{PI(1:3) PI(4) fx_d fy_d cx_d cy_d y_d x_d});
% YY=subs(S.Yp,{'nVec','delta','fx_d','fy_d','cx_d','cy_d','y_d','x_d'},{PI(1:3) PI(4) fx_d fy_d cx_d cy_d y_d x_d});
% ZZ=subs(S.Zp,{'nVec','delta','fx_d','fy_d','cx_d','cy_d','y_d','x_d'},{PI(1:3) PI(4) fx_d fy_d cx_d cy_d y_d x_d});
nVec = PI(1:3);
delta = PI(4);
ZZ=-(delta*fx_d*fy_d)./(fx_d*fy_d*nVec(3) - cy_d*fx_d*nVec(2) - cx_d*fy_d*nVec(1) + fx_d*x_d*nVec(2) + fy_d*y_d*nVec(1));
 
%Compute disparity
if b
dpred = ((1000./ZZ)-dc(1))/dc(2);
else
    dpred = ((1./ZZ)-dc(1))/dc(2);
end