function H=TF_tank(w,h)
%v=sqrt(9.81*h); %v is not constant for all freq
g=9.81;
k=(w.^2)/g; % see below

%calculation goes
% for sinusoid, phase velocity c= w/k. in deepwater,c=sqrt(g/k)
%so w=k*sqrt(g/k) ---> k=w^2/g

num = (4.*sinh(k.*h)).*(k.*h.*sinh(k.*h)-cosh(k.*h)+1);
den = k.*h.*(sinh(2.*k.*h)+2.*k.*h);
H = num./den;
end