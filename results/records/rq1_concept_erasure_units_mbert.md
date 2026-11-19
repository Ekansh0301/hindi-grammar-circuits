# rq1_concept_erasure_units_mbert

_LEACE erasure of role or marker at every layer, at the constituents' own words only._

| provenance | |
|---|---|
| run (UTC) | 2026-10-05 13:59 |
| script | `rq1_concept_erasure_units.py` (sha256 `ed7db8580e9a68c5`) |
| host | gnode (Linux) |
| duration | 559.3 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"batch_size": 24, "conditions": ["none", "role", "marker", "random"], "erasers": "<earlier-repo>/logs/i2u_smoke/mbert/erasers_mbert.npz", "fit_limit": null, "limit": null, "model": "bert-base-multilingual-cased", "osv_pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_osv_transition_pairs.csv", "out_dir": "<earlier-repo>/sets/set1/Results_Checks/concept_erasure_units", "pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "permutations": 10000, "record_tag": null, "tag": "mbert"}` |
| command | `scripts/rq1_concept_erasure_units.py --tag mbert --model bert-base-multilingual-cased --batch-size 24 --erasers <earlier-repo>/logs/i2u_smoke/mbert/erasers_mbert.npz` |


- **fit references / units / encoder blocks**: 2,000 / 5,976 / 12
- **check 1: recomputed unerased unit states against the stored (float16) ones: largest absolute / largest relative departure / elements outside tolerance**: 0.0156 / 2.62e-02 / 0
- **role: erasers loaded from**: <earlier-repo>/logs/i2u_smoke/mbert/erasers_mbert.npz
- **marker: erasers loaded from**: <earlier-repo>/logs/i2u_smoke/mbert/erasers_mbert.npz
- **random: erasers loaded from**: <earlier-repo>/logs/i2u_smoke/mbert/erasers_mbert.npz

## Check: every block's eraser active


| eraser | layer | cross-covariance with role, share of unerased | with marker, share of unerased |
|---|---|---|---|
| role | 1 | 5.65e-08 | 9.51e-01 |
| role | 2 | 4.46e-08 | 9.35e-01 |
| role | 3 | 4.36e-08 | 8.87e-01 |
| role | 4 | 3.56e-08 | 8.60e-01 |
| role | 5 | 4.63e-08 | 8.59e-01 |
| role | 6 | 3.88e-08 | 8.31e-01 |
| role | 7 | 2.64e-08 | 8.26e-01 |
| role | 8 | 2.24e-08 | 8.31e-01 |
| role | 9 | 4.51e-08 | 8.36e-01 |
| role | 10 | 4.33e-08 | 8.59e-01 |
| role | 11 | 5.82e-08 | 8.78e-01 |
| role | 12 | 3.82e-08 | 8.81e-01 |
| marker | 1 | 7.01e-01 | 6.53e-08 |
| marker | 2 | 6.96e-01 | 4.70e-08 |
| marker | 3 | 6.47e-01 | 4.29e-08 |
| marker | 4 | 6.06e-01 | 3.98e-08 |
| marker | 5 | 6.01e-01 | 3.88e-08 |
| marker | 6 | 5.54e-01 | 5.09e-08 |
| marker | 7 | 5.13e-01 | 2.81e-08 |
| marker | 8 | 5.07e-01 | 2.69e-08 |
| marker | 9 | 5.16e-01 | 4.82e-08 |
| marker | 10 | 5.31e-01 | 3.67e-08 |
| marker | 11 | 5.47e-01 | 3.44e-08 |
| marker | 12 | 5.59e-01 | 3.55e-08 |
| random | 1 | 9.98e-01 | 9.98e-01 |
| random | 2 | 9.97e-01 | 9.99e-01 |
| random | 3 | 9.92e-01 | 9.94e-01 |
| random | 4 | 9.89e-01 | 9.90e-01 |
| random | 5 | 9.84e-01 | 9.89e-01 |
| random | 6 | 9.82e-01 | 9.89e-01 |
| random | 7 | 9.84e-01 | 9.91e-01 |
| random | 8 | 9.85e-01 | 9.90e-01 |
| random | 9 | 9.88e-01 | 9.90e-01 |
| random | 10 | 9.87e-01 | 9.90e-01 |
| random | 11 | 9.85e-01 | 9.91e-01 |
| random | 12 | 9.74e-01 | 9.83e-01 |


