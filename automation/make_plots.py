#!/bin/python3

import os, argparse, yaml
from glob import glob
from utils import run_command, write_queue


dqm_prefix = "/eos/user/l/lebeling/www/DQM/" # "/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/cmsl1dpg/www/DQM/T0PromptNanoMonit/"
script_dir = os.getcwd()
config_dict = yaml.safe_load(open('config.yaml', 'r'))


# parse arguments
parser = argparse.ArgumentParser(description="plotting")
parser.add_argument('--local', action='store_true', help='run locally (not on condor)')
args = parser.parse_args()
local = args.local

if not local: os.system('rm -rf ../htcondor/queue.txt')


# main logic: glob files merged root files and make plots
for label, config in config_dict.items():
    pattern = os.path.join(dqm_prefix, '**', label,'**', 'merged')
    merged_dirs = glob(pattern, recursive=True)

    for merged_dir in merged_dirs:
        for cmd in config["plotting"]:
            print(80*"#"+'\n'+f"plotting for {merged_dir}")
            os.makedirs(merged_dir + '/plotsL1Run3', exist_ok=True)

            # if directory is non empty get time of newst file
            if os.listdir(merged_dir):
                newest = max(glob(merged_dir + '/*.root'), key=os.path.getctime)
                time_root = os.path.getctime(newest)
            else: time_root = 0

            # if /plotsL1Run3 is non empty get time of newst png file
            if os.listdir(merged_dir + '/plotsL1Run3'):
                newest = max(glob(merged_dir + '/plotsL1Run3/*.png'), key=os.path.getctime)
                time_png = os.path.getctime(newest)
            else: time_png = 0

            if time_png > time_root: continue

            cmd = cmd.replace("$OUTDIR", merged_dir)
            print(cmd)
            if local: run_command(cmd)
            else: write_queue(cmd) 
