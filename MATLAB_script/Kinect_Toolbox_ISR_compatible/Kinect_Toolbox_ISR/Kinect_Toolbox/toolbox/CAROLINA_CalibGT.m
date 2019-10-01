clear
clearvars -global
clc
%% Create file for GT, without 10 control/validation images:
allIms = 70;
imsVal = [1 8 12 16 17 21 26 27 32 38];
newind = setxor(1:70, imsVal);

full = load('../data/full_set.mat');
%
new_set.dataset_path = '/host/Users/Carolina/Desktop/BIC/Develop/Kinect_Toolbox/data/';
new_set.rfiles{1} = full.rfiles{1}(newind);
new_set.rfiles{2} = full.rfiles{2}(newind);
new_set.rsize = full.rsize;
new_set.dfiles = full.dfiles(newind);
new_set.rgb_grid_p{1} = full.rgb_grid_p{1}(newind);
new_set.rgb_grid_p{2} = full.rgb_grid_p{2}(newind);
new_set.rgb_grid_x{1} = full.rgb_grid_x{1}(newind);
new_set.rgb_grid_x{2} = full.rgb_grid_x{2}(newind);
new_set.depth_corner_p = full.depth_corner_p(newind);
new_set.depth_corner_x = [0 1 1 0;0 0 0.6 0.6];
new_set.depth_plane_poly = full.depth_plane_poly(newind);
new_set.depth_plane_mask = full.depth_plane_mask(newind);
new_set.calib0 = [];
new_set.is_validation = [];
new_set.final_calib = [];
new_set.final_calib_error = [];
path='../data/set_GT.mat';
save(path,'-struct', 'new_set');
%%
%max_depth_sample_count: The maximum number of disparity samples used for
%   full calibration. Used to limit memory usage.
global max_depth_sample_count
max_depth_sample_count = 60000;

do_load_calib(path);


do_initial_rgb_calib();
do_initial_depth_calib(false);

do_calib(false,false);
path_save ='../data/CalibResGTNoDistCorr.mat';
do_save_calib(path_save);
