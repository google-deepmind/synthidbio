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

import pytest

from compute_g_values import parse_fasta


@pytest.mark.parametrize("contents", [
    ">empty\n>actual\nACDEFG\n",
    ">actual\nACDEFG\n>empty\n",
    ">first\nACDEFG\n>empty\n>last\nKLMNPQ\n",
])
def test_empty_record_is_rejected(tmp_path, contents):
    fasta_path = tmp_path / "input.fa"
    fasta_path.write_text(contents)
    with pytest.raises(ValueError, match="FASTA record .* has no sequence"):
        parse_fasta(fasta_path)


def test_sequence_before_header_is_rejected(tmp_path):
    fasta_path = tmp_path / "input.fa"
    fasta_path.write_text("ACDEFG\n>actual\nKLMNPQ\n")
    with pytest.raises(ValueError, match="before the first FASTA header"):
        parse_fasta(fasta_path)


def test_wrapped_sequences_keep_their_headers(tmp_path):
    fasta_path = tmp_path / "input.fa"
    fasta_path.write_text("\n>first description\nACD\nEFG\n\n>second\nKLM\nNPQ\n")
    assert parse_fasta(fasta_path) == (
        [">first description", ">second"], ["ACDEFG", "KLMNPQ"]
    )
