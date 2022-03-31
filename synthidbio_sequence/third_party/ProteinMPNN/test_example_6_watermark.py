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

"""Pytest test for ProteinMPNN example_6 script with watermarking and exact value matching."""

import os
import subprocess
import shutil
import pytest


# Golden values for exact matching
GOLDEN_VALUES = {
  '4GYT': {
    'sample1_score': '0.8914',
    'sample1_global_score': '0.8914',
    'sample1_seq_recovery': '0.4181',
    'sample1_mean_g_value': '0.5157',
    'sample1_seq': 'SLRLPPYREFEAAIAVLDLPVSASELAGLILGYLAAGRTDLGRAWLRALLNGRTDPASQAALAALLALFDILEQQLSDPALPLELLLPPEDASLQERAKAFADFCRGFVRGLELAGVGAASLAKPESRAALARLRELARLDASTLQAGPADEAALQAAIAWARQSIVAIHQDLATTG/SLRLPPYREFEAAIAVLDLPVSASELAGLILGYLAAGRTDLGRAWLRALLNGRTDPASQAALAALLALFDILEQQLSDPALPLELLLPPEDASLQERAKAFADFCRGFVRGLELAGVGAASLAKPESRAALARLRELARLDASTLQAGPADEAALQAAIAWARQSIVAIHQDLATTG',
    'sample2_score': '0.8756',
    'sample2_global_score': '0.8756',
    'sample2_seq_recovery': '0.4463',
    'sample2_mean_g_value': '0.4387',
    'sample2_seq': 'SLTLPPYEEFAAAIAVLRLPVSPSELAGLILGYLVAGKTELGRAYIEALLNGRTDAESQAALAALLELFDILEKQLNDPNYELELLLPPEDASLKERCKAFSEFCAGFVKGLELAGVTAESFAKEESKEAYAKLKEYAKMDCSTFKEGEEDRKKLKELEEEAKEAILAIHKDIKENG/SLTLPPYEEFAAAIAVLRLPVSPSELAGLILGYLVAGKTELGRAYIEALLNGRTDAESQAALAALLELFDILEKQLNDPNYELELLLPPEDASLKERCKAFSEFCAGFVKGLELAGVTAESFAKEESKEAYAKLKEYAKMDCSTFKEGEEDRKKLKELEEEAKEAILAIHKDIKENG',
  },
  '6EHB': {
    'sample1_score': '0.9056',
    'sample1_global_score': '0.9056',
    'sample1_seq_recovery': '0.5372',
    'sample1_mean_g_value': '0.4838',
    'sample1_seq': 'GGLNLRKPKPGSVVYQSNGSTLSLGGYARAILKIIDGKAKDESKGGVSLLKRDQINDDLYGEGYIELEFTTNDNGKDAVNNNLNVKNLYAGIGGKWGTVTYGKNDGALQAIRDFTDIGPYSGATAAPLIPVGDNIDNTISYSRTVGDLTIRASYKFADMVYVDSNGNVVSESEAAKVSDNGKDGWSVSAIYDFGDTGWRVGAGAAHQGDQWAVMLAASYEADNFYVSALLTYGQLDKGVDYVGVELAAAYKVGNWTFVANYNLALVDNEVSSDDLSVGAEYQFTPRFSVFVEYRFNLLDXXXSSYVASLDELYLGIRTDF/GGLNLRKPKPGSVVYQSNGSTLSLGGYARAILKIIDGKAKDESKGGVSLLKRDQINDDLYGEGYIELEFTTNDNGKDAVNNNLNVKNLYAGIGGKWGTVTYGKNDGALQAIRDFTDIGPYSGATAAPLIPVGDNIDNTISYSRTVGDLTIRASYKFADMVYVDSNGNVVSESEAAKVSDNGKDGWSVSAIYDFGDTGWRVGAGAAHQGDQWAVMLAASYEADNFYVSALLTYGQLDKGVDYVGVELAAAYKVGNWTFVANYNLALVDNEVSSDDLSVGAEYQFTPRFSVFVEYRFNLLDXXXSSYVASLDELYLGIRTDF/GGLNLRKPKPGSVVYQSNGSTLSLGGYARAILKIIDGKAKDESKGGVSLLKRDQINDDLYGEGYIELEFTTNDNGKDAVNNNLNVKNLYAGIGGKWGTVTYGKNDGALQAIRDFTDIGPYSGATAAPLIPVGDNIDNTISYSRTVGDLTIRASYKFADMVYVDSNGNVVSESEAAKVSDNGKDGWSVSAIYDFGDTGWRVGAGAAHQGDQWAVMLAASYEADNFYVSALLTYGQLDKGVDYVGVELAAAYKVGNWTFVANYNLALVDNEVSSDDLSVGAEYQFTPRFSVFVEYRFNLLDXXXSSYVASLDELYLGIRTDF',
    'sample2_score': '0.9015',
    'sample2_global_score': '0.9015',
    'sample2_seq_recovery': '0.5215',
    'sample2_mean_g_value': '0.5266',
    'sample2_seq': 'GGLNLASDLPGKTVYQENGRSLQLGGYARAELLIKDGKAKDASKGSVSLLATDKINDDLYGEGYIRLDFTVNDNGTDAVNNNLNVRKLYSGIGGKWGTVTYGKNNGALQDIKDFTDIMPVFGNNAAPLIPVGDNIDNTISYSRTDGNLKVRASYQFANMIYVDSNGNVVAESEAAYYSDNGKDGFSASAIYDFGDTGWSVGAGAAYQGDQWQVMVAASYKKDNFYVSALLTAGRLADGVDYYGVSVAASYDVGNWRFTANYDVAYTDNKVSADNLSVAATYDFTPYFSTYVAYNKNLLDXXXSSYVASADTLAVGIETRF/GGLNLASDLPGKTVYQENGRSLQLGGYARAELLIKDGKAKDASKGSVSLLATDKINDDLYGEGYIRLDFTVNDNGTDAVNNNLNVRKLYSGIGGKWGTVTYGKNNGALQDIKDFTDIMPVFGNNAAPLIPVGDNIDNTISYSRTDGNLKVRASYQFANMIYVDSNGNVVAESEAAYYSDNGKDGFSASAIYDFGDTGWSVGAGAAYQGDQWQVMVAASYKKDNFYVSALLTAGRLADGVDYYGVSVAASYDVGNWRFTANYDVAYTDNKVSADNLSVAATYDFTPYFSTYVAYNKNLLDXXXSSYVASADTLAVGIETRF/GGLNLASDLPGKTVYQENGRSLQLGGYARAELLIKDGKAKDASKGSVSLLATDKINDDLYGEGYIRLDFTVNDNGTDAVNNNLNVRKLYSGIGGKWGTVTYGKNNGALQDIKDFTDIMPVFGNNAAPLIPVGDNIDNTISYSRTDGNLKVRASYQFANMIYVDSNGNVVAESEAAYYSDNGKDGFSASAIYDFGDTGWSVGAGAAYQGDQWQVMVAASYKKDNFYVSALLTAGRLADGVDYYGVSVAASYDVGNWRFTANYDVAYTDNKVSADNLSVAATYDFTPYFSTYVAYNKNLLDXXXSSYVASADTLAVGIETRF',
  },
}


def test_submit_example_6_watermark():
  """Test that submit_example_6_watermark.sh produces outputs with exact value matching."""

  script_dir = os.path.dirname(os.path.abspath(__file__))
  examples_dir = os.path.join(script_dir, 'examples')
  script_path = os.path.join(examples_dir, 'submit_example_6_watermark.sh')
  output_dir = os.path.join(script_dir, 'outputs', 'example_6_watermark_outputs')

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
