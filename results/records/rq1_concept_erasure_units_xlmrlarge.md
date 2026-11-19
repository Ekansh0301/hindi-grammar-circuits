# rq1_concept_erasure_units_xlmrlarge

_LEACE erasure of role or marker at every layer, at the constituents' own words only._

| provenance | |
|---|---|
| run (UTC) | 2026-10-05 14:25 |
| script | `rq1_concept_erasure_units.py` (sha256 `ed7db8580e9a68c5`) |
| host | gnode (Linux) |
| duration | 584.8 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"batch_size": 16, "conditions": ["none", "role", "marker", "random"], "erasers": null, "fit_limit": null, "limit": null, "model": "xlm-roberta-large", "osv_pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_osv_transition_pairs.csv", "out_dir": "<earlier-repo>/sets/set1/Results_Checks/concept_erasure_units", "pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "permutations": 10000, "record_tag": null, "tag": "xlmrlarge"}` |
| command | `scripts/rq1_concept_erasure_units.py --tag xlmrlarge --model xlm-roberta-large --batch-size 16` |


- **fit references / units / encoder blocks**: 2,000 / 5,976 / 24
- **check 1: recomputed unerased unit states against the stored (float16) ones: largest absolute / largest relative departure / elements outside tolerance**: 0.0091 / 1.44e-01 / 0
- **role: rank removed per block**: 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
- **marker: rank removed per block**: 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
- **random: rank removed per block**: 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2

## Check: every block's eraser active


| eraser | layer | cross-covariance with role, share of unerased | with marker, share of unerased |
|---|---|---|---|
| role | 1 | 7.19e-08 | 9.54e-01 |
| role | 2 | 6.83e-08 | 9.33e-01 |
| role | 3 | 8.04e-08 | 9.21e-01 |
| role | 4 | 6.60e-08 | 9.06e-01 |
| role | 5 | 5.96e-08 | 9.05e-01 |
| role | 6 | 6.57e-08 | 9.05e-01 |
| role | 7 | 5.42e-08 | 8.97e-01 |
| role | 8 | 3.61e-08 | 8.79e-01 |
| role | 9 | 4.34e-08 | 8.75e-01 |
| role | 10 | 4.42e-08 | 8.70e-01 |
| role | 11 | 4.80e-08 | 8.82e-01 |
| role | 12 | 4.75e-08 | 8.86e-01 |
| role | 13 | 7.00e-08 | 9.05e-01 |
| role | 14 | 3.77e-08 | 9.14e-01 |
| role | 15 | 5.55e-08 | 9.10e-01 |
| role | 16 | 6.70e-08 | 9.14e-01 |
| role | 17 | 4.26e-08 | 9.18e-01 |
| role | 18 | 6.82e-08 | 9.31e-01 |
| role | 19 | 6.91e-08 | 9.27e-01 |
| role | 20 | 7.42e-08 | 9.42e-01 |
| role | 21 | 5.86e-08 | 9.41e-01 |
| role | 22 | 8.74e-08 | 9.36e-01 |
| role | 23 | 5.85e-08 | 9.25e-01 |
| role | 24 | 2.51e-07 | 8.76e-01 |
| marker | 1 | 7.08e-01 | 9.12e-08 |
| marker | 2 | 6.93e-01 | 6.36e-08 |
| marker | 3 | 6.74e-01 | 5.95e-08 |
| marker | 4 | 6.58e-01 | 6.36e-08 |
| marker | 5 | 6.56e-01 | 8.58e-08 |
| marker | 6 | 6.55e-01 | 5.25e-08 |
| marker | 7 | 6.46e-01 | 7.45e-08 |
| marker | 8 | 6.31e-01 | 6.37e-08 |
| marker | 9 | 6.14e-01 | 6.88e-08 |
| marker | 10 | 5.81e-01 | 5.58e-08 |
| marker | 11 | 6.05e-01 | 5.34e-08 |
| marker | 12 | 5.91e-01 | 4.78e-08 |
| marker | 13 | 5.92e-01 | 5.92e-08 |
| marker | 14 | 5.99e-01 | 7.91e-08 |
| marker | 15 | 5.96e-01 | 5.98e-08 |
| marker | 16 | 5.97e-01 | 7.09e-08 |
| marker | 17 | 6.12e-01 | 6.15e-08 |
| marker | 18 | 6.05e-01 | 6.08e-08 |
| marker | 19 | 5.98e-01 | 6.84e-08 |
| marker | 20 | 6.28e-01 | 7.49e-08 |
| marker | 21 | 6.44e-01 | 8.12e-08 |
| marker | 22 | 6.51e-01 | 1.05e-07 |
| marker | 23 | 6.49e-01 | 1.11e-07 |
| marker | 24 | 6.08e-01 | 2.79e-07 |
| random | 1 | 1.00e+00 | 9.99e-01 |
| random | 2 | 9.99e-01 | 9.96e-01 |
| random | 3 | 9.96e-01 | 9.93e-01 |
| random | 4 | 9.95e-01 | 9.93e-01 |
| random | 5 | 9.91e-01 | 9.92e-01 |
| random | 6 | 9.88e-01 | 9.91e-01 |
| random | 7 | 9.87e-01 | 9.92e-01 |
| random | 8 | 9.85e-01 | 9.91e-01 |
| random | 9 | 9.90e-01 | 9.92e-01 |
| random | 10 | 9.89e-01 | 9.91e-01 |
| random | 11 | 9.89e-01 | 9.91e-01 |
| random | 12 | 9.89e-01 | 9.91e-01 |
| random | 13 | 9.91e-01 | 9.93e-01 |
| random | 14 | 9.96e-01 | 9.95e-01 |
| random | 15 | 9.94e-01 | 9.94e-01 |
| random | 16 | 9.92e-01 | 9.95e-01 |
| random | 17 | 9.92e-01 | 9.92e-01 |
| random | 18 | 9.92e-01 | 9.86e-01 |
| random | 19 | 9.92e-01 | 9.85e-01 |
| random | 20 | 9.94e-01 | 9.87e-01 |
| random | 21 | 9.97e-01 | 9.87e-01 |
| random | 22 | 9.99e-01 | 9.86e-01 |
| random | 23 | 9.99e-01 | 9.86e-01 |
| random | 24 | 9.90e-01 | 9.71e-01 |


