# rq1_word_state_probes_indicbert_f5_standardised

_Structural distance probe and reference-variant similarity per layer._

| provenance | |
|---|---|
| run (UTC) | 2026-09-17 16:34 |
| script | `rq1_word_state_probes.py` (sha256 `2789b7829b1e6a4c`) |
| host | gnode (Linux) |
| duration | 50.1 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce RTX 2080 Ti |
| args | `{"epochs": 40, "model": "<earlier-repo>/local_models/IndicBERTv2-MLM-only", "n_refs": 2000, "only_f5": true, "pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "record_tag": "rq1_word_state_probes_indicbert_f5_standardised", "standardise": true, "tag": "indicbert"}` |
| command | `scripts/rq1_word_state_probes.py --model <earlier-repo>/local_models/IndicBERTv2-MLM-only --tag indicbert --standardise --epochs 40 --only-f5 --record-tag rq1_word_state_probes_indicbert_f5_standardised` |


- **pairs with word states**: 2,000
- **training / held-out references (by document)**: 1,623 / 377

## F5: structural distance probe (held-out references)

- **standardised inputs / epochs**: True / 40

| layer | mean Spearman (5-50 words) | UUAS | training loss, first epoch | last epoch |
|---|---|---|---|---|
| baseline: surface distance |i - j| | 0.404 | 0.549 | nan | nan |
| control (pre-LayerNorm input) | 0.073 | 0.145 | 1.835 | 1.882 |
| 0 | 0.111 | 0.149 | 1.688 | 1.677 |
| 1 | 0.148 | 0.200 | 1.564 | 1.525 |
| 2 | 0.221 | 0.234 | 1.478 | 1.435 |
| 3 | 0.227 | 0.249 | 1.451 | 1.448 |
| 4 | 0.210 | 0.252 | 1.504 | 1.483 |
| 5 | 0.166 | 0.223 | 1.813 | 1.887 |
| 6 | 0.200 | 0.278 | 1.482 | 1.550 |
| 7 | 0.252 | 0.313 | 1.436 | 1.486 |
| 8 | 0.311 | 0.347 | 1.426 | 1.392 |
| 9 | 0.191 | 0.275 | 1.522 | 1.534 |
| 10 | 0.147 | 0.229 | 1.662 | 1.654 |
| 11 | -0.008 | 0.158 | 3.374 | 3.754 |
| 12 | 0.222 | 0.230 | 1.810 | 1.716 |


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `rq1_word_state_probes_rq1_word_state_probes_indicbert_f5_standardised.csv` | 811 | `94f15b85e9b04b7b` | distance: a = Spearman, b = UUAS |
