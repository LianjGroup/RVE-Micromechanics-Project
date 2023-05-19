module load sbatch-hq
module load python-data

### Prevent stack overflow for large models, especially when using openMP
ulimit -s unlimited 

### Enabling environments
PATH=$PATH:/projappl/project_2007935/DREAM3D-6.5.171-Linux-x86_64:/projappl/project_2007935/DREAM3D-6.5.171-Linux-x86_64/bin
