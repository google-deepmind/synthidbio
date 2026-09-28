# SynthID Bio: Biological Sequence and Structure Watermarking

SynthID Bio is a family of methods developed by Google DeepMind for embedding
highly detectable yet function-preserving watermarks directly into AI-generated
biological sequences and structures.

For more details, please refer to our paper: [**"Function-preserving watermarking of AI-generated proteins"**](https://www.nature.com/articles/s41586-026-10965-y).

## Overview

SynthID Bio provides watermarking for autoregressive inverse folding models
(such as ProteinMPNN) and structure prediction models (such as AlphaFold 3):

-   [**SynthID Bio-structure**](#synthid-bio-structure): Fine-tuned AlphaFold 3
    model that embeds imperceptible watermarks into generated 3D biomolecular
    structures.
-   [**SynthID Bio-sequence**](#synthid-bio-sequence): Watermarking protein
    sequences during autoregressive decoding with ProteinMPNN while preserving
    function and expressivity.



## SynthID Bio-Structure

`SynthID Bio-structure` is a fine-tuned AlphaFold 3 (AF3) model that embeds an
imperceptible watermark into biomolecular structures during sampling.

For full instructions on downloading model weights and running watermarked structure predictions with AlphaFold 3, please refer to the [AlphaFold 3 Repository](https://github.com/google-deepmind/alphafold3).



## SynthID Bio-Sequence

`SynthID Bio-sequence` introduces watermarked sampling into ProteinMPNN.

> [!NOTE]
> **Drop-in Integration:** This watermarked version of ProteinMPNN is designed to be a drop-in replacement for existing protein design pipelines. With minimal installation overhead, it can be integrated into your current workflows, enabling the generation of watermarked protein sequences by simply enabling the watermarking flags.

### Installation

We recommend using [`uv`](https://github.com/astral-sh/uv) or standard Python virtual environments (`venv`) to manage dependencies.

Follow these steps to set up the environment from scratch on a Linux system:

1. **Create and activate a virtual environment**:

   ```bash
   uv venv synthid_bio --python 3.9
   source synthid_bio/bin/activate
   ```
   *(Or using standard `venv`: `python3.9 -m venv synthid_bio && source synthid_bio/bin/activate`)*

2. **Install dependencies**:

   ```bash
   cd synthidbio_sequence
   uv pip install -r requirements.txt
   ```
   *(Or using `pip`: `pip install -r requirements.txt`)*

3. **Install SynthID Text package**:

    ```bash
    uv pip install -e third_party/synthid-text
    ```

    *(Or using `pip`: `pip install -e third_party/synthid-text`)*

### Quick Start

Navigate to the ProteinMPNN directory before running generation scripts:

```bash
cd third_party/ProteinMPNN
```

#### Generate Normal (Non-Watermarked) Sequences

Run Example 1 to generate baseline unwatermarked sequences and pre-parsed
inputs:

```bash
(cd examples && bash submit_example_1.sh)
```

**Outputs are stored in `outputs/example_1_outputs/seqs/` and include baseline
g-values (~0.5) for detection:**

```
>T=0.1, sample=1, score=0.8581, global_score=0.8581, seq_recovery=0.4151, mean_g_value=0.5037
SIDEDTQKALDFVKALEEANPELMKKVITPDTEMEVNGKKYKGEEIVEFVKELAAKGVK...
```

#### Generate Watermarked Sequences

When comparing watermarked to unwatermarked sequences, the watermarking
arguments should remain identical across runs so that comparative g-values can
be evaluated. Without the `--watermark` flag, watermarks are not embedded into
generated sequences, but detection g-values are still computed so you can
measure the watermark's signal strength against the unwatermarked baseline.

> [!TIP] If you have not run `submit_example_1.sh` above, you can substitute
> `--jsonl_path outputs/example_1_outputs/parsed_pdbs.jsonl` with the pre-parsed
> dataset at `--jsonl_path test_data/helper_outputs/parsed_pdbs.jsonl`.

##### Example 1: Distortionary Watermarking, Low Sampling Temperature

Use repeating keys for a stronger watermark signal, best suited for
low-temperature generation (e.g., 0.1):

```bash
python protein_mpnn_run.py \
    --jsonl_path outputs/example_1_outputs/parsed_pdbs.jsonl \
    --out_folder outputs/example_1_watermark_outputs \
    --num_seq_per_target 2 \
    --sampling_temp 0.1 \
    --seed 37 \
    --batch_size 1 \
    --watermark \
    --ngram_len 4 \
    --watermark_keys 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
```

**Output includes high g-values (>>0.5):**
```
>T=0.1, sample=1, score=1.1907, global_score=1.1907, seq_recovery=0.3868, mean_g_value=0.8902
TIDDDTAIALKYVESLELADPALMSKVITPNTKMEYNGREFVGEEIVAYVEEVKKEGVK...
```

##### Example 2: Unwatermarked with Distortionary G-Values (Temperature 0.1)

To run an equivalent unwatermarked sequence with distortionary g-values, remove
`--watermark` while keeping the same watermarking arguments:

```bash
python protein_mpnn_run.py \
    --jsonl_path outputs/example_1_outputs/parsed_pdbs.jsonl \
    --out_folder outputs/example_1_unwatermarked_outputs \
    --num_seq_per_target 2 \
    --sampling_temp 0.1 \
    --seed 37 \
    --batch_size 1 \
    --ngram_len 4 \
    --watermark_keys 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
```

##### Example 3: Non-Distortionary Watermarking, Medium Sampling Temperature

Use non-repeating keys for minimal impact on sequence quality at
medium-to-higher sampling temperatures (e.g., 0.5):

```bash
python protein_mpnn_run.py \
    --jsonl_path outputs/example_1_outputs/parsed_pdbs.jsonl \
    --out_folder outputs/example_3_watermark_outputs \
    --num_seq_per_target 2 \
    --sampling_temp 0.5 \
    --seed 37 \
    --batch_size 1 \
    --watermark \
    --ngram_len 4 \
    --watermark_keys 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24
```

**Output with moderate g-values:**
```
>T=0.5, sample=1, score=1.2134, global_score=1.2134, seq_recovery=0.4150, mean_g_value=0.5892
SVDPDTKRAHDFVDALELADPALMREVITPDTQMEYNGQRFVGEEIVEFVKQIAAEGR...
```

##### Example 4: Unwatermarked with Non-Distortionary G-Values (Temperature 0.5)

Similarly, to run an equivalent unwatermarked sequence with non-distortionary
g-values, remove `--watermark` while keeping the same watermarking arguments:

```bash
python protein_mpnn_run.py \
    --jsonl_path outputs/example_1_outputs/parsed_pdbs.jsonl \
    --out_folder outputs/example_3_unwatermarked_outputs \
    --num_seq_per_target 2 \
    --sampling_temp 0.5 \
    --seed 37 \
    --batch_size 1 \
    --ngram_len 4 \
    --watermark_keys 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24
```

### Standalone G-Value Calculator

For existing FASTA files, use the standalone `compute_g_values.py` script to
compute g-values without regenerating sequences:

```bash
python compute_g_values.py \
    --input_fasta test_data/test_sequences.fa \
    --output_fasta outputs/sequences_with_gvalues.fa \
    --ngram_len 4 \
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

**Important**: Use the same watermark parameters (e.g., `--ngram_len`,
`--watermark_keys`) as those used during sequence generation for detection.

### Watermarking Parameters

Parameter                  | Description          | Default      | Notes
-------------------------- | -------------------- | ------------ | -----
`--watermark`              | Enable watermarking  | False        | Must be set to embed watermarks
`--ngram_len`              | N-gram length        | 4            | Context window conditioning watermark (e.g., 2, 4)
`--watermark_keys`         | Comma-separated keys | 0,1,2,...,24 | Sequence of integer keys, one per depth/tournament layer
`--context_history_size`   | Context size         | 1024         | SynthID internal buffer size to track seen contexts
`--watermark_temperature`  | Watermark temp       | 1.0          | Temperature scaling factor for watermark distortion strength
`--watermark_top_k`        | Top-k value          | 21           | Set to vocab size (21 amino acids + mask token)
`--skip_first_ngram_calls` | Skip first tokens    | True         | Disables watermarking for first (ngram_len - 1) tokens

### Applying SynthID Bio-sequence to Other Decoders

SynthID Bio-sequence is designed to be model-agnostic and can be integrated into
other autoregressive protein sequence decoders with minimal changes.

#### Integration Steps

To apply watermarking to a custom protein decoder, follow these steps:

1. **Initialize the Processor**: Create an instance of `SynthIDLogitsProcessor` from `synthid_text.logits_processing`.
    *   For protein sequences, set `apply_top_k=False` to maintain the full
        amino acid alphabet, and set `top_k` to the vocabulary size (typically
        21 for standard amino acids + mask token).
    * Ensure the `device` matches the model's device.

2.  **Enforce Sequential Decoding**: SynthID Bio-sequence requires sequential
    (left-to-right) decoding because the watermark at position *t* depends on
    the history of generated residues from *0* to *t* - 1. If your model uses
    random decoding order (like vanilla ProteinMPNN), you must force it to
    decode sequentially when watermarking is enabled.

3. **Intercept logits in the sampling loop**:
   * At each step *t*, before sampling, construct the context of already-sampled tokens (IDs) up to *t* - 1.
   * Call `watermarked_call` on the processor with the context and the raw logits.
   * Use the returned watermarked scores (which are log probabilities) for sampling.

#### Code Example

Here is a conceptual example of integrating SynthID Bio-sequence into a generic
autoregressive decoding loop:

```python
from synthid_text.logits_processing import SynthIDLogitsProcessor
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 1. Initialize the processor
watermark_processor = SynthIDLogitsProcessor(
    ngram_len=4,
    # Watermark keys (one per depth layer)
    keys=[
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18,
        19, 20, 21, 22, 23, 24,
    ],
    context_history_size=1024,
    temperature=1.0,
    top_k=21,  # Vocabulary size (e.g., 20 amino acids + mask token)
    device=device,
    apply_top_k=False,  # Keep full alphabet for protein design
)

# 2. Sequential decoding loop
# generated_tokens: List of already sampled token IDs (shape: [batch_size, current_len])
generated_tokens = []

for t in range(sequence_length):
  # Get raw logits from your model
  logits = model.get_logits(..., generated_tokens)  # [batch_size, vocab_size]

  # Convert context to int64 tensor
  input_ids = torch.tensor(
      generated_tokens, dtype=torch.long, device=device
  ).unsqueeze(0)  # [1, t]

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

### Testing

This repository includes a test suite to verify the installation and ensure
watermarking works correctly.

#### Test Suite Overview

*   **`test_example_1.py`**: Verifies deterministic non-watermarked and
    watermarked generation (validating sequences, scores, recovery rates, and
    exact g-values).
*   **`test_example_*_watermark.py`**: Tests end-to-end watermarked generation
    across examples 2–8.
*   **`test_g_values.py`**: Tests g-value detection accuracy for both
    watermarked and non-watermarked sequences.
*   **`test_compute_g_values.py`**: Tests the standalone FASTA g-value
    calculator.

#### Running Tests

To run the tests, navigate to the `synthidbio_sequence/third_party/ProteinMPNN` directory and use `pytest`:

```bash
cd synthidbio_sequence/third_party/ProteinMPNN

# Run core tests
pytest test_example_1.py test_g_values.py -v

# Run the standalone calculator test
pytest test_compute_g_values.py -v

# Run all tests
pytest -v
```

#### Expected Test Output

```
==================== test session starts ====================
test_example_1.py::test_example_1_non_watermarked PASSED   [ 25%]
test_example_1.py::test_example_1_watermarked PASSED       [ 50%]
test_g_values.py::test_g_values_non_watermarked PASSED     [ 75%]
test_g_values.py::test_g_values_watermarked PASSED         [100%]

==================== 4 passed in 45.23s =====================
```

### Architecture

#### Key Components

1. **ProteinMPNN** (`synthidbio_sequence/third_party/ProteinMPNN/protein_mpnn_run.py`, `synthidbio_sequence/third_party/ProteinMPNN/protein_mpnn_utils.py`)
   - Protein sequence generation model
   - Modified to support watermarking during decoding
   - Forces left-to-right decoding when watermarking enabled

2. **SynthID Text** (`synthidbio_sequence/third_party/synthid-text/`)
   - Watermarking logic processor
   - G-value computation for detection
   - Tournament-based token selection

3.  **Detector** (integrated in `protein_mpnn_run.py` and `compute_g_values.py`)
    - Always-on g-value computation
    - Uses same SynthID processor for detection
    - Independent of watermarking mode

### Contained Code

- **ProteinMPNN** (`synthidbio_sequence/third_party/ProteinMPNN/`): [MIT License](synthidbio_sequence/third_party/ProteinMPNN/LICENSE)
  - Copyright (c) 2022 Justas Dauparas
  - Original publication: Dauparas et al., "Robust deep learning-based protein sequence design using ProteinMPNN" (2022)

- **SynthID-text** (`synthidbio_sequence/third_party/synthid-text/`): [Apache License 2.0](synthidbio_sequence/third_party/synthid-text/LICENSE)
  - Copyright Google DeepMind
  - Watermarking technology for text and sequences

### Modified, Added, and Removed Files in third_party/ProteinMPNN

To integrate SynthID watermarking and ensure determinism, the following files in
the `synthidbio_sequence/third_party/ProteinMPNN` directory were modified,
added, or removed:

#### Modified Files

*   **`synthidbio_sequence/third_party/ProteinMPNN/protein_mpnn_run.py`**:
    *   Added command-line arguments to configure SynthID watermarking (e.g.,
        `--watermark`, `--ngram_len`, `--watermark_keys`, `--num_leaves`).
    *   Imports `SynthIDLogitsProcessor` and `mean_score` from `synthid_text`.
    *   Initializes the `SynthIDLogitsProcessor` and passes it to the model's
        `sample` function.
    *   Enforces `batch_size=1` when watermarking is active.
    *   Computes g-values for all generated sequences and appends the
        `mean_g_value` to the output FASTA headers.
*   **`synthidbio_sequence/third_party/ProteinMPNN/protein_mpnn_utils.py`**:
    *   Modified the `sample` method of `ProteinMPNN` class to accept
        `watermark_processor`.
    *   Forces left-to-right sequential decoding when `watermark_processor` is
        present, overriding the default random decoding order.
    *   Enforces `batch_size=1` check inside `sample` when `watermark_processor`
        is present.
    *   Intercepts logits at each step of the decoding loop and applies
        `watermark_processor.watermarked_call` to compute watermarked scores
        before sampling.
    *   Modified `tied_sample` signature to accept `watermark_processor` for
        compatibility.
*   **`synthidbio_sequence/third_party/ProteinMPNN/helper_scripts/parse_multiple_chains.py`**:
    *   Sorted the output of `glob.glob` to ensure deterministic parsing order
        of PDB files for testing.

#### Added Files

*   **`synthidbio_sequence/third_party/ProteinMPNN/compute_g_values.py`**:
    *   Standalone script to compute g-values for existing sequences in FASTA
        format, using `SynthIDLogitsProcessor` for detection.
*   **`synthidbio_sequence/third_party/ProteinMPNN/test_*.py`**:
    *   Pytest suite (10 files) for validating various ProteinMPNN examples with
        and without watermarking, ensuring exact score and g-value matches.
*   **`synthidbio_sequence/third_party/ProteinMPNN/test_data/`**:
    *   Directory containing golden outputs and helper inputs used by the test
        suite to ensure determinism.
*   **`synthidbio_sequence/third_party/ProteinMPNN/examples/*_watermark.sh`**:
    *   Example bash scripts (for examples 2, 3, 4, 5, 6, 8) demonstrating how
        to run ProteinMPNN with watermarking parameters.

#### Removed Files & Directories

*   **`synthidbio_sequence/third_party/ProteinMPNN/training/`**:
    *   Removed training code, data, and local training weights, as they are not
        required for inference or validation.

### Publication Data

Derived g-values and *in vitro* validation data supporting the publication are
available in the `synthidbio_sequence/data/` directory. This includes binding
data CSVs and kinetics plots for each target:

-   `synthidbio_sequence/data/all_g_values.csv` - G-values for all sequences
-   `synthidbio_sequence/data/SC2RBD/` - Binding data (`sc2rbd_data.csv`) and
    kinetics plots (`sc2rbd_kinetics/`) for SARS-CoV-2 RBD
-   `synthidbio_sequence/data/VEGF-A/` - Binding data (`vegfa_data.csv`) and
    kinetics plots (`vegfa_kinetics/`) for VEGF-A
-   `synthidbio_sequence/data/PD_L1/` - Binding data (`pdl1_data.csv`) and
    kinetics plots (`pdl1_kinetics/`) for PD-L1



## Citing this work

If you use SynthID Bio in your research, please cite:

```bibtex
@article{synthidbio2026,
  title={Function-preserving watermarking of AI-generated proteins},
  author={David Stutz and Alexander I. Cowen-Rivers and Guillermo Ortiz-Jimenez and Jeremy Ratcliff and Vinicius Zambaldi and Lindsay Willmore and Josh Abramson and Harshnira Patani and Christina Kouridi and Florian Stimberg and Mel Vecerik and Alex Chu and Sukhdeep Singh and Sumanth Dathathri and Eliseo Papa and Valentin De Bortoli and Arnaud Doucet and Demis Hassabis and Jue Wang and Sven Gowal and Pushmeet Kohli},
  journal={Nature},
  volume={?},
  number={?},
  pages={?},
  year={2026},
  publisher={Nature Publishing Group UK London}
}
```

## Contact

For questions surrounding SynthID Bio, please contact
[synthidbio@google.com](mailto:synthidbio@google.com).


## Licensing & Disclaimer

Copyright 2026 Google LLC
All software is licensed under the Apache License, Version 2.0 (Apache 2.0); you may not use this file except in compliance with the Apache 2.0 license. You may obtain a copy of the Apache 2.0 license at: https://www.apache.org/licenses/LICENSE-2.0

The AlphaFold 3 model parameters are made available under the AlphaFold 3 Model Parameters Terms of Use (the "Terms"); you may not use these except in compliance with the Terms. You may obtain a copy of the Terms at https://github.com/google-deepmind/alphafold3/blob/main/WEIGHTS_TERMS_OF_USE.md and in the file WEIGHTS_TERM_USE.

Data in the synthidbio_squence/data directory is licensed under the Creative Commons Attribution 4.0 International License (CC-BY). You may obtain a copy of the CC-BY license at: https://creativecommons.org/licenses/by/4.0/legalcode

Unless required by applicable law or agreed to in writing, all software and materials distributed here under the Apache 2.0, the Terms or CC-BY licenses are distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the licenses for the specific language governing permissions and limitations under those licenses.

You are solely responsible for determining the appropriateness of using the software, model parameters, materials or using or distributing outputs, and assume any and all risks associated with such use or distribution and your exercise of rights and obligations under these Terms. You and anyone you share output with are solely responsible for these and their subsequent uses.

Output are predictions with varying levels of confidence and should be interpreted carefully. Use discretion before relying on, publishing, downloading or otherwise using AlphaFold 3.

All software, model parameters, materials and any outputs you create are for theoretical modeling only. They are not intended, validated, or approved for clinical use. You should not use the software, model parameters, materials or outputs for clinical purposes or rely on them for medical or other professional advice. Any content regarding those topics is provided for informational purposes only and is not a substitute for advice from a qualified professional.
This is not an official Google product.

