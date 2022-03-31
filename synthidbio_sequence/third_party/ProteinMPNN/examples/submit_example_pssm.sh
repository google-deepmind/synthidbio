#!/bin/bash

# Original code licensed under MIT License.
# Copyright (c) 2022 Justas Dauparas
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

#SBATCH -p gpu
#SBATCH --mem=32g
#SBATCH --gres=gpu:rtx2080:1
#SBATCH -c 2
#SBATCH --output=example_2.out

source activate mlfold


#new_probabilities_using_PSSM = (1-pssm_multi*pssm_coef_gathered[:,None])*probs + pssm_multi*pssm_coef_gathered[:,None]*pssm_bias_gathered 
#probs - predictions from MPNN
#pssm_bias_gathered - input PSSM bias (needs to be a probability distribution)
#pssm_multi - a number between 0.0 (no bias) and 1.0 (no MPNN) inputed via flag --pssm_multi; this is a global number equally applied to all the residues
#pssm_coef_gathered - a number between 0.0 (no bias) and 1.0 (no MPNN) inputed via ../helper_scripts/make_pssm_input_dict.py can be adjusted per residue level; i.e only apply PSSM bias to specific residues; or chains



pssm_input_path="../inputs/PSSM_inputs"
folder_with_pdbs="../inputs/PDB_complexes/pdbs/"

output_dir="../outputs/example_pssm_outputs"
if [ ! -d $output_dir ] 
then
    mkdir -p $output_dir
fi

path_for_parsed_chains=$output_dir"/parsed_pdbs.jsonl"
path_for_assigned_chains=$output_dir"/assigned_pdbs.jsonl"
pssm=$output_dir"/pssm.jsonl"
chains_to_design="A B"

python ../helper_scripts/parse_multiple_chains.py --input_path=$folder_with_pdbs --output_path=$path_for_parsed_chains

python ../helper_scripts/assign_fixed_chains.py --input_path=$path_for_parsed_chains --output_path=$path_for_assigned_chains --chain_list "$chains_to_design"

python ../helper_scripts/make_pssm_input_dict.py --jsonl_input_path=$path_for_parsed_chains --PSSM_input_path=$pssm_input_path --output_path=$pssm

python ../protein_mpnn_run.py \
        --jsonl_path $path_for_parsed_chains \
        --chain_id_jsonl $path_for_assigned_chains \
        --out_folder $output_dir \
        --num_seq_per_target 2 \
        --sampling_temp "0.1" \
        --seed 37 \
        --batch_size 1 \
        --pssm_jsonl $pssm \
        --pssm_multi 0.3 \
        --pssm_bias_flag 1
