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

class PostProcessingTools():
    def __init__(self,info):
        self.info = info

    def slicingRVE(self):
        material = self.info["material"]
        numberOfRVE = self.info["numberOfRVE"]
        projectPath = self.info["projectPath"]
        logPath = self.info["logPath"]
        #resultPath = self.info["resultPath"]
        resultPath = self.info["resultPath"]
        simPath = self.info["simPath"]
        templatePath = self.info["templatePath"]
        targetPath = self.info["targetPath"]
        RVEgroups = self.info["RVEgroups"]
        RVEgroupsUnparsed = self.info["RVEgroupsUnparsed"]

        # Removing results/{material}/slicedRVE if they exist
        if os.path.exists(f"{projectPath}/results/{material}/slicedRVE"):
            shutil.rmtree(f"{projectPath}/results/{material}/slicedRVE")
        os.mkdir(f"{projectPath}/results/{material}/slicedRVE")
        
        for groupIndex in RVEgroups:
            for RVEIndex in range(1, numberOfRVE + 1):
                slicingResultPath = f"results/{material}/slicedRVE/{groupIndex}/RVE{RVEIndex}"
                if not os.path.exists(f"{projectPath}/{slicingResultPath}"):
                    os.makedirs(f"{projectPath}/{slicingResultPath}")
    
        for groupIndex in RVEgroups:
            for RVEIndex in range(1, numberOfRVE + 1):
                simulationPath = f"{projectPath}/{simPath}/{groupIndex}/RVE{RVEIndex}/postProc"
                slicingResultPath = f"results/{material}/slicedRVE/{groupIndex}/RVE{RVEIndex}"
                # Reading the csv file from the RVE simulations
                fileName = searchForTXT(simulationPath)
                dimensions = self.info["RVEgroups"][groupIndex]["Dimensions"]
                #print(dimensions)
                XY, Z = self.slicingAlongZdimension(dimensions)
                # Read the input text file
                
                with open(fileName, "r") as file:
                    lines = file.readlines()
                    # Slice the lines and write sub text files
                    for i in range(1, Z + 1):
                        start_index = (i - 1) * XY
                        end_index = i * XY
                        subfile_lines = lines[start_index:end_index]
                        
                        # Generate the sub text file name
                        subfile_name = f"{slicingResultPath}/slice_{i}.txt"
                        
                        # Write the sub text file
                        with open(subfile_name, "w") as subfile:
                            subfile.writelines(subfile_lines)
        
        printLog("Finish slicing the RVEs across Z dimension for all groups\n", logPath) 

    def slicingAlongZdimension(self, dimensions):
        XY = dimensions["x"] * dimensions["y"]
        Z = dimensions["z"]
        return XY, Z

