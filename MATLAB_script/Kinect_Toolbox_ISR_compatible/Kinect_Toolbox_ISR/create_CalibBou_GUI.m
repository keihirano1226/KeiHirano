%Use bouguet to create the calibration files for each grid pose set
%see create_CPfile.m

addpath('bouguet/toolbox_calib');

load('data/Calib_Results.mat','active_images');

Ntot = length(active_images);
imidx = imNums;
mkdir('BouFiles');
for N=Nimsvar
    
    
    hip0 = imidx;
    load('data/Calib_Results.mat');
    est_dist = [1 1 1 1 0]';
    active_images = zeros(1,Ntot);
    active_images ( hip0)=1;
    go_calib_optim;
    save_name = ['BouFiles/BouCalibRes_' num2str(N) 'C'];
    CAROLINA_saving_calib;
    
end
