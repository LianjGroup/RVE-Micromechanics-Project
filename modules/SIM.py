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
from collections import OrderedDict

class SIM:
    def __init__(self,info):
        self.info = info

    ################
    # Generate RVE #
    ################

    def submit_RVE(self):
        self.initialize_directories()
        self.write_RVE_arrays()
        self.run_RVE_generation()
        self.write_RVE_properties()
    
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

        for groupIndex in os.listdir(simPath):
            shutil.rmtree(f"{simPath}/{groupIndex}")
        
        for groupIndex in RVEgroups:
            for RVEIndex in range(1, numberOfRVE + 1):
                destinationPath = f"{simPath}/{groupIndex}/RVE{RVEIndex}"
                shutil.copytree(templatePath, destinationPath)
                replace_outputPath_json(f"{destinationPath}/pipeline.json", f"{projectPath}/{destinationPath}/postProc")
                replace_RVEproperties_json(f"{destinationPath}/pipeline.json", RVEgroups[groupIndex])
        
        # time.sleep(180)

    def write_RVE_arrays(self):
        material = self.info["material"]
        numberOfRVE = self.info["numberOfRVE"]
        projectPath = self.info["projectPath"]
        logPath = self.info["logPath"]
        #resultPath = self.info["resultPath"]
        simPath = self.info["simPath"]
        templatePath = self.info["templatePath"]
        simulationIO = self.info["simulationIO"]
        RVEgroups = self.info["RVEgroups"]

        # with open("linux_slurm/array_RVE.txt", 'w') as filename:
        #     for groupIndex in RVEgroups:
        #         for RVEIndex in range(1, numberOfRVE + 1):
        #             destinationPath = f"{simPath}/{groupIndex}/RVE{RVEIndex}"
        #             #filename.write(f"cp $PIPELINE_DIR/PipelineRunner $PIPELINE_DIR/PipelineRunner{groupIndex}RVE{RVEIndex} && $PIPELINE_DIR/PipelineRunner{groupIndex}RVE{RVEIndex} -p {projectPath}/{destinationPath}/pipeline.json && rm $PIPELINE_DIR/PipelineRunner{groupIndex}RVE{RVEIndex}\n")
        #             filename.write(f"cp $PIPELINE_DIR/PipelineRunner $PIPELINE_DIR/PipelineRunner{groupIndex}RVE{RVEIndex} && $PIPELINE_DIR/PipelineRunner{groupIndex}RVE{RVEIndex} -p {projectPath}/{destinationPath}/pipeline.json && rm $PIPELINE_DIR/PipelineRunner{groupIndex}RVE{RVEIndex}\n")

        with open("linux_slurm/array_RVE.txt", 'w') as filename:
            for groupIndex in RVEgroups:
                allCommands = ""
                for RVEIndex in range(1, numberOfRVE + 1):
                    destinationPath = f"{simPath}/{groupIndex}/RVE{RVEIndex}"
                    allCommands += f"$PIPELINE_DIR/PipelineRunner -p {projectPath}/{destinationPath}/pipeline.json && "
                # Remove last 4 characters
                allCommands = allCommands[:-4]
                filename.write(f"{allCommands}\n")
    
    def run_RVE_generation(self):
        material = self.info["material"]
        numberOfRVE = self.info["numberOfRVE"]
        projectPath = self.info["projectPath"]
        logPath = self.info["logPath"]
        #resultPath = self.info["resultPath"]
        simPath = self.info["simPath"]
        templatePath = self.info["templatePath"]
        simulationIO = self.info["simulationIO"]
        RVEgroups = self.info["RVEgroups"]

        printLog(f"Generation of {numberOfRVE * len(RVEgroups)} RVEs starts", logPath)

        # Execute the shell script
        process = subprocess.Popen(['bash', 'linux_slurm/sbatch-hq.sh'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Wait for the process to complete and capture the output
        stdout, stderr = process.communicate()
        #return_code = process.returncode
        return_code = process.wait()

        if simulationIO == "yes":
            # Check the return code
            if return_code == 0:
                printLog("Sbatch-HQ shell script executed successfully.", logPath)
            else:
                printLog(f"Sbatch-HQ shell script execution failed with return code: {return_code}", logPath)

            # Print the stdout if it is not None
            if isinstance(stdout, bytes):
                printLog("\nStandard Output:", logPath)
                printLog(stdout.decode('utf-8'), logPath)

            # Print the stdout if it is not None
            if isinstance(stderr, bytes):
                printLog("\nStandard Error:", logPath)
                printLog(stderr.decode('utf-8'), logPath)
        
        self.periodCheckFinishedSimulation()
    
    def periodCheckFinishedSimulation(self):
        
        material = self.info["material"]
        numberOfRVE = self.info["numberOfRVE"]
        projectPath = self.info["projectPath"]
        logPath = self.info["logPath"]
        #resultPath = self.info["resultPath"]
        simPath = self.info["simPath"]
        templatePath = self.info["templatePath"]
        simulationIO = self.info["simulationIO"]
        RVEgroups = self.info["RVEgroups"]

        numberOfGroups = len(RVEgroups)
        
        printLog("Waiting for RVE generation to finish", logPath)
        # For each 10 seconds, checking if simulation is finishes by checking directory not empty
        if simulationIO == "yes":
            printLog("Printing RVE generation progress matrix", logPath)
            printLog("Mark ✓ means RVE generation is finished", logPath)
            printLog("Mark ✗ means RVE generation is not finished\n", logPath)
        
        while True:
            time.sleep(30)
            if simulationIO == "yes":
                printProgress(self.info)

            checkAllFinished = []
            for groupIndex in RVEgroups:
                for RVEIndex in range(1, numberOfRVE + 1):
                    # Checking if destinationPath is not empty using all() and os.listdir()
                    destinationPath = f"{simPath}/{groupIndex}/RVE{RVEIndex}"
                    if len(os.listdir(f"{destinationPath}/postProc")) != 0:
                        checkAllFinished.append(True)
                    else:
                        checkAllFinished.append(False)
            if all(checkAllFinished):
                break
        
        printLog(f"{numberOfRVE * numberOfGroups} RVE generation completed", logPath)

    def write_RVE_properties(self):
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
        column_names = ['Group', 'RVE', 'Path', 'NumFeatures']
        propertiesCopy = copy.deepcopy(properties)

        propertiesMinux = []
        for property in propertiesCopy:
            if property not in column_names:
                propertiesMinux.append(property)
        column_names.extend(propertiesMinux)
        recordedProperties = pd.DataFrame(columns=column_names)
        #print(column_names)
        #time.sleep(180)
        # Initialize an empty DataFrame with column names
        for groupIndex in RVEgroups:
            for RVEIndex in range(1, numberOfRVE + 1):
                destinationPath = f"{simPath}/{groupIndex}/RVE{RVEIndex}"
                RVEpropertiesUnparsed = copy.deepcopy(RVEgroupsUnparsed[groupIndex])
                RVEpropertiesUnparsed['Group'] = groupIndex
                RVEpropertiesUnparsed['RVE'] = f"RVE{RVEIndex}"
                RVEpropertiesUnparsed['Path'] = f"{destinationPath}/postProc"
                RVEpropertiesUnparsed['NumFeatures'] = searchForNumFeatures(f"{projectPath}/{destinationPath}/postProc")
                recordedProperties = pd.concat([recordedProperties, pd.DataFrame(RVEpropertiesUnparsed, index=[0])], ignore_index=True)
        # Removing the indexing
        np.save(f"{targetPath}/RVEproperties.npy", recordedProperties.to_numpy())
        recordedProperties.to_excel(f"{targetPath}/RVEproperties.xlsx", index=False)
        recordedProperties.to_csv(f"{targetPath}/RVEproperties.csv", index=False)

        printLog(f"Finish writing RVE properties to targets/{material}", logPath)