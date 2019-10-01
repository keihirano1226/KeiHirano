

clear all;close all;clc;



rmpath('bouguet/toolbox_calib');

addpath('Kinect_Toolbox/toolbox');

addpath('Funcs');

addpath('DepthCamCalib');

addpath('EstimateDistModel');



Nfix = 4

Nimsvar = Nfix

fileCP = ['CPfiles/CP_' num2str(Nimsvar) '.mat']

fileBou = ['BouFiles/BouCalibRes_' num2str(Nimsvar) '.mat']

filePlane = 'PlaneCornersInfo.mat'





loadF = fileBou;

planeinfo = filePlane;

MyTB_Calib;

resCalib = save_file;





res_file = resCalib;

EstDistortion;

distCorr = ['MyTBCalibDistEst' num2str(Nimsvar) '.mat'];

