| eraser | layer | role probe | role majority | marker probe | marker majority |
|---|---|---|---|---|---|
| role | 1 | 0.4729 | 0.6292 | 0.5393 | 0.4098 |
| role | 12 | 0.4719 | 0.6292 | 0.8792 | 0.4098 |
| role | 24 | 0.4729 | 0.6292 | 0.7709 | 0.4098 |
| marker | 1 | 0.5644 | 0.6292 | 0.2082 | 0.4098 |
| marker | 12 | 0.6585 | 0.6292 | 0.1757 | 0.4098 |
| marker | 24 | 0.6382 | 0.6292 | 0.1821 | 0.4098 |
| random | 1 | 0.6600 | 0.6292 | 0.5475 | 0.4098 |
| random | 12 | 0.8814 | 0.6292 | 0.9046 | 0.4098 |
| random | 24 | 0.8389 | 0.6292 | 0.8040 | 0.4098 |

- **readability references (not fit references)**: 500

## Per condition


| condition | held-out nats per subtoken | READ (both within 2 nats of none) | units' subtokens | other subtokens | reference preferred, all RQ1 pairs | same, references not used to fit | OSV defence (OSV->SOV) | OSV->OSV |
|---|---|---|---|---|---|---|---|---|
| none | 1.8150 | yes | 2.1432 | 1.3625 | 0.8090 | 0.8093 | 0.8963 | 0.9090 |
| role | 2.0403 | yes | 2.4710 | 1.4464 | 0.7923 | 0.7952 | 0.8290 | 0.8388 |
| marker | 1.9838 | yes | 2.4058 | 1.4018 | 0.8154 | 0.8164 | 0.8443 | 0.8699 |
| random | 1.8363 | yes | 2.1764 | 1.3673 | 0.8074 | 0.8082 | 0.8972 | 0.8936 |


## Change in the OSV defence and in the RQ1 preference, against no erasure and against random


| pairs | eraser | against | n | change in reference-preferred rate | document sign-flip p |
|---|---|---|---|---|---|
| OSV->SOV | role | none | 2286 | -0.06737 | 0.2223 |
| RQ1 pairs | role | none | 8923 | -0.0167 | 0.0003 |
| OSV->SOV | role | random | 2286 | -0.06824 | 0.232 |
| RQ1 pairs | role | random | 8923 | -0.01502 | 0.0007999 |
| OSV->SOV | marker | none | 2286 | -0.05206 | 0.0104 |
| RQ1 pairs | marker | none | 8923 | 0.006388 | 0.1189 |
| OSV->SOV | marker | random | 2286 | -0.05293 | 0.009599 |
| RQ1 pairs | marker | random | 8923 | 0.008069 | 0.0448 |
| OSV->SOV | random | none | 2286 | 0.0008749 | 0.943 |
| RQ1 pairs | random | none | 8923 | -0.001681 | 0.5337 |


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `erasers_xlmrlarge.npz` | 604,605,898 | `8b72cd552353e38f` | the fitted erasers, every block, for reuse |
| `t_xlmrlargeeu0_s0.csv` | 1,205,851 | `ede7a7a02926ca8e` | RQ1 pairs, condition none |
| `osv_xlmrlargeeu0.csv` | 648,352 | `ccc105b71495e1d0` | OSV transition pairs, condition none |
| `t_xlmrlargeeu1_s0.csv` | 1,202,811 | `62312882f9859f03` | RQ1 pairs, condition role |
| `osv_xlmrlargeeu1.csv` | 646,768 | `36928152a7aa8cbc` | OSV transition pairs, condition role |
| `t_xlmrlargeeu2_s0.csv` | 1,203,492 | `05337f7c786c29b6` | RQ1 pairs, condition marker |
| `osv_xlmrlargeeu2.csv` | 646,684 | `374d5d2e0636daa6` | OSV transition pairs, condition marker |
| `t_xlmrlargeeu4_s0.csv` | 1,205,552 | `3b43044f123d61eb` | RQ1 pairs, condition random |
| `osv_xlmrlargeeu4.csv` | 647,004 | `21af00e916850ddb` | OSV transition pairs, condition random |
