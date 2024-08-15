#!/bin/python3

import os, sys, time, subprocess
from glob import glob
import random


in_prefix = "/eos/cms/tier0/store/data"
#out_prefix = "/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/cmsl1dpg/www/DQM/T0PromptNanoMonit/"
out_prefix = "/eos/home-l/lebeling/www/DQM"
script_dir = "/eos/home-l/lebeling/projects/MacrosNtuples/l1macros"

config_dict = {
    "JetMET" : # for JetMET plots
        {
            "datasets" : ["JetMET0","JetMET1"],
            "eras" : ["Run2024*"],
            "scripts": [
                "python3 performances_nano.py -i $INFILE -o $OUTDIR/all_DiJet.root -c DiJet",  
                "python3 ../plotting/make_DiJet_plots.py --dir $OUTDIR --config ../config_cards/full_DiJet.yaml",
                ]
        },
    "EGamma" : # for JetMET plots
        {
            "datasets" : ["EGamma0","EGamma1"],
            "eras" : ["Run2024*"],
            "scripts": [
                "python3 performances_nano.py -i $INFILE -o $OUTDIR/all_PhotonJet.root -c PhotonJet",
                "python3 performances_nano.py -i $INFILE -o $OUTDIR/all_ZToEE.root -c ZToEE",

                ## OFF DQM
                "python3 performances_nano_dqmoff.py -i $INFILE -o $OUTDIR/oug_zee_dqmoff.root -c ZToEEDQMOff",
                ## Plot
                "python3 ../plotting/make_ZToEE_plots.py --dir $OUTDIR --config ../config_cards/full_ZToEE.yaml",
                "python3 ../plotting/make_PhotonJet_plots.py --dir $OUTDIR --config ../config_cards/full_PhotonJet.yaml",
            ]
        },
    "Muon" : # for JetMET plots
        {
            "datasets" : ["Muon0","Muon1"],
            "eras" : ["Run2024*"],            
            "scripts" : [
                "/bin/python3 performances_nano.py -i $INFILE -o $OUTDIR/all_ZToMuMu.root -c ZToMuMu",
                "/bin/python3 performances_nano.py -i $INFILE -o $OUTDIR/all_MuonJet.root -c MuonJet",
                "/bin/python3 performances_nano.py -i $INFILE -o $OUTDIR/all_ZToTauTau.root -c ZToTauTau ",
                ## OFF DQM
                "/bin/python3 performances_nano_dqmoff.py -i $INFILE -o $OUTDIR/out_zmumu_dqmoffl.root -c ZToMuMuDQMOff",
                "/bin/python3 performances_nano_dqmoff.py -i $INFILE -o $OUTDIR/out_jets_dqmoff.root -c JetsDQMOff ",
                "/bin/python3 performances_nano_dqmoff.py -i $INFILE -o $OUTDIR/out_ztautau_dqmoff.root -c ZToTauTauDQMOff",
                "/bin/python3 performances_nano_dqmoff.py -i $INFILE -o $OUTDIR/out_zmumu_dqmoffl.root -c ZToMuMuDQMOff",
                "/bin/python3 performances_nano_dqmoff.py -i $INFILE -o $OUTDIR/out_etsum_dqmoff.root -c EtSumDQMOff",
                ## plotting
                "/bin/python3 ../plotting/make_ZToMuMu_plots.py --dir $OUTDIR --config ../config_cards/full_ZToMuMu.yaml",
                "/bin/python3 ../plotting/make_ZToTauTau_plots.py --dir $OUTDIR --config ../config_cards/full_ZToTauTau.yaml",
                "/bin/python3 ../plotting/make_MuonJet_plots.py --dir $OUTDIR --config ../config_cards/full_MuonJet.yaml",
                ]
        }
}

def hadd(target, sources):
    old_hadd = ""
    if os.path.exists(target):
        old_hadd = target.replace(".root", f"_old.root")
        os.system(f"mv {target} {old_hadd}")
        sources.append(old_hadd)
    
    hadd_cmd = f"hadd -f {target} {' '.join(sources)}"
    print(hadd_cmd)
    subprocess.run(hadd_cmd, shell=True)

    if os.path.exists(old_hadd):
        os.system(f"rm -rf {old_hadd}")


def make_file_list(filepath):
    if not os.path.exists(filepath):
        os.makedirs(outpath, exist_ok=True)
        subprocess.run(f"touch {filepath}", shell=True)
        print(f"Created file list at {filepath}")


def check_file_list(filepath):
    make_file_list(filepath)
    with open(filepath, "r") as f:
        files_in_list = f.readlines()
        files_in_list = [f.strip() for f in files_in_list]
    return files_in_list


def append_file_list(filepath, files):
    make_file_list(filepath)    
    with open(filepath, "w") as f:
        for file in files: f.write(file + "\n")


def run_script(scripts, infile, outdir):
    os.chdir(script_dir)
    if not os.path.exists(outdir+"/plotsL1Run3"):
        os.makedirs(outdir+"/plotsL1Run3", exist_ok=True)

    for script in scripts:
        script = script.replace("$INFILE", infile).replace("$OUTDIR", outdir)
        print(script)        
        with open(f"{outdir}/log.txt", "w") as f:
            subprocess.run(script, shell=True, stdout=f, stderr=f)
        


for label, config in config_dict.items():
    
    runs = []
    for dataset in config["datasets"]:
        for era in config["eras"]:
            runs += glob(f"{in_prefix}/{era}/{dataset}/NANOAOD/PromptReco-v*/*/*/*/*")
            
            for run in runs: 
                all_files = glob(f"{run}/*.root")
                if len(all_files) == 0: continue

                runnum = int("".join(run.split("/")[11:13]))
                if runnum > 383500: break # just test for few runs

                era_label = run.split("/")[6]

                print(era_label, run, "\n"+80*"#")

                outpath = f"{out_prefix}/{era_label}/{label}/{runnum}"

                merged_files = check_file_list(f"{outpath}/merged_files.txt")

                if set(all_files) == set(merged_files):
                    print("All files are already hadded / plotted")
                    continue

                new_files = list(set(all_files) - set(merged_files))
                hadd(f"{outpath}/merged.root", new_files)
                append_file_list(f"{outpath}/merged_files.txt", new_files)

                run_script(config["scripts"], f"{outpath}/merged.root", outpath)


