% 2012/12/13 �E�c �^��
% �X�e�B�b�N�A�j���[�V�������쐬����

close all; clear; clc; % ������

LN = 8; % �X�e�B�b�N�̖{��
N = 7; % �֐߂̐�
a = 0:9; % �X�e�B�b�N�`��p�ϐ�

v = VideoWriter('�V�^2���.mp4','MPEG-4'); % ���揑���o���p�I�u�W�F�N�g
open(v);

x1 = csvread('�V�^2���1_�t�B���^��.csv'); % �}�[�J�ʒu�̓ǂݍ���
x2 = csvread('�V�^2���2_�t�B���^��.csv');
x3 = csvread('�V�^2���3_�t�B���^��.csv');
x4 = csvread('�V�^2���4_�t�B���^��.csv');
x5 = csvread('�V�^2���5_�t�B���^��.csv');
x6 = csvread('�V�^2���6_�t�B���^��.csv');
x7 = csvread('�V�^2���7_�t�B���^��.csv');

x = struct('Position', {x1, x2, x3, x4, x5, x6, x7}); % �}�[�J�ʒu�i�[�p�̍\����

L = length(x1(:,1)); % �t���[����

U = zeros(L,LN*length(a),3); % �X�e�B�b�N���\������_�Q

for i=1:L
    for j=1:3
        U(i,1:10,j) = x1(i,j) + (x2(i,j)-x1(i,j)) * a/9; % ��r�̃X�e�B�b�N�`��p�̓_�Q
        U(i,11:20,j) = x2(i,j) + (x3(i,j)-x2(i,j)) * a/9;
        U(i,21:30,j) = x3(i,j) + (x1(i,j)-x3(i,j)) * a/9;
        
        U(i,31:40,j) = x3(i,j) + (x4(i,j)-x3(i,j)) * a/9; % �O�r�̃X�e�B�b�N�`��p�̓_�Q
        U(i,41:50,j) = x4(i,j) + (x5(i,j)-x4(i,j)) * a/9;
        U(i,51:60,j) = x5(i,j) + (x3(i,j)-x5(i,j)) * a/9;
        
        U(i,61:70,j) = x5(i,j) + (x6(i,j)-x5(i,j)) * a/9; % �`��̃X�e�B�b�N�`��p�̓_�Q
        U(i,71:80,j) = x6(i,j) + (x7(i,j)-x6(i,j)) * a/9;
    end   
end

figure('Position',[300 300 1000 600])

Hl = line(U(1,:,1),U(i,:,2),U(i,:,3)); hold on % �X�e�B�b�N�`��p�̃I�u�W�F�N�g
Hl = handle(Hl); 
Hl.Color = 'r';

Hp = struct('Point',{ plot3(x1(1,1),x1(1,2),x1(1,3),'ro','MarkerSize',4), ... % �}�[�J�ʒu�`��p�̍\����
                       plot3(x2(1,1),x2(1,2),x2(1,3),'ro','MarkerSize',4), ...
                       plot3(x3(1,1),x3(1,2),x3(1,3),'ro','MarkerSize',4), ...
                       plot3(x4(1,1),x4(1,2),x4(1,3),'ro','MarkerSize',4), ...
                       plot3(x5(1,1),x5(1,2),x5(1,3),'ro','MarkerSize',4), ...
                       plot3(x6(1,1),x6(1,2),x6(1,3),'ro','MarkerSize',4), ...
                       plot3(x7(1,1),x7(1,2),x7(1,3),'ro','MarkerSize',4)});


xlim([0 1.2]); ylim([0 5]); zlim([0.4 1.6]), grid on
xticks([0 0.6 1.2]); yticks([0 1 2 3 4 5]); zticks([0 1 2]);
daspect([1 1 1])

set(gca,'CameraPosition',[-1 3 1.4]) % ���_�̕ύX

for i=1:L
    Hl.XData = U(i,:,1); % �t���[�����ƂɃX�e�B�b�N���X�V
    Hl.YData = U(i,:,2);
    Hl.ZData = U(i,:,3);
    
    for j=1:N
        Hp(j).Point.XData = x(j).Position(i,1); % �t���[�����ƂɃ}�[�J�ʒu���X�V
        Hp(j).Point.YData = x(j).Position(i,2);
        Hp(j).Point.ZData = x(j).Position(i,3);
    end
    
    frame = getframe(gcf);
    writeVideo(v,frame);
    
    pause(0.03)
end

close(v);
