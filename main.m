%% read data
data = readtable('data.csv');

%% The dims in data for visualization
group_values = [0, 1, 2];
time_values = {'time0', 'time1', 'time2', 'time3', 'timepre1', 'timepre2'};

% The names of labels
xLabels = {'G0', 'G1', 'G2'};
yLabels = {'time0', 'time1', 'time2', 'time3', 'timepre1', 'timepre2'};


%% View Parameters
az = 50;
el = 30;

% param of box size
box_factor = 0.7;

%% filter
group = [];
time = [];
value = [];

for i = 1:numel(group_values)
    for j = 1:numel(time_values)
        filtered_data = data.painscore(data.group == group_values(i) & strcmp(data.time, time_values{j}));
        if min(group_values) == 0
            group = [group; repmat(group_values(i)+1, size(filtered_data))];
        else
            group = [group; repmat(group_values(i), size(filtered_data))];
        end
        time = [time; repmat(j, size(filtered_data))];
        value = [value; filtered_data];
    end
end

%% 
xx = value;
g1 = group;
g2 = time;

%% main function
boxPlot3D_(xx, g1, g2, [0 0.25 0.5 0.75 1], box_factor, az, el, xLabels, yLabels)
