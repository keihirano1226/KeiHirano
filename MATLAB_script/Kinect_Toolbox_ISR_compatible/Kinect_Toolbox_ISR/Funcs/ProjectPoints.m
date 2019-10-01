%  
% function xout=ProjectPoints(X,T,fc,cc,kc,alpha)


function xout=ProjectPoints(X,T,fc,cc,kc,alpha)
% kc(5)=0;
n=size(X,2);
arrayONES=ones(1,n);
X=T*[X;arrayONES];
x=X(1,:)./X(3,:);
y=X(2,:)./X(3,:);
xn=[x;y];
r2=x.^2+y.^2;
r4=r2.^2;
r6=r2.^3;
dx=[2.*kc(3).*x.*y+kc(4).*(r2+2.*x.^2);kc(3).*(r2+2.*y.^2)+2.*kc(4).*x.*y];


xd=[1;1]*(arrayONES+kc(1).*r2+kc(2).*r4+kc(5).*r6).*xn+dx;
xout=[fc(1) alpha*fc(1) cc(1);0 fc(2) cc(2) ]*[xd;arrayONES];