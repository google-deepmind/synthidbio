"""Test g-value computation for both non-watermarked and watermarked sequences."""

import os
import subprocess
import shutil
import re


def test_g_values_non_watermarked():
  """Test g-values for non-watermarked sequences (detector always runs)."""

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

  assert result.returncode == 0, f"protein_mpnn_run.py failed: {result.stderr}"

  # Expected g-values (should be ~0.5 for non-watermarked)
  expected_5l33_g = [0.5037, 0.5130]
  expected_6mrr_g = [0.5212, 0.5255]

  # Check 5L33
  file_5l33 = os.path.join(output_dir, 'seqs', '5L33.fa')
  assert os.path.exists(file_5l33), "5L33.fa not created"

  with open(file_5l33, 'r') as f:
    content = f.read()
    g_values = [float(g) for g in re.findall(r'mean_g_value=([\d.]+)', content)]

    assert len(g_values) == 2, f"Expected 2 g-values in 5L33, got {len(g_values)}"
    for i, g_val in enumerate(g_values):
      assert abs(g_val - expected_5l33_g[i]) < 0.0001, \
        f"5L33 sample {i+1}: expected g-value {expected_5l33_g[i]}, got {g_val}"

  # Check 6MRR
  file_6mrr = os.path.join(output_dir, 'seqs', '6MRR.fa')
  assert os.path.exists(file_6mrr), "6MRR.fa not created"

  with open(file_6mrr, 'r') as f:
    content = f.read()
    g_values = [float(g) for g in re.findall(r'mean_g_value=([\d.]+)', content)]

    assert len(g_values) == 2, f"Expected 2 g-values in 6MRR, got {len(g_values)}"
    for i, g_val in enumerate(g_values):
      assert abs(g_val - expected_6mrr_g[i]) < 0.0001, \
        f"6MRR sample {i+1}: expected g-value {expected_6mrr_g[i]}, got {g_val}"


def test_g_values_watermarked():
  """Test g-values for watermarked sequences (high g-values expected)."""

  script_dir = os.path.dirname(os.path.abspath(__file__))
  output_dir = os.path.join(script_dir, 'outputs', 'example_1_watermark_outputs')
  parsed_pdbs = os.path.join(script_dir, 'test_data', 'helper_outputs', 'parsed_pdbs.jsonl')

  if os.path.exists(output_dir):
    shutil.rmtree(output_dir)
  os.makedirs(output_dir, exist_ok=True)

  env = os.environ.copy()
  env['PYTHONHASHSEED'] = '0'
  env['OMP_NUM_THREADS'] = '1'

  result = subprocess.run([
    'python', os.path.join(script_dir, 'protein_mpnn_run.py'),
    '--jsonl_path', parsed_pdbs, '--out_folder', output_dir,
    '--num_seq_per_target', '2', '--sampling_temp', '0.1',
    '--seed', '37', '--batch_size', '1', '--watermark',
    '--ngram_len', '4', '--num_leaves', '25',
    '--watermark_keys', '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0'],
    cwd=script_dir, capture_output=True, text=True, env=env)

  assert result.returncode == 0, f"Watermarked run failed: {result.stderr}"

  # Expected g-values (should be >> 0.5 for watermarked with distortionary keys)
  expected_5l33 = [0.7961, 0.7184]
  expected_6mrr = [0.7846, 0.7846]

  # Check 5L33
  fasta_5l33 = os.path.join(output_dir, 'seqs', '5L33.fa')
  assert os.path.exists(fasta_5l33), "Watermarked 5L33.fa not created"

  with open(fasta_5l33, 'r') as f:
    content = f.read()
    g_values = [float(g) for g in re.findall(r'mean_g_value=([\d.]+)', content)]

    assert len(g_values) == 2, "Should have exactly 2 g-values (2 samples)"
    for i, g_val in enumerate(g_values):
      assert abs(g_val - expected_5l33[i]) < 0.0001, \
        f"5L33 sample {i+1}: expected g-value {expected_5l33[i]}, got {g_val}"

  # Check 6MRR
  fasta_6mrr = os.path.join(output_dir, 'seqs', '6MRR.fa')
  assert os.path.exists(fasta_6mrr), "Watermarked 6MRR.fa not created"

  with open(fasta_6mrr, 'r') as f:
    content = f.read()
    g_values = [float(g) for g in re.findall(r'mean_g_value=([\d.]+)', content)]

    assert len(g_values) == 2, "Should have exactly 2 g-values (2 samples)"
    for i, g_val in enumerate(g_values):
      assert abs(g_val - expected_6mrr[i]) < 0.0001, \
        f"6MRR sample {i+1}: expected g-value {expected_6mrr[i]}, got {g_val}"
