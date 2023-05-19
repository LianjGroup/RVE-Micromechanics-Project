import os
import numpy as np
import random
import shutil
import time
import subprocess
import copy
from replaceOutputFile import *
import sys
import selectors

class SIM:
    def __init__(self,info):
        self.info = info
        self.fileIndex = 1
        self.path2params = {} # loading/fileIndex -> param
      

    ################
    # Generate RVE #
    ################

    def submit_RVE(self):
        material = self.info["material"]
        numberOfRVE = self.info["numberOfRVE"]
        projectPath = self.info["projectPath"]
        logPath = self.info["logPath"]
        resultPath = self.info["resultPath"]
        simPath = self.info["simPath"]
        templatePath = self.info["templatePath"]
        
        for fileIndex in os.listdir(simPath):
            shutil.rmtree(f"{simPath}/{fileIndex}")

        for index in range(1, numberOfRVE + 1):
            destinationPath = f"{simPath}/{index}"
            shutil.copytree(templatePath, destinationPath)
            replace_json(f"{destinationPath}/pipeline.json", f"{projectPath}{destinationPath}/postProc")
        
        self.run_RVE_generation()
    
    def run_RVE_generation(self):
        material = self.info["material"]
        numberOfRVE = self.info["numberOfRVE"]
        projectPath = self.info["projectPath"]
        logPath = self.info["logPath"]
        resultPath = self.info["resultPath"]
        simPath = self.info["simPath"]
        templatePath = self.info["templatePath"]
        simulationIO = self.info["simulationIO"]

        with open("linux_slurm/array_RVE.txt", 'w') as filename:
            for index in range(1, numberOfRVE + 1):
                filename.write(f"PipelineRunner -p {projectPath}/{simPath}/{index}/pipeline.json\n")
        print(f"Generation of {numberOfRVE} RVEs starts")

        # Execute the shell script
        process = subprocess.Popen(['bash', 'linux_slurm/env.sh'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Wait for the process to complete and capture the output
        stdout, stderr = process.communicate()
        return_code = process.returncode

        if simulationIO == "yes":
            # Check the return code
            if return_code == 0:
                print("Env shell script executed successfully.")
            else:
                print("Env shell script execution failed with return code:", return_code)

            # Print the stdout if it is not None
            if isinstance(stdout, bytes):
                print("\nStandard Output:")
                print(stdout.decode('utf-8'))

            # Print the stdout if it is not None
            if isinstance(stderr, bytes):
                print("\nStandard Error:")
                print(stderr.decode('utf-8'))

        process = subprocess.Popen(f"sbatch-hq --wait --cores=1 --nodes=1 --account=/scratch/project_2007935 --partition=test --time=01:00:00 linux_slurm/array_RVE.txt", shell=True)

        # Wait for the process to complete and capture the output
        stdout, stderr = process.communicate()
        return_code = process.returncode

        if simulationIO == "yes":
            # Check the return code
            if return_code == 0:
                print("RVE generation script executed successfully.")
            else:
                print("RVE generation script execution failed with return code:", return_code)

            # Print the stdout if it is not None
            if isinstance(stdout, bytes):
                print("\nStandard Output:")
                print(stdout.decode('utf-8'))

            # Print the stdout if it is not None
            if isinstance(stderr, bytes):
                print("\nStandard Error:")
                print(stderr.decode('utf-8'))