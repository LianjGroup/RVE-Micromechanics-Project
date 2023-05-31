import sys
import json
import os
import numpy as np
import pandas as pd
import glob
from prettytable import PrettyTable

def printLog(message, logPath):
    with open(logPath, 'a+') as logFile:
        logFile.writelines(message)
    print(message)

def replace_outputPath_json(json_file_path, output_path):
    # Read JSON file
    # print(json_file_path)
    with open(json_file_path, 'r') as file:
        json_data = json.load(file)
    
    replace_outputPath(json_data, output_path)

    # Write the modified data back to the JSON file
    with open(json_file_path, 'w') as file:
        json.dump(json_data, file, indent=4)

def replace_outputPath(json_data, output_path):    
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            if key == "OutputFile" or key == "FeatureDataFile":
                file_name = os.path.basename(value)
                json_data[key] = f"{output_path}/{file_name}"
            elif key == "OutputPath" or key == "FeatureInputFile":
                json_data[key] = f"{output_path}"
            elif isinstance(value, dict) or isinstance(value, list):
                replace_outputPath(value, output_path)
    
    elif isinstance(json_data, list):
        for item in json_data:
            replace_outputPath(item, output_path)

def replace_RVEproperties_json(json_file_path, RVEproperties):
    # Read the JSON file
    with open(json_file_path, 'r') as file:
        json_data = json.load(file)
    
    # Iterate over keys '00' to 'xx', xx depends on how many filters you use in dream 3D
    for key in json_data.keys():
        # Check if 'Filter_Human_Label' matches 'Initialize Synthetic Volume'
        if json_data[key].get('Filter_Human_Label') == 'Initialize Synthetic Volume':
            # Switching on "EstimateNumberOfFeatures"
            json_data[key]['EstimateNumberOfFeatures'] = 1
            # Replace 'Origin' with the RVE properties origin
            json_data[key]['Origin'] = RVEproperties['Origin']
            # Replace 'Dimensions' with the RVE properties dimensions
            json_data[key]['Dimensions'] = RVEproperties['Dimensions']
            # Replace 'Resolution' with the RVE properties resolution
            json_data[key]['Resolution'] = RVEproperties['Resolution']
        # Check for "Match Crystallography"
        elif json_data[key].get('Filter_Human_Label') == 'Match Crystallography':
            # Replace 'MaxIterations' with the RVE properties maxIters
            json_data[key]['MaxIterations'] = RVEproperties['MaxIterations']
        elif json_data[key].get('Filter_Human_Label') == "Export Feature Data as CSV File":
            # Switching on 'WriteNumFeaturesLine'
            json_data[key]['WriteNumFeaturesLine'] = 1
    
    # Write the modified data back to the JSON file
    with open(json_file_path, 'w') as file:
        json.dump(json_data, file, indent=4)

def parseDimensions(dimension):
    keys = ['x', 'y', 'z']
    values = [int(x) for x in dimension.split('x')]
    parsedDimension = dict(zip(keys, values))
    return parsedDimension

def parseResolution(resolution):
    keys = ['x', 'y', 'z']
    values = [float(x) for x in resolution.split('x')]
    parsedResolution = dict(zip(keys, values))
    return parsedResolution

def parseOrigin(origin):
    keys = ['x', 'y', 'z']
    values = [float(x) for x in origin.split('x')]
    parsedOrigin = dict(zip(keys, values))
    return parsedOrigin

def searchForNumFeatures(destinationPath):
    csv_file = glob.glob(f'{destinationPath}/*.csv')[0]
    # Read the CSV file with pandas
    df = pd.read_csv(csv_file, nrows=1, header=None)
    # Extract the numFeatures from the first line
    numFeatures = df.iloc[0, 0]
    return numFeatures

def printProgress(info):
    numberOfRVE = info['numberOfRVE']
    RVEgroups = info['RVEgroups']
    simPath = info['simPath']
    logPath = info['logPath']
    logTable = PrettyTable()
    fieldNames = [""]
    fieldNames.extend([f"RVE{i}" for i in range(1, numberOfRVE + 1)])
    logTable.field_names = fieldNames
    for groupIndex in RVEgroups:
        groupRow = [groupIndex]
        for RVEIndex in range(1, numberOfRVE + 1):
            destinationPath = f"{simPath}/{groupIndex}/RVE{RVEIndex}"
            if len(os.listdir(f"{destinationPath}/postProc")) != 0:
                groupRow.append("✓")
            else:
                groupRow.append("✗")
        logTable.add_row(groupRow)
    printLog(logTable.get_string() + "\n", logPath)

def parseNumFeatures(NumFeaturesReference, numFeaturesType, numFeaturesEstimation):
    if numFeaturesType == 'range':
        rangeFeatures = numFeaturesEstimation.split('-')
        lowerBound = int(rangeFeatures[0])
        upperBound = int(rangeFeatures[1])
        if NumFeaturesReference < lowerBound or NumFeaturesReference > upperBound:
            raise ValueError(f"NumFeaturesReference {NumFeaturesReference} is not in the range of {lowerBound} and {upperBound}")
        # Choose a random number of features between the lower and upper bound, inclusive
        numFeatures = np.random.randint(lowerBound, upperBound + 1)
        return numFeatures

    elif numFeaturesType == 'deviation':
        if numFeaturesEstimation <= 0 or numFeaturesEstimation >= 1:
            raise ValueError(f"Deviation percent is not in the range of (0, 1)")
        deviationFeatures = NumFeaturesReference * float(numFeaturesEstimation)
        lowerBound = NumFeaturesReference - deviationFeatures
        upperBound = NumFeaturesReference + deviationFeatures
        # Choose a random number of features between the lower and upper bound, inclusive
        numFeatures = np.random.randint(lowerBound, upperBound + 1)
        return numFeatures    
    else:
        raise ValueError(f"numFeaturesType {numFeaturesType} not recognized. Only range and deviation are supported")


