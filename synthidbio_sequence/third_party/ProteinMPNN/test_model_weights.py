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

"""Test ProteinMPNN with different model weights."""

import os
import subprocess
import shutil
import pytest


MODEL_WEIGHTS = [
  ("vanilla_model_weights", "v_48_020", False),
  ("soluble_model_weights", "v_48_020", False),
]


@pytest.mark.parametrize("model_type,model_version,ca_only", MODEL_WEIGHTS)
def test_model_weights(model_type, model_version, ca_only):
  """Test that different model weights can load and generate sequences."""

  script_dir = os.path.dirname(os.path.abspath(__file__))
  examples_dir = os.path.join(script_dir, 'examples')
  output_dir = os.path.join(script_dir, 'outputs', f'model_test_{model_type}')

  if os.path.exists(output_dir):
    shutil.rmtree(output_dir)

  folder_with_pdbs = os.path.join(script_dir, 'inputs', 'PDB_monomers', 'pdbs')
  path_for_parsed_chains = os.path.join(output_dir, 'parsed_pdbs.jsonl')

  # Parse chains
  os.makedirs(output_dir, exist_ok=True)
  parse_result = subprocess.run(
    ['python', os.path.join(script_dir, 'helper_scripts', 'parse_multiple_chains.py'),
    '--input_path', folder_with_pdbs,
    '--output_path', path_for_parsed_chains],
    cwd=script_dir,
    capture_output=True,
    text=True,
    env={**os.environ, 'PYTHONHASHSEED': '0', 'OMP_NUM_THREADS': '1'}
  )
  assert parse_result.returncode == 0, f"Parse failed: {parse_result.stderr}"

  # Run with specific model weights (path_to_model_weights expects folder)
  model_folder = os.path.join(script_dir, model_type)
  result = subprocess.run(
    ['python', os.path.join(script_dir, 'protein_mpnn_run.py'),
    '--jsonl_path', path_for_parsed_chains,
    '--out_folder', output_dir,
    '--model_name', model_version,
    '--num_seq_per_target', '1',
    '--sampling_temp', '0.1',
    '--seed', '37',
    '--batch_size', '1',
    '--path_to_model_weights', model_folder],
    cwd=script_dir,
    capture_output=True,
    text=True,
    env={**os.environ, 'PYTHONHASHSEED': '0', 'OMP_NUM_THREADS': '1'}
  )

  assert result.returncode == 0, f"Model {model_type}/{model_version} failed: {result.stderr}"

  # Verify outputs exist
  seqs_dir = os.path.join(output_dir, 'seqs')
  assert os.path.exists(seqs_dir), f"Seqs directory not created for {model_type}"

  # Check that at least one FASTA file was created
  fasta_files = [f for f in os.listdir(seqs_dir) if f.endswith('.fa')]
  assert len(fasta_files) > 0, f"No FASTA files generated for {model_type}/{model_version}"


if __name__ == '__main__':
  pytest.main([__file__, '-v'])
