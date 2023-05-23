%% Import Script for EBSD Data
%
% This script was automatically created by the import wizard. You should
% run the whoole script or parts of it in order to import your data. There
% is no problem in making any changes to this script.

%% Specify Crystal and Specimen Symmetries

% crystal symmetry
CS = {... 
  'notIndexed',...
  crystalSymmetry('432', [1 1 1], 'mineral', 'Iron fcc', 'color', [0.53 0.81 0.98])};

% plotting convention
setMTEXpref('xAxisDirection','north');
setMTEXpref('zAxisDirection','outOfPlane');

%% Specify File Names

% path to files
pname = '\\home.org.aalto.fi\yadava4\data\Desktop\AScI Desktop\Steel 5 RVEs';

% which files to be imported
fname = [pname '\steel_RVE1.txt'];

%% Import the Data

% create an EBSD variable containing the data
ebsd = EBSD.load(fname,CS,'interface','generic',...
  'ColumnNames', { 'phi1' 'Phi' 'phi2' 'x' 'y' 'z' 'FeatureID' 'PhaseID'}, 'Bunge');

%% Initial analyses - Phase Map.
% Index/Phase analysis.
figure;plot(ebsd,'coordinates','on');

%% Plot grain map
plot(ebsd('Iron fcc'),ebsd('Iron fcc').orientations)

%% Grain reconstruction.
% Consider only indexed & corrected data.
% ebsd_corrected = ebsd(ebsd.mad<1);
ebsdcorri=ebsd('indexed');
ebsd2 = ebsd('Iron fcc');

grainsall = calcGrains(ebsd,'angle',15*degree);

%[grains,ebsdcorri.grainId,ebsdcorri.mis2mean] = calcGrains(ebsdcorri,'angle',15*degree);
