#!/bin/python3

import argparse
import os

# parse arguments
parser = argparse.ArgumentParser(description="wrapper running script on htcondor")

# Add an argument that accepts multiple values
parser.add_argument('cmd', nargs='+', type=str, help='commands to be executed')
args = parser.parse_args()

concatenated_cmd = ' '.join(args.cmd)
concatenated_cmd = concatenated_cmd.replace("___", " ")
concatenated_cmd = 'cd MacrosNtuples/l1macros; ' + concatenated_cmd

print(concatenated_cmd)
os.system(concatenated_cmd)
#os.system("pwd")
#os.system("ls -a")