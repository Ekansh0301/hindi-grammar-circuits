# rq1_concept_erasure_units_muril

_LEACE erasure of role or marker at every layer, at the constituents' own words only._

| provenance | |
|---|---|
| run (UTC) | 2026-10-05 09:39 |
| script | `rq1_concept_erasure_units.py` (sha256 `ed7db8580e9a68c5`) |
| host | gnode (Linux) |
| duration | 299.5 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"batch_size": 32, "conditions": ["none", "role", "marker", "random"], "erasers": "<earlier-repo>/logs/i2u_smoke/muril/erasers_muril.npz", "fit_limit": null, "limit": null, "model": "<earlier-repo>/local_models/muril-base-cased", "osv_pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_osv_transition_pairs.csv", "out_dir": "<earlier-repo>/sets/set1/Results_Checks/concept_erasure_units", "pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "permutations": 10000, "record_tag": null, "tag": "muril"}` |
| command | `scripts/rq1_concept_erasure_units.py --tag muril --model <earlier-repo>/local_models/muril-base-cased --batch-size 32 --erasers <earlier-repo>/logs/i2u_smoke/muril/erasers_muril.npz` |


- **fit references / units / encoder blocks**: 2,000 / 5,976 / 12
- **check 1: recomputed unerased unit states against the stored (float16) ones: largest absolute / largest relative departure / elements outside tolerance**: 0.0029 / 1.40e-02 / 0
- **role: erasers loaded from**: <earlier-repo>/logs/i2u_smoke/muril/erasers_muril.npz
- **marker: erasers loaded from**: <earlier-repo>/logs/i2u_smoke/muril/erasers_muril.npz
- **random: erasers loaded from**: <earlier-repo>/logs/i2u_smoke/muril/erasers_muril.npz

## Check: every block's eraser active


| eraser | layer | cross-covariance with role, share of unerased | with marker, share of unerased |
|---|---|---|---|
| role | 1 | 5.11e-08 | 9.15e-01 |
| role | 2 | 3.80e-08 | 8.81e-01 |
| role | 3 | 3.06e-08 | 8.67e-01 |
| role | 4 | 2.90e-08 | 8.64e-01 |
| role | 5 | 2.69e-08 | 8.80e-01 |
| role | 6 | 2.59e-08 | 8.79e-01 |
| role | 7 | 2.70e-08 | 8.71e-01 |
| role | 8 | 2.57e-08 | 9.01e-01 |
| role | 9 | 2.49e-08 | 9.17e-01 |
| role | 10 | 2.31e-08 | 9.28e-01 |
| role | 11 | 2.76e-08 | 9.22e-01 |
| role | 12 | 7.72e-08 | 8.90e-01 |
| marker | 1 | 6.70e-01 | 5.40e-08 |
| marker | 2 | 6.14e-01 | 3.61e-08 |
| marker | 3 | 5.96e-01 | 3.30e-08 |
| marker | 4 | 5.72e-01 | 3.06e-08 |
| marker | 5 | 5.83e-01 | 3.08e-08 |
| marker | 6 | 5.91e-01 | 3.15e-08 |
| marker | 7 | 5.65e-01 | 3.07e-08 |
| marker | 8 | 5.77e-01 | 3.08e-08 |
| marker | 9 | 6.05e-01 | 2.93e-08 |
| marker | 10 | 6.22e-01 | 3.04e-08 |
| marker | 11 | 6.01e-01 | 3.34e-08 |
| marker | 12 | 5.64e-01 | 1.28e-07 |
| random | 1 | 9.97e-01 | 9.99e-01 |
| random | 2 | 9.94e-01 | 9.95e-01 |
| random | 3 | 9.91e-01 | 9.92e-01 |
| random | 4 | 9.88e-01 | 9.95e-01 |
| random | 5 | 9.94e-01 | 9.95e-01 |
| random | 6 | 9.94e-01 | 9.95e-01 |
| random | 7 | 9.93e-01 | 9.95e-01 |
| random | 8 | 9.94e-01 | 9.96e-01 |
| random | 9 | 9.95e-01 | 9.95e-01 |
| random | 10 | 9.95e-01 | 9.95e-01 |
| random | 11 | 9.92e-01 | 9.93e-01 |
| random | 12 | 9.91e-01 | 9.89e-01 |


