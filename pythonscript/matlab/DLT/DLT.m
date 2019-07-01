% 2018/12/11 窪田 真汐
% トラッキングデータの3次元化用

clc; close all; imtool close all; clear; % 初期化

% カメラパラメータの読み込み
load('CameraParameters_L.mat');

% マーカ座標の読み込み
data1 = csvread('新型2回目左横7.csv');
data2 = csvread('新型2回目左前7.csv');

frames = length(data1(:,1));

u = zeros(frames,2);
v = zeros(frames,2);

u(:,1) = data1(:,1);
u(:,2) = data2(:,1);
v(:,1) = data1(:,2);
v(:,2) = data2(:,2);

% 3次元座標への変換
A = zeros(4,3,frames);
AT = zeros(3,4,frames);
X = zeros(frames,3);
XT = zeros(3,frames);
uv = zeros(4,frames);


for j = 1:frames
    for k = 1:2
        A(2*k-1,:,j) = L(1:3,k).' - u(j,k)*L(9:11,k).';
        A(2*k,:,j) = L(5:7,k).' - v(j,k)*L(9:11,k).';
        uv(2*k-1,j) = u(j,k) - L(4,k);
        uv(2*k,j) = v(j,k) - L(8,k);            
    end

    AT(:,:,j) = A(:,:,j).';
    XT(:,j) = (AT(:,:,j)*A(:,:,j)) \ (AT(:,:,j)*uv(:,j));
end
X(:,:) =XT(:,:).';


% 結果の出力
csvwrite('新型2回目7.csv', X);
