% Paul McKee
% DSN Trilateration Sim 
% 4/2/19

clear all; close all; clc; 

%% Problem Setup 

% "tower" locations
p1 = [0;0];
p2 = [50;0];
p3 = [0;50]; 
c = [50;50];

% target location (must be in safety diamond)
r = [34;26];

% find real distances
d(1) = norm(r-p1); 
d(2) = norm(r-p2); 
d(3) = norm(r-p3);

%% measurements and processing

% generate measurements
w = 0.001; %standard deviation of gaussian measurement noise
p_real =    @(x) 0.3/(x-13)^2 + 0.003; 
p_meas =    @(x) 0.3/(x-13)^2 + 0.003 + normrnd(0,w); 
p_to_RSSI = @(x) 10*log(x);
RSSI_to_p = @(x) exp(x/10);
meas = zeros(25,3); 
for ii = 1:3
    for jj = 1:25
        dum1 = p_meas(d(ii)); 
        dum2 = p_to_RSSI(dum1); 
        dum3 = round(dum2); 
        dum4 = RSSI_to_p(dum3); 
        meas(jj,ii) = dum4; 
    end
end

% find means
means = [mean(meas(:,1)),mean(meas(:,2)),mean(meas(:,3))];

% estimate distances from means, truncate [20 - d - 50]
d_est = zeros(3,1);
for ii = 1:3
    d_est(ii) = 13 + sqrt(0.3/(means(ii)-0.003)); 
    if d_est(ii) > 50
        d_est(ii) = 50; 
    end
    if d_est(ii) < 20
        d_est(ii) = 20; 
    end
end

%% initial trilateration

q1 = d_est(1)^2 - p1'*p1; 
q2 = d_est(2)^2 - p2'*p2; 
q3 = d_est(3)^2 - p3'*p3;

b = [q1;q2;q3]; 
A = [1, -2*p1';
     1, -2*p2';
     1, -2*p3'];
 
x = inv(A'*A)*A'*b; 

r_est(1) = x(2); 
r_est(2) = x(3); 


%% r0, P0

sig_d = 300; % tuning parameter 
R = sig_d^2*eye(3);

r0 = r_est'; 
H0 = [(r0-2*p1)';(r0-2*p2)';(r0-2*p3)'];
P0 = inv(H0'*inv(R)*H0);

% from P0 calculate ellipse parameters and plot 
[P_evec,P_eval] = eig(P0); 

semimaj = P_eval(1,1); 
semimin = P_eval(2,2); 
semimaj_ang = atan2(P_evec(2,1),P_evec(1,1)); 

x1 = r0(1) + semimaj*cos(semimaj_ang); 
y1 = r0(2) + semimaj*sin(semimaj_ang); 
x2 = r0(1) + semimaj*cos(semimaj_ang + pi); 
y2 = r0(2) + semimaj*cos(semimaj_ang + pi); 

ecc = sqrt(1-(semimin/semimaj)^2);

% ellipse plotting from MATLAB help site
 a = 1/2*sqrt((x2-x1)^2+(y2-y1)^2);
 b = a*sqrt(1-ecc^2);
 t = linspace(0,2*pi);
 X = a*cos(t);
 Y = b*sin(t);
 w = atan2(y2-y1,x2-x1);
 x = (x1+x2)/2 + X*cos(w) - Y*sin(w);
 y = (y1+y2)/2 + X*sin(w) + Y*cos(w);
 figure(1), plot(x,y,'r-')
hold on; grid on; 
xlim([-5,55]); ylim([-5,55]);
xlabel('x (in)'); ylabel('y (in)'); 
scatter(p1(1),p1(2),'b'); 
scatter(p2(1),p2(2),'b'); 
scatter(p3(1),p3(2),'b'); 
scatter(r(1),r(2),'k*'); 
scatter(r0(1),r0(2),'r'); 
title('Kalman Filter Estiate k = 0'); 
hold off;

%% time t_k

rk = r0; 
Pk = P0; 

for k = 1:10

% generate measurements
w = 0.001; %standard deviation of gaussian measurement noise
meas = zeros(25,3); 
for ii = 1:3
    for jj = 1:25
        dum1 = p_meas(d(ii)); 
        dum2 = p_to_RSSI(dum1); 
        dum3 = round(dum2); 
        dum4 = RSSI_to_p(dum3); 
        meas(jj,ii) = dum4; 
    end
end

% find means
means = [mean(meas(:,1)),mean(meas(:,2)),mean(meas(:,3))];

% estimate distances from means, truncate [20 - d - 50]
d_est = zeros(3,1);
for ii = 1:3
    d_est(ii) = 13 + sqrt(0.3/(means(ii)-0.003)); 
    if d_est(ii) > 50
        d_est(ii) = 50; 
    end
    if d_est(ii) < 20
        d_est(ii) = 20; 
    end
end

% KF updates
Hk = [(rk-2*p1)';(rk-2*p2)';(rk-2*p3)']; 
Kk = Pk*Hk'*inv(Hk*Pk*Hk' + R); 

disp(Kk); 

rk_new = rk + 100*Kk*(d_est - [norm(rk-p1);norm(rk-p2);norm(rk-p3)]);
Pk_new = (eye(2) - Kk*Hk)*Pk*(eye(2) - Kk*Hk)' + Kk*R*Kk'; 

rk = rk_new; 
Pk = Pk_new;

disp(rk); 

% from Pk calculate ellipse parameters and plot 
[P_evec,P_eval] = eig(Pk); 

semimaj = P_eval(1,1); 
semimin = P_eval(2,2); 
semimaj_ang = atan2(P_evec(2,1),P_evec(1,1)); 

x1 = rk(1) + semimaj*cos(semimaj_ang); 
y1 = rk(2) + semimaj*sin(semimaj_ang); 
x2 = rk(1) + semimaj*cos(semimaj_ang + pi); 
y2 = rk(2) + semimaj*cos(semimaj_ang + pi); 

ecc = sqrt(1-(semimin/semimaj)^2);

% ellipse plotting from MATLAB
a = 1/2*sqrt((x2-x1)^2+(y2-y1)^2);
b = a*sqrt(1-ecc^2);
t = linspace(0,2*pi);
X = a*cos(t);
Y = b*sin(t);
w = atan2(y2-y1,x2-x1);
x = (x1+x2)/2 + X*cos(w) - Y*sin(w);
y = (y1+y2)/2 + X*sin(w) + Y*cos(w);
figure(2), plot(x,y,'r-')
hold on; grid on; 
xlim([-5,55]); ylim([-5,55]);
xlabel('x (in)'); ylabel('y (in)'); 
scatter(p1(1),p1(2),'b'); 
scatter(p2(1),p2(2),'b'); 
scatter(p3(1),p3(2),'b'); 
scatter(r(1),r(2),'k*'); 
scatter(rk(1),rk(2),'r'); 
title('Kalman Filter Estiate k = 10'); 
hold off;


pause(1); 

end