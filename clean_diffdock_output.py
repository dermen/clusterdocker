import pandas
import os
import glob
import sys

# use this to condense the diffdock folder into a TSV file with
# the SDF files encoded as strings in the TSV file

# diffdock output foleder
dd_odir = sys.argv[1]

dirnames = glob.glob(f"{dd_odir}/*")
all_df =[]
for i_d, d in enumerate(dirnames):
    print(f"gathering from dir {d} ({i_d+1}/{len(dirnames)})")
    fnames = glob.glob(f"{d}/rank*_*sdf")
    confs = [float(f.split("confidence")[1].split(".sdf")[0]) for f in fnames]
    sdf = [open(f, 'r').read() for f in fnames]
    ranks = [int(f.split("rank")[1].split("_")[0]) for f in fnames]
    df = pandas.DataFrame({"dd_conf":confs, "sdf":sdf,"ranks":ranks})
    df['complex_name'] = os.path.basename(os.path.dirname(fnames[0]))
    all_df.append(df)
results = pandas.concat(all_df)

tsv = sys.argv[2]
results.to_csv(tsv, sep="\t")
# open with: df = pandas.read_csv(tsv, sep="\t")

