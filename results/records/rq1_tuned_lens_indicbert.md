# rq1_tuned_lens_indicbert

_Tuned-lens translators and their readability._

| provenance | |
|---|---|
| run (UTC) | 2026-09-17 14:44 |
| script | `rq1_tuned_lens.py` (sha256 `cf6bd803a9a9b1fa`) |
| host | gnode (Linux) |
| duration | 13.4 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce RTX 2080 Ti |
| args | `{"batch_size": 32, "epochs": 2, "model": "<earlier-repo>/local_models/IndicBERTv2-MLM-only", "n_train": 3000, "out_dir": "<earlier-repo>/sets/set1/Results_Checks/lm_units", "sentences": "<earlier-repo>/Results_Checks/indiccorp_sample/readability_sentences.txt", "tag": "indicbert"}` |
| command | `scripts/rq1_tuned_lens.py --model <earlier-repo>/local_models/IndicBERTv2-MLM-only --tag indicbert --batch-size 32` |


- **training sentences / held-out sentences**: 3,000 / 500

| epoch | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 5.587 | 4.143 | 3.295 | 3.058 | 2.649 | 2.382 | 2.115 | 1.901 | 1.514 | 1.159 | 0.522 | 0.154 |
| 1 | 5.433 | 3.595 | 2.755 | 2.537 | 2.111 | 1.862 | 1.610 | 1.419 | 1.110 | 0.822 | 0.333 | 0.096 |


| layer | logit lens nats/subtoken | tuned lens nats/subtoken | tuned minus final | readable (tuned) |
|---|---|---|---|---|
| 0 | 14.672 | 7.647 | 5.333 | no |
| 1 | 11.381 | 5.781 | 3.468 | no |
| 2 | 8.052 | 5.047 | 2.733 | no |
| 3 | 7.930 | 4.832 | 2.518 | no |
| 4 | 8.622 | 4.479 | 2.166 | no |
| 5 | 7.643 | 4.276 | 1.963 | yes |
| 6 | 6.825 | 4.079 | 1.765 | yes |
| 7 | 6.867 | 3.899 | 1.586 | yes |
| 8 | 6.108 | 3.601 | 1.287 | yes |
| 9 | 6.115 | 3.287 | 0.974 | yes |
| 10 | 4.311 | 2.780 | 0.467 | yes |
| 11 | 3.336 | 2.459 | 0.145 | yes |
| 12 | 2.314 | 2.314 | 0.000 | yes |


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `tuned_lens_indicbert.pt` | 28,356,858 | `06ee7d0d0dd8ae74` | translator weights |
