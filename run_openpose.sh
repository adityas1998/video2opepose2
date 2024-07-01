#!/bin/bash
#$ -cwd           # Set the working directory for the job to the current directory
#$ -pe smp 8      # Request 1 core
#$ -l h_rt=2:0:0  # Request 1 hour runtime
#$ -l h_vmem=11G   # Request 1GB RAM

module load anaconda3
conda activate openpose
python app.py