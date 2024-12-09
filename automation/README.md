# Automation Tool Kit
Tool kit to (semi) automize production of DQM plot from NanoAODs stored on tier 0. 
Two modes of operation are offered:
- via cron job: recommended for daily processing of new files
- via htcondor: recommended for rerunning all files currently on tier 0

Further details are provided below. The different processing steps are summarized as: 

1) Histograms
Run `python3 make_hists.py` to produce `.root` files containing histograms for all data types (i.e. EGamma, Muon, JetMet). Which selections are run is specified in `config.yaml` (see scritps). If the respective output file already exists, the histogram production is skipped. 

2) Merge per Run
Run `python3 merge_per_run.py` to merge (i.e. hadd) the histogram files per run. If the respective output file already exists and is newer than all base histogram files, the merging is skipped. 

3) Merge per era/week
Run `python3 merge_per_era.py` to further merge (i.e. hadd) the histograms per era (i.e. Run2024H) and per week using the merged histograms per run. If the respective output file already exists and is newer than all base histogram files, the merging is skipped. 

4) Merge per type
Run `python3 merge_total.py` to merge (i.e. hadd) all histograms of one data type (i.e. EGamma, Muon, JetMet) using the merged histograms per era. If the respective output file already exists and is newer than all base histogram files, the merging is skipped. 

5) Plotting
Run `make_plots.py` to produce png/pdf plots from all merged histograms (merge per run/era/week/total). The plotting repective scripts are specified `condfig.yaml`. If the png/pdf files already exist and are newer than the histogram files, the plotting is skipped.  
   

## Init
Clone the repository into afs directory on lxplus:
`git clone git@github.com:LukasEbeling/MacrosNtuples.git` 

Adjust output path (i.e. directory in which all plots and histogram are deployed):
automation -> `utils.py` -> `dqm_prefix`

Asdjust repository path in `wrapper.py` to user installation of `MacrosNtuples`

## Setup for cron
To periodically process new files on tier 0, the following cron job is recommended:
```*/10 * * * * lxplus . cron_job.sh```

Further usefull commands: 
Show cron job list via `acrontab -l`
Edit cron job list via `acrontab -e`
Exit cron job list via `ctrl+O`/`ctrl+X`
Delete full cron job list via `acrontab -r`

## Setup for htcondor
All prduction steps listed above can be run on htcondor. Using the flag `--htcondor`, the repective commands are not directly executed but instead written into the `queue.txt` file. With `condor_submit submit.txt`, all commands in the queue are submitted to htcondor. This mode is recommended to (re-)run all files currently stored on tier 0. 

## Major Patch Notes
Previously, plotting scripts were submitted to htcondor as ```MacrosNtuples.tar.gz```. No longer needed, as htcondor has access to afs directory. 