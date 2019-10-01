function [Tdep2camout, INc,INd, Tcamout, residual, projerrCam, distPP, resPlaneSize] = optimizeDepthCam(Tdep2cam,CamCalib, DepCalib, Tcam, pts_disp)
% Tdep2cam - Transformation between depth and color camera
% CamCalib - color camera intrinsic parameters -
% DepCalib - depth camera intrinsic parameters - 5 params
% Tcam - Camera to plane transformations (for N plane poses)
clearvars -global
global indexPointsCam indexPointsDep stdQ stdDist N1 N2 N3 


Nplanes = size(Tcam, 3);

KK = CamCalib{1}.K;
kc = CamCalib{1}.kc;
INd.fc = DepCalib{1}.f;
INd.cc = DepCalib{1}.c;
INd.cc = DepCalib{1}.c;
% INd.c1 = DepCalib{1}.dc(1);
INd.dc = DepCalib{1}.dc;
x0=[KK(1,1) KK(2,2) KK(1:2,3)' KK(1,2)/KK(1,1) kc([1:2 5])' INd.fc INd.cc INd.dc];
% x0=[KK(1,1) KK(2,2) KK(1:2,3)' KK(1,2)/KK(1,1) kc([1:2 5])'];
x0=x0';

% Add Td2c
[Theta w] = R2Euler(Tdep2cam(1:3,1:3));
Alpha = acos(w(3));
Beta = atan2(w(2),w(1));
Td2cvec = [Theta;Alpha;Beta;Tdep2cam(1:3,4)];
x0=[x0;Td2cvec];

for i=1:Nplanes
    [Theta w] = R2Euler(Tcam(1:3,1:3,i));
    Alpha = acos(w(3));
    Beta = atan2(w(2),w(1));
    Td2cvec = [Theta;Alpha;Beta;Tcam(1:3,4,i)];
    x0=[x0;Td2cvec];
end
% for i=1:Nplanes
%     x0=[x0 PIcam(:,i)];
% end

%Create xdata with grid points
xdata=[Nplanes 0 0]';
ydata=[];
for i=1:Nplanes
%     i
    indexPointsCam(i) = size ( CamCalib{i}.X, 2);
    indexPointsDep(i) = size ( DepCalib{i}.X, 2);
    xdata = [xdata CamCalib{i}.X [CamCalib{i}.x; zeros(1,indexPointsCam(i))] DepCalib{i}.X];
    ydata = [ydata 0*CamCalib{i}.x zeros(2, indexPointsDep(i)) ];
    
end
NplanesAll = size(pts_disp,2);
for i=1:NplanesAll
    if isempty(pts_disp{i})
        pts_disp{i}.disp=[];
        pts_disp{i}.ptsPix = [];
        pts_disp{i}.ptsMM=[];
    end
xdata=[xdata [length(pts_disp{i}.disp) 0 0]'];
end
% planesize=[1000 600];
for i=1:NplanesAll
%     i
    xdata = [xdata [pts_disp{i}.ptsPix;pts_disp{i}.disp]];
    ptsMM = pts_disp{i}.ptsMM;
%     ptsMM(ptsMM==1000) = planesize(1);
%     ptsMM(ptsMM==600) = planesize(2);

    xdata = [xdata [ptsMM;zeros(1,length(pts_disp{i}.disp))]];
    ydata = [ydata zeros(2,10)]; %compute 3 distances for each plane (4 points)
    
end 

%% size(ydata)

                                                                       
options = optimset('MaxFunEval',5000,'Display','iter','MaxIter',1000,'TolFun',1E-8,'Algorithm','levenberg-marquardt');
[x resnorm residual dummy info s e] = lsqcurvefit(@FitFunctionDepthCam,x0,xdata,ydata,[],[],options);

INc.fc = x(1:2);
INc.cc = x(3:4);
INc.alpha = x(5);
INc.kc = [x(6:7);0;0;x(8)]; % 5 parameters

%Depth camera intrinsics
INd.fc = x(9:10);
INd.cc = x(11:12);
INd.dc = x(13:14);
offset0 = 14;

Theta = x(1+offset0);
Alpha = x(2+offset0);
Beta = x(3+offset0);
tdep2cam = [x(4+offset0);x(5+offset0);x(6+offset0)];
w = [sin(Alpha)*cos(Beta);sin(Alpha)*sin(Beta);cos(Alpha)];
Rdep2cam = Euler2R(Theta,w);
Tdep2camout = [Rdep2cam tdep2cam; 0 0 0 1];

offset0 = offset0+6;
offset=0;
for i=1:Nplanes

    Theta = x(1+offset0);
    Alpha = x(2+offset0);
    Beta = x(3+offset0);
    t = [x(4+offset0);x(5+offset0);x(6+offset0)];
    w = [sin(Alpha)*cos(Beta);sin(Alpha)*sin(Beta);cos(Alpha)];
    R = Euler2R(Theta,w);
    Tcamout(:,:,i) = [R t; 0 0 0 1];
    offset0 = offset0+6;
    
    projerrCam{i} = ((min(stdQ(i,:)))/N1)*residual(:, offset+1:offset+indexPointsCam(i));
    offset = offset + indexPointsCam(i);
    distPP{i} = (stdDist(i)/N2)*residual(1, offset+1:offset+indexPointsDep(i));
    offset = offset + indexPointsDep(i);
    
    
end
% stdQ
% stdDist


resPlaneSize = residual(1,offset+1:end)/N3;

