%% Import Script for EBSD Data -->  z = 1 plane
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
fname = [pname '\steel_RVE1_2D.txt'];

%% Import the Data

% create an EBSD variable containing the data
ebsd = EBSD.load(fname,CS,'interface','generic',...
  'ColumnNames', { 'phi1' 'Phi' 'phi2' 'x' 'y' 'FeatureID' 'Phase'}, 'Columns', [1 2 3 4 5 7 8], 'Bunge');
%% Initial analyses - Phase Map.
% Index/Phase analysis.
figure;plot(ebsd,'coordinates','on');

%% Plot grain map
plot(ebsd('Iron fcc'),ebsd('Iron fcc').orientations)

%% Grain reconstruction.
% Consider only indexed & corrected data.
% ebsd_corrected = ebsd(ebsd.mad<1);
ebsdcorri=ebsd('indexed');
%ebsd2 = ebsd('Iron fcc');

[grains,ebsdcorri.grainId,ebsdcorri.mis2mean] = calcGrains(ebsdcorri,'angle',15*degree);
initialGrainNr = length(grains); % check number of initial grains after first reconstruction

% delete the very small grains which might be caused by the measurement error
ebsdcorri(grains(grains.grainSize < 2)) = []; % delete grains w only 1 or 2 measurement points

% redo grain segmentation
[grains, ebsdcorri.grainId] = calcGrains(ebsdcorri, 'angle', 15*degree); % set grain boundary as 15 deg

% pick up the focused phase
grainsIronfcc = grains('Iron fcc');
totalGrainNr = length(grainsIronfcc); % check the number of tot grains of the focused phase
% totGrainNr = 96

%% Plot the EBSD orientation map

ipfKey = ipfColorKey(ebsd('Iron fcc'));
ipfKey.inversePoleFigureDirection = vector3d.Z;
colors = ipfKey.orientation2color...
    (grainsIronfcc.meanOrientation); % set the orientation map color

figure; 
plot(grainsIronfcc, colors) % plot grain map w grain mean orientation

%% Grain size & shape data analyses
% Find the boundary grains
outerBoundary_id = any(grainsIronfcc.boundary.grainId==0, 2);
grain_id = grainsIronfcc.boundary(outerBoundary_id).grainId;
grain_id(grain_id==0) = [];

% Plot the boundary grains with their mean orientations
figure; plot(grainsIronfcc(grain_id), grainsIronfcc(grain_id).meanOrientation);

% Remove the boundary grains
grainsIronfcc(grain_id) = [];
innerGrainNr = length(grainsIronfcc);

%Plot the inner grains with their mean orientations
figure; plot(grainsIronfcc, grainsIronfcc.meanOrientation);


%% fit and plot the equivalent ellipses of grains
[GrainfitEangle, GrainfitElongA, GrainfitEshortb] = fitEllipse(grainsIronfcc);

%Extract grains data
Grainarea = grainsIronfcc.area;
GraineqR = grainsIronfcc.equivalentRadius;
GraineqD = GraineqR*2; % equivalent diameter
Grainasp = 1./grainsIronfcc.aspectRatio; %shape factor: aspect ratio

%Plot fitted ellipses
figure;
plot(grainsIronfcc, grainsIronfcc.meanOrientation, 'linewidth', 1);
hold on;
plotEllipse(grainsIronfcc.centroid, GrainfitElongA, GrainfitEshortb, ...
    GrainfitEangle, 'lineColor', 'b');
hold off;