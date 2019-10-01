function P3D = Point3Dfromdisp (dK, dc, Ppix, disp,b) %in mm
if nargin < 5
    b=1;
end
x_d = Ppix(1,:);
y_d = Ppix(2,:);

cx_d = dK(1,3);
cy_d = dK(2,3);
fx_d = dK(1,1);
fy_d = dK(2,2);
if b==1
depth = (1.0./(dc(2)*disp+dc(1)))*1000;
else
    depth = (1.0./(dc(2)*disp+dc(1)));
end
P3D(1,:) = (y_d - cx_d) .* depth / fx_d;
P3D(2,:) = (x_d - cy_d) .* depth / fy_d;
P3D(3,:) = depth;
