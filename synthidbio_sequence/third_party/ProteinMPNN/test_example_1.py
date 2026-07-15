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

"""Simplified test for example 1 non-watermarked generation."""

import os
import re
import subprocess
import shutil


def test_example_1_non_watermarked():
  """Test protein_mpnn_run.py with example 1 (non-watermarked)."""

  script_dir = os.path.dirname(os.path.abspath(__file__))
  output_dir = os.path.join(script_dir, 'outputs', 'example_1_outputs')
  parsed_pdbs = os.path.join(script_dir, 'test_data', 'helper_outputs', 'parsed_pdbs.jsonl')

  if os.path.exists(output_dir):
    shutil.rmtree(output_dir)
  os.makedirs(output_dir, exist_ok=True)

  env = os.environ.copy()
  env['PYTHONHASHSEED'] = '0'
  env['OMP_NUM_THREADS'] = '1'

  result = subprocess.run(
    ['python', os.path.join(script_dir, 'protein_mpnn_run.py'),
    '--jsonl_path', parsed_pdbs, '--out_folder', output_dir,
    '--num_seq_per_target', '2', '--sampling_temp', '0.1',
    '--seed', '37', '--batch_size', '1'],
    cwd=script_dir, capture_output=True, text=True, env=env)

  assert result.returncode == 0, f"Failed: {result.stderr}"
  assert os.path.exists(os.path.join(output_dir, 'seqs', '5L33.fa'))
  assert os.path.exists(os.path.join(output_dir, 'seqs', '6MRR.fa'))

  expected_5l33_g = [0.5037, 0.5130]
  expected_6mrr_g = [0.5212, 0.5255]

  with open(os.path.join(output_dir, 'seqs', '5L33.fa'), 'r') as f:
    content = f.read()
    assert 'mean_g_value=' in content, "G-values should be present"
    g_values = [float(g) for g in re.findall(r'mean_g_value=([\d.]+)', content)]
    assert len(g_values) == 2, (
      f'Expected 2 g-values in 5L33, got {len(g_values)}')
    for i, g_val in enumerate(g_values):
      assert abs(g_val - expected_5l33_g[i]) < 0.0001, (
        f'5L33 sample {i+1}: expected g-value '
        f'{expected_5l33_g[i]}, got {g_val}')

  with open(os.path.join(output_dir, 'seqs', '6MRR.fa'), 'r') as f:
    content = f.read()
    g_values = [float(g) for g in re.findall(r'mean_g_value=([\d.]+)', content)]
    assert len(g_values) == 2, (
      f'Expected 2 g-values in 6MRR, got {len(g_values)}')
    for i, g_val in enumerate(g_values):
      assert abs(g_val - expected_6mrr_g[i]) < 0.0001, (
        f'6MRR sample {i+1}: expected g-value '
        f'{expected_6mrr_g[i]}, got {g_val}')


def test_example_1_watermarked():
  """Test protein_mpnn_run.py with example 1 (watermarked)."""

  script_dir = os.path.dirname(os.path.abspath(__file__))
  output_dir = os.path.join(script_dir, 'outputs', 'example_1_watermark_outputs')
  parsed_pdbs = os.path.join(script_dir, 'test_data', 'helper_outputs', 'parsed_pdbs.jsonl')

  if os.path.exists(output_dir):
    shutil.rmtree(output_dir)
  os.makedirs(output_dir, exist_ok=True)

  env = os.environ.copy()
  env['PYTHONHASHSEED'] = '0'
  env['OMP_NUM_THREADS'] = '1'

  result = subprocess.run(
    ['python', os.path.join(script_dir, 'protein_mpnn_run.py'),
     '--jsonl_path', parsed_pdbs, '--out_folder', output_dir,
     '--num_seq_per_target', '2', '--sampling_temp', '0.1',
     '--seed', '37', '--batch_size', '1', '--watermark',
     '--ngram_len', '4', '--num_leaves', '25',
     '--watermark_keys', '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0'],
    cwd=script_dir, capture_output=True, text=True, env=env)

  assert result.returncode == 0, f"Failed: {result.stderr}"
  assert os.path.exists(os.path.join(output_dir, 'seqs', '5L33.fa'))
  assert os.path.exists(os.path.join(output_dir, 'seqs', '6MRR.fa'))

  expected_5l33_g = [0.7961, 0.7184]
  expected_6mrr_g = [0.7846, 0.7846]

  with open(os.path.join(output_dir, 'seqs', '5L33.fa'), 'r') as f:
    content = f.read()
    assert 'mean_g_value=' in content
    g_values = [float(g) for g in re.findall(
      r'mean_g_value=([\d.]+)', content)]
    assert len(g_values) == 2, (
      'Should have exactly 2 g-values (2 samples)')
    for i, g_val in enumerate(g_values):
      assert abs(g_val - expected_5l33_g[i]) < 0.0001, (
        f'5L33 sample {i+1}: expected g-value '
        f'{expected_5l33_g[i]}, got {g_val}')

  with open(os.path.join(output_dir, 'seqs', '6MRR.fa'), 'r') as f:
    content = f.read()
    g_values = [float(g) for g in re.findall(
      r'mean_g_value=([\d.]+)', content)]
    assert len(g_values) == 2, (
      'Should have exactly 2 g-values (2 samples)')
    for i, g_val in enumerate(g_values):
      assert abs(g_val - expected_6mrr_g[i]) < 0.0001, (
        f'6MRR sample {i+1}: expected g-value '
        f'{expected_6mrr_g[i]}, got {g_val}')
