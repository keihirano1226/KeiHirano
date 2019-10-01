addpath('Kinect_Toolbox/toolbox');
base2 = 'data/';

% res_file = ['MyTBCalibRes_' num2str(NCP) '.mat'];

File = load(res_file);
fileCP = load(fileCP);
% dataF2 = load(['data/full_set.mat' ]);
Totims = NCP;

idxin=[];
for i=1:Totims
    if ~isempty(fileCP.dfiles{i})
        idxin = [idxin i];
    end
end

%%
% All inlier planes:
indact = 0;
sizeim=[480 640];
j=1;
% fileBou = ['BouFiles/BouCalibRes_' num2str(NCP) '.mat'];
load(fileBou,'active_images', 'image_numbers');
NUMS = find(active_images==1);

for i=idxin
    
    indact = indact+1;
    %Measurements:
    [i1 i2] = find(fileCP.depth_plane_mask{i}==1);
    
    Ppix{indact} = [i2';i1'];
    
    linind = sub2ind(sizeim, i1,i2);
    ima = read_disparity([base2 fileCP.dfiles{i}]);
    disp_measured{indact} = (ima(linind))';
    
    
    %Optimized parameters:
    dK = [File.INd.fc(1) 0 File.INd.cc(1);
        0 File.INd.fc(2) File.INd.cc(2);
        0 0 1];
    dc = File.INd.dc;
    
    %Plane Equations in the depth camera reference frame:
    %     if i==imsFile(j)
    %         T = inv(File.Tdep2camout)*File.Tcamout(:,:,j);
    %         if j<8
    %         j=j+1;
    %         end
    %     else
%         PIcam = [-dataF2.final_calib.Rext{2}(:,3); dataF2.final_calib.Rext{2}(:,3)'*dataF2.final_calib.text{2}*1000];
    PIcam = [-File.Tcamout(1:3,3,i); File.Tcamout(1:3,3,i)'*File.Tcamout(1:3,4,i)];
    Rdep2cam=File.Tdep2camout(1:3,1:3);
    tdep2cam=File.Tdep2camout(1:3,4);
    Text = [Rdep2cam [0 0 0]'; -tdep2cam'*Rdep2cam 1];
    T = inv(Text)*PIcam;
    %     end
    Planes(:,indact) = T;
    dpred{indact} = DisparityFromPlaneEq(dK, Planes(:,indact), dc, Ppix{indact});
    difdisp{indact} = abs(dpred{indact}-disp_measured{indact});
%         [i mean(difdisp{indact})]
end
