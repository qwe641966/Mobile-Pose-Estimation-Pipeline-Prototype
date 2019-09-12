mse_data = load('mse_data.mat');
mse_data = mse_data.value;

names = mse_data(:,24);

filename = sprintf('results/IMG_%d/final_match_array_direct.txt', names(1));
importdata(filename);