| eraser | layer | role probe | role majority | marker probe | marker majority |
|---|---|---|---|---|---|
| role | 1 | 0.5392 | 0.6292 | 0.5174 | 0.4098 |
| role | 6 | 0.5504 | 0.6292 | 0.8302 | 0.4098 |
| role | 7 | 0.5512 | 0.6292 | 0.8345 | 0.4098 |
| role | 12 | 0.5452 | 0.6292 | 0.8246 | 0.4098 |
| marker | 1 | 0.6111 | 0.6292 | 0.2746 | 0.4098 |
| marker | 6 | 0.6794 | 0.6292 | 0.2579 | 0.4098 |
| marker | 7 | 0.6857 | 0.6292 | 0.2580 | 0.4098 |
| marker | 12 | 0.6725 | 0.6292 | 0.2512 | 0.4098 |
| random | 1 | 0.6948 | 0.6292 | 0.5348 | 0.4098 |
| random | 6 | 0.8650 | 0.6292 | 0.8543 | 0.4098 |
| random | 7 | 0.8753 | 0.6292 | 0.8646 | 0.4098 |
| random | 12 | 0.8517 | 0.6292 | 0.8624 | 0.4098 |

- **readability references (not fit references)**: 500

## Per condition


| condition | held-out nats per subtoken | READ (both within 2 nats of none) | units' subtokens | other subtokens | reference preferred, all RQ1 pairs | same, references not used to fit | OSV defence (OSV->SOV) | OSV->OSV |
|---|---|---|---|---|---|---|---|---|
| none | 1.9774 | yes | 2.5187 | 1.3139 | 0.8204 | 0.8164 | 0.8272 | 0.8542 |
| role | 2.0803 | yes | 2.6560 | 1.3745 | 0.8190 | 0.8176 | 0.7983 | 0.8128 |
| marker | 2.0667 | yes | 2.6583 | 1.3415 | 0.8364 | 0.8319 | 0.8141 | 0.8449 |
| random | 1.9835 | yes | 2.5281 | 1.3157 | 0.8208 | 0.8180 | 0.8355 | 0.8602 |


## Change in the OSV defence and in the RQ1 preference, against no erasure and against random


| pairs | eraser | against | n | change in reference-preferred rate | document sign-flip p |
|---|---|---|---|---|---|
| OSV->SOV | role | none | 2286 | -0.02887 | 0.8802 |
| RQ1 pairs | role | none | 8923 | -0.001345 | 0.7261 |
| OSV->SOV | role | random | 2286 | -0.03718 | 0.8941 |
| RQ1 pairs | role | random | 8923 | -0.001793 | 0.6384 |
| OSV->SOV | marker | none | 2286 | -0.01312 | 0.8312 |
| RQ1 pairs | marker | none | 8923 | 0.01603 | 9.999e-05 |
| OSV->SOV | marker | random | 2286 | -0.02143 | 0.8243 |
| RQ1 pairs | marker | random | 8923 | 0.01558 | 9.999e-05 |
| OSV->SOV | random | none | 2286 | 0.008311 | 0.5962 |
| RQ1 pairs | random | none | 8923 | 0.0004483 | 0.865 |


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `t_murileu0_s0.csv` | 1,206,350 | `178bc623602dc76e` | RQ1 pairs, condition none |
| `osv_murileu0.csv` | 648,229 | `853dd0750b609b26` | OSV transition pairs, condition none |
| `t_murileu1_s0.csv` | 1,204,990 | `599e19f2ace41ef3` | RQ1 pairs, condition role |
| `osv_murileu1.csv` | 647,176 | `ea3fc24984673ed7` | OSV transition pairs, condition role |
| `t_murileu2_s0.csv` | 1,205,181 | `4f8be4ea30844b3d` | RQ1 pairs, condition marker |
| `osv_murileu2.csv` | 646,114 | `d51a14cf3e1d0a36` | OSV transition pairs, condition marker |
| `t_murileu4_s0.csv` | 1,206,167 | `f2aab88b3e92799c` | RQ1 pairs, condition random |
| `osv_murileu4.csv` | 648,176 | `fae062a7f94c06d3` | OSV transition pairs, condition random |
