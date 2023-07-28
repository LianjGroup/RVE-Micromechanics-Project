#!/bin/bash -l
# created: Oct 19, 2022 22:22 PM
# author: xuanbinh
#SBATCH --account=project_2004956
#SBATCH --partition=test
#SBATCH --time=00:15:00
#SBACTH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH -J CPparameter_test
#SBATCH -e CPparameter_test
#SBATCH --mail-type=ALL
#SBATCH --mail-user=binh.nguyen@aalto.fi

module load python-data

python replace_outputPath_json.py --json_file_path $PWD/pipeline.json --output_path $PWD/postProc

### Prevent stack overflow for large models, especially when using openMP
ulimit -s unlimited 

### Enabling environments
PATH=$PATH:/projappl/project_2004956/DREAM3D-6.5.171-Linux-x86_64:/projappl/project_2004956/DREAM3D-6.5.171-Linux-x86_64/bin

### Processing results 
PipelineRunner -p $PWD/pipeline.json

