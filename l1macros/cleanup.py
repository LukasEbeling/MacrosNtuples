#!/bin/python3

import glob
import os

base_path = '/eos/home-l/lebeling/www/DQM'

subdirectories = glob.glob("/eos/home-l/lebeling/www/DQM/*/*/PromptReco-v*/*/*/")

# script to delete every subdirectory that does not contain any .root files
for subdirectory in subdirectories:
    files = glob.glob(os.path.join(subdirectory, "*.root"))
    if len(files) == 0:
        print(f"Deleting subdirectory: {subdirectory}")
        #os.system(f"rm -rf {subdirectory}")
