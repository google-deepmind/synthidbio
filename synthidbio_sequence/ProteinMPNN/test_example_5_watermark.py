"""Pytest test for ProteinMPNN example_5 script with watermarking and exact value matching."""

import os
import subprocess
import shutil
import pytest


# Golden values for exact matching
GOLDEN_VALUES = {
  '3HTN': {
    'sample1_score': '0.7298',
    'sample1_global_score': '0.9335',
    'sample1_seq_recovery': '0.5774',
    'sample1_mean_g_value': '0.5371',
    'sample1_seq': 'SMYSYKKIGNKYIVSINNHTEIVKALKKFCEEKNIKSGSINGIGQVKEVTLKFYNLETKEEELKTFKDYFEISNLTGFISMHDNKVFLDLHITFGDSNFSALAGHLVSAIVDGICELIIEDYNELISTKYDEELGLWLLDFNK/SMYSYKKIGNKYIVSINNHTDIVTAIKKFCEDKKIKSGTINGIGQVSSVTLEFFNPETKEKEEKTFNKQFTISNLTGFISTINGKVFLDLHITFGDENFSALAGHLLSAIVDGKCILEIEDFNEIINKKYNEELGLNLLDFNS',
    'sample2_score': '0.7323',
    'sample2_global_score': '0.9333',
    'sample2_seq_recovery': '0.6264',
    'sample2_mean_g_value': '0.5583',
    'sample2_seq': 'NMYSYKKIGNKYIVSINNHTEIVKALKAFCKEKKIESGSINGIGQISKVTLRFYDFETKEYTEKTFNDYLEISNLTGFISTYNGEVFLDLHITVGKSDFSALAGHLISAVVNGTCELIVEDYKEKLSRKYDEELGLYLLDFNK/NMYSYKKIGNKYIVSINNHTDIYEALLNFVKEKNIKSGTINGIGQISKLTLKFFNIETKEEEKKTFNQQLDISNLTGFISEKDGKPFLDLHITAGKSDFSALAGHLESAIVNGKAEIIVEDYKEKINVKYNEELGLYLLDFNK',
  },
  '4YOW': {
    'sample1_score': '0.7091',
    'sample1_global_score': '0.8861',
    'sample1_seq_recovery': '0.6212',
    'sample1_mean_g_value': '0.4945',
    'sample1_seq': 'MKIVAADTGGAVLDESFQPVGLIATVAVVVEKPYRTSEEFLVRYLDPYNYDLSGHQHLYDELELAIELAEKVKPDLIHLDLDCGGVDLAEMTPELIDKLPISPETKALLKELAKTLTPLAQAYKAKTGIPILLTGSRSVPVRIAHIYASGAAVKWALENVKEKKGLRVGLERAVSVEIKENEIIVRSLDPRDGGLYGRIETEVPEGIKYELYPNPLATGHNVFEITT/MKIVAADTGGALLDENYQPVGLIATVAVVVEYPYRTSKEFLVRYMDPLNYDLSSDEHIYLELELAIELAEKVNPDLIHLDIDLGGVNLADLDPEVIDALPISEETKERLKKLAEKLAPLAQAFLAKTGIPILAIGSRSVPVRIADIYAGVMAVKWALDHVKELKGLRVGLPYATSVEIKEKKIVGRSLDPRDGGLYQEVETEVPEGVEYELYPNPLRIGHMVFEIRV',
    'sample2_score': '0.7121',
    'sample2_global_score': '0.8800',
    'sample2_seq_recovery': '0.6028',
    'sample2_mean_g_value': '0.4812',
    'sample2_seq': 'MKIVAADTGGAVLDESFQPVGLIATVAVVVEKPYTTSDKFKVRYHDPFNYDLSGHEHIYDEIKLAIELAEEVKPDLIHLDITLGGVDVADLTPEVIDKLQISEEEKAILKELAKELTPLAQEYKKKTGIPILAIGDESVPVRIAHIYASAEAVKWALEHVKELKGLRVGLEEAVAVEIGEDSIKATSLDPRDGGLHGEIKTKVPEGVKYELYPNPLRREHLVFEITV/MKIVAADTGGALLDENFQPVGLIATVAVLVEYPYRTSKEFLVRYMDPLAYDLTSDEHLLLELDLAIELARRVHPDEIRLDLDLGGVELADLTPELIDALQISEETKARLRRLAETLAPRAAAFRAETGIPVRAVGDASVPVHIADIYAGAASVIWALENVKERKGLRVGLPYATRVEIKEDKVVATSLDPRHGGLYQEIKVKVPEGITYELYPDPLRIGHMIFEVET',
  },
}


def test_submit_example_5_watermark():
  """Test that submit_example_5_watermark.sh produces outputs with exact value matching."""

  script_dir = os.path.dirname(os.path.abspath(__file__))
  examples_dir = os.path.join(script_dir, 'examples')
  script_path = os.path.join(examples_dir, 'submit_example_5_watermark.sh')
  output_dir = os.path.join(script_dir, 'outputs', 'example_5_watermark_outputs')

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
