"""Pytest test for ProteinMPNN example_7 with watermarking and unconditional probabilities."""

import os
import subprocess
import shutil
import pytest
import numpy as np


def test_submit_example_7_watermark():
  """Test that submit_example_7.sh with watermarking produces unconditional probability outputs."""

  script_dir = os.path.dirname(os.path.abspath(__file__))
  examples_dir = os.path.join(script_dir, 'examples')
  output_dir = os.path.join(script_dir, 'outputs', 'example_7_watermark_outputs')

  if os.path.exists(output_dir):
    shutil.rmtree(output_dir)

  # Create output directory
  os.makedirs(output_dir, exist_ok=True)

  # Create watermarked version by running example 7 with watermark flags
  folder_with_pdbs = os.path.join(script_dir, 'inputs', 'PDB_monomers', 'pdbs')
  path_for_parsed_chains = os.path.join(output_dir, 'parsed_pdbs.jsonl')

  # Parse chains
  parse_result = subprocess.run(
    ['python', os.path.join(script_dir, 'helper_scripts', 'parse_multiple_chains.py'),
    '--input_path', folder_with_pdbs,
    '--output_path', path_for_parsed_chains],
    cwd=script_dir,
    capture_output=True,
    text=True
  )
  assert parse_result.returncode == 0, f"Parse failed: {parse_result.stderr}"

  # Run with watermarking
  result = subprocess.run(
    ['python', os.path.join(script_dir, 'protein_mpnn_run.py'),
    '--jsonl_path', path_for_parsed_chains,
    '--out_folder', output_dir,
    '--num_seq_per_target', '1',
    '--sampling_temp', '0.1',
    '--unconditional_probs_only', '1',
    '--seed', '37',
    '--batch_size', '1',
    '--watermark',
    '--ngram_len', '4',
    '--watermark_keys', '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0',
    '--num_leaves', '25'],
    cwd=script_dir,
    capture_output=True,
    text=True,
    env={**os.environ, 'PYTHONHASHSEED': '0', 'OMP_NUM_THREADS': '1'}
  )

  assert result.returncode == 0, f"Script failed: {result.stderr}"

  # Verify output directory and unconditional_probs_only directory exist
  assert os.path.exists(output_dir), "Output directory not created"
  probs_dir = os.path.join(output_dir, 'unconditional_probs_only')
  assert os.path.exists(probs_dir), "unconditional_probs_only directory not created"

  # Verify .npz files are created for expected proteins
  expected_proteins = ['5L33', '6MRR']
  for protein_id in expected_proteins:
    npz_path = os.path.join(probs_dir, f'{protein_id}.npz')
    assert os.path.exists(npz_path), f"{protein_id}.npz not created"

    # Verify the npz file can be loaded and has expected structure
    data = np.load(npz_path)
    assert 'log_p' in data, f"{protein_id}.npz missing 'log_p' key"
    log_probs = data['log_p']
    assert log_probs.ndim == 3, f"Expected 3D array for log_probs, got {log_probs.ndim}D"
    assert log_probs.shape[2] == 21, f"Expected 21 amino acid probabilities"


if __name__ == '__main__':
  pytest.main([__file__, '-v'])
