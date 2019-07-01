% 2018/12/13 �E�c �^��
% �ʑ�����Ȃ��o�^�[���[�X�t�B���^
clc; close all; imtool close all; clear; % ������

Fs = 300; % �T���v�����O���g��
Fc = 15; % �Ւf���g��
n = 6; % �t�B���^����
N = 0; % �t�@�C�����������p�ϐ�

InputFileName = '�V�^2���7.csv'; % ���̓t�@�C����
OutputFileName = '�V�^2���7_�t�B���^��.csv'; % �o�̓t�@�C����

x = csvread(InputFileName);
L = length(x(:,1));
[b,a] = butter(n/2,Fc/(Fs/2)); % �o�^�[���[�X�t�B���^�̐݌v
y = filtfilt(b,a,x(1+N:L-N,:));

csvwrite(OutputFileName,y);