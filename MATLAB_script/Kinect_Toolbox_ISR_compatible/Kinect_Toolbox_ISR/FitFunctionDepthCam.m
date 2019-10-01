function F=FitFunctionDepthCam(x0,xdata)

global indexPointsCam indexPointsDep stdQ stdDist N1 N2 N3
% idxCam=cumsum(indexPointsCam);
% idxDep=cumsum(indexPointsDep);

%Read x0:

%Color camera intrinsics:
INc.fc = x0(1:2);
INc.cc = x0(3:4);
INc.alpha = x0(5);
INc.kc = [x0(6:7);0;0;x0(8)]; % 5 parameters

%Depth camera intrinsics
INd.fc = x0(9:10);
INd.cc = x0(11:12);

INd.dc = x0(13:14);

Nplanes = xdata(1,1);

offsetini=1;
offset=offsetini;
offset0 = 14;

Theta = x0(1+offset0);
Alpha = x0(2+offset0);
Beta = x0(3+offset0);
tdep2cam = [x0(4+offset0);x0(5+offset0);x0(6+offset0)];
w = [sin(Alpha)*cos(Beta);sin(Alpha)*sin(Beta);cos(Alpha)];
Rdep2cam = Euler2R(Theta,w);
Tdep2cam = [Rdep2cam tdep2cam; 0 0 0 1];

offset0 = offset0+6;

for i=1:Nplanes
    
    Theta = x0(1+offset0);
    Alpha = x0(2+offset0);
    Beta = x0(3+offset0);
    t = [x0(4+offset0);x0(5+offset0);x0(6+offset0)];
    w = [sin(Alpha)*cos(Beta);sin(Alpha)*sin(Beta);cos(Alpha)];
    R = Euler2R(Theta,w);
    Tcam(:,:,i) = [R t; 0 0 0 1];
    
    offset0=offset0+6;
    Xcam{i} = xdata(:,offset+1:offset+indexPointsCam(i));
    offset=offset+indexPointsCam(i);
    
    xcam{i} = xdata(1:2,offset+1:offset+indexPointsCam(i));
    offset=offset+indexPointsCam(i);
    
    Xdep{i} = xdata(:,offset+1:offset+indexPointsDep(i));
    offset=offset+indexPointsDep(i);
end

NpointsPlane = xdata(1,offset+1:offset+Nplanes);
offset=offset+Nplanes;
% planesize = xdata(1:2,offset+1);
% offset=offset+1;


% Compute 3D points of depth camera:
dK = [INd.fc(1) 0 INd.cc(1);
    0 INd.fc(2) INd.cc(2);
    0 0 1];
for i=1:Nplanes
    iplane = Xdep{i}(3,:);
    x_d = Xdep{i}(1,:);
    y_d = Xdep{i}(2,:);
    depth = (1.0./(INd.dc(2)*iplane+INd.dc(1)))*1000; %(mm)
    
    P3D2{i}(1,:) = (y_d - INd.cc(1)) .* depth / INd.fc(1);
    P3D2{i}(2,:) = (x_d - INd.cc(2)) .* depth / INd.fc(2);
    P3D2{i}(3,:) = depth;
    
    
    %     P3D2{i}(4,:) = ones (1,indexPointsDep(i));
end
% N1 = 100;
% N2=0.01;
% N3=0.1;
N1 = 20;
N2=2;
N3=1;

