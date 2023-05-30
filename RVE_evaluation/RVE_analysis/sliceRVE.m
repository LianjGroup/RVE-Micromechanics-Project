%% Use this file first to break down the RVE into its layers. Convert 3D RVE to 2D data.
% create 100 txt files for 100 layers

% add the RVE filename here
filename = "steel_RVE5.txt";
lines = readlines(filename);
%lines(1:2500)
%lines(2502)
% from 1 to 2500 --> 1st layer, 2501 to 5000 --> 2nd layer, ...

% outer for loop 50 times for 50 layers

for i=1:100
    i
    index = num2str(i);
    a = 'layer';
    b = '_RVE5.txt';
    filename2 = [a index b];
    fid = fopen(filename2, 'w');
    % inner for loop 2500 times
    for j=(1 + (i-1)*10000):(10000 + (i-1)*10000)
        fprintf(fid, lines(j)+'\n'); 
    end
fclose(fid);
end


%fid = fopen('layer1.txt', 'w');

%i= 1;



