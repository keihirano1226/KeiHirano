addpath('/host/Users/Carolina/Desktop/BIC/Develop/LaserCamCalib/');
addpath('/host/Users/Carolina/Desktop/BIC/Develop/Mirror/Bin/BinMisc/');
clear
clearvars -global
clc
Npose = 15;
load ../CP_files_Final/sets.mat

%max_depth_sample_count: The maximum number of disparity samples used for
%   full calibration. Used to limit memory usage.

global max_depth_sample_count
max_depth_sample_count = 60000;
use_kc = false;
load '../../Kinect_Toolbox/MyCalibFiles_NewIntFinalv2/idx_best.mat'
for N=15
    N
    hip = hipout{N-2};
    
    Nhip = size(hip,1);
    for i=218%idx_best{N-2}
        %% NO NOISE
        clearvars -except path N Nhip hip use_kc  i hipout idx_best
        clearvars -global -except max_depth_sample_count
        
        path=['../CP_files_Final/CP_' num2str(N) '_set' num2str(i) '.mat'];
        
        do_load_calib(path);
        
        
        do_initial_rgb_calib();
        ti = tic;
        sigma=0;
        sigmaR=0;
        
        do_initial_depth_calib_NewInt(true,sigma,sigmaR);
        
        %FAZER TESTES COM E SEM KC:
        do_calib(use_kc,false); %do not use kc or depth distortion
        telapsed = toc(ti);
        
        if use_kc
            strkc = '1';
        else
            strkc='0';
        end
        path_save =['../CalibFiles_NewIntFinalv2/CalibRes_' num2str(N) '_set' num2str(i) '_kc' strkc '.mat'];
        do_save_calib(path_save);
        save(path_save, 'telapsed','-append');
        
        %% NOISE UNIF
        clearvars -except path N Nhip hip use_kc  i hipout idx_best
        clearvars -global -except max_depth_sample_count
        
        path=['../CP_files_Final/CP_' num2str(N) '_set' num2str(i) '.mat'];
        
        do_load_calib(path);
        
        
        do_initial_rgb_calib();
        ti = tic;
        sigma=0.1;
        sigmaR=deg2rad(1);
        
  do_initial_depth_calib_NewInt(true,sigma,sigmaR);
        
        %FAZER TESTES COM E SEM KC:
        do_calib(use_kc,false); %do not use kc or depth distortion
        telapsed = toc(ti);
        
        if use_kc
            strkc = '1';
        else
            strkc='0';
        end
        path_save =['../CalibFiles_NewIntFinalv2/CalibResNU1_' num2str(N) '_set' num2str(i) '_kc' strkc '.mat'];
        do_save_calib(path_save);
        save(path_save, 'telapsed','-append');
        
        %% NOISE 2
        clearvars -except path N Nhip hip use_kc  i hipout idx_best
        clearvars -global -except max_depth_sample_count
        
        path=['../CP_files_Final/CP_' num2str(N) '_set' num2str(i) '.mat'];
        
        do_load_calib(path);
        
        
        do_initial_rgb_calib();
        ti = tic;
        sigma=0.05;
        sigmaR=deg2rad(1);
        
        do_initial_depth_calib_NewInt(true,sigma,sigmaR);
        
        %FAZER TESTES COM E SEM KC:
        do_calib(use_kc,false); %do not use kc or depth distortion
        telapsed = toc(ti);
        
        if use_kc
            strkc = '1';
        else
            strkc='0';
        end
        path_save =['../CalibFiles_NewIntFinalv2/CalibResNU2_' num2str(N) '_set' num2str(i) '_kc' strkc '.mat'];
        do_save_calib(path_save);
        save(path_save, 'telapsed','-append');
%         
%         %% NOISE 3
%         clearvars -except path N Nhip hip use_kc  i hipout idx_best
%         clearvars -global -except max_depth_sample_count
%         
%         path=['../CP_files_Final/CP_' num2str(N) '_set' num2str(i) '.mat'];
%         
%         do_load_calib(path);
%         
%         
%         do_initial_rgb_calib();
%         ti = tic;
%         sigma=0.02;
%         med=0.1;
%         sigmaR=deg2rad(4);
%         
%         do_initial_depth_calib_NewInt(true,sigma, med,sigmaR);
%         
%         %FAZER TESTES COM E SEM KC:
%         do_calib(use_kc,false); %do not use kc or depth distortion
%         telapsed = toc(ti);
%         
%         if use_kc
%             strkc = '1';
%         else
%             strkc='0';
%         end
%         path_save =['../CalibFiles_NewIntFinal/CalibResN3_' num2str(N) '_set' num2str(i) '_kc' strkc '.mat'];
%         do_save_calib(path_save);
%         save(path_save, 'telapsed','-append');
        %         GT = load('../data/CalibResGT.mat');
        %         global final_calib
        %         [nd1 td1]= CompareTs(([GT.final_calib.dR GT.final_calib.dt; 0 0 0 1]), [final_calib.dR final_calib.dt; 0 0 0 1]);
        %         [nd1*1000 td1]
    end
end
