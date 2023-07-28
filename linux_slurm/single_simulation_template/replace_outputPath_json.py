import sys
import json
import os
import numpy as np
import glob
import argparse

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

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json_file_path", required=True, help="The path to the JSON file")
    parser.add_argument("--output_path", required=True, help="The path where the output will be stored")

    return parser.parse_args()

def main():
    args = parse_args()
    replace_outputPath_json(args.json_file_path, args.output_path)

if __name__ == "__main__":
    main()