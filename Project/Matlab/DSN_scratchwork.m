% Paul McKee
% DSSN Project Scratchwork 
% 3/19/19

clear all; close all; clc; 

p1 = [0;0;0];
p2 = [10;0;0];
p3 = [0;10;0];
p4 = [0;0;10];

r = [1;2;3];

d1_vec = norm(r-p1); d1 = norm(d1_vec)
d2_vec = norm(r-p2); d2 = norm(d2_vec) 
d3_vec = norm(r-p3); d3 = norm(d3_vec) 
d4_vec = norm(r-p4); d4 = norm(d4_vec) 

%% processing RSSI Data

data = [20, -37, -35, -38; 
        30, -40, -38, -43;
        50, -50, -49, -51;
        100, -55, -53, -58;
        150, -66.2, -61, -74; 
        200, -59.4, -54, -62;
        200, -54.5, -54, -56;
        250, -60.3, -59, -63;
        250, -58.8, -57, -61;
        100, -54.4, -51, -61;
        75, -57.2, -52, -61; 
        125, -63.5, -53, -79];
    
figure(1), scatter(data(:,1),data(:,2),'r'); 
hold on; grid on; 
xlabel('distance (inches'); 
ylabel('RSSI (units)'); 
%scatter(data(:,1),data(:,3),'b'); 
%scatter(data(:,1),data(:,4),'b'); 
hold off; 

data_new = zeros(size(data)); 
for ii = 1:max(size(data)) % undo decibel conversion
    data_new(ii,1) = data(ii,1); 
    data_new(ii,2) = 10^(-data(ii,2)/20);
    data_new(ii,3) = 10^(-data(ii,3)/20);
    data_new(ii,4) = 10^(-data(ii,4)/20);
end

figure(2), scatter(data_new(:,1),data_new(:,2),'r'); 
hold on; grid on; 
xlabel('distance (inches'); 
ylabel('RSSI (units)'); 
%scatter(data_new(:,1),data_new(:,3),'b'); 
%scatter(data_new(:,1),data_new(:,4),'b'); 
hold off; 

% linear curve fit to non-decibel data
B = data_new(:,2);
A = [data_new(:,1) , ones(max(size(data)),1)]; 
x = inv(A'*A)*A'*B; 

f = @(input) x(1)*input + x(2); 
dum = linspace(0,250,100); 
f_array = f(dum); 

figure(3), scatter(data_new(:,1),data_new(:,2),'r')
hold on; grid on; 
xlabel('distance (inches'); 
ylabel('RSSI (units)'); 
plot(dum,f_array,'b'); 
legend('data','best fit line'); 
hold off; 

% this is atrocious
% let's try 1/x^2 fitting to raw data

g1 = 500; g2 = -60; % <-- these numbers found by guess-and-check 
g = @(input) g1./(input) + g2; 
g_array = g(dum); 

figure(4), scatter(data(:,1),data(:,2),'r')
hold on; grid on; 
xlabel('distance (inches'); 
ylabel('RSSI (units)'); 
plot(dum,g_array,'b'); 
legend('data','best fit line'); 
xlim([0,250]); ylim([-100,0]); 
hold off; 

%% new work - week of 3/27/19 

clear all; close all; clc; 

% read data from file
A = csvread('DSSN_RSSI_data.csv',4,0,[4 0 228 2]); % tailored to data file 
dist = A(:,1); 
RSSI = A(:,2); 
P2 = A(:,3); 

% processing
distances = [20,30,40,50,60,70,80,90,100];
RSSI_means = [mean(RSSI(1:25)),mean(RSSI(26:50)),mean(RSSI(51:75))...
    mean(RSSI(76:100)),mean(RSSI(101:125)),mean(RSSI(126:151)),...
    mean(RSSI(151:176)),mean(RSSI(176:200)),mean(RSSI(201:225))];
RSSI_meds = [median(RSSI(1:25)),median(RSSI(26:50)),median(RSSI(51:75))...
    median(RSSI(76:100)),median(RSSI(101:125)),median(RSSI(126:151)),...
    median(RSSI(151:176)),median(RSSI(176:200)),median(RSSI(201:225))];

P2_means = [mean(P2(1:25)),mean(P2(26:50)),mean(P2(51:75))...
    mean(P2(76:100)),mean(P2(101:125)),mean(P2(126:151)),...
    mean(P2(151:176)),mean(P2(176:200)),mean(P2(201:225))];
P2_meds = [median(P2(1:25)),median(P2(26:50)),median(P2(51:75))...
    median(P2(76:100)),median(P2(101:125)),median(P2(126:151)),...
    median(P2(151:176)),median(P2(176:200)),median(P2(201:225))];
P2_std = [std(P2(1:25)),std(P2(26:50)),std(P2(51:75))...
    std(P2(76:100)),std(P2(101:125)),std(P2(126:151)),...
    std(P2(151:176)),std(P2(176:200)),std(P2(201:225))];

% curve fitting to P2
dum = linspace(0,100,1000); 
g1 = 0.3; g2 = 0.003; % <-- these numbers found by guess-and-check 
g = @(x) g1./(x-13).^2 + g2; 
g_array = g(dum); 

%plotting
figure(1), scatter(dist,RSSI,'r'); 
hold on; grid on; 
xlabel('distance (inches)'); 
ylabel('RSSI (dB)'); 
scatter(distances,RSSI_means,'b'); 
%scatter(distances,RSSI_meds,'g'); 
xlim([19,101]); 
title('RSSI Measurements at Varying Distances'); 
hold off; 

figure(2), scatter(dist,P2,'r'); 
hold on; grid on; 
xlabel('distance (inches)'); 
ylabel('P2/P1'); 
scatter(distances,P2_means,'b'); 
%scatter(distances,P2_meds,'g'); 
plot(dum,g_array,'b'); 
xlim([19,51]); ylim([0,0.012]); 
title('Power Ratio Curve Fitting');
hold off; 

% inverse curve 
f = @(p) 13 + sqrt(0.3./(p - 0.003));
dum2 = linspace(0.003,0.01,100); 
f_array = f(dum2); 

figure(3), scatter(P2,dist,'r'); 
hold on; grid on; 
xlabel('received signal power'); 
ylabel('distance estimate (in)');
scatter(P2_means,distances,'b'); 
scatter(P2_meds,distances,'g'); 
plot(dum2,f_array); 
xlim([0,0.012]); ylim([19,51]);
hold off; 

%% trying to recreate data from measurement model - succeeded 

w = 0.001; %standard deviation of gaussian measurement noise
P_real = @(d) 0.3/(d-13)^2 + 0.003; 
P_meas = @(d) 0.3/(d-13)^2 + 0.003 + normrnd(0,w); 
P_to_RSSI = @(x) 10*log(x);
RSSI_to_P = @(x) exp(x/10);
d = 30; 

% calculate some measurements
meas_bogus = zeros(1,25); 
dum_bogus = zeros(1,25)+d; 
for ii = 1:25 
    dum1 = P_meas(d); 
    dum2 = P_to_RSSI(dum1); 
    dum3 = round(dum2); 
    dum4 = RSSI_to_P(dum3); 
    meas_bogus(ii) = dum4; 
end
mean_bogus = mean(meas_bogus); 
med_bogus = median(meas_bogus);

figure(4), scatter(dum_bogus,meas_bogus,'r'); 
hold on; grid on; 
xlabel('distance (inches)'); 
ylabel('P2 (units)'); 
scatter(d,mean_bogus,'g'); 
scatter(d,med_bogus,'b'); 
scatter(d,P_real(d),'k*'); 
xlim([19,51]); ylim([0,0.012]); 
hold off; 
    