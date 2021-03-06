% 2012/12/19 Ec ^¬
% ÌßÌp¨iûü]·sñsñjðvZ·é
close all; clear; clc; % ú»

dt = 1/300; % TvOüú

load('R_upper_arm'); % DCMÌÇÝÝ

L = length(R(1,1,:)); % t[
a = 0:L-1;

R_dot = zeros(3,3,L);
R_dot2 = zeros(3,3,L);
     
omega = zeros(3,L);
omega_dot = zeros(3,L);

% for i = 1:L-2 % Oi·ª
%     R_dot(:,:,i) = (R(:,:,i+1)-R(:,:,i))/dt;
%     R_dot2(:,:,i) = (R(:,:,i+2) - 2*R(:,:,i+1) + R(:,:,i))/(dt^2);
%     Temp1 = R_dot(:,:,i) * R(:,:,i).';
%     Temp2 = R_dot2(:,:,i) * R(:,:,i).' + R_dot(:,:,i)*R_dot(:,:,i).';
%         
%     omega(1,i) = (Temp1(3,2) - Temp1(2,3))/2;
%     omega(2,i) = (Temp1(1,3) - Temp1(3,1))/2;
%     omega(3,i) = (Temp1(2,1) - Temp1(1,2))/2;
%     
%     omega_dot(1,i) = (Temp2(3,2) - Temp2(2,3))/2;
%     omega_dot(2,i) = (Temp2(1,3) - Temp2(3,1))/2;
%     omega_dot(3,i) = (Temp2(2,1) - Temp2(1,2))/2;      
% end

% for i=2:L-1 % ·ª
%     R_dot(:,:,i) = (R(:,:,i+1)-R(:,:,i-1))/(2*dt);
%     R_dot2(:,:,i) = (R(:,:,i+1) - 2*R(:,:,i) + R(:,:,i-1))/(dt^2);
%     Temp1 = R_dot(:,:,i) * R(:,:,i).';
%     Temp2 = R_dot2(:,:,i) * R(:,:,i).' + R_dot(:,:,i)*R_dot(:,:,i).';
%     
%     omega(1,i) = (Temp1(3,2) - Temp1(2,3))/2;
%     omega(2,i) = (Temp1(1,3) - Temp1(3,1))/2;
%     omega(3,i) = (Temp1(2,1) - Temp1(1,2))/2;
%     
%     omega_dot(1,i) = (Temp2(3,2) - Temp2(2,3))/2;
%     omega_dot(2,i) = (Temp2(1,3) - Temp2(3,1))/2;
%     omega_dot(3,i) = (Temp2(2,1) - Temp2(1,2))/2;
% end

% for i=3:L-2 % 5_ß1
%     R_dot(:,:,i) = (-R(:,:,i+2) + 8*R(:,:,i+1) - 8*R(:,:,i-1) + R(:,:,i-2))/(12*dt);
%     R_dot2(:,:,i) = (-R(:,:,i+2) + 16*R(:,:,i+1) - 30*R(:,:,i) + 16*R(:,:,i-1) - R(:,:,i-2))/(12*dt^2);
%     Temp1 = R_dot(:,:,i) * R(:,:,i).';
%     Temp2 = R_dot2(:,:,i) * R(:,:,i).' + R_dot(:,:,i)*R_dot(:,:,i).';
%     
%     omega(1,i) = (Temp1(3,2) - Temp1(2,3))/2;
%     omega(2,i) = (Temp1(1,3) - Temp1(3,1))/2;
%     omega(3,i) = (Temp1(2,1) - Temp1(1,2))/2;
%     
%     omega_dot(1,i) = (Temp2(3,2) - Temp2(2,3))/2;
%     omega_dot(2,i) = (Temp2(1,3) - Temp2(3,1))/2;
%     omega_dot(3,i) = (Temp2(2,1) - Temp2(1,2))/2;
% end

for i=3:L-2 % 5_ß2
    R_dot(:,:,i) = (-R(:,:,i+2) + 8*R(:,:,i+1) - 8*R(:,:,i-1) + R(:,:,i-2))/(12*dt);
    Temp1 = R_dot(:,:,i) * R(:,:,i).';
    
    omega(1,i) = (Temp1(3,2) - Temp1(2,3))/2;
    omega(2,i) = (Temp1(1,3) - Temp1(3,1))/2;
    omega(3,i) = (Temp1(2,1) - Temp1(1,2))/2;
end

for i=5:L-4
    omega_dot(:,i) = (-omega(:,i+2) + 8*omega(:,i+1) - 8*omega(:,i-1) + omega(:,i-2))/(12*dt);
end

csvwrite('V^2ñÚãrp¬x.csv', omega.');
csvwrite('V^2ñÚãrpÁ¬x.csv', omega_dot.');