% 2012/12/14 �E�c �^��
% �̐߂̎p���i�����]���s��s��j���v�Z����

close all; clear; clc; % ������

N = 7; % �֐߂̐�
a = 0:9; % �X�e�B�b�N�`��p�ϐ�

% v = VideoWriter('�V�^2��ڎp��.mp4','MPEG-4'); % ���揑���o���p�I�u�W�F�N�g
% open(v);

x1 = csvread('�V�^2���1_�t�B���^��.csv');
x2 = csvread('�V�^2���2_�t�B���^��.csv');
x3 = csvread('�V�^2���3_�t�B���^��.csv');
x4 = csvread('�V�^2���4_�t�B���^��.csv');
x5 = csvread('�V�^2���5_�t�B���^��.csv');
x6 = csvread('�V�^2���6_�t�B���^��.csv');
x7 = csvread('�V�^2���7_�t�B���^��.csv');

L = length(x1(:,1)); % �t���[����

E = struct('e1', zeros(3,L), ... % DCM�i�[�p�̍\����
           'e2', zeros(3,L), ...
           'e3', zeros(3,L));

x = struct('Position', {x1, x2, x3, x4, x5, x6, x7}); % �}�[�J�ʒu�i�[�p�̍\����

U = zeros(L,3*length(a),3); % �p���s����\������_�Q

for i=1:L % �p���s��̌v�Z
%     E.e1(:,i) = (x1(i,:)-x3(i,:)).'/norm((x1(i,:)-x3(i,:)).'); % ��r�p
%     E.e3(:,i) = cross(E.e1(:,i), (x2(i,:)-x3(i,:)).')/norm(cross(E.e1(:,i), (x2(i,:)-x3(i,:)).'));
%     E.e2(:,i) = cross(E.e3(:,i),E.e1(:,i))/norm(cross(E.e3(:,i),E.e1(:,i)));
    
%     E.e1(:,i) = (x1(i,:)-x3(i,:)).'/norm((x1(i,:)-x3(i,:)).'); % ��r�p2
%     E.e3(:,i) = cross(E.e1(:,i), (x5(i,:)-x3(i,:)).')/norm(cross(E.e1(:,i), (x5(i,:)-x3(i,:)).'));
%     E.e2(:,i) = cross(E.e3(:,i),E.e1(:,i))/norm(cross(E.e3(:,i),E.e1(:,i)));
 
%     E.e1(:,i) = (x3(i,:)-x5(i,:)).'/norm((x3(i,:)-x5(i,:)).'); % �O�r�p
%     E.e3(:,i) = cross(E.e1(:,i), (x1(i,:)-x3(i,:)).')/norm(cross(E.e1(:,i), (x1(i,:)-x3(i,:)).'));
%     E.e2(:,i) = cross(E.e3(:,i),E.e1(:,i))/norm(cross(E.e3(:,i),E.e1(:,i)));
    
%     E.e1(:,i) = (x5(i,:)-x6(i,:)).'/norm((x5(i,:)-x6(i,:)).'); % �΂˗p
%     E.e3(:,i) = cross(E.e1(:,i), (x1(i,:)-x3(i,:)).')/norm(cross(E.e1(:,i), (x1(i,:)-x3(i,:)).'));
%     E.e2(:,i) = cross(E.e3(:,i),E.e1(:,i))/norm(cross(E.e3(:,i),E.e1(:,i)));  
    
    E.e1(:,i) = (x6(i,:)-x7(i,:)).'/norm((x6(i,:)-x7(i,:)).'); % �`���[�p
    E.e3(:,i) = cross(E.e1(:,i), (x1(i,:)-x3(i,:)).')/norm(cross(E.e1(:,i), (x1(i,:)-x3(i,:)).'));
    E.e2(:,i) = cross(E.e3(:,i),E.e1(:,i))/norm(cross(E.e3(:,i),E.e1(:,i)));
end

temp = length(a)-1;

for i=1:L
    for j=1:3
%        U(i,1:10,j) = (x1(i,j)+x3(i,j))/2 + 0.2 * E.e1(j,i) * a/temp; % ��r�p
%        U(i,11:20,j) = (x1(i,j)+x3(i,j))/2 + 0.2 * E.e2(j,i) * a/temp;
%        U(i,21:30,j) = (x1(i,j)+x3(i,j))/2 + 0.2 * E.e3(j,i) * a/temp;
       
%       U(i,1:10,j) = (x5(i,j)+x3(i,j))/2 + 0.2 * E.e1(j,i) * a/temp; % �O�r�p
%       U(i,11:20,j) = (x5(i,j)+x3(i,j))/2 + 0.2 * E.e2(j,i) * a/temp;
%       U(i,21:30,j) = (x5(i,j)+x3(i,j))/2 + 0.2 * E.e3(j,i) * a/temp;

%        U(i,1:10,j) = (x5(i,j)+x6(i,j))/2 + 0.2 * E.e1(j,i) * a/temp; % �΂˗p
%        U(i,11:20,j) = (x5(i,j)+x6(i,j))/2 + 0.2 * E.e2(j,i) * a/temp;
%        U(i,21:30,j) = (x5(i,j)+x6(i,j))/2 + 0.2 * E.e3(j,i) * a/temp;
       
%        U(i,1:10,j) = (x7(i,j)+x6(i,j))/2 + 0.2 * E.e1(j,i) * a/temp; % �`���[�p
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
% Hp = struct('Point',{ plot3(x1(1,1),x1(1,2),x1(1,3),'ro','MarkerSize',4), ... % �}�[�J�ʒu�`��p�̍\����
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
% set(gca,'CameraPosition',[0.6 5 1]) % ���_�̕ύX
% 
% for i=1:L
%     Hl.XData = U(i,:,1);
%     Hl.YData = U(i,:,2);
%     Hl.ZData = U(i,:,3);
%     
%     for j=1:N
%         Hp(j).Point.XData = x(j).Position(i,1); % �t���[�����ƂɃ}�[�J�ʒu���X�V
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
