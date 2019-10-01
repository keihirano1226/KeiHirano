function d = DistancePointPlane(Plane, Point)

%Determines the geometric distance of a set of points to a plane
% Plane: 4D- vector [A B C D]' -> Ax+By+Cz+D=0
A=Plane(1);
B=Plane(2);
C=Plane(3);
D=Plane(4);

N = norm(Plane(1:3));

d = abs(A*Point(1,:)+B*Point(2,:)+C*Point(3,:)+D*ones(1,size(Point,2)))./N;