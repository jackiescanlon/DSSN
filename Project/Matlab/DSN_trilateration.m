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
r = [25;25];

% find real distances
d(1) = norm(r-p1); 
d(2) = norm(r-p2); 
d(3) = norm(r-p3); 

A_bar = []; B_bar = []; 

for kk = 1:100 % pseudo-monte carlo

%% measurements and processing

% generate measurements
w = 0.001; %standard deviation of gaussian measurement noise
P_real =    @(x) 0.3/(x-13)^2 + 0.003; 
P_meas =    @(x) 0.3/(x-13)^2 + 0.003 + normrnd(0,w); 
P_to_RSSI = @(x) 10*log(x);
RSSI_to_P = @(x) exp(x/10);
meas = zeros(25,3); 
for ii = 1:3
    for jj = 1:25
        dum1 = P_meas(d(ii)); 
        dum2 = P_to_RSSI(dum1); 
        dum3 = round(dum2); 
        dum4 = RSSI_to_P(dum3); 
        meas(jj,ii) = dum4; 
    end
end

% find means
means = [mean(meas(:,1)),mean(meas(:,2)),mean(meas(:,3))];

% estimate distances from means
d_est(1) = 13 + sqrt(0.3/(means(1)-0.003)); 
d_est(2) = 13 + sqrt(0.3/(means(2)-0.003)); 
d_est(3) = 13 + sqrt(0.3/(means(3)-0.003)); 

% truncate distance estimates [20 - d - 50]
for ii = 1:3
    if d_est(ii) > 50
        d_est(ii) = 50; 
    end
    if d_est(ii) < 20
        d_est(ii) = 20; 
    end
end

%% trilateration

q1 = d_est(1)^2 - p1'*p1; 
q2 = d_est(2)^2 - p2'*p2; 
q3 = d_est(3)^2 - p3'*p3;

b = [q1;q2;q3]; 
A = [1, -2*p1';
     1, -2*p2';
     1, -2*p3'];

A_bar = [A_bar;A]; B_bar = [B_bar;b]; 
 
x = inv(A'*A)*A'*b; 

r_est(kk,1) = x(2); 
r_est(kk,2) = x(3); 


end

% doing trilateration on entire data set
x_bar = inv(A_bar'*A_bar)*A_bar'*B_bar; 

%% adding experimental data

% experiment - true positions
exp_true_pos = [20,33;
                33,24;
                12,24;
                28,42;
                17,18;
                17,18;
                17,18;
                17,18];

% experiment - estimated positions
exp_est_pos  = [20.31,26.73;
                25.71,23.39;
                19.94,26.50;
                21.15,26.78;
                21.52,22.54;
                22.81,21.13;
                21.71,20.03;
                11.31,17.05];

% translate to (25,25)
exp_sim_pos = zeros(8,2); 
for ii = 1:8
    for jj = 1:2
        exp_sim_pos(ii,jj) = exp_est_pos(ii,jj) - exp_true_pos(ii,jj) + 25; 
    end
end


%% plot the situation 

figure(1), scatter(p1(1),p1(2),'b'); 
hold on; grid on; xlim([-5,55]); ylim([-5,55]);
xlabel('x (in)'); ylabel('y (in)');
scatter(p2(1),p2(2),'b'); 
scatter(p3(1),p3(2),'b'); 
scatter(r(1),r(2),'*'); 
for kk = 1:100
   scatter(r_est(kk,1),r_est(kk,2),10,'r'); 
end
%scatter(x_bar(2),x_bar(3),50,'r'); 
for kk = 1:8
    scatter(exp_sim_pos(kk,1),exp_sim_pos(kk,2),'k')
end
title('Trilateration Simulation - 100 Runs');
hold off; 