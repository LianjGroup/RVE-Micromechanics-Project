% Define the file paths and names
inputFilePath = 'steel.txt';
outputFolder = 'RVE_files';
outputFilePrefix = 'RVE';

% Create the output folder if it doesn't exist
if ~isfolder(outputFolder)
    mkdir(outputFolder);
end

% Open the input file for reading
fid = fopen(inputFilePath, 'r');

% Read and split the input file into separate output files
for rveIndex = 1:64
    % Define the output file name
    outputFileName = fullfile(outputFolder, sprintf('%s%d.txt', outputFilePrefix, rveIndex));
    
    % Open the output file for writing
    fout = fopen(outputFileName, 'w');
    
    % Read and write the lines for the current RVE
    for lineIndex = 1:4096
        line = fgetl(fid);  % Read a line from the input file
        fprintf(fout, '%s\n', line);  % Write the line to the output file
    end
    
    % Close the output file
    fclose(fout);
end

% Close the input file
fclose(fid);
