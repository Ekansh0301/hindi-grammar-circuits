# rq1_jacobian_lens_indicbert

_Jacobian-lens translators (masked analogue) and their readability._

| provenance | |
|---|---|
| run (UTC) | 2026-10-01 11:03 |
| script | `rq1_jacobian_lens.py` (sha256 `9872d70601305256`) |
| host | gnode (Linux) |
| duration | 36.4 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"batch_size": 32, "model": "<earlier-repo>/local_models/IndicBERTv2-MLM-only", "n_sentences": 1000, "out_dir": "<earlier-repo>/sets/set1/Results_Checks/lm_units", "per_sentence": 2, "sentences": "<earlier-repo>/Results_Checks/indiccorp_sample/readability_sentences.txt", "tag": "indicbert"}` |
| command | `scripts/rq1_jacobian_lens.py --model <earlier-repo>/local_models/IndicBERTv2-MLM-only --tag indicbert --batch-size 32` |


- **estimation sentences / held-out sentences**: 1,000 / 500
- **masked positions**: 2,000

## The averaged Jacobians


| layer | ‖J − I‖ / ‖I‖ (distance from the logit lens) | split-half ‖J₁ − J₂‖ / ‖J‖ |
|---|---|---|
| 0 | 0.9925 | 0.2525 |
| 1 | 0.9876 | 0.2595 |
| 2 | 0.9848 | 0.2659 |
| 3 | 0.9807 | 0.2193 |
| 4 | 0.9761 | 0.1573 |
| 5 | 0.9729 | 0.0658 |
| 6 | 0.9650 | 0.0511 |
| 7 | 0.9561 | 0.0480 |
| 8 | 0.9404 | 0.0453 |
| 9 | 0.9110 | 0.0398 |
| 10 | 0.8372 | 0.0281 |
| 11 | 0.6884 | 0.0177 |

Positions split into alternating batches, 1,008 and 992. A split-half difference small against 1 means the average is a property of the layer, not of the sample.


## Readability on the 500 held-out sentences (declared rule: within 2 nats per subtoken of the final layer)


| layer | logit lens nats/subtoken | Jacobian, linear (diagnostic) | Jacobian lens, around the mean | Jacobian minus final | readable (Jacobian) |
|---|---|---|---|---|---|
| 0 | 14.672 | 17.629 | 8.048 | 5.734 | no |
| 1 | 11.381 | 17.266 | 7.995 | 5.682 | no |
| 2 | 8.052 | 16.549 | 7.849 | 5.536 | no |
| 3 | 7.930 | 16.243 | 7.733 | 5.419 | no |
| 4 | 8.622 | 16.199 | 7.542 | 5.228 | no |
| 5 | 7.643 | 16.209 | 7.409 | 5.095 | no |
| 6 | 6.825 | 15.877 | 7.216 | 4.902 | no |
| 7 | 6.867 | 15.097 | 6.901 | 4.587 | no |
| 8 | 6.108 | 13.480 | 6.300 | 3.986 | no |
| 9 | 6.115 | 11.137 | 5.197 | 2.883 | no |
| 10 | 4.311 | 7.505 | 3.502 | 1.188 | yes |
| 11 | 3.336 | 4.694 | 2.674 | 0.360 | yes |
| 12 | 2.314 | 2.314 | 2.314 | 0.000 | yes |


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `readability_indicbert_jacobian.csv` | 577 | `a5caed90f59a62a7` | Jacobian-lens readability per layer |
| `jacobian_lens_indicbert.pt` | 28,357,006 | `9a433f21337c4ce4` | translators h -> mu_final + J_l (h - mu_l), for rq1_lm_units.py --tuned-lens |
