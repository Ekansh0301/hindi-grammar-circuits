# rq1_word_state_probes_xlmrlarge_f5_standardised

_Structural distance probe and reference-variant similarity per layer._

| provenance | |
|---|---|
| run (UTC) | 2026-09-17 18:08 |
| script | `rq1_word_state_probes.py` (sha256 `4d6551cd0967e024`) |
| host | gnode (Linux) |
| duration | 93.2 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce RTX 2080 Ti |
| args | `{"epochs": 40, "model": "xlm-roberta-large", "n_refs": 2000, "only_f5": true, "pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "record_tag": "rq1_word_state_probes_xlmrlarge_f5_standardised", "standardise": true, "tag": "xlmrlarge"}` |
| command | `scripts/rq1_word_state_probes.py --model xlm-roberta-large --tag xlmrlarge --standardise --epochs 40 --only-f5 --record-tag rq1_word_state_probes_xlmrlarge_f5_standardised` |


- **pairs with word states**: 2,000
- **training / held-out references (by document)**: 1,623 / 377

## F5: structural distance probe (held-out references)

- **standardised inputs / epochs**: True / 40

| layer | mean Spearman (5-50 words) | UUAS | training loss, first epoch | last epoch |
|---|---|---|---|---|
| baseline: surface distance |i - j| | 0.404 | 0.549 | nan | nan |
| control (pre-LayerNorm input) | 0.014 | 0.123 | 2.295 | 2.287 |
| 0 | 0.095 | 0.132 | 2.100 | 2.120 |
| 1 | 0.076 | 0.125 | 2.185 | 2.146 |
| 2 | 0.100 | 0.143 | 2.034 | 2.035 |
| 3 | 0.113 | 0.144 | 1.956 | 1.961 |
| 4 | 0.171 | 0.148 | 1.933 | 1.869 |
| 5 | 0.141 | 0.161 | 1.856 | 1.853 |
| 6 | 0.140 | 0.144 | 1.874 | 1.873 |
| 7 | 0.150 | 0.143 | 1.885 | 1.866 |
| 8 | 0.182 | 0.177 | 1.849 | 1.859 |
| 9 | 0.154 | 0.173 | 1.798 | 1.761 |
| 10 | 0.147 | 0.174 | 1.853 | 1.816 |
| 11 | 0.168 | 0.206 | 1.875 | 1.858 |
| 12 | 0.176 | 0.229 | 1.865 | 1.826 |
| 13 | 0.187 | 0.219 | 1.886 | 1.871 |
| 14 | 0.167 | 0.232 | 2.114 | 2.149 |
| 15 | 0.106 | 0.225 | 1.986 | 2.054 |
| 16 | 0.109 | 0.242 | 2.026 | 2.027 |
| 17 | 0.104 | 0.246 | 2.019 | 2.091 |
| 18 | 0.120 | 0.261 | 2.003 | 2.061 |
| 19 | 0.090 | 0.207 | 2.055 | 2.106 |
| 20 | 0.096 | 0.203 | 2.027 | 2.049 |
| 21 | 0.123 | 0.195 | 1.970 | 1.972 |
| 22 | 0.202 | 0.204 | 2.357 | 2.993 |
| 23 | 0.174 | 0.180 | 2.290 | 2.582 |
| 24 | 0.146 | 0.157 | 2.224 | 2.160 |


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `rq1_word_state_probes_rq1_word_state_probes_xlmrlarge_f5_standardised.csv` | 1,553 | `e6bd309989c3ca1b` | distance: a = Spearman, b = UUAS |
