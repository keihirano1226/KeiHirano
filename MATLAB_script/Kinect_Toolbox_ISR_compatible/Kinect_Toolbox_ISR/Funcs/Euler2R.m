function R=Euler2R(theta,w);

ERR=10^-7;
if abs(norm(w)-1)<ERR
 R=cos(theta)*eye(3,3)+sin(theta)*skew_symetric_v(w)+(1-cos(theta))*w*transpose(w);
else
 R=[];
 fprintf('Error Euler2R: in Vector Norm \n');
end;
