%Compute RMS error for validation images - GT:
addpath('EstimateDistModel');
addpath('Kinect_Toolbox/toolbox/');
addpath('Funcs');

NCP=Nimsvar;

data = load('data/full_set.mat'); %use masks for validation images
GT = load(res_file);
% load('data/PIval.mat'); %planes in RGB cam ref frame
% close all
allims = [1 2 5 13 18 20 22 27 30 31];
imscalib = [2 13 18 22 27 31];
imsVal = setxor(allims,imscalib);

Rdep2cam=GT.Tdep2camout(1:3,1:3);
tdep2cam=GT.Tdep2camout(1:3,4);
Text = [Rdep2cam [0 0 0]'; -tdep2cam'*Rdep2cam 1];
dK=[GT.INd.fc(1) 0 GT.INd.cc(1);
    0 GT.INd.fc(2) GT.INd.cc(2);
    0 0 1];
sizeim = [480 640];
ind=0;
aux=-1*ones([sizeim length(imsVal)]);
auxD=-1*ones([sizeim length(imsVal)]);
auxGT = auxD;
for i=valIm
    auxC = -1*ones(sizeim);
    auxCD = -1*ones(sizeim);
    auxGT = -1*ones(sizeim);
    ind=ind+1;
    PIval = [-data.final_calib.Rext{i}(:,3); data.final_calib.Rext{i}(:,3)'*data.final_calib.text{i}*1000];
    %     PIval(4,ind) = 1000*PIval(4,ind);
    %Find plane in depth camera Ref frame:
    PIdep(:,ind) = inv(Text)*PIval(:,ind);
    [u v] = find(data.depth_plane_mask{i});
    
    imfile = data.dfiles{i};
    im = (read_disparity(['data/' imfile]));
    %     figure, imagesc(im)
    linid = sub2ind(size(im), u, v);
    real_disp = im(linid);
    dpred_k = DisparityFromPlaneEq_rd(dK,[0 0 0], PIdep(:,ind), GT.INd.dc, [v'; u'],1);
    %    aux(linid)=dpred_k;
    %     figure, imagesc(aux);
    dif{ind} = abs(real_disp'-dpred_k);
    %     aux(linid)=abs(dif{ind});
    %     figure, imagesc(aux);
    RMSerr(ind) = RMS(dif{ind});
    %Undistort:
    load(dist_file);
    D=meanMat;
    correct = lambertw_fast(-a1*D(linid)'.*exp(-a1*dpred_k))/a1;
    idx = find(~isnan(correct));
    dpred=dpred_k;
    dpred(idx) = dpred_k(idx) + correct(idx);
    difF{ind} = abs(real_disp'-dpred);
    RMSerrF(ind) = RMS(difF{ind});
    
    
    auxC(linid)=abs(dif{ind});
    aux(:,:,ind) = auxC;
    figure('Name','Before Distortion Correction'), imagesc(aux(:,:,ind));
    
    auxCD(linid)=abs(difF{ind});
    auxD(:,:,ind) = auxCD;
    figure('Name','After Distortion Correction'), imagesc(auxD(:,:,ind));
    
    
    
    %% Compute with GT
    PIval(4,ind) = 0.001*PIval(4,ind);
    Rdep2cam=data.final_calib.dR;
    tdep2cam=data.final_calib.dt;
    Text = [Rdep2cam [0 0 0]'; -tdep2cam'*Rdep2cam 1];
    PIdep(:,ind) = inv(Text)*PIval(:,ind);
    
    dpred_k = DisparityFromPlaneEq_rd(data.final_calib.dK,data.final_calib.dkc, PIdep(:,ind), data.final_calib.dc, [v'; u'],0);
    dif{ind} = abs(real_disp'-dpred_k);
    a0 = data.final_calib.dc_alpha(1);
    a1 = data.final_calib.dc_alpha(2);
    dpred = dpred_k + lambertw_fast(-a1*data.final_calib.dc_beta(linid)'.*exp(a0-a1*dpred_k))/a1;
    
    difF{ind} = abs(real_disp'-dpred);
    RMSerrGT(ind) = RMS(difF{ind});
    auxGT(linid)=abs(difF{ind});
    figure('Name','Ground Truth'), imagesc(auxGT);
    i
    
    disp('RMS errors');
    str=sprintf('Before Distortion Correction: %f kdu',RMSerr(1));
    disp(str)
    str=sprintf('After Distortion Correction: %f kdu',RMSerrF(1));
    disp(str)
    str=sprintf('Ground Truth (70 plane poses): %f kdu',RMSerrGT(1));
    disp(str)
end
