% Intrinsic and Extrinsic Camera Parameters
%
% This script file can be directly excecuted under Matlab to recover the camera intrinsic and extrinsic parameters.
% IMPORTANT: This file contains neither the structure of the calibration objects nor the image coordinates of the calibration points.
%            All those complementary variables are saved in the complete matlab data file Calib_Results.mat.
% For more information regarding the calibration model visit http://www.vision.caltech.edu/bouguetj/calib_doc/


%-- Focal length:
fc = [ 1058.783729357031234 ; 1052.377619992395694 ];

%-- Principal point:
cc = [ 619.168408026752445 ; 503.579994751386323 ];

%-- Skew coefficient:
alpha_c = 0.000000000000000;

%-- Distortion coefficients:
kc = [ 0.267494055230499 ; -1.072110856469649 ; -0.007949035899917 ; 0.001904690897876 ; 0.000000000000000 ];

%-- Focal length uncertainty:
fc_error = [ 10.016308361910191 ; 9.841696433582717 ];

%-- Principal point uncertainty:
cc_error = [ 10.933521970280525 ; 9.555854926757993 ];

%-- Skew coefficient uncertainty:
alpha_c_error = 0.000000000000000;

%-- Distortion coefficients uncertainty:
kc_error = [ 0.044930380681967 ; 0.408792131538258 ; 0.004081961319529 ; 0.004240941168182 ; 0.000000000000000 ];

%-- Image size:
nx = 1280;
ny = 1024;


%-- Various other variables (may be ignored if you do not use the Matlab Calibration Toolbox):
%-- Those variables are used to control which intrinsic parameters should be optimized

n_ima = 38;						% Number of calibration images
est_fc = [ 1 ; 1 ];					% Estimation indicator of the two focal variables
est_aspect_ratio = 1;				% Estimation indicator of the aspect ratio fc(2)/fc(1)
center_optim = 1;					% Estimation indicator of the principal point
est_alpha = 0;						% Estimation indicator of the skew coefficient
est_dist = [ 1 ; 1 ; 1 ; 1 ; 0 ];	% Estimation indicator of the distortion coefficients


%-- Extrinsic parameters:
%-- The rotation (omc_kk) and the translation (Tc_kk) vectors for every calibration image and their uncertainties

%-- Image #1:
omc_1 = [ NaN ; NaN ; NaN ];
Tc_1  = [ NaN ; NaN ; NaN ];
omc_error_1 = [ NaN ; NaN ; NaN ];
Tc_error_1  = [ NaN ; NaN ; NaN ];

%-- Image #2:
omc_2 = [ -2.224259e+00 ; -2.214313e+00 ; 3.608741e-03 ];
Tc_2  = [ -1.334381e+02 ; -1.417228e+02 ; 6.304915e+02 ];
omc_error_2 = [ 5.728339e-03 ; 5.241941e-03 ; 1.200139e-02 ];
Tc_error_2  = [ 6.528925e+00 ; 5.747082e+00 ; 5.999632e+00 ];

%-- Image #3:
omc_3 = [ NaN ; NaN ; NaN ];
Tc_3  = [ NaN ; NaN ; NaN ];
omc_error_3 = [ NaN ; NaN ; NaN ];
Tc_error_3  = [ NaN ; NaN ; NaN ];

%-- Image #4:
omc_4 = [ NaN ; NaN ; NaN ];
Tc_4  = [ NaN ; NaN ; NaN ];
omc_error_4 = [ NaN ; NaN ; NaN ];
Tc_error_4  = [ NaN ; NaN ; NaN ];

%-- Image #5:
omc_5 = [ NaN ; NaN ; NaN ];
Tc_5  = [ NaN ; NaN ; NaN ];
omc_error_5 = [ NaN ; NaN ; NaN ];
Tc_error_5  = [ NaN ; NaN ; NaN ];

%-- Image #6:
omc_6 = [ NaN ; NaN ; NaN ];
Tc_6  = [ NaN ; NaN ; NaN ];
omc_error_6 = [ NaN ; NaN ; NaN ];
Tc_error_6  = [ NaN ; NaN ; NaN ];

%-- Image #7:
omc_7 = [ NaN ; NaN ; NaN ];
Tc_7  = [ NaN ; NaN ; NaN ];
omc_error_7 = [ NaN ; NaN ; NaN ];
Tc_error_7  = [ NaN ; NaN ; NaN ];

%-- Image #8:
omc_8 = [ NaN ; NaN ; NaN ];
Tc_8  = [ NaN ; NaN ; NaN ];
omc_error_8 = [ NaN ; NaN ; NaN ];
Tc_error_8  = [ NaN ; NaN ; NaN ];

