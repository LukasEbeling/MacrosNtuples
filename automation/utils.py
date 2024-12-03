import os, subprocess, uproot
import pandas as pd

script_dir = os.path.join(os.getcwd(), "../l1macros")
dqm_prefix = "/eos/user/l/lebeling/www/DQM" 
out_prefix = "/eos/user/l/lebeling/www/DQM" 
tier0 = "/eos/cms/tier0/store/data"


def run_command(cmd, log_file = "log.txt"):
    os.chdir(script_dir)
    with open(log_file, "a") as f:
        subprocess.run(cmd, shell=True, stdout=f, stderr=f) 


def parse_file(fname):
        dataset = fname.split("/")[7]
        run = int("".join(fname.split("/")[11:13]))
        base_fname = fname.split("/")[-1].replace(".root","")
        era = fname.split("/")[6]
        reco_version = fname.split("/")[9]

        year = ''.join([char for char in era if char.isdigit()])
        label = ''.join([char for char in dataset if not char.isdigit()])
        
        #return f"{year}/{label}/{era}/{run}/{base_fname}"
        return f"{label}/{era}/{dataset}/{reco_version}/{run}/{base_fname}"


def write_queue(script, infile = "", outdir = ""):
    cmd = script.replace("$INFILE", infile).replace("$OUTDIR", outdir)
    cmd = cmd.replace(" ", "___")
    with open("../htcondor/queue.txt", "a") as f:
        f.write(cmd + "\n")


def get_weeks():
    oms_path = "/eos/cms/store/group/tsg/STEAM/OMSRateNtuple/2024/physics.root"
    with uproot.open(oms_path) as f:
        df = f["tree"].arrays(
            filter_name = ['run', 'year', 'month', 'day'],
            library = "pd"
        )
    df['date'] = pd.to_datetime(df[['year', 'month', 'day']])
    df['week'] = df['date'].dt.isocalendar().week
    
    result_dict = {}
    for _, row in df.iterrows():
        result_dict[row['run']] = row['week']

    return result_dict


def load_filelist(path):
    try: 
        with open(path, "r") as f:
            return [line.strip() for line in f.readlines()]
    except FileNotFoundError: return []


def save_filelist(path, files):
    with open(path, "w") as f:
        for file in files:
            f.write(file + "\n")


def hadd(target, files, local):
    os.makedirs(os.path.dirname(target), exist_ok=True)

    filelist = load_filelist(target.replace('root','txt'))

    if set(filelist) == set(files): 
        print('skipping ' + target, "already hadded")
        return

    save_filelist(target.replace('root','txt'), files)

    print(f"Hadding files with target {target}")
    cmd = f'hadd -f {target} ' + ' '.join(files)
    if local: run_command(cmd, os.path.dirname(target)+"/log.txt")
    else: write_queue(cmd)
