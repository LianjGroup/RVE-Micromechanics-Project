%% Import Script for EBSD Data
%
% This script was automatically created by the import wizard. You should
% run the whoole script or parts of it in order to import your data. There
% is no problem in making any changes to this script.

%% Specify Crystal and Specimen Symmetries

% crystal symmetry
%CS = {... 
%  'notIndexed',...
%  crystalSymmetry('432', [2.9 2.9 2.9], 'mineral', 'Iron - Alpha', 'color', [0.53 0.81 0.98]),...
%  crystalSymmetry('432', [3.6 3.6 3.6], 'mineral', 'Iron - Gamma', 'color', [0.56 0.74 0.56])};

CS = {... 
  'notIndexed',...
  crystalSymmetry('m-3m', [3.7 3.7 3.7], 'mineral', 'Iron fcc', 'color', [0.53 0.81 0.98]),...
  crystalSymmetry('m-3m', [2.9 2.9 2.9], 'mineral', 'Iron bcc (old)', 'color', [0.56 0.74 0.56])};

% plotting convention
setMTEXpref('xAxisDirection','north');
setMTEXpref('zAxisDirection','outOfPlane');

%% Specify File Names

% path to files
pname = 'C:\Users\yadava4\Downloads';

% which files to be imported
fname = [pname '\439_cropped_rot_93@ND_Mod.ang'];

%% Import the Data

% create an EBSD variable containing the data
ebsd = EBSD.load(fname,CS,'interface','ang',...
  'convertEuler2SpatialReferenceFrame','setting 2');

%% Initial analyses - Phase Map.
% Index/Phase analysis.
figure;plot(ebsd,'coordinates','on');

%% Grain reconstruction.
% Consider only indexed & corrected data.
% ebsd_corrected = ebsd(ebsd.mad<1);
ebsdcorri=ebsd('indexed');
% Reconstruct the grain structure.
[grains,ebsdcorri.grainId,ebsdcorri.mis2mean] = calcGrains(ebsdcorri,'angle',15*degree);
%[grains,ebsd.grainId,ebsd.mis2mean] = calcGrains(ebsd,'angle',15*degree);
plot(grains)
initialGrainNr=length(grains);

% delete the very small grains which might be caused by the measurement error
ebsdcorri(grains(grains.grainSize < 2)) = []; % delete grains w only 1 or 2 measurement points

% redo grain segmentation
[grains, ebsdcorri.grainId] = calcGrains(ebsdcorri, 'angle', 15*degree); % set grain boundary as 15 deg

% pick up the focused phase
grainsIronfcc = grains('Iron fcc');
grainsIronbcc = grains('Iron bcc (old)');
totalGrainNr = length(grainsIronfcc); % check the number of tot grains of the focused phase
% totGrainNr = 30218

IronbccGrainNr = length(grainsIronbcc);

%% Plot the EBSD orientation map

ipfKey = ipfColorKey(ebsd('Iron fcc'));
ipfKey.inversePoleFigureDirection = vector3d.Z;
colors = ipfKey.orientation2color...
    (grainsIronfcc.meanOrientation); % set the orientation map color

figure; 
plot(grainsIronfcc, colors) % plot grain map w grain mean orientation

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

avgshape = mean(Grainasp)
avgsize = mean(GraineqD)
