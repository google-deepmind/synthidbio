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

"""Pytest test for ProteinMPNN example_7 with unconditional probabilities."""

import os
import subprocess
import shutil
import pytest
import numpy as np


def test_submit_example_7():
  """Test that submit_example_7.sh produces unconditional probability outputs."""

  script_dir = os.path.dirname(os.path.abspath(__file__))
  examples_dir = os.path.join(script_dir, 'examples')
  script_path = os.path.join(examples_dir, 'submit_example_7.sh')
  output_dir = os.path.join(script_dir, 'outputs', 'example_7_outputs')

  if os.path.exists(output_dir):
    shutil.rmtree(output_dir)

  result = subprocess.run(
    ['bash', script_path],
    cwd=examples_dir,
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
