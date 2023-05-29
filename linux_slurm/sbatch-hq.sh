module load sbatch-hq
module load python-data

### Prevent stack overflow for large models, especially when using openMP
ulimit -s unlimited 

### Enabling environments
PATH=$PATH:/projappl/project_2007935/DREAM3D-6.5.171-Linux-x86_64:/projappl/project_2007935/DREAM3D-6.5.171-Linux-x86_64/bin

sbatch-hq --cores=1 --nodes=1 --account=project_2007935 --partition=small --time=01:00:00 linux_slurm/array_RVE.txt