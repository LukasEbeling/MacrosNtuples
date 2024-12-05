# Automation Tool Kit
Overview 
Steps: make hists, merge per run, merge per era (and week), make plots
Use ```--htcondor``` to write execution commands into queue file and submit 
Make sure the following paths are correct:
- DQM webpage were plots are deployed -> ```dqm_prefix``` in ```utils.py```
- path to tier 0 -> ```tier0``` in ```utils.py```
- path to local installation of automation tool kit -> ```automation_path``` in ```wrapper.py```

### Dump
`*/10 * * * * lxplus python3 /eos/home-l/lebeling/projects/MacrosNtuples/l1macros/cron_job_runner_root.py`

dqm official -> 
```
/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/cmsl1dpg/www/DQM/T0PromptNanoMonit
```

### Bugs
```
python3 ../plotting/make_DiJet_plots.py --dir /eos/user/l/lebeling/www/DQM/Weekly/Week40_386367-386617/JetMET/Run2024H/merged --config ../config_cards/full_DiJet.yaml 

Traceback (most recent call last):
  File "/afs/cern.ch/user/l/lebeling/MacrosNtuples/automation/../plotting/make_DiJet_plots.py", line 678, in <module>
    main()
  File "/afs/cern.ch/user/l/lebeling/MacrosNtuples/automation/../plotting/make_DiJet_plots.py", line 31, in main
    drawplots.makedist(
  File "/afs/cern.ch/user/l/lebeling/MacrosNtuples/plotting/drawplots.py", line 134, in makedist
    h1ds.append(inputFile.Get(h1d[i]+nvtx_suffix).Clone())
ReferenceError: attempt to access a null-pointer
```

```
/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/cmsl1dpg/www/DQM/T0PromptNanoMonit/EGamma/Run2024G/EGamma0/PromptReco-v1/385532/3095b2ea-82b1-41e0-b4bd-f146685a313b
```

### Major Patch Notes
Previously, plotting scripts were submitted to htcondor as ```MacrosNtuples.tar.gz```. No longer needed, as htcondor has access to afs directory. 