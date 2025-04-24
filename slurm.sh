#!/bin/bash

csv=$1
odir=$2
out_tsv=$3

mkdir -p $odir 
srun -c2 python slurm.py $csv $odir
python clean_diffdock_output.py $odir $out_tsv
rm -rf $odir
