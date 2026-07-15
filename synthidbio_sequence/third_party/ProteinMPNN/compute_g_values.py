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

import argparse

import jax.numpy as jnp
import numpy as np
import torch
from synthid_text.detector_mean import mean_score
from synthid_text.logits_processing import SynthIDLogitsProcessor


def parse_fasta(fasta_path):
    sequences = []
    headers = []
    with open(fasta_path, "r") as f:
        current_seq = []
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if current_seq:
                    sequences.append("".join(current_seq))
                    current_seq = []
                headers.append(line)
            else:
                current_seq.append(line)
        if current_seq:
            sequences.append("".join(current_seq))
    return headers, sequences


def main(args):
  device = torch.device("cuda:0" if (torch.cuda.is_available()) else "cpu")

  keys = [int(k) for k in args.watermark_keys.split(",")]

  # Initialize SynthID processor/detector
  # Note: These parameters must match what was used during generation
  # if you want to detect that specific watermark.
  detector_processor = SynthIDLogitsProcessor(
        ngram_len=args.ngram_len,
        keys=keys,
        context_history_size=args.context_history_size,
        temperature=args.watermark_temperature,
        top_k=args.watermark_top_k,
        device=device,
        skip_first_ngram_calls=args.skip_first_ngram_calls,
        apply_top_k=False,
        num_leaves=args.num_leaves,
    )

  headers, sequences = parse_fasta(args.input_fasta)
  alphabet = "ACDEFGHIKLMNPQRSTVWYX"
  alphabet_dict = dict(zip(alphabet, range(21)))

  with open(args.output_fasta, "w") as f:
    for header, seq in zip(headers, sequences):
      # Convert sequence to token IDs
      # Only include characters that are in the alphabet (skips '/' etc.)
      seq_ids = torch.tensor(
                [
                    alphabet_dict.get(aa, 20)
                    for aa in seq
                    if aa in alphabet_dict
                ],
                device=device,
            ).unsqueeze(0)

      # Compute g-values
      g_values_torch = detector_processor.compute_g_values(seq_ids)

      # Compute mean g-value score using JAX
      mask_g = jnp.ones((1, g_values_torch.shape[1]))
      mean_g_value = float(
                mean_score(jnp.array(g_values_torch.cpu().numpy()), mask_g)[0]
            )

      # Format mean g-value string
      mean_g_print = np.format_float_positional(
                np.float32(mean_g_value), unique=False, precision=4
            )

      # Append g-value to header (comma separated as shown in README)
      # README example: >test_seq_1, mean_g_value=0.7286
      # The test expects "mean_g_value=" in the header.
      # We assume the original header starts with '>' and we append after it.
      # If the header already has commas, we just append to the end.

      clean_header = header.strip()
      new_header = f"{clean_header}, mean_g_value={mean_g_print}"

      f.write(f"{new_header}\n{seq}\n")


if __name__ == "__main__":
  parser = argparse.ArgumentParser(
      description="Standalone G-Value Calculator for Protein Sequences"
  )
  parser.add_argument(
      "--input_fasta",
      type=str,
      required=True,
      help="Path to input FASTA file containing sequences to evaluate.",
  )
  parser.add_argument(
      "--output_fasta",
      type=str,
      required=True,
      help=(
          "Path to output FASTA file where sequences will be written with "
          "computed mean g-values appended to their headers."
      ),
  )

  # Watermarking parameters
  parser.add_argument(
      "--watermark_keys",
      type=str,
      default=(
          "0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24"
      ),
      help=(
          "Comma-separated integer keys used for watermarking layers. The "
          "number of keys must match the ngram_len (or depth). These keys "
          "initialize the pseudo-random function. Must match the keys used "
          "during generation for detection. Default is 0,1,...,24."
      ),
  )
  parser.add_argument(
      "--ngram_len",
      type=int,
      default=4,
      help=(
          "N-gram length (L) for watermarking context. Defines the history "
          "window size used to condition the watermark generation. Must match "
          "the value used during sequence generation for accurate detection. "
          "Default is 4."
      ),
  )
  parser.add_argument(
      "--num_leaves",
      type=int,
      default=2,
      help=(
          "Tournament size (number of leaves) for distortionary tournament "
          "watermarking. Controls the branching factor of candidate selection. "
          "Set to 2 for standard binary tournament, or higher (e.g., 25) for "
          "stronger watermark signal in low-temperature generation. Default is 2."
      ),
  )
  parser.add_argument(
      "--context_history_size",
      type=int,
      default=1024,
      help=(
          "Size of the circular buffer used to track previously generated "
          "n-gram contexts. Used to prevent watermarking repeated patterns, "
          "which can degrade sequence quality. Default is 1024."
      ),
  )
  parser.add_argument(
      "--watermark_temperature",
      type=float,
      default=1.0,
      help=(
          "Temperature scaling factor applied during watermarking logits "
          "processing. Controls the strength of the watermark distortion. "
          "Higher values can increase detection signal but might affect "
          "sequence viability. Default is 1.0."
      ),
  )
  parser.add_argument(
      "--watermark_top_k",
      type=int,
      default=21,
      help=(
          "Number of top candidates (K) to consider for watermarking. For "
          "protein design, this should be set to the vocabulary size (21 for "
          "standard amino acids + mask token) to maintain the full alphabet. "
          "Default is 21."
      ),
  )
  parser.add_argument(
      "--skip_first_ngram_calls",
      action="store_true",
      default=True,
      help=(
          "If set, disables watermarking for the first (ngram_len - 1) tokens "
          "of each sequence, as they do not have sufficient context history. "
          "Default is True (enabled)."
      ),
  )

  args = parser.parse_args()
  main(args)
