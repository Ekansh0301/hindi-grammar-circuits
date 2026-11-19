# rq1_word_state_probes_xlmrlarge_f5_norm

_Structural distance probe and reference-variant similarity per layer._

| provenance | |
|---|---|
| run (UTC) | 2026-09-17 21:44 |
| script | `rq1_word_state_probes.py` (sha256 `4d6551cd0967e024`) |
| host | gnode (Linux) |
| duration | 47.0 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ? |
| args | `{"epochs": 40, "model": "xlm-roberta-large", "n_refs": 2000, "only_f5": true, "pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "record_tag": "rq1_word_state_probes_xlmrlarge_f5_norm", "standardise": "norm", "tag": "xlmrlarge"}` |
| command | `scripts/rq1_word_state_probes.py --model xlm-roberta-large --tag xlmrlarge --standardise norm --epochs 40 --only-f5 --record-tag rq1_word_state_probes_xlmrlarge_f5_norm` |


- **pairs with word states**: 2,000
- **training / held-out references (by document)**: 1,623 / 377

## F5: structural distance probe (held-out references)

- **input scaling / epochs**: norm / 40
- **layer 12: dimensions with std < 1e-3 / smallest / largest std**: 0 / 2.78e-01 / 3.93e+00

| layer | mean Spearman (5-50 words) | UUAS | training loss, first epoch | last epoch |
|---|---|---|---|---|
| baseline: surface distance |i - j| | 0.404 | 0.549 | nan | nan |
| control (pre-LayerNorm input) | 0.549 | 0.470 | 1.257 | 0.834 |
| 0 | 0.553 | 0.463 | 1.279 | 0.836 |
| 1 | 0.551 | 0.466 | 1.278 | 0.838 |
| 2 | 0.624 | 0.540 | 1.206 | 0.751 |
| 3 | 0.659 | 0.582 | 1.198 | 0.711 |
| 4 | 0.666 | 0.582 | 1.200 | 0.693 |
| 5 | 0.682 | 0.603 | 1.187 | 0.678 |
| 6 | 0.688 | 0.618 | 1.180 | 0.672 |
| 7 | 0.720 | 0.639 | 1.168 | 0.621 |
| 8 | 0.769 | 0.696 | 1.115 | 0.561 |
| 9 | 0.788 | 0.732 | 1.079 | 0.524 |
| 10 | 0.815 | 0.760 | 1.036 | 0.489 |
| 11 | 0.807 | 0.751 | 1.047 | 0.500 |
| 12 | 0.736 | 0.656 | 1.190 | 0.576 |
| 13 | 0.670 | 0.599 | 1.264 | 0.637 |
| 14 | 0.664 | 0.586 | 1.296 | 0.638 |
| 15 | 0.650 | 0.574 | 1.299 | 0.648 |
| 16 | 0.644 | 0.563 | 1.290 | 0.653 |
| 17 | 0.636 | 0.563 | 1.276 | 0.659 |
| 18 | 0.627 | 0.559 | 1.278 | 0.676 |
| 19 | 0.627 | 0.559 | 1.293 | 0.685 |
| 20 | 0.634 | 0.557 | 1.297 | 0.689 |
| 21 | 0.639 | 0.555 | 1.319 | 0.706 |
| 22 | 0.644 | 0.541 | 1.356 | 0.713 |
| 23 | 0.640 | 0.530 | 1.386 | 0.725 |
| 24 | 0.643 | 0.536 | 1.455 | 0.736 |


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `rq1_word_state_probes_rq1_word_state_probes_xlmrlarge_f5_norm.csv` | 1,510 | `20bb06c86c31611e` | distance: a = Spearman, b = UUAS |
