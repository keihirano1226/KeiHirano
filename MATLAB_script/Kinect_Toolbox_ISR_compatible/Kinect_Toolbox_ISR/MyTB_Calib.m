rmpath('bouguet/toolbox_calib');
addpath('Kinect_Toolbox/toolbox');
addpath('Funcs');
addpath('DepthCamCalib');
addpath('EstimateDistModel');
% clc
% clear

for NCP=Nimsvar
        
%         clearvars -except NCP loadF fileCP hObject
        
%         loadF = ['BouFiles/BouCalibRes_' num2str(NCP) '.mat'];
%         fileCP=['CPfiles/CP_' num2str(NCP) '.mat'];
        ti=tic;
        main_runCalibKin;
        telapsed = toc(ti);
        %NOTE: CalibFiles_NewReg - results for the new registration 
        save_file = ['MyTBCalibRes_' num2str(NCP) '.mat'];
        save(save_file,'Tdep2camout', 'INc','INd', 'Tcamout','projerrCam', 'distPP', 'resPlaneSize',...
            'Tdep2cam','CamCalib', 'DepCalib', 'Tcam','best_inliers','telapsed');
        
end