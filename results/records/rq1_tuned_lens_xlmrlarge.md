# rq1_tuned_lens_xlmrlarge

_Tuned-lens translators and their readability._

| provenance | |
|---|---|
| run (UTC) | 2026-09-17 16:52 |
| script | `rq1_tuned_lens.py` (sha256 `cf6bd803a9a9b1fa`) |
| host | gnode (Linux) |
| duration | 78.9 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"batch_size": 16, "epochs": 2, "model": "xlm-roberta-large", "n_train": 3000, "out_dir": "<earlier-repo>/sets/set1/Results_Checks/lm_units", "sentences": "<earlier-repo>/Results_Checks/indiccorp_sample/readability_sentences.txt", "tag": "xlmrlarge"}` |
| command | `scripts/rq1_tuned_lens.py --model xlm-roberta-large --tag xlmrlarge --batch-size 16` |


- **training sentences / held-out sentences**: 3,000 / 500

| epoch | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 5.413 | 5.282 | 3.710 | 3.489 | 3.347 | 3.201 | 3.122 | 3.038 | 2.960 | 2.765 | 2.650 | 2.466 | 2.281 | 2.176 | 2.084 | 2.010 | 1.953 | 1.831 | 1.727 | 1.465 | 0.922 | 0.516 | 0.290 | 0.155 |
| 1 | 5.233 | 5.092 | 3.201 | 2.964 | 2.792 | 2.654 | 2.550 | 2.461 | 2.379 | 2.163 | 2.055 | 1.840 | 1.632 | 1.533 | 1.443 | 1.383 | 1.354 | 1.277 | 1.217 | 1.023 | 0.605 | 0.342 | 0.209 | 0.138 |


| layer | logit lens nats/subtoken | tuned lens nats/subtoken | tuned minus final | readable (tuned) |
|---|---|---|---|---|
| 0 | 22.336 | 7.100 | 4.861 | no |
| 1 | 25.645 | 6.889 | 4.649 | no |
| 2 | 26.550 | 5.063 | 2.824 | no |
| 3 | 27.943 | 4.855 | 2.615 | no |
| 4 | 26.074 | 4.714 | 2.475 | no |
| 5 | 24.705 | 4.604 | 2.365 | no |
| 6 | 22.523 | 4.525 | 2.286 | no |
| 7 | 21.068 | 4.472 | 2.233 | no |
| 8 | 19.772 | 4.406 | 2.166 | no |
| 9 | 18.148 | 4.215 | 1.976 | yes |
| 10 | 16.192 | 4.127 | 1.888 | yes |
| 11 | 13.286 | 3.957 | 1.718 | yes |
| 12 | 12.196 | 3.790 | 1.550 | yes |
| 13 | 11.436 | 3.711 | 1.471 | yes |
| 14 | 11.281 | 3.653 | 1.413 | yes |
| 15 | 10.523 | 3.606 | 1.367 | yes |
| 16 | 9.377 | 3.562 | 1.323 | yes |
| 17 | 8.687 | 3.485 | 1.246 | yes |
| 18 | 6.550 | 3.446 | 1.207 | yes |
| 19 | 5.511 | 3.309 | 1.070 | yes |
| 20 | 4.801 | 2.888 | 0.649 | yes |
| 21 | 3.817 | 2.608 | 0.369 | yes |
| 22 | 3.706 | 2.414 | 0.175 | yes |
| 23 | 3.306 | 2.345 | 0.106 | yes |
| 24 | 2.239 | 2.239 | 0.000 | yes |


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `tuned_lens_xlmrlarge.pt` | 100,778,346 | `3f1ef78b604fba68` | translator weights |
