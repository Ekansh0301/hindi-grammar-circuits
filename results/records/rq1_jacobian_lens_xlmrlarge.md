# rq1_jacobian_lens_xlmrlarge

_Jacobian-lens translators (masked analogue) and their readability._

| provenance | |
|---|---|
| run (UTC) | 2026-10-01 13:59 |
| script | `rq1_jacobian_lens.py` (sha256 `9872d70601305256`) |
| host | gnode (Linux) |
| duration | 165.6 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"batch_size": 16, "model": "xlm-roberta-large", "n_sentences": 1000, "out_dir": "<earlier-repo>/sets/set1/Results_Checks/lm_units", "per_sentence": 2, "sentences": "<earlier-repo>/Results_Checks/indiccorp_sample/readability_sentences.txt", "tag": "xlmrlarge"}` |
| command | `scripts/rq1_jacobian_lens.py --model xlm-roberta-large --tag xlmrlarge --batch-size 16` |


- **estimation sentences / held-out sentences**: 1,000 / 500
- **masked positions**: 2,000

## The averaged Jacobians


| layer | ‖J − I‖ / ‖I‖ (distance from the logit lens) | split-half ‖J₁ − J₂‖ / ‖J‖ |
|---|---|---|
| 0 | 0.9996 | 0.5049 |
| 1 | 0.9989 | 0.4685 |
| 2 | 0.9984 | 0.4122 |
| 3 | 0.9974 | 0.4196 |
| 4 | 0.9972 | 0.3823 |
| 5 | 0.9968 | 0.3439 |
| 6 | 0.9961 | 0.3150 |
| 7 | 0.9955 | 0.3132 |
| 8 | 0.9945 | 0.3135 |
| 9 | 0.9937 | 0.2786 |
| 10 | 0.9929 | 0.2540 |
| 11 | 0.9922 | 0.0961 |
| 12 | 0.9910 | 0.0896 |
| 13 | 0.9891 | 0.0861 |
| 14 | 0.9878 | 0.0822 |
| 15 | 0.9861 | 0.0794 |
| 16 | 0.9828 | 0.0747 |
| 17 | 0.9778 | 0.0713 |
| 18 | 0.9706 | 0.0657 |
| 19 | 0.9571 | 0.0573 |
| 20 | 0.9285 | 0.0479 |
| 21 | 0.8758 | 0.0370 |
| 22 | 0.7939 | 0.0265 |
| 23 | 0.7365 | 0.0152 |

Positions split into alternating batches, 1,008 and 992. A split-half difference small against 1 means the average is a property of the layer, not of the sample.


## Readability on the 500 held-out sentences (declared rule: within 2 nats per subtoken of the final layer)


| layer | logit lens nats/subtoken | Jacobian, linear (diagnostic) | Jacobian lens, around the mean | Jacobian minus final | readable (Jacobian) |
|---|---|---|---|---|---|
| 0 | 22.336 | 39.318 | 8.029 | 5.790 | no |
| 1 | 25.645 | 38.898 | 8.026 | 5.787 | no |
| 2 | 26.550 | 38.522 | 7.976 | 5.737 | no |
| 3 | 27.943 | 37.505 | 7.914 | 5.674 | no |
| 4 | 26.074 | 34.132 | 7.866 | 5.626 | no |
| 5 | 24.705 | 33.271 | 7.809 | 5.569 | no |
| 6 | 22.523 | 36.256 | 7.779 | 5.540 | no |
| 7 | 21.068 | 35.198 | 7.743 | 5.503 | no |
| 8 | 19.772 | 34.107 | 7.699 | 5.460 | no |
| 9 | 18.148 | 33.361 | 7.591 | 5.351 | no |
| 10 | 16.192 | 31.516 | 7.517 | 5.278 | no |
| 11 | 13.286 | 28.187 | 7.435 | 5.196 | no |
| 12 | 12.196 | 27.029 | 7.326 | 5.087 | no |
| 13 | 11.436 | 26.080 | 7.255 | 5.015 | no |
| 14 | 11.281 | 26.044 | 7.193 | 4.954 | no |
| 15 | 10.523 | 26.185 | 7.126 | 4.887 | no |
| 16 | 9.377 | 24.799 | 7.024 | 4.785 | no |
| 17 | 8.687 | 24.782 | 6.839 | 4.600 | no |
| 18 | 6.550 | 26.158 | 6.654 | 4.415 | no |
| 19 | 5.511 | 29.448 | 6.217 | 3.977 | no |
| 20 | 4.801 | 26.772 | 5.064 | 2.824 | no |
| 21 | 3.817 | 22.150 | 3.622 | 1.383 | yes |
| 22 | 3.706 | 30.109 | 2.819 | 0.580 | yes |
| 23 | 3.306 | 32.635 | 2.431 | 0.191 | yes |
| 24 | 2.239 | 2.239 | 2.239 | 0.000 | yes |


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `readability_xlmrlarge_jacobian.csv` | 1,085 | `a94d395a645c98be` | Jacobian-lens readability per layer |
| `jacobian_lens_xlmrlarge.pt` | 100,778,566 | `489413e7daa686e3` | translators h -> mu_final + J_l (h - mu_l), for rq1_lm_units.py --tuned-lens |
