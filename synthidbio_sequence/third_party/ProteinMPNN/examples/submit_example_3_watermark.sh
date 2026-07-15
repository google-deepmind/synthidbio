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
