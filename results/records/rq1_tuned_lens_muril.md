# rq1_tuned_lens_muril

_Tuned-lens translators and their readability._

| provenance | |
|---|---|
| run (UTC) | 2026-09-17 14:21 |
| script | `rq1_tuned_lens.py` (sha256 `cf6bd803a9a9b1fa`) |
| host | gnode (Linux) |
| duration | 29.1 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"batch_size": 32, "epochs": 2, "model": "<earlier-repo>/local_models/muril-base-cased", "n_train": 3000, "out_dir": "<earlier-repo>/sets/set1/Results_Checks/lm_units", "sentences": "<earlier-repo>/Results_Checks/indiccorp_sample/readability_sentences.txt", "tag": "muril"}` |
| command | `scripts/rq1_tuned_lens.py --model <earlier-repo>/local_models/muril-base-cased --tag muril --batch-size 32` |


- **training sentences / held-out sentences**: 3,000 / 500

| epoch | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 6.400 | 6.142 | 4.902 | 4.444 | 4.204 | 4.034 | 3.978 | 3.891 | 3.447 | 2.858 | 2.072 | 1.426 |
| 1 | 5.681 | 5.279 | 3.783 | 3.237 | 2.985 | 2.745 | 2.583 | 2.429 | 2.083 | 1.579 | 0.969 | 0.530 |


| layer | logit lens nats/subtoken | tuned lens nats/subtoken | tuned minus final | readable (tuned) |
|---|---|---|---|---|
| 0 | 85.427 | 7.957 | 5.208 | no |
| 1 | 102.256 | 7.490 | 4.741 | no |
| 2 | 87.858 | 6.035 | 3.287 | no |
| 3 | 70.937 | 5.515 | 2.766 | no |
| 4 | 65.310 | 5.309 | 2.560 | no |
| 5 | 70.454 | 5.136 | 2.387 | no |
| 6 | 88.053 | 5.029 | 2.281 | no |
| 7 | 96.631 | 4.882 | 2.134 | no |
| 8 | 92.265 | 4.572 | 1.823 | yes |
| 9 | 96.294 | 4.168 | 1.420 | yes |
| 10 | 100.432 | 3.648 | 0.899 | yes |
| 11 | 114.889 | 3.263 | 0.514 | yes |
| 12 | 2.749 | 2.749 | 0.000 | yes |


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `tuned_lens_muril.pt` | 28,356,746 | `97e8f67558cd3e50` | translator weights |
