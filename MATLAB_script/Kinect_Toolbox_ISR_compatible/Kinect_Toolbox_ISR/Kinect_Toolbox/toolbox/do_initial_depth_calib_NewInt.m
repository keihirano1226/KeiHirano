%do_initial_depth_calib()
% UI function
% Kinect calibration toolbox by DHC
function do_initial_depth_calib_NewInt(use_well_known, sigma,sigmaR)

%Inputs
global dataset_path dfiles
global rgb_grid_p rgb_grid_x
global depth_corner_p depth_corner_x
global depth_plane_mask
global max_depth_sample_count
%Outputs
global calib0

if(nargin < 1)
  use_well_known = false;
end

if(isempty(depth_plane_mask))
  do_select_planes();
end
if(isempty(calib0) || isempty(calib0.Rext))
  do_initial_rgb_calib();
end

icount = length(dfiles);
ccount = length(rgb_grid_p);

fprintf('-------------------\n');
fprintf('Initial depth camera calibration\n');
fprintf('-------------------\n');

if(use_well_known)
  fprintf('Using well known values for initial depth camera calibration\n');
  %calib0.dK = [  590 0  320;
   %        0  590 230;
    %       0  0    1];
dK = [  594 0  339;
        0  591 243;
        0  0    1];
    deltadK = abs(sigma*dK);
    dK(1,1) = dK(1,1)-deltadK(1,1)+2*deltadK(1,1)*rand(1);
    dK(1,3) = dK(1,3)-deltadK(1,3)+2*deltadK(1,3)*rand(1);
    dK(2,2) = dK(2,2)-deltadK(2,2)+2*deltadK(2,2)*rand(1);
    dK(2,3) = dK(2,3)-deltadK(2,3)+2*deltadK(2,3)*rand(1);
    calib0.dK=dK;
  calib0.dkc = [0 0 0 0 0];

  dR = [0.9998   -0.0015    0.0175
       0.0013    0.9999    0.0123
       -0.0175   -0.0123    0.9998];
   
   dt = [-0.0198 0.0009 0.0113]';
   
  delta_dt = abs(sigma*dt);  
calib0.dt=[dt(1)-delta_dt(1)+2*delta_dt(1)*rand(1)   dt(2)-delta_dt(2)+2*delta_dt(2)*rand(1) dt(3)-delta_dt(3)+2*delta_dt(3)*rand(1)]'; 
  %calib0.dc = [ -0.0028525         1091];
  %calib0.dc = [3.1121, -0.0028525];
dc=[3.3309495161 -0.0030711016];  
  delta_dc = abs(sigma*dc);  
calib0.dc=[dc(1)-delta_dc(1)+2*delta_dc(1)*rand(1)   dc(2)-delta_dc(2)+2*delta_dc(2)*rand(1)]; 

% Disturb R:
 [vec]=rodrigues(dR);
 nvec = norm(vec);
 newnorm = nvec +2*sigmaR*(rand-0.5);
 
 vec = newnorm*vec/nvec;
 calib0.dR = rodrigues(vec);

else
  fprintf('Estimating initial calibration from depth plane corners.\n');

  %Check previous steps
  if(isempty(depth_corner_p))
    do_select_depth_corners();
  end

  [calib0.dK,calib0.dR,calib0.dt,R0,t0]=estimate_depth_calib_from_corners(depth_corner_x, depth_corner_p, calib0.Rext, calib0.text);
  calib0.dkc = [0 0 0 0 0];
  calib0.dc = estimate_initial_dc(dataset_path,dfiles,depth_corner_p,depth_corner_x,depth_plane_mask,R0,t0);
end
%calib0.dc(3) = 0;
calib0.dc_alpha = [0,0];
calib0.dc_beta = zeros(480,640);
calib0.depth_error_var = 1; %3^2   0.2324;

%Initial pose for depth-only images
fprintf('Estimating initial pose for depth-only images...\n');
missing_rgb = true(1,icount);
for k=1:ccount
  missing_rgb = missing_rgb & cellfun(@(x) isempty(x),rgb_grid_p{k});
end
missing_depth = cellfun(@(x) isempty(x),dfiles);

for i=find(missing_rgb & ~missing_depth)
  [points,disp]=get_depth_samples(dataset_path,dfiles{i},depth_plane_mask{i});
  [points,disp] = reduce_depth_samples(points,disp,max_depth_sample_count);

  fprintf('#%d ',i);
  [calib0.Rext{i},calib0.text{i}] = depth_extern_calib(calib0,points,disp);
end

%Initial minimization
fprintf('Optimizing depth camera parameters...\n');
fprintf('Stats with initial values:\n');
print_calib_stats(calib0);

fprintf('Obtaining samples...');
[depth_plane_points,depth_plane_disparity] = get_depth_samples(dataset_path,dfiles,depth_plane_mask);
[depth_plane_points,depth_plane_disparity] = reduce_depth_samples(depth_plane_points,depth_plane_disparity,max_depth_sample_count);
fprintf('done\n');

options = calibrate_kinect_options();
options.use_fixed_rK = true;
options.use_fixed_rkc = true;
options.use_fixed_dkc = true;
options.use_fixed_rRt = true;
options.use_fixed_dR = false;
options.use_fixed_dt = false;
options.use_fixed_pose = true;

calib0=calibrate_kinect(options,rgb_grid_p,rgb_grid_x,depth_plane_points,depth_plane_disparity,calib0);
fprintf('Stats after depth params optimization:\n');
print_calib_stats(calib0);