%-- Image #9:
omc_9 = [ NaN ; NaN ; NaN ];
Tc_9  = [ NaN ; NaN ; NaN ];
omc_error_9 = [ NaN ; NaN ; NaN ];
Tc_error_9  = [ NaN ; NaN ; NaN ];

%-- Image #10:
omc_10 = [ NaN ; NaN ; NaN ];
Tc_10  = [ NaN ; NaN ; NaN ];
omc_error_10 = [ NaN ; NaN ; NaN ];
Tc_error_10  = [ NaN ; NaN ; NaN ];

%-- Image #11:
omc_11 = [ NaN ; NaN ; NaN ];
Tc_11  = [ NaN ; NaN ; NaN ];
omc_error_11 = [ NaN ; NaN ; NaN ];
Tc_error_11  = [ NaN ; NaN ; NaN ];

%-- Image #12:
omc_12 = [ NaN ; NaN ; NaN ];
Tc_12  = [ NaN ; NaN ; NaN ];
omc_error_12 = [ NaN ; NaN ; NaN ];
Tc_error_12  = [ NaN ; NaN ; NaN ];

%-- Image #13:
omc_13 = [ -2.246710e+00 ; -2.201607e+00 ; -6.062797e-02 ];
Tc_13  = [ -1.417253e+02 ; -4.745213e+01 ; 2.419873e+03 ];
omc_error_13 = [ 2.313023e-02 ; 2.316029e-02 ; 5.026541e-02 ];
Tc_error_13  = [ 2.501027e+01 ; 2.199294e+01 ; 2.398448e+01 ];

%-- Image #14:
omc_14 = [ NaN ; NaN ; NaN ];
Tc_14  = [ NaN ; NaN ; NaN ];
omc_error_14 = [ NaN ; NaN ; NaN ];
Tc_error_14  = [ NaN ; NaN ; NaN ];

%-- Image #15:
omc_15 = [ NaN ; NaN ; NaN ];
Tc_15  = [ NaN ; NaN ; NaN ];
omc_error_15 = [ NaN ; NaN ; NaN ];
Tc_error_15  = [ NaN ; NaN ; NaN ];

%-- Image #16:
omc_16 = [ NaN ; NaN ; NaN ];
Tc_16  = [ NaN ; NaN ; NaN ];
omc_error_16 = [ NaN ; NaN ; NaN ];
Tc_error_16  = [ NaN ; NaN ; NaN ];

%-- Image #17:
omc_17 = [ NaN ; NaN ; NaN ];
Tc_17  = [ NaN ; NaN ; NaN ];
omc_error_17 = [ NaN ; NaN ; NaN ];
Tc_error_17  = [ NaN ; NaN ; NaN ];

%-- Image #18:
omc_18 = [ 1.616010e+00 ; 1.700905e+00 ; 8.615336e-01 ];
Tc_18  = [ -5.617921e+01 ; -1.318616e+02 ; 7.383919e+02 ];
omc_error_18 = [ 9.616148e-03 ; 7.170972e-03 ; 1.099966e-02 ];
Tc_error_18  = [ 7.616319e+00 ; 6.687867e+00 ; 7.358509e+00 ];

%-- Image #19:
omc_19 = [ NaN ; NaN ; NaN ];
Tc_19  = [ NaN ; NaN ; NaN ];
omc_error_19 = [ NaN ; NaN ; NaN ];
Tc_error_19  = [ NaN ; NaN ; NaN ];

%-- Image #20:
omc_20 = [ NaN ; NaN ; NaN ];
Tc_20  = [ NaN ; NaN ; NaN ];
omc_error_20 = [ NaN ; NaN ; NaN ];
Tc_error_20  = [ NaN ; NaN ; NaN ];

%-- Image #21:
omc_21 = [ NaN ; NaN ; NaN ];
Tc_21  = [ NaN ; NaN ; NaN ];
omc_error_21 = [ NaN ; NaN ; NaN ];
Tc_error_21  = [ NaN ; NaN ; NaN ];

%-- Image #22:
omc_22 = [ NaN ; NaN ; NaN ];
Tc_22  = [ NaN ; NaN ; NaN ];
omc_error_22 = [ NaN ; NaN ; NaN ];
Tc_error_22  = [ NaN ; NaN ; NaN ];

