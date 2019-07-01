% 2012/12/19 窪田 真汐
% 体節の姿勢（方向余弦行列行列）を計算する
close all; clear; clc; % 初期化

dt = 1/300; % サンプリング周期
x1 = csvread('新型2回目1_フィルタ後.csv');

load('R_upper_arm_spline'); % DCMの読み込み

L = length(x1(:,1)); % フレーム数
a = 0:L-1;

R_dot = [fnder(R(1,1)) fnder(R(1,2)) fnder(R(1,3));
         fnder(R(2,1)) fnder(R(2,2)) fnder(R(2,3));
         fnder(R(3,1)) fnder(R(3,2)) fnder(R(3,3))];
     
R_dot2 = [fnder(R(1,1),2) fnder(R(1,2),2) fnder(R(1,3),2);
          fnder(R(2,1),2) fnder(R(2,2),2) fnder(R(2,3),2);
          fnder(R(3,1),2) fnder(R(3,2),2) fnder(R(3,3),2)];
     
omega = zeros(3,L);
omega_dot = zeros(3,L);

for i = 1:L
   Temp1 = [ppval(R_dot(1,1), (i-1)/300) ppval(R_dot(1,2), (i-1)/300) ppval(R_dot(1,3), (i-1)/300);
            ppval(R_dot(2,1), (i-1)/300) ppval(R_dot(2,2), (i-1)/300) ppval(R_dot(2,3), (i-1)/300);
            ppval(R_dot(3,1), (i-1)/300) ppval(R_dot(3,2), (i-1)/300) ppval(R_dot(3,3), (i-1)/300)];
        
   Temp2 = [ppval(R_dot2(1,1), (i-1)/300) ppval(R_dot2(1,2), (i-1)/300) ppval(R_dot2(1,3), (i-1)/300);
            ppval(R_dot2(2,1), (i-1)/300) ppval(R_dot2(2,2), (i-1)/300) ppval(R_dot2(2,3), (i-1)/300);
            ppval(R_dot2(3,1), (i-1)/300) ppval(R_dot2(3,2), (i-1)/300) ppval(R_dot2(3,3), (i-1)/300)];
        
   Temp3 = [ppval(R(1,1), (i-1)/300) ppval(R(2,1), (i-1)/300) ppval(R(3,1), (i-1)/300);
            ppval(R(1,2), (i-1)/300) ppval(R(2,2), (i-1)/300) ppval(R(3,2), (i-1)/300);
            ppval(R(1,3), (i-1)/300) ppval(R(2,3), (i-1)/300) ppval(R(3,3), (i-1)/300)];
        
   Temp4 = Temp1 * Temp3;
   Temp5 = Temp2 * Temp3 + Temp1 * Temp1.';
        
   omega(1,i) = (Temp4(3,2) - Temp4(2,3))/2;
   omega(2,i) = (Temp4(1,3) - Temp4(3,1))/2;
   omega(3,i) = (Temp4(2,1) - Temp4(1,2))/2;
   
   omega_dot(1,i) = (Temp5(3,2) - Temp5(2,3))/2;
   omega_dot(2,i) = (Temp5(1,3) - Temp5(3,1))/2;
   omega_dot(3,i) = (Temp5(2,1) - Temp5(1,2))/2;
end

csvwrite('新型2回目上腕角速度スプライン.csv', omega.');
csvwrite('新型2回目上腕角加速度スプライン.csv', omega_dot.');