| eraser | layer | role probe | role majority | marker probe | marker majority |
|---|---|---|---|---|---|
| role | 1 | 0.5380 | 0.6292 | 0.5643 | 0.4098 |
| role | 6 | 0.5435 | 0.6292 | 0.8367 | 0.4098 |
| role | 8 | 0.5504 | 0.6292 | 0.8226 | 0.4098 |
| role | 12 | 0.5479 | 0.6292 | 0.7202 | 0.4098 |
| marker | 1 | 0.5924 | 0.6292 | 0.2741 | 0.4098 |
| marker | 6 | 0.6452 | 0.6292 | 0.2513 | 0.4098 |
| marker | 8 | 0.6419 | 0.6292 | 0.2391 | 0.4098 |
| marker | 12 | 0.6227 | 0.6292 | 0.2279 | 0.4098 |
| random | 1 | 0.6688 | 0.6292 | 0.5671 | 0.4098 |
| random | 6 | 0.8297 | 0.6292 | 0.8889 | 0.4098 |
| random | 8 | 0.8340 | 0.6292 | 0.8706 | 0.4098 |
| random | 12 | 0.7990 | 0.6292 | 0.8005 | 0.4098 |

- **readability references (not fit references)**: 500

## Per condition


| condition | held-out nats per subtoken | READ (both within 2 nats of none) | units' subtokens | other subtokens | reference preferred, all RQ1 pairs | same, references not used to fit | OSV defence (OSV->SOV) | OSV->OSV |
|---|---|---|---|---|---|---|---|---|
| none | 2.9470 | yes | 3.2517 | 2.4485 | 0.7428 | 0.7447 | 0.5171 | 0.7190 |
| role | 3.1871 | yes | 3.5957 | 2.5188 | 0.7046 | 0.7072 | 0.5000 | 0.6261 |
| marker | 3.1459 | yes | 3.5434 | 2.4956 | 0.7316 | 0.7336 | 0.4742 | 0.6475 |
| random | 2.9661 | yes | 3.2847 | 2.4448 | 0.7475 | 0.7483 | 0.5262 | 0.7288 |


## Change in the OSV defence and in the RQ1 preference, against no erasure and against random


| pairs | eraser | against | n | change in reference-preferred rate | document sign-flip p |
|---|---|---|---|---|---|
| OSV->SOV | role | none | 2286 | -0.01706 | 0.7598 |
| RQ1 pairs | role | none | 8922 | -0.03822 | 9.999e-05 |
| OSV->SOV | role | random | 2286 | -0.02625 | 0.6758 |
| RQ1 pairs | role | random | 8922 | -0.04293 | 9.999e-05 |
| OSV->SOV | marker | none | 2286 | -0.04287 | 0.6995 |
| RQ1 pairs | marker | none | 8922 | -0.01121 | 0.0178 |
| OSV->SOV | marker | random | 2286 | -0.05206 | 0.5548 |
| RQ1 pairs | marker | random | 8922 | -0.01592 | 0.0017 |
| OSV->SOV | random | none | 2286 | 0.009186 | 0.5413 |
| RQ1 pairs | random | none | 8922 | 0.004707 | 0.1021 |


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `t_mberteu0_s0.csv` | 1,200,356 | `334d057fa869e541` | RQ1 pairs, condition none |
| `osv_mberteu0.csv` | 646,633 | `186882520de1b727` | OSV transition pairs, condition none |
| `t_mberteu1_s0.csv` | 1,200,514 | `43d99e16de1664e6` | RQ1 pairs, condition role |
| `osv_mberteu1.csv` | 645,565 | `7a7f845ab5705c30` | OSV transition pairs, condition role |
| `t_mberteu2_s0.csv` | 1,200,886 | `da942dd16f248783` | RQ1 pairs, condition marker |
| `osv_mberteu2.csv` | 648,075 | `af3ff4acd22a65c9` | OSV transition pairs, condition marker |
| `t_mberteu4_s0.csv` | 1,200,360 | `e879f41ea41e5000` | RQ1 pairs, condition random |
| `osv_mberteu4.csv` | 646,869 | `af713e034496c207` | OSV transition pairs, condition random |
