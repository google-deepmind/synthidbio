#!/bin/bash
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#SBATCH -p gpu
#SBATCH --mem=32g
#SBATCH --gres=gpu:rtx2080:1
#SBATCH -c 3
#SBATCH --output=example_3_from_fasta.out

source activate mlfold

path_to_PDB="../inputs/PDB_complexes/pdbs/3HTN.pdb"
path_to_fasta="../outputs/example_3_outputs/seqs/3HTN.fa"

output_dir="../outputs/example_3_score_only_from_fasta_outputs"
if [ ! -d $output_dir ]
then
    mkdir -p $output_dir
fi

chains_to_design="A B"

python ../protein_mpnn_run.py \
        --path_to_fasta $path_to_fasta \
        --pdb_path $path_to_PDB \
        --pdb_path_chains "$chains_to_design" \
        --out_folder $output_dir \
        --num_seq_per_target 5 \
        --sampling_temp "0.1" \
        --score_only 1 \
        --seed 13 \
        --batch_size 1
