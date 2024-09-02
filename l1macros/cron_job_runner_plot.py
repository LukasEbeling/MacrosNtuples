#!/bin/python3

import os, sys, time, subprocess
from glob import glob

dqm_prefix = "/eos/home-l/lebeling/www/DQM"
script_dir = "/eos/home-l/lebeling/projects/MacrosNtuples/l1macros"

config_dict = {
    "JetMET" : # for JetMET plots
        {
            "datasets" : ["JetMET0","JetMET1"],
            "eras" : ["Run2024*"],
            "scripts": [
                "python3 ../plotting/make_DiJet_plots.py --dir $OUTDIR --config ../config_cards/full_DiJet.yaml",
                ]
        },
    "EGamma" : # for JetMET plots
        {
            "datasets" : ["EGamma0","EGamma1"],
            "eras" : ["Run2024*"],
            "scripts": [
                ## plotting
                "python3 ../plotting/make_ZToEE_plots.py --dir $OUTDIR --config ../config_cards/full_ZToEE.yaml",
                "python3 ../plotting/make_PhotonJet_plots.py --dir $OUTDIR --config ../config_cards/full_PhotonJet.yaml",
            ]
        },
    "Muon" : # for JetMET plots
        {
            "datasets" : ["Muon0","Muon1"],
            "eras" : ["Run2024*"],            
            "scripts" : [
                ## plotting
                "/bin/python3 ../plotting/make_ZToMuMu_plots.py --dir $OUTDIR --config ../config_cards/full_ZToMuMu.yaml",
                "/bin/python3 ../plotting/make_ZToTauTau_plots.py --dir $OUTDIR --config ../config_cards/full_ZToTauTau.yaml",
                "/bin/python3 ../plotting/make_MuonJet_plots.py --dir $OUTDIR --config ../config_cards/full_MuonJet.yaml",
                ]
        }
}

# run a given script with defined output directory
def run_script(script, outdir):
    os.chdir(script_dir)
    os.makedirs(outdir + "/plotsL1Run3", exist_ok=True)
    cmd = script.replace("$OUTDIR", outdir)
    
    log_file = script.split(' ')[1]
    log_file = log_file.split('/')[-1]
    log_file = outdir + "/" + log_file.replace(".py", ".log")
    
    with open(log_file, "w") as f:
        subprocess.run(cmd, shell=True, stdout=f, stderr=f)


# find all directories called 'merged' (containing hadded files), and run plotting scripts
for label, config in config_dict.items():
    pattern = os.path.join(dqm_prefix, '**', 'merged')
    merged_dirs = glob(pattern, recursive=True)

    for merged_dir in merged_dirs:
        for script in config["scripts"]:
            print(80*"#"+'\n'+f"plotting for {merged_dir}")
            run_script(script, merged_dir) 

