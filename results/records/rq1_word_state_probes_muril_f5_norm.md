# rq1_word_state_probes_muril_f5_norm

_Structural distance probe and reference-variant similarity per layer._

| provenance | |
|---|---|
| run (UTC) | 2026-09-17 18:56 |
| script | `rq1_word_state_probes.py` (sha256 `4d6551cd0967e024`) |
| host | gnode (Linux) |
| duration | 47.6 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce RTX 2080 Ti |
| args | `{"epochs": 40, "model": "<earlier-repo>/local_models/muril-base-cased", "n_refs": 2000, "only_f5": true, "pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "record_tag": "rq1_word_state_probes_muril_f5_norm", "standardise": "norm", "tag": "muril"}` |
| command | `scripts/rq1_word_state_probes.py --model <earlier-repo>/local_models/muril-base-cased --tag muril --standardise norm --epochs 40 --only-f5 --record-tag rq1_word_state_probes_muril_f5_norm` |


- **pairs with word states**: 2,000
- **training / held-out references (by document)**: 1,623 / 377

## F5: structural distance probe (held-out references)

- **input scaling / epochs**: norm / 40
- **layer 6: dimensions with std < 1e-3 / smallest / largest std**: 0 / 5.48e-02 / 1.03e+00

| layer | mean Spearman (5-50 words) | UUAS | training loss, first epoch | last epoch |
|---|---|---|---|---|
| baseline: surface distance |i - j| | 0.404 | 0.549 | nan | nan |
| control (pre-LayerNorm input) | 0.566 | 0.496 | 1.171 | 0.840 |
| 0 | 0.570 | 0.490 | 1.217 | 0.837 |
| 1 | 0.583 | 0.501 | 1.183 | 0.816 |
| 2 | 0.724 | 0.642 | 1.116 | 0.658 |
| 3 | 0.788 | 0.718 | 1.061 | 0.554 |
| 4 | 0.815 | 0.756 | 1.034 | 0.505 |
| 5 | 0.824 | 0.764 | 1.029 | 0.469 |
| 6 | 0.822 | 0.762 | 1.034 | 0.470 |
| 7 | 0.833 | 0.782 | 1.016 | 0.458 |
| 8 | 0.832 | 0.786 | 1.034 | 0.463 |
| 9 | 0.813 | 0.763 | 1.059 | 0.495 |
| 10 | 0.796 | 0.750 | 1.097 | 0.523 |
| 11 | 0.779 | 0.725 | 1.135 | 0.551 |
| 12 | 0.763 | 0.689 | 1.254 | 0.573 |


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `rq1_word_state_probes_rq1_word_state_probes_muril_f5_norm.csv` | 742 | `68f549acb9ebf3ca` | distance: a = Spearman, b = UUAS |
