## pipe for the .py already exists (more or less), 
# see https://github.com/MatthieuGG/GPAQ-scores/blob/main/gpaq.py 
# or https://github.com/MatthieuGG/SF36-scores

## functions for the .py already exists,
# see the notebooks in DualTaskProgress (DTP) and DualTaskEffect (DTE)
# WARNING: I have to change the format of inputs (tranpose)

#-------------- Pipe (for the "from data" part, may be different for "manual")
#1- instal requirements
# not mandatory, mainly using pandas / matplotlib pyplot

#2- select a process
# DTE or DTP

#3- give a direction for Cognitive and Motor performance

#4- import data + conditional check: 
# folder exist
# data exist (folder not empty)
# correctly formated (DTE or DTP)
# correct values types (and range? interesting option)
# no missing data

#DTE = [
# Single Task - Cognitive performance
# Single Task - Motor performance
# Dual Task - Cognitive performance
# Dual Task - Motor performance
# ]

#DTP = [
# T1 - Single Task - Cognitive performance
# T1 - Single Task - Motor performance
# T1 - Dual Task - Cognitive performance
# T1 - Dual Task - Motor performance
# T2 - Single Task - Cognitive performance
# T2 - Single Task - Motor performance
# T2 - Dual Task - Cognitive performance
# T2 - Dual Task - Motor performance
# ]

#5- computation
# DTE = [
# Cognitive Dual Task Effect	
# Motor Dual Task Effect	
# Dual Task Effect	
# ]

# DTP = [
# T1 - Cognitive Dual Task Effect	
# T2 - Cognitive Dual Task Effect	
# T1 - Motor Dual Task Effect	
# T2 - Motor Dual Task Effect	
# Cognitive Dual Task Progress	
# Motor Dual Task Progress	
# Initial Dual Task Effect	
# Final Dual Task Effect	
# Dual Task Progress
# ]

#6- Plot & save
# see notebooks

#-------------- Final function to call
# python3 dualtask [effect or progress] [cog+] [mot-] [-d input_path] [-o output_path] [-ind]

# MANDATORY effect or progress: process as DualTaskEffect.ipynb or DualTaskProgress.ipynb
# MANDATORY cog+/- and mot+/-: defines the direction of the test
# OPTIONAL: input path. Default = /data in same folder
# OPTIONAL: output path. Default = /results in same folder
# OPTIONAL: one file per ID. Default = one concatenated csv for all ID
