# rq1_word_state_probes_muril_f5_raw40

_Structural distance probe and reference-variant similarity per layer._

| provenance | |
|---|---|
| run (UTC) | 2026-09-17 19:42 |
| script | `rq1_word_state_probes.py` (sha256 `4d6551cd0967e024`) |
| host | gnode (Linux) |
| duration | 46.1 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce RTX 2080 Ti |
| args | `{"epochs": 40, "model": "<earlier-repo>/local_models/muril-base-cased", "n_refs": 2000, "only_f5": true, "pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "record_tag": "rq1_word_state_probes_muril_f5_raw40", "standardise": "none", "tag": "muril"}` |
| command | `scripts/rq1_word_state_probes.py --model <earlier-repo>/local_models/muril-base-cased --tag muril --standardise none --epochs 40 --only-f5 --record-tag rq1_word_state_probes_muril_f5_raw40` |


- **pairs with word states**: 2,000
- **training / held-out references (by document)**: 1,623 / 377

## F5: structural distance probe (held-out references)

- **input scaling / epochs**: none / 40
- **layer 6: dimensions with std < 1e-3 / smallest / largest std**: 0 / 5.48e-02 / 1.03e+00

| layer | mean Spearman (5-50 words) | UUAS | training loss, first epoch | last epoch |
|---|---|---|---|---|
| baseline: surface distance |i - j| | 0.404 | 0.549 | nan | nan |
| control (pre-LayerNorm input) | 0.567 | 0.498 | 1.174 | 0.839 |
| 0 | 0.450 | 0.365 | 1.196 | 1.098 |
| 1 | 0.463 | 0.360 | 1.177 | 1.080 |
| 2 | 0.594 | 0.473 | 1.050 | 0.919 |
| 3 | 0.652 | 0.534 | 0.999 | 0.864 |
| 4 | 0.702 | 0.588 | 0.950 | 0.802 |
| 5 | 0.706 | 0.610 | 0.948 | 0.799 |
| 6 | 0.689 | 0.590 | 0.941 | 0.802 |
| 7 | 0.710 | 0.622 | 0.920 | 0.779 |
| 8 | 0.708 | 0.610 | 0.922 | 0.787 |
| 9 | 0.670 | 0.584 | 0.949 | 0.809 |
| 10 | 0.664 | 0.572 | 0.973 | 0.816 |
| 11 | 0.662 | 0.568 | 0.996 | 0.826 |
| 12 | 0.756 | 0.711 | 2.021 | 0.670 |


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `rq1_word_state_probes_rq1_word_state_probes_muril_f5_raw40.csv` | 741 | `952a42b509fb2080` | distance: a = Spearman, b = UUAS |
