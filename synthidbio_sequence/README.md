# SynthID for Biological Sequences

This repository contains code for SynthIDBio-sequence, accompanying the paper **"Function-preserving
biological watermarking of AI-generated protein sequences and structures"**
(SynthIDBio). For more details, please refer to our paper. 

> [!NOTE]
> **Drop-in Integration:** This watermarked version of ProteinMPNN is designed to be a drop-in replacement for existing protein design pipelines. With minimal installation overhead, it can be integrated into your current workflows, enabling the generation of watermarked protein sequences by simply enabling the watermarking flags.

In-vitro validation data is available in the `data/` directory.
This includes:

- `data/sc2rbd_binders.csv` - Binding data for SARS-CoV-2 RBD
- `data/vegh_binders.csv` - Binding data for VEGF-A
- `data/pd_l1_binders.csv` - Binding data for PD-L1
- `data/all_g_values.csv` - G-values for all sequences

## Installation

We recommend using Conda to manage dependencies and isolate the environment.
Follow these steps to set up the environment from scratch on a Linux system:

1. **Install Miniconda** (if Conda is not already installed):
   ```bash
   wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
   bash Miniconda3-latest-Linux-x86_64.sh -b -p $HOME/miniconda
   # Initialize conda for your shell
   eval "$($HOME/miniconda/bin/conda 'shell.bash' 'hook')"
   conda init
   ```
   *Note: You may need to restart your terminal or source your shell*
   *configuration file (e.g., `source ~/.bashrc`) after installation.*

2. **Create and activate a Conda environment**:
   Create a new environment named `synthid_bio` with Python 3.9.18:
   ```bash
   conda create --name synthid_bio python=3.9.18 -y
   conda activate synthid_bio
   ```

3. **Install dependencies**:
   Navigate to the root directory of the cloned repository and run:
   ```bash
   pip install -r requirements.txt
   ```

2. **Install SynthID Text package**:
   ```bash
   cd synthid-text
   pip install -e .
   ```

## Quick Start

### Generate Normal (Non-Watermarked) Sequences
```bash
cd ProteinMPNN/examples
bash submit_example_1.sh
```

**Outputs stored in ProteinMPNN/outputs and includes g-values for detection**:
```
>T=0.1, sample=1, score=0.8581, global_score=0.8581, seq_recovery=0.4151, mean_g_value=0.5255
SIDEDTQKALDFVKALEEANPELMKKVITPDTEMEVNGKKYKGEEIVEFVKELAAKGVK...
```
*Note: g-value ≈ 0.5 indicates no watermark*

### Generate Watermarked Sequences

It is important to note that when comparing watermarked to unwatermarked
sequences, the watermarking args should be the same for both runs as to get
comparative g-values. Without the --watermark arg, watermarking will not be
added to the sequences but the correct g-values will still be computed so you
can see the effect of the watermarking on detection.

#### Example 1: Distortionary Watermarking (Temperature 0.1)

For stronger watermark signal, best for low temperature generation (0.1). Uses repeated keys.

```bash
cd ProteinMPNN
python protein_mpnn_run.py \
    --jsonl_path outputs/example_1_outputs/parsed_pdbs.jsonl \
    --out_folder outputs/example_1_outputs \
    --num_seq_per_target 2 \
    --sampling_temp 0.1 \
    --seed 37 \
    --batch_size 1 \
    --watermark \
    --ngram_len 4 \
    --watermark_keys 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 \
    --num_leaves 25
```

**Output includes high g-values (>>0.5):**
```
>T=0.1, sample=1, score=1.1907, global_score=1.1907, seq_recovery=0.3868, mean_g_value=0.8902
TIDDDTAIALKYVESLELADPALMSKVITPNTKMEYNGREFVGEEIVAYVEEVKKEGVK...
```

#### Example 2: Unwatermarked with Distortionary G-Values (Temperature 0.1)

If you want to run an equivalent unwatermarked sequence with distortionary
g-values, you can run the following command (the key part is removing
--watermark but keeping the same watermark args so g-values are computed
correctly on unwatermarked sequences.):

