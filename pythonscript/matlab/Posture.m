% 2012/12/14 窪田 真汐
% 体節の姿勢（方向余弦行列行列）を計算する

close all; clear; clc; % 初期化

N = 7; % 関節の数
a = 0:9; % スティック描画用変数

% v = VideoWriter('新型2回目姿勢.mp4','MPEG-4'); % 動画書き出し用オブジェクト
% open(v);

x1 = csvread('新型2回目1_フィルタ後.csv');
x2 = csvread('新型2回目2_フィルタ後.csv');
x3 = csvread('新型2回目3_フィルタ後.csv');
x4 = csvread('新型2回目4_フィルタ後.csv');
x5 = csvread('新型2回目5_フィルタ後.csv');
x6 = csvread('新型2回目6_フィルタ後.csv');
x7 = csvread('新型2回目7_フィルタ後.csv');

L = length(x1(:,1)); % フレーム数

E = struct('e1', zeros(3,L), ... % DCM格納用の構造体
           'e2', zeros(3,L), ...
           'e3', zeros(3,L));

x = struct('Position', {x1, x2, x3, x4, x5, x6, x7}); % マーカ位置格納用の構造体

U = zeros(L,3*length(a),3); % 姿勢行列を構成する点群

for i=1:L % 姿勢行列の計算
%     E.e1(:,i) = (x1(i,:)-x3(i,:)).'/norm((x1(i,:)-x3(i,:)).'); % 上腕用
%     E.e3(:,i) = cross(E.e1(:,i), (x2(i,:)-x3(i,:)).')/norm(cross(E.e1(:,i), (x2(i,:)-x3(i,:)).'));
%     E.e2(:,i) = cross(E.e3(:,i),E.e1(:,i))/norm(cross(E.e3(:,i),E.e1(:,i)));
    
%     E.e1(:,i) = (x1(i,:)-x3(i,:)).'/norm((x1(i,:)-x3(i,:)).'); % 上腕用2
%     E.e3(:,i) = cross(E.e1(:,i), (x5(i,:)-x3(i,:)).')/norm(cross(E.e1(:,i), (x5(i,:)-x3(i,:)).'));
%     E.e2(:,i) = cross(E.e3(:,i),E.e1(:,i))/norm(cross(E.e3(:,i),E.e1(:,i)));
 
%     E.e1(:,i) = (x3(i,:)-x5(i,:)).'/norm((x3(i,:)-x5(i,:)).'); % 前腕用
%     E.e3(:,i) = cross(E.e1(:,i), (x1(i,:)-x3(i,:)).')/norm(cross(E.e1(:,i), (x1(i,:)-x3(i,:)).'));
%     E.e2(:,i) = cross(E.e3(:,i),E.e1(:,i))/norm(cross(E.e3(:,i),E.e1(:,i)));
    
%     E.e1(:,i) = (x5(i,:)-x6(i,:)).'/norm((x5(i,:)-x6(i,:)).'); % 板ばね用
%     E.e3(:,i) = cross(E.e1(:,i), (x1(i,:)-x3(i,:)).')/norm(cross(E.e1(:,i), (x1(i,:)-x3(i,:)).'));
%     E.e2(:,i) = cross(E.e3(:,i),E.e1(:,i))/norm(cross(E.e3(:,i),E.e1(:,i)));  
    
    E.e1(:,i) = (x6(i,:)-x7(i,:)).'/norm((x6(i,:)-x7(i,:)).'); % 義手先端用
    E.e3(:,i) = cross(E.e1(:,i), (x1(i,:)-x3(i,:)).')/norm(cross(E.e1(:,i), (x1(i,:)-x3(i,:)).'));
    E.e2(:,i) = cross(E.e3(:,i),E.e1(:,i))/norm(cross(E.e3(:,i),E.e1(:,i)));
end

temp = length(a)-1;

for i=1:L
    for j=1:3
%        U(i,1:10,j) = (x1(i,j)+x3(i,j))/2 + 0.2 * E.e1(j,i) * a/temp; % 上腕用
%        U(i,11:20,j) = (x1(i,j)+x3(i,j))/2 + 0.2 * E.e2(j,i) * a/temp;
%        U(i,21:30,j) = (x1(i,j)+x3(i,j))/2 + 0.2 * E.e3(j,i) * a/temp;
       
%       U(i,1:10,j) = (x5(i,j)+x3(i,j))/2 + 0.2 * E.e1(j,i) * a/temp; % 前腕用
%       U(i,11:20,j) = (x5(i,j)+x3(i,j))/2 + 0.2 * E.e2(j,i) * a/temp;
%       U(i,21:30,j) = (x5(i,j)+x3(i,j))/2 + 0.2 * E.e3(j,i) * a/temp;

%        U(i,1:10,j) = (x5(i,j)+x6(i,j))/2 + 0.2 * E.e1(j,i) * a/temp; % 板ばね用
%        U(i,11:20,j) = (x5(i,j)+x6(i,j))/2 + 0.2 * E.e2(j,i) * a/temp;
%        U(i,21:30,j) = (x5(i,j)+x6(i,j))/2 + 0.2 * E.e3(j,i) * a/temp;
       
%        U(i,1:10,j) = (x7(i,j)+x6(i,j))/2 + 0.2 * E.e1(j,i) * a/temp; % 義手先端用
%        U(i,11:20,j) = (x7(i,j)+x6(i,j))/2 + 0.2 * E.e2(j,i) * a/temp;
%        U(i,21:30,j) = (x7(i,j)+x6(i,j))/2 + 0.2 * E.e3(j,i) * a/temp;
    end
end

% figure('Position',[300 300 1000 600])
% 
% Hl = line(U(1,:,1),U(1,:,2),U(1,:,3)); hold on
% Hl = handle(Hl); 
% Hl.Color = 'b';
% 
% Hp = struct('Point',{ plot3(x1(1,1),x1(1,2),x1(1,3),'ro','MarkerSize',4), ... % マーカ位置描画用の構造体
%                       plot3(x2(1,1),x2(1,2),x2(1,3),'ro','MarkerSize',4), ...
%                       plot3(x3(1,1),x3(1,2),x3(1,3),'ro','MarkerSize',4), ...
%                       plot3(x4(1,1),x4(1,2),x4(1,3),'ro','MarkerSize',4), ...
%                       plot3(x5(1,1),x5(1,2),x5(1,3),'ro','MarkerSize',4), ...
%                       plot3(x6(1,1),x6(1,2),x6(1,3),'ro','MarkerSize',4), ...
%                       plot3(x7(1,1),x7(1,2),x7(1,3),'ro','MarkerSize',4)});
% 
% 
% xlim([0 1.2]); ylim([0 5]); zlim([0.4 1.6]), grid on
% xticks([0 0.6 1.2]); yticks([0 1 2 3 4 5]); zticks([0 1 2]);
% daspect([1 1 1])
% 
% set(gca,'CameraPosition',[0.6 5 1]) % 視点の変更
% 
% for i=1:L
%     Hl.XData = U(i,:,1);
%     Hl.YData = U(i,:,2);
%     Hl.ZData = U(i,:,3);
%     
%     for j=1:N
%         Hp(j).Point.XData = x(j).Position(i,1); % フレームごとにマーカ位置を更新
%         Hp(j).Point.YData = x(j).Position(i,2);
%         Hp(j).Point.ZData = x(j).Position(i,3);
%     end
%     
% %     frame = getframe(gcf);
% %     writeVideo(v,frame);
%     
%     pause(0.03)
% end

% close(v);
