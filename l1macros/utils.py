import os, subprocess, uproot
import pandas as pd

script_dir = os.getcwd()

def run_script(script, infile = "", outdir = ""):
    infile = 'root://eoscms.cern.ch/' + infile
    os.chdir(script_dir)
    os.makedirs(outdir, exist_ok=True)
    cmd = script.replace("$INFILE", infile).replace("$OUTDIR", outdir)

    log_file = script.split(' ')[1]
    log_file = log_file.split('/')[-1]
    log_file = outdir + "/" + log_file.replace(".py", ".log")
    
    with open(log_file, "w") as f: 
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

# def write_queue(script, infile, outdir):
#     script = script.replace("$OUTDIR/", "")
#     strings = script.split(" ")
#     script = strings[1]
#     outfile = strings[5]
#     option = strings[-1]
#     infile = "root://eoscms.cern.ch/" + infile

#     with open("../htcondor/hists.txt", "a") as f:
#         f.write(script + ", " + infile + ", " + outfile + ", " + option + ", " + outdir + "\n")

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