```bash
cd ProteinMPNN
python protein_mpnn_run.py \
    --jsonl_path outputs/example_1_outputs/parsed_pdbs.jsonl \
    --out_folder outputs/example_1_outputs \
    --num_seq_per_target 2 \
    --sampling_temp 0.1 \
    --seed 37 \
    --batch_size 1 \
    --ngram_len 4 \
    --watermark_keys 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 \
    --num_leaves 25
```

#### Example 3: Non-Distortionary Watermarking (Temperature 0.5)

Minimal impact on sequence quality. Uses non-repeated keys and higher
temperature.

```bash
cd ProteinMPNN
python protein_mpnn_run.py \
    --jsonl_path outputs/example_1_outputs/parsed_pdbs.jsonl \
    --out_folder outputs/example_1_outputs \
    --num_seq_per_target 2 \
    --sampling_temp 0.5 \
    --seed 37 \
    --batch_size 1 \
    --watermark \
    --ngram_len 4 \
    --watermark_keys 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24 \
    --num_leaves 25
```

**Output with moderate g-values:**
```
>T=0.5, sample=1, score=1.2134, global_score=1.2134, seq_recovery=0.4150, mean_g_value=0.5892
SVDPDTKRAHDFVDALELADPALMREVITPDTQMEYNGQRFVGEEIVEFVKQIAAEGR...
```


#### Example 4: Unwatermarked with Non-Distortionary G-Values (Temperature 0.5)

Similarly, if you want to run an equivalent unwatermarked sequence with
non-distortionary g-values, you can run the following command (the key part is
removing --watermark but keeping the same watermark args so g-values are
computed correctly on unwatermarked sequences.):

```bash
cd ProteinMPNN
python protein_mpnn_run.py \
    --jsonl_path outputs/example_1_outputs/parsed_pdbs.jsonl \
    --out_folder outputs/example_1_outputs \
    --num_seq_per_target 2 \
    --sampling_temp 0.5 \
    --seed 37 \
    --batch_size 1 \
    --ngram_len 4 \
    --watermark_keys 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24 \
    --num_leaves 25
```

## Standalone G-Value Calculator

For existing FASTA files, use the standalone `compute_g_values.py` script to
compute g-values without regenerating sequences:

```bash
cd ProteinMPNN
python compute_g_values.py \
    --input_fasta test_data/test_sequences.fa \
    --output_fasta outputs/sequences_with_gvalues.fa \
    --ngram_len 4 \
    --num_leaves 25 \
    --watermark_keys 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
```

**Input FASTA format:**
```
>test_seq_1
KMYEYKKIGDEYVVAIYNESEMMTALTTFCKDKNIKSGTITGIGQIKEITLKYFNPETKE...
>test_seq_2
KLYEYKKIGDEYVVNIYDNTEIVKSILEFCEEKNILSGTIQGIGQIKEIELQFFDPETKE...
```

**Output FASTA format:**
```
>test_seq_1, mean_g_value=0.7286
KMYEYKKIGDEYVVAIYNESEMMTALTTFCKDKNIKSGTITGIGQIKEITLKYFNPETKE...
>test_seq_2, mean_g_value=0.7714
KLYEYKKIGDEYVVNIYDNTEIVKSILEFCEEKNILSGTIQGIGQIKEIELQFFDPETKE...
```

**Important**: Use the same watermark parameters (ngram_len, num_leaves,
watermark_keys) that were used during sequence generation for accurate
detection.

## Watermarking Parameters

| Parameter | Description | Default | Notes |
|-----------|-------------|---------|-------|
| `--watermark` | Enable watermarking | False | Must be set to embed watermarks |
| `--ngram_len` | N-gram length | 5 | Higher = stronger watermark (e.g., 25) |
| `--watermark_keys` | Comma-separated keys | 0,1,2,3,4 | Length must match ngram_len |
| `--context_history_size` | Context size | 1024 | SynthID internal parameter |
| `--watermark_temperature` | Watermark temp | 1.0 | Controls watermark strength |
| `--watermark_top_k` | Top-k value | 21 | Set to vocab size (21 amino acids) |
| `--skip_first_ngram_calls` | Skip first tokens | False | SynthID internal parameter |
| `--num_leaves` | Tournament leaves | 25 | SynthID internal parameter |


