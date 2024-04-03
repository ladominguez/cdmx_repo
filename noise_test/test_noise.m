clear all
close all

N = 60000;

X1 = 5*randn(N,1);
X2 = 15*randn(N,1);
dX = X1 - X2;


rms_X1 = rms(X1);
rms_X2 = rms(X2);
rms_dX = rms(dX);

rms_dx_Theo = sqrt(rms_X1^2 + rms_X2^2) 