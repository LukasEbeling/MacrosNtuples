#!/bin/python3

from glob import glob
from utils import hadd, htcondor_flag, dqm_prefix

# parse arguments
htcondor = htcondor_flag()

# work around for the moment, remove later 
dqm_official = '/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/cmsl1dpg/www/DQM/T0PromptNanoMonit' 

# collect all base histogram root files
all_files = glob(f"{dqm_official}/*/*/*/*/*/*/*.root")

# group files by runnum, by era, and by year
file_groups = {}
for file in all_files:
    parts = file.split('/') 
    filename = parts[-1]
    filehash = parts[-2]

    # group by runnum 
    target = file.replace(filehash, "merged").replace(dqm_official, dqm_prefix)
    if target not in file_groups:
        file_groups[target] = []
    file_groups[target].append(file)

# Hadd grouped files
for target, files in file_groups.items():
    hadd(target, files, htcondor)
