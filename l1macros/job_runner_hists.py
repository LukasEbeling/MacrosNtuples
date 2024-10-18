#!/bin/python3

import os, sys, subprocess, yaml
from glob import glob
from job_runner_utils import run_script, write_queue, parse_file


path_prefix = "/eos/cms/tier0/store/data"
out_prefix = "/eos/user/l/lebeling/www/DQM/" # "/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/cmsl1dpg/www/DQM/T0PromptNanoMonit/"
script_dir = os.getcwd()
config_dict = yaml.safe_load(open('config.yaml', 'r'))


for label, config in config_dict.items():
    print(20*"#" + f" Running plots for {label} " + 20*"#")

    # step 1 - find all files on tier 0
    fnames = []
    for dataset in config["datasets"]:
        for era in config["eras"]:
            fnames += glob(f"{path_prefix}/{era}/{dataset}/NANOAOD/PromptReco-v*/*/*/*/*/*.root")

    # step 2 - for each file, run scripts
    fnames = fnames[:5]
    for fname in fnames:
        print(f"Processing file {fname}")

        out_web_path = out_prefix + parse_file(fname)

        if os.path.exists(out_web_path):
                root_files = glob(f"{out_web_path}/*.root")
                if len(root_files) > 0:
                    print(f"Skipping {out_web_path} - already processed")
                    continue

        for script in config["scripts"]: 
            run_script(script, fname, out_web_path)
            #write_queue(script, fname, out_web_path)
