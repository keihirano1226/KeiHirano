function dpred = DisparityFromPlaneEq_rd(dK,kc, PI, dc, Ppix, b)

if nargin < 6
    b=1;
end
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
if length(kc) == 3
    Xn = (1+kc(1)*r2+kc(2)*r2.^2+kc(3)*r2.^3).*Xk;
    Yn = (1+kc(1)*r2+kc(2)*r2.^2+kc(3)*r2.^3).*Yk;
else
    Xg = 2*kc(3)*Xk.*Yk + kc(4)*(r2+2*Xk.^2);
    Yg = kc(3)*(r2+2*Yk.^2)+2*kc(4)*Xk.*Yk;
    
    Xn = (1+kc(1)*r2+kc(2)*r2.^2+kc(5)*r2.^3).*Xk+Xg;
    Yn = (1+kc(1)*r2+kc(2)*r2.^2+kc(5)*r2.^3).*Yk+Yg;
end
%Find depths
% S = solve('Xp=(y_d-cx_d)*Zp/fx_d', 'Yp=(x_d-cy_d)*Zp/fy_d', ...
%     'nVec(1)*Xp+nVec(2)*Yp+nVec(3)*Zp+delta=0','Xp','Yp','Zp');
% 
% XX=subs(S.Xp,{'nVec','delta','fx_d','fy_d','cx_d','cy_d','y_d','x_d'},{PI(1:3) PI(4) fx_d fy_d cx_d cy_d y_d x_d});
% YY=subs(S.Yp,{'nVec','delta','fx_d','fy_d','cx_d','cy_d','y_d','x_d'},{PI(1:3) PI(4) fx_d fy_d cx_d cy_d y_d x_d});
% ZZ=subs(S.Zp,{'nVec','delta','fx_d','fy_d','cx_d','cy_d','y_d','x_d'},{PI(1:3) PI(4) fx_d fy_d cx_d cy_d y_d x_d});
% keyboard
nVec = PI(1:3);
delta = PI(4);
ZZ=-delta./(nVec(3) + Xn*nVec(1) + Yn*nVec(2));

%Compute disparity
if b
    dpred = ((1000./ZZ)-dc(1))/dc(2);
else
    dpred = ((1./ZZ)-dc(1))/dc(2);
end