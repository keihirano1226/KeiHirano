% 2012/12/19 �E�c �^��
% DCM���v�Z����
close all; clear; clc; % ������

dt = 1/300;

P0 = [1 0 0; 0 1 0; 0 0 1]; % ��ƂȂ�p���s��
load('P_upper_arm'); % �p���s��̓ǂݍ���

L = length(E.e1(1,:)); % �t���[����
a = 0:L-1;
R = zeros(3,3,L);

for i=1:L
    R(:,:,i) = [E.e1(:,i) E.e2(:,i) E.e3(:,i)]/P0;
end