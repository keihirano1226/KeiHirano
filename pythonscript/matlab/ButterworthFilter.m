% 2018/12/13 窪田 真汐
% 位相ずれなしバターワースフィルタ
clc; close all; imtool close all; clear; % 初期化

Fs = 300; % サンプリング周波数
Fc = 15; % 遮断周波数
n = 6; % フィルタ次数
N = 0; % ファイル長さ調整用変数

InputFileName = '新型2回目7.csv'; % 入力ファイル名
OutputFileName = '新型2回目7_フィルタ後.csv'; % 出力ファイル名

x = csvread(InputFileName);
L = length(x(:,1));
[b,a] = butter(n/2,Fc/(Fs/2)); % バターワースフィルタの設計
y = filtfilt(b,a,x(1+N:L-N,:));

csvwrite(OutputFileName,y);