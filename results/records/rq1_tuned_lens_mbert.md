# rq1_tuned_lens_mbert

_Tuned-lens translators and their readability._

| provenance | |
|---|---|
| run (UTC) | 2026-09-17 15:30 |
| script | `rq1_tuned_lens.py` (sha256 `cf6bd803a9a9b1fa`) |
| host | gnode (Linux) |
| duration | 16.4 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce RTX 2080 Ti |
| args | `{"batch_size": 24, "epochs": 2, "model": "bert-base-multilingual-cased", "n_train": 3000, "out_dir": "<earlier-repo>/sets/set1/Results_Checks/lm_units", "sentences": "<earlier-repo>/Results_Checks/indiccorp_sample/readability_sentences.txt", "tag": "mbert"}` |
| command | `scripts/rq1_tuned_lens.py --model bert-base-multilingual-cased --tag mbert --batch-size 24` |


- **training sentences / held-out sentences**: 3,000 / 500

| epoch | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 3.297 | 2.507 | 2.179 | 1.962 | 1.781 | 1.708 | 1.370 | 1.037 | 0.949 | 0.853 | 0.711 | 0.457 |
| 1 | 3.235 | 2.147 | 1.852 | 1.614 | 1.456 | 1.363 | 1.046 | 0.783 | 0.676 | 0.574 | 0.413 | 0.180 |


| layer | logit lens nats/subtoken | tuned lens nats/subtoken | tuned minus final | readable (tuned) |
|---|---|---|---|---|
| 0 | 18.357 | 6.181 | 2.834 | no |
| 1 | 18.288 | 4.861 | 1.514 | yes |
| 2 | 15.865 | 4.537 | 1.190 | yes |
| 3 | 14.334 | 4.288 | 0.941 | yes |
| 4 | 13.005 | 4.137 | 0.790 | yes |
| 5 | 11.552 | 4.060 | 0.713 | yes |
| 6 | 11.227 | 3.767 | 0.421 | yes |
| 7 | 12.388 | 3.524 | 0.177 | yes |
| 8 | 12.737 | 3.486 | 0.139 | yes |
| 9 | 13.278 | 3.406 | 0.059 | yes |
| 10 | 13.329 | 3.317 | -0.030 | yes |
| 11 | 12.945 | 3.292 | -0.055 | yes |
| 12 | 3.347 | 3.347 | 0.000 | yes |


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `tuned_lens_mbert.pt` | 28,356,746 | `fa6d5d8e81e76d2f` | translator weights |
