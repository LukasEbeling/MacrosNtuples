#!/bin/python3

import argparse
import os

automation_path = '/afs/cern.ch/user/l/lebeling/MacrosNtuples/automation'

# parse commands to be executed as arguments
parser = argparse.ArgumentParser(description="wrapper running script on htcondor")
parser.add_argument('cmd', nargs='+', type=str, help='commands to be executed')
args = parser.parse_args()

concatenated_cmd = ' '.join(args.cmd)
concatenated_cmd = concatenated_cmd.replace("___", " ")
#concatenated_cmd = 'tar -xzf MacrosNtuples.tar.gz; cd MacrosNtuples/l1macros; ' + concatenated_cmd
concatenated_cmd = f'cd {automation_path}; ' + concatenated_cmd

print('command to be executed: ' + concatenated_cmd)
os.system(concatenated_cmd)
