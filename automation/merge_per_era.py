#!/bin/python3

from glob import glob
from utils import hadd, get_weeks, htcondor_flag, dqm_prefix

htcondor = htcondor_flag()

# collect all histogram root files merged by run
all_files = glob(f"{dqm_prefix}/*/*/*/*/*/merged/*.root") #change later to dqm_prefix 
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
        target = f"{dqm_prefix}/Weekly/{week}/{label}/merged/{filename}"
        if target not in file_groups:
            file_groups[target] = []
        file_groups[target].append(file)

    # group by era
    target = f"{dqm_prefix}/{label}/{era}/merged/{filename}"
    if target not in file_groups:
        file_groups[target] = []
    file_groups[target].append(file)

    # group by year
    target = f"{dqm_prefix}/{label}/merged/{filename}"
    if target not in file_groups:
        file_groups[target] = []
    file_groups[target].append(file)


# Hadd grouped files
for target, files in file_groups.items():
    hadd(target, files, htcondor)
