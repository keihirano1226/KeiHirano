% 2012/12/19 Ec ^¬
% DCMðvZ·é
close all; clear; clc; % ú»

dt = 1/300;

P0 = [1 0 0; 0 1 0; 0 0 1]; % îÆÈép¨sñ
load('P_upper_arm'); % p¨sñÌÇÝÝ

L = length(E.e1(1,:)); % t[
a = 0:L-1;
R = zeros(3,3,L);

for i=1:L
    R(:,:,i) = [E.e1(:,i) E.e2(:,i) E.e3(:,i)]/P0;
end