clear
clearvars -global
clc
Npose = 15;
load ../CP_files/sets.mat

%max_depth_sample_count: The maximum number of disparity samples used for
%   full calibration. Used to limit memory usage.
global max_depth_sample_count 
max_depth_sample_count = 60000;

for N=8
    N
    hip = hipout{N-2};

    Nhip = size(hip,1);
    for i=1
        
        path=['../CP_files/CP_' num2str(N) '_set' num2str(i) '.mat'];
        
        do_load_calib(path);
        
        
        do_initial_rgb_calib();
        do_initial_depth_calib_NewInt(true);
        
        do_calib(false,false); %do not use kc or depth distortion
        
%         path_save =['../CP_files/CalibFilesAll_NewInt/CalibRes_' num2str(N) '_set' num2str(i) '.mat'];
%         do_save_calib(path_save);
    end
end
