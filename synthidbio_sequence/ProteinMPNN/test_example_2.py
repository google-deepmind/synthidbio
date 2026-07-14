"""Pytest test for ProteinMPNN example_2 script with exact value matching."""

import os
import subprocess
import shutil
import pytest


# Golden values for exact matching
GOLDEN_VALUES = {
  '3HTN': {
    'sample1_score': '0.7378',
    'sample1_global_score': '0.9215',
    'sample1_seq_recovery': '0.5745',
    'sample1_mean_g_value': '0.5036',
    'sample1_seq': 'MMYKYLKIGNKYIVSINNNTDIVKALKEFCKEKNIKSGTINGIGQVKSVTLKFYNFETKTSEEKTFNAPFTISNLTGFISEYNNDIYLDLHITFGDSNFSALAGHLISATVGGECKLVIEDYKEKISTKYNSELGLNLLDFNK/HMYKYKKIGNKYLVSINNNKDLVESIKAFCKEKNIKSGTVNGIGSISKVTLEFFDPEXXXXKTKTFNDYYEISNLTGFISTKDGEVFLDLHITIGDSNFSALAGHLVSAIVNGHAELKIEDFNKEVNVKYDEKLGLYLLDFEK',
    'sample2_score': '0.7149',
    'sample2_global_score': '0.9057',
    'sample2_seq_recovery': '0.5745',
    'sample2_mean_g_value': '0.5192',
    'sample2_seq': 'MLYDYKKIGNKYLVSINNNTELVTAIKEFCREKNIKSGTINGIGQVKSVTLKFYNFETKEYELKTFNENLTISNLTGLIGTKDGEVFLDLHITVGKKDFSALAGHLVSAVVNGTATLVVEDYNEEISYKYNEETGLWLLDFNK/NMYSYKKIGNKYIVSINNGKDLVTSIKEFCKDKNIKSGTINGIGSISKVTLEFFDPNXXXXTKKTINDYLEISNLTGFISTKNGEVLVDLHITVGDSNFSALAGHLVSAIVNGIAELIVEDFKEIVNVKYNEETGLWLLDFNK',
  },
  '4YOW': {
    'sample1_score': '0.7220',
    'sample1_global_score': '1.0003',
    'sample1_seq_recovery': '0.5947',
    'sample1_mean_g_value': '0.5079',
    'sample1_seq': 'MKIVAADTGGYLLDENYKPIGPIATVAVLVEKPYRTSDEFLVRYLDPENYDLSSHEGLYHEVELAIELARKVKPDLIHLDLDLGGVPLAELTPEVIEKLQISAETKKLLKELAKTLTPLAQAFLAETGIPILCIGSRSVAVKIAEIYASVAAVKWALEHVKERKGLRVGLVYATDVEIEDDSIIGTSLDPRDGGLHVRIETEIPEGIKYELYPNPLRRNHMIFEVTV/XXXX',
    'sample2_score': '0.7613',
    'sample2_global_score': '1.0220',
    'sample2_seq_recovery': '0.5903',
    'sample2_mean_g_value': '0.5033',
    'sample2_seq': 'MKIVAADTGGYLLNENNEPIGRIATVAVLVEKPYRTSDVFKVRYLDPTKYDLSGHDGFYRELELAIELAREVKPDLIHLDLDLGGVPLYEMDEELINKLQISEETKKILKEMAKTLSPLAKAFLAETGIPILLTGDRSVPVRIAHIYASGEAVKWALDHVKERKGLRVRLEEATSVTIGADSITVTSLDPRDGGLYGTVKTTVPTGITYELYPDPLRTKHMIFEVTV/XXXX',
  },
}


def test_submit_example_2():
  """Test that submit_example_2.sh produces outputs with exact value matching."""

  script_dir = os.path.dirname(os.path.abspath(__file__))
  examples_dir = os.path.join(script_dir, 'examples')
  script_path = os.path.join(examples_dir, 'submit_example_2.sh')
  output_dir = os.path.join(script_dir, 'outputs', 'example_2_outputs')

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

  # Verify output directory and files exist
  assert os.path.exists(output_dir), "Output directory not created"
  seqs_dir = os.path.join(output_dir, 'seqs')
  assert os.path.exists(seqs_dir), "seqs directory not created"

  # Test each protein's FASTA file
  for protein_id in GOLDEN_VALUES.keys():
    fasta_path = os.path.join(seqs_dir, f'{protein_id}.fa')
    assert os.path.exists(fasta_path), f"{protein_id}.fa not created"

    with open(fasta_path, 'r') as f:
      lines = f.readlines()

    golden_data = GOLDEN_VALUES[protein_id]

    # Determine expected number of samples (skip native sequence which is first 2 lines)
    sample_keys = [k for k in golden_data.keys() if k.startswith('sample')]
    num_samples = len(set(k.split('_')[0] for k in sample_keys))

    # Expected lines: 2 (native header + seq) + num_samples * 2 (sample headers + seqs)
    expected_lines = 2 + num_samples * 2
    assert len(lines) == expected_lines, f"Expected {expected_lines} lines in {protein_id}.fa, got {len(lines)}"

    # Verify each sample
    for i in range(1, num_samples + 1):
      sample_prefix = f'sample{i}'
      header_idx = (i - 1) * 2 + 2 # +2 to account for native sequence
      seq_idx = header_idx + 1

      header = lines[header_idx].strip()
      sequence = lines[seq_idx].strip()

      # Verify score
      assert f"score={golden_data[f'{sample_prefix}_score']}" in header, \
        f"Score mismatch for {protein_id} sample {i}"

      # Verify global_score
      assert f"global_score={golden_data[f'{sample_prefix}_global_score']}" in header, \
        f"Global score mismatch for {protein_id} sample {i}"

      # Verify seq_recovery
      assert f"seq_recovery={golden_data[f'{sample_prefix}_seq_recovery']}" in header, \
        f"Seq recovery mismatch for {protein_id} sample {i}"

      # Verify mean_g_value (if watermarked)
      if f'{sample_prefix}_mean_g_value' in golden_data:
        assert f"mean_g_value={golden_data[f'{sample_prefix}_mean_g_value']}" in header, \
          f"Mean g-value mismatch for {protein_id} sample {i}"

      # Verify sequence
      assert sequence == golden_data[f'{sample_prefix}_seq'], \
        f"Sequence mismatch for {protein_id} sample {i}"


if __name__ == '__main__':
  pytest.main([__file__, '-v'])
