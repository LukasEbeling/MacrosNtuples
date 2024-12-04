#!/bin/python3

import os, sys, subprocess, yaml, argparse
from glob import glob
from utils import write_queue, parse_file, run_command, tier0, dqm_prefix

config_dict = yaml.safe_load(open('config.yaml', 'r'))

# parse arguments
parser = argparse.ArgumentParser(description="Run plots for datasets")
parser.add_argument('--htcondor', action='store_true', help='run on htcondor')
args = parser.parse_args()
htcondor = args.htcondor

if htcondor: os.system('rm -rf queue.txt')

# main logic: glob files on tier 0 and run plotting scripts
for label, config in config_dict.items():
    print(20*"#" + f" Running plots for {label} " + 20*"#")

    # step 1 - find all files on tier 0
    fnames = []
    for dataset in config["datasets"]:
        for era in config["eras"]:
            fnames += glob(f"{tier0}/{era}/{dataset}/NANOAOD/PromptReco-v*/*/*/*/*/*.root")

    # step 2 - for each file, run scripts
    # fnames = fnames[:100]
    for fname in fnames:
        print(f"Processing file {fname}")

        out_web_path = dqm_prefix + parse_file(fname)

        # abort if histogram root files already exist
        root_files = glob(f"{out_web_path}/*.root")
        if len(root_files) > 0:
            print(f"Skipping {out_web_path} - already processed")
            continue

        for cmd in config["scripts"]: 
            cmd = cmd.replace("$OUTDIR", out_web_path)
            cmd = cmd.replace("$INFILE", fname)
            
            os.makedirs(out_web_path, exist_ok=True)

            if htcondor: write_queue(cmd) # write script into htcondor queue file
            else: run_command(cmd, out_web_path+"/log.txt") # run script on current shell
