# rq1_jacobian_lens_mbert

_Jacobian-lens translators (masked analogue) and their readability._

| provenance | |
|---|---|
| run (UTC) | 2026-10-01 11:32 |
| script | `rq1_jacobian_lens.py` (sha256 `9872d70601305256`) |
| host | gnode (Linux) |
| duration | 66.0 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"batch_size": 24, "model": "bert-base-multilingual-cased", "n_sentences": 1000, "out_dir": "<earlier-repo>/sets/set1/Results_Checks/lm_units", "per_sentence": 2, "sentences": "<earlier-repo>/Results_Checks/indiccorp_sample/readability_sentences.txt", "tag": "mbert"}` |
| command | `scripts/rq1_jacobian_lens.py --model bert-base-multilingual-cased --tag mbert --batch-size 24` |


- **estimation sentences / held-out sentences**: 1,000 / 500
- **masked positions**: 2,000

## The averaged Jacobians


| layer | ‖J − I‖ / ‖I‖ (distance from the logit lens) | split-half ‖J₁ − J₂‖ / ‖J‖ |
|---|---|---|
| 0 | 0.9957 | 0.2235 |
| 1 | 0.9932 | 0.1201 |
| 2 | 0.9901 | 0.1142 |
| 3 | 0.9846 | 0.0911 |
| 4 | 0.9790 | 0.0808 |
| 5 | 0.9710 | 0.0728 |
| 6 | 0.9603 | 0.0648 |
| 7 | 0.9422 | 0.0621 |
| 8 | 0.9095 | 0.0526 |
| 9 | 0.8581 | 0.0426 |
| 10 | 0.7608 | 0.0323 |
| 11 | 0.6551 | 0.0223 |

Positions split into alternating batches, 1,008 and 992. A split-half difference small against 1 means the average is a property of the layer, not of the sample.


## Readability on the 500 held-out sentences (declared rule: within 2 nats per subtoken of the final layer)


| layer | logit lens nats/subtoken | Jacobian, linear (diagnostic) | Jacobian lens, around the mean | Jacobian minus final | readable (Jacobian) |
|---|---|---|---|---|---|
| 0 | 18.357 | 24.518 | 6.401 | 3.054 | no |
| 1 | 18.288 | 24.174 | 6.391 | 3.045 | no |
| 2 | 15.865 | 24.653 | 6.363 | 3.017 | no |
| 3 | 14.334 | 24.145 | 6.320 | 2.973 | no |
| 4 | 13.005 | 24.228 | 6.264 | 2.917 | no |
| 5 | 11.552 | 24.040 | 6.231 | 2.884 | no |
| 6 | 11.227 | 23.630 | 5.990 | 2.644 | no |
| 7 | 12.388 | 22.151 | 5.510 | 2.163 | no |
| 8 | 12.737 | 19.964 | 5.226 | 1.879 | yes |
| 9 | 13.278 | 19.040 | 4.693 | 1.346 | yes |
| 10 | 13.329 | 16.431 | 3.978 | 0.631 | yes |
| 11 | 12.945 | 14.094 | 3.331 | -0.016 | yes |
| 12 | 3.347 | 3.347 | 3.347 | 0.000 | yes |


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `readability_mbert_jacobian.csv` | 584 | `25087b19fab7fbf5` | Jacobian-lens readability per layer |
| `jacobian_lens_mbert.pt` | 28,356,830 | `c53fd620bfd13a25` | translators h -> mu_final + J_l (h - mu_l), for rq1_lm_units.py --tuned-lens |
