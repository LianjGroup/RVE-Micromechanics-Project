import os
import time
import pandas as pd
import numpy as np
from time import sleep
from prettytable import PrettyTable
from modules.helper import *
###########################################################
#                                                         #
#         CRYSTAL PLASTICITY PARAMETER CALIBRATION        #
#   Tools required: DAMASK and Finnish Supercomputer CSC  #
#                                                         #
###########################################################

# -------------------------------------------------------------------
#   Stage 0: Choose the CP model, the optimization algorithm, number of initial simulations,
#   the target curve index to fit, project path folder and material name
# -------------------------------------------------------------------

def main_config():

    #########################
    # Global configurations #
    #########################

    globalConfig = pd.read_excel("configs/global_config.xlsx", nrows= 1, engine="openpyxl")
    globalConfig = globalConfig.T.to_dict()[0]
    #print(globalConfig)
    material = globalConfig["material"]
    
    numberOfRVE = globalConfig["numberOfRVE"]

    simulationIO = globalConfig["simulationIO"]

    # The project path folder
    projectPath = os.getcwd()
    # The logging path
    logPath = f"log/{material}.txt"

    # The results path
    resultPath = f"results/{material}"

    # The simulations path
    simPath = f"simulations/{material}"

    # The templates path
    templatePath = f"templates/{material}"

    # The target path
    targetPath = f"targets/{material}"

    ###############################
    # Group of RVE configurations #
    ###############################

    RVEgroups = pd.read_excel("configs/RVE_groups.xlsx", engine="openpyxl")
    
    # Convert the DataFrame to a Python dictionary based on RVE group
    RVEgroups = RVEgroups.set_index('Group').to_dict(orient='index')

    for RVEgroup in RVEgroups:
        RVEgroups[RVEgroup]['Dimensions'] = parseDimensions(RVEgroups[RVEgroup]['Dimensions'])
        RVEgroups[RVEgroup]['Resolution'] = parseResolution(RVEgroups[RVEgroup]['Resolution'])
        RVEgroups[RVEgroup]['Origin'] = parseOrigin(RVEgroups[RVEgroup]['Origin'])
    # Print the dictionary
    #print(RVEgroups)
    #sleep(180)

    #########################################################
    # Creating necessary directories for the configurations #
    #########################################################
    def printLog(message, logPath):
        with open(logPath, 'a+') as logFile:
            logFile.writelines(message)
        print(message)

    def checkCreate(path):
        if not os.path.exists(path):
            os.mkdir(path)

    # For configs
    checkCreate("configs")

    # For log
    checkCreate("log")
    path = f"log/{material}"
    checkCreate(path)

    # # For results 
    # checkCreate("results")
    # path = f"results/{material}"
    # checkCreate(path)
    
    # For simulations

    checkCreate("simulations")
    path = f"simulations/{material}"
    checkCreate(path)

    # For templates
    checkCreate("templates")
    path = f"templates/{material}"
    checkCreate(path)

    # For targets
    checkCreate("targets")
    path = f"targets/{material}"
    checkCreate(path)

    ###########################
    # Information declaration #
    ###########################

    info = {
        'projectPath': projectPath,
        'logPath': logPath,
        #'resultPath': resultPath,
        'simPath': simPath,
        'targetPath': targetPath,
        'templatePath': templatePath,
        'material': material,
        'numberOfRVE': numberOfRVE,
        'simulationIO': simulationIO,
        'RVEgroups': RVEgroups
    }

  
    ###############################################
    #  Printing the configurations to the console #
    ###############################################

    printLog(f"\nWelcome to the RVE generation software\n\n", logPath)
    printLog(f"The configurations you have chosen: \n", logPath)
    
    logTable = PrettyTable()

    logTable.field_names = ["Global Configs", "User choice"]
    logTable.add_row(["Material", material])
    logTable.add_row(["Number of RVEs", numberOfRVE])
    logTable.add_row(["Simulation IO", simulationIO])
    printLog(logTable.get_string() + "\n", logPath)

    printLog("Generating necessary directories\n", logPath)
    printLog(f"The path to your main project folder is\n", logPath)
    printLog(f"{projectPath}\n", logPath)

    #############################
    # Returning the information #
    # ###########################

    return info

