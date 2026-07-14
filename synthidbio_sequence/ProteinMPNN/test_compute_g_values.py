import os
import subprocess
import shutil


def test_compute_g_values():
  script_dir = os.path.dirname(os.path.abspath(__file__))
  input_fasta = os.path.join(script_dir, 'test_data', 'test_sequences.fa')
  output_dir = os.path.join(script_dir, 'outputs', 'test_compute_g_values')
  output_fasta = os.path.join(output_dir, 'output.fa')

  if os.path.exists(output_dir):
    shutil.rmtree(output_dir)
  os.makedirs(output_dir, exist_ok=True)

  env = os.environ.copy()
  env['PYTHONHASHSEED'] = '0'
  env['OMP_NUM_THREADS'] = '1'

  result = subprocess.run(
    ['python', os.path.join(script_dir, 'compute_g_values.py'),
    '--input_fasta', input_fasta,
    '--output_fasta', output_fasta,
    '--ngram_len', '4',
    '--num_leaves', '25',
    '--watermark_keys', '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0'],
    cwd=script_dir, capture_output=True, text=True, env=env)

  assert result.returncode == 0, f"Failed: {result.stderr}"
  assert os.path.exists(output_fasta), f"Output file not created: {output_fasta}"

  golden_g_values = {
    'test_seq_1': 0.7286,
    'test_seq_2': 0.7714,
    'test_seq_3_multichain': 0.5512,
  }

  with open(output_fasta, 'r') as f:
    content = f.read()

  lines = content.strip().split('\n')
  for i in range(0, len(lines), 2):
    if i + 1 < len(lines):
      header = lines[i]
      seq = lines[i + 1]

      for seq_name in golden_g_values.keys():
        if seq_name in header:
          if 'mean_g_value=' in header:
            g_value_str = header.split('mean_g_value=')[1].split(',')[0].split()[0]
            g_value = float(g_value_str)

            if golden_g_values[seq_name] is not None:
              expected = golden_g_values[seq_name]
              assert abs(g_value - expected) < 0.0001, (
                f'{seq_name}: expected g-value {expected}, got {g_value}')
            else:
              print(f'{seq_name}: g-value = {g_value}')
