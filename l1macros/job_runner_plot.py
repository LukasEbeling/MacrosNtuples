#!/bin/python3

import os, sys, time, subprocess, yaml
from glob import glob
from job_runner_utils import run_script

dqm_prefix = "/eos/home-l/lebeling/www/DQM"
script_dir = "/eos/home-l/lebeling/projects/MacrosNtuples/l1macros"
config_dict = yaml.safe_load(open('config.yaml', 'r'))


# find all directories called 'merged' (containing hadded files), and run plotting scripts
for label, config in config_dict.items():
    pattern = os.path.join(dqm_prefix, '**', label,'**', 'merged')
    merged_dirs = glob(pattern, recursive=True)

    for merged_dir in merged_dirs:
        for script in config["plotting"]:
            print(80*"#"+'\n'+f"plotting for {merged_dir}")
            run_script(script, "", merged_dir) 

