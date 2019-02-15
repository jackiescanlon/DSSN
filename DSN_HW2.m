% Paul McKee
% Distributed Systems and Sensor Networks
% HW2 
% 2/11/19

clear all; close all; clc; 

%% part A - plot data 

% load data
run DSN_HW2_data.m

figure(1), scatter(nodes(:,2),nodes(:,3)); 
hold on; 
title('locations of nodes'); 

%% part B - unit distance graph 

% connectivity range of 2, plot all connections 

b_check = 1; 

if b_check == 1
for ii = 1:64 % for each node
    
    xo = nodes(ii,2); yo = nodes(ii,3); 
    
    for jj = 1:64
        if ii ~= jj % for each other node
            
            x = nodes(jj,2); y = nodes(jj,3); 
            dist = sqrt((x-xo)^2 + (y-yo)^2); % calculate distance
            
            if dist <= 2
                plot([xo,x],[yo,y],'b'); % plot line 
            end
        end
        pause(0.001); 
    end
end

title('connectivity graph'); 
hold off; 
disp('done!'); 

else
    hold off; 
end

%% part D - test Dijkstra and Greedy for 50 random pairs 


%s = 25; d = 26; 
%[dir_dist_d, numhops_d, path_dist_d,E_dir_d, E_path_d] = dijkstra(s,d,nodes);
%[dir_dist_g, numhops_g, path_dist_g,E_dir_g, E_path_g,deadend] = greedy(s,d,nodes);


% generate 50 random sources, destinations & run both algorithms
dir_dist_d = zeros(50,1); numhops_d = zeros(50,1); path_dist_d = zeros(50,1); 
dir_dist_g = zeros(50,1); numhops_g = zeros(50,1); path_dist_g = zeros(50,1); 
deadend = zeros(50,1); 
for ii = 1:50
    
    % generate random source, destination
    d = randi(64,1); 
    s = randi(64,1); 
    if d == s
        s = randi(64,1); 
    end
    
    % run both algorithms 
    [dir_dist_d(ii), numhops_d(ii), path_dist_d(ii),E_dir_d(ii), E_path_d(ii)] = dijkstra(s,d,nodes);
    [dir_dist_g(ii), numhops_g(ii), path_dist_g(ii),E_dir_g(ii), E_path_g(ii),deadend(ii)] = greedy(s,d,nodes);
    
end

% process dijkstra data 
for jj = 1:50 
    num_hops_per_dist_d(jj) = numhops_d(jj)/dir_dist_d(jj); 
    path_dist_over_dir_dist_d(jj) = path_dist_d(jj)/dir_dist_d(jj); 
end
A_d = mean(num_hops_per_dist_d); % first metric we're asked for
B_d = mean(path_dist_over_dir_dist_d); % second metric we're asked for

% process greedy data
num_deadends = 0; 
E_path_g_processed = []; E_dir_g_processed = []; 
for jj = 1:50 
    if deadend(jj) == 0 % not a dead end
        num_hops_per_dist_g(jj) = numhops_g(jj)/dir_dist_g(jj); 
        path_dist_over_dir_dist_g(jj) = path_dist_g(jj)/dir_dist_g(jj); 
        E_path_g_processed = [E_path_g_processed;E_path_g(jj)]; 
        E_dir_g_processed = [E_dir_g_processed;E_dir_g(jj)]; 
    else
        num_deadends = num_deadends + 1; 
    end
end
A_g = mean(num_hops_per_dist_g); % first metric we're asked for
B_g = mean(path_dist_over_dir_dist_g); % second metric we're asked for 
C_g = 100 - 100*(num_deadends/50); % probability of success

% part E - compare energy of direct transmit to path transmit 
dummy_array = 1:50; 
figure(4), plot(dummy_array,E_dir_d,'o',dummy_array,E_path_d,'ro'); 
hold on; grid on; 
xlabel('trial number'); ylabel('energy'); title('Dijkstra energy analysis');
legend('direct transmission energy','path energy'); 
hold off; 

dummy_array = 1:(50 - nnz(deadend)); 
figure(5), plot(dummy_array,E_dir_g_processed,'o',dummy_array,E_path_g_processed,'ro'); 
hold on; grid on; 
xlabel('trial number'); ylabel('energy'); title('Greedy energy analysis');
legend('direct transmission energy','path energy'); 
hold off; 


%% Dijkstra's algorithm

function [dir_dist, numhops, path_dist,E_dir, E_path] = dijkstra(s,d,nodes) 

% quick change
s = nodes(s,1:3); d = nodes(d,1:3); 

% plot
figure(2), scatter(nodes(:,2),nodes(:,3)); 
hold on; 
scatter([s(2),d(2)],[s(3),d(3)],'r'); 
title('Dijkstra'); 