%-- Image #23:
omc_23 = [ NaN ; NaN ; NaN ];
Tc_23  = [ NaN ; NaN ; NaN ];
omc_error_23 = [ NaN ; NaN ; NaN ];
Tc_error_23  = [ NaN ; NaN ; NaN ];

%-- Image #24:
omc_24 = [ NaN ; NaN ; NaN ];
Tc_24  = [ NaN ; NaN ; NaN ];
omc_error_24 = [ NaN ; NaN ; NaN ];
Tc_error_24  = [ NaN ; NaN ; NaN ];

%-- Image #25:
omc_25 = [ NaN ; NaN ; NaN ];
Tc_25  = [ NaN ; NaN ; NaN ];
omc_error_25 = [ NaN ; NaN ; NaN ];
Tc_error_25  = [ NaN ; NaN ; NaN ];

%-- Image #26:
omc_26 = [ NaN ; NaN ; NaN ];
Tc_26  = [ NaN ; NaN ; NaN ];
omc_error_26 = [ NaN ; NaN ; NaN ];
Tc_error_26  = [ NaN ; NaN ; NaN ];

%-- Image #27:
omc_27 = [ NaN ; NaN ; NaN ];
Tc_27  = [ NaN ; NaN ; NaN ];
omc_error_27 = [ NaN ; NaN ; NaN ];
Tc_error_27  = [ NaN ; NaN ; NaN ];

%-- Image #28:
omc_28 = [ NaN ; NaN ; NaN ];
Tc_28  = [ NaN ; NaN ; NaN ];
omc_error_28 = [ NaN ; NaN ; NaN ];
Tc_error_28  = [ NaN ; NaN ; NaN ];

%-- Image #29:
omc_29 = [ NaN ; NaN ; NaN ];
Tc_29  = [ NaN ; NaN ; NaN ];
omc_error_29 = [ NaN ; NaN ; NaN ];
Tc_error_29  = [ NaN ; NaN ; NaN ];

%-- Image #30:
omc_30 = [ NaN ; NaN ; NaN ];
Tc_30  = [ NaN ; NaN ; NaN ];
omc_error_30 = [ NaN ; NaN ; NaN ];
Tc_error_30  = [ NaN ; NaN ; NaN ];

%-- Image #31:
omc_31 = [ 1.678667e+00 ; 1.715430e+00 ; -8.336364e-01 ];
Tc_31  = [ -1.842147e+02 ; -1.344676e+02 ; 1.396809e+03 ];
omc_error_31 = [ 5.944468e-03 ; 9.567791e-03 ; 1.094076e-02 ];
Tc_error_31  = [ 1.435549e+01 ; 1.267047e+01 ; 1.204641e+01 ];

%-- Image #32:
omc_32 = [ NaN ; NaN ; NaN ];
Tc_32  = [ NaN ; NaN ; NaN ];
omc_error_32 = [ NaN ; NaN ; NaN ];
Tc_error_32  = [ NaN ; NaN ; NaN ];

%-- Image #33:
omc_33 = [ NaN ; NaN ; NaN ];
Tc_33  = [ NaN ; NaN ; NaN ];
omc_error_33 = [ NaN ; NaN ; NaN ];
Tc_error_33  = [ NaN ; NaN ; NaN ];

%-- Image #34:
omc_34 = [ NaN ; NaN ; NaN ];
Tc_34  = [ NaN ; NaN ; NaN ];
omc_error_34 = [ NaN ; NaN ; NaN ];
Tc_error_34  = [ NaN ; NaN ; NaN ];

%-- Image #35:
omc_35 = [ NaN ; NaN ; NaN ];
Tc_35  = [ NaN ; NaN ; NaN ];
omc_error_35 = [ NaN ; NaN ; NaN ];
Tc_error_35  = [ NaN ; NaN ; NaN ];

%-- Image #36:
omc_36 = [ NaN ; NaN ; NaN ];
Tc_36  = [ NaN ; NaN ; NaN ];
omc_error_36 = [ NaN ; NaN ; NaN ];
Tc_error_36  = [ NaN ; NaN ; NaN ];

%-- Image #37:
omc_37 = [ NaN ; NaN ; NaN ];
Tc_37  = [ NaN ; NaN ; NaN ];
omc_error_37 = [ NaN ; NaN ; NaN ];
Tc_error_37  = [ NaN ; NaN ; NaN ];

%-- Image #38:
omc_38 = [ NaN ; NaN ; NaN ];
Tc_38  = [ NaN ; NaN ; NaN ];
omc_error_38 = [ NaN ; NaN ; NaN ];
Tc_error_38  = [ NaN ; NaN ; NaN ];

