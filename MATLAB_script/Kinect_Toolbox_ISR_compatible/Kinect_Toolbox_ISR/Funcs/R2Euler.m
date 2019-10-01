function [theta,w]=R2Euler(R);

ERR=10^-4;
if abs(det(R)-1)<ERR & isempty(find(abs(R*transpose(R)-eye(3,3))>ERR))
 theta=acos((trace(R)-1)/2);
 w=(2*sin(theta))^-1*[R(3,2)-R(2,3);R(1,3)-R(3,1);R(2,1)-R(1,2)];
 w=w*norm(w)^-1;
else
 theta=[];
 w=[];
 fprintf('Error R2Euler: R is not a rotation matrix \n');
end;