#!/bin/bash
#SBATCH -p gpu
#SBATCH --mem=32g
#SBATCH --gres=gpu:rtx2080:1
#SBATCH -c 2
#SBATCH --output=example_3.out

source activate mlfold

output_dir="../outputs/example_3_watermark_outputs"
if [ ! -d $output_dir ]
then
    mkdir -p $output_dir
fi

python ../protein_mpnn_run.py \
        --pdb_path ../inputs/PDB_complexes/pdbs/3HTN.pdb \
        --pdb_path_chains "A B" \
        --out_folder $output_dir \
        --num_seq_per_target 2 \
        --sampling_temp "0.1" \
        --seed 37 \
        --batch_size 1 \
        --watermark \
        --ngram_len 4 \
        --watermark_keys "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0" \
        --num_leaves 25
