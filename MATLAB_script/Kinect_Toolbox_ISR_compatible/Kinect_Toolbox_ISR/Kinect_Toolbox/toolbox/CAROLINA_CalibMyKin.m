clear
clearvars -global
clc
%% Create file for GT, without 10 control/validation images:
allIms = 70;
newind = [1 8 9 10 11 12 14 15];

full = load('../data/calibmy.mat');
%
new_set.dataset_path = full.dataset_path;
new_set.rfiles{1} = full.rfiles{1}(newind);
new_set.rsize = full.rsize;
new_set.dfiles = full.dfiles(newind);
new_set.rgb_grid_p{1} = full.rgb_grid_p{1}(newind);
new_set.rgb_grid_x{1} = full.rgb_grid_x{1}(newind);
new_set.depth_corner_p = [];
new_set.depth_corner_x = [];
new_set.depth_plane_poly = full.depth_plane_poly(newind);
new_set.depth_plane_mask = full.depth_plane_mask(newind);
new_set.calib0 = [];
new_set.is_validation = [];
new_set.final_calib = [];
new_set.final_calib_error = [];
path='../data/calibmySet.mat';
save(path,'-struct', 'new_set');
%%
%max_depth_sample_count: The maximum number of disparity samples used for
%   full calibration. Used to limit memory usage.
global max_depth_sample_count
max_depth_sample_count = 60000;

do_load_calib(path);


do_initial_rgb_calib();
do_initial_depth_calib_NewInt(true,0,0);

do_calib(false,true);
path_save ='../data/CalibResMyKinDistCorr.mat';
do_save_calib(path_save);