F=[];
% G=[];
Tk = [Rdep2cam [0 0 0]'; -tdep2cam'*Rdep2cam 1];
for i=1:Nplanes
    q=ProjectPoints(Xcam{i},Tcam(:,:,i),INc.fc,INc.cc,INc.kc,INc.alpha);
    qdif=q-xcam{i};
    PIcam(:,i) = [-Tcam(1:3,3,i);Tcam(1:3,3,i)'*Tcam(1:3,4,i)];
    %     PIcam(:,i) = PIcam(:,i) * sign (PIcam(4,i)); % for convention
    %     PIcam(:,i) = PIcam(:,i) / norm(PIcam(1:3,i)); % normal vector norm = 1
    %     PIcam(:,i) = PIcam(:,i) / PIcam(4,i);
    %     Xw = (Tcam(:,:,i))*[Xcam{i};ones(1,indexPointsCam(i))];
    %     prodPIQcam = [PIcam(:,i)'* Xw] ;
    PIdep(:,i) = inv(Tk)*PIcam(:,i);
    dpred = DisparityFromPlaneEq(dK, PIdep(:,i), INd.dc, [Xdep{i}(2,:);Xdep{i}(1,:)]);
    %     PIdep(:,i)=PIdep(:,i)/PIdep(4,i);
    %     prodPIQ = [PIdep(:,i)'* P3D2{i}] ;
    %     prodPIQ = DistancePointPlane(PIdep(:,i), P3D2{i});
    prodPIQ = dpred - Xdep{i}(3,:);
    stdDist(i) = 0.9;
    %     vv = sqrt(sum(qdif.^2,1));
    stdQ(i,:) = 0.2;
    
    F=[F (N1/(min(stdQ(i,:))))*qdif (N2/(stdDist(i)))*[prodPIQ;zeros(1,indexPointsDep(i))]];
    % G = [G prodPIQ];
    
end

for i=1:Nplanes
    
    
    pts = (xdata(:,offset+1:offset+NpointsPlane(i)));
    
    offset=offset+NpointsPlane(i);
    ptsMM = (xdata(1:2,offset+1:offset+NpointsPlane(i)));
    offset=offset+NpointsPlane(i);
    
    if NpointsPlane(i) == 4 %maximum number
        H{1}=homography_from_corners(pts(1:2,:),ptsMM);
        
        [RR{1},tt{1}] = extern_from_homography(dK,H{1});
        PI=[-RR{1}(:,3); RR{1}(:,3)'*tt{1}];
        
        
        difpred = DisparityFromPlaneEq(dK, PI, INd.dc, pts(1:2,:))-pts(3,:);
    else
        difpred = zeros(1,4);
    end
    if ~isempty(pts)
        P3D = Point3Dfromdisp (dK, INd.dc, pts(1:2,:), pts(3,:));
        if NpointsPlane(i) == 4
            a=sqrt (sum((P3D(:,1)-P3D(:,2)).^2)) - norm(ptsMM(:,1)-ptsMM(:,2)); %1200
            b=sqrt (sum((P3D(:,1)-P3D(:,4)).^2)) - norm(ptsMM(:,1)-ptsMM(:,4)); %750
            c=sqrt (sum((P3D(:,2)-P3D(:,3)).^2)) - norm(ptsMM(:,2)-ptsMM(:,3));
            d=sqrt (sum((P3D(:,3)-P3D(:,4)).^2)) - norm(ptsMM(:,3)-ptsMM(:,4));
            
            v1 = (P3D(:,1)-P3D(:,2));
            v2 = (P3D(:,1)-P3D(:,4));
            v1=v1/norm(v1);
            v2=v2/norm(v2);
            v3 = (P3D(:,3)-P3D(:,2));
            v4 = (P3D(:,3)-P3D(:,4));
            v3=v3/norm(v3);
            v4=v4/norm(v4);
            ang1=rad2deg(dot(v1,v2));
            ang2=rad2deg(dot(v3,v4));
        elseif NpointsPlane(i) == 2
            a = sqrt (sum((P3D(:,1)-P3D(:,2)).^2)) - norm(ptsMM(:,1)-ptsMM(:,2));
            b=0; c=0; d=0; ang1=0; ang2=0;
        else
            v1 = (ptsMM(:,1)-ptsMM(:,2));
            v2 = (ptsMM(:,1)-ptsMM(:,3));
            v1=v1/norm(v1);
            v2=v2/norm(v2);
            if dot(v1,v2) == 0
                ptcent = 1;
            end
            
            v1 = (ptsMM(:,2)-ptsMM(:,1));
            v2 = (ptsMM(:,2)-ptsMM(:,3));
            v1=v1/norm(v1);
            v2=v2/norm(v2);
            if dot(v1,v2) == 0
                ptcent = 2;
            end
            
            
            v1 = (ptsMM(:,3)-ptsMM(:,1));
            v2 = (ptsMM(:,3)-ptsMM(:,2));
            v1=v1/norm(v1);
            v2=v2/norm(v2);
            if dot(v1,v2) == 0
                ptcent = 3;
            end
            vv = setxor(1:3,ptcent);
            a = sqrt (sum((P3D(:,ptcent)-P3D(:,vv(1))).^2)) - norm(ptsMM(:,ptcent)-ptsMM(:,vv(1)));
            b = sqrt (sum((P3D(:,ptcent)-P3D(:,vv(2))).^2)) - norm(ptsMM(:,ptcent)-ptsMM(:,vv(2)));
            v1 = (P3D(:,ptcent)-P3D(:,vv(1)));
            v2 = (P3D(:,ptcent)-P3D(:,vv(2)));
            v1=v1/norm(v1);
            v2=v2/norm(v2);
            ang1 =rad2deg(dot(v1,v2));
            c=0; d=0; ang2=0;
        end
    else
        a = 0; b=0; c=0; d=0; ang1=0; ang2=0;
    end
    F=[F [N3*[difpred a b c d ang1 ang2]; zeros(1,10)] ];
%     keyboard
    
    
end
% stdQ
% size(F)
