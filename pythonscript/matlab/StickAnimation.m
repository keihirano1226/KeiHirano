% 2012/12/13 窪田 真汐
% スティックアニメーションを作成する

close all; clear; clc; % 初期化

LN = 8; % スティックの本数
N = 7; % 関節の数
a = 0:9; % スティック描画用変数

v = VideoWriter('新型2回目.mp4','MPEG-4'); % 動画書き出し用オブジェクト
open(v);

x1 = csvread('新型2回目1_フィルタ後.csv'); % マーカ位置の読み込み
x2 = csvread('新型2回目2_フィルタ後.csv');
x3 = csvread('新型2回目3_フィルタ後.csv');
x4 = csvread('新型2回目4_フィルタ後.csv');
x5 = csvread('新型2回目5_フィルタ後.csv');
x6 = csvread('新型2回目6_フィルタ後.csv');
x7 = csvread('新型2回目7_フィルタ後.csv');

x = struct('Position', {x1, x2, x3, x4, x5, x6, x7}); % マーカ位置格納用の構造体

L = length(x1(:,1)); % フレーム数

U = zeros(L,LN*length(a),3); % スティックを構成する点群

for i=1:L
    for j=1:3
        U(i,1:10,j) = x1(i,j) + (x2(i,j)-x1(i,j)) * a/9; % 上腕のスティック描画用の点群
        U(i,11:20,j) = x2(i,j) + (x3(i,j)-x2(i,j)) * a/9;
        U(i,21:30,j) = x3(i,j) + (x1(i,j)-x3(i,j)) * a/9;
        
        U(i,31:40,j) = x3(i,j) + (x4(i,j)-x3(i,j)) * a/9; % 前腕のスティック描画用の点群
        U(i,41:50,j) = x4(i,j) + (x5(i,j)-x4(i,j)) * a/9;
        U(i,51:60,j) = x5(i,j) + (x3(i,j)-x5(i,j)) * a/9;
        
        U(i,61:70,j) = x5(i,j) + (x6(i,j)-x5(i,j)) * a/9; % 義手のスティック描画用の点群
        U(i,71:80,j) = x6(i,j) + (x7(i,j)-x6(i,j)) * a/9;
    end   
end

figure('Position',[300 300 1000 600])

Hl = line(U(1,:,1),U(i,:,2),U(i,:,3)); hold on % スティック描画用のオブジェクト
Hl = handle(Hl); 
Hl.Color = 'r';

Hp = struct('Point',{ plot3(x1(1,1),x1(1,2),x1(1,3),'ro','MarkerSize',4), ... % マーカ位置描画用の構造体
                       plot3(x2(1,1),x2(1,2),x2(1,3),'ro','MarkerSize',4), ...
                       plot3(x3(1,1),x3(1,2),x3(1,3),'ro','MarkerSize',4), ...
                       plot3(x4(1,1),x4(1,2),x4(1,3),'ro','MarkerSize',4), ...
                       plot3(x5(1,1),x5(1,2),x5(1,3),'ro','MarkerSize',4), ...
                       plot3(x6(1,1),x6(1,2),x6(1,3),'ro','MarkerSize',4), ...
                       plot3(x7(1,1),x7(1,2),x7(1,3),'ro','MarkerSize',4)});


xlim([0 1.2]); ylim([0 5]); zlim([0.4 1.6]), grid on
xticks([0 0.6 1.2]); yticks([0 1 2 3 4 5]); zticks([0 1 2]);
daspect([1 1 1])

set(gca,'CameraPosition',[-1 3 1.4]) % 視点の変更

for i=1:L
    Hl.XData = U(i,:,1); % フレームごとにスティックを更新
    Hl.YData = U(i,:,2);
    Hl.ZData = U(i,:,3);
    
    for j=1:N
        Hp(j).Point.XData = x(j).Position(i,1); % フレームごとにマーカ位置を更新
        Hp(j).Point.YData = x(j).Position(i,2);
        Hp(j).Point.ZData = x(j).Position(i,3);
    end
    
    frame = getframe(gcf);
    writeVideo(v,frame);
    
    pause(0.03)
end

close(v);
