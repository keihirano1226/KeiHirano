
imD = sprintf('data/%04d-d.pgm',imN-1);
imR = sprintf('data/%04d-c1.jpg',imN-1);
imd = read_disparity(imD);
imR=imread(imR);

if handles.isDC
distFileS = load(distFile);
calib.dc_beta=distFileS.meanMat;
calib.dc_alpha=[0 distFileS.a1];
end

calibFileS=load(calibFile);
dK =[calibFileS.INd.fc(1) 0 calibFileS.INd.cc(1)
    0 calibFileS.INd.fc(2) calibFileS.INd.cc(2)
    0 0 1];
dc=calibFileS.INd.dc;
% GT=load('data/full_set.mat');
% dK = GT.final_calib.dK;
% dc = GT.final_calib.dc;

%compute 3D pts:
[us vs] = size(imd);
[u v] = meshgrid(1:vs, 1:us);
disp_k=imd(:)';
if handles.isDC
disp_k=undistort_disparity(u(:)'-1,v(:)'-1, disp_k,calib);
end
P3D = Point3Dfromdisp (dK, dc, [v(:)'; u(:)'], disp_k,1);
% figure, scatter3(P3D(1,1:100:end),P3D(2,1:100:end),P3D(3,1:100:end));
%Assign colors:
%Project points to color camera ref frame & backproject:
% T = [GT.final_calib.dR GT.final_calib.dt*1000; 0 0 0 1];
% fc = [GT.final_calib.rK{1}(1,1) GT.final_calib.rK{1}(2,2)];
% cc = [GT.final_calib.rK{1}(1,3) GT.final_calib.rK{1}(2,3)];
% kc = GT.final_calib.rkc{1};
% alpha=0;
xout=ProjectPoints(P3D,calibFileS.Tdep2camout,calibFileS.INc.fc,calibFileS.INc.cc,calibFileS.INc.kc,calibFileS.INc.alpha);
% xout=ProjectPoints(P3D,T,fc,cc,kc,alpha);

%get colors:
imRR = imR(:,:,1);
imRG = imR(:,:,2);
imRB = imR(:,:,3);
xout=round(xout);
idx1 = find(xout(1,:) > 0 & xout(1,:) <=size(imRR,2));
idx2 = find(xout(2,:) > 0 & xout(2,:) <=size(imRR,1));
idx = intersect(idx1, idx2);
xout=xout(:,idx);
P3D=P3D(:,idx);

ind = sub2ind(size(imRR),xout(2,:),xout(1,:));
rr = imRR(ind);
gg = imRG(ind);
bb = imRB(ind);
step = 1;
Data.vertex.x=P3D(1,1:step:end);
Data.vertex.y=P3D(2,1:step:end);
Data.vertex.z=P3D(3,1:step:end);
Data.vertex.diffuse_red=uint8(rr(1:step:end));
Data.vertex.diffuse_green=uint8(gg(1:step:end));
Data.vertex.diffuse_blue=uint8(bb(1:step:end));

file = ['Out' num2str(handles.isDC) '.ply'];
plywrite(Data,file,'ascii');