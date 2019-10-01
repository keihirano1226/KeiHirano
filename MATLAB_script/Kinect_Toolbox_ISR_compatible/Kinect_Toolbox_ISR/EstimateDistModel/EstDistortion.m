disp('Performing distortion correction...');
% Compute correspondences of disparities dpred - dmeas:
addpath('Kinect_Toolbox/toolbox');
% load('../../Kinect_Toolbox/MyCalibFiles_NewIntFinalv2/idx_best.mat');
NCP=Nimsvar;

% clearvars -except NCP setCP idx_best
CorrespDisparity;
% load('../../Kinect_Toolbox/data/CalibResGT','final_calib');
% Find all pairs of points which appear in more than one image:
sizeim = [480 640];
Nims = indact;
% imsFile = [1 8 11 17 22 27 29 31];
vecims=1:NCP;
allpairs = nchoosek(vecims,2);

bigV=[];bigV2=[];
for pair=1:size(allpairs,1)
%     pair
    ind1 = allpairs(pair,1);
    ind2 = allpairs(pair,2);
    
    [C,IA,IB] = intersect(Ppix{ind1}',Ppix{ind2}','rows');
    
    % im=zeros(sizeim);
    % linearindex = sub2ind(sizeim, C(:,1), C(:,2));
    % im (linearindex) = 1;figure, imagesc(im) %intersection (common points)
    
    %Compute vectors for determining alpha1:
    
    A = disp_measured{ind2}(IB)-disp_measured{ind1}(IA);
    vv=(dpred{ind1}(IA)-disp_measured{ind1}(IA))./(dpred{ind2}(IB)-disp_measured{ind2}(IB));
    A=A(vv>0);
    vv=vv(vv>0);
    B = log (vv);
    % clearvars -except B A
    
    alpha1{pair} = B./A;
    alpha1{pair}=alpha1{pair}(~isnan(alpha1{pair}) & ~isinf(alpha1{pair}));
%     alpha1INT{pair} = round(alpha1{pair}*1000);
%     alpha1pos{pair} = alpha1{pair}(alpha1{pair}>0 & alpha1{pair}~= Inf);
%     alpha1posINT{pair} = round(alpha1pos{pair}*1000);
%     meanalpha1pos(pair) = mean(alpha1pos{pair});
%     bigV = [bigV alpha1posINT{pair}];
    bigV2 = [bigV2 alpha1{pair}];
%     modealpha1pos(pair) = mode(alpha1posINT{pair});
end


%% Estimate D(u,v)*e^alpha0, knowing alpha1:
% close all
NN=length(vecims);
a1 = mean(bigV2);%final_calib.dc_alpha(2);
MatIms = nan([sizeim NN]);
ind=0;
for i=vecims
    vals = (dpred{i}-disp_measured{i})./exp(-a1.*disp_measured{i});
    linearindex = sub2ind(sizeim, Ppix{i}(2,:),Ppix{i}(1,:));
    Mataux = nan(sizeim);
    Mataux(linearindex)=vals;
    ind=ind+1;
    MatIms(:,:,ind)=Mataux;
end

meanMat = nan(sizeim);
for i=1:sizeim(1)
    for j=1:sizeim(2)
        vec(1:NN) =MatIms(i,j,1:NN);
        
        vec = vec(~isnan(vec));% & vec > -22 & vec < 10);
        meanMat(i,j) = mean(vec);
    end
end


% figure, imagesc(meanMat)


%GT:
% MatGT0 = dataF.final_calib.dc_beta*dataF.final_calib.dc_alpha(1);
% figure, imagesc(MatGT0)

% MatGT = final_calib.dc_beta*exp(final_calib.dc_alpha(1));
% figure, imagesc(MatGT)
%
% figure, imagesc(abs(MatGT-meanMat))
% imF = abs(MatGT-meanMat)./abs(MatGT);
% imF(isnan(imF) | imF>1)=-1;
% figure, imagesc(imF)
save(['MyTBCalibDistEst' num2str(NCP) '.mat'],'a1','meanMat');

disp('Done.');