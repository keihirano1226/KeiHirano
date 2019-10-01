clearvars -global
load(loadF,'active_images', 'image_numbers');
N=sum(active_images);
NUMS = find(active_images==1);
load(fileCP,'dfiles','depth_plane_mask');
GT=load('data/full_set.mat','final_calib');
for i=1:N
    imfilec{i} = ['data/' dfiles{i}];
end
INims=depth_plane_mask;

% close all
for kk=1:N
    kk
    imfile=imfilec{kk};
    %         i1=imread(imfile);
    %         imshow(i1);
    %         %get corners of the plane:
    %
    %         [X,Y] = ginput;
    %
    %         [ptsX,ptsY] = meshgrid(1:size(i1,2),1:size(i1,1));
    %         IN = inpolygon(ptsX,ptsY,X,Y);
    %         INims{kk} = IN;
    
    IN = INims{kk};
    %         figure, imshow(IN)
    %     keyboard
    
    %Read for correcting disparity values
    i1 = (read_disparity(imfile));
    
    
    [xones yones] = find(IN);
    %% Sample Npts
    Npts=round(length(xones)/100);
    vec = linspace (1,length(xones), Npts);
    vec=floor(vec);
    x_d=xones(vec);
    y_d=yones(vec);
    clear xones yones
    linearindex = sub2ind(size(i1), x_d, y_d);
    iplane = i1(linearindex);
    %Remove NaN values:
    x_d = x_d(~isnan(iplane));
    y_d = y_d(~isnan(iplane));
    iplane = iplane(~isnan(iplane));
    Npts=length(iplane);
    %Known intrinsics for the depth camera
    dK = [  594 0  339;
        0  591 243;
        0  0    1];
    cx_d = dK(1,3);
    cy_d = dK(2,3);
    fx_d = dK(1,1);
    fy_d = dK(2,2);
    dc=[3.3309495161 -0.0030711016];
    
    % Get depths:
    
    depth = (1.0./(dc(2)*iplane+dc(1)))*1000; %(mm)
    
    P3D{kk}.x = (y_d - cx_d) .* depth / fx_d;
    P3D{kk}.y = (x_d - cy_d) .* depth / fy_d;
    P3D{kk}.z = depth;
    
    
    
    p_pick = [P3D{kk}.x'; P3D{kk}.y'; P3D{kk}.z'];
    plane{kk}=fitplane(p_pick);
    
    %Variable for optimization
    DepCalib{kk}.X = [x_d';y_d';iplane'];
    DepCalib{kk}.depths = depth;
    
    DepCalib{kk}.DistPP = DistancePointPlane(plane{kk}, p_pick);
end

%% Camera planes:

load(loadF);
if image_numbers(1)==0
    image_numbers=image_numbers+1;
end
n_active = active_images.*image_numbers;
if active_images(1) == 1 && image_numbers(1) == 0
    n_active = n_active(2:end);
    n_active=n_active(n_active ~=0);
    n_active(end+1)=0;
    n_active=sort(n_active);
else
    n_active=n_active(n_active ~=0);
end
N=sum(active_images);
ind=0;
for i=n_active
    ind=ind+1;
    eval(['pi{ind}=[Rc_' num2str(i) ' Tc_' num2str(i) '; 0 0 0 1];']);
end


%%
for i=1:N
    
    PIcam(:,i) = [-pi{i}(1:3,3);pi{i}(1:3,3)'*pi{i}(1:3,4)];
end

for i=1:N
    PIcam(:,i) = PIcam(:,i) * sign (PIcam(4,i)); % for convention
    PIcam(:,i) = PIcam(:,i) / norm(PIcam(1:3,i)); % normal vector norm = 1
end
PIcam = PIcam ./ (ones(4,1)*PIcam(4,:));

% figure,
% subplot(1,3,1);subimage(imread(imfilec{1}))
% subplot(1,3,2);subimage(imread(imfilec{2}))
% subplot(1,3,3);subimage(imread(imfilec{3}))

%% Depth camera planes:

for i=1:N
    PIdep(:,i) = plane{i};
    PIdep(:,i) = PIdep(:,i) * sign (PIdep(4,i)); % for convention
    PIdep(:,i) = PIdep(:,i) / norm(PIdep(1:3,i)); % normal vector norm = 1
end

PIdep = PIdep ./ (ones(4,1)*PIdep(4,:));

%%
rt=0.0001;
Nin = 0;
while Nin < 3
    
    [best_T, best_inliers, best_sample, min_cost] = DepthCamMSACCalib(PIcam,PIdep,rt);
    Nin = length(best_inliers);
    rt = rt+10^-5;
end
% min_cost
% best_T
% best_inliers

% Optimization:

ind=0;
for i=n_active
    ind=ind+1;
    eval(['CamCalib{ind}.X = X_' num2str(i) ';']);
    eval(['CamCalib{ind}.x = x_' num2str(i) ';']);
    DepCalib{ind}.PI = PIdep(:,ind);
end
for i=1:length(n_active)
    %     DepCalib{i}.f=INdout.fc';
    %     DepCalib{i}.c=INdout.cc';
    %     DepCalib{i}.dc=INdout.dc';
    
    DepCalib{i}.f=[fx_d fy_d];
    DepCalib{i}.c=[cx_d cy_d];
    DepCalib{i}.dc=dc;
    DepCalib{i}.kc = [0 0 0]; %radial distortion
    DepCalib{i}.qsi = 0; %radial distortion
    CamCalib{i}.K = KK;
    CamCalib{i}.kc = kc;
    
    CamCalib{i}.ProjErr = ProjectPoints(CamCalib{i}.X,pi{i},[KK(1,1) KK(2,2)],KK(1:2,3),kc,KK(1,2)/KK(1,1))-CamCalib{i}.x;
end
for i=1:N
    %     Tcam(:,:, i)=Tcamout(:,:,i);
    Tcam(:,:, i)=pi{i};
end

Tdep2cam=inv(best_T);


% plane_size =  [1000 600];

%%
CamCalibin = CamCalib(best_inliers);
DepCalibin = DepCalib(best_inliers);
Tcamin = Tcam(:,:,best_inliers);

%% NO RD
load(planeinfo);
% keyboard
[Tdep2camout, INc,INd, Tcamout, residual,projerrCam, distPP, resPlaneSize] = optimizeDepthCam(Tdep2cam,CamCalibin, DepCalibin, Tcamin, PlaneCornersInfo(NUMS(best_inliers)));

disp ('Initial estimation')
[nd1 td1]= CompareTs(([GT.final_calib.dR GT.final_calib.dt*1000; 0 0 0 1]), Tdep2cam);
str = sprintf('Rotation error (degrees): %f', td1);
disp (str)
str = sprintf('Translation error (mm): %f', nd1);
disp (str)
Tdep2camout
disp(' ');
disp ('Result after optimization')
[nd1 td1]= CompareTs(([GT.final_calib.dR GT.final_calib.dt*1000; 0 0 0 1]), Tdep2camout);
str = sprintf('Rotation error (degrees): %f', td1);
disp (str)
str = sprintf('Translation error (mm): %f', nd1);
disp (str)
str = sprintf('Error in c0 and c1 (%%): %f;%f',abs((INd.dc(1)'-GT.final_calib.dc(1))./GT.final_calib.dc(1))*100 ,abs((INd.dc(2)'-GT.final_calib.dc(2))./GT.final_calib.dc(2))*100);
disp (str)

