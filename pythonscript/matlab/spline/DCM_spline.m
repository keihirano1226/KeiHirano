% 2012/12/19 �E�c �^��
% DCM���v�Z����
close all; clear; clc; % ������

dt = 1/300;

P0 = [1 0 0; 0 1 0; 0 0 1]; % ��ƂȂ�p���s��
load('P_upper_arm'); % �p���s��̓ǂݍ���

L = length(E.e1(1,:)); % �t���[����
a = 0:L-1;
r = zeros(3,3,L);

for i=1:L
    r(:,:,i) = [E.e1(:,i) E.e2(:,i) E.e3(:,i)]/P0;
end

R = [csapi(dt*a, r(1,1,:)) csapi(dt*a, r(1,2,:)) csapi(dt*a, r(1,3,:));
     csapi(dt*a, r(2,1,:)) csapi(dt*a, r(2,2,:)) csapi(dt*a, r(2,3,:));
     csapi(dt*a, r(3,1,:)) csapi(dt*a, r(3,2,:)) csapi(dt*a, r(3,3,:))];