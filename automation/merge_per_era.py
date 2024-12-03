#!/bin/python3

import os, argparse
from glob import glob
from utils import hadd, get_weeks


#dqm_prefix = "/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/cmsl1dpg/www/DQM/T0PromptNanoMonit"
dqm_prefix = "/eos/user/l/lebeling/www/DQM" 
out_prefix = "/eos/user/l/lebeling/www/DQM" 


# parse arguments
parser = argparse.ArgumentParser(description="merge per era")
parser.add_argument('--local', action='store_true', help='run locally (not on condor)')
args = parser.parse_args()
local = args.local

if not local: os.system('rm -rf ../htcondor/queue.txt')

# collect all histogram root files
all_files = glob(f"{dqm_prefix}/*/*/*/*/*/merged/*.root")
print('found files:', len(all_files))

weeks = get_weeks()

# group files by week, by era, and by year
file_groups = {}
for file in all_files:
    parts = file.split('/')
    filename = parts[-1]
    run = int(parts[-3])
    era = parts[-6]
    label = parts[-7]

    # group by week - not all run in list? 
    if run in weeks.keys():
        week = weeks[run]
        target = f"{out_prefix}/{label}/{era}/week_{week}/merged/{filename}"
        if target not in file_groups:
            file_groups[target] = []
        file_groups[target].append(file)

    # group by era
    target = f"{out_prefix}/{label}/{era}/merged/{filename}"
    if target not in file_groups:
        file_groups[target] = []
    file_groups[target].append(file)

    # group by year
    target = f"{out_prefix}/{label}/merged/{filename}"
    if target not in file_groups:
        file_groups[target] = []
    file_groups[target].append(file)


# Hadd grouped files
for target, files in file_groups.items():
    hadd(target, files, local)
