# rq1_word_state_probes_mbert_f5_norm

_Structural distance probe and reference-variant similarity per layer._

| provenance | |
|---|---|
| run (UTC) | 2026-09-17 21:42 |
| script | `rq1_word_state_probes.py` (sha256 `4d6551cd0967e024`) |
| host | gnode (Linux) |
| duration | 48.0 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce RTX 2080 Ti |
| args | `{"epochs": 40, "model": "bert-base-multilingual-cased", "n_refs": 2000, "only_f5": true, "pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "record_tag": "rq1_word_state_probes_mbert_f5_norm", "standardise": "norm", "tag": "mbert"}` |
| command | `scripts/rq1_word_state_probes.py --model bert-base-multilingual-cased --tag mbert --standardise norm --epochs 40 --only-f5 --record-tag rq1_word_state_probes_mbert_f5_norm` |


- **pairs with word states**: 2,000
- **training / held-out references (by document)**: 1,623 / 377

## F5: structural distance probe (held-out references)

- **input scaling / epochs**: norm / 40
- **layer 6: dimensions with std < 1e-3 / smallest / largest std**: 0 / 3.95e-01 / 1.14e+00

| layer | mean Spearman (5-50 words) | UUAS | training loss, first epoch | last epoch |
|---|---|---|---|---|
| baseline: surface distance |i - j| | 0.404 | 0.549 | nan | nan |
| control (pre-LayerNorm input) | 0.548 | 0.472 | 1.289 | 0.889 |
| 0 | 0.553 | 0.478 | 1.304 | 0.888 |
| 1 | 0.578 | 0.493 | 1.268 | 0.842 |
| 2 | 0.623 | 0.558 | 1.210 | 0.793 |
| 3 | 0.703 | 0.626 | 1.128 | 0.689 |
| 4 | 0.735 | 0.662 | 1.063 | 0.647 |
| 5 | 0.754 | 0.676 | 1.040 | 0.616 |
| 6 | 0.787 | 0.727 | 1.013 | 0.549 |
| 7 | 0.803 | 0.732 | 1.028 | 0.504 |
| 8 | 0.796 | 0.714 | 1.023 | 0.498 |
| 9 | 0.786 | 0.701 | 1.045 | 0.514 |
| 10 | 0.772 | 0.681 | 1.093 | 0.538 |
| 11 | 0.757 | 0.660 | 1.160 | 0.551 |
| 12 | 0.711 | 0.596 | 1.329 | 0.617 |


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `rq1_word_state_probes_rq1_word_state_probes_mbert_f5_norm.csv` | 737 | `c4e8c7d4bbe4ff2f` | distance: a = Spearman, b = UUAS |