## Applying SynthIDBio-sequence to Other Decoders

SynthIDBio-sequence is designed to be model-agnostic and can be integrated into other autoregressive protein sequence decoders (e.g., ESM-IF1, local designs) with minimal changes.

### Integration Steps

To apply watermarking to a custom protein decoder, follow these steps:

1. **Initialize the Processor**: Create an instance of `SynthIDLogitsProcessor` from `synthid_text.logits_processing`.
   * For protein sequences, it is recommended to set `apply_top_k=False` to maintain the full amino acid alphabet, and set `top_k` to the vocabulary size (typically 21 for standard amino acids + mask token).
   * Ensure the `device` matches the model's device.

2. **Enforce Sequential Decoding**: SynthID requires sequential (left-to-right) decoding because the watermark at position $t$ depends on the history of generated residues from $0$ to $t-1$. If your model uses random decoding order (like vanilla ProteinMPNN), you must force it to decode sequentially when watermarking is enabled.

3. **Intercept logits in the sampling loop**:
   * At each step $t$, before sampling, construct the context of already-sampled tokens (IDs) up to $t-1$.
   * Call `watermarked_call` on the processor with the context and the raw logits.
   * Use the returned watermarked scores (which are log probabilities) for sampling.

### Code Example

Here is a conceptual example of integrating SynthIDBio-sequence into a generic autoregressive decoding loop:

```python
from synthid_text.logits_processing import SynthIDLogitsProcessor
import torch

# 1. Initialize the processor
watermark_processor = SynthIDLogitsProcessor(
    ngram_len=5,
    keys=[0, 1, 2, 3, 4],  # Watermark keys (one per depth)
    context_history_size=1024,
    temperature=1.0,
    top_k=21,  # Vocabulary size (e.g., 20 amino acids + X)
    device=device,
    apply_top_k=False,  # Keep full alphabet for protein design
)

# 2. Sequential decoding loop
# generated_tokens: List of already sampled token IDs (shape: [batch_size, current_len])
generated_tokens = []

for t in range(sequence_length):
  # Get raw logits from your model
  logits = model.get_logits(..., generated_tokens)  # [batch_size, vocab_size]

  # Convert context to tensor
  input_ids = torch.tensor(generated_tokens, device=device).unsqueeze(0)  # [1, t]

  # Get watermarked scores (log probabilities) and top_k indices
  watermarked_scores, top_k_indices, _ = watermark_processor.watermarked_call(
      input_ids, logits
  )

  # Convert log probs to probabilities
  probs = torch.softmax(watermarked_scores, dim=-1)

  # Sample next token
  sampled_idx = torch.multinomial(probs, 1)
  next_token = torch.gather(top_k_indices, 1, sampled_idx)

  generated_tokens.append(next_token.item())
```

## Testing

This repository includes a test suite to verify the installation and ensure
watermarking works correctly.

### Test Suite Overview

*   **`test_example_1.py`**: Verifies backward compatibility with standard
    ProteinMPNN (ensures deterministic non-watermarked generation matches
    golden outputs).
*   **`test_example_1_watermark.py`**: Tests end-to-end watermarked
    generation, validating sequences, scores, recovery rates, and exact
    g-values.
*   **`test_g_values.py`**: Tests g-value detection accuracy for both
    watermarked and non-watermarked sequences.

### Running Tests

To run the tests, navigate to the `ProteinMPNN` directory and use `pytest`:

```bash
cd ProteinMPNN

# Run all tests
pytest -v

# Run a specific test file
pytest test_example_1.py -v
pytest test_example_1_watermark.py -v
pytest test_g_values.py -v
```

### Expected Test Output

```
==================== test session starts ====================
test_example_1.py::test_submit_example_1 PASSED           [ 25%]
test_example_1_watermark.py::test_watermark_... PASSED    [ 50%]
test_g_values.py::test_g_values_non_watermarked PASSED    [ 75%]
test_g_values.py::test_g_values_watermarked PASSED        [100%]

==================== 4 passed in 45.23s =====================
```

