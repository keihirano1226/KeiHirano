% 2012/12/19 窪田 真汐
% DCMを計算する
close all; clear; clc; % 初期化

dt = 1/300;

P0 = [1 0 0; 0 1 0; 0 0 1]; % 基準となる姿勢行列
load('P_upper_arm'); % 姿勢行列の読み込み

L = length(E.e1(1,:)); % フレーム数
a = 0:L-1;
R = zeros(3,3,L);

for i=1:L
    R(:,:,i) = [E.e1(:,i) E.e2(:,i) E.e3(:,i)]/P0;
end