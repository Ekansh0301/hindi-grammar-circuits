# rq1_word_state_probes_muril_f5_standardised

_Structural distance probe and reference-variant similarity per layer._

| provenance | |
|---|---|
| run (UTC) | 2026-09-17 16:32 |
| script | `rq1_word_state_probes.py` (sha256 `2789b7829b1e6a4c`) |
| host | gnode (Linux) |
| duration | 47.9 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce RTX 2080 Ti |
| args | `{"epochs": 40, "model": "<earlier-repo>/local_models/muril-base-cased", "n_refs": 2000, "only_f5": true, "pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "record_tag": "rq1_word_state_probes_muril_f5_standardised", "standardise": true, "tag": "muril"}` |
| command | `scripts/rq1_word_state_probes.py --model <earlier-repo>/local_models/muril-base-cased --tag muril --standardise --epochs 40 --only-f5 --record-tag rq1_word_state_probes_muril_f5_standardised` |


- **pairs with word states**: 2,000
- **training / held-out references (by document)**: 1,623 / 377

## F5: structural distance probe (held-out references)

- **standardised inputs / epochs**: True / 40

| layer | mean Spearman (5-50 words) | UUAS | training loss, first epoch | last epoch |
|---|---|---|---|---|
| baseline: surface distance |i - j| | 0.404 | 0.549 | nan | nan |
| control (pre-LayerNorm input) | -0.042 | 0.119 | 3.141 | 2.666 |
| 0 | 0.004 | 0.124 | 1.836 | 1.900 |
| 1 | 0.062 | 0.163 | 1.860 | 1.893 |
| 2 | 0.076 | 0.158 | 1.647 | 1.598 |
| 3 | 0.149 | 0.214 | 1.502 | 1.498 |
| 4 | 0.181 | 0.276 | 1.527 | 1.516 |
| 5 | 0.326 | 0.368 | 1.452 | 1.443 |
| 6 | 0.324 | 0.388 | 1.412 | 1.401 |
| 7 | 0.304 | 0.370 | 1.406 | 1.417 |
| 8 | 0.359 | 0.402 | 1.380 | 1.375 |
| 9 | 0.270 | 0.351 | 1.452 | 1.443 |
| 10 | 0.257 | 0.324 | 1.451 | 1.432 |
| 11 | 0.259 | 0.325 | 1.509 | 1.517 |
| 12 | 0.196 | 0.269 | 1.549 | 1.537 |


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `rq1_word_state_probes_rq1_word_state_probes_muril_f5_standardised.csv` | 765 | `9c8bb7ebd2b5b59b` | distance: a = Spearman, b = UUAS |
