# rq1_word_state_probes_indicbert_f5_norm

_Structural distance probe and reference-variant similarity per layer._

| provenance | |
|---|---|
| run (UTC) | 2026-09-17 21:46 |
| script | `rq1_word_state_probes.py` (sha256 `4d6551cd0967e024`) |
| host | gnode (Linux) |
| duration | 51.7 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce RTX 2080 Ti |
| args | `{"epochs": 40, "model": "<earlier-repo>/local_models/IndicBERTv2-MLM-only", "n_refs": 2000, "only_f5": true, "pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "record_tag": "rq1_word_state_probes_indicbert_f5_norm", "standardise": "norm", "tag": "indicbert"}` |
| command | `scripts/rq1_word_state_probes.py --model <earlier-repo>/local_models/IndicBERTv2-MLM-only --tag indicbert --standardise norm --epochs 40 --only-f5 --record-tag rq1_word_state_probes_indicbert_f5_norm` |


- **pairs with word states**: 2,000
- **training / held-out references (by document)**: 1,623 / 377

## F5: structural distance probe (held-out references)

- **input scaling / epochs**: norm / 40
- **layer 6: dimensions with std < 1e-3 / smallest / largest std**: 0 / 9.78e-02 / 1.09e+00

| layer | mean Spearman (5-50 words) | UUAS | training loss, first epoch | last epoch |
|---|---|---|---|---|
| baseline: surface distance |i - j| | 0.404 | 0.549 | nan | nan |
| control (pre-LayerNorm input) | 0.592 | 0.511 | 1.191 | 0.811 |
| 0 | 0.591 | 0.509 | 1.205 | 0.813 |
| 1 | 0.672 | 0.596 | 1.115 | 0.718 |
| 2 | 0.736 | 0.669 | 1.086 | 0.617 |
| 3 | 0.764 | 0.708 | 1.057 | 0.582 |
| 4 | 0.812 | 0.760 | 1.028 | 0.516 |
| 5 | 0.824 | 0.771 | 1.017 | 0.493 |
| 6 | 0.827 | 0.775 | 1.032 | 0.481 |
| 7 | 0.812 | 0.752 | 1.073 | 0.491 |
| 8 | 0.786 | 0.722 | 1.106 | 0.517 |
| 9 | 0.758 | 0.691 | 1.160 | 0.555 |
| 10 | 0.734 | 0.658 | 1.195 | 0.602 |
| 11 | 0.402 | 0.416 | 1.467 | 1.000 |
| 12 | 0.650 | 0.564 | 1.510 | 0.747 |


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `rq1_word_state_probes_rq1_word_state_probes_indicbert_f5_norm.csv` | 794 | `65dd158e88b1e227` | distance: a = Spearman, b = UUAS |
