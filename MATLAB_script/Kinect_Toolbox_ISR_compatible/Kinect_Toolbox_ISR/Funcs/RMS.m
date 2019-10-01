% compute RMS of a vector 1xN or Nx1
% if input has a second term 'num', the best and and worst 'num'
%  values will be left out

function [out]=RMS(in,num)
if ~exist('num','var')
  num=0;
end
aux=sort(in);
aux=aux(num+1:end-num);
out=sqrt(sum(aux.^2)/numel(aux));