# rq1_word_state_probes_mbert_f5_standardised

_Structural distance probe and reference-variant similarity per layer._

| provenance | |
|---|---|
| run (UTC) | 2026-09-17 17:03 |
| script | `rq1_word_state_probes.py` (sha256 `2789b7829b1e6a4c`) |
| host | gnode (Linux) |
| duration | 49.7 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"epochs": 40, "model": "bert-base-multilingual-cased", "n_refs": 2000, "only_f5": true, "pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "record_tag": "rq1_word_state_probes_mbert_f5_standardised", "standardise": true, "tag": "mbert"}` |
| command | `scripts/rq1_word_state_probes.py --model bert-base-multilingual-cased --tag mbert --standardise --epochs 40 --only-f5 --record-tag rq1_word_state_probes_mbert_f5_standardised` |


- **pairs with word states**: 2,000
- **training / held-out references (by document)**: 1,623 / 377

## F5: structural distance probe (held-out references)

- **standardised inputs / epochs**: True / 40

| layer | mean Spearman (5-50 words) | UUAS | training loss, first epoch | last epoch |
|---|---|---|---|---|
| baseline: surface distance |i - j| | 0.404 | 0.549 | nan | nan |
| control (pre-LayerNorm input) | 0.149 | 0.161 | 1.993 | 1.944 |
| 0 | 0.168 | 0.178 | 1.845 | 1.812 |
| 1 | 0.150 | 0.173 | 1.782 | 1.762 |
| 2 | 0.214 | 0.200 | 1.712 | 1.685 |
| 3 | 0.263 | 0.228 | 1.631 | 1.567 |
| 4 | 0.312 | 0.264 | 1.588 | 1.555 |
| 5 | 0.283 | 0.237 | 1.582 | 1.560 |
| 6 | 0.309 | 0.270 | 1.494 | 1.448 |
| 7 | 0.365 | 0.352 | 1.408 | 1.390 |
| 8 | 0.301 | 0.308 | 1.394 | 1.406 |
| 9 | 0.319 | 0.336 | 1.398 | 1.415 |
| 10 | 0.367 | 0.350 | 1.410 | 1.408 |
| 11 | 0.311 | 0.310 | 1.404 | 1.410 |
| 12 | 0.273 | 0.295 | 1.498 | 1.492 |


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `rq1_word_state_probes_rq1_word_state_probes_mbert_f5_standardised.csv` | 759 | `b991bae3b4ce2dda` | distance: a = Spearman, b = UUAS |
