# RVE-Project

How to use the project code for RVE generation 
1. Log into CSC server on PuTTy and WinSCP server
2. Create a folder for the project, like "RVE-Project" and drag the project code into the folder
3. Open Dream 3D software, make a pipeline for the RVE generation and save the pipeline as pipeline.json
4. Determine material name for the RVE, such as "aluminum", "steel", etc. Lets call the material name as {material}
4. Create a folder named {material} for the material under "templates" folder and drag the pipeline.json and empty postProc folder into "templates/{material}"
5. Fill in the material name and the number of RVEs for each group in configs/config.xlsx
6. Open the configs/RVE_groups.xlsx and fill in the RVE group names and the RVE properties of each group
   You can choose any name for the group names besides G1, G2, etc. 
   You can add as many groups as you want in the file but make sure there is no empty row between the group rows in the file 
7. run these on PuTTy
   cd <path to RVE-Project>
   module load python-data
   pip install -r --user requirements.txt # Run only once when you first run Python on CSC
   python generate.py
8. The RVEs will be generated under "simulations/{material}/{RVE group name}/{RVE index}" folder.
   In total there are {number of groups} x {number of RVEs per group} simulation results
9. Click refresh button to update the results on WinSCP once in a while. 
   The PuTTy terminal will be kept waiting in a loop until simulations finish. 
   You can also check output results in directory {hq-server-SLURM-job-id}/HQtask.log
10. After simulations have completed, you can make use of the RVE properties excel/csv or npy file from the directory targets/{material}
   You can conduct RVE evaluation from simulations folder that is associated with each RVE properties 
   The RVE properties are saved in the order of the RVEs in the simulation results

