import os
import sys
import tempfile
import pandas

csv=sys.argv[1]
odir=sys.argv[2]

# path to diffdock repo
dd_path="../tools/DiffDock"

local_rank = int(os.environ["SLURM_LOCALID"])
rank = int(os.environ["SLURM_PROCID"]) # Global proc id
size = int(os.environ["SLURM_NTASKS"])
print("local_rank, rank, size=",local_rank, rank, size)

assert os.path.exists(odir)

os.environ["CUDA_VISIBLE_DEVICES"] = str(local_rank)


cmd="python {dd_path}/inference.py  --config {dd_path}/default_inference_args.yaml --protein_ligand_csv {csv} --out_dir {outdir}"

import shutil

df = pandas.read_csv(csv, sep=",")
nrow = len(df)
reader = pandas.read_csv(csv, sep=",", chunksize=nrow//size)
for i_chunk, chunk in enumerate(reader):
    if i_chunk % size != rank:
        continue

    with tempfile.NamedTemporaryFile(mode='w', delete=True, suffix='.csv') as tmp_file:
        path=tmp_file.name
        chunk.to_csv(tmp_file, sep=",")
        print(len(chunk), path)
        print(cmd.format(csv=path, outdir=odir, dd_path=dd_path))
        os.system(cmd.format(csv=path, outdir=odir))
    

