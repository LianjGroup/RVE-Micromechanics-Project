import os
import numpy as np
import pandas as pd
import random
import shutil
import time
import subprocess
import copy
from modules.helper import *
import sys
import selectors

class SIM:
    def __init__(self,info):
        self.info = info

    ################
    # Generate RVE #
    ################

    def submit_RVE(self):
        self.initialize_directories()
        self.write_RVEarrays()
        time.sleep(180)
        self.run_RVE_generation()
    
    def initialize_directories(self):
        material = self.info["material"]
        numberOfRVE = self.info["numberOfRVE"]
        projectPath = self.info["projectPath"]
        logPath = self.info["logPath"]
        #resultPath = self.info["resultPath"]
        simPath = self.info["simPath"]
        templatePath = self.info["templatePath"]
        targetPath = self.info["targetPath"]
        RVEgroups = self.info["RVEgroups"]
        RVEgroupsUnparsed = self.info["RVEgroupsUnparsed"]
        properties = self.info["properties"]

        # Define column names
        column_names = ['Group', 'RVE', 'Path']
        column_names.extend(set(properties) - set(column_names))

        #print(column_names)
        #time.sleep(180)
        # Initialize an empty DataFrame with column names
        recordedProperties = pd.DataFrame(columns=column_names)
        #print(RVEgroupsUnparsed)
        #time.sleep(180)
        for groupIndex in os.listdir(simPath):
            shutil.rmtree(f"{simPath}/{groupIndex}")
        
        for groupIndex in RVEgroups:
            for RVEIndex in range(1, numberOfRVE + 1):
                RVEproperties = copy.deepcopy(RVEgroups[groupIndex])
                RVEpropertiesUnparsed = copy.deepcopy(RVEgroupsUnparsed[groupIndex])
                destinationPath = f"{simPath}/{groupIndex}/RVE{RVEIndex}"
                RVEpropertiesUnparsed['Group'] = groupIndex
                RVEpropertiesUnparsed['RVE'] = f"RVE{RVEIndex}"
                RVEpropertiesUnparsed['Path'] = f"{projectPath}/{destinationPath}/postProc"
                recordedProperties = pd.concat([recordedProperties, pd.DataFrame(RVEpropertiesUnparsed, index=[0])], ignore_index=True)
                shutil.copytree(templatePath, destinationPath)
                replace_outputPath_json(f"{destinationPath}/pipeline.json", f"{projectPath}/{destinationPath}/postProc")
                replace_RVEproperties_json(f"{destinationPath}/pipeline.json", RVEproperties)
        
        
        # Removing the indexing
        np.save(f"{targetPath}/RVEproperties.npy", recordedProperties.to_numpy())
        recordedProperties.to_excel(f"{targetPath}/RVEproperties.xlsx", index=False)
        recordedProperties.to_csv(f"{targetPath}/RVEproperties.csv", index=False)
        
        time.sleep(180)


    def write_RVEarrays(self):
        material = self.info["material"]
        numberOfRVE = self.info["numberOfRVE"]
        projectPath = self.info["projectPath"]
        logPath = self.info["logPath"]
        #resultPath = self.info["resultPath"]
        simPath = self.info["simPath"]
        templatePath = self.info["templatePath"]
        simulationIO = self.info["simulationIO"]
        RVEgroups = self.info["RVEgroups"]

        with open("linux_slurm/array_RVE.txt", 'w') as filename:
            for groupIndex in RVEgroups:
                for RVEIndex in range(1, numberOfRVE + 1):
                    destinationPath = f"{simPath}/{groupIndex}/RVE{RVEIndex}"
                    filename.write(f"PipelineRunner -p {projectPath}/{destinationPath}/pipeline.json\n")

    def run_RVE_generation(self):
        material = self.info["material"]
        numberOfRVE = self.info["numberOfRVE"]
        projectPath = self.info["projectPath"]
        logPath = self.info["logPath"]
        #resultPath = self.info["resultPath"]
        simPath = self.info["simPath"]
        templatePath = self.info["templatePath"]
        simulationIO = self.info["simulationIO"]
        
        print(f"Generation of {numberOfRVE} RVEs starts")

        # Execute the shell script
        process = subprocess.Popen(['bash', 'linux_slurm/sbatch-hq.sh'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Wait for the process to complete and capture the output
        stdout, stderr = process.communicate()
        #return_code = process.returncode
        return_code = process.wait()

        if simulationIO == "yes":
            # Check the return code
            if return_code == 0:
                print("Sbatch-HQ shell script executed successfully.")
            else:
                print("Sbatch-HQ shell script execution failed with return code:", return_code)

            # Print the stdout if it is not None
            if isinstance(stdout, bytes):
                print("\nStandard Output:")
                print(stdout.decode('utf-8'))

            # Print the stdout if it is not None
            if isinstance(stderr, bytes):
                print("\nStandard Error:")
                print(stderr.decode('utf-8'))

        # process = subprocess.Popen(f"sbatch-hq --cores=1 --nodes=1 --account=project_2007935 --partition=small --time=01:00:00 linux_slurm/array_RVE.txt", shell=True)

        # # Wait for the process to complete and capture the output
        # stdout, stderr = process.communicate()

        # # return_code = process.returncode
        # return_code = process.wait()

        # if simulationIO == "yes":
        #     # Check the return code
        #     if return_code == 0:
        #         print("RVE generation script executed successfully.")
        #     else:
        #         print("RVE generation script execution failed with return code:", return_code)

        #     # Print the stdout if it is not None
        #     if isinstance(stdout, bytes):
        #         print("\nStandard Output:")
        #         print(stdout.decode('utf-8'))

        #     # Print the stdout if it is not None
        #     if isinstance(stderr, bytes):
        #         print("\nStandard Error:")
        #         print(stderr.decode('utf-8'))