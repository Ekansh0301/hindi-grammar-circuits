# rq1_jacobian_lens_muril

_Jacobian-lens translators (masked analogue) and their readability._

| provenance | |
|---|---|
| run (UTC) | 2026-10-01 11:02 |
| script | `rq1_jacobian_lens.py` (sha256 `9872d70601305256`) |
| host | gnode (Linux) |
| duration | 36.1 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"batch_size": 32, "model": "<earlier-repo>/local_models/muril-base-cased", "n_sentences": 1000, "out_dir": "<earlier-repo>/sets/set1/Results_Checks/lm_units", "per_sentence": 2, "sentences": "<earlier-repo>/Results_Checks/indiccorp_sample/readability_sentences.txt", "tag": "muril"}` |
| command | `scripts/rq1_jacobian_lens.py --model <earlier-repo>/local_models/muril-base-cased --tag muril --batch-size 32` |


- **estimation sentences / held-out sentences**: 1,000 / 500
- **masked positions**: 2,000

## The averaged Jacobians


| layer | ‖J − I‖ / ‖I‖ (distance from the logit lens) | split-half ‖J₁ − J₂‖ / ‖J‖ |
|---|---|---|
| 0 | 0.9998 | 0.0946 |
| 1 | 0.9997 | 0.0991 |
| 2 | 0.9996 | 0.0876 |
| 3 | 0.9995 | 0.0770 |
| 4 | 0.9993 | 0.0740 |
| 5 | 0.9991 | 0.0702 |
| 6 | 0.9990 | 0.0676 |
| 7 | 0.9986 | 0.0604 |
| 8 | 0.9981 | 0.0580 |
| 9 | 0.9972 | 0.0529 |
| 10 | 0.9947 | 0.0400 |
| 11 | 0.9901 | 0.0215 |

Positions split into alternating batches, 1,008 and 992. A split-half difference small against 1 means the average is a property of the layer, not of the sample.


## Readability on the 500 held-out sentences (declared rule: within 2 nats per subtoken of the final layer)


| layer | logit lens nats/subtoken | Jacobian, linear (diagnostic) | Jacobian lens, around the mean | Jacobian minus final | readable (Jacobian) |
|---|---|---|---|---|---|
| 0 | 85.427 | 15.459 | 8.955 | 6.206 | no |
| 1 | 102.256 | 15.453 | 8.943 | 6.195 | no |
| 2 | 87.858 | 15.429 | 8.793 | 6.044 | no |
| 3 | 70.937 | 15.381 | 8.533 | 5.785 | no |
| 4 | 65.310 | 15.348 | 8.378 | 5.630 | no |
| 5 | 70.454 | 15.300 | 8.157 | 5.409 | no |
| 6 | 88.053 | 15.280 | 7.983 | 5.234 | no |
| 7 | 96.631 | 15.197 | 7.603 | 4.854 | no |
| 8 | 92.265 | 15.047 | 6.880 | 4.132 | no |
| 9 | 96.294 | 14.710 | 5.783 | 3.034 | no |
| 10 | 100.432 | 14.022 | 4.226 | 1.478 | yes |
| 11 | 114.889 | 13.225 | 3.325 | 0.576 | yes |
| 12 | 2.749 | 2.749 | 2.749 | 0.000 | yes |


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `readability_muril_jacobian.csv` | 572 | `957f6dd99162ff92` | Jacobian-lens readability per layer |
| `jacobian_lens_muril.pt` | 28,356,830 | `16f93731dc32bde3` | translators h -> mu_final + J_l (h - mu_l), for rq1_lm_units.py --tuned-lens |
