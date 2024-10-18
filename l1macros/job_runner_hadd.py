#!/bin/python3

import os
import subprocess
from glob import glob

def hadd(target, sources):
    cmd = f"hadd -f {target} {' '.join(sources)}"
    subprocess.run(cmd, shell=True)

dqm_prefix = "/eos/home-l/lebeling/www/DQM"

# collect all histogram root files
#all_files = glob(f"{dqm_prefix}/*/*/*/PromptReco-v*/*/*/*.root")
all_files = glob(f"{dqm_prefix}/*/*/*/*/*/*.root")
print(all_files)

# group files by runnum, by era, and by year
file_groups = {}
for file in all_files:
    parts = file.split('/') 
    filename = parts[-1]
    filehash = parts[-2]
    runnum = parts[-3]
    era = parts[-4]
    label = parts[-5]
    year = parts[-6] 

    # group by runnum 
    #target = file.replace(filehash, "merged")
    target = f"{dqm_prefix}/{year}/{label}/{era}/{runnum}/merged/{filename}"
    if target not in file_groups:
        file_groups[target] = []
    file_groups[target].append(file)

    # group by era
    target = f"{dqm_prefix}/{year}/{label}/{era}/merged/{filename}"
    if target not in file_groups:
        file_groups[target] = []
    file_groups[target].append(file)

    # group by year
    target = f"{dqm_prefix}/{year}/{label}/merged/{filename}"
    if target not in file_groups:
        file_groups[target] = []
    file_groups[target].append(file)


# Hadd grouped files
for target, files in file_groups.items():
    print(f"Hadding files with target {target}")
    os.makedirs(os.path.dirname(target), exist_ok=True)
    hadd(target, files)

# TODO skip files in filelist.txt 