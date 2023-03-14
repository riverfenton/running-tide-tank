function [w,H_res] = TF_res(n,L,h)
%n should be a vector representing "mode number"
%n=1 first normal mode number, n=2 second normal mode, etc.
%fractional n represents some amount of phase cancellation
%w is a nonlinearly spaced vector of angular velocities to be used for
%other transfer functions. this is necessary because we can't invert w to
%solve for n in terms on w

g=9.81;

w=sqrt((n*pi*g./L).*tanh(n*pi*h./L));

H_res=1+cos(2*pi*n);%interpolating sinusoidally between peaks

end