## Architecture


### Key Components

1. **ProteinMPNN** (`protein_mpnn_run.py`, `protein_mpnn_utils.py`)
   - Protein sequence generation model
   - Modified to support watermarking during decoding
   - Forces left-to-right decoding when watermarking enabled

2. **SynthID Text** (`synthid-text/`)
   - Watermarking logic processor
   - G-value computation for detection
   - Tournament-based token selection

3. **Detector** (integrated in `protein_mpnn_run.py`)
   - Always-on g-value computation
   - Uses same SynthID processor for detection
   - Independent of watermarking mode

## Citing this work

TODO

### Contained Code

- **ProteinMPNN** (`ProteinMPNN/`): [MIT License](ProteinMPNN/LICENSE)
  - Copyright (c) 2022 Justas Dauparas
  - Original publication: Dauparas et al., "Robust deep learning-based protein sequence design using ProteinMPNN" (2022)

- **SynthID-text** (`synthid-text/`): [Apache License 2.0](synthid-text/LICENSE)
  - Copyright Google DeepMind
  - Watermarking technology for text and sequences

### Modified and Added Files in ProteinMPNN

To integrate SynthID watermarking and ensure determinism, the following files in the `ProteinMPNN` directory were modified or added:

#### Modified Files
*   **`ProteinMPNN/protein_mpnn_run.py`**:
    *   Added command-line arguments to configure SynthID watermarking (e.g., `--watermark`, `--ngram_len`, `--watermark_keys`, `--num_leaves`).
    *   Imports `SynthIDLogitsProcessor` and `mean_score` from `synthid_text`.
    *   Initializes the `SynthIDLogitsProcessor` and passes it to the model's `sample` function.
    *   Enforces `batch_size=1` when watermarking is active.
    *   Computes g-values for all generated sequences and appends the `mean_g_value` to the output FASTA headers.
*   **`ProteinMPNN/protein_mpnn_utils.py`**:
    *   Modified the `sample` method of `ProteinMPNN` class to accept `watermark_processor`.
    *   Forces left-to-right sequential decoding when `watermark_processor` is present, overriding the default random decoding order.
    *   Enforces `batch_size=1` check inside `sample` when `watermark_processor` is present.
    *   Intercepts logits at each step of the decoding loop and applies `watermark_processor.watermarked_call` to compute watermarked scores before sampling.
    *   Modified `tied_sample` signature to accept `watermark_processor` for compatibility.
*   **`ProteinMPNN/helper_scripts/parse_multiple_chains.py`**:
    *   Sorted the output of `glob.glob` to ensure deterministic parsing order of PDB files for testing.

#### Added Files
*   **`ProteinMPNN/compute_g_values.py`**:
    *   Standalone script to compute g-values for existing sequences in FASTA format, using `SynthIDLogitsProcessor` for detection.
*   **`ProteinMPNN/test_*.py`**:
    *   Pytest suite (10 files) for validating various ProteinMPNN examples with and without watermarking, ensuring exact score and g-value matches.
*   **`ProteinMPNN/test_data/`**:
    *   Directory containing golden outputs and helper inputs used by the test suite to ensure determinism.
*   **`ProteinMPNN/examples/*_watermark.sh`**:
    *   Example bash scripts (for examples 2, 3, 4, 5, 6, 8) demonstrating how to run ProteinMPNN with watermarking parameters.

### Licensing & Disclaimer
Copyright 2025 Google LLC

All software is licensed under the Apache License, Version 2.0 (Apache 2.0);
you may not use this file except in compliance with the Apache 2.0 license.
You may obtain a copy of the Apache 2.0 license at:
https://www.apache.org/licenses/LICENSE-2.0

All other materials are licensed under the Creative Commons Attribution 4.0
International License (CC-BY). You may obtain a copy of the CC-BY license at:
https://creativecommons.org/licenses/by/4.0/legalcode

Unless required by applicable law or agreed to in writing, all software and
materials distributed here under the Apache 2.0 or CC-BY licenses are
distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
either express or implied. See the licenses for the specific language
governing permissions and limitations under those licenses.

This is not an official Google product.

