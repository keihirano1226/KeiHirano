function dpred = DisparityFromPlaneEq_rd_DIVMOD(dK,qsi, PI, dc, Ppix)

%Uses only radial distortion (k1, k2, k5 from bouguet)
% Compute disparities for a set of image points Ppix, knowing the plane
% equation and the depth cam intrinsic parameters Kd, dc
%Plane equation in mm

x_d = Ppix(2,:);
y_d = Ppix(1,:);
cx_d = dK(1,3);
cy_d = dK(2,3);
fx_d = dK(1,1);
fy_d = dK(2,2);

%Get point direction:
Xk = (y_d-cx_d)/fx_d;
Yk = (x_d-cy_d)/fy_d;

r2 = Xk.^2 + Yk.^2;
Xn = Xk./(1+qsi*r2);
Yn = Yk./(1+qsi*r2);
%Find depths
% S = solve('Xp=(y_d-cx_d)*Zp/fx_d', 'Yp=(x_d-cy_d)*Zp/fy_d', ...
%     'nVec(1)*Xp+nVec(2)*Yp+nVec(3)*Zp+delta=0','Xp','Yp','Zp');

% XX=subs(S.Xp,{'nVec','delta','fx_d','fy_d','cx_d','cy_d','y_d','x_d'},{PI(1:3) PI(4) fx_d fy_d cx_d cy_d y_d x_d});
% YY=subs(S.Yp,{'nVec','delta','fx_d','fy_d','cx_d','cy_d','y_d','x_d'},{PI(1:3) PI(4) fx_d fy_d cx_d cy_d y_d x_d});
% ZZ=subs(S.Zp,{'nVec','delta','fx_d','fy_d','cx_d','cy_d','y_d','x_d'},{PI(1:3) PI(4) fx_d fy_d cx_d cy_d y_d x_d});
nVec = PI(1:3);
delta = PI(4);
ZZ=-delta./(nVec(3) + Xn*nVec(1) + Yn*nVec(2));
 
%Compute disparity
dpred = ((1000./ZZ)-dc(1))/dc(2);