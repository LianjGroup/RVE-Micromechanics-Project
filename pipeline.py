import os
import time
import pandas as pd
import numpy as np
from prettytable import PrettyTable
import RVEconfig
from modules.SIM import *
from modules.helper import *
from modules.preprocessing import *
import copy

def main_optimize(info):
    material = info['material']
    numberOfRVE = info['numberOfRVE']
    simulationIO = info['simulationIO']
    projectPath = info['projectPath']
    logPath = info['logPath']
    #resultPath = info['resultPath']
    simPath = info['simPath']
    templatePath = info['templatePath']
    targetPath = info["targetPath"]
    RVEgroups = info["RVEgroups"]
    RVEgroupsUnparsed = info["RVEgroupsUnparsed"]
    properties = info["properties"]
    skipSimulationRVEGeneration = info["skipSimulationRVEGeneration"]
    
    # Create a SIM object
    sim = SIM(info)
    postProcTools = PostProcessingTools(info)
    if skipSimulationRVEGeneration == "no":
        sim.submit_RVE()
    postProcTools.slicingRVE()

if __name__ == '__main__':
    info = RVEconfig.main_config()
    main_optimize(info)