import sys
import json
import os

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