% find direct distance s to d
xs = s(2); ys = s(3); xd = d(2); yd = d(3); 
dir_dist = sqrt((xd-xs)^2 + (yd-ys)^2);
E_dir = dir_dist^2; 
E_path = 0; % will be updated

% table consists of (node ID)(best dist. from source)(prev. node)
table = zeros(64,3); 
table(:,1) = nodes(:,1); table(:,2) = 100; 

% setup 
atdest = 0; 
n = s; 
table(n(1),2) = 0; table(n(1),3) = n(1); 
explored_nodes = [];

while(~atdest)
    
    % test for at-destination
    if n(1) == d(1)
        %disp('at destination!'); 
        break; 
    end
    
    % update explored nodes
    explored_nodes = [explored_nodes, n(1)]; 
    
    % find all nodes within range of current node n
    xo = n(2); yo = n(3); 
    for ii = 1:64 % for all nodes
        x = nodes(ii,2); y = nodes(ii,3); 
        dist = sqrt((x-xo)^2 + (y-yo)^2); % calculate distance 
        if dist <= 2 % test if within range         
            % update node distance if this is a shorter path than was there
            if (dist + table(n(1),2)) < table(ii,2)
                table(ii,2) = dist + table(n(1),2);
                table(ii,3) = n(1); 
            end
        end
    end 
    
    % choose next node to go to (consult table -> lowest cost, unexplored)
    [a,b] = sort(table); % rearrange table by path length (low to hi) 
    decision_table = [b(:,2),a(:,2)]; % keep indexes with paths
    
    for jj = 1:64 
        if ~ismember(decision_table(jj,1),explored_nodes)
        %disp('now going to node'); 
        %disp(decision_table(jj,1)); 
        n_new = nodes(decision_table(jj,1),1:3); 
        break; 
        end
    end
    
    % update
    n = n_new;

end

% extract optimal path from table we've created
p = d(1);
final_path = [p]; 

for ii = 1:64
    q = table(p,3); 
    final_path = [final_path;q];
    p = q; 
    if p == s(1)
        break;
    end
end
final_path = flipud(final_path); 

numhops = length(final_path)-1; 

% plot optimal path 
xo = s(2); yo = s(3); 
path_dist = 0; 
for jj = 2:numhops+1
    x = nodes(final_path(jj),2); 
    y = nodes(final_path(jj),3); 
    plot([xo,x],[yo,y],'b'); % plot line
    dist = sqrt((x-xo)^2 + (y-yo)^2);
    path_dist = path_dist + dist; 
    E_path = E_path + dist^2; 
    xo = x; yo = y; 
    pause(0.5); 
end
hold off; 

end

%% Greedy routing

function [dir_dist, numhops, path_dist,E_dir, E_path, deadend] = greedy(s,d,nodes) 

deadend = 0; 

% quick change
s = nodes(s,1:3); d = nodes(d,1:3);

% plot
figure(3), scatter(nodes(:,2),nodes(:,3)); 
hold on; 
scatter([s(2),d(2)],[s(3),d(3)],'r'); 
title('Greedy'); 

% find direct distance s to d
xs = s(2); ys = s(3); xd = d(2); yd = d(3); 
dir_dist = sqrt((xd-xs)^2 + (yd-ys)^2);
E_dir = dir_dist^2;
E_path = 0; % will be updated 

path = [1]; % will contain node indeces of path taken
path_dist = 0; 
numhops = 0; % will keep track of number of hops
xd = d(2); yd = d(3); % destination location
atdest = 0; % 0 unless done
n = s(2:3); % initialize

while(~atdest)
    
    % test for at-destination
    xo = n(1); yo = n(2);
    h_current = sqrt((xo-xd)^2 + (yo-yd)^2);
    if h_current == 0
        atdest = 1; 
        disp('at destination!'); 
        break; 
    end
    
    h = zeros(64,1)+1000; % initialize all as high (will be lower later)
    
    for ii = 1:64 % for all nodes
        x = nodes(ii,2); y = nodes(ii,3); 
        dist = sqrt((x-xo)^2 + (y-yo)^2); % calculate distance 
        if dist <= 2 % test if within range
            h(ii) = sqrt((x-xd)^2 + (y-yd)^2); % calculate distance to destination
        end
    end 
    
    [h_min, best_next] = min(h); % best next node
    if h_min == h_current && atdest == 0 % we are at a cliff, no closer nodes
        disp('we are at a cliff, no closer nodes'); 
        deadend = 1; 
        break; 
    end
    
    % update 
    numhops = numhops+1; 
    path = [path, best_next]; 
    n = nodes(best_next,2:3); 
    
    % plot 
    plot([xo,n(1)],[yo,n(2)],'b');
    dist = sqrt((x-xo)^2 + (y-yo)^2);
    path_dist = path_dist + dist; 
    E_path = E_path + dist^2; 
    pause(0.5); 
    
end
    
hold off; 

end