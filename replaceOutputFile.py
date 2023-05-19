import sys
import json
import os

def replace_json(json_file_path, output_path):
    # Read JSON file
    # print(json_file_path)
    with open(json_file_path, 'r') as file:
        json_data = json.load(file)
    
    replace_output_file(json_data, output_path)

    # Write the modified data back to the JSON file
    with open(json_file_path, 'w') as file:
        json.dump(json_data, file, indent=4)

def replace_output_file(json_data, output_path):    
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            if key == "OutputFile" or key == "FeatureDataFile":
                file_name = os.path.basename(value)
                json_data[key] = f"{output_path}/{file_name}"
            elif key == "OutputPath" or key == "FeatureInputFile":
                json_data[key] = f"{output_path}"
            elif isinstance(value, dict) or isinstance(value, list):
                replace_output_file(value, output_path)
    
    elif isinstance(json_data, list):
        for item in json_data:
            replace_output_file(item, output_path)


